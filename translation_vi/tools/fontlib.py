"""Read/write glyphs of the Gen 3 latin fonts (16x16 cell, 2bpp, tiles TL TR BL BR, 64 bytes/glyph).

Row encoding (per 8px tile row, 2 bytes): d[1] = 4 left pixels, d[0] = 4 right pixels, MSB first.
Pixel values: 0 = outside, 1 = ink, 2 = shadow, 3 = background inside the glyph width.
"""
import numpy as np

FONTS = {
    # name: (glyph table offset, width table offset or None, cell w, cell h)
    'normal': (0x64C2E4, 0x6542E4),
    'narrow': (0x63BEE4, 0x643EE4),
    'short': (0x6440E4, 0x64C0E4),
    'small': (0x633CE4, 0x63BCE4),
    'small_narrow': (0x62BAE4, 0x633AE4),
}


def get_glyph(rom, base, idx):
    g = np.zeros((16, 16), dtype=np.uint8)
    d = rom[base + idx * 64: base + idx * 64 + 64]
    for t in range(4):
        tx, ty = (t & 1) * 8, (t >> 1) * 8
        for r in range(8):
            lo, hi = d[t * 16 + r * 2], d[t * 16 + r * 2 + 1]
            for k in range(4):
                g[ty + r, tx + k] = (hi >> (6 - 2 * k)) & 3
                g[ty + r, tx + 4 + k] = (lo >> (6 - 2 * k)) & 3
    return g


def put_glyph(g):
    out = bytearray(64)
    for t in range(4):
        tx, ty = (t & 1) * 8, (t >> 1) * 8
        for r in range(8):
            hi = lo = 0
            for k in range(4):
                hi |= int(g[ty + r, tx + k]) << (6 - 2 * k)
                lo |= int(g[ty + r, tx + 4 + k]) << (6 - 2 * k)
            out[t * 16 + r * 2], out[t * 16 + r * 2 + 1] = lo, hi
    return bytes(out)
