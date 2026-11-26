# 🌟 POKÉMON HYPER EMERALD v5.7 VIE — TỔNG KẾT DỰ ÁN & QUY CHUẨN KỸ THUẬT

> [!NOTE]
> Tài liệu này lưu trữ toàn bộ các thành phần đã Việt hóa, cấu trúc vùng nhớ, font chữ, cùng với các quy tắc can thiệp byte bắt buộc không được phép revert trong suốt vòng đời dự án.

---

## 1. THÔNG TIN BẢN ROM & ĐƯỜNG DẪN TỆP
* **Tên bản phát hành**: Pokémon Hyper Emerald v5.7 VIE (Tích hợp English QoL v1.8 Engine).
* **ROM gốc nền tảng**: `Hyper EMR LA v5.7 bugfix 2.gba` (GBA BPEE, 32 MB).
* **Đường dẫn ROM xuất chơi game**:
  `/Users/zephiel/Downloads/Pokemons/Hyper Emerald v5.7 VIE.gba`
* **Bộ tệp đồng bộ giả lập (mGBA / RetroArch)**:
  * `Hyper Emerald v5.7 VIE.sav` *(File save pin chính)*
  * `Hyper Emerald v5.7 VIE.ss1` *(Save state slot 1)*
  * `Hyper Emerald v5.7 VIE.cheats` *(Mã gian lận / Action Replay)*
  * `Hyper Emerald v5.7 VIE.gba.bak` *(File ROM backup)*
  * `Hyper Emerald v5.7 VIE.gba.v2.bak` *(File ROM backup v2)*

---

## 2. DANH MỤC CÁC THÀNH PHẦN ĐÃ VIỆT HÓA

### A. Kịch bản & Cốt truyện chính
* **Overworld**: Đã dịch toàn diện **174 batches** hội thoại thế giới (NPCs, Gym Leaders, Tứ Đại Thiên Vương, Champion, cốt truyện chính, thị trấn, tuyến đường).
* **Birch Intro**: Hoàn thành trọn bộ 9 chuỗi thoại mở đầu New Game.
* **System Prompts**: Việt hóa toàn bộ hộp thoại xác nhận lưu game (Save Game dialogs), bảng chọn Yes/No (Có / Không).
* **Pokédex Evaluation**: Toàn bộ lời thoại đánh giá Pokédex của Giáo sư Birch qua điện thoại.

### B. PokéNav Match Call
* Dịch chuẩn phong cách JRPG cho trọn bộ **336 cuộc gọi** (`MC0001` $\rightarrow$ `MC0336`), tích hợp qua `mc_part1.py` & `mc_part2.py`.
* Bảo toàn 100% control tokens (`[BUF01]`..`[BUF05]`, `\p`, `\n`, `\l`).
* Tự động kiểm soát bề rộng text $\le 174\text{px}$ chống tràn mép khung thoại.

### C. Giao diện & Chuỗi thông báo Chiến đấu (Battle UI & Strings)
* Giao diện trận đấu ("Tớ chọn cậu!", "Phe ta", "Phe địch", Hộp HP, Action Menu).
* **363/363 (100%)** chuỗi thông báo trận đấu `gBattleStringsTable` (BST).
* **312/315 chuỗi trận đấu mở rộng** (Mega Evolution, Z-Move, Dynamax, Terastral, Thời tiết, Trường địa hình).
* **QUY CHUẨN HIỂN THỊ CHỈ SỐ**: Giữ nguyên viết tắt tiếng Anh chuẩn để quan sát trực quan nhất:
  * `Atk` (Tấn công)
  * `Def` (Phòng thủ)
  * `Sp. Atk` (Tấn công Đặc biệt)
  * `Sp. Def` (Phòng thủ Đặc biệt)
  * `Speed` (Tốc độ)

### D. Hệ thống Menu & UI Toàn diện
* **Start Menu**: 7 mục cơ bản + 11 mục mở rộng có icon của Hyper Emerald (mở rộng khung menu chống tràn chữ).
* **Option Menu**: 7 tùy chọn cài đặt (Tốc độ chữ, Hiệu ứng đấu, Lối đấu, Âm thanh/Exp Gain, Chế độ nút, Khung viền, Thoát).
* **Tiêu đề Option**: Hiển thị chuẩn:
  `Hyper Emerald v5.7 VIE (Standard / Hard Mode / Challenge / Lunatic)`
* **Party Menu**: 7 lệnh tương tác Pokémon, màn hình Summary, học chiêu thức.
* **Túi đồ (Bag)**: 5 ngăn túi chính + 7 lệnh thao tác vật phẩm.
* **PC Storage**: 10 lệnh hệ thống hộp chứa Pokémon.
* **Các màn hình khác**: Cửa hàng Mart, màn hình Chọn giới tính, Bàn phím đặt tên tiếng Anh.
* **Gameplay Special Dialogues**: 107 chuỗi sự kiện đặc biệt trong engine C.

### E. Dọn dẹp chuỗi lỗi thời
* Triệt tiêu toàn bộ 14 vị trí chuỗi text `Ultra Emerald 5.5` còn sót từ nhóm tác giả Trung Quốc sang `Hyper Emerald 5.7` và `Hyper Emerald v5.7 VIE`.

---

## 3. NỀN TẢNG KỸ THUẬT & ENGINE GBA

### A. Bảng mã Font tiếng Việt
* Hack & đồng bộ **5 bảng font Latin Gen 3 GBA** (Normal, Narrow, Short, Small, Small Narrow) tại offset glyph `0x62BAE4` $\rightarrow$ `0x6542E4`.
* Định dạng glyph 2bpp, ô $16 \times 16\text{ pixel}$ (`fontlib.py`, `make_font.py`).
* Ánh xạ các ký tự có dấu (ă, â, đ, ê, ô, ơ, ư, dấu thanh, chữ in hoa) vào bảng mã custom an toàn trong `insert.py` & `gen3text.py`.

### B. Phân bổ Vùng nhớ Trống An toàn (Safe Memory Pools)
* `0x36F3B8` – `0x36F7E0` (1.064 bytes): Pool UI cho Start Menu & Option Menu.
* `0x1F89260..`: Expanded System UI Pool cho Party, Summary, Move Learning, Bag, PC.
* `0x00FF24C0..`: Title Header Pool chứa 4 xâu tiêu đề độ khó Option, repoint bảng `0x1F07DF4`.
* `0x00FE6000..`: Pool cho các chuỗi hội thoại đặc biệt của engine C.

### C. Tích hợp Engine QoL v1.8
* Giữ nút `L` khi chọn chiêu trong trận để hiện bảng thông số chi tiết (Power, Acc, Priority, Contact...).
* Switch Ngày/Đêm (Day/Night: On/Off) trong Options.
* Bàn phím gõ tên tiếng Anh chuẩn.

---

## 4. QUY TẮC BẢO LƯU PATCH KỸ THUẬT BẮT BUỘC

> [!IMPORTANT]
> Mỗi khi cập nhật text, build lại hoặc ghi đè file ROM tại `/Users/zephiel/Downloads/Pokemons/Hyper Emerald v5.7 VIE.gba`, **BẮT BUỘC** phải thực thi lại các can thiệp byte sau để không làm mất mod của người dùng:

1. **Gỡ bỏ check trùng đặc tính của Ability Patch (Đặc tính cao dược)**:
   - Offset `0x1F00E84`: đổi từ `c7 d1` thành `c7 e7`
2. **Mở giới hạn 252 EV cho Vitamin (HP Up, Protein, Iron, Carbos, Calcium, Zinc)**:
   - Offset `0x6C468`: `0x63` $\rightarrow$ `0xFB`
   - Offset `0x6C470`: `0x64` $\rightarrow$ `0xFC`
   - Offset `0x6C476`: `0x64` $\rightarrow$ `0xFC`
   - Offset `0x6CA54`: `0x63` $\rightarrow$ `0xFB`
   - Offset `0x6CA5C`: `0x64` $\rightarrow$ `0xFC`
   - Offset `0x6CA62`: `0x64` $\rightarrow$ `0xFC`
3. **Hack đặc tính Pokémon (Bắt buộc đồng bộ cả BaseStats và Expanded Ability Table)**:
   * **Shedinja (ID 303)**:
     - BaseStats (`0xF1A804`): Ab1 (+22)=25 (Wonder Guard), Ab2 (+23)=5 (Sturdy), HA (+26)=5 (Sturdy)
     - ExpTable (`0x17A071A`): `[25, 5, 5]`
   * **Slaking (ID 366)**:
     - BaseStats (`0xF1AEE8`): Ab1 (+22)=54 (Truant), Ab2 (+23)=37 (Huge Power), HA (+26)=37 (Huge Power)
     - ExpTable (`0x17A0894`): `[54, 37, 37]`
   * **Regigigas (ID 539)**:
     - BaseStats (`0xF1C1D4`): Ab1 (+22)=112 (Slow Start), Ab2 (+23)=37 (Huge Power), HA (+26)=37 (Huge Power)
     - ExpTable (`0x17A0CA2`): `[112, 37, 37]`
   * **Spiritomb (ID 495)**:
     - BaseStats (`0xF1BD04`): Ab1 (+22)=46 (Pressure), Ab2 (+23)=25 (Wonder Guard), HA (+26)=151 (Infiltrator)
     - ExpTable (`0x17A0B9A`): `[46, 25, 151]`

---

## 5. SCRIPT PYTHON THỰC THI & LỆNH BUILD TỰ ĐỘNG

Mọi can thiệp kỹ thuật trên đã được quản lý tự động tại `translation_vi/tools/apply_user_mods.py` và tích hợp vào bước cuối của `translation_vi/tools/patch_system_ui.py`.

### Script Python độc lập (dùng khi cần can thiệp nhanh):
```python
import struct

rom_path = '/Users/zephiel/Downloads/Pokemons/Hyper Emerald v5.7 VIE.gba'

with open(rom_path, 'rb') as f:
    rom = bytearray(f.read())

# 1. Bypass check trùng Ability Patch
rom[0x1F00E84:0x1F00E86] = bytes.fromhex('c7 e7')

# 2. Vitamin 252 EV
for off, val in [(0x6C468, 0xFB), (0x6C470, 0xFC), (0x6C476, 0xFC),
                 (0x6CA54, 0xFB), (0x6CA5C, 0xFC), (0x6CA62, 0xFC)]:
    rom[off] = val

# 3. Custom Pokemon Abilities (BaseStats & ExpTable)
mods = [
    ('Shedinja',  303, 0xF1A804, 0x17A071A, 25,  5,   5),
    ('Slaking',   366, 0xF1AEE8, 0x17A0894, 54, 37,  37),
    ('Regigigas', 539, 0xF1C1D4, 0x17A0CA2, 112, 37,  37),
    ('Spiritomb', 495, 0xF1BD04, 0x17A0B9A, 46,  25, 151)
]
for name, idx, base_off, exp_off, ab1, ab2, ha in mods:
    rom[base_off + 22] = ab1
    rom[base_off + 23] = ab2
    rom[base_off + 26] = ha
    struct.pack_into('<HHH', rom, exp_off, ab1, ab2, ha)

with open(rom_path, 'wb') as f:
    f.write(rom)

print("Đã nạp thành công toàn bộ mod kỹ thuật vào ROM!")
```

### Lệnh một chạm build và xuất toàn bộ dự án:
```bash
python3 translation_vi/tools/patch_system_ui.py
```
