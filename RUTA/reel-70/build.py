# -*- coding: utf-8 -*-
"""Reel 70 — «Як зробити CRM у Notion, якщо в тебе малий бізнес?». Batch
2026-11-20 (raw 20261120_140234). STYLE.md §00 + her review of reel 61
(natural editing: one meaningful moment per sentence group). Skeleton and
idioms from reel-61/build.py.

Chain: behind «CRM» (cover) -> the three questions shuffle through one slot ->
her own punch-ins carry «погані новини … не з власного досвіду» -> behind
«5 хвилин» -> step 1, a glass browser tab types notion.com -> FULL 1, Claude
«Customize → Connectors» as a platform-ad sequence (Notion found, Connect ->
Connected on «підключаєш») -> step 3, a glass Claude prompt types her words
as she says them, sent on «І все» -> FULL 2, the CRM database lands in Notion,
a new lead row drops in on «складатимуться всі нові ліди» -> HALF, the scheme:
чати / скріншот -> скіл CRM -> CRM -> a glass draft message her skill wrote,
sent on «відправити» -> CTA: the shuffle slot (Підписатись, CRM, агент,
навчання, і 35-те) + «Напиши + в коментарях» in the subtitle band.

usage: python3 build.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))
sys.path.insert(0, HERE)
from gstyle import G, Words, load_caps, mark  # noqa: E402
import ui  # noqa: E402

NN = "70"
DUR = float(open(os.path.join(HERE, "DUR")).read())
g = G(dur=DUR, reel=NN)
g.PANEL_TOP = 820

FIX = {
    u"глідами.": u"лідами", u"за собі": u"собі", u"твій": u"твої", u"чате": u"чати",
    u"ему скрішет": u"йому скріншот", u"та ісей": u"і се, і", u"35": u"35-те", u"те,": None,
    u"в якому": u"в яку",
}
CAPS = load_caps(NN, FIX)
W = Words(CAPS)
S, E = W.s, W.e

B, P, F, C, J = [], [], [], [], []
BLACKOUT, PLACE, HALF = [], [], []


def js(s):
    J.append(s)


def cam(cx0, cy0, px, py, sc, cx=540, cy=760):
    """window turns and scales about its centre (cx0, cy0); put its point
    (px, py) at screen (cx, cy)"""
    return (round(cx - cx0 - sc * (px - cx0), 1), round(cy - cy0 - sc * (py - cy0), 1))


P.append(u'<svg class="sk" id="skP" data-layout-allow-occlusion width="1080" height="1240" viewBox="0 0 1080 1240"></svg>')
EXTRA = ui.CSS
NOTION_MARK = mark("notion", 26)

# 1 · BEHIND — «CRM», the cover frame -----------------------------------------
t_crm, e_crm = S(u"CRM-системи,", 1.31), E(u"CRM-системи,", 1.31)
t_i = S(u"і", 2.09)
B.append(u'        <div id="bw1" class="big hid" data-layout-allow-occlusion style="top:420px; font-size:250px">CRM</div>')
g.matte("b1", 0.0, round(t_i + 0.7, 3))
js(u'  tl.set("#bw1", {autoAlpha: 1}, 0); sink("#bw1", %.3f);' % (t_i + 0.25))
BLACKOUT.append((t_crm - 0.03, e_crm))

# 2 · ABOVE — the three questions, one slot -------------------------------------
Q = [(u"Скільки зараз лідів?", S(u"скільки", 3.83)), (u"Скільки було клієнтів?", S(u"скільки", 5.10)),
     (u"Як їм написати?", S(u"як", 7.23))]
t_pog = S(u"погані", 9.04)
for i, (txt, t) in enumerate(Q):
    F.append(u'        <div id="q%d" class="shuf hid"><span class="chip"><i></i>%s</span></div>' % (i, txt))
    g.sfx("pop", t - 0.1)
js(u'  shuffle(["#q0", "#q1", "#q2"], [%s], %.3f);' % (", ".join("%.3f" % (t - 0.1) for _, t in Q), t_pog))

# 3 · BEHIND — «5 хвилин» -------------------------------------------------------
t_5, e_5 = S(u"5", 22.01), E(u"хвилин.", 22.29)
B.append(u'        <div id="bw2" class="big hid" data-layout-allow-occlusion style="top:430px; font-size:230px">5 хвилин</div>')
g.matte("b2", round(t_5 - 0.6, 3), round(e_5 - t_5 + 1.3, 3))
js(u'  rise("#bw2", %.3f); sink("#bw2", %.3f);' % (t_5 - 0.35, e_5 + 0.35))
g.sfx("whoosh-short", t_5 - 0.35)
BLACKOUT.append((t_5 - 0.03, e_5))

# 4 · ABOVE — step 1: a glass browser tab, notion.com typed, sign up -----------
t_vkl, t_pyshesh, t_reie = S(u"вкладку", 27.28), S(u"пишеш", 28.18), S(u"реєструєшся.", 29.98)
F.append(u'''
        <div id="tb" class="glass tab hid">
          <div class="bar"><span class="dots"><i></i><i></i><i></i></span><span class="t">Нова вкладка</span></div>
          <div class="addr">%s<span id="url"></span><span class="caret" id="ucar"></span><span id="sgn" class="go hid">Sign up</span></div>
        </div>''' % mark("notion", 44))
URL = u"notion.com"
js(u'  rise("#tb", %.3f);' % (t_vkl - 0.2))
for k in range(1, len(URL) + 1):
    js(u'  tl.set("#url", {textContent: "%s"}, %.3f);' % (URL[:k], t_pyshesh + 0.06 * k))
js(u'  pop("#sgn", %.3f); sink("#tb", %.3f);' % (t_reie, S(u"Другий", 30.57) - 0.2))
g.sfx("pop", t_vkl - 0.2); g.sfx("typing", t_pyshesh); g.sfx("click", t_reie)

# 5 · FULL 1 — Claude, Customize -> Connectors -> Notion -> Connected ------------
f0 = S(u"Другий", 30.57) - 0.15
f1 = E(u"Клода.", 37.85) + 0.2
C.append(ui.CLAUDE % {"notion": NOTION_MARK})
t_cust, t_conn, t_shuk, t_not, t_pidk = (S(u"Customize", 33.35), S(u"Connectors,", 34.15), S(u"шукаєш", 34.83),
                                         S(u"Notion", 35.55), S(u"підключаєш", 36.17))
O1 = (400, 260)
WIDE = (1.2,) + cam(*O1, px=400, py=260, sc=1.2)
SIDE = (2.1,) + cam(*O1, px=260, py=150, sc=2.1)
SRCH = (2.2,) + cam(*O1, px=500, py=170, sc=2.2)
ROW = (2.5,) + cam(*O1, px=520, py=230, sc=2.5)
js(u"""
  gsap.set("#win1", {transformOrigin: "400px 260px"});
  gsap.set("#win1", {x: %(wx)s, y: %(wy)s + 220, scale: %(ws)s * .86, rotationX: 24, rotationY: -20, rotationZ: 5});
  tl.to("#win1", {x: %(wx)s, y: %(wy)s, scale: %(ws)s, rotationX: 9, rotationY: -12, rotationZ: 2, duration: 1.2, ease: "power3.out"}, %(f0).3f + .1);
  tl.to("#win1", {x: %(sx)s, y: %(sy)s, scale: %(ss)s, rotationX: 4, rotationY: 7, rotationZ: 0, duration: 1.1, ease: "power3.inOut"}, %(cust).3f - .7);
  tl.to("#cl-cust", {backgroundColor: "#E6E2D8", duration: .25}, %(cust).3f);
  tl.to("#cl-conn", {color: "#1f1f1f", borderBottomColor: "#1f1f1f", duration: .25}, %(conn).3f);
  tl.to("#win1", {x: %(qx)s, y: %(qy)s, scale: %(qs)s, rotationX: -2, rotationY: -6, duration: 1.0, ease: "power3.inOut"}, %(shuk).3f - .5);
  tl.to("#cl-search", {borderColor: "#1f1f1f", duration: .2}, %(shuk).3f);
  tl.set("#cl-q", {textContent: "N"}, %(not).3f); tl.set("#cl-q", {textContent: "No"}, %(not).3f + .06);
  tl.set("#cl-q", {textContent: "Not"}, %(not).3f + .12); tl.set("#cl-q", {textContent: "Noti"}, %(not).3f + .18);
  tl.set("#cl-q", {textContent: "Notio"}, %(not).3f + .24); tl.set("#cl-q", {textContent: "Notion"}, %(not).3f + .30);
  tl.to("#win1", {x: %(rx)s, y: %(ry)s, scale: %(rs)s, rotationX: 2, rotationY: 5, duration: .8, ease: "power3.inOut"}, %(pidk).3f - .55);
  tl.to("#cl-btn", {backgroundColor: "#E4EEE7", duration: .25}, %(pidk).3f);
  tl.to("#cl-btn .a", {autoAlpha: 0, y: -14, duration: .2}, %(pidk).3f);
  tl.fromTo("#cl-btn .b", {autoAlpha: 0, y: 14}, X({autoAlpha: 1, y: 0, duration: .3, ease: "back.out(2)"}), %(pidk).3f + .08);
  tl.fromTo("#cl-row", {boxShadow: "0 0 0 0 rgba(122,20,36,0)"}, X({boxShadow: "0 0 0 5px rgba(122,20,36,.18)", duration: .35, yoyo: true, repeat: 1}), %(pidk).3f + .1);
  tl.to("#win1", {x: %(wx)s, y: %(wy)s, scale: %(ws)s, rotationX: 10, rotationY: 14, rotationZ: -2, duration: 1.1, ease: "power3.inOut"}, %(pidk).3f + .8);
  full(%(f0).3f, %(f1).3f);
  tl.set("#stage1", {autoAlpha: 0}, %(f1).3f + .9);
""" % {"wx": WIDE[1], "wy": WIDE[2], "ws": WIDE[0], "sx": SIDE[1], "sy": SIDE[2], "ss": SIDE[0],
       "qx": SRCH[1], "qy": SRCH[2], "qs": SRCH[0], "rx": ROW[1], "ry": ROW[2], "rs": ROW[0],
       "f0": f0, "f1": f1, "cust": t_cust, "conn": t_conn, "shuk": t_shuk, "not": t_not, "pidk": t_pidk})
g.sfx("whoosh-short", f0); g.sfx("whoosh-short", t_cust - 0.7); g.sfx("click-soft", t_conn)
g.sfx("typing", t_not); g.sfx("click", t_pidk); g.sfx("whoosh-short", f1)

# 6 · ABOVE — step 3: a glass Claude prompt, typed with her words ---------------
t_chat, t_na, t_kl = S(u"новий", 40.34), S(u"на", 41.52), E(u"клієнтами.", 51.28)
t_vse = S(u"все,", 52.26)
typed = [c for c in CAPS if t_na - 0.01 <= c["s"] <= t_kl]
spans = u" ".join(u'<span id="pw%d" class="hid">%s</span>' % (i, c["w"]) for i, c in enumerate(typed))
F.append(u'''
        <div id="ask" class="glass ask hid">
          <div class="who"><span class="st">✳</span>Claude · новий чат</div>
          <div class="in">%s<span id="snd" class="send">↑</span></div>
        </div>''' % spans)
js(u'  rise("#ask", %.3f);' % (t_chat - 0.1))
for i, c in enumerate(typed):
    js(u'  tl.set("#pw%d", {autoAlpha: 1}, %.3f);' % (i, c["s"]))
js(u'  tl.to("#snd", {backgroundColor: "#7A1424", scale: 1.15, duration: .2, yoyo: true, repeat: 1}, %.3f);' % (S(u"І", 52.03)))
js(u'  sink("#ask", %.3f);' % (t_vse + 0.1))
g.sfx("pop", t_chat - 0.1); g.sfx("typing", t_na); g.sfx("click", S(u"І", 52.03))
BLACKOUT.append((t_na - 0.03, t_kl + 0.05))

# 7 · FULL 2 — the CRM lands in Notion; a new lead drops in ----------------------
g0 = S(u"профіт.", 52.65) - 0.2
t_got, t_sklad, e_lid = S(u"готова", 54.60), S(u"складатимуться", 56.16), E(u"ліди.", 57.50)
g1 = e_lid + 0.1
C.append(ui.NOTION % {"notion": NOTION_MARK, "rows": ui.notion_rows()})
O2 = (430, 235)
W2 = (1.15,) + cam(*O2, px=430, py=235, sc=1.15)
ST = (1.45,) + cam(*O2, px=400, py=290, sc=1.45)
js(u"""
  gsap.set("#win2", {transformOrigin: "430px 235px"});
  gsap.set("#stage2", {autoAlpha: 0}); tl.set("#stage2", {autoAlpha: 1}, %(g0).3f - .05);
  gsap.set("#win2", {x: %(wx)s, y: %(wy)s + 240, scale: %(ws)s * .85, rotationX: 26, rotationY: 18, rotationZ: -5});
  tl.to("#win2", {x: %(wx)s, y: %(wy)s, scale: %(ws)s, rotationX: 9, rotationY: 12, rotationZ: -2, duration: 1.2, ease: "power3.out"}, %(g0).3f + .1);
  tl.fromTo(["#nr0", "#nr1", "#nr2"], {autoAlpha: 0, y: 14}, X({autoAlpha: 1, y: 0, duration: .35, stagger: .12, ease: "power2.out"}), %(g0).3f + .45);
  tl.to("#win2", {x: %(sx)s, y: %(sy)s, scale: %(ss)s, rotationX: 3, rotationY: -6, rotationZ: 0, duration: 1.2, ease: "power3.inOut"}, %(got).3f - .6);
  tl.fromTo("#nr3", {autoAlpha: 0, y: -24, backgroundColor: "rgba(122,20,36,.10)"}, X({autoAlpha: 1, y: 0, duration: .45, ease: "back.out(1.6)"}), %(sk).3f);
  tl.to("#nr3", {backgroundColor: "rgba(122,20,36,0)", duration: .8}, %(sk).3f + .6);
  tl.to("#win2", {x: %(wx)s, y: %(wy)s, scale: %(ws)s, rotationX: 8, rotationY: -12, rotationZ: 2, duration: 1.1, ease: "power3.inOut"}, %(sk).3f + .6);
  full(%(g0).3f, %(g1).3f);
""" % {"wx": W2[1], "wy": W2[2], "ws": W2[0], "sx": ST[1], "sy": ST[2], "ss": ST[0],
       "g0": g0, "g1": g1, "got": t_got, "sk": t_sklad})
g.sfx("whoosh-short", g0); g.sfx("whoosh-short", t_got - 0.6); g.sfx("pop", t_sklad); g.sfx("whoosh-short", g1)

# 8 · HALF — the scheme: чати / скріншот -> скіл CRM -> CRM ---------------------
k0 = S(u"налаштувати", 60.58) - 0.35
k1 = E(u"загубився.", 69.12) + 0.1
HALF.append((k0, k1))
t_skil, t_dyv, t_skr, t_vnos = S(u"скіл", 61.40), S(u"дивиться", 62.78), S(u"йому скріншот", 65.00), S(u"вносить", 66.58)
js(u'''
  sketch("s1", "skP"); box("s1", 410, 450, 270, 130, {seed: 3, fill: true});
  label("s1", 545, 528, "скіл CRM", {size: 50});
  draw("s1", %.3f);
  sketch("s2", "skP"); box("s2", 60, 310, 230, 110, {seed: 5}); label("s2", 175, 378, "чати", {size: 50});
  arrow("s2", 290, 380, 420, 480, {seed: 7, bend: .2});
  draw("s2", %.3f);
  sketch("s3", "skP"); box("s3", 50, 620, 260, 110, {seed: 9}); label("s3", 180, 688, "скріншот", {size: 46});
  arrow("s3", 310, 660, 420, 560, {seed: 11, bend: -.2});
  draw("s3", %.3f);
  sketch("s4", "skP"); arrow("s4", 680, 515, 830, 515, {seed: 13, bend: .12});
  box("s4", 830, 450, 200, 130, {seed: 15, fill: true}); label("s4", 930, 528, "CRM", {size: 54});
  draw("s4", %.3f);
  erase("s1", %.3f); erase("s2", %.3f); erase("s3", %.3f); erase("s4", %.3f);
''' % (t_skil - 0.3, t_dyv - 0.2, t_skr - 0.3, t_vnos - 0.4, k1, k1, k1, k1))
g.sfx("whoosh-short", k0); g.sfx("click-soft", t_skil); g.sfx("click-soft", t_skr); g.sfx("click", t_vnos)

# 9 · ABOVE — a glass draft her skill wrote, sent on «відправити» ---------------
t_gotuie, t_vidp = S(u"готує", 71.18), S(u"відправити.", 73.75)
F.append(u'''
        <div id="dr" class="glass dm hid">
          <div class="hd"><b></b>Чернетка від скіла CRM</div>
          <div class="rowr"><span class="bub me">Добрий день! Нагадую про наш дзвінок завтра. Усе в силі?</span></div>
          <div id="drb" class="sendb">Надіслати</div>
        </div>''')
js(u'''
  rise("#dr", %.3f);
  tl.to("#drb", {backgroundColor: "#7A1424", scale: 1.08, duration: .18, yoyo: true, repeat: 1}, %.3f);
  sink("#dr", %.3f);
''' % (t_gotuie - 0.2, t_vidp, S(u"Тому", 74.47) - 0.1))
g.sfx("pop", t_gotuie - 0.2); g.sfx("click", t_vidp)

# 10 · CTA — the slot: Підписатись, then her list; «Напиши + в коментарях» ------
t_pidp = S(u"підпишись.", 76.78)
t_nap = S(u"напиши", 82.61)
CH = [(u"Підписатись", t_pidp - 0.1), (u"не просто CRM", S(u"CRM,", 79.24) - 0.15),
      (u"агент", S(u"агент,", 80.07) - 0.1), (u"навчання", S(u"навчання,", 80.43) - 0.05),
      (u"і 35-те", S(u"35-те", 81.35) - 0.1)]
for i, (txt, t) in enumerate(CH):
    F.append(u'        <div id="c%d" class="shuf hid"><span class="chip"><i></i>%s</span></div>' % (i, txt))
    g.sfx("pop", t)
js(u'  shuffle([%s], [%s], %.3f);' % (", ".join('"#c%d"' % i for i in range(len(CH))),
                                      ", ".join("%.3f" % t for _, t in CH), DUR + 1))
F.append(u'''        <div id="ctp" class="pill hid" style="left:0; right:0; margin:auto; width:max-content; top:1404px;
             font-size:46px; padding:28px 56px">Напиши + в коментарях</div>''')
js(u'  pop("#ctp", %.3f);' % (t_nap - 0.1))
g.sfx("pop", t_nap)
BLACKOUT.append((t_nap - 0.05, DUR))

# ---------------------------------------------------------------- half screens + their mattes
for i, (a, b) in enumerate(HALF):
    g.matte("half%d" % (i + 1), round(a - 0.1, 3), round(b - a + 1.2, 3))
    js("  half(%.3f, %.3f);" % (a, b))
    PLACE.append((a + 0.4, b + 0.2, "bottom", 938))


def main():
    chunks = g.chunks(CAPS, place=PLACE)
    doc = g.document(title=u"Reel 70 — CRM у Notion", plate="assets/base.mp4",
                     behind="\n".join(B), panel="\n".join(P), front="\n".join(F), cover="\n".join(C),
                     js="\n".join(J), chunks=chunks, blackout=BLACKOUT, extra_css=EXTRA)
    g.write(HERE, doc)
    print("index.html  %d caption chunks, %d sfx cues, %d mattes" % (len(chunks), len(g.cues), len(g.mattes)))


main()
