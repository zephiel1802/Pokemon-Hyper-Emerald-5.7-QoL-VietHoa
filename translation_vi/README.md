# translation_vi — Việt hóa Hyper Emerald 5.7 Lost Artifacts

Rebuild dump: `python3 translation_vi/tools/dump_all.py [rom.gba]` (~2 giây, chỉ đọc ROM, không ghi).

## Cấu trúc
| Đường dẫn | Nội dung |
| --- | --- |
| `dialogues/dialogues_000..026.json` | Hội thoại script (msgbox / message / trainerbattle), 400 câu/file, sắp theo offset |
| `tables/items_names.json` | Tên vật phẩm (trường cố định 14 byte → tối đa 13 byte, sửa tại chỗ) |
| `tables/items_descriptions.json` | Mô tả vật phẩm (gộp theo con trỏ, `pointer_at` = vị trí con trỏ trong bảng item) |
| `tables/pokedex_categories.json` | Phân loại Pokédex ("Seed Pokémon"…; trường cố định 12 byte) |
| `tables/pokedex_descriptions.json` | Mô tả Pokédex (gộp theo con trỏ) |
| `tables/moves_descriptions.json` | Mô tả chiêu thức — bảng con trỏ `0x09D2AD00` (chỉ số move-1). Tên chiêu chỉ để tham khảo, GIỮ tiếng Anh |
| `tables/abilities_descriptions.json` | Mô tả đặc tính — bảng con trỏ ở header `0x1C4` (`0x09D00218`). Tên đặc tính GIỮ tiếng Anh |
| `tables/quests_journal_questlog.json` | Journal / Quest Log — lấy từ `patches/` (CHƯA có trong ROM này) |
| `stats.json` | Thống kê lần dump gần nhất |
| `tools/gen3text.py` | Codec Gen3 không mất dữ liệu (cú pháp token giống `translation/inserter.py`) |

## Trường dữ liệu hội thoại
- `original_en` / `translation_vi`: dịch vào `translation_vi`; `"@@SKIP@@"` = giữ nguyên bản gốc.
- `refs`: vị trí từng con trỏ script trỏ tới chuỗi (cần repoint ở Giai đoạn 3). `aligned_refs`: con trỏ dạng bảng dữ liệu khác.
- `source`: `walk` (đi theo script của map), `scan` (quét opcode thô), `scan+walk` (cả hai — tin cậy nhất).
- `maps`: map chứa script (ngữ cảnh người nói). `has_chinese`: còn sót tiếng Trung (dịch từ tiếng Trung).
- `inside_of`: chuỗi bắt đầu giữa một chuỗi khác. `auto_skip`: lý do bị đặt sẵn `@@SKIP@@`.
- `low_confidence`: walk-only nhưng trông không giống text chuẩn (thường là "……", "Oh…").

## Token (giữ nguyên khi dịch)
`\n` `\l` `\p` là **chuỗi 2 ký tự** (dấu gạch chéo ngược + chữ), không phải ký tự xuống dòng.
Khi dịch: giữ số lượng `\p`, thay `\n`/`\l` bằng dấu cách (inserter tự ngắt dòng).
`[BUFxx]` biến tên · `[FCxx..]` màu/âm thanh/tạm dừng · `[F8xx]`/`[F9xx]` icon · `[Lv]` ·
`[S53][S54]` = PKMN · `[S55]..[S59]` = POKéBLOCK · `[S79]..[S7D]` mũi tên · `[S37]..[S3E]` dấu câu Trung.
