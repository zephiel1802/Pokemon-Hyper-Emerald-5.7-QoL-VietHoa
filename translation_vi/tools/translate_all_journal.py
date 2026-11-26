# -*- coding: utf-8 -*-
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
VI = os.path.dirname(HERE)
DIALOGUES = os.path.join(VI, 'dialogues')

j_data = json.load(open(os.path.join(DIALOGUES, 'paldea_journal_vi.json'), encoding='utf-8'))

JOURNAL_MAP = {
    'Area Zero': 'Area Zero',
    'Area Zero, in the tall grass of\\nthe crater in the future, Lv63-67.\\nThe way in: the black hole in\\nMossdeep City.':
        'Area Zero, trong bãi cỏ cao của\\nmiệng hố thời tương lai, Lv63-67.\\nĐường vào: hố đen ở Mossdeep City.',
    'Area Zero, in the tall grass of\\nthe crater in the past, Lv63-67.\\nThe way in: the black hole in\\nMossdeep City.':
        'Area Zero, trong bãi cỏ cao của\\nmiệng hố thời quá khứ, Lv63-67.\\nĐường vào: hố đen ở Mossdeep City.',
    'Area Zero, the Crystal Cavern,\\nLv75, after the story. Once only:\\nif it faints, it is gone for good.':
        'Area Zero, Động Pha Lê, Lv75,\\nsau cốt truyện. Duy nhất 1 lần:\\nnếu bị hạ, sẽ biến mất vĩnh viễn.',
    'Area Zero, the Underdepths below\\nthe Crystal Cavern, Lv80, after\\nthe story.':
        'Area Zero, Tầng Thẳm Đáy Sâu bên\\ndưới Động Pha Lê, Lv80,\\nsau khi hoàn thành cốt truyện.',
    'Area Zero, the Underdepths\\nbelow the Crystal Cavern,\\nLv80, after the story.':
        'Area Zero, Tầng Thẳm Đáy Sâu\\nbên dưới Động Pha Lê,\\nLv80, sau cốt truyện.',
    'Area Zero, the crater in the\\nfuture, Lv75, after the story.\\nOnce only: if it faints, it is\\ngone for good.':
        'Area Zero, miệng hố thời tương lai,\\nLv75, sau cốt truyện. Duy nhất 1 lần:\\nnếu bị hạ, sẽ biến mất vĩnh viễn.',
    "Area Zero, the crater in the\\nfuture, Lv75: it waits at Arven's\\npicnic spot once the story is\\nover.":
        "Area Zero, miệng hố thời tương lai,\\nLv75: chờ ở điểm dã ngoại của\\nArven sau khi hoàn tất cốt truyện.",
    "Area Zero, the icy cave on the\\ncrater wall's middle ledge, Lv75,\\nafter the story.":
        "Area Zero, hang băng trên gờ đá\\ngiữa vách hố sâu, Lv75,\\nsau khi hoàn thành cốt truyện.",
    "Area Zero, the icy cave on the\\ncrater wall's middle ledge,\\nLv75, after the story.":
        "Area Zero, hang băng trên gờ đá\\ngiữa vách hố sâu,\\nLv75, sau cốt truyện.",
    "Area Zero: Arven's picnic by the\\nbig lake. Beat the Titans in the\\nden on the crater's west side -\\nGreat Tusk in the past, Iron\\nTreads in the future - and bring\\nhim both Sour Herba Mystica: his\\nsandwiches get Koraidon and\\nMiraidon up again.":
        "Area Zero: điểm dã ngoại của Arven\\nbên hồ lớn. Đánh bại các Titan\\ntrong hang phía tây — Great Tusk thời\\nquá khứ, Iron Treads thời tương lai —\\nvà mang về Sour Herba Mystica để\\nsandwich giúp Koraidon và Miraidon hồi phục.",
    "Area Zero: Research Station No. 1,\\nthe crater wall's middle ledge.\\nPlay the professor's recorded log\\non the left counter.":
        "Area Zero: Trạm Nghiên cứu 1,\\ntrên gờ đá giữa vách hố sâu.\\nBật cuốn nhật ký ghi âm của giáo sư\\ntrên quầy bên trái.",
    "Area Zero: Research Station No. 2,\\nthe house on the shelf below the\\nstairs into the crater. Play the\\nprofessor's recorded log on the\\nleft counter.":
        "Area Zero: Trạm Nghiên cứu 2,\\nngôi nhà dưới chân bậc thang dẫn xuống\\nmiệng hố. Bật cuốn nhật ký ghi âm\\ncủa giáo sư trên quầy bên trái.",
    "Area Zero: Research Station No. 3,\\nthe house on the knoll in the east\\nof the crater. Play the\\nprofessor's recorded log on the\\nleft counter.":
        "Area Zero: Trạm Nghiên cứu 3,\\nngôi nhà trên đỉnh gò đất phía đông\\nmiệng hố. Bật cuốn nhật ký ghi âm\\ncủa giáo sư trên quầy bên trái.",
    "Area Zero: Research Station No. 4,\\nabove the waterfall: surf across\\nthe pond and climb it. Play the\\nprofessor's recorded log on the\\nleft counter.":
        "Area Zero: Trạm Nghiên cứu 4,\\ntrên đỉnh thác nước: lướt qua hồ và leo\\nthác lên. Bật cuốn nhật ký ghi âm của\\ngiáo sư trên quầy bên trái.",
    'Area Zero: a Pokémon of iron roams\\nthe tall grass of the crater in\\nthe future.':
        'Area Zero: một Pokémon Sắt lảng vảng\\ntrong bãi cỏ cao của miệng hố\\nở thời tương lai.',
    'Area Zero: a Pokémon of iron\\nroams the tall grass of the\\ncrater in the future.':
        'Area Zero: một Pokémon Sắt\\nlảng vảng trong bãi cỏ cao\\ncủa miệng hố thời tương lai.',
    'Area Zero: a sealed vault deep\\nin a cave of crystals. Pull the\\nstakes on its icy floor.':
        'Area Zero: hầm kho báu phong ấn sâu\\ntrong động pha lê. Hãy rút các cọc\\ntrấn yểm trên mặt sàn băng.',
    'Area Zero: after the story, Nemona\\nlives in Research Station No. 3,\\nthe house on the knoll in the east\\nof the crater. Beat her in a\\nrematch.':
        'Area Zero: sau cốt truyện, Nemona ở\\nTrạm Nghiên cứu số 3 trên gò đất\\nphía đông miệng hố. Đánh bại cậu ấy\\ntrong trận tái đấu.',
    'Area Zero: after the story, a\\nlegend waits in the Crystal\\nCavern.':
        'Area Zero: sau cốt truyện, một\\nHuyền thoại đang chờ đợi trong\\nĐộng Pha Lê.',
    'Area Zero: after the story, a\\nlegend waits in the crater in the\\nfuture.':
        'Area Zero: sau cốt truyện, một\\nHuyền thoại đang chờ đợi trong miệng\\nhố thời tương lai.',
    'Area Zero: after the story, a\\nlegend waits in the crater in the\\npast.':
        'Area Zero: sau cốt truyện, một\\nHuyền thoại đang chờ đợi trong miệng\\nhố thời quá khứ.',
    'Area Zero: after the story, a\\nlegend waits in the crater in\\nthe future.':
        'Area Zero: sau cốt truyện, một\\nHuyền thoại đang chờ đợi trong miệng\\nhố thời tương lai.',
    'Area Zero: after the story, a\\nlegend waits in the crater in\\nthe past.':
        'Area Zero: sau cốt truyện, một\\nHuyền thoại đang chờ đợi trong miệng\\nhố thời quá khứ.',
    "Area Zero: after the story, the\\nSealed Vault behind the Crystal\\nCavern's second cave mouth. Slide\\nover the mirror floor to the stake\\nmarked with a bundle of tablets\\nand pull it out.":
        "Area Zero: sau cốt truyện, Hầm Kho Báu\\nphía sau cửa hang thứ hai Động Pha Lê.\\nTrượt trên sàn gương tới cọc khắc\\nhình xấp thẻ gỗ và nhổ nó ra.",
    "Area Zero: after the story, the\\nSealed Vault behind the Crystal\\nCavern's second cave mouth. Slide\\nover the mirror floor to the stake\\nmarked with a string of curved\\nbeads and pull it out.":
        "Area Zero: sau cốt truyện, Hầm Kho Báu\\nphía sau cửa hang thứ hai Động Pha Lê.\\nTrượt trên sàn gương tới cọc khắc\\nhình chuỗi ngọc cong và nhổ nó ra.",
    "Area Zero: after the story, the\\nSealed Vault behind the Crystal\\nCavern's second cave mouth. Slide\\nover the mirror floor to the stake\\nmarked with a vessel on three legs\\nand pull it out.":
        "Area Zero: sau cốt truyện, Hầm Kho Báu\\nphía sau cửa hang thứ hai Động Pha Lê.\\nTrượt trên sàn gương tới cọc khắc\\nhình chiếc đỉnh 3 chân và nhổ nó ra.",
    'Area Zero: an ancient Pokémon\\nroams the tall grass of the crater\\nin the past.':
        'Area Zero: một Pokémon cổ xưa\\nlảng vảng trong bãi cỏ cao của miệng\\nhố ở thời quá khứ.',
    'Area Zero: an ancient Pokémon\\nroams the tall grass of the\\ncrater in the past.':
        'Area Zero: một Pokémon cổ xưa\\nlảng vảng trong bãi cỏ cao của\\nmiệng hố thời quá khứ.',
    "Area Zero: an icy cave on the\\ncrater's wall, once the story is\\nover.":
        "Area Zero: một hang băng trên vách\\nmiệng hố, sau khi hoàn tất cốt truyện.",
    'Area Zero: the crater in the\\nfuture, in the clearing across the\\nfallen tree.' :
        'Area Zero: miệng hố thời tương lai,\\ntrong khoảng đất trống qua thân cây ngã.',
    'Area Zero: the crater in the past,\\nin the clearing across the fallen\\ntree.':
        'Area Zero: miệng hố thời quá khứ,\\ntrong khoảng đất trống qua thân cây ngã.',
    "Area Zero: the depths below the\\ncave of crystals, once the story\\nis over.":
        "Area Zero: tầng đáy sâu bên dưới hang\\npha lê, sau khi hoàn tất cốt truyện.",
    'The 20 Paradox Pokémon of Area\\nZero.':
        '20 Pokémon Paradox tại Area Zero.',
    'Catch the 20 Paradox Pokémon in\\nArea Zero.':
        'Thu phục 20 Pokémon Paradox trong Area Zero.',
    'Vault stake: beads': 'Cọc kho báu: Chuỗi ngọc',
    'Vault stake: tablets': 'Cọc kho báu: Thẻ gỗ',
    'Vault stake: vessel': 'Cọc kho báu: Đỉnh đồng',
    'Area Zero: an item ball in the\\ncrater in the past, and another in\\nthe crater in the future. Take\\nboth.':
        'Area Zero: nhặt bóng vật phẩm trong miệng\\nhố thời quá khứ và bóng khác ở thời\\ntương lai. Hãy nhặt cả hai.',
    "Area Zero: in the tall grass of\\nthe crater in the future and in\\nthe icy cave on the crater wall's\\nmiddle ledge, Lv63-67.":
        "Area Zero: trong bãi cỏ cao miệng hố\\nthời tương lai và trong hang băng trên gờ\\nđá giữa vách miệng hố, Lv63-67.",
    "Area Zero: an icy cave on the\\ncrater's wall, once the story\\nis over.":
        "Area Zero: một hang băng trên vách\\nmiệng hố, sau khi kết thúc cốt truyện.",
    'Area Zero: the depths below\\nthe cave of crystals, once\\nthe story is over.':
        'Area Zero: tầng thẳm đáy sâu bên dưới\\nhang pha lê, sau khi kết thúc cốt truyện.',
    '[S43]Area Zero: Penny': '[S43]Area Zero: Penny'
}

matched = 0
for item in j_data:
    en = item['original_en']
    if en in JOURNAL_MAP:
        item['translation_vi'] = JOURNAL_MAP[en]
        matched += 1

with open(os.path.join(DIALOGUES, 'paldea_journal_vi.json'), 'w', encoding='utf-8') as f:
    json.dump(j_data, f, indent=2, ensure_ascii=False)

print(f"Matched and updated {matched} / {len(j_data)} journal entries!")
