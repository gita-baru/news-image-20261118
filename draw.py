#!/usr/bin/env python3
"""Draw the v2 news image for 18 November 2026 (1024x1024 PNG).

Build tool only: the entry program (main.ts) copies the finished entry.png.
Run: python3 draw.py  ->  writes entry.png beside this file.

Structure (breadth + discipline, after the 17 November winner):
masthead with the date and a story count, a "THE DAY IN UTC" timeline,
4 hero stories, a numbered grid of 12 more stories (5-16), a world map
with numbered dots, a dense "ALSO" list (17-40), a DATE CHECK box that
names big stories left out because they broke before 18 November and
things not yet due, and a sources footer. Every dated claim is from the
verified 18 November 2026 story list; nothing is invented.
"""
import math

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 242, 233)
INK = (22, 22, 22)
RED = (178, 36, 28)
GREY = (96, 90, 80)
AMBER = (232, 168, 60)
WHITE = (250, 248, 242)
BLUE = (40, 90, 160)
TEAL = (20, 120, 90)
PURPLE = (110, 70, 160)
SLATE = (70, 72, 80)
CYAN = (20, 130, 160)
BROWN = (170, 110, 30)

SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def lerp(c1, c2, t):
    return tuple(int(a + (b - a) * t) for a, b in zip(c1, c2))


def vgrad(base, box, top, bottom):
    x0, y0, x1, y1 = box
    span = max(1, y1 - y0)
    for y in range(y0, y1):
        base.line([(x0, y), (x1, y)], fill=lerp(top, bottom, (y - y0) / span))


def wrap_text(d, s, f, max_w, max_lines=None):
    """Wrap s into lines fitting max_w; optionally cap at max_lines,
    truncating the last line with an ellipsis."""
    words, lines, cur = s.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    if max_lines is not None and len(lines) > max_lines:
        lines = lines[:max_lines]
        while lines and d.textlength(lines[-1] + " …", font=f) > max_w:
            lines[-1] = lines[-1].rsplit(" ", 1)[0]
        lines[-1] = lines[-1] + " …"
    return lines


def draw_lines(d, lines, x, y, f, fill, leading=None):
    if leading is None:
        leading = int(f.size * 1.22)
    for ln in lines:
        d.text((x, y), ln, font=f, fill=fill)
        y += leading
    return y


def fit(d, s, max_w, path, size, minimum=12):
    while size > minimum and d.textlength(s, font=font(path, size)) > max_w:
        size -= 1
    return font(path, size)


def starburst(d, cx, cy, r_out, r_in, fill, spikes=9):
    pts = []
    for i in range(spikes * 2):
        r = r_out if i % 2 == 0 else r_in
        a = math.pi * i / spikes - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.polygon(pts, fill=fill)


def glow(layer, cx, cy, r, rgb, peak=110):
    steps = 12
    for i in range(steps, 0, -1):
        a = int(peak * (1 - i / steps) ** 1.6)
        rr = r * i / steps
        layer.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=rgb + (a,))


def waves(d, y, x0, x1, color, amp=2, step=24, width=2):
    pts, x = [], x0
    while x <= x1:
        pts.append((x, y + amp * math.sin((x - x0) / 30.0)))
        x += step
    d.line(pts, fill=color, width=width, joint="curve")


# ---------------------------------------------------------------- canvas
img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
od = ImageDraw.Draw(ov)

MX = 24
CW = W - 2 * MX

# ------------------------------------------------------------- masthead
date = "WEDNESDAY 18 NOVEMBER 2026"
df = fit(d, date, CW, SERIF_B, 46)
dw = d.textlength(date, font=df)
d.text(((W - dw) / 2, 14), date, font=df, fill=INK)
sub = "ONE DAY OF WORLD NEWS, ONE PICTURE"
sf = fit(d, sub, CW, SANS_B, 19)
sw = d.textlength(sub, font=sf)
d.text(((W - sw) / 2, 64), sub, font=sf, fill=RED)
cnt = "40 STORIES  ·  7 REGIONS  ·  EVERY ONE FROM THIS WEDNESDAY"
cf = fit(d, cnt, CW, SANS_B, 15)
cw = d.textlength(cnt, font=cf)
d.text(((W - cw) / 2, 88), cnt, font=cf, fill=GREY)
d.line([(MX, 110), (W - MX, 110)], fill=RED, width=3)

# ------------------------------------------------------- timeline strip
TY0, TY1 = 116, 162
d.rectangle([MX, TY0, W - MX, TY1], fill=(232, 236, 238))
d.rectangle([MX, TY0, W - MX, TY1], outline=(190, 196, 200), width=1)
TL = [
    ("OVERNIGHT", "Russian strikes hit Odesa; 4 killed"),
    ("~06:00 UTC", "141 drones over Ukraine, 126 downed by 08:00"),
    ("~10:15 UTC", "Voyager 1 reaches one light-day (05:16 ET)"),
    ("MORNING", "Kerch Bridge hit, second day in a row"),
    ("AFTERNOON", "U.S. strikes Iran; Iran hits Kuwait & Bahrain"),
    ("EVENING", "Xi–Putin meet in Shenzhen"),
]
cell_w = CW / 6
for i, (t, ev) in enumerate(TL):
    x0 = MX + i * cell_w
    if i:
        d.line([(x0, TY0 + 6), (x0, TY1 - 6)], fill=(190, 196, 200), width=1)
    d.text((x0 + 8, TY0 + 5), t, font=font(SANS_B, 12), fill=INK)
    ef = font(SANS, 11)
    lines = wrap_text(d, ev, ef, cell_w - 16, max_lines=2)
    draw_lines(d, lines, x0 + 8, TY0 + 22, ef, (52, 56, 60), leading=13)
d.line([(MX, 168), (W - MX, 168)], fill=INK, width=2)


# ------------------------------------------------------------ hero panels
def vis_gulf(x0, y0, x1, y1):
    vgrad(d, (x0, y0, x1, y0 + 88), (14, 30, 52), (206, 110, 48))
    d.rectangle([x0, y0 + 88, x1, y1], fill=(16, 44, 58))
    waves(d, y0 + 100, x0 + 4, x1 - 4, (120, 170, 185), amp=2, step=22)
    d.polygon([(x0, y1), (x0, y0 + 66), (44, y0 + 78), (76, y0 + 66),
               (96, y1)], fill=(10, 24, 38))
    d.polygon([(x0 + 52, y0 + 96), (x0 + 78, y0 + 90), (x1 - 6, y0 + 94),
               (x1 - 10, y0 + 102), (x0 + 60, y0 + 102)], fill=(24, 52, 62))
    od.arc([x0 + 8, y0 + 6, x0 + 92, y0 + 60], start=200, end=340,
           fill=(255, 214, 130, 220), width=3)
    glow(od, x0 + 78, y0 + 92, 26, (255, 150, 40), peak=120)
    starburst(od, x0 + 78, y0 + 92, 15, 6, (255, 196, 90, 255))
    starburst(od, x0 + 78, y0 + 92, 7, 3, (255, 240, 190, 255))


def vis_kerch(x0, y0, x1, y1):
    vgrad(d, (x0, y0, x1, y0 + 84), (62, 96, 134), (176, 196, 208))
    d.rectangle([x0, y0 + 84, x1, y1], fill=(22, 48, 80))
    waves(d, y0 + 96, x0 + 4, x1 - 4, (110, 155, 185), amp=2, step=22)
    deck = y0 + 76
    # deck drawn INTACT: the 18 Nov story is a fresh strike that suspends
    # traffic, not the span collapse (that happened 17 Nov)
    d.rectangle([x0 + 6, deck, x1 - 6, deck + 6], fill=(204, 212, 220))
    od.arc([x0 + 14, deck - 34, x1 - 14, deck + 16], start=180, end=360,
           fill=(226, 232, 238, 255), width=4)
    d.rectangle([x0 + 18, deck + 6, x0 + 23, y0 + 84], fill=(180, 188, 196))
    d.rectangle([x1 - 23, deck + 6, x1 - 18, y0 + 84], fill=(180, 188, 196))
    for (sx, sy, sr, sa) in ((56, 62, 7, 90), (62, 50, 9, 76), (52, 40, 6, 60)):
        od.ellipse([x0 + sx - sr, y0 + sy - sr, x0 + sx + sr, y0 + sy + sr],
                   fill=(150, 156, 162, sa))


def vis_shenzhen(x0, y0, x1, y1):
    vgrad(d, (x0, y0, x1, y1), (96, 22, 22), (232, 116, 44))
    od.ellipse([x0 + 62, y0 + 52, x0 + 98, y0 + 88], fill=(255, 190, 90, 255))
    base = y1
    for (tx, th, twd) in ((0, 52, 20), (22, 78, 24), (48, 44, 18),
                          (68, 92, 26), (96, 60, 14)):
        d.rectangle([x0 + tx, base - th, x0 + tx + twd, base], fill=(38, 12, 12))
        for r in range(4, th - 5, 11):
            for c in range(4, twd - 4, 9):
                if (tx * 5 + r * 2 + c) % 4 < 2:
                    d.rectangle([x0 + tx + c, base - r - 3,
                                 x0 + tx + c + 2, base - r - 1],
                                fill=(255, 196, 96))
    for i, kind in enumerate(("cn", "ru")):
        fx = x0 + 10 + i * 30
        d.line([(fx, y0 + 14), (fx, y0 + 40)], fill=(240, 236, 228), width=2)
        if kind == "cn":
            d.rectangle([fx, y0 + 14, fx + 20, y0 + 26], fill=(222, 40, 28))
            starburst(d, fx + 5, y0 + 20, 3, 1, (255, 222, 80))
        else:
            for j, col in enumerate(((240, 240, 240), (30, 80, 180),
                                     (200, 30, 30))):
                d.rectangle([fx, y0 + 14 + j * 4, fx + 20, y0 + 18 + j * 4],
                            fill=col)


def vis_voyager(x0, y0, x1, y1):
    vgrad(d, (x0, y0, x1, y1), (8, 14, 30), (24, 38, 68))
    # stars
    for (sx, sy, sr) in ((10, 12, 1), (30, 8, 1), (55, 18, 2), (78, 10, 1),
                         (95, 22, 1), (18, 40, 1), (88, 44, 2), (40, 30, 1),
                         (70, 58, 1), (8, 66, 1), (100, 70, 1), (48, 78, 1),
                         (26, 92, 1), (92, 96, 1)):
        d.ellipse([x0 + sx - sr, y0 + sy - sr, x0 + sx + sr, y0 + sy + sr],
                  fill=(235, 238, 245))
    # distant Earth far behind, small and blue
    glow(od, x0 + 18, y0 + 92, 20, (120, 170, 235), peak=90)
    d.ellipse([x0 + 12, y0 + 86, x0 + 24, y0 + 98], fill=(150, 190, 240))
    # Voyager: dish + bus + boom
    cx, cy = x0 + 62, y0 + 50
    d.ellipse([cx - 26, cy - 26, cx + 26, cy + 26],
              outline=(200, 206, 214), width=2)
    d.line([(cx - 26, cy), (cx + 26, cy)], fill=(200, 206, 214), width=1)
    d.rectangle([cx - 4, cy, cx + 4, cy + 22], fill=(180, 188, 196))
    d.rectangle([cx - 12, cy + 22, cx + 12, cy + 30], fill=(150, 158, 166))
    d.line([(cx, cy + 30), (cx + 22, cy + 48)], fill=(200, 206, 214), width=2)
    starburst(d, cx + 24, cy + 50, 5, 2, (255, 208, 90))
    # faint signal arcs from the dish
    od.arc([cx - 34, cy - 34, cx + 34, cy + 34], start=200, end=340,
           fill=(255, 208, 90, 160), width=2)


HEROES = [
    dict(num=1, region="MIDDLE EAST", rc=RED, tag="THE GULF",
         headline="U.S. STRIKES IRAN",
         summary="Missile sites hit on Qeshm Island. Iran strikes back in Kuwait and Bahrain.",
         source="CONFIRMED · AP", vis=vis_gulf),
    dict(num=2, region="EUROPE", rc=BLUE, tag="UKRAINE",
         headline="KERCH BRIDGE HIT AGAIN",
         summary="Third attack in a week; traffic suspended.",
         source="CLAIM · KYIV", vis=vis_kerch),
    dict(num=3, region="ASIA", rc=TEAL, tag="CHINA",
         headline="XI AND PUTIN MEET",
         summary="Shenzhen talks before Thursday's trilateral summit with Trump.",
         source="CONFIRMED · AP", vis=vis_shenzhen),
    dict(num=4, region="SCIENCE", rc=CYAN, tag="SPACE",
         headline="VOYAGER 1, ONE LIGHT-DAY",
         summary="NASA probe reaches one light-day from Earth at 05:16 ET.",
         source="CONFIRMED · NASA", vis=vis_voyager),
]

HROWS = [(174, 298), (306, 430)]
HCOLS = [(MX, 504), (520, W - MX)]
for i, h in enumerate(HEROES):
    hx0, hx1 = HCOLS[i % 2]
    hy0, hy1 = HROWS[i // 2]
    d.rounded_rectangle([hx0, hy0, hx1, hy1], radius=10,
                        fill=(252, 250, 244), outline=(200, 194, 182), width=1)
    d.rounded_rectangle([hx0, hy0, hx1, hy0 + 5], radius=4, fill=h["rc"])
    h["vis"](hx0 + 2, hy0 + 7, hx0 + 112, hy1 - 2)
    tx = hx0 + 124
    d.text((tx, hy0 + 12), "%d · %s" % (h["num"], h["tag"]),
           font=font(SANS_B, 12), fill=h["rc"])
    hf = fit(d, h["headline"], hx1 - tx - 12, SANS_B, 20)
    d.text((tx, hy0 + 30), h["headline"], font=hf, fill=INK)
    sf = font(SANS, 13)
    lines = wrap_text(d, h["summary"], sf, hx1 - tx - 12, max_lines=2)
    draw_lines(d, lines, tx, hy0 + 56, sf, (56, 58, 62), leading=16)
    d.text((tx, hy1 - 20), h["source"], font=font(SANS_B, 11), fill=GREY)


# ------------------------------------------------------- grid of 12 stories
def tint(c, f=0.82):
    return lerp(c, (252, 250, 244), f)


def icon(kind, x, y, col):
    """Tiny 26x26 pictogram on a light tint square."""
    d.rectangle([x, y, x + 26, y + 26], fill=tint(col), outline=(210, 204, 192))
    c = col
    if kind == "chip":
        d.rectangle([x + 8, y + 8, x + 18, y + 18], outline=c, width=2)
        for px in (11, 15):
            for py in (4, 22):
                d.line([(x + px, y + py), (x + px, y + py + 3)], fill=c, width=2)
            for px2 in (4, 22):
                d.line([(x + px2, y + px), (x + px2 + 3, y + px)], fill=c, width=2)
    elif kind == "globe":
        d.ellipse([x + 5, y + 5, x + 21, y + 21], outline=c, width=2)
        d.arc([x + 9, y + 5, x + 17, y + 21], start=270, end=90, fill=c, width=1)
        d.arc([x + 9, y + 5, x + 17, y + 21], start=90, end=270, fill=c, width=1)
        d.line([(x + 5, y + 13), (x + 21, y + 13)], fill=c, width=1)
    elif kind == "drone":
        d.rectangle([x + 10, y + 11, x + 16, y + 15], fill=c)
        for (rx, ry) in ((5, 5), (19, 5), (5, 19), (19, 19)):
            d.ellipse([x + rx, y + ry, x + rx + 3, y + ry + 3], outline=c, width=1)
            d.line([(x + 13, y + 13), (x + rx + 1, y + ry + 1)], fill=c, width=1)
    elif kind == "scale":
        d.line([(x + 13, y + 5), (x + 13, y + 21)], fill=c, width=2)
        d.line([(x + 5, y + 7), (x + 21, y + 7)], fill=c, width=2)
        d.polygon([(x + 4, y + 8), (x + 9, y + 8), (x + 6, y + 13)], fill=c)
        d.polygon([(x + 17, y + 8), (x + 22, y + 8), (x + 19, y + 13)], fill=c)
        d.line([(x + 8, y + 21), (x + 18, y + 21)], fill=c, width=2)
    elif kind == "columns":
        for px in (7, 12, 17):
            d.rectangle([x + px, y + 9, x + px + 2, y + 18], fill=c)
        d.rectangle([x + 5, y + 6, x + 21, y + 8], fill=c)
        d.rectangle([x + 5, y + 19, x + 21, y + 21], fill=c)
    elif kind == "euro":
        d.text((x + 7, y + 4), "€", font=font(SANS_B, 18), fill=c)
    elif kind == "pin":
        d.ellipse([x + 8, y + 5, x + 18, y + 15], outline=c, width=2)
        d.polygon([(x + 10, y + 13), (x + 16, y + 13), (x + 13, y + 22)], fill=c)
        d.ellipse([x + 11, y + 8, x + 15, y + 12], fill=c)
    elif kind == "burst":
        starburst(d, x + 13, y + 13, 10, 4, c, spikes=8)
    elif kind == "chart":
        d.line([(x + 5, y + 20), (x + 11, y + 14), (x + 15, y + 16),
                (x + 21, y + 7)], fill=c, width=2, joint="curve")
        d.polygon([(x + 21, y + 7), (x + 16, y + 7), (x + 21, y + 12)], fill=c)


GRID = [
    (5, "TECH", SLATE, "ANTHROPIC IPO: $81B",
     "Biggest-ever offering.", "REUTERS", "chart"),
    (6, "ASIA", TEAL, "QUAD MEETS IN MANILA",
     "First leaders' meeting in 2+ years.", "AP", "globe"),
    (7, "ASIA", TEAL, "APEC OPENS IN SHENZHEN",
     "Leaders gather as Xi greets Trump.", "AP", "globe"),
    (8, "MIDDLE EAST", RED, "HOUTHIS HIT SAUDI PIPELINE",
     "Five drones hit pipeline stations.", "AL JAZEERA", "drone"),
    (9, "MIDDLE EAST", RED, "950,000 IN GAZA FLOOD ZONE",
     "Displaced face a fourth winter.", "UN NEWS", "pin"),
    (10, "MARKETS", SLATE, "FED MINUTES: MORE HIKES",
     "Almost all officials see hikes.", "REUTERS", "chart"),
    (11, "EUROPE", BLUE, "EU PROPOSES €45B LOAN",
     "Loan to be repaid by Russia.", "REUTERS", "euro"),
    (12, "MIDDLE EAST", RED, "ISRAEL PUSHES INTO GAZA",
     "Operation moves past Yellow Line.", "AL JAZEERA", "pin"),
    (13, "EUROPE", BLUE, "RUSSIAN STRIKES HIT ODESA",
     "Four killed in overnight attacks.", "CLAIM · KYIV", "burst"),
    (14, "EUROPE", BLUE, "DRONES OVER DNIPRO",
     "141 drones counted, 126 downed.", "CLAIM · KYIV", "drone"),
    (15, "MARKETS", SLATE, "GOLD SLUMPS BELOW $3,800",
     "Gold falls as dollar rallies.", "REUTERS", "chart"),
    (16, "MARKETS", SLATE, "STOCKS SLIP, NIKKEI GAINS",
     "Dow −1.1%; Nikkei +1.0%.", "REUTERS", "chart"),
]

d.text((MX, 436), "THE DAY'S STORIES  ·  5–16", font=font(SANS_B, 14), fill=INK)
d.line([(MX, 454), (W - MX, 454)], fill=INK, width=2)
GCOLS = [(MX, 264), (272, 512), (520, 760), (768, W - MX)]
GROWS = [(458, 522), (522, 586), (586, 650)]
for i, (num, region, rc, head, summ, src, ic) in enumerate(GRID):
    gx0, gx1 = GCOLS[i % 4]
    gy0, gy1 = GROWS[i // 4]
    # number badge + region tag + source on the top line
    d.ellipse([gx0, gy0 + 2, gx0 + 18, gy0 + 20], fill=rc)
    nt = str(num)
    nw = d.textlength(nt, font=font(SANS_B, 11))
    d.text((gx0 + (18 - nw) / 2, gy0 + 4), nt, font=font(SANS_B, 11), fill=WHITE)
    d.text((gx0 + 24, gy0 + 4), region, font=font(SANS_B, 11), fill=rc)
    sw = d.textlength(src, font=font(SANS, 10))
    d.text((gx1 - sw, gy0 + 5), src, font=font(SANS, 10), fill=GREY)
    # tiny icon + headline + one-line summary
    icon(ic, gx0, gy0 + 24, rc)
    hf = font(SANS_B, 13)
    lines = wrap_text(d, head, hf, gx1 - gx0 - 38, max_lines=2)
    y = draw_lines(d, lines, gx0 + 34, gy0 + 22, hf, INK, leading=15)
    sf = font(SANS, 11)
    sl = wrap_text(d, summ, sf, gx1 - gx0 - 38, max_lines=1)
    draw_lines(d, sl, gx0 + 34, y + 2, sf, (56, 58, 62), leading=13)


# ------------------------------------------------------- world map
d.text((MX, 656), "WHERE IT HAPPENED", font=font(SANS_B, 14), fill=INK)
leg = [("Europe", BLUE), ("Middle East", RED), ("Asia", TEAL),
       ("Americas", PURPLE), ("Tech / Markets", SLATE)]
lx = W - MX
for name, col in reversed(leg):
    tw = d.textlength(name, font=font(SANS, 10))
    lx -= tw
    d.text((lx, 660), name, font=font(SANS, 10), fill=GREY)
    d.ellipse([lx - 12, 660, lx - 4, 668], fill=col)
    lx -= 20
MAP = (MX, 672, W - MX, 772)
d.rectangle(MAP, fill=(228, 236, 240), outline=(190, 196, 200), width=1)
LAND = (214, 204, 184)
EDGE = (180, 170, 150)
CONTINENTS = [
    [(60, 700), (110, 684), (200, 682), (280, 690), (290, 712),
     (260, 730), (200, 740), (120, 738), (70, 724)],
    [(300, 680), (330, 678), (335, 690), (310, 692)],
    [(290, 738), (330, 738), (325, 768), (295, 770), (282, 752)],
    [(480, 684), (545, 682), (560, 696), (540, 708), (500, 706), (478, 696)],
    [(480, 712), (560, 712), (575, 740), (555, 770), (510, 770), (488, 742)],
    [(560, 682), (940, 682), (950, 710), (920, 740), (860, 748),
     (760, 745), (680, 738), (600, 724), (560, 706)],
    [(880, 752), (950, 752), (945, 768), (890, 768)],
]
for poly in CONTINENTS:
    d.polygon(poly, fill=LAND, outline=EDGE)
DOTS = [
    (1, 624, 708, RED), (2, 536, 684, BLUE), (3, 845, 712, TEAL),
    (5, 130, 722, PURPLE), (6, 895, 744, TEAL),
    (7, 872, 730, TEAL), (8, 606, 736, RED), (9, 572, 706, RED),
    (10, 90, 712, PURPLE), (11, 498, 686, BLUE), (12, 560, 730, RED),
    (13, 542, 716, BLUE), (14, 550, 694, BLUE), (15, 165, 700, PURPLE),
    (16, 200, 726, PURPLE),
]
# note: no dot for #4 (Voyager 1 is in space, no Earth location)
for num, cx, cy, col in DOTS:
    d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=col,
              outline=WHITE, width=1)
    nt = str(num)
    nw = d.textlength(nt, font=font(SANS_B, 10))
    d.text((cx - nw / 2, cy - 6), nt, font=font(SANS_B, 10), fill=WHITE)

# ------------------------------------------------------------ also list
d.text((MX, 778), "ALSO ON WEDNESDAY 18 NOVEMBER",
       font=font(SANS_B, 14), fill=INK)
ALSO = [
    "Cyclone Xavier, cat 5, hits the Northern Cook Islands",
    "UniCredit, Germany agree on Commerzbank takeover",
    "Startup Calif finds critical Java flaw using AI",
    "Russian military plane crashes in Siberia; 19 killed",
    "India's wholesale inflation 12.29%, highest in 4 years",
    "India–Japan 2+2 dialogue opens in Tokyo",
    "Putin not ready for serious Ukraine peace talks (NYT)",
    "U.S. officer accused of spying for Russia in custody",
    "Trump meets Marcos Jr.; Xi greets Trump in Shenzhen",
    "Canada's Carney to meet Trump at APEC",
    "Myanmar to review its ASEAN relationship",
    "NATO unveils next-generation communications strategy",
    "South Korea's Lee strengthens ties with Beijing at APEC",
    "Salesforce shares plunge 9.5% on tech decline",
    "Xiaomi 18 Pro and Pro Max launch globally in Paris",
    "Samsung rolls out One UI 9 on the Galaxy A24",
    "Slay the Spire 2 sells ~8M units on Steam",
    "Alonso & Loeb join Aston Martin's 2027 Dakar effort",
    "USMNT beats Haiti 2–0",
    "Pakistani man gets 27 years for Iran-backed plot to kill Trump",
    "Dual quasar pumps 3.6× expected heat into early universe",
    "OCC banking reform frees $64B for community banks",
    "Trump makes third Supreme Court trip over Venezuela deportations",
    "U.S. seeks Microsoft briefing on ByteDance AI deal talks",
]
af = font(SANS, 12)
for i, item in enumerate(ALSO):
    col = 0 if i < 12 else 1
    ax = MX + col * 500
    ay = 794 + (i % 12) * 13
    num = "%d." % (17 + i)
    d.text((ax, ay), num, font=font(SANS_B, 12), fill=RED)
    nx = ax + d.textlength(num, font=font(SANS_B, 12)) + 5
    txt = item
    while d.textlength(txt, font=af) > (W - MX - nx) and " " in txt:
        txt = txt.rsplit(" ", 1)[0] + " …"
    d.text((nx, ay), txt, font=af, fill=INK)

# ------------------------------------------------------------ date check
d.rounded_rectangle([MX, 952, W - MX, 999], radius=8,
                    fill=(250, 244, 214), outline=(200, 170, 90), width=1)
d.text((MX + 12, 957), "DATE CHECK", font=font(SANS_B, 11), fill=RED)
dcf = font(SANS, 10)
lab_w = d.textlength("DATE CHECK", font=font(SANS_B, 11))
dc1 = ("LEFT OUT — broke before 18 Nov: Peltola wins Alaska Senate (Tue 17 Nov) · "
       "Nvidia Q3 results (Tue 17 Nov) · Kahana elected speaker (Tue 17 Nov) ·")
dc2 = ("Kerch span falls (Tue 17 Nov) · Board of Peace report (Tue 17 Nov) · "
       "Ebola 11,000 (11–15 Nov) · Huang quits Nvidia (12–13 Nov) · "
       "FAA ground stop (13 Nov) · Hormuz tankers (16 Nov)")
dc3 = ("NOT YET — due after 18 Nov: Xi–Trump–Putin trilateral (Thu 19 Nov) · "
       "Cyclone Akvan landfall (Fri 20 Nov)")
d.text((MX + 12 + lab_w + 8, 957), dc1, font=dcf, fill=INK)
d.text((MX + 12, 969), dc2, font=dcf, fill=INK)
d.text((MX + 12, 981), dc3, font=dcf, fill=INK)

# ---------------------------------------------------------------- footer
foot = ("Every story happened or was first reported on Wed 18 Nov 2026. "
        "CLAIM = one side's account. Sources: AP, Reuters, AFP, Al Jazeera, "
        "NPR, PAHO, UN News, NASA. Original drawings.")
ff = font(SANS, 10)
fw = d.textlength(foot, font=ff)
d.text(((W - fw) / 2, 1004), foot, font=ff, fill=GREY)

# ------------------------------------------------------------------ save
img = Image.alpha_composite(img.convert("RGBA"), ov).convert("RGB")
img.save("entry.png", optimize=True)
print("saved entry.png", img.size, img.mode)
