# -*- coding: utf-8 -*-
"""Unplanned reel (posted 2026-10-26) — «Це не запланований рілс»: how she hands 12 reels to Claude.

Unplanned, and it should look it. Her brief: *"waaaay simpler — just cut out
bad takes, pauses …, add subtitles, and maaaaybe a few logos and small
animations, but nothing crazy, very simple and effortless … a minimum of sound
effects. it has to give 'unplanned content didnt even bother to edit a lot'"*.

So none of the near -> over -> near chain the expert reels carry: no takeover,
no matte, no iris. Captions all the way, and seven small things above her head
or beside her, each on its word and gone with its sentence:

  Claude tile on «з Клодом»; a video tile drops into it on «дати їх Клоду» ->
  her gallery screenshot (the 12 hearted takes, her own phone) in her raised
  hand from «12 нових рілсів», a heart on «сердечком» -> Drive on «диск»
  -> a cloud on «в хмарі» -> Drive again on «Google Диск» -> [her screen, as
  filmed] -> a clock that spins on «почекати 2-3 годинки» -> Edits on «Edits»
  -> the comment box types «+» on «пиши плюс».

Cut by hand in work/unplanned/edit.py (no app script for tools/cut.py).

usage: python build.py   (then: python ../tools/sfx.py mix unplanned)

Named, not numbered: it was built as «reel 41» on its own branch, and main's
reel 41 is «Не просто промти».
"""
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))
# built in refined glass before §00; that kit is archived (archive/README.md)
sys.path.insert(0, os.path.join(ROOT, "archive", "tools"))
from kit import Kit  # noqa: E402
import glass  # noqa: E402
from glass import Glass  # noqa: E402
glass.ICONS = os.path.join(ROOT, "assets", "icons")   # the archived kit looks beside itself

CUT = json.load(io.open(os.path.join(ROOT, "work", "unplanned", "cut.json"), encoding="utf-8"))
DUR = 71.783           # (2154 plate frames - 0.5) / 30
FPS = 30
k = Kit(width=1080, height=1920, fps=FPS, duration=DUR)
g = Glass(["claude", "googledrive"])
k.css(g.css())

NO_PAINT = [tuple(x) for x in CUT["no_paint"]]   # the «Це настільки просто» closeup

CAPS = k.load_captions(os.path.join(ROOT, "work", "unplanned", "captions.json"))
# whisper errors align.py kept as "she improvised" -> what she said
FIX = {u"з сердечком.": u"сердечком.", u"дистопі,": u"десктопі,", u"ті": u"ці", u"рюси.": u"рілси.",
       u"тієї": u"цієї", u"CD": u"сюди", u"від мене": u"він в мене", u"Дайте": u"дати"}
for c in CAPS:
    c["w"] = FIX.get(c["w"], c["w"])
for _a, _b in zip(CAPS, CAPS[1:]):
    _a["e"] = round(max(_a["s"] + 0.10, _b["s"] - 0.085), 3)


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
    "klodom": S(u"Клодом", 4.00), "video": S(u"відео", 6.60), "dati": S(u"дати", 7.42),
    "klodu": S(u"Клоду", 7.78), "tomu": S(u"Тому", 8.40),
    "rilsiv": S(u"рілсів", 11.96), "halerei": S(u"галереї", 13.30), "serd": S(u"сердечком", 14.54), "pershe": S(u"Перше", 15.53),
    "dysk": S(u"диск", 17.74), "naspr": S(u"Насправді", 18.17),
    "khmari": S(u"хмарі", 25.52), "komp": S(u"комп'ютер", 26.62),
    "google": S(u"Google", 34.00), "u": S(u"У", 34.81),
    "pochek": S(u"почекати", 47.19), "hod23": S("2-3", 47.77), "poky": S(u"поки", 48.57),
    "ed1": S(u"Edits", 59.58), "ed1e": E(u"Edits", 59.58), "ed2": S(u"Edits", 61.20),
    "ed2e": E(u"Edits", 61.20), "tomu2": S(u"Тому", 61.84),
    "pyshy": S(u"пиши", 70.31), "plius": S(u"плюс", 70.59), "pliuse": E(u"плюс", 70.59),
    "koment": S(u"коментарі", 70.89),
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
    "play": '<path d="M9 6.8v10.4l8.2-5.2z" fill="url(#gw)" stroke="none"/>',
    "cloud": '<path d="M7.2 18.5h10.2a4 4 0 0 0 .5-7.97A5.6 5.6 0 0 0 7.1 9.3a4.6 4.6 0 0 0 .1 9.2z"/>',
    "clock": '<circle cx="12" cy="12" r="8.6"/>',
    "send": '<path d="M5 12h13M12.6 6.4 18.2 12l-5.6 5.6"/>',
}
HEART = ('<svg viewBox="0 0 24 24"><defs><linearGradient id="hg" x1="0" y1="0" x2="0.4" y2="1">'
         '<stop offset="0" stop-color="#ff8ab0"/><stop offset="0.55" stop-color="#e0204b"/>'
         '<stop offset="1" stop-color="#a50f2b"/></linearGradient></defs>'
         '<path fill="url(#hg)" d="M12 20.6 10.6 19.3C5.6 14.8 2.4 11.9 2.4 8.3 2.4 5.4 4.7 3.1 7.6 3.1'
         'c1.6 0 3.2.8 4.4 2 1.2-1.2 2.8-2 4.4-2 2.9 0 5.2 2.3 5.2 5.2 0 3.6-3.2 6.5-8.2 11z"/></svg>')


def stroke(name, cls="sk"):
    return '<svg class="%s" viewBox="0 0 24 24">%s</svg>' % (cls, STROKES[name])


def tile(tid, size, x, y, material, inner, extra_cls="", ring=True, extra=""):
    r = ('<div class="sqring" id="%sR" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx"></div>'
         % (tid, x, y, size, size)) if ring else ""
    return ('%s<div class="tw hide %s" id="%s" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx">'
            '<div class="%s">%s<div class="sheen"></div></div>%s</div>'
            % (r, extra_cls, tid, x, y, size, size, material, inner, extra))


k.css("""
.abs { position: absolute; }
.hide { opacity: 0; visibility: hidden; }
.tw { position: absolute; }
.sk { fill: none; stroke: url(#gw); stroke-width: 2.3; stroke-linecap: round; stroke-linejoin: round;
  width: 50%; height: 50%; position: relative; z-index: 1; overflow: visible; }
.clear { overflow: hidden; }
.pearl .wmark { font-size: 50px; }

/* the clock's hands spin about the dial's centre */
.hand { position: absolute; left: 50%; bottom: 50%; width: 7px; margin-left: -3.5px; border-radius: 4px;
  background: #fff; transform-origin: 50% 100%; z-index: 2; }
.hand.h { height: 22px; } .hand.m { height: 32px; background: #ffd6e3; }
.pin { position: absolute; left: 50%; top: 50%; width: 12px; height: 12px; margin: -6px 0 0 -6px;
  border-radius: 50%; background: #fff; z-index: 3; }

/* her gallery screenshot, as a photo from her phone */
.gal { position: absolute; left: 619px; top: 370px; width: 372px; height: 659px; border-radius: 44px;
  overflow: hidden; background: #fff;
  box-shadow: 0 0 0 6px rgba(255,255,255,0.95), 0 44px 80px -26px rgba(24,4,12,0.62); }
.gal img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }
.gal .sheen { mix-blend-mode: normal; opacity: 0.45; }
.heart { position: absolute; width: 132px; height: 132px; filter: var(--glow); }
.heart svg { width: 100%; height: 100%; }

/* the Instagram comment box */
.cm { position: absolute; left: 150px; top: 130px; width: 780px; height: 132px; border-radius: 66px; }
.cm .av { position: absolute; left: 22px; top: 22px; width: 88px; height: 88px; border-radius: 50%;
  background: linear-gradient(160deg, #ff8ab0 0%, #e0204b 55%, #8d0d24 100%);
  box-shadow: inset 0 2px 1px rgba(255,255,255,0.5); }
.cm .ph { position: absolute; left: 136px; top: 0; height: 132px; line-height: 132px; font-size: 38px;
  font-weight: 500; color: rgba(255,255,255,0.55); white-space: nowrap; }
.cm .plus { position: absolute; left: 132px; top: 0; height: 132px; line-height: 128px; font-size: 92px;
  font-weight: 900; color: #fff; }
.cm .cur { position: absolute; left: 136px; top: 40px; width: 5px; height: 52px; border-radius: 3px;
  background: #ff8ab0; }
.cm .snd { position: absolute; right: 22px; top: 22px; width: 88px; height: 88px; border-radius: 50%;
  background: rgba(255,255,255,0.16); display: flex; align-items: center; justify-content: center; }
.cm .snd .sk { width: 52%; height: 52%; stroke: #fff; stroke-width: 2.6; }
.cm .snd .on { position: absolute; inset: 0; border-radius: 50%; opacity: 0; visibility: hidden;
  background: linear-gradient(165deg, #ff6e9c 0%, #e0204b 55%, #8d0d24 100%); }
""")

L = []
BEATS = []


def beat(fn):
    BEATS.append(fn)
    return fn


# ===========================================================================
# 1 · «з Клодом» … «взяти відео і дати їх Клоду»: a video tile drops into Claude
@beat
def b1_claude():
    L.append('<div class="g full" id="g1">'
             + tile("cl", 180, 450, 104, "jelly", g.mark("claude"))
             + tile("vd", 128, 196, 130, "clear", stroke("play"), ring=False)
             + '</div>')
    sfx("pop", "@klodom+0.02")
    sfx("click-soft", "@klodu+0.12")
    return js("""
  tl.set("#g1", {autoAlpha: 1}, @klodom-0.1);
  arr("#cl", @klodom-0.04, {s: 0.4, y: -30});
  G.ripple("#clR", @klodom+0.3);
  arr("#vd", @video-0.04, {s: 0.4, x: -30, y: 10, d: 0.7});
  tl.to("#vd", {x: 280, y: -2, scale: 0.35, duration: 0.42, ease: "power3.in"}, @dati+0.05);
  tl.to("#vd", {autoAlpha: 0, duration: 0.08}, @dati+0.42);
  G.bump("#cl", @klodu+0.08);
  G.ripple("#clR", @klodu+0.1);
  bout("#cl", @tomu-0.05, 10, 0.3);
  tl.set("#g1", {autoAlpha: 0}, @tomu+0.3);
""")


# 2 · «12 нових рілсів. Ось вони в мене в галереї, я їх відмітила сердечком»: her
# screenshot, in her raised hand — size, angle and 0:12 arrival from her review
@beat
def b2_gallery():
    L.append('<div class="g full" id="g2">'
             '<div class="gal hide" id="gal"><img src="assets/gallery.jpg" alt=""><div class="sheen"></div></div>'
             '<div class="heart hide" id="ht" style="left:624px;top:274px">' + HEART + '</div>'
             '</div>')
    sfx("pop", "@rilsiv")
    sfx("click-soft", "@serd+0.04")
    return js("""
  tl.set("#g2", {autoAlpha: 1}, @rilsiv-0.15);
  gsap.set("#gal", {rotation: 13, transformOrigin: "50% 50%"});
  gsap.set("#ht", {rotation: -12});
  arr("#gal", @rilsiv-0.06, {s: 0.45, x: 20, y: 40, d: 0.8});
  shn("#gal .sheen", @rilsiv+0.3);
  tl.fromTo("#ht", {autoAlpha: 0, scale: 0}, {autoAlpha: 1, scale: 1, duration: 0.6, ease: POP}, @serd);
  tl.to("#ht", {scale: 1.14, duration: 0.12, ease: "power2.out"}, @serd+0.62);
  tl.to("#ht", {scale: 1, duration: 0.4, ease: SP}, @serd+0.74);
  bout(["#gal", "#ht"], @pershe-0.3, 10, 0.28);
  tl.set("#g2", {autoAlpha: 0}, @pershe+0.05);
""")


# 3 · «завантажити їх на диск»
@beat
def b3_drive():
    L.append('<div class="g full" id="g3">' + tile("dr", 180, 450, 92, "clear", g.mark("googledrive"))
             + '</div>')
    sfx("pop", "@dysk", -1)
    return js("""
  tl.set("#g3", {autoAlpha: 1}, @dysk-0.1);
  arr("#dr", @dysk-0.06, {s: 0.4, y: -30});
  G.ripple("#drR", @dysk+0.3);
  bout("#dr", @naspr+0.5, 10, 0.3);
  tl.set("#g3", {autoAlpha: 0}, @naspr+0.85);
""")


# 4 · «Але я люблю робити все в хмарі»
@beat
def b4_cloud():
    L.append('<div class="g full" id="g4">' + tile("cd", 180, 450, 100, "clear", stroke("cloud")) + '</div>')
    return js("""
  tl.set("#g4", {autoAlpha: 1}, @khmari-0.1);
  arr("#cd", @khmari-0.06, {s: 0.4, y: -30});
  tl.to("#cd", {y: -10, duration: 0.9, ease: "sine.inOut"}, @khmari+0.6);
  bout("#cd", @komp+0.15, 10, 0.3);
  tl.set("#g4", {autoAlpha: 0}, @komp+0.5);
""")


# 5 · «завантажу їх на Google Диск» — and the cut lands on Drive itself
@beat
def b5_drive2():
    L.append('<div class="g full" id="g5">' + tile("dr2", 180, 450, 92, "clear", g.mark("googledrive"))
             + '</div>')
    return js("""
  tl.set("#g5", {autoAlpha: 1}, @google-0.1);
  arr("#dr2", @google-0.06, {s: 0.4, y: -30});
  G.ripple("#dr2R", @google+0.3);
  bout("#dr2", @u+0.12, 10, 0.28);
  tl.set("#g5", {autoAlpha: 0}, @u+0.45);
""")


# 6 · «почекати 2-3 годинки»: the clock runs
@beat
def b6_clock():
    L.append('<div class="g full" id="g6">'
             + tile("ck", 180, 450, 100, "clear",
                    stroke("clock") + '<i class="hand h" id="ckH"></i><i class="hand m" id="ckM"></i><i class="pin"></i>')
             + '</div>')
    return js("""
  tl.set("#g6", {autoAlpha: 1}, @pochek-0.1);
  arr("#ck", @pochek-0.06, {s: 0.4, y: -30});
  tl.fromTo("#ckM", {rotation: 0}, {rotation: 1080, duration: 1.6, ease: "power2.inOut"}, @hod23-0.2);
  tl.fromTo("#ckH", {rotation: 90}, {rotation: 180, duration: 1.6, ease: "power2.inOut"}, @hod23-0.2);
  bout("#ck", @poky+0.45, 10, 0.3);
  tl.set("#g6", {autoAlpha: 0}, @poky+0.8);
""")


# 7 · «додати в Edits і запостити вже з Edits» — no icon exists, so the wordmark
@beat
def b7_edits():
    L.append('<div class="g full" id="g7">'
             + tile("ed", 180, 450, 112, "pearl", g.wordmark("Edits", size=50))
             + '</div>')
    sfx("pop", "@ed1", -1)
    return js("""
  tl.set("#g7", {autoAlpha: 1}, @ed1-0.1);
  arr("#ed", @ed1-0.06, {s: 0.4, y: -30});
  G.ripple("#edR", @ed1+0.3);
  G.bump("#ed", @ed2);
  G.ripple("#edR", @ed2+0.05);
  bout("#ed", @tomu2-0.32, 10, 0.26);
  tl.set("#g7", {autoAlpha: 0}, @tomu2);
""")


# 8 · «то пиши плюс в коментарі»: the comment box types «+»
@beat
def b8_comment():
    L.append('<div class="g full" id="g8"><div class="cm dglass edge hide" id="cm">'
             '<div class="av"></div><div class="ph" id="cmPh">Додайте коментар…</div>'
             '<div class="cur" id="cmCur"></div><div class="plus hide" id="cmPl">+</div>'
             '<div class="snd"><div class="on" id="cmOn"></div>' + stroke("send") + '</div>'
             '</div></div>')
    sfx("click-soft", "@plius+0.02")
    return js("""
  tl.set("#g8", {autoAlpha: 1}, @pyshy-0.15);
  arr("#cm", @pyshy-0.1, {s: 0.7, y: -24, d: 0.7});
  tl.set("#cmPh", {autoAlpha: 0}, @plius);
  tl.set("#cmPl", {autoAlpha: 1}, @plius);
  tl.fromTo("#cmPl", {scale: 0.4}, {scale: 1, duration: 0.4, ease: POP}, @plius);
  tl.set("#cmCur", {x: 62}, @plius);
  tl.to("#cmCur", {keyframes: {opacity: [1, 0, 0, 1, 1, 0, 0, 1]}, duration: 1.2, ease: "none"}, @pyshy);
  tl.to("#cmOn", {autoAlpha: 1, duration: 0.2}, @koment+0.1);
  G.bump("#cm .snd", @koment+0.1);
""")


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
  function shn(sel, t) {
    gsap.set(sel, {xPercent: -120});
    tl.fromTo(sel, {xPercent: -120}, {xPercent: 120, duration: 0.8, ease: "power2.inOut", immediateRender: false}, t);
  }
  gsap.set(".sheen", {xPercent: -120});
"""


def span_words(a, b):
    return (round(a - 0.02, 3), round(b, 3), "")


# captions that would repeat the graphic's own words (STYLE.md §2b.1)
BLACKOUT = [
    span_words(T["ed1"], T["ed1e"]),          # the Edits wordmark
    span_words(T["ed2"], T["ed2e"]),
    span_words(T["plius"], T["pliuse"]),      # the «+» typed in the comment box
]


def main():
    gj = []
    for fn in BEATS:
        j = fn()
        gj.append("  /* %s */" % fn.__name__)
        gj.append(j.rstrip())
    push = ["#vid"]
    head = [g.js(), HEAD_JS,
            '  gsap.set(%s, {transformOrigin: "540px 900px"});' % json.dumps(push),
            '  tl.fromTo(%s, {scale: 1}, {scale: 1.045, duration: %.3f, ease: "none"}, 0);' % (json.dumps(push), DUR)]
    doc = k.document(
        title=u"Не запланований рілс",
        plate="assets/base.mp4",
        gfx_html=g.defs() + "\n" + "\n".join(L),
        gfx_js="\n".join(head + gj),
        caps=CAPS,
        blackout=BLACKOUT,
    )
    io.open(os.path.join(HERE, "index.html"), "w", encoding="utf-8").write(doc)
    SFX.sort(key=lambda c: c["t"])
    io.open(os.path.join(HERE, "sfx.json"), "w", encoding="utf-8").write(json.dumps(SFX, indent=1))
    print("index.html  %d captions, %d beats, %d sfx cues" % (len(CAPS), len(BEATS), len(SFX)))


main()
