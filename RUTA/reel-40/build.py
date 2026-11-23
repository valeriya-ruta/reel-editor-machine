# -*- coding: utf-8 -*-
"""Reel 40 — «$20 чи $100: який тариф Claude». Posts 2026-10-18.

Cut from her raw take by tools/cut.py (no closeups this time: no_paint is
empty). Refined glass (STYLE.md §0), sound design (tools/sfx.py).

The one object is **Claude with an energy tank**. Same Claude on every plan;
only the tank differs. She says доларів, so prices are in $.

Chain:  near: the edit timeline, Claude plugs into it, a $20 tag, «?» ->
the $20 tile slides aside and an identical $100 tile comes out from behind it,
«=» -> OVER (iris out of «=»): the two plans side by side on a sheet, every
feature ticked in pairs, «0» stamps -> the sheet clears, a line is drawn: free
($0, grey) | paid, the paid tile lights -> iris closes onto it -> near: it
splits into $20 / $100 / $200, the same tile three times; each gets a tank
and the tanks fill to different levels -> the usage panel: weekly limit, 5-hour
limit -> OVER (iris out of the 5-hour bar): 10 reels on the $100 tank, it
barely moves, more slots keep coming, a lens on the dip -> the $20 tank: one
task, drained, «Ліміт вичерпано» -> iris closes onto the $20 tile -> near: two
steps, start on $20, sparkle, the arrow climbs to $100 -> CTA: the timeline is
back, the DM types «дизайн», the free lesson lands and powers the edit.

usage: python build.py   (then: python ../tools/sfx.py mix 40)
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

CUT = json.load(io.open(os.path.join(ROOT, "work", "r40", "cut.json"), encoding="utf-8"))
DUR = 56.783           # (1704 plate frames - 0.5) / 30
FPS = 30
k = Kit(width=1080, height=1920, fps=FPS, duration=DUR)
g = Glass(["claude", "instagram"])
k.css(g.css())

NO_PAINT = [tuple(x) for x in CUT["no_paint"]]   # empty on this cut

CAPS = k.load_captions(os.path.join(ROOT, "work", "r40", "captions.json"))
# whisper errors in the "she improvised" lines -> what she actually said / the script
FIX = {u"ШІ,": u"зі", u"металетом,": u"інтелектом,", u"0.": u"нуль.", u"твоєму": u"твого"}
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
    "zapustyty": S(u"запустити", 1.03), "montazh": S(u"монтаж", 1.51), "shtuchnym": S(u"штучним", 2.15),
    "pidpyska": S(u"підписка", 3.52), "d20a": S("20", 4.33), "dolariv": S(u"доларів", 4.86),
    "kloda": S(u"Клод", 5.42), "rozumiete": S(u"розумієте", 7.0),
    "pidpyska2": S(u"Підписка", 7.80), "d20b": S("20", 8.40), "d100b": S("100", 9.18),
    "dolariv2e": E(u"доларів", 9.36), "odna": S(u"одна", 10.24), "potuzh": S(u"потужність", 11.27),
    "po": S(u"По", 12.97), "funk": S(u"функціям", 13.19), "vin": S(u"він", 13.61),
    "absol": S(u"абсолютно", 13.87), "odnak": S(u"однаковий", 14.80), "nul": S(u"нуль", 15.90),
    "nule": E(u"нуль", 15.90),
    "yedyna": S(u"Єдина", 16.47), "mezha": S(u"межа", 16.98), "bezk": S(u"безкоштовний", 17.48),
    "platnyi": S(u"платний", 18.38), "klod3": S(u"Клод", 18.78), "dali": S(u"далі", 19.26),
    "d20c": S("20", 19.46), "d100c": S("100", 20.00), "d200": S("200", 20.36),
    "dolariv3e": E(u"доларів", 20.70), "toi": S(u"той", 21.48), "prosto": S(u"просто", 22.72),
    "riznym": S(u"різним", 23.38), "enerhii": S(u"енергії", 24.32),
    "tobto": S(u"Тобто", 25.13), "limit1": S(u"ліміт", 25.93), "tyzhden": S(u"тиждень", 26.59),
    "limit2": S(u"ліміт", 27.17), "d5": S("5", 27.65), "hodyne": E(u"годин", 27.87),
    "yakshcho": S(u"Якщо", 28.42), "zmontuiu": S(u"змонтую", 29.26), "d10": S("10", 29.60),
    "klod5": S(u"Клод", 30.40), "pidpystsi": S(u"підписці", 31.14), "d100d": S("100", 31.68),
    "dolariv4": S(u"доларів", 31.96), "dolariv4e": E(u"доларів", 31.96),
    "mene": S(u"мене", 32.73), "kupa": S(u"купа", 33.42), "pratsiuv": S(u"працювати", 34.19),
    "riznytsiu": S(u"різницю", 35.69), "pomichu": S(u"помічу", 36.55),
    "a": S(u"А", 37.07), "d20e": S("20", 37.54), "dolarakhe": E(u"доларах", 38.06),
    "enerhii3": S(u"енергії", 38.66), "odnu": S(u"одну", 40.44), "zadachu": S(u"задачу", 40.62),
    "pislia": S(u"Після", 41.06), "vse": S(u"все", 41.86),
    "tomu": S(u"Тому", 42.87), "pochynaty": S(u"починати", 43.11), "spokiino": S(u"спокійно", 44.11),
    "z20": S("20", 44.69), "dolariv5e": E(u"доларів", 45.11), "kruto": S(u"круто", 46.87),
    "pidnim": S(u"піднімешся", 48.10), "d100f": S("100", 48.86), "d100fe": E("100", 48.86),
    "a2": S(u"А", 49.23), "montazh2": S(u"монтаж", 50.38), "pyshy": S(u"пиши", 50.92),
    "dyzain": S(u"дизайн", 51.66), "dyzaine": E(u"дизайн", 51.66), "i_send": S(u"і", 52.04),
    "dostup": S(u"доступ", 52.58), "bezkoshtovnoho": S(u"безкоштовного", 53.26),
    "urokue": E(u"уроку", 54.06), "osnovu": S(u"основу", 55.00), "montazhu": S(u"монтажу", 56.24),
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
    "up": '<path d="M12 19.2V5.4M6.2 11l5.8-5.8 5.8 5.8"/>',
    "check": '<path d="M5.4 12.6l4.3 4.3 8.9-9.5"/>',
    "cal": '<rect x="3.5" y="5" width="17" height="15.5" rx="3"/><path d="M3.5 10h17M8 3v4M16 3v4"/>',
    "clock": '<circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/>',
}
BOLT = ('<svg class="bolt" viewBox="0 0 24 24"><path d="M13.2 2 4.6 13.4h6.2L9.9 22l8.6-11.6h-6.2z" '
        'fill="#fff"/></svg>')
PLAY = '<svg viewBox="0 0 24 24"><path d="M8 5.5v13l11-6.5z"/></svg>'
STAR = ('<svg viewBox="0 0 24 24"><path d="M12 1.5c.7 5.4 2.8 7.6 8.5 8.5-5.7.9-7.8 3.1-8.5 8.5'
        '-.7-5.4-2.8-7.6-8.5-8.5 5.7-.9 7.8-3.1 8.5-8.5z"/></svg>')


def stroke(name, cls="sk"):
    return '<svg class="%s" viewBox="0 0 24 24">%s</svg>' % (cls, STROKES[name])


def tile(tid, size, x, y, material, inner, extra_cls="", hide=True, ring=True, extra=""):
    r = ('<div class="sqring" id="%sR" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx"></div>'
         % (tid, x, y, size, size)) if ring else ""
    return ('%s<div class="tw%s %s" id="%s" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx">'
            '<div class="%s">%s<div class="sheen"></div></div>%s</div>'
            % (r, " hide" if hide else "", extra_cls, tid, x, y, size, size, material, inner, extra))


def chip(cid, text, x, y, cls=""):
    return '<div class="pz hide %s" id="%s" style="left:%dpx;top:%dpx">%s</div>' % (cls, cid, x, y, text)


def strip(sid, x, y):
    """The edit timeline: a video track of clips, an audio track, a playhead."""
    clips, cx = "", 36
    for i, w in enumerate((160, 110, 210, 130, 180)):
        clips += ('<div class="clp" style="left:%dpx;width:%dpx"><b class="hotf" id="%sh%d"></b></div>'
                  % (cx, w, sid, i))
        cx += w + 10
    aud = "".join('<div class="aud" style="left:%dpx;width:%dpx"></div>' % (ax, w)
                  for ax, w in ((36, 300), (346, 240), (596, 270)))
    return ('<div class="shelf edge hide" id="%s" style="left:%dpx;top:%dpx;width:940px;height:180px;border-radius:48px">'
            '%s%s<div class="plh" id="%sP" style="left:36px"></div></div>' % (sid, x, y, clips, aud, sid))


def tank(tid, x, y, w, h, level_cls=""):
    marks = "".join('<i class="gm" style="top:%d%%"></i>' % p for p in (25, 50, 75))
    return ('<div class="tank hide %s" id="%s" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx">'
            '<div class="liq" id="%sL"></div>%s%s</div>' % (level_cls, tid, x, y, w, h, tid, marks, BOLT))


k.css("""
.abs { position: absolute; }
.hide { opacity: 0; visibility: hidden; }
.tw { position: absolute; }
.sk { fill: none; stroke: url(#gw); stroke-width: 2.3; stroke-linecap: round; stroke-linejoin: round;
  width: 50%; height: 50%; position: relative; z-index: 1; overflow: visible; }
.pearl .sk { stroke: #17141c; }
.clear { overflow: hidden; }
.circ .jelly, .circ .pearl, .circ .clear, .circ .sheen { border-radius: 50%; }
.ghost .mk { fill: rgba(255,255,255,0.75); }
.dimt .pearl { filter: saturate(0); }
.dimt .pearl .mk { fill: rgba(23,20,28,0.42); }
.aurs { position: absolute; left: -700px; top: -700px; width: 2480px; height: 3320px; pointer-events: none;
  background:
    radial-gradient(circle 526px at 1560px 880px, rgba(255,110,156,0.50), rgba(255,110,156,0)),
    radial-gradient(circle 634px at 760px 2360px, rgba(222,32,74,0.55), rgba(222,32,74,0)),
    radial-gradient(circle 382px at 1480px 1910px, rgba(255,198,214,0.20), rgba(255,198,214,0)); }

/* price tag */
.pz { position: absolute; height: 66px; padding: 0 24px; border-radius: 33px; display: flex; align-items: center;
  background: linear-gradient(160deg, #ffffff 0%, #fff3f7 100%); color: #8d0d24; font-size: 42px; font-weight: 900;
  letter-spacing: -0.02em; white-space: nowrap; z-index: 4;
  box-shadow: inset 0 2px 1px #fff, 0 18px 34px -14px rgba(30,4,12,0.6); }
.pz.dim { color: rgba(23,20,28,0.45); }
.big-g { font-weight: 900; color: #fff; line-height: 1; position: relative; z-index: 1; letter-spacing: -0.04em; }

/* the edit timeline */
.clp { position: absolute; top: 30px; height: 78px; border-radius: 16px; overflow: hidden;
  background: linear-gradient(160deg, rgba(255,255,255,0.92) 0%, rgba(255,226,236,0.78) 100%);
  box-shadow: inset 0 2px 1px #fff, 0 10px 20px -10px rgba(24,4,12,0.5); }
.hotf { position: absolute; inset: 0; display: block; opacity: 0; visibility: hidden;
  background: linear-gradient(165deg, #ff6e9c 0%, #e0204b 50%, #8d0d24 100%); }
.aud { position: absolute; top: 122px; height: 30px; border-radius: 10px; background: rgba(255,255,255,0.42); }
.plh { position: absolute; top: 16px; width: 8px; height: 148px; border-radius: 4px; background: #ff8ab0; z-index: 2;
  box-shadow: 0 0 14px rgba(255,110,156,0.9); }
.plh::before { content: ""; position: absolute; left: -9px; top: -12px; width: 26px; height: 26px; border-radius: 50%;
  background: #ff8ab0; }

/* the comparison sheet */
.prc { position: absolute; text-align: center; font-size: 132px; font-weight: 900; letter-spacing: -0.045em; line-height: 1;
  background: linear-gradient(118deg, #7e0b20 0%, #b4122f 42%, #ff6e9c 100%);
  -webkit-background-clip: text; background-clip: text; color: transparent; padding-right: 8px; }
.vr { position: absolute; width: 3px; background: rgba(23,20,28,0.08); }
.cbx { position: absolute; width: 56px; height: 56px; border-radius: 16px; box-shadow: inset 0 0 0 4px rgba(23,20,28,0.2); }
.cbf { position: absolute; inset: 0; border-radius: 16px; opacity: 0; visibility: hidden;
  background: linear-gradient(165deg, #e0204b 0%, #8d0d24 100%); }
.cbf svg { position: absolute; left: 8px; top: 8px; width: 40px; height: 40px; fill: none; stroke: #fff;
  stroke-width: 3.2; stroke-linecap: round; stroke-linejoin: round; }
.rr { position: absolute; display: block; border-radius: 11px; background: rgba(23,20,28,0.13); }
.hb { position: absolute; display: block; border-radius: 12px; background: linear-gradient(115deg, #c41434 0%, #8d0d24 100%); }
.mz { position: absolute; width: 16px; border-radius: 8px; transform-origin: 50% 0%;
  background: linear-gradient(180deg, #ffffff 0%, #ffd6e3 100%); box-shadow: 0 0 34px rgba(255,110,156,0.85); }

/* the energy tank */
.tank { position: absolute; border-radius: 44px; overflow: hidden;
  background: linear-gradient(160deg, rgba(255,255,255,0.30) 0%, rgba(255,255,255,0.10) 100%);
  box-shadow: inset 0 2px 1px rgba(255,255,255,0.8), inset 0 0 0 3px rgba(255,255,255,0.42),
              inset 0 -20px 30px -16px rgba(255,255,255,0.3), 0 30px 60px -24px rgba(24,4,12,0.6); }
.liq { position: absolute; left: 0; right: 0; bottom: 0; height: 100%; transform-origin: 50% 100%;
  background: linear-gradient(180deg, #ffb3c9 0%, #ff6e9c 10%, #e0204b 55%, #8d0d24 100%);
  box-shadow: inset 0 4px 0 rgba(255,255,255,0.55); }
.tank .gm { position: absolute; left: 0; width: 26%; height: 4px; border-radius: 2px; background: rgba(255,255,255,0.6); z-index: 2; }
.tank .bolt { position: absolute; left: 50%; top: 20px; width: 54px; height: 54px; margin-left: -27px; z-index: 3;
  filter: drop-shadow(0 2px 6px rgba(24,4,12,0.45)); }
.tank.lg { border-radius: 60px; }
.tank.lg .bolt { width: 84px; height: 84px; margin-left: -42px; top: 30px; }
.was { position: absolute; left: 0; right: 0; height: 0; border-top: 6px dashed #fff; z-index: 2; }

/* the usage panel */
.ul { position: absolute; left: 116px; font-size: 38px; font-weight: 700; color: #fff; letter-spacing: -0.01em; white-space: nowrap; }
.ui { position: absolute; left: 42px; width: 54px; height: 54px; fill: none; stroke: #fff; stroke-width: 2.2;
  stroke-linecap: round; stroke-linejoin: round; }
.ut { position: absolute; left: 42px; width: 856px; height: 30px; border-radius: 15px; overflow: hidden;
  background: rgba(255,255,255,0.16); box-shadow: inset 0 1.5px 1px rgba(255,255,255,0.25); }
.uf { position: absolute; inset: 0; border-radius: 15px; transform-origin: 0 50%;
  background: linear-gradient(90deg, #ff8ab0 0%, #e0204b 100%); }
.uh { position: absolute; left: 116px; top: 38px; font-size: 32px; font-weight: 700; color: rgba(255,255,255,0.72); }

/* reels on the tank */
.rc { position: absolute; width: 112px; height: 200px; border-radius: 22px; overflow: hidden;
  background: linear-gradient(165deg, #ffffff 0%, #ffe3ec 100%);
  box-shadow: inset 0 2px 1px #fff, 0 20px 40px -18px rgba(8,0,3,0.7); }
.rc i { position: absolute; left: 16px; right: 22px; bottom: 20px; height: 10px; border-radius: 5px; background: rgba(23,20,28,0.15); }
.rc svg { position: absolute; left: 32px; top: 70px; width: 48px; height: 48px; fill: #b4122f; }
.gs { position: absolute; width: 112px; height: 200px; border-radius: 22px; border: 4px dashed rgba(255,255,255,0.4); }
.rk { position: absolute; width: 48px; height: 48px; border-radius: 50%;
  background: linear-gradient(165deg, #e0204b 0%, #8d0d24 100%);
  box-shadow: inset 0 2px 1px rgba(255,255,255,0.5), 0 0 0 4px #fff, 0 8px 16px rgba(24,4,12,0.4); }
.rk svg { position: absolute; left: 8px; top: 8px; width: 32px; height: 32px; fill: none; stroke: #fff; stroke-width: 3.4;
  stroke-linecap: round; stroke-linejoin: round; }
.lens { position: absolute; overflow: visible; filter: drop-shadow(0 10px 20px rgba(8,0,3,0.5)); }

/* one task, the limit banner */
.tc, .lb, .ls { position: absolute; overflow: hidden; color: #17141c;
  background: linear-gradient(172deg, #ffffff 0%, #fff9fb 55%, #fdf0f4 100%);
  box-shadow: inset 0 2px 1px #fff, 0 40px 80px -30px rgba(8,0,3,0.75); }
.tc { border-radius: 40px; }
.lb { border-radius: 48px; }
.lb .ti, .ls .ti { position: absolute; font-size: 48px; font-weight: 700; letter-spacing: -0.02em; white-space: nowrap; }
.lb .ic { position: absolute; left: 34px; top: 36px; width: 100px; height: 100px; border-radius: 50%;
  background: linear-gradient(165deg, #e0204b 0%, #8d0d24 100%);
  box-shadow: inset 0 2px 1px rgba(255,255,255,0.5), 0 14px 28px -10px rgba(70,4,20,0.6); }
.lb .ic svg { position: absolute; left: 22px; top: 22px; width: 56px; height: 56px; fill: none; stroke: #fff; stroke-width: 2.4;
  stroke-linecap: round; stroke-linejoin: round; }

/* steps */
.star { position: absolute; width: 64px; height: 64px; fill: #fff; filter: drop-shadow(0 0 10px rgba(255,110,156,0.95)); }
.arw { fill: none; stroke: #fff; stroke-width: 14; stroke-linecap: round; stroke-linejoin: round;
  filter: drop-shadow(0 0 12px rgba(255,110,156,0.8)); }

/* the DM bar */
#dm .ph0 { position: absolute; left: 150px; top: 0; height: 124px; line-height: 124px; font-size: 40px; font-weight: 500;
  color: rgba(255,255,255,0.55); }
#dmT { position: absolute; left: 150px; top: 0; height: 124px; line-height: 124px; font-size: 48px; font-weight: 700; color: #fff;
  letter-spacing: -0.01em; }
#dmT::after { content: ""; display: inline-block; width: 3px; height: 46px; margin-left: 4px; vertical-align: -8px; background: #ff8ab0; }

/* the lesson */
.ls { border-radius: 52px; }
.ls .pl { position: absolute; left: 40px; top: 60px; width: 160px; height: 160px; border-radius: 50%;
  background: linear-gradient(165deg, #e0204b 0%, #ab112e 46%, #6b081c 100%);
  box-shadow: inset 0 2px 1px rgba(255,255,255,0.55), 0 20px 40px -16px rgba(70,4,20,0.7); }
.ls .pl svg { position: absolute; left: 44px; top: 40px; width: 80px; height: 80px; fill: #fff; }
.shc { position: absolute; inset: 0; border-radius: inherit; overflow: hidden; pointer-events: none; }
.shc .sheen { mix-blend-mode: normal; opacity: 0.4; }
""")

L = []
BEATS = []


def beat(fn):
    BEATS.append(fn)
    return fn


def cable(cid, d, w=1080, h=700):
    return ('<svg class="cab abs" width="%d" height="%d" viewBox="0 0 %d %d" style="left:0;top:0">'
            '<path class="tube hide" id="%sT" d="%s"/><path class="core hide" id="%sC" d="%s"/>'
            '<g class="pkg"><path class="pkt" id="%sP" style="opacity:0" d="%s"/></g></svg>'
            % (w, h, w, h, cid, d, cid, d, cid, d))


# ===========================================================================
# A + B · the edit, Claude on $20, «?» -> the same Claude on $100, «=»
@beat
def a_hook():
    L.append(
        '<div class="g full" id="gA">'
        + strip("stA", 70, 410)
        + cable("aK", "M540 326 L540 404")
        + tile("bCl", 170, 455, 150, "jelly", g.mark("claude"), extra=chip("bPz", "$100", 104, -30))
        + tile("aCl", 170, 455, 150, "jelly", g.mark("claude"), extra=chip("aPz", "$20", 112, -30))
        + tile("aQ", 110, 290, 180, "jelly", '<span class="big-g" style="font-size:76px">?</span>', extra_cls="circ")
        + tile("bEq", 110, 485, 180, "pearl",
               '<span class="big-g" style="font-size:84px;color:#b4122f">=</span>', extra_cls="circ")
        + '</div>')
    sfx("whoosh-short", "@zapustyty+0.05", -2)
    sfx("pop", "@shtuchnym+0.02")
    sfx("kaching", "@dolariv", -3)
    sfx("whoosh-short", "@pidpyska2", -3)
    sfx("pop", "@d100b+0.02")
    return js("""
  tl.set("#gA", {autoAlpha: 1}, 0.8);
  arr("#stA", @zapustyty-0.05, {s: 0.8, y: 40});
  tl.fromTo("#stAP", {x: 0}, {x: 560, duration: 2.6, ease: "power1.inOut"}, @montazh);
  arr("#aCl", @shtuchnym-0.05, {s: 0.4, y: -40});
  G.ripple("#aClR", @shtuchnym+0.3);
  tl.set(["#aKT", "#aKC"], {autoAlpha: 1}, @shtuchnym+0.35);
  draw2("aKT", @shtuchnym+0.35, 0.35); draw2("aKC", @shtuchnym+0.35, 0.35);
  G.packet("aKP", @shtuchnym+0.75, 0.4);
  arr("#aPz", @d20a-0.04, {s: 0.3, x: -20, y: 20, d: 0.6});
  arr("#aQ", @kloda-0.03, {s: 0.3, x: 40, y: 20, d: 0.7});
  tl.to("#aQ", {keyframes: {rotation: [0, -14, 11, -6, 0]}, duration: 0.6, ease: "none"}, @rozumiete);
  bout(["#stA", "#aKT", "#aKC", "#aQ"], @pidpyska2-0.15, 10, 0.3);
  /* the $20 tile steps aside, an identical one comes out from behind it */
  tl.to("#aCl", {x: -240, scale: 1.12, duration: 0.7, ease: SP}, @pidpyska2+0.02);
  tl.set("#bCl", {autoAlpha: 1}, @d100b-0.25);
  tl.fromTo("#bCl", {x: 0, scale: 0.9}, {x: 240, scale: 1.12, duration: 0.75, ease: SP}, @d100b-0.25);
  arr("#bPz", @d100b-0.02, {s: 0.3, x: -20, y: 20, d: 0.6});
  arr("#bEq", @odna-0.05, {s: 0.3, y: 0, d: 0.7});
  /* same power: both light at once */
  G.bump("#aCl", @potuzh); G.bump("#bCl", @potuzh);
  tl.fromTo(["#aClR", "#bClR"], {scale: 1, autoAlpha: 0.7}, {scale: 1.75, autoAlpha: 0, duration: 0.8, ease: "power2.out", immediateRender: false}, @potuzh);
  gsap.set("#bClR", {x: 240}); gsap.set("#aClR", {x: 0});
  tl.set("#aClR", {x: -240}, @pidpyska2+0.1);
  shn("#aCl .sheen", @potuzh+0.05); shn("#bCl .sheen", @potuzh+0.05);
  G.bump("#bEq", @potuzh+0.35);
  tl.set("#gA", {autoAlpha: 0}, @po+0.6);""")


# ===========================================================================
# TK1 · iris out of «=»: the two plans side by side; then free | paid
COLX = (270, 810)          # column centres, frame x (= the free | paid tiles after)
SHX, SHY = -60, 170        # sheet origin


@beat
def t1_sheet():
    cols = ""
    for ci, (cx, price) in enumerate(zip(COLX, ("$20", "$100"))):
        sx = cx - SHX
        cols += tile("t1C%d" % ci, 150, sx - 75, 60, "jelly", g.mark("claude"), ring=False)
        cols += '<div class="prc" id="t1P%d" style="left:%dpx;top:236px;width:420px">%s</div>' % (ci, sx - 210, price)
        for ri, w in enumerate((200, 150, 220, 130)):
            y = 440 + ri * 118
            cols += ('<div class="cbx" style="left:%dpx;top:%dpx"><div class="cbf" id="cb%d%d">'
                     '<svg viewBox="0 0 24 24"><path id="cbp%d%d" d="M5.4 12.6l4.3 4.3 8.9-9.5"/></svg></div></div>'
                     '<i class="rr" style="left:%dpx;top:%dpx;width:%dpx;height:24px"></i>'
                     % (sx - 160, y, ci, ri, ci, ri, sx - 76, y + 16, w))
    sheet = ('<div class="sheet hide" id="sh1" style="left:%dpx;top:%dpx;width:1200px;height:1050px" data-layout-allow-overflow>'
             '<div class="vr" style="left:598px;top:60px;height:930px"></div>%s'
             '<div class="shc"><div class="sheen"></div></div></div>' % (SHX, SHY, cols))
    zero = tile("t1Z", 220, 430, 700, "jelly", '<span class="big-g" style="font-size:168px">0</span>', extra_cls="circ")
    paid = ('<div class="sqring" id="t1PdR" style="left:690px;top:380px;width:240px;height:240px"></div>'
            '<div class="tw hide ghost" id="t1Pd" style="left:690px;top:380px;width:240px;height:240px">'
            '<div class="clear">%s</div><div class="jelly" id="t1Pj" style="opacity:0;visibility:hidden">%s'
            '<div class="sheen"></div></div></div>' % (g.mark("claude"), g.mark("claude")))
    L.append('<div class="g full" id="gT1"><div class="tkg"></div><div class="aurs"></div><div class="grain"></div>'
             + sheet + zero
             + '<div class="mz" id="t1M" style="left:532px;top:250px;height:940px"></div>'
             + tile("t1F", 240, 150, 380, "pearl", g.mark("claude"), extra_cls="dimt",
                    extra=chip("t1Fz", "$0", 70, 262, "dim"))
             + paid + '</div>')
    sfx("whoosh-short", "@po-0.1")
    sfx("click-soft", "@funk+0.1")
    sfx("pop", "@nul")
    sfx("whoosh-short", "@mezha-0.05", -3)
    sfx("pop", "@platnyi+0.02", -2)
    ticks = [T["funk"] + 0.05, T["vin"] + 0.05, T["absol"] + 0.3, T["odnak"] + 0.05]
    tj = "".join(
        '  tl.fromTo(["#cb0%d", "#cb1%d"], {autoAlpha: 0, scale: 0.4}, {autoAlpha: 1, scale: 1, duration: 0.4, ease: POP}, %.3f);'
        ' draw2("cbp0%d", %.3f, 0.3); draw2("cbp1%d", %.3f, 0.3);\n'
        % (i, i, t, i, t + 0.06, i, t + 0.06) for i, t in enumerate(ticks))
    return js("""
  G.irisOpen("#gT1", @po-0.12, 540, 235, 0.6);
  drift1("#gT1", @po-0.12, @dali-@po);
  arr("#sh1", @po-0.02, {s: 0.86, y: 50, d: 0.8});
  G.inner(["#t1C0", "#t1C1"], @po+0.1);
  tl.fromTo(["#t1P0", "#t1P1"], {autoAlpha: 0, y: 30}, {autoAlpha: 1, y: 0, duration: 0.5, ease: SP}, @po+0.25);
  shn("#sh1 .sheen", @po+0.4);
""") + tj + js("""
  arr("#t1Z", @nul-0.05, {s: 0.3, y: 0, d: 0.7});
  G.ripple("#t1ZR", @nul+0.25);
  bout(["#sh1", "#t1Z"], @yedyna-0.05, 12, 0.32);
  tl.fromTo("#t1M", {scaleY: 0}, {scaleY: 1, duration: 0.55, ease: "power3.inOut"}, @mezha-0.05);
  arr("#t1F", @bezk-0.05, {s: 0.5, x: 60, y: 20});
  arr("#t1Fz", @bezk+0.2, {s: 0.3, y: 20, d: 0.6});
  arr("#t1Pd", @bezk+0.1, {s: 0.5, x: -60, y: 20});
  tl.to("#t1Pj", {autoAlpha: 1, duration: 0.25, ease: "power2.out"}, @platnyi-0.02);
  G.bump("#t1Pd", @platnyi); G.ripple("#t1PdR", @platnyi+0.05);
  shn("#t1Pj .sheen", @platnyi+0.1);
  G.irisClose("#gT1", @klod3+0.15, 810, 500, 0.45);""")


# ===========================================================================
# C · the same Claude three times, three tanks
CC = (220, 540, 860)


@beat
def c_tanks():
    tiles = ""
    for i, (cx, price, cid) in enumerate(zip(CC, ("$20", "$100", "$200"), ("cL", "cM", "cR"))):
        tiles_i = tile(cid, 150, cx - 75, 140, "jelly", g.mark("claude"),
                       extra=chip(cid + "z", price, 96 if i != 1 else 90, -28))
        tiles = tiles + tiles_i if i == 1 else tiles_i + tiles     # the centre tile is on top
    tanks = "".join(tank("cT%d" % i, cx - 60, 316, 120, 240) for i, cx in enumerate(CC))
    L.append('<div class="g full" id="gC">'
             '<div class="shelf edge hide" id="shC" style="left:60px;top:110px;width:960px;height:476px"></div>'
             + tanks + tiles + '</div>')
    sfx("pop", "@d20c+0.02", -2)
    sfx("sparkle", "@riznym+0.05", -2)
    return js("""
  tl.set("#gC", {autoAlpha: 1}, @klod3+0.2);
  arr("#shC", @klod3+0.3, {s: 0.92, y: 30});
  arr("#cM", @dali-0.14, {s: 0.45, x: 270, y: 285, d: 0.8});
  tl.fromTo("#cL", {autoAlpha: 0, x: 320, scale: 0.8}, {autoAlpha: 1, x: 0, scale: 1, duration: 0.7, ease: SP}, @d20c-0.12);
  tl.fromTo("#cR", {autoAlpha: 0, x: -320, scale: 0.8}, {autoAlpha: 1, x: 0, scale: 1, duration: 0.7, ease: SP}, @d200-0.16);
  arr("#cLz", @d20c-0.02, {s: 0.3, y: 20, d: 0.55});
  arr("#cMz", @d100c-0.02, {s: 0.3, y: 20, d: 0.55});
  arr("#cRz", @d200-0.02, {s: 0.3, y: 20, d: 0.55});
  ["#cL", "#cM", "#cR"].forEach(function (s) { G.bump(s, @toi); G.ripple(s + "R", @toi+0.05); shn(s + " .sheen", @toi+0.1); });
  [0, 1, 2].forEach(function (i) { arr("#cT" + i, @prosto-0.05 + i * 0.07, {s: 0.7, y: 30, d: 0.7}); });
  tl.fromTo("#cT0L", {scaleY: 0}, {scaleY: 0.22, duration: 0.9, ease: "power2.out"}, @riznym);
  tl.fromTo("#cT1L", {scaleY: 0}, {scaleY: 0.6, duration: 1.0, ease: "power2.out"}, @riznym+0.18);
  tl.fromTo("#cT2L", {scaleY: 0}, {scaleY: 1, duration: 1.1, ease: "power2.out"}, @riznym+0.36);
  bout("#gC", @tobto-0.14, 10, 0.3);""")


# ===========================================================================
# D · the usage panel: weekly limit, 5-hour limit
UP = (70, 150, 940, 400)
FILL2 = 0.7


@beat
def d_limits():
    x, y, w, h = UP
    panel = ('<div class="dglass edge hide" id="up" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx;border-radius:56px">'
             '<div class="tw" style="left:36px;top:28px;width:62px;height:62px"><div class="jelly">%s</div></div>'
             '<div class="uh">Claude</div>'
             '<svg class="ui hide" id="uI1" viewBox="0 0 24 24" style="top:128px">%s</svg>'
             '<div class="ul hide" id="uL1" style="top:130px">Ліміт на тиждень</div>'
             '<div class="ut hide" id="uT1" style="top:200px"><div class="uf" id="uF1"></div></div>'
             '<svg class="ui hide" id="uI2" viewBox="0 0 24 24" style="top:258px">%s</svg>'
             '<div class="ul hide" id="uL2" style="top:260px">Ліміт на 5 годин</div>'
             '<div class="ut hide" id="uT2" style="top:330px"><div class="uf" id="uF2"></div></div>'
             '<div class="shc"><div class="sheen"></div></div></div>'
             % (x, y, w, h, g.mark("claude"), STROKES["cal"], STROKES["clock"]))
    L.append('<div class="g full" id="gD">' + panel + '</div>')
    sfx("click-soft", "@tyzhden+0.05")
    return js("""
  tl.set("#gD", {autoAlpha: 1}, @tobto-0.15);
  arr("#up", @tobto-0.1, {s: 0.8, y: 40});
  shn("#up .sheen", @tobto+0.3);
  bin(["#uI1", "#uL1", "#uT1"], @limit1-0.05, 8, 0.3);
  tl.fromTo("#uF1", {scaleX: 0}, {scaleX: 0.34, duration: 0.7, ease: SP}, @tyzhden);
  bin(["#uI2", "#uL2", "#uT2"], @limit2-0.05, 8, 0.3);
  tl.fromTo("#uF2", {scaleX: 0}, {scaleX: %.2f, duration: 0.7, ease: SP}, @d5);
  tl.set("#gD", {autoAlpha: 0}, @yakshcho+0.6);""" % FILL2)


# ===========================================================================
# TK2 · 10 reels on the $100 tank; one task on the $20 tank
TKX, TKY, TKW, TKH = 90, 440, 200, 700
LV100, LV100b, LV20 = 0.6, 0.54, 0.2
RX0, RY0, RW, RH, RG = 380, 200, 112, 200, 18


@beat
def t2_reels():
    cards, checks, ghosts = "", "", ""
    for n in range(10):
        r, c = divmod(n, 5)
        x, y = RX0 + c * (RW + RG), RY0 + r * (RH + RG)
        cards += '<div class="rc hide" id="rc%d" style="left:%dpx;top:%dpx">%s<i></i></div>' % (n, x, y, PLAY)
        checks += ('<div class="rk hide" id="rk%d" style="left:%dpx;top:%dpx"><svg viewBox="0 0 24 24">%s</svg></div>'
                   % (n, x + 76, y - 14, STROKES["check"]))
    for n in range(10):
        r, c = divmod(n, 5)
        ghosts += '<div class="gs hide" id="gs%d" style="left:%dpx;top:%dpx"></div>' % (
            n, RX0 + c * (RW + RG), RY0 + (r + 2) * (RH + RG))
    was_y = int(TKH * (1 - LV100))
    t100 = tank("t2A", TKX, TKY, TKW, TKH, "lg").replace(
        '<div class="liq" id="t2AL"></div>',
        '<div class="liq" id="t2AL"></div><div class="was hide" id="t2W" style="top:%dpx"></div>' % was_y)
    lens_y = TKY + was_y - 80
    lens = ('<svg class="lens hide" id="lens" width="260" height="260" viewBox="0 0 260 260" style="left:%dpx;top:%dpx">'
            '<circle cx="100" cy="100" r="84" fill="rgba(255,255,255,0.12)" stroke="#fff" stroke-width="12"/>'
            '<path d="M162 162 L232 232" stroke="#fff" stroke-width="22" stroke-linecap="round"/></svg>'
            % (TKX, lens_y))
    task = ('<div class="tc hide" id="task" style="left:335px;top:560px;width:410px;height:130px">'
            '<div class="cbx" style="left:34px;top:37px"><div class="cbf" id="tcb">'
            '<svg viewBox="0 0 24 24"><path id="tcbp" d="M5.4 12.6l4.3 4.3 8.9-9.5"/></svg></div></div>'
            '<i class="rr" style="left:116px;top:42px;width:250px;height:22px"></i>'
            '<i class="rr" style="left:116px;top:78px;width:170px;height:18px"></i></div>')
    banner = ('<div class="lb hide" id="lim" style="left:120px;top:800px;width:840px;height:172px">'
              '<div class="ic">%s</div><div class="ti" style="left:164px;top:34px">Ліміт вичерпано</div>'
              '<i class="rr" style="left:166px;top:108px;width:380px;height:20px"></i></div>'
              % stroke("clock", "x"))
    L.append('<div class="g full" id="gT2"><div class="tkg"></div><div class="aurs"></div><div class="grain"></div>'
             + ghosts + cards + checks
             + t100 + tile("t2Ac", 200, TKX, 190, "jelly", g.mark("claude"), extra=chip("t2Az", "$100", 112, -30))
             + tank("t2B", 790, TKY, TKW, TKH, "lg")
             + tile("t2Bc", 200, 790, 190, "jelly", g.mark("claude"), extra=chip("t2Bz", "$20", 120, -30))
             + lens + task + banner + '</div>')
    x2 = UP[0] + 42 + int(856 * FILL2)
    y2 = UP[1] + 330 + 15
    sfx("whoosh-short", "@yakshcho-0.12")
    sfx("pop", "@zmontuiu+0.05")
    sfx("kaching", "@dolariv4", -3)
    sfx("click", "@riznytsiu+0.02")
    sfx("whoosh-short", "@a-0.05", -3)
    sfx("click", "@zadachu+0.2")
    sfx("notification", "@vse+0.02")
    sfx("whoosh-short", "@tomu-0.32", -3)
    return js("""
  G.irisOpen("#gT2", @yakshcho-0.12, {{x2}}, {{y2}}, 0.6);
  drift1("#gT2", @yakshcho-0.12, @tomu-@yakshcho);
  for (var n = 0; n < 10; n++) arr("#rc" + n, @zmontuiu-0.05 + n * 0.06, {s: 0.4, y: 40, d: 0.7});
  arr("#t2Ac", @klod5-0.05, {s: 0.5, y: 30});
  G.ripple("#t2AcR", @klod5+0.25);
  arr("#t2A", @pidpystsi-0.05, {s: 0.8, y: 60, d: 0.8});
  tl.fromTo("#t2AL", {scaleY: 0}, {scaleY: {{lv}}, duration: 0.8, ease: "power2.out"}, @pidpystsi+0.1);
  arr("#t2Az", @d100d-0.03, {s: 0.3, y: 20, d: 0.6});
  /* ten reels done; the tank hardly moves */
  tl.set("#t2W", {autoAlpha: 1}, @mene);
  for (var m = 0; m < 10; m++) tl.fromTo("#rk" + m, {autoAlpha: 0, scale: 0.3}, {autoAlpha: 1, scale: 1, duration: 0.4, ease: POP}, @mene+0.02 + m * 0.07);
  tl.to("#t2AL", {scaleY: {{lv2}}, duration: 0.8, ease: "power1.inOut"}, @mene+0.05);
  G.bump("#t2A", @kupa); shn("#t2Ac .sheen", @kupa+0.05);
  for (var q = 0; q < 10; q++) bin("#gs" + q, @pratsiuv-0.05 + q * 0.05, 8, 0.3);
  arr("#lens", @riznytsiu-0.25, {s: 0.5, x: 40, y: 40, d: 0.7});
  tl.to("#lens", {keyframes: {rotation: [0, -8, 6, -3, 0]}, transformOrigin: "100px 100px", duration: 0.6, ease: "none"}, @pomichu);
  var gone = []; for (var z = 0; z < 10; z++) gone.push("#rc" + z, "#rk" + z, "#gs" + z);
  bout(gone.concat(["#lens"]), @a-0.1, 10, 0.3);
  /* the $20 tank */
  arr("#t2Bc", @a+0.02, {s: 0.5, y: 30});
  arr("#t2Bz", @d20e-0.03, {s: 0.3, y: 20, d: 0.6});
  arr("#t2B", @dolarakhe-0.4, {s: 0.8, y: 60, d: 0.8});
  tl.fromTo("#t2BL", {scaleY: 0}, {scaleY: {{lv20}}, duration: 0.8, ease: "power2.out"}, @enerhii3);
  arr("#task", @odnu-0.08, {s: 0.6, y: 30, d: 0.7});
  tl.fromTo("#tcb", {autoAlpha: 0, scale: 0.4}, {autoAlpha: 1, scale: 1, duration: 0.4, ease: POP}, @zadachu+0.2);
  draw2("tcbp", @zadachu+0.26, 0.3);
  tl.to("#t2BL", {scaleY: 0, duration: 0.9, ease: "power2.in"}, @zadachu+0.4);
  tl.to("#t2Bc", {filter: "saturate(0.15) brightness(0.8)", duration: 0.4}, @vse-0.1);
  arr("#lim", @vse-0.06, {s: 0.85, y: -60, d: 0.7, ease: SOFT});
  G.haptic("#lim", @vse+0.4);
  G.irisClose("#gT2", @tomu-0.3, 890, 290, 0.5);""").replace("{{x2}}", str(x2)).replace("{{y2}}", str(y2)) \
        .replace("{{lv}}", str(LV100)).replace("{{lv2}}", str(LV100b)).replace("{{lv20}}", str(LV20))


# ===========================================================================
# E · start on $20, climb to $100
@beat
def e_steps():
    steps = ('<div class="shelf edge hide" id="stp1" style="left:110px;top:470px;width:380px;height:130px;border-radius:36px"></div>'
             '<div class="shelf edge hide" id="stp2" style="left:590px;top:330px;width:380px;height:270px;border-radius:36px"></div>')
    right = ('<div class="sqring" id="eRR" style="left:695px;top:160px;width:170px;height:170px"></div>'
             '<div class="tw hide ghost" id="eR" style="left:695px;top:160px;width:170px;height:170px">'
             '<div class="clear">%s</div><div class="jelly" id="eRj" style="opacity:0;visibility:hidden">%s'
             '<div class="sheen"></div></div>%s</div>' % (g.mark("claude"), g.mark("claude"), chip("eRz", "$100", 96, -30)))
    stars = "".join('<svg class="star hide" id="es%d" viewBox="0 0 24 24" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx">'
                    '<path d="M12 1.5c.7 5.4 2.8 7.6 8.5 8.5-5.7.9-7.8 3.1-8.5 8.5-.7-5.4-2.8-7.6-8.5-8.5 5.7-.9 7.8-3.1 8.5-8.5z"/></svg>'
                    % (i, x, y, s, s) for i, (x, y, s) in enumerate(((150, 250, 70), (410, 268, 52), (402, 400, 40))))
    arrow = ('<svg class="abs" width="1080" height="700" style="left:0;top:0;overflow:visible">'
             '<path class="arw" id="eA" style="opacity:0" d="M408 300 C 470 200 570 182 664 226"/>'
             '<path class="arw" id="eAh" style="opacity:0" d="M622 196 L670 228 L626 262"/></svg>')
    L.append('<div class="g full" id="gE">' + steps + arrow + stars
             + tile("eL", 170, 215, 300, "jelly", g.mark("claude"), extra=chip("eLz", "$20", 112, -30))
             + tile("eK", 64, 190, 276, "jelly", stroke("check"), extra_cls="circ", ring=False)
             + right + '</div>')
    sfx("pop", "@spokiino+0.02", -2)
    sfx("sparkle", "@kruto")
    sfx("pop", "@d100f", -2)
    return js("""
  tl.set("#gE", {autoAlpha: 1}, @tomu-0.3);
  bin(["#stp1", "#stp2"], @tomu-0.2, 12, 0.4);
  arr("#eL", @tomu-0.22, {s: 0.45, x: 590, y: -95, d: 0.8});
  G.ripple("#eLR", @pochynaty+0.1);
  arr("#eR", @pochynaty+0.25, {s: 0.6, y: 20});
  arr("#eK", @spokiino-0.03, {s: 0.3, y: 0, d: 0.6});
  arr("#eLz", @z20-0.03, {s: 0.3, y: 20, d: 0.6});
  [0, 1, 2].forEach(function (i) {
    tl.fromTo("#es" + i, {autoAlpha: 0, scale: 0.2, rotation: -40}, {autoAlpha: 1, scale: 1, rotation: 0, duration: 0.5, ease: POP}, @kruto-0.1 + i * 0.08);
    tl.to("#es" + i, {autoAlpha: 0, scale: 0.6, duration: 0.4, ease: "power2.in"}, @kruto+0.9 + i * 0.05);
  });
  shn("#eL .sheen", @kruto);
  tl.set(["#eA", "#eAh"], {opacity: 1}, @pidnim-0.05);
  draw2("eA", @pidnim-0.05, 0.5); draw2("eAh", @pidnim+0.4, 0.2);
  tl.to("#eRj", {autoAlpha: 1, duration: 0.3}, @pidnim+0.5);
  G.bump("#eR", @pidnim+0.55); G.ripple("#eRR", @pidnim+0.6);
  arr("#eRz", @d100f-0.03, {s: 0.3, y: 20, d: 0.6});
  shn("#eRj .sheen", @d100f+0.1);
  bout("#gE", @a2+0.3, 10, 0.3);""")


# ===========================================================================
# F · CTA: the timeline is back, DM «дизайн», the free lesson powers the edit
@beat
def f_cta():
    dm = ('<div class="dglass edge hide" id="dm" style="left:90px;top:110px;width:900px;height:124px;border-radius:62px">'
          '<div class="tw circ" style="left:24px;top:20px;width:84px;height:84px"><div class="clear">%s</div></div>'
          '<div class="ph0" id="dmPh">Повідомлення…</div><div id="dmT" style="clip-path:inset(0 100%% 0 0)">дизайн</div>'
          '<div class="tw circ" id="dmS" style="left:800px;top:18px;width:88px;height:88px"><div class="jelly">%s</div></div>'
          '</div>' % (g.mark("instagram"), stroke("up")))
    lesson = ('<div class="ls hide" id="ls" style="left:110px;top:100px;width:860px;height:290px">'
              '<div class="pl">%s</div><div class="ti" style="left:236px;top:76px">Безкоштовний урок</div>'
              '<i class="rr" style="left:238px;top:160px;width:420px;height:22px"></i>'
              '<i class="rr" style="left:238px;top:198px;width:300px;height:22px"></i>'
              '<div class="shc"><div class="sheen"></div></div></div>' % PLAY)
    L.append('<div class="g full" id="gF">' + cable("fK", "M540 392 L540 434") + strip("stF", 70, 430)
             + dm + lesson + '</div>')
    sfx("pop", "@montazh2-0.05", -3)
    sfx("typing", "@dyzain", -1)
    sfx("click", "@i_send+0.02")
    sfx("ping", "@dostup", -2)
    return js("""
  tl.set("#gF", {autoAlpha: 1}, @a2+0.3);
  arr("#stF", @montazh2-0.1, {s: 0.8, y: 40});
  arr("#dm", @pyshy-0.08, {s: 0.85, y: -40, d: 0.7});
  tl.set("#dmPh", {autoAlpha: 0}, @dyzain);
  tl.fromTo("#dmT", {clipPath: "inset(0 100% 0 0)"}, {clipPath: "inset(0 0% 0 0)", duration: 0.32, ease: "steps(6)", immediateRender: false}, @dyzain);
  G.bump("#dmS", @i_send);
  tl.to("#dm", {y: -50, autoAlpha: 0, duration: 0.3, ease: "power2.in"}, @i_send+0.15);
  arr("#ls", @dostup-0.1, {s: 0.75, y: 40, d: 0.8});
  shn("#ls .sheen", @dostup+0.3);
  tl.set(["#fKT", "#fKC"], {autoAlpha: 1}, @osnovu-0.1);
  draw2("fKT", @osnovu-0.1, 0.3); draw2("fKC", @osnovu-0.1, 0.3);
  G.packet("fKP", @osnovu+0.2, 0.35);
  G.bump("#stF", @osnovu+0.5);
  for (var h = 0; h < 5; h++) tl.fromTo("#stFh" + h, {autoAlpha: 0}, {autoAlpha: 1, duration: 0.25}, @osnovu+0.55 + h * 0.22);
  tl.fromTo("#stFP", {x: 0}, {x: 840, duration: @dur-@osnovu-0.55, ease: "none"}, @osnovu+0.55);""")


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


def span_words(a, b):
    return (round(a - 0.02, 3), round(b, 3), "")


# captions that would repeat the graphic's own words (STYLE.md §2b.1)
BLACKOUT = [
    span_words(T["d20a"], E(u"доларів", 4.86)),                 # the $20 tag
    span_words(T["d20b"], T["dolariv2e"]),                      # $20 … $100
    span_words(T["nul"], T["nule"]),                            # the 0 stamp
    span_words(T["d20c"], T["dolariv3e"]),                      # $20 / $100 / $200
    span_words(T["limit1"], T["hodyne"]),                       # «Ліміт на тиждень», «Ліміт на 5 годин»
    span_words(T["d100d"], T["dolariv4e"]),                     # $100
    span_words(T["d20e"], T["dolarakhe"]),                      # $20
    span_words(T["z20"], T["dolariv5e"]),                       # $20
    span_words(T["d100f"], T["d100fe"]),                        # $100
    span_words(T["dyzain"], T["dyzaine"]),                      # the DM types it
    span_words(T["bezkoshtovnoho"], T["urokue"]),               # «Безкоштовний урок»
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
        title=u"Reel 40 — $20 чи $100",
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
