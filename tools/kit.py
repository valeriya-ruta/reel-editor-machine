# -*- coding: utf-8 -*-
"""Shared materials for Ruta's reels.

This is deliberately a kit of **materials, not beats**. Reusing a whole beat is
what would make every reel look like the last one; reusing the surface recipe,
the glass, the bar rhythm and the caption machinery is what stops me rebuilding
them from scratch each time and getting them subtly wrong.

Everything here implements STYLE.md §5a. What a beat *depicts* stays invented
per reel, per script.

    from kit import Kit
    k = Kit(width=1080, height=1920, fps=30, duration=67.4)
    k.squircle(".tile.big", 360, 360, 88)
    html = k.document(beats_html, beats_js, captions)
"""
import io
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from squircle import path as sq  # noqa: E402


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# --- §5a.4 the tonal ladder, §5a.5 never a flat fill, §5a.6 edge light,
#     §5a.7 ambient shadow ----------------------------------------------------
TOKENS = """
      --surface:        #fdf6f6;
      --container:      #f4dde2;
      --container-high: #ecc8d0;
      --graphite:       rgba(23,20,28,0.13);
      --accent:         #b4122f;
      --accent-deep:    #8d0d24;
      --pink:           #ff6e9c;
      --ink:            #17141c;

      --lit:        linear-gradient(115deg, #ffffff 0%, #fafafb 100%);
      --lit-blush:  linear-gradient(115deg, #fffdfd 0%, #fdf1f4 100%);
      --lit-accent: linear-gradient(115deg, #c41434 0%, #8d0d24 100%);
      --lit-pink:   linear-gradient(115deg, #ff8ab0 0%, #ff5c8f 100%);
      --lit-ink:    linear-gradient(115deg, #241f2c 0%, #17141c 100%);

      --rim: inset 0 1.5px 0 rgba(255,255,255,0.92),
             inset 0 -1.5px 0 rgba(255,255,255,0.14),
             inset 0 0 0 1px rgba(255,255,255,0.28);
      --rim-dark: inset 0 1.5px 0 rgba(255,255,255,0.16),
                  inset 0 0 0 1px rgba(255,255,255,0.08);
      --rim-glass: inset 0 2px 0 rgba(255,255,255,0.70),
                   inset 0 -2px 0 rgba(255,255,255,0.10),
                   inset 0 0 0 1.5px rgba(255,255,255,0.30);

      --cast: drop-shadow(0 1px 2px rgba(26,30,39,0.10))
              drop-shadow(0 24px 48px rgba(26,30,39,0.14));
      --cast-sm: drop-shadow(0 1px 2px rgba(26,30,39,0.08))
                 drop-shadow(0 12px 24px rgba(26,30,39,0.12));
"""

# --- the recurring materials ------------------------------------------------
SURFACES = """
    /* §5a.9 — glass over her footage is the house look. Panels only; an
       edge-to-edge frosted ground blurs her out of her own reel. */
    .glass { background: rgba(255,255,255,0.15);
             -webkit-backdrop-filter: blur(24px) saturate(1.4);
             backdrop-filter: blur(24px) saturate(1.4);
             box-shadow: var(--rim); filter: var(--cast); }

    /* A takeover: a tinted pane laid ON the footage, with a real margin so it
       reads as an object rather than a blur applied to the video. */
    .ground { position: absolute; left: 44px; top: 64px;
              width: 992px; height: 1792px;
              background: linear-gradient(158deg, rgba(196,20,52,0.62) 0%,
                          rgba(141,13,36,0.70) 100%);
              -webkit-backdrop-filter: blur(30px) saturate(1.5);
              backdrop-filter: blur(30px) saturate(1.5);
              box-shadow: var(--rim-glass); filter: var(--cast); }

    .card { position: absolute; background: var(--lit-blush);
            filter: var(--cast); box-shadow: var(--rim); }
    .card.ink { background: var(--lit-ink); box-shadow: var(--rim-dark); }
    .card.accent { background: var(--lit-accent); box-shadow: var(--rim-dark); }

    .tile { position: absolute; display: grid; place-items: center;
            background: var(--lit-blush); filter: var(--cast);
            box-shadow: var(--rim); }

    /* §5a.3 — bar rhythm. One thick heading, then ragged body. Uniform bars
       read as a loading state; ragged ones read as an abstracted screen. */
    .ph { display: block; height: 66px; border-radius: 18px;
          background: var(--lit-accent); margin-bottom: 26px;
          box-shadow: var(--rim-dark); }
    .pr { display: block; height: 40px; border-radius: 12px;
          background: var(--graphite); margin-bottom: 18px; }
    .pr:nth-of-type(2) { width: 94%; }
    .pr:nth-of-type(3) { width: 71%; }
    .pr:nth-of-type(4) { width: 43%; }

    .phone { position: absolute; background: var(--lit-blush);
             overflow: hidden; filter: var(--cast); box-shadow: var(--rim); }
    .phone video, .phone img { width: 100%; height: 100%; object-fit: cover;
                               display: block; }

    /* a value in its own card — her reference's "big number" pattern, minus
       the label, because a graphic here carries no words */
    .valcard { position: absolute; background: rgba(255,255,255,0.16);
               -webkit-backdrop-filter: blur(16px) saturate(1.3);
               backdrop-filter: blur(16px) saturate(1.3);
               box-shadow: var(--rim-dark);
               display: grid; place-items: center; }
    .valcard span { color: #fff; font-weight: 900; letter-spacing: -0.04em; }

    .wire { fill: none; stroke-width: 20; stroke-linecap: round;
            filter: drop-shadow(0 8px 18px rgba(26,30,39,0.22)); }
    .node { fill: #fdf6f6; stroke: #b4122f; stroke-width: 16;
            filter: drop-shadow(0 10px 22px rgba(26,30,39,0.24)); }
    .node.hub { fill: #b4122f; stroke: #fff; }

    .halo { position: absolute; border-radius: 50%; pointer-events: none;
            background: radial-gradient(circle, rgba(255,110,156,0.5) 0%,
                        rgba(255,110,156,0) 70%); }
    .ring { position: absolute; border-radius: 50%; pointer-events: none;
            border: 18px solid rgba(255,110,156,0.92);
            filter: drop-shadow(0 0 40px rgba(255,110,156,0.55)); }
"""


class Kit(object):
    def __init__(self, width=1080, height=1920, fps=30, duration=60.0,
                 cap_y=1472, cap_size=90, gfx_top=40, gfx_bot=640):
        self.w, self.h, self.fps, self.dur = width, height, fps, duration
        self.cap_y, self.cap_size = cap_y, cap_size
        self.gfx_top, self.gfx_bot = gfx_top, gfx_bot
        self._sq = []
        self._css = []

    # -- §5a.1 continuous-curvature corners ---------------------------------
    def squircle(self, selector, w, h, r, s=0.6):
        """clip-path for one surface. drop-shadow survives the clip; box-shadow
        would not, which is why .card/.tile cast with filter."""
        self._sq.append("    %s { clip-path: path('%s'); }" % (selector, sq(w, h, r, s)))

    def css(self, block):
        self._css.append(block)

    # -- captions ------------------------------------------------------------
    @staticmethod
    def load_captions(path):
        return json.load(io.open(path, encoding="utf-8"))["words"]

    def caption_html(self, caps, blackout=()):
        out = []
        for i, c in enumerate(caps):
            if any(a <= c["s"] < b for a, b, _ in blackout):
                continue
            out.append('<div class="cap" id="cap%d">%s</div>'
                       % (i, esc(c["w"].upper())))
        return "\n      ".join(out)

    def caption_js(self, caps, blackout=(), scrim_off=()):
        """Instant on, instant off — a fade smears two words together at this
        rate. The scrim rides the spoken stretch and stands down for any
        takeover, where it would show through the pane as a halo."""
        lines = []
        for i, c in enumerate(caps):
            if any(a <= c["s"] < b for a, b, _ in blackout):
                continue
            lines.append('  tl.set("#cap%d", {autoAlpha: 1}, %.3f);' % (i, c["s"]))
            lines.append('  tl.set("#cap%d", {autoAlpha: 0}, %.3f);' % (i, c["e"]))
        lines.append('  tl.to("#scrim", {autoAlpha: 1, duration: 0.5}, %.3f);'
                     % max(0.0, caps[0]["s"] - 0.3))
        lines.append('  tl.to("#scrim", {autoAlpha: 0, duration: 0.6}, %.3f);'
                     % (caps[-1]["e"] + 0.1))
        for a, b, _ in list(blackout) + list(scrim_off):
            lines.append('  tl.to("#scrim", {autoAlpha: 0, duration: 0.20}, %.3f);'
                         % max(0.0, a - 0.20))
            lines.append('  tl.to("#scrim", {autoAlpha: 1, duration: 0.25}, %.3f);' % b)
        return "\n".join(lines)

    # -- assembly ------------------------------------------------------------
    def base_css(self):
        return """
    @font-face {
      font-family: "ProductSans";
      src: url("assets/fonts/ProductSans-Black.woff") format("woff");
      font-weight: 900; font-style: normal; font-display: block;
    }
    * { margin: 0; padding: 0; box-sizing: border-box; }
    #root { position: relative; width: %(w)dpx; height: %(h)dpx;
            overflow: hidden; background: #000;
            font-family: "ProductSans", system-ui, sans-serif;%(tokens)s }
    .plate { position: absolute; inset: 0; width: %(w)dpx; height: %(h)dpx;
             object-fit: cover; }
    #scrim { position: absolute; left: 20px; top: %(scrim)dpx;
             width: 1040px; height: 450px;
             background-image: url("assets/underlay.png");
             background-size: 100%% 100%%; background-repeat: no-repeat;
             opacity: 0; visibility: hidden; pointer-events: none; }
    .cap { position: absolute; left: 0; width: %(w)dpx; top: %(capTop)dpx;
           height: %(capH)dpx; line-height: %(capH)dpx; text-align: center;
           color: #fff; font-size: %(capSize)dpx; font-weight: 900;
           letter-spacing: -0.015em; white-space: nowrap;
           opacity: 0; visibility: hidden; }
    .g { position: absolute; left: 0; top: %(gfxTop)dpx; width: %(w)dpx;
         height: %(gfxH)dpx; opacity: 0; visibility: hidden; }
    .g.full { top: 0; height: %(h)dpx; }
%(surfaces)s""" % {
            "w": self.w, "h": self.h, "tokens": TOKENS,
            "scrim": self.cap_y - 225,
            "capTop": self.cap_y - self.cap_size // 2 - 14,
            "capH": self.cap_size + 28, "capSize": self.cap_size,
            "gfxTop": self.gfx_top, "gfxH": self.gfx_bot - self.gfx_top,
            "surfaces": SURFACES,
        }

    def document(self, title, plate, gfx_html, gfx_js, caps,
                 blackout=(), scrim_off=()):
        css = self.base_css() + "\n".join(self._css) + "\n" + "\n".join(self._sq)
        return '''<!DOCTYPE html>
<html lang="uk">
  <head>
    <meta charset="utf-8">
    <title>%(title)s</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
    <style>%(css)s
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0"
         data-width="%(w)d" data-height="%(h)d" data-duration="%(dur).3f" data-fps="%(fps)d">

      <video id="vid" class="plate" src="%(plate)s"
             data-start="0" data-duration="%(dur).3f" data-media-start="0"
             muted playsinline></video>
%(gfx)s

      <div id="scrim"></div>
      %(caps)s

      <audio id="vo" src="%(plate)s"
             data-start="0" data-duration="%(dur).3f" data-media-start="0"></audio>
    </div>

    <script>
      function build() {
        var tl = gsap.timeline({paused: true});

%(capjs)s

%(gfxjs)s

        window.__timelines["main"] = tl;
      }
      if (document.fonts && document.fonts.ready) document.fonts.ready.then(build);
      else build();
    </script>
  </body>
</html>
''' % {"title": esc(title), "css": css, "w": self.w, "h": self.h,
       "dur": self.dur, "fps": self.fps, "plate": plate,
       "gfx": gfx_html, "caps": self.caption_html(caps, blackout),
       "capjs": self.caption_js(caps, blackout, scrim_off), "gfxjs": gfx_js}
