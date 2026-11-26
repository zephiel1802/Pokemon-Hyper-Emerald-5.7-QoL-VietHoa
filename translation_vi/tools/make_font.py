"""Phase 2.2 - Vietnamese glyphs for the normal latin font (dialogue, bag, summary, Pokédex).

Glyphs are generated from the ROM's own letters + pixel-drawn diacritics, so they match the game's
style (ink 1, shadow 2 to the right/below/diagonal, background 3 inside the glyph width).

    python3 make_font.py --preview out.png        # render all generated glyphs, no ROM written

API used by insert.py:
    build_font(data, uppercase_by_freq) -> {char: byte}   writes glyphs + widths into `data`
"""
import argparse, os, sys, unicodedata
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from fontlib import get_glyph, put_glyph  # noqa: E402

GLYPHS, WIDTHS = 0x64C2E4, 0x6542E4
FONTS_TABLE = [
    ('normal', 0x64C2E4, 0x6542E4),
    ('narrow', 0x63BEE4, 0x643EE4),
    ('short', 0x6440E4, 0x64C0E4),
    ('small', 0x633CE4, 0x63BCE4),
    ('small_narrow', 0x62BAE4, 0x633AE4),
]

# Single-byte slots that no remaining (English) string displays: blank glyphs or French/Spanish/German
# accents the English text never uses. 0x01-0x1E are Chinese lead bytes (unusable), 0x7D-0x83 are
# 1..7 px spacers, 0x2A-0x2C º ª er and 0x84 ᵉ are kept because a few strings still show them.
SLOTS = ([*range(0x1F, 0x2A), *range(0x2F, 0x34), *range(0x3F, 0x50), 0x5A, *range(0x5E, 0x7D - 6),
          *range(0x87, 0xA0), *range(0xF1, 0xF7)])
SLOTS = [s for s in SLOTS if s not in range(0x77, 0x7D)]   # 0x79-0x7C arrows (+ keep 77/78 spare)

LOWER = 'àáảãạăằắẳẵặâầấẩẫậèẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđ'   # é exists (0x1B)
UPPER_ALL = ''.join(c.upper() for c in LOWER)
UPPER_DEFAULT = 'ĐỒỪƠỞÔÊƯỜĂÂẤÁÀÝÚÓẠẢỦỔỐẾỂÍÌÒÙỨỚỰỘ'                                  # priority order
BASE_CODE = {c: 0xBB + i for i, c in enumerate('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}
BASE_CODE.update({c: 0xD5 + i for i, c in enumerate('abcdefghijklmnopqrstuvwxyz')})

# marks as bitmaps (rows of '#')
M = {
    'acute': ['.##', '#..'],
    'grave': ['##.', '..#'],
    'hook': ['##.', '..#', '.#.'],
    'hook2': ['##', '.#'],                 # compact hook for capitals (only 2 rows above the letter)
    'tilde': ['.##.#', '#.##.'],
    'hat': ['.#.', '#.#'],
    'breve': ['#..#', '.##.'],
}
TONES = {'\u0301': 'acute', '\u0300': 'grave', '\u0309': 'hook', '\u0303': 'tilde', '\u0323': 'dot'}


def decompose(c):
    """'ấ' -> ('a', 'hat', 'acute');  'ơ' -> ('o', 'horn', None);  'đ' -> ('d', 'bar', None)"""
    if c in 'đĐ': return ('d' if c == 'đ' else 'D'), 'bar', None
    d = unicodedata.normalize('NFD', c)
    base, shape, tone = d[0], None, None
    for m in d[1:]:
        if m == '\u0302': shape = 'hat'
        elif m == '\u0306': shape = 'breve'
        elif m == '\u031b': shape = 'horn'
        elif m in TONES: tone = TONES[m]
    return base, shape, tone


def stamp(ink, bmp, top, left):
    for dy, row in enumerate(bmp):
        for dx, ch in enumerate(row):
            if ch == '#' and 0 <= top + dy < 15 and 0 <= left + dx < 16:
                ink[top + dy, left + dx] = True


def render(ink, width):
    g = np.zeros((16, 16), dtype=np.uint8)
    g[:15, :width] = 3
    sh = np.zeros_like(ink)
    sh[:, 1:] |= ink[:, :-1]
    sh[1:, :] |= ink[:-1, :]
    sh[1:, 1:] |= ink[:-1, :-1]
    sh &= ~ink
    sh[15, :] = False
    sh[:, width:] = False
    g[sh] = 2
    g[ink] = 1
    return g


def make_glyph(rom, c, glyphs=GLYPHS, widths=WIDTHS):
    base, shape, tone = decompose(c)
    src = get_glyph(rom, glyphs, BASE_CODE[base])
    width = rom[widths + BASE_CODE[base]]
    ink = src == 1
    upper = base.isupper()
    if base == 'i': ink[:6] = False                         # dotless i
    cols = np.where(ink.any(0))[0]
    rows = np.where(ink.any(1))[0]
    if len(cols) == 0 or len(rows) == 0:
        return render(ink, width), width
    top, x0, x1 = rows[0], cols[0], cols[-1]
    cx = (x0 + x1) // 2
    if base == 'i': cx = x0                                 # stem
    if shape == 'bar':
        if upper:
            ink = np.roll(ink, 1, axis=1); stamp(ink, ['###'], 7, 0); width += 1
        else:
            stamp(ink, ['###'], 4, x1 - 1); width += 1
        return render(ink, width), width
    if shape == 'horn':
        r = top if base in 'oO' else top                    # top row of the letter
        if base in 'oO':
            stamp(ink, ['.#', '#.'], r - 1, x1)
        else:
            stamp(ink, ['.#', '#.'], r - 1, x1)
        width = max(width, x1 + 3)
    mark_rows = []                                          # (bitmap, top)
    if upper:
        if shape in ('hat', 'breve'):
            mark_rows.append((M[shape], 1, cx - len(M[shape][0]) // 2))
            if tone and tone != 'dot':
                b = M['hook2'] if tone == 'hook' else M[tone]
                mark_rows.append((b, 0, cx + 2))
        elif tone and tone != 'dot':
            b = M['hook2'] if tone == 'hook' else M[tone]
            mark_rows.append((b, 0 if len(b) == 2 else 0, cx - len(b[0]) // 2))
    else:
        if shape in ('hat', 'breve'):
            w = len(M[shape][0])
            mark_rows.append((M[shape], 3, cx - (w - 1) // 2))
            if tone and tone != 'dot':
                b = M[tone]
                mark_rows.append((b, 0 if len(b) == 2 else 0, cx - len(b[0]) // 2 + (1 if tone == 'hook' else 0)))
        elif tone and tone != 'dot':
            b = M[tone]
            t = 3 if len(b) == 2 else 2
            mark_rows.append((b, t, cx - len(b[0]) // 2 + (1 if base == 'i' and tone in ('acute', 'hook') else 0)))
    for b, t, l in mark_rows:
        stamp(ink, b, t, max(0, l))
    if tone == 'dot':
        if base == 'y': stamp(ink, ['#'], 9, x1 + 2)
        else: stamp(ink, ['#'], 14, cx)
    cols = np.where(ink.any(0))[0]
    width = max(width, int(cols[-1]) + 2)
    return render(ink, width), width


def build_font(data, uppercase=None):
    """Write the glyphs into `data` (bytearray ROM) for all 5 fonts. Returns ({char: byte}, [touched (lo, hi)])."""
    up = [c for c in (uppercase or UPPER_DEFAULT) if c in UPPER_ALL]
    up = list(dict.fromkeys(up))[:len(SLOTS) - len(LOWER)]
    chars = list(LOWER) + up
    assert len(chars) <= len(SLOTS)
    cmap, touched = {}, []
    for c, s in zip(chars, SLOTS):
        cmap[c] = s
        for font_name, g_base, w_base in FONTS_TABLE:
            g, w = make_glyph(data, c, glyphs=g_base, widths=w_base)
            data[g_base + s * 64: g_base + s * 64 + 64] = put_glyph(g)
            data[w_base + s] = w
            touched += [(g_base + s * 64, g_base + s * 64 + 64), (w_base + s, w_base + s + 1)]
    return cmap, touched


def fallback(c, cmap):
    """capital that did not get a slot -> its small letter (keeps the accents readable)."""
    if c in cmap: return c
    lo = c.lower()
    return lo if lo in cmap or lo == 'é' else None


def preview(rom, path, chars):
    from PIL import Image, ImageDraw
    pal = [(255, 255, 255), (20, 20, 20), (160, 160, 160), (235, 245, 255)]
    S, per = 4, 16
    n = len(chars)
    img = Image.new('RGB', (per * (16 * S + 4), ((n + per - 1) // per) * (16 * S + 4)), (255, 210, 210))
    px = img.load()
    for k, c in enumerate(chars):
        g, w = make_glyph(rom, c)
        x0, y0 = (k % per) * (16 * S + 4), (k // per) * (16 * S + 4)
        for y in range(16):
            for x in range(16):
                for a in range(S):
                    for b in range(S):
                        px[x0 + x * S + a, y0 + y * S + b] = pal[g[y, x]]
    img.save(path)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--rom', default='/Users/zephiel/Downloads/Pokemons/Hyper Emerald Lost Artifacts 5.7.gba')
    ap.add_argument('--preview')
    a = ap.parse_args()
    rom = bytearray(open(a.rom, 'rb').read())
    print(len(SLOTS), 'slots', len(LOWER), 'lower', len(SLOTS) - len(LOWER), 'upper')
    if a.preview:
        preview(rom, a.preview, list(LOWER) + list(UPPER_ALL))
