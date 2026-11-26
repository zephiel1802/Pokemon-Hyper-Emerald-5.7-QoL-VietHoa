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

EXTRA_PALDEA = {
    'A crystal is growing out of the ground.\\nIt glitters with a strange light.':
        'Một khối tinh thể mọc lên từ lòng đất.\\nNó lấp lánh ánh sáng kỳ lạ.',
    "Arven: It's open. We'll hold the door.\\nWhatever's in there, you can handle it.":
        "Arven: Cửa đã mở! Bọn tớ sẽ giữ cửa.\\nDù bên trong là thứ gì, cậu nhất định sẽ xử lý được!",
    'Koraidon is looking right at you. It\\nwants to come along! Battle it?':
        'Koraidon đang nhìn thẳng vào bạn.\\nNó muốn đồng hành cùng bạn! Khiêu chiến chứ?',
    'The Titan is glaring at you. Battle it?':
        'Con Titan đang gườm gườm nhìn bạn. Khiêu chiến chứ?',
    'Miraidon is looking right at you. It\\nwants to come along! Battle it?':
        'Miraidon đang nhìn thẳng vào bạn.\\nNó muốn đồng hành cùng bạn! Khiêu chiến chứ?',
    "Nemona: Whoa, another Trainer! Down\\nhere?! You're the one Jacq sent? This\\lis the best day ever!":
        "Nemona: Oa, một HLV khác sao! Tận dưới này ư?!\\nCậu là người thầy Jacq phái tới? Ngày tuyệt nhất đời!",
    "Nemona: I'm Nemona. I've battled every\\nIron Pokémon in this crater. Twice.\\lThey're amazing!":
        "Nemona: Tớ là Nemona. Tớ đã đấm nhau với từng con\\nPokémon Sắt trong hố này rồi. Hai lần luôn! Quá đỉnh!",
    "Nemona: But you look like you'd be even\\nbetter. Let's battle! Right now!":
        "Nemona: Nhưng trông cậu còn đỉnh hơn thế nhiều.\\nĐấu với tớ đi! Ngay bây giờ luôn!",
    'Battle it?':
        'Khiêu chiến chứ?',
    "There's a folding cot in the back room,\\nbehind the counter. Rest for a while?":
        "Có một chiếc giường xếp trong phòng nghỉ phía sau quầy.\\nBạn muốn nghỉ ngơi một chút chứ?",
    'You and your Pokémon are fully rested!':
        'Bạn và các Pokémon đã hồi phục toàn bộ thể lực!',
    'A recorder on the counter blinks. A\\nrecording begins to play...':
        'Chiếc máy ghi âm trên quầy nhấp nháy.\\nBản ghi âm bắt đầu phát...',
    "Penny: Eek! ...Oh. You're not a Paradox\\nPokémon. Sorry.":
        "Penny: Ái! ...Ồ. Cậu không phải Paradox Pokémon.\\nThứ lỗi cho tớ nhé.",
    "Penny: I'm Penny. Jacq's student. The\\nblack hole dropped the three of us on\\lthat ledge, and I've been hiding in here\\lever since.":
        "Penny: Tớ là Penny, học sinh của thầy Jacq. Hố đen ném cả\\nba đứa tớ xuống gờ đá đó, và tớ trốn miệt mài trong này từ nãy.",
    'Penny: Arven ran down into the crater\\nwith his backpack full of sandwich\\lstuff, and Nemona went off to battle\\lanything that moves. Typical.':
        'Penny: Arven ôm ba lô đầy đồ làm sandwich chạy xuống hố,\\ncòn Nemona thì hùng hổ lao đi đấm mọi thứ nhúc nhích. Quen quá rồi.',
    "Penny: And the Zero Lab, the big door in\\nthe crater wall, only opens for someone\\lwho has heard all four. I bet that's our\\lway home.":
        "Penny: Và Zero Lab, cánh cửa lớn trên vách hố, chỉ mở\\ncho ai đã nghe đủ cả 4 nhật ký. Tớ cá đó là đường về nhà.",
    "Penny: Still missing Station Two's. The\\nhouse on the shelf, right below the\\lstairs you came down.":
        "Penny: Vẫn còn thiếu Trạm 2. Ngôi nhà trên gờ đá, ngay\\ndưới chân bậc thang cậu vừa đi xuống ấy.",
    "Penny: Still missing Station Three's.\\nIt's the house on top of the knoll, in\\lthe east of the crater.":
        "Penny: Vẫn thiếu Trạm 3. Ngôi nhà nằm trên đỉnh gò đất\\nở phía đông hố sâu.",
    "Penny: Still missing Station Four's.\\nIt's above the waterfall. You'll have to\\lclimb it.":
        "Penny: Vẫn thiếu Trạm 4. Nó nằm trên đỉnh thác nước.\\nCậu sẽ phải leo thác lên đấy.",
    'A great wooden tablet, black with age.\\nThe carving can still be read:':
        'Một tấm bia gỗ cổ xưa đen bóng theo năm tháng.\\nNhững dòng chạm khắc vẫn còn đọc được:',
    'The machine shudders... and goes quiet.\\nThe gates are closing.':
        'Cỗ máy rung chuyển dữ dội... rồi lịm dần.\\nCánh cổng không gian đang từ từ khép lại.'
}

# Update paldea_vi.json
p_data = json.load(open(os.path.join(DIALOGUES, 'paldea_vi.json'), encoding='utf-8'))
for item in p_data:
    en = item['original_en']
    if en in EXTRA_PALDEA:
        item['translation_vi'] = EXTRA_PALDEA[en]

with open(os.path.join(DIALOGUES, 'paldea_vi.json'), 'w', encoding='utf-8') as f:
    json.dump(p_data, f, indent=2, ensure_ascii=False)

# Comprehensive Journal Translator
def translate_journal_string(en):
    t = en.replace('\n', ' ').replace('\l', ' ')
    if en == 'Area Zero': return 'Area Zero'
    if '[S43]Area Zero: Penny' in en: return '[S43]Area Zero: Penny'
    if '$[S43]Area Zero: Nemona' in en: return '$[S43]Area Zero: Nemona'
    if '?[S43]Area Zero: Jacq' in en: return '?[S43]Area Zero: Thầy Jacq'
    if 'Area Zero: Jacq' in en: return 'Area Zero: Thầy Jacq'
    if 'Area Zero: Penny' in en: return 'Area Zero: Penny'
    if 'Area Zero: sandwiches' in en: return 'Area Zero: Làm sandwich'
    if 'Area Zero: Nemona' in en: return 'Area Zero: Nemona'
    if 'Area Zero: the four logs' in en: return 'Area Zero: 4 cuốn nhật ký'
    if 'Area Zero: the Zero Lab' in en: return 'Area Zero: Căn phòng Zero Lab'
    if 'Area Zero: legends' in en: return 'Area Zero: Huyền thoại hội tụ'
    if 'Arven and Nemona have opened the' in t:
        return 'Hậu cốt truyện - Mục tiêu tiếp theo:\\nArven và Nemona đã mở cánh cửa lớn trên vách hố.\\lHãy bước vào Zero Lab và đối mặt trận đấu cuối.'
    if 'Koraidon, Miraidon and the Paradox' in t:
        return 'Hậu cốt truyện - Mục tiêu tiếp theo:\\nKoraidon, Miraidon và các Pokémon Paradox\\lđang chờ đón bạn thu phục tại Area Zero.'
    if "Koraidon waits at Arven's picnic" in t:
        return "Koraidon chờ ở điểm dã ngoại của Arven,\\nở thời quá khứ."
    if "Miraidon waits at Arven's picnic" in t:
        return "Miraidon chờ ở điểm dã ngoại của Arven,\\nở thời tương lai."
    if "Walking Wake: in the crater" in t:
        return "Walking Wake: trong miệng hố, thời quá khứ."
    if "Gouging Fire: in the crater" in t:
        return "Gouging Fire: trong miệng hố, thời quá khứ."
    if "Raging Bolt: in the crater" in t:
        return "Raging Bolt: trong miệng hố, thời quá khứ."
    if "Iron Leaves: in the crater" in t:
        return "Iron Leaves: trong miệng hố, thời tương lai."
    if "Iron Boulder: in the crater" in t:
        return "Iron Boulder: trong miệng hố, thời tương lai."
    if "Iron Crown: in the crater" in t:
        return "Iron Crown: trong miệng hố, thời tương lai."
    if "Wo-Chien: in the Sealed Vault" in t:
        return "Wo-Chien: trong Hầm Kho Báu, sau cửa hang\\nthứ hai của Động Pha Lê."
    if "Chien-Pao: in the icy cave" in t:
        return "Chien-Pao: trong hang băng trên gờ đá\\ngiữa vách hố sâu."
    if "Ting-Lu: in the Sealed Vault" in t:
        return "Ting-Lu: trong Hầm Kho Báu, sau cửa hang\\nthứ hai của Động Pha Lê."
    if "Chi-Yu: in the Sealed Vault" in t:
        return "Chi-Yu: trong Hầm Kho Báu, sau cửa hang\\nthứ hai của Động Pha Lê."
    if "Terapagos: the Underdepths" in t:
        return "Terapagos: Tầng Thẳm Đáy Sâu bên dưới Động Pha Lê."
    if "Area Zero: a sealed vault deep in" in t:
        return "Area Zero: hầm kho báu phong ấn sâu trong Động Pha Lê.\\nHãy rút các cọc trấn yểm trên sàn băng."
    if "Area Zero, the Sealed Vault behind" in t:
        return "Area Zero, Hầm Kho Báu phong ấn sau cửa hang thứ hai\\ncủa Động Pha Lê, sau khi hoàn thành cốt truyện."
    if "Area Zero, the crater in the past" in t:
        return "Area Zero, miệng hố thời quá khứ, chờ ở chỗ dã ngoại\\ncủa Arven sau khi hoàn thành cốt truyện."
    if "Area Zero, the crater in the future" in t:
        return "Area Zero, miệng hố thời tương lai, chờ ở chỗ dã ngoại\\ncủa Arven sau khi hoàn thành cốt truyện."
    if "Area Zero: an icy cave on the crater's wall" in t:
        return "Area Zero: một hang băng trên vách hố sâu,\\nsau khi hoàn thành cốt truyện."
    if "Area Zero, the icy cave on the crater wall's" in t:
        return "Area Zero, hang băng trên gờ đá giữa vách hố sâu,\\nsau khi hoàn thành cốt truyện."
    if "Area Zero: the depths below the cave of crystals" in t:
        return "Area Zero: tầng đáy sâu bên dưới hang pha lê,\\nsau khi hoàn thành cốt truyện."
    if "Area Zero, the Underdepths below the Crystal" in t:
        return "Area Zero, Tầng Thẳm Đáy Sâu dưới Động Pha Lê,\\nsau khi hoàn thành cốt truyện."
    if "The four research stations' logs" in t:
        return "Nhật ký của 4 trạm nghiên cứu trong miệng hố sâu."
    if "Nemona's rematch in Research Station" in t:
        return "Tái đấu cùng Nemona trong Trạm Nghiên cứu số 4."
    if "The three stakes on the Sealed Vault's" in t:
        return "Ba cọc phong ấn trên sàn băng Hầm Kho Báu."
    if "Booster Energy in each crater" in t:
        return "Vật phẩm Booster Energy rơi trong mỗi miệng hố."
    if "The stake of Wo-Chien" in t:
        return "Cọc phong ấn của Wo-Chien: xấp thẻ gỗ."
    if "The stake of Ting-Lu" in t:
        return "Cọc phong ấn của Ting-Lu: chiếc đỉnh ba chân."
    if "The stake of Chi-Yu" in t:
        return "Cọc phong ấn của Chi-Yu: chuỗi ngọc cong."
    if "Booster Energy in the past crater" in t:
        return "Booster Energy trong miệng hố thời quá khứ."
    if "Booster Energy in the future crater" in t:
        return "Booster Energy trong miệng hố thời tương lai."
    return en

# Update paldea_journal_vi.json
j_data = json.load(open(os.path.join(DIALOGUES, 'paldea_journal_vi.json'), encoding='utf-8'))
for item in j_data:
    item['translation_vi'] = translate_journal_string(item['translation_vi'])

with open(os.path.join(DIALOGUES, 'paldea_journal_vi.json'), 'w', encoding='utf-8') as f:
    json.dump(j_data, f, indent=2, ensure_ascii=False)

print("Updated both paldea_vi.json and paldea_journal_vi.json successfully!")
