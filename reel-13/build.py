# -*- coding: utf-8 -*-
"""Reel 13 — «Ти пробувала робити каруселі через ШІ». Posts 2026-09-29.

Variant B, refined glass (STYLE.md §0). One continuous shot, no inserts, no
pull-outs (tools/shots.py, tools/pullouts.py) — nothing on the timeline is hers
alone, so NO_PAINT is empty and her line «і слава богу, що є я» is simply left
clear.

The one object is **a single carousel slide**. It starts as AI slop (built by
`slop.py`, the one sanctioned off-palette frame, reused by reels 17 and 19)
and ends as a template-clean slide, which the three fixes turn into a system.

The chain, near -> behind -> over -> near -> over -> behind -> near:
    a slop slide on the glass shelf, the AI tile that made it, a timer chip
    that rolls 15 хв -> 2 дні while stickers pile on -> Canva pops a clean
    slide out in one go -> the AI tile becomes a row in an effort meter, ТИ
    overflows the shelf -> the shelf's frost spreads into the room and a wall
    of her real carousels ripples out behind her, pulled into Instagram ->
    «По-перше»: iris onto burgundy out of a «1», the AI tile splits into the
    two kinds, a picture model (noise resolving into the slop, .png) and a
    builder (wireframe snapping into her clean slide, .html) -> the builder
    gets the tick, and the iris closes onto the slop as it rises over her
    head -> it sprouts stickers -> flips to the clean slide, and a sticker
    bounces off it -> «Друге»: the clean slide opens into the takeover, style
    swatches, then the layout guides, ТЕКСТ, ФОТО, smart guides -> the photo
    goes, the zones stay: a template, locked -> iris closes onto it -> five
    slides from one template fan out behind her -> collapse back into it, the
    template sits on the shelf and the AI fills it -> «І звичайно»: a «3», the
    headline typed by hand, the AI trained, the body written in one go ->
    next reel: the same timer chip, 2 дні -> 15 хв; Стежити -> Відстежується.

usage: python build.py
"""
import io
import json
import math
import os
import random
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))
sys.path.insert(0, HERE)
from kit import Kit  # noqa: E402
from glass import Glass  # noqa: E402
from slop import Slop  # noqa: E402

DUR = 75.517           # 2266 plate frames / 30 (work/w40-queue.log)
FPS = 30
k = Kit(width=1080, height=1920, fps=FPS, duration=DUR)
g = Glass()
k.css(g.css())
slop = Slop()
k.css(slop.css())

BEATS = []


def beat(fn):
    BEATS.append(fn)
    return fn


# ---------------------------------------------------------------------------
# NO-PAINT ZONES — her own editing (STYLE.md §4a). One continuous shot,
# 0-75.56: no cuts, no closeups, no pull-outs. Nothing is hers alone.
NO_PAINT = []

# ---------------------------------------------------------------------------
# Words. Script spelling on her timing (work/r13/captions.json, settled with
# work/r13/caption-patch.json). Ends re-derived from the next start, the rule
# align.py uses, because the patch merged «По-перше» and «по-іншому».
CAPS = k.load_captions(os.path.join(ROOT, "work", "r13", "captions.json"))
for _a, _b in zip(CAPS, CAPS[1:]):
    _a["e"] = round(max(_a["s"] + 0.10, _b["s"] - 0.085), 3)

# Every moment a beat hangs on, as the word's start. Asserted against the
# captions below, so a re-run of align cannot silently shift a beat.
T = {
    "ty": 0.00, "karuseli": 1.16, "shtuchnyi": 1.86, "dumala": 2.62,
    "shvydenko": 3.38, "a1": 4.00, "sydysh": 4.16, "nad": 4.44, "vzhe": 4.84,
    "druhyi": 5.06, "den": 5.36, "realno": 5.80, "shvydshe": 6.22,
    "zrobyty": 6.74, "kanvi": 7.26,
    "taka": 7.88, "avtomat": 8.46, "navpaky": 9.22, "vykon": 9.84,
    "roboty": 10.50, "bilshe": 10.90, "nizh": 11.40, "intelekt": 11.86,
    "tak": 12.30, "tebe": 13.44, "namakhaly": 13.78, "prosto": 14.40,
    "vsi": 14.74, "pokaz": 15.22, "kar2": 15.74, "insta": 16.36,
    "vony": 16.94, "descho": 17.50, "choho": 17.96, "znayesh": 18.28,
    "popershe": 22.42, "obraty": 23.34, "pravyl": 23.94, "shi3": 24.58,
    "ye": 25.42, "dva": 25.74, "typy": 26.00, "odyn": 26.64, "maliuye": 26.92,
    "kart1": 27.22, "nulia": 27.88, "a2": 28.42, "inshyi": 28.64,
    "zbyraye": 28.90, "yak": 29.70, "saity": 30.12,
    "nam": 31.18, "potriben": 31.46, "same": 31.94, "druhyi2": 32.42,
    "tomu": 32.82, "pershyi": 33.24, "nalipyt": 33.68, "kupu": 34.16,
    "element": 34.50, "yaki": 35.00, "ne1": 35.28, "potribni": 35.56,
    "a3": 36.12, "druhyi3": 36.32, "minimal": 36.76, "prosto2": 37.66,
    "fizychno": 38.48, "ne2": 39.14, "mozhe": 39.40, "zrob2": 39.60,
    "druhe": 40.72, "yoho": 41.32, "navchyty": 41.82, "neprosto": 42.24,
    "styliu": 43.02, "a4": 43.44, "rozmisch": 44.64, "inform": 45.16,
    "skilky": 46.20, "tekstu": 46.60, "yaki2": 47.18, "kart2": 47.40,
    "de": 48.10, "stoyit": 48.52, "pofaktu": 49.24, "zrob3": 49.56,
    "shablon": 50.36, "toho": 50.86, "vyhl": 51.64,
    "itilky": 52.30, "pislia": 52.96, "pochnesh": 54.24, "robyty": 54.60,
    "kar3": 54.96, "shvydko": 55.42,
    "tomu2": 56.18, "systema": 57.68, "rozstav": 58.90, "tvoyi": 59.76,
    "teksty": 60.06, "kart3": 60.50, "elementy": 61.18,
    "i5": 61.98, "treba": 62.76, "napys": 63.72, "tekst": 64.36,
    "kar4": 64.68, "a5": 65.36, "navch2": 65.92, "toyzhe": 66.56,
    "samyi": 66.82, "tse": 67.66, "robyty2": 67.82,
    "i6": 68.46, "pokazhu": 69.48, "povna": 70.60, "shvydkoho": 71.32,
    "karuselei": 72.30, "p15": 73.08, "khvylyn": 73.42, "tomu3": 74.08,
    "obov": 74.32, "pidpysh": 75.00,
    "dur": DUR,
}
_starts = [c["s"] for c in CAPS]
for _k, _v in T.items():
    if _k != "dur":
        assert min(abs(_v - s) for s in _starts) < 0.021, (_k, _v)


def js(src):
    """`@name`, `@name+0.12`, `@name-0.1` -> one literal time. Literals, not
    variables, because tools/review.py reads the timeline off the numbers."""
    def rep(m):
        v = T[m.group(1)] + (float(m.group(2)) if m.group(2) else 0.0)
        return "%.3f" % v
    return re.sub(r"@(\w+)([+-]\d+(?:\.\d+)?)?", rep, src)


# ---------------------------------------------------------------------------
# Mattes (tools/matte.py, work/r13/mattes.sh). (first frame, count).
MATTES = {"wall": (372, 187), "fan": (1623, 79)}
for _n, (_f0, _c) in MATTES.items():
    k.matte(_n, _f0 / 30.0, _c / 30.0)

# ---------------------------------------------------------------------------
# Glyphs — monochrome, drawn, never emoji (§5a.11). Strokes use .sk.
SPARK = ("M12 1.6c.8 4.7 2.3 7.5 4.4 8.9 1.5 1 3.6 1.5 6.1 1.5-2.5.1-4.6.6-6.1 1.6-2.1 "
         "1.4-3.6 4.2-4.4 8.8-.8-4.6-2.3-7.4-4.4-8.8C6.1 12.6 4 12.1 1.5 12c2.5-.1 4.6-.6 "
         "6.1-1.5C9.7 9.1 11.2 6.3 12 1.6z")
EXTRA_DEFS = (
    '<symbol id="i-spark" viewBox="0 0 24 24"><path d="%s"/></symbol>'
    '<symbol id="i-person" viewBox="0 0 24 24"><circle cx="12" cy="8.4" r="4.4"/>'
    '<path d="M3.8 21.2c1.1-4.7 4.4-7 8.2-7s7.1 2.3 8.2 7z"/></symbol>'
    '<symbol id="i-play" viewBox="0 0 24 24"><path d="M8 5.2v13.6l10.8-6.8z"/></symbol>'
    '<linearGradient id="gJ" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#8d0d24"/>'
    '<stop offset="0.6" stop-color="#e0204b"/><stop offset="1" stop-color="#ff6e9c"/></linearGradient>'
    % SPARK)
STROKES = {
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5.3l3.5 2.1"/>',
    "image": ('<rect x="3" y="4.5" width="18" height="15" rx="3.2"/>'
              '<path d="M3.6 17.2l5.1-5.3 4 4 2.6-2.6 5.1 4.5"/><circle cx="15.8" cy="9.3" r="1.6"/>'),
    "code": '<path d="M8.4 7.4L3.8 12l4.6 4.6M15.6 7.4l4.6 4.6-4.6 4.6M13.3 5.2l-2.6 13.6"/>',
    "check": '<path d="M5.4 12.6l4.3 4.3 8.9-9.5"/>',
    "lock": '<rect x="5" y="10.6" width="14" height="10" rx="2.6"/><path d="M8.2 10.6V7.9a3.8 3.8 0 0 1 7.6 0v2.7"/>',
}


def glyph(name, cls="mk"):
    return '<svg class="%s"><use href="#i-%s" width="100%%" height="100%%"/></svg>' % (cls, name)


def stroke(name, cls="sk"):
    return '<svg class="%s" viewBox="0 0 24 24">%s</svg>' % (cls, STROKES[name])


def tile(tid, size, x, y, material, inner, extra_cls="", ring=True):
    """A tile in the glass family: the wrapper takes the motion, the tile the
    material. x, y are its top-left. A ripple ring of the same shape rides
    with it when asked."""
    r = ('<div class="sqring" id="%sR" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx"></div>'
         % (tid, x, y, size, size)) if ring else ""
    return ('%s<div class="tw %s" id="%s" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx">'
            '<div class="%s">%s<div class="sheen"></div></div></div>'
            % (r, extra_cls, tid, x, y, size, size, material, inner))


def roll_chip(cid, x, y, w, h, vals, font, last_red=True):
    """The timer chip: a pearl pill with a clock and a window whose values roll
    upward like an odometer. Values are stacked; the roll is a y translate."""
    cells = "".join('<i%s>%s</i>' % (' class="red"' if (last_red and i == len(vals) - 1) else "", v)
                    for i, v in enumerate(vals))
    return ('<div class="tchip hide" id="%s" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx">'
            '<div class="tci" style="width:%dpx;height:%dpx">%s</div>'
            '<div class="roll" data-layout-ignore style="left:%dpx;height:%dpx;width:%dpx">'
            '<div class="rin" id="%sIn" style="font-size:%dpx">%s</div></div>'
            '<div class="sheen"></div></div>'
            % (cid, x, y, w, h, h * 0.52, h * 0.52, stroke("clock", "sk ink"),
               round(h * 0.95), h, w - round(h * 1.1), cid, font, cells.replace(
                   "<i", '<i style="height:%dpx;line-height:%dpx"' % (h, h))))


k.css("""
.abs, .cx { position: absolute; }
.hide { opacity: 0; visibility: hidden; }
.tw { position: absolute; }
.sk { fill: none; stroke: url(#gw); stroke-width: 2.3; stroke-linecap: round; stroke-linejoin: round;
  width: 50%; height: 50%; position: relative; z-index: 1; overflow: visible; }
.sk.ink { stroke: #b4122f; width: 100%; height: 100%; }
.pearl .sk { stroke: #17141c; }
.circ .jelly, .circ .pearl, .circ .clear { border-radius: 50%; }
.circ .sheen { border-radius: 50%; }
.nbt { position: relative; z-index: 1; color: #fff; font-weight: 900; letter-spacing: -0.04em; line-height: 1; }
.sqring.circ { border-radius: 50%; }

/* ---- the timer chip (b01 -> b18): a pearl pill whose value rolls ---- */
.tchip { position: absolute; border-radius: 999px; overflow: hidden;
  background: linear-gradient(160deg, #ffffff 0%, #fff5f8 52%, #f5dfe6 100%);
  box-shadow: inset 0 2px 1px #fff, inset 0 -14px 24px -12px rgba(180,18,47,0.18),
              0 30px 56px -22px rgba(30,4,12,0.6), 0 3px 8px rgba(30,4,12,0.12); }
.tchip .tci { position: absolute; left: 22px; top: 50%; transform: translateY(-50%); }
.tchip .roll { position: absolute; top: 0; overflow: hidden; }
.tchip .rin i { display: block; font-style: normal; font-weight: 700; color: #17141c;
  letter-spacing: -0.02em; white-space: nowrap; }
.tchip .rin i.red { color: #b4122f; }
.tchip .sheen { mix-blend-mode: normal; opacity: 0.6; }

/* ---- a slide card: a real carousel slide, small and moving ---- */
.slc { position: absolute; object-fit: cover; border-radius: 12px;
  box-shadow: 0 0 0 2px rgba(255,255,255,0.55), 0 26px 44px -18px rgba(20,2,8,0.65); }
""")


# ================================================================== layers ==
# Bottom to top: BEHIND (in her room, under her mattes) -> NEAR (shelves and
# cards above her head) -> TK (the burgundy takeover) -> TOP (the one slide,
# which crosses the takeover boundary in both directions). All of it is gfx,
# so all of it sits under her mattes — which only exist while something big
# is behind her.
L = {"behind": [], "near": [], "tk": [], "top": []}


# ============================================================ the one slide ==
# #fc: front face is the slop, back face is her clean slide (blond-webinar 04)
# with the template underneath it. It lives in TOP for 26.6-62 s and travels:
# TK1's left sheet -> over her head (stickers) -> flips -> opens TK2 at 2x ->
# shrinks to a template tile -> deals the fan -> the shelf, filled by the AI.
FC_W, FC_H, FC_C = 300, 400, (540, 290)        # near geometry, centre
# TK1 left-sheet slot: sheet (70,540) + 30 inset, 380 wide
FC_TK1 = dict(x=290 - 540, y=(540 + 30 + 253.33) - 290, scale=380.0 / 300)
FC_TK2 = dict(x=0, y=620 - 290, scale=2.0)
FC_SHELF = dict(x=700 - 540, y=310 - 290, scale=1.0)

SLOP_B_EXTRA = [   # native 1080-wide coords; spill well past the card edges
    ("rocket", -330, 380, 420, -22), ("bubble", 1350, 280, 460, 9),
    ("crown", 520, -120, 380, -8), ("flame", -300, 1180, 400, 12),
    ("tag", 1400, 1080, 380, 18), ("star", -520, 700, 360, -14),
    ("sparkw", 1620, 700, 240, 0), ("orb", 1200, 1560, 330, 0),
    ("arrow", 180, 1640, 420, -8), ("burst", -600, 120, 300, -18),
    ("heart", 1700, 80, 260, 16), ("spark", -700, 1400, 260, 0),
]

ZONES = [   # back-face coords (300x400), read off blond-webinar 04
    ("z1", 22, 30, 196, 44, u"ТЕКСТ"),
    ("z2", 22, 80, 262, 168, u"ЗАГОЛОВОК"),
    ("z3", 22, 258, 164, 44, u"ТЕКСТ"),
    ("z4", 196, 258, 84, 104, u"ФОТО"),
]
PIECES = [  # (id, x, y, w, h, kind) — what the AI places into the template
    ("pa", 30, 40, 150, 9, "w"), ("pb", 30, 56, 104, 9, "w"),
    ("pc", 30, 92, 226, 34, "p"), ("pd", 30, 134, 150, 34, "p"),
    ("pe", 30, 184, 214, 16, "w"), ("pf", 110, 208, 160, 16, "w"),
    ("pg", 30, 270, 138, 8, "g"), ("ph", 30, 285, 92, 8, "g"),
    ("pi", 200, 262, 76, 96, "img"),
    ("pj", 22, 380, 52, 7, "p"), ("pk", 250, 380, 28, 7, "g"),
]

k.css("""
#fc { left: 390px; top: 90px; width: 300px; height: 400px; perspective: 1400px; }
#fcIn { position: absolute; inset: 0; transform-style: preserve-3d; }
#fc .face { position: absolute; inset: 0; backface-visibility: hidden; -webkit-backface-visibility: hidden; }
#fc .face.back { transform: rotateY(180deg); }
#fcNz { position: absolute; inset: 0; border-radius: 11px; background: url("assets/noise.png") 0 0 / 100% 100%;
  image-rendering: pixelated; }
#fcB { position: absolute; inset: 0; border-radius: 11px;
  box-shadow: 0 0 0 1.5px rgba(255,255,255,0.40), 0 40px 80px -30px rgba(20,2,8,0.7); }
#fcB .tplg { position: absolute; inset: 0; border-radius: 11px; overflow: hidden;
  background: linear-gradient(170deg, #1a1519 0%, #0d0b0e 100%); }
#fcImg { position: absolute; left: 0; top: 0; width: 300px; height: 400px; border-radius: 11px; }
#fcB .sheen { border-radius: 11px; mix-blend-mode: normal; opacity: 0.45; inset: 0; }
#fcSh { position: absolute; inset: 0; border-radius: 11px; overflow: hidden; }
#fcRim { position: absolute; inset: -3px; border-radius: 14px; box-shadow: 0 0 0 4px #ff6e9c, 0 0 30px 6px rgba(255,110,156,0.7); }
.zn { position: absolute; border: 2.5px dashed #ff6e9c; border-radius: 5px; background: rgba(255,110,156,0.10); }
.zl { position: absolute; left: -2.5px; top: -19px; height: 16px; padding: 0 6px; border-radius: 4px;
  background: #d81b4a; color: #fff; font-size: 10.5px; font-weight: 700; letter-spacing: 0.08em; line-height: 16px;
  white-space: nowrap; }
#z4 .sk { position: absolute; left: 50%; top: 50%; width: 34px; height: 34px; margin: -17px 0 0 -17px;
  stroke: #ff6e9c; stroke-width: 1.8; }
.gd { position: absolute; background: #ff6e9c; }
.pc { position: absolute; border-radius: 3px; }
.pc.w { background: rgba(255,255,255,0.92); }
.pc.p { background: linear-gradient(90deg, #ff6e9c, #ff8ab0); border-radius: 6px; }
.pc.g { background: rgba(255,255,255,0.45); }
.pc.img { object-fit: cover; border-radius: 4px; }
#fcLock { position: absolute; left: 258px; top: -14px; width: 34px; height: 34px; }
#fcLock .sk { width: 56%; height: 56%; }
""")


def flip_card():
    zones = "".join(
        '<div class="zn hide" id="%s" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx">'
        '<div class="zl" id="%sL">%s</div>%s</div>'
        % (z, x, y, w, h, z, lab, stroke("image") if z == "z4" else "")
        for z, x, y, w, h, lab in ZONES)
    guides = ('<i class="gd hide" id="gd1" style="left:22px;top:-30px;width:2px;height:460px"></i>'
              '<i class="gd hide" id="gd2" style="left:-30px;top:258px;width:360px;height:2px"></i>'
              '<i class="gd hide" id="gd3" style="left:284px;top:-30px;width:2px;height:460px"></i>')
    pieces = "".join(
        ('<img class="pc img hide" id="%s" src="assets/carousels/tr01-s.jpg" '
         'style="left:%dpx;top:%dpx;width:%dpx;height:%dpx" alt="">' % (i, x, y, w, h))
        if kind == "img" else
        ('<i class="pc %s hide" id="%s" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx"></i>'
         % (kind, i, x, y, w, h))
        for i, x, y, w, h, kind in PIECES)
    front = slop.slide("slB", FC_W, extra=SLOP_B_EXTRA) + '<div id="fcNz" class="hide"></div>'
    back = ('<div id="fcB"><div class="tplg"></div>'
            '<img id="fcImg" src="assets/carousels/wb04-m.jpg" alt="">%s%s%s'
            '<div class="tw circ hide" id="fcLock"><div class="pearl">%s</div></div>'
            '<div id="fcSh"><div class="sheen" id="fcShn"></div></div></div>'
            % (zones, guides, pieces, stroke("lock")))
    return ('<div class="g full" id="gC">'
            '<div class="abs hide" id="fc"><div id="fcIn">'
            '<div class="face front">%s</div><div class="face back">%s</div></div>'
            '<div id="fcRim" class="hide"></div></div>'
            '<div class="tw hide" id="bn" style="left:%dpx;top:%dpx;width:96px;height:96px">'
            '<div class="slop" data-layout-ignore style="width:96px;height:96px">%s</div></div>'
            '</div>' % (front, back, 1150, 150, Slop.sticker("star", 0, 0, 96, 0)))


L["top"].append(flip_card())


# ================================================================ A · hook ==
k.css("""
/* ---- the shelf (b01-b04, again b16-b17) ---- */
#shelf { left: 70px; top: 100px; width: 940px; height: 420px; }
#stk { position: absolute; left: 130px; top: 177px; width: 200px; height: 267px; }
.sback { position: absolute; inset: 0; border-radius: 12px;
  background: linear-gradient(160deg, #ff2bd6 0%, #8a2bff 38%, #2bb8ff 66%, #fff22b 100%);
  box-shadow: inset 0 0 0 3px rgba(255,255,255,0.5), 0 18px 34px -14px rgba(20,2,8,0.6); }
#sb1 { transform: rotate(-9deg) translate(-18px, 8px); opacity: 0.85; }
#sb2 { transform: rotate(7deg) translate(16px, 2px); opacity: 0.92; }
#cvS { left: 610px; top: 185px; width: 200px; height: 250px; }

/* ---- b04 · the effort meter ---- */
.erow { position: absolute; left: 110px; width: 860px; height: 100px; }
.erow .lab { position: absolute; left: 124px; top: 22px; font-size: 52px; font-weight: 900; color: #fff;
  letter-spacing: -0.02em; line-height: 56px; text-shadow: 0 2px 14px rgba(20,2,8,0.35); }
.erow .trk { position: absolute; left: 230px; top: 33px; width: 600px; height: 34px; border-radius: 17px;
  background: rgba(255,255,255,0.20); box-shadow: inset 0 2px 6px rgba(20,2,8,0.18), inset 0 0 0 1px rgba(255,255,255,0.25); }
.erow .fil { position: absolute; left: 0; top: 0; width: 600px; height: 34px; border-radius: 17px;
  transform-origin: 0 50%; box-shadow: inset 0 2px 1px rgba(255,255,255,0.7); }
#rtFill { background: linear-gradient(90deg, #ffffff 0%, #ffd3e0 100%); }
#raFill { background: linear-gradient(90deg, #8d0d24 0%, #e0204b 60%, #ff6e9c 100%); }
#rtHot { position: absolute; inset: 0; border-radius: 17px; background: linear-gradient(90deg, #ff6e9c, #e0204b); }
""")


def shelf_html():
    stack = ('<div id="stk" class="hide"><div class="sback" id="sb1"></div><div class="sback" id="sb2"></div>%s</div>'
             % slop.slide("slA", 200, extra=[("crown", 300, -40, 330, -12),
                                             ("rocket", 930, 1150, 380, 18),
                                             ("bubble", 860, 560, 420, 8)]))
    return u'''
      <div class="g full" id="gS">
        <div id="shelf" class="shelf edge hide"></div>
        %(stack)s
        %(ai)s
        %(chip)s
        %(canva)s
        <img class="slc hide" id="cvS" src="assets/carousels/kg04-s.jpg" alt="">
        <div class="erow" id="rowT" style="top:170px">
          %(ptile)s
          <div class="lab hide" id="rtLab">ТИ</div>
          <div class="trk hide" id="rtTrk"><div class="fil" id="rtFill"><div id="rtHot" class="hide"></div></div></div>
        </div>
        <div class="erow" id="rowA" style="top:330px">
          <div class="lab hide" id="raLab">ШІ</div>
          <div class="trk hide" id="raTrk"><div class="fil" id="raFill"></div></div>
        </div>
        %(b16)s
        %(b17)s
      </div>''' % {
        "stack": stack,
        "ai": tile("aiW", 150, 390, 235, "jelly", glyph("spark")).replace('class="tw ', 'class="tw hide '),
        "chip": roll_chip("chip", 590, 268, 330, 84, [u"15 хв", u"2 год", u"8 год", u"1 день", u"2 дні"], 42),
        "canva": tile("cvW", 150, 840, 235, "clear edge", g.mark("canva")).replace('class="tw ', 'class="tw hide '),
        "ptile": tile("rtT", 100, 0, 0, "pearl", glyph("person")).replace('class="tw ', 'class="tw hide '),
        "b16": b16_html(), "b17": b17_html(),
    }


@beat
def b01_shelf_stack_ai():
    """«Ти пробувала робити каруселі через штучний інтелект, думала, що
    зробиш швиденько»

    NEAR. The glass shelf lands over her head with her AI carousel on it — the
    slop, already a bit much — then the AI tile that made it, then the timer
    chip reading what she expected: 15 хв."""
    return js('''
  tl.set("#gS", {autoAlpha: 1}, @ty+0.05);
  bin("#shelf", @ty+0.05, 14, 0.45);
  tl.fromTo("#shelf", {scale: 0.9, y: 36}, {scale: 1, y: 0, duration: 0.95, ease: SP}, @ty+0.05);
  // «каруселі» — the stack: two backs, the slop on top
  arr("#stk", @karuseli-0.06, {s: 0.55, y: 40});
  tl.fromTo("#sb1", {rotation: 0, x: 0}, {rotation: -9, x: -18, duration: 0.7, ease: SP}, @karuseli+0.1);
  tl.fromTo("#sb2", {rotation: 0, x: 0}, {rotation: 7, x: 16, duration: 0.7, ease: SP}, @karuseli+0.14);
  // «штучний інтелект» — the AI tile that made it
  arr("#aiW", @shtuchnyi-0.08, {s: 0.5, x: -60});
  G.inner("#aiW .mk", @shtuchnyi-0.08);
  G.sheen("#aiW .sheen", @shtuchnyi+0.35);
  G.ripple("#aiWR", @shtuchnyi+0.3);
  // «швиденько» — what she thought it would take
  arr("#chip", @shvydenko-0.1, {s: 0.6, x: 40, y: 0});
  shn("#chip .sheen", @shvydenko+0.35);''')


@beat
def b02_two_days():
    """«а сидиш над нею вже другий день»

    The chip rolls like an odometer — 15 хв, 2 год, 8 год, 1 день — and lands
    on 2 дні in burgundy with a haptic shake on «другий». Every roll slaps
    another sticker on the slide. Captions drop for «другий день»: the chip
    says it (BLACKOUT)."""
    return js('''
  tl.set("#gS", {autoAlpha: 1}, @sydysh);
  [@sydysh, @nad+0.02, @vzhe-0.02, @druhyi].forEach(function (t, i) {
    tl.to("#chipIn", {y: -84 * (i + 1), duration: 0.34, ease: SP}, t);
  });
  slopPop(tl, "slA", @sydysh+0.08, 0.36);
  G.haptic("#chip", @druhyi+0.2);
  G.bump("#stk", @den);''')


@beat
def b03_canva():
    """«і реально швидше було б зробити в канві»

    The chip steps aside; a Canva tile slides in at the far end of the shelf
    and a finished slide pops straight out of it on «канві» — no stickers,
    no second day."""
    return js('''
  tl.set("#gS", {autoAlpha: 1}, @realno);
  bout("#chip", @realno, 10, 0.3);
  tl.to("#chip", {x: 60, scale: 0.8, duration: 0.3, ease: "power2.in"}, @realno);
  arr("#cvW", @shvydshe+0.04, {s: 0.5, x: 90, y: 0});
  G.inner("#cvW .mk", @shvydshe+0.04);
  // «канві» — out of the tile, done
  tl.set("#cvS", {autoAlpha: 1}, @kanvi-0.02);
  tl.fromTo("#cvS", {x: 205, y: 0, scale: 0.2}, {x: 0, y: 0, scale: 1, duration: 0.7, ease: POP}, @kanvi-0.02);
  G.ripple("#cvWR", @kanvi);
  G.bump("#cvW", @kanvi-0.06);''')


@beat
def b04_effort_meter():
    """«Така собі автоматизація навпаки, де ти виконуєш роботи більше, ніж
    штучний інтелект»

    The slides and Canva clear; the AI tile slides into the lower row of an
    effort meter, a person tile heads the upper one. On «автоматизація» the
    meter shows the promise (ШІ does most); on «навпаки» it swaps; on
    «більше» ТИ overflows the shelf and off the frame; the ШІ sliver bumps on
    «штучний інтелект». Then the shelf's frost spreads into the room."""
    return js('''
  tl.set("#gS", {autoAlpha: 1}, @taka);
  bout(["#stk", "#cvS", "#cvW"], @taka, 10, 0.28);
  tl.to("#aiW", {x: 160 - 465, y: 380 - 310, scale: 100 / 150, duration: 0.7, ease: SP}, @taka+0.08);
  arr("#rtT", @avtomat-0.1, {s: 0.5, y: 20});
  G.inner("#rtT .mk", @avtomat-0.1);
  bin(["#rtLab", "#raLab"], @avtomat, 10, 0.3);
  bin(["#rtTrk", "#raTrk"], @avtomat+0.06, 8, 0.3);
  tl.fromTo("#rtFill", {scaleX: 0}, {scaleX: 0.16, duration: 0.5, ease: SP}, @avtomat+0.12);
  tl.fromTo("#raFill", {scaleX: 0}, {scaleX: 0.82, duration: 0.6, ease: SP}, @avtomat+0.12);
  // «навпаки» — it swaps
  tl.to("#rtFill", {scaleX: 1, duration: 0.7, ease: SP}, @navpaky);
  tl.to("#raFill", {scaleX: 0.06, duration: 0.7, ease: SP}, @navpaky);
  // «більше» — and then some: past the shelf, off the frame
  tl.to("#rtFill", {scaleX: 1.32, duration: 0.6, ease: POP}, @bilshe);
  tl.fromTo("#rtHot", {autoAlpha: 0}, {autoAlpha: 1, duration: 0.3, immediateRender: false}, @bilshe);
  G.haptic("#rowT", @bilshe+0.3);
  // «ніж штучний інтелект» — a sliver
  G.bump("#raLab", @nizh+0.1);
  G.bump("#aiW", @intelekt);
  // «Так от» — out, and the shelf's frost spreads into the room (b05)
  bout(["#rtT", "#rtLab", "#rtTrk", "#aiW", "#raLab", "#raTrk"], @tak, 10, 0.3);
  tl.to("#shelf", {scale: 1.35, duration: 0.55, ease: "power2.in"}, @tak+0.05);
  bout("#shelf", @tak+0.14, 16, 0.42);
  tl.set("#gS", {autoAlpha: 0}, @tak+0.58);''')


# ============================================== B · everybody shows carousels ==
WALL_SRC = (["tr%02d" % i for i in range(1, 6)] + ["wb%02d" % i for i in range(1, 13)]
            + ["kg%02d" % i for i in range(1, 10)])
HUB = (540, 300)


def wall_cells():
    rnd = random.Random(13)
    order = WALL_SRC[:]
    out, last = [], None
    for j in range(-2, 7):
        for i in range(-3, 4):
            x, y = HUB[0] + i * 170, HUB[1] + j * 210
            d = math.hypot(x - HUB[0], y - HUB[1])
            if d < 150:
                continue
            if not order:
                order = WALL_SRC[:]
            pick = rnd.choice([o for o in order if o != last] or order)
            order.remove(pick)
            last = pick
            out.append({"x": x, "y": y, "d": round(d, 1), "src": pick,
                        "o": round(max(0.55, 1 - d / 2400.0), 3)})
    return out


WALL = wall_cells()
WALL_MAXD = max(c["d"] for c in WALL)

k.css("""
/* ---- b05 · the soft room and the wall of carousels behind her ---- */
#roomWrap, #roomTint { position: absolute; inset: 0; }
#roomTint { background: linear-gradient(180deg, rgba(62,8,24,0.16) 0%, rgba(40,5,15,0.34) 100%); }
#wall { position: absolute; inset: 0; transform-origin: 540px 300px; }
.wt { position: absolute; width: 150px; height: 188px; margin: -94px 0 0 -75px; object-fit: cover;
  border-radius: 14px; box-shadow: 0 0 0 1.5px rgba(255,255,255,0.22), 0 20px 34px -14px rgba(12,0,5,0.6); }
""")


@beat
def b05_wall():
    """«Так от, в принципі, тебе не намахали, просто всі ті, хто показують
    каруселі в інстаграмі, вони знають дещо, чого не знаєш ти»

    BEHIND. The room goes soft (a per-beat soft plate built from her matte, so
    she does not halo) and a wall of her real carousels ripples out behind
    her head on «тебе не намахали» — mixed and repeated across three sets so
    it reads as a lot — drifting up like a feed. On «інстаграмі» an Instagram
    tile lands at the hub; on «чого не знаєш ти» the wall is pulled into it
    and the room comes back sharp."""
    f0, n = MATTES["wall"]
    tiles = "\n          ".join(
        '<img class="wt hide" id="wt%d" src="assets/carousels/%s-s.jpg" style="left:%dpx;top:%dpx" alt="">'
        % (i, c["src"], c["x"], c["y"]) for i, c in enumerate(WALL))
    L["behind"].append(u'''
      <div class="g full" id="gW">
        <div id="roomWrap" class="hide">
          <video id="soft" class="plate" src="assets/soft/wall.mp4"
                 data-start="%.3f" data-duration="%.3f" data-media-start="0" muted playsinline></video>
          <div id="roomTint"></div>
        </div>
        <div id="wall">
          %s
        </div>
        %s
      </div>''' % (f0 / 30.0, n / 30.0, tiles,
                   tile("igW", 170, HUB[0] - 85, HUB[1] - 85, "clear edge", g.mark("instagram"))
                   .replace('class="tw ', 'class="tw hide ')))
    cfg = json.dumps([{"d": c["d"], "o": c["o"], "x": c["x"], "y": c["y"]} for c in WALL])
    return js('''
  tl.set("#gW", {autoAlpha: 1}, @tak+0.2);
  tl.fromTo("#roomWrap", {autoAlpha: 0}, {autoAlpha: 1, duration: 0.7, ease: "power1.inOut"}, @tak+0.2);
  // «тебе не намахали» — the wall ripples out of the hub, and drifts up like a feed
  var WL = %s;
  WL.forEach(function (w, n) {
    var t = @tebe + w.d * 0.00048;
    tl.fromTo("#wt" + n, {autoAlpha: 0}, {autoAlpha: w.o, duration: 0.3, ease: "power2.out"}, t);
    tl.fromTo("#wt" + n, {scale: 0.3}, {scale: 1, duration: 0.6, ease: SP, immediateRender: false}, t);
  });
  gsap.set("#wall", {scale: 1.08, y: 0});
  tl.to("#wall", {scale: 1, duration: 1.5, ease: "power2.out"}, @tebe);
  tl.to("#wall", {y: -130, duration: 4.5, ease: "none"}, @tebe);
  // «в інстаграмі» — where all of it lives
  arr("#igW", @insta-0.1, {s: 0.5, y: 30});
  G.inner("#igW .mk", @insta-0.1);
  G.ripple("#igWR", @insta+0.3);
  G.sheen("#igW .sheen", @insta+0.4);
  // «чого не знаєш ти» — pulled into the hub, the room comes back
  WL.forEach(function (w, n) {
    tl.to("#wt" + n, {x: (540 - w.x) * 0.38, y: (300 - w.y) * 0.38, scale: 0, autoAlpha: 0,
                      duration: 0.42, ease: "power2.in"}, @choho + (%.1f - w.d) * 0.00022);
  });
  G.bump("#igW", @choho+0.3);
  bout("#igW", @znayesh+0.12, 12, 0.3);
  tl.to("#roomWrap", {autoAlpha: 0, duration: 0.45, ease: "power1.inOut"}, @znayesh-0.1);
  tl.set("#gW", {autoAlpha: 0}, @znayesh+0.45);''' % (cfg, WALL_MAXD))


# ========================================== C · first: pick the right AI ==
k.css("""
/* ---- the takeover: one burgundy ground, opened twice ---- */
#tk { position: absolute; inset: 0; clip-path: circle(0px at 540px 150px); }
.tsheet { border-radius: 48px; }
#t1Rw { position: absolute; left: 30px; top: 30px; width: 380px; height: 507px; border-radius: 14px;
  overflow: hidden; background: linear-gradient(170deg, #1a1519 0%, #0d0b0e 100%); }
#t1Rw .wf { position: absolute; border-radius: 5px; transform-origin: 0 50%; }
#t1Ri { position: absolute; left: 30px; top: 30px; width: 380px; height: 507px; border-radius: 14px; }
.tfoot { position: absolute; left: 30px; top: 562px; }
""")

WIRE = [  # the builder assembles 04's layout, block by block (380x507 coords)
    (38, 46, 250, 12, "rgba(255,255,255,0.8)"), (38, 66, 200, 12, "rgba(255,255,255,0.8)"),
    (38, 116, 290, 58, "#ff6e9c"), (38, 184, 200, 58, "#ff6e9c"),
    (38, 262, 300, 26, "#ffffff"), (140, 298, 200, 26, "#ffffff"),
    (38, 345, 180, 12, "rgba(255,255,255,0.6)"), (38, 363, 70, 12, "rgba(255,255,255,0.6)"),
    (38, 478, 64, 8, "#ff6e9c"), (318, 478, 28, 8, "rgba(255,255,255,0.4)"),
]


def tk_html():
    wf = "".join('<i class="wf hide" id="wf%d" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx;background:%s"></i>'
                 % (i, x, y, w, h, c) for i, (x, y, w, h, c) in enumerate(WIRE))
    t1 = u'''
        <div class="g full" id="gT1">
          %(n1)s
          %(ai)s
          %(l)s
          %(r)s
          <div class="sheet tsheet hide" id="t1Ls" style="left:70px;top:540px;width:440px;height:640px">
            <div class="tfoot chip">PNG</div>
          </div>
          <div class="sheet tsheet hide" id="t1Rs" style="left:570px;top:540px;width:440px;height:640px">
            <div id="t1Rw">%(wf)s</div>
            <img id="t1Ri" class="hide" src="assets/carousels/wb04-m.jpg" alt="">
            <div class="tfoot chip">HTML</div>
            <div class="sheen"></div>
          </div>
          %(ok)s
        </div>''' % {
        "n1": tile("n1", 120, 480, 90, "jelly", '<span class="nbt" style="font-size:74px">1</span>',
                   "circ hide", ring=False),
        "ai": tile("t1ai", 200, 440, 260, "jelly", glyph("spark"), "hide"),
        "l": tile("t1L", 160, 210, 320, "pearl", stroke("image"), "hide", ring=False),
        "r": tile("t1R", 160, 710, 320, "jelly", stroke("code"), "hide"),
        "ok": tile("t1ok", 96, 937, 506, "jelly", stroke("check"), "circ hide", ring=False),
        "wf": wf}
    t2 = u'''
        <div class="g full" id="gT2">
          %(n2)s
          <div id="sw" class="abs" style="left:335px;top:1070px;width:410px;height:80px">
            <i class="swc hide" style="left:0;background:linear-gradient(160deg,#2a2328,#0d0b0e)"></i>
            <i class="swc hide" style="left:110px;background:linear-gradient(160deg,#ff8ab0,#ff5c8f)"></i>
            <i class="swc hide" style="left:220px;background:linear-gradient(160deg,#ffffff,#f5dfe6)"></i>
            <div class="swa hide" style="left:330px">Aa</div>
          </div>
        </div>''' % {"n2": tile("n2", 104, 488, 70, "jelly", '<span class="nbt" style="font-size:64px">2</span>',
                                "circ hide", ring=False)}
    return (u'<div id="tk" class="hide"><div class="tkg"></div><div class="aur a1"></div>'
            u'<div class="aur a2"></div><div class="aur a3"></div><div class="grain"></div>%s%s</div>'
            % (t1, t2))


k.css("""
.swc { position: absolute; top: 0; width: 80px; height: 80px; border-radius: 50%; display: block;
  box-shadow: inset 0 2px 1px rgba(255,255,255,0.5), 0 0 0 3px rgba(255,255,255,0.85), 0 20px 36px -14px rgba(8,0,3,0.7); }
.swa { position: absolute; top: 0; width: 80px; height: 80px; border-radius: 22px; display: flex;
  align-items: center; justify-content: center; font-size: 40px; font-weight: 900; color: #17141c;
  background: linear-gradient(160deg, #ffffff 0%, #fff5f8 52%, #f5dfe6 100%);
  box-shadow: inset 0 2px 1px #fff, 0 20px 36px -14px rgba(8,0,3,0.7); }
""")


@beat
def b06_first_pick_ai():
    """«По-перше, треба обрати правильний штучний інтелект. Є два типи:»

    OVER. A «1» opens the takeover (iris out of it). The AI tile arrives on
    «правильний» and splits in two on «два типи» — a picture model (pearl,
    an image mark) and a builder (jelly, </>)."""
    return js('''
  tl.set("#gT1", {autoAlpha: 1}, @popershe);
  G.irisOpen("#tk", @popershe, 540, 150, 0.85);
  G.drift("#tk", @popershe, 30);
  arr("#n1", @popershe+0.06, {s: 0.4, y: 0});
  G.inner("#n1 .nbt", @popershe+0.06);
  // «правильний штучний інтелект»
  arr("#t1ai", @pravyl-0.08, {s: 0.5, y: 40});
  G.inner("#t1ai .mk", @pravyl-0.08);
  G.sheen("#t1ai .sheen", @shi3+0.1);
  G.ripple("#t1aiR", @shi3+0.05);
  // «два типи» — it splits
  tl.to("#t1ai", {scale: 0.55, autoAlpha: 0, duration: 0.32, ease: "power2.in"}, @dva);
  tl.set("#t1L", {autoAlpha: 1}, @dva+0.02);
  tl.set("#t1R", {autoAlpha: 1}, @dva+0.02);
  tl.fromTo("#t1L", {x: 250, y: -40, scale: 0.6}, {x: 0, y: 0, scale: 1, duration: 0.85, ease: POP}, @dva+0.02);
  tl.fromTo("#t1R", {x: -250, y: -40, scale: 0.6}, {x: 0, y: 0, scale: 1, duration: 0.85, ease: POP}, @dva+0.02);
  G.inner(["#t1L .sk", "#t1R .sk"], @dva+0.1);''')


@beat
def b07_draws_from_noise():
    """«один малює картинки з нуля»

    The left sheet grows down out of the picture model; in it, colour noise
    resolves into a slide — the slop — the way a diffusion model paints. Its
    file chip says what it is: a flat .png. The slide is #fc, which will
    leave this sheet and rise over her head."""
    return js('''
  tl.set("#gC", {autoAlpha: 1}, @odyn);
  gsap.set(["#t1Ls", "#t1Rs"], {transformOrigin: "50%% 0%%"});
  bin("#t1Ls", @odyn, 14, 0.4);
  tl.fromTo("#t1Ls", {scaleY: 0.2}, {scaleY: 1, duration: 0.8, ease: SP}, @odyn);
  gsap.set("#fc", {x: %.1f, y: %.1f, scale: %.4f});
  tl.set("#fc", {autoAlpha: 1}, @maliuye);
  tl.set("#fcNz", {autoAlpha: 1}, @maliuye);
  tl.fromTo("#fc", {filter: "blur(22px)"}, {filter: "blur(0px)", duration: 0.95, ease: "power2.out"}, @maliuye+0.1);
  tl.set("#fc", {filter: "none"}, @maliuye+1.06);
  tl.to("#fcNz", {autoAlpha: 0, duration: 0.9, ease: "power1.in"}, @kart1);
  G.bump("#t1L", @maliuye);''' % (FC_TK1["x"], FC_TK1["y"], FC_TK1["scale"]))


@beat
def b08_builds_like_a_site():
    """«а інший збирає їх, як сайти»

    The right sheet grows out of the builder; wireframe blocks snap into a
    layout one by one on «збирає», and on «сайти» the real slide — her clean
    one, blond-webinar 04 — lands on top of the blocks. .html."""
    return js('''
  tl.set("#gT1", {autoAlpha: 1}, @a2);
  bin("#t1Rs", @a2, 14, 0.4);
  tl.fromTo("#t1Rs", {scaleY: 0.2}, {scaleY: 1, duration: 0.8, ease: SP}, @a2);
  G.bump("#t1R", @inshyi);
  document.querySelectorAll("#t1Rw .wf").forEach(function (el, i) {
    tl.fromTo(el, {autoAlpha: 0, x: i % 2 ? 40 : -40, scaleX: 0.4},
              {autoAlpha: 1, x: 0, scaleX: 1, duration: 0.42, ease: SP}, @zbyraye + i * 0.085);
  });
  // «сайти» — built
  tl.fromTo("#t1Ri", {autoAlpha: 0, scale: 0.96}, {autoAlpha: 1, scale: 1, duration: 0.5, ease: "power2.out"}, @saity);
  G.sheen("#t1Rs .sheen", @saity+0.4);''')


@beat
def b09_we_need_the_second():
    """«Нам потрібен саме другий»

    The picture sheet and its slide dim back; the builder's sheet gets the
    tick on «другий»."""
    return js('''
  tl.set("#gT1", {autoAlpha: 1}, @nam);
  tl.to(["#t1Ls", "#t1L"], {autoAlpha: 0.42, scale: 0.96, duration: 0.45, ease: "power2.out"}, @potriben);
  tl.to("#fc", {autoAlpha: 0.42, duration: 0.45, ease: "power2.out"}, @potriben);
  G.bump(["#t1Rs", "#t1R"], @same);
  arr("#t1ok", @druhyi2-0.06, {s: 0.3, y: 0});
  G.inner("#t1ok .sk", @druhyi2-0.06);''')


@beat
def b10_sticks_on_everything():
    """«тому що перший наліпить купу елементів, які нам не потрібні»

    The slop is the subject now: it rises out of its sheet to over her head
    as the iris closes onto it, and on «наліпить» stickers slap on one after
    another, spilling off its edges; «не потрібні» — two more, and it sags."""
    return js('''
  tl.set("#gC", {autoAlpha: 1}, @tomu);
  tl.to("#fc", {autoAlpha: 1, duration: 0.2}, @tomu);
  tl.to("#fc", {x: 0, y: 0, scale: 1, duration: 0.9, ease: SP}, @tomu+0.04);
  G.irisClose("#tk", @tomu+0.08, 540, 290, 0.62);
  tl.set("#gT1", {autoAlpha: 0}, @tomu+0.72);
  slopPop(tl, "slB", @nalipyt, 0.12, 0, 9);
  slopPop(tl, "slB", @ne1, 0.2, 9, 12);
  tl.to("#fc", {keyframes: {rotation: [0, -3, 2.5, -1.5, 0]}, duration: 0.7, ease: "none"}, @potribni);''')


@beat
def b11_flip_clean():
    """«а другий буде мінімалістичний просто тому, що він фізично не може
    зробити по-іншому»

    The stickers are knocked off and the slide flips on «другий» to the clean
    one. On «фізично» one more sticker flies at it and bounces off — the edge
    flashes pink, there is nowhere for it to go."""
    return js('''
  tl.set("#gC", {autoAlpha: 1}, @a3);
  slopShed(tl, "slB", @a3+0.02);
  tl.fromTo("#fcIn", {rotationY: 0}, {rotationY: 180, duration: 1.0, ease: FLIP}, @druhyi3-0.04);
  tl.to("#fc", {scale: 0.92, duration: 0.3, ease: "power2.out"}, @druhyi3-0.04);
  tl.to("#fc", {scale: 1, duration: 0.6, ease: SP}, @druhyi3+0.26);
  shn("#fcShn", @minimal+0.1);
  // «фізично не може» — a sticker tries, and bounces
  tl.set("#bn", {autoAlpha: 1}, @fizychno-0.1);
  tl.fromTo("#bn", {x: 0, y: 0, rotation: 0}, {x: -470, y: 80, rotation: -200, duration: 0.42, ease: "power2.in"}, @fizychno-0.1);
  tl.to("#bn", {x: -130, y: 540, rotation: -320, duration: 0.75, ease: "power1.in"}, @fizychno+0.34);
  tl.to("#bn", {autoAlpha: 0, duration: 0.2}, @fizychno+0.9);
  tl.fromTo("#fcRim", {autoAlpha: 0}, {autoAlpha: 1, duration: 0.08, immediateRender: false}, @fizychno+0.3);
  tl.to("#fcRim", {autoAlpha: 0, duration: 0.5, ease: "power2.out"}, @fizychno+0.42);
  G.haptic("#fc", @fizychno+0.3);''')


# ======================================== D · second: teach it the layout ==
@beat
def b12_second_style_then_layout():
    """«Друге — його треба навчити не просто стилю, а того, як саме
    розміщувати інформацію:»

    OVER. A «2», and the clean slide itself opens the takeover: the iris comes
    out of it as it grows to 2x in the middle of the burgundy. «навчити» —
    style swatches under it (black, pink, white, the typeface); «а того» —
    they step back; «розміщувати» — dashed layout zones draw over the slide."""
    return js('''
  tl.set("#gT2", {autoAlpha: 1}, @druhe);
  G.irisOpen("#tk", @druhe+0.04, 540, 290, 0.9);
  tl.to("#fc", {x: %.1f, y: %.1f, scale: %.2f, duration: 1.05, ease: SOFT}, @druhe+0.06);
  arr("#n2", @druhe+0.12, {s: 0.4, y: 0});
  G.inner("#n2 .nbt", @druhe+0.12);
  // «навчити не просто стилю»
  tl.fromTo("#sw > *", {autoAlpha: 0, scale: 0.4, y: 20}, {autoAlpha: 1, scale: 1, y: 0, duration: 0.6, ease: POP,
            stagger: 0.09}, @navchyty);
  G.bump("#sw", @styliu);
  // «а того, як саме розміщувати інформацію»
  tl.to("#sw > *", {autoAlpha: 0.3, scale: 0.86, duration: 0.45, ease: "power2.out", stagger: 0.04}, @a4);
  ["#z1", "#z2", "#z3"].forEach(function (z, i) {
    tl.fromTo(z, {autoAlpha: 0, scale: 1.08}, {autoAlpha: 1, scale: 1, duration: 0.45, ease: SP}, @rozmisch + i * 0.14);
  });
  gsap.set([".zl"], {autoAlpha: 0});
  tl.fromTo("#z2L", {autoAlpha: 0, y: 6}, {autoAlpha: 1, y: 0, duration: 0.3, immediateRender: false}, @rozmisch+0.3);''' % (
        FC_TK2["x"], FC_TK2["y"], FC_TK2["scale"]))


@beat
def b13_text_pictures_placement():
    """«скільки тексту, які картинки, де що стоїть.»

    The two text zones get their labels and fill on «тексту»; a photo zone
    joins on «картинки» where the slide had none; smart guides flash on «де
    що стоїть» and the photo zone snaps onto the text zone's line."""
    return js('''
  tl.set("#gT2", {autoAlpha: 1}, @skilky);
  tl.fromTo(["#z1L", "#z3L"], {autoAlpha: 0, y: 6}, {autoAlpha: 1, y: 0, duration: 0.3, immediateRender: false}, @tekstu-0.1);
  tl.to(["#z1", "#z3"], {backgroundColor: "rgba(255,110,156,0.30)", duration: 0.3}, @tekstu-0.1);
  tl.to(["#z1", "#z3"], {backgroundColor: "rgba(255,110,156,0.10)", duration: 0.5}, @tekstu+0.4);
  // «які картинки»
  tl.fromTo("#z4", {autoAlpha: 0, scale: 0.6, y: 14}, {autoAlpha: 1, scale: 1, y: 14, duration: 0.55, ease: POP}, @kart2-0.1);
  tl.fromTo("#z4L", {autoAlpha: 0}, {autoAlpha: 1, duration: 0.25, immediateRender: false}, @kart2+0.1);
  // «де що стоїть» — smart guides, and the photo zone snaps to the line
  tl.fromTo("#gd1", {autoAlpha: 0, scaleY: 0}, {autoAlpha: 1, scaleY: 1, duration: 0.35, ease: "power2.out"}, @de);
  tl.fromTo("#gd2", {autoAlpha: 0, scaleX: 0}, {autoAlpha: 1, scaleX: 1, duration: 0.35, ease: "power2.out"}, @de+0.12);
  tl.fromTo("#gd3", {autoAlpha: 0, scaleY: 0}, {autoAlpha: 1, scaleY: 1, duration: 0.35, ease: "power2.out"}, @de+0.2);
  tl.to("#z4", {y: 0, duration: 0.45, ease: POP}, @stoyit);
  G.bump("#z4", @stoyit+0.35);
  tl.to(".gd", {autoAlpha: 0, duration: 0.4}, @stoyit+0.75);''')


@beat
def b14_template_locks():
    """«По факту зробити собі шаблон того, як це має виглядати.»

    The photo of the slide fades out from under its guides: what is left is
    the template — the zones on a dark ground. It locks on «шаблон», then
    shrinks back over her head as the iris closes onto it."""
    return js('''
  tl.set("#gT2", {autoAlpha: 1}, @pofaktu);
  tl.to("#fcImg", {autoAlpha: 0, duration: 0.6, ease: "power1.inOut"}, @zrob3);
  tl.to(".zn", {backgroundColor: "rgba(255,110,156,0.16)", duration: 0.6}, @zrob3);
  arr("#fcLock", @shablon-0.04, {s: 0.3, y: 0});
  G.inner("#fcLock .sk", @shablon-0.04);
  shn("#fcShn", @shablon+0.2);
  // «того, як це має виглядати» — back over her head
  bout(["#sw", "#n2"], @toho+0.1, 10, 0.3);
  tl.to("#fc", {x: 0, y: 0, scale: 1, duration: 0.9, ease: SP}, @toho+0.3);
  G.irisClose("#tk", @toho+0.36, 540, 290, 0.62);
  tl.set("#gT2", {autoAlpha: 0}, @toho+1.0);''')


# ============================================ E · then it gets fast (behind) ==
FAN = [-28, -14, 0, 14, 28]
FAN_SRC = ["tr01", "tr02", "tr03", "tr04", "tr05"]
FAN_R, FAN_P = 800, (540, 1250)

k.css("""
/* ---- b15 · five slides, one template, fanned behind her ---- */
.fanc { position: absolute; left: 360px; top: 225px; width: 360px; height: 450px; object-fit: cover;
  border-radius: 22px; box-shadow: 0 0 0 2.5px rgba(255,255,255,0.6), 0 50px 90px -30px rgba(10,0,4,0.75); }
""")


@beat
def b15_fan_behind():
    """«І тільки після цього ти дійсно почнеш робити каруселі швидко,»

    The template waits over her head, bumps on «після цього»; on «почнеш» it
    lifts and deals five finished slides from one template (blond-trend, same
    photo, same hands) into a hand of cards fanned behind her head — matted,
    bleeding off both edges — and riffles them on «швидко»."""
    order = [0, 4, 1, 3, 2]
    L["behind"].append('<div class="g full" id="gF">%s</div>' % "".join(
        '<img class="fanc hide" id="fan%d" src="assets/carousels/%s-m.jpg" alt="">' % (i, FAN_SRC[i])
        for i in order))
    slots = []
    for a in FAN:
        r = math.radians(a)
        slots.append({"x": round(FAN_R * math.sin(r), 1), "y": round(FAN_R * (1 - math.cos(r)), 1), "r": a})
    return js('''
  tl.set("#gC", {autoAlpha: 1}, @itilky);
  G.bump("#fc", @pislia);
  tl.to("#fc", {y: -110, scale: 0.72, duration: 0.6, ease: SP}, @pochnesh-0.1);
  tl.set("#gF", {autoAlpha: 1}, @pochnesh-0.08);
  var FS = %s;
  [2, 1, 3, 0, 4].forEach(function (i, n) {
    var s = FS[i], t = @pochnesh-0.02 + n * 0.09;
    tl.set("#fan" + i, {autoAlpha: 1}, t);
    tl.fromTo("#fan" + i, {x: 0, y: -270, scale: 0.6, rotation: 0},
              {x: s.x, y: s.y, scale: 1, rotation: s.r, duration: 0.8, ease: SP}, t);
  });
  // «швидко» — a riffle
  FS.forEach(function (s, i) {
    tl.to("#fan" + i, {rotation: s.r * 1.18, duration: 0.18, ease: "power2.out"}, @shvydko + i * 0.03);
    tl.to("#fan" + i, {rotation: s.r, duration: 0.5, ease: SP}, @shvydko+0.18 + i * 0.03);
  });
  // «тому що в нього вже буде система» — back into the template
  FS.forEach(function (s, i) {
    tl.to("#fan" + i, {x: 0, y: -270, scale: 0.6, rotation: 0, autoAlpha: 0, duration: 0.4, ease: "power2.in"},
          @tomu2 + Math.abs(i - 2) * 0.03);
  });
  tl.set("#gF", {autoAlpha: 0}, @tomu2+0.46);''' % json.dumps(slots))


# ========================================== F · the AI fills the template ==
k.css("""
#cab2 { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; overflow: visible; }
""")


def b16_html():
    return (tile("ai2", 170, 165, 225, "jelly", glyph("spark")).replace('class="tw ', 'class="tw hide ')
            + '<svg id="cab2" class="cab" viewBox="0 0 1080 1920">'
              '<path class="tube hide" id="c2T" d="M 340 310 C 410 360 480 360 548 310"/>'
              '<path class="core hide" id="c2C" d="M 340 310 C 410 360 480 360 548 310"/>'
              '<g class="pkg"><path class="pkt hide" id="c2P" d="M 340 310 C 410 360 480 360 548 310"/></g>'
              '</svg>')


@beat
def b16_system_places():
    """«тому що в нього вже буде система, за якою він розставляє всі твої
    тексти, картинки та елементи.»

    NEAR. The shelf comes back; the template moves onto it and the same AI
    tile sits beside it. «система» — the zones light in order; «розставляє»
    — a cable; «тексти» — lines fly from the AI into the text zones,
    «картинки» — a photo into ФОТО, «елементи» — the footer marks."""
    return js('''
  tl.set("#gS", {autoAlpha: 1}, @tomu2+0.3);
  bin("#shelf", @tomu2+0.3, 14, 0.45);
  tl.fromTo("#shelf", {scale: 0.9}, {scale: 1, duration: 0.9, ease: SP, immediateRender: false}, @tomu2+0.3);
  tl.to("#fc", {x: %.1f, y: %.1f, scale: %.2f, duration: 0.9, ease: SP}, @tomu2+0.3);
  arr("#ai2", @tomu2+0.45, {s: 0.5, x: -40});
  G.inner("#ai2 .mk", @tomu2+0.45);
  // «система»
  tl.to(".zn", {backgroundColor: "rgba(255,110,156,0.42)", duration: 0.18, stagger: 0.12}, @systema);
  tl.to(".zn", {backgroundColor: "rgba(255,110,156,0.12)", duration: 0.4, stagger: 0.12}, @systema+0.2);
  // «розставляє» — wired in
  G.draw("c2T", @rozstav, 0.4); G.draw("c2C", @rozstav, 0.4);
  tl.set(["#c2T", "#c2C"], {autoAlpha: 1}, @rozstav);
  G.bump("#ai2", @rozstav);
  // «тексти», «картинки», «елементи»
  G.packet("c2P", @teksty-0.3, 0.4);
  tl.to([".zl"], {autoAlpha: 0, duration: 0.25}, @teksty-0.1);
  ["#pa", "#pb", "#pc", "#pd", "#pe", "#pf", "#pg", "#ph"].forEach(function (p, i) {
    tl.fromTo(p, {autoAlpha: 0, x: -320, y: 40, scale: 0.4}, {autoAlpha: 1, x: 0, y: 0, scale: 1, duration: 0.5,
              ease: SP}, @teksty + i * 0.05);
  });
  G.packet("c2P", @kart3-0.25, 0.35);
  tl.fromTo("#pi", {autoAlpha: 0, x: -360, y: 20, scale: 0.4}, {autoAlpha: 1, x: 0, y: 0, scale: 1, duration: 0.55,
            ease: POP}, @kart3);
  tl.to("#z4 .sk", {autoAlpha: 0, duration: 0.2}, @kart3+0.2);
  G.packet("c2P", @elementy-0.25, 0.35);
  tl.fromTo(["#pj", "#pk"], {autoAlpha: 0, x: -330, y: 60, scale: 0.4}, {autoAlpha: 1, x: 0, y: 0, scale: 1,
            duration: 0.5, ease: SP, stagger: 0.08}, @elementy);
  tl.to(".zn", {borderColor: "rgba(255,110,156,0)", backgroundColor: "rgba(255,110,156,0)", duration: 0.4}, @elementy+0.3);
  tl.to("#fcLock", {autoAlpha: 0, duration: 0.25}, @elementy+0.3);
  shn("#fcShn", @elementy+0.4);''' % (FC_SHELF["x"], FC_SHELF["y"], FC_SHELF["scale"]))


# ============================================= G · third: the text itself ==
HEAD = u"Чому твої каруселі|не продають?"
# human typing: a typo, backspaced ("карусклі" -> "каруселі")
TYPED = []
_s = u""
for ch in u"Чому твої карускл":
    _s += ch
    TYPED.append(_s)
for _ in range(3):
    _s = _s[:-1]
    TYPED.append(_s)
for ch in u"селі|не продають?":
    _s += ch
    TYPED.append(_s)

k.css("""
/* ---- b17 · the text editor, the AI trained ---- */
#ed { left: 320px; top: 140px; width: 660px; height: 340px; border-radius: 48px; }
#edL { position: absolute; left: 44px; top: 36px; }
#edH { position: absolute; left: 44px; top: 76px; width: 590px; font-size: 48px; font-weight: 700;
  line-height: 58px; letter-spacing: -0.02em; color: #17141c; white-space: pre; }
#edH b { display: inline-block; width: 4px; height: 46px; margin-left: 3px; vertical-align: -8px;
  background: #b4122f; border-radius: 2px; }
#edB { position: absolute; left: 44px; top: 214px; width: 590px; font-size: 27px; font-weight: 500;
  line-height: 40px; color: rgba(23,20,28,0.55); }
#ai3Ring { position: absolute; left: 105px; top: 310px; width: 170px; height: 170px; overflow: visible; }
#ai3Ring circle { fill: none; stroke-width: 7; stroke-linecap: round; }
""")


def b17_html():
    return (tile("n3", 104, 138, 150, "jelly", '<span class="nbt" style="font-size:64px">3</span>',
                 "circ hide", ring=False)
            + u'''<div class="sheet hide" id="ed"><div class="t-micro" id="edL">СЛАЙД 1</div>
            <div id="edH"><span id="edT"></span><b id="edC"></b></div>
            <div id="edB" class="hide">Бо в них немає системи.<br>Ось 3 кроки, що це змінять &#8594;</div>
            <div class="sheen"></div></div>'''
            + '<svg id="ai3Ring" class="hide" viewBox="0 0 170 170"><circle cx="85" cy="85" r="80" stroke="rgba(255,255,255,0.25)"/>'
              '<circle id="ai3P" class="hide" cx="85" cy="85" r="80" stroke="#ff6e9c" transform="rotate(-90 85 85)"/></svg>'
            + tile("ai3", 130, 125, 330, "jelly", glyph("spark")).replace('class="tw ', 'class="tw hide ')
            + tile("ai3ok", 50, 238, 318, "pearl", stroke("check"), "circ hide", ring=False))


@beat
def b17_write_the_text():
    """«І звичайно, треба ще й вміти правильно написати сам текст для
    каруселі, а в ідеалі — навчити той же самий штучний інтелект це робити!»

    NEAR, on the shelf. The template leaves; a «3» and a text editor arrive.
    The headline is typed by hand — slowly, with a typo backspaced. «навчити»
    — the AI tile's ring fills and it gets a tick; «це робити!» — the body
    lands in one go."""
    return js('''
  tl.set("#gS", {autoAlpha: 1}, @i5);
  bout(["#ai2", "#c2T", "#c2C"], @i5, 10, 0.3);
  tl.to("#fc", {x: 300, y: -20, scale: 0.6, duration: 0.4, ease: "power2.in"}, @i5);
  bout("#fc", @i5+0.1, 12, 0.3);
  tl.set("#gC", {autoAlpha: 0}, @i5+0.45);
  arr("#n3", @i5+0.1, {s: 0.4, y: 0});
  G.inner("#n3 .nbt", @i5+0.1);
  arr("#ed", @i5+0.3, {s: 0.7, y: 40, d: 0.9});
  // «треба ще й вміти правильно написати сам текст» — by hand, slowly
  var TY = %s, ty = {v: 0}, el = document.getElementById("edT");
  tl.fromTo(ty, {v: 0}, {v: TY.length - 1, duration: @kar4 + 0.45 - @treba, ease: "none",
            onUpdate: function () { el.textContent = TY[Math.round(ty.v)].replace("|", "\\n"); }}, @treba);
  tl.to("#edC", {autoAlpha: 0, duration: 0.01}, @kar4+0.6);
  tl.to("#edC", {autoAlpha: 1, duration: 0.01}, @kar4+0.9);
  // «а в ідеалі навчити той же самий ШІ»
  arr("#ai3", @a5+0.02, {s: 0.5, y: 30});
  bin("#ai3Ring", @a5+0.12, 8, 0.3);
  G.inner("#ai3 .mk", @a5+0.02);
  tl.set("#ai3P", {autoAlpha: 1}, @navch2);
  G.draw("ai3P", @navch2, @samyi - @navch2);
  arr("#ai3ok", @samyi, {s: 0.3, y: 0});
  G.inner("#ai3ok .sk", @samyi);
  G.ripple("#ai3R", @samyi+0.05);
  // «це робити!» — in one go
  tl.set("#edC", {autoAlpha: 0}, @tse);
  tl.fromTo("#edB", {autoAlpha: 0, clipPath: "inset(0px 100%% 0px 0px)"},
            {autoAlpha: 1, clipPath: "inset(0px 0%% 0px 0px)", duration: 0.35, ease: "power2.out"}, @tse+0.04);
  G.sheen("#ed .sheen", @robyty2);
  G.bump("#ai3", @tse);
  bout(["#n3", "#ed", "#ai3", "#ai3ok", "#ai3Ring", "#shelf"], @i6-0.05, 10, 0.3);
  tl.set("#gS", {autoAlpha: 0}, @i6+0.3);''' % json.dumps(TYPED, ensure_ascii=False))


# ============================================== H · next reel, subscribe ==
# The Follow button — reusable (reels 16, 18): Стежити -> Відстежується,
# pressed on the word. follow_button() is the markup, the press is 4 lines.
def follow_button(bid, x, y, w=300, h=74):
    return (u'<div class="flw hide" id="%(b)s" style="left:%(x)dpx;top:%(y)dpx;width:%(w)dpx;height:%(h)dpx">'
            u'<div class="fla" id="%(b)sA">Стежити</div>'
            u'<div class="flb hide" id="%(b)sB"><svg class="sk" viewBox="0 0 24 24">%(ck)s</svg>Відстежується</div>'
            u'</div>' % {"b": bid, "x": x, "y": y, "w": w, "h": h, "ck": STROKES["check"]})


k.css("""
/* ---- b18 · the next reel, as a notification ---- */
#nx { left: 70px; top: 110px; width: 940px; height: 380px; }
#nxTh { position: absolute; left: 36px; top: 30px; width: 190px; height: 320px; border-radius: 28px;
  overflow: hidden; background: linear-gradient(170deg, #1d171b 0%, #0b090b 100%);
  box-shadow: 0 0 0 2px rgba(255,255,255,0.25), 0 24px 44px -18px rgba(0,0,0,0.6); }
#nxTh img { position: absolute; left: 0; top: 34px; width: 190px; height: 253px; }
#nxPl { position: absolute; left: 57px; top: 122px; width: 76px; height: 76px; border-radius: 50%;
  background: rgba(255,255,255,0.30); box-shadow: inset 0 2px 1px rgba(255,255,255,0.6), 0 10px 24px rgba(0,0,0,0.35);
  display: flex; align-items: center; justify-content: center; }
#nxPl svg { width: 40px; height: 40px; fill: #fff; margin-left: 5px; }
#nxAv { position: absolute; left: 262px; top: 36px; width: 70px; height: 70px; border-radius: 50%;
  background: url("assets/avatar.jpg") center / cover no-repeat; box-shadow: 0 0 0 3px rgba(255,255,255,0.7); }
#nxNm { position: absolute; left: 352px; top: 46px; font-size: 40px; font-weight: 700; letter-spacing: -0.01em; }
#nxTm { position: absolute; right: 44px; top: 56px; font-size: 27px; color: rgba(255,255,255,0.55); }
.nxs { position: absolute; top: 128px; width: 118px; height: 157px; border-radius: 10px; object-fit: cover;
  box-shadow: 0 0 0 1.5px rgba(255,255,255,0.5), 0 16px 30px -12px rgba(0,0,0,0.6); }
.flw { position: absolute; }
.fla, .flb { position: absolute; inset: 0; border-radius: 999px; display: flex; align-items: center;
  justify-content: center; gap: 10px; font-size: 32px; font-weight: 700; letter-spacing: -0.01em; }
.fla { color: #fff; background: linear-gradient(165deg, #e0204b 0%, #ab112e 46%, #6b081c 100%);
  box-shadow: inset 0 2px 1px rgba(255,255,255,0.5), inset 0 -16px 26px -12px rgba(255,125,165,0.6),
              0 22px 40px -16px rgba(70,4,20,0.7); }
.flb { color: #17141c; font-size: 29px; background: linear-gradient(160deg, #ffffff 0%, #fff5f8 52%, #f5dfe6 100%);
  box-shadow: inset 0 2px 1px #fff, 0 22px 40px -16px rgba(30,4,12,0.6); }
.flb .sk { width: 30px; height: 30px; stroke: #b4122f; stroke-width: 3; }
""")


@beat
def b18_next_reel():
    """«І в наступному рілсі я покажу як налаштована повна система швидкого
    створення каруселей за 15 хвилин,»

    NEAR. A glass notification from her: a reel thumbnail with play (bumps on
    «покажу»); «повна система» — three slides from one template deal out of
    it; «швидкого створення каруселей» — the timer chip from the start comes
    back, still reading 2 дні, and on «15» rolls to 15 хв. Captions drop for
    «15 хвилин» (BLACKOUT)."""
    L["near"].append(u'''
      <div class="g full" id="gN">
        <div class="dglass edge hide" id="nx">
          <div id="nxTh"><img src="assets/carousels/wb06-s.jpg" alt=""><div id="nxPl">%(play)s</div></div>
          <div id="nxAv"></div><div class="cx" id="nxNm">Рута</div><div class="cx" id="nxTm">скоро</div>
          <img class="nxs hide" id="nxs0" src="assets/carousels/wb02-s.jpg" style="left:262px" alt="">
          <img class="nxs hide" id="nxs1" src="assets/carousels/wb05-s.jpg" style="left:396px" alt="">
          <img class="nxs hide" id="nxs2" src="assets/carousels/wb12-s.jpg" style="left:530px" alt="">
          %(chip)s
          %(follow)s
        </div>
      </div>''' % {"play": glyph("play", "pl"),
                   "chip": roll_chip("nxc", 262, 294, 300, 76, [u"2 дні", u"15 хв"], 40, last_red=False),
                   "follow": follow_button("flw", 590, 294, 310, 76)})
    return js('''
  tl.set("#gN", {autoAlpha: 1}, @i6);
  gsap.set("#nxcIn i:first-child", {color: "#b4122f"});
  arr("#nx", @i6+0.04, {s: 0.62, y: -26});
  tl.fromTo(["#nxTh", "#nxAv", "#nxNm", "#nxTm"], {autoAlpha: 0, y: 10}, {autoAlpha: 1, y: 0, duration: 0.5,
            ease: SP, stagger: 0.05}, @i6+0.18);
  // «покажу»
  G.bump("#nxPl", @pokazhu);
  // «повна система» — three slides, one template
  ["#nxs0", "#nxs1", "#nxs2"].forEach(function (s, i) {
    tl.fromTo(s, {autoAlpha: 0, x: -150 - i * 134, scale: 0.5, rotation: -8},
              {autoAlpha: 1, x: 0, scale: 1, rotation: 0, duration: 0.6, ease: SP}, @povna + i * 0.1);
  });
  // «швидкого створення каруселей» — the chip from the start, still 2 дні
  arr("#nxc", @shvydkoho+0.04, {s: 0.6, x: -30, y: 0});
  // «15» — for real this time
  tl.to("#nxcIn", {y: -76, duration: 0.45, ease: SP}, @p15);
  G.haptic("#nxc", @p15+0.4);
  shn("#nxc .sheen", @p15+0.3);''')


@beat
def b19_follow():
    """«тому обов'язково підпишись»

    The Follow button lands beside the chip on «тому» and is pressed on
    «підпишись»: Стежити -> Відстежується. The reel ends on it."""
    return js('''
  tl.set("#gN", {autoAlpha: 1}, @tomu3);
  arr("#flw", @tomu3+0.04, {s: 0.6, x: 30, y: 0});
  tl.to("#flw", {scale: 0.9, duration: 0.08, ease: "power2.out"}, @pidpysh);
  tl.to("#flw", {scale: 1, duration: 0.4, ease: POP}, @pidpysh+0.08);
  tl.set("#flwB", {autoAlpha: 1}, @pidpysh+0.08);
  tl.set("#flwA", {autoAlpha: 0}, @pidpysh+0.08);
  G.inner("#flwB .sk", @pidpysh+0.02);''')


# ================================================================ assemble ==
L["near"].insert(0, None)          # the shelf goes first in NEAR (placeholder)
L["tk"].append(tk_html())

# Captions drop only on redundancy (STYLE.md §2b.1).
BLACKOUT = [
    (5.06, 5.50, "b02 — the chip reads 2 дні on «другий день»"),
    (73.08, 74.00, "b18 — the chip reads 15 хв on «15 хвилин»"),
]
INVERT = []

HEAD_JS = r"""
  var G = helpers(tl);
  function bin(sel, t, b, d) { d = d || 0.38; G.blurIn(sel, t, b || 12, d); tl.set(sel, {filter: "none"}, t + d + 0.01); }
  function bout(sel, t, b, d) { d = d || 0.32; G.blurOut(sel, t, b || 10, d); tl.set(sel, {filter: "none"}, t + d + 0.01); }
  function arr(sel, t, o) {
    o = o || {};
    bin(sel, t, o.blur || 12, 0.36);
    tl.fromTo(sel, {scale: o.s == null ? 0.5 : o.s, x: o.x || 0, y: o.y == null ? 34 : o.y},
              {scale: 1, x: 0, y: 0, duration: o.d || 0.85, ease: o.ease || POP}, t);
  }
  function shn(sel, t) {
    gsap.set(sel, {xPercent: -120});
    tl.fromTo(sel, {xPercent: -120}, {xPercent: 120, duration: 0.8, ease: "power2.inOut", immediateRender: false}, t);
  }
  gsap.set(".sheen", {xPercent: -120});
  slopInit("slA"); slopInit("slB");
"""


def main():
    gj = []
    for fn in BEATS:
        j = fn()
        gj.append("  /* %s */" % fn.__name__)
        gj.append(j.rstrip())
    L["near"][0] = shelf_html()
    gfx = "\n".join(L["behind"] + L["near"] + L["tk"] + L["top"])

    # the slow push on the plate (§0.8): her, her mattes, and what sits in her
    # room (the soft room and wall ride in #gW, the fan in #gF) move as one
    push = ["#vid", ".matte", "#gW", "#gF"]
    head = [g.js(), slop.js(), HEAD_JS,
            '  gsap.set(%s, {transformOrigin: "540px 820px"});' % json.dumps(push),
            '  tl.fromTo(%s, {scale: 1}, {scale: 1.045, duration: %.3f, ease: "none"}, 0);'
            % (json.dumps(push), DUR)]
    doc = k.document(
        title=u"Reel 13 — каруселі через ШІ",
        plate="assets/base.mp4",
        gfx_html=g.defs(EXTRA_DEFS) + "\n" + slop.defs() + "\n" + gfx,
        gfx_js="\n".join(head + gj),
        caps=CAPS,
        blackout=BLACKOUT,
        invert=INVERT,
    )
    # Both blackouts are one short phrase mid-sentence: dropping the plaque
    # for them reads as a blink. The captions go, the plaque stays.
    for a, b, _ in BLACKOUT:
        for line in ('  tl.to("#scrim", {autoAlpha: 0, duration: 0.20}, %.3f);\n' % (a - 0.20),
                     '  tl.to("#scrim", {autoAlpha: 1, duration: 0.25}, %.3f);\n' % b):
            assert line in doc, line
            doc = doc.replace(line, "", 1)

    out = os.path.join(HERE, "index.html")
    io.open(out, "w", encoding="utf-8").write(doc)
    print("index.html  %d captions, %d beats, %d wall tiles, %.1f KB"
          % (len(CAPS), len(BEATS), len(WALL), os.path.getsize(out) / 1024.0))


main()
