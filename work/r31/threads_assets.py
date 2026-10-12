# -*- coding: utf-8 -*-
"""Reel 31: pre-blurred Threads avatars and handles (PNG), so the posts carry
no CSS filter (the blur budget is tight). Invented people, blurred illegible.

usage: python work/r31/threads_assets.py   (bare python = 3.10 with Pillow)
"""
import os
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "reel-31", "assets", "threads")
os.makedirs(OUT, exist_ok=True)
FONT = ImageFont.truetype(os.path.join(ROOT, "reel-31", "assets", "fonts", "ProductSans-Bold.ttf"), 64)

HANDLES = ["olena.reels", "mariia_smm", "kate.content.ua", "iryna.creates", "anna_ai_tips",
           "sofiia.media", "dasha.mkt", "yulia.brand", "nastya.edits", "vika_marketing"]
# background, skin, hair, top
AV = [((232, 214, 206), (233, 196, 172), (92, 60, 44), (40, 40, 48)),
      ((206, 220, 232), (240, 208, 186), (196, 150, 92), (180, 30, 60)),
      ((224, 224, 214), (214, 172, 140), (40, 30, 28), (236, 236, 236)),
      ((240, 206, 214), (238, 200, 178), (120, 70, 50), (90, 110, 140)),
      ((210, 226, 212), (226, 186, 160), (30, 24, 24), (220, 180, 190)),
      ((236, 226, 200), (242, 212, 190), (150, 96, 60), (60, 60, 70)),
      ((214, 210, 232), (210, 166, 136), (60, 40, 36), (200, 200, 200)),
      ((232, 218, 226), (236, 198, 176), (176, 120, 80), (140, 30, 50)),
      ((220, 230, 236), (230, 190, 166), (50, 36, 30), (240, 220, 200)),
      ((236, 220, 210), (224, 182, 150), (100, 66, 40), (30, 60, 80))]

S = 168  # 2x of the 84px avatar
for i, (bg, skin, hair, top) in enumerate(AV):
    im = Image.new("RGB", (S, S), bg)
    d = ImageDraw.Draw(im)
    d.ellipse((24, 120, 144, 230), fill=top)                 # shoulders
    d.ellipse((48, 30, 120, 112), fill=hair)                 # hair
    d.ellipse((58, 44, 110, 106), fill=skin)                 # face
    d.rectangle((70, 98, 98, 128), fill=skin)                # neck
    im = im.filter(ImageFilter.GaussianBlur(12))
    mask = Image.new("L", (S, S), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, S - 1, S - 1), fill=255)
    out = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    out.paste(im, (0, 0), mask)
    out.save(os.path.join(OUT, "av%d.png" % i))

for i, h in enumerate(HANDLES):
    for suf, col in (("", (0, 0, 0, 255)), ("d", (243, 245, 247, 255))):
        w = int(FONT.getlength(h)) + 48
        im = Image.new("RGBA", (w, 96), (0, 0, 0, 0))
        ImageDraw.Draw(im).text((24, 12), h, font=FONT, fill=col)
        im = im.filter(ImageFilter.GaussianBlur(22))
        im.save(os.path.join(OUT, "h%d%s.png" % (i, suf)))
print("ok", OUT)
