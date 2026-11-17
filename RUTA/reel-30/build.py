# -*- coding: utf-8 -*-
"""Reel 30 — «Мозок, руки, м'язова пам'ять». Posts 2026-10-12.

The one object is **an AI's body**, drawn as an anatomy chart and assembled
piece by piece on her words: the head (instructions + memory), the hands
(connectors: Notion, Metricool, Google Calendar), the muscle memory (skills),
and finally all of it wired into a routine ring — «це вже не промт, це система».

Chain:  near: a blueprint figure draws itself above her head, Claude drops into
its head, three anatomy pins -> OVER: the iris opens out of the head; the head
is the frame (a giant bust), «Інструкції» and «Пам'ять» land inside it -> the
iris closes onto Claude above her head: arms (cables) reach out to three ghost
sockets, Notion / metricool / Calendar light on their words -> «без них» the
hands drop, Claude alone thinks (ripples), three actions arrive and get a ✕
each -> OVER: the iris opens out of Claude: М'ЯЗОВА ПАМ'ЯТЬ, three skill cards,
switched on; the same explanation typed three times collapses into one task
that ticks itself -> the iris closes onto the tick: near, the morning — sun,
a toothbrush brushes, ✓ -> near: hands + memory wired to a hub, the ring of
the routine draws and runs by itself; her «explaining again» bubble gets ✕ ->
OVER: the iris opens out of the hub: a prompt bar is struck out, the whole
figure assembles inside the ring — СИСТЕМА — then shrinks over three client
cards that each get one -> the iris closes onto the comment bar: «+», posted.

usage: python build.py   (then: python ../tools/sfx.py mix 30)
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

CUT = json.load(io.open(os.path.join(ROOT, "work", "r30", "cut.json"), encoding="utf-8"))
DUR = 45.750           # (1373 plate frames - 0.5) / 30
FPS = 30
k = Kit(width=1080, height=1920, fps=FPS, duration=DUR)
g = Glass(["claude", "notion", "googlecalendar"])
k.css(g.css())

NO_PAINT = [tuple(x) for x in CUT["no_paint"]]      # empty on this cut

CAPS = k.load_captions(os.path.join(ROOT, "work", "r30", "captions.json"))
# whisper mangled these; script spelling restored (her script also writes
# «память» without the apostrophe — set as «пам'ять», the same word she has at 5.2 s)
FIX = {u"з'єдлені": u"з'єднані", u"працювави": u"спрацьовують", u"бюджую": u"будую",
       u"клієнтом.": u"клієнткам.", u"Хочеш": u"хочеш", u"Саме": u"саме",
       u"Мʼязова": u"М'язова", u"память": u"пам'ять"}
for c in CAPS:
    c["w"] = FIX.get(c["w"], c["w"]).replace(u"ʼ", u"'")
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
    "anat": S(u"Анатомія", 0.0), "shtuch": S(u"штучного", 0.85), "intel": S(u"інтелекту", 1.23),
    "dlia": S(u"для", 1.75), "povnykh": S(u"повних", 2.03), "novach": S(u"новачків", 2.51),
    "holova": S(u"Голова", 3.35), "instr": S(u"інструкції", 4.37), "instre": E(u"інструкції", 4.37),
    "pam1": S(u"пам'ять", 5.18), "pam1e": E(u"пам'ять", 5.18), "khto": S(u"хто", 6.03),
    "shcho": S(u"що", 6.71), "vidbuv": S(u"відбувається", 7.37), "vidbuve": E(u"відбувається", 7.37),
    "ruky": S(u"Руки", 8.19), "konekt": S(u"конектори", 9.11), "notion": S("Notion", 9.95),
    "metri": S("Metricool", 10.55), "metrie": E("Metricool", 10.55), "google": S("Google", 11.13),
    "bez": S(u"Без", 12.11), "klod": S(u"Клод", 12.41), "mozkom": S(u"мозком", 13.19),
    "use": S(u"усе", 13.83), "rozumie": S(u"розуміє", 14.19), "nichoho": S(u"нічого", 14.85),
    "opubl": S(u"опублікувати", 17.06), "vziaty": S(u"взяти", 17.96), "dani": S(u"дані", 18.32),
    "vidpov": S(u"відповісти", 19.08), "kliientue": E(u"клієнту", 19.58),
    "miaz": S(u"М'язова", 20.43), "pam2": S(u"пам'ять", 20.87), "pam2e": E(u"пам'ять", 20.87),
    "skily": S(u"скіли", 21.47), "skilye": E(u"скіли", 21.47), "nalasht": S(u"налаштовані", 22.35),
    "klodu": S(u"Клоду", 22.99), "shchorazu": S(u"щоразу", 23.65), "zadachu": S(u"задачу", 25.46),
    "prosto": S(u"просто", 26.12), "vykonuie": S(u"виконує", 26.92),
    "tak": S(u"так", 27.74), "kozhnoho": S(u"кожного", 28.90), "same": S(u"саме", 29.78),
    "chystyty": S(u"чистити", 30.22), "zuby": S(u"зуби", 30.58), "zubye": E(u"зуби", 30.58),
    "i3": S(u"І", 31.07), "ruky2": S(u"руки", 31.70), "pam3": S(u"пам'ять", 32.34),
    "pam3e": E(u"пам'ять", 32.34), "ziedn": S(u"з'єднані", 32.66), "rutyny": S(u"рутини", 33.42),
    "sprats": S(u"спрацьовують", 34.32), "sami": S(u"самі", 34.82), "bez2": S(u"без", 35.20),
    "poiasn2": S(u"пояснювала", 36.46), "zanovo": S(u"заново", 37.04),
    "vzhe": S(u"вже", 37.65), "ne2": S(u"не", 37.89), "promt": S(u"промт", 38.05),
    "systema": S(u"система", 38.62), "systemae": E(u"система", 38.62),
    "buduiu": S(u"будую", 40.94), "kliientkam": S(u"клієнткам", 41.22),
    "kliientkame": E(u"клієнткам", 41.22),
    "yakshcho": S(u"якщо", 42.13), "khochesh": S(u"хочеш", 42.77), "sebe": S(u"себе", 43.95),
    "pyshy": S(u"пиши", 44.37), "plius": S(u"плюс", 44.73), "pliuse": E(u"плюс", 44.73),
    "koment": S(u"коментарі", 45.09),
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
    "person": '<circle cx="12" cy="8.2" r="3.6"/><path d="M4.8 20c.9-3.8 3.7-5.8 7.2-5.8s6.3 2 7.2 5.8"/>',
    "doc": '<path d="M14 2.8H6.6a2 2 0 0 0-2 2v14.4a2 2 0 0 0 2 2h10.8a2 2 0 0 0 2-2V8.2z"/><path d="M14 2.8v5.4h5.4M8.4 13h7.2M8.4 16.8h4.8"/>',
    "layers": '<path d="M12 3.2l8.8 4.4-8.8 4.4-8.8-4.4z"/><path d="M3.2 12l8.8 4.4 8.8-4.4M3.2 16.4l8.8 4.4 8.8-4.4"/>',
    "folder": '<path d="M3.2 7a2 2 0 0 1 2-2h4l2 2.4h7.6a2 2 0 0 1 2 2V17a2 2 0 0 1-2 2H5.2a2 2 0 0 1-2-2z"/>',
    "send": '<path d="M21 3L10.2 13.8M21 3l-6.8 18-4-7.2-7.2-4z"/>',
    "phone": '<path d="M21.2 16.4v2.9a1.9 1.9 0 0 1-2.1 1.9 18.9 18.9 0 0 1-8.2-2.9 18.6 18.6 0 0 1-5.7-5.7A18.9 18.9 0 0 1 2.3 4.3a1.9 1.9 0 0 1 1.9-2.1h2.9a1.9 1.9 0 0 1 1.9 1.6c.1.9.4 1.8.7 2.7a1.9 1.9 0 0 1-.4 2L8 9.7a15.2 15.2 0 0 0 5.7 5.7l1.2-1.2a1.9 1.9 0 0 1 2-.4c.9.3 1.8.6 2.7.7a1.9 1.9 0 0 1 1.6 1.9z"/>',
    "chat": '<path d="M20.6 11.6a8.1 8.1 0 0 1-.9 3.7 8.2 8.2 0 0 1-7.3 4.5 8.1 8.1 0 0 1-3.7-.9L3.4 20.6l1.7-5.3a8.1 8.1 0 0 1-.9-3.7 8.2 8.2 0 0 1 4.5-7.3 8.1 8.1 0 0 1 3.7-.9h.5a8.2 8.2 0 0 1 7.7 7.7z"/>',
    "bolt": '<path d="M13 2.6L4.6 13.8h6.6l-1 7.6 8.4-11.2H12z"/>',
    "sun": '<circle cx="12" cy="12" r="4.2"/><path d="M12 2.6v2.2M12 19.2v2.2M2.6 12h2.2M19.2 12h2.2M5.4 5.4l1.6 1.6M17 17l1.6 1.6M5.4 18.6L7 17M17 7l1.6-1.6"/>',
    "repeat": '<path d="M20.4 4.6v5.2h-5.2M3.6 19.4v-5.2h5.2"/><path d="M5.3 9.2a7.4 7.4 0 0 1 12.3-2.8l2.8 3.4M3.6 14.2l2.8 3.4a7.4 7.4 0 0 0 12.3-2.8"/>',
    "heart": '<path d="M20.4 5a5.2 5.2 0 0 0-7.4 0L12 6l-1-1a5.2 5.2 0 0 0-7.4 7.4l1 1L12 20.8l7.4-7.4 1-1a5.2 5.2 0 0 0 0-7.4z"/>',
}


def stroke(name, cls="sk"):
    return '<svg class="%s" viewBox="0 0 24 24">%s</svg>' % (cls, STROKES[name])


def tile(tid, size, x, y, material, inner, extra_cls="", hide=True, ring=True, w=None):
    w = w or size
    rc = " rnd" if "circ" in extra_cls else ""
    r = ('<div class="sqring%s" id="%sR" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx"></div>'
         % (rc, tid, x, y, w, size)) if ring else ""
    return ('%s<div class="tw%s %s" id="%s" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx">'
            '<div class="%s">%s<div class="sheen"></div></div></div>'
            % (r, " hide" if hide else "", extra_cls, tid, x, y, w, size, material, inner))


def metricool(size=50):
    return '<span class="wmark" style="font-size:%dpx;letter-spacing:-0.035em">metricool</span>' % size


k.css("""
.abs { position: absolute; }
.hide { opacity: 0; visibility: hidden; }
.tw { position: absolute; }
.sk { fill: none; stroke: url(#gw); stroke-width: 2.3; stroke-linecap: round; stroke-linejoin: round;
  width: 50%; height: 50%; position: relative; z-index: 1; overflow: visible; }
.pearl .sk { stroke: #17141c; }
.circ .jelly, .circ .pearl, .circ .clear, .circ .sheen { border-radius: 50%; }
.sqring.rnd { border-radius: 50%; }
.pill .pearl, .pill .clear, .pill .sheen { border-radius: 75px; }
.aurs { position: absolute; left: -700px; top: -700px; width: 2480px; height: 3320px; pointer-events: none;
  background:
    radial-gradient(circle 526px at 1560px 880px, rgba(255,110,156,0.50), rgba(255,110,156,0)),
    radial-gradient(circle 634px at 760px 2360px, rgba(222,32,74,0.55), rgba(222,32,74,0)),
    radial-gradient(circle 382px at 1480px 1910px, rgba(255,198,214,0.20), rgba(255,198,214,0)); }

/* the blueprint figure */
.bp { fill: none; stroke: rgba(255,255,255,0.95); stroke-width: 7; stroke-linecap: round; stroke-linejoin: round; }
.pin { position: absolute; width: 44px; height: 44px; margin: -22px 0 0 -22px; border-radius: 50%;
  background: linear-gradient(165deg, #ff6e9c 0%, #e0204b 60%, #8d0d24 100%);
  box-shadow: 0 0 0 7px rgba(255,255,255,0.85), 0 0 26px 6px rgba(255,110,156,0.75); }

/* the bust (takeover head) */
.bust { position: absolute; inset: 0; }
.bust .hd { position: absolute; border-radius: 50%;
  background: linear-gradient(170deg, #ffffff 0%, #fff8fa 55%, #fbe8ee 100%);
  box-shadow: inset 0 3px 2px #fff, inset 0 -60px 120px -60px rgba(180,18,47,0.22), 0 80px 160px -50px rgba(8,0,3,0.8); }
.bust .sh { position: absolute; border-radius: 50% 50% 0 0 / 34% 34% 0 0;
  background: linear-gradient(175deg, #fbe6ec 0%, #f2d3dc 100%);
  box-shadow: inset 0 3px 2px rgba(255,255,255,0.9), 0 -20px 80px -30px rgba(8,0,3,0.6); }

/* cards on light grounds */
.crd { position: absolute; border-radius: 52px; overflow: hidden; color: #17141c;
  background: linear-gradient(168deg, #ffffff 0%, #fff7fa 60%, #fbe9ef 100%);
  box-shadow: inset 0 2px 1px #fff, 0 40px 80px -30px rgba(60,6,22,0.50), 0 0 0 1.5px rgba(180,18,47,0.07); }
.crd .ttl { position: absolute; font-weight: 700; letter-spacing: -0.02em; color: #17141c; white-space: nowrap; }
.crd .mic { position: absolute; font-size: 25px; font-weight: 700; letter-spacing: 0.16em; color: rgba(23,20,28,0.58); }
.rw { position: absolute; }
.num { position: absolute; left: 0; top: 0; width: 54px; height: 54px; border-radius: 50%; background: #fbe3ea;
  color: #b4122f; font-size: 29px; font-weight: 700; display: flex; align-items: center; justify-content: center; }
.rr { position: absolute; border-radius: 10px; background: rgba(23,20,28,0.13); }
.gc { position: absolute; border-radius: 50%; background: linear-gradient(160deg, #ffffff 0%, #fbe3ea 100%);
  box-shadow: inset 0 0 0 2px rgba(180,18,47,0.12); display: flex; align-items: center; justify-content: center; }
.gc .sk { stroke: #b4122f; width: 56%; height: 56%; }

/* the actions Claude can't do */
.arow { position: absolute; left: 36px; right: 36px; height: 120px; opacity: 0.32; }
.aic { position: absolute; left: 0; top: 12px; width: 96px; height: 96px; border-radius: 50%;
  background: rgba(255,255,255,0.14); box-shadow: inset 0 1.5px 1px rgba(255,255,255,0.55), inset 0 0 0 1.5px rgba(255,255,255,0.18);
  display: flex; align-items: center; justify-content: center; }
.aic .sk { stroke: #fff; width: 50%; height: 50%; }
.atx { position: absolute; left: 124px; top: 0; height: 120px; line-height: 120px; font-size: 37px; font-weight: 700;
  color: #fff; letter-spacing: -0.01em; white-space: nowrap; }
.ax { position: absolute; right: 0; top: 22px; width: 76px; height: 76px; }
.ax .jelly .sk { width: 54%; height: 54%; stroke: #fff; stroke-width: 3; }

/* skills */
.big { position: absolute; left: 0; width: 1080px; text-align: center; color: #fff; font-weight: 900;
  letter-spacing: -0.03em; white-space: nowrap; line-height: 1; }
.big span { display: inline-block; }
.trk { position: absolute; width: 84px; height: 48px; border-radius: 24px; background: rgba(23,20,28,0.14); }
.trk .on { position: absolute; inset: 0; border-radius: 24px; opacity: 0; visibility: hidden;
  background: linear-gradient(165deg, #ff6e9c 0%, #e0204b 100%); }
.trk .knob { position: absolute; left: 5px; top: 5px; width: 38px; height: 38px; border-radius: 50%; background: #fff;
  box-shadow: 0 3px 8px rgba(30,4,12,0.3); }
.bub { position: absolute; height: 98px; border-radius: 49px 49px 14px 49px;
  background: linear-gradient(165deg, #ff7aa6 0%, #e0204b 55%, #ab112e 100%);
  box-shadow: inset 0 2px 1px rgba(255,255,255,0.45), 0 18px 36px -16px rgba(70,4,20,0.55); }
.bub i { position: absolute; display: block; height: 16px; border-radius: 8px; background: rgba(255,255,255,0.88); }
.cbx { position: absolute; width: 76px; height: 76px; border-radius: 22px; box-shadow: inset 0 0 0 5px rgba(23,20,28,0.24); }
.cbf { position: absolute; inset: 0; border-radius: 22px; opacity: 0; visibility: hidden;
  background: linear-gradient(165deg, #e0204b 0%, #8d0d24 100%); }
.cbf svg { position: absolute; left: 10px; top: 10px; width: 56px; height: 56px; fill: none; stroke: #fff;
  stroke-width: 3.2; stroke-linecap: round; stroke-linejoin: round; }
.ck { position: absolute; width: 150px; height: 150px; margin: -75px 0 0 -75px; border-radius: 50%;
  border: 8px solid #ff6e9c; opacity: 0; visibility: hidden; }

/* morning */
.tb { position: absolute; overflow: visible; filter: drop-shadow(0 26px 30px rgba(24,4,12,0.45)); }

/* the routine */
.ringc .tube { fill: none; stroke: rgba(255,255,255,0.26); stroke-width: 22; stroke-linecap: round; }
.ringc .core { fill: none; stroke: rgba(255,255,255,0.95); stroke-width: 5; stroke-linecap: round; }
.dots { position: absolute; left: 0; right: 0; top: 0; bottom: 0; display: flex; align-items: center; justify-content: center; gap: 16px; }
.dots b { width: 20px; height: 20px; border-radius: 50%; background: #fff; display: block; }
.bubh { position: absolute; border-radius: 42px 42px 42px 12px;
  background: linear-gradient(165deg, #ff7aa6 0%, #e0204b 55%, #ab112e 100%);
  box-shadow: inset 0 2px 1px rgba(255,255,255,0.45), 0 22px 44px -18px rgba(40,2,12,0.6); }

/* system */
.pbar { position: absolute; border-radius: 75px; background: linear-gradient(170deg, #ffffff 0%, #fff6f9 100%);
  box-shadow: inset 0 2px 1px #fff, 0 50px 100px -36px rgba(8,0,3,0.75); }
.pbar .pt { position: absolute; left: 56px; top: 0; height: 150px; line-height: 150px; font-size: 42px; font-weight: 500;
  color: rgba(23,20,28,0.62); white-space: nowrap; }
.strk { position: absolute; left: 30px; right: 30px; top: 71px; height: 9px; border-radius: 5px; background: #e0204b;
  transform-origin: 0 50%; }
.chipw { position: absolute; width: 380px; height: 84px; border-radius: 42px; padding: 0 30px 0 18px; display: flex; align-items: center; gap: 14px;
  background: linear-gradient(170deg, #ffffff 0%, #fff4f7 100%); color: #17141c; font-size: 36px; font-weight: 700; white-space: nowrap;
  box-shadow: inset 0 2px 1px #fff, 0 22px 44px -18px rgba(8,0,3,0.6); }
.chipw .gc { position: relative; width: 56px; height: 56px; flex: none; }

/* the comment */
.cmb { position: absolute; border-radius: 75px; }
.cmb .cph { position: absolute; left: 150px; top: 0; height: 150px; line-height: 150px; font-size: 38px; font-weight: 500;
  color: rgba(255,255,255,0.6); white-space: nowrap; }
.cmb .pl { position: absolute; left: 150px; top: 0; height: 150px; line-height: 146px; font-size: 76px; font-weight: 900; color: #fff; }
.cmb .go { position: absolute; right: 44px; top: 0; height: 150px; line-height: 150px; font-size: 35px; font-weight: 700;
  color: #ff9fbf; white-space: nowrap; }
.cmb .hr { position: absolute; right: 44px; top: 43px; width: 64px; height: 64px; }
.cmb .hr .sk { width: 100%; height: 100%; stroke: #fff; stroke-width: 2; }
.cmb .hrf { fill: #ff4f86; stroke: #ff4f86; }
.shc { position: absolute; inset: 0; border-radius: inherit; overflow: hidden; pointer-events: none; }
.shc .sheen { mix-blend-mode: normal; opacity: 0.4; }
""")

L = []
BEATS = []


def beat(fn):
    BEATS.append(fn)
    return fn


def ground():
    return '<div class="tkg"></div><div class="aurs"></div><div class="grain"></div>'


# ===========================================================================
# A · hook — the anatomy chart draws itself above her head
SHX, SHY = 80, 100            # shelf origin


@beat
def a_hook():
    fig = ('<svg class="abs" width="920" height="490" viewBox="0 0 920 490" style="left:0;top:0;overflow:visible">'
           '<circle class="bp" id="aHd" cx="460" cy="125" r="82"/>'
           '<path class="bp" id="aTo" d="M372 238 Q460 214 548 238 L566 452 Q460 476 354 452 Z"/>'
           '<path class="bp" id="aAL" d="M378 254 C300 276 236 300 172 326"/>'
           '<path class="bp" id="aAR" d="M542 254 C620 276 684 300 748 326"/>'
           '<circle class="bp" id="aHL" cx="132" cy="342" r="42"/>'
           '<circle class="bp" id="aHR" cx="788" cy="342" r="42"/>'
           '</svg>')
    shelf = ('<div class="shelf edge hide" id="aSh" style="left:%dpx;top:%dpx;width:920px;height:490px">%s</div>'
             % (SHX, SHY, fig))
    pins = "".join('<div class="pin hide" id="aP%d" style="left:%dpx;top:%dpx"></div>' % (i, x, y)
                   for i, (x, y) in enumerate(((SHX + 132, SHY + 342), (SHX + 460, SHY + 350),
                                               (SHX + 788, SHY + 342))))
    L.append('<div class="g full" id="gA">' + shelf + pins
             + tile("aCl", 150, 465, 150, "jelly", g.mark("claude"), extra_cls="circ") + '</div>')
    sfx("pop", T["shtuch"] + 0.05, -2)
    sfx("click-soft", T["novach"] + 0.05)
    return js("""
  tl.set("#gA", {autoAlpha: 1}, 0);
  arr("#aSh", 0.0, {s: 0.86, y: 30, d: 0.8});
  draw2("aHd", 0.12, 0.5); draw2("aTo", 0.3, 0.6); draw2("aAL", 0.5, 0.45); draw2("aAR", 0.5, 0.45);
  draw2("aHL", 0.85, 0.35); draw2("aHR", 0.85, 0.35);
  arr("#aCl", @shtuch-0.04, {s: 0.3, y: 0, d: 0.7});
  G.ripple("#aClR", @intel+0.05);
  [["#aP0", @dlia-0.02], ["#aP1", @povnykh-0.02], ["#aP2", @novach]].forEach(function (p) {
    tl.fromTo(p[0], {autoAlpha: 0, scale: 0.2}, {autoAlpha: 1, scale: 1, duration: 0.45, ease: POP}, p[1]);
  });
  tl.set("#gA", {autoAlpha: 0}, @holova+0.5);""")


# ===========================================================================
# B · OVER — the head is the frame: instructions + memory
@beat
def b_head():
    rows_in = "".join(
        '<div class="rw" style="left:40px;top:%dpx;width:360px;height:54px"><div class="num">%d</div>'
        '<i class="rr" style="left:76px;top:17px;width:%dpx;height:20px"></i></div>'
        % (262 + i * 80, i + 1, w) for i, w in enumerate((270, 236, 284, 180)))
    card_in = ('<div class="crd hide" id="bIn" style="left:80px;top:440px;width:440px;height:580px">'
               '<div class="tw" style="left:40px;top:40px;width:96px;height:96px"><div class="jelly">%s</div></div>'
               '<div class="ttl" style="left:40px;top:160px;font-size:52px">Інструкції</div>%s'
               '<div class="shc"><div class="sheen"></div></div></div>' % (stroke("doc"), rows_in))
    card_me = ('<div class="crd hide" id="bMe" style="left:560px;top:440px;width:440px;height:580px">'
               '<div class="tw" style="left:40px;top:40px;width:96px;height:96px"><div class="jelly">%s</div></div>'
               '<div class="ttl" style="left:40px;top:160px;font-size:52px">Пам\'ять</div>'
               '<div class="rw hide" id="bM0" style="left:40px;top:262px;width:360px;height:96px">'
               '<div class="gc" style="left:0;top:0;width:96px;height:96px">%s</div>'
               '<i class="rr" style="left:122px;top:20px;width:210px;height:22px"></i>'
               '<i class="rr" style="left:122px;top:56px;width:150px;height:18px;opacity:0.7"></i></div>'
               '<div class="rw hide" id="bM1" style="left:40px;top:400px;width:360px;height:96px">'
               '<div class="gc" style="left:0;top:0;width:96px;height:96px">%s</div>'
               '<i class="rr" style="left:122px;top:20px;width:228px;height:22px"></i>'
               '<i class="rr" style="left:122px;top:56px;width:120px;height:18px;opacity:0.7"></i></div>'
               '<div class="shc"><div class="sheen"></div></div></div>'
               % (stroke("layers"), stroke("person"), stroke("folder")))
    bust = ('<div class="bust hide" id="bBu">'
            '<div class="sh" style="left:-220px;top:1300px;width:1520px;height:900px"></div>'
            '<div class="hd" style="left:-50px;top:110px;width:1180px;height:1180px"></div></div>')
    L.append('<div class="g full" id="gB">' + ground() + bust
             + tile("bCl", 150, 465, 230, "jelly", g.mark("claude"), extra_cls="circ")
             + card_in + card_me + '</div>')
    sfx("whoosh-short", T["holova"] - 0.2)
    sfx("pop", T["instr"])
    return js("""
  G.irisOpen("#gB", @holova-0.2, 540, 225, 0.6);
  drift1("#gB", @holova-0.2, @vidbuve-@holova);
  gsap.set("#bBu", {transformOrigin: "540px 225px"});
  arr("#bBu", @holova-0.18, {s: 0.14, y: 0, d: 0.95, blur: 6});
  arr("#bCl", @holova+0.1, {s: 0.5, y: -40, d: 0.7});
  arr("#bIn", @instr-0.1, {s: 0.6, y: 50});
  shn("#bIn .sheen", @instr+0.3);
  tl.fromTo("#bIn .rw", {autoAlpha: 0, x: -24}, {autoAlpha: 1, x: 0, duration: 0.35, stagger: 0.1, ease: "power2.out"}, @instr+0.3);
  arr("#bMe", @pam1-0.1, {s: 0.6, y: 50});
  shn("#bMe .sheen", @pam1+0.3);
  arr("#bM0", @khto-0.06, {s: 0.7, x: -20, y: 0, d: 0.55});
  arr("#bM1", @shcho-0.06, {s: 0.7, x: -20, y: 0, d: 0.55});
  tl.to(["#bIn", "#bMe"], {scale: 0.25, autoAlpha: 0, y: -380, duration: 0.36, ease: "power2.in"}, @vidbuve-0.42);
  G.irisClose("#gB", @vidbuve-0.25, 540, 180, 0.45);""")


# ===========================================================================
# C + D · near — the hands (connectors), then «без них»
@beat
def c_hands():
    paths = {"0": "M480 240 C 420 300 290 330 230 398",
             "1": "M540 265 L540 408",
             "2": "M600 240 C 660 300 790 330 850 398"}
    cab = '<svg class="cab abs" width="1080" height="700" viewBox="0 0 1080 700" style="left:0;top:0">'
    for i, d in sorted(paths.items()):
        cab += ('<path class="tube hide" id="cT%s" d="%s"/><path class="core hide" id="cC%s" d="%s"/>'
                '<g class="pkg"><path class="pkt" id="cP%s" style="opacity:0" d="%s"/></g>' % (i, d, i, d, i, d))
    cab += '</svg>'
    ghosts = ('<div class="tw hide" id="cG0" style="left:145px;top:400px;width:170px;height:170px">'
              '<div class="clear" style="opacity:0.55">%s</div></div>'
              '<div class="tw hide pill" id="cG1" style="left:390px;top:410px;width:300px;height:150px">'
              '<div class="clear" style="opacity:0.55">%s</div></div>'
              '<div class="tw hide" id="cG2" style="left:765px;top:400px;width:170px;height:170px">'
              '<div class="clear" style="opacity:0.55">%s</div></div>'
              % (g.mark("notion"), metricool(46), g.mark("googlecalendar")))
    rows = ""
    for i, (gl, tx) in enumerate((("send", u"Опублікувати"), ("phone", u"Взяти дані з дзвінка"),
                                   ("chat", u"Відповісти клієнту"))):
        rows += ('<div class="arow" id="dR%d" style="top:%dpx"><div class="aic">%s</div><div class="atx">%s</div>'
                 '<div class="ax tw hide circ" id="dX%d"><div class="jelly">%s</div></div></div>'
                 % (i, 34 + i * 140, stroke(gl), tx, i, stroke("x")))
    panel = ('<div class="dglass edge hide" id="dP" style="left:312px;top:100px;width:720px;height:488px">%s</div>'
             % rows)
    rings = "".join('<div class="sqring rnd" id="dRg%d" style="left:455px;top:95px;width:170px;height:170px"></div>' % i
                    for i in range(3))
    L.append('<div class="g full" id="gC">' + cab + ghosts
             + tile("cNo", 170, 145, 400, "pearl", g.mark("notion"))
             + tile("cMe", 150, 390, 410, "pearl", metricool(46), extra_cls="pill", w=300)
             + tile("cGc", 170, 765, 400, "pearl", g.mark("googlecalendar"))
             + rings + tile("cCl", 170, 455, 95, "jelly", g.mark("claude"), extra_cls="circ", ring=False)
             + panel + '</div>')
    sfx("pop", T["notion"], -2)
    sfx("pop", T["metri"], -2)
    sfx("pop", T["google"], -2)
    sfx("sparkle", T["use"])
    sfx("click", T["opubl"] + 0.5)
    sfx("click", T["kliientue"] - 0.45)
    return js("""
  tl.set("#gC", {autoAlpha: 1}, @vidbuve-0.3);
  arr("#cCl", @vidbuve-0.24, {s: 0.55, y: 0, d: 0.7});
  ["0", "1", "2"].forEach(function (i, n) {
    tl.set(["#cT" + i, "#cC" + i], {autoAlpha: 1}, @ruky-0.04 + n * 0.08);
    draw2("cT" + i, @ruky-0.04 + n * 0.08, 0.5); draw2("cC" + i, @ruky-0.04 + n * 0.08, 0.5);
  });
  arr(["#cG0", "#cG1", "#cG2"], @konekt-0.05, {s: 0.6, y: 20, d: 0.6});
  [["0", "#cNo", "#cG0", @notion], ["1", "#cMe", "#cG1", @metri], ["2", "#cGc", "#cG2", @google]].forEach(function (p) {
    G.packet("cP" + p[0], p[3] - 0.36, 0.36);
    arr(p[1], p[3] - 0.02, {s: 0.7, y: 0, d: 0.6, blur: 8});
    G.ripple(p[1] + "R", p[3] + 0.1);
    tl.set(p[2], {autoAlpha: 0}, p[3] + 0.3);
  });
  /* без них — the hands drop off, Claude is left alone */
  tl.to(["#cNo", "#cMe", "#cGc"], {y: 110, autoAlpha: 0, filter: "blur(8px)", duration: 0.42, ease: "power2.in", stagger: 0.06}, @bez);
  tl.to(["#cT0", "#cC0", "#cT1", "#cC1", "#cT2", "#cC2"], {autoAlpha: 0, duration: 0.3}, @bez+0.05);
  G.bump("#cCl", @klod);
  tl.to("#cCl", {x: -345, y: 155, duration: 0.75, ease: SP}, @nichoho-0.2);
  [0, 1, 2].forEach(function (i) {
    tl.fromTo("#dRg" + i, {scale: 1, autoAlpha: 0.8}, {scale: 1.9, autoAlpha: 0, duration: 0.85, ease: "power2.out", immediateRender: false}, @use-0.05 + i * 0.28);
  });
  /* ...but can't do anything */
  arr("#dP", @nichoho-0.05, {s: 0.8, x: 60, y: 0});
  [["0", @opubl], ["1", @vziaty], ["2", @vidpov]].forEach(function (p) {
    tl.to("#dR" + p[0], {opacity: 1, duration: 0.25}, p[1] - 0.04);
    arr("#dX" + p[0], p[1] + 0.45, {s: 0.2, y: 0, d: 0.5, blur: 6});
    G.haptic("#dR" + p[0], p[1] + 0.5);
  });
  bout(["#dP", "#cCl"], @kliientue-0.12, 10, 0.3);
  tl.set("#gC", {autoAlpha: 0}, @miaz+0.6);""")


# ===========================================================================
# E · OVER — muscle memory = skills; the same explanation, then one task done
@beat
def e_skills():
    cards = ""
    for i in range(3):
        x = 40 + i * 350
        cards += ('<div class="crd hide" id="eK%d" style="left:%dpx;top:330px;width:300px;height:290px;border-radius:48px">'
                  '<div class="tw" style="left:30px;top:30px;width:96px;height:96px"><div class="jelly">%s</div></div>'
                  '<div class="trk" style="left:186px;top:54px"><div class="on" id="eOn%d"></div><div class="knob" id="eKn%d"></div></div>'
                  '<div class="mic" style="left:32px;top:156px">СКІЛ</div>'
                  '<i class="rr" style="left:32px;top:204px;width:%dpx;height:20px"></i>'
                  '<i class="rr" style="left:32px;top:238px;width:%dpx;height:16px;opacity:0.7"></i>'
                  '<div class="shc"><div class="sheen"></div></div></div>'
                  % (i, x, stroke("bolt"), i, i, (210, 186, 228)[i], (140, 166, 118)[i]))
    bubs = "".join('<div class="bub hide" id="eB%d" style="right:40px;top:%dpx;width:640px">'
                   '<i style="left:40px;top:28px;width:470px"></i><i style="left:40px;top:56px;width:330px"></i></div>'
                   % (i, 136 + i * 118) for i in range(3))
    task = ('<div class="rw hide" id="eTk" style="left:60px;top:200px;width:840px;height:120px">'
            '<div class="cbx" style="left:0;top:0"><div class="cbf" id="eCb"><svg viewBox="0 0 24 24">'
            '<path id="eCp" d="M5.4 12.6l4.3 4.3 8.9-9.5"/></svg></div></div>'
            '<i class="rr" style="left:112px;top:12px;width:560px;height:28px;border-radius:14px"></i>'
            '<i class="rr" style="left:112px;top:56px;width:380px;height:20px;opacity:0.7"></i>'
            '<div class="ck" id="eCk" style="left:38px;top:38px"></div></div>')
    sheet = ('<div class="sheet hide" id="eS" style="left:60px;top:690px;width:960px;height:540px">'
             '<div class="tw" style="left:40px;top:34px;width:76px;height:76px"><div class="jelly">%s</div></div>'
             '<div class="ttl" style="position:absolute;left:136px;top:44px;font-size:44px;font-weight:700">Claude</div>'
             '%s%s<div class="shc"><div class="sheen"></div></div></div>' % (g.mark("claude"), bubs, task))
    head = ('<div class="big" id="eH" style="top:170px;font-size:88px">'
            '<span class="hide" id="eH1">М\'ЯЗОВА</span> <span class="hide" id="eH2">ПАМ\'ЯТЬ</span></div>')
    L.append('<div class="g full" id="gE">' + ground() + head + cards + sheet + '</div>')
    sfx("whoosh-short", T["miaz"] - 0.12)
    sfx("pop", T["skily"])
    sfx("click-soft", T["nalasht"] + 0.08)
    sfx("pop", T["vykonuie"] + 0.02)
    return js("""
  G.irisOpen("#gE", @miaz-0.12, 195, 335, 0.62);
  drift1("#gE", @miaz-0.12, @vykonuie+0.8-@miaz);
  arr("#eH1", @miaz-0.02, {s: 0.6, y: 24, d: 0.6});
  arr("#eH2", @pam2-0.02, {s: 0.6, y: 24, d: 0.6});
  [0, 1, 2].forEach(function (i) {
    arr("#eK" + i, @skily-0.06 + i * 0.09, {s: 0.5, y: 70});
    tl.to("#eKn" + i, {x: 36, duration: 0.32, ease: SP}, @nalasht+0.05 + i * 0.1);
    tl.to("#eOn" + i, {autoAlpha: 1, duration: 0.2}, @nalasht+0.05 + i * 0.1);
  });
  arr("#eS", @klodu-0.1, {s: 0.8, y: 90});
  [0, 1, 2].forEach(function (i) { arr("#eB" + i, @shchorazu-0.08 + i * 0.27, {s: 0.7, x: 60, y: 10, d: 0.55}); });
  tl.to(["#eB0", "#eB1", "#eB2"], {scaleY: 0, autoAlpha: 0, duration: 0.3, stagger: 0.05, ease: "power2.in"}, @zadachu-0.12);
  arr("#eTk", @zadachu+0.12, {s: 0.7, y: 20, d: 0.6});
  G.bump("#eK1", @prosto); shn("#eK1 .sheen", @prosto);
  tl.fromTo("#eCb", {autoAlpha: 0, scale: 0.4}, {autoAlpha: 1, scale: 1, duration: 0.4, ease: POP}, @vykonuie);
  draw2("eCp", @vykonuie+0.06, 0.3);
  tl.fromTo("#eCk", {scale: 0.3, autoAlpha: 0.95}, {scale: 1.7, autoAlpha: 0, duration: 0.6, ease: "power2.out", immediateRender: false}, @vykonuie+0.02);
  G.irisClose("#gE", @vykonuie+0.48, 158, 928, 0.45);""")


# ===========================================================================
# F · near — the morning: sun, toothbrush, ✓
TOOTHBRUSH = (
    '<svg class="tb hide" id="fTb" viewBox="0 0 600 210" width="640" height="224" style="left:330px;top:236px">'
    '<defs><linearGradient id="tbg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ff8ab0"/>'
    '<stop offset="0.55" stop-color="#e0204b"/><stop offset="1" stop-color="#8d0d24"/></linearGradient></defs>'
    '<g id="fTbI">'
    '<rect x="14" y="132" width="400" height="50" rx="25" fill="url(#tbg)"/>'
    '<rect x="70" y="140" width="190" height="14" rx="7" fill="rgba(255,255,255,0.45)"/>'
    '<path d="M400 140 L460 146 L460 168 L400 174 Z" fill="url(#tbg)"/>'
    '<rect x="450" y="132" width="140" height="48" rx="22" fill="url(#tbg)"/>'
    '%s'
    '<path d="M458 70 C 470 44 492 58 506 46 C 520 34 540 52 556 42 C 572 34 588 50 584 70 Z" fill="#ffffff"/>'
    '<path d="M470 62 C 490 52 510 64 530 54 C 548 46 566 58 578 56" fill="none" stroke="#ff6e9c" stroke-width="7" stroke-linecap="round"/>'
    '</g></svg>' % "".join('<rect x="%d" y="72" width="17" height="62" rx="7" fill="#ffffff" stroke="rgba(23,20,28,0.12)" stroke-width="2"/>'
                          % (462 + i * 21) for i in range(6)))


@beat
def f_morning():
    L.append('<div class="g full" id="gF">'
             '<div class="shelf edge hide" id="fSh" style="left:80px;top:120px;width:920px;height:400px"></div>'
             + tile("fSu", 180, 130, 256, "jelly", stroke("sun"), extra_cls="circ")
             + TOOTHBRUSH
             + tile("fOk", 96, 860, 150, "jelly", stroke("check"), extra_cls="circ", ring=False)
             + '</div>')
    sfx("sparkle", T["zuby"] + 0.05, -2)
    return js("""
  tl.set("#gF", {autoAlpha: 1}, @tak-0.15);
  arr("#fSh", @tak-0.1, {s: 0.85, y: 30});
  arr("#fSu", @kozhnoho-0.04, {s: 0.4, y: 110, d: 0.85});
  tl.fromTo("#fSu .sk", {rotation: -60, transformOrigin: "50% 50%"}, {rotation: 0, duration: 1.1, ease: SP}, @kozhnoho);
  G.ripple("#fSuR", @kozhnoho+0.4);
  arr("#fTb", @same-0.05, {s: 0.7, x: 160, y: 0, d: 0.7});
  tl.to("#fTbI", {keyframes: {x: [0, -28, 22, -28, 22, -16, 0]}, duration: 0.78, ease: "none"}, @chystyty+0.02);
  arr("#fOk", @zuby, {s: 0.2, y: 0, d: 0.55});
  bout("#gF", @zubye+0.02, 10, 0.26);""")


# ===========================================================================
# G · near — hands + memory wired into the routine, which runs itself
@beat
def g_routine():
    cab = ('<svg class="cab abs" width="1080" height="700" viewBox="0 0 1080 700" style="left:0;top:0">'
           '<path class="tube hide" id="gW0" d="M262 245 C 330 245 350 320 412 336"/>'
           '<path class="core hide" id="gV0" d="M262 245 C 330 245 350 320 412 336"/>'
           '<path class="tube hide" id="gW1" d="M262 435 C 330 435 350 370 412 354"/>'
           '<path class="core hide" id="gV1" d="M262 435 C 330 435 350 370 412 354"/>'
           '<path class="tube hide" id="gW2" d="M756 345 L 668 345"/>'
           '<path class="core hide" id="gV2" d="M756 345 L 668 345"/></svg>')
    ring = ('<svg class="ringc cab abs" width="1080" height="700" viewBox="0 0 1080 700" style="left:0;top:0">'
            '<path class="tube hide" id="gRt" d="M540 220 A125 125 0 1 1 539.9 220"/>'
            '<path class="core hide" id="gRc" d="M540 220 A125 125 0 1 1 539.9 220"/>'
            '<g class="pkg"><path class="pkt" id="gRp" style="opacity:0" d="M540 220 A125 125 0 1 1 539.9 220"/></g></svg>')
    mem = ('<div class="crd hide" id="gMe" style="left:756px;top:205px;width:250px;height:280px;border-radius:44px">'
           '<div class="ttl" style="left:28px;top:26px;font-size:38px">Пам\'ять</div>'
           '<div class="gc" style="left:28px;top:96px;width:64px;height:64px">%s</div>'
           '<i class="rr" style="left:108px;top:110px;width:112px;height:16px"></i>'
           '<i class="rr" style="left:108px;top:136px;width:76px;height:14px;opacity:0.7"></i>'
           '<div class="gc" style="left:28px;top:186px;width:64px;height:64px">%s</div>'
           '<i class="rr" style="left:108px;top:200px;width:124px;height:16px"></i>'
           '<i class="rr" style="left:108px;top:226px;width:68px;height:14px;opacity:0.7"></i></div>'
           % (stroke("person"), stroke("folder")))
    bub = ('<div class="bubh hide" id="gBb" style="left:400px;top:108px;width:280px;height:84px">'
           '<div class="dots"><b></b><b></b><b></b></div></div>')
    L.append('<div class="g full" id="gG">'
             '<div class="shelf edge hide" id="gSh" style="left:60px;top:100px;width:960px;height:490px"></div>'
             + cab + ring
             + tile("gNo", 140, 122, 175, "pearl", g.mark("notion"))
             + tile("gGc", 140, 122, 365, "pearl", g.mark("googlecalendar"))
             + mem
             + tile("gHub", 150, 465, 270, "jelly", stroke("repeat"), extra_cls="circ")
             + bub + tile("gBx", 64, 650, 96, "jelly", stroke("x"), extra_cls="circ", ring=False)
             + '</div>')
    sfx("pop", T["ruky2"], -3)
    sfx("click-soft", T["rutyny"])
    sfx("click", T["poiasn2"] + 0.1)
    return js("""
  tl.set("#gG", {autoAlpha: 1}, @i3-0.1);
  arr("#gSh", @i3-0.06, {s: 0.86, y: 30});
  arr("#gNo", @ruky2-0.06, {s: 0.5, x: -40, y: 0, d: 0.7});
  arr("#gGc", @ruky2+0.06, {s: 0.5, x: -40, y: 0, d: 0.7});
  arr("#gMe", @pam3-0.06, {s: 0.6, x: 40, y: 0});
  arr("#gHub", @ziedn-0.12, {s: 0.4, y: 0, d: 0.7});
  ["0", "1", "2"].forEach(function (i, n) {
    tl.set(["#gW" + i, "#gV" + i], {autoAlpha: 1}, @ziedn+0.05 + n * 0.06);
    draw2("gW" + i, @ziedn+0.05 + n * 0.06, 0.42); draw2("gV" + i, @ziedn+0.05 + n * 0.06, 0.42);
  });
  tl.set(["#gRt", "#gRc"], {autoAlpha: 1}, @rutyny-0.06);
  draw2("gRt", @rutyny-0.06, 0.7); draw2("gRc", @rutyny-0.06, 0.7);
  G.ripple("#gHubR", @rutyny+0.3);
  tl.fromTo("#gHub .sk", {rotation: 0, transformOrigin: "50% 50%"}, {rotation: 360, duration: 1.0, ease: "power2.inOut"}, @sprats);
  G.packet("gRp", @sprats, 0.75);
  G.packet("gRp", @sami+0.12, 0.75);
  /* without her explaining it again */
  arr("#gBb", @bez2-0.04, {s: 0.5, y: 30, d: 0.6});
  tl.to("#gBb .dots b", {keyframes: {y: [0, -10, 0]}, duration: 0.42, stagger: 0.12, ease: "none"}, @bez2+0.35);
  tl.to("#gBb .dots b", {keyframes: {y: [0, -10, 0]}, duration: 0.42, stagger: 0.12, ease: "none"}, @bez2+0.85);
  arr("#gBx", @poiasn2+0.08, {s: 0.2, y: 0, d: 0.5, blur: 6});
  G.haptic("#gBb", @poiasn2+0.12);
  bout(["#gBb", "#gBx"], @zanovo+0.1, 10, 0.3);
  tl.set("#gG", {autoAlpha: 0}, @vzhe+0.6);""")


# ===========================================================================
# H · OVER — not a prompt: the whole figure, inside the ring. СИСТЕМА.
@beat
def h_system():
    arms = ('<svg class="cab abs" width="1080" height="1920" viewBox="0 0 1080 1920" style="left:0;top:0">'
            '<path class="tube" id="hA0" d="M440 570 C 330 600 236 650 216 758"/>'
            '<path class="core" id="hA0c" d="M440 570 C 330 600 236 650 216 758"/>'
            '<path class="tube" id="hA1" d="M640 570 C 750 600 844 650 864 758"/>'
            '<path class="core" id="hA1c" d="M640 570 C 750 600 844 650 864 758"/></svg>')
    ring = ('<svg class="ringc cab abs" width="1080" height="1920" viewBox="0 0 1080 1920" style="left:0;top:0">'
            '<path class="tube" id="hRt" d="M540 330 A440 440 0 1 1 539.9 330"/>'
            '<path class="core" id="hRc" d="M540 330 A440 440 0 1 1 539.9 330"/>'
            '<g class="pkg"><path class="pkt" id="hRp" style="opacity:0" d="M540 330 A440 440 0 1 1 539.9 330"/></g></svg>')
    torso = ('<div class="chipw hide" id="hI" style="left:350px;top:706px">'
             '<div class="gc">%s</div>Інструкції</div>'
             '<div class="chipw hide" id="hM" style="left:350px;top:806px">'
             '<div class="gc">%s</div>Пам\'ять</div>' % (stroke("doc"), stroke("layers")))
    fig = ('<div class="abs" id="hF" style="left:0;top:0;width:1080px;height:1920px">'
           '<div class="big hide" id="hT" style="top:150px;font-size:132px">СИСТЕМА</div>'
           + ring + arms
           + tile("hNo", 170, 131, 760, "pearl", g.mark("notion"))
           + tile("hGc", 170, 779, 760, "pearl", g.mark("googlecalendar"))
           + tile("hS0", 96, 250, 576, "jelly", stroke("bolt"), extra_cls="circ", ring=False)
           + tile("hS1", 96, 734, 576, "jelly", stroke("bolt"), extra_cls="circ", ring=False)
           + tile("hCl", 220, 430, 420, "jelly", g.mark("claude"), extra_cls="circ")
           + torso + '</div>')
    pbar = ('<div class="pbar hide" id="hPb" style="left:90px;top:330px;width:900px;height:150px">'
            '<div class="pt">Напиши пост про…</div>'
            '<div class="tw circ" style="left:776px;top:22px;width:106px;height:106px"><div class="jelly">%s</div></div>'
            '<div class="strk" id="hSt"></div></div>' % stroke("send"))
    clients = ""
    for i in range(3):
        x = 40 + i * 350
        clients += ('<div class="crd hide" id="hK%d" style="left:%dpx;top:930px;width:300px;height:250px;border-radius:46px">'
                    '<div class="gc" style="left:30px;top:30px;width:110px;height:110px">%s</div>'
                    '<i class="rr" style="left:30px;top:168px;width:%dpx;height:22px"></i>'
                    '<i class="rr" style="left:30px;top:204px;width:%dpx;height:16px;opacity:0.7"></i>'
                    '<div class="tw circ hide" id="hKb%d" style="left:176px;top:36px;width:96px;height:96px">'
                    '<div class="jelly">%s<div class="sheen"></div></div></div></div>'
                    % (i, x, stroke("person"), (200, 170, 220)[i], (120, 150, 96)[i], i, stroke("repeat")))
    L.append('<div class="g full" id="gH">' + ground() + pbar + fig + clients + '</div>')
    sfx("whoosh-short", T["vzhe"] - 0.12)
    sfx("pop", T["systema"])
    return js("""
  G.irisOpen("#gH", @vzhe-0.12, 540, 345, 0.6);
  drift1("#gH", @vzhe-0.12, @kliientkame+0.3-@vzhe);
  arr("#hPb", @vzhe-0.04, {s: 0.7, y: 40, d: 0.6});
  gsap.set("#hSt", {scaleX: 0});
  tl.to("#hSt", {scaleX: 1, duration: 0.3, ease: "power2.out"}, @ne2);
  tl.to("#hPb", {scale: 0.55, y: -150, autoAlpha: 0, filter: "blur(8px)", duration: 0.35, ease: "power2.in"}, @promt+0.12);
  /* the whole figure, assembled */
  ["hA0", "hA0c", "hA1", "hA1c", "hRt", "hRc"].forEach(function (id) { gsap.set("#" + id, {autoAlpha: 0}); });
  arr("#hCl", @promt+0.28, {s: 0.4, y: 0, d: 0.7});
  ["hA0", "hA0c", "hA1", "hA1c"].forEach(function (id) { tl.set("#" + id, {autoAlpha: 1}, @promt+0.4); draw2(id, @promt+0.4, 0.4); });
  arr("#hNo", @systema-0.12, {s: 0.5, y: 0, d: 0.6, blur: 8});
  arr("#hGc", @systema-0.06, {s: 0.5, y: 0, d: 0.6, blur: 8});
  arr("#hS0", @systema, {s: 0.3, y: 0, d: 0.55});
  arr("#hS1", @systema+0.06, {s: 0.3, y: 0, d: 0.55});
  arr("#hI", @systema+0.08, {s: 0.6, y: 20, d: 0.6});
  arr("#hM", @systema+0.16, {s: 0.6, y: 20, d: 0.6});
  arr("#hT", @systema-0.04, {s: 0.7, y: -20, d: 0.7});
  ["hRt", "hRc"].forEach(function (id) { tl.set("#" + id, {autoAlpha: 1}, @systema+0.1); draw2(id, @systema+0.1, 0.8); });
  G.ripple("#hClR", @systema+0.3);
  G.packet("hRp", @systema+0.95, 0.9);
  /* ...the one I build for clients */
  gsap.set("#hF", {transformOrigin: "540px 120px"});
  tl.to("#hF", {scale: 0.6, duration: 0.7, ease: SP}, @buduiu-0.35);
  [0, 1, 2].forEach(function (i) {
    arr("#hK" + i, @buduiu-0.2 + i * 0.09, {s: 0.6, y: 80});
    arr("#hKb" + i, @kliientkam+0.02 + i * 0.1, {s: 0.3, y: 0, d: 0.55});
  });
  G.irisClose("#gH", @kliientkame-0.12, 540, 470, 0.45);""")


# ===========================================================================
# I · near — пиши «+» в коментарі
@beat
def i_cta():
    bar = ('<div class="dglass edge cmb hide" id="iCb" style="left:60px;top:430px;width:960px;height:150px">'
           '<div class="tw circ" style="left:25px;top:25px;width:100px;height:100px"><div class="pearl">%s</div></div>'
           '<div class="cph" id="iPh">Додайте коментар…</div>'
           '<div class="pl hide" id="iPl">+</div>'
           '<div class="go" id="iGo">Опублікувати</div></div>' % stroke("person"))
    posted = ('<div class="dglass edge cmb hide" id="iCm" style="left:60px;top:200px;width:960px;height:150px">'
              '<div class="tw circ" style="left:25px;top:25px;width:100px;height:100px"><div class="pearl">%s</div></div>'
              '<div class="pl">+</div>'
              '<svg class="hr" viewBox="0 0 24 24"><path id="iHo" d="M20.4 5a5.2 5.2 0 0 0-7.4 0L12 6l-1-1a5.2 5.2 0 0 0-7.4 7.4l1 1L12 20.8l7.4-7.4 1-1a5.2 5.2 0 0 0 0-7.4z" '
              'fill="none" stroke="#fff" stroke-width="2"/>'
              '<path id="iHf" class="hrf" style="opacity:0" d="M20.4 5a5.2 5.2 0 0 0-7.4 0L12 6l-1-1a5.2 5.2 0 0 0-7.4 7.4l1 1L12 20.8l7.4-7.4 1-1a5.2 5.2 0 0 0 0-7.4z"/></svg>'
              '</div>' % stroke("person"))
    sysm = ('<div class="abs hide" id="iSy" style="left:0;top:0;width:1080px;height:700px">'
            '<svg class="ringc cab abs" width="1080" height="700" viewBox="0 0 1080 700" style="left:0;top:0">'
            '<path class="tube" d="M540 112 A148 148 0 1 1 539.9 112"/><path class="core" d="M540 112 A148 148 0 1 1 539.9 112"/></svg>'
            '</div>')
    L.append('<div class="g full" id="gI">' + sysm
             + tile("iCl", 170, 455, 175, "jelly", g.mark("claude"), extra_cls="circ")
             + tile("iMe", 96, 610, 300, "pearl", stroke("person"), extra_cls="circ", ring=False)
             + bar + posted + '</div>')
    sfx("pop", T["pyshy"], -3)
    sfx("key-press", T["plius"] + 0.02)
    sfx("click", T["koment"] - 0.06)
    return js("""
  tl.set("#gI", {autoAlpha: 1}, @kliientkame-0.2);
  arr("#iCl", @kliientkame-0.12, {s: 0.45, y: 0, d: 0.7});
  arr("#iSy", @yakshcho-0.05, {s: 0.7, y: 0, d: 0.8});
  gsap.set("#iSy", {transformOrigin: "540px 260px"});
  arr("#iMe", @sebe-0.06, {s: 0.3, y: 0, d: 0.55});
  arr("#iCb", @pyshy-0.08, {s: 0.85, y: 40, d: 0.7});
  tl.set("#iPh", {autoAlpha: 0}, @plius);
  tl.fromTo("#iPl", {autoAlpha: 0, scale: 0.3}, {autoAlpha: 1, scale: 1, duration: 0.3, ease: POP}, @plius+0.02);
  tl.to("#iGo", {scale: 0.9, duration: 0.08}, @koment-0.08); tl.to("#iGo", {scale: 1, duration: 0.3, ease: SP}, @koment);
  bout(["#iSy", "#iCl", "#iMe"], @koment-0.12, 10, 0.24);
  tl.set("#iPl", {autoAlpha: 0}, @koment);
  tl.set("#iPh", {autoAlpha: 1}, @koment+0.02);
  arr("#iCm", @koment+0.02, {s: 0.8, y: 120, d: 0.55});
  tl.to("#iHf", {opacity: 1, duration: 0.15}, @koment+0.4);
  tl.fromTo("#iCm .hr", {scale: 0.7, transformOrigin: "50% 50%"}, {scale: 1, duration: 0.35, ease: POP}, @koment+0.4);""")


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
  function drift1(sel, t, d) { tl.fromTo(sel + " .aurs", {x: 0, y: 0}, {x: -110, y: 70, duration: d, ease: "sine.inOut"}, t); }
  gsap.set(".sheen", {xPercent: -120});
"""


def span(a, b):
    return (round(a - 0.02, 3), round(b, 3), "")


# captions drop only where a graphic's own text says her word (STYLE.md §2b.1)
BLACKOUT = [
    span(T["instr"], T["instre"]),            # card «Інструкції»
    span(T["pam1"], T["pam1e"]),              # card «Пам'ять»
    span(T["metri"], T["metrie"]),            # the metricool wordmark
    span(T["opubl"], T["kliientue"]),         # the three action rows
    span(T["miaz"], T["pam2e"]),              # М'ЯЗОВА ПАМ'ЯТЬ
    span(T["skily"], T["skilye"]),            # СКІЛ cards
    span(T["pam3"], T["pam3e"]),              # the memory card
    span(T["systema"], T["systemae"]),        # СИСТЕМА
    span(T["plius"], T["pliuse"]),            # the «+» typed in the comment
]
# the head takeover is a white bust: captions in ink over its shoulders
INVERT = [(round(T["holova"] - 0.25, 3), round(T["vidbuve"] + 0.05, 3), "")]


def main():
    assert not NO_PAINT, "this cut has no closeups; re-check beats if it gets one"
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
        title=u"Reel 30 — анатомія ШІ",
        plate="assets/base.mp4",
        gfx_html=g.defs() + "\n" + "\n".join(L),
        gfx_js="\n".join(head + gj),
        caps=CAPS,
        blackout=BLACKOUT,
        invert=INVERT,
    )
    io.open(os.path.join(HERE, "index.html"), "w", encoding="utf-8").write(doc)
    SFX.sort(key=lambda c: c["t"])
    io.open(os.path.join(HERE, "sfx.json"), "w", encoding="utf-8").write(json.dumps(SFX, indent=1))
    print("index.html  %d captions, %d beats, %d sfx cues (%.2f/s)" % (len(CAPS), len(BEATS), len(SFX), len(SFX) / DUR))


main()
