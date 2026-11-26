"""Comprehensive translation dictionary for:
- Party Menu (Box labels, Actions, Item usage, Heal/Status msgs, Hold Items, Mail)
- Move Learning & Deleting (Party, Move Relearner, Move Tutor)
- Pokémon Summary Screen (Stats, Pages, Egg hatching)
- Pokémart / Shopping (Buy, Sell, Quantities, Prices)
- PC Item Storage & Mailbox
- Bag Action Menu
- Field Moves & Party Context Menu Extras
"""

PARTY_SYSTEM_UI_TRANSLATIONS = {
    # =========================================================================
    # 1. MOVE LEARNING & DELETING (Party Menu: party_menu.c)
    # =========================================================================
    0x5E9AE9: r"[BUF02] muốn học\nchiêu [BUF03].\pTuy nhiên, [BUF02] đã\nbiết đủ 4 chiêu rồi.\pBạn có muốn xóa một chiêu để\nthay bằng [BUF03] không?",
    0x5E9AA5: r"[BUF02] đã học được\nchiêu [BUF03]!",
    0x5E9AB4: r"[BUF02] và [BUF03]\nkhông tương thích.\pKhông thể học được\n[BUF03].[FC09]",
    0x5E9B5D: r"Ngừng dạy chiêu\n[BUF03]?",
    0x5E9B76: r"[BUF02] đã không học\nchiêu [BUF03].[FC09]",
    0x5E9B96: r"Nên quên đi chiêu nào?[FC09]",
    0x5E9BB8: r"1, [FC080F]2, và[FC080F]… [FC080F]… [FC080F]… [FC080F][FC1038] Bùm!\p[BUF02] đã quên cách\nsử dụng [BUF03].\pVà…[FC09]",
    0x5E9C00: r"[BUF02] đã biết chiêu\n[BUF03] rồi.[FC09]",
    0x5EA4CB: r"Không thể quên các chiêu\nHM vào lúc này.",

    # Move Relearner / Tutor (teach_move.c)
    0x5EF8C2: r"Dạy chiêu nào cho [BUF02]?",
    0x5EF8DA: r"Dạy chiêu [BUF03]?",
    0x5EF8E4: r"[BUF02] đã học được\nchiêu [BUF03]!",
    0x5EF8F3: r"[BUF02] đang cố học\n[BUF03].\pNhưng [BUF02] không thể học\nquá 4 chiêu thức.\pXóa một chiêu cũ để nhường\nchỗ cho [BUF03]?",
    0x5EF960: r"Ngừng dạy chiêu\n[BUF03]?",
    0x5EF979: r"[FC0820]1, [FC080F]2, và [FC080F]… [FC080F]… [FC080F]… [FC080F][FC1038] Bùm!\p",
    0x5EF9A6: r"[BUF02] đã quên [BUF04].\pVà…\p[BUF02] đã học được [BUF03].",
    0x5EF9E6: r"Từ bỏ việc dạy chiêu mới\ncho [BUF02]?",
    0xFE4C43: r"Muốn quên [BUF03]?",

    # =========================================================================
    # 2. PARTY BOX LABELS & ACTION PROMPTS (party_menu.c)
    # =========================================================================
    0x5EA0BF: r"Học được!",
    0x5EA0C5: r"Không thể!",
    0x5EA0CF: r"Đã học",
    0x5EA0D7: r"Đang có",
    0x5EA0DC: r"Chưa có",
    0x5EA099: r"Có thể",
    0x5EA0B1: r"Có thể",
    0x5EA0B6: r"Không thể",
    0x5EA09E: r"Thứ nhất",
    0x5EA0A4: r"Thứ hai",
    0x5EA0AB: r"Thứ ba",
    0x5EA0E7: r"Thứ tư",
    0x5EA091: r"Vô dụng.",

    # Prompts
    0x5E9E43: r"Chọn một Pokémon.",
    0x5EA010: r"Chọn Pokémon hoặc Hủy.",
    0x5EA02A: r"Chọn Pokémon và xác nhận.",
    0x5E9E55: r"Chuyển đến đâu?",
    0x5E9E64: r"Dạy cho Pokémon nào?",
    0x5E9E79: r"Dùng cho Pokémon nào?",
    0x5E9E8F: r"Cho Pokémon nào giữ?",
    0x5E9EA6: r"Làm gì với mục này?",
    0x5E9F16: r"Hồi phục chiêu nào?",
    0x5E9F2A: r"Tăng PP cho chiêu nào?",
    0x5E9F42: r"Làm gì với vật phẩm?",
    0x5E9FF9: r"Làm gì với Thư?",
    0x5E9F58: r"Không có Pokémon chiến đấu!",
    0x5E9F6F: r"Chọn một Pokémon.",
    0x5E9F81: r"Không đủ HP…",
    0x5E9F90: r"Cần [BUF02] Pokémon.",
    0x5E9FA7: r"Không được chọn trùng Pokémon.",
    0x5E9FC2: r"Không được giữ trùng vật phẩm.",
    0x5E9EBC: r"Không có gì để Cắt.",
    0x5E9ED4: r"Không thể Lướt sóng ở đây.",
    0x5E9EE9: r"Bạn đang Lướt sóng rồi.",
    0x5E9F01: r"Không thể dùng ở đây.",
    0x5E9FDB: r"Dòng nước chảy quá xiết!",
    0x5EA046: r"Hãy đạp xe nào!",
    0x5EA05B: r"Mục này đang được dùng rồi.",
    0x5EA073: r"[BUF02] đang giữ\nmột [BUF03] rồi.",

    # =========================================================================
    # 3. PARTY CONTEXT MENU & FIELD MOVES
    # =========================================================================
    0x5E96A0: r"Đổi",
    0x5E96A6: r"Ra trận",
    0x5E96AF: r"Đổi chỗ",
    0x5E96B6: r"Lý lịch",
    0x5E96CA: r"Không vào",
    0x5E96D3: r"Lấy lại",
    0x5E96D8: r"Đọc",
    0x5E96DD: r"Trao đổi",
    0x5E8CF7: r"Hủy",
    0x5E8CF0: r"Hủy",
    0x5EBA4E: r"Hủy",
    0x5E8D0B: r"Vật phẩm",
    0x5E8CD4: r"Cho giữ",
    0x5E8D15: r"Lấy lại",
    0x5E8D10: r"Thư",
    0x5E8D1A: r"Cất đi",
    0x5E8CC6: r"Vứt bỏ",
    0x5E96C4: r"Tham gia",
    0xFD9B84: r"Chiêu thức",

    # Field Moves
    0x31983F: r"Cắt",
    0x319F00: r"Tỏa sáng",
    0x31A421: r"Đập đá",
    0x319B0A: r"Đẩy đá",
    0x319A61: r"Lướt sóng",
    0x319873: r"Bay",
    0x31A643: r"Lặn",
    0x319DEF: r"Thác nước",
    0x319C90: r"Dịch chuyển",
    0x319C1B: r"Đào bới",
    0x31A636: r"Sức mạnh ẩn",
    0x31A20C: r"Uống sữa",
    0x319E57: r"Đẻ trứng",
    0x31A32A: r"Hương ngọt",

    # =========================================================================
    # 4. HEALING, VITAMINS & PARTY STATUS
    # =========================================================================
    0x5E9C17: r"[BUF02] được hồi phục\n[BUF03] HP.[FC09]",
    0x5E9C3E: r"[BUF02] đã được\ngiải độc.[FC09]",
    0x5E9C5F: r"[BUF02] đã khỏi\ntê liệt.[FC09]",
    0x5E9C7C: r"[BUF02] đã tỉnh giấc.[FC09]",
    0x5E9C8A: r"[BUF02] đã hết bỏng.[FC09]",
    0x5E9CA2: r"[BUF02] đã tan băng.[FC09]",
    0x5E9CB7: r"Đã phục hồi PP.[FC09]",
    0x5E9CF5: r"PP của [BUF02] đã tăng.[FC09]",
    0x5E9D0A: r"[BUF02] đã lên\nLv. [BUF03].",
    0x5E9D25: r"Chỉ số [BUF03] cơ bản của\n[BUF02] đã tăng![FC09]",
    0x5E9D45: r"[BUF02] trở nên thân thiết.\nChỉ số [BUF03] giảm![FC09]",
    0x5E9D6D: r"[BUF02] rất yêu quý bạn!\nChỉ số [BUF03] giảm![FC09]",
    0x5E9D90: r"[BUF02] trở nên thân thiết.\nChỉ số [BUF03] không thể giảm thêm![FC09]",
    0x5E9DBE: r"[BUF02] đã hết\nbối rối.[FC09]",
    0x5E9DE1: r"[BUF02] đã hết\nmê hoặc.[FC09]",
    0x5E96F6: r"Không có tác dụng gì.[FC09]",
    0x5E9712: r"Không thể dùng trên\nPokémon này.[FC09]",
    0x5E9738: r"Không thể đổi [BUF02]\nra ngoài![FC09]",
    0x5E9754: r"[BUF02] đang ở trong\ntrận chiến rồi![FC09]",
    0x5E976F: r"[BUF02] đã được chọn rồi.[FC09]",
    0x5E978F: r"[BUF02] không còn sức\nđể chiến đấu![FC09]",
    0x5E97E5: r"Trứng không thể chiến đấu![FC09]",
    0x5E97FC: r"Chưa thể dùng cho đến khi\ncó Huy hiệu mới.[FC09]",

    # =========================================================================
    # 5. HOLD ITEMS & MAIL
    # =========================================================================
    0x5E991B: r"Đã cho [BUF02] giữ\n[BUF03].[FC09]",
    0x5E993A: r"[BUF02] đang giữ một [BUF03].\pBạn có muốn tráo đổi\nhai vật phẩm không?",
    0x5E9980: r"[BUF02] không cầm\nvật phẩm nào.[FC09]",
    0x5E999D: r"Đã lấy [BUF03]\ntừ [BUF02].[FC09]",
    0x5E99DB: r"Đã lấy [BUF03] và\nthay bằng [BUF02].[FC09]",
    0x5E9A69: r"Túi đã đầy. Không thể\ntháo đồ của Pokémon.[FC09]",
    0x5E9A08: r"Pokémon này đang giữ đồ.\nKhông thể nhận Thư.[FC09]",
    0x5E99B8: r"Đã lấy Thư từ Pokémon.[FC09]",
    0x5E98EC: r"Phải tháo Thư trước khi\ncho giữ vật phẩm.[FC09]",
    0x5E9855: r"Gửi Thư đã tháo về\nPC của bạn?",
    0x5E9877: r"Đã gửi Thư về PC.[FC09]",

    # =========================================================================
    # 6. POKÉMON SUMMARY SCREEN
    # =========================================================================
    0x5EA3CF: r"Thông tin",
    0x5EA3DC: r"Kỹ năng",
    0x5EA3EB: r"Chiêu đấu",
    0x5EA3F8: r"Chiêu Contest",
    0x5EA33C: r"Atk",
    0x5EA343: r"Def",
    0x5EA34B: r"Sp. Atk",
    0x5EA353: r"Sp. Def",
    0x5EA35B: r"Speed",
    0x5EA361: r"HP",
    0x5EA37E: r"Uy lực",
    0x5EA384: r"Chính xác",
    0x5EA38D: r"Hấp dẫn",
    0x5EA394: r"Phá rối",
    0x5EA398: r"Trạng thái",
    0x5EA39F: r"Điểm Exp",
    0x5EA3AB: r"Lv. kế tiếp",
    0x5EA3B4: r"Ruy băng: [BUF02]",
    0x5EA40B: r"Có vẻ Quả trứng này sẽ\nmất nhiều thời gian để nở.",
    0x5EA442: r"Thứ gì sẽ nở ra nhỉ?\nSẽ mất chút thời gian.",
    0x5EA475: r"Thỉnh thoảng nó động đậy.\nChắc sắp nở rồi.",
    0x5EA4A2: r"Nó đang phát ra tiếng động.\nNó sắp nở rồi!",

    # =========================================================================
    # 7. SHOP / MART DIALOGUES
    # =========================================================================
    0x5E93C7: r"Mua",
    0x5E93CB: r"Bán",
    0x5E93D0: r"Thoát",
    0x5E93D5: r"Trong Túi: [BUF02]",
    0x5E93E0: r"Ngừng mua sắm.",
    0x5E93EF: r"[BUF02]? Được chứ.\nBạn muốn mua bao nhiêu cái?",
    0x5E9417: r"[BUF02]? Được chứ.\nBạn muốn mua bao nhiêu cái?",
    0x5E943F: r"[BUF02]? Bạn mua [BUF03] cái?\nTổng cộng là $[BUF04].",
    0x5E9468: r"[BUF02] phải không?\nGiá $[BUF03]. Bạn muốn mua chứ?",
    0x5E9493: r"Bạn muốn [BUF02]?\nGiá $[BUF03]. Bạn đồng ý chứ?",
    0x5E94C5: r"Của bạn đây!\nCảm ơn bạn rất nhiều.",
    0x5E94E7: r"Cảm ơn bạn!\nTôi sẽ gửi nó về PC nhà bạn.",
    0x5E9510: r"Cảm ơn bạn!\nTôi sẽ gửi nó về PC nhà bạn.",
    0x5E9539: r"Bạn không có đủ tiền.[FC09]",
    0x5E9558: r"Bạn không còn chỗ chứa\ncho vật phẩm này.[FC09]",
    0x5E957F: r"Chỗ chứa [BUF02] đã đầy.[FC09]",
    0x5E959B: r"Tôi có thể giúp gì thêm\ncho bạn không?",
    0x5E95C7: r"Tôi có thể giúp gì thêm không?",
    0x5E95EA: r"Tôi tặng kèm thêm một\nPremier Ball nữa nhé.[FC09]",
    0x5E960F: r"[BUF03]? Ồ không.\nTôi không thể mua món này.[FC09]",
    0x5E962F: r"[BUF03]?\nBạn muốn bán bao nhiêu cái?",
    0x5E9654: r"Tôi có thể trả $[BUF02].\nNhư vậy có được không?",
    0x5E9677: r"Đã bán [BUF03]\nvà nhận được $[BUF02].",

    # =========================================================================
    # 8. PC ITEM STORAGE & MAILBOX
    # =========================================================================
    0x5EAB36: r"Trang trí",
    0x5EAB41: r"Kho đồ",
    0x5EAB4E: r"Hộp thư",
    0x5EAB56: r"Gửi đồ",
    0x5EAB63: r"Rút đồ",
    0x5EAB71: r"Vứt đồ",
    0x5EAB7B: r"Cất giữ vật phẩm vào PC.",
    0x5EAB92: r"Lấy vật phẩm ra khỏi PC.",
    0x5EABAE: r"Vứt bỏ vật phẩm trong PC.",
    0x5EABD1: r"Không có vật phẩm nào.[FC09]",
    0x5EABE7: r"Túi đồ không còn\nchỗ trống nào.",
    0x5EAC09: r"Rút bao nhiêu\n[BUF02]?",
    0x5EAC22: r"Đã rút [BUF03]\n[BUF02].",
    0x5EAC4B: r"Không có Thư nào ở đây.[FC09]",
    0x5EAC63: r"Bạn muốn làm gì với\nThư của [BUF02]?",
    0x5EAC8D: r"Nội dung thư sẽ bị mất.\nBạn có đồng ý không?",
    0x5EACB5: r"Túi đồ đã đầy.[FC09]",
    0x5EACC8: r"Thư đã được đưa về Túi\nvà xóa sạch nội dung.[FC09]",

    # =========================================================================
    # 9. BAG ACTIONS
    # =========================================================================
    0x5E8CC2: r"Dùng",
    0x5E8CCB: r"Đăng ký",
    0x5E8CD9: r"Xem nhãn",
    0x5E8CE3: r"Xác nhận",
    0x5E8CEB: r"Đi bộ",
    0x5E8CFE: r"Cho xem",
    0x5E8D20: r"Kiểm tra",
    0x5E8D2B: r"Bỏ chọn",
}
