# -*- coding: utf-8 -*-
"""Reel 14 — «Мій блогерський сетап». Her travel blogging gear.

Variant B, refined glass (STYLE.md §0) — but this one is a vlog, and she
said so: *"i wanted not too many animations in the blogging gear one, keep it
+- natural like a vlogging reel, i feel like too many animations there would
look forced"* (2026-09-28, after the first full build). So her footage stays
in front almost the whole time, the captions carry the reel, and there are
five small touches, all NEAR, no takeover, no matte:

    37.3  «0,5 кг»     a spec chip beside her while she swings the tripod
    42.6  «150 см»     a hairline dimension up the extended tripod + chip
    53.1  «8 €»        the Amazon holder's price, beside her head
    64.7  the holder   her photo of it as one clean glass card (the one item
                       she could not show — it is holding the camera), with
                       «MagSafe» and «присоска», for that one sentence
    85.0  «3 000 ₴»    the mic's price, which turns into «3 режими»

Each is a small dark-glass chip (or the one white card), 1.5-2.5 s on its
words, then gone. The full chain build (packing list, burgundy takeover,
setup behind her) is what she turned down; it is not in the repo.

usage: python build.py
"""
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))
from kit import Kit  # noqa: E402
from glass import Glass  # noqa: E402

DUR = 163.250          # 4898 plate frames / 30 (work/w40-queue.log)
FPS = 30
k = Kit(width=1080, height=1920, fps=FPS, duration=DUR)
g = Glass()
k.css(g.css())

BEATS = []


def beat(fn):
    BEATS.append(fn)
    return fn


# ---------------------------------------------------------------------------
# NO-PAINT ZONES (STYLE.md §4a). Her cut: nine shots (tools/shots.py). The one
# comedy insert is shot 7, a 1.07 s pull-out under «кастомізабельний!»
# (137.50-138.57, also found by tools/pullouts.py). Shot 6 opens on her
# leaning right into the lens and back out (120.23-120.70, frame diffs) —
# hers too. The spoken gags are listed as well, so review.py keeps them
# clear: «розчаруєтесь… мінімалістичний», «інакше мій РДУГ…», «не питайте
# навіщо, я навіть не знаю», «здається це був Юск».
NO_PAINT = [(7.36, 12.29), (23.36, 25.70), (92.94, 95.00), (120.23, 120.70), (125.88, 128.80),
            (137.50, 138.57)]

# ---------------------------------------------------------------------------
# Words. Script spelling on her timing: work/r14/captions.json after
# tools/patchcaps.py with work/r14/caption-patch.json (her improvisations
# kept, whisper's mishearings put back to the script: «мастхеви», «РДУГ»,
# «ревьорб», «вдячна»…). Ends are normalised here: at least 0.30 s where the
# next word allows, never past the next word, never a whisper-stretched 4 s
# «він» held over a pause, and never an end before its own start (a split
# «їх» with no room once sat on screen for the rest of the reel).
CAPS = k.load_captions(os.path.join(ROOT, "work", "r14", "captions.json"))

try:
    from PIL import ImageFont
    _CF = ImageFont.truetype(os.path.join(HERE, "assets", "fonts", "ProductSans-Black.woff"), 90)

    def cap_w(s):
        return _CF.getlength(s.upper()) - 0.015 * 90 * len(s)
except Exception:          # no Pillow: a rough per-glyph width
    def cap_w(s):
        return 58.0 * len(s)


def _split_wide(caps, limit=1000.0):
    """A merged token («їх використовувати,») wider than the frame is split
    into its words; every word gets at least 0.24 s of the span."""
    out = []
    for c in caps:
        ws = c["w"].split()
        if len(ws) < 2 or cap_w(c["w"]) <= limit:
            out.append(c)
            continue
        span = c["e"] - c["s"]
        tot = float(sum(len(w) for w in ws))
        durs = [max(0.24, span * len(w) / tot) for w in ws[:-1]]
        durs.append(max(0.24, span - sum(durs)))
        t = c["s"]
        for w, d in zip(ws, durs):
            out.append({"w": w, "s": round(t, 3), "e": round(t + d - 0.02, 3)})
            t += d
    return out


CAPS = _split_wide(CAPS)
for _a, _b in zip(CAPS, CAPS[1:]):
    _e = max(_a["e"], _a["s"] + 0.30)
    _e = min(_e, _a["s"] + max(0.75, 0.085 * len(_a["w"]) + 0.35))
    _e = min(_e, _b["s"] - 0.085)
    if _e < _a["s"] + 0.08:
        _e = _b["s"] - 0.005
    _a["e"] = round(_e, 3)
CAPS[-1]["e"] = round(min(CAPS[-1]["e"], DUR - 0.05), 3)
# «інакше мій РДУГ»: whisper heard «і найшим мірі дух»; re-share its span
for _c in CAPS:
    if abs(_c["s"] - 23.76) < 0.02:
        _c["e"] = 23.965
    if abs(_c["s"] - 24.10) < 0.02:
        _c["s"], _c["e"] = 24.00, 24.255
for _a, _b in zip(CAPS, CAPS[1:]):
    assert _a["s"] < _a["e"] <= _b["s"], (_a, _b)


def _n(s):
    return "".join(ch for ch in s.lower() if ch.isalnum() or ch in "+'")


def at(word, n=1):
    """The n-th caption carrying `word` (punctuation ignored)."""
    hit = 0
    for c in CAPS:
        if _n(word) in [_n(x) for x in c["w"].split()]:
            hit += 1
            if hit == n:
                return c
    raise KeyError(word)


def S(w, n=1):
    return at(w, n)["s"]


def E(w, n=1):
    return at(w, n)["e"]


def js(src, **vals):
    """`@name` -> a literal time. Literals, not variables, because
    tools/review.py reads the timeline off the generated numbers."""
    def rep(m):
        v = vals[m.group(1)]
        return "%.3f" % v if isinstance(v, (int, float)) else str(v)
    return re.sub(r"@(\w+)", rep, src)


def P(x, y, t):
    """A point measured on her plate -> where it is on screen at time t: the
    plate pushes 1.0 -> 1.045 about (540, 820) across the reel (§0.8)."""
    s = 1.0 + 0.045 * t / DUR
    return (540.0 + (x - 540.0) * s, 820.0 + (y - 820.0) * s)


def leave(sel, t, y=-18):
    return ('  G.blurOut("%s", %.3f, 10, 0.26);\n'
            '  tl.to("%s", {y: %d, scale: 0.94, duration: 0.26, ease: "power2.in"}, %.3f);'
            % (sel, t, sel, y, t))


GLY = {
    "weight": '<path d="M16.5 20.5V15a5 5 0 0 1 5-5h5a5 5 0 0 1 5 5v5.5"/><circle cx="24" cy="31" r="13"/>',
    "mic": '<rect x="17" y="4" width="14" height="23" rx="7"/><path d="M11 21a13 13 0 0 0 26 0M24 34v9M17 43h14"/>',
    "ruler": '<path d="M24 4v40M16 4h16M16 44h16"/>',
}


def gly(name):
    return '<svg class="gy" viewBox="0 0 48 48">%s</svg>' % GLY[name]


k.css("""
/* Product Sans has no hryvnia sign: ₴ alone falls through to Inter, per glyph */
@font-face { font-family: "InterUAH"; src: url("assets/fonts/Inter.ttf"); font-weight: 100 900;
  unicode-range: U+20B4; font-display: block; }
#root { font-family: "ProductSans", "InterUAH", system-ui, sans-serif; }
.abs, .cx { position: absolute; }
.hide { opacity: 0; visibility: hidden; }
.gy { fill: none; stroke: currentColor; stroke-width: 3.4; stroke-linecap: round; stroke-linejoin: round; }

/* ---- the small spec chip: dark glass, a tile, a micro label, the value ----
   Apple's spec line, sized to sit beside her and not compete with her. */
.sc { position: absolute; height: 96px; border-radius: 34px; overflow: hidden; }
.sc .sct { position: absolute; left: 14px; top: 14px; width: 68px; height: 68px; }
.sc .sct .gy { position: relative; z-index: 1; width: 52%; height: 52%; color: #fff; }
.sc .sct .pearl .gy { color: #17141c; }
.sc .sct .pearl .mk { width: 56%; height: 56%; }
.sc .scm { position: absolute; left: 98px; top: 15px; font-size: 18px; font-weight: 700;
  letter-spacing: 0.16em; color: #ffb3c9; line-height: 20px; white-space: nowrap; }
.sc .scv { position: absolute; left: 96px; top: 38px; font-size: 46px; font-weight: 900;
  letter-spacing: -0.035em; line-height: 52px; color: #fff; white-space: nowrap; }
.sc .scv small { font-size: 30px; font-weight: 700; letter-spacing: -0.01em; margin-left: 6px; }
.sc .rd { position: absolute; left: 0; top: 0; white-space: nowrap; }
""")


def chip(cid, box, w, tile, micro, value, tile_cls="clear edge"):
    return (u'<div class="sc dglass edge hide" id="%s" style="left:%dpx;top:%dpx;width:%dpx">'
            u'<div class="sct"><div class="%s">%s</div></div>'
            u'<div class="scm" id="%s-m">%s</div><div class="scv" id="%s-v">%s</div>'
            u'<div class="sheen" id="%s-sh"></div></div>'
            % (cid, box[0], box[1], w, tile_cls, tile, cid, micro, cid, value, cid))


# =================================================================== b10
@beat
def b10_weight():
    """«…великий від Ulanzi, він важить півкіло»

    NEAR. She swings the tripod about the whole time, so the weight sits on
    a small chip beside her head rather than on a leader chasing it:
    «ВАГА · 0,5 кг», landing on «півкіло» (blackout — it says the word)."""
    html = u'<div class="g full" id="g10">%s</div>' % chip(
        "wC", (100, 420), 262, gly("weight"), u"ВАГА", u"0,5<small>кг</small>")
    src = js('''
  tl.set("#g10", {autoAlpha: 1}, @t_in);
  G.arrive("#wC", @t_in, {s: 0.7, y: 16});
  G.inner("#wC-v", @t_in);
  G.sheen("#wC-sh", @t_sh);
LEAVE
  tl.to("#g10", {autoAlpha: 0, duration: 0.02}, @t_off);''',
             t_in=S(u"півкіло") - 0.10, t_sh=S(u"півкіло") + 0.30, t_off=E(u"півкіло") + 0.95)
    return html, src.replace("LEAVE", leave("#wC", E(u"півкіло") + 0.65))


# =================================================================== b10b
k.css("""
#dim { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; overflow: visible;
  filter: drop-shadow(0 0 5px rgba(12,2,6,0.5)); }
#dim path { fill: none; stroke: #fff; stroke-width: 3.5; stroke-linecap: round; }
""")


@beat
def b10b_height():
    """«…висотою він метр п'ятдесят»

    NEAR, on her real tripod. She walks back and pulls it to full height
    (39-41.5 s, left clear); then one hairline draws up beside the pole from
    the floor to the clamp and the chip counts to «150 см», landing on
    «метр» (blackout). Positions off the 42.5 s frame (pole x≈333, clamp top
    y≈620), mapped through the plate push."""
    t = 42.8
    x0, top = P(262, 626, t)
    _, bot = P(262, 1905, t)
    d = "M %.1f %.1f V %.1f" % (x0, bot, top)
    ticks = "M %.1f %.1f H %.1f M %.1f %.1f H %.1f" % (x0 - 20, bot, x0 + 20, x0 - 20, top, x0 + 20)
    html = u'''
      <div class="g full" id="g10b">
        <svg id="dim" viewBox="0 0 1080 1920"><path id="dimL" d="%s"/><path id="dimT" d="%s"/></svg>
        %s
      </div>''' % (d, ticks, chip("hC", (round(x0) - 131, 486), 262, gly("ruler"), u"ВИСОТА",
                                  u'<span id="hV">0</span><small>см</small>'))
    src = js('''
  tl.set("#g10b", {autoAlpha: 1}, @t_in);
  G.arrive("#hC", @t_in, {s: 0.7, y: 16});
  G.draw("dimL", @t_d, 0.42);
  tl.fromTo("#dimT", {autoAlpha: 0}, {autoAlpha: 1, duration: 0.3}, @t_d);
  G.count("#hV", @t_d, 150, 0.40);
  // «метр п'ятдесят»
  G.bump("#hC", @metr);
  G.sheen("#hC-sh", @metr);
LEAVE
  tl.to("#g10b", {autoAlpha: 0, duration: 0.02}, 44.900);''',
             t_in=S(u"метр") - 0.42, t_d=S(u"метр") - 0.40, metr=S(u"метр"))
    return html, src.replace("LEAVE", leave("#hC", 44.600) +
                             '\n  tl.to("#dim", {autoAlpha: 0, duration: 0.25}, 44.600);')


# =================================================================== b12
@beat
def b12_price_eur():
    """«…ось такий на Амазоні за 8 євро, і він закручується»

    NEAR, beside her head on the side she holds the holder: the Amazon mark
    in a pearl tile, «ЦІНА · 8 €» landing on «8 євро» (blackout)."""
    html = u'<div class="g full" id="g12">%s</div>' % chip(
        "eC", (730, 650), 236, g.mark("amazon"), u"ЦІНА", u"8<small>€</small>", tile_cls="pearl")
    src = js('''
  tl.set("#g12", {autoAlpha: 1}, @t_in);
  G.arrive("#eC", @t_in, {s: 0.7, y: 16});
  G.inner("#eC-v", @t_in);
  G.sheen("#eC-sh", @t_sh);
LEAVE
  tl.to("#g12", {autoAlpha: 0, duration: 0.02}, @t_off);''',
             t_in=S(u"8") - 0.10, t_sh=S(u"закручується"), t_off=S(u"закручується") + 1.20)
    return html, src.replace("LEAVE", leave("#eC", S(u"закручується") + 0.90))


# =================================================================== b14
# The holder photo (reel-14/assets/media/holder.png, 373x697, the white of
# her product shot cut out) at HS in a white glass card. Points measured on
# the cut-out: the MagSafe disc's right rim, the suction pad's right edge.
CX, CY, CW, CH = 600, 70, 440, 470
HS, HPX, HPY = 0.62, 20, 18
RIM, PAD = (240, 150), (300, 660)
k.css("""
#hc { left: %(cx)dpx; top: %(cy)dpx; width: %(cw)dpx; height: %(ch)dpx; border-radius: 46px; overflow: hidden;
  background: linear-gradient(170deg, rgba(255,255,255,0.94) 0%%, rgba(255,249,251,0.90) 55%%, rgba(253,238,243,0.88) 100%%);
  -webkit-backdrop-filter: blur(20px) saturate(1.4); backdrop-filter: blur(20px) saturate(1.4);
  box-shadow: inset 0 2px 1px #fff, inset 0 -24px 50px -26px rgba(180,18,47,0.16), 0 44px 90px -34px rgba(20,2,8,0.6); }
#hcImg { position: absolute; left: %(px)dpx; top: %(py)dpx; width: %(pw)dpx; height: %(ph)dpx;
  transform-origin: 50%% 92%%; }
#hcInk { position: absolute; left: 0; top: 0; width: %(cw)dpx; height: %(ch)dpx; overflow: visible; }
#hcInk line { stroke: rgba(23,20,28,0.5); stroke-width: 2.5; stroke-linecap: round; }
.hcd { position: absolute; width: 0; height: 0; }
.hcd b { position: absolute; left: -8px; top: -8px; width: 16px; height: 16px; border-radius: 50%%;
  background: linear-gradient(165deg, #e0204b, #8d0d24); box-shadow: 0 0 0 4px #fff, 0 4px 10px rgba(60,10,25,0.4); }
.hcl { position: absolute; left: 270px; font-size: 34px; font-weight: 900; letter-spacing: -0.035em;
  line-height: 40px; padding-right: 6px; white-space: nowrap;
  background: linear-gradient(118deg, #7e0b20 0%%, #b4122f 42%%, #ff6e9c 100%%);
  -webkit-background-clip: text; background-clip: text; color: transparent; }
""" % {"cx": CX, "cy": CY, "cw": CW, "ch": CH, "px": HPX, "py": HPY,
       "pw": round(373 * HS), "ph": round(697 * HS)})


@beat
def b14_holder_card():
    """«Тут він трошки крутиться в різні сторони, сам тримач магнітний, а з
    іншої сторони присоска для будь-яких гладких поверхонь»

    NEAR. The one item she could not show — it is holding the camera — so
    her photo of it sits on one clean white glass card up beside her head,
    for this sentence only. It rocks a little on «крутиться в різні
    сторони» (one photo: a turn it can honestly make, never a faked angle);
    «MagSafe» points at the ring on «магнітний»; «присоска» at the base on
    «присоска» (blackout — the card says it)."""
    rim = (HPX + RIM[0] * HS, HPY + RIM[1] * HS)
    pad = (HPX + PAD[0] * HS, HPY + PAD[1] * HS)
    ms_y, su_y = rim[1] - 20, pad[1] - 22
    html = u'''
      <div class="g full" id="g14">
        <div class="abs edge hide" id="hc">
          <img id="hcImg" src="assets/media/holder.png" alt="">
          <svg id="hcInk" viewBox="0 0 %(cw)d %(ch)d">
            <line id="hcMsL" x1="%(rx).1f" y1="%(ry).1f" x2="262" y2="%(ry).1f"/>
            <line id="hcSuL" x1="%(px).1f" y1="%(py).1f" x2="262" y2="%(py).1f"/>
          </svg>
          <div class="hcd hide" id="hcMsD" style="left:%(rx).0fpx;top:%(ry).0fpx"><b></b></div>
          <div class="hcl hide" id="hcMs" style="top:%(msy).0fpx">MagSafe</div>
          <div class="hcd hide" id="hcSuD" style="left:%(px).0fpx;top:%(py).0fpx"><b></b></div>
          <div class="hcl hide" id="hcSu" style="top:%(suy).0fpx">присоска</div>
          <div class="sheen" id="hcSh"></div>
        </div>
      </div>''' % {"cw": CW, "ch": CH, "rx": rim[0], "ry": rim[1], "px": pad[0], "py": pad[1],
                   "msy": ms_y, "suy": su_y}
    src = js('''
  tl.set("#g14", {autoAlpha: 1}, @t_in);
  gsap.set("#hcSh", {xPercent: -120});
  G.drawPrep("hcMsL"); G.drawPrep("hcSuL");
  // «Тут він» — the card, her photo landing a beat after it
  G.arrive("#hc", @t_in, {s: 0.72, y: -24});
  tl.fromTo("#hcImg", {scale: 0.8, autoAlpha: 0, y: 20}, {scale: 1, autoAlpha: 1, y: 0, duration: 0.7, ease: SP, immediateRender: false}, @t_img);
  G.sheen("#hcSh", @t_img2);
  // «трошки крутиться в різні сторони» — a small honest rock
  tl.to("#hcImg", {rotation: -3.5, duration: 0.42, ease: "sine.inOut"}, @kr);
  tl.to("#hcImg", {rotation: 2.5, duration: 0.45, ease: "sine.inOut"}, @rizni);
  tl.to("#hcImg", {rotation: 0, duration: 0.7, ease: SP}, @storony);
  // «магнітний» — the MagSafe ring
  tl.fromTo("#hcMsD", {scale: 0, autoAlpha: 0}, {scale: 1, autoAlpha: 1, duration: 0.45, ease: POP, immediateRender: false}, @magn);
  G.draw("hcMsL", @magn2, 0.26);
  G.blurIn("#hcMs", @magn3, 8, 0.28);
  tl.fromTo("#hcMs", {x: -14}, {x: 0, duration: 0.6, ease: SP, immediateRender: false}, @magn3);
  // «присоска» — the base
  tl.fromTo("#hcSuD", {scale: 0, autoAlpha: 0}, {scale: 1, autoAlpha: 1, duration: 0.45, ease: POP, immediateRender: false}, @pris);
  G.draw("hcSuL", @pris2, 0.26);
  G.blurIn("#hcSu", @pris3, 8, 0.28);
  tl.fromTo("#hcSu", {x: -14}, {x: 0, duration: 0.6, ease: SP, immediateRender: false}, @pris3);
LEAVE
  tl.to("#g14", {autoAlpha: 0, duration: 0.02}, @t_off);''',
             t_in=S(u"тут") - 0.10, t_img=S(u"тут") + 0.02, t_img2=S(u"тут") + 0.35,
             kr=S(u"крутиться"), rizni=S(u"різні") - 0.02, storony=S(u"сторони") + 0.12,
             magn=S(u"магнітний") - 0.04, magn2=S(u"магнітний") + 0.04, magn3=S(u"магнітний") + 0.20,
             pris=S(u"присоска") - 0.06, pris2=S(u"присоска") + 0.02, pris3=S(u"присоска") + 0.16,
             t_off=E(u"поверхонь") + 0.28)
    return html, src.replace("LEAVE", leave("#hc", E(u"поверхонь") - 0.02))


# =================================================================== b18
@beat
def b18_mic_price_modes():
    """«…куплений за 3000 гривень. Тут є три режими…»

    NEAR, above her head (the box has just left her hands; the mic is the
    one clipped to her top). One chip, two readings: «ЦІНА · 3 000 ₴» on
    «3000 гривень», then «МІКРОФОН · 3 режими» on «три режими» (blackout on
    both — the chip says them). Gone before she names the modes."""
    html = u'<div class="g full" id="g18">%s</div>' % chip(
        "mC", (390, 390), 300, gly("mic"),
        u'<span class="rd" id="mM1">ЦІНА</span><span class="rd" id="mM2">МІКРОФОН</span>',
        u'<span class="rd" id="mV1">3 000<small>₴</small></span>'
        u'<span class="rd" id="mV2">3<small>режими</small></span>', tile_cls="pearl")
    src = js('''
  tl.set("#g18", {autoAlpha: 1}, @t_in);
  gsap.set(["#mM2", "#mV2"], {autoAlpha: 0});
  G.arrive("#mC", @t_in, {s: 0.7, y: 16});
  G.inner("#mC-v", @t_in);
  G.sheen("#mC-sh", @t_sh);
  // «три режими» — the same chip, a second reading
  G.blurOut(["#mM1", "#mV1"], @swap, 8, 0.2);
  G.blurIn("#mM2", @swap2, 8, 0.28);
  tl.fromTo("#mV2", {autoAlpha: 0, scale: 0.6, transformOrigin: "0% 60%"}, {autoAlpha: 1, scale: 1, duration: 0.55, ease: POP, immediateRender: false}, @swap2);
  G.bump("#mC", @swap2);
LEAVE
  tl.to("#g18", {autoAlpha: 0, duration: 0.02}, @t_off);''',
             t_in=S(u"3000") - 0.10, t_sh=S(u"3000") + 0.30, swap=S(u"три") - 0.22,
             swap2=S(u"три") - 0.02, t_off=S(u"три") + 1.95)
    return html, src.replace("LEAVE", leave("#mC", S(u"три") + 1.65))


# ---------------------------------------------------------------------------
# Captions drop only on redundancy (STYLE.md §2b.1): where a graphic's own
# text says the word she is saying at that moment. Spans under 1.3 s drop the
# caption but keep the plaque — dropping the plaque for one word reads as a
# blink (reel 12's «+»).
def _bo(w0, w1=None, n0=1, n1=1, why=""):
    a = S(w0, n0) - 0.01
    b = E(w1 or w0, n1 if w1 else n0) + 0.01
    return (round(a, 3), round(b, 3), why)


BLACKOUT = [
    _bo(u"півкіло", why="b10 — «0,5 кг»"),
    _bo(u"метр", u"п'ятдесят", why="b10b — «150 см»"),
    _bo(u"8", u"євро", why="b12 — «8 €»"),
    _bo(u"присоска", why="b14 — the card says «присоска»"),
    _bo(u"3000", u"гривень", why="b18 — «3 000 ₴»"),
    _bo(u"три", u"режими", why="b18 — «3 режими»"),
]
INVERT = []
SHORT = 1.3


def main():
    gh, gj = [], []
    for fn in BEATS:
        h, j = fn()
        gh.append(h.rstrip())
        gj.append("  /* %s */" % fn.__name__)
        gj.append(j.rstrip())

    long_bo = [b for b in BLACKOUT if b[1] - b[0] >= SHORT]
    short_bo = [b for b in BLACKOUT if b[1] - b[0] < SHORT]
    caps = [c for c in CAPS if not any(a <= c["s"] < b for a, b, _ in short_bo)]

    # the slow push on the plate (§0.8)
    head = [g.js(), "  var G = helpers(tl);",
            '  gsap.set("#vid", {transformOrigin: "540px 820px"});',
            '  tl.fromTo("#vid", {scale: 1}, {scale: 1.045, duration: %.3f, ease: "none"}, 0);' % DUR]
    doc = k.document(
        title=u"Reel 14 — Мій блогерський сетап",
        plate="assets/base.mp4",
        gfx_html=g.defs() + "\n" + "\n".join(gh),
        gfx_js="\n".join(head + gj),
        caps=caps,
        blackout=long_bo,
        invert=INVERT,
    )
    out = os.path.join(HERE, "index.html")
    io.open(out, "w", encoding="utf-8").write(doc)
    print("index.html  %d captions, %d beats, %.1f KB"
          % (len(caps), len(BEATS), os.path.getsize(out) / 1024.0))
    for b in BLACKOUT:
        print("  blackout %7.2f-%7.2f  %s" % b)


if __name__ == "__main__":
    main()
