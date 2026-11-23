# -*- coding: utf-8 -*-
"""Reel 57 — «Скільки заробляє RUTA». Google x Excalidraw look (STYLE.md §0b).

Cut from her 220 s raw take by tools/cut.py + work/r57/cut-fix.json (no
closeups: no_paint is empty). Only numbers she says on the recording: 70
users, Claude 100, Supabase 35, Vercel 20, 55, AI 15-20 over the app's whole
life, 1.50 per user, costs ~70, earns 60.

The one object is HER GUESS: plus / minus / zero chips at the start, the
scale at the end that answers it.

Chain:  NEAR the RUTA card, «70+ користувачів», a green arrow «перші гроші»,
chips заробляє / витрати -> the card becomes the guess card: chips плюс /
мінус / нуль, a loop «запамʼятай!» -> the card folds to a sticky note -> NEAR
the phone sketch with RUTA inside, a voice note runs into it, five outputs pop
out -> the phone gives way to a crowd of 70+, a quote bubble, rising bars, a
tick -> OVER board 1 wipes in from the crowd: «Скільки коштує розробити?», the
Claude row $100 is scribbled out «не рахую», branches розробка / робота, a
bypass arrow «оминаю» -> board closes onto the hosting card: Supabase + Vercel,
the free-tier toggle flips off, $35 + $20 = $55 -> the AI card: voice -> text,
three inputs feed the four dots, «15–20 $ за весь час», «1 юзер ≈ $1,50» ->
the scraper card: account -> stats, «Meta API · чекаю», «безкоштовно» -> OVER
board 2 wipes in from that chip: the scale, витрати ≈ $70 vs заробляє $60, it
tips — «мінус»; one more person lands, it levels — «нуль» -> board closes onto
the CTA: the guess chips again, the comment types RUTA, a link DM, «посилання
в профілі».

usage: python build.py   (then: python ../tools/sfx.py mix 57)
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

NN = "57"
CUT = json.load(io.open(os.path.join(ROOT, "work", "r" + NN, "cut.json"), encoding="utf-8"))
DUR = 134.083          # (4023 plate frames - 0.5) / 30
FPS = 30
k = Kit(width=1080, height=1920, fps=FPS, duration=DUR)
k.cap_font = "assets/fonts/ProductSans-Bold.ttf"
k.css(sketch_css())
sk = Sketch(seed=41)

NO_PAINT = [tuple(x) for x in CUT["no_paint"]]   # empty on this cut

CAPS = k.load_captions(os.path.join(ROOT, "work", "r" + NN, "captions.json"))


# ---- caption fixes: whisper errors -> the script word / what she said ------
def fix(caps):
    def find(word, near):
        c = min((i for i, c in enumerate(caps) if c["w"] == word), key=lambda i: abs(caps[i]["s"] - near))
        assert abs(caps[c]["s"] - near) < 0.5, (word, near)
        return c
    edits = [
        (u"більшість", 1.15, u"більше"), (u"це", 1.57, u"70"),
        (u"як", 11.54, u"Як"), (u"ноль.", 14.79, u"нуль?"),
        (u"Рута", 19.50, u"RUTA"), (u"твій", 22.32, u"твоїх"), (u"Перепустив", 23.17, u"переписує"),
        (u"декілька", 25.14, u"кілька"),
        (u"на", 27.82, u"не"), (u"коросалі.", 28.22, u"каруселі,"), (u"«Коросели»", 29.84, u"каруселей"),
        (u"по", 33.56, u"пише"), (u"шатраці.", 33.70, u"тредси."),
        (u"корисують", 35.03, u"користуються"),
        (u"для", 57.40, u"для..."), (u"Взагалі,", 57.58, u"взагалі"),
        (u"Versal.", 67.80, u"Vercel."), (u"За", 75.78, u"за"),
        (u"Versal", 79.11, u"Vercel"), (u"20,", 79.53, u"20."),
        (u"це власне", 83.86, u"це, власне,"), (u"і на", 89.86, u"на"),
        (u"додатку", 93.13, u"додатку"), (u"На", 93.57, u"на"), (u"штучне", 93.73, u"штучний"),
        (u"теле", 94.13, u"інтелект"), (u"15", 95.30, u"15–20"), (u"доларів", 96.87, u"доларів."),
        (u"кожен", 97.30, u"Кожен"), (u"$1", 100.15, u"долар"), (u".50,", 100.43, u"пʼятдесят,"),
        (u"на", 109.49, u"до"), (u"API,", 109.69, u"API."),
        (u"Загалом", 115.80, u"Загалом,"), (u"зйомок.", 26.75, u"зйомок,"), (u"і", 27.28, u"і"),
        (u"шаблонів.", 32.53, u"шаблонів,"), (u"роботи,", 58.44, u"роботи."), (u"мінусі,", 123.13, u"мінусі."), (u"але", 123.51, u"Але"),
    ]
    for w, near, new in edits:
        caps[find(w, near)]["w"] = new
    drop = [(u"видастся", 1.71), (u"20", 96.13), (u"це", 35.55), (u"б", 124.23)]
    for w, near in drop:
        i = find(w, near)
        caps[i - 1]["e"] = caps[i]["e"]
        del caps[i]
    # the CTA: whisper's «пишу Словерута» and the aligner's script words over
    # what she actually said — rebuilt from the cut's own word timings
    words = json.load(io.open(os.path.join(ROOT, "work", "r" + NN, "words.json"), encoding="utf-8"))["words"]
    caps = [c for c in caps if c["s"] < 127.6]
    tail = [w for w in words if w["s"] >= 127.6]
    spell = {u"пишу": u"пиши", u"додаток,": u"додаток."}
    for w in tail:
        t = spell.get(w["w"], w["w"])
        if t == u"Словерута,":
            m = round((w["s"] + w["e"]) / 2, 3)
            caps.append({"w": u"слово", "s": w["s"], "e": m})
            caps.append({"w": u"«RUTA»,", "s": m, "e": w["e"]})
            continue
        if t == u"а" and w["s"] > 131:
            t = u"А"
        caps.append({"w": t, "s": w["s"], "e": w["e"]})
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
    # intro
    "v": S(u"В", 0.0), "s70": S(u"70", 1.57), "korystuvachiv": S(u"користувачів", 2.17),
    "zarobliaie": S(u"заробляє", 3.33), "hroshi": S(u"гроші", 4.17), "chesne": S(u"чесне", 5.58),
    "zarobliaie2": S(u"заробляє", 7.08), "vytraty": S(u"витрати", 9.14),
    # the guess
    "ale": S(u"Але", 9.77), "pohraiemo": S(u"пограємо", 10.80), "pliuc": S(u"плюс", 12.94),
    "minusi": S(u"мінусі", 13.78), "nul": S(u"нуль", 14.79), "zapamiatai": S(u"Запамʼятай", 15.09),
    "kintsi": S(u"кінці", 16.47), "prava": S(u"права", 17.47),
    # the app
    "dlia": S(u"Для", 17.93), "ruta": S(u"RUTA", 19.50), "prodiuser": S(u"продюсер", 20.16),
    "dumok": S(u"думок", 21.78), "holosovykh": S(u"голосових", 22.48), "perepysuie": S(u"переписує", 23.17),
    "storiteli": S(u"сторітели", 24.50), "rilsy": S(u"рілси", 26.23), "karuseli": S(u"каруселі", 28.22),
    "dyzain": S(u"дизайн", 29.38), "vosmy": S(u"восьми", 31.06), "tredsy": S(u"тредси", 33.70),
    # the people
    "tsym": S(u"Цим", 34.30), "p70": S(u"70", 36.35), "odnoholosno": S(u"одноголосно", 37.89),
    "spasinnia": S(u"спасіння", 39.26), "postyty": S(u"постити", 41.55), "sproshchuie": S(u"спрощує", 43.87),
    "zhyttia": S(u"життя", 45.62),
    # board 1: Claude
    "to": S(u"То", 46.13), "koshtuie": S(u"коштує", 47.03), "klod": S(u"Клод", 50.45),
    "s100": S(u"100", 51.75), "rakhuiu": S(u"рахую", 54.28), "rozrobky": S(u"розробки", 56.50),
    "roboty": S(u"роботи", 58.44), "chystoty": S(u"чистоти", 59.60), "omynaiu": S(u"оминаю", 61.20),
    # hosting
    "dali": S(u"Далі", 61.87), "bazu": S(u"базу", 64.96), "supabase": S(u"Supabase", 65.90),
    "khostynh": S(u"хостинг", 66.96), "vercel": S(u"Vercel", 67.80),
    "bezkoshtovnomu": S(u"безкоштовному", 69.54), "korystuvachiv2": S(u"користувачів", 71.10),
    "pidkhodiat": S(u"підходять", 74.92), "supabase2": S(u"Supabase", 76.04), "s35": S(u"35", 77.08),
    "vercel2": S(u"Vercel", 79.11), "s20": S(u"20", 79.53), "razom": S(u"разом", 80.25), "s55": S(u"55", 81.25),
    # AI
    "nastupna": S(u"Наступна", 82.53), "shtuchnyi": S(u"штучний", 84.32), "holosovi": S(u"голосові", 86.20),
    "tekst": S(u"текст", 87.60), "heneratsiia": S(u"генерація", 88.06), "holosovomu": S(u"голосовому", 89.98),
    "pamiati": S(u"памʼяті", 90.98), "analitytsi": S(u"аналітиці", 91.50),
    "za": S(u"За", 92.30), "isnuvannia": S(u"існування", 92.69), "pishlo": S(u"пішло", 94.47),
    "s15": S(u"15–20", 95.30), "kozhen": S(u"Кожен", 97.30), "dolar": S(u"долар", 100.15),
    "kruto": S(u"круто", 101.91),
    # scraper
    "i_shche": S(u"І", 102.43), "skreiper": S(u"скрейпер", 103.74), "statystyku": S(u"статистику", 105.28),
    "chekaiu": S(u"чекаю", 107.75), "api": S(u"API", 109.69), "bezkoshtovno": S(u"безкоштовно", 111.44),
    "platformu": S(u"платформу", 113.34), "taryfamy": S(u"тарифами", 115.04),
    # board 2: the scale
    "zahalom": S(u"Загалом", 115.80), "vytraty3": S(u"витрати", 116.97), "s70b": S(u"70", 118.73),
    "zarobliaie3": S(u"заробляє", 120.03), "s60": S(u"60", 121.10), "tobto": S(u"Тобто", 122.19),
    "minusi2": S(u"мінусі", 123.13), "odna": S(u"одна", 125.03), "liudyna": S(u"людина", 125.61),
    "oplatyt": S(u"оплатить", 125.95), "nul2": S(u"нуль", 127.35),
    # CTA
    "tomu_cta": S(u"Тому", 127.70), "vhadala": S(u"вгадала", 128.29), "pyshy": S(u"пиши", 128.79),
    "slovo": S(u"слово", 129.07), "posylannia": S(u"посилання", 130.09), "ne_vh": S(u"не", 131.46),
    "shukai": S(u"шукай", 132.26), "profili": S(u"профілі", 133.62),
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
.ab { position: absolute; }
.bub { position: absolute; padding: 22px 30px; border-radius: 30px; font-family: "GSans", sans-serif;
       font-size: 36px; font-weight: 500; line-height: 1.25; max-width: 600px; }
.bub.in { background: #f1f3f4; color: #202124; border-bottom-left-radius: 8px; }
.bub.me { background: #d3e3fd; color: #041e49; border-bottom-right-radius: 8px; }
.lbl { font-family: "GSans", sans-serif; font-size: 26px; font-weight: 700; letter-spacing: .14em;
       color: #5f6368; text-transform: uppercase; position: absolute; }
.row { position: absolute; display: flex; align-items: center; gap: 22px; font-family: "GSans", sans-serif; }
.wm { font-family: "GSans", sans-serif; font-weight: 700; letter-spacing: .02em; color: #202124; }
.chip.big, .chip.mid { white-space: nowrap; }
.chip.big { height: 104px; font-size: 50px; padding: 0 40px; border-radius: 28px; font-weight: 700; }
.chip.mid { height: 84px; font-size: 40px; padding: 0 32px; border-radius: 24px; }
.chip.gr { background: #f1f3f4; border-color: #f1f3f4; color: #3c4043; }
.price { position: absolute; font-family: "GSans", sans-serif; font-weight: 700; letter-spacing: -0.03em;
         color: #202124; }
""")


def avatar(cx, cy, r=34, stroke="ink", fill=None):
    """a hand-drawn person: head + shoulders"""
    body = [(cx - r * 1.35, cy + r * 2.6), (cx - r * 1.1, cy + r * 1.6), (cx, cy + r * 1.25),
            (cx + r * 1.1, cy + r * 1.6), (cx + r * 1.35, cy + r * 2.6)]
    return (sk.ellipse(cx, cy, r, r, stroke=stroke, sw=4, fill=fill, style="solid") +
            sk.line(body, stroke=stroke, sw=4, double=False))


# ================================================================ 0 sheet A: the move-down
# (STYLE.md §0c) every near card here is a mockup or a small scheme, so one
# white sheet drops at the start and holds her plate 140 px down for the whole
# reel; the two halfscreen boards drop over it and roll back up onto it.
SH = 700
L.append('<div class="g full" id="shA"><div class="sheet board-bg hide" id="shAS" style="height:%dpx"></div></div>' % SH)


@beat
def b_sheet():
    sfx("whoosh-short", 0.0, -6)
    return js("""
  h.show("#shA", 0);
  h.sheetIn("#shAS", 0, %d, 140, 0.7);
""" % SH)


# ================================================================ 1 the RUTA card
L.append(
    '<div class="g" id="ru" style="top:0;height:700px">'
    '<div class="gcard" id="ruC" style="left:90px;top:70px;width:900px;height:540px">'
    '<div class="pill" id="ruW" style="left:50px;top:44px;height:96px;padding:0 40px;box-shadow:var(--e1);background:#202124">'
    '<span class="wm" style="font-size:52px;color:#fff">RUTA</span></div>'
    '<div class="lbl" style="left:340px;top:76px">мій додаток</div>'
    '<div class="num hide" id="ruN" style="position:absolute;left:50px;top:170px;font-size:190px;line-height:1">70+</div>'
    '<div class="hand hide" id="ruNT" style="position:absolute;left:60px;top:370px;font-size:54px">користувачів</div>'
    + sk.svg(900, 540, sk.arrow([(520, 400), (610, 300), (720, 190)], stroke="green", sw=7, head=36), sid="ruA") +
    '<div class="hand hide" id="ruAT" style="position:absolute;left:560px;top:400px;font-size:52px;color:#34A853">перші гроші</div>'
    '<div class="row hide" id="ruR" style="left:50px;top:420px">'
    '<span class="chip mid cg" id="ruC1">заробляє</span><span class="chip mid cr" id="ruC2">витрати</span></div>'
    '</div></div>')


@beat
def b_ruta():
    sfx("pop", "@v+0.1")
    sfx("pop", "@s70")
    sfx("pencil", "@zarobliaie", -3)
    sfx("kaching", "@hroshi", -4)
    sfx("pop", "@zarobliaie2")
    sfx("pop", "@vytraty")
    return js("""
  h.show("#ru", @v);
  h.pop("#ruC", @v+0.05, {s: 0.8, r: -2});
  h.count("#ruN", @s70-0.1, 70, 0.7, function (v) { return Math.round(v) + "+"; });
  h.pop("#ruN", @s70-0.1, {s: 0.6, r: 0, y: 10});
  h.write("#ruNT", @korystuvachiv, 0.45);
  h.draw("#ruA", @zarobliaie, 0.55);
  h.write("#ruAT", @hroshi-0.3, 0.5);
  /* the honest video: earnings vs costs */
  tl.to("#ruN, #ruNT", {autoAlpha: 0, y: -20, duration: 0.3, ease: "power2.in"}, @chesne);
  h.undraw("#ruA", @chesne, 0.3);
  h.fadeOut("#ruAT", @chesne, 0.3);
  h.show("#ruR", @zarobliaie2-0.1);
  h.pop("#ruC1", @zarobliaie2-0.05, {s: 0.5, r: -4});
  h.pop("#ruC2", @vytraty, {s: 0.5, r: 4});
  tl.to("#ruC", {scale: 0.5, y: -40, autoAlpha: 0, duration: 0.35, ease: "power3.in"}, @ale-0.05);
  tl.set("#ru", {autoAlpha: 0}, @ale+0.35);
""")


# ================================================================ 2 the guess
L.append(
    '<div class="g" id="gs" style="top:0;height:700px">'
    '<div class="gcard" id="gsC" style="left:90px;top:70px;width:900px;height:540px">'
    '<div class="hand hide" id="gsT" style="position:absolute;left:60px;top:46px;font-size:76px">Вгадай:</div>'
    + sk.svg(900, 540, sk.underline(62, 148, 300, stroke="blue"), sid="gsU") +
    '<div class="ab" style="left:60px;top:240px;width:800px;display:flex;gap:26px;justify-content:center">'
    '<span class="chip big cg hide" id="g1">+ плюс</span>'
    '<span class="chip big cr hide" id="g2">− мінус</span>'
    '<span class="chip big gr hide" id="g3">0 нуль</span></div>'
    + sk.svg(900, 540, sk.circle_around(450, 292, 420, 105, stroke="blue", sw=6), sid="gsO") +
    '<div class="hand hide" id="gsZ" style="position:absolute;left:440px;top:420px;font-size:58px;color:#4285F4">запамʼятай!</div>'
    '</div>'
    '<div class="paper hide" id="gsN" style="left:760px;top:60px;width:240px;height:170px;background:#fff7d1">'
    '<div class="hand" style="position:absolute;left:0;right:0;top:20px;text-align:center;font-size:44px">твоя</div>'
    '<div class="hand" style="position:absolute;left:0;right:0;top:78px;text-align:center;font-size:58px;color:#4285F4">відповідь</div>'
    '</div></div>')


@beat
def b_guess():
    sfx("pop", "@ale")
    sfx("pencil", "@pohraiemo-0.2", -3)
    sfx("pop", "@pliuc")
    sfx("pop", "@minusi")
    sfx("pop", "@nul")
    sfx("pencil", "@zapamiatai", -2)
    sfx("whoosh-short", "@kintsi")
    return js("""
  h.show("#gs", @ale-0.05);
  h.pop("#gsC", @ale-0.05, {s: 0.85, r: 2});
  h.write("#gsT", @pohraiemo-0.3, 0.5);
  h.draw("#gsU", @pohraiemo+0.2, 0.35);
  h.pop("#g1", @pliuc-0.05, {s: 0.4, r: -6});
  h.pop("#g2", @minusi-0.05, {s: 0.4, r: 6});
  h.pop("#g3", @nul-0.05, {s: 0.4, r: -6});
  h.draw("#gsO", @zapamiatai, 0.6);
  h.write("#gsZ", @zapamiatai+0.35, 0.5);
  /* the card folds into a sticky note: kept for the end */
  tl.to("#gsC", {scale: 0.25, x: 330, y: -150, autoAlpha: 0, duration: 0.45, ease: "power3.in"}, @kintsi);
  h.pop("#gsN", @kintsi+0.3, {s: 0.4, r: -10, to: -3});
  tl.to("#gsN", {scale: 0.6, autoAlpha: 0, duration: 0.3, ease: "power2.in"}, @prava+0.4);
  tl.set("#gs", {autoAlpha: 0}, @prava+0.75);
""")


# ================================================================ 3 the app: a producer in the phone
OUTS = [("o1", u"сторітели", "on"), ("o2", u"рілси", "cg"), ("o3", u"каруселі", "cy"),
        ("o4", u"8 шаблонів", "cr"), ("o5", u"тредси", "on")]
L.append(
    '<div class="g" id="ap" style="top:0;height:700px">'
    + sk.svg(1080, 700,
             sk.rect(110, 90, 270, 520, stroke="ink", sw=5) +
             sk.line([(205, 125), (285, 125)], sw=5, double=False) +
             sk.ellipse(245, 575, 16, 16, sw=3.5), sid="apP", cls="sk") +
    '<div class="ab hide" id="apS" style="left:128px;top:150px;width:234px;height:420px;border-radius:24px;background:#fff"></div>'
    '<div class="wm hide" id="apW" style="position:absolute;left:110px;top:310px;width:270px;text-align:center;font-size:64px">RUTA</div>'
    '<div class="hand hide" id="apWT" style="position:absolute;left:112px;top:392px;width:266px;text-align:center;font-size:36px">продюсер<br>в телефоні</div>'
    # the voice note
    '<div class="pill hide" id="apV" style="left:470px;top:110px;height:100px;padding:0 34px">'
    '<span style="width:44px;height:44px;border-radius:50%;background:#EA4335;display:inline-block"></span>'
    '<span class="gs" style="font-size:36px;font-weight:700">голосове</span></div>'
    + sk.svg(1080, 700, sk.arrow([(560, 230), (470, 300), (395, 330)], stroke="red", sw=6), sid="apA", cls="sk") +
    '<div class="ab" style="left:430px;top:380px;width:600px;display:flex;flex-wrap:wrap;gap:18px">'
    + "".join('<span class="chip mid %s hide" id="%s">%s</span>' % (c, i, t) for i, t, c in OUTS) +
    '</div></div>')


@beat
def b_app():
    sfx("pencil", "@dlia+0.1", -2)
    sfx("pop", "@ruta")
    sfx("notification", "@holosovykh-0.1", -2)
    sfx("whoosh-short", "@perepysuie")
    for n in ("storiteli", "rilsy", "karuseli", "vosmy", "tredsy"):
        sfx("pop", "@" + n)
    return js("""
  h.show("#ap", @dlia);
  h.draw("#apP", @dlia, 0.9);
  h.show("#apS", @dlia+0.7);
  tl.fromTo("#apS", {autoAlpha: 0}, {autoAlpha: 1, duration: 0.3, immediateRender: false}, @dlia+0.7);
  h.pop("#apW", @ruta-0.05, {s: 0.5, r: 0});
  h.write("#apWT", @prodiuser, 0.6);
  h.pop("#apV", @holosovykh-0.15, {s: 0.5, r: 3});
  h.draw("#apA", @perepysuie, 0.45);
  h.bump("#apW", @perepysuie+0.45);
  h.pop("#o1", @storiteli-0.05, {s: 0.4, r: -5});
  h.pop("#o2", @rilsy-0.05, {s: 0.4, r: 5});
  h.pop("#o3", @karuseli-0.05, {s: 0.4, r: -5});
  h.pop("#o4", @vosmy-0.05, {s: 0.4, r: 5});
  h.pop("#o5", @tredsy-0.1, {s: 0.4, r: -5});
  h.out("#apV", @tredsy+0.4, 0.25);
  h.undraw("#apA", @tredsy+0.3, 0.25);
  tl.to("#ap", {autoAlpha: 0, scale: 0.9, duration: 0.3, ease: "power2.in"}, @tsym-0.1);
""")


# ================================================================ 4 70+ people
CROWD = "".join(avatar(130 + i * 92, 150 + (i % 2) * 22, 30, stroke=("blue", "red", "yellow", "green")[i % 4],
                       fill=("blue", "red", "yellow", "green")[i % 4]) for i in range(10))
BARS = "".join(sk.rect(640 + i * 80, 560 - h, 56, h, stroke="ink", sw=4, fill="blue", round_=False)
               for i, h in enumerate((60, 100, 150, 210)))
L.append(
    '<div class="g" id="pp" style="top:0;height:700px">'
    + sk.svg(1080, 700, CROWD, sid="ppA", cls="sk") +
    '<div class="gcard hide" id="ppN" style="left:90px;top:290px;width:420px;height:280px">'
    '<div class="num" style="position:absolute;left:0;right:0;top:14px;text-align:center;font-size:160px;line-height:1">70+</div>'
    '<div class="hand" style="position:absolute;left:0;right:0;top:206px;text-align:center;font-size:52px">людей</div></div>'
    '<div class="bub in hide" id="ppQ" style="left:560px;top:300px;width:420px;box-shadow:var(--e3);background:#fff">«це спасіння для РДУГ»</div>'
    '<div class="ab hide" id="ppB" style="left:0;top:0;width:1080px;height:700px">'
    + sk.svg(1080, 700, BARS + sk.line([(620, 562), (970, 562)], sw=4, double=False) +
             sk.arrow([(640, 450), (780, 380), (940, 300)], stroke="green", sw=7), sid="ppBS", cls="sk") +
    '<div class="hand" style="position:absolute;left:660px;top:575px;font-size:44px;color:#1e1e1e">пости частіше</div></div>'
    + sk.svg(1080, 700, sk.check(820, 230, 120, sw=11), sid="ppOK", cls="sk") +
    '</div>')


@beat
def b_people():
    sfx("pencil", "@tsym", -2)
    sfx("pop", "@p70")
    sfx("ping", "@spasinnia-0.2", -2)
    sfx("pencil", "@postyty-0.1", -3)
    sfx("sparkle", "@sproshchuie")
    return js("""
  h.show("#pp", @tsym-0.05);
  h.draw("#ppA", @tsym, 1.6);
  h.pop("#ppN", @p70-0.15, {s: 0.6, r: -3});
  h.pop("#ppQ", @spasinnia-0.25, {s: 0.5, r: 3});
  h.out("#ppQ", @postyty-0.25, 0.2);
  h.show("#ppB", @postyty-0.15);
  h.draw("#ppBS", @postyty-0.15, 1.0);
  h.fadeOut("#ppB", @sproshchuie-0.15, 0.25);
  h.draw("#ppOK", @sproshchuie, 0.4);
  h.bump("#ppN", @sproshchuie+0.3);
""")


# ================================================================ 5 OVER: board 1 — Claude
L.append(
    '<div class="g full" id="b1"><div class="sheet board-bg hide" id="b1S" style="height:930px">'
    '<div class="hand hide" id="b1T" style="position:absolute;left:100px;top:50px;font-size:74px">Скільки коштує розробити?</div>'
    + sk.svg(1080, 1300, sk.underline(100, 160, 560, stroke="blue", twice=True), sid="b1U") +
    '<div class="gcard hide" id="b1C" style="left:100px;top:230px;width:880px;height:220px">'
    '<div class="pill" style="left:40px;top:58px;height:104px;padding:0 40px;box-shadow:none;background:#f1f3f4">'
    '<span class="wm" style="font-size:54px">Клод</span></div>'
    '<div class="price hide" id="b1P" style="left:470px;top:42px;font-size:120px">$100</div>'
    '<div class="gs hide" id="b1PM" style="position:absolute;left:760px;top:104px;font-size:36px;color:#5f6368">/ міс</div>'
    + sk.svg(880, 220, sk.scribble(450, 60, 400, 110, stroke="red", sw=8), sid="b1X") +
    '</div>'
    '<div class="hand hide" id="b1NR" style="position:absolute;left:560px;top:460px;font-size:60px;color:#EA4335">не рахую</div>'
    + sk.svg(1080, 1300, sk.arrow([(330, 460), (290, 560), (250, 640)], stroke="ink", sw=5), sid="b1A1")
    + sk.svg(1080, 1300, sk.arrow([(600, 540), (660, 590), (720, 645)], stroke="ink", sw=5), sid="b1A2") +
    '<div class="ab hide" id="b1R1" style="left:110px;top:665px"><span class="chip mid on">розробка</span></div>'
    '<div class="ab hide" id="b1R2" style="left:560px;top:665px"><span class="chip mid cy">уся інша робота</span></div>'
    + sk.svg(1080, 1300, sk.arrow([(60, 220), (40, 520), (90, 770), (380, 845), (620, 830)], stroke="blue", sw=7, head=36),
             sid="b1Y") +
    '<div class="hand hide" id="b1YT" style="position:absolute;left:650px;top:790px;font-size:64px;color:#4285F4">оминаю</div>'
    '</div></div>')


@beat
def b_board1():
    sfx("whoosh-short", "@to-0.1")
    sfx("pencil", "@to+0.3", -2)
    sfx("pop", "@klod-0.1")
    sfx("pop", "@s100")
    sfx("pencil", "@rakhuiu-0.1", -1)
    sfx("pencil", "@rozrobky-0.2", -4)
    sfx("pop", "@rozrobky")
    sfx("pop", "@roboty")
    sfx("pencil", "@omynaiu-0.5", -2)
    sfx("whoosh-short", "@dali-0.3")
    return js("""
  tl.to("#pp", {autoAlpha: 0, duration: 0.3}, @to+0.4);
  h.show("#b1", @to-0.15);
  h.sheetIn("#b1S", @to-0.15, 930);
  h.write("#b1T", @to+0.35, 1.1);
  h.draw("#b1U", @koshtuie+0.6, 0.45);
  h.pop("#b1C", @klod-0.2, {s: 0.8, r: -2});
  h.pop("#b1P", @s100-0.05, {s: 0.5, r: 0});
  h.pop("#b1PM", @s100+0.3, {s: 0.6, r: 0});
  h.draw("#b1X", @rakhuiu-0.1, 0.45);
  h.write("#b1NR", @rakhuiu+0.2, 0.5);
  h.draw("#b1A1", @rozrobky-0.25, 0.3);
  h.pop("#b1R1", @rozrobky-0.05, {s: 0.5, r: -4});
  h.draw("#b1A2", @roboty-0.3, 0.3);
  h.pop("#b1R2", @roboty-0.1, {s: 0.5, r: 4});
  tl.to("#b1C, #b1NR, #b1R1, #b1R2, #b1A1, #b1A2", {opacity: 0.3, duration: 0.4}, @chystoty);
  h.draw("#b1Y", @omynaiu-0.5, 0.7);
  h.write("#b1YT", @omynaiu, 0.4);
  tl.to("#b1S", {y: -970, duration: 0.55, ease: "power3.in"}, @dali-0.3);
  tl.set("#b1", {autoAlpha: 0}, @dali+0.27);
  h.plateDown(@dali-0.25, 140, 0.65);
""")


# ================================================================ 6 hosting: Supabase + Vercel
L.append(
    '<div class="g" id="ho" style="top:0;height:700px">'
    '<div class="gcard" id="hoC" style="left:90px;top:60px;width:900px;height:580px">'
    '<div class="lbl" style="left:50px;top:40px">щоб додаток працював</div>'
    '<div class="row hide" id="hoR1" style="left:50px;top:100px">'
    '<span class="chip big on">Supabase</span><span class="hand" style="font-size:46px">база даних</span></div>'
    '<div class="row hide" id="hoR2" style="left:50px;top:230px">'
    '<span class="chip big cg">Vercel</span><span class="hand" style="font-size:46px">хостинг</span></div>'
    '<div class="price hide" id="hoP1" style="left:700px;top:96px;font-size:96px">$35</div>'
    '<div class="price hide" id="hoP2" style="left:700px;top:226px;font-size:96px">$20</div>'
    # the free tier
    '<div class="ab hide" id="hoF" style="left:50px;top:400px;width:820px;height:120px">'
    '<span class="chip mid gr" style="position:absolute;left:0;top:14px">безкоштовний тариф</span>'
    '<div class="tgl" id="hoTg" style="left:480px;top:24px"><b></b></div>'
    + sk.svg(820, 120, sk.arrow([(610, 100), (650, 50), (690, 10)], stroke="blue", sw=6), sid="hoUA") +
    '<div class="hand" id="hoUT" style="position:absolute;left:700px;top:30px;font-size:40px;color:#4285F4;opacity:0;visibility:hidden">юзерів<br>більше</div>'
    + sk.svg(820, 120, sk.scribble(6, 30, 430, 60, stroke="red", sw=7), sid="hoX") +
    '</div>'
    + sk.svg(900, 580, sk.line([(520, 360), (870, 356)], sw=5, double=True), sid="hoL") +
    '<div class="price hide" id="hoS" style="left:520px;top:380px;font-size:130px;color:#34A853">= $55</div>'
    '</div></div>')


@beat
def b_host():
    sfx("pop", "@supabase-0.1")
    sfx("pop", "@vercel-0.1")
    sfx("click-soft", "@bezkoshtovnomu")
    sfx("pencil", "@korystuvachiv2", -4)
    sfx("click", "@pidkhodiat-0.2")
    sfx("pop", "@s35")
    sfx("pop", "@s20")
    sfx("kaching", "@s55", -3)
    return js("""
  h.show("#ho", @dali-0.1);
  h.pop("#hoC", @dali-0.1, {s: 0.7, r: 0, y: 0});
  h.pop("#hoR1", @supabase-0.15, {s: 0.7, r: -2});
  h.pop("#hoR2", @vercel-0.15, {s: 0.7, r: 2});
  h.pop("#hoF", @bezkoshtovnomu-0.2, {s: 0.8, r: 0, y: 14});
  h.toggle("#hoTg", @bezkoshtovnomu+0.2, "#34A853");
  h.draw("#hoUA", @korystuvachiv2, 0.4);
  h.write("#hoUT", @korystuvachiv2+0.3, 0.5);
  tl.to("#hoTg", {backgroundColor: "#e1e3e1", borderColor: "#747775", duration: 0.18}, @pidkhodiat-0.2);
  tl.to("#hoTg b", {x: 0, scale: 1, backgroundColor: "#747775", duration: 0.45, ease: SP}, @pidkhodiat-0.2);
  h.draw("#hoX", @pidkhodiat, 0.35);
  tl.to("#hoF", {autoAlpha: 0, y: 20, duration: 0.3, ease: "power2.in"}, @supabase2-0.1);
  h.pop("#hoP1", @s35-0.05, {s: 0.5, r: 0});
  h.bump("#hoR1", @s35-0.05);
  h.pop("#hoP2", @s20-0.05, {s: 0.5, r: 0});
  h.bump("#hoR2", @s20-0.05);
  h.draw("#hoL", @razom-0.1, 0.35);
  h.pop("#hoS", @s55-0.1, {s: 0.5, r: -3});
  tl.to("#hoC", {scale: 0.6, autoAlpha: 0, y: -30, duration: 0.35, ease: "power3.in"}, @nastupna-0.1);
  tl.set("#ho", {autoAlpha: 0}, @nastupna+0.3);
""")


# ================================================================ 7 AI
L.append(
    '<div class="g" id="ai" style="top:0;height:700px">'
    '<div class="gcard" id="aiC" style="left:90px;top:60px;width:900px;height:580px">'
    '<div class="gs hide" id="aiT" style="position:absolute;left:50px;top:34px;font-size:52px;font-weight:700">Штучний інтелект</div>'
    + sk.svg(900, 580, sk.underline(50, 104, 430, stroke="yellow"), sid="aiU") +
    # flow: voice -> text
    '<div class="pill hide" id="aiV" style="left:50px;top:150px;height:90px;padding:0 30px;box-shadow:var(--e1)">'
    '<span style="width:38px;height:38px;border-radius:50%;background:#EA4335;display:inline-block"></span>'
    '<span class="gs" style="font-size:34px;font-weight:700">голосове</span></div>'
    + sk.svg(900, 580, sk.arrow([(345, 195), (420, 190), (490, 195)], stroke="ink", sw=5), sid="aiA") +
    '<div class="ab hide" id="aiTx" style="left:520px;top:140px;width:320px;height:110px">'
    '<div class="gs" style="position:absolute;left:0;top:-6px;font-size:30px;color:#5f6368">текст</div>'
    + sk.svg(320, 110, sk.line([(0, 50), (140, 47), (300, 52)], stroke="#3c4043", sw=5, double=False) +
             sk.line([(0, 80), (120, 82), (230, 78)], stroke="#3c4043", sw=5, double=False), sid="aiTxS") +
    '</div>'
    # generation: three inputs feed the four dots
    '<div class="ab" style="left:50px;top:300px;width:400px;display:flex;flex-direction:column;gap:14px">'
    '<span class="chip mid on hide" id="aiI1" style="align-self:flex-start">голосове</span>'
    '<span class="chip mid cg hide" id="aiI2" style="align-self:flex-start">памʼять</span>'
    '<span class="chip mid cy hide" id="aiI3" style="align-self:flex-start">аналітика</span></div>'
    + sk.svg(900, 580, sk.arrow([(360, 400), (450, 410), (540, 420)], stroke="ink", sw=5), sid="aiA2") +
    '<div class="paper hide" id="aiG" style="left:560px;top:320px;width:290px;height:200px">'
    '<div class="dots" id="aiD" style="left:63px;top:52px"><i></i><i></i><i></i><i></i></div>'
    '<div class="hand" style="position:absolute;left:0;right:0;top:118px;text-align:center;font-size:46px">сценарій</div></div>'
    # the money: 15-20 over the whole life, 1.50 per user
    '<div class="ab hide" id="aiM" style="left:50px;top:150px;width:800px;height:400px">'
    '<div class="price" style="left:0;top:0;font-size:150px">$15–20</div>'
    '<div class="hand" style="position:absolute;left:10px;top:180px;font-size:56px">за весь час існування</div>'
    '</div>'
    '<div class="ab hide" id="aiU1" style="left:50px;top:300px;width:800px;height:260px">'
    + sk.svg(800, 260, avatar(70, 70, 46, stroke="blue", fill="blue"), sid="aiUS") +
    '<div class="hand" style="position:absolute;left:150px;top:40px;font-size:56px">1 юзер</div>'
    '<div class="price" style="left:370px;top:22px;font-size:110px">≈ $1,50</div>'
    + sk.svg(800, 260, sk.spark(740, 40, 30, stroke="yellow", sw=7) + sk.underline(380, 160, 380, stroke="green"),
             sid="aiK") +
    '</div>'
    '</div></div>')


@beat
def b_ai():
    sfx("pop", "@nastupna")
    sfx("pencil", "@shtuchnyi", -4)
    sfx("pop", "@holosovi")
    sfx("pencil", "@tekst-0.2", -4)
    sfx("pop", "@holosovomu")
    sfx("pop", "@pamiati")
    sfx("pop", "@analitytsi")
    sfx("whoosh-short", "@za")
    sfx("kaching", "@s15", -4)
    sfx("pop", "@kozhen")
    sfx("sparkle", "@kruto")
    return js("""
  h.show("#ai", @nastupna-0.05);
  h.pop("#aiC", @nastupna-0.05, {s: 0.8, r: 0, y: 0});
  h.write("#aiT", @nastupna+0.4, 0.8);
  h.draw("#aiU", @shtuchnyi+0.3, 0.35);
  h.pop("#aiV", @holosovi-0.1, {s: 0.5, r: -3});
  h.draw("#aiA", @holosovi+0.6, 0.3);
  h.show("#aiTx", @tekst-0.25);
  h.draw("#aiTxS", @tekst-0.25, 0.5);
  h.pop("#aiG", @heneratsiia-0.1, {s: 0.6, r: 2});
  h.pop("#aiI1", @holosovomu-0.1, {s: 0.5, r: -4});
  h.pop("#aiI2", @pamiati-0.1, {s: 0.5, r: 4});
  h.pop("#aiI3", @analitytsi-0.1, {s: 0.5, r: -4});
  h.draw("#aiA2", @analitytsi+0.15, 0.3);
  h.think("#aiD", @heneratsiia+0.3, 3.6);
  /* clear the flow; the money */
  tl.to("#aiV, #aiTx, #aiI1, #aiI2, #aiI3, #aiG", {autoAlpha: 0, scale: 0.9, duration: 0.3, ease: "power2.in"}, @za-0.1);
  h.undraw("#aiA", @za-0.1, 0.25);
  h.undraw("#aiA2", @za-0.1, 0.25);
  h.show("#aiM", @isnuvannia);
  h.write("#aiM .hand", @isnuvannia, 0.9);
  h.pop("#aiM .price", @s15-0.1, {s: 0.5, r: -3});
  tl.to("#aiM", {autoAlpha: 0, y: -40, duration: 0.3, ease: "power2.in"}, @kozhen-0.15);
  h.show("#aiU1", @kozhen-0.05);
  h.draw("#aiUS", @kozhen-0.05, 0.5);
  h.write("#aiU1 .hand", @kozhen+0.4, 0.4);
  h.pop("#aiU1 .price", @dolar-0.1, {s: 0.5, r: 3});
  h.draw("#aiK", @kruto-0.1, 0.5);
  tl.to("#aiC", {scale: 0.6, autoAlpha: 0, y: -30, duration: 0.35, ease: "power3.in"}, @i_shche-0.1);
  tl.set("#ai", {autoAlpha: 0}, @i_shche+0.3);
""")


# ================================================================ 8 the scraper
STATS = (sk.rect(30, 20, 300, 300, stroke="ink", sw=4.5) + avatar(180, 95, 40, stroke="red", fill="red") +
         sk.line([(70, 250), (290, 248)], sw=4, double=False) + sk.line([(70, 285), (230, 287)], sw=4, double=False))
CHART = (sk.line([(480, 300), (480, 40)], sw=4, double=False) + sk.line([(480, 300), (790, 300)], sw=4, double=False) +
         sk.line([(500, 260), (580, 200), (650, 225), (760, 90)], stroke="blue", sw=7, double=False))
L.append(
    '<div class="g" id="sc" style="top:0;height:700px">'
    '<div class="gcard" id="scC" style="left:90px;top:60px;width:900px;height:580px">'
    '<div class="ab" style="left:20px;top:80px;width:860px;height:340px">'
    + sk.svg(860, 340, STATS, sid="scA") +
    '<div class="gs hide" id="scAT" style="position:absolute;left:30px;top:330px;width:300px;text-align:center;font-size:30px;color:#5f6368">акаунт</div>'
    + sk.svg(860, 340, sk.arrow([(345, 170), (400, 150), (460, 170)], stroke="ink", sw=5), sid="scAr")
    + sk.svg(860, 340, CHART, sid="scS") +
    '<div class="gs hide" id="scST" style="position:absolute;left:480px;top:330px;width:310px;text-align:center;font-size:30px;color:#5f6368">статистика</div>'
    '</div>'
    '<div class="hand hide" id="scT" style="position:absolute;left:40px;top:20px;font-size:62px">скрейпер</div>'
    '<div class="row" style="left:40px;top:470px">'
    '<span class="chip mid gr hide" id="scM">Meta API · чекаю…</span>'
    '<span class="chip mid cg hide" id="scF">безкоштовно</span></div>'
    '</div></div>')


@beat
def b_scraper():
    sfx("pop", "@i_shche")
    sfx("pencil", "@skreiper", -3)
    sfx("pencil", "@statystyku", -4)
    sfx("click-soft", "@chekaiu")
    sfx("pop", "@bezkoshtovno")
    return js("""
  h.show("#sc", @i_shche-0.05);
  h.pop("#scC", @i_shche-0.05, {s: 0.8, r: 0, y: 0});
  h.write("#scT", @skreiper-0.1, 0.5);
  h.draw("#scA", @skreiper+0.1, 0.9);
  h.write("#scAT", @skreiper+0.6, 0.3);
  h.draw("#scAr", @statystyku-0.2, 0.3);
  h.draw("#scS", @statystyku, 0.8);
  h.write("#scST", @statystyku+0.5, 0.35);
  h.pop("#scM", @chekaiu-0.1, {s: 0.5, r: -3});
  h.wiggle("#scM", @api);
  h.pop("#scF", @bezkoshtovno-0.1, {s: 0.4, r: 4});
  h.bump("#scF", @taryfamy-0.1);
""")


# ================================================================ 9 OVER: board 2 — the scale
PX, PY = 540, 420                     # the beam's pivot
SC_POST = (sk.line([(PX, PY), (PX - 110, 820)], sw=6, double=True) + sk.line([(PX, PY), (PX + 110, 820)], sw=6, double=True) +
           sk.line([(PX - 200, 822), (PX + 200, 818)], sw=6, double=True) + sk.ellipse(PX, PY, 16, 16, sw=5, fill="ink", style="solid"))
BEAM = sk.line([(PX - 360, PY), (PX + 360, PY)], sw=8, double=True)


def pan(cx, y0, color):
    """strings from the beam end + the bowl, local to a div at the end"""
    return (sk.line([(cx, y0), (cx - 120, y0 + 200)], sw=3.5, double=False) +
            sk.line([(cx, y0), (cx + 120, y0 + 200)], sw=3.5, double=False) +
            sk.line([(cx - 150, y0 + 200), (cx - 110, y0 + 250), (cx + 110, y0 + 250), (cx + 150, y0 + 200)],
                    stroke=color, sw=6, double=True) +
            sk.line([(cx - 150, y0 + 200), (cx + 150, y0 + 200)], stroke=color, sw=4, double=False))


L.append(
    '<div class="g full" id="b2"><div class="sheet board-bg hide" id="b2S" style="height:930px">'
    '<div class="lbl hide" id="b2L" style="left:110px;top:60px">на місяць</div>'
    + sk.svg(1080, 1300, SC_POST, sid="b2P") +
    '<div class="ab" id="b2Beam" style="left:0;top:0;width:1080px;height:1300px">'
    + sk.svg(1080, 1300, BEAM, sid="b2B") + '</div>'
    '<div class="ab" id="b2PL" style="left:0;top:0;width:1080px;height:1300px">'
    + sk.svg(1080, 1300, pan(PX - 360, PY, "red"), sid="b2PLs") +
    '<div class="ab hide" id="b2CL" style="left:60px;top:680px;width:240px;text-align:center">'
    '<div class="hand" style="font-size:52px;color:#EA4335">витрати</div>'
    '<div class="price" style="position:relative;font-size:84px">≈ $70</div></div></div>'
    '<div class="ab" id="b2PR" style="left:0;top:0;width:1080px;height:1300px">'
    + sk.svg(1080, 1300, pan(PX + 360, PY, "green"), sid="b2PRs") +
    '<div class="ab hide" id="b2CR" style="left:780px;top:680px;width:240px;text-align:center">'
    '<div class="hand" style="font-size:52px;color:#34A853">заробляє</div>'
    '<div class="price" style="position:relative;font-size:84px">$60</div></div>'
    '<div class="ab hide" id="b2One" style="left:830px;top:490px;width:120px;height:130px">'
    + sk.svg(120, 130, avatar(60, 34, 26, stroke="blue", fill="blue"), sid="b2OneS") + '</div>'
    '<div class="hand hide" id="b2OneT" style="position:absolute;left:830px;top:330px;font-size:44px;color:#4285F4">+1 людина</div>'
    '</div>'
    '<div class="ab" style="left:0;top:130px;width:1080px;display:flex;justify-content:center">'
    '<span class="chip big cr hide" id="b2M">− мінус</span></div>'
    '<div class="ab" style="left:0;top:130px;width:1080px;display:flex;justify-content:center">'
    '<span class="chip big gr hide" id="b2Z">0 нуль</span></div>'
    '</div></div>')


@beat
def b_board2():
    sfx("whoosh-short", "@zahalom-0.1")
    sfx("pencil", "@zahalom+0.4", -2)
    sfx("pop", "@vytraty3")
    sfx("pop", "@s70b")
    sfx("pop", "@zarobliaie3")
    sfx("kaching", "@s60", -3)
    sfx("click", "@minusi2-0.1")
    sfx("pop", "@liudyna-0.2")
    sfx("ping", "@nul2-0.05")
    sfx("whoosh-short", "@tomu_cta-0.1")
    return js("""
  h.show("#b2", @zahalom-0.15);
  h.sheetIn("#b2S", @zahalom-0.15, 930);
  tl.set("#sc", {autoAlpha: 0}, @zahalom+0.6);
  h.write("#b2L", @zahalom+0.4, 0.4);
  h.draw("#b2P", @zahalom+0.3, 0.8);
  h.draw("#b2B", @zahalom+0.8, 0.4);
  h.draw("#b2PLs", @vytraty3-0.3, 0.5);
  h.draw("#b2PRs", @vytraty3-0.1, 0.5);
  h.pop("#b2CL", @vytraty3, {s: 0.5, r: -3});
  h.pop("#b2CR", @zarobliaie3-0.05, {s: 0.5, r: 3});
  /* costs are heavier: the left side goes down */
  tl.fromTo("#b2Beam", {rotation: 0, transformOrigin: "%dpx %dpx"}, {rotation: -7, transformOrigin: "%dpx %dpx", duration: 0.9, ease: SP, immediateRender: false}, @s60+0.3);
  tl.fromTo("#b2PL", {y: 0}, {y: 44, duration: 0.9, ease: SP, immediateRender: false}, @s60+0.3);
  tl.fromTo("#b2PR", {y: 0}, {y: -44, duration: 0.9, ease: SP, immediateRender: false}, @s60+0.3);
  h.pop("#b2M", @minusi2-0.15, {s: 0.4, r: -6});
  /* one more person pays: it levels */
  h.show("#b2One", @liudyna-0.3);
  tl.fromTo("#b2One", {y: -360, autoAlpha: 0}, {y: 0, autoAlpha: 1, duration: 0.5, ease: "power2.in", immediateRender: false}, @liudyna-0.3);
  h.draw("#b2OneS", @liudyna-0.3, 0.3);
  h.write("#b2OneT", @liudyna+0.15, 0.4);
  tl.to("#b2Beam", {rotation: 0, duration: 1.0, ease: SP}, @oplatyt);
  tl.to("#b2PL", {y: 0, duration: 1.0, ease: SP}, @oplatyt);
  tl.to("#b2PR", {y: 0, duration: 1.0, ease: SP}, @oplatyt);
  h.out("#b2M", @nul2-0.3, 0.2);
  h.pop("#b2Z", @nul2-0.1, {s: 0.4, r: 6});
  tl.to("#b2S", {y: -970, duration: 0.55, ease: "power3.in"}, @tomu_cta-0.05);
  tl.set("#b2", {autoAlpha: 0}, @tomu_cta+0.52);
  h.plateDown(@tomu_cta, 140, 0.65);
""" % (PX, PY, PX, PY))


# ================================================================ 10 CTA
L.append(
    '<div class="g" id="ct" style="top:0;height:700px">'
    '<div class="gcard" id="ctC" style="left:90px;top:60px;width:900px;height:580px">'
    '<div class="lbl" style="left:50px;top:40px">твоя відповідь</div>'
    '<div class="ab" style="left:50px;top:90px;display:flex;gap:18px">'
    '<span class="chip mid cg">+ плюс</span><span class="chip mid cr" id="ctM">− мінус</span><span class="chip mid gr">0 нуль</span></div>'
    + sk.svg(900, 580, sk.circle_around(384, 132, 128, 54, stroke="red", sw=6), sid="ctOK") +
    '<div class="pill hide" id="ctCm" style="left:50px;top:230px;width:800px;height:100px;padding:0 36px;box-shadow:var(--e1);border:2px solid #dadce0">'
    '<span class="gs" style="font-size:34px;color:#5f6368">Коментар:</span>'
    '<span class="wm" id="ctCmT" data-text="RUTA" style="font-size:48px"></span></div>'
    '<div class="bub me hide" id="ctDM" style="left:340px;top:360px;box-shadow:var(--e1)">Тримай посилання на RUTA</div>'
    '<div class="ab hide" id="ctPr" style="left:50px;top:470px"><span class="chip mid on">посилання в профілі</span></div>'
    '</div></div>')


@beat
def b_cta():
    sfx("pop", "@tomu_cta")
    sfx("pencil", "@vhadala", -3)
    sfx("pop", "@pyshy-0.1")
    sfx("key-press", "@slovo+0.1")
    sfx("notification", "@posylannia", -2)
    sfx("pop", "@shukai")
    return js("""
  h.show("#ct", @tomu_cta-0.05);
  h.pop("#ctC", @tomu_cta-0.05, {s: 0.7, r: 0, y: 0});
  h.draw("#ctOK", @vhadala, 0.35);
  h.pop("#ctCm", @pyshy-0.15, {s: 0.8, r: 0, y: 20});
  h.type("#ctCmT", @slovo+0.1, 9);
  h.pop("#ctDM", @posylannia-0.05, {s: 0.5, r: 3});
  h.pop("#ctPr", @shukai-0.1, {s: 0.5, r: -4});
""")


INVERT = []    # halfscreen keeps her and the white captions in the bottom half (STYLE.md §0c)
BLACKOUT = [
    (T["s70"] - 0.05, T["korystuvachiv"] + 0.6, ""),                      # «70+ користувачів»
    (T["zarobliaie2"] - 0.05, T["zarobliaie2"] + 0.5, ""),               # chip заробляє
    (T["vytraty"] - 0.05, T["vytraty"] + 0.55, ""),                      # chip витрати
    (T["pliuc"] - 0.05, T["nul"] + 0.3, ""),                              # плюс / мінус / нуль
    (T["ruta"] - 0.05, T["ruta"] + 0.5, ""),                              # RUTA
    (T["rilsy"] - 0.05, T["rilsy"] + 0.4, ""),                            # chip рілси
    (T["tredsy"] - 0.1, T["tredsy"] + 0.5, ""),                           # chip тредси
    (T["s100"] - 0.05, T["s100"] + 0.4, ""),                              # $100
    (T["supabase"] - 0.05, T["supabase"] + 0.4, ""),                      # Supabase
    (T["vercel"] - 0.05, T["vercel"] + 0.45, ""),                         # Vercel
    (T["s35"] - 0.05, T["s35"] + 0.6, ""), (T["s20"] - 0.05, T["s20"] + 0.4, ""),
    (T["s55"] - 0.05, T["s55"] + 0.6, ""),
    (T["s15"] - 0.05, T["s15"] + 0.8, ""),                                # $15–20
    (T["dolar"] - 0.05, T["dolar"] + 0.7, ""),                            # $1,50
    (T["bezkoshtovno"] - 0.05, T["bezkoshtovno"] + 0.6, ""),
    (T["s70b"] - 0.05, T["s70b"] + 0.5, ""), (T["s60"] - 0.05, T["s60"] + 0.5, ""),
    (T["minusi2"] - 0.05, T["minusi2"] + 0.35, ""), (T["nul2"] - 0.05, T["nul2"] + 0.3, ""),
    (T["slovo"] - 0.05, T["slovo"] + 0.45, ""),                           # слово «RUTA» typed
]


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
        title=u"Reel 57 — скільки заробляє RUTA",
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
    if "--caps" in sys.argv:
        print(" ".join(c["w"] for c in CAPS))


main()
