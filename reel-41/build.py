# -*- coding: utf-8 -*-
"""Reel 41 — «Цей рілс змонтував Клод». Delivered 2026-10-27.

A short closer cut from the end of her long explainer: the phone reel she shot
at the start was edited by her Claude in the 15 minutes she spent recording,
so invest in the system rather than another course, then the CTA.

Built on a 15-minute brief, so four light beats, all in the top band above her
head (STYLE.md §3), refined glass (§0):
  1. «рілс на телефоні»   — a reel tile lands and bumps on «телефоні»
  2. «Клодом за 15 хв»    — the Claude tile lands, a «15 хв» pill pops beside it
  3. «курс … SMM … час»   — three dark pills land on their words, one strike runs through them
  4. «натискай кнопку під відео» — an arrow tile pointing down, bouncing

usage: python build.py
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

DUR = 22.0             # 660 plate frames, raw 3.85-25.85 s
FPS = 30
k = Kit(width=1080, height=1920, fps=FPS, duration=DUR)
g = Glass(["claude"])
k.css(g.css())

CAPS = k.load_captions(os.path.join(ROOT, "work", "r41", "captions.json"))


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
    "rils": S(u"рілс", 3.17), "tel": S(u"телефоні", 3.69), "tak": S(u"Так", 4.55),
    "klod": S(u"Клодом", 7.01), "p15": S("15", 7.79), "poky": S(u"поки", 8.63),
    "dovhe": S(u"довге", 9.99), "i": S(u"І", 11.67),
    "kurs": S(u"курс", 15.75), "smm": S("SMM", 17.17), "chas": S(u"час", 19.25),
    "to": S(u"то", 19.97), "nat": S(u"натискай", 20.07), "knop": S(u"кнопку", 20.67),
    "dur": DUR,
}


def js(src):
    def rep(m):
        v = T[m.group(1)] + (float(m.group(2)) if m.group(2) else 0.0)
        return "%.3f" % v
    return re.sub(r"@(\w+)([+-]\d+(?:\.\d+)?)?", rep, src)


STROKES = {
    "clapper": '<path d="M4 10h16v8.4a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2z"/><path d="M4 10l-.6-3.4 15.2-2.7.6 3.4z"/>'
               '<path d="M8.4 5.8l2.3 3.3M13.4 4.9l2.3 3.3"/>',
    "down": '<path d="M12 4.8v13.8M6.2 13l5.8 5.8 5.8-5.8"/>',
}


def stroke(name):
    return '<svg class="sk" viewBox="0 0 24 24">%s</svg>' % STROKES[name]


def tile(tid, size, x, y, material, inner):
    return ('<div class="sqring" id="%sR" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx"></div>'
            '<div class="tw hide" id="%s" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx">'
            '<div class="%s">%s<div class="sheen"></div></div></div>'
            % (tid, x, y, size, size, tid, x, y, size, size, material, inner))


k.css("""
.hide { opacity: 0; visibility: hidden; }
.tw { position: absolute; }
.sk { fill: none; stroke: url(#gw); stroke-width: 2.3; stroke-linecap: round; stroke-linejoin: round;
  width: 50%; height: 50%; position: relative; z-index: 1; overflow: visible; }
.pill { position: absolute; height: 120px; border-radius: 60px; padding: 0 46px; line-height: 120px;
  font-size: 60px; font-weight: 900; letter-spacing: -0.02em; color: #fff; white-space: nowrap; }
.pill.lt { color: #17141c; background: linear-gradient(172deg, #ffffff 0%, #fff9fb 55%, #fdf0f4 100%);
  box-shadow: inset 0 2px 1px #fff, 0 40px 80px -30px rgba(24,4,12,0.6), 0 0 0 1px rgba(255,255,255,0.4); }
.stk { position: absolute; left: 0; top: 0; overflow: visible; z-index: 4; }
.sline { fill: none; stroke: #ff4d7f; stroke-width: 13; stroke-linecap: round;
  filter: drop-shadow(0 0 8px rgba(255,110,156,0.9)); }
""")

L = []
J = []


def b_reel():
    L.append(tile("ph", 220, 430, 260, "jelly", stroke("clapper")))
    J.append("""
  arr("#ph", @rils-0.1, {s: 0.5});
  G.ripple("#phR", @tel+0.05);
  tl.to("#ph", {scale: 1.1, duration: 0.12, ease: "power2.out"}, @tel);
  tl.to("#ph", {scale: 1, duration: 0.45, ease: SP}, @tel+0.12);
  bout("#ph", @tak+0.1);""")


def b_claude():
    L.append(tile("cl", 240, 230, 250, "jelly", g.mark("claude")))
    L.append('<div class="pill lt hide" id="p15" style="left:540px;top:310px">15 хв</div>')
    J.append("""
  arr("#cl", @klod-0.08, {s: 0.5});
  G.ripple("#clR", @klod+0.3);
  arr("#p15", @p15-0.05, {s: 0.6, x: -40, y: 0, d: 0.7});
  shn("#cl .sheen", @poky);
  bout("#p15", @dovhe+0.4);
  bout("#cl", @dovhe+0.5);""")


def b_courses():
    pills = [("pk", u"Курс", 120, "kurs"), ("ps", "SMM", 430, "smm"), ("pc", u"Час", 715, "chas")]
    for pid, txt, x, _ in pills:
        L.append('<div class="pill dglass edge hide" id="%s" style="left:%dpx;top:330px">%s</div>' % (pid, x, txt))
    L.append('<svg class="stk" width="1080" height="800"><path id="strike" class="sline" d="M100 392 L 980 386"/></svg>')
    J.append("""
  arr("#pk", @kurs-0.05, {s: 0.6});
  arr("#ps", @smm-0.05, {s: 0.6});
  arr("#pc", @chas-0.05, {s: 0.6});
  draw2("strike", @chas+0.35, 0.35);
  bout("#pk, #ps, #pc, #strike", @to-0.05);""")


def b_cta():
    L.append(tile("dn", 230, 425, 270, "jelly", stroke("down")))
    J.append("""
  arr("#dn", @nat-0.05, {s: 0.5});
  G.ripple("#dnR", @knop);
  tl.to("#dn", {y: 46, duration: 0.22, ease: "power2.in", yoyo: true, repeat: 3}, @knop+0.05);""")


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
  gsap.set(".sheen", {xPercent: -120});
"""

# graphics that say her word (STYLE.md §2b.1)
BLACKOUT = [
    (T["p15"] - 0.02, E(u"хвилин", 8.13), ""),
    (T["kurs"] - 0.02, E(u"курс", 15.75), ""),
    (T["smm"] - 0.02, E("SMM", 17.17), ""),
    (T["chas"] - 0.02, E(u"час", 19.25), ""),
]


def main():
    for fn in (b_reel, b_claude, b_courses, b_cta):
        fn()
    head = [g.js(), HEAD_JS,
            '  gsap.set(["#vid"], {transformOrigin: "540px 900px"});',
            '  tl.fromTo(["#vid"], {scale: 1}, {scale: 1.045, duration: %.3f, ease: "none"}, 0);' % DUR]
    doc = k.document(
        title=u"Reel 41 — Цей рілс змонтував Клод",
        plate="assets/base.mp4",
        gfx_html=g.defs() + "\n" + "\n".join(L),
        gfx_js="\n".join(head + [js(x) for x in J]),
        caps=CAPS,
        blackout=BLACKOUT,
    )
    io.open(os.path.join(HERE, "index.html"), "w", encoding="utf-8").write(doc)
    print("index.html  %d captions, 4 beats" % len(CAPS))


main()
