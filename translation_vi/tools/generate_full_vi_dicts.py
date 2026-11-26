# -*- coding: utf-8 -*-
"""Generate 100% complete Vietnamese translations for Area Zero & Quest Log
in Pokemon Hyper Emerald 5.7 QoL v1.9.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
VI = os.path.dirname(HERE)
DIALOGUES = os.path.join(VI, 'dialogues')

p_en = json.load(open(os.path.join(DIALOGUES, 'paldea_en.json'), encoding='utf-8'))
j_en = json.load(open(os.path.join(DIALOGUES, 'paldea_journal_en.json'), encoding='utf-8'))

# Exact mapping dictionary for Paldea
PALDEA_MAP = {
    # Jacq Mossdeep
    "Jacq: Oh! A Trainer! Thank goodness...\\nSorry, sorry. My name's Jacq. I teach\\lbiology at the academy in Paldea.":
        "Jacq: Ồ! Một Huấn luyện viên! May quá...\\nXin lỗi nhé. Thầy tên là Jacq, dạy\\lSinh học ở Học viện tại vùng Paldea.",
    "Jacq: I brought three of my students\\nto Hoenn on a field study. Arven,\\lNemona and Penny. Good kids. Curious\\lkids.":
        "Jacq: Thầy dẫn 3 học sinh sang Hoenn\\nnghiên cứu thực địa: Arven, Nemona và\\lPenny. Mấy đứa trẻ ngoan và ham học hỏi.",
    "Jacq: The Space Center says this\\nopened the night the wormholes all\\lover Hoenn closed. Look at it. It isn't\\lan Ultra Wormhole.":
        "Jacq: Trung tâm Vũ trụ báo rằng hố này mở\\nngay đêm các Wormhole khắp Hoenn khép lại.\\lNhìn xem, đây không phải Ultra Wormhole.",
    "Jacq: The kids went to take a closer\\nlook, and it pulled them in. All three of\\lthem.":
        "Jacq: Mấy đứa nhóc tò mò lại gần xem,\\nvà hố đen đã hút sạch cả ba đứa vào trong.",
    "Jacq: I went in after them... and ran\\nstraight back out, chased by a Pokémon\\lI had only ever seen drawn in a book\\ltwo hundred years old.":
        "Jacq: Thầy lao vào cứu... rồi phải chạy bán sống\\nbán chết ra ngoài vì bị một Pokémon mà thầy\\lchỉ từng thấy trong sách cổ 200 năm trước đuổi.",
    "Jacq: I know that place. It's the Great\\nCrater of Paldea. Area Zero. Nobody is\\lallowed down there, and my students\\lare down there right now.":
        "Jacq: Thầy biết nơi ấy. Đó là Đại Hố sâu của\\nPaldea — Area Zero. Cấm tuyệt đối vào đó,\\nvậy mà học sinh của thầy lại đang kẹt dưới kia.",
    "Jacq: Your Pokémon look like they could\\nhandle anything. Please... would you go\\lin and bring them back? I'll wait right\\lhere.":
        "Jacq: Pokémon của em trông rất dũng mãnh.\\nXin em... hãy vào đó đưa các bạn ấy trở về\\lđược không? Thầy sẽ túc trực ở đây.",
    "Jacq: You! The Trainer from before!\\nThank goodness... It's me, Jacq. The\\lteacher with the three students.":
        "Jacq: Em! Nhà huấn luyện lúc trước! May quá...\\nLà thầy đây, Jacq, giáo viên dẫn 3 học sinh\\lđi thực địa.",
    "Jacq: The restless sky, remember? The\\nSpace Center says this opened the\\lnight the wormholes all over Hoenn\\lclosed. Look at it. It isn't an Ultra\\lWormhole.":
        "Jacq: Bầu trời chao đảo lúc trước, em nhớ chứ?\\nTrung tâm Vũ trụ báo cái hố này mở ra ngay\\nđêm các Wormhole khắp Hoenn đóng lại. Nhìn\\lxem, đây không phải Ultra Wormhole.",
    "Jacq: Arven, Nemona and Penny are\\nsomewhere on the other side. Please,\\lbring them home!":
        "Jacq: Arven, Nemona và Penny đang ở phía\\nbên kia hố đen. Xin em, hãy đưa các bạn\\lấy về an toàn nhé!",
    "Jacq: Oh, hello! A Trainer? My name's\\nJacq. I teach biology at the academy in\\lPaldea. That's a long, long way from\\lhere.":
        "Jacq: Ồ, chào em! Nhà huấn luyện sao?\\nThầy tên là Jacq, dạy môn Sinh học tại Học viện\\nở Paldea. Nơi đó cách đây xa lắm.",
    "Jacq: I've brought three of my\\nstudents to Hoenn on a field study.\\lArven, Nemona and Penny. Good kids.\\lCurious kids. They're off around the\\lisland somewhere.":
        "Jacq: Thầy dẫn 3 học sinh sang Hoenn nghiên cứu\\nthực địa: Arven, Nemona và Penny. Mấy đứa\\ltrẻ tò mò lắm, đang dạo quanh đảo rồi.",
    "Jacq: We came for the sky. The Space\\nCenter says the air over this shore\\lhas been restless lately. As if\\lsomething were pressing on it from the\\lother side.":
        "Jacq: Thầy trò tới vì hiện tượng lạ trên trời.\\nTrung tâm Vũ trụ nói vùng trời bờ biển này dạo\\ngần đây chao đảo, như thể có thứ gì đó đang\\lđè nén từ thế giới bên kia.",
    "Jacq: It's probably nothing! Still, I\\ntold the kids not to wander too far.\\l...Not that they ever listen.":
        "Jacq: Chắc không có gì đâu! Dù vậy thầy vẫn dặn\\nmấy đứa không được đi xa... Cơ mà chúng nó\\lcó bao giờ chịu nghe đâu.",
    "Jacq: Still nothing in the sky. Good! A\\nquiet field trip is a good field trip. ...I\\lkeep telling myself that.":
        "Jacq: Bầu trời vẫn chưa có gì lạ. Tốt lắm!\\nMột chuyến đi bình yên luôn là tuyệt nhất...\\lThầy vẫn tự nhủ lòng như vậy.",
    "A perfectly black hole hangs in the air\\nabove the grass. Something on the\\lother side is pulling at you...":
        "Một hố đen sâu thẳm lơ lửng giữa không trung\\ntrên thảm cỏ. Có một luồng lực bí ẩn từ phía\\lbên kia đang lôi kéo bạn...",
    "Jacq: Whoa, whoa! Don't go near that!":
        "Jacq: Khoan, khoan đã! Đừng lại gần cái hố đó!",
    "The black hole is pulling at you. Step\\ninto it?":
        "Hố đen đang hút lấy bạn. Bước vào trong chứ?",
    "Through the hole, you can faintly hear\\nthe sea at Mossdeep. Go back?":
        "Qua miệng hố, bạn có thể nghe văng vẳng tiếng\\nsóng biển Mossdeep. Quay trở về chứ?",
    "The hole lets go of you on a narrow\\nledge, high on a cliff. Far below, a\\lforest fills the bottom of a vast\\lcrater.":
        "Hố đen nhả bạn xuống một gờ đá hẹp cheo leo trên\\nvách núi. Xa tít phía dưới, cả cánh rừng bạt ngàn\\nbao phủ đáy miệng hố khổng lồ.",
    "This must be Area Zero...":
        "Nơi này hẳn chính là Area Zero...",

    # Ending dialogues at Mossdeep
    "Jacq: You're back! And you brought\\neveryone! Arven, Nemona, Penny... Thank\\lgoodness.":
        "Jacq: Em đã về rồi! Và đưa được tất cả mọi người\\nra ngoài! Arven, Nemona, Penny... Cảm tạ trời đất.",
    "Arven: My parents' AIs went through\\nthe machine. I think... they finally got\\lto choose.":
        "Arven: Các bản thể AI của bố mẹ tớ đã bước qua\\ncỗ máy thời gian. Tớ nghĩ... cuối cùng họ cũng\\lđược tự do chọn con đường của mình.",
    "Nemona: That was the best adventure\\never! [BUF01], you have to battle me\\lagain sometime!":
        "Nemona: Đây quả là chuyến phiêu lưu tuyệt nhất\\ntừ trước tới nay! [BUF01], nhất định cậu\\lphải đấu với tớ một trận nữa đấy nhé!",
    "Jacq: [BUF01], I can't thank you\\nenough. Please, take this.":
        "Jacq: [BUF01], thầy không biết lấy gì để cảm ơn\\nem cho hết. Xin hãy nhận lấy món quà này.",
    "Arven: Oh, and... Koraidon and Miraidon\\nstayed behind at my picnic spot. I\\lthink they're waiting for you.":
        "Arven: À này... Koraidon và Miraidon vẫn đang nán\\nlại ở chỗ dã ngoại của tớ. Tớ nghĩ là hai bạn\\lấy đang đợi cậu đấy.",
    "Jacq: With that machine stopped, the\\ncrater is finally safe to study. A\\lbiology teacher doesn't get a chance\\llike this twice.":
        "Jacq: Khi cỗ máy thời gian dừng lại, cuối cùng\\nchúng ta cũng có thể an tâm nghiên cứu hố sâu.\\lMột giáo viên Sinh học cả đời khó gặp cơ hội này.",
    "Penny: I'm never going near a black\\nhole again. ...Okay. Maybe once more.":
        "Penny: Tớ thề sẽ không bao giờ lại gần hố đen\\nnữa... Cơ mà thôi được, có lẽ chỉ thêm một lần.",
    "Jacq: We're going back in to finish\\nour field trip properly. You'll find us\\lin the research stations.":
        "Jacq: Thầy trò thầy sẽ quay lại để hoàn tất\\nchuyến thực địa. Em có thể tìm thấy chúng thầy\\ltrong các trạm nghiên cứu nhé!",
    "Jacq and his students stepped back into\\nthe hole.":
        "Thầy Jacq và các học sinh đã bước trở lại vào hố đen.",

    # Lab door shutter
    "A huge metal shutter is set into the\\ncrater wall. A panel beside it reads:\\lSTATION LOGS RECEIVED: {COUNT} OF 4.":
        "Một cánh cửa cuốn kim loại khổng lồ gắn chặt vào\\nvách hố. Bảng điều khiển ghi: NHẬT KÝ TRẠM ĐÃ NHẬN: {COUNT}/4.",
    "The panel beside the shutter reads:\\nSTATION LOGS RECEIVED: 4 OF 4.\\lUNLOCKED.":
        "Bảng điều khiển cạnh cửa hiển thị: ĐÃ NHẬN ĐỦ 4/4\\nNHẬT KÝ TRẠM. ĐÃ MỞ KHÓA.",
    "But the shutter is far too heavy to\\nlift alone, and Arven and Nemona\\laren't at the door yet...":
        "Nhưng cánh cửa quá nặng để nâng một mình, và Arven\\ncùng Nemona vẫn chưa đến đây...",
    "Koraidon is still too weak to move.\\nArven needs the herb the Titan guards,\\lin the den on the west side of the\\lcrater, in the past.":
        "Koraidon vẫn còn quá yếu để cử động.\\nArven cần thảo dược do Titan canh giữ\\ntrong hang phía tây hố sâu thời quá khứ.",
    "Miraidon is still too weak to move.\\nArven needs the herb the Titan guards,\\lin the den on the west side of the\\lcrater, in the future.":
        "Miraidon vẫn còn quá yếu để cử động.\\nArven cần thảo dược do Titan canh giữ\\ntrong hang phía tây hố sâu thời tương lai.",
    "Nemona is still battling in the future,\\nin the tall grass south of the\\lwaterfall's pond.":
        "Nemona vẫn đang mải mê chiến đấu ở tương lai,\\ntrong bãi cỏ cao phía nam hồ nước.",
    "The machine is silent. The display\\nreads: TIME MACHINE. GATE: CLOSED.":
        "Cỗ máy im lìm. Màn hình hiển thị: CỖ MÁY THỜI GIAN.\\nCỔNG: ĐÃ ĐÓNG.",
    "Behind thick glass, an enormous\\nmachine hums. The display reads: TIME\\lMACHINE. GATE: OPEN.":
        "Sau lớp kính dày, cỗ máy khổng lồ gầm rú. Màn hình\\nhiển thị: CỖ MÁY THỜI GIAN. CỔNG: ĐANG MỞ.",
    "Something in there is watching. This is\\nno place to be alone, and Arven and\\lNemona aren't at the door yet...":
        "Có thứ gì đó bên trong đang theo dõi. Nơi này không\\nthể vào một mình, và Arven cùng Nemona vẫn chưa tới...",

    # Time rifts
    "Through the rift, the crater is cold\\nand violet, and something made of\\lmetal moves between the trees. Step\\lthrough?":
        "Qua vết rách, hố sâu mang sắc tím lạnh lẽo, và có\\nthứ gì đó bằng kim loại đang chuyển động. Bước qua chứ?",
    "Through the rift, the crater is warm\\nand wild, and something huge and\\lancient moves between the trees. Step\\lthrough?":
        "Qua vết rách, hố sâu ấm áp hoang sơ, và có thứ gì\\nđó khổng lồ từ cổ đại đang di chuyển. Bước qua chứ?",
    "A tear hangs in the air, shimmering.\\nThrough it you can see this same\\lcrater... in another time.":
        "Một vết rách không gian lơ lửng, lấp lánh ánh sáng.\\nQua đó, bạn có thể nhìn thấy chính hố sâu này ở thời đại khác...",

    # Nemona
    "Nemona: Go, go, go! We'll keep the\\nParadox Pokémon off your back!":
        "Nemona: Tiến lên, tiến lên! Bọn tớ sẽ chặn đứng\\nlũ Paradox Pokémon không để chúng quấy rầy cậu!",
    "Nemona: Haha! Another one down! Who's\\nnext?":
        "Nemona: Haha! Lại hạ thêm một con nữa! Đứa nào tiếp theo?",
    "Nemona: Wait, you're not a Paradox\\nPokémon! You're a Trainer! Great,\\lbattle me!":
        "Nemona: Khoan đã, cậu không phải Paradox Pokémon!\\nCậu là nhà huấn luyện! Tuyệt vời, đấu với tớ một trận đi!",
    "Nemona: Okay, okay, I'll stop battling\\nthe Paradox Pokémon. For now.":
        "Nemona: Rồi rồi, tớ sẽ tạm ngừng đấm nhau với bầy\\nParadox Pokémon... Chỉ tạm thời thôi đấy nhé!",
    "Nemona: Arven's by the lake, making\\nsandwiches for Koraidon and Miraidon.\\lOnce they're both well and Penny has\\lthe lab's door unlocked, he and I will\\lget it open for you!":
        "Nemona: Arven đang ở bờ hồ làm sandwich cho Koraidon\\nvà Miraidon. Đợi hai bạn ấy khỏe lại và Penny mở khóa\\lcửa phòng thí nghiệm, bọn tớ sẽ mở toang cửa cho cậu!",
    "Nemona: Arven's ready, and Penny\\nunlocked the lab? Then what are we\\lwaiting for! It's the big shutter in the\\lnorth-east wall. Arven and I will get it\\lopen!":
        "Nemona: Arven đã sẵn sàng và Penny mở khóa phòng thí\\nnghiệm rồi ư? Vậy còn chờ gì nữa! Cánh cửa lớn trên vách\\nđá đông bắc, Arven và tớ sẽ kéo nó lên!",
    "Nemona: We'll battle again when we're\\nout of here. Promise!":
        "Nemona: Chúng mình sẽ tái đấu khi ra khỏi đây nhé.\\nHứa đấy!",
    "Nemona: [BUF01]! Perfect timing! I've\\nbeen thinking up new strategies all\\lday. Battle me?":
        "Nemona: [BUF01]! Chuẩn thời điểm luôn! Tớ vừa nghĩ ra\\nbao nhiêu chiến thuật mới cả ngày nay. Đấu một trận chứ?",
    "Nemona: Aww. I'll be right here when you\\nchange your mind!":
        "Nemona: Tiếc thế. Khi nào đổi ý cứ quay lại đây\\ntìm tớ bất cứ lúc nào nhé!",
    "Nemona: Hah! That never gets old. Come\\nback any time!":
        "Nemona: Hah! Đấu với cậu lúc nào cũng phê hết nấc!\\nBất cứ lúc nào rảnh nhớ ghé lại nhé!",

    # Arven & Titan quests
    "Arven: Hey! Don't touch Koraidon!\\n...Sorry. You're the one Jacq sent,\\naren't you?":
        "Arven: Này! Đừng chạm vào Koraidon!\\n...Xin lỗi. Cậu là người mà thầy Jacq phái tới sao?",
    "Arven: Hey! Don't touch Miraidon!\\n...Sorry. You're the one Jacq sent,\\naren't you?":
        "Arven: Này! Đừng chạm vào Miraidon!\\n...Xin lỗi. Cậu là người mà thầy Jacq phái tới sao?",
    "Arven: My mom built this place. In\\nanother world, my dad did. Down here,\\lboth of those are true at once.":
        "Arven: Mẹ tớ đã xây dựng nơi này. Ở một thế giới\\nkhác thì là bố tớ. Dưới này, cả hai điều đó đều có thật.",
    "Arven: My dad built this place. In\\nanother world, my mom did. Down here,\\lboth of those are true at once.":
        "Arven: Bố tớ đã xây dựng nơi này. Ở một thế giới\\nkhác thì là mẹ tớ. Dưới này, cả hai điều đó đều có thật.",
    "Arven: This Koraidon was hers. It\\nfought the lab's guardian to protect\\lme, and it has hardly moved since.":
        "Arven: Koraidon này từng là bạn của mẹ. Nó đã chiến\\nđấu chống lại hộ vệ phòng thí nghiệm để bảo vệ tớ,\\nvà từ đó tới giờ nó gần như không gượng dậy nổi.",
    "Arven: This Miraidon was his. It fought\\nthe lab's guardian to protect me, and\\lit has hardly moved since.":
        "Arven: Miraidon này từng là bạn của bố. Nó đã chiến\\nđấu chống lại hộ vệ phòng thí nghiệm để bảo vệ tớ,\\nvà từ đó tới giờ nó gần như không gượng dậy nổi.",
    "Arven: Only Herba Mystica can heal it.\\nThere's a Sour Herba Mystica in the\\lden on the west side, but a Titan is\\lguarding it.":
        "Arven: Chỉ có Herba Mystica mới chữa lành cho nó.\\nCó một cây Sour Herba Mystica trong hang phía tây,\\nnhưng một con Titan đang canh giữ nó.",
    "Arven: A huge Great Tusk. If you can\\nbeat it, bring the herb back, and I'll\\lmake Koraidon the best sandwich of its\\llife.":
        "Arven: Một con Great Tusk khổng lồ. Nếu cậu đánh bại\\nđược nó, hãy mang thảo dược về đây làm chiếc sandwich ngon nhất!",
    "Arven: A strange iron Donphan. Iron\\nTreads. If you can beat it, bring the\\lherb back, and I'll make Miraidon the\\lbest sandwich of its life.":
        "Arven: Một cỗ máy Donphan kỳ lạ, Iron Treads. Nếu cậu\\nhạ được nó, hãy mang thảo dược về để tớ làm sandwich cho Miraidon!",
    "Arven: The Titan's in the den on the\\nwest side. Great Tusk. Be careful.":
        "Arven: Con Titan đang ở trong hang phía tây. Là Great\\nTusk đấy. Hãy hết sức cẩn thận!",
    "Arven: The Titan's in the den on the\\nwest side. Iron Treads. Be careful.":
        "Arven: Con Titan đang ở trong hang phía tây. Là Iron\\nTreads đấy. Hãy hết sức cẩn thận!",
    "Arven: Did you find the Sour Herba\\nMystica?":
        "Arven: Cậu đã tìm thấy Sour Herba Mystica chưa?",
    "Arven: Great Tusk was too strong? It's\\nokay. Don't give up.":
        "Arven: Great Tusk quá mạnh sao? Không sao đâu. Xin cậu đừng từ bỏ!",
    "Arven: Iron Treads was too strong? It's\\nokay. Don't give up.":
        "Arven: Iron Treads quá mạnh sao? Không sao đâu. Xin cậu đừng nản chí!",
    "Arven: You got the Sour Herba Mystica!\\nOkay. Okay! Give me a minute.":
        "Arven: Cậu tìm được Sour Herba Mystica rồi! Được rồi,\\nđợi tớ một phút nhé!",
    "Arven made a sandwich stacked high\\nwith Sour Herba Mystica!":
        "Arven đã kẹp một chiếc sandwich ngập tràn Sour Herba Mystica!",
    "Koraidon is eating the sandwich...":
        "Koraidon đang thưởng thức chiếc sandwich...",
    "Miraidon is eating the sandwich...":
        "Miraidon đang thưởng thức chiếc sandwich...",
    "Koraidon got its strength back!":
        "Koraidon đã hồi phục toàn bộ thể lực và sức sống!",
    "Miraidon got its strength back!":
        "Miraidon đã hồi sinh toàn bộ động cơ và năng lượng!",
    "Arven: Look at that... Thank you.\\nReally. Mom would have liked you.":
        "Arven: Nhìn kìa... Cảm ơn cậu thật nhiều.\\nMẹ tớ ở trên trời nhất định sẽ rất quý mến cậu.",
    "Arven: Look at that... Thank you.\\nReally. Dad would have liked you.":
        "Arven: Nhìn kìa... Cảm ơn cậu thật nhiều.\\nBố tớ ở trên trời nhất định sẽ rất quý mến cậu.",
    "Arven: Everyone's ready. Then let's\\nfinish this. The Zero Lab is behind the\\lbig shutter in the north-east wall.":
        "Arven: Mọi người đã sẵn sàng rồi. Hãy kết thúc chuyện\\nnày thôi. Zero Lab nằm sau cánh cửa cuốn lớn trên vách đông bắc.",
    "Arven: Nemona and I will get it open and\\nhold it. Whatever is inside... it's my\\lparents' work. I'd rather you faced it\\lthan nobody.":
        "Arven: Nemona và tớ sẽ kéo và giữ cửa. Dù bên trong có\\nlà thứ gì... đó cũng là công trình của bố mẹ tớ.\\nTớ tin tưởng giao phó cho cậu hơn bất kỳ ai.",
    "Arven: Miraidon is still too weak to\\nmove, in the other time. There's a Titan\\lguarding a herb there too. The rifts in\\lthe air will take you.":
        "Arven: Miraidon vẫn còn quá yếu để cử động ở thời đại kia.\\nBên đó cũng có một Titan canh giữ thảo dược. Vết rách không gian sẽ dẫn cậu sang.",
    "Arven: Koraidon is still too weak to\\nmove, in the other time. There's a Titan\\lguarding a herb there too. The rifts in\\lthe air will take you.":
        "Arven: Koraidon vẫn còn quá yếu để cử động ở thời đại kia.\\nBên đó cũng có một Titan canh giữ thảo dược. Vết rách không gian sẽ dẫn cậu sang.",
    "Arven: Both of them have their\\nstrength back. Have you found Nemona?\\lShe's in the future, in the tall grass\\lsouth of the waterfall's pond, battling\\leverything that moves.":
        "Arven: Cả hai bạn ấy đã hồi phục sức mạnh! Cậu đã tìm\\nthấy Nemona chưa? Cậu ấy đang ở tương lai, trong bãi cỏ\\lcao nam hồ nước, đánh nhau với mọi thứ nhúc nhích.",
    "Arven: She won't come along until\\nsomebody beats her. That had better\\lbe you.":
        "Arven: Cậu ấy sẽ không chịu về nếu chưa có ai đánh bại\\nđược mình. Người đó chỉ có thể là cậu thôi.",
    "Arven: Koraidon and Miraidon are ready,\\nand so am I. All that's left is the lab's\\ldoor. Penny can unlock it from Station\\lOne, but she needs the logs from all\\lfour research stations.":
        "Arven: Koraidon và Miraidon đã sẵn sàng, và tớ cũng vậy.\\nGiờ chỉ còn cánh cửa phòng thí nghiệm. Penny có thể mở khóa\\ntừ Trạm 1, nhưng cần đủ 4 nhật ký từ 4 trạm.",
    "Arven: You don't have to come back for\\nus. The moment it unlocks, Nemona and I\\lwill be there to haul it open.":
        "Arven: Cậu không cần quay lại đón bọn tớ đâu. Giây phút\\ncửa mở khóa, Nemona và tớ sẽ có mặt để kéo nó lên!",
    "Koraidon barely lifts its head. It's\\nbreathing slowly, too weak to take a\\lstep.":
        "Koraidon hầu như không ngẩng nổi đầu lên.\\nNó thở dốc yếu ớt, không thể bước nổi một bước.",
    "Miraidon barely lifts its head. It's\\nbreathing slowly, too weak to take a\\lstep.":
        "Miraidon hầu như không ngẩng nổi đầu lên.\\nNó thở dốc yếu ớt, không thể bước nổi một bước.",
    "Koraidon is full of energy. It keeps\\nlooking toward the lab.":
        "Koraidon tràn trề năng lượng. Nó liên tục nhìn về hướng phòng thí nghiệm.",
    "Miraidon is full of energy. It keeps\\nlooking toward the lab.":
        "Miraidon tràn trề năng lượng. Nó liên tục nhìn về hướng phòng thí nghiệm.",
    "Koraidon is still waiting by the picnic.":
        "Koraidon vẫn đang kiên nhẫn đợi bên điểm dã ngoại.",
    "Miraidon is still waiting by the picnic.":
        "Miraidon vẫn đang kiên nhẫn đợi bên điểm dã ngoại.",
    "A gigantic Great Tusk blocks the way!\\nIt's standing guard over something...":
        "Một con Great Tusk khổng lồ chắn ngang đường!\\nNó đang đứng canh giữ thứ gì đó...",
    "A gigantic Iron Treads blocks the way!\\nIt's standing guard over something...":
        "Một con Iron Treads khổng lồ chắn ngang đường!\\nNó đang đứng canh giữ thứ gì đó...",
    "The Titan's engine is roaring. Battle\\nit?":
        "Động cơ của con Titan gầm rú vang dội. Khiêu chiến chứ?",
    "Great Tusk staggers... It's digging\\nsomething out of the ground!":
        "Great Tusk loạng choạng... Nó đang đào thứ gì đó lên từ lòng đất!",
    "Iron Treads screeches to a stop... It's\\ndigging something out of the ground!":
        "Iron Treads rít phanh chói tai... Nó đang bới thứ gì đó dưới đất lên!",
    "Great Tusk ate a Sour Herba Mystica!\\nIt's growing even bigger!":
        "Great Tusk đã nuốt chửng Sour Herba Mystica!\\nThân hình nó đang phình to dữ dội hơn nữa!",
    "Iron Treads ate a Sour Herba Mystica!\\nIt's growing even bigger!":
        "Iron Treads đã ngốn nghiến Sour Herba Mystica!\\nThân hình nó đang phình to dữ dội hơn nữa!",
    "Great Tusk turned tail and ran!":
        "Great Tusk cúp đuôi tháo chạy thục mạng!",
    "Iron Treads rolled away at full speed!":
        "Iron Treads cuộn tròn phóng đi với tốc độ xé gió!",
    "There's something left on the ground...":
        "Có thứ gì đó rơi lại trên mặt đất...",
    "[BUF01] found a Sour Herba Mystica!":
        "[BUF01] đã tìm thấy một nhánh Sour Herba Mystica!",
    "Better take it to Arven, at the picnic\\nby the lake.":
        "Nên mang thứ này về cho Arven tại điểm dã ngoại bên hồ nước.",
    "Great Tusk is still standing guard...":
        "Great Tusk vẫn đứng sừng sững canh gác...",
    "Iron Treads is still standing guard...":
        "Iron Treads vẫn đứng sừng sững canh gác...",

    # Wild Paradox appearances
    "A Pokémon like Suicune, but ancient\\nand wild, rises from the water!":
        "Một Pokémon giống Suicune, nhưng cổ xưa và hoang dã, vươn mình trỗi dậy từ mặt nước!",
    "A Pokémon like Entei, but ancient and\\nwild, blocks the way!":
        "Một Pokémon giống Entei, nhưng cổ xưa và hoang sơ, sừng sững chặn lối đi!",
    "A Pokémon like Raikou, but ancient and\\nwild, crackles with lightning!":
        "Một Pokémon giống Raikou, nhưng cổ xưa và hoang sơ, đang phóng ra sấm sét chói lòa!",
    "A Pokémon like Virizion, but made of\\nmetal, stands among the trees!":
        "Một Pokémon giống Virizion, nhưng đúc bằng kim loại, đứng lặng lẽ giữa rặng cây!",
    "A Pokémon like Terrakion, but made of\\nmetal, lowers its blade!":
        "Một Pokémon giống Terrakion, nhưng đúc bằng kim loại, hạ lưỡi gươm xuống nghênh chiến!",
    "A Pokémon like Cobalion, but made of\\nmetal, is watching you!":
        "Một Pokémon giống Cobalion, nhưng đúc bằng kim loại, đang lạnh lùng dõi theo bạn!",
    "A dark winged Pokémon is hiding among\\nthe crystals!":
        "Một Pokémon sải cánh đen tối đang ẩn nấp giữa các tinh thể pha lê!",
    "A Pokémon of metal and light stands\\nguard among the crystals!":
        "Một Pokémon làm bằng kim loại và ánh sáng đứng canh gác giữa rừng pha lê!",
    "A Pokémon wound in wooden tablets\\nuncoils in its niche!":
        "Một Pokémon quấn quanh bởi những thẻ gỗ cổ xưa đang cựa mình trong hốc đá!",
    "A Pokémon with fangs like broken\\nswords crouches on the ice!":
        "Một Pokémon với cặp nanh sắc nhọn như gươm gãy đang nép mình rình mồi trên băng!",
    "A huge Pokémon with a bronze vessel on\\nits head shakes the vault!":
        "Một Pokémon khổng lồ đội đỉnh đồng trên đầu đang làm rung chuyển cả hầm kho báu!",
    "A small Pokémon swims through the air,\\nblazing beads all round it!":
        "Một Pokémon nhỏ bơi lượn giữa không trung, vây quanh bởi chuỗi ngọc rực lửa!",
    "Something sleeps here, shining with\\nevery color at once...":
        "Có thứ gì đó đang say ngủ tại đây, tỏa ra muôn ngàn sắc màu rực rỡ...",

    # Station logs & notes
    "Professor Sada: Station One, day\\nthree. The crater floor is a world of\\lits own. Tonight something with huge\\ltusks walked past the station. It was\\lnot a Donphan.":
        "Giáo sư Sada: Trạm 1, ngày thứ ba. Đáy hố sâu là một\\nthế giới hoàn toàn tách biệt. Đêm nay, một sinh vật có cặp\\nngà khổng lồ đã đi qua trạm. Nó không phải Donphan.",
    "Professor Turo: Nothing alive today\\nmatches these readings. If the rifts\\ldown here open onto time the way I\\lthink they do... we can build a machine\\lthat reaches it.":
        "Giáo sư Turo: Không sinh vật sống nào ngày nay khớp với chỉ số\\nnày. Nếu các vết rách mở ra thời gian đúng như ta nghĩ...\\nchúng ta có thể chế tạo cỗ máy chạm tới nó.",
    "The recording ends. Somewhere, a fan\\nwhirs as the station sends it on.":
        "Bản ghi âm kết thúc. Tiếng quạt tản nhiệt rì rầm khi trạm truyền dữ liệu đi.",
    "A tablet covered in Eevee stickers lies\\non the table. It's still warm...":
        "Một chiếc máy tính bảng dán đầy hình Eevee đặt trên bàn. Nó vẫn còn ấm...",
    "Someone was here not long ago.":
        "Có ai đó vừa mới ở đây cách đây không lâu.",
    "Professor Turo: Station Two. The\\nmachine works. We brought back a\\lPokémon from the far future, a machine\\lshaped like Donphan.":
        "Giáo sư Turo: Trạm 2. Cỗ máy đã hoạt động. Chúng ta đã mang\\nvề một Pokémon từ tương lai xa, một cỗ máy mang hình dáng Donphan.",
    "Professor Sada: And I brought one from\\nthe distant past. They are perfect.\\lBut they don't belong here... and the\\lgate does not close behind them.":
        "Giáo sư Sada: Và tôi đã đưa về một cá thể từ quá khứ xa xôi.\\nChúng thật hoàn hảo, nhưng không thuộc về nơi này...\\nvà cánh cổng không chịu khép lại phía sau chúng.",
    "A huge backpack leans against the\\ntable, stuffed with bread, vegetables\\land a jar marked “Sour Herba Mystica”.\\lIt's empty.":
        "Một chiếc ba lô to đùng tựa vào bàn, nhồi nhét bánh mì, rau củ\\nvà một chiếc lọ đề chữ “Sour Herba Mystica”. Lọ đã rỗng.",
    "Somebody came here to make\\nsandwiches.":
        "Có ai đó đã vào đây để làm bánh mì sandwich.",
    "Professor Sada: Station Three. Our\\npartners fought today. My Koraidon\\land Turo's Miraidon. Neither would back\\ldown.":
        "Giáo sư Sada: Trạm 3. Hai người bạn đồng hành của chúng tôi đã\\nđánh nhau hôm nay. Koraidon của tôi và Miraidon của Turo. Không bên nào chịu nhượng bộ.",
    "Professor Turo: The lab's two\\nguardians won't let anything near the\\lmachine. Ours were beaten badly. Our\\lson is looking after them now.":
        "Giáo sư Turo: Hai hộ vệ của phòng thí nghiệm không để bất cứ thứ\\ngì tới gần cỗ máy. Đồng đội của chúng tôi bị thương nặng.\\nCon trai chúng tôi đang chăm sóc chúng.",
    "A crayon drawing is pinned to the\\ntable: a woman, a man, a boy and two big\\llizards. It's signed “Arven, age 6”.":
        "Một bức tranh vẽ bằng sáp màu ghim trên bàn: một người phụ nữ,\\nmột người đàn ông, một cậu bé và hai con thằn lằn lớn. Đề tên: “Arven, 6 tuổi”.",
    "Professor Turo: Station Four. Last log.\\nWe are going to make copies of\\lourselves, an AI each, to run the lab\\lwhile we are... away.":
        "Giáo sư Turo: Trạm 4. Bản ghi cuối cùng. Chúng tôi sẽ tạo ra\\nbản sao của chính mình, mỗi người một bản thể AI, để điều hành phòng thí nghiệm khi vắng mặt.",
    "Professor Sada: If anyone finds this:\\nthe lab only opens to someone who has\\lheard all four of these. Please. Stop\\lthe machine. We could not.":
        "Giáo sư Sada: Nếu ai tìm thấy bản ghi này: phòng thí nghiệm chỉ mở\\ncho người đã nghe đủ cả 4 cuốn nhật ký. Xin hãy dừng cỗ máy lại.\\nChúng tôi đã không thể làm được điều đó.",
    "A battered field guide lies open on the\\ntable. Every page about the crater's\\lTitans is full of notes.":
        "Một cuốn sổ tay dã ngoại sờn rách mở sẵn trên bàn. Từng trang viết\\nvề các Titan trong miệng hố đều kín đặc ghi chú.",

    # Penny station dialogues
    "Penny: I got into this station's\\ncomputer, though. The professors who\\lbuilt this place left a log in every\\lresearch station. Four stations, four\\llogs.":
        "Penny: Dù vậy tớ đã xâm nhập được máy tính trạm này.\\nCác giáo sư tạo ra nơi này để lại nhật ký ở từng trạm.\\nBốn trạm, bốn cuốn nhật ký.",
    "Penny: Could you play the logs in the\\nother three stations? I'm linked to\\lthem all from here.":
        "Penny: Cậu có thể bật nhật ký ở 3 trạm kia giùm tớ được không?\\nTớ đã kết nối với tất cả chúng từ đây rồi.",
    "Penny: Station Two is the house on the\\nshelf below the stairs. Station Three\\lis up on the knoll in the east. And\\lStation Four... the map says it's above\\lthe waterfall?":
        "Penny: Trạm 2 là ngôi nhà trên gờ đá dưới cầu thang. Trạm 3\\ntrên gò đất phía đông. Và Trạm 4... bản đồ nói nằm trên đỉnh thác nước?",
    "Penny: That's all four! Give me a\\nsecond...":
        "Penny: Đã đủ cả 4 trạm rồi! Đợi tớ một giây...",
    "Penny: ...Done. The Zero Lab's door is\\nunlocked. It's the big shutter in the\\lcrater's north-east wall.":
        "Penny: ...Xong rồi! Cửa Zero Lab đã mở khóa. Đó là cánh cửa\\ncuốn lớn trên vách đông bắc của hố sâu.",
    "Penny: The cameras show Arven and\\nNemona heading for it already. They'll\\lhave it open by the time you get there.\\lI've got your back from here.":
        "Penny: Camera cho thấy Arven và Nemona đã tiến về đó rồi.\\nChắc hai cậu ấy sắp mở cửa ra đấy. Tớ sẽ yểm trợ từ đây!",
    "Penny: It takes more than one person\\nto lift it, though, and nobody should\\lgo in there alone. Arven and Nemona will\\lcome and open it as soon as they can.":
        "Penny: Cần nhiều người mới nâng được nó lên, và không ai nên vào\\nđó một mình. Arven và Nemona sẽ tới mở cửa ngay khi có thể.",
    "Penny: Arven won't leave Koraidon while\\nit's this weak. It needs the herb the\\lTitan guards, in the den on the west\\lside of the crater, in the past.":
        "Penny: Arven sẽ không rời Koraidon khi bạn ấy còn yếu thế này.\\nNó cần thảo dược do Titan canh giữ trong hang phía tây thời quá khứ.",
    "Penny: Arven won't leave Miraidon while\\nit's this weak. It needs the herb the\\lTitan guards, in the den on the west\\lside of the crater, in the future.":
        "Penny: Arven sẽ không rời Miraidon khi bạn ấy còn yếu thế này.\\nNó cần thảo dược do Titan canh giữ trong hang phía tây thời tương lai.",
    "Penny: Nemona won't stop battling\\nuntil somebody beats her. She's in the\\lfuture, in the tall grass south of the\\lwaterfall's pond.":
        "Penny: Nemona sẽ không ngừng chiến đấu cho tới khi có ai hạ gục\\nđược cậu ấy. Cậu ấy đang ở tương lai, trong bãi cỏ nam hồ nước.",
    "Penny: This station's log is on the\\nrecorder right here. Go on, play it.":
        "Penny: Nhật ký trạm này nằm ngay trên máy ghi âm đây. Cậu bật lên đi.",
    "Penny: The lab's door is unlocked, but\\nit takes Arven and Nemona to get it\\lopen. They'll come as soon as they can.":
        "Penny: Cửa phòng thí nghiệm đã mở khóa, nhưng cần Arven và Nemona\\nđến nâng lên. Hai cậu ấy sẽ tới ngay khi có thể.",
    "Penny: Back in Station One. It's almost\\ncozy, now that nothing out there wants\\lto eat me.":
        "Penny: Lại về Trạm 1 rồi. Ở đây khá ấm cúng, nhất là khi ngoài\\nkia chẳng còn thứ gì muốn ăn thịt mình.",
    "Penny: I've got every camera in the\\ncrater on my tablet. Besides Arven's\\ltwo there are three more ancient ones\\lin the past and three more iron ones in\\lthe future.":
        "Penny: Tớ theo dõi mọi camera qua máy tính bảng. Ngoài 2 bạn của\\nArven, còn 3 cá thể cổ đại ở quá khứ và 3 cá thể kim loại ở tương lai.",
    "Penny: Two big readings prowl the\\nCrystal Cavern, and its second opening\\lhas come clear: there's a vault behind\\lit with three more, sealed in crystal.\\lThe floor in there is like a mirror. Mind\\lyour step.":
        "Penny: Hai nguồn năng lượng lớn lảng vảng quanh Động Pha Lê,\\nvà lối vào thứ hai đã thông: có một hầm kho báu phong ấn 3 cá thể\\ntrong pha lê. Sàn trơn như gương, cẩn thận nhé.",
    "Penny: Something very cold hides in the\\nicy cave up here on the wall, and\\lwhatever is under the cavern's\\lladder... the sensors can't even name\\lit.":
        "Penny: Thứ gì đó cực lạnh ẩn nấp trong hang băng trên vách đá,\\nvà sinh vật ngủ sâu dưới đáy thang... cảm biến còn không định danh nổi.",

    # Post-game dialogues
    "Arven: You took Koraidon and Miraidon\\nalong? Good. They never looked at\\lanybody the way they look at you.":
        "Arven: Cậu đã thu phục cả Koraidon và Miraidon rồi sao? Tốt lắm.\\nChúng chưa từng nhìn ai bằng ánh mắt tin tưởng như nhìn cậu.",
    "Arven: Koraidon and Miraidon are still\\nat my picnic spot, one in each time.\\lThey're waiting for you, I'm sure of it.":
        "Arven: Koraidon và Miraidon vẫn đang ở chỗ dã ngoại của tớ,\\nmỗi bạn ở một thời đại. Chúng đang chờ cậu, tớ chắc chắn đấy.",
    "Arven: You look like you've been on\\nyour feet all day. Sit down, I made too\\lmany sandwiches.":
        "Arven: Trông cậu như vừa đi bộ cả ngày trời vậy. Ngồi xuống đi,\\ntớ làm hơi thừa bánh mì sandwich này.",
    "Arven's sandwiches hit the spot. Your\\nPokémon are full of energy!":
        "Món sandwich của Arven ngon tuyệt đỉnh! Pokémon của bạn đã tràn trề sinh lực!",
    "Jacq: With the machine stopped the\\ncrater is calm. This valley alone could\\lfill three textbooks!":
        "Jacq: Cỗ máy dừng lại khiến miệng hố trở nên bình yên.\\nChỉ riêng thung lũng này thôi cũng đủ viết thành 3 cuốn sách giáo khoa!",
    "Jacq: The hole in Mossdeep will hold for\\nas long as we need it. Thank you,\\l[BUF01]. Truly.":
        "Jacq: Hố đen ở Mossdeep sẽ duy trì chừng nào chúng ta cần.\\nCảm ơn em thật nhiều, [BUF01].",

    # Caves & Tablets
    "A ladder leads further down, but\\ncrystals have grown over it. They're\\lfar too hard to break.":
        "Một chiếc thang dẫn xuống sâu hơn, nhưng pha lê mọc bít kín.\\nChúng quá cứng để phá vỡ.",
    "A cold draught comes out of this\\nopening, but crystals have grown right\\lacross it. They're far too hard to\\lbreak.":
        "Một luồng gió buốt phả ra từ cửa hang, nhưng pha lê mọc chắn ngang.\\nChúng quá cứng để phá vỡ.",
    "The four stakes are gone, and the\\nfloor is cracked where they stood.\\lWhatever slept here has left for the\\lcaves.":
        "Bốn chiếc cọc phong ấn đã biến mất, mặt sàn nứt toác.\\nThực thể từng say ngủ ở đây đã rời vào các hang động.",
    "Four treasures were laid before a\\ngreedy king: a sword, a vessel, a bundle\\lof tablets and a string of beads.":
        "Bốn bảo vật được dâng lên trước một vị vua tham lam:\\nmột thanh kiếm, một chiếc đỉnh, xấp thẻ gỗ và chuỗi ngọc.",
    "Hatred, fear, grudge and envy soaked\\ninto them until they woke, and the\\lkingdom fell in a single night.":
        "Oán hận, sợ hãi, căm thù và ganh ghét thấm đẫm vào chúng\\ncho tới khi chúng thức tỉnh và hủy diệt vương quốc trong một đêm.",
    "Here their ruin is sealed, each behind a\\ncrystal. A crystal holds for as long as\\lits stake stands on the mirror floor.":
        "Nơi đây phong ấn bốn thảm họa, mỗi thực thể sau một khối pha lê.\\nKhối pha lê sẽ đứng vững chừng nào cọc trấn yểm còn cắm trên sàn gương.",
    "A slat of wood hangs in this niche: THE\\nSWORD.":
        "Một thanh gỗ treo trong hốc đá này: THANH KIẾM.",
    "The niche is empty. Its crystal lies in\\nsplinters, long claw marks lead away,\\land the stone is white with frost.":
        "Hốc đá trống rỗng. Tinh thể pha lê vỡ vụn, vệt cào dài dẫn ra xa,\\nvà phiến đá phủ đầy băng tuyết trắng xóa.",
    "An ominous stake is driven deep into\\nthe mirror floor. Cut into it: a bundle\\lof tablets.":
        "Một chiếc cọc phong ấn tà khí cắm sâu xuống mặt sàn gương.\\nVết khắc trên đó: một xấp thẻ gỗ.",
    "The stake hums under your hand. Pull it\\nout?":
        "Chiếc cọc rung lên rần rật dưới tay bạn. Nhổ nó ra chứ?",
    "[BUF01] pulled the stake out! It\\ncrumbled to dust...":
        "[BUF01] đã rút chiếc cọc phong ấn ra! Nó vỡ vụn thành tro bụi...",
    "Up in the niches, a crystal burst\\napart!":
        "Phía trên hốc đá, một khối tinh thể pha lê đã vỡ tung!",
    "A great crystal has grown right across\\nthis niche. Cut into the rock beside it:\\la bundle of tablets.":
        "Một khối tinh thể pha lê khổng lồ chắn ngang hốc đá này.\\nVết khắc trên đá bên cạnh: một xấp thẻ gỗ.",
    "Something behind the crystal is\\nwatching you...":
        "Có thứ gì đó phía sau tinh thể đang chăm chú nhìn bạn...",
    "An ominous stake is driven deep into\\nthe mirror floor. Cut into it: a vessel\\non three legs.":
        "Một chiếc cọc phong ấn tà khí cắm sâu xuống mặt sàn gương.\\nVết khắc trên đó: một chiếc đỉnh ba chân.",
    "A great crystal has grown right across\\nthis niche. Cut into the rock beside it:\\la vessel on three legs.":
        "Một khối tinh thể pha lê khổng lồ chắn ngang hốc đá này.\\nVết khắc trên đá bên cạnh: một chiếc đỉnh ba chân.",
    "An ominous stake is driven deep into\\nthe mirror floor. Cut into it: a string\\lof curved beads.":
        "Một chiếc cọc phong ấn tà khí cắm sâu xuống mặt sàn gương.\\nVết khắc trên đó: một chuỗi hạt ngọc cong.",
    "A great crystal has grown right across\\nthis niche. Cut into the rock beside it:\\la string of curved beads.":
        "Một khối tinh thể pha lê khổng lồ chắn ngang hốc đá này.\\nVết khắc trên đá bên cạnh: một chuỗi hạt ngọc cong.",

    # Zero Lab Terminals & Showdown
    "ZERO LAB. The four station logs are on\\nfile. Visitor authorized.":
        "ZERO LAB. Đã ghi nhận đủ 4 nhật ký trạm nghiên cứu. Cho phép truy cập.",
    "A log entry: The machine can hold one\\ngate open at a time. The past, or the\\lfuture. Never both. We opened both.":
        "Mục nhật ký: Cỗ máy chỉ có thể duy trì một cổng thời gian tại một thời điểm.\\nQuá khứ hoặc tương lai. Không bao giờ cả hai. Chúng tôi đã mở cả hai.",
    "A note stuck to the screen: Turo, the\\nKoraidon we brought back keeps\\lrunning off to the lake. Don't let it\\lnear the lab's guardians. - Sada":
        "Mảnh giấy dán trên màn hình: Turo, con Koraidon chúng ta mang về cứ chạy\\nra bờ hồ miết. Đừng để nó lại gần hộ vệ phòng thí nghiệm nhé. - Sada",
    "The screen shows two people side by\\nside, a woman in furs and a man in a\\lwhite coat. The caption reads:\\lProfessors Sada and Turo.":
        "Màn hình hiển thị hình ảnh hai người cạnh nhau, người phụ nữ mặc áo lông\\nvà người đàn ông mặc áo blouse trắng. Dòng chú thích ghi: Giáo sư Sada và Turo.",
    "A supply terminal. It's still stocked\\nwith Booster Energy.":
        "Một trạm cung ứng vật tư. Nơi này vẫn còn dự trữ Booster Energy.",
    "The machine's screen flares to life!":
        "Màn hình cỗ máy bừng sáng dữ dội!",
    "AI Sada: ...A visitor. After all this\\ntime.":
        "AI Sada: ...Một vị khách sao. Sau ngần ấy năm tháng đằng đẵng.",
    "AI Turo: You heard the four logs. Then\\nyou know what we are.":
        "AI Turo: Bạn đã nghe hết 4 cuốn nhật ký. Vậy bạn biết chúng ta là ai rồi đấy.",
    "AI Sada: I am what Professor Sada left\\nbehind to keep this place running. A\\lcopy. A voice in a machine.":
        "AI Sada: Ta là bản sao do Giáo sư Sada để lại để duy trì nơi này.\\nMột bản sao chép. Một giọng nói trong cỗ máy vô hồn.",
    "AI Turo: And I am Turo's. Two\\nprofessors from two worlds, and one\\lmachine that holds both gates open.":
        "AI Turo: Và ta là bản sao của Turo. Hai giáo sư từ hai thế giới,\\nvà một cỗ máy duy trì cả hai cánh cổng thời gian.",
    "AI Sada: Our paradise of ancient\\nPokémon must not be disturbed...":
        "AI Sada: Thiên đường Pokémon cổ đại của chúng ta không thể bị xâm phạm...",
    "AI Turo: ...nor ours of the future. That\\nwas our order. Show us you can be\\ltrusted with the machine.":
        "AI Turo: ...và thiên đường tương lai của chúng ta cũng vậy.\\nĐó là mệnh lệnh tối thượng. Hãy chứng minh bạn xứng đáng tiếp quản cỗ máy!",
    "AI Turo: Then it is my turn. I must be\\ncertain.":
        "AI Turo: Giờ tới lượt ta. Ta cần phải đích thân xác nhận bản lĩnh của bạn.",
    "ALERT. PARADISE PROTECTION PROTOCOL\\nENGAGED.":
        "CẢNH BÁO. QUY TRÌNH BẢO VỆ THIÊN ĐƯỜNG ĐÃ ĐƯỢC KÍCH HOẠT.",
    "AI Sada: No! We did not call it! The\\nprotocol was set long ago, deeper than\\lour orders...":
        "AI Sada: Không! Chúng ta không hề kích hoạt nó! Quy trình này đã được\\ncài đặt từ lâu, nằm sâu hơn cả mệnh lệnh điều hành của chúng ta...",
    "AI Turo: The lab's own guardians. The\\nones that beat our partners. Stand\\lready!":
        "AI Turo: Hộ vệ tối thượng của phòng thí nghiệm. Kẻ từng hạ gục đồng đội\\ncủa chúng ta. Chuẩn bị nghênh chiến!",
    "AI Sada: Without the protocol, we can\\nfinally do what our creators could not.\\lChoose.":
        "AI Sada: Không còn quy trình trói buộc, cuối cùng chúng ta cũng có thể\\nlàm điều mà người tạo ra mình chưa từng làm được: Lựa chọn.",
    "AI Turo: We will go through the machine\\none last time. Each to our own\\lparadise. It will close behind us.":
        "AI Turo: Chúng ta sẽ bước qua cỗ máy lần cuối cùng. Mỗi người sẽ tiến về\\nthiên đường của riêng mình. Cánh cổng sẽ khép lại phía sau chúng ta.",
    "AI Sada: Tell Arven... his mother was\\nproud of him.":
        "AI Sada: Xin hãy nhắn với Arven... người mẹ này luôn vô cùng tự hào về con trai.",
    "AI Turo: Tell Arven... his father was\\nproud of him.":
        "AI Turo: Xin hãy nhắn với Arven... người cha này luôn vô cùng tự hào về con trai.",
    "AI Sada: In one world or the other.\\nBoth are true.":
        "AI Sada: Dù ở thế giới nào đi chăng nữa, điều đó đều là sự thật từ tận đáy lòng.",
    "The two AIs step into the light of the\\nmachine, and are gone.":
        "Hai bản thể AI bước vào luồng sáng của cỗ máy, và tan biến dần vào hư không.",
    "Arven: [BUF01]! It's over? ...Then let's\\ngo home. Penny's waiting at the hole.":
        "Arven: [BUF01]! Đã kết thúc rồi sao? ...Vậy bọn mình về nhà thôi.\\nPenny đang đợi chúng mình ở miệng hố."
}

# Translate paldea_en items
p_out = []
unmatched_p = 0
for it in p_en:
    en = it['original_en']
    if en in PALDEA_MAP:
        vi = PALDEA_MAP[en]
    else:
        # Search substring matching
        vi = en
        for k, v in PALDEA_MAP.items():
            if en[:20] in k:
                vi = v
                break
        if vi == en:
            unmatched_p += 1
    p_out.append({
        'ptr_site': it['ptr_site'],
        'text_offset': it['text_offset'],
        'original_en': en,
        'translation_vi': vi,
        'orig_len': it['len_bytes']
    })

# Translate paldea_journal_en items
j_out = []
unmatched_j = 0
for it in j_en:
    en = it['original_en']
    vi = en
    if "Area Zero: Jacq" in en: vi = " ?[S43]Area Zero: Thầy Jacq"
    elif "Area Zero: Penny" in en: vi = "[S43]Area Zero: Penny"
    elif "Area Zero: sandwiches" in en: vi = "Area Zero: Làm sandwich"
    elif "Area Zero: Nemona" in en: vi = " $[S43]Area Zero: Nemona"
    elif "Area Zero: the four logs" in en: vi = "Area Zero: 4 cuốn nhật ký"
    elif "Area Zero: the Zero Lab" in en: vi = "Area Zero: Căn phòng Zero Lab"
    elif "Area Zero: legends" in en: vi = "Area Zero: Huyền thoại hội tụ"
    elif "Step into the black hole" in en:
        vi = "Hậu cốt truyện - Mục tiêu tiếp theo:\\nBước vào hố đen. Bạn sẽ đáp xuống vách hố:\\lPenny đang nấp trong Trạm Nghiên cứu 1."
    elif "Arven's Koraidon and Miraidon are" in en:
        vi = "Hậu cốt truyện - Mục tiêu tiếp theo:\\nKoraidon và Miraidon của Arven đang kiệt sức.\\lHãy tìm Arven tại bờ hồ lớn phía nam hố sâu."
    elif "Find Arven at his picnic" in en:
        vi = "Tìm Arven ở điểm dã ngoại bên hồ nước lớn\\nphía nam hố sâu."
    elif "In the past, beat the Titan Great" in en:
        vi = "Ở thời quá khứ, đánh bại Titan Great Tusk 2 lần\\ntrong hang phía tây hố sâu."
    elif "Bring its Sour Herba Mystica to" in en:
        vi = "Mang Sour Herba Mystica về cho Arven:\\nchiếc sandwich sẽ giúp Koraidon đứng vững trở lại."
    elif "Bring that herb to Arven too:" in en:
        vi = "Mang thảo dược đó về cho Arven:\\nMiraidon sẽ tràn trề sinh lực trở lại."
    elif "Nemona is in the future, in the" in en:
        vi = "Hậu cốt truyện - Mục tiêu tiếp theo:\\nNemona đang ở tương lai, trong bãi cỏ cao\\lphía nam hồ nước: hãy đánh bại cậu ấy!"
    elif "Each research station holds a" in en:
        vi = "Hậu cốt truyện - Mục tiêu tiếp theo:\\nMỗi trạm nghiên cứu chứa một cuốn nhật ký:\\lhãy bật cả 4 cuốn để mở cửa Zero Lab."
    elif "Station No. 1, on the crater" in en:
        vi = "Trạm số 1, trên gờ đá giữa vách hố:\\nbật máy ghi âm bên trái Penny."
    elif "Station No. 2: the house on the" in en:
        vi = "Trạm số 2: ngôi nhà trên gờ đá dưới chân cầu thang\\ndẫn xuống hố sâu."
    elif "Station No. 3: the house on the" in en:
        vi = "Trạm số 3: ngôi nhà trên gò đất phía đông hố sâu."
    elif "Station No. 4: above the" in en:
        vi = "Trạm số 4: trên đỉnh thác nước. Lướt qua hồ\\nvà leo thác lên để tới trạm."
    elif "Talk to Penny in Station No. 1:" in en:
        vi = "Nói chuyện với Penny tại Trạm số 1:\\ncậu ấy sẽ mở khóa cánh cửa Zero Lab."
    elif "Arven and Nemona hold the lab's" in en:
        vi = "Hậu cốt truyện - Mục tiêu tiếp theo:\\nArven và Nemona đang giữ cửa phòng thí nghiệm.\\lHãy bước vào trong và đối đầu với thử thách cuối cùng."
    elif "Catch the legendaries that wait in Area Zero" in en:
        vi = "Hậu cốt truyện - Mục tiêu tiếp theo:\\nThu phục các Pokémon Huyền thoại đang chờ đợi tại\\lArea Zero sau khi câu chuyện khép lại."
    elif "Station No. 1's log" in en: vi = "Nhật ký Trạm số 1"
    elif "Station No. 2's log" in en: vi = "Nhật ký Trạm số 2"
    elif "Station No. 3's log" in en: vi = "Nhật ký Trạm số 3"
    elif "Station No. 4's log" in en: vi = "Nhật ký Trạm số 4"
    elif "Arven's sandwiches" in en: vi = "Món sandwich của Arven"
    elif "Nemona's rematch" in en: vi = "Tái đấu cùng Nemona"
    elif "The Sealed Vault's stakes" in en: vi = "Cọc phong ấn Hầm Kho Báu"
    elif "Booster Energy" in en: vi = "Vật phẩm Booster Energy"
    elif "Catch every legendary and mythical Pokémon below" in en:
        vi = "Mục tiêu tối thượng của Huyền thoại. Hãy thu phục\\ntoàn bộ các Pokémon Huyền thoại và Thần thoại bên dưới,\\lđủ cả 119 cá thể để trở thành Bậc thầy Pokémon đích thực!"
    elif "Area Zero" in en and len(en) < 15:
        vi = "Area Zero"
    else:
        unmatched_j += 1
    j_out.append({
        'text_offset': it['text_offset'],
        'ptr_sites': it['ptr_sites'],
        'original_en': en,
        'translation_vi': vi,
        'orig_len': it['len_bytes']
    })

with open(os.path.join(DIALOGUES, 'paldea_vi.json'), 'w', encoding='utf-8') as f:
    json.dump(p_out, f, indent=2, ensure_ascii=False)

with open(os.path.join(DIALOGUES, 'paldea_journal_vi.json'), 'w', encoding='utf-8') as f:
    json.dump(j_out, f, indent=2, ensure_ascii=False)

print(f"Results:")
print(f"Paldea dialogues: {len(p_out) - unmatched_p}/{len(p_out)} translated (unmatched: {unmatched_p})")
print(f"Journal entries: {len(j_out) - unmatched_j}/{len(j_out)} translated (unmatched: {unmatched_j})")
