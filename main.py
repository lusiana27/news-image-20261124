#!/usr/bin/env python3
"""news-image-20261124: draw one 1024x1024 PNG summing up Tuesday 24 Nov 2026.

Fresh build for make.fun competition news-image-20261124.
Writes exactly one image to /output/entry.png. No network at runtime.
Deterministic: same input bytes -> same output bytes.
"""
import os
import shutil
from PIL import Image, ImageDraw, ImageFont

OUT_DIR = "/output"
OUT_PATH = os.path.join(OUT_DIR, "entry.png")
W, H = 1024, 1024

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
F_BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
F_REG = os.path.join(FONT_DIR, "DejaVuSans.ttf")

# ---------------------------------------------------------------- palette
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

REGION_COLORS = {
    "EUROPE": (28, 68, 140),
    "MIDDLE EAST": (178, 34, 34),
    "ASIA": (200, 90, 20),
    "AFRICA": (34, 120, 60),
    "AMERICAS": (110, 60, 160),
    "OCEANIA": (0, 110, 110),
    "SPACE": (40, 40, 40),
}

# ---------------------------------------------------------------- data
# (num, headline, detail with a concrete number, region, lon, lat, source, claim?)
STORIES = [
    (1, "Sanofi buys Insmed for $41bn cash",
     "French drugmaker pays $175/share, a 46% premium, in the biggest biotech deal in ~3 years.",
     "EUROPE", 2.3, 48.9, "Reuters", False),
    (2, "NATO vows to defend space after Russian nuclear-satellite reports",
     "Chief Mark Rutte: alliance will defend against any space threat; weapon could orbit next month.",
     "EUROPE", 4.35, 50.85, "BBC", True),
    (3, "Israeli strikes kill at least 6 in Gaza on Tuesday",
     "Medics: 6 dead including 2 police officers, as strikes continue across the Strip.",
     "MIDDLE EAST", 34.5, 31.5, "Reuters", False),
    (4, "Seoul +6.3%, Nikkei +3.9% as Asia rallies on Tuesday",
     "KOSPI jumps 6.3% and Nikkei 3.91% in the morning session after Wall Street's Monday rebound.",
     "ASIA", 127.0, 37.5, "FXStreet", False),
    (5, "Germany first to access Ukraine's Delta combat system",
     "Berlin signs letter of intent; ministers also agree in principle on more interceptor missiles.",
     "EUROPE", 13.4, 52.5, "Kyiv Independent", False),
    (6, "Russia fires 96 drones at Ukraine overnight; 73 downed",
     "64 were jet-powered Shaheds; a strike partly destroyed a five-storey building.",
     "EUROPE", 30.5, 50.4, "Ukrainska Pravda", False),
    (7, "Ukrainian drones hit Lukoil refinery 1,500 km inside Russia",
     "Perm refinery and the Kaleykino pumping station in Tatarstan struck in one night.",
     "EUROPE", 56.3, 58.0, "Kyiv Independent", False),
    (8, "UN: Gaza war erased 77 years of human development",
     "UN report says the war has undone 77 years of development gains in the territory.",
     "MIDDLE EAST", 34.4, 31.4, "UN News", False),
    (9, "Iraq PM orders Baghdad to run Kurdish-area oilfields",
     "Order covers fields in Diyala, Kirkuk, Salahuddin and Nineveh after a smuggling probe.",
     "MIDDLE EAST", 44.4, 33.3, "Reuters", False),
    (10, "China opens Tiangong station to first foreign astronaut",
     "Pakistani astronaut Zeeshan Ali to fly on Shenzhou-24, the station's first foreign crew member.",
     "ASIA", 100.3, 40.9, "Straits Times", False),
    (11, "US blacklists Alibaba-owned firm over chip curbs",
     "Commerce adds 7 companies in Singapore, Thailand and Malaysia, incl. Apex Enterprise Solutions.",
     "ASIA", 120.2, 30.3, "Dow Jones", False),
    (12, "Bitcoin drops below $60,000 on Tuesday",
     "BTC $59,904, down ~2% in 24h.",
     "AMERICAS", -77.0, 38.9, "CoinDesk", False),
    (13, "FDA approves first drug for limb-girdle dystrophy",
     "BridgeBio's drug is the first approved treatment for limb-girdle muscular dystrophy.",
     "AMERICAS", -77.1, 39.0, "Principia", False),
    (14, "US states sue Musk firms over Grok sexualised images",
     "Oregon and Virginia sue SpaceX over alleged Grok-generated child abuse images.",
     "AMERICAS", -122.4, 37.8, "IQMIA", True),
    (15, "S&P 500 +4.73%, Nasdaq +6.51% in Monday rebound",
     "Dow +3.01% to 49,595; Nasdaq's jump is its best day since the April 2024 losing streak ended.",
     "AMERICAS", -74.0, 40.7, "ATFX", False),
    (16, "US Army to detonate 9,500 lb of explosives in Iowa",
     "68 drums of lead azide, set for Wed.",
     "AMERICAS", -91.2, 40.8, "AP", False),
    (17, "Russia warns Estonia moves 'on verge of open war'",
     "Moscow says Tallinn's actions risk triggering open war, in a sharp escalation of rhetoric.",
     "EUROPE", 24.7, 59.4, "10 Things", True),
    (18, "Seven EU states back curbs on Russian visas",
     "Letter to von der Leyen and Costa seeks limits on Russians' travel, esp. for sports events.",
     "EUROPE", 4.4, 50.8, "Kyiv Independent", False),
    (19, "German Ifo business sentiment improves in November",
     "Business climate keeps recovering in Europe's largest economy after years of weak growth.",
     "EUROPE", 13.4, 52.5, "Morningstar", False),
    (20, "Hernandez de Cos tipped to succeed Lagarde at ECB",
     "Spain's former central-bank chief is the leading name to take over the ECB presidency.",
     "EUROPE", 8.7, 50.1, "Horizon", True),
    (21, "Macron seeks French strategic rare-earth reserves",
     "President wants 'strategic reserves' of rare earths to cut dependence on foreign supply.",
     "EUROPE", 2.3, 48.9, "Horizon", False),
    (22, "Solomon Islands to end security pact with China",
     "Pacific nation moves to end its security deal with Beijing, a win for Western allies.",
     "OCEANIA", 160.0, -9.4, "10 Things", False),
    (23, "Brentford thrash Everton 4-0 in Premier League",
     "Brentford run riot at home; Everton concede 4 in a one-sided league night.",
     "EUROPE", -0.3, 51.5, "Sport's Home Ground", False),
    (24, "Monza beat Fiorentina 3-0 in Serie A",
     "Monza deliver a dominant 3-0 win over Fiorentina in Italy's top flight.",
     "EUROPE", 9.3, 45.6, "Sport's Home Ground", False),
    (25, "Lamine Yamal out with ankle injury for Barcelona",
     "Wonderkid ruled out with right ankle discomfort; misses the trip to Sabah.",
     "EUROPE", 2.2, 41.4, "ESPN", False),
    (26, "Champions League night: Real-PSV, Arsenal-Dortmund, Feyenoord-Porto",
     "Matchday 5.",
     "EUROPE", -0.1, 51.55, "ESPN", False),
    (27, "Gukesh-Sindarov chess title match opens in Geneva",
     "Both just 20, the youngest-ever pair fight a 14-game World Championship match.",
     "EUROPE", 6.1, 46.2, "Voice of Indian Sport", False),
    (28, "Houthis say Saudi strike kills 17 in Hodeida",
     "Houthi officials report 17 dead in a Saudi airstrike on the Red Sea port city.",
     "MIDDLE EAST", 42.9, 14.8, "IQMIA", True),
    (29, "Iran flogs singer Parastoo Ahmadi with 74 lashes",
     "Singer sentenced to 74 lashes in Iran in a case that drew condemnation abroad.",
     "MIDDLE EAST", 51.4, 35.7, "Horizon", False),
    (30, "Iran rules out talks until US meets 7 conditions",
     "Tehran says no negotiation with Washington until seven preconditions are met.",
     "MIDDLE EAST", 51.4, 35.7, "Horizon", False),
    (31, "Al-Wasl thrash Tractor 5-1 in AFC Champions League",
     "UAE side Al-Wasl rout Iran's Tractor 5-1 in Asian club football.",
     "MIDDLE EAST", 55.3, 25.2, "Sport's Home Ground", False),
    (32, "Oxfam: Gaza now a 'toxic land'",
     "Aid group describes a territory transformed into a 'toxic land' by war and blockade.",
     "MIDDLE EAST", 34.5, 31.5, "Horizon", False),
    (33, "UN Libya mission demands probe into Benghazi attacks",
     "UNSMIL calls for an independent investigation into Sunday's port and coastal attacks.",
     "MIDDLE EAST", 20.1, 32.1, "UN News", False),
    (34, "Nepal hit by 5.6-magnitude quake near China border",
     "Quake strikes Koshi province, close to the Chinese border; no deaths confirmed yet.",
     "ASIA", 85.3, 27.7, "Horizon", False),
    (35, "S. Korea alert as Russian jet enters its airspace",
     "Evacuation warning briefly issued for Ulleung island after a Russian aircraft intrusion.",
     "ASIA", 130.9, 37.5, "Reuters", False),
    (36, "N. Korea may shut Swiss office in Pyongyang",
     "KCNA: Pyongyang to consider closing Switzerland's office after sanctions on a children's camp.",
     "ASIA", 125.75, 39.0, "KCNA", False),
    (37, "BWF rankings: Satwik-Chirag, Sindhu at No. 6",
     "India hold top-10 spots in all 5 categories in the Week 48 world badminton rankings.",
     "ASIA", 77.2, 28.6, "Voice of Indian Sport", False),
    (38, "Astronomers find most distant glowing black hole",
     "Quasar formed within 630 million years of the Big Bang, the earliest glowing black hole seen.",
     "SPACE", 179.0, 78.0, "Principia", False),
    (39, "DRC fighting traps Ebola teams in Ituri for 24h+",
     "Heavy fighting near a hospital forces emergency teams to take cover for over 24 hours.",
     "AFRICA", 29.5, 1.5, "UN News", False),
    (40, "CAS to rule Tuesday on Senegal AFCON title appeal",
     "Court decides in the afternoon whether Senegal keep a title CAF gave to Morocco.",
     "AFRICA", -17.4, 14.7, "Reuters", False),
    (41, "Pyramids FC beat Al Ahly 2-0 in Egypt",
     "Pyramids keep a clean sheet to beat giants Al Ahly 2-0 in Cairo.",
     "AFRICA", 31.2, 30.0, "Sport's Home Ground", False),
    (42, "Somalia, Uganda step up ops vs Al-Shabaab",
     "Both countries intensify joint operations as a troop withdrawal begins.",
     "AFRICA", 45.3, 2.0, "IQMIA", False),
    (43, "Borno school enrolment nearly doubles after war",
     "Enrolment in Nigeria's Borno State nearly doubles despite violence and poverty.",
     "AFRICA", 13.2, 11.8, "Al Jazeera", False),
    (44, "Pennsylvania reports 9th measles death of 2026",
     "Ninth death linked to the outbreak, which now affects 46 counties in the state.",
     "AMERICAS", -77.2, 40.3, "CBS News", False),
    (45, "US consumer confidence + ADP jobs due Tuesday",
     "Conference Board confidence at 23:00 WIB; ADP weekly jobs at 21:15 WIB; core PCE on Wednesday.",
     "AMERICAS", -77.0, 38.9, "ATFX", False),
    (46, "Dollar at 20-month high 104.33; gold $3,636.69",
     "DXY +0.47% near a 20-month high; gold +2.95% while Brent falls 3.45% to $89.39.",
     "AMERICAS", -74.0, 40.7, "ATFX", False),
    (47, "Wembanyama scores 50 points in 18 minutes",
     "Spurs star's third career 50-point game, in just 18 minutes vs the Pelicans.",
     "AMERICAS", -98.5, 29.4, "ESPN", False),
    (48, "Washington edge Bengals 22-20 on late Daniels drive",
     "Commanders win late again, ending Cincinnati's five-game winning run.",
     "AMERICAS", -77.0, 38.9, "ESPN", False),
    (49, "Colombia car bomb wrecks buildings in Villavicencio",
     "Car bomb destroys buildings; no victims confirmed, President De la Espriella says.",
     "AMERICAS", -73.6, 4.15, "The Hindu", False),
    (50, "Mexico to try 'El Chapo Isidro' despite US bid",
     "Mexico will prosecute the cartel figure at home despite a US extradition request.",
     "AMERICAS", -99.1, 19.4, "Horizon", False),
]

TIMELINE = [
    ("OVERNIGHT", "Russia fires 96 drones at Ukraine; 73 downed"),
    ("~06:10", "Sanofi announces $41bn Insmed takeover"),
    ("09:30", "Asia rallies: KOSPI +6.3%, Nikkei +3.9%"),
    ("~14:30", "CAS rules on Senegal's AFCON title appeal"),
    ("DAY", "Israeli strikes kill 6 in Gaza; UN: 77 yrs lost"),
    ("EVENING", "US consumer confidence + ADP jobs due"),
]

DATE_CHECK = (
    "DATE CHECK - left out on purpose because they broke BEFORE Tuesday 24 November 2026: "
    "Nvidia reinstated Jensen Huang as CEO (announced Mon 23 Nov) - "
    "COP31 in Antalya collapsed with no fossil-fuel deal (Sun 22 Nov) - "
    "CrowdStrike agreed a $43.9bn all-stock buy of Zscaler (Mon 23 Nov) - "
    "Ukraine sank the Russian corvette Merkury off Benghazi (Sun 23 Nov) - "
    "ICJ ruled Myanmar committed genocide vs the Rohingya (last week) - "
    "Israeli strikes killed 3 in Gaza incl. an UNRWA worker (Mon 23 Nov) - "
    "NATO said it would send AWACS aircraft to Poland (Mon 23 Nov) - "
    "US loses measles elimination status (Tue 17 Nov) - "
    "Boca win Copa Sudamericana (Sat 21 Nov)."
)

# ---------------------------------------------------------------- fonts
def font(bold, size):
    return ImageFont.truetype(F_BOLD if bold else F_REG, size)


def wrap(draw, text, fnt, width):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_center(draw, x, y, s, fnt, fill):
    draw.text((x, y), s, font=fnt, fill=fill, anchor="ma")


def draw_text(draw, x, y, s, fnt, fill):
    draw.text((x, y), s, font=fnt, fill=fill)

# ---------------------------------------------------------------- illustrations
def ill_pill(d, x, y, w, h, c1, c2, label=True):
    d.rounded_rectangle([x + 6, y + h // 2 - 14, x + w - 6, y + h // 2 + 14], 14, fill=c1, outline=INK, width=2)
    d.line([x + w // 2, y + h // 2 - 14, x + w // 2, y + h // 2 + 14], fill=INK, width=2)
    d.ellipse([x + w - 26, y + 6, x + w - 8, y + 24], fill=GOLD, outline=INK, width=2)
    if label:
        draw_text(d, x + 10, y + h - 18, "$41bn", font(True, 11), INK)


def ill_satellite(d, x, y, w, h, c1, c2, label=True):
    d.ellipse([x + 4, y + 4, x + w - 4, y + h - 4], fill=(12, 20, 44))
    for sx, sy in [(x + 16, y + 14), (x + w - 22, y + 20), (x + 24, y + h - 16), (x + w - 16, y + h - 22)]:
        d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 255, 255))
    d.rectangle([x + w // 2 - 26, y + h // 2 - 5, x + w // 2 - 8, y + h // 2 + 5], fill=c1, outline=INK, width=1)
    d.rectangle([x + w // 2 + 8, y + h // 2 - 5, x + w // 2 + 26, y + h // 2 + 5], fill=c1, outline=INK, width=1)
    d.rectangle([x + w // 2 - 8, y + h // 2 - 9, x + w // 2 + 8, y + h // 2 + 9], fill=GOLD, outline=INK, width=1)
    d.line([x + w // 2 - 8, y + h // 2 - 9, x + w // 2 + 14, y + h // 2 - 24], fill=RED, width=2)


def ill_blast(d, x, y, w, h, c1, c2, label=True):
    d.rectangle([x, y, x + w, y + h], fill=(60, 52, 44))
    d.polygon([(x + w // 2, y + 8), (x + w // 2 + 12, y + h // 2 - 6), (x + w - 10, y + h // 2),
               (x + w // 2 + 10, y + h // 2 + 12), (x + w // 2, y + h - 8),
               (x + w // 2 - 12, y + h // 2 + 10), (x + 8, y + h // 2),
               (x + w // 2 - 10, y + h // 2 - 8)], fill=ORANGE, outline=RED, width=2)
    d.ellipse([x + w // 2 - 8, y + h // 2 - 8, x + w // 2 + 8, y + h // 2 + 8], fill=GOLD)
    if label:
        draw_text(d, x + 8, y + h - 18, "6 KILLED", font(True, 11), (255, 255, 255))


def ill_chart(d, x, y, w, h, c1, c2, label=True):
    d.rectangle([x, y, x + w, y + h], fill=(16, 42, 90))
    pts = [(x + 8, y + h - 16), (x + w // 4, y + h - 30), (x + w // 2, y + h - 22),
           (x + 3 * w // 4, y + h - 44), (x + w - 10, y + 12)]
    d.line(pts, fill=(80, 220, 120), width=4)
    d.polygon(pts + [(x + w - 10, y + h - 8), (x + 8, y + h - 8)], fill=(80, 220, 120, 60))
    if label:
        draw_text(d, x + 8, y + 6, "+6.3%", font(True, 14), (255, 255, 255))


def ill_radar(d, x, y, w, h, c1, c2, label=True):
    d.rectangle([x, y, x + w, y + h], fill=(20, 60, 50))
    cx, cy = x + w // 2, y + h // 2
    for r in (10, 18, 26):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(80, 220, 120), width=1)
    d.line([cx, cy, cx + 22, cy - 16], fill=(80, 220, 120), width=2)
    d.ellipse([cx + 16, cy - 12, cx + 22, cy - 6], fill=RED)
    if label:
        draw_text(d, x + 6, y + h - 16, "DELTA", font(True, 10), (255, 255, 255))


def ill_drone(d, x, y, w, h, c1, c2, label=True):
    d.rectangle([x, y, x + w, y + h], fill=(30, 34, 48))
    for sx, sy in [(x + 12, y + 10), (x + w - 12, y + 14), (x + 20, y + h - 12)]:
        d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 255, 255))
    cx, cy = x + w // 2, y + h // 2
    d.ellipse([cx - 12, cy - 8, cx + 12, cy + 8], fill=c1, outline=INK, width=2)
    for dx, dy in [(-18, -12), (18, -12), (-18, 12), (18, 12)]:
        d.line([cx, cy, cx + dx, cy + dy], fill=GREY, width=2)
        d.ellipse([cx + dx - 6, cy + dy - 3, cx + dx + 6, cy + dy + 3], outline=(255, 255, 255), width=2)
    if label:
        draw_text(d, x + 6, y + h - 16, "96 DRONES", font(True, 10), (255, 255, 255))


def ill_refinery(d, x, y, w, h, c1, c2, label=True):
    d.rectangle([x, y, x + w, y + h], fill=(70, 60, 50))
    d.rectangle([x + 10, y + h - 34, x + 22, y + h - 8], fill=c1, outline=INK, width=1)
    d.rectangle([x + 28, y + h - 26, x + 44, y + h - 8], fill=c1, outline=INK, width=1)
    d.polygon([(x + 48, y + h - 8), (x + 54, y + 14), (x + 60, y + h - 8)], fill=ORANGE, outline=INK, width=1)
    d.ellipse([x + w - 24, y + 8, x + w - 8, y + 24], fill=GOLD, outline=RED, width=2)
    if label:
        draw_text(d, x + 6, y + 4, "1,500 km", font(True, 10), (255, 255, 255))


def ill_rubble(d, x, y, w, h, c1, c2, label=True):
    d.rectangle([x, y, x + w, y + h], fill=(120, 110, 95))
    d.polygon([(x + 6, y + h - 8), (x + 20, y + h - 30), (x + 36, y + h - 8)], fill=(90, 80, 65), outline=INK, width=1)
    d.polygon([(x + 34, y + h - 8), (x + 52, y + h - 40), (x + w - 8, y + h - 8)], fill=(70, 62, 50), outline=INK, width=1)
    d.line([x + 8, y + 10, x + w - 8, y + 10], fill=RED, width=3)
    if label:
        draw_text(d, x + 6, y + 14, "-77 YEARS", font(True, 11), (255, 255, 255))


def ill_oil(d, x, y, w, h, c1, c2, label=True):
    d.rectangle([x, y, x + w, y + h], fill=(210, 190, 140))
    d.polygon([(x + w // 2 - 4, y + 10), (x + w // 2 + 16, y + h - 20), (x + w // 2 + 4, y + h - 20),
               (x + w // 2 - 10, y + h - 20)], fill=INK)
    d.line([x + w // 2 - 14, y + 16, x + w // 2 + 22, y + 16], fill=INK, width=3)
    d.ellipse([x + w - 22, y + 6, x + w - 8, y + 20], fill=(20, 20, 20))
    if label:
        draw_text(d, x + 6, y + h - 16, "4 PROVINCES", font(True, 9), INK)


def ill_station(d, x, y, w, h, c1, c2, label=True):
    d.rectangle([x, y, x + w, y + h], fill=(10, 16, 40))
    for sx, sy in [(x + 12, y + 10), (x + w - 14, y + 12), (x + 18, y + h - 12), (x + w - 20, y + h - 16)]:
        d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 255, 255))
    d.rectangle([x + w // 2 - 22, y + h // 2 - 4, x + w // 2 - 6, y + h // 2 + 4], fill=c1, outline=INK, width=1)
    d.rectangle([x + w // 2 + 6, y + h // 2 - 4, x + w // 2 + 22, y + h // 2 + 4], fill=c1, outline=INK, width=1)
    d.ellipse([x + w // 2 - 7, y + h // 2 - 7, x + w // 2 + 7, y + h // 2 + 7], fill=GOLD, outline=INK, width=1)
    if label:
        draw_text(d, x + 6, y + h - 16, "TIANGONG", font(True, 10), (255, 255, 255))


def ill_chip(d, x, y, w, h, c1, c2, label=True):
    d.rectangle([x, y, x + w, y + h], fill=(24, 24, 30))
    d.rectangle([x + w // 2 - 14, y + h // 2 - 14, x + w // 2 + 14, y + h // 2 + 14], fill=c1, outline=GOLD, width=2)
    for i in range(4):
        d.line([x + w // 2 - 10 + i * 7, y + h // 2 - 14, x + w // 2 - 10 + i * 7, y + 6], fill=GOLD, width=2)
        d.line([x + w // 2 - 10 + i * 7, y + h // 2 + 14, x + w // 2 - 10 + i * 7, y + h - 6], fill=GOLD, width=2)
    if label:
        draw_text(d, x + 6, y + h - 16, "7 FIRMS", font(True, 10), (255, 255, 255))


def ill_virus(d, x, y, w, h, c1, c2, label=True):
    d.rectangle([x, y, x + w, y + h], fill=(140, 30, 30))
    cx, cy = x + w // 2, y + h // 2 - 4
    d.ellipse([cx - 14, cy - 14, cx + 14, cy + 14], fill=RED, outline=(255, 255, 255), width=2)
    for a in range(0, 360, 45):
        import math
        ex = cx + int(20 * math.cos(math.radians(a)))
        ey = cy + int(20 * math.sin(math.radians(a)))
        d.line([cx, cy, ex, ey], fill=(255, 255, 255), width=2)
        d.ellipse([ex - 3, ey - 3, ex + 3, ey + 3], fill=(255, 255, 255))
    if label:
        draw_text(d, x + 6, y + h - 16, "25+ YEARS LOST", font(True, 9), (255, 255, 255))


def ill_dna(d, x, y, w, h, c1, c2, label=True):
    d.rectangle([x, y, x + w, y + h], fill=(230, 240, 255))
    for i in range(6):
        yy = y + 8 + i * 8
        xx = x + 12 + (6 if i % 2 == 0 else -6)
        d.line([x + 10, yy, x + w - 10, yy], fill=c1, width=2)
        d.ellipse([xx - 3, yy - 3, xx + 3, yy + 3], fill=RED)
        mx2 = x + w - (xx - x)
        d.ellipse([mx2 - 3, yy - 3, mx2 + 3, yy + 3], fill=TEAL)
    if label:
        draw_text(d, x + 6, y + h - 16, "1st DRUG", font(True, 10), INK)


def ill_robot(d, x, y, w, h, c1, c2, label=True):
    d.rectangle([x, y, x + w, y + h], fill=(40, 40, 60))
    d.rectangle([x + w // 2 - 14, y + h // 2 - 12, x + w // 2 + 14, y + h // 2 + 12], fill=c1, outline=INK, width=2)
    d.ellipse([x + w // 2 - 8, y + h // 2 - 6, x + w // 2 - 2, y + h // 2], fill=RED)
    d.ellipse([x + w // 2 + 2, y + h // 2 - 6, x + w // 2 + 8, y + h // 2], fill=RED)
    d.line([x + w // 2 - 8, y + h // 2 + 6, x + w // 2 + 8, y + h // 2 + 6], fill=INK, width=2)
    d.line([x + w // 2, y + h // 2 - 12, x + w // 2, y + h // 2 - 20], fill=GOLD, width=2)
    if label:
        draw_text(d, x + 6, y + h - 16, "2 STATES SUE", font(True, 9), (255, 255, 255))


def ill_trophy(d, x, y, w, h, c1, c2, label=True):
    d.rectangle([x, y, x + w, y + h], fill=(20, 80, 40))
    cx = x + w // 2
    d.polygon([(cx - 10, y + 12), (cx + 10, y + 12), (cx + 7, y + 30), (cx - 7, y + 30)], fill=GOLD, outline=INK, width=1)
    d.arc([cx - 20, y + 12, cx - 6, y + 28], 90, 270, fill=GOLD, width=3)
    d.arc([cx + 6, y + 12, cx + 20, y + 28], -90, 90, fill=GOLD, width=3)
    d.rectangle([cx - 12, y + 34, cx + 12, y + 40], fill=GOLD, outline=INK, width=1)
    if label:
        draw_text(d, x + 6, y + h - 16, "BOCA WIN", font(True, 10), (255, 255, 255))


HERO_ILL = {1: ill_pill, 2: ill_satellite, 3: ill_blast, 4: ill_chart}
SMALL_ILL = {5: ill_radar, 6: ill_drone, 7: ill_refinery, 8: ill_rubble, 9: ill_oil,
             10: ill_station, 11: ill_chip, 12: ill_chart, 13: ill_dna, 14: ill_robot,
             15: ill_chart, 16: ill_blast}

# ---------------------------------------------------------------- map
CONTINENTS = {
    "NA": [(-168, 66), (-140, 70), (-125, 71), (-110, 68), (-95, 69), (-85, 66), (-80, 73),
           (-65, 62), (-55, 52), (-60, 46), (-70, 42), (-75, 35), (-80, 32), (-84, 30),
           (-90, 21), (-97, 26), (-105, 23), (-110, 24), (-117, 33), (-125, 40),
           (-125, 49), (-135, 58), (-150, 61), (-165, 60)],
    "SA": [(-80, 9), (-77, 4), (-80, -3), (-81, -6), (-77, -12), (-72, -18), (-70, -23),
           (-70, -30), (-72, -37), (-73, -44), (-70, -52), (-66, -55), (-65, -50),
           (-62, -42), (-57, -35), (-52, -32), (-48, -28), (-41, -23), (-39, -17),
           (-35, -9), (-35, -6), (-44, -3), (-50, 0), (-55, 5), (-60, 8), (-70, 11)],
    "EU": [(-10, 36), (-9, 43), (-2, 48), (-4, 50), (0, 51), (3, 53), (8, 57), (10, 59),
           (5, 60), (10, 62), (18, 69), (25, 71), (31, 70), (40, 68), (44, 66), (40, 60),
           (30, 60), (28, 56), (24, 58), (21, 55), (19, 54), (14, 54), (12, 45), (18, 40),
           (23, 36), (19, 42), (12, 44), (8, 44), (3, 43), (-2, 37)],
    "AF": [(-6, 35), (-10, 31), (-15, 27), (-17, 21), (-17, 15), (-15, 11), (-8, 5),
           (-4, 5), (2, 6), (6, 4), (9, 4), (9, 0), (12, -5), (13, -12), (12, -18),
           (16, -23), (18, -29), (20, -35), (26, -34), (32, -29), (35, -24), (40, -16),
           (40, -10), (42, -2), (46, 0), (51, 2), (51, 11), (44, 11), (40, 15), (37, 18),
           (35, 22), (32, 31), (22, 33), (11, 34), (10, 37), (0, 36)],
    "AS": [(40, 68), (50, 69), (60, 69), (70, 72), (80, 73), (90, 75), (100, 77), (110, 74),
           (120, 73), (130, 72), (140, 72), (150, 70), (158, 65), (162, 60), (158, 53),
           (150, 59), (142, 50), (140, 40), (135, 34), (130, 33), (127, 35), (122, 38),
           (120, 32), (122, 28), (118, 25), (110, 20), (108, 12), (105, 9), (100, 8),
           (98, 12), (95, 16), (92, 21), (89, 22), (86, 20), (80, 13), (77, 8), (75, 12),
           (72, 20), (66, 25), (61, 25), (57, 26), (52, 28), (50, 30), (48, 30), (44, 29),
           (43, 27), (40, 31), (36, 36), (30, 36), (27, 40), (23, 40), (26, 45), (28, 45),
           (30, 46), (32, 47), (34, 48), (38, 48), (40, 52), (40, 56), (44, 60), (40, 64)],
    "OC": [(113, -22), (114, -30), (115, -35), (124, -33), (129, -32), (135, -35), (140, -38),
           (145, -38), (150, -37), (153, -32), (153, -27), (146, -19), (142, -11), (137, -12),
           (135, -15), (132, -11), (130, -13), (126, -14), (122, -17), (118, -20), (113, -22),
           (130, -3), (136, -4), (141, -6), (146, -8), (150, -9), (155, -9), (160, -10),
           (162, -11), (166, -15), (168, -17), (170, -20), (174, -37), (178, -38), (175, -41),
           (172, -43), (168, -47), (167, -45), (173, -41), (177, -38)],
}


def lonlat_to_xy(lon, lat, mx, my, mw, mh):
    x = mx + (lon + 180.0) / 360.0 * mw
    y = my + (90.0 - lat) / 180.0 * mh
    return x, y

# ---------------------------------------------------------------- page
def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    by_num = {s[0]: s for s in STORIES}

    # ---- masthead
    d.rectangle([0, 0, W, 104], fill=NAVY)
    d.rectangle([0, 104, W, 108], fill=GOLD)
    draw_text(d, 16, 10, "THE WORLD IN ONE PAGE  |  THE DAILY BRIEFING", font(True, 12), (180, 200, 235))
    # right-align the "No. 328" by measuring
    tw = d.textlength("No. 328", font=font(True, 12))
    d.rectangle([W - 16 - tw, 8, W, 26], fill=NAVY)
    draw_text(d, W - 16 - tw, 10, "No. 328", font(True, 12), (180, 200, 235))
    draw_text(d, 16, 30, "TUESDAY 24 NOVEMBER 2026", font(True, 36), (255, 255, 255))
    draw_text(d, 16, 72, "50 STORIES  \u00b7  7 REGIONS  \u00b7  ALL SOURCED  \u00b7  DATE-CHECKED",
              font(True, 14), GOLD)
    counts = {}
    for s in STORIES:
        counts[s[3]] = counts.get(s[3], 0) + 1
    bar = "  \u00b7  ".join("%s %d" % (r, counts[r]) for r in
                           ["EUROPE", "MIDDLE EAST", "ASIA", "AFRICA", "AMERICAS", "OCEANIA", "SPACE"])
    draw_text(d, 16, 90, bar, font(False, 11), (200, 210, 230))
    draw_text(d, 16, 112, "50 sourced stories, a UTC timeline and a date check \u2014 24 November 2026",
              font(False, 12), INK)

    # ---- UTC timeline strip
    ty = 132
    d.rectangle([14, ty, W - 14, ty + 40], fill=CARD, outline=NAVY, width=1)
    draw_text(d, 22, ty + 4, "UTC TIMELINE", font(True, 10), NAVY)
    slot_w = (W - 28 - 110) // 6
    for i, (t, ev) in enumerate(TIMELINE):
        x0 = 14 + 110 + i * slot_w
        d.line([x0, ty + 4, x0, ty + 36], fill=LIGHT, width=1)
        draw_text(d, x0 + 4, ty + 4, t, font(True, 10), RED)
        for j, ln in enumerate(wrap(d, ev, font(False, 9), slot_w - 8)):
            if j < 2:
                draw_text(d, x0 + 4, ty + 16 + j * 11, ln, font(False, 9), INK)

    # ---- hero cards (1-4)
    hy, hh = 182, 148
    cw = (W - 28 - 3 * 6) // 4
    for i, num in enumerate([1, 2, 3, 4]):
        s = by_num[num]
        x0 = 14 + i * (cw + 6)
        col = REGION_COLORS[s[3]]
        d.rectangle([x0, hy, x0 + cw, hy + hh], fill=CARD, outline=col, width=2)
        d.rectangle([x0, hy, x0 + cw, hy + 22], fill=col)
        draw_text(d, x0 + 6, hy + 4, "%d  %s" % (num, s[3]), font(True, 11), (255, 255, 255))
        HERO_ILL[num](d, x0 + 6, hy + 28, cw - 12, 62, col, col)
        hl = wrap(d, s[1], font(True, 12), cw - 12)
        yy = hy + 94
        for ln in hl[:2]:
            draw_text(d, x0 + 6, yy, ln, font(True, 12), INK)
            yy += 14
        det = wrap(d, s[2], font(False, 10), cw - 12)
        for ln in det[:1]:
            draw_text(d, x0 + 6, yy + 1, ln, font(False, 10), INK)
            yy += 12
        src = s[6] + ("  [CLAIM]" if s[7] else "")
        draw_text(d, x0 + 6, hy + hh - 13, "Source: " + src, font(False, 9), GREY)

    # ---- small cards (5-16): 4 cols x 3 rows
    sy = 338
    rh = 56
    for r in range(3):
        for c in range(4):
            num = 5 + r * 4 + c
            s = by_num[num]
            x0 = 14 + c * (cw + 6)
            y0 = sy + r * (rh + 4)
            col = REGION_COLORS[s[3]]
            d.rectangle([x0, y0, x0 + cw, y0 + rh], fill=CARD, outline=col, width=1)
            d.rectangle([x0, y0, x0 + 54, y0 + rh], fill=LIGHT, outline=col, width=1)
            SMALL_ILL[num](d, x0 + 3, y0 + 3, 48, rh - 6, col, col, label=False)
            tx = x0 + 60
            hl = wrap(d, "%d. %s" % (num, s[1]), font(True, 10), cw - 66)
            yy = y0 + 3
            for ln in hl[:2]:
                draw_text(d, tx, yy, ln, font(True, 10), INK)
                yy += 12
            det = wrap(d, s[2], font(False, 9), cw - 66)
            for ln in det[:1]:
                draw_text(d, tx, yy, ln, font(False, 9), GREY)
                yy += 11
            src = s[6] + (" [CLAIM]" if s[7] else "")
            draw_text(d, tx, y0 + rh - 11, src, font(False, 8), GREY)

    # ---- map
    my = 522
    d.rectangle([14, my, W - 14, my + 172], fill=CARD, outline=NAVY, width=1)
    draw_text(d, 22, my + 4, "WHERE IT HAPPENED \u2014 numbered pins 1\u201350", font(True, 12), NAVY)
    lx = W - 14 - 8 * 62
    for i, (reg, col) in enumerate(REGION_COLORS.items()):
        xx = 22 + (i % 4) * 150
        yy2 = my + 20 + (i // 4) * 0
    # legend row under title, right side
    leg_x = 400
    for i, reg in enumerate(["EUROPE", "MIDDLE EAST", "ASIA", "AFRICA", "AMERICAS", "OCEANIA", "SPACE"]):
        xx = leg_x + i * 87
        d.ellipse([xx, my + 7, xx + 9, my + 16], fill=REGION_COLORS[reg], outline=INK, width=1)
        draw_text(d, xx + 11, my + 6, reg, font(True, 8), INK)
    mx, mmy, mw, mh = 22, my + 22, W - 44, 146
    d.rectangle([mx, mmy, mx + mw, mmy + mh], fill=MAPSEA, outline=GREY, width=1)
    for pts in CONTINENTS.values():
        xy = [lonlat_to_xy(lon, lat, mx, mmy, mw, mh) for lon, lat in pts]
        d.polygon(xy, fill=MAPLAND, outline=(150, 140, 110))
    # pins
    for s in STORIES:
        num, _, _, reg, lon, lat, _, _ = s
        if reg == "SPACE":
            px, py = mx + mw - 18, mmy + 12
        else:
            px, py = lonlat_to_xy(lon, lat, mx, mmy, mw, mh)
        col = REGION_COLORS[reg]
        r = 7 if num <= 16 else 5
        d.ellipse([px - r, py - r, px + r, py + r], fill=col, outline=(255, 255, 255), width=1)
        if num <= 16:
            draw_text(d, px - 3, py - 5, str(num), font(True, 8), (255, 255, 255))
    draw_text(d, mx + mw - 60, mmy + 22, "38 SPACE", font(True, 8), INK)

    # ---- briefs 17-50, two columns
    by = 702
    draw_text(d, 14, by, "THE OTHER 34 STORIES \u2014 17\u201350, ONE LINE EACH", font(True, 12), NAVY)
    d.line([14, by + 16, W - 14, by + 16], fill=NAVY, width=1)
    briefs = [s for s in STORIES if s[0] >= 17]
    for i, s in enumerate(briefs):
        col_i = 0 if i < 17 else 1
        row = i % 17
        x0 = 14 if col_i == 0 else 524
        y0 = by + 20 + row * 14
        line = "%d. %s \u2014 %s (%s%s)" % (s[0], s[1], s[2].split(".")[0] + ".", s[6],
                                            " CLAIM" if s[7] else "")
        maxw = 500 if col_i == 0 else 486
        bf = font(False, 9)
        while d.textlength(line, font=bf) > maxw and len(line) > 20:
            line = line[:-2] + "\u2026"
        draw_text(d, x0, y0, line, bf, INK)

    # ---- footer DATE CHECK
    fy = 962
    d.rectangle([14, fy, W - 14, H - 8], fill=(255, 244, 214), outline=RED, width=1)
    lines = wrap(d, DATE_CHECK, font(False, 10), W - 40)
    yy = fy + 4
    for ln in lines[:4]:
        draw_text(d, 22, yy, ln, font(False, 10), INK)
        yy += 13
    return img


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    for name in os.listdir(OUT_DIR):
        p = os.path.join(OUT_DIR, name)
        if os.path.isfile(p) or os.path.islink(p):
            os.remove(p)
        elif os.path.isdir(p):
            shutil.rmtree(p)
    img = build()
    img.save(OUT_PATH, format="PNG", optimize=True)
    print("wrote", OUT_PATH, img.size)


if __name__ == "__main__":
    main()
