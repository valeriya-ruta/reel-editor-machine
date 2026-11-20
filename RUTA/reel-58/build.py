# -*- coding: utf-8 -*-
"""Reel 58 — «Автоматизація без бану». Posts 2026-11-20.

Google x Excalidraw look (STYLE.md §0b), skeleton from reel-45/build.py.
Cut from her raw take by tools/cut.py (no closeups: no_paint is empty).

Chain: NEAR the Direct card: sent bubbles, «150» counts, «Акаунт заблоковано»
crossed out -> the same card becomes her task list (leads, three checkbox
rows), the «Клод» pill lands and ticks them, «менеджер», chips «не
втомлюється» / «безкоштовно» -> OVER the board wipes in from the pill: the
internal browser sketched, «= Chrome», a blue «Клод» frame around it, «швидше»
-> closes onto the browser -> NEAR the browser card: instagram.com/direct, the
prompt, a cursor walking people rows, bubbles, ticks -> red banner, «бот?»,
stamp «БАН» -> folds into a sticky note «2 речі» -> OVER the board from the
note: «1 пауза» timeline with 30-40 с gaps, «довше» vs «заблокували акаунт»;
pan to «2 персоналізація»: name-only bubble -> full message, Клод -> profile ->
message, «мій скрипт» -> closes onto the message -> NEAR the Direct card again
«150+», «без жодної проблеми» -> CTA «Підписатися» clicked.

usage: python build.py   (then: python ../tools/sfx.py mix 58)
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

NN = "58"
CUT = json.load(io.open(os.path.join(ROOT, "work", "r" + NN, "cut.json"), encoding="utf-8"))
DUR = 90.017           # (2701 plate frames - 0.5) / 30
FPS = 30
k = Kit(width=1080, height=1920, fps=FPS, duration=DUR)
k.cap_font = "assets/fonts/ProductSans-Bold.ttf"
k.css(sketch_css())
sk = Sketch(seed=42)

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
        (u"і", 4.70, u"І"), (u"аудиторією", 10.97, u"аудиторією,"), (u"повідомлення", 13.86, u"повідомлення,"),
        (u"То", 14.53, u"то"), (u"про чось,", 13.12, u"про щось,"), (u"можу", 16.78, u"може"),
        (u"Входиш", 35.57, u"входиш"), (u"От і", 39.40, u"І,"), (u"нюанс:", 45.54, u"нюанс,"),
        (u"і", 50.43, u"І"), (u"і дві", 52.52, u"є дві"), (u"Перша", 55.40, u"Перше"),
        (u"цепь", 55.99, u"це"), (u"Ніж", 58.47, u"між"), (u"Ми", 66.57, u"ми"),
        (u"Не", 71.63, u"не"), (u"Тут", 74.28, u"тут"), (u"Так", 81.59, u"так"),
        (u"корисно", 88.00, u"корисно,"), (u"санкціонована", 48.66, u"несанкціонована"),
    ]
    for w, near, new in edits:
        caps[find(w, near)]["w"] = new
    # «не санкціонована» is one word: fold «не» into it
    i = find(u"несанкціонована", 48.66)
    assert caps[i - 1]["w"] == u"не"
    caps[i]["s"] = caps[i - 1]["s"]
    del caps[i - 1]
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
    "vidpravyv": S(u"відправив", 0.81), "n150": S(u"150", 2.39), "povidomlen": S(u"повідомлень", 3.29),
    "zhodnoho": S(u"жодного", 4.93), "insta1": S(u"Інстаграм", 5.93), "ne1": S(u"не", 6.81),
    "zablokuvav": S(u"заблокував", 7.05), "korotshe": S(u"Коротше", 7.70), "auditoriieiu": S(u"аудиторією", 10.97),
    "pysaty": S(u"писати", 11.65), "nahaduvaty": S(u"нагадувати", 12.39), "rozsylaty": S(u"розсилати", 13.44),
    "metod": S(u"метод", 14.96), "klod1": S(u"Клод", 15.83), "pratsiuvaty": S(u"працювати", 17.14),
    "menedzher": S(u"менеджер", 18.26), "nikoly": S(u"ніколи", 19.44), "vtomliuietsia": S(u"втомлюється", 19.82),
    "bezkoshtovno": S(u"безкоштовно", 20.76), "zavdiaky": S(u"завдяки", 22.50),
    "vnutrishnomu": S(u"внутрішньому", 23.03), "kloda1": S(u"Клода", 24.96), "vnutrishnii": S(u"Внутрішній", 25.57),
    "khrom": S(u"хром", 28.12), "zvychainyi": S(u"звичайний", 28.90), "vseredyni": S(u"всередині", 30.84),
    "kloda2": S(u"Клода", 31.50), "oriientuietsia": S(u"орієнтується", 32.62), "shvydshe": S(u"швидше", 33.85),
    "vidkryvaiesh": S(u"Відкриваєш", 34.23), "brauzer3": S(u"браузер", 35.00), "vkhodysh": S(u"входиш", 35.57),
    "instahrami": S(u"Інстаграмі", 36.53), "prosysh": S(u"просиш", 37.37), "rozislaty": S(u"розіслати", 37.95),
    "vse": S(u"все", 40.27), "khodyty": S(u"ходити", 41.09), "shukaty": S(u"шукати", 42.23),
    "pysaty2": S(u"писати", 43.11), "vidpravliaty": S(u"відправляти", 43.69), "ale": S(u"Але", 44.27),
    "niuans": S(u"нюанс", 45.54), "instahramu": S(u"Інстаграму", 46.12), "podobaietsia": S(u"подобається", 47.38),
    "nesanktsionovana": S(u"несанкціонована", 48.48), "botiv": S(u"ботів", 49.88), "daty": S(u"дати", 51.36),
    "shaptsi": S(u"шапці", 51.75), "dvi": S(u"дві", 52.52), "propysuiu": S(u"прописую", 53.68),
    "stalos": S(u"сталось", 54.88), "pershe": S(u"Перше", 55.40), "pauza": S(u"пауза", 56.27),
    "minimum": S(u"мінімум", 57.08), "n3040": S(u"30-40", 57.46), "mizh": S(u"між", 58.47),
    "diieiu": S(u"дією", 59.90), "vyhliadalo": S(u"виглядало", 60.72), "bota": S(u"бота", 61.90),
    "zaimaie": S(u"займає", 63.07), "chasu": S(u"часу", 63.89), "dovshe": S(u"довше", 64.79),
    "zablokuvaly": S(u"заблокували", 65.37), "obyraiemo": S(u"обираємо", 66.94), "dovshe2": S(u"довше", 67.36),
    "druhe": S(u"Друге", 67.87), "personalizatsiia": S(u"персоналізація", 68.68), "hlybsha": S(u"глибша", 70.10),
    "prosto": S(u"просто", 71.85), "imia": S(u"ім'я", 72.15), "same": S(u"саме", 72.75),
    "povidomlennia7": S(u"повідомлення", 73.21), "klod7": S(u"Клод", 75.38), "zaity": S(u"зайти", 76.10),
    "profil": S(u"профіль", 76.50), "podyvytys": S(u"подивитись", 77.16), "zaimaietsia": S(u"займається", 78.07),
    "vpysaty": S(u"вписати", 78.77), "tekst": S(u"текст", 79.69), "moim": S(u"моїм", 80.31),
    "skryptom": S(u"скриптом", 80.55), "tomu8": S(u"Тому", 81.10), "rozislala": S(u"розіслала", 82.01),
    "bilshe8": S(u"більше", 82.69), "n150b": S(u"150", 83.01), "bez": S(u"без", 84.25),
    "problemy": S(u"проблеми", 85.15), "korystuius": S(u"користуюсь", 86.33), "yakshcho": S(u"Якщо", 87.07),
    "korysno": S(u"корисно", 88.00), "pidpyshys": S(u"підпишись", 89.32),
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
       font-size: 36px; font-weight: 500; line-height: 1.25; max-width: 600px; }
.bub.in { background: #f1f3f4; color: #202124; border-bottom-left-radius: 8px; }
.bub.me { background: #d3e3fd; color: #041e49; border-bottom-right-radius: 8px; }
.av { position: absolute; width: 64px; height: 64px; border-radius: 50%; display: grid; place-items: center;
      font-family: "GSans", sans-serif; font-weight: 700; font-size: 30px; color: #fff; }
.lbl { font-family: "GSans", sans-serif; font-size: 26px; font-weight: 700; letter-spacing: .14em;
       color: #5f6368; text-transform: uppercase; position: absolute; }
.field { position: absolute; border-radius: 16px; border: 2px solid #747775; background: #fff; }
.row { position: absolute; display: flex; align-items: center; gap: 26px; font-family: "GSans", sans-serif; }
.hdr { position: absolute; left: 0; right: 0; top: 0; height: 110px; border-bottom: 2px solid #e8eaed; }
.gl { position: absolute; height: 18px; border-radius: 9px; background: #e8eaed; }
.cur { position: absolute; left: 0; top: 0; width: 56px; height: 80px; }
.btn { position: absolute; display: flex; align-items: center; justify-content: center; gap: 16px;
       border-radius: 999px; font-family: "GSans", sans-serif; font-weight: 700; }
""")

CURSOR = ('<svg class="cur" viewBox="0 0 56 80" width="56" height="80">'
          '<path d="M4 4 L4 64 L18 51 L29 75 L40 70 L29 46 L50 46 Z" fill="#1e1e1e" stroke="#fff" '
          'stroke-width="4" stroke-linejoin="round"/></svg>')


def header(title, sub):
    return ('<div class="hdr"><div class="av" style="left:36px;top:24px;background:#EA4335">I</div>'
            '<div class="gs" style="position:absolute;left:122px;top:22px;font-size:34px;font-weight:700">%s</div>'
            '<div class="gs" style="position:absolute;left:122px;top:64px;font-size:24px;color:#5f6368">%s</div></div>'
            % (title, sub))


# ---------------------------------------------------------------- 1 the Direct card: 150 sent, not banned
L.append(
    '<div class="g" id="dc" style="top:0;height:700px">'
    '<div class="sheet hide" id="dcC" style="height:700px;background:#f1f3f4">'
    '<div class="gcard" id="dcI" style="left:100px;top:90px;width:880px;height:580px">'
    '<div id="h1">' + header("Instagram", "Direct") +
    '<div class="num hide" id="cnt" style="position:absolute;left:44px;top:140px;font-size:170px;color:#4285F4">0</div>'
    '<div class="hand hide" id="cntT" style="position:absolute;left:52px;top:330px;font-size:54px">повідомлень</div>'
    '<div class="bub me hide" id="b1" style="right:36px;top:140px;width:330px;height:64px;padding:0"></div>'
    '<div class="bub me hide" id="b2" style="right:36px;top:222px;width:280px;height:64px;padding:0"></div>'
    '<div class="bub me hide" id="b3" style="right:36px;top:304px;width:340px;height:64px;padding:0"></div>'
    + sk.svg(880, 580,
             sk.line([(530, 172), (640, 168), (790, 174)], stroke="#041e49", sw=5, double=False) +
             sk.line([(580, 254), (700, 250), (800, 256)], stroke="#041e49", sw=5, double=False) +
             sk.line([(520, 336), (660, 332), (800, 338)], stroke="#041e49", sw=5, double=False),
             sid="bS") +
    '<div class="ab hide" id="ban" style="left:52px;top:452px"><span class="chip cr" style="height:84px;font-size:38px">'
    'Акаунт заблоковано</span></div>'
    + sk.svg(880, 580, sk.cross(150, 438, 110, sw=11) + sk.scribble(60, 480, 420, 26, sw=7), sid="banX")
    + sk.svg(880, 580, sk.check(680, 450, 100, sw=11), sid="okH") +
    '</div>'
    # ---- 2 the same card: her task list
    '<div id="h2">'
    '<div class="gs hide" id="tT" style="position:absolute;left:44px;top:40px;font-size:40px;font-weight:700">Мої ліди</div>'
    '<div class="av hide" id="a1" style="left:250px;top:30px;background:#4285F4">О</div>'
    '<div class="av hide" id="a2" style="left:300px;top:30px;background:#34A853">М</div>'
    '<div class="av hide" id="a3" style="left:350px;top:30px;background:#FBBC04">А</div>'
    + sk.svg(880, 580,
             sk.rect(44, 150, 58, 58, sw=4.5, round_=False), sid="cb1") +
    sk.svg(880, 580, sk.rect(44, 250, 58, 58, sw=4.5, round_=False), sid="cb2") +
    sk.svg(880, 580, sk.rect(44, 350, 58, 58, sw=4.5, round_=False), sid="cb3") +
    '<div class="hand hide" id="r1" style="position:absolute;left:132px;top:150px;font-size:54px">писати лідам</div>'
    '<div class="hand hide" id="r2" style="position:absolute;left:132px;top:250px;font-size:54px">нагадувати</div>'
    '<div class="hand hide" id="r3" style="position:absolute;left:132px;top:350px;font-size:54px">розсилати повідомлення</div>'
    + sk.svg(880, 580, sk.check(48, 140, 62, sw=9), sid="ck1")
    + sk.svg(880, 580, sk.check(48, 240, 62, sw=9), sid="ck2")
    + sk.svg(880, 580, sk.check(48, 340, 62, sw=9), sid="ck3") +
    '<div class="pill hide" id="kp" style="left:600px;top:26px;height:84px;padding:0 34px 0 22px;font-size:38px;font-weight:700;box-shadow:var(--e1)">'
    '<span style="display:inline-block;width:40px;height:40px;border-radius:50%;background:#D97757"></span>Клод</div>'
    '<div class="hand hide" id="kpT" style="position:absolute;left:610px;top:112px;font-size:46px;color:#4285F4">менеджер</div>'
    '<div class="ab" style="left:44px;top:470px;display:flex;gap:18px">'
    '<span class="chip cg hide" id="ch1">не втомлюється</span>'
    '<span class="chip cy hide" id="ch2">безкоштовно</span></div>'
    '</div>'
    '</div></div></div>')


@beat
def b_dc():
    sfx("pop", "@vidpravyv-0.4")
    sfx("ping", "@vidpravyv")
    sfx("click-soft", "@n150")
    sfx("pop", "@insta1")
    sfx("pencil", "@ne1", -2)
    return js("""
  h.show("#dc", 0);
  h.sheetIn("#dcC", 0.0, 700);
  h.pop("#b1", @vidpravyv, {s: 0.5, r: 3});
  h.pop("#b2", @vidpravyv+0.3, {s: 0.5, r: -3});
  h.pop("#b3", @vidpravyv+0.6, {s: 0.5, r: 3});
  h.draw("#bS", @vidpravyv+0.2, 0.9);
  h.show("#cnt", @n150-0.05);
  h.count("#cnt", @n150-0.05, 150, 0.8);
  h.write("#cntT", @povidomlen, 0.5);
  h.pop("#ban", @insta1-0.1, {s: 0.5, r: -5});
  h.draw("#banX", @ne1, 0.4);
  h.draw("#okH", @zablokuvav, 0.35);
  h.bump("#cnt", @zablokuvav+0.1);
  /* -> the same card becomes her list */
  tl.to("#h1", {autoAlpha: 0, duration: 0.25, ease: "power1.in"}, @korotshe-0.05);
  h.bump("#dcI", @korotshe+0.1);
""")


@beat
def b_tasks():
    sfx("pop", "@auditoriieiu")
    sfx("pencil", "@pysaty", -3)
    sfx("pop", "@klod1")
    sfx("click-soft", "@pratsiuvaty")
    sfx("pop", "@vtomliuietsia")
    sfx("kaching", "@bezkoshtovno", -2)
    return js("""
  h.write("#tT", @korotshe+0.4, 0.5);
  h.pop("#a1", @auditoriieiu-0.05, {s: 0.3, r: 0});
  h.pop("#a2", @auditoriieiu+0.1, {s: 0.3, r: 0});
  h.pop("#a3", @auditoriieiu+0.25, {s: 0.3, r: 0});
  h.draw("#cb1", @pysaty-0.1, 0.3);  h.write("#r1", @pysaty, 0.5);
  h.draw("#cb2", @nahaduvaty-0.1, 0.3);  h.write("#r2", @nahaduvaty, 0.5);
  h.draw("#cb3", @rozsylaty-0.1, 0.3);  h.write("#r3", @rozsylaty, 0.7);
  h.wiggle("#tT", @metod);
  h.pop("#kp", @klod1-0.05, {s: 0.4, r: 6});
  h.draw("#ck1", @pratsiuvaty, 0.25);
  h.draw("#ck2", @pratsiuvaty+0.35, 0.25);
  h.draw("#ck3", @pratsiuvaty+0.7, 0.25);
  h.write("#kpT", @menedzher, 0.5);
  h.pop("#ch1", @vtomliuietsia-0.05, {s: 0.5, r: -4});
  h.pop("#ch2", @bezkoshtovno, {s: 0.5, r: 4});
  h.bump("#kp", @zavdiaky-0.4);
""")


# ---------------------------------------------------------------- 3 OVER: the internal browser
L.append(
    '<div class="g full" id="bd1"><div class="sheet board-bg hide" id="bd1S" style="height:930px">'
    '<div class="hand hide" id="b1T" style="position:absolute;left:110px;top:50px;font-size:80px">внутрішній браузер</div>'
    + sk.svg(1080, 930, sk.underline(112, 160, 640, stroke="blue"), sid="b1U")
    + sk.svg(1080, 930,
             sk.rect(150, 230, 540, 360, sw=5) +
             sk.line([(150, 300), (690, 300)], sw=4, double=False) +
             sk.ellipse(195, 265, 13, 13, stroke="red", fill="red", style="solid") +
             sk.ellipse(235, 265, 13, 13, stroke="yellow", fill="yellow", style="solid") +
             sk.ellipse(275, 265, 13, 13, stroke="green", fill="green", style="solid") +
             sk.rect(320, 247, 330, 38, sw=3, round_=True) +
             sk.line([(200, 370), (420, 366), (620, 372)], stroke="#9aa0a6", sw=6, double=False) +
             sk.line([(200, 430), (380, 434), (560, 428)], stroke="#9aa0a6", sw=6, double=False) +
             sk.line([(200, 490), (460, 486), (640, 492)], stroke="#9aa0a6", sw=6, double=False),
             sid="b1B")
    + '<div class="hand hide" id="b1Eq" style="position:absolute;left:712px;top:345px;font-size:96px">=</div>'
    '<div class="pill hide" id="b1Ch" style="left:790px;top:355px;height:96px;padding:0 34px;font-size:42px;font-weight:700">Chrome</div>'
    '<div class="hand hide" id="b1Zv" style="position:absolute;left:770px;top:475px;font-size:44px;color:#5f6368">звичайний</div>'
    + sk.svg(1080, 930, sk.rect(110, 200, 620, 520, stroke="blue", sw=7), sid="b1K") +
    '<div class="pill hide" id="b1KP" style="left:130px;top:625px;height:72px;padding:0 28px 0 18px;font-size:34px;font-weight:700;box-shadow:var(--e1)">'
    '<span style="display:inline-block;width:34px;height:34px;border-radius:50%;background:#D97757"></span>Клод</div>'
    + sk.svg(1080, 930,
             sk.arrow([(160, 810), (420, 790), (720, 800)], stroke="blue", sw=6) +
             sk.line([(130, 765), (230, 763)], stroke="blue", sw=4, double=False) +
             sk.line([(110, 850), (210, 848)], stroke="blue", sw=4, double=False) +
             sk.spark(760, 780, 30, stroke="yellow", sw=7), sid="b1F") +
    '<div class="hand hide" id="b1Sh" style="position:absolute;left:800px;top:760px;font-size:64px;color:#4285F4">швидше</div>'
    '</div></div>')


@beat
def b_board1():
    sfx("whoosh-short", "@zavdiaky-0.1")
    sfx("pencil", "@vnutrishnomu", -2)
    sfx("pop", "@khrom")
    sfx("pencil", "@vseredyni", -2)
    sfx("pop", "@kloda2")
    sfx("whoosh-short", "@shvydshe+0.25")
    return js("""
  tl.to("#kp", {scale: 1.3, duration: 0.3, ease: "power2.in"}, @zavdiaky-0.15);
  h.show("#bd1", @zavdiaky-0.15);
  h.sheetIn("#bd1S", @zavdiaky-0.15, 930);
  tl.set("#dc", {autoAlpha: 0}, @zavdiaky+0.8);
  h.write("#b1T", @vnutrishnomu-0.1, 0.8);
  h.draw("#b1U", @vnutrishnomu+0.6, 0.35);
  h.draw("#b1B", @vnutrishnomu+0.8, 1.6);
  h.write("#b1Eq", @khrom-0.15, 0.25);
  h.pop("#b1Ch", @khrom, {s: 0.5, r: 5});
  h.write("#b1Zv", @zvychainyi, 0.5);
  h.draw("#b1K", @vseredyni-0.1, 0.7);
  h.pop("#b1KP", @kloda2-0.05, {s: 0.5, r: -4});
  h.draw("#b1F", @oriientuietsia, 0.6);
  h.write("#b1Sh", @shvydshe-0.1, 0.4);
  /* the board rolls up, the browser mockup drops in under it */
  tl.to("#bd1S", {y: -970, duration: 0.5, ease: "power3.in"}, @shvydshe+0.25);
  tl.set("#bd1", {autoAlpha: 0}, @shvydshe+0.8);
""")


# ---------------------------------------------------------------- 4 NEAR the browser card in Instagram
ROWY = [130, 225, 320]
rows = ""
for i, (y, c, n) in enumerate(zip(ROWY, ["#4285F4", "#34A853", "#FBBC04"], [u"О", u"М", u"А"])):
    rows += ('<div class="ab hide" id="p%d" data-layout-allow-overlap style="left:30px;top:%dpx;width:480px;height:80px">'
             '<div class="av" style="left:0;top:8px;background:%s">%s</div>'
             '<div class="gl" style="left:86px;top:18px;width:220px"></div>'
             '<div class="gl" style="left:86px;top:48px;width:320px;height:14px;opacity:.7"></div></div>'
             '<div class="bub me hide" id="m%d" style="left:470px;top:%dpx;padding:14px 24px;font-size:28px">Привіт! Бачу, що ти…</div>'
             % (i, y, c, n, i, y + 4))
L.append(
    '<div class="g" id="br" style="top:0;height:700px">'
    '<div class="sheet hide" id="brS" style="height:700px;background:#f1f3f4">'
    '<div class="gcard" id="brC" style="left:100px;top:90px;width:880px;height:580px;overflow:hidden">'
    '<div style="position:absolute;left:0;right:0;top:0;height:96px;background:#f1f3f4"></div>'
    '<div style="position:absolute;left:30px;top:36px;width:22px;height:22px;border-radius:50%;background:#EA4335"></div>'
    '<div style="position:absolute;left:62px;top:36px;width:22px;height:22px;border-radius:50%;background:#FBBC04"></div>'
    '<div style="position:absolute;left:94px;top:36px;width:22px;height:22px;border-radius:50%;background:#34A853"></div>'
    '<div class="pill" style="left:150px;top:20px;width:690px;height:56px;padding:0 26px;font-size:30px;box-shadow:none">'
    '<span id="brU" data-text="instagram.com/direct" style="color:#3c4043"></span></div>'
    '<div id="brIn">' + rows +
    '<div class="pill hide" id="pr" style="left:30px;top:452px;width:820px;height:96px;padding:0 26px;font-size:32px;box-shadow:var(--e1)">'
    '<span class="chip on" style="height:56px;font-size:28px;padding:0 20px">Клод</span>'
    '<span id="prT" data-text="Розішли повідомлення лідам" style="color:#202124"></span></div>'
    + sk.svg(880, 580, sk.check(780, 470, 52, sw=9), sid="prOK")
    + sk.svg(880, 580, sk.check(820, 140, 40, sw=7) + sk.check(820, 235, 40, sw=7) + sk.check(820, 330, 40, sw=7),
             sid="sent") +
    '</div>'
    # ---- the catch: Instagram does not like it
    '<div class="hide" id="warn" data-layout-allow-overlap style="position:absolute;left:30px;top:116px;width:820px;height:110px;border-radius:20px;'
    'background:#ffdad6;border:3px solid #EA4335;display:flex;align-items:center;gap:20px;padding:0 30px;box-sizing:border-box">'
    '<span class="gs" style="font-size:56px;font-weight:700;color:#EA4335">!</span>'
    '<span class="gs" style="font-size:36px;font-weight:700;color:#410002">Підозріла активність</span></div>'
    '<div class="hand hide" id="botT" style="position:absolute;left:560px;top:360px;font-size:64px;color:#EA4335">бот?</div>'
    + sk.svg(880, 580, sk.circle_around(640, 400, 120, 66, stroke="red", sw=7), sid="botO") +
    '<div class="hide" id="stamp" style="position:absolute;left:120px;top:260px;width:380px;height:170px;border:10px solid #EA4335;'
    'border-radius:20px;display:grid;place-items:center;background:rgba(255,255,255,.85)">'
    '<span class="gs" style="font-size:110px;font-weight:700;color:#EA4335;letter-spacing:.08em">БАН</span></div>'
    '</div>'
    '<div class="ab" id="curW" style="left:0;top:0">' + CURSOR + '</div>'
    # the sticky note the card folds into
    '<div class="paper hide" id="nt" style="left:350px;top:180px;width:380px;height:330px;background:#fff7d1">'
    '<div class="num" data-layout-allow-overlap style="position:absolute;left:0;right:0;top:20px;text-align:center;font-size:170px;line-height:1">2</div>'
    '<div class="hand" data-layout-allow-overlap style="position:absolute;left:0;right:0;top:245px;text-align:center;font-size:56px">речі</div>'
    + sk.svg(380, 330, sk.circle_around(190, 140, 100, 90, stroke="blue", sw=7), sid="ntS") +
    '</div></div></div>')


@beat
def b_browser():
    sfx("pop", "@vidkryvaiesh")
    sfx("pop", "@prosysh")
    sfx("typing", "@rozislaty-0.1", -6)
    sfx("click-soft", "@shukaty")
    sfx("ping", "@pysaty2", -3)
    sfx("notification", "@vidpravliaty")
    return js("""
  h.show("#br", @vidkryvaiesh-0.15);
  h.sheetIn("#brS", @vidkryvaiesh-0.15, 700);
  tl.set("#curW", {autoAlpha: 0}, 0);
  h.type("#brU", @instahrami-0.3, 20);
  h.pop("#pr", @prosysh-0.1, {s: 0.8, r: 0, y: 20});
  h.type("#prT", @rozislaty-0.05, 24);
  h.draw("#prOK", @vse, 0.3);
  tl.fromTo("#curW", {autoAlpha: 0, x: 700, y: 550}, {autoAlpha: 1, x: 640, y: 500, duration: 0.3, immediateRender: false}, @khodyty-0.2);
  tl.to("#curW", {x: 420, y: 310, duration: 0.6, ease: "power2.inOut"}, @khodyty+0.15);
  h.pop("#p0", @shukaty-0.15, {s: 0.8, r: 0, y: 12});
  h.pop("#p1", @shukaty+0.05, {s: 0.8, r: 0, y: 12});
  h.pop("#p2", @shukaty+0.25, {s: 0.8, r: 0, y: 12});
  tl.to("#curW", {x: 300, y: 260, duration: 0.35, ease: "power2.inOut"}, @shukaty);
  tl.to("#curW", {x: 300, y: 450, duration: 0.45, ease: "power2.inOut"}, @shukaty+0.4);
  h.pop("#m0", @pysaty2-0.1, {s: 0.5, r: 2});
  h.pop("#m1", @pysaty2+0.1, {s: 0.5, r: -2});
  h.pop("#m2", @pysaty2+0.3, {s: 0.5, r: 2});
  tl.to("#curW", {x: 760, y: 470, duration: 0.4, ease: "power2.inOut"}, @pysaty2);
  h.draw("#sent", @vidpravliaty, 0.5);
""")


@beat
def b_catch():
    sfx("notification", "@instahramu", -2)
    sfx("pencil", "@nesanktsionovana", -3)
    sfx("click", "@shaptsi-0.1")
    sfx("whoosh-short", "@dvi-0.2")
    sfx("pop", "@dvi")
    return js("""
  tl.to("#brIn", {autoAlpha: 0.25, duration: 0.3}, @niuans);
  tl.to("#prT", {autoAlpha: 0, duration: 0.2}, @niuans);
  tl.to("#p0, #m0", {autoAlpha: 0, duration: 0.15}, @instahramu-0.2);
  h.pop("#warn", @instahramu-0.05, {s: 0.8, r: 0, y: -20});
  h.wiggle("#brC", @podobaietsia);
  tl.to("#curW", {x: 590, y: 410, duration: 0.4, ease: "power2.inOut"}, @nesanktsionovana-0.4);
  h.draw("#botO", @nesanktsionovana, 0.5);
  h.write("#botT", @botiv-0.3, 0.45);
  tl.fromTo("#stamp", {autoAlpha: 0, scale: 2.2, rotation: -14}, {autoAlpha: 1, scale: 1, rotation: -8, duration: 0.3, ease: "power3.in", immediateRender: false}, @shaptsi-0.4);
  h.wiggle("#brC", @shaptsi-0.05);
  /* -> folds into the note «2 речі» */
  tl.to("#brC", {scale: 0.4, autoAlpha: 0, duration: 0.4, ease: "power3.in"}, @dvi-0.3);
  tl.to("#curW", {autoAlpha: 0, duration: 0.2}, @dvi-0.3);
  h.pop("#nt", @dvi-0.05, {s: 0.4, r: -12, to: -3});
  h.draw("#ntS", @propysuiu, 0.5);
""")


# ---------------------------------------------------------------- 5 OVER: the two rules
OFF = 1000       # section 2 sits this far below section 1 on the camera layer
DX = [170, 420, 670, 920]
tline = sk.line([(120, 330), (970, 330)], sw=5)
dots = "".join(sk.ellipse(x, 330, 32, 32, stroke="blue", fill="blue", style="solid") for x in DX)
L.append(
    '<div class="g full" id="bd2"><div class="sheet board-bg hide" id="bd2S" style="height:930px">'
    '<div id="cam" style="position:absolute;left:0;top:0;width:1080px;height:2000px">'
    # ---- 1 pause
    '<div class="num hide" id="n1" style="position:absolute;left:110px;top:20px;font-size:150px;color:#4285F4">1</div>'
    '<div class="hand hide" id="n1T" style="position:absolute;left:230px;top:60px;font-size:96px">пауза</div>'
    + sk.svg(1080, 2000, tline, sid="tl1") + sk.svg(1080, 2000, dots, sid="tlD") +
    "".join('<div class="hand hide d%d" id="dL%d" style="position:absolute;left:%dpx;top:375px;width:120px;'
            'text-align:center;font-size:44px">дія</div>' % (i, i, x - 60) for i, x in enumerate(DX)) +
    "".join('<div class="hand hide" id="gL%d" style="position:absolute;left:%dpx;top:225px;width:200px;'
            'text-align:center;font-size:44px;color:#EA4335">30-40 с</div>' % (i, (a + b) // 2 - 100)
            for i, (a, b) in enumerate(zip(DX, DX[1:]))) +
    sk.svg(1080, 2000, "".join(sk.arrow([(a + 40, 290), ((a + b) / 2, 278), (b - 40, 290)], stroke="red", sw=4,
                                        head=18, both=True) for a, b in zip(DX, DX[1:])), sid="gA") +
    '<div class="hand hide" id="nb" style="position:absolute;left:130px;top:480px;font-size:58px;color:#34A853">не бот</div>'
    + sk.svg(1080, 2000, sk.check(340, 476, 64, sw=9), sid="nbC")
    + sk.svg(1080, 2000,
             sk.ellipse(800, 520, 78, 78, sw=5) +
             sk.line([(800, 520), (800, 468)], sw=6, double=False) +
             sk.line([(800, 520), (840, 541)], sw=6, double=False), sid="clk") +
    '<div class="hand hide" id="clkT" style="position:absolute;left:660px;top:605px;width:280px;text-align:center;'
    'font-size:44px">більше часу</div>'
    + sk.svg(1080, 2000, sk.rect(110, 690, 400, 160, stroke="green", sw=5), sid="oA")
    + sk.svg(1080, 2000, sk.rect(570, 690, 400, 160, stroke="red", sw=5), sid="oB") +
    '<div class="hand hide" id="oAT" style="position:absolute;left:110px;top:730px;width:400px;text-align:center;font-size:66px">довше</div>'
    '<div class="hand hide" id="oBT" style="position:absolute;left:570px;top:710px;width:400px;text-align:center;font-size:52px">заблокували<br>акаунт</div>'
    + sk.svg(1080, 2000, sk.circle_around(310, 770, 225, 100, stroke="green", sw=7), sid="oAO")
    + sk.svg(1080, 2000, sk.cross(700, 705, 130, sw=11), sid="oBX")
    # ---- 2 personalisation
    + ('<div class="num hide" id="n2" style="position:absolute;left:110px;top:%dpx;font-size:150px;color:#34A853">2</div>'
       '<div class="hand hide" id="n2T" style="position:absolute;left:230px;top:%dpx;font-size:88px">персоналізація</div>'
       % (OFF + 20, OFF + 60))
    + sk.svg(1080, 2000, sk.underline(232, OFF + 180, 600, stroke="green", twice=True), sid="n2U")
    + ('<div class="bub me hide" id="q1" style="left:110px;top:%dpx;font-size:40px">Привіт, '
       '<span style="background:#ffec99;padding:0 6px;border-radius:6px">Олено</span>!</div>' % (OFF + 235))
    + ('<div class="hand hide" id="q1T" style="position:absolute;left:560px;top:%dpx;font-size:50px;color:#EA4335">лише ім\'я</div>'
       % (OFF + 245))
    + sk.svg(1080, 2000, sk.arrow([(300, OFF + 335), (290, OFF + 365), (300, OFF + 400)], stroke="ink", sw=5, head=22),
             sid="q12")
    + ('<div class="bub me hide" id="q2" style="left:110px;top:%dpx;width:560px;font-size:34px;max-width:600px">'
       'Олено, бачу, що ти <span id="q2M" style="padding:0 6px;border-radius:6px">робиш букети на весілля</span>. '
       'Хочу запропонувати…</div>' % (OFF + 410))
    + ('<div class="hand hide" id="q2T" style="position:absolute;left:770px;top:%dpx;font-size:44px;color:#34A853">усе<br>повідомлення</div>'
       % (OFF + 420))
    + ('<div class="pill hide" id="k2" style="left:110px;top:%dpx;height:84px;padding:0 32px 0 22px;font-size:38px;font-weight:700">'
       '<span style="display:inline-block;width:40px;height:40px;border-radius:50%%;background:#D97757"></span>Клод</div>'
       % (OFF + 625))
    + sk.svg(1080, 2000, sk.arrow([(330, OFF + 667), (450, OFF + 650), (575, OFF + 690)], stroke="blue", sw=5), sid="k2A")
    + ('<div class="gcard hide" id="pf" style="left:590px;top:%dpx;width:380px;height:260px">'
       '<div class="av" style="left:30px;top:26px;width:84px;height:84px;font-size:38px;background:#EA4335">О</div>'
       '<div class="gs" style="position:absolute;left:134px;top:36px;font-size:36px;font-weight:700">Олена</div>'
       '<div class="gs" style="position:absolute;left:134px;top:80px;font-size:24px;color:#5f6368">профіль</div>'
       '<div class="gs" style="position:absolute;left:30px;top:136px;width:320px;font-size:30px;line-height:1.3;color:#3c4043">'
       '<span id="pfM" style="padding:0 4px;border-radius:6px">Флористка · весільні букети</span></div></div>' % (OFF + 615))
    + sk.svg(1080, 2000, sk.arrow([(800, OFF + 610), (770, OFF + 575), (690, OFF + 560)], stroke="green", sw=6), sid="pfA")
    + sk.svg(1080, 2000,
             sk.rect(110, OFF + 740, 220, 130, sw=4.5) +
             sk.line([(135, OFF + 780), (300, OFF + 776)], stroke="#9aa0a6", sw=5, double=False) +
             sk.line([(135, OFF + 810), (280, OFF + 814)], stroke="#9aa0a6", sw=5, double=False) +
             sk.line([(135, OFF + 840), (305, OFF + 836)], stroke="#9aa0a6", sw=5, double=False), sid="doc")
    + ('<div class="hand hide" id="docT" style="position:absolute;left:345px;top:%dpx;font-size:46px">мій скрипт</div>'
       % (OFF + 780))
    + '</div></div></div>')


@beat
def b_board2():
    sfx("whoosh-short", "@stalos-0.2")
    sfx("pencil", "@pauza-0.2", -3)
    sfx("click-soft", "@mizh")
    sfx("ping", "@bota-0.1", -3)
    sfx("pop", "@dovshe")
    sfx("pencil", "@obyraiemo", -2)
    sfx("whoosh-short", "@druhe-0.1")
    sfx("pop", "@prosto-0.1")
    sfx("click-soft", "@profil")
    sfx("pencil", "@vpysaty", -3)
    sfx("whoosh-short", "@skryptom+0.4", -3)
    return js("""
  h.bump("#nt", @stalos-0.45);
  h.show("#bd2", @stalos-0.25);
  h.sheetIn("#bd2S", @stalos-0.25, 930);
  tl.set("#br", {autoAlpha: 0}, @stalos+0.75);
  h.pop("#n1", @pershe, {s: 0.4, r: -6});
  h.write("#n1T", @pauza-0.1, 0.5);
  h.draw("#tl1", @minimum-0.3, 0.5);
  h.draw("#tlD", @minimum+0.1, 0.5);
  h.draw("#gA", @n3040-0.1, 0.6);
  h.write("#gL0", @n3040, 0.3);
  h.write("#gL1", @n3040+0.2, 0.3);
  h.write("#gL2", @n3040+0.4, 0.3);
  h.write("#dL0", @mizh, 0.25);
  h.write("#dL1", @mizh+0.35, 0.25);
  h.write("#dL2", @mizh+0.7, 0.25);
  h.write("#dL3", @mizh+1.05, 0.25);
  h.write("#nb", @vyhliadalo, 0.45);
  h.draw("#nbC", @bota-0.1, 0.3);
  h.draw("#clk", @zaimaie-0.1, 0.6);
  h.write("#clkT", @chasu-0.3, 0.5);
  h.draw("#oA", @dovshe-0.2, 0.4);
  h.write("#oAT", @dovshe, 0.4);
  h.draw("#oB", @zablokuvaly-0.2, 0.4);
  h.write("#oBT", @zablokuvaly, 0.6);
  h.draw("#oAO", @obyraiemo, 0.5);
  h.draw("#oBX", @dovshe2, 0.3);
  /* pan down to rule 2 */
  tl.fromTo("#cam", {y: 0}, {y: -%(OFF)d, duration: 0.8, ease: "power3.inOut", immediateRender: false}, @druhe-0.15);
  h.pop("#n2", @druhe+0.35, {s: 0.4, r: 6});
  h.write("#n2T", @personalizatsiia-0.1, 0.7);
  h.draw("#n2U", @hlybsha, 0.4);
  h.pop("#q1", @prosto-0.1, {s: 0.5, r: -3});
  h.write("#q1T", @imia, 0.4);
  h.draw("#q12", @same-0.15, 0.3);
  h.pop("#q2", @same, {s: 0.6, r: 2});
  h.write("#q2T", @povidomlennia7-0.2, 0.5);
  h.pop("#k2", @klod7-0.05, {s: 0.5, r: -5});
  h.draw("#k2A", @zaity, 0.35);
  h.pop("#pf", @profil-0.05, {s: 0.6, r: 3});
  tl.to("#pfM", {backgroundColor: "#ffec99", duration: 0.3}, @zaimaietsia-0.1);
  h.draw("#pfA", @vpysaty, 0.4);
  tl.to("#q2M", {backgroundColor: "#ffec99", duration: 0.3}, @vpysaty+0.35);
  h.bump("#q2", @tekst);
  h.draw("#doc", @moim-0.3, 0.5);
  h.write("#docT", @moim, 0.45);
  h.bump("#doc", @skryptom);
  /* the board rolls up, the Direct mockup drops back in */
  tl.to("#bd2S", {y: -970, duration: 0.5, ease: "power3.in"}, @skryptom+0.4);
  tl.set("#bd2", {autoAlpha: 0}, @skryptom+0.95);
""".replace("%(OFF)d", str(OFF)))


# ---------------------------------------------------------------- 6 the Direct mockup again, then the CTA in the same sheet
L.append(
    '<div class="g" id="fn" style="top:0;height:700px">'
    '<div class="sheet hide" id="fnS" style="height:700px;background:#f1f3f4">'
    '<div class="gcard" id="fnC" style="left:100px;top:90px;width:880px;height:560px">' + header("Instagram", "Direct") +
    '<div class="num" id="fnN" style="position:absolute;left:44px;top:140px;font-size:170px;color:#4285F4">0</div>'
    '<div class="hand hide" id="fnT" style="position:absolute;left:52px;top:330px;font-size:54px">повідомлень</div>'
    '<div class="ab" style="left:44px;top:440px"><span class="chip cg hide" id="fnCh" style="height:84px;font-size:38px">'
    'без жодної проблеми</span></div>'
    + sk.svg(880, 560, sk.check(640, 170, 140, sw=13), sid="fnOK")
    + sk.svg(880, 560, sk.spark(710, 160, 40, stroke="yellow", sw=8), sid="fnSp") +
    '</div>'
    # ---- CTA
    '<div class="btn hide" id="fb" style="left:240px;top:280px;width:600px;height:150px;background:#4285F4;color:#fff;font-size:56px">'
    '<span id="fbA">Підписатися</span></div>'
    '<div class="btn hide" id="fb2" style="left:240px;top:280px;width:600px;height:150px;background:#e8eaed;color:#202124;font-size:52px">'
    'Ви підписані</div>'
    + sk.svg(1080, 700, sk.arrow([(130, 150), (160, 280), (225, 340)], stroke="ink", sw=7), sid="fbA2")
    + sk.svg(1080, 700, sk.spark(840, 280, 36, stroke="yellow", sw=8), sid="fbS") +
    '<div class="ab" id="cur2" style="left:0;top:0">' + CURSOR + '</div>'
    '</div></div>')


@beat
def b_fn():
    sfx("whoosh-short", "@tomu8-0.1", -4)
    sfx("click-soft", "@n150b")
    sfx("pencil", "@bez", -3)
    sfx("sparkle", "@korystuius", -3)
    return js("""
  h.show("#fn", @skryptom+0.5);
  h.sheetIn("#fnS", @skryptom+0.5, 700);
  tl.set("#fnN", {autoAlpha: 0}, 0);
  h.show("#fnN", @n150b-0.3);
  h.count("#fnN", @n150b-0.3, 150, 0.8, function (v) { return Math.round(v) + (v > 149.5 ? "+" : ""); });
  h.write("#fnT", @n150b+0.6, 0.5);
  h.draw("#fnOK", @bez, 0.4);
  h.pop("#fnCh", @bez+0.3, {s: 0.5, r: 4});
  h.draw("#fnSp", @korystuius, 0.3);
  h.bump("#fnOK", @korystuius);
  tl.to("#fnC", {y: -30, autoAlpha: 0, duration: 0.3, ease: "power2.in"}, @yakshcho-0.35);
""")


@beat
def b_cta():
    sfx("pop", "@yakshcho")
    sfx("click", "@pidpyshys")
    return js("""
  tl.set("#cur2", {autoAlpha: 0}, 0);
  h.pop("#fb", @yakshcho, {s: 0.5, r: -3});
  h.draw("#fbA2", @korysno-0.2, 0.5);
  tl.fromTo("#cur2", {autoAlpha: 0, x: 900, y: 620}, {autoAlpha: 1, x: 620, y: 370, duration: 0.7, ease: "power2.out", immediateRender: false}, @pidpyshys-0.9);
  tl.to("#cur2", {scale: 0.85, duration: 0.08}, @pidpyshys-0.05);
  tl.to("#cur2", {scale: 1, duration: 0.15}, @pidpyshys+0.05);
  h.show("#fb2", @pidpyshys);
  h.fadeOut("#fb", @pidpyshys, 0.05);
  h.bump("#fb2", @pidpyshys);
  h.draw("#fbS", @pidpyshys+0.1, 0.3);
""")


BLACKOUT = [
    (T["n150"], T["povidomlen"] + 0.6, ""),                       # «150 повідомлень» on the card
    (T["pysaty"], T["metod"] - 0.5, ""),                          # the three task rows say it
    (T["menedzher"], T["menedzher"] + 0.4, ""),
    (T["vtomliuietsia"], T["bezkoshtovno"] + 0.5, ""),            # the two chips
    (T["vnutrishnomu"], T["kloda1"] - 0.05, ""),                   # «внутрішній браузер» written
    (T["khrom"], T["khrom"] + 0.3, ""),
    (T["shvydshe"], T["shvydshe"] + 0.3, ""),
    (T["rozislaty"], T["rozislaty"] + 1.0, ""),                   # the prompt types it
    (T["pershe"], T["minimum"] - 0.05, ""),                       # «1 пауза»
    (T["n3040"], T["n3040"] + 0.5, ""),
    (T["dovshe"], T["zablokuvaly"] + 0.9, ""),                    # the two boxes
    (T["druhe"], T["personalizatsiia"] + 0.5, ""),                # «2 персоналізація»
    (T["bilshe8"], T["n150b"] + 1.1, ""),                         # «150+ повідомлень»
    (T["bez"], T["problemy"] + 0.5, ""),                          # chip «без жодної проблеми»
]
INVERT = []    # halfscreen keeps her (and the white captions) in the bottom half (STYLE.md §0c)


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
        title=u"Reel 58 — автоматизація без бану",
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
