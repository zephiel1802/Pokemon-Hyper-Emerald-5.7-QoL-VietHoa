"""Phase 2/3 - insert translation_vi into a COPY of the ROM.

    python3 translation_vi/tools/insert.py [--rom in.gba] [--out out.gba] [--only ID,ID...]

Always builds from the clean input ROM + every translation_vi JSON (never edits in place, so a build is
reproducible). Rules (translation/RESUME.md + HANDOFF.md - each fixed a real bug):
  * safe allocation: in-place cluster packing for contiguous dialogue runs, with spillover into verified
    0xFF runs >= 64 bytes with safe margin, outside font, mega-expansion, and QoL feature areas
  * only the verified pointer sites recorded by dump_all.py are rewritten (script args, table slots, aligned refs),
    and only while they still hold the old pointer; nothing below 0x1DC000 is ever touched
  * a translation is rejected if it loses/changes a control token, changes the number of \\p pages,
    ends in a control code, or does not fit its box (tables) - it then stays English and is reported
Text is word-wrapped by real pixel width (the ROM's glyph-width table), not by character count.

Vietnamese diacritics use generated glyphs (make_font.py) written into free single-byte slots of the
normal font; --strip-diacritics gives the old unaccented POC output.
"""
import argparse, bisect, collections, glob, json, os, re, struct, sys, unicodedata
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
VI = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from gen3text import encode_raw, CHR2BYTE  # noqa: E402
import make_font  # noqa: E402

BASE, LOW = 0x08000000, 0x1DC000
FONT_LO, FONT_HI = 0xE3CF64, 0xF18F64
MEGA = 0x1F82521
FEAT = (0xFD8000, 0x1000000)          # QoL patch blobs live here: keep clear
MARGIN, MAXREFS, MINRUN = 64, 6, 64
GLYPH_W = 0x6542E4                    # gFontNormalLatinGlyphWidths
BUF_W = 42                            # a [BUFxx] (names) counts as 7 average glyphs

# box formats: width px, max lines (None = dialogue: pages + scrolling), join byte
FMT = {
    'dialogue': (208, None),
    'pokenav_call': (174, None),
    'items_descriptions': (104, 3),
    'moves_descriptions': (150, 2),
    'abilities_descriptions': (150, 2),
    'pokedex_descriptions': (224, 4),
}

TOKEN = re.compile(r'\[[^\]]+\]|\\[nlp]')
NORMALIZE = {'—': '-', '–': '-', '~': '-', '"': '”', '。': '.', '！': '!', '？': '?', '，': ',',
             '、': ',', '：': ':', '’': "'", '`': "'", '\u00a0': ' ', '...': '…'}
KEEP_E = [('Pokemon', 'Pokémon'), ('Pokedex', 'Pokédex'), ('Poke Ball', 'Poké Ball'),
          ('Pokenav', 'Pokénav'), ('Poke Mart', 'Poké Mart'), ('Pokeblock', 'Pokéblock')]


def strip_vi(text):
    """POC: Vietnamese -> unaccented ASCII (Đ/đ -> D/d), keeping the game's own é in Pokémon words."""
    res, pos = [], 0
    for m in TOKEN.finditer(text):
        res.append(_strip(text[pos:m.start()])); res.append(m.group(0)); pos = m.end()
    res.append(_strip(text[pos:]))
    return ''.join(res)


def _strip(s):
    s = s.replace('đ', 'd').replace('Đ', 'D')
    s = ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')
    for a, b in KEEP_E:
        s = s.replace(a, b)
    return s


class Encoder:
    def __init__(self, rom, cmap=None):
        self.w = rom[GLYPH_W:GLYPH_W + 0x100]
        self.cmap = dict(CHR2BYTE)
        self.fallbacks = collections.Counter()
        for c, b in (cmap or {}).items(): self.cmap[c] = b
        if cmap:
            for c in make_font.UPPER_ALL:             # capitals without a slot -> small letter
                if c not in self.cmap and c.lower() in self.cmap:
                    self.cmap[c] = self.cmap[c.lower()]; self.fallbacks[c] = 0

    def byte(self, ch):
        b = self.cmap.get(ch)
        if b is None: raise ValueError('unencodable %r' % ch)
        if ch in self.fallbacks: self.fallbacks[ch] += 1
        return b

    def tok_width(self, tok):
        if tok.startswith('[BUF'): return BUF_W
        if tok.startswith('[F8') or tok.startswith('[F9'): return 12
        if tok.startswith('[S'): return self.w[int(tok[2:4], 16)]
        if tok == '[Lv]': return self.w[0x34]
        return 0                                   # [FC..] colour / pause / sound

    def words(self, page):
        """page text (no \\p) -> list of (width, bytes) words; \\n \\l and spaces separate words."""
        out, wb, ww = [], bytearray(), 0
        def flush():
            nonlocal wb, ww
            if wb: out.append((ww, bytes(wb)))
            wb, ww = bytearray(), 0
        pos = 0
        for m in list(TOKEN.finditer(page)) + [None]:
            seg = page[pos:m.start()] if m else page[pos:]
            for ch in seg:
                if ch == ' ': flush(); continue
                b = self.byte(ch)
                wb.append(b); ww += self.w[b]
            if m is None: break
            t = m.group(0)
            if t in ('\\n', '\\l'): flush()
            else: wb += encode_raw(t); ww += self.tok_width(t)
            pos = m.end()
        flush()
        return out

    def wrap(self, words, width):
        sp = self.w[0]
        lines, cur, cw = [], [], 0
        for w, b in words:
            if cur and cw + sp + w > width:
                lines.append(cur); cur, cw = [], 0
            cw += (sp if cur else 0) + w
            cur.append(b)
        if cur: lines.append(cur)
        return [b'\x00'.join(l) for l in lines]

    def encode(self, text, kind):
        width, maxlines = FMT[kind]
        if maxlines is None:                       # dialogue: \p pages, line 2 = \n, then \l scroll
            pages = []
            for pg in text.split('\\p'):
                ls = self.wrap(self.words(pg), width)
                b = ls[0] if ls else b''
                for i, l in enumerate(ls[1:]):
                    b += (b'\xfe' if i == 0 else b'\xfa') + l
                pages.append(b)
            return b'\xfb'.join(pages)
        ls = self.wrap(self.words(text.replace('\\p', ' ')), width)
        if len(ls) > maxlines: return None
        return b'\xfe'.join(ls)


def ctrl_tokens(t):
    """tokens that must survive translation (names, colours, icons, sounds)."""
    return sorted(x for x in re.findall(r'\[[^\]]+\]', t) if not x.startswith('[S') and x != '[Lv]')


def check(orig, vi):
    if vi.rstrip().endswith(('\\p', '\\n', '\\l')): return 'ends with a control code'
    if vi.count('[') != vi.count(']'): return 'unbalanced []'
    if ctrl_tokens(orig) != ctrl_tokens(vi): return 'control tokens differ: %s vs %s' % (ctrl_tokens(orig), ctrl_tokens(vi))
    if orig.count('\\p') != vi.count('\\p'): return '\\p count %d != %d' % (orig.count('\\p'), vi.count('\\p'))
    return None


# Script pointers that were missed during initial dump_all scan (e.g. 0x67 without 0x66, or 0x9b messageautoscroll)
EXTRA_SCRIPT_SITES = {
    'D03623': [0x271b96],  # STD_OBTAIN_ITEM message opcode 0x67 ("Nhận được [BUF03]!")
    'D03840': [0x21acaf],  # Contest messageautoscroll opcode 0x9b
    'D02591': [0x23f153],  # Battle Frontier messageautoscroll opcode 0x9b
    'D03845': [0x27a291],  # Contest messageautoscroll opcode 0x9b
    'D03846': [0x27a2cb],  # Contest messageautoscroll opcode 0x9b
    'D03848': [0x27a915],  # Contest messageautoscroll opcode 0x9b
    'D03850': [0x27a95b],  # Contest messageautoscroll opcode 0x9b
    'D03851': [0x27a97e],  # Contest messageautoscroll opcode 0x9b
    'D03852': [0x27aa15],  # Contest messageautoscroll opcode 0x9b
}


def load_jobs(only):
    jobs = []
    for f in sorted(glob.glob(os.path.join(VI, 'dialogues', 'dialogues_*.json'))):
        kind = 'pokenav_call' if f.endswith('dialogues_match_call.json') else 'dialogue'
        for e in json.load(open(f, encoding='utf-8')):
            sites = [int(r['at'], 16) for r in e['refs']]
            if e['id'] in EXTRA_SCRIPT_SITES:
                for s in EXTRA_SCRIPT_SITES[e['id']]:
                    if s not in sites:
                        sites.append(s)
            jobs.append((kind, e['id'], e, sites))
    for kind in FMT:
        if kind in ('dialogue', 'pokenav_call'): continue
        p = os.path.join(VI, 'tables', kind + '.json')
        if not os.path.exists(p): continue
        for e in json.load(open(p, encoding='utf-8')):
            jobs.append((kind, '%s@%s' % (kind, e['offset_hex']), e, [int(a, 16) for a in e['pointer_at']]))
    jobs = [j for j in jobs if (j[2].get('translation_vi') or '').strip() not in ('', '@@SKIP@@')]
    if only: jobs = [j for j in jobs if j[1] in only]
    return jobs


def build_free_pool(rom, aligned_targets):
    tl = aligned_targets
    pool = []
    for m in re.finditer(rb'\xff{%d,}' % MINRUN, rom):
        s, e = m.start(), m.end()
        if s < LOW or not (e <= FONT_LO or s >= FONT_HI) or s >= MEGA or (e > FEAT[0] and s < FEAT[1]): continue
        if bisect.bisect_right(tl, e) - bisect.bisect_left(tl, s) > MAXREFS: continue
        lo, hi = bisect.bisect_left(tl, s - MARGIN), bisect.bisect_right(tl, e)
        forbid = sorted((max(s, tl[i] - 4), min(e, tl[i] + MARGIN)) for i in range(lo, hi))
        cur = s
        for fs, fe in forbid:
            if fs - cur >= 16: pool.append([cur + 1, fs])     # +1: keep the previous string's 0xFF
            cur = max(cur, fe)
        if e - cur >= 16: pool.append([cur + 1, e])
    pool.sort()
    return pool


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--rom', default='/Users/zephiel/Downloads/Pokemons/Hyper Emerald Lost Artifacts 5.7.gba')
    ap.add_argument('--out', default=os.path.join(VI, 'build', 'Hyper Emerald v5.7 VIE.gba'))
    ap.add_argument('--only', default='')
    ap.add_argument('--strip-diacritics', action='store_true', help='old POC mode: unaccented, no font change')
    a = ap.parse_args()
    orig = open(a.rom, 'rb').read()
    assert len(orig) == 0x2000000 and orig[0xAC:0xB0] == b'BPEE'
    data = bytearray(orig)
    allowed = np.zeros(len(orig), dtype=bool)
    jobs = load_jobs(set(x for x in a.only.split(',') if x))
    report = collections.OrderedDict(rejected=[], overflow=[], warnings=[])
    stats = collections.Counter()

    # ---- 1) Vietnamese font ----
    cmap = None
    if not a.strip_diacritics:
        freq = collections.Counter(c for j in jobs for c in j[2]['translation_vi'] if c in make_font.UPPER_ALL)
        order = sorted(make_font.UPPER_ALL, key=lambda c: (-freq[c], (make_font.UPPER_DEFAULT + make_font.UPPER_ALL).index(c)))
        cmap, touched = make_font.build_font(data, order)
        for lo, hi in touched: allowed[lo:hi] = True
        report['font'] = {'slots': {c: '0x%02X' % b for c, b in cmap.items()},
                          'capitals_used_in_text': dict(freq.most_common())}
    enc = Encoder(data, cmap)

    # ---- 2) Aligned targets & Free Pool ----
    w = np.frombuffer(orig, dtype='<u4')
    v = w[(w >= BASE) & (w < BASE + len(orig))] - BASE
    aligned_targets = sorted(set(int(x) for x in v))
    pool = build_free_pool(orig, aligned_targets)
    pool_bytes = sum(e - s for s, e in pool)

    # ---- 3) Encode translations ----
    todo = []
    for kind, jid, e, sites in jobs:
        vi = e['translation_vi'].strip()
        err = check(e['original_en'], vi)
        if err: report['rejected'].append({'id': jid, 'why': err}); stats['rejected'] += 1; continue
        text = vi
        for k, v in NORMALIZE.items(): text = text.replace(k, v)
        if a.strip_diacritics: text = strip_vi(text)
        try:
            b = enc.encode(text, kind)
        except ValueError as ex:
            report['rejected'].append({'id': jid, 'why': str(ex)}); stats['rejected'] += 1; continue
        if b is None:
            report['overflow'].append({'id': jid, 'text': text}); stats['overflow'] += 1; continue
        
        b_term = b + b'\xff'
        todo.append({
            'kind': kind, 'id': jid, 'e': e, 'sites': sites,
            'b': b_term,
            'off': int(e['offset_hex'], 16),
            'orig_len': e['byte_len'] + 1,
            'new_len': len(b_term)
        })

    # ---- 4) Clustering & Allocation Strategy ----
    # Sort by offset to cluster contiguous strings
    aligned_set = set(aligned_targets)
    todo.sort(key=lambda x: x['off'])
    clusters = []
    cur = [todo[0]]
    for it in todo[1:]:
        prev = cur[-1]
        gap = it['off'] - (prev['off'] + prev['orig_len'])
        has_referenced_data = False
        if gap > 0:
            g_start = prev['off'] + prev['orig_len']
            g_end = it['off']
            if any(t in aligned_set for t in range(g_start, g_end)):
                has_referenced_data = True
            elif not all(orig[p] in (0x00, 0xFF) for p in range(g_start, g_end)):
                has_referenced_data = True

        if 0 <= gap <= 4 and it['off'] >= LOW and not has_referenced_data:
            cur.append(it)
        else:
            clusters.append(cur)
            cur = [it]
    if cur: clusters.append(cur)

    spillover = []
    in_situ_packs = []

    for c in clusters:
        c_start = c[0]['off']
        c_orig_end = c[-1]['off'] + c[-1]['orig_len']

        # Determine safe trailing 0xFF in original ROM
        next_t_idx = bisect.bisect_right(aligned_targets, c_orig_end)
        next_t = aligned_targets[next_t_idx] if next_t_idx < len(aligned_targets) else len(orig)
        max_p = min(next_t, c_orig_end + 32)
        p = c_orig_end
        trailing_ff = 0
        while p < max_p and orig[p] == 0xFF:
            trailing_ff += 1
            p += 1

        avail = (c_orig_end - c_start)
        c_new_len = sum(it['new_len'] for it in c)

        if len(c) == 1:
            it = c[0]
            if it['new_len'] <= it['orig_len']:
                in_situ_packs.append((c_start, [it], it['orig_len']))
            elif it['new_len'] <= avail and not it['e'].get('inside_of'):
                in_situ_packs.append((c_start, [it], it['new_len']))
            else:
                spillover.append(it)
        else:
            if c_new_len <= avail:
                in_situ_packs.append((c_start, c, max(c_orig_end - c_start, c_new_len)))
            else:
                # Spill largest items until remainder fits within original span
                c_sorted = sorted(c, key=lambda x: -x['new_len'])
                target_space = c_orig_end - c_start
                cur_sum = c_new_len
                moved = set()
                for it in c_sorted:
                    if cur_sum > target_space:
                        moved.add(it['id'])
                        cur_sum -= it['new_len']
                        spillover.append(it)
                    else:
                        break
                kept = [it for it in c if it['id'] not in moved]
                if kept:
                    in_situ_packs.append((c_start, kept, target_space))

    # ---- 5) Spillover placement in free pool ----
    placed_pool = {}
    for it in sorted(spillover, key=lambda x: (-x['new_len'], x['id'])):
        b = it['b']
        if b in placed_pool: continue
        for reg in pool:
            if reg[1] - reg[0] >= len(b):
                placed_pool[b] = reg[0]
                reg[0] += len(b)
                break

    for it in spillover:
        if it['b'] not in placed_pool:
            stats['no space'] += 1
            report['warnings'].append({'id': it['id'], 'why': 'no free space'})

    # ---- 6) Apply In-Situ Packs & Repointing ----
    final_locations = {}
    ptrs_rewritten = 0

    for start_off, items, total_len in in_situ_packs:
        cur_p = start_off
        for it in items:
            new_off = cur_p
            data[new_off:new_off + it['new_len']] = it['b']
            allowed[new_off:new_off + it['new_len']] = True
            final_locations[it['id']] = new_off
            cur_p += it['new_len']

            if new_off != it['off']:
                old_p = struct.pack('<I', BASE + it['off'])
                new_p = struct.pack('<I', BASE + new_off)
                for at in it['sites']:
                    if at >= LOW and data[at:at + 4] == old_p:
                        data[at:at + 4] = new_p
                        allowed[at:at + 4] = True
                        ptrs_rewritten += 1
                for ar in it['e'].get('aligned_refs', []):
                    ar_int = int(ar, 16)
                    if ar_int >= LOW and data[ar_int:ar_int + 4] == old_p:
                        data[ar_int:ar_int + 4] = new_p
                        allowed[ar_int:ar_int + 4] = True
                        ptrs_rewritten += 1
            stats['strings in place'] += 1

        if cur_p < start_off + total_len:
            pad_len = (start_off + total_len) - cur_p
            data[cur_p:cur_p + pad_len] = b'\xff' * pad_len
            allowed[cur_p:cur_p + pad_len] = True
            stats['bytes freed (0xFF padding)'] += pad_len

    # ---- 7) Apply Free Pool Placed Strings & Repointing ----
    for b, off in placed_pool.items():
        data[off:off + len(b)] = b
        allowed[off:off + len(b)] = True

    for it in spillover:
        if it['b'] not in placed_pool: continue
        new_off = placed_pool[it['b']]
        final_locations[it['id']] = new_off
        old_p = struct.pack('<I', BASE + it['off'])
        new_p = struct.pack('<I', BASE + new_off)
        for at in it['sites']:
            if at >= LOW and data[at:at + 4] == old_p:
                data[at:at + 4] = new_p
                allowed[at:at + 4] = True
                ptrs_rewritten += 1
        for ar in it['e'].get('aligned_refs', []):
            ar_int = int(ar, 16)
            if ar_int >= LOW and data[ar_int:ar_int + 4] == old_p:
                data[ar_int:ar_int + 4] = new_p
                allowed[ar_int:ar_int + 4] = True
                ptrs_rewritten += 1
        stats['strings moved'] += 1

    stats['pointers rewritten'] = ptrs_rewritten

    # ---- 8) Verification ----
    assert data[:LOW] == orig[:LOW], 'low ROM changed'
    diff = np.frombuffer(bytes(data), dtype=np.uint8) != np.frombuffer(orig, dtype=np.uint8)
    stray = np.where(diff & ~allowed)[0]
    assert not len(stray), 'stray changes at %s' % [hex(i) for i in stray[:5]]

    for it in todo:
        if it['id'] in final_locations:
            off = final_locations[it['id']]
            assert bytes(data[off:off + len(it['b'])]) == it['b'], 'string mismatch at %s' % hex(off)

    changed = int(diff.sum())
    if enc.fallbacks and any(enc.fallbacks.values()):
        report['warnings'].append({'why': 'capitals without a glyph printed as small letters',
                                   'counts': {c: n for c, n in enc.fallbacks.items() if n}})

    st = collections.OrderedDict(
        input=a.rom, output=a.out, translated_entries=len(jobs), **stats,
        unique_spillover_placed=len(placed_pool), bytes_spillover=sum(len(b) for b in placed_pool),
        free_pool_bytes=pool_bytes, free_pool_left=sum(e - s for s, e in pool), rom_bytes_changed=changed,
        checks='low ROM identical; every changed byte is a font glyph/width, an in-situ cluster string, '
               'a placed spillover string or a rewritten pointer; all strings verified identical in ROM')
    report['stats'] = st
    with open(os.path.join(os.path.dirname(a.out), 'build_report.json'), 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    open(a.out, 'wb').write(data)
    try:
        import patch_system_ui
        patch_system_ui.patch_system_ui(a.out, cmap=cmap)
    except Exception as ex:
        print('Error in patch_system_ui:', ex)
    print(json.dumps(st, indent=2, ensure_ascii=False))
    for k in ('rejected', 'overflow'):
        for r in report[k][:20]: print(k.upper(), r)
        if len(report[k]) > 20: print(f'... and {len(report[k]) - 20} more {k}')
    for w in report['warnings'][:10]: print('WARN', w)
    if len(report['warnings']) > 10: print(f'... and {len(report["warnings"]) - 10} more warnings')


if __name__ == '__main__':
    main()
