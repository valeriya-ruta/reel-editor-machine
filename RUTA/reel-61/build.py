# -*- coding: utf-8 -*-
"""Reel 61 — «Як зробити, щоб АІ-агент нічого не вигадував?». Posts 2026-11-21.
Batch 2026-11-20 (raw 20261120_134413). STYLE.md §00, v3 after her review of v2
(2026-11-23):

  - big text behind her head again («СТРАХ», «SendPulse»)
  - no red handwriting with a thick white halo over her footage
  - far fewer animations: not every phrase gets a graphic («іноді корисно»
    read as cringe / "claude vibes")
  - nothing crowding her head or the top edge: small cards, y 300-560
  - not a tiny blurry screenshot: the two parts of her real SendPulse screen
    that matter («Інструкція для бота», «ВЕБ-ПОШУК»), rebuilt crisp, same labels
  - Excalidraw only for the scheme (half 2); the rest modern Google, a little glass
  - no CTA arrow

Beats: behind «СТРАХ» -> glass DM, the reply struck on «дурницю» -> HALF 1 the
agent settings (field lights on «інструкції», toggle row ringed on «Веб», on at
«Ця кнопка») -> glass search pill «шукає в інтернеті» -> HALF 2 the scheme:
агент -> інтернет struck, агент -> скрипти, a loop on «ніколи» -> behind
«SendPulse» -> glass DM 2: «Не знаю відповіді. Передаю вас менеджеру», a
manager joins -> CTA card.

usage: python3 build.py   (then: sh work/b1021/mattes.sh 61; python3 tools/sfx.py mix 61)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))
from gstyle import G, Words, load_caps  # noqa: E402

NN = "61"
DUR = 68.417           # (2053 plate frames - 0.5) / 30
g = G(dur=DUR, reel=NN)
g.PANEL_TOP = 820      # panel captions: bottom 938, her pushed hair at ≈ 980

FIX = {
    u"Небільше": u"Найбільший", u"страт": u"страх", u"будь": u"будь-яким", u"яким": None,
    u"дурнетю.": u"дурницю.", u"Штукав.": u"штуку.", u"таку": u"такого",
    u"синпуївсь,": u"SendPulse,", u"Туму!": u"Тому", (u"Я", 35.1): u"якщо", (u"ще", 35.3): u"цю",
    u"концюю": None, u"виділяв": u"відійде", u"Сенпульс.": u"SendPulse.", (u"Якщо", 47.9): u"якщо",
    u"Йв": u"І", u"сссссссссссссс": u"все.", (u"Якщо", 60.2): u"якщо", u"пишу": u"пиши",
    u"плюсів": u"плюсик", u"ми...": u"ми", (u"по", 67.6): u"поспілкуємось.", u"спілкуємось.": None,
}
CAPS = load_caps(NN, FIX)
W = Words(CAPS)
S, E = W.s, W.e

B, P, F, C, J = [], [], [], [], []
BLACKOUT, PLACE, HALF = [], [], []


def js(s):
    J.append(s)


P.append(u'<svg class="sk" id="skP" data-layout-allow-occlusion width="1080" height="1240" viewBox="0 0 1080 1240"></svg>')

EXTRA = u'''
    /* a little glass over her footage: frosted white, a hairline rim, a soft cast */
    .glass { position: absolute; border-radius: 36px;
             background: rgba(255,255,255,.62);
             -webkit-backdrop-filter: blur(22px) saturate(1.5); backdrop-filter: blur(22px) saturate(1.5);
             box-shadow: inset 0 1px 0 rgba(255,255,255,.85), inset 0 0 0 1px rgba(255,255,255,.45),
                         0 12px 36px rgba(36,25,25,.16); }
    .dm { left: 150px; top: 300px; width: 780px; padding: 26px 28px; }
    .dm .hd { display: flex; align-items: center; gap: 14px; font-size: 26px; font-weight: 500;
              color: #574142; margin-bottom: 18px; }
    .dm .hd b { width: 40px; height: 40px; border-radius: 50%; background: #7A1424; display: inline-block; }
    .bub { display: inline-block; border-radius: 26px; padding: 16px 24px; font-size: 34px;
           font-weight: 500; line-height: 1.25; position: relative; }
    .bub.in { background: rgba(255,255,255,.92); color: #241919; border-bottom-left-radius: 8px; }
    .bub.me { background: #7A1424; color: #fff; border-bottom-right-radius: 8px; }
    .bub .st { position: absolute; left: 18px; right: 18px; top: 50%; height: 4px; margin-top: -2px;
               border-radius: 2px; background: #fff; transform-origin: 0 50%; transform: scaleX(0); }
    .rowr { display: flex; justify-content: flex-end; margin-top: 14px; }
    .sys { margin-top: 14px; text-align: center; font-size: 26px; color: #574142; }

    /* her real SendPulse agent screen, the two parts that matter, rebuilt crisp */
    .sp { position: absolute; left: 90px; top: 300px; width: 900px; border-radius: 32px; background: #fff;
          border: 2px solid #ECE6E6; padding: 34px 38px; font-family: "Google Sans", sans-serif; }
    .sp .t { font-size: 30px; font-weight: 700; color: #1f1f1f; margin-bottom: 18px; }
    .sp .fld { border: 2px solid #D9D9D9; border-radius: 16px; padding: 18px 22px; font-size: 27px;
               line-height: 1.5; color: #5f5f5f; height: 186px; transition: none; }
    .sp .web { margin-top: 26px; display: flex; align-items: center; gap: 22px; background: #F7F7F8;
               border-radius: 20px; padding: 22px 26px; }
    .sp .ic { width: 58px; height: 58px; border-radius: 50%; background: #DDEBFB; flex: none; }
    .sp .wt { flex: 1; }
    .sp .wt b { display: block; font-size: 24px; letter-spacing: .06em; color: #1f1f1f; }
    .sp .wt span { font-size: 24px; color: #5f5f5f; }
    .sp .sw { width: 70px; height: 38px; border-radius: 19px; background: #C9C9C9; position: relative; flex: none; }
    .sp .sw i { position: absolute; left: 4px; top: 4px; width: 30px; height: 30px; border-radius: 50%;
                background: #fff; box-shadow: 0 1px 3px rgba(0,0,0,.25); }

    .search { left: 150px; top: 330px; width: 780px; height: 108px; border-radius: 54px; padding: 0 36px;
              display: flex; align-items: center; gap: 22px; font-size: 36px; color: #241919; }
    .gdots { display: flex; gap: 10px; margin-left: auto; }
    .gdots i { width: 14px; height: 14px; border-radius: 50%; background: #7A1424; display: block; }
    /* her note on v4: the 3-row card cut her forehead on the last clip — one row, ends ≈ y 500 */
    .cta { left: 100px; top: 290px; width: 880px; padding: 24px 24px; display: flex; flex-direction: column;
           align-items: center; gap: 16px; }
'''

# 1 · BEHIND — «СТРАХ» ----------------------------------------------------------
t_strakh, e_strakh = S(u"страх", 0.75), E(u"страх", 0.75)
B.append(u'        <div id="bw1" class="big hid" data-layout-allow-occlusion style="top:430px; font-size:250px">СТРАХ</div>')
g.matte("b1", 0.3, round(S(u"який", 2.61) + 0.6 - 0.3, 3))
js(u'  rise("#bw1", %.3f); sink("#bw1", %.3f);' % (t_strakh - 0.25, S(u"який", 2.61) + 0.1))
g.sfx("whoosh-short", t_strakh - 0.25)
BLACKOUT.append((t_strakh - 0.03, e_strakh))

# 2 · ABOVE — a glass DM: the reply is made up ----------------------------------
t_prydum, t_durn, t_skladno = S(u"придумає", 5.45), S(u"дурницю.", 7.39), S(u"складно", 8.97)
F.append(u'''
        <div id="d1" class="glass dm hid">
          <div class="hd"><b></b>Direct · AI-агент</div>
          <div><span class="bub in">Скільки коштує і коли можна почати?</span></div>
          <div class="rowr"><span class="bub me hid" id="d1a">Звісно! Усе безкоштовно, почнемо вчора<i class="st"></i></span></div>
        </div>''')
js(u'''
  rise("#d1", %.3f);
  pop("#d1a", %.3f);
  tl.fromTo("#d1a .st", {scaleX: 0}, X({scaleX: 1, duration: .35, ease: "power2.out"}), %.3f);
  tl.to("#d1a", {keyframes: {x: [0, -8, 7, -4, 2, 0]}, duration: .35, ease: "none"}, %.3f);
  sink("#d1", %.3f);
''' % (S(u"сам", 2.79), t_prydum, t_durn, t_durn, t_skladno + 0.2))
g.sfx("pop", S(u"сам", 2.79)); g.sfx("notification", t_prydum); g.sfx("click", t_durn)

# 3 · FULL — her SendPulse agent screen as a platform-ad sequence ---------------
# Her note 2026-11-23: "instead of keeping the screenshot super tiny, you could
# have done full screen and showed all the parts animated, like in a platform ad
# (the 3d angles smooth zoom ins sorta thing)". Her screenshot is 793 px wide —
# a 2-3x zoom would blur it — so the screen is rebuilt 1:1 in HTML (same layout,
# labels, text; coordinates are the screenshot's own pixels) and stays crisp.
f0 = S(u"Коли", 12.27) - 0.15
f1 = E(u"інформацію.", 26.94) + 0.25
C.append(u"""
        <div id="stage">
          <div id="win">
            <div class="sp-t" style="left:18px;top:12px">Main AI Agent <span style="color:#9aa0a6">✎</span></div>
            <div class="sp-x" style="left:756px;top:10px">×</div>
            <div class="sp-l" style="left:18px;top:48px">Інструкція для бота</div>
            <div id="fld" class="sp-box" style="left:18px;top:68px;width:442px;height:172px;padding:8px 10px;line-height:1.45">
              You are a helpful assistant.<br>User name:&nbsp; {{full_name}}<br>Current date:&nbsp; {{$current_datetime}}</div>
            <div class="sp-l" style="left:18px;top:254px">Встановити цілі як умови виходу</div>
            <div class="sp-a" style="left:18px;top:272px">Додати умову</div>
            <div class="sp-l" style="left:482px;top:48px">Модель</div>
            <div class="sp-box sp-sel" style="left:482px;top:68px;width:293px;height:27px">GPT-6 Luna</div>
            <div class="sp-l" style="left:482px;top:104px">Ключ API</div>
            <div class="sp-box sp-sel" style="left:482px;top:124px;width:293px;height:27px">Наслідувати з налаштувань облікового запису</div>
            <div id="cw" class="sp-card" style="left:482px;top:168px"><i style="background:#DDEBFB"></i><b>ВЕБ-ПОШУК</b>
              <span>Пошук актуальної інформації в інтернеті перед формуванням відповіді.</span><em id="tg"><u></u></em></div>
            <div class="sp-card" style="left:482px;top:236px"><i style="background:#ECEFF3"></i><b>СЕРВЕРИ MCP</b>
              <span>Підключення сторонніх інструментів і джерел даних.</span><em><u></u></em></div>
            <div class="sp-card" style="left:482px;top:304px"><i style="background:#E3F5EA"></i><b>ПОШУК У ФАЙЛАХ</b>
              <span>Формування відповіді на основі ваших завантажених файлів.</span><em><u></u></em></div>
            <div class="sp-l" style="left:482px;top:382px">Обсяг контексту переписки</div>
            <div class="sp-box" style="left:482px;top:400px;width:64px;height:28px;padding:5px 8px">10</div>
            <div class="sp-s" style="left:482px;top:434px;width:200px">попередніх повідомлень підписника та бота</div>
            <div class="sp-l" style="left:688px;top:382px;width:90px">Рівень міркувань</div>
            <div class="sp-box sp-sel" style="left:688px;top:416px;width:86px;height:27px">None</div>
            <div class="sp-btn" style="left:614px;top:496px;width:72px;background:#E8EAED;color:#3c4043">Скасувати</div>
            <div class="sp-btn" style="left:692px;top:496px;width:84px;background:#1EA672;color:#fff">Застосувати</div>
          </div>
        </div>""")
EXTRA += u"""
    #cover { background: radial-gradient(120% 80% at 50% 35%, #FFFFFF 0%, #F6EFEF 70%, #F1E7E7 100%); }
    #stage { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; perspective: 2200px; }
    #win { position: absolute; left: 0; top: 0; width: 793px; height: 541px; background: #fff;
           border-radius: 14px; font-family: "Google Sans", sans-serif; color: #1f1f1f;
           box-shadow: 0 2px 6px rgba(36,25,25,.10), 0 30px 80px rgba(36,25,25,.22);
           transform-origin: 0 0; will-change: transform; }
    #win > div { position: absolute; }
    .sp-t { font-size: 15px; font-weight: 700; } .sp-x { font-size: 18px; color: #5f6368; }
    .sp-l { font-size: 12px; font-weight: 700; } .sp-a { font-size: 12px; color: #1a73e8; border-bottom: 1px dashed #1a73e8; }
    .sp-s { font-size: 10px; color: #5f6368; line-height: 1.35; }
    .sp-box { border: 1px solid #D9D9D9; border-radius: 6px; font-size: 12px; color: #5f6368; background: #fff;
              padding: 5px 9px; overflow: hidden; white-space: nowrap; }
    .sp-sel::after { content: "⌄"; position: absolute; right: 8px; top: 2px; color: #5f6368; }
    .sp-card { width: 293px; height: 62px; background: #F6F7F9; border-radius: 8px; }
    .sp-card i { position: absolute; left: 12px; top: 12px; width: 26px; height: 26px; border-radius: 50%; }
    .sp-card b { position: absolute; left: 48px; top: 10px; font-size: 9.5px; letter-spacing: .04em; }
    .sp-card span { position: absolute; left: 48px; top: 24px; width: 200px; font-size: 9.5px; color: #5f6368; line-height: 1.3; }
    .sp-card em { position: absolute; left: 256px; top: 12px; width: 26px; height: 13px; border-radius: 7px; background: #C4C7C5; }
    .sp-card em u { position: absolute; left: 1px; top: 1px; width: 11px; height: 11px; border-radius: 50%; background: #fff; }
    .sp-btn { height: 26px; border-radius: 6px; font-size: 11px; font-weight: 500; text-align: center; line-height: 26px; }
"""
t_pole, t_instr, t_knopka = S(u"поле,", 15.62), S(u"інструкції", 17.14), S(u"кнопка", 19.17)
t_tsia, t_vyity = S(u"Ця", 22.48), S(u"вийти", 24.92)
# camera: screen = (0,0) + p*s + (x,y). Wide shows the whole window; zooms centre
# a point of the window at (540, 760). Field centre (239,154); web card (628,199).
def cam(px, py, sc, cx=540, cy=730):
    # the window turns and scales about its own centre (396, 270): a point p of
    # it lands at O + s*(p - O) + (x, y)
    return (round(cx - 396 - sc * (px - 396), 1), round(cy - 270 - sc * (py - 270), 1))
WIDE = (1.24,) + cam(396, 270, 1.24)
FLD = (2.15,) + cam(239, 154, 2.15)
WEB = (3.0,) + cam(628, 199, 3.0)
js(u"""
  gsap.set("#win", {transformOrigin: "396px 270px"});
  gsap.set("#win", {x: %(wx)s, y: %(wy)s + 220, scale: %(ws)s * .86, rotationX: 24, rotationY: -20, rotationZ: 5});
  tl.to("#win", {x: %(wx)s, y: %(wy)s, scale: %(ws)s, rotationX: 9, rotationY: -12, rotationZ: 2, duration: 1.3, ease: "power3.out"}, %(f0)s + .15);
  tl.to("#win", {rotationX: 6, rotationY: -7, rotationZ: 1, duration: 1.9, ease: "sine.inOut"}, %(f0)s + 1.45);
  tl.to("#win", {x: %(fx)s, y: %(fy)s, scale: %(fs)s, rotationX: 3, rotationY: 6, rotationZ: 0, duration: 1.2, ease: "power3.inOut"}, %(pole)s - .5);
  tl.to("#fld", {borderColor: "#7A1424", boxShadow: "0 0 0 3px rgba(122,20,36,.16)", duration: .3}, %(instr)s);
  tl.to("#win", {x: %(bx)s, y: %(by)s, scale: %(bs)s, rotationX: -2, rotationY: -8, duration: 1.3, ease: "power3.inOut"}, %(knop)s - .45);
  tl.to("#tg", {backgroundColor: "#1EA672", duration: .2}, %(tsia)s);
  tl.to("#tg u", {x: 13, duration: .3, ease: "back.out(2)"}, %(tsia)s);
  tl.fromTo("#cw", {boxShadow: "0 0 0 0 rgba(30,166,114,.0)"}, X({boxShadow: "0 0 0 6px rgba(30,166,114,.25)", duration: .35, yoyo: true, repeat: 1}), %(tsia)s + .1);
  tl.to("#win", {x: %(wx)s, y: %(wy)s, scale: %(ws)s, rotationX: 10, rotationY: 14, rotationZ: -2, duration: 1.4, ease: "power3.inOut"}, %(vyity)s - .4);
  full(%(f0)s, %(f1)s);
""" % {"wx": WIDE[1], "wy": WIDE[2], "ws": WIDE[0], "fx": FLD[1], "fy": FLD[2], "fs": FLD[0],
       "bx": WEB[1], "by": WEB[2], "bs": WEB[0], "f0": "%.3f" % f0, "f1": "%.3f" % f1,
       "pole": "%.3f" % t_pole, "instr": "%.3f" % t_instr, "knop": "%.3f" % t_knopka,
       "tsia": "%.3f" % t_tsia, "vyity": "%.3f" % t_vyity})
g.sfx("whoosh-short", f0); g.sfx("whoosh-short", t_pole - 0.5); g.sfx("whoosh-short", t_knopka - 0.45)
g.sfx("click", t_tsia); g.sfx("whoosh-short", t_vyity - 0.4); g.sfx("whoosh-short", f1)

# 5 · HALF 2 — the scheme (Excalidraw): no web, only scripts ----------------------
k0 = S(u"Тому", 34.43) - 0.1
k1 = E(u"інструкції.", 41.47) + 0.3
HALF.append((k0, k1))
t_vmyk, t_propys, t_nikoly = S(u"вмикати,", 36.96), S(u"прописати", 38.60), S(u"ніколи", 40.33)
js(u'''
  sketch("s1", "skP"); box("s1", 380, 330, 320, 130, {seed: 3, fill: true});
  label("s1", 540, 412, "агент", {size: 58});
  draw("s1", %.3f);
  sketch("s2", "skP"); arrow("s2", 380, 420, 190, 620, {seed: 5, bend: -.15});
  box("s2", 60, 630, 280, 120, {seed: 7}); label("s2", 200, 706, "інтернет", {size: 50});
  draw("s2", %.3f);
  sketch("s3", "skP"); ln("s3", 70, 600, 330, 770, {stroke: "#7A1424", strokeWidth: 7, seed: 9});
  ln("s3", 70, 770, 330, 600, {stroke: "#7A1424", strokeWidth: 7, seed: 13});
  draw("s3", %.3f, .3);
  sketch("s4", "skP"); arrow("s4", 700, 420, 880, 620, {seed: 15, bend: .15});
  box("s4", 730, 630, 290, 120, {seed: 17, fill: true}); label("s4", 875, 706, "скрипти", {size: 50});
  draw("s4", %.3f);
  sketch("s5", "skP"); ell("s5", 700, 560, 760, 470, {seed: 19, stroke: "#7A1424", strokeWidth: 6, fill: false});
  draw("s5", %.3f, .7);
  erase("s1", %.3f); erase("s2", %.3f); erase("s3", %.3f); erase("s4", %.3f); erase("s5", %.3f);
''' % (k0 + 0.6, k0 + 1.4, t_vmyk - 0.1, t_propys - 0.3, t_nikoly - 0.1, k1, k1, k1, k1, k1))
g.sfx("whoosh-short", k0); g.sfx("click", t_vmyk); g.sfx("click-soft", t_propys)

# 6 · BEHIND — «SendPulse» ----------------------------------------------------------
t_sp, e_sp = S(u"SendPulse.", 46.38), E(u"SendPulse.", 46.38)
B.append(u'        <div id="bw2" class="big hid" data-layout-allow-occlusion style="top:440px; font-size:200px">SendPulse</div>')
g.matte("b2", round(t_sp - 0.6, 3), round(e_sp - t_sp + 1.2, 3))
js(u'  rise("#bw2", %.3f); sink("#bw2", %.3f);' % (t_sp - 0.35, e_sp + 0.3))
g.sfx("whoosh-short", t_sp - 0.35)
BLACKOUT.append((t_sp - 0.03, e_sp))

# 7 · ABOVE — the glass DM again: it doesn't know -> a manager --------------------
t_pyt, t_skazhe, t_men, t_mozhe = S(u"питання,", 48.48), S(u"скаже,", 53.44), S(u"менеджеру.", 55.58), S(u"може.", 59.59)
F.append(u'''
        <div id="d2" class="glass dm hid">
          <div class="hd"><b></b>Direct · AI-агент</div>
          <div><span class="bub in">А ви робите доставку в Канаду?</span></div>
          <div class="rowr"><span class="bub me hid" id="d2a">Не знаю відповіді. Передаю вас менеджеру</span></div>
          <div class="sys hid" id="d2s">Менеджерка приєдналась до чату</div>
        </div>''')
js(u'''
  rise("#d2", %.3f);
  pop("#d2a", %.3f);
  fadein("#d2s", %.3f);
  sink("#d2", %.3f);
''' % (t_pyt - 0.3, t_skazhe, t_men, t_mozhe + 0.2))
g.sfx("pop", t_pyt - 0.3); g.sfx("notification", t_skazhe); g.sfx("ping", t_men)

# 8 · CTA — who it is for, «Пиши + в коментарях» -------------------------------------
t_mal, t_pyshy = S(u"малий", 60.76), S(u"пиши", 65.80)
F.append(u'''
        <div id="ct" class="glass cta hid">
          <div class="chips" style="justify-content:center; flex-wrap:nowrap; gap:12px">
            <span class="chip" style="font-size:30px; padding:10px 18px"><i></i>малий і середній бізнес</span>
            <span class="chip" style="font-size:30px; padding:10px 18px"><i></i>команда</span>
            <span class="chip" style="font-size:30px; padding:10px 18px"><i></i>багато заявок</span>
          </div>
          <div id="ctp" class="pill hid" style="position:relative; font-size:40px; padding:22px 46px">Пиши + в коментарях</div>
        </div>''')
js(u'''
  rise("#ct", %.3f);
  pop("#ctp", %.3f);
''' % (t_mal - 0.1, t_pyshy - 0.1))
g.sfx("pop", t_mal); g.sfx("pop", t_pyshy)
BLACKOUT.append((t_pyshy - 0.05, DUR))

# ---------------------------------------------------------------- half screens + their mattes
for i, (a, b) in enumerate(HALF):
    g.matte("half2", round(a - 0.1, 3), round(b - a + 1.2, 3))     # the scheme (its cut-out was made as half2)
    js("  half(%.3f, %.3f);" % (a, b))
    PLACE.append((a + 0.4, b + 0.2, "bottom", 938))


def main():
    chunks = g.chunks(CAPS, place=PLACE)
    doc = g.document(title=u"Reel 61 — агент нічого не вигадує", plate="assets/base.mp4",
                     behind="\n".join(B), panel="\n".join(P), front="\n".join(F), cover="\n".join(C),
                     js="\n".join(J), chunks=chunks, blackout=BLACKOUT, extra_css=EXTRA)
    g.write(HERE, doc)
    print("index.html  %d caption chunks, %d sfx cues, %d mattes" % (len(chunks), len(g.cues), len(g.mattes)))


main()
