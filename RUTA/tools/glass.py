# -*- coding: utf-8 -*-
"""ARCHIVED 2026-10-28 — kept so reels 12–40 still rebuild. New reels use
tools/gstyle.py (STYLE.md §00); see archive/STYLE-refined-glass.md.

Refined glass — the house look, locked 2026-09-28.

Her verdict on the test pass (`style-test/`): *"this is fucking amazing.
delicious. just YES"*. This module is that test's materials and motion, lifted
out so every reel from 12 onward starts from them instead of re-deriving them.

It sits on top of `kit.py`, not instead of it: the kit still owns the document,
the plate, mattes and the caption machinery (whose look did not change). This
owns what a graphic is made of and how it moves.

    from kit import Kit
    from glass import Glass
    k = Kit(duration=DUR)
    g = Glass(["instagram", "tiktok", "claude"])
    k.css(g.css())
    beats = '<div class="tile"><div class="jelly">' + g.mark("claude") + '</div></div>'
    gfx_html = g.defs() + beats        # defs() LAST: it only knows marks used so far
    gfx_js = g.js() + 'var G = helpers(tl); G.arrive("#x", 3.2);'

Class names avoid the kit's (.gl, .ring, .glass, .tile and .card are taken
there): marks are `.mk`, the ripple is `.sqring`, the shelf is `.shelf`.
"""
import io
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ICONS = os.path.join(ROOT, "assets", "icons")

# ---------------------------------------------------------------------------
# Type. The kit declares ProductSans 900 for captions; graphics also need the
# lighter cuts, because weight contrast (a Black number over a Medium label) is
# most of what makes a card read as designed rather than typed.
FONTS = """
@font-face { font-family: "ProductSans"; src: url("assets/fonts/ProductSans-Regular.ttf"); font-weight: 400; font-display: block; }
@font-face { font-family: "ProductSans"; src: url("assets/fonts/ProductSans-Medium.ttf"); font-weight: 500; font-display: block; }
@font-face { font-family: "ProductSans"; src: url("assets/fonts/ProductSans-Bold.ttf"); font-weight: 700; font-display: block; }
"""

MATERIALS = """
/* ---------- the edge light: what makes a surface read as glass ----------
   A uniform stroke is 2013. Real glass catches light at two opposite corners
   and goes almost dark along the sides, so the rim is a gradient ring. */
.edge::before { content: ""; position: absolute; inset: 0; border-radius: inherit; padding: 1.6px;
  background: linear-gradient(140deg, rgba(255,255,255,0.95) 0%, rgba(255,255,255,0.34) 16%,
              rgba(255,255,255,0.05) 42%, rgba(255,255,255,0.07) 62%,
              rgba(255,255,255,0.50) 86%, rgba(255,255,255,0.90) 100%);
  -webkit-mask: linear-gradient(#000 0 0) content-box, linear-gradient(#000 0 0);
  -webkit-mask-composite: xor; mask-composite: exclude; pointer-events: none; z-index: 3; }

/* ---------- the shelf: frosted glass over her footage ----------
   The house look since reel 3, rebuilt in layers: blur + saturation, a faint
   top-to-bottom tint, light inside the bottom edge (thickness), huge soft
   shadow. Add .edge for the rim. */
.shelf { position: absolute; border-radius: 80px;
  background: linear-gradient(158deg, rgba(255,255,255,0.24) 0%, rgba(255,255,255,0.07) 50%,
              rgba(255,255,255,0.13) 100%);
  -webkit-backdrop-filter: blur(22px) saturate(1.7) brightness(1.05);
  backdrop-filter: blur(22px) saturate(1.7) brightness(1.05);
  box-shadow: inset 0 2px 1px rgba(255,255,255,0.65), inset 0 -24px 44px -22px rgba(255,255,255,0.36),
              0 44px 90px -34px rgba(24,4,12,0.5); }

/* dark glass — notifications and anything with white text over footage */
.dglass { position: absolute; border-radius: 64px; color: #fff;
  background: linear-gradient(160deg, rgba(58,22,32,0.58) 0%, rgba(24,10,15,0.50) 100%);
  -webkit-backdrop-filter: blur(30px) saturate(1.8); backdrop-filter: blur(30px) saturate(1.8);
  box-shadow: inset 0 1.5px 1px rgba(255,255,255,0.30), inset 0 -16px 30px -16px rgba(255,255,255,0.14),
              0 40px 80px -30px rgba(10,0,4,0.6); }

/* ---------- the tile family: every mark lives in one of three ----------
   Same radius ratio as an iOS icon (22.4%), glyph at 50%. Put the tile in a
   sized wrapper; the wrapper takes the motion, the tile takes the material. */
.clear { position: absolute; inset: 0; border-radius: 22.4%;
  background: linear-gradient(158deg, rgba(255,255,255,0.36) 0%, rgba(255,255,255,0.11) 48%,
              rgba(255,255,255,0.17) 100%);
  box-shadow: inset 0 2px 1px rgba(255,255,255,0.70), inset 0 -18px 30px -14px rgba(255,255,255,0.42),
              0 34px 60px -22px rgba(24,4,12,0.55), 0 3px 8px rgba(24,4,12,0.10);
  display: flex; align-items: center; justify-content: center; }
.pearl { position: absolute; inset: 0; border-radius: 22.4%; overflow: hidden;
  background: linear-gradient(160deg, #ffffff 0%, #fff5f8 52%, #f5dfe6 100%);
  box-shadow: inset 0 2px 1px #fff, inset 0 -20px 32px -14px rgba(180,18,47,0.18),
              0 36px 64px -22px rgba(30,4,12,0.55), 0 3px 8px rgba(30,4,12,0.12);
  display: flex; align-items: center; justify-content: center; }
.jelly { position: absolute; inset: 0; border-radius: 22.4%; overflow: hidden;
  background: linear-gradient(165deg, #e0204b 0%, #ab112e 46%, #6b081c 100%);
  box-shadow: inset 0 2px 1px rgba(255,255,255,0.55), inset 0 -26px 40px -14px rgba(255,125,165,0.60),
              inset 0 0 0 1px rgba(255,255,255,0.10),
              0 36px 64px -22px rgba(70,4,20,0.62), 0 3px 8px rgba(70,4,20,0.14);
  display: flex; align-items: center; justify-content: center; }
/* the lens highlight — subtle, or it turns into 2009 gloss */
.jelly::after, .pearl::after { content: ""; position: absolute; left: 7%; right: 7%; top: 3.5%; height: 44%;
  border-radius: 40% 40% 50% 50% / 38% 38% 24% 24%;
  background: linear-gradient(180deg, rgba(255,255,255,0.26), rgba(255,255,255,0)); }
.pearl::after { background: linear-gradient(180deg, rgba(255,255,255,0.9), rgba(255,255,255,0)); opacity: 0.5; }
.mk { width: 50%; height: 50%; fill: url(#gw); position: relative; z-index: 1; }
.pearl .mk { fill: #17141c; }
/* a wordmark stands in where a brand has no icon (RUTA, Windsor's "w.") */
.wmark { font-weight: 900; color: #17141c; letter-spacing: -0.045em; line-height: 1;
  position: relative; z-index: 1; }
.wmark i { font-style: normal; color: #b4122f; }
.jelly .wmark { color: #fff; } .jelly .wmark i { color: #ffb3c9; }

/* one light sweep across a surface when it lands — once, never looping */
.sheen { position: absolute; inset: -10%; z-index: 2; pointer-events: none;
  background: linear-gradient(105deg, rgba(255,255,255,0) 38%, rgba(255,255,255,0.75) 50%, rgba(255,255,255,0) 62%);
  mix-blend-mode: soft-light; }
/* a ripple the same shape as the tile that sent it */
.sqring { position: absolute; border-radius: 22.4%; border: 3px solid rgba(255,255,255,0.75);
  opacity: 0; visibility: hidden; }

/* ---------- the takeover ground: deep burgundy, lit from inside ----------
   Approved on the test: a dark ground is allowed now (it overrides §5's old
   "never dark"). Three soft light pools drift slowly; grain stops banding. */
.tkg { position: absolute; inset: 0;
  background: linear-gradient(172deg, #4a0a1c 0%, #660c26 36%, #3c0716 70%, #1d030a 100%); }
.aur { position: absolute; border-radius: 50%; pointer-events: none; }
.aur.a1 { left: 260px; top: -420px; width: 1200px; height: 1200px;
  background: radial-gradient(circle, rgba(255,110,156,0.50) 0%, rgba(255,110,156,0) 62%); }
.aur.a2 { left: -640px; top: 960px; width: 1400px; height: 1400px;
  background: radial-gradient(circle, rgba(222,32,74,0.55) 0%, rgba(222,32,74,0) 64%); }
.aur.a3 { left: 330px; top: 760px; width: 900px; height: 900px;
  background: radial-gradient(circle, rgba(255,198,214,0.20) 0%, rgba(255,198,214,0) 60%); }
.grain { position: absolute; inset: 0; background: url("assets/grain.png"); opacity: 0.075;
  mix-blend-mode: overlay; pointer-events: none; }

/* the white report card that sits on a burgundy ground */
.sheet { position: absolute; border-radius: 68px; overflow: hidden; color: #17141c;
  background: linear-gradient(172deg, #ffffff 0%, #fff9fb 55%, #fdf0f4 100%);
  box-shadow: inset 0 2px 1px #fff, inset 0 -30px 60px -30px rgba(180,18,47,0.14),
              0 70px 130px -40px rgba(8,0,3,0.75), 0 0 0 1px rgba(255,255,255,0.35); }
.sheet .sheen { mix-blend-mode: normal; opacity: 0.55; }
/* type ladder inside a sheet */
.t-micro { font-size: 24px; font-weight: 700; letter-spacing: 0.16em; color: rgba(23,20,28,0.42); }
.t-title { font-size: 42px; font-weight: 700; letter-spacing: -0.015em; }
.t-sub   { font-size: 26px; font-weight: 500; color: rgba(23,20,28,0.46); }
.t-big   { font-size: 176px; font-weight: 900; letter-spacing: -0.045em; line-height: 1;
  background: linear-gradient(118deg, #7e0b20 0%, #b4122f 42%, #ff6e9c 100%);
  -webkit-background-clip: text; background-clip: text; color: transparent; padding-right: 10px; }
.chip { display: inline-flex; align-items: center; gap: 10px; height: 58px; padding: 0 24px;
  border-radius: 29px; background: #fbe3ea; color: #b4122f; font-size: 26px; font-weight: 700; }
.hair { height: 2px; background: rgba(23,20,28,0.07); transform-origin: 0 0; }

/* a cable between two tiles: a glass tube, a bright core, a travelling packet */
.cab .tube { fill: none; stroke: rgba(255,255,255,0.26); stroke-width: 20; stroke-linecap: round; }
.cab .core { fill: none; stroke: rgba(255,255,255,0.92); stroke-width: 4.5; stroke-linecap: round; }
.cab .pkt  { fill: none; stroke: #ffd6e3; stroke-width: 11; stroke-linecap: round; }
.cab .pkg  { filter: drop-shadow(0 0 10px rgba(255,120,165,1)); }
.cab .wire { fill: none; stroke: rgba(255,255,255,0.55); stroke-width: 4; stroke-linecap: round; }
"""

# ---------------------------------------------------------------------------
# Motion. Springs, not stock eases: a small overshoot that settles is what reads
# as physical. Opacity and blur never take a spring (blur(-2px) is invalid).
MOTION = r"""
function spring(z, w) {
  var wd = w * Math.sqrt(1 - z * z);
  function f(t) { return 1 - Math.exp(-z * w * t) * (Math.cos(wd * t) + (z * w / wd) * Math.sin(wd * t)); }
  var e = f(1);
  return function (t) { return t >= 1 ? 1 : f(t) / e; };
}
var SP = spring(0.62, 13), POP = spring(0.46, 14), SOFT = spring(0.84, 11), FLIP = spring(0.58, 9);

function helpers(tl) {
  function blurIn(sel, t, b, d) {
    tl.fromTo(sel, {autoAlpha: 0, filter: "blur(" + (b || 12) + "px)"},
                   {autoAlpha: 1, filter: "blur(0px)", duration: d || 0.38, ease: "power2.out"}, t);
  }
  function blurOut(sel, t, b, d) {
    tl.to(sel, {autoAlpha: 0, filter: "blur(" + (b || 10) + "px)", duration: d || 0.32, ease: "power2.in"}, t);
  }
  // arrive from depth: blur -> sharp, small -> full, with a spring. o: {s, x, y, ease, d}
  function arrive(sel, t, o) {
    o = o || {};
    blurIn(sel, t, o.blur || 12, 0.36);
    tl.fromTo(sel, {scale: o.s == null ? 0.5 : o.s, x: o.x || 0, y: o.y == null ? 34 : o.y},
              {scale: 1, x: 0, y: 0, duration: o.d || 0.85, ease: o.ease || POP}, t);
  }
  // the contents land a beat after their container
  function inner(sel, t) {
    tl.fromTo(sel, {scale: 0.55, autoAlpha: 0}, {scale: 1, autoAlpha: 1, duration: 0.55, ease: SP}, t + 0.1);
  }
  function sheen(sel, t) { gsap.set(sel, {xPercent: -120}); tl.to(sel, {xPercent: 120, duration: 0.8, ease: "power2.inOut"}, t); }
  function len(id) { return document.getElementById(id).getTotalLength(); }
  // +3: a dash that ends exactly at the path start leaves a round-cap dot behind
  function drawPrep(id) { var L = len(id) + 3; gsap.set("#" + id, {strokeDasharray: (L - 3) + " " + (L + 40), strokeDashoffset: L}); return L; }
  function draw(id, t, d) { var L = drawPrep(id); tl.to("#" + id, {strokeDashoffset: 0, duration: d || 0.55, ease: "power2.inOut"}, t); return L; }
  function packet(id, t, d) {
    var L = len(id);
    tl.fromTo("#" + id, {strokeDasharray: "46 " + (L + 200), strokeDashoffset: 49, autoAlpha: 1},
              {strokeDashoffset: -L, duration: d || 0.5, ease: "power1.inOut", immediateRender: false}, t);
    tl.set("#" + id, {autoAlpha: 0}, t + (d || 0.5));
  }
  // a tile the same shape grows out and fades — "something arrived here"
  function ripple(sel, t) {
    tl.fromTo(sel, {scale: 1, autoAlpha: 0.7}, {scale: 1.75, autoAlpha: 0, duration: 0.8, ease: "power2.out", immediateRender: false}, t);
  }
  function bump(sel, t) {
    tl.to(sel, {scale: 1.07, duration: 0.1, ease: "power2.out"}, t);
    tl.to(sel, {scale: 1, duration: 0.45, ease: SP}, t + 0.1);
  }
  // iris: a takeover opens out of (x, y) and later closes back into another point
  function irisOpen(sel, t, x, y, d) {
    tl.set(sel, {autoAlpha: 1}, t);
    tl.fromTo(sel, {clipPath: "circle(0px at " + x + "px " + y + "px)"},
              {clipPath: "circle(2300px at " + x + "px " + y + "px)", duration: d || 0.85, ease: "power3.inOut", immediateRender: false}, t);
  }
  function irisClose(sel, t, x, y, d) {
    tl.to(sel, {clipPath: "circle(0px at " + x + "px " + y + "px)", duration: d || 0.6, ease: "power3.inOut"}, t);
    tl.set(sel, {autoAlpha: 0}, t + (d || 0.6) + 0.02);
  }
  function drift(sel, t, dur) {
    ["a1", "a2", "a3"].forEach(function (c, i) {
      var v = [[-140, 90], [160, -120], [-90, -60]][i];
      tl.fromTo(sel + " .aur." + c, {x: 0, y: 0}, {x: v[0], y: v[1], duration: dur, ease: "sine.inOut"}, t);
    });
  }
  function haptic(sel, t) { tl.to(sel, {keyframes: {x: [0, -9, 8, -5, 3, 0]}, duration: 0.34, ease: "none"}, t); }
  function count(sel, t, to, d, fmt) {
    var o = {v: 0}, el = document.querySelector(sel);
    tl.fromTo(o, {v: 0}, {v: to, duration: d || 1.1, ease: "power2.out",
              onUpdate: function () { el.textContent = fmt ? fmt(o.v) : Math.round(o.v); }}, t);
  }
  return {blurIn: blurIn, blurOut: blurOut, arrive: arrive, inner: inner, sheen: sheen,
          drawPrep: drawPrep, draw: draw, packet: packet, ripple: ripple, bump: bump,
          irisOpen: irisOpen, irisClose: irisClose, drift: drift, haptic: haptic, count: count};
}
"""


def _path(name):
    svg = io.open(os.path.join(ICONS, name + ".svg"), encoding="utf-8").read()
    return re.search(r'<path d="([^"]+)"', svg).group(1)


def available():
    return sorted(f[:-4] for f in os.listdir(ICONS) if f.endswith(".svg"))


class Glass(object):
    """`marks` are simple-icons slugs under assets/icons (monochrome 24x24
    paths). Fetch a missing one with:
        curl -o assets/icons/<slug>.svg https://cdn.jsdelivr.net/npm/simple-icons@13/icons/<slug>.svg
    """

    def __init__(self, marks=()):
        self.marks = list(marks)

    def css(self):
        return FONTS + MATERIALS

    def js(self):
        return MOTION

    def defs(self, extra=""):
        sym = "\n".join('<symbol id="i-%s" viewBox="0 0 24 24"><path d="%s"/></symbol>'
                        % (n, _path(n)) for n in self.marks)
        return ('<svg width="0" height="0" style="position:absolute"><defs>'
                '<linearGradient id="gw" x1="0" y1="0" x2="0" y2="1">'
                '<stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#ffdbe6"/>'
                '</linearGradient>%s\n%s</defs></svg>' % (extra, sym))

    def mark(self, name, cls="mk"):
        if name not in self.marks:
            self.marks.append(name)
        return ('<svg class="%s"><use href="#i-%s" width="100%%" height="100%%"/></svg>'
                % (cls, name))

    @staticmethod
    def wordmark(text, dot=False, size=128):
        return '<span class="wmark" style="font-size:%dpx">%s%s</span>' % (
            size, text, "<i>.</i>" if dot else "")
