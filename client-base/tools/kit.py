# -*- coding: utf-8 -*-
"""Shared machinery for a client's reels (Ruta's kit.py, client-agnostic).

BASE LAYER. The client's look (tokens, materials, caption style) is imported
from tools/look.py; nothing in this file names a client.

This is deliberately a kit of **materials, not beats**. Reusing a whole beat is
what would make every reel look like the last one; reusing the surface recipe,
the glass, the bar rhythm and the caption machinery is what stops me rebuilding
them from scratch each time and getting them subtly wrong.

Everything here implements LOOK.md §5a. What a beat *depicts* stays invented
per reel, per script.

    from kit import Kit
    k = Kit(width=1080, height=1920, fps=30, duration=67.4)
    k.squircle(".tile.big", 360, 360, 88)
    html = k.document(beats_html, beats_js, captions)
"""
import io
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from squircle import path as sq  # noqa: E402


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# --- the look lives in tools/look.py (the client's design layer) ------------
#     TOKENS (css custom properties), SURFACES (the client's materials),
#     CAPTION_CSS (how a caption looks) and LOOK (sizes, positions, caption
#     mode). Everything in this file is the base: the same for every client.
from look import TOKENS, SURFACES, CAPTION_CSS, LOOK  # noqa: E402


class Kit(object):
    def __init__(self, width=1080, height=1920, fps=30, duration=60.0,
                 cap_y=None, cap_size=None, gfx_top=None, gfx_bot=None):
        self.w, self.h, self.fps, self.dur = width, height, fps, duration
        self.cap_y = LOOK["cap_y"] if cap_y is None else cap_y
        self.cap_size = LOOK["cap_size"] if cap_size is None else cap_size
        self.gfx_top = LOOK["gfx_top"] if gfx_top is None else gfx_top
        self.gfx_bot = LOOK["gfx_bot"] if gfx_bot is None else gfx_bot
        self.cap_mode = LOOK.get("caption_mode", "phrase")
        self._sq = []
        self._css = []
        self._mattes = []

    # -- §5a.1 continuous-curvature corners ---------------------------------
    def squircle(self, selector, w, h, r, s=0.6):
        """clip-path for one surface. drop-shadow survives the clip; box-shadow
        would not, which is why .card/.tile cast with filter."""
        self._sq.append("    %s { clip-path: path('%s'); }" % (selector, sq(w, h, r, s)))

    def css(self, block):
        self._css.append(block)

    # -- masking -------------------------------------------------------------
    def matte(self, name, start, dur):
        """Put her back on top for one beat, so the graphic under her reads as
        being *behind* her instead of stuck to her head.

        `tools/matte.py` makes the clip. It is the same pixels as the plate,
        cut out of its background, played at the same composition time — so it
        lands exactly over itself and only the removed background lets the
        graphic through. Mattes are collected here and emitted above every
        graphic but below the scrim, which is what makes one call enough.

        Per-beat only, and only when something big goes behind her: see
        RULES.md §1 for the arithmetic that makes a whole reel a bad idea.
        """
        self._mattes.append(
            '      <video id="matte-%s" class="plate matte" '
            'src="assets/mattes/%s.webm"\n'
            '             data-start="%.3f" data-duration="%.3f" '
            'data-media-start="0"\n'
            '             muted playsinline></video>' % (name, name, start, dur))

    # -- motion (RULES.md §4.1) -----------------------------------------------
    # The refs cut graphics on and off. When something animates, it is short
    # and mechanical: no bounce, no overshoot, no spring, nothing moving while
    # it is held. These are the only motions; each returns one line of GSAP.
    @staticmethod
    def on(sel, t):
        """Cut on at t (hidden before t, from the first frame)."""
        return ('tl.fromTo("%s", {autoAlpha: 0}, {autoAlpha: 1, duration: 0.001, '
                'immediateRender: true}, %.3f);' % (sel, t))

    @staticmethod
    def off(sel, t):
        """Cut off at t."""
        return 'tl.set("%s", {autoAlpha: 0}, %.3f);' % (sel, t)

    @staticmethod
    def type_on(sel, t, chars, cps=24):
        """Type-on, left to right, one step per character (15-35 chars/s)."""
        n = max(1, int(chars))
        return ('tl.fromTo("%s", {autoAlpha: 1, clipPath: "inset(0%% 100%% 0%% 0%%)"}, '
                '{clipPath: "inset(0%% 0%% 0%% 0%%)", duration: %.3f, ease: "steps(%d)", '
                'immediateRender: true}, %.3f);' % (sel, n / float(cps), n, t))

    @staticmethod
    def count_up(sel, t, end, frm=0, dur=0.6, fmt="{}"):
        """A number counting up, landing on `end` at t + dur (put t + dur on
        the moment she finishes saying the number). `fmt` wraps the figure."""
        pre, post = fmt.split("{}")
        return ('(function(){var o={v:%s};tl.to(o,{v:%s,duration:%.3f,ease:"none",'
                'onUpdate:function(){document.querySelector("%s").textContent="%s"+'
                'Math.round(o.v).toLocaleString("uk-UA")+"%s";}},%.3f);})();'
                % (frm, end, dur, sel, pre, post, t))

    @staticmethod
    def slide_in(sel, t, dx=0, dy=60, frames=4, fps=30):
        """Slide in from its own edge in 3-4 frames, ease-out, no overshoot."""
        return ('tl.fromTo("%s", {x: %d, y: %d, autoAlpha: 0}, {x: 0, y: 0, autoAlpha: 1, '
                'duration: %.3f, ease: "power2.out", immediateRender: true}, %.3f);'
                % (sel, dx, dy, frames / float(fps), t))

    @staticmethod
    def fade_in(sel, t, frames=4, fps=30):
        """Fade in over 3-5 frames: photos and GIFs only."""
        return ('tl.fromTo("%s", {autoAlpha: 0}, {autoAlpha: 1, duration: %.3f, '
                'ease: "none", immediateRender: true}, %.3f);' % (sel, frames / float(fps), t))

    # -- emoji ---------------------------------------------------------------
    @staticmethod
    def emoji(name, cls="", eid=""):
        """An emoji as an <img>, because a text glyph renders in the render
        machine's emoji font and not in Apple's. `name` is the file stem under
        assets/emoji (see the README there for the naming). A missing file is a
        hard failure in `hyperframes check`, which is the point: it cannot
        silently fall back to the wrong artwork."""
        return '<img class="emoji%s"%s src="assets/emoji/%s.png" alt="">' % (
            (" " + cls) if cls else "", (' id="%s"' % eid) if eid else "", name)

    # -- captions ------------------------------------------------------------
    @staticmethod
    def load_captions(path):
        return json.load(io.open(path, encoding="utf-8"))["words"]

    @staticmethod
    def phrases(words, max_chars=None, gap_break=None, lower=None):
        """Phrase blocks: a phrase up to its comma, one or two short lines.
        Sizes come from LOOK (the client's refs). Returns caption items in the
        same {"w","s","e"} shape the rest of the kit takes, so blackout /
        invert / scrim work unchanged; each item also keeps its "words" (with
        their own times) for the typing caption mode."""
        max_chars = LOOK.get("max_chars", 34) if max_chars is None else max_chars
        gap_break = LOOK.get("gap_break", 0.30) if gap_break is None else gap_break
        lower = LOOK.get("lowercase", True) if lower is None else lower
        out, cur = [], []

        def flush():
            if cur:
                ws = [dict(x) for x in cur]
                if lower:
                    for x in ws:
                        x["w"] = x["w"].lower()
                if ws:
                    ws[-1]["w"] = re.sub(r"[.…]+$", "", ws[-1]["w"]).strip()
                t = " ".join(x["w"] for x in ws).strip()
                out.append({"w": t, "s": cur[0]["s"], "e": cur[-1]["e"],
                            "words": ws})
            del cur[:]

        for w in words:
            if cur:
                txt = " ".join(x["w"] for x in cur + [w])
                if len(txt) > max_chars or w["s"] - cur[-1]["e"] > gap_break:
                    flush()
            cur.append(w)
            if re.search(r"[.,!?:;—–]$", w["w"]):
                flush()
        flush()
        # a block holds until the next starts, so the line never flickers
        # empty between phrases (§2b: clamp end = next.start - 0.085 kept)
        for x, y in zip(out, out[1:]):
            x["e"] = max(x["s"] + 0.2, y["s"] - 0.085)
        return out

    def captions(self, words):
        """What goes on screen, in the client's caption mode (LOOK):
        "phrase" = a phrase block at a time; "type" = a phrase block that
        types itself on letter by letter in time with her speech, with a
        cursor; "word" = one word at a time (Ruta's own reels)."""
        if self.cap_mode == "word":
            return [dict(w) for w in words]
        return self.phrases(words)

    def _type_spans(self, c):
        """Letters of one caption as spans, each with the time it appears:
        a word's letters spread over the first part of that word."""
        spans, t_of = [], []
        ws = c.get("words") or [{"w": c["w"], "s": c["s"], "e": c["e"]}]
        for wi, w in enumerate(ws):
            txt = w["w"] + ("" if wi == len(ws) - 1 else " ")
            dur = max(0.05, min(w["e"] - w["s"], LOOK.get("type_max", 0.35)))
            n = max(1, len(txt))
            for i, ch in enumerate(txt):
                spans.append(esc(ch) if ch != " " else " ")
                t_of.append(w["s"] + dur * i / n)
        return spans, t_of

    def caption_html(self, caps, blackout=(), invert=()):
        """`invert` spans set the caption in ink instead of white. A light
        takeover (a white skeleton page, a blushed deck) leaves white type
        invisible; §2b keeps the captions running wherever the graphic is not
        already saying the same word, so they have to survive a light ground.
        A caption belongs to exactly one moment, so the decision is made here
        at generation time rather than tweened at runtime."""
        out = []
        for i, c in enumerate(caps):
            if any(a <= c["s"] < b for a, b, _ in blackout):
                continue
            inv = " inv" if any(a <= c["s"] < b for a, b, _ in invert) else ""
            if self.cap_mode == "type":
                spans, _ = self._type_spans(c)
                body = "".join('<span class="ch" id="c%d_%d">%s</span>' % (i, j, ch)
                               for j, ch in enumerate(spans))
                body += '<span class="cur"></span>'
            else:
                body = esc(c["w"])
            out.append('<div class="cap%s" id="cap%d">%s</div>' % (inv, i, body))
        return "\n      ".join(out)

    def caption_js(self, caps, blackout=(), scrim_off=(), invert=()):
        """Instant on, instant off — a fade smears two words together at this
        rate. The scrim rides the spoken stretch and stands down for any
        takeover, where it would show through the pane as a halo."""
        lines = []
        for i, c in enumerate(caps):
            if any(a <= c["s"] < b for a, b, _ in blackout):
                continue
            lines.append('  tl.set("#cap%d", {autoAlpha: 1}, %.3f);' % (i, c["s"]))
            if self.cap_mode == "type":
                _, t_of = self._type_spans(c)
                for j, t in enumerate(t_of):
                    lines.append('  tl.set("#c%d_%d", {display: "inline"}, %.3f);' % (i, j, t))
            lines.append('  tl.set("#cap%d", {autoAlpha: 0}, %.3f);' % (i, c["e"]))
        lines.append('  tl.to("#scrim", {autoAlpha: 1, duration: 0.5}, %.3f);'
                     % max(0.0, caps[0]["s"] - 0.3))
        lines.append('  tl.to("#scrim", {autoAlpha: 0, duration: 0.6}, %.3f);'
                     % (caps[-1]["e"] + 0.1))
        # An inverted span is over a light takeover, where the dark underlay
        # reads as a grey smear behind ink type. Same treatment as a blackout.
        #
        # These are merged into a union first. One off/on pair per span looks
        # right and is not: a blackout nested inside an invert span restores
        # the scrim at its own end, and the underlay comes back for the rest
        # of the takeover. Reel 9 had exactly that — the 51.10-52.15 blackout
        # switched the scrim on over a white page until 58.70, which rendered
        # as a grey cloud behind ink captions.
        _spans = sorted([a, b] for a, b, _ in
                        list(blackout) + list(scrim_off) + list(invert))
        _off = []
        for a, b in _spans:
            if _off and a <= _off[-1][1] + 0.001:
                _off[-1][1] = max(_off[-1][1], b)
            else:
                _off.append([a, b])
        for a, b in _off:
            lines.append('  tl.to("#scrim", {autoAlpha: 0, duration: 0.20}, %.3f);'
                         % max(0.0, a - 0.20))
            lines.append('  tl.to("#scrim", {autoAlpha: 1, duration: 0.25}, %.3f);' % b)
        return "\n".join(lines)

    # -- assembly ------------------------------------------------------------
    def base_css(self):
        return """
    @import url("assets/fonts/fonts.css");
    * { margin: 0; padding: 0; box-sizing: border-box; }
    #root { position: relative; width: %(w)dpx; height: %(h)dpx;
            overflow: hidden; background: #000;
            font-family: var(--sans);%(tokens)s }
    .plate { position: absolute; inset: 0; width: %(w)dpx; height: %(h)dpx;
             object-fit: cover; }
%(capcss)s
    /* typing caption mode: letters start hidden, the timeline shows them */
    .cap .ch { display: none; white-space: pre; }
    .g { position: absolute; left: 0; top: %(gfxTop)dpx; width: %(w)dpx;
         height: %(gfxH)dpx; opacity: 0; visibility: hidden; }
    .g.full { top: 0; height: %(h)dpx; }
%(surfaces)s""" % {
            "w": self.w, "h": self.h, "tokens": TOKENS,
            "capBottom": self.h - (self.cap_y + self.cap_size // 2), "capSize": self.cap_size,
            "gfxTop": self.gfx_top, "gfxH": self.gfx_bot - self.gfx_top,
            "surfaces": SURFACES,
            "capcss": CAPTION_CSS % {
                "w": self.w, "capSize": self.cap_size,
                "capTop": self.cap_y - self.cap_size // 2,
                # bottom-anchored: one line sits at cap_y, two lines grow upward
                "capBottom": self.h - (self.cap_y + self.cap_size // 2)},
        }

    def document(self, title, plate, gfx_html, gfx_js, caps,
                 blackout=(), scrim_off=(), invert=()):
        css = self.base_css() + "\n".join(self._css) + "\n" + "\n".join(self._sq)
        return '''<!DOCTYPE html>
<html lang="%(lang)s">
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
%(mattes)s
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
       "gfx": gfx_html, "mattes": "\n".join(self._mattes),
       "caps": self.caption_html(caps, blackout, invert),
       "capjs": self.caption_js(caps, blackout, scrim_off, invert),
       "gfxjs": gfx_js, "lang": LOOK.get("lang", "uk")}
