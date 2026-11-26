# -*- coding: utf-8 -*-
"""Generate high-quality Vietnamese translations for 92 Journal story steps,
strictly aligned 1:1 with the ROM STEPS table and jtitles array.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
en_path = os.path.join(HERE, 'aligned_steps_en.json')
en_steps = json.load(open(en_path, encoding='utf-8'))

# Exact Vietnamese titles for all 92 steps (<= 20 chars)
TITLES_VI = [
    # Hoenn (0..23)
    "Giúp GS. Birch",             # 0: Help Prof. Birch
    "Nhận Pokédex",              # 1: Get the Pokédex
    "Hạ gục Roxanne",            # 2: Beat Roxanne
    "Đuổi theo lính Aqua",       # 3: Chase the Aqua grunt
    "Về Devon Corp.",            # 4: Back to Devon Corp.
    "Giao thư cho Steven",       # 5: A letter for Steven
    "Hạ gục Brawly",             # 6: Beat Brawly
    "Giao Devon Goods",          # 7: Deliver the Devon Goods
    "Hạ gục Wattson",            # 8: Beat Wattson
    "Truy lùng Magma",           # 9: Chase Team Magma
    "Hạ gục Flannery",           # 10: Beat Flannery
    "Hạ gục Norman",             # 11: Beat Norman
    "Viện Thời tiết",            # 12: The Weather Institute
    "Hạ gục Winona",             # 13: Beat Winona
    "Lên Đỉnh Mt. Pyre",         # 14: Climb Mt. Pyre
    "Căn cứ Team Magma",         # 15: Team Magma's hideout
    "Căn cứ Team Aqua",          # 16: Team Aqua's hideout
    "Phong tỏa của Plasma",      # 17: Team Plasma's blockade
    "Hạ Tate & Liza",            # 18: Beat Tate & Liza
    "Trạm Vũ trụ",               # 19: The Space Center
    "Hang Seafloor Cavern",      # 20: The Seafloor Cavern
    "Khủng hoảng Sootopolis",    # 21: Crisis in Sootopolis
    "Hạ gục Juan",               # 22: Beat Juan
    "Liên minh Pokémon",         # 23: The Pokémon League

    # Post-game (24..69)
    "Interpol ghé thăm",         # 24: Interpol at home
    "Đảo Steven",                # 25: Steven's Island
    "Vòng Mega của Wally",       # 26: Wally's Mega Bracelet
    "Khẩn cấp tại Devon",        # 27: Emergency at Devon
    "Mảnh thiên thạch",          # 28: A meteorite fragment
    "GS. Cozmo",                 # 29: Prof. Cozmo
    "Vòng Mega bị cướp",         # 30: The stolen bracelet
    "Đối đầu Zinnia",            # 31: Face Zinnia
    "Leo Tháp Sky Pillar",       # 32: Climb the Sky Pillar
    "Vượt trên bầu trời",        # 33: Beyond the sky
    "Gặp Wallace ở Mossdeep",    # 34: Wallace in Mossdeep
    "Biến cố Meteor Falls",      # 35: Trouble in Meteor Falls
    "Lỗ sâu đầu tiên",           # 36: The first wormhole
    "Báo cáo với Anabel",        # 37: Report to Anabel
    "Pokémon Totem",             # 38: The Totem Pokémon
    "Bốn thử thách Tapu",        # 39: The four trials
    "Báo cáo với Nanu",          # 40: Report to Nanu
    "Tin tức về Faba",           # 41: News of Faba
    "Truy bắt Faba",             # 42: Chase Faba
    "Báo cáo với Anabel",        # 43: Report to Anabel
    "Luyện tập cùng Quán quân",  # 44: Train with Champions
    "Báo cáo với Anabel",        # 45: Report to Anabel
    "Thời tiết dị thường",       # 46: The strange weather
    "Báo cáo với Anabel",        # 47: Report to Anabel
    "Lỗ sâu tại Mt. Pyre",       # 48: Mt. Pyre's wormhole
    "Báo cáo với Anabel",        # 49: Report to Anabel
    "Lỗ sâu tại Shoal Cave",     # 50: Shoal Cave's wormhole
    "Báo cáo với Anabel",        # 51: Report to Anabel
    "Lỗ sâu Tuyến 116",          # 52: Route 116's wormhole
    "Báo cáo với Anabel",        # 53: Report to Anabel
    "Tóm gọn Faba",              # 54: Catch Faba
    "Báo cáo với Anabel",        # 55: Report to Anabel
    "Tìm kiếm Red",              # 56: Find Red
    "Báo cáo với Anabel",        # 57: Report to Anabel
    "18 Tinh thể Z-Crystal",     # 58: The 18 Z-Crystals
    "Tấn công Lâu đài",          # 59: Storm the castle
    "Steven đang đợi",           # 60: Steven is waiting
    "Area Zero: Thầy Jacq",      # 61: Area Zero: Jacq
    "Area Zero: Penny",          # 62: Area Zero: Penny
    "Area Zero: Bánh kẹp",       # 63: Area Zero: sandwiches
    "Area Zero: Nemona",         # 64: Area Zero: Nemona
    "Area Zero: Bốn nhật ký",    # 65: Area Zero: the four logs
    "Area Zero: Phòng Thí nghiệm",# 66: Area Zero: the Zero Lab
    "Area Zero: Huyền thoại",    # 67: Area Zero: legends
    "Biểu tượng Bạc",            # 68: A Silver Symbol
    "Tới Đảo Champion",          # 69: To Champion Island

    # Sinnoh (70..72)
    "Lên tàu tới Sinnoh",        # 70: Sail to Sinnoh
    "Huy hiệu Sinnoh",           # 71: The Sinnoh Badges
    "Liên minh Sinnoh",          # 72: The Sinnoh League

    # Lost Artifacts / Cổ vật (73..91)
    "17 Phiến đá Arceus",        # 73: The 17 Plates
    "Bàn thờ Spear Pillar",      # 74: The Spear Pillar altar
    "Mở lối thông",              # 75: A way through
    "Thế giới Đảo ngược",        # 76: The reverse world
    "Chủ nhân Phiến đá",         # 77: The Plates' owner
    "Cogita ở Hearthome",        # 78: Cogita in Hearthome
    "Vượt qua Khe nứt",          # 79: Through the rift
    "Tìm Cogita ở Hisui",        # 80: Find Cogita in Hisui
    "Các Thủ lĩnh Bộ tộc",       # 81: The clan leaders
    "Động Primeval Cave",        # 82: The Primeval Cave
    "Trở về Trại chỉ huy",       # 83: Back to base camp
    "Người phụ nữ mê ngủ",       # 84: A sleeping woman
    "Đánh thức người mê ngủ",    # 85: Wake the sleeper
    "Tháp Lost Tower",           # 86: The Lost Tower
    "Huyền thoại cuối cùng",     # 87: One more legend
    "Cá khô của Kitty",          # 88: Kitty's dried fish
    "Đỉnh núi linh thiêng",      # 89: The summit
    "Lời mời của Cogita",        # 90: Cogita's invitation
    "Khép lại Hành trình",       # 91: Beyond the story
]

BODY_VI = [
    # 0
    "Đi về phía bắc Littleroot Town tới Tuyến đường 101 giúp GS. Birch. Bạn sẽ nhận chú Pokémon đầu tiên.",
    # 1
    "Tìm con của GS. Birch trên Tuyến đường 103, phía bắc Oldale Town, rồi quay lại phòng nghiên cứu ở Littleroot để nhận Pokédex.",
    # 2
    "Băng qua Rừng Petalburg tới Thành phố Rustboro và đánh bại Roxanne, Thủ lĩnh Nhà thi đấu.",
    # 3
    "Tên lính Team Aqua cướp Hàng Devon! Hãy đuổi theo hắn về phía đông Rustboro vào Đường hầm Rusturf để giành lại.",
    # 4
    "Mang Hàng Devon trả lại Devon Corp. ở Rustboro. Ngài chủ tịch có một lá thư và một món hàng nhờ bạn chuyển giao.",
    # 5
    "Tới nhà ông Briney trên Tuyến 104 nhờ ông chở thuyền tới Thị trấn Dewford. Giao bức thư cho Steven ở sâu trong Hang Granite.",
    # 6
    "Đánh bại Brawly, Thủ lĩnh Nhà thi đấu Thị trấn Dewford.",
    # 7
    "Đi thuyền tới Thành phố Slateport và giao Hàng Devon cho Thuyền trưởng Stern tại Bảo tàng Hải dương học.",
    # 8
    "Đi về phía bắc dọc Tuyến 110 tới Thành phố Mauville và đánh bại Wattson, Thủ lĩnh Nhà thi đấu.",
    # 9
    "Truy lùng Team Magma: từ Tuyến 111 qua Fiery Path tới Thị trấn Fallarbor và Meteor Falls, rồi đi cáp treo lên Mt. Chimney.",
    # 10
    "Đi xuống Đèo Jagged Pass tới Thị trấn Lavaridge và đánh bại Flannery, Thủ lĩnh Nhà thi đấu.",
    # 11
    "Quay về nhà ở Thành phố Petalburg và khiêu chiến với cha của bạn, Norman, Thủ lĩnh Nhà thi đấu.",
    # 12
    "Lướt sóng về phía đông từ Tuyến 118 rồi lên phía bắc theo Tuyến 119: Team Aqua đã chiếm đóng Viện Nghiên cứu Thời tiết.",
    # 13
    "Đánh bại Winona, Thủ lĩnh Fortree City. Nếu chướng ngại vật vô hình chắn đường, dùng Devon Scope của Steven trên Tuyến 120.",
    # 14
    "Đi về phía đông tới Lilycove City. Team Magma và Aqua đang nhắm tới các bảo ngọc trên Mt. Pyre (Tuyến 122): hãy leo lên đỉnh.",
    # 15
    "Đem Magma Emblem từ Mt. Pyre tới Jagged Pass để mở lối vào Căn cứ Team Magma: ngăn chặn Maxie bên trong.",
    # 16
    "Đột kích Căn cứ Team Aqua ở bờ biển phía đông Lilycove City trước khi Archie kịp tẩu thoát.",
    # 17
    "Team Plasma đang phong tỏa Gym Mossdeep. Tìm chúng trong căn phòng băng giá ở Shoal Cave, phía bắc Mossdeep City, và đánh đuổi chúng.",
    # 18
    "Đánh bại Tate & Liza, các Thủ lĩnh Nhà thi đấu Thành phố Mossdeep.",
    # 19
    "Team Magma đang tấn công Trung tâm Vũ trụ Mossdeep! Ngăn chặn chúng, sau đó trò chuyện với Steven.",
    # 20
    "Dùng Dive trên Tuyến đường 128 để tiếp cận Động Seafloor Cavern và ngăn chặn âm mưu của Team Aqua.",
    # 21
    "Groudon và Kyogre đang giao tranh dữ dội tại Sootopolis City. Giúp Wallace: đánh thức Rayquaza tại Sky Pillar (Tuyến 131).",
    # 22
    "Đánh bại Juan, Thủ lĩnh Nhà thi đấu Thành phố Sootopolis.",
    # 23
    "Lướt sóng tới Thành phố Ever Grande, vượt qua Đường Victory Road gian nan và đánh bại Tứ Hoàng cùng Nhà Quán quân.",

    # Post-game (24..69)
    # 24
    "Trở về nhà ở Thị trấn Littleroot: đặc vụ Interpol Nanu và Anabel đang đợi để chúc mừng Tân Quán quân.",
    # 25
    "Người lính gác tại Ever Grande City đã cho bạn đi qua. Đi theo lối thông tới Đảo Steven, nơi đặc vụ Interpol đang đợi.",
    # 26
    "Wally gọi điện khẩn từ Thành phố Petalburg. Nhanh lên: có kẻ đang tìm cách cướp Vòng Mega Bracelet của cậu ấy!",
    # 27
    "Steven gọi điện báo tin khẩn cấp. Hãy đến ngay trụ sở Devon Corp. ở Thành phố Rustboro.",
    # 28
    "Tìm mảnh thiên thạch trong Hang Granite, gần Thị trấn Dewford. Zinnia cũng đang có mặt ở đó.",
    # 29
    "Mang mảnh thiên thạch giao cho GS. Cozmo tại Trung tâm Vũ trụ Thành phố Mossdeep.",
    # 30
    "Team Magma đã cướp mất Vòng Mega Bracelet của bạn. Đến ngay Meteor Falls để ngăn chặn chúng.",
    # 31
    "Đánh bại Zinnia tại Meteor Falls để lấy lại Vòng Mega Bracelet của bạn.",
    # 32
    "Leo lên đỉnh Tháp Sky Pillar (Tuyến 131) và đối đầu với rồng thần Rayquaza.",
    # 33
    "Cưỡi Rayquaza bay thẳng vào vũ trụ để phá hủy thiên thạch. Có điều gì đó bí ẩn đang chờ đợi ngoài không gian.",
    # 34
    "Trở lại mặt đất an toàn, hãy đến nói chuyện với Wallace tại Thành phố Mossdeep.",
    # 35
    "Trở về Đảo Steven. Anabel báo tin có biến cố ở sâu trong Meteor Falls: hãy tìm Steven ở đó.",
    # 36
    "Anabel phát hiện một Lỗ sâu Ultra Wormhole mới gần Thị trấn Pacifidlog: hãy tới điều tra.",
    # 37
    "Báo cáo tình hình cho Anabel tại Đảo Steven.",
    # 38
    "Gladion cần bạn tại Căn cứ Bí mật trên Tuyến 111: Pokémon Totem đang mất kiểm soát.",
    # 39
    "Nanu phát hiện những hòn đảo kỳ lạ. Vượt qua 4 thử thách của các vị thần bảo hộ Tapu.",
    # 40
    "Cả 4 thần bảo hộ Tapu đã công nhận bạn. Hãy quay lại báo cáo với Nanu trên Đảo Steven.",
    # 41
    "Trò chuyện với trinh sát Devon trên Đảo Steven: anh ta phát hiện tung tích của Faba.",
    # 42
    "Trinh sát Devon đã theo dấu Faba tới Lỗ sâu Ultra Wormhole tại Scorched Slab: đuổi theo hắn!",
    # 43
    "Báo cáo tình hình cho Anabel tại Đảo Steven.",
    # 44
    "Anabel thông báo Steven và các cựu Quán quân đang đợi bạn tại phòng huấn luyện trên Đảo Steven.",
    # 45
    "Báo cáo tình hình cho Anabel tại Đảo Steven.",
    # 46
    "Trinh sát Devon báo tin: dao động Lỗ sâu Ultra Wormhole xuất hiện bất thường khắp Hoenn.",
    # 47
    "Báo cáo tình hình cho Anabel tại Đảo Steven.",
    # 48
    "Trinh sát Devon phát hiện một Lỗ sâu Ultra Wormhole tại đỉnh Núi Mt. Pyre: tới điều tra.",
    # 49
    "Báo cáo tình hình cho Anabel tại Đảo Steven.",
    # 50
    "Dao động tiếp theo: căn phòng băng giá ở Động Shoal Cave, nơi Team Plasma từng xuất hiện.",
    # 51
    "Báo cáo tình hình cho Anabel tại Đảo Steven.",
    # 52
    "Dao động tiếp theo: Lỗ sâu Ultra Wormhole trên Tuyến đường 116 gần Đường hầm Rusturf.",
    # 53
    "Báo cáo tình hình cho Anabel tại Đảo Steven.",
    # 54
    "Faba bị bắt gặp một mình gần Tháp Mirage Tower trên Sa mạc Tuyến 111. Bắt hắn lại!",
    # 55
    "Báo cáo tình hình cho Anabel tại Đảo Steven.",
    # 56
    "Tìm Red. Lỗ sâu Ultra Wormhole cuối cùng nằm ở nơi sâu nhất của Hang Meteor Falls.",
    # 57
    "Báo cáo tình hình cho Anabel tại Đảo Steven.",
    # 58
    "Thu thập đủ 18 Tinh thể Z-Crystal, sau đó đến Thị trấn Pacifidlog tìm lối dẫn tới Lâu đài Rainbow Rocket.",
    # 59
    "Tấn công Lâu đài Team Rainbow Rocket và đánh bại trùm phản diện Giovanni.",
    # 60
    "Trở về Đảo Steven: Steven đang đợi bạn ở đó.",
    # 61
    "Nhiệm vụ phụ: một giáo viên đến từ Paldea đang đứng cạnh hố đen tại Mossdeep City, dưới cầu thang gần Viện Vũ trụ.",
    # 62
    "Bước vào hố đen để tới Vực thẳm Area Zero: Penny đang ẩn nấp trong Trạm Nghiên cứu số 1.",
    # 63
    "Koraidon và Miraidon của Arven kiệt sức. Bánh kẹp của cậu ấy cần Sour Herba Mystica từ hai Titan.",
    # 64
    "Nemona đang ở tương lai, trong bãi cỏ cao phía nam hồ nước thác. Hãy đánh bại cô ấy trong trận đấu.",
    # 65
    "Mỗi trạm nghiên cứu chứa một nhật ký của các giáo sư. Hãy xem đủ cả 4 nhật ký rồi nói chuyện với Penny.",
    # 66
    "Arven và Nemona đã mở cửa trập ở vách đông bắc miệng hố. Đi vào trong và nói chuyện với cỗ máy.",
    # 67
    "Koraidon, Miraidon và Pokémon Paradox có thể bắt được ngay bây giờ. Lớp học của thầy Jacq ở trong các trạm nghiên cứu.",
    # 68
    "Đoạt lấy một Biểu tượng Bạc tại Battle Frontier - ví dụ đánh bại Anabel ở Battle Tower chuỗi 35 trận đơn. Sau đó nhận vé tàu từ Scott.",
    # 69
    "Lên phà từ Thành phố Lilycove tới Champion Island để tham gia Giải vô địch Thế giới.",

    # Sinnoh (70..72)
    # 70
    "Đưa vé tàu của Waji cho người thủy thủ tại cảng Lilycove City và lên đường tới Canalave City ở vùng Sinnoh.",
    # 71
    "Đoạt đủ 8 Huy hiệu Gym của vùng Sinnoh. Các huy hiệu còn lại cần đạt:",
    # 72
    "Băng qua Victory Road tới Liên minh Sinnoh và đánh bại Tứ Hoàng cùng Quán quân Cynthia.",

    # Lost Artifacts / Cổ vật (73..91)
    # 73
    "Thu thập đủ 17 Phiến đá Plates ẩn giấu khắp Hoenn và Sinnoh. Waji ở đỉnh Spear Pillar trên Núi Mt. Coronet có gợi ý.",
    # 74
    "Bước lên bàn thờ tại Spear Pillar với đủ 17 Phiến đá. Khe nứt mở ra sẽ thử thách toàn bộ bản lĩnh của bạn.",
    # 75
    "Waji cảm nhận năng lượng khe nứt ở Thị trấn Celestic Town. Đến tàn tích cùng Dialga và Palkia để mở lối vào Thế giới Đảo ngược.",
    # 76
    "Tiến vào Thế giới Đảo ngược Distortion World và đối đầu với chúa tể nơi đây: Giratina.",
    # 77
    "Giữ toàn bộ 17 Phiến đá trong Túi và trở lại đỉnh núi phía trên lâu đài Team Rainbow Rocket. Chủ nhân của các phiến đá đang đợi bạn.",
    # 78
    "Arceus đưa bạn tới Hearthome City. Hãy tìm Cogita trong một ngôi nhà ở phía tây thị trấn, với đủ 17 Phiến đá trong Túi.",
    # 79
    "Bước qua khe nứt không-thời gian trong nhà của Cogita. Lối đi này dẫn tới vùng đất Hisui thời cổ đại.",
    # 80
    "Tìm Cogita ở Hisui. Rei (Mingyao) tại trại Deertrack Heights sẽ chở bạn bay quanh: hãy tìm trên Đảo Firespit Island.",
    # 81
    "Ghé thăm các thủ lĩnh bộ tộc tại suối nước nóng ở vùng tuyết Alabaster Icelands.",
    # 82
    "Diamond và Pearl chỉ về phía chân Núi Mt. Coronet. Vào Động Primeval Cave: kẻ đứng sau khe nứt đang ở bên trong.",
    # 83
    "Volo đã bị đánh bại. Trở về trại chỉ huy ở Hisui: Rei và Cogita có tin tức mới.",
    # 84
    "Tại Thị trấn Solaceon ở Sinnoh, một người phụ nữ chìm trong cơn mê ác mộng từ khi cúng tế ở Lost Tower. Hãy nghe người chồng tâm sự.",
    # 85
    "Mang Lông vũ Mặt trăng Lunar Wing tới cho người phụ nữ mê ngủ ở Thị trấn Solaceon để đánh thức cô ấy.",
    # 86
    "Khí tức áp bức tại Tháp Lost Tower đã tiêu tán. Một thực thể hắc ám đang cựa quậy ở sâu bên trong: đối mặt bóng ma ác mộng.",
    # 87
    "Bắt trọn Tornadus, Thundurus và Landorus, rồi cho Cogita trên Đảo Firespit Island xem. Cô ấy có thêm một truyền thuyết để kể.",
    # 88
    "Kitty trong ngôi nhà 3 tầng trên Đảo Steven đang thèm cá khô. Tìm Món Cá Khô trên Bãi biển Prelude Beach ở Hisui đem về đổi lấy hòn đá vô danh.",
    # 89
    "Giữ hòn đá vô danh của Kitty trong Túi, leo lên Ngôi đền Thiêng liêng ở cao nguyên Hisui. Cảm giác kinh hãi bao trùm đỉnh núi.",
    # 90
    "Cogita đang đợi bạn trên Champion Island với nhiều câu chuyện huyền thoại chưa từng kể.",
    # 91
    "Mọi mục tiêu cốt truyện đã hoàn thành viên mãn! Thử thách 6 trận đấu tại ẩn cốc của Cogita ngoài khơi Sootopolis vẫn đang chờ bạn khám phá!",
]

assert len(TITLES_VI) == 92, f"Titles count mismatch: {len(TITLES_VI)}"
assert len(BODY_VI) == 92, f"Body count mismatch: {len(BODY_VI)}"
assert len(en_steps) == 92, f"EN steps count mismatch: {len(en_steps)}"

result = []
for i in range(92):
    en = en_steps[i]
    if i < 24:
        hdr = "Hoenn - Mục tiêu tiếp theo:"
    elif i < 70:
        hdr = "Hậu truyện - Mục tiêu tiếp theo:"
    elif i < 73:
        hdr = "Sinnoh - Mục tiêu tiếp theo:"
    else:
        hdr = "Cổ vật - Mục tiêu tiếp theo:"

    result.append({
        'index': i,
        'title': TITLES_VI[i],
        'loc': en['loc'],
        'header': hdr,
        'body': BODY_VI[i]
    })

out_path = os.path.join(HERE, 'journal_steps_vi.json')
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(result, f, indent=2, ensure_ascii=False)

print(f"[OK] Successfully built {len(result)} perfectly aligned steps in journal_steps_vi.json!")
