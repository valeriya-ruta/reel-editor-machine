# -*- coding: utf-8 -*-
"""Reel 34 — «Все в одному Claude». Posts 2026-10-14.

A fast list reel: «Для картинок… ні, OpenRouter в Клод» six times, then her
wrap-up (stop jumping between AI platforms, one platform set up for you) and
the CTA. See PLAN.md for the chain.

One mechanic, escalating: a Claude dock collects the right tools. On every
«Для X» she points up-left, on every answer up-right — so the wrong tool lands
on a dark card on the left, the right one on a white card on the right, and on
«в Клод» the right tile flies up into the dock. Lines 1–2 are struck on «ні»;
lines 3–6 have no «ні», so the right card shoves the wrong one off. The sixth
tile lands, the iris opens out of the hub into the takeover, and closes back
onto it for the CTA.

usage: python build.py   (then: python ../tools/sfx.py mix 34)
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

CUT = json.load(io.open(os.path.join(ROOT, "work", "r34", "cut.json"), encoding="utf-8"))
DUR = 28.183           # (846 plate frames - 0.5) / 30
FPS = 30
k = Kit(width=1080, height=1920, fps=FPS, duration=DUR)
g = Glass(["claude", "googlegemini", "openai", "canva", "openrouter", "fathom"])
k.css(g.css())

NO_PAINT = [tuple(x) for x in CUT["no_paint"]]          # none in this cut

CAPS = k.load_captions(os.path.join(ROOT, "work", "r34", "captions.json"))
FIX = {u"пожив": u"пиши"}                                # whisper misheard her «пиши»
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
    "d1": S(u"Для", 0.0), "ni1": S(u"ні", 1.547), "openr": S("OpenRouter", 2.02), "k1": S(u"Клод", 2.88),
    "d2": S(u"Для", 3.3), "ni2": S(u"ні", 4.647), "fathom": S("Fathom", 5.227), "k2": S(u"Клод", 5.598),
    "d3": S(u"Для", 6.1), "dyz": S(u"дизайн-система", 7.14), "k3": S(u"Клод", 8.109),
    "d4": S(u"Для", 8.79), "winds": S("Windsor", 10.232), "k4": S(u"Клод", 10.699),
    "d5": S(u"Для", 11.167), "skil": S(u"скіл", 12.467), "k5": S(u"Клод", 13.037),
    "d6": S(u"Для", 13.933), "skily": S(u"скіли", 15.376), "k6": S(u"в", 15.883),
    "treba": S(u"Треба", 16.4), "stryb": S(u"стрибати", 17.314), "mizh": S(u"між", 17.814),
    "kupoiu": S(u"купою", 18.134), "riznykh": S(u"різних", 18.614), "shi": S(u"ШІ-платформ", 19.114),
    "platyty": S(u"платити", 19.914), "za": S(u"за", 20.394), "a": S(u"а", 21.034),
    "vziaty": S(u"взяти", 21.674), "odnu": S(u"одну", 22.214), "i2": S(u"і", 23.274),
    "nalasht": S(u"налаштувати", 23.414), "pid": S(u"під", 24.914), "tebe": S(u"тебе", 25.174),
    "yakshcho": S(u"Якщо", 25.5), "to": S(u"то", 26.967), "plius": S(u"плюс", 27.45),
    "koment": S(u"коментарі", 27.63),
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
SFX = []


def sfx(name, t, db=0):
    if isinstance(t, str):
        t = float(js(t))
    SFX.append({"t": round(max(0.0, t), 3), "name": name, "db": db})


# ---------------------------------------------------------------------------
# Glyphs (24-unit strokes) for the tools that have no simple-icons mark
STROKES = {
    "grid": '<rect x="3.5" y="4.5" width="17" height="15" rx="2.6"/><path d="M3.5 9.6h17M3.5 14.5h17M9.6 4.5v15"/>',
    "scissors": '<circle cx="6.6" cy="17.2" r="2.7"/><circle cx="17.4" cy="17.2" r="2.7"/>'
                '<path d="M8.5 15.3L18 4.6M15.5 15.3L6 4.6"/>',
    "palette": '<path d="M12 3.6a8.4 8.4 0 1 0 0 16.8c1.3 0 1.9-.9 1.6-2-.3-1.2.4-2.3 1.7-2.3h1.8a3.4 3.4 0 0 0 3.4-3.4'
               'C20.5 7.3 16.7 3.6 12 3.6z"/><circle cx="7.8" cy="11.2" r="1.15"/><circle cx="10.6" cy="7.7" r="1.15"/>'
               '<circle cx="14.9" cy="7.9" r="1.15"/>',
    "clapper": '<path d="M4 10h16v8.4a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2z"/><path d="M4 10l-.6-3.4 15.2-2.7.6 3.4z"/>'
               '<path d="M8.4 5.8l2.3 3.3M13.4 4.9l2.3 3.3"/>',
    "skill": '<path d="M7 3.6h7.2l4.4 4.4v10.4a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V5.6a2 2 0 0 1 2-2z"/>'
             '<path d="M14 3.6v4.6h4.6M8.6 12.6h6.8M8.6 16.2h4.6"/>',
    "person": '<circle cx="12" cy="8.2" r="3.6"/><path d="M4.8 20c.9-3.8 3.7-5.8 7.2-5.8s6.3 2 7.2 5.8"/>',
    "up": '<path d="M12 19.2V5.4M6.2 11l5.8-5.8 5.8 5.8"/>',
}


def stroke(name, cls="sk"):
    return '<svg class="%s" viewBox="0 0 24 24">%s</svg>' % (cls, STROKES[name])


def glyph(spec, size):
    kind, val = spec
    if kind == "i":
        return g.mark(val)
    if kind == "s":
        return stroke(val)
    return '<span class="wmark" style="font-size:%dpx">%s<i>.</i></span>' % (int(size * 0.56), val)


def tile(tid, size, x, y, material, inner, extra_cls="", hide=True, ring=True):
    r = ('<div class="sqring" id="%sR" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx"></div>'
         % (tid, x, y, size, size)) if ring else ""
    return ('%s<div class="tw%s %s" id="%s" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx">'
            '<div class="%s">%s<div class="sheen"></div></div></div>'
            % (r, " hide" if hide else "", extra_cls, tid, x, y, size, size, material, inner))


# the six lines: wrong tool (never said) -> right tool (said), with her timing keys
LINES = [
    dict(wn="Nano Banana", wg=("i", "googlegemini"), rn="OpenRouter", rg=("i", "openrouter"),
         d="d1", ni="ni1", r="openr", k="k1"),
    dict(wn="Whisper", wg=("i", "openai"), rn="Fathom", rg=("i", "fathom"),
         d="d2", ni="ni2", r="fathom", k="k2"),
    dict(wn="Canva", wg=("i", "canva"), rn=u"дизайн-система", rg=("s", "palette"),
         d="d3", ni=None, r="dyz", k="k3"),
    dict(wn="Excel", wg=("s", "grid"), rn="Windsor", rg=("w", "w"),
         d="d4", ni=None, r="winds", k="k4"),
    dict(wn="CapCut", wg=("s", "scissors"), rn=u"скіл монтажу", rg=("s", "clapper"),
         d="d5", ni=None, r="skil", k="k5"),
    dict(wn="ChatGPT", wg=("i", "openai"), rn=u"скіли", rg=("s", "skill"),
         d="d6", ni=None, r="skily", k="k6"),
]

# geometry
HUB = (540, 155, 170)                                  # centre x, centre y, size
SLOT_X = [375, 705, 245, 835, 115, 965]                # dock fills centre-out
SLOT_Y, SLOT = 155, 104
WC = (60, 300, 440, 250)                               # wrong card: left, top, w, h
RC = (580, 300, 440, 250)                              # right card
CT = 120                                               # tile inside a card
CT_TOP = 28
RC_TILE = (RC[0] + RC[2] // 2, RC[1] + CT_TOP + CT // 2)

k.css("""
.abs { position: absolute; }
.hide { opacity: 0; visibility: hidden; }
.tw { position: absolute; }
.sk { fill: none; stroke: url(#gw); stroke-width: 2.3; stroke-linecap: round; stroke-linejoin: round;
  width: 50%; height: 50%; position: relative; z-index: 1; overflow: visible; }
.pearl .sk { stroke: #17141c; }
.circ .jelly, .circ .pearl, .circ .clear, .circ .sheen { border-radius: 50%; }
.aurs { position: absolute; left: -700px; top: -700px; width: 2480px; height: 3320px; pointer-events: none;
  background:
    radial-gradient(circle 526px at 1560px 880px, rgba(255,110,156,0.50), rgba(255,110,156,0)),
    radial-gradient(circle 634px at 760px 2360px, rgba(222,32,74,0.55), rgba(222,32,74,0)),
    radial-gradient(circle 382px at 1480px 1910px, rgba(255,198,214,0.20), rgba(255,198,214,0)); }

/* the dock */
.slot { position: absolute; border-radius: 22.4%; border: 3px dashed rgba(255,255,255,0.42);
  background: rgba(255,255,255,0.06); }

/* swap cards */
.wc { border-radius: 56px; }
.rc { position: absolute; border-radius: 56px; overflow: hidden; color: #17141c;
  background: linear-gradient(172deg, #ffffff 0%, #fff9fb 55%, #fdf0f4 100%);
  box-shadow: inset 0 2px 1px #fff, inset 0 -26px 50px -30px rgba(180,18,47,0.16),
              0 50px 100px -36px rgba(24,4,12,0.62), 0 0 0 1px rgba(255,255,255,0.4); }
.nm { position: absolute; left: 0; right: 0; top: 166px; text-align: center; font-size: 46px; font-weight: 700;
  letter-spacing: -0.02em; line-height: 56px; white-space: nowrap; }
.wc .nm { color: #fff; }
.stk { position: absolute; left: 0; top: 0; overflow: visible; z-index: 4; }
.sline { fill: none; stroke: #ff4d7f; stroke-width: 13; stroke-linecap: round;
  filter: drop-shadow(0 0 8px rgba(255,110,156,0.9)); }
.shc { position: absolute; inset: 0; border-radius: inherit; overflow: hidden; pointer-events: none; }
.shc .sheen { mix-blend-mode: normal; opacity: 0.45; }

/* takeover */
.lbl { position: absolute; width: 330px; text-align: center; font-size: 40px; font-weight: 700; color: #fff;
  letter-spacing: -0.015em; white-space: nowrap; }
.row { position: absolute; left: 180px; width: 900px; height: 104px; }
.row .rn { position: absolute; left: 124px; top: 0; line-height: 104px; font-size: 46px; font-weight: 700;
  letter-spacing: -0.02em; color: #17141c; white-space: nowrap; }
.row .hr { position: absolute; left: 0; right: 40px; bottom: -11px; height: 2px; background: rgba(23,20,28,0.07); }
.tg { position: absolute; left: 720px; top: 16px; width: 130px; height: 72px; border-radius: 36px;
  background: rgba(23,20,28,0.13); box-shadow: inset 0 2px 4px rgba(23,20,28,0.10); }
.tg .on { position: absolute; inset: 0; border-radius: 36px; opacity: 0; visibility: hidden;
  background: linear-gradient(165deg, #e0204b 0%, #ab112e 46%, #6b081c 100%);
  box-shadow: inset 0 2px 1px rgba(255,255,255,0.45); }
.tg .kn { position: absolute; left: 7px; top: 7px; width: 58px; height: 58px; border-radius: 50%; background: #fff;
  box-shadow: 0 4px 10px rgba(23,20,28,0.25); }

/* the comment field */
#cm .ph, #cm .pl { position: absolute; left: 150px; top: 0; line-height: 150px; white-space: nowrap; }
#cm .ph { font-size: 38px; font-weight: 500; color: rgba(255,255,255,0.55); }
#cm .pl { font-size: 76px; font-weight: 900; color: #fff; }
.ck { position: absolute; width: 120px; height: 120px; margin: -60px 0 0 -60px; border-radius: 50%;
  border: 7px solid #ff6e9c; opacity: 0; visibility: hidden; z-index: 5; }
""")

L = []
BEATS = []


def beat(fn):
    BEATS.append(fn)
    return fn


def card_html(i, ln):
    wx, wy, ww, wh = WC
    rx, ry, rw, rh = RC
    tx = (ww - CT) // 2
    sl_y = 166 + 30
    wrong = ('<div class="dglass edge wc hide" id="wc%d" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx">'
             '%s<div class="nm">%s</div>'
             '<svg class="stk" width="%d" height="%d"><path class="sline" id="ws%d" d="M44 %d L%d %d"/></svg>'
             '</div>' % (i, wx, wy, ww, wh,
                         tile("wt%d" % i, CT, tx, CT_TOP, "pearl", glyph(ln["wg"], CT), hide=False, ring=False),
                         ln["wn"], ww, wh, i, sl_y + 8, ww - 44, sl_y - 8))
    right = ('<div class="rc hide" id="rc%d" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx">'
             '%s<div class="nm">%s</div><div class="shc"><div class="sheen"></div></div></div>'
             % (i, rx, ry, rw, rh,
                tile("rt%d" % i, CT, tx, CT_TOP, "jelly", glyph(ln["rg"], CT), hide=False, ring=False),
                ln["rn"]))
    return wrong + right


# ===========================================================================
# A · the dock and the six swaps
@beat
def a_swaps():
    hx, hy, hs = HUB
    slots = "".join('<div class="slot" id="sl%d" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx"></div>'
                    % (i, x - SLOT // 2 - 40, SLOT_Y - SLOT // 2 - 75, SLOT, SLOT) for i, x in enumerate(SLOT_X))   # inside the shelf
    dock = "".join(tile("dk%d" % i, SLOT, SLOT_X[i] - SLOT // 2, SLOT_Y - SLOT // 2, "jelly",
                        glyph(ln["rg"], SLOT), ring=False) for i, ln in enumerate(LINES))
    cards = "".join(card_html(i, ln) for i, ln in enumerate(LINES))
    L.append('<div class="g full" id="gN">'
             '<div class="shelf edge hide" id="dock" style="left:40px;top:75px;width:1000px;height:160px">%s</div>'
             % slots
             + cards + dock
             + tile("hub", hs, hx - hs // 2, hy - hs // 2, "jelly", g.mark("claude"))
             + '</div>')
    out = ["""
  tl.set("#gN", {autoAlpha: 1}, 0);
  arr("#dock", 0.0, {s: 0.86, y: -20, d: 0.8});
  arr("#hub", 0.06, {s: 0.4, y: 0, d: 0.8});
  gsap.set("#hub", {transformOrigin: "50% 50%"});"""]
    wx, wy, ww, wh = WC
    for i, ln in enumerate(LINES):
        tw = T[ln["d"]] + (0.12 if i == 0 else 0.0)        # the wrong card lands on «Для»
        tr = T[ln["r"]] - 0.08                              # the right card on its word
        tk = T[ln["k"]] + 0.12                              # the tile flies on «в Клод»
        dx, dy = RC_TILE[0] - SLOT_X[i], RC_TILE[1] - SLOT_Y
        hsz = 1 + 0.03 * (i + 1)
        o = []
        o.append('  arr("#wc%d", %.3f, {s: 0.62, x: -50, y: 20, d: 0.8});' % (i, tw))
        if ln["ni"]:
            tn = T[ln["ni"]]
            o.append('  draw2("ws%d", %.3f, 0.22); G.haptic("#wc%d", %.3f);' % (i, tn + 0.02, i, tn + 0.08))
            o.append('  tl.to("#wc%d", {x: -620, y: 150, rotation: -24, autoAlpha: 0, filter: "blur(8px)", '
                     'duration: 0.42, ease: "power2.in"}, %.3f);' % (i, tn + 0.44))
            o.append('  arr("#rc%d", %.3f, {s: 0.6, x: 60, y: 20, d: 0.8});' % (i, tr))
            sfx("click", tn + 0.03)
        else:
            # no «ні» on camera: the right card shoves the wrong one off
            o.append('  draw2("ws%d", %.3f, 0.16);' % (i, tr - 0.14))
            o.append('  bin("#rc%d", %.3f, 10, 0.22);' % (i, tr))
            o.append('  tl.fromTo("#rc%d", {x: 380, rotation: 4}, {x: 0, rotation: 0, duration: 0.6, ease: SP}, %.3f);'
                     % (i, tr))
            o.append('  tl.to("#wc%d", {x: -660, y: 120, rotation: -30, autoAlpha: 0, filter: "blur(8px)", '
                     'duration: 0.38, ease: "power2.in"}, %.3f);' % (i, tr + 0.06))
        o.append('  shn("#rc%d .shc .sheen", %.3f);' % (i, tr + 0.3))
        # into the dock
        o.append('  tl.set("#rt%d", {autoAlpha: 0}, %.3f);' % (i, tk))
        o.append('  tl.to("#rc%d", {scale: 0.6, y: -70, autoAlpha: 0, duration: 0.26, ease: "power2.in"}, %.3f);'
                 % (i, tk))
        o.append('  tl.set("#dk%d", {autoAlpha: 1}, %.3f);' % (i, tk))
        o.append('  tl.fromTo("#dk%d", {x: %d, y: %d, scale: %.3f}, {x: 0, y: 0, scale: 1, duration: 0.6, ease: SP}, %.3f);'
                 % (i, dx, dy, CT / float(SLOT), tk))
        o.append('  tl.to("#hub", {scale: %.3f, duration: 0.1, ease: "power2.out"}, %.3f);' % (hsz + 0.08, tk + 0.34))
        o.append('  tl.to("#hub", {scale: %.3f, duration: 0.45, ease: SP}, %.3f);' % (hsz, tk + 0.44))
        o.append('  G.ripple("#hubR", %.3f);' % (tk + 0.34))
        sfx("pop", tk + 0.34, -1)
        out.append("\n".join(o))
    out.append('  tl.set("#gN", {autoAlpha: 0}, @treba+0.66);')
    return js("\n".join(out))


# ===========================================================================
# TK · the iris opens out of the hub: platforms everywhere -> one Claude -> the system
PA = [(40, 300), (415, 220), (790, 330), (60, 760), (430, 680), (780, 800)]     # tile left, top (250 px)
PA_ROT = [-5, 3, 6, 4, -4, -6]
PT = 250
HOP = [(0, "stryb", -0.1), (1, "mizh", 0.0), (2, "kupoiu", 0.0), (5, "riznykh", 0.0), (4, "shi", 0.0),
       (3, "shi", 0.42)]
PK = 110
CEN = (540, 620)
BIG = 380
ROWS_TOP = 130          # inside the sheet
SHEET = (-70, 240, 1220, 940)


def pk_pos(ti):
    x, y = PA[ti]
    return x + PT // 2 - PK // 2, y - 62


@beat
def t_takeover():
    tiles = ""
    for i, ln in enumerate(LINES):
        x, y = PA[i]
        tiles += tile("pa%d" % i, PT, x, y, "pearl", glyph(ln["wg"], PT))
        tiles += '<div class="lbl hide" id="pl%d" style="left:%dpx;top:%dpx">%s</div>' % (i, x - 40, y + 268, ln["wn"])
    coins = "".join(tile("ce%d" % i, 84, PA[i][0] + 196, PA[i][1] - 26, "jelly",
                         '<span class="wmark" style="font-size:50px;color:#fff">€</span>',
                         extra_cls="circ", ring=False) for i in range(6))
    p0 = pk_pos(0)
    puck = tile("pk", PK, p0[0], p0[1], "jelly", stroke("person"), extra_cls="circ", ring=False)
    big = tile("tkC", BIG, CEN[0] - BIG // 2, CEN[1] - BIG // 2, "jelly", g.mark("claude"))
    rows = ""
    for i, ln in enumerate(LINES):
        rows += ('<div class="row" id="rw%d" style="top:%dpx">%s<div class="rn">%s</div>'
                 '<div class="tg"><div class="on" id="tgO%d"></div><div class="kn" id="tgK%d"></div></div>%s</div>'
                 % (i, ROWS_TOP + i * 125,
                    tile("rwT%d" % i, 96, 0, 4, "jelly", glyph(ln["rg"], 96), hide=False, ring=False),
                    ln["rn"], i, i, '<div class="hr"></div>' if i < 5 else ""))
    sx, sy, sw, sh = SHEET
    sheet = ('<div class="sheet hide" id="sh" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx" '
             'data-layout-allow-overflow>%s<div class="sheen"></div></div>' % (sx, sy, sw, sh, rows))
    badge = tile("tkP", 100, 590, 222, "pearl", stroke("person"), extra_cls="circ")
    L.append('<div class="g full" id="gT"><div class="tkg"></div><div class="aurs"></div><div class="grain"></div>'
             + tiles + coins + puck + sheet + big + badge + '</div>')

    sfx("whoosh-short", T["treba"] - 0.04)
    sfx("kaching", T["platyty"] + 0.12)
    sfx("whoosh-short", T["a"] + 0.02, -2)
    sfx("click-soft", T["nalasht"] + 0.1)
    sfx("whoosh-short", T["tebe"] + 0.05, -2)

    o = ["""
  G.irisOpen("#gT", @treba+0.0, 540, 155, 0.62);
  drift1("#gT", @treba, @tebe+0.5-@treba);"""]
    for i in range(6):
        o.append('  gsap.set("#pa%d", {rotation: %d});' % (i, PA_ROT[i]))
        o.append('  arr("#pa%d", %.3f, {s: 0.5, y: 40, d: 0.8});' % (i, T["treba"] + 0.22 + i * 0.07))
        o.append('  bin("#pl%d", %.3f, 8, 0.3);' % (i, T["treba"] + 0.36 + i * 0.07))
    # the puck hops tile to tile
    cx, cy = p0
    first = True
    for ti, key, off in HOP:
        t = T[key] + off
        px, py = pk_pos(ti)
        if first:
            o.append('  arr("#pk", %.3f, {s: 0.3, y: -60, d: 0.6});' % t)
            o.append('  G.bump("#pa%d", %.3f);' % (ti, t + 0.25))
            first = False
            continue
        nx, ny = px - p0[0], py - p0[1]
        apex = min(cy - p0[1], ny) - 150
        o.append('  tl.to("#pk", {x: %d, duration: 0.32, ease: "power1.inOut"}, %.3f);' % (nx, t))
        o.append('  tl.to("#pk", {y: %d, duration: 0.16, ease: "power2.out"}, %.3f);' % (apex, t))
        o.append('  tl.to("#pk", {y: %d, duration: 0.16, ease: "power2.in"}, %.3f);' % (ny, t + 0.16))
        o.append('  G.bump("#pa%d", %.3f);' % (ti, t + 0.3))
        cx, cy = px, py
    # a € on each
    for i in range(6):
        o.append('  arr("#ce%d", %.3f, {s: 0.2, y: 20, d: 0.5});' % (i, T["platyty"] + 0.08 + i * 0.07))
    # everything sucked into one point
    ta = T["a"] + 0.04
    for i in range(6):
        x, y = PA[i]
        dx, dy = CEN[0] - (x + PT // 2), CEN[1] - (y + PT // 2)
        o.append('  tl.to(["#pa%d", "#pl%d"], {x: %d, y: %d, scale: 0.15, autoAlpha: 0, duration: 0.44, ease: "power3.in"}, %.3f);'
                 % (i, i, dx, dy, ta + i * 0.02))
        cdx, cdy = CEN[0] - (x + 196 + 42), CEN[1] - (y - 26 + 42)
        o.append('  tl.to("#ce%d", {x: %d, y: %d, scale: 0.15, autoAlpha: 0, duration: 0.44, ease: "power3.in"}, %.3f);'
                 % (i, cdx, cdy, ta + i * 0.02))
    pdx, pdy = CEN[0] - (p0[0] + PK // 2), CEN[1] - (p0[1] + PK // 2)
    o.append('  tl.to("#pk", {x: %d, y: %d, scale: 0.2, autoAlpha: 0, duration: 0.44, ease: "power3.in"}, %.3f);'
             % (pdx, pdy, ta + 0.1))
    o.append("""
  arr("#tkC", @vziaty-0.08, {s: 0.25, y: 0, d: 0.85, blur: 14});
  G.ripple("#tkCR", @odnu); G.bump("#tkC", @odnu+0.02); shn("#tkC .sheen", @odnu+0.1);
  /* it rises onto the sheet; the system switches on */
  tl.to("#tkC", {y: %d, scale: %.3f, duration: 0.62, ease: SP}, @i2-0.04);
  gsap.set("#sh", {transformOrigin: "50%% 0%%"});
  arr("#sh", @i2+0.0, {s: 0.9, y: 90, d: 0.8});
  shn("#sh > .sheen", @i2+0.45);""" % (170 - CEN[1], 220.0 / BIG))
    for i in range(6):
        o.append('  tl.fromTo("#rw%d", {autoAlpha: 0, x: -40}, {autoAlpha: 1, x: 0, duration: 0.45, ease: SP}, %.3f);'
                 % (i, T["i2"] + 0.14 + i * 0.05))
        t = T["nalasht"] + 0.06 + i * 0.19
        o.append('  tl.to("#tgO%d", {autoAlpha: 1, duration: 0.16}, %.3f);' % (i, t))
        o.append('  tl.to("#tgK%d", {x: 58, duration: 0.34, ease: SP}, %.3f);' % (i, t))
    o.append("""
  arr("#tkP", @pid-0.04, {s: 0.2, y: 0, d: 0.6}); G.ripple("#tkPR", @pid+0.2);
  G.irisClose("#gT", @tebe+0.03, 540, 160, 0.42);""")
    return js("\n".join(o))


# ===========================================================================
# C · the full dock again («так само»), the comment
@beat
def c_cta():
    hx, hy, hs = HUB
    dock = "".join(tile("dr%d" % i, SLOT, SLOT_X[i] - SLOT // 2, SLOT_Y - SLOT // 2, "jelly",
                        glyph(ln["rg"], SLOT), ring=False) for i, ln in enumerate(LINES))
    cm = ('<div class="dglass edge hide" id="cm" style="left:90px;top:300px;width:900px;height:150px;border-radius:75px">'
          '<div class="tw circ" style="left:27px;top:27px;width:96px;height:96px"><div class="pearl">%s</div></div>'
          '<div class="ph" id="cmPh">Додайте коментар…</div><div class="pl hide" id="cmPl">+</div>'
          '<div class="tw circ" id="cmS" style="left:777px;top:27px;width:96px;height:96px"><div class="jelly">%s</div></div>'
          '<div class="ck" id="ckS" style="left:825px;top:75px"></div>'
          '<div class="shc"><div class="sheen"></div></div></div>' % (stroke("person"), stroke("up")))
    L.append('<div class="g full" id="gR">'
             '<div class="shelf edge hide" id="dock2" style="left:40px;top:75px;width:1000px;height:160px"></div>'
             + dock + tile("hub2", hs, hx - hs // 2, hy - hs // 2, "jelly", g.mark("claude")) + cm + '</div>')
    sfx("click", T["koment"] + 0.08)
    o = ["""
  tl.set("#gR", {autoAlpha: 1}, @tebe+0.3);
  arr("#dock2", @tebe+0.3, {s: 0.9, y: 0, d: 0.7});
  arr("#hub2", @tebe+0.34, {s: 0.5, y: 0, d: 0.7}); G.ripple("#hub2R", @yakshcho+0.25);"""]
    for i in range(6):
        o.append('  arr("#dr%d", %.3f, {s: 0.3, y: 0, d: 0.6});' % (i, T["tebe"] + 0.42 + i * 0.05))
    o.append("""
  arr("#cm", @to-0.08, {s: 0.7, y: 40, d: 0.75});
  tl.set("#cmPh", {autoAlpha: 0}, @plius-0.03);
  tl.fromTo("#cmPl", {autoAlpha: 0, scale: 1.8}, {autoAlpha: 1, scale: 1, duration: 0.3, ease: POP}, @plius-0.03);
  tl.to("#cmS", {scale: 0.86, duration: 0.09, ease: "power2.out"}, @koment+0.08);
  tl.to("#cmS", {scale: 1, duration: 0.4, ease: SP}, @koment+0.17);
  tl.fromTo("#ckS", {scale: 0.3, autoAlpha: 0.95}, {scale: 1.9, autoAlpha: 0, duration: 0.5, ease: "power2.out", immediateRender: false}, @koment+0.1);
  shn("#cm .sheen", @koment+0.15);""")
    return js("\n".join(o))


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


def span_words(a, b):
    return (round(a - 0.02, 3), round(b, 3), "")


# the right card says the tool's name while she says it (STYLE.md §2b.1)
BLACKOUT = [
    span_words(T["openr"], E("OpenRouter", 2.02)),
    span_words(T["fathom"], E("Fathom", 5.227)),
    span_words(T["dyz"], E(u"дизайн-система", 7.14)),
    span_words(T["winds"], E("Windsor", 10.232)),
    span_words(T["skil"], E(u"монтажу", 12.674)),
    span_words(T["skily"], E(u"скіли", 15.376)),
]


def check():
    assert not NO_PAINT, "this cut has no closeups; re-check the beats if it gets one"
    assert T["k6"] + 0.12 + 0.34 < T["treba"] + 0.05, "sixth tile still flying when the iris opens"


def main():
    check()
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
        title=u"Reel 34 — Все в одному Claude",
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
