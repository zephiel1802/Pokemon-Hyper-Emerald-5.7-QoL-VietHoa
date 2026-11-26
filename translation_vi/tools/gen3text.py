"""Gen 3 text codec for Hyper Emerald 5.7 (English build), lossless.

decode(rom, off)  -> (text, end_offset)   end_offset = index of the 0xFF terminator
encode_raw(text)  -> bytes (no terminator, NO word-wrap)

Token syntax is the one translation/inserter.py already understands, so a dumped string can be
fed straight back into the inserter:
    \\n  0xFE new line         \\l  0xFA scroll line        \\p  0xFB new page
    [BUFxx]   0xFD xx  (01 player, 02-04 STR_VAR_1-3, 06 rival ...)
    [FCxx..]  0xFC ext-ctrl + its argument bytes (colour, pause, sound ...)
    [F8xx] [F9xx]  key icon / extra symbol      [F7]  0xF7
    [Lv]  0x34      [Sxx] any other single byte  [?xx] / [?xxyy] undecodable bytes
Newline tokens are written as a literal backslash + letter (two characters), never as a real
newline character.

Leftover Chinese (two-byte GB2312 scheme of the original hack) is decoded to real hanzi so it is
visible and translatable; encode_raw maps it back to the same two bytes.

The guarantee checked by dump_all.py: encode_raw(decode(x)) == x for every dumped string.
"""

# --- single-byte charmap (matches translation/inserter.py ENC) ---
STD = {0x00: ' '}
for _i in range(10): STD[0xA1 + _i] = chr(48 + _i)
for _i in range(26): STD[0xBB + _i] = chr(65 + _i)
for _i in range(26): STD[0xD5 + _i] = chr(97 + _i)
STD.update({0xAB: '!', 0xAC: '?', 0xAD: '.', 0xAE: '-', 0xAF: '·', 0xB0: '…', 0xB1: '“', 0xB2: '”',
            0xB3: '‘', 0xB4: "'", 0xB5: '♂', 0xB6: '♀', 0xB7: '$', 0xB8: ',', 0xB9: '×', 0xBA: '/',
            0x1B: 'é', 0x06: 'É', 0xF0: ':', 0x2D: '&', 0x2E: '+', 0x35: '=', 0x36: ';',
            0x5B: '%', 0x5C: '(', 0x5D: ')'})
CHR2BYTE = {v: k for k, v in STD.items()}

# 0xFC sub-command -> number of argument bytes (pokeemerald EXT_CTRL_CODE_*)
FC_ARGS = {0x00: 0, 0x01: 1, 0x02: 1, 0x03: 1, 0x04: 3, 0x05: 1, 0x06: 1, 0x07: 0, 0x08: 1, 0x09: 0,
           0x0A: 0, 0x0B: 2, 0x0C: 1, 0x0D: 1, 0x0E: 1, 0x0F: 0, 0x10: 2, 0x11: 1, 0x12: 1, 0x13: 1,
           0x14: 1, 0x15: 0, 0x16: 0, 0x17: 0, 0x18: 0}

# --- Chinese two-byte scheme (translation/RESUME.md) ---
_GB = []
for _hi in range(0xB0, 0xF8):
    for _lo in range(0xA1, 0xFF):
        try:
            _GB.append(bytes([_hi, _lo]).decode('gb2312'))
        except UnicodeDecodeError:
            _GB.append(None)
CN_LEADS = set(range(0x01, 0x1F)) - {0x06, 0x1B}


def _adj(lead):
    a = lead - 1
    if lead > 6: a -= 1
    if lead > 0x1B: a -= 1
    return a


def _hanzi(lead, second):
    if second > 0xF6: return None
    o = _adj(lead) * 247 + second
    return _GB[o] if o < len(_GB) else None


HANZI2BYTES = {}
for _l in sorted(CN_LEADS):
    for _s in range(0xF7):
        _c = _hanzi(_l, _s)
        if _c and _c not in HANZI2BYTES:
            HANZI2BYTES[_c] = bytes([_l, _s])


def is_hanzi(c):
    return '\u4e00' <= c <= '\u9fff'


def decode(rom, off, maxlen=4000):
    """Decode the FF-terminated string at `off`. Returns (text, end) or (None, None) if no 0xFF
    is met within `maxlen` bytes."""
    out = []
    i = off
    n = len(rom)
    lim = min(n, off + maxlen)
    while i < lim:
        b = rom[i]
        if b == 0xFF:
            return ''.join(out), i
        if b == 0xFE: out.append('\\n'); i += 1; continue
        if b == 0xFA: out.append('\\l'); i += 1; continue
        if b == 0xFB: out.append('\\p'); i += 1; continue
        if b == 0xFD and i + 1 < n:
            out.append('[BUF%02X]' % rom[i + 1]); i += 2; continue
        if b == 0xFC and i + 1 < n:
            na = FC_ARGS.get(rom[i + 1], 0)
            out.append('[FC%s]' % bytes(rom[i + 1:i + 2 + na]).hex().upper()); i += 2 + na; continue
        if b in (0xF8, 0xF9) and i + 1 < n:
            out.append('[%02X%02X]' % (b, rom[i + 1])); i += 2; continue
        if b == 0xF7: out.append('[F7]'); i += 1; continue
        if b == 0x34: out.append('[Lv]'); i += 1; continue
        if b in CN_LEADS:
            s2 = rom[i + 1] if i + 1 < n else 0xFF
            c = _hanzi(b, s2) if s2 != 0xFF else None
            if c and HANZI2BYTES.get(c) == bytes([b, s2]):
                out.append(c)
            elif s2 != 0xFF:
                out.append('[?%02X%02X]' % (b, s2))
            else:
                out.append('[?%02X]' % b); i += 1; continue
            i += 2; continue
        if b in STD: out.append(STD[b]); i += 1; continue
        out.append('[S%02X]' % b); i += 1
    return None, None


def encode_raw(text):
    """Exact inverse of decode (no normalisation, no wrapping)."""
    out = bytearray()
    i = 0
    L = len(text)
    while i < L:
        c = text[i]
        if c == '\\' and i + 1 < L and text[i + 1] in 'nlp':
            out.append({'n': 0xFE, 'l': 0xFA, 'p': 0xFB}[text[i + 1]]); i += 2; continue
        if c == '[':
            j = text.index(']', i)
            tok = text[i + 1:j]
            if tok.startswith('BUF'): out += bytes([0xFD, int(tok[3:], 16)])
            elif tok.startswith('FC'): out += b'\xfc' + bytes.fromhex(tok[2:])
            elif tok == 'F7': out.append(0xF7)
            elif tok[:2] in ('F8', 'F9'): out += bytes.fromhex(tok)
            elif tok == 'Lv': out.append(0x34)
            elif tok.startswith('S'): out.append(int(tok[1:], 16))
            elif tok.startswith('?'): out += bytes.fromhex(tok[1:])
            else: raise ValueError('bad token [%s]' % tok)
            i = j + 1
            continue
        if c in CHR2BYTE: out.append(CHR2BYTE[c]); i += 1; continue
        if c in HANZI2BYTES: out += HANZI2BYTES[c]; i += 1; continue
        raise ValueError('unencodable char %r' % c)
    return bytes(out)


# [Sxx] bytes that are real glyphs in this ROM's fonts, not junk:
#   37-3E  Chinese punctuation 。—~、,!?:   51/52 ¿ ¡   53-54 PK MN   55-59 PO Ké BL OC K
#   79-7D  arrows / D-pad   A0 "re"   F1-F6  Ä Ö Ü ä ö ü
LEGIT_S = set(range(0x37, 0x3F)) | {0x51, 0x52} | set(range(0x53, 0x5A)) | set(range(0x79, 0x7E)) \
    | {0xA0} | set(range(0xF1, 0xF7))
# GB2312 level-1 (common) hanzi = rows 0xB0-0xD7; random bytes land in level 2 just as often
COMMON_HANZI = {c for c, b in HANZI2BYTES.items()
                if bytes([b[0], b[1]]) and (lambda o: o < (0xD8 - 0xB0) * 94)(_adj(b[0]) * 247 + b[1])}


def stats(text):
    """(letters, hanzi, junk_tokens, common_hanzi) of a decoded string."""
    import re
    letters = sum(1 for c in text if c.isascii() and c.isalpha()) + text.count('é') + text.count('É')
    hz = sum(1 for c in text if is_hanzi(c))
    common = sum(1 for c in text if c in COMMON_HANZI)
    junk = text.count('[?') + sum(1 for m in re.finditer(r'\[S([0-9A-F]{2})\]', text)
                                  if int(m.group(1), 16) not in LEGIT_S)
    return letters, hz, junk, common


def plausible(text):
    """Heuristic: does this decoded string look like real game text?"""
    letters, hz, junk, common = stats(text)
    if hz:
        if common < (hz if hz < 4 else 0.75 * hz): return False   # rare hanzi -> random bytes
        if junk > hz // 8: return False
        return hz >= 2 or letters >= 3
    return letters >= 3 and junk <= letters // 40
