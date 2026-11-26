# -*- coding: utf-8 -*-
"""Comprehensive patcher for all Quest Log chapters, Journal steps, Legends, Key Items,
Side Content, Badges, Evolutions UI, and Overworld Journal in Pokemon Hyper Emerald 5.7 QoL v1.9.
"""
import json, os, struct, sys

HERE = os.path.dirname(os.path.abspath(__file__))
VI = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from insert import Encoder, NORMALIZE

BASE = 0x08000000

def patch_questlog_side(data, safe_alloc, enc):
    def norm(t):
        for k, v in NORMALIZE.items(): t = t.replace(k, v)
        return t

    def enc_raw(t):
        t = norm(t)
        return bytes(enc.byte(c) for c in t) + b'\xff'

    def enc_raw_no_term(t):
        t = norm(t)
        return bytes(enc.byte(c) for c in t)

    FONTW = 0x006542E4
    def px(text):
        t = norm(text)
        b = bytes(enc.byte(c) for c in t)
        return sum(data[FONTW + byte] for byte in b)

    def wrap_px_text(text, width=200):
        text = text.replace('\\n', ' ').replace('\n', ' ').replace('\\l', ' ').replace('\\p', ' ')
        words = text.split()
        lines, cur = [], ""
        for w in words:
            cand = w if not cur else cur + " " + w
            if px(cand) <= width:
                cur = cand
            else:
                lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
        return lines

    def wrap_px(text, width=158, max_lines=3):
        text = text.replace('\\n', ' ').replace('\n', ' ').replace('\\l', ' ').replace('\\p', ' ')
        words = text.split()
        lines, cur = [], ""
        for w in words:
            cand = w if not cur else cur + " " + w
            if px(cand) <= width:
                cur = cand
                continue
            lines.append(cur)
            cur = w
            if len(lines) == max_lines:
                break
        else:
            lines.append(cur)
            return lines
        last = lines[-1]
        while px(last + "…") > width:
            last = last.rsplit(" ", 1)[0] if " " in last else last[:-1]
        lines[-1] = last + "…"
        return lines

    def pane_lines(text, width=180, max_lines=7):
        text = text.replace('\\n', ' ').replace('\n', ' ').replace('\\l', ' ').replace('\\p', ' ')
        words = text.split()
        lines, cur = [], ""
        for w in words:
            cand = w if not cur else cur + " " + w
            if px(cand) <= width:
                cur = cand
                continue
            lines.append(cur)
            cur = w
            if len(lines) == max_lines:
                break
        else:
            lines.append(cur)
            return lines
        last = lines[-1]
        while px(last + "…") > width:
            last = last.rsplit(" ", 1)[0] if " " in last else last[:-1]
        lines[-1] = last + "…"
        return lines

    loc_cache = {}
    def get_loc(loc_str):
        if loc_str not in loc_cache:
            loc_cache[loc_str] = safe_alloc.alloc(enc_raw(loc_str))
        return loc_cache[loc_str]

    # ---- 1. Chapter headers in PAGES table (0xFEC5EC) ----
    chapter_titles = [
        (0xfec5f0, 'Hoenn'),
        (0xfec5f8, 'Hậu truyện'),
        (0xfec600, 'Sinnoh'),
        (0xfec608, 'Cổ vật'),
        (0xfec610, 'Huyền thoại'),
        (0xfec618, 'Đồ quan trọng'),
        (0xfec620, 'Nhiệm vụ phụ'),
        (0xfec628, 'Huy hiệu'),
        (0xfec630, 'Tiến hóa'),
    ]
    for site, title in chapter_titles:
        off = safe_alloc.alloc(enc_raw(title))
        data[site:site + 4] = struct.pack('<I', BASE + off)

    # ---- 2. UI Labels & Headers ----
    # Location label in info panel (0xFEA858)
    loc_label_off = safe_alloc.alloc(enc_raw('Vị trí:'))
    data[0xfea858:0xfea85c] = struct.pack('<I', BASE + loc_label_off)

    # Evolutions method label (0xFEA85C)
    meth_label_off = safe_alloc.alloc(enc_raw('Cách tiến hóa'))
    data[0xfea85c:0xfea860] = struct.pack('<I', BASE + meth_label_off)

    # Evolutions "Not seen yet." labels (0xFEBC78, 0xFEBC7C)
    b_notseen_suffix = b'\x01\x02\x05\x00' + enc_raw('Chưa bắt gặp.')
    notseen_off = safe_alloc.alloc(b'\x09\x02\x05\x00' + b_notseen_suffix)
    data[0xfebc78:0xfebc7c] = struct.pack('<I', BASE + notseen_off)
    data[0xfebc7c:0xfebc80] = struct.pack('<I', BASE + notseen_off + 4)

    # Overworld Journal Headers
    ow_headers = [
        ([0xfe8590, 0x1fe1e58], 'Hoenn - Mục tiêu tiếp theo:'),
        ([0xfe8710, 0x1fe1fd8], 'Hậu truyện - Mục tiêu tiếp theo:'),
        ([0xfe8980, 0x1fe22b8], 'Sinnoh - Mục tiêu tiếp theo:'),
        ([0xfe89b0, 0x1fe22e8], 'Cổ vật - Mục tiêu tiếp theo:'),
    ]
    for sites, hdr_text in ow_headers:
        hdr_off = safe_alloc.alloc(enc_raw(hdr_text))
        for s in sites:
            data[s:s + 4] = struct.pack('<I', BASE + hdr_off)

    # ---- 3. Status Tags (Done, To do, Active, Seen, Locked, Side) ----
    done_off = safe_alloc.alloc(enc_raw('Xong'))
    todo_off = safe_alloc.alloc(enc_raw('Cần làm'))
    active_off = safe_alloc.alloc(enc_raw('Đang làm'))
    seen_off = safe_alloc.alloc(enc_raw('Đã gặp'))
    locked_off = safe_alloc.alloc(enc_raw('Khóa'))
    side_off = safe_alloc.alloc(enc_raw('Phụ'))

    # gen9journal status tags table at 0x1FE8078..0x1FE80A4
    data[0x1fe807c:0x1fe8080] = struct.pack('<I', BASE + done_off)
    data[0x1fe8080:0x1fe8084] = struct.pack('<I', BASE + active_off)
    data[0x1fe8084:0x1fe8088] = struct.pack('<I', BASE + side_off)
    data[0x1fe8090:0x1fe8094] = struct.pack('<I', BASE + seen_off)
    data[0x1fe8098:0x1fe809c] = struct.pack('<I', BASE + todo_off)
    data[0x1fe809c:0x1fe80a0] = struct.pack('<I', BASE + done_off)
    data[0x1fe80a0:0x1fe80a4] = struct.pack('<I', BASE + locked_off)

    # old tags table at 0xFEBF30..0xFEBF54
    data[0xfebf30:0xfebf34] = struct.pack('<I', BASE + done_off)
    data[0xfebf34:0xfebf38] = struct.pack('<I', BASE + active_off)
    data[0xfebf38:0xfebf3c] = struct.pack('<I', BASE + side_off)
    data[0xfebf44:0xfebf48] = struct.pack('<I', BASE + seen_off)
    data[0xfebf4c:0xfebf50] = struct.pack('<I', BASE + todo_off)
    data[0xfebf50:0xfebf54] = struct.pack('<I', BASE + done_off)

    # ---- 4. KEY ITEMS CHAPTER (54 Items) ----
    key_json_path = os.path.join(VI, 'dialogues', 'key_items_vi.json')
    key_data = json.load(open(key_json_path, encoding='utf-8'))
    orig_keys_ptr = struct.unpack('<I', data[0xfeb22c:0xfeb230])[0] - BASE
    orig_keyp_ptr = struct.unpack('<I', data[0xfed364:0xfed368])[0] - BASE

    new_keys_entries = bytearray()
    new_keyp_entries = bytearray()

    for i, entry in enumerate(key_data):
        orig_row = data[orig_keys_ptr + 16*i : orig_keys_ptr + 16*(i+1)]
        orig_item, orig_flag = struct.unpack('<HH', orig_row[:4])

        name_off = safe_alloc.alloc(enc_raw(entry['name']))
        hint_off = safe_alloc.alloc(enc_raw(entry['hint']))

        where_lines = pane_lines(entry['where'], 180, 7)
        b_where = b'\xfe'.join(bytes(enc.byte(c) for c in l) for l in where_lines) + b'\xff'
        where_off = safe_alloc.alloc(b_where)

        loc_off = get_loc(entry['loc'])

        panel_lines = wrap_px(entry['where'], 158, 3)
        b_panel = b'\xfe'.join(bytes(enc.byte(c) for c in l) for l in panel_lines) + b'\xff'
        panel_off = safe_alloc.alloc(b_panel)

        new_keys_entries.extend(struct.pack('<HHIII', orig_item, orig_flag, BASE + name_off, BASE + hint_off, BASE + where_off))
        new_keyp_entries.extend(struct.pack('<BBHIII', 3, 0, orig_item, BASE + loc_off, BASE + panel_off, BASE + panel_off))

    new_keys_off = safe_alloc.alloc(bytes(new_keys_entries))
    new_keyp_off = safe_alloc.alloc(bytes(new_keyp_entries))
    data[0xfeb22c:0xfeb230] = struct.pack('<I', BASE + new_keys_off)
    data[0xfed364:0xfed368] = struct.pack('<I', BASE + new_keyp_off)
    print(f"[OK] Patched {len(key_data)} Key Items rows (keys @{hex(BASE+new_keys_off)}, panes @{hex(BASE+new_keyp_off)}).")

    # ---- 5. SIDE CONTENT & BADGES (63 Entries) ----
    side_json_path = os.path.join(VI, 'dialogues', 'side_quests_vi.json')
    side_data = json.load(open(side_json_path, encoding='utf-8'))
    orig_sides_ptr = struct.unpack('<I', data[0xfeb230:0xfeb234])[0] - BASE
    orig_sidep_ptr = struct.unpack('<I', data[0xfed368:0xfed36c])[0] - BASE

    new_sides_entries = bytearray()
    new_sidep_entries = bytearray()

    for i, entry in enumerate(side_data):
        orig_row = data[orig_sides_ptr + 16*i : orig_sides_ptr + 16*(i+1)]
        orig_also_shiny, orig_flag = struct.unpack('<HH', orig_row[:4])

        orig_prow = data[orig_sidep_ptr + 16*i : orig_sidep_ptr + 16*(i+1)]
        orig_kind, _, orig_pid = struct.unpack('<BBH', orig_prow[:4])

        name_off = safe_alloc.alloc(enc_raw(entry['name']))

        where_lines = pane_lines(entry['where'], 180, 7)
        b_where = b'\xfe'.join(bytes(enc.byte(c) for c in l) for l in where_lines) + b'\xff'
        where_off = safe_alloc.alloc(b_where)

        loc_off = get_loc(entry['loc'])

        place, _, what = entry['where'].partition(': ')
        panel_lines = wrap_px(what if what else entry['where'], 158, 3)
        b_panel = b'\xfe'.join(bytes(enc.byte(c) for c in l) for l in panel_lines) + b'\xff'
        panel_off = safe_alloc.alloc(b_panel)

        new_sides_entries.extend(struct.pack('<HHIII', orig_also_shiny, orig_flag, BASE + name_off, BASE + where_off, BASE + where_off))
        new_sidep_entries.extend(struct.pack('<BBHIII', orig_kind, 0, orig_pid, BASE + loc_off, BASE + panel_off, BASE + panel_off))

    new_sides_off = safe_alloc.alloc(bytes(new_sides_entries))
    new_sidep_off = safe_alloc.alloc(bytes(new_sidep_entries))
    data[0xfeb230:0xfeb234] = struct.pack('<I', BASE + new_sides_off)
    data[0xfed368:0xfed36c] = struct.pack('<I', BASE + new_sidep_off)
    print(f"[OK] Patched {len(side_data)} Side Content & Badges rows (sides @{hex(BASE+new_sides_off)}, panes @{hex(BASE+new_sidep_off)}).")

    # ---- 6. JOURNAL STORY STEPS (92 Steps: Hoenn, Post-game, Sinnoh, Lost Artifacts) ----
    journal_json_path = os.path.join(VI, 'dialogues', 'journal_steps_vi.json')
    journal_data = json.load(open(journal_json_path, encoding='utf-8'))
    orig_jtitles_ptr = struct.unpack('<I', data[0xfeb248:0xfeb24c])[0] - BASE
    orig_jpanes_ptr = struct.unpack('<I', data[0xfed35c:0xfed360])[0] - BASE

    new_jtitles_ptrs = []
    new_jpanes_entries = bytearray()
    new_steps_entries = bytearray()

    for i, entry in enumerate(journal_data):
        orig_prow = data[orig_jpanes_ptr + 16*i : orig_jpanes_ptr + 16*(i+1)]
        orig_kind, _, orig_pid = struct.unpack('<BBH', orig_prow[:4])

        title_off = safe_alloc.alloc(enc_raw(entry['title']))
        new_jtitles_ptrs.append(BASE + title_off)

        loc_off = get_loc(entry['loc'])

        # 3-line panel text for the right-hand preview panel
        panel_lines = wrap_px(entry['body'], 158, 3)
        b_panel = b'\xfe'.join(bytes(enc.byte(c) for c in norm(l)) for l in panel_lines) + b'\xff'
        panel_off = safe_alloc.alloc(b_panel)

        new_jpanes_entries.extend(struct.pack('<BBHIII', orig_kind, 0, orig_pid, BASE + loc_off, BASE + panel_off, BASE + panel_off))

        # STEPS entry (for open_detail full popup and overworld [R] Journal / Bag journal)
        # Read original step metadata from 0x1FE1E50 + 16*i
        orig_srow = data[0x1fe1e50 + 16*i : 0x1fe1e50 + 16*(i+1)]
        mode, anchor, n_flags, _, flags_ptr, _, group_ptr = struct.unpack('<BBBBIII', orig_srow)

        # Handle group labels (Step 67, 71, 73)
        new_group_ptr = group_ptr
        if mode == 2 and group_ptr != 0:
            g_off = group_ptr - BASE
            label_ptr, n_mem, list_all, pad = struct.unpack('<IBBH', data[g_off:g_off+8])
            members_blob = data[g_off+8 : g_off+8 + 8*n_mem]
            grp_labels = {
                67: 'Đã xong:',
                71: 'Huy hiệu Sinnoh:',
                73: 'Phiến đá đã tìm:'
            }
            grp_lbl = grp_labels.get(i, 'Tiến độ:')
            lbl_off = safe_alloc.alloc(enc_raw(grp_lbl))
            new_grp_bytes = struct.pack('<IBBH', BASE + lbl_off, n_mem, list_all, 0) + members_blob
            new_grp_off = safe_alloc.alloc(new_grp_bytes)
            new_group_ptr = BASE + new_grp_off

        # Wrap body lines for detail popup & overworld box
        step_lines = wrap_px_text(entry['body'], 200)
        # Format: header + \xfe + line0 + (\xfa + line1 ...) + \xff
        b_step = enc_raw_no_term(entry['header']) + b'\xfe'
        for line_idx, l in enumerate(step_lines):
            if line_idx > 0:
                b_step += b'\xfa'
            b_step += enc_raw_no_term(l)
        b_step += b'\xff'
        step_text_off = safe_alloc.alloc(b_step)

        new_steps_entries.extend(struct.pack('<BBBBIII', mode, anchor, n_flags, 0, flags_ptr, BASE + step_text_off, new_group_ptr))

    new_jtitles_blob = struct.pack(f'<{len(new_jtitles_ptrs)}I', *new_jtitles_ptrs)
    new_jtitles_off = safe_alloc.alloc(new_jtitles_blob)
    new_jpanes_off = safe_alloc.alloc(bytes(new_jpanes_entries))
    new_steps_off = safe_alloc.alloc(bytes(new_steps_entries))

    data[0xfeb248:0xfeb24c] = struct.pack('<I', BASE + new_jtitles_off)
    data[0xfed35c:0xfed360] = struct.pack('<I', BASE + new_jpanes_off)

    # Repoint all 4 sites in the ROM to the new STEPS table
    data[0xfe563c:0xfe5640] = struct.pack('<I', BASE + new_steps_off)
    data[0xfea3f4:0xfea3f8] = struct.pack('<I', BASE + new_steps_off)
    data[0xfeac7c:0xfeac80] = struct.pack('<I', BASE + new_steps_off)
    data[0x1fe2c0c:0x1fe2c10] = struct.pack('<I', BASE + new_steps_off)

    print(f"[OK] Patched {len(journal_data)} Journal story steps (titles @{hex(BASE+new_jtitles_off)}, panes @{hex(BASE+new_jpanes_off)}, steps @{hex(BASE+new_steps_off)}).")

    # ---- 7. LEGENDS CHAPTER (125 Entries) ----
    leg_json_path = os.path.join(VI, 'dialogues', 'legends_vi.json')
    leg_data = json.load(open(leg_json_path, encoding='utf-8'))
    orig_leg_ptr = struct.unpack('<I', data[0xfeb23c:0xfeb240])[0] - BASE
    orig_legp_ptr = struct.unpack('<I', data[0xfed360:0xfed364])[0] - BASE

    new_leg_entries = bytearray()
    new_legp_entries = bytearray()

    for i, entry in enumerate(leg_data):
        orig_row = data[orig_leg_ptr + 16*i : orig_leg_ptr + 16*(i+1)]
        orig_dex, orig_locked = struct.unpack('<HH', orig_row[:4])

        orig_prow = data[orig_legp_ptr + 16*i : orig_legp_ptr + 16*(i+1)]
        orig_kind, _, orig_pid = struct.unpack('<BBH', orig_prow[:4])

        name_off = safe_alloc.alloc(enc_raw(entry['name']))

        hint_lines = pane_lines(entry['hint'], 180, 7)
        b_hint = b'\xfe'.join(bytes(enc.byte(c) for c in l) for l in hint_lines) + b'\xff'
        hint_off = safe_alloc.alloc(b_hint)

        where_lines = pane_lines(entry['where'], 180, 7)
        b_where = b'\xfe'.join(bytes(enc.byte(c) for c in l) for l in where_lines) + b'\xff'
        where_off = safe_alloc.alloc(b_where)

        loc_off = get_loc(entry['loc'])

        where_panel_lines = wrap_px(entry['where'], 158, 3)
        b_where_panel = b'\xfe'.join(bytes(enc.byte(c) for c in l) for l in where_panel_lines) + b'\xff'
        where_panel_off = safe_alloc.alloc(b_where_panel)

        hint_panel_lines = wrap_px(entry['hint'], 158, 3)
        b_hint_panel = b'\xfe'.join(bytes(enc.byte(c) for c in l) for l in hint_panel_lines) + b'\xff'
        hint_panel_off = safe_alloc.alloc(b_hint_panel)

        new_leg_entries.extend(struct.pack('<HHIII', orig_dex, orig_locked, BASE + name_off, BASE + hint_off, BASE + where_off))
        new_legp_entries.extend(struct.pack('<BBHIII', orig_kind, 0, orig_pid, BASE + loc_off, BASE + where_panel_off, BASE + hint_panel_off))

    new_leg_off = safe_alloc.alloc(bytes(new_leg_entries))
    new_legp_off = safe_alloc.alloc(bytes(new_legp_entries))
    data[0xfeb23c:0xfeb240] = struct.pack('<I', BASE + new_leg_off)
    data[0xfed360:0xfed364] = struct.pack('<I', BASE + new_legp_off)
    print(f"[OK] Patched {len(leg_data)} Legends rows (legends @{hex(BASE+new_leg_off)}, panes @{hex(BASE+new_legp_off)}).")
    print(f"[OK] 100% COMPLETE QUEST LOG & JOURNAL LOCALIZATION DEPLOYED!")
