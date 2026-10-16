#!/usr/bin/env python3
"""Build Kinney Cleaning Services flyer PNG (1080x1350)."""
from PIL import Image, ImageDraw, ImageFont

S = 2
W, H = 1080 * S, 1350 * S
NAVY = (10, 42, 107)
BLUE = (22, 99, 217)
LIGHT_BLUE = (234, 242, 255)
WHITE = (255, 255, 255)
GRAY = (51, 65, 92)
PALE = (159, 192, 245)

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FSI = "/usr/share/fonts/truetype/noto/NotoSerif-Italic.ttf"

def font(path, size):
    return ImageFont.truetype(path, size * S)

def centered(draw, cx, y, s, fnt, fill):
    bb = draw.textbbox((0, 0), s, font=fnt)
    w = bb[2] - bb[0]
    draw.text((cx - w / 2 - bb[0], y), s, font=fnt, fill=fill)
    return bb[3] - bb[1]

def wrap(draw, s, fnt, max_w):
    words, lines, cur = s.split(), [], ""
    for wd in words:
        t = (cur + " " + wd).strip()
        if draw.textbbox((0, 0), t, font=fnt)[2] <= max_w:
            cur = t
        else:
            lines.append(cur); cur = wd
    lines.append(cur)
    return lines

img = Image.new("RGB", (W, H), WHITE)
d = ImageDraw.Draw(img)
cx = W / 2
y = 15 * S

# --- House logo ---
house = Image.open("media-generation-kinney-house-logo-0-a68f64b2-670e-42a2-91fe-271bb12c93b2.webp").convert("RGB")
hw = 520 * S
hh = int(hw * house.size[1] / house.size[0])
house = house.resize((hw, hh), Image.LANCZOS)
img.paste(house, (int(cx - hw / 2), int(y)))
y += hh + 4 * S
print("after logo y:", y // S)

# --- Business name, one line ---
f_big = font(FB, 50)
lh = centered(d, cx, y, "KINNEY CLEANING SERVICES", f_big, NAVY)
y += lh + 8 * S
print("after name y:", y // S)

# --- Tagline ---
f_tag = font(FSI, 32)
lh = centered(d, cx, y, "Veteran Owned. Mobile Proud.", f_tag, BLUE)
y += lh + 10 * S
print("after tagline y:", y // S)

# --- Hero photo band ---
hero = Image.open("media-generation-kinney-pressure-wash-hero-0-3acbadd3-6088-4edb-a91c-d9d122f2e442.webp").convert("RGB")
hero = hero.resize((W, int(W * hero.size[1] / hero.size[0])), Image.LANCZOS)
band_h = 150 * S
top = (hero.size[1] - band_h) // 2
band = hero.crop((0, top, W, top + band_h)).convert("RGBA")
ov = Image.new("RGBA", (W, 80 * S), (0, 0, 0, 0))
od = ImageDraw.Draw(ov)
for r_ in range(80 * S):
    a = int(200 * (r_ / (80 * S)) ** 1.4)
    od.line([(0, r_), (W, r_)], fill=(10, 20, 60, a))
band.paste(ov, (0, band_h - 80 * S), ov)
img.paste(band.convert("RGB"), (0, int(y)))
bd = ImageDraw.Draw(img)
bd.text((40 * S, y + band_h - 62 * S), "We Bring the Clean Back.", font=font(FB, 34), fill=WHITE)
y += band_h + 14 * S
print("after hero y:", y // S)

# --- Services grid ---
services = [
    ("house", "HOUSE SOFT WASH", "Gentle wash for siding, trim and porches. Safe for your home."),
    ("spray", "DRIVEWAY & CONCRETE", "Driveways, sidewalks and patios restored like new."),
    ("roof", "ROOF SOFT WASH", "Kills algae and black streaks with no shingle damage."),
    ("gutter", "GUTTER CLEANING", "Debris removal plus downspout flush. Water flows free."),
    ("window", "WINDOW CLEANING", "Inside and out, streak free shine. Screens wiped."),
    ("tile", "TILE & GROUT", "Deep steam clean lifts years of grime from grout lines."),
]

def glyph(kind, cxx, cyy, r_):
    w_ = 4 * S
    if kind == "house":
        d.line([(cxx - r_, cyy + r_ * .35), (cxx, cyy - r_ * .55), (cxx + r_, cyy + r_ * .35)], fill=WHITE, width=w_, joint="curve")
        d.rectangle([cxx - r_ * .62, cyy - r_ * .05, cxx + r_ * .62, cyy + r_ * .55], outline=WHITE, width=w_)
    elif kind == "spray":
        d.line([(cxx - r_ * .5, cyy + r_ * .55), (cxx + r_ * .1, cyy - r_ * .1)], fill=WHITE, width=w_)
        import math
        for a_ in (-0.5, 0, 0.5):
            ex = cxx + r_ * .1 + math.cos(-0.9 + a_) * r_ * .8
            ey = cyy - r_ * .1 + math.sin(-0.9 + a_) * r_ * .8
            d.line([(cxx + r_ * .1, cyy - r_ * .1), (ex, ey)], fill=WHITE, width=int(w_ * .8))
    elif kind == "roof":
        d.polygon([(cxx - r_, cyy + r_ * .4), (cxx, cyy - r_ * .55), (cxx + r_, cyy + r_ * .4)], outline=WHITE, width=w_)
        d.line([(cxx - r_ * .55, cyy + r_ * .4), (cxx + r_ * .55, cyy + r_ * .4)], fill=WHITE, width=w_)
    elif kind == "gutter":
        d.rounded_rectangle([cxx - r_, cyy - r_ * .35, cxx + r_, cyy + r_ * .05], radius=6 * S, outline=WHITE, width=w_)
        d.ellipse([cxx - 5 * S, cyy + r_ * .25, cxx + 5 * S, cyy + r_ * .55], fill=WHITE)
    elif kind == "window":
        d.rectangle([cxx - r_ * .6, cyy - r_ * .7, cxx + r_ * .6, cyy + r_ * .7], outline=WHITE, width=w_)
        d.line([(cxx, cyy - r_ * .7), (cxx, cyy + r_ * .7)], fill=WHITE, width=w_)
        d.line([(cxx - r_ * .6, cyy), (cxx + r_ * .6, cyy)], fill=WHITE, width=w_)
    elif kind == "tile":
        d.rectangle([cxx - r_ * .65, cyy - r_ * .65, cxx + r_ * .65, cyy + r_ * .65], outline=WHITE, width=w_)
        for f_ in (-0.22, 0.22):
            d.line([(cxx + f_ * r_, cyy - r_ * .65), (cxx + f_ * r_, cyy + r_ * .65)], fill=WHITE, width=int(w_ * .7))
            d.line([(cxx - r_ * .65, cyy + f_ * r_), (cxx + r_ * .65, cyy + f_ * r_)], fill=WHITE, width=int(w_ * .7))

f_svc_t = font(FB, 18)
f_svc_d = font(FR, 14)
ROW_H = 168 * S
col_w = W / 3
for idx, (kind, title, desc) in enumerate(services):
    col, row = idx % 3, idx // 3
    ccx = col_w * (col + 0.5)
    cy0 = y + row * ROW_H
    cr = 36 * S
    d.ellipse([ccx - cr, cy0, ccx + cr, cy0 + 2 * cr], fill=NAVY)
    glyph(kind, ccx, cy0 + cr, 26 * S)
    ty = cy0 + 2 * cr + 6 * S
    th = centered(d, ccx, ty, title, f_svc_t, NAVY)
    dy = ty + th + 4 * S
    for ln in wrap(d, desc, f_svc_d, 290 * S):
        dh = centered(d, ccx, dy, ln, f_svc_d, GRAY)
        dy += dh + 2 * S
y += 2 * ROW_H + 10 * S
print("after services y:", y // S)

# --- Trust box ---
box_h = 128 * S
d.rounded_rectangle([40 * S, y, W - 40 * S, y + box_h], radius=16 * S, fill=LIGHT_BLUE)
checks = [("VETERAN OWNED & OPERATED", "5.0 STAR GOOGLE RATING"),
          ("RELIABLE & ON TIME", "RESIDENTIAL & COMMERCIAL")]
f_chk = font(FB, 17)
for r_, (a_, b_) in enumerate(checks):
    yy = y + 18 * S + r_ * 36 * S
    for c_, txt in enumerate((a_, b_)):
        xx = 80 * S + c_ * 470 * S
        d.ellipse([xx, yy, xx + 28 * S, yy + 28 * S], fill=NAVY)
        d.line([(xx + 6 * S, yy + 14 * S), (xx + 12 * S, yy + 20 * S)], fill=WHITE, width=4 * S, joint="curve")
        d.line([(xx + 12 * S, yy + 20 * S), (xx + 22 * S, yy + 8 * S)], fill=WHITE, width=4 * S, joint="curve")
        d.text((xx + 36 * S, yy + 1 * S), txt, font=f_chk, fill=NAVY)
centered(d, cx, y + 92 * S, "No job too big or too small!", font(FSI, 30), NAVY)
y += box_h + 10 * S
print("after trust y:", y // S)

# --- Contact band ---
d.rectangle([0, y, W, y + 190 * S], fill=NAVY)
yy = y
centered(d, cx, yy + 12 * S, "O W N E D   &   O P E R A T E D   B Y", font(FB, 15), PALE)
centered(d, cx, yy + 40 * S, "Chad Kinney", font(FSI, 40), WHITE)
centered(d, cx, yy + 100 * S, "(251) 767-0754", font(FB, 48), WHITE)
centered(d, cx, yy + 160 * S, "kinneycleaningservices.com", font(FB, 22), PALE)
y += 190 * S
print("after contact y:", y // S)

# --- Footer ---
d.rectangle([0, y, W, H], fill=(8, 34, 88))
centered(d, cx, y + 6 * S, "Veteran Owned. Local. Trusted.", font(FSI, 22), (207, 225, 255))
centered(d, cx, y + 38 * S, "Mobile, AL  |  Serving Mobile County and the Eastern Shore  |  Since 2019", font(FR, 13), PALE)

img = img.resize((1080, 1350), Image.LANCZOS)
img.save("kinney-cleaning-flyer.png")
print("saved", img.size)
