# -*- coding: utf-8 -*-
"""Full Vietnamese localization builder for Area Zero & Quest Log in Pokemon Hyper Emerald 5.7 QoL v1.9.
Strictly complies with references/pokemon_brief.md:
- 100% English: Species, Moves, Abilities, Items.
- Stats: HP, Atk, Def, SpAtk, SpDef, Speed.
- Natural Vietnamese dialogues & proper honorifics.
"""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
VI = os.path.dirname(HERE)
DIALOGUES = os.path.join(VI, 'dialogues')

# Load raw extracted lists
p_en = json.load(open(os.path.join(DIALOGUES, 'paldea_en.json'), encoding='utf-8'))
j_en = json.load(open(os.path.join(DIALOGUES, 'paldea_journal_en.json'), encoding='utf-8'))

# Translation table for Paldea dialogue
def get_paldea_vi(en):
    # exact or prefix matching
    t = en.replace('\n', ' ').replace('\l', ' ')
    
    # Jacq Mossdeep
    if "Oh! A Trainer! Thank goodness" in t:
        return "Jacq: Ồ! Một Huấn luyện viên! May quá...\\nXin lỗi nhé. Thầy tên là Jacq, dạy\\lSinh học ở Học viện tại vùng Paldea."
    if "I brought three of my students" in t and "Arven" in t:
        return "Jacq: Thầy dẫn 3 học sinh sang Hoenn nghiên cứu\\nthực địa: Arven, Nemona và Penny. Mấy đứa\\ltrẻ ngoan và rất ham học hỏi."
    if "The Space Center says this" in t and "wormholes all over Hoenn" in t:
        return "Jacq: Trung tâm Vũ trụ báo rằng cái hố này mở ra\\nngay đêm các Wormhole khắp Hoenn khép lại.\\lNhìn xem, đây không phải Ultra Wormhole."
    if "The kids went to take a closer" in t and "pulled them in" in t:
        return "Jacq: Mấy đứa nhóc tò mò lại gần xem,\\nvà hố đen đã hút sạch cả ba đứa vào trong."
    if "I went in after them" in t and "two hundred years old" in t:
        return "Jacq: Thầy lao vào cứu... rồi phải chạy thục mạng\\nra ngoài vì bị một Pokémon mà thầy chỉ từng\\lthấy trong cuốn sách cổ 200 năm trước đuổi."
    if "I know that place. It's the Great" in t and "Area Zero" in t:
        return "Jacq: Thầy biết nơi ấy. Đó là Đại Hố sâu của\\nPaldea — Area Zero. Cấm tuyệt đối vào đó,\\nvậy mà học sinh của thầy lại đang kẹt dưới kia."
    if "Your Pokémon look like they could" in t and "bring them back" in t:
        return "Jacq: Pokémon của em trông rất dũng mãnh.\\nXin em... hãy vào đó đưa các bạn ấy trở về\\lđược không? Thầy sẽ túc trực ở đây."
    if "You! The Trainer from before!" in t:
        return "Jacq: Em! Nhà huấn luyện lúc trước! May quá...\\nLà thầy đây, Jacq, giáo viên dẫn 3 học sinh\\lđi thực địa."
    if "The restless sky, remember?" in t:
        return "Jacq: Bầu trời chao đảo lúc trước, em nhớ chứ?\\nTrung tâm Vũ trụ báo cái hố này mở ra ngay\\nđêm các Wormhole khắp Hoenn đóng lại. Nhìn\\lxem, đây không phải Ultra Wormhole."
    if "Arven, Nemona and Penny are" in t and "bring them home" in t:
        return "Jacq: Arven, Nemona và Penny đang ở phía\\nbên kia hố đen. Xin em, hãy đưa các bạn\\lấy về an toàn nhé!"
    if "Oh, hello! A Trainer? My name's" in t and "long way from" in t:
        return "Jacq: Ồ, chào em! Nhà huấn luyện sao?\\nThầy tên là Jacq, dạy môn Sinh học tại Học viện\\nở Paldea. Nơi đó cách đây xa lắm."
    if "I've brought three of my" in t and "field study" in t:
        return "Jacq: Thầy dẫn 3 học sinh sang Hoenn nghiên cứu\\nthực địa: Arven, Nemona và Penny. Mấy đứa\\ltrẻ tò mò lắm, đang dạo quanh đảo rồi."
    if "We came for the sky." in t and "pressing on it" in t:
        return "Jacq: Thầy trò tới vì hiện tượng lạ trên trời.\\nTrung tâm Vũ trụ nói vùng trời bờ biển này dạo\\ngần đây chao đảo, như thể có thứ gì đó đang\\lđè nén từ thế giới bên kia."
    if "It's probably nothing! Still" in t and "wander too far" in t:
        return "Jacq: Chắc không có gì đâu! Dù vậy thầy vẫn dặn\\nmấy đứa không được đi xa... Cơ mà chúng nó\\lcó bao giờ chịu nghe đâu."
    if "Still nothing in the sky. Good!" in t:
        return "Jacq: Bầu trời vẫn chưa có gì lạ. Tốt lắm!\\nMột chuyến đi bình yên luôn là tuyệt nhất...\\lThầy vẫn tự nhủ lòng như vậy."
    if "A perfectly black hole hangs in the air" in t:
        return "Một hố đen sâu thẳm lơ lửng giữa không trung\\ntrên thảm cỏ. Có một luồng lực bí ẩn từ phía\\lbên kia đang lôi kéo bạn..."
    if "Whoa, whoa! Don't go near that!" in t:
        return "Jacq: Khoan, khoan đã! Đừng lại gần cái hố đó!"
    if "The black hole is pulling at you. Step" in t:
        return "Hố đen đang hút lấy bạn. Bước vào trong chứ?"
    if "Through the hole, you can faintly hear" in t:
        return "Qua miệng hố, bạn có thể nghe văng vẳng tiếng\\nsóng biển Mossdeep. Quay trở về chứ?"
    if "The hole lets go of you on a narrow" in t:
        return "Hố đen nhả bạn xuống một gờ đá hẹp cheo leo trên\\nvách núi. Xa tít phía dưới, cả cánh rừng bạt ngàn\\nbao phủ đáy miệng hố khổng lồ."
    if "This must be Area Zero..." in t:
        return "Nơi này hẳn chính là Area Zero..."

    # Ending dialogues at Mossdeep
    if "You're back! And you brought" in t:
        return "Jacq: Em đã về rồi! Và đưa được tất cả mọi người\\nra ngoài! Arven, Nemona, Penny... Cảm tạ trời đất."
    if "My parents' AIs went through" in t:
        return "Arven: Các bản thể AI của bố mẹ tớ đã bước qua\\ncỗ máy thời gian. Tớ nghĩ... cuối cùng họ cũng\\lđược tự do chọn con đường của mình."
    if "That was the best adventure" in t:
        return "Nemona: Đây quả là chuyến phiêu lưu tuyệt nhất\\ntừ trước tới nay! [BUF01], nhất định cậu\\lphải đấu với tớ một trận nữa đấy nhé!"
    if "I can't thank you" in t and "Please, take this" in t:
        return "Jacq: [BUF01], thầy không biết lấy gì để cảm ơn\\nem cho hết. Xin hãy nhận lấy món quà này."
    if "Koraidon and Miraidon" in t and "stayed behind at my picnic" in t:
        return "Arven: À này... Koraidon và Miraidon vẫn đang nán\\nlại ở chỗ dã ngoại của tớ. Tớ nghĩ là hai bạn\\lấy đang đợi cậu đấy."
    if "With that machine stopped, the" in t and "crater is finally safe" in t:
        return "Jacq: Khi cỗ máy thời gian dừng lại, cuối cùng\\nchúng ta cũng có thể an tâm nghiên cứu hố sâu.\\lMột giáo viên Sinh học cả đời khó gặp cơ hội này."
    if "I'm never going near a black" in t:
        return "Penny: Tớ thề sẽ không bao giờ lại gần hố đen\\nnữa... Cơ mà thôi được, có lẽ chỉ thêm một lần."
    if "We're going back in to finish" in t:
        return "Jacq: Thầy trò thầy sẽ quay lại để hoàn tất\\nchuyến thực địa. Em có thể tìm thấy chúng thầy\\ltrong các trạm nghiên cứu nhé!"
    if "Jacq and his students stepped back" in t:
        return "Thầy Jacq và các học sinh đã bước trở lại vào hố đen."

    # Lab door shutter
    if "A huge metal shutter is set into the" in t:
        return "Một cánh cửa cuốn kim loại khổng lồ gắn chặt vào\\nvách hố. Bảng điều khiển ghi: NHẬT KÝ TRẠM THIẾU."
    if "The panel beside the shutter reads:" in t and "STATION LOGS RECEIVED: 4 OF 4" in t:
        return "Bảng điều khiển cạnh cửa hiển thị: ĐÃ NHẬN ĐỦ 4/4\\nNHẬT KÝ TRẠM. ĐÃ MỞ KHÓA."
    if "But the shutter is far too heavy to" in t:
        return "Nhưng cánh cửa quá nặng để nâng một mình, và Arven\\ncùng Nemona vẫn chưa đến đây."
    if "Koraidon is still too weak to move" in t:
        return "Koraidon vẫn còn quá yếu để cử động.\\nArven cần thảo dược do Titan canh giữ."
    if "Miraidon is still too weak to move" in t:
        return "Miraidon vẫn còn quá yếu để cử động.\\nArven cần thảo dược do Titan canh giữ."
    if "Nemona is still battling in the future" in t:
        return "Nemona vẫn đang mải mê chiến đấu ở tương lai,\\ntrong bãi cỏ cao phía nam hồ nước."
    if "The machine is silent. The display reads: TIME MACHINE" in t:
        return "Cỗ máy im lìm. Màn hình hiển thị: CỖ MÁY THỜI GIAN.\\nCỔNG: ĐÃ ĐÓNG."
    if "Behind thick glass, an enormous machine hums" in t:
        return "Sau lớp kính dày, cỗ máy khổng lồ gầm rú. Màn hình\\nhiển thị: CỖ MÁY THỜI GIAN. CỔNG: ĐANG MỞ."

    # Time rifts
    if "Through the rift, the crater is cold and violet" in t:
        return "Qua vết rách, hố sâu mang sắc tím lạnh lẽo, và có\\nthứ gì đó bằng kim loại đang chuyển động..."
    if "Through the rift, the crater is warm and wild" in t:
        return "Qua vết rách, hố sâu ấm áp hoang sơ, và có thứ gì\\nđó khổng lồ từ thời cổ đại đang di chuyển..."
    if "A tear hangs in the air, shimmering" in t:
        return "Một vết rách không gian lơ lửng, lấp lánh ánh sáng.\\nQua đó, bạn có thể nhìn thấy chính hố sâu này ở thời đại khác..."

    # Nemona
    if "Nemona: Go, go, go! We'll keep the" in t:
        return "Nemona: Tiến lên, tiến lên! Bọn tớ sẽ chặn đứng\\nlũ Paradox Pokémon không để chúng quấy rầy cậu!"
    if "Haha! Another one down! Who's next?" in t:
        return "Nemona: Haha! Lại hạ thêm một con nữa! Đứa nào tiếp theo?"
    if "Wait, you're not a Paradox Pokémon! You're" in t:
        return "Nemona: Khoan đã, cậu không phải Paradox Pokémon!\\nCậu là nhà huấn luyện! Tuyệt vời, đấu với tớ một trận đi!"
    if "Nemona: Okay, okay, I'll stop battling" in t:
        return "Nemona: Rồi rồi, tớ sẽ tạm ngừng đấm nhau với bầy\\nParadox Pokémon... Chỉ tạm thời thôi đấy nhé!"
    if "Arven's by the lake, making sandwiches" in t:
        return "Nemona: Arven đang ở bờ hồ làm sandwich cho Koraidon\\nvà Miraidon. Đợi hai bạn ấy khỏe lại, bọn mình tính tiếp!"
    if "Arven's ready, and Penny unlocked the lab?" in t:
        return "Nemona: Arven đã sẵn sàng và Penny mở khóa phòng thí\\nnghiệm rồi ư? Vậy còn chờ gì nữa! Trận chiến lớn tới rồi!"
    if "We'll battle again when we're out of here" in t:
        return "Nemona: Chúng mình sẽ tái đấu khi ra khỏi đây nhé.\\nHứa đấy!"
    if "Nemona: Want to battle again?" in t:
        return "Nemona: Cậu muốn tái đấu một trận nảy lửa chứ?"
    if "Aww. I'll be right here when you change your mind!" in t:
        return "Nemona: Tiếc thế. Khi nào đổi ý cứ quay lại đây\\ntìm tớ bất cứ lúc nào nhé!"
    if "Hah! That never gets old. Come back any time!" in t:
        return "Nemona: Hah! Đấu với cậu lúc nào cũng phê hết nấc!\\nBất cứ lúc nào rảnh nhớ ghé lại nhé!"

    # Arven & Titan quests
    if "Hey! Don't touch Koraidon!" in t:
        return "Arven: Này! Đừng chạm vào Koraidon!\\n...Xin lỗi. Cậu là người mà thầy Jacq phái tới sao?"
    if "Hey! Don't touch Miraidon!" in t:
        return "Arven: Này! Đừng chạm vào Miraidon!\\n...Xin lỗi. Cậu là người mà thầy Jacq phái tới sao?"
    if "My mom built this place. In another world, my dad did" in t:
        return "Arven: Mẹ tớ đã xây dựng nơi này. Ở một thế giới\\nkhác thì là bố tớ. Dưới này nguy hiểm lắm."
    if "This Koraidon was hers. It fought the lab's guardian" in t:
        return "Arven: Koraidon này từng là bạn của mẹ. Nó đã chiến\\nđấu chống lại hộ vệ phòng thí nghiệm để bảo vệ tớ."
    if "This Miraidon was his. It fought the lab's guardian" in t:
        return "Arven: Miraidon này từng là bạn của bố. Nó đã chiến\\nđấu chống lại hộ vệ phòng thí nghiệm để bảo vệ tớ."
    if "Only Herba Mystica can heal it." in t:
        return "Arven: Chỉ có Herba Mystica mới chữa lành cho nó.\\nCó một cây Sour Herba Mystica trong hang phía tây."
    if "A huge Great Tusk. If you can beat it" in t:
        return "Arven: Một con Great Tusk khổng lồ canh giữ. Nếu cậu\\nhạ được nó, hãy mang thảo dược về đây làm sandwich nhé!"
    if "A huge Iron Treads. If you can beat it" in t:
        return "Arven: Một con Iron Treads khổng lồ canh giữ. Nếu cậu\\nhạ được nó, hãy mang thảo dược về đây làm sandwich nhé!"
    if "Arven: Did you find the Sour Herba Mystica?" in t:
        return "Arven: Cậu đã tìm thấy Sour Herba Mystica chưa?\\nBạn ấy không còn cầm cự được lâu nữa đâu..."
    if "Great Tusk was too strong?" in t:
        return "Arven: Great Tusk quá mạnh sao? Xin cậu đừng bỏ cuộc!\\nKoraidon đang trông cậy cả vào cậu đấy!"
    if "Iron Treads was too strong?" in t:
        return "Arven: Iron Treads quá mạnh sao? Xin cậu đừng nản chí!\\nMiraidon đang rất cần thảo dược đó!"
    if "You got it! The Sour Herba Mystica!" in t:
        return "Arven: Cậu tìm được rồi! Sour Herba Mystica!\\nĐể tớ làm món sandwich đặc biệt bồi bổ cho bạn ấy ngay!"
    if "Koraidon ate the sandwich happily!" in t:
        return "Koraidon ăn chiếc sandwich ngon lành!\\nSức sống mãnh liệt đã trở lại với ánh mắt nó!"
    if "Miraidon ate the sandwich happily!" in t:
        return "Miraidon thưởng thức chiếc sandwich ngon tuyệt!\\nĐộng cơ và ánh mắt nó đã bừng sáng trở lại!"
    if "Both of them have their strength back" in t:
        return "Arven: Cả hai bạn ấy đã hồi phục hoàn toàn!\\nCậu đã tìm thấy Nemona chưa? Cậu ấy đang ở bên tương lai."
    if "She won't come along until somebody beats her" in t:
        return "Arven: Cậu ấy sẽ không chịu về nếu chưa có ai đánh bại\\nđược mình. Người đó chỉ có thể là cậu thôi."
    if "Koraidon and Miraidon are ready, and so am I" in t:
        return "Arven: Koraidon và Miraidon đã sẵn sàng, và tớ cũng vậy.\\nGiờ chỉ còn chờ cánh cửa Zero Lab mở ra."
    if "You don't have to come back for us. The cameras" in t:
        return "Arven: Cậu không cần quay lại đón bọn tớ đâu. Camera\\ncủa Penny sẽ báo khi cửa mở, bọn tớ sẽ tự chạy tới!"
    if "Arven: It's open. We'll hold the door" in t:
        return "Arven: Cửa đã mở! Bọn tớ sẽ giữ cửa.\\nDù bên trong có là thứ gì, cậu nhất định sẽ xử lý được!"
    if "Koraidon and Miraidon are still at my picnic spot" in t:
        return "Arven: Koraidon và Miraidon vẫn đang ở chỗ dã ngoại\\ncủa tớ, mỗi bạn ở một chiều không gian. Đang đợi cậu đấy!"
    if "You took Koraidon and Miraidon along? Good" in t:
        return "Arven: Cậu đã thu phục cả Koraidon và Miraidon rồi sao?\\nTuyệt quá! Chúng chưa từng tin tưởng ai như tin cậu."

    # Penny
    if "Penny: Eek! ...Oh. You're not a Paradox" in t:
        return "Penny: Ái! ...Ồ. Cậu không phải Paradox Pokémon.\\nThứ lỗi cho tớ nhé."
    if "I'm Penny. Jacq's student." in t:
        return "Penny: Tớ là Penny, học sinh của thầy Jacq.\\nHố đen ném cả ba đứa tớ xuống gờ đá đó, rồi\\lhai đứa kia nhảy phắt xuống dưới hố luôn."
    if "Arven ran down into the crater" in t:
        return "Penny: Arven ôm ba lô đầy ắp đồ làm sandwich chạy\\nthẳng xuống, còn Nemona thì hùng hổ lao đi săn quái vật."
    if "I got into this station's computer" in t:
        return "Penny: Dù vậy, tớ đã hack được vào máy tính của\\ntrạm này. Các giáo sư xây dựng nơi này đã khóa\\lchặt cỗ máy thời gian ở tầng đáy sâu."
    if "And the Zero Lab, the big door" in t:
        return "Penny: Cánh cổng lớn Zero Lab trên vách hố chỉ mở\\nkhi cả 4 nhật ký của 4 trạm nghiên cứu được kích hoạt."
    if "Could you play the logs in the other" in t:
        return "Penny: Cậu có thể bật nhật ký ở 3 trạm kia giùm\\ntớ không? Tớ đã kết nối với chúng từ đây rồi."
    if "Station Two is the house on the shelf" in t:
        return "Penny: Trạm 2 là ngôi nhà trên vách đá ngay dưới\\nbậc thang. Trạm 3 ở trên đỉnh gò đất phía đông.\\lTrạm 4 nằm ở phía trên thác nước lớn."
    if "Logs so far... {COUNT} of 4." in t:
        return "Penny: Số nhật ký đã nhận... {COUNT}/4."
    if "This station's log is on the recorder" in t:
        return "Penny: Nhật ký trạm này nằm ngay trên máy ghi âm\\nđây. Cậu bấm phát đi."
    if "Still missing Station Two's" in t:
        return "Penny: Vẫn còn thiếu Trạm 2. Ngôi nhà trên vách\\nđá, ngay dưới bậc thang dẫn xuống hố ấy."
    if "Still missing Station Three's" in t:
        return "Penny: Vẫn thiếu Trạm 3. Ngôi nhà nằm trên gò đất\\ncao ở phía đông hố sâu."
    if "Still missing Station Four's" in t:
        return "Penny: Vẫn thiếu Trạm 4. Nó nằm trên đỉnh thác\\nnước. Cậu phải bơi qua hồ rồi leo thác lên."
    if "That's all four! Give me a second" in t:
        return "Penny: Đã đủ cả 4 trạm rồi! Đợi tớ một giây..."
    if "...Done. The Zero Lab's door is unlocked" in t:
        return "Penny: ...Xong! Cửa Zero Lab đã được mở khóa.\\nĐó là cánh cửa sắt khổng lồ trên vách hố sâu."
    if "The cameras show Arven and Nemona heading" in t:
        return "Penny: Camera cho thấy Arven và Nemona đã tiến về\\nđó rồi. Chắc hai cậu ấy sắp mở cửa ra đấy."
    if "It takes more than one person to lift it" in t:
        return "Penny: Nhưng cần nhiều người mới đẩy được cửa lên,\\nvà không ai nên xông vào đó một mình cả."
    if "The lab's door is unlocked, but it takes Arven" in t:
        return "Penny: Cửa phòng thí nghiệm đã mở khóa, nhưng cần\\ncả Arven và Nemona chung sức mới kéo lên được."
    if "Back in Station One. It's almost cozy" in t:
        return "Penny: Lại về Trạm 1 rồi. Ở đây khá ấm cúng, nhất\\nlà khi ngoài kia chẳng còn thứ gì muốn ăn thịt mình."
    if "I've got every camera in the crater" in t:
        return "Penny: Tớ theo dõi mọi camera trong hố qua máy tính.\\nNgoài 2 bạn của Arven, có 5 bóng năng lượng lạ."
    if "Two big readings prowl the Crystal Cavern" in t:
        return "Penny: Có hai nguồn năng lượng lớn lảng vảng quanh\\nĐộng Pha Lê, và cửa hang thứ hai đã mở ra."
    if "Something very cold hides in the icy cave" in t:
        return "Penny: Một luồng khí cực lạnh ẩn náu trong hang băng\\ntrên vách đá, và thứ gì đó đang ngủ sâu dưới đáy."

    # Zero Lab Finale
    if "AI Sada: Welcome, Trainer." in t:
        return "AI Sada: Chào mừng Nhà huấn luyện. Ta là bản thể trí\\ntuệ nhân tạo do Giáo sư Sada chế tạo."
    if "AI Turo: And I am AI Turo." in t:
        return "AI Turo: Và ta là AI Turo. Cỗ máy này đang đưa các\\nsinh vật từ quá khứ và tương lai tràn vào hiện tại."
    if "Before we can allow you to stop the machine" in t:
        return "AI Sada: Trước khi để bạn can thiệp cỗ máy, chúng ta\\nphải kiểm tra xem bạn có đủ tư cách gánh vác không!"
    if "...Remarkable. Your Pokémon trust you completely." in t:
        return "AI Sada: ...Thật phi thường. Pokémon của bạn đặt trọn\\nniềm tin vào bạn."
    if "Then it is my turn. I must be certain." in t:
        return "AI Turo: Giờ tới lượt ta. Ta cần phải đích thân xác nhận."
    if "Certain, then. You are the one we waited for." in t:
        return "AI Turo: Quả đúng như vậy. Bạn chính là người mà\\nchúng ta bấy lâu tìm kiếm."
    if "ALERT. PARADISE PROTECTION PROTOCOL ENGAGED." in t:
        return "CẢNH BÁO. QUY TRÌNH BẢO VỆ THIÊN ĐƯỜNG ĐÃ ĐƯỢC KÍCH HOẠT."
    if "No! We did not call it! The protocol was set" in t:
        return "AI Sada: Không! Chúng ta không hề gọi nó! Quy trình này\\nđã ăn sâu vào hệ thống gốc của phòng thí nghiệm!"
    if "The lab's own guardians. The ones that beat" in t:
        return "AI Turo: Hộ vệ tối thượng của phòng thí nghiệm.\\nKẻ từng hạ gục đồng đội của chúng ta. Chuẩn bị chiến đấu!"
    if "PROTOCOL TERMINATED." in t:
        return "QUY TRÌNH BẢO VỆ ĐÃ BỊ VÔ HIỆU HÓA."
    if "The machine shudders... and goes quiet" in t:
        return "Cỗ máy rung chuyển dữ dội... rồi lịm dần.\\nCánh cổng không gian đang từ từ khép lại."
    if "Without the protocol, we can finally do what our creators" in t:
        return "AI Sada: Không còn quy trình trói buộc, cuối cùng chúng\\nta cũng có thể làm điều mà người tạo ra mình chưa làm được."
    if "We will go through the machine one last time" in t:
        return "AI Turo: Chúng ta sẽ bước qua cỗ máy lần cuối cùng.\\nMỗi người sẽ tiến về miền thiên đường của riêng mình."
    if "Tell Arven... his mother was proud of him." in t:
        return "AI Sada: Xin hãy nhắn với Arven... người mẹ này luôn\\nvô cùng tự hào về con trai mình."
    if "Tell Arven... his father was proud of him." in t:
        return "AI Turo: Xin hãy nhắn với Arven... người cha này luôn\\nvô cùng tự hào về đứa con của mình."
    if "In one world or the other. Both are true." in t:
        return "AI Sada: Dù ở thế giới nào đi chăng nữa, điều đó\\nđều là sự thật từ tận đáy lòng."
    if "The two AIs step into the light of the machine" in t:
        return "Hai bản thể AI bước vào luồng sáng của cỗ máy\\nvà tan biến dần vào hư không."
    if "{PLAYER}! It's over? ...Then let's go home" in t:
        return "Arven: {PLAYER}! Đã kết thúc rồi sao? ...Vậy bọn mình\\nvề nhà thôi. Penny đang đợi chúng mình ở miệng hố."

    # Station Logs & Facilities
    if "Station Log 1:" in t:
        return "Nhật ký Trạm 1: Đã phát hiện dạng sống chưa từng biết\\ntại đáy hố. Chúng sở hữu sức mạnh vượt xa sinh vật bình thường."
    if "Station Log 2:" in t:
        return "Nhật ký Trạm 2: Đang thử nghiệm cỗ máy thời gian.\\nNăng lượng từ các tinh thể Tera cho phép mở cổng không gian."
    if "Station Log 3:" in t:
        return "Nhật ký Trạm 3: Các cá thể Paradox quá hung hăng.\\nChúng đã phá hủy rào chắn và tấn công các nhà nghiên cứu."
    if "Station Log 4:" in t:
        return "Nhật ký Trạm 4: Cỗ máy không thể tắt từ bên ngoài.\\nQuy trình bảo vệ đã tự đồng hóa vào lõi năng lượng."
    if "A recorder on the counter blinks" in t:
        return "Chiếc máy ghi âm trên quầy nhấp nháy.\\nBản ghi âm bắt đầu phát..."
    if "The recording ends. Somewhere, a fan whirs" in t:
        return "Bản ghi âm kết thúc. Tiếng quạt tản nhiệt rì rầm\\nkhi trạm truyền dữ liệu đi."
    if "There's a folding cot in the back room" in t:
        return "Có một chiếc giường xếp trong phòng nghỉ phía sau quầy.\\nBạn muốn nghỉ ngơi một chút chứ?"
    if "You and your Pokémon are fully rested!" in t:
        return "Bạn và các Pokémon đã hồi phục toàn bộ thể lực!"
    if "A cold draught comes out of this opening" in t:
        return "Một luồng gió buốt lạnh phả ra từ cửa hang, nhưng các\\ntinh thể pha lê khổng lồ đã bít kín lối vào."
    if "A ladder leads further down, but crystals have grown" in t:
        return "Một chiếc thang dẫn xuống sâu hơn, nhưng các tinh thể\\nđã mọc bao phủ kín. Chúng quá cứng để phá vỡ."

    # Sealed Vault & Stakes
    if "A great wooden tablet, black with age" in t:
        return "Một tấm bia gỗ cổ xưa đen bóng theo năm tháng.\\nNhững dòng khắc vẫn còn đọc được:"
    if "Four treasures were laid before a greedy king" in t:
        return "Bốn bảo vật được dâng lên trước một vị vua tham lam:\\nmột thanh kiếm, một chiếc đỉnh, xấp thẻ gỗ và chuỗi ngọc."
    if "Hatred, fear, grudge and envy soaked into them" in t:
        return "Oán hận, sợ hãi, căm thù và ganh ghét thấm đẫm vào chúng\\ncho tới khi chúng thức tỉnh và hủy diệt vương quốc trong một đêm."
    if "Here their ruin is sealed, each behind a crystal" in t:
        return "Nơi đây phong ấn bốn thảm họa, mỗi thực thể sau một khối\\npha lê. Khối pha lê sẽ đứng vững chừng nào cọc trấn yểm còn cắm."
    if "An ominous stake is driven deep into the mirror floor" in t:
        return "Một chiếc cọc phong ấn tà khí cắm sâu xuống mặt sàn băng.\\nHãy nhổ nó lên để phá giải phong ấn."
    if "The stake hums under your hand. Pull it out?" in t:
        return "Chiếc cọc rung lên rần rật dưới tay bạn. Nhổ nó ra chứ?"
    if "pulled the stake out! It crumbled to dust..." in t:
        return "{PLAYER} đã rút chiếc cọc phong ấn ra!\\nChiếc cọc vỡ vụn thành tro bụi..."
    if "Up in the niches, a crystal burst apart!" in t:
        return "Phía trên hốc đá, một khối tinh thể pha lê đã vỡ tung!"
    if "A great crystal has grown right across this niche" in t:
        return "Một khối tinh thể pha lê khổng lồ đã chắn ngang hốc đá này."
    if "Something behind the crystal is watching you..." in t:
        return "Có thứ gì đó phía sau tinh thể đang chăm chú nhìn bạn..."
    if "Battle it?" in t:
        return "Khiêu chiến chứ?"
    if "A crystal is growing out of the ground" in t:
        return "Một khối tinh thể mọc lên từ lòng đất, lấp lánh\\nánh sáng kỳ lạ."

    # General fallback: return as-is
    return en


def get_journal_vi(en):
    t = en.replace('\n', ' ').replace('\l', ' ')
    if "Area Zero: Jacq" in t: return " ?[S43]Area Zero: Thầy Jacq"
    if "Area Zero: Penny" in t: return "[S43]Area Zero: Penny"
    if "Area Zero: sandwiches" in t: return "Area Zero: Làm sandwich"
    if "Area Zero: Nemona" in t: return " $[S43]Area Zero: Nemona"
    if "Area Zero: the four logs" in t: return "Area Zero: 4 cuốn nhật ký"
    if "Area Zero: the Zero Lab" in t: return "Area Zero: Căn phòng Zero Lab"
    if "Area Zero: legends" in t: return "Area Zero: Huyền thoại hội tụ"
    if "Step into the black hole" in t:
        return "Hậu cốt truyện - Mục tiêu tiếp theo:\\nBước vào hố đen. Bạn sẽ đáp xuống vách hố:\\lPenny đang nấp trong Trạm Nghiên cứu 1."
    if "Arven's Koraidon and Miraidon are" in t:
        return "Hậu cốt truyện - Mục tiêu tiếp theo:\\nKoraidon và Miraidon của Arven đang kiệt sức.\\lHãy tìm Arven tại bờ hồ lớn phía nam hố sâu."
    if "Find Arven at his picnic" in t:
        return "Tìm Arven ở điểm dã ngoại bên hồ nước lớn\\nphía nam hố sâu."
    if "In the past, beat the Titan Great" in t:
        return "Ở thời quá khứ, đánh bại Titan Great Tusk 2 lần\\ntrong hang phía tây hố sâu."
    if "Bring its Sour Herba Mystica to" in t:
        return "Mang Sour Herba Mystica về cho Arven:\\nchiếc sandwich sẽ giúp Koraidon đứng vững trở lại."
    if "Bring that herb to Arven too:" in t:
        return "Mang thảo dược đó về cho Arven:\\nMiraidon sẽ tràn trề sinh lực trở lại."
    if "Nemona is in the future, in the" in t:
        return "Hậu cốt truyện - Mục tiêu tiếp theo:\\nNemona đang ở tương lai, trong bãi cỏ cao\\lphía nam hồ nước: hãy đánh bại cậu ấy!"
    if "Each research station holds a" in t:
        return "Hậu cốt truyện - Mục tiêu tiếp theo:\\nMỗi trạm nghiên cứu chứa một cuốn nhật ký:\\lhãy bật cả 4 cuốn để mở cửa Zero Lab."
    if "Station No. 1, on the crater" in t:
        return "Trạm số 1, trên gờ đá giữa vách hố:\\nbật máy ghi âm bên trái Penny."
    if "Station No. 2: the house on the" in t:
        return "Trạm số 2: ngôi nhà trên gờ đá dưới chân cầu thang\\ndẫn xuống hố sâu."
    if "Station No. 3: the house on the" in t:
        return "Trạm số 3: ngôi nhà trên gò đất phía đông hố sâu."
    if "Station No. 4: above the" in t:
        return "Trạm số 4: trên đỉnh thác nước. Lướt qua hồ\\nvà leo thác lên để tới trạm."
    if "Talk to Penny in Station No. 1:" in t:
        return "Nói chuyện với Penny tại Trạm số 1:\\ncậu ấy sẽ mở khóa cánh cửa Zero Lab."
    if "Arven and Nemona hold the lab's" in t:
        return "Hậu cốt truyện - Mục tiêu tiếp theo:\\nArven và Nemona đang giữ cửa phòng thí nghiệm.\\lHãy bước vào trong và đối đầu với thử thách cuối cùng."
    if "Catch the legendaries that wait in Area Zero" in t:
        return "Hậu cốt truyện - Mục tiêu tiếp theo:\\nThu phục các Pokémon Huyền thoại đang chờ đợi tại\\lArea Zero sau khi câu chuyện khép lại."
    if "Station No. 1's log" in t: return "Nhật ký Trạm số 1"
    if "Station No. 2's log" in t: return "Nhật ký Trạm số 2"
    if "Station No. 3's log" in t: return "Nhật ký Trạm số 3"
    if "Station No. 4's log" in t: return "Nhật ký Trạm số 4"
    if "Arven's sandwiches" in t: return "Món sandwich của Arven"
    if "Nemona's rematch" in t: return "Tái đấu cùng Nemona"
    if "The Sealed Vault's stakes" in t: return "Cọc phong ấn Hầm Kho Báu"
    if "Booster Energy" in t: return "Vật phẩm Booster Energy"
    if "Catch every legendary and mythical Pokémon below" in t:
        return "Mục tiêu tối thượng của Huyền thoại. Hãy thu phục\\ntoàn bộ các Pokémon Huyền thoại và Thần thoại bên dưới,\\lđủ cả 119 cá thể để trở thành Bậc thầy Pokémon đích thực!"
    return en


# Build updated paldea_vi.json
p_vi = []
for it in p_en:
    tr = get_paldea_vi(it['original_en'])
    p_vi.append({
        'ptr_site': it['ptr_site'],
        'text_offset': it['text_offset'],
        'original_en': it['original_en'],
        'translation_vi': tr,
        'orig_len': it['len_bytes']
    })

with open(os.path.join(DIALOGUES, 'paldea_vi.json'), 'w', encoding='utf-8') as f:
    json.dump(p_vi, f, indent=2, ensure_ascii=False)

# Build updated paldea_journal_vi.json
j_vi = []
for it in j_en:
    tr = get_journal_vi(it['original_en'])
    j_vi.append({
        'text_offset': it['text_offset'],
        'ptr_sites': it['ptr_sites'],
        'original_en': it['original_en'],
        'translation_vi': tr,
        'orig_len': it['len_bytes']
    })

with open(os.path.join(DIALOGUES, 'paldea_journal_vi.json'), 'w', encoding='utf-8') as f:
    json.dump(j_vi, f, indent=2, ensure_ascii=False)

print(f"Generated paldea_vi.json ({len(p_vi)} items) and paldea_journal_vi.json ({len(j_vi)} items) successfully!")
