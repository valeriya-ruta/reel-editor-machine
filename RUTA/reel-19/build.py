# -*- coding: utf-8 -*-
"""Reel 19 — «Той самий хук»: каруселі за 5 хвилин. Posts 2026-10-03.

Variant B, refined glass (STYLE.md §0). The follow-up reel 13 promised.

The one object is **the carousel**, and the reel builds the system that makes
it: a design system (step 1), two skills (step 2), one Claude chat that pulls
them together (step 3). The whole Claude flow is built as graphics — her call
for this reel: «no need, just animate it».

The chain, behind -> near -> over -> near -> behind -> near -> over -> near:
    a wall of her real carousels ripples out behind her head on «каруселі»,
    fed by an AI tile; two good ones come forward on «гарно», and the slop
    slams in between them on «не ай-слоп» -> the wall is pulled away, the slop
    multiplies, sags, and sinks behind her -> a time chip balloons 20 хв ->
    3 год, a by-hand chip says 1 год -> the system: three step tiles wired on
    a shelf, a carousel out of the last one, the chip rolls down to 5 хв ->
    her coffee-sip insert (left clear) -> the iris opens out of a «1»:
    Claude, and the Design System sheet grows
    out of it — type, colour, image placement, saved, liked to 100 % -> the
    sheet folds away and the iris closes onto step 2: two skills train, the
    first one opens her YouTube video, the second lights -> the shelf's frost
    spreads into the room, one long text rises behind her and is cut into
    five slides -> step 3 and a 5:00 clock: the Claude chat opens, she
    dictates, both skills snap in, output flips to Design, the design system
    from step 1 is attached, send -> her gag (left clear) -> the iris opens
    on twelve slides fanned out, the clock at 0:00 -> one is edited by hand,
    Export to Canva, the slides pour into Canva -> the iris closes onto the
    Canva tile, which flips into RUTA: one voice note -> a reel script, a
    carousel, stories -> the three steps once more, a client's carousel out
    of them -> a DM: «карусель», sent.

The 5:00 clock is the plan's spine, re-cut to what she says: steps 1 and 2 are
one-time setup («Це робиться один раз»), so the clock runs through step 3 —
the part that takes five minutes — and reads 0:00 on the fan. It cannot land
on «Бадабім, бадабум» itself: that is her tilted-frame gag (NO_PAINT), so the
fan and the 0:00 arrive on «в тебе є карусель», the line right after it.

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
sys.path.insert(0, os.path.join(ROOT, "reel-13"))
from kit import Kit  # noqa: E402
from glass import Glass  # noqa: E402
from slop import Slop  # noqa: E402  (reel 13's component, imported, not forked)

DUR = 81.717           # 2452 plate frames / 30 (work/w40-queue2.log)
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
# NO-PAINT ZONES — her own editing (STYLE.md §4a).
#   17.40 – 17.77   a 0.37 s closeup: she sips her iced coffee with a side-eye
#                   after «за 5 хвилин» (the gap between shots 0 and 1 in
#                   work/r19/shots — too short for shots.py to call a shot)
#   58.75 – 59.75   on «Бадабім, бадабум» she pulls the frame back and tilts
#                   it over (tools/pullouts.py; tools/shots.py sees the 0.5 s
#                   tilted shot 59.17-59.67). Captions only.
# From ~77.37 to the end she punches in for the CTA (4.3 s, a closer framing,
# not a gag — she points at the viewer): it keeps its beat, but her hair rises
# to y ~465, so the DM sits higher and the system shelf clears before the cut.
NO_PAINT = [(17.40, 17.77), (58.75, 59.75)]

# ---------------------------------------------------------------------------
# Words. Script spelling on her timing (work/r19/captions.json, settled with
# work/r19/caption-patch.json). Ends re-derived from the next start.
CAPS = k.load_captions(os.path.join(ROOT, "work", "r19", "captions.json"))
for _a, _b in zip(CAPS, CAPS[1:]):
    _a["e"] = round(max(_a["s"] + 0.10, _b["s"] - 0.085), 3)


def _n(s):
    return "".join(ch for ch in s.lower() if ch.isalnum() or ch == "+")


def at(word, near):
    hits = [c for c in CAPS if _n(word) in [_n(x) for x in c["w"].split()]]
    c = min(hits, key=lambda c: abs(c["s"] - near))
    assert abs(c["s"] - near) < 0.5, (word, near, c["s"])
    return c


def S(w, near):
    return at(w, near)["s"]


T = {
    # A · hook
    "karuseli": S(u"каруселі", 1.9), "shtuchnym": S(u"штучним", 2.5),
    "intelektom": S(u"інтелектом", 2.9), "shvydko": S(u"швидко", 3.8),
    "harno": S(u"гарно", 4.5), "aislop": S(u"ай-слоп", 5.7),
    "ale": S(u"але", 6.4), "vykhodyt": S(u"виходить", 7.2),
    "zabyraie": S(u"забирає", 7.8), "chasu": S(u"часу", 8.2),
    "bilshe": S(u"більше", 8.8), "zrobyla": S(u"зробила", 9.9),
    "starinke": S(u"старінкє", 11.0), "yakshcho": S(u"Якщо", 11.5),
    "pokazhu": S(u"покажу", 12.9), "svoiu": S(u"свою", 14.1),
    "systemu": S(u"систему", 14.3), "karuseli2": S(u"каруселі", 15.4),
    "realno": S(u"реально", 16.0), "za": S(u"за", 16.5), "five": S("5", 16.7),
    # B · step 1
    "krok1": S(u"Крок", 17.9), "pershyi": S(u"перший", 18.1),
    "zakhodzhu": S(u"Заходжу", 18.8), "claude1": S("Claude", 19.4), "proshu": S(u"прошу", 19.7),
    "stvoryty": S(u"створити", 20.1), "design1": S("Design", 20.6),
    "i1": S(u"і", 21.8), "detalei": S(u"деталей", 21.9),
    "produmuiu": S(u"продумую", 22.5), "shryfty": S(u"шрифти", 23.6),
    "kolory": S(u"кольори", 24.4), "yak": S(u"як", 25.0),
    "rozmisch": S(u"розміщуються", 25.1), "kartynky": S(u"картинки", 25.6),
    "odyn": S(u"один", 27.0), "raz": S(u"раз", 27.3), "ale2": S(u"але", 27.9),
    "treba": S(u"треба", 28.1), "dovesty": S(u"довести", 28.4),
    "koly": S(u"коли", 29.2), "sto": S("100%", 30.2),
    "podob": S(u"подобається", 31.0),
    # C · step 2
    "krok2": S(u"Крок", 32.0), "druhyi": S(u"другий", 32.1),
    "treniu": S(u"Треную", 32.7), "dva": S(u"два", 33.3),
    "skily": S(u"скіли", 33.7), "pershyi2": S(u"Перший", 34.5),
    "styli": S(u"стилі", 35.4), "movlennia": S(u"мовлення", 35.7),
    "doreche": S(u"до", 36.1), "video": S(u"відео", 36.8),
    "yutubi": S(u"Ютубі", 37.4), "druhyi2": S(u"Другий", 38.2),
    "metodi": S(u"методі", 39.1), "karuselei": S(u"каруселей", 39.9),
    "tobto": S(u"тобто", 40.5), "odyn2": S(u"один", 41.1),
    "tekst": S(u"текст", 41.9), "rozdil": S(u"розділяється", 42.1),
    "tsikavi": S(u"цікаві", 42.9), "slaidy": S(u"слайди", 43.3),
    # D · step 3
    "krok3": S(u"Крок", 44.3), "tretii": S(u"третій", 44.5),
    "koly2": S(u"Коли", 45.1), "karusel1": S(u"карусель", 45.9),
    "vidkryvaiu": S(u"відкриваю", 46.5), "claude2": S("Claude", 47.0),
    "nahovor": S(u"наговорюю", 47.7), "holosom": S(u"голосом", 48.2),
    "vsiu": S(u"всю", 48.6), "inform": S(u"інформацію", 48.8),
    "vyzyvaiu": S(u"визиваю", 49.7), "skil1": S(u"скіл", 50.6),
    "karuseli3": S(u"каруселі", 50.9), "skil2": S(u"скіл", 52.1),
    "styliu": S(u"стилю", 52.4), "obyraiu": S(u"обираю", 53.1),
    "output": S("output", 53.6), "design2": S("design", 54.1),
    "pidtiah": S(u"підтягую", 54.7), "design3": S("design", 55.3),
    "pershoho": S(u"першого", 56.2), "kroku": S(u"кроку", 56.5),
    "i2": S(u"і", 56.9), "proshu2": S(u"прошу", 57.2),
    "zhener": S(u"згенерувати", 57.5), "karusel2": S(u"карусель", 58.0),
    # E · the carousel, Canva
    "v": S(u"в", 59.8), "karusel3": S(u"карусель", 60.3),
    "yakshcho2": S(u"Якщо", 60.7), "shchos": S(u"щось", 61.8),
    "pidpr": S(u"підправити", 62.0), "rukamy": S(u"руками", 62.5),
    "tsi": S(u"ці", 63.3), "odniieiu": S(u"однією", 63.9),
    "knopkoiu": S(u"кнопкою", 64.4), "eksport": S(u"експортуються", 64.9),
    "canva": S("Canva", 65.9),
    # F · RUTA
    "a": S(u"А", 66.3), "naspravdi": S(u"насправді", 66.5),
    "karuseli4": S(u"каруселі", 68.0), "dodatku": S(u"додатку", 69.1),
    "ruta": S("RUTA", 69.6), "odnoho": S(u"одного", 70.5),
    "vykhodiat": S(u"виходять", 71.3), "stsenarii": S(u"сценарії", 71.9),
    "ikaruseli": S(u"каруселі", 73.0), "storiteli": S(u"сторітели", 73.9),
    # G · the system, the DM
    "dlia2": S(u"Для", 74.3), "svoikh": S(u"своїх", 74.6),
    "kliientiv": S(u"клієнтів", 75.0), "korystuius": S(u"користуюсь", 75.3),
    "same": S(u"саме", 75.9), "tsiieiu": S(u"цією", 76.5),
    "i5": S(u"І", 77.6), "tobi": S(u"тобі", 77.9), "tsikavo": S(u"цікаво", 78.9),
    "napyshy": S(u"напиши", 79.6), "slovo": S(u"слово", 80.3),
    "karusel4": S(u"карусель", 80.6),
    "dur": DUR,
}


def js(src, **extra):
    """`@name`, `@name+0.12`, `@name-0.1` -> one literal time. Literals, not
    variables, because tools/review.py reads the timeline off the numbers."""
    vals = dict(T)
    vals.update(extra)

    def rep(m):
        v = vals[m.group(1)] + (float(m.group(2)) if m.group(2) else 0.0)
        return "%.3f" % v
    return re.sub(r"@(\w+)([+-]\d+(?:\.\d+)?)?", rep, src)


def fill(_src, **kw):
    for key, v in kw.items():
        _src = _src.replace("{{%s}}" % key, v if isinstance(v, str) else str(v))
    assert "{{" not in _src, _src[_src.index("{{"):_src.index("{{") + 40]
    return _src


# ---------------------------------------------------------------------------
# Mattes (tools/matte.py via work/r19/mattes.sh). (first frame, frames).
MATTES = {"hook": (51, 202), "slice": (1212, 121)}
for _name, (_f0, _c) in sorted(MATTES.items()):
    k.matte(_name, _f0 / 30.0, _c / 30.0)

# ---------------------------------------------------------------------------
# Glyphs. Monochrome, drawn, never emoji (§5a.11).
SPARK = ("M12 1.6c.8 4.7 2.3 7.5 4.4 8.9 1.5 1 3.6 1.5 6.1 1.5-2.5.1-4.6.6-6.1 1.6-2.1 "
         "1.4-3.6 4.2-4.4 8.8-.8-4.6-2.3-7.4-4.4-8.8C6.1 12.6 4 12.1 1.5 12c2.5-.1 4.6-.6 "
         "6.1-1.5C9.7 9.1 11.2 6.3 12 1.6z")
HEART = ("M12 20.6s-7.6-4.5-9.4-9.3C1.3 7.8 3.5 4.4 7 4.4c2 0 3.7 1.1 5 3 "
         "1.3-1.9 3-3 5-3 3.5 0 5.7 3.4 4.4 6.9-1.8 4.8-9.4 9.3-9.4 9.3z")
EXTRA_DEFS = (
    '<symbol id="i-spark" viewBox="0 0 24 24"><path d="%s"/></symbol>'
    '<symbol id="i-play" viewBox="0 0 24 24"><path d="M8 5.2v13.6l10.8-6.8z"/></symbol>'
    '<linearGradient id="gHeart" x1="0" y1="0" x2="0" y2="1">'
    '<stop offset="0" stop-color="#ff6e9c"/><stop offset="1" stop-color="#c4143a"/></linearGradient>'
    % SPARK)
STROKES = {
    "clock": '<circle cx="12" cy="12" r="8.6"/><path d="M12 7.2v5.1l3.4 2"/>',
    "pencil": '<path d="M4.2 19.8l1-4.3L15.6 5.1a2.1 2.1 0 0 1 3 3L8.3 18.5z"/><path d="M13.7 7l3 3"/>',
    "check": '<path d="M5.4 12.6l4.3 4.3 8.9-9.5"/>',
    "mic": ('<path d="M12 3.4a3 3 0 0 1 3 3v5.2a3 3 0 0 1-6 0V6.4a3 3 0 0 1 3-3z"/>'
            '<path d="M5.6 11.4a6.4 6.4 0 0 0 12.8 0M12 17.8v3"/>'),
    "up": '<path d="M12 19.2V5.4M6.2 11l5.8-5.8 5.8 5.8"/>',
    "image": ('<rect x="3" y="4.5" width="18" height="15" rx="3.2"/>'
              '<path d="M3.6 17.2l5.1-5.3 4 4 2.6-2.6 5.1 4.5"/><circle cx="15.8" cy="9.3" r="1.6"/>'),
    "clip": ('<path d="M19.6 11.2l-7.6 7.6a4.8 4.8 0 0 1-6.8-6.8l8-8a3.2 3.2 0 0 1 4.5 4.5'
             'l-7.9 7.9a1.6 1.6 0 0 1-2.3-2.3l7.2-7.2"/>'),
    "clapper": ('<path d="M3.6 10h16.8v8.4a2 2 0 0 1-2 2H5.6a2 2 0 0 1-2-2z"/>'
                '<path d="M3.6 10l-.5-3.2 16-2.6.5 3.2zM7.6 5.6l1.9 3.6M12.6 4.8l1.9 3.6"/>'),
    "send": '<path d="M20.6 3.4L10.4 13.6M20.6 3.4l-6.4 17.2-3.8-7-7-3.8z"/>',
}


def glyph(name, cls="mk"):
    return '<svg class="%s"><use href="#i-%s" width="100%%" height="100%%"/></svg>' % (cls, name)


def stroke(name, cls="sk"):
    return '<svg class="%s" viewBox="0 0 24 24">%s</svg>' % (cls, STROKES[name])


# the two skills: a speech bubble whose lines draw, and a stack of slides
BUBBLE = ('<svg class="sk" viewBox="0 0 24 24"><path d="M5 4.6h14a2.4 2.4 0 0 1 2.4 2.4v8'
          'a2.4 2.4 0 0 1-2.4 2.4h-7.2L7.2 21v-3.6H5A2.4 2.4 0 0 1 2.6 15V7A2.4 2.4 0 0 1 5 4.6z"/>'
          '<path id="%s1" d="M6.8 9.4h10.4"/><path id="%s2" d="M6.8 13h6.4"/></svg>')
SLIDES = ('<svg class="sk" viewBox="0 0 24 24"><g id="%sa"><rect x="2.6" y="6.4" width="9.6" height="12.4" rx="1.8"/></g>'
          '<g id="%sc"><rect x="11.8" y="6.4" width="9.6" height="12.4" rx="1.8"/></g>'
          '<g id="%sb"><rect x="6.6" y="4.2" width="10.8" height="14.2" rx="2" fill="rgba(255,255,255,0.22)"/>'
          '<path d="M9.2 8.4h5.6M9.2 11.2h3.8"/></g></svg>')


def tile(tid, size, x, y, material, inner, extra_cls="", ring=True, hide=True, after=""):
    """A tile in the glass family: the wrapper takes the motion, the tile the
    material. x, y are its top-left. A ripple ring of the same shape rides
    with it when asked; `after` goes inside the wrapper, over the tile."""
    r = ('<div class="sqring%s" id="%sR" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx"></div>'
         % (" circ" if "circ" in extra_cls else "", tid, x, y, size, size)) if ring else ""
    return ('%s<div class="tw%s %s" id="%s" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx">'
            '<div class="%s">%s<div class="sheen"></div></div>%s</div>'
            % (r, " hide" if hide else "", extra_cls, tid, x, y, size, size, material, inner, after))


def roll_chip(cid, x, y, w, h, vals, font, icon_html, red=()):
    """A pearl pill with an icon and a window whose values roll upward like an
    odometer (reel 13's chip): values are stacked; the roll is a y translate."""
    ic = h - 24
    rl = 12 + ic + 22
    cells = "".join('<i class="%s" style="height:%dpx;line-height:%dpx">%s</i>'
                    % ("red" if i in red else "", h, h, v) for i, v in enumerate(vals))
    return ('<div class="tchip hide" id="%s" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx">'
            '<div class="tci" style="left:12px;width:%dpx;height:%dpx">%s</div>'
            '<div class="roll" data-layout-ignore style="left:%dpx;height:%dpx;width:%dpx">'
            '<div class="rin" id="%sIn" style="font-size:%dpx">%s</div></div>'
            '<div class="sheen"></div></div>'
            % (cid, x, y, w, h, ic, ic, icon_html, rl, h, w - rl - 16, cid, font, cells))


def mini(material, inner):
    """a small round badge inside a chip or a card"""
    return '<div class="%s" style="border-radius:50%%">%s</div>' % (material, inner)


k.css("""
.abs, .cx { position: absolute; }
.hide { opacity: 0; visibility: hidden; }
.tw { position: absolute; }
.sk { fill: none; stroke: url(#gw); stroke-width: 2.3; stroke-linecap: round; stroke-linejoin: round;
  width: 50%; height: 50%; position: relative; z-index: 1; overflow: visible; }
.pearl .sk { stroke: #17141c; }
.circ .jelly, .circ .pearl, .circ .clear, .circ .sheen { border-radius: 50%; }
.sqring.circ { border-radius: 50%; }
.nbt { position: relative; z-index: 1; color: #fff; font-weight: 900; letter-spacing: -0.04em; line-height: 1; }
/* the takeover's three light pools as one element (reel 15) — budget */
.aurs { position: absolute; left: -700px; top: -700px; width: 2480px; height: 3320px; pointer-events: none;
  background:
    radial-gradient(circle 526px at 1560px 880px, rgba(255,110,156,0.50), rgba(255,110,156,0)),
    radial-gradient(circle 634px at 760px 2360px, rgba(222,32,74,0.55), rgba(222,32,74,0)),
    radial-gradient(circle 382px at 1480px 1910px, rgba(255,198,214,0.20), rgba(255,198,214,0)); }
.roomTint { position: absolute; inset: 0;
  background: linear-gradient(180deg, rgba(62,8,24,0.16) 0%, rgba(40,5,15,0.34) 100%); }
/* a real carousel slide, small and moving */
.slc { position: absolute; object-fit: cover; border-radius: 12px;
  box-shadow: 0 0 0 2px rgba(255,255,255,0.55), 0 26px 44px -18px rgba(20,2,8,0.65); }
/* the step number on a step tile */
.nb { position: absolute; left: -12px; top: -12px; width: 48px; height: 48px; border-radius: 50%; z-index: 4;
  background: linear-gradient(165deg, #e0204b 0%, #8d0d24 100%); color: #fff; font-size: 27px; font-weight: 900;
  display: flex; align-items: center; justify-content: center;
  box-shadow: 0 0 0 3px rgba(255,255,255,0.9), 0 8px 16px -6px rgba(70,4,20,0.6); }
/* ---- the odometer chip ---- */
.tchip { position: absolute; border-radius: 999px; overflow: hidden;
  background: linear-gradient(160deg, #ffffff 0%, #fff5f8 52%, #f5dfe6 100%);
  box-shadow: inset 0 2px 1px #fff, inset 0 -14px 24px -12px rgba(180,18,47,0.18),
              0 30px 56px -22px rgba(30,4,12,0.6), 0 3px 8px rgba(30,4,12,0.12); }
.tchip .tci { position: absolute; top: 12px; }
.tchip .tci .sk { width: 56%; height: 56%; }
.tchip .roll { position: absolute; top: 0; overflow: hidden; }
.tchip .rin i { display: block; font-style: normal; font-weight: 700; color: #17141c;
  letter-spacing: -0.02em; white-space: nowrap; }
.tchip .rin i.red { color: #b4122f; }
.tchip .sheen { mix-blend-mode: normal; opacity: 0.6; }
.shc { position: absolute; inset: 0; border-radius: inherit; overflow: hidden; pointer-events: none; }
/* .clear has no overflow clip in glass.py, so its parked sheen showed as a
   white slash beside the tile on dark glass */
.clear { overflow: hidden; }
.shc .sheen { mix-blend-mode: normal; opacity: 0.35; }
""")

# ================================================================== layers ==
# Bottom to top: BEHIND (in her room, under her mattes) -> NEAR (shelves and
# windows above her head) -> TK (the burgundy takeovers) -> TOP (the Canva
# tile, which crosses out of the second takeover onto her footage).
L = {"behind": [], "near": [], "tk": [], "top": []}

# ============================================================== A · hook ==
WALL_SRC = (["tr%02d" % i for i in range(1, 6)] + ["wb%02d" % i for i in range(1, 13)]
            + ["kg%02d" % i for i in (1, 4, 5, 6, 9)])
HUB = (540, 300)
WALL_SHIFT = 360           # how far the feed has scrolled when it is pulled in


def wall_cells():
    rnd = random.Random(19)
    order, last, out = WALL_SRC[:], None, []
    for j in range(-2, 9):
        for i in range(-3, 4):
            x, y = HUB[0] + i * 160, HUB[1] + j * 200
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

SLOP_EXTRA = [   # native 1080-wide coords; they spill past the slide's edges
    ("rocket", -230, 420, 360, -22), ("bubble", 1270, 330, 400, 9),
    ("crown", 540, -110, 330, -8), ("tag", 1280, 1120, 340, 18),
    ("star", -280, 1080, 320, -14), ("orb", 1160, 1500, 300, 0),
]

k.css("""
/* ---- b01-b02 · the soft room, the wall of carousels, the slop ---- */
#roomW, #roomX { position: absolute; inset: 0; }
#wall { position: absolute; inset: 0; transform-origin: 540px 300px; }
.wt { position: absolute; width: 140px; height: 175px; margin: -87px 0 0 -70px; object-fit: cover;
  border-radius: 14px; box-shadow: 0 0 0 1.5px rgba(255,255,255,0.22), 0 20px 34px -14px rgba(12,0,5,0.6); }
.hero { position: absolute; width: 240px; height: 310px; object-fit: cover; border-radius: 18px;
  box-shadow: 0 0 0 2.5px rgba(255,255,255,0.65), 0 40px 70px -26px rgba(10,0,4,0.75); }
.spw { position: absolute; width: 250px; height: 333px; }
""")


def wall_html():
    tiles = "\n          ".join(
        '<img class="wt hide" id="wt%d" src="assets/carousels/%s-s.jpg" style="left:%dpx;top:%dpx" alt="">'
        % (i, c["src"], c["x"], c["y"]) for i, c in enumerate(WALL))
    f0, n = MATTES["hook"]
    return fill(u'''
      <div class="g full" id="gW">
        <div id="roomW" class="hide">
          <video id="softW" class="plate" src="assets/soft/hook.mp4"
                 data-start="{{s}}" data-duration="{{d}}" data-media-start="0" muted playsinline></video>
          <div class="roomTint"></div>
        </div>
        <div id="wall">
          {{tiles}}
        </div>
        <img class="hero hide" id="hr0" src="assets/carousels/wb04-m.jpg" style="left:130px;top:185px" alt="">
        <img class="hero hide" id="hr1" src="assets/carousels/kg04-m.jpg" style="left:710px;top:185px" alt="">
        {{ai}}
        <div class="spw hide" id="sp0" style="left:105px;top:183px">{{s0}}</div>
        <div class="spw hide" id="sp2" style="left:725px;top:183px">{{s2}}</div>
        <div class="spw hide" id="sp1" style="left:415px;top:163px">{{s1}}</div>
      </div>''', s="%.3f" % (f0 / 30.0), d="%.3f" % (n / 30.0), tiles=tiles,
                ai=tile("aiW", 170, HUB[0] - 85, HUB[1] - 85, "jelly", glyph("spark")),
                s0=slop.slide("slA", 250), s1=slop.slide("slB", 250, extra=SLOP_EXTRA),
                s2=slop.slide("slC", 250))


@beat
def b01_wall():
    """«Ти хочеш нарешті почати робити каруселі зі штучним інтелектом, щоб це
    було швидко, гарно і бажано не ай-слоп»

    BEHIND. The room goes soft (a per-beat soft plate built from her matte,
    so she does not halo) and a wall of her real carousels — all three sets,
    mixed and repeated so it reads as a lot — ripples out behind her head on
    «каруселі». The AI tile that makes them lands in the hub on «штучним
    інтелектом»; the feed flies on «швидко»; two good slides come forward on
    «гарно»; the slop slams in between them on «ай-слоп» and gets its
    stickers slapped on."""
    cfg = json.dumps([{"d": c["d"], "o": c["o"]} for c in WALL])
    return js(fill('''
  tl.set("#gW", {autoAlpha: 1}, @karuseli-0.18);
  tl.fromTo("#roomW", {autoAlpha: 0}, {autoAlpha: 1, duration: 0.6, ease: "power1.inOut"}, @karuseli-0.18);
  // «каруселі» — the wall ripples out of the hub
  var WL = {{cfg}};
  WL.forEach(function (w, n) {
    var t = @karuseli + w.d * 0.00048;
    tl.fromTo("#wt" + n, {autoAlpha: 0}, {autoAlpha: w.o, duration: 0.3, ease: "power2.out"}, t);
    tl.fromTo("#wt" + n, {scale: 0.3}, {scale: 1, duration: 0.6, ease: SP, immediateRender: false}, t);
  });
  gsap.set("#wall", {scale: 1.08, y: 0});
  tl.to("#wall", {scale: 1, duration: 1.5, ease: "power2.out"}, @karuseli);
  tl.to("#wall", {y: -60, duration: 1.8, ease: "none"}, @karuseli);
  // «штучним інтелектом» — what makes them
  arr("#aiW", @shtuchnym-0.06, {s: 0.5, y: 30});
  G.inner("#aiW .mk", @shtuchnym-0.06);
  G.ripple("#aiWR", @intelektom+0.1);
  shn("#aiW .sheen", @intelektom+0.2);
  // «швидко» — the feed flies
  tl.to("#wall", {y: -300, duration: 0.7, ease: "power2.inOut"}, @shvydko-0.04);
  tl.to("#wall", {y: -360, duration: 1.9, ease: "none"}, @shvydko+0.66);
  // «гарно» — two good ones come forward
  bin("#hr0", @harno-0.06, 14, 0.36);
  tl.fromTo("#hr0", {scale: 0.45, x: 200, y: 20}, {scale: 1, x: 0, y: 0, duration: 0.85, ease: POP}, @harno-0.06);
  bin("#hr1", @harno+0.04, 14, 0.36);
  tl.fromTo("#hr1", {scale: 0.45, x: -200, y: 20}, {scale: 1, x: 0, y: 0, duration: 0.85, ease: POP}, @harno+0.04);
  // «не ай-слоп» — the slop slams in over the AI tile, stickers and all
  tl.to("#aiW", {scale: 0.8, autoAlpha: 0, duration: 0.25, ease: "power2.in"}, @aislop-0.04);
  tl.set("#sp1", {autoAlpha: 1}, @aislop-0.08);
  tl.fromTo("#sp1", {scale: 1.7, rotation: -8}, {scale: 1, rotation: 0, duration: 0.55, ease: POP}, @aislop-0.08);
  slopPop(tl, "slB", @aislop+0.12, 0.07);
  G.haptic("#sp1", @aislop+0.4);''', cfg=cfg))


@beat
def b02_slop_sags():
    """«Але в тебе досі не виходить»

    The wall and the good slides are pulled into the hub; the slop stays and
    multiplies — two more slide out from behind it. On «не виходить» all
    three sag. Just before «забирає» they sink behind her, and the room comes
    back sharp."""
    cfg = json.dumps([{"d": c["d"], "x": c["x"], "y": c["y"]} for c in WALL])
    return js(fill('''
  tl.set("#gW", {autoAlpha: 1}, @ale);
  var WP = {{cfg}};
  WP.forEach(function (w, n) {
    tl.to("#wt" + n, {x: (540 - w.x) * 0.4, y: (300 + {{shift}} - w.y) * 0.4, scale: 0, autoAlpha: 0,
                      duration: 0.42, ease: "power2.in"}, @ale + ({{maxd}} - w.d) * 0.00022);
  });
  tl.to("#hr0", {x: 290, scale: 0.3, autoAlpha: 0, duration: 0.4, ease: "power2.in"}, @ale);
  tl.to("#hr1", {x: -290, scale: 0.3, autoAlpha: 0, duration: 0.4, ease: "power2.in"}, @ale);
  // that is what you get — three of them
  tl.set(["#sp0", "#sp2"], {autoAlpha: 1}, @ale+0.16);
  tl.fromTo("#sp0", {x: 310, y: -20, scale: 0.8}, {x: 0, y: 0, scale: 1, duration: 0.58, ease: SP}, @ale+0.16);
  tl.fromTo("#sp2", {x: -310, y: -20, scale: 0.8}, {x: 0, y: 0, scale: 1, duration: 0.58, ease: SP}, @ale+0.16);
  // «не виходить» — they sag
  tl.to("#sp0", {rotation: -9, y: 36, duration: 0.5, ease: SOFT}, @vykhodyt);
  tl.to("#sp1", {rotation: 4, y: 22, duration: 0.5, ease: SOFT}, @vykhodyt+0.06);
  tl.to("#sp2", {rotation: 11, y: 44, duration: 0.5, ease: SOFT}, @vykhodyt+0.12);
  // and sink behind her
  tl.to("#sp1", {y: 860, duration: 0.5, ease: "power2.in"}, @zabyraie-0.06);
  tl.to(["#sp0", "#sp2"], {y: 880, duration: 0.46, ease: "power2.in"}, @zabyraie-0.02);
  tl.to(["#sp0", "#sp1", "#sp2"], {autoAlpha: 0, duration: 0.18}, @zabyraie+0.26);
  tl.to("#roomW", {autoAlpha: 0, duration: 0.42, ease: "power1.inOut"}, @zabyraie);
  tl.set("#gW", {autoAlpha: 0}, @zabyraie+0.46);''', cfg=cfg, shift=str(WALL_SHIFT),
                   maxd="%.1f" % WALL_MAXD))


# ---- the time chips (b03-b04) ----
k.css("""
#chA .rin i.pk { color: #b4122f; }
""")


def chips_html():
    return fill(u'''
      <div class="g full" id="gH">
        {{a}}
        {{b}}
      </div>''', a=roll_chip("chA", 330, 210, 420, 110, [u"20 хв", u"1 год", u"3 год", u"5 хв"], 52,
                             mini("jelly", glyph("spark")), red=(2,)),
                b=roll_chip("chB", 330, 350, 420, 110, [u"1 год"], 52, mini("pearl", stroke("pencil"))))


@beat
def b03_time_balloons():
    """«і це забирає часу більше, ніж якщо б ти зробила їх по старінкє?»

    NEAR. The AI's time chip lands and rolls like an odometer on her words —
    20 хв, 1 год, and on «більше» 3 год in burgundy with a haptic shake. On
    «зробила» the by-hand chip lands under it: 1 год."""
    return js('''
  tl.set("#gH", {autoAlpha: 1}, @zabyraie-0.04);
  arr("#chA", @zabyraie-0.04, {s: 0.55, y: -20});
  shn("#chA .sheen", @zabyraie+0.3);
  tl.to("#chAIn", {y: -110, duration: 0.34, ease: SP}, @chasu);
  tl.to("#chAIn", {y: -220, duration: 0.34, ease: SP}, @bilshe);
  G.haptic("#chA", @bilshe+0.24);
  // «ніж якщо б ти зробила їх по старінкє» — by hand, less
  arr("#chB", @zrobyla-0.1, {s: 0.55, y: 30});
  shn("#chB .sheen", @zrobyla+0.3);
  G.bump("#chB", @starinke);''')


# ---- the system shelf (b04, again b08-b09 and b18) ----
ST = [("st1", 150, 285, "pearl", '<span class="wmark" style="font-size:56px">Aa</span>'),
      ("st2", 360, 285, "jelly", glyph("spark")),
      ("st3", 570, 285, "jelly", None)]
CS_SLOTS = [(-62, 12, -9), (0, 0, 0), (62, 12, 9)]
CS_C = (842, 352)

k.css("""
#shelf { left: 70px; top: 180px; width: 940px; height: 340px; }
#cabS { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; overflow: visible; }
.csl { position: absolute; width: 150px; height: 190px; margin: -95px 0 0 -75px; }
""")


def cable(cid, d):
    return ('<path class="tube" id="%sT" d="%s"/><path class="core" id="%sC" d="%s"/>'
            '<g class="pkg"><path class="pkt hide" id="%sP" d="%s"/></g>' % (cid, d, cid, d, cid, d))


C12 = "M 283 350 C 305 376 338 376 357 350"
C23 = "M 493 350 C 515 376 548 376 567 350"


def step_tiles():
    out = []
    for i, (tid, x, y, mat, inner) in enumerate(ST):
        inner = inner or g.mark("claude")
        out.append(tile(tid, 130, x, y, mat, '<div class="gi" style="position:relative;z-index:1;'
                        'display:flex;align-items:center;justify-content:center;width:100%%;height:100%%">%s</div>'
                        % inner, after='<div class="nb">%d</div>' % (i + 1)))
    return "\n        ".join(out)


# ---- step 2 on the same shelf ----
k.css("""
/* ---- b08-b09 · two skills on the shelf ---- */
.tag { position: absolute; top: 424px; width: 150px; height: 46px; border-radius: 23px;
  background: rgba(20,6,12,0.34); box-shadow: inset 0 1px 1px rgba(255,255,255,0.35), inset 0 0 0 1.5px rgba(255,255,255,0.22);
  color: #fff; font-size: 22px; font-weight: 700; letter-spacing: 0.16em; line-height: 46px; text-align: center; }
.okb { position: absolute; width: 50px; height: 50px; }
.okb .sk { width: 62%; height: 62%; stroke-width: 3; }
#skR { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; overflow: visible; }
#skR circle { fill: none; stroke-width: 7; stroke-linecap: round; }
#skR .trk { stroke: rgba(255,255,255,0.22); }
#skR .prg { stroke: #ff8ab0; }
/* the YouTube card */
#yt { left: 300px; top: 196px; width: 700px; height: 300px; border-radius: 48px; }
#ytTh { left: 22px; top: 40px; width: 400px; height: 220px; border-radius: 22px; overflow: hidden;
  box-shadow: 0 0 0 1.5px rgba(255,255,255,0.3), 0 20px 40px -16px rgba(0,0,0,0.6); }
#ytTh img { width: 100%; height: 100%; object-fit: cover; display: block; }
#ytMk { left: 446px; top: 40px; width: 70px; height: 70px; }
#ytTi { left: 446px; top: 126px; width: 232px; font-size: 25px; font-weight: 700; line-height: 32px; letter-spacing: -0.01em; }
#ytMe { left: 446px; top: 232px; font-size: 21px; font-weight: 500; color: rgba(255,255,255,0.6); }
""")


def shelf_html():
    sk1 = tile("sk1", 170, 270, 225, "jelly", BUBBLE % ("bub", "bub"))
    sk2 = tile("sk2", 170, 640, 225, "jelly", SLIDES % ("s2", "s2", "s2"))
    ok1 = tile("ok1", 50, 416, 212, "pearl", stroke("check"), "circ okb", ring=False)
    ok2 = tile("ok2", 50, 786, 212, "pearl", stroke("check"), "circ okb", ring=False)
    return fill(u'''
      <div class="g full" id="gS">
        <div id="shelf" class="shelf edge hide"></div>
        <svg id="cabS" class="cab" viewBox="0 0 1080 1920">{{c12}}{{c23}}</svg>
        {{tiles}}
        <img class="slc csl hide" id="cs0" src="assets/carousels/wb06-s.jpg" style="left:780px;top:364px" alt="">
        <img class="slc csl hide" id="cs1" src="assets/carousels/wb04-s.jpg" style="left:842px;top:352px" alt="">
        <img class="slc csl hide" id="cs2" src="assets/carousels/kg05-s.jpg" style="left:904px;top:364px" alt="">
        <img class="slc csl hide" id="ct0" src="assets/carousels/tr01-s.jpg" style="left:780px;top:364px" alt="">
        <img class="slc csl hide" id="ct1" src="assets/carousels/tr04-s.jpg" style="left:842px;top:352px" alt="">
        <img class="slc csl hide" id="ct2" src="assets/carousels/tr05-s.jpg" style="left:904px;top:364px" alt="">
        {{bd2}}
        <svg id="skR" viewBox="0 0 1080 1920">
          <circle class="trk hide" id="rg1t" cx="355" cy="310" r="104"/>
          <circle class="trk hide" id="rg2t" cx="725" cy="310" r="104"/>
          <circle class="prg hide" id="rg1p" cx="355" cy="310" r="104" transform="rotate(-90 355 310)"/>
          <circle class="prg hide" id="rg2p" cx="725" cy="310" r="104" transform="rotate(-90 725 310)"/>
        </svg>
        {{sk1}}
        {{sk2}}
        {{ok1}}
        {{ok2}}
        <div class="tag hide" id="tg1" style="left:280px">SKILL</div>
        <div class="tag hide" id="tg2" style="left:650px">SKILL</div>
        <div class="dglass edge abs hide" id="yt">
          <div class="cx" id="ytTh"><img src="assets/her/yt-thumb.jpg" alt=""></div>
          {{ytmk}}
          <div class="cx" id="ytTi">Як прибрати «пластиковий» стиль в ШІ</div>
          <div class="cx" id="ytMe">Рута · 14:38</div>
          <div class="shc"><div class="sheen"></div></div>
        </div>
      </div>''', c12=cable("c12", C12), c23=cable("c23", C23), tiles=step_tiles(),
                bd2=tile("bd2", 96, 492, 66, "jelly", '<span class="nbt" style="font-size:58px">2</span>',
                         "circ", ring=False),
                sk1=sk1, sk2=sk2, ok1=ok1, ok2=ok2,
                ytmk=tile("ytMk", 70, 446, 40, "clear edge", g.mark("youtube"), hide=False))


@beat
def b04_system():
    """«Якщо це про тебе, то зараз я покажу, як я налаштувала свою систему, яка
    робить мені каруселі реально за 5 хвилин.»

    The by-hand chip goes, the AI chip rises to the top. A glass shelf lands
    on «покажу»; on «свою систему» three step tiles land on it and wire
    together — 1 the design system («Aa»), 2 the skills, 3 Claude. On
    «каруселі» a finished carousel deals out of step 3; on «5» the time chip
    rolls down from 3 год to 5 хв (BLACKOUT «5 хвилин», plaque kept). All of it
    clears by 17.38 for her coffee-sip insert."""
    slots = json.dumps([{"x": x, "y": y, "r": r} for x, y, r in CS_SLOTS])
    return js(fill('''
  tl.set("#gH", {autoAlpha: 1}, @yakshcho);
  bout("#chB", @yakshcho, 10, 0.3);
  tl.to("#chA", {y: -128, scale: 0.78, duration: 0.7, ease: SP}, @yakshcho+0.04);
  tl.set("#gS", {autoAlpha: 1}, @pokazhu-0.06);
  bin("#shelf", @pokazhu-0.06, 14, 0.45);
  tl.fromTo("#shelf", {scale: 0.9, y: 36}, {scale: 1, y: 0, duration: 0.95, ease: SP}, @pokazhu-0.06);
  // «свою систему» — three steps, wired
  ["#st1", "#st2", "#st3"].forEach(function (s, i) {
    arr(s, @svoiu-0.04 + i * 0.16, {s: 0.5, y: 30});
    G.inner(s + " .gi", @svoiu-0.04 + i * 0.16);
  });
  G.draw("c12T", @systemu+0.12, 0.3); G.draw("c12C", @systemu+0.12, 0.3);
  G.draw("c23T", @systemu+0.3, 0.3); G.draw("c23C", @systemu+0.3, 0.3);
  G.packet("c12P", @systemu+0.5, 0.3);
  G.packet("c23P", @systemu+0.78, 0.3);
  G.bump("#st3", @systemu+1.06);
  // «каруселі» — a finished carousel deals out of step 3
  var CS = {{slots}};
  [1, 0, 2].forEach(function (i, n) {
    var s = CS[i], t = @karuseli2-0.08 + n * 0.09;
    tl.set("#cs" + i, {autoAlpha: 1}, t);
    tl.fromTo("#cs" + i, {x: {{fx}} - s.x, y: -s.y, scale: 0.3, rotation: 0},
              {x: 0, y: 0, scale: 1, rotation: s.r, duration: 0.8, ease: POP}, t);
  });
  G.bump("#cs1", @realno);
  // «за 5 хвилин» — the chip rolls all the way down
  tl.to("#chAIn", {y: -330, duration: 0.45, ease: SP}, @za-0.02);
  G.haptic("#chA", @five+0.3);
  shn("#chA .sheen", @five+0.2);
  // clear before her coffee-sip insert at 17.40 (NO_PAINT)
  bout(["#chA", "#st1", "#st2", "#st3", "#c12T", "#c12C", "#c23T", "#c23C", "#cs0", "#cs1", "#cs2"], @five+0.42, 10, 0.2);
  tl.to("#shelf", {scale: 1.15, duration: 0.22, ease: "power2.in"}, @five+0.42);
  bout("#shelf", @five+0.42, 14, 0.2);
  tl.set(["#gH", "#gS"], {autoAlpha: 0}, @five+0.64);''', slots=slots, fx=str(635 - 842)))


# ============================================================ B · step 1 ==
SW = [("#0A0A0A", "#0a0a0a"), ("#FF78BF", "#ff78bf"), ("#FFFFFF", "#ffffff"), ("#F2F2F2", "#f2f2f2")]
WF = [  # wireframes: (photo zone x, y, w, h, from dx, dy, photo), bars
    ((0, 0, 144, 78, -34, 26, "tr01"), [(12, 92, 96, 14, "p"), (12, 116, 112, 8, "w"), (12, 130, 80, 8, "w")]),
    ((70, 94, 62, 74, 34, -30, "tr03"), [(12, 14, 104, 14, "p"), (12, 38, 120, 8, "w"), (12, 52, 88, 8, "w")]),
    ((0, 0, 64, 180, 30, 20, "tr02"), [(76, 22, 56, 12, "p"), (76, 44, 56, 7, "w"), (76, 57, 40, 7, "w")]),
    ((12, 100, 120, 66, -28, 30, "tr05"), [(12, 16, 112, 16, "p"), (12, 44, 98, 8, "w"), (12, 58, 70, 8, "w")]),
]

k.css("""
/* ---- b05-b07 · over her: Claude builds the Design System ---- */
#tk1, #tk2 { position: absolute; inset: 0; }
#tk1 { clip-path: circle(0px at 540px 142px); }
#tk2 { clip-path: circle(0px at 540px 560px); }
#dsW { left: 100px; top: 250px; width: 880px; height: 960px; transform-origin: 102px 96px; }
#ds { position: absolute; inset: 0; }
#dsTi { left: 168px; top: 54px; }
#dsSb { left: 168px; top: 108px; }
#dsOk { right: 56px; top: 64px; }
#dsOk .sk { width: 30px; height: 30px; stroke: #b4122f; stroke-width: 3; }
#dsHr { left: 60px; right: 60px; top: 172px; }
.dsL { position: absolute; left: 60px; color: rgba(23,20,28,0.58); }
.dsG { position: absolute; left: 60px; height: 30px; border-radius: 15px; background: rgba(23,20,28,0.06);
  transform-origin: 0 50%; }
#tyAa { left: 50px; top: 226px; font-size: 150px; }
#ty1 { left: 330px; top: 240px; font-size: 56px; font-weight: 900; letter-spacing: -0.03em; }
#ty2 { left: 330px; top: 314px; font-size: 32px; font-weight: 700; color: rgba(23,20,28,0.82); }
#ty3 { left: 330px; top: 364px; font-size: 24px; font-weight: 400; color: rgba(23,20,28,0.5); }
.swc { position: absolute; top: 474px; width: 104px; height: 104px; border-radius: 50%;
  box-shadow: inset 0 2px 1px rgba(255,255,255,0.5), 0 0 0 1.5px rgba(23,20,28,0.10), 0 18px 30px -14px rgba(30,4,12,0.45); }
.swh { position: absolute; top: 592px; width: 130px; margin-left: -13px; text-align: center; font-size: 21px;
  font-weight: 700; letter-spacing: 0.04em; color: rgba(23,20,28,0.64); }
.wfr { position: absolute; top: 664px; width: 144px; height: 180px; border-radius: 14px; overflow: hidden;
  background: linear-gradient(170deg, #1a1519 0%, #0d0b0e 100%);
  box-shadow: 0 0 0 1.5px rgba(23,20,28,0.1), 0 18px 30px -14px rgba(30,4,12,0.5); }
.wfr i { position: absolute; display: block; border-radius: 3px; }
.wfr i.p { background: #ff78bf; border-radius: 4px; }
.wfr i.w { background: rgba(255,255,255,0.75); }
.wph { position: absolute; border: 2.5px dashed #ff78bf; border-radius: 6px; background: rgba(255,120,191,0.12);
  display: flex; align-items: center; justify-content: center; overflow: hidden; }
.wph .sk { width: 30px; height: 30px; stroke: #ff78bf; stroke-width: 1.8; }
.wph img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }
#dsHr2 { left: 60px; right: 60px; top: 862px; }
#lkH { left: 60px; top: 882px; width: 56px; height: 56px; }
#lkH svg { position: absolute; inset: 0; width: 56px; height: 56px; }
#lkH .o { fill: none; stroke: rgba(23,20,28,0.55); stroke-width: 1.8; }
#lkH .fl { fill: url(#gHeart); }
#lkT { left: 140px; top: 902px; width: 520px; height: 16px; border-radius: 8px; background: #f4dfe5; overflow: hidden; }
#lkF { position: absolute; left: 0; top: 0; width: 520px; height: 16px; border-radius: 8px; transform-origin: 0 50%;
  transform: scaleX(0); background: linear-gradient(90deg, #8d0d24 0%, #e0204b 60%, #ff6e9c 100%); }
#lkK { left: 118px; top: 888px; width: 44px; height: 44px; }
#lkKi { position: absolute; inset: 0; border-radius: 50%;
  background: linear-gradient(160deg, #ffffff 0%, #f5dfe6 100%);
  box-shadow: inset 0 2px 1px #fff, 0 0 0 1.5px rgba(23,20,28,0.08), 0 10px 20px -8px rgba(30,4,12,0.5); }
#lkV { right: 60px; top: 878px; font-size: 52px; font-weight: 900; letter-spacing: -0.03em; color: #b4122f; }
#lkR { left: 60px; top: 882px; width: 56px; height: 56px; border-radius: 50%; border: 3px solid rgba(255,110,156,0.9); }
""")


def wireframes():
    out = []
    for i, ((px, py, pw, ph, _dx, _dy, src), bars) in enumerate(WF):
        b = "".join('<i class="%s" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx"></i>' % (c, x, y, w, h)
                    for x, y, w, h, c in bars)
        out.append('<div class="wfr hide" style="left:%dpx">%s<div class="wph" id="wph%d" '
                   'style="left:%dpx;top:%dpx;width:%dpx;height:%dpx">%s'
                   '<img class="wpi hide" src="assets/carousels/%s-s.jpg" alt=""></div></div>'
                   % (60 + i * 164, b, i, px, py, pw, ph, stroke("image"), src))
    return "".join(out)


def tk1_html():
    sw = "".join('<i class="swc hide" style="left:%dpx;background:%s"></i>'
                 '<div class="swh hide" style="left:%dpx">%s</div>' % (60 + i * 150, c, 60 + i * 150, h)
                 for i, (h, c) in enumerate(SW))
    return fill(u'''
      <div class="g full" id="gT1">
        <div id="tk1">
          <div class="tkg"></div><div class="aurs"></div><div class="grain"></div>
          {{bd1}}
          <div id="dsW" class="abs hide"><div id="ds" class="sheet">
            <div class="cx t-title hide" id="dsTi">Design System</div>
            <div class="cx t-sub hide" id="dsSb">Каруселі · Рута</div>
            <div class="cx chip hide" id="dsOk"><svg class="sk" viewBox="0 0 24 24"><path id="dsOkP" d="M5.4 12.6l4.3 4.3 8.9-9.5"/></svg><span>Збережено</span></div>
            <div class="cx hair" id="dsHr"></div>
            <div class="dsL t-micro hide" style="top:196px">TYPOGRAPHY</div>
            <div class="dsL t-micro hide" style="top:436px">COLOR</div>
            <div class="dsL t-micro hide" style="top:628px">IMAGERY</div>
            <div class="dsG hide" id="dsG0" style="top:250px;width:560px"></div>
            <div class="dsG hide" id="dsG1" style="top:496px;width:440px"></div>
            <div class="dsG hide" id="dsG2" style="top:700px;width:620px"></div>
            <div class="cx t-big hide" id="tyAa">Aa</div>
            <div class="cx hide" id="ty1">Заголовок</div>
            <div class="cx hide" id="ty2">Підзаголовок</div>
            <div class="cx hide" id="ty3">Основний текст слайда · 24</div>
            {{sw}}
            {{wf}}
            <div class="cx hair hide" id="dsHr2"></div>
            <div class="cx hide" id="lkH"><svg viewBox="0 0 24 24"><path class="o" d="{{heart}}"/></svg>
              <svg viewBox="0 0 24 24" id="lkHf"><path class="fl" d="{{heart}}"/></svg></div>
            <div class="cx hide" id="lkR"></div>
            <div class="cx hide" id="lkT"><div id="lkF"></div></div>
            <div class="cx hide" id="lkK"><div id="lkKi"></div></div>
            <div class="cx hide" id="lkV">0%</div>
            <div class="sheen" id="dsSh"></div>
          </div></div>
          {{cl1}}
        </div>
      </div>''', bd1=tile("bd1", 104, 488, 90, "jelly", '<span class="nbt" style="font-size:62px">1</span>',
                          "circ", ring=False),
                sw=sw, wf=wireframes(), heart=HEART,
                cl1=tile("cl1", 200, 440, 460, "jelly", g.mark("claude")))


@beat
def b05_step1_claude():
    """«Крок перший. Заходжу в Claude, прошу створити Design System,»

    OVER. After her coffee-sip insert, the iris opens out of a «1» onto burgundy.
    «Заходжу в Claude» — the Claude jelly lands, bumps on «Claude»; «прошу створити» — it works (bump,
    ripple); «Design System» — the white sheet grows out of it and Claude
    becomes its header icon. BLACKOUT «Design System» (the header says it)."""
    return js('''
  tl.set("#gT1", {autoAlpha: 1}, @krok1-0.04);
  G.irisOpen("#tk1", @krok1-0.04, 540, 142, 0.85);
  drift1("#tk1", @krok1-0.04, 15);
  arr("#bd1", @krok1+0.1, {s: 0.4, y: 0});
  G.inner("#bd1 .nbt", @krok1+0.1);
  G.bump("#bd1", @pershyi+0.1);
  // «Заходжу в Claude»
  arr("#cl1", @zakhodzhu-0.06, {s: 0.5, y: 40, d: 0.6});
  G.inner("#cl1 .mk", @zakhodzhu-0.06);
  G.bump("#cl1", @claude1);
  shn("#cl1 .sheen", @claude1+0.1);
  G.ripple("#cl1R", @claude1+0.04);
  // «прошу створити» — it works on it
  G.bump("#cl1", @proshu);
  tl.fromTo("#cl1R", {scale: 1, autoAlpha: 0.7}, {scale: 1.75, autoAlpha: 0, duration: 0.8, ease: "power2.out", immediateRender: false}, @stvoryty);
  // «Design System» — the sheet grows out of Claude; Claude becomes its icon
  tl.to("#cl1", {x: -338, y: -214, scale: 0.42, duration: 0.8, ease: SP}, @design1-0.14);
  bin("#dsW", @design1-0.12, 16, 0.4);
  tl.fromTo("#dsW", {scale: 0.2}, {scale: 1, duration: 1.0, ease: spring(0.72, 12)}, @design1-0.12);
  tl.fromTo(["#dsTi", "#dsSb"], {autoAlpha: 0, y: 14}, {autoAlpha: 1, y: 0, duration: 0.55, ease: SP, stagger: 0.08}, @design1);
  tl.fromTo("#dsHr", {scaleX: 0}, {scaleX: 1, duration: 0.7, ease: "power3.out"}, @design1+0.3);''')


@beat
def b06_step1_style():
    """«і до деталей продумую весь стиль: шрифти, кольори, як розміщуються
    картинки. Це робиться один раз,»

    Three sections open empty on «до деталей» (labelled, with grey ghost
    bars); each fills on its word: the type specimen on «шрифти», four
    swatches from her carousels on «кольори», four slide wireframes on «як»
    whose photo zones slide into place on «розміщуються» and fill with real
    photos on «картинки». «один раз» — Збережено, ticked."""
    wph = json.dumps([[dx, dy] for (_x, _y, _w, _h, dx, dy, _s), _b in WF])
    return js(fill('''
  tl.set("#gT1", {autoAlpha: 1}, @i1);
  // «до деталей продумую весь стиль» — the sections open, still empty
  tl.fromTo(".dsL", {autoAlpha: 0, y: 10}, {autoAlpha: 1, y: 0, duration: 0.45, ease: SP, stagger: 0.12}, @detalei);
  tl.fromTo(".dsG", {autoAlpha: 0, scaleX: 0.3}, {autoAlpha: 1, scaleX: 1, duration: 0.5, ease: "power3.out", stagger: 0.12}, @detalei+0.1);
  shn("#dsSh", @produmuiu);
  // «шрифти»
  tl.to("#dsG0", {autoAlpha: 0, duration: 0.2}, @shryfty-0.06);
  arr("#tyAa", @shryfty-0.06, {s: 0.5, y: 20});
  tl.fromTo(["#ty1", "#ty2", "#ty3"], {autoAlpha: 0, x: -20}, {autoAlpha: 1, x: 0, duration: 0.5, ease: SP, stagger: 0.09}, @shryfty+0.12);
  // «кольори»
  tl.to("#dsG1", {autoAlpha: 0, duration: 0.2}, @kolory-0.06);
  tl.fromTo(".swc", {autoAlpha: 0, scale: 0.3}, {autoAlpha: 1, scale: 1, duration: 0.55, ease: POP, stagger: 0.08}, @kolory-0.05);
  tl.fromTo(".swh", {autoAlpha: 0, y: 8}, {autoAlpha: 1, y: 0, duration: 0.4, ease: SP, stagger: 0.08}, @kolory+0.16);
  // «як розміщуються картинки»
  tl.to("#dsG2", {autoAlpha: 0, duration: 0.2}, @yak-0.06);
  tl.fromTo(".wfr", {autoAlpha: 0, y: 20}, {autoAlpha: 1, y: 0, duration: 0.5, ease: SP, stagger: 0.07}, @yak-0.05);
  var WPH = {{wph}};
  WPH.forEach(function (d, i) {
    tl.fromTo("#wph" + i, {x: d[0], y: d[1]}, {x: 0, y: 0, duration: 0.55, ease: POP}, @rozmisch + i * 0.1);
  });
  tl.fromTo(".wpi", {autoAlpha: 0}, {autoAlpha: 1, duration: 0.3, stagger: 0.08}, @kartynky);
  // «Це робиться один раз» — saved
  arr("#dsOk", @odyn-0.06, {s: 0.5, y: 0});
  G.draw("dsOkP", @odyn+0.08, 0.3);
  shn("#dsSh", @raz+0.05);''', wph=wph))


@beat
def b07_step1_hundred():
    """«але треба довести до стану, коли тобі все на 100% подобається.»

    A liking meter under the sheet: it climbs on «треба», «довести», «коли»
    and lands on 100 % on «100%» (BLACKOUT, plaque kept); the heart fills on
    «подобається». On «Крок другий» the sheet shrinks away upward — it comes
    back in step 3 — and the iris closes onto the step-2 shelf."""
    return js('''
  tl.set("#gT1", {autoAlpha: 1}, @ale2);
  tl.fromTo("#dsHr2", {autoAlpha: 0, scaleX: 0}, {autoAlpha: 1, scaleX: 1, duration: 0.6, ease: "power3.out"}, @ale2);
  tl.fromTo(["#lkH", "#lkT", "#lkK", "#lkV"], {autoAlpha: 0, y: 12}, {autoAlpha: 1, y: 0, duration: 0.45, ease: SP, stagger: 0.06}, @ale2+0.04);
  gsap.set("#lkHf", {scale: 0, autoAlpha: 0, transformOrigin: "50% 60%"});
  // the meter itself is driven by the clock (paintAll): 35 on «треба», 62 on
  // «довести», 80 on «коли»
  G.bump("#lkV", @dovesty+0.3);
  // «100%»
  G.bump("#lkV", @sto+0.1);
  // «подобається» — the heart
  tl.to("#lkHf", {scale: 1, autoAlpha: 1, duration: 0.55, ease: POP}, @podob);
  tl.fromTo("#lkR", {scale: 1, autoAlpha: 0.9}, {scale: 2.2, autoAlpha: 0, duration: 0.7, ease: "power2.out", immediateRender: false}, @podob);
  G.haptic("#dsW", @podob+0.3);
  shn("#dsSh", @podob+0.2);
  // «Крок другий» — the sheet folds up and away; the iris closes onto the shelf
  tl.to("#dsW", {scale: 0.14, y: -330, duration: 0.5, ease: "power3.in"}, @krok2-0.12);
  tl.to("#cl1", {x: -150, y: -560, scale: 0.12, duration: 0.5, ease: "power3.in"}, @krok2-0.12);
  bout(["#dsW", "#cl1"], @krok2+0.14, 12, 0.24);
  bout("#bd1", @krok2-0.1, 10, 0.3);
  G.irisClose("#tk1", @krok2, 540, 118, 0.6);
  tl.set("#gT1", {autoAlpha: 0}, @krok2+0.64);''')


# ============================================================ C · step 2 ==
@beat
def b08_skills():
    """«Крок другий. Треную два скіли. Перший — на моєму стилі мовлення, до
    речі в мене є відео про це на Ютубі.»

    NEAR. A «2» and the shelf; two skill tiles land on «Треную» — a speech
    bubble and a stack of slides — and train (progress rings fill), tagged
    SKILL on «скіли» (BLACKOUT, plaque kept), ticked. «Перший» lifts; its
    bubble speaks on «стилі мовлення». «відео про це на Ютубі» — her real
    YouTube video slides out of it as a glass card."""
    return js('''
  tl.set("#gS", {autoAlpha: 1}, @krok2+0.1);
  bin("#shelf", @krok2+0.1, 14, 0.45);
  tl.fromTo("#shelf", {scale: 0.9, y: 36}, {scale: 1, y: 0, duration: 0.9, ease: SP, immediateRender: false}, @krok2+0.1);
  arr("#bd2", @druhyi-0.02, {s: 0.4, y: 0});
  G.inner("#bd2 .nbt", @druhyi-0.02);
  // «Треную два скіли» — two skills, training
  arr("#sk1", @treniu-0.06, {s: 0.5, y: 30});
  G.inner("#sk1 .sk", @treniu-0.06);
  arr("#sk2", @treniu+0.1, {s: 0.5, y: 30});
  G.inner("#sk2 .sk", @treniu+0.1);
  tl.set(["#rg1t", "#rg2t", "#rg1p", "#rg2p"], {autoAlpha: 1}, @treniu+0.24);
  G.draw("rg1p", @treniu+0.26, 1.2);
  G.draw("rg2p", @treniu+0.36, 1.2);
  tl.fromTo(["#tg1", "#tg2"], {autoAlpha: 0, y: 10}, {autoAlpha: 1, y: 0, duration: 0.45, ease: SP, stagger: 0.08}, @skily-0.04);
  arr("#ok1", @skily+0.24, {s: 0.3, y: 0});
  G.inner("#ok1 .sk", @skily+0.24);
  arr("#ok2", @skily+0.34, {s: 0.3, y: 0});
  G.inner("#ok2 .sk", @skily+0.34);
  tl.to(["#rg1t", "#rg2t", "#rg1p", "#rg2p"], {autoAlpha: 0, duration: 0.3}, @pershyi2-0.12);
  // «Перший — на моєму стилі мовлення»
  G.bump("#sk1", @pershyi2);
  G.ripple("#sk1R", @pershyi2+0.05);
  tl.to(["#sk2", "#tg2", "#ok2"], {autoAlpha: 0.4, duration: 0.4}, @pershyi2);
  G.draw("bub1", @styli-0.02, 0.35);
  G.draw("bub2", @styli+0.16, 0.3);
  G.bump("#sk1", @movlennia);
  // «до речі у мене є відео про це на Ютубі»
  tl.to(["#sk2", "#tg2", "#ok2"], {autoAlpha: 0, duration: 0.3}, @doreche);
  tl.to(["#sk1", "#sk1R", "#tg1", "#ok1"], {x: -170, duration: 0.6, ease: SP}, @doreche);
  arr("#yt", @video-0.12, {s: 0.55, x: -240, y: 0});
  tl.fromTo(["#ytTh", "#ytMk", "#ytTi", "#ytMe"], {autoAlpha: 0, y: 10}, {autoAlpha: 1, y: 0, duration: 0.45, ease: SP, stagger: 0.06}, @video);
  // «Ютубі»
  G.bump("#ytMk", @yutubi);
  G.ripple("#ytMkR", @yutubi+0.04);
  shn("#yt .sheen", @yutubi+0.1);''')


@beat
def b09_method():
    """«Другий — на моєму методі створення каруселей,»

    The card folds back into skill 1, which dims; skill 2 lifts and its
    slides fan on «методі створення каруселей». On «тобто» the shelf's frost
    spreads into the room (b10)."""
    return js('''
  tl.set("#gS", {autoAlpha: 1}, @druhyi2-0.1);
  tl.to("#yt", {x: -330, scale: 0.3, autoAlpha: 0, duration: 0.42, ease: "power2.in"}, @druhyi2-0.1);
  tl.to(["#sk1", "#sk1R", "#tg1", "#ok1"], {x: 0, duration: 0.6, ease: SP}, @druhyi2);
  tl.to(["#sk1", "#tg1", "#ok1"], {autoAlpha: 0.4, duration: 0.4}, @druhyi2);
  tl.to(["#sk2", "#tg2", "#ok2"], {autoAlpha: 1, duration: 0.35}, @druhyi2);
  G.bump("#sk2", @druhyi2+0.12);
  G.ripple("#sk2R", @druhyi2+0.16);
  // «методі створення каруселей» — its slides fan
  gsap.set(["#s2a", "#s2c"], {transformOrigin: "50% 100%"});
  tl.to("#s2a", {rotation: -16, x: -1.5, duration: 0.6, ease: POP}, @metodi);
  tl.to("#s2c", {rotation: 16, x: 1.5, duration: 0.6, ease: POP}, @metodi+0.08);
  G.bump("#sk2", @karuselei);
  // «тобто» — out, and the shelf's frost spreads into the room
  bout(["#bd2", "#sk1", "#sk2", "#tg1", "#tg2", "#ok1", "#ok2"], @tobto-0.1, 10, 0.3);
  tl.to("#shelf", {scale: 1.35, duration: 0.55, ease: "power2.in"}, @tobto-0.04);
  bout("#shelf", @tobto+0.06, 16, 0.42);
  tl.set("#gS", {autoAlpha: 0}, @tobto+0.5);''')


# one long text: her webinar carousel's copy, which becomes slides 02-06
STRIPS = [
    (188, u'<b class="hd">Знайомо?</b>Ти робиш блонд щодня, але дохід стоїть на місці. '
          u'Більше клієнток, довші дні — а чек той самий.'),
    (178, u'Ти працюєш за звичними формулами, і кожна складна робота — лотерея. '
          u'Виправляєш чужі помилки за ціною звичайного фарбування.'),
    (136, u'<b>Дорогий блонд — це система, а не техніка.</b> І цю систему тобі ніхто не пояснив.'),
    (178, u'За дві години ефіру: з чого складається дорогий блонд, чому дешевий результат '
          u'коштує тобі клієнток і як зберегти якість волосся.'),
    (136, u'І головне — скільки має коштувати твоя година. Вебінар 8 жовтня о 19:00.'),
]
DOC = (90, 120, 900)
XS = [(124, 348, -7), (332, 336, -3.5), (540, 330, 0), (748, 336, 3.5), (956, 348, 7)]
XS_W, XS_H = 196, 261


def strip_cfg():
    out, top = [], 0
    for i, (h, _t) in enumerate(STRIPS):
        cy = DOC[1] + top + h / 2.0
        sx, sy, r = XS[i]
        out.append({"top": top, "h": h, "dx": round(sx - 540, 1), "dy": round(sy - cy, 1), "r": r})
        top += h
    return out


SCFG = strip_cfg()

k.css("""
/* ---- b10 · behind her: one long text, cut into slides ---- */
#doc { left: 90px; top: 120px; width: 900px; }
.strip { position: absolute; left: 0; width: 900px; padding: 26px 44px; background: #fffdfd;
  font-size: 30px; font-weight: 400; line-height: 42px; color: rgba(23,20,28,0.8);
  box-shadow: 0 40px 80px -30px rgba(10,0,4,0.55); }
.strip b { font-weight: 700; color: #17141c; }
.strip b.hd { display: block; font-size: 44px; font-weight: 900; line-height: 52px; color: #d81b6a; letter-spacing: -0.02em; }
.strip:first-child { border-radius: 30px 30px 0 0; }
.strip:last-child { border-radius: 0 0 30px 30px; }
.cut { position: absolute; left: -20px; width: 940px; height: 0; border-top: 4px dashed #ff4f9a;
  transform-origin: 0 50%; }
.xs { position: absolute; width: 196px; height: 261px; margin: -130px 0 0 -98px; object-fit: cover; border-radius: 16px;
  box-shadow: 0 0 0 2.5px rgba(255,255,255,0.6), 0 40px 70px -26px rgba(10,0,4,0.75); }
""")


def slice_html():
    strips = "".join('<div class="strip" id="str%d" style="top:%dpx;height:%dpx">%s</div>'
                     % (i, c["top"], c["h"], STRIPS[i][1]) for i, c in enumerate(SCFG))
    cuts = "".join('<i class="cut hide" id="cut%d" style="top:%dpx"></i>' % (i, SCFG[i + 1]["top"] - 2)
                   for i in range(len(SCFG) - 1))
    slides = "".join('<img class="xs hide" id="xs%d" src="assets/carousels/wb%02d-m.jpg" style="left:%dpx;top:%dpx" alt="">'
                     % (i, i + 2, x, y) for i, (x, y, _r) in enumerate(XS))
    f0, n = MATTES["slice"]
    return fill(u'''
      <div class="g full" id="gX">
        <div id="roomX" class="hide">
          <video id="softX" class="plate" src="assets/soft/slice.mp4"
                 data-start="{{s}}" data-duration="{{d}}" data-media-start="0" muted playsinline></video>
          <div class="roomTint"></div>
        </div>
        <div id="doc" class="abs hide" style="height:{{h}}px">{{strips}}{{cuts}}</div>
        {{slides}}
      </div>''', s="%.3f" % (f0 / 30.0), d="%.3f" % (n / 30.0), strips=strips, cuts=cuts,
                slides=slides, h=str(sum(c["h"] for c in SCFG)))


@beat
def b10_slice():
    """«тобто як один великий текст розділяється на цікаві слайди»

    BEHIND. The room goes soft; one long text — the copy of her webinar
    carousel — rises behind her on «один великий текст». «розділяється»:
    dashed cuts draw along its paragraphs and the strips part. «на цікаві
    слайди»: each strip flies to a slot above her head and lands as the real
    slide it became (blond-webinar 02-06). Pulled up and out before «Крок
    третій»."""
    return js(fill('''
  tl.set("#gX", {autoAlpha: 1}, @tobto-0.08);
  tl.fromTo("#roomX", {autoAlpha: 0}, {autoAlpha: 1, duration: 0.55, ease: "power1.inOut"}, @tobto-0.08);
  // «один великий текст» — it rises behind her
  bin("#doc", @odyn2-0.1, 14, 0.4);
  tl.fromTo("#doc", {y: 700, scale: 0.94}, {y: 0, scale: 1, duration: 0.9, ease: SP}, @odyn2-0.1);
  // «розділяється» — cut along its paragraphs, and the strips part
  tl.fromTo(".cut", {scaleX: 0, autoAlpha: 1}, {scaleX: 1, duration: 0.3, ease: "power2.out", stagger: 0.07,
            immediateRender: false}, @rozdil-0.04);
  var SC = {{cfg}};
  SC.forEach(function (s, i) { tl.to("#str" + i, {y: (i - 2) * 26, duration: 0.45, ease: SP}, @rozdil+0.3); });
  tl.to(".cut", {autoAlpha: 0, duration: 0.2}, @rozdil+0.36);
  // «на цікаві слайди» — each strip becomes a slide
  SC.forEach(function (s, i) {
    var t = @tsikavi-0.08 + i * 0.09;
    tl.to("#str" + i, {x: s.dx, y: s.dy, scale: 0.24, autoAlpha: 0, duration: 0.4, ease: "power2.in"}, t);
    tl.set("#xs" + i, {autoAlpha: 1}, t + 0.2);
    tl.fromTo("#xs" + i, {x: -s.dx * 0.2, y: 60, scale: 0.5, rotation: 0},
              {x: 0, y: 0, scale: 1, rotation: s.r, duration: 0.8, ease: POP}, t + 0.2);
  });
  // «слайди» — a riffle
  SC.forEach(function (s, i) {
    tl.to("#xs" + i, {rotation: s.r * 1.6, duration: 0.16, ease: "power2.out"}, @slaidy+0.1 + i * 0.03);
    tl.to("#xs" + i, {rotation: s.r, duration: 0.5, ease: SP}, @slaidy+0.26 + i * 0.03);
  });
  // before «Крок третій» — pulled up and out; the room comes back
  tl.to(".xs", {y: -560, autoAlpha: 0, duration: 0.3, ease: "power2.in", stagger: 0.02}, @krok3-0.26);
  tl.to("#roomX", {autoAlpha: 0, duration: 0.3}, @krok3-0.2);
  tl.set("#gX", {autoAlpha: 0}, @krok3+0.12);''', cfg=json.dumps(SCFG)))


# ============================================================ D · step 3 ==
WAVE = []
_rnd = random.Random(7)
for _i in range(34):
    WAVE.append([round(0.2 + _rnd.random() * 0.8, 2) for _ in range(7)] + [0.15])

k.css("""
/* ---- b11-b14 · near: one Claude chat does it all ---- */
#tm { left: 470px; top: 58px; width: 250px; height: 90px; }
#tmV { position: absolute; left: 94px; top: 0; height: 90px; line-height: 90px; font-size: 46px; font-weight: 700;
  color: #17141c; letter-spacing: -0.02em; }
#cw { left: 70px; top: 176px; width: 940px; height: 368px; border-radius: 56px; }
#cwTi { left: 108px; top: 30px; font-size: 34px; font-weight: 700; color: #fff; letter-spacing: -0.01em; }
#cwSt { right: 36px; top: 40px; font-size: 22px; font-weight: 500; color: rgba(255,255,255,0.62); }
#cwIn { left: 30px; top: 100px; width: 880px; height: 150px; border-radius: 34px;
  background: linear-gradient(170deg, #ffffff 0%, #fff8fa 100%);
  box-shadow: inset 0 2px 1px #fff, 0 22px 44px -22px rgba(20,2,8,0.55); }
#cwPh { left: 28px; top: 22px; font-size: 26px; font-weight: 500; color: rgba(23,20,28,0.36); }
#cwWv { left: 28px; top: 14px; width: 600px; height: 64px; display: flex; align-items: center; gap: 9px; }
#cwWv i { display: block; width: 8px; height: 60px; border-radius: 4px; background: linear-gradient(180deg, #ff6e9c, #b4122f);
  transform: scaleY(0.15); }
.txl { position: absolute; left: 28px; width: 720px; font-size: 23px; font-weight: 500; line-height: 30px;
  color: rgba(23,20,28,0.72); white-space: nowrap; }
.sch { position: absolute; top: 92px; height: 44px; border-radius: 22px; padding: 0 18px 0 8px; display: flex;
  align-items: center; gap: 8px; color: #fff; font-size: 23px; font-weight: 700; white-space: nowrap;
  background: linear-gradient(165deg, #e0204b 0%, #ab112e 46%, #6b081c 100%);
  box-shadow: inset 0 2px 1px rgba(255,255,255,0.5), 0 10px 20px -8px rgba(70,4,20,0.6); }
.sch .sk { width: 30px; height: 30px; }
.rbt { position: absolute; top: 45px; width: 60px; height: 60px; }
.rbt .pearl .sk { width: 56%; height: 56%; }
#seg { left: 30px; top: 270px; width: 404px; height: 70px; border-radius: 35px;
  background: rgba(20,6,12,0.32); box-shadow: inset 0 1px 1px rgba(255,255,255,0.3), inset 0 0 0 1.5px rgba(255,255,255,0.16); }
#segL { left: 24px; top: 25px; font-size: 19px; font-weight: 700; letter-spacing: 0.14em; color: rgba(255,255,255,0.62); }
#segK { left: 130px; top: 7px; width: 128px; height: 56px; border-radius: 28px;
  background: linear-gradient(160deg, #ffffff 0%, #f5dfe6 100%); box-shadow: inset 0 2px 1px #fff, 0 8px 16px -8px rgba(20,2,8,0.6); }
.sgt { position: absolute; top: 7px; width: 128px; height: 56px; line-height: 56px; text-align: center;
  font-size: 25px; font-weight: 700; }
#segA { left: 130px; color: #17141c; }
#segB { left: 262px; color: #ffffff; }
#att { left: 452px; top: 270px; width: 458px; height: 70px; border-radius: 35px;
  border: 2.5px dashed rgba(255,255,255,0.45); }
#attE { left: 22px; top: 12px; height: 42px; display: flex; align-items: center; gap: 10px; font-size: 22px;
  font-weight: 600; color: rgba(255,255,255,0.6); }
#attE .sk { width: 34px; height: 34px; stroke: rgba(255,255,255,0.7); }
#dsc { left: -2px; top: -2px; width: 458px; height: 70px; border-radius: 35px;
  background: linear-gradient(160deg, #ffffff 0%, #fff5f8 52%, #f5dfe6 100%);
  box-shadow: inset 0 2px 1px #fff, 0 16px 30px -14px rgba(20,2,8,0.6); }
#dscT { left: 14px; top: 9px; width: 42px; height: 52px; border-radius: 8px; background: #fff;
  box-shadow: 0 0 0 1.5px rgba(23,20,28,0.12); overflow: hidden; }
#dscT i { position: absolute; left: 6px; display: block; height: 5px; border-radius: 3px; }
#dscL { left: 70px; top: 0; height: 70px; line-height: 70px; font-size: 25px; font-weight: 700; color: #17141c; }
#dscN { right: 12px; top: 11px; width: 48px; height: 48px; }
""")


def step3_html():
    wave = "".join("<i class=\"wvb\"></i>" for _ in WAVE)
    return fill(u'''
      <div class="g full" id="gC">
        {{bd3}}
        {{tm}}
        <div class="shelf edge abs hide" id="cw">
          {{cwic}}
          <div class="cx hide" id="cwTi">Claude</div>
          <div class="cx hide" id="cwSt">новий чат</div>
          <div class="cx hide" id="cwIn">
            <div class="cx" id="cwPh">Чим допомогти?</div>
            <div class="cx hide" id="cwWv">{{wave}}</div>
            <div class="txl hide" id="cwTx1" style="top:16px">Вебінар «Прибутковий блонд», 8 жовтня о 19:00, для колористів —</div>
            <div class="txl hide" id="cwTx2" style="top:46px">як піднять чек без нових клієнток, дорогий блонд як система…</div>
            <div class="sch hide" id="sc1" style="left:28px">{{g2}}<span>/каруселі</span></div>
            <div class="sch hide" id="sc2" style="left:242px">{{g1}}<span>/стиль</span></div>
            {{mic}}
            {{send}}
          </div>
          <div class="cx hide" id="seg">
            <div class="cx" id="segL">OUTPUT</div>
            <div class="cx" id="segK"></div>
            <div class="sgt" id="segA">Text</div>
            <div class="sgt" id="segB">Design</div>
          </div>
          <div class="cx hide" id="att">
            <div class="cx" id="attE">{{clip}}<span>файл</span></div>
            <div class="cx hide" id="dsc">
              <div class="cx" id="dscT"><i style="top:8px;width:22px;background:#ff78bf"></i>
                <i style="top:18px;width:30px;background:rgba(23,20,28,0.25)"></i>
                <i style="top:27px;width:24px;background:rgba(23,20,28,0.25)"></i>
                <i style="top:38px;width:14px;height:8px;background:#0a0a0a"></i>
                <i style="top:38px;left:22px;width:14px;height:8px;background:#ff78bf"></i></div>
              <div class="cx" id="dscL">Design System</div>
              {{dscn}}
            </div>
          </div>
          <div class="shc"><div class="sheen" id="cwSh"></div></div>
        </div>
      </div>''',
                bd3=tile("bd3", 90, 360, 58, "jelly", '<span class="nbt" style="font-size:54px">3</span>',
                         "circ", ring=False),
                tm=('<div class="tchip hide" id="tm"><div class="tci" style="left:12px;width:66px;height:66px">%s</div>'
                    '<div id="tmV">5:00</div><div class="sheen"></div></div>' % mini("jelly", stroke("clock"))),
                cwic=tile("cwIc", 60, 30, 24, "jelly", g.mark("claude")),
                wave=wave, g1=BUBBLE % ("cb", "cb"), g2=SLIDES % ("c2", "c2", "c2"),
                mic=tile("cwMic", 60, 720, 45, "pearl", stroke("mic"), "circ rbt", ring=True, hide=False,
                         after='<div class="jelly hide" id="cwMicF" style="border-radius:50%%">%s</div>' % stroke("mic")),
                send=tile("cwSend", 60, 796, 45, "pearl", stroke("up"), "circ rbt", ring=True, hide=False,
                          after='<div class="jelly hide" id="cwSendF" style="border-radius:50%%">%s</div>' % stroke("up")),
                clip=stroke("clip"),
                dscn=tile("dscN", 48, 398, 11, "jelly", '<span class="nbt" style="font-size:28px">1</span>',
                          "circ", ring=False, hide=False))


@beat
def b11_claude_voice():
    """«Крок третій. Коли треба зробити карусель, я відкриваю Claude,
    наговорюю голосом всю інформацію,»

    NEAR. A «3», and the clock: 5:00, running from «карусель» (it reads
    down through the whole step). «відкриваю Claude» — the chat window
    arrives. «наговорюю голосом» — the mic goes live and her voice runs as a
    waveform in the prompt; «всю інформацію» — it lands as text (the
    webinar's brief, which is the carousel the fan will show)."""
    return js(fill('''
  tl.set("#gC", {autoAlpha: 1}, @krok3-0.04);
  arr("#bd3", @krok3-0.04, {s: 0.4, y: 0});
  G.inner("#bd3 .nbt", @krok3-0.04);
  G.bump("#bd3", @tretii+0.1);
  // «Коли треба зробити карусель» — five minutes on the clock
  arr("#tm", @koly2-0.06, {s: 0.55, x: -40, y: 0});
  shn("#tm .sheen", @koly2+0.3);
  G.bump("#tm", @karusel1);
  // «відкриваю Claude»
  arr("#cw", @vidkryvaiu-0.08, {s: 0.72, y: 40, d: 0.9});
  tl.fromTo(["#cwIn", "#cwSt"], {autoAlpha: 0, y: 16}, {autoAlpha: 1, y: 0, duration: 0.55, ease: SP, stagger: 0.06}, @vidkryvaiu+0.1);
  arr("#cwIc", @claude2-0.08, {s: 0.4, y: 0});
  G.inner("#cwIc .mk", @claude2-0.08);
  tl.fromTo("#cwTi", {autoAlpha: 0, x: -12}, {autoAlpha: 1, x: 0, duration: 0.5, ease: SP}, @claude2+0.02);
  G.ripple("#cwIcR", @claude2+0.1);
  // «наговорюю голосом» — the mic goes live, her voice as a waveform
  tl.to("#cwMicF", {autoAlpha: 1, duration: 0.2}, @nahovor-0.06);
  G.ripple("#cwMicR", @nahovor);
  tl.set("#cwPh", {autoAlpha: 0}, @nahovor);
  tl.set("#cwWv", {autoAlpha: 1}, @nahovor);
  var WV = {{wave}};
  document.querySelectorAll(".wvb").forEach(function (b, i) {
    tl.to(b, {keyframes: {scaleY: WV[i]}, duration: 1.0, ease: "none"}, @nahovor+0.04 + (i % 5) * 0.01);
  });
  tl.fromTo("#cwMicR", {scale: 1, autoAlpha: 0.7}, {scale: 1.75, autoAlpha: 0, duration: 0.8, ease: "power2.out", immediateRender: false}, @holosom+0.1);
  // «всю інформацію» — it lands as text
  tl.to("#cwWv", {autoAlpha: 0, duration: 0.2}, @vsiu);
  tl.set(["#cwTx1", "#cwTx2"], {autoAlpha: 1}, @vsiu+0.08);
  tl.fromTo("#cwTx1", {clipPath: "inset(0px 100% 0px 0px)"}, {clipPath: "inset(0px 0% 0px 0px)", duration: 0.45, ease: "power1.inOut", immediateRender: false}, @vsiu+0.08);
  tl.fromTo("#cwTx2", {clipPath: "inset(0px 100% 0px 0px)"}, {clipPath: "inset(0px 0% 0px 0px)", duration: 0.45, ease: "power1.inOut", immediateRender: false}, @inform+0.26);
  tl.to("#cwMicF", {autoAlpha: 0, duration: 0.25}, @inform+0.6);''', wave=json.dumps(WAVE)))


@beat
def b12_skills_in():
    """«визиваю спочатку скіл каруселі, потім скіл стилю,»

    The two skills from step 2 drop into the prompt as slash chips, one on
    each «скіл»: /каруселі, then /стиль. BLACKOUT both phrases — the chips
    say them (plaque kept)."""
    return js('''
  tl.set("#gC", {autoAlpha: 1}, @vyzyvaiu);
  tl.to(["#cwTx1", "#cwTx2"], {y: -6, duration: 0.4, ease: SP}, @vyzyvaiu);
  G.bump("#cwIn", @vyzyvaiu+0.1);
  // «скіл каруселі»
  tl.set("#sc1", {autoAlpha: 1}, @skil1-0.1);
  tl.fromTo("#sc1", {x: 160, y: -330, scale: 1.8, rotation: -10}, {x: 0, y: 0, scale: 1, rotation: 0, duration: 0.7, ease: SP}, @skil1-0.1);
  G.bump("#cwIn", @karuseli3+0.12);
  // «скіл стилю»
  tl.set("#sc2", {autoAlpha: 1}, @skil2-0.1);
  tl.fromTo("#sc2", {x: 300, y: -330, scale: 1.8, rotation: 10}, {x: 0, y: 0, scale: 1, rotation: 0, duration: 0.7, ease: SP}, @skil2-0.1);
  G.bump("#cwIn", @styliu+0.12);''')


@beat
def b13_output_design():
    """«обираю output — design, підтягую свою design system з першого кроку»

    The Output switch arrives on «обираю» and clicks from Text to Design on
    «design». On «підтягую» an attachment slot opens and the Design System
    sheet from step 1 drops into it as a file, with its «1» on «першого
    кроку». BLACKOUT «output design» and «design system» (plaque kept)."""
    return js('''
  tl.set("#gC", {autoAlpha: 1}, @obyraiu);
  arr("#seg", @obyraiu-0.06, {s: 0.6, y: 20});
  G.bump("#segL", @output);
  // «design» — click
  tl.to("#segK", {x: 132, duration: 0.45, ease: SP}, @design2-0.08);
  tl.to("#segA", {color: "#ffffff", duration: 0.2}, @design2-0.02);
  tl.to("#segB", {color: "#17141c", duration: 0.2}, @design2);
  G.bump("#seg", @design2+0.2);
  // «підтягую свою design system» — the sheet from step 1, pulled in as a file
  arr("#att", @pidtiah-0.08, {s: 0.7, y: 20});
  tl.set("#dsc", {autoAlpha: 1}, @design3-0.3);
  tl.fromTo("#dsc", {x: -120, y: -440, scale: 2.4, rotation: -8}, {x: 0, y: 0, scale: 1, rotation: 0, duration: 0.75, ease: SP}, @design3-0.3);
  tl.to("#attE", {autoAlpha: 0, duration: 0.2}, @design3);
  // «з першого кроку» — its step
  G.bump("#dscN", @pershoho);
  G.bump("#dsc", @kroku);''')


@beat
def b14_generate():
    """«і прошу згенерувати карусель.»

    Send is pressed on «згенерувати»; on «карусель» Claude works — a sheen
    through the window, a ripple off its icon. Everything is gone by 58.70:
    her gag starts at 58.75."""
    return js('''
  tl.set("#gC", {autoAlpha: 1}, @i2);
  tl.to("#cwSendF", {autoAlpha: 1, duration: 0.2}, @proshu2);
  tl.to("#cwSend", {scale: 0.84, duration: 0.08, ease: "power2.out"}, @zhener);
  tl.to("#cwSend", {scale: 1, duration: 0.4, ease: POP}, @zhener+0.08);
  G.ripple("#cwSendR", @zhener+0.06);
  // «карусель» — Claude works on it
  shn("#cwSh", @karusel2-0.1);
  G.bump("#cwIc", @karusel2);
  tl.fromTo("#cwIcR", {scale: 1, autoAlpha: 0.7}, {scale: 1.75, autoAlpha: 0, duration: 0.8, ease: "power2.out", immediateRender: false}, @karusel2+0.02);
  // clear for her gag
  bout(["#cw", "#tm", "#bd3"], @karusel2+0.34, 10, 0.3);
  tl.set("#gC", {autoAlpha: 0}, @karusel2+0.68);''')


# ====================================================== E · the carousel ==
FAN_R, FAN_C = 1000, (540, 500)
FAN = []
for _i in range(12):
    _a = -33 + 6 * _i
    _r = math.radians(_a)
    FAN.append({"x": round(FAN_R * math.sin(_r), 1), "y": round(FAN_R * (1 - math.cos(_r)), 1), "r": _a})
FAN_ORDER = [0, 11, 1, 10, 2, 9, 3, 8, 4, 7, 5, 6]      # outside in: the middle on top
LIFT = 3                                                 # wb04 «дорогий блонд» is edited by hand
CANVA_C = (540, 320)

k.css("""
/* ---- b15-b16 · over her: the carousel, fanned; Export to Canva ---- */
#tm2 { left: 390px; top: 70px; width: 300px; height: 100px; }
#tm2V { position: absolute; left: 104px; top: 0; height: 100px; line-height: 100px; font-size: 54px; font-weight: 900;
  color: #b4122f; letter-spacing: -0.03em; }
.fanc { position: absolute; left: 422px; top: 343px; width: 236px; height: 315px; object-fit: cover;
  border-radius: 18px; box-shadow: 0 0 0 2.5px rgba(255,255,255,0.6), 0 50px 90px -30px rgba(10,0,4,0.75); }
#sel { left: 386px; top: 418px; width: 312px; height: 127px; border: 3px solid #ff6e9c; border-radius: 4px;
  box-shadow: 0 0 0 1px rgba(255,255,255,0.4); }
#sel, #cur { z-index: 10; }
#sel i { position: absolute; width: 16px; height: 16px; background: #fff; border: 3px solid #ff6e9c; border-radius: 4px; }
#cur { left: 0; top: 0; width: 64px; height: 64px; }
#cur svg { width: 64px; height: 64px; filter: drop-shadow(0 6px 10px rgba(0,0,0,0.45)); }
#exb { left: 250px; top: 900px; width: 580px; height: 120px; border-radius: 60px;
  background: linear-gradient(160deg, #ffffff 0%, #fff5f8 52%, #f5dfe6 100%);
  box-shadow: inset 0 2px 1px #fff, inset 0 -16px 28px -14px rgba(180,18,47,0.2), 0 40px 70px -26px rgba(8,0,3,0.8); }
#exbI { left: 16px; top: 16px; width: 88px; height: 88px; }
#exbT { left: 126px; top: 0; height: 120px; line-height: 120px; font-size: 42px; font-weight: 700; color: #17141c;
  letter-spacing: -0.015em; white-space: nowrap; }
#exbR { left: 250px; top: 900px; width: 580px; height: 120px; border-radius: 60px; border: 3px solid rgba(255,255,255,0.8); }
""")

CURSOR = ('<svg viewBox="0 0 24 24"><path d="M5.5 2.8v16.9l4.3-4.1 2.8 6.3 3-1.3-2.8-6.2h6z" '
          'fill="#fff" stroke="#17141c" stroke-width="1.3" stroke-linejoin="round"/></svg>')


def tk2_html():
    fan = "".join('<img class="fanc hide" id="fn%d" src="assets/carousels/wb%02d-m.jpg" alt="">' % (i, i + 1)
                  for i in FAN_ORDER)
    return fill(u'''
      <div class="g full" id="gT2">
        <div id="tk2">
          <div class="tkg"></div><div class="aurs"></div><div class="grain"></div>
          <div class="tchip hide" id="tm2"><div class="tci" style="left:12px;width:76px;height:76px">{{ok}}</div>
            <div id="tm2V">0:00</div><div class="sheen"></div></div>
          {{fan}}
          <div class="abs hide" id="sel"><i style="left:-10px;top:-10px"></i><i style="right:-10px;top:-10px"></i>
            <i style="left:-10px;bottom:-10px"></i><i style="right:-10px;bottom:-10px"></i></div>
          <div class="abs hide" id="exbR"></div>
          <div class="abs hide" id="exb">
            <div class="cx" id="exbI">{{cv}}</div>
            <div class="cx" id="exbT">Export to Canva</div>
            <div class="shc"><div class="sheen"></div></div>
          </div>
          <div class="abs hide" id="cur">{{cursor}}</div>
        </div>
      </div>''', ok=mini("jelly", stroke("check")), fan=fan,
                cv=mini("jelly", g.mark("canva")), cursor=CURSOR)


@beat
def b15_fan():
    """«в тебе є карусель.»

    OVER, the moment her gag ends: the iris opens on burgundy, the clock is
    back reading 0:00 (haptic), and her twelve-slide webinar carousel pops in
    as a stack and fans out on «карусель» — two bounces, her «бадабім,
    бадабум» played back in motion. The fan bleeds off both edges."""
    return js(fill('''
  tl.set("#gT2", {autoAlpha: 1}, @v-0.06);
  G.irisOpen("#tk2", @v-0.06, 540, 560, 0.7);
  drift1("#tk2", @v-0.06, 7);
  arr("#tm2", @v-0.02, {s: 0.5, y: -20});
  G.haptic("#tm2", @karusel3+0.1);
  shn("#tm2 .sheen", @karusel3+0.2);
  var FN = {{fan}};
  // a stack first (bounce one)
  FN.forEach(function (s, i) {
    tl.set("#fn" + i, {autoAlpha: 1}, @v+0.04);
    tl.fromTo("#fn" + i, {scale: 0.35, rotation: (i % 3 - 1) * 3, x: 0, y: 40},
              {scale: 1, rotation: (i % 3 - 1) * 3, x: 0, y: 0, duration: 0.5, ease: POP}, @v+0.04);
  });
  // «карусель» — it fans out (bounce two)
  FN.forEach(function (s, i) {
    tl.to("#fn" + i, {x: s.x, y: s.y, rotation: s.r, duration: 0.85, ease: SP}, @karusel3-0.1 + Math.abs(i - 5.5) * 0.015);
  });
  tl.to(".fanc", {scale: 1.05, duration: 0.12, ease: "power2.out"}, @karusel3+0.3);
  tl.to(".fanc", {scale: 1, duration: 0.45, ease: SP}, @karusel3+0.42);''', fan=json.dumps(FAN)))


@beat
def b16_export_canva():
    """«Якщо дуже хочеться щось підправити руками, ці слайди однією кнопкою
    експортуються в Canva.»

    One slide (wb04) lifts out of the fan; «щось підправити» — a cursor and a
    selection box on its headline, dragged by a handle on «руками». «ці
    слайди» — it goes back. «однією кнопкою» — Export to Canva lands and is
    pressed on «кнопкою»; «експортуються» — the slides pour up into a Canva
    tile (b17). BLACKOUT «експортуються в Canva» — the button and the tile
    say it (plaque kept)."""
    s = FAN[LIFT]
    return js(fill('''
  tl.set("#gT2", {autoAlpha: 1}, @yakshcho2);
  // «щось підправити руками» — one slide out, edited by hand
  tl.set("#fn{{i}}", {zIndex: 5}, @yakshcho2);
  tl.to("#fn{{i}}", {x: 0, y: 60, rotation: 0, scale: 1.55, duration: 0.7, ease: SP}, @yakshcho2);
  tl.to(".fanc:not(#fn{{i}})", {autoAlpha: 0.45, duration: 0.4}, @yakshcho2);
  tl.set("#cur", {autoAlpha: 1}, @shchos-0.3);
  tl.fromTo("#cur", {x: 900, y: 1120}, {x: 690, y: 530, duration: 0.5, ease: "power2.out"}, @shchos-0.3);
  bin("#sel", @shchos, 6, 0.2);
  tl.fromTo("#sel", {scale: 0.96}, {scale: 1, duration: 0.3, ease: SP}, @shchos);
  // «підправити» — drag the corner handle
  tl.to("#cur", {x: 740, y: 560, duration: 0.5, ease: "power2.inOut"}, @pidpr+0.1);
  tl.to("#sel", {scaleX: 1.12, scaleY: 1.1, transformOrigin: "0% 0%", duration: 0.5, ease: "power2.inOut"}, @pidpr+0.1);
  // (G.bump would reset the lift's 1.55 scale to 1)
  tl.to("#fn{{i}}", {scale: 1.61, duration: 0.1, ease: "power2.out"}, @rukamy+0.1);
  tl.to("#fn{{i}}", {scale: 1.55, duration: 0.45, ease: SP}, @rukamy+0.2);
  // «ці слайди» — back into the fan
  bout("#sel", @tsi-0.1, 6, 0.2);
  tl.to("#fn{{i}}", {x: {{x}}, y: {{y}}, rotation: {{r}}, scale: 1, duration: 0.6, ease: SP}, @tsi-0.04);
  tl.to(".fanc", {autoAlpha: 1, duration: 0.3}, @tsi);
  tl.set("#fn{{i}}", {zIndex: 0}, @tsi+0.6);
  // «однією кнопкою» — Export to Canva, pressed
  arr("#exb", @odniieiu-0.06, {s: 0.6, y: 40});
  G.inner("#exbI .mk", @odniieiu+0.04);
  tl.to("#cur", {x: 700, y: 980, duration: 0.45, ease: "power2.inOut"}, @odniieiu+0.05);
  tl.to("#exb", {scale: 0.93, duration: 0.08, ease: "power2.out"}, @knopkoiu);
  tl.to("#exb", {scale: 1, duration: 0.45, ease: POP}, @knopkoiu+0.08);
  tl.fromTo("#exbR", {scale: 1, autoAlpha: 0.9}, {scale: 1.25, autoAlpha: 0, duration: 0.6, ease: "power2.out", immediateRender: false}, @knopkoiu+0.06);
  shn("#exb .sheen", @knopkoiu+0.1);
  // «експортуються» — the slides pour up into Canva
  tl.to("#cur", {autoAlpha: 0, duration: 0.2}, @eksport-0.1);
  var FN = {{fan}};
  FN.forEach(function (s, i) {
    tl.to("#fn" + i, {x: 0, y: {{cy}} - 500, rotation: 0, scale: 0.16, autoAlpha: 0, duration: 0.45, ease: "power2.in"},
          @eksport + Math.abs(i - 5.5) * 0.045);
  });
  bout("#exb", @eksport+0.1, 10, 0.3);''', i=str(LIFT), x=str(s["x"]), y=str(s["y"]), r=str(s["r"]),
                   fan=json.dumps(FAN), cy=str(CANVA_C[1])))


# ============================================================== F · RUTA ==
k.css("""
/* ---- b17 · Canva flips into RUTA: one voice note, three outputs ---- */
#cvW { left: 440px; top: 220px; width: 200px; height: 200px; perspective: 1100px; }
#cvF { position: absolute; inset: 0; transform-style: preserve-3d; }
#cvF .face { position: absolute; inset: 0; backface-visibility: hidden; -webkit-backface-visibility: hidden; }
#cvF .face.back { transform: rotateY(180deg); }
#cvR { left: 440px; top: 220px; width: 200px; height: 200px; }
#vn { left: 330px; top: 272px; width: 420px; height: 104px; border-radius: 52px; }
#vnP { left: 14px; top: 14px; width: 76px; height: 76px; }
#vnP .mk { width: 44%; height: 44%; margin-left: 6%; }
#vnW { left: 108px; top: 22px; width: 210px; height: 60px; display: flex; align-items: center; gap: 7px; }
#vnW i { display: block; width: 7px; border-radius: 4px; background: rgba(255,255,255,0.85); }
#vnT { right: 30px; top: 0; height: 104px; line-height: 104px; font-size: 26px; font-weight: 700; color: rgba(255,255,255,0.75); }
#oS { left: 80px; top: 272px; width: 250px; height: 270px; border-radius: 34px; }
#oSI { left: 18px; top: 18px; width: 54px; height: 54px; }
#oSI .sk { width: 58%; height: 58%; }
#oSH { left: 86px; top: 30px; font-size: 22px; font-weight: 700; letter-spacing: 0.12em; color: rgba(23,20,28,0.42); }
.osr { position: absolute; left: 20px; height: 26px; display: flex; align-items: center; gap: 12px; }
.osr b { font-size: 20px; font-weight: 700; color: #b4122f; width: 46px; }
.osr i { display: block; height: 11px; border-radius: 6px; background: rgba(23,20,28,0.14); }
.oc { position: absolute; width: 150px; height: 188px; margin: -94px 0 0 -75px; }
.stf { position: absolute; top: 290px; width: 136px; height: 242px; border-radius: 18px; overflow: hidden; background: #111;
  box-shadow: 0 0 0 2px rgba(255,255,255,0.55), 0 26px 44px -18px rgba(20,2,8,0.65); }
.stf img.bg { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }
.stp { position: absolute; left: 8px; right: 8px; top: 8px; height: 4px; display: flex; gap: 4px; }
.stp i { flex: 1; display: block; border-radius: 2px; background: rgba(255,255,255,0.45); }
.stp i:first-child { background: #fff; }
.sta { position: absolute; left: 10px; top: 20px; width: 28px; height: 28px; border-radius: 50%;
  background: url("assets/her/avatar.jpg") center / cover no-repeat; box-shadow: 0 0 0 2px #fff; }
""")

VN_BARS = [18, 34, 52, 26, 44, 60, 30, 48, 22, 40, 56, 28, 36, 20, 46, 32, 24, 38]
OC_SLOTS = [(445, 418, -8), (540, 406, 0), (635, 418, 8)]


def ruta_html():
    rows = "".join('<div class="osr" style="top:%dpx"><b>%s</b><i style="width:%dpx"></i></div>'
                   % (y, tc, w) for y, tc, w in [(92, "0:00", 150), (132, "0:03", 118), (172, "0:15", 160),
                                                  (212, "0:38", 96)])
    oc = "".join('<img class="slc oc hide" id="oc%d" src="assets/carousels/kg%02d-s.jpg" style="left:%dpx;top:%dpx" alt="">'
                 % (i, 4 + i, x, y) for i, (x, y, _r) in enumerate(OC_SLOTS))
    stories = "".join('<div class="stf hide" id="of%d" style="left:%dpx"><img class="bg" src="assets/carousels/%s-s.jpg" alt="">'
                      '<div class="stp"><i></i><i></i><i></i></div><div class="sta"></div></div>'
                      % (i, x, src) for i, (x, src) in enumerate([(770, "tr02"), (860, "tr03")]))
    return fill(u'''
      <div class="g full" id="gR">
        <div class="sqring" id="cvR"></div>
        <div class="tw hide" id="cvW"><div id="cvF">
          <div class="face front"><div class="pearl">{{canva}}<div class="sheen"></div></div></div>
          <div class="face back"><div class="jelly">{{ruta}}<div class="sheen"></div></div></div>
        </div></div>
        <div class="dglass edge abs hide" id="vn">
          <div class="cx" id="vnP">{{play}}</div>
          <div class="cx" id="vnW">{{bars}}</div>
          <div class="cx" id="vnT">0:42</div>
        </div>
        <div class="sheet abs hide" id="oS">
          <div class="cx" id="oSI">{{clap}}</div>
          <div class="cx" id="oSH">0:42</div>
          {{rows}}
        </div>
        {{oc}}
        {{stories}}
      </div>''', canva=g.mark("canva"), ruta=Glass.wordmark("RUTA", size=58),
                play=mini("jelly", glyph("play")),
                bars="".join('<i style="height:%dpx"></i>' % h for h in VN_BARS),
                clap=mini("jelly", stroke("clapper")), rows=rows, oc=oc, stories=stories)


@beat
def b17_canva_to_ruta():
    """«…в Canva. А насправді сама я зараз роблю каруселі у своєму додатку
    RUTA, бо там з одного голосового виходять і сценарії для рілсів, і
    каруселі, і сторітели.»

    The Canva tile catches the pour (b16) and bumps on «Canva»; the iris
    closes onto it and it stays over her room. «А насправді» — it shakes
    its head. «у своєму додатку» — it flips (FLIP), and lands on RUTA (a
    wordmark tile, her app has no icon) on «RUTA» (BLACKOUT, plaque kept).
    «з одного голосового» — one voice note, sucked into RUTA on «виходять»;
    out come a reel script on «сценарії», her carousel on «каруселі», and
    stories on «сторітели»."""
    slots = json.dumps([{"x": x, "y": y, "r": r} for x, y, r in OC_SLOTS])
    return js(fill('''
  tl.set("#gR", {autoAlpha: 1}, @eksport-0.08);
  arr("#cvW", @eksport-0.08, {s: 0.5, y: 30});
  G.inner("#cvW .front .mk", @eksport);
  G.bump("#cvF", @eksport+0.4);
  // «Canva»
  G.bump("#cvF", @canva);
  G.ripple("#cvR", @canva);
  shn("#cvW .front .sheen", @canva+0.05);
  G.irisClose("#tk2", @a, {{cx}}, {{cy}}, 0.6);
  tl.set("#gT2", {autoAlpha: 0}, @a+0.64);
  // «А насправді» — not quite
  G.haptic("#cvW", @naspravdi+0.02);
  tl.to("#cvF", {scale: 0.9, duration: 0.45, ease: SP}, @naspravdi+0.1);
  G.bump("#cvW", @karuseli4);
  // «у своєму додатку RUTA» — it flips into RUTA
  tl.fromTo("#cvF", {rotationY: 0}, {rotationY: 180, duration: 1.0, ease: FLIP}, @ruta-0.16);
  tl.to("#cvF", {scale: 1, duration: 0.6, ease: SP}, @ruta-0.16);
  G.ripple("#cvR", @ruta+0.04);
  shn("#cvW .back .sheen", @ruta+0.2);
  // «з одного голосового» — one voice note
  tl.to(["#cvW", "#cvR"], {y: -130, scale: 0.8, duration: 0.6, ease: SP}, @odnoho-0.2);
  arr("#vn", @odnoho-0.1, {s: 0.6, y: 30});
  G.inner("#vnP .mk", @odnoho);
  tl.fromTo("#vnW i", {scaleY: 0.2}, {scaleY: 1, duration: 0.4, ease: SP, stagger: 0.02}, @odnoho+0.05);
  // «виходять» — into RUTA...
  tl.to("#vn", {y: -170, scale: 0.2, autoAlpha: 0, duration: 0.36, ease: "power2.in"}, @vykhodiat-0.06);
  G.bump("#cvW", @vykhodiat+0.3);
  G.ripple("#cvR", @vykhodiat+0.3);
  // ...and out: a reel script, the carousel, stories
  tl.set("#oS", {autoAlpha: 1}, @stsenarii-0.1);
  tl.fromTo("#oS", {x: 335, y: -200, scale: 0.2}, {x: 0, y: 0, scale: 1, duration: 0.8, ease: POP}, @stsenarii-0.1);
  tl.fromTo("#oS .osr", {autoAlpha: 0, x: -10}, {autoAlpha: 1, x: 0, duration: 0.4, ease: SP, stagger: 0.07}, @stsenarii+0.2);
  var OC = {{slots}};
  [1, 0, 2].forEach(function (i, n) {
    var s = OC[i], t = @ikaruseli-0.08 + n * 0.08;
    tl.set("#oc" + i, {autoAlpha: 1}, t);
    tl.fromTo("#oc" + i, {x: 540 - s.x, y: 170 - s.y, scale: 0.2, rotation: 0},
              {x: 0, y: 0, scale: 1, rotation: s.r, duration: 0.8, ease: POP}, t);
  });
  ["#of0", "#of1"].forEach(function (s, n) {
    var t = @storiteli-0.08 + n * 0.1;
    tl.set(s, {autoAlpha: 1}, t);
    tl.fromTo(s, {x: [-270, -360][n], y: -240, scale: 0.2, rotation: 0},
              {x: 0, y: [0, 12][n], scale: 1, rotation: [-4, 5][n], duration: 0.8, ease: POP}, t);
  });
  // «Для своїх клієнтів» — back into RUTA, and RUTA goes
  tl.to(["#oS", "#oc0", "#oc1", "#oc2", "#of0", "#of1"], {x: 0, y: -200, scale: 0.2, autoAlpha: 0,
        duration: 0.36, ease: "power2.in", stagger: 0.03}, @dlia2-0.04);
  G.bump("#cvW", @svoikh-0.1);
  bout("#cvW", @svoikh+0.12, 12, 0.3);
  tl.set("#gR", {autoAlpha: 0}, @svoikh+0.46);''', cx=str(CANVA_C[0]), cy=str(CANVA_C[1]), slots=slots))


# ========================================== G · this system, for clients ==
@beat
def b18_system_again():
    """«Для своїх клієнтів я користуюсь саме цією системою.»

    NEAR, a callback: the shelf and the three step tiles from the hook come
    back and wire up again; a packet runs 1 -> 2 -> 3 on «саме», and on «цією
    системою» a client's carousel (blond-trend) deals out of step 3."""
    slots = json.dumps([{"x": x, "y": y, "r": r} for x, y, r in CS_SLOTS])
    return js(fill('''
  tl.set("#gS", {autoAlpha: 1}, @svoikh);
  bin("#shelf", @svoikh, 14, 0.45);
  tl.fromTo("#shelf", {scale: 0.9, y: 36}, {scale: 1, y: 0, duration: 0.9, ease: SP, immediateRender: false}, @svoikh);
  ["#st1", "#st2", "#st3"].forEach(function (s, i) {
    arr2(s, @kliientiv-0.06 + i * 0.14, {s: 0.5, y: 30});
  });
  draw2("c12T", @korystuius, 0.3); draw2("c12C", @korystuius, 0.3);
  draw2("c23T", @korystuius+0.18, 0.3); draw2("c23C", @korystuius+0.18, 0.3);
  // «саме» — through all three
  G.packet("c12P", @same-0.1, 0.3);
  G.packet("c23P", @same+0.18, 0.3);
  G.bump("#st3", @same+0.46);
  // «цією системою» — a client's carousel out of step 3
  var CS = {{slots}};
  [1, 0, 2].forEach(function (i, n) {
    var s = CS[i], t = @tsiieiu-0.06 + n * 0.09;
    tl.set("#ct" + i, {autoAlpha: 1}, t);
    tl.fromTo("#ct" + i, {x: {{fx}} - s.x, y: -s.y, scale: 0.3, rotation: 0},
              {x: 0, y: 0, scale: 1, rotation: s.r, duration: 0.8, ease: POP}, t);
  });
  // out before her punch-in for the CTA (~77.37, her hair rises to y 465)
  bout(["#st1", "#st2", "#st3", "#c12T", "#c12C", "#c23T", "#c23C", "#ct0", "#ct1", "#ct2"], @i5-0.36, 10, 0.24);
  tl.to("#shelf", {scale: 0.92, y: -30, duration: 0.26, ease: "power2.in"}, @i5-0.36);
  bout("#shelf", @i5-0.34, 14, 0.24);
  tl.set("#gS", {autoAlpha: 0}, @i5-0.08);''', slots=slots, fx=str(635 - 842)))


k.css("""
/* ---- b19 · the DM ---- */
#dm { left: 70px; top: 90px; width: 940px; height: 330px; border-radius: 52px; }
#dmAv { left: 28px; top: 22px; width: 72px; height: 72px; border-radius: 50%;
  background: url("assets/her/avatar.jpg") center / cover no-repeat; box-shadow: 0 0 0 3px rgba(255,255,255,0.75); }
#dmNm { left: 120px; top: 22px; font-size: 36px; font-weight: 700; letter-spacing: -0.01em; }
#dmSb { left: 120px; top: 66px; font-size: 22px; font-weight: 500; color: rgba(255,255,255,0.58); }
#dmIg { left: 852px; top: 28px; width: 60px; height: 60px; }
#dmHr { left: 28px; right: 28px; top: 112px; height: 2px; background: rgba(255,255,255,0.14); }
#dmB { right: 28px; top: 130px; height: 72px; padding: 0 32px; border-radius: 36px 36px 10px 36px;
  line-height: 72px; font-size: 36px; font-weight: 700; color: #fff; white-space: nowrap;
  background: linear-gradient(165deg, #e0204b 0%, #ab112e 46%, #6b081c 100%);
  box-shadow: inset 0 2px 1px rgba(255,255,255,0.5), 0 18px 34px -14px rgba(70,4,20,0.7); }
#dmIn { left: 28px; top: 226px; width: 884px; height: 76px; border-radius: 38px; background: rgba(255,255,255,0.12);
  box-shadow: inset 0 1px 1px rgba(255,255,255,0.35), inset 0 0 0 1.5px rgba(255,255,255,0.22); }
#dmPh { left: 34px; top: 0; height: 76px; line-height: 76px; font-size: 29px; font-weight: 500; color: rgba(255,255,255,0.55); }
#dmTyW { left: 34px; top: 0; height: 76px; line-height: 76px; font-size: 36px; font-weight: 700; color: #fff; white-space: nowrap; }
#dmCa { display: inline-block; width: 4px; height: 44px; margin-left: 3px; vertical-align: -8px; border-radius: 2px; background: #ff9cbc; }
#dmS { width: 60px; height: 60px; }
#dmS .sk { width: 52%; height: 52%; }
""")


def dm_html():
    return fill(u'''
      <div class="g full" id="gD">
        <div class="dglass edge abs hide" id="dm">
          <div class="cx" id="dmAv"></div>
          <div class="cx" id="dmNm">Рута</div>
          <div class="cx" id="dmSb">Instagram · в мережі</div>
          {{ig}}
          <div class="cx" id="dmHr"></div>
          <div class="cx hide" id="dmB">карусель</div>
          <div class="cx" id="dmIn">
            <div class="cx" id="dmPh">Повідомлення…</div>
            <div class="cx" id="dmTyW"><span id="dmTy"></span><b id="dmCa" class="hide"></b></div>
            {{send}}
          </div>
        </div>
      </div>''', ig=tile("dmIg", 60, 852, 28, "clear edge", g.mark("instagram"), ring=False, hide=False),
                send=tile("dmS", 60, 816, 8, "jelly", stroke("send"), "circ", ring=True, hide=False))


@beat
def b19_dm():
    """«І якщо тобі це було дуже цікаво, то напиши слово «карусель».»

    NEAR. Her DMs: the thread with her lands on «І»; the caret comes up on
    «напиши»; «карусель» is typed on the word (BLACKOUT, plaque kept) and
    sent — it lands in the thread as the reel ends."""
    return js('''
  tl.set("#gD", {autoAlpha: 1}, @i5+0.04);
  arr("#dm", @i5+0.04, {s: 0.7, y: 40});
  tl.fromTo(["#dmAv", "#dmNm", "#dmSb", "#dmIg"], {autoAlpha: 0, y: 10}, {autoAlpha: 1, y: 0, duration: 0.5, ease: SP, stagger: 0.05}, @i5+0.2);
  tl.fromTo(["#dmHr", "#dmIn"], {autoAlpha: 0}, {autoAlpha: 1, duration: 0.4}, @tobi);
  G.bump("#dmAv", @tsikavo);
  // «напиши» — the caret
  tl.set("#dmPh", {autoAlpha: 0}, @napyshy);
  tl.set("#dmCa", {autoAlpha: 1}, @napyshy);
  tl.set("#dmCa", {autoAlpha: 0}, @napyshy+0.35);
  tl.set("#dmCa", {autoAlpha: 1}, @napyshy+0.7);
  tl.set("#dmCa", {autoAlpha: 0}, @slovo);
  tl.set("#dmCa", {autoAlpha: 1}, @slovo+0.2);
  // «карусель» — typed (paintAll), then sent
  G.bump("#dmS", @karusel4+0.5);
  G.ripple("#dmSR", @karusel4+0.52);
  tl.set(["#dmTyW"], {autoAlpha: 0}, @karusel4+0.6);
  tl.set("#dmPh", {autoAlpha: 1}, @karusel4+0.6);
  tl.set("#dmB", {autoAlpha: 1}, @karusel4+0.6);
  tl.fromTo("#dmB", {y: 96, scale: 0.6, transformOrigin: "100% 100%"}, {y: 0, scale: 1, duration: 0.5, ease: POP}, @karusel4+0.6);''')


# ================================================================ assemble ==
# Captions drop only on redundancy (STYLE.md §2b.1): the graphic says the word.
BLACKOUT = [
    (16.74, 17.77, "b04 — the chip rolls to 5 хв on «5 хвилин»"),
    (20.58, 21.71, "b05 — the sheet header says Design System"),
    (30.18, 30.88, "b07 — the meter reads 100% on «100%»"),
    (33.74, 34.39, "b08 — the tags say SKILL on «скіли»"),
    (50.64, 51.70, "b12 — the chip says /каруселі on «скіл каруселі»"),
    (52.06, 53.03, "b12 — the chip says /стиль on «скіл стилю»"),
    (53.56, 54.63, "b13 — the switch says Output · Design"),
    (55.34, 55.89, "b13 — the file says Design System"),
    (64.90, 66.23, "b16 — Export to Canva, the Canva tile"),
    (69.56, 69.80, "b17 — the tile says RUTA"),
    (80.60, 81.34, "b19 — «карусель» typed in the DM"),
]
# Every one is a phrase inside a sentence: dropping the plaque with it reads
# as a blink (reel 12's lesson), so the words go and the plaque stays.
KEEP_PLAQUE = [(a, b) for a, b, _ in BLACKOUT]
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
  // a second arrival of something already on the timeline: explicit from, no immediate render
  function arr2(sel, t, o) {
    o = o || {};
    tl.fromTo(sel, {autoAlpha: 0, filter: "blur(12px)"}, {autoAlpha: 1, filter: "blur(0px)", duration: 0.36,
              ease: "power2.out", immediateRender: false}, t);
    tl.set(sel, {filter: "none"}, t + 0.37);
    tl.fromTo(sel, {scale: o.s == null ? 0.5 : o.s, x: o.x || 0, y: o.y == null ? 34 : o.y},
              {scale: 1, x: 0, y: 0, duration: o.d || 0.85, ease: o.ease || POP, immediateRender: false}, t);
  }
  function draw2(id, t, d) {
    var L = document.getElementById(id).getTotalLength() + 3;
    tl.fromTo("#" + id, {strokeDashoffset: L, autoAlpha: 1}, {strokeDashoffset: 0, duration: d || 0.5,
              ease: "power2.inOut", immediateRender: false}, t);
  }
  function shn(sel, t) {
    gsap.set(sel, {xPercent: -120});
    tl.fromTo(sel, {xPercent: -120}, {xPercent: 120, duration: 0.8, ease: "power2.inOut", immediateRender: false}, t);
  }
  function drift1(sel, t, d) { tl.fromTo(sel + " .aurs", {x: 0, y: 0}, {x: -110, y: 70, duration: d, ease: "sine.inOut"}, t); }
  gsap.set(".sheen", {xPercent: -120});
  slopInit("slA"); slopInit("slB"); slopInit("slC");
"""


def counters():
    """Every number that changes as text, driven from one clock so that any
    frame can be rendered cold (reel 15's pattern)."""
    c = {"k1": T["karusel1"], "tr": T["treba"], "dv": T["dovesty"], "ko": T["koly"], "st": T["sto"],
         "k4": T["karusel4"], "dur": DUR}
    return js(r"""
  var CLK = {t: 0};
  function e2o(x) { return 1 - (1 - x) * (1 - x); }
  function seg(t, t0, d, a, b) { return t <= t0 ? a : t >= t0 + d ? b : a + (b - a) * e2o((t - t0) / d); }
  function mmss(s) { s = Math.max(0, Math.round(s)); return Math.floor(s / 60) + ":" + ("0" + (s % 60)).slice(-2); }
  var CN = {}, LKF = document.getElementById("lkF"), LKK = document.getElementById("lkKi");
  function put(id, txt) { if (CN[id] !== txt) { CN[id] = txt; document.getElementById(id).textContent = txt; } }
  function paintAll() {
    var t = CLK.t;
    put("tmV", mmss(t < @k1 ? 300 : 300 - (t - @k1) * 23.04));
    var v = t < @dv ? seg(t, @tr, 0.5, 0, 35) : t < @ko ? seg(t, @dv, 0.6, 35, 62)
          : t < @st ? seg(t, @ko, 0.6, 62, 80) : seg(t, @st, 0.5, 80, 100);
    put("lkV", Math.round(v) + "%");
    var tf = "scaleX(" + (v / 100).toFixed(4) + ")", tk = "translateX(" + (v * 5.2).toFixed(1) + "px)";
    if (CN.lkF !== tf) { CN.lkF = tf; LKF.style.transform = tf; }
    if (CN.lkK !== tk) { CN.lkK = tk; LKK.style.transform = tk; }
    var n = t < @k4 ? 0 : Math.min(8, Math.floor((t - @k4) / 0.055) + 1);
    put("dmTy", "карусель".slice(0, n));
  }
  tl.fromTo(CLK, {t: 0}, {t: @dur, duration: @dur, ease: "none", onUpdate: paintAll}, 0);""", **c)


def main():
    gj = []
    for fn in BEATS:
        j = fn()
        gj.append("  /* %s */" % fn.__name__)
        gj.append(j.rstrip())

    L["behind"] += [wall_html(), slice_html()]
    L["near"] += [chips_html(), shelf_html(), step3_html(), dm_html()]
    L["tk"] += [tk1_html(), tk2_html()]
    L["top"] += [ruta_html()]
    gfx = "\n".join(L["behind"] + L["near"] + L["tk"] + L["top"])

    # the slow push on the plate (§0.8): her, her mattes and what sits in her
    # room (the soft rooms ride in #gW and #gX) move as one
    push = ["#vid", ".matte", "#gW", "#gX"]
    head = [g.js(), slop.js(), HEAD_JS, counters(),
            '  gsap.set(%s, {transformOrigin: "540px 820px"});' % json.dumps(push),
            '  tl.fromTo(%s, {scale: 1}, {scale: 1.045, duration: %.3f, ease: "none"}, 0);'
            % (json.dumps(push), DUR)]
    doc = k.document(
        title=u"Reel 19 — каруселі за 5 хвилин",
        plate="assets/base.mp4",
        gfx_html=g.defs(EXTRA_DEFS) + "\n" + slop.defs() + "\n" + gfx,
        gfx_js="\n".join(head + gj),
        caps=CAPS,
        blackout=BLACKOUT,
        invert=INVERT,
    )
    for a, b in KEEP_PLAQUE:
        for line in ('  tl.to("#scrim", {autoAlpha: 0, duration: 0.20}, %.3f);\n' % (a - 0.20),
                     '  tl.to("#scrim", {autoAlpha: 1, duration: 0.25}, %.3f);\n' % b):
            assert line in doc, line
            doc = doc.replace(line, "", 1)

    out = os.path.join(HERE, "index.html")
    io.open(out, "w", encoding="utf-8").write(doc)
    print("index.html  %d captions, %d beats, %d wall tiles, %.1f KB"
          % (len(CAPS), len(BEATS), len(WALL), os.path.getsize(out) / 1024.0))


main()
