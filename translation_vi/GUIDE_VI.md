# Hướng dẫn dịch – Pokémon Hyper Emerald 5.7 Lost Artifacts (Tiếng Việt)

Mọi người dịch đều phải làm theo đúng file này, để cả game thống nhất một giọng văn.

## 1. Quy trình (bắt buộc)
1. Chỉ ĐỌC file nguồn được giao (`translation_vi/dialogues/dialogues_NNN.json` hoặc `translation_vi/tables/<bảng>.json`). **KHÔNG BAO GIỜ sửa file nguồn** và không chạy `merge_batch.py` (có nhiều người dịch chạy song song; trưởng nhóm sẽ merge).
2. Dịch mọi mục có `translation_vi` rỗng. Mục đã có `"@@SKIP@@"` hoặc đã có bản dịch thì bỏ qua.
3. Ghi kết quả vào `translation_vi/batches/<prefix>_partK.json` (K = 1, 2, 3…). Mỗi file là một object JSON phẳng `{khóa: "bản dịch"}`, khoảng 60–100 mục mỗi phần, UTF-8, `ensure_ascii=False`.
   - Khóa của hội thoại = `id` (ví dụ `"D05701"`).
   - Khóa của bảng = `"<bảng>@<offset_hex>"` (ví dụ `"moves_descriptions@0x6181c1"`).
   - Nên viết file bằng một script Python nhỏ (json.dump) để không bị lỗi escape. Trong JSON, `\p` được viết là `"\\p"`, đúng như `original_en` lưu nó.
4. Sau mỗi phần, chạy `python3 translation_vi/tools/check_batch.py translation_vi/batches/<file>.json`, sửa đến khi in ra `OK`.
5. Xong thì báo lại: số mục đã dịch, số mục SKIP, các file đã ghi, và những điểm còn phân vân.

## 2. Quy tắc kỹ thuật
- Giữ **chính xác** mọi token: `[BUF01]` (tên người chơi), `[BUF02]`–`[BUF04]` (biến: Pokémon/vật phẩm/số), `[BUF06]` (đối thủ), `[FCxx…]` (màu/âm thanh/tạm dừng), `[F8xx]`, `[F9xx]`, `[F7]`, `[Lv]`. Có thể đổi vị trí token trong câu cho tự nhiên, nhưng số lượng và nội dung phải giữ nguyên. Token màu `[FC01xx]` ở đầu câu thì để nguyên ở đầu.
- **Số lượng `\p` phải bằng đúng bản gốc.** Không được thêm hay bớt trang.
- **KHÔNG viết `\n` hoặc `\l`.** Thay bằng dấu cách; trình chèn sẽ tự ngắt dòng theo độ rộng pixel.
- Không kết thúc chuỗi bằng `\p`.
- Chuỗi rác, chuỗi vô nghĩa, chỉ có ký hiệu/mã: ghi `"@@SKIP@@"`. Chuỗi chỉ gồm `… … …` hoặc dấu câu thì giữ nguyên.
- Nội dung giữa hai `\p` nên ≤ ~90 ký tự (một hộp thoại có 2 dòng, mỗi dòng ~34 ký tự; dài hơn thì sẽ cuộn).
- **Độ dài:** cố gắng để bản dịch KHÔNG dài hơn tiếng Anh (bản dịch ngắn hơn hoặc bằng sẽ được ghi đè tại chỗ, an toàn nhất). Hãy dịch gọn, tự nhiên, bỏ từ thừa. Mỗi chữ cái có dấu chỉ tốn 1 byte.
- Ký tự được phép: chữ Việt có dấu, A–Z a–z 0–9, khoảng trắng, `! ? . , - … “ ” ‘ ' : ; ( ) % & + = / ♂ ♀ é É`. Không dùng `"` thẳng, `—`, emoji, ký tự tiếng Trung. Dấu ba chấm dùng `…`.
- Mục có `has_chinese` (tiếng Trung chưa dịch): dịch thẳng từ tiếng Trung sang tiếng Việt. Phần tiếng Anh xen trong đó thì vẫn theo các quy tắc này.

## 3. GIỮ NGUYÊN TIẾNG ANH (không dịch)
- Tên loài Pokémon (Pikachu, Mudkip, Rayquaza, Arceus…), tên chiêu thức (Tackle, Surf, Fly, Cut, Strength, Rock Smash, Waterfall, Dive, Flash…), đặc tính (Intimidate…), tính cách (Adamant…).
- **Tên mọi vật phẩm** (Potion, Poké Ball, Running Shoes, Rare Candy, Choice Band, Leftovers, Mega Bracelet, Key Stone, TM/HM…). Bảng tên vật phẩm vẫn để tiếng Anh, nên trong thoại cũng phải để y nguyên để khớp.
- Địa danh: Littleroot Town, Route 101, Petalburg City, Mt. Chimney, Meteor Falls, Space Center, Safari Zone, Battle Frontier… (giữ nguyên chữ "Town/City/Route").
- Tên người: Birch, Norman, May, Brendan, Wally, Steven, Wallace, Maxie, Archie, Zinnia, Volo, Cyrus… Danh xưng đi trước tên thì dịch: "Prof. Birch" → "Giáo sư Birch", "Mr. Steven" → "anh Steven".
- Tên hệ (Fire, Water, Grass…): "Fire-type" → "hệ Fire".
- Pokémon, Pokédex, Poké Mart, PokéNav, PC, HP, PP, Lv., Mega Evolution → "Tiến hóa Mega".

## 4. Thuật ngữ thống nhất
| Tiếng Anh | Tiếng Việt |
|---|---|
| Trainer | Huấn luyện viên (khi cần ngắn: HLV) |
| Pokémon Trainer | Huấn luyện viên Pokémon |
| Gym | Nhà thi đấu |
| Gym Leader | Thủ lĩnh Nhà thi đấu / Thủ lĩnh |
| Badge | Huy hiệu (Stone Badge → Huy hiệu Stone) |
| Elite Four | Tứ Hoàng |
| Champion | Quán quân |
| Pokémon League | Liên đoàn Pokémon |
| Pokémon Center | Trung tâm Pokémon |
| Team Magma / Team Aqua / Team Rocket / Team Galactic | Băng Magma / Băng Aqua / Băng Rocket / Băng Galactic |
| Grunt / Team Magma Member | Lính / Thành viên Băng Magma |
| Admin / Leader (của băng) | Chỉ huy / Thủ lĩnh |
| Professor / Prof. | Giáo sư |
| Mom / Dad | Mẹ / Bố |
| Rival | Đối thủ |
| wild Pokémon | Pokémon hoang dã |
| battle | trận đấu / đấu |
| Double Battle | Đấu đôi |
| party | đội hình |
| Bag | Túi |
| egg / Pokémon Egg | Trứng / Trứng Pokémon |
| evolve / evolution | tiến hóa |
| faint / fainted | gục ngã / bị hạ gục |
| level | cấp |
| move (chiêu) | chiêu thức / chiêu |
| ability | đặc tính |
| nature | tính cách |
| held item | vật phẩm giữ |
| stats | chỉ số |
| EXP. Points | điểm kinh nghiệm (EXP.) |
| Day Care | Nhà trẻ Pokémon |
| Secret Base | Căn cứ bí mật |
| Contest | Cuộc thi |
| Hall of Fame | Đại sảnh Danh vọng |
| Fragment / Artifact | Mảnh vỡ / Cổ vật |
| Quest / Journal | Nhiệm vụ / Nhật ký |
| Save the game | Lưu game |
| Yes / No | Có / Không |

Tiền tệ: "¥"/"$" giữ nguyên ký hiệu như bản gốc.

## 5. Xưng hô (phong cách Anime / Manga Pokémon Đặc Biệt)
- Người chơi với bạn bè cùng tuổi, đối thủ (May/Brendan) và NPC trẻ: **tớ – cậu** (hoặc **mình – bạn**).
- Wally (rụt rè, ngưỡng mộ người chơi): nói với người chơi thì xưng **tớ – cậu**, vì chưa biết giới tính người chơi nên không dùng anh/chị. Giọng nhút nhát, lễ phép.
- Giáo sư Birch và người lớn tuổi tốt bụng: **bác/ta – cháu/nhóc**.
- Mẹ: **mẹ – con**. Bố (Norman, cũng là Thủ lĩnh Nhà thi đấu): **bố – con**.
- Thủ lĩnh Nhà thi đấu, Tứ Hoàng, Quán quân: uy nghiêm, hào sảng mà thân thiện, xưng **ta/tôi**, gọi **nhóc/cậu**. Steven/Wallace nói với người chơi: **tôi – cậu**.
- Lính băng phản diện: hống hách, xưng **bọn ta/ta**, gọi **mi/nhóc/các ngươi**, gọi tổ chức là "Băng Magma chúng ta".
- Trùm (Maxie, Archie, Cyrus, Volo…): lạnh lùng, triết lý, tham vọng, xưng **ta – các ngươi/mi**.
- Huấn luyện viên NPC thường (Youngster, Lass, Hiker…): tự nhiên theo tuổi. Trẻ con: tớ–cậu. Người lớn: tôi–cậu/em. Ông bà: ông/bà–cháu.
- Nhân viên (Trung tâm Pokémon, cửa hàng): lịch sự, **quý khách / bạn**. Câu kinh điển của Nurse Joy: "Chào mừng đến Trung tâm Pokémon!"
- Pokémon là bạn đồng hành, như người nhà: "các bạn ấy", "bé", "nhóc", "đồng đội".
- Người chơi không rõ giới tính: tránh "anh/chị" khi nói với người chơi, dùng "cậu/nhóc/cháu/con".
- Tiền tố người nói dạng `Name:` (ví dụ "Steven: …") giữ tên, dịch chức danh: "Mom:" → "Mẹ:", "President:" → "Chủ tịch:", "Team Magma Member:" → "Lính Magma:".
- Từ cảm thán: "Hm?" → "Hửm?", "Oh!" → "Ồ!", "Huh?" → "Hả?", "Hahaha!" giữ nguyên, "Wow!" → "Oa!".

## 6. Văn phong theo loại
- Mô tả chiêu thức/đặc tính: câu ngắn, kiểu "Tấn công đối thủ bằng…", "Có thể khiến đối thủ bị bỏng." (hộp 2 dòng ~150px, khoảng ≤ 50 ký tự).
- Mô tả vật phẩm: hộp rất hẹp (3 dòng × ~17 ký tự). Viết cực gọn: "Hồi 20 HP cho một Pokémon."
- Pokédex: văn phong bách khoa, trung tính, tối đa 4 dòng × ~38 ký tự.
- Bảng chỉ dẫn / biển báo: "ROUTE 101 ↑ OLDALE TOWN" → giữ địa danh, dịch phần chữ.
- Không bịa nội dung, không bỏ ý quan trọng (nhất là gợi ý nhiệm vụ, vị trí).
