# -*- coding: utf-8 -*-
"""Reel 56 — «Чим AI-агент відрізняється від звичайного чат-бота з кнопками?».
Posts 2026-11-26. Google x Excalidraw look (STYLE.md §0b), skeleton from reel-45.

Cut from her raw take by tools/cut.py (no closeups: no_paint is empty).

Chain:  NEAR two Material cards, «AI-агент» (Google dots) and «Чат-бот» (chips А/Б):
«?» -> «=» -> «+AI» sticker + price tag with a red arrow up -> red cross -> «≠»
-> OVER (the board wipes in out of the Чат-бот card): «хардкод-бот», a message,
two buttons, А -> туди, Б -> сюди, a stray arrow crossed out, a green fence;
board closes onto the message -> NEAR the webinar form fills (ім'я, телефон,
інфо), a bot bubble with made-up text is crossed out -> the AI-агент card
returns: «скрипт» + «інформація» feed in, a bubble writes itself, a person
-> the bag-shop DM: question, dots, agent asks back, a bag is sketched, arrow to
«менеджер»; grey buttons scribbled -> chips «послуги» / «продукти» -> OVER
(board 2 out of the chips): Чат-бот «або» AI-агент, «або» crossed, one arrow,
buttons + data ticks under the bot, the person rides to the agent, dots, a
checklist; closes onto the agent -> NEAR «або» -> «+», a funnel with two
zones, «?» -> CTA: comment «+», Direct types her business, green tick.

usage: python build.py   (then: python ../tools/sfx.py mix 56)
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

NN = "56"
CUT = json.load(io.open(os.path.join(ROOT, "work", "r" + NN, "cut.json"), encoding="utf-8"))
DUR = 101.017          # (3031 plate frames - 0.5) / 30
FPS = 30
k = Kit(width=1080, height=1920, fps=FPS, duration=DUR)
k.cap_font = "assets/fonts/ProductSans-Bold.ttf"
k.css(sketch_css())
sk = Sketch(seed=56)

NO_PAINT = [tuple(x) for x in CUT["no_paint"]]   # empty on this cut

CAPS = k.load_captions(os.path.join(ROOT, "work", "r" + NN, "captions.json"))


# ---- caption fixes: whisper errors -> the script word / what she said ------
def fix(caps):
    """by position, because the same mangled token can be right elsewhere."""
    def find(word, near):
        c = min((i for i, c in enumerate(caps) if c["w"] == word), key=lambda i: abs(caps[i]["s"] - near))
        assert abs(caps[c]["s"] - near) < 0.5, (word, near)
        return c
    edits = [
        (u"найовують?", 4.41, u"наєбують?"), (u"вони", 5.95, u"одне"), (u"і", 7.83, u"AI"),
        (u"наявують", 11.29, u"наєбують"), (u"Швидко", 17.81, u"чітко"), (u"Я", 19.66, u"є"),
        (u"реєстраційний", 32.20, u"реєстрація на"), (u"вебінар", 36.66, u"вебінар."),
        (u"AI", 40.71, u"AI-агент"), (u"пыша", 54.89, u"пише"), (u"базу", 78.84, u"базові"),
        (u"віддання.", 79.16, u"дані,"), (u"Ап...", 79.63, u"а"), (u"інформацію", 84.52, u"інформацію."),
        (u"в Воронзі", 88.54, u"в воронці"), (u"не одне,", 89.60, u"доречне одне,"),
        (u"писати", 94.34, u"вписати"), (u"коментарі", 96.47, u"в коментарі"),
        (u"пишемо", 97.35, u"мені"), (u"не втирати", 97.69, u"в дірект,"),
        (u"розбираємось", 100.00, u"розберемось"),
        (u"маю", 9.49, u"можу"), (u"треба", 86.68, u"треба,"),
    ]
    for w, near, new in edits:
        caps[find(w, near)]["w"] = new
    drop = [(u"яйцю", 8.07), (u"AN", 41.19)]
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


T = {
    # hook
    "ahent": S(u"AI-агент", 0.53), "chatbota": S(u"чатбота", 2.47), "knopkamy": S(u"кнопками", 3.07),
    "naiebuiut": S(u"наєбують", 4.41), "odne": S(u"одне", 5.95), "dodaty": S(u"додати", 7.45),
    "ai": S(u"AI", 7.83), "tsinu": S(u"ціну", 8.83), "ni": S(u"ні", 10.19), "dvi": S(u"дві", 12.83),
    "rizni": S(u"різні", 13.61),
    # board 1
    "zvychainyi": S(u"Звичайний", 14.40), "khardkod": S(u"хардкод-бот", 16.36), "skrypt": S(u"скрипт", 19.29),
    "povidomlennia": S(u"повідомлення", 20.02), "dvi_kn": S(u"дві", 21.12), "natysnula": S(u"натиснула", 21.73),
    "tudy": S(u"туди", 23.03), "natysnula2": S(u"натиснула", 23.43), "siudy": S(u"сюди", 24.63),
    "niiakoi": S(u"Ніякої", 25.10), "samodiialnosti": S(u"самодіяльності", 25.84),
    # webinar form
    "i_tse": S(u"І", 27.03), "superkorysno": S(u"суперкорисно", 28.04), "chitki": S(u"чіткі", 29.68),
    "reiestratsiia": S(u"реєстрація", 32.20), "imia": S(u"ім'я", 33.90), "nomer": S(u"номер", 34.60),
    "informatsiiu": S(u"інформацію", 35.96), "shchob": S(u"щоб", 38.29), "vid": S(u"від", 39.25),
    "pravylno": S(u"правильно", 39.81),
    # the agent
    "ale": S(u"але", 40.27), "ahent2": S(u"AI-агент", 40.71), "skryptom": S(u"скриптом", 44.20),
    "informatsiieiu": S(u"інформацією", 45.04), "dopysuvaty": S(u"дописувати", 46.83),
    "pidlasht": S(u"підлаштовуватись", 48.35), "liudyna": S(u"людина", 50.22), "otrymaty": S(u"отримати", 50.90),
    # the DM
    "napryklad": S(u"Наприклад", 51.53), "sumok": S(u"сумок", 53.80), "pyshe": S(u"пише", 54.89),
    "sam": S(u"сам", 56.23), "opytaie": S(u"опитає", 56.81), "zrozumiie": S(u"зрозуміє", 57.35),
    "sumka": S(u"сумка", 58.01), "peredast": S(u"передасть", 59.27), "menedzheru": S(u"менеджеру", 60.33),
    "adaptuietsia": S(u"адаптується", 61.52), "ne_vede": S(u"не", 63.52), "knopkakh": S(u"кнопках", 65.06),
    # chips
    "i_tse2": S(u"І", 65.73), "posluhamy": S(u"послугами", 67.88), "produktovykh": S(u"продуктових", 69.16),
    # board 2
    "naitsikavishe": S(u"найцікавіше", 70.46), "boty": S(u"боти", 71.64), "isnuvaty": S(u"існувати", 72.10),
    "zamist": S(u"замість", 72.90), "razom": S(u"разом", 74.36), "odnomu": S(u"одному", 74.86),
    "prosti": S(u"прості", 77.50), "zibraty": S(u"зібрати", 78.42), "bazovi": S(u"базові", 78.84),
    "potim": S(u"потім", 79.98), "liudynu": S(u"людину", 81.02), "ahenta": S(u"AI-агента", 81.62),
    "utochniuie": S(u"уточнює", 82.82), "zbyraie": S(u"збирає", 83.98), "tobto": S(u"Тобто", 85.23),
    # funnel
    "obyraty": S(u"обирати", 85.62), "ne_treba": S(u"не", 86.34), "voronttsi": S(u"воронці", 88.54),
    "odne2": S(u"одне", 89.60), "inshe": S(u"інше", 90.36), "ne_rozum": S(u"не", 93.28),
    "voronku": S(u"воронку", 95.08),
    # CTA
    "plius": S(u"плюс", 96.29), "dyrekt": S(u"дірект", 97.69), "rozkazhy": S(u"розкажи", 98.23),
    "biznes": S(u"бізнес", 99.06), "rozberemos": S(u"розберемось", 100.00),
    "dur": DUR,
}


def js(src):
    """`@name`, `@name+0.12`, `@name-0.1` -> one literal time."""
    def rep(m):
        v = T[m.group(1)] + (float(m.group(2)) if m.group(2) else 0.0)
        return "%.3f" % v
    return re.sub(r"@(\w+)([+-]\d+(?:\.\d+)?)?", rep, src)


SFX = []


def sfx(name, t, db=0):
    if isinstance(t, str):
        t = float(js(t))
    SFX.append({"t": round(max(0.0, t), 3), "name": name, "db": db})


L = []        # html
BEATS = []    # functions returning js


def beat(fn):
    BEATS.append(fn)
    return fn


k.css("""
.hide { opacity: 0; visibility: hidden; }
.sk .sf { opacity: 0; visibility: hidden; }
.ab { position: absolute; }
.bub { position: absolute; padding: 22px 30px; border-radius: 30px; font-family: "GSans", sans-serif;
       font-size: 36px; font-weight: 500; line-height: 1.25; max-width: 560px; }
.bub.in { background: #f1f3f4; color: #202124; border-bottom-left-radius: 8px; }
.bub.me { background: #d3e3fd; color: #041e49; border-bottom-right-radius: 8px; }
.av { position: absolute; width: 64px; height: 64px; border-radius: 50%; display: grid; place-items: center;
      font-family: "GSans", sans-serif; font-weight: 700; font-size: 30px; color: #fff; }
.lbl { font-family: "GSans", sans-serif; font-size: 26px; font-weight: 700; letter-spacing: .14em;
       color: #5f6368; text-transform: uppercase; position: absolute; }
.field { position: absolute; border-radius: 16px; border: 2px solid #747775; background: #fff; }
.field .fl { position: absolute; left: 22px; top: -20px; background: #fff; padding: 0 10px;
             font-family: "GSans", sans-serif; font-size: 28px; color: #0b57d0; font-weight: 500; }
.row { position: absolute; display: flex; align-items: center; gap: 26px; font-family: "GSans", sans-serif; }
.ttl { position: absolute; font-family: "GSans", sans-serif; font-size: 46px; font-weight: 700; color: #202124; }
.ctr { left: 0; right: 0; text-align: center; }
.btn { position: absolute; height: 84px; border-radius: 42px; display: grid; place-items: center;
       font-family: "GSans", sans-serif; font-size: 36px; font-weight: 700; color: #0b57d0;
       border: 3px solid #0b57d0; background: #fff; }
""")


def dots(did, left, top, cls="dots hide"):
    return '<div class="%s" id="%s" style="left:%dpx;top:%dpx"><i></i><i></i><i></i><i></i></div>' % (
        cls, did, left, top)


# ---------------------------------------------------------------- 1 the hook: two cards
L.append(
    '<div class="g" id="vs" style="top:0;height:700px">'
    # left: the button bot
    '<div class="gcard hide" id="vsB" style="left:60px;top:130px;width:400px;height:400px">'
    '<div class="ttl ctr" style="top:44px">Чат-бот</div>'
    '<div class="btn" style="left:60px;top:150px;width:280px">Кнопка А</div>'
    '<div class="btn" style="left:60px;top:262px;width:280px">Кнопка Б</div>'
    '<div class="ab hide" id="vsAI" style="right:-34px;top:-30px;transform:rotate(8deg)">'
    '<span class="chip cy" style="font-weight:700;font-size:38px">+ AI</span></div>'
    '</div>'
    # right: the agent
    '<div class="gcard hide" id="vsA" style="left:620px;top:130px;width:400px;height:400px">'
    '<div class="ttl ctr" style="top:44px">AI-агент</div>'
    + dots("vsD", 108, 200, "dots") +
    '<div class="gs ctr" style="position:absolute;top:290px;font-size:30px;color:#5f6368">думає</div>'
    '</div>'
    '<div class="hand hide" id="vsQ" style="position:absolute;left:500px;top:250px;width:80px;text-align:center;font-size:120px;color:#EA4335">?</div>'
    + sk.svg(1080, 700, sk.line([(500, 315), (580, 312)], sw=8, double=False) +
             sk.line([(500, 355), (580, 352)], sw=8, double=False), sid="vsEq") +
    sk.svg(1080, 700, sk.line([(575, 270), (505, 400)], stroke="red", sw=9, double=False), sid="vsNe") +
    # the price tag with an arrow up (no number: she says none)
    sk.svg(1080, 700,
           sk.rect(240, 470, 220, 110, stroke="ink", fill="yellow", style="solid") +
           sk.ellipse(268, 525, 11, 11, stroke="ink", sw=3.5), sid="vsTag") +
    '<div class="hand hide" id="vsTagT" style="position:absolute;left:310px;top:496px;font-size:48px">ціна</div>'
    + sk.svg(1080, 700, sk.arrow([(480, 590), (492, 520), (500, 450)], stroke="red", sw=7), sid="vsUp") +
    '</div>')


@beat
def b_vs():
    sfx("pop", "@ahent-0.05")
    sfx("pop", "@chatbota")
    sfx("pencil", "@naiebuiut", -3)
    sfx("pop", "@ai")
    sfx("click", "@ni")
    sfx("pencil", "@dvi", -3)
    return js("""
  h.show("#vs", @ahent-0.1);
  h.pop("#vsA", @ahent-0.05, {s: 0.6, r: 4});
  h.think("#vsD", @ahent+0.3, 2.4);
  h.pop("#vsB", @chatbota-0.05, {s: 0.6, r: -4});
  h.bump("#vsB .btn", @knopkamy);
  h.write("#vsQ", @naiebuiut, 0.35);
  h.wiggle("#vsQ", @naiebuiut+0.4);
  h.fadeOut("#vsQ", @odne-0.2, 0.15);
  h.draw("#vsEq", @odne-0.1, 0.4);
  h.pop("#vsAI", @ai-0.05, {s: 0.3, r: -20, to: 8});
  h.draw("#vsTag", @ai+0.3, 0.45);
  h.write("#vsTagT", @ai+0.55, 0.3);
  h.draw("#vsUp", @tsinu-0.3, 0.4);
  h.wiggle("#vsTag", @tsinu+0.1);
  h.out("#vsAI", @ni-0.1, 0.2);
  h.undraw("#vsTag", @ni-0.1, 0.25);
  h.undraw("#vsUp", @ni-0.1, 0.25);
  h.fadeOut("#vsTagT", @ni-0.1, 0.2);
  h.wiggle("#vsEq", @ni);
  h.draw("#vsNe", @dvi, 0.3);
  h.bump("#vsA", @rizni);
  h.bump("#vsB", @rizni);
  h.out("#vsA", @zvychainyi-0.3, 0.25);
  h.undraw("#vsEq", @zvychainyi-0.3, 0.2);
  h.undraw("#vsNe", @zvychainyi-0.3, 0.2);
  tl.to("#vsB", {scale: 1.12, duration: 0.3, ease: "power2.in"}, @zvychainyi-0.2);
  tl.set("#vs", {autoAlpha: 0}, @zvychainyi+0.6);
""")


# ---------------------------------------------------------------- 2 OVER: the hardcode bot on the board
L.append(
    '<div class="g full" id="bd">'
    '<div class="board"></div>'
    '<div class="lbl hide" id="bdL" style="left:110px;top:170px">Звичайний чат-бот</div>'
    '<div class="hand hide" id="bdT" style="left:108px;top:214px;position:absolute;font-size:90px">хардкод-бот</div>'
    + sk.svg(1080, 1300, sk.underline(110, 335, 480, stroke="blue"), sid="bdU") +
    '<div class="lbl hide" id="bdS" style="left:110px;top:400px;color:#0b57d0">скрипт</div>'
    '<div class="bub in hide" id="bdM" style="left:250px;top:450px;width:520px;text-align:center">Привіт! Обери варіант:</div>'
    '<div class="btn hide" id="bdA" style="left:230px;top:620px;width:220px">А</div>'
    '<div class="btn hide" id="bdB" style="left:630px;top:620px;width:220px">Б</div>'
    + sk.svg(1080, 1300, sk.arrow([(340, 720), (300, 820), (280, 905)], stroke="blue"), sid="bdArA")
    + sk.svg(1080, 1300, sk.rect(130, 920, 300, 120, stroke="blue"), sid="bdBxA") +
    '<div class="hand hide" id="bdTA" style="position:absolute;left:130px;top:950px;width:300px;text-align:center;font-size:52px">туди</div>'
    + sk.svg(1080, 1300, sk.arrow([(740, 720), (780, 820), (800, 905)], stroke="blue"), sid="bdArB")
    + sk.svg(1080, 1300, sk.rect(650, 920, 300, 120, stroke="blue"), sid="bdBxB") +
    '<div class="hand hide" id="bdTB" style="position:absolute;left:650px;top:950px;width:300px;text-align:center;font-size:52px">сюди</div>'
    # the improvisation that is not allowed: a stray dashed arrow off the rails
    + sk.svg(1080, 1300, sk.arrow([(540, 735), (560, 860), (520, 1130)], stroke="#9aa0a6", sw=5, dashed=True), sid="bdStray")
    + '<div class="hand hide" id="bdQ" style="position:absolute;left:560px;top:1100px;font-size:70px;color:#9aa0a6">?</div>'
    + sk.svg(1080, 1300, sk.cross(480, 1070, 100, sw=11), sid="bdX")
    + sk.svg(1080, 1300, sk.rect(90, 430, 900, 650, stroke="green", sw=7), sid="bdF")
    + '</div>')

BX, BY = 260, 330          # the Чат-бот card's centre: the board opens out of it


@beat
def b_board():
    sfx("whoosh-short", "@zvychainyi-0.2")
    sfx("pencil", "@khardkod-0.1", -2)
    sfx("pop", "@povidomlennia")
    sfx("pop", "@dvi_kn")
    sfx("click", "@natysnula+0.3")
    sfx("click", "@natysnula2+0.3")
    sfx("click-soft", "@niiakoi+0.2")
    sfx("pencil", "@samodiialnosti", -3)
    sfx("whoosh-short", "@i_tse-0.45")
    return js("""
  h.boardIn("#bd", @zvychainyi-0.2, %d, %d, 0.75);
  h.write("#bdL", @zvychainyi+0.35, 0.35);
  h.write("#bdT", @khardkod-0.05, 0.6);
  h.draw("#bdU", @khardkod+0.6, 0.35);
  h.write("#bdS", @skrypt-0.1, 0.3);
  h.pop("#bdM", @povidomlennia-0.1, {s: 0.6, r: -3});
  h.pop("#bdA", @dvi_kn, {s: 0.5, r: -6});
  h.pop("#bdB", @dvi_kn+0.15, {s: 0.5, r: 6});
  tl.to("#bdA", {backgroundColor: "#0b57d0", color: "#ffffff", duration: 0.15}, @natysnula+0.3);
  h.bump("#bdA", @natysnula+0.3);
  h.draw("#bdArA", @natysnula+0.5, 0.35);
  h.draw("#bdBxA", @tudy-0.2, 0.4);
  h.write("#bdTA", @tudy, 0.3);
  tl.to("#bdB", {backgroundColor: "#0b57d0", color: "#ffffff", duration: 0.15}, @natysnula2+0.3);
  h.bump("#bdB", @natysnula2+0.3);
  h.draw("#bdArB", @natysnula2+0.5, 0.35);
  h.draw("#bdBxB", @siudy-0.25, 0.4);
  h.write("#bdTB", @siudy, 0.3);
  h.draw("#bdStray", @niiakoi-0.1, 0.3);
  h.write("#bdQ", @niiakoi+0.1, 0.25);
  h.draw("#bdX", @niiakoi+0.35, 0.3);
  h.draw("#bdF", @samodiialnosti, 0.6);
  h.boardOut("#bd", @i_tse-0.5, 510, 490, 0.5);
""" % (BX, BY))


# ---------------------------------------------------------------- 3 NEAR: the webinar form
L.append(
    '<div class="g" id="fm" style="top:0;height:700px">'
    '<div class="gcard" id="fmC" style="left:100px;top:70px;width:880px;height:560px">'
    '<div class="ttl hide" id="fmT" style="left:44px;top:36px">Реєстрація на вебінар</div>'
    '<div class="field" id="fm1" style="left:44px;top:140px;width:640px;height:100px"><span class="fl">Ім\'я</span>'
    '<div class="hand hide" id="fm1T" style="position:absolute;left:30px;top:22px;font-size:50px">Олена</div></div>'
    '<div class="field" id="fm2" style="left:44px;top:280px;width:640px;height:100px"><span class="fl">Номер телефону</span>'
    '<div class="hand hide" id="fm2T" style="position:absolute;left:30px;top:22px;font-size:50px">+380 ...</div></div>'
    + sk.svg(880, 560, sk.check(720, 160, 66), sid="fmK1")
    + sk.svg(880, 560, sk.check(720, 300, 66), sid="fmK2") +
    '<div class="ab hide" id="fmI" style="left:44px;top:430px"><span class="chip cg">Інфо про вебінар</span></div>'
    '<div class="bub me hide" id="fmBot" style="left:470px;top:416px;width:370px;height:100px"></div>'
    + sk.svg(880, 560, sk.line([(500, 450), (580, 444), (660, 456), (800, 446)], stroke="#041e49", sw=5, double=False)
             + sk.line([(500, 486), (590, 492), (700, 480)], stroke="#041e49", sw=5, double=False), sid="fmBotS")
    + sk.svg(880, 560, sk.cross(590, 405, 120, sw=11), sid="fmX") +
    '</div>'
    + sk.svg(1080, 700, sk.spark(960, 90, 30, stroke="green", sw=7), sid="fmSp", cls="sk over-plate") +
    '</div>')


@beat
def b_form():
    sfx("pop", "@superkorysno")
    sfx("pop", "@reiestratsiia-0.1")
    sfx("pencil", "@imia", -4)
    sfx("pop", "@informatsiiu")
    sfx("pop", "@shchob")
    sfx("click", "@vid")
    return js("""
  h.show("#fm", @superkorysno-0.1);
  h.pop("#fmC", @superkorysno-0.1, {s: 0.6, r: -3});
  h.draw("#fmSp", @superkorysno+0.3, 0.35);
  h.bump("#fm1", @chitki);
  h.bump("#fm2", @chitki+0.15);
  h.write("#fmT", @reiestratsiia-0.05, 0.6);
  h.write("#fm1T", @imia, 0.4);
  h.draw("#fmK1", @imia+0.35, 0.25);
  h.write("#fm2T", @nomer, 0.5);
  h.draw("#fmK2", @nomer+0.5, 0.25);
  h.pop("#fmI", @informatsiiu-0.05, {s: 0.5, r: -4});
  h.pop("#fmBot", @shchob, {s: 0.6, r: 3});
  h.draw("#fmBotS", @shchob+0.2, 0.6);
  h.draw("#fmX", @vid, 0.3);
  h.wiggle("#fmBot", @vid+0.1);
  tl.to("#fmC", {y: -30, autoAlpha: 0, duration: 0.3, ease: "power2.in"}, @ale-0.3);
  tl.set("#fm", {autoAlpha: 0}, @ale+0.05);
""")


# ---------------------------------------------------------------- 4 NEAR: the agent works differently
L.append(
    '<div class="g" id="ag" style="top:0;height:700px">'
    '<div class="gcard" id="agC" style="left:190px;top:70px;width:700px;height:560px">'
    + dots("agD", 230, 60, "dots") +
    '<div class="ttl ctr" style="top:120px">AI-агент</div>'
    '<div class="ab hide" id="agS" style="left:90px;top:210px"><span class="chip cy">скрипт</span></div>'
    '<div class="ab hide" id="agI" style="left:330px;top:210px"><span class="chip on">інформація</span></div>'
    '<div class="bub me hide" id="agB" style="left:150px;top:330px;width:500px;height:130px"></div>'
    + sk.svg(700, 560, sk.line([(185, 370), (300, 362), (420, 374), (610, 364)], stroke="#041e49", sw=5, double=False)
             + sk.line([(185, 410), (280, 418), (400, 406), (540, 414)], stroke="#041e49", sw=5, double=False), sid="agBS") +
    '<div class="av hide" id="agP" style="left:50px;top:470px;background:#34A853">Л</div>'
    '<div class="hand hide" id="agPT" style="position:absolute;left:128px;top:478px;font-size:40px">людина</div>'
    '</div></div>')


@beat
def b_agent():
    sfx("pop", "@ahent2-0.1")
    sfx("pop", "@skryptom")
    sfx("pop", "@informatsiieiu")
    sfx("pencil", "@dopysuvaty", -3)
    sfx("pop", "@liudyna")
    return js("""
  h.show("#ag", @ahent2-0.15);
  h.pop("#agC", @ahent2-0.15, {s: 0.6, r: 3});
  h.think("#agD", @ahent2+0.2, 2.4);
  h.pop("#agS", @skryptom-0.05, {s: 0.4, r: -8});
  h.pop("#agI", @informatsiieiu-0.05, {s: 0.4, r: 8});
  h.pop("#agB", @dopysuvaty-0.15, {s: 0.6, r: 2});
  h.draw("#agBS", @dopysuvaty+0.1, 1.2);
  tl.to("#agB", {rotation: -3, x: -20, duration: 0.6, ease: SP}, @pidlasht);
  h.pop("#agP", @liudyna-0.05, {s: 0.3, r: 0});
  h.write("#agPT", @liudyna+0.15, 0.35);
  h.bump("#agB", @otrymaty);
  tl.to("#agC", {scale: 0.9, autoAlpha: 0, duration: 0.28, ease: "power2.in"}, @napryklad-0.3);
  tl.set("#ag", {autoAlpha: 0}, @napryklad+0.02);
""")


# ---------------------------------------------------------------- 5 NEAR: the bag-shop DM
L.append(
    '<div class="g" id="dm" style="top:0;height:700px">'
    '<div class="gcard" id="dmC" style="left:100px;top:50px;width:880px;height:590px">'
    '<div class="av" style="left:36px;top:26px;background:#4285F4">С</div>'
    '<div class="gs" style="position:absolute;left:122px;top:28px;font-size:34px;font-weight:700">Магазин сумок</div>'
    '<div class="gs" style="position:absolute;left:122px;top:70px;font-size:24px;color:#5f6368">Direct · AI-агент</div>'
    '<div style="position:absolute;left:0;right:0;top:116px;height:2px;background:#e8eaed"></div>'
    '<div id="dmIn">'
    '<div class="bub in hide" id="dmQ" style="left:36px;top:140px">Привіт! Шукаю сумку</div>'
    + dots("dmD", 690, 250) +
    '<div class="bub me hide" id="dmA" style="right:36px;top:232px">Для чого вона вам?</div>'
    '<div class="bub in hide" id="dmR" style="left:36px;top:324px">На роботу, під ноутбук</div>'
    + sk.svg(880, 590,
             sk.rect(620, 430, 200, 130, stroke="ink", fill="yellow", style="hachure") +
             sk.line([(665, 432), (680, 385), (760, 385), (775, 432)], sw=5), sid="dmBag") +
    '<div class="av hide" id="dmM" style="left:60px;top:450px;width:84px;height:84px;background:#EA4335;font-size:36px">М</div>'
    '<div class="hand hide" id="dmMT" style="position:absolute;left:160px;top:470px;font-size:44px">менеджер</div>'
    + sk.svg(880, 590, sk.arrow([(605, 500), (480, 530), (370, 505)], stroke="red", sw=5), sid="dmAr") +
    '</div>'
    '<div class="ab hide" id="dmK" style="left:0;right:0;top:250px;display:flex;justify-content:center;gap:40px">'
    '<div class="btn" style="position:relative;width:260px;color:#9aa0a6;border-color:#9aa0a6">Кнопка А</div>'
    '<div class="btn" style="position:relative;width:260px;color:#9aa0a6;border-color:#9aa0a6">Кнопка Б</div></div>'
    + sk.svg(880, 590, sk.scribble(150, 250, 580, 80, sw=8), sid="dmKX") +
    '</div></div>')


@beat
def b_dm():
    sfx("pop", "@napryklad")
    sfx("notification", "@pyshe")
    sfx("ping", "@opytaie")
    sfx("ping", "@zrozumiie+0.1", -3)
    sfx("pencil", "@sumka", -3)
    sfx("pop", "@peredast+0.3")
    sfx("pop", "@ne_vede-0.1")
    sfx("pencil", "@knopkakh-0.2", -3)
    return js("""
  h.show("#dm", @napryklad-0.05);
  h.pop("#dmC", @napryklad-0.05, {s: 0.7, r: -3});
  h.pop("#dmQ", @pyshe, {s: 0.5, r: 0});
  h.pop("#dmD", @sam-0.1, {s: 0.5, r: 0});
  h.think("#dmD", @sam, 0.6);
  h.out("#dmD", @opytaie-0.1, 0.12);
  h.pop("#dmA", @opytaie, {s: 0.6, r: 2});
  h.pop("#dmR", @zrozumiie+0.1, {s: 0.5, r: 0});
  h.draw("#dmBag", @sumka-0.05, 0.6);
  h.draw("#dmAr", @peredast, 0.35);
  h.pop("#dmM", @peredast+0.3, {s: 0.3, r: 0});
  h.write("#dmMT", @menedzheru-0.1, 0.4);
  h.bump("#dmA", @adaptuietsia);
  h.bump("#dmR", @adaptuietsia+0.15);
  tl.to("#dmIn", {autoAlpha: 0.18, duration: 0.25}, @ne_vede-0.15);
  h.pop("#dmK", @ne_vede-0.1, {s: 0.8, r: 0, y: 10});
  h.draw("#dmKX", @knopkakh-0.2, 0.4);
  tl.to("#dmC", {y: -30, autoAlpha: 0, duration: 0.3, ease: "power2.in"}, @i_tse2-0.2);
  tl.set("#dm", {autoAlpha: 0}, @i_tse2+0.15);
""")


# ---------------------------------------------------------------- 6 NEAR: services / products
L.append(
    '<div class="g" id="ch" style="top:0;height:700px">'
    '<div class="ab hide" id="ch1" style="left:150px;top:270px"><span class="chip cg" style="height:100px;font-size:46px;padding:0 44px">послуги</span></div>'
    '<div class="ab hide" id="ch2" style="left:580px;top:270px"><span class="chip on" style="height:100px;font-size:46px;padding:0 44px">продукти</span></div>'
    + sk.svg(1080, 700, sk.check(240, 160, 80, sw=10), sid="chK1", cls="sk over-plate")
    + sk.svg(1080, 700, sk.check(690, 160, 80, sw=10), sid="chK2", cls="sk over-plate") +
    '</div>')


@beat
def b_chips():
    sfx("pop", "@posluhamy")
    sfx("pop", "@produktovykh")
    return js("""
  h.show("#ch", @posluhamy-0.1);
  h.pop("#ch1", @posluhamy-0.05, {s: 0.4, r: -6});
  h.draw("#chK1", @posluhamy+0.3, 0.3);
  h.pop("#ch2", @produktovykh-0.05, {s: 0.4, r: 6});
  h.draw("#chK2", @produktovykh+0.3, 0.3);
  tl.to("#ch1, #ch2", {scale: 1.2, duration: 0.3, ease: "power2.in"}, @naitsikavishe-0.2);
  tl.set("#ch", {autoAlpha: 0}, @naitsikavishe+0.6);
""")


# ---------------------------------------------------------------- 7 OVER: one chain
L.append(
    '<div class="g full" id="b2">'
    '<div class="board"></div>'
    '<div class="lbl hide" id="b2L" style="left:110px;top:170px">Не замість, а разом</div>'
    '<div class="hand hide" id="b2T" style="left:108px;top:210px;position:absolute;font-size:84px">один ланцюжок</div>'
    + sk.svg(1080, 1300, sk.rect(70, 380, 380, 190, stroke="ink", fill="yellow", style="solid"), sid="b2Bot") +
    '<div class="ttl hide" id="b2BotT" style="left:70px;top:446px;width:380px;text-align:center">Чат-бот</div>'
    + sk.svg(1080, 1300, sk.rect(630, 380, 380, 190, stroke="ink", fill="blue", style="solid"), sid="b2Ag") +
    '<div class="ttl hide" id="b2AgT" style="left:630px;top:446px;width:380px;text-align:center">AI-агент</div>'
    '<div class="hand hide" id="b2Or" style="position:absolute;left:470px;top:430px;width:140px;text-align:center;font-size:60px">або</div>'
    + sk.svg(1080, 1300, sk.scribble(470, 440, 140, 60, sw=7), sid="b2OrX")
    + sk.svg(1080, 1300, sk.arrow([(460, 475), (540, 462), (620, 475)], stroke="blue", sw=7, head=34), sid="b2Ar") +
    # under the bot: buttons, then the basic data
    '<div class="btn hide" id="b2A" style="left:90px;top:620px;width:160px">А</div>'
    '<div class="btn hide" id="b2B" style="left:270px;top:620px;width:160px">Б</div>'
    '<div class="hand hide" id="b2D1" style="position:absolute;left:110px;top:760px;font-size:52px">ім\'я</div>'
    '<div class="hand hide" id="b2D2" style="position:absolute;left:110px;top:850px;font-size:52px">телефон</div>'
    + sk.svg(1080, 1300, sk.check(340, 760, 54), sid="b2K1")
    + sk.svg(1080, 1300, sk.check(340, 850, 54), sid="b2K2") +
    # the person who rides the arrow
    '<div class="av hide" id="b2P" style="left:228px;top:290px;width:76px;height:76px;background:#34A853;font-size:34px">Л</div>'
    # under the agent: dots, then a checklist
    + dots("b2D", 742, 630) +
    '<div class="hand hide" id="b2Q" style="position:absolute;left:660px;top:690px;font-size:46px">деталі запиту</div>'
    + sk.svg(1080, 1300,
             sk.rect(670, 790, 50, 50, sw=4) + sk.line([(745, 815), (860, 812), (960, 816)], sw=4.5, double=False) +
             sk.rect(670, 870, 50, 50, sw=4) + sk.line([(745, 895), (830, 898), (930, 893)], sw=4.5, double=False) +
             sk.rect(670, 950, 50, 50, sw=4) + sk.line([(745, 975), (880, 972), (970, 977)], sw=4.5, double=False),
             sid="b2CL")
    + sk.svg(1080, 1300, sk.check(672, 782, 50, sw=7), sid="b2C1")
    + sk.svg(1080, 1300, sk.check(672, 862, 50, sw=7), sid="b2C2")
    + sk.svg(1080, 1300, sk.check(672, 942, 50, sw=7), sid="b2C3")
    + '</div>')


@beat
def b_board2():
    sfx("whoosh-short", "@naitsikavishe-0.2")
    sfx("pencil", "@boty-0.1", -3)
    sfx("pencil", "@razom", -3)
    sfx("pop", "@prosti")
    sfx("pop", "@potim")
    sfx("click-soft", "@utochniuie")
    sfx("pencil", "@zbyraie-0.1", -3)
    sfx("whoosh-short", "@tobto-0.3")
    return js("""
  h.boardIn("#b2", @naitsikavishe-0.2, 540, 320, 0.75);
  h.write("#b2L", @naitsikavishe+0.4, 0.35);
  h.draw("#b2Bot", @boty-0.2, 0.5);
  h.write("#b2BotT", @boty, 0.3);
  h.draw("#b2Ag", @boty+0.15, 0.5);
  h.write("#b2AgT", @boty+0.35, 0.3);
  h.write("#b2Or", @isnuvaty, 0.3);
  h.draw("#b2OrX", @zamist, 0.35);
  h.fadeOut("#b2Or", @razom-0.25, 0.15);
  h.undraw("#b2OrX", @razom-0.25, 0.15);
  h.draw("#b2Ar", @razom, 0.4);
  h.write("#b2T", @odnomu-0.1, 0.6);
  h.pop("#b2A", @prosti, {s: 0.5, r: -6});
  h.pop("#b2B", @prosti+0.15, {s: 0.5, r: 6});
  h.write("#b2D1", @zibraty, 0.3);
  h.draw("#b2K1", @zibraty+0.3, 0.2);
  h.write("#b2D2", @bazovi, 0.35);
  h.draw("#b2K2", @bazovi+0.35, 0.2);
  h.pop("#b2P", @potim, {s: 0.3, r: 0});
  tl.to("#b2P", {x: 560, duration: 1.1, ease: "power2.inOut"}, @liudynu-0.2);
  h.bump("#b2Ag", @ahenta);
  h.pop("#b2D", @utochniuie-0.1, {s: 0.5, r: 0});
  h.think("#b2D", @utochniuie, 1.2);
  h.write("#b2Q", @utochniuie+0.3, 0.45);
  h.draw("#b2CL", @zbyraie-0.2, 0.5);
  h.draw("#b2C1", @zbyraie+0.25, 0.15);
  h.draw("#b2C2", @zbyraie+0.45, 0.15);
  h.draw("#b2C3", @zbyraie+0.65, 0.15);
  h.boardOut("#b2", @tobto-0.3, 820, 475, 0.5);
""")


# ---------------------------------------------------------------- 8 NEAR: no choosing; the funnel
L.append(
    '<div class="g" id="fn" style="top:0;height:700px">'
    '<div class="ab hide" id="fnB" style="left:150px;top:80px"><span class="chip cy" style="font-weight:700">Чат-бот</span></div>'
    '<div class="ab hide" id="fnA" style="left:690px;top:80px"><span class="chip on" style="font-weight:700">AI-агент</span></div>'
    '<div class="hand hide" id="fnOr" style="position:absolute;left:470px;top:84px;width:140px;text-align:center;font-size:54px;color:#fff">або</div>'
    + sk.svg(1080, 700, sk.scribble(470, 96, 140, 50, sw=7), sid="fnOrX", cls="sk over-plate") +
    '<div class="num hide" id="fnPl" style="position:absolute;left:470px;top:58px;width:140px;text-align:center;font-size:110px;color:#34A853">+</div>'
    '<div class="paper hide" id="fnP" style="left:250px;top:210px;width:580px;height:420px">'
    + sk.svg(580, 420,
             sk.line([(40, 40), (540, 40), (360, 390), (220, 390), (40, 40)], sw=5) +
             sk.line([(140, 200), (440, 200)], sw=4, double=False), sid="fnS") +
    '<div class="hand hide" id="fnT1" style="position:absolute;left:0;right:0;top:90px;text-align:center;font-size:54px;color:#b06000">кнопки</div>'
    '<div class="hand hide" id="fnT2" style="position:absolute;left:0;right:0;top:250px;text-align:center;font-size:50px;color:#0b57d0">AI-агент</div>'
    '</div>'
    '<div class="hand hide" id="fnQ" style="position:absolute;left:860px;top:300px;font-size:150px;color:#EA4335">?</div>'
    '</div>')


@beat
def b_funnel():
    sfx("pop", "@obyraty-0.1")
    sfx("pop", "@ne_treba+0.4")
    sfx("pencil", "@voronttsi-0.1", -2)
    return js("""
  h.show("#fn", @obyraty-0.15);
  h.pop("#fnB", @obyraty-0.1, {s: 0.5, r: -6});
  h.pop("#fnA", @obyraty, {s: 0.5, r: 6});
  h.write("#fnOr", @obyraty+0.2, 0.3);
  h.draw("#fnOrX", @ne_treba, 0.3);
  h.fadeOut("#fnOr", @ne_treba+0.35, 0.12);
  h.undraw("#fnOrX", @ne_treba+0.35, 0.12);
  h.pop("#fnPl", @ne_treba+0.4, {s: 0.3, r: 0});
  h.pop("#fnP", @voronttsi-0.15, {s: 0.7, r: -3});
  h.draw("#fnS", @voronttsi, 0.7);
  h.write("#fnT1", @odne2, 0.35);
  h.write("#fnT2", @inshe-0.1, 0.4);
  h.write("#fnQ", @ne_rozum, 0.35);
  h.wiggle("#fnQ", @ne_rozum+0.4);
  h.bump("#fnP", @voronku);
  h.fadeOut("#fnQ", @voronku+0.2, 0.2);
  tl.to("#fnP, #fnB, #fnA, #fnPl", {scale: 0.5, y: -60, autoAlpha: 0, duration: 0.3, ease: "power2.in"}, @plius-0.45);
  tl.set("#fn", {autoAlpha: 0}, @plius-0.1);
""")


# ---------------------------------------------------------------- 9 CTA
L.append(
    '<div class="g" id="cta" style="top:0;height:700px">'
    '<div class="pill hide" id="cmt" style="left:170px;top:140px;width:740px;height:110px;padding:0 36px;font-size:36px">'
    '<span style="color:#5f6368">Коментар:</span><span id="cmtT" data-text="+" style="font-weight:700;font-size:56px"></span></div>'
    '<div class="pill hide" id="dmP" style="left:110px;top:310px;width:860px;height:110px;padding:0 36px;font-size:34px">'
    '<span style="color:#0b57d0;font-weight:700">Direct</span><span style="color:#5f6368">Руті:</span>'
    '<span id="dmPT" data-text="Мій бізнес — це..." style="font-weight:500"></span></div>'
    + sk.svg(1080, 700, sk.check(470, 470, 120, sw=12), sid="ctaK", cls="sk over-plate") +
    '</div>')


@beat
def b_cta():
    sfx("pop", "@plius-0.25")
    sfx("key-press", "@plius+0.1")
    sfx("pop", "@dyrekt-0.2")
    sfx("typing", "@rozkazhy+0.1", -4)
    sfx("chime", "@rozberemos")
    return js("""
  h.show("#cta", @plius-0.3);
  h.pop("#cmt", @plius-0.25, {s: 0.8, r: 0, y: 20});
  h.type("#cmtT", @plius+0.1, 6);
  h.pop("#dmP", @dyrekt-0.2, {s: 0.8, r: 0, y: 20});
  h.type("#dmPT", @rozkazhy+0.1, 13);
  h.draw("#ctaK", @rozberemos, 0.45);
  h.bump("#ctaK", @rozberemos+0.5);
""")


INVERT = [(T["zvychainyi"] + 0.3, T["i_tse"] + 0.05, ""),          # board 1
          (T["naitsikavishe"] + 0.3, T["tobto"] + 0.2, "")]         # board 2
BLACKOUT = [(T["khardkod"] - 0.05, T["khardkod"] + 0.9, ""),       # «хардкод-бот» title
            (T["reiestratsiia"] - 0.05, T["imia"] - 0.1, ""),       # «Реєстрація на вебінар»
            (T["posluhamy"] - 0.05, T["naitsikavishe"] - 0.1, ""),  # «послуги» / «продукти»
            (T["odnomu"] - 0.2, T["odnomu"] + 0.75, ""),            # «один ланцюжок»
            (T["plius"] - 0.05, T["plius"] + 0.5, "")]              # comment «+»


def main():
    gj = []
    for fn in BEATS:
        gj.append("  /* %s */" % fn.__name__)
        gj.append(fn().rstrip())
    for a, b in NO_PAINT:
        for c in SFX:
            assert not (a <= c["t"] < b), ("sfx in no_paint", c)
    head = [SKETCH_JS, "  var h = sketchHelpers(tl);",
            '  gsap.set("#vid", {transformOrigin: "540px 900px"});',
            '  tl.fromTo("#vid", {scale: 1}, {scale: 1.045, duration: %.3f, ease: "none"}, 0);' % DUR]
    doc = k.document(
        title=u"Reel 56 — агент чи чат-бот",
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
    print(" ".join(c["w"] for c in CAPS))


main()
