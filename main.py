#!/usr/bin/env python3
"""Tuesday 24 November 2026 - The World in One Page.
Pure Python stdlib. Writes exactly one file: /output/entry.png (1024x1024).
No Pillow, no fonts from disk, no network. Deterministic output.
Bitmap 5x7 font defined in this file; PNG encoder written by hand.
"""
import binascii
import math
import os
import struct
import zlib

W = 1024
H = 1024

PAPER = (247, 243, 232)
INK = (18, 24, 38)
NAVY = (16, 42, 90)
NAVY2 = (28, 68, 140)
RED = (178, 34, 34)
GOLD = (184, 134, 11)
TEAL = (0, 110, 110)
GREEN = (34, 120, 60)
ORANGE = (200, 90, 20)
PURPLE = (110, 60, 160)
GREY = (90, 96, 108)
LIGHT = (232, 226, 210)
CARD = (255, 255, 255)
MAPSEA = (198, 222, 235)
MAPLAND = (226, 214, 178)
CREAM = (255, 244, 214)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGOLD = (150, 105, 0)

REGION_COLOR = {
    "EUROPE": (28, 68, 140),
    "MIDDLE EAST": (178, 34, 34),
    "ASIA": (200, 90, 20),
    "AFRICA": (34, 120, 60),
    "AMERICAS": (110, 60, 160),
    "OCEANIA": (0, 110, 110),
    "SPACE": (40, 40, 40),
}

# ---------------- 5x7 bitmap font ----------------
# Each glyph: 7 rows of 5 chars, '#' = ink, '.' = empty.
FONT = {
"A": ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
"B": ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
"C": ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
"D": ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
"E": ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
"F": ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
"G": ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
"H": ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
"I": ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
"J": ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
"K": ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
"L": ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
"M": ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
"N": ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
"O": ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
"P": ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
"Q": ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
"R": ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
"S": ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
"T": ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
"U": ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
"V": ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
"W": ("10001", "10001", "10001", "10101", "10101", "11011", "10001"),
"X": ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
"Y": ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
"Z": ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
"0": ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
"1": ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
"2": ("01110", "10001", "00001", "00110", "01000", "10000", "11111"),
"3": ("11110", "00001", "00001", "01110", "00001", "00001", "11110"),
"4": ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
"5": ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
"6": ("01110", "10000", "10000", "11110", "10001", "10001", "01110"),
"7": ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
"8": ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
"9": ("01110", "10001", "10001", "01111", "00001", "00001", "01110"),
"a": ("00000", "00000", "01110", "00001", "01111", "10001", "01111"),
"b": ("10000", "10000", "10110", "11001", "10001", "10001", "11110"),
"c": ("00000", "00000", "01110", "10000", "10000", "10001", "01110"),
"d": ("00001", "00001", "01101", "10011", "10001", "10001", "01111"),
"e": ("00000", "00000", "01110", "10001", "11111", "10000", "01110"),
"f": ("00110", "01001", "01000", "11110", "01000", "01000", "01000"),
"g": ("00000", "01111", "10001", "10001", "01111", "00001", "01110"),
"h": ("10000", "10000", "10110", "11001", "10001", "10001", "10001"),
"i": ("00100", "00000", "01100", "00100", "00100", "00100", "01110"),
"j": ("00010", "00000", "00110", "00010", "00010", "10010", "01100"),
"k": ("10000", "10000", "10010", "10100", "11000", "10100", "10010"),
"l": ("01100", "00100", "00100", "00100", "00100", "00100", "01110"),
"m": ("00000", "00000", "11010", "10101", "10101", "10101", "10101"),
"n": ("00000", "00000", "10110", "11001", "10001", "10001", "10001"),
"o": ("00000", "00000", "01110", "10001", "10001", "10001", "01110"),
"p": ("00000", "00000", "11110", "10001", "11110", "10000", "10000"),
"q": ("00000", "00000", "01101", "10011", "01111", "00001", "00001"),
"r": ("00000", "00000", "10110", "11001", "10000", "10000", "10000"),
"s": ("00000", "00000", "01111", "10000", "01110", "00001", "11110"),
"t": ("01000", "01000", "11100", "01000", "01000", "01001", "00110"),
"u": ("00000", "00000", "10001", "10001", "10001", "10011", "01101"),
"v": ("00000", "00000", "10001", "10001", "10001", "01010", "00100"),
"w": ("00000", "00000", "10001", "10101", "10101", "10101", "01010"),
"x": ("00000", "00000", "10001", "01010", "00100", "01010", "10001"),
"y": ("00000", "00000", "10001", "10001", "01111", "00001", "01110"),
"z": ("00000", "00000", "11111", "00010", "00100", "01000", "11111"),
" ": ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
".": ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
",": ("00000", "00000", "00000", "00000", "01100", "00100", "01000"),
":": ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
";": ("00000", "01100", "01100", "00000", "01100", "00100", "01000"),
"'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
'"': ("01010", "01010", "00000", "00000", "00000", "00000", "00000"),
"-": ("00000", "00000", "00000", "01110", "00000", "00000", "00000"),
"\u2013": ("00000", "00000", "00000", "01110", "00000", "00000", "00000"),
"\u2014": ("00000", "00000", "00000", "11111", "00000", "00000", "00000"),
"\u00b7": ("00000", "00000", "01100", "01100", "00000", "00000", "00000"),
"$": ("00100", "01111", "10100", "01110", "00101", "11110", "00100"),
"%": ("11001", "11010", "00010", "00100", "01000", "01011", "10011"),
"+": ("00000", "00100", "00100", "11111", "00100", "00100", "00000"),
"/": ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
"(": ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
")": ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
"[": ("01110", "01000", "01000", "01000", "01000", "01000", "01110"),
"]": ("01110", "00010", "00010", "00010", "00010", "00010", "01110"),
"~": ("00000", "00000", "01001", "10110", "00000", "00000", "00000"),
"\u2026": ("00000", "00000", "00000", "00000", "00000", "00000", "10101"),
"!": ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
"?": ("01110", "10001", "00001", "00110", "00100", "00000", "00100"),
"&": ("01100", "10010", "10100", "01000", "10101", "10010", "01101"),
}

def text_width(s, scale):
    return len(s) * 6 * scale

def wrap_text(s, max_width, scale):
    """Greedy word wrap; returns list of lines, each fits max_width."""
    cw = 6 * scale
    max_chars = max(1, max_width // cw)
    words = s.split(" ")
    lines = []
    cur = ""
    for w_ in words:
        if len(w_) > max_chars:
            if cur:
                lines.append(cur)
                cur = ""
            while len(w_) > max_chars:
                lines.append(w_[:max_chars])
                w_ = w_[max_chars:]
            cur = w_
            continue
        trial = w_ if not cur else cur + " " + w_
        if len(trial) <= max_chars:
            cur = trial
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines

def truncate_ellipsis(s, max_width, scale):
    cw = 6 * scale
    max_chars = max(1, max_width // cw)
    if len(s) <= max_chars:
        return s
    if max_chars <= 1:
        return "\u2026"
    return s[:max_chars - 1] + "\u2026"

# ---------------- framebuffer ----------------
FB = bytearray(W * H * 3)

def set_px(x, y, color):
    if 0 <= x < W and 0 <= y < H:
        i = (y * W + x) * 3
        FB[i] = color[0]
        FB[i + 1] = color[1]
        FB[i + 2] = color[2]

def fill_rect(x, y, w, h, color):
    x0 = max(0, x)
    y0 = max(0, y)
    x1 = min(W, x + w)
    y1 = min(H, y + h)
    if x1 <= x0 or y1 <= y0:
        return
    r, g, b = color
    for yy in range(y0, y1):
        base = (yy * W + x0) * 3
        for xx in range(x0, x1):
            i = base + (xx - x0) * 3
            FB[i] = r
            FB[i + 1] = g
            FB[i + 2] = b

def rect_outline(x, y, w, h, color, t=1):
    fill_rect(x, y, w, t, color)
    fill_rect(x, y + h - t, w, t, color)
    fill_rect(x, y, t, h, color)
    fill_rect(x + w - t, y, t, h, color)

def hline(x, y, w, color):
    fill_rect(x, y, w, 1, color)

def vline(x, y, h, color):
    fill_rect(x, y, 1, h, color)

def line(x0, y0, x1, y1, color):
    dx = abs(x1 - x0)
    dy = -abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx + dy
    while True:
        set_px(x0, y0, color)
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x0 += sx
        if e2 <= dx:
            err += dx
            y0 += sy

def circle_fill(cx, cy, r, color):
    for yy in range(cy - r, cy + r + 1):
        dy = yy - cy
        dx = int(math.sqrt(max(0, r * r - dy * dy)))
        fill_rect(cx - dx, yy, dx * 2 + 1, 1, color)

def circle_outline(cx, cy, r, color):
    x = 0
    y = r
    d = 3 - 2 * r
    while y >= x:
        for px, py in ((cx + x, cy + y), (cx - x, cy + y), (cx + x, cy - y),
                       (cx - x, cy - y), (cx + y, cy + x), (cx - y, cy + x),
                       (cx + y, cy - x), (cx - y, cy - x)):
            set_px(px, py, color)
        x += 1
        if d > 0:
            y -= 1
            d = d + 4 * (x - y) + 10
        else:
            d = d + 4 * x + 6

def ellipse_fill(cx, cy, rx, ry, color):
    for yy in range(cy - ry, cy + ry + 1):
        dy = (yy - cy) / float(ry) if ry else 0.0
        dx = int(rx * math.sqrt(max(0.0, 1.0 - dy * dy)))
        fill_rect(cx - dx, yy, dx * 2 + 1, 1, color)

def polygon_fill(points, color):
    if len(points) < 3:
        return
    ys = [p[1] for p in points]
    y0, y1 = min(ys), max(ys)
    n = len(points)
    for y in range(y0, y1 + 1):
        xs = []
        for i in range(n):
            x1, y1p = points[i]
            x2, y2p = points[(i + 1) % n]
            if (y1p <= y < y2p) or (y2p <= y < y1p):
                if y2p != y1p:
                    x = x1 + (y - y1p) * (x2 - x1) / (y2p - y1p)
                    xs.append(x)
        xs.sort()
        for k in range(0, len(xs) - 1, 2):
            xa = int(math.ceil(xs[k]))
            xb = int(math.floor(xs[k + 1]))
            if xb >= xa:
                fill_rect(xa, y, xb - xa + 1, 1, color)

def polygon_outline(points, color):
    n = len(points)
    for i in range(n):
        x1, y1 = points[i]
        x2, y2 = points[(i + 1) % n]
        line(x1, y1, x2, y2, color)

def draw_text(x, y, s, color, scale=1, bold=False):
    cx = x
    for ch in s:
        glyph = FONT.get(ch)
        if glyph is None:
            cx += 6 * scale
            continue
        for row in range(7):
            bits = glyph[row]
            for col in range(5):
                if bits[col] == "1":
                    for dy in range(scale):
                        for dx in range(scale):
                            set_px(cx + col * scale + dx, y + row * scale + dy, color)
                            if bold:
                                set_px(cx + col * scale + dx + 1, y + row * scale + dy, color)
        cx += 6 * scale
    return cx

def draw_text_right(x_right, y, s, color, scale=1, bold=False):
    draw_text(x_right - text_width(s, scale), y, s, color, scale, bold)

def draw_text_center(cx, y, s, color, scale=1, bold=False):
    draw_text(cx - text_width(s, scale) // 2, y, s, color, scale, bold)

# ---------------- PNG encoder ----------------
def png_chunk(kind, data):
    out = struct.pack(">I", len(data)) + kind + data
    out += struct.pack(">I", binascii.crc32(kind + data) & 0xFFFFFFFF)
    return out

def write_png(path):
    raw = bytearray()
    for y in range(H):
        raw.append(0)
        raw.extend(FB[y * W * 3:(y + 1) * W * 3])
    ihdr = struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0)
    png = b"\x89PNG\r\n\x1a\n"
    png += png_chunk(b"IHDR", ihdr)
    png += png_chunk(b"IDAT", zlib.compress(bytes(raw), 9))
    png += png_chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(png)
    return len(png)

# ---------------- DATA ----------------
# (num, headline, detail, region, lon, lat, source, claim)
STORIES = [
(1, "Sanofi buys Insmed for $41bn cash", "French drugmaker pays $175/share, a 46% premium, in the biggest biotech deal in ~3 years.", "EUROPE", 2.3, 48.9, "Reuters", False),
(2, "NATO vows to defend space after Russian nuclear-satellite reports", "Chief Mark Rutte: alliance will defend against any space threat; weapon could orbit next month.", "EUROPE", 4.35, 50.85, "BBC", True),
(3, "Israeli strikes kill at least 6 in Gaza on Tuesday", "Medics: 6 dead including 2 police officers, as strikes continue across the Strip.", "MIDDLE EAST", 34.5, 31.5, "Reuters", False),
(4, "Seoul +6.3%, Nikkei +3.9% as Asia rallies on Tuesday", "KOSPI jumps 6.3% and Nikkei 3.91% in the morning session after Wall Street's Monday rebound.", "ASIA", 127.0, 37.5, "FXStreet", False),
(5, "Germany first to access Ukraine's Delta combat system", "Berlin signs letter of intent; ministers also agree in principle on more interceptor missiles.", "EUROPE", 13.4, 52.5, "Kyiv Independent", False),
(6, "Russia fires 96 drones at Ukraine overnight; 73 downed", "64 were jet-powered Shaheds; a strike partly destroyed a five-storey building.", "EUROPE", 30.5, 50.4, "Ukrainska Pravda", False),
(7, "Ukrainian drones hit Lukoil refinery 1,500 km inside Russia", "Perm refinery and the Kaleykino pumping station in Tatarstan struck in one night.", "EUROPE", 56.3, 58.0, "Kyiv Independent", False),
(8, "UN: Gaza war erased 77 years of human development", "UN report says the war has undone 77 years of development gains in the territory.", "MIDDLE EAST", 34.4, 31.4, "UN News", False),
(9, "Iraq PM orders Baghdad to run Kurdish-area oilfields", "Order covers fields in Diyala, Kirkuk, Salahuddin and Nineveh after a smuggling probe.", "MIDDLE EAST", 44.4, 33.3, "Reuters", False),
(10, "China opens Tiangong station to first foreign astronaut", "Pakistani astronaut Zeeshan Ali to fly on Shenzhou-24, the station's first foreign crew member.", "ASIA", 100.3, 40.9, "Straits Times", False),
(11, "US blacklists Alibaba-owned firm over chip curbs", "Commerce adds 7 companies in Singapore, Thailand and Malaysia, incl. Apex Enterprise Solutions.", "ASIA", 120.2, 30.3, "Dow Jones", False),
(12, "Bitcoin drops below $60,000 on Tuesday", "BTC $59,904, down ~2% in 24h.", "AMERICAS", -77.0, 38.9, "CoinDesk", False),
(13, "FDA approves first drug for limb-girdle dystrophy", "BridgeBio's drug is the first approved treatment for limb-girdle muscular dystrophy.", "AMERICAS", -77.1, 39.0, "Principia", False),
(14, "US states sue Musk firms over Grok sexualised images", "Oregon and Virginia sue SpaceX over alleged Grok-generated child abuse images.", "AMERICAS", -122.4, 37.8, "IQMIA", True),
(15, "S&P 500 +4.73%, Nasdaq +6.51% in Monday rebound", "Dow +3.01% to 49,595; Nasdaq's jump is its best day since the April 2024 losing streak ended.", "AMERICAS", -74.0, 40.7, "ATFX", False),
(16, "US Army to detonate 9,500 lb of explosives in Iowa", "68 drums of lead azide, set for Wed.", "AMERICAS", -91.2, 40.8, "AP", False),
(17, "Russia warns Estonia moves 'on verge of open war'", "Moscow says Tallinn's actions risk triggering open war, in a sharp escalation of rhetoric.", "EUROPE", 24.7, 59.4, "10 Things", True),
(18, "Seven EU states back curbs on Russian visas", "Letter to von der Leyen and Costa seeks limits on Russians' travel, esp. for sports events.", "EUROPE", 4.4, 50.8, "Kyiv Independent", False),
(19, "German Ifo business sentiment improves in November", "Business climate keeps recovering in Europe's largest economy after years of weak growth.", "EUROPE", 13.4, 52.5, "Morningstar", False),
(20, "Hernandez de Cos tipped to succeed Lagarde at ECB", "Spain's former central-bank chief is the leading name to take over the ECB presidency.", "EUROPE", 8.7, 50.1, "Horizon", True),
(21, "Macron seeks French strategic rare-earth reserves", "President wants 'strategic reserves' of rare earths to cut dependence on foreign supply.", "EUROPE", 2.3, 48.9, "Horizon", False),
(22, "Solomon Islands to end security pact with China", "Pacific nation moves to end its security deal with Beijing, a win for Western allies.", "OCEANIA", 160.0, -9.4, "10 Things", False),
(23, "Brentford thrash Everton 4-0 in Premier League", "Brentford run riot at home; Everton concede 4 in a one-sided league night.", "EUROPE", -0.3, 51.5, "Sport's Home Ground", False),
(24, "Monza beat Fiorentina 3-0 in Serie A", "Monza deliver a dominant 3-0 win over Fiorentina in Italy's top flight.", "EUROPE", 9.3, 45.6, "Sport's Home Ground", False),
(25, "Lamine Yamal out with ankle injury for Barcelona", "Wonderkid ruled out with right ankle discomfort; misses the trip to Sabah.", "EUROPE", 2.2, 41.4, "ESPN", False),
(26, "Champions League night: Real-PSV, Arsenal-Dortmund, Feyenoord-Porto", "Matchday 5.", "EUROPE", -0.1, 51.55, "ESPN", False),
(27, "Gukesh-Sindarov chess title match opens in Geneva", "Both just 20, the youngest-ever pair fight a 14-game World Championship match.", "EUROPE", 6.1, 46.2, "Voice of Indian Sport", False),
(28, "Houthis say Saudi strike kills 17 in Hodeida", "Houthi officials report 17 dead in a Saudi airstrike on the Red Sea port city.", "MIDDLE EAST", 42.9, 14.8, "IQMIA", True),
(29, "Iran flogs singer Parastoo Ahmadi with 74 lashes", "Singer sentenced to 74 lashes in Iran in a case that drew condemnation abroad.", "MIDDLE EAST", 51.4, 35.7, "Horizon", False),
(30, "Iran rules out talks until US meets 7 conditions", "Tehran says no negotiation with Washington until seven preconditions are met.", "MIDDLE EAST", 51.4, 35.7, "Horizon", False),
(31, "Al-Wasl thrash Tractor 5-1 in AFC Champions League", "UAE side Al-Wasl rout Iran's Tractor 5-1 in Asian club football.", "MIDDLE EAST", 55.3, 25.2, "Sport's Home Ground", False),
(32, "Oxfam: Gaza now a 'toxic land'", "Aid group describes a territory transformed into a 'toxic land' by war and blockade.", "MIDDLE EAST", 34.5, 31.5, "Horizon", False),
(33, "UN Libya mission demands probe into Benghazi attacks", "UNSMIL calls for an independent investigation into Sunday's port and coastal attacks.", "MIDDLE EAST", 20.1, 32.1, "UN News", False),
(34, "Nepal hit by 5.6-magnitude quake near China border", "Quake strikes Koshi province, close to the Chinese border; no deaths confirmed yet.", "ASIA", 85.3, 27.7, "Horizon", False),
(35, "S. Korea alert as Russian jet enters its airspace", "Evacuation warning briefly issued for Ulleung island after a Russian aircraft intrusion.", "ASIA", 130.9, 37.5, "Reuters", False),
(36, "N. Korea may shut Swiss office in Pyongyang", "KCNA: Pyongyang to consider closing Switzerland's office after sanctions on a children's camp.", "ASIA", 125.75, 39.0, "KCNA", False),
(37, "BWF rankings: Satwik-Chirag, Sindhu at No. 6", "India hold top-10 spots in all 5 categories in the Week 48 world badminton rankings.", "ASIA", 77.2, 28.6, "Voice of Indian Sport", False),
(38, "Astronomers find most distant glowing black hole", "Quasar formed within 630 million years of the Big Bang, the earliest glowing black hole seen.", "SPACE", 179.0, 78.0, "Principia", False),
(39, "DRC fighting traps Ebola teams in Ituri for 24h+", "Heavy fighting near a hospital forces emergency teams to take cover for over 24 hours.", "AFRICA", 29.5, 1.5, "UN News", False),
(40, "CAS to rule Tuesday on Senegal AFCON title appeal", "Court decides in the afternoon whether Senegal keep a title CAF gave to Morocco.", "AFRICA", -17.4, 14.7, "Reuters", False),
(41, "Pyramids FC beat Al Ahly 2-0 in Egypt", "Pyramids keep a clean sheet to beat giants Al Ahly 2-0 in Cairo.", "AFRICA", 31.2, 30.0, "Sport's Home Ground", False),
(42, "Somalia, Uganda step up ops vs Al-Shabaab", "Both countries intensify joint operations as a troop withdrawal begins.", "AFRICA", 45.3, 2.0, "IQMIA", False),
(43, "Borno school enrolment nearly doubles after war", "Enrolment in Nigeria's Borno State nearly doubles despite violence and poverty.", "AFRICA", 13.2, 11.8, "Al Jazeera", False),
(44, "Pennsylvania reports 9th measles death of 2026", "Ninth death linked to the outbreak, which now affects 46 counties in the state.", "AMERICAS", -77.2, 40.3, "CBS News", False),
(45, "US consumer confidence + ADP jobs due Tuesday", "Conference Board confidence at 23:00 WIB; ADP weekly jobs at 21:15 WIB; core PCE on Wednesday.", "AMERICAS", -77.0, 38.9, "ATFX", False),
(46, "Dollar at 20-month high 104.33; gold $3,636.69", "DXY +0.47% near a 20-month high; gold +2.95% while Brent falls 3.45% to $89.39.", "AMERICAS", -74.0, 40.7, "ATFX", False),
(47, "Wembanyama scores 50 points in 18 minutes", "Spurs star's third career 50-point game, in just 18 minutes vs the Pelicans.", "AMERICAS", -98.5, 29.4, "ESPN", False),
(48, "Washington edge Bengals 22-20 on late Daniels drive", "Commanders win late again, ending Cincinnati's five-game winning run.", "AMERICAS", -77.0, 38.9, "ESPN", False),
(49, "Colombia car bomb wrecks buildings in Villavicencio", "Car bomb destroys buildings; no victims confirmed, President De la Espriella says.", "AMERICAS", -73.6, 4.15, "The Hindu", False),
(50, "Mexico to try 'El Chapo Isidro' despite US bid", "Mexico will prosecute the cartel figure at home despite a US extradition request.", "AMERICAS", -99.1, 19.4, "Horizon", False),
]

TIMELINE = [
("OVERNIGHT", "Russia fires 96 drones at Ukraine; 73 downed"),
("~06:10", "Sanofi announces $41bn Insmed takeover"),
("09:30", "Asia rallies: KOSPI +6.3%, Nikkei +3.9%"),
("~14:30", "CAS rules on Senegal's AFCON title appeal"),
("DAY", "Israeli strikes kill 6 in Gaza; UN: 77 yrs lost"),
("EVENING", "US consumer confidence + ADP jobs due"),
]

DATE_CHECK = ("DATE CHECK - left out on purpose because they broke BEFORE Tuesday 24 November 2026: "
"Nvidia reinstated Jensen Huang as CEO (announced Mon 23 Nov) - COP31 in Antalya collapsed with no fossil-fuel deal (Sun 22 Nov) - "
"CrowdStrike agreed a $43.9bn all-stock buy of Zscaler (Mon 23 Nov) - Ukraine sank the Russian corvette Merkury off Benghazi (Sun 23 Nov) - "
"ICJ ruled Myanmar committed genocide vs the Rohingya (last week) - Israeli strikes killed 3 in Gaza incl. an UNRWA worker (Mon 23 Nov) - "
"NATO said it would send AWACS aircraft to Poland (Mon 23 Nov) - US loses measles elimination status (Tue 17 Nov) - "
"Boca win Copa Sudamericana (Sat 21 Nov).")

NA = [(-168, 66), (-140, 70), (-125, 71), (-110, 68), (-95, 69), (-85, 66), (-80, 73), (-65, 62), (-55, 52), (-60, 46), (-70, 42), (-75, 35), (-80, 32), (-84, 30), (-90, 21), (-97, 26), (-105, 23), (-110, 24), (-117, 33), (-125, 40), (-125, 49), (-135, 58), (-150, 61), (-165, 60)]
SA = [(-80, 9), (-77, 4), (-80, -3), (-81, -6), (-77, -12), (-72, -18), (-70, -23), (-70, -30), (-72, -37), (-73, -44), (-70, -52), (-66, -55), (-65, -50), (-62, -42), (-57, -35), (-52, -32), (-48, -28), (-41, -23), (-39, -17), (-35, -9), (-35, -6), (-44, -3), (-50, 0), (-55, 5), (-60, 8), (-70, 11)]
EU = [(-10, 36), (-9, 43), (-2, 48), (-4, 50), (0, 51), (3, 53), (8, 57), (10, 59), (5, 60), (10, 62), (18, 69), (25, 71), (31, 70), (40, 68), (44, 66), (40, 60), (30, 60), (28, 56), (24, 58), (21, 55), (19, 54), (14, 54), (12, 45), (18, 40), (23, 36), (19, 42), (12, 44), (8, 44), (3, 43), (-2, 37)]
AF = [(-6, 35), (-10, 31), (-15, 27), (-17, 21), (-17, 15), (-15, 11), (-8, 5), (-4, 5), (2, 6), (6, 4), (9, 4), (9, 0), (12, -5), (13, -12), (12, -18), (16, -23), (18, -29), (20, -35), (26, -34), (32, -29), (35, -24), (40, -16), (40, -10), (42, -2), (46, 0), (51, 2), (51, 11), (44, 11), (40, 15), (37, 18), (35, 22), (32, 31), (22, 33), (11, 34), (10, 37), (0, 36)]
AS = [(40, 68), (50, 69), (60, 69), (70, 72), (80, 73), (90, 75), (100, 77), (110, 74), (120, 73), (130, 72), (140, 72), (150, 70), (158, 65), (162, 60), (158, 53), (150, 59), (142, 50), (140, 40), (135, 34), (130, 33), (127, 35), (122, 38), (120, 32), (122, 28), (118, 25), (110, 20), (108, 12), (105, 9), (100, 8), (98, 12), (95, 16), (92, 21), (89, 22), (86, 20), (80, 13), (77, 8), (75, 12), (72, 20), (66, 25), (61, 25), (57, 26), (52, 28), (50, 30), (48, 30), (44, 29), (43, 27), (40, 31), (36, 36), (30, 36), (27, 40), (23, 40), (26, 45), (28, 45), (30, 46), (32, 47), (34, 48), (38, 48), (40, 52), (40, 56), (44, 60), (40, 64)]
OC = [(113, -22), (114, -30), (115, -35), (124, -33), (129, -32), (135, -35), (140, -38), (145, -38), (150, -37), (153, -32), (153, -27), (146, -19), (142, -11), (137, -12), (135, -15), (132, -11), (130, -13), (126, -14), (122, -17), (118, -20), (113, -22), (130, -3), (136, -4), (141, -6), (146, -8), (150, -9), (155, -9), (160, -10), (162, -11), (166, -15), (168, -17), (170, -20), (174, -37), (178, -38), (175, -41), (172, -43), (168, -47), (167, -45), (173, -41), (177, -38)]
CONTINENTS = [NA, SA, EU, AF, AS, OC]

# ---------------- illustrations ----------------
LABELS = {1: "$41bn", 2: "SPACE", 3: "6 KILLED", 4: "+6.3%", 5: "DELTA",
          6: "96 DRONES", 7: "1,500 km", 8: "-77 YEARS", 9: "4 PROVINCES",
          10: "TIANGONG", 11: "7 FIRMS", 12: "-2%", 13: "1st DRUG",
          14: "2 STATES SUE", 15: "+4.73%", 16: "9,500 lb"}

def starburst(cx, cy, r_out, r_in, spikes, color):
    pts = []
    for i in range(spikes * 2):
        ang = math.pi * i / spikes
        r = r_out if i % 2 == 0 else r_in
        pts.append((int(cx + r * math.cos(ang)), int(cy + r * math.sin(ang))))
    polygon_fill(pts, color)

def chart_up(x, y, w, h, color):
    pts = [(x + 4, y + h - 12), (x + w // 3, y + h - 22),
           (x + w // 2, y + h - 16), (x + 2 * w // 3, y + 14),
           (x + w - 6, y + 8)]
    for i in range(len(pts) - 1):
        line(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], color)
        line(pts[i][0], pts[i][1] + 1, pts[i + 1][0], pts[i + 1][1] + 1, color)
    line(x + 4, y + 8, x + 4, y + h - 8, GREY)
    line(x + 4, y + h - 8, x + w - 4, y + h - 8, GREY)
    for px, py in pts:
        circle_fill(px, py, 2, color)

def draw_illo(num, x, y, w, h, with_label):
    cx = x + w // 2
    cy = y + h // 2
    dark = num in (2, 10)
    bg = (10, 20, 50) if dark else (238, 233, 218)
    fill_rect(x, y, w, h, bg)
    label = LABELS.get(num, "") if with_label else ""
    ly = y + h - 11
    if num == 1:
        # pill / capsule, red + white halves
        fill_rect(cx - 26, cy - 9, 52, 18, WHITE)
        circle_fill(cx - 26, cy, 9, RED)
        circle_fill(cx + 26, cy, 9, WHITE)
        fill_rect(cx - 26, cy - 9, 26, 18, RED)
        circle_fill(cx - 26, cy, 9, RED)
        rect_outline(cx - 26, cy - 9, 52, 18, INK, 1)
        circle_outline(cx - 26, cy, 9, INK)
        circle_outline(cx + 26, cy, 9, INK)
        line(cx, cy - 9, cx, cy + 9, INK)
    elif num in (2, 10):
        for sx, sy in ((6, 5), (w - 8, 8), (12, h - 12), (w - 14, h - 8), (w // 2, 6), (w - 20, h // 2)):
            set_px(x + sx, y + sy, WHITE)
            set_px(x + sx + 1, y + sy, WHITE)
        fill_rect(cx - 34, cy - 8, 24, 16, (40, 90, 180))
        fill_rect(cx + 10, cy - 8, 24, 16, (40, 90, 180))
        fill_rect(cx - 10, cy - 10, 20, 20, GOLD)
        fill_rect(cx - 6, cy - 4, 12, 8, (255, 220, 120))
        circle_outline(cx, cy + 16, 5, WHITE)
        line(cx, cy + 10, cx, cy + 12, WHITE)
    elif num in (3, 16):
        starburst(cx, cy - 2, 26, 12, 8, ORANGE)
        starburst(cx, cy - 2, 17, 8, 8, RED)
        circle_fill(cx, cy - 2, 7, (255, 210, 0))
    elif num in (4, 12, 15):
        chart_up(x, y, w, h, GREEN if num != 12 else RED)
    elif num == 5:
        for r in (24, 17, 10):
            circle_outline(cx, cy - 2, r, GREEN)
        line(cx, cy - 2, cx + 22, cy - 12, GREEN)
        line(cx, cy - 2, cx - 20, cy + 6, GREEN)
        circle_fill(cx + 12, cy + 8, 3, RED)
        circle_fill(cx - 8, cy - 12, 3, RED)
        circle_fill(cx, cy - 2, 3, INK)
    elif num == 6:
        fill_rect(cx - 16, cy - 6, 32, 12, GREY)
        fill_rect(cx - 5, cy - 12, 10, 24, (60, 64, 72))
        for dx, dy in ((-20, -12), (20, -12), (-20, 12), (20, 12)):
            circle_outline(cx + dx, cy + dy, 6, INK)
            line(cx + dx - 8, cy + dy, cx + dx + 8, cy + dy, INK)
        circle_fill(cx, cy, 3, RED)
    elif num == 7:
        fill_rect(cx - 24, cy + 2, 18, 16, GREY)
        fill_rect(cx - 2, cy + 2, 18, 16, (120, 124, 132))
        ellipse_fill(cx - 15, cy + 2, 9, 4, (160, 164, 172))
        ellipse_fill(cx + 7, cy + 2, 9, 4, (160, 164, 172))
        pts = [(cx + 26, cy - 4), (cx + 32, cy - 18), (cx + 38, cy - 4)]
        polygon_fill(pts, ORANGE)
        polygon_fill([(cx + 29, cy - 4), (cx + 32, cy - 12), (cx + 35, cy - 4)], RED)
        fill_rect(cx - 26, cy + 18, 56, 3, INK)
    elif num == 8:
        polygon_fill([(cx - 26, cy + 14), (cx - 10, cy - 12), (cx + 2, cy + 14)], (150, 154, 162))
        polygon_fill([(cx + 2, cy + 14), (cx + 14, cy - 4), (cx + 28, cy + 14)], (120, 124, 132))
        line(cx - 26, cy + 14, cx + 28, cy + 14, RED)
        line(cx - 26, cy + 14, cx + 28, cy + 14, RED)
        fill_rect(cx - 8, cy - 2, 16, 3, RED)
    elif num == 9:
        line(cx - 20, cy + 18, cx, cy - 18, INK)
        line(cx + 20, cy + 18, cx, cy - 18, INK)
        line(cx - 14, cy + 6, cx + 14, cy + 6, INK)
        line(cx - 8, cy - 6, cx + 8, cy - 6, INK)
        fill_rect(cx - 24, cy + 18, 48, 4, INK)
        circle_fill(cx, cy - 20, 3, RED)
    elif num == 11:
        rect_outline(cx - 18, cy - 14, 36, 28, GOLD, 2)
        fill_rect(cx - 10, cy - 6, 20, 12, GOLD)
        for dx in (-18, -9, 0, 9):
            vline(cx + dx, cy - 20, 6, GOLD)
            vline(cx + dx, cy + 14, 6, GOLD)
    elif num == 13:
        line(cx - 10, cy - 18, cx - 10, cy + 16, TEAL)
        line(cx + 10, cy - 18, cx + 10, cy + 16, TEAL)
        for dy in (-12, -4, 4, 12):
            line(cx - 10, cy + dy, cx + 10, cy + dy, TEAL)
        circle_fill(cx - 10, cy - 12, 3, RED)
        circle_fill(cx + 10, cy - 4, 3, RED)
        circle_fill(cx - 10, cy + 4, 3, RED)
        circle_fill(cx + 10, cy + 12, 3, RED)
    elif num == 14:
        fill_rect(cx - 16, cy - 14, 32, 24, (200, 204, 212))
        rect_outline(cx - 16, cy - 14, 32, 24, INK, 1)
        line(cx, cy - 14, cx, cy - 22, INK)
        circle_fill(cx, cy - 23, 3, RED)
        circle_fill(cx - 8, cy - 4, 4, RED)
        circle_fill(cx + 8, cy - 4, 4, RED)
        fill_rect(cx - 10, cy + 6, 20, 3, INK)
    else:
        chart_up(x, y, w, h, GREEN)
    if label:
        lc = WHITE if dark else INK
        draw_text_center(cx, ly, label, lc, 1, True)

# ---------------- layout ----------------
def first_sentence(detail):
    i = detail.find(".")
    if i >= 0:
        return detail[:i + 1]
    return detail

def draw_masthead():
    fill_rect(0, 0, W, 104, NAVY)
    fill_rect(0, 104, W, 4, GOLD)
    draw_text(14, 12, "THE WORLD IN ONE PAGE  |  THE DAILY BRIEFING", (200, 210, 235), 1, True)
    draw_text_right(1010, 12, "No. 328", (200, 210, 235), 1, True)
    draw_text(14, 28, "TUESDAY 24 NOVEMBER 2026", WHITE, 5, True)
    draw_text(14, 72, "50 STORIES  \u00b7  7 REGIONS  \u00b7  ALL SOURCED  \u00b7  DATE-CHECKED", GOLD, 2, True)
    draw_text(14, 92, "EUROPE 15  \u00b7  MIDDLE EAST 9  \u00b7  ASIA 7  \u00b7  AFRICA 5  \u00b7  AMERICAS 12  \u00b7  OCEANIA 1  \u00b7  SPACE 1", WHITE, 1, True)
    draw_text(14, 112, "50 sourced stories, a UTC timeline and a date check \u2014 24 November 2026", INK, 1, True)

def draw_timeline():
    fill_rect(14, 132, 996, 40, CARD)
    rect_outline(14, 132, 996, 40, NAVY, 1)
    draw_text(22, 147, "UTC", NAVY, 1, True)
    draw_text(22, 156, "TIMELINE", NAVY, 1, True)
    sx = 104
    slot_w = (1010 - sx) // 6
    for i, (t, ev) in enumerate(TIMELINE):
        x = sx + i * slot_w
        if i > 0:
            vline(x, 136, 32, LIGHT)
        draw_text(x + 6, 138, t, RED, 1, True)
        lines = wrap_text(ev, slot_w - 12, 1)[:2]
        for j, ln in enumerate(lines):
            draw_text(x + 6, 148 + j * 9, ln, INK, 1, False)

def draw_hero():
    for idx, st in enumerate(STORIES[:4]):
        num, headline, detail, region, lon, lat, source, claim = st
        x = 14 + idx * 250
        y = 182
        w, h = 244, 148
        rc = REGION_COLOR[region]
        fill_rect(x, y, w, h, CARD)
        rect_outline(x, y, w, h, rc, 2)
        fill_rect(x, y, w, 22, rc)
        draw_text(x + 8, y + 7, str(num) + "  " + region, WHITE, 1, True)
        draw_illo(num, x + 2, y + 24, w - 4, 58, True)
        lines = wrap_text(headline, w - 12, 1)[:2]
        for j, ln in enumerate(lines):
            draw_text(x + 6, y + 88 + j * 9, ln, INK, 1, True)
        det = truncate_ellipsis(detail, w - 12, 1)
        draw_text(x + 6, y + 108, det, (60, 64, 72), 1, False)
        src = "Source: " + source
        if claim:
            src += "  [CLAIM]"
        draw_text(x + 6, y + 128, truncate_ellipsis(src, w - 12, 1), GREY, 1, False)

def draw_small():
    for idx, st in enumerate(STORIES[4:16]):
        num, headline, detail, region, lon, lat, source, claim = st
        col = idx % 4
        row = idx // 4
        x = 14 + col * 250
        y = 338 + row * 60
        w, h = 244, 56
        rc = REGION_COLOR[region]
        fill_rect(x, y, w, h, CARD)
        rect_outline(x, y, w, h, rc, 1)
        draw_illo(num, x + 1, y + 1, 54, h - 2, False)
        tx = x + 60
        tw = w - 66
        head = str(num) + ". " + headline
        lines = wrap_text(head, tw, 1)[:2]
        for j, ln in enumerate(lines):
            draw_text(tx, y + 4 + j * 9, ln, INK, 1, True)
        draw_text(tx, y + 24, truncate_ellipsis(detail, tw, 1), (60, 64, 72), 1, False)
        draw_text(tx, y + 36, truncate_ellipsis(source + (" [CLAIM]" if claim else ""), tw, 1), GREY, 1, False)

MAP_X, MAP_Y, MAP_W, MAP_H = 22, 544, 980, 146

def project(lon, lat):
    px = MAP_X + (lon + 180.0) / 360.0 * MAP_W
    py = MAP_Y + (90.0 - lat) / 180.0 * MAP_H
    return int(px), int(py)

def draw_map():
    fill_rect(14, 522, 996, 172, CARD)
    rect_outline(14, 522, 996, 172, NAVY, 1)
    draw_text(22, 528, "WHERE IT HAPPENED \u2014 numbered pins 1-50", NAVY, 1, True)
    lx = 470
    for name in ("EUROPE", "MIDDLE EAST", "ASIA", "AFRICA", "AMERICAS", "OCEANIA", "SPACE"):
        circle_fill(lx + 4, 531, 3, REGION_COLOR[name])
        draw_text(lx + 10, 528, name, INK, 1, False)
        lx += 10 + text_width(name, 1) + 10
    fill_rect(MAP_X, MAP_Y, MAP_W, MAP_H, MAPSEA)
    rect_outline(MAP_X, MAP_Y, MAP_W, MAP_H, (150, 160, 170), 1)
    for poly in CONTINENTS:
        pts = [project(lon, lat) for lon, lat in poly]
        polygon_fill(pts, MAPLAND)
        polygon_outline(pts, (180, 165, 120))
    for st in STORIES:
        num, headline, detail, region, lon, lat, source, claim = st
        rc = REGION_COLOR[region]
        if num == 38:
            px, py = 984, 556
            circle_fill(px, py, 5, rc)
            circle_outline(px, py, 5, WHITE)
            draw_text(906, 552, "38 SPACE", INK, 1, True)
            continue
        px, py = project(lon, lat)
        px = max(MAP_X + 8, min(MAP_X + MAP_W - 8, px))
        py = max(MAP_Y + 8, min(MAP_Y + MAP_H - 8, py))
        if num <= 16:
            circle_fill(px, py, 7, rc)
            circle_outline(px, py, 7, WHITE)
            s = str(num)
            draw_text(px - text_width(s, 1) // 2, py - 3, s, WHITE, 1, True)
        else:
            circle_fill(px, py, 5, rc)
            circle_outline(px, py, 5, WHITE)

def draw_briefs():
    draw_text(14, 700, "THE OTHER 34 STORIES \u2014 17-50, ONE LINE EACH", NAVY, 1, True)
    fill_rect(14, 712, 996, 2, NAVY)
    for i, st in enumerate(STORIES[16:]):
        num, headline, detail, region, lon, lat, source, claim = st
        col = 0 if i < 17 else 1
        row = i if i < 17 else i - 17
        x = 14 if col == 0 else 524
        wdt = 500 if col == 0 else 486
        y = 720 + row * 14
        txt = str(num) + ". " + headline + " \u2014 " + first_sentence(detail) + " (" + source + (" [CLAIM]" if claim else "") + ")"
        draw_text(x, y, truncate_ellipsis(txt, wdt, 1), INK, 1, False)

def draw_footer():
    fill_rect(14, 962, 996, 54, CREAM)
    rect_outline(14, 962, 996, 54, RED, 2)
    lines = wrap_text(DATE_CHECK, 972, 1)
    for j, ln in enumerate(lines):
        draw_text(22, 968 + j * 9, ln, INK, 1, False)
    return len(lines)

def main():
    fill_rect(0, 0, W, H, PAPER)
    draw_masthead()
    draw_timeline()
    draw_hero()
    draw_small()
    draw_map()
    draw_briefs()
    nlines = draw_footer()
    outdir = "/output"
    os.makedirs(outdir, exist_ok=True)
    # clean contents only - never remove the folder itself
    for name in os.listdir(outdir):
        p = os.path.join(outdir, name)
        if os.path.isfile(p):
            os.remove(p)
    size = write_png(os.path.join(outdir, "entry.png"))
    print("footer lines: %d" % nlines)
    print("wrote /output/entry.png %d bytes" % size)

if __name__ == "__main__":
    main()
