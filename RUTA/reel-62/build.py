# -*- coding: utf-8 -*-
"""Reel 62 — «Які налаштування є в АІ-агентах SendPulse і які з них справді важливі?»
Batch 2026-11-20 (raw 20261120_134603). STYLE.md §00 + her review of reel 61
(2026-11-23): natural editing, one meaningful moment per sentence group, big
text behind her, her real SendPulse screen as a full-screen platform-ad
sequence (rebuilt 1:1 from app-screenshots/sendpulse-ai-agent-settings.png,
the same rebuild as reel-61's #win), Excalidraw only for the scheme, shuffle
for lists, CTA pill in the subtitle band, no arrows.

Chain: behind «AI-агент» (cover) -> shuffle: what the agent does -> FULL 1 the
settings window flies in, on «два» the instruction field and the token limit
light up, the rest goes grey on «забити» -> FULL 2 inside the instruction field
the three things she puts there type in; the camera swings to «Модель», the
list opens, Haiku is picked on its word -> card Sonnet | Haiku, «×3–4» on
«дорожче», «=» on «різниці … не побачила» -> FULL 3 «ПОШУК У ФАЙЛАХ» goes grey
on «пропустити», the camera swings back to the instruction field -> behind
«Токени» -> HALF the scheme: a token budget = думає + відповідь; at 500 думає
eats it all and the reply is struck -> FULL 4 the token field 500 -> 2000 ->
card: «Пиши коротко.» typed into the instruction, then twice more -> glass DM,
the agent's reply keeps growing -> CTA shuffle + «Став + в коментарях».

Reel 61 is the sibling: same window, different beats (61 zoomed the field and
switched ВЕБ-ПОШУК on; 62 never touches the web toggle).

usage: python3 build.py   (then: python3 tools/sfx.py mix 62; sh work/b1021/mattes.sh 62)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))
from gstyle import G, Words, load_caps  # noqa: E402

NN = "62"
DUR = 116.016          # (3481 plate frames - 0.5) / 30
g = G(dur=DUR, reel=NN)
g.PANEL_TOP = 820      # panel captions: bottom 938, her pushed hair at ≈ 980

# whisper's token -> what she said (re-heard on the plate where unsure)
FIX = {
    u"пульс,": u"SendPulse,", u"Дирекції.": u"діректі,", u"спілкується": u"Спілкується",
    (u"І ось", 6.9): u"Із", (u"з усіх", 7.2): u"усіх", u"налаштовань,": u"налаштувань,",
    (u"там,", 8.3): u"там", u"важлива": u"важливі", u"Просто": u"просто",
    u"це звичайно,": u"це, звичайно,", u"ліміту…": u"ліміту,", (u"У", 16.5): u"по",
    u"суті,": u"суті", u"я не": None, u"маю.": u"немає.",
    u"і челюбова": u"і цільова", u"контекст,": u"контекст", u"обирати": u"обирати,",
    u"закономиш": u"зекономиш.", (u"я", 35.1): u"Я", u"Сонеті": u"Sonnet", u"Хайку.": u"Haiku.",
    u"дорожче": u"дорожче,", u"побачила": u"побачила.", u"Завантаження": u"завантаження",
    (u"інструкції.", 50.2): u"інструкції,", u"Токені.": u"Токени.", u"Здається": u"здається",
    u"пише": u"пише,", u"токінів": u"токенів", (u"і якщо", 68.9): u"якщо",
    u"в максимум.": u"в максимум,", (u"в інструкції,", 89.4): u"в інструкції.",
    u"здогадається.": u"здогадається,", u"Великі!": u"великі,", (u"Тому", 99.9): u"Тому,",
    (u"Якщо", 100.1): u"якщо", u"справляється.": u"справляється,", u"Купи": u"купа",
    u"гугляться": u"губляться", (u"саме", 83.1): u"це", (u"ж", 83.3): u"майже",
    u"не впливає.": u"не впливає", (u"ваш", 84.1): u"вартість.", (u"тість.", 84.3): None, u"відповіді": u"відповіді,", u"ставь": u"став", u"вдові": u"в тебе", (u"що вони", 107.1): u"вони",
    u"налаштувати.": u"налаштувати,", (u"і", 106.3): u"І", (u"5", 27.9): u"5.5,", (u".5.", 28.4): None,
}
FIX.update(globals().get("FIX_HEARD", {}))
CAPS = load_caps(NN, FIX)
W = Words(CAPS)
S, E = W.s, W.e
g.cta_start = S(u"Тому,", 99.9)    # «Тому, якщо в тебе ще немає менеджера…» — no meme from here on

B, P, F, C, J = [], [], [], [], []
BLACKOUT, PLACE, HALF = [], [], []


def js(s):
    J.append(s)


P.append(u'<svg class="sk" id="skP" data-layout-allow-occlusion width="1080" height="1240" viewBox="0 0 1080 1240"></svg>')

EXTRA = u'''
    .dm { left: 130px; width: 820px; padding: 18px 22px; bottom: 1372px; }   /* bottom y 548: clear of her hair (≈ 600 here) */
    .bub { display: inline-block; border-radius: 26px; padding: 12px 20px; font-size: 27px;
           font-weight: 500; line-height: 1.3; position: relative; max-width: 720px; }
    .bub.in { background: rgba(255,255,255,.92); color: #241919; border-bottom-left-radius: 8px; }
    .bub.me { background: #7A1424; color: #fff; border-bottom-right-radius: 8px; }
    .rowr { display: flex; justify-content: flex-end; margin-top: 12px; }
    .bub .gl { display: block; overflow: hidden; }

    /* Sonnet | Haiku: two names, the price multiple she says, an equals sign */
    .cmp { left: 0; right: 0; margin: auto; width: 700px; top: 310px; padding: 30px 40px 34px;
           display: flex; align-items: flex-start; justify-content: space-between; }
    .cmp .m { width: 250px; text-align: center; }
    .cmp .m b { display: block; font-size: 54px; font-weight: 700; letter-spacing: -0.02em; color: #241919; }
    .cmp .m span { display: block; font-size: 26px; font-weight: 500; color: #574142; margin-bottom: 6px; }
    .cmp .x { display: inline-block; margin-top: 18px; background: #7A1424; color: #fff; border-radius: 999px;
              padding: 8px 24px; font-size: 38px; font-weight: 700; }
    .cmp .eq { font-size: 96px; font-weight: 700; color: #7A1424; line-height: 1; margin-top: 24px; }

    /* her instruction, typed: «Пиши коротко.» */
    .ins { left: 0; right: 0; margin: auto; width: 680px; top: 290px; padding: 24px 30px; }
    .ins .t { font-size: 26px; font-weight: 700; color: #1f1f1f; margin-bottom: 14px; }
    .ins .f { border: 2px solid #D9D9D9; border-radius: 16px; padding: 12px 20px; font-size: 30px;
              line-height: 1.38; color: #241919; height: 146px; }   /* card bottom ≈ y 540, her hair ≈ 600 */
    .ins .f div { white-space: nowrap; overflow: hidden; }
'''

# 1 · BEHIND — «AI-агент», the cover frame -------------------------------------
# (her note on 61: «AI-агент» attracts — it is the hook and the cover)
t_ai, e_ai = S(u"AI-агента", 1.43), E(u"AI-агента", 1.43)
t_yakyi = S(u"який", 2.69)
B.append(u'        <div id="bw1" class="big" data-layout-allow-occlusion style="top:450px; font-size:210px">AI-агент</div>')
g.matte("b1", 0.0, round(t_yakyi + 0.6, 3))
js(u'  sink("#bw1", %.3f);' % (t_yakyi + 0.2))
BLACKOUT.append((t_ai - 0.03, e_ai))

# 2 · ABOVE — what the agent does, one card at a time ---------------------------
SH1 = [(u"кваліфікує людей", S(u"кваліфікує", 3.19) - 0.1),
       (u"спілкується", S(u"Спілкується", 4.64) - 0.1),
       (u"доводить до продажу", S(u"доводить", 5.80) - 0.1)]
for i, (txt, _) in enumerate(SH1):
    F.append(u'        <div id="sa%d" class="shuf hid"><span class="chip"><i></i>%s</span></div>' % (i, txt))
    g.sfx("pop", SH1[i][1])
js(u'  shuffle([%s], [%s], %.3f);' % (", ".join('"#sa%d"' % i for i in range(len(SH1))),
                                      ", ".join("%.3f" % t for _, t in SH1), E(u"продажу.", 6.42) + 0.15))

# 3 · FULL — her SendPulse agent screen, the same labels and text as
# app-screenshots/sendpulse-ai-agent-settings.png, laid out as a portrait version of it
# (the coordinator's full-screen bar, 2026-11-23): 972 px wide = 90 % of the frame at
# scale 1, labels 26 px, body 30 px, so the wide shot reads without a zoom and nothing
# is cropped at the sides unless the camera zooms into one element on purpose.
# Four visits to one window: the overview («важливі тільки два»), the field and the model
# list, the files card, the token limit. The token field is NOT on her screenshot (her
# screen shows «Обсяг контексту» / «Рівень міркувань»): it is added in her settings'
# wording, with only the numbers she says (500, 2000).
C.append(u"""
        <div id="stage">
          <div id="win">
            <div class="sp-t o" style="left:36px;top:34px">Main AI Agent <span style="color:#9aa0a6">✎</span></div>
            <div class="sp-x o" style="left:912px;top:20px">×</div>
            <div class="sp-l" style="left:36px;top:92px">Інструкція для бота</div>
            <div id="fld" class="sp-box" style="left:36px;top:130px;width:900px;height:292px;padding:12px 18px;line-height:1.42;white-space:normal;color:#5f6368">
              You are a helpful assistant.<br>User name:&nbsp; {{full_name}}<br>Current date:&nbsp; {{$current_datetime}}
              <div class="ty"><b>Скрипт:</b> привітайся, дізнайся запит, запропонуй дзвінок<br><b>Цільова аудиторія:</b> власниці малого бізнесу<br><b>Контекст:</b> послуги, ціни, умови, часті питання</div>
              <i class="tc" id="ty1" style="top:140px"></i><i class="tc" id="ty2" style="top:184px"></i><i class="tc" id="ty3" style="top:228px"></i></div>
            <div class="sp-l o" style="left:36px;top:432px;width:420px">Встановити цілі як умови виходу</div>
            <div class="sp-a o" style="left:36px;top:502px">Додати умову</div>
            <div class="sp-l" id="tokl" style="left:36px;top:578px;width:420px">Максимальна кількість токенів</div>
            <div id="tok" class="sp-box" style="left:36px;top:624px;width:170px;height:62px;padding:0 18px;line-height:58px;color:#1f1f1f">
              <span id="tk5">500</span><span id="tk2">2000</span></div>
            <div class="sp-s" id="toks" style="left:226px;top:626px;width:230px">на одну відповідь бота</div>
            <div class="sp-l o" style="left:36px;top:716px">Рівень міркувань</div>
            <div class="sp-box sp-sel o" style="left:36px;top:762px;width:220px;height:62px;padding:0 18px;line-height:58px">None</div>
            <div class="sp-l o" style="left:36px;top:850px;width:420px">Обсяг контексту переписки</div>
            <div class="sp-box o" style="left:36px;top:896px;width:110px;height:62px;padding:0 18px;line-height:58px">10</div>
            <div class="sp-s o" style="left:36px;top:972px;width:420px">попередніх повідомлень підписника та бота</div>
            <div class="sp-btn o" style="left:36px;top:1070px;width:200px;background:#E8EAED;color:#3c4043">Скасувати</div>
            <div class="sp-btn o" style="left:252px;top:1070px;width:220px;background:#1EA672;color:#fff">Застосувати</div>
            <div class="sp-l o2" style="left:486px;top:432px">Модель</div>
            <div id="sel" class="sp-box sp-sel o2" style="left:486px;top:478px;width:450px;height:62px;padding:0 18px;line-height:58px">
              <span id="sv1">GPT-6 Luna</span><span id="sv2">%(HAIKU)s</span></div>
            <div id="kl" class="sp-l o" style="left:486px;top:552px">Ключ API</div>
            <div id="kv" class="sp-box sp-sel o" style="left:486px;top:600px;width:450px;height:62px;padding:0 18px;line-height:58px">Наслідувати з налашт…</div>
            <div id="cw" class="sp-card o" style="left:486px;top:684px"><i style="background:#DDEBFB"></i><b>ВЕБ-ПОШУК</b>
              <span>Пошук актуальної інформації в інтернеті перед формуванням відповіді.</span><em><u></u></em></div>
            <div class="sp-card o" style="left:486px;top:864px"><i style="background:#ECEFF3"></i><b>СЕРВЕРИ MCP</b>
              <span>Підключення сторонніх інструментів і джерел даних.</span><em><u></u></em></div>
            <div id="fc" class="sp-card o" style="left:486px;top:1044px"><i style="background:#E3F5EA"></i><b>ПОШУК У ФАЙЛАХ</b>
              <span>Формування відповіді на основі ваших завантажених файлів.</span><em><u></u></em></div>
            <div id="dd">
              <div class="op">GPT-6 Luna</div><div class="op">Claude Sonnet</div><div class="op" id="opH">%(HAIKU)s</div></div>
          </div>
        </div>""" % {"HAIKU": u"Claude Haiku"})
EXTRA += u"""
    #cover { background: radial-gradient(120% 80% at 50% 35%, #FFFFFF 0%, #F6EFEF 70%, #F1E7E7 100%); }
    #stage { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; perspective: 2200px; }
    #win { position: absolute; left: 0; top: 0; width: 972px; height: 1234px; background: #fff;
           border-radius: 28px; font-family: "Google Sans", sans-serif; color: #1f1f1f;
           box-shadow: 0 2px 8px rgba(36,25,25,.10), 0 30px 80px rgba(36,25,25,.22);
           transform-origin: 0 0; will-change: transform; }
    #win > div { position: absolute; }
    .sp-t { font-size: 38px; font-weight: 700; } .sp-x { font-size: 44px; color: #5f6368; }
    .sp-l { font-size: 26px; font-weight: 700; line-height: 1.3; }
    .sp-a { font-size: 30px; color: #1a73e8; border-bottom: 2px dashed #1a73e8; }
    .sp-s { font-size: 26px; color: #5f6368; line-height: 1.3; }
    .sp-box { border: 2px solid #D9D9D9; border-radius: 12px; font-size: 30px; color: #5f6368; background: #fff;
              overflow: hidden; white-space: nowrap; box-sizing: border-box; }
    .sp-sel::after { content: "⌄"; position: absolute; right: 18px; top: -6px; color: #5f6368; font-size: 32px; }
    .sp-card { width: 450px; height: 174px; background: #F6F7F9; border-radius: 16px; }
    .sp-card i { position: absolute; left: 18px; top: 18px; width: 48px; height: 48px; border-radius: 50%; }
    .sp-card b { position: absolute; left: 80px; top: 28px; font-size: 26px; letter-spacing: .03em; }
    .sp-card span { position: absolute; left: 18px; top: 74px; width: 414px; font-size: 26px; color: #5f6368; line-height: 1.25; }
    .sp-card em { position: absolute; left: 376px; top: 20px; width: 56px; height: 28px; border-radius: 14px; background: #C4C7C5; }
    .sp-card em u { position: absolute; left: 3px; top: 3px; width: 22px; height: 22px; border-radius: 50%; background: #fff; }
    .sp-btn { height: 64px; border-radius: 12px; font-size: 30px; font-weight: 500; text-align: center; line-height: 64px; }
    /* the three typed lines are ONE text block (no stacked line boxes to collide under the 3D
       tilt); each line is revealed by an empty white cover shrinking off it to the right */
    #fld .ty { line-height: 44px; color: #1f1f1f; white-space: nowrap; }
    #fld .tc { position: absolute; left: 2px; right: 2px; height: 44px; background: #fff; transform-origin: 100% 50%; }
    #fld .ty b { font-weight: 700; }
    #tok span { position: absolute; left: 18px; top: 0; }
    #tk2 { opacity: 0; }
    #sel span { position: absolute; left: 18px; top: 0; } #sv2 { opacity: 0; color: #1f1f1f; }
    #dd { left: 486px; top: 546px; width: 450px; background: #fff; border-radius: 12px; padding: 8px 0;
          box-shadow: 0 2px 6px rgba(0,0,0,.12), 0 8px 24px rgba(0,0,0,.14); transform-origin: 50% 0;
          opacity: 0; visibility: hidden; z-index: 5; }
    #dd .op { position: relative; height: 60px; line-height: 60px; padding: 0 20px; font-size: 30px; color: #1f1f1f; }
"""

OX, OY = 486, 617      # the window's own centre: it turns and scales about it


def cam(px, py, sc, cx=540, cy=760):
    # a point p of the window lands at O + s*(p - O) + (x, y); this centres p on (cx, cy)
    return (round(cx - OX - sc * (px - OX), 1), round(cy - OY - sc * (py - OY), 1))


def V(name, px, py, sc, cy=760, dy=0, **rot):
    x, y = cam(px, py, sc, cy=cy)
    o = {"x": x, "y": round(y + dy, 1), "scale": sc, "rotationX": 0, "rotationY": 0, "rotationZ": 0}
    o.update(rot)
    o["rotationZ"] = 0      # no roll: long UI rows stay level (and their boxes never touch)
    return "{%s}" % ", ".join("%s: %s" % (k, v) for k, v in o.items())


# wide: the whole window, 972 px of 1080, y 236-1470
WIDE = lambda sc=1.0, **r: V("wide", OX, OY, sc, cy=845, **r)     # noqa: E731
FLD = lambda sc=1.06, **r: V("fld", 486, 300, sc, cy=680, **r)     # noqa: E731  the field, whole width (its text uncut)
MOD = lambda sc=1.7, **r: V("mod", 711, 590, sc, **r)             # noqa: E731  the select + its open list
FIL = lambda sc=1.6, **r: V("fil", 711, 1000, sc, cy=900, **r)           # noqa: E731  ПОШУК У ФАЙЛАХ
TOK = lambda sc=2.0, **r: V("tok", 250, 640, sc, **r)             # noqa: E731  the token field + its label

js(u'  gsap.set("#win", {transformOrigin: "%dpx %dpx"});' % (OX, OY))

RING = u'boxShadow: "0 0 0 3px rgba(122,20,36,.85), 0 0 0 9px rgba(122,20,36,.14)", borderColor: "#7A1424"'
UNRING = u'boxShadow: "0 0 0 0px rgba(122,20,36,0), 0 0 0 0px rgba(122,20,36,0)", borderColor: "#D9D9D9"'

# FULL 1 — the overview: of all of it, only two matter ------------------------
t_nal, t_dva, t_zab = S(u"налаштувань,", 7.68), S(u"два.", 10.04), S(u"забити.", 12.11)
a0, a1 = t_nal - 0.55, E(u"забити.", 12.11) + 0.12
js(u"""
  tl.set("#win", %(w0)s, %(a0).3f);
  tl.to("#win", %(w1)s, %(a0).3f + .15);
  tl.to("#win", %(w2)s, %(a0).3f + 1.45);
  tl.to(["#fld", "#tok"], {%(ring)s, duration: .3}, %(dva).3f);
  tl.to(".o, .o2, #toks", {opacity: .28, duration: .5}, %(zab).3f - .25);
  full(%(a0).3f, %(a1).3f);
""" % {"w0": WIDE(sc=0.86, dy=240, rotationX=18, rotationY=-14, rotationZ=3),
       "w1": WIDE(rotationX=5, rotationY=-6, rotationZ=1)[:-1] + ", duration: 1.3, ease: \"power3.out\"}",
       "w2": WIDE(sc=0.98, rotationX=3, rotationY=5, rotationZ=-1)[:-1] + ", duration: 2.6, ease: \"sine.inOut\"}",
       "a0": a0, "a1": a1, "dva": t_dva, "zab": t_zab, "ring": RING})
g.sfx("whoosh-short", a0); g.sfx("click", t_dva); g.sfx("whoosh-short", a1)

# FULL 2 — inside the instruction field: what goes in; then «Модель» -> Haiku --
t_tobto, t_skr, t_aud, t_kon = S(u"Тобто", 17.97), S(u"скрипти,", 20.05), S(u"і цільова", 20.61), S(u"контекст", 22.17)
t_mod, t_obyr, t_haiku, t_tomu = S(u"Модель", 24.50), S(u"обирати,", 25.49), S(u"Haiku", 27.57), S(u"тому", 29.18)
b0, b1 = t_tobto - 0.2, t_tomu - 0.1
js(u"""
  tl.set(".o, .o2, #toks", {opacity: 1}, %(b0).3f);
  tl.set(["#fld", "#tok"], {%(unring)s}, %(b0).3f);
  tl.set("#win", %(f0)s, %(b0).3f);
  tl.to("#win", %(f1)s, %(b0).3f + .1);
  tl.to("#fld", {%(ring)s, duration: .3}, %(b0).3f + .7);
  tl.to("#ty1", {scaleX: 0, duration: .7, ease: "steps(22)"}, %(skr).3f - .1);
  tl.to("#ty2", {scaleX: 0, duration: .6, ease: "steps(18)"}, %(aud).3f - .05);
  tl.to("#ty3", {scaleX: 0, duration: .8, ease: "steps(24)"}, %(kon).3f - .1);
  tl.to("#fld", {%(unring)s, duration: .3}, %(mod).3f - .5);
  tl.to("#win", %(m1)s, %(mod).3f - .55);
  tl.fromTo("#dd", {autoAlpha: 0, scaleY: .6}, X({autoAlpha: 1, scaleY: 1, duration: .3, ease: "power2.out"}), %(obyr).3f);
  tl.to("#opH", {backgroundColor: "#F3E7E8", duration: .15}, %(haiku).3f - .25);
  tl.to("#kl, #kv, #cw", {autoAlpha: 0, duration: .15}, %(obyr).3f);
  tl.to("#dd", {autoAlpha: 0, duration: .2}, %(haiku).3f + .35);
  tl.to("#kl, #kv, #cw", {autoAlpha: 1, duration: .2}, %(haiku).3f + .5);
  tl.to("#sv1", {opacity: 0, duration: .1}, %(haiku).3f + .35);
  tl.to("#sv2", {opacity: 1, duration: .1}, %(haiku).3f + .4);
  tl.to("#sel", {%(ring)s, duration: .3}, %(haiku).3f + .4);
  tl.to("#win", %(m2)s, %(haiku).3f + .5);
  full(%(b0).3f, %(b1).3f);
""" % {"b0": b0, "b1": b1, "skr": t_skr, "aud": t_aud, "kon": t_kon, "mod": t_mod, "obyr": t_obyr,
       "haiku": t_haiku, "ring": RING, "unring": UNRING,
       "f0": FLD(sc=0.95, rotationX=10, rotationY=-8, rotationZ=2),
       "f1": FLD(rotationX=3, rotationY=-2, rotationZ=0.5)[:-1] + ", duration: 1.6, ease: \"power3.out\"}",
       "m1": MOD(rotationX=0, rotationY=9)[:-1] + ", duration: 1.2, ease: \"power3.inOut\"}",
       "m2": WIDE(rotationX=0, rotationY=3)[:-1] + ", duration: 1.6, ease: \"sine.inOut\"}"})
g.sfx("whoosh-short", b0); g.sfx("typing", t_skr - 0.1); g.sfx("typing", t_kon - 0.1)
g.sfx("whoosh-short", t_mod - 0.55); g.sfx("click-soft", t_obyr); g.sfx("click", t_haiku + 0.35)
g.sfx("whoosh-short", b1)

# 4 · ABOVE — Sonnet | Haiku: «×3–4» on «дорожче», «=» on «різниці» ----------
t_son, t_hai2, t_tri, t_dor = S(u"Sonnet", 36.30), S(u"Haiku.", 37.20), S(u"три", 39.07), S(u"дорожче,", 40.09)
t_rizn, t_ido = S(u"різниці", 41.09), S(u"І,", 44.37)
F.append(u'''
        <div id="cmp" class="card cmp hid">
          <div class="m"><span>Claude</span><b>Sonnet</b><div class="x hid" id="cx">×3–4</div></div>
          <div class="eq hid" id="ceq">=</div>
          <div class="m hid" id="cmH"><span>Claude</span><b>Haiku</b></div>
        </div>''')
js(u'''
  rise("#cmp", %.3f);
  pop("#cmH", %.3f);
  pop("#cx", %.3f);
  pop("#ceq", %.3f);
  sink("#cmp", %.3f);
''' % (t_son - 0.25, t_hai2 - 0.05, t_tri - 0.05, t_rizn, t_ido - 0.35))
# MEME 1 — «а гроші зекономиш.»: deal-with-it hamster, right of her head, before the card
g.meme(F, J, "35", E(u"зекономиш.", 34.5) + 0.05, dur=0.85, slot="r")
g.sfx("pop", t_son - 0.25); g.sfx("pop", t_hai2); g.sfx("kaching", t_dor); g.sfx("click-soft", t_rizn)

# FULL 3 — «ПОШУК У ФАЙЛАХ» goes grey; it all goes into the instruction --------
t_zav, t_prop, t_mozh, t_znovu = S(u"завантаження", 45.08), S(u"пропустити,", 46.42), S(u"можна", 49.33), S(u"знову", 50.92)
c0, c1 = t_ido - 0.1, t_znovu + 0.05
js(u"""
  tl.set(["#sel"], {%(unring)s}, %(c0).3f);
  tl.set("#win", %(w0)s, %(c0).3f);
  tl.to("#win", %(w1)s, %(c0).3f + .1);
  tl.to("#win", %(f1)s, %(zav).3f - .45);
  tl.to("#fc", {opacity: .35, filter: "grayscale(1)", duration: .4}, %(prop).3f);
  tl.to("#win", %(f2)s, %(mozh).3f - .3);
  tl.to("#fld", {%(ring)s, duration: .3}, %(mozh).3f + .9);
  full(%(c0).3f, %(c1).3f);
""" % {"c0": c0, "c1": c1, "zav": t_zav, "prop": t_prop, "mozh": t_mozh, "ring": RING, "unring": UNRING,
       "w0": WIDE(sc=0.9, dy=200, rotationX=0, rotationY=12, rotationZ=-2),
       "w1": WIDE(rotationX=0, rotationY=6, rotationZ=-1)[:-1] + ", duration: 1.0, ease: \"power3.out\"}",
       "f1": FIL(rotationX=0, rotationY=-5)[:-1] + ", duration: 1.2, ease: \"power3.inOut\"}",
       "f2": FLD(rotationX=0, rotationY=2, rotationZ=-0.5)[:-1] + ", duration: 1.3, ease: \"power3.inOut\"}"})
g.sfx("whoosh-short", c0); g.sfx("whoosh-short", t_zav - 0.45); g.sfx("click-soft", t_prop)
g.sfx("whoosh-short", t_mozh - 0.3); g.sfx("whoosh-short", c1)

# 5 · BEHIND — «Токени» --------------------------------------------------------
t_tok, e_tok = S(u"Токени.", 57.50), E(u"Токени.", 57.50)
B.append(u'        <div id="bw2" class="big hid" data-layout-allow-occlusion style="top:440px; font-size:230px">Токени</div>')
g.matte("b2", round(t_tok - 0.6, 3), 3.6)
js(u'  rise("#bw2", %.3f); sink("#bw2", %.3f);' % (t_tok - 0.35, t_tok + 2.4))
g.sfx("whoosh-short", t_tok - 0.35)
BLACKOUT.append((t_tok - 0.03, e_tok))

# 6 · HALF — the scheme: a token budget = думає + відповідь; at 500 nothing is left
t_ale, t_chast, t_podum = S(u"Але", 64.60), S(u"частину", 66.00), S(u"подумати,", 68.13)
t_500, t_zmozhe, e_tekst = S(u"500,", 70.33), S(u"зможе", 74.58), E(u"текст.", 75.86)
k0, k1 = t_ale - 0.1, e_tekst + 0.05
HALF.append((k0, k1))
js(u'''
  sketch("h1", "skP"); box("h1", 110, 330, 860, 130, {seed: 3});
  draw("h1", %(chast).3f - .3);
  sketch("h2", "skP"); box("h2", 120, 340, 420, 110, {seed: 5, fill: true, r: 22});
  label("h2", 330, 412, "думає", {size: 54}); label("h2", 755, 412, "відповідь", {size: 54});
  draw("h2", %(podum).3f - .35);
  sketch("h3", "skP"); label("h3", 190, 612, "500", {size: 64, color: "#7A1424"});
  box("h3", 280, 540, 380, 120, {seed: 9, fill: true});
  label("h3", 470, 617, "думає", {size: 54});
  draw("h3", %(p500).3f - .1, .5);
  sketch("h4", "skP"); box("h4", 700, 540, 270, 120, {seed: 11});
  label("h4", 835, 617, "відповідь", {size: 46, color: "#9a8a8a"});
  ln("h4", 712, 552, 958, 648, {stroke: "#7A1424", strokeWidth: 7, seed: 13});
  ln("h4", 712, 648, 958, 552, {stroke: "#7A1424", strokeWidth: 7, seed: 17});
  draw("h4", %(zm).3f - .5, .35);
  erase("h1", %(k1).3f); erase("h2", %(k1).3f); erase("h3", %(k1).3f); erase("h4", %(k1).3f);
''' % {"chast": t_chast, "podum": t_podum, "p500": t_500, "zm": t_zmozhe, "k1": k1})
g.sfx("whoosh-short", k0); g.sfx("click-soft", t_podum); g.sfx("pop", t_500); g.sfx("click", t_zmozhe)

# FULL 4 — the token field: 500 -> 2000 on its word ----------------------------
t_u, t_2000, t_adek, t_vpl = S(u"У", 76.40), S(u"2000", 77.55), S(u"адекватна", 78.95), S(u"не впливає", 83.42)
d0, d1 = max(t_u - 0.15, k1 + 0.3), E(u"вартість.", 84.08) + 0.15
js(u"""
  tl.set(".o, .o2, #toks, #fc", {opacity: 1, filter: "none"}, %(d0).3f);
  tl.set(["#fld", "#sel", "#tok"], {%(unring)s}, %(d0).3f);
  tl.set("#win", %(t0)s, %(d0).3f);
  tl.to("#win", %(t1)s, %(d0).3f + .1);
  tl.to("#tok", {%(ring)s, duration: .25}, %(t2k).3f - .3);
  tl.to("#tk5", {opacity: 0, duration: .08}, %(t2k).3f - .05);
  tl.to("#tk2", {opacity: 1, duration: .08}, %(t2k).3f);
  tl.fromTo("#tok", {scale: 1}, X({scale: 1.12, duration: .18, yoyo: true, repeat: 1, ease: "power2.out"}), %(t2k).3f);
  tl.to("#win", %(t2)s, %(adek).3f);
  tl.to("#win", %(t3)s, %(vpl).3f - .6);
  full(%(d0).3f, %(d1).3f);
""" % {"d0": d0, "d1": d1, "t2k": t_2000, "adek": t_adek, "vpl": t_vpl, "ring": RING, "unring": UNRING,
       "t0": TOK(sc=1.6, rotationX=0, rotationY=12, rotationZ=-2),
       "t1": TOK(rotationX=0, rotationY=4)[:-1] + ", duration: 1.2, ease: \"power3.out\"}",
       "t2": TOK(sc=1.85, rotationX=0, rotationY=-6)[:-1] + ", duration: 2.6, ease: \"sine.inOut\"}",
       "t3": WIDE(rotationX=0, rotationY=-6, rotationZ=1)[:-1] + ", duration: 1.4, ease: \"power3.inOut\"}"})
g.sfx("whoosh-short", d0); g.sfx("click", t_2000); g.sfx("whoosh-short", t_vpl - 0.6); g.sfx("whoosh-short", d1)

# 7 · ABOVE — «Пиши коротко.» into the instruction, then again and again -------
t_pysav, t_propys, t_dekil, t_raziv, t_tomu2 = (S(u"писав", 86.09), S(u"прописати", 88.29),
                                                S(u"декілька", 90.32), S(u"разів", 90.68), S(u"Тому", 91.73))
F.append(u'''
        <div id="ins" class="card ins hid">
          <div class="t">Інструкція для бота</div>
          <div class="f"><div id="pk1">Пиши коротко.</div><div id="pk2">Пиши коротко.</div><div id="pk3">ПИШИ КОРОТКО.</div></div>
        </div>''')
EXTRA += u"    #pk1, #pk2, #pk3 { clip-path: inset(0 100% 0 0); }\n"
js(u'''
  rise("#ins", %.3f);
  tl.to("#pk1", {clipPath: "inset(0 0%% 0 0)", duration: .55, ease: "steps(13)"}, %.3f);
  tl.to("#pk2", {clipPath: "inset(0 0%% 0 0)", duration: .45, ease: "steps(13)"}, %.3f);
  tl.to("#pk3", {clipPath: "inset(0 0%% 0 0)", duration: .45, ease: "steps(13)"}, %.3f);
  sink("#ins", %.3f);
''' % (t_pysav - 0.3, t_propys, t_dekil - 0.05, t_raziv + 0.15, t_tomu2 + 0.1))
g.sfx("pop", t_pysav - 0.3); g.sfx("typing", t_propys); g.sfx("typing", t_dekil - 0.05)

# MEME 2 — «сам він про це не здогадається»: the clueless goat, above her head,
# in the gap between the instruction card and the DM
g.meme(F, J, "44", E(u"здогадається,", 93.1) + 0.05, dur=0.85, slot="top")

# 8 · ABOVE — glass DM: left alone it writes an essay -------------------------
t_pysaty, t_vel, t_rozsh, t_posl, e_dali = (S(u"писати", 94.77), S(u"великі,", 95.27), S(u"розширені", 96.04),
                                           S(u"послуги", 98.22), E(u"далі.", 99.44))
F.append(u'''
        <div id="dm" class="glass dm hid">
          <div><span class="bub in">Скільки коштує консультація?</span></div>
          <div class="rowr"><span class="bub me" id="dmr">
            <span class="gl" id="g1">Дякуємо за повідомлення! Раді, що ви з нами.</span>
            <span class="gl" id="g2">Ми надаємо консультації, супровід, навчання,</span>
            <span class="gl" id="g3">аудит, стратегії та програми для бізнесу…</span></span></div>
        </div>''')
js(u'''
  rise("#dm", %.3f);
  tl.fromTo("#g1", {height: 0, autoAlpha: 0}, X({height: "auto", autoAlpha: 1, duration: .45, ease: "power2.out"}), %.3f);
  tl.fromTo("#g2", {height: 0, autoAlpha: 0}, X({height: "auto", autoAlpha: 1, duration: .45, ease: "power2.out"}), %.3f);
  tl.fromTo("#g3", {height: 0, autoAlpha: 0}, X({height: "auto", autoAlpha: 1, duration: .45, ease: "power2.out"}), %.3f);
  sink("#dm", %.3f);
''' % (t_pysaty - 0.2, t_vel - 0.1, t_rozsh + 0.1, t_posl - 0.2, e_dali + 0.15))
g.sfx("pop", t_pysaty - 0.2); g.sfx("notification", t_vel); g.sfx("notification", t_posl - 0.2)

# 9 · CTA — who it is for, one card at a time; «Став + в коментарях» -----------
t_stav = S(u"став", 109.68)
SH2 = [(u"немає менеджера", S(u"немає", 100.87) - 0.1),
       (u"менеджер не справляється", S(u"менеджер,", 102.15) - 0.1),
       (u"купа заявок у діректі", S(u"купа", 103.80) - 0.05),
       (u"губляться без відповіді", S(u"губляться", 107.80) - 0.1)]
for i, (txt, t) in enumerate(SH2):
    F.append(u'        <div id="sc%d" class="shuf hid"><span class="chip"><i></i>%s</span></div>' % (i, txt))
    g.sfx("pop", t)
js(u'  shuffle([%s], [%s], %.3f);' % (", ".join('"#sc%d"' % i for i in range(len(SH2))),
                                      ", ".join("%.3f" % t for _, t in SH2), t_stav + 1.4))
F.append(u'''        <div id="ctp" class="pill hid" style="left:0; right:0; margin:auto; width:max-content; top:1404px;
             font-size:46px; padding:28px 56px">Став + в коментарях</div>''')
js(u'  pop("#ctp", %.3f);' % (t_stav - 0.1))
g.sfx("pop", t_stav)
BLACKOUT.append((t_stav - 0.05, DUR))

# ---------------------------------------------------------------- half screen + its matte
for i, (a, b) in enumerate(HALF):
    g.matte("half%d" % (i + 1), round(a - 0.1, 3), round(b - a + 1.2, 3))
    js("  half(%.3f, %.3f);" % (a, b))
    PLACE.append((a + 0.4, b + 0.2, "bottom", 938))


def main():
    chunks = g.chunks(CAPS, place=PLACE)
    doc = g.document(title=u"Reel 62 — налаштування AI-агента", plate="assets/base.mp4",
                     behind="\n".join(B), panel="\n".join(P), front="\n".join(F), cover="\n".join(C),
                     js="\n".join(J), chunks=chunks, blackout=BLACKOUT, extra_css=EXTRA)
    g.write(HERE, doc)
    print("index.html  %d caption chunks, %d sfx cues, %d mattes" % (len(chunks), len(g.cues), len(g.mattes)))
    if "-w" in sys.argv:
        print(" ".join("%s/%.1f" % (c["w"], c["s"]) for c in CAPS))


main()
