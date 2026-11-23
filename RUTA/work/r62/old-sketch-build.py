# -*- coding: utf-8 -*-
"""Reel 46 — «Які налаштування є в АІ-агентах SendPulse і які з них справді важливі?»

Google x Excalidraw look (STYLE.md §0b), skeleton copied from reel-45.

The one object: the SendPulse agent's SETTINGS CARD — four rows (Інструкції,
Модель, Завантаження файлів, Макс. токенів). Every beat opens one of its rows.

Layouts (STYLE.md §0c, her note «graphics never on my head»): every mockup is a
move-down sheet (her plate is pushed down under it), the two boards and the
Sonnet | Haiku comparison are halfscreen whiteboards; no full-frame takeover.

Chain:  NEAR the agent card: SendPulse pill, three chips (кваліфікує ->
спілкується -> продаж) joined by drawn arrows -> the chips clear and the card
becomes the settings list; «два»: green loops 1 and 2 round Інструкції and
Токени, the other two get struck through -> OVER board 1 wipes out of the
Інструкції row: title, «№1» looped, the field grows long («без ліміту»), the
hand fills it and chips drop in (скрипти, цільова аудиторія, контекст про
бізнес) -> closes onto the model card -> NEAR «Модель» dropdown: Haiku typed
in, «найдешевша», «по скрипту» arrow, economy chip -> Sonnet | Haiku columns,
Sonnet's bar grows, «×3–4», two equal reply bubbles and a drawn «=» -> NEAR
the files row: upload button scribbled out, a sketched file slides along an
arrow into «Інструкції», «без ліміту» -> «Макс. токенів» pill with a red «?»
-> OVER board 2 wipes out of it: «Токени»; the slider goes down, short bubble,
«дешевше?»; then the four Google dots = «думає»; 500: a short box filled all
yellow, the reply bubble crossed out; 2000: a long box, yellow + blue, tick,
a real reply bubble, «вартість майже та сама» -> closes onto the instruction
card -> NEAR «Пиши коротко.» typed three times, underlined; then a DM with a
huge reply bubble growing, scribbled -> CTA: two chips (немає менеджера /
не справляється), Direct notifications stack up, go grey «без відповіді»,
a hand-drawn «+» and the comment field types «+».

usage: python build.py   (then: python ../tools/sfx.py mix 46)
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

NN = "46"
CUT = json.load(io.open(os.path.join(ROOT, "work", "r" + NN, "cut.json"), encoding="utf-8"))
DUR = 115.550
FPS = 30
k = Kit(width=1080, height=1920, fps=FPS, duration=DUR)
k.cap_font = "assets/fonts/ProductSans-Bold.ttf"
k.css(sketch_css())
sk = Sketch(seed=46)

NO_PAINT = [tuple(x) for x in CUT["no_paint"]]

CAPS = k.load_captions(os.path.join(ROOT, "work", "r" + NN, "captions.json"))


# ---- caption fixes: whisper errors -> the script word / what she said ------
def fix(caps):
    def find(word, near):
        c = min((i for i, c in enumerate(caps) if c["w"] == word), key=lambda i: abs(caps[i]["s"] - near))
        assert abs(caps[c]["s"] - near) < 0.5, (word, near)
        return c
    edits = [
        ("пульс,", 2.21, u"SendPulse,"), ("Дирекції.", 4.21, u"дірект,"),
        ("налаштовань,", 7.68, u"налаштувань,"), ("важлива", 9.26, u"важливі"),
        ("на", 10.60, u"а на"), ("Просто", 11.80, u"просто"),
        ("це звичайно,", 13.64, u"це, звичайно,"),
        ("ліміту…", 15.90, u"ліміту,"), ("У", 16.53, u"по"), ("я не", 17.26, u"і"), ("маю.", 17.56, u"немає."),
        ("і челюбова", 20.61, u"і цільова"), ("обирати", 25.49, u"обирати,"),
        ("закономиш", 34.15, u"зекономиш."), ("я", 34.73, u"Я"),
        ("Сонеті", 35.90, u"Sonnet"), ("Хайку.", 36.80, u"Haiku."), ("дорожче", 39.69, u"дорожче,"),
        ("побачила", 43.41, u"побачила."), ("Завантаження", 44.68, u"завантаження"),
        ("Токені.", 57.10, u"Токени."), ("Здається", 58.14, u"здається"), ("пише", 61.92, u"пише,"),
        ("токінів", 66.12, u"токенів"), ("максимум.", 70.92, u"максимум,"),
        ("саме", 82.63, u"це"), ("ж не", 82.85, u"майже не"), ("впливає.", 83.01, u"впливає"),
        ("в інструкції,", 88.94, u"в інструкції."), ("Великі!", 94.80, u"великі,"),
        ("Тому", 99.43, u"Тому,"), ("Якщо", 99.66, u"якщо"), ("вдові", 99.94, u"в тебе"),
        ("Купи", 103.33, u"купа"), ("гугляться", 107.33, u"губляться"), ("відповіді", 108.15, u"відповіді,"),
        ("ставь", 109.21, u"став"),
        ("там,", 8.32, u"там"), ("інструкції.", 49.82, u"інструкції,"), ("контекст,", 22.17, u"контекст"),
        ("здогадається.", 92.66, u"здогадається,"), ("справляється.", 102.72, u"справляється,"), ("налаштувати.", 112.27, u"налаштувати,"),
    ]
    for w, near, new in edits:
        caps[find(w, near)]["w"] = new
    # merge caps[i+1] into caps[i]
    merges = [("5", 27.93, u"5.5,"), ("ваш", 83.61, u"вартість.")]
    for w, near, new in merges:
        i = find(w, near)
        caps[i]["w"] = new
        caps[i]["e"] = caps[i + 1]["e"]
        del caps[i + 1]
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
    "nalasht": S(u"Налаштовувала", 0.0), "sendpulse": S(u"SendPulse", 2.21), "kvalif": S(u"кваліфікує", 3.19),
    "spilk": S(u"спілкується", 4.64), "prodazhu": S(u"продажу", 6.42), "nalashtuvan": S(u"налаштувань", 7.68),
    "dva": S(u"два", 10.04), "inshe": S(u"інше", 11.14), "zabyty": S(u"забити", 12.11),
    "instr": S(u"Інструкція", 12.67), "naivazh": S(u"найважливіша", 14.46), "limitu": S(u"ліміту", 15.90),
    "nemaie": S(u"немає", 17.56), "zanosysh": S(u"заносиш", 18.66), "skrypty": S(u"скрипти", 20.05),
    "audytoriia": S(u"аудиторія", 21.07), "kontekst": S(u"контекст", 22.17), "biznes": S(u"бізнес", 22.77),
    "buty": S(u"бути", 24.07),
    "model": S(u"Модель", 24.50), "naideshevshu": S(u"найдешевшу", 26.37), "haiku": S(u"Haiku", 27.57),
    "chitko": S(u"чітко", 30.27), "skryptu": S(u"скрипту", 30.81), "riznytsi": S(u"різниці", 31.37),
    "hroshi": S(u"гроші", 33.81), "testuvala": S(u"тестувала", 35.06), "sonnet": S(u"Sonnet", 35.90),
    "haiku2": S(u"Haiku", 36.80), "try": S(u"три", 38.67), "dorozhche": S(u"дорожче", 39.69),
    "riznytsi2": S(u"різниці", 40.69), "vizualno": S(u"візуально", 41.19), "pobachyla": S(u"побачила", 43.41),
    "zavant": S(u"завантаження", 44.68), "propustyty": S(u"пропустити", 46.02), "faylom": S(u"файлом", 48.32),
    "instruktsii": S(u"інструкції", 49.82), "limitu2": S(u"ліміту", 51.50), "optym": S(u"оптимізовувати", 52.68),
    "ale": S(u"Але", 53.67), "vazhlyvo": S(u"важливо", 55.02), "dyvnym": S(u"дивним", 56.52),
    "tokeny": S(u"Токени", 57.10), "lohichnym": S(u"логічним", 58.42), "menshe": S(u"менше", 59.52),
    "korotshi": S(u"коротші", 60.92), "deshevshe": S(u"дешевше", 62.86), "ale2": S(u"Але", 64.13),
    "chastynu": S(u"частину", 65.54), "podumaty": S(u"подумати", 67.67), "p500": S(u"500", 69.87),
    "vytratyt": S(u"витратить", 72.27), "zmozhe": S(u"зможе", 74.11), "tekst": S(u"текст", 75.39),
    "p2000": S(u"2000", 77.08), "adekvatna": S(u"адекватна", 78.48), "podumaty2": S(u"подумати", 79.86),
    "vstyh": S(u"встиг", 80.14), "normalne": S(u"нормальне", 81.01), "vplyvaie": S(u"впливає", 83.01),
    "vartist": S(u"вартість", 83.61),
    "khochesh": S(u"хочеш", 84.78), "korotko": S(u"коротко", 86.10), "propysaty": S(u"прописати", 87.82),
    "dekilka": S(u"декілька", 89.85), "napysala": S(u"написала", 90.57), "sam": S(u"сам", 91.96),
    "zdohad": S(u"здогадається", 92.66), "velyki": S(u"великі", 94.80), "rozshyreni": S(u"розширені", 95.57),
    "posluhy": S(u"послуги", 97.75), "dali": S(u"далі", 98.97),
    "menedzhera": S(u"менеджера", 100.66), "sprav": S(u"справляється", 102.72), "zaiavok": S(u"заявок", 103.75),
    "dirTekti": S(u"діректі", 104.13), "bachysh": S(u"бачиш", 106.31), "hubliatsia": S(u"губляться", 107.33),
    "vidpovidi": S(u"відповіді", 108.15), "pliuS": S(u"плюс", 109.73), "personalno": S(u"персонально", 111.31),
    "dopomozhe": S(u"допоможе", 113.77), "pobach": S(u"Побачимося", 114.43),
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
.srow { position: absolute; left: 40px; width: 800px; height: 84px; display: flex; align-items: center;
        justify-content: space-between; border-bottom: 2px solid #e8eaed; font-family: "GSans", sans-serif;
        font-size: 40px; font-weight: 500; color: #202124; }
.srow i { font-style: normal; font-size: 30px; color: #5f6368; }
.ntf { position: absolute; left: 0; width: 880px; height: 84px; border-radius: 22px; background: #fff;
       box-shadow: var(--e1); display: flex; align-items: center; gap: 22px; padding: 0 26px;
       box-sizing: border-box; font-family: "GSans", sans-serif; font-size: 32px; color: #202124; }
.ntf .av { position: static; width: 56px; height: 56px; font-size: 26px; }
.ntf b { font-weight: 700; } .ntf span { color: #5f6368; flex: 1; }
.ntf em { font-style: normal; font-size: 24px; color: #0b57d0; font-weight: 700; }
.ty { font-family: "GSans", sans-serif; font-size: 40px; font-weight: 500; color: #202124; position: absolute;
      white-space: nowrap; }
""")

# ---------------------------------------------------------------- layouts (STYLE.md §0c)
# Mockups = move-down sheets (h 620-700, Material grey ground, the card inside);
# schemes (the two boards, the price comparison) = halfscreen whiteboard sheets
# (h 930, authored at full size inside 0..890). One sheet hands over to the next
# with swap(): the old one rolls up while the new one drops over it, and her
# plate goes straight to the new depth (no up-down bounce between them).
MOCK_H, HALF_H = 700, 930
SHEET_BG = "background:#f1f3f4"


def mock_open(gid, sid, h=MOCK_H):
    return ('<div class="g full" id="%s"><div class="sheet hide" id="%s" style="height:%dpx;%s">'
            % (gid, sid, h, SHEET_BG))


def half_open(gid, sid, h=HALF_H):
    return '<div class="g full" id="%s"><div class="sheet board-bg hide" id="%s" style="height:%dpx">' % (gid, sid, h)


# ---------------------------------------------------------------- 1+2 the agent card -> settings list
ROWS = [(u"Інструкції", u"текст"), (u"Модель", u"Haiku"), (u"Завантаження файлів", u"вимк."),
        (u"Макс. токенів", u"—")]
ROW_Y = [150, 250, 350, 450]
rows_html = "".join(
    '<div class="srow hide" id="sr%d" style="top:%dpx"><span>%s</span><i>%s</i></div>' % (i, y, a, b)
    for i, ((a, b), y) in enumerate(zip(ROWS, ROW_Y)))
L.append(
    mock_open("ag", "agS") +
    '<div class="gcard" id="agC" style="left:100px;top:110px;width:880px;height:560px">'
    '<div class="row" style="left:36px;top:30px;height:70px">'
    '<span id="spDot" style="display:inline-block;width:44px;height:44px;border-radius:50%;background:#4285F4"></span>'
    '<span class="gs" id="spW" style="font-size:42px;font-weight:700">SendPulse</span>'
    '<span class="lbl" style="position:static">AI-агент</span></div>'
    '<div style="position:absolute;left:0;right:0;top:120px;height:2px;background:#e8eaed"></div>'
    + sk.svg(880, 560, sk.ellipse(170, 335, 110, 110, stroke="blue", fill="blue"), sid="jag")
    + '<div class="gs hide" id="jagT" style="position:absolute;left:60px;top:310px;width:220px;text-align:center;font-size:42px;font-weight:700;color:#0b57d0">агент</div>'
    '<div class="ab hide" id="j1" style="left:440px;top:165px"><span class="chip on">кваліфікує</span></div>'
    '<div class="ab hide" id="j2" style="left:440px;top:300px"><span class="chip cy">спілкується</span></div>'
    '<div class="ab hide" id="j3" style="left:440px;top:435px"><span class="chip cg">продаж</span></div>'
    + sk.svg(880, 560, sk.arrow([(290, 290), (350, 230), (425, 205)], stroke="blue", sw=5, head=22), sid="ja0")
    + sk.svg(880, 560, sk.arrow([(295, 338), (360, 334), (425, 338)], stroke="blue", sw=5, head=22), sid="ja1")
    + sk.svg(880, 560, sk.arrow([(290, 385), (350, 445), (425, 470)], stroke="blue", sw=5, head=22), sid="ja2")
    + rows_html
    + sk.svg(880, 560, sk.circle_around(200, ROW_Y[0] + 42, 175, 46, stroke="green", sw=6), sid="lp1")
    + sk.svg(880, 560, sk.circle_around(200, ROW_Y[3] + 42, 175, 46, stroke="green", sw=6), sid="lp2")
    + '<div class="hand hide" id="n1" style="position:absolute;left:600px;top:%dpx;font-size:64px;color:#34A853">1</div>' % (ROW_Y[0] + 4)
    + '<div class="hand hide" id="n2" style="position:absolute;left:600px;top:%dpx;font-size:64px;color:#34A853">2</div>' % (ROW_Y[3] + 4)
    + sk.svg(880, 560, sk.line([(40, ROW_Y[1] + 44), (420, ROW_Y[1] + 40), (840, ROW_Y[1] + 46)], stroke="red", sw=6, double=False), sid="st1")
    + sk.svg(880, 560, sk.line([(40, ROW_Y[2] + 44), (460, ROW_Y[2] + 48), (840, ROW_Y[2] + 42)], stroke="red", sw=6, double=False), sid="st2")
    + '</div></div></div>')


@beat
def b_agent():
    sfx("whoosh-short", 0.05, -4)
    sfx("pencil", 0.9, -4)
    sfx("click-soft", "@sendpulse")
    sfx("pop", "@kvalif")
    sfx("pop", "@spilk")
    sfx("pop", "@prodazhu")
    return js("""
  h.show("#ag", 0.02);
  h.sheetIn("#agS", 0.02, %d);
  h.bump("#spW", @sendpulse);
  h.wiggle("#spDot", @sendpulse);
  h.draw("#jag", 0.9, 0.8);
  h.write("#jagT", 1.4, 0.4);
  h.draw("#ja0", @kvalif-0.35, 0.3);
  h.pop("#j1", @kvalif-0.05, {s: 0.5, r: -5});
  h.draw("#ja1", @spilk-0.35, 0.3);
  h.pop("#j2", @spilk, {s: 0.5, r: 4});
  h.draw("#ja2", @prodazhu-0.4, 0.3);
  h.pop("#j3", @prodazhu-0.05, {s: 0.5, r: -4});
  h.bump("#j3", @prodazhu+0.4);
""" % MOCK_H)


@beat
def b_settings():
    sfx("click-soft", "@nalashtuvan")
    sfx("pencil", "@dva-0.1", -3)
    sfx("pencil", "@inshe", -4)
    return js("""
  h.out("#j1", @nalashtuvan-0.55, 0.2);
  h.out("#j2", @nalashtuvan-0.5, 0.2);
  h.out("#j3", @nalashtuvan-0.45, 0.2);
  h.undraw("#ja0", @nalashtuvan-0.55, 0.2);
  h.undraw("#ja1", @nalashtuvan-0.55, 0.2);
  h.undraw("#ja2", @nalashtuvan-0.55, 0.2);
  h.undraw("#jag", @nalashtuvan-0.55, 0.25);
  h.out("#jagT", @nalashtuvan-0.55, 0.2);
  h.pop("#sr0", @nalashtuvan-0.1, {s: 0.95, r: 0, y: 16, d: 0.5});
  h.pop("#sr1", @nalashtuvan+0.05, {s: 0.95, r: 0, y: 16, d: 0.5});
  h.pop("#sr2", @nalashtuvan+0.2, {s: 0.95, r: 0, y: 16, d: 0.5});
  h.pop("#sr3", @nalashtuvan+0.35, {s: 0.95, r: 0, y: 16, d: 0.5});
  h.draw("#lp1", @dva-0.15, 0.4);
  h.write("#n1", @dva+0.1, 0.25);
  h.draw("#lp2", @dva+0.25, 0.4);
  h.write("#n2", @dva+0.5, 0.25);
  h.draw("#st1", @inshe, 0.35);
  tl.to("#sr1", {opacity: 0.35, duration: 0.3}, @inshe+0.1);
  h.draw("#st2", @inshe+0.45, 0.35);
  tl.to("#sr2", {opacity: 0.35, duration: 0.3}, @inshe+0.55);
  h.bump("#sr0", @instr-0.45);
""")


# ---------------------------------------------------------------- 3 HALFSCREEN: the instructions board
L.append(
    half_open("bd1", "bd1S") +
    '<div class="lbl hide" id="b1L" style="left:110px;top:56px">SendPulse · AI-агент</div>'
    '<div class="hand hide" id="b1T" style="left:108px;top:96px;position:absolute;font-size:84px">Інструкції</div>'
    + sk.svg(1080, 930, sk.underline(110, 208, 420, stroke="blue"), sid="b1U")
    + '<div class="hand hide" id="b1N" style="position:absolute;left:740px;top:96px;font-size:80px;color:#EA4335">№1</div>'
    + sk.svg(1080, 930, sk.circle_around(812, 144, 110, 66, stroke="red", sw=6), sid="b1NC")
    + '<div class="field hide" id="b1F" style="left:110px;top:300px;width:860px;height:270px"><span class="fl">Інструкції</span></div>'
    + sk.svg(1080, 930,
             sk.line([(150, 370), (420, 366), (700, 374), (920, 368)], stroke="#3c4043", sw=5, double=False) +
             sk.line([(150, 425), (360, 429), (620, 421), (880, 427)], stroke="#3c4043", sw=5, double=False) +
             sk.line([(150, 480), (330, 476), (560, 484), (760, 478)], stroke="#3c4043", sw=5, double=False) +
             sk.line([(150, 535), (300, 531), (480, 537), (700, 533)], stroke="#3c4043", sw=5, double=False),
             sid="b1S")
    + sk.svg(1080, 930, sk.arrow([(1012, 330), (1018, 590), (1012, 850)], stroke="blue", sw=5, both=True), sid="b1A")
    + '<div class="hand hide" id="b1LT" style="position:absolute;left:640px;top:226px;font-size:44px;color:#4285F4">майже без ліміту</div>'
    + '<div class="ab hide" id="b1c1" style="left:150px;top:610px"><span class="chip cy">скрипти</span></div>'
    + '<div class="ab hide" id="b1c2" style="left:420px;top:690px"><span class="chip on">цільова аудиторія</span></div>'
    + '<div class="ab hide" id="b1c3" style="left:200px;top:770px"><span class="chip cg">контекст про бізнес</span></div>'
    + '</div></div>')


@beat
def b_board1():
    sfx("whoosh-short", "@instr-0.15")
    sfx("pencil", "@instr+0.3", -3)
    sfx("pencil", "@naivazh", -3)
    sfx("click-soft", "@limitu-0.3")
    sfx("pencil", "@zanosysh", -4)
    sfx("pop", "@skrypty")
    sfx("pop", "@audytoriia")
    sfx("pop", "@kontekst+0.2")
    sfx("whoosh-short", "@buty-0.05")
    return js("""
  h.show("#bd1", @instr-0.15);
  swap("#agS", %(m)d, "#bd1S", @instr-0.15, %(f)d);
  tl.set("#ag", {autoAlpha: 0}, @instr+0.6);
  h.write("#b1L", @instr+0.2, 0.35);
  h.write("#b1T", @instr+0.35, 0.55);
  h.draw("#b1U", @instr+0.8, 0.35);
  h.write("#b1N", @naivazh-0.05, 0.3);
  h.draw("#b1NC", @naivazh+0.25, 0.45);
  h.pop("#b1F", @limitu-0.4, {s: 0.92, r: 0, y: 14});
  tl.fromTo("#b1F", {height: 270}, {height: 570, duration: 0.9, ease: "power3.inOut", immediateRender: false}, @limitu+0.1);
  h.draw("#b1A", @limitu+0.4, 0.5);
  h.write("#b1LT", @nemaie-0.1, 0.5);
  h.draw("#b1S", @zanosysh-0.2, 1.0);
  h.pop("#b1c1", @skrypty-0.05, {s: 0.4, r: -6, y: -60});
  h.pop("#b1c2", @audytoriia-0.25, {s: 0.4, r: 5, y: -60});
  h.pop("#b1c3", @kontekst+0.1, {s: 0.4, r: -4, y: -60});
  h.bump("#b1F", @buty-0.2);
""" % {"m": MOCK_H, "f": HALF_H})


# ---------------------------------------------------------------- 4 MOVE-DOWN: the model dropdown
L.append(
    mock_open("md", "mdS") +
    '<div class="gcard" id="mdC" style="left:100px;top:110px;width:880px;height:560px">'
    '<div class="field" id="mdF" style="left:40px;top:70px;width:800px;height:120px"><span class="fl">Модель</span>'
    '<span class="ty" id="mdV" data-text="Haiku" style="left:34px;top:34px;font-size:46px;font-weight:700"></span></div>'
    + sk.svg(880, 560, sk.line([(760, 120), (780, 142), (800, 120)], sw=5, double=False), sid="mdCar")
    + '<div class="ab hide" id="mdCh" style="left:40px;top:230px"><span class="chip cg">найдешевша</span></div>'
    + '<div class="hand hide" id="mdSc" style="position:absolute;left:400px;top:236px;font-size:50px">йде по скрипту</div>'
    + sk.svg(880, 560, sk.arrow([(410, 320), (600, 312), (820, 320)], stroke="blue", sw=5), sid="mdAr")
    + '<div class="ab hide" id="mdEc" style="left:40px;top:400px"><span class="chip cy">гроші зекономиш</span></div>'
    + sk.svg(880, 560, sk.spark(420, 430, 30, stroke="green", sw=6), sid="mdSp")
    + '</div></div></div>')

# ---------------------------------------------------------------- 4b HALFSCREEN: Sonnet | Haiku
L.append(
    half_open("cmp", "cmpS") +
    '<div class="gs hide" id="mbS" style="position:absolute;left:100px;top:70px;width:360px;text-align:center;font-size:64px;font-weight:700">Sonnet</div>'
    '<div class="gs hide" id="mbH" style="position:absolute;left:620px;top:70px;width:360px;text-align:center;font-size:64px;font-weight:700">Haiku</div>'
    + sk.svg(1080, 930, sk.line([(540, 70), (540, 580)], stroke="#bdc1c6", sw=4, double=False), sid="mbDiv")
    + sk.svg(1080, 930, sk.rect(190, 190, 180, 360, stroke="red", fill="red"), sid="mbBS")
    + sk.svg(1080, 930, sk.rect(710, 470, 180, 80, stroke="green", fill="green"), sid="mbBH")
    + '<div class="hand hide" id="mbX" style="position:absolute;left:390px;top:200px;font-size:76px;color:#EA4335">×3–4</div>'
    + '<div class="lbl hide" id="mbP" style="left:100px;top:578px;width:880px;text-align:center">ціна</div>'
    + '<div class="bub me hide" id="mbR1" style="left:100px;top:650px;width:380px;height:150px;box-sizing:border-box;max-width:none"></div>'
    + '<div class="bub me hide" id="mbR2" style="left:600px;top:650px;width:380px;height:150px;box-sizing:border-box;max-width:none"></div>'
    + sk.svg(1080, 930,
             sk.line([(140, 705), (290, 701), (440, 707)], stroke="#041e49", sw=5, double=False) +
             sk.line([(140, 750), (260, 754), (370, 748)], stroke="#041e49", sw=5, double=False) +
             sk.line([(640, 705), (790, 701), (940, 707)], stroke="#041e49", sw=5, double=False) +
             sk.line([(640, 750), (760, 754), (870, 748)], stroke="#041e49", sw=5, double=False), sid="mbRL")
    + sk.svg(1080, 930, sk.line([(510, 708), (570, 706)], stroke="green", sw=10, double=False) +
             sk.line([(510, 746), (570, 744)], stroke="green", sw=10, double=False), sid="mbEq")
    + '</div></div>')


@beat
def b_model():
    sfx("whoosh-short", "@buty-0.05", -4)
    sfx("click-soft", "@naideshevshu")
    sfx("key-press", "@haiku")
    sfx("pencil", "@chitko", -3)
    sfx("kaching", "@hroshi")
    sfx("whoosh-short", "@testuvala-0.2")
    sfx("pop", "@sonnet")
    sfx("pop", "@haiku2")
    sfx("pencil", "@try-0.2", -3)
    sfx("pop", "@riznytsi2")
    sfx("pencil", "@vizualno+0.2", -4)
    return js("""
  h.show("#md", @buty-0.05);
  swap("#bd1S", %(f)d, "#mdS", @buty-0.05, %(m)d);
  tl.set("#bd1", {autoAlpha: 0}, @buty+0.6);
  h.draw("#mdCar", @model+0.3, 0.3);
  h.pop("#mdCh", @naideshevshu, {s: 0.5, r: -4});
  h.type("#mdV", @haiku-0.05, 14);
  h.bump("#mdF", @haiku+0.35);
  h.write("#mdSc", @chitko-0.1, 0.55);
  h.draw("#mdAr", @skryptu, 0.5);
  h.pop("#mdEc", @hroshi-0.15, {s: 0.5, r: 4});
  h.draw("#mdSp", @hroshi+0.2, 0.3);
  /* the test: a scheme -> halfscreen */
  h.show("#cmp", @testuvala-0.2);
  swap("#mdS", %(m)d, "#cmpS", @testuvala-0.2, %(f)d);
  tl.set("#md", {autoAlpha: 0}, @testuvala+0.5);
  h.pop("#mbS", @sonnet-0.05, {s: 0.6, r: -3});
  h.draw("#mbDiv", @sonnet+0.2, 0.3);
  h.pop("#mbH", @haiku2-0.05, {s: 0.6, r: 3});
  h.write("#mbP", @haiku2+0.4, 0.3);
  h.draw("#mbBH", @haiku2+0.4, 0.5);
  h.draw("#mbBS", @try-0.2, 0.9);
  h.write("#mbX", @try+0.1, 0.4);
  h.wiggle("#mbX", @dorozhche);
  h.pop("#mbR1", @riznytsi2, {s: 0.6, r: -2});
  h.pop("#mbR2", @riznytsi2+0.15, {s: 0.6, r: 2});
  h.draw("#mbRL", @riznytsi2+0.3, 0.7);
  h.draw("#mbEq", @vizualno+0.2, 0.35);
  h.bump("#mbR1", @pobachyla);
  h.bump("#mbR2", @pobachyla);
""" % {"m": MOCK_H, "f": HALF_H})


# ---------------------------------------------------------------- 5 MOVE-DOWN: file upload
L.append(
    mock_open("fl", "flS") +
    '<div class="gcard" id="flC" style="left:100px;top:110px;width:880px;height:560px">'
    '<div class="gs" style="position:absolute;left:40px;top:44px;font-size:42px;font-weight:700">Завантаження файлів</div>'
    '<div class="ab" id="flB" style="left:40px;top:120px;width:360px;height:84px;border-radius:42px;border:2px solid #747775;'
    'display:flex;align-items:center;justify-content:center;font-family:GSans,sans-serif;font-size:32px;color:#0b57d0;font-weight:500">'
    'Завантажити файл</div>'
    + sk.svg(880, 560, sk.scribble(30, 125, 380, 70, sw=7), sid="flX")
    + '<div id="flDoc" class="ab hide" style="left:50px;top:270px;width:170px;height:220px">'
    + sk.svg(170, 220, sk.rect(10, 10, 150, 200, stroke="ink", sw=4.5, round_=False) +
             sk.line([(35, 70), (135, 66)], sw=4, double=False) + sk.line([(35, 105), (125, 108)], sw=4, double=False) +
             sk.line([(35, 140), (110, 137)], sw=4, double=False), sid="flDS")
    + '<div class="hand" style="position:absolute;left:0;width:170px;top:160px;text-align:center;font-size:36px">файл</div></div>'
    + sk.svg(880, 560, sk.arrow([(240, 380), (340, 350), (460, 380)], stroke="blue", sw=5), sid="flAr")
    + '<div class="field hide" id="flF" style="left:480px;top:270px;width:360px;height:220px"><span class="fl">Інструкції</span></div>'
    + sk.svg(880, 560,
             sk.line([(510, 330), (640, 326), (800, 332)], stroke="#3c4043", sw=5, double=False) +
             sk.line([(510, 380), (620, 384), (760, 378)], stroke="#3c4043", sw=5, double=False) +
             sk.line([(510, 430), (600, 426), (720, 432)], stroke="#3c4043", sw=5, double=False), sid="flFS")
    + '<div class="hand hide" id="flL" style="position:absolute;left:520px;top:496px;font-size:42px;color:#4285F4">без ліміту</div>'
    + '</div></div></div>')


@beat
def b_files():
    sfx("whoosh-short", "@pobachyla+0.4", -4)
    sfx("pencil", "@propustyty", -2)
    sfx("pop", "@faylom-0.2")
    sfx("whoosh-short", "@instruktsii-0.3", -3)
    sfx("pencil", "@limitu2-0.2", -4)
    return js("""
  h.show("#fl", @pobachyla+0.4);
  swap("#cmpS", %(f)d, "#flS", @pobachyla+0.4, %(m)d);
  tl.set("#cmp", {autoAlpha: 0}, @pobachyla+1.0);
  h.draw("#flX", @propustyty, 0.45);
  tl.to("#flB", {opacity: 0.4, duration: 0.3}, @propustyty+0.3);
  h.pop("#flDoc", @faylom-0.2, {s: 0.5, r: -8});
  h.draw("#flDS", @faylom-0.2, 0.5);
  h.pop("#flF", @faylom+0.3, {s: 0.8, r: 0, y: 10});
  h.draw("#flAr", @instruktsii-0.5, 0.35);
  tl.to("#flDoc", {x: 470, scale: 0.35, autoAlpha: 0, duration: 0.55, ease: "power3.in"}, @instruktsii-0.1);
  h.draw("#flFS", @instruktsii+0.35, 0.6);
  h.bump("#flF", @instruktsii+0.5);
  h.write("#flL", @limitu2-0.2, 0.45);
""" % {"m": MOCK_H, "f": HALF_H})


# ---------------------------------------------------------------- 6 MOVE-DOWN: the tokens setting (zoomed-in clip)
TK_H = 640
L.append(
    mock_open("tk", "tkS", TK_H) +
    '<div class="pill hide" id="tkP" style="left:190px;top:250px;width:700px;height:130px;padding:0 44px;box-sizing:border-box;'
    'justify-content:space-between;font-size:48px;font-weight:700"><span>Макс. токенів</span>'
    '<span class="field" style="position:relative;width:170px;height:76px;display:inline-block"></span></div>'
    '<div class="hand hide" id="tkQ" style="position:absolute;left:740px;top:220px;font-size:120px;color:#EA4335">?</div>'
    '</div></div>')


@beat
def b_tokpill():
    sfx("pop", "@ale-0.05")
    sfx("pencil", "@dyvnym", -3)
    return js("""
  h.show("#tk", @optym+0.6);
  swap("#flS", %(m)d, "#tkS", @optym+0.6, %(t)d);
  tl.set("#fl", {autoAlpha: 0}, @optym+1.2);
  h.pop("#tkP", @ale-0.05, {s: 0.5, r: -3});
  h.write("#tkQ", @dyvnym, 0.35);
  h.wiggle("#tkQ", @dyvnym+0.4);
""" % {"m": MOCK_H, "t": TK_H})


# ---------------------------------------------------------------- 7 HALFSCREEN: the tokens board
L.append(
    half_open("bd2", "bd2S") +
    '<div class="lbl hide" id="b2L" style="left:110px;top:56px">SendPulse · AI-агент</div>'
    '<div class="hand hide" id="b2T" style="left:108px;top:96px;position:absolute;font-size:84px">Токени</div>'
    + sk.svg(1080, 930, sk.underline(110, 208, 300, stroke="red", twice=True), sid="b2U")
    # A: the "logical" idea
    + '<div id="b2A">'
    + '<div class="hand hide" id="b2lo" style="position:absolute;left:640px;top:110px;font-size:56px;color:#5f6368">логічно?</div>'
    + '<div class="lbl hide" id="b2sl" style="left:110px;top:300px">Макс. токенів</div>'
    + '<div class="ab hide" id="b2tr" style="left:110px;top:380px;width:860px;height:12px;border-radius:6px;background:#d3e3fd">'
      '<div id="b2tf" style="height:100%;width:100%;border-radius:6px;background:#0b57d0;transform-origin:0 50%"></div>'
      '<div id="b2th" style="position:absolute;left:0;top:-22px;width:56px;height:56px;border-radius:50%;background:#0b57d0"></div></div>'
    + '<div class="bub me hide" id="b2sb" style="left:110px;top:480px">Ок</div>'
    + '<div class="ab hide" id="b2ch" style="left:330px;top:490px"><span class="chip cy">дешевше?</span></div>'
    + '</div>'
    # B: think + 500
    + '<div class="dots hide" id="b2D" style="left:110px;top:290px"><i></i><i></i><i></i><i></i></div>'
    + '<div class="hand hide" id="b2Dt" style="position:absolute;left:290px;top:272px;font-size:54px;color:#d39e00">думає</div>'
    + '<div class="hand hide" id="b2Rt" style="position:absolute;left:600px;top:272px;font-size:54px;color:#4285F4">відповідь</div>'
    + '<div class="num hide" id="b2n5" style="position:absolute;left:110px;top:380px;font-size:84px">500</div>'
    + sk.svg(1080, 930, sk.rect(340, 385, 260, 90, stroke="ink"), sid="b2r5")
    + sk.svg(1080, 930, sk._hachure([(348, 393), (592, 393), (592, 467), (348, 467)], "#FBBC04", gap=13), sid="b2h5")
    + '<div class="bub me hide" id="b2e5" style="left:650px;top:385px;width:320px;height:90px;box-sizing:border-box"></div>'
    + sk.svg(1080, 930, sk.cross(770, 390, 80, sw=10), sid="b2x5")
    # C: 2000
    + '<div class="num hide" id="b2n2" style="position:absolute;left:110px;top:540px;font-size:84px">2000</div>'
    + sk.svg(1080, 930, sk.rect(340, 545, 630, 90, stroke="ink"), sid="b2r2")
    + sk.svg(1080, 930, sk._hachure([(348, 553), (560, 553), (560, 627), (348, 627)], "#FBBC04", gap=13), sid="b2h2y")
    + sk.svg(1080, 930, sk._hachure([(568, 553), (962, 553), (962, 627), (568, 627)], "#4285F4", gap=13), sid="b2h2b")
    + sk.svg(1080, 930, sk.check(150, 650, 80, sw=10), sid="b2ok")
    + '<div class="bub me hide" id="b2rb" style="left:340px;top:665px;width:630px;height:110px;box-sizing:border-box;max-width:none"></div>'
    + sk.svg(1080, 930,
             sk.line([(380, 705), (560, 701), (760, 707), (930, 703)], stroke="#041e49", sw=5, double=False) +
             sk.line([(380, 741), (520, 745), (680, 739)], stroke="#041e49", sw=5, double=False), sid="b2rl")
    + '<div class="hand hide" id="b2v" style="position:absolute;left:340px;top:800px;font-size:50px;color:#34A853">вартість ≈ та сама</div>'
    + '</div></div>')


@beat
def b_board2():
    sfx("whoosh-short", "@tokeny-0.1")
    sfx("pencil", "@tokeny+0.25", -3)
    sfx("click", "@menshe")
    sfx("ping", "@korotshi")
    sfx("pop", "@deshevshe")
    sfx("pop", "@chastynu-0.2")
    sfx("pop", "@p500")
    sfx("pencil", "@vytratyt", -3)
    sfx("click", "@zmozhe+0.1")
    sfx("pop", "@p2000")
    sfx("pencil", "@podumaty2-0.3", -3)
    sfx("ping", "@normalne")
    sfx("pencil", "@vplyvaie-0.2", -4)
    sfx("whoosh-short", "@vartist+0.4")
    return js("""
  h.show("#bd2", @tokeny-0.1);
  swap("#tkS", %(t)d, "#bd2S", @tokeny-0.1, %(f)d);
  tl.set("#tk", {autoAlpha: 0}, @tokeny+0.6);
  h.write("#b2L", @tokeny+0.2, 0.35);
  h.write("#b2T", @tokeny+0.3, 0.45);
  h.draw("#b2U", @tokeny+0.7, 0.4);
  h.write("#b2lo", @lohichnym, 0.45);
  h.write("#b2sl", @lohichnym+0.3, 0.3);
  h.pop("#b2tr", @lohichnym+0.4, {s: 0.95, r: 0, y: 10});
  tl.fromTo("#b2th", {x: 800}, {x: 170, duration: 0.8, ease: "power3.inOut", immediateRender: false}, @menshe-0.1);
  tl.fromTo("#b2tf", {scaleX: 0.95}, {scaleX: 0.22, duration: 0.8, ease: "power3.inOut", immediateRender: false}, @menshe-0.1);
  h.pop("#b2sb", @korotshi, {s: 0.5, r: 0});
  h.pop("#b2ch", @deshevshe-0.05, {s: 0.5, r: 4});
  h.wiggle("#b2lo", @deshevshe+0.4);
  /* B: but part of it is for thinking */
  h.fadeOut("#b2A", @ale2, 0.3);
  h.pop("#b2D", @chastynu-0.2, {s: 0.5, r: 0, y: 0});
  h.write("#b2Dt", @chastynu+0.1, 0.4);
  h.think("#b2D", @chastynu+0.2, 3.0);
  h.write("#b2Rt", @podumaty+0.3, 0.45);
  h.pop("#b2n5", @p500-0.05, {s: 0.5, r: -3});
  h.draw("#b2r5", @p500+0.2, 0.5);
  h.draw("#b2h5", @vytratyt-0.1, 0.9);
  h.think("#b2D", @vytratyt, 1.8);
  h.pop("#b2e5", @zmozhe-0.2, {s: 0.6, r: 2});
  h.draw("#b2x5", @zmozhe+0.1, 0.35);
  h.wiggle("#b2e5", @tekst);
  /* C: 2000 fits both */
  h.pop("#b2n2", @p2000-0.05, {s: 0.5, r: 3});
  h.draw("#b2r2", @p2000+0.25, 0.6);
  h.draw("#b2h2y", @podumaty2-0.3, 0.6);
  h.draw("#b2ok", @vstyh, 0.3);
  h.draw("#b2h2b", @vstyh+0.25, 0.7);
  h.pop("#b2rb", @normalne-0.1, {s: 0.6, r: -2});
  h.draw("#b2rl", @normalne+0.15, 0.5);
  h.write("#b2v", @vplyvaie-0.3, 0.6);
""" % {"t": TK_H, "f": HALF_H})


# ---------------------------------------------------------------- 8 MOVE-DOWN: write it short, in the instruction
L.append(
    mock_open("ins", "inS") +
    '<div class="gcard" id="inC" style="left:100px;top:110px;width:880px;height:560px">'
    '<div class="field" id="inF" style="left:40px;top:60px;width:800px;height:440px"><span class="fl">Інструкції</span>'
    '<span class="ty" id="in1" data-text="Пиши коротко." style="left:34px;top:50px"></span>'
    '<span class="ty" id="in2" data-text="Пиши коротко!" style="left:34px;top:150px"></span>'
    '<span class="ty" id="in3" data-text="ПИШИ КОРОТКО." style="left:34px;top:250px;font-weight:700"></span></div>'
    + sk.svg(880, 560, sk.underline(76, 380, 340, stroke="red", twice=True), sid="inU")
    + '<div class="dots hide" id="inD" style="left:560px;top:420px"><i></i><i></i><i></i><i></i></div>'
    + '</div>'
    '<div class="gcard hide" id="lgC" style="left:100px;top:110px;width:880px;height:560px;overflow:hidden">'
    '<div class="av" style="left:36px;top:26px;background:#34A853">К</div>'
    '<div class="gs" style="position:absolute;left:122px;top:30px;font-size:34px;font-weight:700">Клієнтка</div>'
    '<div class="gs" style="position:absolute;left:122px;top:72px;font-size:24px;color:#5f6368">Direct</div>'
    '<div style="position:absolute;left:0;right:0;top:116px;height:2px;background:#e8eaed"></div>'
    '<div class="bub me" id="lgB" style="right:36px;top:140px;width:600px;height:390px;box-sizing:border-box;max-width:none"></div>'
    + sk.svg(880, 560, "".join(
        sk.line([(280, 180 + 44 * i), (480, 176 + 44 * i), (800 - (i % 3) * 40, 182 + 44 * i)],
                stroke="#041e49", sw=5, double=False) for i in range(8)), sid="lgL")
    + sk.svg(880, 560, sk.scribble(250, 190, 570, 300, sw=7), sid="lgX")
    + '<div class="hand hide" id="lgT" style="position:absolute;left:40px;top:400px;width:200px;font-size:40px;color:#EA4335">про всі послуги…</div>'
    + '</div></div></div>')


@beat
def b_short():
    sfx("typing", "@propysaty-0.2", -4)
    sfx("typing", "@dekilka", -4)
    sfx("pencil", "@napysala", -3)
    sfx("whoosh-short", "@velyki-0.3")
    sfx("pencil", "@posluhy", -3)
    sfx("whoosh-short", "@dali+0.35", -4)
    return js("""
  h.show("#ins", @vartist+0.4);
  swap("#bd2S", %(f)d, "#inS", @vartist+0.4, %(m)d);
  tl.set("#bd2", {autoAlpha: 0}, @vartist+1.0);
  h.type("#in1", @propysaty-0.2, 16);
  h.type("#in2", @dekilka-0.1, 18);
  h.type("#in3", @napysala-0.3, 18);
  h.draw("#inU", @napysala+0.4, 0.5);
  h.pop("#inD", @sam, {s: 0.5, r: 0, y: 0});
  h.think("#inD", @sam+0.1, 1.2);
  h.out("#inC", @velyki-0.3, 0.25);
  h.pop("#lgC", @velyki-0.2, {s: 0.7, r: 2});
  tl.fromTo("#lgB", {clipPath: "inset(0%% 0%% 88%% 0%%)"}, {clipPath: "inset(0%% 0%% 0%% 0%%)", duration: 1.4, ease: "power1.inOut", immediateRender: true}, @velyki);
  h.draw("#lgL", @velyki, 1.6);
  h.write("#lgT", @posluhy-0.2, 0.45);
  h.draw("#lgX", @dali-0.3, 0.45);
  h.sheetOut("#inS", @dali+0.35, %(m)d);
  tl.set("#ins", {autoAlpha: 0}, @dali+1.0);
""" % {"m": MOCK_H, "f": HALF_H})


# ---------------------------------------------------------------- 9 MOVE-DOWN: CTA
NT = [(u"М", "#4285F4", u"Марія"), (u"О", "#EA4335", u"Олена"), (u"А", "#FBBC04", u"Андрій"), (u"І", "#34A853", u"Ірина")]
L.append(
    mock_open("cta", "ctS") +
    '<div class="ab" style="left:100px;top:90px;width:880px;display:flex;flex-wrap:wrap;gap:20px">'
    '<span class="chip cr hide" id="c1">немає менеджера</span>'
    '<span class="chip cy hide" id="c2">менеджер не справляється</span></div>'
    '<div class="ab" id="ntW" style="left:100px;top:270px;width:880px;height:390px">'
    + "".join('<div class="ntf hide" id="nt%d" style="top:%dpx"><div class="av" style="background:%s">%s</div>'
              '<b>%s</b><span>Нове повідомлення</span><em>DIRECT</em></div>' % (i, i * 96, c, a, n)
              for i, (a, c, n) in enumerate(NT))
    + '</div>'
    '<div class="hand hide" id="ntT" style="position:absolute;left:600px;top:560px;font-size:54px;color:#EA4335">без відповіді</div>'
    + sk.svg(1080, 700, sk.ellipse(540, 270, 105, 100, stroke="blue", sw=7) +
             sk.line([(540, 215), (540, 325)], stroke="blue", sw=11, double=False) +
             sk.line([(485, 270), (595, 270)], stroke="blue", sw=11, double=False),
             sid="plus")
    + '<div class="pill hide" id="cmt" style="left:170px;top:440px;width:740px;height:100px;padding:0 36px;font-size:36px">'
    '<span style="color:#5f6368">Коментар:</span><span id="cmtT" data-text="+" style="font-weight:700;font-size:52px"></span></div>'
    '</div></div>')


@beat
def b_cta():
    sfx("whoosh-short", "@menedzhera-0.4", -4)
    sfx("pop", "@menedzhera")
    sfx("pop", "@sprav")
    sfx("notification", "@zaiavok-0.1")
    sfx("ping", "@zaiavok+0.45", -3)
    sfx("pencil", "@hubliatsia+0.3", -3)
    sfx("pencil", "@pliuS-0.3", -2)
    sfx("key-press", "@pliuS+0.6")
    return js("""
  h.show("#cta", @menedzhera-0.4);
  h.sheetIn("#ctS", @menedzhera-0.4, %(m)d);
  h.pop("#c1", @menedzhera-0.1, {s: 0.5, r: -4});
  h.pop("#c2", @sprav-0.2, {s: 0.5, r: 4});
  h.pop("#nt0", @zaiavok-0.15, {s: 0.8, r: 0, y: -30, d: 0.5});
  h.pop("#nt1", @zaiavok+0.15, {s: 0.8, r: 0, y: -30, d: 0.5});
  h.pop("#nt2", @zaiavok+0.45, {s: 0.8, r: 0, y: -30, d: 0.5});
  h.pop("#nt3", @zaiavok+0.75, {s: 0.8, r: 0, y: -30, d: 0.5});
  tl.to("#ntW", {opacity: 0.45, filter: "grayscale(1)", duration: 0.6}, @hubliatsia);
  tl.to("#ntW", {y: 40, duration: 1.2, ease: "power2.in"}, @hubliatsia);
  h.write("#ntT", @hubliatsia+0.3, 0.5);
  h.fadeOut("#ntW", @pliuS-0.65, 0.25);
  h.fadeOut("#ntT", @pliuS-0.65, 0.25);
  h.out("#c1", @pliuS-0.65, 0.25);
  h.out("#c2", @pliuS-0.65, 0.25);
  h.draw("#plus", @pliuS-0.35, 0.7);
  h.pop("#cmt", @pliuS+0.2, {s: 0.8, r: 0, y: 20});
  h.type("#cmtT", @pliuS+0.6, 6);
  h.bump("#plus", @personalno);
""" % {"m": MOCK_H})


INVERT = []    # move-down / halfscreen keep her and the white captions in the bottom half


def main():
    gj = []
    for fn in BEATS:
        gj.append("  /* %s */" % fn.__name__)
        gj.append(fn().rstrip())
    for a, b in NO_PAINT:
        for c in SFX:
            assert not (a <= c["t"] < b), ("sfx in no_paint", c)
    head = [SKETCH_JS, "  var h = sketchHelpers(tl);",
            # one sheet hands over to the next: the old rolls up, the new drops
            # over it, her plate goes straight to the new depth
            "  function swap(o, oh, n, t, nh) {",
            '    tl.to(o, {y: -oh - 40, duration: 0.5, ease: "power3.in"}, t + 0.15);',
            "    tl.set(o, {autoAlpha: 0}, t + 0.67);",
            "    h.sheetIn(n, t, nh);",
            "  }",
            '  gsap.set("#vid", {transformOrigin: "540px 900px"});',
            '  tl.fromTo("#vid", {scale: 1}, {scale: 1.045, duration: %.3f, ease: "none"}, 0);' % DUR]
    doc = k.document(
        title=u"Reel 46 — налаштування агента SendPulse",
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
    print(" ".join(c["w"] for c in CAPS))


main()
