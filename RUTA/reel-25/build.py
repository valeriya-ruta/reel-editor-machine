# -*- coding: utf-8 -*-
"""Reel 25 — «Вебінар зупинився в прямому ефірі». Posts 2026-10-09.

Explainer, full refined-glass chain (STYLE.md §0). Same pipeline as reel 23
(OBS -> YouTube -> Webinar Stars) and the same tile look for those three, so the
two reels match: OBS = jelly + simple-icons obsstudio, YouTube = pearl +
youtube, Webinar Stars = jelly wordmark.

The one object is **her webinar going down and coming back**: a LIVE screen
that loses the signal, the 4-step checklist that fixes it, and the pipeline it
runs on.

Chain:  near: a LIVE screen lands and glitches to «немає сигналу» -> it steps
aside for a 0:30 stopwatch; take off or not (an arrow flips) -> the screen deals
out into a fan of her 30+ webinars, the presenters become bloggers -> they
collapse into 13 000 € (kaching) -> the checklist she knows by heart (0-3, still
blank) drops when «все падає» -> *her closeup on «технічні шоколадки», clear* ->
the checklist returns: 0 · не панікувати, ticked -> a knot is pulled straight
(«набагато простіше») -> OVER: the iris opens out of the check: 1 · написати в
чат grows into the chat: viewers panic, her message types, sends, WC / tea /
coffee / 5:00 land under it, the chat calms -> iris closes onto row 2 · де
проблема -> near: OBS, YouTube, Webinar Stars on a shelf; Webinar Stars wraps
the YouTube video; a lens checks YouTube and the OBS cable; the cable snaps,
OBS is pressed, it reconnects -> OVER: the iris opens out of YouTube: the stream
stalls, «Завершити», a new key is generated in OBS and carried down to YouTube,
LIVE again, the new link goes up into Webinar Stars -> iris closes onto it ->
near: LIVE screen, viewers watching, nothing noticed -> one recording splits in
two -> the checklist, all four ticked, 5:00 -> the screen breaks again
(«страшно») and comes back LIVE on «не катастрофа» -> Стежити.

usage: python build.py   (then: python ../tools/sfx.py mix 25)
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

CUT = json.load(io.open(os.path.join(ROOT, "work", "r25", "cut.json"), encoding="utf-8"))
DUR = 87.716           # 2632 plate frames (cloud re-cut: centred zooms, first-take «підпишись» dropped)
FPS = 30
k = Kit(width=1080, height=1920, fps=FPS, duration=DUR)
g = Glass(["obsstudio", "youtube", "instagram"])
k.css(g.css())

# NO-PAINT: the closeup cut.py punched in on «технічні шоколадки» — her joke, captions only.
NO_PAINT = [tuple(x) for x in CUT["no_paint"]]
assert len(NO_PAINT) == 1, NO_PAINT
NP0, NP1 = NO_PAINT[0]

CAPS = k.load_captions(os.path.join(ROOT, "work", "r25", "captions.json"))
# whisper errors the aligner kept as "her wording" -> the word she said; brand
# names spelled as in reel 23 (same chain, posted three days apart): OBS,
# YouTube, Webinar Stars — which is also what whisper heard her say.
FIX = {u"завчається": u"зазвичай", u"ВБС,": u"OBS,", u"користно,": u"корисно,",
       u"ОБС,": u"OBS,", u"ОБС.": u"OBS.", u"ОБС": u"OBS",
       u"в Ютубі": u"в YouTube", u"до Ютубу,": u"до YouTube,",
       u"вебінар-старсу.": u"Webinar Stars.", u"Вебінар-старс": u"Webinar Stars",
       u"вебінар-старс.": u"Webinar Stars."}
for c in CAPS:
    c["w"] = FIX.get(c["w"], c["w"])
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
    "vebinar": S(u"Вебінар", 0.0), "zupyn": S(u"зупинився", 0.83), "priamomu": S(u"прямому", 1.63),
    "efiri": S(u"ефірі", 1.97),
    "robysh": S(u"робиш", 3.00), "n30": S("30", 3.86), "sekund": S(u"секунд", 4.12), "sekunde": E(u"секунд", 4.12),
    "vyrishuie": S(u"вирішує", 4.50), "zletyt": S(u"злетить", 5.04), "ni": S(u"ні", 6.12),
    "ya": S(u"Я", 6.55), "provela": S(u"провела", 6.77), "bilshe": S(u"більше", 7.07),
    "n30b": S("30", 7.79), "n30be": E("30", 7.79), "vebinariv": S(u"вебінарів", 8.19),
    "bloh": S(u"блогерки", 8.91), "zarobl": S(u"заробляють", 9.24), "vebinariv2": S(u"вебінарів", 9.91),
    "n13": S("13", 10.59), "ievro": S(u"євро", 11.59), "ievroe": E(u"євро", 11.59),
    "tomu": S(u"тому", 12.19), "znaiu": S(u"знаю", 12.99), "robyty": S(u"робити", 13.53),
    "vse": S(u"все", 14.05), "padaie": S(u"падає", 14.31),
    "nulovyi": S(u"Нульовий", 17.70), "krok": S(u"крок", 18.29), "ne0": S(u"не", 19.07),
    "panik": S(u"панікувати", 19.33), "panike": E(u"панікувати", 19.33),
    "tomu2": S(u"тому", 20.03), "vyrish": S(u"вирішується", 20.65), "zazvychai": S(u"зазвичай", 21.47),
    "prostishe": S(u"простіше", 22.37), "zdaie": E(u"здається", 23.21),
    "realnyi": S(u"Реальний", 24.06), "pershyi": S(u"перший", 24.42), "napysaty": S(u"написати", 25.08),
    "chate": E(u"чат", 25.70), "ne1": S(u"не", 26.00), "poverne": E(u"повернеться", 27.32),
    "mozhete": S(u"можете", 27.93), "tualet": S(u"туалет", 28.67), "chai": S(u"чай", 29.83),
    "kavu": S(u"каву", 30.11), "n5": S("5", 31.35), "khvylyne": E(u"хвилин", 31.53),
    "zaspok": S(u"заспокоює", 32.29), "perest": S(u"перестають", 33.89), "tobe": E(u"тобою", 35.35),
    "dali": S(u"Далі", 35.90), "dyvymos": S(u"дивимось", 36.31), "de": S(u"де", 36.85),
    "problema": S(u"проблема", 37.29), "probe": E(u"проблема", 37.29),
    "zviazka": S(u"Зв'язка", 37.91), "obs1": S("OBS", 39.73), "yt1": S("YouTube", 40.43),
    "ws1": S("Webinar", 40.91), "ws2": S("Webinar", 41.95), "ws2e": E("Webinar", 41.95),
    "lamaietsia": S(u"ламається", 43.58), "obhortka": S(u"обгортка", 44.84),
    "tomu3": S(u"тому", 46.84), "pereviriaty": S(u"перевіряти", 47.86), "yt2": S("YouTube", 48.46),
    "zviazok": S(u"зв'язок", 49.24), "obs2": S("OBS", 49.84),
    "yakshcho": S(u"Якщо", 50.79), "pererv": S(u"перерваний", 51.96), "zakhodymo": S(u"заходимо", 52.77),
    "perepidk": S(u"перепідключаємо", 53.99), "bukvalno": S(u"буквально", 55.71),
    "ale": S(u"Але", 56.73), "tak": S(u"так", 58.66), "vymyk": S(u"вимикаємо", 59.72),
    "povnistiu": S(u"повністю", 61.18), "heneruiemo": S(u"генеруємо", 62.01), "kliuch": S(u"ключ", 62.92),
    "obs5e": E("OBS", 63.30), "pidkl": S(u"підключаємо", 63.81), "znovu": S(u"знову", 64.61),
    "zapusk": S(u"запускаємо", 65.92), "novu": S(u"нову", 66.62), "vstavl": S(u"вставляємо", 67.78),
    "nove": S(u"нове", 68.47), "nazad": S(u"назад", 69.19), "ws3": S("Webinar", 69.91),
    "ws3e": E("Webinar", 69.91),
    "na": S(u"На", 71.16), "hliadachi": S(u"глядачі", 73.14), "nichoho": S(u"нічого", 73.50),
    "yedyna": S(u"єдина", 74.72), "zamist": S(u"замість", 75.75), "lezhat": S(u"лежать", 77.67),
    "dva": S(u"два", 78.03), "zapysye": E(u"записи", 78.75),
    "use": S(u"Усе", 79.69), "khv5": S(u"хвилин", 80.43), "piat": S(u"п'ять", 80.99), "piate": E(u"п'ять", 80.99),
    "umomenti": S(u"моменті", 81.65), "strashno": S(u"страшно", 82.31), "absol": S(u"абсолютно", 83.66),
    "katastr": S(u"катастрофа", 84.36), "katastre": E(u"катастрофа", 84.36),
    "pidp1": S(u"Якщо", 85.2), "pidp2": S(u"підпишись", 87.06),   # the CTA's first take is cut now
    "np0": NP0, "np1": NP1, "dur": DUR,
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
# Sound design (tools/sfx.py). Quiet, on the event, never on her closeup.
SFX = []


def sfx(name, t, db=0):
    if isinstance(t, str):
        t = float(js(t))
    SFX.append({"t": round(max(0.0, t), 3), "name": name, "db": db})


# ---------------------------------------------------------------------------
# Glyphs (24x24, stroked)
STROKES = {
    "person": '<circle cx="12" cy="8.2" r="3.6"/><path d="M4.8 20c.9-3.8 3.7-5.8 7.2-5.8s6.3 2 7.2 5.8"/>',
    "check": '<path d="M5.4 12.6l4.3 4.3 8.9-9.5"/>',
    "up": '<path d="M12 19.2V5.4M6.2 11l5.8-5.8 5.8 5.8"/>',
    "sigoff": ('<circle cx="12" cy="12" r="1.9"/><path d="M8.3 15.7a5.3 5.3 0 0 1 0-7.4M15.7 8.3a5.3 5.3 0 0 1 0 7.4'
               'M5.4 18.6a9.4 9.4 0 0 1 0-13.2M18.6 5.4a9.4 9.4 0 0 1 0 13.2"/><path d="M3.6 3.6l16.8 16.8"/>'),
    "chat": ('<path d="M4.6 5.2h14.8a1.6 1.6 0 0 1 1.6 1.6v8.6a1.6 1.6 0 0 1-1.6 1.6H10.2l-4.4 3.4V17H4.6'
             'A1.6 1.6 0 0 1 3 15.4V6.8a1.6 1.6 0 0 1 1.6-1.6z"/>'),
    "tea": ('<path d="M4.4 9.6h12.2v3.8a5.7 5.7 0 0 1-5.7 5.7h-.8a5.7 5.7 0 0 1-5.7-5.7z"/>'
            '<path d="M16.6 11h1.3a2.4 2.4 0 0 1 0 4.8h-1.6"/><path d="M3.4 21.4h15.2"/>'
            '<path d="M9.6 9.6V6.3"/><rect x="8.1" y="2.6" width="3" height="3.7" rx=".7"/>'),
    "coffee": ('<path d="M4.6 9.8h11.2v5.6a4.6 4.6 0 0 1-4.6 4.6H9.2a4.6 4.6 0 0 1-4.6-4.6z"/>'
               '<path d="M15.8 11.2h1.5a2.4 2.4 0 0 1 0 4.8h-1.5"/>'
               '<path d="M7.9 3.4c-1 1.1 1 2.1 0 3.4M11.3 3.4c-1 1.1 1 2.1 0 3.4"/>'),
    "shield": '<path d="M12 3l7.4 3v5.5c0 4.6-3.1 8-7.4 9.5-4.3-1.5-7.4-4.9-7.4-9.5V6z"/><path d="M8.7 12.1l2.3 2.3 4.4-4.7"/>',
    "refresh": '<path d="M19.4 12a7.4 7.4 0 1 1-2.2-5.3"/><path d="M19.7 4.3v4.5h-4.5"/>',
    "key": '<circle cx="8" cy="15.6" r="4.1"/><path d="M10.9 12.7l8.4-8.4M16.1 7.5l2.6 2.6M13.8 9.8l2 2"/>',
    "link": ('<path d="M10.2 13.8a4.3 4.3 0 0 0 6.1 0l2.9-2.9a4.3 4.3 0 0 0-6.1-6.1l-1.3 1.3"/>'
             '<path d="M13.8 10.2a4.3 4.3 0 0 0-6.1 0l-2.9 2.9a4.3 4.3 0 0 0 6.1 6.1l1.3-1.3"/>'),
    "heart": '<path d="M12 19.6s-7.3-4.4-7.3-9.7A4.1 4.1 0 0 1 12 7.6a4.1 4.1 0 0 1 7.3 2.3c0 5.3-7.3 9.7-7.3 9.7z"/>',
}
PLAY = '<svg class="ply" viewBox="0 0 24 24"><path d="M8.5 5.8v12.4l9.8-6.2z"/></svg>'


def stroke(name, cls="sk"):
    return '<svg class="%s" viewBox="0 0 24 24">%s</svg>' % (cls, STROKES[name])


def tile(tid, size, x, y, material, inner, extra_cls="", hide=True, ring=True, h=None):
    h = h or size
    rnd = " rnd" if "circ" in extra_cls else ""
    r = ('<div class="sqring%s" id="%sR" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx"></div>'
         % (rnd, tid, x, y, size, h)) if ring else ""
    return ('%s<div class="tw%s %s" id="%s" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx">'
            '<div class="%s">%s<div class="sheen"></div></div></div>'
            % (r, " hide" if hide else "", extra_cls, tid, x, y, size, h, material, inner))


def ws_mark(size=40):
    """Webinar Stars has no icon: the wordmark, two lines (as in reel 23)."""
    return '<span class="wmark wsm" style="font-size:%dpx">Webinar<br>Stars</span>' % size


k.css("""
.abs { position: absolute; }
.hide { opacity: 0; visibility: hidden; }
.tw { position: absolute; }
.sk { fill: none; stroke: url(#gw); stroke-width: 2.3; stroke-linecap: round; stroke-linejoin: round;
  width: 50%; height: 50%; position: relative; z-index: 1; overflow: visible; }
.pearl .sk { stroke: #17141c; }
.clear { overflow: hidden; }
.circ .jelly, .circ .pearl, .circ .clear, .circ .sheen { border-radius: 50%; }
.sqring.rnd { border-radius: 50%; }
.wsm { color: #fff; text-align: center; letter-spacing: -0.035em; line-height: 0.98; }
.aurs { position: absolute; left: -700px; top: -700px; width: 2480px; height: 3320px; pointer-events: none;
  background:
    radial-gradient(circle 526px at 1560px 880px, rgba(255,110,156,0.50), rgba(255,110,156,0)),
    radial-gradient(circle 634px at 760px 2360px, rgba(222,32,74,0.55), rgba(222,32,74,0)),
    radial-gradient(circle 382px at 1480px 1910px, rgba(255,198,214,0.20), rgba(255,198,214,0)); }
.shc { position: absolute; inset: 0; border-radius: inherit; overflow: hidden; pointer-events: none; }
.shc .sheen { mix-blend-mode: normal; opacity: 0.4; }
i { font-style: normal; }
.hb { position: absolute; display: block; border-radius: 12px; background: linear-gradient(115deg, #c41434 0%, #8d0d24 100%); }
.rr { position: absolute; display: block; border-radius: 9px; background: rgba(23,20,28,0.13); }
.live { position: absolute; display: flex; align-items: center; justify-content: center; gap: 12px;
  background: linear-gradient(165deg, #e0204b 0%, #8d0d24 100%); color: #fff; font-weight: 900;
  letter-spacing: 0.06em; box-shadow: inset 0 2px 1px rgba(255,255,255,0.5), 0 20px 40px -16px rgba(70,4,20,0.7); }
.live b { width: 16px; height: 16px; border-radius: 50%; background: #fff; display: block; }
.live.off { background: linear-gradient(165deg, #6f6770 0%, #443d47 100%); color: rgba(255,255,255,0.78);
  box-shadow: inset 0 2px 1px rgba(255,255,255,0.28), 0 20px 40px -16px rgba(10,4,8,0.6); }
.live.off b { background: transparent; box-shadow: inset 0 0 0 3px rgba(255,255,255,0.8); }
.pill { position: absolute; display: flex; align-items: center; justify-content: center; border-radius: 999px;
  font-weight: 900; letter-spacing: -0.01em; }
.pill.j { background: linear-gradient(165deg, #e0204b 0%, #ab112e 46%, #6b081c 100%); color: #fff;
  box-shadow: inset 0 2px 1px rgba(255,255,255,0.55), inset 0 -14px 24px -12px rgba(255,125,165,0.6), 0 26px 50px -20px rgba(8,0,3,0.7); }
.pill.p { background: linear-gradient(160deg, #ffffff 0%, #fff5f8 52%, #f5dfe6 100%); color: #17141c;
  box-shadow: inset 0 2px 1px #fff, 0 26px 50px -20px rgba(8,0,3,0.7); }

/* the webinar screen: LIVE, a presenter, the scrubber — and the signal it loses */
.scr { overflow: hidden; }
.scr .trk { position: absolute; left: 34px; height: 12px; border-radius: 6px; background: rgba(255,255,255,0.22); overflow: hidden; }
.scr .fil { position: absolute; left: 0; top: 0; width: 100%; height: 12px; border-radius: 6px;
  background: linear-gradient(90deg, #ff6e9c, #ffd6e3); transform-origin: 0 50%; }
.nsig { position: absolute; inset: 0; border-radius: inherit; overflow: hidden; transform-origin: 50% 0%;
  background: linear-gradient(165deg, #22141a 0%, #0d070a 100%); }
.nsig .nz { position: absolute; inset: 0; background: url("assets/grain.png"); background-size: 300px 300px;
  opacity: 0.38; mix-blend-mode: screen; }
.nsig .scan { position: absolute; inset: 0;
  background: repeating-linear-gradient(0deg, rgba(255,255,255,0.06) 0 2px, rgba(255,255,255,0) 2px 7px); }
.nsig .nso { position: absolute; top: 96px; width: 120px; height: 120px; fill: none; stroke: rgba(255,255,255,0.88);
  stroke-width: 1.9; stroke-linecap: round; stroke-linejoin: round; }
.nsig .nst { position: absolute; left: 0; right: 0; top: 246px; text-align: center; font-size: 30px; font-weight: 700;
  letter-spacing: 0.18em; color: rgba(255,255,255,0.78); }
.gsl { position: absolute; left: 0; top: 0; width: 100%; height: 38px; background: rgba(255,110,156,0.62);
  mix-blend-mode: screen; opacity: 0; visibility: hidden; z-index: 4; }
.gsl.b { height: 16px; background: rgba(255,255,255,0.55); }
.ring1 { fill: none; stroke: #ffd6e3; stroke-width: 10; stroke-linecap: round; filter: drop-shadow(0 0 10px rgba(255,110,156,0.9)); }
.hand { fill: #fff; }
.dig { position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; z-index: 2;
  color: #fff; font-size: 70px; font-weight: 900; letter-spacing: -0.03em; }

/* her webinars, fanned */
.fc { position: absolute; width: 300px; height: 180px; border-radius: 36px; overflow: hidden;
  background: linear-gradient(160deg, rgba(70,26,38,0.94) 0%, rgba(26,11,16,0.96) 100%);
  box-shadow: inset 0 1.5px 1px rgba(255,255,255,0.32), inset 0 0 0 1px rgba(255,255,255,0.08), 0 30px 60px -24px rgba(10,0,4,0.75); }
.fc .live { left: 18px; top: 16px; height: 34px; padding: 0 13px; border-radius: 17px; font-size: 16px; gap: 7px; }
.fc .live b { width: 10px; height: 10px; }
.fc .face { position: absolute; left: 108px; top: 54px; width: 84px; height: 84px; }
.mny .num { position: absolute; left: 52px; top: 118px; white-space: nowrap; }
.mny .eur { display: inline-block; margin-left: 26px; }
.mny .t-big { font-size: 168px; }

/* the checklist: what to do when the stream falls */
.lst { position: absolute; border-radius: 52px; overflow: hidden;
  background: linear-gradient(172deg, #ffffff 0%, #fff9fb 55%, #fdf0f4 100%);
  box-shadow: inset 0 2px 1px #fff, 0 50px 100px -36px rgba(24,4,12,0.62); }
.cbx { position: absolute; width: 50px; height: 50px; border-radius: 15px; box-shadow: inset 0 0 0 4px rgba(23,20,28,0.22); }
.cbf { position: absolute; inset: 0; border-radius: 15px;
  background: linear-gradient(165deg, #e0204b 0%, #8d0d24 100%); opacity: 0; visibility: hidden; }
.cbf.on { opacity: 1; visibility: inherit; }
.cbf svg { position: absolute; left: 7px; top: 7px; width: 36px; height: 36px; fill: none; stroke: #fff;
  stroke-width: 3.2; stroke-linecap: round; stroke-linejoin: round; }
.rn { position: absolute; left: 36px; width: 46px; height: 50px; line-height: 50px; text-align: center;
  font-size: 38px; font-weight: 900; color: #b4122f; letter-spacing: -0.03em; }
.rl { position: absolute; left: 172px; height: 50px; line-height: 50px; font-size: 40px; font-weight: 700;
  color: #17141c; letter-spacing: -0.015em; white-space: nowrap; }
.rhl { position: absolute; left: 22px; width: 776px; height: 66px; border-radius: 24px; background: #fbe3ea;
  transform-origin: 0 50%; }

/* the knot that gets pulled straight */
.knot { fill: none; stroke: #ffffff; stroke-width: 13; stroke-linecap: round; stroke-linejoin: round;
  filter: drop-shadow(0 0 10px rgba(255,110,156,0.95)) drop-shadow(0 0 26px rgba(255,110,156,0.55)); }

/* the chat */
.cht .hdt { position: absolute; left: 132px; top: 30px; height: 76px; line-height: 76px; font-size: 44px; font-weight: 700;
  letter-spacing: -0.02em; }
.cht .hair2 { position: absolute; left: 36px; right: 36px; top: 128px; height: 2px; background: rgba(23,20,28,0.08); }
.cht .live { left: 690px; top: 42px; height: 54px; padding: 0 20px; border-radius: 27px; font-size: 22px; gap: 9px; }
.cht .live b { width: 13px; height: 13px; }
.mrow { position: absolute; left: 36px; width: 600px; height: 92px; }
.mrow .av { position: absolute; left: 0; top: 8px; width: 72px; height: 72px; border-radius: 50%;
  background: linear-gradient(160deg, #f6e3e9 0%, #ecc8d0 100%); display: flex; align-items: center; justify-content: center; }
.mrow .av .sk { width: 40px; height: 40px; stroke: rgba(23,20,28,0.55); }
.mrow .nm { position: absolute; left: 96px; top: 10px; height: 16px; border-radius: 8px; background: rgba(23,20,28,0.16); }
.mrow .tx { position: absolute; left: 96px; top: 34px; font-size: 38px; font-weight: 500; color: #17141c;
  letter-spacing: -0.01em; white-space: nowrap; }
.mrow .tx.pn { color: #b4122f; font-weight: 700; }
.hbub { position: absolute; border-radius: 52px 52px 14px 52px; color: #fff; font-size: 38px; font-weight: 700;
  line-height: 1.2; letter-spacing: -0.012em; padding: 30px 40px;
  background: linear-gradient(165deg, #e0204b 0%, #ab112e 46%, #6b081c 100%);
  box-shadow: inset 0 2px 1px rgba(255,255,255,0.5), 0 30px 60px -20px rgba(70,4,20,0.6); }
.chip2 { position: absolute; height: 104px; border-radius: 34px; display: flex; align-items: center; justify-content: center;
  background: linear-gradient(160deg, #ffffff 0%, #fff5f8 52%, #f5dfe6 100%); color: #17141c;
  box-shadow: inset 0 2px 1px #fff, inset 0 0 0 1.5px rgba(23,20,28,0.07), 0 20px 40px -18px rgba(24,4,12,0.45); }
.chip2 .sk { width: 76px; height: 76px; stroke: #b4122f; stroke-width: 2.1; }
.chip2 .wc { font-size: 46px; font-weight: 900; letter-spacing: -0.02em; color: #b4122f; }
.chip2.j { background: linear-gradient(165deg, #e0204b 0%, #ab112e 46%, #6b081c 100%); color: #fff;
  font-size: 48px; font-weight: 900; letter-spacing: -0.02em;
  box-shadow: inset 0 2px 1px rgba(255,255,255,0.5), 0 20px 40px -18px rgba(70,4,20,0.6); }
.inp { position: absolute; left: 36px; top: 932px; width: 828px; height: 100px; border-radius: 50px; background: #f6e6eb;
  box-shadow: inset 0 0 0 1.5px rgba(23,20,28,0.05); }
.inp .phd, .inp #msgT { position: absolute; left: 40px; top: 0; height: 100px; line-height: 100px; font-size: 34px;
  white-space: nowrap; }
.inp .phd { font-weight: 500; color: rgba(23,20,28,0.38); }
.inp #msgT { font-weight: 500; color: #17141c; }
.inp #msgT::after { content: ""; display: inline-block; width: 3px; height: 38px; margin-left: 3px; vertical-align: -7px;
  background: #e0204b; }
.hrt { position: absolute; width: 74px; height: 74px; }
.hrt .sk { width: 56%; height: 56%; fill: #fff; stroke: #fff; }

/* the lens, the cables, the spark */
.lens { position: absolute; left: 0; top: 0; width: 210px; height: 210px; z-index: 6; }
.lens .gl2 { position: absolute; inset: 0; border-radius: 50%;
  background: linear-gradient(150deg, rgba(255,255,255,0.30) 0%, rgba(255,255,255,0.06) 60%, rgba(255,255,255,0.14) 100%);
  -webkit-backdrop-filter: blur(1px) saturate(1.6) brightness(1.12); backdrop-filter: blur(1px) saturate(1.6) brightness(1.12);
  box-shadow: inset 0 0 0 13px rgba(255,255,255,0.94), inset 0 0 0 16px rgba(180,18,47,0.30),
              inset 0 -20px 30px -10px rgba(255,255,255,0.35), 0 34px 60px -20px rgba(24,4,12,0.6); }
.lens .hdl { position: absolute; left: 178px; top: 160px; width: 44px; height: 124px; border-radius: 22px;
  transform: rotate(-45deg); transform-origin: 22px 0;
  background: linear-gradient(165deg, #e0204b 0%, #ab112e 46%, #6b081c 100%);
  box-shadow: inset 0 2px 1px rgba(255,255,255,0.5), 0 20px 30px -12px rgba(70,4,20,0.6); }
.cab .tube { fill: none; stroke: rgba(255,255,255,0.30); stroke-width: 20; stroke-linecap: round; }
.cab .core { fill: none; stroke: rgba(255,255,255,0.94); stroke-width: 4.5; stroke-linecap: round; }
.spk { fill: none; stroke: #ffd6e3; stroke-width: 6; stroke-linecap: round; filter: drop-shadow(0 0 8px rgba(255,110,156,1)); }
.wrp { position: absolute; border-radius: 70px; overflow: hidden;
  background: linear-gradient(165deg, #e0204b 0%, #ab112e 46%, #6b081c 100%);
  box-shadow: inset 0 2px 1px rgba(255,255,255,0.55), inset 0 -26px 40px -14px rgba(255,125,165,0.6),
              0 36px 64px -22px rgba(70,4,20,0.62); }
.wrp .wl { position: absolute; left: 0; right: 0; top: 12px; text-align: center; font-size: 30px; font-weight: 900;
  color: #fff; letter-spacing: -0.03em; }

/* the YouTube stream, the OBS key */
.ytc .pv { position: absolute; left: 40px; top: 140px; width: 780px; height: 440px; border-radius: 32px; overflow: hidden;
  background: radial-gradient(ellipse at 50% 40%, #2a1e26 0%, #0c090e 78%); box-shadow: inset 0 0 0 1.5px rgba(23,20,28,0.1); }
.ytc .live { left: 640px; top: 44px; height: 58px; padding: 0 22px; border-radius: 29px; font-size: 24px; gap: 10px; }
.spn { position: absolute; fill: none; stroke: #ff8ab0; stroke-width: 9; stroke-linecap: round; stroke-dasharray: 210 200;
  filter: drop-shadow(0 0 10px rgba(255,110,156,0.8)); }
.stp { position: absolute; width: 104px; height: 104px; border-radius: 26px; background: #fff;
  box-shadow: 0 0 40px rgba(255,255,255,0.35); }
.sbt { position: absolute; left: 40px; top: 616px; width: 380px; height: 104px; border-radius: 52px; color: #fff;
  font-size: 38px; font-weight: 700; display: flex; align-items: center; justify-content: center; letter-spacing: -0.01em;
  background: linear-gradient(165deg, #e0204b 0%, #ab112e 46%, #6b081c 100%);
  box-shadow: inset 0 2px 1px rgba(255,255,255,0.5), 0 24px 44px -16px rgba(70,4,20,0.65); }
.ckr { position: absolute; width: 140px; height: 140px; margin: -70px 0 0 -70px; border-radius: 50%;
  border: 8px solid #ff6e9c; opacity: 0; visibility: hidden; z-index: 5; }
.fing { position: absolute; width: 84px; height: 84px; margin: -42px 0 0 -42px; border-radius: 50%;
  background: rgba(255,255,255,0.55); box-shadow: 0 0 0 3px rgba(255,255,255,0.9), 0 10px 24px rgba(24,4,12,0.35); z-index: 6; }
.obs { position: absolute; border-radius: 48px; overflow: hidden;
  background: linear-gradient(170deg, #2b2330 0%, #1b161f 60%, #151118 100%);
  box-shadow: inset 0 1.5px 0 rgba(255,255,255,0.18), inset 0 0 0 1px rgba(255,255,255,0.07),
              0 70px 130px -40px rgba(8,0,3,0.85); }
.obs .tt { position: absolute; left: 124px; top: 22px; height: 76px; line-height: 76px; font-size: 36px; font-weight: 700;
  color: rgba(255,255,255,0.9); letter-spacing: -0.01em; }
.obs .wd { position: absolute; top: 52px; width: 18px; height: 18px; border-radius: 50%; background: rgba(255,255,255,0.18); }
.obs .lb2 { position: absolute; left: 44px; top: 146px; font-size: 24px; font-weight: 700; letter-spacing: 0.16em;
  color: rgba(255,255,255,0.5); }
.obs .fld { position: absolute; left: 40px; top: 194px; width: 680px; height: 124px; border-radius: 30px;
  background: rgba(255,255,255,0.07); box-shadow: inset 0 0 0 1.5px rgba(255,255,255,0.1); overflow: hidden; }
.obs #keyT { position: absolute; left: 36px; top: 0; height: 124px; line-height: 124px; font-size: 42px; font-weight: 700;
  color: #fff; letter-spacing: 0.07em; white-space: nowrap; }
.kp { position: absolute; height: 88px; border-radius: 44px; display: flex; align-items: center; gap: 14px; padding: 0 30px 0 16px;
  background: linear-gradient(165deg, #e0204b 0%, #ab112e 46%, #6b081c 100%); color: #fff; font-size: 30px; font-weight: 700;
  letter-spacing: 0.06em; white-space: nowrap; box-shadow: inset 0 2px 1px rgba(255,255,255,0.5), 0 26px 50px -20px rgba(8,0,3,0.7); }
.kp .kc { width: 58px; height: 58px; border-radius: 50%; background: rgba(255,255,255,0.18); display: flex;
  align-items: center; justify-content: center; }
.kp .kc .sk { width: 36px; height: 36px; stroke: #fff; }
.lnk { position: absolute; height: 80px; border-radius: 40px; display: flex; align-items: center; gap: 14px; padding: 0 28px 0 18px;
  background: linear-gradient(160deg, #ffffff 0%, #fff5f8 52%, #f5dfe6 100%); color: #17141c; font-size: 30px; font-weight: 700;
  letter-spacing: -0.01em; white-space: nowrap; box-shadow: inset 0 2px 1px #fff, 0 26px 50px -20px rgba(24,4,12,0.7); }
.lnk .lc { width: 50px; height: 50px; border-radius: 50%; display: flex; align-items: center; justify-content: center;
  background: linear-gradient(165deg, #e0204b 0%, #8d0d24 100%); }
.lnk .lc .sk { width: 30px; height: 30px; stroke: #fff; }
.lnk em { font-style: normal; color: rgba(23,20,28,0.45); }
.ghost { opacity: 0.4; }

/* the recordings */
.rcd { position: absolute; width: 400px; height: 330px; border-radius: 44px; overflow: hidden;
  background: linear-gradient(172deg, #ffffff 0%, #fff9fb 55%, #fdf0f4 100%);
  box-shadow: inset 0 2px 1px #fff, 0 44px 90px -34px rgba(24,4,12,0.62); }
.rcd .th { position: absolute; left: 20px; top: 20px; width: 360px; height: 200px; border-radius: 28px;
  background: linear-gradient(160deg, #4a2a38 0%, #1c1016 100%); }
.rcd .pc { position: absolute; left: 140px; top: 60px; width: 80px; height: 80px; border-radius: 50%;
  background: rgba(255,255,255,0.92); display: flex; align-items: center; justify-content: center; }
.ply { width: 46px; height: 46px; fill: #b4122f; margin-left: 4px; }
.nbd { position: absolute; width: 84px; height: 84px; border-radius: 50%; display: flex; align-items: center; justify-content: center;
  color: #fff; font-size: 46px; font-weight: 900;
  background: linear-gradient(165deg, #e0204b 0%, #ab112e 46%, #6b081c 100%);
  box-shadow: inset 0 2px 1px rgba(255,255,255,0.55), 0 20px 40px -14px rgba(70,4,20,0.7); }

/* follow */
.fl { position: absolute; border-radius: 80px; overflow: hidden;
  background: linear-gradient(160deg, #ffffff 0%, #fff5f8 52%, #f5dfe6 100%);
  box-shadow: inset 0 2px 1px #fff, 0 40px 80px -28px rgba(30,4,12,0.65); }
.fl .t { position: absolute; left: 160px; top: 0; height: 150px; line-height: 150px; font-size: 56px; font-weight: 700;
  letter-spacing: -0.02em; color: #17141c; }
.fl .on { position: absolute; inset: 0; background: linear-gradient(165deg, #e0204b 0%, #ab112e 46%, #6b081c 100%);
  opacity: 0; visibility: hidden; }
.fl .on .t { color: #fff; left: 150px; }
""")

L = []
BEATS = []


def beat(fn):
    BEATS.append(fn)
    return fn


def screen(pid, x, y, broken=False, fill=0.3, w=720, h=405):
    """The webinar screen. `broken` starts it on «немає сигналу»."""
    return (
        '<div class="dglass edge scr hide" id="%(p)s" style="left:%(x)dpx;top:%(y)dpx;width:%(w)dpx;height:%(h)dpx">'
        '<div class="tw circ" style="left:%(px)dpx;top:92px;width:170px;height:170px"><div class="pearl">%(person)s</div></div>'
        '<div class="trk" style="top:%(ty)dpx;width:%(tw)dpx"><div class="fil" id="%(p)sF" style="transform:scaleX(%(f).2f)"></div></div>'
        '<div class="nsig%(nh)s" id="%(p)sN"><div class="nz"></div><div class="scan"></div>'
        '<svg class="nso" viewBox="0 0 24 24" style="left:%(ox)dpx">%(off)s</svg><div class="nst">НЕМАЄ СИГНАЛУ</div></div>'
        '<div class="gsl" id="%(p)sS0"></div><div class="gsl b" id="%(p)sS1"></div><div class="gsl" id="%(p)sS2"></div>'
        '<div class="live%(lh)s" id="%(p)sL" style="left:30px;top:28px;height:56px;padding:0 22px;border-radius:28px;font-size:24px"><b></b>LIVE</div>'
        '<div class="live off%(oh)s" id="%(p)sO" style="left:30px;top:28px;height:56px;padding:0 22px;border-radius:28px;font-size:24px"><b></b>LIVE</div>'
        '<div class="shc"><div class="sheen"></div></div></div>'
        % {"p": pid, "x": x, "y": y, "w": w, "h": h, "px": (w - 170) // 2, "person": stroke("person"),
           "ty": h - 54, "tw": w - 68, "f": fill, "nh": "" if broken else " hide",
           "ox": (w - 120) // 2, "off": STROKES["sigoff"],
           "lh": " hide" if broken else "", "oh": "" if broken else " hide"})


def glitch(p, t):
    """A broken signal: three slices jump about for ~0.35 s and the screen shudders."""
    ys = [(40, 230, 150), (190, 80, 320), (300, 20, 120), (90, 270, 40), (250, 150, 360), (20, 330, 210), (150, 60, 280)]
    out = []
    for j, (a, b, c) in enumerate(ys):
        tt = t + j * 0.05
        out.append('tl.set("#%sS0", {autoAlpha: 1, y: %d}, %.3f); tl.set("#%sS1", {autoAlpha: %d, y: %d}, %.3f); '
                   'tl.set("#%sS2", {autoAlpha: %d, y: %d}, %.3f);'
                   % (p, a, tt, p, j % 2, b, tt, p, (j + 1) % 2, c, tt))
    out.append('tl.set(["#%sS0", "#%sS1", "#%sS2"], {autoAlpha: 0}, %.3f);' % (p, p, p, t + len(ys) * 0.05))
    out.append('tl.to("#%s", {keyframes: {x: [0, -16, 12, -8, 10, -4, 0], skewX: [0, 5, -4, 3, -2, 1, 0]}, '
               'duration: 0.36, ease: "none"}, %.3f);' % (p, t))
    return "\n  ".join(out)


STEPS = [u"Не панікувати", u"Написати в чат", u"Де проблема?", u"Новий ключ"]
GHOST_W = (380, 330, 300, 250)


def checklist(pid, left, top, done=()):
    """Steps 0-3. `done` rows start labelled and ticked."""
    rows = ""
    for i in range(4):
        y = 124 + 68 * i
        on = i in done
        rows += ('<div class="rhl hide" id="%(p)sH%(i)d" style="top:%(yh)dpx"></div>'
                 '<div class="rn" style="top:%(y)dpx">%(i)d</div>'
                 '<div class="cbx" style="left:96px;top:%(y)dpx"><div class="cbf%(on)s" id="%(p)sC%(i)d">'
                 '<svg viewBox="0 0 24 24"><path id="%(p)sP%(i)d" d="M5.4 12.6l4.3 4.3 8.9-9.5"/></svg></div></div>'
                 '<i class="rr%(gh)s" id="%(p)sG%(i)d" style="left:172px;top:%(yg)dpx;width:%(w)dpx;height:22px;border-radius:11px"></i>'
                 '<div class="rl%(lh)s" id="%(p)sL%(i)d" style="top:%(y)dpx">%(lab)s</div>'
                 % {"p": pid, "i": i, "y": y, "yh": y - 8, "yg": y + 14, "w": GHOST_W[i], "lab": STEPS[i],
                    "on": " on" if on else "", "gh": " hide" if on else "", "lh": "" if on else " hide"})
    return ('<div class="lst hide" id="%s" style="left:%dpx;top:%dpx;width:820px;height:420px">'
            '<div class="tw circ" style="left:40px;top:30px;width:66px;height:66px"><div class="jelly">%s</div></div>'
            '<i class="hb" style="left:126px;top:49px;width:300px;height:28px"></i>%s'
            '<div class="shc"><div class="sheen"></div></div></div>' % (pid, left, top, stroke("sigoff"), rows))


# ===========================================================================
# A · hook — the LIVE screen loses its signal; B · 0:30, take off or not
@beat
def a_hook():
    ring = ('<svg class="abs hide" id="tmrS" width="290" height="290" viewBox="0 0 290 290" style="left:670px;top:170px;overflow:visible">'
            '<circle class="ring1" id="rng" cx="145" cy="145" r="136" transform="rotate(-90 145 145)"/>'
            '<g id="hand"><circle class="hand" cx="145" cy="9" r="11"/></g></svg>')
    L.append('<div class="g full" id="gA">' + screen("scrA", 180, 130, fill=0.3)
             + ring + tile("tmr", 230, 700, 200, "jelly", '<div class="dig" id="dig">0:30</div>', extra_cls="circ")
             + tile("upB", 104, 604, 112, "jelly", stroke("up"), extra_cls="circ") + '</div>')
    sfx("glitch-1", T["zupyn"] + 0.02)
    sfx("whoosh-short", T["robysh"] - 0.25, -5)
    sfx("pop", T["n30"] - 0.02)
    sfx("ping", T["zletyt"] + 0.02, -4)
    return js("""
  tl.set("#gA", {autoAlpha: 1}, 0);
  arr("#scrA", 0.0, {s: 0.7, y: 40, d: 0.8});
  tl.fromTo("#scrAF", {scaleX: 0.3}, {scaleX: 0.42, duration: @zupyn, ease: "none"}, 0);
  {{glitch}}
  tl.set("#scrAN", {autoAlpha: 1}, @zupyn+0.12); tl.set("#scrAN", {autoAlpha: 0}, @zupyn+0.17);
  tl.set("#scrAN", {autoAlpha: 1}, @zupyn+0.22); tl.set("#scrAN", {autoAlpha: 0}, @zupyn+0.27);
  tl.set("#scrAN", {autoAlpha: 1}, @zupyn+0.32);
  /* «в прямому ефірі»: the LIVE pill flickers out */
  tl.set("#scrAL", {autoAlpha: 0}, @priamomu); tl.set("#scrAO", {autoAlpha: 1}, @priamomu);
  tl.set("#scrAL", {autoAlpha: 1}, @priamomu+0.07); tl.set("#scrAL", {autoAlpha: 0}, @priamomu+0.14);
  tl.set("#scrAL", {autoAlpha: 1}, @priamomu+0.24); tl.set("#scrAL", {autoAlpha: 0}, @priamomu+0.3);
  /* B: the screen steps aside for the 30 seconds */
  tl.to("#scrA", {x: -170, scale: 0.8, duration: 0.6, ease: SP}, @robysh-0.25);
  arr("#tmr", @n30-0.06, {s: 0.4, y: 20, d: 0.7});
  G.ripple("#tmrR", @n30+0.25);
  tl.set("#tmrS", {autoAlpha: 1}, @n30+0.02);
  draw2("rng", @n30+0.02, 0.4);
  tl.fromTo("#hand", {rotation: 0, svgOrigin: "145 145"}, {rotation: 900, svgOrigin: "145 145", duration: 2.5, ease: "none"}, @n30+0.1);
  /* «злетить ефір далі чи ні»: up, LIVE again ... then down, off */
  arr("#upB", @zletyt-0.04, {s: 0.3, y: 30, d: 0.65});
  tl.set("#scrAN", {autoAlpha: 0}, @zletyt); tl.set("#scrAO", {autoAlpha: 0}, @zletyt); tl.set("#scrAL", {autoAlpha: 1}, @zletyt);
  shn("#scrA .sheen", @zletyt);
  tl.to("#upB", {rotation: 180, duration: 0.6, ease: FLIP}, @ni-0.05);
  tl.set("#scrAN", {autoAlpha: 1}, @ni); tl.set("#scrAL", {autoAlpha: 0}, @ni); tl.set("#scrAO", {autoAlpha: 1}, @ni);
  bout(["#tmr", "#tmrS", "#upB"], @ya-0.12, 10, 0.25);
  bout("#scrA", @ya+0.02, 10, 0.25);
  tl.set("#gA", {autoAlpha: 0}, @ya+0.35);""").replace("{{glitch}}", glitch("scrA", T["zupyn"]))


# ===========================================================================
# C · 30+ webinars -> the bloggers -> 13 000 € -> the checklist, which falls
FAN = []
for _i in range(5):
    _cx = 540 + (_i - 2) * 165
    _cy = 352 + abs(_i - 2) * 26
    FAN.append((_cx, _cy, (_i - 2) * 5))


@beat
def c_proof():
    cards = ""
    for i in (0, 4, 1, 3, 2):
        cx, cy, _r = FAN[i]
        cards += ('<div class="fc hide" id="fc%d" style="left:%dpx;top:%dpx"><div class="live"><b></b>LIVE</div>'
                  '<div class="face tw circ" id="fp%d"><div class="pearl">%s</div></div>'
                  '<div class="face tw circ hide" id="fj%d"><div class="jelly">%s</div></div></div>'
                  % (i, cx - 150, cy - 90, i, stroke("person"), i, stroke("person")))
    badge = ('<div class="pill j hide" id="b30" style="left:405px;top:96px;width:270px;height:132px;font-size:92px">'
             '<span id="c30">0</span><span id="b30p" class="hide">+</span></div>'
             '<div class="sqring rnd" id="b30R" style="left:405px;top:96px;width:270px;height:132px;border-radius:66px"></div>')
    avs = "".join('<div class="tw circ" style="left:%dpx;top:40px;width:70px;height:70px"><div class="jelly">%s</div></div>'
                  % (52 + j * 50, stroke("person")) for j in range(3))
    mny = ('<div class="sheet mny hide" id="mny" style="left:110px;top:170px;width:860px;height:340px">%s'
           '<div class="num"><span class="t-big" id="cnt">0</span><span class="t-big eur" id="eur">€</span></div>'
           '<div class="sheen"></div></div>' % avs)
    L.append('<div class="g full" id="gC">' + cards + badge + mny + checklist("chkC", 130, 150) + '</div>')
    sfx("whoosh-short", T["ya"] + 0.05, -4)
    sfx("pop", T["n30b"] + 0.02)
    sfx("kaching", T["ievro"] + 0.02)
    deal = []
    for i in range(5):
        cx, cy, r = FAN[i]
        deal.append('  tl.fromTo("#fc%d", {autoAlpha: 0, x: %d, y: %d, rotation: 0, scale: 0.6}, '
                    '{autoAlpha: 1, x: 0, y: 0, rotation: %d, scale: 1, duration: 0.75, ease: SP}, %.3f);'
                    % (i, 370 - cx, 332 - cy, r, T["ya"] + 0.08 + abs(i - 2) * 0.07))
        deal.append('  tl.to("#fp%d", {rotationY: 90, duration: 0.16, ease: "power2.in"}, %.3f);'
                    % (i, T["bloh"] - 0.05 + i * 0.07))
        deal.append('  tl.set("#fp%d", {autoAlpha: 0}, %.3f); tl.set("#fj%d", {autoAlpha: 1}, %.3f);'
                    % (i, T["bloh"] + 0.11 + i * 0.07, i, T["bloh"] + 0.11 + i * 0.07))
        deal.append('  tl.fromTo("#fj%d", {rotationY: -90}, {rotationY: 0, duration: 0.6, ease: FLIP, immediateRender: false}, %.3f);'
                    % (i, T["bloh"] + 0.11 + i * 0.07))
        deal.append('  gsap.set("#fj%d", {rotationY: -90});' % i)
        deal.append('  tl.to("#fc%d", {x: %d, y: %d, rotation: 0, scale: 0.5, autoAlpha: 0, duration: 0.42, ease: "power3.in"}, %.3f);'
                    % (i, 540 - cx, 340 - cy, T["vebinariv2"] - 0.1))
    return js("""
  tl.set("#gC", {autoAlpha: 1}, @ya);
{{deal}}
  arr("#b30", @bilshe-0.04, {s: 0.4, y: 20, d: 0.7});
  tl.set("#b30p", {autoAlpha: 1}, @n30b+0.18); G.bump("#b30", @n30b+0.18); G.ripple("#b30R", @n30b+0.2);
  bout("#b30", @vebinariv2-0.1, 10, 0.3);
  arr("#mny", @vebinariv2+0.3, {s: 0.5, y: 0, d: 0.8});
  G.bump("#eur", @ievro-0.02); G.bump("#mny", @ievro+0.04); shn("#mny .sheen", @ievro+0.02);
  bout("#mny", @tomu-0.12, 10, 0.26);
  /* «тому я точно знаю, що робити»: the checklist she knows, still blank */
  arr("#chkC", @tomu+0.06, {s: 0.75, y: 40});
  shn("#chkC .sheen", @znaiu);
  /* «коли все падає»: it falls — and is gone before her closeup */
  tl.to("#chkC", {y: 190, rotation: 8, autoAlpha: 0, filter: "blur(8px)", duration: 0.42, ease: "power2.in"}, @vse+0.06);
  tl.set("#chkC", {filter: "none"}, @vse+0.49);
  tl.set("#gC", {autoAlpha: 0}, @np0-0.02);""").replace("{{deal}}", "\n".join(deal))


# ===========================================================================
# D · step 0: don't panic; the knot is pulled straight
def _coil():
    """A tangled cable: a coiled cord (a prolate cycloid), a little irregular."""
    import math
    pts = []
    t0 = -math.pi / 2
    for i in range(201):
        th = t0 + 9 * math.pi * i / 200
        r = 78 + 18 * math.sin(0.7 * th)
        pts.append((24 * (th - t0) - 58 * math.sin(th), 180 + r * math.cos(th) + 14 * math.sin(0.45 * th)))
    dx = 80 - min(p[0] for p in pts)
    return "M" + " L".join("%.1f %.1f" % (x + dx, y) for x, y in pts)


KNOT = _coil()
KN_TILE = (770, 120)              # the check at the end of the straight line, inside the shelf
KN0 = (70, 170)                   # the shelf, on screen
IRIS1 = (KN0[0] + KN_TILE[0] + 60, KN0[1] + KN_TILE[1] + 60)


@beat
def d_step0():
    shelf = ('<div class="shelf edge hide" id="kn" style="left:%dpx;top:%dpx;width:940px;height:360px">'
             '<svg class="abs" width="940" height="360" style="left:0;top:0;overflow:visible">'
             '<path class="knot" id="knP" d="%s"/><path class="knot" id="knS" style="opacity:0" d="M80 180 L 760 180"/></svg>'
             '%s</div>' % (KN0 + (KNOT, tile("knC", 120, KN_TILE[0], KN_TILE[1], "jelly", stroke("check"), extra_cls="circ"))))
    L.append('<div class="g full" id="gD">' + checklist("chkD", 130, 150) + shelf + '</div>')
    sfx("pop", T["nulovyi"] - 0.02, -4)
    sfx("click-soft", T["panik"] + 0.1)
    sfx("sparkle", T["prostishe"] + 0.03, -2)
    return js("""
  tl.set("#gD", {autoAlpha: 1}, @nulovyi-0.1);
  arr("#chkD", @nulovyi-0.06, {s: 0.75, y: 40});
  hl("chkD", 0, @krok);
  lab("chkD", 0, @ne0);
  tick("chkD", 0, @panik+0.08);
  bout("#chkD", @tomu2-0.05, 10, 0.28);
  /* «все вирішується»: a knot ... «набагато простіше»: pulled straight */
  arr("#kn", @tomu2+0.02, {s: 0.9, y: 30, d: 0.75});
  draw2("knP", @tomu2+0.12, 0.95);
  var KL = document.getElementById("knP").getTotalLength() + 3;
  tl.to("#knP", {strokeDashoffset: -KL, duration: 0.75, ease: "power2.inOut"}, @zazvychai+0.02);
  tl.set("#knS", {opacity: 1}, @zazvychai+0.12);
  draw2("knS", @zazvychai+0.12, 0.72);
  arr("#knC", @prostishe-0.04, {s: 0.3, y: 0, d: 0.6});
  G.ripple("#knCR", @prostishe+0.25);
  tl.set("#gD", {autoAlpha: 0}, @realnyi+0.8);""")


# ===========================================================================
# TK1 · step 1: write in the chat
PANIC = [u"Що сталося???", u"Нічого не чути", u"Зависло!!", u"Алло???"]
CALM = [u"Ок, чекаємо", u"Йду по чай", u"Дякуємо!", u"Без паніки"]
MSG = u"Не переживайте, зараз усе повернеться"
CH0 = (90, 150)                   # the chat sheet on screen (900 x 1060)
CHK_D2 = (130, 150)               # where the checklist sits when the iris closes on row 2
IRIS2 = (CHK_D2[0] + 121, CHK_D2[1] + 124 + 2 * 68 + 25)


@beat
def t1_chat():
    rows = ""
    for i in range(4):
        rows += ('<div class="mrow" style="top:%dpx"><div class="av">%s</div><i class="nm" style="width:%dpx"></i>'
                 '<div class="tx pn" id="mp%d">%s</div><div class="tx hide" id="mc%d">%s</div></div>'
                 % (150 + 108 * i, stroke("person"), (130, 100, 150, 116)[i], i, PANIC[i], i, CALM[i]))
    chips = ('<div class="chip2 hide" id="chWC" style="left:244px;top:796px;width:130px"><span class="wc">WC</span></div>'
             '<div class="chip2 hide" id="chTea" style="left:390px;top:796px;width:120px">%s</div>'
             '<div class="chip2 hide" id="chCof" style="left:526px;top:796px;width:120px">%s</div>'
             '<div class="chip2 j hide" id="ch5" style="left:662px;top:796px;width:202px">5:00</div>'
             % (stroke("tea"), stroke("coffee")))
    hearts = "".join('<div class="tw circ hrt hide" id="hr%d" style="left:%dpx;top:%dpx"><div class="jelly">%s</div></div>'
                     % (j, 740 + (j % 2) * 60, 170 + j * 110, stroke("heart")) for j in range(3))
    sheet = ('<div class="sheet cht hide" id="cht" style="left:%dpx;top:%dpx;width:900px;height:1060px">'
             '<div class="tw circ" style="left:36px;top:30px;width:78px;height:78px"><div class="jelly">%s</div></div>'
             '<div class="hdt">Чат</div><div class="live off"><b></b>LIVE</div><div class="hair2"></div>%s'
             '<div class="hbub hide" id="hbub" style="left:250px;top:600px;width:614px">%s</div>%s'
             '<div class="inp"><div class="phd" id="msgP">Повідомлення…</div><div id="msgT"></div>'
             '<div class="tw circ" id="sendB" style="left:740px;top:10px;width:80px;height:80px"><div class="jelly">%s</div></div></div>'
             '%s<div class="sheen"></div></div>'
             % (CH0 + (stroke("chat"), rows, MSG, chips, stroke("up"), hearts)))
    L.append('<div class="g full" id="gT1"><div class="tkg"></div><div class="aurs"></div><div class="grain"></div>'
             + checklist("chkT", 130, 430, done=(0,)) + sheet + '</div>')
    sfx("whoosh-short", T["zdaie"] - 0.12)
    sfx("click-soft", T["napysaty"] + 0.45)
    sfx("typing", T["ne1"] + 0.05, -2)
    sfx("click", T["mozhete"] + 0.02)
    sfx("pop", T["tualet"] + 0.03, -4)
    sfx("click-soft", T["n5"] + 0.02)
    sfx("notification", T["zaspok"] + 0.03, -4)
    sfx("whoosh-short", T["tobe"] - 0.32, -4)
    calm = "\n".join('  tl.to("#mp%d", {autoAlpha: 0, y: -14, duration: 0.22, ease: "power2.in"}, %.3f);\n'
                     '  tl.fromTo("#mc%d", {autoAlpha: 0, y: 18}, {autoAlpha: 1, y: 0, duration: 0.4, ease: SP}, %.3f);'
                     % (i, T["zaspok"] + i * 0.2, i, T["zaspok"] + 0.12 + i * 0.2) for i in range(4))
    return js("""
  G.irisOpen("#gT1", @zdaie-0.12, {{ix}}, {{iy}}, 0.85);
  drift1("#gT1", @zdaie, @tobe-@zdaie);
  arr("#chkT", @zdaie+0.02, {s: 0.7, y: 40});
  hl("chkT", 1, @pershyi);
  lab("chkT", 1, @napysaty);
  tick("chkT", 1, @napysaty+0.42);
  tl.to("#chkT", {y: -160, scale: 0.85, autoAlpha: 0, duration: 0.34, ease: "power2.in"}, @chate-0.02);
  gsap.set("#cht", {transformOrigin: "450px 220px"});
  arr("#cht", @chate, {s: 0.7, y: 60, d: 0.8});
  tl.set("#msgP", {autoAlpha: 0}, @ne1+0.05);
  G.bump("#sendB", @mozhete-0.04);
  tl.set("#msgP", {autoAlpha: 1}, @mozhete+0.05);
  tl.fromTo("#hbub", {autoAlpha: 0, y: 330, scale: 0.6, transformOrigin: "100% 100%"},
            {autoAlpha: 1, y: 0, scale: 1, duration: 0.6, ease: SP}, @mozhete+0.02);
  arr("#chWC", @tualet-0.04, {s: 0.4, y: 20, d: 0.6});
  arr("#chTea", @chai-0.04, {s: 0.4, y: 20, d: 0.6});
  arr("#chCof", @kavu-0.04, {s: 0.4, y: 20, d: 0.6});
  arr("#ch5", @n5-0.04, {s: 0.4, y: 20, d: 0.6});
  /* «це заспокоює людей у чаті»: the panic turns into calm */
{{calm}}
  [0, 1, 2].forEach(function (j) {
    tl.fromTo("#hr" + j, {autoAlpha: 0, y: 40, scale: 0.4}, {autoAlpha: 1, y: 0, scale: 1, duration: 0.45, ease: POP, immediateRender: false}, @perest+0.05 + j * 0.16);
    tl.to("#hr" + j, {y: -150, autoAlpha: 0, duration: 0.9, ease: "power1.in"}, @perest+0.55 + j * 0.16);
  });
  G.irisClose("#gT1", @tobe-0.32, {{cx}}, {{cy}}, 0.5);""").replace("{{calm}}", calm).replace(
        "{{ix}}", str(IRIS1[0])).replace("{{iy}}", str(IRIS1[1])).replace(
        "{{cx}}", str(IRIS2[0])).replace("{{cy}}", str(IRIS2[1]))


# ===========================================================================
# D2 · step 2: where is the problem — OBS, YouTube, Webinar Stars
C1 = "M306 300 C 360 288 392 288 446 300"
C2 = "M636 300 C 690 312 722 312 776 300"
YT_C = (540, 300)


@beat
def d2_chain():
    cab = ('<svg class="cab abs" width="1080" height="700" viewBox="0 0 1080 700" style="left:0;top:0;overflow:visible">'
           '<path class="tube hide" id="c1T" d="%(c1)s"/><path class="core hide" id="c1C" d="%(c1)s"/>'
           '<path class="tube hide" id="c2T" d="%(c2)s"/><path class="core hide" id="c2C" d="%(c2)s"/>'
           '<path class="tube hide" id="hAT" d="M306 300 Q 340 290 370 290"/><path class="core hide" id="hAC" d="M306 300 Q 340 290 370 290"/>'
           '<path class="tube hide" id="hBT" d="M446 300 Q 412 290 382 290"/><path class="core hide" id="hBC" d="M446 300 Q 412 290 382 290"/>'
           '<g class="pkg"><path class="pkt" id="c1P" style="opacity:0" d="%(c1)s"/></g>'
           '%(spk)s</svg>'
           % {"c1": C1, "c2": C2,
              "spk": "".join('<path class="spk hide" id="sp%d" d="M%d %d L %d %d"/>'
                             % (j, 376 + dx * 14, 290 + dy * 14, 376 + dx * 46, 290 + dy * 46)
                             for j, (dx, dy) in enumerate(((0, -1), (0.8, -0.6), (-0.8, -0.6), (0.9, 0.4), (-0.9, 0.4), (0, 1))))})
    wrp = ('<div class="wrp hide" id="wrp" style="left:380px;top:152px;width:320px;height:306px">'
           '<div class="wl">Webinar Stars</div><div class="shc"><div class="sheen"></div></div></div>')
    lens = '<div class="lens hide" id="lens"><div class="hdl"></div><div class="gl2"></div></div>'
    chip = '<div class="pill j hide" id="ch01" style="left:300px;top:332px;width:156px;height:72px;font-size:36px">0:01</div>'
    L.append('<div class="g full" id="gD2">' + checklist("chkD2", CHK_D2[0], CHK_D2[1], done=(0, 1))
             + '<div class="shelf edge hide" id="shT" style="left:70px;top:150px;width:940px;height:400px"></div>'
             + cab + wrp
             + tile("tOB", 190, 115, 205, "jelly", g.mark("obsstudio"))
             + tile("tYT", 190, 445, 205, "pearl", g.mark("youtube"))
             + tile("tWS", 190, 775, 205, "jelly", ws_mark(40))
             + tile("shd", 84, 912, 178, "pearl", stroke("shield"), extra_cls="circ", ring=False)
             + chip + lens + '</div>')
    sfx("click-soft", T["problema"] + 0.12)
    sfx("pop", T["obs1"] + 0.02, -3)
    sfx("pop", T["yt1"] + 0.02, -3)
    sfx("pop", T["ws1"] + 0.02, -2)
    sfx("whoosh-short", T["obhortka"] + 0.02, -5)
    sfx("glitch-1", T["pererv"] + 0.02)
    sfx("click", T["zakhodymo"] + 0.05)
    sfx("ping", T["perepidk"] + 0.55, -4)
    return js("""
  tl.set("#gD2", {autoAlpha: 1}, @tobe-0.4);
  arr("#chkD2", @tobe-0.36, {s: 0.85, y: 20, d: 0.7});
  hl("chkD2", 2, @dyvymos);
  lab("chkD2", 2, @de);
  tick("chkD2", 2, @problema+0.1);
  bout("#chkD2", @zviazka-0.08, 10, 0.28);
  /* the pipeline: OBS -> YouTube -> Webinar Stars */
  arr("#shT", @zviazka+0.02, {s: 0.92, y: 20, d: 0.7});
  arr("#tOB", @obs1-0.05, {s: 0.4, y: 20, d: 0.7}); G.ripple("#tOBR", @obs1+0.25);
  tl.set(["#c1T", "#c1C"], {autoAlpha: 1}, @obs1+0.3);
  draw2("c1T", @obs1+0.3, 0.4); draw2("c1C", @obs1+0.3, 0.4);
  arr("#tYT", @yt1-0.05, {s: 0.4, y: 20, d: 0.7}); G.ripple("#tYTR", @yt1+0.25);
  tl.set(["#c2T", "#c2C"], {autoAlpha: 1}, @yt1+0.22);
  draw2("c2T", @yt1+0.22, 0.35); draw2("c2C", @yt1+0.22, 0.35);
  arr("#tWS", @ws1-0.05, {s: 0.4, y: 20, d: 0.7}); G.ripple("#tWSR", @ws1+0.25);
  G.bump("#tWS", @ws2);
  /* «ламається рідко»: a shield on it */
  arr("#shd", @lamaietsia-0.02, {s: 0.3, y: 10, d: 0.6});
  /* «просто обгортка твого відео з YouTube»: it wraps the video */
  tl.to("#shd", {autoAlpha: 0, scale: 0.5, duration: 0.2}, @obhortka-0.05);
  tl.to(["#c2T", "#c2C"], {autoAlpha: 0, duration: 0.2}, @obhortka-0.05);
  tl.to("#tWS", {x: -330, scale: 1.4, autoAlpha: 0, duration: 0.42, ease: "power2.in"}, @obhortka-0.02);
  tl.fromTo("#wrp", {autoAlpha: 0, x: 330, scale: 0.55}, {autoAlpha: 1, x: 0, scale: 1, duration: 0.75, ease: SP}, @obhortka+0.12);
  shn("#wrp .sheen", @obhortka+0.4);
  tl.to(["#tOB", "#c1T", "#c1C"], {autoAlpha: 0.3, duration: 0.3}, @obhortka+0.1);
  /* «тому йдемо одразу перевіряти»: unwrap, the lens */
  tl.to("#wrp", {autoAlpha: 0, x: 330, scale: 0.55, duration: 0.4, ease: "power2.in"}, @tomu3-0.05);
  tl.fromTo("#tWS", {x: -330, scale: 1.4, autoAlpha: 0}, {x: 0, scale: 1, autoAlpha: 1, duration: 0.6, ease: SP, immediateRender: false}, @tomu3+0.1);
  tl.to(["#c2T", "#c2C", "#tOB", "#c1T", "#c1C"], {autoAlpha: 1, duration: 0.3}, @tomu3+0.2);
  tl.fromTo("#lens", {autoAlpha: 0, x: 760, y: 420, scale: 0.6}, {autoAlpha: 1, x: {{ytx}}, y: {{yty}}, scale: 1, duration: 0.7, ease: SP}, @pereviriaty-0.1);
  G.bump("#tYT", @yt2+0.05);
  tl.to("#lens", {x: 271, y: 185, duration: 0.5, ease: SP}, @zviazok-0.05);
  tl.to("#lens", {x: 105, y: 195, duration: 0.5, ease: SP}, @obs2-0.05);
  bout("#lens", @yakshcho-0.1, 8, 0.28);
  /* «якщо зв'язок з OBS перерваний»: the cable snaps */
  tl.set(["#c1T", "#c1C"], {autoAlpha: 0}, @pererv);
  tl.set(["#hAT", "#hAC", "#hBT", "#hBC"], {autoAlpha: 1}, @pererv);
  ["hAT", "hAC", "hBT", "hBC"].forEach(function (id) {
    var L = document.getElementById(id).getTotalLength() + 3;
    gsap.set("#" + id, {strokeDasharray: (L - 3) + " " + (L + 40), strokeDashoffset: 0});
    tl.to("#" + id, {strokeDashoffset: L * 0.72, duration: 0.45, ease: "power3.out"}, @pererv+0.02);
  });
  [0, 1, 2, 3, 4, 5].forEach(function (j) {
    tl.set("#sp" + j, {autoAlpha: 1}, @pererv);
    draw2("sp" + j, @pererv, 0.2);
    tl.to("#sp" + j, {autoAlpha: 0, duration: 0.3}, @pererv+0.22);
  });
  G.haptic("#tOB", @pererv+0.02);
  /* «заходимо в OBS і перепідключаємо все з нуля» */
  G.bump("#tOB", @zakhodymo+0.03); G.ripple("#tOBR", @zakhodymo+0.08);
  tl.set(["#hAT", "#hAC", "#hBT", "#hBC"], {autoAlpha: 0}, @perepidk);
  tl.set(["#c1T", "#c1C"], {autoAlpha: 1}, @perepidk);
  draw2("c1T", @perepidk, 0.5); draw2("c1C", @perepidk, 0.5);
  G.packet("c1P", @perepidk+0.5, 0.45);
  G.bump("#tYT", @perepidk+0.92); G.ripple("#tYTR", @perepidk+0.92);
  /* «це займає буквально секунду» */
  arr("#ch01", @bukvalno-0.02, {s: 0.4, y: 10, d: 0.6});
  tl.set("#gD2", {autoAlpha: 0}, @ale+0.9);""").replace("{{ytx}}", str(YT_C[0] - 105)).replace("{{yty}}", str(YT_C[1] - 105))


# ===========================================================================
# TK2 · step 3: stop, new key in OBS, back to YouTube, LIVE, the new link to Webinar Stars
NEWKEY = u"k7d2 9fqx m4tz 81wp"


@beat
def t2_restart():
    ytc = ('<div class="sheet ytc hide" id="ytc" style="left:110px;top:170px;width:860px;height:760px">'
           '<div class="tw" style="left:36px;top:30px;width:84px;height:84px"><div class="pearl">%s</div></div>'
           '<i class="hb" style="left:144px;top:58px;width:260px;height:28px"></i>'
           '<div class="live off" id="ytO"><b></b>LIVE</div><div class="live hide" id="ytL"><b></b>LIVE</div>'
           '<div class="pv" id="pv">'
           '<svg class="spn abs" id="spn" width="170" height="170" viewBox="0 0 170 170" style="left:305px;top:135px">'
           '<circle cx="85" cy="85" r="66"/></svg>'
           '<div class="stp hide" id="stp" style="left:338px;top:168px"></div>'
           '<div class="tw circ hide" id="ppr" style="left:295px;top:125px;width:190px;height:190px"><div class="pearl">%s</div></div>'
           '</div>'
           '<div class="sbt" id="sbt">Завершити</div>'
           '<i class="rr" style="left:460px;top:654px;width:300px;height:28px;border-radius:14px"></i>'
           '<div class="shc"><div class="sheen"></div></div></div>' % (g.mark("youtube"), stroke("person")))
    tap = ('<div class="ckr" id="ckr" style="left:340px;top:838px"></div>'
           '<div class="fing hide" id="fing" style="left:340px;top:838px"></div>')
    okc = ('<div class="obs hide" id="okc" style="left:90px;top:150px;width:900px;height:430px">'
           '<div class="tw circ" style="left:34px;top:24px;width:72px;height:72px"><div class="jelly">%s</div></div>'
           '<div class="tt">OBS Studio</div>'
           '<div class="wd" style="left:792px"></div><div class="wd" style="left:820px"></div><div class="wd" style="left:848px"></div>'
           '<div class="lb2">КЛЮЧ ТРАНСЛЯЦІЇ</div>'
           '<div class="fld" id="fld"><div id="keyT"></div><div class="shc"><div class="sheen"></div></div></div>'
           '<div class="tw circ" id="rgB" style="left:744px;top:196px;width:120px;height:120px"><div class="jelly">%s</div></div>'
           '</div>' % (g.mark("obsstudio"), stroke("refresh")))
    vcab = ('<svg class="cab abs" width="1080" height="1920" viewBox="0 0 1080 1920" style="left:0;top:0">'
            '<path class="tube hide" id="vT" d="M540 584 L 540 690"/><path class="core hide" id="vC" d="M540 584 L 540 690"/></svg>')
    kp = ('<div class="kp hide" id="kp" style="left:360px;top:362px"><div class="kc">%s</div>%s</div>'
          % (stroke("key"), NEWKEY[:9] + u"…"))
    lnk = ('<div class="lnk hide" id="lnk2" style="left:330px;top:600px"><div class="lc">%s</div>'
           'youtube.com<em>/live/…</em></div>' % stroke("link"))
    wsg = ('<div class="tw hide" id="wsG" style="left:430px;top:220px;width:220px;height:220px">'
           '<div class="clear ghost">%s</div></div>' % ws_mark(46))
    L.append('<div class="g full" id="gT2"><div class="tkg"></div><div class="aurs"></div><div class="grain"></div>'
             + vcab + ytc + tap + okc + kp + wsg + tile("tWS2", 220, 430, 220, "jelly", ws_mark(46)) + lnk + '</div>')
    sfx("whoosh-short", T["ale"] - 0.12)
    sfx("click", T["vymyk"] + 0.08)
    sfx("click", T["heneruiemo"] + 0.25)
    sfx("click-soft", T["kliuch"] + 0.02)
    sfx("pop", T["znovu"] + 0.0, -4)
    sfx("ping", T["novu"] + 0.02, -3)
    sfx("click-soft", T["nove"] + 0.02, -3)
    sfx("pop", T["ws3"] + 0.02, -2)
    sfx("whoosh-short", T["ws3e"] - 0.4, -4)
    return js("""
  G.irisOpen("#gT2", @ale-0.1, {{yx}}, {{yy}}, 0.85);
  drift1("#gT2", @ale, @ws3e-@ale);
  gsap.set("#ytc", {transformOrigin: "50% 50%"});
  arr("#ytc", @ale+0.02, {s: 0.4, y: -200, d: 0.9});
  /* «так і не йде»: it spins and stalls */
  tl.fromTo("#spn", {rotation: 0, transformOrigin: "50% 50%"}, {rotation: 640, duration: @vymyk-@ale-0.1, ease: "power2.out"}, @ale+0.1);
  /* «вимикаємо трансляцію повністю» */
  tl.fromTo("#fing", {autoAlpha: 0, x: 180, y: 220, scale: 1.3}, {autoAlpha: 1, x: 0, y: 0, scale: 1, duration: 0.45, ease: SP, immediateRender: false}, @vymyk-0.4);
  tl.to("#fing", {scale: 0.8, duration: 0.1}, @vymyk+0.08); tl.to("#fing", {scale: 1, autoAlpha: 0, duration: 0.4}, @vymyk+0.18);
  tl.to("#sbt", {scale: 0.94, duration: 0.1, ease: "power2.out"}, @vymyk+0.08);
  tl.to("#sbt", {scale: 1, duration: 0.45, ease: SP}, @vymyk+0.18);
  tl.fromTo("#ckr", {scale: 0.3, autoAlpha: 0.95}, {scale: 2.2, autoAlpha: 0, duration: 0.7, ease: "power2.out", immediateRender: false}, @vymyk+0.1);
  tl.to("#spn", {autoAlpha: 0, duration: 0.2}, @vymyk+0.15);
  tl.fromTo("#stp", {autoAlpha: 0, scale: 0.4}, {autoAlpha: 1, scale: 1, duration: 0.5, ease: POP}, @vymyk+0.25);
  tl.to("#ytc", {y: 380, scale: 0.62, duration: 0.65, ease: SP}, @povnistiu+0.05);
  /* «генеруємо новий ключ в OBS» */
  arr("#okc", @heneruiemo-0.08, {s: 0.8, y: -40, d: 0.75});
  G.bump("#rgB", @heneruiemo+0.25);
  tl.fromTo("#rgB .sk", {rotation: 0, transformOrigin: "50% 50%"}, {rotation: 360, duration: 0.7, ease: "power2.inOut"}, @heneruiemo+0.25);
  shn("#fld .sheen", @kliuch);
  /* «підключаємо його знову до YouTube» */
  tl.set(["#vT", "#vC"], {autoAlpha: 1}, @pidkl-0.02);
  draw2("vT", @pidkl-0.02, 0.4); draw2("vC", @pidkl-0.02, 0.4);
  tl.fromTo("#kp", {autoAlpha: 0, scale: 0.5, y: 0}, {autoAlpha: 1, scale: 1, y: 0, duration: 0.4, ease: POP}, @pidkl);
  tl.to("#kp", {y: 524, scale: 0.55, duration: 0.55, ease: "power2.in"}, @pidkl+0.4);
  tl.set("#kp", {autoAlpha: 0}, @pidkl+0.96);
  tl.to("#ytc", {scale: 0.67, duration: 0.1, ease: "power2.out"}, @znovu);
  tl.to("#ytc", {scale: 0.62, duration: 0.45, ease: SP}, @znovu+0.1);
  /* «запускаємо нову трансляцію»: LIVE */
  bout(["#okc", "#vT", "#vC"], @zapusk-0.08, 10, 0.3);
  tl.to("#ytc", {y: -30, scale: 0.82, duration: 0.7, ease: SP}, @zapusk);
  tl.to("#stp", {autoAlpha: 0, scale: 0.5, duration: 0.2}, @zapusk+0.05);
  arr("#ppr", @zapusk+0.2, {s: 0.4, y: 10, d: 0.6});
  tl.set("#ytO", {autoAlpha: 0}, @novu); tl.fromTo("#ytL", {autoAlpha: 0, scale: 0.6}, {autoAlpha: 1, scale: 1, duration: 0.45, ease: POP}, @novu);
  shn("#ytc .sheen", @novu+0.1);
  /* «вставляємо нове посилання назад у Webinar Stars» */
  tl.to("#ytc", {y: 340, scale: 0.6, duration: 0.6, ease: SP}, @vstavl-0.05);
  arr("#lnk2", @nove-0.04, {s: 0.5, y: 60, d: 0.6});
  bin("#wsG", @nazad-0.1, 8, 0.3);
  tl.to("#lnk2", {y: -150, duration: 0.55, ease: SP}, @nazad);
  arr("#tWS2", @ws3-0.06, {s: 0.5, y: 0, d: 0.7});
  tl.set("#wsG", {autoAlpha: 0}, @ws3+0.2);
  tl.to("#lnk2", {y: -300, scale: 0.2, autoAlpha: 0, duration: 0.32, ease: "power3.in"}, @ws3+0.12);
  G.bump("#tWS2", @ws3+0.45); G.ripple("#tWS2R", @ws3+0.45);
  G.irisClose("#gT2", @ws3e-0.4, 540, 330, 0.5);""").replace("{{yx}}", str(YT_C[0])).replace("{{yy}}", str(YT_C[1]))


# ===========================================================================
# E · nothing noticed; one recording becomes two
@beat
def e_viewers():
    viewers = "".join(tile("vw%d" % j, 104, 306 + j * 120, 474, "pearl", stroke("person"), extra_cls="circ", ring=False)
                      for j in range(4))
    hearts = "".join('<div class="tw circ hrt hide" id="vh%d" style="left:%dpx;top:420px"><div class="jelly">%s</div></div>'
                     % (j, 321 + j * 120, stroke("heart")) for j in range(4))

    def rcd(rid, x):
        return ('<div class="rcd hide" id="%s" style="left:%dpx;top:170px"><div class="th"><div class="pc">%s</div></div>'
                '<div class="tw" style="left:20px;top:240px;width:64px;height:64px"><div class="pearl">%s</div></div>'
                '<i class="hb" style="left:100px;top:250px;width:220px;height:22px;border-radius:8px"></i>'
                '<i class="rr" style="left:100px;top:288px;width:150px;height:16px;border-radius:8px"></i></div>'
                % (rid, x, PLAY, g.mark("youtube")))
    nb = ('<div class="nbd hide" id="nb1" style="left:88px;top:140px">1</div>'
          '<div class="nbd hide" id="nb2" style="left:548px;top:140px">2</div>')
    L.append('<div class="g full" id="gE">' + screen("scrE", 180, 130, fill=0.35) + viewers + hearts
             + rcd("rcB", 340) + rcd("rcA", 340) + nb + '</div>')
    sfx("pop", T["zamist"] - 0.1, -4)
    sfx("pop", T["lezhat"] + 0.03, -3)
    return js("""
  tl.set("#gE", {autoAlpha: 1}, @ws3e-0.45);
  arr("#scrE", @ws3e-0.4, {s: 0.5, y: 0, d: 0.8});
  tl.fromTo("#scrEF", {scaleX: 0.35}, {scaleX: 0.72, duration: @yedyna-@na, ease: "none"}, @na);
  [0, 1, 2, 3].forEach(function (j) { arr("#vw" + j, @hliadachi-0.05 + j * 0.08, {s: 0.4, y: 40, d: 0.65}); });
  [0, 1, 2, 3].forEach(function (j) {
    tl.fromTo("#vh" + j, {autoAlpha: 0, y: 30, scale: 0.4}, {autoAlpha: 1, y: 0, scale: 1, duration: 0.4, ease: POP, immediateRender: false}, @nichoho+0.2 + j * 0.1);
    tl.to("#vh" + j, {y: -110, autoAlpha: 0, duration: 0.8, ease: "power1.in"}, @nichoho+0.7 + j * 0.1);
  });
  bout(["#vw0", "#vw1", "#vw2", "#vw3"], @yedyna-0.05, 10, 0.28);
  /* «замість одного запису ... два окремих записи» */
  tl.to("#scrE", {scale: 0.55, autoAlpha: 0, filter: "blur(10px)", duration: 0.35, ease: "power2.in"}, @zamist-0.4);
  tl.set("#scrE", {filter: "none"}, @zamist);
  arr("#rcA", @zamist-0.1, {s: 0.6, y: 20, d: 0.75});
  tl.set("#rcB", {autoAlpha: 1}, @lezhat);
  tl.to("#rcA", {x: -230, rotation: -2, duration: 0.7, ease: SP}, @lezhat);
  tl.fromTo("#rcB", {x: 0, scale: 0.9}, {x: 230, rotation: 2, scale: 1, duration: 0.7, ease: SP, immediateRender: false}, @lezhat);
  arr("#nb1", @dva-0.02, {s: 0.3, y: 10, d: 0.55});
  arr("#nb2", @dva+0.1, {s: 0.3, y: 10, d: 0.55});
  bout("#gE", @zapysye-0.05, 10, 0.28);""")


# ===========================================================================
# F · five minutes, all four ticked; scary — and back LIVE
@beat
def f_recap():
    L.append('<div class="g full" id="gF">' + checklist("chkF", 130, 150, done=(0, 1, 2))
             + tile("t5", 180, 830, 96, "jelly", '<div class="dig" style="font-size:56px">5:00</div>', extra_cls="circ")
             + screen("scrF", 180, 130, broken=True, fill=0.5) + '</div>')
    sfx("click-soft", T["use"] + 0.3)
    sfx("pop", T["piat"] + 0.02, -2)
    sfx("glitch-1", T["strashno"] + 0.02)
    sfx("ping", T["katastr"] + 0.02, -2)
    return js("""
  tl.set("#gF", {autoAlpha: 1}, @use-0.3);
  arr("#chkF", @use-0.28, {s: 0.75, y: 40});
  hl("chkF", 3, @use-0.05);
  lab("chkF", 3, @use+0.05);
  tick("chkF", 3, @use+0.28);
  arr("#t5", @piat-0.06, {s: 0.3, y: 20, d: 0.7});
  tl.fromTo("#t5", {rotation: -24}, {rotation: -8, duration: 0.8, ease: SP, immediateRender: false}, @piat-0.06);
  gsap.set("#t5", {rotation: -24});
  G.ripple("#t5R", @piat+0.25);
  bout(["#chkF", "#t5"], @umomenti-0.12, 10, 0.26);
  /* «у моменті це страшно»: the screen is down again */
  arr("#scrF", @umomenti+0.02, {s: 0.75, y: 30, d: 0.7});
  {{glitch}}
  G.haptic("#scrF", @strashno+0.4);
  /* «але по факту абсолютно не катастрофа»: back LIVE */
  tl.to("#scrFN", {scaleY: 0, duration: 0.55, ease: "power2.inOut"}, @absol);
  tl.set("#scrFO", {autoAlpha: 0}, @katastr); tl.fromTo("#scrFL", {autoAlpha: 0, scale: 0.6}, {autoAlpha: 1, scale: 1, duration: 0.45, ease: POP}, @katastr);
  shn("#scrF .sheen", @katastr+0.05); G.bump("#scrF", @katastr+0.05);
  tl.fromTo("#scrFF", {scaleX: 0.5}, {scaleX: 0.58, duration: 0.6, ease: "none", immediateRender: false}, @katastr);
  bout("#scrF", @katastre-0.12, 10, 0.26);
  tl.set("#gF", {autoAlpha: 0}, @katastre+0.2);""").replace("{{glitch}}", glitch("scrF", T["strashno"]))


# ===========================================================================
# G · Стежити
@beat
def g_follow():
    L.append('<div class="g full" id="gG"><div class="fl hide" id="fl" style="left:190px;top:300px;width:700px;height:150px">'
             '<div class="tw circ" style="left:28px;top:27px;width:96px;height:96px"><div class="jelly">%s</div></div>'
             '<div class="t" id="flT">Стежити</div>'
             '<div class="on" id="flOn"><div class="tw circ" style="left:28px;top:27px;width:96px;height:96px">'
             '<div class="pearl">%s</div></div><div class="t">Ви стежите</div></div>'
             '<div class="ckr" id="ck4" style="left:470px;top:75px"></div>'
             '<div class="shc"><div class="sheen"></div></div></div></div>'
             % (g.mark("instagram"), stroke("check")))
    sfx("pop", T["pidp1"] + 0.02, -3)
    sfx("click", T["pidp2"] + 0.02)
    return js("""
  tl.set("#gG", {autoAlpha: 1}, @pidp1-0.1);
  arr("#fl", @pidp1-0.04, {s: 0.6, y: 40});
  tl.to("#fl", {scale: 0.95, duration: 0.09, ease: "power2.out"}, @pidp2);
  tl.to("#fl", {scale: 1, duration: 0.45, ease: SP}, @pidp2+0.09);
  tl.fromTo("#flOn", {autoAlpha: 0}, {autoAlpha: 1, duration: 0.2}, @pidp2+0.04);
  tl.set("#flT", {autoAlpha: 0}, @pidp2+0.05);
  tl.fromTo("#ck4", {scale: 0.3, autoAlpha: 0.95}, {scale: 2.4, autoAlpha: 0, duration: 0.7, ease: "power2.out", immediateRender: false}, @pidp2+0.02);
  shn("#fl .sheen", @pidp2+0.15);""")


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
  /* the checklist: highlight a row, write its step, tick it */
  function hl(p, i, t) { tl.fromTo("#" + p + "H" + i, {autoAlpha: 0, scaleX: 0.9}, {autoAlpha: 1, scaleX: 1, duration: 0.45, ease: SP}, t); }
  function lab(p, i, t) {
    tl.to("#" + p + "G" + i, {autoAlpha: 0, duration: 0.18}, t);
    tl.fromTo("#" + p + "L" + i, {autoAlpha: 0, x: -24, filter: "blur(8px)"}, {autoAlpha: 1, x: 0, filter: "blur(0px)", duration: 0.36, ease: "power2.out"}, t);
    tl.set("#" + p + "L" + i, {filter: "none"}, t + 0.37);
  }
  function tick(p, i, t) {
    tl.fromTo("#" + p + "C" + i, {autoAlpha: 0, scale: 0.4}, {autoAlpha: 1, scale: 1, duration: 0.4, ease: POP}, t);
    draw2(p + "P" + i, t + 0.06, 0.3);
  }
  gsap.set(".sheen", {xPercent: -120});
"""


def clock_js():
    """Every text that changes over time is painted from one clock, so any frame renders cold."""
    sw0 = T["n30"] + 1.0                       # 0:30 -> 0:29 -> 0:28, in real seconds
    a0, a1 = T["bilshe"] - 0.02, T["n30b"] + 0.15
    c0, c1 = T["vebinariv2"] + 0.35, T["ievro"] - 0.05
    m0, m1 = T["ne1"] + 0.05, T["poverne"] - 0.02
    mc = T["mozhete"] + 0.02
    k0, k1 = T["heneruiemo"] + 0.3, T["kliuch"] + 0.02
    return r"""
  var CLK = {t: 0}, P = {};
  var E_DIG = document.getElementById("dig"), E_C30 = document.getElementById("c30"),
      E_CNT = document.getElementById("cnt"), E_MSG = document.getElementById("msgT"),
      E_KEY = document.getElementById("keyT");
  var MSG = %(msg)s, KEY0 = "•••• •••• •••• ••••", KEY1 = %(key)s, CH = "abcdefghjkmnpqrstuvwxyz23456789";
  function put(el, key, s) { if (P[key] !== s) { P[key] = s; el.textContent = s; } }
  function ease3(p) { return 1 - Math.pow(1 - p, 3); }
  function clamp(p) { return p < 0 ? 0 : p > 1 ? 1 : p; }
  function paintAll() {
    var t = CLK.t;
    var n = t < %(sw0).3f ? 0 : Math.min(2, Math.floor(t - %(sw0).3f) + 1);
    put(E_DIG, "d", "0:" + (30 - n));
    put(E_C30, "a", String(Math.round(30 * ease3(clamp((t - %(a0).3f) / %(ad).3f)))));
    var v = Math.round(13000 * ease3(clamp((t - %(c0).3f) / %(cd).3f)) / 100) * 100;
    put(E_CNT, "c", v >= 1000 ? Math.floor(v / 1000) + " " + ("00" + (v %% 1000)).slice(-3) : String(v));
    var m = t <= %(m0).3f ? 0 : t >= %(m1).3f ? MSG.length : Math.round(MSG.length * (t - %(m0).3f) / %(md).3f);
    put(E_MSG, "m", t >= %(mc).3f ? "" : MSG.slice(0, m));
    var s = KEY0;
    if (t >= %(k1).3f) s = KEY1;
    else if (t >= %(k0).3f) {
      var f = Math.floor(t * 30); s = "";
      for (var i = 0; i < KEY1.length; i++) {
        if (KEY1.charAt(i) === " ") { s += " "; continue; }
        s += CH.charAt((f * 7 + i * 13 + (f * i) %% 11) %% CH.length);
      }
    }
    put(E_KEY, "k", s);
  }
  paintAll();
  tl.fromTo(CLK, {t: 0}, {t: %(dur).3f, duration: %(dur).3f, ease: "none", onUpdate: paintAll}, 0);""" % {
        "msg": json.dumps(MSG, ensure_ascii=False), "key": json.dumps(NEWKEY, ensure_ascii=False),
        "sw0": sw0, "a0": a0, "ad": a1 - a0, "c0": c0, "cd": c1 - c0,
        "m0": m0, "m1": m1, "md": m1 - m0, "mc": mc, "k0": k0, "k1": k1, "dur": DUR}


# captions that would repeat the graphic's own words (STYLE.md §2b.1)
def span_words(a, b):
    return (round(a - 0.02, 3), round(b, 3), "")


BLACKOUT = [
    span_words(T["n30"], T["sekunde"]),                       # the stopwatch says 0:30
    span_words(T["bilshe"], T["n30be"]),                      # the badge says 30+
    span_words(T["n13"], T["ievroe"]),                        # the card says 13 000 €
    span_words(T["ne0"], T["panike"]),                        # row 0 says Не панікувати
    span_words(T["napysaty"], T["chate"]),                    # row 1 says Написати в чат
    span_words(T["ne1"], T["poverne"]),                       # the message types it
    span_words(T["n5"], T["khvylyne"]),                       # the chip says 5:00
    span_words(T["de"], T["probe"]),                          # row 2 says Де проблема?
    span_words(T["ws1"], T["ws2e"]),                          # the tile says Webinar Stars (twice)
    span_words(T["kliuch"], T["obs5e"]),                      # the card says КЛЮЧ ... OBS Studio
    span_words(T["ws3"], T["ws3e"]),                          # the tile says Webinar Stars
    span_words(T["khv5"], T["piate"]),                        # the timer says 5:00
]
# the burgundy takeovers: white captions sit on the ground, the scrim would only halo
SCRIM_OFF = [(T["zdaie"] + 0.3, T["tobe"] + 0.1, ""), (T["ale"] + 0.4, T["ws3e"] + 0.1, "")]


def main():
    # nothing but captions inside her closeup
    assert T["vse"] + 0.49 < NP0 and T["nulovyi"] - 0.1 > NP1, (T["vse"], T["nulovyi"], NO_PAINT)
    gj = []
    for fn in BEATS:
        j = fn()
        gj.append("  /* %s */" % fn.__name__)
        gj.append(j.rstrip())
    assert not [c for c in SFX if NP0 - 0.05 <= c["t"] <= NP1], "a cue lands on her closeup"
    push = ["#vid"]
    head = [g.js(), HEAD_JS, clock_js(),
            '  gsap.set(%s, {transformOrigin: "540px 900px"});' % json.dumps(push),
            '  tl.fromTo(%s, {scale: 1}, {scale: 1.045, duration: %.3f, ease: "none"}, 0);' % (json.dumps(push), DUR)]
    doc = k.document(
        title=u"Reel 25 — ефір упав",
        plate="assets/base.mp4",
        gfx_html=g.defs() + "\n" + "\n".join(L),
        gfx_js="\n".join(head + gj),
        caps=CAPS,
        blackout=BLACKOUT,
        scrim_off=SCRIM_OFF,
    )
    io.open(os.path.join(HERE, "index.html"), "w", encoding="utf-8").write(doc)
    SFX.sort(key=lambda c: c["t"])
    io.open(os.path.join(HERE, "sfx.json"), "w", encoding="utf-8").write(json.dumps(SFX, indent=1))
    print("index.html  %d captions, %d beats, %d sfx cues (%.2f/s)" % (len(CAPS), len(BEATS), len(SFX), len(SFX) / DUR))


main()
