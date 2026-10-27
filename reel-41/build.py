# -*- coding: utf-8 -*-
"""Reel 41 — «Клод розсилає повідомлення, поки я вмиваюсь».

One raw take, cut by ../work/r41/ramp.py: her intro, the five-minute screen
session as a 27x time-lapse that brakes into real time on the last profile
switch, then the last take of her outro. 36.95 s.

Her brief for the graphics, all of it, and it is literal:
  - NO animations. Everything here is a hard on / hard off (tl.set), no plate
    push, no springs. Captions stay as always: word by word, instant.
  - on «розсилає повідомлення» a footnote above the caption,
    «*персоналізовані», because she forgot to say it.
  - while the screen works, a smaller text (not a caption) explaining how it
    works, in her voice (ruta-voice), at WCAG AA at least.

Contrast, computed against the worst case (a white laptop screen behind the
panel): the explainer panel is ink-burgundy at 0.88 alpha, so over pure white
its ground is ~#3d2930 -> white text 13:1, the pink accent #ff8db0 6:1.
The footnote pill is the same material. Both pass AA for body text.

usage: python3 build.py
"""
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))
from kit import Kit, esc  # noqa: E402
from glass import FONTS  # noqa: E402

CUT = json.load(io.open(os.path.join(ROOT, "work", "r41", "cut.json"), encoding="utf-8"))
DUR = CUT["DUR"]       # (1109 plate frames - 0.5) / 30
FPS = 30
k = Kit(width=1080, height=1920, fps=FPS, duration=DUR)
k.css(FONTS)

# -- captions: whisper timing, mapped through the cut ------------------------
# The intro runs 1x from INTRO[0]; the outro 1x from OUTRO[0] at t4. The first
# outro take (333.1-349.3) is not in the cut.
WORDS = json.load(io.open(os.path.join(ROOT, "work", "r41", "words.json"), encoding="utf-8"))["words"]
FIX = {u"мимо": u"моїм", u"розіслено.": u"розіслано."}
I0, I1 = CUT["intro"]
O0, O1 = CUT["outro"]
T4 = CUT["t4"]
CAPS = []
for x in WORDS:
    if I0 <= x["s"] < I1:
        s, e = x["s"] - I0, x["e"] - I0
    elif O0 <= x["s"] < O1:
        s, e = T4 + x["s"] - O0, T4 + x["e"] - O0
    else:
        continue
    CAPS.append({"w": FIX.get(x["w"], x["w"]), "s": round(max(0.0, s), 3), "e": round(e, 3)})
# her first word lands at 0.62 in the source (whisper says 0.52): no caption
# before she speaks
CAPS[0]["s"] = max(CAPS[0]["s"], 0.17)
for _a, _b in zip(CAPS, CAPS[1:]):
    _a["e"] = round(max(_a["s"] + 0.10, _b["s"] - 0.085), 3)
# the last intro word must not run onto the screen; the last word holds a beat
for c in CAPS:
    if c["s"] < CUT["t1"]:
        c["e"] = min(c["e"], CUT["t1"])
CAPS[-1]["e"] = round(min(DUR - 0.05, CAPS[-1]["s"] + 0.9), 3)

# the footnote mark rides the caption word itself
NOTE_WORD = next(i for i, c in enumerate(CAPS) if c["w"].startswith(u"повідомлення") and c["s"] < 5)
CAPS[NOTE_WORD]["w"] = CAPS[NOTE_WORD]["w"].rstrip(",") + u"*"
NOTE_ON = CAPS[NOTE_WORD]["s"]
NOTE_OFF = round(NOTE_ON + 2.2, 3)             # long enough to read two words

SCREEN = (round(CUT["t1"], 3), round(CUT["t4"], 3))

# -- the explainer (ruta-voice) ----------------------------------------------
P1 = (u"По суті, Клод працює через вбудований браузер і робить паузу "
      u"<b>мінімум 30 секунд</b> між повідомленнями, щоб інстаграм мене не заблокував.")
P2 = (u"До кожної людини він спершу заходить у профіль: дивиться контент, біо, ім'я "
      u"і вже тоді пише персональне повідомлення за моїм правилом.")

k.css(u"""
/* one material for both: ink-burgundy glass, dense enough for AA over a white screen */
.inkp { position: absolute; color: #fff;
  background: linear-gradient(160deg, rgba(52,20,30,0.90) 0%, rgba(23,10,16,0.88) 100%);
  -webkit-backdrop-filter: blur(26px) saturate(1.4); backdrop-filter: blur(26px) saturate(1.4);
  box-shadow: inset 0 2px 1px rgba(255,255,255,0.26), inset 0 -14px 28px -16px rgba(255,255,255,0.10),
              0 36px 70px -28px rgba(10,0,4,0.55);
  opacity: 0; visibility: hidden; }
#explain { left: 90px; width: 900px; top: 1150px; border-radius: 48px; padding: 40px 48px 42px; }
#explain p { font-family: "ProductSans"; font-weight: 500; font-size: 39px; line-height: 1.32;
  letter-spacing: -0.005em; }
#explain p + p { margin-top: 20px; }
#explain b { font-weight: 700; color: #ff8db0; }
#note { left: 0; right: 0; margin: 0 auto; width: max-content; top: 1318px;
  border-radius: 30px; padding: 12px 30px 14px;
  font-family: "ProductSans"; font-weight: 700; font-size: 44px; line-height: 1; }
.cap { letter-spacing: -0.015em; }
""")

# Her rule (STYLE.md §4a, «proof is a screenshot»): real screens, blurred where
# personal. The phone sat still on the laptop the whole session, so the
# commenters' handles stay where they are: the browser's address bar and profile
# header (a different person every few frames), and on the left, in Claude's
# report, which never scrolls, one @handle and two first names. Static boxes,
# on with the screen, off with it.
BLUR = [(600, 88, 480, 182),     # URL + avatar + handle + stats + bio
        (312, 274, 166, 32),     # @womenhelpua
        (172, 420, 150, 32),     # «Rina, Emma,»
        (0, 448, 96, 30)]        # «...business»
k.css(u""".bl { position: absolute; border-radius: 14px;
  -webkit-backdrop-filter: blur(9px); backdrop-filter: blur(9px); opacity: 0; visibility: hidden; }""")
BLUR_HTML = "\n".join(u'      <div class="bl" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx"></div>'
                      % b for b in BLUR)

HTML = BLUR_HTML + u"""
      <div id="explain" class="inkp"><p>%s</p><p>%s</p></div>""" % (P1, esc(P2))
# the footnote sits on the caption plaque, so it paints after the scrim
NOTE = u'<div id="scrim"></div>\n      <div id="note" class="inkp">*персоналізовані</div>'

JS = u"""
  tl.set("#note", {autoAlpha: 1}, %.3f);
  tl.set("#note", {autoAlpha: 0}, %.3f);
  tl.set(".bl", {autoAlpha: 1}, %.3f);
  tl.set(".bl", {autoAlpha: 0}, %.3f);
  tl.set("#explain", {autoAlpha: 1}, %.3f);
  tl.set("#explain", {autoAlpha: 0}, %.3f);""" % (NOTE_ON, NOTE_OFF, SCREEN[0], SCREEN[1], SCREEN[0], SCREEN[1])


def main():
    doc = k.document(
        title=u"Reel 41 — Клод розсилає повідомлення",
        plate="assets/base.mp4",
        gfx_html=HTML,
        gfx_js=JS,
        caps=CAPS,
        scrim_off=[(SCREEN[0], SCREEN[1], None)],
    )
    doc = doc.replace(u'<div id="scrim"></div>', NOTE, 1)
    io.open(os.path.join(HERE, "index.html"), "w", encoding="utf-8").write(doc)
    json.dump({"words": CAPS}, io.open(os.path.join(ROOT, "work", "r41", "captions.json"), "w",
                                       encoding="utf-8"), ensure_ascii=False, indent=1)
    print("index.html  %d captions, note %.2f-%.2f, explainer %.2f-%.2f, DUR %.3f"
          % (len(CAPS), NOTE_ON, NOTE_OFF, SCREEN[0], SCREEN[1], DUR))


main()
