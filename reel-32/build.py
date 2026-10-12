# -*- coding: utf-8 -*-
"""Reel 32 — «Чому Claude пише не як ти». Posts 2026-10-13.

Raw take, cut by tools/cut.py (no closeups this time: no_paint is empty).
Refined glass (STYLE.md §0), sound design (tools/sfx.py).

The one object is **a skill**: one skill card that tries to be everything,
splits into one per format, gets trained on her content, and ends as her own
three skills fed by what actually worked.

Chain:  near: a consultation call, the client's tile speaks -> her speech
bubble becomes the text she rewrites in Claude (half of it struck, rewritten)
-> a magnifier reads it, it flips into ONE skill («1») -> four format chips
plug in (Рілси, YouTube, Сторіз, Уроки) -> each takes its own style, the cables
turn to sparks, the chips get crammed inside the one card -> it prints a text
that is neither fish nor meat -> the card splits into four, each gets its
format -> the Reels skill rises, a prompt bar types a description of her
style and deletes it («важко сформулювати») -> OVER: the iris opens out of the
send button: a wall of her content, run, a scan line reads it; methods / style
/ manner pull out of it as pills; they fold into a sheet of numbered rules
(«Правила») -> the iris closes onto the test text: it writes itself, she reads
it with a highlighter, «Окей»; the lines take her colour, Claude + her ->
near: a shelf of her three skills, ghost to lit (Клієнти, Контент, Лідмагніти)
-> her best posts (hearts) feed them; two random cards and a die are thrown
in and crossed out -> Стежити.

usage: python build.py   (then: python ../tools/sfx.py mix 32)
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

CUT = json.load(io.open(os.path.join(ROOT, "work", "r32", "cut.json"), encoding="utf-8"))
DUR = 61.483           # (1845 plate frames - 0.5) / 30
FPS = 30
k = Kit(width=1080, height=1920, fps=FPS, duration=DUR)
g = Glass(["claude", "instagram", "youtube"])
k.css(g.css())

NO_PAINT = [tuple(x) for x in CUT["no_paint"]]      # empty for this cut

# ---------------------------------------------------------------------------
# Captions: script spelling on her timing; whisper errors restored.
CAPS = k.load_captions(os.path.join(ROOT, "work", "r32", "captions.json"))
FIX = {u"якось": u"Якось", u"поштовічному": u"по штучному", u"ютуб,": u"YouTube,",
       u"рибані,": u"риба,", u"Потім": u"потім", u"Кожен": u"кожен"}
for c in CAPS:
    c["w"] = FIX.get(c["w"], c["w"])
# «нав» + «мене.» is whisper hearing «навмання.»
for i, c in enumerate(CAPS):
    if c["w"] == u"нав" and i + 1 < len(CAPS) and CAPS[i + 1]["w"] == u"мене.":
        c["w"] = u"навмання."
        c["e"] = CAPS[i + 1]["e"]
        del CAPS[i + 1]
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
    "konsult": S(u"консультацію", 1.11), "kliientka": S(u"клієнтка", 2.81), "skazala": S(u"сказала", 3.23),
    "perepys": S(u"переписую", 3.97), "claude": S("Claude", 4.68), "polovynu": S(u"половину", 5.04),
    "tekstu": S(u"тексту", 5.51), "podyv": S(u"подивилась", 6.71), "vyiav": S(u"виявилось", 7.72),
    "odyn": S(u"один", 8.70), "skil": S(u"скіл", 8.94),
    "rilsy": S(u"рілси", 9.75), "yutub": S("YouTube", 10.53), "storiz": S(u"сторіз", 11.15),
    "uroky": S(u"уроки", 11.67), "urokye": E(u"уроки", 11.67),
    "styli": S(u"стилі", 12.45), "rizni": S(u"різні", 13.25), "svar": S(u"сваряться", 14.44),
    "vseredyni": S(u"всередині", 15.38), "skilu": S(u"скілу", 16.16),
    "tekst": S(u"текст", 17.09), "ryba": S(u"риба", 18.59), "miaso": S(u"мясо", 19.07),
    "tomu2": S(u"Тому", 19.53), "okremoho": S(u"окремого", 21.34), "kozhen": S(u"кожен", 22.86),
    "format": S(u"формат", 23.24),
    "naikr": S(u"найкращий", 24.06), "navchyty": S(u"навчити", 24.86), "poiasn": S(u"пояснювати", 26.07),
    "vazhko": S(u"важко", 28.89), "sform": S(u"сформулювати", 29.15), "samii": S(u"самій", 29.81),
    "natomist": S(u"Натомість", 30.39), "zapusk": S(u"запускаєш", 30.91), "analiz": S(u"аналіз", 31.49),
    "kontentu": S(u"контенту", 32.83), "vytiah": S(u"витягує", 33.80), "metody": S(u"методи", 35.32),
    "styl2": S(u"стиль", 36.22), "maneru": S(u"манеру", 36.54), "spilke": E(u"спілкування", 36.78),
    "sam": S(u"сам", 37.66), "pyshe": S(u"пише", 38.65), "pravyla": S(u"правила", 39.02),
    "pravylae": E(u"правила", 39.02),
    "potim": S(u"потім", 40.02), "pyshe2": S(u"пише", 40.24), "testovyi": S(u"тестовий", 41.19),
    "tekst2e": E(u"текст", 41.69), "perevir": S(u"перевіряєш", 42.39), "okei": S(u"окей", 43.33),
    "okeie": E(u"окей", 43.33), "ivot": S(u"от", 44.03), "rozumiie": S(u"розуміє", 45.29),
    "same": S(u"саме", 46.21), "tebe": S(u"тебе", 46.65),
    "itak": S(u"так", 47.15), "vyishlo": S(u"вийшло", 47.65), "kilka": S(u"кілька", 48.15),
    "rozmovu": S(u"розмову", 49.64), "kliientamy": S(u"клієнтами", 50.05), "kliientamye": E(u"клієнтами", 50.05),
    "napys": S(u"написання", 51.05), "kontentu2": S(u"контенту", 51.55), "kontentu2e": E(u"контенту", 51.55),
    "lidm": S(u"лідмагніти", 52.43), "lidme": E(u"лідмагніти", 52.43),
    "kozhen2": S(u"кожен", 53.59), "navchenyi": S(u"навчений", 53.79), "tomu3": S(u"тому", 54.43),
    "naikrashche": S(u"найкраще", 55.42), "zaishlo": S(u"зайшло", 55.94), "ane": S(u"а", 56.54),
    "prykl": S(u"прикладів", 57.08), "kynula": S(u"кинула", 58.13), "navm": S(u"навмання", 58.53),
    "yakshcho": S(u"Якщо", 59.29), "pidpysh": S(u"підпишись", 60.85),
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
# Glyphs
STROKES = {
    "up": '<path d="M12 19.2V5.4M6.2 11l5.8-5.8 5.8 5.8"/>',
    "check": '<path d="M5.4 12.6l4.3 4.3 8.9-9.5"/>',
    "x": '<path d="M6.5 6.5l11 11M17.5 6.5l-11 11"/>',
    "person": '<circle cx="12" cy="8.2" r="3.6"/><path d="M4.8 20c.9-3.8 3.7-5.8 7.2-5.8s6.3 2 7.2 5.8"/>',
    "chat": '<path d="M7 4h10a2.5 2.5 0 0 1 2.5 2.5V13a2.5 2.5 0 0 1-2.5 2.5h-6l-4.3 3.6v-3.6A2.5 2.5 0 0 1 4.5 13V6.5A2.5 2.5 0 0 1 7 4z"/>',
    "pen": '<path d="M15.2 4.6l4.2 4.2L9 19.2H4.8V15z"/><path d="M12.8 7l4.2 4.2"/>',
    "magnet": '<path d="M5.5 4.5h4.4v7.6a2.1 2.1 0 0 0 4.2 0V4.5h4.4v7.6a6.5 6.5 0 0 1-13 0z"/><path d="M5.5 8.6h4.4M14.1 8.6h4.4"/>',
    "cap": '<path d="M2.5 9.5L12 5l9.5 4.5L12 14z"/><path d="M6.5 11.6v4.1c1.6 1.5 3.4 2.3 5.5 2.3s3.9-.8 5.5-2.3v-4.1M21.5 9.5v5"/>',
    "ring": '<circle cx="12" cy="12" r="8.6" stroke-dasharray="4.4 2.35"/><circle cx="12" cy="12" r="4.6"/>',
}
FILLS = {
    "fish": ('<path fill-rule="evenodd" d="M2.3 12c2.6-4 6.6-5.8 10.4-5.1 2.2.4 4 1.7 5.3 3.4l3.4-2.6v8.6l-3.4-2.6'
             'c-1.3 1.7-3.1 3-5.3 3.4C8.9 17.8 4.9 16 2.3 12zM8.2 10.5a1.3 1.3 0 1 0 0 2.6 1.3 1.3 0 1 0 0-2.6z"/>'),
    "meat": ('<path d="M15 2.8a6.2 6.2 0 0 1 4.4 10.6c-1.7 1.7-4 2.2-6.1 1.6l-3 3a2 2 0 1 1-2.6 2.4 2 2 0 1 1-2.4-2.6'
             'l3-3c-.6-2.1-.1-4.4 1.6-6.1A6.2 6.2 0 0 1 15 2.8z"/>'),
    "play": '<path d="M8 4.8v14.4c0 .8.9 1.3 1.6.9l11-7.2c.6-.4.6-1.3 0-1.7l-11-7.2C8.9 3.5 8 4 8 4.8z"/>',
    "heart": ('<path d="M12 20.3l-1.3-1.2C5.8 14.7 3 12.1 3 8.9 3 6.3 5 4.3 7.6 4.3c1.5 0 2.9.7 3.8 1.8h1.2'
              'c.9-1.1 2.3-1.8 3.8-1.8C19 4.3 21 6.3 21 8.9c0 3.2-2.8 5.8-7.7 10.2z"/>'),
}


def stroke(name, cls="sk"):
    return '<svg class="%s" viewBox="0 0 24 24">%s</svg>' % (cls, STROKES[name])


def fill(name, cls="fk"):
    return '<svg class="%s" viewBox="0 0 24 24">%s</svg>' % (cls, FILLS[name])


def tile(tid, size, x, y, material, inner, extra_cls="", hide=True, ring=True):
    r = ('<div class="sqring" id="%sR" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx"></div>'
         % (tid, x, y, size, size)) if ring else ""
    return ('%s<div class="tw%s %s" id="%s" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx">'
            '<div class="%s">%s<div class="sheen"></div></div></div>'
            % (r, " hide" if hide else "", extra_cls, tid, x, y, size, size, material, inner))


def xmark(xid, size, x, y):
    return ('<svg class="xm" id="%s" viewBox="0 0 24 24" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx">'
            '<path id="%sa" d="M5 5l14 14"/><path id="%sb" d="M19 5L5 19"/></svg>' % (xid, x, y, size, size, xid, xid))


k.css("""
.abs { position: absolute; }
.hide { opacity: 0; visibility: hidden; }
.tw { position: absolute; }
.sk { fill: none; stroke: url(#gw); stroke-width: 2.3; stroke-linecap: round; stroke-linejoin: round;
  width: 50%; height: 50%; position: relative; z-index: 1; overflow: visible; }
.pearl .sk { stroke: #17141c; }
.fk { fill: url(#gw); width: 56%; height: 56%; position: relative; z-index: 1; }
.pearl .fk { fill: #17141c; }
.circ .jelly, .circ .pearl, .circ .clear, .circ .sheen { border-radius: 50%; }
.shc { position: absolute; inset: 0; border-radius: inherit; overflow: hidden; pointer-events: none; }
.shc .sheen { mix-blend-mode: normal; opacity: 0.4; }
.xm { position: absolute; fill: none; stroke: #e0204b; stroke-width: 3.4; stroke-linecap: round; z-index: 4;
  overflow: visible; filter: drop-shadow(0 0 6px rgba(255,255,255,0.9)); }
.ck { position: absolute; width: 120px; height: 120px; margin: -60px 0 0 -60px; border-radius: 50%;
  border: 7px solid #ff6e9c; opacity: 0; visibility: hidden; z-index: 5; }
.aurs { position: absolute; left: -700px; top: -700px; width: 2480px; height: 3320px; pointer-events: none;
  background:
    radial-gradient(circle 526px at 1560px 880px, rgba(255,110,156,0.50), rgba(255,110,156,0)),
    radial-gradient(circle 634px at 760px 2360px, rgba(222,32,74,0.55), rgba(222,32,74,0)),
    radial-gradient(circle 382px at 1480px 1910px, rgba(255,198,214,0.20), rgba(255,198,214,0)); }

/* a white card (text, skills) */
.wc { position: absolute; border-radius: 48px; overflow: hidden; color: #17141c;
  background: linear-gradient(172deg, #ffffff 0%, #fff9fb 58%, #fdf0f4 100%);
  box-shadow: inset 0 2px 1px #fff, inset 0 -24px 44px -26px rgba(180,18,47,0.16),
              0 44px 90px -34px rgba(24,4,12,0.62), 0 0 0 1px rgba(255,255,255,0.4); }
.wc i { position: absolute; display: block; }
.hb { border-radius: 12px; background: linear-gradient(115deg, #c41434 0%, #8d0d24 100%); }
.rr { border-radius: 11px; background: rgba(23,20,28,0.13); }
.rk { border-radius: 11px; background: linear-gradient(115deg, #c41434 0%, #ff6e9c 100%); opacity: 0; visibility: hidden; }
.stk { height: 8px; border-radius: 4px; background: #c41434; transform-origin: 0 50%; transform: scaleX(0); }
.nr { border-radius: 11px; background: linear-gradient(115deg, #8d0d24 0%, #c41434 70%, #e0204b 100%);
  opacity: 0; visibility: hidden; }
.wc .ttl { position: absolute; font-weight: 700; letter-spacing: -0.02em; color: #17141c; line-height: 1; }
.wc .mic { position: absolute; font-size: 25px; font-weight: 700; letter-spacing: 0.16em; color: rgba(23,20,28,0.42); }

/* the call */
#call .hdr { position: absolute; left: 44px; top: 30px; height: 44px; display: flex; align-items: center; gap: 14px;
  font-size: 30px; font-weight: 700; color: rgba(255,255,255,0.85); letter-spacing: -0.005em; }
#call .rec { width: 16px; height: 16px; border-radius: 50%; background: #ff4d6d; box-shadow: 0 0 14px rgba(255,77,109,0.9); }
.pt { position: absolute; border-radius: 40px;
  background: linear-gradient(160deg, rgba(255,255,255,0.17) 0%, rgba(255,255,255,0.06) 100%);
  box-shadow: inset 0 1.5px 1px rgba(255,255,255,0.35); }
.pt .nm { position: absolute; left: 24px; bottom: 22px; height: 50px; padding: 0 22px; border-radius: 25px;
  background: rgba(10,4,8,0.45); color: #fff; font-size: 27px; font-weight: 700; line-height: 50px; }
.pt .spk { position: absolute; inset: 0; border-radius: 40px; opacity: 0; visibility: hidden;
  box-shadow: inset 0 0 0 6px #ff6e9c, 0 0 40px rgba(255,110,156,0.6); }

/* magnifier */
#mag .lens { position: absolute; left: 0; top: 0; width: 170px; height: 170px; border-radius: 50%;
  border: 15px solid #fff; background: radial-gradient(circle at 35% 30%, rgba(255,255,255,0.55), rgba(255,255,255,0.12) 60%);
  box-shadow: 0 24px 50px -18px rgba(24,4,12,0.6), inset 0 0 0 2px rgba(23,20,28,0.08); }
#mag .hdl { position: absolute; left: 142px; top: 150px; width: 104px; height: 30px; border-radius: 15px;
  background: linear-gradient(165deg, #e0204b 0%, #8d0d24 100%); transform: rotate(45deg); transform-origin: 0 50%;
  box-shadow: 0 16px 30px -12px rgba(70,4,20,0.6); }

/* a badge with a number */
.nb { position: absolute; border-radius: 50%; display: flex; align-items: center; justify-content: center;
  background: linear-gradient(165deg, #e0204b 0%, #ab112e 46%, #6b081c 100%); color: #fff; font-weight: 900;
  box-shadow: inset 0 2px 1px rgba(255,255,255,0.5), 0 18px 36px -12px rgba(70,4,20,0.7); }

/* format chips */
.chip2 { position: absolute; width: 250px; height: 100px; border-radius: 50px; }
.chip2 .base, .chip2 .alt { position: absolute; inset: 0; border-radius: 50px; display: flex; align-items: center;
  gap: 16px; padding-left: 26px; font-size: 36px; font-weight: 700; letter-spacing: -0.015em; }
.chip2 .base { color: #17141c; background: linear-gradient(160deg, #ffffff 0%, #fff5f8 52%, #f5dfe6 100%);
  box-shadow: inset 0 2px 1px #fff, 0 30px 56px -22px rgba(30,4,12,0.6); }
.chip2 .alt { opacity: 0; visibility: hidden; }
.chip2 svg { width: 54px; height: 54px; flex: none; }
.chip2 .base .mk2 { fill: #17141c; } .chip2 .base .sk { stroke: #17141c; width: 54px; height: 54px; stroke-width: 2.1; }
.chip2 .alt .mk2 { fill: #fff; } .chip2 .alt .sk { stroke: #fff; width: 54px; height: 54px; stroke-width: 2.1; }
.alt.s0 { color: #fff; background: linear-gradient(165deg, #e0204b 0%, #ab112e 46%, #6b081c 100%);
  font-weight: 900; box-shadow: inset 0 2px 1px rgba(255,255,255,0.5), 0 30px 56px -22px rgba(70,4,20,0.7); }
.alt.s1 { color: #fff; background: linear-gradient(160deg, #2a1f2a 0%, #17141c 100%); font-weight: 500;
  font-size: 34px; letter-spacing: 0.04em; box-shadow: inset 0 1.5px 0 rgba(255,255,255,0.16), 0 30px 56px -22px rgba(10,0,4,0.7); }
.alt.s2 { color: #fff; background: linear-gradient(160deg, #ff8ab0 0%, #ff5c8f 100%); font-weight: 900;
  font-size: 40px; box-shadow: inset 0 2px 1px rgba(255,255,255,0.6), 0 30px 56px -22px rgba(120,10,40,0.6); }
.alt.s3 { color: #b4122f; background: #fff7fa; font-weight: 400; font-style: italic; font-size: 38px;
  box-shadow: inset 0 0 0 5px #b4122f, 0 30px 56px -22px rgba(30,4,12,0.6); }
.alt.s3 .mk2 { fill: #b4122f; } .alt.s3 .sk { stroke: #b4122f; }
.zap { fill: none; stroke: #ffd6e3; stroke-width: 6; stroke-linecap: round; stroke-linejoin: round; }
.zapg { filter: drop-shadow(0 0 10px rgba(255,110,156,1)); }

.mk2 { width: 50%; height: 50%; position: relative; z-index: 1; fill: url(#gw); }
.pearl .mk2 { fill: #17141c; }

/* the prompt bar */
#pbT { position: absolute; left: 44px; top: 34px; width: 790px; font-size: 36px; font-weight: 500; line-height: 1.32;
  color: #fff; white-space: pre-wrap; }
#pbT::after { content: ""; display: inline-block; width: 3px; height: 40px; margin-left: 3px; vertical-align: -7px;
  background: #ff8ab0; }
.ghost { position: absolute; border-radius: 26px; border: 4px dashed rgba(23,20,28,0.18); }

/* the takeover */
.cc { position: absolute; width: 250px; height: 444px; border-radius: 34px; overflow: hidden;
  background: linear-gradient(172deg, #ffffff 0%, #fff6f9 100%);
  box-shadow: inset 0 2px 1px #fff, 0 40px 80px -30px rgba(8,0,3,0.7); }
.cc i { position: absolute; display: block; }
.cc .im { left: 0; top: 0; width: 250px; height: 316px; }
.cc .b1 { left: 22px; top: 342px; width: 180px; height: 22px; border-radius: 11px; background: rgba(23,20,28,0.16); }
.cc .b2 { left: 22px; top: 380px; width: 124px; height: 18px; border-radius: 9px; background: rgba(23,20,28,0.10); }
.cc .pl { left: 20px; top: 20px; width: 50px; height: 50px; border-radius: 50%; background: rgba(255,255,255,0.8); }
.cc .pl:after { content: ""; position: absolute; left: 19px; top: 14px; border-left: 17px solid #b4122f;
  border-top: 11px solid transparent; border-bottom: 11px solid transparent; }
.cc .lt { left: 0; top: 0; width: 250px; height: 444px; border-radius: 34px; opacity: 0; visibility: hidden;
  box-shadow: inset 0 0 0 7px #ff6e9c, inset 0 0 40px rgba(255,110,156,0.55); }
#scan { position: absolute; left: -40px; top: 0; width: 1160px; height: 12px; border-radius: 6px;
  background: linear-gradient(90deg, rgba(255,214,227,0) 0%, #ffe3ec 20%, #fff 50%, #ffe3ec 80%, rgba(255,214,227,0) 100%);
  box-shadow: 0 0 30px 10px rgba(255,110,156,0.75), 0 0 90px 30px rgba(255,110,156,0.35); }
.pill { position: absolute; height: 150px; border-radius: 75px; display: flex; align-items: center; justify-content: center;
  gap: 26px; font-size: 74px; font-weight: 700; letter-spacing: -0.025em; color: #17141c;
  background: linear-gradient(170deg, #ffffff 0%, #fff6f9 60%, #f8e6ec 100%);
  box-shadow: inset 0 2px 1px #fff, 0 50px 100px -30px rgba(8,0,3,0.8); }
.pill b { width: 30px; height: 30px; border-radius: 50%; display: block;
  background: linear-gradient(165deg, #e0204b 0%, #8d0d24 100%); }
.gpill { position: absolute; height: 150px; border-radius: 75px; border: 4px dashed rgba(255,255,255,0.4);
  background: rgba(255,255,255,0.06); }
.sheet .ttl2 { position: absolute; left: 64px; top: 92px; font-size: 104px; font-weight: 900; letter-spacing: -0.045em;
  line-height: 1.05; padding-right: 12px;
  background: linear-gradient(118deg, #7e0b20 0%, #b4122f 42%, #ff6e9c 100%);
  -webkit-background-clip: text; background-clip: text; color: transparent; }
.sheet .mic { position: absolute; left: 68px; top: 56px; font-size: 26px; font-weight: 700; letter-spacing: 0.16em;
  color: rgba(23,20,28,0.42); }
.sheet i { position: absolute; display: block; }
.rrow { position: absolute; left: 0; width: 900px; height: 110px; }
.rrow .nb { left: 64px; top: 10px; width: 72px; height: 72px; font-size: 38px; }
.rrow i { transform-origin: 0 50%; }

/* the test card */
.hl { border-radius: 10px; background: rgba(255,110,156,0.38); transform-origin: 0 50%; }
.yes { position: absolute; border-radius: 60px 60px 14px 60px; display: flex; align-items: center; justify-content: center;
  background: linear-gradient(165deg, #e0204b 0%, #ab112e 46%, #6b081c 100%); color: #fff; font-size: 58px; font-weight: 900;
  box-shadow: inset 0 2px 1px rgba(255,255,255,0.5), 0 30px 60px -20px rgba(70,4,20,0.7); }

/* her three skills */
.sc { position: absolute; width: 290px; height: 400px; border-radius: 46px; }
.sc .gh { position: absolute; inset: 0; border-radius: 46px; background: rgba(255,255,255,0.10);
  box-shadow: inset 0 0 0 3px rgba(255,255,255,0.35); }
.sc .gh .slot { position: absolute; left: 80px; top: 50px; width: 130px; height: 130px; border-radius: 30px;
  border: 4px dashed rgba(255,255,255,0.55); display: flex; align-items: center; justify-content: center; }
.sc .gh .slot .sk { stroke: rgba(255,255,255,0.55); stroke-width: 2; }
.sc .gh i { position: absolute; display: block; border-radius: 13px; background: rgba(255,255,255,0.32); }
.sc .on2 { position: absolute; inset: 0; border-radius: 46px; overflow: hidden; opacity: 0; visibility: hidden; filter: none;
  background: linear-gradient(172deg, #ffffff 0%, #fff8fa 58%, #fbe9ef 100%);
  box-shadow: inset 0 2px 1px #fff, 0 40px 80px -30px rgba(24,4,12,0.6); }
.sc .on2 .lb { position: absolute; left: 0; right: 0; top: 208px; text-align: center; font-size: 40px; font-weight: 700;
  letter-spacing: -0.02em; color: #17141c; }
.sc .on2 i { position: absolute; display: block; border-radius: 9px; background: rgba(23,20,28,0.13); height: 18px; }
.ps { position: absolute; width: 120px; height: 213px; border-radius: 22px;
  background: linear-gradient(172deg, #ffffff 0%, #fff6f9 100%);
  box-shadow: inset 0 2px 1px #fff, 0 26px 50px -20px rgba(24,4,12,0.65); }
.ps i { position: absolute; display: block; }
.ps .im { left: 0; top: 0; width: 120px; height: 150px; border-radius: 22px 22px 0 0; }
.ps .b1 { left: 14px; top: 166px; width: 84px; height: 12px; border-radius: 6px; background: rgba(23,20,28,0.16); }
.ps .b2 { left: 14px; top: 188px; width: 56px; height: 10px; border-radius: 5px; background: rgba(23,20,28,0.10); }
.ps.grey { background: linear-gradient(172deg, #f1eef0 0%, #e2dde0 100%); }
.ps.grey .im { background: linear-gradient(150deg, #cfc9cc 0%, #b8b1b5 100%); }
.dice { position: absolute; width: 130px; height: 130px; border-radius: 30px;
  background: linear-gradient(160deg, #ffffff 0%, #fff5f8 52%, #f5dfe6 100%);
  box-shadow: inset 0 2px 1px #fff, inset 0 -14px 24px -12px rgba(180,18,47,0.2), 0 30px 56px -20px rgba(30,4,12,0.6); }
.dice b { position: absolute; width: 24px; height: 24px; border-radius: 50%; background: #17141c; }

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


def mark2(name):
    g.mark(name)                     # register the symbol
    return '<svg class="mk2" viewBox="0 0 24 24"><use href="#i-%s" width="24" height="24"/></svg>' % name


# ===========================================================================
# A · the consultation — the client speaks, her words become the text in Claude
@beat
def a_call():
    def pt(pid, x, name):
        return ('<div class="pt" id="%s" style="left:%dpx;top:96px;width:404px;height:330px">'
                '<div class="tw circ" style="left:127px;top:62px;width:150px;height:150px"><div class="pearl">%s</div></div>'
                '<div class="nm">%s</div><div class="spk" id="%sS"></div></div>' % (pid, x, stroke("person"), name, pid))
    call = ('<div class="dglass edge hide" id="call" style="left:90px;top:140px;width:900px;height:460px">'
            '<div class="hdr"><b class="rec"></b>Консультація · ШІ</div>'
            + pt("pMe", 34, "Ruta") + pt("pCl", 462, "Клієнтка") + '</div>')
    rows, stk, nr = "", "", ""
    ws = (720, 664, 700, 560, 630)
    for i, w in enumerate(ws):
        y = 150 + i * 50
        rows += '<i class="rr r%d" style="left:44px;top:%dpx;width:%dpx;height:24px"></i>' % (i, y, w)
        if i >= 2:
            stk += '<i class="stk" id="st%d" style="left:34px;top:%dpx;width:%dpx"></i>' % (i, y + 8, w + 20)
            nr += '<i class="nr" id="nr%d" style="left:44px;top:%dpx;width:%dpx;height:24px"></i>' % (
                i, y, (690, 610, 520)[i - 2])
    txt = ('<div class="wc hide" id="txt" style="left:130px;top:150px;width:820px;height:420px;'
           'border-radius:52px 52px 14px 52px">'
           '<div class="tw hide" id="txC" style="left:40px;top:34px;width:92px;height:92px"><div class="jelly">%s</div></div>'
           '<i class="hb" style="left:44px;top:64px;width:300px;height:32px" id="txH"></i>%s%s%s'
           '<div class="shc"><div class="sheen"></div></div></div>' % (g.mark("claude"), rows, stk, nr))
    mag = '<div class="abs hide" id="mag" style="left:100px;top:200px;width:260px;height:260px"><div class="lens"></div><div class="hdl"></div></div>'
    L.append('<div class="g full" id="gA">' + call + txt + mag + '</div>')
    sfx("pop", 0.10, -2)
    sfx("ping", T["kliientka"] + 0.05, -3)
    sfx("pop", T["skazala"] + 0.05)
    sfx("pop", T["claude"] + 0.02, -2)
    sfx("click", T["polovynu"] + 0.05)
    sfx("whoosh-short", T["podyv"] + 0.02, -3)
    return js("""
  tl.set("#gA", {autoAlpha: 1}, 0);
  arr("#call", 0.06, {s: 0.82, y: 40, d: 0.8});
  tl.fromTo("#pClS", {autoAlpha: 0}, {autoAlpha: 1, duration: 0.2}, @kliientka);
  G.bump("#pCl", @kliientka);
  /* her words leave the client's tile and become a text */
  tl.to("#call", {scale: 0.9, autoAlpha: 0.3, y: 30, duration: 0.45, ease: "power2.inOut"}, @skazala);
  gsap.set("#txt", {transformOrigin: "90% 100%"});
  arr("#txt", @skazala+0.02, {s: 0.3, x: 200, y: 60, d: 0.8});
  tl.set("#call", {autoAlpha: 0}, @perepys+0.2);
  /* it is Claude's text: the tile lands, the heading slides over */
  tl.to("#txH", {x: 112, duration: 0.45, ease: SP}, @claude-0.12);
  arr("#txC", @claude-0.05, {s: 0.3, y: 0, d: 0.7});
  shn("#txt .sheen", @claude+0.2);
  /* half of it is struck and rewritten */
  [2, 3, 4].forEach(function (i, n) {
    tl.to("#st" + i, {scaleX: 1, duration: 0.22, ease: "power2.out"}, @polovynu+0.02 + n * 0.1);
    tl.to([".r" + i, "#st" + i], {x: -30, autoAlpha: 0, duration: 0.25, ease: "power2.in"}, @tekstu-0.05 + n * 0.08);
    tl.fromTo("#nr" + i, {autoAlpha: 0, x: 40, scaleX: 0.3, transformOrigin: "0% 50%"},
              {autoAlpha: 1, x: 0, scaleX: 1, duration: 0.5, ease: SP}, @tekstu+0.15 + n * 0.1);
  });
  /* she looks closer */
  tl.fromTo("#mag", {autoAlpha: 0, scale: 0.6, x: 0, y: 40}, {autoAlpha: 1, scale: 1, y: 0, duration: 0.2, ease: SP}, @podyv-0.05);
  tl.to("#mag", {x: 470, y: 60, duration: 0.85, ease: "power1.inOut"}, @podyv+0.15);
  tl.to("#mag", {autoAlpha: 0, scale: 0.8, duration: 0.2, ease: "power2.in"}, @vyiav-0.12);
  /* the text flips over: behind it there is ONE skill */
  tl.set("#txt", {transformOrigin: "50% 50%"}, @vyiav-0.04);
  tl.to("#txt", {scaleX: 0, duration: 0.17, ease: "power2.in"}, @vyiav-0.02);
  tl.set("#gA", {autoAlpha: 0}, @vyiav+0.2);""")


# ===========================================================================
# B · one skill for everything: four formats plug in, fight, get crammed
CH = [("c0", 30, 150, "instagram", u"Рілси"), ("c1", 30, 470, "youtube", "YouTube"),
      ("c2", 795, 150, "ring", u"Сторіз"), ("c3", 795, 470, "cap", u"Уроки")]
CAB = {"c0": "M280 200 C 330 200 310 320 350 320", "c1": "M280 520 C 330 520 310 420 350 420",
       "c2": "M795 200 C 745 200 770 320 730 320", "c3": "M795 520 C 745 520 770 420 730 420"}
ROT = {"c0": -6, "c1": 5, "c2": 4, "c3": -5}


def zig(x0, y0, x1, y1, n=7, a=16):
    pts = []
    for i in range(n + 1):
        t = i / float(n)
        x, y = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
        if 0 < i < n:
            dx, dy = (y1 - y0), -(x1 - x0)
            ln = (dx * dx + dy * dy) ** 0.5
            s = a if i % 2 else -a
            x, y = x + dx / ln * s, y + dy / ln * s
        pts.append("%d %d" % (x, y))
    return "M" + " L".join(pts)


ZAP = {"c0": zig(280, 200, 350, 320), "c1": zig(280, 520, 350, 420),
       "c2": zig(795, 200, 730, 320), "c3": zig(795, 520, 730, 420)}


@beat
def b_one_skill():
    def glyph(m):
        return mark2(m) if m in ("instagram", "youtube") else stroke(m)
    chips = ""
    for i, (cid, x, y, m, w) in enumerate(CH):
        chips += ('<div class="chip2 hide" id="%s" style="left:%dpx;top:%dpx">'
                  '<div class="base">%s<span>%s</span></div>'
                  '<div class="alt s%d" id="%sA">%s<span>%s</span></div></div>'
                  % (cid, x, y, glyph(m), w, i, cid, glyph(m), w))
    cab = '<svg class="cab abs" width="1080" height="700" viewBox="0 0 1080 700" style="left:0;top:0">'
    for cid, d in CAB.items():
        cab += ('<path class="tube hide cb" id="%sT" d="%s"/><path class="core hide cb" id="%sK" d="%s"/>'
                % (cid, d, cid, d))
    cab += '<g class="zapg">' + "".join('<path class="zap" id="%sZ" style="opacity:0" d="%s"/>' % (c, d)
                                        for c, d in ZAP.items()) + '</g></svg>'
    cram = "".join('<div class="tw" style="left:%dpx;top:%dpx;width:76px;height:76px;transform:rotate(%ddeg)">'
                   '<div class="pearl">%s</div></div>' % (x, y, r, inner)
                   for x, y, r, inner in ((40, 120, -14, mark2("instagram")), (112, 134, 9, mark2("youtube")),
                                          (186, 116, -6, stroke("ring")), (258, 132, 12, stroke("cap"))))
    sk1 = ('<div class="wc hide" id="sk1" style="left:350px;top:240px;width:380px;height:260px">'
           '<div class="tw" style="left:30px;top:28px;width:74px;height:74px"><div class="jelly">%s</div></div>'
           '<div class="ttl" style="left:124px;top:42px;font-size:50px">Скіл</div>'
           '<div id="skRows"><i class="rr" style="left:34px;top:130px;width:300px;height:20px"></i>'
           '<i class="rr" style="left:34px;top:168px;width:248px;height:20px"></i>'
           '<i class="rr" style="left:34px;top:206px;width:190px;height:20px"></i></div>'
           '<div class="abs hide" id="cram" style="left:0;top:0;width:380px;height:260px">%s</div>'
           '<div class="shc"><div class="sheen"></div></div></div>' % (g.mark("claude"), cram))
    one = '<div class="nb hide" id="one" style="left:672px;top:196px;width:100px;height:100px;font-size:60px">1</div>'
    # the text it prints: neither fish nor meat
    out = ('<div class="wc hide" id="out" style="left:250px;top:330px;width:580px;height:250px;border-radius:40px">'
           '<i class="hb" style="left:36px;top:34px;width:380px;height:34px;border-radius:12px"></i>'
           '<i style="left:36px;top:92px;width:470px;height:16px;border-radius:8px;background:rgba(23,20,28,0.16)"></i>'
           '<i style="left:36px;top:124px;width:300px;height:28px;border-radius:9px;background:#ff8ab0"></i>'
           '<i style="left:350px;top:128px;width:160px;height:18px;border-radius:9px;background:rgba(23,20,28,0.30)"></i>'
           '<i style="left:36px;top:172px;width:420px;height:12px;border-radius:6px;background:rgba(180,18,47,0.45)"></i>'
           '<i style="left:36px;top:200px;width:210px;height:22px;border-radius:11px;background:rgba(23,20,28,0.22)"></i>'
           '</div>')
    fm = (tile("fish", 150, 70, 380, "pearl", fill("fish"), extra_cls="fm")
          + tile("xf", 66, 178, 352, "jelly", stroke("x"), extra_cls="circ", ring=False)
          + tile("meat", 150, 860, 380, "pearl", fill("meat"), extra_cls="fm")
          + tile("xmt", 66, 968, 352, "jelly", stroke("x"), extra_cls="circ", ring=False))
    L.append('<div class="g full" id="gB">' + cab + sk1 + one + chips + out + fm + '</div>')
    for key in ("rilsy", "yutub", "storiz", "uroky"):
        sfx("click-soft", T[key] + 0.03)
    sfx("whoosh-short", T["svar"] + 0.02)
    sfx("pop", T["ryba"] + 0.02)
    sfx("pop", T["miaso"] + 0.02)
    cj = []
    for i, (cid, x, y, m, w) in enumerate(CH):
        word = ("rilsy", "yutub", "storiz", "uroky")[i]
        cx, cy = x + 125, y + 50
        cj.append('arr("#%s", @%s-0.06, {s: 0.4, x: %d, y: %d, d: 0.75});' % (cid, word, (540 - cx) // 3, (370 - cy) // 3))
        cj.append('tl.set(["#%sT", "#%sK"], {autoAlpha: 1}, @%s+0.05); draw2("%sT", @%s+0.05, 0.35); draw2("%sK", @%s+0.05, 0.35);'
                  % (cid, cid, word, cid, word, cid, word))
        cj.append('tl.fromTo("#%sA", {autoAlpha: 0}, {autoAlpha: 1, duration: 0.25}, @rizni-0.1+%.2f);' % (cid, i * 0.1))
        cj.append('tl.set("#%s .base", {autoAlpha: 0}, @rizni+0.16+%.2f);' % (cid, i * 0.1))
        cj.append('tl.to("#%s", {rotation: %d, duration: 0.5, ease: SP}, @rizni-0.1+%.2f);' % (cid, ROT[cid], i * 0.1))
        cj.append('G.haptic("#%s", @svar+%.2f);' % (cid, 0.05 + i * 0.07))
        cj.append('tl.to("#%s", {x: %d, y: %d, rotation: %d, scale: 0.25, autoAlpha: 0, duration: 0.5, ease: "power3.in"}, @vseredyni+%.2f);'
                  % (cid, 540 - cx, 370 - cy, ROT[cid] * 4, i * 0.06))
    return js("""
  tl.set("#gB", {autoAlpha: 1}, @vyiav+0.1);
  tl.fromTo("#sk1", {autoAlpha: 0, scaleX: 0, scaleY: 1.25}, {autoAlpha: 1, scaleX: 1, scaleY: 1, duration: 0.55, ease: SP}, @vyiav+0.14);
  shn("#sk1 .sheen", @vyiav+0.4);
  arr("#one", @odyn-0.04, {s: 0.2, y: 20, d: 0.6});
  {{chips}}
  /* they fight: the cables turn to sparks, the card shakes */
  tl.to(".cb", {autoAlpha: 0, duration: 0.15}, @svar);
  ["c0Z", "c1Z", "c2Z", "c3Z"].forEach(function (id, i) { tl.set("#" + id, {opacity: 1}, @svar+i*0.05); draw2(id, @svar+i*0.05, 0.22); });
  G.haptic("#sk1", @svar+0.15); G.haptic("#sk1", @svar+0.6);
  tl.to(["#c0Z", "#c1Z", "#c2Z", "#c3Z"], {opacity: 0, duration: 0.2}, @vseredyni+0.1);
  /* ... inside one skill */
  tl.to("#skRows", {autoAlpha: 0, duration: 0.2}, @vseredyni+0.35);
  tl.fromTo("#cram", {autoAlpha: 0, scale: 0.6}, {autoAlpha: 1, scale: 1, duration: 0.45, ease: POP}, @vseredyni+0.38);
  tl.to("#sk1", {scale: 1.08, duration: 0.12, ease: "power2.out"}, @vseredyni+0.4);
  tl.to("#sk1", {scale: 1, duration: 0.5, ease: SP}, @vseredyni+0.52);
  G.haptic("#sk1", @skilu+0.05);
  /* it prints a text — neither fish nor meat */
  bout("#one", @tekst-0.3, 8, 0.25);
  tl.to("#sk1", {y: -110, scale: 0.72, duration: 0.55, ease: SP}, @tekst-0.1);
  gsap.set("#out", {transformOrigin: "50% 0%"});
  tl.fromTo("#out", {autoAlpha: 0, y: -140, scaleY: 0.2}, {autoAlpha: 1, y: 0, scaleY: 1, duration: 0.7, ease: SP}, @tekst+0.15);
  arr("#fish", @ryba-0.08, {s: 0.4, x: 40, y: 0, d: 0.6}); G.ripple("#fishR", @ryba+0.15);
  arr("#xf", @ryba+0.22, {s: 0.2, y: 0, d: 0.5});
  arr("#meat", @miaso-0.08, {s: 0.4, x: -40, y: 0, d: 0.6}); G.ripple("#meatR", @miaso+0.15);
  arr("#xmt", @miaso+0.2, {s: 0.2, y: 0, d: 0.5});
  bout(["#out", "#fish", "#meat", "#xf", "#xmt"], @tomu2-0.02, 10, 0.3);
  /* back to the one card ... */
  tl.to("#cram", {autoAlpha: 0, scale: 0.7, duration: 0.3, ease: "power2.in"}, @tomu2+0.05);
  tl.to("#skRows", {autoAlpha: 1, duration: 0.3}, @tomu2+0.3);
  tl.to("#sk1", {y: 0, scale: 1, duration: 0.65, ease: SP}, @tomu2+0.1);
  tl.set("#sk1", {autoAlpha: 0}, @okremoho+0.02);
  tl.set("#gB", {autoAlpha: 0}, @okremoho+0.3);""").replace("{{chips}}", js("\n  ".join(cj)))


# ===========================================================================
# C · … splits into one skill per format; the Reels skill rises; she tries to
#     describe her style in words and deletes it
GC = [("g0", 55, "instagram", u"Рілси"), ("g1", 305, "youtube", "YouTube"),
      ("g2", 555, "ring", u"Сторіз"), ("g3", 805, "cap", u"Уроки")]
PROMPT = (u"Пиши легко, але не просто. З гумором, але без клоунади. "
          u"Коротко, але щоб усе було зрозуміло. І щоб звучало як я, але")


@beat
def c_split():
    cards = ""
    for cid, x, m, w in GC:
        inner = mark2(m) if m in ("instagram", "youtube") else stroke(m)
        cards += ('<div class="wc hide" id="%s" style="left:%dpx;top:250px;width:220px;height:240px;border-radius:40px">'
                  '<div class="tw" style="left:20px;top:20px;width:54px;height:54px"><div class="jelly">%s</div></div>'
                  '<div class="ttl" style="left:88px;top:30px;font-size:34px">Скіл</div>'
                  '<div class="ghost" style="left:66px;top:92px;width:88px;height:88px"></div>'
                  '<div class="tw hide fmt" id="%sM" style="left:66px;top:92px;width:88px;height:88px"><div class="jelly">%s</div></div>'
                  '<div class="ttl hide fmtL" id="%sL" style="left:0;right:0;top:194px;text-align:center;font-size:30px">%s</div>'
                  '</div>' % (cid, x, g.mark("claude"), cid, inner, cid, w))
    bar = ('<div class="dglass edge hide" id="pb" style="left:60px;top:300px;width:960px;height:270px;border-radius:56px">'
           '<div id="pbT"></div>'
           '<div class="tw circ" id="pbS" style="left:846px;top:156px;width:84px;height:84px"><div class="jelly">%s</div></div>'
           '</div>' % stroke("up"))
    L.append('<div class="g full" id="gC">' + cards + bar + '</div>')
    sfx("whoosh-short", T["okremoho"] + 0.02)
    sfx("typing", T["poiasn"] + 0.05, -1)
    return js("""
  tl.set("#gC", {autoAlpha: 1}, @okremoho-0.02);
  [["#g0", 375], ["#g1", 125], ["#g2", -125], ["#g3", -375]].forEach(function (p, i) {
    tl.fromTo(p[0], {autoAlpha: 0.9, x: p[1], scale: 1.4}, {autoAlpha: 1, x: 0, scale: 1, duration: 0.8, ease: POP}, @okremoho+0.02+i*0.04);
  });
  ["g0", "g1", "g2", "g3"].forEach(function (c, i) {
    tl.fromTo("#" + c + "M", {autoAlpha: 0, y: -50, scale: 0.5}, {autoAlpha: 1, y: 0, scale: 1, duration: 0.55, ease: POP}, @kozhen+i*0.1);
    tl.fromTo("#" + c + "L", {autoAlpha: 0, y: 12}, {autoAlpha: 1, y: 0, duration: 0.3, ease: "power2.out"}, @kozhen+0.12+i*0.1);
  });
  /* the Reels skill stays: how do you teach it? */
  bout(["#g1", "#g2", "#g3"], @naikr-0.05, 10, 0.3);
  tl.to("#g0", {x: 375, y: -190, scale: 0.8, duration: 0.75, ease: SP}, @naikr);
  arr("#pb", @navchyty-0.15, {s: 0.85, y: 50, d: 0.75});
  G.haptic("#pb", @samii);
  G.bump("#pbS", @natomist-0.12);""")


# ===========================================================================
# TK · OVER: the iris opens out of «send»: her content, run, scan; methods /
#      style / manner pull out; they fold into a sheet of rules
GRID_IMS = [
    "linear-gradient(150deg,#f4dfe5 0%,#ecc8d0 100%)", "linear-gradient(150deg,#e0204b 0%,#6b081c 100%)",
    "linear-gradient(150deg,#ffd6e3 0%,#ff8ab0 100%)", "linear-gradient(150deg,#2a1f2a 0%,#5a1a2c 100%)",
]


@beat
def t_takeover():
    cards = ""
    for r in range(4):
        for c in range(4):
            n = r * 4 + c
            im = GRID_IMS[(r + c * 3) % 4]
            cards += ('<div class="cc" id="cc%d" style="left:%dpx;top:%dpx"><i class="im" style="background:%s"></i>'
                      '%s<i class="b1"></i><i class="b2"></i><i class="lt" id="lt%d"></i></div>'
                      % (n, c * 276, r * 470, im, '<i class="pl"></i>' if (r + c) % 2 == 0 else "", n))
    grid = ('<div class="abs" id="grid" data-layout-allow-overflow style="left:-14px;top:-150px;width:1104px;'
            'height:1880px">%s</div>' % cards)
    run = tile("run", 230, 425, 560, "jelly", fill("play"), extra_cls="circ")
    pills = ""
    for pid, x, y, w, word in (("p0", 320, 380, 440, u"Методи"), ("p1", 350, 570, 380, u"Стиль"),
                               ("p2", 90, 760, 900, u"Манера спілкування")):
        pills += ('<div class="gpill hide" id="%sG" style="left:%dpx;top:%dpx;width:%dpx"></div>'
                  '<div class="pill hide" id="%s" style="left:%dpx;top:%dpx;width:%dpx"><b></b>%s</div>'
                  % (pid, x, y, w, pid, x, y, w, word))
    rows = ""
    for i, (w1, w2) in enumerate(((640, 420), (590, 470), (660, 360), (540, 440), (610, 300))):
        y = 260 + i * 130
        rows += ('<div class="rrow" style="top:%dpx"><div class="nb rn" id="rn%d">%d</div>'
                 '<i class="hb rb" id="rb%d" style="left:166px;top:14px;width:%dpx;height:30px"></i>'
                 '<i class="rr rb" id="rc%d" style="left:166px;top:60px;width:%dpx;height:20px"></i></div>'
                 % (y, i, i + 1, i, w1, i, w2))
    sheet = ('<div class="sheet hide" id="rules" style="left:90px;top:200px;width:900px;height:980px">'
             '<div class="mic">СКІЛ · РІЛСИ</div><div class="ttl2" id="rT">Правила</div>%s'
             '<div class="sheen"></div></div>' % rows)
    L.append('<div class="g full" id="gT"><div class="tkg"></div><div class="aurs"></div>'
             + grid + '<div class="abs hide" id="scan"></div><div class="grain"></div>'
             + run + pills + sheet + '</div>')
    sfx("whoosh-short", T["natomist"] - 0.02)
    sfx("click", T["zapusk"] + 0.1)
    sfx("whoosh-short", T["analiz"] + 0.02, -4)
    sfx("click-soft", T["metody"] + 0.02)
    sfx("click-soft", T["styl2"] + 0.02)
    sfx("pop", T["sam"] + 0.02)
    sfx("whoosh-short", T["pravylae"] + 0.02, -2)
    # scan: each card lights as the line passes its (rotated) centre
    lit = []
    t0, t1, y0, y1 = T["analiz"] + 0.02, T["kontentu"] + 0.6, 40.0, 1340.0
    import math
    a = math.radians(-6)
    for r in range(4):
        for c in range(4):
            lx, ly = c * 276 + 125 - 552, r * 470 + 222 - 940     # relative to the grid centre
            yy = -150 + 940 + lx * math.sin(a) + ly * math.cos(a)
            if y0 < yy < y1:
                tt = t0 + (yy - y0) / (y1 - y0) * (t1 - t0)
                lit.append('tl.fromTo("#lt%d", {autoAlpha: 0}, {autoAlpha: 1, duration: 0.18}, %.3f);' % (r * 4 + c, tt))
    return js("""
  gsap.set("#grid", {rotation: -6});
  G.irisOpen("#gT", @natomist-0.04, 948, 498, 0.6);
  drift1("#gT", @natomist, @pravylae-@natomist);
  tl.set("#gC", {autoAlpha: 0}, @natomist+0.6);
  tl.fromTo("#grid", {scale: 1.12}, {scale: 1, duration: 1.4, ease: "power2.out"}, @natomist-0.04);
  arr("#run", @zapusk-0.3, {s: 0.4, y: 0, d: 0.6});
  tl.to("#run", {scale: 0.88, duration: 0.09, ease: "power2.out"}, @zapusk+0.1);
  tl.to("#run", {scale: 1, duration: 0.4, ease: SP}, @zapusk+0.19);
  G.ripple("#runR", @zapusk+0.12);
  bout("#run", @analiz-0.12, 10, 0.25);
  tl.set("#scan", {autoAlpha: 1, y: {{y0}}}, @analiz);
  tl.to("#scan", {y: {{y1}}, duration: {{sd}}, ease: "none"}, @analiz+0.02);
  tl.set("#scan", {autoAlpha: 0}, @kontentu+0.65);
  {{lit}}
  /* it pulls the essentials out of the content */
  tl.to("#grid", {scale: 0.9, autoAlpha: 0.28, duration: 0.6, ease: "power2.inOut"}, @vytiah-0.05);
  arr(["#p0G", "#p1G", "#p2G"], @vytiah+0.05, {s: 0.85, y: 20, d: 0.6});
  [["#p0", @metody], ["#p1", @styl2], ["#p2", @maneru]].forEach(function (p) {
    tl.set(p[0] + "G", {autoAlpha: 0}, p[1] + 0.12);
    arr(p[0], p[1]-0.06, {s: 0.5, y: 160, d: 0.7});
  });
  /* … and writes itself the rules */
  tl.to(["#p0", "#p1", "#p2"], {y: 160, scale: 0.6, autoAlpha: 0, duration: 0.3, ease: "power2.in", stagger: 0.05}, @sam-0.12);
  arr("#rules", @sam, {s: 0.7, y: 120, d: 0.85});
  gsap.set(".rb", {scaleX: 0});
  [0, 1, 2, 3, 4].forEach(function (i) {
    tl.fromTo("#rn" + i, {autoAlpha: 0, scale: 0.3}, {autoAlpha: 1, scale: 1, duration: 0.45, ease: POP}, @pyshe-0.35 + i * 0.11);
    tl.to("#rb" + i, {scaleX: 1, duration: 0.4, ease: "power2.out"}, @pyshe-0.3 + i * 0.11);
    tl.to("#rc" + i, {scaleX: 1, duration: 0.4, ease: "power2.out"}, @pyshe-0.22 + i * 0.11);
  });
  tl.fromTo("#rT", {clipPath: "inset(0% 100% 0% 0%)"}, {clipPath: "inset(0% 0% 0% 0%)", duration: 0.45, ease: "power2.out"}, @pravyla-0.02);
  shn("#rules .sheen", @pravyla+0.2);
  G.irisClose("#gT", @pravylae+0.02, 540, 380, 0.5);""").replace("{{lit}}", "\n  ".join(lit)).replace(
        "{{y0}}", "%d" % y0).replace("{{y1}}", "%d" % y1).replace("{{sd}}", "%.3f" % (t1 - t0))


# ===========================================================================
# D · the test text: written, read with a highlighter, «Окей»; it becomes hers
@beat
def d_test():
    ws = (760, 700, 742, 610, 680, 420)
    rows = ""
    for i, w in enumerate(ws):
        y = 140 + i * 46
        if i < 4:
            rows += '<i class="hl" id="hl%d" style="left:30px;top:%dpx;width:%dpx;height:36px;transform:scaleX(0)"></i>' % (i, y - 6, w + 20)
        rows += ('<i class="rr tr" id="tr%d" style="left:40px;top:%dpx;width:%dpx;height:22px"></i>'
                 '<i class="rk" id="tk%d" style="left:40px;top:%dpx;width:%dpx;height:22px"></i>' % (i, y, w, i, y, w))
    card = ('<div class="wc hide" id="tc" style="left:110px;top:160px;width:860px;height:420px;border-radius:52px">'
            + tile("tcC", 80, 36, 30, "jelly", g.mark("claude"), hide=False)
            + '<div class="mic" style="left:136px;top:56px">ТЕСТОВИЙ ТЕКСТ</div>'
            + tile("you", 80, 700, 30, "pearl", stroke("person"), extra_cls="circ", ring=False)
            + '<div class="nb hide" id="tick" style="left:762px;top:20px;width:46px;height:46px">'
              '<svg viewBox="0 0 24 24" style="width:30px;height:30px;fill:none;stroke:#fff;stroke-width:3.2;'
              'stroke-linecap:round;stroke-linejoin:round"><path d="M5.4 12.6l4.3 4.3 8.9-9.5"/></svg></div>'
            + rows + '<div class="shc"><div class="sheen"></div></div></div>')
    ok = '<div class="yes hide" id="ok" style="left:700px;top:500px;width:250px;height:122px">Окей</div>'
    L.append('<div class="g full" id="gD">' + card + ok + '</div>')
    sfx("pop", T["okei"] + 0.02)
    sfx("sparkle", T["rozumiie"] + 0.05)
    return js("""
  tl.set("#gD", {autoAlpha: 1}, @pravylae+0.3);
  arr("#tc", @pravylae+0.36, {s: 0.4, y: 20, d: 0.8});
  gsap.set(".tr", {scaleX: 0, transformOrigin: "0% 50%"});
  [0, 1, 2, 3, 4, 5].forEach(function (i) { tl.to("#tr" + i, {scaleX: 1, duration: 0.3, ease: "power1.out"}, @pyshe2+0.3 + i * 0.2); });
  [0, 1, 2, 3].forEach(function (i) { tl.to("#hl" + i, {scaleX: 1, duration: 0.24, ease: "power1.inOut"}, @perevir-0.05 + i * 0.22); });
  arr("#ok", @okei-0.05, {s: 0.3, x: 40, y: 40, d: 0.7});
  bout("#ok", @ivot+0.15, 10, 0.25);
  tl.to(["#hl0", "#hl1", "#hl2", "#hl3"], {autoAlpha: 0, duration: 0.3}, @ivot+0.2);
  /* now it writes the way she does */
  G.bump("#tcC", @rozumiie-0.02); G.ripple("#tcCR", @rozumiie);
  [0, 1, 2, 3, 4, 5].forEach(function (i) { tl.fromTo("#tk" + i, {autoAlpha: 0}, {autoAlpha: 1, duration: 0.3}, @rozumiie+0.05 + i * 0.07); });
  shn("#tc .sheen", @rozumiie+0.25);
  arr("#you", @same-0.05, {s: 0.3, x: -40, y: 0, d: 0.65});
  arr("#tick", @tebe-0.02, {s: 0.2, y: 0, d: 0.55});
  bout("#gD", @itak-0.08, 10, 0.3);""")


# ===========================================================================
# E · her three skills, fed by what worked — not by random examples
SC = [("s0", 30, "chat", u"Клієнти", "kliientamy"), ("s1", 350, "pen", u"Контент", "napys"),
      ("s2", 670, "magnet", u"Лідмагніти", "lidm")]
POSTS = [(80, 0), (280, 0), (480, 1), (680, 2), (880, 2)]     # left, which skill it feeds
SC_CX = {0: 335, 1: 540, 2: 745}


@beat
def e_skills():
    cards = ""
    for sid, x, glyph, label, _ in SC:
        cards += ('<div class="sc" id="%s" style="left:%dpx;top:35px">'
                  '<div class="gh"><div class="slot">%s</div>'
                  '<i style="left:65px;top:222px;width:160px;height:28px"></i>'
                  '<i style="left:75px;top:280px;width:140px;height:18px"></i>'
                  '<i style="left:95px;top:312px;width:100px;height:18px"></i></div>'
                  '<div class="on2" id="%sL">'
                  '<div class="tw" style="left:80px;top:50px;width:130px;height:130px"><div class="jelly">%s<div class="sheen"></div></div></div>'
                  '<div class="lb">%s</div>'
                  '<i style="left:55px;top:280px;width:180px"></i><i style="left:80px;top:312px;width:130px"></i>'
                  '</div></div>' % (sid, x, stroke(glyph), sid, stroke(glyph), label))
    shelf = ('<div class="shelf edge hide" id="shE" style="left:45px;top:130px;width:990px;height:470px">%s</div>'
             % cards)
    posts = ""
    for i, (x, _) in enumerate(POSTS):
        im = GRID_IMS[i % 4]
        posts += ('<div class="ps hide" id="ps%d" style="left:%dpx;top:405px"><i class="im" style="background:%s"></i>'
                  '<i class="b1"></i><i class="b2"></i></div>' % (i, x, im))
        posts += tile("ht%d" % i, 58, x + 82, 386, "jelly", fill("heart"), extra_cls="circ", ring=False)
    rnd = ('<div class="ps grey hide" id="rd0" style="left:330px;top:405px"><i class="im"></i><i class="b1"></i><i class="b2"></i></div>'
           + xmark("xr0", 90, 345, 470)
           + '<div class="ps grey hide" id="rd1" style="left:630px;top:405px"><i class="im"></i><i class="b1"></i><i class="b2"></i></div>'
           + xmark("xr1", 90, 645, 470))
    pips = "".join('<b style="left:%dpx;top:%dpx"></b>' % (x, y)
                   for x, y in ((26, 26), (80, 26), (53, 53), (26, 80), (80, 80)))
    dice = '<div class="dice hide" id="dice" style="left:475px;top:445px">%s</div>' % pips
    L.append('<div class="g full" id="gE">' + shelf + posts + rnd + dice + '</div>')
    sfx("pop", T["rozmovu"] + 0.02)
    sfx("pop", T["napys"] + 0.02)
    sfx("pop", T["lidm"] + 0.02)
    sfx("whoosh-short", T["zaishlo"] + 0.02, -2)
    sfx("click", T["kynula"] + 0.05)
    lit = []
    for i, (sid, _, _, _, word) in enumerate(SC):
        lit.append('tl.fromTo("#%sL", {autoAlpha: 0, scale: 0.86}, {autoAlpha: 1, scale: 1, duration: 0.55, ease: POP}, @%s-0.05);'
                   % (sid, word if i else "rozmovu"))
        lit.append('shn("#%sL .sheen", @%s+0.25);' % (sid, word if i else "rozmovu"))
    feed = []
    for i, (x, s) in enumerate(POSTS):
        feed.append('tl.to(["#ps%d", "#ht%d"], {x: %d, y: -281, scale: 0.2, autoAlpha: 0, duration: 0.45, ease: "power3.in"}, @zaishlo+%.2f);'
                    % (i, i, SC_CX[s] - (x + 60), 0.04 * i))
    return js("""
  tl.set("#gE", {autoAlpha: 1}, @itak-0.05);
  arr("#shE", @vyishlo-0.1, {s: 0.8, y: 40});
  tl.fromTo(".sc .gh", {autoAlpha: 0, scale: 0.8}, {autoAlpha: 1, scale: 1, duration: 0.5, ease: POP, stagger: 0.09}, @kilka-0.05);
  {{lit}}
  /* each one learned on what actually worked */
  gsap.set("#shE", {transformOrigin: "50% 0%"});
  tl.to("#shE", {y: -50, scale: 0.64, duration: 0.7, ease: SP}, @navchenyi-0.1);
  [0, 1, 2, 3, 4].forEach(function (i) { arr("#ps" + i, @tomu3-0.1 + i * 0.07, {s: 0.5, y: 40, d: 0.7}); });
  [0, 1, 2, 3, 4].forEach(function (i) { arr("#ht" + i, @naikrashche-0.04 + i * 0.07, {s: 0.2, y: 10, d: 0.55}); });
  {{feed}}
  ["#s0", "#s1", "#s2"].forEach(function (s, i) { G.bump(s, @zaishlo+0.42 + i * 0.05); });
  /* … not on a couple of examples thrown in at random */
  tl.fromTo("#rd0", {autoAlpha: 0, x: 420, rotation: 30}, {autoAlpha: 1, x: 0, rotation: -8, duration: 0.6, ease: SP}, @ane+0.1);
  tl.fromTo("#rd1", {autoAlpha: 0, x: 300, rotation: 40}, {autoAlpha: 1, x: 0, rotation: 7, duration: 0.6, ease: SP}, @prykl);
  tl.fromTo("#dice", {autoAlpha: 0, x: 520, y: -60, rotation: 0}, {autoAlpha: 1, x: 0, y: 0, rotation: -540, duration: 0.75, ease: "power3.out"}, @kynula-0.05);
  draw2("xr0a", @navm+0.05, 0.14); draw2("xr0b", @navm+0.16, 0.14);
  draw2("xr1a", @navm+0.12, 0.14); draw2("xr1b", @navm+0.23, 0.14);
  tl.to(["#rd0", "#xr0a", "#xr0b"], {y: 240, rotation: -30, autoAlpha: 0, duration: 0.4, ease: "power2.in"}, @navm+0.42);
  tl.to(["#rd1", "#xr1a", "#xr1b"], {y: 240, rotation: 30, autoAlpha: 0, duration: 0.4, ease: "power2.in"}, @navm+0.47);
  bout(["#dice", "#shE"], @yakshcho-0.2, 10, 0.28);
  tl.set("#gE", {autoAlpha: 0}, @yakshcho+0.2);""").replace("{{lit}}", js("\n  ".join(lit))).replace(
        "{{feed}}", js("\n  ".join(feed)))


# ===========================================================================
# F · Стежити
@beat
def f_follow():
    L.append('<div class="g full" id="gF"><div class="fl hide" id="fl" style="left:190px;top:300px;width:700px;height:150px">'
             '<div class="tw circ" style="left:28px;top:27px;width:96px;height:96px"><div class="jelly">%s</div></div>'
             '<div class="t" id="flT">Стежити</div>'
             '<div class="on" id="flOn"><div class="tw circ" style="left:28px;top:27px;width:96px;height:96px">'
             '<div class="pearl">%s</div></div><div class="t">Ви стежите</div></div>'
             '<div class="ck" id="ck4" style="left:470px;top:75px"></div>'
             '<div class="shc"><div class="sheen"></div></div></div></div>'
             % (g.mark("instagram"), stroke("check")))
    sfx("click", T["pidpysh"] + 0.02)
    return js("""
  tl.set("#gF", {autoAlpha: 1}, @yakshcho-0.1);
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
    """The style description types, stalls and is deleted — one clock, so any frame renders cold."""
    t0, t1 = T["poiasn"] + 0.02, T["vazhko"] - 0.05
    t2, t3 = T["sform"] + 0.02, T["samii"] - 0.05
    return r"""
  var CLK = {t: 0}, PB = document.getElementById("pbT"), PTXT = %s, PCUR = null;
  function paintAll() {
    var t = CLK.t, N = PTXT.length, n;
    if (t <= %.3f) n = 0;
    else if (t < %.3f) n = Math.round(N * (t - %.3f) / %.3f);
    else if (t <= %.3f) n = N;
    else if (t < %.3f) n = Math.round(N * (1 - (t - %.3f) / %.3f));
    else n = 0;
    if (n !== PCUR) { PCUR = n; PB.textContent = PTXT.slice(0, n); }
  }
  tl.fromTo(CLK, {t: 0}, {t: %.3f, duration: %.3f, ease: "none", onUpdate: paintAll}, 0);""" % (
        json.dumps(PROMPT, ensure_ascii=False), t0, t1, t0, t1 - t0, t2, t3, t2, t3 - t2, DUR, DUR)


# captions that would repeat the graphic's own words (STYLE.md §2b.1)
def span_words(a, b):
    return (round(a - 0.02, 3), round(b, 3), "")


BLACKOUT = [
    span_words(T["konsult"], E(u"клієнтка", 2.81)),          # header «Консультація · ШІ», name «Клієнтка»
    span_words(T["odyn"], T["urokye"]),                      # «1 · Скіл», then the four format chips
    span_words(T["metody"], T["spilke"]),                    # the three pills
    span_words(T["pravyla"], T["pravylae"]),                 # «Правила»
    span_words(T["testovyi"], T["tekst2e"]),                 # «ТЕСТОВИЙ ТЕКСТ»
    span_words(T["okei"], T["okeie"]),                       # the «Окей» bubble
    span_words(T["kliientamy"], T["kliientamye"]),           # «Клієнти»
    span_words(T["kontentu2"], T["kontentu2e"]),             # «Контент»
    span_words(T["lidm"], T["lidme"]),                       # «Лідмагніти»
]


def main():
    assert not NO_PAINT, "this cut has closeups now: re-check the beats against them"
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
        title=u"Reel 32 — Чому Claude пише не як ти",
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
