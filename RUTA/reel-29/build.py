# -*- coding: utf-8 -*-
"""Reel 29 — «Ти думаєш, що тобі треба…». Posts 2026-10-11.

Explainer, refined glass (STYLE.md §0). One design system, two formats.

The one object is **her design-system sheet** (swatches in her palette, a type
specimen, a sample of text on screen). A carousel flows out of one side of it
and a reel out of the other — the reel's spine. The carousel side is her real
slides (the colourist webinar set, reel 19's wall); the reel side is a still of
her from this very take, with overlay text in the system's style.

Chain:  near: two separate shelves — a carousel fan on one, a reel on the other
-> they slide into one shelf, the system card lands in the middle and cables out
to a 4:5 slide and a 9:16 reel -> «колись»: the card is gone, the two sides each
get a «1 год» chip, re-roll their look three times, and lean on an empty dashed
slot -> the iris opens out of that slot: the full sheet (стиль, кольори, шрифти,
текст на екрані) -> it folds into the card near her: a text skeleton pours in,
«5 хв», real slides fan out -> the reel lands, the card docks into an «ШІ» tile,
the overlay text writes itself onto the reel, the slide comes back beside it,
one bracket under both -> the iris opens out of the AI tile: two separate
prompts collapse into one sheet that pours into a slide and then into a reel ->
the iris closes onto the card: it fans out to carousel, reel, presentation,
guide, banner, «щось завгодно» -> a wall of her content in one style -> her
closeup (left clear) -> the guide and the system assembling, «15 хв», «твій
бренд» -> the comment box types «система», the guide arrives in a DM.

usage: python build.py   (then: python ../tools/sfx.py mix 29)
"""
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))
from kit import Kit  # noqa: E402
from glass import Glass  # noqa: E402

CUT = json.load(io.open(os.path.join(ROOT, "work", "r29", "cut.json"), encoding="utf-8"))
DUR = 72.350           # (2171 plate frames - 0.5) / 30
FPS = 30
k = Kit(width=1080, height=1920, fps=FPS, duration=DUR)
g = Glass([])
k.css(g.css())

# ---------------------------------------------------------------------------
# NO-PAINT: her closeup «а не як випадковий набір картинок». Captions only.
NO_PAINT = [tuple(x) for x in CUT["no_paint"]]

CAPS = k.load_captions(os.path.join(ROOT, "work", "r29", "captions.json"))
# whisper errors the aligner kept as «her wording»: «Колись я» (she said it in
# that order — the token doubled the «я»), «інтелекті» (heard «металекті»),
# «ще й» (heard «шиї»), and the quoted CTA word in her guillemets.
FIX = {u"Я колись": u"Колись", u"металекті": u"інтелекті", u"шиї": u"ще й",
       u"\"система\",": u"«система»,"}
for c in CAPS:
    c["w"] = FIX.get(c["w"], c["w"])
for _a, _b in zip(CAPS, CAPS[1:]):
    _a["e"] = round(max(_a["s"] + 0.10, _b["s"] - 0.085), 3)


def _n(s):
    return "".join(ch for ch in s.lower() if ch.isalnum())


def S(word, near):
    hits = [c for c in CAPS if _n(word) in [_n(x) for x in c["w"].split()]]
    c = min(hits, key=lambda c: abs(c["s"] - near))
    assert abs(c["s"] - near) < 0.6, (word, near, c["s"])
    return c["s"]


def E(word, near):
    hits = [c for c in CAPS if _n(word) in [_n(x) for x in c["w"].split()]]
    return min(hits, key=lambda c: abs(c["s"] - near))["e"]


T = {
    # A · two separate things -> one system, two formats
    "treba": S(u"треба", 0.95), "okremo": S(u"окремо", 1.27), "dyzain": S(u"дизайн", 2.13),
    "karuseli": S(u"каруселі", 2.53), "okremo2": S(u"окремо", 3.41), "rilsu": S(u"рілсу", 4.01),
    "naspr": S(u"насправді", 4.51), "odna": S(u"одна", 5.19), "dsys": S(u"дизайн-система", 6.25),
    "dsyse": E(u"дизайн-система", 6.25), "zastos": S(u"застосовується", 7.83), "dvokh": S(u"двох", 8.67),
    "format": S(u"форматах", 9.09),
    # B · before
    "kolys": S(u"Колись", 10.04), "vytrach": S(u"витрачала", 10.54), "hod1": S(u"годину", 11.94),
    "hod1e": E(u"годину", 11.94), "montazh": S(u"монтаж", 13.26), "hod2": S(u"годину", 14.44),
    "hod2e": E(u"годину", 14.44), "shchorazu": S(u"щоразу", 15.08), "prydum": S(u"придумувала", 15.48),
    "zanovo": S(u"заново", 16.44), "nichoho": S(u"нічого", 17.22), "spert": S(u"спертись", 17.88),
    # C · the sheet
    "zaraz": S(u"Зараз", 18.70), "odna2": S(u"одна", 19.77), "dsys2": S(u"дизайн-система", 20.19),
    "styl": S(u"стиль", 21.23), "kolory": S(u"кольори", 21.71), "shryfty": S(u"шрифти", 22.23),
    "te": S(u"те", 22.75), "tekst": S(u"текст", 23.43), "ekrani": S(u"екрані", 23.75),
    "ekranie": E(u"екрані", 23.75),
    # C2 · the carousel
    "i1": S(u"І", 24.21), "zrobyty": S(u"зробити", 24.99), "karusel2": S(u"карусель", 25.39),
    "zalyv": S(u"заливаю", 26.23), "skelet": S(u"скелет", 26.87), "tekstom": S(u"текстом", 27.49),
    "za5": S(u"за", 28.10), "p5": S("5", 28.22), "khve": E(u"хвилин", 28.40),
    "vona": S(u"вона", 28.74), "hotova": S(u"готова", 28.92),
    # D · the reel
    "akoly": S(u"коли", 29.66), "rils": S(u"рілс", 30.62), "tasama": S(u"сама", 31.41),
    "shtuch": S(u"штучному", 32.41), "intel": S(u"інтелекті", 32.73), "znaie": S(u"знає", 33.20),
    "vyhl": S(u"виглядати", 33.84), "nakl": S(u"накладений", 34.28), "tekst2": S(u"текст", 34.84),
    "odyn": S(u"один", 36.14), "vpizn": S(u"впізнаваний", 36.54), "styl2": S(u"стиль", 37.34),
    "rils2": S(u"рілс", 38.20), "karusel3": S(u"карусель", 39.00),
    # F · prompts -> one system that pours
    "tobto": S(u"Тобто", 40.20), "dva": S(u"два", 41.09), "okremykh": S(u"окремих", 41.27),
    "promty": S(u"промти", 41.93), "kozhen": S(u"кожен", 42.69), "format2": S(u"формат", 42.95),
    "a2": S(u"а", 44.01), "odyn2": S(u"один", 44.13), "zrobl": S(u"зроблена", 44.73),
    "systema2": S(u"система", 45.13), "systema2e": E(u"система", 45.13),
    "potim": S(u"потім", 46.13), "prosto": S(u"просто", 46.53), "perelyv": S(u"переливається", 46.89),
    "to1": S(u"то", 47.49), "odne": S(u"одне", 47.79), "to2": S(u"то", 48.31), "inshe": S(u"інше", 48.57),
    # G · anything
    "takym": S(u"таким", 49.10), "karuseli2": S(u"каруселі", 50.68), "montazh2": S(u"монтаж", 52.44),
    "prez": S(u"презентації", 54.62), "preze": E(u"презентації", 54.62),
    "haidy": S(u"гайди", 55.52), "haidye": E(u"гайди", 55.52),
    "banery": S(u"банери", 56.10), "banerye": E(u"банери", 56.10),
    "shchos2": S(u"щось", 56.70),
    # H · one brand
    "i3": S(u"І", 57.57), "ves": S(u"весь", 58.71), "kontent": S(u"контент", 58.93),
    "odyn3": S(u"один", 59.99), "brend": S(u"бренд", 60.33),
    # I · the guide
    "zrobyla": S(u"зробила", 63.35), "haid": S(u"гайд", 63.71), "haide": E(u"гайд", 63.71),
    "zibraty": S(u"зібрати", 65.11), "systemu": S(u"систему", 65.99), "p15": S("15", 66.97),
    "khv15e": E(u"хвилин", 67.37), "vlasn": S(u"власного", 68.57), "brendu": S(u"бренду", 69.01),
    "brendue": E(u"бренду", 69.01),
    # J · CTA
    "napyshy": S(u"Напиши", 69.73), "syst": S(u"«система»", 70.69), "syste": E(u"«система»", 70.69),
    "tobi": S(u"тобі", 71.65), "skynu": S(u"скину", 71.89),
    "dur": DUR,
}


def js(src, **extra):
    """`@name`, `@name+0.12`, `@name-0.1` -> one literal time."""
    vals = dict(T)
    vals.update(extra)

    def rep(m):
        v = vals[m.group(1)] + (float(m.group(2)) if m.group(2) else 0.0)
        return "%.3f" % v
    return re.sub(r"@(\w+)([+-]\d+(?:\.\d+)?)?", rep, src)


# ---------------------------------------------------------------------------
# Sound design (tools/sfx.py). Quiet, on the event, never on her joke.
SFX = []


def sfx(name, t, db=0):
    if isinstance(t, str):
        t = float(js(t))
    SFX.append({"t": round(max(0.0, t), 3), "name": name, "db": db})


# ---------------------------------------------------------------------------
# Glyphs
STROKES = {
    "up": '<path d="M12 19.2V5.4M6.2 11l5.8-5.8 5.8 5.8"/>',
    "right": '<path d="M4.8 12h13.6M13 6.6l5.4 5.4-5.4 5.4"/>',
    "check": '<path d="M5.4 12.6l4.3 4.3 8.9-9.5"/>',
    "person": '<circle cx="12" cy="8.2" r="3.6"/><path d="M4.8 20c.9-3.8 3.7-5.8 7.2-5.8s6.3 2 7.2 5.8"/>',
    "heart": '<path d="M12 19.4s-7-4.3-7-9.5A3.9 3.9 0 0 1 12 7.6a3.9 3.9 0 0 1 7 2.3c0 5.2-7 9.5-7 9.5z"/>',
    "bubble": '<path d="M20 11.5c0 4.1-3.6 7.4-8 7.4-1.3 0-2.5-.3-3.6-.8L4.3 19.4l1.3-3.5A7 7 0 0 1 4 11.5C4 7.4 7.6 4.1 12 4.1s8 3.3 8 7.4z"/>',
    "plane": '<path d="M20.6 3.6 3.4 10.4l6.8 2.8 2.8 6.8zM10.2 13.2l4.6-4.6"/>',
    "carousel": '<rect x="7" y="4.4" width="10" height="13.2" rx="2"/><path d="M3.8 7v8.4M20.2 7v8.4M10 20.4h4"/>',
    "reel": '<rect x="6.6" y="2.8" width="10.8" height="18.4" rx="2.6"/><path d="M10.6 9.4v5.2l4.2-2.6z"/>',
    "plus": '<path d="M12 6.5v11M6.5 12h11"/>',
    "play": '<path d="M8.5 6.2v11.6l9.2-5.8z"/>',
}


def stroke(name, cls="sk"):
    return '<svg class="%s" viewBox="0 0 24 24">%s</svg>' % (cls, STROKES[name])


def clock(hid, cls="sk"):
    return ('<svg class="%s" viewBox="0 0 24 24"><circle cx="12" cy="12" r="8.6"/>'
            '<path d="M12 12h3.4"/><path id="%s" d="M12 12V6.9"/></svg>' % (cls, hid))


def tile(tid, size, x, y, material, inner, extra_cls="", hide=True, ring=True):
    r = ('<div class="sqring" id="%sR" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx"></div>'
         % (tid, x, y, size, size)) if ring else ""
    return ('%s<div class="tw%s %s" id="%s" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx">'
            '<div class="%s">%s<div class="sheen"></div></div></div>'
            % (r, " hide" if hide else "", extra_cls, tid, x, y, size, size, material, inner))


ROT = {}


def slide(sid, src, x, y, w, rot=0, hide=True, folder="carousels"):
    """One of her real carousel slides (4:5)."""
    if rot:
        ROT[sid] = rot
    return ('<div class="slw%s" id="%s" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx">'
            '<img src="assets/%s/%s.jpg" alt=""><div class="sheen"></div></div>'
            % (" hide" if hide else "", sid, x, y, w, round(w * 1.25), folder, src))


def phone(pid, x, y, sc, img="r1", ov=True, ov_hide=False, hide=True, wrap=True):
    """A reel: a still of her from this take, the IG rail, and overlay text in
    the system's style (pink lowercase heading + her white caption)."""
    o = ""
    if ov:
        hcls = " hide" if ov_hide else ""
        o = ('<div class="hh%s" id="%sH">одна<br>система</div>'
             '<div class="cpb%s" id="%sB"></div><div class="cp%s" id="%sT">СТИЛЬ</div>'
             % (hcls, pid, hcls, pid, hcls, pid))
    rail = "".join('<div class="rl" style="top:%dpx">%s</div>' % (300 + i * 52, stroke(n, "rk"))
                   for i, n in enumerate(("heart", "bubble", "plane")))
    body = ('<div class="ph9"><img class="her" src="assets/her/%s.jpg" alt=""><div class="shade"></div>%s%s'
            '<i class="av"></i><i class="hn"></i><div class="sheen"></div></div>' % (img, o, rail))
    w, h = round(300 * sc), round(533 * sc)
    if not wrap:
        return '<div class="scl" style="transform:scale(%.4f)">%s</div>' % (sc, body)
    return ('<div class="tw%s" id="%s" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx">'
            '<div class="scl" style="transform:scale(%.4f)">%s</div></div>'
            % (" hide" if hide else "", pid, x, y, w, h, sc, body))


SW4 = ["#17141c", "#b4122f", "#ff6e9c", "#fbe3ea"]


def dscard(did, x, y, sc, hide=True, ring=False, parts=False):
    """The design system as a card: label, type, four swatches, two text rows."""
    p = " p" if parts else ""
    sw = "".join('<i class="sw%s" style="left:%dpx;background:%s"></i>' % (p, 26 + i * 56, c)
                 for i, c in enumerate(SW4))
    w, h = round(260 * sc), round(320 * sc)
    r = ('<div class="sqring" id="%sR" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx;border-radius:%dpx"></div>'
         % (did, x, y, w, h, round(40 * sc))) if ring else ""
    return ('%s<div class="tw%s" id="%s" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx">'
            '<div class="scl" style="transform:scale(%.4f)"><div class="ds">'
            '<span class="mi%s">ДИЗАЙН-СИСТЕМА</span><span class="aa%s">А<b>а</b></span>%s'
            '<i class="b1%s"></i><i class="b2%s"></i><div class="sheen"></div></div></div></div>'
            % (r, " hide" if hide else "", did, x, y, w, h, sc, p, p, sw, p, p))


def chip(cid, cx, top, text, icon=None, w=300):
    """A pearl time chip, centred on cx."""
    ic = icon or ""
    return ('<div class="tcw hide" id="%s" style="left:%dpx;top:%dpx;width:%dpx">'
            '<div class="tc">%s<span>%s</span></div></div>' % (cid, cx - w // 2, top, w, ic, text))


def label(cid, cx, top, text, w=240):
    return ('<div class="tcw hide" id="%s" style="left:%dpx;top:%dpx;width:%dpx">'
            '<div class="lb">%s</div></div>' % (cid, cx - w // 2, top, w, text))


k.css("""
.abs { position: absolute; }
.hide { opacity: 0; visibility: hidden; }
.tw { position: absolute; }
.scl { position: absolute; left: 0; top: 0; transform-origin: 0 0; }
.sk { fill: none; stroke: url(#gw); stroke-width: 2.3; stroke-linecap: round; stroke-linejoin: round;
  width: 50%; height: 50%; position: relative; z-index: 1; overflow: visible; }
.pearl .sk { stroke: #17141c; }
.clear { overflow: hidden; }
.circ .jelly, .circ .pearl, .circ .clear, .circ .sheen { border-radius: 50%; }
.aurs { position: absolute; left: -700px; top: -700px; width: 2480px; height: 3320px; pointer-events: none;
  background:
    radial-gradient(circle 526px at 1560px 880px, rgba(255,110,156,0.50), rgba(255,110,156,0)),
    radial-gradient(circle 634px at 760px 2360px, rgba(222,32,74,0.55), rgba(222,32,74,0)),
    radial-gradient(circle 382px at 1480px 1910px, rgba(255,198,214,0.20), rgba(255,198,214,0)); }
.shc { position: absolute; inset: 0; border-radius: inherit; overflow: hidden; pointer-events: none; }
.shc .sheen { mix-blend-mode: normal; opacity: 0.4; }

/* her real slides */
.slw { position: absolute; border-radius: 14px; overflow: hidden; background: #17141c;
  box-shadow: 0 0 0 2px rgba(255,255,255,0.55), 0 30px 54px -20px rgba(20,2,8,0.66); }
.slw img { position: absolute; left: 0; top: 0; width: 100%; height: 100%; object-fit: cover; display: block; }
.slw .sheen { mix-blend-mode: normal; opacity: 0.35; }

/* a reel, 300 x 533 at scale 1 */
.ph9 { position: absolute; left: 0; top: 0; width: 300px; height: 533px; border-radius: 40px; overflow: hidden;
  background: #17141c;
  box-shadow: 0 0 0 6px #17141c, 0 0 0 8px rgba(255,255,255,0.34), 0 46px 90px -30px rgba(10,0,4,0.72); }
.ph9 img.her { position: absolute; left: 0; top: 0; width: 300px; height: 533px; object-fit: cover; }
.ph9 .shade { position: absolute; inset: 0;
  background: linear-gradient(180deg, rgba(14,4,8,0.62) 0%, rgba(14,4,8,0) 38%, rgba(14,4,8,0) 64%, rgba(14,4,8,0.5) 100%); }
.ph9 .hh { position: absolute; left: 24px; top: 46px; font-size: 52px; font-weight: 900; line-height: 0.9;
  letter-spacing: -0.045em; color: #ff6e9c; }
.ph9 .cpb { position: absolute; left: 52px; right: 52px; top: 384px; height: 62px; border-radius: 20px;
  background: rgba(24,8,14,0.46); }
.ph9 .cp { position: absolute; left: 0; right: 0; top: 384px; height: 62px; line-height: 62px; text-align: center;
  font-size: 34px; font-weight: 900; color: #fff; letter-spacing: -0.01em; }
.ph9 .rl { position: absolute; right: 12px; width: 34px; height: 34px; }
.rk { width: 34px; height: 34px; fill: none; stroke: #fff; stroke-width: 2; stroke-linecap: round; stroke-linejoin: round; }
.ph9 .av { position: absolute; left: 18px; bottom: 22px; width: 32px; height: 32px; border-radius: 50%;
  background: rgba(255,255,255,0.85); }
.ph9 .hn { position: absolute; left: 60px; bottom: 32px; width: 96px; height: 12px; border-radius: 6px;
  background: rgba(255,255,255,0.78); }
.ph9 .sheen { mix-blend-mode: normal; opacity: 0.35; }
/* «before»: three looks, invented each time */
.ph9 .v1 { position: absolute; left: 30px; top: 70px; padding: 8px 16px; background: #fff; color: #17141c;
  font-size: 30px; font-weight: 900; transform: rotate(-3deg); }
.ph9 .v2 { position: absolute; left: 0; right: 0; top: 200px; text-align: center; font-size: 56px; font-weight: 900;
  color: transparent; -webkit-text-stroke: 2.5px #fff; letter-spacing: -0.02em; }
.ph9 .v3 { position: absolute; left: 0; right: 0; top: 410px; height: 70px; line-height: 70px; text-align: center;
  background: #ff6e9c; color: #17141c; font-size: 34px; font-weight: 700; }

/* the design-system card, 260 x 320 at scale 1 */
.ds { position: absolute; left: 0; top: 0; width: 260px; height: 320px; border-radius: 40px; overflow: hidden;
  background: linear-gradient(172deg, #ffffff 0%, #fff9fb 55%, #fdf0f4 100%);
  box-shadow: inset 0 2px 1px #fff, inset 0 -24px 48px -26px rgba(180,18,47,0.16),
              0 44px 90px -30px rgba(24,4,12,0.62), 0 0 0 1px rgba(255,255,255,0.4); }
.ds .mi { position: absolute; left: 26px; top: 20px; font-size: 15px; font-weight: 700; letter-spacing: 0.16em;
  color: rgba(23,20,28,0.42); }
.ds .aa { position: absolute; left: 22px; top: 66px; font-size: 104px; font-weight: 900; letter-spacing: -0.05em;
  line-height: 1; color: #17141c; }
.ds .aa b { font-weight: 900;
  background: linear-gradient(118deg, #7e0b20 0%, #b4122f 42%, #ff6e9c 100%);
  -webkit-background-clip: text; background-clip: text; color: transparent; padding-right: 6px; }
.ds .sw { position: absolute; top: 192px; width: 44px; height: 44px; border-radius: 50%;
  box-shadow: inset 0 0 0 1.5px rgba(23,20,28,0.08), inset 0 2px 1px rgba(255,255,255,0.35); }
.ds .b1 { position: absolute; left: 26px; top: 258px; width: 150px; height: 14px; border-radius: 7px;
  background: linear-gradient(115deg, #c41434 0%, #8d0d24 100%); }
.ds .b2 { position: absolute; left: 26px; top: 284px; width: 200px; height: 10px; border-radius: 5px;
  background: rgba(23,20,28,0.13); }

/* chips */
.tcw { position: absolute; display: flex; justify-content: center; }
.tc { height: 62px; padding: 0 26px 0 16px; border-radius: 31px; display: flex; align-items: center; gap: 10px;
  background: linear-gradient(160deg, #ffffff 0%, #fff5f8 52%, #f5dfe6 100%); color: #17141c;
  font-size: 32px; font-weight: 900; letter-spacing: -0.01em; white-space: nowrap;
  box-shadow: inset 0 2px 1px #fff, inset 0 -14px 24px -12px rgba(180,18,47,0.16), 0 26px 46px -18px rgba(30,4,12,0.62); }
.tc .sk { width: 40px; height: 40px; stroke: #b4122f; stroke-width: 2.3; }
.lb { height: 48px; line-height: 48px; padding: 0 20px; border-radius: 24px; white-space: nowrap;
  background: linear-gradient(160deg, #ffffff 0%, #fff5f8 52%, #f5dfe6 100%); color: #17141c;
  font-size: 26px; font-weight: 700; letter-spacing: -0.005em;
  box-shadow: inset 0 2px 1px #fff, 0 20px 40px -16px rgba(30,4,12,0.6); }
.fmt { height: 50px; line-height: 50px; padding: 0 18px; border-radius: 25px; white-space: nowrap;
  background: rgba(20,6,12,0.40); color: #fff; font-size: 28px; font-weight: 700; letter-spacing: 0.02em;
  box-shadow: inset 0 1.5px 1px rgba(255,255,255,0.35), inset 0 0 0 1.5px rgba(255,255,255,0.22); }

/* an empty dashed slot — the system that was not there */
.dash { position: absolute; border: 5px dashed rgba(255,255,255,0.78); border-radius: 30px;
  background: rgba(255,255,255,0.07); }

/* a text skeleton */
.skl { position: absolute; border-radius: 18px; overflow: hidden;
  background: linear-gradient(172deg, #ffffff 0%, #fff9fb 60%, #fdf0f4 100%);
  box-shadow: inset 0 2px 1px #fff, 0 34px 60px -24px rgba(24,4,12,0.6); }
.skl i { position: absolute; display: block; border-radius: 8px; transform-origin: 100% 50%; }
.skl i.hb { background: linear-gradient(115deg, #c41434 0%, #8d0d24 100%); }
.skl i.rr { background: rgba(23,20,28,0.15); }
.strm { fill: none; stroke: #ff8ab0; stroke-width: 14; stroke-linecap: round;
  filter: drop-shadow(0 0 10px rgba(255,110,156,0.9)); }
.strm.big { stroke-width: 30; stroke: #ff6e9c; }
.brk { fill: none; stroke: #ffd6e3; stroke-width: 8; stroke-linecap: round; stroke-linejoin: round;
  filter: drop-shadow(0 0 10px rgba(255,110,156,0.9)); }
.cab .tube { fill: none; stroke: rgba(255,255,255,0.26); stroke-width: 20; stroke-linecap: round; }
.cab .core { fill: none; stroke: rgba(255,255,255,0.92); stroke-width: 4.5; stroke-linecap: round; }
.cab .wire { fill: none; stroke: rgba(255,255,255,0.62); stroke-width: 5; stroke-linecap: round; }

/* ---- the takeover sheet ---- */
.cm { position: absolute; font-size: 24px; font-weight: 700; letter-spacing: 0.16em; color: rgba(23,20,28,0.42); }
.cm.wh { color: rgba(255,255,255,0.72); width: 1080px; left: 0; text-align: center; }
#cHd { position: absolute; left: 60px; top: 46px; font-size: 96px; font-weight: 900; letter-spacing: -0.045em;
  line-height: 1.1; color: #17141c; white-space: nowrap; }
#cHr { position: absolute; left: 64px; top: 176px; width: 980px; }
.cpill { position: absolute; width: 230px; height: 92px; border-radius: 46px; display: flex; align-items: center;
  justify-content: center; background: linear-gradient(165deg, #e0204b 0%, #ab112e 46%, #6b081c 100%);
  box-shadow: inset 0 2px 1px rgba(255,255,255,0.5), 0 22px 40px -16px rgba(70,4,20,0.6); }
.cpill .sk { width: 56px; height: 56px; stroke: #fff; stroke-width: 2.4; }
.chl { position: absolute; padding: 6px 18px 10px; background: #ff6e9c; color: #17141c; font-size: 50px;
  font-weight: 900; letter-spacing: -0.03em; line-height: 1; }
.chd { position: absolute; width: 330px; height: 110px; border-radius: 22px; background: #17141c;
  color: #ff6e9c; font-size: 56px; font-weight: 900; letter-spacing: -0.045em; line-height: 110px; padding-left: 26px; }
.csw { position: absolute; width: 170px; height: 170px; border-radius: 50%;
  box-shadow: inset 0 3px 2px rgba(255,255,255,0.32), inset 0 -18px 30px -12px rgba(0,0,0,0.20),
              inset 0 0 0 1.5px rgba(23,20,28,0.07), 0 26px 44px -20px rgba(30,4,12,0.5); }
.chx { position: absolute; top: 640px; width: 170px; text-align: center; font-size: 23px; font-weight: 700;
  letter-spacing: 0.05em; color: rgba(23,20,28,0.46); }
#cAa { position: absolute; left: 50px; top: 806px; font-size: 300px; font-weight: 900; letter-spacing: -0.05em;
  line-height: 0.92; color: #17141c; }
#cAa b { background: linear-gradient(118deg, #7e0b20 0%, #b4122f 42%, #ff6e9c 100%);
  -webkit-background-clip: text; background-clip: text; color: transparent; padding-right: 10px; }
.cwt { position: absolute; left: 500px; font-size: 64px; letter-spacing: -0.03em; color: #17141c; line-height: 1; }
#cPS { position: absolute; left: 504px; top: 1080px; font-size: 30px; font-weight: 500; color: rgba(23,20,28,0.46); }

/* the prompt bars */
.pbar { position: absolute; left: 40px; width: 1000px; height: 170px; border-radius: 85px;
  background: linear-gradient(172deg, #ffffff 0%, #fff9fb 55%, #fdf0f4 100%);
  box-shadow: inset 0 2px 1px #fff, 0 50px 100px -36px rgba(8,0,3,0.75); }
.pbar .pl { position: absolute; left: 300px; height: 22px; border-radius: 11px; background: rgba(23,20,28,0.13);
  transform-origin: 0 50%; }
.pbar .chip { position: absolute; left: 168px; top: 56px; }
/* vessels the system pours into */
.ves { position: absolute; border-radius: 30px; overflow: hidden; border: 5px dashed rgba(255,255,255,0.62);
  background: rgba(255,255,255,0.06); }
.ves .liq { position: absolute; inset: 0;
  background: linear-gradient(180deg, #ff9cbc 0%, #ff6e9c 22%, #e0204b 64%, #8d0d24 100%); }
.ves .liq::before { content: ""; position: absolute; left: 0; right: 0; top: 0; height: 10px;
  background: rgba(255,255,255,0.65); }
.ves img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }

/* formats */
.prs { position: absolute; border-radius: 16px; overflow: hidden;
  background: linear-gradient(172deg, #ffffff 0%, #fff9fb 60%, #fdf0f4 100%);
  box-shadow: inset 0 2px 1px #fff, 0 30px 54px -20px rgba(24,4,12,0.62); }
.prs i, .gd i, .bn i { position: absolute; display: block; }
.prs i.hb, .gd i.hb { height: 14px; border-radius: 7px; background: linear-gradient(115deg, #c41434 0%, #8d0d24 100%); }
.prs i.rr, .gd i.rr { height: 9px; border-radius: 5px; background: rgba(23,20,28,0.15); }
.prs i.bar { bottom: 18px; width: 22px; border-radius: 6px; background: linear-gradient(170deg, #ff6e9c 0%, #b4122f 100%); }
.gd { position: absolute; border-radius: 14px 18px 18px 14px; overflow: hidden;
  background: linear-gradient(172deg, #ffffff 0%, #fff9fb 60%, #fdf0f4 100%);
  box-shadow: inset 0 2px 1px #fff, 6px 0 0 -1px #f4dfe5, 11px 0 0 -2px #ecc8d0, 0 30px 54px -20px rgba(24,4,12,0.62); }
.gd i.sp { left: 0; top: 0; bottom: 0; width: 18px; background: linear-gradient(165deg, #e0204b 0%, #8d0d24 100%); }
.gd .ga { position: absolute; left: 32px; top: 40px; font-size: 52px; font-weight: 900; letter-spacing: -0.05em;
  color: #17141c; line-height: 1; }
.bn { position: absolute; border-radius: 16px; overflow: hidden; background: linear-gradient(160deg, #241f2c 0%, #17141c 100%);
  box-shadow: inset 0 1.5px 0 rgba(255,255,255,0.16), 0 30px 54px -20px rgba(10,0,4,0.7); }
.bn i.ph { height: 16px; border-radius: 8px; background: #ff6e9c; }
.bn i.pr { height: 9px; border-radius: 5px; background: rgba(255,255,255,0.55); }
.bn i.pl { border-radius: 999px; background: linear-gradient(165deg, #ff6e9c 0%, #e0204b 100%); }
.gh { position: absolute; border: 4px dashed rgba(255,255,255,0.75); display: flex; align-items: center;
  justify-content: center; background: rgba(255,255,255,0.08); }
.gh .sk { width: 54%; height: 54%; stroke: #fff; stroke-width: 2.6; }

/* reel covers in the wall */
.cvh { position: absolute; left: 12px; top: 14px; font-size: 30px; font-weight: 900; line-height: 0.9;
  letter-spacing: -0.045em; color: #ff6e9c; }
.cvs { position: absolute; inset: 0; background: linear-gradient(180deg, rgba(14,4,8,0.6) 0%, rgba(14,4,8,0) 45%); }
.cvp { position: absolute; right: 10px; top: 12px; width: 28px; height: 28px; fill: #fff; }

/* the guide */
.bk { position: absolute; inset: 0; border-radius: 22px 30px 30px 22px; overflow: hidden;
  background: linear-gradient(165deg, #e0204b 0%, #ab112e 46%, #6b081c 100%);
  box-shadow: inset 0 2px 1px rgba(255,255,255,0.55), inset 0 -26px 40px -14px rgba(255,125,165,0.55),
              8px 0 0 -2px #fbe3ea, 14px 0 0 -4px #f4dfe5, 0 40px 70px -24px rgba(70,4,20,0.66); }
.bk .bt { position: absolute; left: 28px; top: 26px; font-size: 104px; font-weight: 900; letter-spacing: -0.05em;
  line-height: 1; color: #fff; }
.bk .bm { position: absolute; left: 30px; top: 160px; font-size: 17px; font-weight: 700; letter-spacing: 0.16em;
  color: rgba(255,255,255,0.72); }
.bk i { position: absolute; display: block; }
.bk i.d { top: 204px; width: 36px; height: 36px; border-radius: 50%; box-shadow: 0 0 0 3px rgba(255,255,255,0.85); }
.bk i.r { left: 30px; height: 10px; border-radius: 5px; background: rgba(255,255,255,0.45); }
.tag { position: absolute; height: 60px; line-height: 60px; padding: 0 26px; border-radius: 30px; white-space: nowrap;
  background: linear-gradient(165deg, #ff8ab0 0%, #ff6e9c 50%, #e0204b 100%); color: #fff; font-size: 30px; font-weight: 900;
  letter-spacing: -0.01em; box-shadow: inset 0 2px 1px rgba(255,255,255,0.55), 0 22px 40px -16px rgba(70,4,20,0.7); }

/* the comment box + DM */
#jPh { position: absolute; left: 150px; top: 0; height: 150px; line-height: 150px; font-size: 40px; font-weight: 500;
  color: rgba(255,255,255,0.5); }
#jTx { position: absolute; left: 150px; top: 0; height: 150px; line-height: 150px; font-size: 48px; font-weight: 700;
  color: #fff; letter-spacing: -0.01em; }
#jTx::after { content: ""; display: inline-block; width: 3px; height: 46px; margin-left: 4px; vertical-align: -6px;
  background: #ff8ab0; }
.ck { position: absolute; width: 120px; height: 120px; margin: -60px 0 0 -60px; border-radius: 50%;
  border: 7px solid #ff6e9c; opacity: 0; visibility: hidden; z-index: 5; }
.dm { position: absolute; border-radius: 48px; overflow: hidden;
  background: linear-gradient(160deg, #ffffff 0%, #fff5f8 52%, #f5dfe6 100%);
  box-shadow: inset 0 2px 1px #fff, 0 40px 80px -28px rgba(30,4,12,0.65); }
.dm i { position: absolute; display: block; }
.dm i.r { height: 16px; border-radius: 8px; background: rgba(23,20,28,0.15); }
.dm .mb { position: absolute; left: 28px; top: 22px; width: 112px; height: 146px; border-radius: 12px 16px 16px 12px;
  background: linear-gradient(165deg, #e0204b 0%, #ab112e 46%, #6b081c 100%);
  box-shadow: inset 0 2px 1px rgba(255,255,255,0.5), 5px 0 0 -1px #fbe3ea, 0 16px 30px -12px rgba(70,4,20,0.6); }
.dm .mb span { position: absolute; left: 12px; top: 10px; font-size: 36px; font-weight: 900; color: #fff;
  letter-spacing: -0.05em; }
.dm .pi { position: absolute; left: 172px; top: 34px; width: 54px; height: 54px; }
.dm .pi .sk { width: 54px; height: 54px; stroke: #b4122f; stroke-width: 2.2; }
""")

L = []
BEATS = []


def beat(fn):
    BEATS.append(fn)
    return fn


# ===========================================================================
# A · two separate shelves -> one system -> two formats
@beat
def a_hook():
    fan = (slide("aF1", "wb02-s", 112, 238, 220, rot=-9) + slide("aF2", "wb03-s", 312, 238, 220, rot=9)
           + slide("aF0", "wb04-s", 210, 222, 220))
    cab = ('<svg class="cab abs" width="1080" height="700" viewBox="0 0 1080 700" style="left:0;top:0">'
           '<path class="tube hide" id="aT1" d="M410 338 C 380 338 350 338 322 338"/>'
           '<path class="core hide" id="aC1" d="M410 338 C 380 338 350 338 322 338"/>'
           '<path class="tube hide" id="aT2" d="M670 338 C 720 338 770 338 820 338"/>'
           '<path class="core hide" id="aC2" d="M670 338 C 720 338 770 338 820 338"/></svg>')
    # B's columns: a slide + a chip, a reel + a chip. The slide re-rolls its look.
    col1 = ('<div class="tw hide" id="aCol1" style="left:100px;top:200px;width:220px;height:360px">'
            '<div class="slw" id="aCs" style="left:0;top:0;width:220px;height:275px">'
            '<img id="aV0" src="assets/carousels/wb04-s.jpg" alt="">'
            '<img id="aV1" class="hide" src="assets/carousels/kg05-s.jpg" alt="">'
            '<img id="aV2" class="hide" src="assets/carousels/tr01-s.jpg" alt="">'
            '<img id="aV3" class="hide" src="assets/carousels/kg04-s.jpg" alt="">'
            '<div class="sheen"></div></div>'
            '<div class="tcw hide" id="aK1" style="left:-40px;top:300px;width:300px"><div class="fmt">4:5</div></div>'
            '<div class="tcw hide" id="aH1" style="left:-40px;top:296px;width:300px"><div class="tc">%s<span>1 год</span></div></div>'
            '</div>' % clock("aH1h"))
    ph = phone("aP", 0, 0, 0.52, img="r1", ov=False, wrap=False)
    ph = ph.replace('<div class="sheen"></div></div></div>',
                    '<div class="v1 hide" id="aW1">ВАРІАНТ 1</div><div class="v2 hide" id="aW2">варіант 2</div>'
                    '<div class="v3 hide" id="aW3">Варіант 3</div><div class="sheen"></div></div></div>', 1)
    col2 = ('<div class="tw hide" id="aCol2" style="left:822px;top:199px;width:156px;height:360px">'
            '<div class="tw" id="aPw" style="left:0;top:0;width:156px;height:277px">%s</div>'
            '<div class="tcw hide" id="aK2" style="left:-72px;top:301px;width:300px"><div class="fmt">9:16</div></div>'
            '<div class="tcw hide" id="aH2" style="left:-72px;top:297px;width:300px"><div class="tc">%s<span>1 год</span></div></div>'
            '</div>' % (ph, clock("aH2h")))
    L.append(
        '<div class="g full" id="gA">'
        '<div class="shelf edge hide" id="aL" style="left:60px;top:150px;width:460px;height:470px"></div>'
        '<div class="shelf edge hide" id="aR" style="left:560px;top:150px;width:460px;height:470px"></div>'
        '<div class="shelf edge hide" id="aM" style="left:60px;top:150px;width:960px;height:470px"></div>'
        + fan + phone("aPh", 682, 193, 0.72, img="r1", ov=False)
        + cab
        + '<div class="dash hide" id="aSl" style="left:410px;top:178px;width:260px;height:320px"></div>'
        + dscard("aDS", 410, 178, 1.0, ring=True)
        + col1 + col2 + '</div>')
    sfx("pop", T["okremo"] + 0.02)
    sfx("pop", T["rilsu"] - 0.02, -1)
    sfx("whoosh-short", T["naspr"], -2)
    sfx("pop", T["odna"])
    sfx("click", T["hod1"])
    sfx("click", T["hod2"])
    sfx("click-soft", T["zanovo"], -2)

    def reroll(t, i):
        return ('  tl.to(["#aCs", "#aPw"], {rotationY: 90, duration: 0.12, ease: "power2.in"}, %.3f);\n'
                '  tl.set("#aV%d", {autoAlpha: 0}, %.3f); tl.set("#aV%d", {autoAlpha: 1}, %.3f);\n'
                '  %s tl.set("#aW%d", {autoAlpha: 1}, %.3f);\n'
                '  tl.to(["#aCs", "#aPw"], {rotationY: 0, duration: 0.5, ease: SP}, %.3f);'
                % (t, i - 1, t + 0.12, i, t + 0.12,
                   ('tl.set("#aW%d", {autoAlpha: 0}, %.3f);' % (i - 1, t + 0.12)) if i > 1 else "",
                   i, t + 0.12, t + 0.12))
    rr = "\n".join(reroll(t, i + 1) for i, t in enumerate(
        (T["shchorazu"] - 0.02, T["prydum"] + 0.22, T["zanovo"] - 0.02)))
    return js("""
  tl.set("#gA", {autoAlpha: 1}, 0);
  gsap.set(["#aCs", "#aPw"], {transformPerspective: 900});
  arr("#aL", @okremo-0.06, {s: 0.82, y: 30});
  [["#aF1", 0], ["#aF2", 0.1], ["#aF0", 0.2]].forEach(function (p) { arr(p[0], @dyzain+0.02+p[1], {s: 0.5, y: 40, d: 0.75}); });
  arr("#aR", @okremo2-0.06, {s: 0.82, y: 30});
  arr("#aPh", @rilsu-0.14, {s: 0.5, y: 40, d: 0.75});
  /* «а насправді» — the two shelves slide into one */
  bout(["#aF0", "#aF1", "#aF2", "#aPh"], @naspr-0.12, 10, 0.26);
  tl.to("#aL", {x: 230, scaleX: 0.6, autoAlpha: 0, duration: 0.5, ease: "power3.inOut"}, @naspr-0.05);
  tl.to("#aR", {x: -230, scaleX: 0.6, autoAlpha: 0, duration: 0.5, ease: "power3.inOut"}, @naspr-0.05);
  tl.fromTo("#aM", {autoAlpha: 0, scaleX: 0.45}, {autoAlpha: 1, scaleX: 1, duration: 0.7, ease: SP}, @naspr+0.25);
  arr("#aDS", @odna-0.08, {s: 0.4, y: 30, d: 0.85});
  G.ripple("#aDSR", @odna+0.3);
  shn("#aDS .sheen", @dsys);
  /* «застосовується в двох форматах» */
  tl.set(["#aT1", "#aC1", "#aT2", "#aC2"], {autoAlpha: 1}, @zastos);
  draw2("aT1", @zastos, 0.4); draw2("aC1", @zastos, 0.4); draw2("aT2", @zastos, 0.4); draw2("aC2", @zastos, 0.4);
  tl.set(["#aCol1", "#aCol2"], {autoAlpha: 1}, @dvokh-0.1);
  arr("#aCs", @dvokh-0.1, {s: 0.4, x: 60, y: 0, d: 0.8});
  arr("#aPw", @dvokh+0.05, {s: 0.4, x: -60, y: 0, d: 0.8});
  arr("#aK1", @format-0.05, {s: 0.5, y: 14, d: 0.6});
  arr("#aK2", @format+0.07, {s: 0.5, y: 14, d: 0.6});
  /* «колись» — the system is gone */
  bout(["#aDS", "#aT1", "#aC1", "#aT2", "#aC2", "#aK1", "#aK2"], @kolys-0.15, 10, 0.3);
  tl.to("#aPw", {autoAlpha: 0.5, duration: 0.3}, @vytrach);
  G.bump("#aCs", @vytrach+0.05);
  arr("#aH1", @hod1-0.1, {s: 0.4, y: 20, d: 0.7});
  tl.fromTo("#aH1h", {rotation: 0}, {rotation: 360, svgOrigin: "12 12", duration: 0.9, ease: "power2.inOut"}, @hod1+0.05);
  tl.to("#aPw", {autoAlpha: 1, duration: 0.3}, @montazh-0.1);
  tl.to("#aCs", {autoAlpha: 0.5, duration: 0.3}, @montazh-0.1);
  G.bump("#aPw", @montazh);
  arr("#aH2", @hod2-0.1, {s: 0.4, y: 20, d: 0.7});
  tl.fromTo("#aH2h", {rotation: 0}, {rotation: 360, svgOrigin: "12 12", duration: 0.9, ease: "power2.inOut"}, @hod2+0.05);
  tl.to("#aCs", {autoAlpha: 1, duration: 0.3}, @shchorazu-0.3);
  /* «щоразу придумувала оформлення заново» — three new looks */
{{reroll}}
  /* «бо не було нічого, на що спертись» */
  tl.fromTo("#aSl", {autoAlpha: 0, scale: 0.8}, {autoAlpha: 1, scale: 1, duration: 0.5, ease: SP}, @nichoho-0.05);
  gsap.set("#aCol1", {transformOrigin: "100% 100%"}); gsap.set("#aCol2", {transformOrigin: "0% 100%"});
  tl.to("#aCol1", {rotation: 9, x: 26, y: 18, duration: 0.6, ease: SOFT}, @spert-0.02);
  tl.to("#aCol2", {rotation: -9, x: -26, y: 18, duration: 0.6, ease: SOFT}, @spert+0.06);
  tl.set("#gA", {autoAlpha: 0}, @zaraz+0.8);""").replace("{{reroll}}", rr)


# ===========================================================================
# C · OVER — the iris opens out of the empty slot: the full sheet
SW5 = [("#17141C", "#17141c"), ("#8D0D24", "#8d0d24"), ("#B4122F", "#b4122f"),
       ("#FF6E9C", "#ff6e9c"), ("#FBE3EA", "#fbe3ea")]


@beat
def c_sheet():
    circles = "".join(
        '<div class="csw" id="cw%d" style="left:%dpx;top:456px;background:%s"></div>'
        '<div class="chx" id="cx%d" style="left:%dpx">%s</div>' % (i, 64 + i * 194, c, i, 64 + i * 194, hx)
        for i, (hx, c) in enumerate(SW5))
    weights = "".join('<div class="cwt" id="cwt%d" style="top:%dpx;font-weight:%d">%s</div>' % (i, 822 + i * 84, wt, nm)
                      for i, (wt, nm) in enumerate(((900, "Black"), (700, "Bold"), (400, "Regular"))))
    sheet = (
        '<div class="sheet" id="cS" data-layout-allow-overflow style="left:60px;top:100px;width:1100px;height:1130px">'
        '<div id="cHd">дизайн-система</div><div class="hair" id="cHr"></div>'
        '<span class="cm" id="cm1" style="left:64px;top:208px">СТИЛЬ</span>'
        '<div class="cpill" id="cs1" style="left:64px;top:262px">%s</div>'
        '<div class="chl" id="cs2" style="left:328px;top:276px">впізнавано</div>'
        '<div class="chd" id="cs3" style="left:650px;top:254px">заголовок</div>'
        '<span class="cm" id="cm2" style="left:64px;top:412px">КОЛЬОРИ</span>%s'
        '<span class="cm" id="cm3" style="left:64px;top:722px">ШРИФТИ</span>'
        '<div id="cAa">А<b>а</b></div>%s<div id="cPS">Product Sans</div>'
        '<div class="sheen"></div></div>'
        '<span class="cm wh" id="cm4" style="top:1282px">ТЕКСТ НА ЕКРАНІ</span>%s'
        % (stroke("right"), circles, weights, phone("cPh", 381, 1326, 1.06, img="r1", ov=True, ov_hide=True)))
    L.append('<div class="g full" id="gC"><div class="tkg"></div><div class="aurs"></div><div class="grain"></div>'
             + sheet + '</div>')
    sfx("whoosh-short", T["zaraz"] - 0.12)
    sfx("pop", T["odna2"], -1)
    sfx("click-soft", T["kolory"], -2)
    sfx("whoosh-short", T["i1"] - 0.25, -3)
    return js("""
  G.irisOpen("#gC", @zaraz-0.12, 540, 338, 0.85);
  drift1("#gC", @zaraz, 5.6);
  gsap.set("#cS", {transformOrigin: "480px 238px"});
  arr("#cS", @odna2-0.14, {s: 0.26, y: 0, d: 0.95});
  gsap.set(["#cm1", "#cm2", "#cm3", "#cm4", "#cPS", "#cHd", "#cs1", "#cs2", "#cs3", "#cAa", "#cPh"], {autoAlpha: 0});
  tl.set("#cHd", {autoAlpha: 1}, @dsys2-0.06);
  tl.fromTo("#cHd", {clipPath: "inset(0% 100% 0% 0%)"}, {clipPath: "inset(0% 0% 0% 0%)", duration: 0.6, ease: "power2.out", immediateRender: false}, @dsys2-0.06);
  tl.fromTo("#cHr", {scaleX: 0}, {scaleX: 1, duration: 0.7, ease: "power2.out"}, @dsys2+0.15);
  shn("#cS > .sheen", @dsys2+0.35);
  bin("#cm1", @styl-0.1, 6, 0.3);
  [["#cs1", 0], ["#cs2", 0.1], ["#cs3", 0.2]].forEach(function (p) { arr(p[0], @styl-0.04+p[1], {s: 0.5, y: 24, d: 0.7}); });
  bin("#cm2", @kolory-0.1, 6, 0.3);
  [0, 1, 2, 3, 4].forEach(function (i) {
    arr("#cw" + i, @kolory-0.04 + i * 0.07, {s: 0.3, y: 20, d: 0.75});
    bin("#cx" + i, @kolory+0.25 + i * 0.07, 6, 0.3);
  });
  bin("#cm3", @shryfty-0.1, 6, 0.3);
  arr("#cAa", @shryfty-0.04, {s: 0.6, y: 30, d: 0.8});
  [0, 1, 2].forEach(function (i) { arr("#cwt" + i, @shryfty+0.14 + i * 0.1, {s: 0.7, x: -30, y: 0, d: 0.6}); });
  bin("#cPS", @shryfty+0.45, 6, 0.3);
  bin("#cm4", @te-0.08, 6, 0.3);
  arr("#cPh", @te-0.04, {s: 0.6, y: 30, d: 0.8});
  tl.set("#cPhH", {autoAlpha: 1}, @tekst-0.06);
  tl.fromTo("#cPhH", {clipPath: "inset(0% 100% 0% 0%)"}, {clipPath: "inset(0% 0% 0% 0%)", duration: 0.4, ease: "power2.out", immediateRender: false}, @tekst-0.06);
  arr(["#cPhB", "#cPhT"], @ekrani-0.04, {s: 0.6, y: 10, d: 0.55});
  /* the sheet folds into the card near her, the iris closes onto it */
  bout(["#cPh", "#cm4"], @ekranie-0.04, 10, 0.24);
  tl.to("#cS", {scale: 0.2, autoAlpha: 0.6, duration: 0.5, ease: "power3.in"}, @i1-0.32);
  G.irisClose("#gC", @i1-0.26, 540, 330, 0.5);""")


# ===========================================================================
# C2 + D · NEAR — the carousel from a skeleton, then the reel from the AI
@beat
def k_formats():
    skel = ('<div class="skl hide" id="kSk" style="left:120px;top:195px;width:200px;height:250px">'
            '<i class="hb" id="kb0" style="left:20px;top:26px;width:130px;height:24px"></i>'
            '<i class="rr" id="kb1" style="left:20px;top:76px;width:160px;height:14px"></i>'
            '<i class="rr" id="kb2" style="left:20px;top:102px;width:148px;height:14px"></i>'
            '<i class="rr" id="kb3" style="left:20px;top:128px;width:112px;height:14px"></i>'
            '<i class="rr" id="kb4" style="left:20px;top:154px;width:70px;height:14px"></i>'
            '<i class="hb" id="kb5" style="left:20px;top:196px;width:60px;height:24px;border-radius:12px"></i></div>')
    svg = ('<svg class="abs" width="1080" height="700" viewBox="0 0 1080 700" style="left:0;top:0;overflow:visible">'
           '<path class="strm hide" id="kS1" d="M322 300 C 360 238 404 238 444 292"/>'
           '<path class="strm hide" id="kS2" d="M636 292 C 676 238 718 238 758 300"/>'
           '<path class="brk hide" id="kBr" d="M150 500 L150 534 Q150 548 164 548 L916 548 Q930 548 930 534 L930 500"/>'
           '</svg>'
           '<svg class="cab abs" width="1080" height="700" viewBox="0 0 1080 700" style="left:0;top:0">'
           '<path class="tube hide" id="kT1" d="M634 300 C 690 280 735 280 790 300"/>'
           '<path class="core hide" id="kC1" d="M634 300 C 690 280 735 280 790 300"/>'
           '<path class="tube hide" id="kT2" d="M446 300 C 400 280 352 280 310 300"/>'
           '<path class="core hide" id="kC2" d="M446 300 C 400 280 352 280 310 300"/>'
           '<g class="pkg"><path class="pkt" id="kP1" style="opacity:0" d="M634 300 C 690 280 735 280 790 300"/></g></svg>')
    L.append(
        '<div class="g full" id="gK">'
        '<div class="shelf edge hide" id="kSh" style="left:60px;top:150px;width:960px;height:470px"></div>'
        + skel
        + '<div class="dash hide" id="kFr" style="left:760px;top:195px;width:200px;height:250px;border-radius:16px"></div>'
        + slide("kF1", "wb06-s", 716, 206, 200, rot=-7) + slide("kF2", "wb07-s", 804, 206, 200, rot=7)
        + slide("kF0", "wb04-s", 760, 195, 200)
        + tile("kOk", 70, 928, 168, "jelly", stroke("check"), extra_cls="circ", ring=False)
        + slide("kCa", "wb04-s", 110, 195, 200)
        + phone("kPh", 790, 160, 0.6, img="r1", ov=True, ov_hide=True)
        + svg
        + tile("kAI", 190, 445, 205, "jelly", '<span class="wmark" style="font-size:88px">ШІ</span>')
        + dscard("kDS", 442, 200, 0.75, ring=True)
        + chip("kC5", 540, 470, "5 хв", clock("kC5h"))
        + '</div>')
    sfx("pop", T["zrobyty"], -2)
    sfx("click", T["p5"])
    sfx("pop", T["hotova"])
    sfx("pop", T["rils"], -1)
    sfx("pop", T["shtuch"], -2)
    sfx("click-soft", T["nakl"], -1)
    return js("""
  tl.set("#gK", {autoAlpha: 1}, @i1-0.3);
  arr("#kSh", @i1-0.2, {s: 0.85, y: 20, d: 0.8});
  arr("#kDS", @i1-0.12, {s: 0.55, y: 0, d: 0.8});
  /* «зробити карусель»: a text skeleton in, an empty slide frame out */
  arr("#kSk", @zrobyty-0.06, {s: 0.5, x: -30, y: 20});
  tl.fromTo("#kFr", {autoAlpha: 0, scale: 0.8}, {autoAlpha: 1, scale: 1, duration: 0.5, ease: SP}, @karusel2-0.04);
  /* «заливаю туди скелет з текстом»: the text pours into the system */
  tl.set("#kS1", {autoAlpha: 1}, @zalyv-0.02); draw2("kS1", @zalyv-0.02, 0.4);
  tl.to(["#kb0", "#kb1", "#kb2", "#kb3", "#kb4", "#kb5"], {scaleX: 0, duration: 0.32, ease: "power2.in", stagger: 0.16}, @zalyv+0.25);
  G.bump("#kDS", @tekstom+0.2); G.ripple("#kDSR", @tekstom+0.2);
  bout(["#kSk", "#kS1"], @za5-0.08, 8, 0.3);
  /* «за 5 хвилин вона готова» */
  arr("#kC5", @p5-0.1, {s: 0.4, y: 16, d: 0.65});
  tl.fromTo("#kC5h", {rotation: 0}, {rotation: 360, svgOrigin: "12 12", duration: 0.8, ease: "power2.inOut"}, @p5+0.05);
  tl.set("#kS2", {autoAlpha: 1}, @vona-0.06); draw2("kS2", @vona-0.06, 0.3);
  bout("#kFr", @hotova+0.1, 6, 0.2);
  arr("#kF1", @hotova-0.08, {s: 0.5, x: -40, y: 10, d: 0.7});
  arr("#kF2", @hotova, {s: 0.5, x: 40, y: 10, d: 0.7});
  arr("#kF0", @hotova+0.08, {s: 0.5, y: 20, d: 0.75});
  arr("#kOk", @hotova+0.3, {s: 0.2, y: 0, d: 0.55});
  /* «а коли треба змонтувати рілс» */
  bout(["#kF0", "#kF1", "#kF2", "#kOk", "#kS2", "#kC5"], @akoly-0.18, 10, 0.28);
  arr("#kPh", @rils-0.14, {s: 0.5, y: 30, d: 0.8});
  G.bump("#kDS", @tasama); G.ripple("#kDSR", @tasama);
  /* «в штучному інтелекті»: the system docks into the AI */
  arr("#kAI", @shtuch-0.06, {s: 0.3, y: 20, d: 0.8});
  G.ripple("#kAIR", @shtuch+0.3);
  tl.to("#kDS", {x: 104, y: -96, scale: 0.36, duration: 0.6, ease: SP}, @shtuch-0.12);
  G.bump("#kAI", @znaie);
  /* «як має виглядати накладений текст» */
  tl.set(["#kT1", "#kC1"], {autoAlpha: 1}, @vyhl-0.12);
  draw2("kT1", @vyhl-0.12, 0.4); draw2("kC1", @vyhl-0.12, 0.4);
  G.packet("kP1", @nakl-0.3, 0.45);
  tl.set("#kPhH", {autoAlpha: 1}, @nakl);
  tl.fromTo("#kPhH", {clipPath: "inset(0% 100% 0% 0%)"}, {clipPath: "inset(0% 0% 0% 0%)", duration: 0.45, ease: "power2.out", immediateRender: false}, @nakl);
  arr(["#kPhB", "#kPhT"], @tekst2-0.04, {s: 0.6, y: 10, d: 0.55});
  /* «один впізнаваний стиль»: the slide comes back, one bracket under both */
  tl.set(["#kT2", "#kC2"], {autoAlpha: 1}, @odyn-0.2);
  draw2("kT2", @odyn-0.2, 0.4); draw2("kC2", @odyn-0.2, 0.4);
  arr("#kCa", @odyn-0.06, {s: 0.5, x: 30, y: 10, d: 0.8});
  tl.set("#kBr", {autoAlpha: 1}, @vpizn); draw2("kBr", @vpizn, 0.6);
  shn("#kCa .sheen", @styl2-0.05); shn("#kPh .sheen", @styl2-0.05);
  G.bump("#kPh", @rils2); G.bump("#kCa", @karusel3);
  bout(["#kSh", "#kCa", "#kPh", "#kT1", "#kC1", "#kT2", "#kC2", "#kBr", "#kDS"], @tobto-0.2, 10, 0.28);
  tl.to("#kAI", {scale: 0.6, autoAlpha: 0, duration: 0.3, ease: "power2.in"}, @tobto-0.12);
  tl.set("#gK", {autoAlpha: 0}, @tobto+0.3);""")


# ===========================================================================
# F · OVER — two prompts collapse into one system that pours into two formats
def pbar(pid, top, glyph, fmt):
    return ('<div class="pbar hide" id="%s" style="top:%dpx">'
            '<div class="tw circ" style="left:25px;top:25px;width:120px;height:120px"><div class="jelly">%s</div></div>'
            '<div class="chip hide" id="%sF">%s</div>'
            '<i class="pl" id="%sL1" style="top:56px;width:470px"></i>'
            '<i class="pl" id="%sL2" style="top:94px;width:330px;height:18px"></i>'
            '<div class="tw circ" style="left:865px;top:30px;width:110px;height:110px"><div class="jelly">%s</div></div>'
            '</div>' % (pid, top, stroke(glyph), pid, fmt, pid, pid, stroke("up")))


@beat
def f_pour():
    v1 = ('<div class="ves hide" id="fV1" data-layout-allow-overflow style="left:-30px;top:620px;width:440px;height:550px">'
          '<div class="liq" id="fL1"></div><img id="fI1" src="assets/carousels/wb04-m.jpg" alt=""></div>')
    v2 = ('<div class="ves hide" id="fV2" data-layout-allow-overflow style="left:760px;top:610px;width:340px;height:604px;border-radius:44px">'
          '<div class="liq" id="fL2"></div><div class="abs" id="fI2" style="left:-5px;top:-5px">%s</div></div>'
          % phone("fPh", 0, 0, 1.1333, img="r1", ov=True, wrap=False))
    svg = ('<svg class="abs" width="1080" height="1240" viewBox="0 0 1080 1240" style="left:0;top:0;overflow:visible">'
           '<path class="strm big hide" id="fS1" d="M410 520 C 330 560 230 560 190 640"/>'
           '<path class="strm big hide" id="fS2" d="M670 520 C 770 556 900 556 930 630"/></svg>')
    L.append('<div class="g full" id="gF"><div class="tkg"></div><div class="aurs"></div><div class="grain"></div>'
             + pbar("fB1", 300, "carousel", "4:5") + pbar("fB2", 540, "reel", "9:16")
             + v1 + v2 + svg
             + dscard("fDS", 280, 160, 2.0, ring=True)
             + '</div>')
    sfx("whoosh-short", T["tobto"] - 0.12)
    sfx("pop", T["dva"], -1)
    sfx("typing", T["promty"], -4)
    sfx("pop", T["odyn2"])
    sfx("whoosh-short", T["to1"] - 0.15, -4)
    sfx("whoosh-short", T["takym"] + 0.05, -3)
    return js("""
  G.irisOpen("#gF", @tobto-0.12, 540, 300, 0.85);
  drift1("#gF", @tobto, 9.4);
  arr("#fB1", @dva-0.06, {s: 0.7, y: 40, d: 0.8});
  arr("#fB2", @dva+0.08, {s: 0.7, y: 40, d: 0.8});
  tl.to("#fB1", {y: -34, duration: 0.6, ease: SP}, @okremykh+0.08);
  tl.to("#fB2", {y: 34, duration: 0.6, ease: SP}, @okremykh+0.08);
  tl.fromTo(["#fB1L1", "#fB1L2", "#fB2L1", "#fB2L2"], {scaleX: 0}, {scaleX: 1, duration: 0.45, ease: "power2.out", stagger: 0.12}, @promty-0.04);
  arr("#fB1F", @kozhen-0.04, {s: 0.4, y: 0, d: 0.55});
  arr("#fB2F", @format2-0.04, {s: 0.4, y: 0, d: 0.55});
  /* «а один раз зроблена система» */
  tl.to("#fB1", {y: 120, scale: 0.4, autoAlpha: 0, duration: 0.38, ease: "power2.in"}, @a2-0.06);
  tl.to("#fB2", {y: -120, scale: 0.4, autoAlpha: 0, duration: 0.38, ease: "power2.in"}, @a2-0.06);
  gsap.set("#fDS", {transformOrigin: "50% 50%"});
  arr("#fDS", @odyn2-0.04, {s: 0.3, y: 0, d: 0.9});
  G.ripple("#fDSR", @odyn2+0.35);
  shn("#fDS .sheen", @zrobl);
  /* «яка потім просто переливається то в одне, то в інше» */
  tl.to("#fDS", {y: -150, scale: 0.62, duration: 0.75, ease: SP}, @potim-0.05);
  arr("#fV1", @prosto-0.1, {s: 0.85, x: -20, y: 40, d: 0.8});
  arr("#fV2", @prosto+0.02, {s: 0.85, x: 20, y: 40, d: 0.8});
  gsap.set(["#fI1", "#fI2"], {autoAlpha: 0});
  gsap.set(["#fL1", "#fL2"], {clipPath: "inset(100% 0% 0% 0%)"});
  tl.to("#fDS", {rotation: -11, duration: 0.45, ease: "power2.out"}, @perelyv+0.05);
  tl.set("#fS1", {autoAlpha: 1}, @to1-0.16); draw2("fS1", @to1-0.16, 0.3);
  tl.to("#fL1", {clipPath: "inset(0% 0% 0% 0%)", duration: 0.5, ease: "power1.inOut"}, @to1-0.02);
  tl.to("#fI1", {autoAlpha: 1, duration: 0.3}, @odne+0.12);
  tl.to("#fV1", {borderColor: "rgba(255,255,255,0)", duration: 0.3}, @odne+0.12);
  tl.to("#fS1", {autoAlpha: 0, duration: 0.2}, @odne+0.15);
  tl.to("#fDS", {rotation: 11, duration: 0.5, ease: "power2.inOut"}, @to2-0.3);
  tl.set("#fS2", {autoAlpha: 1}, @to2-0.14); draw2("fS2", @to2-0.14, 0.3);
  tl.to("#fL2", {clipPath: "inset(0% 0% 0% 0%)", duration: 0.45, ease: "power1.inOut"}, @to2+0.02);
  tl.to("#fI2", {autoAlpha: 1, duration: 0.25}, @inshe+0.02);
  tl.to("#fV2", {borderColor: "rgba(255,255,255,0)", duration: 0.25}, @inshe+0.02);
  tl.to("#fS2", {autoAlpha: 0, duration: 0.2}, @inshe+0.05);
  tl.to("#fDS", {rotation: 0, duration: 0.4, ease: SP}, @inshe+0.2);
  tl.to("#fDS", {y: -300, scale: 0.3, duration: 0.55, ease: "power3.inOut"}, @takym-0.05);
  G.irisClose("#gF", @takym+0.05, 540, 180, 0.5);""")


# ===========================================================================
# G · NEAR — the card fans out: carousel, reel, presentations, guides, banners
GI = {  # id: (x, y, w, h)
    "gCa": (73, 315, 136, 170), "gPh": (243, 310, 102, 181), "gPr": (379, 338, 220, 124),
    "gGd": (633, 315, 130, 170), "gBn": (797, 360, 210, 80),
}


@beat
def g_anything():
    hub = (540, 268)
    wires = ""
    for i, key in enumerate(("gCa", "gPh", "gPr", "gGd", "gBn")):
        x, y, w, h = GI[key]
        tx, ty = x + w // 2, y
        wires += ('<path class="wire hide" id="gW%d" d="M%d %d C %d %d %d %d %d %d"/>'
                  % (i, hub[0], hub[1], hub[0], hub[1] + 40, tx, ty - 50, tx, ty - 4))
    pres = ('<div class="prs hide" id="gPr" style="left:379px;top:338px;width:220px;height:124px">'
            '<i class="hb" style="left:16px;top:16px;width:96px"></i>'
            '<i class="rr" style="left:16px;top:42px;width:110px"></i><i class="rr" style="left:16px;top:58px;width:84px"></i>'
            '<i class="rr" style="left:16px;top:74px;width:96px"></i>'
            '<i class="bar" style="left:144px;height:36px"></i><i class="bar" style="left:170px;height:58px"></i>'
            '<i class="bar" style="left:196px;width:12px;height:80px;opacity:0"></i>'
            '<div class="sheen"></div></div>')
    pres = pres.replace('<i class="bar" style="left:196px;width:12px;height:80px;opacity:0"></i>', '')
    guide = ('<div class="gd hide" id="gGd" style="left:633px;top:315px;width:130px;height:170px">'
             '<i class="sp"></i><div class="ga">А<span style="color:#b4122f">а</span></div>'
             '<i class="hb" style="left:32px;top:104px;width:70px"></i>'
             '<i class="rr" style="left:32px;top:128px;width:80px"></i><i class="rr" style="left:32px;top:144px;width:58px"></i>'
             '<div class="sheen"></div></div>')
    banner = ('<div class="bn hide" id="gBn" style="left:797px;top:360px;width:210px;height:80px">'
              '<i class="ph" style="left:18px;top:20px;width:104px"></i>'
              '<i class="pr" style="left:18px;top:46px;width:84px"></i>'
              '<i class="pl" style="left:138px;top:24px;width:56px;height:32px"></i><div class="sheen"></div></div>')
    ghosts = ""
    for i, (x, y, w, h, r) in enumerate(((282, 118, 76, 76, "50%"), (372, 176, 64, 64, "16px"),
                                         (650, 108, 50, 89, "12px"), (720, 170, 110, 62, "14px"))):
        ghosts += ('<div class="gh hide" id="gG%d" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx;border-radius:%s">%s</div>'
                   % (i, x, y, w, h, r, stroke("plus")))
    L.append('<div class="g full" id="gG">'
             '<svg class="cab abs" width="1080" height="700" viewBox="0 0 1080 700" style="left:0;top:0">%s</svg>'
             % wires
             + slide("gCa", "wb04-s", 73, 315, 136)
             + phone("gPh", 243, 310, 0.34, img="r1", ov=True)
             + pres + guide + banner
             + label("gLp", 489, 505, u"презентації", 260) + label("gLg", 698, 505, u"гайди", 200)
             + label("gLb", 902, 505, u"банери", 220)
             + ghosts + dscard("gDS", 469, 92, 0.55, ring=True) + '</div>')
    sfx("pop", T["karuseli2"], -3)
    sfx("click-soft", T["prez"], -1)
    sfx("click-soft", T["banery"], -1)
    return js("""
  tl.set("#gG", {autoAlpha: 1}, @takym+0.1);
  arr("#gDS", @takym+0.18, {s: 0.5, y: 60, d: 0.8});
  function out(i, sel, t) {
    tl.set("#gW" + i, {autoAlpha: 1}, t - 0.12); draw2("gW" + i, t - 0.12, 0.35);
    arr(sel, t, {s: 0.4, y: 30, d: 0.75});
  }
  out(0, "#gCa", @karuseli2-0.05);
  out(1, "#gPh", @montazh2-0.05);
  out(2, "#gPr", @prez-0.06); arr("#gLp", @prez+0.06, {s: 0.5, y: 10, d: 0.55});
  out(3, "#gGd", @haidy-0.06); arr("#gLg", @haidy+0.06, {s: 0.5, y: 10, d: 0.55});
  out(4, "#gBn", @banery-0.06); arr("#gLb", @banery+0.06, {s: 0.5, y: 10, d: 0.55});
  G.bump("#gDS", @shchos2); G.ripple("#gDSR", @shchos2);
  [0, 1, 2, 3].forEach(function (i) { arr("#gG" + i, @shchos2+0.05 + i * 0.07, {s: 0.3, y: 0, d: 0.6}); });
  bout("#gG", @i3-0.24, 10, 0.24);""")


# ===========================================================================
# H · NEAR — all her content, one brand
WALL = [("s", "wb01-s"), ("r", "r2"), ("s", "wb04-s"), ("s", "wb06-s"), ("s", "wb08-s"),
        ("s", "wb02-s"), ("s", "wb05-s"), ("r", "r3"), ("s", "wb03-s"), ("s", "wb12-s")]


@beat
def h_wall():
    cells = ""
    for n, (kind, src) in enumerate(WALL):
        c, r = n % 5, n // 5
        x, y = 91 + c * 182, 158 + r * 224
        if kind == "s":
            cells += slide("hW%d" % n, src, x, y, 170)
        else:
            cells += ('<div class="slw hide" id="hW%d" style="left:%dpx;top:%dpx;width:170px;height:212px">'
                      '<img src="assets/her/%s.jpg" alt="" style="object-position:50%% 30%%"><div class="cvs"></div>'
                      '<div class="cvh">одна<br>система</div><svg class="cvp" viewBox="0 0 24 24">%s</svg>'
                      '<div class="sheen"></div></div>' % (n, x, y, src, STROKES["play"]))
    L.append('<div class="g full" id="gH">'
             '<div class="shelf edge hide" id="hS" style="left:70px;top:140px;width:940px;height:488px"></div>'
             + cells
             + '<div class="abs" id="hSh" style="left:70px;top:140px;width:940px;height:488px;border-radius:80px">'
               '<div class="shc"><div class="sheen"></div></div></div></div>')
    sfx("whoosh-short", T["i3"], -3)
    sfx("sparkle", T["odyn3"], -2)
    return js("""
  tl.set("#gH", {autoAlpha: 1}, @i3-0.15);
  arr("#hS", @i3-0.12, {s: 0.85, y: 20, d: 0.8});
  for (var n = 0; n < 10; n++) {
    var c = n % 5, r = Math.floor(n / 5);
    arr("#hW" + n, @i3+0.02 + Math.abs(c - 2) * 0.08 + r * 0.1, {s: 0.4, y: 30, d: 0.75});
  }
  tl.to("#gH .slw", {scale: 1.05, duration: 0.12, ease: "power2.out", stagger: 0.03}, @kontent);
  tl.to("#gH .slw", {scale: 1, duration: 0.4, ease: SP, stagger: 0.03}, @kontent+0.12);
  shn("#hSh .sheen", @odyn3-0.05);
  bout("#gH", @brend-0.04, 10, 0.26);
  tl.set("#gH", {autoAlpha: 0}, @brend+0.26);""")


# ===========================================================================
# I · NEAR — the guide: build the system in 15 minutes, from your own brand
@beat
def i_guide():
    dots = "".join('<i class="d" style="left:%dpx;background:%s"></i>' % (30 + i * 50, c) for i, c in enumerate(SW4))
    book = ('<div class="tw hide" id="iG" style="left:120px;top:195px;width:260px;height:340px"><div class="bk">'
            '<div class="bt">гайд</div><div class="bm">ДИЗАЙН-СИСТЕМА</div>%s'
            '<i class="r" style="top:270px;width:170px"></i><i class="r" style="top:294px;width:120px"></i>'
            '<div class="sheen"></div></div></div>' % dots)
    cab = ('<svg class="cab abs" width="1080" height="700" viewBox="0 0 1080 700" style="left:0;top:0">'
           '<path class="tube hide" id="iT" d="M386 350 C 480 316 600 316 696 350"/>'
           '<path class="core hide" id="iC" d="M386 350 C 480 316 600 316 696 350"/>'
           '<g class="pkg"><path class="pkt" id="iP" style="opacity:0" d="M386 350 C 480 316 600 316 696 350"/></g></svg>')
    L.append('<div class="g full" id="gI">'
             '<div class="shelf edge hide" id="iS" style="left:70px;top:150px;width:940px;height:470px"></div>'
             + cab + book + dscard("iDS", 700, 213, 0.95, ring=True, parts=True)
             + chip("iC15", 541, 400, "15 хв", clock("iC15h"))
             + '<div class="tag hide" id="iTg" style="left:776px;top:478px">твій бренд</div></div>')
    sfx("pop", T["zrobyla"], -1)
    sfx("click", T["p15"])
    sfx("click-soft", T["vlasn"], -2)
    return js("""
  tl.set("#gI", {autoAlpha: 1}, @zrobyla-0.3);
  arr("#iS", @zrobyla-0.25, {s: 0.85, y: 20, d: 0.8});
  arr("#iG", @zrobyla-0.06, {s: 0.4, y: 40, d: 0.85});
  shn("#iG .sheen", @haid+0.1);
  /* «як зібрати таку систему»: the card assembles out of its parts */
  tl.set(["#iT", "#iC"], {autoAlpha: 1}, @zibraty-0.15);
  draw2("iT", @zibraty-0.15, 0.45); draw2("iC", @zibraty-0.15, 0.45);
  G.packet("iP", @zibraty+0.2, 0.45);
  gsap.set("#iDS .p", {autoAlpha: 0});
  arr("#iDS", @zibraty+0.05, {s: 0.6, y: 20, d: 0.75});
  var PO = [[-90, -60, -20], [110, -40, 25], [-120, 50, 30], [-40, 90, -25], [60, 110, 20], [140, 40, -30], [-80, 120, 15], [100, -90, -15]];
  gsap.utils.toArray("#iDS .p").forEach(function (el, i) {
    var o = PO[i % PO.length];
    tl.fromTo(el, {x: o[0], y: o[1], rotation: o[2], scale: 0.5, autoAlpha: 0},
              {x: 0, y: 0, rotation: 0, scale: 1, autoAlpha: 1, duration: 0.6, ease: SP, immediateRender: false}, @zibraty+0.3 + i * 0.07);
  });
  G.ripple("#iDSR", @systemu+0.3);
  /* «за 15 хвилин» */
  arr("#iC15", @p15-0.1, {s: 0.4, y: 16, d: 0.65});
  tl.fromTo("#iC15h", {rotation: 0}, {rotation: 360, svgOrigin: "12 12", duration: 0.8, ease: "power2.inOut"}, @p15+0.05);
  /* «виходячи з власного бренду» */
  gsap.set("#iTg", {rotation: -5});
  arr("#iTg", @vlasn-0.06, {s: 0.4, y: 20, d: 0.7});
  tl.to("#iDS .sw", {scale: 1.25, duration: 0.12, ease: "power2.out", stagger: 0.05}, @brendu);
  tl.to("#iDS .sw", {scale: 1, duration: 0.4, ease: SP, stagger: 0.05}, @brendu+0.12);
  bout("#gI", @napyshy-0.22, 10, 0.24);
  tl.set("#gI", {autoAlpha: 0}, @napyshy+0.04);""")


# ===========================================================================
# J · NEAR — comment «система», the guide arrives in a DM
@beat
def j_cta():
    box = ('<div class="dglass edge hide" id="jC" style="left:60px;top:380px;width:960px;height:150px;border-radius:75px">'
           '<div class="tw circ" style="left:27px;top:27px;width:96px;height:96px"><div class="pearl">%s</div></div>'
           '<div id="jPh">Додайте коментар…</div><div id="jTx"></div>'
           '<div class="tw circ" id="jS" style="left:837px;top:27px;width:96px;height:96px"><div class="jelly">%s</div></div>'
           '<div class="ck" id="jK" style="left:885px;top:75px"></div>'
           '<div class="shc"><div class="sheen"></div></div></div>' % (stroke("person"), stroke("up")))
    dm = ('<div class="dm hide" id="jD" style="left:230px;top:150px;width:620px;height:190px">'
          '<div class="mb"><span>гайд</span></div>'
          '<div class="pi">%s</div>'
          '<i class="r" style="left:244px;top:44px;width:250px"></i>'
          '<i class="r" style="left:172px;top:112px;width:380px"></i><i class="r" style="left:172px;top:140px;width:260px"></i>'
          '<div class="shc"><div class="sheen"></div></div></div>' % stroke("plane"))
    L.append('<div class="g full" id="gJ">' + box + dm + '</div>')
    sfx("pop", T["napyshy"], -2)
    sfx("typing", T["syst"] - 0.05, -2)
    sfx("click", T["syste"])
    sfx("notification", T["tobi"] - 0.05, -1)
    return js("""
  tl.set("#gJ", {autoAlpha: 1}, @napyshy-0.12);
  arr("#jC", @napyshy-0.06, {s: 0.8, y: 40, d: 0.8});
  tl.set("#jPh", {autoAlpha: 0}, @syst-0.08);
  G.bump("#jS", @syste);
  tl.fromTo("#jK", {scale: 0.3, autoAlpha: 0.95}, {scale: 1.6, autoAlpha: 0, duration: 0.6, ease: "power2.out", immediateRender: false}, @syste+0.02);
  arr("#jD", @tobi-0.08, {s: 0.5, y: 40, d: 0.8});
  shn("#jD .sheen", @skynu);""")


# ---------------------------------------------------------------------------
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
  function draw2(id, t, d) {
    var L = document.getElementById(id).getTotalLength() + 3;
    tl.fromTo("#" + id, {strokeDasharray: (L - 3) + " " + (L + 40), strokeDashoffset: L},
              {strokeDashoffset: 0, duration: d || 0.5, ease: "power2.inOut", immediateRender: false}, t);
    gsap.set("#" + id, {strokeDasharray: (L - 3) + " " + (L + 40), strokeDashoffset: L});
  }
  function shn(sel, t) {
    gsap.set(sel, {xPercent: -120});
    tl.fromTo(sel, {xPercent: -120}, {xPercent: 120, duration: 0.8, ease: "power2.inOut", immediateRender: false}, t);
  }
  function drift1(sel, t, d) { tl.fromTo(sel + " .aurs", {x: 0, y: 0}, {x: -110, y: 70, duration: d, ease: "sine.inOut"}, t); }
  gsap.set(".sheen", {xPercent: -120});
"""


def typing_js():
    """The comment types itself, driven from one clock so any frame renders cold."""
    txt = u"система"
    t0, t1 = T["syst"] - 0.06, T["syst"] + 0.42
    return r"""
  var CLK = {t: 0}, PB = document.getElementById("jTx"), PTXT = %s, PCUR = null;
  function paintAll() {
    var t = CLK.t, n = t <= %.3f ? 0 : t >= %.3f ? PTXT.length : Math.round(PTXT.length * (t - %.3f) / %.3f);
    if (n !== PCUR) { PCUR = n; PB.textContent = PTXT.slice(0, n); }
  }
  tl.fromTo(CLK, {t: 0}, {t: %.3f, duration: %.3f, ease: "none", onUpdate: paintAll}, 0);""" % (
        json.dumps(txt, ensure_ascii=False), t0, t1, t0, t1 - t0, DUR, DUR)


# captions that would repeat the graphic's own words (STYLE.md §2b.1)
def span_words(a, b):
    return (round(a - 0.02, 3), round(b, 3), "")


BLACKOUT = [
    span_words(T["dsys"], T["dsyse"]),                 # the card's label says ДИЗАЙН-СИСТЕМА
    span_words(T["hod1"], T["hod1e"]),                 # the chip says «1 год»
    span_words(T["hod2"], T["hod2e"]),                 # the chip says «1 год»
    span_words(T["dsys2"], T["ekranie"] + 0.03),       # the sheet's heading and section labels
    span_words(T["p5"], T["khve"]),                    # the chip says «5 хв»
    span_words(T["systema2"], T["systema2e"]),         # the big card's label says it
    span_words(T["prez"], T["preze"]),                 # the labels say «презентації»
    span_words(T["haidy"], T["haidye"]),               #   «гайди»
    span_words(T["banery"], T["banerye"]),             #   «банери»
    span_words(T["haid"], T["haide"]),                 # the cover says «гайд»
    span_words(T["p15"], T["khv15e"]),                 # the chip says «15 хв»
    span_words(T["brendu"], T["brendue"]),             # the tag says «твій бренд»
    span_words(T["syst"], T["syste"]),                 # the comment box types «система»
]


def check_no_paint():
    """No beat may be on screen inside her closeup."""
    a, b = NO_PAINT[0]
    assert T["brend"] + 0.26 < a, "the wall runs into the closeup"
    assert T["zrobyla"] - 0.3 >= b - 0.001, "the guide arrives inside the closeup"
    for c in SFX:
        assert not (a - 0.05 <= c["t"] <= b), ("sfx inside the closeup", c)


def main():
    gj = []
    for fn in BEATS:
        j = fn()
        gj.append("  /* %s */" % fn.__name__)
        gj.append(j.rstrip())
    check_no_paint()
    rot = "\n".join('  gsap.set("#%s", {rotation: %s});' % (i, r) for i, r in sorted(ROT.items()))
    push = ["#vid"]
    head = [g.js(), HEAD_JS, rot, typing_js(),
            '  gsap.set(%s, {transformOrigin: "540px 900px"});' % json.dumps(push),
            '  tl.fromTo(%s, {scale: 1}, {scale: 1.045, duration: %.3f, ease: "none"}, 0);' % (json.dumps(push), DUR)]
    doc = k.document(
        title=u"Reel 29 — одна дизайн-система, два формати",
        plate="assets/base.mp4",
        gfx_html=g.defs() + "\n" + "\n".join(L),
        gfx_js="\n".join(head + gj),
        caps=CAPS,
        blackout=BLACKOUT,
        scrim_off=[(T["prez"] - 0.02, T["banerye"], "")],
    )
    io.open(os.path.join(HERE, "index.html"), "w", encoding="utf-8").write(doc)
    SFX.sort(key=lambda c: c["t"])
    io.open(os.path.join(HERE, "sfx.json"), "w", encoding="utf-8").write(json.dumps(SFX, indent=1))
    print("index.html  %d captions, %d beats, %d sfx cues (%.2f/s)" % (len(CAPS), len(BEATS), len(SFX), len(SFX) / DUR))


main()
