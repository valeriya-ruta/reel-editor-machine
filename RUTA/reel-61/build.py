# -*- coding: utf-8 -*-
"""Reel 61 — «Як зробити, щоб АІ-агент нічого не вигадував?». Posts 2026-11-21.

THE WORKED EXAMPLE of the Google x Excalidraw look (STYLE.md §0b): Material
cards, chips, toggles and Google Sans hold hand-drawn content that draws itself
on — Excalidraw strokes, hachure, Excalifont handwriting — in Google's four
colours. The whiteboard (dot grid) is the takeover.

Cut from her raw take by tools/cut.py (no closeups: no_paint is empty).

Chain:  NEAR the DM: a client asks, the agent "thinks" (Google dots), answers
with a scribble -> red cross on «дурницю» -> the card shrinks to one sticky
note «1 штука» -> OVER (the board wipes in from the note): the SendPulse agent
panel sketched — «Інструкції» field, chip «скрипти», the «Веб» toggle -> the
toggle flips on, the agent runs an arrow out to a hand-drawn globe and back,
a green tick (useful) then a red risk bar fills and a nonsense bubble appears
-> the toggle flips off, the globe is scratched out, the instruction field
fills with handwriting and a fence is drawn around agent + instructions ->
board closes onto the agent -> NEAR a lightbulb sketch «геніально», the
SendPulse chip gets a heart -> the DM again: a question it can't answer, dots,
«Не знаю — передаю менеджеру», a manager joins by arrow, green tick -> CTA:
four Material chips (business, team, managers, leads), a hand-drawn «+» in a
circle, the comment field types «+».

usage: python build.py   (then: python ../tools/sfx.py mix 61)
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

NN = "61"
CUT = json.load(io.open(os.path.join(ROOT, "work", "r" + NN, "cut.json"), encoding="utf-8"))
DUR = 68.417           # (2053 plate frames - 0.5) / 30
FPS = 30
k = Kit(width=1080, height=1920, fps=FPS, duration=DUR)
k.cap_font = "assets/fonts/ProductSans-Bold.ttf"
k.css(sketch_css())
sk = Sketch(seed=45)

NO_PAINT = [tuple(x) for x in CUT["no_paint"]]   # empty on this cut

CAPS = k.load_captions(os.path.join(ROOT, "work", "r" + NN, "captions.json"))


# ---- caption fixes: whisper errors -> the script word / what she said ------
def fix(caps):
    """by position, because the same mangled token can be right elsewhere.
    ('w', i, text) replaces; ('merge', i) folds caps[i+1] into caps[i]."""
    def find(word, near):
        c = min((i for i, c in enumerate(caps) if c["w"] == word), key=lambda i: abs(caps[i]["s"] - near))
        assert abs(caps[c]["s"] - near) < 0.5, (word, near)
        return c
    edits = [
        ("Небільше", 0.0, u"Найбільший"), ("страт", 0.75, u"страх"), ("будь", 1.35, u"будь-яким"),
        ("дурнетю.", 7.39, u"дурницю."), ("Штукав.", 11.60, u"штуку."), ("таку", 13.38, u"такого"),
        ("синпуївсь,", 14.10, u"SendPulse,"), ("Туму!", 34.43, u"Тому"), ("Я", 35.07, u"якщо"),
        ("ще", 35.32, u"цю"), ("виділяв", 40.97, u"відійде"), ("Сенпульс.", 46.38, u"SendPulse."),
        ("Йв", 56.17, u"І"), ("сссссссссссссс", 56.49, u"все."), ("пишу", 65.80, u"пиши"),
        ("плюсів", 66.08, u"плюсик"), ("ми...", 66.98, u"ми"), ("по", 67.59, u"поспілкуємось."),
    ]
    for w, near, new in edits:
        caps[find(w, near)]["w"] = new
    drop = [("яким", 1.71), ("концюю", 35.44), ("спілкуємось.", 67.73)]
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
    "strakh": S(u"страх", 0.75), "ahentom": S(u"агентом", 2.11), "dyrekti": S(u"діректі", 3.73),
    "prydumaie": S(u"придумає", 5.45), "klientu": S(u"клієнту", 6.73), "durnytsiu": S(u"дурницю", 7.39),
    "skladno": S(u"складно", 8.97), "odnu": S(u"одну", 11.20), "shtuku": S(u"штуку", 11.60),
    "koly": S(u"Коли", 12.27), "sendpulse": S(u"SendPulse", 14.10), "pole": S(u"поле", 15.62),
    "instruktsii": S(u"інструкції", 17.14), "skrypty": S(u"скрипти", 17.66), "knopka": S(u"кнопка", 19.17),
    "korystuvannia": S(u"користування", 19.92), "tsia": S(u"Ця", 22.48), "oznachaie": S(u"означає", 23.00),
    "vyity": S(u"вийти", 24.92), "internet": S(u"інтернет", 25.36), "informatsiiu": S(u"інформацію", 26.94),
    "keisy": S(u"кейси", 28.72), "korysno": S(u"корисно", 29.84), "ale": S(u"Але", 30.64),
    "zbilshuie": S(u"збільшує", 31.62), "shans": S(u"шанс", 32.28), "ne_te": S(u"те", 34.06),
    "tomu": S(u"Тому", 34.43), "knopku": S(u"кнопку", 35.86), "vmykaty": S(u"вмикати", 36.96),
    "natomist": S(u"натомість", 37.66), "propysaty": S(u"прописати", 38.60), "skrypty2": S(u"скрипти", 39.36),
    "nikoly": S(u"ніколи", 40.33), "instruktsii2": S(u"інструкції", 41.47), "henialno": S(u"геніально", 43.00),
    "podobaiutsia": S(u"подобаються", 44.84), "sendpulse2": S(u"SendPulse", 46.38),
    "pytannia": S(u"питання", 48.48), "znaie": S(u"знає", 50.10), "politkorektno": S(u"політкоректно", 51.30),
    "skazhe": S(u"скаже", 53.44), "znaie2": S(u"знає", 54.25), "menedzheru": S(u"менеджеру", 55.58),
    "vse": S(u"все", 56.49), "nichoho": S(u"нічого", 57.05), "mozhe": S(u"може", 59.59),
    "biznes": S(u"бізнес", 61.76), "maluy": S(u"малий", 60.76), "komanda": S(u"команда", 62.32),
    "menedzhery": S(u"менеджери", 62.83), "zaiavok": S(u"заявок", 63.53), "khochesh": S(u"хочеш", 64.31),
    "pyshy": S(u"пиши", 65.80), "pliusyk": S(u"плюсик", 66.08), "komentari": S(u"коментарі", 66.32),
    "dur": DUR,
}


# the half screen's span, snapped to frames: her cut-out covers it with slack
HALF0 = round(int((T["koly"] - 0.25) * FPS) / FPS, 3)
HALF1 = round(int((T["instruktsii2"] + 0.25 + 0.95) * FPS) / FPS, 3)


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
""")

# ---------------------------------------------------------------- 1 the DM
CHAT = "#dm"


def dm_card(cid, top):
    # a mockup -> a sheet that drops from the top and pushes her down (STYLE.md §0c)
    return ('<div class="sheet hide" id="%sC" style="height:700px;background:#fff">'
            '<div style="position:absolute;left:100px;top:%dpx;width:880px;height:560px">'
            '<div class="av" style="left:36px;top:30px;background:#34A853">К</div>'
            '<div class="gs" style="position:absolute;left:122px;top:34px;font-size:34px;font-weight:700">Клієнтка</div>'
            '<div class="gs" style="position:absolute;left:122px;top:76px;font-size:24px;color:#5f6368">Direct</div>'
            '<div style="position:absolute;left:0;right:0;top:124px;height:2px;background:#e8eaed"></div>'
            % (cid, top))


L.append(
    '<div class="g" id="dm" style="top:0;height:700px">' + dm_card("dm", 110) +
    '<div class="bub in hide" id="dmQ" style="left:36px;top:160px">Скільки коштує і коли можна почати?</div>'
    '<div class="dots hide" id="dmD" style="left:690px;top:330px"><i></i><i></i><i></i><i></i></div>'
    '<div class="bub me hide" id="dmA" style="right:36px;top:300px;width:470px;height:150px"></div>'
    + sk.svg(880, 560, sk.line([(450, 340), (560, 330), (680, 345), (800, 334)], stroke="#041e49", sw=5, double=False)
             + sk.line([(450, 380), (530, 392), (640, 372), (740, 386)], stroke="#041e49", sw=5, double=False)
             + sk.line([(450, 418), (520, 410), (590, 420)], stroke="#041e49", sw=5, double=False),
             sid="dmS", style="left:0;top:0") +
    sk.svg(880, 560, sk.cross(560, 300, 150, sw=11), sid="dmX") +
    '<div class="hand hide" id="dmH" style="position:absolute;left:470px;top:470px;font-size:48px;color:#EA4335">дурниця!</div>'
    '</div></div></div>')


@beat
def b_dm():
    sfx("pop", "@strakh")
    sfx("click-soft", "@strakh+0.35")
    sfx("pencil", "@prydumaie", 2)
    sfx("click", "@durnytsiu")
    return js("""
  h.show("#dm", @strakh-0.3);
  h.sheetIn("#dmC", @strakh-0.3, 700);
  h.pop("#dmQ", @strakh+0.35, {s: 0.5, r: 0});
  h.pop("#dmD", @ahentom, {s: 0.5, r: 0});
  h.think("#dmD", @ahentom+0.1, 2.6);
  h.out("#dmD", @prydumaie-0.15, 0.15);
  h.pop("#dmA", @prydumaie-0.1, {s: 0.6, r: 2});
  h.draw("#dmS", @prydumaie+0.15, 1.1);
  h.draw("#dmX", @durnytsiu, 0.35);
  h.wiggle("#dmA", @durnytsiu+0.1);
  h.write("#dmH", @durnytsiu+0.25, 0.4);
""")


# ---------------------------------------------------------------- 2 one thing
L.append(
    '<div class="g" id="one" style="top:0;height:700px">'
    '<div class="paper" id="oneP" style="left:350px;top:150px;width:380px;height:330px;transform:rotate(-3deg);background:#fff7d1">'
    + sk.svg(380, 330, sk.circle_around(190, 140, 110, 80, stroke="red", sw=7), sid="oneS") +
    '<div class="num" style="position:absolute;left:0;right:0;top:56px;text-align:center;font-size:150px;color:#202124">1</div>'
    '<div class="hand" style="position:absolute;left:0;right:0;top:240px;text-align:center;font-size:52px">штука</div>'
    '</div></div>')


@beat
def b_one():
    sfx("whoosh-short", "@skladno")
    sfx("pop", "@odnu")
    sfx("pencil", "@shtuku", -2)
    return js("""
  h.sheetOut("#dmC", @skladno, 700);
  tl.set("#dm", {autoAlpha: 0}, @skladno+0.7);
  h.pop("#one", @odnu-0.1, {s: 1, r: 0, y: 0, d: 0.2});
  h.pop("#oneP", @odnu-0.1, {s: 0.4, r: -12, to: -3});
  h.draw("#oneS", @shtuku+0.05, 0.45);
""")


# ---------------------------------------------------------------- 3 OVER: the agent panel on the board

L.append(
    '<div class="g full" id="bd">'
    # a scheme -> halfscreen, her §00.3.3 geometry: the whiteboard comes down to
    # y 1240, she drops 330 px, her cut-out keeps her head in front of it.
    # Content: y 290 (top no-go) to ~940 across, and beside her head to 1240.
    '<div class="sheet board-bg hide" id="bdS" style="height:1240px">'
    '<div id="cam" style="position:absolute;inset:0">'
    '<div class="lbl hide" id="bdL" style="left:110px;top:300px">SendPulse · AI-агент</div>'
    '<div class="hand hide" id="bdT" style="left:108px;top:336px;position:absolute;font-size:70px">Налаштування</div>'
    + sk.svg(1080, 1240, sk.underline(110, 428, 430, stroke="blue"), sid="bdU") +
    '<div class="field hide" id="fI" style="left:110px;top:480px;width:860px;height:220px"><span class="fl">Інструкції</span></div>'
    + sk.svg(1080, 1240,
             sk.line([(150, 535), (420, 531), (700, 539), (900, 533)], stroke="#3c4043", sw=5, double=False) +
             sk.line([(150, 590), (360, 594), (620, 586), (840, 592)], stroke="#3c4043", sw=5, double=False) +
             sk.line([(150, 645), (330, 641), (560, 649)], stroke="#3c4043", sw=5, double=False),
             sid="fIS") +
    '<div class="ab hide" id="chS" style="left:720px;top:618px"><span class="chip cy">скрипти</span></div>'
    '<div class="row hide" id="rW" style="left:110px;top:730px;width:860px;height:90px">'
    '<div class="gs" style="font-size:44px;font-weight:700">Веб</div>'
    '<div class="gs" style="font-size:30px;color:#5f6368;flex:1">користування веб-сайтами</div></div>'
    '<div class="tgl hide" id="tW" style="left:866px;top:743px"><b></b></div>'
    # agent left of her head, the internet right of it, arrows arcing over her
    + sk.svg(1080, 1240, sk.ellipse(170, 1080, 92, 92, stroke="blue", fill="blue", style="hachure"), sid="agO") +
    '<div class="gs hide" id="agT" style="position:absolute;left:70px;top:1058px;width:200px;text-align:center;font-size:38px;font-weight:700;color:#0b57d0">агент</div>'
    + sk.svg(1080, 1240,
             sk.ellipse(910, 1080, 95, 95, stroke="ink") +
             sk.ellipse(910, 1080, 42, 95, stroke="ink", sw=3.5) +
             sk.line([(818, 1045), (1002, 1045)], sw=3.5, double=False) +
             sk.line([(818, 1115), (1002, 1115)], sw=3.5, double=False), sid="glO") +
    '<div class="hand hide" id="glT" style="position:absolute;left:820px;top:1180px;width:180px;text-align:center;font-size:40px">інтернет</div>'
    + sk.svg(1080, 1240, sk.arrow([(235, 1000), (540, 870), (845, 1000)], stroke="blue"), sid="arO")
    + sk.svg(1080, 1240, sk.arrow([(840, 1035), (540, 950), (240, 1035)], stroke="blue"), sid="arI")
    + sk.svg(1080, 1240, sk.check(960, 930, 60), sid="okC")
    + '<div class="ab hide" id="rk" style="left:40px;top:1214px;width:260px;height:22px;border-radius:11px;background:#f1f3f4">'
      '<div id="rkF" style="height:100%;width:100%;border-radius:11px;background:#EA4335;transform-origin:0 50%"></div></div>'
    + '<div class="hand hide" id="rkT" style="position:absolute;left:40px;top:1168px;font-size:36px;color:#EA4335">шанс помилки</div>'
    + sk.svg(1080, 1240, sk.scribble(815, 990, 190, 180, sw=8), sid="glX")
    # the fence: instructions + the (off) web row — nothing gets out
    + sk.svg(1080, 1240, sk.rect(60, 462, 960, 378, stroke="green", sw=7), sid="fence")
    + '</div></div></div>')
k.matte("half1", HALF0, round(HALF1 - HALF0, 3))


@beat
def b_board():
    sfx("whoosh-short", "@koly-0.1")
    sfx("pencil", "@koly+0.4", -2)
    sfx("click-soft", "@pole")
    sfx("pencil", "@instruktsii", -3)
    sfx("pop", "@skrypty")
    sfx("click-soft", "@knopka")
    sfx("click", "@tsia+0.2")
    sfx("whoosh-short", "@vyity")
    sfx("ping", "@korysno")
    sfx("pencil", "@ne_te-0.2", -3)
    sfx("click", "@vmykaty")
    sfx("pencil", "@propysaty", -2)
    sfx("sparkle", "@nikoly")
    sfx("whoosh-short", "@instruktsii2+0.25")
    return js("""
  tl.to("#oneP", {scale: 1.25, duration: 0.35, ease: "power2.in"}, @koly-0.15);
  h.show("#bd", @koly-0.15);
  h.halfIn("#bdS", @koly-0.15);
  tl.set("#one", {autoAlpha: 0}, @koly+0.6);
  h.write("#bdL", @koly+0.25, 0.35);
  h.write("#bdT", @koly+0.45, 0.6);
  h.draw("#bdU", @sendpulse+0.1, 0.4);
  h.pop("#fI", @pole-0.1, {s: 0.9, r: 0, y: 14});
  h.draw("#fIS", @instruktsii-0.05, 0.7);
  h.pop("#chS", @skrypty, {s: 0.4, r: -6});
  h.pop("#rW", @knopka-0.05, {s: 0.95, r: 0, y: 18});
  h.pop("#tW", @knopka+0.1, {s: 0.5, r: 0, y: 0});
  /* on: the agent can go out */
  h.toggle("#tW", @tsia+0.2, "#0b57d0");
  h.draw("#agO", @oznachaie, 0.6);
  h.write("#agT", @oznachaie+0.3, 0.35);
  h.draw("#glO", @vyity-0.2, 0.7);
  h.write("#glT", @internet, 0.4);
  h.draw("#arO", @vyity, 0.5);
  h.draw("#arI", @informatsiiu-0.1, 0.5);
  h.draw("#okC", @korysno-0.1, 0.3);
  h.show("#rk", @ale);
  h.write("#rkT", @ale, 0.4);
  tl.fromTo("#rkF", {scaleX: 0}, {scaleX: 0.88, duration: 1.2, ease: "power2.out"}, @zbilshuie);
  h.wiggle("#rkT", @ne_te);
  /* off: scripts instead */
  tl.to("#tW", {backgroundColor: "#e1e3e1", borderColor: "#747775", duration: 0.18}, @vmykaty);
  tl.to("#tW b", {x: 0, scale: 1, backgroundColor: "#747775", duration: 0.45, ease: SP}, @vmykaty);
  h.undraw("#arO", @vmykaty, 0.25);
  h.undraw("#arI", @vmykaty, 0.25);
  h.undraw("#okC", @vmykaty, 0.2);
  h.draw("#glX", @vmykaty+0.15, 0.45);
  tl.to("#rkF", {scaleX: 0.06, duration: 0.8, ease: "power2.inOut"}, @natomist);
  h.bump("#fI", @propysaty);
  h.bump("#chS", @skrypty2);
  h.draw("#fence", @nikoly-0.1, 0.9);
  h.halfOut("#bdS", @instruktsii2+0.25);
""")


# ---------------------------------------------------------------- 4 genius + SendPulse
L.append(
    '<div class="g" id="gen" style="top:0;height:700px">'
    + sk.svg(1080, 700,
             sk.ellipse(420, 290, 105, 115, stroke="ink", fill="yellow", style="solid") +
             sk.rect(375, 400, 90, 70, stroke="ink", sw=4, round_=False) +
             sk.line([(380, 495), (460, 495)], sw=4, double=False) +
             sk.spark(420, 160, 34, stroke="yellow", sw=7), sid="bulb", cls="sk over-plate") +
    '<div class="pill hide" id="spP" style="left:560px;top:250px;height:110px;padding:0 40px 0 30px;font-size:44px;font-weight:700">'
    '<span style="display:inline-block;width:46px;height:46px;border-radius:50%;background:#4285F4"></span>SendPulse</div>'
    + sk.svg(1080, 700,
             sk._p("M905 410 C 870 370, 820 410, 905 470 C 990 410, 940 370, 905 410", "#EA4335", 7),
             sid="heart", cls="sk over-plate") +
    '</div>')


@beat
def b_gen():
    sfx("sparkle", "@henialno")
    sfx("pop", "@sendpulse2-0.4")
    sfx("pencil", "@sendpulse2+0.2", -3)
    return js("""
  h.show("#gen", @henialno-0.3);
  h.draw("#bulb", @henialno-0.3, 0.8);
  h.pop("#spP", @podobaiutsia, {s: 0.5, r: 4});
  h.draw("#heart", @sendpulse2, 0.5);
  h.bump("#spP", @sendpulse2+0.35);
  h.fadeOut("#gen", @sendpulse2+0.9, 0.3);
""")


# ---------------------------------------------------------------- 5 the DM again: it doesn't know
L.append(
    '<div class="g" id="dm2" style="top:0;height:700px">' + dm_card("dm2", 110) +
    '<div class="bub in hide" id="d2Q" style="left:36px;top:160px">А ви робите доставку в Канаду?</div>'
    '<div class="dots hide" id="d2D" style="left:690px;top:330px"><i></i><i></i><i></i><i></i></div>'
    '<div class="bub me hide" id="d2A" style="right:36px;top:290px;width:520px">Не знаю відповіді. Передаю вас менеджеру</div>'
    '<div class="av hide" id="d2M" style="left:52px;top:430px;width:84px;height:84px;background:#EA4335;font-size:36px">М</div>'
    '<div class="hand hide" id="d2MT" style="position:absolute;left:24px;top:500px;font-size:40px">менеджер</div>'
    + sk.svg(880, 560, sk.arrow([(470, 410), (330, 440), (150, 466)], stroke="red", sw=5), sid="d2Ar") +
    sk.svg(880, 560, sk.check(760, 440, 80), sid="d2OK") +
    '</div></div></div>')


@beat
def b_dm2():
    sfx("pop", "@pytannia-0.3")
    sfx("click-soft", "@pytannia")
    sfx("notification", "@skazhe")
    sfx("pop", "@menedzheru")
    sfx("pencil", "@nichoho", -3)
    return js("""
  h.show("#dm2", @pytannia-0.6);
  h.sheetIn("#dm2C", @pytannia-0.6, 700);
  h.pop("#d2Q", @pytannia, {s: 0.5, r: 0});
  h.pop("#d2D", @znaie, {s: 0.5, r: 0});
  h.think("#d2D", @znaie+0.1, 2.6);
  h.out("#d2D", @skazhe-0.15, 0.15);
  h.pop("#d2A", @skazhe, {s: 0.6, r: 2});
  h.pop("#d2M", @menedzheru-0.1, {s: 0.3, r: 0});
  h.draw("#d2Ar", @menedzheru-0.25, 0.35);
  h.write("#d2MT", @menedzheru+0.2, 0.4);
  h.draw("#d2OK", @nichoho, 0.35);
  h.bump("#d2OK", @mozhe);
  h.sheetOut("#dm2C", @mozhe+0.2, 700);
  tl.set("#dm2", {autoAlpha: 0}, @mozhe+0.9);
""")


# ---------------------------------------------------------------- 6 CTA
L.append(
    '<div class="g" id="cta" style="top:0;height:700px">'
    '<div class="ab" style="left:90px;top:90px;width:900px;display:flex;flex-wrap:wrap;gap:20px">'
    '<span class="chip on hide" id="c1">малий чи середній бізнес</span>'
    '<span class="chip cg hide" id="c2">команда</span>'
    '<span class="chip cy hide" id="c3">менеджери</span>'
    '<span class="chip cr hide" id="c4">багато заявок</span></div>'
    + sk.svg(1080, 700, sk.ellipse(540, 395, 95, 90, stroke="white", sw=7) +
             sk.line([(540, 345), (540, 445)], stroke="white", sw=10, double=False) +
             sk.line([(490, 395), (590, 395)], stroke="white", sw=10, double=False),
             sid="plus", cls="sk over-plate") +
    '<div class="pill hide" id="cmt" style="left:170px;top:470px;width:740px;height:100px;padding:0 36px;font-size:36px">'
    '<span style="color:#5f6368">Коментар:</span><span id="cmtT" data-text="+" style="font-weight:700;font-size:48px"></span></div>'
    '</div>')


@beat
def b_cta():
    sfx("pop", "@maluy")
    sfx("pop", "@komanda")
    sfx("pop", "@menedzhery")
    sfx("pop", "@zaiavok")
    sfx("pencil", "@pyshy", -2)
    sfx("key-press", "@komentari+0.3")
    return js("""
  h.show("#cta", @maluy-0.1);
  h.pop("#c1", @maluy, {s: 0.5, r: -4});
  h.pop("#c2", @komanda, {s: 0.5, r: 4});
  h.pop("#c3", @menedzhery, {s: 0.5, r: -4});
  h.pop("#c4", @zaiavok, {s: 0.5, r: 4});
  h.draw("#plus", @pyshy, 0.7);
  h.pop("#cmt", @komentari-0.2, {s: 0.8, r: 0, y: 20});
  h.type("#cmtT", @komentari+0.3, 6);
  h.bump("#plus", @komentari+0.4);
""")


INVERT = []    # halfscreen keeps her (and the white captions) in the bottom half


def main():
    gj = []
    for fn in BEATS:
        gj.append("  /* %s */" % fn.__name__)
        gj.append(fn().rstrip())
    for a, b in NO_PAINT:
        for c in SFX:
            assert not (a <= c["t"] < b), ("sfx in no_paint", c)
    head = [SKETCH_JS, "  var h = sketchHelpers(tl);",
            '  gsap.set("#vid, .plate.matte", {transformOrigin: "540px 900px"});',
            '  tl.fromTo("#vid, .plate.matte", {scale: 1}, {scale: 1.045, duration: %.3f, ease: "none"}, 0);' % DUR]
    doc = k.document(
        title=u"Reel 61 — агент нічого не вигадує",
        plate="assets/base.mp4",
        gfx_html="\n".join(L),
        gfx_js="\n".join(head + gj),
        caps=CAPS,
        invert=INVERT,
    )
    io.open(os.path.join(HERE, "index.html"), "w", encoding="utf-8").write(doc)
    SFX.sort(key=lambda c: c["t"])
    io.open(os.path.join(HERE, "sfx.json"), "w", encoding="utf-8").write(json.dumps(SFX, indent=1))
    print("index.html  %d captions, %d beats, %d sfx cues" % (len(CAPS), len(BEATS), len(SFX)))


main()
