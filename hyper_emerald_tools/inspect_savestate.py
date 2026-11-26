#!/usr/bin/env python3
"""Đọc savestate mGBA (.ss1/.ss2) để chẩn đoán game treo/crash.

In ra: chế độ CPU (cpsr), r0-r15, SP/LR của mode SYS, rồi dump stack trong IWRAM và đánh dấu các địa chỉ
return (đứng sau lệnh BL) để dựng chuỗi gọi hàm. Nếu truyền --rom, kiểm tra từng địa chỉ có thật sự sau BL.

Layout state (mGBA v7, 0x61000 byte, đã kiểm chứng): r0..r15 @0x20..0x5C, cpsr @0x60, spsr @0x64,
SP/LR của SYS/USR @0x70/0x74, VRAM @0x1000, IWRAM @0x19000, EWRAM @0x21000, palette (giả định) @0x800.
cpsr mode 0x1B = Undefined: thường là nhảy vào dữ liệu/ARM do con trỏ hàm Thumb mất bit 0.

  python3 inspect_savestate.py "X.ss2" --rom "X.gba" [--stack 0x120] [--extract state.bin]
"""
import argparse
import struct
import zlib

MODES = {0x10: "USR", 0x11: "FIQ", 0x12: "IRQ", 0x13: "SVC", 0x17: "ABT", 0x1B: "UND", 0x1F: "SYS"}


def load_state(path):
    d = open(path, "rb").read()
    if d[:8] != b"\x89PNG\r\n\x1a\n":
        raise SystemExit("không phải savestate mGBA dạng PNG")
    p = 8
    while p < len(d):
        ln, = struct.unpack(">I", d[p:p + 4])
        typ = d[p + 4:p + 8]
        if typ == b"gbAs":
            return zlib.decompress(d[p + 8:p + 8 + ln])
        p += 12 + ln
    raise SystemExit("không thấy chunk gbAs")


def is_bl_return(rom, addr):
    a = (addr & ~1) - 0x08000000
    if rom is None or a < 4 or a >= len(rom):
        return None
    h1, h2 = struct.unpack_from("<HH", rom, a - 4)
    if (h1 & 0xF800) == 0xF000 and (h2 & 0xF800) == 0xF800:
        off = ((h1 & 0x7FF) << 12) | ((h2 & 0x7FF) << 1)
        if off & 0x400000:
            off -= 0x800000
        return "BL -> 0x%X" % (0x08000000 + a + off)
    return "KHÔNG đứng sau BL"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("state")
    ap.add_argument("--rom")
    ap.add_argument("--stack", type=lambda s: int(s, 0), default=0x120, help="số byte stack cần dump")
    ap.add_argument("--extract", help="ghi state đã giải nén ra file")
    args = ap.parse_args()
    s = load_state(args.state)
    rom = open(args.rom, "rb").read() if args.rom else None
    if args.extract:
        open(args.extract, "wb").write(s)
    r = struct.unpack_from("<16I", s, 0x20)
    cpsr, spsr = struct.unpack_from("<II", s, 0x60)
    mode = MODES.get(cpsr & 0x1F, "?")
    print("title: %r  code: %r" % (s[0x10:0x1C].decode("ascii", "replace"), s[0x1C:0x20].decode("ascii", "replace")))
    print("cpsr=%08X mode=%s thumb=%d  spsr=%08X" % (cpsr, mode, (cpsr >> 5) & 1, spsr))
    for i in range(0, 16, 4):
        print("  " + "  ".join("r%-2d=%08X" % (j, r[j]) for j in range(i, i + 4)))
    sys_sp, sys_lr = struct.unpack_from("<II", s, 0x70)
    sp = r[13] if mode in ("SYS", "USR") else sys_sp
    if mode not in ("SYS", "USR"):
        print("CPU đang ở mode %s -> dùng SP/LR của SYS: sp=%08X lr=%08X" % (mode, sys_sp, sys_lr))
        if mode == "UND":
            print("!! Undefined instruction: kiểm tra bx rN với rN chẵn (con trỏ hàm Thumb mất bit 0)")
    if 0x03000000 <= sp < 0x03008000:
        print("\nstack từ SP=%08X (địa chỉ ROM lẻ = nghi return Thumb):" % sp)
        for a in range(sp, min(sp + args.stack, 0x03008000), 4):
            w = struct.unpack_from("<I", s, 0x19000 + (a - 0x03000000))[0]
            note = ""
            if 0x08000000 <= w < 0x0A000000 and w & 1:
                bl = is_bl_return(rom, w)
                note = "  <-- return? " + (bl or "")
            print("  %08X: %08X%s" % (a, w, note))


if __name__ == "__main__":
    main()
