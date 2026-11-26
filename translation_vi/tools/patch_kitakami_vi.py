# -*- coding: utf-8 -*-
"""Patch Kitakami (The Teal Mask & Mochi Mayhem) story dialogues
into Pokemon Hyper Emerald 5.7 QoL v2.0 Vietnamese ROM.
"""
import os, sys, json, struct

HERE = os.path.dirname(os.path.abspath(__file__))
VI = os.path.dirname(HERE)
DIALOGUES = os.path.join(VI, 'dialogues')
BASE = 0x08000000

def patch_kitakami_vi(data, enc, alloc):
    """Patch all Kitakami story dialogues.
    Args:
        data: bytearray of the ROM
        enc: Encoder instance from insert.py with font cmap
        alloc: PoolAllocator instance
    """
    from insert import NORMALIZE

    def enc_diag(t):
        for k, v in NORMALIZE.items():
            t = t.replace(k, v)
        t = t.replace('\r\n', '\\n').replace('\n', '\\n').replace('\r', '\\n')
        return enc.encode(t, 'dialogue') + b'\xff'

    kitakami_vi_path = os.path.join(DIALOGUES, 'kitakami_vi.json')
    if not os.path.exists(kitakami_vi_path):
        b1_path = os.path.join(DIALOGUES, 'kitakami_batch1_vi.json')
        b2_path = os.path.join(DIALOGUES, 'kitakami_batch2_vi.json')
        if os.path.exists(b1_path) and os.path.exists(b2_path):
            b1 = json.load(open(b1_path, encoding='utf-8'))
            b2 = json.load(open(b2_path, encoding='utf-8'))
            items = b1 + b2
            with open(kitakami_vi_path, 'w', encoding='utf-8') as f:
                json.dump(items, f, indent=2, ensure_ascii=False)
        else:
            print("[WARN] Kitakami Vietnamese dialogue files not found yet.")
            return

    kitakami_vi = json.load(open(kitakami_vi_path, encoding='utf-8'))
    p_in_place = 0
    p_spill = 0

    for it in kitakami_vi:
        b = enc_diag(it['translation_vi'])
        orig_off = int(it['offset'], 16)
        orig_len = it['len']
        sites = [int(s, 16) for s in it['sites']]

        if len(b) <= orig_len:
            data[orig_off:orig_off + len(b)] = b
            if len(b) < orig_len:
                data[orig_off + len(b):orig_off + orig_len] = b'\xff' * (orig_len - len(b))
            p_in_place += 1
        else:
            new_off = alloc.alloc(b)
            new_p = struct.pack('<I', BASE + new_off)
            for s in sites:
                data[s:s + 4] = new_p
            p_spill += 1

    print(f"[OK] Patched {len(kitakami_vi)} Kitakami story dialogues ({p_in_place} in-place, {p_spill} moved to safe pool).")
