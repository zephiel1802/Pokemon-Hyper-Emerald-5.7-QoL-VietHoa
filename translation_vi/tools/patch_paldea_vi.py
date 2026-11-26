# -*- coding: utf-8 -*-
"""Patch Area Zero (Paldea) story dialogues and Quest Log / Journal entries
into Pokemon Hyper Emerald 5.7 QoL v1.9 Vietnamese ROM.
"""
import os, sys, json, struct, numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
VI = os.path.dirname(HERE)
DIALOGUES = os.path.join(VI, 'dialogues')
BASE = 0x08000000

class PoolAllocator:
    def __init__(self, data, blocks):
        self.data = data
        self.blocks = []
        for s, e, *rest in blocks:
            s_aligned = (s + 3) & ~3
            if e > s_aligned:
                self.blocks.append([s_aligned, e])
        self.allocated = 0

    def alloc(self, b_bytes):
        needed = len(b_bytes)
        pad = (4 - (needed % 4)) % 4
        total_needed = needed + pad
        padded_bytes = b_bytes + (b'\xff' * pad)

        # Best-fit search: pick the smallest block that fits, preserving large contiguous blocks for big tables
        best_idx = -1
        best_size = float('inf')
        for i, (s, e) in enumerate(self.blocks):
            rem = e - s
            if rem >= total_needed and rem < best_size:
                best_size = rem
                best_idx = i

        if best_idx != -1:
            block = self.blocks[best_idx]
            s, e = block
            off = s
            self.data[off:off + total_needed] = padded_bytes
            block[0] = s + total_needed
            self.allocated += total_needed
            return off

        max_avail = max((e - s for s, e in self.blocks), default=0)
        raise RuntimeError(f"Out of free pool space! Needed {needed} bytes (total {total_needed}), allocated {self.allocated} so far, max available single block is {max_avail} bytes, total remaining is {sum(e-s for s, e in self.blocks)} bytes across {len(self.blocks)} blocks.")


def patch_paldea_vi(data, enc, alloc=None):
    """Patch all Paldea story dialogues and Quest Log / Journal entries.
    Args:
        data: bytearray of the ROM
        enc: Encoder instance from insert.py with font cmap
        alloc: optional pre-configured PoolAllocator instance
    """
    import insert
    from insert import NORMALIZE

    def enc_diag(t):
        for k, v in NORMALIZE.items():
            t = t.replace(k, v)
        t = t.replace('\r\n', '\\n').replace('\n', '\\n').replace('\r', '\\n')
        return enc.encode(t, 'dialogue') + b'\xff'

    if alloc is None:
        w = np.frombuffer(data, dtype='<u4')
        aligned_targets = sorted(set(int(x) for x in (w[(w >= BASE) & (w < BASE + len(data))] - BASE)))
        pool = insert.build_free_pool(bytes(data), aligned_targets)

        free_blocks = []
        for s, e in pool:
            # Strictly avoid any QoL engine hooks, naturefix, hypertrain, hmfree, journal, evoinfo
            if s >= 0xF50000 and s < 0x1000000: continue
            if e > 0xF50000 and e <= 0x1000000: continue
            if s >= 0x1F80000: continue
            if e > 0x1F80000: continue
            if all(b == 0xFF for b in data[s:e]):
                free_blocks.append((s, e, e - s))

        alloc = PoolAllocator(data, free_blocks)

    # 1. Patch Paldea Dialogues (217 entries)
    paldea_vi_path = os.path.join(DIALOGUES, 'paldea_vi.json')
    paldea_vi = json.load(open(paldea_vi_path, encoding='utf-8'))
    p_in_place = 0
    p_spill = 0

    for it in paldea_vi:
        b = enc_diag(it['translation_vi'])
        ps = int(it['ptr_site'], 16)
        orig_off = int(it['text_offset'], 16)
        orig_len = it['orig_len']

        if len(b) <= orig_len:
            data[orig_off:orig_off + len(b)] = b
            if len(b) < orig_len:
                data[orig_off + len(b):orig_off + orig_len] = b'\xff' * (orig_len - len(b))
            p_in_place += 1
        else:
            new_off = alloc.alloc(b)
            data[ps:ps + 4] = struct.pack('<I', BASE + new_off)
            p_spill += 1

    print(f"[OK] Patched {len(paldea_vi)} Paldea story dialogues ({p_in_place} in-place, {p_spill} moved to safe pool).")

    # 2. Patch Paldea Quest Log & Journal (198 entries)
    journal_vi_path = os.path.join(DIALOGUES, 'paldea_journal_vi.json')
    journal_vi = json.load(open(journal_vi_path, encoding='utf-8'))
    j_in_place = 0
    j_spill = 0

    handled_special = set()

    # Jacq
    b_prefix = enc.encode("?[S43]", "dialogue")
    b_title = enc_diag("Area Zero: Thầy Jacq")
    b_full = b_prefix + b_title
    new_off = alloc.alloc(b_full)
    data[0x1fe2224:0x1fe2228] = struct.pack("<I", BASE + new_off)
    data[0x1fe2504:0x1fe2508] = struct.pack("<I", BASE + new_off + len(b_prefix))
    handled_special.update(["0x1fe10af", "0x1fe10b0", "0x1fe10b2"])

    # Penny
    b_prefix = enc.encode("“[S43]", "dialogue")
    b_title = enc_diag("Area Zero: Penny")
    b_full = b_prefix + b_title
    new_off = alloc.alloc(b_full)
    data[0x1fe2234:0x1fe2238] = struct.pack("<I", BASE + new_off)
    data[0x1fe2508:0x1fe250c] = struct.pack("<I", BASE + new_off + len(b_prefix))
    handled_special.update(["0x1fe11b4", "0x1fe11b5", "0x1fe11b6"])

    # Nemona
    b_prefix = enc.encode("$[S43]", "dialogue")
    b_title = enc_diag("Area Zero: Nemona")
    b_full = b_prefix + b_title
    new_off = alloc.alloc(b_full)
    data[0x1fe2254:0x1fe2258] = struct.pack("<I", BASE + new_off)
    data[0x1fe2510:0x1fe2514] = struct.pack("<I", BASE + new_off + len(b_prefix))
    handled_special.update(["0x1fe1551", "0x1fe1552", "0x1fe1554"])

    for it in journal_vi:
        off_hex = it['text_offset']
        if off_hex in handled_special:
            continue

        b = enc_diag(it['translation_vi'])
        orig_off = int(off_hex, 16)
        orig_len = it['orig_len']

        old_p = struct.pack("<I", BASE + orig_off)
        sites = [int(s, 16) for s in it.get('ptr_sites', [])]

        # Scan for any additional pointer sites targeting orig_off in the quest tables
        p_idx = 0x1fe2000
        while p_idx < 0x1ff2000:
            pos = data.find(old_p, p_idx, 0x1ff2000)
            if pos == -1: break
            if pos not in sites:
                sites.append(pos)
            p_idx = pos + 1

        if len(b) <= orig_len:
            data[orig_off:orig_off + len(b)] = b
            if len(b) < orig_len:
                data[orig_off + len(b):orig_off + orig_len] = b'\xff' * (orig_len - len(b))
            j_in_place += 1
        else:
            new_off = alloc.alloc(b)
            new_p = struct.pack("<I", BASE + new_off)
            for s in sites:
                data[s:s + 4] = new_p
            j_spill += 1

    print(f"[OK] Patched {len(journal_vi)} Paldea Quest Log & Journal entries ({j_in_place} in-place, {j_spill} moved to safe pool).")
    print(f"[OK] Total Paldea pool allocated: {alloc.allocated:,} bytes across safe free pool.")
