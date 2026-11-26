# Báo Cáo Kỹ Thuật: Kiến Trúc & Kỹ Thuật Việt Hóa Pokémon Hyper Emerald – Lost Artifacts 5.7 (GBA, BPEE)

> **Mục đích:** Tổng hợp kiến trúc kỹ thuật (ROM layout, mã hóa text, con trỏ, đồ họa nén), nguyên nhân các lỗi của bản Việt hóa `Hyper Emerald 5.7 VIE.gba` (nát title, treo trong trận đấu), cách vá và kế hoạch tiếp theo.
> **Tệp tài liệu:** `/Users/zephiel/Downloads/Project/personal/GameVH/Pokemons/hyper_emerald_architecture_summary.md`
> **Tựa game:** Pokémon Hyper Emerald – Lost Artifacts 5.7 (GBA, header `POKEMON EMER` / `BPEE`), ROM hack nền Emerald, 32 MB. Title screen dùng logo tiếng Trung.
> **Cập nhật lần cuối:** 2026-10-26 (Bản build hiện tại: `Hyper Emerald 5.7 VIE (fixed).gba`)
> **Phạm vi đã khảo sát:** ROM layout, text/pointer, LZ77, code, savestate debug. **Chưa khảo sát:** font/glyph tiếng Việt, bảng độ rộng ký tự, video (xem mục 2–5, 9).

---

## 1. Bản Đồ ROM & Bộ Công Cụ (Layout & Toolchain)

### A. Các file trong thư mục `Pokemons/`
| File | Vai trò |
| :--- | :--- |
| `Hyper Emerald Lost Artifacts 5.7.gba` | **ROM gốc (tham chiếu sạch, chỉ đọc).** Mọi so sánh/khôi phục lấy từ đây. |
| `Hyper Emerald 5.7 VIE.gba` | Bản Việt hóa gốc (dựng 2026-10-25), **có lỗi** (mục 6). Không sửa. |
| `Hyper Emerald 5.7 VIE (fixed).gba` | Bản đã vá (mục 6). Kèm `.sav`, `.ss1`, `.cheats` copy từ bản VIE. |
| `Hyper Emerald 5.7 VIE (fixed).ss2` | Savestate **tại thời điểm treo** (dùng để debug, đừng load lại). |

### B. Bản đồ vùng ROM (offset file = địa chỉ − `0x08000000`)
| Vùng | Nội dung | Ghi chú |
| :--- | :--- | :--- |
| `0x000000–0x1CFFFF` | Code Emerald + dữ liệu | Bản VIE chỉ sửa 8 chỗ có chủ đích + ~389 literal pool pointer. |
| `0x1D0000–0x2C0000` | Text/script hội thoại (MB 1–2) | Dịch tại chỗ, nhiều pointer script bị đổi. |
| `0x1D37CE0–0x1D37FF0` | Bảng 196 con trỏ hàm Thumb | Từng bị hỏng (mục 6.2). |
| `0x1D4000–0x1D8000` | Code Thumb mở rộng của hack (cả hai ROM giống hệt) | Gọi hàm qua veneer `bx rN` (vd `0x1D45888 = bx r3`). |
| `0x55D30D–0x56B5AD` | Mô tả Pokédex (~387 chuỗi) | Dịch tại chỗ. |
| `0x5984FA…` | Bảng tên move/ability/type | **Không đổi** giữa hai bản. |
| `0xB9xxxx–0xBBxxxx`, `0xD5xxxx`, `0x1F7xxxx–0x1FDxxxx` | Vùng text VIE mới ghi (một phần là vùng trống 0xFF của bản gốc) | Text chuyển chỗ + text mới. |
| `0xF20xxx`, `0x169xxxx`, `0x1ACxxxx` | 3 bản sao bảng sprite sheet nén `{ptr, size|tag}` | Trỏ tới các block LZ77 `0x800`/`0x1000`. |
| `0xFAE1A0` | **Bitmap title (LZ77, 0x9600 byte = 600 tile 8bpp, lưới 30×20)** | Dùng palette 512 B trong RAM. Block thứ hai ở `0xFA5ED0`. |
| `0x1C1EB94…0x1C26D54`, `0x1C21xxx–0x1C25xxx` | Bảng Pokédex (stride `0x20`), con trỏ tới mô tả | ~775 pointer từng không được cập nhật. |

### C. Nguyên tắc & công cụ
- ROM gốc giữ chỉ đọc. Bản vá luôn tạo trên **bản sao**; so sánh luôn đối chiếu với ROM gốc.
- Script phân tích đã lưu trong dự án: `hyper_emerald_tools/` (xem `README.md`):
  - `he_common.py`: đọc ROM, giải LZ77 chặt (dist > output / hết dữ liệu → hỏng), tìm pointer/chuỗi, gom cụm khác biệt.
  - `audit_lz77.py`, `fix_text_pointers.py`, `audit_code_pointers.py`: kiểm tra/sửa khối nén, pointer text, pointer hàm.
  - `inspect_savestate.py`, `render_title.py`: đọc savestate mGBA (CPU/stack) và vẽ ảnh title.
  - Bảng mã Gen3: A=`0xBB`, a=`0xD5`, 0–9=`0xA1`, space=`0x00`, `-`=`0xAE`, `.`=`0xAD`, `!`=`0xAB`, `?`=`0xAC`.
- Thư viện: `capstone` (Thumb/ARM) đã có; Pillow có ở user-site (chạy `python3` **không** dùng `-I` khi cần PIL).

---

## 2. Cấu Trúc Font Của Game
**Chưa khảo sát.** Ghi nhận duy nhất: bản VIE dùng các mã byte tùy biến cho chữ có dấu, ví dụ `0x1F`, `0x20`, `0x29`, `0x2F`, `0x3F`, `0x46`, `0x4A`, `0x5A`, `0x61`–`0x76`, `0x8D`, `0x8E`, `0x9D`, `0x93`… (xuất hiện xen giữa chữ thường, vd `C<3f>u c<5a> mu<63>n`). Chưa xác minh glyph nằm ở đâu/bank nào.

## 3. Đường Vẽ Chữ & Bộ Giải Mã (Encoding)
- Text là **Gen3 charmap 1 byte**, kết thúc bằng `0xFF`. Mã điều khiển: `0xFE` xuống dòng, `0xFA` cuộn dòng, `0xFB` sang đoạn (`\p`), `0xFC xx` điều khiển, `0xFD xx` placeholder (`{PLAYER}`…), `0xF9 xx` ký tự mở rộng, `0xB0/B1/B2` nháy/ngoặc.
- Chuỗi hội thoại được tham chiếu bằng con trỏ 4 byte `0x08xxxxxx/0x09xxxxxx` ở nhiều dạng:
  - **Căn hàng 4:** trong bảng con trỏ và literal pool của code.
  - **Không căn hàng:** trong script event: `0F <slot> <ptr>` (loadword/msgbox), `04`/`05 <ptr>` (goto/call), `06`/`07 <cond> <ptr>`, `67 <ptr>` (message).
- Chuỗi VIE dài hơn gốc nên **bị chuyển chỗ**; vùng cũ thường bị lấp bằng `0xFF` hoặc bị ghi đè (xem Gotchas).

## 4. Bảng Độ Rộng Ký Tự & Canh Lề
**Chưa khảo sát.** Hai patch code liên quan có thể là nới giới hạn độ rộng/EV, chưa xác minh ý nghĩa (mục 6.4).

## 5. Kỹ Thuật Tạo & Ghép Glyph Tiếng Việt
**Chưa khảo sát** (bản VIE do nguồn khác dựng, không có script/glyph kèm theo trong thư mục).

---

## 6. Nhật Ký Lỗi & Cách Xử Lý (Debug Chronicles)

### 6.0. Nguyên nhân gốc chung
Công cụ dựng bản VIE dịch lại text, chuyển chỗ chuỗi rồi sửa pointer bằng cách **quét từng byte (cả vị trí không căn hàng) toàn ROM** tìm mọi word 4 byte trùng địa chỉ text cũ và thay bằng địa chỉ mới. Word trùng ngẫu nhiên nằm trong dữ liệu **không phải pointer** (ảnh nén, bảng con trỏ hàm, vắt ngang 2 entry) bị ghi hỏng.

| # | Hiện tượng | Nguyên nhân | Cách phát hiện | Cách xử lý |
| :--- | :--- | :--- | :--- | :--- |
| 6.1 | Title nát hình lưới ô 8×8 | 4 byte trong stream LZ77 `0xFAE1A0` (tại `0xFAFB32`: `0d 06 e5 09` → `08 17 b6 08`) bị coi là pointer → mọi dữ liệu sau byte ~9500 giải nén ra rác | Trích VRAM từ savestate mGBA (`gbAs` → zlib), khớp tile với block LZ77, render lại 8bpp tiled | Chép lại byte gốc của block |
| 6.1b | Cùng lỗi ở **53 block LZ77** (42 không giải nén được, 11 giải nén sai) ~1% số block được tham chiếu | như trên | Duyệt mọi block LZ77 được trỏ bởi pointer căn hàng trong ROM gốc, so sánh giải nén VIE vs gốc cùng offset | Khôi phục toàn bộ 53 block từ ROM gốc (đã xác minh giải nén khớp 100%) |
| 6.2 | **Treo trong trận đấu đôi** (savestate: `cpsr=0x9B` = chế độ Undefined, `PC=8`) | Bảng hàm Thumb `0x1D37CE0`: cửa sổ `d7 09 e5 09` vắt ngang 2 entry → `0x09D70899`→`0x2AD00899` (rác), `0x09D709E5`→`0x09D708B6` (sai địa chỉ, **mất bit Thumb**). Game gọi `bx r3` với `r3` chẵn → vào ARM → chạy rác | Đọc thanh ghi trong state (`r0..r15` tại offset `0x20..0x5C`), stack ở IWRAM, kiểm tra các địa chỉ return đứng sau `BL`, thấy `bx r3` ở `0x1D45888` | Khôi phục 8 byte `0x1D37ED8–0x1D37EDF` từ ROM gốc; cả bảng giống hệt gốc |
| 6.3 | ~814 pointer text không được cập nhật → text cụt đầu/lệch | Công cụ chỉ sửa một phần pointer; vùng như bảng `0x1C1EB94` bị bỏ sót | Tìm slot pointer còn nguyên mà đích gốc là đầu chuỗi nhưng ở VIE đã không còn là đầu chuỗi | **515** sửa bằng ánh xạ theo thứ tự chuỗi trong từng cụm text (kiểm chứng 0 sai trên ~870 mốc); **292** sửa bằng ánh xạ từ pointer anh em trỏ cùng chuỗi đã được sửa; chi tiết còn lại ở 6.5 |
| 6.4 | Patch code có chủ đích (không phải lỗi) | – | Diff vùng `<0x1D0000` | `0x6C468/0x6C470/0x6C476` và `0x6CA54/0x6CA5C/0x6CA62`: ngưỡng `100/0x64` → `252/0xFC` (và `0x63` → `0xFB`); `0x1979EA/0x1979EE`: tham số cửa sổ `0x16,7` → `0x13,0xA`. Giữ nguyên |
| 6.5 | Chuỗi bị xóa/ghi dở khi chuyển chỗ | Công cụ ghi `0xFF`/`0x00` đè lên chuỗi cũ nhưng pointer vẫn trỏ vào | So sánh O vs V quanh đích pointer | Khôi phục chuỗi tiếng Anh gốc tại: `0x2C892A` ("Save error…", 47 B), `0x5E86B8` (nhãn `?????`, 5 B), `0x5EE6F3` ("Retire", 1 B), `0x2C8A13..0x2C8A1E` (đuôi + `0xFF` của "This is what we call a Pokémon.", 12 B) |

### Số liệu tổng quan bản VIE vs gốc (2026-10-26)
- 1,873,119 byte khác nhau, 81,330 run; vùng code `<0x1D0000` chỉ ~400 run (392 literal pool pointer + 8 patch).
- Bản fixed khác bản VIE: 53 block LZ77 (210 byte) + 515 + 292 pointer text + 8 byte bảng hàm + 65 byte chuỗi khôi phục.

---

## 7. Kỹ Thuật Debug & Reverse Engineering Thực Chiến
- **Savestate mGBA (`.ss1/.ss2`):** PNG chứa chunk `gbAs` (zlib) → state 0x61000 byte. Layout đã xác minh: `0x00` version, `0x10–0x1F` title/game code, **`0x20–0x5C` = r0–r15**, `0x60` cpsr, `0x64` spsr, bank mode lưu từ `0x70` (SP/LR của mode SYS ở `0x70/0x74`); VRAM tại `0x1000` (đã thử), **IWRAM `0x19000`**, **EWRAM `0x21000`**; palette giả định tại `0x800`. Screenshot là chính ảnh PNG.
- **Quy trình chẩn đoán treo:** đọc `cpsr` (mode `0x1B` = Undefined) → đọc stack từ SP trong IWRAM → xác minh từng địa chỉ return có `BL` đứng trước → disassemble hàm (`capstone`, `CS_MODE_THUMB`) → tìm giá trị con trỏ trong cả hai ROM → so sánh bảng chứa nó.
- **Phát hiện lỗi “pointer rewrite” hàng loạt:**
  1. Lấy mọi cửa sổ 4 byte (mọi offset) trong ROM gốc là pointer ROM mà ROM VIE khác.
  2. Phân loại theo ngữ cảnh: trong block LZ77 được tham chiếu → chắc chắn hỏng; trong bảng con trỏ mà đích gốc là **code** (không phải đầu chuỗi text) → hỏng; trong script (đứng sau `0F xx`, `04`, `05`…) → hợp lệ.
  3. Cẩn thận: cửa sổ căn hàng 4 có thể cắt ngang con trỏ script không căn hàng (nhiễu), và điều kiện "con trỏ lẻ = Thumb" **không đúng** vì địa chỉ chuỗi text cũng có thể lẻ.
- **Quy tắc vàng khi kiểm tra bản vá:** không load savestate cũ (đã chụp bằng ROM cũ), bắt đầu từ `.sav`.

---

## 8. Cấu Trúc Kịch Bản, Bảng Con Trỏ & Injection
- Mỗi chuỗi dịch có thể dài hơn bản gốc nên được **ghi tại chỗ nếu vừa**, hoặc **chuyển sang vùng trống / vùng mới** rồi sửa mọi pointer tới nó.
- Quy tắc sửa pointer an toàn (cần khi dựng lại bản VIE):
  - Chỉ sửa tại **slot pointer đã biết**: bảng căn hàng 4 (đã xác nhận là bảng text), literal pool có lệnh `ldr rX,[pc,#imm]` trỏ tới, và toán hạng script có opcode hợp lệ đứng trước.
  - **Không** quét mù mọi offset, **không** động vào vùng LZ77/ảnh/bảng con trỏ hàm.
  - Sau khi dựng: duyệt lại mọi block LZ77 và mọi slot đích code, so với ROM gốc.
- Nơi ghi text mới cần kiểm tra: không ghi đè chuỗi vẫn còn được tham chiếu (đã gặp 3 trường hợp, mục 6.5 và `0xBBF1B9`).

---

## 9. Đa Phương Tiện: Đồ Họa
- Title: LZ77 8bpp tiled (`0xFAE1A0`), logo Trung Quốc "精灵宝可梦 / 究极绿宝石V / Lost Artifacts" (chưa dịch/vẽ lại).
- Sprite trainer/Pokémon: bảng `CompressedSpriteSheet {ptr, size|tag}`, size `0x800` hoặc `0x1000`.
- Video/UI atlas: không có.

---

## 10. Rào Cản & Bất Biến (Gotchas)

> [!WARNING]
> **KHÔNG ĐƯỢC QUÉT MÙ POINTER TOÀN ROM.** Mỗi lần dựng lại bản VIE, một bộ quét theo byte sẽ lại phá ảnh nén và bảng con trỏ hàm. Mọi bản dựng mới phải có bước kiểm tra tự động (xem TODO).

1. **Con trỏ hàm Thumb luôn lẻ:** bất kỳ entry con trỏ code nào bị chẵn hoặc không còn trỏ vào hàm sẽ gây Undefined (state: `cpsr=0x9B`).
2. **Con trỏ text cũng có thể lẻ** – không thể dùng bit 0 để phân biệt text với code.
3. **Đầu chuỗi ≠ luôn có `0xFF` đứng trước:** trong script, text nằm ngay sau byte lệnh.
4. **Chuỗi VIE gộp:** một số chuỗi dịch mất ký tự kết thúc nên dính vào chuỗi sau (đã gặp ở `0x2C89FB`).
5. **Text mới có thể ghi đè chuỗi còn được dùng**, vd vùng `0xBBF144–0xBBF222` đè lên `0xBBF1B9` và `0xBBF1EE` (pointer `0x2EE83C` vẫn trỏ vào đó).
6. **Mã tuỳ biến cho chữ có dấu nằm lẫn trong dải `0x1F..0x9D`** – đừng dùng ngưỡng "≥0xA1 là chữ" để nhận diện text VIE.

---

## 11. Checklist Trạng Thái Hiện Tại (2026-10-26)

### Files
- [x] `Hyper Emerald 5.7 VIE (fixed).gba` – bản vá (53 block LZ77, 1 bảng hàm, 807 pointer text, 4 chuỗi khôi phục).
- [x] `Hyper Emerald 5.7 VIE (fixed).sav / .ss1 / .cheats` – copy từ bản VIE (`.ss1` chụp bằng ROM cũ, nên dùng `.sav`).
- [x] `Hyper Emerald 5.7 VIE (fixed).ss2` – state treo, chỉ để tham khảo.
- [x] Script phân tích đã lưu tại `hyper_emerald_tools/`.

### Đã chốt
- [x] Title khôi phục đúng (đã xác minh bằng render).
- [x] Nguyên nhân treo tìm ra (bảng hàm `0x1D37CE0`) và đã vá.
- [x] 807 / 814 pointer mồ côi đã sửa (515 + 292); 7 còn lại: 1 đúng sẵn (`0x30A64`), 4 được khôi phục chuỗi gốc, 1 không phải text (`0x9FB9E4`), 1 chưa sửa được (`0x2EE83C`).
- [ ] Chưa boot thử bản fixed trong mGBA sau các lần vá pointer text và chuỗi (chưa có CLI emulator).

---

## 12. Kế Hoạch Hành Động (TODO)

### A. Phiên làm việc tiếp theo
- [ ] **Chơi thử bản fixed từ `.sav`:** màn title, trận đôi (Magneton/Loudred vs Godchu/Genbu), Pokédex, các hộp thoại Birch/Save, mục "Retire".
- [ ] **Xử lý pointer `0x2EE83C` → `0xBBF1B9`:** chuỗi cũ bị ghi đè (trainer "A battle? Of course…"); tìm bản dịch của nó hoặc trỏ về chuỗi tiếng Anh gốc khôi phục.
- [ ] **Quét thêm lỗi tương tự:** duyệt toàn bộ bảng con trỏ hàm/ dữ liệu khác trỏ vào code mà bản VIE đã đổi (hiện chỉ thấy bảng `0x1D37CE0`).
- [x] Lưu bộ script phân tích vào dự án (`hyper_emerald_tools/`).

### B. Tương lai
- [ ] **Dựng lại bản VIE từ đầu** với bộ sửa pointer chỉ chạm các slot đã biết + kiểm tra tự động sau khi dựng (LZ77 so sánh, đích code không đổi, đích text là đầu chuỗi).
- [ ] **Khảo sát font/bảng độ rộng/glyph** tiếng Việt (mục 2–5).
- [ ] **Dịch lại ảnh title** (logo tiếng Trung) nếu muốn.
- [ ] **QA toàn bộ game:** các màn text dài, shop, Pokédex, tên địa danh.
