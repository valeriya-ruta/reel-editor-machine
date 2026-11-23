# -*- coding: utf-8 -*-
"""The AI-slop carousel slide — a reusable component (reels 13, 17, 19).

The one sanctioned off-palette frame in the series (W40.md). It is the bare
"before": what an image model hands back when you ask it for a carousel —
rainbow ground, sunburst, extruded 3D title, a glowing button, garbled text
(«ЗРОСТУУТЬ», «1О разіів» — the tell of text drawn by a picture model) and
far too many stickers. It has to look *confidently* bad, so the clean slide
that follows it pays off.

Budget-safe on purpose (STYLE.md §5a.1 box): no filter, no clip-path, no
radial-gradient anywhere — glows are box-/text-shadows, the sunburst is a
conic gradient, sticker borders are SVG strokes (the white die-cut edge).

    import sys; sys.path.insert(0, os.path.join(ROOT, "reel-13"))
    from slop import Slop
    s = Slop()
    k.css(s.css())
    html = s.slide("sl1", 300, extra=[("rocket", -180, 420, 300, -20), ...])
    gfx_html = s.defs() + html + ...          # defs once per document
    gfx_js   = s.js() + 'slopPop(tl, "sl1", 33.680, 0.13);'

The slide is designed at 1080x1440 (3:4, IG's portrait grid) and scaled to
`w`; everything sits inside a 4:5 safe area too, so a caller can crop it to
1080x1350 with `h`. `extra` stickers are hidden until `slopPop` slaps them
on; coordinates are native (1080-wide) and may fall outside the slide — that
is the point, they spill over its edges. `slopShed` knocks every sticker off.
The motion needs `POP` from tools/glass.py (Glass.js()).
"""

NATIVE_W, NATIVE_H = 1080, 1440

# --- sticker artwork, 100x100 viewBox. White die-cut edge = paint-order stroke.
ART = {
    "burst": '<polygon points="%s"/>',
    "spark": '<path d="M50 2C54 34 66 46 98 50C66 54 54 66 50 98C46 66 34 54 2 50C34 46 46 34 50 2Z"/>',
    "star": '<polygon points="50,4 62,36 96,37 69,58 79,92 50,72 21,92 31,58 4,37 38,36"/>',
    "heart": '<path d="M50 90S8 64 8 35C8 20 19 10 32 10c8 0 14 4 18 11c4-7 10-11 18-11c13 0 24 10 24 25c0 29-42 55-42 55z"/>',
    "bolt": '<polygon points="60,2 16,58 46,58 36,98 86,38 56,38 72,2"/>',
    "crown": '<path d="M8 80L14 24L34 52L50 12L66 52L86 24L92 80Z"/>',
    "bubble": '<path d="M50 8C75 8 95 22 95 42S75 76 50 76c-5 0-10-.5-14-1.5L14 92l6-20C10 65 5 54 5 42C5 22 25 8 50 8Z"/>',
    "flame": '<path d="M50 96C26 96 12 80 12 60C12 40 30 30 34 8c10 10 12 22 10 30c6-4 10-12 10-20c18 14 34 32 34 50c0 18-16 28-38 28Z"/>',
    "arrow": '<path d="M8 70C20 34 50 20 74 26L72 12L96 34L68 52L70 38C50 34 30 44 20 76Z"/>',
    "rocket": ('<path d="M50 4C66 16 72 36 70 60H30C28 36 34 16 50 4Z"/>'
               '<path d="M30 48L14 70L30 66Z"/><path d="M70 48L86 70L70 66Z"/>'),
    "tag": '<path d="M8 38L38 8H90V60L60 90Z"/>',
    "orb": '<circle cx="50" cy="50" r="44"/>',
}


def _burst(n=16, r0=48, r1=34):
    import math
    pts = []
    for i in range(n * 2):
        a = math.pi * i / n - math.pi / 2
        r = r0 if i % 2 == 0 else r1
        pts.append("%.1f,%.1f" % (50 + r * math.cos(a), 50 + r * math.sin(a)))
    return " ".join(pts)


# kind -> (fill, stroke-accent, label, label colour, label size as % of sticker)
LOOK = {
    "burst": ("#fff22b", "#ff2bd6", "NEW!", "#e0007a", 0.26),
    "badge": ("#ff2bd6", "#fff22b", "100%", "#ffffff", 0.25),
    "spark": ("#fff22b", None, "", "", 0),
    "sparkc": ("#2bf0ff", None, "", "", 0),
    "sparkw": ("#ffffff", None, "", "", 0),
    "star": ("#2bf0ff", "#7a2bff", "", "", 0),
    "heart": ("#ff2b8a", "#ffffff", "", "", 0),
    "bolt": ("#fff22b", "#5b00d6", "", "", 0),
    "crown": ("#ffd400", "#ff8a00", "", "", 0),
    "bubble": ("#ffffff", "#2b6bff", "WOW!", "#2b3bff", 0.25),
    "flame": ("#ff7a00", "#ffd400", "", "", 0),
    "arrow": ("#b6ff2b", "#00a86b", "", "", 0),
    "rocket": ("#e6e6ff", "#ff2bd6", "", "", 0),
    "tag": ("#2bff9c", "#008a55", "-50%", "#004d30", 0.22),
    "orb": ("#7a2bff", "#2bf0ff", "AI", "#ffffff", 0.3),
}

# the base look: what is already stuck on before anyone slaps more on
BASE = [
    ("burst", 900, 190, 250, 14),
    ("sparkc", 140, 130, 130, 0),
    ("spark", 975, 720, 100, 10),
    ("badge", 175, 1190, 230, -12),
    ("bolt", 935, 1160, 210, 16),
    ("heart", 110, 700, 120, -16),
    ("sparkw", 820, 470, 70, 0),
]

CSS = """
/* ---- the AI-slop slide (reel-13/slop.py) — off-palette on purpose ---- */
.slop { position: absolute; }
.slop .sl-art { position: absolute; left: 0; top: 0; width: 1080px; height: 1440px;
  transform-origin: 0 0; overflow: visible; border-radius: 40px; color: #fff;
  font-family: "ProductSans", system-ui, sans-serif;
  background: linear-gradient(160deg, #ff2bd6 0%, #8a2bff 28%, #2bb8ff 52%, #6dffb0 70%,
              #fff22b 86%, #ff8a00 100%);
  box-shadow: inset 0 0 0 16px rgba(255,255,255,0.55), 0 0 60px 16px rgba(255,43,214,0.75),
              0 0 130px 40px rgba(43,217,255,0.45); }
.slop .sl-sun { position: absolute; inset: 0; border-radius: 40px;
  background: repeating-conic-gradient(from 0deg at 50% 30%, rgba(255,255,255,0.26) 0deg 7deg,
              rgba(255,255,255,0) 7deg 17deg); }
.slop .sl-dot { position: absolute; border-radius: 50%; }
.slop .sl-pill { position: absolute; left: 50%; top: 118px; transform: translateX(-50%) rotate(-3deg);
  white-space: nowrap; padding: 16px 44px; border-radius: 50px; background: #2bf0ff; color: #6a00d6;
  font-size: 46px; font-weight: 900; letter-spacing: 0.04em;
  box-shadow: 0 0 0 6px #fff, 0 0 40px 10px rgba(43,240,255,0.9); }
.slop .sl-t { position: absolute; left: 0; width: 1080px; text-align: center; font-weight: 900;
  line-height: 1; letter-spacing: -0.02em; color: #fff22b; white-space: nowrap;
  -webkit-text-stroke: 6px #5b00d6;
  text-shadow: 6px 6px 0 #ff2bd6, 12px 12px 0 #2bd9ff, 18px 18px 0 #5b00d6,
               0 0 60px rgba(255,255,255,0.95); transform: skewX(-8deg); }
.slop .sl-sub { position: absolute; left: 0; width: 1080px; text-align: center; font-size: 56px;
  font-weight: 700; color: #fff; white-space: nowrap;
  text-shadow: 0 0 24px #ff2bd6, 0 0 48px #ff2bd6, 3px 3px 0 #5b00d6; }
.slop .sl-btn { position: absolute; left: 190px; top: 1236px; width: 700px; height: 118px;
  border-radius: 59px; display: flex; align-items: center; justify-content: center;
  font-size: 46px; font-weight: 900; color: #fff; letter-spacing: 0.02em; white-space: nowrap;
  background: linear-gradient(90deg, #ff8a00 0%, #ff2bd6 50%, #7a2bff 100%);
  box-shadow: 0 0 0 6px #fff22b, 0 0 50px 14px rgba(255,43,214,0.9); }
.slop .sl-in { position: absolute; left: 0; width: 1080px; height: 1440px; }
.slop .stk { position: absolute; left: 0; top: 0; }
.slop .stk svg { position: absolute; inset: 0; width: 100%; height: 100%; overflow: visible; }
.slop .stk .sw { fill: none; stroke: #ffffff; stroke-width: 9; stroke-linejoin: round; }
.slop .stk b { position: absolute; inset: 0; display: flex; align-items: center; justify-content: center;
  font-weight: 900; letter-spacing: -0.03em; white-space: nowrap; }
.slop .stk.x { opacity: 0; visibility: hidden; }
"""

JS = r"""
/* ---- slop.py motion: stickers slapped on, and knocked off ---- */
function slopInit(sid) {
  document.querySelectorAll("#" + sid + " .stk").forEach(function (el) {
    gsap.set(el, {xPercent: -50, yPercent: -50, rotation: +el.dataset.r});
  });
}
function slopPop(tl, sid, t, gap, from, to) {
  var els = Array.prototype.slice.call(document.querySelectorAll("#" + sid + " .stk.x"));
  els.slice(from || 0, to == null ? els.length : to).forEach(function (el, i) {
    var r = +el.dataset.r, tt = t + i * (gap == null ? 0.12 : gap);
    tl.fromTo(el, {autoAlpha: 0}, {autoAlpha: 1, duration: 0.06, immediateRender: false}, tt);
    tl.fromTo(el, {scale: 2.1, rotation: r - 28}, {scale: 1, rotation: r, duration: 0.5, ease: POP,
              immediateRender: false}, tt);
  });
}
function slopShed(tl, sid, t) {
  document.querySelectorAll("#" + sid + " .stk").forEach(function (el, i) {
    var x = +el.dataset.x - 540, y = +el.dataset.y - 720, d = Math.sqrt(x * x + y * y) || 1;
    tl.to(el, {x: x / d * 900, y: y / d * 900 + 500, rotation: "+=" + (i % 2 ? 140 : -140),
               autoAlpha: 0, duration: 0.5, ease: "power2.in"}, t + (i % 5) * 0.025);
  });
}
"""


class Slop(object):
    """One per document. `slide()` as many times as needed, distinct ids."""

    def __init__(self):
        self._n = 0

    @staticmethod
    def css():
        return CSS

    @staticmethod
    def js():
        return JS

    @staticmethod
    def defs():
        sym = []
        for k, v in ART.items():
            body = v % _burst() if k == "burst" else v
            sym.append('<symbol id="slp-%s" viewBox="0 0 100 100">%s</symbol>' % (k, body))
        sym.append('<symbol id="slp-badge" viewBox="0 0 100 100"><polygon points="%s"/></symbol>'
                   % _burst(24, 48, 42))
        return ('<svg width="0" height="0" style="position:absolute"><defs>%s</defs></svg>'
                % "".join(sym))

    @staticmethod
    def sticker(kind, x, y, size, rot, extra=False):
        fill, acc, label, lcol, lsz = LOOK[kind]
        art = {"sparkc": "spark", "sparkw": "spark"}.get(kind, kind)
        use = '<use href="#slp-%s"/>' % art
        shapes = ('<g class="sw">%s</g><g fill="%s" stroke="%s" stroke-width="%s" '
                  'stroke-linejoin="round">%s</g>'
                  % (use, fill, acc or "none", "4" if acc else "0", use))
        if kind == "rocket":   # a porthole, or it is just a shape
            shapes += '<circle cx="50" cy="34" r="9" fill="#2bd9ff" stroke="#5b00d6" stroke-width="4"/>'
            shapes += '<path d="M40 62L50 92L60 62Z" fill="#ff8a00"/>'
        text = ('<b style="font-size:%dpx;color:%s">%s</b>' % (round(size * lsz), lcol, label)
                if label else "")
        return ('<div class="stk%s" data-x="%d" data-y="%d" data-r="%d" '
                'style="left:%dpx;top:%dpx;width:%dpx;height:%dpx">'
                '<svg viewBox="0 0 100 100">%s</svg>%s</div>'
                % (" x" if extra else "", x, y, rot, x, y, size, size, shapes, text))

    def slide(self, sid, w, h=None, extra=(), cls="", style=""):
        """`w` display width; `h` defaults to 3:4. Returns the wrapper div,
        absolutely positioned at 0,0 of its parent unless `style` says else."""
        h = h or round(w * NATIVE_H / NATIVE_W)
        s = w / float(NATIVE_W)
        dy = (h / s - NATIVE_H) / 2.0          # a 4:5 crop trims top and bottom
        dots = "".join(
            '<i class="sl-dot" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx;background:%s"></i>'
            % (x, y, d, d, c) for x, y, d, c in [
                (70, 380, 26, "#fff22b"), (1000, 360, 20, "#2bf0ff"), (320, 1120, 22, "#ffffff"),
                (760, 1110, 30, "#fff22b"), (60, 930, 18, "#ff2bd6"), (1010, 930, 24, "#ffffff"),
                (520, 70, 18, "#fff22b"), (420, 1400, 16, "#2bf0ff")])
        art = u"".join([
            dots,
            u'<div class="sl-pill">СЕКРЕТНИЙ ЛАЙФХАК</div>',
            u'<div class="sl-t" style="top:250px;font-size:190px">10 ПОРАД</div>',
            u'<div class="sl-t" style="top:470px;font-size:118px">ДЛЯ ІДЕАЛЬНИХ</div>',
            u'<div class="sl-t" style="top:620px;font-size:176px">КАРУСЕЛЕЙ</div>',
            u'<div class="sl-sub" style="top:880px">Твій блоог виросте в 1О разіів!!!</div>',
            u'<div class="sl-sub" style="top:960px;font-size:44px;color:#fff22b">'
            u'продажі ЗРОСТУУТЬ гарантованно</div>',
            u'<div class="sl-btn">ДІЗНАТИСЯ БІЛЬШЕЕ &#8594;</div>',
            "".join(self.sticker(*b) for b in BASE),
            "".join(self.sticker(*e, extra=True) for e in extra),
        ])
        # data-layout-ignore: set dressing, not copy — its low contrast is the
        # point, and the stickers overflow on purpose (hyperframes check).
        return ('<div class="slop%s" id="%s" data-layout-ignore style="width:%dpx;height:%dpx;%s">'
                '<div class="sl-art" style="height:%dpx;transform:scale(%.5f)">'
                '<div class="sl-sun"></div><div class="sl-in" style="top:%dpx">%s</div></div></div>'
                % ((" " + cls) if cls else "", sid, w, h, style, round(h / s), s, round(dy), art))
