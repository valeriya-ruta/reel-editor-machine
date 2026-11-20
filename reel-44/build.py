# -*- coding: utf-8 -*-
"""Reel 44 — «Скільки насправді коштує монтаж з Клодом на місяць?». Posts 2026-11-21.

Google x Excalidraw look (STYLE.md §0b), skeleton copied from reel-45/build.py.
Cut from her raw take by tools/cut.py + work/r44/cut-fix.json (first CTA take,
two whisper-hallucinated silences, a mumbled aside and an unclear tail dropped;
no closeups: no_paint is empty). See PLAN.md for the chain.

usage: python build.py   (then: python ../tools/sfx.py mix 44)
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

NN = "44"
CUT = json.load(io.open(os.path.join(ROOT, "work", "r" + NN, "cut.json"), encoding="utf-8"))
DUR = 87.550           # (2627 plate frames - 0.5) / 30
FPS = 30
k = Kit(width=1080, height=1920, fps=FPS, duration=DUR)
k.cap_font = "assets/fonts/ProductSans-Bold.ttf"
k.css(sketch_css())
sk = Sketch(seed=44)

NO_PAINT = [tuple(x) for x in CUT["no_paint"]]   # empty on this cut

CAPS = k.load_captions(os.path.join(ROOT, "work", "r" + NN, "captions.json"))


# ---- caption fixes: whisper errors -> the script word / what she said ------
def fix(caps):
    """by index into captions.json, each asserting the token it replaces.
    ('w', i, old, new) replaces; ('drop', i, old) folds caps[i] into caps[i-1]."""
    edits = [
        (1, u"досправлі", u"насправді"),
        (8, u"якщо", u"Якщо"), (9, u"часу,", u"чесно,"), (10, u"то переховати", u"то порахувати"),
        (17, u"юзич", u"юсадж"),
        (40, u"дідати", u"витрачати"), (41, u"абсолютну", u"абсолютно"), (44, u"стокенів.", u"токенів."),
        (60, u"в 5", u"пʼять"), (61, u"RealSafe.", u"рілсів."), (62, u"якщо", u"Якщо"),
        (79, u"дві", u"дві-три"), (86, u"більше.", u"більше,"), (88, u"п'ять.", u"пʼять."),
        (101, u"тоді", u"Тоді"), (102, u"сьогодні!", u"десь"), (103, u"Туреріал", u"три"),
        (104, u"СИЗ", u"рілси"), (106, u"5", u"пʼятигодинний"),
        (122, u"Коли", u"коли"), (128, u"клієнкам,", u"клієнткам,"), (134, u"токенів,", u"токенів."),
        (148, u"І", u"і"), (149, u"може", u"можна"),
        (166, u"євро,", u"євро."), (167, u"я", u"Я"), (183, u"витрачалось", u"витрачалось."),
        (188, u"перевзакуєш", u"про таку"),
        (205, u"Тупо", u"то пиши"), (206, u"шиттес", u"ТЕСТ"), (208, u"коментарях", u"коментарях."),
        (213, u"поспекомись.", u"поспілкуємось."), (214, u"ти", u"Ти"),
        (235, u"тест", u"ТЕСТ"), (239, u"в Директі!", u"в директі!"),
    ]
    for i, old, new in edits:
        assert caps[i]["w"] == old, (i, caps[i]["w"], old)
        caps[i]["w"] = new
    drops = [(7, u"І"), (76, u"б"), (80, u"три"), (107, u"годинний")]
    for i, old in sorted(drops, reverse=True):
        assert caps[i]["w"] == old, (i, caps[i]["w"], old)
        if i == 7:                       # leading «І»: the next word takes its start
            caps[i + 1]["s"] = caps[i]["s"]
        else:
            caps[i - 1]["e"] = caps[i]["e"]
        del caps[i]
    return caps


CAPS = fix(CAPS)


def punct(caps):
    """after the merges: (word, near, new) by time"""
    for w, near, new in [(u"навіть", 13.07, u"Навіть"), (u"хвилини", 31.13, u"хвилини,"),
                         (u"нуля.", 55.67, u"нуля,"), (u"тобі", 76.36, u"тобі,")]:
        i = min((i for i, c in enumerate(caps) if c["w"] == w), key=lambda i: abs(caps[i]["s"] - near))
        assert abs(caps[i]["s"] - near) < 0.5, (w, near)
        caps[i]["w"] = new
    return caps


CAPS = punct(CAPS)
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
    "skilky": S(u"Скільки", 0.0), "montazh": S(u"монтаж", 1.89), "misiats": S(u"місяць", 2.93),
    "chesno": S(u"чесно", 3.73), "porakhuvaty": S(u"порахувати", 4.33), "nemozhlyvo": S(u"неможливо", 5.79),
    "iusadzh": S(u"юсадж", 6.77), "nepered": S(u"непередбачувана", 7.87), "napered": S(u"наперед", 9.14),
    "skilky2": S(u"скільки", 10.17), "zadachu": S(u"задачу", 12.52), "dvi": S(u"дві", 13.48),
    "odnakovi": S(u"однакові", 13.90), "riznykh": S(u"різних", 14.94), "liudei": S(u"людей", 15.32),
    "riznu": S(u"різну", 17.52), "tokeniv": S(u"токенів", 18.36), "oriientyr": S(u"орієнтир", 19.21),
    "na": S(u"На", 20.00), "dvadtsiat": S(u"20", 21.07), "dolariv": S(u"доларів", 21.43),
    "odyn": S(u"один", 22.09), "limit": S(u"ліміт", 23.05), "harant": S(u"гарантовано", 24.20),
    "piat": S(u"пʼять", 25.30), "ekspertni": S(u"експертні", 27.06), "kameru": S(u"камеру", 28.86),
    "sufliera": S(u"суфлера", 29.34), "dvitry": S(u"дві-три", 30.79), "khvylyny": S(u"хвилини", 31.13),
    "bilshe": S(u"більше", 32.78), "yakshcho2": S(u"Якщо", 33.80), "dovshe": S(u"довше", 34.53),
    "piatshist": S(u"5-6", 35.47), "vstavok": S(u"вставок", 36.61), "pomylok": S(u"помилок", 37.69),
    "try": S(u"три", 38.98), "rilsy": S(u"рілси", 39.70), "liimit2": S(u"ліміт", 40.72),
    "tobto": S(u"Тобто", 41.13), "upyraietsia": S(u"впирається", 42.06), "video": S(u"відео", 44.62),
    "koly": S(u"коли", 46.16), "nalashtovuiu": S(u"налаштовую", 46.44), "systemu": S(u"систему", 47.10),
    "optymizuiu": S(u"оптимізую", 49.51), "vytratu": S(u"витрату", 50.09), "tokeniv2": S(u"токенів", 50.53),
    "napryklad": S(u"Наприклад", 51.13), "shablony": S(u"шаблони", 52.07), "animatsii": S(u"анімації", 53.53),
    "pysaty": S(u"писати", 54.95), "nulia": S(u"нуля", 55.67), "prosto": S(u"просто", 56.60),
    "vziaty": S(u"взяти", 57.10), "vstavyty": S(u"вставити", 57.58),
    "rozumily": S(u"розуміли", 59.60), "klod": S(u"Клод", 60.66), "sto": S(u"100", 61.30),
    "montuiu": S(u"монтую", 62.46), "desiat": S(u"10-15", 63.44), "raz": S(u"раз", 64.88),
    "bachu": S(u"бачу", 66.18), "vytrachalos": S(u"витрачалось", 67.16),
    "tomu": S(u"Тому", 68.10), "systemu2": S(u"систему", 69.55), "vpevnena": S(u"впевнена", 70.65),
    "rivni": S(u"рівні", 72.44), "shvydko": S(u"швидко", 73.02), "pyshy": S(u"пиши", 74.17),
    "test": S(u"ТЕСТ", 74.58), "komentariakh": S(u"коментарях", 75.02), "napyshu": S(u"напишу", 75.94),
    "dasy": S(u"даси", 77.65), "syre": S(u"сире", 79.23), "zmontuiu": S(u"змонтую", 80.70),
    "kloda": S(u"Клода", 81.70), "rezultat": S(u"результат", 82.90), "materiali": S(u"матеріалі", 84.34),
    "pyshy2": S(u"Пиши", 85.00), "test2": S(u"ТЕСТ", 85.39), "pobachymos": S(u"Побачимося", 86.37),
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
.sk .sf, .sk .mk { opacity: 0; visibility: hidden; }
.ab { position: absolute; }
.bub { position: absolute; padding: 22px 30px; border-radius: 30px; font-family: "GSans", sans-serif;
       font-size: 36px; font-weight: 500; line-height: 1.25; max-width: 560px; }
.bub.in { background: #f1f3f4; color: #202124; border-bottom-left-radius: 8px; }
.bub.me { background: #d3e3fd; color: #041e49; border-bottom-right-radius: 8px; }
.av { position: absolute; width: 64px; height: 64px; border-radius: 50%; display: grid; place-items: center;
      font-family: "GSans", sans-serif; font-weight: 700; font-size: 30px; color: #fff; }
.lbl { font-family: "GSans", sans-serif; font-size: 26px; font-weight: 700; letter-spacing: .14em;
       color: #5f6368; text-transform: uppercase; position: absolute; }
.row { position: absolute; display: flex; align-items: center; gap: 26px; font-family: "GSans", sans-serif; }
.track { position: absolute; height: 34px; border-radius: 17px; background: #e8eaed; overflow: hidden; }
.track i { display: block; height: 100%; width: 100%; border-radius: 17px; transform-origin: 0 50%; }
.wrap { position: absolute; display: flex; flex-wrap: wrap; gap: 16px; }
""")


def tile(x, y, w=110, h=180, fill="blue"):
    """a reel: a phone-shaped sketched card with a play triangle"""
    cx, cy = x + w / 2.0, y + h / 2.0
    s = w * 0.2
    tri = [(cx - s * 0.6, cy - s), (cx + s, cy), (cx - s * 0.6, cy + s), (cx - s * 0.6, cy - s)]
    return sk.rect(x, y, w, h, fill=fill, style="solid", sw=4) + sk.line(tri, sw=4, double=False)


# ---------------------------------------------------------------- 1 the question
L.append(
    '<div class="g" id="q" style="top:0;height:700px">'
    '<div class="gcard" id="qC" style="left:90px;top:90px;width:900px;height:500px">'
    '<div class="lbl hide" id="qL" style="left:50px;top:44px">Монтаж з Клодом</div>'
    '<div class="gs hide" id="qT" style="position:absolute;left:48px;top:84px;font-size:64px;font-weight:700">за місяць</div>'
    '<div class="hand hide" id="qQ" style="position:absolute;left:700px;top:20px;font-size:190px;color:#EA4335">?</div>'
    '<div class="hand hide" id="qF" style="position:absolute;left:50px;top:200px;font-size:58px">рілси &#215; юсадж = ?</div>'
    + sk.svg(900, 500, sk.scribble(40, 210, 560, 60, sw=8), sid="qX") +
    sk.svg(900, 500,
           sk.line([(60, 300), (60, 460), (620, 460)], sw=4, double=False) +
           sk.line([(70, 430), (150, 350), (200, 420), (270, 320), (330, 440), (400, 330),
                    (450, 400), (520, 310), (600, 380)], stroke="blue", sw=7, double=False),
           sid="qG") +
    '<div class="hand hide" id="qGL" style="position:absolute;left:650px;top:360px;font-size:56px;color:#4285F4">юсадж</div>'
    '</div></div>')


@beat
def b_q():
    sfx("pop", "@skilky+0.1")
    sfx("pencil", "@porakhuvaty", -3)
    sfx("click", "@nemozhlyvo")
    sfx("pencil", "@iusadzh-0.1", -2)
    return js("""
  h.pop("#q", @skilky+0.1, {s: 1, r: 0, y: 0, d: 0.2});
  h.pop("#qC", @skilky+0.1, {s: 0.7, r: -3});
  h.write("#qL", @montazh-0.1, 0.4);
  h.write("#qT", @misiats-0.3, 0.45);
  h.write("#qQ", @misiats, 0.35);
  h.wiggle("#qQ", @misiats+0.45);
  h.write("#qF", @porakhuvaty-0.1, 0.9);
  h.draw("#qX", @nemozhlyvo, 0.35);
  h.draw("#qG", @iusadzh-0.1, 0.9);
  h.write("#qGL", @iusadzh+0.3, 0.4);
  h.wiggle("#qG", @nepered);
  tl.to("#qC", {scale: 0.47, x: -240, y: -10, autoAlpha: 0, duration: 0.4, ease: "power3.in"}, @napered-0.35);
  tl.set("#q", {autoAlpha: 0}, @napered+0.1);
""")


# ---------------------------------------------------------------- 2 two identical tasks
def task_card(cid, left, fill):
    body = (sk.rect(40, 120, 36, 36, sw=4, round_=False) + sk.line([(100, 140), (360, 136)], sw=4, double=False) +
            sk.rect(40, 185, 36, 36, sw=4, round_=False) + sk.line([(100, 205), (330, 202)], sw=4, double=False) +
            sk.rect(40, 250, 36, 36, sw=4, round_=False) + sk.line([(100, 270), (300, 268)], sw=4, double=False))
    person = (sk.ellipse(350, 50, 22, 22, sw=4) +
              sk.line([(312, 100), (322, 80), (350, 74), (378, 80), (388, 100)], sw=4, double=False))
    return ('<div class="gcard hide" id="%s" style="left:%dpx;top:110px;width:420px;height:470px">'
            '<div class="gs" style="position:absolute;left:40px;top:36px;font-size:44px;font-weight:700">Задача</div>'
            % (cid, left) + sk.svg(420, 470, body, sid=cid + "B") +
            sk.svg(420, 470, person, sid=cid + "P") +
            '<div class="lbl" style="left:40px;top:340px">токени</div>'
            '<div class="track" style="left:40px;top:390px;width:340px"><i id="%sF" style="background:%s"></i></div>'
            '</div>' % (cid, fill))


L.append(
    '<div class="g" id="tk" style="top:0;height:700px">' + task_card("tA", 90, "#34A853") +
    task_card("tB", 570, "#EA4335") +
    '<div class="hand hide" id="tQ" style="position:absolute;left:250px;top:440px;font-size:70px;color:#EA4335">?</div>'
    '<div class="hand hide" id="tEq" style="position:absolute;left:512px;top:250px;font-size:80px">=</div>'
    '</div>')


@beat
def b_tk():
    sfx("pop", "@napered-0.2")
    sfx("pop", "@dvi")
    sfx("whoosh-short", "@riznu-0.1", -4)
    return js("""
  h.show("#tk", @napered-0.25);
  h.pop("#tA", @napered-0.25, {s: 0.6, r: -3});
  h.draw("#tAB", @napered+0.15, 0.9);
  tl.set("#tAF", {scaleX: 0}, 0);
  tl.set("#tBF", {scaleX: 0}, 0);
  h.write("#tQ", @skilky2, 0.3);
  h.wiggle("#tQ", @zadachu);
  h.pop("#tB", @dvi-0.1, {s: 0.6, r: 3});
  h.draw("#tBB", @dvi+0.1, 0.6);
  h.write("#tEq", @odnakovi, 0.3);
  h.draw("#tAP", @riznykh, 0.4);
  h.draw("#tBP", @liudei, 0.4);
  h.fadeOut("#tQ", @riznu-0.3, 0.2);
  tl.to("#tAF", {scaleX: 0.22, duration: 0.7, ease: "power2.out"}, @riznu-0.1);
  tl.to("#tBF", {scaleX: 0.92, duration: 1.1, ease: "power2.out"}, @riznu-0.1);
  h.bump("#tB", @tokeniv);
  h.out("#tA", @oriientyr-0.35, 0.25);
  h.out("#tB", @oriientyr-0.35, 0.25);
  h.fadeOut("#tEq", @oriientyr-0.35, 0.2);
  tl.set("#tk", {autoAlpha: 0}, @oriientyr);
""")


# ---------------------------------------------------------------- 3 «орієнтир» pill -> OVER board 1
L.append(
    '<div class="g" id="or" style="top:0;height:700px">'
    '<div class="pill hide" id="orP" style="left:330px;top:250px;height:110px;padding:0 44px 0 34px;font-size:52px;font-weight:700">'
    '<span style="display:inline-block;width:40px;height:40px;border-radius:50%;background:#34A853"></span>орієнтир</div>'
    '</div>')

LEFT = [("on", "cE", u"експертні"), ("on", "cK", u"на камеру"), ("on", "cS", u"суфлер"), ("cg", "c23", u"2-3 хв")]
RIGHT = [("cy", "cD", u"довші"), ("cr", "c56", u"5-6 хв"), ("cy", "cV", u"багато вставок"), ("cy", "cP", u"помилки")]


def chips(left, items):
    return ('<div class="wrap" style="left:%dpx;top:440px;width:450px">' % left +
            "".join('<span class="chip %s hide" id="%s">%s</span>' % c for c in items) + '</div>')


LT = [(100, 720), (235, 720), (370, 720), (100, 930), (235, 930)]
RT = [(600, 720), (735, 720), (870, 720)]
L.append(
    '<div class="g full" id="bd">'
    '<div class="board"></div>'
    '<div class="lbl hide" id="bL" style="left:100px;top:150px">Підписка Клода</div>'
    '<div class="num hide" id="b20" style="position:absolute;left:92px;top:180px;font-size:150px">$20</div>'
    '<div class="gs hide" id="bLim" style="position:absolute;left:520px;top:200px;font-size:36px;font-weight:700">Ліміт на 5 годин</div>'
    '<div class="track hide" id="bTr" style="left:520px;top:270px;width:460px"><i id="bF" style="background:#4285F4"></i></div>'
    + sk.svg(1080, 1300, sk.line([(540, 450), (546, 800), (538, 1180)], sw=4, double=False), sid="bDiv")
    + chips(80, LEFT) + chips(570, RIGHT)
    + "".join(sk.svg(1080, 1300, tile(x, y), sid="lt%d" % i) for i, (x, y) in enumerate(LT))
    + '<div class="hand hide" id="lMore" style="position:absolute;left:372px;top:965px;font-size:52px;color:#4285F4">+ ще</div>'
    + sk.svg(1080, 1300, sk.rect(370, 930, 110, 180, sw=4), sid="lDash", style="opacity:.45")
    + '<div class="hand hide" id="lN" style="position:absolute;left:100px;top:1130px;font-size:56px">5 рілсів</div>'
    + "".join(sk.svg(1080, 1300, tile(x, y, fill="yellow"), sid="rt%d" % i) for i, (x, y) in enumerate(RT))
    + '<div class="hand hide" id="rN" style="position:absolute;left:600px;top:925px;font-size:56px">3 рілси</div>'
    + sk.svg(1080, 1300, sk.circle_around(300, 525, 250, 120, stroke="red", sw=6), sid="lLoop")
    + sk.svg(1080, 1300, sk.circle_around(790, 525, 250, 120, stroke="red", sw=6), sid="rLoop")
    + '</div>')


@beat
def b_board():
    sfx("pop", "@oriientyr-0.05")
    sfx("whoosh-short", "@na-0.1")
    sfx("kaching", "@dvadtsiat")
    sfx("click-soft", "@odyn")
    sfx("pencil", "@piat-0.1", -2)
    sfx("pop", "@ekspertni")
    sfx("pop", "@dvitry")
    sfx("pop", "@dovshe")
    sfx("pop", "@vstavok")
    sfx("pencil", "@try-0.1", -2)
    sfx("pencil", "@upyraietsia", -3)
    sfx("whoosh-short", "@video+0.3")
    lt = "\n".join('  h.draw("#lt%d", @piat-0.1+%.2f, 0.32);' % (i, i * 0.22) for i in range(5))
    rt = "\n".join('  h.draw("#rt%d", @try-0.1+%.2f, 0.32);' % (i, i * 0.25) for i in range(3))
    return js("""
  h.show("#or", @oriientyr-0.1);
  h.pop("#orP", @oriientyr-0.1, {s: 0.5, r: -4});
  h.boardIn("#bd", @na-0.15, 540, 305, 0.75);
  tl.set("#or", {autoAlpha: 0}, @na+0.6);
  h.write("#bL", @na+0.3, 0.4);
  h.pop("#b20", @dvadtsiat-0.05, {s: 0.5, r: -5});
  h.write("#bLim", @odyn, 0.5);
  h.pop("#bTr", @odyn+0.1, {s: 0.9, r: 0, y: 0});
  tl.set("#bF", {scaleX: 0}, 0);
  tl.to("#bF", {scaleX: 0.9, duration: 1.6, ease: "power1.inOut"}, @piat-0.2);
""" + lt + """
  h.write("#lN", @piat+0.6, 0.45);
  h.draw("#bDiv", @ekspertni-0.3, 0.5);
  h.pop("#cE", @ekspertni-0.1, {s: 0.5, r: -4});
  h.pop("#cK", @kameru-0.15, {s: 0.5, r: 4});
  h.pop("#cS", @sufliera-0.1, {s: 0.5, r: -4});
  h.pop("#c23", @dvitry-0.1, {s: 0.5, r: 4});
  h.draw("#lDash", @bilshe-0.1, 0.4);
  h.write("#lMore", @bilshe+0.1, 0.4);
  /* the same limit, longer videos */
  tl.to("#bF", {scaleX: 0, duration: 0.35, ease: "power2.in"}, @yakshcho2);
  h.pop("#cD", @dovshe-0.1, {s: 0.5, r: -4});
  h.pop("#c56", @piatshist-0.1, {s: 0.5, r: 4});
  h.pop("#cV", @vstavok-0.15, {s: 0.5, r: -4});
  h.pop("#cP", @pomylok-0.1, {s: 0.5, r: 4});
  tl.to("#bF", {scaleX: 0.9, duration: 1.2, ease: "power1.inOut"}, @try-0.2);
""" + rt + """
  h.write("#rN", @try+0.7, 0.45);
  h.draw("#lLoop", @upyraietsia-0.1, 0.5);
  h.draw("#rLoop", @upyraietsia+0.4, 0.5);
  h.boardOut("#bd", @video+0.3, 540, 700, 0.55);
""")


# ---------------------------------------------------------------- 4 the client's system: optimise tokens
L.append(
    '<div class="g" id="sys" style="top:0;height:700px">'
    '<div class="gcard" id="sysC" style="left:90px;top:110px;width:900px;height:420px">'
    '<div class="lbl" style="left:50px;top:44px">Система для клієнтки</div>'
    '<div class="row" style="left:50px;top:110px;width:800px;height:120px">'
    '<div class="gs" style="font-size:46px;font-weight:700;flex:1">Оптимізація токенів</div></div>'
    '<div class="tgl" id="sysT" style="left:746px;top:138px"><b></b></div>'
    '<div class="lbl" style="left:50px;top:270px">токени на рілс</div>'
    '<div class="track" style="left:50px;top:320px;width:800px"><i id="sysF" style="background:#FBBC04"></i></div>'
    '</div></div>')


@beat
def b_sys():
    sfx("pop", "@nalashtovuiu-0.1")
    sfx("click", "@optymizuiu")
    sfx("whoosh-short", "@vytratu", -4)
    return js("""
  h.show("#sys", @nalashtovuiu-0.15);
  h.pop("#sysC", @nalashtovuiu-0.15, {s: 0.7, r: 3});
  tl.set("#sysF", {scaleX: 0.85}, 0);
  h.toggle("#sysT", @optymizuiu, "#0b57d0");
  tl.to("#sysF", {scaleX: 0.3, duration: 0.9, ease: "power2.inOut"}, @vytratu);
  h.bump("#sysT", @tokeniv2+0.2);
""")


# ---------------------------------------------------------------- 5 OVER board 2: templates
def tpl(x, y, motif, lab, cid):
    return (sk.svg(1080, 1300, sk.rect(x, y, 260, 200, sw=4.5) + motif, sid=cid) +
            '<div class="gs hide" id="%sL" style="position:absolute;left:%dpx;top:%dpx;width:260px;text-align:center;'
            'font-size:30px;color:#5f6368;font-weight:500">%s</div>' % (cid, x, y + 212, lab))


M1 = (sk.rect(150, 370, 180, 110, stroke="blue", fill="blue", style="solid", sw=3.5) +
      sk.line([(170, 400), (290, 398)], sw=3.5, double=False) + sk.line([(170, 435), (250, 433)], sw=3.5, double=False))
M2 = sk.arrow([(450, 470), (530, 380), (630, 400)], stroke="red", sw=5)
M3 = (sk.rect(745, 420, 40, 70, fill="green", style="solid", sw=3.5, round_=False) +
      sk.rect(805, 390, 40, 100, fill="yellow", style="solid", sw=3.5, round_=False) +
      sk.rect(865, 360, 40, 130, fill="blue", style="solid", sw=3.5, round_=False))
CODE = "".join(sk.line([(150, y), (150 + w, y + 3)], stroke="#5f6368", sw=4, double=False)
               for y, w in [(760, 300), (800, 240), (840, 330), (880, 200), (920, 280), (960, 320), (1000, 180)])
L.append(
    '<div class="g full" id="bd2">'
    '<div class="board"></div>'
    '<div class="hand hide" id="b2T" style="position:absolute;left:110px;top:150px;font-size:80px">шаблони анімації</div>'
    + sk.svg(1080, 1300, sk.underline(110, 262, 600, stroke="blue"), sid="b2U")
    + tpl(110, 330, M1, u"картка", "tp1") + tpl(410, 330, M2, u"стрілка", "tp2") + tpl(710, 330, M3, u"графік", "tp3")
    + sk.svg(1080, 1300, sk.rect(110, 700, 420, 360, sw=4.5) + CODE, sid="code")
    + '<div class="hand hide" id="codeL" style="position:absolute;left:120px;top:1075px;font-size:54px">з нуля</div>'
    + sk.svg(1080, 1300, sk.cross(200, 760, 240, sw=12), sid="codeX")
    + sk.svg(1080, 1300, sk.rect(700, 660, 240, 420, sw=5) + sk.line([(780, 690), (860, 690)], sw=4, double=False),
             sid="ph")
    + '<div class="gs hide" id="phL" style="position:absolute;left:700px;top:1095px;width:240px;text-align:center;font-size:34px;font-weight:700">рілс</div>'
    + '<div class="ab hide" id="mv" style="left:410px;top:330px;width:260px;height:200px;border-radius:22px;background:#fff;box-shadow:0 10px 30px rgba(0,0,0,.2)">'
    + sk.svg(260, 200, sk.rect(4, 4, 252, 192, sw=4.5) + sk.arrow([(40, 140), (120, 50), (220, 70)], stroke="red", sw=5),
             sid="mvS", style="left:0;top:0")
    + '</div>'
    + sk.svg(1080, 1300, sk.check(960, 880, 90), sid="phOK")
    + '</div>')


@beat
def b_board2():
    sfx("whoosh-short", "@napryklad")
    sfx("pencil", "@shablony", -2)
    sfx("pencil", "@pysaty-0.5", -3)
    sfx("click", "@nulia")
    sfx("pop", "@vziaty")
    sfx("ping", "@vstavyty+0.25", -3)
    sfx("whoosh-short", "@vstavyty+0.5")
    return js("""
  tl.to("#sysC", {scale: 1.06, duration: 0.3, ease: "power2.in"}, @napryklad-0.3);
  h.boardIn("#bd2", @napryklad-0.2, 790, 280, 0.75);
  tl.set("#sys", {autoAlpha: 0}, @napryklad+0.6);
  h.write("#b2T", @napryklad+0.3, 0.7);
  h.draw("#b2U", @shablony-0.2, 0.35);
  h.draw("#tp1", @shablony, 0.5);
  h.write("#tp1L", @shablony+0.3, 0.3);
  h.draw("#tp2", @shablony+0.5, 0.5);
  h.write("#tp2L", @shablony+0.8, 0.3);
  h.draw("#tp3", @shablony+1.0, 0.5);
  h.write("#tp3L", @shablony+1.3, 0.3);
  h.draw("#ph", @animatsii+0.1, 0.5);
  h.write("#phL", @animatsii+0.4, 0.3);
  h.draw("#code", @pysaty-0.6, 0.9);
  h.write("#codeL", @pysaty+0.1, 0.4);
  h.draw("#codeX", @nulia, 0.35);
  tl.set("#mv", {autoAlpha: 1}, @prosto);
  h.draw("#mvS", @prosto-0.01, 0.01);
  tl.fromTo("#mv", {x: 0, y: 0, scale: 1, rotation: 0}, {x: 280, y: 440, scale: 0.8, rotation: -4, duration: 0.7, ease: SP, immediateRender: false}, @vziaty);
  h.draw("#phOK", @vstavyty+0.1, 0.3);
  h.boardOut("#bd2", @vstavyty+0.55, 820, 870, 0.55);
""")


# ---------------------------------------------------------------- 6 my €100 plan: 10-15 reels, the limit barely moves
L.append(
    '<div class="g" id="pl" style="top:0;height:700px">'
    '<div class="gcard" id="plC" style="left:90px;top:80px;width:900px;height:560px;overflow:hidden">'
    '<div class="lbl" style="left:50px;top:40px">Мій тариф</div>'
    '<div class="num hide" id="pl100" style="position:absolute;left:44px;top:66px;font-size:130px">&#8364;100</div>'
    '<div class="ab hide" id="plK" style="left:600px;top:96px"><span class="chip on" style="font-size:40px;height:84px">Клод</span></div>'
    + "".join(sk.svg(900, 560, tile(50 + i * 100, 250, 80, 130, fill=("blue", "yellow", "green", "red")[i % 4]),
                     sid="pt%d" % i) for i in range(10)) +
    '<div style="position:absolute;right:0;top:240px;width:160px;height:160px;background:linear-gradient(90deg,rgba(255,255,255,0),#fff)"></div>'
    '<div class="hand hide" id="plN" style="position:absolute;left:50px;top:392px;font-size:52px">10-15 рілсів за раз</div>'
    '<div class="lbl" style="left:50px;top:470px">Ліміт</div>'
    '<div class="track" style="left:180px;top:466px;width:520px"><i id="plF" style="background:#4285F4"></i></div>'
    + sk.svg(900, 560, sk.ellipse(200, 482, 46, 46, sw=5) + sk.line([(234, 516), (280, 556)], sw=8, double=False),
             sid="plM") +
    '</div></div>')


@beat
def b_pl():
    sfx("pop", "@klod-0.1")
    sfx("kaching", "@sto")
    sfx("pencil", "@bachu-0.2", -3)
    pts = "\n".join('  h.draw("#pt%d", @montuiu+%.2f, 0.25);' % (i, i * 0.16) for i in range(10))
    return js("""
  h.show("#pl", @klod-0.15);
  h.pop("#plC", @klod-0.15, {s: 0.7, r: -3});
  h.pop("#plK", @klod+0.05, {s: 0.5, r: 4});
  h.pop("#pl100", @sto-0.05, {s: 0.5, r: -5});
  tl.set("#plF", {scaleX: 0.03}, 0);
""" + pts + """
  h.write("#plN", @desiat, 0.6);
  h.draw("#plM", @bachu-0.2, 0.5);
  h.bump("#plM", @vytrachalos);
  tl.to("#plC", {y: -30, autoAlpha: 0, duration: 0.3, ease: "power2.in"}, @tomu-0.35);
  tl.set("#pl", {autoAlpha: 0}, @tomu);
""")


# ---------------------------------------------------------------- 7 CTA: doubts -> comment ТЕСТ -> DM -> result
L.append(
    '<div class="g" id="dbt" style="top:0;height:700px">'
    '<div class="gcard" id="dbC" style="left:90px;top:110px;width:900px;height:420px">'
    '<div class="lbl" style="left:50px;top:44px">Система для себе</div>'
    '<div class="gs" style="position:absolute;left:48px;top:88px;font-size:52px;font-weight:700">Клод змонтує?</div>'
    '<div class="hand hide" id="dbQ" style="position:absolute;left:720px;top:40px;font-size:200px;color:#EA4335">?</div>'
    '<div class="ab" style="left:50px;top:250px;display:flex;gap:20px">'
    '<span class="chip cy hide" id="dbR">на твоєму рівні?</span><span class="chip cy hide" id="dbS">так швидко?</span></div>'
    '</div></div>')


def cmt(cid, tid):
    return ('<div class="pill hide" id="%s" style="left:140px;top:270px;width:800px;height:110px;padding:0 40px;font-size:36px">'
            '<span style="color:#5f6368">Коментар:</span><span id="%s" data-text="ТЕСТ" style="font-weight:700;font-size:50px"></span></div>'
            % (cid, tid))


L.append('<div class="g" id="cm" style="top:0;height:700px">' + cmt("cmP", "cmT") + '</div>')
L.append('<div class="g" id="cm2" style="top:0;height:700px">' + cmt("cm2P", "cm2T") + '</div>')
L.append(
    '<div class="g" id="dm" style="top:0;height:700px">'
    '<div class="gcard" id="dmC" style="left:90px;top:60px;width:900px;height:590px">'
    '<div class="av" style="left:36px;top:30px;background:#4285F4">Р</div>'
    '<div class="gs" style="position:absolute;left:122px;top:34px;font-size:34px;font-weight:700">Рута</div>'
    '<div class="gs" style="position:absolute;left:122px;top:76px;font-size:24px;color:#5f6368">Direct</div>'
    '<div style="position:absolute;left:0;right:0;top:124px;height:2px;background:#e8eaed"></div>'
    '<div class="bub in hide" id="dm1" style="left:36px;top:150px">Привіт! Скинь одне сире відео</div>'
    '<div class="bub me hide" id="dm2" style="right:36px;top:250px">сире відео.mp4</div>'
    '<div class="ab hide" id="dmK" style="left:36px;top:372px"><span class="chip on">Клод</span></div>'
    '<div class="dots hide" id="dmD" style="left:220px;top:394px"><i></i><i></i><i></i><i></i></div>'
    '<div class="bub in hide" id="dm3" style="left:36px;top:470px">Готово, ось результат</div>'
    + sk.svg(900, 590, sk.check(450, 470, 70), sid="dmOK") +
    '</div></div>')


@beat
def b_cta():
    sfx("pop", "@systemu2-0.2")
    sfx("pencil", "@vpevnena", -4)
    sfx("pop", "@shvydko")
    sfx("pop", "@pyshy-0.1")
    sfx("key-press", "@test")
    sfx("notification", "@napyshu")
    sfx("pop", "@syre")
    sfx("ping", "@rezultat")
    sfx("pop", "@pyshy2")
    sfx("key-press", "@test2")
    return js("""
  h.show("#dbt", @systemu2-0.2);
  h.pop("#dbC", @systemu2-0.2, {s: 0.7, r: 3});
  h.write("#dbQ", @vpevnena, 0.35);
  h.wiggle("#dbQ", @vpevnena+0.4);
  h.pop("#dbR", @rivni-0.1, {s: 0.5, r: -4});
  h.pop("#dbS", @shvydko-0.1, {s: 0.5, r: 4});
  tl.to("#dbC", {y: -30, autoAlpha: 0, duration: 0.25, ease: "power2.in"}, @pyshy-0.3);
  tl.set("#dbt", {autoAlpha: 0}, @pyshy);
  h.show("#cm", @pyshy-0.1);
  h.pop("#cmP", @pyshy-0.1, {s: 0.8, r: 0, y: 20});
  h.type("#cmT", @test, 8);
  h.bump("#cmP", @komentariakh);
  tl.to("#cmP", {y: -40, autoAlpha: 0, duration: 0.25, ease: "power2.in"}, @napyshu-0.3);
  tl.set("#cm", {autoAlpha: 0}, @napyshu);
  h.show("#dm", @napyshu-0.15);
  h.pop("#dmC", @napyshu-0.15, {s: 0.75, r: -2});
  h.pop("#dm1", @napyshu+0.1, {s: 0.5, r: 0});
  h.pop("#dm2", @syre-0.1, {s: 0.5, r: 0});
  h.pop("#dmK", @zmontuiu-0.1, {s: 0.5, r: -4});
  h.pop("#dmD", @zmontuiu, {s: 0.5, r: 0});
  h.think("#dmD", @zmontuiu+0.1, 1.9);
  h.bump("#dmK", @kloda);
  h.out("#dmD", @rezultat-0.2, 0.15);
  h.pop("#dm3", @rezultat-0.1, {s: 0.6, r: 2});
  h.draw("#dmOK", @rezultat+0.3, 0.35);
  tl.to("#dmC", {y: -30, autoAlpha: 0, duration: 0.3, ease: "power2.in"}, @pyshy2-0.3);
  tl.set("#dm", {autoAlpha: 0}, @pyshy2);
  h.show("#cm2", @pyshy2-0.1);
  h.pop("#cm2P", @pyshy2-0.1, {s: 0.8, r: 0, y: 20});
  h.type("#cm2T", @test2, 8);
  h.bump("#cm2P", @pobachymos);
""")


INVERT = [(T["na"] + 0.3, T["video"] + 0.7, ""), (T["napryklad"] + 0.3, T["vstavyty"] + 0.95, "")]
BLACKOUT = [(T["dvadtsiat"], T["odyn"], u"$20"), (T["sto"], T["montuiu"] - 0.2, u"€100"),
            (T["test"], T["komentariakh"], u"ТЕСТ"), (T["test2"], T["test2"] + 0.25, u"ТЕСТ")]


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
        title=u"Reel 44 — скільки коштує монтаж з Клодом",
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
