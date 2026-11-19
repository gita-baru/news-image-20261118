#!/usr/bin/env python3
"""Draw the v3 news image for 18 November 2026 (1024x1024 PNG).

Build tool only: the entry program (main.ts) copies the finished entry.png.
Run: python3 draw.py  ->  writes entry.png beside this file.

Layout (breadth + discipline, after the 17 November winner and the v2.1
fix): masthead with the date and a story count, a "THE DAY IN UTC"
timeline, 4 hero stories with detailed drawn scenes, a numbered grid of
12 more stories (5-16) with small scene icons, a world map with numbered
dots, a dense "ALSO" list (17-50), a DATE CHECK box naming big stories
left out because they broke before 18 November and things not yet due,
and a sources footer. 50 stories, 7 regions. Every dated claim is from
the verified 18 November 2026 story list; nothing is invented.
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


def waves(d, y, x0, x1, color, amp=2, step=22, width=2):
    pts, x = [], x0
    while x <= x1:
        pts.append((x, y + amp * math.sin((x - x0) / 30.0)))
        x += step
    d.line(pts, fill=color, width=width, joint="curve")


def bird(d, x, y, col, s=4):
    d.arc([x - s, y - s, x, y + s], start=200, end=340, fill=col, width=1)
    d.arc([x, y - s, x + s, y + s], start=200, end=340, fill=col, width=1)


# ---------------------------------------------------------------- canvas
img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
od = ImageDraw.Draw(ov)

MX = 24
CW = W - 2 * MX

# ------------------------------------------------------------- masthead
date = "WEDNESDAY 18 NOVEMBER 2026"
df = fit(d, date, CW, SERIF_B, 44)
dw = d.textlength(date, font=df)
d.text(((W - dw) / 2, 12), date, font=df, fill=INK)
sub = "ONE DAY OF WORLD NEWS, ONE PICTURE"
sf = fit(d, sub, CW, SANS_B, 18)
sw = d.textlength(sub, font=sf)
d.text(((W - sw) / 2, 60), sub, font=sf, fill=RED)
cnt = "50 STORIES  ·  7 REGIONS  ·  EVERY ONE FROM THIS WEDNESDAY"
cf = fit(d, cnt, CW, SANS_B, 15)
cw = d.textlength(cnt, font=cf)
d.text(((W - cw) / 2, 84), cnt, font=cf, fill=GREY)
d.line([(MX, 106), (W - MX, 106)], fill=RED, width=3)

# ------------------------------------------------------- timeline strip
TY0, TY1 = 112, 156
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
        d.line([(x0, TY0 + 5), (x0, TY1 - 5)], fill=(190, 196, 200), width=1)
    d.text((x0 + 8, TY0 + 4), t, font=font(SANS_B, 12), fill=INK)
    ef = font(SANS, 11)
    lines = wrap_text(d, ev, ef, cell_w - 16, max_lines=2)
    draw_lines(d, lines, x0 + 8, TY0 + 20, ef, (52, 56, 60), leading=13)
d.line([(MX, 162), (W - MX, 162)], fill=INK, width=2)


# ------------------------------------------------------------ hero scenes
# Each visual fills a ~106x91 box; scenes are deliberately detailed:
# a dusk Gulf with radar mast, missile trails and two blasts; a bridge
# under smoke with a boat and gulls; a Shenzhen sunset skyline with a
# spired tower and two flags; Voyager in a dense starfield with Earth
# far behind and the Sun glowing at the edge.

def vis_gulf(x0, y0, x1, y1):
    # dusk sky over the sea
    vgrad(d, (x0, y0, x1, y0 + 58), (14, 30, 52), (206, 110, 48))
    d.rectangle([x0, y0 + 58, x1, y1], fill=(16, 44, 58))
    # low sun arc, upper left
    od.arc([x0 + 6, y0 + 4, x0 + 70, y0 + 48], start=200, end=340,
           fill=(255, 214, 130, 220), width=3)
    # coastline silhouette, left
    d.polygon([(x0, y1), (x0, y0 + 46), (26, y0 + 56), (44, y0 + 48),
               (58, y0 + 58), (58, y1)], fill=(10, 24, 38))
    # radar mast on the coast, dish sweeping
    d.line([(x0 + 30, y0 + 50), (x0 + 30, y0 + 22)], fill=(200, 206, 214),
           width=2)
    d.line([(x0 + 30, y0 + 50), (x0 + 22, y0 + 58)], fill=(200, 206, 214),
           width=2)
    d.line([(x0 + 30, y0 + 50), (x0 + 38, y0 + 58)], fill=(200, 206, 214),
           width=2)
    od.ellipse([x0 + 22, y0 + 12, x0 + 38, y0 + 28],
               outline=(235, 240, 246, 255), width=2)
    d.line([(x0 + 30, y0 + 20), (x0 + 44, y0 + 10)], fill=(235, 240, 246),
           width=1)
    # missile trails arcing down from the top right
    od.line([(x0 + 96, y0 + 6), (x0 + 78, y0 + 40), (x0 + 70, y0 + 62)],
            fill=(255, 220, 150, 230), width=2, joint="curve")
    od.line([(x0 + 104, y0 + 18), (x0 + 92, y0 + 48), (x0 + 88, y0 + 68)],
            fill=(255, 220, 150, 200), width=2, joint="curve")
    # two blasts on the water
    glow(od, x0 + 70, y0 + 66, 22, (255, 150, 40), peak=130)
    starburst(od, x0 + 70, y0 + 66, 13, 5, (255, 196, 90, 255))
    starburst(od, x0 + 70, y0 + 66, 6, 2, (255, 240, 190, 255))
    glow(od, x0 + 90, y0 + 72, 14, (255, 150, 40), peak=110)
    starburst(od, x0 + 90, y0 + 72, 8, 3, (255, 196, 90, 255))
    # small ship on the sea, right
    d.polygon([(x0 + 52, y0 + 74), (x0 + 76, y0 + 74), (x0 + 72, y0 + 80),
               (x0 + 56, y0 + 80)], fill=(24, 52, 62))
    d.line([(x0 + 64, y0 + 74), (x0 + 64, y0 + 64)], fill=(200, 206, 214),
           width=1)
    waves(d, y0 + 84, x0 + 4, x1 - 4, (120, 170, 185), amp=2, step=22)


def vis_kerch(x0, y0, x1, y1):
    # pale morning sky over the strait
    vgrad(d, (x0, y0, x1, y0 + 56), (62, 96, 134), (176, 196, 208))
    d.rectangle([x0, y0 + 56, x1, y1], fill=(22, 48, 80))
    # gulls
    bird(d, x0 + 22, y0 + 14, (240, 244, 248))
    bird(d, x0 + 38, y0 + 20, (240, 244, 248))
    bird(d, x0 + 88, y0 + 12, (240, 244, 248))
    # bridge deck drawn INTACT: the 18 Nov story is a fresh strike that
    # suspends traffic, not the span collapse (that happened 17 Nov)
    deck = y0 + 52
    d.rectangle([x0 + 6, deck, x1 - 6, deck + 6], fill=(204, 212, 220))
    od.arc([x0 + 14, deck - 32, x1 - 14, deck + 16], start=180, end=360,
           fill=(226, 232, 238, 255), width=4)
    d.rectangle([x0 + 18, deck + 6, x0 + 23, y0 + 68], fill=(180, 188, 196))
    d.rectangle([x1 - 23, deck + 6, x1 - 18, y0 + 68], fill=(180, 188, 196))
    # smoke columns rising from two hits on the deck
    for (sx, sy, sr, sa) in ((56, 40, 7, 90), (62, 28, 9, 76),
                             (52, 18, 6, 60), (84, 44, 6, 80),
                             (88, 32, 8, 66)):
        od.ellipse([x0 + sx - sr, y0 + sy - sr, x0 + sx + sr, y0 + sy + sr],
                   fill=(150, 156, 162, sa))
    # small flash on the deck
    starburst(od, x0 + 62, deck - 2, 6, 2, (255, 190, 80, 255))
    # boat below the bridge, waves
    d.polygon([(x0 + 40, y0 + 68), (x0 + 64, y0 + 68), (x0 + 60, y0 + 74),
               (x0 + 44, y0 + 74)], fill=(30, 60, 78))
    d.line([(x0 + 52, y0 + 68), (x0 + 52, y0 + 60)], fill=(200, 206, 214),
           width=1)
    waves(d, y0 + 80, x0 + 4, x1 - 4, (110, 155, 185), amp=2, step=22)


def vis_shenzhen(x0, y0, x1, y1):
    # sunset over the skyline
    vgrad(d, (x0, y0, x1, y1), (96, 22, 22), (232, 116, 44))
    # big low sun
    od.ellipse([x0 + 58, y0 + 34, x0 + 92, y0 + 68], fill=(255, 190, 90, 255))
    # birds
    bird(d, x0 + 16, y0 + 16, (255, 220, 160))
    bird(d, x0 + 30, y0 + 24, (255, 220, 160))
    # skyline: eight towers, one tall spired landmark
    base = y1
    towers = ((0, 40, 14), (16, 62, 16), (34, 34, 12), (48, 78, 18),
              (68, 50, 14), (84, 66, 16), (100, 38, 6))
    for (tx, th, twd) in towers:
        d.rectangle([x0 + tx, base - th, x0 + tx + twd, base],
                    fill=(38, 12, 12))
        for r in range(4, th - 5, 10):
            for c in range(3, twd - 3, 7):
                if (tx * 5 + r * 2 + c) % 4 < 2:
                    d.rectangle([x0 + tx + c, base - r - 3,
                                 x0 + tx + c + 2, base - r - 1],
                                fill=(255, 196, 96))
    # spired landmark tower, centre-right
    tx, th, twd = 48, 78, 18
    d.polygon([(x0 + tx + 3, base - th), (x0 + tx + twd - 3, base - th),
               (x0 + tx + twd // 2, base - th - 12)], fill=(38, 12, 12))
    d.line([(x0 + tx + twd // 2, base - th - 12),
            (x0 + tx + twd // 2, base - th - 18)], fill=(255, 196, 96),
           width=2)
    # two flags on poles, upper left
    for i, kind in enumerate(("cn", "ru")):
        fx = x0 + 8 + i * 26
        d.line([(fx, y0 + 10), (fx, y0 + 32)], fill=(240, 236, 228), width=2)
        if kind == "cn":
            d.rectangle([fx, y0 + 10, fx + 18, y0 + 21], fill=(222, 40, 28))
            starburst(d, fx + 4, y0 + 15, 3, 1, (255, 222, 80))
        else:
            for j, col in enumerate(((240, 240, 240), (30, 80, 180),
                                     (200, 30, 30))):
                d.rectangle([fx, y0 + 10 + j * 4, fx + 18, y0 + 14 + j * 4],
                            fill=col)


def vis_voyager(x0, y0, x1, y1):
    # deep space
    vgrad(d, (x0, y0, x1, y1), (8, 14, 30), (24, 38, 68))
    # dense starfield
    stars = ((8, 10, 1), (26, 6, 1), (48, 14, 2), (70, 8, 1), (92, 18, 1),
             (16, 30, 1), (84, 36, 2), (36, 24, 1), (62, 44, 1),
             (6, 52, 1), (96, 56, 1), (44, 62, 1), (22, 76, 1),
             (88, 80, 1), (12, 84, 1), (58, 84, 1), (76, 68, 1),
             (34, 82, 1), (100, 40, 1), (52, 6, 1), (10, 66, 1),
             (68, 22, 1), (40, 44, 1), (96, 86, 1), (28, 52, 1))
    for (sx, sy, sr) in stars:
        d.ellipse([x0 + sx - sr, y0 + sy - sr, x0 + sx + sr, y0 + sy + sr],
                  fill=(235, 238, 245))
    # the Sun glowing at the top right edge
    glow(od, x0 + 104, y0 + 4, 26, (255, 210, 110), peak=120)
    # distant Earth far behind, small and blue, lower left
    glow(od, x0 + 16, y0 + 80, 18, (120, 170, 235), peak=90)
    d.ellipse([x0 + 10, y0 + 74, x0 + 22, y0 + 86], fill=(150, 190, 240))
    d.ellipse([x0 + 13, y0 + 77, x0 + 19, y0 + 83], fill=(110, 160, 220))
    # Voyager: big dish, bus, boom with RTG fins
    cx, cy = x0 + 58, y0 + 42
    d.ellipse([cx - 24, cy - 24, cx + 24, cy + 24],
              outline=(200, 206, 214), width=2)
    d.line([(cx - 24, cy), (cx + 24, cy)], fill=(200, 206, 214), width=1)
    d.line([(cx, cy - 24), (cx, cy + 24)], fill=(200, 206, 214), width=1)
    d.rectangle([cx - 4, cy, cx + 4, cy + 20], fill=(180, 188, 196))
    d.rectangle([cx - 12, cy + 20, cx + 12, cy + 28], fill=(150, 158, 166))
    # boom to the RTG
    d.line([(cx, cy + 28), (cx + 20, cy + 44)], fill=(200, 206, 214), width=2)
    for k in range(3):
        fx = cx + 14 + k * 4
        fy = cy + 38 + k * 3
        d.line([(fx, fy - 4), (fx, fy + 4)], fill=(220, 226, 232), width=2)
    starburst(d, cx + 22, cy + 46, 5, 2, (255, 208, 90))
    # faint signal arcs from the dish
    od.arc([cx - 32, cy - 32, cx + 32, cy + 32], start=200, end=340,
           fill=(255, 208, 90, 160), width=2)
    od.arc([cx - 40, cy - 40, cx + 40, cy + 40], start=200, end=340,
           fill=(255, 208, 90, 90), width=1)


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

HROWS = [(168, 268), (274, 374)]
HCOLS = [(MX, 504), (520, W - MX)]
for i, h in enumerate(HEROES):
    hx0, hx1 = HCOLS[i % 2]
    hy0, hy1 = HROWS[i // 2]
    d.rounded_rectangle([hx0, hy0, hx1, hy1], radius=10,
                        fill=(252, 250, 244), outline=(200, 194, 182), width=1)
    d.rounded_rectangle([hx0, hy0, hx1, hy0 + 5], radius=4, fill=h["rc"])
    h["vis"](hx0 + 2, hy0 + 7, hx0 + 108, hy1 - 2)
    tx = hx0 + 120
    d.text((tx, hy0 + 9), "%d · %s" % (h["num"], h["tag"]),
           font=font(SANS_B, 12), fill=h["rc"])
    hf = fit(d, h["headline"], hx1 - tx - 12, SANS_B, 19)
    d.text((tx, hy0 + 27), h["headline"], font=hf, fill=INK)
    sf = font(SANS, 13)
    lines = wrap_text(d, h["summary"], sf, hx1 - tx - 12, max_lines=2)
    draw_lines(d, lines, tx, hy0 + 51, sf, (56, 58, 62), leading=15)
    d.text((tx, hy1 - 17), h["source"], font=font(SANS_B, 11), fill=GREY)


# ------------------------------------------------------- grid of 12 stories
def tint(c, f=0.82):
    return lerp(c, (252, 250, 244), f)


def icon(kind, x, y, col):
    """A 26x26 pictogram on a light tint square; each kind is a tiny
    scene rather than a bare shape."""
    d.rectangle([x, y, x + 26, y + 26], fill=tint(col), outline=(210, 204, 192))
    c = col
    if kind == "chart":
        # three rising bars with a trend line and arrow
        for j, bh in enumerate((6, 10, 14)):
            d.rectangle([x + 6 + j * 6, y + 20 - bh, x + 10 + j * 6, y + 20],
                        fill=c)
        d.line([(x + 5, y + 16), (x + 11, y + 11), (x + 15, y + 13),
                (x + 21, y + 5)], fill=RED, width=2, joint="curve")
        d.polygon([(x + 21, y + 5), (x + 16, y + 5), (x + 21, y + 10)],
                  fill=RED)
    elif kind == "globe":
        d.ellipse([x + 5, y + 5, x + 21, y + 21], outline=c, width=2)
        d.arc([x + 9, y + 5, x + 17, y + 21], start=270, end=90, fill=c, width=1)
        d.arc([x + 9, y + 5, x + 17, y + 21], start=90, end=270, fill=c, width=1)
        d.line([(x + 5, y + 13), (x + 21, y + 13)], fill=c, width=1)
        d.ellipse([x + 9, y + 8, x + 13, y + 11], fill=c)
    elif kind == "flags":
        # four small flags meeting (Quad)
        for j, fcol in enumerate(((30, 80, 180), (200, 30, 30),
                                  (20, 120, 90), (178, 36, 28))):
            fx = x + 4 + j * 5
            d.line([(fx, y + 6), (fx, y + 20)], fill=c, width=1)
            d.polygon([(fx, y + 6), (fx + 5, y + 8), (fx, y + 11)], fill=fcol)
    elif kind == "skyline":
        # three towers with lit windows (APEC)
        for j, (bx, bh) in enumerate(((5, 12), (11, 18), (18, 10))):
            d.rectangle([x + bx, y + 21 - bh, x + bx + 5, y + 21], fill=c)
            d.rectangle([x + bx + 1, y + 21 - bh + 2, x + bx + 3,
                         y + 21 - bh + 4], fill=(255, 196, 96))
    elif kind == "drone":
        d.rectangle([x + 10, y + 11, x + 16, y + 15], fill=c)
        for (rx, ry) in ((5, 5), (19, 5), (5, 19), (19, 19)):
            d.ellipse([x + rx, y + ry, x + rx + 3, y + ry + 3], outline=c, width=1)
            d.line([(x + 13, y + 13), (x + rx + 1, y + ry + 1)], fill=c, width=1)
        # motion lines
        d.line([(x + 4, y + 6), (x + 8, y + 6)], fill=c, width=1)
        d.line([(x + 4, y + 22), (x + 8, y + 22)], fill=c, width=1)
    elif kind == "waves":
        # flood water over ground
        d.rectangle([x + 4, y + 19, x + 22, y + 22], fill=c)
        for wy in (8, 13):
            pts = [(x + 4 + k * 3, y + wy + (2 if k % 2 else -1))
                   for k in range(7)]
            d.line(pts, fill=c, width=2, joint="curve")
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
        starburst(d, x + 13, y + 13, 4, 2, (255, 196, 90), spikes=8)
    elif kind == "bars":
        # stacked gold bars
        for j, (bx, by) in enumerate(((8, 16), (14, 16), (11, 10))):
            d.polygon([(x + bx, y + by + 5), (x + bx + 2, y + by),
                       (x + bx + 6, y + by), (x + bx + 8, y + by + 5)],
                      fill=(196, 140, 20))
            d.line([(x + bx + 2, y + by), (x + bx + 6, y + by)],
                   fill=(255, 214, 110), width=1)


GRID = [
    (5, "TECH", SLATE, "ANTHROPIC IPO: $81B",
     "Biggest-ever offering.", "REUTERS", "chart"),
    (6, "ASIA", TEAL, "QUAD MEETS IN MANILA",
     "First leaders' meeting in 2+ years.", "AP", "flags"),
    (7, "ASIA", TEAL, "APEC OPENS IN SHENZHEN",
     "Leaders gather as Xi greets Trump.", "AP", "skyline"),
    (8, "MIDDLE EAST", RED, "HOUTHIS HIT SAUDI PIPELINE",
     "Five drones hit pipeline stations.", "AL JAZEERA", "drone"),
    (9, "MIDDLE EAST", RED, "950,000 IN GAZA FLOOD ZONE",
     "Displaced face a fourth winter.", "UN NEWS", "waves"),
    (10, "MARKETS", SLATE, "FED MINUTES: MORE HIKES",
     "Almost all officials see hikes.", "REUTERS", "columns"),
    (11, "EUROPE", BLUE, "EU PROPOSES €45B LOAN",
     "Loan to be repaid by Russia.", "REUTERS", "euro"),
    (12, "MIDDLE EAST", RED, "ISRAEL PUSHES INTO GAZA",
     "Operation moves past Yellow Line.", "AL JAZEERA", "pin"),
    (13, "EUROPE", BLUE, "RUSSIAN STRIKES HIT ODESA",
     "Four killed in overnight attacks.", "CLAIM · KYIV", "burst"),
    (14, "EUROPE", BLUE, "DRONES OVER DNIPRO",
     "141 drones counted, 126 downed.", "CLAIM · KYIV", "drone"),
    (15, "MARKETS", SLATE, "GOLD SLUMPS BELOW $3,800",
     "Gold falls as dollar rallies.", "REUTERS", "bars"),
    (16, "MARKETS", SLATE, "STOCKS SLIP, NIKKEI GAINS",
     "Dow −1.1%; Nikkei +1.0%.", "REUTERS", "chart"),
]

d.text((MX, 380), "THE DAY'S STORIES  ·  5–16", font=font(SANS_B, 14), fill=INK)
d.line([(MX, 398), (W - MX, 398)], fill=INK, width=2)
GCOLS = [(MX, 264), (272, 512), (520, 760), (768, W - MX)]
GROWS = [(402, 462), (462, 522), (522, 582)]
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
    # small scene icon + headline + one-line summary
    icon(ic, gx0, gy0 + 24, rc)
    hf = font(SANS_B, 13)
    lines = wrap_text(d, head, hf, gx1 - gx0 - 38, max_lines=2)
    y = draw_lines(d, lines, gx0 + 34, gy0 + 22, hf, INK, leading=15)
    sf = font(SANS, 11)
    sl = wrap_text(d, summ, sf, gx1 - gx0 - 38, max_lines=1)
    draw_lines(d, sl, gx0 + 34, y + 2, sf, (56, 58, 62), leading=13)


# ------------------------------------------------------- world map
d.text((MX, 588), "WHERE IT HAPPENED", font=font(SANS_B, 14), fill=INK)
leg = [("Europe", BLUE), ("Middle East", RED), ("Asia", TEAL),
       ("Americas", PURPLE), ("Africa", BROWN), ("Tech / Markets", SLATE)]
lx = W - MX
for name, col in reversed(leg):
    tw = d.textlength(name, font=font(SANS, 10))
    lx -= tw
    d.text((lx, 592), name, font=font(SANS, 10), fill=GREY)
    d.ellipse([lx - 12, 592, lx - 4, 600], fill=col)
    lx -= 20
MAP = (MX, 604, W - MX, 704)
d.rectangle(MAP, fill=(228, 236, 240), outline=(190, 196, 200), width=1)
LAND = (214, 204, 184)
EDGE = (180, 170, 150)
CONTINENTS = [
    [(60, 632), (110, 616), (200, 614), (280, 622), (290, 644),
     (260, 662), (200, 672), (120, 670), (70, 656)],
    [(300, 612), (330, 610), (335, 622), (310, 624)],
    [(290, 670), (330, 670), (325, 700), (295, 702), (282, 684)],
    [(480, 616), (545, 614), (560, 628), (540, 640), (500, 638), (478, 628)],
    [(480, 644), (560, 644), (575, 672), (555, 702), (510, 702), (488, 674)],
    [(560, 614), (940, 614), (950, 642), (920, 672), (860, 680),
     (760, 677), (680, 670), (600, 656), (560, 638)],
    [(880, 684), (950, 684), (945, 700), (890, 700)],
]
for poly in CONTINENTS:
    d.polygon(poly, fill=LAND, outline=EDGE)
DOTS = [
    (1, 624, 640, RED), (2, 536, 616, BLUE), (3, 845, 644, TEAL),
    (5, 130, 654, PURPLE), (6, 895, 676, TEAL),
    (7, 872, 662, TEAL), (8, 606, 668, RED), (9, 572, 638, RED),
    (10, 90, 644, PURPLE), (11, 498, 618, BLUE), (12, 560, 662, RED),
    (13, 542, 648, BLUE), (14, 550, 626, BLUE), (15, 165, 632, PURPLE),
    (16, 200, 658, PURPLE),
    (41, 528, 690, BROWN), (42, 492, 660, BROWN), (43, 548, 674, BROWN),
    (44, 600, 694, BROWN), (45, 308, 676, PURPLE), (46, 292, 684, PURPLE),
    (47, 306, 694, PURPLE), (48, 922, 632, TEAL), (49, 818, 656, TEAL),
    (50, 590, 624, TEAL),
]
# note: no dot for #4 (Voyager 1 is in space, no Earth location)
for num, cx, cy, col in DOTS:
    d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=col,
              outline=WHITE, width=1)
    nt = str(num)
    nf = font(SANS_B, 9) if num >= 10 else font(SANS_B, 10)
    nw = d.textlength(nt, font=nf)
    d.text((cx - nw / 2, cy - 6), nt, font=nf, fill=WHITE)

# ------------------------------------------------------------ also list
d.text((MX, 710), "ALSO ON WEDNESDAY 18 NOVEMBER",
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
    "Mozambique: opposition leader Mondlane on trial",
    "Guinea jails 224 over illegal gold mining",
    "Ethiopia–Eritrea: artillery fire near Badme",
    "Mauritius sets UK a December Chagos deadline",
    "Venezuela: unions call 24-hour strike over pay",
    "Colombia: economy shrinks 0.8% in Q3",
    "Peru: Tumbes River passes red alert",
    "Japan: Takaichi makes first China visit as PM",
    "Bangladesh: police tear-gas garment worker protests",
    "COP31: ministers weigh a divided draft in Antalya",
]
af = font(SANS, 12)
for i, item in enumerate(ALSO):
    col = 0 if i < 17 else 1
    ax = MX + col * 500
    ay = 726 + (i % 17) * 12
    num = "%d." % (17 + i)
    d.text((ax, ay), num, font=font(SANS_B, 12), fill=RED)
    nx = ax + d.textlength(num, font=font(SANS_B, 12)) + 5
    txt = item
    while d.textlength(txt, font=af) > (W - MX - nx) and " " in txt:
        txt = txt.rsplit(" ", 1)[0] + " …"
    d.text((nx, ay), txt, font=af, fill=INK)

# ------------------------------------------------------------ date check
d.rounded_rectangle([MX, 936, W - MX, 984], radius=8,
                    fill=(250, 244, 214), outline=(200, 170, 90), width=1)
d.text((MX + 12, 941), "DATE CHECK", font=font(SANS_B, 11), fill=RED)
dcf = font(SANS, 10)
lab_w = d.textlength("DATE CHECK", font=font(SANS_B, 11))
dc1 = ("LEFT OUT — broke before 18 Nov: Peltola wins Alaska Senate (Tue 17 Nov) · "
       "Nvidia Q3 results (Tue 17 Nov) · Kahana elected speaker (Tue 17 Nov) ·")
dc2 = ("Kerch span falls (Tue 17 Nov) · Board of Peace report (Tue 17 Nov) · "
       "Ebola 11,000 (11–15 Nov) · Huang quits Nvidia (12–13 Nov) · "
       "FAA ground stop (13 Nov) · Hormuz tankers (16 Nov)")
dc3 = ("NOT YET — due after 18 Nov: Xi–Trump–Putin trilateral (Thu 19 Nov) · "
       "Cyclone Akvan landfall (Fri 20 Nov)")
d.text((MX + 12 + lab_w + 8, 941), dc1, font=dcf, fill=INK)
d.text((MX + 12, 953), dc2, font=dcf, fill=INK)
d.text((MX + 12, 965), dc3, font=dcf, fill=INK)

# ---------------------------------------------------------------- footer
foot = ("Every story happened or was first reported on Wed 18 Nov 2026. "
        "CLAIM = one side's account. Sources: AP, Reuters, AFP, Al Jazeera, "
        "NPR, PAHO, UN News, NASA. Original drawings.")
ff = font(SANS, 10)
fw = d.textlength(foot, font=ff)
d.text(((W - fw) / 2, 990), foot, font=ff, fill=GREY)

# ------------------------------------------------------------------ save
img = Image.alpha_composite(img.convert("RGBA"), ov).convert("RGB")
img.save("entry.png", optimize=True)
print("saved entry.png", img.size, img.mode)
