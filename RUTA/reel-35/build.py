# -*- coding: utf-8 -*-
"""Reel 35 — «А мене не заблокують?». Posts 2026-10-14.

The one object is **the padlock on her Instagram**: the fear of it, the ban
that really hits bots, the official door (Meta API) that opens it, the
chatbots that live behind that door, and the one time the account really did
get wary.

Chain:  near: Instagram, «?» bubbles, a padlock drops on it -> Claude lands, a
dashed «?» link -> the link becomes a cable, the «?» becomes Windsor, a post
travels Claude -> Windsor -> Instagram; the ban ring slams on «забанить» ->
OVER: the iris opens out of the ban ring: a bot puts on a human face and
clicks the buttons of an Instagram screen; the ban ring lands on the bot ->
the iris closes onto the Meta API hub -> near: Metricool and Windsor plug into
it, an «official» seal, the post flows through to Instagram, its padlock
opens -> OVER: the iris opens out of the open lock: an Instagram chat where
the robot (legit now) replies; it is plugged into the Meta API plate, a seal,
a padlock tries to drop and is struck through -> the iris closes onto «1» ->
near: Instagram gets a «!»; a calendar, one day lit; «Тип акаунта» switch
flips; Claude, Windsor, Meta plug in -> all of it pours into that one day,
the day overflows -> Instagram, wary («!») -> Стежити.

usage: python build.py   (then: python ../tools/sfx.py mix 35)
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

CUT = json.load(io.open(os.path.join(ROOT, "work", "r35", "cut.json"), encoding="utf-8"))
DUR = 45.016           # (1351 plate frames - 0.5) / 30, floored
FPS = 30
k = Kit(width=1080, height=1920, fps=FPS, duration=DUR)
g = Glass(["instagram", "claude", "meta"])
k.css(g.css())

# NO-PAINT: closeups from tools/cut.py. This cut has none.
NO_PAINT = [tuple(x) for x in CUT["no_paint"]]

CAPS = k.load_captions(os.path.join(ROOT, "work", "r35", "captions.json"))
# whisper errors in the "she improvised" list: the brand, the pronoun, and a
# doubled «і» (she said «одразу змінила і тип акаунта»)
FIX = {u"Wincer,": u"Windsor,", u"цей Інстаграм.": u"це Інстаграм.", u"і змінила": u"змінила"}
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
    c = min(hits, key=lambda c: abs(c["s"] - near))
    assert abs(c["s"] - near) < 0.6, (word, near, c["s"])
    return c["e"]


T = {
    "naich": S(u"Найчастіше", 0.1), "pytannia": S(u"питання", 0.46), "yake": S(u"яке", 0.92),
    "pyshut": S(u"пишуть", 1.26), "zablok": S(u"заблокують", 2.08), "postyty": S(u"постити", 2.93),
    "shtuchnyi": S(u"штучний", 3.49), "intelekt": S(u"інтелект", 3.85), "idetsia": S(u"Ідеться", 4.55),
    "klod": S(u"Клод", 5.39), "konektor": S(u"конектор", 5.92), "windsor": S("Windsor", 6.71),
    "sam": S(u"сам", 7.38), "mii": S(u"мій", 8.18), "profil": S(u"профіль", 8.38),
    "zabanyt": S(u"забанить", 9.15), "insta1": S(u"Інстаграм", 9.94), "insta1e": E(u"Інстаграм", 9.94),
    "tak": S(u"Так", 10.7), "blokuiut": S(u"блокують", 11.41), "botiv": S(u"ботів", 11.97),
    "imituiut": S(u"імітують", 12.73), "liudynu": S(u"людину", 13.43), "klats": S(u"клацають", 14.05),
    "knopky": S(u"кнопки", 14.57), "interf": S(u"інтерфейсі", 15.07), "interfe": E(u"інтерфейсі", 15.07),
    "a": S(u"А", 16.01), "ofits": S(u"офіційний", 16.19), "meta": S("Meta", 16.77),
    "api": S("API", 17.17), "apie": E("API", 17.17), "cherez": S(u"через", 17.9),
    "metricool": S("Metricool", 18.68), "metricoole": E("Metricool", 18.68),
    "windsor2": S("Windsor", 19.38), "lehal": S(u"легальний", 20.34), "postyty2": S(u"постити", 21.3),
    "ne": S(u"не", 22.26), "blokuiut2": S(u"блокують", 22.6), "blokuiut2e": E(u"блокують", 22.6),
    "te": S(u"Те", 23.52), "chatbot": S(u"чатботів", 25.42), "vinsta": S(u"інстаграмі", 25.88),
    "vony": S(u"Вони", 26.44), "ofits2": S(u"офіційний", 27.42), "api2": S("API", 28.26),
    "api2e": E("API", 28.26), "apriori": S(u"апріорі", 29.26), "mozhut": S(u"можуть", 30.64),
    "zablokuv": S(u"заблокувати", 30.86), "zablokuve": E(u"заблокувати", 30.86),
    "mene": S(u"мене", 31.73), "odyn": S(u"один-єдиний", 32.42), "insta2": S(u"Інстаграм", 33.42),
    "proty": S(u"проти", 34.08), "tse2": S(u"Це", 34.64), "odnoho": S(u"одного", 35.3),
    "dnia": S(u"дня", 35.52), "odrazu": S(u"одразу", 35.78), "zminyla": S(u"змінила", 36.22),
    "typ": S(u"тип", 36.94), "akaunta": S(u"акаунта", 37.12), "akauntae": E(u"акаунта", 37.12),
    "pidkl": S(u"підключила", 37.7), "vse": S(u"все", 38.22), "nioho": S(u"нього", 38.54),
    "zabahato": S(u"Забагато", 39.1), "zmin": S(u"змін", 39.72), "raz": S(u"раз", 40.12),
    "os": S(u"ось", 40.62), "akaunt": S(u"акаунт", 41.25), "spravdi": S(u"справді", 41.75),
    "nastor": S(u"насторожитись", 42.33), "nastore": E(u"насторожитись", 42.33),
    "yakshcho": S(u"Якщо", 43.33), "korysno": S(u"корисно", 43.71), "pidpysh": S(u"підпишись", 44.21),
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
# Sound design (tools/sfx.py). Quiet, on the event.
SFX = []


def sfx(name, t, db=0):
    if isinstance(t, str):
        t = float(js(t))
    SFX.append({"t": round(max(0.0, t), 3), "name": name, "db": db})


# ---------------------------------------------------------------------------
# Glyphs
HEART = ("M12 20.6s-7.6-4.5-9.4-9.3C1.3 7.8 3.5 4.4 7 4.4c2 0 3.7 1.1 5 3 "
         "1.3-1.9 3-3 5-3 3.5 0 5.7 3.4 4.4 6.9-1.8 4.8-9.4 9.3-9.4 9.3z")
STROKES = {
    "check": '<path d="M5.4 12.6l4.3 4.3 8.9-9.5"/>',
    "person": '<circle cx="12" cy="8.2" r="3.6"/><path d="M4.8 20c.9-3.8 3.7-5.8 7.2-5.8s6.3 2 7.2 5.8"/>',
    "lock": '<rect x="5" y="10.5" width="14" height="10" rx="2.5"/><path class="shk" d="M8.2 10.5V8a3.8 3.8 0 0 1 7.6 0v2.5"/>',
    "robot": ('<rect x="4.6" y="8.2" width="14.8" height="11.4" rx="3.2"/><path d="M12 8.2V5.2"/>'
              '<circle cx="12" cy="4" r="1.2"/><circle cx="9.2" cy="13.2" r="1.25"/><circle cx="14.8" cy="13.2" r="1.25"/>'
              '<path d="M9.6 16.6h4.8M2.6 12.4v3.6M21.4 12.4v3.6"/>'),
    "heart": '<path d="%s"/>' % HEART,
    "comment": '<path d="M20.5 11.6a8.4 8.4 0 0 1-12.3 7.4L3.5 20.5l1.5-4.6A8.4 8.4 0 1 1 20.5 11.6z"/>',
    "share": '<path d="M21 3.5L10.2 13.8M21 3.5l-6.6 17-4.2-6.7-6.7-4.2z"/>',
    "back": '<path d="M15 4.5L7.5 12l7.5 7.5"/>',
}
CURSOR = ('<svg viewBox="0 0 24 24" width="64" height="64"><path d="M4.2 2.8l14.6 8.1-6.3 1.5-3.1 5.9z" '
          'fill="#fff" stroke="#17141c" stroke-width="1.6" stroke-linejoin="round"/></svg>')


def stroke(name, cls="sk"):
    return '<svg class="%s" viewBox="0 0 24 24">%s</svg>' % (cls, STROKES[name])


def wmark(size):
    """Windsor has no icon: its wordmark «w.» (style-test, reel 27)."""
    return '<span class="wmark" style="font-size:%dpx">w<i>.</i></span>' % size


def big(text, size, color="#fff"):
    return '<span class="wmark" style="font-size:%dpx;color:%s">%s</span>' % (size, color, text)


def tile(tid, size, x, y, material, inner, extra_cls="", hide=True, ring=True):
    circ = "circ" in extra_cls
    r = ('<div class="sqring%s" id="%sR" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx"></div>'
         % (" rc" if circ else "", tid, x, y, size, size)) if ring else ""
    return ('%s<div class="tw%s %s" id="%s" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx">'
            '<div class="%s">%s<div class="sheen"></div></div></div>'
            % (r, " hide" if hide else "", extra_cls, tid, x, y, size, size, material, inner))


def ban(bid, size, x, y):
    return ('<svg class="ban hide" id="%s" viewBox="0 0 200 200" width="%d" height="%d" '
            'style="left:%dpx;top:%dpx"><circle cx="100" cy="100" r="82"/><path d="M42 42 L158 158"/></svg>'
            % (bid, size, size, x, y))


k.css("""
.abs { position: absolute; }
.hide { opacity: 0; visibility: hidden; }
.tw { position: absolute; }
.sk { fill: none; stroke: url(#gw); stroke-width: 2.3; stroke-linecap: round; stroke-linejoin: round;
  width: 50%; height: 50%; position: relative; z-index: 1; overflow: visible; }
.pearl .sk { stroke: #17141c; }
.clear { overflow: hidden; }
.circ .jelly, .circ .pearl, .circ .clear, .circ .sheen { border-radius: 50%; }
.sqring.rc { border-radius: 50%; }
.aurs { position: absolute; left: -700px; top: -700px; width: 2480px; height: 3320px; pointer-events: none;
  background:
    radial-gradient(circle 526px at 1560px 880px, rgba(255,110,156,0.50), rgba(255,110,156,0)),
    radial-gradient(circle 634px at 760px 2360px, rgba(222,32,74,0.55), rgba(222,32,74,0)),
    radial-gradient(circle 382px at 1480px 1910px, rgba(255,198,214,0.20), rgba(255,198,214,0)); }
.shc { position: absolute; inset: 0; border-radius: inherit; overflow: hidden; pointer-events: none; }
.shc .sheen { mix-blend-mode: normal; opacity: 0.4; }

/* the ban ring: one object, used on Instagram, then on the bot */
.ban { position: absolute; fill: none; stroke: #ff6e9c; stroke-width: 20; stroke-linecap: round; overflow: visible;
  filter: drop-shadow(0 0 10px rgba(255,196,218,0.9)) drop-shadow(0 0 34px rgba(255,110,156,0.75)); }

/* «?» speech bubbles */
.qb { position: absolute; width: 124px; height: 108px; border-radius: 54px 54px 54px 14px; display: flex;
  align-items: center; justify-content: center; font-size: 70px; font-weight: 900; color: #fff; }
.qb.r { border-radius: 54px 54px 14px 54px; }

/* a post, small, travelling */
.post { position: absolute; width: 96px; height: 118px; border-radius: 22px; overflow: hidden;
  background: linear-gradient(172deg, #ffffff 0%, #fff6f9 100%);
  box-shadow: inset 0 2px 1px #fff, 0 24px 40px -16px rgba(24,4,12,0.6); }
.post i, .phn i, .cal i, .stc i, .plt i, .chat i { position: absolute; display: block; }
.im { border-radius: 14px; background: linear-gradient(150deg, #f4dfe5 0%, #ecc8d0 100%); }
.rr { border-radius: 9px; background: rgba(23,20,28,0.13); }
.wire { fill: none; stroke: rgba(255,255,255,0.7); stroke-width: 6; stroke-linecap: round; stroke-dasharray: 4 18; }

/* the Instagram screen on the first takeover */
.phn { position: absolute; overflow: hidden; border-radius: 64px; color: #17141c;
  background: linear-gradient(172deg, #ffffff 0%, #fff9fb 55%, #fdf0f4 100%);
  box-shadow: inset 0 2px 1px #fff, 0 70px 130px -40px rgba(8,0,3,0.75), 0 0 0 1px rgba(255,255,255,0.35); }
.phn .av { border-radius: 50%; background: linear-gradient(150deg, #f4dfe5 0%, #ecc8d0 100%); }
.btn { border-radius: 999px; background: linear-gradient(165deg, #e0204b 0%, #ab112e 46%, #6b081c 100%);
  box-shadow: inset 0 2px 1px rgba(255,255,255,0.5), 0 18px 36px -14px rgba(70,4,20,0.6);
  color: #fff; font-weight: 700; display: flex; align-items: center; justify-content: center; letter-spacing: -0.01em; }
.phn i.btn { display: flex; font-style: normal; }
.ico { position: absolute; width: 66px; height: 66px; fill: none; stroke: #17141c; stroke-width: 1.9;
  stroke-linecap: round; stroke-linejoin: round; overflow: visible; }
.cur { position: absolute; left: 0; top: 0; width: 64px; height: 64px; z-index: 6;
  filter: drop-shadow(0 6px 10px rgba(24,4,12,0.35)); }
.ck { position: absolute; width: 120px; height: 120px; margin: -60px 0 0 -60px; border-radius: 50%;
  border: 7px solid #ff6e9c; opacity: 0; visibility: hidden; z-index: 5; }
.ant { position: absolute; left: 50%; top: -58px; width: 40px; height: 66px; margin-left: -20px; overflow: visible;
  fill: none; stroke: #ffd6e3; stroke-width: 6; stroke-linecap: round; }

/* the Meta API plate */
.plt { position: absolute; border-radius: 56px; overflow: hidden;
  background: linear-gradient(160deg, #ffffff 0%, #fff5f8 52%, #f5dfe6 100%);
  box-shadow: inset 0 2px 1px #fff, inset 0 -20px 32px -14px rgba(180,18,47,0.18),
              0 36px 64px -22px rgba(30,4,12,0.55); }
.plt .mm { position: absolute; fill: #17141c; }
.plt .api { position: absolute; font-size: 72px; font-weight: 900; letter-spacing: -0.03em; color: #17141c; line-height: 1; }
.pill { position: absolute; border-radius: 55px; display: flex; align-items: center; justify-content: center;
  background: linear-gradient(160deg, #ffffff 0%, #fff5f8 52%, #f5dfe6 100%);
  box-shadow: inset 0 2px 1px #fff, inset 0 -20px 32px -14px rgba(180,18,47,0.18), 0 36px 64px -22px rgba(30,4,12,0.55); }
.pill .wmark { font-weight: 700; letter-spacing: -0.03em; }

/* the chat on the second takeover */
.chat { position: absolute; overflow: hidden; border-radius: 64px; color: #17141c;
  background: linear-gradient(172deg, #ffffff 0%, #fff9fb 55%, #fdf0f4 100%);
  box-shadow: inset 0 2px 1px #fff, 0 70px 130px -40px rgba(8,0,3,0.75), 0 0 0 1px rgba(255,255,255,0.35); }
.chat .hdr { left: 0; top: 0; right: 0; height: 130px; border-bottom: 2px solid rgba(23,20,28,0.07); }
.bub { position: absolute; border-radius: 44px; }
.bub.in { background: #f3e7eb; border-bottom-left-radius: 12px; }
.bub.out { background: linear-gradient(165deg, #e0204b 0%, #ab112e 46%, #8d0d24 100%); border-bottom-right-radius: 12px;
  box-shadow: inset 0 2px 1px rgba(255,255,255,0.4); }
.bub.btn2 { background: #fff; box-shadow: inset 0 0 0 3px #e0204b; }
.bub i { position: absolute; display: block; height: 18px; border-radius: 9px; }
.bub.in i { background: rgba(23,20,28,0.2); }
.bub.out i { background: rgba(255,255,255,0.75); }
.bub.btn2 i { background: rgba(180,18,47,0.55); }
.dt { position: absolute; top: 37px; width: 18px; height: 18px; border-radius: 50%; background: rgba(255,255,255,0.85); }
.cab .tube { fill: none; stroke: rgba(255,255,255,0.26); stroke-width: 20; stroke-linecap: round; }

/* the calendar: one day */
.cal { position: absolute; border-radius: 52px; overflow: hidden;
  background: linear-gradient(170deg, #ffffff 0%, #fff6f9 60%, #f8e6ec 100%);
  box-shadow: inset 0 2px 1px #fff, 0 44px 80px -30px rgba(24,4,12,0.6); }
.cal .hd { left: 0; top: 0; right: 0; height: 84px; background: linear-gradient(165deg, #e0204b 0%, #8d0d24 100%); }
.cal .hole { top: 30px; width: 22px; height: 22px; border-radius: 50%; background: rgba(255,255,255,0.85); }
.cal .cell { width: 48px; height: 48px; border-radius: 14px; background: rgba(23,20,28,0.08); }
.hot { position: absolute; width: 48px; height: 48px; border-radius: 14px;
  background: linear-gradient(165deg, #e0204b 0%, #8d0d24 100%);
  box-shadow: inset 0 2px 1px rgba(255,255,255,0.5), 0 0 26px rgba(255,110,156,0.7); }

/* the settings card: «Тип акаунта» */
.stc { position: absolute; border-radius: 52px; overflow: hidden;
  background: linear-gradient(170deg, #ffffff 0%, #fff6f9 60%, #f8e6ec 100%);
  box-shadow: inset 0 2px 1px #fff, 0 44px 80px -30px rgba(24,4,12,0.6); }
.stc .lb { position: absolute; left: 140px; top: 38px; font-size: 34px; font-weight: 700; letter-spacing: -0.01em; color: #17141c; }
.sw { position: absolute; width: 104px; height: 62px; border-radius: 31px; background: rgba(23,20,28,0.16); }
.swf { position: absolute; inset: 0; border-radius: 31px; background: linear-gradient(165deg, #e0204b 0%, #8d0d24 100%);
  opacity: 0; visibility: hidden; }
.knob { position: absolute; left: 5px; top: 5px; width: 52px; height: 52px; border-radius: 50%; background: #fff;
  box-shadow: 0 4px 10px rgba(24,4,12,0.3); }

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


# ===========================================================================
# A+B · the question: Instagram, «?», a padlock -> Claude -> Windsor -> post -> ban
IGX, IGY, IGS = 430, 210, 220          # Instagram group, before it steps right
IG_DX = 270                            # -> centre (810, 320)
BAN_C = (IGX + IG_DX + IGS // 2, IGY + IGS // 2)


@beat
def a_question():
    bubbles = (
        '<div class="dglass edge qb hide" id="qb0" style="left:196px;top:176px">?</div>'
        '<div class="dglass edge qb r hide" id="qb1" style="left:762px;top:148px">?</div>'
        '<div class="dglass edge qb r hide" id="qb2" style="left:720px;top:392px">?</div>')
    ig = ('<div class="abs" id="igG" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx">' % (IGX, IGY, IGS, IGS)
          + tile("aIG", IGS, 0, 0, "pearl", g.mark("instagram"))
          + tile("aLk", 104, 146, 146, "pearl", stroke("lock"), extra_cls="circ")
          + '</div>')
    cab = ('<svg class="cab abs" width="1080" height="700" viewBox="0 0 1080 700" style="left:0;top:0">'
           '<path class="wire hide" id="aW" d="M386 320 L 694 320"/>'
           '<path class="tube hide" id="aT" d="M386 320 L 694 320"/>'
           '<path class="core hide" id="aC" d="M386 320 L 694 320"/></svg>')
    post = ('<div class="post hide" id="aPost" style="left:222px;top:261px">'
            '<i class="im" style="left:10px;top:10px;width:76px;height:58px"></i>'
            '<i class="rr" style="left:10px;top:80px;width:66px;height:10px;border-radius:5px"></i>'
            '<i class="rr" style="left:10px;top:97px;width:44px;height:10px;border-radius:5px"></i></div>')
    L.append('<div class="g full" id="gA">' + cab + bubbles
             + tile("aCl", 220, 160, 210, "jelly", g.mark("claude"))
             + tile("aQ", 96, 492, 272, "pearl", big("?", 64, "#17141c"), extra_cls="circ", ring=False)
             + tile("aWs", 150, 465, 245, "pearl", wmark(84))
             + ig + post + ban("aBan", 330, BAN_C[0] - 165, BAN_C[1] - 165) + '</div>')
    sfx("click", T["zablok"] + 0.12)
    sfx("pop", T["shtuchnyi"])
    sfx("pop", T["windsor"] + 0.02)
    sfx("impact-bass-1", T["zabanyt"] + 0.08, -2)
    return js("""
  tl.set("#gA", {autoAlpha: 1}, 0);
  arr("#aIG", @naich-0.05, {s: 0.5, y: 30});
  arr("#qb0", @pytannia-0.02, {s: 0.3, x: 60, y: 40, d: 0.7});
  arr("#qb1", @yake-0.02, {s: 0.3, x: -60, y: 40, d: 0.7});
  arr("#qb2", @pyshut-0.02, {s: 0.3, x: -60, y: -30, d: 0.7});
  /* «заблокують» — a padlock drops onto it */
  tl.fromTo("#aLk", {autoAlpha: 0, y: -170, scale: 0.7}, {autoAlpha: 1, y: 0, scale: 1, duration: 0.55, ease: POP}, @zablok-0.1);
  G.haptic("#aIG", @zablok+0.12); G.ripple("#aLkR", @zablok+0.15);
  bout(["#qb0", "#qb1", "#qb2"], @postyty-0.25, 10, 0.28);
  /* «постити через штучний інтелект» — Instagram steps right, Claude lands, a «?» link */
  tl.to("#igG", {x: {{igdx}}, duration: 0.7, ease: SP}, @postyty-0.1);
  arr("#aCl", @shtuchnyi-0.05, {s: 0.4, x: -40, y: 20});
  G.ripple("#aClR", @shtuchnyi+0.3);
  tl.set("#aW", {autoAlpha: 1}, @intelekt); draw2("aW", @intelekt, 0.45);
  arr("#aQ", @intelekt+0.25, {s: 0.3, y: 0, d: 0.6});
  /* «Клод через конектор, типу Windsor» */
  G.bump("#aCl", @klod); G.ripple("#aClR", @klod+0.05);
  tl.set(["#aT", "#aC"], {autoAlpha: 1}, @konektor); draw2("aT", @konektor, 0.5); draw2("aC", @konektor, 0.5);
  tl.to("#aW", {autoAlpha: 0, duration: 0.2}, @konektor+0.45);
  bout("#aQ", @windsor-0.15, 8, 0.2);
  arr("#aWs", @windsor-0.04, {s: 0.4, y: 0, d: 0.75});
  G.ripple("#aWsR", @windsor+0.3); shn("#aWs .sheen", @windsor+0.25);
  /* «сам постить за мене в мій профіль» — a post travels the line */
  arr("#aPost", @sam-0.08, {s: 0.4, y: 0, d: 0.5, blur: 8});
  tl.to("#aPost", {x: 270, duration: 0.42, ease: "power2.inOut"}, @sam+0.25);
  tl.to("#aPost", {x: 540, duration: 0.42, ease: "power2.inOut"}, @mii-0.25);
  tl.to("#aPost", {scale: 0.2, autoAlpha: 0, duration: 0.22, ease: "power2.in"}, @mii+0.17);
  G.bump("#aIG", @mii+0.3); G.ripple("#aIGR", @mii+0.3);
  /* «забанить» — the ban ring slams onto Instagram */
  tl.fromTo("#aBan", {autoAlpha: 0, scale: 1.7, rotation: -25, transformOrigin: "50% 50%"},
            {autoAlpha: 1, scale: 1, rotation: 0, duration: 0.45, ease: "power3.out"}, @zabanyt-0.05);
  G.haptic(["#aIG", "#aLk"], @zabanyt+0.3);
  tl.set("#aLk .pearl", {className: "jelly"}, @zabanyt+0.3);
  G.bump("#aBan", @insta1+0.05);
  bout(["#aCl", "#aWs", "#aT", "#aC"], @insta1+0.2, 10, 0.3);
  tl.set("#gA", {autoAlpha: 0}, @tak+0.5);""").replace("{{igdx}}", str(IG_DX))


# ===========================================================================
# T1 · the iris opens out of the ban ring: a bot in a human face clicks buttons
PH = (180, 100, 600, 940)         # the Instagram screen: x, y, w, h (drawn at 600x940, shown x1.2)
PS = 1.2


def _ph(ix, iy):
    return (int(PH[0] + PS * ix), int(PH[1] + PS * iy))


HEART_C = _ph(36 + 33, 700 + 33)
COMM_C = _ph(130 + 33, 700 + 33)
BTN_C = _ph(356 + 105, 44 + 32)
BOT = (120, 50, 240)
HUB = (440, 190, 260, 230)        # the Meta API hub on the next near beat
HUB_C = (HUB[0] + HUB[2] // 2, HUB[1] + HUB[3] // 2)


@beat
def t1_bots():
    x, y, w, h = PH
    phone = (
        '<div class="abs" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx;transform:scale(%s);transform-origin:0 0">'
        '<div class="phn hide" id="ph" style="left:0;top:0;width:100%%;height:100%%">'
        '<i class="av" style="left:36px;top:36px;width:84px;height:84px"></i>'
        '<i class="rr" style="left:140px;top:50px;width:170px;height:24px;border-radius:12px"></i>'
        '<i class="rr" style="left:140px;top:86px;width:110px;height:18px"></i>'
        '<i class="btn" id="phBtn" style="left:356px;top:44px;width:210px;height:64px;font-size:28px">Підписатися</i>'
        '<i class="im" style="left:0;top:150px;width:600px;height:520px;border-radius:0"></i>'
        '<svg class="ico" id="icH" viewBox="0 0 24 24" style="left:36px;top:700px">%s</svg>'
        '<svg class="ico" id="icC" viewBox="0 0 24 24" style="left:130px;top:700px">%s</svg>'
        '<svg class="ico" viewBox="0 0 24 24" style="left:224px;top:700px">%s</svg>'
        '<i class="rr" style="left:40px;top:800px;width:430px;height:22px;border-radius:11px"></i>'
        '<i class="rr" style="left:40px;top:838px;width:300px;height:22px;border-radius:11px"></i>'
        '</div></div>' % (x, y, w, h, PS, STROKES["heart"], STROKES["comment"], STROKES["share"]))
    bx, by, bs = BOT
    bot = ('<div class="sqring rc" id="botR" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx"></div>'
           '<div class="tw circ hide" id="bot" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx">'
           '<svg class="ant" viewBox="0 0 40 66"><path d="M20 64V18"/><circle cx="20" cy="11" r="7"/></svg>'
           '<div class="jelly" id="botA">%s<div class="sheen"></div></div>'
           '<div class="pearl" id="botB" style="opacity:0;visibility:hidden">%s</div></div>'
           % (bx, by, bs, bs, bx, by, bs, bs, stroke("robot"), stroke("person")))
    cks = "".join('<div class="ck" id="t1k%d" style="left:%dpx;top:%dpx"></div>' % (i, cx, cy)
                  for i, (cx, cy) in enumerate((HEART_C, COMM_C, BTN_C)))
    L.append('<div class="g full" id="gT1"><div class="tkg"></div><div class="aurs"></div><div class="grain"></div>'
             + phone + bot + cks + '<div class="cur hide" id="t1cur">%s</div>' % CURSOR
             + ban("t1Ban", 300, bx + bs // 2 - 150, by + bs // 2 - 150) + '</div>')
    sfx("whoosh-short", T["tak"] - 0.1)
    sfx("pop", T["botiv"] + 0.02)
    sfx("click", T["klats"] + 0.27)
    sfx("impact-bass-1", T["interfe"] - 0.3, -4)
    c0 = (bx + bs - 40, by + bs - 30)
    out = js("""
  G.irisOpen("#gT1", @tak-0.1, {{bcx}}, {{bcy}}, 0.6);
  drift1("#gT1", @tak, 5.5);
  arr("#ph", @tak+0.2, {s: 0.7, y: 60, d: 0.9});
  /* «ботів» — a robot lands */
  arr("#bot", @botiv-0.05, {s: 0.3, x: -30, y: -30});
  G.ripple("#botR", @botiv+0.3);
  /* «імітують людину» — it puts on a human face (the antenna stays) */
  tl.to("#botA", {scaleX: 0, duration: 0.2, ease: "power2.in"}, @imituiut+0.1);
  tl.set("#botA", {autoAlpha: 0}, @imituiut+0.3);
  tl.fromTo("#botB", {autoAlpha: 1, scaleX: 0}, {autoAlpha: 1, scaleX: 1, duration: 0.5, ease: FLIP, immediateRender: false}, @imituiut+0.3);
  G.bump("#bot", @liudynu+0.05);
  /* «клацають кнопки в інтерфейсі» — its cursor taps heart, comment, button */
  tl.set("#t1cur", {x: {{c0x}}, y: {{c0y}}}, 0);
  bin("#t1cur", @klats-0.4, 6, 0.2);
  tl.to("#t1cur", {x: {{hx}}, y: {{hy}}, duration: 0.42, ease: "power2.inOut"}, @klats-0.18);
  tl.fromTo("#t1k0", {scale: 0.3, autoAlpha: 0.95}, {scale: 1.4, autoAlpha: 0, duration: 0.5, ease: "power2.out", immediateRender: false}, @klats+0.26);
  tl.to("#icH", {fill: "#e0204b", stroke: "#e0204b", duration: 0.1}, @klats+0.26);
  tl.to("#t1cur", {x: {{cx}}, y: {{cy}}, duration: 0.3, ease: "power2.inOut"}, @knopky-0.15);
  tl.fromTo("#t1k1", {scale: 0.3, autoAlpha: 0.95}, {scale: 1.4, autoAlpha: 0, duration: 0.5, ease: "power2.out", immediateRender: false}, @knopky+0.16);
  tl.to("#t1cur", {x: {{btx}}, y: {{bty}}, duration: 0.45, ease: "power2.inOut"}, @interf-0.42);
  tl.fromTo("#t1k2", {scale: 0.3, autoAlpha: 0.95}, {scale: 1.6, autoAlpha: 0, duration: 0.55, ease: "power2.out", immediateRender: false}, @interf+0.02);
  tl.to("#phBtn", {scale: 0.92, duration: 0.08}, @interf+0.02); tl.to("#phBtn", {scale: 1, duration: 0.4, ease: SP}, @interf+0.1);
  /* and the ban ring lands on the bot */
  tl.fromTo("#t1Ban", {autoAlpha: 0, scale: 1.7, rotation: -25, transformOrigin: "50% 50%"},
            {autoAlpha: 1, scale: 1, rotation: 0, duration: 0.42, ease: "power3.out"}, @interfe-0.38);
  G.haptic("#bot", @interfe-0.1);
  bout("#t1cur", @interfe-0.2, 6, 0.2);
  G.irisClose("#gT1", @interfe+0.02, {{hubx}}, {{huby}}, 0.5);""")
    for kk, v in {"bcx": BAN_C[0], "bcy": BAN_C[1], "c0x": c0[0] - 11, "c0y": c0[1] - 8,
                  "hx": HEART_C[0] - 11, "hy": HEART_C[1] - 8, "cx": COMM_C[0] - 11, "cy": COMM_C[1] - 8,
                  "btx": BTN_C[0] - 11, "bty": BTN_C[1] - 8, "hubx": HUB_C[0], "huby": HUB_C[1]}.items():
        out = out.replace("{{%s}}" % kk, str(v))
    return out


# ===========================================================================
# C · the official door: Meta API, Metricool, Windsor -> Instagram, the lock opens
IG2 = (790, 220, 170)
LK2 = (IG2[0] + 100, IG2[1] + 100, 104)
LK2_C = (LK2[0] + LK2[2] // 2, LK2[1] + LK2[2] // 2)


@beat
def c_official():
    hx, hy, hw, hh = HUB
    hub = ('<div class="plt hide" id="hub" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx">'
           '<svg class="mm" id="hubM" style="left:75px;top:24px;width:110px;height:110px;opacity:0.18">'
           '<use href="#i-meta" width="100%%" height="100%%"/></svg>'
           '<span class="api" id="hubA" style="left:0;right:0;top:138px;text-align:center;opacity:0;visibility:hidden">API</span>'
           '<div class="shc"><div class="sheen"></div></div></div>' % (hx, hy, hw, hh))
    cab = ('<svg class="cab abs" width="1080" height="700" viewBox="0 0 1080 700" style="left:0;top:0">'
           '<path class="tube hide" id="cT1" d="M382 225 C 414 225 410 292 438 296"/>'
           '<path class="core hide" id="cC1" d="M382 225 C 414 225 410 292 438 296"/>'
           '<path class="tube hide" id="cT2" d="M282 390 C 380 390 400 322 438 316"/>'
           '<path class="core hide" id="cC2" d="M282 390 C 380 390 400 322 438 316"/>'
           '<path class="tube hide" id="cT3" d="M702 305 L 788 305"/>'
           '<path class="core hide" id="cC3" d="M702 305 L 788 305"/>'
           '<g class="pkg"><path class="pkt" id="cP1" style="opacity:0" d="M382 225 C 414 225 410 292 438 296"/>'
           '<path class="pkt" id="cP2" style="opacity:0" d="M282 390 C 380 390 400 322 438 316"/>'
           '<path class="pkt" id="cP3" style="opacity:0" d="M702 305 L 788 305"/></g></svg>')
    L.append('<div class="g full" id="gC">' + cab + hub
             + '<div class="pill hide" id="cMc" style="left:60px;top:170px;width:320px;height:110px">'
               '<span class="wmark" style="font-size:52px">Metricool</span></div>'
             + tile("cWs", 120, 160, 330, "pearl", wmark(68))
             + tile("cSeal", 88, hx + hw - 64, hy - 28, "jelly", stroke("check"), extra_cls="circ")
             + tile("cIG", IG2[2], IG2[0], IG2[1], "pearl", g.mark("instagram"))
             + tile("cLk", LK2[2], LK2[0], LK2[1], "jelly", stroke("lock"), extra_cls="circ")
             + '</div>')
    g.mark("meta")
    sfx("pop", T["meta"] + 0.02, -2)
    sfx("click-soft", T["lehal"] + 0.1)
    sfx("click", T["blokuiut2"] + 0.12)
    return js("""
  tl.set("#gC", {autoAlpha: 1}, @interfe+0.3);
  arr("#hub", @interfe+0.32, {s: 0.4, y: 0, d: 0.8});
  /* «Meta API» */
  tl.to("#hubM", {opacity: 1, duration: 0.3}, @meta-0.03);
  G.bump("#hub", @meta+0.02);
  tl.fromTo("#hubA", {autoAlpha: 0, scale: 0.6, y: 20}, {autoAlpha: 1, scale: 1, y: 0, duration: 0.55, ease: POP}, @api-0.02);
  shn("#hub .sheen", @api+0.2);
  /* «через який працюють Metricool чи Windsor» */
  arr("#cMc", @metricool-0.06, {s: 0.5, x: 40, y: 0, d: 0.75});
  tl.set(["#cT1", "#cC1"], {autoAlpha: 1}, @metricool+0.25); draw2("cT1", @metricool+0.25, 0.4); draw2("cC1", @metricool+0.25, 0.4);
  arr("#cWs", @windsor2-0.05, {s: 0.4, x: 40, y: 0, d: 0.7});
  G.ripple("#cWsR", @windsor2+0.3);
  tl.set(["#cT2", "#cC2"], {autoAlpha: 1}, @windsor2+0.3); draw2("cT2", @windsor2+0.3, 0.4); draw2("cC2", @windsor2+0.3, 0.4);
  /* «легальний спосіб» — the official seal */
  arr("#cSeal", @lehal-0.02, {s: 0.2, y: 0, d: 0.6});
  G.ripple("#cSealR", @lehal+0.25);
  /* «постити» — Instagram is on the other side; posts flow through */
  arr("#cIG", @postyty2-0.45, {s: 0.5, x: 40, y: 0, d: 0.7});
  arr("#cLk", @postyty2-0.3, {s: 0.3, y: 0, d: 0.55});
  tl.set(["#cT3", "#cC3"], {autoAlpha: 1}, @postyty2-0.1); draw2("cT3", @postyty2-0.1, 0.3); draw2("cC3", @postyty2-0.1, 0.3);
  G.packet("cP1", @postyty2+0.05, 0.4); G.packet("cP2", @postyty2+0.12, 0.4);
  G.bump("#hub", @postyty2+0.5);
  G.packet("cP3", @postyty2+0.55, 0.3);
  G.bump("#cIG", @postyty2+0.85);
  /* «і за нього не блокують» — the padlock opens */
  tl.to("#cLk .shk", {y: -5, duration: 0.4, ease: SP}, @blokuiut2+0.1);
  G.bump("#cLk", @blokuiut2+0.1); G.ripple("#cLkR", @blokuiut2+0.15);
  bout(["#hub", "#cMc", "#cWs", "#cSeal", "#cT1", "#cC1", "#cT2", "#cC2", "#cT3", "#cC3"], @blokuiut2+0.45, 10, 0.3);
  tl.set("#gC", {autoAlpha: 0}, @te+0.45);""")


# ===========================================================================
# T2 · the iris opens out of the open lock: a chatbot, plugged into the API
CH = (115, 50, 680, 820)          # drawn at 680x820, shown x1.25
CS = 1.25
PLT = (330, 1100, 420, 140)
ONE = (160, 160, 220)
ONE_C = (ONE[0] + ONE[2] // 2, ONE[1] + ONE[2] // 2)


@beat
def t2_chatbots():
    x, y, w, h = CH

    def bub(bid, cls, bx, by, bw, bh, bars):
        b = "".join('<i style="left:%dpx;top:%dpx;width:%dpx"></i>' % (34, 30 + j * 32, int((bw - 68) * f))
                    for j, f in enumerate(bars))
        return ('<div class="bub %s hide" id="%s" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx">%s</div>'
                % (cls, bid, bx, by, bw, bh, b))
    dots = "".join('<div class="dt" id="dt%d" style="left:%dpx"></div>' % (i, 50 + i * 34) for i in range(3))
    chat = (
        '<div class="abs" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx;transform:scale(%s);transform-origin:0 0">'
        '<div class="chat hide" id="ch" style="left:0;top:0;width:100%%;height:100%%">'
        '<i class="hdr"></i>'
        '<svg class="ico" viewBox="0 0 24 24" style="left:26px;top:34px;width:60px;height:60px">%s</svg>'
        '<div class="tw circ" style="left:100px;top:25px;width:80px;height:80px"><div class="jelly">%s</div></div>'
        '<i class="rr" style="left:204px;top:44px;width:180px;height:22px;border-radius:11px"></i>'
        '<i class="rr" style="left:204px;top:78px;width:110px;height:16px"></i>'
        '%s'
        '%s%s%s%s%s'
        '<div class="bub out hide" id="typ" style="left:456px;top:300px;width:188px;height:92px">%s</div>'
        '</div></div>' % (x, y, w, h, CS, STROKES["back"], stroke("robot"),
                    tile("chIG", 74, 580, 28, "pearl", g.mark("instagram"), ring=False),
                    bub("b1", "in", 36, 170, 400, 104, (1.0, 0.62)),
                    bub("b2", "out", 244, 300, 400, 150, (1.0, 0.86, 0.5)),
                    bub("b3", "btn2", 244, 470, 400, 86, (0.6,)),
                    bub("b4", "in", 36, 590, 320, 92, (0.8,)),
                    bub("b5", "out", 324, 702, 320, 92, (0.9,)), dots))
    px, py, pw, ph = PLT
    plate = ('<div class="plt hide" id="plt" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx">'
             '<svg class="mm" style="left:52px;top:24px;width:92px;height:92px"><use href="#i-meta" width="100%%" height="100%%"/></svg>'
             '<span class="api" style="left:176px;top:34px">API</span>'
             '<div class="shc"><div class="sheen"></div></div></div>' % (px, py, pw, ph))
    cab = ('<svg class="cab abs" width="1080" height="1300" viewBox="0 0 1080 1300" style="left:0;top:0">'
           '<path class="tube hide" id="t2T" d="M540 1078 L 540 1098"/><path class="core hide" id="t2C" d="M540 1078 L 540 1098"/>'
           '<g class="pkg"><path class="pkt" id="t2P" style="opacity:0" d="M540 1098 L 540 1078"/></g></svg>')
    slash = ('<svg class="ban hide" id="t2X" viewBox="0 0 200 200" width="230" height="230" style="left:740px;top:520px">'
             '<path id="t2Xp" d="M30 30 L170 170"/></svg>')
    L.append('<div class="g full" id="gT2"><div class="tkg"></div><div class="aurs"></div><div class="grain"></div>'
             + cab + chat + plate
             + tile("t2Seal", 96, px + pw - 70, py - 34, "jelly", stroke("check"), extra_cls="circ")
             + tile("t2Lk", 150, 780, 560, "jelly", stroke("lock"), extra_cls="circ")
             + slash + '</div>')
    sfx("whoosh-short", T["te"] - 0.1)
    sfx("notification", T["chatbot"] + 0.02, -3)
    sfx("click-soft", T["apriori"] + 0.05)
    sfx("click", T["zablokuv"] + 0.25)
    return js("""
  G.irisOpen("#gT2", @te-0.12, {{lkx}}, {{lky}}, 0.6);
  drift1("#gT2", @te, 8.3);
  arr("#ch", @te+0.12, {s: 0.7, y: 60, d: 0.9});
  /* a message comes in; the bot is typing */
  arr("#b1", @te+0.5, {s: 0.5, x: -40, y: 20, d: 0.6, blur: 6});
  arr("#typ", @saame+0.1, {s: 0.4, x: 40, y: 10, d: 0.5, blur: 6});
  tl.fromTo(["#dt0", "#dt1", "#dt2"], {y: 0}, {y: -10, duration: 0.18, ease: "power1.out", yoyo: true, repeat: 3, stagger: 0.09, immediateRender: false}, @saame+0.35);
  /* «чатботів» — the bot replies */
  tl.set("#typ", {autoAlpha: 0}, @chatbot-0.03);
  arr("#b2", @chatbot-0.03, {s: 0.6, x: 30, y: 10, d: 0.6, blur: 6});
  arr("#b3", @chatbot+0.25, {s: 0.6, x: 30, y: 10, d: 0.6, blur: 6});
  /* «в інстаграмі» */
  arr("#chIG", @vinsta-0.02, {s: 0.3, y: 0, d: 0.55});
  arr("#b4", @vony-0.05, {s: 0.5, x: -40, y: 20, d: 0.6, blur: 6});
  arr("#b5", @vony+0.4, {s: 0.6, x: 30, y: 10, d: 0.6, blur: 6});
  /* «через офіційний API» */
  arr("#plt", @ofits2-0.05, {s: 0.5, y: 40, d: 0.8});
  tl.set(["#t2T", "#t2C"], {autoAlpha: 1}, @ofits2+0.35); draw2("t2T", @ofits2+0.35, 0.3); draw2("t2C", @ofits2+0.35, 0.3);
  shn("#plt .sheen", @api2);
  G.packet("t2P", @api2+0.25, 0.35);
  G.bump("#ch", @api2+0.55);
  /* «апріорі» — the seal */
  arr("#t2Seal", @apriori-0.02, {s: 0.2, y: 0, d: 0.6});
  G.ripple("#t2SealR", @apriori+0.25);
  /* «не можуть заблокувати» — a padlock comes for it and is struck through */
  tl.fromTo("#t2Lk", {autoAlpha: 0, y: -200, scale: 0.7}, {autoAlpha: 1, y: 0, scale: 1, duration: 0.5, ease: POP}, @mozhut-0.15);
  tl.set("#t2X", {autoAlpha: 1}, @zablokuv+0.2); draw2("t2Xp", @zablokuv+0.2, 0.25);
  tl.to("#t2Lk", {autoAlpha: 0.45, scale: 0.9, duration: 0.3}, @zablokuv+0.45);
  G.irisClose("#gT2", @zablokuve-0.25, {{onex}}, {{oney}}, 0.5);""",
              saame=S(u"саме", 23.74)).replace("{{lkx}}", str(LK2_C[0])).replace(
        "{{lky}}", str(LK2_C[1])).replace("{{onex}}", str(ONE_C[0])).replace("{{oney}}", str(ONE_C[1]))


# ===========================================================================
# D · the one time: «1», Instagram «!», one day, the switch, everything plugged in
CAL = (110, 150, 360, 400)
HOT = (2, 1)                            # col, row of the lit day
CELL0, CELLS, CELLY = 28, 64, 120
HOT_XY = (CAL[0] + CELL0 + HOT[0] * CELLS, CAL[1] + CELLY + HOT[1] * CELLS)
HOT_C = (HOT_XY[0] + 24, HOT_XY[1] + 24)
STC = (510, 150, 470, 170)
TILES = [("dCl", 540, "jelly", "claude"), ("dWs", 680, "pearl", "w"), ("dMt", 820, "pearl", "meta")]
TY, TS = 360, 104


@beat
def d_once():
    cells = "".join('<i class="cell" style="left:%dpx;top:%dpx"></i>' % (CELL0 + c * CELLS, CELLY + r * CELLS)
                    for r in range(4) for c in range(5))
    cal = ('<div class="cal hide" id="cal" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx">'
           '<i class="hd"></i><i class="hole" style="left:96px"></i><i class="hole" style="left:242px"></i>%s'
           '<div class="shc"><div class="sheen"></div></div></div>' % (CAL + (cells,)))
    hot = ('<div class="sqring" id="hotR" style="left:%dpx;top:%dpx;width:48px;height:48px;border-radius:14px"></div>'
           '<div class="hot hide" id="hot" style="left:%dpx;top:%dpx"></div>' % (HOT_XY + HOT_XY))
    sx, sy, sw, sh = STC
    stc = ('<div class="stc hide" id="stc" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx">'
           '<div class="tw" style="left:28px;top:40px;width:90px;height:90px"><div class="pearl">%s</div></div>'
           '<span class="lb">Тип акаунта</span>'
           '<i class="rr" style="left:140px;top:96px;width:150px;height:18px"></i>'
           '<div class="sw" style="left:338px;top:86px"><div class="swf" id="swf"></div><div class="knob" id="knob"></div></div>'
           '<div class="shc"><div class="sheen"></div></div></div>'
           % (sx, sy, sw, sh, g.mark("instagram")))
    tiles = "".join(tile(tid, TS, tx, TY, mat, wmark(58) if name == "w" else g.mark(name))
                    for tid, tx, mat, name in TILES)
    L.append('<div class="g full" id="gD">'
             + tile("dOne", ONE[2], ONE[0], ONE[1], "jelly", big("1", 150), extra_cls="circ")
             + tile("dIG", 220, 640, 160, "pearl", g.mark("instagram"))
             + tile("dEx", 100, 800, 128, "jelly", big("!", 64), extra_cls="circ")
             + cal + hot + stc + tiles + '</div>')
    sfx("pop", T["odyn"] + 0.05, -2)
    sfx("ping", T["proty"] + 0.05, -3)
    sfx("click", T["akaunta"] + 0.05)
    # flight of the settings card and tiles into the lit day
    fl = []
    for i, (sel, cx, cy) in enumerate([("#stc", STC[0] + STC[2] / 2.0, STC[1] + STC[3] / 2.0)]
                                      + [("#" + tid, tx + TS / 2.0, TY + TS / 2.0) for tid, tx, _, _ in TILES]):
        fl.append('  tl.to("%s", {x: %d, y: %d, scale: 0.12, autoAlpha: 0, duration: 0.42, ease: "power3.in"}, %.3f);'
                  % (sel, HOT_C[0] - cx, HOT_C[1] - cy, T["zabahato"] - 0.05 + i * 0.09))
    return js("""
  tl.set("#gD", {autoAlpha: 1}, @zablokuve-0.3);
  /* «один-єдиний раз» */
  arr("#dOne", @zablokuve-0.28, {s: 0.3, y: 0, d: 0.8});
  G.bump("#dOne", @odyn+0.05); G.ripple("#dOneR", @odyn+0.1);
  /* «коли Інстаграм був проти» */
  arr("#dIG", @insta2-0.05, {s: 0.5, x: 40, y: 0});
  arr("#dEx", @proty-0.02, {s: 0.2, y: 0, d: 0.55});
  G.haptic("#dIG", @proty+0.1); G.ripple("#dExR", @proty+0.2);
  bout(["#dOne", "#dIG", "#dEx"], @tse2-0.05, 10, 0.3);
  /* «одного дня» — a calendar, one day lit */
  arr("#cal", @odnoho-0.25, {s: 0.6, y: 30});
  arr("#hot", @dnia+0.02, {s: 0.2, y: 0, d: 0.5, blur: 6});
  G.ripple("#hotR", @dnia+0.2);
  /* «одразу змінила тип акаунта» */
  arr("#stc", @odrazu-0.05, {s: 0.6, x: 40, y: 0});
  shn("#stc .sheen", @zminyla);
  tl.to("#knob", {x: 42, duration: 0.4, ease: SP}, @akaunta-0.05);
  tl.fromTo("#swf", {autoAlpha: 0}, {autoAlpha: 1, duration: 0.2}, @akaunta-0.05);
  /* «і підключила все до нього» */
  [["#dCl", @pidkl-0.05], ["#dWs", @pidkl+0.2], ["#dMt", @vse+0.0]].forEach(function (p) {
    arr(p[0], p[1], {s: 0.3, y: 50, d: 0.6});
  });
  G.bump("#stc", @nioho);
  /* «Забагато змін за раз» — all of it pours into that one day */
{{flight}}
  [0, 1, 2, 3].forEach(function (i) { G.bump("#hot", @zabahato+0.3 + i * 0.09); });
  tl.to("#hot", {scale: 1.9, duration: 0.5, ease: SP}, @raz-0.12);
  G.ripple("#hotR", @raz-0.1); G.ripple("#hotR", @raz+0.2);
  G.haptic("#cal", @raz-0.05);
  bout(["#cal", "#hot"], @os-0.1, 10, 0.3);
  tl.set("#gD", {autoAlpha: 0}, @os+0.3);""").replace("{{flight}}", "\n".join(fl))


# ===========================================================================
# E · «акаунт справді може насторожитись»
@beat
def e_wary():
    L.append('<div class="g full" id="gE">'
             + tile("eIG", 220, 430, 190, "pearl", g.mark("instagram"))
             + tile("eEx", 104, 592, 156, "jelly", big("!", 68), extra_cls="circ")
             + '</div>')
    sfx("notification", T["nastor"] + 0.05, -2)
    return js("""
  tl.set("#gE", {autoAlpha: 1}, @os);
  arr("#eIG", @os+0.05, {s: 0.5, y: 30});
  G.bump("#eIG", @akaunt+0.02);
  arr("#eEx", @nastor-0.04, {s: 0.2, y: 0, d: 0.55});
  G.haptic("#eIG", @nastor+0.15); G.ripple("#eExR", @nastor+0.2); G.ripple("#eIGR", @nastor+0.35);
  bout("#gE", @yakshcho-0.2, 10, 0.26);""")


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
    sfx("pop", T["yakshcho"] + 0.02, -2)
    sfx("click", T["pidpysh"] + 0.06)
    return js("""
  tl.set("#gF", {autoAlpha: 1}, @yakshcho-0.1);
  arr("#fl", @yakshcho-0.02, {s: 0.6, y: 40});
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


def span_words(a, b):
    return (round(a - 0.02, 3), round(b, 3), "")


# captions that would repeat the graphic's own words (STYLE.md §2b.1)
BLACKOUT = [
    span_words(T["meta"], T["apie"]),                 # the hub says Meta API
    span_words(T["metricool"], T["metricoole"]),      # the pill says Metricool
    span_words(T["api2"], T["api2e"]),                # the plate says API
    span_words(T["typ"], T["akauntae"]),              # the card says «Тип акаунта»
]


def check_rules():
    for a, b in NO_PAINT:
        raise AssertionError("this cut was expected to have no closeups: %s" % ((a, b),))
    assert PH[1] + PH[3] * PS <= 1240 and PLT[1] + PLT[3] <= 1240, "a sheet runs into the caption plaque"


def main():
    check_rules()
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
        title=u"Reel 35 — А мене не заблокують?",
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
