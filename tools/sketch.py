# -*- coding: utf-8 -*-
"""The Google x Excalidraw look (STYLE.md §0b, from the 2026-11-20 batch).

Her brief, 2026-11-20: *"edit these reels in the google+excalidraw style"*.

What that means here, in one breath: a whiteboard someone is sketching on live.
Hand-drawn, slightly wobbly ink strokes that DRAW THEMSELVES ON (never fade in),
hachure fills, Excalidraw's handwriting (Excalifont, merged with its Cyrillic
subsets so Ukrainian works) for labels and annotations — and Google's side of it:
the four Google colours as the only accents, Google Sans for titles and numbers,
clean Material cards, pills, chips, toggles and the four-dot "thinking" loader.

    from sketch import Sketch, SKETCH_CSS, SKETCH_JS
    sk = Sketch(seed=41)
    svg = sk.svg(1080, 600, sk.rect(100, 80, 400, 220, fill="blue") +
                            sk.arrow([(520, 190), (700, 150), (860, 260)]) +
                            sk.ellipse(880, 300, 120, 80, fill="yellow", style="solid"))

Every stroke is a <path pathLength="1" class="dr">: the JS helper `draw(sel, t,
d)` draws all of them inside `sel` in document order, so a shape is drawn the way
a hand would (outline first pass, second pass, then the fill hachure).

Python generates the roughness (seeded, deterministic) — nothing random at
render time, so a re-render is pixel-identical.
"""
import math
import random

INK = "#1e1e1e"
G = {   # Google's four, plus Excalidraw's pastel fill for each
    "blue": ("#4285F4", "#a5d8ff"), "red": ("#EA4335", "#ffc9c9"),
    "yellow": ("#FBBC04", "#ffec99"), "green": ("#34A853", "#b2f2bb"),
    "ink": (INK, "#e9ecef"), "white": ("#ffffff", "#ffffff"),
}


def col(name):
    return G[name][0] if name in G else name


def pastel(name):
    return G[name][1] if name in G else name


class Sketch(object):
    def __init__(self, seed=1, rough=1.0):
        self.r = random.Random(seed)
        self.k = rough

    # ------------------------------------------------------------ primitives
    def _j(self, o):
        return self.r.uniform(-o, o) * self.k

    def _seg(self, x1, y1, x2, y2, o=None, move=True):
        """one rough.js-style bowed cubic from p1 to p2"""
        L = math.hypot(x2 - x1, y2 - y1) or 1.0
        o = min(2.4, L * 0.04) if o is None else o
        nx, ny = -(y2 - y1) / L, (x2 - x1) / L
        bow = self.r.uniform(-1, 1) * min(L * 0.012, 3.2) * self.k
        d = self.r.uniform(0.2, 0.4)
        sx, sy = x1 + self._j(o), y1 + self._j(o)
        ex, ey = x2 + self._j(o), y2 + self._j(o)
        c1 = (x1 + (x2 - x1) * d + nx * bow + self._j(o), y1 + (y2 - y1) * d + ny * bow + self._j(o))
        c2 = (x1 + (x2 - x1) * 2 * d + nx * bow + self._j(o), y1 + (y2 - y1) * 2 * d + ny * bow + self._j(o))
        return ("M%.1f %.1f " % (sx, sy) if move else "") + "C%.1f %.1f %.1f %.1f %.1f %.1f" % (
            c1[0], c1[1], c2[0], c2[1], ex, ey)

    def _closed(self, pts, o=2.2, over=0.06):
        """a closed hand-drawn curve through pts (catmull-rom), jittered, which
        overshoots its own start a little — the tell of a pen stroke"""
        n = len(pts)
        jp = [(x + self._j(o), y + self._j(o)) for x, y in pts]
        extra = max(2, int(n * over))
        seq = jp + jp[:extra + 2]
        sx, sy = seq[0]
        d = ["M%.1f %.1f" % (sx, sy)]
        for i in range(1, len(seq) - 2):
            p0, p1, p2, p3 = seq[i - 1], seq[i], seq[i + 1], seq[i + 2]
            c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
            c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
            d.append("C%.1f %.1f %.1f %.1f %.1f %.1f" % (c1[0], c1[1], c2[0], c2[1], p2[0], p2[1]))
        return " ".join(d)

    def _open(self, pts, o=1.4):
        jp = [(x + self._j(o), y + self._j(o)) for x, y in pts]
        if len(jp) == 2:
            return self._seg(jp[0][0], jp[0][1], jp[1][0], jp[1][1], o=o)
        seq = [jp[0]] + jp + [jp[-1]]
        d = ["M%.1f %.1f" % jp[0]]
        for i in range(1, len(seq) - 2):
            p0, p1, p2, p3 = seq[i - 1], seq[i], seq[i + 1], seq[i + 2]
            c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
            c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
            d.append("C%.1f %.1f %.1f %.1f %.1f %.1f" % (c1[0], c1[1], c2[0], c2[1], p2[0], p2[1]))
        return " ".join(d)

    @staticmethod
    def _p(d, stroke, sw, cls="dr", extra=""):
        return ('<path class="%s" pathLength="1" d="%s" fill="none" stroke="%s" '
                'stroke-width="%.1f" stroke-linecap="round" stroke-linejoin="round"%s/>'
                % (cls, d, stroke, sw, extra))

    # ----------------------------------------------------------------- fills
    def _hachure(self, poly, color, gap=14, angle=-41, sw=3.0, cross=False):
        out = []
        for ang in ([angle, angle + 82] if cross else [angle]):
            a = math.radians(ang)
            ca, sa = math.cos(a), math.sin(a)
            rot = [(x * ca + y * sa, -x * sa + y * ca) for x, y in poly]
            ys = [p[1] for p in rot]
            y = min(ys) + gap * 0.6
            segs = []
            while y < max(ys):
                xs = []
                for i in range(len(rot)):
                    (x1, y1), (x2, y2) = rot[i], rot[(i + 1) % len(rot)]
                    if (y1 <= y < y2) or (y2 <= y < y1):
                        xs.append(x1 + (y - y1) * (x2 - x1) / (y2 - y1))
                xs.sort()
                for i in range(0, len(xs) - 1, 2):
                    if xs[i + 1] - xs[i] > 6:
                        p = [(xx * ca - y * sa, xx * sa + y * ca) for xx in (xs[i] + 2, xs[i + 1] - 2)]
                        segs.append(self._seg(p[0][0], p[0][1], p[1][0], p[1][1], o=1.6))
                y += gap
            # zig-zag order reads like a hand going back and forth
            out.append(" ".join(segs))
        return self._p(" ".join(out), color, sw, "dr hz")

    def _fill(self, poly, fill, style, closed_d):
        if not fill:
            return ""
        if style == "solid":
            return '<path class="sf" d="%s" fill="%s" stroke="none"/>' % (closed_d, pastel(fill))
        return self._hachure(poly, col(fill), cross=(style == "cross"))

    # ---------------------------------------------------------------- shapes
    def rect(self, x, y, w, h, stroke=INK, sw=4.5, fill=None, style="hachure", round_=True):
        """Excalidraw rectangle. round_=True is Excalidraw's 'round' edges."""
        r = min(28, w * 0.16, h * 0.16) if round_ else 0
        pts = []
        if r:
            # perimeter polyline with rounded corners
            corners = [(x + w - r, y + r, -90), (x + w - r, y + h - r, 0), (x + r, y + h - r, 90), (x + r, y + r, 180)]
            for cx, cy, a0 in corners:
                for k in range(0, 4):
                    a = math.radians(a0 + k * 30)
                    pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
            # insert midpoints on long sides so the jitter has room to wander
            dense = []
            for i in range(len(pts)):
                p, q = pts[i], pts[(i + 1) % len(pts)]
                dense.append(p)
                L = math.hypot(q[0] - p[0], q[1] - p[1])
                for m in range(1, int(L // 140) + 1):
                    t = m / (int(L // 140) + 1)
                    dense.append((p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t))
            pts = dense
            # rotate start so the stroke begins mid top edge, like a hand would
            d1 = self._closed(pts, o=1.6)
            d2 = self._closed(pts[3:] + pts[:3], o=2.6, over=0.03)
            poly = pts
            closed = d1
        else:
            c = [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]
            d1 = " ".join(self._seg(*c[i], *c[(i + 1) % 4]) for i in range(4))
            d2 = " ".join(self._seg(*c[i], *c[(i + 1) % 4]) for i in range(4))
            poly = c
            closed = "M%.1f %.1f L%.1f %.1f L%.1f %.1f L%.1f %.1f Z" % sum(c, ())
        return (self._fill(poly, fill, style, closed) +
                self._p(d1, col(stroke), sw) + self._p(d2, col(stroke), sw * 0.62))

    def ellipse(self, cx, cy, rx, ry, stroke=INK, sw=4.5, fill=None, style="hachure"):
        n = max(16, int((rx + ry) / 7))
        a0 = self.r.uniform(0, 2 * math.pi)
        pts = [(cx + rx * math.cos(a0 + 2 * math.pi * i / n), cy + ry * math.sin(a0 + 2 * math.pi * i / n))
               for i in range(n)]
        d1 = self._closed(pts, o=min(rx, ry) * 0.012 + 0.8, over=0.1)
        d2 = self._closed(pts[2:] + pts[:2], o=min(rx, ry) * 0.022 + 1.2, over=0.05)
        return (self._fill(pts, fill, style, d1) +
                self._p(d1, col(stroke), sw) + self._p(d2, col(stroke), sw * 0.55))

    def diamond(self, cx, cy, w, h, stroke=INK, sw=4.5, fill=None, style="hachure"):
        c = [(cx, cy - h / 2), (cx + w / 2, cy), (cx, cy + h / 2), (cx - w / 2, cy)]
        d1 = " ".join(self._seg(*c[i], *c[(i + 1) % 4]) for i in range(4))
        d2 = " ".join(self._seg(*c[i], *c[(i + 1) % 4]) for i in range(4))
        closed = "M%.1f %.1f L%.1f %.1f L%.1f %.1f L%.1f %.1f Z" % sum(c, ())
        return (self._fill(c, fill, style, closed) + self._p(d1, col(stroke), sw) +
                self._p(d2, col(stroke), sw * 0.6))

    def line(self, pts, stroke=INK, sw=4.5, double=True):
        d = self._open(pts)
        out = self._p(d, col(stroke), sw)
        if double:
            out += self._p(self._open(pts, o=2.2), col(stroke), sw * 0.5)
        return out

    def arrow(self, pts, stroke=INK, sw=5, head=30, both=False, dashed=False):
        """Excalidraw arrow: a curve through pts, an open arrowhead at the end"""
        d = self._open(pts, o=1.2)
        extra = ' stroke-dasharray="0.03 0.025"' if dashed else ""
        out = self._p(d, col(stroke), sw, "dr" if not dashed else "dr dash", extra)

        def headat(p, q):
            a = math.atan2(p[1] - q[1], p[0] - q[0])
            h = []
            for s in (-1, 1):
                b = a + s * math.radians(28)
                h.append(self._seg(p[0], p[1], p[0] - head * math.cos(b), p[1] - head * math.sin(b), o=1.0))
            return self._p(" ".join(h), col(stroke), sw, "dr ah")
        out += headat(pts[-1], pts[-2])
        if both:
            out += headat(pts[0], pts[1])
        return out

    def underline(self, x, y, w, stroke="red", sw=7, twice=False):
        pts = [(x, y), (x + w * 0.5, y + self.r.uniform(-3, 3)), (x + w, y - 4)]
        out = self._p(self._open(pts, o=2), col(stroke), sw)
        if twice:
            pts2 = [(x + w * 0.06, y + 13), (x + w * 0.55, y + 11), (x + w * 0.96, y + 8)]
            out += self._p(self._open(pts2, o=2), col(stroke), sw * 0.8)
        return out

    def circle_around(self, cx, cy, rx, ry, stroke="red", sw=6):
        """the loose loop a hand draws around a word — 1.15 turns, not closed"""
        n = 24
        a0 = math.radians(-160)
        pts = []
        for i in range(int(n * 1.15)):
            a = a0 + 2 * math.pi * i / n
            k = 1 + 0.06 * i / n
            pts.append((cx + rx * k * math.cos(a), cy + ry * k * math.sin(a)))
        return self._p(self._open(pts, o=2.5), col(stroke), sw)

    def check(self, x, y, s=60, stroke="green", sw=8):
        pts = [(x, y + s * 0.5), (x + s * 0.36, y + s * 0.86), (x + s, y)]
        return self._p(self._open(pts, o=1.5), col(stroke), sw)

    def cross(self, x, y, s=60, stroke="red", sw=8):
        return self._p(self._seg(x, y, x + s, y + s, o=2) + " " + self._seg(x + s, y, x, y + s, o=2),
                       col(stroke), sw)

    def scribble(self, x, y, w, h, stroke="red", sw=6):
        """crossing-out zig-zag over something wrong"""
        pts, n = [], max(4, int(w / 26))
        for i in range(n + 1):
            pts.append((x + w * i / n, y + (h if i % 2 else 0) + self._j(4)))
        return self._p(self._open(pts, o=1.5), col(stroke), sw)

    def spark(self, cx, cy, s=26, stroke="yellow", sw=6):
        """three short dashes radiating — Excalidraw's 'emphasis' marks"""
        out = []
        for a in (-60, -20, 20):
            r = math.radians(a - 90)
            out.append(self._seg(cx + s * 0.6 * math.cos(r), cy + s * 0.6 * math.sin(r),
                                 cx + s * 1.6 * math.cos(r), cy + s * 1.6 * math.sin(r), o=1))
        return self._p(" ".join(out), col(stroke), sw)

    def marker(self, x, y, w, h, color="yellow"):
        """highlighter band behind a word (sits under the text, multiply)"""
        pts = [(x, y + 6), (x + w, y), (x + w + 6, y + h - 4), (x - 4, y + h)]
        d = self._closed([(px + self._j(3), py + self._j(3)) for px, py in pts], o=1.5, over=0)
        return '<path class="mk" d="%s" fill="%s" opacity="0.85"/>' % (d, pastel(color))

    @staticmethod
    def svg(w, h, body, cls="sk", sid="", style=""):
        return ('<svg class="%s"%s viewBox="0 0 %d %d" width="%d" height="%d"%s>%s</svg>'
                % (cls, (' id="%s"' % sid) if sid else "", w, h, w, h,
                   (' style="%s"' % style) if style else "", body))


# ---------------------------------------------------------------------------
SKETCH_CSS = r"""
    @font-face { font-family: "Hand"; src: url("assets/fonts/Excalifont.ttf") format("truetype");
                 font-display: block; }
    @font-face { font-family: "Cap"; src: url("assets/fonts/ProductSans-Bold.ttf") format("truetype");
                 font-weight: 900; font-display: block; }
%(gsans)s
    #root { --ink: #1e1e1e; --gb: #4285F4; --gr: #EA4335; --gy: #FBBC04; --gg: #34A853;
            --pb: #a5d8ff; --pr: #ffc9c9; --py: #ffec99; --pg: #b2f2bb;
            --paper: #ffffff; --line: #dadce0; --sub: #5f6368;
            --e1: 0 1px 2px rgba(60,64,67,.30), 0 1px 3px 1px rgba(60,64,67,.15);
            --e3: 0 4px 8px 3px rgba(60,64,67,.15), 0 1px 3px rgba(60,64,67,.30);
            --e5: 0 8px 12px 6px rgba(60,64,67,.15), 0 4px 4px rgba(60,64,67,.30); }
    .cap { font-family: "Cap", system-ui, sans-serif !important; }
    .hand { font-family: "Hand", "Cap", sans-serif; color: var(--ink); line-height: 1.12;
            letter-spacing: 0; }
    .gs { font-family: "GSans", "Cap", sans-serif; color: #202124; letter-spacing: -0.01em; }
    .sk { position: absolute; left: 0; top: 0; overflow: visible; }
    .sk .dr { stroke-dasharray: 1 2; stroke-dashoffset: 1.05; }
    .sk .dr.dash { stroke-dasharray: 0.03 0.025; stroke-dashoffset: 0; }

    /* a Material card: white, 28px corners, elevation shadow — Google's side */
    .gcard { position: absolute; background: #fff; border-radius: 28px; box-shadow: var(--e3); }
    .gcard.flat { box-shadow: var(--e1); }
    /* paper: the Excalidraw side — a white sheet with a hand-drawn edge (draw the
       edge with sk.rect inside it), a whisker of tilt, a soft cast shadow */
    .paper { position: absolute; background: #fff; border-radius: 22px;
             box-shadow: 0 18px 40px rgba(0,0,0,.22), 0 2px 6px rgba(0,0,0,.12); }
    .pill { position: absolute; display: flex; align-items: center; gap: 18px;
            background: #fff; border-radius: 999px; box-shadow: var(--e3);
            font-family: "GSans", sans-serif; color: #202124; }
    .chip { display: inline-flex; align-items: center; gap: 12px; padding: 0 30px;
            height: 72px; border-radius: 20px; border: 2px solid var(--line); background: #fff;
            font-family: "GSans", sans-serif; font-weight: 500; font-size: 34px; color: #3c4043; }
    .chip.on { background: #d3e3fd; border-color: #d3e3fd; color: #041e49; }
    .chip.cg { background: #c4eed0; border-color: #c4eed0; color: #072711; }
    .chip.cr { background: #ffdad6; border-color: #ffdad6; color: #410002; }
    .chip.cy { background: #ffefc2; border-color: #ffefc2; color: #3d2e00; }
    /* the four-dot loader, Google's "thinking" */
    .dots { position: absolute; display: flex; gap: 18px; }
    .dots i { display: block; width: 30px; height: 30px; border-radius: 50%%; }
    .dots i:nth-child(1) { background: var(--gb); } .dots i:nth-child(2) { background: var(--gr); }
    .dots i:nth-child(3) { background: var(--gy); } .dots i:nth-child(4) { background: var(--gg); }
    /* Material toggle */
    .tgl { position: absolute; width: 104px; height: 64px; border-radius: 32px; background: #e1e3e1;
           border: 4px solid #747775; }
    .tgl b { position: absolute; left: 10px; top: 10px; width: 36px; height: 36px; border-radius: 50%%;
             background: #747775; }
    /* §0c layouts. A .sheet is a full-width panel from the top edge down to
       its own height; her plate is pushed down under it (plateDown), so the
       panel never covers her head. .sheet.board-bg = halfscreen (a scheme on
       the whiteboard); a plain .sheet holds a mockup (browser, app screen). */
    .sheet { position: absolute; left: 0; top: 0; width: 1080px; overflow: hidden;
             box-shadow: 0 10px 30px rgba(0,0,0,.28), 0 2px 6px rgba(0,0,0,.18); }
    .sheet.board-bg { background-color: #fff;
             background-image: radial-gradient(circle, rgba(30,30,30,.16) 2px, transparent 2.6px);
             background-size: 44px 44px; background-position: 11px 11px; }
    .sheet .edge { position: absolute; left: 0; right: 0; bottom: 0; height: 6px; }
    /* whiteboard: Excalidraw's canvas — white with a faint dot grid */
    .board { position: absolute; inset: 0; background-color: #fff;
             background-image: radial-gradient(circle, rgba(30,30,30,.16) 2px, transparent 2.6px);
             background-size: 44px 44px; background-position: 11px 11px; }
    /* free strokes over her footage need to survive a busy background */
    .over-plate .dr, .over-plate .hand { filter: drop-shadow(0 2px 5px rgba(0,0,0,.35)); }
    .wbox { position: absolute; }
    .num { font-family: "GSans", sans-serif; font-weight: 700; letter-spacing: -0.04em; color: #202124; }
"""


def sketch_css():
    """the look's CSS, with Google Sans (latin + cyrillic subsets, self-hosted
    from assets/fonts/gsans — copy that folder's woff2 into the reel's
    assets/fonts/)"""
    import os
    p = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                     "assets", "fonts", "gsans", "fontfaces.css")
    return SKETCH_CSS % {"gsans": "    " + open(p).read().replace("\n", "\n    ")}


SKETCH_JS = r"""
function spring(z, w) {
  var wd = w * Math.sqrt(1 - z * z);
  function f(t) { return 1 - Math.exp(-z * w * t) * (Math.cos(wd * t) + (z * w / wd) * Math.sin(wd * t)); }
  var e = f(1);
  return function (t) { return t >= 1 ? 1 : f(t) / e; };
}
var SP = spring(0.62, 13), POP = spring(0.46, 14), SOFT = spring(0.84, 11);

function sketchHelpers(tl) {
  var Q = function (s) { return Array.prototype.slice.call(document.querySelectorAll(s)); };
  // draw every stroke inside sel in document order — a hand drawing it.
  // d is the total time; hachure strokes go faster than outlines.
  function draw(sel, t, d) {
    var ps = Q(sel + " .dr").filter(function (p) { return !p.classList.contains("dash"); });
    if (!ps.length && document.querySelector(sel) && document.querySelector(sel).classList.contains("dr")) ps = Q(sel);
    var w = ps.map(function (p) { return p.classList.contains("hz") ? 0.6 : (p.classList.contains("ah") ? 0.25 : 1); });
    var sum = w.reduce(function (a, b) { return a + b; }, 0) || 1, at = t;
    d = d || 0.7;
    ps.forEach(function (p, i) {
      var dd = d * w[i] / sum;
      tl.fromTo(p, {strokeDashoffset: 1.05}, {strokeDashoffset: 0, duration: dd, ease: "power1.inOut", immediateRender: false}, at);
      at += dd;
    });
    Q(sel + " .dr.dash").forEach(function (p) { tl.fromTo(p, {autoAlpha: 0}, {autoAlpha: 1, duration: 0.25, immediateRender: false}, t); });
    Q(sel + " .sf, " + sel + " .mk").forEach(function (p) {
      tl.fromTo(p, {autoAlpha: 0}, {autoAlpha: 1, duration: 0.3, ease: "power1.out", immediateRender: false}, t + d * 0.5);
    });
    return at;
  }
  // erase: the strokes un-draw backwards, fast
  function undraw(sel, t, d) {
    var ps = Q(sel + " .dr").reverse(); d = d || 0.35;
    ps.forEach(function (p, i) { tl.to(p, {strokeDashoffset: 1.05, duration: d, ease: "power1.in"}, t); });
    Q(sel + " .sf, " + sel + " .mk").forEach(function (p) { tl.to(p, {autoAlpha: 0, duration: d}, t); });
  }
  // handwriting: the text is revealed left to right, like ink going down
  function write(sel, t, d) {
    tl.set(sel, {autoAlpha: 1}, t);
    tl.fromTo(sel, {clipPath: "inset(-20% 100% -20% 0%)"},
              {clipPath: "inset(-20% -2% -20% 0%)", duration: d || 0.55, ease: "power1.inOut", immediateRender: false}, t);
  }
  // a Material object lands: scale with a spring, a whisker of tilt that settles
  function pop(sel, t, o) {
    o = o || {};
    tl.fromTo(sel, {autoAlpha: 0, scale: o.s == null ? 0.6 : o.s, rotation: o.r == null ? -4 : o.r, y: o.y == null ? 24 : o.y},
              {autoAlpha: 1, scale: 1, rotation: o.to || 0, y: 0, duration: o.d || 0.7, ease: o.ease || POP, immediateRender: true}, t);
  }
  function show(sel, t) { tl.set(sel, {autoAlpha: 1}, t); }
  function out(sel, t, d) { tl.to(sel, {autoAlpha: 0, scale: 0.92, duration: d || 0.25, ease: "power2.in"}, t); }
  function fadeOut(sel, t, d) { tl.to(sel, {autoAlpha: 0, duration: d || 0.25, ease: "power1.in"}, t); }
  function bump(sel, t) {
    tl.to(sel, {scale: 1.08, duration: 0.1, ease: "power2.out"}, t);
    tl.to(sel, {scale: 1, duration: 0.45, ease: SP}, t + 0.1);
  }
  function wiggle(sel, t) { tl.to(sel, {keyframes: {rotation: [0, -5, 4, -2.5, 1, 0]}, duration: 0.5, ease: "none"}, t); }
  // the four Google dots bounce in sequence while something "thinks"
  function think(sel, t, d) {
    var dots = Q(sel + " i"), n = Math.max(1, Math.floor((d || 1.2) / 0.6));
    dots.forEach(function (el, i) {
      for (var k = 0; k < n; k++)
        tl.to(el, {keyframes: {y: [0, -22, 0]}, duration: 0.42, ease: "sine.inOut"}, t + k * 0.6 + i * 0.09);
    });
  }
  function toggle(sel, t, color) {
    tl.to(sel, {backgroundColor: color || "#0b57d0", borderColor: color || "#0b57d0", duration: 0.18}, t);
    tl.to(sel + " b", {x: 40, scale: 1.18, backgroundColor: "#fff", duration: 0.45, ease: SP}, t);
  }
  // typing into a Google search pill / input: chars appear one by one
  function type(sel, t, cps) {
    var el = document.querySelector(sel), txt = el.getAttribute("data-text") || "", o = {n: 0};
    cps = cps || 22;
    tl.fromTo(o, {n: 0}, {n: txt.length, duration: txt.length / cps, ease: "none", immediateRender: true,
      onUpdate: function () { el.textContent = txt.slice(0, Math.round(o.n)); }}, t);
  }
  function count(sel, t, to, d, fmt) {
    var o = {v: 0}, el = document.querySelector(sel);
    tl.fromTo(o, {v: 0}, {v: to, duration: d || 1.0, ease: "power2.out", immediateRender: false,
              onUpdate: function () { el.textContent = fmt ? fmt(o.v) : Math.round(o.v); }}, t);
  }
  // the whiteboard takes over: it is wiped in by a marker sweep from a point
  function boardIn(sel, t, x, y, d) {
    tl.set(sel, {autoAlpha: 1}, t);
    tl.fromTo(sel, {clipPath: "circle(0px at " + x + "px " + y + "px)"},
              {clipPath: "circle(2300px at " + x + "px " + y + "px)", duration: d || 0.75, ease: "power3.inOut", immediateRender: false}, t);
  }
  function boardOut(sel, t, x, y, d) {
    tl.to(sel, {clipPath: "circle(0px at " + x + "px " + y + "px)", duration: d || 0.55, ease: "power3.inOut"}, t);
    tl.set(sel, {autoAlpha: 0}, t + (d || 0.55) + 0.02);
  }
  // infinite canvas: pan/zoom the board's camera layer to frame the next idea
  function pan(sel, t, x, y, s, d) {
    tl.to(sel, {x: x, y: y, scale: s == null ? 1 : s, duration: d || 0.8, ease: "power3.inOut"}, t);
  }
  // §0c — her plate moves. plateDown: push her down by d px (spring), so a
  // panel/card above her never sits on her head. plateUp: back to full frame.
  function plateDown(t, d, dur) {
    tl.to("#platebox", {y: d, duration: dur || 0.75, ease: SP}, t);
  }
  function plateUp(t, dur) {
    tl.to("#platebox", {y: 0, duration: dur || 0.6, ease: "power3.inOut"}, t);
  }
  // halfscreen / mockup sheet: the panel drops in from the top edge while she
  // is pushed down by the same move; out = the panel rolls back up and she
  // rises. h = panel height, d = how far she moves (default h - 560: her
  // hairline sits ~40 px under the panel's edge).
  function sheetIn(sel, t, h, d, dur) {
    dur = dur || 0.7; d = d == null ? Math.max(0, h - 580) : d;
    tl.set(sel, {autoAlpha: 1}, t);
    tl.fromTo(sel, {y: -h - 40}, {y: 0, duration: dur, ease: SOFT, immediateRender: false}, t);
    plateDown(t, d, dur + 0.1);
  }
  function sheetOut(sel, t, h, dur) {
    dur = dur || 0.55;
    tl.to(sel, {y: -h - 40, duration: dur, ease: "power3.in"}, t);
    tl.set(sel, {autoAlpha: 0}, t + dur + 0.02);
    plateUp(t + 0.05, dur + 0.1);
  }
  return {plateDown: plateDown, plateUp: plateUp, sheetIn: sheetIn, sheetOut: sheetOut,
          draw: draw, undraw: undraw, write: write, pop: pop, show: show, out: out, fadeOut: fadeOut,
          bump: bump, wiggle: wiggle, think: think, toggle: toggle, type: type, count: count,
          boardIn: boardIn, boardOut: boardOut, pan: pan};
}
"""
