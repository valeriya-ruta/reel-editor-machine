# -*- coding: utf-8 -*-
"""Reel 21 — «Клод мені сказав… показувати, що я роблю». Posts 2026-10-05.

First reel she handed over raw: I cut it (tools/cut.py — last take wins,
framing changes on every cut, the closeup on «навайбкоджений»), it carries
sound design (tools/sfx.py), and the graphics are refined glass (STYLE.md §0).

The one object is **her webinar site**. Claude reads it and rewrites it; the
viewer sees why the site matters (4 days, ads running, sign-ups and sales),
then what Clarity sees on it (a cursor that moves, clicks, stalls), the button
that gets moved where people will press it, the connector that lets Claude do
all that, the list she approves, the code diff, and the routine that repeats
it every three days.

Chain:  near: a Claude notification lands («Клод мені сказав») -> it folds into
the Claude tile, the site card comes in beside it, data flows site -> Claude,
changes flow back and the site rearranges; a Meta tile (the ads) gets an up
badge -> near: the calendar rolls 7 -> 4 days, LIVE, the ads tile spins; bars
climb, sign-ups get ticks, a € coin -> the iris opens out of the coin: two
analytics slots, GA and Clarity, Clarity wins; GA only counts in / out ->
Clarity grows into her page: the cursor wanders, clicks twice, stalls (heat);
the page is rearranged and the button lands where the cursor taps it -> the
iris closes onto the Clarity tile: cable to Claude, the prompt types her ask,
send -> the list, ticked line by line, «Так» -> the code diff -> her closeup
(left clear) -> the routine: every third day lights -> Стежити.

usage: python build.py   (then: python ../tools/sfx.py mix 21)
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

CUT = json.load(io.open(os.path.join(ROOT, "work", "r21", "cut.json"), encoding="utf-8"))
DUR = 69.150           # 2075 plate frames / 30 (v2: clip starts trimmed to her first word)
FPS = 30
k = Kit(width=1080, height=1920, fps=FPS, duration=DUR)
g = Glass(["claude", "googleanalytics", "meta", "instagram"])
k.css(g.css())

# ---------------------------------------------------------------------------
# NO-PAINT: the closeups I cut in (tools/cut.py «punch»). Captions only.
NO_PAINT = [tuple(x) for x in CUT["no_paint"]]

CAPS = k.load_captions(os.path.join(ROOT, "work", "r21", "captions.json"))
FIX = {u"клікують,": u"клікають,", u"Тому": u"Тому", u"У": u"у", u"три": u"3",
       u"це)": u"це.", u"\"зареєструватися\".": u"зареєструватися.", u"\"так\"": u"«так»"}
for c in CAPS:
    c["w"] = FIX.get(c["w"], c["w"])
for _a, _b in zip(CAPS, CAPS[1:]):
    _a["e"] = round(max(_a["s"] + 0.10, _b["s"] - 0.085), 3)


def _n(s):
    return "".join(ch for ch in s.lower() if ch.isalnum())


# v2 re-cut the plate (two clip starts trimmed — her notes at 0:09 and 0:19).
# Beat anchors below were written against v1's timeline; map them across.
OLD = json.load(io.open(os.path.join(ROOT, "work", "r21", "cut-v1.json"), encoding="utf-8"))


def remap(t):
    for c in OLD["clips"]:
        if c["tl"] - 1e-6 <= t < c["tl"] + c["dur"] + 1e-6:
            src = c["src_in"] + (t - c["tl"])
            break
    else:
        return t
    best = min(CUT["clips"], key=lambda c: 0 if c["src_in"] <= src < c["src_in"] + c["dur"]
               else min(abs(src - c["src_in"]), abs(src - c["src_in"] - c["dur"])))
    # a time inside a trimmed lead-in lands on the start of the clip that replaced it
    return best["tl"] + min(max(0.0, src - best["src_in"]), best["dur"])


def S(word, near):
    near = remap(near)
    hits = [c for c in CAPS if _n(word) in [_n(x) for x in c["w"].split()]]
    c = min(hits, key=lambda c: abs(c["s"] - near))
    assert abs(c["s"] - near) < 0.6, (word, near, c["s"])
    return c["s"]


def E(word, near):
    near = remap(near)
    hits = [c for c in CAPS if _n(word) in [_n(x) for x in c["w"].split()]]
    return min(hits, key=lambda c: abs(c["s"] - near))["e"]


T = {
    "klod": S(u"Клод", 0.0), "pokazhu": S(u"покажу", 3.39), "klod2": S(u"Клод", 4.68),
    "analizuie": S(u"аналізує", 4.9), "dani": S(u"дані", 5.44), "saitu": S(u"сайту", 5.82),
    "zminiuie": S(u"змінює", 6.9), "tarhet": S(u"таргет", 7.96), "krashche": S(u"краще", 8.72),
    "dlia": S(u"Для", 9.27), "chotyry": S("4", 10.96), "dni": S(u"дні", 11.48),
    "vebinar": S(u"вебінар", 11.7), "tarhet2": S(u"таргет", 12.27), "krutytsia": S(u"крутиться", 12.74),
    "vazhlyvo": S(u"важливо", 13.88), "pidvyshchyty": S(u"підвищити", 14.94),
    "konversiiu": S(u"конверсію", 15.42), "liudei": S(u"людей", 16.45),
    "zareiestr": S(u"зареєструвалися", 16.71), "kupyly": S(u"купили", 18.26),
    "na": S(u"На", 18.87), "dvi": S(u"дві", 20.72), "google": S("Google", 21.85),
    "clarity1": S("Clarity", 23.57), "clarity2": S("Clarity", 24.4), "tsikavisha": S(u"цікавіша", 25.5),
    "rakhuie": S(u"рахує", 27.0), "zaishlo": S(u"зайшло", 27.84), "vyishlo": S(u"вийшло", 28.38),
    "pokazuie": S(u"показує", 28.93), "povedinku": S(u"поведінку", 29.83),
    "rukhaiutsia": S(u"рухаються", 31.03), "kudy": S(u"куди", 32.31), "klikaiut": S(u"клікають", 32.79),
    "halmuiut": S(u"гальмують", 33.49), "osnovi": S(u"основі", 35.16),
    "pidlasht": S(u"підлаштувати", 36.1), "liudyna": S(u"людина", 37.78),
    "tytsnula": S(u"тицьнула", 39.38), "knopku": S(u"кнопку", 40.02),
    "zareiestr2": S(u"зареєструватися", 40.48), "zareiestr2e": E(u"зареєструватися", 40.48),
    "tomu": S(u"Тому", 42.15), "konektor": S(u"конектор", 43.69), "klodi": S(u"Клоді", 44.05),
    "proshu": S(u"прошу", 45.27), "zaidy": S(u"зайди", 45.89), "pokrashchyty": S(u"покращити", 50.4),
    "pokrashchytye": E(u"покращити", 50.4),
    "dali": S(u"Далі", 51.58), "pereghl": S(u"переглядаю", 51.9), "pereviriaiu": S(u"перевіряю", 53.1),
    "lohichno": S(u"логічно", 54.08), "podob": S(u"подобається", 54.66), "tak": S(u"«так»", 55.95),
    "vin": S(u"він", 56.33), "kod": S(u"код", 57.24), "vnosyt": S(u"вносить", 57.58),
    "zminy": S(u"зміни", 58.24),
    "vidbuv": S(u"відбувається", 61.47), "avtom": S(u"автоматично", 62.24),
    "rutynu": S(u"рутину", 64.19), "povtor": S(u"повторюється", 64.77), "kozhni": S(u"кожні", 65.43),
    "dni3": S(u"дні", 65.93), "robyt": S(u"робить", 66.42),
    "yakshcho": S(u"Якщо", 67.98), "korysno": S(u"корисно", 68.4), "pidpysh": S(u"підпишись", 69.6),
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
    "up": '<path d="M12 19.2V5.4M6.2 11l5.8-5.8 5.8 5.8"/>',
    "check": '<path d="M5.4 12.6l4.3 4.3 8.9-9.5"/>',
    "in": '<path d="M3.5 12h11M10.5 7.5l4.5 4.5-4.5 4.5M14.5 4h3.5a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2h-3.5"/>',
    "out": '<path d="M9.5 12h11M16.5 7.5l4.5 4.5-4.5 4.5M9.5 4H6a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h3.5"/>',
    "person": '<circle cx="12" cy="8.2" r="3.6"/><path d="M4.8 20c.9-3.8 3.7-5.8 7.2-5.8s6.3 2 7.2 5.8"/>',
    "lock": '<rect x="5" y="10.5" width="14" height="10" rx="2.5"/><path d="M8.2 10.5V8a3.8 3.8 0 0 1 7.6 0v2.5"/>',
}
CURSOR = ('<svg viewBox="0 0 24 24" width="64" height="64"><path d="M4.2 2.8l14.6 8.1-6.3 1.5-3.1 5.9z" '
          'fill="#fff" stroke="#17141c" stroke-width="1.6" stroke-linejoin="round"/></svg>')


def stroke(name, cls="sk"):
    return '<svg class="%s" viewBox="0 0 24 24">%s</svg>' % (cls, STROKES[name])


def tile(tid, size, x, y, material, inner, extra_cls="", hide=True, ring=True):
    r = ('<div class="sqring" id="%sR" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx"></div>'
         % (tid, x, y, size, size)) if ring else ""
    return ('%s<div class="tw%s %s" id="%s" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx">'
            '<div class="%s">%s<div class="sheen"></div></div></div>'
            % (r, " hide" if hide else "", extra_cls, tid, x, y, size, size, material, inner))


def clarity_mark(size=50):
    return '<span class="wmark cl" style="font-size:%dpx">Clarity</span>' % size


k.css("""
.abs { position: absolute; }
.hide { opacity: 0; visibility: hidden; }
.tw { position: absolute; }
.sk { fill: none; stroke: url(#gw); stroke-width: 2.3; stroke-linecap: round; stroke-linejoin: round;
  width: 50%; height: 50%; position: relative; z-index: 1; overflow: visible; }
.pearl .sk { stroke: #17141c; }
.clear { overflow: hidden; }
.wmark.cl { color: #fff; letter-spacing: -0.03em; font-weight: 700; }
.circ .jelly, .circ .pearl, .circ .clear, .circ .sheen { border-radius: 50%; }
.aurs { position: absolute; left: -700px; top: -700px; width: 2480px; height: 3320px; pointer-events: none;
  background:
    radial-gradient(circle 526px at 1560px 880px, rgba(255,110,156,0.50), rgba(255,110,156,0)),
    radial-gradient(circle 634px at 760px 2360px, rgba(222,32,74,0.55), rgba(222,32,74,0)),
    radial-gradient(circle 382px at 1480px 1910px, rgba(255,198,214,0.20), rgba(255,198,214,0)); }

/* the notification */
#nt .app { position: absolute; left: 168px; top: 36px; font-size: 30px; font-weight: 700; color: rgba(255,255,255,0.72); }
#nt .tm  { position: absolute; right: 44px; top: 38px; font-size: 26px; font-weight: 500; color: rgba(255,255,255,0.5); }
#nt .msg { position: absolute; left: 168px; top: 84px; right: 40px; font-size: 41px; font-weight: 700; color: #fff;
  letter-spacing: -0.012em; line-height: 1.15; }

/* a website, small (her webinar page) */
.site { position: absolute; border-radius: 44px; overflow: hidden;
  background: linear-gradient(172deg, #ffffff 0%, #fff9fb 60%, #fdf0f4 100%);
  box-shadow: inset 0 2px 1px #fff, 0 44px 90px -34px rgba(24,4,12,0.62), 0 0 0 1px rgba(255,255,255,0.4); }
.site i, .pg i { position: absolute; display: block; }
.site .bar, .pg .bar { left: 0; top: 0; right: 0; background: #f6e6eb; }
.site .dot, .pg .dot { border-radius: 50%; background: rgba(23,20,28,0.18); }
.hb { border-radius: 12px; background: linear-gradient(115deg, #c41434 0%, #8d0d24 100%); }
.rr { border-radius: 9px; background: rgba(23,20,28,0.13); }
.im { border-radius: 22px; background: linear-gradient(150deg, #f4dfe5 0%, #ecc8d0 100%); }
.pg i.btn, .site i.btn { display: flex; font-style: normal; }
.btn { border-radius: 999px; background: linear-gradient(165deg, #e0204b 0%, #ab112e 46%, #6b081c 100%);
  box-shadow: inset 0 2px 1px rgba(255,255,255,0.5), 0 18px 36px -14px rgba(70,4,20,0.6);
  color: #fff; font-weight: 700; display: flex; align-items: center; justify-content: center; letter-spacing: -0.01em; }

/* the calendar */
.cal { position: absolute; border-radius: 52px; overflow: hidden;
  background: linear-gradient(170deg, #ffffff 0%, #fff6f9 60%, #f8e6ec 100%);
  box-shadow: inset 0 2px 1px #fff, 0 44px 80px -30px rgba(24,4,12,0.6); }
.cal .hd { position: absolute; left: 0; top: 0; right: 0; height: 84px;
  background: linear-gradient(165deg, #e0204b 0%, #8d0d24 100%); }
.cal .hole { position: absolute; top: 30px; width: 22px; height: 22px; border-radius: 50%; background: rgba(255,255,255,0.85); }
.cal .win { position: absolute; left: 0; right: 0; top: 96px; height: 170px; overflow: hidden; }
.cal .roll i { display: block; height: 170px; line-height: 170px; text-align: center; font-style: normal;
  font-size: 158px; font-weight: 900; letter-spacing: -0.04em;
  background: linear-gradient(118deg, #7e0b20 0%, #b4122f 42%, #ff6e9c 100%);
  -webkit-background-clip: text; background-clip: text; color: transparent; }
.cal .lb { position: absolute; left: 0; right: 0; top: 262px; text-align: center; font-size: 36px; font-weight: 700;
  color: rgba(23,20,28,0.45); }
.live { position: absolute; height: 66px; border-radius: 33px; padding: 0 26px; display: flex; align-items: center; gap: 12px;
  background: linear-gradient(165deg, #e0204b 0%, #8d0d24 100%); color: #fff; font-size: 30px; font-weight: 900;
  letter-spacing: 0.06em; box-shadow: inset 0 2px 1px rgba(255,255,255,0.5), 0 20px 40px -16px rgba(70,4,20,0.7); }
.live b { width: 16px; height: 16px; border-radius: 50%; background: #fff; display: block; }
.spin { position: absolute; fill: none; stroke: #ff8ab0; stroke-width: 8; stroke-linecap: round; stroke-dasharray: 60 34;
  filter: drop-shadow(0 0 10px rgba(255,110,156,0.8)); }

/* bars that climb */
.bar6 { position: absolute; bottom: 60px; width: 92px; border-radius: 22px; transform-origin: 50% 100%;
  background: linear-gradient(170deg, rgba(255,255,255,0.92) 0%, rgba(255,240,245,0.78) 100%);
  box-shadow: inset 0 2px 1px #fff, 0 20px 40px -18px rgba(24,4,12,0.5); }
.bar6.hot { background: linear-gradient(165deg, #ff6e9c 0%, #e0204b 50%, #8d0d24 100%); }

/* in / out chips */
.io { position: absolute; height: 84px; width: 150px; border-radius: 42px; display: flex; align-items: center; justify-content: center;
  background: linear-gradient(160deg, #ffffff 0%, #fff5f8 52%, #f5dfe6 100%);
  box-shadow: inset 0 2px 1px #fff, 0 26px 50px -20px rgba(8,0,3,0.7); }
.io .sk { width: 46px; height: 46px; stroke: #17141c; }

/* her page, full size, on the takeover */
.pg { position: absolute; overflow: hidden; border-radius: 56px; color: #17141c;
  background: linear-gradient(172deg, #ffffff 0%, #fff9fb 55%, #fdf0f4 100%);
  box-shadow: inset 0 2px 1px #fff, 0 70px 130px -40px rgba(8,0,3,0.75), 0 0 0 1px rgba(255,255,255,0.35); }
.pg .url { left: 150px; top: 22px; width: 560px; height: 44px; border-radius: 22px; background: #ffffff;
  box-shadow: inset 0 0 0 1.5px rgba(23,20,28,0.07); }
.pg .url .sk { position: absolute; left: 14px; top: 9px; width: 26px; height: 26px; stroke: rgba(23,20,28,0.4); }
.trail { position: absolute; left: 0; top: 0; fill: none; stroke: rgba(180,18,47,0.55); stroke-width: 6;
  stroke-linecap: round; stroke-dasharray: 2 16; }
.cur { position: absolute; left: -11px; top: -8px; width: 64px; height: 64px; z-index: 6;
  filter: drop-shadow(0 6px 10px rgba(24,4,12,0.35)); }
.ck { position: absolute; width: 120px; height: 120px; margin: -60px 0 0 -60px; border-radius: 50%;
  border: 7px solid #ff6e9c; opacity: 0; visibility: hidden; z-index: 5; }
.heat { position: absolute; width: 400px; height: 400px; margin: -200px 0 0 -200px; border-radius: 50%; z-index: 4;
  background: radial-gradient(circle, rgba(225,32,74,0.80) 0%, rgba(255,110,156,0.55) 34%, rgba(255,110,156,0) 70%);
  mix-blend-mode: multiply; }

/* the prompt bar */
#pb { position: absolute; }
#pbT { position: absolute; left: 44px; top: 30px; width: 780px; font-size: 35px; font-weight: 500; line-height: 1.3;
  color: #fff; white-space: pre-wrap; }
#pbT::after { content: ""; display: inline-block; width: 3px; height: 38px; margin-left: 3px; vertical-align: -6px;
  background: #ff8ab0; }
#pbS { position: absolute; right: 30px; bottom: 30px; width: 84px; height: 84px; }

/* the list Claude gives back */
.lst { position: absolute; border-radius: 52px; overflow: hidden;
  background: linear-gradient(172deg, #ffffff 0%, #fff9fb 55%, #fdf0f4 100%);
  box-shadow: inset 0 2px 1px #fff, 0 50px 100px -36px rgba(24,4,12,0.62); }
.lst i { position: absolute; display: block; }
.cbx { position: absolute; width: 50px; height: 50px; border-radius: 15px;
  box-shadow: inset 0 0 0 4px rgba(23,20,28,0.22); }
.cbf { position: absolute; inset: 0; border-radius: 15px;
  background: linear-gradient(165deg, #e0204b 0%, #8d0d24 100%); opacity: 0; visibility: hidden; }
.cbf svg { position: absolute; left: 7px; top: 7px; width: 36px; height: 36px; fill: none; stroke: #fff;
  stroke-width: 3.2; stroke-linecap: round; stroke-linejoin: round; }
.yes { position: absolute; border-radius: 60px 60px 14px 60px; display: flex; align-items: center; justify-content: center;
  background: linear-gradient(165deg, #e0204b 0%, #ab112e 46%, #6b081c 100%); color: #fff; font-size: 58px; font-weight: 900;
  box-shadow: inset 0 2px 1px rgba(255,255,255,0.5), 0 30px 60px -20px rgba(70,4,20,0.7); }

/* the code diff */
.code { position: absolute; border-radius: 44px; overflow: hidden;
  background: linear-gradient(160deg, #2a1f2a 0%, #17141c 100%);
  box-shadow: inset 0 1.5px 0 rgba(255,255,255,0.16), inset 0 0 0 1px rgba(255,255,255,0.08),
              0 50px 100px -36px rgba(10,0,4,0.75); }
.code .tab { position: absolute; left: 30px; top: 26px; height: 50px; padding: 0 22px; border-radius: 25px;
  background: rgba(255,255,255,0.08); color: rgba(255,255,255,0.78); font-size: 25px; font-weight: 700;
  line-height: 50px; letter-spacing: 0.01em; }
.crow { position: absolute; left: 0; right: 0; height: 44px; transform-origin: 0 50%; }
.crow .gn { position: absolute; left: 30px; top: 6px; width: 40px; text-align: right; font-size: 22px; font-weight: 700;
  color: rgba(255,255,255,0.26); }
.crow .sg { position: absolute; top: 15px; height: 14px; border-radius: 7px; }
.crow.del { background: rgba(225,32,74,0.24); }
.crow.add { background: rgba(255,110,156,0.20); }
.crow.del .gn, .crow.add .gn { color: #fff; }

/* the routine strip */
.day { position: absolute; width: 66px; height: 66px; border-radius: 50%; display: flex; align-items: center;
  justify-content: center; font-size: 26px; font-weight: 700; color: rgba(255,255,255,0.85);
  background: rgba(255,255,255,0.16); box-shadow: inset 0 1.5px 1px rgba(255,255,255,0.5); }
.dayf { position: absolute; inset: 0; border-radius: 50%; display: flex; align-items: center; justify-content: center;
  background: linear-gradient(165deg, #e0204b 0%, #8d0d24 100%); color: #fff;
  box-shadow: inset 0 2px 1px rgba(255,255,255,0.5), 0 0 30px rgba(255,110,156,0.7); opacity: 0; visibility: hidden; }
.arc { fill: none; stroke: #ffd6e3; stroke-width: 7; stroke-linecap: round; filter: drop-shadow(0 0 8px rgba(255,110,156,0.9)); }

/* follow */
.fl { position: absolute; border-radius: 80px; overflow: hidden;
  background: linear-gradient(160deg, #ffffff 0%, #fff5f8 52%, #f5dfe6 100%);
  box-shadow: inset 0 2px 1px #fff, 0 40px 80px -28px rgba(30,4,12,0.65); }
.fl .t { position: absolute; left: 160px; top: 0; height: 150px; line-height: 150px; font-size: 56px; font-weight: 700;
  letter-spacing: -0.02em; color: #17141c; }
.fl .on { position: absolute; inset: 0; background: linear-gradient(165deg, #e0204b 0%, #ab112e 46%, #6b081c 100%);
  opacity: 0; visibility: hidden; }
.fl .on .t { color: #fff; left: 150px; }
.shc { position: absolute; inset: 0; border-radius: inherit; overflow: hidden; pointer-events: none; }
.shc .sheen { mix-blend-mode: normal; opacity: 0.4; }
""")

L = []
BEATS = []


def beat(fn):
    BEATS.append(fn)
    return fn


# ===========================================================================
# A · hook — Claude told me
@beat
def a_notif():
    L.append(
        '<div class="g full" id="gA">'
        '<div class="dglass edge hide" id="nt" style="left:80px;top:150px;width:920px;height:196px">'
        '<div class="tw" style="left:34px;top:46px;width:104px;height:104px"><div class="jelly">%s</div></div>'
        '<div class="app">Claude</div><div class="tm">зараз</div>'
        '<div class="msg">Показуй кожного дня, що&nbsp;ти&nbsp;робиш</div>'
        '<div class="shc"><div class="sheen"></div></div></div></div>' % g.mark("claude"))
    sfx("notification", T["klod"] + 0.18)
    return js("""
  tl.set("#gA", {autoAlpha: 1}, 0);
  tl.fromTo("#nt", {autoAlpha: 0, y: -280, scale: 0.92}, {autoAlpha: 1, y: 0, scale: 1, duration: 0.9, ease: SOFT}, @klod+0.05);
  G.haptic("#nt", @klod+0.62);
  shn("#nt .sheen", @klod+0.5);
  tl.to("#nt", {scale: 0.24, x: -370, y: 150, autoAlpha: 0, duration: 0.42, ease: "power3.in"}, @pokazhu-0.2);
  tl.set("#gA", {autoAlpha: 0}, @pokazhu+0.3);""")


# ===========================================================================
# B · Claude reads the site and rewrites it
@beat
def b_site():
    site = (
        '<div class="site hide" id="site" style="left:604px;top:150px;width:330px;height:430px">'
        '<i class="bar" style="height:54px"></i>'
        '<i class="dot" style="left:24px;top:20px;width:14px;height:14px"></i>'
        '<i class="dot" style="left:46px;top:20px;width:14px;height:14px"></i>'
        '<i class="dot" style="left:68px;top:20px;width:14px;height:14px"></i>'
        '<i class="hb" style="left:28px;top:84px;width:220px;height:34px"></i>'
        '<i class="rr" style="left:28px;top:138px;width:262px;height:16px"></i>'
        '<i class="rr" style="left:28px;top:164px;width:196px;height:16px"></i>'
        '<i class="im" id="sIm" style="left:28px;top:200px;width:274px;height:118px"></i>'
        '<i class="btn" id="sBtn" style="left:28px;top:344px;width:186px;height:56px"></i>'
        '</div>')
    cab = (
        '<svg class="cab abs" width="1080" height="700" viewBox="0 0 1080 700" style="left:0;top:0">'
        '<path class="tube hide" id="bT" d="M376 362 C 460 362 520 372 600 372"/>'
        '<path class="core hide" id="bC" d="M376 362 C 460 362 520 372 600 372"/>'
        '<g class="pkg"><path class="pkt" id="bP1" style="opacity:0" d="M600 372 C 520 372 460 362 376 362"/>'
        '<path class="pkt" id="bP2" style="opacity:0" d="M376 362 C 460 362 520 372 600 372"/></g></svg>')
    L.append('<div class="g full" id="gB">' + cab + site
             + tile("bCl", 220, 150, 252, "jelly", g.mark("claude"))
             + tile("bMt", 140, 418, 118, "pearl", g.mark("meta"))
             + tile("bUp", 64, 528, 96, "jelly", stroke("up"), extra_cls="circ", ring=False)
             + '</div>')
    sfx("whoosh-short", T["pokazhu"] - 0.15)
    sfx("pop", T["analizuie"])
    sfx("whoosh-short", T["dani"] + 0.05, -2)
    sfx("pop", T["tarhet"])
    sfx("click", T["krashche"] + 0.05)
    return js("""
  tl.set("#gB", {autoAlpha: 1}, @pokazhu-0.25);
  arr("#bCl", @pokazhu-0.12, {s: 0.3, x: -30, y: -90});
  G.ripple("#bClR", @pokazhu+0.3);
  arr("#site", @analizuie-0.05, {s: 0.6, x: 40, y: 20});
  tl.set(["#bT", "#bC"], {autoAlpha: 1}, @analizuie+0.1);
  draw2("bT", @analizuie+0.1, 0.45); draw2("bC", @analizuie+0.1, 0.45);
  G.packet("bP1", @dani+0.05, 0.5);
  G.bump("#bCl", @dani+0.55); G.ripple("#bClR", @dani+0.55);
  G.packet("bP2", @zminiuie+0.05, 0.5);
  tl.to("#sBtn", {y: -144, scale: 1.3, transformOrigin: "0% 50%", duration: 0.6, ease: SP}, @zminiuie+0.5);
  tl.to("#sIm", {y: 70, scaleY: 0.6, transformOrigin: "50% 100%", autoAlpha: 0.55, duration: 0.6, ease: SP}, @zminiuie+0.5);
  G.bump("#site", @zminiuie+0.55);
  arr("#bMt", @tarhet-0.05, {s: 0.4, y: 30});
  G.ripple("#bMtR", @tarhet+0.25);
  arr("#bUp", @krashche-0.02, {s: 0.2, y: 20, d: 0.6});
  bout("#gB", @dlia-0.12, 10, 0.28);""")


# ===========================================================================
# C · context: 4 days, ads running, conversion, sign-ups, sales
@beat
def c_context():
    roll = "".join("<i>%s</i>" % n for n in ("7", "6", "5", "4"))
    cal = ('<div class="cal hide" id="cal" style="left:150px;top:160px;width:290px;height:330px">'
           '<div class="hd"></div><div class="hole" style="left:76px"></div><div class="hole" style="left:192px"></div>'
           '<div class="win"><div class="roll" id="calR">%s</div></div><div class="lb">дні</div>'
           '<div class="shc"><div class="sheen"></div></div></div>' % roll)
    live = '<div class="live hide" id="live" style="left:352px;top:450px"><b></b>LIVE</div>'
    spin = ('<svg class="spin hide" id="spin" viewBox="0 0 320 320" width="320" height="320" '
            'style="left:640px;top:166px"><circle cx="160" cy="160" r="146"/></svg>')
    bars = "".join('<div class="bar6%s" id="b6%d" style="left:%dpx;height:%dpx"></div>'
                   % (" hot" if i == 5 else "", i, 56 + i * 124, h)
                   for i, h in enumerate((80, 112, 150, 186, 222, 262)))
    shelf = ('<div class="shelf edge hide" id="shC" style="left:70px;top:150px;width:940px;height:400px">%s'
             '</div>' % bars)
    avat = "".join(tile("cAv%d" % i, 120, 150 + i * 168, 268, "pearl", stroke("person"), extra_cls="circ", ring=False)
                   + tile("cCk%d" % i, 48, 232 + i * 168, 262, "jelly", stroke("check"), extra_cls="circ", ring=False)
                   for i in range(4))
    coin = tile("cEu", 160, 820, 248, "jelly", '<span class="wmark" style="font-size:96px;color:#fff">€</span>',
                extra_cls="circ")
    L.append('<div class="g full" id="gC">' + cal + live
             + tile("cMt", 220, 690, 216, "pearl", g.mark("meta"))
             + spin + shelf
             + tile("cUp", 120, 846, 118, "jelly", stroke("up"), extra_cls="circ")
             + avat + coin + '</div>')
    sfx("pop", T["dlia"] + 0.1)
    sfx("click-soft", T["chotyry"] + 0.02)
    sfx("pop", T["tarhet2"] + 0.02)
    sfx("whoosh-short", T["vazhlyvo"] + 0.05, -2)
    sfx("pop", T["konversiiu"] + 0.02)
    sfx("kaching", T["kupyly"] + 0.02)
    return js("""
  tl.set("#gC", {autoAlpha: 1}, @dlia-0.05);
  arr("#cal", @dlia+0.05, {s: 0.5});
  tl.fromTo("#calR", {y: 0}, {y: -510, duration: 0.7, ease: "power3.inOut"}, @chotyry-0.62);
  G.bump("#cal", @chotyry+0.08); shn("#cal .sheen", @dni);
  arr("#live", @vebinar-0.02, {s: 0.4, y: 20, d: 0.6});
  arr("#cMt", @tarhet2-0.05, {s: 0.4});
  G.ripple("#cMtR", @tarhet2+0.3);
  tl.fromTo("#spin", {autoAlpha: 0, rotation: 0, scale: 0.85, transformOrigin: "50% 50%"},
            {autoAlpha: 1, scale: 1, duration: 0.3, ease: "power2.out"}, @krutytsia-0.05);
  tl.to("#spin", {rotation: 300, duration: 1.15, ease: "power2.inOut"}, @krutytsia-0.05);
  bout(["#cal", "#live", "#cMt", "#spin"], @vazhlyvo-0.1, 10, 0.28);
  arr("#shC", @vazhlyvo+0.05, {s: 0.8, y: 30});
  tl.fromTo("#shC .bar6", {scaleY: 0.12}, {scaleY: 1, duration: 0.85, ease: SP, stagger: 0.07}, @pidvyshchyty-0.05);
  arr("#cUp", @konversiiu-0.05, {s: 0.3, y: 40});
  G.ripple("#cUpR", @konversiiu+0.3);
  bout(["#shC", "#cUp"], @liudei-0.3, 10, 0.25);
  [0, 1, 2, 3].forEach(function (i) { arr("#cAv" + i, @liudei-0.05 + i * 0.1, {s: 0.4, y: 40, d: 0.7}); });
  [0, 1, 2, 3].forEach(function (i) { arr("#cCk" + i, @zareiestr+0.35 + i * 0.09, {s: 0.2, y: 0, d: 0.5}); });
  arr("#cEu", @kupyly-0.04, {s: 0.3, y: 30, d: 0.7});
  G.ripple("#cEuR", @kupyly+0.25);
  shn("#cEu .sheen", @kupyly+0.2);
  tl.set("#gC", {autoAlpha: 0}, @na+0.6);""")


# ===========================================================================
# TK · the iris opens out of the coin: two analytics, then her page in Clarity
PTS = [(150, 300), (560, 360), (300, 540), (650, 640), (430, 760)]
SEGS = [(0, 1, "rukhaiutsia", -0.3, 0.75), (1, 2, "rukhaiutsia", 0.45, 0.75),
        (2, 3, "klikaiut", -0.25, 0.3), (3, 4, "halmuiut", -0.18, 0.4)]
BTN0 = (200, 900, 460, 104)          # x, y, w, h inside the page, before the rearrange
BTN_DY = -430


@beat
def t_takeover():
    trail = "".join('<path class="trail hide" id="tr%d" d="M%d %d L%d %d"/>'
                    % (i, PTS[a][0], PTS[a][1], PTS[b][0], PTS[b][1]) for i, (a, b, _, _, _) in enumerate(SEGS))
    page = (
        '<div class="pg hide" id="pg" style="left:110px;top:110px;width:860px;height:1060px">'
        '<i class="bar" style="height:88px"></i>'
        '<i class="dot" style="left:38px;top:36px;width:17px;height:17px"></i>'
        '<i class="dot" style="left:66px;top:36px;width:17px;height:17px"></i>'
        '<i class="dot" style="left:94px;top:36px;width:17px;height:17px"></i>'
        '<i class="url">%s</i>'
        '<i class="hb" style="left:60px;top:150px;width:600px;height:58px;border-radius:16px"></i>'
        '<i class="hb" style="left:60px;top:224px;width:420px;height:58px;border-radius:16px"></i>'
        '<i class="rr pgr" style="left:60px;top:318px;width:690px;height:24px;border-radius:12px"></i>'
        '<i class="rr pgr" style="left:60px;top:358px;width:610px;height:24px;border-radius:12px"></i>'
        '<i class="im" id="pgIm" style="left:60px;top:430px;width:740px;height:330px;border-radius:34px"></i>'
        '<i class="rr pgr2" style="left:60px;top:800px;width:700px;height:24px;border-radius:12px"></i>'
        '<i class="rr pgr2" style="left:60px;top:840px;width:520px;height:24px;border-radius:12px"></i>'
        '<i class="btn" id="pgBtn" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx;font-size:42px">Зареєструватися</i>'
        '<svg class="abs" width="860" height="1060" style="left:0;top:0;overflow:visible">%s</svg>'
        '<div class="heat hide" id="heat" style="left:%dpx;top:%dpx"></div>'
        '<div class="ck" id="ck1" style="left:%dpx;top:%dpx"></div>'
        '<div class="ck" id="ck2" style="left:%dpx;top:%dpx"></div>'
        '<div class="ck" id="ck3" style="left:%dpx;top:%dpx"></div>'
        '<div class="cur hide" id="cur">%s</div>'
        '</div>' % ((stroke("lock"),) + BTN0 + (trail, PTS[4][0], PTS[4][1], PTS[2][0], PTS[2][1],
                                                 PTS[3][0], PTS[3][1],
                                                 BTN0[0] + BTN0[2] // 2, BTN0[1] + BTN_DY + BTN0[3] // 2, CURSOR)))
    ghost_ga = '<div class="clear">%s</div>' % g.mark("googleanalytics")
    ghost_cl = '<div class="clear">%s</div>' % clarity_mark(62)
    L.append(
        '<div class="g full" id="gT"><div class="tkg"></div><div class="aurs"></div><div class="grain"></div>'
        '<div class="tw hide" id="sGA" style="left:50px;top:520px;width:300px;height:300px">%s</div>'
        '<div class="tw hide" id="sCL" style="left:730px;top:520px;width:300px;height:300px">%s</div>'
        % (ghost_ga, ghost_cl)
        + tile("tGA", 300, 50, 520, "pearl", g.mark("googleanalytics"))
        + '<div class="io hide" id="ioIn" style="left:30px;top:700px">%s</div>' % stroke("in")
        + '<div class="io hide" id="ioOut" style="left:192px;top:700px">%s</div>' % stroke("out")
        + page
        + tile("tCL", 300, 730, 520, "jelly", clarity_mark(62))
        + '</div>')
    sfx("whoosh-short", T["na"] - 0.05)
    sfx("pop", T["na"] + 0.65, -3)
    sfx("click-soft", T["google"] + 0.05)
    sfx("click-soft", T["clarity1"] + 0.05)
    sfx("ping", T["tsikavisha"] + 0.05, -3)
    sfx("click-soft", T["zaishlo"] + 0.02, -2)
    sfx("whoosh-short", T["pokazuie"] + 0.05)
    sfx("click", T["kudy"] + 0.25)
    sfx("click", T["klikaiut"] + 0.17)
    sfx("click", T["tytsnula"] + 0.02)

    # cursor and trail, segment by segment, in sync
    seg_js = []
    for i, (a, b, word, off, d) in enumerate(SEGS):
        t0 = T[word] + off
        seg_js.append('  tl.set("#tr%d", {autoAlpha: 1}, %.3f); draw2("tr%d", %.3f, %.2f);'
                      % (i, t0, i, t0, d))
        seg_js.append('  tl.to("#cur", {x: %d, y: %d, duration: %.2f, ease: "power1.inOut"}, %.3f);'
                      % (PTS[b][0], PTS[b][1], d, t0))
    bx, by = BTN0[0] + BTN0[2] // 2 + 40, BTN0[1] + BTN_DY + BTN0[3] // 2 + 10
    out = js("""
  G.irisOpen("#gT", @na-0.08, 925, 355, 0.6);
  drift1("#gT", @na, @zareiestr2e-@na);
  arr(["#sGA", "#sCL"], @dvi-0.1, {s: 0.6, y: 30});
  tl.set("#sGA", {autoAlpha: 0}, @google+0.3);
  arr("#tGA", @google-0.02, {s: 0.85, y: 0, d: 0.6, blur: 8}); G.ripple("#tGAR", @google+0.2);
  tl.set("#sCL", {autoAlpha: 0}, @clarity1+0.3);
  arr("#tCL", @clarity1-0.02, {s: 0.85, y: 0, d: 0.6, blur: 8}); G.ripple("#tCLR", @clarity1+0.2);
  /* Clarity wins: it swings in behind her head, GA shrinks off to the side */
  tl.to("#tGA", {scale: 0.62, x: -40, y: -90, autoAlpha: 0.5, duration: 0.55, ease: SP}, @clarity2+0.05);
  tl.to("#tCL", {x: -340, y: -30, scale: 1.85, duration: 0.8, ease: SP}, @tsikavisha-0.15);
  shn("#tCL .sheen", @tsikavisha+0.3);
  tl.to("#tGA", {autoAlpha: 1, duration: 0.3}, @rakhuie-0.1);
  arr("#ioIn", @zaishlo-0.05, {s: 0.4, y: 20, d: 0.55});
  arr("#ioOut", @vyishlo-0.05, {s: 0.4, y: 20, d: 0.55});
  tl.fromTo("#ioIn .sk", {x: -10}, {x: 6, duration: 0.5, ease: SP, immediateRender: false}, @zaishlo+0.2);
  tl.fromTo("#ioOut .sk", {x: -6}, {x: 10, duration: 0.5, ease: SP, immediateRender: false}, @vyishlo+0.2);
  bout(["#tGA", "#ioIn", "#ioOut"], @pokazuie-0.05, 10, 0.3);
  /* Clarity becomes the page's logo, the page grows out of it */
  tl.to("#tCL", {x: 25, y: -516, scale: 0.31, duration: 0.7, ease: SP}, @pokazuie);
  gsap.set("#pg", {transformOrigin: "430px 530px"});
  arr("#pg", @pokazuie+0.08, {s: 0.25, y: 0, d: 0.9});
  /* she steps out as the page takes the frame */
  tl.to("#matte-tk", {autoAlpha: 0, duration: 0.35, ease: "power2.in"}, @pokazuie+0.12);
  tl.set("#cur", {x: {{x0}}, y: {{y0}}}, 0);
  bin("#cur", @rukhaiutsia-0.45, 6, 0.25);
{{segs}}
  tl.fromTo("#ck1", {scale: 0.3, autoAlpha: 0.95}, {scale: 1.5, autoAlpha: 0, duration: 0.55, ease: "power2.out", immediateRender: false}, @kudy+0.25);
  tl.fromTo("#ck2", {scale: 0.3, autoAlpha: 0.95}, {scale: 1.5, autoAlpha: 0, duration: 0.55, ease: "power2.out", immediateRender: false}, @klikaiut+0.17);
  tl.fromTo("#heat", {autoAlpha: 0, scale: 0.2}, {autoAlpha: 1, scale: 1, duration: 0.9, ease: "power2.out"}, @halmuiut+0.25);
  bout(["#heat", "#tr0", "#tr1", "#tr2", "#tr3"], @osnovi, 6, 0.4);
  /* the page is rearranged: the button comes up to where people are */
  tl.to("#pgIm", {y: 330, scale: 0.62, transformOrigin: "50% 0%", autoAlpha: 0.7, duration: 0.7, ease: SP}, @pidlasht);
  tl.to(".pgr2", {autoAlpha: 0, duration: 0.25}, @pidlasht);
  tl.to("#pgBtn", {y: {{dy}}, scale: 1.12, duration: 0.8, ease: SP}, @pidlasht+0.08);
  tl.to("#cur", {x: {{bx}}, y: {{by}}, duration: 0.85, ease: "power2.inOut"}, @tytsnula-0.95);
  tl.to("#pgBtn", {scale: 1.02, duration: 0.09, ease: "power2.out"}, @tytsnula);
  tl.to("#pgBtn", {scale: 1.12, duration: 0.45, ease: SP}, @tytsnula+0.09);
  tl.to("#cur", {scale: 0.86, duration: 0.09}, @tytsnula); tl.to("#cur", {scale: 1, duration: 0.3}, @tytsnula+0.09);
  tl.fromTo("#ck3", {scale: 0.4, autoAlpha: 0.95}, {scale: 2.1, autoAlpha: 0, duration: 0.7, ease: "power2.out", immediateRender: false}, @tytsnula+0.02);
  G.irisClose("#gT", @zareiestr2e-0.42, 260, 280, 0.55);""",
              x0=PTS[0][0], y0=PTS[0][1])
    for key, v in {"x0": PTS[0][0], "y0": PTS[0][1], "segs": "\n".join(seg_js),
                   "dy": BTN_DY, "bx": bx, "by": by}.items():
        out = out.replace("{{%s}}" % key, str(v))
    return out


# ===========================================================================
# D · connector, the prompt
PROMPT = (u"Зайди на сайт, проаналізуй поточний стан, скажи, яка зараз "
          u"конверсія, і дай список того, що можна покращити")


@beat
def d_connector():
    cab = ('<svg class="cab abs" width="1080" height="700" viewBox="0 0 1080 700" style="left:0;top:0">'
           '<path class="tube hide" id="dT" d="M372 280 C 470 236 620 236 718 280"/>'
           '<path class="core hide" id="dC" d="M372 280 C 470 236 620 236 718 280"/>'
           '<g class="pkg"><path class="pkt" id="dP" style="opacity:0" d="M372 280 C 470 236 620 236 718 280"/></g></svg>')
    bar = ('<div class="dglass edge hide" id="pb" style="left:60px;top:430px;width:960px;height:210px;border-radius:52px">'
           '<div id="pbT"></div>'
           '<div class="tw circ" id="pbS" style="right:30px;bottom:30px;left:auto;top:auto"><div class="jelly">%s</div></div>'
           '</div>' % stroke("up"))
    L.append('<div class="g full" id="gD">' + cab
             + tile("dCL", 220, 150, 170, "jelly", clarity_mark(46))
             + tile("dCd", 220, 720, 170, "jelly", g.mark("claude"))
             + bar + '</div>')
    sfx("click-soft", T["konektor"] + 0.1)
    sfx("pop", T["klodi"] + 0.02)
    sfx("typing", T["zaidy"] + 0.05, -1)
    sfx("click", T["pokrashchytye"] - 0.15)
    return js("""
  tl.set("#gD", {autoAlpha: 1}, @zareiestr2e-0.45);
  arr("#dCL", @zareiestr2e-0.38, {s: 0.55, y: 0, d: 0.7});
  tl.set(["#dT", "#dC"], {autoAlpha: 1}, @konektor-0.1);
  draw2("dT", @konektor-0.1, 0.5); draw2("dC", @konektor-0.1, 0.5);
  arr("#dCd", @klodi-0.05, {s: 0.4, y: 20});
  G.ripple("#dCdR", @klodi+0.25);
  G.packet("dP", @klodi+0.35, 0.5);
  arr("#pb", @proshu-0.3, {s: 0.85, y: 40, d: 0.7});
  G.bump("#pbS", @pokrashchytye-0.15);
  tl.to("#pb", {y: -60, autoAlpha: 0, duration: 0.32, ease: "power2.in"}, @pokrashchytye-0.02);
  bout(["#dCL", "#dCd", "#dT", "#dC"], @pokrashchytye, 10, 0.28);
  tl.set("#gD", {autoAlpha: 0}, @dali);""")


# ===========================================================================
# E · the list she checks, «так»
@beat
def e_list():
    rows = ""
    for i, w in enumerate((440, 372, 476, 318)):
        y = 132 + i * 80
        rows += ('<div class="cbx" style="left:44px;top:%dpx"><div class="cbf" id="cb%d">'
                 '<svg viewBox="0 0 24 24"><path id="cbp%d" d="M5.4 12.6l4.3 4.3 8.9-9.5"/></svg></div></div>'
                 '<i class="rr" style="left:122px;top:%dpx;width:%dpx;height:24px;border-radius:12px"></i>'
                 % (y, i, i, y + 13, w))
    lst = ('<div class="lst hide" id="lst" style="left:150px;top:140px;width:780px;height:470px">'
           '<div class="tw" style="left:40px;top:34px;width:62px;height:62px"><div class="jelly">%s</div></div>'
           '<i class="hb" style="left:122px;top:50px;width:300px;height:30px"></i>%s'
           '<div class="shc"><div class="sheen"></div></div></div>' % (g.mark("claude"), rows))
    L.append('<div class="g full" id="gE">' + lst
             + '<div class="yes hide" id="yes" style="left:704px;top:540px;width:230px;height:126px">Так</div></div>')
    for key in ("pereghl", "pereviriaiu", "lohichno", "podob"):
        sfx("click-soft", T[key] + 0.25, -1)
    sfx("pop", T["tak"])
    return js("""
  tl.set("#gE", {autoAlpha: 1}, @dali-0.1);
  arr("#lst", @dali-0.05, {s: 0.7, y: 40});
  shn("#lst .sheen", @dali+0.3);
  [["#cb0", @pereghl+0.25], ["#cb1", @pereviriaiu+0.25], ["#cb2", @lohichno+0.25], ["#cb3", @podob+0.25]].forEach(function (p, i) {
    tl.fromTo(p[0], {autoAlpha: 0, scale: 0.4}, {autoAlpha: 1, scale: 1, duration: 0.4, ease: POP}, p[1]);
    draw2("cbp" + i, p[1] + 0.06, 0.3);
  });
  arr("#yes", @tak-0.04, {s: 0.3, x: 30, y: 30, d: 0.7});
  bout("#gE", @vin-0.05, 10, 0.26);""")


# ===========================================================================
# F · the code diff
@beat
def f_code():
    def row(i, y, cls, sign, spans):
        s = "".join('<i class="sg" style="left:%dpx;width:%dpx;background:%s"></i>' % (x, w, c) for x, w, c in spans)
        return ('<div class="crow %s" id="cr%s" style="top:%dpx"><span class="gn">%s</span>%s</div>'
                % (cls, i, y, sign, s))
    P, W_, D_ = "#ff8ab0", "rgba(255,255,255,0.5)", "rgba(255,255,255,0.22)"
    base = [
        [(96, 90, P), (200, 220, W_)], [(126, 160, D_), (300, 120, P)], [(126, 300, W_)],
        [(126, 240, W_), (380, 90, P)], [(96, 120, P)], [(126, 380, W_)], [(96, 90, P), (200, 160, D_)],
    ]
    rows = ""
    for i, sp in enumerate(base):
        rows += row(str(i), 104 + i * 46, "", str(i + 1), sp)
    adds = [[(126, 130, P), (270, 260, W_)], [(156, 330, P)], [(126, 210, W_), (350, 120, P)]]
    for j, sp in enumerate(adds):
        rows += row("a%d" % j, 104 + (2 + j) * 46, "add hide", "+", sp)
    card = ('<div class="code hide" id="code" style="left:90px;top:120px;width:900px;height:500px">'
            '<div class="tab">index.html</div>%s</div>' % rows)
    L.append('<div class="g full" id="gF">' + card + '</div>')
    sfx("whoosh-short", T["vin"] + 0.02, -1)
    sfx("typing", T["vnosyt"] + 0.05, -2)
    return js("""
  tl.set("#gF", {autoAlpha: 1}, @vin-0.05);
  arr("#code", @vin+0.02, {s: 0.75, y: 40, d: 0.75});
  tl.set(["#cr2", "#cr3"], {className: "crow del"}, @vnosyt);
  tl.to(["#cr2", "#cr3"], {scaleY: 0, autoAlpha: 0, duration: 0.3, ease: "power2.in"}, @vnosyt+0.25);
  tl.to(["#cr4", "#cr5", "#cr6"], {y: 46, duration: 0.45, ease: SP}, @vnosyt+0.45);
  tl.fromTo(["#cra0", "#cra1", "#cra2"], {autoAlpha: 0, scaleY: 0.2}, {autoAlpha: 1, scaleY: 1, duration: 0.4, ease: POP, stagger: 0.12}, @vnosyt+0.5);
  bout("#gF", {{npaint}}, 10, 0.26);""").replace("{{npaint}}", "%.3f" % (NO_PAINT[0][0] - 0.32))


# ===========================================================================
# G · the routine — every third day
DAYS = 10
DX0, DSTEP, DY = 51, 86, 186


@beat
def g_routine():
    cells = ""
    for i in range(DAYS):
        cells += ('<div class="day" style="left:%dpx;top:%dpx">%d<div class="dayf" id="dy%d">%d</div></div>'
                  % (DX0 + i * DSTEP, DY, i + 1, i, i + 1))
    arcs = ""
    for n, i in enumerate((0, 3, 6)):
        x0 = DX0 + i * DSTEP + 33
        x1 = DX0 + (i + 3) * DSTEP + 33
        arcs += '<path class="arc" id="ar%d" style="opacity:0" d="M%d %d Q %d %d %d %d"/>' % (
            n, x0, DY - 8, (x0 + x1) // 2, DY - 150, x1, DY - 8)
    shelf = ('<div class="shelf edge hide" id="rt" style="left:70px;top:210px;width:940px;height:320px">'
             '<svg class="abs" width="940" height="320" style="left:0;top:0;overflow:visible">%s</svg>%s</div>'
             % (arcs, cells))
    L.append('<div class="g full" id="gG">' + shelf
             + tile("rtC", 104, 488, 150, "jelly", g.mark("claude")) + '</div>')
    sfx("pop", T["vidbuv"] - 0.1, -2)
    sfx("pop", T["rutynu"] + 0.05, -3)
    return js("""
  tl.set("#gG", {autoAlpha: 1}, @vidbuv-0.2);
  arr("#rt", @vidbuv-0.12, {s: 0.8, y: 40});
  arr("#rtC", @avtom-0.05, {s: 0.3, y: 30, d: 0.7}); G.ripple("#rtCR", @avtom+0.25);
  function lite(i, t) { tl.fromTo("#dy" + i, {autoAlpha: 0, scale: 0.4}, {autoAlpha: 1, scale: 1, duration: 0.45, ease: POP}, t); }
  lite(0, @rutynu+0.05);
  [[0, @povtor+0.15], [1, @kozhni+0.1], [2, @dni3+0.2]].forEach(function (p) {
    tl.set("#ar" + p[0], {opacity: 1}, p[1]); draw2("ar" + p[0], p[1], 0.42); lite(p[0] * 3 + 3, p[1] + 0.38);
  });
  G.bump("#rtC", @robyt);
  bout("#gG", @yakshcho-0.15, 10, 0.26);""")


# ===========================================================================
# H · Стежити
@beat
def h_follow():
    L.append('<div class="g full" id="gH"><div class="fl hide" id="fl" style="left:190px;top:300px;width:700px;height:150px">'
             '<div class="tw circ" style="left:28px;top:27px;width:96px;height:96px"><div class="jelly">%s</div></div>'
             '<div class="t" id="flT">Стежити</div>'
             '<div class="on" id="flOn"><div class="tw circ" style="left:28px;top:27px;width:96px;height:96px">'
             '<div class="pearl">%s</div></div><div class="t">Ви стежите</div></div>'
             '<div class="ck" id="ck4" style="left:470px;top:75px"></div>'
             '<div class="shc"><div class="sheen"></div></div></div></div>'
             % (g.mark("instagram"), stroke("check")))
    sfx("pop", T["yakshcho"] + 0.02, -2)
    sfx("click", T["pidpysh"] + 0.02)
    return js("""
  tl.set("#gH", {autoAlpha: 1}, @yakshcho-0.1);
  arr("#fl", @yakshcho-0.02, {s: 0.6, y: 40});
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


def typing_js():
    """The prompt types itself, driven from one clock so any frame renders cold."""
    t0, t1 = T["zaidy"] + 0.02, T["pokrashchytye"] - 0.3
    return r"""
  var CLK = {t: 0}, PB = document.getElementById("pbT"), PTXT = %s, PCUR = null;
  function paintAll() {
    var t = CLK.t, n = t <= %.3f ? 0 : t >= %.3f ? PTXT.length : Math.round(PTXT.length * (t - %.3f) / %.3f);
    if (n !== PCUR) { PCUR = n; PB.textContent = PTXT.slice(0, n); }
  }
  tl.fromTo(CLK, {t: 0}, {t: %.3f, duration: %.3f, ease: "none", onUpdate: paintAll}, 0);""" % (
        json.dumps(PROMPT, ensure_ascii=False), t0, t1, t0, t1 - t0, DUR, DUR)


# captions that would repeat the graphic's own words (STYLE.md §2b.1)
def span_words(a, b):
    return (round(a - 0.02, 3), round(b, 3), "")


BLACKOUT = [
    span_words(0.0, T["pokazhu"] - 0.05),                       # the notification says it
    span_words(T["zareiestr2"], T["zareiestr2e"]),              # the button says it
    span_words(T["zaidy"], T["pokrashchytye"] + 0.2),           # the prompt types it
    span_words(T["tak"], T["tak"] + 0.35),                      # the bubble says «Так»
    span_words(T["chotyry"], E(u"дні", 11.48)),                 # the calendar says «4 дні»
]


def check_no_paint():
    """No beat may be on screen inside a closeup."""
    a, b = NO_PAINT[0]
    assert T["vnosyt"] + 1.2 < a, "code diff runs into the closeup"
    assert T["vidbuv"] - 0.2 > b, "routine arrives inside the closeup"


# her, cut out (GitHub Actions, .github/workflows/matte.yml on asr-inbox) over
# the takeover ground — her note on v1: "could have been a mask behind me OR
# greenscreened me in … the middle is all empty"
k.matte("tk", 549 / 30.0, 307 / 30.0)


def main():
    check_no_paint()
    gj = []
    for fn in BEATS:
        j = fn()
        gj.append("  /* %s */" % fn.__name__)
        gj.append(j.rstrip())
    push = ["#vid"]
    head = [g.js(), HEAD_JS, typing_js(),
            '  gsap.set(%s, {transformOrigin: "540px 900px"});' % json.dumps(push),
            '  tl.fromTo(%s, {scale: 1}, {scale: 1.045, duration: %.3f, ease: "none"}, 0);' % (json.dumps(push), DUR)]
    doc = k.document(
        title=u"Reel 21 — Clarity + Claude",
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
