# -*- coding: utf-8 -*-
"""Builder and QA script for kitakami_batch1_vi.json."""
import json
import re

# Base translations (clean text without hardcoded line breaks, except specific intentional pauses)
# We will wrap them nicely with line 1 = \n, then \l, so that each line <= 36 chars.

RAW_TEXTS = {
    0: "Mục tiêu tối thượng của Huyền thoại. Thu phục toàn bộ Pokémon huyền thoại và thần thoại bên dưới, đủ 124 loài, để hoàn tất.",
    1: "Bạn đã thu phục toàn bộ Pokémon huyền thoại và thần thoại trong game, đủ cả 124 loài! Gotta catch 'em all - và bạn đã làm được. Một Bậc thầy Pokémon thực thụ!",
    2: "Bạn đã thu phục toàn bộ Pokémon huyền thoại và thần thoại trong game, đủ cả 124 loài! Gotta…",
    3: "Mục tiêu tối thượng của Huyền thoại. Thu phục toàn bộ Pokémon huyền thoại và thần thoại bên dưới, đủ 124…",
    4: "Briar: Em đây rồi! Có một lá thư gửi cho em từ Kieran đấy. Để cô đọc cho em nghe nhé...",
    5: "“Nhiều chuyện kỳ lạ đang xảy ra ở Kitakami. Chị Carmine không còn là chính mình nữa, và người ta bảo có lời nguyền.”",
    6: "“Xin hãy quay lại đây, và dẫn theo cả các bạn từ Paldea nữa nhé. Tớ cũng đã viết thư cho họ rồi. - Kieran”",
    7: "Briar: Arven, Nemona và Penny vừa mới xuống xe buýt đấy. Các em ấy đang ở ngoài chợ cùng Kieran!",
    8: "Briar: Cô trò mình đón xe buýt quay về Mossdeep nhé?",
    9: "Briar: Cứ thong thả nhé! Mỗi ngóc ngách ở Kitakami đều ẩn chứa một câu chuyện đấy.",
    10: "Briar: Lên đường thôi nào! Kitakami vẫn sẽ luôn ở đây đón em quay lại.",
    11: "Carmine: Ồ. Là cậu à. Ông bảo tôi phải dẫn cậu đi dạo quanh lễ hội, nên là... chào mừng nhé. Chắc vậy.",
    12: "Carmine: Tối nay ai cũng đeo mặt nạ cả. Đến cả các quầy hàng cũng bày bán. Đây là đêm duy nhất trong năm cái làng này có chút vui vẻ.",
    13: "Carmine: Hử? Nhóc con đó đang làm gì ở đây thế nhỉ?",
    14: "Một Pokémon nhỏ bé đeo chiếc mặt nạ ngọc bích lao thẳng vào bạn! Chiếc mặt nạ của nó rơi loảng xoảng xuống đất...",
    15: "Bạn nhặt chiếc mặt nạ lên. Nó bị mẻ một chút ở phần mép.",
    16: "Carmine: Vừa rồi là... một Pokémon ư? Nó đeo mặt nạ lễ hội sao? Tôi chưa từng thấy loài nào như thế bao giờ.",
    17: "Carmine: Với lại cái mặt nạ đó trông cổ xưa lắm. Cổ xưa thực sự. Ông chắc chắn sẽ biết. Mau đến nhà tôi đi, ở phố phía tây chợ ấy!",
    18: "Carmine: Đi tiếp đi. Cô bé ấy vẫn luôn chờ cậu đấy.",
    19: "Carmine: Một tên chạy qua rặng cây đỏ của ngôi đền, một tên hướng về phía hồ nước, và một tên lên đồi Sảnh Mặt Nạ. Phải đoạt lại các mặt nạ!",
    20: "Carmine: Mochi, mochi, mochi! Muốn ăn không? Ngon lắắắm luôn đó!",
    21: "Carmine: Ư ư, đầu tôi... Tôi chẳng nhớ nổi chuyện gì kể từ khi ăn bánh mochi đó. Cảm ơn vì đã giúp tôi tỉnh lại nhé, kẻ ngoại tộc. ...Ý tôi là, bạn của tôi.",
    22: "Carmine: Hừ. Lại một kẻ ngoại tộc nữa đến để săm soi lễ hội của bọn tôi à?",
    23: "Carmine: Lễ Hội Mặt Nạ là của Kitakami. Nếu cậu muốn xía mũi vào chuyện ở đây, cậu sẽ phải bước qua tôi trước đã!",
    24: "Carmine: C-cái gì cơ?! Cậu thực sự mạnh đấy chứ...",
    25: "Kieran: Chị Carmine! Chị đâu thể cứ đấu với bất kỳ ai vừa bước xuống xe buýt như thế được!",
    26: "Carmine: Tôi làm được hết nếu họ là những kẻ ngoại tộc nhiều chuyện.",
    27: "Kieran: Xin lỗi cậu về chị tớ nhé... Tớ là Kieran. Cậu hẳn là Nhà huấn luyện mà cô Briar đã kể với bọn tớ.",
    28: "Kieran: Người quản lý ở Kitakami Hall có giao nhiệm vụ dã ngoại đấy. Ở trên các bậc thang sau cổng torii, trên đồi ấy.",
    29: "Carmine: Sao cũng được. Đừng có mà đi lạc đấy nhé, kẻ ngoại tộc.",
    30: "Carmine: Ha! Rút cuộc cũng chẳng mạnh mẽ gì cho cam. Khi nào bắt kịp được trình độ của tôi thì hãy quay lại nhé.",
    31: "Kieran: Ồ! Ờm... chào cậu. Xin lỗi nếu chị tớ thô lỗ với cậu nhé. Tính của chị Carmine vốn dĩ là như vậy rồi.",
    32: "Kieran: Tớ là Kieran. Cậu đã nghe về Ác quỷ của Kitakami chưa? Mọi người đều bảo nó từng là một con quái vật...",
    33: "Kieran: ...nhưng tớ luôn thấy có chút tội nghiệp cho nó. Chưa từng có ai kể lại câu chuyện từ góc nhìn của nó cả.",
    34: "Kieran: Người quản lý ở Kitakami Hall có giao nhiệm vụ cho chuyến đi đấy. Đó là tòa nhà màu ngọc bích lớn trên đồi!",
    35: "Kieran: Đây là tấm biển chỉ dẫn đầu tiên! Cậu mau đọc thử đi.",
    36: "Kieran: Đây là tấm biển thứ hai này! Đọc đi, đọc đi nào!",
    37: "...biển thứ hai này! Mau đọc đi, đọc đi nào!",
    38: "Kieran: Đây là tấm biển cuối cùng rồi. Cậu đọc tiếp đi.",
    39: "Kieran: Đây chính là Tam Đại Hộ Vệ. Mọi người ở Mossui đều đến đây để bày tỏ lòng biết ơn với họ.",
    40: "Kieran: Nhưng tớ cứ mãi nghĩ về Ác quỷ đó. Bị xua đuổi khỏi nhà mình, cô độc một mình... mà chẳng có ai thèm hỏi câu chuyện từ phía nó.",
    41: "...Ác quỷ đó. Bị xua đuổi khỏi nhà mình, cô độc một mình... mà chẳng có ai thèm hỏi câu chuyện từ phía nó.",
    42: "Kieran: ...Xin lỗi cậu nhé. Kỳ cục lắm phải không? Chị Carmine bảo tớ bị ám ảnh quá mức rồi.",
    43: "Kieran: Ồ! Trời đã bắt đầu tối rồi kìa. Lễ Hội Mặt Nạ sẽ khai mạc tối nay đấy! Cậu nhất định sẽ đến chứ?",
    44: "...tối nay đấy! Cậu nhất định sẽ đến chứ?",
    45: "Màn đêm buông xuống thị trấn Mossui, và những chiếc đèn lồng của Lễ Hội Mặt Nạ đã được thắp sáng rực rỡ.",
    46: "Kieran: Cậu đã gặp cô bé ấy. Ác quỷ ấy. Ở lễ hội... vậy mà cậu lại không nói với tớ một lời nào.",
    47: "...gặp cô bé ấy. Ác quỷ ấy. Ở lễ hội... vậy mà cậu lại không nói với tớ.",
    48: "Kieran: Cậu biết tớ muốn gặp cô bé ấy hơn bất kỳ điều gì mà! Tớ sẽ giữ chiếc mặt nạ này. Có nó thì cô bé sẽ tìm đến tớ!",
    49: "Kieran: Cậu muốn lấy lại nó ư? Thế thì đấu với tớ đi!",
    50: "Kieran: ...Không. Không, không thể nào!",
    51: "Mặt đất đang rung chuyển dữ dội!",
    52: "Tam Đại Hộ Vệ đã trở lại rồi sao?! Những vị anh hùng, các ngài trở về để bảo vệ chúng tôi ư?",
    53: "Những bức tượng của Tam Đại Hộ Vệ đang... cử động kìa!",
    54: "Kieran: Ác quỷ kìa...! Cô bé ấy ở đây rồi! Cô bé đến để lấy lại chiếc mặt nạ của mình!",
    55: "Okidogi, Munkidori và Fezandipiti đang vây hãm lấy Pokémon đeo mặt nạ!",
    56: "Carmine: Kieran! [BUF01]! Có ai đó đột nhập vào Sảnh Mặt Nạ! Cả ba chiếc mặt nạ đều biến mất rồi!",
    57: "Carmine: Khoan đã... chính ba tên kia đã cướp chúng! Đừng đứng đực ra đó, mau giúp cô bé ấy đi!",
    58: "Bạn, Carmine và Kieran đứng bên Pokémon đeo mặt nạ. Tam Đại Hộ Vệ lùi bước, rồi tháo chạy vào thị trấn!",
    59: "Kieran: Đây... cái này là của cậu. Cho tớ xin lỗi nhé.",
    60: "Pokémon đeo mặt nạ ngoảnh mặt đi khỏi Kieran. Nó đang chăm chú nhìn bạn.",
    61: "Kieran trao Mặt Nạ Ngọc Bích cho bạn, và bạn đưa nó về phía Pokémon ấy.",
    62: "Ogerpon đã đeo Mặt Nạ Ngọc Bích lên!",
    63: "Ogerpon cất tiếng reo vui sướng, rồi chạy vút về phía khu rừng.",
    64: "Kieran: ...Cô bé ấy thậm chí còn chẳng thèm nhìn tớ lấy một lần.",
    65: "Carmine: Ba tên kia đã ôm mặt nạ bỏ chạy. Một tên qua rặng cây đỏ đền thờ, một tên về phía ao, một tên lên đồi Sảnh!",
    66: "...rặng cây đỏ đền thờ, một tên về phía ao, một tên lên đồi Sảnh!",
    67: "Carmine: Nếu đoạt lại được các mặt nạ, Ogerpon có thể sẽ quay lại. Cậu đi đi, tôi sẽ trông chừng em trai.",
    68: "Kieran: Đi đi! Chiếc mặt nạ này giờ là của tớ rồi.",
    69: "Kieran: Cô bé ấy đang đợi cậu. Chứ không phải tớ.",
    70: "Kieran: Tất cả là lỗi tại tớ... Làm ơn, hãy lấy lại những chiếc mặt nạ cho cô bé.",
    71: "...làm ơn, hãy lấy lại các mặt nạ cho cô bé.",
    72: "Kieran: Cậu đã đến rồi! Cảm ơn cậu nhé... Cả Arven, Nemona, Penny, cảm ơn các cậu.",
    73: "Kieran: Là chị Carmine đấy. Mấy ngày nay chị ấy chỉ toàn nhảy múa và nhắc đến mochi. Không chỉ mình chị ấy đâu.",
    74: "Kieran: Dân làng bảo đó là lời nguyền. Lễ hội đã hết từ lâu, vậy mà người ta vẫn nhảy múa ngoài đường suốt đêm...",
    75: "Nemona: Mochi hả? Để tớ chạy ra quầy mua cho tụi mình một ít nhé! Về ngay đây!",
    76: "Kieran: Khoan đã, Nemona! ...Chạy mất rồi. Tụi mình xem quanh đây đi. Bác làm vườn và người mẹ cũng rất lạ.",
    77: "Kieran: Bác nông dân bên ruộng lúa và người mẹ trên phố ấy. Có điều gì đó bất thường ở họ.",
    78: "Kieran: Ông bà vừa mới nhảy múa đi lên Kitakami Hall rồi... Mau lên nào!",
    79: "Kieran: Arven và Penny ăn mochi rồi... Giờ họ cũng đang nhảy múa kìa! Họ ở ngay đằng kia!",
    80: "Kieran: Con Pokémon hình quả đào kia đã lên Loyalty Plaza rồi. Nemona cũng đang ở trên đó cùng với nó!",
    81: "Kieran: Mọi người đã trở lại bình thường. ...Chị Carmine và tớ sắp phải quay về Blueberry Academy rồi.",
    82: "Kieran: Lần tới, tụi mình hãy đấu một trận tại League Club nhé. Tớ sẽ mạnh hơn nhiều. Hứa đấy.",
    83: "Okidogi, Munkidori và Fezandipiti. Tam Đại Hộ Vệ. Ngày xưa họ đã đánh đuổi Ác quỷ ra khỏi Kitakami.",
    84: "Tôi đến cảm tạ họ mỗi buổi sáng. Không có họ, ai biết con Ác quỷ đó đã làm gì với chúng tôi chứ?",
    85: "Các bức tượng... Tam Đại Hộ Vệ sống lại ư? Và họ đã đánh cắp các mặt nạ sao? Anh hùng đâu có đi trộm...",
    86: "...sống lại ư? Và họ đã đánh cắp các mặt nạ sao? Anh hùng đâu có đi trộm...",
    87: "...ư? Và họ đã trộm các mặt nạ sao? Anh hùng đâu có đi ăn trộm...",
    88: "...anh hùng đâu có đi ăn trộm...",
    89: "Kieran kể cho chúng tôi biết sự thật ngày xưa. Từng ấy năm qua, chúng tôi lại đi tạ ơn lũ trộm. Thật xấu hổ.",
    90: "Mochi... mochi... Cậu có chiếc bánh mochi nào không?",
    91: "Lễ Hội Mặt Nạ sắp diễn ra rồi! Mọi người ở Mossui đều đeo mặt nạ và đổ về khu chợ.",
    92: "Các quầy hàng vẫn đang được dựng lên, nên lát nữa hãy quay lại dự lễ hội nhé. Cậu sẽ không thất vọng đâu!",
    93: "...sẽ không thất vọng đâu!",
    94: "Lễ Hội Mặt Nạ đã bắt đầu rồi! Hãy chọn một chiếc mặt nạ ở quầy và tận hưởng đêm hội nhé!",
    95: "Với ba tên kia đang lảng vảng ngoài đó, tôi mừng là lễ hội đã kết thúc...",
    96: "Năm tới, lễ hội sẽ tôn vinh cả Ogerpon nữa. Đó là điều tối thiểu chúng tôi có thể làm cho cô bé.",
    97: "Bức tượng đá của Okidogi, một trong Tam Đại Hộ Vệ. Cánh tay nó trông đủ khỏe để nghiền nát cả tảng đá lớn.",
    98: "Bức tượng đá của Munkidori, một trong Tam Đại Hộ Vệ. Đôi mắt sắc lẹm dường như đang dõi theo bước chân bạn.",
    99: "Bức tượng đá của Fezandipiti, một trong Tam Đại Hộ Vệ. Dù tạc từ đá, bộ lông nó vẫn toát lên vẻ thanh thoát kiêu kỳ.",
    100: "Vẫn đang xếp táo đây! Tại lễ hội, tôi sẽ bày bán Sweet Apple và Tart Apple hái tươi từ trên thung lũng.",
    101: "Táo bọc đường đây! Vừa ngọt vừa thanh, tươi ngon hái từ thung lũng về!",
    102: "Mặt nạ Tam Đại Hộ Vệ đẽo thủ công đây! ...Mặt nạ Ác quỷ hả? Chẳng ai thèm mua thứ đó đâu.",
    103: "Mặt nạ Tam Đại Hộ Vệ đây! Okidogi, Munkidori, Fezandipiti, tha hồ chọn nhé!",
    104: "Hôm nay chẳng có ai muốn mua mặt nạ Tam Đại Hộ Vệ cả. Chẳng hiểu tại sao nữa.",
    105: "Mặt nạ Ogerpon hả? Cháy hàng rồi! Tôi đang cố đẽo thêm thật nhanh đây.",
    106: "Bánh mochi Kitakami, mềm mại và ngọt ngào! Ăn một miếng là thấy khỏe khoắn hẳn. Lễ hội tôi sẽ có rất nhiều.",
    107: "Ai đó để quên thú bông hình quả đào ở quầy tôi... Ồ! Cô Briar đang tìm cậu đấy. Hình như có thư từ gì đó.",
    108: "Bánh mochi lễ hội đây! Chỉ một miếng là cậu sẽ thấy tràn đầy sinh lực!",
    109: "Cơm nắm và xiên nướng, phong vị lễ hội đây! Dù bếp chưa nhóm lửa. Lát nữa để bụng đói rồi quay lại nhé!",
    110: "Cơm nắm và thịt xiên đây! Món ăn tuyệt vời cho một Nhà huấn luyện đang đói bụng!",
    111: "Ác quỷ có quay lại không ạ? ...Mẹ bảo là không. Nhưng ban đêm cháu vẫn chẳng dám bén mảng lại gần rừng đâu.",
    112: "Cháu đang đeo mặt nạ Tam Đại Hộ Vệ này! Grừừ!",
    113: "Mấy bức tượng tự bước đi đấy! Cháu tận mắt thấy luôn!",
    114: "Ác quỷ tên là Ogerpon đấy! Cháu muốn được gặp cô bé ấy quá!",
    115: "Tôi là người làm lồng đèn giấy cho lễ hội. Khi tất cả được thắp sáng, cả khu chợ sẽ rực lên ánh đỏ lung linh!",
    116: "Thấy chưa? Từng chiếc đèn lồng đều đã thắp sáng. Cả khu chợ rực lên ánh đỏ rồi kìa!",
    117: "Đêm nay tôi sẽ thắp vài chiếc đèn lồng. Chẳng ai muốn ở trong bóng tối khi ba tên kia còn lảng vảng ngoài đó.",
    118: "Năm sau tôi sẽ làm một chiếc đèn lồng màu ngọc bích. Dành riêng cho Ogerpon.",
    119: "Tôi vượt núi sang đây xem lễ hội. Lạ thật... Tôi chắc chắn đêm qua mình nghe thấy thứ rất lớn di chuyển trong rừng.",
    120: "Lễ hội tuyệt thật đấy! Thật mừng vì mình đã cất công leo núi sang đây.",
    121: "Đã bảo mà, tôi nghe thấy có tiếng động lớn trong rừng mà lị!",
    122: "Hóa ra thứ ở trong rừng là Ogerpon ư? Ha! Đúng là một câu chuyện tuyệt vời để mang về kể lại.",
    123: "Tôi đẽo mặt nạ cho lễ hội. Đứa trẻ nào cũng đòi mặt nạ Tam Đại Hộ Vệ. Chẳng ai hỏi mua mặt nạ Ác quỷ cả.",
    124: "Tối nay đứa trẻ nào cũng đeo mặt nạ Tam Đại Hộ Vệ. Phần lớn là do chính tay tôi đẽo đấy!",
    125: "Tam Đại Hộ Vệ là những kẻ trộm ư? Tôi đã đẽo khuôn mặt của họ suốt cả đời mình...",
    126: "Tôi đang đẽo chiếc mặt nạ Ác quỷ đầu tiên đây. Ý tôi là của Ogerpon. Khó hơn tôi tưởng nhiều đấy.",
    127: "Tôi trồng lúa ở đây và trồng táo trên thung lũng. Khi lá phong chuyển đỏ, mùa thu hoạch sẽ bắt đầu.",
    128: "Những thửa ruộng trông thật thơ mộng dưới ánh đèn lồng, phải không?",
    129: "Sáng nay có thứ gì to lớn dẫm nát ruộng lúa của tôi! Nó có đôi cánh tay khổng lồ...",
    130: "Ác quỷ hóa ra lại là vị anh hùng thực sự... Tôi nhất định sẽ kể câu chuyện này cho các cháu mình nghe.",
    131: "Tôi chẳng biết chuyện gì đã xảy ra nữa. Một Pokémon màu tím nhỏ bé đưa cho tôi cái bánh mochi, rồi sau đó...",
    132: "...chuyện gì đã xảy ra nữa. Một Pokémon màu tím nhỏ bé đưa cho tôi cái bánh mochi, rồi sau đó...",
    133: "Mochi... thêm mochi nữa đi... Quả đào nhỏ cho tôi mochi! Mochi, mochi...",
    134: "Bạn cất tiếng gọi, hết lần này đến lần khác... Cuối cùng họ chớp mắt, như thể vừa bừng tỉnh sau cơn mê.",
    135: "Mochi... ủa? Mình đang làm gì ở ngoài này thế này?",
    136: "Bé con nhà tôi rất sợ chuyện Ác quỷ. Tôi vẫn luôn bảo cháu rằng Tam Đại Hộ Vệ sẽ bảo vệ chúng tôi.",
    137: "Nhìn bé con nhà tôi đeo mặt nạ kìa! Con bé đáng yêu quá phải không?",
    138: "Chúng tôi sẽ quanh quẩn ở nhà cho tới khi ba tên kia bị bắt giữ.",
    139: "Giờ bé con nhà tôi lại đòi mặt nạ Ogerpon. Thế mà quầy hàng bán sạch veo chỉ trong một tiếng đồng hồ!",
    140: "Tôi thấy ông bà Kieran đi lên Kitakami Hall. Họ mang theo cả một hộp bánh mochi lớn...",
    141: "Mochi mochi! Mochi ngọt ngào nhất ở Kitakami đây! Muốn nhảy múa không? Khiêu vũ cùng tôi đi!",
    142: "...ở Kitakami! Muốn nhảy múa không? Khiêu vũ cùng tôi đi!",
    143: "Ái da... bánh mochi của tôi đâu mất rồi?",
    144: "Bạn đưa ba chiếc mặt nạ ra. Ogerpon nhận lại từng chiếc một... Trông cô bé ngập tràn hạnh phúc!",
    145: "Ogerpon ngước nhìn bạn. Cô bé muốn được đi cùng bạn!",
    146: "Kieran: Không! Cô bé ấy phải là cộng sự của TỚ chứ! Tớ đã chờ đợi cả đời mình chỉ để được gặp cô bé!",
    147: "Kieran: Đấu với tớ đi! Nếu tớ thắng, cô bé sẽ đi cùng tớ!",
    148: "Kieran: Tại sao... tại sao tớ không bao giờ thắng được chứ?",
    149: "Carmine: Kieran à... cô bé đã chọn rồi.",
    150: "Kieran: ...Được rồi. Được rồi mà!",
    151: "Ogerpon giương cao chiếc chùy. Cô bé muốn tự mình thấy thực lực của bạn qua từng chiếc mặt nạ của mình!",
    152: "Đội của bạn lấy lại nhịp thở. Ogerpon đã đeo Mặt Nạ Ngọc Bích lên!",
    153: "Đội của bạn lấy lại nhịp thở. Ogerpon đã đeo chiếc Wellspring Mask lên!",
    154: "Đội của bạn lấy lại nhịp thở. Ogerpon đã đeo chiếc Hearthflame Mask lên!",
    155: "Đội của bạn lấy lại nhịp thở. Ogerpon đã đeo chiếc Cornerstone Mask lên!"
}

def format_dialogue(text, max_len=36):
    words = text.split()
    lines = []
    cur_line = []
    cur_len = 0
    
    for w in words:
        w_len = len(re.sub(r'\[BUF\d+\]', 'XXXXXX', w))
        add_len = w_len if not cur_line else 1 + w_len
        if cur_line and cur_len + add_len > max_len:
            lines.append(' '.join(cur_line))
            cur_line = [w]
            cur_len = w_len
        else:
            cur_line.append(w)
            cur_len += add_len
    if cur_line:
        lines.append(' '.join(cur_line))
        
    if len(lines) == 1:
        return lines[0]
    elif len(lines) == 2:
        return lines[0] + r'\n' + lines[1]
    else:
        return lines[0] + r'\n' + lines[1] + r'\l' + r'\l'.join(lines[2:])

def main():
    in_path = '/Users/zephiel/.gemini/antigravity/scratch/Pokemon-Hyper-Emerald-5.7-QoL/translation_vi/dialogues/kitakami_batch1.json'
    out_path = '/Users/zephiel/.gemini/antigravity/scratch/Pokemon-Hyper-Emerald-5.7-QoL/translation_vi/dialogues/kitakami_batch1_vi.json'
    
    with open(in_path, 'r', encoding='utf-8') as f:
        orig_items = json.load(f)
        
    output = []
    for i in range(156):
        item = orig_items[i]
        raw = RAW_TEXTS[i]
        
        # Format lines
        # For items 0-3 (legends descriptions), use \n between lines
        if i in [0, 1, 2, 3]:
            # wrap with \n only
            words = raw.split()
            lines = []
            cur = []
            clen = 0
            for w in words:
                add = len(w) if not cur else 1 + len(w)
                if cur and clen + add > 35:
                    lines.append(' '.join(cur))
                    cur = [w]
                    clen = len(w)
                else:
                    cur.append(w)
                    clen += add
            if cur: lines.append(' '.join(cur))
            formatted = r'\n'.join(lines)
        else:
            formatted = format_dialogue(raw, max_len=35)
            
        # Verify tag preservation
        orig_tags = re.findall(r'\[[^\]]+\]', item['text'])
        vi_tags = re.findall(r'\[[^\]]+\]', formatted)
        assert orig_tags == vi_tags, f"Tag mismatch at {i}: {orig_tags} vs {vi_tags}"
        
        output.append({
            "offset": item["offset"],
            "sites": item["sites"],
            "text": item["text"],
            "len": item["len"],
            "translation_vi": formatted
        })
        
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
        
    print(f"Generated {out_path} with {len(output)} items.")

if __name__ == '__main__':
    main()
