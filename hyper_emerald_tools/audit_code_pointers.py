#!/usr/bin/env python3
"""Tìm slot con trỏ căn hàng 4 mà ROM gốc trỏ vào CODE Thumb nhưng bản VIE đã đổi.

Công cụ sửa pointer text của VIE không bao giờ được động vào con trỏ hàm. Nếu có, game sẽ nhảy vào chỗ
sai (vd. bảng 0x1D37CE0: entry mất bit Thumb -> `bx` vào chế độ ARM -> Undefined exception).

Kết quả cần xem tay: con trỏ nằm trong literal pool của code hoặc cửa sổ cắt ngang con trỏ script
có thể bị báo nhầm (đích "giống code"). Con trỏ hàm thật nằm trong BẢNG nhiều entry liền nhau.

  python3 audit_code_pointers.py GOC.gba VIE.gba
  python3 audit_code_pointers.py GOC.gba VIE.gba --restore FIX.gba --slots 0x1D37ED8 0x1D37EDC
"""
import argparse
import struct

import numpy as np
from capstone import CS_ARCH_ARM, CS_MODE_THUMB, Cs

from he_common import ROM_BASE, is_rom_ptr, read, words_u32

md = Cs(CS_ARCH_ARM, CS_MODE_THUMB)


def code_like(R, t):
    ins = list(md.disasm(R[t:t + 30], t))
    if len(ins) < 10 or any(i.mnemonic in ("svc", "udf") for i in ins):
        return False
    if ins[0].mnemonic not in ("push", "ldr", "movs", "adds", "sub", "mov", "cmp", "lsls", "bl", "ldrb", "b"):
        return False
    return any(i.mnemonic in ("push", "pop", "bx") for i in ins[:12])


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("orig")
    ap.add_argument("vie")
    ap.add_argument("--restore", help="ghi bản sao của VIE với các slot (--slots) trả về giá trị gốc")
    ap.add_argument("--slots", nargs="*", type=lambda s: int(s, 0), default=[])
    args = ap.parse_args()
    O, V = read(args.orig), read(args.vie)
    n = len(O)
    wO, wV = words_u32(O), words_u32(V)
    hits = []
    for i in np.nonzero((wO != wV) & ((wO & 1) == 1) & (wO >= ROM_BASE) & (wO < ROM_BASE + n))[0]:
        t = int(wO[i]) - ROM_BASE - 1  # địa chỉ hàm thật (bỏ bit Thumb)
        if t >= n or t % 2:
            continue
        if t > 0 and O[t] == 0xFF:  # byte ngay trước địa chỉ lẻ là 0xFF -> đầu chuỗi text, không phải hàm
            continue
        if code_like(O, t):
            hits.append((int(i) * 4, int(wO[i]), int(wV[i])))
    print("slot trỏ vào code Thumb (theo ROM gốc) nhưng đã bị đổi ở VIE:", len(hits))
    for p, o, v in hits:
        note = "  <-- giá trị mới không còn là con trỏ Thumb" if not (is_rom_ptr(v, n) and v & 1) else ""
        print("  0x%07X  %08X -> %08X%s" % (p, o, v, note))
    if args.restore:
        F = bytearray(V)
        for p in args.slots:
            F[p:p + 4] = O[p:p + 4]
        with open(args.restore, "wb") as f:
            f.write(F)
        print("đã ghi %s, khôi phục %d slot" % (args.restore, len(args.slots)))


if __name__ == "__main__":
    main()
