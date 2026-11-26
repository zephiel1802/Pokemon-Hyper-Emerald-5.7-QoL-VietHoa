#!/usr/bin/env python3
"""Tìm và sửa các pointer text "mồ côi" của bản Việt hóa (pointer không được cập nhật khi text bị dịch/chuyển chỗ).

Pointer mồ côi = slot (căn hàng 4, hoặc toán hạng script `0F 0x ptr` / `67 ptr`) mà ROM gốc trỏ vào đầu một
chuỗi, bản VIE KHÔNG đổi slot đó, nhưng chuỗi ở đích không còn bắt đầu tại đó nữa.

Hai cách tìm địa chỉ mới (không đoán, chỉ áp dụng khi có bằng chứng):
  1. Theo thứ tự: trong cụm text có SỐ CHUỖI bằng nhau giữa gốc và VIE, chuỗi thứ k gốc = chuỗi thứ k VIE.
     Chỉ dùng khi các pointer đã được sửa đúng (mốc) trong cụm khớp >=95% (hoặc cụm không có mốc nào sai).
  2. Theo pointer anh em: một pointer khác trỏ CÙNG chuỗi gốc đã được sửa sang một địa chỉ duy nhất.

  python3 fix_text_pointers.py GOC.gba VIE.gba                # báo cáo
  python3 fix_text_pointers.py GOC.gba VIE.gba --out FIX.gba  # ghi bản đã sửa (từ bản sao của VIE)
"""
import argparse
import collections
import struct

import numpy as np

from he_common import (ROM_BASE, ClusterIndex, diff_clusters, is_rom_ptr, is_string_start, is_text_like,
                       read, string_starts, words_u32)


def candidate_slots(O):
    """Các slot có thể chứa pointer: mọi word căn hàng 4 + toán hạng script không căn hàng."""
    n = len(O)
    w = words_u32(O)
    m = np.nonzero((w >= ROM_BASE) & (w < ROM_BASE + n))[0]
    slots = [int(i) * 4 for i in m]
    for p in range(0, n - 6):
        if O[p] == 0x0F and O[p + 1] < 4 and (p + 2) % 4 != 0:
            slots.append(p + 2)
        elif O[p] == 0x67 and (p + 1) % 4 != 0:
            slots.append(p + 1)
    return slots


def find_orphans(O, V):
    n = len(O)
    orphans = []
    for p in candidate_slots(O):
        wo = struct.unpack_from("<I", O, p)[0]
        if not is_rom_ptr(wo, n):
            continue
        t = wo - ROM_BASE
        if not (is_string_start(O, t) and is_text_like(O, t)):
            continue
        if struct.unpack_from("<I", V, p)[0] == wo and not is_string_start(V, t):
            orphans.append((p, t))
    return orphans


def rewritten_anchors(O, V):
    """old_target -> new_target cho các slot căn hàng đã được bản VIE sửa đúng (cả hai đầu là đầu chuỗi)."""
    n = len(O)
    wO, wV = words_u32(O), words_u32(V)
    anch = {}
    for i in np.nonzero(wO != wV)[0]:
        wo, wv = int(wO[i]), int(wV[i])
        if not is_rom_ptr(wo, n):
            continue
        t, tn = wo - ROM_BASE, wv - ROM_BASE
        if t > 1 and O[t - 1] == 0xFF and 1 < tn < n and V[tn - 1] == 0xFF:
            anch[t] = tn
    return anch


def sibling_votes(O, V, extra):
    n = len(O)
    votes = collections.defaultdict(collections.Counter)
    wO, wV = words_u32(O), words_u32(V)
    for i in np.nonzero(wO != wV)[0]:
        wo, wv = int(wO[i]), int(wV[i])
        if is_rom_ptr(wo, n) and 1 < wv - ROM_BASE < n:
            votes[wo - ROM_BASE][wv - ROM_BASE] += 1
    for t, tn in extra.items():
        votes[t][tn] += 1
    for p in range(0, n - 8):
        q = p + 2 if (O[p] == 0x0F and O[p + 1] < 4 and (p + 2) % 4 != 0) else \
            (p + 1 if (O[p] == 0x67 and (p + 1) % 4 != 0) else None)
        if q is None:
            continue
        wo, wv = struct.unpack_from("<I", O, q)[0], struct.unpack_from("<I", V, q)[0]
        if wo != wv and is_rom_ptr(wo, n) and 1 < wv - ROM_BASE < n:
            votes[wo - ROM_BASE][wv - ROM_BASE] += 1
    return votes


def plan_by_order(O, V, orphans, anch):
    cidx = ClusterIndex(diff_clusters(O, V))
    by_cluster = collections.defaultdict(list)
    for p, t in orphans:
        k = cidx.find(t)
        if k:
            by_cluster[k].append((p, t))
    plan, report = {}, []
    for (a, b), lst in by_cluster.items():
        so, sv = string_starts(O, a, b), string_starts(V, a, b)
        if len(so) != len(sv):
            report.append((a, len(lst), "số chuỗi lệch %d/%d" % (len(so), len(sv))))
            continue
        idx = {s: i for i, s in enumerate(so)}
        good = bad = 0
        for t, tn in anch.items():
            if a <= t < b and t in idx:
                good, bad = (good + 1, bad) if sv[idx[t]] == tn else (good, bad + 1)
        if good + bad and good / (good + bad) < 0.95:
            report.append((a, len(lst), "mốc chỉ khớp %d/%d" % (good, good + bad)))
            continue
        for p, t in lst:
            if t in idx:
                plan[p] = (t, sv[idx[t]])
    return plan, report


def plan_by_sibling(O, V, orphans, done, plan):
    anch_extra = {t: tn for p, (t, tn) in plan.items()}
    votes = sibling_votes(O, V, anch_extra)
    out = {}
    for p, t in orphans:
        if p in done:
            continue
        c = votes.get(t)
        if c and len(c) == 1:
            tn = next(iter(c))
            if V[tn - 1] == 0xFF:
                out[p] = (t, tn)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("orig")
    ap.add_argument("vie", help="ROM đầu vào (nên là bản đã khôi phục LZ77 nếu muốn ghi chồng)")
    ap.add_argument("--out")
    args = ap.parse_args()
    O, V = read(args.orig), read(args.vie)

    orphans = find_orphans(O, V)
    print("pointer text mồ côi:", len(orphans))
    anch = rewritten_anchors(O, V)
    plan, report = plan_by_order(O, V, orphans, anch)
    print("  sửa theo thứ tự chuỗi trong cụm :", len(plan))
    for a, k, why in sorted(report, key=lambda x: -x[1])[:10]:
        print("    bỏ qua cụm 0x%X (%d pointer): %s" % (a, k, why))
    sib = plan_by_sibling(O, V, orphans, set(plan), plan)
    print("  sửa theo pointer anh em         :", len(sib))
    plan.update(sib)
    left = [(p, t) for p, t in orphans if p not in plan]
    print("  CHƯA sửa được                   :", len(left))
    for p, t in left[:20]:
        print("    slot 0x%X -> 0x%X" % (p, t))

    if args.out:
        F = bytearray(V)
        for p, (t, tn) in plan.items():
            assert struct.unpack_from("<I", F, p)[0] == ROM_BASE + t, "slot 0x%X đã bị đổi" % p
            struct.pack_into("<I", F, p, ROM_BASE + tn)
        bad = [p for p, (_, tn) in plan.items() if not is_string_start(bytes(F), tn)]
        with open(args.out, "wb") as f:
            f.write(F)
        print("đã ghi %s: %d slot, đích không phải đầu chuỗi: %d" % (args.out, len(plan), len(bad)))


if __name__ == "__main__":
    main()
