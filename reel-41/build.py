# -*- coding: utf-8 -*-
"""Reel 41 — «Незапланований рілс». Test pass: one 7.4 s take, cut to 6.4 s.

The one object is **the post that goes to Instagram**: first a chat-bot wired
to Instagram, then the slot it leaves, then the reel that takes it.

Chain:  near: Instagram cabled to a chat-bot tile above her head, a packet
runs -> «перестав працювати» the cable snaps, the bot greys out and gets a ✕
-> OVER: the iris opens out of the dead bot; burgundy ground, a white sheet
with two weeks of her content plan, planned reels sitting in their days,
today's cell empty -> «незапланований» a reel card drops into today, tilted
and too big for the cell -> «рілс» it lands with a sheen -> the iris closes
onto it: near, the reel card above her head, Instagram arrives on its left
and cables into it -> «ідеальний» a packet runs, «варіант» it gets the tick.

usage: python build.py   (then: python ../tools/sfx.py mix 41)
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

CUT = json.load(io.open(os.path.join(ROOT, "work", "r41", "cut.json"), encoding="utf-8"))
DUR = 6.383            # (192 plate frames - 0.5) / 30
FPS = 30
k = Kit(width=1080, height=1920, fps=FPS, duration=DUR)
g = Glass(["instagram"])
k.css(g.css())

NO_PAINT = [tuple(x) for x in CUT["no_paint"]]      # empty on this cut

CAPS = k.load_captions(os.path.join(ROOT, "work", "r41", "captions.json"))
# no written script for this one (she calls it unplanned in the take itself);
# her spoken words are the spelling, whisper's mishearings fixed by hand
FIX = {u"ріос,": u"рілс,"}
_caps = []
for c in CAPS:
    c["w"] = FIX.get(c["w"], c["w"])
    if c["w"] == u"що це ідеальний":
        # align merged three words onto one slot; whisper's own word times
        # (raw 5.66 / 5.66-5.76 / 5.76-6.34, clip 2 offset -0.57) split it back
        _caps += [dict(c, w=u"що", s=c["s"], e=5.13), dict(c, w=u"це", s=5.13, e=5.19),
                  dict(c, w=u"ідеальний", s=5.19, e=c["e"])]
    else:
        _caps.append(c)
CAPS = _caps
for _a, _b in zip(CAPS, CAPS[1:]):
    _a["e"] = round(max(_a["s"] + 0.06, _b["s"] - 0.085), 3)


def _n(s):
    return "".join(ch for ch in s.lower() if ch.isalnum())


def _hit(word, near):
    hits = [c for c in CAPS if _n(word) in [_n(x) for x in c["w"].split()]]
    c = min(hits, key=lambda c: abs(c["s"] - near))
    assert abs(c["s"] - near) < 0.6, (word, near, c["s"])
    return c


def S(word, near):
    return _hit(word, near)["s"]


def E(word, near):
    return _hit(word, near)["e"]


T = {
    "meni": S(u"Мені", 0.07), "bot": S(u"чат-бот", 0.55), "insta": S(u"Інстаграмі", 0.93),
    "perestav": S(u"перестав", 1.41), "prats": S(u"працювати", 1.71),
    "tomu": S(u"тому", 2.35), "tse": S(u"це", 2.47), "absol": S(u"абсолютно", 2.67),
    "nezapl": S(u"незапланований", 3.09), "rils": S(u"рілс", 3.79), "rilse": E(u"рілс", 3.79),
    "i": S(u"і", 4.185), "zaraz": S(u"зараз", 4.305), "vvazhaiu": S(u"вважаю", 4.725),
    "idealnyi": S(u"ідеальний", 5.19), "variant": S(u"варіант", 5.765),
    "dur": DUR,
}


def js(src, **extra):
    """`@name`, `@name+0.12`, `@name-0.1` -> one literal time."""
    vals = dict(T)
    vals.update(extra)

    def rep(m):
        v = vals[m.group(1)] + (float(m.group(2)) if m.group(2) else 0.0)
        return "%.3f" % v
    return re.sub(r"@(\w+)([+-]\d+(?:\.\d+)?)?", rep, src)


# ---------------------------------------------------------------------------
SFX = []


def sfx(name, t, db=0):
    if isinstance(t, str):
        t = float(js(t))
    SFX.append({"t": round(max(0.0, t), 3), "name": name, "db": db})


# ---------------------------------------------------------------------------
STROKES = {
    "check": '<path d="M5.4 12.6l4.3 4.3 8.9-9.5"/>',
    "x": '<path d="M7 7l10 10M17 7L7 17"/>',
    "chat": '<path d="M20.6 11.6a8.1 8.1 0 0 1-.9 3.7 8.2 8.2 0 0 1-7.3 4.5 8.1 8.1 0 0 1-3.7-.9L3.4 20.6l1.7-5.3a8.1 8.1 0 0 1-.9-3.7 8.2 8.2 0 0 1 4.5-7.3 8.1 8.1 0 0 1 3.7-.9h.5a8.2 8.2 0 0 1 7.7 7.7z"/>',
    "play": '<path d="M8.6 5.6v12.8l10-6.4z"/>',
}


def stroke(name, cls="sk"):
    return '<svg class="%s" viewBox="0 0 24 24">%s</svg>' % (cls, STROKES[name])


def tile(tid, size, x, y, material, inner, extra_cls="", ring=True, w=None):
    w = w or size
    r = ('<div class="sqring" id="%sR" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx"></div>'
         % (tid, x, y, w, size)) if ring else ""
    return ('%s<div class="tw hide %s" id="%s" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx">'
            '<div class="%s">%s<div class="sheen"></div></div></div>'
            % (r, extra_cls, tid, x, y, w, size, material, inner))


def badge(bid, x, y, kind):
    """A round pearl badge with a stroke glyph — the ✕ or the tick."""
    return ('<div class="bdg hide %s" id="%s" style="left:%dpx;top:%dpx">%s</div>'
            % (kind, bid, x, y, stroke("x" if kind == "no" else "check", "bk")))


def cable(cid, d):
    return ('<svg class="cab abs" id="%s" style="left:0;top:0" width="1080" height="1920" '
            'viewBox="0 0 1080 1920"><path class="tube" id="%sT" d="%s"/>'
            '<path class="core" id="%sC" d="%s"/><g class="pkg"><path class="pkt" id="%sP" d="%s"/></g></svg>'
            % (cid, cid, d, cid, d, cid, d))


k.css("""
.abs { position: absolute; }
.hide { opacity: 0; visibility: hidden; }
.tw { position: absolute; }
.sk { fill: none; stroke: url(#gw); stroke-width: 2.3; stroke-linecap: round; stroke-linejoin: round;
  width: 50%; height: 50%; position: relative; z-index: 1; overflow: visible; }
.dots { position: absolute; left: 0; right: 0; top: 47%; display: flex; justify-content: center; gap: 13px; z-index: 2; }
.dots i { display: block; width: 15px; height: 15px; border-radius: 50%; background: #ffd6e3; }
.bdg { position: absolute; width: 104px; height: 104px; border-radius: 50%; z-index: 5;
  display: flex; align-items: center; justify-content: center;
  background: linear-gradient(160deg, #ffffff 0%, #fff5f8 52%, #f5dfe6 100%);
  box-shadow: inset 0 2px 1px #fff, 0 22px 40px -14px rgba(30,4,12,0.6); }
.bk { width: 58%; height: 58%; fill: none; stroke: #b4122f; stroke-width: 3.4; stroke-linecap: round; stroke-linejoin: round; }
.bdg.ok { background: linear-gradient(165deg, #ff6e9c 0%, #e0204b 55%, #8d0d24 100%);
  box-shadow: inset 0 2px 1px rgba(255,255,255,0.6), 0 0 0 7px rgba(255,255,255,0.85), 0 0 40px 8px rgba(255,110,156,0.7); }
.bdg.ok .bk { stroke: #fff; }
.half { position: absolute; }

/* the content plan */
.cal { position: absolute; left: 70px; top: 300px; width: 940px; height: 820px; }
.cal .hd { position: absolute; left: 56px; top: 54px; }
.cal .dow { position: absolute; top: 150px; width: 112px; text-align: center; font-size: 24px;
  font-weight: 700; letter-spacing: 0.1em; color: rgba(23,20,28,0.62); }
.cell { position: absolute; width: 112px; height: 272px; border-radius: 30px;
  background: linear-gradient(170deg, #fdf6f6 0%, #f8e8ec 100%);
  box-shadow: inset 0 1.5px 0 rgba(255,255,255,0.9); }
.cell b { position: absolute; left: 0; right: 0; top: 18px; text-align: center; font-size: 34px;
  font-weight: 700; color: rgba(23,20,28,0.72); }
.cell.today { background: #fff; box-shadow: inset 0 0 0 5px #b4122f; }
.cell.today b { color: #b4122f; }
.rc { position: absolute; left: 14px; top: 84px; width: 84px; height: 150px; border-radius: 22px;
  background: linear-gradient(165deg, #f7c9d6 0%, #eaa8bb 100%);
  box-shadow: inset 0 1.5px 0 rgba(255,255,255,0.7); display: flex; align-items: center; justify-content: center; }
.rc svg { width: 46%; height: 46%; fill: #fff; stroke: none; }
.ring2 { position: absolute; border-radius: 34px; border: 5px solid #ff6e9c; opacity: 0; visibility: hidden; }

/* the reel card: a tall jelly tile with a play glyph */
.reel .jelly { border-radius: 52px; }
.reel .sheen { border-radius: 52px; }
.reel svg.pl { width: 44%; height: 44%; fill: url(#gw); position: relative; z-index: 1; }
""")

L = []          # html, in paint order
BEATS = []


def beat(fn):
    BEATS.append(fn)
    return fn


# --------------------------------------------------------------------------- A
# near: Instagram -> cable -> chat-bot; «перестав працювати» the cable snaps
IGX, BOTX, TY, TS = 180, 680, 180, 220
L.append('<div class="g full" id="gA">')
L.append('<div class="half" id="hA1">' + cable("cA1", "M %d %d L %d %d" % (IGX + TS - 10, TY + 110, 545, TY + 110)) + '</div>')
L.append('<div class="half" id="hA2">' + cable("cA2", "M %d %d L %d %d" % (545, TY + 110, BOTX + 10, TY + 110)) + '</div>')
L.append(tile("aIg", TS, IGX, TY, "clear", g.mark("instagram")))
L.append(tile("aBot", TS, BOTX, TY, "jelly", stroke("chat") + '<div class="dots"><i></i><i></i><i></i></div>'))
L.append(badge("aNo", BOTX + TS - 70, TY - 34, "no"))
L.append('</div>')


@beat
def b_bot():
    sfx("pop", "@bot-0.05")
    sfx("pop", "@insta-0.08", -2)
    sfx("click-soft", "@perestav")
    sfx("click", "@prats+0.02")
    return js(r"""
  tl.set("#gA", {autoAlpha: 1}, 0);
  arr("#aBot", @bot-0.1, {s: 0.5, y: 30});
  tl.fromTo("#aBot .dots i", {y: 0}, {keyframes: {y: [0, -12, 0]}, duration: 0.42, stagger: 0.1, ease: "sine.inOut"}, @bot+0.45);
  arr("#aIg", @insta-0.12, {s: 0.5, y: 30});
  draw2("cA1T", @insta+0.12, 0.3); draw2("cA1C", @insta+0.12, 0.3);
  draw2("cA2T", @insta+0.36, 0.26); draw2("cA2C", @insta+0.36, 0.26);
  G.packet("cA1P", @insta+0.5, 0.22); G.packet("cA2P", @insta+0.7, 0.2);
  /* the break: the core dies, the two halves fall apart, the bot greys */
  tl.to(["#cA1C", "#cA2C"], {opacity: 0, duration: 0.12, ease: "power2.in"}, @perestav);
  tl.to("#hA1", {x: -26, y: 14, rotation: -4, duration: 0.5, ease: SP, transformOrigin: "300px 290px"}, @perestav);
  tl.to("#hA2", {x: 26, y: 14, rotation: 4, duration: 0.5, ease: SP, transformOrigin: "800px 290px"}, @perestav);
  tl.to("#aBot", {filter: "grayscale(1) brightness(0.8)", duration: 0.3}, @perestav+0.05);
  tl.to("#aBot .dots i", {opacity: 0.25, duration: 0.2}, @perestav+0.05);
  tl.fromTo("#aNo", {autoAlpha: 0, scale: 0.3}, {autoAlpha: 1, scale: 1, duration: 0.5, ease: POP}, @prats-0.04);
  G.haptic("#aBot", @prats);
""")


# --------------------------------------------------------------------------- B
# over: the iris opens out of the dead bot onto her content plan
BOTC = (BOTX + TS // 2, TY + TS // 2)
DAYS = [28, 29, 30, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
PLANNED = {28, 30, 2, 5, 7, 9}
DOW = [u"ПН", u"ВТ", u"СР", u"ЧТ", u"ПТ", u"СБ", u"НД"]
CX0, CW, CG, RY = 56, 112, 6, (200, 494)
TODAY = (CX0 + 1 * (CW + CG), RY[0])                 # 29 Sep, a Tuesday: the day she filmed
L.append('<div class="g full" id="gB"><div class="tkg"></div>'
         '<div class="aur a1"></div><div class="aur a2"></div><div class="aur a3"></div><div class="grain"></div>')
cal = ['<div class="sheet cal hide" id="bSh"><div class="sheen"></div>',
       '<div class="hd"><div class="t-micro" style="color:rgba(23,20,28,0.62)">КОНТЕНТ-ПЛАН</div></div>']
for i, d in enumerate(DOW):
    cal.append('<div class="dow" style="left:%dpx">%s</div>' % (CX0 + i * (CW + CG), d))
for i, d in enumerate(DAYS):
    x, y = CX0 + (i % 7) * (CW + CG), RY[i // 7]
    cls = " today" if d == 29 else ""
    rc = ('<div class="rc" id="bR%d"><svg viewBox="0 0 24 24">%s</svg></div>' % (d, STROKES["play"])
          if d in PLANNED else "")
    cal.append('<div class="cell%s" id="bC%d" style="left:%dpx;top:%dpx"><b>%d</b>%s</div>' % (cls, d, x, y, d, rc))
cal.append('<div class="ring2" id="bTr" style="left:%dpx;top:%dpx;width:%dpx;height:272px"></div>'
           % (TODAY[0], TODAY[1], CW))
cal.append('</div>')
L.extend(cal)
# the unplanned reel: sized for the near beat, scaled down into the calendar
NEWW, NEWH = 210, 300
NX, NY = 70 + TODAY[0] + CW // 2 - NEWW // 2, 300 + TODAY[1] + 136 - NEWH // 2
L.append(tile("bNew", NEWH, NX, NY, "jelly", '<svg class="pl" viewBox="0 0 24 24">%s</svg>' % STROKES["play"],
              "reel", ring=True, w=NEWW))
L.append('</div>')
NEWC = (NX + NEWW // 2, NY + NEWH // 2)


@beat
def b_plan():
    sfx("whoosh-short", "@tomu-0.08")
    sfx("click-soft", "@tse+0.05", -2)
    sfx("whoosh-short", "@nezapl+0.05", -3)
    sfx("pop", "@rils")
    planned = ", ".join('"#bR%d"' % d for d in DAYS if d in PLANNED)
    return js(r"""
  tl.set("#gA", {autoAlpha: 0}, @tomu+0.6);
  G.irisOpen("#gB", @tomu-0.08, %d, %d, 0.7);
  drift1("#gB", @tomu, 4.0);
  arr("#bSh", @tomu+0.04, {s: 0.82, y: 60, d: 0.8});
  shn("#bSh .sheen", @tomu+0.3);
  tl.fromTo([%s], {autoAlpha: 0, scale: 0.4}, {autoAlpha: 1, scale: 1, duration: 0.5, ease: POP, stagger: 0.06}, @tse+0.05);
  G.ripple("#bTr", @absol+0.1);
  /* «незапланований»: a reel drops into today, tilted, too big for the cell */
  tl.set("#bNew", {autoAlpha: 1}, @nezapl);
  tl.fromTo("#bNew", {y: -700, rotation: -18, scale: 0.62, filter: "blur(10px)"},
            {y: 0, rotation: -7, scale: 0.62, filter: "blur(0px)", duration: 0.62, ease: POP}, @nezapl);
  tl.to("#bNew", {scale: 0.7, duration: 0.12, ease: "power2.out"}, @rils);
  tl.to("#bNew", {scale: 0.62, duration: 0.45, ease: SP}, @rils+0.12);
  shn("#bNew .sheen", @rils);
  tl.to(["#bC29", "#bSh"], {keyframes: {y: [0, 8, 0]}, duration: 0.3, ease: "sine.out"}, @rils);
""" % (BOTC[0], BOTC[1], planned))


# --------------------------------------------------------------------------- C
# near: the iris closes onto the new reel, which comes up above her head;
# Instagram cables into it, a packet runs, it gets the tick
RX, RY0 = 610, 150
IG2X = 200
L.append('<div class="g full" id="gC">')
L.append(cable("cC", "M %d %d L %d %d" % (IG2X + TS - 10, RY0 + 150, RX + 10, RY0 + 150)))
L.append(tile("cIg", TS, IG2X, RY0 + 40, "clear", g.mark("instagram")))
L.append(tile("cReel", NEWH, RX, RY0, "jelly", '<svg class="pl" viewBox="0 0 24 24">%s</svg>' % STROKES["play"],
              "reel", w=NEWW))
L.append(badge("cOk", RX + NEWW - 66, RY0 - 36, "ok"))
L.append('</div>')


@beat
def b_reel():
    sfx("whoosh-short", "@i-0.1", -2)
    sfx("pop", "@vvazhaiu-0.05", -2)
    sfx("click-soft", "@idealnyi")
    sfx("sparkle", "@variant-0.04")
    return js(r"""
  G.irisClose("#gB", @i-0.12, %d, %d, 0.45);
  tl.set("#gC", {autoAlpha: 1}, @i+0.2);
  tl.set("#cReel", {autoAlpha: 1}, @i+0.2);
  tl.fromTo("#cReel", {x: %d, y: %d, scale: 0.62, rotation: -7}, {x: 0, y: 0, scale: 1, rotation: 0, duration: 0.8, ease: SP}, @i+0.2);
  shn("#cReel .sheen", @zaraz+0.2);
  arr("#cIg", @vvazhaiu-0.1, {s: 0.5, x: -60, y: 20});
  draw2("cCT", @vvazhaiu+0.2, 0.32); draw2("cCC", @vvazhaiu+0.2, 0.32);
  G.packet("cCP", @idealnyi, 0.36);
  G.ripple("#cReelR", @idealnyi+0.34);
  tl.fromTo("#cOk", {autoAlpha: 0, scale: 0.3, rotation: -30}, {autoAlpha: 1, scale: 1, rotation: 0, duration: 0.55, ease: POP}, @variant-0.06);
  G.bump("#cReel", @variant);
""" % (NEWC[0], NEWC[1], NEWC[0] - (RX + NEWW // 2), NEWC[1] - (RY0 + NEWH // 2)))


# ---------------------------------------------------------------------------
HEAD_JS = r"""
  var G = helpers(tl);
  function bin(sel, t, b, d) { d = d || 0.38; G.blurIn(sel, t, b || 12, d); tl.set(sel, {filter: "none"}, t + d + 0.01); }
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
  function drift1(sel, t, d) { G.drift(sel, t, d); }
  gsap.set(".sheen", {xPercent: -120});
  gsap.set(".pkt", {autoAlpha: 0});
"""

# captions drop only where a graphic's own text says her word (STYLE.md §2b.1):
# nothing on screen says her words here, so they run the whole reel
BLACKOUT = []


def main():
    assert not NO_PAINT, "this cut has no closeups; re-check beats if it gets one"
    gj = []
    for fn in BEATS:
        gj.append("  /* %s */" % fn.__name__)
        gj.append(fn().rstrip())
    push = ["#vid"]
    head = [g.js(), HEAD_JS,
            '  gsap.set(%s, {transformOrigin: "540px 900px"});' % json.dumps(push),
            '  tl.fromTo(%s, {scale: 1}, {scale: 1.045, duration: %.3f, ease: "none"}, 0);' % (json.dumps(push), DUR)]
    doc = k.document(
        title=u"Reel 41 — незапланований рілс",
        plate="assets/base.mp4",
        gfx_html=g.defs() + "\n" + "\n".join(L),
        gfx_js="\n".join(head + gj),
        caps=CAPS,
        blackout=BLACKOUT,
    )
    io.open(os.path.join(HERE, "index.html"), "w", encoding="utf-8").write(doc)
    SFX.sort(key=lambda c: c["t"])
    io.open(os.path.join(HERE, "sfx.json"), "w", encoding="utf-8").write(json.dumps(SFX, indent=1))
    print("index.html  %d captions, %d beats, %d sfx cues (%.2f/s)" % (len(CAPS), len(BEATS), len(SFX), len(SFX) / DUR))


main()
