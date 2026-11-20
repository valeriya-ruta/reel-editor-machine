# -*- coding: utf-8 -*-
"""Reel 55 — «Скільки хвилин займає один рілс, коли система вже налаштована?».

Google x Excalidraw look (STYLE.md §0b), layouts per §0c (her plate moves;
nothing sits on her head). Cut from her raw take by tools/cut.py (no punches,
no_paint empty). Whisper's «Дякую за підтримку!» hallucinations and her
«Давайте так!» restart cue are dropped in work/r55/cut-fix.json.

The one object is the STOPWATCH (how long the edit takes), carried through:

NEAR  a small card over the footage: stopwatch, «? хв»; the needle spins; chip
      «система налаштована»; «10–15 хв» lands on her words, gets scribbled out on
      «правдива», «залежить від рілса» is written.
HALF  board A drops (her plate pushed down): MY reels — суфлер, мінімум помилок,
      the raw strip «2–3 хв» -> arrow -> Клод -> «15–20 хв»; an «анімації» slider
      (більше -> довше, менше -> швидше). The camera pans down to the long video:
      a strip «5–6 хв», red crosses (помилки), a red cut line «3 хв», the tail
      scribbled out -> Клод -> «30 хв» / «1 год»; formula «погані вхідні дані ->
      довше». Board rolls up.
MOVE  a Material comparison sheet: Клод / самій / монтажер bars; chips
      «безкоштовно», «лише підписка на Клод».
HALF  board B: sun «зранку», 10 raw thumbnails, -> Клод (dots think), «кілька
      годин», 10 green ticks, «а я — своїми справами»; pan: phone (tick) vs laptop
      (cross), «пам'ять» / «перегрів» struck out, the cloud.
NEAR  pill «АІ-монтаж ?» over the footage.
MOVE  CTA mockup: the comment field types «ТЕСТ», her DM, the raw video
      attachment, Claude thinks, «Готово: твій рілс» + green tick.

usage: python build.py   (then: python ../tools/sfx.py mix 55)
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

NN = "55"
CUT = json.load(io.open(os.path.join(ROOT, "work", "r" + NN, "cut.json"), encoding="utf-8"))
DUR = 92.450           # (2774 plate frames - 0.5) / 30
FPS = 30
k = Kit(width=1080, height=1920, fps=FPS, duration=DUR)
k.cap_font = "assets/fonts/ProductSans-Bold.ttf"
k.css(sketch_css())
sk = Sketch(seed=55)

NO_PAINT = [tuple(x) for x in CUT["no_paint"]]

CAPS = k.load_captions(os.path.join(ROOT, "work", "r" + NN, "captions.json"))


# ---- caption fixes: whisper errors -> the script word / what she said ------
def fix(caps):
    def find(word, near):
        c = min((i for i, c in enumerate(caps) if c["w"] == word), key=lambda i: abs(caps[i]["s"] - near))
        assert abs(caps[c]["s"] - near) < 0.5, (word, near)
        return c
    # the leading whisper hallucination over silence: not her
    del caps[find(u"підтримку!", 0.00)]
    edits = [
        (u"сказати", 13.81, u"сказати,"), (u"ділса.", 16.78, u"рілса."),
        (u"тексту", 21.18, u"текст"), (u"Флера,", 21.56, u"з суфлера,"),
        (u"понвілок", 23.76, u"помилок,"), (u"Такі", 28.23, u"такі"), (u"А якщо", 33.73, u"Якщо"),
        (u"і що,", 37.16, u"і ще"), (u"всі", 39.14, u"в"), (u"хвилини", 39.44, u"хвилини,"),
        (u"не", 48.51, u"навіть"), (u"біддак!", 48.69, u"так!"), (u"це", 49.17, u"Це"),
        (u"Мені", 59.28, u"мені"), (u"кривосів", 61.82, u"рілсів,"), (u"Ви", 62.57, u"віддати"),
        (u"Клоді?", 63.84, u"Клоді,"), (u"Повся", 74.97, u"бо все"), (u"хмарій.", 75.99, u"в хмарі."),
        (u"Якщо", 77.39, u"якщо"), (u"Claude,", 89.04, u"мій Claude,"), (u"результат.", 90.26, u"результат"),
        # punctuation only
        (u"анімацій", 31.43, u"анімацій,"), (u"менше", 32.67, u"менше,"), (u"одно", 49.97, u"одно,"),
        (u"більше", 69.38, u"більше,"), (u"телефона", 70.60, u"телефона,"), (u"пам'ять", 73.45, u"пам'ять,"),
        (u"перегріється.", 74.17, u"перегріється,"), (u"інвестувати.", 81.53, u"інвестувати,"),
        (u"напишу", 84.58, u"напишу,"),
    ]
    for w, near, new in edits:
        caps[find(w, near)]["w"] = new
    for w, near in [(u"дати", 62.92)]:          # «Ви дати» -> «віддати»
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
    "skilky": S(u"Скільки", 0.41), "khvylyn": S(u"хвилин", 1.17), "rilsa": S(u"рілса", 2.97),
    "systema": S(u"система", 3.63), "nalashtovana": S(u"налаштована", 4.31), "khochetsia": S(u"хочеться", 6.85),
    "n1015": S(u"10-15", 8.53), "vse": S(u"все", 9.59), "prodazhna": S(u"продажна", 11.14),
    "pravdyva": S(u"правдива", 12.36), "zalezhyt": S(u"залежить", 15.44), "pochatkovoho": S(u"початкового", 16.10),
    "rilsa2": S(u"рілса", 16.78),
    "koly": S(u"Коли", 17.33), "ekspertni": S(u"експертні", 19.12), "chytaiu": S(u"читаю", 20.76),
    "sufliera": S(u"суфлера", 21.18), "minimum": S(u"мінімум", 23.32), "syre": S(u"сире", 24.50),
    "pauzamy": S(u"паузами", 25.32), "n23": S(u"2-3", 26.60), "klod": S(u"Клод", 28.77),
    "n1520": S(u"15-20", 29.52), "bilshe": S(u"більше", 31.19), "dovshe": S(u"довше", 32.11),
    "menshe": S(u"менше", 32.67), "shvydshe": S(u"швидше", 33.07),
    "yakshcho": S(u"Якщо", 33.73), "dovshe2": S(u"довше", 34.46), "n56": S(u"5-6", 35.59),
    "pomylok": S(u"помилок", 36.60), "vyrizaty": S(u"вирізати", 38.16), "chastynu": S(u"частину", 38.64),
    "try": S(u"три", 39.30), "n30": S(u"30", 41.45), "hodynu": S(u"годину", 42.51),
    "tobto": S(u"Тобто", 43.13), "pohanykh": S(u"поганих", 45.28), "dovshe3": S(u"довше", 47.02),
    "pratsiuie": S(u"працює", 47.48),
    "ale": S(u"Але", 48.13), "shvydshe2": S(u"швидше", 51.35), "samii": S(u"самій", 52.23),
    "montazhera": S(u"монтажера", 54.09), "bezkoshtovno": S(u"безкоштовно", 55.27),
    "pidpysku": S(u"підписку", 57.13), "klod2": S(u"Клод", 57.79),
    "i_yakshcho": S(u"якщо", 58.38), "zranku": S(u"зранку", 60.66), "n10": S(u"10", 61.42),
    "montazh": S(u"монтаж", 63.30), "klodi": S(u"Клоді", 63.84), "kilka": S(u"кілька", 64.72),
    "n10b": S(u"10", 66.21), "hotovykh": S(u"готових", 66.55), "spravamy": S(u"справами", 68.43),
    "tym": S(u"Тим", 69.07), "telefona": S(u"телефона", 70.60), "pryviazana": S(u"прив'язана", 71.34),
    "kompiutera": S(u"комп'ютера", 71.92), "pamiat": S(u"пам'ять", 73.45),
    "perehriietsia": S(u"перегріється", 74.17), "montuietsia": S(u"монтується", 75.47),
    "khmari": S(u"хмарі", 75.99),
    "khochesh": S(u"хочеш", 78.11), "vpevnena": S(u"впевнена", 78.87), "ai": S(u"АІ-монтаж", 79.63),
    "investuvaty": S(u"інвестувати", 81.53), "pyshit": S(u"пишіть", 82.62), "test": S(u"ТЕСТ", 83.00),
    "napyshu": S(u"напишу", 84.58), "skynesh": S(u"скинеш", 85.59), "zmontuiu": S(u"змонтую", 87.73),
    "claude": S(u"Claude", 89.04), "rezultat": S(u"результат", 90.26), "treba": S(u"треба", 91.74),
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


L = []
BEATS = []


def beat(fn):
    BEATS.append(fn)
    return fn


k.css("""
.hide { opacity: 0; visibility: hidden; }
.ab { position: absolute; }
.bub { position: absolute; padding: 22px 30px; border-radius: 30px; font-family: "GSans", sans-serif;
       font-size: 36px; font-weight: 500; line-height: 1.25; max-width: 600px; }
.bub.in { background: #f1f3f4; color: #202124; border-bottom-left-radius: 8px; }
.bub.me { background: #d3e3fd; color: #041e49; border-bottom-right-radius: 8px; }
.av { position: absolute; width: 64px; height: 64px; border-radius: 50%; display: grid; place-items: center;
      font-family: "GSans", sans-serif; font-weight: 700; font-size: 30px; color: #fff; }
.lbl { font-family: "GSans", sans-serif; font-size: 26px; font-weight: 700; letter-spacing: .14em;
       color: #5f6368; text-transform: uppercase; position: absolute; }
.row { position: absolute; display: flex; align-items: center; gap: 26px; font-family: "GSans", sans-serif; }
.trk { position: absolute; height: 36px; border-radius: 18px; background: #f1f3f4; overflow: hidden; }
.trk i { display: block; height: 100%; border-radius: 18px; transform-origin: 0 50%; }
.ndl { position: absolute; width: 8px; border-radius: 4px; background: #EA4335; transform-origin: 50% 100%; }
.kpill { position: absolute; display: flex; align-items: center; gap: 16px; padding: 0 34px; height: 96px;
         border-radius: 48px; background: #fff; box-shadow: var(--e3); font-family: "GSans", sans-serif;
         font-weight: 700; font-size: 44px; color: #202124; }
.kpill .dt { width: 34px; height: 34px; border-radius: 50%; background: #4285F4; }
""")


def stopwatch(cx, cy, r, color="ink"):
    return (sk.ellipse(cx, cy, r, r, stroke=color, sw=5) +
            sk.rect(cx - r * 0.18, cy - r - r * 0.32, r * 0.36, r * 0.22, stroke=color, sw=4, round_=False) +
            sk.line([(cx + r * 0.72, cy - r * 0.72), (cx + r * 0.9, cy - r * 0.9)], stroke=color, sw=5, double=False))


def film(x, y, w, h, n):
    """a raw clip, drawn as a film strip: frame + sprocket holes top and bottom"""
    out = sk.rect(x, y, w, h, stroke="ink", sw=5, fill="ink", style="hachure")
    step = w / float(n)
    for i in range(n):
        hx = x + step * i + step * 0.3
        out += sk.rect(hx, y + 10, step * 0.4, 16, stroke="ink", sw=3, round_=False)
        out += sk.rect(hx, y + h - 26, step * 0.4, 16, stroke="ink", sw=3, round_=False)
    return out


# ---------------------------------------------------------------- 1 hook: the stopwatch card (NEAR)
L.append(
    '<div class="g" id="hk" style="top:0;height:700px">'
    '<div class="gcard hide" id="hkC" style="left:120px;top:110px;width:840px;height:300px">'
    + sk.svg(840, 300, stopwatch(150, 165, 92), sid="hkW") +
    '<div class="ndl hide" id="hkN" style="left:146px;top:95px;height:70px"></div>'
    '<div class="lbl" style="left:290px;top:52px">монтаж 1 рілса</div>'
    '<div class="num hide" id="hkQ" style="position:absolute;left:290px;top:84px;font-size:110px">? хв</div>'
    '<div class="num hide" id="hkV" style="position:absolute;left:290px;top:84px;font-size:110px;color:#1a73e8">10–15 хв</div>'
    + sk.svg(840, 300, sk.scribble(285, 120, 470, 70, sw=9), sid="hkX") +
    '<div class="ab hide" id="hkS" style="left:290px;top:210px"><span class="chip cg">система налаштована</span></div>'
    '<div class="hand hide" id="hkZ" style="position:absolute;left:292px;top:208px;font-size:58px;color:#EA4335">залежить від рілса!</div>'
    '</div></div>')


@beat
def b_hook():
    sfx("pop", "@skilky-0.1")
    sfx("pop", "@nalashtovana")
    sfx("ping", "@n1015")
    sfx("pencil", "@pravdyva", -2)
    sfx("pencil", "@zalezhyt", -4)
    return js("""
  h.show("#hk", @skilky-0.15);
  h.pop("#hkC", @skilky-0.15, {s: 0.7, r: -3});
  h.draw("#hkW", @skilky+0.05, 0.7);
  h.show("#hkN", @skilky+0.2);
  tl.fromTo("#hkN", {rotation: 0}, {rotation: 720, duration: 2.6, ease: "power2.inOut"}, @skilky+0.3);
  h.pop("#hkQ", @khvylyn, {s: 0.5, r: 0, y: 10});
  h.wiggle("#hkQ", @rilsa);
  h.pop("#hkS", @nalashtovana, {s: 0.5, r: -4});
  h.fadeOut("#hkS", @khochetsia, 0.25);
  h.fadeOut("#hkQ", @n1015-0.15, 0.15);
  h.pop("#hkV", @n1015-0.05, {s: 0.5, r: 3, y: 0});
  tl.fromTo("#hkN", {rotation: 720}, {rotation: 810, duration: 0.6, ease: SP, immediateRender: false}, @n1015);
  h.bump("#hkV", @vse);
  h.draw("#hkX", @pravdyva-0.05, 0.5);
  tl.to("#hkV", {autoAlpha: 0.35, duration: 0.3}, @pravdyva+0.4);
  h.write("#hkZ", @zalezhyt-0.05, 0.8);
  h.wiggle("#hkW", @pochatkovoho);
  tl.to("#hkC", {y: -40, scale: 0.9, autoAlpha: 0, duration: 0.35, ease: "power2.in"}, @rilsa2+0.25);
  tl.set("#hk", {autoAlpha: 0}, @rilsa2+0.65);
""")


# ---------------------------------------------------------------- 2 board A: how long (HALFSCREEN)
HA = 930
L.append(
    '<div class="g full" id="bA">'
    '<div class="sheet board-bg hide" id="bAS" style="height:%dpx">'
    '<div id="camA" style="position:absolute;left:0;top:0;width:1080px;height:1900px">'
    # --- section 1: my reels
    '<div class="lbl hide" id="aL" style="left:90px;top:66px">мої рілси</div>'
    '<div class="hand hide" id="aE" style="position:absolute;left:88px;top:100px;font-size:66px">експертні відео</div>'
    % HA
    + sk.svg(1080, 1900, sk.rect(90, 225, 360, 230, stroke="ink", sw=5) +
             sk.line([(130, 285), (300, 282), (410, 287)], stroke="#3c4043", sw=5, double=False) +
             sk.line([(130, 335), (260, 338), (400, 333)], stroke="#3c4043", sw=5, double=False) +
             sk.line([(130, 385), (330, 382), (380, 386)], stroke="#3c4043", sw=5, double=False), sid="aT") +
    '<div class="hand hide" id="aTl" style="position:absolute;left:96px;top:470px;font-size:52px">суфлер</div>'
    '<div class="ab hide" id="aM" style="left:90px;top:545px"><span class="chip cg">мінімум помилок</span></div>'
    + sk.svg(1080, 1900, film(560, 225, 430, 170, 6), sid="aF") +
    '<div class="hand hide" id="aFl" style="position:absolute;left:566px;top:408px;font-size:52px">сире відео</div>'
    '<div class="num hide" id="aF3" style="position:absolute;left:566px;top:470px;font-size:92px">2–3 хв</div>'
    + sk.svg(1080, 1900, sk.arrow([(700, 590), (640, 650), (540, 690)], stroke="blue"), sid="aA1") +
    '<div class="kpill hide" id="aK" style="left:220px;top:650px"><span class="dt"></span>Клод</div>'
    + sk.svg(1080, 1900, sk.arrow([(500, 745), (560, 770), (610, 750)], stroke="blue"), sid="aA2") +
    sk.svg(1080, 1900, stopwatch(675, 735, 38, color="green"), sid="aW") +
    '<div class="num hide" id="aV" style="position:absolute;left:730px;top:690px;font-size:84px;color:#188038">15–20 хв</div>'
    # the animation slider
    '<div class="hand hide" id="aSl" style="position:absolute;left:90px;top:800px;font-size:50px">анімації</div>'
    '<div class="trk hide" id="aTr" style="left:330px;top:816px;width:380px"><i id="aTi" style="background:#FBBC04"></i></div>'
    '<div class="hand hide" id="aDl" style="position:absolute;left:740px;top:800px;font-size:52px;color:#EA4335">довше</div>'
    '<div class="hand hide" id="aSh" style="position:absolute;left:740px;top:800px;font-size:52px;color:#34A853">швидше</div>'
    # --- section 2 (y 930..1820): the long, messy video
    '<div class="lbl hide" id="bL" style="left:90px;top:996px">якщо відео довше</div>'
    + sk.svg(1080, 1900, film(90, 1060, 900, 170, 11), sid="bF") +
    '<div class="num hide" id="bF6" style="position:absolute;left:96px;top:1250px;font-size:92px">5–6 хв</div>'
    + sk.svg(1080, 1900, sk.cross(190, 1115, 60, sw=9) + sk.cross(380, 1115, 60, sw=9) +
             sk.cross(610, 1115, 60, sw=9) + sk.cross(820, 1115, 60, sw=9), sid="bX") +
    '<div class="hand hide" id="bXl" style="position:absolute;left:420px;top:1262px;font-size:52px;color:#EA4335">купа помилок</div>'
    + sk.svg(1080, 1900, sk.line([(560, 1030), (556, 1150), (562, 1262)], stroke="red", sw=8, double=False), sid="bC") +
    '<div class="hand hide" id="bCl" style="position:absolute;left:470px;top:960px;font-size:50px;color:#EA4335">3 хв</div>'
    + sk.svg(1080, 1900, sk.rect(572, 1068, 412, 154, stroke="red", sw=4, fill="red", style="cross"), sid="bT") +
    '<div class="kpill hide" id="bK" style="left:90px;top:1380px"><span class="dt"></span>Клод</div>'
    + sk.svg(1080, 1900, sk.arrow([(380, 1428), (440, 1450), (500, 1430)], stroke="blue"), sid="bA2") +
    sk.svg(1080, 1900, stopwatch(560, 1425, 38, color="red"), sid="bW") +
    '<div class="num hide" id="bV" style="position:absolute;left:618px;top:1378px;font-size:84px;color:#c5221f">30 хв</div>'
    '<div class="num hide" id="bV2" style="position:absolute;left:618px;top:1480px;font-size:84px;color:#c5221f">1 год</div>'
    + sk.svg(1080, 1900, sk.circle_around(720, 1530, 140, 62, stroke="red", sw=6), sid="bO") +
    # the formula
    '<div class="hand hide" id="bP" style="position:absolute;left:90px;top:1640px;font-size:54px">погані вхідні дані</div>'
    + sk.svg(1080, 1900, sk.arrow([(560, 1720), (562, 1640)], stroke="red", sw=6, head=24), sid="bPu") +
    sk.svg(1080, 1900, sk.arrow([(610, 1680), (690, 1676), (760, 1682)], stroke="ink"), sid="bPa") +
    '<div class="hand hide" id="bD" style="position:absolute;left:785px;top:1640px;font-size:54px;color:#EA4335">довше</div>'
    + sk.svg(1080, 1900, sk.arrow([(960, 1720), (962, 1640)], stroke="red", sw=6, head=24), sid="bDu") +
    '</div></div></div>')


@beat
def b_boardA():
    sfx("whoosh-short", "@koly-0.2")
    sfx("pencil", "@ekspertni", -4)
    sfx("pencil", "@chytaiu", -3)
    sfx("pop", "@minimum")
    sfx("pencil", "@syre-0.1", -3)
    sfx("pop", "@n23")
    sfx("pop", "@klod")
    sfx("ping", "@n1520")
    sfx("click-soft", "@bilshe")
    sfx("whoosh-short", "@yakshcho-0.15", -4)
    sfx("pencil", "@dovshe2", -3)
    sfx("click", "@pomylok")
    sfx("pencil", "@vyrizaty", -2)
    sfx("ping", "@n30")
    sfx("click", "@hodynu")
    sfx("whoosh-short", "@pratsiuie+0.3")
    return js("""
  h.show("#bA", @koly-0.2);
  h.sheetIn("#bAS", @koly-0.2, %d);
  h.write("#aL", @koly+0.3, 0.3);
  h.write("#aE", @ekspertni-0.1, 0.7);
  h.draw("#aT", @chytaiu-0.1, 0.8);
  h.write("#aTl", @sufliera, 0.45);
  h.pop("#aM", @minimum, {s: 0.5, r: -5});
  h.draw("#aF", @syre-0.1, 1.0);
  h.write("#aFl", @syre+0.1, 0.5);
  h.pop("#aF3", @n23-0.05, {s: 0.5, r: 3, y: 0});
  h.draw("#aA1", @klod-0.4, 0.35);
  h.pop("#aK", @klod-0.1, {s: 0.5, r: -4});
  h.draw("#aA2", @n1520-0.35, 0.3);
  h.draw("#aW", @n1520-0.2, 0.4);
  h.pop("#aV", @n1520-0.05, {s: 0.5, r: 3, y: 0});
  h.write("#aSl", @bilshe-0.35, 0.4);
  h.show("#aTr", @bilshe-0.35);
  tl.fromTo("#aTi", {scaleX: 0.08}, {scaleX: 0.95, duration: 0.6, ease: SP, immediateRender: true}, @bilshe);
  h.write("#aDl", @dovshe-0.05, 0.35);
  tl.to("#aTi", {scaleX: 0.15, duration: 0.5, ease: SP}, @menshe);
  h.fadeOut("#aDl", @menshe, 0.15);
  h.write("#aSh", @shvydshe, 0.4);
  /* pan: the long, messy video */
  h.pan("#camA", @yakshcho-0.15, 0, -930, 1, 0.8);
  h.write("#bL", @yakshcho+0.3, 0.3);
  h.draw("#bF", @dovshe2-0.2, 1.1);
  h.pop("#bF6", @n56-0.05, {s: 0.5, r: -3, y: 0});
  h.draw("#bX", @pomylok-0.1, 0.6);
  h.write("#bXl", @pomylok+0.2, 0.5);
  h.draw("#bC", @vyrizaty, 0.35);
  h.draw("#bT", @chastynu, 0.6);
  h.write("#bCl", @try-0.05, 0.35);
  h.pop("#bK", @n30-0.6, {s: 0.5, r: -4});
  h.draw("#bA2", @n30-0.4, 0.3);
  h.draw("#bW", @n30-0.25, 0.35);
  h.pop("#bV", @n30-0.05, {s: 0.5, r: 3, y: 0});
  h.pop("#bV2", @hodynu-0.05, {s: 0.5, r: -3, y: 0});
  h.draw("#bO", @hodynu+0.3, 0.45);
  h.write("#bP", @pohanykh-0.3, 0.8);
  h.draw("#bPu", @pohanykh+0.6, 0.3);
  h.draw("#bPa", @dovshe3-0.5, 0.3);
  h.write("#bD", @dovshe3-0.1, 0.4);
  h.draw("#bDu", @dovshe3+0.3, 0.3);
  h.sheetOut("#bAS", @pratsiuie+0.3, %d);
  tl.set("#bA", {autoAlpha: 0}, @pratsiuie+1.0);
""" % (HA, HA))


# ---------------------------------------------------------------- 3 comparison sheet (MOVE-DOWN)
HC = 720


def bar_row(rid, top, name, color, sub):
    return ('<div class="gs hide" id="%sN" style="position:absolute;left:90px;top:%dpx;font-size:46px;font-weight:700">%s'
            '<div style="font-size:26px;font-weight:500;color:#5f6368;margin-top:2px">%s</div></div>'
            '<div class="trk hide" id="%sT" style="left:420px;top:%dpx;width:570px"><i id="%sI" style="background:%s"></i></div>'
            % (rid, top, name, sub, rid, top + 22, rid, color))


L.append(
    '<div class="g" id="cm" style="top:0;height:760px">'
    '<div class="sheet hide" id="cmS" style="height:%dpx;background:#fff">'
    '<div class="lbl" style="left:90px;top:70px">час на один рілс</div>' % HC
    + bar_row("r1", 140, u"Клод", "#34A853", u"монтує сам") +
    bar_row("r2", 270, u"самій", "#EA4335", u"власноруч") +
    bar_row("r3", 400, u"монтажер", "#FBBC04", u"чекати") +
    sk.svg(1080, HC, sk.underline(90, 236, 150, stroke="green", sw=7), sid="cmU") +
    '<div class="ab hide" id="cB" style="left:90px;top:560px"><span class="chip cg" style="font-size:40px;height:84px">безкоштовно</span></div>'
    '<div class="ab hide" id="cP" style="left:450px;top:560px"><span class="chip on" style="font-size:40px;height:84px">лише підписка на Клод</span></div>'
    '</div></div>')


@beat
def b_cmp():
    sfx("whoosh-short", "@ale-0.2", -3)
    sfx("pop", "@shvydshe2-0.2")
    sfx("pop", "@samii-0.1")
    sfx("pop", "@montazhera-0.1")
    sfx("kaching", "@bezkoshtovno")
    sfx("pop", "@pidpysku-0.2")
    return js("""
  h.show("#cm", @ale-0.25);
  h.sheetIn("#cmS", @ale-0.25, %d);
  h.pop("#r1N", @shvydshe2-0.25, {s: 0.7, r: 0, y: 12});
  h.show("#r1T", @shvydshe2-0.25);
  tl.fromTo("#r1I", {scaleX: 0}, {scaleX: 0.22, duration: 0.5, ease: SP, immediateRender: true}, @shvydshe2-0.1);
  h.pop("#r2N", @samii-0.15, {s: 0.7, r: 0, y: 12});
  h.show("#r2T", @samii-0.15);
  tl.fromTo("#r2I", {scaleX: 0}, {scaleX: 0.96, duration: 1.0, ease: "power2.out", immediateRender: true}, @samii);
  h.pop("#r3N", @montazhera-0.15, {s: 0.7, r: 0, y: 12});
  h.show("#r3T", @montazhera-0.15);
  tl.fromTo("#r3I", {scaleX: 0}, {scaleX: 0.78, duration: 1.0, ease: "power2.out", immediateRender: true}, @montazhera);
  h.draw("#cmU", @montazhera+1.0, 0.35);
  h.bump("#r1N", @montazhera+1.0);
  h.pop("#cB", @bezkoshtovno-0.05, {s: 0.5, r: -5});
  h.pop("#cP", @pidpysku-0.2, {s: 0.5, r: 4});
  h.sheetOut("#cmS", @i_yakshcho, %d);
  tl.set("#cm", {autoAlpha: 0}, @i_yakshcho+0.7);
""" % (HC, HC))


# ---------------------------------------------------------------- 4 board B: ten reels by lunch (HALFSCREEN)
HB = 930
thumbs, ticks = "", []
for i in range(10):
    x, y = 90 + (i % 5) * 186, 250 + (i // 5) * 140
    thumbs += sk.rect(x, y, 150, 110, stroke="ink", sw=4, fill="blue", style="hachure")
    ticks.append(sk.svg(1080, 1900, sk.check(x + 42, y + 22, 66, sw=9), sid="tk%d" % i))
L.append(
    '<div class="g full" id="bB">'
    '<div class="sheet board-bg hide" id="bBS" style="height:%dpx">'
    '<div id="camB" style="position:absolute;left:0;top:0;width:1080px;height:1900px">' % HB
    + sk.svg(1080, 1900, sk.ellipse(150, 165, 46, 46, stroke="yellow", sw=6, fill="yellow", style="solid") +
             sk.spark(150, 165, 48, stroke="yellow", sw=7), sid="sun") +
    '<div class="hand hide" id="sunT" style="position:absolute;left:240px;top:100px;font-size:66px">зранку</div>'
    + sk.svg(1080, 1900, thumbs, sid="th") +
    '<div class="hand hide" id="thT" style="position:absolute;left:560px;top:110px;font-size:58px;color:#1a73e8">10 рілсів</div>'
    + sk.svg(1080, 1900, sk.arrow([(540, 540), (520, 590), (470, 630)], stroke="blue"), sid="bbA") +
    '<div class="kpill hide" id="bbK" style="left:170px;top:600px"><span class="dt"></span>Клод</div>'
    '<div class="dots hide" id="bbD" style="left:440px;top:633px"><i></i><i></i><i></i><i></i></div>'
    + sk.svg(1080, 1900, stopwatch(640, 650, 36), sid="bbW") +
    '<div class="hand hide" id="bbH" style="position:absolute;left:695px;top:615px;font-size:54px">кілька годин</div>'
    + "".join(ticks) +
    '<div class="hand hide" id="bbM" style="position:absolute;left:90px;top:760px;font-size:56px;color:#1a73e8">а я — своїми справами</div>'
    + sk.svg(1080, 1900, sk.underline(90, 840, 560, stroke="blue", sw=6), sid="bbU") +
    # --- section 2: phone, not a computer; the cloud
    sk.svg(1080, 1900, sk.rect(130, 1000, 210, 380, stroke="ink", sw=6) +
           sk.line([(205, 1350), (265, 1350)], sw=5, double=False) +
           sk.rect(155, 1040, 160, 280, stroke="green", sw=3, fill="green", style="hachure"), sid="ph") +
    '<div class="hand hide" id="phT" style="position:absolute;left:132px;top:1395px;font-size:52px">телефон</div>'
    + sk.svg(1080, 1900, sk.check(360, 1020, 80, sw=10), sid="phC") +
    sk.svg(1080, 1900, sk.rect(560, 1000, 380, 230, stroke="ink", sw=6) +
           sk.line([(520, 1262), (980, 1262)], sw=6), sid="lp") +
    '<div class="hand hide" id="lpT" style="position:absolute;left:600px;top:1275px;font-size:50px">комп\'ютер</div>'
    + sk.svg(1080, 1900, sk.cross(670, 1030, 160, sw=11), sid="lpX") +
    '<div class="ab hide" id="cM" style="left:560px;top:1360px"><span class="chip cr">пам\'ять</span></div>'
    '<div class="ab hide" id="cH" style="left:780px;top:1360px"><span class="chip cr">перегрів</span></div>'
    + sk.svg(1080, 1900, sk.line([(548, 1398), (700, 1392)], stroke="red", sw=7, double=False), sid="cMx") +
    sk.svg(1080, 1900, sk.line([(768, 1398), (950, 1392)], stroke="red", sw=7, double=False), sid="cHx") +
    sk.svg(1080, 1900, sk.ellipse(590, 1590, 90, 75, stroke="blue", sw=5) + sk.ellipse(790, 1575, 110, 85, stroke="blue", sw=5) +
           sk.ellipse(700, 1640, 190, 95, stroke="blue", sw=6, fill="blue", style="solid"),
           sid="cl") +
    '<div class="gs hide" id="clT" style="position:absolute;left:560px;top:1610px;width:280px;text-align:center;font-size:44px;font-weight:700;color:#0b57d0">хмара</div>'
    + sk.svg(1080, 1900, sk.arrow([(345, 1300), (420, 1560), (500, 1620)], stroke="blue", dashed=False), sid="phA") +
    '</div></div></div>')


@beat
def b_boardB():
    sfx("whoosh-short", "@zranku-0.6")
    sfx("pencil", "@zranku-0.1", -4)
    sfx("pencil", "@n10-0.1", -2)
    sfx("pop", "@montazh")
    sfx("pencil", "@kilka", -4)
    sfx("ping", "@hotovykh")
    sfx("whoosh-short", "@tym-0.1", -4)
    sfx("pencil", "@telefona-0.2", -3)
    sfx("click", "@kompiutera+0.1")
    sfx("pop", "@pamiat-0.1")
    sfx("whoosh-short", "@khmari+0.8")
    s = js("""
  h.show("#bB", @zranku-0.6);
  h.sheetIn("#bBS", @zranku-0.6, %d);
  h.draw("#sun", @zranku-0.2, 0.6);
  h.write("#sunT", @zranku, 0.45);
  h.draw("#th", @n10-0.15, 1.1);
  h.write("#thT", @n10, 0.5);
  h.draw("#bbA", @montazh-0.25, 0.3);
  h.pop("#bbK", @montazh, {s: 0.5, r: -4});
  h.pop("#bbD", @klodi+0.2, {s: 0.5, r: 0, y: 0});
  h.think("#bbD", @klodi+0.3, 1.5);
  h.out("#bbD", @kilka+0.2, 0.15);
  h.draw("#bbW", @kilka-0.1, 0.4);
  h.write("#bbH", @kilka, 0.6);
""" % HB)
    for i in range(10):
        s += '  h.draw("#tk%d", %.3f, 0.22);\n' % (i, T["n10b"] - 0.05 + i * 0.07)
    s += js("""
  h.write("#bbM", @spravamy-0.75, 0.8);
  h.draw("#bbU", @spravamy+0.1, 0.35);
  h.pan("#camB", @tym-0.1, 0, -930, 1, 0.8);
  h.draw("#ph", @telefona-0.3, 0.7);
  h.write("#phT", @telefona, 0.4);
  h.draw("#phC", @telefona+0.4, 0.3);
  h.draw("#lp", @pryviazana-0.1, 0.6);
  h.write("#lpT", @kompiutera-0.15, 0.4);
  h.draw("#lpX", @kompiutera+0.15, 0.35);
  h.pop("#cM", @pamiat-0.1, {s: 0.5, r: -4});
  h.draw("#cMx", @pamiat+0.4, 0.25);
  h.pop("#cH", @perehriietsia-0.1, {s: 0.5, r: 4});
  h.draw("#cHx", @perehriietsia+0.45, 0.25);
  h.draw("#phA", @montuietsia-0.2, 0.4);
  h.draw("#cl", @montuietsia+0.1, 0.8);
  h.pop("#clT", @khmari-0.05, {s: 0.6, r: 0, y: 8});
  h.sheetOut("#bBS", @khmari+0.8, %d);
  tl.set("#bB", {autoAlpha: 0}, @khmari+1.5);
""" % HB)
    return s


# ---------------------------------------------------------------- 5 the doubt pill (NEAR)
L.append(
    '<div class="g" id="dq" style="top:0;height:700px">'
    '<div class="pill hide" id="dqP" style="left:230px;top:170px;height:120px;padding:0 54px;font-size:52px;font-weight:700">'
    u'АІ-монтаж</div>'
    '<div class="hand hide" id="dqQ" style="position:absolute;left:650px;top:120px;font-size:150px;color:#EA4335">?</div>'
    '</div>')


@beat
def b_doubt():
    sfx("pop", "@vpevnena-0.1")
    sfx("pencil", "@ai+0.1", -4)
    return js("""
  h.show("#dq", @vpevnena-0.15);
  h.pop("#dqP", @vpevnena-0.15, {s: 0.6, r: -3});
  h.write("#dqQ", @ai+0.1, 0.4);
  h.wiggle("#dqQ", @investuvaty-0.4);
  tl.to("#dqP, #dqQ", {autoAlpha: 0, y: -30, duration: 0.3, ease: "power2.in"}, @investuvaty+0.35);
  tl.set("#dq", {autoAlpha: 0}, @investuvaty+0.7);
""")


# ---------------------------------------------------------------- 6 CTA mockup (MOVE-DOWN)
HD = 740
L.append(
    '<div class="g" id="ct" style="top:0;height:780px">'
    '<div class="sheet hide" id="ctS" style="height:%dpx;background:#fff">'
    '<div class="gs" style="position:absolute;left:90px;top:40px;font-size:34px;font-weight:700">Коментарі</div>'
    '<div style="position:absolute;left:0;right:0;top:100px;height:2px;background:#e8eaed"></div>'
    '<div class="pill" id="cmF" style="left:90px;top:128px;width:900px;height:96px;padding:0 34px;font-size:40px;box-shadow:none;border:2px solid #dadce0">'
    '<span id="cmT" data-text="ТЕСТ" style="font-weight:700;color:#202124"></span>'
    '<span id="cmPh" style="color:#9aa0a6;font-weight:500">Додай коментар…</span></div>'
    '<div class="av hide" id="ruA" style="left:90px;top:270px;background:#EA4335">Р</div>'
    '<div class="bub in hide" id="ruB" style="left:170px;top:258px">Привіт! Скинь одне сире відео</div>'
    '<div class="bub me hide" id="vdB" style="right:90px;top:390px;display:flex;align-items:center;gap:20px">'
    '<span style="display:block;width:96px;height:96px;border-radius:16px;background:#202124;position:relative">'
    '<span style="position:absolute;left:36px;top:28px;width:0;height:0;border-left:32px solid #fff;border-top:20px solid transparent;border-bottom:20px solid transparent"></span></span>'
    'сире відео</div>'
    '<div class="kpill hide" id="clK" style="left:90px;top:560px;box-shadow:var(--e1)"><span class="dt"></span>Claude</div>'
    '<div class="dots hide" id="clD" style="left:370px;top:593px"><i></i><i></i><i></i><i></i></div>'
    '<div class="bub in hide" id="rsB" style="left:400px;top:566px;font-weight:700">Готово: твій рілс</div>'
    % HD
    + sk.svg(1080, HD, sk.check(880, 560, 80, sw=10), sid="rsC") +
    '</div></div>')


@beat
def b_cta():
    sfx("whoosh-short", "@pyshit-0.5", -4)
    sfx("key-press", "@test")
    sfx("notification", "@napyshu-0.1")
    sfx("pop", "@skynesh")
    sfx("click-soft", "@zmontuiu+0.1")
    sfx("ping", "@rezultat-0.1")
    s = js("""
  h.show("#ct", @pyshit-0.5);
  h.sheetIn("#ctS", @pyshit-0.5, %d);
  tl.set("#cmPh", {autoAlpha: 0}, @test-0.05);
  h.type("#cmT", @test-0.05, 9);
  h.bump("#cmF", @test+0.5);
  h.pop("#ruA", @napyshu-0.2, {s: 0.4, r: 0, y: 0});
  h.pop("#ruB", @napyshu-0.1, {s: 0.6, r: -2});
  h.pop("#vdB", @skynesh, {s: 0.6, r: 2});
  h.pop("#clK", @zmontuiu, {s: 0.5, r: -3});
  h.pop("#clD", @zmontuiu+0.2, {s: 0.5, r: 0, y: 0});
  h.think("#clD", @zmontuiu+0.3, 1.7);
  h.out("#clD", @rezultat-0.3, 0.15);
  h.pop("#rsB", @rezultat-0.15, {s: 0.6, r: 2});
  h.draw("#rsC", @rezultat+0.3, 0.35);
  h.bump("#rsB", @treba);
""" % HD)
    return s


BLACKOUT = [
    (T["n1015"] - 0.05, T["n1015"] + 0.75, ""),        # «10–15 хв» on the card
    (T["n23"] - 0.05, T["n23"] + 0.7, ""),              # «2–3 хв»
    (T["n1520"] - 0.05, T["n1520"] + 0.75, ""),         # «15–20 хв»
    (T["n56"] - 0.05, T["n56"] + 0.3, ""),              # «5–6 хв»
    (T["n30"] - 0.05, T["n30"] + 0.45, ""),             # «30 хв»
    (T["hodynu"] - 0.05, T["hodynu"] + 0.4, ""),        # «1 год»
    (T["bezkoshtovno"] - 0.05, T["bezkoshtovno"] + 0.5, ""),   # chip безкоштовно
    (T["pidpysku"] - 0.2, T["klod2"] + 0.3, ""),        # chip лише підписка на Клод
    (T["zranku"] - 0.05, T["zranku"] + 0.35, ""),       # «зранку»
    (T["n10"] - 0.05, T["n10"] + 0.75, ""),             # «10 рілсів»
    (T["ai"] - 0.05, T["ai"] + 0.5, ""),                # pill АІ-монтаж
    (T["test"] - 0.05, T["test"] + 0.18, ""),           # the field types ТЕСТ
]
INVERT = []


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
        title=u"Reel 55 — скільки хвилин займає рілс",
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
