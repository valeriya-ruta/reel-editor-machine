# -*- coding: utf-8 -*-
"""Reel 41 — the long YouTube video: «моя AI-система для контенту».
Landscape 1920x1080, ~7:53, cut from three raw takes by work/demo/plate.py.

Not rendered end to end. Each beat is a *window*: its own small composition
over its own slice of the plate (demo/w/<name>/), and work/demo/final.py lays
the rendered windows back over the plate frame-exact and burns the subtitles
on top. A window starts and ends on clean plate, so the splice is invisible.
That keeps each composition far under the heavy-element budget (STYLE.md
§5a.1) and renders ~2 min of graphics instead of 8 min of video.

Placement in landscape: her head sits at x 780-1200 and her shoulders start
at y ~640, so graphics live beside her head — left x 80-700, right x
1250-1850, y 110-600 — and over her chest only below the shoulders' reach.
Subtitles own y 840-960 (work/demo/captions.ass), so nothing goes there.

The one recurring object is the **content line**: Ідеї → Сценарій → Зйомка →
Монтаж. It shows up on «ідеї», again on the scripts, lights step by step on
«прописати, зняти, змонтувати», gets ×30 on «30 тем… 30 сценаріїв», and the
AI system is what finally runs it.

usage: python build.py            -> demo/w/*/index.html + windows.json
       python build.py --plates   -> also cut each window's plate slice
"""
import io
import json
import os
import re
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))
from kit import Kit  # noqa: E402
from glass import Glass  # noqa: E402

FPS = 30
W_, H_ = 1920, 1080
WORDS = json.load(io.open(os.path.join(ROOT, "work", "demo", "words_out.json"), encoding="utf-8"))["words"]
SHOTS = os.path.join(ROOT, "work", "media", "demo")      # her stats screenshots (gitignored)


def _n(s):
    return "".join(ch for ch in s.lower() if ch.isalnum())


MISS = []
# Beat times below were authored against the first cut (v1, timeline_v1.json).
# R() carries a v1 time to the source take and back onto the current cut, so a
# re-cut moves every beat with its words instead of breaking them.
_TL1 = json.load(io.open(os.path.join(ROOT, "work", "demo", "timeline_v1.json"), encoding="utf-8"))["spans"]
_TL = json.load(io.open(os.path.join(ROOT, "work", "demo", "timeline.json"), encoding="utf-8"))["spans"]


def R(t):
    f = t * FPS
    sp = [x for x in _TL1 if x["start"] <= f < x["start"] + x["frames"]]
    if not sp:
        return t
    sp = sp[0]
    src = sp["a"] + (f - sp["start"]) / FPS * sp["speed"]
    best = None
    for x in _TL:
        if x["src"] == sp["src"] and x["speed"] == sp["speed"]:
            if x["a"] <= src < x["b"]:
                return (x["start"] + (src - x["a"]) / x["speed"] * FPS) / FPS
            # in a cut-out stretch: snap to the nearest kept edge
            for edge, out in ((x["a"], x["start"]), (x["b"], x["start"] + x["frames"])):
                d = abs(src - edge)
                if best is None or d < best[0]:
                    best = (d, out / float(FPS))
    return best[1]


def S(word, near, end=False):
    near = R(near)
    hits = [w for w in WORDS if _n(word) == _n(w["w"])]
    assert hits, ("word not in this cut", word)
    w = min(hits, key=lambda w: abs(w["s"] - near))
    if abs(w["s"] - near) >= 0.8:
        MISS.append((word, near, w["s"]))
    return w["e"] if end else w["s"]


def E(word, near):
    return S(word, near, end=True)


# ---------------------------------------------------------------------------
class Beat(object):
    def __init__(self, name, t0, t1):
        self.name, self.t0, self.t1 = name, t0, t1
        self.html, self.js, self.css = "", "", ""
        self.marks = []
        self.assets = []


BEATS = []
T = {}


def beat(name, t0, t1):
    b = Beat(name, R(t0), None if t1 is None else R(t1))
    BEATS.append(b)
    return b


def js(src, **extra):
    """`@name`, `@name+0.12` -> a literal (absolute) time; shifted per window later."""
    vals = dict(T)
    vals.update(extra)

    def rep(m):
        v = vals[m.group(1)] + (float(m.group(2)) if m.group(2) else 0.0)
        return "%.3f" % v
    return re.sub(r"@(\w+)([+-]\d+(?:\.\d+)?)?", rep, src)


g = Glass(["claude", "telegram", "instagram", "buffer", "googledrive", "youtube"])

STROKES = {
    "check": '<path d="M5.4 12.6l4.3 4.3 8.9-9.5"/>',
    "x": '<path d="M6.5 6.5l11 11M17.5 6.5l-11 11"/>',
    "clock": '<circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/>',
    "cal": '<rect x="3.5" y="5" width="17" height="15.5" rx="3"/><path d="M3.5 10h17M8 3v4M16 3v4"/>',
    "bulb": '<path d="M9 18h6M10 21h4M12 3a6 6 0 0 0-3.6 10.8c.6.5 1 1.2 1 2V16h5.2v-.2c0-.8.4-1.5 1-2A6 6 0 0 0 12 3z"/>',
    "doc": '<path d="M7 3h7l4 4v14H7z"/><path d="M14 3v4h4M9.5 12h5M9.5 15.5h5"/>',
    "cam": '<rect x="3" y="7" width="13" height="10" rx="2.5"/><path d="M16 11l5-3v8l-5-3"/>',
    "cut": '<circle cx="6.5" cy="17" r="2.6"/><circle cx="17.5" cy="17" r="2.6"/><path d="M8.4 15.2 17 4M15.6 15.2 7 4"/>',
    "user": '<circle cx="12" cy="8.5" r="3.6"/><path d="M5 20c.8-3.8 3.6-5.6 7-5.6s6.2 1.8 7 5.6"/>',
    "bag": '<rect x="3.5" y="8" width="17" height="12" rx="2.5"/><path d="M9 8V6a3 3 0 0 1 6 0v2"/>',
    "mic": '<rect x="9" y="3" width="6" height="11" rx="3"/><path d="M5.5 11.5a6.5 6.5 0 0 0 13 0M12 18v3"/>',
    "down": '<path d="M12 4.8v14.4M6.2 13.4 12 19.2l5.8-5.8"/>',
    "play": '<path d="M8 5.5v13l11-6.5z"/>',
    "brain": '<path d="M9 4a3 3 0 0 0-3 3 3 3 0 0 0-1.5 5.4A3 3 0 0 0 7 17a3 3 0 0 0 5 1.6V5.6A3 3 0 0 0 9 4z"/><path d="M15 4a3 3 0 0 1 3 3 3 3 0 0 1 1.5 5.4A3 3 0 0 1 17 17a3 3 0 0 1-5 1.6"/>',
    "book": '<path d="M4 5.5C6.5 4.3 9.5 4.3 12 6c2.5-1.7 5.5-1.7 8-.5V19c-2.5-1.2-5.5-1.2-8 .5-2.5-1.7-5.5-1.7-8-.5z"/><path d="M12 6v13.5"/>',
    "send": '<path d="M4 12l16-7-6 16-3-7z"/>',
}


def stroke(name, cls="sk"):
    return '<svg class="%s" viewBox="0 0 24 24">%s</svg>' % (cls, STROKES[name])


def tile(tid, size, x, y, material, inner, extra_cls="", ring=True, extra=""):
    r = ('<div class="sqring" id="%sR" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx"></div>'
         % (tid, x, y, size, size)) if ring else ""
    return ('%s<div class="tw hide %s" id="%s" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx">'
            '<div class="%s">%s<div class="sheen"></div></div>%s</div>'
            % (r, extra_cls, tid, x, y, size, size, material, inner, extra))


def chip(cid, text, x, y, cls=""):
    return '<div class="pz hide %s" id="%s" style="left:%dpx;top:%dpx">%s</div>' % (cls, cid, x, y, text)


def ctile(tid, icon, x, y, size=84, material="jelly"):
    """a small round icon tile"""
    return tile(tid, size, x, y, material, stroke(icon), extra_cls="circ", ring=False)


CSS = """
.abs { position: absolute; }
.hide { opacity: 0; visibility: hidden; }
.tw { position: absolute; }
.sk { fill: none; stroke: url(#gw); stroke-width: 2.3; stroke-linecap: round; stroke-linejoin: round;
  width: 50%; height: 50%; position: relative; z-index: 1; overflow: visible; }
.pearl .sk { stroke: #17141c; }
.clear { overflow: hidden; }
.circ .jelly, .circ .pearl, .circ .clear, .circ .sheen { border-radius: 50%; }
.aurs { position: absolute; left: -500px; top: -500px; width: 2920px; height: 2080px; pointer-events: none;
  background:
    radial-gradient(circle 560px at 1960px 520px, rgba(255,110,156,0.50), rgba(255,110,156,0)),
    radial-gradient(circle 640px at 700px 1500px, rgba(222,32,74,0.55), rgba(222,32,74,0)),
    radial-gradient(circle 420px at 1500px 1300px, rgba(255,198,214,0.20), rgba(255,198,214,0)); }
.pz { position: absolute; height: 64px; padding: 0 26px; border-radius: 32px; display: flex; align-items: center; gap: 12px;
  background: linear-gradient(160deg, #ffffff 0%, #fff3f7 100%); color: #8d0d24; font-size: 34px; font-weight: 700;
  letter-spacing: -0.01em; white-space: nowrap; z-index: 4;
  box-shadow: inset 0 2px 1px #fff, 0 18px 34px -14px rgba(30,4,12,0.6); }
.pz.dim { color: rgba(23,20,28,0.45); }
.pz.red { background: linear-gradient(165deg, #e0204b 0%, #8d0d24 100%); color: #fff;
  box-shadow: inset 0 2px 1px rgba(255,255,255,0.45), 0 18px 34px -14px rgba(70,4,20,0.7); }
.pz .sk { width: 36px; height: 36px; stroke: #b4122f; }
.pz.red .sk { stroke: #fff; }
.big-g { font-weight: 900; color: #fff; line-height: 1; position: relative; z-index: 1; letter-spacing: -0.04em; }
/* white type over footage, on dark glass */
.lb { position: absolute; color: #fff; font-weight: 700; font-size: 34px; letter-spacing: -0.01em; white-space: nowrap; }
.lb.s { font-size: 26px; font-weight: 500; color: rgba(255,255,255,0.72); }
.lb.k { font-size: 22px; font-weight: 700; letter-spacing: 0.16em; color: rgba(255,255,255,0.6); }
.num { position: absolute; font-weight: 900; color: #fff; letter-spacing: -0.045em; line-height: 1; }
/* a strike drawn through a row */
.strk { position: absolute; height: 6px; border-radius: 3px; background: #ff6e9c; transform-origin: 0 50%;
  box-shadow: 0 0 14px rgba(255,110,156,0.8); }
/* checklist rows on dark glass */
.cb { position: absolute; width: 46px; height: 46px; border-radius: 14px; box-shadow: inset 0 0 0 3.5px rgba(255,255,255,0.45); }
.cbf { position: absolute; inset: 0; border-radius: 14px; opacity: 0; visibility: hidden;
  background: linear-gradient(165deg, #ff6e9c 0%, #e0204b 55%, #8d0d24 100%); box-shadow: 0 0 18px rgba(255,110,156,0.6); }
.cbf svg { position: absolute; left: 7px; top: 7px; width: 32px; height: 32px; fill: none; stroke: #fff;
  stroke-width: 3.2; stroke-linecap: round; stroke-linejoin: round; }
.bar { position: absolute; display: block; height: 14px; border-radius: 7px; background: rgba(255,255,255,0.34); }
.bar.d { background: rgba(23,20,28,0.13); }
.hb { position: absolute; display: block; height: 20px; border-radius: 8px; background: linear-gradient(115deg, #c41434 0%, #8d0d24 100%); }
/* the content line */
.st { position: absolute; left: 34px; width: 452px; height: 88px; border-radius: 26px;
  background: rgba(255,255,255,0.10); box-shadow: inset 0 1.5px 1px rgba(255,255,255,0.28); }
.st .ic { position: absolute; left: 14px; top: 12px; width: 64px; height: 64px; }
.st .lb { left: 96px; top: 24px; }
.st .x30 { position: absolute; right: 18px; top: 16px; height: 56px; padding: 0 18px; border-radius: 28px;
  background: linear-gradient(165deg, #ff6e9c 0%, #e0204b 100%); color: #fff; font-size: 32px; font-weight: 900;
  display: flex; align-items: center; letter-spacing: -0.02em; }
.st .ok { position: absolute; right: 22px; top: 21px; }
.lit-st { position: absolute; left: 34px; width: 452px; height: 88px; border-radius: 26px; opacity: 0; visibility: hidden;
  background: linear-gradient(120deg, rgba(255,110,156,0.55) 0%, rgba(224,32,75,0.35) 100%);
  box-shadow: inset 0 1.5px 1px rgba(255,255,255,0.5), 0 0 30px rgba(255,110,156,0.45); }
/* the calendar */
.dd { position: absolute; width: 58px; height: 52px; border-radius: 14px; border: 3px dashed rgba(255,255,255,0.32); }
.dd.f { border: 0; background: rgba(255,255,255,0.16); }
/* the chart */
.cv { fill: none; stroke: #fff; stroke-width: 9; stroke-linecap: round; stroke-linejoin: round;
  filter: drop-shadow(0 0 12px rgba(255,110,156,0.9)); }
.cvd { fill: none; stroke: #ff6e9c; stroke-width: 9; stroke-linecap: round; stroke-linejoin: round;
  filter: drop-shadow(0 0 14px rgba(255,110,156,1)); }
/* script and reel cards */
.sc { position: absolute; border-radius: 26px; overflow: hidden;
  background: linear-gradient(172deg, #ffffff 0%, #fff9fb 55%, #fdf0f4 100%);
  box-shadow: inset 0 2px 1px #fff, 0 30px 60px -26px rgba(8,0,3,0.75); }
.rc { position: absolute; border-radius: 18px; overflow: hidden;
  background: linear-gradient(165deg, #ffffff 0%, #ffe3ec 100%);
  box-shadow: inset 0 2px 1px #fff, 0 20px 40px -18px rgba(8,0,3,0.7); }
.rc svg { position: absolute; left: 50%; top: 50%; width: 44%; height: 44%; transform: translate(-50%, -50%); fill: #b4122f; }
.rc.lit { background: linear-gradient(165deg, #ff8ab0 0%, #e0204b 50%, #8d0d24 100%); }
.rc.lit svg { fill: #fff; }
/* the takeover sheet */
.prc { position: absolute; font-weight: 900; letter-spacing: -0.045em; line-height: 1; white-space: nowrap;
  background: linear-gradient(118deg, #7e0b20 0%, #b4122f 42%, #ff6e9c 100%);
  -webkit-background-clip: text; background-clip: text; color: transparent; padding-right: 8px; }
.ink { position: absolute; color: #17141c; font-weight: 700; white-space: nowrap; letter-spacing: -0.015em; }
.ink.s { color: rgba(23,20,28,0.5); font-weight: 500; }
.ink.k { font-size: 24px; letter-spacing: 0.16em; color: rgba(23,20,28,0.42); }
.vr { position: absolute; width: 3px; background: rgba(23,20,28,0.08); }
.slash { position: absolute; height: 12px; border-radius: 6px; background: #b4122f; transform-origin: 0 50%; }
/* notification */
.ntf { position: absolute; border-radius: 40px; }
.ntf .lb { left: 132px; }
/* voice note */
.wv { position: absolute; width: 10px; border-radius: 5px; background: #fff; transform-origin: 50% 50%; }
.shc { position: absolute; inset: 0; border-radius: inherit; overflow: hidden; pointer-events: none; }
.shc .sheen { mix-blend-mode: normal; opacity: 0.4; }
/* screenshots stay screenshots (her rule): a card of her own screen, never retyped */
.shot { position: absolute; border-radius: 34px; overflow: hidden; background: #fff;
  box-shadow: 0 0 0 4px rgba(255,255,255,0.9), 0 50px 100px -30px rgba(8,0,3,0.8); }
.shot img { position: absolute; display: block; }
.hl { position: absolute; border-radius: 22px; border: 6px solid #ff3d7f; box-shadow: 0 0 26px rgba(255,61,127,0.75); }
"""

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
  function tick(id, t) {
    tl.fromTo("#" + id, {autoAlpha: 0, scale: 0.4}, {autoAlpha: 1, scale: 1, duration: 0.4, ease: POP}, t);
    draw2(id + "p", t + 0.06, 0.3);
  }
  function strike(sel, t) { tl.fromTo(sel, {scaleX: 0}, {scaleX: 1, duration: 0.4, ease: "power3.out"}, t); }
  gsap.set(".sheen", {xPercent: -120});
"""


def cbox(cid, x, y):
    return ('<div class="cb" style="left:%dpx;top:%dpx"><div class="cbf" id="%s">'
            '<svg viewBox="0 0 24 24"><path id="%sp" d="M5.4 12.6l4.3 4.3 8.9-9.5"/></svg></div></div>'
            % (x, y, cid, cid))


# ===========================================================================
# 1 · a whole month: no reel, no carousel
T.update(serp=S("серпня,", 16.40), misiats=S("місяць.", 18.82), zhodnoho=S("жодного", 20.56),
         rilsa=S("рілса,", 20.96), karus=S("каруселі.", 22.02), vplyv=S("вплив", 23.6))
b = beat("month", 14.3, 24.3)
cells = ""
for i in range(35):
    r, c = divmod(i, 7)
    cells += '<div class="dd" id="md%d" style="left:%dpx;top:%dpx"></div>' % (i, 34 + c * 70, 112 + r * 62)
b.html = ('<div class="dglass edge hide" id="mC" style="left:1280px;top:120px;width:560px;height:460px;border-radius:48px">'
          '<div class="lb k" style="left:36px;top:40px">ВЕРЕСЕНЬ</div>' + cells
          + '<div class="shc"><div class="sheen"></div></div></div>'
          + chip("mR", stroke("play") + "0 рілсів", 1330, 520, "red")
          + chip("mK", stroke("doc") + "0 каруселей", 1560, 520, "red"))
b.js = js("""
  arr("#mC", @serp-0.1, {s: 0.85, y: 30});
  shn("#mC .sheen", @serp+0.3);
  for (var i = 0; i < 35; i++) tl.fromTo("#md" + i, {autoAlpha: 0, scale: 0.6}, {autoAlpha: 1, scale: 1, duration: 0.3, ease: SP}, @misiats-0.7 + i * 0.022);
  arr("#mR", @rilsa-0.15, {s: 0.4, y: 20, d: 0.6});
  arr("#mK", @karus-0.15, {s: 0.4, y: 20, d: 0.6});
  G.haptic("#mC", @karus+0.25);
  bout(["#mC", "#mR", "#mK"], @vplyv-0.1, 10, 0.32);""")

# ===========================================================================
# 2 · not a UGC creator, not a blogger: an expert — with clients and services
T.update(ugc=S("UGC-креаторка,", 25.6), blog=S("блогерка", 27.04), expert=S("експертка.", 28.76),
         klienty=S("клієнти,", 29.94), poslugy=S("послуги.", 30.88), koly=S("коли", 31.9))
b = beat("expert", 24.6, 32.4)
b.html = ('<div class="dglass edge hide" id="eP" style="left:110px;top:150px;width:520px;height:330px;border-radius:44px">'
          '<div class="lb hide" id="e1" style="left:44px;top:46px">UGC-креаторка</div><div class="strk" id="e1s" style="left:38px;top:68px;width:290px"></div>'
          '<div class="lb hide" id="e2" style="left:44px;top:126px">Блогерка</div><div class="strk" id="e2s" style="left:38px;top:148px;width:180px"></div>'
          '<div class="pz red hide" id="e3" style="left:36px;top:208px;height:84px;font-size:44px;border-radius:42px">'
          + stroke("check") + 'Експертка</div>'
          '<div class="shc"><div class="sheen"></div></div></div>'
          + chip("eK", stroke("user") + "Клієнти", 140, 510)
          + chip("eS", stroke("bag") + "Послуги", 380, 510))
b.js = js("""
  arr("#eP", @ugc-0.3, {s: 0.85, y: 30});
  bin("#e1", @ugc-0.15, 8, 0.3);
  gsap.set(["#e1s", "#e2s"], {scaleX: 0});
  strike("#e1s", @ugc+0.55);
  bin("#e2", @blog-0.1, 8, 0.3);
  strike("#e2s", @blog+0.4);
  arr("#e3", @expert-0.05, {s: 0.5, y: 20, d: 0.7});
  shn("#eP .sheen", @expert+0.1);
  arr("#eK", @klienty-0.1, {s: 0.4, y: 20, d: 0.6});
  arr("#eS", @poslugy-0.1, {s: 0.4, y: 20, d: 0.6});
  bout(["#eP", "#eK", "#eS"], @koly+0.1, 10, 0.32);""")

# ===========================================================================
# 3 · not posting -> marketing sinks
T.update(marketing=S("маркетинг,", 34.87), bachyty=S("бачити.", 37.19), katastr=S("катастрофа.", 39.0))
b = beat("drop", 33.0, 39.8)
b.html = ('<div class="dglass edge hide" id="dP" style="left:1290px;top:150px;width:540px;height:380px;border-radius:44px">'
          '<div class="lb" style="left:40px;top:38px">Маркетинг</div>'
          '<svg class="abs" width="540" height="380" style="left:0;top:0;overflow:visible">'
          '<path class="cv" id="dL1" d="M50 300 C 110 260 140 200 200 190 S 260 150 290 140"/>'
          '<path class="cvd" id="dL2" d="M290 140 C 330 150 360 230 400 270 S 460 320 495 330"/></svg>'
          '<div class="shc"><div class="sheen"></div></div></div>')
b.js = js("""
  arr("#dP", @marketing-0.9, {s: 0.85, y: 30});
  draw2("dL1", @marketing-0.6, 0.6);
  draw2("dL2", @marketing+0.15, 0.8);
  G.haptic("#dP", @bachyty);
  bout("#dP", @bachyty+0.7, 10, 0.32);""")

# ===========================================================================
# ===========================================================================
# PROOF · her own Instagram screenshots, as screenshots (STYLE.md §4a): cropped,
# the number that matters ringed, never retyped. Files live in work/media/r41/
# (gitignored): custom.jpg = the month of silence (Aug 20 – Sep 10),
# d30.jpg = the last 30 days, summary.jpg = Sep 27 – Oct 26, reel_5492.jpg =
# one reel's summary. Coordinates below are in the screenshots' own 1080-wide pixels.
SHOT_CUSTOM = os.path.join(SHOTS, "custom.jpg")
SHOT_30 = os.path.join(SHOTS, "d30.jpg")
SHOT_SUM = os.path.join(SHOTS, "summary.jpg")
SHOT_REEL = os.path.join(SHOTS, "reel_5492.jpg")
OVERVIEW = (20, 440, 1060, 1060)              # header, the two cards, the chart, the dates
R_VIEWS, R_FOLLOW = (44, 560, 430, 236), (500, 560, 436, 236)
R_FLAT = (552, 1356, 336, 96)                 # the flat stretch, Aug 31 – Sep 7


def shot(sid, path, x, y, w, crop, hl=()):
    """crop = (cx, cy, cw, ch) in the screenshot's own pixels; shown at width w.
    hl = rings in the same pixel space."""
    from PIL import Image
    nat = Image.open(path).size[0]
    cx, cy, cw, ch = crop
    k = w / float(cw)
    rings = "".join('<div class="hl hide" id="%s" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx"></div>'
                    % (hid, (hx - cx) * k, (hy - cy) * k, hw * k, hh * k) for hid, (hx, hy, hw, hh) in hl)
    return ('<div class="shot hide" id="%s" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx">'
            '<img src="assets/%s" style="left:%dpx;top:%dpx;width:%dpx"></div>%s'
            % (sid, x, y, w, ch * k, os.path.basename(path), -cx * k, -cy * k, nat * k,
               '<div class="abs" style="left:%dpx;top:%dpx">%s</div>' % (x, y, rings)))


def ring(ids, t):
    return ('  tl.fromTo(%s, {autoAlpha: 0, scale: 1.25}, {autoAlpha: 1, scale: 1, duration: 0.4, ease: POP}, %s);\n'
            % (json.dumps(ids), t))


if os.path.exists(SHOT_CUSTOM):
    # the month of silence: the views flatline, followers go negative
    T.update(postyty=S("постити,", 44.92), perehl=E("набирати", 49.3), bachyly=S("бачили,", 51.98),
             misiats2=E("місяць.", 56.54))
    b = beat("proof1", 42.8, 57.2)
    b.assets = [SHOT_CUSTOM]
    b.html = shot("p1", SHOT_CUSTOM, 1270, 70, 560, OVERVIEW, hl=[("p1c", R_FLAT), ("p1f", R_FOLLOW)])
    b.js = js("""
  arr("#p1", @postyty-0.2, {s: 0.8, y: 40, d: 0.8});""") + ring(["#p1c"], js("@perehl-0.3")) + ring(["#p1f"], js("@bachyly-0.4")) + js("""
  bout(["#p1", "#p1c", "#p1f"], @misiats2-0.2, 10, 0.32);""")

if os.path.exists(SHOT_CUSTOM) and os.path.exists(SHOT_30):
    # «до і після» (her note on v3: no graphics at all, only the screenshots,
    # and every good one on this line): the month of silence on «до», then all
    # the good screens land one by one on «після» and stay through «дві години»
    D30_INT = os.path.join(SHOTS, "d30_int.jpg")
    REELS = [os.path.join(SHOTS, f) for f in ("reel_5492.jpg", "reel_2594.jpg", "reel_1427.jpg")]
    T.update(do=S("до", 243.06), pislia=S("після.", 243.56), vse2=E("все.", 249.82))
    b = beat("proof2", 242.5, 250.5)
    b.assets = [SHOT_CUSTOM, SHOT_30, D30_INT, SHOT_SUM] + REELS
    R_REEL = (40, 506, 490, 238)
    goods = [  # (id, file, x, y, w, crop, rings)
        ("g1", SHOT_30, 590, 60, 430, OVERVIEW, [("g1v", R_VIEWS), ("g1f", R_FOLLOW)]),
        ("g2", D30_INT, 590, 520, 430, (20, 1520, 1060, 480), [("g2a", (24, 1612, 1036, 168)), ("g2b", (24, 1786, 1036, 168))]),
        ("g3", SHOT_SUM, 1060, 60, 520, (0, 0, 1080, 798), [("g3v", (760, 400, 310, 110)), ("g3f", (760, 535, 310, 110))]),
    ] + [("g%d" % (4 + i), f, 1060 + i * 272, 480, 256, (0, 0, 1080, 1030), [("g%dv" % (4 + i), R_REEL)])
         for i, f in enumerate(REELS)]
    html = shot("p2a", SHOT_CUSTOM, 70, 60, 470, OVERVIEW, hl=[("p2av", R_VIEWS), ("p2af", R_FOLLOW)])
    for gid, f, x, y, w, crop, hl in goods:
        html += shot(gid, f, x, y, w, crop, hl=hl)
    b.html = html
    jsb = js("""
  arr("#p2a", @do-0.25, {s: 0.8, x: 40, y: 20, d: 0.7});""") + ring(["#p2av", "#p2af"], js("@do+0.25"))
    allids = ["#p2a", "#p2av", "#p2af"]
    for i, (gid, f, x, y, w, crop, hl) in enumerate(goods):
        t0 = T["pislia"] - 0.1 + i * 0.42
        jsb += '  arr("#%s", %.3f, {s: 0.75, y: 40, d: 0.7});\n' % (gid, t0)
        jsb += ring(["#" + h[0] for h in hl], "%.3f" % (t0 + 0.45))
        allids += ["#" + gid] + ["#" + h[0] for h in hl]
    jsb += js("""
  bout(%s, @vse2+0.05, 10, 0.32);""" % json.dumps(allids))
    b.js = jsb

if os.path.exists(SHOT_SUM) and os.path.exists(SHOT_REEL):
    # «два рілси … незалежно від того, як я себе відчуваю»: what that has done
    T.update(nezal2=S("Незалежно", 432.46), dali=E("далі.", 436.44))
    b = beat("proof3", 432.3, 437.9)
    b.assets = [SHOT_SUM, SHOT_REEL]
    b.html = (shot("p3a", SHOT_SUM, 1250, 110, 600, (0, 0, 1080, 798),
                   hl=[("p3v", (760, 400, 310, 110)), ("p3f", (760, 535, 310, 110))])
              + shot("p3b", SHOT_REEL, 110, 150, 480, (0, 0, 1080, 1033),
                     hl=[("p3r", (40, 508, 488, 236))]))
    b.js = js("""
  arr("#p3a", @nezal2-0.1, {s: 0.8, x: -30, y: 20, d: 0.7});
  arr("#p3b", @nezal2+0.5, {s: 0.8, x: 30, y: 20, d: 0.7});""") \
        + ring(["#p3v", "#p3f"], js("@nezal2+0.9")) + ring(["#p3r"], js("@nezal2+1.3")) + js("""
  bout(["#p3a", "#p3b", "#p3v", "#p3f", "#p3r"], @dali-0.1, 10, 0.32);""")

# ===========================================================================
# the content line (reused): Ідеї -> Сценарій -> Зйомка -> Монтаж
STEPS = [("bulb", "Ідеї"), ("doc", "Сценарій"), ("cam", "Зйомка"), ("cut", "Монтаж")]


def line_html(pid, x=110, y=120, x30=False):
    rows = ""
    for i, (ic, label) in enumerate(STEPS):
        top = 34 + i * 104
        rows += ('<div class="lit-st" id="%sL%d" style="top:%dpx"></div>'
                 '<div class="st" style="top:%dpx"><div class="tw circ ic"><div class="jelly">%s</div></div>'
                 '<div class="lb">%s</div>%s%s</div>'
                 % (pid, i, top, top, stroke(ic), label,
                    ('<div class="x30 hide" id="%sX%d">×30</div>' % (pid, i)) if x30 else "",
                    cbox("%sC%d" % (pid, i), 382, 21) if not x30 else ""))
    return ('<div class="dglass edge hide" id="%s" style="left:%dpx;top:%dpx;width:520px;height:476px;border-radius:44px">'
            '%s<div class="shc"><div class="sheen"></div></div></div>' % (pid, x, y, rows))


# 5 · first: ideas
T.update(idei1=S("ідеї", 68.77), kontentu1=S("контенту.", 69.6), temy=S("Теми", 70.5))
b = beat("line1", 67.2, 71.4)
b.html = line_html("l1")
b.js = js("""
  arr("#l1", @idei1-0.45, {s: 0.85, y: 30});
  tl.to("#l1L0", {autoAlpha: 1, duration: 0.3}, @idei1);
  G.bump("#l1 .st:nth-of-type(2)", @idei1);
  bout("#l1", @temy+0.1, 10, 0.32);""")

# 6 · a script: years of experience -> hi-hi-ha-ha, + hook, + call to action
T.update(stsen=S("сценарій.", 95.25), dosvid=S("досвіду,", 99.73), khi=S("хі-хі-ха-ха", 105.85),
         hachok=S("гачок,", 108.73), dyvytys=E("дивитись.", 110.9))
b = beat("script", 94.6, 111.2)
b.html = ('<div class="sc hide" id="sS" style="left:1290px;top:110px;width:540px;height:520px">'
          '<div class="ink k" style="left:40px;top:40px">СЦЕНАРІЙ</div>'
          '<i class="hb" style="left:40px;top:92px;width:300px"></i>'
          '<i class="bar d" style="left:40px;top:134px;width:440px"></i><i class="bar d" style="left:40px;top:162px;width:400px"></i>'
          '<i class="bar d" style="left:40px;top:190px;width:310px"></i>'
          '<div class="ink hide" id="sY" style="left:40px;top:236px;font-size:34px">Роки досвіду</div>'
          '<div class="strk" id="sYs" style="left:34px;top:256px;width:230px;background:#b4122f;box-shadow:none"></div>'
          '<div class="ink hide" id="sH" style="left:290px;top:236px;font-size:34px;color:#b4122f">хі-хі-ха-ха</div>'
          '<div class="pz red hide" id="sG" style="left:36px;top:322px">' + stroke("bulb") + 'Гачок</div>'
          '<div class="shc"><div class="sheen"></div></div></div>')
b.js = js("""
  arr("#sS", @stsen-0.25, {s: 0.85, y: 30});
  shn("#sS .sheen", @stsen+0.2);
  bin("#sY", @dosvid-0.4, 8, 0.3);
  gsap.set("#sYs", {scaleX: 0});
  strike("#sYs", @khi-0.3);
  arr("#sH", @khi-0.05, {s: 0.5, y: 10, d: 0.6});
  arr("#sG", @hachok-0.1, {s: 0.4, y: 20, d: 0.6});
  bout("#sS", @dyvytys+0.15, 10, 0.32);""")

# ===========================================================================
# 7 · once a day, better twice
T.update(raz1=S("раз", 129.81), dva1=S("два.", 130.97))
T["tomu"] = T["dva1"] + 0.35
b = beat("daily", 128.9, 131.9)
b.html = (chip("dy1", stroke("cal") + "1 раз на день", 1340, 220)
          + chip("dy2", stroke("cal") + "2 рази на день", 1340, 310, "red"))
b.js = js("""
  arr("#dy1", @raz1-0.4, {s: 0.4, x: 40, y: 0, d: 0.6});
  arr("#dy2", @dva1-0.25, {s: 0.4, x: 40, y: 0, d: 0.6});
  tl.to("#dy1", {autoAlpha: 0.5, scale: 0.9, duration: 0.3}, @dva1);
  bout(["#dy1", "#dy2"], @tomu+0.6, 10, 0.3);""")

# 8 · seven scripts from scratch, every week
T.update(sim=S("сім", 151.07), nulia=S("нуля.", 153.3), tyzhnia=S("тижня.", 154.52), kozhen=S("Хочу", 155.8))
b = beat("week", 150.4, 155.7)
cards = ""
for i, d in enumerate(("Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Нд")):
    x = 1290 + (i % 4) * 140
    y = 150 + (i // 4) * 200
    cards += ('<div class="sc hide" id="wk%d" style="left:%dpx;top:%dpx;width:120px;height:170px;border-radius:20px">'
              '<div class="ink" style="left:16px;top:14px;font-size:24px;color:#b4122f">%s</div>'
              '<i class="bar d" style="left:16px;top:60px;width:86px;height:10px"></i>'
              '<i class="bar d" style="left:16px;top:82px;width:70px;height:10px"></i>'
              '<i class="bar d" style="left:16px;top:104px;width:52px;height:10px"></i></div>' % (i, x, y, d))
b.html = cards
b.js = js("""
  for (var i = 0; i < 7; i++) arr("#wk" + i, @sim-0.1 + i * 0.09, {s: 0.5, y: 30, d: 0.7});
  for (var j = 0; j < 7; j++) G.bump("#wk" + j, @tyzhnia + j * 0.05);
  bout(["#wk0","#wk1","#wk2","#wk3","#wk4","#wk5","#wk6"], @kozhen-0.45, 10, 0.3);""")

# 9 · the line again: write, film, edit
T.update(propys=S("прописати,", 156.73), zniaty=S("зняти", 157.69), zmont=S("змонтувати.", 162.17),
         yakshcho=S("якщо", 163.5))
b = beat("line2", 155.7, 164.2)
b.html = line_html("l2")
b.js = js("""
  arr("#l2", @kozhen, {s: 0.85, y: 30});
  tl.set("#l2L0", {autoAlpha: 0.35}, @kozhen);
  tick("l2C0", @kozhen+0.3);
  tl.to("#l2L1", {autoAlpha: 1, duration: 0.3}, @propys);
  tick("l2C1", @propys+0.4);
  tl.to("#l2L1", {autoAlpha: 0.35, duration: 0.3}, @zniaty-0.1);
  tl.to("#l2L2", {autoAlpha: 1, duration: 0.3}, @zniaty);
  tick("l2C2", @zniaty+0.35);
  tl.to("#l2L2", {autoAlpha: 0.35, duration: 0.3}, @zmont-0.1);
  tl.to("#l2L3", {autoAlpha: 1, duration: 0.3}, @zmont);
  G.haptic("#l2", @zmont+0.2);
  bout("#l2", @yakshcho+0.3, 10, 0.32);""")

# ===========================================================================
# 10 · OVER: what delegating the edit costs. Only the numbers she says.
T.update(deleg=S("делегувати", 174.23), anim=S("анімації,", 183.15), e2030=S("20-30", 187.21),
         mnozh=S("множимо", 190.33), d500=S("500,", 195.16), d600=S("600,", 196.14), d1000=S("1000", 196.76),
         d1000e=E("доларів,", 197.12))
T["rutynu"] = T["d1000e"] + 0.75
T.update(dorogo=S("дорого.", 175.55), obiekt=S("Об'єктивно", 176.45))
b = beat("cost", 173.6, 197.95)
reels = "".join('<div class="rc hide" id="cR%d" style="left:%dpx;top:%dpx;width:64px;height:110px">%s</div>'
                % (i, 1080 + (i % 6) * 78, 300 + (i // 6) * 126, stroke("play").replace('class="sk"', ""))
                for i in range(12))
b.html = ('<div class="g full" id="gC" style="opacity:0;visibility:hidden"><div class="tkg"></div><div class="aurs"></div><div class="grain"></div>'
          '<div class="sheet hide" id="cS" style="left:200px;top:120px;width:760px;height:600px">'
          '<div class="ink k" style="left:56px;top:56px">МОНТАЖ, 1 ВІДЕО</div>'
          '<div class="ink s hide" id="cA" style="left:56px;top:150px;font-size:34px">З класними анімаціями</div>'
          '<div class="prc hide" id="c2030" style="left:52px;top:220px;font-size:150px">€20–30</div>'
          '<div class="hair" style="position:absolute;left:56px;top:430px;width:648px"></div>'
          '<i class="bar d" style="left:56px;top:470px;width:520px;height:18px"></i>'
          '<i class="bar d" style="left:56px;top:510px;width:420px;height:18px"></i>'
          '<div class="shc"><div class="sheen"></div></div></div>'
          + tile("cE", 260, 330, 250, "pearl", stroke("user"), extra_cls="circ")
          + chip("cEl", stroke("cut") + "Монтажер", 345, 560)
          + chip("cEp", "€ € €", 520, 230, "red")
          + reels
          + '<div class="num hide" id="cX" style="left:1080px;top:180px;font-size:72px">× на місяць</div>'
          '<div class="sheet hide" id="cT" style="left:1060px;top:600px;width:660px;height:230px">'
          '<div class="ink k" style="left:50px;top:40px">НА МІСЯЦЬ</div>'
          '<div class="prc" id="cSum" style="left:46px;top:84px;font-size:118px">$500</div>'
          '<div class="shc"><div class="sheen"></div></div></div>'
          '</div>')
b.js = js("""
  G.irisOpen("#gC", @deleg-0.2, 960, 300, 0.7);
  tl.fromTo("#gC .aurs", {x: 0, y: 0}, {x: -120, y: 60, duration: @rutynu-@deleg, ease: "sine.inOut"}, @deleg);
  arr("#cE", @deleg+0.05, {s: 0.5, y: 30});
  arr("#cEl", @deleg+0.3, {s: 0.4, y: 20, d: 0.6});
  arr("#cEp", @dorogo-0.1, {s: 0.3, y: 20, d: 0.6});
  G.bump("#cEp", @obiekt+0.1); G.haptic("#cE", @obiekt+0.2);
  bout(["#cE", "#cEl", "#cEp"], @anim-1.2, 10, 0.3);
  arr("#cS", @anim-0.9, {s: 0.86, y: 50, d: 0.8});
  bin("#cA", @anim-0.5, 8, 0.3);
  shn("#cS .sheen", @anim-0.4);
  arr("#c2030", @e2030-0.1, {s: 0.4, y: 20, d: 0.7});
  for (var i = 0; i < 12; i++) arr("#cR" + i, @mnozh-0.1 + i * 0.06, {s: 0.4, y: 30, d: 0.6});
  bin("#cX", @mnozh+0.1, 10, 0.35);
  arr("#cT", @d500-0.3, {s: 0.8, y: 40, d: 0.8});
  tl.set("#cSum", {textContent: "$600"}, @d600);
  tl.set("#cSum", {textContent: "$1000"}, @d1000);
  G.bump("#cT", @d500); G.bump("#cT", @d600); G.bump("#cT", @d1000);
  shn("#cT .sheen", @d1000+0.1);
  G.irisClose("#gC", @rutynu-0.5, 1390, 700, 0.55);""")

# ===========================================================================
# 11 · thirty of everything, and «я вмру»
T.update(t30a=S("30", 225.09), t30b=S("30", 227.67), zniaty2=S("зняти,", 229.89), zmont2=S("змонтувати,", 230.59),
         vmru=S("вмру.", 231.33), nezroblu=S("зроблю", 232.6))
b = beat("thirty", 223.6, 233.6)
b.html = line_html("l3", x30=True)
b.js = js("""
  arr("#l3", @t30a-0.7, {s: 0.85, y: 30});
  arr("#l3X0", @t30a-0.05, {s: 0.3, y: 0, d: 0.55});
  arr("#l3X1", @t30b-0.05, {s: 0.3, y: 0, d: 0.55});
  arr("#l3X2", @zniaty2-0.05, {s: 0.3, y: 0, d: 0.55});
  arr("#l3X3", @zmont2-0.05, {s: 0.3, y: 0, d: 0.55});
  /* no filter here: a filter on a backdrop-filter surface renders black */
  tl.to("#l3", {autoAlpha: 0.55, y: 40, rotation: -2.5, duration: 0.5, ease: "power2.in"}, @vmru);
  bout("#l3", @nezroblu+0.25, 10, 0.32);""")

# ===========================================================================
# 12 · now: two hours a week
T.update(dvi=S("дві", 246.54), hodyny=E("години", 247.06), zrobyty=S("зробити", 250.0), yak=S("Як", 250.6))
b = beat("twohours", 245.9, 251.0)
b.html = ('<div class="dglass edge hide" id="hP" style="left:1300px;top:160px;width:520px;height:250px;border-radius:44px">'
          + ctile("hI", "clock", 40, 40, 96)
          + '<div class="num" style="left:160px;top:44px;font-size:110px">2 год</div>'
          '<div class="lb s" style="left:164px;top:170px">на тиждень, максимум</div>'
          '<div class="shc"><div class="sheen"></div></div></div>')
b.js = js("""
  arr("#hP", @dvi-0.15, {s: 0.8, y: 30});
  arr("#hI", @dvi, {s: 0.4, y: 0, d: 0.6});
  shn("#hP .sheen", @hodyny);
  bout("#hP", @yak-0.1, 10, 0.3);""")

# ===========================================================================
# 13 · it all runs in the Claude app: no Telegram agents, no extra chats
T.update(klod1=S("Клод.", 253.64), tele=S("телеграм-агенти,", 255.0), teleg2=S("Телеграмі.", 257.80),
         klod2=S("Клод.", 260.70), chaty=S("чати.", 262.56), nedil=S("неділю", 263.64))
b = beat("claude", 252.4, 264.0)
chats = "".join('<i class="bar hide" id="chB%d" style="left:%dpx;top:%dpx;width:%dpx;height:16px"></i>'
                % (i, 1330, 430 + i * 36, w) for i, w in enumerate((300, 240, 280, 200)))
b.html = (tile("cl", 190, 1460, 160, "jelly", g.mark("claude"))
          + tile("tg", 120, 1700, 200, "pearl", g.mark("telegram"))
          + '<div class="strk" id="tgS" style="left:1690px;top:256px;width:140px;transform:rotate(-38deg);transform-origin:50% 50%"></div>'
          + '<div class="dglass edge hide" id="chP" style="left:1300px;top:400px;width:430px;height:180px;border-radius:36px"></div>'
          + chats)
b.js = js("""
  arr("#cl", @klod1-0.25, {s: 0.4, y: 30});
  G.ripple("#clR", @klod1+0.1);
  shn("#cl .sheen", @klod1+0.15);
  tl.to("#cl", {x: -150, duration: 0.6, ease: SP}, @tele-0.3);
  arr("#tg", @tele-0.1, {s: 0.4, y: 20, d: 0.6});
  gsap.set("#tgS", {scaleX: 0, autoAlpha: 1});
  tl.fromTo("#tgS", {scaleX: 0}, {scaleX: 1, duration: 0.35, ease: "power3.out"}, @tele+0.5);
  tl.to("#tg", {filter: "saturate(0) brightness(0.7)", duration: 0.3}, @teleg2-0.2);
  bout(["#tg", "#tgS"], @klod2-0.4, 10, 0.3);
  tl.to("#cl", {x: 0, scale: 1.1, duration: 0.6, ease: SP}, @klod2-0.3);
  G.ripple("#clR", @klod2);
  arr("#chP", @chaty-1.0, {s: 0.85, y: 20, d: 0.7});
  for (var i = 0; i < 4; i++) bin("#chB" + i, @chaty-0.8 + i * 0.1, 8, 0.3);
  bout(["#cl", "#chP", "#chB0", "#chB1", "#chB2", "#chB3"], @nedil-0.1, 10, 0.3);""")

# 14 · Sunday morning: the notification
T.update(notif=S("нотифікація", 265.10), analiz=S("аналіз", 267.76), idei3=S("ідеї", 269.52), vidkr=S("відкриваю", 270.9))
b = beat("notif", 264.4, 270.55)
b.html = ('<div class="dglass edge hide ntf" id="nT" style="left:1180px;top:110px;width:680px;height:150px">'
          '<div class="tw" style="left:30px;top:30px;width:88px;height:88px"><div class="jelly">' + g.mark("claude") + '</div></div>'
          '<div class="lb" style="top:30px">Аналіз готовий</div>'
          '<div class="lb s" style="top:82px">Ідеї для контенту на тиждень</div>'
          '<div class="lb s" style="left:auto;right:34px;top:32px;font-size:22px">нд, 09:00</div>'
          '<div class="shc"><div class="sheen"></div></div></div>')
b.js = js("""
  arr("#nT", @notif-0.1, {s: 0.85, y: -60, d: 0.7, ease: SOFT});
  G.haptic("#nT", @notif+0.35);
  shn("#nT .sheen", @analiz);
  tl.to("#nT", {y: -40, autoAlpha: 0, duration: 0.3, ease: "power2.in"}, @idei3+0.45);""")

# ===========================================================================
# 15 · the numbered list: she keeps 1, 2, 3, 5, 6, 7
T.update(numer=S("нумерований", 292.34), r1=S("раз,", 297.65), r2=S("два,", 297.85), r3=S("три,", 298.03),
         r5=S("п'ять,", 298.4), r6=S("шість,", 298.99), r7=S("сім.", 299.25), tyzh3=E("тиждень.", 301.5))
b = beat("ideas", 291.6, 302.4)
rows = ""
for i in range(8):
    y = 76 + i * 56
    rows += ('<div class="lb" style="left:40px;top:%dpx;font-size:28px">%d.</div>' % (y + 4, i + 1)
             + cbox("iC%d" % i, 90, y)
             + '<i class="bar" style="left:156px;top:%dpx;width:%dpx"></i>' % (y + 16, (300, 250, 330, 210, 290, 260, 320, 230)[i]))
b.html = ('<div class="dglass edge hide" id="iP" style="left:1300px;top:110px;width:540px;height:560px;border-radius:44px">'
          '<div class="lb k" style="left:40px;top:34px">ІДЕЇ НА ТИЖДЕНЬ</div>' + rows
          + '<div class="shc"><div class="sheen"></div></div></div>')
b.js = js("""
  arr("#iP", @numer-0.3, {s: 0.85, y: 30});
  shn("#iP .sheen", @numer+0.2);
  tick("iC0", @r1); tick("iC1", @r2); tick("iC2", @r3); tick("iC4", @r5); tick("iC5", @r6); tick("iC6", @r7);
  tl.to(["#iP .bar:nth-of-type(4)", "#iP .bar:nth-of-type(8)"], {autoAlpha: 0.35, duration: 0.3}, @r7+0.3);
  bout("#iP", @tyzh3+0.1, 10, 0.32);""")

# ===========================================================================
# 15b · the strategy file it works from: services, prices, cases, lead magnets, courses
T.update(fail=S("файл", 307.9), poslugy2=S("послуги,", 311.11), vartist=S("вартість", 311.9),
         keisy=S("кейси,", 313.6), lidmag=S("лідмагніти,", 314.5), kursy=S("курси.", 315.4),
         znaie=S("знає", 316.1), zhnaie_e=E("все.", 316.4))
b = beat("strategy", 306.9, 317.4)
rows = [("poslugy2", "bag", "Послуги"), ("vartist", "doc", "Вартість послуг"), ("keisy", "check", "Кейси"),
        ("lidmag", "send", "Лідмагніти"), ("kursy", "book", "Курси")]
html = ('<div class="sc hide" id="gS" style="left:1290px;top:100px;width:540px;height:600px">'
        '<div class="ink k" style="left:40px;top:40px">СТРАТЕГІЯ</div>'
        '<i class="hb" style="left:40px;top:90px;width:260px"></i>')
for i, (key, ic, label) in enumerate(rows):
    html += ('<div class="pz hide" id="gR%d" style="left:36px;top:%dpx;background:linear-gradient(160deg,#fbe3ea 0%%,#f7d3de 100%%)">%s%s</div>'
             % (i, 140 + i * 86, stroke(ic), label))
html += '<div class="shc"><div class="sheen"></div></div></div>'
b.html = html
b.js = js("""
  arr("#gS", @fail-0.2, {s: 0.85, y: 30});
  shn("#gS .sheen", @fail+0.3);
  arr("#gR0", @poslugy2-0.1, {s: 0.4, x: -30, y: 0, d: 0.55});
  arr("#gR1", @vartist-0.1, {s: 0.4, x: -30, y: 0, d: 0.55});
  arr("#gR2", @keisy-0.1, {s: 0.4, x: -30, y: 0, d: 0.55});
  arr("#gR3", @lidmag-0.1, {s: 0.4, x: -30, y: 0, d: 0.55});
  arr("#gR4", @kursy-0.1, {s: 0.4, x: -30, y: 0, d: 0.55});
  G.bump("#gS", @znaie); shn("#gS .sheen", @znaie);
  bout("#gS", @zhnaie_e+0.3, 10, 0.32);""")

# ===========================================================================
# 16 · «запиши мені голосове»
T.update(zapysh=S("Запиши", 328.2), holos1=S("голосове,", 328.78), temu=E("тему.", 331.5))
b = beat("voice1", 327.6, 332.3)
bars = "".join('<i class="wv" id="vA%d" style="left:%dpx;top:%dpx;height:%dpx"></i>'
               % (i, 140 + i * 20, 75 - h // 2, h) for i, h in enumerate((20, 46, 70, 38, 58, 86, 44, 64, 30, 52, 78, 40, 60, 26, 48, 34)))
b.html = ('<div class="dglass edge hide" id="vB" style="left:1300px;top:200px;width:520px;height:150px;border-radius:75px">'
          + ctile("vM", "mic", 30, 30, 90) + bars
          + '<div class="lb s" style="left:auto;right:32px;top:56px;font-size:26px">0:42</div></div>')
b.js = js("""
  arr("#vB", @zapysh-0.1, {s: 0.8, y: 30});
  for (var i = 0; i < 16; i++) tl.fromTo("#vA" + i, {scaleY: 0.1}, {scaleY: 1, duration: 0.4, ease: SP}, @holos1 + i * 0.04);
  bout("#vB", @temu+0.2, 10, 0.3);""")

# 17 · Sunday coffee voice note: the mess becomes a script
T.update(zapysuiu=S("записую", 344.6), kavardak=S("кавардак,", 354.36), peretv=S("перетворює", 355.78))
b = beat("voice2", 344.0, 355.85)
bars2 = "".join('<i class="wv" id="vC%d" style="left:%dpx;top:%dpx;height:%dpx"></i>'
                % (i, 140 + i * 20, 75 - h // 2, h) for i, h in enumerate((30, 66, 44, 80, 36, 58, 90, 40, 72, 28, 62, 84, 46, 70, 32, 54)))
b.html = ('<div class="dglass edge hide" id="vD" style="left:1300px;top:200px;width:520px;height:150px;border-radius:75px">'
          + ctile("vN", "mic", 30, 30, 90) + bars2
          + '<div class="lb s" style="left:auto;right:32px;top:56px;font-size:26px">3:15</div></div>')
b.js = js("""
  arr("#vD", @zapysuiu-0.1, {s: 0.8, y: 30});
  for (var i = 0; i < 16; i++) tl.fromTo("#vC" + i, {scaleY: 0.1}, {scaleY: 1, duration: 0.4, ease: SP}, @zapysuiu+0.2 + i * 0.04);
  tl.to("#vD", {keyframes: {rotation: [0, -3, 3, -2, 2, 0]}, duration: 0.7, ease: "none"}, @kavardak);
  tl.to("#vD", {scale: 0.6, autoAlpha: 0, filter: "blur(10px)", duration: 0.35, ease: "power2.in"}, @peretv-0.4);""")

# 18 · ... and gives her the script: hooks, calls to action
T.update(zakl2=S("закликами", 362.24), tekst=E("текст.", 366.0), vse=S("все,", 366.6))
b = beat("script2", 361.95, 367.4)
b.html = ('<div class="sc hide" id="tS" style="left:1290px;top:130px;width:540px;height:420px">'
          '<div class="ink k" style="left:40px;top:40px">СЦЕНАРІЙ</div>'
          '<i class="hb" style="left:40px;top:92px;width:320px"></i>'
          '<i class="bar d" style="left:40px;top:136px;width:450px"></i><i class="bar d" style="left:40px;top:164px;width:410px"></i>'
          '<i class="bar d" style="left:40px;top:192px;width:330px"></i><i class="bar d" style="left:40px;top:220px;width:200px"></i>'
          '<div class="pz red hide" id="tG" style="left:36px;top:272px">' + stroke("check") + 'Гачок</div>'
          '<div class="pz red hide" id="tC" style="left:220px;top:272px">' + stroke("check") + 'Заклик до дії</div>'
          '<div class="shc"><div class="sheen"></div></div></div>')
b.js = js("""
  arr("#tS", @zakl2-0.25, {s: 0.7, y: 30, d: 0.8});
  shn("#tS .sheen", @zakl2+0.15);
  arr("#tG", @zakl2-0.4, {s: 0.4, y: 20, d: 0.6});
  arr("#tC", @zakl2+0.1, {s: 0.4, y: 20, d: 0.6});
  bout("#tS", @vse-0.05, 10, 0.3);""")

# 19 · Monday: dress up, camera at the window, read off the teleprompter
T.update(ponedil=S("понеділок", 368.91), sufl=S("суфлера,", 377.72), zapys=S("записати", 380.0))
b = beat("prompter", 368.5, 381.2)
lines = "".join('<i class="bar" style="left:44px;top:%dpx;width:%dpx;height:16px"></i>' % (60 + i * 46, w)
                for i, w in enumerate((420, 380, 440, 300, 410, 360, 430, 280, 400, 350, 420, 310)))
b.html = (chip("pD", stroke("cal") + "Понеділок", 1330, 150, "red")
          + '<div class="dglass edge hide" id="pT" style="left:1300px;top:250px;width:520px;height:330px;border-radius:40px;overflow:hidden">'
          '<div id="pTL" style="position:absolute;inset:0">' + lines + '</div>'
          '<i style="position:absolute;left:24px;right:24px;top:150px;height:56px;border-radius:16px;background:rgba(255,110,156,0.25);box-shadow:inset 0 0 0 2px rgba(255,138,176,0.7)"></i>'
          '</div>')
b.js = js("""
  arr("#pD", @ponedil-0.1, {s: 0.4, x: 40, y: 0, d: 0.6});
  bout("#pD", @sufl-1.2, 10, 0.3);
  arr("#pT", @sufl-0.6, {s: 0.85, y: 30});
  tl.fromTo("#pTL", {y: 40}, {y: -200, duration: 3.2, ease: "none"}, @sufl-0.3);
  bout("#pT", @zapys+0.6, 10, 0.3);""")

# ===========================================================================
# 20 · after a while: the finished videos
T.update(otrym=S("отримую", 399.10), vid2=E("відео.", 400.5))
b = beat("videos", 398.2, 401.15)
rcs = "".join('<div class="rc lit hide" id="vR%d" style="left:%dpx;top:%dpx;width:120px;height:210px">%s</div>'
              % (i, 1310 + i * 132, 230, stroke("play").replace('class="sk"', "")) for i in range(4))
b.html = rcs
b.js = js("""
  for (var i = 0; i < 4; i++) arr("#vR" + i, @otrym-0.15 + i * 0.1, {s: 0.4, y: -60, d: 0.7, ease: SOFT});
  bout(["#vR0", "#vR1", "#vR2", "#vR3"], @vid2+0.2, 10, 0.25);""")

# 21 · and it schedules them to Instagram itself (Buffer)
T.update(planuie=S("планує", 406.66), insta=S("Інстаграм.", 407.12), nasprav=S("насправді", 408.0))
b = beat("buffer", 405.4, 408.9)
b.html = (tile("bf", 150, 1330, 190, "pearl", g.mark("buffer"))
          + '<svg class="cab abs" width="1920" height="700" style="left:0;top:0">'
          '<path class="tube hide" id="bKT" d="M1490 265 L1610 265"/><path class="core hide" id="bKC" d="M1490 265 L1610 265"/>'
          '<g class="pkg"><path class="pkt" id="bKP" style="opacity:0" d="M1490 265 L1610 265"/></g></svg>'
          + tile("ig", 150, 1630, 190, "jelly", g.mark("instagram"))
          + chip("bC", stroke("cal") + "Заплановано", 1400, 380, "red"))
b.js = js("""
  arr("#bf", @planuie-0.6, {s: 0.4, y: 20, d: 0.7});
  tl.set(["#bKT", "#bKC"], {autoAlpha: 1}, @planuie-0.2);
  draw2("bKT", @planuie-0.2, 0.3); draw2("bKC", @planuie-0.2, 0.3);
  arr("#ig", @planuie, {s: 0.4, y: 20, d: 0.7});
  G.packet("bKP", @planuie+0.2, 0.4);
  G.ripple("#igR", @insta);
  arr("#bC", @insta-0.05, {s: 0.4, y: 20, d: 0.6});
  bout(["#bf", "#ig", "#bKT", "#bKC", "#bC"], @nasprav+0.35, 10, 0.3);""")

# 22 · every day, two reels go out
T.update(kozh=S("кожен", 428.44), dva2=S("два", 429.78), profil=S("профіль.", 431.64), nezal=S("Незалежно", 432.5))
b = beat("twoaday", 427.9, 433.4)
grid = ""
for i, d in enumerate(("Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Нд")):
    x = 1290 + i * 80
    grid += '<div class="lb s" style="left:%dpx;top:150px;font-size:24px">%s</div>' % (x + 16, d)
    for k in range(2):
        grid += ('<div class="rc hide" id="tw%d_%d" style="left:%dpx;top:%dpx;width:64px;height:110px">%s</div>'
                 % (i, k, x, 196 + k * 126, stroke("play").replace('class="sk"', "")))
b.html = ('<div class="dglass edge hide" id="twP" style="left:1260px;top:120px;width:600px;height:470px;border-radius:44px">'
          '</div>' + grid.replace('class="lb s"', 'class="lb s hide twd"'))
b.js = js("""
  arr("#twP", @kozh-0.3, {s: 0.85, y: 30});
  bin(".twd", @kozh, 8, 0.3);
  for (var i = 0; i < 7; i++) { arr("#tw" + i + "_0", @dva2-0.1 + i * 0.07, {s: 0.4, y: -40, d: 0.6, ease: SOFT});
                                arr("#tw" + i + "_1", @dva2+0.15 + i * 0.07, {s: 0.4, y: -40, d: 0.6, ease: SOFT}); }
  var all = ["#twP", ".twd"]; for (var j = 0; j < 7; j++) all.push("#tw" + j + "_0", "#tw" + j + "_1");
  bout(all, @nezal+0.3, 10, 0.3);""")

# 23 · CTA: the button under the video
T.update(naty=S("натискай", 470.8), knop=S("кнопку", 471.51))
b = beat("cta", 470.4, 473.25)
b.html = ('<div class="pz red hide" id="ctB" style="left:150px;top:600px;height:96px;font-size:44px;border-radius:48px;padding:0 36px">'
          + stroke("down") + 'Кнопка під відео</div>')
b.js = js("""
  arr("#ctB", @knop-0.25, {s: 0.5, y: -30, d: 0.7});
  shn("#ctB .sheen", @knop);
  tl.to("#ctB", {y: 14, duration: 0.3, ease: "sine.inOut", yoyo: true, repeat: 1}, @knop+0.55);
  bout("#ctB", @knop+1.3, 10, 0.25);""")


# ===========================================================================
# assembly: one composition per window
def window_doc(b, dur, plate_rel):
    k = Kit(width=W_, height=H_, fps=FPS, duration=dur)
    k.css(g.css())
    k.css(CSS)
    css = k.base_css() + "\n".join(k._css) + "\n" + "\n".join(k._sq)
    off = b.t0

    def shift(m):
        return "%.3f" % (float(m.group(0)) - off)
    # every absolute time literal in this beat's JS is shifted into the window's clock
    body = re.sub(r"(?<![\w.#\-])\d{2,3}\.\d{3}(?![\w])", shift, b.js)
    body = re.sub(r"(?<![\w.#\-])(\d{3}\.\d{1,2})(?=[,)\s])", lambda m: "%.3f" % (float(m.group(1)) - off), body)
    return '''<!DOCTYPE html>
<html lang="uk">
  <head>
    <meta charset="utf-8">
    <title>Reel 41 — %(name)s</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
    <style>%(css)s
    .g.full { top: 0; height: 1080px; }
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0"
         data-width="%(w)d" data-height="%(h)d" data-duration="%(dur).3f" data-fps="%(fps)d">
      <video id="vid" class="plate" src="%(plate)s"
             data-start="0" data-duration="%(dur).3f" data-media-start="0"
             muted playsinline></video>
      %(defs)s
      %(html)s
    </div>
    <script>
      function build() {
        var tl = gsap.timeline({paused: true});
%(motion)s
%(head)s
%(body)s
        window.__timelines["main"] = tl;
      }
      if (document.fonts && document.fonts.ready) document.fonts.ready.then(build);
      else build();
    </script>
  </body>
</html>
''' % {"name": b.name, "css": css, "w": W_, "h": H_, "dur": dur, "fps": FPS, "plate": plate_rel,
       "defs": g.defs(), "html": b.html, "motion": g.js(), "head": HEAD_JS, "body": body}


# her note on v3 (2026-10-27): "i dont think we need graphics at all. keep subtitles
# and cuts and zoom ins, remove all the graphics, keep only the screenshots".
# The other beats stay defined above for the record but are not built.
KEEP = ("proof1", "proof2")


def main():
    if MISS:
        sys.exit("words off their expected time: %r" % MISS)
    tl = json.load(io.open(os.path.join(ROOT, "work", "demo", "timeline.json"), encoding="utf-8"))
    total = tl["frames"]
    plate = os.path.join(HERE, "assets", "voice.mp4")
    # each beat's span: from t0 to after its last tween, whatever the re-cut did
    # to t1 (the last time literal in its JS + the longest exit, ~0.7 s)
    spans = []
    for b in sorted((x for x in BEATS if x.name in KEEP), key=lambda x: x.t0):
        last = max(float(x) for x in re.findall(r"(?<![\w.#\-])\d+\.\d{3}(?![\w])", b.js) if float(x) > 5.0)
        spans.append([b, b.t0, max(b.t1 or 0.0, last + 0.7)])
    # beats that hand off inside each other's span share one window
    merged = []
    for b, a0, a1 in spans:
        if merged and a0 < merged[-1][2]:
            m = merged[-1]
            m[0] = m[0] if isinstance(m[0], list) else [m[0]]
            m[0].append(b)
            m[2] = max(m[2], a1)
        else:
            merged.append([b, a0, a1])
    wins = []
    for grp, a0, a1 in merged:
        if isinstance(grp, list):
            b = Beat("+".join(x.name for x in grp), a0, a1)
            b.html = "\n".join(x.html for x in grp)
            b.js = "\n".join(x.js for x in grp)
            b.assets = [f for x in grp for f in x.assets]
        else:
            b = grp
        f0 = int(round(a0 * FPS))
        f1 = min(total, int(round(a1 * FPS)))
        n = f1 - f0
        b.t0 = f0 / float(FPS)
        d = os.path.join(HERE, "w", b.name)
        os.makedirs(os.path.join(d, "assets", "fonts"), exist_ok=True)
        for f in ("ProductSans-Regular.ttf", "ProductSans-Medium.ttf", "ProductSans-Bold.ttf"):
            shutil.copy(os.path.join(ROOT, "assets", "fonts", f), os.path.join(d, "assets", "fonts", f))
        shutil.copy(os.path.join(ROOT, "reel-09", "assets", "fonts", "ProductSans-Black.woff"),
                    os.path.join(d, "assets", "fonts", "ProductSans-Black.woff"))
        shutil.copy(os.path.join(ROOT, "assets", "grain.png"), os.path.join(d, "assets", "grain.png"))
        for f in b.assets:
            shutil.copy(f, os.path.join(d, "assets", os.path.basename(f)))
        for f in ("hyperframes.json", "package.json"):
            shutil.copy(os.path.join(ROOT, "reel-40", f), os.path.join(d, f))
        io.open(os.path.join(d, "meta.json"), "w").write('{ "id": "demo-%s", "name": "demo-%s" }' % (b.name, b.name))
        dur = (n - 0.5) / FPS
        io.open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(window_doc(b, dur, "assets/plate.mp4"))
        pl = os.path.join(d, "assets", "plate.mp4")
        if "--plates" in sys.argv and os.path.exists(plate):
            subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-ss", "%.4f" % (f0 / float(FPS)), "-i", plate,
                            "-frames:v", str(n), "-an", "-c:v", "libx264", "-preset", "fast", "-crf", "14",
                            "-pix_fmt", "yuv420p", "-r", str(FPS), pl], check=True)
        wins.append({"name": b.name, "f0": f0, "frames": n})
    for a, c in zip(wins, wins[1:]):
        assert a["f0"] + a["frames"] <= c["f0"], ("windows overlap", a, c)
    json.dump(wins, open(os.path.join(HERE, "windows.json"), "w"), indent=1)
    print("%d windows, %.1f s of graphics" % (len(wins), sum(w["frames"] for w in wins) / float(FPS)))


main()
