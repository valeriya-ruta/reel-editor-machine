# -*- coding: utf-8 -*-
"""Reel 24 — «Штучний інтелект тепер може замінити монтажерів…». Posts 2026-10-08.

v1 followed her idea note (plain version shrinking into a «до» window). Her
review, 2026-10-05: *"i wanted all the edits from very beginning because then
i would have put the before and after by myself in edits ... removing the
"before" from the edits and filling up the beginning, starting from second 3"*.
So this is the fully edited version from 0:03 — she builds the before/after
herself. 0 -> 3 s (the hook) stays clean; her punch-in on «і це не хайп і не
жарт» stays clear (captions only).

Chain:  «зберегти тобі сотні євро на місяць» — € coins multiply on a shelf,
kaching on «євро» -> clear for her closeup -> on «Цей рілс» the shelf comes
back and her profile grid flicks past («десятки інших») -> the grid
clears into an editor: Claude lands, tracks fill by themselves under a running
playhead («самостійно») -> Claude rises into a subscription card, a frame draws
round it («в рамках»), «включено» -> the card becomes a clock that stops short
of the hour -> the iris opens out of the clock: a
design-system sheet with ghost slots, lit on «налаштувати дизайн-систему» ->
the sheet shrinks onto a cable into Claude, skill chips snap in from both
edges; «розкажу згодом» blurs their names -> the iris closes onto the sheet,
which stays above her head as a near card -> it clears for an IG comment that
types «система» and posts -> the DM with the instruction lands above it.

usage: python build.py   (then: python ../tools/sfx.py mix 24)
"""
import io
import json
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))
from kit import Kit, esc  # noqa: E402
from glass import Glass  # noqa: E402

CUT = json.load(io.open(os.path.join(ROOT, "work", "r24", "cut.json"), encoding="utf-8"))
DUR = 26.183           # set from the plate's frame count after cut.py --render
FPS = 30
k = Kit(width=1080, height=1920, fps=FPS, duration=DUR)
g = Glass(["claude", "instagram"])
k.css(g.css())

NO_PAINT = [tuple(x) for x in CUT["no_paint"]]          # her punch-in, «і це не хайп і не жарт»

CAPS = k.load_captions(os.path.join(ROOT, "work", "r24", "captions.json"))
FIX = {u"клод": u"Клод"}
for c in CAPS:
    c["w"] = FIX.get(c["w"], c["w"])
for _a, _b in zip(CAPS, CAPS[1:]):
    _a["e"] = round(max(_a["s"] + 0.10, _b["s"] - 0.085), 3)
CAPS[-1]["e"] = round(min(CAPS[-1]["e"], DUR), 3)


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
    "zberehty": S(u"зберегти", 2.91), "sotni": S(u"сотні", 3.71), "ievro": S(u"євро", 4.33),
    "misiats": S(u"місяць", 4.95), "misiatse": E(u"місяць", 4.95),
    "tsei": S(u"Цей", 7.44), "rils": S(u"рілс", 7.66), "yak": S(u"як", 7.98),
    "desiatky": S(u"десятки", 8.2), "inshykh": S(u"інших", 8.68),
    "meni": S(u"мені", 9.30), "zmont": S(u"змонтував", 9.42), "klod": S(u"Клод", 10.08),
    "samost": S(u"самостійно", 10.37), "samoste": E(u"самостійно", 10.37),
    "v": S(u"в", 11.42), "ramkakh": S(u"рамках", 11.64), "moiei": S(u"моєї", 11.94),
    "pidpysky": S(u"підписки", 12.26), "pidpyskye": E(u"підписки", 12.26),
    "menshe": S(u"менше", 13.18), "nizh": S(u"ніж", 13.46), "hodynu": S(u"годину", 13.80),
    "hodynue": E(u"годину", 13.80),
    "dlia": S(u"Для", 14.39), "zrobyty": S(u"зробити", 15.07), "treba": S(u"треба", 15.77),
    "lyshe": S(u"лише", 16.15), "nalasht": S(u"налаштувати", 16.55),
    "dyzsys": S(u"дизайн-систему", 17.18), "dyzsyse": E(u"дизайн-систему", 17.18),
    "ta": S(u"та", 17.92), "pidkl": S(u"підключити", 18.03), "pravylni": S(u"правильні", 18.59),
    "skily": S(u"скіли", 19.17), "pro": S(u"Про", 19.57), "skily2": S(u"скіли", 19.80),
    "rozkazhu": S(u"розкажу", 20.18), "zghodom": S(u"згодом", 20.42),
    "ashchob": S(u"а", 20.96), "nalasht2": S(u"налаштувати", 21.16), "dyzain": S(u"дизайн", 21.60),
    "systemu": S(u"систему", 21.92), "pyshy": S(u"пиши", 22.54), "slovo": S(u"слово", 22.70),
    "systema": S(u"система", 22.88), "systemae": E(u"система", 22.88),
    "koment": S(u"коментарі", 23.48), "komente": E(u"коментарі", 23.48),
    "i_": S(u"і", 24.10), "otrymai": S(u"отримай", 24.32), "bezkosht": S(u"безкоштовну", 24.76),
    "instr": S(u"інструкцію", 25.39),
    "dur": DUR,
}
T["tS"] = round(T["tsei"] - 0.03, 3)          # the shelf comes back after her closeup
T["wEnd"] = round(T["dlia"] + 0.95, 3)        # the shelf is under the iris by now
T["mOut"] = round(T["misiatse"] - 0.1, 3)     # the coins clear before her closeup


def js(src, **extra):
    """`@name`, `@name+0.12`, `@name-0.1` -> one literal time."""
    vals = dict(T)
    vals.update(extra)

    def rep(m):
        v = vals[m.group(1)] + (float(m.group(2)) if m.group(2) else 0.0)
        return "%.3f" % v
    return re.sub(r"@(\w+)([+-]\d+(?:\.\d+)?)?", rep, src)


# ---------------------------------------------------------------------------
# Sound design (tools/sfx.py). Nothing on the hook (0-3 s) or her closeup.
SFX = []


def sfx(name, t, db=0):
    if isinstance(t, str):
        t = float(js(t))
    assert t >= T["zberehty"] - 0.05, "no sound on the hook"
    assert not any(a - 0.05 < t < b for a, b in NO_PAINT), ("sfx inside a closeup", name, t)
    SFX.append({"t": round(max(0.0, t), 3), "name": name, "db": db})


# ---------------------------------------------------------------------------
# Glyphs
STROKES = {
    "up": '<path d="M12 19.2V5.4M6.2 11l5.8-5.8 5.8 5.8"/>',
    "check": '<path d="M5.4 12.6l4.3 4.3 8.9-9.5"/>',
    "person": '<circle cx="12" cy="8.2" r="3.6"/><path d="M4.8 20c.9-3.8 3.7-5.8 7.2-5.8s6.3 2 7.2 5.8"/>',
    "puzzle": ('<path d="M9.2 5.6a2.3 2.3 0 0 1 4.6 0V7h3.3c.6 0 1 .4 1 1v3.2h-1.3a2.3 2.3 0 0 0 0 4.6h1.3V19'
               'c0 .6-.4 1-1 1h-3.2v-1.3a2.3 2.3 0 0 0-4.6 0V20H6c-.6 0-1-.4-1-1v-3.3h1.4a2.3 2.3 0 0 0 0-4.6'
               'H5V8c0-.6.4-1 1-1h3.2z"/>'),
    "heart": '<path d="M12 19.5s-7.2-4.4-7.2-9.4A3.9 3.9 0 0 1 12 8a3.9 3.9 0 0 1 7.2 2.1c0 5-7.2 9.4-7.2 9.4z"/>',
    "reel": '<rect x="4" y="4" width="16" height="16" rx="4.5"/><path d="M10.4 9.3v5.4l4.4-2.7z"/>',
}
PERSON_FILL = ('<svg class="sil" viewBox="0 0 100 100"><circle cx="50" cy="38" r="17"/>'
               '<path d="M14 104 C 16 72 34 60 50 60 C 66 60 84 72 86 104 Z"/></svg>')


def stroke(name, cls="sk"):
    return '<svg class="%s" viewBox="0 0 24 24">%s</svg>' % (cls, STROKES[name])


def tile(tid, size, x, y, material, inner, extra_cls="", hide=True, ring=True):
    r = ('<div class="sqring" id="%sR" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx"></div>'
         % (tid, x, y, size, size)) if ring else ""
    return ('%s<div class="tw%s %s" id="%s" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx">'
            '<div class="%s">%s<div class="sheen"></div></div></div>'
            % (r, " hide" if hide else "", extra_cls, tid, x, y, size, size, material, inner))


k.css("""
.abs { position: absolute; }
.hide { opacity: 0; visibility: hidden; }
.tw { position: absolute; }
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

/* ---- «сотні євро на місяць»: € coins on a shelf ---- */
.eur { position: relative; z-index: 1; font-size: 74px; font-weight: 900; color: #fff; line-height: 1;
  letter-spacing: -0.03em; }
#mL { position: absolute; left: 0; width: 840px; top: 236px; text-align: center; color: #fff;
  font-size: 80px; font-weight: 900; letter-spacing: -0.035em; line-height: 1; white-space: nowrap; }

/* ---- the shelf ---- */
#sh { overflow: hidden; }
.th { position: absolute; width: 186px; height: 248px; border-radius: 24px; overflow: hidden;
  box-shadow: inset 0 1.5px 1px rgba(255,255,255,0.45), 0 14px 26px -12px rgba(20,2,8,0.55); }
.th.v0 { background: linear-gradient(160deg, #e0204b 0%, #8d0d24 60%, #5a0718 100%); }
.th.v1 { background: linear-gradient(160deg, #ffe3ec 0%, #ffb3c9 100%); }
.th.v2 { background: linear-gradient(160deg, #3a2430 0%, #17141c 100%); }
.th.v3 { background: linear-gradient(160deg, #ffffff 0%, #f4dfe5 100%); }
.th.v4 { background: linear-gradient(160deg, #ff8ab0 0%, #c41434 100%); }
.th .sil { position: absolute; left: 28px; top: 112px; width: 130px; height: 136px; fill: rgba(255,255,255,0.78); }
.th.v1 .sil, .th.v3 .sil { fill: rgba(141,13,36,0.42); }
.th .cb { position: absolute; left: 46px; top: 208px; width: 94px; height: 15px; border-radius: 6px; background: #fff;
  box-shadow: 0 2px 6px rgba(0,0,0,0.25); }
.th.v1 .cb, .th.v3 .cb { background: #17141c; }
.th .rg { position: absolute; right: 12px; top: 12px; width: 30px; height: 30px; fill: none; stroke: #fff;
  stroke-width: 2.2; stroke-linejoin: round; }
.th.v1 .rg, .th.v3 .rg { stroke: #8d0d24; }

/* the editor: lanes, ghost clips, lit clips, playhead */
#ed { position: absolute; left: 222px; top: 92px; width: 400px; height: 290px; }
.lane { position: absolute; left: 0; width: 400px; height: 68px; border-radius: 18px;
  background: rgba(255,255,255,0.10); box-shadow: inset 0 1.5px 1px rgba(255,255,255,0.28); }
.clp { position: absolute; }
.clp.vid { top: 8px; height: 52px; border-radius: 12px;
  background: linear-gradient(165deg, #e0204b 0%, #ab112e 50%, #6b081c 100%);
  box-shadow: inset 0 2px 1px rgba(255,255,255,0.45); }
.clp.cpb { top: 21px; height: 26px; border-radius: 8px; background: #fff; }
.clp.wav { width: 6px; border-radius: 3px; background: #ffb3c9; }
#edGh .clp { opacity: 0.22; }
#edGh .clp.vid, #edGh .clp.cpb, #edGh .clp.wav { background: #fff; box-shadow: none; }
#edLit { position: absolute; inset: 0; }
#ph { position: absolute; left: -3px; top: -10px; width: 6px; height: 300px; border-radius: 3px; background: #fff;
  box-shadow: 0 0 14px rgba(255,110,156,0.9); }
#ph b { position: absolute; left: -9px; top: -8px; width: 24px; height: 24px; border-radius: 50%; display: block;
  background: linear-gradient(165deg, #ff8ab0 0%, #e0204b 100%); box-shadow: 0 0 0 3px #fff; }
.ruler { position: absolute; left: 0; top: 0; width: 400px; height: 16px; }

/* the subscription card (the same shelf) */
.ctr { position: absolute; left: 0; width: 656px; text-align: center; color: #fff; }
#sbT { top: 212px; font-size: 56px; font-weight: 700; letter-spacing: -0.02em; }
#sbS { top: 284px; font-size: 34px; font-weight: 500; color: rgba(255,255,255,0.72); }
#sbC { position: absolute; left: 214px; top: 352px; width: 228px; height: 64px; border-radius: 32px;
  display: flex; align-items: center; justify-content: center; gap: 10px;
  background: linear-gradient(160deg, #ffffff 0%, #fff5f8 52%, #f5dfe6 100%); color: #b4122f;
  font-size: 30px; font-weight: 700; box-shadow: inset 0 2px 1px #fff, 0 18px 34px -14px rgba(30,4,12,0.6); }
#sbC svg { width: 34px; height: 34px; fill: none; stroke: #b4122f; stroke-width: 3; stroke-linecap: round;
  stroke-linejoin: round; }
.frm { fill: none; stroke: #ffb3c9; stroke-width: 6; stroke-linecap: round;
  filter: drop-shadow(0 0 8px rgba(255,110,156,0.8)); }

/* the clock */
#clk svg { position: absolute; inset: 0; width: 100%; height: 100%; z-index: 1; }
#clk .trk { fill: none; stroke: rgba(23,20,28,0.08); stroke-width: 16; }
#clk .arc { fill: none; stroke: url(#gArc); stroke-width: 16; stroke-linecap: round; }
#clk .tick { stroke: rgba(23,20,28,0.30); stroke-width: 4; stroke-linecap: round; }
#clk .hand { stroke: #17141c; stroke-width: 9; stroke-linecap: round; }
#clk .hub { fill: #b4122f; }
#clkL { position: absolute; left: 0; width: 656px; top: 296px; text-align: center; color: #fff;
  font-size: 80px; font-weight: 900; letter-spacing: -0.03em; line-height: 1; }

/* ---- the design-system sheet ---- */
.ds { position: absolute; width: 1160px; height: 1290px; }
.ds i { position: absolute; display: block; font-style: normal; }
.ds .lbl { font-size: 26px; font-weight: 700; letter-spacing: 0.16em; color: rgba(23,20,28,0.42); }
.ds .ttl { font-size: 78px; font-weight: 900; letter-spacing: -0.035em; color: #17141c; line-height: 1; }
.ds .aa { font-size: 260px; font-weight: 900; letter-spacing: -0.05em; color: #17141c; line-height: 1; }
.ds .aa.gh { color: rgba(23,20,28,0.06); }
.ds .fn { font-size: 46px; font-weight: 700; letter-spacing: -0.02em; color: #17141c; }
.ds .tb { border-radius: 10px; transform-origin: 0 50%; }
.ds .tb.h { background: #17141c; } .ds .tb.s { background: rgba(23,20,28,0.32); } .ds .tb.b { background: rgba(23,20,28,0.13); }
.ds .tb.gh { background: rgba(23,20,28,0.05); }
.ds .sw { width: 136px; height: 136px; border-radius: 50%; box-shadow: inset 0 2px 1px rgba(255,255,255,0.5), 0 16px 30px -14px rgba(30,4,12,0.5); }
.ds .sw.gh, .ds .cg { box-shadow: none; background: none; border: 4px dashed rgba(23,20,28,0.14); }
.ds .hx { width: 136px; text-align: center; font-size: 22px; font-weight: 700; letter-spacing: 0.04em; color: rgba(23,20,28,0.5); }
.ds .btn { display: flex; align-items: center; justify-content: center; border-radius: 50px; color: #fff;
  font-size: 40px; font-weight: 700; letter-spacing: -0.01em;
  background: linear-gradient(165deg, #e0204b 0%, #ab112e 46%, #6b081c 100%);
  box-shadow: inset 0 2px 1px rgba(255,255,255,0.5), 0 20px 36px -16px rgba(70,4,20,0.6); }
.ds .tgl { border-radius: 36px; background: rgba(23,20,28,0.14); }
.ds .tgl .on { position: absolute; inset: 0; border-radius: 36px; background: linear-gradient(165deg, #e0204b 0%, #8d0d24 100%); }
.ds .tgl .kn { left: 6px; top: 6px; width: 60px; height: 60px; border-radius: 50%; background: #fff;
  box-shadow: 0 4px 10px rgba(30,4,12,0.3); }
.ds .chp { display: flex; align-items: center; gap: 14px; padding: 0 26px; border-radius: 36px; background: #fbe3ea; }
.ds .chp b { width: 20px; height: 20px; border-radius: 50%; background: #b4122f; display: block; }
.ds .chp u { width: 120px; height: 16px; border-radius: 8px; background: rgba(180,18,47,0.55); display: block; }
.ds .mc { border-radius: 30px; overflow: hidden; background: linear-gradient(170deg, #ffffff 0%, #fdf0f4 100%);
  box-shadow: inset 0 0 0 2px rgba(23,20,28,0.06), 0 22px 40px -20px rgba(30,4,12,0.45); }
.ds .mc i { border-radius: 8px; }
.hr { height: 3px; background: rgba(23,20,28,0.08); }

/* skill chips */
.skc { position: absolute; width: 400px; height: 110px; border-radius: 55px; display: flex; align-items: center;
  background: linear-gradient(160deg, #ffffff 0%, #fff5f8 52%, #f5dfe6 100%);
  box-shadow: inset 0 2px 1px #fff, inset 0 -16px 26px -14px rgba(180,18,47,0.16), 0 30px 54px -22px rgba(8,0,3,0.75); }
.skc .pz { position: absolute; left: 16px; top: 16px; width: 78px; height: 78px; }
.skc .pz .sk { stroke-width: 2.1; }
.skc span { position: absolute; left: 116px; top: 0; line-height: 110px; font-size: 44px; font-weight: 700;
  letter-spacing: -0.02em; color: #17141c; }

/* the comment */
#cmIn .phd, #cmIn .tx { position: absolute; left: 44px; top: 0; line-height: 120px; font-size: 40px; }
#cmIn .phd { color: rgba(255,255,255,0.5); font-weight: 500; }
#cmIn .tx { color: #fff; font-weight: 700; }
#cmIn .tx::after { content: ""; display: inline-block; width: 3px; height: 44px; margin-left: 4px; vertical-align: -8px;
  background: #ff8ab0; }
#cmRow .nm { position: absolute; left: 134px; top: 30px; width: 190px; height: 20px; border-radius: 10px;
  background: rgba(255,255,255,0.32); }
#cmRow .tx { position: absolute; left: 134px; top: 62px; font-size: 44px; font-weight: 700; color: #fff; }
#cmRow .ht { position: absolute; right: 44px; top: 42px; width: 52px; height: 52px; fill: none; stroke: rgba(255,255,255,0.7);
  stroke-width: 2.2; }

/* the DM */
#dm .app { position: absolute; left: 168px; top: 36px; font-size: 30px; font-weight: 700; color: rgba(255,255,255,0.72); }
#dm .tm  { position: absolute; left: 640px; top: 38px; font-size: 26px; font-weight: 500; color: rgba(255,255,255,0.5); }
#dm .msg { position: absolute; left: 168px; top: 84px; width: 560px; font-size: 41px; font-weight: 700; color: #fff;
  letter-spacing: -0.012em; line-height: 1.15; }
.doc { position: absolute; border-radius: 18px; overflow: hidden;
  background: linear-gradient(172deg, #ffffff 0%, #fdf0f4 100%); box-shadow: 0 14px 26px -10px rgba(10,0,4,0.6); }
.doc i { position: absolute; display: block; font-style: normal; }
.doc .aa { left: 12px; top: 34px; font-size: 40px; font-weight: 900; color: #17141c; letter-spacing: -0.05em; line-height: 1; }
.doc .d { width: 18px; height: 18px; border-radius: 50%; top: 92px; }
""")

L = []
BEATS = []


def beat(fn):
    BEATS.append(fn)
    return fn


# ===========================================================================
# A · «зберегти тобі сотні євро на місяць» — one € coin, then hundreds; kaching
MS = (120, 150, 840, 380)          # x, y, w, h of the coin shelf (bottom 530, her head ≈ 660 at 1.10)
COIN, CGAP = 132, 22


@beat
def a_money():
    x0 = (MS[2] - (5 * COIN + 4 * CGAP)) // 2
    coins = "".join(tile("co%d" % i, COIN, x0 + i * (COIN + CGAP), 58, "jelly", '<span class="eur">€</span>',
                         "circ coin", ring=False) for i in range(5))
    L.append('<div class="g full" id="gM">'
             '<div class="shelf edge hide" id="shM" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx;border-radius:64px">'
             '%s<div class="hide" id="mL">сотні € на місяць</div>'
             '<div class="shc"><div class="sheen"></div></div></div></div>' % (MS + (coins,)))
    sfx("pop", T["zberehty"] + 0.1, -4)
    sfx("kaching", T["ievro"] + 0.02)
    out = js("""
  tl.set("#gM", {autoAlpha: 1}, @zberehty-0.02);
  arr("#shM", @zberehty, {s: 0.86, y: 30, d: 0.8});
  arr("#co2", @zberehty+0.1, {s: 0.3, y: 20, d: 0.7});""")
    for i in (0, 1, 3, 4):
        out += js("""
  tl.fromTo("#co%d", {autoAlpha: 0, x: %d, scale: 0.4}, {autoAlpha: 1, x: 0, scale: 1, duration: 0.6, ease: POP,
            immediateRender: false}, @sotni%+.2f);""" % (i, (2 - i) * (COIN + CGAP), -0.04 + 0.05 * abs(2 - i)))
    out += js("""
  gsap.set(["#co0", "#co1", "#co3", "#co4"], {autoAlpha: 0});
  arr("#mL", @sotni+0.02, {s: 0.7, y: 18, d: 0.6});
  tl.to(".coin", {y: -22, duration: 0.16, stagger: 0.04, ease: "power2.out"}, @ievro);
  tl.to(".coin", {y: 0, duration: 0.5, stagger: 0.04, ease: SP}, @ievro+0.16);
  shn("#shM .shc .sheen", @ievro+0.05);
  G.bump("#mL", @misiats);
  bout("#shM", @mOut, 10, 0.22);
  tl.set("#gM", {autoAlpha: 0}, @mOut+0.24);""")
    return out


# ===========================================================================
# B · the shelf comes back on «Цей рілс» — her profile grid flicks past: «десятки інших»
SH = (212, 130, 656, 461)          # x, y, w, h of the shelf, centred
ROWS = 6


@beat
def b_grid():
    thumbs = ""
    for r in range(ROWS):
        for cidx in range(3):
            v = (r * 3 + cidx * 2 + r) % 5
            thumbs += ('<div class="th v%d" style="left:%dpx;top:%dpx">%s<i class="cb abs"></i>%s</div>'
                       % (v, 33 + cidx * 202, 24 + r * 264, PERSON_FILL, stroke("reel", "rg")))
    strip = '<div class="abs" id="gs" style="left:0;top:0;width:656px;height:%dpx">%s</div>' % (ROWS * 264, thumbs)
    L.append('<div class="g full" id="gB">'
             '<div class="shelf edge hide" id="sh" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx;border-radius:56px">'
             '%s{{ED}}</div></div>' % (SH + (strip,)))
    sfx("pop", T["desiatky"] + 0.05, -3)
    return js("""
  tl.set("#gB", {autoAlpha: 1}, @tS);
  arr("#sh", @tS+0.03, {s: 0.86, y: 30, d: 0.85});
  tl.fromTo("#gs", {y: -%d}, {y: 0, duration: 0.95, ease: "expo.out"}, @desiatky-0.02);
  bout("#gs", @meni-0.06, 10, 0.26);
  tl.set("#gB", {autoAlpha: 0}, @wEnd);""" % ((ROWS - 2) * 264 + 140))


# ===========================================================================
# C · the editor: Claude lands, the tracks fill by themselves
VID = [(6, 96), (108, 60), (174, 118), (298, 52), (356, 38)]
CAPB = [(6, 54), (66, 40), (112, 70), (188, 46), (240, 64), (310, 36), (352, 42)]


def lanes(prefix):
    h = ""
    for x, w in VID:
        h += '<div class="clp vid" style="left:%dpx;width:%dpx"></div>' % (x, w)
    l0 = '<div class="abs" style="left:0;top:26px;width:400px;height:68px">%s</div>' % h
    h = ""
    for x, w in CAPB:
        h += '<div class="clp cpb" style="left:%dpx;width:%dpx"></div>' % (x, w)
    l1 = '<div class="abs" style="left:0;top:112px;width:400px;height:68px">%s</div>' % h
    h = ""
    for i in range(35):
        hh = 10 + (i * 37 + 11) % 34
        h += '<div class="clp wav" style="left:%dpx;top:%dpx;height:%dpx"></div>' % (10 + i * 11, 34 - hh // 2, hh)
    l2 = '<div class="abs" style="left:0;top:198px;width:400px;height:68px">%s</div>' % h
    return '<div class="abs" id="%s" style="left:0;top:0;width:400px;height:290px">%s%s%s</div>' % (prefix, l0, l1, l2)


def editor_html():
    ruler = ''.join('<path d="M%d %d V 16"/>' % (i * 40, 8 if i % 5 else 0) for i in range(11))
    ed = ('<div class="hide" id="ed">'
          '<svg class="ruler" viewBox="0 0 400 16" style="overflow:visible"><g stroke="rgba(255,255,255,0.45)" '
          'stroke-width="3" stroke-linecap="round">%s</g></svg>'
          '<div class="lane" style="top:26px"></div><div class="lane" style="top:112px"></div>'
          '<div class="lane" style="top:198px"></div>%s%s'
          '<div id="ph"><b></b></div></div>' % (ruler, lanes("edGh"), lanes("edLit")))
    claude = tile("cC", 150, 36, 156, "jelly", g.mark("claude"))
    return ed + claude


@beat
def c_editor():
    sfx("pop", T["klod"] + 0.02)
    return js("""
  arr("#ed", @zmont-0.04, {s: 0.9, x: 30, y: 0, d: 0.7});
  arr("#cC", @klod-0.06, {s: 0.3, y: 20, d: 0.75});
  G.ripple("#cCR", @klod+0.25);
  gsap.set("#edLit", {clipPath: "inset(0px 100% 0px 0px)"});
  gsap.set("#ph", {x: 0});
  tl.fromTo("#edLit", {clipPath: "inset(0px 100% 0px 0px)"}, {clipPath: "inset(0px 0% 0px 0px)", duration: 0.9,
            ease: "power1.inOut", immediateRender: false}, @samost+0.02);
  tl.fromTo("#ph", {x: 0}, {x: 400, duration: 0.9, ease: "power1.inOut", immediateRender: false}, @samost+0.02);
  G.bump("#cC", @samoste-0.1);
  bout("#ed", @v-0.1, 10, 0.26);""")


# ===========================================================================
# D · «в рамках моєї підписки» — Claude rises into the subscription card
@beat
def d_sub():
    sfx("pop", T["pidpysky"] + 0.02, -1)
    return js("""
  tl.to("#cC", {x: 217, y: -118, duration: 0.65, ease: SP}, @v-0.04);
  bin("#sbT", @v+0.1, 8, 0.32);
  tl.fromTo("#sbT", {y: 16}, {y: 0, duration: 0.5, ease: SP}, @v+0.1);
  tl.set("#frm", {autoAlpha: 1}, @ramkakh-0.02); draw2("frm", @ramkakh-0.02, 0.6);
  arr("#sbS", @pidpysky-0.03, {s: 0.7, y: 14, d: 0.6});
  arr("#sbC", @pidpysky+0.28, {s: 0.4, y: 10, d: 0.6});
  shn("#sh .shc .sheen", @pidpysky+0.3);
  bout(["#cC", "#sbT", "#sbS", "#sbC", "#frm"], @menshe-0.2, 10, 0.24);""")


def sub_html():
    w, h = SH[2], SH[3]
    return ('<div class="ctr hide" id="sbT">Claude</div><div class="ctr hide" id="sbS">Підписка</div>'
            '<div class="hide" id="sbC">%s<span>включено</span></div>'
            '<svg class="abs" width="%d" height="%d" style="left:0;top:0;overflow:visible">'
            '<rect class="frm hide" id="frm" x="18" y="18" width="%d" height="%d" rx="42"/></svg>'
            '<div class="shc"><div class="sheen"></div></div>'
            % (STROKES["check"].replace("<path", '<svg viewBox="0 0 24 24"><path').replace("/>", "/></svg>", 1),
               w, h, w - 36, h - 36))


# ===========================================================================
# E · «менше ніж за годину» — a clock that stops short of the hour
CLK = (210, 34, 236)               # x, y, size inside the shelf
STOP = 300                         # degrees: 50 minutes, short of the hour


def clock_html():
    c = CLK[2] / 2.0
    ticks = ""
    for i in range(12):
        a = math.radians(i * 30)
        r0, r1 = 66, 74
        ticks += '<line class="tick" x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>' % (
            c + r0 * math.sin(a), c - r0 * math.cos(a), c + r1 * math.sin(a), c - r1 * math.cos(a))
    svg = ('<svg viewBox="0 0 %d %d"><circle class="trk" cx="%.1f" cy="%.1f" r="96"/>'
           '<circle class="arc" id="clA" cx="%.1f" cy="%.1f" r="96" transform="rotate(-90 %.1f %.1f)"/>%s'
           '<line class="hand" id="clH" x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>'
           '<circle class="hub" cx="%.1f" cy="%.1f" r="11"/></svg>'
           % (CLK[2], CLK[2], c, c, c, c, c, c, ticks, c, c, c, c - 58, c, c))
    return ('<div class="tw circ hide" id="clk" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx">'
            '<div class="pearl">%s</div></div><div class="hide" id="clkL">&lt; 1 год</div>'
            % (CLK[0], CLK[1], CLK[2], CLK[2], svg))


@beat
def e_clock():
    sfx("click-soft", T["menshe"] + 0.04, -2)
    c = CLK[2] / 2.0
    return js("""
  arr("#clk", @menshe-0.04, {s: 0.5, y: 20, d: 0.75});
  arr("#clkL", @menshe+0.08, {s: 0.6, y: 16, d: 0.6});
  var CA = 2 * Math.PI * 96;
  gsap.set("#clA", {strokeDasharray: CA + " " + (CA + 40), strokeDashoffset: CA});
  tl.fromTo("#clA", {strokeDashoffset: CA}, {strokeDashoffset: CA * (1 - %d / 360), duration: 0.85,
            ease: "power2.out", immediateRender: false}, @nizh-0.05);
  gsap.set("#clH", {svgOrigin: "%.1f %.1f", rotation: 0});
  tl.fromTo("#clH", {rotation: 0}, {rotation: %d, duration: 0.85, ease: "power2.out", svgOrigin: "%.1f %.1f",
            immediateRender: false}, @nizh-0.05);
  G.bump("#clk", @hodynu+0.05);""" % (STOP, c, c, STOP, c, c))


# ===========================================================================
# F · the takeover: the design-system sheet, then skills into Claude
DSX, DSY = -40, -80                # the sheet's frame position (bleeds off top, left, right)
DS_SCALE, DS_DY = 0.4, 190         # the shrunk card: frame x 308..772, y 110..626
SWATCH = ["#b4122f", "#ff6e9c", "#fdf1f4", "#17141c", "#ffffff"]


def ds_html(pid, ghosts):
    """The design-system sheet in its own 1160x1290 space. `ghosts` adds the
    empty-slot layer the takeover opens on; the near copy is lit only."""
    gh = []
    lit = []

    def G_(s):
        if ghosts:
            gh.append(s)

    # header
    G_('<i class="tb gh" style="left:140px;top:196px;width:560px;height:70px;border-radius:18px"></i>')
    lit.append('<i class="ttl" id="%sT" style="left:140px;top:192px">Дизайн-система</i>' % pid)
    lit.append('<i class="hr" style="left:140px;top:304px;width:880px"></i>')
    # type
    lit.append('<i class="lbl" id="%sL0" style="left:140px;top:346px">ШРИФТ</i>' % pid)
    G_('<i class="aa gh" style="left:128px;top:408px">Aa</i>')
    lit.append('<i class="aa" id="%sAa" style="left:128px;top:408px">Aa</i>' % pid)
    G_('<i class="tb gh" style="left:560px;top:420px;width:300px;height:44px"></i>')
    lit.append('<i class="fn" id="%sFn" style="left:560px;top:412px">Product Sans</i>' % pid)
    for j, (y, w, h, cl) in enumerate([(488, 400, 34, "h"), (538, 330, 24, "s"), (582, 460, 16, "b"),
                                       (610, 420, 16, "b"), (638, 280, 16, "b")]):
        G_('<i class="tb gh" style="left:560px;top:%dpx;width:%dpx;height:%dpx"></i>' % (y, w, h))
        lit.append('<i class="tb %s %sTb" style="left:560px;top:%dpx;width:%dpx;height:%dpx"></i>' % (cl, pid, y, w, h))
    # colours
    lit.append('<i class="lbl" id="%sL1" style="left:140px;top:708px">КОЛЬОРИ</i>' % pid)
    for j, col in enumerate(SWATCH):
        x = 140 + j * 180
        G_('<i class="sw gh" style="left:%dpx;top:750px"></i>' % x)
        ring = "box-shadow: inset 0 0 0 3px rgba(23,20,28,0.10), 0 16px 30px -14px rgba(30,4,12,0.4);" if j in (2, 4) else ""
        lit.append('<i class="sw %sSw" style="left:%dpx;top:750px;background:%s;%s"></i>' % (pid, x, col, ring))
        lit.append('<i class="hx %sHx" style="left:%dpx;top:900px">%s</i>' % (pid, x, col.upper()))
    # components
    lit.append('<i class="lbl" id="%sL2" style="left:140px;top:964px">КОМПОНЕНТИ</i>' % pid)
    G_('<i class="cg" style="left:140px;top:1008px;width:320px;height:100px;border-radius:50px"></i>')
    lit.append('<i class="btn %sCp" style="left:140px;top:1008px;width:320px;height:100px">Далі</i>' % pid)
    G_('<i class="cg" style="left:500px;top:1022px;width:136px;height:72px;border-radius:36px"></i>')
    lit.append('<i class="tgl %sCp" style="left:500px;top:1022px;width:136px;height:72px">'
               '<i class="on" id="%sTo"></i><i class="kn" id="%sTk"></i></i>' % (pid, pid, pid))
    G_('<i class="cg" style="left:140px;top:1140px;width:240px;height:72px;border-radius:36px"></i>')
    lit.append('<i class="chp %sCp" style="left:140px;top:1140px;width:240px;height:72px"><b></b><u></u></i>' % pid)
    G_('<i class="cg" style="left:690px;top:1008px;width:330px;height:204px;border-radius:30px"></i>')
    lit.append('<i class="mc %sCp" style="left:690px;top:1008px;width:330px;height:204px">'
               '<i style="left:26px;top:26px;width:170px;height:26px;background:linear-gradient(115deg,#c41434,#8d0d24)"></i>'
               '<i style="left:26px;top:74px;width:270px;height:14px;background:rgba(23,20,28,0.13)"></i>'
               '<i style="left:26px;top:100px;width:230px;height:14px;background:rgba(23,20,28,0.13)"></i>'
               '<i style="left:26px;top:126px;width:150px;height:14px;background:rgba(23,20,28,0.13)"></i>'
               '<i style="left:26px;top:156px;width:96px;height:28px;border-radius:14px;background:#ff8ab0"></i></i>' % pid)
    ghost = '<div class="abs gh%s" style="left:0;top:0;width:1160px;height:1290px">%s</div>' % (pid, "".join(gh)) if ghosts else ""
    return ('<div class="sheet ds hide" id="%s" style="left:%dpx;top:%dpx" data-layout-allow-overflow>%s%s'
            '<div class="shc"><div class="sheen"></div></div></div>' % (pid, DSX, DSY, ghost, "".join(lit)))


SKILLS = [u"монтаж", u"субтитри", u"графіка", u"звук"]
SK_POS = [(100, 990), (580, 990), (100, 1124), (580, 1124)]
CL_T = (430, 710, 220)             # the takeover's Claude tile


@beat
def f_takeover():
    chips = ""
    for i, (w, (x, y)) in enumerate(zip(SKILLS, SK_POS)):
        chips += ('<div class="skc hide" id="sk%d" style="left:%dpx;top:%dpx">'
                  '<div class="tw circ pz"><div class="jelly">%s</div></div><span>%s</span></div>'
                  % (i, x, y, stroke("puzzle"), w))
    cab = ('<svg class="cab abs" width="1080" height="1920" viewBox="0 0 1080 1920" style="left:0;top:0">'
           '<path class="tube hide" id="fT" d="M540 632 L540 704"/>'
           '<path class="core hide" id="fC" d="M540 632 L540 704"/>'
           '<g class="pkg"><path class="pkt" id="fP" style="opacity:0" d="M540 628 L540 708"/></g></svg>')
    L.append('<div class="g full" id="gT"><div class="tkg"></div><div class="aurs"></div><div class="grain"></div>'
             + ds_html("ds", True) + cab
             + tile("tC", CL_T[2], CL_T[0], CL_T[1], "jelly", g.mark("claude"))
             + chips + '</div>')
    sfx("whoosh-short", T["dlia"] - 0.06)
    sfx("pop", T["nalasht"] + 0.04, -2)
    sfx("click", T["pidkl"] + 0.24)
    sfx("click", T["skily"] + 0.22, -1)
    sfx("whoosh-short", T["zghodom"] - 0.02, -2)
    out = js("""
  G.irisOpen("#gT", @dlia-0.06, 688, 282, 0.85);
  drift1("#gT", @dlia, @zghodom+0.6-@dlia);
  gsap.set("#ds", {transformOrigin: "580px 0px"});
  arr("#ds", @dlia+0.16, {s: 0.86, y: 70, d: 0.9});
  [["#dsL0", @zrobyty], ["#dsL1", @treba-0.1], ["#dsL2", @lyshe-0.05]].forEach(function (p) { bin(p[0], p[1], 8, 0.3); });
  gsap.set(["#dsT", "#dsAa", "#dsFn", ".dsTb", ".dsSw", ".dsHx", ".dsCp"], {autoAlpha: 0});
  /* «налаштувати» — type, then colours, then the title, then components */
  arr("#dsAa", @nalasht-0.02, {s: 0.7, y: 20, d: 0.7});
  bin("#dsFn", @nalasht+0.12, 8, 0.3);
  tl.fromTo(".dsTb", {autoAlpha: 1, scaleX: 0}, {autoAlpha: 1, scaleX: 1, duration: 0.5, ease: SP, stagger: 0.05, immediateRender: false}, @nalasht+0.16);
  tl.fromTo(".dsSw", {autoAlpha: 0, scale: 0.3}, {autoAlpha: 1, scale: 1, duration: 0.5, ease: POP, stagger: 0.07, immediateRender: false}, @nalasht+0.3);
  bin(".dsHx", @nalasht+0.45, 6, 0.3);
  arr("#dsT", @dyzsys-0.03, {s: 0.8, y: 12, d: 0.6});
  shn("#ds .sheen", @dyzsys+0.1);
  tl.fromTo(".dsCp", {autoAlpha: 0, scale: 0.6, y: 24}, {autoAlpha: 1, scale: 1, y: 0, duration: 0.55, ease: POP, stagger: 0.07, immediateRender: false}, @dyzsys+0.12);
  gsap.set("#dsTo", {autoAlpha: 0}); gsap.set("#dsTk", {x: 0});
  tl.to("#dsTo", {autoAlpha: 1, duration: 0.2}, @dyzsyse-0.12);
  tl.to("#dsTk", {x: 64, duration: 0.4, ease: SP}, @dyzsyse-0.12);
  tl.to(".ghds", {autoAlpha: 0, duration: 0.2}, @dyzsyse);
  /* «та підключити правильні скіли» — the sheet becomes a card on a cable into Claude */
  tl.to("#ds", {scale: %.2f, y: %d, duration: 0.8, ease: SP}, @ta-0.06);
  arr("#tC", @ta+0.1, {s: 0.4, y: 40, d: 0.75});
  tl.set(["#fT", "#fC"], {autoAlpha: 1}, @pidkl+0.05); draw2("fT", @pidkl+0.05, 0.3); draw2("fC", @pidkl+0.05, 0.3);
  G.packet("fP", @pidkl+0.4, 0.35);""" % (DS_SCALE, DS_DY))
    times = ["pidkl", "pidkl", "pravylni", "skily"]
    offs = [-0.02, 0.26, -0.02, -0.04]
    for i, (key, off) in enumerate(zip(times, offs)):
        dx = -620 if SK_POS[i][0] < 540 else 620
        out += js("""
  tl.fromTo("#sk%d", {autoAlpha: 1, x: %d, rotation: %d}, {autoAlpha: 1, x: 0, rotation: 0, duration: 0.6, ease: POP, immediateRender: false}, @%s%+.2f);
  G.bump("#tC", @%s%+.2f); G.ripple("#tCR", @%s%+.2f);""" % (i, dx, -8 if dx < 0 else 8, key, off,
                                                            key, off + 0.24, key, off + 0.24))
    out += js("""
  /* «Про скіли розкажу згодом» — the names blur: later */
  tl.fromTo("#gT .skc span", {filter: "blur(0px)", autoAlpha: 1}, {filter: "blur(10px)", autoAlpha: 0.5, duration: 0.4,
            ease: "power2.out", stagger: 0.05, immediateRender: false}, @skily2);
  tl.to("#gT .skc", {scale: 0.94, duration: 0.4, ease: "power2.out"}, @skily2);
  /* the iris closes onto the card, which stays on her footage */
  G.irisClose("#gT", @zghodom-0.02, 540, 368, 0.55);""")
    return out


# ===========================================================================
# G · near: the same card above her head — «а щоб налаштувати дизайн систему»
@beat
def g_card():
    L.append('<div class="g full" id="gG">' + ds_html("nd", False) + '{{HI}}</div>')
    return js("""
  gsap.set("#nd", {transformOrigin: "580px 0px", scale: %.2f, y: %d});
  tl.set("#gG", {autoAlpha: 1}, @zghodom-0.04);
  tl.set("#nd", {autoAlpha: 1}, @zghodom-0.04);
  gsap.set("#ndTo", {autoAlpha: 1}); gsap.set("#ndTk", {x: 64});
  tl.to("#nd", {scale: %.3f, duration: 0.1, ease: "power2.out"}, @nalasht2+0.02);
  tl.to("#nd", {scale: %.3f, duration: 0.45, ease: SP}, @nalasht2+0.12);
  shn("#nd .sheen", @dyzain);
  tl.to(".ndSw", {scale: 1.12, duration: 0.18, stagger: 0.06, ease: "power2.out"}, @dyzain+0.05);
  tl.to(".ndSw", {scale: 1, duration: 0.45, stagger: 0.06, ease: SP}, @dyzain+0.23);
  tl.to("#nd", {y: %d, autoAlpha: 0, duration: 0.24, ease: "power2.in"}, @pyshy-0.27);""" % (
        DS_SCALE, DS_DY, DS_SCALE * 1.05, DS_SCALE, DS_DY - 70))


# ===========================================================================
# H · the comment: «пиши слово система в коментарі»
@beat
def h_comment():
    sfx("typing", T["systema"] + 0.02, -1)
    sfx("click", T["koment"] + 0.04)
    return js("""
  arr("#cmIn", @pyshy, {s: 0.86, y: 40, d: 0.7});
  tl.set("#cmIn .phd", {autoAlpha: 0}, @systema);
  tl.set("#cmIn .tx", {autoAlpha: 1}, @systema);
  G.bump("#cmS", @koment+0.02);
  tl.fromTo("#cmRow", {autoAlpha: 0, y: 150, scale: 0.9}, {autoAlpha: 1, y: 0, scale: 1, duration: 0.7, ease: SP}, @koment+0.06);
  tl.set("#cmIn .tx", {autoAlpha: 0}, @koment+0.08);
  tl.set("#cmIn .phd", {autoAlpha: 1}, @koment+0.08);
  bout("#cmIn", @i_-0.1, 10, 0.3);""")


# ===========================================================================
# I · the DM with the instruction: «і отримай безкоштовну інструкцію!»
@beat
def i_dm():
    sfx("notification", T["otrymai"] - 0.12)
    return js("""
  tl.fromTo("#dm", {autoAlpha: 0, y: -280, scale: 0.92}, {autoAlpha: 1, y: 0, scale: 1, duration: 0.9, ease: SOFT}, @otrymai-0.2);
  G.haptic("#dm", @otrymai+0.36);
  shn("#dm .sheen", @bezkosht);""")


def near_html():
    """H and I live in the near layer #gG, after the card."""
    doc = ('<div class="doc" style="left:774px;top:40px;width:104px;height:118px">'
           '<i style="left:12px;top:12px;width:62px;height:12px;border-radius:6px;background:linear-gradient(115deg,#c41434,#8d0d24)"></i>'
           '<i class="aa">Aa</i>'
           '<i class="d" style="left:12px;background:#b4122f"></i><i class="d" style="left:36px;background:#ff6e9c"></i>'
           '<i class="d" style="left:60px;background:#17141c"></i></div>')
    dm = ('<div class="dglass edge hide" id="dm" style="left:70px;top:112px;width:940px;height:196px">'
          '<div class="tw" style="left:34px;top:46px;width:104px;height:104px"><div class="jelly">%s</div></div>'
          '<div class="app">Instagram</div><div class="tm">зараз</div>'
          '<div class="msg">Інструкція: <span style="white-space:nowrap">дизайн-система</span></div>%s'
          '<div class="shc"><div class="sheen"></div></div></div>' % (g.mark("instagram"), doc))
    row = ('<div class="dglass edge hide" id="cmRow" style="left:70px;top:340px;width:940px;height:140px;border-radius:52px">'
           '<div class="tw circ" style="left:30px;top:26px;width:88px;height:88px"><div class="pearl">%s</div></div>'
           '<div class="nm"></div><div class="tx">система</div>%s</div>' % (stroke("person"), stroke("heart", "ht")))
    inp = ('<div class="dglass edge hide" id="cmIn" style="left:70px;top:504px;width:940px;height:120px;border-radius:60px">'
           '<div class="phd">Додайте коментар…</div><div class="tx hide" id="cmTx"></div>'
           '<div class="tw circ" id="cmS" style="left:828px;top:14px;width:92px;height:92px"><div class="jelly">%s</div></div>'
           '</div>' % stroke("up"))
    return row + inp + dm


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
    """«система» types itself into the comment, driven from one clock."""
    word = u"система"
    t0, t1 = T["systema"] + 0.02, T["systemae"] - 0.04
    return r"""
  var CLK = {t: 0}, CT = document.getElementById("cmTx"), CTXT = %s, CCUR = null;
  function paintAll() {
    var t = CLK.t, n = t <= %.3f ? 0 : t >= %.3f ? CTXT.length : Math.round(CTXT.length * (t - %.3f) / %.3f);
    if (n !== CCUR) { CCUR = n; CT.textContent = CTXT.slice(0, n); }
  }
  tl.fromTo(CLK, {t: 0}, {t: %.3f, duration: %.3f, ease: "none", onUpdate: paintAll}, 0);""" % (
        json.dumps(word, ensure_ascii=False), t0, t1, t0, t1 - t0, DUR, DUR)


# captions that would repeat the graphic's own words (STYLE.md §2b.1)
def span_words(a, b):
    return (round(a - 0.02, 3), round(b, 3), "")


BLACKOUT = [
    span_words(T["sotni"], T["misiatse"]),         # the shelf says «сотні € на місяць»
    span_words(T["pidpysky"], T["menshe"] - 0.02),  # the card says «Підписка» (merged with the next)
    span_words(T["menshe"], T["hodynue"]),         # the clock says «< 1 год»
    span_words(T["dyzsys"], T["dyzsyse"]),         # the sheet's title says it
    span_words(T["systema"], T["systemae"]),       # the comment types it
    span_words(T["instr"], DUR + 0.1),             # the DM says «Інструкція»
]


def main():
    # her closeup («і це не хайп і не жарт») sits between the coins and the
    # shelf: both must be off screen for all of it
    for a, b in NO_PAINT:
        assert T["mOut"] + 0.24 <= a and T["tS"] >= b, ("graphics inside a closeup", a, b)
    gj = []
    for fn in BEATS:
        j = fn()
        gj.append("  /* %s */" % fn.__name__)
        gj.append(j.rstrip())
    html = "\n".join(L)
    html = html.replace("{{ED}}", editor_html() + sub_html() + clock_html())
    html = html.replace("{{HI}}", near_html())
    defs_extra = ('<linearGradient id="gArc" x1="0" y1="0" x2="1" y2="1">'
                  '<stop offset="0" stop-color="#ff8ab0"/><stop offset="1" stop-color="#b4122f"/></linearGradient>')
    head = [g.js(), HEAD_JS, typing_js(),
            '  gsap.set("#vid", {transformOrigin: "540px 900px"});',
            '  tl.fromTo("#vid", {scale: 1}, {scale: 1.045, duration: %.3f, ease: "none"}, 0);' % DUR]
    doc = k.document(
        title=u"Reel 24 — Клод монтує",
        plate="assets/base.mp4",
        gfx_html=g.defs(defs_extra) + "\n" + html,
        gfx_js="\n".join(head + gj),
        caps=CAPS,
        blackout=BLACKOUT,
    )
    io.open(os.path.join(HERE, "index.html"), "w", encoding="utf-8").write(doc)
    SFX.sort(key=lambda c: c["t"])
    io.open(os.path.join(HERE, "sfx.json"), "w", encoding="utf-8").write(json.dumps(SFX, indent=1))
    print("index.html  %d captions, %d beats, %d sfx cues (%.2f/s)" % (
        len(CAPS), len(BEATS), len(SFX), len(SFX) / DUR))


main()
