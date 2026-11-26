"""Phase 1 - dump every translatable string of Hyper Emerald 5.7 into translation_vi/.

    python3 translation_vi/tools/dump_all.py [rom.gba]

Dialogues (translation_vi/dialogues/dialogues_NNN.json), two independent sources merged:
  * walk  - every map's event scripts (objects, triggers, signs, map-script tables), following
            goto/call/goto_if/call_if and trainerbattle continue-scripts (tools/romdata/scripts.py rules)
  * scan  - a raw byte scan of the whole ROM >= 0x1DC000 for
            0F 00 <ptr>  loadpointer (msgbox), 67 <ptr> message, 5C <type> trainerbattle
            accepted only when the pointed-to bytes decode as real text
Tables (translation_vi/tables/): item names + descriptions, Pokedex categories + descriptions,
Journal / Quest Log texts (from patches/ sources: not in this ROM yet).

Every dumped string is checked: gen3text.encode_raw(original_en) must give back the ROM bytes.
"""
import json, os, struct, sys, collections, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
VI = os.path.dirname(HERE)
REPO = os.path.dirname(VI)
sys.path.insert(0, HERE)
from gen3text import decode, encode_raw, stats, plausible  # noqa: E402

ROM_PATH = sys.argv[1] if len(sys.argv) > 1 else "/Users/zephiel/Downloads/Pokemons/Hyper Emerald Lost Artifacts 5.7.gba"
rom = open(ROM_PATH, 'rb').read()
assert len(rom) == 0x2000000 and rom[0xAC:0xB0] == b'BPEE', "not the 32 MB BPEE ROM"
N = len(rom)
BASE = 0x08000000
LOW = 0x1DC000                     # below this: engine code / vanilla script table - never a dialogue site
PER_FILE = 400

# ROM tables (tools/romdata/SUMMARY.md, patches/dexdesc)
GMAPGROUPS, NGROUPS = 0xA54698, 38
MAPSEC = 0x5A147C
ITEMS, ITEM_STRIDE, ITEM_COUNT = 0xFC2C7C, 44, 769          # 0..768 real items
DEX, DEX_STRIDE, DEX_COUNT = 0x1250000, 32, 960
NTRAINERS = 1459


def u16(o): return struct.unpack_from('<H', rom, o)[0]
def u32(o): return struct.unpack_from('<I', rom, o)[0]
def inrom(p): return BASE <= p < BASE + N
def ptr(o):
    v = u32(o)
    return v - BASE if inrom(v) else None


def dec(off, maxlen=4000):
    t, e = decode(rom, off, maxlen)
    return t, e


def check_roundtrip(off, text, end):
    return encode_raw(text) == bytes(rom[off:end])


# ------------------------------------------------------------------ script walking
OPLEN = {0x00:0,0x01:0,0x02:0,0x03:0,0x04:4,0x05:4,0x06:5,0x07:5,0x08:1,0x09:1,0x0A:2,0x0B:2,0x0C:0,0x0D:0,
 0x0E:1,0x0F:5,0x10:2,0x11:5,0x12:5,0x13:5,0x14:2,0x15:8,0x16:4,0x17:4,0x18:4,0x19:4,0x1A:4,0x1B:2,0x1C:2,
 0x1D:5,0x1E:5,0x1F:5,0x20:8,0x21:4,0x22:4,0x23:4,0x24:4,0x25:2,0x26:4,0x27:0,0x28:2,0x29:2,0x2A:2,0x2B:2,
 0x2C:4,0x2D:0,0x2E:0,0x2F:2,0x30:0,0x31:2,0x32:0,0x33:3,0x34:2,0x35:0,0x36:2,0x37:1,0x38:1,0x39:7,0x3A:7,
 0x3B:7,0x3C:2,0x3D:7,0x3E:7,0x3F:7,0x40:7,0x41:7,0x42:4,0x43:0,0x44:4,0x45:4,0x46:4,0x47:4,0x48:2,0x49:4,
 0x4A:4,0x4B:2,0x4C:2,0x4D:2,0x4E:2,0x4F:6,0x50:8,0x51:2,0x52:4,0x53:2,0x54:4,0x55:2,0x56:4,0x57:6,0x58:4,
 0x59:4,0x5A:0,0x5B:3,0x5D:0,0x5E:0,0x5F:0,0x60:2,0x61:2,0x62:2,0x63:6,0x64:2,0x65:3,0x66:0,0x67:4,0x68:0,
 0x69:0,0x6A:0,0x6B:0,0x6C:0,0x6D:0,0x6E:2,0x6F:4,0x70:5,0x71:5,0x72:0,0x73:4,0x74:4,0x75:4,0x76:0,0x77:1,
 0x78:4,0x79:14,0x7A:2,0x7B:4,0x7C:2,0x7D:3,0x7E:1,0x7F:3,0x80:3,0x81:3,0x82:3,0x83:3,0x84:3,0x85:5,0x86:4,
 0x87:4,0x88:4,0x89:2,0x8A:3,0x8B:0,0x8C:0,0x8D:0,0x8E:0,0x8F:2,0x90:5,0x91:5,0x92:5,0x93:3,0x94:2,0x95:3,
 0x96:2,0x97:1,0x98:2,0x99:2,0x9A:1,0x9B:4,0x9C:2,0x9D:3,0x9E:2,0x9F:2,0xA0:0,0xA1:4,0xA2:8,0xA3:0,0xA4:2,
 0xA5:0,0xA6:1,0xA7:2,0xA8:5,0xA9:4,0xAA:8,0xAB:2,0xAC:4,0xAD:4,0xAE:0,0xAF:4,0xB0:4,0xB1:7,0xB2:0,0xB3:2,
 0xB4:2,0xB5:2,0xB6:5,0xB7:0,0xB8:4,0xB9:4,0xBA:4,0xBB:5,0xBC:5,0xBD:4,0xBE:4,0xBF:5,0xC0:2,0xC1:2,0xC2:2,
 0xC3:1,0xC4:7,0xC5:0,0xC6:3,0xC7:1,0xC8:4,0xC9:0,0xCA:0,0xCB:0,0xCC:5,0xCD:2,0xCE:2,0xCF:0,0xD0:2,0xD1:7,
 0xD2:3,0xD3:2,0xD4:0,0xD5:2,0xD6:0,0xD7:7,0xD8:0,0xD9:0,0xDA:0,0xDB:4,0xDC:1,0xDD:3,0xDE:3,0xDF:4,0xE0:7,
 0xE1:3,0xE2:5}
# trainerbattle <type>: number of pointers, and which (1-based) is an event script; the rest are texts
TB_PTRS = {0: 2, 1: 3, 2: 3, 3: 1, 4: 3, 5: 2, 6: 4, 7: 3, 8: 4, 9: 2, 10: 2, 11: 2, 12: 2}
TB_SCRIPT = {1: 3, 2: 3, 6: 4, 8: 4}
TB_NAMES = {0: ['intro', 'defeat'], 1: ['intro', 'defeat'], 2: ['intro', 'defeat'], 3: ['defeat'],
            4: ['intro', 'defeat', 'not_enough_mons'], 5: ['intro', 'defeat'],
            6: ['intro', 'defeat', 'not_enough_mons'], 7: ['intro', 'defeat', 'not_enough_mons'],
            8: ['intro', 'defeat', 'not_enough_mons'], 9: ['defeat', 'victory'],
            10: ['intro', 'defeat'], 11: ['intro', 'defeat'], 12: ['intro', 'defeat']}
WARPS = (0x39, 0x3A, 0x3B, 0x3D, 0xD1, 0xD7, 0xE0)
STOP = (0x02, 0x03, 0x05, 0x08, 0x0C, 0x0D, 0x24, 0xB9) + WARPS


def tb_text_slots(o):
    """trainerbattle at file offset o -> [(pointer_word_offset, role)] for its text pointers."""
    kind = rom[o + 1]
    out, names = [], iter(TB_NAMES[kind])
    for k in range(TB_PTRS[kind]):
        if TB_SCRIPT.get(kind) == k + 1: continue
        out.append((o + 6 + 4 * k, next(names)))
    return out


def walk(entry, hits, label, limit=6000):
    """Collect text references reachable from `entry` into hits: list of (text_ptr, ref_off, op, label)."""
    seen, todo, steps = set(), [entry], 0
    while todo and steps < limit:
        pc = todo.pop()
        while steps < limit:
            if not inrom(pc) or pc in seen: break
            seen.add(pc); steps += 1
            o = pc - BASE
            op = rom[o]
            if op == 0x5C:
                kind = rom[o + 1]
                if kind not in TB_PTRS: break
                for at, role in tb_text_slots(o):
                    hits.append((u32(at), at, 'trainerbattle:' + role, label))
                if kind in TB_SCRIPT:
                    todo.append(u32(o + 6 + 4 * (TB_SCRIPT[kind] - 1)))
                pc += 6 + 4 * TB_PTRS[kind]
                continue
            if op not in OPLEN: break
            if op == 0x0F and rom[o + 1] == 0:
                hits.append((u32(o + 2), o + 2, 'loadpointer', label))
            elif op == 0x67:
                hits.append((u32(o + 1), o + 1, 'message', label))
            if op in (0x04, 0x05): todo.append(u32(o + 1))
            elif op in (0x06, 0x07): todo.append(u32(o + 2))
            if op in STOP: break
            pc += 1 + OPLEN[op]


def mapsec_names():
    names = {}
    for i in range(213):
        p = ptr(MAPSEC + 8 * i + 4)
        t = dec(p, 60)[0] if p is not None else None
        names[i] = t or '?'
    return names


def enumerate_maps():
    secs = mapsec_names()
    gstarts = [ptr(GMAPGROUPS + 4 * g) for g in range(NGROUPS)]
    maps = []
    for g in range(NGROUPS):
        gs = gstarts[g]
        nxt = min([x for x in gstarts if x > gs], default=None)
        n = 0
        while True:
            o = gs + 4 * n
            if nxt is not None and o >= nxt: break
            h = ptr(o)
            if h is None or h % 4 or h + 0x1C > N: break
            lay = ptr(h)
            if lay is None or (ptr(h + 4) is None and u32(h + 4) != 0): break
            if not (1 <= u32(lay) <= 1000 and 1 <= u32(lay + 4) <= 1000): break
            maps.append(dict(group=g, num=n, name=secs.get(rom[h + 0x14], '?'),
                             events=u32(h + 4), scripts=u32(h + 8)))
            n += 1
    return maps


def entry_points(m):
    out = []
    ev = m['events']
    if inrom(ev):
        e = ev - BASE
        nobj, ncoord, nbg = rom[e], rom[e + 2], rom[e + 3]
        objs, coords, bgs = u32(e + 4), u32(e + 12), u32(e + 16)
        for i in range(nobj if inrom(objs) else 0):
            sc = u32(objs - BASE + i * 0x18 + 0x10)
            if inrom(sc): out.append(sc)
        for i in range(ncoord if inrom(coords) else 0):
            sc = u32(coords - BASE + i * 0x10 + 12)
            if inrom(sc): out.append(sc)
        for i in range(nbg if inrom(bgs) else 0):
            o = bgs - BASE + i * 0x0C
            if rom[o + 5] <= 4:
                sc = u32(o + 8)
                if inrom(sc): out.append(sc)
    ms = m['scripts']
    if inrom(ms):
        o = ms - BASE
        for _ in range(12):
            kind = rom[o]
            if kind == 0: break
            p = u32(o + 1)
            if kind in (2, 4) and inrom(p):
                t = p - BASE
                for _ in range(40):
                    if u16(t) == 0: break
                    sc = u32(t + 4)
                    if inrom(sc): out.append(sc)
                    t += 8
            elif inrom(p):
                out.append(p)
            o += 5
    return out


# ------------------------------------------------------------------ text plausibility
_cache = {}


def text_info(off):
    """(text, end, plausible) for a text pointer target (file offset)."""
    if off in _cache: return _cache[off]
    t, e = dec(off)
    ok = False
    if t is not None and e > off:
        ok = plausible(t) and check_roundtrip(off, t, e)
    _cache[off] = (t, e, ok)
    return _cache[off]


def scan_hits():
    """Raw opcode scan of [LOW, N). Returns list of (text_ptr, ref_off, op, None)."""
    hits = []
    lo_ptr, hi_ptr = BASE + LOW, BASE + N

    def good(p): return lo_ptr <= p < hi_ptr and text_info(p - BASE)[2]

    # loadpointer: 0F 00 <ptr32> 09 <std>   (msgbox = loadword 0 + callstd: all 9,478 walk-confirmed
    # loadpointers in this ROM are followed by callstd, so a scan hit must be too)
    i = rom.find(b'\x0f\x00', LOW)
    while i != -1 and i + 7 <= N:
        p = u32(i + 2)
        if rom[i + 6] == 0x09 and good(p): hits.append((p, i + 2, 'loadpointer', None))
        i = rom.find(b'\x0f\x00', i + 1)
    # message: 67 <ptr32> 66   (message + waitmessage)
    i = rom.find(b'\x67', LOW)
    while i != -1 and i + 6 <= N:
        p = u32(i + 1)
        if rom[i + 5] == 0x66 and good(p): hits.append((p, i + 1, 'message', None))
        i = rom.find(b'\x67', i + 1)
    # trainerbattle: 5C <type> <u16 trainer> <u16 local> <ptrs...>
    i = rom.find(b'\x5c', LOW)
    while i != -1 and i + 6 + 16 <= N:
        kind = rom[i + 1]
        if kind in TB_PTRS and u16(i + 2) < NTRAINERS:
            slots = tb_text_slots(i)
            texts = [(at, role, u32(at)) for at, role in slots]
            script_ok = True
            if kind in TB_SCRIPT:
                script_ok = inrom(u32(i + 6 + 4 * (TB_SCRIPT[kind] - 1)))
            nonzero = [t for t in texts if t[2] != 0]
            if script_ok and nonzero and all(good(p) for _, _, p in nonzero):
                for at, role, p in nonzero:
                    hits.append((p, at, 'trainerbattle:' + role, None))
        i = rom.find(b'\x5c', i + 1)
    return hits


def aligned_pointer_index():
    """value -> [aligned word offsets] for every aligned word pointing into [LOW, N)."""
    import numpy as np
    w = np.frombuffer(rom, dtype='<u4')
    mask = (w >= BASE + LOW) & (w < BASE + N)
    idx = collections.defaultdict(list)
    for k in np.nonzero(mask)[0]:
        idx[int(w[k])].append(int(k) * 4)
    return idx


# ------------------------------------------------------------------ dialogues
def dump_dialogues():
    walk_hits = []
    maps = enumerate_maps()
    n_entries = 0
    for m in maps:
        for sc in entry_points(m):
            n_entries += 1
            walk(sc, walk_hits, '%s (%d.%d)' % (m['name'], m['group'], m['num']))
    sc_hits = scan_hits()
    print('maps: %d, script entry points: %d, walk text refs: %d, scan text refs: %d'
          % (len(maps), n_entries, len(walk_hits), len(sc_hits)))

    recs = {}
    rejected_walk = 0
    for src, hits in (('walk', walk_hits), ('scan', sc_hits)):
        for p, at, op, label in hits:
            if not inrom(p):
                continue
            off = p - BASE
            if off < LOW:
                continue
            t, e, ok = text_info(off)
            if t is None or e == off:
                rejected_walk += src == 'walk'; continue
            if src == 'walk' and not check_roundtrip(off, t, e):
                rejected_walk += 1; continue
            r = recs.get(off)
            if r is None:
                r = recs[off] = dict(off=off, end=e, text=t, refs={}, sources=set(), maps=[], plausible=ok)
            r['refs'].setdefault(at, op)
            r['sources'].add(src)
            if label and label not in r['maps'] and len(r['maps']) < 4: r['maps'].append(label)
    print('distinct dialogue strings: %d (walk-only rejects: %d)' % (len(recs), rejected_walk))

    apidx = aligned_pointer_index()
    offs = sorted(recs)
    # mark strings that begin inside another string (shared tails)
    inside = {}
    prev = None
    for o in offs:
        if prev is not None and o < recs[prev]['end']: inside[o] = prev
        else: prev = o

    out = []
    for k, o in enumerate(offs, 1):
        r = recs[o]
        letters, hz, junk, _ = stats(r['text'])
        script_refs = set(r['refs'])
        aligned = [a for a in apidx.get(BASE + o, []) if a not in script_refs]
        e = collections.OrderedDict()
        e['id'] = 'D%05d' % k
        e['offset_hex'] = hex(o)
        e['pointer_hex'] = hex(BASE + o)
        e['original_en'] = r['text']
        e['translation_vi'] = '@@SKIP@@' if letters == 0 and hz == 0 else ''
        e['byte_len'] = r['end'] - o
        e['refs'] = [{'at': hex(a), 'op': op} for a, op in sorted(r['refs'].items())]
        if aligned: e['aligned_refs'] = [hex(a) for a in aligned]
        e['source'] = '+'.join(sorted(r['sources']))
        if r['maps']: e['maps'] = r['maps']
        if hz: e['has_chinese'] = True
        if not r['plausible']: e['low_confidence'] = True
        if o in inside: e['inside_of'] = hex(inside[o])
        out.append(e)

    d = os.path.join(VI, 'dialogues')
    os.makedirs(d, exist_ok=True)
    olds = [os.path.join(d, f) for f in os.listdir(d) if f.startswith('dialogues_') and f.endswith('.json')]
    carry(out, existing_translations(olds))
    for f in olds: os.remove(f)
    nfiles = 0
    for i in range(0, len(out), PER_FILE):
        with open(os.path.join(d, 'dialogues_%03d.json' % nfiles), 'w', encoding='utf-8') as f:
            json.dump(out[i:i + PER_FILE], f, ensure_ascii=False, indent=2)
        nfiles += 1
    return out, nfiles, len(maps), n_entries


# ------------------------------------------------------------------ tables
def fixed_field(off, size):
    t, e = dec(off, size)
    if t is None:                                   # name fills the whole field without terminator
        b = rom[off:off + size]
        t, e = decode(bytes(b) + b'\xff', 0)
        e = off + size
    return t, e


def dump_items():
    names, descs, by_ptr = [], [], collections.OrderedDict()
    for k in range(ITEM_COUNT):
        e = ITEMS + ITEM_STRIDE * k
        name, ne = fixed_field(e, 14)
        names.append(collections.OrderedDict(id=k, offset_hex=hex(e), max_bytes=13,
                                             original_en=name, translation_vi=''))
        p = ptr(e + 20)
        if p is not None:
            by_ptr.setdefault(p, []).append((k, name))
    for p, users in by_ptr.items():
        t, end = dec(p, 600)
        if t is None: continue
        letters, hz, _, _ = stats(t)
        rec = collections.OrderedDict()
        rec['offset_hex'] = hex(p); rec['pointer_hex'] = hex(BASE + p)
        rec['items'] = ['%d %s' % u for u in users[:6]] + (['... +%d' % (len(users) - 6)] if len(users) > 6 else [])
        rec['original_en'] = t
        rec['translation_vi'] = '@@SKIP@@' if letters == 0 and hz == 0 else ''
        rec['byte_len'] = end - p
        rec['pointer_at'] = [hex(ITEMS + ITEM_STRIDE * k + 20) for k, _ in users]
        if hz: rec['has_chinese'] = True
        assert check_roundtrip(p, t, end), hex(p)
        descs.append(rec)
    return names, descs


def dump_dex():
    cats, descs, by_ptr = [], [], collections.OrderedDict()
    for n in range(DEX_COUNT):
        e = DEX + DEX_STRIDE * n
        p = ptr(e + 16)
        if p is None: continue
        cat, _ = fixed_field(e, 12)
        if n > 0 and cat.strip():
            cats.append(collections.OrderedDict(dex=n, offset_hex=hex(e), max_bytes=11,
                                                original_en=cat, translation_vi=''))
        by_ptr.setdefault(p, []).append(n)
    for p, users in by_ptr.items():
        t, end = dec(p, 1000)
        if t is None: continue
        letters, hz, _, _ = stats(t)
        if letters == 0 and hz == 0: continue
        rec = collections.OrderedDict()
        rec['offset_hex'] = hex(p); rec['pointer_hex'] = hex(BASE + p)
        rec['dex'] = users
        rec['original_en'] = t
        rec['translation_vi'] = ''
        rec['byte_len'] = end - p
        rec['pointer_at'] = [hex(DEX + DEX_STRIDE * n + 16) for n in users]
        if hz: rec['has_chinese'] = True
        assert check_roundtrip(p, t, end), hex(p)
        descs.append(rec)
    return cats, descs


def dump_named_descs(names_base, name_len, ptr_of, ids, label):
    """Descriptions behind a pointer table, grouped by pointer. Names (kept English) are context only."""
    by_ptr = collections.OrderedDict()
    for i in ids:
        at = ptr_of(i)
        p = ptr(at)
        if p is None or p < LOW: continue
        name, _ = fixed_field(names_base + name_len * i, name_len)
        by_ptr.setdefault(p, []).append((i, name.strip(), at))
    out = []
    for p, users in by_ptr.items():
        t, end = dec(p, 600)
        if t is None or not plausible(t): continue
        _l, hz, _j, _c = stats(t)
        rec = collections.OrderedDict()
        rec['offset_hex'] = hex(p); rec['pointer_hex'] = hex(BASE + p)
        rec[label] = ['%d %s' % (i, n) for i, n, _ in users[:6]] + \
            (['... +%d' % (len(users) - 6)] if len(users) > 6 else [])
        rec['original_en'] = t
        rec['translation_vi'] = ''
        rec['byte_len'] = end - p
        rec['pointer_at'] = [hex(a) for _, _, a in users]
        if hz: rec['has_chinese'] = True
        assert check_roundtrip(p, t, end), hex(p)
        out.append(rec)
    return out


MOVE_NAMES, MOVE_DESC_PTRS, NMOVES = 0x1D30258, 0x1D2AD00, 936        # desc table is indexed move-1
ABIL_NAMES, ABIL_DESC_PTRS, NABIL = u32(0x1C0) - BASE, u32(0x1C4) - BASE, 400


def dump_moves():
    return dump_named_descs(MOVE_NAMES, 13, lambda m: MOVE_DESC_PTRS + 4 * (m - 1), range(1, NMOVES + 1), 'moves')


def dump_abilities():
    # the pointer table is followed directly by the strings: stop before the first byte any entry points to
    end, i = N, 0
    while ABIL_DESC_PTRS + 4 * i < end and i < NABIL:
        p = ptr(ABIL_DESC_PTRS + 4 * i)
        if p is not None and p > ABIL_DESC_PTRS: end = min(end, p)
        i += 1
    n = min(NABIL, (end - ABIL_DESC_PTRS) // 4)
    return dump_named_descs(ABIL_NAMES, 13, lambda a: ABIL_DESC_PTRS + 4 * a, range(1, n), 'abilities')


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def dump_quests():
    """Journal / Quest Log texts, from the patch sources (they are not in this ROM)."""
    pj, pq = os.path.join(REPO, 'patches', 'journal'), os.path.join(REPO, 'patches', 'questlog')
    out = []

    def add(group, key, text, ctx=None):
        e = collections.OrderedDict(id='%s.%s' % (group, key), source=group, original_en=text, translation_vi='')
        if ctx: e['context'] = ctx
        out.append(e)

    S = load_module('steps', os.path.join(pj, 'steps.py'))
    for h in ('HOENN', 'POST', 'SINNOH', 'LOST'):
        add('journal.header', h, getattr(S, h))
    for i, (head, step, text) in enumerate(S.STEPS):
        add('journal.step', '%03d' % i, text, head)
        if step.get('label'):
            add('journal.group_label', '%03d' % i, step['label'], head)
            for j, mem in enumerate(step.get('members', [])):
                add('journal.group_member', '%03d.%02d' % (i, j), mem[-1], step['label'])
    L = load_module('legends', os.path.join(pq, 'legends.py'))
    for num, name, hint, where in L.LEGENDS:
        add('questlog.legend_hint', '%04d' % num, hint, name)
        add('questlog.legend_where', '%04d' % num, where, name)
    K = load_module('keyitems', os.path.join(pq, 'keyitems.py'))
    for row in K.KEYITEMS:
        item, flag, name, hint, where = row[:5]
        add('questlog.keyitem_hint', '%d' % item, hint, name)
        add('questlog.keyitem_where', '%d' % item, where, name)
    C = load_module('sidecontent', os.path.join(pq, 'sidecontent.py'))
    for flag, name, where in C.SIDE:
        add('questlog.side_name', '%04X' % flag, name)
        add('questlog.side_where', '%04X' % flag, where, name)
    for flag, name, where in C.BADGES:
        add('questlog.badge_where', '%04X' % flag, where, name)
    P = load_module('portraits', os.path.join(pq, 'portraits.py'))
    seen = set()
    for loc, _ in P.JOURNAL:
        if loc not in seen:
            seen.add(loc); add('questlog.location', loc.replace(' ', '_'), loc)
    return out


def existing_translations(paths):
    """(offset_hex or id, original_en) -> translation_vi from files about to be overwritten."""
    old = {}
    for p in paths:
        if not os.path.exists(p): continue
        for e in json.load(open(p, encoding='utf-8')):
            tv = e.get('translation_vi') or ''
            if tv and not e.get('auto_skip'):
                old[(e.get('offset_hex') or e.get('id'), e['original_en'])] = tv
    return old


def carry(records, old):
    for e in records:
        tv = old.get((e.get('offset_hex') or e.get('id'), e['original_en']))
        if tv: e['translation_vi'] = tv; e.pop('auto_skip', None)
    return records


def write(path, obj):
    if isinstance(obj, list):
        carry(obj, existing_translations([path]))
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)


def main():
    dia, nfiles, nmaps, nentries = dump_dialogues()
    t = os.path.join(VI, 'tables')
    os.makedirs(t, exist_ok=True)
    inames, idescs = dump_items()
    write(os.path.join(t, 'items_names.json'), inames)
    write(os.path.join(t, 'items_descriptions.json'), idescs)
    cats, ddescs = dump_dex()
    write(os.path.join(t, 'pokedex_categories.json'), cats)
    write(os.path.join(t, 'pokedex_descriptions.json'), ddescs)
    quests = dump_quests()
    write(os.path.join(t, 'quests_journal_questlog.json'), quests)
    mdescs = dump_moves()
    write(os.path.join(t, 'moves_descriptions.json'), mdescs)
    adescs = dump_abilities()
    write(os.path.join(t, 'abilities_descriptions.json'), adescs)

    src = collections.Counter(e['source'] for e in dia)
    ops = collections.Counter(r['op'].split(':')[0] for e in dia for r in e['refs'])
    uniq = len(set(e['original_en'] for e in dia))
    st = collections.OrderedDict()
    st['rom'] = ROM_PATH
    st['dialogues'] = collections.OrderedDict(
        strings=len(dia), unique_texts=uniq, files=nfiles, per_file=PER_FILE,
        maps_walked=nmaps, script_entry_points=nentries,
        by_source=dict(src), refs_by_opcode=dict(ops),
        auto_skip=dict(collections.Counter(e['auto_skip'] for e in dia if 'auto_skip' in e)),
        has_chinese=sum(bool(e.get('has_chinese')) for e in dia),
        low_confidence=sum(bool(e.get('low_confidence')) for e in dia),
        inside_other_string=sum('inside_of' in e for e in dia),
        with_aligned_data_refs=sum('aligned_refs' in e for e in dia),
        total_bytes=sum(e['byte_len'] for e in dia),
        chars_to_translate=sum(len(e['original_en']) for e in dia if e['translation_vi'] != '@@SKIP@@'))
    st['tables'] = collections.OrderedDict(
        item_names=len(inames), item_descriptions=len(idescs),
        pokedex_categories=len(cats), pokedex_descriptions=len(ddescs),
        move_descriptions=len(mdescs), ability_descriptions=len(adescs),
        quest_texts=len(quests))
    st['roundtrip_check'] = 'all dumped ROM strings re-encode byte-identical'
    write(os.path.join(VI, 'stats.json'), st)
    print(json.dumps(st, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
