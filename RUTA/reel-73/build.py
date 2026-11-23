# -*- coding: utf-8 -*-
"""Reel 73 — «Що таке OpenRouter?». A basic edit (her brief 2026-11-23): the
explanation of what OpenRouter is kept, the over-explanation and the whole
second half (reel-copying / competitors / skill) cut. Few animations, only where
they make sense: a behind-me word, the model list as a shuffle, the 9 $ vs 5 $
cards, one meme. Captions as usual.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))
from gstyle import G, Words, load_caps  # noqa: E402

NN = "73"
DUR = 64.883           # (1947 plate frames - 0.5) / 30
g = G(dur=DUR, reel=NN)
CAPS = load_caps(NN, {})
W = Words(CAPS)
S, E = W.s, W.e
B, F, J = [], [], []
EXTRA = u""


def js(s):
    J.append(s)


# 1 · BEHIND — «OpenRouter» on the question that opens the reel (her hook word)
t0 = S(u"OpenRouter?", 1.6) - 0.1
B.append(u'        <div id="bw1" class="big hid" data-layout-allow-occlusion style="top:450px; font-size:200px">OpenRouter</div>')
g.matte("b1", round(t0 - 0.1, 3), 2.9)
js(u'  rise("#bw1", %.3f); sink("#bw1", %.3f);' % (t0, t0 + 2.6))
g.sfx("whoosh-short", t0)

# 2 · SHUFFLE — the models it holds, one card at a time
M = [(u"Claude", S(u"Клода,", 6.92)), (u"ChatGPT", S(u"ChatGPT,", 7.48)),
     (u"NanoBanana", S(u"NanoBanana,", 8.32)), (u"Kling", S(u"Kling,", 9.28))]
for i, (txt, _) in enumerate(M):
    F.append(u'        <div id="m%d" class="shuf hid"><span class="chip"><i></i>%s</span></div>' % (i, txt))
js(u'  shuffle(%s, %s, %.3f);' % ([u'"#m%d"' % i for i in range(len(M))] and
                                 u'[' + u','.join(u'"#m%d"' % i for i in range(len(M))) + u']',
                                 u'[' + u','.join('%.3f' % (t - 0.1) for _, t in M) + u']',
                                 S(u"платформі.", 12.6) - 0.1))
for _, t in M:
    g.sfx("pop", t - 0.1)

# 3 · SHUFFLE — what it costs: a 9 $ subscription -> 5 $ you top up
C = [(u"підписка — 9 $ / міс", S(u"доларів", 30.4) - 0.5), (u"OpenRouter — від 5 $", S(u"доларів,", 35.12) - 0.5)]
for i, (txt, _) in enumerate(C):
    F.append(u'        <div id="c%d" class="shuf hid"><span class="chip"><i></i>%s</span></div>' % (i, txt))
js(u'  shuffle(["#c0","#c1"], [%.3f, %.3f], %.3f);' % (C[0][1], C[1][1], E(u"доларів,", 35.12) + 1.6))
for _, t in C:
    g.sfx("pop", t)

# 4 · MEME — «ти бач, треба ж таке» after «все, що завгодно»
g.meme(F, J, "20", E(u"завгодно.", 42.1) + 0.1, dur=1.3)


def main():
    chunks = g.chunks(CAPS)
    doc = g.document(title=u"Reel 73 — Що таке OpenRouter", plate="assets/base.mp4",
                     behind="\n".join(B), panel="", front="\n".join(F), cover="",
                     js="\n".join(J), chunks=chunks, blackout=[], extra_css=EXTRA)
    doc = doc.replace('    <script src="assets/js/rough-4.6.6.js"></script>\n', "")   # no sketches here
    g.write(HERE, doc)
    print("index.html  %d caption chunks, %d sfx cues, %d mattes" % (len(chunks), len(g.cues), len(g.mattes)))


main()
