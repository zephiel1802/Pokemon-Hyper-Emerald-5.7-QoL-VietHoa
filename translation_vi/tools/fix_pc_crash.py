"""Fix PC item withdrawal crash across all Hyper Emerald ROMs.

Root cause:
6 pointers in PC Item Storage (0x16b000 .. 0x16d000) and 3 menu description pointers
were repointed to expanded_pool_cur (0x09F825xx, >= 0x09000000 in upper 16MB ROM).
Addresses >= 0x09000000 can cause bounds check failure, and dereferencing them in
Hyper Emerald's custom menu renderer hook (0x8005878 -> 0x9f00270 -> 0x9f00150)
assumes valid 0x08xxxxxx menu context pointers.

Fix:
1. Repoint Withdrew message (0x16c280) to in-situ 0x085eac22 ('Đã rút [BUF03]\\n[BUF02].').
2. Repoint Bag full message (0x16c298) to in-situ 0x085eabe7 ('Túi đồ không còn chỗ trống nào.').
3. Repoint PC menu descriptions (0x5dfea4, 0x1f004a0, 0x5dfea8, 0x1f004a4, 0x5dfeac, 0x1f004a8)
   to in-situ 0x085eab92, 0x085eab7b, 0x085eabae.
4. Allocate 'Không có vật phẩm nào.[FC09]', 'Không có Thư nào ở đây.[FC09]',
   and 'Bạn muốn làm gì với\\nThư của [BUF02]?' in safe pool 0x36f6e0 (< 0x09000000).
"""
import json, os, struct, sys

HERE = os.path.dirname(os.path.abspath(__file__))
VI = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from insert import NORMALIZE
from gen3text import CHR2BYTE, decode

def apply_pc_fix_to_data(data):
    report_path = os.path.join(VI, 'build', 'build_report.json')
    report = json.load(open(report_path, encoding='utf-8'))
    cmap = {c: int(b, 16) for c, b in report['font']['slots'].items()}

    def enc_battle(text):
        text = text.replace('\\\\n', '\\n').replace('\\\\l', '\\l').replace('\\\\p', '\\p')
        for k, v in NORMALIZE.items(): text = text.replace(k, v)
        out = bytearray()
        i = 0
        L = len(text)
        while i < L:
            if text[i] == '\n':
                out.append(0xFE)
                i += 1
                continue
            if text[i] == '\\' and i + 1 < L and text[i + 1] in 'nlp':
                out.append({'n': 0xFE, 'l': 0xFA, 'p': 0xFB}[text[i + 1]])
                i += 2
                continue
            if text[i] == '[':
                end = text.find(']', i)
                if end != -1:
                    token = text[i:end+1]
                    if token.startswith('[BUF'):
                        code = int(token[4:6], 16)
                        out.extend([0xFD, code])
                    elif token.startswith('[FC'):
                        raw_hex = bytes.fromhex(token[3:-1])
                        out.extend([0xFC] + list(raw_hex))
                    i = end + 1
                    continue
            c = text[i]
            if c in cmap: out.append(cmap[c])
            elif c in CHR2BYTE: out.append(CHR2BYTE[c])
            elif c.lower() in cmap: out.append(cmap[c.lower()])
            else: raise ValueError(f'Cannot encode: {repr(c)}')
            i += 1
        out.append(0xFF)
        return bytes(out)

    b_items = enc_battle('Không có vật phẩm nào.[FC09]')
    b_nomail = enc_battle('Không có Thư nào ở đây.[FC09]')
    b_whatmail = enc_battle('Bạn muốn làm gì với\\nThư của [BUF02]?')
    b_store = enc_battle('Cất vật phẩm vào PC.')
    b_take = enc_battle('Lấy vật phẩm ra khỏi PC.')
    b_toss = enc_battle('Vứt bỏ vật phẩm trong PC.')
    b_withdrew = enc_battle('Đã rút [BUF03]\\n[BUF02].')
    b_bagfull = enc_battle('Túi đồ không còn\\nchỗ trống nào.')

    # 1. In-place writes
    # 0x5eab7b (23 bytes): 'Cất vật phẩm vào PC.'
    data[0x5eab7b : 0x5eab7b + len(b_store)] = b_store
    data[0x5eab7b + len(b_store) : 0x5eab7b + 23] = b'\xff' * (23 - len(b_store))

    # 0x5eab92 (28 bytes): 'Lấy vật phẩm ra khỏi PC.'
    data[0x5eab92 : 0x5eab92 + len(b_take)] = b_take
    data[0x5eab92 + len(b_take) : 0x5eab92 + 28] = b'\xff' * (28 - len(b_take))

    # 0x5eabae (35 bytes): 'Vứt bỏ vật phẩm trong PC.'
    data[0x5eabae : 0x5eabae + len(b_toss)] = b_toss
    data[0x5eabae + len(b_toss) : 0x5eabae + 35] = b'\xff' * (35 - len(b_toss))

    # 0x5eac22 (19 bytes): 'Đã rút [BUF03]\n[BUF02].'
    data[0x5eac22 : 0x5eac22 + len(b_withdrew)] = b_withdrew
    data[0x5eac22 + len(b_withdrew) : 0x5eac22 + 19] = b'\xff' * (19 - len(b_withdrew))

    # 0x5eabe7 (34 bytes): 'Túi đồ không còn\nchỗ trống nào.'
    data[0x5eabe7 : 0x5eabe7 + len(b_bagfull)] = b_bagfull
    data[0x5eabe7 + len(b_bagfull) : 0x5eabe7 + 34] = b'\xff' * (34 - len(b_bagfull))

    # 2. Alloc in safe pool sys_pool (< 0x09000000)
    off_items = 0x36f6e0
    data[off_items : off_items + len(b_items)] = b_items
    pad1 = 4 - (len(b_items) % 4) if len(b_items) % 4 != 0 else 0
    data[off_items + len(b_items) : off_items + len(b_items) + pad1] = b'\xff' * pad1

    off_nomail = off_items + len(b_items) + pad1
    data[off_nomail : off_nomail + len(b_nomail)] = b_nomail
    pad2 = 4 - (len(b_nomail) % 4) if len(b_nomail) % 4 != 0 else 0
    data[off_nomail + len(b_nomail) : off_nomail + len(b_nomail) + pad2] = b'\xff' * pad2

    off_whatmail = off_nomail + len(b_nomail) + pad2
    data[off_whatmail : off_whatmail + len(b_whatmail)] = b_whatmail
    pad3 = 4 - (len(b_whatmail) % 4) if len(b_whatmail) % 4 != 0 else 0
    data[off_whatmail + len(b_whatmail) : off_whatmail + len(b_whatmail) + pad3] = b'\xff' * pad3

    # 3. Patch pointers
    def write_p(off, target):
        data[off:off+4] = struct.pack('<I', target)

    write_p(0x16c280, 0x085eac22) # Withdrew [BUF03]\n[BUF02].
    write_p(0x16c298, 0x085eabe7) # Room in bag
    write_p(0x16b3dc, 0x08000000 + off_items) # There are no items
    write_p(0x16b428, 0x08000000 + off_items)
    write_p(0x16b0d0, 0x08000000 + off_nomail) # There's no mail
    write_p(0x16b130, 0x08000000 + off_nomail)
    write_p(0x16b790, 0x08000000 + off_whatmail) # What to do with mail

    # Description pointers
    write_p(0x5dfea4, 0x085eab92)
    write_p(0x1f004a0, 0x085eab92)
    write_p(0x5dfea8, 0x085eab7b)
    write_p(0x1f004a4, 0x085eab7b)
    write_p(0x5dfeac, 0x085eabae)
    write_p(0x1f004a8, 0x085eabae)

def apply_pc_fix(rom_path):
    print(f"Applying PC crash fix to: {rom_path}")
    with open(rom_path, 'rb') as f:
        data = bytearray(f.read())
    apply_pc_fix_to_data(data)
    with open(rom_path, 'wb') as f:
        f.write(data)
    print(f"[SUCCESS] Patched {rom_path} successfully!")

if __name__ == '__main__':
    for path in sys.argv[1:]:
        if os.path.exists(path):
            apply_pc_fix(path)
        else:
            print(f"[SKIP] Not found: {path}")
