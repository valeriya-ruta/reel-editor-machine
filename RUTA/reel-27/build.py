# -*- coding: utf-8 -*-
"""Reel 27 — «Питання від підписниці…». Posts 2026-10-10.

An explainer: a follower asks whether Claude can be hooked to Threads, read
which posts get reach, and write new ones in her style. Answer: Windsor +
Threads for the data, a copywriter skill for the voice; the limit is that it
only sees your own Threads.

The one object is **her Threads**: the question arrives as a DM, her feed is
read and sorted by reach, new posts come out of Claude + the skill wearing the
winning topic, then the same Threads profile sits inside a boundary it cannot
search past.

Chain:  near: a DM notification («підписниця») opens into the question bubble,
the words light as she reads them, markers on the key phrases -> her reply
«Можна» -> the chat folds into her name capsule (Рута · технічна продюсерка)
-> her closeup (clear) -> a shelf: Claude · ? · Threads; the «?» pulses on
«улюблений» -> her «Хто?» closeup (hard cut, clear) -> the «?» flips to
Windsor «w.»; cables to Claude and to Threads -> the iris opens out of the
Threads tile: her feed scrolls in, reach bars fill, topic chips, hook markers,
the feed sorts itself by reach, the winners light -> the iris closes onto the
Claude tile: the copywriter skill plugs in, her posts are fed into it, her
face lands on it -> «ця пара»: the iris opens out of the pair: two new posts
are written, a comment gets a reply, the winning topic chip stamps onto the new
posts -> the iris closes onto her profile: a boundary draws around it, a scan
reads only inside it, the rest of Threads appears outside, the magnifier
bumps into the boundary -> it becomes Claude's in-app browser: threads.com
types, the bar crawls, the spinner dies, a warning -> an org chart (owner +
team) -> the system row, the owner docks into its last slot -> a comment box
types «+», it posts, her reply comes back, liked -> Стежити.

usage: python build.py   (then: python ../tools/sfx.py mix 27)
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

CUT = json.load(io.open(os.path.join(ROOT, "work", "r27", "cut.json"), encoding="utf-8"))
DUR = 61.150           # (plate frames - 0.5) / 30, floored to 3 decimals
FPS = 30
k = Kit(width=1080, height=1920, fps=FPS, duration=DUR)
g = Glass(["claude", "threads", "instagram"])
k.css(g.css())

# ---------------------------------------------------------------------------
# NO-PAINT: her closeups (cut.py «punch»): «…і я знаю все про штучний інтелект»
# and «Хто?». Captions only.
NO_PAINT = [tuple(x) for x in CUT["no_paint"]]

CAPS = k.load_captions(os.path.join(ROOT, "work", "r27", "captions.json"))
# whisper errors the aligner kept as "her wording": restore the real word
FIX = {u"Треться,": u"тредсів,", u"інтелект😁": u"інтелект.", u"Для": u"для",
       u"Вінцер!": u"Windsor!", u"третсі": u"Threads", u"трець.": u"тредс.",
       u"зомні": u"зовні,", u"трець,": u"Threads,", u"Хочеш": u"хочеш",
       u"то Напиши": u"то напиши", u"назнуштувати": u"налаштувати"}
for c in CAPS:
    c["w"] = FIX.get(c["w"], c["w"])


def _at(word, near):
    return min((i for i, c in enumerate(CAPS) if c["w"] == word), key=lambda i: abs(CAPS[i]["s"] - near))


# «саме в обласниці агенції» is «сама власниця агенції»
_i = _at(u"саме", 53.46)
assert CAPS[_i + 1]["w"] == u"в" and CAPS[_i + 2]["w"] == u"обласниці", CAPS[_i:_i + 3]
CAPS[_i]["w"] = u"сама"
CAPS[_i + 1]["w"] = u"власниця"
CAPS[_i + 1]["e"] = CAPS[_i + 2]["e"]
del CAPS[_i + 2]
# words whisper timed but did not hear the end of: «у [тебе]», «саме [тобі]»
CAPS[_at(u"у", 39.08)]["w"] = u"у тебе."
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
    c = min(hits, key=lambda c: abs(c["s"] - near))
    assert abs(c["s"] - near) < 0.6, (word, near, c["s"])
    return c["e"]


T = {
    "pidp": S(u"підписниці", 0.73), "chy": S(u"Чи", 1.625), "pidkl0": S(u"підключити", 2.245),
    "kloda_e": E(u"Клода", 2.898), "tredsiv": S(u"тредсів", 3.465), "tredsiv_e": E(u"тредсів", 3.465),
    "analiz": S(u"аналізував", 4.598), "analiz_e": E(u"аналізував", 4.598), "yaki": S(u"які", 5.178),
    "nabyr": S(u"набирають", 5.898), "nabyr_e": E(u"набирають", 5.898), "naib": S(u"найбільше", 6.298),
    "okhopl1_e": E(u"охоплення", 6.738), "vmoiemu": S(u"в", 8.788), "styli_e": E(u"стилі", 9.328),
    "temy0": S(u"ті", 9.828), "temy0_e": E(u"теми", 10.388),
    "pratsiuiut1": S(u"що", 10.748), "pratsiuiut1e": E(u"працюють", 10.87),
    "mozhna": S(u"Можна", 11.711), "mozhnae": E(u"Можна", 11.711), "ruta": S(u"Рута", 12.711),
    "tekhn": S(u"технічна", 13.191), "prodiue": E(u"продюсерка", 13.571),
    "dlia": S(u"для", 16.403), "tsoho": S(u"цього", 16.663), "potriben": S(u"потрібен", 17.423),
    "uliub": S(u"улюблений", 18.143), "pravylno": S(u"Правильно", 19.983), "windsor": S("Windsor", 20.543),
    "pidkl": S(u"Підключаєш", 21.316), "threads1": S("Threads", 22.336), "bachyt": S(u"бачить", 22.916),
    "tredsy": S(u"тредси", 23.636), "stat": S(u"статистику", 24.516), "temy1": S(u"теми", 25.4),
    "khuky": S(u"хуки", 26.16), "krashche": S(u"краще", 26.7), "zbyr": S(u"збирають", 27.1),
    "okhopl2e": E(u"охоплення", 27.48),
    "a": S(u"А", 28.133), "stavysh": S(u"ставиш", 29.163), "skil": S(u"скіл", 29.523),
    "kopire": E(u"копірайтера", 29.783), "navch": S(u"навчений", 30.663), "tvoiemu": S(u"твоєму", 31.583),
    "tsia": S(u"ця", 32.777), "para": S(u"пара", 33.077), "heneruie": S(u"генерує", 33.837),
    "novi": S(u"нові", 34.777), "vidpov": S(u"відповіді", 35.597), "komenty": S(u"коменти", 36.297),
    "temy2": S(u"теми", 37.496), "realno": S(u"реально", 38.156), "pratsiuiut2": S(u"працюють", 38.636),
    "utebee": E(u"тебе", 39.076),
    "ale": S(u"Але", 39.533), "mezha": S(u"межа", 39.995), "analizuie": S(u"аналізує", 40.695),
    "tilky": S(u"тільки", 41.195), "vlasnyi": S(u"власний", 42.035), "shukav": S(u"шукав", 43.944),
    "novi2": S(u"нові", 44.464), "zovni": S(u"зовні", 45.084), "vsiomu": S(u"всьому", 45.524),
    "zapusk": S(u"запускати", 46.837), "okremyi": S(u"окремий", 47.657), "vnutr": S(u"внутрішній", 48.597),
    "brauzere": E(u"браузер", 49.097), "poky": S(u"поки", 49.758), "pohano": S(u"погано", 50.778),
    "chesnoe": E(u"чесно", 51.378),
    "sama": S(u"сама", 53.46), "ahentsii": S(u"агенції", 54.44), "khochesh": S(u"хочеш", 55.24),
    "systemu": S(u"систему", 55.84), "tebe": S(u"тебе", 56.38), "napyshy": S(u"напиши", 56.942),
    "plius": S(u"плюс", 57.322), "pliuse": E(u"плюс", 57.322), "komentar": S(u"коментарях", 57.602),
    "rozkazhu": S(u"розкажу", 58.362), "nalasht": S(u"налаштувати", 59.042), "tobi": S(u"тобі", 59.762),
    "same2": S(u"саме", 59.53), "ashche": S(u"ще", 60.233), "pidpysh": S(u"підпишись", 60.393),
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
    SFX.append({"t": round(max(0.0, t), 3), "name": name, "db": db})


# On-screen windows of every group, checked against NO_PAINT.
WINDOWS = []


def win(gid, a, b):
    WINDOWS.append((gid, a, b))
    return ('  tl.set("#%s", {autoAlpha: 1}, %.3f); tl.set("#%s", {autoAlpha: 0}, %.3f);'
            % (gid, a, gid, b))


# ---------------------------------------------------------------------------
# Glyphs
STROKES = {
    "up": '<path d="M12 19.2V5.4M6.2 11l5.8-5.8 5.8 5.8"/>',
    "check": '<path d="M5.4 12.6l4.3 4.3 8.9-9.5"/>',
    "eye": '<path d="M2.6 12s3.4-6.4 9.4-6.4 9.4 6.4 9.4 6.4-3.4 6.4-9.4 6.4S2.6 12 2.6 12z"/><circle cx="12" cy="12" r="2.9"/>',
    "pen": '<path d="M15.6 4.4l4 4L8.9 19.1l-5.2 1.2 1.2-5.2z"/><path d="M13.3 6.7l4 4"/>',
    "hash": '<path d="M10 4.2L8 19.8M16 4.2l-2 15.6M4.8 9.2h15M4 14.8h15"/>',
    "search": '<circle cx="10.4" cy="10.4" r="6"/><path d="M15 15l5.2 5.2"/>',
    "lock": '<rect x="5" y="10.5" width="14" height="10" rx="2.5"/><path d="M8.2 10.5V8a3.8 3.8 0 0 1 7.6 0v2.5"/>',
    "alert": '<path d="M12 3.9L2.9 19.7h18.2zM12 9.9v4.4M12 17.1v.2"/>',   # one path: a zero-width bbox drops url(#gw)
    "plus": '<path d="M12 5.2v13.6M5.2 12h13.6"/>',
}
PERSON = ('<svg class="pf" viewBox="0 0 24 24"><circle cx="12" cy="9" r="4.3"/>'
          '<path d="M4.2 21c1.1-4.4 4.3-6.6 7.8-6.6s6.7 2.2 7.8 6.6z"/></svg>')
HEART = ("M12 20.6s-7.6-4.5-9.4-9.3C1.3 7.8 3.5 4.4 7 4.4c2 0 3.7 1.1 5 3 "
         "1.3-1.9 3-3 5-3 3.5 0 5.7 3.4 4.4 6.9-1.8 4.8-9.4 9.3-9.4 9.3z")


def stroke(name, cls="sk"):
    return '<svg class="%s" viewBox="0 0 24 24">%s</svg>' % (cls, STROKES[name])


def wmark(size):
    """Windsor has no icon: its wordmark «w.» (style-test)."""
    return '<span class="wmark ws" style="font-size:%dpx">w<i>.</i></span>' % size


def tile(tid, size, x, y, material, inner, extra_cls="", hide=True, ring=True):
    circ = "circ" in extra_cls
    r = ('<div class="sqring%s" id="%sR" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx"></div>'
         % (" rc" if circ else "", tid, x, y, size, size)) if ring else ""
    return ('%s<div class="tw%s %s" id="%s" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx">'
            '<div class="%s">%s<div class="sheen"></div></div></div>'
            % (r, " hide" if hide else "", extra_cls, tid, x, y, size, size, material, inner))


def tkground():
    return ('<div class="tkg"></div><div class="aurs"></div>'
            '<svg class="wmk" viewBox="0 0 24 24"><use href="#i-threads" width="24" height="24"/></svg>'
            '<div class="grain"></div>')


# a Threads post card (her avatar, name, hook line, body line, reach row, topic chip)
def post(pid, x, y, hook, body, chip, hide=True, reach=True, badge=False, ring=False):
    return (
        '<div class="post%s" id="%s" style="left:%dpx;top:%dpx">'
        '<i class="av"></i><i class="nm"></i><i class="hd"></i>'
        '<div class="th">%s</div>'
        '<div class="chp %s">%s<b></b></div>'
        '<i class="hkm" style="width:%dpx"></i><i class="hk" style="width:%dpx"></i>'
        '<i class="bd" style="width:%dpx"></i>'
        '%s'
        '%s%s'
        '<div class="shc"><div class="sheen"></div></div></div>'
        % (" hide" if hide else "", pid, x, y, g.mark("threads", "pm"), chip, stroke("hash"),
           hook + 20, hook, body,
           ('<div class="ey">%s</div><i class="rt"></i><i class="rf"></i>' % stroke("eye")) if reach else "",
           ('<div class="tw circ ub" style="left:812px;top:190px;width:56px;height:56px">'
            '<div class="jelly">%s</div></div>' % stroke("up")) if badge else "",
           '<i class="wn"></i>' if ring else ""))


k.css("""
.abs, .cx { position: absolute; }
.hide { opacity: 0; visibility: hidden; }
.tw { position: absolute; }
.sk { fill: none; stroke: url(#gw); stroke-width: 2.3; stroke-linecap: round; stroke-linejoin: round;
  width: 50%; height: 50%; position: relative; z-index: 1; overflow: visible; }
.pearl .sk { stroke: #17141c; }
.pf { width: 100%; height: 100%; fill: rgba(180,18,47,0.42); transform: translateY(8%); }
.jelly .pf { fill: url(#gw); width: 62%; height: 62%; }
.pearl .pf { width: 64%; height: 64%; }
.circ .jelly, .circ .pearl, .circ .clear, .circ .sheen { border-radius: 50%; }
.sqring.rc { border-radius: 50%; }
.wmark.ws { transform: translate(2%, -3%); }
.pm { width: 100%; height: 100%; fill: #17141c; display: block; }
.shc { position: absolute; inset: 0; border-radius: inherit; overflow: hidden; pointer-events: none; }
.shc .sheen { mix-blend-mode: normal; opacity: 0.4; }
.aurs { position: absolute; left: -700px; top: -700px; width: 2480px; height: 3320px; pointer-events: none;
  background:
    radial-gradient(circle 526px at 1560px 880px, rgba(255,110,156,0.50), rgba(255,110,156,0)),
    radial-gradient(circle 634px at 760px 2360px, rgba(222,32,74,0.55), rgba(222,32,74,0)),
    radial-gradient(circle 382px at 1480px 1910px, rgba(255,198,214,0.20), rgba(255,198,214,0)); }
.wmk { position: absolute; left: 430px; top: 1010px; width: 1100px; height: 1100px;
  fill: rgba(255,255,255,0.05); transform: rotate(-8deg); }
.av-img { background: url("assets/avatar.jpg") center / cover no-repeat; border-radius: 50%; }
.gav { border-radius: 50%; overflow: hidden; background: linear-gradient(160deg, #ffffff 0%, #f6e3e9 100%);
  box-shadow: inset 0 2px 1px #fff, 0 8px 18px -6px rgba(10,0,4,0.5); }

/* ---- A · her real DM screenshot ---- */
.dmc { position: absolute; border-radius: 52px; overflow: hidden; background: #ffffff;
  box-shadow: inset 0 0 0 1px rgba(255,255,255,0.6), 0 50px 100px -34px rgba(20,2,8,0.7), 0 6px 16px rgba(20,2,8,0.18); }
#dmS { position: absolute; left: 0; top: 0; width: 100%; height: 1000px; }
.dms { position: absolute; left: 0; width: 920px; background-image: url("assets/proof-dm.jpg");
  background-size: 920px auto; background-repeat: no-repeat; }
.dmk { position: absolute; display: block; border-radius: 8px; background: rgba(255,92,143,0.42); mix-blend-mode: multiply; }
#cap .ca { position: absolute; left: 26px; top: 26px; width: 96px; height: 96px;
  box-shadow: 0 0 0 3px rgba(255,255,255,0.55), 0 10px 24px -8px rgba(10,0,4,0.5); }
#cap .nm { position: absolute; left: 150px; top: 20px; font-size: 48px; font-weight: 700; letter-spacing: -0.015em; }
#cap .rl { position: absolute; left: 150px; top: 80px; font-size: 32px; font-weight: 500; color: rgba(255,255,255,0.76); }

/* ---- B · the «?» slot ---- */
.slotf { position: absolute; inset: 0; border-radius: 22.4%; border: 5px dashed rgba(255,255,255,0.72);
  background: rgba(255,255,255,0.10); display: flex; align-items: center; justify-content: center;
  color: #fff; font-size: 116px; font-weight: 900; }

/* ---- Threads post cards ---- */
.post { position: absolute; width: 920px; height: 250px; border-radius: 48px; overflow: hidden; color: #17141c;
  background: linear-gradient(172deg, #ffffff 0%, #fff9fb 55%, #fdf0f4 100%);
  box-shadow: inset 0 2px 1px #fff, 0 50px 100px -36px rgba(8,0,3,0.72), 0 0 0 1px rgba(255,255,255,0.35); }
.post i { position: absolute; display: block; }
.post .av { left: 34px; top: 28px; width: 72px; height: 72px; border-radius: 50%;
  background: url("assets/avatar.jpg") center / cover no-repeat; box-shadow: 0 0 0 3px #fff, 0 6px 14px -6px rgba(24,4,12,0.4); }
.post .nm { left: 126px; top: 40px; width: 190px; height: 22px; border-radius: 11px; background: rgba(23,20,28,0.78); }
.post .hd { left: 126px; top: 74px; width: 120px; height: 16px; border-radius: 8px; background: rgba(23,20,28,0.22); }
.post .th { position: absolute; right: 36px; top: 36px; width: 50px; height: 50px; }
.post .hkm { left: 22px; top: 115px; height: 48px; border-radius: 14px; background: rgba(255,110,156,0.40);
  transform-origin: 0 50%; }
.post .hk { left: 34px; top: 126px; height: 26px; border-radius: 13px; background: rgba(23,20,28,0.80); transform-origin: 0 50%; }
.post .bd { left: 34px; top: 170px; height: 18px; border-radius: 9px; background: rgba(23,20,28,0.16); transform-origin: 0 50%; }
.post .ey { position: absolute; left: 30px; top: 198px; width: 40px; height: 40px; }
.post .ey .sk { width: 100%; height: 100%; stroke: rgba(23,20,28,0.55); }
.post .rt { left: 84px; top: 209px; width: 600px; height: 18px; border-radius: 9px; background: rgba(23,20,28,0.07); }
.post .rf { left: 84px; top: 209px; width: 600px; height: 18px; border-radius: 9px; transform-origin: 0 50%;
  background: linear-gradient(90deg, #8d0d24 0%, #e0204b 60%, #ff6e9c 100%); }
.post .chp { position: absolute; left: 360px; top: 34px; height: 54px; padding: 0 20px 0 12px; border-radius: 27px;
  display: flex; align-items: center; gap: 8px; background: rgba(23,20,28,0.07); }
.post .chp .sk { width: 32px; height: 32px; stroke: rgba(23,20,28,0.55); stroke-width: 2.6; }
.post .chp b { display: block; width: 76px; height: 12px; border-radius: 6px; background: rgba(23,20,28,0.30); }
.post .chp.hot { background: linear-gradient(165deg, #e0204b 0%, #8d0d24 100%);
  box-shadow: inset 0 2px 1px rgba(255,255,255,0.45), 0 10px 20px -10px rgba(70,4,20,0.6); }
.post .chp.hot .sk { stroke: #fff; } .post .chp.hot b { background: rgba(255,255,255,0.75); }
.post .chp.pink { background: #fbe3ea; } .post .chp.pink .sk { stroke: #b4122f; }
.post .chp.pink b { background: rgba(180,18,47,0.45); }
.post .wn { inset: 0; border-radius: 48px; box-shadow: inset 0 0 0 6px #ff6e9c, inset 0 0 40px rgba(255,110,156,0.35);
  opacity: 0; visibility: hidden; }
.post .ub { z-index: 2; }
.post .ub .sk { width: 56%; height: 56%; }

/* ---- C / TK2 · the copywriter skill ---- */
.skl { position: absolute; border-radius: 52px; overflow: hidden; color: #17141c;
  background: linear-gradient(172deg, #ffffff 0%, #fff9fb 55%, #fdf0f4 100%);
  box-shadow: inset 0 2px 1px #fff, 0 50px 100px -36px rgba(24,4,12,0.62); }
.skl .mi { position: absolute; font-size: 24px; font-weight: 700; letter-spacing: 0.16em; color: rgba(23,20,28,0.42); }
.skl .ti { position: absolute; font-size: 46px; font-weight: 700; letter-spacing: -0.015em; }
.skl i { position: absolute; display: block; }
.skl .sb { height: 22px; border-radius: 11px; background: rgba(23,20,28,0.14); transform-origin: 0 50%; }
.mp { position: absolute; width: 170px; height: 110px; border-radius: 28px;
  background: linear-gradient(172deg, #ffffff 0%, #fdf0f4 100%);
  box-shadow: inset 0 2px 1px #fff, 0 24px 44px -18px rgba(24,4,12,0.6); }
.mp i { position: absolute; display: block; }

/* ---- TK2 · the comment ---- */
.cmc { position: absolute; border-radius: 48px; overflow: hidden; color: #17141c;
  background: linear-gradient(172deg, #ffffff 0%, #fff9fb 55%, #fdf0f4 100%);
  box-shadow: inset 0 2px 1px #fff, 0 50px 100px -36px rgba(8,0,3,0.72); }
.cmc i { position: absolute; display: block; }
.cmc .br { border-radius: 9px; background: rgba(23,20,28,0.16); transform-origin: 0 50%; }
.cmc .bk { border-radius: 10px; background: rgba(23,20,28,0.78); }
.cmc .bp { border-radius: 9px; background: linear-gradient(90deg, #b4122f 0%, #ff6e9c 100%); transform-origin: 0 50%; }

/* ---- D · her profile, the boundary, the rest of Threads ---- */
.prof { position: absolute; border-radius: 44px; overflow: hidden;
  background: linear-gradient(172deg, #ffffff 0%, #fff9fb 55%, #fdf0f4 100%);
  box-shadow: inset 0 2px 1px #fff, 0 40px 80px -30px rgba(24,4,12,0.6); }
.prof i { position: absolute; display: block; }
.gt { border-radius: 16px; background: linear-gradient(150deg, #f4dfe5 0%, #ecc8d0 100%); }
.gtl { position: absolute; inset: 0; border-radius: 16px; opacity: 0; visibility: hidden;
  background: linear-gradient(150deg, #ff8ab0 0%, #e0204b 60%, #8d0d24 100%); }
#scan { left: 20px; top: 196px; width: 260px; height: 8px; border-radius: 4px; background: #ff6e9c;
  box-shadow: 0 0 18px 4px rgba(255,110,156,0.75); }
.bnd { fill: none; stroke: #ff6e9c; stroke-width: 8; stroke-linecap: round;
  filter: drop-shadow(0 0 10px rgba(255,110,156,0.9)); }
.oc { position: absolute; width: 112px; height: 130px; border-radius: 26px;
  background: linear-gradient(158deg, rgba(255,255,255,0.30) 0%, rgba(255,255,255,0.10) 60%, rgba(255,255,255,0.16) 100%);
  box-shadow: inset 0 2px 1px rgba(255,255,255,0.6), 0 20px 40px -20px rgba(24,4,12,0.5); }
.oc i { position: absolute; display: block; }

/* ---- E · the in-app browser ---- */
#br .dot { position: absolute; top: 37px; width: 18px; height: 18px; border-radius: 50%; background: rgba(255,255,255,0.42); }
#url { position: absolute; left: 140px; top: 18px; width: 560px; height: 56px; border-radius: 28px;
  background: rgba(255,255,255,0.14); box-shadow: inset 0 0 0 1.5px rgba(255,255,255,0.12); }
#url .sk { position: absolute; left: 18px; top: 13px; width: 30px; height: 30px; stroke: rgba(255,255,255,0.7); }
#urlT { position: absolute; left: 62px; top: 0; height: 56px; line-height: 56px; font-size: 31px; font-weight: 500;
  color: #fff; white-space: nowrap; }
#prgT { position: absolute; left: 0; top: 92px; width: 900px; height: 7px; background: rgba(255,255,255,0.10); }
#prg { position: absolute; left: 0; top: 92px; width: 900px; height: 7px; transform-origin: 0 50%;
  background: linear-gradient(90deg, #e0204b 0%, #ff6e9c 100%); box-shadow: 0 0 12px rgba(255,110,156,0.8); }
.skc { position: absolute; width: 394px; height: 160px; border-radius: 26px; background: rgba(255,255,255,0.12);
  box-shadow: inset 0 1.5px 1px rgba(255,255,255,0.25); }
.skc i { position: absolute; display: block; border-radius: 8px; background: rgba(255,255,255,0.22); }
.spn { position: absolute; fill: none; stroke: #ff8ab0; stroke-width: 9; stroke-linecap: round; stroke-dasharray: 64 30;
  filter: drop-shadow(0 0 10px rgba(255,110,156,0.8)); }

/* ---- F · CTA ---- */
#cmPh { left: 130px; top: 42px; font-size: 36px; font-weight: 500; color: rgba(255,255,255,0.58); }
#cmTyped { left: 130px; top: 26px; font-size: 64px; font-weight: 900; line-height: 76px; color: #fff; }
#cmCaret { left: 132px; top: 38px; width: 4px; height: 52px; border-radius: 2px; background: #ff9cbc; }
#cmSend { right: 40px; top: 44px; font-size: 32px; font-weight: 700; color: #ff9cbc; }
.cmav { width: 80px; height: 80px; }
#cpUser { left: 128px; top: 28px; font-size: 32px; font-weight: 700; color: #fff; }
#cpUser span, #rpUser span { font-weight: 500; color: rgba(255,255,255,0.55); margin-left: 12px; }
#cpTxt { left: 128px; top: 66px; font-size: 60px; font-weight: 900; line-height: 70px; color: #fff; }
#cpHeart { right: 44px; top: 44px; width: 60px; height: 60px; }
#cpHeart svg { position: absolute; inset: 0; width: 60px; height: 60px; }
#cpHeart .o { fill: none; stroke: rgba(255,255,255,0.8); stroke-width: 1.8; }
#cpHeart .fl { fill: url(#gHeart); }
#rpUser { left: 128px; top: 26px; font-size: 32px; font-weight: 700; color: #fff; }
.rpb { position: absolute; height: 18px; border-radius: 9px; transform-origin: 0 50%;
  background: linear-gradient(90deg, rgba(255,255,255,0.85) 0%, rgba(255,176,204,0.85) 100%); }
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
# A · her follower's real DM (her screenshot — STYLE.md: proof is a screenshot,
# animated around, never retyped); her «Можна» (a tick); the name capsule
DM_SRC_W = 1080
DMX, DMY, DMW, DMH = 80, 80, 920, 560      # the card: a window onto the screenshot
DS = DMW / float(DM_SRC_W)                   # 0.852
SLICES = [(0, 313, "l"), (313, 566, "r"), (566, 1090, "l")]   # follower / Ruta / follower
SCROLL = int(round((1090 - DMH / DS) * DS))  # scroll that brings the last bubble fully in
# highlighter marks, in screenshot px: (x0, x1, line top, line bottom), on her words
MARKS = [
    ("m0", (388, 743, 58, 96), "pidkl0", "kloda_e"),          # «підключити клод» <- «підключити Клода»
    ("m1", (433, 587, 112, 154), "tredsiv", "tredsiv_e"),    # «тредсів»
    ("m2", (193, 417, 178, 210), "analiz", "analiz_e"),      # «аналізував»
    ("m3", (425, 737, 674, 716), "nabyr", "nabyr_e"),        # «краще набирає» <- «набирають»
    ("m4", (194, 413, 726, 770), "naib", "okhopl1_e"),       # «охоплення» <- «найбільше охоплення»
    ("m5", (521, 806, 900, 932), "vmoiemu", "styli_e"),      # «в моєму стилі»
    ("m6", (193, 796, 944, 986), "temy0", "temy0_e"),        # «теми, які набільше збирають» <- «ті самі теми»
    ("m7", (194, 413, 1008, 1038), "pratsiuiut1", "pratsiuiut1e"),   # «охоплення» <- «що працюють»
]


@beat
def a_dm():
    sl = ""
    for n, (y0, y1, side) in enumerate(SLICES):
        sl += ('<div class="dms hide" id="dms%d" style="top:%dpx;height:%dpx;background-position:0 -%dpx;'
               'transform-origin:%s 100%%"></div>' % (n, round(y0 * DS), round((y1 - y0) * DS) + 1,
                                                      round(y0 * DS), "12%" if side == "l" else "88%"))
    mk = ""
    for mid, (x0, x1, a, b), _, _ in MARKS:
        top = (a + 0.36 * (b - a)) * DS
        mk += ('<i class="dmk" id="%s" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx"></i>'
               % (mid, round((x0 - 7) * DS), round(top), round((x1 - x0 + 14) * DS),
                  round(((b - a) * 0.64 + 9) * DS)))
    L.append(
        '<div class="g full" id="gA">'
        '<div class="dmc hide" id="dm" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx">'
        '<div id="dmS">%s%s</div><div class="shc"><div class="sheen"></div></div></div>'
        '<div class="tw hide" id="dmIg" style="left:%dpx;top:%dpx;width:96px;height:96px"><div class="jelly">%s</div></div>'
        '%s'
        '<div class="dglass edge hide" id="cap" style="left:240px;top:250px;width:600px;height:148px;border-radius:74px">'
        '<div class="ca av-img"></div><div class="nm">Рута</div><div class="rl">технічна продюсерка</div></div>'
        '</div>' % (DMX, DMY, DMW, DMH, sl, mk, DMX - 30, DMY - 30, g.mark("instagram"),
                    tile("yes", 170, 455, 245, "jelly", stroke("check"), extra_cls="circ")))
    sfx("notification", 0.1)
    sfx("pop", T["yaki"] - 0.06, -3)
    sfx("pop", T["mozhna"] - 0.01)
    mjs = []
    for mid, _, ta, tb in MARKS:
        a, b = T[ta], T[tb]
        mjs.append('  tl.fromTo("#%s", {scaleX: 0}, {scaleX: 1, duration: %.3f, ease: "power1.inOut", immediateRender: false}, %.3f);'
                   % (mid, max(0.2, b - a), a))
    return win("gA", 0.0, T["prodiue"] + 0.05) + js("""
  gsap.set(".dmk", {scaleX: 0, transformOrigin: "0% 50%"});
  arr("#dm", 0.02, {s: 0.82, y: 40, d: 0.9});
  arr("#dmIg", 0.2, {s: 0.3, y: 10, d: 0.7});
  shn("#dm .sheen", 0.55);
  /* «Питання» — her question lands; Ruta's reply under it */
  bin("#dms0", 0.12, 10, 0.3);
  tl.fromTo("#dms0", {scale: 0.86, y: 26}, {scale: 1, y: 0, duration: 0.75, ease: POP}, 0.12);
  bin("#dms1", @pidp+0.1, 10, 0.3);
  tl.fromTo("#dms1", {scale: 0.86, y: 26}, {scale: 1, y: 0, duration: 0.75, ease: POP}, @pidp+0.1);
  /* «…які дописи» — the conversation scrolls; her answer lands */
  tl.to("#dmS", {y: -{{scroll}}, duration: 0.7, ease: SP}, @yaki-0.22);
  bin("#dms2", @yaki-0.12, 10, 0.3);
  tl.fromTo("#dms2", {scale: 0.9, y: 60}, {scale: 1, y: 0, duration: 0.8, ease: POP}, @yaki-0.12);
{{marks}}
  /* «Можна» — yes */
  tl.to("#dm", {scale: 0.3, y: -40, duration: 0.42, ease: "power3.in"}, @mozhna-0.16);
  bout(["#dm", "#dmIg"], @mozhna-0.06, 12, 0.28);
  arr("#yes", @mozhna-0.02, {s: 0.3, y: 0, d: 0.7}); G.ripple("#yesR", @mozhna+0.2);
  /* «я Рута, твоя технічна продюсерка» — the name capsule */
  tl.to("#yes", {x: -196, y: 34, scale: 0.56, duration: 0.42, ease: "power3.in"}, @ruta-0.3);
  tl.to("#yes", {autoAlpha: 0, duration: 0.14}, @ruta-0.02);
  arr("#cap", @ruta-0.1, {s: 0.75, y: 40, d: 0.8});
  gsap.set(["#cap .ca", "#cap .nm", "#cap .rl"], {autoAlpha: 0});
  tl.fromTo("#cap .ca", {scale: 0.5, autoAlpha: 0}, {scale: 1, autoAlpha: 1, duration: 0.55, ease: SP}, @ruta-0.04);
  bin("#cap .nm", @ruta+0.02, 10, 0.3);
  tl.fromTo("#cap .nm", {x: -18}, {x: 0, duration: 0.6, ease: SP}, @ruta+0.02);
  bin("#cap .rl", @tekhn-0.02, 10, 0.3);
  tl.fromTo("#cap .rl", {x: -18}, {x: 0, duration: 0.6, ease: SP}, @tekhn-0.02);
  bout("#cap", @prodiue-0.24, 10, 0.24);""").replace("{{marks}}", "\n".join(mjs)).replace("{{scroll}}", str(SCROLL))


# ===========================================================================
# B · Claude · ? · Threads -> «Windsor!» -> cables
@beat
def b_windsor():
    cab = ('<svg class="cab abs" width="1080" height="700" viewBox="0 0 1080 700" style="left:0;top:0">'
           '<path class="tube hide" id="cT1" d="M322 320 C 362 312 403 312 443 320"/><path class="core hide" id="cC1" d="M322 320 C 362 312 403 312 443 320"/>'
           '<path class="tube hide" id="cT2" d="M637 320 C 677 312 718 312 758 320"/><path class="core hide" id="cC2" d="M637 320 C 677 312 718 312 758 320"/>'
           '<g class="pkg"><path class="pkt" id="cP1" style="opacity:0" d="M443 320 C 403 312 362 312 322 320"/>'
           '<path class="pkt" id="cP2" style="opacity:0" d="M758 320 C 718 312 677 312 637 320"/></g></svg>')
    L.append('<div class="g full" id="gB">'
             '<div class="shelf edge hide" id="shB" style="left:70px;top:170px;width:940px;height:300px"></div>'
             + cab
             + tile("bCl", 190, 130, 225, "jelly", g.mark("claude"))
             + '<div class="tw hide" id="slot" style="left:445px;top:225px;width:190px;height:190px">'
               '<div class="slotf">?</div></div>'
             + tile("bW", 190, 445, 225, "pearl", wmark(124))
             + tile("bTh", 190, 760, 225, "pearl", g.mark("threads"))
             + '</div>')
    sfx("whoosh-short", T["dlia"] - 0.08, -3)
    sfx("pop", T["potriben"] - 0.03, -3)
    sfx("pop", T["windsor"] + 0.04)
    sfx("click-soft", T["threads1"] - 0.2)
    # her «Хто?» closeup is a hard cut: the shelf cuts out with the shot and back in after it
    np = [p for p in NO_PAINT if T["uliub"] < p[0] < T["windsor"]][0]
    return (win("gB", T["dlia"] - 0.15, np[0]) + "\n" + win("gB", np[1], T["bachyt"] + 1.0) + "\n" + js("""
  arr("#shB", @dlia-0.12, {s: 0.86, y: 30, d: 0.8});
  arr("#bCl", @dlia-0.02, {s: 0.4, y: 30}); G.ripple("#bClR", @dlia+0.33);
  arr("#bTh", @tsoho+0.04, {s: 0.4, y: 30}); G.ripple("#bThR", @tsoho+0.4);
  arr("#slot", @potriben-0.06, {s: 0.5, y: 20, d: 0.7});
  G.bump("#slot", @uliub+0.12);
  /* «Windsor!» — the «?» flips to the w. */
  tl.to("#slot", {rotationY: 90, transformPerspective: 900, duration: 0.16, ease: "power2.in"}, @windsor-0.12);
  tl.set("#slot", {autoAlpha: 0}, @windsor+0.04);
  tl.set("#bW", {autoAlpha: 1}, @windsor+0.04);
  tl.fromTo("#bW", {rotationY: -90, transformPerspective: 900}, {rotationY: 0, duration: 0.8, ease: FLIP, immediateRender: false}, @windsor+0.04);
  G.ripple("#bWR", @windsor+0.3); shn("#bW .sheen", @windsor+0.35);
  /* «Підключаєш його» — to Claude; «до Threads» — to Threads */
  tl.set(["#cT1", "#cC1"], {autoAlpha: 1}, @pidkl-0.02);
  draw2("cT1", @pidkl-0.02, 0.4); draw2("cC1", @pidkl-0.02, 0.4);
  G.packet("cP1", @pidkl+0.36, 0.4); G.bump("#bCl", @pidkl+0.74);
  tl.set(["#cT2", "#cC2"], {autoAlpha: 1}, @threads1-0.24);
  draw2("cT2", @threads1-0.24, 0.4); draw2("cC2", @threads1-0.24, 0.4);
  G.ripple("#bThR", @threads1+0.12);
  G.packet("cP2", @threads1+0.16, 0.36); G.bump("#bW", @threads1+0.5);"""))


# ===========================================================================
# TK1 · the iris opens out of Threads: her feed, reach, topics, hooks, sorted
FEED_Y = [150, 410, 670, 930]
REACH = [0.38, 0.92, 0.55, 0.80]
HOOK = [600, 660, 540, 700]
BODY = [520, 440, 600, 480]
TOPIC = ["grey", "hot", "pink", "hot"]
ORDER = sorted(range(4), key=lambda i: -REACH[i])       # new slot of each card: by reach


@beat
def t1_feed():
    cards = "".join(post("p%d" % i, 80, FEED_Y[i], HOOK[i], BODY[i], TOPIC[i], hide=True,
                         badge=TOPIC[i] == "hot", ring=TOPIC[i] == "hot") for i in range(4))
    L.append('<div class="g full" id="gT1">' + tkground() + cards + '</div>')
    sfx("whoosh-short", T["bachyt"] - 0.2)
    sfx("click-soft", T["stat"] + 0.02, -2)
    sfx("pop", T["temy1"] + 0.02, -3)
    sfx("whoosh-short", T["krashche"] + 0.02, -2)
    t_open, t_close = T["bachyt"] - 0.2, T["okhopl2e"] - 0.06
    WINDOWS.append(("gT1", t_open, t_close + 0.52))
    moves, lose = [], []
    for slot, i in enumerate(ORDER):
        dy = FEED_Y[slot] - FEED_Y[i]
        moves.append('  tl.to("#p%d", {y: %d, duration: 0.85, ease: SP}, %.3f);' % (i, dy, T["krashche"] + 0.02 * slot))
        if TOPIC[i] != "hot":
            lose.append('"#p%d"' % i)
    js_cards = []
    for i in range(4):
        js_cards.append(
            '  tl.fromTo("#p{i}", {{y: 360, autoAlpha: 0, scale: 0.92}}, {{y: 0, autoAlpha: 1, scale: 1, duration: 0.85, '
            'ease: SP}}, {t:.3f});\n'
            '  tl.fromTo("#p{i} .rf", {{scaleX: 0}}, {{scaleX: {v}, duration: 0.85, ease: "power3.out"}}, {tb:.3f});'
            .format(i=i, t=T["bachyt"] - 0.02 + i * 0.12, v=REACH[i], tb=T["stat"] + i * 0.08))
    return js("""
  G.irisOpen("#gT1", @t_open, 855, 320, 0.8);
  drift1("#gT1", @t_open, @t_close-@t_open+0.5);
  gsap.set("#gT1 .post .chp", {autoAlpha: 0});
  gsap.set("#gT1 .post .hkm", {scaleX: 0});
  gsap.set("#gT1 .post .ub", {autoAlpha: 0});
{{cards}}
  tl.fromTo("#gT1 .post .ey", {scale: 0.4, autoAlpha: 0}, {scale: 1, autoAlpha: 1, duration: 0.5, ease: POP, stagger: 0.08}, @stat-0.12);
  /* «які теми» — topic chips */
  tl.fromTo("#gT1 .post .chp", {scale: 0.5, autoAlpha: 0}, {scale: 1, autoAlpha: 1, duration: 0.55, ease: POP, stagger: 0.08}, @temy1-0.04);
  /* «які хуки» — the first line of every post gets the marker */
  tl.to("#gT1 .post .hkm", {scaleX: 1, duration: 0.36, ease: "power2.out", stagger: 0.07}, @khuky-0.02);
  /* «краще збирають охоплення» — the feed sorts itself by reach; the winners light */
  gsap.set(["#p1", "#p3"], {zIndex: 3});
{{moves}}
  tl.to([{{lose}}], {autoAlpha: 0.5, scale: 0.97, duration: 0.45, ease: "power2.out"}, @zbyr);
  tl.fromTo(["#p1 .wn", "#p3 .wn"], {autoAlpha: 0}, {autoAlpha: 1, duration: 0.3, ease: "power2.out"}, @zbyr+0.02);
  tl.fromTo("#p1 .ub", {scale: 0.3, autoAlpha: 0}, {scale: 1, autoAlpha: 1, duration: 0.55, ease: POP}, @zbyr+0.12);
  tl.fromTo("#p3 .ub", {scale: 0.3, autoAlpha: 0}, {scale: 1, autoAlpha: 1, duration: 0.55, ease: POP}, @zbyr+0.22);
  shn("#p1 .sheen", @zbyr+0.1);
  G.irisClose("#gT1", @t_close, 230, 360, 0.5);""", t_open=t_open, t_close=t_close).replace(
        "{{cards}}", "\n".join(js_cards)).replace("{{moves}}", "\n".join(moves)).replace(
        "{{lose}}", ", ".join(lose))


# ===========================================================================
# C · near: the copywriter skill plugs into Claude, her posts go into it
SKX, SKY, SKW, SKH = 420, 200, 530, 320
MP_DY = [-150, 0, 150]


def skill_card(sid, x, y, w, h, small=False):
    bars = "" if small else "".join(
        '<i class="sb" style="left:34px;top:%dpx;width:%dpx"></i>' % (yy, ww)
        for yy, ww in ((166, 440), (206, 392), (246, 286)))
    return ('<div class="skl hide" id="%s" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx">'
            '<div class="tw" style="left:34px;top:%dpx;width:88px;height:88px"><div class="jelly">%s</div></div>'
            '<div class="mi" style="left:146px;top:%dpx">SKILL</div>'
            '<div class="ti" style="left:146px;top:%dpx">копірайтер</div>%s'
            '<div class="shc"><div class="sheen"></div></div></div>'
            % (sid, x, y, w, h, 34 if not small else (h - 88) // 2, stroke("pen"),
               42 if not small else h // 2 - 50, 72 if not small else h // 2 - 20, bars))


@beat
def c_skill():
    cab = ('<svg class="cab abs" width="1080" height="700" viewBox="0 0 1080 700" style="left:0;top:0">'
           '<path class="tube hide" id="sT" d="M332 360 C 360 353 390 353 418 360"/><path class="core hide" id="sC" d="M332 360 C 360 353 390 353 418 360"/>'
           '<g class="pkg"><path class="pkt" id="sP" style="opacity:0" d="M418 360 C 390 353 360 353 332 360"/></g></svg>')
    mps = "".join(
        '<div class="mp hide" id="mp%d" style="left:%dpx;top:%dpx"><i class="av-img" style="left:16px;top:16px;width:40px;height:40px"></i>'
        '<i style="left:66px;top:24px;width:80px;height:12px;border-radius:6px;background:rgba(23,20,28,0.7)"></i>'
        '<i style="left:16px;top:70px;width:136px;height:12px;border-radius:6px;background:rgba(23,20,28,0.18)"></i></div>'
        % (i, SKX + SKW // 2 - 85, SKY + SKH // 2 - 55) for i in range(3))
    av = ('<div class="tw circ hide" id="sklAv" style="left:%dpx;top:%dpx;width:76px;height:76px">'
          '<div class="av-img" style="position:absolute;inset:0;box-shadow:0 0 0 4px #fff,0 10px 20px -8px rgba(24,4,12,0.5)">'
          '</div></div>' % (SKX + SKW - 34 - 76, SKY + 34))
    L.append('<div class="g full" id="gC">'
             '<div class="shelf edge hide" id="shC" style="left:70px;top:150px;width:940px;height:420px"></div>'
             + cab + tile("cCl", 200, 132, 260, "jelly", g.mark("claude"))
             + skill_card("skl", SKX, SKY, SKW, SKH) + av + mps + '</div>')
    sfx("whoosh-short", T["okhopl2e"] - 0.06, -3)
    sfx("pop", T["stavysh"] + 0.2)
    sfx("whoosh-short", T["navch"] + 0.02, -4)
    t_on = T["okhopl2e"] - 0.08
    t_off = T["para"] - 0.1 + 0.85
    mp_js = []
    for i in range(3):
        t = T["navch"] + i * 0.2
        mp_js.append(
            '  tl.fromTo("#mp{i}", {{x: 470, y: {dy}, scale: 1, autoAlpha: 0}}, {{autoAlpha: 1, duration: 0.14}}, {t:.3f});\n'
            '  tl.to("#mp{i}", {{x: 0, y: 0, scale: 0.15, duration: 0.5, ease: "power2.in"}}, {t:.3f});\n'
            '  tl.set("#mp{i}", {{autoAlpha: 0}}, {te:.3f}); G.bump("#skl", {te:.3f});'
            .format(i=i, dy=MP_DY[i], t=t, te=t + 0.5))
    return win("gC", t_on, t_off) + "\n" + js("""
  arr("#shC", @a-0.1, {s: 0.88, y: 30, d: 0.8});
  arr("#cCl", @a-0.02, {s: 0.4, y: 30}); G.ripple("#cClR", @a+0.3);
  /* «ставиш скіл копірайтера» — the skill slides in and plugs into Claude */
  arr("#skl", @stavysh+0.18, {s: 0.62, x: 170, y: 0, d: 0.85});
  shn("#skl .sheen", @skil+0.2);
  tl.set(["#sT", "#sC"], {autoAlpha: 1}, @skil+0.25);
  draw2("sT", @skil+0.25, 0.35); draw2("sC", @skil+0.25, 0.35);
  G.packet("sP", @kopire-0.1, 0.35); G.bump("#cCl", @kopire+0.2);
  /* «навчений писати» — her posts go into it */
{{mps}}
  /* «в твоєму стилі» — her face on it, its lines turn hers */
  arr("#sklAv", @tvoiemu-0.04, {s: 0.3, y: 0, d: 0.6});
  tl.to("#skl .sb", {backgroundColor: "rgba(255,110,156,0.62)", duration: 0.35, stagger: 0.07}, @tvoiemu+0.12);
  /* «ця пара» — they snap together */
  tl.to("#cCl", {x: 34, duration: 0.5, ease: SP}, @tsia-0.05);
  tl.to(["#skl", "#sklAv"], {x: -24, duration: 0.5, ease: SP}, @tsia-0.05);
  G.bump("#cCl", @tsia+0.25); G.bump("#skl", @tsia+0.3);""").replace("{{mps}}", "\n".join(mp_js))


# ===========================================================================
# TK2 · the iris opens out of the pair: new posts, a reply, the winning topic
@beat
def t2_generate():
    cab = ('<svg class="cab abs" width="1080" height="400" viewBox="0 0 1080 400" style="left:0;top:0">'
           '<path class="tube hide" id="pT" d="M352 220 C 394 212 436 212 478 220"/><path class="core hide" id="pC" d="M352 220 C 394 212 436 212 478 220"/>'
           '<g class="pkg"><path class="pkt" id="pP" style="opacity:0" d="M352 220 C 394 212 436 212 478 220"/></g></svg>')
    posts = (post("n0", 80, 380, 640, 520, "hot", hide=True, badge=True)
             + post("n1", 80, 650, 580, 600, "hot", hide=True, badge=True))
    cm = ('<div class="cmc hide" id="cm" style="left:80px;top:930px;width:920px;height:280px">'
          '<div class="tw gav" style="left:34px;top:30px;width:64px;height:64px">%s</div>'
          '<i class="bk" style="left:120px;top:36px;width:150px;height:20px"></i>'
          '<i class="br" style="left:120px;top:70px;width:440px;height:18px"></i>'
          '<i class="br" style="left:582px;top:70px;width:150px;height:18px"></i>'
          '<svg style="position:absolute;right:40px;top:34px;width:48px;height:48px" viewBox="0 0 24 24">'
          '<path d="%s" fill="none" stroke="rgba(23,20,28,0.5)" stroke-width="1.8"/></svg>'
          '<div id="cmR" style="position:absolute;left:0;top:0;width:920px;height:280px">'
          '<i style="left:62px;top:110px;width:6px;height:120px;border-radius:3px;background:rgba(23,20,28,0.08)"></i>'
          '<i class="av-img" style="left:110px;top:140px;width:60px;height:60px"></i>'
          '<div class="tw circ" style="left:150px;top:180px;width:34px;height:34px"><div class="jelly">%s</div></div>'
          '<i class="bk" style="left:192px;top:144px;width:130px;height:20px"></i>'
          '<i class="bp" id="rb0" style="left:192px;top:180px;width:560px;height:18px"></i>'
          '<i class="bp" id="rb1" style="left:192px;top:210px;width:380px;height:18px"></i>'
          '</div></div>' % (PERSON, HEART, stroke("pen")))
    L.append('<div class="g full" id="gT2">' + tkground() + cab
             + tile("tCl", 200, 150, 120, "jelly", g.mark("claude"))
             + skill_card("tSk", 480, 120, 450, 200, small=True)
             + posts + cm + '</div>')
    sfx("whoosh-short", T["para"] - 0.1)
    sfx("typing", T["heneruie"] + 0.25, -3)
    sfx("pop", T["vidpov"] - 0.02, -2)
    sfx("click", T["temy2"] - 0.24)
    t_open, t_close = T["para"] - 0.1, T["utebee"] - 0.15
    WINDOWS.append(("gT2", t_open, t_close + 0.52))
    return js("""
  G.irisOpen("#gT2", @t_open, 380, 360, 0.8);
  drift1("#gT2", @t_open, @t_close-@t_open+0.5);
  gsap.set(["#n0 .chp", "#n1 .chp", "#n0 .ub", "#n1 .ub", "#n0 .ey", "#n1 .ey", "#n0 .rt", "#n1 .rt"], {autoAlpha: 0});
  gsap.set(["#n0 .rf", "#n1 .rf"], {scaleX: 0});
  gsap.set(["#n0 .hkm", "#n1 .hkm"], {scaleX: 0});
  arr("#tCl", @t_open+0.08, {s: 0.5, y: 30, d: 0.8});
  arr("#tSk", @t_open+0.18, {s: 0.6, y: 30, d: 0.8});
  tl.set(["#pT", "#pC"], {autoAlpha: 1}, @t_open+0.4);
  draw2("pT", @t_open+0.4, 0.35); draw2("pC", @t_open+0.4, 0.35);
  /* «сама генерує тобі і нові пости» — two posts are written out of the pair */
  gsap.set(["#n0", "#n1"], {transformOrigin: "50% 0%"});
  tl.fromTo("#n0", {y: -230, scale: 0.4, autoAlpha: 0}, {y: 0, scale: 1, autoAlpha: 1, duration: 0.8, ease: SP}, @heneruie-0.06);
  tl.fromTo("#n0 .hk", {scaleX: 0}, {scaleX: 1, duration: 0.45, ease: "power1.inOut"}, @heneruie+0.28);
  tl.fromTo("#n0 .bd", {scaleX: 0}, {scaleX: 1, duration: 0.45, ease: "power1.inOut"}, @heneruie+0.62);
  G.packet("pP", @heneruie-0.1, 0.3);
  tl.fromTo("#n1", {y: -500, scale: 0.4, autoAlpha: 0}, {y: 0, scale: 1, autoAlpha: 1, duration: 0.8, ease: SP}, @novi-0.08);
  tl.fromTo("#n1 .hk", {scaleX: 0}, {scaleX: 1, duration: 0.45, ease: "power1.inOut"}, @novi+0.22);
  tl.fromTo("#n1 .bd", {scaleX: 0}, {scaleX: 1, duration: 0.45, ease: "power1.inOut"}, @novi+0.52);
  /* «і відповіді на коменти» — a comment, and the reply comes back */
  arr("#cm", @vidpov-0.06, {s: 0.8, y: 40, d: 0.8});
  tl.fromTo("#cmR", {autoAlpha: 0, x: -24}, {autoAlpha: 1, x: 0, duration: 0.5, ease: SP}, @komenty-0.2);
  tl.fromTo(["#rb0", "#rb1"], {scaleX: 0}, {scaleX: 1, duration: 0.4, ease: "power1.inOut", stagger: 0.18}, @komenty-0.05);
  /* «вже під ті теми» — the winning topic stamps onto both */
  tl.fromTo("#n0 .chp", {scale: 1.9, autoAlpha: 0}, {scale: 1, autoAlpha: 1, duration: 0.5, ease: POP}, @temy2-0.26);
  tl.fromTo("#n1 .chp", {scale: 1.9, autoAlpha: 0}, {scale: 1, autoAlpha: 1, duration: 0.5, ease: POP}, @temy2-0.06);
  tl.to(["#n0 .hkm", "#n1 .hkm"], {scaleX: 1, duration: 0.36, ease: "power2.out", stagger: 0.1}, @temy2+0.2);
  /* «які реально працюють» — and their reach climbs */
  tl.to(["#n0 .ey", "#n1 .ey", "#n0 .rt", "#n1 .rt"], {autoAlpha: 1, duration: 0.25}, @realno-0.1);
  tl.to("#n0 .rf", {scaleX: 0.9, duration: 0.8, ease: "power3.out"}, @realno);
  tl.to("#n1 .rf", {scaleX: 0.84, duration: 0.8, ease: "power3.out"}, @realno+0.1);
  tl.fromTo("#n0 .ub", {scale: 0.3, autoAlpha: 0}, {scale: 1, autoAlpha: 1, duration: 0.55, ease: POP}, @pratsiuiut2);
  tl.fromTo("#n1 .ub", {scale: 0.3, autoAlpha: 0}, {scale: 1, autoAlpha: 1, duration: 0.55, ease: POP}, @pratsiuiut2+0.1);
  G.irisClose("#gT2", @t_close, 540, 360, 0.5);""", t_open=t_open, t_close=t_close)


# ===========================================================================
# D · near: her own Threads inside a boundary; the rest of Threads outside
PX, PY, PW, PH = 390, 150, 300, 420
BND = (350, 118, 380, 484, 64)        # x, y, w, h, r
OTHERS = [(x, y) for y in (130, 290, 450) for x in (80, 210, 760, 890)]


def rrect(x, y, w, h, r):
    return ("M%d %d H%d A%d %d 0 0 1 %d %d V%d A%d %d 0 0 1 %d %d H%d A%d %d 0 0 1 %d %d V%d A%d %d 0 0 1 %d %d Z"
            % (x + r, y, x + w - r, r, r, x + w, y + r, y + h - r, r, r, x + w - r, y + h, x + r, r, r, x, y + h - r,
               y + r, r, r, x + r, y))


@beat
def d_limit():
    grid = ""
    for row in range(2):
        for col in range(3):
            grid += ('<i class="gt" style="left:%dpx;top:%dpx;width:72px;height:72px"><span class="gtl"></span></i>'
                     % (34 + col * 81, 220 + row * 81))
    prof = ('<div class="prof hide" id="prof" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx">'
            '<i class="av-img" style="left:102px;top:30px;width:96px;height:96px"></i>'
            '<i style="left:75px;top:142px;width:150px;height:20px;border-radius:10px;background:rgba(23,20,28,0.78)"></i>'
            '<i style="left:100px;top:174px;width:100px;height:14px;border-radius:7px;background:rgba(23,20,28,0.22)"></i>'
            '<div style="position:absolute;right:22px;top:22px;width:36px;height:36px">%s</div>'
            '%s<i id="scan"></i></div>' % (PX, PY, PW, PH, g.mark("threads", "pm"), grid))
    ring = ('<div class="sqring rc" id="profR" style="left:%dpx;top:%dpx;width:96px;height:96px"></div>'
            % (PX + 102, PY + 30))
    others = "".join(
        '<div class="oc hide" id="oc%d" style="left:%dpx;top:%dpx">'
        '<i class="gav" style="left:14px;top:14px;width:36px;height:36px"></i>'
        '<i style="left:58px;top:22px;width:40px;height:10px;border-radius:5px;background:rgba(255,255,255,0.6)"></i>'
        '<i style="left:14px;top:66px;width:84px;height:10px;border-radius:5px;background:rgba(255,255,255,0.4)"></i>'
        '<i style="left:14px;top:88px;width:60px;height:10px;border-radius:5px;background:rgba(255,255,255,0.4)"></i>'
        '</div>' % (n, x, y) for n, (x, y) in enumerate(OTHERS))
    bnd = ('<svg class="abs" width="1080" height="700" viewBox="0 0 1080 700" style="left:0;top:0;overflow:visible">'
           '<path class="bnd hide" id="bnd" d="%s"/></svg>' % rrect(*BND))
    L.append('<div class="g full" id="gD">'
             '<div class="shelf edge hide" id="shD" style="left:60px;top:100px;width:960px;height:540px"></div>'
             + others + prof + ring + bnd
             + tile("mag", 110, 560, 480, "jelly", stroke("search"), extra_cls="circ", ring=False)
             + '</div>')
    sfx("whoosh-short", T["utebee"] - 0.15, -3)
    sfx("click-soft", T["mezha"] - 0.03, -2)
    sfx("click", T["zovni"] + 0.33, -1)
    # the order the others appear in: nearest to the boundary first
    order = sorted(range(len(OTHERS)), key=lambda n: abs(OTHERS[n][0] + 56 - 540))
    t_on = T["utebee"] - 0.2
    t_off = T["zapusk"] + 0.25
    return win("gD", t_on, t_off) + "\n" + js("""
  arr("#shD", @ale-0.12, {s: 0.9, y: 30, d: 0.8});
  arr("#prof", @ale-0.02, {s: 0.6, y: 30, d: 0.8});
  /* «є межа» — the boundary draws round her own Threads */
  tl.set("#bnd", {autoAlpha: 1}, @mezha-0.06);
  draw2("bnd", @mezha-0.06, 0.6);
  /* «це аналізує тільки твій власний тредс» — the scan stays inside */
  tl.fromTo("#scan", {autoAlpha: 0, y: 0}, {autoAlpha: 1, duration: 0.15}, @analizuie-0.05);
  tl.to("#scan", {y: 176, duration: 0.85, ease: "power1.inOut"}, @analizuie-0.05);
  tl.to("#scan", {autoAlpha: 0, duration: 0.2}, @analizuie+0.8);
  tl.to("#prof .gtl", {autoAlpha: 1, duration: 0.25, stagger: 0.12}, @analizuie+0.05);
  G.bump("#prof", @tilky+0.05); G.ripple("#profR", @tilky+0.1);
  tl.fromTo("#bnd", {strokeWidth: 8}, {strokeWidth: 13, duration: 0.2, yoyo: true, repeat: 1, immediateRender: false}, @vlasnyi);
  /* «шукав нові теми зовні, по всьому Threads» — the rest of Threads, out of reach */
  arr("#mag", @shukav-0.06, {s: 0.4, y: 20, d: 0.7});
  {{others}}
  tl.to("#mag", {x: 72, duration: 0.33, ease: "power2.in"}, @zovni);
  tl.to("#mag", {x: 18, duration: 0.6, ease: SP}, @zovni+0.33);
  tl.to("#bnd", {stroke: "#ffffff", duration: 0.08}, @zovni+0.33);
  tl.to("#bnd", {stroke: "#ff6e9c", duration: 0.4}, @zovni+0.45);
  tl.to(".oc", {y: -8, duration: 0.2, ease: "power2.out", stagger: 0.03, yoyo: true, repeat: 1}, @vsiomu);
  /* «запускати окремий аналіз» — everything clears for the browser */
  bout(["#shD", "#prof", "#bnd", ".oc"], @zapusk-0.1, 10, 0.3);
  tl.to("#mag", {scale: 2.2, autoAlpha: 0, duration: 0.3, ease: "power2.in"}, @zapusk-0.1);""").replace(
        "{{others}}", "\n  ".join(
            'tl.fromTo("#oc%d", {autoAlpha: 0, scale: 0.5}, {autoAlpha: 0.75, scale: 1, duration: 0.5, ease: POP}, %.3f);'
            % (n, T["novi2"] - 0.1 + k_ * 0.06) for k_, n in enumerate(order)))


# ===========================================================================
# E · near: Claude's in-app browser; it crawls, stalls, fails
@beat
def e_browser():
    skel = ""
    for n, (x, y) in enumerate(((40, 130), (466, 130), (40, 310), (466, 310))):
        skel += ('<div class="skc" style="left:%dpx;top:%dpx"><i style="left:24px;top:24px;width:44px;height:44px;border-radius:50%%"></i>'
                 '<i style="left:84px;top:34px;width:160px;height:14px"></i>'
                 '<i style="left:24px;top:92px;width:330px;height:14px"></i><i style="left:24px;top:120px;width:220px;height:14px"></i></div>'
                 % (x, y))
    L.append('<div class="g full" id="gE">'
             '<div class="dglass edge hide" id="br" style="left:90px;top:120px;width:900px;height:500px;border-radius:52px">'
             '<div class="dot" style="left:40px"></div><div class="dot" style="left:68px"></div><div class="dot" style="left:96px"></div>'
             '<div id="url">%s<div id="urlT">threads.com</div></div>'
             '<div class="tw" style="right:26px;top:16px;left:auto;width:62px;height:62px"><div class="jelly">%s</div></div>'
             '<div id="prgT"></div><div id="prg"></div>%s'
             '<svg class="spn hide" id="spn" viewBox="0 0 170 170" width="170" height="170" style="left:365px;top:225px">'
             '<circle cx="85" cy="85" r="70"/></svg>'
             '%s'
             '</div></div>' % (stroke("lock"), g.mark("claude"), skel,
                              tile("warn", 150, 375, 235, "jelly", stroke("alert"), extra_cls="circ", ring=False)))
    sfx("pop", T["zapusk"] - 0.06)
    sfx("typing", T["vnutr"] + 0.02, -3)
    sfx("click", T["pohano"] + 0.06)
    t_on = T["zapusk"] - 0.12
    t_off = T["chesnoe"] + 0.08
    return win("gE", t_on, t_off) + "\n" + js("""
  gsap.set("#br", {transformOrigin: "62% 76%"});
  arr("#br", @zapusk-0.08, {s: 0.3, y: 0, d: 0.9});
  gsap.set("#prg", {scaleX: 0});
  gsap.set("#urlT", {clipPath: "inset(0px 100% 0px 0px)"});
  /* «окремий аналіз» — the page skeleton */
  tl.fromTo("#br .skc", {autoAlpha: 0, y: 24}, {autoAlpha: 1, y: 0, duration: 0.45, ease: SP, stagger: 0.08}, @okremyi-0.05);
  /* «через внутрішній браузер» — the address types */
  tl.to("#urlT", {clipPath: "inset(0px 0% 0px 0px)", duration: 0.75, ease: "steps(11)"}, @vnutr+0.02);
  /* «і поки що це працює…» — it crawls */
  tl.to("#prg", {scaleX: 0.2, duration: 0.3, ease: "power2.out"}, @brauzere-0.1);
  tl.to("#prg", {scaleX: 0.31, duration: 1.1, ease: "power1.out"}, @poky);
  tl.fromTo("#spn", {autoAlpha: 0, rotation: 0, transformOrigin: "50% 50%"}, {autoAlpha: 1, duration: 0.25}, @brauzere-0.2);
  tl.to("#spn", {rotation: 420, duration: {{spd}}, ease: "power1.out"}, @brauzere-0.2);
  tl.to("#spn", {rotation: 440, duration: 0.2, ease: "steps(2)"}, @pohano-0.25);
  tl.to(["#br .skc", "#prg"], {autoAlpha: 0.35, duration: 0.4}, @pohano);
  /* «погано» — it stops dead */
  tl.to("#spn", {autoAlpha: 0, scale: 0.6, duration: 0.18, ease: "power2.in"}, @pohano+0.02);
  arr("#warn", @pohano+0.04, {s: 0.3, y: 0, d: 0.6});
  G.haptic("#br", @pohano+0.2);
  bout("#br", @chesnoe-0.26, 10, 0.3);""").replace("{{spd}}", "%.3f" % (T["pohano"] - T["brauzere"] - 0.1))


# ===========================================================================
# F1 · «сама власниця агенції» -> «таку систему під тебе»
ROW = [("threads", "pearl"), ("w", "pearl"), ("claude", "jelly"), ("pen", "pearl")]
ROW_X = [120, 300, 480, 660]
ROW_Y = 440
TEAM_X = [200, 485, 770]


@beat
def f1_agency():
    row = ""
    for i, ((name, mat), x) in enumerate(zip(ROW, ROW_X)):
        inner = wmark(78) if name == "w" else stroke("pen") if name == "pen" else g.mark(name)
        row += tile("r%d" % i, 120, x, ROW_Y, mat, inner, ring=False)
    lines = "".join('<path class="tube hide" id="tl%d" d="M540 312 C 540 380 %d 360 %d 430"/>'
                    '<path class="core hide" id="tc%d" d="M540 312 C 540 380 %d 360 %d 430"/>'
                    % (i, x + 55, x + 55, i, x + 55, x + 55) for i, x in enumerate(TEAM_X))
    cab = ('<svg class="cab abs" width="1080" height="700" viewBox="0 0 1080 700" style="left:0;top:0">%s'
           '<path class="tube hide" id="rT" d="M180 500 C 420 494 660 494 900 500"/><path class="core hide" id="rC" d="M180 500 C 420 494 660 494 900 500"/>'
           '<g class="pkg"><path class="pkt" id="rP" style="opacity:0" d="M180 500 C 420 494 660 494 900 500"/></g></svg>' % lines)
    team = "".join(tile("tm%d" % i, 110, x, 430, "pearl", PERSON, extra_cls="circ", ring=False)
                   for i, x in enumerate(TEAM_X))
    slot = ('<div class="tw hide" id="oslot" style="left:840px;top:%dpx;width:120px;height:120px">'
            '<div class="slotf" style="border-radius:50%%;font-size:0"></div></div>' % ROW_Y)
    L.append('<div class="g full" id="gF1">'
             '<div class="shelf edge hide" id="shF" style="left:70px;top:400px;width:940px;height:200px"></div>'
             + cab + team + row + slot
             + tile("own", 160, 460, 150, "jelly", PERSON, extra_cls="circ")
             + '</div>')
    sfx("pop", T["sama"] - 0.04, -2)
    sfx("pop", T["systemu"] - 0.2, -3)
    t_on, t_off = T["sama"] - 0.15, T["napyshy"] + 0.08
    ox = 840 + 60 - (460 + 80)
    oy = ROW_Y + 60 - (150 + 80)
    return win("gF1", t_on, t_off) + "\n" + js("""
  /* «сама власниця агенції» — the owner, then her team */
  arr("#own", @sama-0.06, {s: 0.4, y: 30, d: 0.8}); G.ripple("#ownR", @sama+0.3);
  [0, 1, 2].forEach(function (i) {
    tl.set(["#tl" + i, "#tc" + i], {autoAlpha: 1}, @ahentsii-0.08 + i * 0.08);
    draw2("tl" + i, @ahentsii-0.08 + i * 0.08, 0.4); draw2("tc" + i, @ahentsii-0.08 + i * 0.08, 0.4);
    arr("#tm" + i, @ahentsii+0.18 + i * 0.1, {s: 0.3, y: 20, d: 0.7});
  });
  /* «хочеш таку систему» — the team folds away; the system lands where it stood */
  tl.to(["#tl0", "#tc0", "#tl1", "#tc1", "#tl2", "#tc2"], {autoAlpha: 0, duration: 0.25}, @khochesh-0.05);
  [0, 1, 2].forEach(function (i) {
    tl.to("#tm" + i, {x: (540 - 55 - [{{tx}}][i]) * 0.6, y: -120, scale: 0.2, autoAlpha: 0, duration: 0.36, ease: "power2.in"}, @khochesh-0.05);
  });
  arr("#shF", @khochesh+0.12, {s: 0.9, y: 20, d: 0.7});
  [0, 1, 2, 3].forEach(function (i) { arr("#r" + i, @systemu-0.22 + i * 0.08, {s: 0.4, y: 20, d: 0.7}); });
  arr("#oslot", @systemu+0.1, {s: 0.5, y: 0, d: 0.6});
  tl.set(["#rT", "#rC"], {autoAlpha: 1}, @systemu+0.15);
  draw2("rT", @systemu+0.15, 0.5); draw2("rC", @systemu+0.15, 0.5);
  /* «під тебе» — the owner docks into the last slot */
  tl.to("#own", {x: {{ox}}, y: {{oy}}, scale: 0.75, duration: 0.75, ease: SP}, @tebe-0.32);
  tl.set("#oslot", {autoAlpha: 0}, @tebe+0.1);
  G.packet("rP", @tebe+0.05, 0.45);
  bout(["#shF", "#own", "#r0", "#r1", "#r2", "#r3", "#rT", "#rC"], @napyshy-0.22, 10, 0.28);""").replace(
        "{{tx}}", ", ".join(str(x) for x in TEAM_X)).replace("{{ox}}", str(ox)).replace("{{oy}}", str(oy))


# ===========================================================================
# F2 · the comment: «+» typed, posted, her reply comes back, liked
@beat
def f2_comment():
    L.append(
        '<div class="g full" id="gF2">'
        '<div class="dglass edge hide" id="cmPost" style="left:70px;top:188px;width:940px;height:152px">'
        '<div class="cx gav cmav" style="left:26px;top:36px">%(person)s</div>'
        '<div class="cx" id="cpUser">ти<span>щойно</span></div>'
        '<div class="cx" id="cpTxt">+</div>'
        '<div class="cx" id="cpHeart"><svg viewBox="0 0 24 24"><path class="o" d="%(heart)s"/></svg>'
        '<svg viewBox="0 0 24 24" id="cpFill"><path class="fl" d="%(heart)s"/></svg></div>'
        '</div>'
        '<div class="dglass edge hide" id="cmBox" style="left:70px;top:372px;width:940px;height:128px">'
        '<div class="cx gav cmav" style="left:24px;top:24px">%(person)s</div>'
        '<div class="cx" id="cmPh">Додайте коментар…</div>'
        '<div class="cx hide" id="cmTyped">+</div>'
        '<div class="cx hide" id="cmCaret"></div>'
        '<div class="cx" id="cmSend">Опублікувати</div>'
        '</div>'
        '<div class="dglass edge hide" id="cmRp" style="left:170px;top:372px;width:840px;height:150px">'
        '<div class="cx av-img" style="left:26px;top:35px;width:80px;height:80px"></div>'
        '<div class="cx" id="rpUser">Рута<span>автор</span></div>'
        '<i class="rpb" id="rp0" style="left:128px;top:78px;width:560px"></i>'
        '<i class="rpb" id="rp1" style="left:128px;top:108px;width:380px"></i>'
        '</div></div>' % {"person": PERSON, "heart": HEART})
    sfx("click", T["plius"] + 0.01)
    sfx("pop", T["komentar"] + 0.18, -3)
    sfx("pop", T["rozkazhu"] + 0.02, -3)
    t_on, t_off = T["napyshy"] - 0.12, T["ashche"] - 0.08
    return win("gF2", t_on, t_off) + "\n" + js("""
  gsap.set("#cpFill", {scale: 0, autoAlpha: 0, transformOrigin: "50% 60%"});
  gsap.set("#cmSend", {autoAlpha: 0.4});
  arr("#cmBox", @napyshy-0.1, {s: 0.7, y: 40, d: 0.8});
  tl.set("#cmCaret", {autoAlpha: 1}, @napyshy+0.25);
  tl.set("#cmPh", {autoAlpha: 0}, @napyshy+0.25);
  /* «плюс» */
  tl.fromTo("#cmTyped", {autoAlpha: 0, scale: 0.4, transformOrigin: "20% 50%"},
            {autoAlpha: 1, scale: 1, duration: 0.3, ease: POP}, @plius);
  tl.to("#cmCaret", {x: 46, duration: 0.06}, @plius);
  tl.to("#cmSend", {autoAlpha: 1, duration: 0.12}, @plius);
  /* «у коментарях» — sent; it posts above */
  G.bump("#cmSend", @komentar);
  tl.set(["#cmTyped", "#cmCaret"], {autoAlpha: 0}, @komentar+0.16);
  tl.set("#cmPh", {autoAlpha: 1}, @komentar+0.16);
  tl.to("#cmSend", {autoAlpha: 0.4, duration: 0.2}, @komentar+0.16);
  bin("#cmPost", @komentar+0.16, 10, 0.3);
  tl.fromTo("#cmPost", {y: 150, scale: 0.9}, {y: 0, scale: 1, duration: 0.8, ease: SP}, @komentar+0.16);
  /* «і я розкажу» — her reply comes back under it */
  bout("#cmBox", @rozkazhu-0.24, 10, 0.24);
  arr("#cmRp", @rozkazhu-0.02, {s: 0.8, y: 40, d: 0.8});
  tl.fromTo(["#rp0", "#rp1"], {scaleX: 0}, {scaleX: 1, duration: 0.5, ease: "power1.inOut", stagger: 0.3}, @nalasht-0.05);
  /* «саме тобі» — and she likes your comment */
  tl.to("#cpFill", {scale: 1, autoAlpha: 1, duration: 0.5, ease: POP}, @same2-0.05);
  bout(["#cmPost", "#cmRp"], @ashche-0.24, 10, 0.24);""")


# ===========================================================================
# F3 · Стежити
@beat
def f3_follow():
    L.append('<div class="g full" id="gF3"><div class="fl hide" id="fl" style="left:190px;top:300px;width:700px;height:150px">'
             '<div class="tw circ" style="left:28px;top:27px;width:96px;height:96px"><div class="jelly">%s</div></div>'
             '<div class="t" id="flT">Стежити</div>'
             '<div class="on" id="flOn"><div class="tw circ" style="left:28px;top:27px;width:96px;height:96px">'
             '<div class="pearl">%s</div></div><div class="t">Ви стежите</div></div>'
             '<div class="ck" id="ck4" style="left:470px;top:75px"></div>'
             '<div class="shc"><div class="sheen"></div></div></div></div>'
             % (g.mark("instagram"), stroke("check")))
    sfx("click", T["pidpysh"] + 0.06)
    return win("gF3", T["ashche"] - 0.22, DUR + 0.5) + "\n" + js("""
  arr("#fl", @ashche-0.2, {s: 0.6, y: 40, d: 0.4});
  tl.to("#fl", {scale: 0.95, duration: 0.09, ease: "power2.out"}, @pidpysh+0.06);
  tl.to("#fl", {scale: 1, duration: 0.45, ease: SP}, @pidpysh+0.15);
  tl.fromTo("#flOn", {autoAlpha: 0}, {autoAlpha: 1, duration: 0.2}, @pidpysh+0.1);
  tl.set("#flT", {autoAlpha: 0}, @pidpysh+0.11);
  tl.fromTo("#ck4", {scale: 0.3, autoAlpha: 0.95}, {scale: 2.4, autoAlpha: 0, duration: 0.7, ease: "power2.out", immediateRender: false}, @pidpysh+0.08);
  shn("#fl .sheen", @pidpysh+0.2);""")


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
    span_words(T["chy"], T["pratsiuiut1e"]),            # her DM screenshot shows the question
    span_words(T["ruta"], T["prodiue"]),                 # the capsule: «Рута · технічна продюсерка»
    span_words(T["skil"], T["kopire"]),                  # the skill card: «SKILL · копірайтер»
    span_words(T["plius"], T["pliuse"]),                 # the comment box types «+»
]


def check_no_paint():
    """No group may be on screen inside a closeup."""
    for gid, a, b in WINDOWS:
        for na, nb in NO_PAINT:
            assert b <= na + 1e-3 or a >= nb - 1e-3, "%s %.3f-%.3f paints over the closeup %.3f-%.3f" % (gid, a, b, na, nb)


def main():
    gj = []
    for fn in BEATS:
        j = fn()
        gj.append("  /* %s */" % fn.__name__)
        gj.append(j.rstrip())
    check_no_paint()
    push = ["#vid"]
    head = [g.js(), HEAD_JS,
            '  gsap.set(%s, {transformOrigin: "540px 900px"});' % json.dumps(push),
            '  tl.fromTo(%s, {scale: 1}, {scale: 1.045, duration: %.3f, ease: "none"}, 0);' % (json.dumps(push), DUR)]
    extra = ('<linearGradient id="gHeart" x1="0" y1="0" x2="0" y2="1">'
             '<stop offset="0" stop-color="#ff6e9c"/><stop offset="1" stop-color="#c4143a"/></linearGradient>')
    doc = k.document(
        title=u"Reel 27 — Claude + Threads",
        plate="assets/base.mp4",
        gfx_html=g.defs(extra) + "\n" + "\n".join(L),
        gfx_js="\n".join(head + gj),
        caps=CAPS,
        blackout=BLACKOUT,
    )
    io.open(os.path.join(HERE, "index.html"), "w", encoding="utf-8").write(doc)
    SFX.sort(key=lambda c: c["t"])
    io.open(os.path.join(HERE, "sfx.json"), "w", encoding="utf-8").write(json.dumps(SFX, indent=1))
    print("index.html  %d captions, %d beats, %d sfx cues (%.2f/s)" % (len(CAPS), len(BEATS), len(SFX), len(SFX) / DUR))


main()
