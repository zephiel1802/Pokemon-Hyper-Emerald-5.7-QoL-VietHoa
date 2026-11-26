#!/usr/bin/env python3
"""Tìm (và tuỳ chọn khôi phục) các block LZ77 bị hỏng trong ROM Việt hóa so với ROM gốc.

Nguyên nhân thường gặp: công cụ sửa pointer quét mù toàn ROM nên ghi nhầm vào bên trong dữ liệu nén
(vd. 4 byte trong stream bitmap title bị coi là con trỏ text).

  python3 audit_lz77.py GOC.gba VIE.gba                 # chỉ báo cáo
  python3 audit_lz77.py GOC.gba VIE.gba --out FIX.gba    # khôi phục block hỏng từ ROM gốc
  python3 audit_lz77.py GOC.gba VIE.gba --scan-all ...   # thêm các block không có pointer trỏ tới
"""
import argparse

from he_common import lz77, read, words_u32, ROM_BASE


def referenced_targets(orig):
    w = words_u32(orig)
    tg = {int(x) - ROM_BASE for x in w if ROM_BASE <= x < ROM_BASE + len(orig)}
    return sorted(t for t in tg if t + 8 < len(orig) and orig[t] == 0x10)


def scan_all_targets(orig):
    """Mọi header LZ77 căn hàng 4 có kích thước hợp lý (kể cả block không ai trỏ tới)."""
    out = []
    for off in range(0, len(orig) - 8, 4):
        if orig[off] == 0x10 and orig[off + 3] == 0 and orig[off + 1] % 32 == 0:
            sz = orig[off + 1] | orig[off + 2] << 8
            if 0x400 <= sz <= 0x10000:
                out.append(off)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("orig")
    ap.add_argument("vie")
    ap.add_argument("--out", help="ghi ROM đã khôi phục ra file này (bản sao của VIE)")
    ap.add_argument("--scan-all", action="store_true",
                    help="quét cả block không được pointer tham chiếu (chỉ tính block có <=64 byte khác)")
    args = ap.parse_args()
    O, V = read(args.orig), read(args.vie)

    targets = referenced_targets(O)
    if args.scan_all:
        targets = sorted(set(targets) | set(scan_all_targets(O)))
    broken = []
    total = 0
    for t in targets:
        r = lz77(O, t)
        if not r or r[1] - t < 8:
            continue
        ln = r[1] - t
        if V[t:t + ln] == O[t:t + ln]:
            total += 1
            continue
        if args.scan_all and sum(1 for i in range(ln) if V[t + i] != O[t + i]) > 64:
            continue  # nhiều khả năng là block giả hoặc nội dung dịch thật
        total += 1
        rv = lz77(V, t)
        if rv is None:
            broken.append((t, len(r[0]), ln, "KHÔNG giải nén được"))
        elif rv[0] != r[0]:
            nd = sum(a != b for a, b in zip(r[0], rv[0]))
            broken.append((t, len(r[0]), ln, "giải nén SAI (%d byte)" % nd))
    print("block LZ77 hợp lệ trong ROM gốc: %d, hỏng ở bản VIE: %d" % (total, len(broken)))
    for t, sz, ln, why in broken:
        print("  0x%07X  giải nén=0x%X  nén=%d B  %s" % (t, sz, ln, why))
    if args.out:
        fixed = bytearray(V)
        for t, _, ln, _ in broken:
            fixed[t:t + ln] = O[t:t + ln]
        bad = sum(1 for t, *_ in broken if lz77(bytes(fixed), t)[0] != lz77(O, t)[0])
        with open(args.out, "wb") as f:
            f.write(fixed)
        print("đã ghi %s (khôi phục %d block, còn lệch sau khi khôi phục: %d)" % (args.out, len(broken), bad))


if __name__ == "__main__":
    main()
