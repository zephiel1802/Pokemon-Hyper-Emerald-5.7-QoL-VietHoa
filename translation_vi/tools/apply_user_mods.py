# -*- coding: utf-8 -*-
"""Mandatory technical patches & gameplay mods for Pokemon Hyper Emerald 5.7 VI.

MUST BE PRESERVED ACROSS ALL BUILDS AND REPACKS:
1. Ability Patch duplicate check bypass (0x1f00e84 -> c7 e7)
2. Vitamin 252 EV limit (0x6c468, 0x6c470, 0x6c476, 0x6ca54, 0x6ca5c, 0x6ca62)
3. Custom Pokemon Abilities (BaseStats & ExpTable):
   - Shedinja (303): Wonder Guard (25), Sturdy (5), Sturdy (5)
   - Slaking (366): Truant (54), Huge Power (37), Huge Power (37)
   - Regigigas (539): Slow Start (112), Huge Power (37), Huge Power (37)
   - Spiritomb (495): Pressure (46), Wonder Guard (25), Infiltrator (151)
"""
import struct

CUSTOM_ABILITY_MODS = [
    ('Shedinja',  303, 0xf1a804, 0x17a071a, 25,  5,   5),
    ('Slaking',   366, 0xf1aee8, 0x17a0894, 54, 37,  37),
    ('Regigigas', 539, 0xf1c1d4, 0x17a0ca2, 112, 37,  37),
    ('Spiritomb', 495, 0xf1bd04, 0x17a0b9a, 46,  25, 151)
]

VITAMIN_EV_PATCHES = [
    (0x6c468, 0xFB), (0x6c470, 0xFC), (0x6c476, 0xFC),
    (0x6ca54, 0xFB), (0x6ca5c, 0xFC), (0x6ca62, 0xFC)
]

def apply_user_mods(rom_bytearray):
    """Apply all mandatory technical gameplay mods directly into a bytearray."""
    # 1. Bypass check trùng Ability Patch
    rom_bytearray[0x1f00e84:0x1f00e86] = bytes.fromhex('c7 e7')

    # 2. Vitamin 252 EV
    for off, val in VITAMIN_EV_PATCHES:
        rom_bytearray[off] = val

    # 3. Custom Pokemon Abilities (BaseStats & ExpTable)
    for name, idx, base_off, exp_off, ab1, ab2, ha in CUSTOM_ABILITY_MODS:
        rom_bytearray[base_off + 22] = ab1
        rom_bytearray[base_off + 23] = ab2
        rom_bytearray[base_off + 26] = ha
        struct.pack_into('<HHH', rom_bytearray, exp_off, ab1, ab2, ha)

def apply_user_mods_to_file(rom_path):
    """Read a ROM file, apply mandatory mods, and write back."""
    with open(rom_path, 'rb') as f:
        data = bytearray(f.read())
    apply_user_mods(data)
    with open(rom_path, 'wb') as f:
        f.write(data)
    print(f"[OK] Mandatory technical mods successfully applied to {rom_path}")

if __name__ == '__main__':
    import sys
    target = '/Users/zephiel/Downloads/Pokemons/Hyper Emerald v5.7 VIE.gba'
    if len(sys.argv) > 1:
        target = sys.argv[1]
    apply_user_mods_to_file(target)
