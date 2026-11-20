# -*- coding: utf-8 -*-
"""Nika r01: «Шукаю 25 експертів». An UNLOCK ad, built on the approved look (../tools/look.py).

    python ../tools/plate.py ../work/src/IMG_7332.MOV . "<SPANS>" <SPEED>   # graded, tightened, -14 LUFS
    python build.py && python ../tools/sfx.py mix .                  # index.html + sfx.json -> base.mp4
    npx hyperframes@0.8.33 render . -o renders/NIKA-R01.mp4 -q high --fps 30

index.html is generated; edit this file. Spelling: script.txt. Beats: PLAN.md.
"""
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "tools"))
from look import Reel, scrap, card, html_card, icon, cursor, pink_shadow, LOCK, REST  # noqa: E402

# Kept spans of IMG_7332. The pauses over ~0.5 s are tightened to ~0.3 s and the
# lead-in is trimmed. Three cuts fall under the stage; the two on her get a zoom change.
SPANS = [(0.52, 14.92), (15.52, 20.00), (20.42, 45.05), (45.85, 55.00), (55.36, 68.40), (68.66, 72.10)]
SPEED = 1.2                    # her delivery sped up, pitch kept (Nika, 2026-11-20)
R = Reel(SPANS, SPEED)
T = R.T

CAPS = [
    ("привіт!", 0.68, 1.34), ("я шукаю", 1.34, 2.02), ("25 експертів,", 2.02, 3.32),
    ("яким хочу", 3.32, 3.82), ("особисто", 3.82, 4.54), ("показати,", 4.54, 5.16),
    ("як запустити", 5.16, 5.86), ("цифровий продукт", 5.86, 6.94), ("без команди.", 6.94, 8.10),
    ("раніше для цього", 8.10, 9.22), ("потрібні були", 9.22, 9.86),
    # 9.86–12.98: the tiles name them
    ("і ще хтось,", 12.98, 13.66), ("хто це все налаштує", 13.66, 14.92),
    ("а тепер достатньо", 15.67, 17.02), ("лише двох речей", 17.02, 18.00),
    # 18.00–20.45: the stage says it, «твоя експертиза + unlock»
    ("мене звати Ніка", 20.56, 21.76), ("і я працюю над Unlock", 21.76, 23.08),
    ("над платформою,", 23.08, 23.88), ("де ти можеш", 23.88, 24.40), ("створювати", 24.40, 24.92),
    ("мінікурси,", 24.92, 25.66), ("приймати оплати", 25.66, 26.60), ("та продавати", 26.60, 27.30),
    ("свої знання", 27.30, 27.92), ("і все в одному місці", 27.92, 29.80),
    ("і зараз я хочу", 29.80, 30.98), ("особисто", 30.98, 31.70), ("познайомитися", 31.70, 32.60),
    ("з нашими першими", 32.60, 33.62), ("користувачами.", 33.62, 34.56),
    ("тому запрошую тебе", 34.56, 35.74), ("на 20-хвилинну", 35.74, 37.26),
    ("демозустріч зі мною,", 37.26, 38.52), ("де я покажу", 38.52, 39.58), ("платформу,", 39.58, 40.28),
    ("відповім", 40.28, 40.64), ("на запитання,", 40.64, 41.38), ("і ми разом", 41.38, 42.04),
    ("подивимося,", 42.04, 42.68), ("як Unlock може", 42.68, 43.68), ("допомогти", 43.68, 44.12),
    ("саме тобі.", 44.12, 45.05),
    ("а якщо", 46.03, 46.76), ("після зустрічі", 46.76, 47.72), ("ти приєднаєшся", 47.72, 48.86),
    ("до нас", 48.86, 49.30), ("цього тижня,", 49.30, 50.36), ("то ти отримаєш", 50.36, 51.62),
    ("цілий рік Unlock", 51.62, 52.62), ("за ціною", 52.62, 53.44), ("одного місяця.", 53.44, 55.00),
    ("пропозиція діє", 55.50, 56.54), ("тільки для перших", 56.54, 57.74), ("ста експертів.", 57.74, 59.48),
    # 59.48–66.02: the chips name them
    ("хто хоче", 66.02, 66.82), ("монетизувати", 66.82, 67.48), ("свої знання.", 67.48, 68.40),
    ("пиши «Unlock»", 68.82, 69.58), ("у коментарях", 69.58, 70.38), ("і побачимося на демо", 70.38, 72.10),
]

# --------------------------------------------------------------------------- pieces
PILE = [  # «раніше для цього потрібні були…»: the old way, one tile per thing she lists
    ("t1", "i-layout", "Сайт", 300, 440, -7, 9.86),
    ("t2", "i-tg", "Telegram-бот", 700, 575, 6, 10.30),
    ("t3", "i-card", "Платіжна система", 430, 760, 3, 10.96),
    ("m1", "i-mail", None, 175, 965, 10, 12.06),
    ("m2", "i-chart", None, 905, 770, -12, 12.16),
    ("t4", "i-share", "Інтеграції", 720, 945, -5, 12.30),
    ("m3", "i-file", None, 905, 1110, 8, 12.42),
    ("t5", "i-user", "Підрядник", 330, 1105, -4, 13.30),
]

NICHES = [  # her words, one chip per word
    ("Психологи", "i-n-psy", 59.48), ("Коучі", "i-users", 60.20), ("Викладачі мов", "i-n-edu", 60.74),
    ("Маркетологи", "i-mega", 62.86), ("Консультанти", "i-chat", 63.70), ("Продюсери", "i-video", 64.50),
]
EVERYONE = [  # «і всі-всі-всі»: the site's own list of fields, around her
    ("Бізнес і підприємництво", "i-n-biz", 320, 125, -4), ("Маркетинг і комунікації", "i-mega", 760, 215, 3),
    ("Краса та стиль", "i-n-beauty", 175, 400, -6), ("Дизайн і креатив", "i-n-design", 190, 640, 4),
    ("IT та технології", "i-n-code", 905, 365, 5), ("Здоров’я та спорт", "i-n-health", 890, 610, -4),
    ("Lifestyle та хобі", "i-n-life", 200, 880, -3), ("Освіта та навчання", "i-n-edu", 880, 860, 3),
    ("Психологія та розвиток", "i-n-psy", 300, 1480, 3), ("Фінанси та кар’єра", "i-n-wallet", 790, 1525, -4),
    ("Мистецтво та творчість", "i-n-brush", 330, 1650, -2), ("Професійна експертиза", "i-n-award", 760, 1700, 4),
]

HEART = ('<svg viewBox="0 0 24 24" width="46" height="46"><path d="M12 21s-7.5-4.6-9.6-9.2C.9 8.4 3 4.6 6.6 4.6c2.1 0 '
         '3.6 1.2 5.4 3.2 1.8-2 3.3-3.2 5.4-3.2 3.6 0 5.7 3.8 4.2 7.2C19.5 16.4 12 21 12 21z" fill="#F0648F"/></svg>')

CSS = """
#pile, #gB, #nich { display: none; }
#grey { position: absolute; inset: 0; visibility: hidden; opacity: 0; background: linear-gradient(180deg, #F7F7F9 0%, #ECECF0 100%); }
.tile { position: absolute; display: flex; align-items: center; gap: 22px; padding: 20px 34px 20px 20px;
  background: #fff; border-radius: 30px; border: 1.5px solid rgba(10,15,29,0.08); white-space: nowrap;
  box-shadow: 0 30px 50px -24px rgba(20,25,60,0.30), 0 4px 10px rgba(10,15,29,0.06);
  font: 600 40px/1 "Geist", sans-serif; letter-spacing: -0.01em; color: #2D3142; visibility: hidden; }
.tile.mini { padding: 18px; }
.ib { width: 72px; height: 72px; border-radius: 22px; background: #F0F0F3; display: flex; align-items: center;
  justify-content: center; flex: none; }
.tile .ib .ic { color: #656B7A; }

.inv { position: absolute; inset: 0; padding: 46px 50px; display: flex; flex-direction: column; gap: 28px; }
.row { display: flex; align-items: center; gap: 16px; }
.micro { font: 700 22px/1 "Geist"; letter-spacing: 0.16em; color: #656B7A; }
.ttl { font: 650 56px/1.06 "Geist"; letter-spacing: -0.03em; color: #0A0F1D; }
.pill { display: inline-flex; align-items: center; gap: 12px; padding: 14px 26px 14px 16px; border-radius: 999px;
  background: #F4F7FF; border: 1.5px solid rgba(45,67,210,0.16); font: 600 32px/1 "Geist"; color: #1E32B4; }
.av { width: 72px; height: 72px; border-radius: 50%; background: linear-gradient(135deg, #2D43D2, #8F31EA);
  color: #fff; font: 700 32px/72px "Geist"; text-align: center; flex: none; }
.av.you { background: #14192A; }
.who { font: 600 32px/1 "Geist"; color: #2D3142; flex: 1; }
.btn { padding: 22px 34px; border-radius: 22px; background: linear-gradient(135deg, #2D43D2, #8F31EA); color: #fff;
  font: 650 32px/1 "Geist"; box-shadow: 0 14px 30px -10px rgba(63,88,232,0.6); }
.ib.soft { background: #EEF1FF; border-radius: 50%; }

.call .bar { position: absolute; left: 0; right: 0; top: 0; height: 86px; display: flex; align-items: center; gap: 18px;
  padding: 0 30px; border-bottom: 1.5px solid rgba(10,15,29,0.07); }
.dots { display: flex; gap: 9px; } .dots i { width: 16px; height: 16px; border-radius: 50%; background: #E4E7EE; }
.ttl2 { font: 600 30px/1 "Geist"; color: #14192A; flex: 1; }
.rec { display: flex; align-items: center; gap: 10px; font: 650 26px/1 "Geist"; color: #E5484D; }
.rec i { width: 14px; height: 14px; border-radius: 50%; background: #E5484D; }
.screen { position: absolute; left: 30px; top: 112px; width: 840px; height: 400px; border-radius: 22px;
  background: #F4F7FF; border: 1.5px solid rgba(10,15,29,0.06); display: flex; align-items: center;
  justify-content: center; overflow: hidden; }
.screen img { width: 800px; }
.ctrl { position: absolute; left: 0; right: 0; bottom: 24px; display: flex; justify-content: center; gap: 18px; }
.cb { width: 76px; height: 76px; border-radius: 50%; background: #F2F4F8; display: flex; align-items: center;
  justify-content: center; } .cb.end { background: #E5484D; }
.ppl { position: absolute; right: -36px; top: 150px; display: flex; flex-direction: column; gap: 14px; }
.ppl .av { width: 88px; height: 88px; font-size: 36px; line-height: 88px; border: 5px solid #fff;
  box-shadow: 0 14px 26px -10px rgba(10,15,29,0.35); }
#bq { position: absolute; right: -70px; top: 360px; width: 116px; height: 116px; border-radius: 44px 44px 14px 44px;
  background: linear-gradient(135deg, #2D43D2, #8F31EA); color: #fff; font: 800 70px/116px "Geist";
  text-align: center; box-shadow: 0 20px 36px -12px rgba(63,88,232,0.6); visibility: hidden; }
#ba { position: absolute; left: -56px; top: 400px; padding: 30px 30px; border-radius: 44px 44px 44px 14px;
  background: #fff; display: flex; gap: 12px; box-shadow: 0 20px 40px -14px rgba(10,15,29,0.35); visibility: hidden; }
.tdot { width: 18px; height: 18px; border-radius: 50%; background: #878D9C; }

.mt { position: absolute; width: 150px; height: 150px; border-radius: 34px; background: #fff;
  border: 1.5px solid rgba(10,15,29,0.08); box-shadow: 0 24px 40px -22px rgba(45,50,160,0.35);
  display: flex; flex-direction: column; align-items: center; justify-content: center; visibility: hidden;
  font: 700 62px/1 "Geist"; letter-spacing: -0.03em; color: #0A0F1D; }
.mt small { font: 600 22px/1 "Geist"; color: #878D9C; margin-top: 8px; letter-spacing: 0.04em; position: relative; }
.mt b { position: relative; font-weight: 700; }
.mtbg { position: absolute; inset: 0; border-radius: inherit; background: linear-gradient(135deg, #2D43D2, #8F31EA); opacity: 0; }
#mhead { position: absolute; left: 333px; top: -96px; white-space: nowrap; visibility: hidden; }
#mtag { position: absolute; left: 333px; top: 530px; white-space: nowrap; visibility: hidden; font-size: 34px; }

#hn { position: absolute; left: 400px; top: 210px; transform: translate(-50%, -50%); white-space: nowrap;
  font: 800 400px/1 "Geist"; letter-spacing: -0.07em;
  background: linear-gradient(135deg, #2D43D2 0%, #8F31EA 100%); -webkit-background-clip: text; background-clip: text;
  color: transparent; padding: 0 30px; }
#hl { position: absolute; left: 400px; top: 470px; transform: translate(-50%, -50%); white-space: nowrap;
  font: 600 56px/1 "Geist"; letter-spacing: -0.02em; color: #2D3142; visibility: hidden; }

.chips { position: absolute; left: 0; width: 1080px; display: flex; justify-content: center; gap: 20px; }
.chip { display: inline-flex; align-items: center; gap: 16px; padding: 12px 32px 12px 12px; border-radius: 999px;
  background: #fff; border: 1.5px solid rgba(10,15,29,0.10); white-space: nowrap; visibility: hidden;
  box-shadow: 0 18px 34px -16px rgba(20,25,60,0.45); font: 600 40px/1 "Geist"; letter-spacing: -0.01em; color: #0A0F1D; }
.chip .ib { width: 62px; height: 62px; border-radius: 50%; background: #EEF1FF; }
.chip.sm { position: absolute; font-size: 28px; padding: 8px 24px 8px 8px; gap: 12px; }
.chip.sm .ib { width: 46px; height: 46px; }

#cmt { position: absolute; left: 540px; top: 1110px; width: 880px; height: 118px; border-radius: 59px; background: #fff;
  box-shadow: 0 30px 60px -20px rgba(0,0,0,0.40); display: none; align-items: center; gap: 22px; padding: 0 20px;
  visibility: hidden; }
.cav { width: 78px; height: 78px; border-radius: 50%; background: #E4E7EE; display: flex; align-items: center;
  justify-content: center; flex: none; }
.fld { flex: 1; position: relative; font: 500 40px/1 "Geist"; color: #0A0F1D; white-space: nowrap; }
#ph { position: absolute; left: 0; top: 50%; transform: translateY(-50%); color: #878D9C; }
.k { visibility: hidden; font-weight: 650; }
#caret { display: inline-block; width: 3px; height: 44px; background: #2D43D2; vertical-align: middle; margin-left: 2px;
  visibility: hidden; }
#send { width: 78px; height: 78px; border-radius: 50%; background: linear-gradient(135deg, #2D43D2, #8F31EA);
  display: flex; align-items: center; justify-content: center; flex: none; }
#heart { position: absolute; right: 120px; top: 36px; visibility: hidden; }
"""


def body():
    pile = "\n".join(
        f'<div class="tile{" mini" if lbl is None else ""}" id="{tid}" style="left:{x}px;top:{y}px">'
        f'<span class="ib">{icon(ic, 40, "#656B7A")}</span>{lbl or ""}</div>'
        for tid, ic, lbl, x, y, rot, _ in PILE)

    invite = html_card("inv", 780, 480, f"""<div class="inv">
      <div class="row"><span class="ib soft">{icon("i-calendar", 36)}</span><span class="micro">ЗАПРОШЕННЯ</span></div>
      <div class="ttl">Демозустріч<br>з Нікою</div>
      <div class="row"><span class="pill" id="p20">{icon("i-clock", 32, "#1E32B4")}20 хвилин</span>
        <span class="pill">{icon("i-video", 32, "#1E32B4")}онлайн</span></div>
      <div class="row"><span class="av">Н</span><span class="who">Ніка · Unlock</span><span class="btn">Записатися</span></div>
    </div>""")

    call = html_card("call", 900, 640, f"""
      <div class="bar"><span class="dots"><i></i><i></i><i></i></span><span class="ttl2">Демо · Unlock</span>
        <span class="rec"><i></i>20 хв</span></div>
      <div class="screen"><img src="assets/ui/dashboard-call.png"></div>
      <div class="ctrl"><span class="cb">{icon("i-video", 36, "#2D3142")}</span><span class="cb">{icon("i-chat", 36, "#2D3142")}</span>
        <span class="cb">{icon("i-share", 36, "#2D3142")}</span><span class="cb end">{icon("i-x", 36, "#fff", 2.6)}</span></div>
      <div class="ppl"><span class="av">Н</span><span class="av you">Ти</span></div>
      <div id="bq">?</div>
      <div id="ba"><i class="tdot"></i><i class="tdot"></i><i class="tdot"></i></div>""", cls="call")

    tiles = "\n".join(
        f'<div class="mt" id="mt{i + 1}" style="left:{(i % 4) * 172}px;top:{(i // 4) * 172}px">'
        f'<span class="mtbg"></span><b>{i + 1}</b><small>міс.</small></div>' for i in range(12))
    months = (f'<div class="card" id="months" style="width:666px;height:494px">{tiles}'
              f'<span class="pill" id="mhead">{icon("i-calendar", 32, "#1E32B4")}12 місяців Unlock</span>'
              f'<span class="pill" id="mtag">{icon("i-check", 30, "#1E32B4", 2.6)}ціна 1 місяця</span></div>')
    hund = '<div class="card" id="hund" style="width:800px;height:520px"><div id="hn">0</div><div id="hl">перших експертів</div></div>'

    product = "\n      ".join([
        card("cP", "products", cursor("k1", 0.874, 0.232)), card("cE", "editor"), card("cPay", "payments"),
        card("tPay", "toast-pay"), card("cS", "salespage", cursor("k2", 0.83, 0.83)), card("cD", "dashboard"),
        card("cPh", "phone")])

    stage = f"""
  <div id="stage">
    <div class="blob" id="bl1"></div><div class="blob" id="bl2"></div><div id="gridbg"></div>
    <div id="grey"></div>
    <div id="pile">{pile}</div>
    <div id="gB">{scrap("bExp", "твоя експертиза", 86, 3, cls="big")}
    <div id="plus" style="position:absolute;left:540px;top:905px;visibility:hidden;font:900 120px/1 'MS';color:#F9B5CA;text-shadow:{pink_shadow(6)}">+</div>
    <div class="lockup" id="lock" style="left:540px;top:1085px"><div class="mark" id="mark">{LOCK}</div><div class="word" id="word">unlock</div></div></div>
    <div id="scene"><div id="world">
      {product}
      {invite}
      {call}
      {months}
      {hund}
    </div></div>
  </div>"""

    rows = [NICHES[0:2], NICHES[2:4], NICHES[4:6]]
    chips = "\n".join(
        f'<div class="chips" style="top:{1040 + r * 108}px">' + "".join(
            f'<span class="chip" id="ch{r * 2 + k}"><span class="ib">{icon(ic, 34)}</span>{lbl}</span>'
            for k, (lbl, ic, _) in enumerate(row)) + "</div>" for r, row in enumerate(rows))
    burst = "\n".join(
        f'<span class="chip sm" id="cb{i}" style="left:{x}px;top:{y}px"><span class="ib">{icon(ic, 26)}</span>{lbl}</span>'
        for i, (lbl, ic, x, y, rot) in enumerate(EVERYONE))

    letters = "".join(f'<span class="k" id="kk{i}">{c}</span>' for i, c in enumerate("Unlock"))
    composer = f"""<div id="cmt"><span class="cav">{icon("i-user", 40, "#656B7A")}</span>
    <span class="fld"><span id="ph">Додайте коментар…</span>{letters}<span id="caret"></span></span>
    <span id="send">{icon("i-send", 38, "#fff", 2.4)}</span><span id="heart">{HEART}</span></div>"""

    return stage + f"""
  <div id="over">
<div id="nich">
{chips}
{burst}
</div>
{composer}
  </div>
  <div id="caps">
{R.captions(CAPS)}
  </div>"""


# --------------------------------------------------------------------------- motion
def motion():
    j = R.j
    j('gsap.set([".big","#plus","#lock",".tile",".chip.sm","#cmt"],{xPercent:-50,yPercent:-50});')
    j('gsap.set(".cap",{xPercent:-50,yPercent:-50});')
    j('gsap.set(".card",{xPercent:-50,yPercent:-50});')
    j('gsap.set(["#mhead","#mtag"],{xPercent:-50});')
    j(f'tl.to("#bl1",{{x:-160,y:120,duration:{R.dur},ease:"none"}},0);')
    j(f'tl.to("#bl2",{{x:140,y:-140,duration:{R.dur},ease:"none"}},0);')
    R.fx(T(0.68), "click")

    # ---- her, 0–8.7: the hook, with a snap zoom on «25 експертів»
    R.push(0, T(2.02), 1.0, 1.03)
    j(f'tl.to("#cam",{{scale:1.11,duration:0.2,ease:"power3.out"}},{T(2.02)});')
    R.fx(T(2.02), "swish", -4)
    R.push(T(2.25), T(8.70), 1.11, 1.06)

    # ---- the old way, 8.7–14.92: a pile of separate tools
    a = T(8.70)
    R.stage_in(a)
    R.show("#pile", a)
    j(f'tl.set("#grey",{{autoAlpha:1}},{a});')
    for tid, ic, lbl, x, y, rot, s in PILE:
        R.pop(f'"#{tid}"', T(s), f"{{autoAlpha:0,scale:0.5,y:-70,rotation:{rot * 3}}}",
              f"{{autoAlpha:1,scale:1,y:0,rotation:{rot}}}", 0.45, "back.out(1.8)", "pop",
              -3 if lbl else -8)
    j(f'tl.fromTo("#pile",{{rotation:-0.6}},{{rotation:0.8,duration:{round(T(14.92) - a, 3)},'
      f'ease:"sine.inOut",immediateRender:false}},{a});')
    x = T(14.92)                       # the cut: «налаштує.» | «А тепер»
    rng = random.Random(3)
    for k, (tid, *_r) in enumerate(PILE):
        j(f'tl.to("#{tid}",{{y:"+=1500",rotation:"+={rng.uniform(-40, 40):.0f}",duration:0.55,'
          f'ease:"power2.in"}},{round(x - 0.42 + k * 0.025, 3)});')
    R.fx(x - 0.42, "whoosh", -3)
    R.stage_out(round(x - 0.12, 3), hide=["#pile", "#grey"])

    # ---- her, «а тепер достатньо лише двох речей»
    R.push(round(x - 0.12, 3), T(18.00), 1.0, 1.035)

    # ---- «твоєї експертизи та Unlock»
    b = T(18.00)
    R.stage_in(b)
    R.show("#gB", b)
    R.pop('"#bExp"', T(18.30), "{autoAlpha:0,scale:0.6,rotation:-12}", "{autoAlpha:1,scale:1,rotation:-3}",
          0.5, "back.out(1.9)", "pop", 0)
    R.pop('"#plus"', T(19.24), "{autoAlpha:0,scale:0.3,rotation:-90}", "{autoAlpha:1,scale:1,rotation:0}",
          0.4, "back.out(2.5)", "pop", -5)
    j(f'tl.set("#lock",{{autoAlpha:1}},{T(19.40)});')
    R.pop('"#mark"', T(19.40), "{scale:0,rotation:-25}", "{scale:1,rotation:0}", 0.55, "back.out(2)", "pop", -2)
    j(f'tl.fromTo("#word",{{autoAlpha:0,x:-50,clipPath:"inset(0 100% 0 0)"}},{{autoAlpha:1,x:0,'
      f'clipPath:"inset(0 0% 0 0)",duration:0.5,ease:"power3.out",immediateRender:false}},{T(19.55)});')
    R.fx(T(19.50), "sparkle")
    j(f'tl.to(["#bExp","#plus","#lock"],{{y:"-=26",duration:{round(T(20.0) - T(18.30), 3)},'
      f'ease:"sine.inOut"}},{T(18.30)});')
    c = round(T(20.00) - 0.10, 3)      # the cut: «Unlock.» | «Мене»
    R.stage_out(c, hide=["#gB"])

    # ---- her, «мене звати Ніка, і я працюю над Unlock»
    R.push(c, T(23.00), 1.06, 1.10)

    # ---- the platform, 23.0–29.8: one screen per thing she names
    d = T(23.00)
    R.stage_in(d)
    # at 1.2x the screens come quicker: shorter entrances and exits, and the editor follows the click
    IN, OUT = 0.48, 0.34
    R.card_in("cP", T(23.06), IN); R.card_hold("cP", round(T(23.06) + IN, 3), T(24.56))
    R.click("k1", T(23.86), T(24.30))
    R.card_out("cP", T(24.56), OUT); R.fx(T(24.56), "swish")
    R.card_in("cE", T(24.62), IN); R.card_hold("cE", round(T(24.62) + IN, 3), T(25.58))
    R.card_out("cE", T(25.58), OUT); R.fx(T(25.58), "swish")
    R.card_in("cPay", T(25.64), IN); R.card_hold("cPay", round(T(25.64) + IN, 3), T(26.52))
    R.show("#tPay", T(26.06))
    R.pop('"#tPay"', T(26.06), "{autoAlpha:0,x:240,y:-330,z:160,scale:0.7,rotationY:-21,rotationX:13,rotationZ:2}",
          "{autoAlpha:1,x:220,y:-300,z:200,scale:1}", 0.45, "back.out(2)", "kaching", 0)
    R.card_out("cPay", T(26.52), OUT)
    j(f'tl.to("#tPay",{{x:-700,y:-380,z:0,autoAlpha:0,duration:{OUT},ease:"power2.in"}},{T(26.52)});')
    R.fx(T(26.52), "swish")
    R.card_in("cS", T(26.58), IN); R.card_hold("cS", round(T(26.58) + IN, 3), T(27.90))
    R.click("k2", T(27.10), T(27.52))
    e = T(27.90)                       # «і все в одному місці»: everything at once, the camera pulls back
    R.fx(e - 0.04, "whoosh", -3)
    j(f'tl.to("#k2",{{autoAlpha:0,duration:0.15}},{e});')
    j(f'tl.to("#cS",{{x:-275,y:215,z:140,rotationY:-18,rotationX:12,rotationZ:2,scale:0.6,duration:0.75,'
      f'ease:"power3.inOut"}},{e});')
    R.show(["#cD", "#cPh"], round(e + 0.05, 3))
    j(f'tl.fromTo("#cD",{{autoAlpha:0,x:0,y:-90,z:-700,rotationY:-21,rotationX:13,rotationZ:2}},'
      f'{{autoAlpha:1,z:-60,duration:0.8,ease:"expo.out",immediateRender:false}},{round(e + 0.05, 3)});')
    j(f'tl.fromTo("#cP",{{autoAlpha:0,x:-560,y:-460,z:-200,rotationY:-34,rotationX:13,rotationZ:2,scale:0.55}},'
      f'{{autoAlpha:1,x:-240,y:-440,z:60,rotationY:-21,duration:0.75,ease:"expo.out",immediateRender:false}},'
      f'{round(e + 0.15, 3)});')
    j(f'tl.fromTo("#cPh",{{autoAlpha:0,x:620,y:120,z:-100,rotationY:-34,rotationX:13,rotationZ:2,scale:1}},'
      f'{{autoAlpha:1,x:330,y:40,z:200,rotationY:-18,duration:0.75,ease:"expo.out",immediateRender:false}},'
      f'{round(e + 0.22, 3)});')
    R.pop('"#tPay"', round(e + 0.35, 3), "{autoAlpha:0,x:560,y:-470,z:120,rotationY:-21,rotationX:13,rotationZ:2,scale:0.8}",
          "{autoAlpha:1,x:270,y:-430,z:240,scale:0.9}", 0.6, "back.out(1.8)", "pop", -6)
    f = T(29.80)
    j(f'tl.fromTo("#world",{{scale:1.1,y:0,rotationY:0}},{{scale:0.94,y:-70,rotationY:-5,duration:{round(f - e, 3)},'
      f'ease:"sine.inOut",immediateRender:false}},{e});')
    R.stage_out(f, hide=["#cP", "#cE", "#cPay", "#tPay", "#cS", "#cD", "#cPh"])

    # ---- her, «і зараз я хочу особисто познайомитися…»
    R.push(f, T(35.70), 1.0, 1.045)

    # ---- the demo, 35.7–41.3
    g = T(35.70)
    R.stage_in(g)
    j(f'tl.set("#world",{{scale:1,y:0,rotationY:0}},{g});')
    R.card_in("inv", T(35.80)); R.fx(T(36.0), "ping", -3)
    j(f'tl.to("#p20",{{scale:1.14,duration:0.2,yoyo:true,repeat:1,ease:"power2.out"}},{T(36.10)});')
    R.card_hold("inv", T(36.42), T(38.40))
    R.card_out("inv", T(38.40)); R.fx(T(38.40), "swish")
    R.card_in("call", T(38.48)); R.card_hold("call", T(39.10), T(41.25))
    R.pop('"#bq"', T(40.28), "{autoAlpha:0,scale:0.3,rotation:-20}", "{autoAlpha:1,scale:1,rotation:0}",
          0.4, "back.out(2.4)", "ping", -5)
    R.pop('"#ba"', T(40.80), "{autoAlpha:0,scale:0.4}", "{autoAlpha:1,scale:1}", 0.35, "back.out(2)", "pop", -8)
    j(f'tl.to("#ba .tdot",{{y:-10,duration:0.22,yoyo:true,repeat:3,stagger:0.08,ease:"sine.inOut"}},{T(40.95)});')
    R.stage_out(T(41.30), hide=["#inv", "#call"])

    # ---- her, «і ми разом подивимося, як Unlock може допомогти саме тобі» | cut | «а якщо…»
    h = T(41.30)
    R.push(h, T(45.05), 1.04, 1.075)
    R.push(T(45.85), T(50.30), 1.12, 1.16)            # the cut on her: a closer frame

    # ---- the offer, 50.3–55.0: a year for the price of a month
    k = T(50.30)
    R.stage_in(k)
    j(f'tl.set("#world",{{scale:1,y:-30,rotationY:0}},{k});')
    R.show("#months", k)
    j(f'tl.fromTo("#months",Object.assign({REST},{{autoAlpha:1,z:-120}}),{{z:120,duration:{round(T(55.0) - 0.22 - k, 3)},'
      f'ease:"sine.inOut",immediateRender:false}},{k});')
    R.pop('"#mhead"', T(50.36), "{autoAlpha:0,y:30,scale:0.8}", "{autoAlpha:1,y:0,scale:1}", 0.4, "back.out(2)", "pop", -4)
    j(f'tl.fromTo(".mt",{{autoAlpha:0,scale:0.4,z:-80}},{{autoAlpha:1,scale:1,z:0,duration:0.38,ease:"back.out(2)",'
      f'stagger:0.045,immediateRender:false}},{T(51.62)});')
    R.fx(T(51.62), "pop", -4); R.fx(T(51.80), "sparkle", -2)
    j(f'tl.to(".mt:not(#mt1)",{{opacity:0.28,scale:0.9,duration:0.4,ease:"power2.out"}},{T(52.90)});')
    j(f'tl.to("#mt1",{{z:90,scale:1.14,color:"#ffffff",duration:0.45,ease:"back.out(2)"}},{T(52.90)});')
    j(f'tl.to("#mt1 .mtbg",{{opacity:1,duration:0.3}},{T(52.90)});')
    j(f'tl.to("#mt1 small",{{color:"rgba(255,255,255,0.8)",duration:0.3}},{T(52.90)});')
    R.pop('"#mtag"', T(53.44), "{autoAlpha:0,x:-30,scale:0.8}", "{autoAlpha:1,x:0,scale:1}", 0.4, "back.out(2)", "kaching", 0)

    # ---- «пропозиція діє тільки для перших ста експертів»: the count to 100
    m = T(55.00)                       # the cut: «місяця.» | «Пропозиція»
    j(f'tl.to("#months",{{z:-700,autoAlpha:0,duration:0.45,ease:"power2.in"}},{round(m - 0.22, 3)});')
    R.fx(m - 0.22, "whoosh", -4)
    R.show("#hund", round(m + 0.05, 3))
    j(f'tl.fromTo("#hund",{{autoAlpha:0,x:0,y:-40,z:-300,rotationY:-12,rotationX:8,rotationZ:1}},'
      f'{{autoAlpha:1,z:0,duration:0.7,ease:"expo.out",immediateRender:false}},{round(m + 0.05, 3)});')
    j(f'tl.to("#hund",{{z:110,rotationY:-7,duration:{round(T(59.0) - m - 0.75, 3)},ease:"sine.inOut"}},{round(m + 0.75, 3)});')
    j('var cnt={v:0};')
    j(f'tl.fromTo(cnt,{{v:0}},{{v:100,duration:{round(T(57.80) - T(55.50), 3)},ease:"power2.out",immediateRender:false,'
      f'onUpdate:function(){{document.getElementById("hn").textContent=Math.round(cnt.v);}}}},{T(55.50)});')
    R.pop('"#hl"', T(55.70), "{autoAlpha:0,y:24}", "{autoAlpha:1,y:0}", 0.4, "power3.out", None)
    j(f'tl.to("#hn",{{scale:1.08,duration:0.18,yoyo:true,repeat:1,ease:"power2.out"}},{T(57.80)});')
    R.fx(T(57.80), "sparkle"); R.fx(T(57.80), "pop", -3)
    n = T(59.00)
    R.stage_out(n, hide=["#months", "#hund"])

    # ---- her, «психологи, коучі…»: one chip per word, then everyone
    R.push(n, T(68.40), 1.0, 1.05)
    R.show("#nich", T(59.40))
    for i, (lbl, ic, s) in enumerate(NICHES):
        R.pop(f'"#ch{i}"', T(s), "{autoAlpha:0,scale:0.4,y:30}", "{autoAlpha:1,scale:1,y:0}", 0.4,
              "back.out(2.2)", "pop", -6)
    rng = random.Random(9)
    for i, (lbl, ic, x0, y0, rot) in enumerate(EVERYONE):
        t = round(T(65.08) + i * 0.06, 3)
        dx, dy = (x0 - 540) * 0.35, (y0 - 900) * 0.35
        R.pop(f'"#cb{i}"', t, f"{{autoAlpha:0,scale:0.3,x:{-dx:.0f},y:{-dy:.0f},rotation:{rot * 4}}}",
              f"{{autoAlpha:1,scale:1,x:0,y:0,rotation:{rot}}}", 0.45, "back.out(1.8)",
              "pop" if i % 3 == 0 else None, -9)
    R.fx(T(65.10), "sparkle", -3)
    q = T(66.02)
    j(f'tl.to([".chip"],{{autoAlpha:0,scale:0.4,duration:0.3,ease:"power2.in",stagger:0.012}},{q});')
    R.fx(q, "swish", -4)
    R.hide("#nich", round(q + 0.6, 3))

    # ---- «пиши Unlock у коментарях, і побачимося на демо»
    R.push(T(68.66), R.dur, 1.10, 1.14)               # the cut on her: a closer frame
    R.show("#cmt", T(68.80), "flex")
    R.pop('"#cmt"', T(68.82), "{autoAlpha:0,y:60,scale:0.9}", "{autoAlpha:1,y:0,scale:1}", 0.45, "back.out(1.7)", "pop", -4)
    j(f'tl.set("#caret",{{autoAlpha:1}},{T(68.95)});')
    t0, t1 = T(69.18), T(69.62)
    j(f'tl.set("#ph",{{autoAlpha:0}},{t0});')
    for i in range(6):
        t = round(t0 + i * (t1 - t0) / 6, 3)
        j(f'tl.set("#kk{i}",{{autoAlpha:1}},{t});')
        R.fx(t, "click", -2)
    R.click_send = T(70.05)
    j(f'tl.to("#send",{{scale:0.84,duration:0.08,yoyo:true,repeat:1}},{T(70.05)});')
    R.fx(T(70.05), "tap")
    j(f'tl.set("#caret",{{autoAlpha:0}},{T(70.10)});')
    R.pop('"#heart"', T(70.30), "{autoAlpha:0,scale:0.2}", "{autoAlpha:1,scale:1}", 0.45, "back.out(3)", "ping", -6)


def main():
    """`python build.py --window 12 10` writes a 10 s test of the stretch from 12 s; plain builds the reel."""
    motion()
    win = None
    if "--window" in sys.argv:
        i = sys.argv.index("--window")
        win = (float(sys.argv[i + 1]), float(sys.argv[i + 2]))
    R.write(HERE, body(), CSS, title="Nika r01 — «Шукаю 25 експертів»", window=win)


if __name__ == "__main__":
    main()
