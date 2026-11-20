# -*- coding: utf-8 -*-
"""Reel 63 — «Які автоматизації зробити викладачці мови?». Posts 2026-11-22.

Google x Excalidraw (STYLE.md §0b), layouts per §0c: every graphic lives on a
sheet that drops from the top and pushes her plate down — mockups on a white
move-down sheet, schemes on a halfscreen whiteboard sheet. Same series as reel
43 (tutor automations); the carried object here is a FLASHCARD.

Cut from her raw take by tools/cut.py + cut-fix (drops the false start «Клод
пише!»). No closeups: no_paint is empty.

Chain:  s1 (sketch sheet): chips «китайська»/«англійська», a deck of four index
cards fans out, the Claude pill -> the top card grows into the Claude app
mockup: «Картки з нових слів», the Quizlet connector toggles on, a words field
types, chip «транскрипт уроку», dots, a set of three cards fans out, «Учень»
opens it and the top card flips apple -> яблуко -> s2 HALFSCREEN wipes out of
that card: «Щоденник помилок» — Fathom -> транскрипт -> Claude + скіл ->
помилки -> вправи -> Notion -> картка учня; closes onto the student card ->
s3 (mockup): «Перевірка домашок», «Claude перевіряє сам» scribbled out, the
student list with status chips, a search pill crossed out, a green tick ->
s4 HALFSCREEN wipes out of the tick: «Тест на рівень» — Claude -> питання +
шкала, SendPulse flow «без коду» -> CRM card; a magnet «лідмагніт» +
«кваліфікація лідів», looped together; closes onto the CRM card -> s5 (mockup)
CTA: a post's action bar, bookmark fills, share row, «Колега» picked.

usage: python build.py   (then: python ../tools/sfx.py mix 63)
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

NN = "63"
CUT = json.load(io.open(os.path.join(ROOT, "work", "r" + NN, "cut.json"), encoding="utf-8"))
DUR = 66.117           # (1984 plate frames - 0.5) / 30
FPS = 30
k = Kit(width=1080, height=1920, fps=FPS, duration=DUR)
k.cap_font = "assets/fonts/ProductSans-Bold.ttf"
k.css(sketch_css())
sk = Sketch(seed=47)

NO_PAINT = [tuple(x) for x in CUT["no_paint"]]   # empty on this cut

CAPS = k.load_captions(os.path.join(ROOT, "work", "r" + NN, "captions.json"))


# ---- caption fixes: whisper errors -> the script word / what she said ------
def fix(caps):
    """by position. ('w', near, new) replaces; drop folds caps[i] into caps[i-1]."""
    def find(word, near):
        c = min((i for i, c in enumerate(caps) if c["w"] == word), key=lambda i: abs(caps[i]["s"] - near))
        assert abs(caps[c]["s"] - near) < 0.5, (word, near)
        return c
    edits = [
        (u"з клод", 4.26, u"з Клод"), (u"налаштувала", 5.32, u"налаштувала."),
        (u"По", 6.03, u"По-перше,"), (u"звичайна", 6.94, u"звичайні"), (u"картинка.", 7.48, u"картки"),
        (u"квісла.", 11.49, u"Quizlet:"), (u"сет,", 15.79, u"сет"), (u"впізлят.", 18.06, u"в Quizlet."),
        (u"урок,", 27.17, u"урок"), (u"а", 28.50, u"А"), (u"Notion", 29.69, u"Notion,"),
        (u"зробити", 42.41, u"зробити,"), (u"це", 45.13, u"Це"), (u"чотверте,", 46.38, u"четверте,"),
        (u"колодом", 49.60, u"Claude"), (u"шкалу,", 51.50, u"шкалу."),
        (u"в Сенпусі", 53.42, u"в SendPulse"), (u"коду,", 54.24, u"коду."),
        (u"Сьоромся", 57.31, u"CRM-систему."), (u"Це", 58.36, u"це"), (u"Збережи", 62.52, u"збережи"),
        (u"щоб не загубити,", 63.26, u"щоб не загубити"), (u"знайомій", 65.07, u"своїй"),
        (u"викладачці.", 65.47, u"колезі."), (u"б", 36.15, u"б,"), (u"ідей.", 63.88, u"ідей"),
    ]
    for w, near, new in edits:
        caps[find(w, near)]["w"] = new
    drop = [(u"Перше", 6.30), (u"таки", 7.72), (u"з", 57.53), (u"того.", 57.63)]
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
    "vykl": S(u"викладачкою", 0.79), "kyt": S(u"китайської", 1.41), "angl": S(u"англійської", 2.19),
    "avto": S(u"автоматизації", 3.50), "klod0": S(u"Клод", 4.26), "nalasht": S(u"налаштувала", 5.32),
    "pershe": S(u"По-перше", 6.03), "kartky": S(u"картки", 7.48), "urok1": S(u"уроку", 9.16),
    "claude1": S(u"Claude", 9.95), "konektor": S(u"конектор", 11.11), "quizlet": S(u"Quizlet", 11.49),
    "kydaiesh": S(u"кидаєш", 12.33), "spysok": S(u"список", 12.77), "transkr": S(u"транскрипт", 13.65),
    "otrym": S(u"отримуєш", 14.73), "hotovyi": S(u"готовий", 15.23), "uchen": S(u"учень", 16.70),
    "vidkryvaie": S(u"відкриває", 17.54), "druhe": S(u"Друге", 18.67), "shchod": S(u"щоденник", 19.46),
    "fathom": S(u"Fathom", 20.75), "zapysuie": S(u"записує", 21.23), "claude2": S(u"Claude", 21.98),
    "zabyraie": S(u"забирає", 22.90), "skil": S(u"скіл", 23.61), "vypysuie": S(u"виписує", 23.90),
    "skladaie": S(u"складає", 25.59), "nastupnyi": S(u"наступний", 26.59), "pidkl": S(u"підключиш", 29.07),
    "notion": S(u"Notion", 29.69), "lahty": S(u"лягти", 30.89), "kartku": S(u"картку", 31.59),
    "tretie": S(u"Третє", 32.43), "orh": S(u"організація", 33.24), "domashok": S(u"домашок", 34.36),
    "samu": S(u"Саму", 35.00), "ne_vidd": S(u"віддавала", 36.91), "klodu": S(u"Клоду", 37.99),
    "a_ot": S(u"от", 38.44), "orhanizovuvaty": S(u"організовувати", 39.52), "maks": S(u"максимально", 41.61),
    "vytrachala": S(u"витрачала", 43.66), "poshuk": S(u"пошук", 44.59), "tochno": S(u"точно", 45.40),
    "mozhna": S(u"можна", 45.66), "chetverte": S(u"четверте", 46.38), "test": S(u"тест", 47.18),
    "novykh": S(u"нових", 48.42), "claude3": S(u"Claude", 49.60), "pytannia": S(u"питання", 50.64),
    "shkalu": S(u"шкалу", 51.50), "lants": S(u"Ланцюжок", 51.96), "sendpulse": S(u"SendPulse", 53.42),
    "bez": S(u"без", 54.00), "rezult": S(u"результати", 55.18), "padaiut": S(u"падають", 56.22),
    "crm": S(u"CRM-систему", 57.31), "lidmagnit": S(u"лідмагніт", 58.82), "kvalif": S(u"кваліфікація", 59.38),
    "odnomu": S(u"одному", 60.70), "mistsi": S(u"місці", 61.18), "tomu": S(u"Тому", 61.83),
    "zberezhy": S(u"збережи", 62.52), "zahubyty": S(u"загубити", 63.26), "pereshly": S(u"перешли", 64.71),
    "svoii": S(u"своїй", 65.07), "kolezi": S(u"колезі", 65.47),
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
.av { position: absolute; width: 64px; height: 64px; border-radius: 50%; display: grid; place-items: center;
      font-family: "GSans", sans-serif; font-weight: 700; font-size: 30px; color: #fff; }
.lbl { font-family: "GSans", sans-serif; font-size: 26px; font-weight: 700; letter-spacing: .14em;
       color: #5f6368; text-transform: uppercase; position: absolute; }
.field { position: absolute; border-radius: 16px; border: 2px solid #747775; background: #fff; }
.field .fl { position: absolute; left: 22px; top: -20px; background: #fff; padding: 0 10px;
             font-family: "GSans", sans-serif; font-size: 28px; color: #0b57d0; font-weight: 500; }
.row { position: absolute; display: flex; align-items: center; gap: 26px; font-family: "GSans", sans-serif; }
.bpill { position: absolute; height: 96px; padding: 0 34px; font-size: 38px; font-weight: 700; }
.dot { display: inline-block; width: 30px; height: 30px; border-radius: 50%; }
.hd { position: absolute; left: 122px; top: 34px; font-size: 34px; font-weight: 700; }
.hs { position: absolute; left: 122px; top: 76px; font-size: 24px; color: #5f6368; }
.sep { position: absolute; left: 0; right: 0; top: 124px; height: 2px; background: #e8eaed; }
.idx { position: absolute; width: 300px; height: 190px; background: #fff; border-radius: 14px;
       box-shadow: 0 10px 24px rgba(0,0,0,.18), 0 2px 5px rgba(0,0,0,.12); }
.fc { position: absolute; width: 180px; height: 140px; background: #fff; border-radius: 16px;
      box-shadow: var(--e3); display: grid; place-items: center; font-family: "GSans", sans-serif;
      font-size: 31px; font-weight: 700; color: #202124; }
.fc .bk { position: absolute; inset: 0; display: grid; place-items: center; border-radius: 16px;
          background: #d3e3fd; color: #041e49; }
.st { position: absolute; left: 60px; width: 900px; height: 84px; display: flex; align-items: center; gap: 24px;
      border-bottom: 2px solid #e8eaed; font-family: "GSans", sans-serif; font-size: 38px; color: #202124; }
.st .av { position: relative; width: 58px; height: 58px; font-size: 26px; }
.st .nm { flex: 1; }
.st .chip { height: 60px; font-size: 28px; padding: 0 22px; }
.node { position: absolute; height: 74px; padding: 0 26px; border-radius: 18px; background: #fff;
        border: 3px solid #1e1e1e; display: flex; align-items: center; font-family: "GSans", sans-serif;
        font-size: 30px; font-weight: 500; color: #202124; }
.lv { display: inline-grid; place-items: center; width: 70px; height: 52px; border-radius: 12px;
      font-family: "GSans", sans-serif; font-size: 26px; font-weight: 700; color: #fff; }
""")

# =============================================================== s1: the deck -> the Claude app
CARDS = ['<div class="idx" id="dk%d" style="left:390px;top:300px">%s</div>' % (
    i + 1,
    sk.svg(300, 190, sk.line([(30, 70), (200, 68)], stroke="#9aa0a6", sw=4, double=False) +
           sk.line([(30, 110), (250, 112)], stroke="#9aa0a6", sw=4, double=False) +
           sk.line([(30, 150), (170, 148)], stroke="#9aa0a6", sw=4, double=False))
    if i < 3 else
    '<div class="hand" style="position:absolute;left:0;right:0;top:66px;text-align:center;font-size:44px">'
    u'автоматизації</div>' + sk.svg(300, 190, sk.underline(50, 132, 200, stroke="blue", sw=6), sid="dkU"))
    for i in range(4)]
L.append(
    '<div class="g full hide" id="g1">'
    '<div class="sheet board-bg hide" id="s1" style="height:720px">'
    '<div class="lbl hide" id="s1L" style="left:80px;top:60px">якби я була викладачкою</div>'
    '<div class="ab hide" id="c1" style="left:150px;top:130px"><span class="chip cr">китайська</span></div>'
    '<div class="ab hide" id="c2" style="left:560px;top:130px"><span class="chip on">англійська</span></div>'
    + "".join(CARDS) +
    '<div class="pill hide" id="cl0" style="left:390px;top:560px;height:90px;padding:0 34px;font-size:38px;font-weight:700">'
    '<span class="dot" style="background:#FBBC04"></span>з Claude</div>'
    # the Claude app (a mockup) that grows out of the top card
    '<div class="gcard hide" id="app" style="left:40px;top:40px;width:1000px;height:640px">'
    '<div class="av" style="left:36px;top:30px;background:#1e1e1e">C</div>'
    '<div class="gs hd">Claude</div><div class="gs hs">картки з нових слів уроку</div><div class="sep"></div>'
    '<div class="row hide" id="qz" style="left:36px;top:150px;width:928px;height:96px">'
    '<span class="chip cy" style="font-weight:700">Quizlet</span>'
    '<span class="gs" style="font-size:32px;color:#5f6368;flex:1">офіційний конектор</span></div>'
    '<div class="tgl hide" id="qzT" style="left:860px;top:166px"><b></b></div>'
    '<div class="field hide" id="wf" style="left:36px;top:280px;width:928px;height:96px"><span class="fl">Слова</span>'
    '<span class="gs" id="wfT" data-text="apple, homework, teacher, school" style="position:absolute;left:28px;top:24px;font-size:36px"></span></div>'
    '<div class="ab hide" id="trc" style="left:36px;top:410px"><span class="chip on">або транскрипт уроку</span></div>'
    '<div class="dots hide" id="ad" style="left:430px;top:450px"><i></i><i></i><i></i><i></i></div>'
    '<div class="fc hide" id="f3" style="left:800px;top:440px">teacher</div>'
    '<div class="fc hide" id="f2" style="left:620px;top:430px">homework</div>'
    '<div class="fc hide" id="f1" style="left:440px;top:420px"><span id="f1a">apple</span>'
    '<div class="bk hide" id="f1b">яблуко</div></div>'
    '<div class="av hide" id="stu" style="left:60px;top:520px;background:#34A853">У</div>'
    '<div class="hand hide" id="stuT" style="position:absolute;left:140px;top:526px;font-size:44px">учень</div>'
    + sk.svg(1000, 640, sk.arrow([(250, 560), (340, 560), (430, 520)], stroke="green", sw=5, head=24), sid="stuA") +
    '</div>'
    '</div></div>')


@beat
def b_s1():
    sfx("whoosh-short", 0.05)
    sfx("pop", "@kyt")
    sfx("pop", "@angl")
    sfx("pencil", "@avto", -3)
    sfx("pop", "@klod0")
    sfx("whoosh-short", "@pershe")
    sfx("click", "@quizlet")
    sfx("typing", "@kydaiesh", -4)
    sfx("pop", "@transkr")
    sfx("pop", "@hotovyi")
    sfx("click-soft", "@vidkryvaie")
    return js("""
  h.show("#g1", 0.0);
  h.sheetIn("#s1", 0.05, 720, 140);
  h.write("#s1L", 0.5, 0.5);
  h.pop("#c1", @kyt-0.05, {s: 0.5, r: -5});
  h.pop("#c2", @angl-0.05, {s: 0.5, r: 5});
  h.pop("#dk1", @avto-0.3, {s: 0.6, r: 0});
  h.pop("#dk2", @avto-0.25, {s: 0.6, r: 0});
  h.pop("#dk3", @avto-0.2, {s: 0.6, r: 0});
  h.pop("#dk4", @avto-0.15, {s: 0.6, r: 0});
  tl.to("#dk1", {x: -210, rotation: -12, duration: 0.6, ease: SP}, @avto+0.15);
  tl.to("#dk2", {x: -70, rotation: -4, duration: 0.6, ease: SP}, @avto+0.2);
  tl.to("#dk3", {x: 70, rotation: 4, duration: 0.6, ease: SP}, @avto+0.25);
  tl.to("#dk4", {x: 210, rotation: 12, duration: 0.6, ease: SP}, @avto+0.3);
  h.draw("#dkU", @avto+0.6, 0.4);
  h.pop("#cl0", @klod0-0.05, {s: 0.5, r: 3});
  /* the first card grows into the Claude app */
  h.fadeOut("#c1, #c2, #s1L, #cl0, #dk1, #dk2, #dk3", @pershe-0.1, 0.25);
  tl.to("#dk4", {x: 0, rotation: 0, scale: 2.2, autoAlpha: 0, duration: 0.4, ease: "power2.in"}, @pershe-0.1);
  h.pop("#app", @pershe+0.1, {s: 0.45, r: 0, y: 0});
  h.pop("#qz", @claude1, {s: 0.9, r: 0, y: 14});
  h.pop("#qzT", @konektor, {s: 0.5, r: 0, y: 0});
  h.toggle("#qzT", @quizlet, "#0b57d0");
  h.pop("#wf", @kydaiesh-0.15, {s: 0.95, r: 0, y: 14});
  h.type("#wfT", @kydaiesh+0.1, 24);
  h.pop("#trc", @transkr-0.05, {s: 0.5, r: -3});
  h.pop("#ad", @otrym-0.1, {s: 0.5, r: 0});
  h.think("#ad", @otrym, 0.6);
  h.out("#ad", @hotovyi-0.1, 0.15);
  h.pop("#f3", @hotovyi, {s: 0.4, r: 10, to: 6});
  h.pop("#f2", @hotovyi+0.12, {s: 0.4, r: 6, to: 2});
  h.pop("#f1", @hotovyi+0.24, {s: 0.4, r: -6, to: -3});
  h.pop("#stu", @uchen-0.05, {s: 0.4, r: 0});
  h.write("#stuT", @uchen+0.1, 0.35);
  h.draw("#stuA", @uchen+0.3, 0.4);
  tl.to("#f1", {scaleX: 0, duration: 0.14, ease: "power2.in"}, @vidkryvaie);
  tl.set("#f1a", {autoAlpha: 0}, @vidkryvaie+0.14);
  tl.set("#f1b", {autoAlpha: 1}, @vidkryvaie+0.14);
  tl.to("#f1", {scaleX: 1, duration: 0.3, ease: SP}, @vidkryvaie+0.14);
""")


# =============================================================== s3: homework (mockup, under s2)
STU = [(u"Оля", "#4285F4", "cg", u"здано"), (u"Марк", "#EA4335", "cr", u"не здано"),
       (u"Софія", "#34A853", "cy", u"чекає"), (u"Денис", "#FBBC04", "cg", u"здано")]
rows = "".join(
    '<div class="st hide" id="st%d" style="top:%dpx"><span class="av" style="background:%s">%s</span>'
    '<span class="nm">%s</span><span class="chip %s hide" id="sc%d">%s</span></div>'
    % (i + 1, 300 + 92 * i, c, n[0], n, cc, i + 1, lab) for i, (n, c, cc, lab) in enumerate(STU))
L.append(
    '<div class="g full hide" id="g3">'
    '<div class="sheet hide" id="s3" style="height:760px;background:#fff">'
    '<div class="lbl" style="left:60px;top:56px">третє</div>'
    '<div class="gs hide" id="s3T" style="position:absolute;left:60px;top:92px;font-size:62px;font-weight:700">Перевірка домашок</div>'
    '<div class="pill hide" id="clx" style="left:60px;top:190px;height:86px;padding:0 32px;font-size:34px;font-weight:700">'
    '<span class="dot" style="background:#FBBC04"></span>Claude перевіряє сам</div>'
    + sk.svg(1080, 760, sk.scribble(70, 210, 440, 46, sw=8), sid="clxS") +
    rows +
    '<div class="pill hide" id="srch" style="left:460px;top:190px;width:540px;height:86px;padding:0 30px;font-size:32px">'
    '<span style="color:#5f6368">Пошук:</span><span id="srT" data-text="де домашка Марка?"></span></div>'
    + sk.svg(1080, 760, sk.cross(680, 178, 110, sw=10), sid="srX")
    + sk.svg(1080, 760, sk.circle_around(300, 434, 270, 50, stroke="red", sw=6), sid="mkO")
    + sk.svg(1080, 760, sk.check(860, 60, 110, sw=12), sid="okC") +
    '<div class="hand hide" id="okT" style="position:absolute;left:820px;top:640px;font-size:54px;color:#34A853">можна!</div>'
    '</div></div>')

# =============================================================== s5: CTA (mockup, under s4)
ICONS = (
    sk._p("M150 92 C 130 62, 92 78, 100 108 C 106 128, 150 156, 150 156 C 150 156, 194 128, 200 108 C 208 78, 170 62, 150 92", "#1e1e1e", 6) +
    sk._p("M300 120 C 300 88, 324 70, 350 70 C 378 70, 400 90, 400 116 C 400 144, 376 162, 350 162 C 340 162, 330 160, 322 156 L 298 164 L 306 142 C 302 136, 300 128, 300 120", "#1e1e1e", 6) +
    sk._p("M460 76 L 560 76 L 500 160 L 492 110 L 460 76 M 492 110 L 560 76", "#1e1e1e", 6)
)
L.append(
    '<div class="g full hide" id="g5">'
    '<div class="sheet hide" id="s5" style="height:640px;background:#fff">'
    '<div class="gcard flat" style="left:110px;top:60px;width:860px;height:520px">'
    '<div class="av" style="left:30px;top:26px;background:#EA4335">R</div>'
    '<div class="gs hd" style="left:112px;top:40px">reel</div>'
    '<div class="ab" style="left:30px;top:110px;width:800px;height:220px;border-radius:18px;background:#f1f3f4"></div>'
    '<div class="hand" style="position:absolute;left:60px;top:160px;font-size:52px">автоматизації</div>'
    '<div class="hand" style="position:absolute;left:60px;top:226px;font-size:52px">для викладачки мови</div>'
    + sk.svg(860, 520, '<g transform="translate(-60,270)">' + ICONS + '</g>', sid="icons") +
    '<svg class="sk" viewBox="0 0 860 520" width="860" height="520"><path id="bmF" d="M745 345 L 805 345 L 805 435 L 775 410 L 745 435 Z" '
    'fill="#1e1e1e" opacity="0"/></svg>'
    + sk.svg(860, 520, sk._p("M745 345 L 805 345 L 805 435 L 775 410 L 745 435 Z", "#1e1e1e", 6), sid="bm") +
    '<div class="hand hide" id="bmT" style="position:absolute;left:690px;top:450px;font-size:38px">зберегти</div>'
    '<div class="hand hide" id="shT" style="position:absolute;left:370px;top:450px;font-size:38px">переслати</div>'
    '</div>'
    '<div class="pill hide" id="share" style="left:250px;top:200px;height:110px;padding:0 20px 0 18px;font-size:36px;font-weight:700">'
    '<span class="av" style="position:relative;background:#34A853">К</span>Колега'
    '<span class="chip on" style="height:64px;font-size:30px">Надіслати</span></div>'
    '</div></div>')


# =============================================================== s2: HALFSCREEN — error diary
def paper(pid, x, y, w, h, inner):
    return '<div class="paper hide" id="%s" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx">%s</div>' % (
        pid, x, y, w, h, inner)


L.append(
    '<div class="g full hide" id="g2">'
    '<div class="sheet board-bg hide" id="s2" style="height:930px">'
    '<div class="lbl" style="left:70px;top:50px">друге</div>'
    '<div class="hand hide" id="s2T" style="position:absolute;left:66px;top:82px;font-size:76px">Щоденник помилок</div>'
    + sk.svg(1080, 930, sk.underline(70, 182, 560, stroke="red"), sid="s2U") +
    '<div class="pill bpill hide" id="pf" style="left:60px;top:232px"><span class="dot" style="background:#EA4335"></span>Fathom</div>'
    '<div class="hand hide" id="pfT" style="position:absolute;left:76px;top:338px;font-size:40px;color:#EA4335">запис уроку</div>'
    + sk.svg(1080, 930, sk.arrow([(340, 280), (440, 262), (540, 280)], stroke="blue"), sid="a1") +
    '<div class="hand hide" id="a1T" style="position:absolute;left:330px;top:300px;font-size:38px;color:#4285F4">транскрипт</div>'
    + sk.svg(1080, 930, sk.ellipse(690, 282, 120, 82, stroke="ink", fill="yellow", style="solid"), sid="cE") +
    '<div class="gs hide" id="cT" style="position:absolute;left:570px;top:258px;width:240px;text-align:center;font-size:42px;font-weight:700">Claude</div>'
    '<div class="ab hide" id="skl" style="left:840px;top:246px"><span class="chip on">скіл</span></div>'
    + sk.svg(1080, 930, sk.arrow([(640, 372), (480, 420), (330, 470)], stroke="ink"), sid="a2") +
    paper("pE", 70, 480, 420, 220,
          '<div class="hand" style="position:absolute;left:26px;top:14px;font-size:44px">помилки учня</div>'
          '<div class="gs" style="position:absolute;left:30px;top:96px;font-size:36px">I goed</div>'
          '<div class="gs hide" id="pEf" style="position:absolute;left:30px;top:150px;font-size:36px;color:#188038">→ I went</div>'
          + sk.svg(420, 220, sk.line([(24, 120), (150, 118)], stroke="red", sw=6, double=False), sid="pEx")) +
    sk.svg(1080, 930, sk.arrow([(500, 590), (560, 590)], stroke="ink", sw=5, head=22), sid="a3") +
    paper("pV", 580, 480, 430, 220,
          '<div class="hand" style="position:absolute;left:26px;top:14px;font-size:44px">вправи</div>'
          + sk.svg(430, 220, sk.rect(28, 88, 30, 30, sw=3, round_=False) +
                   sk.line([(74, 104), (300, 102)], stroke="#9aa0a6", sw=4, double=False) +
                   sk.rect(28, 136, 30, 30, sw=3, round_=False) +
                   sk.line([(74, 152), (260, 152)], stroke="#9aa0a6", sw=4, double=False), sid="pVL") +
          '<div class="hand hide" id="pVT" style="position:absolute;left:150px;top:172px;font-size:34px;color:#4285F4">на наступний урок</div>') +
    '<div class="pill bpill hide" id="pn" style="left:90px;top:760px"><span class="dot" style="background:#1e1e1e"></span>Notion</div>'
    + sk.svg(1080, 930, sk.arrow([(400, 808), (480, 800), (560, 808)], stroke="green"), sid="a4") +
    paper("pK", 580, 730, 430, 150,
          '<div class="av" style="left:26px;top:20px;background:#4285F4">О</div>'
          '<div class="gs" style="position:absolute;left:108px;top:28px;font-size:36px;font-weight:700">Оля</div>'
          '<div class="hand" style="position:absolute;left:108px;top:76px;font-size:38px">картка учня</div>') +
    '</div></div>')


@beat
def b_s2():
    sfx("whoosh-short", "@druhe-0.1")
    sfx("pencil", "@shchod-0.2", -2)
    sfx("pop", "@fathom")
    sfx("pencil", "@zabyraie", -4)
    sfx("pop", "@skil")
    sfx("pencil", "@vypysuie", -3)
    sfx("pop", "@skladaie")
    sfx("pop", "@notion")
    sfx("pop", "@kartku")
    return js("""
  /* the flipped card opens into the halfscreen board */
  tl.to("#f1", {scale: 1.25, duration: 0.3, ease: "power2.in"}, @druhe-0.15);
  h.show("#g2", @druhe-0.15);
  h.boardIn("#s2", @druhe-0.15, 570, 530, 0.75);
  h.plateDown(@druhe-0.15, 350, 0.8);
  tl.set("#g1", {autoAlpha: 0}, @druhe+0.7);
  h.write("#s2T", @druhe+0.35, 0.8);
  h.draw("#s2U", @shchod+0.4, 0.35);
  h.pop("#pf", @fathom-0.05, {s: 0.5, r: -4});
  h.write("#pfT", @zapysuie, 0.45);
  h.draw("#cE", @claude2-0.15, 0.5);
  h.write("#cT", @claude2+0.1, 0.3);
  h.draw("#a1", @zabyraie-0.1, 0.4);
  h.write("#a1T", @zabyraie+0.15, 0.4);
  h.pop("#skl", @skil-0.05, {s: 0.5, r: 4});
  h.draw("#a2", @vypysuie-0.1, 0.35);
  h.pop("#pE", @vypysuie+0.1, {s: 0.6, r: -4, to: 0});
  h.draw("#pEx", @vypysuie+0.6, 0.25);
  h.write("#pEf", @vypysuie+0.85, 0.35);
  h.draw("#a3", @skladaie-0.15, 0.25);
  h.pop("#pV", @skladaie, {s: 0.6, r: 4, to: 0});
  h.draw("#pVL", @skladaie+0.2, 0.5);
  h.write("#pVT", @nastupnyi, 0.6);
  h.pop("#pn", @notion-0.05, {s: 0.5, r: -4});
  h.draw("#a4", @lahty-0.2, 0.4);
  h.pop("#pK", @kartku-0.1, {s: 0.5, r: 3, to: 0});
  h.bump("#pK", @kartku+0.4);
""")


@beat
def b_s3():
    sfx("whoosh-short", "@tretie-0.1")
    sfx("pop", "@samu")
    sfx("pencil", "@ne_vidd", -2)
    sfx("pop", "@orhanizovuvaty-0.1")
    sfx("click-soft", "@maks")
    sfx("typing", "@vytrachala", -5)
    sfx("pencil", "@poshuk", -2)
    sfx("ping", "@tochno")
    return js("""
  /* the board closes onto the student card: the homework app is under it */
  h.show("#g3", @tretie-0.2);
  h.show("#s3", @tretie-0.2);
  h.boardOut("#s2", @tretie-0.2, 795, 805, 0.6);
  h.plateDown(@tretie-0.2, 180, 0.75);
  h.pop("#s3T", @tretie+0.3, {s: 0.85, r: 0, y: 16});
  h.pop("#clx", @samu, {s: 0.5, r: -3});
  h.draw("#clxS", @ne_vidd, 0.45);
  h.wiggle("#clx", @ne_vidd+0.3);
  h.fadeOut("#clx, #clxS", @a_ot, 0.25);
  h.pop("#st1", @orhanizovuvaty-0.2, {s: 0.9, r: 0, y: 20});
  h.pop("#st2", @orhanizovuvaty-0.05, {s: 0.9, r: 0, y: 20});
  h.pop("#st3", @orhanizovuvaty+0.1, {s: 0.9, r: 0, y: 20});
  h.pop("#st4", @orhanizovuvaty+0.25, {s: 0.9, r: 0, y: 20});
  h.pop("#sc1", @maks-0.1, {s: 0.5, r: 0});
  h.pop("#sc2", @maks+0.1, {s: 0.5, r: 0});
  h.pop("#sc3", @maks+0.3, {s: 0.5, r: 0});
  h.pop("#sc4", @maks+0.5, {s: 0.5, r: 0});
  h.draw("#mkO", @maks+0.9, 0.5);
  h.pop("#srch", @vytrachala-0.2, {s: 0.8, r: 0, y: 12});
  h.type("#srT", @vytrachala, 22);
  h.draw("#srX", @poshuk, 0.3);
  h.draw("#okC", @tochno-0.1, 0.35);
  h.write("#okT", @mozhna-0.05, 0.35);
""")


# =============================================================== s4: HALFSCREEN — placement test
LV = "".join('<span class="lv" style="background:%s">%s</span>' % (c, l) for l, c in
             [("A1", "#34A853"), ("A2", "#34A853"), ("B1", "#4285F4"), ("B2", "#4285F4"), ("C1", "#EA4335")])
L.append(
    '<div class="g full hide" id="g4">'
    '<div class="sheet board-bg hide" id="s4" style="height:930px">'
    '<div class="lbl" style="left:70px;top:50px">четверте</div>'
    '<div class="hand hide" id="s4T" style="position:absolute;left:66px;top:82px;font-size:76px">Тест на рівень</div>'
    + sk.svg(1080, 930, sk.underline(70, 182, 470, stroke="blue"), sid="s4U") +
    '<div class="hand hide" id="s4N" style="position:absolute;left:640px;top:104px;font-size:46px;color:#4285F4">для нових учнів</div>'
    + sk.svg(1080, 930, sk.ellipse(170, 330, 110, 80, stroke="ink", fill="yellow", style="solid"), sid="c4E") +
    '<div class="gs hide" id="c4T" style="position:absolute;left:60px;top:306px;width:220px;text-align:center;font-size:40px;font-weight:700">Claude</div>'
    + sk.svg(1080, 930, sk.arrow([(290, 310), (330, 300), (360, 300)], stroke="ink", sw=5, head=22), sid="b1") +
    paper("qP", 370, 230, 340, 210,
          '<div class="hand" style="position:absolute;left:24px;top:12px;font-size:42px">питання</div>'
          '<div class="gs" style="position:absolute;left:24px;top:84px;font-size:32px">She ___ to school.</div>'
          '<div class="row" style="left:24px;top:140px;gap:12px"><span class="chip" style="height:50px;font-size:26px;padding:0 16px">go</span>'
          '<span class="chip on" style="height:50px;font-size:26px;padding:0 16px">goes</span>'
          '<span class="chip" style="height:50px;font-size:26px;padding:0 16px">going</span></div>') +
    paper("sP", 730, 230, 290, 210,
          '<div class="hand" style="position:absolute;left:24px;top:12px;font-size:42px">шкала</div>'
          '<div class="ab" style="left:20px;top:90px;width:260px;display:flex;flex-wrap:wrap;gap:10px">' + LV + '</div>') +
    '<div class="pill bpill hide" id="psp" style="left:60px;top:490px"><span class="dot" style="background:#34A853"></span>SendPulse</div>'
    '<div class="ab hide" id="bk" style="left:470px;top:502px"><span class="chip cg">без коду</span></div>'
    '<div class="node hide" id="n1" style="left:60px;top:620px">старт</div>'
    '<div class="node hide" id="n2" style="left:290px;top:620px">питання</div>'
    '<div class="node hide" id="n3" style="left:560px;top:620px">результат</div>'
    + sk.svg(1080, 930, sk.arrow([(200, 657), (280, 657)], stroke="ink", sw=4, head=18), sid="na1")
    + sk.svg(1080, 930, sk.arrow([(470, 657), (550, 657)], stroke="ink", sw=4, head=18), sid="na2")
    + sk.svg(1080, 930, sk.arrow([(800, 660), (900, 680), (900, 730)], stroke="green", sw=5, head=22), sid="na3") +
    '<div class="gcard hide" id="crm" style="left:620px;top:745px;width:400px;height:140px">'
    '<span class="chip cy" style="position:absolute;left:20px;top:16px;height:52px;font-size:28px;font-weight:700">CRM</span>'
    '<div class="gs" style="position:absolute;left:20px;top:84px;font-size:30px">нова учениця · <b style="color:#4285F4">B1</b></div></div>'
    + sk.svg(1080, 930, sk._p("M90 740 L 90 790 C 90 830, 160 830, 160 790 L 160 740", "#EA4335", 18, "dr") +
             sk.line([(80, 748), (100, 748)], stroke="ink", sw=10, double=False) +
             sk.line([(150, 748), (170, 748)], stroke="ink", sw=10, double=False), sid="mag") +
    '<div class="hand hide" id="magT" style="position:absolute;left:190px;top:746px;font-size:48px">лідмагніт</div>'
    '<div class="ab hide" id="kv" style="left:70px;top:832px"><span class="chip on">кваліфікація лідів</span></div>'
    + sk.svg(1080, 930, sk.circle_around(540, 812, 510, 98, stroke="green", sw=6), sid="loop") +
    '</div></div>')


@beat
def b_s4():
    sfx("whoosh-short", "@chetverte-0.2")
    sfx("pencil", "@test", -2)
    sfx("pencil", "@claude3-0.1", -4)
    sfx("pop", "@pytannia")
    sfx("pop", "@shkalu")
    sfx("pencil", "@lants", -4)
    sfx("pop", "@sendpulse")
    sfx("pop", "@bez")
    sfx("pop", "@padaiut")
    sfx("pencil", "@lidmagnit-0.1", -3)
    sfx("pop", "@kvalif")
    sfx("pencil", "@odnomu", -4)
    return js("""
  /* the tick opens the second board */
  h.show("#g4", @chetverte-0.35);
  h.boardIn("#s4", @chetverte-0.35, 915, 120, 0.75);
  h.plateDown(@chetverte-0.35, 350, 0.8);
  tl.set("#g3", {autoAlpha: 0}, @chetverte+0.5);
  h.write("#s4T", @chetverte+0.3, 0.7);
  h.draw("#s4U", @test+0.45, 0.35);
  h.write("#s4N", @novykh-0.1, 0.6);
  h.draw("#c4E", @claude3-0.2, 0.45);
  h.write("#c4T", @claude3, 0.3);
  h.draw("#b1", @pytannia-0.3, 0.2);
  h.pop("#qP", @pytannia-0.1, {s: 0.6, r: -4, to: 0});
  h.pop("#sP", @shkalu-0.1, {s: 0.6, r: 4, to: 0});
  h.pop("#n1", @lants, {s: 0.6, r: 0});
  h.draw("#na1", @lants+0.25, 0.2);
  h.pop("#n2", @lants+0.4, {s: 0.6, r: 0});
  h.draw("#na2", @lants+0.65, 0.2);
  h.pop("#n3", @lants+0.8, {s: 0.6, r: 0});
  h.pop("#psp", @sendpulse-0.05, {s: 0.5, r: -4});
  h.pop("#bk", @bez-0.05, {s: 0.5, r: 4});
  h.bump("#n3", @rezult);
  h.draw("#na3", @padaiut-0.2, 0.35);
  h.pop("#crm", @padaiut+0.1, {s: 0.5, r: 3, to: 0});
  h.draw("#mag", @lidmagnit-0.15, 0.4);
  h.write("#magT", @lidmagnit, 0.4);
  h.pop("#kv", @kvalif-0.05, {s: 0.5, r: -3});
  h.draw("#loop", @odnomu-0.1, 0.7);
""")


@beat
def b_s5():
    sfx("whoosh-short", "@tomu-0.15")
    sfx("click", "@zberezhy+0.1")
    sfx("whoosh-short", "@pereshly")
    sfx("click-soft", "@kolezi")
    return js("""
  /* the board closes onto the CRM card: the post with its action bar is under it */
  h.show("#g5", @tomu-0.3);
  h.show("#s5", @tomu-0.3);
  h.boardOut("#s4", @tomu-0.3, 820, 815, 0.6);
  h.plateDown(@tomu-0.3, 60, 0.75);
  h.draw("#icons", @tomu+0.2, 0.6);
  h.draw("#bm", @tomu+0.3, 0.3);
  tl.fromTo("#bmF", {opacity: 0}, {opacity: 1, duration: 0.2, immediateRender: false}, @zberezhy);
  h.bump("#bm", @zberezhy);
  h.write("#bmT", @zberezhy+0.1, 0.4);
  h.write("#shT", @pereshly-0.1, 0.4);
  h.pop("#share", @pereshly+0.15, {s: 0.6, r: 0, y: 20});
  h.bump("#share", @kolezi);
""")


INVERT = []    # halfscreen keeps her (and the white captions) in the bottom half
# captions drop only where a graphic says her words at the same time
BLACKOUT = [(T["kyt"], T["angl"] + 0.55, ""),                 # chips китайська / англійська
            (T["druhe"], T["shchod"] + 0.7, ""),              # «Щоденник помилок»
            (T["tretie"], T["domashok"] + 0.45, ""),          # «Перевірка домашок»
            (T["chetverte"] - 0.2, T["test"] + 0.7, ""),     # «Тест на рівень»
            (T["bez"], T["bez"] + 0.4, ""),                   # chip «без коду»
            (T["lidmagnit"], T["lidmagnit"] + 0.5, "")]       # «лідмагніт»


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
        title=u"Reel 63 — автоматизації викладачки мови",
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
