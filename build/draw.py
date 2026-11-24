#!/usr/bin/env python3
"""Draw the front page for Monday 23 November 2026.

Own work: every line, polygon and number below was written for this entry.
News facts come from VERIFIED_NEWS.md (verified against Reuters, AP, CNN,
WSJ, NIHR and other named outlets on 24 Nov 2026). Fonts are OFL data
vendored under fonts/. Renders a 1024x1024 PNG at repo/entry.png.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
FONTS = os.path.join(REPO, "fonts")

# ---------------------------------------------------------------- palette
PAPER = (247, 243, 232)      # warm newsprint
INK = (17, 17, 17)
RED = (166, 30, 34)          # deep newspaper red
RED_DK = (140, 20, 25)
SEA = (222, 232, 238)        # map sea
LAND_FILL = (214, 196, 158)
LAND_LINE = (120, 110, 90)
GREY = (90, 88, 82)
LIGHT_LINE = (190, 184, 172)
GREEN = (21, 128, 61)        # CONFIRMED
BLUE = (29, 78, 216)         # OFFICIAL
BROWN = (146, 64, 14)        # REPORTED

REGION_COLOURS = {
    "europe": (29, 78, 216), "asia": (220, 38, 38), "mideast": (217, 119, 6),
    "americas": (5, 150, 105), "africa": (124, 58, 237),
    "oceania": (8, 145, 178), "global": (107, 114, 128),
}
REGION_LABELS = [
    ("EUROPE", 9, "europe"), ("AMERICAS", 9, "americas"),
    ("ASIA", 7, "asia"), ("MIDDLE EAST", 5, "mideast"),
    ("AFRICA", 2, "africa"), ("OCEANIA", 1, "oceania"), ("GLOBAL", 2, "global"),
]

# ---------------------------------------------------------------- fonts
def font(name, size):
    return ImageFont.truetype(os.path.join(FONTS, name), size)

DM = "DMSerifDisplay-Regular.ttf"
LB = "Lato-Bold.ttf"
LK = "Lato-Black.ttf"
LR = "Lato-Regular.ttf"

# ---------------------------------------------------------------- helpers
def wrap_text(draw, text, fnt, width):
    """Greedy wrap; returns list of lines that fit `width`."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def text_block(draw, x, y, text, fnt, width, fill=INK, leading=None, max_lines=None):
    """Draw wrapped text; returns the y just below the block."""
    if leading is None:
        leading = int(fnt.size * 1.18)
    lines = wrap_text(draw, text, fnt, width)
    if max_lines:
        lines = lines[:max_lines]
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y

def fit_font(name, text, width, start, minimum=10):
    """Largest size <= start whose rendering of `text` fits `width`."""
    size = start
    while size > minimum:
        f = font(name, size)
        if ImageFont.truetype(os.path.join(FONTS, name), size).getlength(text) <= width:
            return f
        size -= 1
    return font(name, minimum)

def centre(draw, y, text, fnt, cx, fill=INK):
    w = draw.textlength(text, font=fnt)
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)
    return w

def badge(draw, x, y, kind):
    """Small verification badge; returns its width."""
    label = {"CONFIRMED": "CONFIRMED", "OFFICIAL": "OFFICIAL",
             "REPORTED": "REPORTED"}[kind]
    colour = {"CONFIRMED": GREEN, "OFFICIAL": BLUE, "REPORTED": BROWN}[kind]
    f = font(LK, 8)
    tw = draw.textlength(label, font=f)
    w = int(tw) + 10
    h = 12
    draw.rounded_rectangle([x, y, x + w, y + h], radius=2, fill=colour)
    draw.text((x + 5, y + 1), label, font=f, fill=(255, 255, 255))
    return w

# ---------------------------------------------------------------- map data
# (lon, lat) rings, drawn from geographic knowledge. Equirectangular:
# the same projection places the land and the pins, so pins land right.
NORTH_AMERICA = [(-168, 66), (-161, 58), (-153, 58), (-145, 60), (-137, 58),
    (-131, 54), (-125, 49), (-124, 40), (-120, 34), (-114, 29), (-109, 23),
    (-105, 20), (-97, 16), (-94, 17), (-91, 14), (-87, 13), (-83, 9), (-79, 9),
    (-80, 9), (-83, 10), (-86, 12), (-88, 14), (-88, 17), (-87, 21), (-90, 21),
    (-91, 19), (-96, 19), (-97, 22), (-97, 26), (-96, 29), (-93, 30), (-89, 30),
    (-84, 30), (-81, 25), (-80, 27), (-80, 32), (-76, 35), (-74, 39), (-71, 41),
    (-69, 44), (-66, 45), (-60, 46), (-65, 49), (-59, 50), (-55, 52), (-60, 55),
    (-65, 58), (-68, 55), (-70, 58), (-73, 62), (-78, 62), (-82, 66), (-88, 66),
    (-93, 67), (-95, 69), (-105, 68), (-115, 68), (-125, 70), (-135, 69),
    (-145, 70), (-155, 71), (-162, 70), (-168, 66)]
GREENLAND = [(-45, 60), (-40, 64), (-32, 68), (-25, 70), (-20, 74), (-25, 76),
    (-35, 77), (-50, 76), (-58, 74), (-58, 70), (-53, 66), (-48, 62), (-45, 60)]
SOUTH_AMERICA = [(-79, 9), (-77, 4), (-80, -3), (-81, -6), (-77, -12), (-72, -18),
    (-70, -23), (-70, -30), (-72, -37), (-73, -44), (-74, -50), (-69, -52),
    (-66, -55), (-68, -50), (-65, -45), (-62, -41), (-58, -35), (-52, -32),
    (-48, -28), (-41, -23), (-39, -17), (-35, -9), (-35, -6), (-40, -3),
    (-44, -2), (-50, 0), (-53, 4), (-58, 6), (-62, 9), (-68, 11), (-72, 12),
    (-75, 11), (-77, 8), (-79, 9)]
AFRICA = [(-6, 35), (-10, 31), (-15, 27), (-17, 21), (-17, 15), (-15, 11),
    (-13, 8), (-8, 5), (-4, 5), (0, 6), (6, 4), (9, 4), (9, 0), (12, -4),
    (13, -10), (12, -17), (14, -22), (16, -28), (19, -34), (26, -34), (32, -29),
    (35, -24), (36, -18), (40, -15), (40, -10), (42, -4), (46, -1), (51, 2),
    (51, 11), (48, 11), (44, 11), (40, 15), (38, 18), (37, 22), (34, 27),
    (32, 31), (30, 31), (25, 32), (20, 32), (15, 32), (11, 34), (10, 37),
    (6, 37), (-6, 35)]
EURASIA = [(-10, 36), (-9, 38), (-9, 43), (-2, 44), (-1, 46), (-4, 48), (-2, 49),
    (0, 51), (3, 53), (8, 55), (8, 57), (10, 59), (5, 60), (5, 62), (12, 65),
    (18, 69), (25, 71), (30, 70), (35, 68), (40, 67), (45, 68), (55, 69),
    (65, 69), (75, 72), (85, 74), (95, 76), (105, 77), (115, 73), (125, 72),
    (135, 72), (145, 72), (155, 70), (162, 66), (170, 66), (178, 65), (178, 62),
    (170, 60), (162, 60), (158, 53), (156, 51), (150, 59), (142, 59), (141, 52),
    (140, 46), (138, 42), (135, 35), (132, 33), (130, 32), (127, 35), (126, 38),
    (122, 39), (120, 35), (122, 32), (120, 28), (118, 25), (110, 21), (108, 18),
    (105, 10), (104, 9), (103, 7), (100, 7), (98, 10), (97, 15), (94, 17),
    (92, 21), (89, 22), (87, 21), (85, 19), (80, 15), (77, 8), (76, 10),
    (73, 16), (70, 20), (66, 25), (62, 25), (58, 25), (56, 27), (54, 27),
    (52, 28), (50, 29), (48, 30), (48, 29), (50, 26), (52, 25), (54, 24),
    (56, 26), (58, 23), (59, 22), (57, 20), (55, 17), (52, 15), (48, 14),
    (44, 13), (43, 12), (41, 15), (39, 20), (38, 22), (35, 29), (34, 31),
    (36, 36), (33, 36), (30, 36), (27, 37), (26, 38), (23, 36), (22, 37),
    (19, 40), (19, 42), (15, 44), (12, 44), (10, 44), (8, 44), (3, 43),
    (0, 39), (-2, 37), (-6, 36), (-9, 37), (-10, 36)]
AUSTRALIA = [(114, -22), (114, -30), (115, -33), (118, -35), (124, -33),
    (129, -32), (132, -32), (135, -35), (138, -35), (140, -38), (145, -38),
    (150, -37), (153, -32), (153, -27), (150, -23), (146, -19), (142, -15),
    (142, -11), (140, -17), (136, -15), (135, -12), (132, -11), (130, -13),
    (126, -14), (122, -17), (118, -20), (114, -22)]
NEW_ZEALAND = [(167, -45), (170, -43), (173, -41), (175, -38), (177, -38),
    (178, -37), (175, -40), (172, -43), (168, -46), (167, -45)]
UK = [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53), (1, 51),
    (-3, 50), (-5, 50)]
JAPAN = [(130, 31), (132, 33), (135, 34), (137, 35), (139, 37), (140, 39),
    (141, 41), (142, 43), (144, 44), (142, 42), (140, 38), (139, 36), (136, 33),
    (133, 34), (131, 32), (130, 31)]
MADAGASCAR = [(44, -16), (47, -15), (50, -16), (49, -20), (47, -24), (44, -25),
    (43, -21), (44, -16)]
SUMATRA_JAVA = [(95, 5), (100, 0), (104, -3), (106, -6), (110, -7), (114, -8),
    (114, -9), (110, -8), (106, -7), (102, -4), (98, 0), (95, 5)]
BORNEO = [(109, 1), (113, 3), (117, 5), (119, 0), (117, -3), (113, -4),
    (110, -2), (109, 1)]
ICELAND = [(-22, 64), (-18, 65), (-15, 66), (-18, 67), (-22, 66), (-22, 64)]
LAND_RINGS = [NORTH_AMERICA, GREENLAND, SOUTH_AMERICA, AFRICA, EURASIA, AUSTRALIA,
        NEW_ZEALAND, UK, JAPAN, MADAGASCAR, SUMATRA_JAVA, BORNEO, ICELAND]

def make_proj(x0, y0, w, h, lon0, lon1, lat0, lat1):
    def proj(lon, lat):
        x = x0 + (lon - lon0) / (lon1 - lon0) * w
        y = y0 + (lat0 - lat) / (lat0 - lat1) * h
        return (x, y)
    return proj

def draw_land(draw, proj):
    for ring in LAND_RINGS:
        pts = [proj(lon, lat) for lon, lat in ring]
        draw.polygon(pts, fill=LAND_FILL, outline=LAND_LINE)

def draw_pins(draw, proj, pins, r=9, font_size=11):
    """pins: list of (number, lat, lon, region). Repulsion keeps neighbours apart;
    a leader line joins a moved pin to its true spot."""
    f = font(LK, font_size)
    pts = []
    for num, lat, lon, reg in pins:
        x, y = proj(lon, lat)
        pts.append([num, x, y, reg, (x, y)])
    for _ in range(80):
        for i in range(len(pts)):
            for j in range(i + 1, len(pts)):
                dx = pts[j][1] - pts[i][1]
                dy = pts[j][2] - pts[i][2]
                dist = (dx * dx + dy * dy) ** 0.5
                if dist < 2 * r + 4 and dist > 0.01:
                    push = (2 * r + 4 - dist) / 2
                    ux, uy = dx / dist, dy / dist
                    pts[i][1] -= ux * push
                    pts[i][2] -= uy * push
                    pts[j][1] += ux * push
                    pts[j][2] += uy * push
    for num, x, y, reg, true in pts:
        c = REGION_COLOURS[reg]
        if abs(x - true[0]) > 1 or abs(y - true[1]) > 1:
            draw.line([true, (x, y)], fill=(70, 70, 70), width=1)
            draw.ellipse([true[0] - 2, true[1] - 2, true[0] + 2, true[1] + 2],
                         fill=(70, 70, 70))
        draw.ellipse([x - r, y - r, x + r, y + r], fill=c,
                     outline=(255, 255, 255), width=2)
        t = str(num)
        tw = draw.textlength(t, font=f)
        draw.text((x - tw / 2, y - font_size / 2 - 1), t, font=f,
                  fill=(255, 255, 255))

# (number, lat, lon, region) for the 13 numbered stories
MAP_PINS = [
    (1, 37.4, -122.0, "americas"),   # Nvidia, Santa Clara
    (2, 36.9, 30.7, "global"),      # COP31, Antalya
    (3, 32.1, 20.1, "europe"),      # Merkury, Benghazi
    (4, 50.8, 30.3, "europe"),      # Dymer, Kyiv region
    (5, -6.2, 106.3, "asia"),       # Cikande, Banten
    (6, 30.3, -97.7, "americas"),   # CrowdStrike, Austin
    (7, 35.7, 51.4, "mideast"),     # Tehran
    (8, 28.6, 77.2, "asia"),        # New Delhi
    (9, 50.85, 4.35, "europe"),     # Brussels
    (10, 40.8, -91.3, "americas"),  # Iowa plant
    (11, 52.2, 0.1, "europe"),      # Cambridge
    (12, 40.3, -76.9, "americas"),  # Harrisburg, PA
    (13, 32.0, 35.3, "mideast"),    # Kufr Malik, West Bank
]

# ---------------------------------------------------------------- page data
W, H = 1024, 1024
MX = 24                      # side margin
CW = W - 2 * MX              # content width = 976

TIMELINE = [  # (utc hour, label) — all times verified in VERIFIED_NEWS.md
    (5.5, "05:30  Kyiv toll 11"),
    (8.1, "08:05  Merkury sunk"),
    (9.7, "09:42  COP31 collapse"),
    (13.6, "13:33  \u201cWorst COP ever\u201d"),
    (14.6, "14:37  Raya out"),
    (21.0, "21:00  Nasdaq +6.5%"),
    (21.9, "21:51  Ashland talks"),
]

KPI = [  # (big number, fact sentence) — number + FULL fact sentence
    ("+31%", "Nvidia shares on Huang's return — its best day since 2003 (Reuters)"),
    ("194", "parties at COP31, the longest talks ever — no deal (CNN)"),
    ("7", "Sea drones sank the corvette Merkury off Libya (Reuters)"),
    ("153", "Russian drones launched overnight; 134 shot down (Ukraine AF)"),
    ("24", "dead confirmed in the factory fire; about 30 missing (Reuters)"),
    ("$43.9B", "CrowdStrike's all-stock deal to buy rival Zscaler (Reuters)"),
]

def draw_top(draw):
    # --- black top bar (fix #5): story count, regions, dating line
    draw.rectangle([0, 0, W, 22], fill=INK)
    f = font(LK, 11)
    draw.text((MX, 5), "THE WORLD IN ONE DAY", font=f, fill=(255, 255, 255))
    centre(draw, 5, "DAY 327 OF 2026", f, W // 2, fill=(255, 90, 90))
    r = "ALL TIMES UTC  ·  RANKED BY CONSEQUENCE"
    draw.text((W - MX - draw.textlength(r, font=f), 5), r, font=f,
              fill=(255, 255, 255))

    # --- masthead (fix #8): DM Serif Display, auto-fit from 76pt
    mast = fit_font(DM, "Monday 23 November 2026", CW, 76)
    mw = draw.textlength("Monday 23 November 2026", font=mast)
    draw.text(((W - mw) / 2, 22), "Monday 23 November 2026", font=mast, fill=INK)

    # --- red rule (fix #5): count, regions, dating line
    y = 122
    draw.line([(MX, y), (W - MX, y)], fill=RED, width=2)
    f2 = font(LK, 13)
    centre(draw, y + 5, "35 STORIES  ·  7 REGIONS  ·  EVERY ONE DATED MONDAY 23 NOVEMBER 2026",
           f2, W // 2, fill=RED)
    draw.line([(MX, y + 22), (W - MX, y + 22)], fill=INK, width=2)

    # --- subhead: the three biggest events (auto-fit so it never clips)
    sub = ("Huang back at Nvidia as shares soar 31%  \u25c6  COP31 collapses over "
           "fossil fuels  \u25c6  Ukraine sinks Russian corvette off Libya")
    f3 = fit_font(LB, sub, CW, 15)
    centre(draw, 148, sub, f3, W // 2)

def draw_timeline(draw):
    # --- UTC timeline strip (fix #1): 7 timed events on a 0-24h axis
    x0, x1, y = MX, W - MX, 164
    draw.rectangle([x0, y, x0 + 108, y + 15], fill=INK)
    f = font(LK, 10)
    draw.text((x0 + 6, y + 2), "THE DAY IN UTC", font=f, fill=(255, 255, 255))
    ax0, ax1 = x0 + 118, x1
    ay = y + 26
    draw.line([(ax0, ay), (ax1, ay)], fill=INK, width=2)
    fs = font(LB, 8)
    for h in (0, 6, 12, 18, 24):
        tx = ax0 + (ax1 - ax0) * h / 24
        draw.line([(tx, ay - 3), (tx, ay + 3)], fill=INK, width=1)
        lab = "%02d" % h
        draw.text((tx - draw.textlength(lab, font=fs) / 2, ay + 5), lab,
                  font=fs, fill=GREY)
    ft = font(LB, 9)
    # alternate labels above / below the axis so none collide
    for i, (h, label) in enumerate(TIMELINE):
        tx = ax0 + (ax1 - ax0) * h / 24
        draw.ellipse([tx - 3, ay - 3, tx + 3, ay + 3], fill=RED,
                     outline=(255, 255, 255), width=1)
        if i % 2 == 0:
            draw.line([(tx, ay - 3), (tx, ay - 8)], fill=GREY, width=1)
            tw = draw.textlength(label, font=ft)
            lx = min(max(tx - tw / 2, ax0), ax1 - tw)
            draw.text((lx, ay - 20), label, font=ft, fill=INK)
        else:
            draw.line([(tx, ay + 3), (tx, ay + 8)], fill=GREY, width=1)
            tw = draw.textlength(label, font=ft)
            lx = min(max(tx - tw / 2, ax0), ax1 - tw)
            draw.text((lx, ay + 10), label, font=ft, fill=INK)

def draw_kpi(draw):
    # --- KPI strip (fix #7): every box = big number + full fact sentence
    y0, h = 212, 48
    bw = (CW - 5 * 5) / 6
    for i, (num, fact) in enumerate(KPI):
        x = MX + i * (bw + 5)
        draw.rectangle([x, y0, x + bw, y0 + h], outline=LIGHT_LINE, width=1)
        draw.rectangle([x, y0, x + 3, y0 + h], fill=RED)
        fn = font(LK, 24)
        draw.text((x + 8, y0 + 2), num, font=fn, fill=RED)
        ff = font(LR, 9.5)
        # fact sentence under the number, wrapped to the box
        text_block(draw, x + 8, y0 + 26, fact, ff, bw - 14, fill=INK,
                   leading=10, max_lines=2)

def draw_regions(draw):
    # --- region bar (fix #5/#6): coloured chips with story counts
    y = 264
    f = font(LK, 10)
    draw.text((MX, y), "STORIES BY REGION", font=f, fill=INK)
    x = MX + 130
    for label, count, key in REGION_LABELS:
        c = REGION_COLOURS[key]
        draw.rectangle([x, y - 1, x + 11, y + 10], fill=c)
        t = "%s %d" % (label, count)
        ft = font(LB, 10)
        draw.text((x + 15, y), t, font=ft, fill=INK)
        x += 15 + draw.textlength(t, font=ft) + 16

# ---------------------------------------------------------------- heroes
HEROES = [
    # (number, region label, badge, headline, standfirst, sources)
    (1, "AMERICAS  ·  MARKETS", "CONFIRMED",
     "Huang is back at Nvidia — shares soar 31%",
     "Board reinstates the co-founder 11 days after he quit; Trump says he "
     "spoke to the board. Wall Street has its best day since April 2025.",
     "REUTERS  ·  WSJ  ·  CNN"),
    (2, "GLOBAL  ·  CLIMATE", "CONFIRMED",
     "COP31 collapses over fossil fuels",
     "The longest climate talks ever end with no deal after the EU, the UK "
     "and island states reject a pact that never names fossil fuels.",
     "CNN  ·  WSJ  ·  LE MONDE  ·  NPR"),
    (3, "EUROPE  ·  CONFLICT", "CONFIRMED",
     "Ukraine sinks Russian corvette off Libya",
     "Seven sea drones hit the Merkury at Benghazi, 2,400 km from the front; "
     "a Ka-27 helicopter is destroyed and the cargo ship Angara is hit.",
     "REUTERS  ·  AP  ·  CNN"),
]

def hero_diagram_nvidia(draw, x, y, w, h, img=None):
    # (fix #1) a data diagram: Monday's market moves as a bar chart
    draw.rectangle([x, y, x + w, y + h], fill=(24, 28, 36))
    ft = font(LB, 9)
    draw.text((x + 8, y + 5), "MONDAY'S MARKET MOVES — % CHANGE",
              font=ft, fill=(255, 255, 255))
    rows = [("NVIDIA", 31.0, "+31%", RED), ("CHIP INDEX", 12.0, "+12%", (200, 200, 200)),
            ("NASDAQ", 6.5, "+6.5%", (200, 200, 200)),
            ("S&P 500", 4.7, "+4.7%", (200, 200, 200)),
            ("DOW", 3.0, "+3.0%", (200, 200, 200))]
    fl, fv = font(LB, 9), font(LK, 10)
    top = y + 19
    for i, (lab, val, txt, col) in enumerate(rows):
        ry = top + i * 13
        draw.text((x + 8, ry), lab, font=fl, fill=(220, 220, 220))
        bx = x + 78
        bw = max(4, val / 31.0 * 150)
        draw.rectangle([bx, ry + 1, bx + bw, ry + 11], fill=col)
        draw.text((bx + bw + 5, ry), txt, font=fv, fill=(255, 255, 255))
    draw.text((x + 8, y + h - 12),
              "12 NOV — HUANG RESIGNS    \u2192    23 NOV — REINSTATED  (11 DAYS)",
              font=ft, fill=(255, 200, 90))

def hero_diagram_cop31(draw, x, y, w, h, img=None):
    # (fix #1) a data diagram: the 14-day COP31 calendar + the count that killed it
    draw.rectangle([x, y, x + w, y + h], fill=(232, 240, 228))
    ft = font(LB, 9)
    draw.text((x + 8, y + 5), "COP31, ANTALYA — 14 DAYS OF TALKS", font=ft, fill=INK)
    cw, ch = 20, 20
    x0 = x + 8
    y0 = y + 20
    fd = font(LB, 9)
    for d in range(9, 23):
        cx = x0 + (d - 9) * (cw + 2)
        col = (200, 60, 50) if d >= 21 else (120, 180, 120)
        draw.rectangle([cx, y0, cx + cw, y0 + ch], fill=col,
                       outline=(255, 255, 255), width=1)
        t = str(d)
        draw.text((cx + (cw - draw.textlength(t, font=fd)) / 2, y0 + 4), t,
                  font=fd, fill=(255, 255, 255))
    draw.text((x0, y0 + ch + 3), "9–20 NOV: TALKS    21–22 NOV: OVERTIME",
              font=font(LB, 8), fill=GREY)
    fn = font(LK, 30)
    draw.text((x + 8, y + 58), "NO DEAL", font=fn, fill=RED)
    draw.text((x + 8, y + h - 16),
              "194 PARTIES  ·  0 MENTIONS OF \u201cFOSSIL FUELS\u201d IN THE DRAFT",
              font=font(LK, 10), fill=INK)

def hero_diagram_merkury(draw, x, y, w, h, img=None):
    # (fix #1) a data diagram: a real map — the Mediterranean, Benghazi, the drones.
    # Rendered on its own image first: the land polygons extend far outside
    # this window, and drawing them straight onto the page would paint the
    # whole sheet. Pasting clips them to the panel.
    sub = Image.new("RGB", (w, h), SEA)
    sd = ImageDraw.Draw(sub)
    proj = make_proj(0, 0, w, h, -10.0, 40.0, 47.0, 30.0)
    draw_land(sd, proj)
    # labels for the seas and shores
    fl = font(LB, 8)
    sd.text(proj(-6, 44), "EUROPE", font=fl, fill=GREY)
    sd.text(proj(2, 33.5), "MEDITERRANEAN SEA", font=fl, fill=(90, 120, 140))
    sd.text(proj(24, 31.5), "LIBYA", font=fl, fill=GREY)
    # dashed drone track from the north-west, labelled with the distance
    bx, by = proj(20.1, 32.1)
    sx, sy = proj(-8, 46)
    n = 14
    for i in range(n):
        t0, t1 = i / n, (i + 0.5) / n
        sd.line([(sx + (bx - sx) * t0, sy + (by - sy) * t0),
                 (sx + (bx - sx) * t1, sy + (by - sy) * t1)],
                fill=RED, width=2)
    sd.text((8, 6), "2,400 KM FROM THE FRONT LINE",
            font=font(LK, 9), fill=RED)
    # the corvette, listing at Benghazi
    sd.polygon([(bx - 16, by + 2), (bx + 14, by + 2), (bx + 18, by + 8),
                (bx - 12, by + 8)], fill=(40, 40, 40))
    sd.line([(bx - 2, by + 2), (bx - 2, by - 8)], fill=(40, 40, 40), width=2)
    sd.ellipse([bx + 8, by - 14, bx + 22, by], fill=(255, 140, 40))
    sd.ellipse([bx + 12, by - 10, bx + 18, by - 4], fill=(255, 200, 60))
    sd.text((bx + 24, by - 8), "BENGHAZI", font=font(LK, 9), fill=INK)
    sd.text((8, h - 26), "7 SEA DRONES  ·  Ka-27 DESTROYED",
            font=font(LK, 10), fill=INK)
    sd.text((8, h - 14), "MV ANGARA HIT  ·  10 CREW HURT",
            font=font(LK, 10), fill=INK)
    img.paste(sub, (x, y))

HERO_DIAGRAMS = [hero_diagram_nvidia, hero_diagram_cop31, hero_diagram_merkury]

def draw_heroes(draw, img):
    y0, ph = 282, 196
    pw = 322
    for i, (num, region, bdg, head, stand, src) in enumerate(HEROES):
        x = MX + i * (pw + 5)
        HERO_DIAGRAMS[i](draw, x, y0, pw, 100, img)
        ky = y0 + 104
        fk = font(LK, 10)
        draw.text((x, ky), "%d  %s" % (num, region), font=fk, fill=RED)
        badge(draw, x + pw - 62, ky - 1, bdg)
        fh = font(DM, 19)
        text_block(draw, x, ky + 14, head, fh, pw, leading=20, max_lines=2)
        fs = font(LR, 10.5)
        text_block(draw, x, ky + 56, stand, fs, pw, leading=12, max_lines=2)
        draw.text((x, y0 + ph - 10), src, font=font(LB, 8), fill=GREY)

# ---------------------------------------------------------------- tiles
# (number, key number, headline, fact, sources, badge, scene)
TILES = [
    ("4", "15", "Russian strikes kill 15 around Kyiv",
     "153 drones in; 134 shot down. Boy, 7, freed after 14 hours in rubble.",
     "REUTERS", "CONFIRMED", "kyiv"),
    ("5", "24", "Factory fire toll confirmed in Indonesia",
     "Blaze at a sweets plant in Banten; about 30 still missing.",
     "REUTERS", "CONFIRMED", "fire"),
    ("6", "$43.9B", "CrowdStrike to buy Zscaler",
     "All-stock deal unites two cyber rivals.",
     "REUTERS", "CONFIRMED", "shield"),
    ("7", "$14.7B", "US sanctions Iran shadow banks",
     "24+ exchange houses hit; FinCEN flags $14.7bn in flows.",
     "REUTERS", "OFFICIAL", "bank"),
    ("8", "$1.62B", "India aid for flood-hit Nepal",
     "Package worth 240bn rupees after Modi–Shah talks.",
     "REUTERS", "CONFIRMED", "peaks"),
    ("9", "404", "Belgium strike grounds flights",
     "Airspace shut 14 hours; 50,000+ travellers hit.",
     "REUTERS", "CONFIRMED", "tower"),
    ("10", "68", "Trump pauses Iowa blast",
     "68 barrels of toxic lead azide; court to rule first.",
     "REUTERS", "CONFIRMED", "barrel"),
    ("11", "700,000", "NHS starts biggest AI cancer trial",
     "Nearly 700,000 women; AI to help read mammograms.",
     "NIHR", "OFFICIAL", "screen"),
    ("12", "1,638", "Measles cases hit 1,638 in Pennsylvania",
     "Nine dead; 330 in hospital in this year's outbreak.",
     "REUTERS", "OFFICIAL", "virus"),
    ("13", "12", "Eisenkot: settler arson is \u201cJewish terrorism\u201d",
     "A dozen cars torched in four West Bank villages.",
     "REUTERS", "CONFIRMED", "houses"),
]

def scene(draw, x, y, w, h, kind):
    """Small flat scene for a tile — simple shapes, no garble risk."""
    if kind == "kyiv":
        draw.rectangle([x, y, x + w, y + h], fill=(26, 30, 44))
        draw.ellipse([x + w - 26, y + 6, x + w - 12, y + 20], fill=(240, 230, 180))
        for bx, bh in ((x + 8, 26), (x + 30, 34), (x + 56, 22), (x + 82, 30)):
            draw.rectangle([bx, y + h - bh, bx + 20, y + h], fill=(10, 12, 20))
            draw.rectangle([bx + 4, y + h - bh + 5, bx + 8, y + h - bh + 9],
                           fill=(255, 200, 90))
        for dx, dy in ((x + 120, y + 8), (x + 140, y + 16), (x + 160, y + 6)):
            draw.ellipse([dx - 2, dy - 2, dx + 2, dy + 2], fill=(255, 255, 255))
        draw.ellipse([x + 150, y + h - 16, x + 170, y + h + 4], fill=(255, 120, 40))
        draw.ellipse([x + 156, y + h - 10, x + 164, y + h - 2], fill=(255, 200, 60))
    elif kind == "fire":
        draw.rectangle([x, y, x + w, y + h], fill=(40, 30, 26))
        draw.rectangle([x + 20, y + 16, x + w - 20, y + h], fill=(90, 70, 60))
        draw.rectangle([x + 30, y + 24, x + 50, y + 34], fill=(255, 220, 120))
        draw.rectangle([x + 60, y + 24, x + 80, y + 34], fill=(255, 220, 120))
        for fx, fh in ((x + 100, 26), (x + 120, 32), (x + 140, 24)):
            draw.polygon([(fx, y + h), (fx + 8, y + h - fh), (fx + 16, y + h)],
                         fill=(255, 110, 30))
        draw.ellipse([x + 130, y + 4, x + 170, y + 22], fill=(120, 120, 120))
    elif kind == "shield":
        draw.rectangle([x, y, x + w, y + h], fill=(18, 40, 60))
        cx, cy = x + w // 2, y + h // 2 + 2
        draw.polygon([(cx - 16, cy - 14), (cx + 16, cy - 14), (cx + 16, cy + 2),
                      (cx, cy + 18), (cx - 16, cy + 2)], fill=(40, 140, 200),
                     outline=(255, 255, 255))
        draw.line([(cx - 8, cy + 2), (cx - 2, cy + 8), (cx + 10, cy - 8)],
                  fill=(255, 255, 255), width=3)
        for nx, ny in ((x + 14, y + 10), (x + w - 14, y + 12), (x + 16, y + h - 10),
                       (x + w - 16, y + h - 12)):
            draw.ellipse([nx - 3, ny - 3, nx + 3, ny + 3], fill=(255, 200, 60))
    elif kind == "bank":
        draw.rectangle([x, y, x + w, y + h], fill=(36, 36, 40))
        draw.polygon([(x + 20, y + 12), (x + w - 20, y + 12), (x + w // 2, y + 4)],
                     fill=(200, 200, 200))
        for px in (x + 34, x + 66, x + 98, x + 130, x + 162):
            draw.rectangle([px, y + 14, px + 8, y + h - 6], fill=(220, 220, 220))
        draw.line([(x + 60, y + 4), (x + w - 20, y + h - 4)], fill=RED, width=4)
        draw.text((x + w // 2 - 12, y + h - 20), "$", font=font(LK, 16),
                  fill=(255, 220, 90))
    elif kind == "peaks":
        draw.rectangle([x, y, x + w, y + h], fill=(210, 228, 240))
        draw.polygon([(x, y + h), (x + 60, y + 8), (x + 120, y + h)], fill=(90, 120, 150))
        draw.polygon([(x + 60, y + 8), (x + 78, y + 20), (x + 48, y + 22)], fill=(255, 255, 255))
        draw.polygon([(x + 90, y + h), (x + 150, y + 14), (x + w, y + h)], fill=(60, 90, 120))
        draw.rectangle([x + 130, y + h - 16, x + 170, y + h - 6], fill=(180, 120, 60))
        draw.text((x + 138, y + h - 16), "$", font=font(LK, 10), fill=(255, 255, 255))
    elif kind == "tower":
        draw.rectangle([x, y, x + w, y + h], fill=(200, 220, 235))
        draw.rectangle([x + 26, y + 10, x + 40, y + h], fill=(120, 120, 120))
        draw.ellipse([x + 18, y + 2, x + 48, y + 16], fill=(60, 90, 120))
        draw.polygon([(x + 90, y + 22), (x + 150, y + 22), (x + 158, y + 28),
                      (x + 90, y + 28)], fill=(220, 220, 220))
        draw.polygon([(x + 150, y + 22), (x + 166, y + 14), (x + 166, y + 28)],
                     fill=(180, 40, 40))
        draw.text((x + w - 24, y + 4), "\u2715", font=font(LK, 16), fill=RED)
    elif kind == "barrel":
        draw.rectangle([x, y, x + w, y + h], fill=(50, 55, 60))
        for bx in (x + 30, x + 80, x + 130):
            draw.rounded_rectangle([bx, y + 10, bx + 34, y + h - 6], radius=4,
                                   fill=(200, 90, 30))
            draw.rectangle([bx, y + 18, bx + 34, y + 22], fill=(140, 50, 10))
            draw.rectangle([bx, y + h - 16, bx + 34, y + h - 12], fill=(140, 50, 10))
        draw.polygon([(x + w - 34, y + 4), (x + w - 14, y + 4), (x + w - 24, y + 20)],
                     fill=(255, 220, 60), outline=(0, 0, 0))
        draw.text((x + w - 27, y + 6), "!", font=font(LK, 10), fill=(0, 0, 0))
    elif kind == "screen":
        draw.rectangle([x, y, x + w, y + h], fill=(230, 240, 235))
        draw.rectangle([x + 30, y + 8, x + 110, y + h - 8], fill=(20, 30, 40))
        draw.ellipse([x + 55, y + 16, x + 85, y + 32], fill=(255, 150, 190))
        draw.ellipse([x + 62, y + 20, x + 78, y + 28], fill=(255, 255, 255))
        draw.rectangle([x + 130, y + 12, x + 150, y + h - 10], fill=(200, 90, 130))
        draw.text((x + 134, y + 16), "AI", font=font(LK, 12), fill=(255, 255, 255))
    elif kind == "virus":
        draw.rectangle([x, y, x + w, y + h], fill=(240, 230, 220))
        for vx, vy, vr in ((x + 40, y + 20, 12), (x + 90, y + 14, 9),
                           (x + 140, y + 24, 13), (x + 170, y + 12, 7)):
            draw.ellipse([vx - vr, vy - vr, vx + vr, vy + vr], fill=(200, 60, 60))
            for ang in range(0, 360, 60):
                import math as _m
                ex = vx + int(vr * 1.5 * _m.cos(_m.radians(ang)))
                ey = vy + int(vr * 1.5 * _m.sin(_m.radians(ang)))
                draw.line([(vx, vy), (ex, ey)], fill=(200, 60, 60), width=2)
        draw.rectangle([x + w - 40, y + h - 22, x + w - 8, y + h - 6], fill=(255, 255, 255),
                       outline=RED, width=1)
        draw.text((x + w - 34, y + h - 22), "+", font=font(LK, 14), fill=RED)
    else:  # houses
        draw.rectangle([x, y, x + w, y + h], fill=(30, 28, 40))
        for hx, hc in ((x + 14, (200, 120, 60)), (x + 62, (90, 140, 200)),
                       (x + 110, (200, 180, 90))):
            draw.rectangle([hx, y + 18, hx + 40, y + h - 4], fill=hc)
            draw.polygon([(hx - 4, y + 18), (hx + 20, y + 6), (hx + 44, y + 18)],
                         fill=(60, 40, 30))
        draw.polygon([(x + 150, y + h), (x + 158, y + h - 26), (x + 166, y + h)],
                     fill=(255, 110, 30))
        draw.ellipse([x + 140, y + 6, x + 170, y + 20], fill=(120, 120, 120))

def draw_tiles(draw):
    # (fix #2) every tile carries a BIG key number + short caption
    tw, th = 191, 112
    rows_y = [482, 597]
    for idx, tile in enumerate(TILES):
        num, key, head, fact, src, bdg, sc = tile
        row, col = divmod(idx, 5)
        x = MX + col * (tw + 5)
        y = rows_y[row]
        draw.rectangle([x, y, x + tw, y + th], outline=LIGHT_LINE, width=1)
        scene(draw, x + 1, y + 1, tw - 2, 42, sc)
        # key number (auto-fit) + badge
        fn = fit_font(LK, key, 118, 22)
        draw.text((x + 6, y + 46), key, font=fn, fill=RED)
        badge(draw, x + tw - 66, y + 48, bdg)
        fh = font(LB, 12)
        text_block(draw, x + 6, y + 68, head, fh, tw - 12, leading=13,
                   max_lines=2)
        # fact line + source, two short lines
        ff = font(LR, 9.5)
        text_block(draw, x + 6, y + 93, fact + "  (%s)" % src, ff, tw - 12,
                   leading=9.5, max_lines=2)

# ---------------------------------------------------------------- map + date check
def draw_map_panel(draw):
    # (fix #6) real land polygons + region-coloured numbered pins, right places
    x0, y0, w, h = MX, 712, 500, 154
    draw.rectangle([x0, y0, x0 + w, y0 + h], fill=SEA, outline=LIGHT_LINE, width=1)
    proj = make_proj(x0 + 4, y0 + 18, w - 8, h - 36, -170.0, 190.0, 78.0, -58.0)
    draw_land(draw, proj)
    draw_pins(draw, proj, MAP_PINS)
    ft = font(LK, 10)
    draw.text((x0 + 8, y0 + 4), "WHERE IT HAPPENED — PIN NUMBERS MATCH THE STORIES; PIN COLOUR IS THE REGION",
              font=ft, fill=INK)
    draw.text((x0 + 8, y0 + h - 12),
              "EUROPE CALL-OUT:  4 KYIV  ·  9 BRUSSELS  ·  11 CAMBRIDGE  ·  13 WEST BANK",
              font=font(LB, 8), fill=GREY)

DATE_LEFT = [  # (date, text) — stories from other days, deliberately left out
    ("SAT 21 NOV", "Iran strikes Bahrain \u00b7 Sparta II ablaze off Finland"),
    ("SAT 21 NOV", "BepiColombo enters Mercury orbit \u00b7 El Chapo Isidro seized"),
    ("SAT 21 NOV", "EU\u2013Indonesia pact signed \u00b7 BTS take five MAMA awards \u00b7 "
     "England beat All Blacks 37\u201312"),
    ("SUN 22 NOV", "Democrats clinch 258 House seats \u00b7 Skubal agrees record $450m Mets deal"),
    ("SUN 22 NOV", "COP31 final session ends in Antalya (collapse confirmed Monday)"),
    ("FRI 20 NOV", "Anthropic claims a Riemann proof (Lean check Sat) \u00b7 "
     "Nigeria boat capsizes, 24 dead"),
]
DATE_FUTURE = [  # (date, text) — not yet happened on 23 Nov
    ("TUE 24 NOV", "Arsenal v Borussia Dortmund, Champions League"),
    ("WED 25 NOV", "US October PCE inflation report due"),
    ("MON 1 DEC", "MLB lockout expected to begin"),
    ("DEC", "Huang to testify on Capitol Hill; BepiColombo orbiters separate 9\u201310 Dec"),
]

def draw_date_check(draw):
    x0, y0, w, h = MX + 512, 712, 464, 154
    draw.rectangle([x0, y0, x0 + w, y0 + h], outline=RED, width=2)
    ft = font(LK, 11)
    draw.text((x0 + 8, y0 + 5), "DATE CHECK", font=ft, fill=RED)
    draw.text((x0 + 90, y0 + 5), "—  what we left out, and why", font=font(LB, 10),
              fill=GREY)
    y = y0 + 24
    draw.text((x0 + 8, y), "LEFT OUT — OTHER DAYS", font=font(LK, 9), fill=INK)
    y += 13
    ff = font(LR, 9)
    for date, text in DATE_LEFT:
        draw.text((x0 + 8, y), date, font=font(LB, 9), fill=RED)
        text_block(draw, x0 + 78, y, text, ff, w - 86, leading=10.5, max_lines=1)
        y += 10
    y += 2
    draw.text((x0 + 8, y), "NOT YET — AFTER 23 NOV", font=font(LK, 9), fill=INK)
    y += 13
    for date, text in DATE_FUTURE:
        draw.text((x0 + 8, y), date, font=font(LB, 9), fill=RED)
        text_block(draw, x0 + 78, y, text, ff, w - 86, leading=10.5, max_lines=1)
        y += 10

# ---------------------------------------------------------------- also on
ALSO_ON = [
    ("14", "Washington", "Trump signs order curbing Congress information requests (AP)"),
    ("15", "New York", "Trump meme-coin gala as the token hits record lows (Reuters)"),
    ("16", "Washington", "FBI probes suspected hack of police database NCIC (AP)"),
    ("17", "Seoul", "Education minister quits over exam cheating scandal (Reuters)"),
    ("18", "Bangkok", "Court halves royal-insult prison term (Reuters)"),
    ("19", "Jakarta", "Prabowo to name vice-presidential candidates (Reuters)"),
    ("20", "Istanbul", "Thousands rally against Turkey crackdown (Reuters)"),
    ("21", "United Nations", "UN chief urges a global AI safety framework within a year (Reuters)"),
    ("22", "Dhaka", "Hasina: arrest if she returns; extradition sought (Reuters)"),
    ("23", "Sydney", "AustralianSuper backs Brookfield's $2.53bn Reliance deal (Reuters)"),
    ("24", "Helsinki", "Finland backs anti-tank barriers on the Russia border (Reuters)"),
    ("25", "Taiz", "Houthi attack kills 10 at a telecom building (Reuters)"),
    ("26", "Gaza", "UNRWA: 1 staffer killed, 3 hurt in Israeli attack (Reuters)"),
    ("27", "Tripoli", "Libya parliament launches unification initiative (Reuters)"),
    ("28", "London", "Arsenal: Raya out of Dortmund clash (Reuters, 14:37 UTC)"),
    ("29", "Basel", "Clariant in talks to buy Ashland (Reuters, 21:51 UTC)"),
    ("30", "Calgary", "Alberta bill may let province fund gas pipelines (Reuters)"),
    ("31", "Khartoum", "UN and US condemn Sunday drone strikes, 4 killed (Reuters)"),
    ("32", "Seoul", "SK hynix +20% after Huang's return (Reuters)"),
    ("33", "London", "UK voters: rising prices top concern amid Iran war (Reuters)"),
    ("34", "Moscow", "Russia to send nuclear-armed satellite, German media claim (Reuters)"),
    ("35", "Beijing", "Trump: China to buy 250 more Boeing planes (CNBC)"),
]

def draw_also_on(draw):
    y0 = 870
    draw.text((MX, y0), "ALSO ON MONDAY 23 NOVEMBER", font=font(LK, 11), fill=INK)
    draw.line([(MX, y0 + 16), (W - MX, y0 + 16)], fill=INK, width=1)
    ff = font(LR, 9)
    fb = font(LB, 9)
    col_w = (CW - 20) / 2
    for i, (num, place, text) in enumerate(ALSO_ON):
        col, row = divmod(i, 11)
        x = MX + col * (col_w + 20)
        y = y0 + 20 + row * 9
        draw.text((x, y), num + ".", font=fb, fill=RED)
        draw.text((x + 20, y), place + " — ", font=fb, fill=INK)
        pw = draw.textlength(place + " — ", font=fb)
        draw.text((x + 20 + pw, y), text, font=ff, fill=INK)

# ---------------------------------------------------------------- footer
def draw_footer(draw):
    y = 989
    draw.line([(MX, y), (W - MX, y)], fill=INK, width=1)
    # (fix #3) HOW WE CHECKED legend, as real badges
    fy = y + 4
    draw.text((MX, fy), "HOW WE CHECKED:", font=font(LK, 9), fill=INK)
    x = MX + 96
    for kind, meaning in (("CONFIRMED", "= 2+ major outlets"),
                          ("OFFICIAL", "= on the record"),
                          ("REPORTED", "= one major outlet")):
        bw = badge(draw, x, fy, kind)
        draw.text((x + bw + 4, fy + 1), meaning, font=font(LR, 9), fill=GREY)
        x += bw + 4 + draw.textlength(meaning, font=font(LR, 9)) + 18
    # (fix #8) honest corrections line
    cy = fy + 13
    draw.text((MX, cy),
              "CORRECTIONS: Dymer toll was 10 early Monday, 11 later; Kyiv-region toll "
              "14\u201315 by outlet; Merkury sunk (Kyiv) vs heavily damaged (Libya); "
              "NHS trial nearly 700,000 (NIHR) vs 660,000 (dpa-AFX).",
              font=font(LR, 8.5), fill=GREY)
    draw.text((MX, cy + 9),
              "Every story here happened or was first reported on Monday 23 November "
              "2026 (UTC), as the named outlets reported it.",
              font=font(LB, 8.5), fill=INK)

# ---------------------------------------------------------------- main
def render():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    draw_top(draw)
    draw_timeline(draw)
    draw_kpi(draw)
    draw_regions(draw)
    draw_heroes(draw, img)
    draw_tiles(draw)
    draw_map_panel(draw)
    draw_date_check(draw)
    draw_also_on(draw)
    draw_footer(draw)
    return img

if __name__ == "__main__":
    out = os.path.join(REPO, "entry.png")
    render().save(out, format="PNG", optimize=True)
    print("saved", out, os.path.getsize(out), "bytes")
