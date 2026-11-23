# -*- coding: utf-8 -*-
"""Reel 37 — «А якщо я перестану з тобою працювати?». Posts 2026-10-16.

Raw take, cut by tools/cut.py (work/r37/cut.json). Refined glass (STYLE.md §0),
sound design (tools/sfx.py), expert reel -> full near -> over -> near chain.

The one object is **the system** — a Claude hub with a cable to the person who
set it up. The hook unplugs that cable and the hub shakes («все зламається?»);
the answer unplugs it again and the hub keeps its pulse («ні, не зламається»).

Chain:  near: her tile -- cable -- the hub; the cable is pulled, the hub shakes,
a «?» -> more «?» around it (she hears it all the time) -> the hub moves to the
centre, two apps snap onto it, a key turns under it (AI-producer під ключ) ->
three chips: SMM-агенції / блогерки / підприємниці -> the iris opens out of the
hub: a team board, four columns ticking content, the team lights up, 24/7 and a
moon -> the team collapses into one slot, it fills as Claude, two apps join ->
the iris closes onto Claude -> near: the same hub on a shelf, a pulse draws
under it (it lives on its own) -> it slides aside, her tile plugs in, a spinner
waits for her update -> «ні»: she unplugs, the hub comes back, the pulse keeps
going, a check -> a ring closes round the hub (fully set up), the wrench is
struck out -> the iris opens out of the hub: arrows turn round Claude (it
updates itself), content cards fly into it, a profile fills, a curve rises ->
the iris closes -> near: a doc card, one line edited, a «!» flips to a check
-> the iris opens: the turnkey system's list ticks line by line, «+» goes into
a comment.

usage: python build.py   (then: python ../tools/sfx.py mix 37)
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

CUT = json.load(io.open(os.path.join(ROOT, "work", "r37", "cut.json"), encoding="utf-8"))
DUR = 49.850           # (1496 plate frames - 0.5) / 30, floored
FPS = 30
k = Kit(width=1080, height=1920, fps=FPS, duration=DUR)
g = Glass(["claude", "notion", "canva"])
k.css(g.css())

# NO-PAINT: the closeups cut.py punched in. Captions only.
NO_PAINT = [tuple(x) for x in CUT["no_paint"]]

# ---------------------------------------------------------------------------
# Captions: script spelling on her timing. Whisper errors among the "she
# improvised" lines get the script word back (align.txt).
CAPS = k.load_captions(os.path.join(ROOT, "work", "r37", "captions.json"))
FIX = {u"лежити": u"жити", u"оновлювання.": u"оновлю.", u"якось": u"якусь"}
_out = []
for i, c in enumerate(CAPS):
    w = c["w"]
    if w == u"що" and abs(c["s"] - 10.04) < 0.05:
        w = u"щоб"                                   # «щоб вони могли»
    if w == u"є" and abs(c["s"] - 23.34) < 0.05:
        w = u"я"                                     # «поки я щось оновлю»
    if w == u"це." and _out and _out[-1]["w"] == u"зламай":
        _out[-1]["w"] = u"зламається."               # «зламай це» -> «зламається.»
        _out[-1]["e"] = c["e"]
        continue
    c["w"] = FIX.get(w, w)
    _out.append(c)
CAPS = _out
for _a, _b in zip(CAPS, CAPS[1:]):
    _a["e"] = round(max(_a["s"] + 0.10, _b["s"] - 0.085), 3)


def _n(s):
    return "".join(ch for ch in s.lower() if ch.isalnum())


def _hits(word):
    return [c for c in CAPS if _n(word) in [_n(x) for x in c["w"].split()]]


def S(word, near):
    c = min(_hits(word), key=lambda c: abs(c["s"] - near))
    assert abs(c["s"] - near) < 0.6, (word, near, c["s"])
    return c["s"]


def E(word, near):
    return min(_hits(word), key=lambda c: abs(c["s"] - near))["e"]


T = {
    "yakshcho": S(u"якщо", 0.0), "perestanu": S(u"перестану", 0.51), "pratsiuvaty": S(u"працювати", 1.17),
    "zlam": S(u"зламається", 2.23),
    "pytannia": S(u"питання", 3.44), "chuiu": S(u"чую", 4.08), "tomu1": S(u"тому", 4.66),
    "nalasht": S(u"налаштовую", 5.10), "ai": S(u"АІ-продюсера", 5.68), "pid": S(u"під", 6.33),
    "kliuch": S(u"ключ", 6.51), "dlia": S(u"для", 6.74),
    "smm": S(u"SMM-агенцій", 7.38), "blogerok": S(u"блогерок", 8.52), "pidpr": S(u"підприємниць", 9.10),
    "pidpre": E(u"підприємниць", 9.10),
    "shchob": S(u"щоб", 10.04), "stvor": S(u"створювати", 10.50), "kontent": S(u"контент", 11.04),
    "komanda": S(u"команда", 12.17), "n24": S("24", 12.59), "n7e": E("7", 13.25),
    "nikoly": S(u"ніколи", 13.55), "spyt": S(u"спить", 14.13),
    "naspr": S(u"насправді", 14.80), "pidpyska": S(u"підписка", 16.50), "claude": S("Claude", 17.06),
    "kilka": S(u"кілька", 17.40),
    "zvych": S(u"звичайно", 18.39), "systema": S(u"система", 20.30), "zhyty": S(u"жити", 20.84),
    "samost": S(u"самостійно", 21.16),
    "bez": S(u"без", 21.88), "chekaty": S(u"чекати", 22.64), "onovliu": S(u"оновлю", 23.70),
    "tomu2": S(u"тому", 24.38), "ni": S(u"ні", 25.26), "zlam2": S(u"зламається", 25.96),
    "yak": S(u"як", 26.86), "povnistiu": S(u"повністю", 27.66), "pidtrymka": S(u"підтримка", 29.28),
    "vona": S(u"вона", 29.85), "sama": S(u"сама", 30.39), "chym": S(u"чим", 31.43),
    "robysh": S(u"робиш", 31.99), "kontentu": S(u"контенту", 32.21), "vona2": S(u"вона", 33.09),
    "znaie": S(u"знає", 33.61), "tym3": S(u"тим", 34.33), "krashche": S(u"краще", 34.47),
    "yakshcho2": S(u"якщо", 35.40), "minim": S(u"мінімальну", 36.59), "pravku": S(u"правку", 37.07),
    "perestalo": S(u"перестало", 37.87), "zminyty": S(u"змінити", 39.80), "zahalom": S(u"загалом", 40.76),
    "treba": S(u"треба", 41.88), "trebae": E(u"треба", 41.88),
    "tomu3": S(u"тому", 42.47), "yakshcho3": S(u"якщо", 42.66), "tsikava": S(u"цікава", 43.16), "systema3": S(u"система", 43.56),
    "kliuch3": S(u"ключ", 44.13), "analiz": S(u"аналізує", 44.57), "tarhet": S(u"таргет", 45.62),
    "pyshe": S(u"пише", 46.13), "stsen": S(u"сценарії", 46.35), "dyzain": S(u"дизайнить", 46.77),
    "karus": S(u"каруселі", 47.25), "montuie": S(u"монтує", 47.73), "rilsy": S(u"рілси", 48.11),
    "stav": S(u"став", 48.73), "plius": S(u"плюс", 48.83), "koment": S(u"коментарі", 49.25),
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
# Sound design (tools/sfx.py). Quiet, on the event, never on her closeup.
SFX = []


def sfx(name, t, db=0):
    if isinstance(t, str):
        t = float(js(t))
    SFX.append({"t": round(max(0.0, t), 3), "name": name, "db": db})


# ---------------------------------------------------------------------------
# Glyphs
STROKES = {
    "up": '<path d="M12 19.2V5.4M6.2 11l5.8-5.8 5.8 5.8"/>',
    "check": '<path d="M5.4 12.6l4.3 4.3 8.9-9.5"/>',
    "person": '<circle cx="12" cy="8.2" r="3.6"/><path d="M4.8 20c.9-3.8 3.7-5.8 7.2-5.8s6.3 2 7.2 5.8"/>',
    "key": '<circle cx="7.6" cy="12" r="4"/><path d="M11.6 12h9.2M17.6 12v3.6M20.6 12v2.6"/>',
    "moon": '<path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9z"/>',
    "down": '<path d="M12 4v11M7 10.2l5 5 5-5M5 20h14"/>',
    "wrench": ('<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94'
               'l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/>'),
}


def stroke(name, cls="sk"):
    return '<svg class="%s" viewBox="0 0 24 24">%s</svg>' % (cls, STROKES[name])


def tile(tid, size, x, y, material, inner, extra_cls="", hide=True, ring=True):
    r = ('<div class="sqring%s" id="%sR" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx"></div>'
         % (" rnd" if "circ" in extra_cls else "", tid, x, y, size, size)) if ring else ""
    return ('%s<div class="tw%s %s" id="%s" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx">'
            '<div class="%s">%s<div class="sheen"></div></div></div>'
            % (r, " hide" if hide else "", extra_cls, tid, x, y, size, size, material, inner))


def glyph(ch, size, color="#fff"):
    return '<span class="wmark" style="font-size:%dpx;color:%s">%s</span>' % (size, color, ch)


k.css("""
.abs { position: absolute; }
.hide { opacity: 0; visibility: hidden; }
.tw { position: absolute; }
.sk { fill: none; stroke: url(#gw); stroke-width: 2.3; stroke-linecap: round; stroke-linejoin: round;
  width: 50%; height: 50%; position: relative; z-index: 1; overflow: visible; }
.pearl .sk { stroke: #17141c; }
.circ .jelly, .circ .pearl, .circ .clear, .circ .sheen { border-radius: 50%; }
.sqring.rnd { border-radius: 50%; }
.aurs { position: absolute; left: -700px; top: -700px; width: 2480px; height: 3320px; pointer-events: none;
  background:
    radial-gradient(circle 526px at 1560px 880px, rgba(255,110,156,0.50), rgba(255,110,156,0)),
    radial-gradient(circle 634px at 760px 2360px, rgba(222,32,74,0.55), rgba(222,32,74,0)),
    radial-gradient(circle 382px at 1480px 1910px, rgba(255,198,214,0.20), rgba(255,198,214,0)); }
.shc { position: absolute; inset: 0; border-radius: inherit; overflow: hidden; pointer-events: none; }
.shc .sheen { mix-blend-mode: normal; opacity: 0.4; }

/* the audience chips */
.chips { position: absolute; left: 0; width: 1080px; display: flex; justify-content: center; gap: 22px; }
.chip2 { position: relative; height: 92px; padding: 0 38px; border-radius: 46px; display: flex; align-items: center;
  font-size: 42px; font-weight: 700; letter-spacing: -0.01em; white-space: nowrap; }

/* cables and lines */
.pulse { fill: none; stroke: #ffd6e3; stroke-width: 9; stroke-linecap: round; stroke-linejoin: round;
  filter: drop-shadow(0 0 10px rgba(255,110,156,0.9)); }
.spin { position: absolute; fill: none; stroke: #ff8ab0; stroke-width: 9; stroke-linecap: round; stroke-dasharray: 70 40;
  filter: drop-shadow(0 0 10px rgba(255,110,156,0.8)); }
.ringP { fill: none; stroke: #ff8ab0; stroke-width: 11; stroke-linecap: round;
  filter: drop-shadow(0 0 12px rgba(255,110,156,0.9)); }
.strike { fill: none; stroke: #e0204b; stroke-width: 12; stroke-linecap: round; }

/* checklists */
.cbx { position: absolute; border-radius: 28%; box-shadow: inset 0 0 0 4px rgba(23,20,28,0.22); }
.cbf { position: absolute; inset: 0; border-radius: 28%;
  background: linear-gradient(165deg, #e0204b 0%, #8d0d24 100%); opacity: 0; visibility: hidden; }
.cbf svg { position: absolute; left: 14%; top: 14%; width: 72%; height: 72%; fill: none; stroke: #fff;
  stroke-width: 3.2; stroke-linecap: round; stroke-linejoin: round; }
.rr { position: absolute; display: block; border-radius: 12px; background: rgba(23,20,28,0.13); }
.hb { position: absolute; display: block; border-radius: 12px; background: linear-gradient(115deg, #c41434 0%, #8d0d24 100%); }
.fillb { position: absolute; display: block; border-radius: 12px; transform-origin: 0 50%;
  background: linear-gradient(115deg, #ff6e9c 0%, #e0204b 60%, #b4122f 100%); }

/* TK1: the team board */
.col { position: absolute; width: 220px; height: 440px; }
.t247 { position: absolute; font-size: 250px; font-weight: 900; letter-spacing: -0.05em; line-height: 1; text-align: center;
  background: linear-gradient(118deg, #7e0b20 0%, #b4122f 42%, #ff6e9c 100%);
  -webkit-background-clip: text; background-clip: text; color: transparent; padding-right: 12px; }

/* TK2: content cards, the curve */
.cc { position: absolute; border-radius: 26px; overflow: hidden;
  background: linear-gradient(172deg, #ffffff 0%, #fff9fb 55%, #fdf0f4 100%);
  box-shadow: inset 0 2px 1px #fff, 0 30px 60px -24px rgba(8,0,3,0.7); }
.cc i { position: absolute; display: block; }
.cc .im { left: 10px; top: 10px; right: 10px; border-radius: 18px;
  background: linear-gradient(150deg, #e0204b 0%, #8d0d24 100%); }
.cc .rr { height: 12px; border-radius: 6px; }
.curve { fill: none; stroke: url(#gc); stroke-width: 14; stroke-linecap: round; stroke-linejoin: round; }
.gridl { stroke: rgba(23,20,28,0.08); stroke-width: 2; }
.arcs path { fill: none; stroke: #ffe3ec; stroke-width: 12; stroke-linecap: round; stroke-linejoin: round; }
.arcs { filter: drop-shadow(0 0 12px rgba(255,110,156,0.9)); }

/* J: the doc card */
.doc { position: absolute; border-radius: 52px; overflow: hidden;
  background: linear-gradient(172deg, #ffffff 0%, #fff9fb 55%, #fdf0f4 100%);
  box-shadow: inset 0 2px 1px #fff, 0 50px 100px -36px rgba(24,4,12,0.62); }
.hl { position: absolute; left: 0; right: 0; background: rgba(255,110,156,0.20); transform-origin: 0 50%; }
.caret { position: absolute; width: 5px; border-radius: 3px; background: #e0204b; }

/* TK3: the list and the comment */
.row { position: absolute; left: 0; right: 0; height: 110px; }
.row .tx { position: absolute; left: 235px; top: 14px; font-size: 58px; font-weight: 700; letter-spacing: -0.015em;
  line-height: 80px; color: #17141c; white-space: nowrap; }
.ttl { position: absolute; font-size: 74px; font-weight: 900; letter-spacing: -0.03em; line-height: 1; color: #17141c;
  white-space: nowrap; }
.cmt { position: absolute; border-radius: 75px; background: #f7eef1;
  box-shadow: inset 0 0 0 2px rgba(23,20,28,0.06); }
.cmt .ph { position: absolute; left: 150px; top: 0; line-height: 150px; font-size: 42px; font-weight: 500;
  color: rgba(23,20,28,0.38); white-space: nowrap; }
.cmt .pl { position: absolute; left: 150px; top: 0; line-height: 150px; font-size: 92px; font-weight: 900; color: #b4122f; }
""")

L = []
BEATS = []


def beat(fn):
    BEATS.append(fn)
    return fn


# ===========================================================================
# A-D · the hub: the cable is pulled («зламається?»), the «?»s, the key, who
HUB = (730, 155, 180)       # x, y, size at the start (right); it moves to x 450


@beat
def a_hook():
    cab = ('<svg class="cab abs" width="1080" height="700" viewBox="0 0 1080 700" style="left:0;top:0">'
           '<path class="tube hide" id="aT" d="M338 245 C 470 200 600 200 730 245"/>'
           '<path class="core hide" id="aC" d="M338 245 C 470 200 600 200 730 245"/>'
           '<g class="pkg"><path class="pkt" id="aP" style="opacity:0" d="M338 245 C 470 200 600 200 730 245"/></g></svg>')
    qs = "".join(tile("aQ%d" % i, s, x, y, "pearl", glyph("?", int(s * 0.56), "#b4122f"), extra_cls="circ", ring=False)
                 for i, (x, y, s) in enumerate(((560, 100, 96), (936, 330, 92), (640, 370, 84))))
    chips = ('<div class="chips" style="top:476px">'
             '<div class="chip2 dglass edge hide" id="ch0">SMM-агенції</div>'
             '<div class="chip2 dglass edge hide" id="ch1">блогерки</div>'
             '<div class="chip2 dglass edge hide" id="ch2">підприємниці</div></div>')
    L.append('<div class="g full" id="gA">' + cab
             + tile("aMe", 170, 170, 160, "pearl", stroke("person"), extra_cls="circ", ring=False)
             + tile("aNo", 120, 235, 185, "pearl", g.mark("notion"))
             + tile("aCa", 120, 725, 185, "pearl", g.mark("canva"))
             + tile("aKey", 104, 488, 356, "pearl", stroke("key"), extra_cls="circ", ring=False)
             + tile("aHub", HUB[2], HUB[0], HUB[1], "jelly", g.mark("claude"))
             + tile("aQ", 100, 862, 100, "jelly", glyph("?", 58), extra_cls="circ", ring=False)
             + qs + chips + '</div>')
    sfx("pop", 0.06, -2)
    sfx("click", T["pratsiuvaty"] + 0.3)
    sfx("pop", T["zlam"] + 0.25)
    sfx("click", T["kliuch"] + 0.05)
    sfx("click-soft", T["smm"] + 0.02, -2)
    return js("""
  tl.set("#gA", {autoAlpha: 1}, 0);
  arr("#aHub", 0.0, {s: 0.55, y: 20});
  arr("#aMe", 0.12, {s: 0.55, y: 20});
  tl.set(["#aT", "#aC"], {autoAlpha: 1}, 0.3);
  draw2("aT", 0.3, 0.4); draw2("aC", 0.3, 0.4);
  G.packet("aP", @perestanu, 0.45);
  G.bump("#aHub", @perestanu+0.42);
  /* the cable is pulled: her tile steps back, the line retracts */
  tl.to("#aMe", {x: -46, rotation: -6, duration: 0.5, ease: SP}, @pratsiuvaty+0.25);
  undraw("aT", @pratsiuvaty+0.28, 0.32); undraw("aC", @pratsiuvaty+0.28, 0.32);
  tl.to("#aMe", {autoAlpha: 0.55, duration: 0.3}, @pratsiuvaty+0.4);
  /* «все зламається?» — the hub shakes and tilts */
  G.haptic("#aHub", @zlam+0.05);
  tl.to("#aHub", {rotation: 9, y: 16, duration: 0.5, ease: SP}, @zlam+0.2);
  arr("#aQ", @zlam+0.22, {s: 0.3, y: 20, d: 0.6});
  /* «це питання я чую постійно» — more of them */
  tl.to("#aHub", {rotation: 0, y: 0, duration: 0.5, ease: SP}, @pytannia);
  bout("#aMe", @pytannia, 10, 0.3);
  [0, 1, 2].forEach(function (i) { arr("#aQ" + i, @chuiu+i * 0.14, {s: 0.3, y: 20, d: 0.6}); });
  /* «налаштовую» — the hub takes the centre, two apps snap on, the key turns */
  bout(["#aQ", "#aQ0", "#aQ1", "#aQ2"], @tomu1-0.05, 10, 0.28);
  tl.to("#aHub", {x: -280, y: -5, duration: 0.7, ease: SP}, @tomu1+0.05);
  arr("#aNo", @nalasht+0.02, {s: 0.4, x: 120, y: 0, d: 0.7});
  arr("#aCa", @nalasht+0.14, {s: 0.4, x: -120, y: 0, d: 0.7});
  G.bump("#aHub", @nalasht+0.3);
  arr("#aKey", @pid-0.12, {s: 0.4, y: 50, d: 0.6});
  tl.fromTo("#aKey .sk", {rotation: 0}, {rotation: 90, transformOrigin: "50% 50%", duration: 0.45, ease: SP}, @kliuch+0.02);
  G.ripple("#aHubR", @kliuch+0.2);
  tl.set("#aHubR", {x: -280, y: -5}, 0);
  shn("#aHub .sheen", @kliuch+0.15);
  /* «для власниць ...» — who it is for */
  tl.to("#aHub", {y: -41, duration: 0.5, ease: SP}, @smm-0.3);
  tl.to(["#aNo", "#aCa", "#aKey"], {y: -36, duration: 0.5, ease: SP}, @smm-0.3);
  arr("#ch0", @smm-0.04, {s: 0.6, y: 30, d: 0.6});
  arr("#ch1", @blogerok-0.04, {s: 0.6, y: 30, d: 0.6});
  arr("#ch2", @pidpr-0.04, {s: 0.6, y: 30, d: 0.6});
  bout(["#ch0", "#ch1", "#ch2", "#aNo", "#aCa", "#aKey"], @pidpre-0.12, 10, 0.26);
  tl.set("#gA", {autoAlpha: 0}, @shchob+0.7);""")


# ===========================================================================
# TK1 · the team board, 24/7, then it is only Claude + a few apps
SHX, SHY = -50, 170
COLS = [215, 455, 695, 935]          # column centres, sheet coords
CLAUDE_C = (540, 560)


@beat
def tk1_team():
    cols = ""
    for ci, cx in enumerate(COLS):
        rows = ""
        for ri, (y, w) in enumerate(((190, 124), (265, 98), (340, 136))):
            rows += ('<div class="cbx" style="left:10px;top:%dpx;width:48px;height:48px"><div class="cbf" id="t1c%d%d">'
                     '<svg viewBox="0 0 24 24"><path id="t1p%d%d" d="M5.4 12.6l4.3 4.3 8.9-9.5"/></svg></div></div>'
                     '<i class="rr" style="left:74px;top:%dpx;width:%dpx;height:22px"></i>'
                     % (y, ci, ri, ci, ri, y + 13, w))
        cols += ('<div class="col" id="t1col%d" style="left:%dpx;top:50px">%s%s</div>'
                 % (ci, cx - 110, tile("t1av%d" % ci, 140, 40, 0, "pearl", stroke("person"), extra_cls="circ", ring=False),
                    rows))
    sheet = ('<div class="sheet hide" id="t1sh" style="left:%dpx;top:%dpx;width:1180px;height:960px" '
             'data-layout-allow-overflow>%s'
             '<div class="t247 hide" id="t247" style="left:110px;top:570px;width:640px">24/7</div>'
             '%s<div class="sheen"></div></div>'
             % (SHX, SHY, cols, tile("t1mo", 200, 800, 590, "jelly", stroke("moon"), extra_cls="circ")))
    cx, cy = CLAUDE_C
    L.append('<div class="g full" id="gT1"><div class="tkg"></div><div class="aurs"></div><div class="grain"></div>'
             + sheet
             + '<div class="tw hide" id="t1gh" style="left:%dpx;top:%dpx;width:300px;height:300px"><div class="clear"></div></div>'
             % (cx - 150, cy - 150)
             + tile("t1cl", 300, cx - 150, cy - 150, "jelly", g.mark("claude"))
             + tile("t1no", 150, 100, cy - 75, "pearl", g.mark("notion"))
             + tile("t1ca", 150, 830, cy - 75, "pearl", g.mark("canva"))
             + '</div>')
    sfx("whoosh-short", T["shchob"] - 0.08)
    sfx("pop", T["n24"] + 0.02)
    sfx("whoosh-short", T["naspr"] - 0.05, -2)
    sfx("pop", T["pidpyska"] + 0.05)
    ticks = []
    for ri, key, off in ((0, "kontent", 0.08), (1, "komanda", 0.4), (2, "nikoly", 0.08)):
        for ci in range(4):
            ticks.append('  tick("t1c%d%d", "t1p%d%d", @%s+%.2f);' % (ci, ri, ci, ri, key, off + ci * 0.09))
    collapse = []
    for ci, cx_ in enumerate(COLS):
        collapse.append('  tl.to("#t1col%d", {x: %d, y: %d, scale: 0.12, autoAlpha: 0, duration: 0.42, ease: "power3.in"}, @naspr-0.08+%.2f);'
                        % (ci, (CLAUDE_C[0] - SHX) - cx_, (CLAUDE_C[1] - SHY) - 260, ci * 0.04))
    return js("""
  G.irisOpen("#gT1", @shchob-0.1, 540, 225, 0.6);
  drift1("#gT1", @shchob, 18.3-@shchob);
  arr("#t1sh", @stvor-0.05, {s: 0.82, y: 60, d: 0.85});
  shn("#t1sh .sheen", @stvor+0.4);
  tl.set(["#t1av0", "#t1av1", "#t1av2", "#t1av3"], {autoAlpha: 0.28}, @stvor);
  [0, 1, 2, 3].forEach(function (i) {
    tl.fromTo("#t1av" + i, {autoAlpha: 0.28, scale: 0.8}, {autoAlpha: 1, scale: 1, duration: 0.6, ease: POP, immediateRender: false}, @komanda-0.05+i * 0.08);
  });
{{ticks}}
  arr("#t247", @n24-0.04, {s: 0.6, y: 40, d: 0.8});
  arr("#t1mo", @nikoly-0.04, {s: 0.4, y: 30, d: 0.7}); G.ripple("#t1moR", @nikoly+0.3);
  tl.fromTo("#t1mo .sk", {rotation: -30}, {rotation: 0, transformOrigin: "50% 50%", duration: 0.7, ease: SP, immediateRender: false}, @nikoly);
  /* «а насправді» — the whole team folds into one slot */
  bout(["#t247", "#t1mo"], @naspr-0.12, 10, 0.26);
{{collapse}}
  tl.to("#t1sh", {scale: 0.25, autoAlpha: 0, duration: 0.38, ease: "power3.in"}, @naspr+0.2);
  arr("#t1gh", @naspr+0.42, {s: 0.3, y: 0, d: 0.7});
  arr("#t1cl", @pidpyska-0.04, {s: 0.86, y: 0, d: 0.6, blur: 8});
  G.ripple("#t1clR", @pidpyska+0.25);
  shn("#t1cl .sheen", @claude);
  tl.set("#t1gh", {autoAlpha: 0}, @pidpyska+0.4);
  arr("#t1no", @kilka-0.02, {s: 0.4, x: 120, y: 0, d: 0.6});
  arr("#t1ca", @kilka+0.1, {s: 0.4, x: -120, y: 0, d: 0.6});
  G.irisClose("#gT1", 17.86, {{cx}}, {{cy}}, 0.37);""").replace("{{ticks}}", js("\n".join(ticks))).replace(
        "{{collapse}}", js("\n".join(collapse))).replace("{{cx}}", str(CLAUDE_C[0])).replace("{{cy}}", str(CLAUDE_C[1]))


# ===========================================================================
# F-H · the shelf: it lives on its own; she plugs in, the update waits; «ні»
PULSE = "M130 500 H352 L384 444 L420 556 L452 466 L478 500 H598 L630 444 L666 556 L698 466 L724 500 H950"


@beat
def f_shelf():
    svg = ('<svg class="abs" width="1080" height="700" viewBox="0 0 1080 700" style="left:0;top:0;overflow:visible">'
           '<g class="cab"><path class="tube hide" id="fT" d="M400 240 C 500 200 600 200 690 240"/>'
           '<path class="core hide" id="fC" d="M400 240 C 500 200 600 200 690 240"/></g>'
           '<path class="pulse hide" id="fPl" d="%s"/>'
           '<g class="cab"><g class="pkg"><path class="pkt" id="fPk1" style="opacity:0" d="%s"/>'
           '<path class="pkt" id="fPk2" style="opacity:0" d="%s"/><path class="pkt" id="fPk3" style="opacity:0" d="%s"/></g></g>'
           '<circle class="ringP hide" id="fRing" cx="540" cy="240" r="124" transform="rotate(-90 540 240)"/>'
           '<path class="strike hide" id="fSt" d="M772 192 L866 298"/>'
           '</svg>' % (PULSE, PULSE, PULSE, PULSE))
    spin = ('<svg class="spin hide" id="fSp" viewBox="0 0 220 220" width="220" height="220" '
            'style="left:660px;top:130px"><circle cx="110" cy="110" r="100"/></svg>')
    L.append('<div class="g full" id="gF">'
             '<div class="shelf edge hide" id="fSh" style="left:70px;top:110px;width:940px;height:470px"></div>'
             + svg
             + tile("fNo", 120, 235, 180, "pearl", g.mark("notion"))
             + tile("fCa", 120, 725, 180, "pearl", g.mark("canva"))
             + tile("fHub", 180, 450, 150, "jelly", g.mark("claude"))
             + tile("fMe", 160, 690, 160, "pearl", stroke("person"), extra_cls="circ", ring=False)
             + spin
             + tile("fUp", 76, 820, 132, "jelly", stroke("down"), extra_cls="circ", ring=False)
             + tile("fOk", 80, 588, 118, "jelly", stroke("check"), extra_cls="circ")
             + tile("fWr", 120, 760, 180, "pearl", stroke("wrench"))
             + '</div>')
    sfx("pop", T["zvych"] + 0.02, -3)
    sfx("ping", T["onovliu"] + 0.05, -2)
    sfx("whoosh-short", T["ni"] + 0.02, -2)
    sfx("pop", T["zlam2"] + 0.1)
    sfx("sparkle", T["povnistiu"] + 0.75, -2)
    sfx("click", T["pidtrymka"] + 0.3)
    return js("""
  tl.set("#gF", {autoAlpha: 1}, 18.31);
  arr("#fSh", 18.31, {s: 0.9, y: 30, d: 0.8});
  arr("#fHub", 18.33, {s: 1.4, y: 0, d: 0.7, blur: 8});
  arr("#fNo", 18.42, {s: 0.5, x: 120, y: 0, d: 0.6});
  arr("#fCa", 18.48, {s: 0.5, x: -120, y: 0, d: 0.6});
  G.bump("#fHub", @systema);
  /* «жити самостійно» — a pulse under it */
  tl.set("#fPl", {autoAlpha: 1}, @zhyty-0.05);
  draw2("fPl", @zhyty-0.05, 0.95);
  G.packet("fPk1", @samost+0.2, 0.7);
  /* «без того, щоб постійно чекати, поки я щось оновлю» */
  bout(["#fNo", "#fCa"], @bez-0.05, 10, 0.26);
  tl.to(["#fHub", "#fHubR"], {x: -230, duration: 0.6, ease: SP}, @bez);
  tl.to("#fPl", {opacity: 0.32, duration: 0.4}, @bez+0.1);
  arr("#fMe", @bez+0.15, {s: 0.5, x: 40, y: 0, d: 0.7});
  tl.set(["#fT", "#fC"], {autoAlpha: 1}, @bez+0.35);
  draw2("fT", @bez+0.35, 0.4); draw2("fC", @bez+0.35, 0.4);
  tl.fromTo("#fSp", {autoAlpha: 0, rotation: 0, transformOrigin: "50% 50%"}, {autoAlpha: 1, duration: 0.3}, @chekaty-0.05);
  tl.to("#fSp", {rotation: 520, duration: @onovliu+0.9-@chekaty, ease: "power1.inOut"}, @chekaty-0.05);
  arr("#fUp", @onovliu-0.02, {s: 0.3, y: 20, d: 0.6});
  G.haptic("#fUp", @onovliu+0.45);
  /* «ні» — she unplugs; the hub comes back; the pulse keeps going */
  undraw("fT", @ni-0.02, 0.3); undraw("fC", @ni-0.02, 0.3);
  tl.to(["#fMe", "#fSp", "#fUp"], {x: 140, autoAlpha: 0, duration: 0.4, ease: "power2.in"}, @ni+0.05);
  tl.to(["#fHub", "#fHubR"], {x: 0, duration: 0.6, ease: SP}, @ni+0.3);
  tl.to("#fPl", {opacity: 1, duration: 0.3}, @zlam2-0.2);
  G.packet("fPk2", @zlam2-0.1, 0.7);
  arr("#fOk", @zlam2+0.1, {s: 0.3, y: 10, d: 0.6}); G.ripple("#fOkR", @zlam2+0.35);
  /* «повністю налаштована» — the ring closes; «не потрібна підтримка» */
  tl.set("#fRing", {autoAlpha: 1}, @povnistiu-0.05);
  draw2("fRing", @povnistiu-0.05, 0.9);
  shn("#fHub .sheen", @povnistiu+0.75);
  G.packet("fPk3", @povnistiu+0.3, 0.7);
  arr("#fWr", @pidtrymka-0.25, {s: 0.4, y: 20, d: 0.6});
  tl.set("#fSt", {autoAlpha: 1}, @pidtrymka+0.25);
  draw2("fSt", @pidtrymka+0.25, 0.22);
  tl.to("#fWr", {autoAlpha: 0.45, duration: 0.25}, @pidtrymka+0.45);
  tl.set("#gF", {autoAlpha: 0}, @vona+0.65);""")


# ===========================================================================
# TK2 · it updates itself: arrows round Claude, content flies in, a profile
# fills, a curve rises
TC = (540, 380)
CARDS = [(30, 170, 124, 220), (70, 470, 150, 188), (920, 160, 124, 220), (880, 480, 150, 188)]


@beat
def tk2_learn():
    cx, cy = TC
    arcs = ('<svg class="abs" width="1080" height="1000" viewBox="0 0 1080 1000" style="left:0;top:0;overflow:visible">'
            '<g class="arcs hide" id="t2arc">'
            '<path id="t2a1" d="M365 380 A175 175 0 0 1 704.4 320.1"/><path d="M682 316 L705 321 L713 299"/>'
            '<path id="t2a2" d="M715 380 A175 175 0 0 1 375.6 439.9"/><path d="M398 444 L375 439 L367 461"/>'
            '</g></svg>')
    cards = ""
    for i, (x, y, w, h) in enumerate(CARDS):
        cards += ('<div class="cc hide" id="t2c%d" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx">'
                  '<i class="im" style="height:%dpx"></i>'
                  '<i class="rr" style="left:14px;top:%dpx;width:%dpx"></i>'
                  '<i class="rr" style="left:14px;top:%dpx;width:%dpx"></i></div>'
                  % (i, x, y, w, h, h - 64, h - 44, w - 34, h - 24, (w - 34) * 6 // 10))
    bars = ""
    for i, (y, w) in enumerate(((270, 470), (322, 400), (374, 440), (426, 300))):
        bars += ('<i class="rr" style="left:100px;top:%dpx;width:%dpx;height:24px"></i>'
                 '<i class="fillb" id="t2f%d" style="left:100px;top:%dpx;width:%dpx;height:24px"></i>' % (y, w, i, y, w))
    chart = ('<svg class="abs" width="1160" height="500" viewBox="0 0 1160 500" style="left:0;top:0;overflow:visible">'
             '<defs><linearGradient id="gc" x1="0" y1="1" x2="1" y2="0"><stop offset="0" stop-color="#b4122f"/>'
             '<stop offset="1" stop-color="#ff6e9c"/></linearGradient></defs>'
             '<line class="gridl" x1="660" y1="140" x2="1080" y2="140"/>'
             '<line class="gridl" x1="660" y1="260" x2="1080" y2="260"/>'
             '<line class="gridl" x1="660" y1="380" x2="1080" y2="380"/>'
             '<line class="gridl" x1="610" y1="60" x2="610" y2="440"/>'
             '<path class="curve" id="t2cv" d="M670 420 C 760 410 820 380 880 320 S 990 150 1060 110"/>'
             '</svg>')
    sheet = ('<div class="sheet hide" id="t2sh" style="left:-40px;top:700px;width:1160px;height:480px" '
             'data-layout-allow-overflow>%s%s'
             '<i class="hb" style="left:270px;top:110px;width:250px;height:34px"></i>%s'
             '<div class="tw circ" id="t2dot" style="left:1040px;top:90px;width:40px;height:40px;opacity:0">'
             '<div class="jelly"></div></div>'
             '<div class="sheen"></div></div>'
             % (chart, tile("t2av", 140, 100, 70, "pearl", stroke("person"), extra_cls="circ", hide=False, ring=False), bars))
    L.append('<div class="g full" id="gT2"><div class="tkg"></div><div class="aurs"></div><div class="grain"></div>'
             + arcs + cards + sheet
             + tile("t2cl", 240, cx - 120, cy - 120, "jelly", g.mark("claude"), hide=False)
             + '</div>')
    sfx("whoosh-short", T["vona"] - 0.08, -2)
    sfx("pop", T["robysh"] + 0.4, -2)
    sfx("click-soft", T["znaie"] + 0.05)
    fly = []
    for i, (x, y, w, h) in enumerate(CARDS):
        t0 = "@robysh-0.05+%.2f" % (i * 0.13)
        fly.append('  arr("#t2c%d", %s, {s: 0.6, y: 30, d: 0.5});' % (i, t0))
        fly.append('  tl.to("#t2c%d", {x: %d, y: %d, scale: 0.18, rotation: %d, autoAlpha: 0, duration: 0.42, ease: "power2.in"}, %s+0.42);'
                   % (i, cx - (x + w // 2), cy - (y + h // 2), (-8 if i < 2 else 8), t0))
        fly.append('  G.bump("#t2cl", %s+0.82);' % t0)
    return js("""
  G.irisOpen("#gT2", @vona-0.1, 540, 240, 0.6);
  drift1("#gT2", @vona, 5.4);
  tl.fromTo("#t2cl", {x: 0, y: -140, scale: 0.75}, {x: 0, y: 0, scale: 1, duration: 0.8, ease: SP}, @vona-0.05);
  /* «сама себе оновлює» — two arrows turn round it */
  tl.set("#t2arc", {autoAlpha: 1}, @sama-0.1);
  draw2("t2a1", @sama-0.1, 0.45); draw2("t2a2", @sama-0.1, 0.45);
  tl.fromTo("#t2arc", {rotation: 0, svgOrigin: "540 380"}, {rotation: 360, svgOrigin: "540 380", duration: 1.6, ease: "power2.inOut"}, @sama+0.1);
  G.ripple("#t2clR", @sama+0.5);
  bout("#t2arc", @chym-0.05, 8, 0.3);
  /* «чим більше ти робиш контенту» — the content goes into it */
{{fly}}
  /* «тим більше вона про тебе знає» — a profile fills */
  arr("#t2sh", @vona2-0.2, {s: 0.85, y: 60, d: 0.8});
  shn("#t2sh .sheen", @vona2+0.3);
  tl.fromTo(".fillb", {scaleX: 0}, {scaleX: 1, duration: 0.5, ease: SP, stagger: 0.12}, @znaie-0.02);
  /* «і тим краще працює» — a curve rises */
  draw2("t2cv", @tym3, 0.75);
  tl.fromTo("#t2dot", {opacity: 0, scale: 0.2}, {opacity: 1, scale: 1, duration: 0.4, ease: POP}, @tym3+0.7);
  G.irisClose("#gT2", 34.98, 540, 330, 0.38);""").replace("{{fly}}", js("\n".join(fly)))


# ===========================================================================
# J · a minor edit; something stopped working -> fixed; nothing else
@beat
def j_edit():
    rows = ""
    for i, (y, w) in enumerate(((140, 610), (210, 540), (280, 640), (350, 410))):
        rows += '<i class="rr" id="jr%d" style="left:56px;top:%dpx;width:%dpx;height:26px;transform-origin:0 50%%"></i>' % (i, y, w)
    doc = ('<div class="doc hide" id="jd" style="left:140px;top:132px;width:800px;height:440px">'
           '<div class="hl" id="jhl" style="top:196px;height:54px;opacity:0"></div>'
           '<i class="hb" style="left:56px;top:56px;width:300px;height:36px"></i>%s'
           '<i class="fillb" id="jnew" style="left:%dpx;top:210px;width:250px;height:26px"></i>'
           '<div class="caret" id="jcar" style="left:%dpx;top:200px;height:46px;opacity:0"></div>'
           '<div class="shc"><div class="sheen"></div></div></div>' % (rows, 56 + 290 + 14, 56 + 290 + 14 + 256))
    L.append('<div class="g full" id="gJ">' + doc
             + tile("jWa", 104, 884, 96, "jelly", glyph("!", 62), extra_cls="circ")
             + tile("jOk", 104, 884, 96, "pearl", stroke("check"), extra_cls="circ")
             + '</div>')
    sfx("click", T["pravku"] + 0.05)
    sfx("notification", T["perestalo"] + 0.05, -3)
    sfx("pop", T["zminyty"] + 0.1)
    return js("""
  tl.set("#gJ", {autoAlpha: 1}, @yakshcho2-0.05);
  arr("#jd", @yakshcho2-0.02, {s: 0.75, y: 40, d: 0.8});
  shn("#jd .sheen", @yakshcho2+0.35);
  /* «мінімальну правку» — one line, partly rewritten */
  tl.fromTo("#jhl", {opacity: 0, scaleX: 0.2}, {opacity: 1, scaleX: 1, duration: 0.35, ease: "power2.out"}, @minim-0.05);
  tl.to("#jr1", {scaleX: 290 / 540, duration: 0.35, ease: "power2.inOut"}, @pravku-0.15);
  tl.fromTo("#jnew", {scaleX: 0}, {scaleX: 1, duration: 0.45, ease: SP}, @pravku+0.15);
  tl.fromTo("#jcar", {opacity: 0, x: -256}, {opacity: 1, x: 0, duration: 0.45, ease: "power2.out", immediateRender: false}, @pravku+0.15);
  tl.to("#jcar", {opacity: 0, duration: 0.15}, @perestalo-0.1);
  tl.to("#jhl", {opacity: 0, duration: 0.3}, @perestalo);
  /* «або щось перестало працювати» -> «можна змінити» */
  arr("#jWa", @perestalo-0.02, {s: 0.3, y: 20, d: 0.6});
  G.haptic("#jd", @perestalo+0.1);
  bout("#jWa", @zminyty-0.05, 8, 0.22);
  arr("#jOk", @zminyty+0.05, {s: 0.4, y: 0, d: 0.6}); G.ripple("#jOkR", @zminyty+0.3);
  G.bump("#jOk", @zahalom+0.7);
  bout("#gJ", @treba-0.1, 10, 0.3);""")


# ===========================================================================
# TK3 · the turnkey system: the list ticks, «+» goes in a comment
ITEMS = [(u"Аналізує контент та таргет", "analiz", "tarhet", 0.05),
         (u"Пише сценарії", "pyshe", "stsen", 0.1),
         (u"Дизайнить каруселі", "dyzain", "karus", 0.08),
         (u"Монтує рілси", "montuie", "rilsy", 0.05)]


@beat
def tk3_cta():
    rows = ""
    for i, (txt, _, _, _) in enumerate(ITEMS):
        rows += ('<div class="row hide" id="t3r%d" style="top:%dpx">'
                 '<div class="cbx" style="left:110px;top:16px;width:78px;height:78px"><div class="cbf" id="t3c%d">'
                 '<svg viewBox="0 0 24 24"><path id="t3p%d" d="M5.4 12.6l4.3 4.3 8.9-9.5"/></svg></div></div>'
                 '<div class="tx">%s</div></div>' % (i, 290 + i * 140, i, i, txt))
    sheet = ('<div class="sheet hide" id="t3sh" style="left:-40px;top:130px;width:1160px;height:1090px" '
             'data-layout-allow-overflow>'
             '%s<div class="ttl" id="t3tt" style="left:275px;top:98px">Система під ключ</div>'
             '<div class="hair" style="position:absolute;left:110px;top:250px;width:1010px"></div>%s'
             '<div class="cmt hide" id="t3cm" style="left:110px;top:880px;width:960px;height:150px">'
             '<div class="tw circ" style="left:30px;top:30px;width:90px;height:90px"><div class="pearl">%s</div></div>'
             '<div class="ph" id="t3ph">Додайте коментар…</div><div class="pl" id="t3pl" style="opacity:0">+</div>'
             '%s</div>'
             '<div class="sheen"></div></div>'
             % (tile("t3key", 130, 110, 66, "jelly", stroke("key"), hide=False, ring=False), rows, stroke("person"),
                tile("t3se", 104, 830, 23, "jelly", stroke("up"), extra_cls="circ", hide=False)))
    L.append('<div class="g full" id="gT3"><div class="tkg"></div><div class="aurs"></div><div class="grain"></div>'
             + sheet + '</div>')
    sfx("whoosh-short", T["tomu3"] - 0.1, -1)
    for _, a, b, off in ITEMS:
        sfx("click-soft", T[b] + off + 0.05, -1)
    sfx("pop", T["plius"] + 0.04)
    out = ["""
  G.irisOpen("#gT3", @tomu3-0.1, 540, 330, 0.65);
  drift1("#gT3", @tomu3, @dur-@tomu3);
  arr("#t3sh", @yakshcho3-0.05, {s: 0.82, y: 70, d: 0.9});
  shn("#t3sh .sheen", @tsikava+0.2);
  tl.fromTo("#t3tt", {clipPath: "inset(0 100% 0 0)"}, {clipPath: "inset(0 0% 0 0)", duration: 0.6, ease: "power2.out"}, @systema3-0.05);
  tl.fromTo("#t3key .sk", {rotation: 0}, {rotation: 90, transformOrigin: "50% 50%", duration: 0.45, ease: SP}, @kliuch3+0.02);
  G.bump("#t3key", @kliuch3+0.05);"""]
    for i, (_, a, b, off) in enumerate(ITEMS):
        out.append('  arr("#t3r%d", @%s-0.08, {s: 0.92, x: -40, y: 0, d: 0.6, blur: 8});' % (i, a))
        out.append('  tick("t3c%d", "t3p%d", @%s+%.2f);' % (i, i, b, off))
    out.append("""
  arr("#t3cm", @stav-0.25, {s: 0.9, y: 30, d: 0.6});
  tl.set("#t3ph", {opacity: 0}, @plius);
  tl.fromTo("#t3pl", {opacity: 0, scale: 0.4}, {opacity: 1, scale: 1, duration: 0.4, ease: POP, transformOrigin: "30% 50%"}, @plius);
  G.bump("#t3se", @koment+0.05); G.ripple("#t3seR", @koment+0.1);""")
    return js("\n".join(out))


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
  function undraw(id, t, d) {
    var L = document.getElementById(id).getTotalLength() + 3;
    tl.to("#" + id, {strokeDashoffset: L, duration: d || 0.3, ease: "power2.in"}, t);
  }
  function tick(box, path, t) {
    tl.fromTo("#" + box, {autoAlpha: 0, scale: 0.4}, {autoAlpha: 1, scale: 1, duration: 0.4, ease: POP}, t);
    draw2(path, t + 0.06, 0.3);
  }
  function shn(sel, t) {
    gsap.set(sel, {xPercent: -120});
    tl.fromTo(sel, {xPercent: -120}, {xPercent: 120, duration: 0.8, ease: "power2.inOut", immediateRender: false}, t);
  }
  function drift1(sel, t, d) { tl.fromTo(sel + " .aurs", {x: 0, y: 0}, {x: -110, y: 70, duration: d, ease: "sine.inOut"}, t); }
  gsap.set(".sheen", {xPercent: -120});
"""


def span(a, b):
    return (round(a - 0.02, 3), round(b, 3), "")


# captions that would repeat the graphic's own words (STYLE.md §2b.1)
BLACKOUT = [
    span(T["smm"], T["pidpre"]),                 # the three chips say who
    span(T["n24"], T["n7e"]),                    # «24/7» on the board
    span(T["systema3"], T["stav"] - 0.04),       # the list says «система під ключ ...»
]


def check_no_paint():
    """No graphic may be on screen inside a closeup."""
    for a, b in NO_PAINT:
        assert 17.86 + 0.39 < a - 0.001, "TK1 still open in the closeup"
        assert 18.31 > b, "the shelf arrives inside the closeup"


def main():
    check_no_paint()
    gj = []
    for fn in BEATS:
        j = fn()
        gj.append("  /* %s */" % fn.__name__)
        gj.append(j.rstrip())
    push = ["#vid"]
    head = [g.js(), HEAD_JS,
            '  gsap.set(%s, {transformOrigin: "540px 900px"});' % json.dumps(push),
            '  tl.fromTo(%s, {scale: 1}, {scale: 1.045, duration: %.3f, ease: "none"}, 0);' % (json.dumps(push), DUR)]
    doc = k.document(
        title=u"Reel 37 — А якщо я перестану з тобою працювати",
        plate="assets/base.mp4",
        gfx_html=g.defs() + "\n" + "\n".join(L),
        gfx_js="\n".join(head + gj),
        caps=CAPS,
        blackout=BLACKOUT,
    )
    io.open(os.path.join(HERE, "index.html"), "w", encoding="utf-8").write(doc)
    SFX.sort(key=lambda c: c["t"])
    io.open(os.path.join(HERE, "sfx.json"), "w", encoding="utf-8").write(json.dumps(SFX, indent=1))
    print("index.html  %d captions, %d beats, %d sfx cues (%.2f/s)" % (len(CAPS), len(BEATS), len(SFX), len(SFX) / DUR))


main()
