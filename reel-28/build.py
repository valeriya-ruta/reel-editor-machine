# -*- coding: utf-8 -*-
"""Reel 28 — «Мені в дірект… на який суфлер я записую свої рілси». Posts 2026-10-10.

A show-and-tell about how she records, so it stays close to her vlog style
(memory: vlog reels stay natural): her footage in front, captions on, and a
handful of clean near touches — no takeover, no matte.

The one big moment is HER ask: *"cut out this popup of the notes and put them
right on top of me but half transparent — its to show them what i actually see
when i record (which is not much lol)"*. Her real Samsung Notes popup
(assets/notes-popup.png) arrives small above her head on «нотатки», the text is
pasted in, and on «накладаю зверху на камеру» it drops over her face at ~50 %,
scrolling slowly while she explains; a fainter callback on «що я зараз читаю з
суфлера».

Chain:  near: two DM notifications land (two strangers, same question), more
stack up on «багатьох» -> two tiles 1 / 2, both «0 грн», then a desk and a
window chip («де я знімаю») -> tile 1 flips into Edits and opens into its
teleprompter (camera, text pasted, size + speed sliders, the text scrolls) ->
the card folds back into the tile, which docks in a shelf: desk chip, background
blur OFF -> window chip, blur ON, Edits gets an ✕ -> the Notes popup lands above
her and is laid over her face (front camera, portrait-video mode strip; an
eye-level line) -> her closeup left clear -> the popup again, faint -> Стежити.

usage: python build.py   (then: python ../tools/sfx.py mix 28)
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

CUT = json.load(io.open(os.path.join(ROOT, "work", "r28", "cut.json"), encoding="utf-8"))
DUR = 79.883           # (plate frames - 0.5) / 30
FPS = 30
k = Kit(width=1080, height=1920, fps=FPS, duration=DUR)
g = Glass(["instagram"])
k.css(g.css())

# ---------------------------------------------------------------------------
# NO-PAINT: her closeup «Не треба собі ускладнювати життя…». Captions only.
NO_PAINT = [tuple(x) for x in CUT["no_paint"]]

CAPS = k.load_captions(os.path.join(ROOT, "work", "r28", "captions.json"))
# whisper errors the aligner kept as "her wording" -> what she said / the script
FIX = {u"вдірок": u"в дірект", u"спортомнєвну": u"з портретним", u"софлера,": u"з суфлера,"}
FIX_AT = {74.87: u"ви"}          # «Якщо ти не знали» -> «Якщо ви не знали»
for c in CAPS:
    c["w"] = FIX.get(c["w"], c["w"])
    for t, w in FIX_AT.items():
        if abs(c["s"] - t) < 0.02:
            c["w"] = w
for _a, _b in zip(CAPS, CAPS[1:]):
    _a["e"] = round(max(_a["s"] + 0.10, _b["s"] - 0.085), 3)


def _n(s):
    return "".join(ch for ch in s.lower() if ch.isalnum())


def S(word, near):
    hits = [c for c in CAPS if _n(word) in [_n(x) for x in c["w"].split()]]
    c = min(hits, key=lambda c: abs(c["s"] - near))
    assert abs(c["s"] - near) < 0.6, (word, near, c["s"])
    return c["s"]


def E(word, near):
    hits = [c for c in CAPS if _n(word) in [_n(x) for x in c["w"].split()]]
    return min(hits, key=lambda c: abs(c["s"] - near))["e"]


T = {
    # A
    "dirkt": S(u"дірект", 0.35), "dvoie": S(u"двоє", 1.77), "odnym": S(u"одним", 3.87),
    "neznai": S(u"незнайомих", 2.21), "sufler": S(u"суфлер", 6.03), "bahatokh": S(u"багатьох", 9.09),
    "bahatokhe": E(u"багатьох", 9.09),
    # B
    "u": S(u"У", 10.03), "dva": S(u"два", 10.37), "varianty": S(u"варіанти", 10.67),
    "bezkosht": S(u"безкоштовні", 12.09), "de": S(u"де", 14.90), "pershyi": S(u"Перший", 16.62),
    # C
    "instagramu": S(u"Інстаграму", 17.90), "edits1": S("Edits", 18.72), "edits1e": E("Edits", 18.72),
    "tam": S(u"Там", 19.23), "kamera": S(u"камера", 19.84), "sufler2": S(u"суфлер", 20.54),
    "vstavl": S(u"вставляєш", 22.02), "nalasht": S(u"налаштовуєш", 22.78), "rozmir": S(u"розмір", 23.48),
    "shvydk": S(u"швидкість", 23.78), "shvydke": E(u"швидкість", 23.78), "chytaiesh": S(u"читаєш", 24.52),
    "ya": S(u"Я", 25.17),
    # D / E
    "robochoho": S(u"робочого", 27.01), "stola": S(u"стола", 27.53), "stolae": E(u"стола", 27.53),
    "ne": S(u"не", 29.58), "rozmyvaty": S(u"розмивати", 29.96), "fon1e": E(u"фон", 30.52),
    "ale": S(u"Але", 30.97), "vikna": S(u"вікна", 34.15), "viknae": E(u"вікна", 34.15),
    "zablur": S(u"заблюрити", 36.21), "fon2": S(u"фон", 37.21), "fon2e": E(u"фон", 37.21),
    "edits2": S("Edits", 37.96), "edits2e": E("Edits", 37.96), "pidkhodyt": S(u"підходить", 38.50),
    "todi": S(u"Тоді", 39.35),
    # F
    "notatky": S(u"нотатки", 41.05), "vstavliaiu": S(u"вставляю", 42.43), "vstavliaiue": E(u"вставляю", 42.43),
    "nakladaiu": S(u"накладаю", 43.93), "kameru2": S(u"камеру", 46.36), "frontal": S(u"фронтальну", 47.26),
    "portret": S(u"портретним", 47.68), "videoe": E(u"відео", 48.28), "mene": S(u"мене", 50.60),
    "rivni": S(u"рівні", 56.48), "ochei": S(u"очей", 56.98),
    "kudy": S(u"куди", 60.62), "vzahali": S(u"взагалі", 62.54), "tomu": S(u"Тому", 63.66),
    # G / H
    "yakshcho": S(u"Якщо", 74.35), "sufl3e": E(u"суфлера", 77.40), "to": S(u"то", 78.20),
    "pidpysh": S(u"підпишись", 79.02),
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
# Sound design (tools/sfx.py). Quiet, on the event, never on her joke.
SFX = []


def sfx(name, t, db=0):
    if isinstance(t, str):
        t = float(js(t))
    SFX.append({"t": round(max(0.0, t), 3), "name": name, "db": db})


# ---------------------------------------------------------------------------
# Glyphs
STROKES = {
    "person": '<circle cx="12" cy="8.2" r="3.6"/><path d="M4.8 20c.9-3.8 3.7-5.8 7.2-5.8s6.3 2 7.2 5.8"/>',
    "check": '<path d="M5.4 12.6l4.3 4.3 8.9-9.5"/>',
    "camera": '<path d="M3.6 8.6a2 2 0 0 1 2-2h2.3l1.6-2.2h5l1.6 2.2h2.3a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2H5.6a2 2 0 0 1-2-2z"/>'
              '<circle cx="12" cy="12.8" r="3.5"/>',
    "desk": '<rect x="5.2" y="4.6" width="13.6" height="9.4" rx="1.6"/><path d="M12 14v3.2M2.6 17.6h18.8M5 17.6v3M19 17.6v3"/>',
    "window": '<rect x="4.4" y="3.4" width="15.2" height="17.2" rx="1.6"/><path d="M12 3.4v17.2M4.4 12h15.2"/>',
    "flip": '<path d="M4.6 10.2A7.6 7.6 0 0 1 18.2 7.4M19.4 13.8A7.6 7.6 0 0 1 5.8 16.6"/>'
            '<path d="M18.6 3.6v4.2h-4.2M5.4 20.4v-4.2h4.2"/>',
    "eye": '<path d="M2.4 12s3.6-6.4 9.6-6.4 9.6 6.4 9.6 6.4-3.6 6.4-9.6 6.4S2.4 12 2.4 12z"/><circle cx="12" cy="12" r="3.1"/>',
    "x": '<path d="M7.2 7.2l9.6 9.6M16.8 7.2l-9.6 9.6"/>',
}


def stroke(name, cls="sk"):
    return '<svg class="%s" viewBox="0 0 24 24">%s</svg>' % (cls, STROKES[name])


def tile(tid, size, x, y, material, inner, extra_cls="", hide=True, ring=True):
    r = ('<div class="sqring" id="%sR" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx"></div>'
         % (tid, x, y, size, size)) if ring else ""
    return ('%s<div class="tw%s %s" id="%s" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx">'
            '<div class="%s">%s<div class="sheen"></div></div></div>'
            % (r, " hide" if hide else "", extra_cls, tid, x, y, size, size, material, inner))


k.css("""
.abs { position: absolute; }
.hide { opacity: 0; visibility: hidden; }
.tw { position: absolute; }
.sk { fill: none; stroke: url(#gw); stroke-width: 2.3; stroke-linecap: round; stroke-linejoin: round;
  width: 50%; height: 50%; position: relative; z-index: 1; overflow: visible; }
.pearl .sk { stroke: #17141c; }
.clear { overflow: hidden; }
.circ .jelly, .circ .pearl, .circ .clear, .circ .sheen, .circ .sqring { border-radius: 50%; }
.shc { position: absolute; inset: 0; border-radius: inherit; overflow: hidden; pointer-events: none; }
.shc .sheen { mix-blend-mode: normal; opacity: 0.4; }

/* A · her two real DM screenshots */
.shot { position: absolute; border-radius: 44px; overflow: hidden; background: #fff;
  box-shadow: inset 0 0 0 1px rgba(255,255,255,0.6), 0 44px 90px -30px rgba(10,0,4,0.62), 0 3px 10px rgba(10,0,4,0.18); }
.shot img { position: absolute; left: 0; top: 0; width: 100%; height: 100%; display: block; }
.shot .hl { position: absolute; display: block; border-radius: 12px; background: rgba(255,110,156,0.42);
  mix-blend-mode: multiply; transform-origin: 0 50%; transform: scaleX(0); }
.shot .sheen { mix-blend-mode: normal; opacity: 0.35; }

/* B · two options */
.num { font-size: 150px; padding-right: 0; position: relative; z-index: 1; }
.chp { position: absolute; height: 84px; border-radius: 42px; overflow: hidden;
  background: linear-gradient(160deg, #ffffff 0%, #fff5f8 52%, #f5dfe6 100%);
  box-shadow: inset 0 2px 1px #fff, 0 26px 50px -20px rgba(8,0,3,0.6); }
.chp .cf { position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; gap: 12px;
  color: #17141c; font-size: 38px; font-weight: 700; letter-spacing: -0.01em; }
.chp .cf b { font-weight: 900; color: #b4122f; }
.chp .sk { width: 46px; height: 46px; stroke: #17141c; stroke-width: 2.1; }

/* C · the Edits teleprompter */
.tp { position: absolute; left: 40px; top: 128px; width: 820px; height: 196px; border-radius: 30px; overflow: hidden;
  background: rgba(8,2,5,0.34); box-shadow: inset 0 0 0 1.5px rgba(255,255,255,0.10); }
.tpx { position: absolute; left: 30px; top: 22px; width: 640px; font-size: 38px; font-weight: 700; line-height: 1.32;
  color: #fff; transform-origin: 0 0; letter-spacing: -0.005em; }
.tpc { position: absolute; left: 30px; top: 28px; width: 4px; height: 44px; background: #ff8ab0; }
.sl { position: absolute; left: 40px; width: 820px; height: 56px; }
.sl .lb { position: absolute; left: 0; top: 7px; font-size: 30px; font-weight: 700; color: rgba(255,255,255,0.8); }
.sl .tr, .sl .fi { position: absolute; left: 230px; top: 23px; width: 560px; height: 10px; border-radius: 5px; }
.sl .tr { background: rgba(255,255,255,0.22); }
.sl .fi { background: linear-gradient(90deg, #ff8ab0, #ff6e9c); transform-origin: 0 50%; }
.sl .kn { position: absolute; left: 210px; top: 8px; width: 40px; height: 40px; border-radius: 50%;
  background: linear-gradient(165deg, #ffffff, #f5dfe6); box-shadow: 0 6px 14px rgba(10,0,4,0.45); }

/* D · the blur switch */
.swl { position: absolute; font-size: 32px; font-weight: 700; color: #fff; letter-spacing: -0.01em; white-space: nowrap; }
.sw { position: absolute; width: 124px; height: 70px; border-radius: 35px; background: rgba(255,255,255,0.22);
  box-shadow: inset 0 0 0 2px rgba(255,255,255,0.25); }
.sw .on { position: absolute; inset: 0; border-radius: 35px;
  background: linear-gradient(165deg, #ff6e9c 0%, #e0204b 55%, #ab112e 100%);
  box-shadow: 0 0 30px rgba(255,110,156,0.6); opacity: 0; visibility: hidden; }
.sw .kb { position: absolute; left: 7px; top: 7px; width: 56px; height: 56px; border-radius: 50%;
  background: linear-gradient(165deg, #ffffff, #f3e4e9); box-shadow: 0 6px 14px rgba(10,0,4,0.4); }
.xb .sk { stroke: #b4122f; stroke-width: 3.2; }

/* F · her Notes popup, laid over the camera */
.np { position: absolute; inset: 0; border-radius: 36px; overflow: hidden; background: #fcfcfc;
  box-shadow: 0 40px 90px -30px rgba(10,0,4,0.45); }
.nph { position: absolute; left: 0; top: 0; width: 880px; height: 194px; overflow: hidden; }
.npb { position: absolute; left: 0; top: 194px; width: 880px; height: 726px; overflow: hidden; }
.np img { position: absolute; left: 0; top: 0; width: 880px; height: auto; display: block; }
.npc { position: absolute; left: 0; top: 196px; width: 880px; height: 724px; background: #fcfcfc; }
.pst { position: absolute; height: 80px; padding: 0 36px; border-radius: 40px; white-space: nowrap;
  background: linear-gradient(165deg, #2c2730 0%, #17141c 100%); color: #fff; font-size: 33px; font-weight: 700;
  line-height: 80px; box-shadow: 0 22px 44px -14px rgba(0,0,0,0.6), inset 0 1.5px 0 rgba(255,255,255,0.16); }
.mw { position: absolute; left: 130px; top: 0; width: 750px; height: 124px; overflow: hidden; }
.ms { position: absolute; left: 0; top: 0; height: 124px; width: 900px; }
.ml { position: absolute; top: 0; height: 116px; line-height: 116px; text-align: center; font-size: 31px; font-weight: 700;
  letter-spacing: 0.05em; color: rgba(255,255,255,0.5); white-space: nowrap; }
.mdot { position: absolute; left: 369px; top: 96px; width: 12px; height: 12px; border-radius: 50%; background: #ff6e9c;
  box-shadow: 0 0 12px rgba(255,110,156,0.9); }
.eyl { fill: none; stroke: #ff8ab0; stroke-width: 8; stroke-linecap: round; stroke-dasharray: 22 18; }
.eyw { position: absolute; filter: drop-shadow(0 0 8px rgba(255,110,156,0.9)); }

/* H · follow */
.fl { position: absolute; border-radius: 80px; overflow: hidden;
  background: linear-gradient(160deg, #ffffff 0%, #fff5f8 52%, #f5dfe6 100%);
  box-shadow: inset 0 2px 1px #fff, 0 40px 80px -28px rgba(30,4,12,0.65); }
.fl .t { position: absolute; left: 160px; top: 0; height: 150px; line-height: 150px; font-size: 56px; font-weight: 700;
  letter-spacing: -0.02em; color: #17141c; }
.fl .on { position: absolute; inset: 0; background: linear-gradient(165deg, #e0204b 0%, #ab112e 46%, #6b081c 100%);
  opacity: 0; visibility: hidden; }
.fl .on .t { color: #fff; left: 150px; }
.ck { position: absolute; width: 120px; height: 120px; margin: -60px 0 0 -60px; border-radius: 50%;
  border: 7px solid #ff6e9c; opacity: 0; visibility: hidden; z-index: 5; }
""")

L = []
BEATS = []


def beat(fn):
    BEATS.append(fn)
    return fn


# ===========================================================================
# A · two strangers, the same question, in DMs — her real screenshots
#     (STYLE.md: proof is a screenshot; animate around it, never retype it)
DMS = [("dm1", "proof-dm1.jpg", 903, 225, 100, (194, 399)),     # «…яким суфлером ви користуєтесь?»
       ("dm2", "proof-dm2.jpg", 938, 278, 345, (346, 493))]     # «…який суфлер для запису рілсів…»


@beat
def a_dms():
    cards = ""
    for did, src, w, h, y, (h0, h1) in DMS:
        cards += ('<div class="shot hide" id="%s" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx">'
                  '<img src="assets/%s" alt=""><i class="hl" id="%sH" style="left:%dpx;top:111px;width:%dpx;height:54px"></i>'
                  '<div class="shc"><div class="sheen"></div></div></div>'
                  % (did, (1080 - w) // 2, y, w, h, src, did, h0 - 10, h1 - h0 + 20))
    L.append('<div class="g full" id="gA">' + cards + '</div>')
    sfx("notification", T["dvoie"] + 0.1)
    sfx("notification", T["neznai"] + 0.3, -2)
    sfx("pop", T["odnym"] + 0.02, -5)
    sfx("click-soft", T["sufler"] + 0.05, -2)
    return js("""
  tl.set("#gA", {autoAlpha: 1}, @dvoie-0.2);
  arr("#dm1", @dvoie-0.06, {s: 0.82, y: -60, d: 0.8, ease: SOFT});
  arr("#dm2", @neznai+0.15, {s: 0.82, y: -60, d: 0.8, ease: SOFT});
  /* the same question: both land together again */
  G.bump("#dm1", @odnym); G.bump("#dm2", @odnym);
  shn("#dm1 .sheen", @odnym+0.05); shn("#dm2 .sheen", @odnym+0.05);
  /* «на який суфлер»: the word gets marked in both */
  tl.fromTo(["#dm1H", "#dm2H"], {scaleX: 0}, {scaleX: 1, duration: 0.45, ease: "power2.out", stagger: 0.08}, @sufler+0.02);
  bout("#gA", @bahatokhe-0.22, 10, 0.26);""")


# ===========================================================================
# B · two options, both free, it depends where she films
def chip(cid, x, y, w, faces):
    inner = "".join('<div class="cf%s" id="%s%d">%s</div>' % ("" if i == 0 else " hide", cid, i, f)
                    for i, f in enumerate(faces))
    return '<div class="chp hide" id="%s" style="left:%dpx;top:%dpx;width:%dpx">%s</div>' % (cid, x, y, w, inner)


DESK = stroke("desk") + u"стіл"
WINDOW = stroke("window") + u"вікно"


@beat
def b_options():
    L.append('<div class="g full" id="gB">'
             + tile("t2", 220, 610, 150, "pearl", '<span class="t-big num">2</span>')
             + chip("c1", 250, 400, 220, [u"<b>0</b>&nbsp;грн", DESK])
             + chip("c2", 610, 400, 220, [u"<b>0</b>&nbsp;грн", WINDOW])
             + '</div>')
    sfx("pop", T["dva"] + 0.02)
    sfx("pop", T["varianty"] + 0.05, -2)
    sfx("click-soft", T["bezkosht"] + 0.05)
    sfx("click-soft", T["de"] + 0.05, -1)
    return js("""
  tl.set("#gB", {autoAlpha: 1}, @dva-0.1);
  arr("#t2", @varianty+0.02, {s: 0.4, y: 30});
  G.ripple("#t2R", @varianty+0.3);
  arr("#c1", @bezkosht-0.04, {s: 0.5, y: 20, d: 0.7});
  arr("#c2", @bezkosht+0.08, {s: 0.5, y: 20, d: 0.7});
  [["#c1", 0], ["#c2", 0.1]].forEach(function (p) {
    var t = @de+p[1];
    tl.to(p[0], {scaleY: 0, duration: 0.13, ease: "power2.in"}, t);
    tl.set(p[0] + "0", {autoAlpha: 0}, t + 0.13); tl.set(p[0] + "1", {autoAlpha: 1}, t + 0.13);
    tl.to(p[0], {scaleY: 1, duration: 0.5, ease: FLIP}, t + 0.13);
  });
  bout(["#t2", "#c1", "#c2"], @pershyi-0.1, 10, 0.26);
  tl.set("#gB", {autoAlpha: 0}, @pershyi+0.3);""")


# ===========================================================================
# C · Edits: a camera with the teleprompter inside
TPTXT = (u"Мені в дірект за один день написали двоє незнайомих між собою людей з одним і тим самим "
         u"питанням, на який суфлер я записую свої рілси, тож, видно, це дійсно хвилює багатьох.")


@beat
def c_edits():
    card = ('<div class="dglass edge hide" id="ed" style="left:90px;top:110px;width:900px;height:520px;border-radius:56px">'
            + tile("edCam", 84, 776, 26, "clear", stroke("camera"), extra_cls="circ", ring=False)
            + '<div class="tp hide" id="tp"><div class="tpx" id="tpx">%s</div><div class="tpc" id="tpc"></div></div>'
            '<div class="sl hide" id="sl1" style="top:356px"><span class="lb">Розмір</span><i class="tr"></i>'
            '<i class="fi" id="fi1"></i><i class="kn" id="kn1"></i></div>'
            '<div class="sl hide" id="sl2" style="top:432px"><span class="lb">Швидкість</span><i class="tr"></i>'
            '<i class="fi" id="fi2"></i><i class="kn" id="kn2"></i></div>'
            '<div class="shc"><div class="sheen"></div></div></div>' % TPTXT)
    L.append('<div class="g full" id="gC">' + card + '</div>')
    sfx("whoosh-short", T["pershyi"] - 0.05, -3)
    sfx("click", T["edits1"] + 0.06)
    sfx("pop", T["tam"] + 0.02, -1)
    sfx("click-soft", T["vstavl"] + 0.02)
    sfx("click-soft", T["rozmir"] - 0.4, -3)
    sfx("click-soft", T["shvydk"] + 0.05, -3)
    return js("""
  tl.set("#gC", {autoAlpha: 1}, @tam-0.05);
  gsap.set("#ed", {transformOrigin: "84px 70px"});
  arr("#ed", @tam+0.02, {s: 0.3, y: 0, d: 0.8, ease: SP});
  shn("#ed .sheen", @tam+0.35);
  arr("#edCam", @kamera-0.04, {s: 0.4, y: 10, d: 0.6});
  arr("#tp", @sufler2-0.05, {s: 0.9, y: 16, d: 0.6});
  gsap.set("#tpx", {clipPath: "inset(0% 0% 100% 0%)"});
  tl.fromTo("#tpx", {clipPath: "inset(0% 0% 100% 0%)"}, {clipPath: "inset(0% 0% 0% 0%)", duration: 0.4, ease: "power2.out", immediateRender: false}, @vstavl+0.04);
  tl.set("#tpc", {autoAlpha: 0}, @vstavl+0.04);
  arr(["#sl1", "#sl2"], @vstavl+0.15, {s: 0.9, y: 14, d: 0.6});
  gsap.set(["#kn1"], {x: 168}); gsap.set(["#fi1"], {scaleX: 0.3});
  gsap.set(["#kn2"], {x: 224}); gsap.set(["#fi2"], {scaleX: 0.4});
  tl.to("#kn1", {x: 392, duration: 0.6, ease: SP}, @nalasht+0.25);
  tl.to("#fi1", {scaleX: 0.7, duration: 0.6, ease: SP}, @nalasht+0.25);
  tl.to("#tpx", {scale: 1.2, duration: 0.6, ease: SP}, @nalasht+0.3);
  tl.to("#kn2", {x: 420, duration: 0.55, ease: SP}, @shvydk+0.02);
  tl.to("#fi2", {scaleX: 0.75, duration: 0.55, ease: SP}, @shvydk+0.02);
  tl.to("#tpx", {y: -118, duration: 0.55, ease: "power1.inOut"}, @chytaiesh-0.04);
  tl.to("#ed", {scale: 0.55, duration: 0.3, ease: "power2.in"}, @ya-0.32);
  bout("#ed", @ya-0.32, 12, 0.24);
  tl.set("#gC", {autoAlpha: 0}, @ya+0.2);""")


# ===========================================================================
# D / E · at the desk the blur is off; by the window it has to be on
@beat
def d_shelf():
    sh = ('<div class="dglass edge hide" id="sh" style="left:80px;top:330px;width:920px;height:190px;border-radius:60px">'
          '<div class="shc"><div class="sheen"></div></div></div>')
    sw = ('<span class="swl hide" id="swl" style="left:590px;top:404px">Розмиття фону</span>'
          '<div class="sw hide" id="sw" style="left:850px;top:390px"><div class="on" id="swOn"></div><div class="kb" id="swK"></div></div>'
          '<div class="sqring" id="swR" style="left:850px;top:390px;width:124px;height:70px;border-radius:35px"></div>')
    L.append('<div class="g full" id="gD">' + sh + chip("lc", 286, 383, 280, [DESK, WINDOW]) + sw + '</div>')
    sfx("pop", T["ya"] - 0.1, -3)
    sfx("click-soft", T["robochoho"] + 0.05)
    sfx("click-soft", T["vikna"] - 0.05)
    sfx("click", T["zablur"] + 0.1)
    sfx("click", T["edits2"] + 0.06, -1)
    return js("""
  tl.set("#gD", {autoAlpha: 1}, @ya-0.3);
  arr("#sh", @ya-0.2, {s: 0.85, y: 30, d: 0.75});
  shn("#sh .sheen", @ya+0.2);
  arr("#lc", @robochoho-0.02, {s: 0.5, y: 20, d: 0.7});
  arr(["#swl", "#sw"], @ne-0.04, {s: 0.7, y: 16, d: 0.65});
  tl.to("#swK", {keyframes: {x: [0, 10, -3, 0]}, duration: 0.4, ease: "none"}, @rozmyvaty+0.25);
  /* by the window: the chip turns over */
  tl.to("#lc", {scaleY: 0, duration: 0.13, ease: "power2.in"}, @vikna-0.08);
  tl.set("#lc0", {autoAlpha: 0}, @vikna+0.05); tl.set("#lc1", {autoAlpha: 1}, @vikna+0.05);
  tl.to("#lc", {scaleY: 1, duration: 0.5, ease: FLIP}, @vikna+0.05);
  /* and the background has to blur: switch on */
  tl.to("#swK", {x: 54, duration: 0.45, ease: SP}, @zablur+0.1);
  tl.fromTo("#swOn", {autoAlpha: 0}, {autoAlpha: 1, duration: 0.25, ease: "power2.out"}, @zablur+0.12);
  G.ripple("#swR", @zablur+0.2);
  bout(["#sh", "#lc", "#swl", "#sw"], @todi-0.32, 10, 0.26);
  tl.set("#gD", {autoAlpha: 0}, @todi);""")


# ===========================================================================
# the tile that carries B -> C -> D: «1», then Edits, then crossed out
@beat
def t_edits_tile():
    L.append('<div class="g full" id="gT">'
             '<div class="sqring" id="eTR" style="left:250px;top:150px;width:220px;height:220px"></div>'
             '<div class="tw hide" id="eT" style="left:250px;top:150px;width:220px;height:220px">'
             '<div class="pearl" id="eT1"><span class="t-big num">1</span><div class="sheen"></div></div>'
             '<div class="jelly hide" id="eT2"><span class="wmark" style="font-size:68px">Edits</span><div class="sheen"></div></div>'
             '<div class="tw circ hide" id="eIG" style="left:150px;top:-30px;width:96px;height:96px"><div class="jelly">%s</div></div>'
             '<div class="tw circ hide" id="eX" style="left:148px;top:-32px;width:104px;height:104px"><div class="pearl xb">%s</div></div>'
             '</div></div>' % (g.mark("instagram"), stroke("x")))
    return js("""
  tl.set("#gT", {autoAlpha: 1}, @dva-0.1);
  gsap.set("#eT", {transformOrigin: "50% 50%"});
  arr("#eT", @dva-0.04, {s: 0.4, y: 30});
  G.ripple("#eTR", @dva+0.28);
  /* «Перший»: tile 1 takes the centre */
  tl.to("#eT", {x: 180, duration: 0.7, ease: SP}, @pershyi);
  arr("#eIG", @instagramu-0.02, {s: 0.3, y: 10, d: 0.6});
  /* «Edits»: it turns over into Edits */
  tl.to("#eT", {scaleX: 0, duration: 0.13, ease: "power2.in"}, @edits1-0.06);
  tl.set("#eT1", {autoAlpha: 0}, @edits1+0.07); tl.set("#eT2", {autoAlpha: 1}, @edits1+0.07);
  tl.to("#eT", {scaleX: 1, duration: 0.4, ease: FLIP}, @edits1+0.07);
  shn("#eT2 .sheen", @edits1+0.3);
  /* it becomes the card's app icon */
  bout("#eIG", @tam-0.02, 8, 0.2);
  tl.set("#eT", {transformOrigin: "0px 0px"}, @tam+0.04);
  tl.to("#eT", {x: -120, y: -12, scale: 0.364, duration: 0.6, ease: SP}, @tam+0.05);
  /* the card folds back into it; it docks in the shelf */
  tl.to("#eT", {x: -138, y: 200, scale: 0.682, duration: 0.7, ease: SP}, @ya-0.08);
  /* «Edits вже не підходить» */
  arr("#eX", @edits2+0.02, {s: 0.3, y: 0, d: 0.6});
  G.haptic("#eT2", @edits2+0.1);
  tl.to("#eT2", {autoAlpha: 0.45, duration: 0.35, ease: "power2.out"}, @pidkhodyt);
  bout("#eT", @todi-0.32, 10, 0.26);
  tl.set("#gT", {autoAlpha: 0}, @todi);""")


# ===========================================================================
# F · her Notes popup: on the phone, pasted, laid over the camera, at eye level
POP_W, POP_H = 880, 920          # 926x1197 source at 0.9503, body window cut to 726
POP_X, POP_Y = 100, 470
SMALL_S, SMALL_DY = 0.42, -333   # on the phone, above her head
SCROLL = 176                      # px the body scrolls under her eyes
EYE_Y = 900


@beat
def f_notes():
    pop = ('<div class="tw hide" id="npW" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx"><div class="np">'
           '<div class="nph"><img src="assets/notes-popup.png" alt=""></div>'
           '<div class="npb"><img id="npI" src="assets/notes-popup.png" alt="" style="top:-194px"></div>'
           '<div class="npc" id="npC"></div></div></div>' % (POP_X, POP_Y, POP_W, POP_H))
    paste = '<div class="pst hide" id="pst" style="left:540px;top:300px">Вставити</div>'
    L.append('<div class="g full" id="gN">' + pop + paste + '</div>')

    labels = [(u"ФОТО", 0, 160), (u"ВІДЕО", 160, 170), (u"ПОРТРЕТНЕ ВІДЕО", 330, 380), (u"ЩЕ", 710, 120)]
    strip = "".join('<span class="ml" id="ml%d" style="left:%dpx;width:%dpx">%s</span>' % (i, x, w, t)
                    for i, (t, x, w) in enumerate(labels))
    mode = ('<div class="dglass edge hide" id="md" style="left:90px;top:300px;width:900px;height:124px;border-radius:62px">'
            '<div class="tw circ" id="mdF" style="left:18px;top:18px;width:88px;height:88px"><div class="pearl">%s</div></div>'
            '<div class="mw"><div class="ms" id="ms">%s</div><i class="mdot"></i></div>'
            '<div class="shc"><div class="sheen"></div></div></div>' % (stroke("flip"), strip))
    eye = ('<div class="eyw hide" id="eyW" style="left:0;top:%dpx;width:1080px;height:60px">'
           '<svg class="abs" width="1080" height="60" style="left:0;top:0"><path class="eyl" d="M60 30 L 872 30"/></svg></div>'
           % (EYE_Y - 30)
           + tile("eyC", 96, 902, EYE_Y - 48, "jelly", stroke("eye"), extra_cls="circ"))
    L.append('<div class="g full" id="gF">' + mode + eye + '</div>')

    sfx("whoosh-short", T["notatky"] - 0.08, -2)
    sfx("click", T["vstavliaiu"] - 0.02)
    sfx("whoosh-short", T["nakladaiu"] + 0.02)
    sfx("click-soft", T["frontal"] + 0.02)
    sfx("click-soft", T["portret"] + 0.05)
    sfx("click-soft", T["rivni"] + 0.02, -2)
    sfx("whoosh-short", T["vzahali"] + 0.55, -5)
    sfx("whoosh-short", T["yakshcho"] - 0.05, -6)
    return js("""
  tl.set("#gN", {autoAlpha: 1}, @notatky-0.3);
  gsap.set("#npW", {transformOrigin: "50% 0%"});
  /* on her phone: small, above her head, opaque */
  tl.fromTo("#npW", {autoAlpha: 0, filter: "blur(12px)"}, {autoAlpha: 1, filter: "blur(0px)", duration: 0.42, ease: "power2.out"}, @notatky-0.1);
  tl.set("#npW", {filter: "none"}, @notatky+0.33);
  tl.fromTo("#npW", {scale: {{s0}}, y: {{dy}}+40}, {scale: {{s1}}, y: {{dy}}, duration: 0.85, ease: SOFT}, @notatky-0.1);
  /* «вставляю туди текст»: Вставити, tap, the text drops in */
  gsap.set("#pst", {xPercent: -50});
  arr("#pst", @vstavliaiu-0.32, {s: 0.5, y: 16, d: 0.55});
  tl.to("#pst", {scale: 0.92, duration: 0.08, ease: "power2.out"}, @vstavliaiu-0.02);
  tl.to("#pst", {scale: 1, duration: 0.3, ease: SP}, @vstavliaiu+0.06);
  tl.fromTo("#npC", {clipPath: "inset(0% 0% 0% 0%)"}, {clipPath: "inset(100% 0% 0% 0%)", duration: 0.4, ease: "power2.inOut"}, @vstavliaiu+0.04);
  bout("#pst", @vstavliaiu+0.22, 8, 0.24);
  /* «накладаю зверху на камеру»: over her face, half transparent */
  tl.to("#npW", {scale: 1, y: 0, duration: 1.0, ease: SOFT}, @nakladaiu);
  tl.to("#npW", {autoAlpha: 0.5, duration: 0.85, ease: "power2.inOut"}, @nakladaiu+0.1);
  tl.fromTo("#npI", {y: 0}, {y: -{{scroll}}, duration: {{sd}}, ease: "none"}, @nakladaiu+1.4);
  tl.to("#npW", {autoAlpha: 0, scale: 0.97, filter: "blur(8px)", duration: 0.34, ease: "power2.in"}, @vzahali+0.55);
  tl.set("#npW", {filter: "none"}, @vzahali+0.9);
  /* the callback: fainter, while she says she is reading it right now */
  tl.fromTo("#npW", {autoAlpha: 0, scale: 0.97, filter: "blur(10px)"},
            {autoAlpha: 0.3, scale: 1, filter: "blur(0px)", duration: 0.55, ease: "power2.out", immediateRender: false}, @yakshcho-0.04);
  tl.set("#npW", {filter: "none"}, @yakshcho+0.52);
  tl.fromTo("#npI", {y: -{{scroll}}}, {y: -{{scroll}}-10, duration: @sufl3e-@yakshcho, ease: "none", immediateRender: false}, @yakshcho);
  tl.to("#npW", {autoAlpha: 0, duration: 0.3, ease: "power2.in"}, @sufl3e-0.22);
  tl.set("#gN", {autoAlpha: 0}, @to);

  /* front camera, portrait video */
  tl.set("#gF", {autoAlpha: 1}, @kameru2-0.1);
  arr("#md", @kameru2-0.02, {s: 0.85, y: 24, d: 0.7});
  gsap.set("#ms", {x: 130}); gsap.set("#ml1", {color: "#ffffff"});
  tl.fromTo("#mdF svg", {rotation: 0}, {rotation: 180, duration: 0.6, ease: SP, transformOrigin: "50% 50%"}, @frontal+0.02);
  tl.to("#ms", {x: -145, duration: 0.6, ease: SP}, @portret-0.02);
  tl.to("#ml1", {color: "rgba(255,255,255,0.5)", duration: 0.25}, @portret);
  tl.to("#ml2", {color: "#ffffff", duration: 0.25}, @portret+0.1);
  shn("#md .sheen", @portret+0.3);
  bout("#md", @mene-0.1, 10, 0.26);
  /* eye level */
  tl.fromTo("#eyW", {autoAlpha: 0, clipPath: "inset(0% 100% 0% 0%)"},
            {autoAlpha: 1, clipPath: "inset(0% 0% 0% 0%)", duration: 0.6, ease: "power2.inOut"}, @rivni-0.02);
  arr("#eyC", @ochei-0.12, {s: 0.4, y: 0, d: 0.65});
  G.ripple("#eyCR", @ochei+0.2);
  bout(["#eyW", "#eyC"], @kudy-0.05, 8, 0.28);
  tl.set("#gF", {autoAlpha: 0}, @kudy+0.3);""").replace("{{s0}}", "%.3f" % (SMALL_S * 0.72)).replace(
        "{{s1}}", "%.3f" % SMALL_S).replace("{{dy}}", str(SMALL_DY)).replace("{{scroll}}", str(SCROLL)).replace(
        "{{sd}}", "%.3f" % (T["vzahali"] + 0.55 - T["nakladaiu"] - 1.4))


# ===========================================================================
# H · Стежити
@beat
def h_follow():
    L.append('<div class="g full" id="gH"><div class="fl hide" id="fl" style="left:190px;top:330px;width:700px;height:150px">'
             '<div class="tw circ" style="left:28px;top:27px;width:96px;height:96px"><div class="jelly">%s</div></div>'
             '<div class="t" id="flT">Стежити</div>'
             '<div class="on" id="flOn"><div class="tw circ" style="left:28px;top:27px;width:96px;height:96px">'
             '<div class="pearl">%s</div></div><div class="t">Ви стежите</div></div>'
             '<div class="ck" id="ck4" style="left:470px;top:75px"></div>'
             '<div class="shc"><div class="sheen"></div></div></div></div>'
             % (g.mark("instagram"), stroke("check")))
    sfx("pop", T["to"] + 0.02, -2)
    sfx("click", T["pidpysh"] + 0.02)
    return js("""
  tl.set("#gH", {autoAlpha: 1}, @to-0.1);
  arr("#fl", @to-0.02, {s: 0.6, y: 40});
  tl.to("#fl", {scale: 0.95, duration: 0.09, ease: "power2.out"}, @pidpysh);
  tl.to("#fl", {scale: 1, duration: 0.45, ease: SP}, @pidpysh+0.09);
  tl.fromTo("#flOn", {autoAlpha: 0}, {autoAlpha: 1, duration: 0.2}, @pidpysh+0.04);
  tl.set("#flT", {autoAlpha: 0}, @pidpysh+0.05);
  tl.fromTo("#ck4", {scale: 0.3, autoAlpha: 0.95}, {scale: 2.4, autoAlpha: 0, duration: 0.7, ease: "power2.out", immediateRender: false}, @pidpysh+0.02);
  shn("#fl .sheen", @pidpysh+0.15);""")


# ---------------------------------------------------------------------------
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


# captions that would repeat the graphic's own words (STYLE.md §2b.1)
def span_words(a, b):
    return (round(a - 0.02, 3), round(b, 3), "")


BLACKOUT = [
    span_words(T["edits1"], T["edits1e"]),          # the tile turns into «Edits»
    span_words(T["rozmir"], T["shvydke"]),          # slider labels Розмір / Швидкість
    span_words(T["stola"], T["stolae"]),            # the chip says «стіл»
    span_words(T["rozmyvaty"], T["fon1e"]),         # the switch says «Розмиття фону»
    span_words(T["vikna"], T["viknae"]),            # the chip says «вікно»
    span_words(T["fon2"], T["fon2e"]),              # «фон» again, on the switch
    span_words(T["edits2"], T["edits2e"]),          # the crossed tile says «Edits»
    span_words(T["vstavliaiu"], T["vstavliaiue"]),  # the «Вставити» pill
    span_words(T["portret"], T["videoe"]),          # the mode strip: ПОРТРЕТНЕ ВІДЕО
]


def check_no_paint():
    """No beat may be on screen inside the closeup."""
    a, b = NO_PAINT[0]
    assert T["vzahali"] + 0.95 < a, "the popup runs into the closeup"
    assert T["yakshcho"] - 0.04 > b + 0.15, "the callback arrives inside the closeup"


def main():
    check_no_paint()
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
        title=u"Reel 28 — суфлер",
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
