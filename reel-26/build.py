# -*- coding: utf-8 -*-
"""Reel 26 — «Тебе теж бомбить це питання». Posts 2026-10-09.

Opinion / explainer: ChatGPT or Claude? Honest answer — not a big difference;
ChatGPT went toward an agent that acts for you, Claude built an ecosystem of
products around itself; she picked Claude (Claude Design, a sync niggle in
ChatGPT); the real point is to learn one, not chase «the best». Refined glass
(STYLE.md §0), not too heavy: near beats with two burgundy takeovers.

Chain:  near: her real Threads post (screenshot), a highlighter reads along -> it folds into two tiles on a
seesaw that settles level («≈») -> the seesaw drops away, ChatGPT gets an AGI
badge and its cursor ticks a task list and presses send by itself -> Claude
lands, the iris opens out of it: Claude is the hub, six product tiles snap into
orbit -> the iris closes onto the Claude tile: ChatGPT · you · Claude, both
move closer, she picks Claude (tick) -> Claude opens into Claude Design, three
small artboards, tick -> the window shrinks, «›» integrated Figma (Claude
plugged in) -> ChatGPT on a laptop and in the cloud, the sync breaks (×), the
whole thing shrinks («дрібниця»), a code tile (vibe-coding), × turns into ?
-> her closeup (left clear) -> two platforms, she hops across and back, × on
the hop -> the iris opens out of her: any AI, the sliders tune to her, then a
checklist of learning it, and the «кращий» badge she won't chase, struck
through -> the iris closes onto Claude: tick, heart, bulb, the ecosystem ring
again -> Стежити.

usage: python build.py   (then: python ../tools/sfx.py mix 26)
"""
import io
import json
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))
from kit import Kit  # noqa: E402
from glass import Glass  # noqa: E402

CUT = json.load(io.open(os.path.join(ROOT, "work", "r26", "cut.json"), encoding="utf-8"))
DUR = 57.817           # set from the plate's frame count after cut.py --render
FPS = 30
k = Kit(width=1080, height=1920, fps=FPS, duration=DUR)
g = Glass(["openai", "claude", "figma", "threads", "googlechrome", "googlegemini", "instagram"])
k.css(g.css())

# ---------------------------------------------------------------------------
# NO-PAINT: the closeup cut.py made («але мені це не сподобалось»). Captions only.
NO_PAINT = [tuple(x) for x in CUT["no_paint"]]

CAPS = k.load_captions(os.path.join(ROOT, "work", "r26", "captions.json"))
# whisper errors kept as "her wording" by the aligner -> the script word
FIX = {u"IGI,": u"AGI,", u"дій": u"дії", u"застосунками": u"застосунком", u"хмару": u"і хмарою,",
       u"переструйовувати": u"перестрибувати", u"телеп": u"інтелект"}
for c in CAPS:
    c["w"] = FIX.get(c["w"], c["w"])
# «який «кращий».» is one token; the badge says only «кращий», so split it and
# black out just that word.
for i, c in enumerate(CAPS):
    if c["w"] == u"який «кращий».":
        s, e = c["s"], c["e"]
        CAPS[i:i + 1] = [{"w": u"який", "s": s, "e": s + 0.21, "src": "split"},
                         {"w": u"«кращий».", "s": round(s + 0.25, 3), "e": e, "src": "split"}]
        break
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
    "chesno": S(u"Чесно", 4.96), "riznytsi": S(u"різниці", 5.66), "velykoi": S(u"великої", 6.12),
    "nemaie": S(u"немає", 6.72), "gpt2": S("ChatGPT", 7.52), "agi": S("AGI", 9.00), "agie": E("AGI", 9.00),
    "tobto": S(u"тобто", 9.57), "yakyi": S(u"який", 10.26), "sam": S(u"сам", 10.59),
    "vykonuie": S(u"виконує", 10.69), "dii": S(u"дії", 11.11), "tebe": S(u"тебе", 11.53),
    "a3": S(u"а", 12.05), "claude3": S("Claude", 12.21), "ekosys": S(u"екосистему", 12.99),
    "produktiv": S(u"продуктів", 13.61), "navkolo": S(u"навколо", 14.13), "sebe": S(u"себе", 14.63),
    "tut": S(u"тут", 15.15), "pytannia": S(u"питання", 15.49), "blyzhche": S(u"ближче", 16.61),
    "ya": S(u"Я", 17.06), "obrala": S(u"обрала", 17.54), "claude4": S("Claude", 17.98),
    "u": S(u"У", 18.40), "dyzain": S(u"Claude-дизайн", 18.82), "dyzaine": E(u"Claude-дизайн", 18.82),
    "lehenkykh": S(u"легеньких", 20.24), "dyzainer": S(u"дизайнерських", 20.72),
    "potreb": S(u"потреб", 21.30), "vystachaie": S(u"вистачає", 22.13), "holovoiu": S(u"головою", 22.80),
    "tse": S(u"це", 23.47), "zruchnishe": S(u"зручніше", 24.09), "nizh": S(u"ніж", 25.27),
    "intehr": S(u"інтегрована", 25.91), "fihma": S(u"фігма", 26.56), "fihmae": E(u"фігма", 26.56),
    "shche": S(u"Ще", 27.26), "gpt3": S("ChatGPT", 28.20), "ne_s": S(u"не", 28.74),
    "syncro": S(u"синхронізується", 29.00), "chat": S(u"чат", 29.84), "lokal": S(u"локальним", 30.24),
    "khmaroiu": S(u"хмарою", 31.26), "dribn": S(u"дрібниця", 31.94), "vazhlyva": S(u"важлива", 32.46),
    "vaib": S(u"вайбкодить", 33.38), "mozhlyvo": S(u"можливо", 33.94), "vypravyly": S(u"виправили", 34.92),
    "ale2": S(u"Але", 37.21), "yakshcho": S(u"якщо", 37.95), "osobl": S(u"особливого", 38.83),
    "perestryb": S(u"перестрибувати", 39.93), "platformy": S(u"платформи", 40.97),
    "nemaie2": S(u"немає", 41.97),
    "bud": S(u"Будь", 42.70), "shtuchnyi": S(u"штучний", 43.04), "nalasht": S(u"налаштовується", 43.70),
    "pid": S(u"під", 44.36), "holovne": S(u"головне", 44.97), "rozibr": S(u"розібратись", 45.27),
    "nomu": S(u"ньому", 46.15), "a5": S(u"а", 46.73), "haniatys": S(u"ганятись", 46.95),
    "tym": S(u"тим", 47.55), "krashchyi": S(u"кращий", 48.06), "krashchyie": E(u"кращий", 48.06),
    "ya2": S(u"Я", 48.56), "obrala2": S(u"обрала", 49.23), "claude5": S("Claude", 49.61),
    "podob": S(u"подобається", 51.09), "model": S(u"модель", 52.03), "rozumna": S(u"розумна", 52.74),
    "zruchno": S(u"зручно", 53.64), "ekosys2": S(u"екосистемі", 54.26), "ekosys2e": E(u"екосистемі", 54.26),
    "yakshcho2": S(u"Якщо", 55.21), "korysno": S(u"корисно", 55.84), "pidpysh": S(u"підпишись", 57.13),
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
# Sound design (tools/sfx.py). Quiet, on the event, never on her closeup.
SFX = []


def sfx(name, t, db=0):
    if isinstance(t, str):
        t = float(js(t))
    SFX.append({"t": round(max(0.0, t), 3), "name": name, "db": db})


# ---------------------------------------------------------------------------
# Glyphs (24-grid strokes)
STROKES = {
    "check": '<path d="M5.4 12.6l4.3 4.3 8.9-9.5"/>',
    "x": '<path d="M7 7l10 10M17 7L7 17"/>',
    "q": '<path d="M9.1 9.3a3 3 0 1 1 4.3 2.7c-.9.45-1.4 1.1-1.4 2.1v.5"/><path d="M12 18.2v.1"/>',
    "person": '<circle cx="12" cy="8.2" r="3.6"/><path d="M4.8 20c.9-3.8 3.7-5.8 7.2-5.8s6.3 2 7.2 5.8"/>',
    "heart": '<path d="M12 19.6s-7.4-4.4-7.4-9.6A4.1 4.1 0 0 1 12 7.6a4.1 4.1 0 0 1 7.4 2.4c0 5.2-7.4 9.6-7.4 9.6z"/>',
    "bubble": '<path d="M20 11.6a7.9 7.9 0 0 1-11.6 7L4 20l1.4-4.2A7.9 7.9 0 1 1 20 11.6z"/>',
    "repost": '<path d="M7 7h9.5A2.5 2.5 0 0 1 19 9.5V12M17 17H7.5A2.5 2.5 0 0 1 5 14.5V12M14.5 4.5L17 7l-2.5 2.5M9.5 19.5L7 17l2.5-2.5"/>',
    "send": '<path d="M20.5 3.5L10.2 13.8M20.5 3.5l-6.4 17-3.9-6.7-6.7-3.9z"/>',
    "code": '<path d="M8.5 7.5L4 12l4.5 4.5M15.5 7.5L20 12l-4.5 4.5M13.4 5.5l-2.8 13"/>',
    "pen": '<path d="M12 3.6l5.8 8.6L12 20.4l-5.8-8.2z"/><path d="M12 3.6v7.2"/><circle cx="12" cy="12.4" r="1.6"/>',
    "grid": '<rect x="4" y="5" width="16" height="14" rx="2.6"/><path d="M4 10h16M4 14.5h16M10 5v14"/>',
    "folder": '<path d="M3.8 7.6a2 2 0 0 1 2-2h3.6l2 2.2h6.8a2 2 0 0 1 2 2v7.6a2 2 0 0 1-2 2H5.8a2 2 0 0 1-2-2z"/>',
    "monitor": '<rect x="3.5" y="4.5" width="17" height="11.5" rx="2.2"/><path d="M9 20h6M12 16v4"/>',
    "laptop": '<rect x="5" y="5.2" width="14" height="9.8" rx="1.8"/><path d="M2.6 17.6l1.4 1.8h16l1.4-1.8z"/>',
    "cloud": '<path d="M7.2 18.5h10a3.8 3.8 0 0 0 .6-7.6 5.6 5.6 0 0 0-10.9 1.2 3.2 3.2 0 0 0 .3 6.4z"/>',
    "sync": '<path d="M19 12a7 7 0 0 1-12.2 4.7M5 12a7 7 0 0 1 12.2-4.7M17.6 3.8v3.6H14M6.4 20.2v-3.6H10"/>',
    "bulb": '<path d="M9.3 17.6h5.4M10.2 20.6h3.6M12 3.4a5.8 5.8 0 0 0-3.4 10.5c.6.5 1 1.2 1 2v1.7h4.8v-1.7c0-.8.4-1.5 1-2A5.8 5.8 0 0 0 12 3.4z"/>',
    "crown": '<path d="M4.2 17.6L3.2 8l5 3.8L12 5.4l3.8 6.4 5-3.8-1 9.6z"/>',
    "arrow": '<path d="M5 12h13M13 6.5l5.5 5.5-5.5 5.5"/>',
    "rect": '<rect x="5" y="5" width="14" height="14" rx="3"/>',
    "text": '<path d="M6 6.5h12M12 6.5v12"/>',
    "pointer": '<path d="M6 4.5l12 6.6-5.2 1.3-2.6 5.1z"/>',
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


def badge(tid, size, x, y, material, glyph):
    return tile(tid, size, x, y, material, stroke(glyph), extra_cls="circ", ring=False)


# the six Claude products (labels so every tile is nameable)
PRODUCTS = [("code", "Code"), ("pen", "Design"), ("@googlechrome", "Chrome"),
            ("grid", "Excel"), ("folder", "Cowork"), ("monitor", "Desktop")]


def pglyph(name):
    return g.mark(name[1:]) if name.startswith("@") else stroke(name)


k.css("""
.abs { position: absolute; }
.hide { opacity: 0; visibility: hidden; }
.tw { position: absolute; }
.sk { fill: none; stroke: url(#gw); stroke-width: 2.3; stroke-linecap: round; stroke-linejoin: round;
  width: 50%; height: 50%; position: relative; z-index: 1; overflow: visible; }
.pearl .sk { stroke: #17141c; }
.clear { overflow: hidden; }
.circ .jelly, .circ .pearl, .circ .clear, .circ .sheen { border-radius: 50%; }
.aurs { position: absolute; left: -700px; top: -700px; width: 2480px; height: 3320px; pointer-events: none;
  background:
    radial-gradient(circle 526px at 1560px 880px, rgba(255,110,156,0.50), rgba(255,110,156,0)),
    radial-gradient(circle 634px at 760px 2360px, rgba(222,32,74,0.55), rgba(222,32,74,0)),
    radial-gradient(circle 382px at 1480px 1910px, rgba(255,198,214,0.20), rgba(255,198,214,0)); }
.shc { position: absolute; inset: 0; border-radius: inherit; overflow: hidden; pointer-events: none; }
.shc .sheen { mix-blend-mode: normal; opacity: 0.4; }
.cur { position: absolute; left: -11px; top: -8px; width: 64px; height: 64px; z-index: 6;
  filter: drop-shadow(0 6px 10px rgba(24,4,12,0.35)); }
.ck { position: absolute; width: 120px; height: 120px; margin: -60px 0 0 -60px; border-radius: 50%;
  border: 7px solid #ff6e9c; opacity: 0; visibility: hidden; z-index: 5; }
.wm { position: absolute; font-weight: 900; letter-spacing: -0.04em; line-height: 1; color: #fff; text-align: center; }

/* A · her real Threads screenshot (proof is a screenshot: never retyped) */
.shot { position: absolute; border-radius: 44px; overflow: hidden; background: #fff;
  box-shadow: inset 0 2px 1px #fff, 0 50px 100px -36px rgba(24,4,12,0.62), 0 0 0 1px rgba(255,255,255,0.45); }
.shot img { position: absolute; left: 0; top: 0; display: block; }
.mark { position: absolute; height: 46px; border-radius: 10px; transform-origin: 0 50%;
  background: rgba(255,110,156,0.42); mix-blend-mode: multiply; }

/* B · the seesaw */
.beam { position: absolute; border-radius: 16px; height: 32px;
  background: linear-gradient(180deg, rgba(255,255,255,0.9) 0%, rgba(255,236,242,0.78) 100%);
  box-shadow: inset 0 2px 1px #fff, 0 26px 50px -18px rgba(24,4,12,0.55); }
.fulc { position: absolute; width: 0; height: 0; border-left: 46px solid transparent; border-right: 46px solid transparent;
  border-bottom: 78px solid rgba(255,255,255,0.86); filter: drop-shadow(0 20px 24px rgba(24,4,12,0.4)); }

/* C · the agent's window */
.win { position: absolute; border-radius: 48px; overflow: hidden; color: #17141c;
  background: linear-gradient(172deg, #ffffff 0%, #fff9fb 55%, #fdf0f4 100%);
  box-shadow: inset 0 2px 1px #fff, 0 50px 100px -36px rgba(24,4,12,0.62), 0 0 0 1px rgba(255,255,255,0.4); }
.win i { position: absolute; display: block; }
.win .bar { left: 0; top: 0; right: 0; height: 70px; background: #f6e6eb; }
.win .dot { top: 27px; width: 16px; height: 16px; border-radius: 50%; background: rgba(23,20,28,0.18); }
.rr { border-radius: 12px; background: rgba(23,20,28,0.13); }
.hb { border-radius: 12px; background: linear-gradient(115deg, #c41434 0%, #8d0d24 100%); }
.im { border-radius: 18px; background: linear-gradient(150deg, #f4dfe5 0%, #ecc8d0 100%); }
.btn { border-radius: 999px; background: linear-gradient(165deg, #e0204b 0%, #ab112e 46%, #6b081c 100%);
  box-shadow: inset 0 2px 1px rgba(255,255,255,0.5), 0 18px 36px -14px rgba(70,4,20,0.6);
  display: flex; align-items: center; justify-content: center; }
.btn .sk { width: 44px; height: 44px; }
.cbx { position: absolute; width: 54px; height: 54px; border-radius: 16px;
  box-shadow: inset 0 0 0 4px rgba(23,20,28,0.22); }
.cbf { position: absolute; inset: 0; border-radius: 16px;
  background: linear-gradient(165deg, #e0204b 0%, #8d0d24 100%); opacity: 0; visibility: hidden; }
.cbf svg { position: absolute; left: 8px; top: 8px; width: 38px; height: 38px; fill: none; stroke: #fff;
  stroke-width: 3.2; stroke-linecap: round; stroke-linejoin: round; }
.chip2 { position: absolute; height: 64px; padding: 0 26px; border-radius: 32px; display: flex; align-items: center;
  background: linear-gradient(165deg, #e0204b 0%, #8d0d24 100%); color: #fff; font-size: 34px; font-weight: 900;
  letter-spacing: 0.04em; box-shadow: inset 0 2px 1px rgba(255,255,255,0.5), 0 20px 40px -16px rgba(70,4,20,0.7); }
.ctag { position: absolute; left: 40px; top: 44px; width: 58px; height: 58px; }

/* D · orbit */
.plb { position: absolute; left: -50px; width: 240px; top: 152px; text-align: center; font-size: 31px; font-weight: 700;
  color: #fff; letter-spacing: -0.01em; }
.orbr { fill: none; stroke: rgba(255,255,255,0.22); stroke-width: 4; stroke-linecap: round; }

/* F · Claude Design */
.wtb { position: absolute; left: 0; top: 0; right: 0; height: 92px; border-bottom: 2px solid rgba(23,20,28,0.07); }
.wtt { position: absolute; left: 112px; top: 0; line-height: 92px; font-size: 36px; font-weight: 700; letter-spacing: -0.015em; }
.wtt b { font-weight: 500; color: rgba(23,20,28,0.5); }
.cvs { position: absolute; left: 0; right: 0; top: 92px; bottom: 0; background-color: #fbf2f5;
  background-image: repeating-linear-gradient(0deg, rgba(23,20,28,.05) 0 1px, transparent 1px 40px),
                    repeating-linear-gradient(90deg, rgba(23,20,28,.05) 0 1px, transparent 1px 40px); }
.tbar { position: absolute; left: 24px; top: 28px; width: 76px; height: 236px; border-radius: 26px; background: #fff;
  box-shadow: 0 10px 24px -10px rgba(24,4,12,0.25); }
.tbar .sk { position: absolute; left: 20px; width: 36px; height: 36px; stroke: #17141c; }
.ab { position: absolute; border-radius: 22px; background: #fff; overflow: hidden;
  box-shadow: 0 18px 36px -16px rgba(24,4,12,0.35), 0 0 0 1px rgba(23,20,28,0.05); }
.ab i { position: absolute; display: block; }
.gt { position: absolute; font-weight: 900; font-size: 150px; color: #fff; line-height: 1; letter-spacing: -0.04em;
  filter: drop-shadow(0 0 18px rgba(255,110,156,0.75)) drop-shadow(0 10px 20px rgba(24,4,12,0.4)); }

/* H · sync */
.cab .tube { fill: none; stroke: rgba(255,255,255,0.26); stroke-width: 20; stroke-linecap: round; }
.cab .core { fill: none; stroke: rgba(255,255,255,0.92); stroke-width: 4.5; stroke-linecap: round; }
.cab .pkt  { fill: none; stroke: #ffd6e3; stroke-width: 11; stroke-linecap: round; }
.cab .pkg  { filter: drop-shadow(0 0 10px rgba(255,120,165,1)); }
.bub { position: absolute; width: 230px; height: 104px; border-radius: 34px 34px 34px 10px;
  background: linear-gradient(170deg, #ffffff 0%, #fff4f7 100%);
  box-shadow: inset 0 2px 1px #fff, 0 26px 50px -18px rgba(24,4,12,0.55); }
.bub i { position: absolute; display: block; }
.bub.ghost { background: none; box-shadow: none; border: 4px dashed rgba(255,255,255,0.75); }
.gl2 { position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; }
.jelly .gl2 .sk { width: 52%; height: 52%; }

/* I · platforms */
.plat { position: absolute; height: 60px; border-radius: 30px; }
.trl { fill: none; stroke: rgba(255,214,227,0.85); stroke-width: 7; stroke-linecap: round; }

/* J · tuning sheet */
.trk { position: absolute; height: 18px; border-radius: 9px; background: rgba(23,20,28,0.10); }
.fil { position: absolute; height: 18px; border-radius: 9px; transform-origin: 0 50%;
  background: linear-gradient(90deg, #ff8ab0 0%, #e0204b 100%); }
.knob { position: absolute; width: 58px; height: 58px; border-radius: 50%;
  background: linear-gradient(160deg, #ffffff 0%, #fbeef2 100%);
  box-shadow: inset 0 2px 1px #fff, 0 10px 22px -6px rgba(70,4,20,0.45), 0 0 0 1px rgba(23,20,28,0.06); }
.sav { position: absolute; left: 44px; top: 40px; width: 110px; height: 110px; border-radius: 50%;
  background: linear-gradient(160deg, #f4dfe5 0%, #e7c3cd 100%); display: flex; align-items: center; justify-content: center; }
.sav .sk { width: 56%; height: 56%; stroke: rgba(23,20,28,0.6); }
.best { position: absolute; height: 92px; width: 330px; justify-content: center; border-radius: 46px; display: flex; align-items: center; gap: 12px;
  background: linear-gradient(165deg, #ffffff 0%, #ffeef3 100%); color: #b4122f; font-size: 46px; font-weight: 900;
  letter-spacing: -0.01em; box-shadow: inset 0 2px 1px #fff, 0 24px 48px -16px rgba(8,0,3,0.7); white-space: nowrap; }
.best .sk { width: 48px; height: 48px; stroke: #e0204b; }
.strike { position: absolute; left: 22px; right: 22px; top: 41px; height: 10px; border-radius: 5px; background: #17141c;
  transform-origin: 0 50%; }

/* L · follow */
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


# ===========================================================================
# A · the hook — her real Threads screenshot; a highlighter reads along with her
SHOT_W = 940
SHOT_K = SHOT_W / 1080.0                 # proof-threads.jpg is 1080x397
SHOT_H = int(round(397 * SHOT_K))
# (left, top, right) of each text line in the source image, and the caption
# indices she reads it over
LINES = [((193, 108, 1004), 0, 4), ((193, 166, 842), 5, 9), ((193, 222, 628), 10, 14)]


@beat
def a_post():
    marks = "".join('<div class="mark" id="aM%d" style="left:%dpx;top:%dpx;width:%dpx"></div>'
                    % (i, x0 * SHOT_K - 6, (y0 + 27) * SHOT_K - 23, (x1 - x0) * SHOT_K + 12)
                    for i, ((x0, y0, x1), _, _) in enumerate(LINES))
    L.append(
        '<div class="g full" id="gA">'
        '<div class="shot edge hide" id="pt" style="left:70px;top:150px;width:%dpx;height:%dpx">'
        '<img src="assets/proof-threads.jpg" width="%d" height="%d" alt="">%s'
        '<div class="shc"><div class="sheen"></div></div></div></div>'
        % (SHOT_W, SHOT_H, SHOT_W, SHOT_H, marks))
    sfx("pop", 0.04, -2)
    sw = []
    for i, (_, c0, c1) in enumerate(LINES):
        t0, t1 = CAPS[c0]["s"], CAPS[c1]["e"]
        sw.append('  gsap.set("#aM%d", {scaleX: 0});'
                  ' tl.fromTo("#aM%d", {scaleX: 0}, {scaleX: 1, duration: %.3f, ease: "none", immediateRender: false}, %.3f);'
                  % (i, i, max(0.3, t1 - t0), t0))
    return js("""
  tl.set("#gA", {autoAlpha: 1}, 0);
  arr("#pt", 0.0, {s: 0.86, y: 40, d: 0.8, blur: 8});
  shn("#pt .sheen", 0.35);
{{sw}}
  tl.to("#pt", {scale: 0.5, y: 70, autoAlpha: 0, filter: "blur(10px)", duration: 0.34, ease: "power2.in"}, @chesno-0.1);
  tl.set("#gA", {autoAlpha: 0}, @chesno+0.3);""").replace("{{sw}}", "\n".join(sw))


# ===========================================================================
# B · «різниці великої немає» — a seesaw settles level
@beat
def b_seesaw():
    L.append(
        '<div class="g full" id="gB">'
        '<div class="fulc hide" id="bF" style="left:494px;top:486px"></div>'
        '<div class="abs" id="bSee" style="left:0;top:0;width:1080px;height:640px">'
        '<div class="beam hide" id="bBeam" style="left:150px;top:458px;width:780px"></div>'
        + tile("bGp", 190, 200, 262, "pearl", g.mark("openai"))
        + tile("bCl", 190, 690, 262, "jelly", g.mark("claude"))
        + '</div>'
        + '<div class="tw circ hide" id="bEq" style="left:480px;top:300px;width:120px;height:120px">'
          '<div class="clear"><span class="wm" style="position:relative;font-size:84px;top:-4px">≈</span></div></div>'
        + '</div>')
    sfx("whoosh-short", T["chesno"] - 0.12, -2)
    sfx("click", T["nemaie"] + 0.12)
    return js("""
  tl.set("#gB", {autoAlpha: 1}, @chesno-0.12);
  gsap.set("#bSee", {transformOrigin: "540px 474px"});
  arr("#bBeam", @chesno-0.08, {s: 0.7, y: 20, d: 0.7});
  arr("#bF", @chesno-0.02, {s: 0.5, y: 20, d: 0.7});
  arr("#bGp", @chesno-0.02, {s: 0.4, x: 140, y: -60});
  arr("#bCl", @chesno+0.06, {s: 0.4, x: -140, y: -60});
  tl.fromTo("#bSee", {rotation: 0}, {rotation: -6, duration: 0.6, ease: SOFT}, @chesno+0.2);
  tl.to("#bSee", {rotation: 5, duration: 0.44, ease: SOFT}, @riznytsi);
  tl.to("#bSee", {rotation: -2.5, duration: 0.45, ease: SOFT}, @velykoi);
  tl.to("#bSee", {rotation: 0, duration: 0.6, ease: SP}, @nemaie);
  arr("#bEq", @nemaie+0.12, {s: 0.3, y: 10, d: 0.6});
  bout(["#bBeam", "#bF", "#bCl", "#bEq"], @gpt2-0.08, 10, 0.26);
  tl.set("#bGp", {autoAlpha: 0}, @gpt2+0.02);
  tl.set("#gB", {autoAlpha: 0}, @gpt2+0.3);""")


# ===========================================================================
# C · ChatGPT went toward AGI: an agent that does things for you
WIN_C = (330, 118, 680, 490)
ROWS_C = (122, 214, 306)


@beat
def c_agent():
    wx, wy, ww, wh = WIN_C
    rows = ""
    for i, (y, w) in enumerate(zip(ROWS_C, (380, 300, 430))):
        rows += ('<div class="cbx" style="left:44px;top:%dpx"><div class="cbf" id="cc%d">'
                 '<svg viewBox="0 0 24 24"><path id="ccp%d" d="M5.4 12.6l4.3 4.3 8.9-9.5"/></svg></div></div>'
                 '<i class="rr" style="left:126px;top:%dpx;width:%dpx;height:26px;border-radius:13px"></i>'
                 % (y, i, i, y + 14, w))
    win = ('<div class="win hide" id="cW" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx">'
           '<i class="bar"></i><i class="dot" style="left:30px"></i><i class="dot" style="left:56px"></i>'
           '<i class="dot" style="left:82px"></i>%s'
           '<i class="btn" id="cBtn" style="left:%dpx;top:%dpx;width:150px;height:76px">%s</i>'
           '<div class="shc"><div class="sheen"></div></div></div>'
           % (wx, wy, ww, wh, rows, ww - 194, wh - 112, stroke("send")))
    cur = ('<div class="abs hide" id="cCur" style="left:0;top:0;width:10px;height:10px">'
           '<div class="cur">%s</div>'
           '<div class="tw circ" style="left:34px;top:40px;width:62px;height:62px"><div class="pearl">%s</div></div></div>'
           % (CURSOR, g.mark("openai")))
    pts = [(185, 309)] + [(WIN_C[0] + 44 + 27, WIN_C[1] + y + 27) for y in ROWS_C] + \
          [(WIN_C[0] + WIN_C[2] - 194 + 75, WIN_C[1] + WIN_C[3] - 112 + 38)]
    ck = "".join('<div class="ck" id="cK%d" style="left:%dpx;top:%dpx"></div>' % (i, p[0], p[1])
                 for i, p in enumerate(pts[1:]))
    L.append('<div class="g full" id="gC">'
             + tile("cGp", 190, 90, 214, "pearl", g.mark("openai"))
             + '<div class="chip2 hide" id="cAgi" style="left:176px;top:168px">AGI</div>'
             + win + ck + cur + '</div>')
    sfx("click-soft", T["agi"] + 0.04)
    sfx("click", T["sam"] + 0.05)
    sfx("click", T["tebe"] + 0.07, -1)
    # cursor stops: tile centre -> 3 checkboxes -> send
    stops = [("sam", 0.05), ("vykonuie", 0.36), ("dii", 0.12), ("tebe", 0.07)]
    moves = []
    for i, ((w, off), p) in enumerate(zip(stops, pts[1:])):
        t_hit = T[w] + off
        prev_hit = T[stops[i - 1][0]] + stops[i - 1][1] if i else T["tobto"] + 0.35
        d = min(0.42, max(0.18, t_hit - prev_hit - 0.06))
        moves.append('  tl.to("#cCur", {x: %d, y: %d, duration: %.2f, ease: "power2.inOut"}, %.3f);'
                     % (p[0], p[1], d, t_hit - d))
        moves.append('  tl.to("#cCur .cur", {scale: 0.84, duration: 0.07}, %.3f); tl.to("#cCur .cur", {scale: 1, duration: 0.1}, %.3f);'
                     % (t_hit, t_hit + 0.07))
        moves.append('  tl.fromTo("#cK%d", {scale: 0.3, autoAlpha: 0.95}, {scale: 1.3, autoAlpha: 0, duration: 0.45, ease: "power2.out", immediateRender: false}, %.3f);'
                     % (i, t_hit + 0.01))
        if i < 3:
            moves.append('  tl.fromTo("#cc%d", {autoAlpha: 0, scale: 0.4}, {autoAlpha: 1, scale: 1, duration: 0.35, ease: POP}, %.3f);'
                         ' draw2("ccp%d", %.3f, 0.25);' % (i, t_hit + 0.02, i, t_hit + 0.06))
        else:
            moves.append('  G.bump("#cBtn", %.3f);' % t_hit)
    return js("""
  tl.set("#gC", {autoAlpha: 1}, @gpt2-0.06);
  /* the seesaw's ChatGPT tile becomes this one */
  tl.set("#cGp", {autoAlpha: 1, x: 110, y: 48}, @gpt2+0.02);
  tl.to("#cGp", {x: 0, y: 0, duration: 0.6, ease: SP}, @gpt2+0.04);
  G.ripple("#cGpR", @gpt2+0.4);
  arr("#cAgi", @agi-0.04, {s: 0.3, x: -20, y: 20, d: 0.6});
  arr("#cW", @gpt2+0.55, {s: 0.75, x: -60, y: 30, d: 0.8});
  shn("#cW .sheen", @gpt2+0.9);
  tl.set("#cCur", {x: {{x0}}, y: {{y0}}}, 0);
  tl.fromTo("#cCur", {autoAlpha: 0, scale: 0.2}, {autoAlpha: 1, scale: 1, duration: 0.45, ease: POP}, @tobto);
{{moves}}
  bout(["#cW", "#cGp", "#cAgi", "#cCur"], @a3-0.16, 10, 0.24);
  tl.set("#gC", {autoAlpha: 0}, @a3+0.12);""").replace("{{x0}}", str(pts[0][0])).replace(
        "{{y0}}", str(pts[0][1])).replace("{{moves}}", "\n".join(moves))


# ===========================================================================
# D · OVER — Claude built an ecosystem of products around itself
HUB_C = (540, 700)
ORB_R = 330
E_CL = (810, 210, 180)          # Claude tile in beat E (x, y, size)


def orbit_pos(i, cx=HUB_C[0], cy=HUB_C[1], rx=ORB_R, ry=ORB_R):
    a = math.radians(-90 + 60 * i)
    return cx + rx * math.cos(a), cy + ry * math.sin(a)


@beat
def d_ecosystem():
    items = ""
    for i, (gl, lb) in enumerate(PRODUCTS):
        x, y = orbit_pos(i)
        items += ('<div class="tw hide oi" id="o%d" style="left:%dpx;top:%dpx;width:140px;height:140px">'
                  '<div class="pearl">%s<div class="sheen"></div></div><div class="plb hide" id="ol%d">%s</div></div>'
                  % (i, x - 70, y - 70, pglyph(gl), i, lb))
    ring = ('<svg class="abs" width="1080" height="1920" style="left:0;top:0">'
            '<path class="orbr" id="oRing" d="M%d %d A%d %d 0 1 1 %.1f %d"/></svg>'
            % (HUB_C[0], HUB_C[1] - ORB_R, ORB_R, ORB_R, HUB_C[0] - 0.1, HUB_C[1] - ORB_R))
    L.append('<div class="g full" id="gD"><div class="tkg"></div><div class="aurs"></div><div class="grain"></div>'
             '<div class="abs" id="dOrb" style="left:0;top:0;width:1080px;height:1920px">%s%s</div>' % (ring, items)
             + tile("dHub", 260, HUB_C[0] - 130, HUB_C[1] - 130, "jelly", g.mark("claude"))
             + '</div>')
    # the near Claude tile the iris opens out of
    L.append('<div class="g full" id="gD0">' + tile("dCl", 200, 440, 170, "jelly", g.mark("claude")) + '</div>')
    sfx("whoosh-short", T["claude3"] + 0.06)
    sfx("pop", T["ekosys"] + 0.02, -3)
    hx = (E_CL[0] + E_CL[2] / 2) - HUB_C[0]
    hy = (E_CL[1] + E_CL[2] / 2) - HUB_C[1]
    hs = E_CL[2] / 260.0
    pops = []
    for i in range(6):
        x, y = orbit_pos(i)
        pops.append('  arr("#o%d", %.3f, {s: 0.3, x: %d, y: %d, d: 0.75});'
                    % (i, T["ekosys"] - 0.04 + i * 0.07, (HUB_C[0] - x) * 0.8, (HUB_C[1] - y) * 0.8))
    return js("""
  tl.set("#gD0", {autoAlpha: 1}, @a3-0.08);
  arr("#dCl", @a3-0.06, {s: 0.4, y: 40, d: 0.7});
  G.ripple("#dClR", @claude3+0.05);
  G.irisOpen("#gD", @claude3+0.06, 540, 270, 0.8);
  drift1("#gD", @claude3, 3.6);
  /* the hub is the same tile, pulled down into the middle */
  /* hand-off once the iris has covered the near tile: same size, same spot */
  tl.set("#dHub", {autoAlpha: 1, x: 0, y: -430, scale: 0.77}, @claude3+0.3);
  tl.set("#gD0", {autoAlpha: 0}, @claude3+0.31);
  tl.fromTo("#dHub", {x: 0, y: -430, scale: 0.77}, {x: 0, y: 0, scale: 1, duration: 0.7, ease: SP, immediateRender: false}, @claude3+0.32);
  draw2("oRing", @ekosys-0.1, 0.9);
{{pops}}
  G.bump("#dHub", @produktiv-0.05); shn("#dHub .sheen", @produktiv);
  tl.fromTo(".plb", {autoAlpha: 0, y: 12}, {autoAlpha: 1, y: 0, duration: 0.35, ease: "power2.out", stagger: 0.06}, @produktiv);
  gsap.set("#dOrb", {transformOrigin: "540px 700px"}); gsap.set(".oi", {transformOrigin: "50% 50%"});
  tl.to("#dOrb", {rotation: 30, duration: 0.9, ease: SP}, @navkolo);
  tl.to(".oi", {rotation: -30, duration: 0.9, ease: SP}, @navkolo);
  G.ripple("#dHubR", @navkolo+0.35);
  /* the ring folds away, the hub travels to where Claude sits next */
  tl.to(".oi", {scale: 0.3, autoAlpha: 0, duration: 0.32, ease: "power2.in", stagger: 0.03}, @tut-0.42);
  tl.to("#oRing", {autoAlpha: 0, duration: 0.3}, @tut-0.42);
  tl.to("#dHub", {x: {{hx}}, y: {{hy}}, scale: {{hs}}, duration: 0.6, ease: "power3.inOut"}, @tut-0.4);
  G.irisClose("#gD", @tut-0.3, {{ex}}, {{ey}}, 0.55);""").replace("{{pops}}", "\n".join(pops)).replace(
        "{{hx}}", "%d" % hx).replace("{{hy}}", "%d" % hy).replace("{{hs}}", "%.3f" % hs).replace(
        "{{ex}}", "%d" % (E_CL[0] + E_CL[2] / 2)).replace("{{ey}}", "%d" % (E_CL[1] + E_CL[2] / 2))


# ===========================================================================
# E · which is closer to you — she picks Claude
@beat
def e_choice():
    ex, ey, es = E_CL
    L.append('<div class="g full" id="gE">'
             + tile("eGp", 180, 90, 210, "pearl", g.mark("openai"))
             + badge("ePs", 170, 455, 215, "pearl", "person")
             + badge("eQ", 70, 590, 196, "jelly", "q")
             + tile("eCl", es, ex, ey, "jelly", g.mark("claude"))
             + badge("eCk", 70, ex - 125 + es - 46, ey - 24, "pearl", "check")
             + '</div>')
    sfx("pop", T["tut"] + 0.05, -2)
    sfx("pop", T["obrala"] + 0.08)
    return js("""
  tl.set("#gE", {autoAlpha: 1}, @tut-0.3);
  tl.set("#eCl", {autoAlpha: 1}, @tut+0.2);
  arr("#ePs", @tut, {s: 0.4, y: 30});
  arr("#eGp", @tut+0.14, {s: 0.4, x: -40, y: 30});
  G.ripple("#eGpR", @tut+0.45);
  arr("#eQ", @pytannia+0.02, {s: 0.2, y: 10, d: 0.55});
  tl.to("#eGp", {x: 80, duration: 0.7, ease: SP}, @blyzhche-0.05);
  tl.to("#eCl", {x: -80, duration: 0.7, ease: SP}, @blyzhche-0.05);
  /* the pick */
  bout("#eQ", @obrala-0.1, 8, 0.2);
  tl.to("#eGp", {x: 0, scale: 0.8, autoAlpha: 0.32, duration: 0.5, ease: "power2.out"}, @obrala);
  tl.to("#eCl", {x: -125, duration: 0.55, ease: SP}, @obrala);
  arr("#eCk", @obrala+0.08, {s: 0.2, x: -60, y: 10, d: 0.6});
  G.bump("#eCl", @claude4); shn("#eCl .sheen", @claude4);
  bout(["#eGp", "#ePs", "#eCk"], @u-0.1, 10, 0.26);
  /* the tile becomes the Design window's logo */
  tl.to("#eCl", {x: {{lx}}, y: {{ly}}, scale: {{ls}}, duration: 0.55, ease: "power3.inOut"}, @u-0.05);
  tl.set("#gE", {autoAlpha: 0}, @dyzain+0.12);""").replace(
        "{{lx}}", "%d" % (WIN_F[0] + 30 + 31 - (ex + es / 2))).replace(
        "{{ly}}", "%d" % (WIN_F[1] + 15 + 31 - (ey + es / 2))).replace("{{ls}}", "%.3f" % (62.0 / es))


# ===========================================================================
# F · Claude Design covers her light design needs
WIN_F = (80, 110, 920, 500)


@beat
def f_design():
    wx, wy, ww, wh = WIN_F
    abs_ = (
        '<div class="ab hide" id="fA1" style="left:136px;top:56px;width:236px;height:236px">'
        '<i class="im" style="left:20px;top:20px;width:196px;height:124px"></i>'
        '<i class="hb" style="left:20px;top:160px;width:150px;height:22px;border-radius:11px"></i>'
        '<i class="rr" style="left:20px;top:196px;width:110px;height:16px;border-radius:8px"></i></div>'
        '<div class="ab hide" id="fA2" style="left:404px;top:34px;width:164px;height:290px">'
        '<i class="im" style="left:18px;top:18px;width:128px;height:168px"></i>'
        '<i class="rr" style="left:18px;top:202px;width:110px;height:16px;border-radius:8px"></i>'
        '<i class="btn" style="left:18px;top:236px;width:128px;height:36px"></i></div>'
        '<div class="ab hide" id="fA3" style="left:600px;top:96px;width:292px;height:156px">'
        '<i class="hb" style="left:22px;top:26px;width:150px;height:24px;border-radius:12px"></i>'
        '<i class="rr" style="left:22px;top:64px;width:118px;height:15px;border-radius:8px"></i>'
        '<i class="btn" style="left:22px;top:98px;width:112px;height:36px"></i>'
        '<i class="im" style="left:180px;top:30px;width:92px;height:92px;border-radius:50%"></i></div>')
    tb = ('<div class="tbar">%s</div>' % "".join(
        '<svg class="sk" viewBox="0 0 24 24" style="top:%dpx">%s</svg>' % (24 + i * 70, STROKES[n])
        for i, n in enumerate(("pointer", "rect", "text"))))
    win = ('<div class="win hide" id="fW" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx">'
           '<div class="wtb"><div class="tw" style="left:30px;top:15px;width:62px;height:62px">'
           '<div class="jelly">%s</div></div><div class="wtt">Claude <b>Design</b></div></div>'
           '<div class="cvs">%s%s</div>'
           '<div class="shc"><div class="sheen"></div></div></div>'
           % (wx, wy, ww, wh, g.mark("claude"), tb, abs_))
    L.append('<div class="g full" id="gF">' + win
             + badge("fCk", 78, wx + ww - 108, wy + 7, "jelly", "check") + '</div>')
    sfx("whoosh-short", T["dyzain"] - 0.12, -2)
    sfx("click", T["holovoiu"] + 0.05)
    return js("""
  tl.set("#gF", {autoAlpha: 1}, @dyzain-0.2);
  gsap.set("#fW", {transformOrigin: "60px 46px"});
  arr("#fW", @dyzain-0.16, {s: 0.25, y: 0, d: 0.85, blur: 10});
  shn("#fW .sheen", @dyzain+0.3);
  arr("#fA1", @lehenkykh-0.02, {s: 0.5, y: 30, d: 0.7});
  arr("#fA2", @dyzainer-0.02, {s: 0.5, y: 30, d: 0.7});
  arr("#fA3", @potreb-0.02, {s: 0.5, y: 30, d: 0.7});
  G.bump("#fW", @vystachaie+0.05);
  arr("#fCk", @holovoiu+0.02, {s: 0.2, y: 10, d: 0.6});
  /* G grows out of it: the window steps left to make room */
  bout("#fCk", @tse-0.12, 8, 0.2);""")


# ===========================================================================
# G · much more convenient than the integrated Figma
@beat
def g_figma():
    L.append('<div class="g full" id="gG">'
             '<div class="gt hide" id="gGt" style="left:566px;top:226px">&gt;</div>'
             + tile("gFg", 200, 712, 206, "pearl", g.mark("figma"))
             + tile("gCl", 78, 866, 176, "jelly", g.mark("claude"), ring=False)
             + '</div>')
    sfx("pop", T["nizh"] + 0.06)
    sfx("click-soft", T["fihma"] + 0.04, -1)
    return js("""
  tl.set("#gG", {autoAlpha: 1}, @tse-0.1);
  tl.set("#fW", {transformOrigin: "0px 0px"}, @tse-0.07);
  tl.to("#fW", {x: -10, y: 70, scale: 0.5, duration: 0.7, ease: SP}, @tse-0.05);
  tl.to("#fW", {scale: 0.535, duration: 0.1, ease: "power2.out"}, @zruchnishe+0.05);
  tl.to("#fW", {scale: 0.5, duration: 0.45, ease: SP}, @zruchnishe+0.15); shn("#fW .sheen", @zruchnishe);
  arr("#gGt", @nizh-0.04, {s: 0.4, x: -20, y: 0, d: 0.6});
  arr("#gFg", @nizh+0.04, {s: 0.5, x: 40, y: 20});
  /* Claude, plugged into Figma */
  arr("#gCl", @intehr+0.02, {s: 0.3, x: -150, y: 40, d: 0.7});
  G.bump("#gFg", @fihma+0.02); G.ripple("#gFgR", @fihma+0.06);
  bout(["#gGt", "#gFg", "#gCl", "#fW"], @shche-0.08, 10, 0.26);
  tl.set(["#gG", "#gF"], {autoAlpha: 0}, @shche+0.22);""")


# ===========================================================================
# H · the ChatGPT chat doesn't sync between the local app and the cloud
@beat
def h_sync():
    cab = ('<svg class="cab abs" width="1080" height="640" viewBox="0 0 1080 640" style="left:0;top:0">'
           '<path class="tube hide" id="hT" d="M318 330 L762 330"/>'
           '<path class="core hide" id="hC" d="M318 330 L762 330"/>'
           '<g class="pkg"><path class="pkt" id="hP" style="opacity:0" d="M318 330 L486 330"/></g></svg>')
    bub = ('<div class="bub hide" id="hB1" style="left:95px;top:452px">'
           '<i class="hb" style="left:26px;top:28px;width:140px;height:20px;border-radius:10px"></i>'
           '<i class="rr" style="left:26px;top:62px;width:176px;height:16px;border-radius:8px"></i></div>'
           '<div class="bub ghost hide" id="hB2" style="left:755px;top:452px"></div>')
    sync = ('<div class="tw circ hide" id="hS" style="left:480px;top:270px;width:120px;height:120px"><div class="jelly">'
            '<div class="gl2" id="hSs">%s</div><div class="gl2" id="hSx" style="opacity:0">%s</div>'
            '<div class="gl2" id="hSq" style="opacity:0">%s</div><div class="sheen"></div></div></div>'
            % (stroke("sync"), stroke("x"), stroke("q")))
    L.append('<div class="g full" id="gH"><div class="abs" id="hAll" style="left:0;top:0;width:1080px;height:640px">'
             + cab
             + tile("hGp", 140, 470, 84, "pearl", g.mark("openai"))
             + tile("hLp", 200, 110, 230, "clear", stroke("laptop"))
             + tile("hCd", 200, 770, 230, "clear", stroke("cloud"))
             + sync + bub + '</div>'
             + tile("hCo", 140, 470, 486, "jelly", stroke("code"))
             + '</div>')
    sfx("pop", T["gpt3"] + 0.04, -2)
    sfx("click", T["syncro"] + 0.62)
    sfx("pop", T["vaib"] + 0.04, -2)
    return js("""
  tl.set("#gH", {autoAlpha: 1}, @shche);
  arr("#hGp", @gpt3-0.04, {s: 0.4, y: 30});
  arr("#hLp", @ne_s-0.02, {s: 0.4, x: 120, y: -40});
  arr("#hCd", @ne_s+0.08, {s: 0.4, x: -120, y: -40});
  tl.set(["#hT", "#hC"], {autoAlpha: 1}, @ne_s+0.2);
  draw2("hT", @ne_s+0.2, 0.45); draw2("hC", @ne_s+0.2, 0.45);
  arr("#hS", @syncro-0.05, {s: 0.3, y: 0, d: 0.6});
  tl.fromTo("#hSs", {rotation: 0}, {rotation: 300, duration: 0.65, ease: "power2.inOut"}, @syncro);
  /* it stops: × */
  tl.to("#hSs", {opacity: 0, duration: 0.12}, @syncro+0.6); tl.to("#hSx", {opacity: 1, duration: 0.12}, @syncro+0.62);
  G.haptic("#hS", @syncro+0.62);
  tl.to("#hC", {stroke: "#ff6e9c", duration: 0.2}, @syncro+0.62);
  arr("#hB1", @chat-0.02, {s: 0.4, x: 0, y: -40, d: 0.6});
  G.bump("#hLp", @lokal); G.ripple("#hLpR", @lokal+0.05);
  G.packet("hP", @lokal+0.15, 0.45);
  G.bump("#hS", @lokal+0.6);
  G.bump("#hCd", @khmaroiu); G.ripple("#hCdR", @khmaroiu+0.05);
  bin("#hB2", @khmaroiu+0.1, 8, 0.35);
  /* «це дрібниця»: the whole problem shrinks */
  gsap.set("#hAll", {transformOrigin: "540px 330px"});
  tl.to("#hAll", {scale: 0.62, duration: 0.7, ease: SP}, @dribn);
  arr("#hCo", @vaib-0.04, {s: 0.3, y: 30, d: 0.7});
  /* «можливо вже виправили»: × turns into ? */
  tl.to("#hSx", {opacity: 0, duration: 0.15}, @mozhlyvo+0.1); tl.to("#hSq", {opacity: 1, duration: 0.15}, @mozhlyvo+0.12);
  G.bump("#hS", @mozhlyvo+0.12);
  tl.to("#hC", {stroke: "rgba(255,255,255,0.92)", duration: 0.3}, @vypravyly);
  bout(["#hAll", "#hCo"], {{np}}, 10, 0.24);
  tl.set("#gH", {autoAlpha: 0}, {{npe}});""").replace("{{np}}", "%.3f" % (NO_PAINT[0][0] - 0.3)).replace(
        "{{npe}}", "%.3f" % (NO_PAINT[0][0] - 0.03))


# ===========================================================================
# I · no point hopping from one platform to the other
P_L, P_R = (335, 395), (755, 395)


@beat
def i_hop():
    arc = ('<svg class="abs" width="1080" height="640" style="left:0;top:0">'
           '<path class="trl" id="iTr" style="opacity:0" d="M%d %d Q545 120 %d %d"/></svg>'
           % (P_L[0], P_L[1], P_R[0], P_R[1]))
    L.append('<div class="g full" id="gI">'
             '<div class="shelf edge plat hide" id="iPl" style="left:60px;top:462px;width:370px"></div>'
             '<div class="shelf edge plat hide" id="iPr" style="left:650px;top:462px;width:370px"></div>'
             + arc
             + tile("iGp", 160, 86, 296, "pearl", g.mark("openai"))
             + tile("iCl", 160, 834, 296, "jelly", g.mark("claude"))
             + badge("iMe", 130, P_L[0] - 65, P_L[1] - 65, "pearl", "person")
             + badge("iX", 84, 503, 216, "jelly", "x")
             + '</div>')
    sfx("pop", T["ale2"] + 0.06, -2)
    sfx("whoosh-short", T["perestryb"] + 0.02, -1)
    sfx("click", T["nemaie2"] + 0.06)
    hop = """
  tl.to("#iMe", {x: %(x)d, duration: 0.6, ease: "power1.inOut"}, %(t).3f);
  tl.to("#iMe", {y: -138, duration: 0.3, ease: "power2.out"}, %(t).3f);
  tl.to("#iMe", {y: 0, duration: 0.3, ease: "power2.in"}, %(t2).3f);
  tl.to("#iMe", {scaleY: 0.88, scaleX: 1.08, duration: 0.08, ease: "power2.out"}, %(t3).3f);
  tl.to("#iMe", {scaleY: 1, scaleX: 1, duration: 0.35, ease: SP}, %(t4).3f);"""
    h1 = T["perestryb"] - 0.02
    h2 = T["platformy"] - 0.05
    return js("""
  tl.set("#gI", {autoAlpha: 1}, @ale2-0.05);
  arr("#iPl", @ale2, {s: 0.7, y: 30, d: 0.8});
  arr("#iPr", @ale2+0.1, {s: 0.7, y: 30, d: 0.8});
  arr("#iGp", @ale2+0.14, {s: 0.4, y: 40});
  arr("#iCl", @ale2+0.24, {s: 0.4, y: 40});
  gsap.set("#iMe", {transformOrigin: "50% 100%"});
  arr("#iMe", @yakshcho-0.02, {s: 0.3, y: 30, d: 0.7});
  tl.set("#iTr", {opacity: 1}, {{h1}}); draw2("iTr", {{h1}}, 0.6);""").replace("{{h1}}", "%.3f" % h1) \
        + hop % {"x": P_R[0] - P_L[0], "t": h1, "t2": h1 + 0.3, "t3": h1 + 0.6, "t4": h1 + 0.68} \
        + hop % {"x": 0, "t": h2, "t2": h2 + 0.3, "t3": h2 + 0.6, "t4": h2 + 0.68} \
        + js("""
  arr("#iX", @nemaie2+0.04, {s: 0.2, y: 10, d: 0.6});
  tl.to("#iTr", {opacity: 0.35, duration: 0.3}, @nemaie2+0.1);
  tl.set("#gI", {autoAlpha: 0}, @bud+0.7);""")


# ===========================================================================
# J · OVER — any AI tunes to you; learn it; don't chase «кращий»
SH = (140, 470, 800, 620)
ROWS_J = (236, 346, 456)
KX0, KX1 = (140, 560, 300), (470, 230, 610)
TRK_X, TRK_W = 60, 680


@beat
def j_tune():
    sx, sy, sw, sh = SH
    rows = ""
    for i, y in enumerate(ROWS_J):
        rows += ('<div class="trk jsl" style="left:%dpx;top:%dpx;width:%dpx"></div>'
                 '<div class="fil jsl" id="jF%d" style="left:%dpx;top:%dpx;width:%dpx"></div>'
                 '<div class="knob jsl" id="jK%d" style="left:%dpx;top:%dpx"></div>'
                 % (TRK_X, y + 20, TRK_W, i, TRK_X, y + 20, TRK_W, i, TRK_X - 29, y - 0))
        rows += ('<div class="cbx jcl" style="left:60px;top:%dpx;opacity:0;visibility:hidden"><div class="cbf" id="jc%d">'
                 '<svg viewBox="0 0 24 24"><path id="jcp%d" d="M5.4 12.6l4.3 4.3 8.9-9.5"/></svg></div></div>'
                 '<i class="rr jcl" style="position:absolute;display:block;left:142px;top:%dpx;width:%dpx;height:26px;'
                 'border-radius:13px;opacity:0;visibility:hidden"></i>'
                 % (y + 2, i, i, y + 16, (470, 380, 520)[i]))
    sheet = ('<div class="sheet hide" id="jS" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx">'
             '<div class="sav" id="jAv">%s</div>'
             '<i class="abs" style="left:184px;top:68px;width:230px;height:30px;border-radius:15px;background:rgba(23,20,28,0.78)"></i>'
             '<i class="abs" style="left:184px;top:112px;width:140px;height:20px;border-radius:10px;background:rgba(23,20,28,0.16)"></i>'
             '<i class="abs hair" style="left:44px;top:182px;width:712px"></i>%s'
             '<div class="shc"><div class="sheen"></div></div></div>'
             % (sx, sy, sw, sh, stroke("person"), rows))
    ais = (tile("jA0", 170, 230, 222, "pearl", g.mark("openai"))
           + tile("jA1", 170, 455, 222, "jelly", g.mark("claude"))
           + tile("jA2", 170, 680, 222, "pearl", g.mark("googlegemini")))
    best = ('<div class="best hide" id="jBest" style="left:150px;top:104px">%s«кращий»'
            '<div class="strike" id="jStr"></div></div>' % stroke("crown"))
    cur = '<div class="abs hide" id="jCur" style="left:0;top:0;width:10px;height:10px"><div class="cur">%s</div></div>' % CURSOR
    L.append('<div class="g full" id="gJ"><div class="tkg"></div><div class="aurs"></div><div class="grain"></div>'
             + ais + sheet + best + cur + '</div>')
    sfx("whoosh-short", T["bud"] - 0.18)
    sfx("click-soft", T["nalasht"] + 0.05, -1)
    sfx("click-soft", T["rozibr"] + 0.06, -2)
    sfx("click", T["krashchyi"] + 0.04)
    k0 = "".join('  gsap.set("#jK%d", {x: %d}); gsap.set("#jF%d", {scaleX: %.3f});\n'
                 % (i, KX0[i], i, KX0[i] / float(TRK_W)) for i in range(3))
    k1 = "".join('  tl.to("#jK%d", {x: %d, duration: 0.75, ease: SP}, %.3f);'
                 ' tl.to("#jF%d", {scaleX: %.3f, duration: 0.75, ease: SP}, %.3f);\n'
                 % (i, KX1[i], T["nalasht"] + i * 0.13, i, KX1[i] / float(TRK_W), T["nalasht"] + i * 0.13)
                 for i in range(3))
    ticks = "".join('  tl.fromTo("#jc%d", {autoAlpha: 0, scale: 0.4}, {autoAlpha: 1, scale: 1, duration: 0.35, ease: POP}, %.3f);'
                    ' draw2("jcp%d", %.3f, 0.25);\n' % (i, t, i, t + 0.05)
                    for i, t in enumerate((T["rozibr"] + 0.05, T["rozibr"] + 0.45, T["nomu"] + 0.02)))
    # «кращий» hops tile to tile; the cursor is always one tile late
    t1, t2 = T["haniatys"] + 0.12, T["tym"] - 0.02
    chase = """
  tl.set("#jCur", {x: 120, y: 190}, 0);
  arr("#jBest", @a5-0.02, {s: 0.4, y: 20, d: 0.6});
  bin("#jCur", @a5+0.1, 6, 0.25);
  tl.to("#jCur", {x: 300, y: 170, duration: 0.42, ease: "power2.inOut"}, @a5+0.12);
  tl.to("#jBest", {x: 225, duration: 0.34, ease: "power2.inOut"}, %(t1).3f);
  tl.to("#jBest", {y: -34, duration: 0.17, ease: "power2.out"}, %(t1).3f); tl.to("#jBest", {y: 0, duration: 0.17, ease: "power2.in"}, %(t1b).3f);
  tl.to("#jCur", {x: 525, y: 170, duration: 0.4, ease: "power2.inOut"}, %(c1).3f);
  tl.to("#jBest", {x: 450, duration: 0.34, ease: "power2.inOut"}, %(t2).3f);
  tl.to("#jBest", {y: -34, duration: 0.17, ease: "power2.out"}, %(t2).3f); tl.to("#jBest", {y: 0, duration: 0.17, ease: "power2.in"}, %(t2b).3f);
  tl.to("#jCur", {x: 560, y: 196, duration: 0.36, ease: "power2.inOut"}, %(c2).3f);""" % {
        "t1": t1, "t1b": t1 + 0.17, "c1": t1 + 0.2, "t2": t2, "t2b": t2 + 0.17, "c2": t2 + 0.2}
    return js("""
  G.irisOpen("#gJ", @bud-0.2, {{px}}, {{py}}, 0.8);
  drift1("#gJ", @bud-0.2, 6.2);
{{k0}}
  [0, 1, 2].forEach(function (i) { arr("#jA" + i, @bud-0.02 + i * 0.08, {s: 0.4, y: 40, d: 0.75}); });
  G.bump("#jA0", @shtuchnyi); G.bump("#jA1", @shtuchnyi+0.08); G.bump("#jA2", @shtuchnyi+0.16);
  arr("#jS", @shtuchnyi+0.1, {s: 0.8, y: 60, d: 0.8});
  shn("#jS .sheen", @shtuchnyi+0.5);
{{k1}}
  G.bump("#jAv", @pid+0.02);
  tl.to(".jsl", {autoAlpha: 0, duration: 0.25}, @holovne-0.08);
  tl.fromTo(".jcl", {autoAlpha: 0, x: -20}, {autoAlpha: 1, x: 0, duration: 0.35, ease: "power2.out", stagger: 0.05, immediateRender: false}, @holovne-0.02);
{{ticks}}
{{chase}}
  gsap.set("#jStr", {scaleX: 0});
  tl.fromTo("#jStr", {scaleX: 0}, {scaleX: 1, duration: 0.28, ease: "power2.out", immediateRender: false}, @krashchyi+0.02);
  tl.to("#jBest", {opacity: 0.6, duration: 0.3}, @krashchyi+0.25);
  G.irisClose("#gJ", @ya2-0.08, 540, 300, 0.55);""").replace("{{px}}", "%d" % P_L[0]).replace(
        "{{py}}", "%d" % P_L[1]).replace("{{k0}}", k0).replace("{{k1}}", k1).replace(
        "{{ticks}}", ticks).replace("{{chase}}", js(chase))


# ===========================================================================
# K · she chose Claude: tick, heart, bulb, the ecosystem again
K_CL = (440, 200, 200)


@beat
def k_claude():
    x, y, s = K_CL
    ring = ""
    for i, (gl, lb) in enumerate(PRODUCTS):
        px, py = orbit_pos(i, 540, 300, 380, 190)
        ring += tile("kO%d" % i, 100, px - 50, py - 50, "clear", pglyph(gl),
                     extra_cls="kor", ring=False)
    L.append('<div class="g full" id="gK">' + ring
             + tile("kCl", s, x, y, "jelly", g.mark("claude"))
             + badge("kCk", 72, x + s - 46, y - 24, "pearl", "check")
             + '<div class="abs" id="kBw" style="left:0;top:0;width:1080px;height:640px">'
             + badge("kHt", 120, 190, 240, "pearl", "heart")
             + '<div class="lit soft hide" id="kBl" style="inset:auto;left:770px;top:240px;width:120px;height:120px">'
               '<div class="tw circ" style="left:0;top:0;width:120px;height:120px"><div class="pearl">%s'
               '<div class="sheen"></div></div></div></div>' % stroke("bulb")
             + '</div></div>')
    sfx("pop", T["obrala2"] + 0.08)
    sfx("sparkle", T["rozumna"] + 0.02, -1)
    sfx("pop", T["ekosys2"] + 0.02, -3)
    return js("""
  tl.set("#gK", {autoAlpha: 1}, @ya2-0.2);
  tl.set("#kCl", {autoAlpha: 1}, @ya2-0.2);
  G.ripple("#kClR", @ya2+0.3);
  arr("#kCk", @obrala2+0.08, {s: 0.2, x: -60, y: 10, d: 0.6});
  G.bump("#kCl", @claude5); shn("#kCl .sheen", @claude5);
  arr("#kHt", @podob-0.04, {s: 0.3, x: 120, y: 20, d: 0.7});
  tl.to("#kHt .sk", {scale: 1.22, duration: 0.14, ease: "power2.out"}, @podob+0.45);
  tl.to("#kHt .sk", {scale: 1, duration: 0.4, ease: SP}, @podob+0.59);
  arr("#kBl", @rozumna-0.06, {s: 0.3, x: -120, y: 20, d: 0.7});
  bout(["#kBw", "#kCk"], @zruchno-0.06, 10, 0.26);
  [0, 1, 2, 3, 4, 5].forEach(function (i) { arr("#kO" + i, @zruchno+0.1 + i * 0.08, {s: 0.3, y: 0, d: 0.7}); });
  G.bump("#kCl", @ekosys2+0.05); G.ripple("#kClR", @ekosys2+0.1);
  bout("#gK", @yakshcho2-0.12, 10, 0.26);""")


# ===========================================================================
# L · Стежити
@beat
def l_follow():
    L.append('<div class="g full" id="gL"><div class="fl hide" id="fl" style="left:190px;top:300px;width:700px;height:150px">'
             '<div class="tw circ" style="left:28px;top:27px;width:96px;height:96px"><div class="jelly">%s</div></div>'
             '<div class="t" id="flT">Стежити</div>'
             '<div class="on" id="flOn"><div class="tw circ" style="left:28px;top:27px;width:96px;height:96px">'
             '<div class="pearl">%s</div></div><div class="t">Ви стежите</div></div>'
             '<div class="ck" id="ck4" style="left:470px;top:75px"></div>'
             '<div class="shc"><div class="sheen"></div></div></div></div>'
             % (g.mark("instagram"), stroke("check")))
    sfx("pop", T["yakshcho2"] + 0.04, -2)
    sfx("click", T["pidpysh"] + 0.02)
    return js("""
  tl.set("#gL", {autoAlpha: 1}, @yakshcho2-0.1);
  arr("#fl", @yakshcho2-0.02, {s: 0.6, y: 40});
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


# captions that would repeat the graphic's own words (STYLE.md §2b.1)
def span_words(a, b):
    return (round(a - 0.02, 3), round(b, 3), "")


BLACKOUT = [
    span_words(0.0, T["chesno"] - 0.03),                    # her Threads screenshot says it
    span_words(T["agi"], T["agie"]),                        # the AGI badge says it
    span_words(T["dyzain"], T["dyzaine"]),                  # the window title says Claude Design
    span_words(T["krashchyi"], T["krashchyie"]),            # the badge says «кращий»
]


def check_no_paint():
    """No beat may be on screen inside a closeup."""
    a, b = NO_PAINT[0]
    assert T["vypravyly"] < a, "sync beat runs into the closeup"
    assert T["ale2"] - 0.05 > b, "platforms arrive inside the closeup"


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
        title=u"Reel 26 — ChatGPT чи Claude",
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
