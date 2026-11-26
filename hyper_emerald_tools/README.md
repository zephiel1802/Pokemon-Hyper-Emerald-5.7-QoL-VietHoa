# hyper_emerald_tools

Bộ script phân tích/sửa lỗi cho `Hyper Emerald 5.7 VIE.gba` (so với bản gốc `Hyper Emerald Lost Artifacts 5.7.gba`).
Chạy bằng `python3` thường (render_title cần Pillow ở user-site; các script khác cần numpy/capstone).
Dùng chung `he_common.py` (đọc ROM, giải LZ77 chặt, tìm pointer/chuỗi, gom cụm khác biệt).

| Script | Công dụng |
|---|---|
| `audit_lz77.py GOC VIE [--out FIX] [--scan-all]` | Tìm khối LZ77 bị hỏng do repoint nhầm (nát hình); `--out` khôi phục từ bản gốc. |
| `fix_text_pointers.py GOC VIE [--out FIX]` | Sửa pointer text mồ côi (theo thứ tự cụm + pointer anh em). In danh sách còn sót. |
| `audit_code_pointers.py GOC VIE [--restore FIX --slots A B]` | Tìm pointer hàm/bảng Thumb bị repoint nhầm (nguyên nhân treo). Có vài false positive đã biết. |
| `inspect_savestate.py STATE [--rom ROM] [--stack N] [--extract f]` | Đọc savestate mGBA: mode CPU, thanh ghi, stack (đánh dấu địa chỉ trả về BL). |
| `render_title.py ROM STATE out.png [--offset 0xFAE1A0] [--scale 3]` | Vẽ ảnh title (LZ77 8bpp 30x20 tile). STATE phải chụp ở màn title (palette lấy từ state). |

Nguyên nhân gốc: tool build VIE quét pointer ở mọi offset (không căn hàng) nên 4 byte trùng ngẫu nhiên
trong dữ liệu nén/bảng hàm bị "repoint". Chi tiết: `../hyper_emerald_architecture_summary.md`.
Còn tồn: pointer 0x2EE83C→0xBBF1B9 (đích bị ghi đè bởi text mới).
