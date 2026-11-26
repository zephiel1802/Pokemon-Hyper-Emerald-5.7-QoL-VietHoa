#!/usr/bin/env python3
"""Render ảnh title (block LZ77 8bpp tiled 30x20 tile) từ ROM ra PNG để so sánh gốc/VIE/đã sửa.

Palette lấy từ savestate (offset 0x800, 512 byte BGR555) nên STATE PHẢI ĐƯỢC CHỤP Ở MÀN TITLE
(state chụp ở màn khác sẽ ra ảnh sai màu). Chưa tìm được palette title nằm sẵn trong ROM.
(Dùng `python3` thường, không `-I`, vì cần Pillow ở user-site.)

  python3 render_title.py ROM.gba STATE.ss1 out.png [--offset 0xFAE1A0]
"""
import argparse
import struct

from PIL import Image

from he_common import lz77, read
from inspect_savestate import load_state


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("rom")
    ap.add_argument("state")
    ap.add_argument("out")
    ap.add_argument("--offset", type=lambda s: int(s, 0), default=0xFAE1A0)
    ap.add_argument("--scale", type=int, default=3)
    args = ap.parse_args()
    rom = read(args.rom)
    st = load_state(args.state)
    pal = [((x & 31) * 8, ((x >> 5) & 31) * 8, ((x >> 10) & 31) * 8) for x in struct.unpack_from("<256H", st, 0x800)]
    r = lz77(rom, args.offset, 0x20000)
    if not r:
        raise SystemExit("block LZ77 tại 0x%X KHÔNG giải nén được (đúng triệu chứng ảnh hỏng)" % args.offset)
    d = r[0]
    im = Image.new("RGB", (240, 160))
    for t in range(600):
        for y in range(8):
            for x in range(8):
                im.putpixel(((t % 30) * 8 + x, (t // 30) * 8 + y), pal[d[t * 64 + y * 8 + x]])
    im.resize((240 * args.scale, 160 * args.scale), Image.NEAREST).save(args.out)
    print("đã ghi", args.out)


if __name__ == "__main__":
    main()
