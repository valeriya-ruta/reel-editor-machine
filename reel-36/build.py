# -*- coding: utf-8 -*-
"""Reel 36 — «Мене спитали в Threads: а як ти це робиш — цей ваш ШІ-монтаж?».
Posts 2026-10-15. Title in the app: «Pinterest → дизайн-система».

The one object is **the setup chain itself**: a five-station rail at the top of
the frame (1 skills, 2 style.md, 3 design system, 4 test renders, 5 cloud) that
lights station by station; two of the stations open into takeovers, and when the
last one ticks the rail turns into an edit timeline — «тільки тоді можна
монтувати». Then the time it took (2 дні) flips to the time it takes you
(1 година), and the CTA sends the design system from station 3 back as a DM.

Chain:  near: a Threads tile, the follower's post opens out of it (avatar and
handle blurred), highlighter reads along -> clear for «Пффф, вабщє дуже просто»
-> the rail slides in, station 1 lights: skill chips land and drop into a
laptop, a plug snaps on -> station 2: the iris opens out of it: style.md lands,
three liked reels fan in, a prompt splits one into four scenes, a second prompt
scans each, the scenes file themselves into style.md -> the iris closes onto
station 3: the design-system card -> station 4: three test renders fill and tick
-> station 5: the iris opens into the cloud: the laptop sends the job up, the
renders fill inside the cloud, the laptop's own render is crossed out -> the iris
closes onto the rail, all five tick, the rail becomes an edit timeline -> a
calendar «2 дні»; the five steps pass to «you» -> the calendar flips to «1
година», ↓ «або й менше» -> CTA: the comment types «design», her DM comes back
carrying the station-3 design system, «безкоштовно».

usage: python build.py   (then: python ../tools/sfx.py mix 36)
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

CUT = json.load(io.open(os.path.join(ROOT, "work", "r36", "cut.json"), encoding="utf-8"))
DUR = 45.483           # (1365 plate frames - 0.5) / 30
FPS = 30
k = Kit(width=1080, height=1920, fps=FPS, duration=DUR)
g = Glass(["threads", "claude", "instagram"])
k.css(g.css())

NO_PAINT = [tuple(x) for x in CUT["no_paint"]]      # empty for this cut
# her sarcastic beat — «Пффф, вабщє дуже просто))» — stays clear like a closeup
JOKE = (3.74, 5.85)

CAPS = k.load_captions(os.path.join(ROOT, "work", "r36", "captions.json"))
# whisper errors the aligner kept as "her wording" -> script spelling
FIX = {u"шуїй": u"ШІ-", u"Тхе,": u"Пффф,", u"вопші": u"вабщє", u"хмеру,": u"хмару,",
       u"Окремо": u"окремо", u"це могла": u"могла"}
for c in CAPS:
    c["w"] = FIX.get(c["w"], c["w"])
# «стелем дій.» is whisper's «style.md:» — one token on her timing
for i, c in enumerate(CAPS):
    if c["w"] == u"стелем" and CAPS[i + 1]["w"] == u"дій.":
        c["w"] = u"style.md:"
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
    "spytaly": S(u"спитали", 0.57), "threads": S(u"Threads:", 0.95), "a": S(u"а", 1.37),
    "tsei": S(u"цей", 2.32), "montazh": S(u"монтаж?", 3.24), "montazhe": E(u"монтаж?", 3.24),
    "spochatku": S(u"Спочатку", 5.95), "nabir": S(u"набір", 7.21), "skiliv": S(u"скілів", 7.49),
    "stavysh": S(u"ставиш", 8.01), "lokalno": S(u"локально", 8.43), "skily": S(u"скіли", 9.05),
    "plahiny": S(u"плагіни.", 9.47),
    "potim": S(u"Потім", 9.93), "style": S(u"style.md:", 10.65), "stylee": E(u"style.md:", 10.65),
    "beresh": S(u"береш", 11.3), "rilsiv": S(u"рілсів,", 12.02), "podob": S(u"подобаються,", 12.66),
    "spets": S(u"спеціальним", 13.32), "promtom": S(u"промтом", 13.92), "rozbyr": S(u"розбираєш", 14.24),
    "rils": S(u"рілс", 15.22), "stseny": S(u"сцени.", 15.76), "stsenye": E(u"сцени.", 15.76),
    "dali": S(u"Далі", 16.23), "inshyi": S(u"інший", 16.82), "analiz": S(u"аналізує", 17.42),
    "stsenu": S(u"сцену", 18.32), "stsenue": E(u"сцену", 18.32),
    "zberih": S(u"зберігає", 18.56), "pryklad": S(u"приклад.", 19.26),
    "okremo": S(u"окремо", 19.82), "hotuiesh": S(u"готуєш", 20.06), "vlasnu": S(u"власну", 20.52),
    "dyzain": S(u"дизайн-систему", 20.84), "dyzaine": E(u"дизайн-систему", 20.84),
    "pislia": S(u"Після", 22.16), "kilka": S(u"кілька", 22.64), "testovykh": S(u"тестових", 22.96),
    "renderiv": S(u"рендерів,", 23.44), "pereviryty": S(u"перевірити,", 23.9),
    "vzahali": S(u"взагалі", 24.7), "pratsiuie": S(u"працює,", 25.02),
    "pidkl": S(u"підключаєш", 25.58), "render": S(u"рендер", 26.18), "khmaru": S(u"хмару,", 26.84),
    "stvor": S(u"створювалось", 27.75), "tam": S(u"там,", 28.25), "nena": S(u"не", 28.75),
    "komp": S(u"компʼютері.", 29.25),
    "tilky": S(u"тільки", 30.31), "mozhna": S(u"можна", 30.97), "montuv": S(u"монтувати.", 31.37),
    "montuve": E(u"монтувати.", 31.37),
    "koly": S(u"Коли", 32.22), "zainialo": S(u"зайняло", 33.76), "dva": S(u"два", 34.46),
    "dni": S(u"дні,", 34.92), "dnie": E(u"дні,", 34.92),
    "ale": S(u"але", 35.35), "teper": S(u"тепер", 35.83), "znaiu": S(u"знаю,", 36.21),
    "peredaty": S(u"передати", 36.67), "tobi": S(u"тобі,", 37.05), "shchob": S(u"щоб", 37.47),
    "bukv": S(u"буквально", 38.59), "za": S(u"за", 39.03), "hodynu": S(u"годину", 39.23),
    "hodynue": E(u"годину", 39.23), "abo": S(u"або", 39.63), "menshe": S(u"менше.", 40.01),
    "menshee": E(u"менше.", 40.01),
    "napyshy": S(u"Напиши", 40.7), "slovo": S(u"слово", 41.12), "design": S(u"«дизайн»", 41.34),
    "designe": E(u"«дизайн»", 41.34), "nadishliu": S(u"надішлю,", 42.39),
    "dyzain2": S(u"дизайн-систему", 43.67), "bezk": S(u"безкоштовно.", 44.53),
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
    assert not (JOKE[0] <= t <= JOKE[1]), ("sfx on her joke", name, t)
    SFX.append({"t": round(max(0.0, t), 3), "name": name, "db": db})


# ---------------------------------------------------------------------------
# Glyphs (24-grid strokes)
STROKES = {
    "up": '<path d="M12 19.2V5.4M6.2 11l5.8-5.8 5.8 5.8"/>',
    "down": '<path d="M12 4.8v13.8M6.2 13l5.8 5.8 5.8-5.8"/>',
    "check": '<path d="M5.4 12.6l4.3 4.3 8.9-9.5"/>',
    "x": '<path d="M6.8 6.8l10.4 10.4M17.2 6.8L6.8 17.2"/>',
    "person": '<circle cx="12" cy="8.2" r="3.6"/><path d="M4.8 20c.9-3.8 3.7-5.8 7.2-5.8s6.3 2 7.2 5.8"/>',
    "heart": '<path d="M12 20.2s-7.7-4.6-7.7-10.2A4.3 4.3 0 0 1 12 7.5a4.3 4.3 0 0 1 7.7 2.5c0 5.6-7.7 10.2-7.7 10.2z"/>',
    "comment": '<path d="M20.2 11.7a8.2 8.2 0 0 1-12 7.2L3.8 20.2l1.3-4.3a8.2 8.2 0 1 1 15.1-4.2z"/>',
    "repost": '<path d="M6.5 10.5V9a2.5 2.5 0 0 1 2.5-2.5h9.5M15.8 3.8l2.7 2.7-2.7 2.7M17.5 13.5V15a2.5 2.5 0 0 1-2.5 2.5H5.5M8.2 20.2l-2.7-2.7 2.7-2.7"/>',
    "share": '<path d="M20.6 3.6L10.3 13.7M20.6 3.6l-6.6 17-3.7-6.9-6.9-3.7z"/>',
    "plug": '<path d="M9 3.2v5M15 3.2v5M6.4 8.2h11.2v3.4a5.6 5.6 0 0 1-11.2 0V8.2zM12 17.2v3.8"/>',
    "clock": '<circle cx="12" cy="12" r="8.4"/><path d="M12 7.4V12l3.1 2.1"/>',
    "lens": '<circle cx="10.4" cy="10.4" r="6.4"/><path d="M15.2 15.2l5 5"/>',
    "doc": '<path d="M6.8 3h7.4l4.6 4.6V20a1 1 0 0 1-1 1H6.8a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1z"/><path d="M14 3v5h4.8"/>',
}
PLAY = '<svg class="ply" viewBox="0 0 24 24"><path d="M8.5 5.6v12.8l10.2-6.4z"/></svg>'


def stroke(name, cls="sk"):
    return '<svg class="%s" viewBox="0 0 24 24">%s</svg>' % (cls, STROKES[name])


def tile(tid, size, x, y, material, inner, extra_cls="", hide=True, ring=True):
    r = ('<div class="sqring" id="%sR" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx"></div>'
         % (tid, x, y, size, size)) if ring else ""
    return ('%s<div class="tw%s %s" id="%s" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx">'
            '<div class="%s">%s<div class="sheen"></div></div></div>'
            % (r, " hide" if hide else "", extra_cls, tid, x, y, size, size, material, inner))


SWATCH = ("#6b081c", "#b4122f", "#ff6e9c", "#fdf1f4", "#17141c")

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
.ink { stroke: #17141c !important; }

/* ---- A · the Threads post ---- */
.thr { position: absolute; border-radius: 48px; overflow: hidden; color: #101010;
  background: linear-gradient(172deg, #ffffff 0%, #fdfcfd 100%);
  box-shadow: inset 0 2px 1px #fff, 0 44px 90px -34px rgba(24,4,12,0.62), 0 0 0 1px rgba(0,0,0,0.04); }
.thr .av { position: absolute; left: 38px; top: 38px; width: 88px; height: 88px; border-radius: 50%;
  background: radial-gradient(circle at 50% 38%, #f1c9b4 0 22%, rgba(0,0,0,0) 23%),
              radial-gradient(ellipse 46% 34% at 50% 98%, #6b3b2e 0 98%, rgba(0,0,0,0) 100%),
              linear-gradient(160deg, #c9a08c 0%, #7a4a3c 100%);
  filter: blur(6px); }
.thr .hd { position: absolute; left: 150px; top: 44px; display: flex; align-items: baseline; gap: 16px; }
.thr .hn { font-size: 33px; font-weight: 700; letter-spacing: -0.01em; filter: blur(6px); }
.thr .tm { font-size: 30px; font-weight: 400; color: #808080; }
.thr .more { position: absolute; right: 42px; top: 58px; display: flex; gap: 7px; }
.thr .more b { width: 8px; height: 8px; border-radius: 50%; background: #101010; display: block; }
.thr .tx { position: absolute; left: 150px; top: 104px; width: 720px; font-size: 46px; font-weight: 500;
  line-height: 1.3; letter-spacing: -0.012em; }
.thr .ln { position: relative; display: inline-block; white-space: nowrap; }
.thr .ln span { position: relative; z-index: 1; }
.thr .hlb { position: absolute; left: -6px; right: -6px; bottom: 4px; height: 26px; border-radius: 8px;
  background: rgba(255,110,156,0.38); transform-origin: 0 50%; z-index: 0; }
.thr .act { position: absolute; left: 140px; top: 290px; display: flex; align-items: center; gap: 34px; }
.thr .act div { display: flex; align-items: center; gap: 10px; font-size: 27px; color: #8a8a8a; font-weight: 500; }
.thr .act svg { width: 46px; height: 46px; fill: none; stroke: #101010; stroke-width: 1.7;
  stroke-linecap: round; stroke-linejoin: round; }

/* ---- R · the five-station rail ---- */
.rtrk { position: absolute; left: 180px; top: 129px; width: 720px; height: 6px; border-radius: 3px;
  background: rgba(255,255,255,0.26); }
.rfil { position: absolute; left: 180px; top: 129px; width: 720px; height: 6px; border-radius: 3px;
  background: linear-gradient(90deg, #ff8ab0, #ffd6e3); transform-origin: 0 50%;
  box-shadow: 0 0 14px rgba(255,110,156,0.9); }
.nd { position: absolute; width: 78px; height: 78px; border-radius: 50%; display: flex; align-items: center;
  justify-content: center; font-size: 34px; font-weight: 700; color: rgba(255,255,255,0.86);
  background: rgba(255,255,255,0.16); box-shadow: inset 0 1.5px 1px rgba(255,255,255,0.55), 0 10px 24px -10px rgba(10,0,4,0.5); }
.ndf, .ndk { position: absolute; inset: 0; border-radius: 50%; display: flex; align-items: center;
  justify-content: center; opacity: 0; visibility: hidden; }
.ndf { background: linear-gradient(165deg, #e0204b 0%, #ab112e 46%, #6b081c 100%); color: #fff;
  box-shadow: inset 0 2px 1px rgba(255,255,255,0.55), 0 0 30px rgba(255,110,156,0.75); }
.ndk { background: linear-gradient(160deg, #ffffff 0%, #fff5f8 52%, #f5dfe6 100%);
  box-shadow: inset 0 2px 1px #fff, 0 10px 24px -10px rgba(10,0,4,0.5); }
.ndk svg { width: 44px; height: 44px; fill: none; stroke: #b4122f; stroke-width: 3; stroke-linecap: round; stroke-linejoin: round; }
.clp { position: absolute; top: 104px; height: 56px; border-radius: 16px; opacity: 0; visibility: hidden;
  box-shadow: inset 0 2px 1px rgba(255,255,255,0.45), 0 10px 20px -10px rgba(10,0,4,0.5); }
.clp.j { background: linear-gradient(165deg, #e0204b 0%, #8d0d24 100%); }
.clp.p { background: linear-gradient(160deg, #ffffff 0%, #f5dfe6 100%); }
.clp.k { background: linear-gradient(165deg, #ff8ab0 0%, #ff5c8f 100%); }
.phd { position: absolute; left: 0; top: 84px; width: 6px; height: 96px; border-radius: 3px; background: #fff;
  box-shadow: 0 0 16px rgba(255,255,255,0.9); opacity: 0; visibility: hidden; }

/* ---- B · skills -> laptop ---- */
.chp { position: absolute; width: 410px; height: 100px; border-radius: 50px; display: flex; align-items: center;
  gap: 18px; padding-left: 22px; color: #17141c; font-size: 38px; font-weight: 700; letter-spacing: -0.015em;
  background: linear-gradient(160deg, #ffffff 0%, #fff5f8 52%, #f5dfe6 100%);
  box-shadow: inset 0 2px 1px #fff, 0 30px 60px -22px rgba(30,4,12,0.6); }
.chp .tw { position: relative; width: 60px; height: 60px; flex: none; }
.lap { position: absolute; border-radius: 30px; overflow: hidden;
  background: linear-gradient(160deg, #2a1f2a 0%, #17141c 100%);
  box-shadow: inset 0 0 0 7px #e9dde2, inset 0 0 0 8px rgba(255,255,255,0.5), 0 44px 90px -30px rgba(10,0,4,0.7); }
.lapb { position: absolute; border-radius: 4px 4px 30px 30px;
  background: linear-gradient(180deg, #ffffff 0%, #ecdde3 100%);
  box-shadow: inset 0 2px 1px #fff, 0 30px 50px -20px rgba(10,0,4,0.6); }
.lapb i { position: absolute; left: 50%; top: 0; width: 130px; height: 12px; margin-left: -65px;
  border-radius: 0 0 10px 10px; background: rgba(23,20,28,0.12); }
.lrow { position: absolute; left: 44px; height: 46px; display: flex; align-items: center; gap: 16px;
  color: rgba(255,255,255,0.9); font-size: 30px; font-weight: 500; opacity: 0; visibility: hidden; }
.lrow b { width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center;
  background: linear-gradient(165deg, #e0204b 0%, #8d0d24 100%); }
.lrow b svg { width: 28px; height: 28px; fill: none; stroke: #fff; stroke-width: 3; stroke-linecap: round; stroke-linejoin: round; }
.lhd { position: absolute; left: 44px; top: 30px; display: flex; align-items: center; gap: 14px;
  color: rgba(255,255,255,0.55); font-size: 26px; font-weight: 700; letter-spacing: 0.12em; }
.lhd .tw { position: relative; width: 48px; height: 48px; }

/* ---- TK1 · style.md ---- */
.fcard { position: absolute; border-radius: 52px; }
.fcard .ttl { position: absolute; left: 186px; top: 52px; font-size: 76px; font-weight: 700; letter-spacing: -0.03em; }
.slot { position: absolute; width: 64px; height: 114px; border-radius: 14px;
  box-shadow: inset 0 0 0 3px rgba(23,20,28,0.13); }
.rl { position: absolute; width: 340px; height: 604px; border-radius: 40px; overflow: hidden;
  box-shadow: inset 0 2px 1px rgba(255,255,255,0.4), 0 60px 110px -40px rgba(8,0,3,0.8); }
.rl .ph { position: absolute; inset: 0; }
.rl .fig { position: absolute; left: 70px; top: 190px; width: 200px; height: 420px; border-radius: 100px 100px 0 0;
  background: rgba(255,255,255,0.22); }
.rl .fig::before { content: ""; position: absolute; left: 50px; top: -110px; width: 100px; height: 100px; border-radius: 50%;
  background: rgba(255,255,255,0.3); }
.rl .ply { position: absolute; left: 130px; top: 262px; width: 80px; height: 80px; fill: rgba(255,255,255,0.92);
  filter: drop-shadow(0 6px 14px rgba(0,0,0,0.3)); }
.rl .ig { position: absolute; right: 26px; top: 26px; width: 46px; height: 46px; fill: #fff; }
.rl .bt { position: absolute; left: 28px; bottom: 34px; right: 28px; height: 90px; }
.rl .bt i { position: absolute; display: block; border-radius: 8px; background: rgba(255,255,255,0.8); }
.hrt { position: absolute; width: 96px; height: 96px; }
.hrt svg { position: absolute; left: 24px; top: 26px; width: 48px; height: 48px; fill: #fff; stroke: none; }
.pbw { position: absolute; border-radius: 56px; overflow: hidden;
  background: linear-gradient(172deg, #ffffff 0%, #fff9fb 55%, #fdf0f4 100%);
  box-shadow: inset 0 2px 1px #fff, 0 50px 100px -36px rgba(8,0,3,0.8); }
.pbw .tw { position: absolute; }
.ptx { position: absolute; left: 150px; top: 0; height: 170px; line-height: 170px; font-size: 42px; font-weight: 500;
  color: #17141c; white-space: nowrap; letter-spacing: -0.01em; }
.ptx::after { content: ""; display: inline-block; width: 3px; height: 44px; margin-left: 4px; vertical-align: -8px;
  background: #b4122f; }
.sc { position: absolute; width: 200px; height: 356px; border-radius: 28px; overflow: hidden;
  background: linear-gradient(170deg, #ffffff 0%, #fff5f8 60%, #f8e6ec 100%);
  box-shadow: inset 0 2px 1px #fff, 0 40px 80px -30px rgba(8,0,3,0.8); }
.sc i { position: absolute; display: block; }
.sc .num { position: absolute; left: 14px; top: 14px; width: 50px; height: 50px; border-radius: 50%;
  background: linear-gradient(165deg, #e0204b 0%, #8d0d24 100%); color: #fff; font-size: 28px; font-weight: 700;
  display: flex; align-items: center; justify-content: center; opacity: 0; visibility: hidden; z-index: 2; }
.sc .ok { position: absolute; right: 14px; top: 14px; width: 50px; height: 50px; border-radius: 50%;
  background: linear-gradient(160deg, #ffffff 0%, #f5dfe6 100%); box-shadow: 0 6px 14px -6px rgba(10,0,4,0.5);
  opacity: 0; visibility: hidden; z-index: 2; }
.sc .ok svg { position: absolute; left: 8px; top: 8px; width: 34px; height: 34px; fill: none; stroke: #b4122f;
  stroke-width: 3.2; stroke-linecap: round; stroke-linejoin: round; }
.hb { border-radius: 10px; background: linear-gradient(115deg, #c41434 0%, #8d0d24 100%); }
.rr { border-radius: 7px; background: rgba(23,20,28,0.13); }
.im { border-radius: 18px; background: linear-gradient(150deg, #f4dfe5 0%, #ecc8d0 100%); }
.lens { position: absolute; width: 150px; height: 150px; z-index: 5; }
.lens svg { width: 150px; height: 150px; fill: rgba(255,255,255,0.18); stroke: #fff; stroke-width: 1.6;
  stroke-linecap: round; filter: drop-shadow(0 0 12px rgba(255,110,156,0.9)); overflow: visible; }

/* ---- C · design system ---- */
.sw { position: absolute; width: 86px; height: 86px; border-radius: 50%;
  box-shadow: inset 0 2px 1px rgba(255,255,255,0.45), 0 14px 26px -12px rgba(30,4,12,0.55); }
.aa { position: absolute; font-size: 168px; font-weight: 900; letter-spacing: -0.05em; line-height: 1;
  background: linear-gradient(118deg, #7e0b20 0%, #b4122f 42%, #ff6e9c 100%);
  -webkit-background-clip: text; background-clip: text; color: transparent; padding-right: 8px; }
.btnp { position: absolute; border-radius: 999px; display: flex; align-items: center; justify-content: center;
  color: #fff; font-weight: 700; letter-spacing: -0.01em;
  background: linear-gradient(165deg, #e0204b 0%, #ab112e 46%, #6b081c 100%);
  box-shadow: inset 0 2px 1px rgba(255,255,255,0.5), 0 18px 36px -14px rgba(70,4,20,0.6); }
.ty { position: absolute; color: #17141c; line-height: 1; }

/* ---- D · test renders ---- */
.rc { position: absolute; width: 164px; height: 290px; border-radius: 30px; overflow: hidden; }
.rc .pp { position: absolute; left: 47px; top: 70px; width: 70px; height: 70px; border-radius: 50%;
  background: rgba(255,255,255,0.75); }
.rc .pb2 { position: absolute; left: 30px; top: 150px; width: 104px; height: 120px; border-radius: 52px 52px 0 0;
  background: rgba(255,255,255,0.5); }
.rc .cb { position: absolute; left: 26px; top: 200px; width: 112px; height: 22px; border-radius: 8px;
  background: #fff; box-shadow: 0 4px 10px rgba(0,0,0,0.25); }
.pgt { position: absolute; width: 164px; height: 14px; border-radius: 7px; background: rgba(255,255,255,0.28); overflow: hidden; }
.pgf { position: absolute; inset: 0; border-radius: 7px; background: linear-gradient(90deg, #ff8ab0, #ffffff);
  transform-origin: 0 50%; }

/* ---- TK2 · the cloud ---- */
.cloud { position: absolute; left: 0; top: 0; overflow: visible;
  filter: drop-shadow(0 50px 70px rgba(8,0,3,0.55)); }
.rq { position: absolute; width: 130px; height: 230px; border-radius: 24px; overflow: hidden;
  background: linear-gradient(165deg, #e0204b 0%, #ab112e 46%, #6b081c 100%);
  box-shadow: inset 0 2px 1px rgba(255,255,255,0.5), 0 24px 40px -18px rgba(70,4,20,0.7); }
.rq .pp { position: absolute; left: 37px; top: 52px; width: 56px; height: 56px; border-radius: 50%; background: rgba(255,255,255,0.7); }
.rq .pb2 { position: absolute; left: 22px; top: 118px; width: 86px; height: 112px; border-radius: 43px 43px 0 0; background: rgba(255,255,255,0.4); }
.rq .pgt { left: 16px; bottom: 16px; width: 98px; height: 12px; background: rgba(255,255,255,0.3); }
.cab .tube { fill: none; stroke: rgba(255,255,255,0.26); stroke-width: 20; stroke-linecap: round; }
.cab .core { fill: none; stroke: rgba(255,255,255,0.92); stroke-width: 4.5; stroke-linecap: round; }
.cab .pkt  { fill: none; stroke: #ffd6e3; stroke-width: 11; stroke-linecap: round; }
.cab .pkg  { filter: drop-shadow(0 0 10px rgba(255,120,165,1)); }

/* ---- E · 2 days -> 1 hour ---- */
.calw { position: absolute; }
.calc { position: absolute; inset: 0; border-radius: 54px; overflow: hidden; backface-visibility: hidden;
  background: linear-gradient(170deg, #ffffff 0%, #fff6f9 60%, #f8e6ec 100%);
  box-shadow: inset 0 2px 1px #fff, 0 44px 80px -30px rgba(24,4,12,0.6); }
.calc .hd { position: absolute; left: 0; top: 0; right: 0; height: 92px;
  background: linear-gradient(165deg, #e0204b 0%, #8d0d24 100%); }
.calc .hole { position: absolute; top: 34px; width: 24px; height: 24px; border-radius: 50%; background: rgba(255,255,255,0.85); }
.calc .hd svg { position: absolute; left: 50%; top: 16px; width: 60px; height: 60px; margin-left: -30px; fill: none;
  stroke: #fff; stroke-width: 2.4; stroke-linecap: round; stroke-linejoin: round; }
.calc .big { position: absolute; left: 0; right: 0; top: 104px; text-align: center; font-size: 190px; font-weight: 900;
  letter-spacing: -0.05em; line-height: 1;
  background: linear-gradient(118deg, #7e0b20 0%, #b4122f 42%, #ff6e9c 100%);
  -webkit-background-clip: text; background-clip: text; color: transparent; }
.calc .lb { position: absolute; left: 0; right: 0; top: 300px; text-align: center; font-size: 46px; font-weight: 700;
  color: rgba(23,20,28,0.5); }
.gdoc { position: absolute; border-radius: 40px; overflow: hidden;
  background: linear-gradient(172deg, #ffffff 0%, #fff9fb 55%, #fdf0f4 100%);
  box-shadow: inset 0 2px 1px #fff, 0 40px 80px -30px rgba(24,4,12,0.62); }
.gdoc i { position: absolute; display: block; }
.gdoc .ck { position: absolute; left: 26px; width: 34px; height: 34px; border-radius: 10px;
  background: linear-gradient(165deg, #e0204b 0%, #8d0d24 100%); }
.gdoc .ck svg { position: absolute; left: 5px; top: 5px; width: 24px; height: 24px; fill: none; stroke: #fff;
  stroke-width: 3.4; stroke-linecap: round; stroke-linejoin: round; }

/* ---- F · CTA ---- */
.cmt { position: absolute; border-radius: 60px; overflow: hidden;
  background: linear-gradient(172deg, #ffffff 0%, #fff9fb 55%, #fdf0f4 100%);
  box-shadow: inset 0 2px 1px #fff, 0 40px 80px -30px rgba(24,4,12,0.62); }
.cmt .avp { position: absolute; left: 22px; top: 20px; width: 80px; height: 80px; border-radius: 50%;
  background: linear-gradient(160deg, #f4dfe5 0%, #ecc8d0 100%); display: flex; align-items: center; justify-content: center; }
.cmt .avp svg { width: 44px; height: 44px; fill: none; stroke: #8d0d24; stroke-width: 2.2; stroke-linecap: round; }
.cmt .phd2 { position: absolute; left: 128px; top: 0; height: 120px; line-height: 120px; font-size: 40px; font-weight: 500;
  color: rgba(23,20,28,0.38); }
#cmT { position: absolute; left: 128px; top: 0; height: 120px; line-height: 120px; font-size: 46px; font-weight: 700;
  color: #17141c; white-space: nowrap; }
#cmT::after { content: ""; display: inline-block; width: 3px; height: 46px; margin-left: 4px; vertical-align: -8px;
  background: #b4122f; }
#dm .app { position: absolute; left: 166px; top: 40px; font-size: 30px; font-weight: 700; color: rgba(255,255,255,0.72); }
#dm .tm  { position: absolute; right: 46px; top: 42px; font-size: 26px; font-weight: 500; color: rgba(255,255,255,0.5); }
.mini { position: absolute; border-radius: 34px; overflow: hidden;
  background: linear-gradient(172deg, #ffffff 0%, #fff9fb 55%, #fdf0f4 100%);
  box-shadow: inset 0 2px 1px #fff, 0 24px 44px -20px rgba(10,0,4,0.6); }
.free { position: absolute; height: 84px; border-radius: 42px; padding: 0 34px; display: flex; align-items: center;
  background: linear-gradient(165deg, #e0204b 0%, #ab112e 46%, #6b081c 100%); color: #fff; font-size: 40px;
  font-weight: 700; letter-spacing: -0.01em; white-space: nowrap;
  box-shadow: inset 0 2px 1px rgba(255,255,255,0.5), 0 24px 44px -16px rgba(70,4,20,0.75); }
""")

L = []
BEATS = []


def beat(fn):
    BEATS.append(fn)
    return fn


# ===========================================================================
# A · the Threads question
@beat
def a_threads():
    acts = ('<div>%s48</div><div>%s12</div><div>%s</div><div>%s</div>'
            % (stroke("heart", "ts"), stroke("comment", "ts"), stroke("repost", "ts"), stroke("share", "ts")))
    acts = acts.replace('class="ts"', "")
    post = (
        '<div class="thr hide" id="thr" style="left:90px;top:130px;width:900px;height:390px">'
        '<div class="av"></div>'
        '<div class="hd"><span class="hn">olena.kovalchuk_</span><span class="tm">2 год</span></div>'
        '<div class="tx"><div class="ln"><i class="hlb" id="hl1"></i><span>А як ти це робиш —</span></div><br>'
        '<div class="ln"><i class="hlb" id="hl2"></i><span>цей ваш ШІ-монтаж?</span></div></div>'
        '<div class="act">%s</div>'
        '<div class="shc"><div class="sheen"></div></div></div>' % acts)
    L.append('<div class="g full" id="gA">' + post
             + tile("aTh", 120, 480, 230, "pearl", g.mark("threads")) + '</div>')
    sfx("pop", T["spytaly"] + 0.02, -2)
    sfx("notification", T["threads"] + 0.05, -2)
    return js("""
  tl.set("#gA", {autoAlpha: 1}, 0);
  arr("#aTh", @spytaly-0.05, {s: 0.3, y: 30, d: 0.7});
  G.ripple("#aThR", @spytaly+0.25);
  /* the tile becomes the post's badge, the post opens out of it */
  tl.to("#aTh", {x: 395, y: -126, scale: 0.7, duration: 0.6, ease: SP}, @threads-0.05);
  gsap.set("#thr", {transformOrigin: "450px 160px"});
  arr("#thr", @threads, {s: 0.35, y: 20, d: 0.8});
  shn("#thr .sheen", @threads+0.35);
  gsap.set(["#hl1", "#hl2"], {scaleX: 0});
  tl.to("#hl1", {scaleX: 1, duration: 0.8, ease: "power1.inOut"}, @a);
  tl.to("#hl2", {scaleX: 1, duration: 1.25, ease: "power1.inOut"}, @tsei);
  bout(["#thr", "#aTh"], @montazhe-0.3, 10, 0.26);
  tl.set("#gA", {autoAlpha: 0}, @montazhe);""")


# ===========================================================================
# R · the rail: five stations, lit one by one; at the end it becomes a timeline
NX = [180 + i * 180 for i in range(5)]
NY = 132
CLIPS = [(126, 150, "j"), (284, 210, "p"), (502, 120, "k"), (630, 170, "j"), (808, 146, "p")]


@beat
def r_rail():
    nodes = ""
    for i, x in enumerate(NX):
        nodes += ('<div class="nd" id="n%d" style="left:%dpx;top:%dpx"><span id="n%dn">%d</span>'
                  '<div class="ndf" id="n%df">%d</div><div class="ndk" id="n%dk">%s</div></div>'
                  % (i, x - 39, NY - 39, i, i + 1, i, i + 1, i, '<svg viewBox="0 0 24 24">%s</svg>' % STROKES["check"]))
    clips = "".join('<div class="clp %s" id="cl%d" style="left:%dpx;width:%dpx"></div>' % (c, i, x, w)
                    for i, (x, w, c) in enumerate(CLIPS))
    L.append('<div class="g full" id="gR">'
             '<div class="shelf edge hide" id="rSh" style="left:90px;top:66px;width:900px;height:132px"></div>'
             '<div class="abs" id="rNodes" style="left:0;top:0"><div class="rtrk"></div><div class="rfil" id="rFil"></div>'
             + nodes + '</div>'
             '<div class="abs" id="rTl" style="left:0;top:0">' + clips
             + '<div class="phd" id="phd" style="left:126px"></div></div></div>')
    sfx("sparkle", T["tilky"] + 0.05, -3)
    return js("""
  tl.set("#gR", {autoAlpha: 1}, @spochatku-0.1);
  gsap.set("#rFil", {scaleX: 0});
  arr("#rSh", @spochatku-0.08, {s: 0.9, y: -40, d: 0.7});
  [0, 1, 2, 3, 4].forEach(function (i) { arr("#n" + i, @spochatku+0.02 + i * 0.07, {s: 0.3, y: -10, d: 0.6, blur: 6}); });
  function lite(i, t) { tl.fromTo("#n" + i + "f", {autoAlpha: 0, scale: 0.4}, {autoAlpha: 1, scale: 1, duration: 0.45, ease: POP}, t);
    tl.set("#n" + i + "n", {autoAlpha: 0}, t + 0.02); }
  function done(i, t) {
    tl.fromTo("#n" + i + "k", {autoAlpha: 0, scale: 0.4}, {autoAlpha: 1, scale: 1, duration: 0.45, ease: POP}, t);
    tl.to("#rFil", {scaleX: Math.min(1, (i + 1) / 4), duration: 0.5, ease: SP}, t + 0.05);
    tl.set("#n" + i + "f", {autoAlpha: 0}, t + 0.3);
  }
  /* the rail steps out while a takeover owns the frame */
  tl.set("#gR", {autoAlpha: 0}, @style+0.6); tl.set("#gR", {autoAlpha: 1}, @okremo-0.62);
  tl.set("#gR", {autoAlpha: 0}, @pidkl+1.0); tl.set("#gR", {autoAlpha: 1}, @komp+0.48);
  lite(0, @spochatku+0.3);
  done(0, @potim); lite(1, @potim+0.3);
  done(1, @okremo-0.25); lite(2, @okremo-0.1);
  done(2, @pislia); lite(3, @pislia+0.25);
  done(3, @pidkl-0.08); lite(4, @pidkl+0.1);
  done(4, @tilky);
  G.bump("#rSh", @tilky+0.1);
  /* the chain becomes the edit: nodes out, clips in, the playhead runs */
  bout("#rNodes", @mozhna-0.05, 8, 0.28);
  [0, 1, 2, 3, 4].forEach(function (i) {
    tl.fromTo("#cl" + i, {autoAlpha: 0, scaleX: 0.2, transformOrigin: "0% 50%"},
              {autoAlpha: 1, scaleX: 1, duration: 0.45, ease: SP}, @mozhna+0.2 + i * 0.06);
  });
  tl.set("#phd", {autoAlpha: 1}, @montuv-0.05);
  tl.fromTo("#phd", {x: 0}, {x: 820, duration: 0.85, ease: "none"}, @montuv-0.05);
  bout("#gR", @montuve-0.05, 10, 0.26);""")


# ===========================================================================
# B · station 1 — skills and plugins, installed locally
SKILLS = ("hyperframes", "remotion", "video-use", "media-use")
CHIP_XY = [(110, 236), (560, 236), (110, 360), (560, 360)]
LAP = (260, 232, 560, 316)            # screen x, y, w, h


@beat
def b_skills():
    chips = ""
    for i, (name, (x, y)) in enumerate(zip(SKILLS, CHIP_XY)):
        chips += ('<div class="chp hide" id="ch%d" style="left:%dpx;top:%dpx">'
                  '<div class="tw"><div class="jelly">%s</div></div>%s</div>' % (i, x, y, g.mark("claude"), name))
    rows = "".join('<div class="lrow" id="lr%d" style="top:%dpx"><b>%s</b>%s</div>'
                   % (i, 96 + i * 52, '<svg viewBox="0 0 24 24">%s</svg>' % STROKES["check"], n)
                   for i, n in enumerate(SKILLS))
    x, y, w, h = LAP
    lap = ('<div class="abs hide" id="lap" style="left:0;top:0">'
           '<div class="lap" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx">'
           '<div class="lhd" id="lhd"><div class="tw"><div class="jelly">%s</div></div>SKILLS</div>%s</div>'
           '<div class="lapb" style="left:%dpx;top:%dpx;width:%dpx;height:30px"><i></i></div></div>'
           % (x, y, w, h, g.mark("claude"), rows, x - 70, y + h, w + 140))
    L.append('<div class="g full" id="gB">' + lap + chips
             + tile("bPl", 128, 830, 290, "jelly", stroke("plug")) + '</div>')
    sfx("pop", T["nabir"] + 0.02)
    sfx("whoosh-short", T["lokalno"] - 0.05, -3)
    sfx("pop", T["plahiny"] + 0.02)
    # chip centre -> a point inside the screen
    fly = []
    for i, (cx, cy) in enumerate(CHIP_XY):
        tx, ty = x + 200, y + 96 + i * 52 + 23
        fly.append('  tl.to("#ch%d", {x: %d, y: %d, scale: 0.3, autoAlpha: 0, duration: 0.32, ease: "power3.in"}, @lokalno-0.2+%.2f);'
                   % (i, tx - (cx + 205), ty - (cy + 50), i * 0.04))
    return js("""
  tl.set("#gB", {autoAlpha: 1}, @nabir-0.2);
  [0, 1, 2, 3].forEach(function (i) { arr("#ch" + i, @nabir-0.12 + i * 0.1, {s: 0.4, y: 40, d: 0.7}); });
  arr("#lap", @stavysh-0.1, {s: 0.85, y: 120, d: 0.8});
{{fly}}
  [0, 1, 2, 3].forEach(function (i) {
    tl.fromTo("#lr" + i, {autoAlpha: 0, x: -20}, {autoAlpha: 1, x: 0, duration: 0.35, ease: SP}, @lokalno+0.3 + i * 0.1);
  });
  tl.fromTo("#lhd", {autoAlpha: 0}, {autoAlpha: 1, duration: 0.25}, @lokalno+0.25);
  arr("#bPl", @plahiny-0.12, {s: 0.4, x: 160, y: 0, d: 0.6});
  G.haptic("#lap", @plahiny+0.3); G.ripple("#bPlR", @plahiny+0.25);
  bout("#gB", @potim+0.05, 10, 0.28);""").replace("{{fly}}", js("\n".join(fly)))


# ===========================================================================
# TK1 · station 2 — style.md, out of the rail's second node
RL = [(-40, 380, -6, "linear-gradient(165deg,#ff8ab0 0%,#b4122f 70%,#5a0718 100%)"),
      (370, 360, 0, "linear-gradient(160deg,#f4dfe5 0%,#c98a9a 50%,#6b081c 100%)"),
      (780, 380, 6, "linear-gradient(170deg,#e0204b 0%,#8d0d24 60%,#2a0510 100%)")]
SC_X = [95 + i * 230 for i in range(4)]
SC_Y = 452
FC = (70, 110, 940, 210)               # the style.md card
SLOT_X = [FC[0] + 600 + i * 80 for i in range(4)]
SLOT_Y = FC[1] + 48
P1 = u"Розбий цей рілс на сцени"
P2 = u"Проаналізуй кожну сцену"


def scene(i):
    inner = [
        '<i class="hb" style="left:24px;top:96px;width:150px;height:30px"></i>'
        '<i class="hb" style="left:24px;top:136px;width:104px;height:30px"></i>'
        '<i class="rr" style="left:24px;top:190px;width:150px;height:14px"></i>'
        '<i class="rr" style="left:24px;top:214px;width:118px;height:14px"></i>'
        '<i class="im" style="left:24px;top:248px;width:152px;height:84px"></i>',
        '<i class="im" style="left:0;top:0;width:200px;height:356px;border-radius:0"></i>'
        '<i style="left:62px;top:100px;width:76px;height:76px;border-radius:50%;background:#fff"></i>'
        '<i style="left:36px;top:190px;width:128px;height:170px;border-radius:64px 64px 0 0;background:rgba(255,255,255,0.8)"></i>'
        '<i style="left:30px;top:270px;width:140px;height:24px;border-radius:8px;background:#17141c"></i>',
        '<i class="hb" style="left:24px;top:84px;width:70px;height:70px;border-radius:18px"></i>'
        '<i class="im" style="left:106px;top:84px;width:70px;height:70px"></i>'
        '<i class="im" style="left:24px;top:166px;width:70px;height:70px"></i>'
        '<i class="hb" style="left:106px;top:166px;width:70px;height:70px;border-radius:18px;opacity:0.55"></i>'
        '<i class="rr" style="left:24px;top:262px;width:152px;height:14px"></i>'
        '<i class="rr" style="left:24px;top:286px;width:100px;height:14px"></i>',
        '<i class="im" style="left:24px;top:220px;width:30px;height:100px;border-radius:9px"></i>'
        '<i class="im" style="left:64px;top:180px;width:30px;height:140px;border-radius:9px"></i>'
        '<i class="im" style="left:104px;top:140px;width:30px;height:180px;border-radius:9px"></i>'
        '<i class="hb" style="left:144px;top:90px;width:30px;height:230px;border-radius:9px"></i>'
        '<i class="rr" style="left:24px;top:96px;width:100px;height:14px"></i>',
    ][i]
    return ('<div class="sc hide" id="sc%d" style="left:%dpx;top:%dpx">%s<div class="num" id="sn%d">%d</div>'
            '<div class="ok" id="so%d"><svg viewBox="0 0 24 24">%s</svg></div></div>'
            % (i, SC_X[i], SC_Y, inner, i, i + 1, i, STROKES["check"]))


@beat
def t_style():
    fx, fy, fw, fh = FC
    slots = "".join('<div class="slot" style="left:%dpx;top:%dpx"></div>' % (sx - fx, SLOT_Y - fy) for sx in SLOT_X)
    fcard = ('<div class="sheet fcard hide" id="fc" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx">'
             '<div class="tw" style="left:44px;top:46px;width:118px;height:118px"><div class="jelly">%s</div></div>'
             '<div class="ttl">style.md</div>%s<div class="sheen"></div></div>'
             % (fx, fy, fw, fh, stroke("doc"), slots))
    reels = ""
    for i, (x, y, rot, bg) in enumerate(RL):
        reels += ('<div class="abs hide" id="rl%d" style="left:%dpx;top:%dpx;width:340px;height:604px">'
                  '<div class="rl" style="left:0;top:0;transform:rotate(%ddeg)"><div class="ph" style="background:%s"></div>'
                  '<div class="fig"></div>%s<svg class="ig" viewBox="0 0 24 24"><use href="#i-instagram"/></svg>'
                  '<div class="bt"><i style="left:0;top:0;width:56px;height:56px;border-radius:50%%"></i>'
                  '<i style="left:72px;top:8px;width:150px;height:18px"></i>'
                  '<i style="left:72px;top:38px;width:96px;height:14px;opacity:0.6"></i></div></div>'
                  '%s</div>'
                  % (i, x, y, rot, bg, PLAY,
                     tile("ht%d" % i, 96, 228, 490, "jelly", '<svg class="hs" viewBox="0 0 24 24">%s</svg>' % STROKES["heart"],
                          extra_cls="circ hrt", ring=False)))
    g.mark("instagram")
    pb = ('<div class="pbw hide" id="pbw" style="left:70px;top:1030px;width:940px;height:170px">'
          '<div class="tw" style="left:30px;top:35px;width:100px;height:100px"><div class="jelly">%s</div></div>'
          '<div class="ptx" id="pT"></div>'
          '<div class="tw circ" id="pS" style="left:830px;top:40px;width:90px;height:90px"><div class="jelly">%s</div></div>'
          '</div>' % (g.mark("claude"), stroke("up")))
    lens = ('<div class="abs" id="lensW" style="left:0;top:0"><div class="lens hide" id="lens">'
            '<svg viewBox="0 0 24 24">%s</svg></div></div>' % STROKES["lens"])
    L.append('<div class="g full" id="gT1"><div class="tkg"></div><div class="aurs"></div><div class="grain"></div>'
             + fcard + reels + "".join(scene(i) for i in range(4)) + lens + pb + '</div>')
    sfx("whoosh-short", T["style"] - 0.2)
    sfx("pop", T["beresh"] + 0.02, -2)
    sfx("click-soft", T["podob"] + 0.05)
    sfx("typing", T["promtom"] - 0.05, -2)
    sfx("whoosh-short", T["rils"] - 0.02, -3)
    # middle reel -> four scenes
    mid_x, mid_y = RL[1][0] + 170, RL[1][1] + 302
    split = []
    for i in range(4):
        dx = mid_x - (SC_X[i] + 100)
        dy = mid_y - (SC_Y + 178)
        split.append('  tl.fromTo("#sc%d", {autoAlpha: 0, x: %d, y: %d, scale: 0.6}, {autoAlpha: 1, x: 0, y: 0, scale: 1, duration: 0.7, ease: SP}, @rils+%.2f);'
                     % (i, dx, dy, i * 0.06))
        split.append('  tl.fromTo("#sn%d", {autoAlpha: 0, scale: 0.3}, {autoAlpha: 1, scale: 1, duration: 0.4, ease: POP}, @stseny-0.1+%.2f);'
                     % (i, i * 0.08))
    hop = []
    t_an = T["analiz"] + 0.3
    for i in range(4):
        t = t_an + i * 0.26
        lx, ly = SC_X[i] + 25, SC_Y + 90
        if i == 0:
            hop.append('  tl.set("#lensW", {x: %d, y: %d}, 0); arr("#lens", %.3f, {s: 0.4, y: 0, d: 0.5, blur: 6});' % (lx, ly, t - 0.15))
        else:
            hop.append('  tl.to("#lensW", {x: %d, y: %d, duration: 0.22, ease: "power2.inOut"}, %.3f);' % (lx, ly, t - 0.2))
        hop.append('  tl.fromTo("#so%d", {autoAlpha: 0, scale: 0.3}, {autoAlpha: 1, scale: 1, duration: 0.35, ease: POP}, %.3f);'
                   % (i, t + 0.08))
    fly = []
    for i in range(4):
        fly.append('  tl.to("#sc%d", {x: %d, y: %d, scale: 0.32, transformOrigin: "0px 0px", duration: 0.55, ease: "power3.inOut"}, @zberih+%.2f);'
                   % (i, SLOT_X[i] - SC_X[i], SLOT_Y - SC_Y, i * 0.08))
    out = js("""
  G.irisOpen("#gT1", @style-0.2, {{nx}}, {{ny}}, 0.7);
  drift1("#gT1", @style-0.2, @pryklad-@style+1.2);
  arr("#fc", @style-0.02, {s: 0.5, y: -20, d: 0.8});
  shn("#fc .sheen", @style+0.35);
  [0, 1, 2].forEach(function (i) { arr("#rl" + i, @beresh-0.05 + [0.1, 0, 0.18][i], {s: 0.55, y: 160, d: 0.85}); });
  [0, 1, 2].forEach(function (i) { arr("#ht" + i, @podob-0.05 + i * 0.1, {s: 0.2, y: 20, d: 0.55, blur: 6}); });
  arr("#pbw", @spets-0.1, {s: 0.85, y: 60, d: 0.7});
  G.bump("#pS", @rils-0.2);
  bout(["#rl0", "#rl2"], @rozbyr+0.65, 10, 0.3);
  tl.to("#rl1", {scale: 0.6, autoAlpha: 0, duration: 0.3, ease: "power2.in"}, @rils-0.08);
{{split}}
  G.bump("#pS", @analiz+0.2);
{{hop}}
  bout("#lens", @zberih+0.1, 6, 0.22);
  bout("#pbw", @zberih-0.05, 10, 0.3);
{{fly}}
  G.bump("#fc", @pryklad-0.1);
  G.irisClose("#gT1", @okremo-0.6, {{n3x}}, {{ny}}, 0.5);""", )
    for key, v in {"split": "\n".join(split), "hop": "\n".join(hop), "fly": "\n".join(fly),
                   "nx": NX[1], "ny": NY, "n3x": NX[2]}.items():
        out = out.replace("{{%s}}" % key, js(str(v)))
    return out


# ===========================================================================
# C · station 3 — her own design system
@beat
def c_design():
    sw = "".join('<div class="sw" id="sw%d" style="left:%dpx;top:96px;background:%s%s"></div>'
                 % (i, 330 + i * 102, c, ";box-shadow:inset 0 0 0 2px rgba(23,20,28,0.12), 0 14px 26px -12px rgba(30,4,12,0.45)"
                    if c == "#fdf1f4" else "") for i, c in enumerate(SWATCH))
    card = ('<div class="sheet hide" id="ds" style="left:100px;top:222px;width:880px;height:376px">'
            '<div class="t-micro abs" id="dsH" style="left:52px;top:42px">ДИЗАЙН-СИСТЕМА</div>'
            '<div class="aa" id="dsA" style="left:44px;top:96px">Aa</div>%s'
            '<div class="btnp" id="dsB" style="left:330px;top:232px;width:260px;height:86px;font-size:34px">Кнопка</div>'
            '<div class="ty" id="dsT" style="left:640px;top:226px"><div style="font-size:44px;font-weight:900">H1</div>'
            '<div style="font-size:32px;font-weight:700;margin-top:10px;color:rgba(23,20,28,0.7)">H2</div>'
            '<div style="font-size:24px;font-weight:500;margin-top:10px;color:rgba(23,20,28,0.46)">Текст</div></div>'
            '<div class="sheen"></div></div>' % sw)
    L.append('<div class="g full" id="gC">' + card + '</div>')
    sfx("pop", T["hotuiesh"] - 0.05)
    return js("""
  tl.set("#gC", {autoAlpha: 1}, @okremo-0.1);
  arr("#ds", @okremo-0.02, {s: 0.6, y: 40, d: 0.8});
  [0, 1, 2, 3, 4].forEach(function (i) { tl.fromTo("#sw" + i, {autoAlpha: 0, scale: 0.2}, {autoAlpha: 1, scale: 1, duration: 0.45, ease: POP}, @hotuiesh-0.05 + i * 0.08); });
  tl.fromTo("#dsA", {autoAlpha: 0, y: 30}, {autoAlpha: 1, y: 0, duration: 0.5, ease: SP}, @vlasnu-0.05);
  tl.fromTo("#dsH", {autoAlpha: 0}, {autoAlpha: 1, duration: 0.25}, @dyzain-0.03);
  tl.fromTo("#dsB", {autoAlpha: 0, scale: 0.5}, {autoAlpha: 1, scale: 1, duration: 0.5, ease: POP}, @dyzain+0.15);
  tl.fromTo("#dsT", {autoAlpha: 0, x: 30}, {autoAlpha: 1, x: 0, duration: 0.45, ease: SP}, @dyzain+0.35);
  shn("#ds .sheen", @dyzain+0.6);
  bout("#gC", @pislia-0.12, 10, 0.26);""")


# ===========================================================================
# D · station 4 — a few test renders, each one checked
RC_X = [250, 458, 666]
RC_Y = 232


@beat
def d_tests():
    cards = ""
    for i, x in enumerate(RC_X):
        cards += ('<div class="abs hide" id="rc%d" style="left:%dpx;top:%dpx;width:164px;height:330px">'
                  '<div class="dglass edge rc" style="left:0;top:0;border-radius:30px"><div class="pp"></div><div class="pb2"></div>'
                  '<div class="cb"></div></div>'
                  '<div class="pgt" style="left:0;top:308px"><div class="pgf" id="rf%d"></div></div></div>'
                  % (i, x, RC_Y, i))
        cards += tile("rk%d" % i, 70, x + 118, RC_Y - 26, "jelly", stroke("check"), extra_cls="circ", ring=False)
    L.append('<div class="g full" id="gD">' + cards + '</div>')
    sfx("pop", T["kilka"] + 0.02)
    sfx("click", T["pratsiuie"] + 0.05)
    ticks = [T["pereviryty"] + 0.15, T["vzahali"] + 0.05, T["pratsiuie"] + 0.02]
    out = js("""
  tl.set("#gD", {autoAlpha: 1}, @kilka-0.15);
  [0, 1, 2].forEach(function (i) { arr("#rc" + i, @kilka-0.1 + i * 0.1, {s: 0.5, y: 40, d: 0.75}); });
  gsap.set(["#rf0", "#rf1", "#rf2"], {scaleX: 0});
  [0, 1, 2].forEach(function (i) { tl.to("#rf" + i, {scaleX: 1, duration: 0.75 + i * 0.12, ease: "power1.inOut"}, @testovykh + i * 0.18); });
  {{ticks}}
  bout("#gD", @pidkl-0.05, 10, 0.26);""")
    tj = "\n".join('  arr("#rk%d", %.3f, {s: 0.2, y: 0, d: 0.5, blur: 6});' % (i, t) for i, t in enumerate(ticks))
    return out.replace("{{ticks}}", tj)


# ===========================================================================
# TK2 · station 5 — the render goes to the cloud, not your computer
CLOUD = [(70, 300, 260), (330, 190, 300), (660, 170, 310), (950, 290, 270), (520, 360, 300), (220, 420, 210), (840, 430, 210)]
RQ_X = [320, 475, 630]
RQ_Y = 250
LP = (290, 860, 500, 300)


@beat
def t_cloud():
    circles = "".join('<circle cx="%d" cy="%d" r="%d"/>' % c for c in CLOUD)
    cloud = ('<svg class="cloud hide" id="cld" width="1080" height="720" viewBox="0 0 1080 720">'
             '<defs><linearGradient id="cg" x1="0" y1="0" x2="0" y2="720" gradientUnits="userSpaceOnUse">'
             '<stop offset="0.25" stop-color="#ffffff"/><stop offset="1" stop-color="#f6dbe3"/></linearGradient></defs>'
             '<g fill="url(#cg)">%s<rect x="-40" y="-40" width="1160" height="400"/></g></svg>' % circles)
    rq = "".join('<div class="rq hide" id="rq%d" style="left:%dpx;top:%dpx"><div class="pp"></div><div class="pb2"></div>'
                 '<div class="pgt"><div class="pgf" id="qf%d"></div></div></div>' % (i, x, RQ_Y, i)
                 for i, x in enumerate(RQ_X))
    x, y, w, h = LP
    lap = ('<div class="abs hide" id="lp2" style="left:0;top:0">'
           '<div class="lap" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx">'
           '<div class="rq" id="lrq" style="left:185px;top:36px;transform:scale(0.98)"><div class="pp"></div><div class="pb2"></div>'
           '<div class="pgt"><div class="pgf" id="lqf" style="transform:scaleX(0.18)"></div></div></div></div>'
           '<div class="lapb" style="left:%dpx;top:%dpx;width:%dpx;height:34px"><i></i></div></div>'
           % (x, y, w, h, x - 70, y + h, w + 140))
    cab = ('<svg class="cab abs" width="1080" height="1920" viewBox="0 0 1080 1920" style="left:0;top:0">'
           '<path class="tube hide" id="cT" d="M540 852 L540 600"/>'
           '<path class="core hide" id="cC" d="M540 852 L540 600"/>'
           '<g class="pkg"><path class="pkt" id="cP" style="opacity:0" d="M540 852 L540 600"/></g></svg>')
    L.append('<div class="g full" id="gT2"><div class="tkg"></div><div class="aurs"></div><div class="grain"></div>'
             + cab + cloud + rq + lap
             + tile("xk", 96, x + w - 60, y - 34, "jelly", stroke("x"), extra_cls="circ", ring=False)
             + '</div>')
    sfx("whoosh-short", T["pidkl"] + 0.05)
    sfx("pop", T["stvor"] - 0.05, -3)
    sfx("click", T["nena"] + 0.02, -2)
    return js("""
  G.irisOpen("#gT2", @pidkl+0.2, {{nx}}, {{ny}}, 0.7);
  drift1("#gT2", @pidkl+0.2, 4.6);
  tl.fromTo("#cld", {autoAlpha: 0, y: -160, scale: 1.08, transformOrigin: "540px 0px"},
            {autoAlpha: 1, y: 0, scale: 1, duration: 0.9, ease: SOFT}, @pidkl+0.35);
  arr("#lp2", @pidkl+0.45, {s: 0.8, y: 120, d: 0.8});
  tl.set(["#cT", "#cC"], {autoAlpha: 1}, @render-0.25);
  draw2("cT", @render-0.25, 0.35); draw2("cC", @render-0.25, 0.35);
  G.packet("cP", @render+0.1, 0.55);
  tl.to("#cld", {scale: 1.03, duration: 0.12, ease: "power2.out"}, @khmaru);
  tl.to("#cld", {scale: 1, duration: 0.5, ease: SP}, @khmaru+0.12);
  [0, 1, 2].forEach(function (i) { arr("#rq" + i, @stvor-0.1 + i * 0.1, {s: 0.4, y: 30, d: 0.6}); });
  gsap.set(["#qf0", "#qf1", "#qf2"], {scaleX: 0});
  [0, 1, 2].forEach(function (i) { tl.to("#qf" + i, {scaleX: 1, duration: 0.8, ease: "power1.inOut"}, @stvor+0.2 + i * 0.12); });
  arr("#xk", @nena-0.03, {s: 0.2, y: 0, d: 0.5, blur: 6});
  tl.to("#lrq", {autoAlpha: 0.35, duration: 0.3}, @nena+0.05);
  G.haptic("#lp2", @komp+0.05);
  G.irisClose("#gT2", @komp+0.5, {{n5x}}, {{ny}}, 0.45);""").replace("{{nx}}", str(NX[4])).replace(
        "{{ny}}", str(NY)).replace("{{n5x}}", str(NX[4]))


# ===========================================================================
# E · two days -> one hour; the steps pass to you
@beat
def e_time():
    front = ('<div class="calc" id="cF"><div class="hd"><div class="hole" style="left:120px"></div>'
             '<div class="hole" style="left:276px"></div></div>'
             '<div class="big" id="cN">2</div><div class="lb" id="cL">дні</div>'
             '<div class="shc"><div class="sheen"></div></div></div>')
    back = ('<div class="calc" id="cB"><div class="hd">%s</div>'
            '<div class="big">1</div><div class="lb">година</div></div>'
            % ('<svg viewBox="0 0 24 24">%s</svg>' % STROKES["clock"]))
    cal = '<div class="calw hide" id="cal" style="left:330px;top:196px;width:420px;height:390px">%s%s</div>' % (front, back)
    rows = ""
    for i in range(5):
        y = 34 + i * 46
        rows += ('<div class="ck" style="top:%dpx"><svg viewBox="0 0 24 24">%s</svg></div>'
                 '<i class="rr" style="left:76px;top:%dpx;width:%dpx;height:16px;border-radius:8px"></i>'
                 % (y, STROKES["check"], y + 9, (112, 96, 124, 84, 104)[i]))
    gdoc = '<div class="gdoc hide" id="gdoc" style="left:480px;top:250px;width:220px;height:280px">%s</div>' % rows
    L.append('<div class="g full" id="gE">' + cal + gdoc
             + tile("you", 170, 770, 300, "pearl", stroke("person"), extra_cls="circ")
             + tile("dn", 92, 690, 168, "jelly", stroke("down"), extra_cls="circ", ring=False)
             + '</div>')
    sfx("pop", T["zainialo"] + 0.02)
    sfx("whoosh-short", T["peredaty"] + 0.05, -3)
    sfx("whoosh-short", T["hodynu"] - 0.1, -2)
    return js("""
  tl.set("#gE", {autoAlpha: 1}, @zainialo-0.1);
  gsap.set(["#cF", "#cB"], {transformPerspective: 1400});
  gsap.set("#cB", {rotationY: -90, autoAlpha: 0});
  arr("#cal", @zainialo-0.02, {s: 0.5, y: 40, d: 0.8});
  tl.fromTo("#cN", {autoAlpha: 0, scale: 1.6}, {autoAlpha: 1, scale: 1, duration: 0.5, ease: POP}, @dva-0.05);
  tl.fromTo("#cL", {autoAlpha: 0, y: 20}, {autoAlpha: 1, y: 0, duration: 0.35, ease: SP}, @dni-0.05);
  gsap.set(["#cN", "#cL"], {autoAlpha: 0});
  shn("#cF .sheen", @dni+0.2);
  /* the calendar steps aside, the five ticked steps go to you */
  tl.to("#cal", {x: -230, scale: 0.78, duration: 0.6, ease: SP}, @ale-0.05);
  arr("#gdoc", @teper-0.1, {s: 0.4, y: 30, d: 0.7});
  arr("#you", @znaiu-0.12, {s: 0.4, y: 20, d: 0.7});
  tl.to("#gdoc", {x: 265, y: -5, scale: 0.3, autoAlpha: 0, duration: 0.55, ease: "power3.in"}, @peredaty);
  G.bump("#you", @tobi+0.05); G.ripple("#youR", @tobi+0.05);
  bout("#you", @shchob+0.1, 10, 0.3);
  tl.to("#cal", {x: 0, scale: 1, duration: 0.7, ease: SP}, @shchob+0.15);
  /* 2 days flip to 1 hour */
  tl.to("#cF", {rotationY: 90, duration: 0.2, ease: "power2.in"}, @hodynu-0.2);
  tl.set("#cF", {autoAlpha: 0}, @hodynu);
  tl.set("#cB", {autoAlpha: 1}, @hodynu);
  tl.to("#cB", {rotationY: 0, duration: 0.7, ease: FLIP}, @hodynu);
  arr("#dn", @abo-0.02, {s: 0.2, y: -20, d: 0.55, blur: 6});
  tl.to("#dn", {y: 18, duration: 0.5, ease: SP}, @menshe);
  bout("#gE", @menshee-0.05, 10, 0.26);""")


# ===========================================================================
# F · CTA — comment «design», her DM brings the design system back
@beat
def f_cta():
    cmt = ('<div class="cmt hide" id="cmt" style="left:70px;top:478px;width:940px;height:120px">'
           '<div class="avp">%s</div><div class="phd2" id="cmPh">Додати коментар…</div><div id="cmT"></div>'
           '<div class="tw circ" id="cmS" style="left:836px;top:16px;width:88px;height:88px"><div class="jelly">%s</div></div>'
           '</div>' % ('<svg viewBox="0 0 24 24">%s</svg>' % STROKES["person"], stroke("up")))
    sw = "".join('<div class="sw" style="left:%dpx;top:42px;width:64px;height:64px;background:%s"></div>'
                 % (220 + i * 74, c) for i, c in enumerate(SWATCH))
    mini = ('<div class="mini" id="mini" style="left:166px;top:112px;width:620px;height:150px">'
            '<div class="aa" style="left:34px;top:22px;font-size:104px">Aa</div>%s</div>' % sw)
    dm = ('<div class="dglass edge hide" id="dm" style="left:70px;top:110px;width:940px;height:300px">'
          '<div class="tw" style="left:36px;top:36px;width:104px;height:104px"><div class="jelly">%s</div></div>'
          '<div class="app">Instagram</div><div class="tm">зараз</div>%s'
          '<div class="shc"><div class="sheen"></div></div></div>' % (g.mark("instagram"), mini))
    free = '<div class="free hide" id="free" style="left:640px;top:350px">безкоштовно</div>'
    L.append('<div class="g full" id="gF">' + dm + cmt + free + '</div>')
    sfx("typing", T["design"] + 0.02, -2)
    sfx("notification", T["nadishliu"] + 0.02, -2)
    sfx("sparkle", T["bezk"] + 0.05, -3)
    return js("""
  tl.set("#gF", {autoAlpha: 1}, @napyshy-0.15);
  arr("#cmt", @napyshy-0.08, {s: 0.7, y: 40, d: 0.75});
  tl.set("#cmPh", {autoAlpha: 0}, @design);
  G.bump("#cmS", @designe+0.05);
  tl.fromTo("#dm", {autoAlpha: 0, y: -260, scale: 0.92}, {autoAlpha: 1, y: 0, scale: 1, duration: 0.9, ease: SOFT}, @nadishliu-0.1);
  G.haptic("#dm", @nadishliu+0.45);
  tl.fromTo("#mini", {autoAlpha: 0, scale: 0.6}, {autoAlpha: 1, scale: 1, duration: 0.6, ease: POP}, @dyzain2-0.05);
  shn("#dm .sheen", @dyzain2+0.3);
  arr("#free", @bezk-0.04, {s: 0.3, y: 20, d: 0.7});""")


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

TYPES = [
    # element, text, start, end, cleared at
    ("pT", P1, "promtom", 0.0, "rils", -0.25, "dali", 0.0),
    ("pT", P2, "inshyi", 0.0, "analiz", 0.15, None, 0.0),
    ("cmT", u"design", "design", 0.0, "designe", -0.1, None, 0.0),
]


def typing_js():
    """Every typed field is painted from one clock, so any frame renders cold."""
    items = []
    for el, txt, a, ao, b, bo, c, co in TYPES:
        items.append({"el": el, "tx": txt, "t0": round(T[a] + ao, 3), "t1": round(T[b] + bo, 3),
                      "tc": round(T[c] + co, 3) if c else 999.0})
    return r"""
  var CLK = {t: 0}, TYP = %s, TEL = {}, TCUR = {};
  TYP.forEach(function (it) { TEL[it.el] = document.getElementById(it.el); });
  function paintAll() {
    var t = CLK.t, want = {};
    TYP.forEach(function (it) {
      if (t < it.t0 || t >= it.tc) { if (!(it.el in want)) want[it.el] = ""; return; }
      var n = t >= it.t1 ? it.tx.length : Math.round(it.tx.length * (t - it.t0) / (it.t1 - it.t0));
      want[it.el] = it.tx.slice(0, n);
    });
    for (var e in want) { if (TCUR[e] !== want[e]) { TCUR[e] = want[e]; TEL[e].textContent = want[e]; } }
  }
  tl.fromTo(CLK, {t: 0}, {t: %.3f, duration: %.3f, ease: "none", onUpdate: paintAll}, 0);""" % (
        json.dumps(items, ensure_ascii=False), DUR, DUR)


# captions that would repeat the graphic's own words (STYLE.md §2b.1)
def span(a, b):
    return (round(a - 0.02, 3), round(b + 0.02, 3), "")


BLACKOUT = [
    span(T["a"], T["montazhe"]),                       # the Threads post says the question
    span(T["style"], T["stylee"]),                     # the file card says style.md
    span(T["rozbyr"], T["stsenye"]),                   # prompt 1 types «розбий цей рілс на сцени»
    span(T["analiz"], T["stsenue"]),                   # prompt 2 types «проаналізуй кожну сцену»
    span(T["dyzain"], T["dyzaine"]),                   # the card header says ДИЗАЙН-СИСТЕМА
    span(T["dva"], T["dnie"]),                         # the calendar says 2 дні
    span(T["za"], T["hodynue"]),                       # the calendar says 1 година
    span(T["design"], T["designe"]),                   # the comment types design
    span(T["bezk"], DUR),                              # the chip says безкоштовно
]


def check_rules():
    a, b = JOKE
    assert T["montazhe"] <= a + 0.01, "the post must be gone before «Пффф»"
    assert T["spochatku"] - 0.1 >= b - 0.01, "the rail must not arrive inside the joke"
    for s in SFX:
        assert not (a <= s["t"] <= b)
    span_s = DUR
    rate = len(SFX) / span_s
    assert rate <= 0.55, ("too many sfx", rate)


def main():
    gj = []
    for fn in BEATS:
        j = fn()
        gj.append("  /* %s */" % fn.__name__)
        gj.append(j.rstrip())
    check_rules()
    push = ["#vid"]
    head = [g.js(), HEAD_JS, typing_js(),
            '  gsap.set(%s, {transformOrigin: "540px 900px"});' % json.dumps(push),
            '  tl.fromTo(%s, {scale: 1}, {scale: 1.045, duration: %.3f, ease: "none"}, 0);' % (json.dumps(push), DUR)]
    doc = k.document(
        title=u"Reel 36 — Pinterest → дизайн-система",
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
