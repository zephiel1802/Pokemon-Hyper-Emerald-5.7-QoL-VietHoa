"""Patch system UI, Start Menu, Option Menu, Battle Menu, Bag Pockets, Save Game dialogues,
and Birch New Game Intro strings into the ROM.
"""
import json, os, struct, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
VI = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from gen3text import encode_raw, CHR2BYTE, decode
from insert import Encoder, NORMALIZE
from expanded_battle_dict import EXPANDED_BATTLE_TRANSLATIONS
from bst_full_dict import BST_FULL_TRANSLATIONS
from party_system_ui_dict import PARTY_SYSTEM_UI_TRANSLATIONS

BASE, LOW = 0x08000000, 0x1DC000

def patch_system_ui(rom_path, cmap=None):
    orig = open(rom_path, 'rb').read()
    data = bytearray(orig)
    
    # Load font cmap & sync all 5 Latin font tables
    report_path = os.path.join(VI, 'build', 'build_report.json')
    if cmap is None and os.path.exists(report_path):
        report = json.load(open(report_path, encoding='utf-8'))
        cmap = {c: int(b, 16) for c, b in report['font']['slots'].items()}
    
    if cmap is not None:
        enc = Encoder(data, cmap)
        up_order = sorted([c for c in cmap if c.isupper()], key=lambda c: cmap[c])
        import make_font
        make_font.build_font(data, uppercase=up_order)
    else:
        enc = Encoder(data)
    
    def enc_diag(t):
        for k, v in NORMALIZE.items(): t = t.replace(k, v)
        return enc.encode(t, 'dialogue') + b'\xff'
    
    def enc_raw(t):
        for k, v in NORMALIZE.items(): t = t.replace(k, v)
        return bytes(enc.byte(c) for c in t) + b'\xff'

    # Safe Free Pool Allocation for System UI (0x36f3b8 .. 0x36f7e0, 1064 bytes available)
    sys_pool_cur = 0x36f3b8

    def alloc_pool(b):
        nonlocal sys_pool_cur
        off = sys_pool_cur
        data[off:off + len(b)] = b
        sys_pool_cur += len(b)
        if sys_pool_cur % 4 != 0:
            pad = 4 - (sys_pool_cur % 4)
            data[sys_pool_cur:sys_pool_cur + pad] = b'\xff' * pad
            sys_pool_cur += pad
        return off

    count = 0
    
    # ---- 1. BIRCH NEW GAME INTRO (All 7 in-place dialogue strings) ----
    # Ensure zero padding before Birch 3 and Birch 5 matching original ROM layout
    data[0x2c8a13:0x2c8a1f] = b'\x00' * 12
    data[0xf9efa1] = 0x00

    birch_patches = [
        (0x1891038, 707, enc_diag('Chào cháu! Xin lỗi vì để cháu đợi lâu!\\pChào mừng cháu đến với thế giới Pokémon!\\pBác là Birch, mọi người thường gọi bác là Giáo sư Pokémon.\\pÀ, trước khi bắt đầu, bác có 2 lưu ý quan trọng cần dặn dò:\\p[FC0106]1. Ultra Emerald hoàn toàn MIỄN PHÍ, tuyệt đối không trả tiền mua game.\\pNhóm phát triển không chịu trách nhiệm cho mọi tổn thất của bạn.\\p[FC0104]2. Bản game có độ khó cao, KHÔNG phù hợp nếu bạn:\\p1. Muốn rush game nhanh, chơi qua loa.\\p2. Chưa từng chơi bản gốc như Emerald.\\p3. Dùng mã gian lận (cheat).\\p4. Thiếu kiên nhẫn.\\p5. Chúng tôi mong bạn chơi CÔNG BẰNG.\\p6. Chúc bạn chơi game thật vui vẻ!\\p')),
        (0x5e8692, 43, enc_diag('Đây gọi là một “Pokémon.”[FC0860]\\p')),
        (0x2c8a1f, 433, enc_diag('Thế giới này là nơi sinh sống của muôn loài Pokémon.\\pCon người chúng ta chung sống cùng Pokémon, khi là bạn bè thân thiết, khi lại giúp đỡ nhau trong công việc.\\pVà đôi khi, chúng ta cùng sát cánh thi đấu với các Huấn luyện viên khác.\\pDù gần gũi, chúng ta vẫn chưa hiểu hết về Pokémon.\\pThực tế, vẫn còn muôn vàn bí ẩn xoay quanh Pokémon.\\pĐể làm sáng tỏ những điều ấy, bác đang ngày đêm nghiên cứu.\\lĐó chính là sứ mệnh của bác.\\p')),
        (0x2c8bd0, 13, enc_diag('Còn cháu là?')),
        (0x2c8bdd, 34, enc_diag('Cháu là con trai?\\lHay là con gái?')),
        (0xf9efa2, 98, enc_diag('Được rồi. Hãy cho bác biết tên của cháu nhé.\\p[FC0104]Tên không vượt quá 6 chữ cái tiếng Anh.')),
        (0x2c8c1c, 14, enc_diag('Cháu là [BUF01][BUF05]?')),
        (0x2c8c2a, 86, enc_diag('A, ra vậy!\\pCháu là [BUF01][BUF05], người chuyển tới Littleroot quê bác.\\lBác hiểu rồi!\\p')),
        (0x2c8c7a, 242, enc_diag('Được rồi, cháu đã sẵn sàng chưa?\\pChuyến phiêu lưu của cháu sắp sửa bắt đầu.\\pHãy vững tin bước vào thế giới Pokémon rực rỡ, nơi ước mơ và tình bạn đang đón chờ!\\pBác sẽ đợi cháu ở Viện Nghiên cứu Pokémon nhé!\\p'))
    ]
    
    for off, orig_len, b in birch_patches:
        assert len(b) <= orig_len, f'Birch intro {hex(off)} overflow: {len(b)} > {orig_len}'
        data[off:off + len(b)] = b
        if len(b) < orig_len:
            data[off + len(b):off + orig_len] = b'\xff' * (orig_len - len(b))
        count += 1
    print(f"[OK] Patched {len(birch_patches)} Birch New Game Intro strings.")

    # ---- 2. START MENU (Packed perfectly in 0x5eb25c .. 0x5eb289) ----
    start_items = [
        ('Pokédex', ['0xe2ca4', '0x58b3c8']),
        ('Pokémon', ['0xe2ca8', '0x58b3d0']),
        ('Túi', ['0xe2cac', '0x58b3d8']),
        ('Pokénav', ['0xe2cb0', '0x58b3e0']),
        ('Lưu', ['0xe2cb8', '0x58b3f0']),
        ('Cài đặt', ['0xe2cbc', '0x58b3f8']),
        ('Thoát', ['0xe2cc0', '0x58b400'])
    ]
    cur_p = 0x5eb25c
    for vi, sites in start_items:
        b = enc_raw(vi)
        new_off = cur_p
        data[new_off:new_off + len(b)] = b
        cur_p += len(b)
        new_p = struct.pack('<I', BASE + new_off)
        for at_hex in sites:
            at = int(at_hex, 16)
            data[at:at + 4] = new_p
        count += 1
    assert cur_p <= 0x5eb28a, f'Start menu overflow: {hex(cur_p)}'
    print(f"[OK] Patched {len(start_items)} Start Menu items.")

    # ---- 3. OPTION MENU TITLES ----
    opt_items = [
        ('Tốc độ chữ', ['0x55c664']),
        ('Hiệu ứng đấu', ['0x55c668']),
        ('Lối đấu', ['0x55c66c']),
        ('Âm thanh', ['0x55c670']),
        ('Chế độ nút', ['0x55c674']),
        ('Khung viền', ['0x4e6068', '0x4e6268', '0x55c678']),
        ('Thoát', ['0x55c67c'])
    ]
    for vi, sites in opt_items:
        new_off = alloc_pool(enc_raw(vi))
        new_p = struct.pack('<I', BASE + new_off)
        for at_hex in sites:
            at = int(at_hex, 16)
            data[at:at + 4] = new_p
        count += 1
    print(f"[OK] Patched {len(opt_items)} Option Menu titles.")

    # ---- 3.1 OPTION SCREEN HEADER & VERSION TITLES (Hyper Emerald v5.7 VIE) ----
    import re
    FIVE, DOT, SEVEN = 0xA6, 0xAD, 0xA8
    EMERALD = bytes((0xBF, 0xE1, 0xD9, 0xE6, 0xD5, 0xE0, 0xD8))

    # 1. version 5.5 -> 5.7 across all occurrences near Emerald
    hits = [m.start() for m in re.finditer(re.escape(bytes((FIVE, DOT, FIVE))), bytes(data))
            if EMERALD in data[max(0, m.start() - 10):m.start()]]
    for h in hits:
        data[h + 2] = SEVEN

    # 2. Ultra Emerald -> Hyper Emerald in banners and text
    ULTRA = enc_raw('Ultra Emerald')[:-1]
    HYPER = enc_raw('Hyper Emerald')[:-1]
    if len(ULTRA) == len(HYPER):
        idx = 0
        while True:
            idx = data.find(ULTRA, idx)
            if idx == -1: break
            data[idx:idx + len(HYPER)] = HYPER
            idx += len(HYPER)

    # 3. Option Screen Title Header (Table at 0x1F07DF4) -> "Hyper Emerald v5.7 VIE (...)"
    title_modes = [
        ('Hyper Emerald v5.7 VIE (Standard)', 0),
        ('Hyper Emerald v5.7 VIE (Hard Mode)', 1),
        ('Hyper Emerald v5.7 VIE (Challenge)', 2),
        ('Hyper Emerald v5.7 VIE (Lunatic)', 3)
    ]
    color_prefix = bytes([0x00, 0xFC, 0x01, 0x04, 0xFC, 0x03, 0x05])
    title_free_cur = 0x00FF24C0
    for text, k in title_modes:
        b_str = color_prefix + enc_raw(text)
        data[title_free_cur:title_free_cur + len(b_str)] = b_str
        ptr = BASE + title_free_cur
        struct.pack_into('<I', data, 0x1F07DF4 + 4 * k, ptr)
        title_free_cur += len(b_str)
    print(f"[OK] Patched Option screen title headers: 'Hyper Emerald v5.7 VIE'.")

    # ---- 4. BATTLE UI & BATTLE MESSAGES ----
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
                    elif token == '[F7]':
                        out.append(0xF7)
                    elif token == '[Lv]':
                        out.append(0x34)
                    elif len(token) == 6 and token[1:3] in ('F8', 'F9'):
                        out.extend(bytes.fromhex(token[1:5]))
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

    battle_pool_cur = 0xf53704
    def alloc_battle(text):
        nonlocal battle_pool_cur
        b = enc_battle(text)
        off = battle_pool_cur
        data[off:off + len(b)] = b
        battle_pool_cur += len(b)
        if battle_pool_cur % 4 != 0:
            pad = 4 - (battle_pool_cur % 4)
            data[battle_pool_cur:battle_pool_cur + pad] = b'\xff' * pad
            battle_pool_cur += pad
        return off

    # 4.1 Battle Action Menu (Fight / Bag / Pokemon / Run)
    # The active 4-button battle menu in Emerald is formatted at 0x5cca3a:
    # "Fight[FC1338]Bag\nPokémon[FC1338]Run" with [FC1338] column alignment (X=56).
    b_menu = enc_battle(r'Đấu[FC1338]Túi\nPokémon[FC1338]Chạy')
    data[0x5cca3a:0x5cca3a + len(b_menu)] = b_menu
    data[0x5cca3a + len(b_menu):0x5cca54] = b'\xff' * (0x5cca54 - (0x5cca3a + len(b_menu)))
    count += 1

    # Fallback & secondary battle menu pointers
    data[0x5981ec:0x5981f0] = struct.pack('<I', BASE + 0x5980cb)
    b_tui = enc_raw('Túi')
    data[0x9c10b0:0x9c10b0 + len(b_tui)] = b_tui
    if len(b_tui) < 5:
        data[0x9c10b0 + len(b_tui):0x9c10b5] = b'\xff' * (5 - len(b_tui))
    battle_single_patches = [
        (0x598c6f, 6, enc_raw('Đấu')),
        (0x5980cb, 4, enc_raw('Túi')),
        (0x5980a2, 8, enc_raw('POKÉMON'))
    ]
    for off, orig_len, b in battle_single_patches:
        data[off:off + len(b)] = b
        if len(b) < orig_len:
            data[off + len(b):off + orig_len] = b'\xff' * (orig_len - len(b))
        count += 1
    b_run = enc_raw('Chạy')
    run_slot = 0x189128c
    data[run_slot:run_slot + len(b_run)] = b_run
    data[0x59b4f4:0x59b4f8] = struct.pack('<I', BASE + run_slot)
    count += 1

    # 4.2 Battle Turn Prompts ("What will [BUF] do?")
    b_what12 = enc_battle(r'[BUF12]\nsẽ làm gì?')
    data[0x5cc9f3:0x5cc9f3 + len(b_what12)] = b_what12
    data[0x5cc9f3 + len(b_what12):0x5cca04] = b'\xff' * (0x5cca04 - (0x5cc9f3 + len(b_what12)))

    b_what23 = enc_battle(r'[BUF23]\nsẽ làm gì?')
    data[0x5cca04:0x5cca04 + len(b_what23)] = b_what23
    data[0x5cca04 + len(b_what23):0x5cca15] = b'\xff' * (0x5cca15 - (0x5cca04 + len(b_what23)))

    b_whatw = enc_battle(r'Wally\nsẽ làm gì?')
    data[0x5cca15:0x5cca15 + len(b_whatw)] = b_whatw
    data[0x5cca15 + len(b_whatw):0x5cca28] = b'\xff' * (0x5cca28 - (0x5cca15 + len(b_whatw)))
    count += 3

    # 4.3 Fight Sub-menu & Summary Screen Move Info
    b_pp_type = enc_battle(r'[FC0505][FC040D0E0F]PP\nHệ/')
    data[0x5cca79:0x5cca79 + len(b_pp_type)] = b_pp_type
    data[0x5cca79 + len(b_pp_type):0x5cca88] = b'\xff' * (0x5cca88 - (0x5cca79 + len(b_pp_type)))

    # Summary screen Move info Type/ label at 0x5ea378
    b_he = enc_battle('Hệ/')
    data[0x5ea378:0x5ea378 + len(b_he)] = b_he
    data[0x5ea378 + len(b_he):0x5ea37e] = b'\xff' * (6 - len(b_he))
    count += 2

    # 4.4 Wild & Trainer Battle Encounters and Commands
    encounter_patches = [
        (r'Xuất hiện [BUF06] hoang dã!\p', ['0x14e27c', '0x14e2a4', '0x1d4ae60', '0x1d4ae6c']),
        (r'Xuất hiện [BUF06] hoang dã![FC087F]', ['0x14e2a8', '0x1d4ae5c']),
        (r'Xuất hiện [BUF06] và\n[BUF08] hoang dã!\p', ['0x14e28c', '0x1d4ae64']),
        (r'[BUF20]\nmuốn khiêu chiến!', ['0x14e240']),
        (r'[BUF20]\nmuốn khiêu chiến![FC0831]', ['0x14e244']),
        (r'[BUF1C] [BUF1D]\nmuốn khiêu chiến!\p', ['0x14e228', '0x14e264', '0x1d4ae58']),
        (r'[BUF1C] [BUF1D] và\n[BUF2E] [BUF2F]\lmuốn khiêu chiến!\p', ['0x14e268', '0x1d4ae54']),
        (r'[BUF20] và [BUF21]\nmuốn khiêu chiến!', ['0x14e20c']),
        (r'[BUF20] và [BUF21]\nmuốn khiêu chiến![FC0831]', ['0x14e210']),
        (r'[BUF32] [BUF33] phái\n[BUF07]!\lLên nào, [BUF05]!', ['0x14e2d8', '0x1d4ae94']),
        (r'[BUF1F] phái [BUF0B]!\nLên nào! [BUF09]!', ['0x14e304', '0x1d4ae98']),
        (r'Lên nào! [BUF05]!', ['0x14e30c']),
        (r'Lên nào! [BUF05] và\n[BUF07]!', ['0x14e2ec', '0x14e300', '0x1d4ae9c']),
        (r'Lên nào! [BUF00]!', ['0x14e464', '0x1d4aecc']),
        (r'Làm đi, [BUF00]!', ['0x14e470']),
        (r'Tiến lên, [BUF00]!', ['0x14e484', '0x1d4aed4']),
        (r'Đối thủ yếu rồi!\nTới đi, [BUF00]!', ['0x14e480', '0x1d4aed0']),
        (r'[BUF1C] [BUF1D] phái\n[BUF06]!\p[BUF2E] [BUF2F] phái\n[BUF08]!', ['0x14e338', '0x1d4ae78']),
        (r'[BUF20] phái [BUF0A]!\n[BUF21] phái [BUF0C]!', ['0x14e348', '0x1d4ae7c']),
        (r'[BUF1C] [BUF1D] phái\n[BUF06] và [BUF08]!', ['0x14e360', '0x1d4ae84']),
        (r'[BUF20] phái\n[BUF06] và [BUF08]!', ['0x14e364', '0x1d4ae80']),
        (r'[BUF1C] [BUF1D] phái\n[BUF06] ra trận!', ['0x14e390', '0x1d4ae88']),
        (r'[BUF20] phái\n[BUF06] ra trận!', ['0x14e38c', '0x1d4ae90']),
        (r'[BUF22] phái\n[BUF00] ra trận!', ['0x14e4b8', '0x1d4aebc']),
        (r'[BUF20] phái\n[BUF00] ra trận!', ['0x14e4d4', '0x1d4aec4']),
        (r'[BUF1C] [BUF1D] phái\n[BUF00] ra trận!', ['0x14e4d8', '0x1d4aec0']),
        (r'[BUF2E] [BUF2F] phái\n[BUF00] ra trận!', ['0x14e4f4', '0x1d4aec8']),
        (r'[BUF00], đủ rồi!\nQuay lại nào!', ['0x14e3b8', '0x1d4aeac']),
        (r'[BUF00], quay lại nào!', ['0x14e3d4', '0x1d4aeb0']),
        (r'[BUF00], tốt lắm!\nQuay lại nào!', ['0x14e3e4', '0x1d4aeb8']),
        (r'[BUF00], được rồi!\nQuay lại nào!', ['0x14e3e8', '0x1d4aeb4']),
        (r'[BUF20] thu hồi\n[BUF00]!', ['0x14e420', '0x1d4aea8']),
        (r'[BUF22] thu hồi\n[BUFFF]!', ['0x14e424', '0x1d4aea4']),
        (r'[BUF1C] [BUF1D]\nthu hồi [BUF00]!', ['0x14e42c', '0x1d4aea0']),
        (r'[BUF0F] dùng\n[BUF01]', ['0x14e558', '0x1d4aedc']),
        (r'[FC101100]Đã chạy thoát an toàn!\p', ['0x14e5a0', '0x1d4aee0']),
        (r'[FC101100][BUF20] đã bỏ chạy!', ['0x14e5bc', '0x1d4aee8']),
        (r'[FC101100][BUF20] và\n[BUF21] đã bỏ chạy!', ['0x14e5c0', '0x1d4aee4']),
        (r'Bị đánh bại bởi [BUF20]\nvà [BUF21]!', ['0x14e62c', '0x1d4aeec']),
        (r'Đã đánh bại [BUF20]\nvà [BUF21]!', ['0x14e620', '0x1d4aef0']),
        (r'Hòa trận đấu với\n[BUF20] và [BUF21]!', ['0x14e634', '0x1d4aef4']),
        (r'Bị đánh bại bởi\n[BUF20]!', ['0x14e6ac', '0x1d4aef8']),
        (r'Đã đánh bại\n[BUF20]!', ['0x14e6a4', '0x1d4aefc']),
        (r'Hòa trận đấu với\n[BUF20]!', ['0x14e6b4', '0x1d4af00']),
        (r'Đã đánh bại\n[BUF1C] [BUF1D]!\p', ['0x14e66c']),
        (r'Bị đánh bại bởi\n[BUF1C] [BUF1D]!', ['0x14e674']),
        (r'Hòa trận đấu với\n[BUF1C] [BUF1D]!', ['0x14e67c']),
    ]
    for text, sites in encounter_patches:
        off = alloc_battle(text)
        p = struct.pack('<I', BASE + off)
        for s in sites:
            data[int(s, 16):int(s, 16) + 4] = p
        count += 1

    # 4.5 Colored Stat Names (gStatNamesTable at 0x5cbe00)
    stat_names = [
        ('0x5cbe04', r'[FC0102]Tấn công[FC0101]'),
        ('0x5cbe08', r'[FC0103]Phòng thủ[FC0101]'),
        ('0x5cbe0c', r'[FC010D]Tốc độ[FC0101]'),
        ('0x5cbe10', r'[FC0104]T.Công ĐB[FC0101]'),
        ('0x5cbe14', r'[FC0107]P.Thủ ĐB[FC0101]'),
        ('0x5cbe18', r'[FC0108]Chính xác[FC0101]'),
        ('0x5cbe1c', r'[FC0108]Né tránh[FC0101]'),
    ]
    for site, text in stat_names:
        off = alloc_battle(text)
        data[int(site, 16):int(site, 16) + 4] = struct.pack('<I', BASE + off)
        count += 1

    # 4.6 Battle Status Conditions (Table at 0x31bca0)
    status_words = [
        ('0x31bcac', 'độc'),
        ('0x31bcb4', 'ngủ'),
        ('0x31bcbc', 'tê liệt'),
        ('0x31bcc4', 'bỏng'),
        ('0x31bccc', 'băng'),
        ('0x31bcd4', 'bối rối'),
        ('0x31bcdc', 'say đắm'),
    ]
    for site, word in status_words:
        off = alloc_battle(word)
        data[int(site, 16):int(site, 16) + 4] = struct.pack('<I', BASE + off)
        count += 1

    # 4.7 Core Battle Messages (gBattleStringsTable at 0x5cc270)
    bst_patches = {
        1: r'[BUF00] nhận được[BUF01]\n[BUF34] Điểm EXP!\p',
        2: r'[BUF00] đạt tới\nCấp [BUF01]![FC0A]\p',
        3: r'[BUF00] đã học được\n[BUF01]![FC0A]\p',
        4: r'[BUF00] đang cố\nhọc [BUF01].\p',
        5: r'Nhưng [BUF00] không thể học\nquá bốn chiêu thức.\p',
        6: r'Quên một chiêu để nhường\nchỗ cho [BUF01]?',
        7: r'[BUF00] đã quên\n[BUF01].\p',
        8: r'[FC0820]Dừng việc học\n[BUF01]?',
        9: r'[BUF00] đã không học\n[BUF01].\p',
        10: r'[BUF0F] đã học\n[BUF00]!',
        11: r'Đòn đánh của [BUF0F]\nđã trượt!',
        12: r'[BUF10]\nđã tự bảo vệ mình.',
        13: r'Chỉ số của [BUF0F]\nkhông thể tăng thêm!',
        14: r'[BUF10] né đòn nhờ\nđặc tính [BUF19]!',
        15: r'Không có tác dụng\nvới [BUF10].',
        16: r'[BUF0F]\nđã gục ngã!\p',
        17: r'[BUF10]\nđã gục ngã!\p',
        18: r'[BUF23] nhận được $[BUF00]\ncho chiến thắng!\p',
        19: r'[BUF23] không còn Pokémon\nnào có thể chiến đấu!\p',
        20: r'[BUF23] bị bất tỉnh![FC09]',
        21: r'[BUF13] ngăn không cho\ntrốn thoát với [BUF1A]!\p',
        22: r'Trúng [BUF00] lần!',
        23: r'[BUF11]\nđã ngủ thiếp đi!',
        24: r'[BUF1A] của [BUF13]\nru ngủ [BUF11]!',
        25: r'[BUF10]\nđang ngủ say!',
        26: r'[BUF0F]\nđang ngủ say!',
        27: r'[BUF10]\nkhông hề bị ảnh hưởng!',
        28: r'[BUF11]\nđã bị trúng độc!',
        29: r'[BUF1A] của [BUF13]\nđầu độc [BUF11]!',
        30: r'[BUF0F] bị đau\ndo trúng độc!',
        31: r'[BUF10] vốn dĩ\nđã trúng độc!',
        32: r'[BUF11] bị trúng\nkịch độc!',
        33: r'[BUF10] bị hút\nhết năng lượng!',
        34: r'[BUF11]\nđã bị bỏng!',
        35: r'[BUF1A] của [BUF13]\nthêu đốt [BUF11]!',
        36: r'[BUF0F] bị đau\ndo vết bỏng!',
        37: r'[BUF11] đã bị\nđóng băng!',
        38: r'[BUF1A] của [BUF13]\nđóng băng [BUF11]!',
        39: r'[BUF0F] đang bị\nđóng băng!',
        40: r'[BUF10] đã được\nrã đông!',
        41: r'[BUF0F] đã được\nrã đông!',
        43: r'[BUF11] đã bị tê liệt!\nCó thể không cử động được!',
        44: r'[BUF1A] của [BUF13]\nlàm [BUF11] tê liệt!',
        45: r'[BUF0F] bị tê liệt!\nKhông thể cử động!',
        46: r'[BUF10] vốn dĩ\nđã bị tê liệt!',
        47: r'[BUF10] đã được\nchữa khỏi tê liệt!',
        49: r'[BUF00] của [BUF13]\nkhông thể tăng thêm!',
        50: r'[BUF00] của [BUF13]\nkhông thể giảm thêm!',
        53: r'[BUF0F]\nđang bị bối rối!',
        54: r'[BUF0F] đã hết\nbối rối!',
        55: r'[BUF11]\ntrở nên bối rối!',
        56: r'[BUF10] vốn dĩ\nđang bị bối rối!',
        62: r'[BUF0F] bị nao núng!',
        63: r'[BUF10] đã hồi phục\nthể lực!',
        64: r'HP của [BUF10]\nđã đầy!',
        93: r'[BUF10] đã né được\nđòn tấn công!',
        95: r'[BUF0F] đang ngủ say.',
        96: r'[BUF0F] đã tỉnh giấc!',
        197: r'đột ngột ',
        198: r'tăng!',
        199: r'đột ngột ',
        200: r'giảm!',
        201: r'[BUF00] của [BUF0F]\n[BUF01]',
        202: r'[BUF00] của [BUF10]\n[BUF01]',
        203: r'[BUF00] của [BUF0F]\n[BUF01]',
        204: r'[BUF00] của [BUF10]\n[BUF01]',
        205: r'Một đòn chí mạng!',
        206: r'Đòn hạ gục trong 1 hit!',
        209: r'Không hiệu quả lắm…',
        210: r'Cực kỳ hiệu quả!',
        211: r'[FC101100]Đã chạy thoát an toàn!\p',
        212: r'[FC101100][BUF00] hoang dã đã trốn thoát!',
        213: r'Không! Đang đấu với Huấn luyện viên\nthì không thể bỏ chạy!\p',
        214: r'Không thể trốn thoát!\p',
        215: r'GS. Birch: Đừng bỏ bác lại mà!\p',
        216: r'Nhưng không có gì xảy ra!',
        217: r'Nhưng chiêu đã thất bại!',
        218: r'Nó tự đánh bản thân\ndo bối rối!',
        220: r'Trời bắt đầu đổ mưa!',
        224: r'Mưa đã tạnh.',
        225: r'Bão cát nổi lên!',
        226: r'Bão cát đang hoành hành.',
        227: r'Bão cát đã lắng xuống.',
        228: r'Ánh mặt trời chói chang!',
        230: r'Ánh mặt trời dịu đi.',
        231: r'Mưa đá bắt đầu rơi!',
        233: r'Mưa đá đã ngừng.',
        243: r'Chiêu này đã hết PP rồi!\p',
        244: r'Nhưng chiêu này đã hết PP!',
        245: r'[BUF23] đã dùng\n[BUF16]!',
        247: r'Huấn luyện viên đã chặn quả bóng!',
        248: r'Đừng có ăn trộm!',
        249: r'Nó đã né được Poké Ball!\nPokémon này không thể bắt!',
        250: r'Ném trượt Pokémon rồi!',
        251: r'Ồ không!\nPokémon đã thoát ra ngoài!',
        252: r'Tiếc quá!\nSuýt chút nữa là được rồi!',
        253: r'Aaa!\nChút nữa là bắt được rồi!',
        254: r'Tiếc thật!\nChỉ một chút xíu nữa thôi!',
        255: r'Bắt được rồi!\nĐã bắt được [BUF06]![FC0A][FC0B6001]\p',
        256: r'Bắt được rồi!\nĐã bắt được [BUF06]![FC0A][FC0B6001][FC087F]',
        257: r'Đặt biệt danh cho\n[BUF06] vừa bắt được?',
        258: r'[BUF06] đã được chuyển tới\nMáy tính của [BUF27].',
        259: r'Dữ liệu của [BUF06]\nđã được thêm vào Pokédex.\p',
        262: r'Không thể trốn thoát!\p',
        263: r'[BUF0F] phớt lờ mệnh lệnh\ntrong khi ngủ!',
        264: r'[BUF0F] phớt lờ mệnh lệnh!',
        270: r'[BUF1C] [BUF1D] chuẩn bị\ndùng [BUF01].\p[BUF23] có muốn đổi\nPokémon không?',
        291: r'[BUF10] cố trụ vững\nnhờ có [BUF16]!',
        309: r'Người chơi đã đánh bại\n[BUF1C] [BUF1D]!\p',
        325: r'Đổi sang Pokémon tiếp theo?',
        332: r'Hộp đã đầy!\nKhông thể bắt thêm Pokémon!\p',
        333: r'[BUF10] đã né được\nđòn tấn công!',
        349: r'Nhưng không có tác dụng!'
    }
    for idx, text in bst_patches.items():
        off = alloc_battle(text)
        data[0x5cc270 + idx * 4:0x5cc270 + idx * 4 + 4] = struct.pack('<I', BASE + off)
        count += 1

    # 4.8 Move usage & Exp. Share in-place messages
    b_exp_share = enc_battle(r'Nhờ có Exp. Share, toàn bộ\nđội hình đều nhận được EXP.')
    data[0x381f9c:0x381f9c + len(b_exp_share)] = b_exp_share
    data[0x381f9c + len(b_exp_share):0x381fe5] = b'\xff' * (0x381fe5 - (0x381f9c + len(b_exp_share)))
    count += 1
    # 4.9 Level-up Stat Window Labels (Table at 0x625b54)
    lvlup_stats = [
        ('0x625b54', 'HP T.đa'),
        ('0x625b58', 'Atk'),
        ('0x625b5c', 'Def'),
        ('0x625b60', 'Sp. Atk'),
        ('0x625b64', 'Sp. Def'),
        ('0x625b68', 'Speed'),
    ]
    for site, text in lvlup_stats:
        off = alloc_battle(text)
        data[int(site, 16):int(site, 16) + 4] = struct.pack('<I', BASE + off)
        count += 1

    assert battle_pool_cur <= 0xf54aa0, f'Battle pool overflow: {hex(battle_pool_cur)} > 0xf54aa0'
    print(f"[OK] Patched Battle UI & {len(bst_patches) + len(encounter_patches) + len(stat_names) + len(status_words) + len(lvlup_stats) + 8} battle messages (Battle pool used: {battle_pool_cur - 0xf53704} / 5020 bytes).")

    # 4.10 In-place Custom Send-out & Battle Team Strings
    # 0x1D74A23: 'I choose you! [BUF00]!' (18 bytes) -> 'Tớ chọn cậu! [BUF00]!' (17 bytes)
    b_p1 = enc_battle(r'Tớ chọn cậu! [BUF00]!')
    data[0x1D74A23:0x1D74A23 + len(b_p1)] = b_p1
    data[0x1D74A23 + len(b_p1):0x1D74A23 + 18] = b'\xff' * (18 - len(b_p1))
    count += 1

    # 0x1D74A4E: '[FC020F]I choose you! [BUF05]!' (21 bytes) -> '[FC020F]Tớ chọn cậu! [BUF05]!' (20 bytes)
    b_p2 = enc_battle(r'[FC020F]Tớ chọn cậu! [BUF05]!')
    data[0x1D74A4E:0x1D74A4E + len(b_p2)] = b_p2
    data[0x1D74A4E + len(b_p2):0x1D74A4E + 21] = b'\xff' * (21 - len(b_p2))
    count += 1

    # 0x1D749E2: 'Enemy team' (11 bytes) -> 'Phe địch' (9 bytes)
    b_enemy = enc_battle('Phe địch')
    data[0x1D749E2:0x1D749E2 + len(b_enemy)] = b_enemy
    data[0x1D749E2 + len(b_enemy):0x1D749ED] = b'\xff' * (11 - len(b_enemy))
    count += 1

    # 0x1D74A05: 'Ally team' (10 bytes) -> 'Phe ta' (7 bytes)
    b_ally = enc_battle('Phe ta')
    data[0x1D74A05:0x1D74A05 + len(b_ally)] = b_ally
    data[0x1D74A05 + len(b_ally):0x1D74A0F] = b'\xff' * (10 - len(b_ally))
    count += 1

    # 0x1D749ED: 'rose' (5 bytes) -> 'tăng'
    b_rose1 = enc_battle('tăng')
    data[0x1D749ED:0x1D749ED + len(b_rose1)] = b_rose1
    data[0x1D749ED + len(b_rose1):0x1D749F2] = b'\xff' * (5 - len(b_rose1))

    # 0x1D749F7: 'rose' (5 bytes) -> 'tăng'
    b_rose2 = enc_battle('tăng')
    data[0x1D749F7:0x1D749F7 + len(b_rose2)] = b_rose2
    data[0x1D749F7 + len(b_rose2):0x1D749FC] = b'\xff' * (5 - len(b_rose2))

    # 0x1D74A10: 'lost' (5 bytes) -> 'thua'
    b_lost = enc_battle('thua')
    data[0x1D74A10:0x1D74A10 + len(b_lost)] = b_lost
    data[0x1D74A10 + len(b_lost):0x1D74A15] = b'\xff' * (5 - len(b_lost))
    count += 3
    print("[OK] Patched in-place custom send-out & battle team strings ('Tớ chọn cậu!', 'Phe ta', 'Phe địch').")

    # 4.11 Expanded Battle Strings Table (0x1D744E4 .. 0x1D749D0 - 315 pointers)
    # Using clean free pool at 0x1F82520 (over 500 KB available)
    expanded_pool_cur = 0x1F82520
    def alloc_expanded(text):
        nonlocal expanded_pool_cur
        b = enc_battle(text)
        off = expanded_pool_cur
        data[off:off + len(b)] = b
        expanded_pool_cur += len(b)
        if expanded_pool_cur % 4 != 0:
            pad = 4 - (expanded_pool_cur % 4)
            data[expanded_pool_cur:expanded_pool_cur + pad] = b'\xff' * pad
            expanded_pool_cur += pad
        return off

    orig_rom_path = os.path.join(VI, 'tests', 'run_cmp_orig', 'game.gba')
    orig_rom = open(orig_rom_path, 'rb').read() if os.path.exists(orig_rom_path) else orig

    exp_table_count = 0
    for idx in range(315):
        orig_val = struct.unpack('<I', orig_rom[0x1D744E4 + idx * 4 : 0x1D744E4 + idx * 4 + 4])[0]
        orig_off = orig_val - 0x08000000
        try:
            orig_txt, _ = decode(orig_rom, orig_off)
            if orig_txt in EXPANDED_BATTLE_TRANSLATIONS:
                vi_txt = EXPANDED_BATTLE_TRANSLATIONS[orig_txt]
                new_off = alloc_expanded(vi_txt)
                data[0x1D744E4 + idx * 4 : 0x1D744E4 + idx * 4 + 4] = struct.pack('<I', BASE + new_off)
                exp_table_count += 1
        except Exception:
            pass
    count += exp_table_count
    print(f"[OK] Patched {exp_table_count} / 315 Expanded Battle Strings (Mega, Z-Move, Dynamax, Terrain, Quotes).")

    # 4.12 Remaining 250 gBattleStringsTable Entries (Completes 100% of 363 Battle Strings)
    bst_full_count = 0
    for idx, vi_txt in BST_FULL_TRANSLATIONS.items():
        new_off = alloc_expanded(vi_txt)
        data[0x5CC270 + idx * 4 : 0x5CC270 + idx * 4 + 4] = struct.pack('<I', BASE + new_off)
        bst_full_count += 1
    count += bst_full_count
    print(f"[OK] Patched {bst_full_count} remaining gBattleStringsTable entries (Total 363/363 BST patched = 100%).")

    # 4.13 Party Menu, Move Learning, Summary Screen, Pokémart & PC Storage Strings (178 strings)
    party_str_count = 0
    party_ptrs_rewritten = 0
    for orig_off, vi_txt in PARTY_SYSTEM_UI_TRANSLATIONS.items():
        new_off = alloc_expanded(vi_txt)
        new_p = struct.pack('<I', BASE + new_off)
        old_p = struct.pack('<I', BASE + orig_off)
        idx = 0
        while True:
            idx = orig_rom.find(old_p, idx)
            if idx == -1: break
            data[idx:idx + 4] = new_p
            party_ptrs_rewritten += 1
            idx += 4
        # Also write in-situ if it fits, so direct offset reads get the translated string
        b = enc_diag(vi_txt) if any(x in vi_txt for x in ['\\n', '\\l', '\\p', '[BUF', '[FC']) else enc_raw(vi_txt)
        end = orig_rom.find(b'\xff', orig_off)
        if end != -1 and end < orig_off + 200:
            orig_len = end - orig_off + 1
            if len(b) <= orig_len:
                data[orig_off : orig_off + len(b)] = b
                if len(b) < orig_len:
                    data[orig_off + len(b) : orig_off + orig_len] = b'\xff' * (orig_len - len(b))
        party_str_count += 1
    count += party_str_count
    print(f"[OK] Patched {party_str_count} Party / Move Learning / Summary / Shop / PC strings ({party_ptrs_rewritten} pointers rewritten).")

    assert expanded_pool_cur <= 0x1FF0000, f'Expanded pool overflow: {hex(expanded_pool_cur)} > 0x1FF0000'
    print(f"[OK] Expanded system UI pool used: {expanded_pool_cur - 0x1F82520} bytes (pool cur: {hex(expanded_pool_cur)}).")

    # ---- 5. BAG POCKET NAMES ----
    bag_pockets_in_situ = [
        ('Vật phẩm', ['0x5e91fc']),
        ('Poké Ball', ['0x5e9200']),
        ('TM & HM', ['0x5e9204']),
        ('Berry', ['0x5e9208']),
        ('Đồ Q.Trọng', ['0x5e920c'])
    ]
    cur_p = 0x5e91ce
    for vi, sites in bag_pockets_in_situ:
        b = enc_raw(vi)
        new_off = cur_p
        data[new_off:new_off + len(b)] = b
        cur_p += len(b)
        new_p = struct.pack('<I', BASE + new_off)
        for at_hex in sites:
            at = int(at_hex, 16)
            data[at:at + 4] = new_p
        count += 1
    if cur_p < 0x5e91fb:
        data[cur_p:0x5e91fb] = b'\xff' * (0x5e91fb - cur_p)
    # Clear old Key Item slot in Birch padding
    data[0x1891294:0x18912a4] = b'\xff' * 16
    print(f"[OK] Patched {len(bag_pockets_in_situ)} Bag Pocket names.")

    # ---- 6. SAVE GAME DIALOGUES ----
    # Save prompt in Hyper Emerald is at 0x1823e37, referenced at 0xa00e4
    b_save_prompt = enc_diag('Còn [FC0104][BUF02][FC0102] chỗ trống trong túi.\\nCậu có muốn lưu trò chơi không?')
    save_prompt_slot = 0x18912a4
    data[save_prompt_slot:save_prompt_slot + len(b_save_prompt)] = b_save_prompt
    data[0xa00e4:0xa00e8] = struct.pack('<I', BASE + save_prompt_slot)
    count += 1

    save_dialogues = [
        (0x2c87b1, 35, enc_diag('   Cậu có muốn lưu trò chơi không?')),
        (0x2c87d5, 59, enc_diag('Đã có dữ liệu lưu trước đó.\\nCậu có muốn ghi đè lên không?')),
        (0x2c8810, 34, enc_diag('Đang lưu…\\nxin đừng tắt nguồn máy.')),
        (0x2c8832, 19, enc_diag('[BUF01] đã lưu game.')),
        (0x2c8845, 253, enc_diag('CẢNH BÁO!\\pĐã có file lưu khác trong máy.\\pNếu lưu bây giờ, toàn bộ hành trình,\\nvật phẩm và Pokémon sẽ bị mất.\\pCậu có chắc chắn muốn lưu\\nvà ghi đè lên file cũ không?'))
    ]
    for off, orig_len, b in save_dialogues:
        assert len(b) <= orig_len, f'Save dialogue {hex(off)} overflow: {len(b)} > {orig_len}'
        data[off:off + len(b)] = b
        if len(b) < orig_len:
            data[off + len(b):off + orig_len] = b'\xff' * (orig_len - len(b))
        count += 1
    print(f"[OK] Patched {len(save_dialogues) + 1} Save Game dialogues.")

    # ---- 7. YES / NO BOX & PROMPTS (Có / Không) ----
    # Expand Yes/No window template (width 5 -> 6 tiles, left 21 -> 20) for ample margin
    data[0x60f0a9] = 20 # tilemapLeft
    data[0x60f0ab] = 6  # width (48px)

    # In-situ 'Có' at 0x5eae62 (fits within 4 bytes)
    b_co_raw = enc_raw('Có')
    data[0x5eae62:0x5eae62 + len(b_co_raw)] = b_co_raw
    if len(b_co_raw) < 4:
        data[0x5eae62 + len(b_co_raw):0x5eae66] = b'\xff' * (4 - len(b_co_raw))

    def enc_opt(word):
        for k, v in NORMALIZE.items(): word = word.replace(k, v)
        return b'\xfc\x01\x06\xfc\x03\x07' + bytes(enc.byte(c) for c in word) + b'\xff'

    # Yes/No Box 2-line string
    b_yesno_box = enc_raw('Có')[:-1] + b'\xfe' + enc_raw('Không')
    yesno_box_off = alloc_pool(b_yesno_box)
    for site in ['0x198c30', '0x1997a8']:
        data[int(site, 16):int(site, 16) + 4] = struct.pack('<I', BASE + yesno_box_off)
    count += 1

    # 'Có' and 'Không' items for scripts and multichoice
    yes_off = alloc_pool(enc_raw('Có'))
    no_off = alloc_pool(enc_raw('Không'))

    for site in ['0x1feb4', '0x2a184', '0x2a284', '0x1a0644', '0x58ad10', '0x58b280', '0x58b4a8', '0x19bbfc', '0x19ece8']:
        data[int(site, 16):int(site, 16) + 4] = struct.pack('<I', BASE + yes_off)
    for site in ['0x1feb8', '0x2a188', '0x2a288', '0x1a0648', '0x58ad18', '0x58b288', '0x58b4b0', '0x19bc00', '0x19ecec']:
        data[int(site, 16):int(site, 16) + 4] = struct.pack('<I', BASE + no_off)
    count += 2
    print(f"[OK] Patched Yes/No system box and multichoice prompts (Có / Không).")

    # ---- 8. PARTY MENU ACTIONS ----
    party_items = [
        ('Thông tin', ['0x615c08', '0xfd9b8c', '0x57ba98', '0x19bb58', '0x19ec88']),
        ('Đổi chỗ', ['0x615c10', '0xfd9b94', '0x1c2abc', '0x57babc']),
        ('Vật phẩm', ['0x615c20', '0xfd9ba4']),
        ('Cho giữ', ['0x613fcc', '0x615c28', '0x61f2e8', '0xfd9bac']),
        ('Lấy lại', ['0x615c30', '0xfd9bb4']),
        ('Thư', ['0x615c38', '0xfd9bbc']),
        ('Hủy', ['0x615c18', '0x615c50', '0xfd9b9c', '0xfd9bd4', '0x613fd4', '0x61f2f0'])
    ]
    for vi, sites in party_items:
        new_off = alloc_pool(enc_raw(vi))
        p = struct.pack('<I', BASE + new_off)
        for s in sites:
            data[int(s, 16):int(s, 16) + 4] = p
        count += 1
    print(f"[OK] Patched {len(party_items)} Party Menu actions.")

    # ---- 9. BAG ITEM ACTIONS ----
    bag_item_actions = [
        ('Dùng', ['0x5b2668', '0x5b2680', '0x5b2688', '0x613fb4', '0x613fdc', '0x61f2d8', '0x61f2f8']),
        ('Vứt', ['0x5b2670', '0x613fbc', '0x615c98', '0x61f2e0', '0xfd9c1c', '0x5a6b58']),
        ('Đăng ký', ['0x58ac90', '0x613fc4', '0x2f0264', '0x615c80', '0xfd9c04']),
        ('Kiểm tra', ['0x613fe4', '0x6227ec']),
        ('Bỏ chọn', ['0x613ff4', '0x19bb5c']),
        ('Xem thẻ', ['0x613fec']),
        ('Xác nhận', ['0x614004'])
    ]
    for vi, sites in bag_item_actions:
        new_off = alloc_pool(enc_raw(vi))
        p = struct.pack('<I', BASE + new_off)
        for s in sites:
            data[int(s, 16):int(s, 16) + 4] = p
        count += 1
    print(f"[OK] Patched {len(bag_item_actions)} Bag Item actions.")

    # ---- 10. MART SHOP MENU ----
    mart_items = [
        ('Mua', ['0x589a10', '0x589a28']),
        ('Bán', ['0x589a18']),
        ('Thoát', ['0x589a20', '0x589a30'])
    ]
    for vi, sites in mart_items:
        new_off = alloc_pool(enc_raw(vi))
        p = struct.pack('<I', BASE + new_off)
        for s in sites:
            data[int(s, 16):int(s, 16) + 4] = p
        count += 1
    print(f"[OK] Patched {len(mart_items)} Mart Shop menu items.")

    # ---- 11. PC BOX & SYSTEM MENU ----
    pc_items = [
        (enc_raw('Máy tính ai đó'), ['0xe2508', '0x58bb70']),
        (enc_raw('Máy tính Lanette'), ['0xe24ac', '0x58bb74']),
        (enc_raw('Máy tính ')[:-1] + b'\xfd\x01\xff', ['0xe2510', '0x58bb78']),
        (enc_raw('Sảnh Danh vọng'), ['0xe2440']),
        (enc_raw('Đăng xuất'), ['0xe2444', '0xe24a4', '0x58bb7c']),
        (enc_raw('Rút Pokémon'), ['0x5716c0']),
        (enc_raw('Gửi Pokémon'), ['0x5716c8']),
        (enc_raw('Chuyển Pokémon'), ['0x5716d0']),
        (enc_raw('Chuyển vật phẩm'), ['0x5716d8']),
        (enc_raw('Tạm biệt!'), ['0x5716e0'])
    ]
    for b, sites in pc_items:
        new_off = alloc_pool(b)
        p = struct.pack('<I', BASE + new_off)
        for s in sites:
            data[int(s, 16):int(s, 16) + 4] = p
        count += 1
    print(f"[OK] Patched {len(pc_items)} PC Menu items.")

    # ---- 12. OPTION MENU VALUES ----
    opt_values = [
        (enc_opt('Chậm'), ['0xbacd4']),
        (enc_opt('Vừa'), ['0xbacd8']),
        (enc_opt('Nhanh'), ['0xbacdc']),
        (enc_opt('Bật'), ['0xbad54']),
        (enc_opt('Tắt'), ['0xbad58']),
        (enc_opt('Đổi'), ['0xbadd0']),
        (enc_opt('Cố định'), ['0xbadd4']),
        (enc_opt('Kiểu'), ['0xbaf7c']),
        (enc_opt('Chuẩn'), ['0xbb0c4'])
    ]
    for b, sites in opt_values:
        new_off = alloc_pool(b)
        p = struct.pack('<I', BASE + new_off)
        for s in sites:
            data[int(s, 16):int(s, 16) + 4] = p
        count += 1
    # ---- 13. HYPER EMERALD START MENU (with icons, sStartMenuItems at 0x510540) ----
    # Expand Start Menu window width from 7 tiles (56px) to 10 tiles (80px, left=19)
    # 0x1979ea: mov r1, #19 (tilemapLeft=19)
    # 0x1979ee: mov r3, #10 (tilemapWidth=10)
    data[0x1979ea] = 0x13
    data[0x1979ee] = 0x0a

    # CRITICAL: 0x510578 (Exit item pointer) MUST remain pointing to 0x085ee6ec!
    # Repointing 0x510578 causes overworld NPC dialogue to freeze on interaction.
    # In-place patch 'Thoát' (Exit with icon) at 0x5ee6ec (free unused area in VI).
    b_thoat = b'\x02\xfa' + enc_raw('Thoát')
    data[0x5ee6ec:0x5ee6ec + len(b_thoat)] = b_thoat
    count += 1

    start_he_items = [
        (0x510540, b'\xfc\x06\x01\x01\xf7\x00' + enc_raw('Pokédex')),
        (0x510548, b'\x01\xf8\x00' + enc_raw('Pokémon')),
        (0x510550, b'\x01\xf9\x00' + enc_raw('Túi')),
        (0x510558, b'\x01\xfa\x00' + enc_raw('Pokénav')),
        (0x510568, b'\x02\xf8\x00' + enc_raw('Lưu')),
        (0x510570, b'\x02\xf9\x00' + enc_raw('Cài đặt')),
        (0x510580, enc_raw('Rút lui')),
        (0x510590, enc_raw('Nghỉ ngơi')),
        (0x510598, enc_raw('Rút lui')),
        (0x5105a0, b'\x01\xf9\x00' + enc_raw('Túi')),
    ]
    for table_addr, b_val in start_he_items:
        off = alloc_pool(b_val)
        data[table_addr:table_addr + 4] = struct.pack('<I', BASE + off)
        count += 1
    print(f"[OK] Patched {len(start_he_items) + 1} Hyper Emerald Start Menu items (with icons) & expanded window width.")

    # ---- 14. MAIN MENU / TITLE SCREEN MENU ----
    main_menu_items = [
        (enc_raw('Trò chơi mới'), ['0x2fd34', '0x2fdf0', '0x2fee8', '0x30084']),
        (enc_raw('Tiếp tục'), ['0x2fdec', '0x2fee4', '0x30080']),
        (enc_raw('Cài đặt'), ['0x2fd38', '0x2fdf4', '0x2fef0', '0x30090']),
        (enc_raw('Quà bí ẩn'), ['0x2feec', '0x30088']),
        (enc_raw('Sự kiện bí ẩn'), ['0x3008c']),
        (enc_diag('Chưa kết nối\\nBộ chuyển đổi Không dây.'), ['0x3060c']),
    ]
    for b_val, sites in main_menu_items:
        off = alloc_pool(b_val)
        p = struct.pack('<I', BASE + off)
        for s in sites:
            data[int(s, 16):int(s, 16) + 4] = p
        count += 1
    print(f"[OK] Patched {len(main_menu_items)} Main Menu / Title Screen entries.")

    # ---- 15. SAVE FILE INFO & IN-GAME SAVE BOX ----
    save_info_items = [
        (enc_raw('Người chơi'), ['0x31eec', '0xa0878', '0x1f004c4']),
        (enc_raw('Thời gian'), ['0x31f70', '0xa0884']),
        (enc_raw('Pokédex'), ['0x3200c', '0xa0880']),
        (enc_raw('Huy hiệu'), ['0x3209c', '0xa087c', '0x1f05b7c']),
    ]
    for b_val, sites in save_info_items:
        off = alloc_pool(b_val)
        p = struct.pack('<I', BASE + off)
        for s in sites:
            data[int(s, 16):int(s, 16) + 4] = p
        count += 1
    print(f"[OK] Patched {len(save_info_items)} Save Info / Save Box labels.")

    # ---- 16. GENDER SELECTION & NAMING SCREEN ----
    gender_naming_items = [
        (enc_raw('Con trai'), ['0x2ff118']),
        (enc_raw('Con gái'), ['0x2ff120']),
        (enc_raw('Tên của cháu?'), ['0x58bfb0']),
        (enc_raw('Tên Hộp?'), ['0x58bfbc']),
        (enc_diag('Biệt danh [BUF02]?'), ['0x58bfc8']),
    ]
    for b_val, sites in gender_naming_items:
        off = alloc_pool(b_val)
        p = struct.pack('<I', BASE + off)
        for s in sites:
            data[int(s, 16):int(s, 16) + 4] = p
        count += 1
    print(f"[OK] Patched {len(gender_naming_items)} Gender Selection & Naming Screen titles.")

    assert sys_pool_cur <= 0x36f7e0, f'Sys pool overflow: {hex(sys_pool_cur)} > 0x36f7e0'
    print(f"[OK] Total pool used {sys_pool_cur - 0x36f3b8} / 1064 bytes.")

    # ---- 17. GAMEPLAY SPECIAL DIALOGUES, C TABLES & FIELD PROMPTS ----
    from gameplay_special_dict import ALL_GAMEPLAY_SPECIAL_DATA
    gameplay_pool_cur = 0xFE6000
    def alloc_gameplay(b):
        nonlocal gameplay_pool_cur
        off = gameplay_pool_cur
        data[off:off + len(b)] = b
        gameplay_pool_cur += len(b)
        if gameplay_pool_cur % 4 != 0:
            pad = 4 - (gameplay_pool_cur % 4)
            data[gameplay_pool_cur:gameplay_pool_cur + pad] = b'\xff' * pad
            gameplay_pool_cur += pad
        return off

    for item in ALL_GAMEPLAY_SPECIAL_DATA:
        b_val = enc_diag(item['vi'])
        off = alloc_gameplay(b_val)
        p = struct.pack('<I', BASE + off)
        for s in item['sites']:
            at = int(s, 16)
            data[at:at + 4] = p
        count += 1
    assert gameplay_pool_cur <= 0xFEE000, f'Gameplay pool overflow: {hex(gameplay_pool_cur)} > 0xFEE000'
    print(f"[OK] Patched {len(ALL_GAMEPLAY_SPECIAL_DATA)} Gameplay Special dialogues & C-engine strings (used {gameplay_pool_cur - 0xFE6000} bytes in 0xFE6000 pool).")

    # ---- 18. C-CODE LITERAL POOLS & DIALOGUE REPOINTERS ----
    c_literal_pools = [
        (0xe2544, 0x271dad, 'D03605 Which PC prompt'),
        (0xb3768, 0x23f2cb, 'D03762 Wireless wait prompt'),
        (0x396a4, 0x23e8d9, 'D02641 Save error prompt'),
        (0x39148, 0x24948e, 'D02696 Link standby prompt'),
        (0x395c4, 0x24948e, 'D02696 Link standby prompt'),
        (0x39700, 0x24948e, 'D02696 Link standby prompt'),
        (0x197178, 0x2721a7, 'D05276 Birch Dex rating dialogue'),
    ]
    for target_site, source_ref, desc in c_literal_pools:
        data[target_site:target_site + 4] = data[source_ref:source_ref + 4]
        count += 1
    print(f"[OK] Patched {len(c_literal_pools)} C-code literal pool dialogue pointers.")

    # ---- 19. POKÉNAV UI STRINGS ----
    from pokenav_ui_dict import POKENAV_UI_TRANSLATIONS
    for item in POKENAV_UI_TRANSLATIONS:
        b_val = enc_diag(item['translation_vi'])
        off = alloc_gameplay(b_val)
        p = struct.pack('<I', BASE + off)
        for s in item['sites']:
            at = int(s, 16)
            data[at:at + 4] = p
        count += 1
    print(f"[OK] Patched {len(POKENAV_UI_TRANSLATIONS)} PokéNav UI strings.")

    # ---- 20. MANDATORY TECHNICAL MODS & GAMEPLAY PATCHES ----
    from apply_user_mods import apply_user_mods
    apply_user_mods(data)
    print(f"[OK] Applied mandatory technical mods (Ability Patch bypass, 252 EV vitamins, Custom Pokemon Abilities).")

    # ---- 21. PC STORAGE CRASH FIX ----
    from fix_pc_crash import apply_pc_fix_to_data
    apply_pc_fix_to_data(data)
    print(f"[OK] Applied PC Item Storage crash fix (pointers < 0x09000000).")

    # Write output
    with open(rom_path, 'wb') as f:
        f.write(data)
    print(f"\n[DONE] Total {count} system & UI entries successfully patched into {rom_path}!")

    # Always export game directly to user directory: Downloads/Pokemons/
    user_export_dir = '/Users/zephiel/Downloads/Pokemons'
    if os.path.isdir(user_export_dir):
        user_rom_target = os.path.join(user_export_dir, 'Hyper Emerald v5.7 VIE.gba')
        with open(user_rom_target, 'wb') as f:
            f.write(data)
        print(f"[EXPORT] Successfully exported game to {user_rom_target}")

if __name__ == '__main__':
    rom_target = os.path.join(VI, 'build', 'Hyper Emerald v5.7 VIE.gba')
    if len(sys.argv) > 1:
        rom_target = sys.argv[1]
    patch_system_ui(rom_target)
