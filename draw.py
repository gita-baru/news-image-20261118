#!/usr/bin/env python3
"""Draw the news image for 18 November 2026 (1024x1024 PNG).

Build tool only: the entry program (main.ts) copies the finished entry.png.
Run: python3 draw.py  ->  writes entry.png beside this file.
Fonts: DejaVu / Liberation (system fonts, present on this machine).
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 231)
INK = (20, 20, 20)
RED = (179, 38, 30)
GREY = (90, 86, 78)

SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def text_w(draw, s, f):
    return draw.textlength(s, font=f)


def wrap(draw, s, f, max_w):
    """Wrap s into lines that fit max_w."""
    words, lines, cur = s.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=f) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, lines, x, y, f, fill, align="left", box_w=None, leading=None):
    """Draw lines; returns y after last line."""
    if leading is None:
        leading = int(f.size * 1.18)
    for ln in lines:
        if align == "center":
            lx = x + (box_w - draw.textlength(ln, font=f)) / 2
        else:
            lx = x
        draw.text((lx, y), ln, font=f, fill=fill)
        y += leading
    return y


def star(draw, cx, cy, r_out, r_in, fill, points=5):
    import math
    pts = []
    for i in range(points * 2):
        r = r_out if i % 2 == 0 else r_in
        a = math.pi * i / points - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    draw.polygon(pts, fill=fill)


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img, "RGBA")

# ---------------- Masthead ----------------
M = 24  # outer margin
title_f = font(SERIF_B, 62)
title = "THE WORLD IN ONE DAY"
tw = d.textlength(title, font=title_f)
d.text(((W - tw) / 2, 26), title, font=title_f, fill=INK)

# red rule under masthead
d.rectangle([M, 104, W - M, 110], fill=RED)
date_f = font(SANS_B, 42)
date = "WEDNESDAY  ·  18 NOVEMBER 2026"
dw = d.textlength(date, font=date_f)
d.text(((W - dw) / 2, 118), date, font=date_f, fill=RED)
# thin black rule
d.rectangle([M, 168, W - M, 171], fill=INK)

# ---------------- Panels 2x2 ----------------
# grid: x 24..1000, two cols of 476 with 24 gutter; rows y 186..514 and 530..858
PX, PY = M, 186
PW, PH = 476, 328
GX, GY = 24, 16

PANELS = [
    dict(
        kicker="THE GULF",
        bg=(22, 68, 92),
        accent=(255, 190, 60),
        headline="U.S. STRIKES IRAN",
        sub="Missile sites hit on Qeshm Island. Iran strikes back in Kuwait and Bahrain.",
        art="gulf",
    ),
    dict(
        kicker="UKRAINE",
        bg=(46, 90, 136),
        accent=(255, 190, 60),
        headline="KERCH BRIDGE HIT",
        sub="Second day of strikes on the Crimea crossing. A road span collapses.",
        art="bridge",
    ),
    dict(
        kicker="CHINA",
        bg=(140, 29, 24),
        accent=(255, 214, 90),
        headline="XI AND PUTIN MEET",
        sub="Shenzhen talks before Thursday's summit with Trump.",
        art="skyline",
    ),
    dict(
        kicker="U.S. POLITICS",
        bg=(31, 58, 95),
        accent=(255, 190, 60),
        headline="PELTOLA WINS",
        sub="Democrat takes Alaska's Senate seat. Democrats lead 56–44.",
        art="alaska",
    ),
]

kick_f = font(SANS_B, 21)
head_f = font(SANS_B, 37)
sub_f = font(SANS, 22)


def rounded_panel(x, y, w, h, bg):
    d.rounded_rectangle([x, y, x + w, y + h], radius=14, fill=bg)


def art_gulf(x, y, w, h, accent):
    # Stylised Gulf: dark water, coastline polygon, Qeshm island dot + burst
    # water
    d.rectangle([x, y, x + w, y + h], fill=(18, 52, 70))
    # land masses (simplified)
    d.polygon([(x, y), (x + w * 0.42, y), (x + w * 0.30, y + h * 0.55),
               (x + w * 0.18, y + h), (x, y + h)], fill=(38, 84, 96))
    d.polygon([(x + w, y + h * 0.35), (x + w, y), (x + w * 0.62, y),
               (x + w * 0.55, y + h * 0.45), (x + w * 0.72, y + h),
               (x + w, y + h)], fill=(38, 84, 96))
    # Qeshm island (small ellipse in the strait) + red burst
    ix, iy = x + w * 0.52, y + h * 0.42
    d.ellipse([ix - 26, iy - 9, ix + 26, iy + 9], fill=(120, 140, 120))
    star(d, ix, iy - 34, 26, 11, (255, 80, 60))
    d.ellipse([ix - 5, iy - 5, ix + 5, iy + 5], fill=(255, 80, 60))
    # missile arc
    d.arc([x + w * 0.10, y + h * 0.10, x + w * 0.95, y + h * 1.05],
          start=200, end=320, fill=accent, width=4)
    d.text((x + 14, y + h - 30), "QESHM ISLAND", font=font(SANS_B, 15), fill=(200, 220, 225))


def art_bridge(x, y, w, h, accent):
    d.rectangle([x, y, x + w, y + h], fill=(30, 62, 96))
    # sky glow
    d.ellipse([x + w * 0.62, y + h * 0.08, x + w * 0.98, y + h * 0.45],
              fill=(70, 110, 150))
    # sea
    d.rectangle([x, y + h * 0.72, x + w, y + h], fill=(20, 44, 70))
    # bridge deck with a broken gap in the middle
    deck_y = y + h * 0.55
    d.rectangle([x + 18, deck_y, x + w * 0.44, deck_y + 10], fill=(225, 225, 225))
    d.rectangle([x + w * 0.56, deck_y, x + w - 18, deck_y + 10], fill=(225, 225, 225))
    # tilted fallen span
    d.polygon([(x + w * 0.45, deck_y + 2), (x + w * 0.55, deck_y + 2),
               (x + w * 0.52, deck_y + 42), (x + w * 0.44, deck_y + 40)],
              fill=(200, 200, 200))
    # towers + arch
    for tx in (x + w * 0.22, x + w * 0.78):
        d.rectangle([tx - 5, deck_y - 62, tx + 5, deck_y], fill=(225, 225, 225))
    d.arc([x + w * 0.22, deck_y - 96, x + w * 0.78, deck_y + 30],
          start=180, end=360, fill=(225, 225, 225), width=5)
    # smoke from the gap
    for i, (sx, sy, sr) in enumerate([(0.50, 0.30, 16), (0.54, 0.22, 20), (0.47, 0.16, 13)]):
        d.ellipse([x + w * sx - sr, y + h * sy - sr, x + w * sx + sr, y + h * sy + sr],
                  fill=(120, 120, 120))
    d.text((x + 14, y + h - 30), "KERCH STRAIT", font=font(SANS_B, 15), fill=(200, 220, 225))


def art_skyline(x, y, w, h, accent):
    d.rectangle([x, y, x + w, y + h], fill=(120, 22, 18))
    # sun disc
    d.ellipse([x + w * 0.68, y + h * 0.06, x + w * 0.94, y + h * 0.32], fill=(255, 190, 60))
    # skyline silhouette
    base = y + h
    heights = [0.42, 0.62, 0.50, 0.78, 0.58, 0.70, 0.46, 0.64]
    bw = w / len(heights)
    for i, hh in enumerate(heights):
        bx = x + i * bw
        d.rectangle([bx + 3, base - h * hh, bx + bw - 3, base], fill=(60, 10, 10))
        # lit windows
        for wy in range(int(base - h * hh) + 10, int(base) - 8, 18):
            for wx in range(int(bx) + 8, int(bx + bw) - 10, 16):
                if (wx + wy) % 3 == 0:
                    d.rectangle([wx, wy, wx + 4, wy + 6], fill=(255, 214, 90))
    # three flag bars: China, Russia, USA
    fy = y + h - 34
    d.rectangle([x + 14, fy, x + 44, fy + 18], fill=(222, 41, 16))       # China
    d.rectangle([x + 50, fy, x + 80, fy + 6], fill=(255, 255, 255))      # Russia
    d.rectangle([x + 50, fy + 6, x + 80, fy + 12], fill=(0, 57, 166))
    d.rectangle([x + 50, fy + 12, x + 80, fy + 18], fill=(213, 0, 50))
    d.rectangle([x + 86, fy, x + 116, fy + 18], fill=(60, 59, 110))      # USA
    for i in range(3):
        d.rectangle([x + 86, fy + i * 6, x + 116, fy + i * 6 + 3], fill=(255, 255, 255))
    d.text((x + 126, fy - 2), "SHENZHEN", font=font(SANS_B, 15), fill=(255, 220, 200))


def art_alaska(x, y, w, h, accent):
    d.rectangle([x, y, x + w, y + h], fill=(24, 44, 76))
    # big North Star + dipper dots
    star(d, x + w * 0.78, y + h * 0.30, 42, 17, (255, 255, 255))
    dipper = [(0.18, 0.22), (0.30, 0.16), (0.42, 0.20), (0.50, 0.30),
              (0.38, 0.38), (0.26, 0.36), (0.16, 0.30)]
    for fx, fy in dipper:
        d.ellipse([x + w * fx - 6, y + h * fy - 6, x + w * fx + 6, y + h * fy + 6],
                  fill=(255, 255, 255))
    # ballot box
    bx, by = x + w * 0.60, y + h * 0.62
    d.rectangle([bx, by, bx + 110, by + 78], fill=(255, 255, 255))
    d.rectangle([bx - 8, by - 12, bx + 118, by + 2], fill=(230, 230, 230))
    d.rectangle([bx + 38, by - 8, bx + 72, by - 2], fill=(20, 20, 20))
    d.text((x + 14, y + h - 30), "56 – 44", font=font(SANS_B, 26), fill=accent)


ART = {"gulf": art_gulf, "bridge": art_bridge, "skyline": art_skyline, "alaska": art_alaska}

for i, p in enumerate(PANELS):
    col, row = i % 2, i // 2
    x = PX + col * (PW + GX)
    y = PY + row * (PH + GY)
    rounded_panel(x, y, PW, PH, p["bg"])
    # art zone: top ~150px of the panel
    ART[p["art"]](x, y, PW, 150, p["accent"])
    # kicker
    d.text((x + 18, y + 162), p["kicker"], font=kick_f, fill=p["accent"])
    # headline (wrap, max 2 lines)
    lines = wrap(d, p["headline"], head_f, PW - 36)
    yy = draw_wrapped(d, lines, x + 18, y + 190, head_f, (255, 255, 255))
    # sub
    sub_lines = wrap(d, p["sub"], sub_f, PW - 36)
    draw_wrapped(d, sub_lines, x + 18, yy + 6, sub_f, (235, 235, 235))

# ---------------- Bottom strip ----------------
SY = 874
d.rectangle([M, SY - 14, W - M, SY - 11], fill=INK)
STRIP = [
    ("EBOLA IN CONGO", "11,000+ cases,\n5,400+ dead"),
    ("MEASLES IN THE U.S.", "Free status lost\nafter 26 years"),
    ("VOYAGER 1", "One light-day\nfrom Earth"),
    ("CYCLONE XAVIER", "Category 5 hits the\nNorthern Cook Islands"),
]
strip_f = font(SANS_B, 20)
fact_f = font(SANS, 20)
col_w = (W - 2 * M) / 4
for i, (label, fact) in enumerate(STRIP):
    cx = M + i * col_w
    d.text((cx + 4, SY + 2), label, font=strip_f, fill=RED)
    yy = SY + 30
    for ln in fact.split("\n"):
        d.text((cx + 4, yy), ln, font=fact_f, fill=INK)
        yy += 25
    if i < 3:
        d.line([cx + col_w - 8, SY + 2, cx + col_w - 8, SY + 78], fill=(180, 175, 165), width=2)

# footer
foot_f = font(SANS, 17)
foot = "Also: Russian military plane crashes in Siberia — 19 killed  ·  Summarising the world's news of 18 November 2026"
fw = d.textlength(foot, font=foot_f)
d.text(((W - fw) / 2, 972), foot, font=foot_f, fill=GREY)

img.save("entry.png", optimize=True)
print("saved entry.png")
