"""Helpers dùng chung cho bộ công cụ phân tích Hyper Emerald (GBA, Gen3 charmap)."""
import bisect
import struct

import numpy as np

ROM_BASE = 0x08000000
# Gen3 charmap (tiếng Anh). Bản VIE dùng thêm mã tuỳ biến cho chữ có dấu nên không decode hết được.
_PUNCT = {0xAB: "!", 0xAC: "?", 0xAD: ".", 0xAE: "-", 0xB4: "'", 0xB8: ",",
          0xFE: "\\n", 0xFA: "\\l", 0xFB: "\\p"}


def read(path):
    with open(path, "rb") as f:
        return f.read()


def dec(b, limit=200):
    """Decode một chuỗi Gen3 tới 0xFF (chỉ để xem nhanh)."""
    out = ""
    for x in b[:limit]:
        if x == 0xFF:
            break
        if x == 0:
            out += " "
        elif 0xBB <= x <= 0xD4:
            out += chr(65 + x - 0xBB)
        elif 0xD5 <= x <= 0xEE:
            out += chr(97 + x - 0xD5)
        elif 0xA1 <= x <= 0xAA:
            out += str(x - 0xA1)
        elif x in _PUNCT:
            out += _PUNCT[x]
        else:
            out += "<%02x>" % x
    return out


def lz77(rom, off, maxsize=0x60000):
    """Giải nén LZ77 kiểu BIOS (header 0x10). Trả (data, địa_chỉ_kết_thúc) hoặc None nếu stream hỏng.

    Hỏng = back-reference vượt quá phần đã giải nén, hoặc hết dữ liệu ROM giữa chừng.
    """
    if off < 0 or off + 4 > len(rom) or rom[off] != 0x10:
        return None
    size = rom[off + 1] | rom[off + 2] << 8 | rom[off + 3] << 16
    if size < 0x40 or size > maxsize:
        return None
    out = bytearray()
    p, n = off + 4, len(rom)
    while len(out) < size:
        if p >= n:
            return None
        flags = rom[p]
        p += 1
        for bit in range(8):
            if len(out) >= size:
                break
            if flags & (0x80 >> bit):
                if p + 1 >= n:
                    return None
                a, c = rom[p], rom[p + 1]
                p += 2
                length, disp = (a >> 4) + 3, ((a & 15) << 8 | c) + 1
                if disp > len(out):
                    return None
                for _ in range(length):
                    out.append(out[-disp])
                    if len(out) >= size:
                        break
            else:
                if p >= n:
                    return None
                out.append(rom[p])
                p += 1
    return bytes(out[:size]), p


def words_u32(rom):
    """Mảng u32 căn hàng 4 của ROM (little endian)."""
    return np.frombuffer(rom[: len(rom) // 4 * 4], dtype="<u4")


def is_rom_ptr(w, n):
    return ROM_BASE <= w < ROM_BASE + n


def string_starts(rom, a, b):
    """Offset đầu các chuỗi KHÔNG rỗng (kết thúc bằng 0xFF) trong [a, b)."""
    out, p = [], a
    while p < b:
        e = rom.find(b"\xff", p, b + 64)
        if e < 0:
            break
        if e > p:
            out.append(p)
        p = e + 1
    return out


def is_string_start(rom, t):
    """t là đầu chuỗi: ngay sau 0xFF và có 0xFF kết thúc trong 3000 byte."""
    n = len(rom)
    if t <= 0 or t >= n - 8 or rom[t - 1] != 0xFF:
        return False
    return rom.find(b"\xff", t, t + 3000) > t


_TXT = set([0] + list(range(0xA1, 0xFF)) + [0x1B, 0x1C, 0x1D, 0x1E, 0x1F])


def is_text_like(rom, t):
    """>=90% byte nằm trong tập ký tự của charmap tiếng Anh (dùng cho ROM GỐC)."""
    e = rom.find(b"\xff", t, t + 4000)
    if e <= t:
        return False
    seg = rom[t:e]
    return sum(1 for b in seg if b in _TXT) >= len(seg) * 0.9


def diff_clusters(orig, vie, gap=64):
    """Gom các byte khác nhau thành cụm (khoảng cách <= gap)."""
    d = np.nonzero(np.frombuffer(orig, np.uint8) != np.frombuffer(vie, np.uint8))[0]
    if len(d) == 0:
        return []
    cl, s, p = [], int(d[0]), int(d[0])
    for x in d[1:]:
        x = int(x)
        if x - p > gap:
            cl.append((s, p + 1))
            s = x
        p = x
    cl.append((s, p + 1))
    return cl


class ClusterIndex:
    def __init__(self, clusters):
        self.cl = clusters
        self.starts = [a for a, _ in clusters]

    def find(self, t):
        i = bisect.bisect_right(self.starts, t) - 1
        if i >= 0 and self.cl[i][0] <= t < self.cl[i][1]:
            return self.cl[i]
        return None
