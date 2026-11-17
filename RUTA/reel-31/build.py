# -*- coding: utf-8 -*-
"""Reel 31 — «Відповіді про ШІ монтаж» (Q&A). Posts 2026-10-12.

Her ask for this one: every question she reads out is a **Threads post**
(real Threads UI, avatar + handle blurred — pre-blurred PNGs from
work/r31/threads_assets.py, so no CSS filter is spent on them).

Chain:  OVER: the iris opens on «питання»: the Threads tile, all eight
questions pile up on the burgundy ground -> the iris closes and the top post
(Q1) drops into its near place -> near: the set (Claude skills + style.md +
cloud) -> style.md alone, crossed-out drafts fan behind it, «?» -> a tangled
path A->B, then the straight one -> a stopwatch, 30 -> Q2 dark post drops
like a notification -> the Claude subscription card, the cloud, a bolt, the
20¢ coin -> OVER: the iris opens out of the coin: 40 reels -> they collapse
into 8 € -> 30 € for one reel, bars -> the iris closes onto Q3, which flips
up -> </> struck -> the chat: files + wishes out, a finished reel back, ✓ ->
Q4 with replies piling under it -> the track 30–40 хв, her 1-minute sliver,
her own checklist -> Q5 scrolls up the feed -> the edit timeline: pauses
close, subtitles, music, colour -> Q6 zooms in, the heart fills on «Так» ->
she types what to change, the reel redoes, each render a coin -> 15¢ shrinks
to nothing -> Q7 slides in -> the reel flips through styles, style.md sets
hers -> OVER: the iris opens out of style.md: Q8 huge, folds into a header ->
the subscription card, two laptops (strong: cloud not needed / old: cloud +
€ into the API wallet) -> the iris closes onto the subscription card -> near:
subscription + $1 -> the comment bar types «design», the first step lights,
«безкоштовно».

usage: python build.py   (then: python ../tools/sfx.py mix 31)
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

CUT = json.load(io.open(os.path.join(ROOT, "work", "r31", "cut.json"), encoding="utf-8"))
DUR = 106.317          # 3190 plate frames
FPS = 30
k = Kit(width=1080, height=1920, fps=FPS, duration=DUR)
g = Glass(["claude", "threads", "instagram"])
k.css(g.css())

NO_PAINT = [tuple(x) for x in CUT["no_paint"]]          # empty for this cut

CAPS = k.load_captions(os.path.join(ROOT, "work", "r31", "captions.json"))
# whisper errors in "said" words -> script / real word (align.txt), by index
FIXI = {
    11: (u"роботя?", u"робиться?"),
    29: (u"сталим", u"style.md"),
    30: (u"дій я", u"я"),
    80: (u"питати", u"бо так"),
    105: (u"монтажеру....", u"монтажеру..."),
    107: (u"Треба", u"треба"),
    142: (u"не бо", u"не"),
    143: (u"я", u"моя"),
    184: (u"пишею,", u"пишеш,"),
    194: (u"рівз", u"рілз з"),
    197: (u"про", u"при"),
    199: (u"центів", u"центах"),
    224: (u"здаєш", u"задаєш"),
    242: (u"а Якщо", u"а якщо"),
    249: (u"ще покласти", u"покласти"),
    268: (u"дизайн,", u"«design»,"),
}
for i, (old, new) in FIXI.items():
    assert CAPS[i]["w"] == old, (i, CAPS[i]["w"], old)
    CAPS[i]["w"] = new
for _a, _b in zip(CAPS, CAPS[1:]):
    _a["e"] = round(max(_a["s"] + 0.10, _b["s"] - 0.085), 3)

ANCH = {
    "pytannia": (4, u"питання"), "yak": (8, u"Як"), "ni": (15, u"Ні."), "nabir": (17, u"набір:"),
    "skily": (20, u"скіли,"), "stylemd": (22, u"style.md"), "render": (25, u"рендер"),
    "khmari": (26, u"у хмарі."), "do": (27, u"До"), "cherez": (32, u"через"), "sproby": (35, u"спроби,"),
    "robyla": (38, u"робила"), "vpershe": (40, u"вперше,"), "poiasn": (43, u"пояснював"),
    "yaki": (44, u"як, і я"), "uskl": (45, u"ускладнила"), "zrobyty": (52, u"зробити"),
    "prostishe": (53, u"простіше."), "ale": (54, u"Але коли"), "zaimaie": (59, u"займає"),
    "tr30": (60, u"30"), "khv": (61, u"хвилин,"), "bilshe": (63, u"більше."),
    "q2": (64, u"Скільки"), "potribna": (67, u"Потрібна"), "pidpyska": (69, u"підписка"),
    "yakshcho": (72, u"Якщо"), "khmari2": (74, u"у хмарі,"), "rekom": (79, u"рекомендую,"),
    "shvydshe": (81, u"швидше,"), "d20": (84, u"20"), "tsentiv": (85, u"центів"),
    "tobto": (88, u"Тобто"), "s40": (89, u"40"), "plius": (95, u"плюс-мінус"), "v8": (96, u"8"),
    "ievro": (97, u"євро."), "porivn": (98, u"Порівняно"), "t30": (100, u"30"), "ievro2": (101, u"євро"),
    "montazh": (105, u"монтажеру..."), "q3": (106, u"Чи"), "ni2": (110, u"Ні,"),
    "ne": (112, u"не"), "prosto": (114, u"просто"), "videof": (116, u"відеофайли"),
    "pobazh": (119, u"побажання"), "otrym": (123, u"отримуєш"), "hotovyi": (124, u"готовий"),
    "vse": (126, u"Все."), "q4": (127, u"Скільки"), "tsezaim": (129, u"це займає"),
    "zapysu": (131, u"запису"), "sam": (135, u"Сам"), "tryvaie": (137, u"триває"),
    "t3040": (138, u"30-40"), "khv2": (139, u"хвилин,"), "aktyvna": (144, u"активна"),
    "khvylynu": (150, u"хвилину,"), "zavant": (152, u"завантажити"), "i58": (155, u"і"),
    "zaimatys": (157, u"займатись"), "svoimy": (158, u"своїми"), "spravamy": (159, u"справами."),
    "q5": (160, u"Чи"), "absol": (168, u"Абсолютно,"), "muzyku": (173, u"музику"),
    "kolor": (176, u"кольорокорекцію!"), "q6": (177, u"Чи"), "tak": (181, u"Так,"),
    "prosto2": (183, u"просто"), "pererob": (188, u"переробляє."), "kozhna": (189, u"кожна"),
    "pererobka": (190, u"переробка"), "oplach": (191, u"оплачується"), "nulia": (195, u"нуля."),
    "ale2": (196, u"Але"), "p15": (198, u"15"), "tsentakh": (199, u"центах"),
    "kopiiky": (203, u"копійки,"), "zvert": (207, u"звертаю"), "q7": (209, u"Чи"),
    "tak2": (215, u"Так,"), "budy": (219, u"будь-яким"), "styliem": (220, u"стилем,"),
    "bo": (221, u"бо"), "styl2": (222, u"стиль"), "zadaiesh": (224, u"задаєш"), "sama": (225, u"сама."), "q8": (226, u"Що"),
    "zvych": (230, u"Звичайна"), "pidpyska2": (231, u"підписка"), "yakshcho2": (234, u"Якщо"),
    "potuzh": (236, u"потужний"), "render3": (237, u"рендер"), "znadob": (241, u"знадобиться."),
    "ayakshcho": (242, u"а якщо"), "staren": (245, u"старенький,"), "doved": (248, u"доведеться"),
    "kilka": (251, u"кілька"), "ievro3": (252, u"євро"), "api": (254, u"API."),
    "ale3": (255, u"Але"), "odnoho": (262, u"одного"), "dolara": (263, u"долара,"),
    "sprob": (264, u"щоб спробувати."), "komentar": (267, u"коментарях"), "design": (268, u"«design»,"),
    "pokazhu": (271, u"покажу,"), "pershyi": (274, u"перший"), "bezk": (276, u"Безкоштовно!"),
}
T = {}
TE = {}
for name, (i, w) in ANCH.items():
    assert CAPS[i]["w"] == w, (name, i, CAPS[i]["w"], w)
    T[name] = CAPS[i]["s"]
    TE[name] = CAPS[i]["e"]
# question spans (post text == her words) and answer starts
Q = [(8, 14), (64, 66), (106, 109), (127, 134), (160, 167), (177, 180), (209, 214), (226, 229)]
for n, (a, b) in enumerate(Q, 1):
    T["q%ds" % n], T["q%de" % n] = CAPS[a]["s"], CAPS[b]["e"]
T["dur"] = DUR


def js(src, **extra):
    """`@name`, `@name+0.12`, `@name-0.1` -> one literal time."""
    vals = dict(T)
    vals.update(extra)

    def rep(m):
        v = vals[m.group(1)] + (float(m.group(2)) if m.group(2) else 0.0)
        return "%.3f" % v
    return re.sub(r"@(\w+)([+-]\d+(?:\.\d+)?)?", rep, src)


SFX = []


def sfx(name, t, db=0):
    if isinstance(t, str):
        t = float(js(t))
    SFX.append({"t": round(max(0.0, t), 3), "name": name, "db": db})


# ---------------------------------------------------------------------------
STROKES = {
    "check": '<path d="M5.4 12.6l4.3 4.3 8.9-9.5"/>',
    "person": '<circle cx="12" cy="8.2" r="3.6"/><path d="M4.8 20c.9-3.8 3.7-5.8 7.2-5.8s6.3 2 7.2 5.8"/>',
    "doc": '<path d="M6.5 2.8h7.6l4.6 4.6v13.8H6.5z"/><path d="M14 2.8v4.8h4.7"/><path d="M9.3 12.6h6.6M9.3 16.2h4.6"/>',
    "cloud": '<path d="M7.2 18.6h10.4a4 4 0 0 0 .5-7.96A6 6 0 0 0 6.7 9.8a4.4 4.4 0 0 0 .5 8.8z"/>',
    "bolt": '<path d="M13.2 2.6L5.4 13.4h5.9l-1 8 7.9-10.9h-6z"/>',
    "up": '<path d="M12 19.2V5.4M6.2 11l5.8-5.8 5.8 5.8"/>',
    "redo": '<path d="M19.5 12a7.5 7.5 0 1 1-2.2-5.3"/><path d="M19.6 3.6v4.2h-4.2"/>',
    "laptop": '<rect x="4.2" y="5.2" width="15.6" height="10.6" rx="1.6"/><path d="M2.2 19h19.6"/>',
    "wave": '<path d="M3 12h1.6M6.4 8v8M9.6 5v14M12.8 9v6M16 6.5v11M19.2 10v4M21 12h0"/>',
    "note": '<path d="M9 18.2V5.6l10.4-2v12.2"/><circle cx="6.6" cy="18.2" r="2.4"/><circle cx="17" cy="15.8" r="2.4"/>',
    "drop": '<path d="M12 3.2s6.2 6.6 6.2 11a6.2 6.2 0 0 1-12.4 0c0-4.4 6.2-11 6.2-11z"/>',
    "rec": '<circle cx="12" cy="12" r="8.2"/>',
}
TH_ICONS = {
    "heart": '<path d="M12 20.2c-.4 0-8.4-4.9-8.4-10.5A4.7 4.7 0 0 1 12 6.8a4.7 4.7 0 0 1 8.4 2.9c0 5.6-8 10.5-8.4 10.5z"/>',
    "comment": '<path d="M20.6 11.6a8.6 8.6 0 0 1-12.6 7.6l-4.5 1.3 1.3-4.3A8.6 8.6 0 1 1 20.6 11.6z"/>',
    "repost": ('<path d="M16.6 3.4l3 3-3 3"/><path d="M19.6 6.4H9a4.6 4.6 0 0 0-4.6 4.6v.8"/>'
               '<path d="M7.4 20.6l-3-3 3-3"/><path d="M4.4 17.6H15a4.6 4.6 0 0 0 4.6-4.6v-.8"/>'),
    "share": '<path d="M21 3.2L3.4 9.9l7.3 3.4 3.4 7.5z"/><path d="M10.7 13.3l4.7-4.7"/>',
}


def stroke(name, cls="sk"):
    return '<svg class="%s" viewBox="0 0 24 24">%s</svg>' % (cls, STROKES[name])


def tile(tid, size, x, y, material, inner, extra_cls="", hide=True, ring=True):
    r = ('<div class="sqring" id="%sR" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx%s"></div>'
         % (tid, x, y, size, size, ";border-radius:50%" if "circ" in extra_cls else "")) if ring else ""
    return ('%s<div class="tw%s %s" id="%s" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx">'
            '<div class="%s">%s<div class="sheen"></div></div></div>'
            % (r, " hide" if hide else "", extra_cls, tid, x, y, size, size, material, inner))


QTEXT = [u"Як це взагалі робиться? Це якийсь плагін?",
         u"Скільки це коштує?",
         u"Чи треба вміти кодити?",
         u"Скільки часу це займає від запису до готового відео?",
         u"Чи може він додати субтитри та вирізати паузи?",
         u"Чи можу я вносити правки?",
         u"Чи можна задати йому власний стиль?",
         u"Що треба, щоб почати?"]
DARK = {2, 6}
META = {1: ("2 год", "48", "17"), 2: ("5 год", "31", "12"), 3: ("1 год", "26", "9"), 4: ("3 год", "57", "21"),
        5: ("40 хв", "19", "6"), 6: ("2 год", "24", "11"), 7: ("6 год", "38", "14"), 8: ("1 год", "63", "25")}


def post(pid, n, x=70, y=120, w=940, extra="", heart_fill=False, text=None, av=None, feed=False):
    dark = n in DARK
    tm, likes, reps = META.get(n, ("2 год", "12", "4"))
    a = (n - 1) if av is None else av
    hico = '<svg viewBox="0 0 24 24">%s</svg>' % TH_ICONS["heart"]
    if heart_fill:
        hico += ('<svg class="hfl hide" id="%sH" viewBox="0 0 24 24">%s</svg>' % (pid, TH_ICONS["heart"]))
        likes_html = '<b id="%sL0">%s</b><b class="hide" id="%sL1" style="position:absolute;left:54px">%d</b>' % (
            pid, likes, pid, int(likes) + 1)
    else:
        likes_html = "<b>%s</b>" % likes
    body = text if text is not None else '<div class="tx">%s</div>' % QTEXT[n - 1]
    return (
        '<div class="tp%s%s hide" id="%s" style="left:%dpx;top:%dpx;width:%dpx;%s">'
        '<div class="av"><img src="assets/threads/av%d.png" alt=""></div>'
        '<div class="hd"><img class="hn" src="assets/threads/h%d%s.png" alt=""><span class="tm">%s</span></div>'
        '<svg class="more" viewBox="0 0 24 24"><circle cx="5" cy="12" r="1.8"/><circle cx="12" cy="12" r="1.8"/>'
        '<circle cx="19" cy="12" r="1.8"/></svg>%s'
        '<div class="ic"><span>%s%s</span><span><svg viewBox="0 0 24 24">%s</svg><b>%s</b></span>'
        '<span><svg viewBox="0 0 24 24">%s</svg></span><span><svg viewBox="0 0 24 24">%s</svg></span></div>'
        '<div class="shc"><div class="sheen"></div></div></div>'
        % (" tdk" if dark else "", " fd" if feed else "", pid, x, y, w, extra, a % 10, a % 10, "d" if dark else "",
           tm, body, hico, likes_html, TH_ICONS["comment"], reps, TH_ICONS["repost"], TH_ICONS["share"]))


k.css("""
.abs { position: absolute; }
.hide { opacity: 0; visibility: hidden; }
.tw { position: absolute; }
.sk { fill: none; stroke: url(#gw); stroke-width: 2.3; stroke-linecap: round; stroke-linejoin: round;
  width: 50%; height: 50%; position: relative; z-index: 1; overflow: visible; }
.pearl .sk { stroke: #17141c; }
.circ .jelly, .circ .pearl, .circ .clear, .circ .sheen { border-radius: 50%; }
.clear { overflow: hidden; }
.aurs { position: absolute; left: -700px; top: -700px; width: 2480px; height: 3320px; pointer-events: none;
  background:
    radial-gradient(circle 526px at 1560px 880px, rgba(255,110,156,0.50), rgba(255,110,156,0)),
    radial-gradient(circle 634px at 760px 2360px, rgba(222,32,74,0.55), rgba(222,32,74,0)),
    radial-gradient(circle 382px at 1480px 1910px, rgba(255,198,214,0.20), rgba(255,198,214,0)); }
.shc { position: absolute; inset: 0; border-radius: inherit; overflow: hidden; pointer-events: none; }
.shc .sheen { mix-blend-mode: normal; opacity: 0.4; }

/* ---------- a Threads post (light; .tdk = Threads dark) ---------- */
.tp { position: absolute; border-radius: 46px; padding: 30px 44px 28px 142px; color: #000;
  background: linear-gradient(170deg, #ffffff 0%, #fafafa 100%);
  box-shadow: inset 0 2px 1px #fff, 0 0 0 1px rgba(0,0,0,0.05), 0 44px 90px -34px rgba(16,4,10,0.62); }
.tp .av { position: absolute; left: 40px; top: 34px; width: 84px; height: 84px; border-radius: 50%; overflow: hidden; }
.tp .av img { width: 84px; height: 84px; display: block; }
.tp .hd { display: flex; align-items: center; height: 50px; margin-left: -12px; }
.tp .hn { height: 48px; width: auto; display: block; }
.tp .tm { font-size: 30px; font-weight: 400; color: #999; margin-left: 4px; }
.tp .more { position: absolute; right: 40px; top: 40px; width: 42px; height: 42px; fill: #000; }
.tp .tx { font-size: 43px; line-height: 1.25; font-weight: 400; letter-spacing: -0.005em; margin-top: 4px; }
.tp .ic { display: flex; align-items: center; gap: 46px; margin-top: 24px; height: 46px; }
.tp .ic span { display: flex; align-items: center; gap: 10px; position: relative; }
.tp .ic svg { width: 44px; height: 44px; fill: none; stroke: #000; stroke-width: 1.7; stroke-linecap: round;
  stroke-linejoin: round; }
.tp .ic b { font-size: 28px; font-weight: 400; color: #999; }
.tp .ic svg.hfl { position: absolute; left: 0; top: 1px; fill: #ff3040; stroke: #ff3040; }
.tp.tdk { color: #f3f5f7; background: linear-gradient(170deg, #1b1b1b 0%, #0f0f0f 100%);
  box-shadow: inset 0 1.5px 0 rgba(255,255,255,0.12), 0 0 0 1px rgba(255,255,255,0.08), 0 44px 90px -30px rgba(0,0,0,0.78); }
.tp.tdk .ic svg { stroke: #f3f5f7; } .tp.tdk .more { fill: #f3f5f7; }
.tp.tdk .tm, .tp.tdk .ic b { color: #7a7a7a; }
.tp.tdk .ic svg.hfl { fill: #ff3040; stroke: #ff3040; }
.tp.fd { border-radius: 0; box-shadow: none; background: #fff; border-bottom: 1.5px solid #ececec; }
.gbar { display: block; height: 26px; border-radius: 13px; background: rgba(0,0,0,0.11); margin: 14px 0 0; }
.thread-tile { position: absolute; }

/* a reply under a thread */
.rep { position: absolute; height: 92px; border-radius: 30px; background: linear-gradient(170deg, #ffffff 0%, #f7f7f7 100%);
  box-shadow: inset 0 2px 1px #fff, 0 30px 60px -26px rgba(16,4,10,0.6); }
.rep .ra { position: absolute; left: 18px; top: 16px; width: 60px; height: 60px; border-radius: 50%; overflow: hidden; }
.rep .ra img { width: 60px; height: 60px; display: block; }
.rep .rh { position: absolute; left: 82px; top: 6px; height: 40px; }
.rep i { position: absolute; display: block; left: 96px; top: 56px; height: 16px; border-radius: 8px; background: rgba(0,0,0,0.12); }
.thl { position: absolute; width: 6px; border-radius: 3px; background: rgba(255,255,255,0.75); transform-origin: 50% 0%; }

/* labels on footage */
.lbl { position: absolute; width: 300px; text-align: center; color: #fff; font-size: 36px; font-weight: 700;
  letter-spacing: -0.01em; text-shadow: 0 2px 18px rgba(20,4,10,0.45); }
.pls { position: absolute; width: 60px; text-align: center; color: #fff; font-size: 72px; font-weight: 400; line-height: 1; }

/* drafts that did not work */
.drf { position: absolute; width: 150px; height: 190px; border-radius: 26px;
  background: linear-gradient(170deg, #ffffff 0%, #fbf3f6 100%);
  box-shadow: inset 0 2px 1px #fff, 0 30px 60px -24px rgba(24,4,12,0.6); }
.drf i { position: absolute; display: block; left: 22px; height: 12px; border-radius: 6px; background: rgba(23,20,28,0.13); }
.drf i.h { height: 18px; background: linear-gradient(115deg, #c41434 0%, #8d0d24 100%); }
.xx { position: absolute; left: 0; top: 0; overflow: visible; }
.xx path { fill: none; stroke: #e0204b; stroke-width: 10; stroke-linecap: round; }
.tang { fill: none; stroke: rgba(255,255,255,0.9); stroke-width: 9; stroke-linecap: round; stroke-linejoin: round; }
.strt { fill: none; stroke: #ff8ab0; stroke-width: 14; stroke-linecap: round; }

/* stopwatch */
.sw { position: absolute; border-radius: 50%;
  background: linear-gradient(160deg, #ffffff 0%, #fff5f8 52%, #f5dfe6 100%);
  box-shadow: inset 0 2px 1px #fff, inset 0 -20px 32px -14px rgba(180,18,47,0.18), 0 40px 80px -28px rgba(30,4,12,0.65); }
.sw .crown { position: absolute; left: 50%; top: -34px; width: 60px; height: 34px; margin-left: -30px; border-radius: 12px 12px 4px 4px;
  background: linear-gradient(165deg, #e0204b 0%, #8d0d24 100%); }
.sw svg { position: absolute; left: 0; top: 0; }
.sw .trk { fill: none; stroke: rgba(23,20,28,0.08); stroke-width: 22; }
.sw .prg { fill: none; stroke: #c41434; stroke-width: 22; stroke-linecap: round; }
.sw .num { position: absolute; left: 0; right: 0; top: 96px; text-align: center; }
.sw .u { position: absolute; left: 0; right: 0; top: 262px; text-align: center; font-size: 40px; font-weight: 700; color: rgba(23,20,28,0.45); }
.big { font-weight: 900; letter-spacing: -0.045em; line-height: 1;
  background: linear-gradient(118deg, #7e0b20 0%, #b4122f 42%, #ff6e9c 100%);
  -webkit-background-clip: text; background-clip: text; color: transparent; padding-right: 8px; }

/* Claude subscription card */
.memb { position: absolute; border-radius: 52px; overflow: hidden; color: #fff;
  background: linear-gradient(150deg, #e0204b 0%, #ab112e 46%, #6b081c 100%);
  box-shadow: inset 0 2px 1px rgba(255,255,255,0.55), inset 0 -40px 60px -30px rgba(255,125,165,0.55),
              0 50px 100px -36px rgba(70,4,20,0.75); }
.memb .mk { position: absolute; left: 44px; top: 44px; width: 96px; height: 96px; }
.memb .nm { position: absolute; left: 160px; top: 58px; font-size: 62px; font-weight: 700; letter-spacing: -0.02em; }
.memb .chp { position: absolute; left: 44px; bottom: 44px; height: 72px; padding: 0 30px 0 22px; border-radius: 36px;
  display: flex; align-items: center; gap: 10px; background: rgba(255,255,255,0.94); color: #b4122f;
  font-size: 34px; font-weight: 700; }
.memb .chp svg { width: 40px; height: 40px; fill: none; stroke: #b4122f; stroke-width: 2.6; stroke-linecap: round; stroke-linejoin: round; }
.memb .emv { position: absolute; right: 50px; top: 52px; width: 96px; height: 72px; border-radius: 16px;
  background: linear-gradient(140deg, rgba(255,255,255,0.55), rgba(255,210,224,0.25));
  box-shadow: inset 0 0 0 1.5px rgba(255,255,255,0.45); }
.coin .wmark { color: #fff; }

/* the 40-reel grid */
.rl { position: absolute; width: 112px; height: 199px; border-radius: 22px;
  background: linear-gradient(165deg, rgba(255,255,255,0.96) 0%, rgba(255,232,240,0.86) 100%);
  box-shadow: inset 0 2px 1px #fff, 0 18px 30px -14px rgba(8,0,3,0.6); }
.rl::before { content: ""; position: absolute; left: 46px; top: 80px; width: 0; height: 0;
  border-left: 26px solid #b4122f; border-top: 16px solid transparent; border-bottom: 16px solid transparent; }
.rl::after { content: ""; position: absolute; left: 18px; right: 18px; bottom: 22px; height: 10px; border-radius: 5px;
  background: rgba(23,20,28,0.15); }
.sheet .cm { position: absolute; left: 0; right: 0; text-align: center; }
.bar { position: absolute; bottom: 60px; left: 130px; width: 200px; border-radius: 30px; transform-origin: 50% 100%; }
.bar.lo { background: linear-gradient(170deg, #ffd0de 0%, #ff8ab0 100%); box-shadow: inset 0 2px 1px rgba(255,255,255,0.7); }
.bar.hi { background: linear-gradient(165deg, #ff6e9c 0%, #e0204b 45%, #8d0d24 100%); box-shadow: inset 0 2px 1px rgba(255,255,255,0.5); }
.who { display: inline-flex; align-items: center; gap: 10px; }
.who svg { width: 36px; height: 36px; fill: none; stroke: rgba(23,20,28,0.5); stroke-width: 2.4; stroke-linecap: round; }

/* code tile */
.inkt { position: absolute; inset: 0; border-radius: 22.4%; display: flex; align-items: center; justify-content: center;
  background: linear-gradient(160deg, #2e2430 0%, #17141c 100%); color: #fff; font-size: 82px; font-weight: 700;
  letter-spacing: -0.02em; box-shadow: inset 0 1.5px 0 rgba(255,255,255,0.18), 0 40px 80px -30px rgba(10,0,4,0.75); }
.strike { fill: none; stroke: #ff6e9c; stroke-width: 18; stroke-linecap: round; }

/* chat */
.bub { position: absolute; border-radius: 48px 48px 14px 48px; overflow: hidden;
  background: linear-gradient(165deg, #e0204b 0%, #ab112e 46%, #6b081c 100%);
  box-shadow: inset 0 2px 1px rgba(255,255,255,0.5), 0 34px 70px -26px rgba(70,4,20,0.7); }
.bub i { position: absolute; display: block; height: 22px; border-radius: 11px; background: rgba(255,255,255,0.85); }
.fth { position: absolute; width: 100px; height: 150px; border-radius: 20px;
  background: linear-gradient(160deg, #3a2a34 0%, #17141c 100%); box-shadow: inset 0 1.5px 0 rgba(255,255,255,0.2); }
.fth::before { content: ""; position: absolute; left: 40px; top: 56px; width: 0; height: 0;
  border-left: 26px solid #fff; border-top: 16px solid transparent; border-bottom: 16px solid transparent; }
.rcard { position: absolute; border-radius: 40px; overflow: hidden;
  background: linear-gradient(170deg, #ffffff 0%, #fff6f9 100%);
  box-shadow: inset 0 2px 1px #fff, 0 44px 90px -30px rgba(24,4,12,0.65); }
.rcard .th { position: absolute; left: 14px; top: 14px; right: 14px; bottom: 96px; border-radius: 28px;
  background: linear-gradient(160deg, #ff8ab0 0%, #c41434 55%, #6b081c 100%); }
.rcard .th.v2 { background: linear-gradient(200deg, #ffd6e3 0%, #ff6e9c 50%, #8d0d24 100%); }
.rcard .th::before { content: ""; position: absolute; left: 50%; top: 50%; margin: -24px 0 0 -14px; width: 0; height: 0;
  border-left: 40px solid rgba(255,255,255,0.95); border-top: 24px solid transparent; border-bottom: 24px solid transparent; }
.rcard i { position: absolute; display: block; left: 30px; height: 18px; border-radius: 9px; background: rgba(23,20,28,0.14); }

/* time track */
.trk2 { position: absolute; height: 34px; border-radius: 17px; }
.trk2.bg { background: rgba(255,255,255,0.18); box-shadow: inset 0 1.5px 2px rgba(0,0,0,0.25); }
.trk2.fl { background: linear-gradient(90deg, #ff8ab0 0%, #e0204b 100%); transform-origin: 0 50%; }
.trk2.cl { background: linear-gradient(90deg, rgba(255,255,255,0.92) 0%, rgba(255,226,236,0.86) 100%); transform-origin: 0 50%; }
.trk2.sl { background: #ff3d7a; box-shadow: 0 0 22px rgba(255,110,156,0.9); }
.pill { position: absolute; height: 68px; border-radius: 34px; padding: 0 28px; display: flex; align-items: center;
  background: linear-gradient(160deg, #ffffff 0%, #fff3f7 100%); color: #b4122f; font-size: 38px; font-weight: 700;
  white-space: nowrap; box-shadow: inset 0 2px 1px #fff, 0 22px 44px -18px rgba(24,4,12,0.6); }
.pill.hot { background: linear-gradient(165deg, #e0204b 0%, #8d0d24 100%); color: #fff;
  box-shadow: inset 0 2px 1px rgba(255,255,255,0.5), 0 22px 44px -18px rgba(70,4,20,0.7); }

/* checklist */
.lst { position: absolute; border-radius: 52px; overflow: hidden;
  background: linear-gradient(172deg, #ffffff 0%, #fff9fb 55%, #fdf0f4 100%);
  box-shadow: inset 0 2px 1px #fff, 0 50px 100px -36px rgba(24,4,12,0.62); }
.lst i { position: absolute; display: block; height: 24px; border-radius: 12px; background: rgba(23,20,28,0.13); }
.cbx { position: absolute; width: 56px; height: 56px; border-radius: 17px; box-shadow: inset 0 0 0 4px rgba(23,20,28,0.22); }
.cbf { position: absolute; inset: 0; border-radius: 17px;
  background: linear-gradient(165deg, #e0204b 0%, #8d0d24 100%); opacity: 0; visibility: hidden; }
.cbf svg { position: absolute; left: 8px; top: 8px; width: 40px; height: 40px; fill: none; stroke: #fff;
  stroke-width: 3.2; stroke-linecap: round; stroke-linejoin: round; }

/* the Threads feed window */
.feed { position: absolute; border-radius: 46px; overflow: hidden; background: #fff;
  box-shadow: inset 0 2px 1px #fff, 0 44px 90px -34px rgba(16,4,10,0.62); }
.fcol { position: absolute; left: 0; top: 0; width: 940px; }

/* the edit timeline */
.tln { position: absolute; }
.trh { position: absolute; left: 34px; width: 80px; height: 80px; border-radius: 22px; display: flex; align-items: center;
  justify-content: center; background: linear-gradient(160deg, #ffffff 0%, #fff5f8 52%, #f5dfe6 100%);
  box-shadow: inset 0 2px 1px #fff, 0 14px 28px -12px rgba(10,0,4,0.6); color: #17141c; font-size: 36px; font-weight: 700; }
.trh svg { width: 46px; height: 46px; fill: none; stroke: #17141c; stroke-width: 2.2; stroke-linecap: round; stroke-linejoin: round; }
.cpl { position: absolute; height: 36px; border-radius: 12px; background: rgba(255,255,255,0.92); }
.wv { position: absolute; width: 10px; border-radius: 5px; background: rgba(255,255,255,0.88); }
.gap { position: absolute; border-radius: 14px; background: rgba(255,61,122,0.55); box-shadow: inset 0 0 0 2px #ff6e9c;
  transform-origin: 0 50%; }
.mus { fill: none; stroke: #ffd6e3; stroke-width: 7; stroke-linecap: round; }
.grd0 { position: absolute; height: 56px; border-radius: 18px; background: linear-gradient(90deg, #8a8a8a 0%, #c9c9c9 50%, #9a9a9a 100%); }
.grd1 { position: absolute; height: 56px; border-radius: 18px; background: linear-gradient(90deg, #6b081c 0%, #e0204b 40%, #ff8ab0 75%, #ffd6e3 100%); }

/* coins */
.coin { position: absolute; }
.coin .jelly { border-radius: 50%; }

/* style skins on the reel card */
.skin { position: absolute; inset: 0; border-radius: 40px; overflow: hidden; }
.skin i { position: absolute; display: block; border-radius: 10px; }
.sk0 { background: linear-gradient(165deg, #e0204b 0%, #8d0d24 100%); }
.sk0 i { background: rgba(255,255,255,0.85); }
.sk1 { background: linear-gradient(170deg, #ffffff 0%, #f6f6f6 100%); }
.sk1 i { background: rgba(23,20,28,0.8); }
.sk2 { background: linear-gradient(170deg, #2a2230 0%, #121016 100%); }
.sk2 i { background: #ff6e9c; }
.sk3 { background: linear-gradient(170deg, #fff4f7 0%, #ffd6e3 100%); }
.sk3 i { background: linear-gradient(115deg, #c41434 0%, #8d0d24 100%); }
.dlab { position: absolute; width: 260px; text-align: center; color: #fff; font-size: 34px; font-weight: 700; }

/* API wallet */
.wal { position: absolute; border-radius: 52px; overflow: hidden;
  background: linear-gradient(172deg, #ffffff 0%, #fff9fb 55%, #fdf0f4 100%);
  box-shadow: inset 0 2px 1px #fff, 0 50px 100px -36px rgba(8,0,3,0.75); }
.wal .t { position: absolute; left: 44px; top: 36px; font-size: 72px; font-weight: 900; letter-spacing: -0.03em; color: #17141c; }
.wal .bb { position: absolute; left: 44px; right: 44px; top: 150px; height: 34px; border-radius: 17px; background: rgba(23,20,28,0.08); }
.wal .bf { position: absolute; left: 44px; top: 150px; width: 382px; height: 34px; border-radius: 17px; transform-origin: 0 50%;
  background: linear-gradient(90deg, #ff8ab0 0%, #e0204b 100%); }
.spin { position: absolute; fill: none; stroke: #ff8ab0; stroke-width: 9; stroke-linecap: round; stroke-dasharray: 70 300; }

/* the comment bar */
.cbar { position: absolute; }
.cbar .ph { position: absolute; left: 150px; top: 0; height: 130px; line-height: 130px; font-size: 40px; font-weight: 500;
  color: rgba(255,255,255,0.6); }
.cbar .ty { position: absolute; left: 150px; top: 0; height: 130px; line-height: 130px; font-size: 50px; font-weight: 700;
  color: #fff; letter-spacing: -0.01em; }
.step { position: absolute; width: 170px; border-radius: 30px;
  background: linear-gradient(158deg, rgba(255,255,255,0.36) 0%, rgba(255,255,255,0.12) 100%);
  box-shadow: inset 0 2px 1px rgba(255,255,255,0.7), 0 30px 60px -24px rgba(24,4,12,0.55); }
.step .on { position: absolute; inset: 0; border-radius: 30px; opacity: 0; visibility: hidden;
  background: linear-gradient(165deg, #ff6e9c 0%, #e0204b 50%, #8d0d24 100%);
  box-shadow: inset 0 2px 1px rgba(255,255,255,0.5), 0 0 40px rgba(255,110,156,0.7); }
.free { position: absolute; height: 120px; border-radius: 60px; padding: 0 56px; display: flex; align-items: center;
  background: linear-gradient(165deg, #ff6e9c 0%, #e0204b 46%, #8d0d24 100%); color: #fff; font-size: 66px; font-weight: 900;
  letter-spacing: -0.02em; box-shadow: inset 0 2px 1px rgba(255,255,255,0.5), 0 40px 80px -26px rgba(70,4,20,0.75); }
""")

L = []
BEATS = []


def beat(fn):
    BEATS.append(fn)
    return fn


TKG = '<div class="tkg"></div><div class="aurs"></div><div class="grain"></div>'


# ===========================================================================
# A · OVER — «всі ваші питання»: the eight questions pile up; Q1 lands on top
PILE = [  # n, dx, dy (from its own near pose), rotation
    (8, -60, 220, -2.4), (7, 90, 310, 2.2), (6, -90, 400, 1.6), (5, 70, 490, -2.0),
    (4, -40, 580, 2.4), (3, 110, 670, -1.4), (2, -80, 760, 1.8),
]


@beat
def a_pile():
    cards = "".join(post("pA%d" % n, n, x=70, y=0) for n, _, _, _ in PILE)
    L.append('<div class="g full" id="gA">' + TKG
             + tile("aTh", 150, 465, 46, "jelly", g.mark("threads"), ring=False)
             + cards + '</div>')
    L.append('<div class="g full" id="gQ1">' + post("pQ1", 1) + '</div>')
    sfx("whoosh-short", T["pytannia"] - 0.2)
    sfx("pop", T["pytannia"] + 0.15, -2)
    sfx("whoosh-short", 3.22, -3)
    lines = []
    t0 = T["pytannia"] + 0.08
    for i, (n, dx, dy, r) in enumerate(PILE):
        t = t0 + i * 0.15
        lines.append('  tl.fromTo("#pA%d", {autoAlpha: 0, x: %d, y: %d, rotation: %.1f, scale: 1.12}, '
                     '{autoAlpha: 1, x: %d, y: %d, rotation: %.1f, scale: 1.12, duration: 0.6, ease: SOFT}, %.3f);'
                     % (n, dx * 1.6, dy - 520, r * 3, dx, dy, r, t))
    tq1 = t0 + len(PILE) * 0.15 + 0.05
    return js("""
  G.irisOpen("#gA", @pytannia-0.2, 540, 330, 0.6);
  arr("#aTh", @pytannia-0.1, {s: 0.4, y: 40});
%s
  tl.set("#gQ1", {autoAlpha: 1}, %.3f);
  tl.fromTo("#pQ1", {autoAlpha: 0, x: 0, y: 240, rotation: -4, scale: 1.12},
            {autoAlpha: 1, y: 740, rotation: -0.8, scale: 1.12, duration: 0.55, ease: SOFT}, %.3f);
  tl.to("#pQ1", {y: 0, rotation: 0, scale: 1, duration: 0.75, ease: SP}, 3.22);
  G.irisClose("#gA", 3.2, 540, 262, 0.5);
  shn("#pQ1 .sheen", @q1s);
  tl.to("#pQ1", {y: -60, scale: 0.9, autoAlpha: 0, duration: 0.3, ease: "power3.in"}, @ni-0.1);
  tl.set("#gQ1", {autoAlpha: 0}, @ni+0.25);""" % ("\n".join(lines), tq1, tq1))


# ===========================================================================
# B · near — the set: Claude skills + style.md + the cloud render
#     -> style.md alone, crossed-out drafts, «?» -> tangled vs straight
@beat
def b_set():
    drafts = ""
    for i in range(4):
        drafts += ('<div class="drf hide" id="dr%d" style="left:465px;top:210px">'
                   '<i class="h" style="top:26px;width:80px"></i><i style="top:60px;width:106px"></i>'
                   '<i style="top:84px;width:92px"></i><i style="top:108px;width:66px"></i>'
                   '<svg class="xx" width="150" height="190"><path id="drx%d" d="M28 40 L122 150 M122 40 L28 150"/></svg>'
                   '</div>' % (i, i))
    tang = ("M195 360 C 300 150, 430 560, 380 330 S 250 190, 470 250 S 650 560, 560 430 "
            "S 450 210, 690 230 S 830 540, 760 420 S 700 250, 885 360")
    svg = ('<svg class="abs" width="1080" height="700" style="left:0;top:0;overflow:visible">'
           '<path class="tang hide" id="tng" d="%s"/><path class="strt hide" id="str" d="M195 360 L885 360"/></svg>' % tang)
    L.append(
        '<div class="g full" id="gB">'
        '<div class="shelf edge hide" id="shB" style="left:70px;top:150px;width:940px;height:430px"></div>'
        + drafts
        + tile("bSk", 200, 130, 190, "jelly", g.mark("claude"))
        + tile("bSt", 200, 440, 190, "pearl", stroke("doc"))
        + tile("bCl", 200, 750, 190, "clear", stroke("cloud"))
        + '<div class="lbl hide" id="lb0" style="left:80px;top:414px">скіли</div>'
        + '<div class="lbl hide" id="lb1" style="left:390px;top:414px">style.md</div>'
        + '<div class="lbl hide" id="lb2" style="left:700px;top:414px">рендер у хмарі</div>'
        + '<div class="pls hide" id="pl0" style="left:355px;top:254px">+</div>'
        + '<div class="pls hide" id="pl1" style="left:665px;top:254px">+</div>'
        + tile("bQ", 112, 612, 150, "jelly", '<span class="wmark" style="font-size:70px;color:#fff">?</span>',
               extra_cls="circ")
        + svg
        + tile("bA", 130, 130, 295, "jelly", stroke("person"), extra_cls="circ", ring=False)
        + tile("bB", 130, 820, 295, "pearl", stroke("check"), extra_cls="circ")
        + '</div>')
    sfx("pop", T["nabir"], -3)
    sfx("click-soft", T["skily"] + 0.05)
    sfx("ping", T["poiasn"] + 0.05, -3)
    sfx("pop", T["prostishe"] + 0.35, -2)
    return js("""
  tl.set("#gB", {autoAlpha: 1}, @nabir-0.15);
  arr("#shB", @nabir-0.1, {s: 0.85, y: 30});
  arr("#bSk", @skily-0.06, {s: 0.4, y: 30}); G.ripple("#bSkR", @skily+0.25);
  bin("#lb0", @skily+0.1, 8, 0.3);
  bin("#pl0", @stylemd-0.25, 8, 0.25);
  arr("#bSt", @stylemd-0.06, {s: 0.4, y: 30}); G.ripple("#bStR", @stylemd+0.25);
  bin("#lb1", @stylemd+0.1, 8, 0.3);
  bin("#pl1", @render-0.25, 8, 0.25);
  arr("#bCl", @render-0.06, {s: 0.4, y: 30}); G.ripple("#bClR", @render+0.25);
  bin("#lb2", @render+0.1, 8, 0.3);
  /* style.md stays: the others step away */
  bout(["#bSk", "#bCl", "#lb0", "#lb2", "#pl0", "#pl1"], @do-0.1, 10, 0.3);
  tl.to("#lb1", {y: 40, duration: 0.5, ease: SP}, @do);
  tl.to("#bSt", {scale: 1.18, y: 10, duration: 0.6, ease: SP}, @do);
  shn("#bSt .sheen", @do+0.2);
  /* the long tries: drafts fan out behind it, each crossed out */
  [[-370, -9], [-200, -4], [200, 4], [370, 9]].forEach(function (p, i) {
    tl.fromTo("#dr" + i, {autoAlpha: 0, x: 0, rotation: 0, scale: 0.6},
              {autoAlpha: 1, x: p[0], rotation: p[1], scale: 1, duration: 0.7, ease: SP}, @cherez-0.1 + i * 0.09);
  });
  [0, 1, 2, 3].forEach(function (i) { draw2("drx" + i, @sproby+0.15 + i * 0.28, 0.28); });
  tl.to(["#dr0", "#dr1", "#dr2", "#dr3"], {autoAlpha: 0.45, duration: 0.4}, @vpershe);
  arr("#bQ", @poiasn-0.05, {s: 0.3, y: 30, d: 0.7}); G.ripple("#bQR", @poiasn+0.2);
  G.haptic("#bQ", @poiasn+0.45);
  /* the hard way vs the simple way */
  bout(["#dr0", "#dr1", "#dr2", "#dr3", "#bSt", "#lb1", "#bQ"], @yaki-0.15, 10, 0.3);
  arr("#bA", @yaki-0.05, {s: 0.4, y: 20, d: 0.7});
  arr("#bB", @yaki+0.1, {s: 0.4, y: 20, d: 0.7});
  tl.set("#tng", {autoAlpha: 1}, @uskl);
  draw2("tng", @uskl, 1.35);
  tl.to("#tng", {autoAlpha: 0.18, duration: 0.35}, @prostishe-0.05);
  tl.set("#str", {autoAlpha: 1}, @prostishe-0.05);
  draw2("str", @prostishe-0.05, 0.4);
  G.bump("#bB", @prostishe+0.35); G.ripple("#bBR", @prostishe+0.35);
  bout("#gB", @ale-0.05, 10, 0.3);""")


# ===========================================================================
# C · near — «це займає 30 хвилин, не більше»: a stopwatch
@beat
def c_watch():
    L.append(
        '<div class="g full" id="gC"><div class="sw hide" id="sw" style="left:350px;top:170px;width:380px;height:380px">'
        '<div class="crown"></div>'
        '<svg width="380" height="380" viewBox="0 0 380 380"><circle class="trk" cx="190" cy="190" r="160"/>'
        '<path class="prg" id="swp" d="M190 30 A160 160 0 0 1 190 350"/></svg>'
        '<div class="num"><span class="big" id="swn" style="font-size:150px">0</span></div>'
        '<div class="u">хв</div></div></div>')
    sfx("click", T["tr30"] + 0.02, -2)
    return js("""
  tl.set("#gC", {autoAlpha: 1}, @ale+0.05);
  arr("#sw", @ale+0.1, {s: 0.5, y: 30});
  draw2("swp", @zaimaie+0.1, 0.75);
  G.count("#swn", @zaimaie+0.1, 30, 0.75);
  G.bump("#sw", @bilshe+0.05);
  bout("#gC", @q2s-0.3, 10, 0.25);""")


# ===========================================================================
# D · Q2 — a dark post drops in like a notification
@beat
def d_q2():
    L.append('<div class="g full" id="gD">' + post("pQ2", 2) + '</div>')
    sfx("notification", T["q2s"] - 0.05, -2)
    return js("""
  tl.set("#gD", {autoAlpha: 1}, @q2s-0.3);
  tl.fromTo("#pQ2", {autoAlpha: 0, y: -430, scale: 0.94}, {autoAlpha: 1, y: 0, scale: 1, duration: 0.85, ease: SOFT}, @q2s-0.25);
  G.haptic("#pQ2", @q2s+0.3);
  tl.to("#pQ2", {scale: 0.6, y: -110, autoAlpha: 0, duration: 0.3, ease: "power3.in"}, @potribna-0.08);
  tl.set("#gD", {autoAlpha: 0}, @potribna+0.3);""")


# ===========================================================================
# E · near — the Claude subscription, the cloud, faster, 20¢ a reel
def memb(mid, x, y):
    return ('<div class="memb hide" id="%s" style="left:%dpx;top:%dpx;width:520px;height:320px">'
            '%s<div class="nm">Claude</div><div class="emv"></div>'
            '<div class="chp" id="%sC"><svg viewBox="0 0 24 24">%s</svg>підписка</div>'
            '<div class="shc"><div class="sheen"></div></div></div>'
            % (mid, x, y, g.mark("claude"), mid, STROKES["check"]))


@beat
def e_cost():
    cab = ('<svg class="cab abs" width="1080" height="700" style="left:0;top:0">'
           '<path class="tube hide" id="eT" d="M632 330 C 680 330 712 312 760 312"/>'
           '<path class="core hide" id="eC" d="M632 330 C 680 330 712 312 760 312"/>'
           '<g class="pkg"><path class="pkt" id="eP" style="opacity:0" d="M632 330 C 680 330 712 312 760 312"/></g></svg>')
    L.append('<div class="g full" id="gE">' + cab + memb("eM", 110, 170)
             + tile("eCl", 220, 760, 200, "pearl", stroke("cloud"))
             + tile("eBt", 96, 924, 160, "jelly", stroke("bolt"), extra_cls="circ")
             + tile("eCo", 170, 640, 425, "jelly", '<span class="wmark" style="font-size:66px;color:#fff">20¢</span>',
                    extra_cls="circ coin")
             + '</div>')
    sfx("pop", T["potribna"], -2)
    sfx("whoosh-short", T["khmari2"] - 0.05, -3)
    sfx("kaching", T["d20"] + 0.03)
    return js("""
  tl.set("#gE", {autoAlpha: 1}, @potribna-0.1);
  arr("#eM", @potribna-0.05, {s: 0.55, y: 40});
  tl.fromTo("#eMC", {autoAlpha: 0, scale: 0.5}, {autoAlpha: 1, scale: 1, duration: 0.5, ease: POP}, @pidpyska);
  shn("#eM .sheen", @pidpyska+0.1);
  arr("#eCl", @khmari2-0.1, {s: 0.4, y: 30}); G.ripple("#eClR", @khmari2+0.2);
  tl.set(["#eT", "#eC"], {autoAlpha: 1}, @khmari2+0.05);
  draw2("eT", @khmari2+0.05, 0.35); draw2("eC", @khmari2+0.05, 0.35);
  G.packet("eP", @khmari2+0.45, 0.45);
  G.bump("#eCl", @rekom);
  arr("#eBt", @shvydshe-0.05, {s: 0.3, y: 20, d: 0.6}); G.ripple("#eBtR", @shvydshe+0.2);
  arr("#eCo", @d20-0.05, {s: 0.3, y: 30, d: 0.7}); G.ripple("#eCoR", @d20+0.25);
  shn("#eCo .sheen", @d20+0.2);
  tl.set("#gE", {autoAlpha: 0}, @tobto+0.6);""")


# ===========================================================================
# F · OVER — 40 reels -> ≈ 8 € a month; 30 € for one reel to an editor
CX0, CY0, CW, CH, CG = 29, 120, 112, 199, 18


@beat
def f_compare():
    grid = "".join('<div class="rl hide" id="rl%d" style="left:%dpx;top:%dpx"></div>'
                   % (i, CX0 + (i % 8) * (CW + CG), CY0 + (i // 8) * (CH + CG)) for i in range(40))
    sl = ('<div class="sheet hide" id="hSL" style="left:310px;top:200px;width:460px;height:1000px">'
          '<div class="cm t-micro" style="top:64px">40 РІЛЗІВ · МІСЯЦЬ</div>'
          '<div class="cm" style="top:128px"><span class="t-big">8 €</span></div>'
          '<div class="cm t-sub" style="top:330px">на місяць</div>'
          '<div class="bar lo" id="hBL" style="height:150px"></div>'
          '<div class="shc"><div class="sheen"></div></div></div>')
    sr = ('<div class="sheet hide" id="hSR" style="left:560px;top:200px;width:460px;height:1000px">'
          '<div class="cm t-micro" style="top:64px">1 РІЛЗ</div>'
          '<div class="cm" style="top:128px"><span class="t-big">30 €</span></div>'
          '<div class="cm t-sub" style="top:330px"><span class="who" id="hWho">%sмонтажеру</span></div>'
          '<div class="bar hi" id="hBR" style="height:560px"></div>'
          '<div class="shc"><div class="sheen"></div></div></div>'
          % ('<svg viewBox="0 0 24 24">%s</svg>' % STROKES["person"]))
    L.append('<div class="g full" id="gF">' + TKG + grid + sl + sr + '</div>')
    sfx("whoosh-short", T["tobto"] - 0.08)
    sfx("kaching", T["v8"] + 0.03)
    sfx("pop", T["t30"] + 0.03)
    return js("""
  G.irisOpen("#gF", @tobto-0.08, 725, 510, 0.6);
  drift1("#gF", @tobto, @montazh+0.8-@tobto);
  tl.fromTo(".rl", {autoAlpha: 0, scale: 0.3}, {autoAlpha: 1, scale: 1, duration: 0.5, ease: POP,
            stagger: {each: 0.018, grid: [5, 8], from: "center"}}, @s40-0.05);
  tl.to(".rl", {x: function (i) { return 540 - (%d + (i %% 8) * %d + 56); },
                y: function (i) { return 700 - (%d + Math.floor(i / 8) * %d + 100); },
                scale: 0.15, autoAlpha: 0, duration: 0.45, ease: "power3.in", stagger: {each: 0.006, from: "random"}},
        @plius-0.12);
  arr("#hSL", @plius+0.15, {s: 0.7, y: 40});
  tl.fromTo("#hBL", {scaleY: 0}, {scaleY: 1, duration: 0.7, ease: SP}, @v8);
  shn("#hSL .sheen", @v8+0.1);
  tl.to("#hSL", {x: -250, duration: 0.6, ease: SP}, @porivn-0.05);
  arr("#hSR", @porivn+0.02, {s: 0.7, x: 60, y: 40});
  tl.fromTo("#hBR", {scaleY: 0}, {scaleY: 1, duration: 0.9, ease: SP}, @t30);
  tl.fromTo("#hWho", {autoAlpha: 0, y: 14}, {autoAlpha: 1, y: 0, duration: 0.4, ease: SP}, @montazh-0.05);
  G.irisClose("#gF", @montazh+0.55, 540, 262, 0.5);""" % (CX0, CW + CG, CY0, CH + CG))


# ===========================================================================
# G · Q3 — the post flips up out of the iris
@beat
def g_q3():
    L.append('<div class="g full" id="gG">' + post("pQ3", 3) + '</div>')
    sfx("whoosh-short", T["montazh"] + 0.55, -3)
    return js("""
  tl.set("#gG", {autoAlpha: 1}, @montazh+0.6);
  gsap.set("#pQ3", {transformPerspective: 1500, transformOrigin: "50% 0%"});
  tl.fromTo("#pQ3", {autoAlpha: 0, rotationX: -100}, {autoAlpha: 1, rotationX: 0, duration: 0.9, ease: FLIP}, @montazh+0.62);
  tl.set("#pQ3", {autoAlpha: 1}, @montazh+0.75);
  bout("#pQ3", @ni2-0.08, 10, 0.25);
  tl.set("#gG", {autoAlpha: 0}, @ni2+0.25);""")


# ===========================================================================
# H · near — «Ні, кодити не потрібно» -> files + wishes out, a reel back. «Все.»
@beat
def h_chat():
    thumbs = "".join('<div class="fth" style="left:%dpx;top:20px"></div>' % (30 + i * 120) for i in range(3))
    b1 = '<div class="bub hide" id="hB1" style="left:610px;top:120px;width:400px;height:190px">%s</div>' % thumbs
    b2 = ('<div class="bub hide" id="hB2" style="left:560px;top:330px;width:450px;height:150px">'
          '<i style="left:36px;top:36px;width:360px"></i><i style="left:36px;top:72px;width:300px"></i>'
          '<i style="left:36px;top:108px;width:190px"></i></div>')
    rc = ('<div class="rcard hide" id="hRc" style="left:100px;top:140px;width:240px;height:426px">'
          '<div class="th"></div><i style="bottom:56px;width:150px"></i><i style="bottom:28px;width:100px;height:14px"></i>'
          '<div class="shc"><div class="sheen"></div></div></div>')
    code = ('<div class="tw hide" id="hCd" style="left:430px;top:180px;width:220px;height:220px"><div class="inkt">&lt;/&gt;</div></div>'
            '<svg class="abs" width="1080" height="700" style="left:0;top:0;overflow:visible">'
            '<path class="strike hide" id="hSt" d="M400 420 L680 160"/></svg>')
    L.append('<div class="g full" id="gH">' + code + b1 + b2 + rc
             + tile("hOk", 104, 290, 104, "jelly", stroke("check"), extra_cls="circ") + '</div>')
    sfx("click", T["ne"] + 0.05, -2)
    sfx("pop", T["videof"] + 0.02, -2)
    sfx("ping", T["hotovyi"] + 0.02, -3)
    sfx("pop", T["vse"] + 0.02)
    return js("""
  tl.set("#gH", {autoAlpha: 1}, @ni2-0.1);
  arr("#hCd", @ni2-0.05, {s: 0.4, y: 30, d: 0.7});
  tl.set("#hSt", {autoAlpha: 1}, @ne);
  draw2("hSt", @ne, 0.25);
  G.haptic("#hCd", @ne+0.25);
  bout(["#hCd", "#hSt"], @prosto-0.1, 10, 0.25);
  arr("#hB1", @videof-0.08, {s: 0.6, x: 60, y: 30});
  tl.fromTo("#hB1 .fth", {autoAlpha: 0, scale: 0.4}, {autoAlpha: 1, scale: 1, duration: 0.45, ease: POP, stagger: 0.08}, @videof+0.05);
  arr("#hB2", @pobazh-0.08, {s: 0.6, x: 60, y: 30});
  tl.fromTo("#hB2 i", {scaleX: 0, transformOrigin: "0% 50%"}, {scaleX: 1, duration: 0.4, ease: "power2.out", stagger: 0.1}, @pobazh+0.1);
  tl.to(["#hB1", "#hB2"], {y: -20, autoAlpha: 0.55, duration: 0.4, ease: SP}, @otrym);
  arr("#hRc", @hotovyi-0.1, {s: 0.5, x: -60, y: 30});
  shn("#hRc .sheen", @hotovyi+0.2);
  arr("#hOk", @vse-0.03, {s: 0.3, y: 10, d: 0.6}); G.ripple("#hOkR", @vse+0.2);
  bout("#gH", @q4s-0.12, 10, 0.25);""")


# ===========================================================================
# I · Q4 — a post with replies piling under it
def reply(rid, x, y, w, av, bar):
    return ('<div class="rep hide" id="%s" style="left:%dpx;top:%dpx;width:%dpx">'
            '<div class="ra"><img src="assets/threads/av%d.png" alt=""></div>'
            '<img class="rh" src="assets/threads/h%d.png" alt=""><i style="width:%dpx"></i></div>'
            % (rid, x, y, w, av, av, bar))


@beat
def i_q4():
    L.append('<div class="g full" id="gI"><div class="thl hide" id="iTl" style="left:146px;top:378px;height:160px"></div>'
             + post("pQ4", 4, y=90)
             + reply("iR1", 190, 396, 820, 8, 520) + reply("iR2", 190, 498, 820, 9, 380) + '</div>')
    sfx("pop", T["q4s"] - 0.05, -2)
    sfx("click-soft", T["tsezaim"] + 0.02, -2)
    return js("""
  tl.set("#gI", {autoAlpha: 1}, @q4s-0.15);
  arr("#pQ4", @q4s-0.12, {s: 0.8, y: 40, ease: SOFT});
  shn("#pQ4 .sheen", @q4s+0.4);
  tl.fromTo("#iTl", {autoAlpha: 0, scaleY: 0}, {autoAlpha: 1, scaleY: 1, duration: 0.5, ease: "power2.out"}, @tsezaim-0.1);
  arr("#iR1", @tsezaim, {s: 0.6, y: 30, d: 0.7});
  arr("#iR2", @zapysu+0.38, {s: 0.6, y: 30, d: 0.7});
  bout("#gI", @sam-0.1, 10, 0.28);""")


# ===========================================================================
# J · near — 30-40 хв, her one minute, then her own checklist
@beat
def j_time():
    shelf = ('<div class="dglass edge hide" id="jS" style="left:70px;top:170px;width:940px;height:300px">'
             '<div class="trk2 bg" style="left:170px;top:190px;width:600px"></div>'
             '<div class="trk2 fl" id="jF" style="left:170px;top:190px;width:600px"></div>'
             '<div class="trk2 cl hide" id="jC" style="left:170px;top:190px;width:600px"></div>'
             '<div class="trk2 sl hide" id="jSl" style="left:170px;top:190px;width:46px"></div>'
             '</div>')
    rows = ""
    for i, w in enumerate((420, 350, 470)):
        y = 70 + i * 96
        rows += ('<div class="cbx" style="left:50px;top:%dpx"><div class="cbf" id="jcb%d">'
                 '<svg viewBox="0 0 24 24"><path id="jcp%d" d="M5.4 12.6l4.3 4.3 8.9-9.5"/></svg></div></div>'
                 '<i style="left:136px;top:%dpx;width:%dpx"></i>' % (y, i, i, y + 16, w))
    lst = ('<div class="lst hide" id="jL" style="left:190px;top:160px;width:700px;height:370px">%s'
           '<div class="shc"><div class="sheen"></div></div></div>' % rows)
    L.append('<div class="g full" id="gJ">' + shelf
             + tile("jRec", 110, 120, 315, "jelly", stroke("rec"), extra_cls="circ", ring=False)
             + tile("jOk", 110, 850, 315, "pearl", stroke("check"), extra_cls="circ")
             + tile("jCd", 76, 502, 339, "jelly", g.mark("claude"), ring=False)
             + '<div class="pill hide" id="jP" style="left:440px;top:200px">30–40 хв</div>'
             + '<div class="pill hot hide" id="jP1" style="left:200px;top:200px">1 хв</div>'
             + tile("jUp", 64, 208, 420, "jelly", stroke("up"), extra_cls="circ", ring=False)
             + lst + '</div>')
    sfx("click-soft", T["t3040"] + 0.02)
    sfx("click", T["khvylynu"] + 0.02, -2)
    sfx("click-soft", T["zaimatys"] + 0.2, -3)
    return js("""
  tl.set("#gJ", {autoAlpha: 1}, @sam-0.08);
  arr("#jS", @sam-0.05, {s: 0.85, y: 30});
  arr("#jRec", @sam+0.05, {s: 0.4, y: 20, d: 0.6});
  arr("#jOk", @sam+0.2, {s: 0.4, y: 20, d: 0.6});
  tl.fromTo("#jF", {scaleX: 0}, {scaleX: 1, duration: 1.3, ease: "power2.inOut"}, @tryvaie-0.1);
  G.ripple("#jOkR", @tryvaie+1.2);
  arr("#jP", @t3040-0.05, {s: 0.5, y: 20, d: 0.6});
  /* not her work: the bar turns into Claude's time, her sliver is one minute */
  tl.fromTo("#jC", {autoAlpha: 0}, {autoAlpha: 1, duration: 0.35}, @aktyvna-0.2);
  arr("#jCd", @aktyvna-0.1, {s: 0.3, y: 10, d: 0.6});
  tl.fromTo("#jSl", {autoAlpha: 0, scaleX: 0.2, transformOrigin: "0% 50%"}, {autoAlpha: 1, scaleX: 1, duration: 0.5, ease: SP}, @khvylynu-0.6);
  bout("#jP", @khvylynu-0.2, 8, 0.2);
  arr("#jP1", @khvylynu-0.03, {s: 0.4, y: 20, d: 0.6});
  arr("#jUp", @zavant-0.05, {s: 0.3, y: -10, d: 0.6});
  G.bump("#jUp", @zavant+0.6);
  bout(["#jS", "#jRec", "#jOk", "#jCd", "#jP1", "#jUp"], @i58-0.15, 10, 0.28);
  arr("#jL", @i58-0.02, {s: 0.7, y: 40});
  [["#jcb0", @zaimatys+0.2], ["#jcb1", @svoimy+0.2], ["#jcb2", @spravamy+0.2]].forEach(function (p, i) {
    tl.fromTo(p[0], {autoAlpha: 0, scale: 0.4}, {autoAlpha: 1, scale: 1, duration: 0.4, ease: POP}, p[1]);
    draw2("jcp" + i, p[1] + 0.06, 0.3);
  });
  bout("#gJ", @q5s-0.2, 10, 0.25);""")


# ===========================================================================
# K · Q5 — the feed scrolls up and stops on the question
def ghost(gid, av, y, bars):
    body = '<div class="tx">%s</div>' % "".join('<i class="gbar" style="width:%dpx"></i>' % b for b in bars)
    return post(gid, 0, x=0, y=y, text=body, av=av, feed=True)


@beat
def k_q5():
    col = (ghost("kG1", 3, 0, (620, 430)) + ghost("kG2", 6, 262, (700, 520))
           + post("pQ5", 5, x=0, y=524, feed=True))
    L.append('<div class="g full" id="gK"><div class="feed hide" id="kW" style="left:70px;top:100px;width:940px;height:330px">'
             '<div class="fcol" id="kCol">%s</div></div></div>' % col)
    sfx("whoosh-short", T["q5s"] - 0.15, -2)
    return js("""
  tl.set("#gK", {autoAlpha: 1}, @q5s-0.3);
  tl.set(["#kG1", "#kG2", "#pQ5"], {autoAlpha: 1}, 0);
  arr("#kW", @q5s-0.28, {s: 0.85, y: 30, d: 0.7});
  tl.fromTo("#kCol", {y: 120}, {y: -502, duration: 0.95, ease: SOFT}, @q5s-0.2);
  bout("#gK", @absol-0.1, 10, 0.28);""")


# ===========================================================================
# L · near — «Абсолютно»: pauses close, subtitles, music, colour
WV = [42, 64, 30, 72, 50, 80, 38, 58, 26, 70, 46, 62, 34, 76, 54, 40, 66, 30, 58, 48, 72, 36, 60, 44, 28]


@beat
def l_edit():
    # waveform in three segments separated by two pauses
    segs = [(0, 8), (8, 17), (17, 25)]
    x0, step, gw = 140, 22, 70
    wv = ""
    gaps = ""
    for si, (a, b) in enumerate(segs):
        bars = "".join('<div class="wv" style="left:%dpx;top:%dpx;height:%dpx"></div>'
                       % ((i - a) * step, 40 - h // 2, h) for i, h in enumerate(WV[a:b], a))
        sx = x0 + a * step + si * gw
        wv += '<div class="abs" id="lW%d" style="left:%dpx;top:0px">%s</div>' % (si, sx, bars)
        if si < 2:
            gx = x0 + b * step + si * gw - 6
            gaps += '<div class="gap" id="lGp%d" style="left:%dpx;top:2px;width:%dpx;height:76px"></div>' % (si, gx, gw)
    caps = "".join('<div class="cpl" style="left:%dpx;top:22px;width:%dpx"></div>' % (x, w)
                   for x, w in ((140, 120), (276, 160), (452, 96), (564, 180), (760, 110)))
    mus = ('<svg class="abs" width="800" height="80" style="left:140px;top:0;overflow:visible">'
           '<path class="mus" id="lMu" d="M0 40 C 40 0, 80 0, 120 40 S 200 80, 240 40 S 320 0, 360 40 S 440 80, 480 40 '
           'S 560 0, 600 40 S 680 80, 720 40"/></svg>')
    card = ('<div class="dglass edge hide" id="lC" style="left:70px;top:110px;width:940px;height:470px">'
            '<div class="tln" style="left:0;top:28px;width:940px;height:80px">'
            '<div class="trh">Aa</div><div id="lCp">%s</div></div>'
            '<div class="tln" style="left:0;top:136px;width:940px;height:80px"><div class="trh">%s</div>%s%s</div>'
            '<div class="tln" style="left:0;top:244px;width:940px;height:80px"><div class="trh">%s</div>%s</div>'
            '<div class="tln" style="left:0;top:352px;width:940px;height:80px"><div class="trh">%s</div>'
            '<div class="grd0" style="left:140px;top:12px;width:760px"></div>'
            '<div class="grd1" id="lG1" style="left:140px;top:12px;width:760px"></div></div>'
            '</div>' % (caps, '<svg viewBox="0 0 24 24">%s</svg>' % STROKES["wave"], gaps, wv,
                        '<svg viewBox="0 0 24 24">%s</svg>' % STROKES["note"], mus,
                        '<svg viewBox="0 0 24 24">%s</svg>' % STROKES["drop"]))
    L.append('<div class="g full" id="gL">' + card + '</div>')
    sfx("pop", T["absol"], -3)
    sfx("pop", T["muzyku"] + 0.02, -3)
    sfx("whoosh-short", T["kolor"] + 0.02, -4)
    return js("""
  tl.set("#gL", {autoAlpha: 1}, @absol-0.1);
  arr("#lC", @absol-0.08, {s: 0.85, y: 30});
  tl.fromTo("#lCp .cpl", {autoAlpha: 0, scaleX: 0.3, transformOrigin: "0%% 50%%"},
            {autoAlpha: 1, scaleX: 1, duration: 0.35, ease: SP, stagger: 0.09}, @absol+0.15);
  tl.to(["#lGp0", "#lGp1"], {scaleX: 0, autoAlpha: 0, duration: 0.35, ease: "power2.in"}, @absol+0.4);
  tl.to("#lW1", {x: -%d, duration: 0.4, ease: SP}, @absol+0.45);
  tl.to("#lW2", {x: -%d, duration: 0.4, ease: SP}, @absol+0.45);
  tl.set("#lMu", {autoAlpha: 1}, 0);
  draw2("lMu", @muzyku-0.05, 0.7);
  tl.fromTo("#lG1", {clipPath: "inset(0px 100%% 0px 0px round 18px)"}, {clipPath: "inset(0px 0%% 0px 0px round 18px)",
            duration: 0.8, ease: "power2.inOut"}, @kolor);
  bout("#gL", @q6s-0.12, 10, 0.25);""" % (70, 140))


# ===========================================================================
# M · Q6 — zooms in from depth; the heart fills on «Так»
@beat
def m_q6():
    L.append('<div class="g full" id="gM">' + post("pQ6", 6, heart_fill=True) + '</div>')
    sfx("pop", T["tak"] + 0.05, -1)
    return js("""
  tl.set("#gM", {autoAlpha: 1}, @q6s-0.12);
  arr("#pQ6", @q6s-0.1, {s: 0.3, y: 0, blur: 18, d: 0.95, ease: SOFT});
  tl.fromTo("#pQ6H", {autoAlpha: 0, scale: 0.2, transformOrigin: "50% 60%"}, {autoAlpha: 1, scale: 1, duration: 0.5, ease: POP}, @tak+0.03);
  tl.set("#pQ6L0", {autoAlpha: 0}, @tak+0.05); tl.set("#pQ6L1", {autoAlpha: 1}, @tak+0.05);
  G.bump("#pQ6", @tak+0.05);
  bout("#gM", @prosto2-0.35, 10, 0.25);""")


# ===========================================================================
# N · near — she writes what to change, it redoes; each redo = a full render;
#     15¢ -> копійки
@beat
def n_redo():
    bub = ('<div class="bub hide" id="nB" style="left:520px;top:150px;width:490px;height:150px">'
           '<div id="nBi" style="position:absolute;inset:0">'
           '<i style="left:36px;top:40px;width:400px"></i><i style="left:36px;top:84px;width:280px"></i></div></div>')
    rc = ('<div class="rcard hide" id="nRc" style="left:150px;top:140px;width:240px;height:426px">'
          '<div class="th"></div><div class="th v2 hide" id="nTh2"></div>'
          '<i style="bottom:56px;width:150px"></i><i style="bottom:28px;width:100px;height:14px"></i>'
          '<div class="shc"><div class="sheen"></div></div></div>')
    trk = ('<div class="trk2 bg hide" id="nTb" style="left:450px;top:250px;width:520px"></div>'
           '<div class="trk2 fl hide" id="nTf" style="left:450px;top:250px;width:520px"></div>')
    coins = "".join(tile("nC%d" % i, 110, 450 + i * 140, 330, "jelly",
                         '<span class="wmark" style="font-size:52px;color:#fff">¢</span>', extra_cls="circ coin",
                         ring=False) for i in range(2))
    tag = tile("nTag", 200, 560, 230, "jelly", '<span class="wmark" style="font-size:76px;color:#fff">15¢</span>',
               extra_cls="circ coin")
    L.append('<div class="g full" id="gN">' + bub + rc
             + tile("nRd", 100, 340, 110, "jelly", stroke("redo"), extra_cls="circ", ring=False)
             + trk + coins + tag + '</div>')
    sfx("typing", T["prosto2"] + 0.05, -3)
    sfx("whoosh-short", T["pererob"] + 0.02, -3)
    sfx("click-soft", T["oplach"] + 0.05)
    sfx("kaching", T["p15"] + 0.02, -2)
    return js("""
  tl.set("#gN", {autoAlpha: 1}, @prosto2-0.3);
  arr("#nB", @prosto2-0.25, {s: 0.6, x: 60, y: 30});
  tl.fromTo("#nBi", {clipPath: "inset(0px 100% 0px 0px)"}, {clipPath: "inset(0px 0% 0px 0px)", duration: 1.3, ease: "none"}, @prosto2+0.1);
  arr("#nRc", @pererob-0.6, {s: 0.5, x: -60, y: 30});
  arr("#nRd", @pererob-0.05, {s: 0.3, y: 10, d: 0.6});
  tl.to("#nRd", {rotation: 360, duration: 0.9, ease: "power2.inOut"}, @pererob+0.1);
  tl.to("#nRc", {scaleX: 0, duration: 0.14, ease: "power2.in"}, @pererob+0.25);
  tl.set("#nTh2", {autoAlpha: 1}, @pererob+0.39);
  tl.to("#nRc", {scaleX: 1, duration: 0.4, ease: SP}, @pererob+0.39);
  /* every redo is a whole render: the bar fills, a coin; from zero again, another coin */
  bout("#nB", @kozhna-0.1, 10, 0.25);
  tl.set("#nTf", {autoAlpha: 1}, @kozhna);
  bin("#nTb", @kozhna, 8, 0.3);
  tl.fromTo("#nTf", {scaleX: 0}, {scaleX: 1, duration: 0.8, ease: "power1.inOut"}, @pererobka-0.2);
  arr("#nC0", @oplach+0.02, {s: 0.3, y: -60, d: 0.6});
  tl.to("#nRd", {rotation: 720, duration: 0.7, ease: "power2.inOut"}, @nulia-0.3);
  tl.set("#nTf", {scaleX: 0}, @nulia+0.02);
  tl.to("#nTf", {scaleX: 1, duration: 0.55, ease: "power1.inOut"}, @nulia+0.04);
  arr("#nC1", @nulia+0.3, {s: 0.3, y: -60, d: 0.6});
  /* 15¢ a render: the coins become one small tag, and it shrinks to nothing much */
  bout(["#nTb", "#nTf"], @p15-0.3, 8, 0.25);
  tl.to(["#nC0", "#nC1"], {x: function (i) { return 155 - i * 140; }, y: -55, scale: 0.4, autoAlpha: 0, duration: 0.35, ease: "power3.in"}, @p15-0.3);
  arr("#nTag", @p15-0.04, {s: 0.4, y: 0, d: 0.7}); G.ripple("#nTagR", @p15+0.2);
  tl.to("#nTag", {scale: 0.34, y: 70, duration: 0.6, ease: SP}, @kopiiky);
  tl.to(["#nRc", "#nRd"], {autoAlpha: 0.0, duration: 0.3}, @zvert-0.2);
  bout("#nTag", @zvert+0.1, 10, 0.3);
  tl.set("#gN", {autoAlpha: 0}, @q7s-0.2);""")


# ===========================================================================
# O · Q7 — slides in from the left
@beat
def o_q7():
    L.append('<div class="g full" id="gO">' + post("pQ7", 7) + '</div>')
    sfx("whoosh-short", T["q7s"] - 0.15, -2)
    return js("""
  tl.set("#gO", {autoAlpha: 1}, @q7s-0.2);
  tl.fromTo("#pQ7", {autoAlpha: 0, x: -1150, rotation: -5}, {autoAlpha: 1, x: 0, rotation: 0, duration: 0.85, ease: SOFT}, @q7s-0.18);
  shn("#pQ7 .sheen", @q7s+0.5);
  tl.to("#pQ7", {x: 260, autoAlpha: 0, duration: 0.3, ease: "power3.in"}, @tak2-0.12);
  tl.set("#gO", {autoAlpha: 0}, @tak2+0.2);""")


# ===========================================================================
# P · near — any style: the reel flips through looks; style.md sets hers
def skin(n, sid):
    return ('<div class="skin sk%d%s" id="%s">'
            '<i style="left:30px;top:40px;width:120px;height:24px"></i>'
            '<i style="left:30px;top:86px;width:180px;height:44px"></i>'
            '<i style="left:30px;top:144px;width:150px;height:44px"></i>'
            '<i style="left:30px;top:240px;width:200px;height:16px;opacity:.6"></i>'
            '<i style="left:30px;top:268px;width:160px;height:16px;opacity:.6"></i>'
            '<i style="left:30px;top:296px;width:180px;height:16px;opacity:.6"></i>'
            '<i style="left:30px;top:370px;width:130px;height:52px;border-radius:26px"></i></div>'
            % (n, "" if n == 1 else " hide", sid))


@beat
def p_style():
    card = ('<div class="rcard hide" id="pRc" style="left:470px;top:100px;width:270px;height:470px">%s'
            '<div class="shc"><div class="sheen"></div></div></div>'
            % "".join(skin(n, "pSk%d" % n) for n in (1, 2, 0, 3)))
    cab = ('<svg class="cab abs" width="1080" height="700" style="left:0;top:0">'
           '<path class="tube hide" id="pT" d="M330 330 C 380 330 420 335 470 335"/>'
           '<path class="core hide" id="pC" d="M330 330 C 380 330 420 335 470 335"/>'
           '<g class="pkg"><path class="pkt" id="pP" style="opacity:0" d="M330 330 C 380 330 420 335 470 335"/></g></svg>')
    L.append('<div class="g full" id="gP">' + cab + card
             + tile("pDoc", 190, 130, 235, "pearl", stroke("doc"))
             + '<div class="dlab hide" id="pDl" style="left:95px;top:440px">style.md</div></div>')
    sfx("click-soft", T["budy"] + 0.02)
    sfx("sparkle", T["sama"] + 0.02, -3)
    return js("""
  tl.set("#gP", {autoAlpha: 1}, @tak2-0.1);
  arr("#pRc", @tak2-0.05, {s: 0.55, y: 30});
  function flip(a, b, t) {
    tl.to("#pRc", {scaleX: 0, duration: 0.12, ease: "power2.in"}, t);
    tl.set(a, {autoAlpha: 0}, t + 0.12); tl.set(b, {autoAlpha: 1}, t + 0.12);
    tl.to("#pRc", {scaleX: 1, duration: 0.32, ease: SP}, t + 0.12);
  }
  flip("#pSk1", "#pSk2", @budy);
  flip("#pSk2", "#pSk0", @styliem);
  arr("#pDoc", @bo-0.05, {s: 0.4, y: 30}); G.ripple("#pDocR", @styl2+0.1);
  bin("#pDl", @bo+0.1, 8, 0.3);
  tl.set(["#pT", "#pC"], {autoAlpha: 1}, @zadaiesh-0.25);
  draw2("pT", @zadaiesh-0.25, 0.3); draw2("pC", @zadaiesh-0.25, 0.3);
  G.packet("pP", @zadaiesh+0.1, 0.4);
  flip("#pSk0", "#pSk3", @sama-0.05);
  shn("#pRc .sheen", @sama+0.25);
  tl.set("#gP", {autoAlpha: 0}, @q8s+0.4);""")


# ===========================================================================
# Q · OVER — iris out of style.md: Q8 huge -> header; subscription; two laptops
@beat
def q_start():
    sub = memb("uM", 280, 340)
    strike = ('<svg class="abs" width="1080" height="1920" style="left:0;top:0;overflow:visible">'
              '<path class="strike hide" id="uX" d="M350 760 L530 930 M530 760 L350 930"/></svg>')
    spin = ('<svg class="spin hide" id="uSp" viewBox="0 0 160 160" width="160" height="160" '
            'style="left:590px;top:750px"><circle cx="80" cy="80" r="66"/></svg>')
    coins = "".join(tile("uE%d" % i, 96, 700 + i * 110, 900, "jelly",
                         '<span class="wmark" style="font-size:52px;color:#fff">€</span>', extra_cls="circ coin",
                         ring=False) for i in range(3))
    wal = ('<div class="wal hide" id="uW" style="left:560px;top:1000px;width:470px;height:220px">'
           '<div class="t">API</div><div class="bb"></div><div class="bf" id="uWf"></div>'
           '<div class="shc"><div class="sheen"></div></div></div>')
    L.append('<div class="g full" id="gQ">' + TKG
             + post("pQ8", 8, x=40, y=520, w=1000)
             + sub
             + tile("uL1", 220, 90, 730, "pearl", stroke("laptop"))
             + tile("uBo", 96, 250, 690, "jelly", stroke("bolt"), extra_cls="circ")
             + tile("uC1", 220, 330, 730, "clear", stroke("cloud"), ring=False)
             + tile("uL2", 220, 560, 730, "pearl", stroke("laptop"), ring=False)
             + spin
             + tile("uC2", 200, 830, 740, "pearl", stroke("cloud"))
             + wal + coins + strike + '</div>')
    sfx("whoosh-short", T["sama"] + 0.3, -2)
    sfx("pop", T["q8s"] + 0.02, -2)
    sfx("whoosh-short", T["zvych"] - 0.05, -4)
    sfx("click", T["znadob"] - 0.1, -2)
    sfx("kaching", T["ievro3"] + 0.02, -1)
    sfx("whoosh-short", T["api"] + 0.45, -3)
    return js("""
  G.irisOpen("#gQ", @sama+0.32, 225, 330, 0.6);
  drift1("#gQ", @sama+0.3, @api+0.8-@sama);
  gsap.set("#pQ8", {transformOrigin: "50% 50%"});
  tl.fromTo("#pQ8", {autoAlpha: 0, scale: 0.6, y: 140}, {autoAlpha: 1, scale: 1.16, y: 0, duration: 0.85, ease: POP}, @q8s-0.08);
  shn("#pQ8 .sheen", @q8s+0.4);
  tl.to("#pQ8", {scale: 0.66, y: -415, duration: 0.7, ease: SP}, @zvych-0.1);
  arr("#uM", @zvych+0.05, {s: 0.55, y: 60});
  shn("#uM .sheen", @pidpyska2);
  /* a strong computer: no cloud needed */
  arr("#uL1", @yakshcho2, {s: 0.5, y: 40});
  arr("#uBo", @potuzh-0.05, {s: 0.3, y: 20, d: 0.6}); G.ripple("#uBoR", @potuzh+0.2);
  arr("#uC1", @render3-0.05, {s: 0.5, y: 40});
  tl.set("#uX", {autoAlpha: 1}, @znadob-0.15);
  draw2("uX", @znadob-0.15, 0.35);
  tl.to("#uC1", {autoAlpha: 0.35, duration: 0.3}, @znadob+0.2);
  /* an old one, like hers: the cloud does it, a few euros into the API wallet */
  arr("#uL2", @ayakshcho, {s: 0.5, y: 40});
  tl.fromTo("#uSp", {autoAlpha: 0, rotation: 0, transformOrigin: "50% 50%"}, {autoAlpha: 1, duration: 0.3}, @staren-0.3);
  tl.to("#uSp", {rotation: 260, duration: 1.6, ease: "none"}, @staren-0.3);
  bout("#uSp", @doved-0.2, 8, 0.25);
  arr("#uC2", @doved-0.05, {s: 0.5, y: 40}); G.ripple("#uC2R", @doved+0.3);
  arr("#uW", @doved+0.3, {s: 0.7, y: 40});
  tl.set("#uWf", {scaleX: 0}, 0);
  [0, 1, 2].forEach(function (i) {
    var t = @kilka-0.05 + i * 0.14;
    tl.fromTo("#uE" + i, {autoAlpha: 0, y: -160, scale: 0.6}, {autoAlpha: 1, y: 0, scale: 1, duration: 0.4, ease: "power2.in"}, t);
    tl.to("#uE" + i, {y: 150, scale: 0.4, autoAlpha: 0, duration: 0.3, ease: "power2.in"}, t + 0.42);
    tl.to("#uWf", {scaleX: 0.25 + i * 0.25, duration: 0.35, ease: SP}, t + 0.6);
  });
  shn("#uW .sheen", @api);
  G.irisClose("#gQ", @api+0.45, 540, 500, 0.5);""")


# ===========================================================================
# R · near — start with the subscription + $1
@beat
def r_dollar():
    L.append('<div class="g full" id="gR">' + memb("vM", 110, 170)
             + '<div class="pls hide" id="vPl" style="left:650px;top:290px">+</div>'
             + tile("vD", 200, 750, 230, "jelly", '<span class="wmark" style="font-size:84px;color:#fff">$1</span>',
                    extra_cls="circ coin")
             + '</div>')
    sfx("kaching", T["odnoho"] + 0.05, -2)
    sfx("pop", T["sprob"] + 0.1, -3)
    return js("""
  tl.set("#gR", {autoAlpha: 1}, @api+0.6);
  tl.fromTo("#vM", {autoAlpha: 0, scale: 1.35, x: 170, y: 170}, {autoAlpha: 1, scale: 1, x: 0, y: 0, duration: 0.8, ease: SP}, @api+0.62);
  bin("#vPl", @odnoho-0.25, 8, 0.25);
  arr("#vD", @odnoho-0.05, {s: 0.3, y: 30, d: 0.7}); G.ripple("#vDR", @odnoho+0.25);
  shn("#vD .sheen", @odnoho+0.2);
  G.bump("#vM", @sprob+0.1); G.bump("#vD", @sprob+0.2);
  shn("#vM .sheen", @sprob+0.15);
  bout("#gR", @sprob+0.82, 10, 0.25);""")


# ===========================================================================
# S · CTA — the comment types «design»; the first step lights; безкоштовно
@beat
def s_cta():
    bar = ('<div class="dglass edge cbar hide" id="wB" style="left:70px;top:400px;width:940px;height:130px;border-radius:65px">'
           '<div class="tw" style="left:22px;top:21px;width:88px;height:88px"><div class="clear">%s</div></div>'
           '<div class="ph" id="wPh">Додайте коментар…</div>'
           '<div class="ty hide" id="wTy">design</div>'
           '<div class="tw circ" id="wSn" style="left:826px;top:19px;width:92px;height:92px"><div class="jelly">%s</div></div>'
           '</div>' % (g.mark("instagram"), stroke("up")))
    steps = "".join('<div class="step hide" id="wS%d" style="left:%dpx;top:%dpx;height:%dpx;border-radius:%s"><div class="on" id="wO%d" style="border-radius:inherit"></div></div>'
                    % (i, 285 + i * 170, 350 - h, h, ("26px 0 0 0", "0", "0 26px 0 0")[i], i) for i, h in enumerate((80, 160, 240)))
    steps += tile("wMe", 76, 332, 192, "jelly", stroke("person"), extra_cls="circ", ring=False)
    L.append('<div class="g full" id="gS">' + steps + bar
             + '<div class="abs hide" id="wF" style="left:0;top:180px;width:1080px;display:flex;justify-content:center">'
             '<div class="free" style="position:relative">безкоштовно<div class="shc"><div class="sheen"></div></div></div></div></div>')
    sfx("pop", T["komentar"] - 0.05, -3)
    sfx("typing", T["design"] + 0.02, -3)
    sfx("click", T["design"] + 0.6)
    sfx("sparkle", T["bezk"] + 0.02, -2)
    return js("""
  tl.set("#gS", {autoAlpha: 1}, @komentar-0.4);
  arr("#wB", @komentar-0.35, {s: 0.8, y: 40});
  tl.set("#wPh", {autoAlpha: 0}, @design-0.02);
  tl.set("#wTy", {autoAlpha: 1}, @design-0.02);
  tl.fromTo("#wTy", {clipPath: "inset(0px 100% 0px 0px)"}, {clipPath: "inset(0px 0% 0px 0px)", duration: 0.42, ease: "steps(6)"}, @design-0.02);
  G.bump("#wSn", @design+0.6);
  [0, 1, 2].forEach(function (i) { arr("#wS" + i, @pokazhu-0.05 + i * 0.1, {s: 0.5, y: 40, d: 0.7}); });
  tl.fromTo("#wO0", {autoAlpha: 0}, {autoAlpha: 1, duration: 0.3}, @pershyi);
  G.bump("#wS0", @pershyi);
  tl.fromTo("#wMe", {autoAlpha: 0, y: -90, scale: 0.6}, {autoAlpha: 1, y: 0, scale: 1, duration: 0.55, ease: POP}, @pershyi-0.15);
  bout(["#wS0", "#wS1", "#wS2", "#wMe"], @bezk-0.2, 10, 0.22);
  gsap.set("#wF", {transformOrigin: "50% 50%"});
  arr("#wF", @bezk-0.04, {s: 0.4, y: 30, d: 0.7});
  shn("#wF .sheen", @bezk+0.3);""")


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


BLACKOUT = [span(T["q%ds" % n], T["q%de" % n]) for n in range(1, 9)] + [
    span(T["skily"], TE["skily"]),            # tile label says it
    span(T["stylemd"], TE["stylemd"]),
    span(T["render"], TE["khmari"]),
    span(T["tr30"], TE["tr30"]),              # the stopwatch counts to 30
    span(T["pidpyska"], TE["pidpyska"]),      # the card's chip says «підписка»
    span(T["d20"], TE["tsentiv"]),            # the coin says 20¢
    span(T["v8"], TE["ievro"]),               # 8 €
    span(T["t30"], TE["ievro2"]),             # 30 €
    span(T["t3040"], TE["khv2"]),             # 30–40 хв
    span(T["khvylynu"], TE["khvylynu"]),      # 1 хв
    span(T["p15"], TE["tsentakh"]),           # 15¢
    span(T["pidpyska2"], TE["pidpyska2"]),
    span(T["api"], TE["api"]),                # the wallet says API
    span(T["odnoho"], TE["dolara"]),          # $1
    span(T["design"], TE["design"]),          # the comment types it
    span(T["bezk"], DUR + 0.5),               # the chip says it
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
        title=u"Reel 31 — Відповіді про ШІ монтаж",
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
