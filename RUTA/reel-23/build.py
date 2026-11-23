# -*- coding: utf-8 -*-
"""Reel 23 — «Якщо ти плануєш провести вебінар…». Posts 2026-10-06.

An explainer, and she promises it in one minute, so the chain is fast. The one
object is **the webinar's pipeline**: a slide, OBS, YouTube, Webinar Stars —
four pieces that end up in one line and go LIVE.

Chain:  near: a webinar screen lands (LIVE), its presenter flips from «ти» to
«клієнтка» -> the screen steps aside for a 1:00 stopwatch and a settings
badge -> curtains close over the lot («за кулісами») -> a backstage pass swings
down in front of them: RUTA, технічна продюсерка -> the curtains open on three
webinar screens with bloggers -> they collapse into «від 13 000 €» (kaching)
-> «Погнали»: the iris opens out of the € -> the slide arrives 16:9, morphs to
1:1; the old 16:9 is left behind and crossed out; trend badge, tick -> OBS
assembles around the slide: the slide drops into the canvas, her live camera
drops in beside it, the sources list fills, OBS names itself; the canvas lights
up, an eye for the viewer -> the iris closes onto the OBS tile above her head:
cable to YouTube, the link travels on to Webinar Stars -> the iris opens out of
Webinar Stars: the registration page is set up (title types, details, the
button), a phone wraps it, a tap registers -> the iris closes onto the four
pieces scattered on a shelf; they snap into one line, cables, LIVE -> the
checklist (0 €) ticks itself -> a DM types ВЕБІНАР, sends, the guide comes back.

usage: python build.py   (then: python ../tools/sfx.py mix 23)
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

CUT = json.load(io.open(os.path.join(ROOT, "work", "r23", "cut.json"), encoding="utf-8"))
DUR = 53.883           # (plate frames - 0.5) / 30, set from the plate after cut.py --render
FPS = 30
k = Kit(width=1080, height=1920, fps=FPS, duration=DUR)
g = Glass(["obsstudio", "youtube", "instagram"])
k.css(g.css())

# NO-PAINT: the closeup cut.py punched in on «Погнали!» — her joke, captions only.
NO_PAINT = [tuple(x) for x in CUT["no_paint"]]
assert len(NO_PAINT) == 1, NO_PAINT
NP0, NP1 = NO_PAINT[0]

CAPS = k.load_captions(os.path.join(ROOT, "work", "r23", "captions.json"))
# whisper errors the aligner kept as "her wording": restore the script word
FIX = {u"готовий": u"готова", u"якусь": u"як у", u"вбачать": u"бачить", u"Тою": u"Той", u"без": u"OBS",
       u"Ютубу,": u"YouTube,", u"з Ютуб": u"з YouTube", u"А": u"а", u"його)": u"його.",
       u"Погнали": u"Погнали!"}
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
    "planuiesh": S(u"плануєш", 0.79), "vebinar": S(u"вебінар", 1.51), "sebe": S(u"себе", 2.11),
    "kliientky": S(u"клієнтки", 2.91), "zaraz": S(u"зараз", 3.41), "odnu": S(u"одну", 4.27),
    "khvylynu": S(u"хвилину", 4.43), "khvylynue": E(u"хвилину", 4.43),
    "nalasht": S(u"налаштувати", 6.35), "kulisamy": S(u"кулісами", 7.05), "tomu": S(u"тому", 7.48),
    "ruta": S(u"Рута", 7.80), "prod": S(u"продюсерка", 8.76), "prode": E(u"продюсерка", 8.76),
    "moikh": S(u"моїх", 9.82), "vebinariv": S(u"вебінарів", 10.11), "bloh": S(u"блогерки", 10.54),
    "zarobl": S(u"заробляють", 10.96), "vid": S(u"від", 11.40), "n13": S("13", 11.62),
    "tysiach": S(u"тисяч", 12.19), "ievro": S(u"євро", 13.03), "ievroe": E(u"євро", 13.03),
    "pohnaly": S(u"Погнали", 13.75),
    "prez1": S(u"презентації", 15.12), "vazhlyvo": S(u"важливо", 16.06), "format": S(u"формат", 16.66),
    "odyn": S(u"один", 17.04), "odyn2e": E(u"один", 17.62), "ne": S(u"не", 18.08),
    "n16": S("16", 18.24), "n9": S("9", 18.86), "n9e": E("9", 18.86),
    "zvych": S(u"звичайній", 19.35), "prez2": S(u"презентації", 19.71), "prez2e": E(u"презентації", 19.71),
    "trend": S(u"трендовий", 21.15), "potriben": S(u"потрібен", 22.05), "same": S(u"саме", 22.39),
    "takyi": S(u"такий", 22.67),
    "dali": S(u"Далі", 24.56), "prezent": S(u"презентацію", 25.04), "liudynu": S(u"людину", 25.78),
    "samu": S(u"саму", 25.52), "stavysh": S(u"ставиш", 26.06), "obs": S("OBS", 26.80), "obse": E("OBS", 26.80),
    "prohrama": S(u"програма", 27.80), "vsia": S(u"вся", 28.72), "kartynka": S(u"картинка", 28.84),
    "bachyt": S(u"бачить", 29.78), "hliadach": S(u"глядач", 30.14),
    "toi": S(u"Той", 30.83), "obs2": S("OBS", 31.18), "pidkl": S(u"підключаєш", 31.39),
    "youtube": S("YouTube", 32.30), "posyl": S(u"посилання", 33.12), "zyoutube": S("YouTube", 33.62),
    "vede": S(u"веде", 34.19), "webinar": S("Webinar", 34.69), "starse": E("Stars", 35.09),
    "same2": S(u"саме", 35.86), "nalashtovuiesh": S(u"налаштовуєш", 36.32), "nazvu": S(u"назву", 37.02),
    "vsi": S(u"всі", 37.54), "detali": S(u"деталі", 37.66), "robochi": S(u"робочі", 38.24),
    "knopky": S(u"кнопки", 38.50), "finalnu": S(u"фінальну", 39.08), "obhortku": S(u"обгортку", 39.50),
    "bachyt2": S(u"бачить", 40.42), "liudyna": S(u"людина", 40.76), "reiestr": S(u"реєструється", 41.24),
    "reiestre": E(u"реєструється", 41.24),
    "tilky": S(u"тільки", 42.35), "vsi2": S(u"всі", 42.89), "shmatky": S(u"шматки", 43.27),
    "zibrani": S(u"зібрані", 43.67), "liniiu": S(u"лінію", 44.51), "hotovyi": S(u"готова", 45.09),
    "zapusk": S(u"запускати", 45.53), "vebinar2": S(u"вебінар", 46.11), "vebinar2e": E(u"вебінар", 46.11),
    "rechi": S(u"речі", 47.88), "mene": S(u"мене", 48.28), "bezk": S(u"безкоштовний", 48.66),
    "haid": S(u"гайд-чекліст", 49.58), "nalasht2": S(u"налаштуванню", 50.70), "vebinara": S(u"вебінара", 51.24),
    "tomu2": S(u"тому", 51.70), "pyshy": S(u"пиши", 51.86), "VEB": S(u"ВЕБІНАР", 52.26), "VEBe": E(u"ВЕБІНАР", 52.26),
    "shchob": S(u"щоб", 53.04), "zabraty": S(u"забрати", 53.14), "yoho": S(u"його", 53.56),
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
# Sound design (tools/sfx.py). Quiet, on the event.
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
    "trend": '<path d="M3.5 17.2l5.6-5.6 4 4 7.4-7.4"/><path d="M14.6 8.2h5.9v5.9"/>',
    "eye": '<path d="M2.4 12s3.6-6.4 9.6-6.4 9.6 6.4 9.6 6.4-3.6 6.4-9.6 6.4S2.4 12 2.4 12z"/><circle cx="12" cy="12" r="2.9"/>',
    "link": ('<path d="M10.2 13.8a4.3 4.3 0 0 0 6.1 0l2.9-2.9a4.3 4.3 0 0 0-6.1-6.1l-1.3 1.3"/>'
             '<path d="M13.8 10.2a4.3 4.3 0 0 0-6.1 0l-2.9 2.9a4.3 4.3 0 0 0 6.1 6.1l1.3-1.3"/>'),
    "cal": '<rect x="3.6" y="5.2" width="16.8" height="15" rx="3"/><path d="M3.6 10.2h16.8M8.2 3.2v4M15.8 3.2v4"/>',
    "clock": '<circle cx="12" cy="12" r="8.4"/><path d="M12 7.4V12l3.1 2"/>',
    "mic": '<rect x="9" y="3.4" width="6" height="10.6" rx="3"/><path d="M5.8 11.4a6.2 6.2 0 0 0 12.4 0M12 17.6v3"/>',
    "cam": '<rect x="2.8" y="6.6" width="12.8" height="10.8" rx="2.6"/><path d="M15.6 10.6l5.4-3.1v9l-5.4-3.1"/>',
    "slide": '<rect x="4" y="4" width="16" height="16" rx="2.6"/><path d="M7.6 8.6h6M7.6 12h8.8M7.6 15.4h5"/>',
    "send": '<path d="M20.6 3.4L3.6 10.4l7 3 3 7z"/><path d="M10.6 13.4l10-10"/>',
    "x": '<path d="M6 6l12 12M18 6L6 18"/>',
}
SLIDERS = ('<svg class="sk" viewBox="0 0 24 24"><path d="M4 7.5h16M4 16.5h16"/>'
           '<circle id="knA" cx="8" cy="7.5" r="2.5" class="kn"/><circle id="knB" cx="16" cy="16.5" r="2.5" class="kn"/></svg>')


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
    """Webinar Stars has no icon: the wordmark, two lines."""
    return ('<span class="wmark wsm" style="font-size:%dpx">Webinar<br>Stars</span>' % size)


def mini_slide(cls=""):
    """a 1:1 slide in miniature: heading bar, three lines, a picture"""
    return ('<div class="msl %s"><i class="hb" style="left:14%%;top:14%%;width:52%%;height:9%%"></i>'
            '<i class="rr" style="left:14%%;top:30%%;width:40%%;height:5%%"></i>'
            '<i class="rr" style="left:14%%;top:39%%;width:32%%;height:5%%"></i>'
            '<i class="im" style="left:14%%;top:52%%;width:72%%;height:34%%"></i></div>' % cls)


k.css("""
.abs { position: absolute; }
.hide { opacity: 0; visibility: hidden; }
.tw { position: absolute; }
.sk { fill: none; stroke: url(#gw); stroke-width: 2.3; stroke-linecap: round; stroke-linejoin: round;
  width: 50%; height: 50%; position: relative; z-index: 1; overflow: visible; }
.pearl .sk { stroke: #17141c; }
.kn { fill: #17141c; stroke: none; }
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
.im { position: absolute; display: block; border-radius: 22px; background: linear-gradient(150deg, #f4dfe5 0%, #ecc8d0 100%); }
.live { position: absolute; display: flex; align-items: center; justify-content: center; gap: 12px;
  background: linear-gradient(165deg, #e0204b 0%, #8d0d24 100%); color: #fff; font-weight: 900;
  letter-spacing: 0.06em; box-shadow: inset 0 2px 1px rgba(255,255,255,0.5), 0 20px 40px -16px rgba(70,4,20,0.7); }
.live b { width: 16px; height: 16px; border-radius: 50%; background: #fff; display: block; }
.pill { position: absolute; display: flex; align-items: center; justify-content: center; border-radius: 999px;
  font-weight: 900; letter-spacing: -0.01em; }
.pill.j { background: linear-gradient(165deg, #e0204b 0%, #ab112e 46%, #6b081c 100%); color: #fff;
  box-shadow: inset 0 2px 1px rgba(255,255,255,0.55), inset 0 -14px 24px -12px rgba(255,125,165,0.6), 0 26px 50px -20px rgba(8,0,3,0.7); }
.pill.p { background: linear-gradient(160deg, #ffffff 0%, #fff5f8 52%, #f5dfe6 100%); color: #17141c;
  box-shadow: inset 0 2px 1px #fff, 0 26px 50px -20px rgba(8,0,3,0.7); }

/* A · the webinar screen */
.scr .pres { position: absolute; left: 265px; top: 88px; width: 190px; height: 190px; perspective: 900px; }
.scr .face { position: absolute; inset: 0; }
.scr .trk { position: absolute; left: 34px; top: 362px; width: 652px; height: 12px; border-radius: 6px;
  background: rgba(255,255,255,0.22); overflow: hidden; }
.scr .fil { position: absolute; left: 0; top: 0; width: 652px; height: 12px; border-radius: 6px;
  background: linear-gradient(90deg, #ff6e9c, #ffd6e3); transform-origin: 0 50%; }
.ring1 { position: absolute; fill: none; stroke: #ffd6e3; stroke-width: 12; stroke-linecap: round;
  filter: drop-shadow(0 0 10px rgba(255,110,156,0.9)); }
.dig { position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; z-index: 2;
  color: #fff; font-size: 74px; font-weight: 900; letter-spacing: -0.03em; }

/* the curtains */
.drape { position: absolute; top: 96px; width: 580px; height: 520px; border-radius: 0 0 46px 46px;
  background:
    linear-gradient(180deg, rgba(255,255,255,0.10) 0%, rgba(0,0,0,0) 30%, rgba(20,0,6,0.45) 100%),
    repeating-linear-gradient(90deg, #4f0819 0px, #7a0b22 22px, #b4122f 40px, #c8203f 46px, #8d0d24 62px, #4f0819 84px);
  box-shadow: 0 50px 90px -30px rgba(10,0,4,0.7), inset 0 -3px 0 rgba(255,140,175,0.5); }
.val { position: absolute; left: -30px; top: 70px; width: 1140px; height: 74px; border-radius: 0 0 38px 38px;
  background: linear-gradient(180deg, #8d0d24 0%, #5e0819 100%);
  box-shadow: inset 0 -5px 0 #ff8ab0, 0 24px 40px -14px rgba(10,0,4,0.7); }

/* the backstage pass */
.lan { position: absolute; fill: none; stroke-linecap: round; }
.lan .s1 { stroke: #b4122f; stroke-width: 24; }
.lan .s2 { stroke: #ff8ab0; stroke-width: 6; }
.bdg { position: absolute; border-radius: 44px; overflow: hidden;
  background: linear-gradient(160deg, #ffffff 0%, #fff7fa 60%, #f7e3ea 100%);
  box-shadow: inset 0 2px 1px #fff, 0 50px 90px -30px rgba(24,4,12,0.7); }
.bdg .top { position: absolute; left: 0; top: 0; right: 0; height: 78px;
  background: linear-gradient(165deg, #e0204b 0%, #8d0d24 100%); }
.bdg .slot { position: absolute; left: 180px; top: 26px; width: 100px; height: 24px; border-radius: 12px;
  background: rgba(255,255,255,0.88); }
.bdg .nm { position: absolute; left: 0; right: 0; top: 104px; text-align: center; }
.bdg .rl { position: absolute; left: 0; right: 0; top: 248px; text-align: center; font-size: 24px; font-weight: 700;
  letter-spacing: 0.16em; color: rgba(23,20,28,0.5); }
.clip { position: absolute; left: 510px; top: 200px; width: 60px; height: 44px; border-radius: 12px;
  background: linear-gradient(180deg, #ffffff 0%, #d9c9cf 100%); box-shadow: 0 6px 12px rgba(24,4,12,0.4); }

/* mini webinar screens */
.msc { position: absolute; border-radius: 40px; }
.msc .live { left: 22px; top: 20px; height: 34px; padding: 0 14px; border-radius: 17px; font-size: 16px; gap: 7px; }
.msc .live b { width: 10px; height: 10px; }

/* the money card */
.mny .lb { position: absolute; left: 64px; top: 46px; }
.mny .num { position: absolute; left: 56px; top: 96px; white-space: nowrap; }
.mny .eur { display: inline-block; margin-left: 26px; }

/* TK1 · the slide */
.slS { position: absolute; inset: 0;
  background: linear-gradient(172deg, #ffffff 0%, #fff9fb 55%, #fdf0f4 100%); }
.slS .sheen { mix-blend-mode: normal; opacity: 0.6; }
.slW { position: absolute; left: 0; top: 0; width: 1000px; height: 1000px; transform-origin: 50% 50%;
  filter: drop-shadow(0 46px 60px rgba(8,0,3,0.55)); }
.card169 { position: absolute; border-radius: 30px; overflow: hidden;
  background: linear-gradient(172deg, #ffffff 0%, #fff9fb 55%, #fdf0f4 100%);
  box-shadow: inset 0 2px 1px #fff, 0 40px 80px -30px rgba(8,0,3,0.7); }
.xs { position: absolute; fill: none; stroke: #ff3d6e; stroke-width: 9; stroke-linecap: round;
  filter: drop-shadow(0 6px 10px rgba(60,0,14,0.5)); }

/* OBS */
.obs { position: absolute; border-radius: 48px; overflow: hidden;
  background: linear-gradient(170deg, #2b2330 0%, #1b161f 60%, #151118 100%);
  box-shadow: inset 0 1.5px 0 rgba(255,255,255,0.18), inset 0 0 0 1px rgba(255,255,255,0.07),
              0 70px 130px -40px rgba(8,0,3,0.85); }
.obs .tt { position: absolute; left: 116px; top: 0; height: 92px; line-height: 92px; font-size: 34px; font-weight: 700;
  color: rgba(255,255,255,0.88); letter-spacing: -0.01em; }
.obs .wd { position: absolute; top: 36px; width: 18px; height: 18px; border-radius: 50%; background: rgba(255,255,255,0.18); }
.obs .cv { position: absolute; left: 30px; top: 96px; width: 900px; height: 506px; border-radius: 26px; overflow: hidden;
  background: radial-gradient(ellipse at 50% 40%, #241c26 0%, #0c090e 75%);
  box-shadow: inset 0 0 0 1.5px rgba(255,255,255,0.08); }
.obs .oph { position: absolute; top: 632px; font-size: 22px; font-weight: 700; letter-spacing: 0.16em;
  color: rgba(255,255,255,0.42); }
.obs .pn { position: absolute; top: 676px; height: 272px; border-radius: 26px; background: rgba(255,255,255,0.05);
  box-shadow: inset 0 0 0 1px rgba(255,255,255,0.06); }
.orow { position: absolute; left: 16px; right: 16px; height: 70px; border-radius: 18px; display: flex; align-items: center;
  gap: 16px; padding-left: 18px; font-size: 30px; font-weight: 700; color: rgba(255,255,255,0.9); }
.orow.on { background: linear-gradient(165deg, rgba(224,32,75,0.9) 0%, rgba(141,13,36,0.9) 100%);
  box-shadow: inset 0 1.5px 1px rgba(255,255,255,0.35); }
.orow .sk { width: 38px; height: 38px; stroke: #ffd6e3; flex: none; }
.pip { position: absolute; border-radius: 26px; overflow: hidden; background: #1b161f;
  box-shadow: 0 0 0 3px rgba(255,255,255,0.9), 0 24px 40px -14px rgba(0,0,0,0.7); }
.vw { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; transform-origin: 0 0; }
.vw video, video.vv { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; }
.rec { position: absolute; left: 18px; top: 16px; height: 40px; padding: 0 14px; border-radius: 20px; display: flex;
  align-items: center; gap: 8px; background: rgba(23,20,28,0.55); color: #fff; font-size: 20px; font-weight: 700;
  letter-spacing: 0.08em; }
.rec b { width: 12px; height: 12px; border-radius: 50%; background: #ff3d6e; display: block; }
.cvg { position: absolute; fill: none; stroke: #ff8ab0; stroke-width: 9; stroke-linecap: round;
  filter: drop-shadow(0 0 12px rgba(255,110,156,0.95)) drop-shadow(0 0 30px rgba(255,110,156,0.6)); }

/* cables */
.cab .tube { fill: none; stroke: rgba(255,255,255,0.30); stroke-width: 20; stroke-linecap: round; }
.cab .core { fill: none; stroke: rgba(255,255,255,0.94); stroke-width: 4.5; stroke-linecap: round; }

/* the link pill */
.lnk { position: absolute; height: 76px; border-radius: 38px; display: flex; align-items: center; gap: 14px; padding: 0 26px 0 18px;
  background: linear-gradient(160deg, #ffffff 0%, #fff5f8 52%, #f5dfe6 100%); color: #17141c; font-size: 28px; font-weight: 700;
  letter-spacing: -0.01em; white-space: nowrap; box-shadow: inset 0 2px 1px #fff, 0 26px 50px -20px rgba(24,4,12,0.7); }
.lnk .lc { width: 48px; height: 48px; border-radius: 50%; display: flex; align-items: center; justify-content: center;
  background: linear-gradient(165deg, #e0204b 0%, #8d0d24 100%); }
.lnk .lc .sk { width: 30px; height: 30px; }
.lnk em { font-style: normal; color: rgba(23,20,28,0.45); }

/* TK2 · the registration page in a phone */
.bez { position: absolute; border-radius: 100px;
  background: linear-gradient(160deg, #2e2630 0%, #151116 100%);
  box-shadow: inset 0 2px 1px rgba(255,255,255,0.3), inset 0 0 0 2px rgba(255,255,255,0.08), 0 70px 130px -40px rgba(8,0,3,0.85); }
.bez .isl { position: absolute; left: 270px; top: 26px; width: 160px; height: 44px; border-radius: 22px; background: #050405; }
.pg { position: absolute; border-radius: 72px; overflow: hidden; color: #17141c;
  background: linear-gradient(172deg, #ffffff 0%, #fff9fb 55%, #fdf0f4 100%);
  box-shadow: inset 0 2px 1px #fff, 0 70px 130px -40px rgba(8,0,3,0.75), 0 0 0 1px rgba(255,255,255,0.35); }
.pg .brand { position: absolute; left: 50px; top: 84px; font-size: 32px; font-weight: 900; color: #b4122f; letter-spacing: -0.03em; }
.pg .hair2 { position: absolute; left: 50px; right: 50px; top: 140px; height: 2px; background: rgba(23,20,28,0.08); }
.pg .ttl { position: absolute; left: 50px; top: 446px; width: 540px; font-size: 60px; font-weight: 900; letter-spacing: -0.03em;
  line-height: 1.05; white-space: nowrap; }
.pg .ttl::after { content: ""; display: inline-block; width: 4px; height: 56px; margin-left: 4px; vertical-align: -6px;
  background: #e0204b; }
.pg .tbox { position: absolute; left: 34px; top: 428px; width: 572px; height: 100px; border-radius: 24px;
  border: 4px dashed rgba(224,32,75,0.7); }
.drow { position: absolute; left: 50px; height: 60px; }
.drow .ic { position: absolute; left: 0; top: 0; width: 60px; height: 60px; border-radius: 50%; background: #fbe3ea;
  display: flex; align-items: center; justify-content: center; }
.drow .ic .sk { width: 34px; height: 34px; stroke: #b4122f; }
.drow .rr { left: 84px; top: 19px; height: 22px; }
.rbtn { position: absolute; left: 50px; top: 820px; width: 540px; height: 116px; border-radius: 58px; color: #fff;
  font-size: 40px; font-weight: 700; display: flex; align-items: center; justify-content: center; letter-spacing: -0.01em;
  background: linear-gradient(165deg, #e0204b 0%, #ab112e 46%, #6b081c 100%);
  box-shadow: inset 0 2px 1px rgba(255,255,255,0.5), 0 24px 44px -16px rgba(70,4,20,0.65); }
.rbtn .lbl, .rbtn .okk { position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; }
.rbtn .okk .sk { width: 64px; height: 64px; stroke: #fff; stroke-width: 3; }
.ckr { position: absolute; width: 140px; height: 140px; margin: -70px 0 0 -70px; border-radius: 50%;
  border: 8px solid #ff6e9c; opacity: 0; visibility: hidden; z-index: 5; }
.fing { position: absolute; width: 84px; height: 84px; margin: -42px 0 0 -42px; border-radius: 50%;
  background: rgba(255,255,255,0.55); box-shadow: 0 0 0 3px rgba(255,255,255,0.9), 0 10px 24px rgba(24,4,12,0.35); z-index: 6; }

/* line-up tiles: the slide in miniature */
.msl { position: absolute; inset: 14%; border-radius: 16%; background: #fff;
  box-shadow: 0 0 0 2px rgba(23,20,28,0.08); z-index: 1; }
.msl i { position: absolute; display: block; }
.msl .hb { border-radius: 4px; } .msl .rr { border-radius: 3px; } .msl .im { border-radius: 6px; }

/* CTA · checklist + DM */
.lst { position: absolute; border-radius: 52px; overflow: hidden;
  background: linear-gradient(172deg, #ffffff 0%, #fff9fb 55%, #fdf0f4 100%);
  box-shadow: inset 0 2px 1px #fff, 0 50px 100px -36px rgba(24,4,12,0.62); }
.cbx { position: absolute; width: 50px; height: 50px; border-radius: 15px; box-shadow: inset 0 0 0 4px rgba(23,20,28,0.22); }
.cbf { position: absolute; inset: 0; border-radius: 15px;
  background: linear-gradient(165deg, #e0204b 0%, #8d0d24 100%); opacity: 0; visibility: hidden; }
.cbf svg { position: absolute; left: 7px; top: 7px; width: 36px; height: 36px; fill: none; stroke: #fff;
  stroke-width: 3.2; stroke-linecap: round; stroke-linejoin: round; }
.zero { position: absolute; display: flex; align-items: center; justify-content: center; border-radius: 50%; color: #fff;
  font-size: 54px; font-weight: 900; letter-spacing: -0.03em; }
#dmT { position: absolute; left: 164px; top: 0; height: 150px; line-height: 150px; font-size: 56px; font-weight: 900;
  color: #fff; letter-spacing: 0.01em; white-space: nowrap; }
#dmT::after { content: ""; display: inline-block; width: 4px; height: 52px; margin-left: 4px; vertical-align: -6px; background: #ff8ab0; }
#dmP { position: absolute; left: 164px; top: 0; height: 150px; line-height: 150px; font-size: 40px; font-weight: 500;
  color: rgba(255,255,255,0.45); }
.bub { position: absolute; border-radius: 60px 60px 16px 60px; display: flex; align-items: center; justify-content: center;
  background: linear-gradient(165deg, #e0204b 0%, #ab112e 46%, #6b081c 100%); color: #fff; font-size: 52px; font-weight: 900;
  letter-spacing: 0.01em; box-shadow: inset 0 2px 1px rgba(255,255,255,0.5), 0 30px 60px -20px rgba(70,4,20,0.7); }
.rep { position: absolute; border-radius: 60px 60px 60px 16px; overflow: hidden;
  background: linear-gradient(160deg, #ffffff 0%, #fff5f8 52%, #f5dfe6 100%);
  box-shadow: inset 0 2px 1px #fff, 0 30px 60px -20px rgba(24,4,12,0.65); }
""")

L = []
BEATS = []


def beat(fn):
    BEATS.append(fn)
    return fn


# ===========================================================================
# A · hook — a webinar, for you or for a client; one minute; behind the scenes
@beat
def a_screen():
    scr = ('<div class="dglass edge scr hide" id="scr" style="left:180px;top:140px;width:720px;height:410px">'
           '<div class="live" style="left:34px;top:30px;height:56px;padding:0 22px;border-radius:28px;font-size:24px"><b></b>LIVE</div>'
           '<div class="pres">'
           '<div class="face tw circ" id="prF"><div class="pearl">%s</div></div>'
           '<div class="face tw circ hide" id="prB"><div class="jelly">%s</div></div></div>'
           '<div class="trk"><div class="fil" id="fil"></div></div>'
           '<div class="shc"><div class="sheen"></div></div></div>' % (stroke("person"), stroke("person")))
    ring = ('<svg class="abs" id="tmrS" width="320" height="320" viewBox="0 0 320 320" style="left:660px;top:190px;overflow:visible">'
            '<circle class="ring1" id="rng" cx="160" cy="160" r="146" transform="rotate(-90 160 160)"/></svg>')
    tmr = tile("tmr", 240, 700, 230, "jelly", '<div class="dig" id="dig">1:00</div>', extra_cls="circ")
    sett = tile("set", 116, 60, 452, "pearl", SLIDERS, extra_cls="circ", ring=False)
    L.append('<div class="g full" id="gA">' + scr + ring + tmr + sett + '</div>')
    sfx("pop", T["vebinar"] - 0.02)
    sfx("click", T["odnu"] + 0.02, -2)
    return js("""
  tl.set("#gA", {autoAlpha: 1}, 0);
  arr("#scr", @vebinar-0.1, {s: 0.7, y: 40});
  shn("#scr .sheen", @vebinar+0.4);
  tl.fromTo("#fil", {scaleX: 0.04}, {scaleX: 0.62, duration: @kulisamy-@vebinar, ease: "none"}, @vebinar);
  arr("#prF", @sebe-0.1, {s: 0.4, y: 20, d: 0.6});
  tl.to("#prF", {rotationY: 90, duration: 0.16, ease: "power2.in"}, @kliientky-0.06);
  tl.set("#prF", {autoAlpha: 0}, @kliientky+0.1);
  tl.set("#prB", {autoAlpha: 1}, @kliientky+0.1);
  tl.fromTo("#prB", {rotationY: -90}, {rotationY: 0, duration: 0.7, ease: FLIP, immediateRender: false}, @kliientky+0.1);
  gsap.set("#prB", {rotationY: -90});
  /* one minute: the screen steps aside for the stopwatch */
  tl.to("#scr", {x: -160, scale: 0.84, duration: 0.6, ease: SP}, @zaraz-0.1);
  arr("#tmr", @odnu-0.08, {s: 0.4, y: 20, d: 0.7});
  G.ripple("#tmrR", @odnu+0.25);
  tl.set("#tmrS", {autoAlpha: 1}, @odnu+0.05);
  draw2("rng", @odnu+0.05, 0.4);
  tl.to("#rng", {strokeDashoffset: {{ringL}}, duration: @kulisamy-@khvylynu, ease: "none"}, @khvylynu+0.5);
  arr("#set", @nalasht-0.4, {s: 0.4, y: 20, d: 0.6});
  tl.fromTo("#knA", {x: 0}, {x: 7, duration: 0.5, ease: SP, immediateRender: false}, @nalasht+0.25);
  tl.fromTo("#knB", {x: 0}, {x: -8, duration: 0.5, ease: SP, immediateRender: false}, @nalasht+0.38);
  tl.set("#gA", {autoAlpha: 0}, @kulisamy+0.62);""").replace("{{ringL}}", "%.1f" % (2 * 3.14159 * 146 + 3))


# ===========================================================================
# B · the curtains close; the backstage pass; they open on her webinars
@beat
def b_curtains():
    drL = '<div class="drape hide" id="drL" style="left:-40px"></div>'
    drR = '<div class="drape hide" id="drR" style="left:540px"></div>'
    val = '<div class="val hide" id="val"></div>'
    lan = ('<svg class="lan abs" width="1080" height="320" viewBox="0 0 1080 320" style="left:0;top:-80px;overflow:visible">'
           '<path class="s1" d="M330 -20 L 522 300"/><path class="s1" d="M750 -20 L 558 300"/>'
           '<path class="s2" d="M330 -20 L 522 300"/><path class="s2" d="M750 -20 L 558 300"/></svg>')
    bdg = ('<div class="bdg" style="left:310px;top:226px;width:460px;height:310px">'
           '<div class="top"></div><div class="slot"></div>'
           '<div class="nm">%s</div><div class="rl">ТЕХНІЧНА ПРОДЮСЕРКА</div>'
           '<div class="shc"><div class="sheen"></div></div></div>' % g.wordmark("RUTA", size=128))
    pas = ('<div class="abs hide" id="pas" style="left:0;top:0;width:1080px;height:640px">%s%s'
           '<div class="clip"></div></div>' % (lan, bdg))
    mini = ""
    for i in range(3):
        x = 66 + i * 324
        mini += ('<div class="dglass edge msc hide" id="ms%d" style="left:%dpx;top:212px;width:300px;height:200px">'
                 '<div class="live"><b></b>LIVE</div>'
                 '<div class="tw circ hide" id="mp%d" style="left:100px;top:52px;width:100px;height:100px">'
                 '<div class="pearl">%s</div></div></div>' % (i, x, i, stroke("person")))
    L.append('<div class="g full" id="gB">' + mini + drL + drR + val + pas + '</div>')
    sfx("whoosh-short", T["kulisamy"] - 0.12, -1)
    sfx("pop", T["ruta"] - 0.05)
    sfx("whoosh-short", T["moikh"] - 0.05, -3)
    return js("""
  tl.set("#gB", {autoAlpha: 1}, @kulisamy-0.35);
  tl.fromTo("#val", {autoAlpha: 0, y: -110}, {autoAlpha: 1, y: 0, duration: 0.45, ease: SP}, @kulisamy-0.32);
  tl.set(["#drL", "#drR"], {autoAlpha: 1}, @kulisamy-0.2);
  tl.fromTo("#drL", {scaleX: 0.1, transformOrigin: "0% 50%"}, {scaleX: 1, duration: 0.7, ease: SOFT, immediateRender: false}, @kulisamy-0.2);
  tl.fromTo("#drR", {scaleX: 0.1, transformOrigin: "100% 50%"}, {scaleX: 1, duration: 0.7, ease: SOFT, immediateRender: false}, @kulisamy-0.2);
  gsap.set("#drL", {scaleX: 0.1, transformOrigin: "0% 50%"}); gsap.set("#drR", {scaleX: 0.1, transformOrigin: "100% 50%"});
  /* the pass swings down on its lanyard */
  tl.set("#pas", {autoAlpha: 1}, @ruta-0.3);
  tl.fromTo("#pas", {y: -640, rotation: -9, transformOrigin: "540px -100px"},
            {y: 0, rotation: 0, duration: 1.15, ease: POP, immediateRender: false}, @ruta-0.3);
  gsap.set("#pas", {y: -640, rotation: -9, transformOrigin: "540px -100px"});
  shn("#pas .sheen", @ruta+0.5);
  tl.to("#pas", {rotation: 2.2, duration: 0.6, ease: "sine.inOut"}, @ruta+0.85);
  tl.to("#pas", {rotation: 0, duration: 0.7, ease: "sine.inOut"}, @ruta+1.45);
  tl.to("#pas", {y: -700, duration: 0.42, ease: "power2.in"}, @moikh-0.2);
  tl.set("#pas", {autoAlpha: 0}, @moikh+0.25);
  /* the curtains open on her webinars */
  tl.to("#drL", {scaleX: 0.1, duration: 0.6, ease: "power3.inOut"}, @moikh-0.02);
  tl.to("#drR", {scaleX: 0.1, duration: 0.6, ease: "power3.inOut"}, @moikh-0.02);
  tl.set(["#drL", "#drR"], {autoAlpha: 0}, @moikh+0.6);
  tl.to("#val", {y: -120, autoAlpha: 0, duration: 0.35, ease: "power2.in"}, @moikh+0.45);
  [0, 1, 2].forEach(function (i) { arr("#ms" + i, @moikh+0.08 + i * 0.08, {s: 0.7, y: 30, d: 0.7}); });
  [0, 1, 2].forEach(function (i) { arr("#mp" + i, @bloh-0.06 + i * 0.1, {s: 0.3, y: 20, d: 0.6}); });
  /* they collapse into the money */
  [0, 1, 2].forEach(function (i) {
    tl.to("#ms" + i, {x: (1 - i) * 324, scale: 0.5, autoAlpha: 0, duration: 0.42, ease: "power3.in"}, @zarobl-0.05);
  });
  tl.set("#gB", {autoAlpha: 0}, @zarobl+0.5);""")


# ===========================================================================
# C · «від 13 000 €»


@beat
def c_money():
    card = ('<div class="sheet mny hide" id="mny" style="left:110px;top:168px;width:860px;height:350px">'
            '<div class="t-micro lb">ВІД</div>'
            '<div class="num"><span class="t-big" id="cnt">0</span><span class="t-big eur" id="eur">€</span></div>'
            '<div class="sheen"></div></div>')
    L.append('<div class="g full" id="gC">' + card + '</div>')
    sfx("kaching", T["ievro"] + 0.02)
    return js("""
  tl.set("#gC", {autoAlpha: 1}, @zarobl+0.1);
  arr("#mny", @zarobl+0.18, {s: 0.5, y: 0, d: 0.8});
  G.bump("#eur", @ievro-0.02); G.bump("#mny", @ievro+0.04); shn("#mny .sheen", @ievro+0.02);
  /* clear before her closeup on «Погнали!» */
  bout("#mny", @np0-0.27, 10, 0.24);
  tl.set("#gC", {autoAlpha: 0}, @np0-0.02);""")


# ===========================================================================
# TK1 · «Погнали»: the slide (16:9 -> 1:1), then OBS
SL0 = (40, 140)                          # the 1000x1000 slide surface, top-left on screen
CLIP169 = "inset(219px 0px 219px 0px round 44px)"
CLIP11 = "inset(110px 110px 110px 110px round 56px)"
SL11 = (0.846, 0, -80)                   # wrapper scale, x, y once it is 1:1
OBS0 = (60, 170)                         # the OBS window, 960x1000
CV = (OBS0[0] + 30, OBS0[1] + 96, 900, 506)   # the canvas on screen
SLOBS = (430.0 / 780, (CV[0] + 36 + 215) - 540, (CV[1] + 38 + 215) - 640)
PIP = (CV[0] + CV[2] - 36 - 380, CV[1] + 38, 380, 430)
PIP_SRC = (140, 600, 760)                # x, y, width of the plate rect shown in the PiP
OBS_TILE = (210, 300)                    # where the OBS tile lands above her head (iris closes there)


@beat
def t1_slide_obs():
    sl = ('<div class="abs" id="slA" style="left:%dpx;top:%dpx;width:1000px;height:1000px">'
          '<div class="slW" id="slW"><div class="slS" id="slS" style="clip-path:%s">'
          '<i class="hb" id="slH" style="left:170px;top:170px;width:440px;height:58px;border-radius:16px"></i>'
          '<i class="rr slB" style="left:170px;top:262px;width:300px;height:26px;border-radius:13px"></i>'
          '<i class="rr slB" style="left:170px;top:304px;width:260px;height:26px;border-radius:13px"></i>'
          '<i class="rr slB" style="left:170px;top:346px;width:200px;height:26px;border-radius:13px"></i>'
          '<i class="im" id="slIM" style="left:170px;top:420px;width:660px;height:400px;border-radius:30px"></i>'
          '<div class="sheen" id="slSh"></div></div></div></div>' % (SL0[0], SL0[1], CLIP169))
    c169 = ('<div class="card169 hide" id="c169" style="left:300px;top:948px;width:480px;height:270px">'
            '<i class="hb" style="left:32px;top:42px;width:200px;height:28px;border-radius:8px"></i>'
            '<i class="rr" style="left:32px;top:92px;width:150px;height:14px;border-radius:7px"></i>'
            '<i class="rr" style="left:32px;top:116px;width:120px;height:14px;border-radius:7px"></i>'
            '<i class="im" style="left:250px;top:42px;width:196px;height:150px;border-radius:14px"></i></div>')
    xs = ('<svg class="abs" width="1080" height="1300" style="left:0;top:0;overflow:visible">'
          '<path class="xs" id="x1" style="opacity:0" d="M370 990 L 710 1176"/>'
          '<path class="xs" id="x2" style="opacity:0" d="M710 990 L 370 1176"/></svg>')
    ch169 = '<div class="pill p hide" id="ch169" style="left:690px;top:912px;width:170px;height:76px;font-size:38px">16:9</div>'
    ch11 = '<div class="pill j hide" id="ch11" style="left:455px;top:136px;width:170px;height:76px;font-size:40px">1:1</div>'
    ok11 = tile("ok11", 76, 640, 136, "pearl", stroke("check"), extra_cls="circ", ring=False)
    trd = tile("trd", 128, 806, 166, "jelly", stroke("trend"), extra_cls="circ")
    # OBS
    vx, vy, vw = PIP_SRC
    s = PIP[2] / float(vw)
    pip = ('<div class="pip hide" id="pip" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx">'
           '<div class="vw" style="transform: translate(%.1fpx,%.1fpx) scale(%.5f)">'
           '<video id="pipv" class="vv" src="assets/base.mp4" data-start="%.3f" data-duration="%.3f" '
           'data-media-start="%.3f" muted playsinline></video></div>'
           '<div class="rec"><b></b>CAM</div></div>'
           % (PIP[0] - CV[0], PIP[1] - CV[1], PIP[2], PIP[3], -vx * s, -vy * s, s,
              T["samu"] - 0.3, T["toi"] + 0.6 - (T["samu"] - 0.3), T["samu"] - 0.3))
    rows = ('<div class="pn" style="left:30px;width:400px"></div><div class="pn" style="left:460px;width:470px"></div>'
            '<div class="oph" style="left:52px">СЦЕНИ</div><div class="oph" style="left:482px">ДЖЕРЕЛА</div>'
            '<div class="orow on hide" id="or0" style="left:46px;right:auto;width:368px;top:692px">%s Вебінар</div>'
            '<div class="orow hide" id="or1" style="left:476px;right:auto;width:438px;top:692px">%s Презентація</div>'
            '<div class="orow hide" id="or2" style="left:476px;right:auto;width:438px;top:774px">%s Камера</div>'
            % (stroke("slide"), stroke("slide"), stroke("cam")))
    obs = ('<div class="obs hide" id="obs" style="left:%dpx;top:%dpx;width:960px;height:1000px">'
           '<div class="tw circ hide" id="obsM" style="left:30px;top:14px;width:64px;height:64px"><div class="jelly">%s</div></div>'
           '<div class="tt hide" id="obsT">OBS Studio</div>'
           '<div class="wd" style="left:858px"></div><div class="wd" style="left:888px"></div><div class="wd" style="left:918px"></div>'
           '<div class="cv" id="cv">%s</div>%s</div>'
           % (OBS0[0], OBS0[1], g.mark("obsstudio"), pip, rows))
    cvg = ('<svg class="abs" width="1080" height="1300" style="left:0;top:0;overflow:visible">'
           '<rect class="cvg" id="cvg" style="opacity:0" x="%d" y="%d" width="%d" height="%d" rx="30"/></svg>'
           % (CV[0] - 7, CV[1] - 7, CV[2] + 14, CV[3] + 14))
    eye = tile("eye", 116, CV[0] + CV[2] - 70, CV[1] - 48, "jelly", stroke("eye"), extra_cls="circ")
    L.append('<div class="g full" id="gT1"><div class="tkg"></div><div class="aurs"></div><div class="grain"></div>'
             + c169 + xs + ch169 + obs + cvg + sl + ch11 + ok11 + trd + eye
             + '<div class="sqring" id="obsMR" style="left:%dpx;top:%dpx;width:64px;height:64px;border-radius:50%%"></div>'
             % (OBS0[0] + 30, OBS0[1] + 14) + '</div>')
    sfx("whoosh-short", T["np1"] + 0.02)
    sfx("pop", T["prez1"] - 0.05, -1)
    sfx("click", T["n9"] + 0.05)
    sfx("pop", T["trend"] + 0.02, -3)
    sfx("whoosh-short", T["dali"] - 0.05, -2)
    sfx("pop", T["samu"] + 0.05, -2)
    sfx("pop", T["obs"] + 0.02, -3)
    a, b = SL11[0], SLOBS[0]
    out = js("""
  G.irisOpen("#gT1", @np1+0.01, 540, 640, 0.85);
  drift1("#gT1", @np1, @toi+0.4-@np1);
  /* the slide, 16:9 */
  gsap.set("#slH", {x: -100, y: 110}); gsap.set(".slB", {x: -100, y: 110});
  gsap.set("#slIM", {x: 300, y: -70, scale: 0.74, transformOrigin: "0% 0%"});
  arr("#slA", @prez1-0.15, {s: 0.55, y: 60, d: 0.9});
  tl.fromTo("#slSh", {xPercent: -120}, {xPercent: 120, duration: 0.8, ease: "power2.inOut", immediateRender: false}, @prez1+0.35);
  /* -> 1:1 */
  tl.fromTo("#slS", {clipPath: "{{c169}}"}, {clipPath: "{{c11}}", duration: 0.62, ease: "power3.inOut", immediateRender: false}, @odyn-0.12);
  tl.fromTo("#slW", {scale: 1, x: 0, y: 0}, {scale: {{a}}, x: 0, y: {{ay}}, duration: 0.7, ease: SP, immediateRender: false}, @odyn-0.1);
  tl.fromTo(["#slH", ".slB"], {x: -100, y: 110}, {x: 0, y: 0, duration: 0.7, ease: SP, immediateRender: false}, @odyn-0.05);
  tl.fromTo("#slIM", {x: 300, y: -70, scale: 0.74}, {x: 0, y: 0, scale: 1, duration: 0.75, ease: SP, immediateRender: false}, @odyn-0.02);
  arr("#ch11", @odyn-0.02, {s: 0.4, y: 20, d: 0.6});
  /* the old 16:9 is left behind and crossed out */
  arr("#c169", @ne-0.15, {s: 0.7, y: -120, d: 0.7});
  arr("#ch169", @n16-0.05, {s: 0.4, y: 10, d: 0.55});
  tl.set("#x1", {opacity: 1}, @n9-0.05); draw2("x1", @n9-0.05, 0.2);
  tl.set("#x2", {opacity: 1}, @n9+0.12); draw2("x2", @n9+0.12, 0.2);
  G.haptic("#c169", @n9+0.3);
  tl.to(["#c169", "#ch169", "#x1", "#x2"], {autoAlpha: 0.45, duration: 0.3}, @zvych);
  tl.to(["#c169", "#ch169", "#x1", "#x2"], {y: 90, autoAlpha: 0, duration: 0.4, ease: "power2.in"}, @prez2e-0.1);
  /* trending: this is the format */
  arr("#trd", @trend-0.05, {s: 0.3, y: 20, d: 0.65}); G.ripple("#trdR", @trend+0.25);
  G.bump("#slA", @same); tl.fromTo("#slSh", {xPercent: -120}, {xPercent: 120, duration: 0.8, ease: "power2.inOut", immediateRender: false}, @same);
  arr("#ok11", @takyi-0.02, {s: 0.3, y: 0, d: 0.55});
  /* OBS assembles around it */
  bout(["#ch11", "#ok11", "#trd"], @dali-0.2, 8, 0.25);
  arr("#obs", @dali-0.05, {s: 0.88, y: 50, d: 0.8});
  arr("#or0", @dali+0.3, {s: 0.8, y: 10, d: 0.5});
  tl.fromTo("#slW", {scale: {{a}}, x: 0, y: {{ay}}}, {scale: {{b}}, x: {{bx}}, y: {{by}}, duration: 0.75, ease: SP, immediateRender: false}, @prezent-0.08);
  arr("#or1", @prezent+0.2, {s: 0.8, y: 10, d: 0.5});
  arr("#pip", @samu, {s: 0.5, y: 30, d: 0.7});
  arr("#or2", @liudynu+0.1, {s: 0.8, y: 10, d: 0.5});
  arr("#obsM", @obs-0.04, {s: 0.3, y: 0, d: 0.6}); G.ripple("#obsMR", @obs+0.2);
  bin("#obsT", @obs+0.08, 8, 0.3);
  /* the whole picture is made here */
  tl.set("#cvg", {opacity: 1}, @vsia-0.1); draw2("cvg", @vsia-0.1, 0.65);
  arr("#eye", @bachyt-0.05, {s: 0.3, y: 10, d: 0.6}); G.ripple("#eyeR", @hliadach+0.05);
  G.irisClose("#gT1", @toi-0.3, {{ox}}, {{oy}}, 0.55);""",
             )
    for key, v in {"c169": CLIP169, "c11": CLIP11, "a": "%.4f" % a,
                   "ay": SL11[2], "b": "%.4f" % b, "bx": "%.1f" % SLOBS[1], "by": "%.1f" % SLOBS[2],
                   "ox": OBS_TILE[0], "oy": OBS_TILE[1]}.items():
        out = out.replace("{{%s}}" % key, str(v))
    return out


# ===========================================================================
# D · near: OBS -> YouTube -> link -> Webinar Stars
WS_TILE = (870, 300)


@beat
def d_chain():
    cab = ('<svg class="cab abs" width="1080" height="700" viewBox="0 0 1080 700" style="left:0;top:0">'
           '<path class="tube hide" id="yT1" d="M306 300 C 360 288 392 288 446 300"/>'
           '<path class="core hide" id="yC1" d="M306 300 C 360 288 392 288 446 300"/>'
           '<path class="tube hide" id="yT2" d="M636 300 C 690 312 722 312 776 300"/>'
           '<path class="core hide" id="yC2" d="M636 300 C 690 312 722 312 776 300"/>'
           '<g class="pkg"><path class="pkt" id="yP1" style="opacity:0" d="M306 300 C 360 288 392 288 446 300"/>'
           '<path class="pkt" id="yP2" style="opacity:0" d="M636 300 C 690 312 722 312 776 300"/></g></svg>')
    lnk = ('<div class="lnk hide" id="lnk" style="left:356px;top:442px"><div class="lc">%s</div>'
           'youtube.com<em>/live/…</em></div>' % stroke("link"))
    L.append('<div class="g full" id="gD">'
             '<div class="shelf edge hide" id="shY" style="left:70px;top:150px;width:940px;height:400px"></div>'
             + cab
             + tile("yOB", 190, OBS_TILE[0] - 95, 205, "jelly", g.mark("obsstudio"))
             + tile("yYT", 190, 445, 205, "pearl", g.mark("youtube"))
             + tile("yWS", 190, WS_TILE[0] - 95, 205, "jelly", ws_mark(40))
             + lnk + '</div>')
    sfx("pop", T["youtube"] - 0.02)
    sfx("click-soft", T["posyl"] + 0.02, -2)
    sfx("pop", T["webinar"] + 0.02, -1)
    return js("""
  tl.set("#gD", {autoAlpha: 1}, @toi-0.35);
  arr("#yOB", @toi-0.3, {s: 0.6, y: 0, d: 0.7});
  arr("#shY", @toi+0.2, {s: 0.92, y: 20, d: 0.7});      /* after the iris has closed */
  tl.set(["#yT1", "#yC1"], {autoAlpha: 1}, @pidkl-0.05);
  draw2("yT1", @pidkl-0.05, 0.5); draw2("yC1", @pidkl-0.05, 0.5);
  arr("#yYT", @youtube-0.06, {s: 0.4, y: 20, d: 0.7}); G.ripple("#yYTR", @youtube+0.25);
  G.packet("yP1", @youtube+0.1, 0.45);
  arr("#lnk", @posyl-0.05, {s: 0.5, y: -60, d: 0.65});
  tl.set(["#yT2", "#yC2"], {autoAlpha: 1}, @vede-0.1);
  draw2("yT2", @vede-0.1, 0.45); draw2("yC2", @vede-0.1, 0.45);
  tl.to("#lnk", {x: 300, scale: 0.86, duration: 0.55, ease: SP}, @vede-0.05);
  arr("#yWS", @webinar-0.06, {s: 0.4, y: 20, d: 0.7});
  tl.to("#lnk", {x: 360, y: -150, scale: 0.2, autoAlpha: 0, duration: 0.35, ease: "power3.in"}, @webinar+0.15);
  G.ripple("#yWSR", @webinar+0.45); G.bump("#yWS", @webinar+0.45);
  tl.set("#gD", {autoAlpha: 0}, @starse+0.75);""")


# ===========================================================================
# TK2 · Webinar Stars: the page she sets up, wrapped in a phone, a registration
PG = (220, 140, 640, 1060)
TITLE = u"Мій вебінар"


@beat
def t2_page():
    rows = ""
    for i, (ic, w) in enumerate((("cal", 300), ("clock", 220), ("mic", 340))):
        rows += ('<div class="drow hide" id="dr%d" style="top:%dpx;width:500px"><div class="ic">%s</div>'
                 '<i class="rr" style="width:%dpx"></i></div>' % (i, 580 + i * 78, stroke(ic), w))
    page = ('<div class="pg hide" id="pg" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx">'
            '<div class="brand">Webinar Stars</div><div class="hair2"></div>'
            '<i class="im" style="left:50px;top:176px;width:540px;height:236px;border-radius:34px"></i>'
            '<div class="tw circ" style="left:256px;top:230px;width:128px;height:128px"><div class="pearl">%s</div></div>'
            '<div class="tbox hide" id="tbox"></div><div class="ttl" id="ttl"></div>%s'
            '<div class="rbtn hide" id="rbtn"><div class="lbl" id="rbL">Зареєструватися</div>'
            '<div class="okk hide" id="rbO">%s</div></div>'
            '<i class="rr" style="left:150px;top:970px;width:340px;height:18px"></i>'
            '<div class="ckr" id="ckr" style="left:320px;top:878px"></div>'
            '<div class="fing hide" id="fing" style="left:320px;top:878px"></div>'
            '<div class="shc"><div class="sheen"></div></div></div>'
            % (PG + (stroke("person"), rows, stroke("check"))))
    bez = ('<div class="bez hide" id="bez" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx"><div class="isl"></div></div>'
           % (PG[0] - 30, PG[1] - 30, PG[2] + 60, PG[3] + 60))
    L.append('<div class="g full" id="gT2"><div class="tkg"></div><div class="aurs"></div><div class="grain"></div>'
             + bez + page + '</div>')
    sfx("whoosh-short", T["starse"] - 0.12)
    sfx("typing", T["nazvu"] - 0.1, -2)
    sfx("pop", T["knopky"] - 0.05, -2)
    sfx("click", T["reiestr"] + 0.02)
    return js("""
  G.irisOpen("#gT2", @starse-0.15, {{wx}}, {{wy}}, 0.85);
  drift1("#gT2", @starse, @reiestre+0.4-@starse);
  gsap.set("#pg", {transformOrigin: "650px 160px"});
  arr("#pg", @starse+0.1, {s: 0.3, y: 0, d: 0.95});
  shn("#pg .sheen", @nalashtovuiesh);
  bin("#tbox", @nazvu-0.2, 6, 0.25);
  tl.to("#tbox", {autoAlpha: 0, duration: 0.3}, @vsi+0.2);
  [0, 1, 2].forEach(function (i) { arr("#dr" + i, @vsi-0.04 + i * 0.12, {s: 0.7, x: -40, y: 0, d: 0.6}); });
  arr("#rbtn", @robochi+0.02, {s: 0.5, y: 20, d: 0.7});
  G.bump("#rbtn", @knopky+0.2);
  /* the final wrapper: the page becomes a phone screen */
  arr("#bez", @obhortku-0.1, {s: 1.14, y: 0, d: 0.8, blur: 16});
  shn("#pg .sheen", @obhortku+0.2);
  /* a person registers */
  tl.fromTo("#fing", {autoAlpha: 0, x: 160, y: 200, scale: 1.3}, {autoAlpha: 1, x: 0, y: 0, scale: 1, duration: 0.5, ease: SP, immediateRender: false}, @liudyna-0.1);
  tl.to("#fing", {scale: 0.8, duration: 0.1}, @reiestr); tl.to("#fing", {scale: 1, autoAlpha: 0, duration: 0.4}, @reiestr+0.1);
  tl.to("#rbtn", {scale: 0.95, duration: 0.1, ease: "power2.out"}, @reiestr);
  tl.to("#rbtn", {scale: 1, duration: 0.45, ease: SP}, @reiestr+0.1);
  tl.fromTo("#ckr", {scale: 0.3, autoAlpha: 0.95}, {scale: 2.2, autoAlpha: 0, duration: 0.7, ease: "power2.out", immediateRender: false}, @reiestr+0.02);
  tl.to("#rbL", {autoAlpha: 0, duration: 0.15}, @reiestr+0.05);
  tl.fromTo("#rbO", {autoAlpha: 0, scale: 0.3}, {autoAlpha: 1, scale: 1, duration: 0.5, ease: POP}, @reiestr+0.1);
  G.irisClose("#gT2", @reiestre-0.22, {{lx}}, {{ly}}, 0.55);""").replace(
        "{{wx}}", str(WS_TILE[0])).replace("{{wy}}", str(WS_TILE[1])).replace(
        "{{lx}}", str(LINE[3][0] + 85 + SCAT[3][0])).replace("{{ly}}", str(LINE_Y + 85 + SCAT[3][1]))


# ===========================================================================
# E · near: all the pieces in one line, LIVE
LINE = [(105, 0), (335, 0), (565, 0), (795, 0)]
LINE_Y = 200
SCAT = [(-10, 120, -13), (40, -30, 10), (-40, 130, -7), (-30, -20, 12)]     # dx, dy, rot before the snap


@beat
def e_line():
    cab = '<svg class="cab abs" width="1080" height="700" viewBox="0 0 1080 700" style="left:0;top:0">'
    for i in range(3):
        x0 = LINE[i][0] + 170
        x1 = LINE[i + 1][0]
        cab += ('<path class="tube hide" id="lT%d" d="M%d 285 L %d 285"/><path class="core hide" id="lC%d" d="M%d 285 L %d 285"/>'
                '<g class="pkg"><path class="pkt" id="lP%d" style="opacity:0" d="M%d 285 L %d 285"/></g>'
                % (i, x0 - 6, x1 + 6, i, x0 - 6, x1 + 6, i, x0 - 20, x1 + 20))
    cab += '</svg>'
    tiles = (tile("lSL", 170, LINE[0][0], LINE_Y, "pearl", mini_slide())
             + tile("lOB", 170, LINE[1][0], LINE_Y, "jelly", g.mark("obsstudio"))
             + tile("lYT", 170, LINE[2][0], LINE_Y, "pearl", g.mark("youtube"))
             + tile("lWS", 170, LINE[3][0], LINE_Y, "jelly", ws_mark(35)))
    live = ('<div class="live hide" id="lLV" style="left:400px;top:418px;width:280px;height:96px;border-radius:48px;font-size:40px">'
            '<b id="lDot" style="width:22px;height:22px"></b>LIVE<div class="shc"><div class="sheen"></div></div></div>'
            '<div class="sqring rnd" id="lLVR" style="left:400px;top:418px;width:280px;height:96px;border-radius:48px"></div>')
    L.append('<div class="g full" id="gE">'
             '<div class="shelf edge hide" id="shL" style="left:70px;top:150px;width:940px;height:400px"></div>'
             + cab + tiles + live + '</div>')
    sfx("pop", T["zibrani"] + 0.05)
    sfx("ping", T["zapusk"] + 0.02, -2)
    return js("""
  tl.set("#gE", {autoAlpha: 1}, @reiestre-0.3);
  arr("#shL", @reiestre+0.3, {s: 0.92, y: 20, d: 0.7});  /* after the iris has closed */
  var ids = ["#lSL", "#lOB", "#lYT", "#lWS"], sc = {{scat}};
  ids.forEach(function (id, i) {
    var s = sc[i];
    gsap.set(id, {x: s[0], y: s[1], rotation: s[2]});
    bin(id, (i === 3 ? @reiestre-0.15 : @vsi2-0.3 + i * 0.12), 10, 0.36);
    tl.fromTo(id, {scale: 0.5}, {scale: 0.86, duration: 0.6, ease: POP, immediateRender: false}, (i === 3 ? @reiestre-0.15 : @vsi2-0.3 + i * 0.12));
    tl.fromTo(id, {x: s[0], y: s[1], rotation: s[2], scale: 0.86}, {x: 0, y: 0, rotation: 0, scale: 1, duration: 0.6, ease: SP, immediateRender: false}, @zibrani-0.06 + i * 0.06);
  });
  gsap.set(["#lSL", "#lOB", "#lYT", "#lWS"], {scale: 0.5});
  [0, 1, 2].forEach(function (i) {
    tl.set(["#lT" + i, "#lC" + i], {autoAlpha: 1}, @liniiu-0.25 + i * 0.1);
    draw2("lT" + i, @liniiu-0.25 + i * 0.1, 0.3); draw2("lC" + i, @liniiu-0.25 + i * 0.1, 0.3);
  });
  arr("#lLV", @hotovyi-0.05, {s: 0.4, y: 30, d: 0.7});
  [0, 1, 2].forEach(function (i) { G.packet("lP" + i, @zapusk + i * 0.16, 0.3); });
  tl.fromTo("#lDot", {scale: 1}, {scale: 1.6, duration: 0.25, yoyo: true, repeat: 3, ease: "sine.inOut", immediateRender: false}, @zapusk+0.2);
  G.ripple("#lLVR", @zapusk+0.45); shn("#lLV .sheen", @vebinar2);
  G.bump("#lLV", @vebinar2+0.05);
  bout("#gE", @vebinar2e-0.15, 10, 0.3);""").replace("{{scat}}", json.dumps([list(s) for s in SCAT]))


# ===========================================================================
# F · CTA: the checklist (free), then a DM types ВЕБІНАР and the guide comes back
@beat
def f_cta():
    rows = ""
    for i, w in enumerate((440, 372, 476, 318)):
        y = 140 + i * 72
        rows += ('<div class="cbx" style="left:46px;top:%dpx"><div class="cbf" id="cb%d">'
                 '<svg viewBox="0 0 24 24"><path id="cbp%d" d="M5.4 12.6l4.3 4.3 8.9-9.5"/></svg></div></div>'
                 '<i class="rr" style="left:124px;top:%dpx;width:%dpx;height:24px;border-radius:12px"></i>'
                 % (y, i, i, y + 13, w))
    lst = ('<div class="lst hide" id="ckl" style="left:150px;top:130px;width:780px;height:440px">'
           '<div class="tw" style="left:42px;top:36px;width:66px;height:66px"><div class="jelly">%s</div></div>'
           '<i class="hb" style="left:130px;top:54px;width:300px;height:30px"></i>%s'
           '<div class="shc"><div class="sheen"></div></div></div>' % (stroke("check"), rows))
    zero = ('<div class="tw circ hide" id="zr" style="left:820px;top:78px;width:170px;height:170px">'
            '<div class="jelly"><div class="zero" style="inset:0;position:absolute">0 €</div></div></div>')
    dm = ('<div class="dglass edge hide" id="dm" style="left:60px;top:440px;width:960px;height:150px;border-radius:75px">'
          '<div class="tw circ" style="left:24px;top:24px;width:102px;height:102px"><div class="jelly">%s</div></div>'
          '<div id="dmP">Повідомлення…</div><div id="dmT"></div>'
          '<div class="tw circ" id="dmS" style="left:840px;top:24px;width:102px;height:102px"><div class="pearl">%s</div></div></div>'
          % (g.mark("instagram"), stroke("send")))
    bub = '<div class="bub hide" id="bub" style="left:560px;top:150px;width:400px;height:124px">ВЕБІНАР</div>'
    rep = ('<div class="rep hide" id="rep" style="left:120px;top:296px;width:470px;height:118px">'
           '<div class="tw" style="left:22px;top:22px;width:74px;height:74px"><div class="jelly">%s</div></div>'
           '<i class="hb" style="left:118px;top:34px;width:240px;height:22px;border-radius:8px"></i>'
           '<i class="rr" style="left:118px;top:70px;width:300px;height:16px;border-radius:8px"></i></div>' % stroke("check"))
    L.append('<div class="g full" id="gF">' + lst + zero + dm + bub + rep + '</div>')
    sfx("pop", T["bezk"] + 0.05, -3)
    sfx("click-soft", T["haid"] + 0.15, -3)
    sfx("whoosh-short", T["tomu2"] - 0.1, -3)
    sfx("typing", T["pyshy"] + 0.2, -2)
    sfx("click", T["shchob"] - 0.02)
    sfx("notification", T["yoho"] - 0.1, -3)
    return js("""
  tl.set("#gF", {autoAlpha: 1}, @vebinar2e-0.15);
  arr("#ckl", @mene-0.1, {s: 0.7, y: 40});
  shn("#ckl .sheen", @mene+0.3);
  arr("#zr", @bezk-0.02, {s: 0.3, y: 20, d: 0.7});
  tl.fromTo("#zr", {rotation: -24}, {rotation: -8, duration: 0.8, ease: SP, immediateRender: false}, @bezk-0.02);
  gsap.set("#zr", {rotation: -24});
  [["#cb0", @haid+0.05], ["#cb1", @haid+0.45], ["#cb2", @nalasht2+0.1], ["#cb3", @vebinara+0.05]].forEach(function (p, i) {
    tl.fromTo(p[0], {autoAlpha: 0, scale: 0.4}, {autoAlpha: 1, scale: 1, duration: 0.4, ease: POP}, p[1]);
    draw2("cbp" + i, p[1] + 0.06, 0.3);
  });
  /* DM */
  tl.to(["#ckl", "#zr"], {y: -60, scale: 0.8, autoAlpha: 0, duration: 0.32, ease: "power2.in"}, @tomu2-0.15);
  arr("#dm", @tomu2-0.05, {s: 0.85, y: 40, d: 0.7});
  tl.set("#dmP", {autoAlpha: 0}, @pyshy+0.18);
  G.bump("#dmS", @shchob-0.04);
  tl.fromTo("#bub", {autoAlpha: 0, y: 300, scale: 0.6, transformOrigin: "100% 100%"}, {autoAlpha: 1, y: 0, scale: 1, duration: 0.6, ease: SP}, @shchob);
  arr("#rep", @yoho-0.12, {s: 0.5, x: -40, y: 20, d: 0.6});""")


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


def clock_js():
    """Every text that changes over time (stopwatch, count-up, typed title, the
    DM) is painted from one clock, so any frame renders cold."""
    t_sw = T["khvylynu"] + 0.45
    c0, c1 = T["n13"] - 0.02, T["tysiach"] + 0.25
    y0, y1 = T["nazvu"] - 0.05, T["nazvu"] + 0.55
    d0, d1 = T["pyshy"] + 0.2, T["VEB"] + 0.35
    d_clear = T["shchob"]
    return r"""
  var CLK = {t: 0}, E_DIG = document.getElementById("dig"), E_CNT = document.getElementById("cnt"),
      E_TTL = document.getElementById("ttl"), E_DM = document.getElementById("dmT"),
      TTL = %(ttl)s, DMW = "ВЕБІНАР", P = {};
  function put(el, key, s) { if (P[key] !== s) { P[key] = s; el.textContent = s; } }
  function paintAll() {
    var t = CLK.t;
    var n = t < %(sw).3f ? 0 : Math.min(9, Math.floor(t - %(sw).3f) + 1);
    put(E_DIG, "d", n === 0 ? "1:00" : "0:" + (60 - n < 10 ? "0" : "") + (60 - n));
    var p = t <= %(c0).3f ? 0 : t >= %(c1).3f ? 1 : (t - %(c0).3f) / %(cd).3f;
    var v = Math.round(13000 * (1 - Math.pow(1 - p, 3)) / 100) * 100;
    put(E_CNT, "c", v >= 1000 ? Math.floor(v / 1000) + " " + ("00" + (v %% 1000)).slice(-3) : String(v));
    var k = t <= %(y0).3f ? 0 : t >= %(y1).3f ? TTL.length : Math.round(TTL.length * (t - %(y0).3f) / %(yd).3f);
    put(E_TTL, "t", TTL.slice(0, k));
    var m = t <= %(d0).3f ? 0 : t >= %(d1).3f ? DMW.length : Math.round(DMW.length * (t - %(d0).3f) / %(dd).3f);
    put(E_DM, "m", t >= %(dc).3f ? "" : DMW.slice(0, m));
  }
  paintAll();
  tl.fromTo(CLK, {t: 0}, {t: %(dur).3f, duration: %(dur).3f, ease: "none", onUpdate: paintAll}, 0);""" % {
        "ttl": json.dumps(TITLE, ensure_ascii=False), "sw": t_sw, "c0": c0, "c1": c1, "cd": c1 - c0,
        "y0": y0, "y1": y1, "yd": y1 - y0, "d0": d0, "d1": d1, "dd": d1 - d0, "dc": d_clear, "dur": DUR}


# captions that would repeat the graphic's own words (STYLE.md §2b.1)
def span_words(a, b):
    return (round(a - 0.02, 3), round(b, 3), "")


BLACKOUT = [
    span_words(T["odnu"], T["khvylynue"]),              # the stopwatch says 1:00
    span_words(T["ruta"], T["prode"]),                   # the pass says RUTA, технічна продюсерка
    span_words(T["vid"], T["ievroe"]),                   # the card says від 13 000 €
    span_words(T["odyn"], T["odyn2e"]),                  # the chip says 1:1
    span_words(T["n16"], T["n9e"]),                      # the chip says 16:9
    span_words(T["obs"], T["obse"]),                     # the window title says OBS Studio
    span_words(T["webinar"], T["starse"]),               # the tile says Webinar Stars
    span_words(T["reiestr"], T["reiestre"]),             # the button says Зареєструватися
    span_words(T["VEB"], T["VEBe"]),                     # the DM types ВЕБІНАР
]


def main():
    # nothing but captions inside her closeup: the money card is out before it,
    # the takeover's iris opens after it, and no sound cue lands in it
    assert T["np0"] - 0.27 + 0.24 <= NP0 and T["np1"] + 0.01 >= NP1
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
        title=u"Reel 23 — вебінар за кулісами",
        plate="assets/base.mp4",
        gfx_html=g.defs() + "\n" + "\n".join(L),
        gfx_js="\n".join(head + gj),
        caps=CAPS,
        blackout=BLACKOUT,
        # keep the plaque down through «а не» between the 1:1 and 16:9 chips
        scrim_off=[(T["odyn2e"], T["n16"], "")],
    )
    io.open(os.path.join(HERE, "index.html"), "w", encoding="utf-8").write(doc)
    SFX.sort(key=lambda c: c["t"])
    io.open(os.path.join(HERE, "sfx.json"), "w", encoding="utf-8").write(json.dumps(SFX, indent=1))
    print("index.html  %d captions, %d beats, %d sfx cues (%.2f/s)" % (len(CAPS), len(BEATS), len(SFX), len(SFX) / DUR))


main()
