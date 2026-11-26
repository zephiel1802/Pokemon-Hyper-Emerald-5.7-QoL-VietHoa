"""Gameplay special dialogues, C-engine tables, scripted calls, and field interaction strings
for Pokémon Hyper Emerald 5.7 Vietnamese translation.
"""

# 1. GS BIRCH POKÉDEX RATING (21 levels at 0x60f020 & 0x137aac..0x137c0c)
# Each has pointers at [0x137xxx, 0x60f020 + 4*i]
BIRCH_RATING_DATA = [
    {
        'index': 0,
        'orig_off': 0x2A5D6C,
        'sites': ['0x137c00', '0x60f020'],
        'en': r"Go into grassy areas more and look\nfor Pokémon more carefully.",
        'vi': r"Cháu nên chịu khó tìm kiếm Pokémon\nkỹ hơn ở các bãi cỏ nhé."
    },
    {
        'index': 1,
        'orig_off': 0x2A5DAB,
        'sites': ['0x137aac', '0x60f024'],
        'en': r"I guess you're getting the hang\nof it. But, it gets harder from here.",
        'vi': r"Bác thấy cháu đã bắt đầu quen tay rồi.\nNhưng từ giờ sẽ khó khăn hơn đấy."
    },
    {
        'index': 2,
        'orig_off': 0x2A5DF1,
        'sites': ['0x137ab8', '0x60f028'],
        'en': r"Some Pokémon only appear in\ncertain areas.\lYou must be persistent.",
        'vi': r"Có những Pokémon chỉ xuất hiện ở vài nơi\nnhất định. Cháu phải thật kiên trì nhé."
    },
    {
        'index': 3,
        'orig_off': 0x2A5E34,
        'sites': ['0x137ac4', '0x60f02c'],
        'en': r"Well, it could use more quantity,\nbut this is looking more like\la Pokédex now.",
        'vi': r"Dù số lượng chưa nhiều, nhưng trông\nđã ra dáng một Pokédex rồi đấy."
    },
    {
        'index': 4,
        'orig_off': 0x2A5E83,
        'sites': ['0x137ad0', '0x60f030'],
        'en': r"This is coming along pretty good.\nKeep up the effort.",
        'vi': r"Tiến độ rất khả quan đấy.\nHãy tiếp tục cố gắng nhé."
    },
    {
        'index': 5,
        'orig_off': 0x2A5EB9,
        'sites': ['0x137adc', '0x60f034'],
        'en': r"Are you using any Rods?\nThere are many Pokémon in the sea.",
        'vi': r"Cháu có dùng Cần câu không?\nCó rất nhiều Pokémon dưới biển đấy."
    },
    {
        'index': 6,
        'orig_off': 0x2A5EF4,
        'sites': ['0x137ae8', '0x60f038'],
        'en': r"Instead of just catching Pokémon,\nhow about making them evolve, too?",
        'vi': r"Thay vì chỉ bắt Pokémon, cháu thử cho\nchúng tiến hóa xem sao nhé?"
    },
    {
        'index': 7,
        'orig_off': 0x2A5F39,
        'sites': ['0x137af4', '0x60f03c'],
        'en': r"This is going to be a fantastic\nPokédex.\lThat's the feeling I'm getting.",
        'vi': r"Đây chắc chắn sẽ là một Pokédex tuyệt vời.\nBác có linh cảm rất rõ ràng như vậy."
    },
    {
        'index': 8,
        'orig_off': 0x2A5F82,
        'sites': ['0x137b00', '0x60f040'],
        'en': r"You've collected this many…\nYour talent is remarkable!",
        'vi': r"Cháu đã thu thập được chừng này rồi ư…\nTài năng của cháu thật đáng nể!"
    },
    {
        'index': 9,
        'orig_off': 0x2A5FB9,
        'sites': ['0x137b0c', '0x60f044'],
        'en': r"Have you visited the Safari Zone?\pI hear there are some Pokémon that\ncan only be caught there.",
        'vi': r"Cháu đã đến Safari Zone chưa?\pBác nghe nói có vài loài Pokémon\nchỉ có thể bắt được ở đó thôi."
    },
    {
        'index': 10,
        'orig_off': 0x2A6018,
        'sites': ['0x137b18', '0x60f048'],
        'en': r"You've finally reached\nthe 100-kind mark.\pThis is an impressive Pokédex!",
        'vi': r"Cuối cùng cháu đã chạm mốc 100 loài.\pQuả là một cuốn Pokédex ấn tượng!"
    },
    {
        'index': 11,
        'orig_off': 0x2A6061,
        'sites': ['0x137b24', '0x60f04c'],
        'en': r"There might be Pokémon that can be\nfound using Rock Smash.",
        'vi': r"Có thể tìm thấy vài loài Pokémon\nbằng cách dùng chiêu Rock Smash đấy."
    },
    {
        'index': 12,
        'orig_off': 0x2A609C,
        'sites': ['0x137b30', '0x60f050'],
        'en': r"You should get some more Pokémon\nby trading with others.",
        'vi': r"Cháu nên trao đổi thêm Pokémon\nvới những người bạn khác xem sao."
    },
    {
        'index': 13,
        'orig_off': 0x2A60D5,
        'sites': ['0x137b3c', '0x60f054'],
        'en': r"I've heard of Pokémon that evolve\nwhen they come to fully love their\lTrainers.",
        'vi': r"Bác nghe nói có loài Pokémon chỉ tiến hóa\nkhi chúng thực sự yêu quý Huấn luyện viên."
    },
    {
        'index': 14,
        'orig_off': 0x2A6124,
        'sites': ['0x137b48', '0x60f058'],
        'en': r"I had no idea that there were so\nmany Pokémon species in the Hoenn\lregion.",
        'vi': r"Bác không ngờ vùng Hoenn lại có nhiều\nloài Pokémon đa dạng đến thế này."
    },
    {
        'index': 15,
        'orig_off': 0x2A616F,
        'sites': ['0x137b54', '0x60f05c'],
        'en': r"On occasion, some Pokémon appear\nin large numbers like outbreaks.\pDon't miss opportunities like\nthose.",
        'vi': r"Đôi khi, vài loài Pokémon sẽ xuất hiện\nvới số lượng lớn như bầy đàn.\pĐừng bỏ lỡ những cơ hội như vậy nhé."
    },
    {
        'index': 16,
        'orig_off': 0x2A61D6,
        'sites': ['0x137b60', '0x60f060'],
        'en': r"One can get a very good idea about\nthe Pokémon of the Hoenn region\lby looking through your Pokédex.",
        'vi': r"Chỉ cần nhìn vào cuốn Pokédex của cháu\nlà có thể hiểu rất rõ về Pokémon vùng Hoenn."
    },
    {
        'index': 17,
        'orig_off': 0x2A623A,
        'sites': ['0x137b6c', '0x60f064'],
        'en': r"I would say you already qualify as\na Pokémon Professor, and a good\lone, too!",
        'vi': r"Bác cho rằng cháu đã đủ tiêu chuẩn làm\nGiáo sư Pokémon rồi, mà còn rất giỏi nữa!"
    },
    {
        'index': 18,
        'orig_off': 0x2A6287,
        'sites': ['0x137b78', '0x60f068'],
        'en': r"With a Pokédex this complete,\nyou're a real professional at this!",
        'vi': r"Với cuốn Pokédex hoàn thiện thế này,\ncháu đúng là một chuyên gia thực thụ!"
    },
    {
        'index': 19,
        'orig_off': 0x2A62C9,
        'sites': ['0x137bf4', '0x60f06c'],
        'en': r"You're very close to completing\nthis Pokédex.\lI can feel it in my bones!",
        'vi': r"Cháu đã rất gần với việc hoàn thành\nPokédex rồi. Bác cảm nhận rõ điều đó!"
    },
    {
        'index': 20,
        'orig_off': 0x2A6312,
        'sites': ['0x137c0c', '0x60f070'],
        'en': r"Congratulations!\nYour Pokédex is complete!",
        'vi': r"Xin chúc mừng cháu!\nCuốn Pokédex của cháu đã hoàn tất!"
    }
]

# 2. CASINO ROULETTE STRINGS (Mauville Game Corner)
ROULETTE_DATA = [
    {
        'orig_off': 0x2A5B12,
        'sites': ['0x142a7c', '0x142b6c'],
        'en': r"The minimum wager at this table\nis [BUF02]. Do you want to play?",
        'vi': r"Mức cược tối thiểu ở bàn này\nlà [BUF02] Xu. Bạn muốn chơi không?"
    },
    {
        'orig_off': 0x2A5B4E,
        'sites': ['0x142bc0'],
        'en': r"You don't have enough Coins.",
        'vi': r"Bạn không có đủ Xu."
    },
    {
        'orig_off': 0x2A5B6B,
        'sites': ['0x142b20'],
        'en': r"Special rate table right now!",
        'vi': r"Bàn đang có tỷ lệ cược đặc biệt!"
    },
    {
        'orig_off': 0x2A5B89,
        'sites': ['0x140744'],
        'en': r"Place your wager with the + Control\nPad, then press the A Button.",
        'vi': r"Dùng phím điều hướng để đặt cược,\nsau đó nhấn nút A."
    },
    {
        'orig_off': 0x2A5BCB,
        'sites': ['0x141924'],
        'en': r"It's a hit!",
        'vi': r"Trúng rồi!"
    },
    {
        'orig_off': 0x2A5BD7,
        'sites': ['0x1418e8'],
        'en': r"Jackpot!",
        'vi': r"Trúng độc đắc!"
    },
    {
        'orig_off': 0x2A5BE0,
        'sites': ['0x141978'],
        'en': r"Nothing doing!",
        'vi': r"Không trúng rồi!"
    },
    {
        'orig_off': 0x2A5BEF,
        'sites': ['0x141ab4'],
        'en': r"You've won [BUF02] Coins!",
        'vi': r"Bạn đã thắng [BUF02] Xu!"
    },
    {
        'orig_off': 0x2A5C04,
        'sites': ['0x141d04'],
        'en': r"No Coins left…",
        'vi': r"Đã hết Xu rồi…"
    },
    {
        'orig_off': 0x2A5C13,
        'sites': ['0x140960'],
        'en': r"Keep playing?",
        'vi': r"Chơi tiếp không?"
    },
    {
        'orig_off': 0x2A5C21,
        'sites': ['0x141c50'],
        'en': r"The Roulette board will be cleared.",
        'vi': r"Bàn Roulette sẽ được làm mới."
    },
    {
        'orig_off': 0x2A5C61,
        'sites': ['0x141ca4', '0x141dc8'],
        'en': r"Your COIN CASE is full!\nCoins can be exchanged for prizes.",
        'vi': r"Hộp Đựng Xu của bạn đã đầy!\nCó thể đổi Xu lấy phần thưởng."
    }
]

# 3. EVOLUTION MESSAGES
EVOLUTION_DATA = [
    {
        'orig_off': 0x5CC990,
        'sites': ['0x13e70c', '0x13f27c'],
        'en': r"What?\n[BUF02] is evolving!",
        'vi': r"Gì cơ?\n[BUF02] đang tiến hóa!"
    },
    {
        'orig_off': 0x5CC9A6,
        'sites': ['0x13ea10', '0x13f564'],
        'en': r"Congratulations! Your [BUF02]\nevolved into [BUF03]![FC0A]\p",
        'vi': r"Chúc mừng! [BUF02] của bạn\nđã tiến hóa thành [BUF03]![FC0A]\p"
    },
    {
        'orig_off': 0x5CC9D3,
        'sites': ['0x13ec08'],
        'en': r"Huh? [BUF02]\nstopped evolving!\p",
        'vi': r"Ủa? [BUF02]\nđã ngừng tiến hóa!\p"
    }
]

# 4. EGG HATCHING
EGG_HATCH_DATA = [
    {
        'orig_off': 0x5ED5A5,
        'sites': ['0x71c80'],
        'en': r"[BUF02] hatched from the Egg!",
        'vi': r"[BUF02] đã nở ra từ Trứng!"
    },
    {
        'orig_off': 0x5ED5BE,
        'sites': ['0x71ce4'],
        'en': r"Would you like to nickname the newly\nhatched [BUF02]?",
        'vi': r"Bạn có muốn đặt biệt danh cho\n[BUF02] vừa mới nở không?"
    }
]

# 5. DAY CARE COMPATIBILITY (Route 117 Day Care)
DAYCARE_DATA = [
    {
        'orig_off': 0x5EF7DA,
        'sites': ['0x32b6f8'],
        'en': r"The two seem to get along\nvery well.",
        'vi': r"Hai đứa rất thân thiết với nhau."
    },
    {
        'orig_off': 0x5EF7FF,
        'sites': ['0x32b6fc'],
        'en': r"The two seem to get along.",
        'vi': r"Hai đứa có vẻ hòa thuận với nhau."
    },
    {
        'orig_off': 0x5EF81A,
        'sites': ['0x32b700'],
        'en': r"The two don't seem to like\neach other much.",
        'vi': r"Hai đứa không thích nhau cho lắm."
    },
    {
        'orig_off': 0x5EF846,
        'sites': ['0x32b704'],
        'en': r"The two prefer to play with other\nPokémon than each other.",
        'vi': r"Hai đứa thích chơi với Pokémon khác\nhơn là chơi cùng nhau."
    }
]

# 6. REPEL & OVERWORLD FIELD PROMPTS
FIELD_PROMPT_DATA = [
    {
        'orig_off': 0x2A4B2A,
        'sites': ['0x3d7712'],
        'en': r"Repel's effect wore off…",
        'vi': r"Thuốc xịt Repel đã hết tác dụng…"
    },
    {
        'orig_off': 0x5E8F0E,
        'sites': ['0x16c2a8', '0x1ad008', '0x1c63c8'],
        'en': r"Is it okay to\nthrow away [BUF03]\n[BUF02](s)?",
        'vi': r"Bạn có chắc muốn\nvứt bỏ [BUF03]\n[BUF02] không?"
    },
    {
        'orig_off': 0x5E8F31,
        'sites': ['0xfd1ac', '0xfd1dc', '0x1c6220'],
        'en': r"Dad's advice…\n[BUF01], there's a time and place for\leverything![FC09]",
        'vi': r"Lời bố dặn…\n[BUF01] à, chuyện gì cũng phải đúng nơi\nđúng lúc chứ![FC09]"
    },
    {
        'orig_off': 0x5E8F6E,
        'sites': ['0xfd1f4'],
        'en': r"You can't dismount your Bike here.[FC09]",
        'vi': r"Không thể xuống Xe đạp ở đây.[FC09]"
    },
    {
        'orig_off': 0x5E8F93,
        'sites': ['0xfdad4'],
        'en': r"Huh?\nThe Itemfinder's responding!\pThere's an item buried around here![FC09]",
        'vi': r"Ủa?\nMáy Dò Đồ đang phản hồi!\pCó vật phẩm chôn quanh đây![FC09]"
    },
    {
        'orig_off': 0x5E8FDB,
        'sites': ['0xfdb64'],
        'en': r"Oh!\nThe Itemfinder's shaking wildly![FC09]",
        'vi': r"Ô kìa!\nMáy Dò Đồ rung lắc dữ dội![FC09]"
    },
    {
        'orig_off': 0x5E9002,
        'sites': ['0xfd4fc'],
        'en': r"… … … …Nope!\nThere's no response.[FC09]",
        'vi': r"… … … …Không có gì!\nMáy không có phản hồi.[FC09]"
    },
    {
        'orig_off': 0x5E9037,
        'sites': ['0xfdf88'],
        'en': r"Booted up a TM.",
        'vi': r"Đã mở đĩa TM."
    },
    {
        'orig_off': 0x5E9047,
        'sites': ['0xfdf6c'],
        'en': r"Booted up an HM.",
        'vi': r"Đã mở đĩa HM."
    },
    {
        'orig_off': 0x5E9058,
        'sites': ['0xfe01c'],
        'en': r"It contained\n[BUF02].\pTeach [BUF02]\nto a Pokémon?",
        'vi': r"Bên trong có chứa\n[BUF02].\pDạy chiêu [BUF02]\ncho Pokémon chứ?"
    },
    {
        'orig_off': 0x5E9080,
        'sites': ['0xfe0a8'],
        'en': r"[BUF01] used the\n[BUF03].[FC09]",
        'vi': r"[BUF01] đã dùng\n[BUF03].[FC09]"
    },
    {
        'orig_off': 0x5E9092,
        'sites': ['0xfe104', '0xfe11c'],
        'en': r"But the effects of a Repel\nlingered from earlier.[FC09]",
        'vi': r"Nhưng thuốc Repel dùng trước đó\nvẫn còn tác dụng.[FC09]"
    },
    {
        'orig_off': 0x5E90C6,
        'sites': ['0xfe274'],
        'en': r"[BUF01] used the\n[BUF03].\pWild Pokémon will be lured.[FC09]",
        'vi': r"[BUF01] đã dùng\n[BUF03].\pPokémon hoang dã sẽ bị thu hút.[FC09]"
    },
    {
        'orig_off': 0x5E90F4,
        'sites': ['0xfe2b0'],
        'en': r"[BUF01] used the\n[BUF03].\pWild Pokémon will be repelled.[FC09]",
        'vi': r"[BUF01] đã dùng\n[BUF03].\pPokémon hoang dã sẽ bị xua đuổi.[FC09]"
    },
    {
        'orig_off': 0x5E9125,
        'sites': ['0xfe3e8', '0xfe400'],
        'en': r"The Box is full.[FC09]",
        'vi': r"Hộp chứa đã đầy.[FC09]"
    }
]

# 7. SCRIPTED POKÉNAV CALLS (Called via 0xDF opcode)
POKENAV_CALL_DATA = [
    {
        'orig_off': 0x1DFDFB,
        'sites': ['0x1df7bc'],
        'en': r"… … … … … …\n… … … … … Beep!\pWally: Oh, hello, [BUF01]!\pI just wanted to tell you that\nmy uncle bought me a Pokénav!\pNow I can get in touch with you\nanytime, [BUF01]!\p… … … … … …\n… … … … … Click!",
        'vi': r"… … … … … …\n… … … … … Bíp!\pWally: A, chào cậu, [BUF01]!\pTớ chỉ muốn khoe là chú tớ\nvừa mua cho tớ một chiếc Pokénav đấy!\pBây giờ tớ có thể liên lạc với cậu\nbất cứ lúc nào rồi, [BUF01]!\p… … … … … …\n… … … … … Tách!"
    },
    {
        'orig_off': 0x1EE336,
        'sites': ['0x1ed101'],
        'en': r"… … … … … …\n… … … … … Beep!\pDad: Oh, [BUF01]?\p… … … … … …\nWhere are you now?\lIt sounds windy wherever you are.\pI just heard from Devon's Mr. Stone\nabout your Pokénav, so I decided\lto give you a call.\pIt sounds like you're doing fine,\nso that's fine with me.\pYou take care now.\p… … … … … …\n… … … … … Click!",
        'vi': r"… … … … … …\n… … … … … Bíp!\pBố: Ồ, [BUF01] đó hả con?\p… … … … … …\nBây giờ con đang ở đâu thế?\lBên con nghe có tiếng gió rít mạnh quá.\pBố vừa nghe ngài Stone bên tập đoàn\nDevon kể về chiếc Pokénav của con,\nnên bố gọi điện thử xem sao.\pNghe giọng con vẫn khỏe mạnh là bố\nyên tâm rồi.\pCon nhớ tự chăm sóc bản thân nhé.\p… … … … … …\n… … … … … Tách!"
    },
    {
        'orig_off': 0x1F4FBA,
        'sites': ['0x1f49ee'],
        'en': r"… … … … … …\n… … … … … Beep!\pScott: Hiya, [BUF01][BUF05], it's me!\pJust as I thought, you won at\nthe Fortree Gym.\pYour strength…\nPerhaps you really are the Trainer\lthat I've been searching for.\pRemember, you have a fan in me.\nI'll be cheering from the sidelines.\lKeep up the great work!\p… … … … … …\n… … … … … Click!",
        'vi': r"… … … … … …\n… … … … … Bíp!\pScott: Chào [BUF01][BUF05], tôi đây!\pĐúng như tôi dự đoán, cậu đã giành chiến\nthắng tại Nhà thi đấu Fortree.\pThực lực của cậu…\nCó lẽ cậu chính là Huấn luyện viên\nmà bấy lâu nay tôi đang tìm kiếm.\pNhớ nhé, tôi luôn là người ủng hộ cậu đấy.\nTôi sẽ cổ vũ cậu hết mình từ xa.\nHãy tiếp tục phát huy phong độ nhé!\p… … … … … …\n… … … … … Tách!"
    },
    {
        'orig_off': 0x1FBD1A,
        'sites': ['0x1fa4d8'],
        'en': r"… … … … … …\n… … … … … Beep!\pScott: Hi, hi, [BUF01]!\nIt's me, Scott.\pI'm aboard the S.S. Tidal now.\nIt feels great to be on the sea!\pBy the way…\pThere's this place that I'd like to\ninvite you to for a visit.\pIf you're interested, board a ferry\nat either Slateport or Lilycove.\pI'll fill you in on the details when\nwe meet. I'll be waiting!\p… … … … … …\n… … … … … Click!",
        'vi': r"… … … … … …\n… … … … … Bíp!\pScott: Chào cậu, [BUF01]!\nTôi đây, Scott đây.\pHiện tôi đang ở trên tàu S.S. Tidal.\nCảm giác lênh đênh trên biển thật tuyệt!\pÀ này, nhân tiện…\pCó một nơi tuyệt vời mà tôi rất muốn mời\ncậu đến thăm một chuyến đấy.\pNếu hứng thú, hãy bắt phà tại thành phố\nSlateport hoặc Lilycove nhé.\pKhi gặp nhau tôi sẽ nói chi tiết hơn.\nTôi sẽ đợi cậu đấy nhé!\p… … … … … …\n… … … … … Tách!"
    },
    {
        'orig_off': 0x213A76,
        'sites': ['0x21307d'],
        'en': r"… … … … … …\n… … … … … Beep!\pRoxanne: Oh, hello, [BUF01]?\nThis is Roxanne of Rustboro City.\pI heard from Brawly that you're\nmoving up through the ranks of\lTrainers at an incredible clip.\pWell, I'd rather not think that\nI can't beat you.\pI promise, I will shape up my Gym\nso that you may challenge us again.\pI hope you'll be looking forward to\nthat occasion as much as me!\p… … … … … …\n… … … … … Click!",
        'vi': r"… … … … … …\n… … … … … Bíp!\pRoxanne: A, xin chào [BUF01] phải không?\nTôi là Roxanne ở thành phố Rustboro đây.\pTôi nghe Brawly kể rằng cậu đang thăng\ntiến trong giới Huấn luyện viên với\nmột tốc độ đáng kinh ngạc đấy.\nNhưng tôi không hề nghĩ rằng mình sẽ\nchịu thua cậu đâu nhé.\nTôi hứa sẽ rèn luyện lại Nhà thi đấu\nđể cậu có thể đến khiêu chiến lần nữa.\nTôi rất mong chờ ngày tái đấu với cậu đấy!\p… … … … … …\n… … … … … Tách!"
    },
    {
        'orig_off': 0x2B38C1,
        'sites': ['0x224194'],
        'en': r"… … … … … …\n… … … … … Beep!\pMay: Hi, [BUF01][BUF05]!\pI was just in Pacifidlog a little\nwhile ago.\pI saw a giant green Pokémon\nflying high in the sky.\pI…\nI've never seen anything like it.\pI wonder what it was.\nIs this maybe a major discovery?\p… … … … … …\n… … … … … Click!",
        'vi': r"… … … … … …\n… … … … … Bíp!\pMay: Chào cậu, [BUF01][BUF05]!\pVừa nãy tớ vừa ghé qua thị trấn\nPacifidlog một lát.\nTớ đã nhìn thấy một Pokémon khổng lồ màu xanh\nbay lượn tít trên bầu trời cao đấy.\nTớ…\nChưa từng thấy con nào kỳ diệu như vậy cả.\nKhông biết đó là Pokémon gì nhỉ?\nLiệu đây có phải phát hiện vĩ đại không?\p… … … … … …\n… … … … … Tách!"
    },
    {
        'orig_off': 0x2B39C6,
        'sites': ['0x22419b'],
        'en': r"… … … … … …\n… … … … … Beep!\pBrendan: Hey, [BUF01]!\nI was in Pacifidlog just now.\pI saw this huge green Pokémon\nflying across the sky.\pI've never seen anything that\namazing before.\pI wish you could've seen it,\n[BUF01].\p… … … … … …\n… … … … … Click!",
        'vi': r"… … … … … …\n… … … … … Bíp!\pBrendan: Này, [BUF01]!\nTớ vừa ở thị trấn Pacifidlog xong.\nTớ đã thấy một Pokémon khổng lồ màu xanh lục\nbay vút qua bầu trời.\nTrước giờ tớ chưa bao giờ thấy điều gì\nphi thường đến thế.\nGiá mà cậu cũng được tận mắt thấy nó,\n[BUF01] ạ.\p… … … … … …\n… … … … … Tách!"
    }
]

# 8. POKÉDEX SORT ORDER & SEARCH MODE
DEX_SORT_DATA = [
    {
        'orig_off': 0x5E88F6,
        'sites': ['0x56ee28'],
        'en': r"Numerical Mode",
        'vi': r"Theo số thứ tự"
    },
    {
        'orig_off': 0x5E89D4,
        'sites': ['0x56ee24'],
        'en': r"Pokémon are listed according to their\nnumber.",
        'vi': r"Xếp Pokémon theo số thứ tự\ntrong Pokédex."
    },
    {
        'orig_off': 0x5E8905,
        'sites': ['0x56ee30'],
        'en': r"A to Z Mode",
        'vi': r"Theo chữ cái"
    },
    {
        'orig_off': 0x5E8A02,
        'sites': ['0x56ee2c'],
        'en': r"Spotted and owned Pokémon are listed\nalphabetically.",
        'vi': r"Xếp Pokémon đã gặp và đã bắt\ntheo thứ tự bảng chữ cái."
    },
    {
        'orig_off': 0x5E8911,
        'sites': ['0x56ee38'],
        'en': r"Heaviest Mode",
        'vi': r"Nặng nhất"
    },
    {
        'orig_off': 0x5E8A37,
        'sites': ['0x56ee34'],
        'en': r"Owned Pokémon are listed from the\nheaviest to the lightest.",
        'vi': r"Xếp các Pokémon đã bắt từ\nnặng nhất đến nhẹ nhất."
    },
    {
        'orig_off': 0x5E891F,
        'sites': ['0x56ee40'],
        'en': r"Lightest Mode",
        'vi': r"Nhẹ nhất"
    },
    {
        'orig_off': 0x5E8A73,
        'sites': ['0x56ee3c'],
        'en': r"Owned Pokémon are listed from the\nlightest to the heaviest.",
        'vi': r"Xếp các Pokémon đã bắt từ\nnhẹ nhất đến nặng nhất."
    },
    {
        'orig_off': 0x5E892D,
        'sites': ['0x56ee48'],
        'en': r"Tallest Mode",
        'vi': r"Cao nhất"
    },
    {
        'orig_off': 0x5E8AAF,
        'sites': ['0x56ee44'],
        'en': r"Owned Pokémon are listed from the\ntallest to the smallest.",
        'vi': r"Xếp các Pokémon đã bắt từ\ncao nhất đến thấp nhất."
    },
    {
        'orig_off': 0x5E893A,
        'sites': ['0x56ee50'],
        'en': r"Smallest Mode",
        'vi': r"Thấp nhất"
    },
    {
        'orig_off': 0x5E8AEA,
        'sites': ['0x56ee4c'],
        'en': r"Owned Pokémon are listed from the\nsmallest to the tallest.",
        'vi': r"Xếp các Pokémon đã bắt từ\nthấp nhất đến cao nhất."
    },
    {
        'orig_off': 0x5E87A5,
        'sites': ['0x56ed30'],
        'en': r"Search for Pokémon based on\nselected parameters.",
        'vi': r"Tìm kiếm Pokémon theo các điều kiện\nđã chọn."
    },
    {
        'orig_off': 0x5E87D6,
        'sites': ['0x56ed38'],
        'en': r"Switch Pokédex listings.",
        'vi': r"Đổi cách sắp xếp Pokédex."
    },
    {
        'orig_off': 0x5E87EF,
        'sites': ['0x56ed40'],
        'en': r"Return to the Pokédex.",
        'vi': r"Quay lại Pokédex."
    },
    {
        'orig_off': 0x5E8840,
        'sites': ['0x56ed48'],
        'en': r"List by the first letter in the name.\nSpotted Pokémon only.",
        'vi': r"Xếp theo chữ cái đầu của tên.\nChỉ áp dụng với Pokémon đã gặp."
    },
    {
        'orig_off': 0x5E887C,
        'sites': ['0x56ed54'],
        'en': r"List by body color.\nSpotted Pokémon only.",
        'vi': r"Xếp theo màu sắc cơ thể.\nChỉ áp dụng với Pokémon đã gặp."
    },
    {
        'orig_off': 0x5E88A6,
        'sites': ['0x56ed60', '0x56ed6c'],
        'en': r"List by type.\nOwned Pokémon only.",
        'vi': r"Xếp theo hệ thuộc tính.\nChỉ áp dụng với Pokémon đã bắt."
    },
    {
        'orig_off': 0x5E871B,
        'sites': ['0xbf3c4'],
        'en': r"Cry of",
        'vi': r"Tiếng kêu"
    },
    {
        'orig_off': 0x5E8723,
        'sites': ['0xbf970'],
        'en': r"Size Compared To ",
        'vi': r"So kích thước với "
    },
    {
        'orig_off': 0x5E8735,
        'sites': ['0xc0248'],
        'en': r"Pokédex registration completed.",
        'vi': r"Đã đăng ký vào Pokédex thành công."
    },
    {
        'orig_off': 0x5E875B,
        'sites': ['0xc1858'],
        'en': r"Searching…\nPlease wait.",
        'vi': r"Đang tìm kiếm…\nXin vui lòng chờ."
    },
    {
        'orig_off': 0x5E8773,
        'sites': ['0xc1a80'],
        'en': r"Search completed.",
        'vi': r"Đã tìm kiếm xong."
    },
    {
        'orig_off': 0x5E8785,
        'sites': ['0xc1aac'],
        'en': r"No matching Pokémon were found.",
        'vi': r"Không tìm thấy Pokémon phù hợp."
    }
]

# 9. CONTEST MC & ENTRY STRINGS
CONTEST_DATA = [
    {
        'orig_off': 0x27BFF8,
        'sites': ['0x21ab24'],
        'en': r"Your Pokémon will be entered in\nthe Contest. Your Pokémon is Entry No. [BUF03].",
        'vi': r"Pokémon của bạn đã được ghi danh vào\nCuộc thi. Số báo danh là Số [BUF03]."
    },
    {
        'orig_off': 0x27C043,
        'sites': ['0x21ac4a'],
        'en': r"The Contest will begin shortly.",
        'vi': r"Cuộc thi sẽ sớm bắt đầu."
    },
    {
        'orig_off': 0x27BEEC,
        'sites': ['0x21aa8f', '0x21ac3e'],
        'en': r"Transmitting…",
        'vi': r"Đang truyền dữ liệu…"
    },
    {
        'orig_off': 0x278197,
        'sites': ['0x276fcc', '0x277145', '0x277257'],
        'en': r"Please enter.",
        'vi': r"Xin mời vào."
    },
    {
        'orig_off': 0x2781A5,
        'sites': ['0x277b3b'],
        'en': r"I'll direct you to your room now.",
        'vi': r"Tôi sẽ dẫn bạn vào phòng ngay."
    },
    {
        'orig_off': 0x278E00,
        'sites': ['0x277e0f'],
        'en': r"Okay, you're all good to go.\nDon't let the others beat you!",
        'vi': r"Được rồi, bạn đã sẵn sàng.\nĐừng để đối thủ vượt mặt nhé!"
    },
    {
        'orig_off': 0x27B78F,
        'sites': ['0x27a0d8'],
        'en': r"MC: Hello! We're just getting started\nwith a 4-player linked Pokémon [BUF03]! The participating Trainers and their\nPokémon are as follows:",
        'vi': r"MC: Xin chào! Chúng ta chuẩn bị bắt đầu\nCuộc thi Pokémon [BUF03] 4 người chơi!\nCác Huấn luyện viên tham gia và\nPokémon của họ lần lượt là:"
    },
    {
        'orig_off': 0x27C972,
        'sites': ['0x27a0ea'],
        'en': r"The participating Trainers and their\nPokémon are as follows:",
        'vi': r"Các Huấn luyện viên tham gia và\nPokémon của họ lần lượt là:"
    },
    {
        'orig_off': 0x27C9AF,
        'sites': ['0x27a298'],
        'en': r"MC: We've just seen the four Pokémon\ncontestants. Now it's time for primary judging!",
        'vi': r"MC: Chúng ta vừa gặp 4 thí sinh Pokémon.\nBây giờ là lúc bắt đầu vòng sơ khảo!"
    },
    {
        'orig_off': 0x27CA04,
        'sites': ['0x27a2a3'],
        'en': r"The audience will vote on their\nfavorite Pokémon contestants.",
        'vi': r"Khán giả sẽ bình chọn cho thí sinh\nPokémon mà họ yêu thích nhất."
    },
    {
        'orig_off': 0x27CA42,
        'sites': ['0x27a2ae'],
        'en': r"Without any further ado,\nlet the voting begin!",
        'vi': r"Không để quý vị đợi lâu nữa,\nvòng bình chọn xin được phép bắt đầu!"
    },
    {
        'orig_off': 0x27CA71,
        'sites': ['0x27a884'],
        'en': r"Voting is now complete! While the votes are being tallied,\nlet's move on to secondary judging!",
        'vi': r"Vòng bình chọn đã kết thúc! Trong lúc\nkiểm phiếu, chúng ta cùng bước vào\nvòng chấm điểm thứ hai!"
    },
    {
        'orig_off': 0x27CAD0,
        'sites': ['0x27a88f'],
        'en': r"The second stage of judging is\nthe much-anticipated appeal time! May the contestants amaze us with\nsuperb appeals of dazzling moves!",
        'vi': r"Vòng thi thứ hai chính là phần biểu diễn\nđược mong chờ nhất! Hy vọng các thí sinh\nsẽ khiến chúng ta thán phục bằng những\nmàn trình diễn chiêu thức mãn nhãn!"
    },
    {
        'orig_off': 0x27CB55,
        'sites': ['0x27a89a'],
        'en': r"Let's see a little enthusiasm!\nLet's appeal!",
        'vi': r"Hãy cùng cổ vũ thật nhiệt tình nào!\nBắt đầu phần biểu diễn!"
    }
]

# 10. FRONTIER PASS & SAVE ERRORS & HEALER
SYSTEM_MISC_DATA = [
    {
        'orig_off': 0x5CD28F,
        'sites': ['0x39494'],
        'en': r"Would you like to record your battle\non your Frontier Pass?",
        'vi': r"Bạn có muốn lưu trận đấu này\nvào thẻ Frontier Pass không?"
    },
    {
        'orig_off': 0x5E8453,
        'sites': ['0x2fb44'],
        'en': r"The internal battery has run dry.\nThe game can be played. However, clock-based events will no longer occur.",
        'vi': r"Pin đồng hồ bên trong đã cạn.\nBạn vẫn có thể chơi game, nhưng các sự kiện\ntheo thời gian thực sẽ dừng hoạt động."
    },
    {
        'orig_off': 0x5E83C2,
        'sites': ['0x2f9c8'],
        'en': r"The save file is corrupted. The\nprevious save file will be loaded.",
        'vi': r"File lưu bị lỗi. Game sẽ tải lại\nfile lưu trước đó."
    },
    {
        'orig_off': 0x5E8405,
        'sites': ['0x2f9a0'],
        'en': r"The save file has been erased\ndue to corruption or damage.",
        'vi': r"File lưu đã bị xóa\ndo dữ liệu bị hỏng hoặc lỗi."
    },
    {
        'orig_off': 0x242217,
        'sites': ['0x249119'],
        'en': r"现在为你的宝可梦\n进行回复。",
        'vi': r"Đang hồi phục cho Pokémon\ncủa bạn."
    }
]

ALL_GAMEPLAY_SPECIAL_DATA = (
    BIRCH_RATING_DATA +
    ROULETTE_DATA +
    EVOLUTION_DATA +
    EGG_HATCH_DATA +
    DAYCARE_DATA +
    FIELD_PROMPT_DATA +
    POKENAV_CALL_DATA +
    DEX_SORT_DATA +
    CONTEST_DATA +
    SYSTEM_MISC_DATA
)
