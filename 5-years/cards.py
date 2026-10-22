# -*- coding: utf-8 -*-
"""Doodle cards for the 5-years series: the question stickers that sit above
their heads, and the end card. Each card is a full 1080x1920 transparent PNG,
drawn as HTML/SVG and screenshotted by headless Chromium, so ffmpeg only has
to lay it over the footage.

The look: a hand-drawn paper sticker, slightly tilted, wobbly ink outline,
Ukrainian in Caveat Bold, English smaller underneath. Static: it appears and
disappears, nothing moves.
"""
import html, os, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS = os.path.join(ROOT, "assets", "fonts")
CHROME = "/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell"

INK, PAPER, SOFT = "#1f1b16", "#fffdf6", "#5d574f"

PAGE = """<!doctype html><html><head><meta charset="utf-8"><style>
@font-face {{ font-family: Doodle; font-weight: 400; src: url("file://{fonts}/Caveat-Regular.ttf"); }}
@font-face {{ font-family: Doodle; font-weight: 700; src: url("file://{fonts}/Caveat-Bold.ttf"); }}
html, body {{ margin: 0; width: 1080px; height: 1920px; background: transparent; overflow: hidden; }}
.wrap {{ position: absolute; left: 0; right: 0; top: {top}px; display: flex; justify-content: center; }}
.card {{ position: relative; max-width: 880px; padding: 34px 54px 38px; transform: rotate({tilt}deg);
        text-align: center; font-family: Doodle, cursive; color: {ink}; }}
.card svg.edge {{ position: absolute; inset: 0; width: 100%; height: 100%; overflow: visible; }}
.uk {{ position: relative; font-weight: 700; font-size: {uk}px; line-height: 1.02; }}
.en {{ position: relative; font-weight: 400; font-size: {en}px; line-height: 1.1; color: {soft}; margin-top: 10px; }}
.squig {{ position: relative; display: block; margin: 4px auto 0; }}
</style></head><body>
<svg width="0" height="0" style="position:absolute">
  <filter id="wob" x="-5%" y="-5%" width="110%" height="110%">
    <feTurbulence type="fractalNoise" baseFrequency="0.022" numOctaves="2" seed="{seed}"/>
    <feDisplacementMap in="SourceGraphic" scale="7"/>
  </filter>
</svg>
<div class="wrap"><div class="card">
  <svg class="edge" preserveAspectRatio="none">
    <rect x="9" y="11" width="100%" height="100%" rx="30" fill="{ink}" fill-opacity="0.16" filter="url(#wob)"/>
    <rect x="0" y="0" width="100%" height="100%" rx="30" fill="{paper}" filter="url(#wob)"/>
    <rect x="0" y="0" width="100%" height="100%" rx="30" fill="none" stroke="{ink}" stroke-width="5" filter="url(#wob)"/>
    <rect x="5" y="-3" width="100%" height="100%" rx="32" fill="none" stroke="{ink}" stroke-width="2" stroke-opacity="0.55" filter="url(#wob)"/>
  </svg>
  <div class="uk">{uk_text}</div>
  <svg class="squig" width="{sq_w}" height="22" viewBox="0 0 {sq_w} 22">
    <path d="{sq_path}" fill="none" stroke="{ink}" stroke-width="4" stroke-linecap="round" filter="url(#wob)"/>
  </svg>
  {en_html}
</div></div>
</body></html>"""


def _squiggle(width):
    pts, x, up = [], 6, True
    while x < width - 6:
        pts.append(f"{x},{5 if up else 17}")
        x += 26
        up = not up
    return "M" + " L".join(pts)


def render(path_png, uk, en="", top=150, tilt=-2.0, uk_px=86, en_px=46, seed=3):
    """Write the card's HTML next to the PNG and screenshot it transparent."""
    sq_w = 260
    page = PAGE.format(
        fonts=FONTS, top=top, tilt=tilt, ink=INK, paper=PAPER, soft=SOFT,
        uk=uk_px, en=en_px, seed=seed, uk_text=html.escape(uk).replace("\n", "<br>"),
        sq_w=sq_w, sq_path=_squiggle(sq_w),
        en_html=f'<div class="en">{html.escape(en)}</div>' if en else "")
    return _shoot(path_png, page)


TAB = """<!doctype html><html><head><meta charset="utf-8"><style>
@font-face {{ font-family: Doodle; font-weight: 700; src: url("file://{fonts}/Caveat-Bold.ttf"); }}
html, body {{ margin: 0; width: 1080px; height: 1920px; background: transparent; overflow: hidden; }}
.tab {{ position: absolute; left: {cx}px; top: {top}px; transform: translateX(-50%) rotate({tilt}deg);
       padding: 10px 34px 14px; font-family: Doodle, cursive; font-weight: 700; font-size: {px}px;
       line-height: 1; color: {ink}; white-space: nowrap; }}
.tab svg {{ position: absolute; inset: 0; width: 100%; height: 100%; overflow: visible; }}
.tab span {{ position: relative; }}
</style></head><body>
<svg width="0" height="0" style="position:absolute">
  <filter id="wob" x="-10%" y="-10%" width="120%" height="140%">
    <feTurbulence type="fractalNoise" baseFrequency="0.03" numOctaves="2" seed="{seed}"/>
    <feDisplacementMap in="SourceGraphic" scale="6"/>
  </filter>
</svg>
<div class="tab">
  <svg preserveAspectRatio="none">
    <rect x="6" y="8" width="100%" height="100%" rx="22" fill="{ink}" fill-opacity="0.16" filter="url(#wob)"/>
    <rect x="0" y="0" width="100%" height="100%" rx="22" fill="{paper}" filter="url(#wob)"/>
    <rect x="0" y="0" width="100%" height="100%" rx="22" fill="none" stroke="{ink}" stroke-width="4.5" filter="url(#wob)"/>
  </svg>
  <span>{text}</span>
</div>
<svg style="position:absolute; left:{ax}px; top:{ay}px; overflow:visible" width="40" height="70">
  <g filter="url(#wob)" fill="none" stroke-linecap="round" stroke-linejoin="round">
    <path d="M20 4 C 16 24, 24 40, 19 60 M 9 47 L 19 62 L 30 46" stroke="{paper}" stroke-width="13"/>
    <path d="M20 4 C 16 24, 24 40, 19 60 M 9 47 L 19 62 L 30 46" stroke="{ink}" stroke-width="5"/>
  </g>
</svg>
</body></html>"""


def tab(path_png, text, cx, top, px=70, tilt=-3.0, seed=11):
    """A name tab over one person's head, with a doodled arrow down to them."""
    page = TAB.format(fonts=FONTS, cx=cx, top=top, tilt=tilt, px=px, ink=INK, paper=PAPER,
                      seed=seed, text=html.escape(text), ax=cx - 20, ay=top + px + 30)
    return _shoot(path_png, page)


def _shoot(path_png, page):
    path_png = os.path.abspath(path_png)
    path_html = path_png[:-4] + ".html"
    with open(path_html, "w", encoding="utf-8") as f:
        f.write(page)
    subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
                    "--force-device-scale-factor=1", "--window-size=1080,1920",
                    "--default-background-color=00000000", "--virtual-time-budget=3000",
                    f"--screenshot={path_png}", "file://" + path_html],
                   check=True, capture_output=True)
    return path_png
