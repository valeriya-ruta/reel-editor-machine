# -*- coding: utf-8 -*-
"""Reel 59 — «Які автоматизації зробити репетиторці?». Google x Excalidraw (STYLE.md §0b).

Layouts per STYLE.md §0c: mockups = move-down sheets (h 640-700), the
list board = halfscreen whiteboard sheet (h 940); her plate moves, never under a card.

A list reel: the running object is the WHITEBOARD LIST «Автоматизації
репетиторки» with four checkboxes. Every item is written onto the board, the
board closes onto that item and it is shown near (a Material card above her
head), then the board reopens out of that card, ticks the item and writes the
next one.

Chain:  NEAR the Threads question card -> it shrinks into a little sketch board
(a² + b² = c², chips «математика», «історія») -> OVER the whiteboard wipes in out
of it: title, four empty checkboxes, «1. CRM учнів + фінанси» -> board closes
onto row 1 -> NEAR the Claude card: connectors Notion / Google Drive, the
message «Оля заплатила 2000 за 4 уроки» types, a table row lands with a tick;
«Скільки я заробила?» -> dots -> «точна сума»; «приблизно» scribbled out -> OVER
board reopens out of the answer: tick 1, «2. Нагадування», Google Calendar +
SendPulse -> Claude -> chip «щоранку» -> board closes onto SendPulse -> NEAR
the Telegram bot: today's lessons, «Нагадую: сьогодні урок», «оплачені уроки
закінчились», the WayForPay button clicks -> OVER board reopens out of the
button: tick 2, «3. Афтеркер», Zoom/Meet -> Fathom -> транскрипт -> Claude +
скіл -> конспект + домашка -> SendPulse -> учню / батькам; tick 3, «4. Тести
НМТ» -> board closes onto row 4 -> NEAR a test card (chips: скіл «тест за
темою», Google Drive), the options turn into four coloured quiz tiles,
Kahoot pill, «вікторина!» -> CTA: the whole list again, all four ticked, with
«Зберегти» and «Переслати» pills.

usage: python3 build.py   (then: python3 ../tools/sfx.py mix 59)
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
from sketch import Sketch, sketch_css, SKETCH_JS  # noqa: E402

NN = "59"
CUT = json.load(io.open(os.path.join(ROOT, "work", "r" + NN, "cut.json"), encoding="utf-8"))
DUR = 83.450           # (2504 plate frames - 0.5) / 30
FPS = 30
k = Kit(width=1080, height=1920, fps=FPS, duration=DUR)
k.cap_font = "assets/fonts/ProductSans-Bold.ttf"
k.css(sketch_css())
sk = Sketch(seed=43)

NO_PAINT = [tuple(x) for x in CUT["no_paint"]]

CAPS = k.load_captions(os.path.join(ROOT, "work", "r" + NN, "captions.json"))


def fix(caps):
    def find(word, near):
        c = min((i for i, c in enumerate(caps) if c["w"] == word), key=lambda i: abs(caps[i]["s"] - near))
        assert abs(caps[c]["s"] - near) < 0.5, (word, near)
        return c
    # merges first (they shift nothing in time)
    i = find(u"По", 11.23)
    caps[i]["w"] = u"По-перше,"
    caps[i]["e"] = caps[i + 1]["e"]
    del caps[i + 1]
    edits = [
        (u"репетиторці?\"", 5.12, u"репетиторці?»"),
        (u"через", 8.24, u"чи"), (u"асторію,", 8.56, u"історії,"), (u"щоб", 9.60, u"що"),
        (u"складом.", 10.70, u"з Claude."),
        (u"надеюсь", 27.22, u"не десь"),
        (u"в", 31.32, u"В"), (u"конектору", 31.48, u"конекторі"), (u"гугл", 31.86, u"Google"),
        (u"календар", 32.13, u"Calendar"), (u"син", 32.77, u"SendPulse,"), (u"вклод", 33.45, u"в Claude"),
        (u"якийсь", 36.44, u"в кого"), (u"батькану", 38.22, u"батькам"),
        (u"а", 40.90, u"А"),
        (u"вейфорпей", 46.56, u"WayForPay"), (u"себе", 47.96, u"сам"),
        (u"aftercare.", 50.08, u"афтеркер."), (u"Урок", 51.42, u"урок"), (u"зумі", 51.82, u"Zoom"),
        (u"мід", 52.32, u"Meet"), (u"Фатум.", 52.98, u"Fathom."),
        (u"син", 58.51, u"SendPulse"),
        (u"Скіл", 65.85, u"скіл"), (u"формацію", 68.83, u"інформацію"), (u"NMT.", 69.33, u"НМТ,"),
        (u"То", 74.50, u"то"), (u"іде?", 74.75, u"є"), (u"Кахут", 75.87, u"Kahoot,"),
        (u"бікторину", 78.11, u"вікторину"), (u"кахуті.", 79.07, u"Kahoot."),
        (u"Збережи,", 80.02, u"збережи,"),
        (u"приблизно", 28.02, u"приблизно."), (u"Друге", 28.37, u"Друге,"), (u"шранку.", 35.17, u"щоранку,"),
        (u"батькам", 61.03, u"батькам."), (u"Третє", 49.13, u"Третє,"), (u"Четверте", 61.53, u"Четверте,"),
        (u"темою»", 66.77, u"темою»,"),
    ]
    for w, near, new in edits:
        caps[find(w, near)]["w"] = new
    drop = [(u"пульс", 32.99), (u"пусть", 58.71)]
    for w, near in drop:
        i = find(w, near)
        caps[i - 1]["e"] = caps[i]["e"]
        del caps[i]
    return caps


CAPS = fix(CAPS)
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
    return c["e"]


T = {
    "rubryka": S(u"рубрика", 0.99), "pytannia": S(u"питання", 1.49), "yaki": S(u"Які", 2.87),
    "repet": S(u"репетиторці", 5.12), "korotshe": S(u"Коротше", 5.90), "bula": S(u"була", 6.87),
    "matem": S(u"математики", 7.85), "istorii": S(u"історії", 8.56), "os": S(u"ось", 9.28),
    "nalasht": S(u"налаштувала", 10.10), "claude0": S(u"Claude", 10.70),
    "pershe": S(u"По-перше", 11.23), "crm": S(u"CRM", 12.32), "finansy": S(u"фінанси", 13.64),
    "pidkl": S(u"Підключаєш", 14.05), "notion": S(u"Notion", 15.44), "google": S(u"Google", 16.06),
    "pyshesh": S(u"пишеш", 17.70), "olia": S(u"Оля", 18.27), "uroky": S(u"уроки", 20.48),
    "vin": S(u"Він", 20.97), "vnosyt": S(u"вносить", 21.78), "oplatu": S(u"оплату", 22.26),
    "kintsi": S(u"кінці", 23.48), "pytannia2": S(u"питання", 24.24), "skilky": S(u"скільки", 24.73),
    "vidp": S(u"відповідає", 25.59), "tsyfroiu": S(u"цифрою", 26.19), "des": S(u"десь", 27.22),
    "pryblyzno": S(u"приблизно", 28.02),
    "druhe": S(u"Друге", 28.37), "nahad": S(u"нагадування", 29.10), "oplatu2": S(u"оплату", 30.80),
    "konektori": S(u"конекторі", 31.48), "calendar": S(u"Calendar", 32.13), "sendpulse": S(u"SendPulse", 32.77),
    "vclaude": S(u"Claude", 33.45), "zaplan": S(u"запланована", 34.03), "shchoranku": S(u"щоранку", 35.17),
    "dyvytsia": S(u"дивиться", 36.08), "kogo": S(u"кого", 36.44), "pyshe": S(u"пише", 37.38),
    "batkam": S(u"батькам", 38.22), "zakinch": S(u"закінчились", 41.72), "nahaduie": S(u"нагадує", 43.34),
    "oplatu3": S(u"оплату", 44.16), "yomu": S(u"йому", 44.92), "posyl": S(u"посилання", 46.06),
    "wfp": S(u"WayForPay", 46.56), "vidpr": S(u"відправляти", 47.42), "posyl2": S(u"посилання", 48.34),
    "tretie": S(u"Третє", 49.13), "after": S(u"афтеркер", 50.08), "urok": S(u"урок", 51.42),
    "zoom": S(u"Zoom", 51.82), "meet": S(u"Meet", 52.32), "zapysuie": S(u"записує", 52.50),
    "fathom": S(u"Fathom", 52.98), "konektor3": S(u"конектор", 54.18), "transkr": S(u"транскрипт", 55.36),
    "claude3": S(u"Claude", 55.83), "skil": S(u"скіл", 56.40), "konspekt": S(u"конспект", 57.15),
    "domashku": S(u"домашку", 57.52), "sp3": S(u"SendPulse", 58.51), "letyt": S(u"летить", 59.13),
    "uchniu": S(u"учню", 60.35), "batkam3": S(u"батькам", 61.03),
    "chetv": S(u"Четверте", 61.53), "testy": S(u"тести", 62.64), "nmt": S(u"НМТ", 63.90),
    "tobto2": S(u"Тобто", 64.50), "skil2": S(u"скіл", 65.85), "test": S(u"тест", 66.39),
    "natren": S(u"натренований", 67.65), "pliuse": S(u"плюс", 69.90), "drive2": S(u"Drive", 70.97),
    "yakshcho": S(u"якщо", 71.60), "porishav": S(u"порішав", 73.32), "azartom": S(u"азартом", 73.96),
    "kahoot": S(u"Kahoot", 75.87), "claude4": S(u"Claude", 76.67), "viktor": S(u"вікторину", 78.11),
    "kahoot2": S(u"Kahoot", 79.07), "tomu": S(u"Тому", 79.77), "zberezhy": S(u"збережи", 80.02),
    "pereshly": S(u"перешли", 81.66), "kolezi": S(u"колезі", 82.90),
    "dur": DUR,
}


def js(src):
    def rep(m):
        v = T[m.group(1)] + (float(m.group(2)) if m.group(2) else 0.0)
        return "%.3f" % v
    return re.sub(r"@(\w+)([+-]\d+(?:\.\d+)?)?", rep, src)


SFX = []


def sfx(name, t, db=0):
    if isinstance(t, str):
        t = float(js(t))
    SFX.append({"t": round(max(0.0, t), 3), "name": name, "db": db})


L = []
BEATS = []


def beat(fn):
    BEATS.append(fn)
    return fn


k.css("""
.hide { opacity: 0; visibility: hidden; }
.cap, #scrim { z-index: 60; }
.sk .sf { opacity: 0; visibility: hidden; }
.ab { position: absolute; }
.bub { position: absolute; padding: 22px 30px; border-radius: 30px; font-family: "GSans", sans-serif;
       font-size: 36px; font-weight: 500; line-height: 1.25; max-width: 620px; }
.bub.in { background: #f1f3f4; color: #202124; border-bottom-left-radius: 8px; }
.bub.me { background: #d3e3fd; color: #041e49; border-bottom-right-radius: 8px; }
.av { position: absolute; width: 64px; height: 64px; border-radius: 50%; display: grid; place-items: center;
      font-family: "GSans", sans-serif; font-weight: 700; font-size: 30px; color: #fff; }
.lbl { font-family: "GSans", sans-serif; font-size: 26px; font-weight: 700; letter-spacing: .14em;
       color: #5f6368; text-transform: uppercase; position: absolute; }
.row { position: absolute; display: flex; align-items: center; gap: 26px; font-family: "GSans", sans-serif; }
.hd { position: absolute; left: 122px; top: 34px; font-size: 34px; font-weight: 700; }
.hs { position: absolute; left: 122px; top: 76px; font-size: 24px; color: #5f6368; }
.sep { position: absolute; left: 0; right: 0; top: 124px; height: 2px; background: #e8eaed; }
.tbl { position: absolute; left: 36px; width: 808px; display: grid; grid-template-columns: 1.3fr 1fr 1fr;
       font-family: "GSans", sans-serif; font-size: 32px; color: #202124; }
.tbl div { padding: 14px 20px; border-bottom: 2px solid #e8eaed; }
.tbl .th { font-size: 24px; font-weight: 700; letter-spacing: .1em; color: #5f6368; text-transform: uppercase; }
.bpill { position: absolute; height: 96px; padding: 0 34px; font-size: 38px; font-weight: 700; }
.dot { display: inline-block; width: 30px; height: 30px; border-radius: 50%; }
.opt { position: absolute; left: 36px; width: 380px; height: 84px; border-radius: 18px; border: 2px solid #dadce0;
       display: flex; align-items: center; gap: 20px; padding: 0 24px; box-sizing: border-box;
       font-family: "GSans", sans-serif; font-size: 34px; color: #202124; }
.opt i { width: 30px; height: 30px; border-radius: 50%; border: 3px solid #5f6368; box-sizing: border-box; }
.kt { position: absolute; width: 392px; height: 104px; border-radius: 14px; display: flex; align-items: center;
      gap: 22px; padding: 0 26px; box-sizing: border-box; font-family: "GSans", sans-serif; font-size: 36px;
      font-weight: 700; color: #fff; box-shadow: 0 6px 0 rgba(0,0,0,.18); }
.kt b { width: 34px; height: 34px; background: rgba(255,255,255,.95); }
""")

# ---------------------------------------------------------------- 1 the Threads question
L.append(
    '<div class="g" id="q" style="top:0;height:700px">'
    '<div class="sheet hide" id="qS" style="height:640px;background:#fff">'
    '<div class="gcard" id="qC" style="left:100px;top:90px;width:880px;height:500px">'
    '<div class="av" style="left:36px;top:30px;background:#1e1e1e">@</div>'
    '<div class="gs hd">Threads</div><div class="gs hs">питання з Threads</div><div class="sep"></div>'
    '<div class="lbl hide" id="qL" style="left:40px;top:160px">Ваша улюблена рубрика</div>'
    '<div class="gs hide" id="qT" style="position:absolute;left:40px;top:215px;width:800px;font-size:58px;'
    'font-weight:700;line-height:1.18">Які автоматизації можна використати репетиторці?</div>'
    + sk.svg(880, 500, sk.underline(70, 440, 360, stroke="red", sw=7), sid="qU") +
    '</div></div></div>')


@beat
def b_q():
    sfx("pop", 0.05)
    sfx("click-soft", "@yaki")
    sfx("pencil", "@repet", -3)
    return js("""
  h.show("#q", 0.0);
  h.sheetIn("#qS", 0.0, 640, null, 0.6);
  h.write("#qL", @rubryka-0.3, 0.5);
  h.pop("#qT", @yaki-0.05, {s: 0.85, r: 0, y: 18});
  h.draw("#qU", @repet, 0.45);
""")


# ---------------------------------------------------------------- 2 if I were a tutor: a little sketch board
L.append(
    '<div class="g" id="tb" style="top:0;height:700px">'
    '<div class="sheet board-bg hide" id="tbS" style="height:700px">'
    '<div class="paper" id="tbP" style="left:250px;top:100px;width:580px;height:360px;transform:rotate(-2deg)">'
    + sk.svg(580, 360, sk.rect(14, 14, 552, 332, stroke="ink", sw=4), sid="tbE") +
    '<div class="hand hide" id="tbF" style="position:absolute;left:0;right:0;top:110px;text-align:center;font-size:92px">'
    'a² + b² = c²</div>'
    + sk.svg(580, 360, sk.underline(120, 250, 340, stroke="blue", sw=7), sid="tbU") +
    '</div>'
    '<div class="ab hide" id="tc1" style="left:250px;top:500px"><span class="chip on">математика</span></div>'
    '<div class="ab hide" id="tc2" style="left:590px;top:500px"><span class="chip cy">історія</span></div>'
    '</div></div>')


@beat
def b_tb():
    sfx("whoosh-short", "@korotshe-0.1")
    sfx("pencil", "@bula", -2)
    sfx("pop", "@matem")
    sfx("pop", "@istorii")
    return js("""
  swap("#q", "#tb", "#tbS", @korotshe-0.2, 700);
  h.pop("#tbP", @korotshe+0.1, {s: 0.4, r: -10, to: -2});
  h.draw("#tbE", @korotshe+0.25, 0.6);
  h.write("#tbF", @bula, 0.9);
  h.draw("#tbU", @matem-0.2, 0.4);
  h.pop("#tc1", @matem, {s: 0.5, r: -5});
  h.pop("#tc2", @istorii, {s: 0.5, r: 5});
""")


# ---------------------------------------------------------------- the BOARD: the running list
RY = [214 + 80 * i for i in range(4)]
BH = 940                   # halfscreen sheet height (STYLE.md §0c)
ROWS = [u"CRM учнів + фінанси", u"Нагадування: урок + оплата", u"Афтеркер", u"Тести у форматі НМТ"]
board = ['<div class="g full" id="bd"><div class="sheet board-bg hide" id="bdS" style="height:%dpx">' % BH,
         '<div id="cam" style="position:absolute;inset:0">',
         '<div class="lbl hide" id="bdL" style="left:100px;top:56px">якби я була репетиторкою</div>',
         '<div class="hand hide" id="bdT" style="position:absolute;left:96px;top:90px;font-size:64px">'
         u'Автоматизації репетиторки</div>',
         sk.svg(1080, 1300, sk.underline(100, 176, 560, stroke="blue"), sid="bdU")]
for i, y in enumerate(RY):
    board.append(sk.svg(1080, 1300, sk.rect(100, y, 54, 54, stroke="ink", sw=4, round_=False), sid="cb%d" % (i + 1)))
    board.append(sk.svg(1080, 1300, sk.check(102, y - 6, 58, sw=9), sid="ck%d" % (i + 1)))
    board.append('<div class="hand hide" id="rt%d" style="position:absolute;left:186px;top:%dpx;font-size:50px;'
                 'white-space:nowrap"><span style="color:#4285F4">%d.</span> %s</div>' % (i + 1, y - 4, i + 1, ROWS[i]))
# diagram 2: calendar + SendPulse -> Claude -> every morning
board.append(
    '<div id="d2">'
    '<div class="pill bpill hide" id="p2c" style="left:80px;top:556px"><span class="dot" style="background:#4285F4"></span>Google Calendar</div>'
    '<div class="pill bpill hide" id="p2s" style="left:640px;top:556px"><span class="dot" style="background:#34A853"></span>SendPulse</div>'
    + sk.svg(1080, 1300, sk.ellipse(540, 730, 112, 76, stroke="ink", fill="yellow", style="solid"), sid="d2C") +
    '<div class="gs hide" id="d2CT" style="position:absolute;left:428px;top:704px;width:224px;text-align:center;font-size:44px;font-weight:700">Claude</div>'
    + sk.svg(1080, 1300, sk.arrow([(300, 664), (360, 700), (432, 716)], stroke="blue"), sid="d2a1")
    + sk.svg(1080, 1300, sk.arrow([(800, 664), (730, 700), (650, 716)], stroke="green"), sid="d2a2")
    + sk.svg(1080, 1300, sk.ellipse(340, 858, 34, 34, stroke="red", sw=4) +
             sk.line([(340, 858), (340, 836)], stroke="red", sw=4, double=False) +
             sk.line([(340, 858), (356, 867)], stroke="red", sw=4, double=False), sid="d2K") +
    '<div class="ab hide" id="d2ch" style="left:396px;top:822px"><span class="chip cr">задача: щоранку</span></div>'
    '</div>')
# diagram 3: aftercare
board.append(
    '<div id="d3">'
    '<div class="pill bpill hide" id="p3z" style="left:60px;top:540px"><span class="dot" style="background:#4285F4"></span>Zoom / Meet</div>'
    + sk.svg(1080, 1300, sk.arrow([(430, 588), (560, 588)], stroke="ink"), sid="d3a1") +
    '<div class="pill bpill hide" id="p3f" style="left:580px;top:540px"><span class="dot" style="background:#EA4335"></span>Fathom</div>'
    '<div class="hand hide" id="d3rec" style="position:absolute;left:850px;top:556px;font-size:34px;line-height:1;color:#EA4335">запис<br>уроку</div>'
    + sk.svg(1080, 1300, sk.arrow([(720, 648), (470, 702), (220, 712)], stroke="blue"), sid="d3a2") +
    '<div class="hand hide" id="d3tr" style="position:absolute;left:300px;top:636px;font-size:40px;color:#4285F4">транскрипт</div>'
    + sk.svg(1080, 1300, sk.ellipse(150, 772, 100, 62, stroke="ink", fill="yellow", style="solid"), sid="d3C") +
    '<div class="gs hide" id="d3CT" style="position:absolute;left:50px;top:748px;width:200px;text-align:center;font-size:40px;font-weight:700">Claude</div>'
    '<div class="ab hide" id="d3sk" style="left:96px;top:838px"><span class="chip on" style="height:54px;font-size:28px">скіл</span></div>'
    + sk.svg(1080, 1300, sk.arrow([(254, 772), (284, 772)], stroke="ink", head=18), sid="d3a3") +
    '<div class="paper hide" id="d3k" style="left:296px;top:706px;width:210px;height:132px">'
    '<div class="hand" style="position:absolute;left:20px;top:10px;font-size:36px">конспект</div>'
    + sk.svg(210, 132, sk.line([(22, 76), (188, 74)], stroke="#9aa0a6", sw=4, double=False) +
             sk.line([(22, 104), (150, 106)], stroke="#9aa0a6", sw=4, double=False), sid="d3kL") +
    '</div>'
    '<div class="paper hide" id="d3d" style="left:524px;top:706px;width:210px;height:132px">'
    '<div class="hand" style="position:absolute;left:20px;top:10px;font-size:36px">домашка</div>'
    + sk.svg(210, 132, sk.rect(22, 62, 24, 24, sw=3, round_=False) + sk.line([(58, 74), (188, 72)], stroke="#9aa0a6", sw=4, double=False) +
             sk.rect(22, 96, 24, 24, sw=3, round_=False) + sk.line([(58, 108), (160, 108)], stroke="#9aa0a6", sw=4, double=False),
             sid="d3dL") +
    '</div>'
    + sk.svg(1080, 1300, sk.arrow([(738, 772), (768, 772)], stroke="green", sw=4, head=18), sid="d3a4") +
    '<div class="pill bpill hide" id="p3s" style="left:780px;top:732px;height:80px;font-size:30px;padding:0 24px"><span class="dot" style="background:#34A853"></span>SendPulse</div>'
    '<div class="hand hide" id="d3u" style="position:absolute;left:740px;top:836px;font-size:40px">учню / батькам</div>'
    + sk.svg(1080, 1300, sk.arrow([(900, 814), (898, 830), (900, 842)], stroke="green", sw=4, head=12), sid="d3a5") +
    '</div>')
board.append('</div></div></div>')
L.append("".join(board))


@beat
def b_board1():
    sfx("whoosh-short", "@os+0.1")
    sfx("pencil", "@nalasht", -2)
    sfx("pencil", "@crm-0.1", -2)
    return js("""
  swap("#tb", "#bd", "#bdS", @os+0.1, 940);
  h.write("#bdL", @os+0.6, 0.35);
  h.write("#bdT", @nalasht-0.05, 0.75);
  h.draw("#bdU", @nalasht+0.6, 0.35);
  h.draw("#cb1", @claude0-0.1, 0.15); h.draw("#cb2", @claude0+0.05, 0.15);
  h.draw("#cb3", @claude0+0.2, 0.15); h.draw("#cb4", @claude0+0.35, 0.15);
  h.write("#rt1", @crm-0.25, 1.3);
""")


# ---------------------------------------------------------------- 3 NEAR: Claude keeps the books
L.append(
    '<div class="g" id="cl" style="top:0;height:700px">'
    '<div class="sheet hide" id="clS" style="height:700px;background:#fff">'
    '<div class="gcard" id="clC" style="left:100px;top:100px;width:880px;height:570px">'
    '<div class="av" style="left:36px;top:30px;background:#FBBC04;color:#1e1e1e">C</div>'
    '<div class="gs hd">Claude</div><div class="gs hs">конектори</div>'
    '<div class="ab hide" id="clN" style="left:360px;top:36px"><span class="chip">Notion</span></div>'
    '<div class="ab hide" id="clG" style="left:560px;top:36px"><span class="chip cg">Google Drive</span></div>'
    '<div class="sep"></div>'
    '<div class="bub me hide" id="clM" style="right:36px;top:150px"><span id="clMT" data-text="Оля заплатила 2000 за 4 уроки"></span></div>'
    '<div class="dots hide" id="clD" style="left:60px;top:270px"><i></i><i></i><i></i><i></i></div>'
    '<div class="tbl hide" id="clTb" style="top:280px">'
    '<div class="th">Учень</div><div class="th">Уроки</div><div class="th">Оплата</div>'
    '<div id="clR1">Оля</div><div id="clR2">4</div><div id="clR3" style="color:#188038;font-weight:700">оплачено</div></div>'
    + sk.svg(880, 570, sk.check(770, 360, 60), sid="clOK") +
    '<div class="bub me hide" id="clQ2" style="right:36px;top:150px">Скільки я заробила цього місяця?</div>'
    '<div class="dots hide" id="clD2" style="left:60px;top:300px"><i></i><i></i><i></i><i></i></div>'
    '<div class="bub in hide" id="clA" style="left:36px;top:280px;font-size:30px">Рахую по таблиці оплат:<br>'
    '<span class="num" style="font-size:72px;color:#202124">точна сума</span></div>'
    '<div class="hand hide" id="clP" style="position:absolute;left:560px;top:400px;font-size:52px;color:#5f6368">«десь так»</div>'
    + sk.svg(880, 570, sk.scribble(550, 410, 270, 40, sw=7), sid="clX") +
    '</div></div></div>')


@beat
def b_cl():
    sfx("pop", "@pidkl")
    sfx("click-soft", "@notion")
    sfx("click-soft", "@google")
    sfx("typing", "@olia-0.1", -4)
    sfx("pop", "@vnosyt")
    sfx("ping", "@oplatu")
    sfx("click-soft", "@skilky")
    sfx("ping", "@tsyfroiu")
    sfx("pencil", "@des", -2)
    return js("""
  swap("#bd", "#cl", "#clS", @pidkl-0.2, 700);
  h.pop("#clN", @notion-0.05, {s: 0.5, r: -5});
  h.pop("#clG", @google-0.05, {s: 0.5, r: 5});
  h.pop("#clM", @pyshesh, {s: 0.7, r: 2});
  h.type("#clMT", @olia-0.1, 13);
  h.pop("#clD", @vin-0.1, {s: 0.5, r: 0});
  h.think("#clD", @vin, 0.7);
  h.out("#clD", @vnosyt-0.15, 0.15);
  h.pop("#clTb", @vnosyt-0.1, {s: 0.9, r: 0, y: 20});
  h.draw("#clOK", @oplatu, 0.3);
  h.out("#clM", @kintsi, 0.25);
  h.out("#clTb", @kintsi, 0.25);
  h.undraw("#clOK", @kintsi, 0.2);
  h.pop("#clQ2", @skilky-0.1, {s: 0.7, r: 2});
  h.pop("#clD2", @skilky+0.5, {s: 0.5, r: 0});
  h.think("#clD2", @skilky+0.55, 0.6);
  h.out("#clD2", @tsyfroiu-0.2, 0.15);
  h.pop("#clA", @tsyfroiu-0.1, {s: 0.6, r: -2});
  h.write("#clP", @des-0.1, 0.5);
  h.draw("#clX", @pryblyzno, 0.35);
""")


@beat
def b_board2():
    sfx("whoosh-short", "@druhe-0.1")
    sfx("pencil", "@druhe+0.3", -2)
    sfx("pop", "@konektori+0.2")
    sfx("pop", "@sendpulse")
    sfx("pencil", "@vclaude", -3)
    sfx("click-soft", "@zaplan+0.2")
    return js("""
  swap("#cl", "#bd", "#bdS", @druhe-0.15, 940);
  h.draw("#ck1", @druhe+0.35, 0.3);
  h.write("#rt2", @nahad-0.1, 1.3);
  h.pop("#p2c", @konektori+0.15, {s: 0.5, r: -4});
  h.pop("#p2s", @sendpulse-0.05, {s: 0.5, r: 4});
  h.draw("#d2a1", @vclaude-0.4, 0.35);
  h.draw("#d2a2", @vclaude-0.2, 0.35);
  h.draw("#d2C", @vclaude, 0.5);
  h.write("#d2CT", @vclaude+0.3, 0.35);
  h.draw("#d2K", @zaplan, 0.45);
  h.pop("#d2ch", @zaplan+0.2, {s: 0.5, r: -3});
  tl.set("#d2", {autoAlpha: 0}, @dyvytsia+0.8);
""")


# ---------------------------------------------------------------- 4 NEAR: the Telegram bot
L.append(
    '<div class="g" id="tg" style="top:0;height:700px">'
    '<div class="sheet hide" id="tgSh" style="height:700px;background:#fff">'
    '<div class="gcard" id="tgC" style="left:100px;top:100px;width:880px;height:570px">'
    '<div class="av" style="left:36px;top:30px;background:#4285F4">Б</div>'
    '<div class="gs hd">Telegram-бот</div><div class="gs hs">SendPulse</div><div class="sep"></div>'
    '<div class="row hide" id="tgS" style="left:36px;top:146px;gap:16px">'
    '<span class="gs" style="font-size:28px;color:#5f6368;font-weight:700">Сьогодні урок:</span>'
    '<span class="chip on">Оля</span><span class="chip on">Марко</span><span class="chip on">Іра</span></div>'
    '<div class="bub in hide" id="tgB1" style="left:36px;top:246px">Нагадую: сьогодні урок!</div>'
    '<div class="bub in hide" id="tgB2" style="left:36px;top:356px;width:560px">Оплачені уроки закінчились. Нагадую про оплату</div>'
    '<div class="pill hide" id="tgW" style="left:640px;top:400px;height:90px;padding:0 30px;font-size:32px;font-weight:700;'
    'background:#1e1e1e;color:#fff">WayForPay</div>'
    + sk.svg(880, 570, sk.arrow([(620, 520), (690, 500), (740, 480)], stroke="red", sw=5, head=22), sid="tgAr") +
    '<div class="hand hide" id="tgWT" style="position:absolute;left:420px;top:500px;font-size:40px;color:#EA4335">посилання</div>'
    '</div></div></div>')


@beat
def b_tg():
    sfx("pop", "@dyvytsia")
    sfx("click-soft", "@kogo")
    sfx("notification", "@pyshe")
    sfx("notification", "@zakinch")
    sfx("pop", "@wfp")
    sfx("click", "@vidpr")
    return js("""
  swap("#bd", "#tg", "#tgSh", @dyvytsia-0.2, 700);
  h.pop("#tgS", @kogo-0.05, {s: 0.8, r: 0, y: 14});
  h.pop("#tgB1", @pyshe, {s: 0.6, r: -2});
  tl.to("#tgC", {keyframes: {x: [0, -8, 7, -4, 2, 0]}, duration: 0.35, ease: "none"}, @pyshe+0.05);
  h.pop("#tgB2", @zakinch-0.1, {s: 0.6, r: -2});
  tl.to("#tgC", {keyframes: {x: [0, -8, 7, -4, 2, 0]}, duration: 0.35, ease: "none"}, @zakinch-0.05);
  h.bump("#tgB2", @nahaduie);
  h.pop("#tgW", @wfp-0.05, {s: 0.5, r: 4});
  h.draw("#tgAr", @posyl-0.1, 0.35);
  h.write("#tgWT", @posyl-0.1, 0.45);
  h.bump("#tgW", @vidpr);
""")


@beat
def b_board3():
    sfx("whoosh-short", "@tretie-0.15")
    sfx("pencil", "@tretie+0.3", -2)
    sfx("pop", "@zoom")
    sfx("pop", "@fathom")
    sfx("pencil", "@transkr-0.2", -3)
    sfx("pop", "@konspekt")
    sfx("pop", "@domashku")
    sfx("pop", "@sp3")
    sfx("pencil", "@uchniu-0.2", -3)
    sfx("pencil", "@chetv+0.2", -2)
    return js("""
  swap("#tg", "#bd", "#bdS", @tretie-0.2, 940);
  h.draw("#ck2", @tretie+0.3, 0.3);
  h.write("#rt3", @after-0.15, 0.7);
  h.pop("#p3z", @zoom-0.15, {s: 0.5, r: -4});
  h.draw("#d3a1", @zapysuie, 0.3);
  h.pop("#p3f", @fathom-0.1, {s: 0.5, r: 4});
  h.write("#d3rec", @fathom+0.3, 0.5);
  h.draw("#d3a2", @transkr-0.3, 0.5);
  h.write("#d3tr", @transkr, 0.5);
  h.draw("#d3C", @claude3-0.1, 0.45);
  h.write("#d3CT", @claude3+0.1, 0.3);
  h.pop("#d3sk", @skil, {s: 0.5, r: -5});
  h.draw("#d3a3", @konspekt-0.3, 0.25);
  h.pop("#d3k", @konspekt-0.05, {s: 0.5, r: -4, to: -2});
  h.draw("#d3kL", @konspekt+0.2, 0.3);
  h.pop("#d3d", @domashku-0.05, {s: 0.5, r: 4, to: 2});
  h.draw("#d3dL", @domashku+0.2, 0.35);
  h.draw("#d3a4", @sp3-0.3, 0.3);
  h.pop("#p3s", @sp3-0.05, {s: 0.5, r: -3});
  h.draw("#d3a5", @letyt, 0.5);
  h.write("#d3u", @uchniu-0.1, 0.6);
  tl.to("#d3", {autoAlpha: 0, duration: 0.3}, @chetv-0.1);
  h.draw("#ck3", @chetv, 0.3);
  h.write("#rt4", @chetv+0.25, 1.4);
""")


# ---------------------------------------------------------------- 5 NEAR: the NMT test -> a quiz
KT = [("#EA4335", "2 і 3"), ("#4285F4", "−2 і 3"), ("#FBBC04", "1 і 6"), ("#34A853", "−1 і −6")]
opts = "".join('<div class="opt hide" id="op%d" style="left:%dpx;top:%dpx"><i></i>%s</div>'
               % (i + 1, 36 + (i % 2) * 412, 330 + (i // 2) * 104, KT[i][1]) for i in range(4))
tiles = "".join('<div class="kt hide" id="kt%d" style="left:%dpx;top:%dpx;background:%s;color:%s"><b style="border-radius:%s"></b>%s</div>'
                % (i + 1, 36 + (i % 2) * 412, 324 + (i // 2) * 120, KT[i][0], "#1e1e1e" if i == 2 else "#fff", ["0", "50%", "0", "50%"][i], KT[i][1])
                for i in range(4))
L.append(
    '<div class="g" id="ts" style="top:0;height:700px">'
    '<div class="sheet hide" id="tsS" style="height:700px;background:#fff">'
    '<div class="gcard" id="tsC" style="left:100px;top:100px;width:880px;height:570px">'
    '<div class="lbl" style="left:40px;top:36px">Тест за темою</div>'
    '<div class="ab" style="left:620px;top:24px"><span class="chip cy">НМТ</span></div>'
    '<div class="gs" id="tsQ" style="position:absolute;left:40px;top:96px;font-size:44px;font-weight:700">Квадратні рівняння</div>'
    '<div class="gs" style="position:absolute;left:40px;top:160px;font-size:52px;font-weight:700">x² − 5x + 6 = 0</div>'
    '<div class="row hide" id="tsCh" style="left:40px;top:244px;gap:16px">'
    '<span class="chip on" id="tsC1">скіл «тест за темою»</span><span class="chip cg hide" id="tsC2">Google Drive</span></div>'
    + opts + tiles +
    '<div class="pill hide" id="ksP" style="left:600px;top:236px;height:80px;padding:0 30px;font-size:36px;font-weight:700;'
    'background:#46178f;color:#fff">Kahoot</div>'
    '</div>'
    '<div class="hand hide" id="ksV" style="position:absolute;left:640px;top:220px;font-size:60px;color:#EA4335;'
    'transform:rotate(-4deg)">вікторина!</div>'
    + sk.svg(1080, 700, sk.spark(626, 240, 26, stroke="yellow", sw=7), sid="ksS") +
    '</div></div>')


@beat
def b_ts():
    sfx("pop", "@tobto2+0.1")
    sfx("pop", "@skil2")
    sfx("pop", "@drive2-0.2")
    sfx("whoosh-short", "@porishav")
    sfx("pop", "@kahoot")
    sfx("sparkle", "@viktor")
    return js("""
  swap("#bd", "#ts", "#tsS", @tobto2-0.1, 700);
  h.pop("#op1", @tobto2+0.3, {s: 0.8, r: 0, y: 10}); h.pop("#op2", @tobto2+0.4, {s: 0.8, r: 0, y: 10});
  h.pop("#op3", @tobto2+0.5, {s: 0.8, r: 0, y: 10}); h.pop("#op4", @tobto2+0.6, {s: 0.8, r: 0, y: 10});
  h.pop("#tsCh", @skil2-0.05, {s: 0.6, r: -3});
  h.pop("#tsC2", @drive2-0.25, {s: 0.5, r: 4});
  h.out("#tsCh", @porishav-0.1, 0.25);
  for (var i = 1; i <= 4; i++) {
    h.out("#op" + i, @porishav-0.1 + i * 0.05, 0.2);
    h.pop("#kt" + i, @porishav + i * 0.12, {s: 0.4, r: (i % 2 ? -6 : 6)});
  }
  h.pop("#ksP", @kahoot-0.05, {s: 0.5, r: 4});
  h.bump("#kt1", @claude4); h.bump("#kt2", @claude4+0.1); h.bump("#kt3", @claude4+0.2); h.bump("#kt4", @claude4+0.3);
  h.write("#ksV", @viktor-0.05, 0.6);
  h.draw("#ksS", @viktor+0.3, 0.3);
""")


# ---------------------------------------------------------------- 6 CTA: the whole list, ticked
mini = "".join('<div class="gs" style="position:absolute;left:96px;top:%dpx;font-size:34px;font-weight:500">'
               '<span style="color:#4285F4;font-weight:700">%d.</span> %s</div>' % (104 + 62 * i, i + 1, ROWS[i])
               for i in range(4))
ticks = "".join(sk.check(36, 104 + 62 * i, 40, sw=7) for i in range(4))
L.append(
    '<div class="g" id="cta" style="top:0;height:700px">'
    '<div class="sheet hide" id="ctaS" style="height:700px;background:#fff">'
    '<div class="gcard" id="ctC" style="left:100px;top:80px;width:880px;height:380px">'
    '<div class="lbl" style="left:40px;top:40px">Автоматизації репетиторки</div>' + mini +
    sk.svg(880, 380, ticks, sid="ctK") + '</div>'
    '<div class="pill hide" id="ctS" style="left:130px;top:480px;height:110px;padding:0 40px;font-size:40px;font-weight:700">'
    + sk.svg(40, 56, sk.line([(4, 4), (36, 4), (36, 52), (20, 38), (4, 52), (4, 4)], stroke="#1e1e1e", sw=4, double=False),
             cls="sk", style="position:relative") + 'Зберегти</div>'
    '<div class="pill hide" id="ctF" style="left:560px;top:480px;height:110px;padding:0 40px;font-size:40px;font-weight:700">'
    + sk.svg(50, 50, sk.arrow([(4, 44), (20, 16), (46, 8)], stroke="#4285F4", sw=4, head=16),
             cls="sk", style="position:relative") + 'Переслати</div>'
    '<div class="hand hide" id="ctT" style="position:absolute;left:640px;top:608px;font-size:46px;color:#EA4335">колезі</div>'
    '</div></div>')


@beat
def b_cta():
    sfx("pop", "@tomu")
    sfx("pencil", "@tomu+0.3", -4)
    sfx("click", "@zberezhy+0.1")
    sfx("click", "@pereshly")
    return js("""
  swap("#ts", "#cta", "#ctaS", @tomu-0.2, 700);
  h.draw("#ctK", @tomu+0.3, 0.9);
  h.pop("#ctS", @zberezhy-0.1, {s: 0.5, r: -4});
  h.bump("#ctS", @zberezhy+0.15);
  h.pop("#ctF", @pereshly-0.15, {s: 0.5, r: 4});
  h.bump("#ctF", @pereshly+0.1);
  h.write("#ctT", @kolezi-0.1, 0.4);
""")


# the white board under ink captions
INVERT = []    # halfscreen keeps her and the white captions in the bottom half (STYLE.md §0c)
# captions drop only where a graphic says her words at the same time
BLACKOUT = [(T["yaki"], T["korotshe"], ""),                 # the question card
            (T["crm"] - 0.2, T["pidkl"] - 0.05, ""),         # «CRM учнів + фінанси» written
            (T["olia"], T["vin"], ""),                       # the typed message
            (T["nahad"] - 0.1, T["konektori"] - 0.05, ""),   # «Нагадування: урок + оплата»
            (T["after"] - 0.1, T["urok"] - 0.3, ""),               # «Афтеркер»
            (T["testy"] - 0.15, T["tobto2"] - 0.05, ""),     # «Тести у форматі НМТ»
            (T["test"] - 0.05, T["natren"] - 0.05, ""),      # chip «тест за темою»
            (T["kahoot"], T["kahoot"] + 0.5, ""),            # the Kahoot pill
            (T["zberezhy"], T["zberezhy"] + 0.5, ""),
            (T["pereshly"], T["pereshly"] + 0.6, "")]


# one sheet replaces another: the new one drops in over the old (z on top), her
# plate re-settles to the new height, the old one is hidden once covered.
SWAP_JS = """
  var Z = 10;
  function swap(oldG, newG, newS, t, hgt) {
    Z += 1;
    tl.set(newG, {autoAlpha: 1, zIndex: Z}, t);
    tl.set(newS, {autoAlpha: 1}, t);
    tl.fromTo(newS, {y: -hgt - 40}, {y: 0, duration: 0.7, ease: SOFT, immediateRender: false}, t);
    h.plateDown(t, Math.max(0, hgt - 580), 0.8);
    tl.set(oldG, {autoAlpha: 0}, t + 0.72);
  }
  tl.set("#q", {zIndex: 10}, 0);
"""


def main():
    gj = []
    for fn in BEATS:
        gj.append("  /* %s */" % fn.__name__)
        gj.append(fn().rstrip())
    for a, b in NO_PAINT:
        for c in SFX:
            assert not (a <= c["t"] < b), ("sfx in no_paint", c)
    head = [SKETCH_JS, "  var h = sketchHelpers(tl);", SWAP_JS,
            '  gsap.set("#vid", {transformOrigin: "540px 900px"});',
            '  tl.fromTo("#vid", {scale: 1}, {scale: 1.045, duration: %.3f, ease: "none"}, 0);' % DUR]
    doc = k.document(
        title=u"Reel 59 — автоматизації репетиторки",
        plate="assets/base.mp4",
        gfx_html="\n".join(L),
        gfx_js="\n".join(head + gj),
        caps=CAPS,
        blackout=BLACKOUT,
        invert=INVERT,
    )
    io.open(os.path.join(HERE, "index.html"), "w", encoding="utf-8").write(doc)
    SFX.sort(key=lambda c: c["t"])
    io.open(os.path.join(HERE, "sfx.json"), "w", encoding="utf-8").write(json.dumps(SFX, indent=1))
    print("index.html  %d captions, %d beats, %d sfx cues" % (len(CAPS), len(BEATS), len(SFX)))


main()
