# -*- coding: utf-8 -*-
"""The look from reel 41 on — Google style + Excalidraw sketches (STYLE.md §00).

Her spec of 2026-10-21, built against her approved mock «Reel Layer States».
This replaces tools/glass.py for new reels; kit.py's caption rail is replaced
too, because captions are now boxed phrases with a key word in a pill.

Layers, bottom to top (the z-order is the design):

    #vid      her plate                      pushed down 330 px by half()
    #behind   big words she stands in front of   (needs a matte on top)
    #panel    the half-screen white panel, slides from the top
    .matte    her cut-out, same pixels, same time, same push as #vid
    #front    cards, chips, pills, the CTA, pointer doodles
    #cover    the full-screen white, slides up from the bottom
    #caps     captions — they carry on over everything, cover included

    from gstyle import G
    g = G(dur=DUR, reel="41")
    caps = g.chunks(CAPS, keys={...}, place=[...])
    html = g.document(title, behind, panel, front, cover, js, caps, sfx_cues)
"""
import io
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---- §00.6 colour, Material 3 seeded from #7A1424 ---------------------------
PRIMARY = "#7A1424"
INK = "#1E1E1E"          # sketch ink
ON_SURFACE = "#241919"
ON_SURFACE_VAR = "#574142"
OUTLINE_VAR = "#DEBFBF"
CONTAINER_LOW = "#FFF0F0"
CHIP_FILL = "#FFF8F7"
HACHURE = "#F2C7CA"

# ---- §00.1 no-go zones -------------------------------------------------------
SAFE_TOP, SAFE_BOTTOM = 270, 1536
SAFE_LEFT, SAFE_RIGHT = 90, 900          # right column x 900+ only for y 940-1536
CAP_BOTTOM = 1520                        # caption box bottom edge, default band


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


CSS = """
    @font-face { font-family: "Google Sans"; font-weight: 400; font-display: block;
                 src: url("assets/fonts/GoogleSans-400.ttf") format("truetype"); }
    @font-face { font-family: "Google Sans"; font-weight: 500; font-display: block;
                 src: url("assets/fonts/GoogleSans-500.ttf") format("truetype"); }
    @font-face { font-family: "Google Sans"; font-weight: 700; font-display: block;
                 src: url("assets/fonts/GoogleSans-700.ttf") format("truetype"); }
    @font-face { font-family: "Pangolin"; font-weight: 400; font-display: block;
                 src: url("assets/fonts/Pangolin.ttf") format("truetype"); }
    * { margin: 0; padding: 0; box-sizing: border-box; }
    #root { position: relative; width: 1080px; height: 1920px; overflow: hidden;
            background: #fff; font-family: "Google Sans", system-ui, sans-serif;
            color: %(on)s;
            --primary: %(p)s; --on-surface: %(on)s; --on-surface-var: %(onv)s;
            --outline-var: %(ov)s; --container-low: %(cl)s; --chip: %(chip)s; }
    .plate { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px;
             object-fit: cover; }
    .L { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px;
         pointer-events: none; }
    .hid { opacity: 0; visibility: hidden; }

    /* §00.3.1 above me */
    .card { position: absolute; background: #FFFFFF; border-radius: 40px;
            box-shadow: 0 1px 3px rgba(36,25,25,.10), 0 10px 30px rgba(36,25,25,.10);
            padding: 36px 40px; }
    .card .lbl { display: block; font-weight: 500; font-size: 28px;
                 color: var(--on-surface-var); margin-bottom: 20px; }
    .card .ttl { display: block; font-weight: 700; font-size: 56px; line-height: 1.08;
                 letter-spacing: -0.02em; color: var(--on-surface); }
    .chips { display: flex; flex-wrap: wrap; gap: 14px; }
    .chip { display: inline-flex; align-items: center; gap: 12px;
            border: 2px solid var(--outline-var); border-radius: 16px;
            padding: 14px 24px; font-weight: 500; font-size: 36px;
            color: var(--on-surface); background: var(--chip); }
    .chip i { width: 16px; height: 16px; border-radius: 50%%; background: var(--primary);
              display: inline-block; flex: none; }
    .chip.on { background: var(--primary); border-color: var(--primary); color: #fff; }
    .chip.on i { background: #fff; }
    .pill { position: absolute; display: inline-flex; align-items: center; gap: 16px;
            background: var(--primary); color: #fff; border-radius: 999px;
            padding: 30px 54px; font-weight: 500; font-size: 46px; white-space: nowrap;
            box-shadow: 0 1px 3px rgba(36,25,25,.12), 0 10px 30px rgba(122,20,36,.22); }
    .pill.light { background: #fff; color: var(--on-surface);
                  box-shadow: 0 1px 3px rgba(36,25,25,.10), 0 10px 30px rgba(36,25,25,.10); }
    .num { font-weight: 700; letter-spacing: -0.04em; color: var(--primary); line-height: 1; }
    .row { display: flex; align-items: center; gap: 18px; }
    .check { width: 44px; height: 44px; border-radius: 12px; flex: none;
             border: 3px solid var(--outline-var); background: #fff; position: relative; }
    .check.on { background: var(--primary); border-color: var(--primary); }
    .check.on::after { content: ""; position: absolute; left: 13px; top: 5px; width: 11px;
                       height: 22px; border: solid #fff; border-width: 0 5px 5px 0;
                       transform: rotate(45deg); }
    .line { display: block; height: 18px; border-radius: 9px; background: #EFE3E3; }
    .logo { width: 64px; height: 64px; flex: none; }
    .logo path { fill: var(--primary); }
    .mark { display: block; }
    .mark path { fill: currentColor; }

    /* §00.3.2 behind me */
    .big { position: absolute; left: 0; width: 1080px; text-align: center;
           font-weight: 700; line-height: 0.9; letter-spacing: -0.04em;
           color: var(--primary); white-space: nowrap; }

    /* §00.3.3 half screen. Its parked position (up, off frame) is set from JS
       with gsap.set: a CSS translate here would be parsed by GSAP as a px offset
       and then stacked under yPercent, and the panel stalls a quarter of the
       way in (reel 41's first snapshot). Same for #cover. */
    #panel { position: absolute; left: 0; top: 0; width: 1080px; height: 1240px;
             background: #FFFFFF; }
    /* §00.3.4 full screen */
    #cover { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px;
             background: #FFFFFF; }

    /* §00.5 sketches */
    .sk { position: absolute; left: 0; top: 0; overflow: visible; }
    .sk text, .hand { font-family: "Pangolin", cursive; fill: %(ink)s; color: %(ink)s; }
    .hand { position: absolute; white-space: nowrap; }

    /* §00.2 captions */
    #caps { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px;
            pointer-events: none; }
    .cap { position: absolute; left: 0; width: 1080px; display: flex;
           justify-content: center; opacity: 0; visibility: hidden; }
    .cap .box { display: inline-block; max-width: 720px; text-align: center;
                background: rgba(255,255,255,.94); border-radius: 28px; padding: 16px 30px;
                font-weight: 500; font-size: 54px; line-height: 1.25; letter-spacing: -0.01em;
                color: %(on)s; box-shadow: 0 2px 10px rgba(36,25,25,.10);
                text-wrap: balance; }
    .cap .k { position: relative; display: inline-block; padding: 0 .32em; }
    .cap .kb { position: absolute; inset: 0; border-radius: 999px; background: %(p)s;
               opacity: 0; }
    .cap .kt { position: relative; }
""" % {"p": PRIMARY, "on": ON_SURFACE, "onv": ON_SURFACE_VAR, "ov": OUTLINE_VAR,
       "cl": CONTAINER_LOW, "chip": CHIP_FILL, "ink": INK}


# Runs inside build(), after `var tl`. Motion is §00.7 exactly: the three
# cubic-beziers are solved here rather than approximated with GSAP's back/expo.
JS = r"""
  function bez(x1, y1, x2, y2) {
    function a(p1, p2) { return 1 - 3 * p2 + 3 * p1; }
    function b(p1, p2) { return 3 * p2 - 6 * p1; }
    function c(p1) { return 3 * p1; }
    function at(t, p1, p2) { return ((a(p1, p2) * t + b(p1, p2)) * t + c(p1)) * t; }
    function slope(t, p1, p2) { return 3 * a(p1, p2) * t * t + 2 * b(p1, p2) * t + c(p1); }
    return function (x) {
      if (x <= 0) return 0; if (x >= 1) return 1;
      var t = x;
      for (var i = 0; i < 8; i++) {
        var s = slope(t, x1, x2); if (Math.abs(s) < 1e-6) break;
        t -= (at(t, x1, x2) - x) / s;
      }
      t = Math.min(1, Math.max(0, t));
      return at(t, y1, y2);
    };
  }
  var POP = bez(.34, 1.56, .64, 1), RISE = bez(.2, .9, .25, 1), SLIDE = bez(.65, 0, .25, 1);
  var PUSH = "#vid, .matte";
  gsap.set("#panel", {yPercent: -101}); gsap.set("#cover", {yPercent: 101});
  var NO = {immediateRender: false};
  function X(o) { for (var k in NO) o[k] = NO[k]; return o; }

  // arrivals (§00.7): pops 0.5-0.6 s, rise-ins 0.7 s; exits quicker, easing in
  function pop(sel, t, d) {
    tl.fromTo(sel, {autoAlpha: 0, scale: .6}, X({autoAlpha: 1, scale: 1, duration: d || .55, ease: POP}), t);
  }
  function rise(sel, t, dy) {
    tl.fromTo(sel, {autoAlpha: 0, y: dy || 60}, X({autoAlpha: 1, y: 0, duration: .7, ease: RISE}), t);
  }
  function fadein(sel, t, d) { tl.fromTo(sel, {autoAlpha: 0}, X({autoAlpha: 1, duration: d || .4}), t); }
  function out(sel, t) { tl.to(sel, {autoAlpha: 0, scale: .9, duration: .3, ease: "power2.in"}, t); }
  function sink(sel, t) { tl.to(sel, {autoAlpha: 0, y: 40, duration: .35, ease: "power2.in"}, t); }

  // §00.3.3 half screen: the panel comes down as the video goes down
  function half(t0, t1) {
    tl.fromTo("#panel", {yPercent: -101}, X({yPercent: 0, duration: .85, ease: SLIDE}), t0);
    tl.fromTo(PUSH, {y: 0}, X({y: 330, duration: .85, ease: SLIDE}), t0);
    tl.to("#panel", {yPercent: -101, duration: .85, ease: SLIDE}, t1);
    tl.to(PUSH, {y: 0, duration: .85, ease: SLIDE}, t1);
  }
  // §00.3.4 full screen: white up from the bottom over everything
  function full(t0, t1) {
    tl.fromTo("#cover", {yPercent: 101}, X({yPercent: 0, duration: .85, ease: SLIDE}), t0);
    tl.to("#cover", {yPercent: 101, duration: .85, ease: SLIDE}, t1);
  }

  // ---- §00.5 Excalidraw sketches (rough.js), drawn on stroke by stroke ----
  var SKO = {roughness: 2.4, bowing: 2.5, strokeWidth: 4.5, stroke: "#1E1E1E",
             disableMultiStroke: false, preserveVertices: false};
  var HACH = {fill: "#F2C7CA", fillStyle: "hachure", hachureGap: 16, hachureAngle: -41,
              fillWeight: 2.5};
  function opt(o, seed) { var r = {}; for (var k in SKO) r[k] = SKO[k];
    for (var k2 in (o || {})) r[k2] = o[k2]; r.seed = seed; return r; }
  function hatch(o) { var r = {}; for (var k in HACH) r[k] = HACH[k];
    for (var k2 in (o || {})) r[k2] = o[k2]; return r; }
  function rrectD(x, y, w, h, r) {
    return "M" + (x + r) + " " + y + " H" + (x + w - r) + " A" + r + " " + r + " 0 0 1 " + (x + w) + " " + (y + r) +
           " V" + (y + h - r) + " A" + r + " " + r + " 0 0 1 " + (x + w - r) + " " + (y + h) +
           " H" + (x + r) + " A" + r + " " + r + " 0 0 1 " + x + " " + (y + h - r) +
           " V" + (y + r) + " A" + r + " " + r + " 0 0 1 " + (x + r) + " " + y + " Z";
  }
  var SK = {};
  // a sketch is a named group of rough shapes inside one <svg class="sk">
  function sketch(name, svgId) {
    var svg = document.getElementById(svgId);
    var g = document.createElementNS("http://www.w3.org/2000/svg", "g");
    g.setAttribute("id", "sk-" + name); svg.appendChild(g);
    SK[name] = {g: g, rc: rough.svg(svg), shapes: []};
    return SK[name];
  }
  function _add(s, node, kind) {
    s.g.appendChild(node);
    var paths = [].slice.call(node.querySelectorAll ? node.querySelectorAll("path") : []);
    if (node.tagName === "path") paths = [node];
    paths.forEach(function (p) {
      var L = 0; try { L = p.getTotalLength(); } catch (e) {}
      p.style.strokeDasharray = L + " " + (L + 2); p.style.strokeDashoffset = L + 1;
      p.style.strokeLinecap = "round"; p.style.strokeLinejoin = "round";
    });
    s.shapes.push({paths: paths, kind: kind || "stroke"});
  }
  function box(name, x, y, w, h, o) {      // rounded rough box, radius 28 (§00.5.2)
    var s = SK[name], r = (o && o.r) || 28;
    var oo = opt(o, (o && o.seed) || 7);
    if (o && o.fill) { var f = hatch(o.fill === true ? {} : {fill: o.fill}); for (var k in f) oo[k] = f[k]; }
    _add(s, s.rc.path(rrectD(x, y, w, h, r), oo));
  }
  function ell(name, cx, cy, w, h, o) { var s = SK[name];
    _add(s, s.rc.ellipse(cx, cy, w, h, opt(o, (o && o.seed) || 11))); }
  function ln(name, x1, y1, x2, y2, o) { var s = SK[name];
    _add(s, s.rc.line(x1, y1, x2, y2, opt(o, (o && o.seed) || 13))); }
  function under(name, x1, y, x2, o) { var s = SK[name];      // a hand underline
    _add(s, s.rc.curve([[x1, y + 4], [(x1 + x2) / 2, y - 6], [x2, y + 2]], opt(o, (o && o.seed) || 17))); }
  function arrow(name, x1, y1, x2, y2, o) {
    var s = SK[name], oo = opt(o, (o && o.seed) || 19), bend = (o && o.bend != null) ? o.bend : .12;
    var mx = (x1 + x2) / 2 + (y2 - y1) * bend, my = (y1 + y2) / 2 - (x2 - x1) * bend;
    _add(s, s.rc.curve([[x1, y1], [mx, my], [x2, y2]], oo));
    var ang = Math.atan2(y2 - my, x2 - mx), L = 38, sp = .5;
    _add(s, s.rc.line(x2, y2, x2 - L * Math.cos(ang - sp), y2 - L * Math.sin(ang - sp), oo), "head");
    _add(s, s.rc.line(x2, y2, x2 - L * Math.cos(ang + sp), y2 - L * Math.sin(ang + sp), oo), "head");
  }
  function label(name, x, y, txt, o) {   // Pangolin, fades in after its shapes
    var s = SK[name], t = document.createElementNS("http://www.w3.org/2000/svg", "text");
    t.setAttribute("x", x); t.setAttribute("y", y);
    t.setAttribute("text-anchor", (o && o.anchor) || "middle");
    t.setAttribute("font-size", (o && o.size) || 50);
    if (o && o.color) t.style.fill = o.color;
    t.textContent = txt; t.style.opacity = 0; s.g.appendChild(t);
    s.shapes.push({text: t});
  }
  // draw a sketch on from time t: each stroke 0.7 s, in sequence (the next one
  // starts as the last is two-thirds done); a label fades in after its box.
  function draw(name, t, per) {
    var s = SK[name], at = t; per = per || .7;
    s.shapes.forEach(function (sh) {
      if (sh.text) { tl.to(sh.text, {opacity: 1, duration: .35}, at + .05); return; }
      // an arrowhead is a flick, not a stroke: the arrow reads as one gesture
      if (sh.kind === "head") {
        sh.paths.forEach(function (p) { tl.to(p, {strokeDashoffset: 0, duration: .18, ease: "power1.out"}, at); });
        at += .12; return;
      }
      sh.paths.forEach(function (p, i) {
        tl.to(p, {strokeDashoffset: 0, duration: per, ease: "power1.inOut"}, at + i * .12);
      });
      at += per * .66 + (sh.paths.length - 1) * .12;
    });
    return at;
  }
  function erase(name, t) { tl.to("#sk-" + name, {autoAlpha: 0, duration: .3, ease: "power2.in"}, t); }
"""


class G(object):
    def __init__(self, dur, reel, fps=30):
        self.dur, self.reel, self.fps = dur, reel, fps
        self.mattes = []
        self.cues = []

    # -- sound (tools/sfx.py mixes sfx.json under her voice) ----------------
    def sfx(self, name, t, db=0):
        self.cues.append({"t": round(t, 3), "name": name, **({"db": db} if db else {})})

    # -- her cut-out for one beat -------------------------------------------
    def matte(self, name, start, dur):
        # on the frame grid: matte.py cuts whole frames from int(start*fps), so
        # an off-grid data-start would lay her cut-out half a frame off herself
        f0 = int(start * self.fps + 1e-6)
        n = int(round((start + dur) * self.fps)) + 1 - f0
        start, dur = f0 / float(self.fps), n / float(self.fps)
        self.mattes.append(
            '      <video id="matte-%s" class="plate matte" src="assets/mattes/%s.webm"\n'
            '             data-start="%.3f" data-duration="%.3f" data-media-start="0"\n'
            '             muted playsinline></video>' % (name, name, start, dur))

    # -- §00.2 captions: phrase chunks, a key word in a pill ----------------
    STOP = set(u"і й та а але що це як в у на з зі із до для по від не ні ти я ми ви він вона воно "
               u"вони мені тобі його її їх свій своє свою свої твій твоє твою твої мій моє мою мої "
               u"то так от же ж би б чи або ще вже тут там цей ця ці той та те тих тому коли якщо "
               u"щоб бо теж також навіть просто саме дуже все всі весь вся".split())

    def chunks(self, caps, keys=None, place=(), max_chars=40, max_words=6, gap=0.38):
        """Group word captions into phrases of one or two lines.

        keys:  {start_time_of_word: True} pins the key word by its time (±0.06 s),
               {"word": True} pins it by text; {"off": [t0, ...]} gives a chunk
               starting there no pill. Otherwise the longest content word wins,
               with numbers and Latin brand names first.
        place: [(t0, t1, "top", y)] puts the box's top at y for chunks starting
               in [t0, t1); [(t0, t1, "bottom", y)] its bottom. Default bottom 1520.
        """
        keys = keys or {}
        out, cur = [], []

        def flush():
            if cur:
                out.append(list(cur))
                del cur[:]

        for i, c in enumerate(caps):
            if cur:
                prev = cur[-1]
                text = " ".join(x["w"] for x in cur + [c])
                if (c["s"] - prev["e"] > gap or len(text) > max_chars or len(cur) >= max_words
                        or (re.search(u"[.!?…]$", prev["w"]) and len(cur) >= 1)
                        or (re.search(u"[,:;—–]$", prev["w"]) and len(cur) >= 3)):
                    flush()
            cur.append(c)
        flush()
        # a lone short word glued to its neighbour reads better than a flash
        merged = []
        for ch in out:
            if merged and len(ch) == 1 and len(ch[0]["w"]) <= 4 and \
                    ch[0]["s"] - merged[-1][-1]["e"] < 0.25 and \
                    len(" ".join(x["w"] for x in merged[-1] + ch)) <= max_chars + 6:
                merged[-1].extend(ch)
            else:
                merged.append(ch)
        res = []
        for n, ch in enumerate(merged):
            s = ch[0]["s"]
            nxt = merged[n + 1][0]["s"] if n + 1 < len(merged) else self.dur
            e = min(nxt, ch[-1]["e"] + 0.6)
            kw = self._key(ch, keys)
            pos = ("bottom", 1920 - 1520)
            for a, b, how, y in place:
                if a <= s < b:
                    pos = (how, y if how == "top" else 1920 - y)
            res.append({"s": round(s, 3), "e": round(e, 3), "words": ch, "key": kw, "pos": pos})
        return res

    def _key(self, ch, keys):
        if any(abs(ch[0]["s"] - t) < 0.06 for t in keys.get("off", [])):
            return None
        for i, w in enumerate(ch):
            if any(isinstance(t, float) and abs(w["s"] - t) < 0.06 for t in keys):
                return i
            if keys.get(w["w"].strip(u".,!?:;«»—–")):
                return i
        best, bi = 0, None
        for i, w in enumerate(ch):
            bare = re.sub(u"[^\\w€%+'’ʼ-]", "", w["w"])
            low = bare.lower()
            if not bare or low in self.STOP:
                continue
            sc = len(bare)
            if re.search(u"\\d", bare):
                sc += 20
            if re.search(u"[A-Za-z]", bare) or bare[:1].isupper() and i > 0:
                sc += 8
            if sc > best:
                best, bi = sc, i
        return bi if best >= 5 else None

    def caps_html(self, chunks):
        out = []
        for n, c in enumerate(chunks):
            words = []
            for i, w in enumerate(c["words"]):
                t = esc(w["w"])
                if i == c["key"]:
                    # the punctuation stays outside the pill
                    m = re.match(u"^(.*?)([.,!?:;…»]*)$", t)
                    words.append('<span class="k"><span class="kb"></span><span class="kt">%s</span></span>%s'
                                 % (m.group(1), m.group(2)))
                else:
                    words.append(t)
            how, y = c["pos"]
            style = ("top:%dpx" % y) if how == "top" else ("bottom:%dpx" % y)
            out.append('<div class="cap" id="cap%d" style="%s"><span class="box">%s</span></div>'
                       % (n, style, " ".join(words)))
        return "\n      ".join(out)

    def caps_js(self, chunks, blackout=()):
        L = []
        for n, c in enumerate(chunks):
            if any(a <= c["s"] < b for a, b in blackout):
                continue
            L.append('  tl.set("#cap%d", {autoAlpha: 1}, %.3f);' % (n, c["s"]))
            L.append('  tl.fromTo("#cap%d .box", {opacity: 0, y: 18, scale: .96}, X({opacity: 1, y: 0, scale: 1, '
                     'duration: .35, ease: RISE}), %.3f);' % (n, c["s"]))
            if c["key"] is not None:
                ks = c["words"][c["key"]]["s"]
                L.append('  tl.fromTo("#cap%d .kb", {opacity: 0, scale: .6}, X({opacity: 1, scale: 1, '
                         'duration: .5, ease: POP}), %.3f);' % (n, ks))
                L.append('  tl.to("#cap%d .kt", {color: "#FFFFFF", duration: .12}, %.3f);' % (n, ks))
            L.append('  tl.set("#cap%d", {autoAlpha: 0}, %.3f);' % (n, c["e"]))
        return "\n".join(L)

    # -- assembly ----------------------------------------------------------
    def document(self, title, plate, behind="", panel="", front="", cover="", js="",
                 chunks=(), blackout=(), extra_css="", push=True):
        head = JS
        if push:   # §0.8, kept: a slow push on the plate, the matte moving with it
            head += ('\n  gsap.set(PUSH, {transformOrigin: "540px 900px"});\n'
                     '  tl.fromTo(PUSH, {scale: 1}, {scale: 1.045, duration: %.3f, ease: "none"}, 0);\n'
                     % self.dur)
        return u'''<!DOCTYPE html>
<html lang="uk">
  <head>
    <meta charset="utf-8">
    <title>%(title)s</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
    <script src="assets/js/rough-4.6.6.js"></script>
    <style>%(css)s%(extra)s
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0"
         data-width="1080" data-height="1920" data-duration="%(dur).3f" data-fps="%(fps)d">

      <video id="vid" class="plate" src="%(plate)s"
             data-start="0" data-duration="%(dur).3f" data-media-start="0"
             muted playsinline></video>
      <div id="behind" class="L">
%(behind)s
      </div>
      <div id="panel">
%(panel)s
      </div>
%(mattes)s
      <div id="front" class="L">
%(front)s
      </div>
      <div id="cover">
%(cover)s
      </div>
      <div id="caps">
      %(caps)s
      </div>

      <audio id="vo" src="%(plate)s"
             data-start="0" data-duration="%(dur).3f" data-media-start="0"></audio>
    </div>

    <script>
      function build() {
        var tl = gsap.timeline({paused: true});
%(head)s
%(capjs)s

%(js)s

        window.__timelines["main"] = tl;
      }
      if (document.fonts && document.fonts.ready) document.fonts.ready.then(build);
      else build();
    </script>
  </body>
</html>
''' % {"title": esc(title), "css": CSS, "extra": extra_css, "dur": self.dur, "fps": self.fps,
       "plate": plate, "behind": behind, "panel": panel, "mattes": "\n".join(self.mattes),
       "front": front, "cover": cover, "caps": self.caps_html(chunks), "head": head,
       "capjs": self.caps_js(chunks, blackout), "js": js}

    def write(self, here, doc):
        io.open(os.path.join(here, "index.html"), "w", encoding="utf-8").write(doc)
        self.cues.sort(key=lambda c: c["t"])
        io.open(os.path.join(here, "sfx.json"), "w", encoding="utf-8").write(json.dumps(self.cues, indent=1))


class Words(object):
    """Word times by text: W.s("дизайном", 35.5) is the start of the «дизайном»
    nearest 35.5 s, and it fails loudly if that word is not within 0.8 s —
    a beat lands ON its word (STYLE §4a.1), so a drifted time is a bug."""

    def __init__(self, caps):
        self.caps = caps

    @staticmethod
    def _n(s):
        return "".join(ch for ch in s.lower() if ch.isalnum())

    def hit(self, word, near):
        hits = [c for c in self.caps if self._n(word) == self._n(c["w"])]
        assert hits, word
        c = min(hits, key=lambda c: abs(c["s"] - near))
        assert abs(c["s"] - near) < 0.8, (word, near, c["s"])
        return c

    def s(self, word, near):
        return self.hit(word, near)["s"]

    def e(self, word, near):
        return self.hit(word, near)["e"]


def load_caps(nn, fix=None):
    """captions.json for reel nn, with a FIX dict applied (whisper's mangling
    of what she plainly said -> her word), word ends clamped so two words never
    overlap."""
    caps = json.load(io.open(os.path.join(ROOT, "work", "r" + nn, "captions.json"), encoding="utf-8"))["words"]
    fix = fix or {}
    out = []
    for c in caps:
        key = (c["w"], round(c["s"], 1))
        w = fix.get(key, fix.get(c["w"], c["w"]))
        if w is None:
            continue
        out.append(dict(c, w=w))
    for a, b in zip(out, out[1:]):
        a["e"] = round(max(a["s"] + 0.10, min(a["e"], b["s"] - 0.02)), 3)
    return out


def mark(slug, size=64, cls="mark"):
    """A monochrome simple-icons mark from assets/icons as inline SVG."""
    p = os.path.join(ROOT, "assets", "icons", slug + ".svg")
    svg = io.open(p, encoding="utf-8").read()
    d = re.search(r'<path[^>]* d="([^"]+)"', svg).group(1)
    return '<svg class="%s" width="%d" height="%d" viewBox="0 0 24 24"><path d="%s"/></svg>' % (cls, size, size, d)
