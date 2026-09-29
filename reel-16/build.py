# -*- coding: utf-8 -*-
"""Reel 16 — «Ти взагалі знаєш, звідки приходять твої клієнти». UTM tags and
end-to-end analytics on the webinar funnel she is producing.

Variant B, refined glass (STYLE.md §0, tools/glass.py). Structure follows
reel-12/build.py: kit document, her plate, mattes per beat, captions on the
plaque, one `.g full` container per beat.

The one object is **one link** and the one unknown is **the «?» where a
client's source should be**. Bare early: a new client's card with «?» in its
source field, and the sources she names can't fill it. Paid off: the link's
`?utm_…` tail travels reel -> site -> button -> SendPulse bot -> the contact
card, and the «?» turns into «instagram / reels». Then a crowd of cards sorts
itself by source.

The chain, near -> behind -> over, three times over:
    (her entrance — hair flip into the lens, zoom out to a pose: hers) ->
    a client card with «?» for a source; Reels, Stories, Meta land in the
    room as she names them and each is tried in the slot -> they fall away
    behind her on «втрачаєш», the card empties -> the card folds into a shelf:
    launch, «Купити», ×2 -> the shelf becomes a webinar card (a generic
    video tile, «Вебінар», her avatar) -> iris onto burgundy: her client's real
    landing page scrolls in a glass phone, the button is pressed -> the phone
    docks, a cable to the SendPulse bot, registration, the contact card fills
    with «?» for UTM -> the iris closes into the «?», which flies up into a
    card above her head: which reel, which ad? -> iris: the same funnel, a
    source added, one cable through every stage, a tick at each -> the iris
    closes into an address bar; the link types itself, the UTM tail turns
    pink, detaches as a chip and rides reel -> site -> button -> bot -> card
    -> it hides back in the link, which becomes a link chip -> iris: the link
    is tapped, the chip rides the real funnel and lands in the card: «?» ->
    instagram / reels, push in -> cards pour in behind her and sort into
    three columns by source -> her profile, Стежити -> Відстежується.

Her cut: two shots, 0-27.93 and 27.93-74.54, no pull-outs (tools/shots.py,
tools/pullouts.py). The first 2.7 s are her own gag the detectors can't see:
an extreme closeup hair flip at the lens (0-0.5), a zoom out to a model pose
at the back of the room (0.5-2.6), then she walks in. NO_PAINT.

Her answers (2026-09-28): the bot platform is SendPulse (no icon in
simple-icons: set as a wordmark, STYLE.md §0.2); the UTM fields are built as
graphics, not screenshots; the site scroll is real (work/media/r16).

usage: python build.py
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
from glass import Glass  # noqa: E402

DUR = 74.483           # 2235 plate frames / 30 (work/w40-queue2.log)
FPS = 30
k = Kit(width=1080, height=1920, fps=FPS, duration=DUR)
g = Glass()
k.css(g.css())

BEATS = []


def beat(fn):
    BEATS.append(fn)
    return fn


# ---------------------------------------------------------------------------
# NO-PAINT ZONES — her own editing (STYLE.md §4a). One: the entrance. She
# flips her hair into the lens, the frame zooms out to her posing at the back
# of the room, and she walks in on «клієнти?». Captions only.
NO_PAINT = [(0.00, 2.70)]

# ---------------------------------------------------------------------------
# Words: script spelling on her timing (work/r16/captions.json, settled by
# work/r16/caption-patch.json — «працює це», «яке ми їй», «маркетинг»).
CAPS = k.load_captions(os.path.join(ROOT, "work", "r16", "captions.json"))


def _n(s):
    return "".join(ch for ch in s.lower() if ch.isalnum())


def w(t, word):
    """Start of the caption at ~t that carries `word` — both must agree, so a
    re-run of align that shifts a word fails loudly instead of drifting."""
    c = min(CAPS, key=lambda c: abs(c["s"] - t))
    assert abs(c["s"] - t) < 0.08 and _n(word) in _n(c["w"]), (t, word, c["s"], c["w"])
    return c["s"]


def we(t, word):
    c = min(CAPS, key=lambda c: abs(c["s"] - t))
    assert abs(c["s"] - t) < 0.08 and _n(word) in _n(c["w"]), (t, word, c["s"], c["w"])
    return c["e"]


T = {
    # A · the hook
    "z": w(2.96, u"З"), "rilsa": w(3.34, u"рілса"), "stori": w(4.40, u"сторі"),
    "reklamy": w(5.40, u"реклами"), "yakshcho": w(6.10, u"Якщо"),
    "vtrach": w(6.90, u"втрачаєш"), "kupu": w(7.54, u"купу"),
    "vazhl": w(7.98, u"важливої"), "inform": w(8.46, u"інформації"),
    "ayakshcho": w(9.26, u"якщо"), "zapusk": w(10.06, u"запускаєш"),
    "produkty": w(10.68, u"продукти"), "prodav": w(11.60, u"продавати"),
    "vazhlyvo": w(13.16, u"важливо"), "vdvichi": w(13.74, u"вдвічі"),
    "bilshe_e": we(14.50, u"більше"),
    # B · the webinar
    "pokazuyu": w(14.90, u"Показую"), "prykladi": w(15.44, u"прикладі"),
    "vebinaru": w(15.76, u"вебінару"), "zapuskayu": w(17.22, u"запускаю"),
    "prodyus": w(17.84, u"продюсерка"),
    # C · over: the funnel
    "unas": w(18.40, u"У"), "sait": w(19.22, u"сайт"), "rozpys": w(19.80, u"розписано"),
    "vebinar2": w(20.64, u"вебінар"), "knopka": w(21.92, u"кнопка"),
    "vede": w(22.60, u"веде"), "chatbot": w(22.94, u"чат-бот"),
    "chatboti": w(23.80, u"чат-боті"), "vzhe": w(24.32, u"вже"),
    "reiestr": w(25.02, u"реєстрація"), "odrazu": w(25.92, u"одразу"),
    "zberih": w(26.38, u"зберігаються"), "dani": w(27.14, u"дані"),
    "lyudyny": w(27.66, u"людини"),
    # D · near: the questions
    "ishchob": w(28.04, u"щоб"), "zrozum": w(28.52, u"зрозуміти"),
    "zvidky2": w(29.08, u"звідки"), "reiestratsii": w(30.28, u"реєстрації"),
    "pratsyuye": w(31.44, u"працює"), "reklama": w(31.72, u"реклама"),
    "rilsiv": w(32.76, u"рілсів"), "bilshe2": w(33.68, u"більше"),
    "menshe": w(34.46, u"менше"),
    # E · over: end-to-end
    "unas2": w(35.14, u"нас"), "stoyit": w(35.30, u"стоїть"),
    "naskr": w(35.78, u"наскрізна"), "analit": w(36.56, u"аналітика"),
    "naskr2": w(37.46, u"Наскрізна"), "prokhod": w(38.54, u"проходить"),
    "cherez": w(38.96, u"через"), "kilka": w(39.28, u"кілька"),
    "etapiv": w(39.74, u"етапів"), "ne": w(40.40, u"не"),
    "tilky": w(40.92, u"тільки"), "kintsi": w(41.28, u"кінці"),
    # F · near: the link
    "i_prats": w(42.20, u"І"), "pratsyuye_tse": w(42.46, u"працює"),
    "utm1": w(43.96, u"UTM"), "utm2": w(45.25, u"UTM"),
    "inform2": w(46.70, u"інформація"), "pered": w(47.34, u"передається"),
    "dali1": w(47.98, u"далі"), "dali2": w(48.48, u"далі"),
    "dzherela": w(49.08, u"джерела"), "do": w(49.52, u"до"),
    "etapu": w(50.72, u"етапу"), "unashomu": w(51.52, u"У"),
    "khovayemo": w(52.48, u"ховаємо"), "posyl": w(53.58, u"посиланні"),
    "sait2": w(54.18, u"сайт"),
    # G · over: the payoff
    "i_fin": w(54.52, u"і"), "finalno": w(55.00, u"фінально"),
    "zberih2": w(55.66, u"зберігаються"), "chatboti2": w(56.62, u"чат-боті"),
    "tobto": w(57.54, u"Тобто"), "pereishla": w(58.48, u"перейшла"),
    "sekret": w(59.06, u"секретному"), "posylannyu": w(59.50, u"посиланню"),
    "dali_gave": w(60.58, u"дали"), "lyshayut": w(61.72, u"лишаються"),
    "pryamo": w(62.32, u"прямо"), "kartsi": w(63.08, u"картці"),
    "chatboti3": w(63.54, u"чат-боті"),
    # H · behind: segments
    "idali": w(64.28, u"і"), "sehment": w(65.52, u"сегментувати"),
    "lyudei": w(66.12, u"людей"), "rozdil": w(67.12, u"розділяти"),
    "pryishly": w(68.04, u"прийшли"), "redah": w(69.48, u"редагувати"),
    "market": w(70.10, u"маркетинг"),
    # I · follow
    "vpershe": w(70.90, u"вперше"), "proutm": w(71.54, u"UTM"),
    "totobi": w(72.26, u"тобі"), "obov": w(72.78, u"обов"),
    "pidp": w(73.68, u"підписатись"),
    "dur": DUR,
}


def js(src, **extra):
    """`@name` or `@name+0.12` -> a literal time. Literals, not variables,
    because tools/review.py reads the timeline off the generated numbers."""
    vals = dict(T)
    vals.update(extra)

    def rep(m):
        v = vals[m.group(1)] + (float(m.group(2)) if m.group(2) else 0.0)
        return "%.3f" % v
    return re.sub(r"@(\w+)([+-]\d+(?:\.\d+)?)?", rep, src)


def fill(s, **kw):
    for key, v in kw.items():
        s = s.replace("{{%s}}" % key, v if isinstance(v, str) else str(v))
    assert "{{" not in s, s[s.index("{{"):s.index("{{") + 40]
    return s


# ---------------------------------------------------------------------------
# Mattes (tools/matte.py via work/r16/mattes.sh): (first frame, frames).
# Soft rooms (work/r16/softroom.sh) are cut to exactly the same frames, so the
# room behind her goes out of focus without smearing her into a halo.
MATTES = {"hook": (87, 205), "segs": (1945, 180)}
for _name, (_f0, _n) in sorted(MATTES.items()):
    k.matte(_name, _f0 / 30.0, _n / 30.0)


def soft(name):
    f0, n = MATTES[name]
    return ('<video id="soft-%s" class="plate soft" src="assets/soft/%s.mp4" '
            'data-start="%.3f" data-duration="%.3f" data-media-start="0" muted playsinline></video>'
            % (name, name, f0 / 30.0, n / 30.0))


# ---------------------------------------------------------------------------
# Glyphs — strokes on a 24 grid, monochrome like the simple-icons marks.
def sk(body, cls="sk"):
    return '<svg class="%s" viewBox="0 0 24 24">%s</svg>' % (cls, body)


REELS = ('<rect x="3.2" y="3.2" width="17.6" height="17.6" rx="5"/><path d="M3.4 8.4h17.2M8.6 3.4l2.7 5M14.3 3.4l2.7 5"/>'
         '<path class="fl" d="M10.1 11.5v5.4l4.7-2.7z"/>')
STORY = ('<circle class="ring" cx="12" cy="12" r="9.4"/>'
         '<circle class="fl" cx="12" cy="10.2" r="2.6"/><path class="fl" d="M7.4 16.6c.9-2 2.6-3 4.6-3s3.7 1 4.6 3c-1.2 1.2-2.8 1.9-4.6 1.9s-3.4-.7-4.6-1.9z"/>')
ROCKET = ('<path d="M12 2.9c3.3 2.3 5 5.9 5 10.1l-2.2 3.1H9.2L7 13c0-4.2 1.7-7.8 5-10.1z"/>'
          '<circle cx="12" cy="9.7" r="1.9"/><path d="M7.1 13.5 4.3 16.4l3.4 1M16.9 13.5l2.8 2.9-3.4 1M10.4 19.2 12 21.6l1.6-2.4"/>')
GLOBE = ('<circle cx="12" cy="12" r="8.8"/><path d="M3.4 12h17.2M12 3.2c2.4 2.5 3.6 5.4 3.6 8.8s-1.2 6.3-3.6 8.8'
         'c-2.4-2.5-3.6-5.4-3.6-8.8S9.6 5.7 12 3.2z"/>')
CARDG = ('<rect x="2.8" y="5" width="18.4" height="14" rx="3.2"/><circle cx="8.8" cy="10.6" r="2.1"/>'
         '<path d="M5.7 15.9c.6-1.5 1.7-2.3 3.1-2.3s2.5.8 3.1 2.3M14.3 10h3.6M14.3 13.6h3.6"/>')
LINK = ('<path d="M10.2 13.8a4 4 0 0 0 5.7 0l3-3a4 4 0 0 0-5.7-5.7l-1.1 1.1M13.8 10.2a4 4 0 0 0-5.7 0l-3 3'
        'a4 4 0 0 0 5.7 5.7l1.1-1.1"/>')
LOCK = '<rect x="5" y="10.6" width="14" height="10" rx="2.6"/><path d="M8.2 10.6V7.9a3.8 3.8 0 0 1 7.6 0v2.7"/>'
TAG = ('<path d="M3.6 12.1V4.6a1 1 0 0 1 1-1h7.5l8.3 8.3a1.4 1.4 0 0 1 0 2l-6.3 6.3a1.4 1.4 0 0 1-2 0z"/>'
       '<circle cx="8" cy="8" r="1.5"/>')
UP = '<path d="M12 19V5.5M5.8 11.4 12 5.2l6.2 6.2"/>'
DOWN = '<path d="M12 5v13.5M5.8 12.6 12 18.8l6.2-6.2"/>'
CHECK_D = "M6.2 12.6l3.9 3.9 7.7-8.6"
PLAY = ('<rect x="2.8" y="4.4" width="18.4" height="15.2" rx="4"/>'
        '<path class="fl" d="M10 8.9v6.2l5.2-3.1z"/>')
PERSON = ('<svg viewBox="0 0 24 24"><circle cx="12" cy="9" r="4.3"/>'
          '<path d="M4.2 21c1.1-4.4 4.3-6.6 7.8-6.6s6.7 2.2 7.8 6.6z"/></svg>')


def check_svg(pid):
    return '<svg viewBox="0 0 24 24"><path id="%s" d="%s"/></svg>' % (pid, CHECK_D)


def sp_wm(size):
    """SendPulse has no simple-icons mark: its name, set as the wordmark."""
    return '<span class="spw" style="font-size:%dpx">SendPulse</span>' % size


k.css("""
.abs, .cx { position: absolute; }
.hide { opacity: 0; visibility: hidden; }
.plate.soft { position: absolute; left: 0; top: 0; }
/* stroke glyphs, sized by their box */
.sk { width: 50%; height: 50%; fill: none; stroke: url(#gw); stroke-width: 1.9;
  stroke-linecap: round; stroke-linejoin: round; position: relative; z-index: 1; }
.sk .fl { fill: url(#gw); stroke: none; }
.sk .ring { stroke: url(#gStory); stroke-width: 2.3; }
.pearl .sk { stroke: #17141c; } .pearl .sk .fl { fill: #17141c; }
.spw { font-weight: 900; letter-spacing: -0.035em; line-height: 1; color: #17141c; position: relative; z-index: 1; }
.jelly .spw { color: #fff; }
/* a tile wrapper: takes the motion, the tile inside takes the material */
.tw { position: absolute; }
/* the takeover's three light pools as one element (reel 15) */
.aurs { position: absolute; left: -700px; top: -700px; width: 2480px; height: 3320px; pointer-events: none;
  background:
    radial-gradient(circle 526px at 1560px 880px, rgba(255,110,156,0.50), rgba(255,110,156,0)),
    radial-gradient(circle 634px at 760px 2360px, rgba(222,32,74,0.55), rgba(222,32,74,0)),
    radial-gradient(circle 382px at 1480px 1910px, rgba(255,198,214,0.20), rgba(255,198,214,0)); }
/* dense dark tint where a backdrop blur would blow the heavy-element budget */
.dchip { position: absolute; color: #fff;
  background: linear-gradient(160deg, rgba(66,24,36,0.88) 0%, rgba(28,11,17,0.84) 100%);
  box-shadow: inset 0 1.5px 1px rgba(255,255,255,0.30), inset 0 -16px 30px -16px rgba(255,255,255,0.14),
              0 30px 60px -26px rgba(10,0,4,0.6); }
/* a round check: burgundy fill, white tick drawn on */
.rck { position: absolute; border-radius: 50%;
  background: linear-gradient(165deg, #ff7aa4 0%, #e0204b 50%, #8d0d24 100%);
  box-shadow: inset 0 2px 1px rgba(255,255,255,0.5), 0 14px 26px -10px rgba(70,4,20,0.7), 0 0 0 4px rgba(255,255,255,0.9); }
.rck svg { position: absolute; inset: 0; width: 100%; height: 100%; fill: none; stroke: #fff;
  stroke-width: 3.2; stroke-linecap: round; stroke-linejoin: round; }
/* the «?» — pink, heavy, the reel's one unknown */
.qm { font-weight: 900; letter-spacing: -0.04em; line-height: 1;
  background: linear-gradient(160deg, #ff8ab0 0%, #e0204b 55%, #8d0d24 100%);
  -webkit-background-clip: text; background-clip: text; color: transparent; }
.avc { position: absolute; border-radius: 50%; overflow: hidden;
  background: linear-gradient(160deg, #ffffff 0%, #f6e3e9 100%);
  box-shadow: inset 0 2px 1px #fff, 0 8px 18px -6px rgba(30,4,12,0.35); }
.avc svg { width: 100%; height: 100%; fill: rgba(180,18,47,0.42); transform: translateY(8%); }
.avc.me { background: url("assets/avatar.jpg") center / cover no-repeat;
  box-shadow: 0 0 0 4px rgba(255,255,255,0.85), 0 10px 22px -8px rgba(10,0,4,0.6); }
""")


# =================================================================== b01
k.css("""
/* ---- b01 · the client card with no source, and three sources that can't fill it ---- */
#g1tint { position: absolute; inset: 0;
  background: linear-gradient(180deg, rgba(62,8,24,0.20) 0%, rgba(40,5,15,0.34) 100%); }
#c1W { left: 250px; top: 150px; width: 580px; height: 330px; transform-origin: 290px 165px; }
#c1 { position: absolute; inset: 0; }
#c1av { left: 34px; top: 34px; width: 88px; height: 88px; }
#c1t { left: 142px; top: 38px; font-size: 38px; }
#c1s { left: 142px; top: 88px; }
.gbar { position: absolute; height: 26px; border-radius: 13px; background: rgba(23,20,28,0.10); }
#c1tb { left: 142px; top: 44px; width: 250px; } #c1sb { left: 142px; top: 92px; width: 170px; height: 20px; }
#c1h { left: 34px; right: 34px; top: 152px; }
#c1l { left: 34px; top: 180px; color: rgba(23,20,28,0.60); }
#c1slot { left: 34px; top: 216px; width: 512px; height: 84px; border-radius: 24px;
  border: 3px dashed rgba(180,18,47,0.32); background: rgba(251,227,234,0.5); }
#c1q { position: absolute; left: 0; right: 0; top: 4px; text-align: center; font-size: 66px; }
.cand { position: absolute; left: 226px; top: 12px; width: 56px; height: 56px; }
.cand .sk { width: 100%; height: 100%; stroke: #b4122f; } .cand .sk .fl { fill: #b4122f; }
.cand .sk .ring { stroke: #e0204b; }
.cand .mkc { width: 100%; height: 100%; fill: #b4122f; }
.cand b { position: absolute; left: 44px; top: -12px; width: 34px; height: 34px; border-radius: 50%;
  background: linear-gradient(165deg, #ff7aa4 0%, #e0204b 60%, #8d0d24 100%); color: #fff;
  font-size: 24px; font-weight: 900; line-height: 34px; text-align: center; }
.t1 { width: 150px; height: 150px; }
""")


@beat
def b01_no_source():
    """«З якого рілса, з якої сторі, з якої реклами? Якщо ні — то ти
    втрачаєш купу важливої інформації,»

    As she walks in, the room goes soft behind her and a new client's card
    lands above her head: «Нова клієнтка», and a dashed source slot with «?».
    Reels, Stories and Meta tiles land in the room on her three words; each
    is tried in the slot and the «?» comes back. On «втрачаєш» they drop out
    of the room behind her; on «інформації» the card itself empties to grey
    bars. Captions stay: nothing here says her words."""
    tiles = [("R", 57, 155, sk(REELS)), ("S", 873, 265, sk(STORY)), ("M", 57, 375, g.mark("meta"))]
    th = "".join('<div class="tw t1 hide" id="t1%s" style="left:%dpx;top:%dpx"><div class="clear edge">%s</div></div>'
                 % (key, x, y, glyph) for key, x, y, glyph in tiles)
    cands = "".join('<div class="cand hide" id="cd%s">%s<b>?</b></div>' % (key, glyph) for key, glyph in
                    (("R", sk(REELS)), ("S", sk(STORY)), ("M", g.mark("meta", "mkc"))))
    html = fill(u'''
      <div class="g full" id="g1">
        <div id="g1soft" class="hide">{{soft}}<div id="g1tint"></div></div>
        {{tiles}}
        <div id="c1W" class="abs hide">
          <div id="c1" class="sheet">
            <div class="cx avc" id="c1av">{{person}}</div>
            <div class="cx t-title" id="c1t">Нова клієнтка</div>
            <div class="cx t-sub" id="c1s">щойно · заявка</div>
            <div class="gbar hide" id="c1tb"></div><div class="gbar hide" id="c1sb"></div>
            <div class="cx hair" id="c1h"></div>
            <div class="cx t-micro" id="c1l">ДЖЕРЕЛО</div>
            <div class="cx" id="c1slot"><div class="qm" id="c1q">?</div>{{cands}}</div>
            <div class="sheen"></div>
          </div>
        </div>
      </div>''', soft=soft("hook"), tiles=th, person=PERSON, cands=cands)
    src = js('''
  tl.set("#g1", {autoAlpha: 1}, @z-0.06);
  // she walks in: the room goes soft behind her (matte `hook` puts her back sharp)
  tl.fromTo("#g1soft", {autoAlpha: 0}, {autoAlpha: 1, duration: 0.6, ease: "power1.inOut"}, @z-0.06);
  arr("#c1W", @z-0.04, {s: 0.55, y: 40});
  tl.fromTo(["#c1av", "#c1t", "#c1s"], {autoAlpha: 0, y: 14}, {autoAlpha: 1, y: 0, duration: 0.5, ease: SP, stagger: 0.05}, @z+0.10);
  tl.fromTo("#c1h", {scaleX: 0, transformOrigin: "0 0"}, {scaleX: 1, duration: 0.6, ease: "power3.out"}, @z+0.16);
  tl.fromTo(["#c1l", "#c1slot"], {autoAlpha: 0, y: 12}, {autoAlpha: 1, y: 0, duration: 0.45, ease: SP, stagger: 0.05}, @z+0.14);
  tl.fromTo("#c1q", {scale: 0.4, autoAlpha: 0}, {scale: 1, autoAlpha: 1, duration: 0.42, ease: POP}, @z+0.20);
  shn("#c1 .sheen", @z+0.40);

  // «рілса», «сторі», «реклами» — each source lands and is tried in the slot
  function tryit(key, t) {
    arr("#t1" + key, t - 0.10, {s: 0.5, y: 40});
    tl.fromTo("#t1" + key + " .mk, #t1" + key + " .sk", {scale: 0.55, autoAlpha: 0}, {scale: 1, autoAlpha: 1, duration: 0.55, ease: SP}, t);
    tl.to("#c1q", {autoAlpha: 0, scale: 0.6, duration: 0.12, ease: "power2.in"}, t + 0.28);
    tl.fromTo("#cd" + key, {autoAlpha: 0, scale: 0.5}, {autoAlpha: 1, scale: 1, duration: 0.45, ease: POP, immediateRender: false}, t + 0.36);
    G.bump("#c1slot", t + 0.36);
    tl.to("#cd" + key, {autoAlpha: 0, scale: 0.7, duration: 0.16, ease: "power2.in"}, t + 0.80);
    tl.to("#c1q", {autoAlpha: 1, scale: 1, duration: 0.3, ease: POP}, t + 0.90);
  }
  tryit("R", @rilsa);
  tryit("S", @stori);
  tryit("M", @reklamy);
  // «Якщо ні»
  G.haptic("#c1W", @yakshcho+0.30);

  // «втрачаєш» — the sources drop out of the room, behind her
  tl.to("#t1R", {y: 980, rotation: -24, duration: 1.05, ease: "power2.in"}, @vtrach);
  tl.to("#t1S", {y: 900, rotation: 20, duration: 1.05, ease: "power2.in"}, @vtrach+0.10);
  tl.to("#t1M", {y: 860, rotation: 16, duration: 1.05, ease: "power2.in"}, @vtrach+0.20);
  tl.to(["#t1R", "#t1S", "#t1M"], {autoAlpha: 0, duration: 0.3, ease: "power1.in"}, @vtrach+0.85);

  // «купу важливої інформації» — and what the card knew goes with them
  bout(["#c1t", "#c1s"], @vazhl, 8, 0.3);
  tl.fromTo(["#c1tb", "#c1sb"], {autoAlpha: 0}, {autoAlpha: 1, duration: 0.35, ease: "power1.out"}, @vazhl+0.14);
  tl.to("#c1av svg", {autoAlpha: 0.25, duration: 0.35}, @vazhl);
  tl.to("#c1q", {scale: 1.3, duration: 0.5, ease: POP}, @inform);
  G.haptic("#c1slot", @inform+0.12);

  // «а якщо» — the card folds up into the shelf above her head
  tl.to("#c1W", {scaleX: 1.62, scaleY: 0.9, y: 0, duration: 0.42, ease: "power3.in"}, @ayakshcho-0.10);
  bout("#c1W", @ayakshcho+0.06, 10, 0.26);
  tl.to("#g1soft", {autoAlpha: 0, duration: 0.4, ease: "power1.inOut"}, @ayakshcho-0.04);
  tl.to("#g1", {autoAlpha: 0, duration: 0.02}, @ayakshcho+0.36);''')
    return html, src


# =================================================================== b03
k.css("""
/* ---- b03 · near: the shelf — launch, sell, ×2 — then the webinar ---- */
#s3 { left: 70px; top: 150px; width: 940px; height: 300px; border-radius: 72px; overflow: hidden; }
#s3rk { left: 44px; top: 62px; width: 176px; height: 176px; }
#s3buy { left: 300px; top: 98px; width: 300px; height: 104px; border-radius: 52px; }
#s3buy .jelly { border-radius: 52px; }
#s3buy span { position: relative; z-index: 1; color: #fff; font-size: 42px; font-weight: 700; letter-spacing: -0.01em; }
#s3tap { left: 405px; top: 105px; width: 90px; height: 90px; border-radius: 50%;
  border: 4px solid rgba(255,255,255,0.95); background: rgba(255,255,255,0.18); }
#s3x2 { left: 646px; top: 44px; width: 260px; height: 210px; text-align: center; font-size: 200px; font-weight: 900;
  letter-spacing: -0.06em; line-height: 210px;
  background: linear-gradient(160deg, #ffffff 0%, #ffd0de 45%, #ff6e9c 100%);
  -webkit-background-clip: text; background-clip: text; color: transparent; }
#s3xr { left: 686px; top: 70px; width: 180px; height: 160px; border-radius: 40px; }
#s3th { left: 44px; top: 44px; width: 212px; height: 212px;
  box-shadow: 0 0 0 2px rgba(255,255,255,0.35), 0 24px 44px -18px rgba(0,0,0,0.6); }
#s3ti { left: 290px; top: 56px; font-size: 48px; font-weight: 700; letter-spacing: -0.02em; }
#s3su { left: 290px; top: 120px; font-size: 30px; font-weight: 500; color: rgba(255,255,255,0.74); }
#s3st { left: 290px; top: 176px; height: 64px; padding: 0 28px 0 22px; border-radius: 32px;
  display: flex; align-items: center; gap: 14px; font-size: 27px; font-weight: 700; color: #ffe1ea;
  background: rgba(255,110,156,0.24); box-shadow: inset 0 0 0 1.5px rgba(255,150,185,0.45); }
#s3st i { width: 16px; height: 16px; border-radius: 50%; background: #ff6e9c; display: block;
  box-shadow: 0 0 0 5px rgba(255,110,156,0.28); }
#s3av { left: 196px; top: 196px; width: 84px; height: 84px; }
#s3avr { left: 196px; top: 196px; width: 84px; height: 84px; border-radius: 50%; border: 3px solid rgba(255,150,185,0.95); }
""")


@beat
def b03_launch_webinar():
    """«а якщо ти при цьому запускаєш продукти і плануєш їх продавати, то тобі
    це важливо вдвічі більше. Показую на прикладі вебінару, який я прямо
    зараз запускаю як продюсерка.»

    The emptied card folds into a glass shelf above her head. A rocket tile
    launches on «запускаєш», a «Купити» button lands and is tapped on
    «продавати», ×2 lands on «вдвічі» (blackout: it says the word). On
    «Показую» the shelf becomes the webinar she produces — a video tile,
    «Вебінар» (blackout on «вебінару»: it says the word), «онлайн ·
    безкоштовно». Her change request (2026-09-29): none of the host's name or
    photo outside the site recording itself;
    «Реєстрація відкрита» lights on «запускаю», and her avatar docks on
    «продюсерка». The iris onto the site opens out of this shelf."""
    html = fill(u'''
      <div class="g full" id="g3">
        <div id="s3" class="dglass edge abs hide">
          <div class="tw hide" id="s3rk"><div class="jelly">{{rocket}}<div class="sheen"></div></div></div>
          <div class="tw hide" id="s3buy"><div class="jelly"><span>Купити</span></div></div>
          <div class="cx hide" id="s3tap"></div>
          <div class="sqring hide" id="s3xr"></div>
          <div class="cx hide" id="s3x2">×2</div>
          <div class="tw hide" id="s3th"><div class="jelly">{{play}}<div class="sheen"></div></div></div>
          <div class="cx hide" id="s3ti">Вебінар</div>
          <div class="cx hide" id="s3su">онлайн · безкоштовно</div>
          <div class="cx hide" id="s3st"><i></i>Реєстрація відкрита</div>
          <div class="cx hide" id="s3avr"></div>
          <div class="cx avc me hide" id="s3av"></div>
          <div class="sheen"></div>
        </div>
      </div>''', rocket=sk(ROCKET), play=sk(PLAY))
    src = js('''
  tl.set("#g3", {autoAlpha: 1}, @ayakshcho);
  // the card's frame arrives as the shelf
  bin("#s3", @ayakshcho, 12, 0.36);
  tl.fromTo("#s3", {scaleX: 0.62, scaleY: 1.1}, {scaleX: 1, scaleY: 1, duration: 0.8, ease: SP}, @ayakshcho);
  // «запускаєш продукти» — lift-off
  bin("#s3rk", @zapusk-0.06, 12, 0.3);
  tl.fromTo("#s3rk", {y: 150, scale: 0.6}, {y: 0, scale: 1, duration: 0.8, ease: POP}, @zapusk-0.06);
  tl.fromTo("#s3rk .sk", {y: 26}, {y: 0, duration: 0.7, ease: SP}, @zapusk+0.04);
  shn("#s3rk .sheen", @produkty);
  // «продавати» — a buy button, tapped
  arr("#s3buy", @prodav-0.06, {s: 0.5, y: 30});
  tl.fromTo("#s3tap", {autoAlpha: 0.9, scale: 0.3}, {autoAlpha: 0, scale: 1.6, duration: 0.6, ease: "power2.out", immediateRender: false}, @prodav+0.52);
  tl.to("#s3buy", {scale: 0.92, duration: 0.08, ease: "power2.out"}, @prodav+0.50);
  tl.to("#s3buy", {scale: 1, duration: 0.45, ease: POP}, @prodav+0.58);
  // «вдвічі більше» — ×2
  G.ripple("#s3xr", @vdvichi+0.08);
  bin("#s3x2", @vdvichi-0.04, 10, 0.3);
  tl.fromTo("#s3x2", {scale: 0.3}, {scale: 1, duration: 0.7, ease: POP}, @vdvichi-0.04);
  G.bump("#s3", @vdvichi+0.10);
  G.bump("#s3rk", @vdvichi+0.16); G.bump("#s3buy", @vdvichi+0.22);

  // «Показую» — the shelf becomes the webinar
  bout(["#s3rk", "#s3buy", "#s3x2"], @pokazuyu-0.08, 10, 0.28);
  arr("#s3th", @prykladi, {s: 0.55, y: 20});
  tl.fromTo("#s3th .sk", {scale: 0.55, autoAlpha: 0}, {scale: 1, autoAlpha: 1, duration: 0.5, ease: SP}, @prykladi+0.14);
  bin("#s3ti", @vebinaru-0.04, 10, 0.3);
  tl.fromTo("#s3ti", {x: -16}, {x: 0, duration: 0.6, ease: SP}, @vebinaru-0.04);
  bin("#s3su", @vebinaru+0.12, 10, 0.3);
  tl.fromTo("#s3su", {x: -16}, {x: 0, duration: 0.6, ease: SP}, @vebinaru+0.12);
  shn("#s3 > .sheen", @vebinaru+0.40);
  // «запускаю» — registration opens
  arr("#s3st", @zapuskayu-0.04, {s: 0.6, y: 0, x: -30});
  // «продюсерка» — her avatar docks on it
  tl.fromTo("#s3av", {autoAlpha: 0, scale: 0.3}, {autoAlpha: 1, scale: 1, duration: 0.55, ease: POP}, @prodyus-0.04);
  G.ripple("#s3avr", @prodyus+0.10);
  G.bump("#s3th", @prodyus+0.08);
  // «У нас є сайт» — the iris opens out of the shelf; it goes under the ground
  tl.to("#g3", {autoAlpha: 0, duration: 0.02}, @unas+0.38);''')
    return html, src


# =================================================================== the funnel
# One takeover, three visits: TK1 builds it (site -> button -> bot -> card),
# TK2 threads one cable through it, TK3 runs the link through it. Same DOM, so
# the state carries over from one visit to the next.
#
# Layout (final, frame px):  phone slot 60-346 x 110-612 (the phone is
# 572x1004 at scale 0.5) · bot 410-1020 x 110-710 · card 410-1020 x 780-1220 ·
# source tile 113-293 x 760-940 · link bubble 40-370 x 990-1066.
PH = (254, 110)                          # the phone at full size, centred
SLOT_X = 60 - PH[0]                      # -> x 60 at scale 0.5 (origin 0 0)
CAB = {
    "sp": "M 203 758 L 203 628",
    "pb": "M 346 562 C 384 562 374 470 412 470",
    "bc": "M 715 712 L 715 780",
}
# where the travelling chip sits (centre), stage by stage
CHIP = {"link": (205, 1028), "src": (203, 850), "srcTop": (203, 760), "ph": (203, 612),
        "btn": (346, 562), "bot": (430, 470), "botB": (715, 712), "card": (715, 780),
        "row": (915, 1061)}
CARD_C = (715, 1000)
PUSH_K = 1.4
PUSH = (540 - int(CARD_C[0] * PUSH_K), 660 - int(CARD_C[1] * PUSH_K))

k.css("""
/* ---- the funnel takeover: site in a glass phone, SendPulse, the contact card ---- */
#tkU { position: absolute; inset: 0; clip-path: circle(0px at 540px 300px); }
#uCam { position: absolute; inset: 0; transform-origin: 0 0; }
#uCab { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; overflow: visible; }
#uPhM { left: 254px; top: 110px; width: 572px; height: 1004px; transform-origin: 0 0; }
#uPhA { position: absolute; inset: 0; transform-origin: 286px 420px; }
#uPhF { position: absolute; inset: 0; border-radius: 84px;
  background: linear-gradient(160deg, rgba(70,24,38,0.94) 0%, rgba(22,8,13,0.96) 100%);
  box-shadow: inset 0 2px 1px rgba(255,255,255,0.35), inset 0 0 0 2px rgba(255,255,255,0.10),
              0 80px 140px -40px rgba(8,0,3,0.85), 0 0 0 1px rgba(255,255,255,0.18); }
#uPhS { position: absolute; left: 16px; top: 16px; width: 540px; height: 972px; border-radius: 68px;
  overflow: hidden; background: #fff; }
#uPhS img, #uPhS video { position: absolute; left: 0; top: 0; width: 540px; height: 972px; object-fit: cover; }
#uPhS .sheen { mix-blend-mode: normal; opacity: 0.35; }
#uBtnR { left: 38px; top: 864px; width: 510px; height: 126px; border-radius: 20px;
  border: 5px solid #ffffff; box-shadow: 0 0 26px 4px rgba(255,110,156,0.85), inset 0 0 18px rgba(255,110,156,0.6); }
#uTap { left: 238px; top: 872px; width: 110px; height: 110px; border-radius: 50%;
  border: 5px solid #fff; background: rgba(255,255,255,0.28); }

#uBotW { left: 410px; top: 110px; width: 610px; height: 600px; transform-origin: 305px 300px; }
#uBot { position: absolute; inset: 0; border-radius: 56px; }
#uSP { left: 30px; top: 30px; width: 232px; height: 76px; }
#uSP .jelly { border-radius: 38px; }
#uBn { left: 284px; top: 32px; font-size: 32px; font-weight: 700; letter-spacing: -0.015em; }
#uBo { left: 284px; top: 74px; font-size: 22px; font-weight: 500; color: rgba(23,20,28,0.64);
  display: flex; align-items: center; gap: 10px; }
#uBo i { width: 12px; height: 12px; border-radius: 50%; background: #ff6e9c; display: block; }
#uBh { left: 30px; right: 30px; top: 128px; }
.bb { position: absolute; max-width: 470px; padding: 16px 26px; border-radius: 30px; font-size: 28px;
  font-weight: 500; line-height: 36px; letter-spacing: -0.005em; white-space: nowrap; }
.bb.bot { left: 30px; background: #f4e3e8; color: #17141c; border-bottom-left-radius: 10px; }
.bb.me { right: 30px; color: #fff; border-bottom-right-radius: 10px;
  background: linear-gradient(160deg, #e0204b 0%, #ab112e 60%, #8d0d24 100%);
  box-shadow: inset 0 2px 1px rgba(255,255,255,0.35); }

#uCardW { left: 410px; top: 780px; width: 610px; height: 440px; transform-origin: 305px 220px; }
#uCard { position: absolute; inset: 0; border-radius: 56px; }
#uCav { left: 30px; top: 28px; width: 84px; height: 84px; }
#uCn { left: 134px; top: 30px; font-size: 38px; }
#uCs { left: 134px; top: 80px; font-size: 24px; }
#uCh { left: 30px; right: 30px; top: 136px; }
.crow { position: absolute; left: 30px; right: 30px; height: 74px; display: flex; align-items: center;
  justify-content: space-between; }
.crow .t-micro { font-size: 22px; color: rgba(23,20,28,0.60); }
.crow .v { font-size: 30px; font-weight: 700; letter-spacing: -0.01em; display: flex; align-items: center; gap: 12px; }
.crow .v svg { width: 34px; height: 34px; fill: #b4122f; }
.crow + .crow { border-top: 2px solid rgba(23,20,28,0.06); }
.qslot { position: absolute; right: 0; top: 9px; width: 150px; height: 56px; border-radius: 18px;
  border: 3px dashed rgba(180,18,47,0.32); background: rgba(251,227,234,0.5);
  display: flex; align-items: center; justify-content: center; font-size: 44px; }
.fillv { position: absolute; right: 0; top: 0; height: 74px; }
#uRowR { left: 26px; top: 238px; width: 558px; height: 82px; border-radius: 24px;
  box-shadow: 0 0 0 4px rgba(255,110,156,0.85), 0 0 30px rgba(255,110,156,0.5); }
#uRowR2 { left: 26px; top: 322px; width: 558px; height: 82px; border-radius: 24px;
  box-shadow: 0 0 0 4px rgba(255,110,156,0.85), 0 0 30px rgba(255,110,156,0.5); }

#uSrcW { left: 113px; top: 760px; width: 180px; height: 180px; }
#uSrcR { left: 113px; top: 760px; width: 180px; height: 180px; }
#uLink { left: 40px; top: 990px; width: 330px; height: 76px; border-radius: 38px;
  background: linear-gradient(170deg, #ffffff 0%, #fff4f7 100%); color: #17141c;
  box-shadow: 0 26px 50px -22px rgba(8,0,3,0.75), inset 0 2px 1px #fff;
  display: flex; align-items: center; gap: 12px; padding: 0 24px; font-size: 25px; font-weight: 700; white-space: nowrap; }
#uLink svg { width: 34px; height: 34px; fill: none; stroke: #b4122f; stroke-width: 2.2; stroke-linecap: round; flex: none; }
#uLink b { color: #e0204b; }
#uLtap { left: 150px; top: 973px; width: 110px; height: 110px; border-radius: 50%;
  border: 5px solid #fff; background: rgba(255,255,255,0.25); }
.tick { width: 64px; height: 64px; }
#uChip { left: 0; top: 0; width: 150px; height: 56px; margin: -28px 0 0 -75px; border-radius: 28px;
  display: flex; align-items: center; justify-content: center; gap: 8px; color: #fff; font-size: 26px; font-weight: 700;
  background: linear-gradient(160deg, #ff8ab0 0%, #e0204b 55%, #8d0d24 100%);
  box-shadow: inset 0 2px 1px rgba(255,255,255,0.55), 0 0 26px rgba(255,110,156,0.9), 0 14px 26px -10px rgba(70,4,20,0.7); }
#uChip svg { width: 28px; height: 28px; fill: none; stroke: #fff; stroke-width: 2.2; stroke-linejoin: round; }
""")


def funnel_html():
    cab = "".join('<path class="tube" id="ct-%s" d="%s"/><path class="core" id="cc-%s" d="%s"/>'
                  '<g class="pkg"><path class="pkt hide" id="cp-%s" d="%s"/></g>' % (n, d, n, d, n, d)
                  for n, d in sorted(CAB.items()))
    ticks = [("src", 261, 734), ("ph", 314, 84), ("bot", 978, 80), ("card", 978, 750)]
    tk = "".join('<div class="rck tick hide" id="tk-%s" style="left:%dpx;top:%dpx">%s</div>'
                 % (n, x, y, check_svg("tkp-" + n)) for n, x, y in ticks)
    return fill(u'''
      <div class="g full" id="gU">
        <div id="tkU">
          <div class="tkg"></div><div class="aurs"></div><div class="grain"></div>
          <div id="uCam">
            <svg id="uCab" class="cab" viewBox="0 0 1080 1920">{{cab}}</svg>
            <div class="tw hide" id="uSrcW"><div class="jelly">{{reels}}<div class="sheen"></div></div></div>
            <div class="sqring hide" id="uSrcR"></div>
            <div class="cx hide" id="uLink">{{link}}<span>site.com/<b>?utm…</b></span></div>
            <div class="cx hide" id="uLtap"></div>
            <div class="abs hide" id="uPhM"><div id="uPhA">
              <div id="uPhF" class="edge"></div>
              <div id="uPhS">
                <img id="siteStill" class="hide" src="assets/site-end.jpg" alt="">
                <video id="siteV" src="assets/site.mp4" data-start="{{vs}}" data-duration="{{vd}}"
                       data-media-start="0" muted playsinline></video>
                <div class="sheen"></div>
              </div>
              <div class="cx hide" id="uBtnR"></div>
              <div class="cx hide" id="uTap"></div>
            </div></div>
            <div class="abs hide" id="uBotW"><div id="uBot" class="sheet">
              <div class="tw" id="uSP"><div class="jelly">{{spw}}<div class="sheen"></div></div></div>
              <div class="cx" id="uBn">Вебінар</div>
              <div class="cx" id="uBo"><i></i>онлайн</div>
              <div class="cx hair" id="uBh"></div>
              <div class="bb bot hide" id="bb1" style="top:156px">Привіт! Як тебе звати?</div>
              <div class="bb me hide" id="bb2" style="top:242px">Олена</div>
              <div class="bb bot hide" id="bb3" style="top:328px">Залиш номер — нагадаю про ефір</div>
              <div class="bb me hide" id="bb4" style="top:414px">+380 67 ••• •• 17</div>
              <div class="sheen"></div>
            </div></div>
            <div class="abs hide" id="uCardW"><div id="uCard" class="sheet">
              <div class="cx avc" id="uCav">{{person}}</div>
              <div class="cx t-title hide" id="uCn">Олена</div>
              <div class="cx t-sub hide" id="uCs">SendPulse · щойно</div>
              <div class="gbar" id="uCnb" style="left:134px;top:38px;width:220px"></div>
              <div class="gbar" id="uCsb" style="left:134px;top:86px;width:160px;height:20px"></div>
              <div class="cx hair" id="uCh"></div>
              <div class="crow" style="top:160px"><span class="t-micro">ТЕЛЕФОН</span>
                <span class="v hide" id="uCph">+380 67 ••• •• 17</span></div>
              <div class="crow" style="top:244px"><span class="t-micro">UTM_SOURCE</span>
                <div class="qslot hide" id="uQ1"><span class="qm">?</span></div>
                <span class="v fillv hide" id="uV1">{{ig}}instagram</span></div>
              <div class="crow" style="top:328px"><span class="t-micro">UTM_MEDIUM</span>
                <div class="qslot hide" id="uQ2"><span class="qm">?</span></div>
                <span class="v fillv hide" id="uV2">reels</span></div>
              <div class="cx hide" id="uRowR"></div><div class="cx hide" id="uRowR2"></div>
              <div class="sheen"></div>
            </div></div>
            {{ticks}}
            <div class="cx hide" id="uChip" data-layout-allow-overlap>{{tag}}utm</div>
          </div>
        </div>
      </div>''', cab=cab, reels=sk(REELS), link=sk(LINK, ""), spw=sp_wm(34), person=PERSON,
                ig=g.mark("instagram", ""), ticks=tk, tag=sk(TAG, ""),
                vs="%.3f" % SITE[0], vd="%.3f" % SITE[1])


# the site clip (work/r16/site.sh): starts with the phone, ends frozen
SITE = (18.450, 9.800)


def chip_to(key, t, d, ease="power2.inOut"):
    x, y = CHIP[key]
    return '  tl.to("#uChip", {x: %d, y: %d, duration: %.2f, ease: "%s"}, %.3f);' % (x, y, d, ease, t)


@beat
def b06_funnel_site_bot_card():
    """«У нас є сайт, де розписано все про вебінар, на сайті є кнопка, яка
    веде в чат-бот, і в цьому чат-боті вже проходить реєстрація і одразу
    зберігаються дані людини.»

    TK1. The iris opens out of the webinar shelf onto burgundy and a glass
    phone grows out of it playing her client's real landing page: the hero
    («прибутковий блонд») on «сайт», a fast scroll through everything on
    «розписано все», the sticky «Зареєструватися» button ringed and tapped on
    «кнопка». On «веде в чат-бот» the phone docks left and a cable draws to
    the SendPulse bot; registration runs as four bubbles on «реєстрація»; on
    «зберігаються дані людини» a cable drops to the contact card and it fills
    — name, phone — and its two UTM fields land empty: «?». The iris closes
    into that «?»."""
    src = js('''
  tl.set("#gU", {autoAlpha: 1}, @unas);
  gsap.set(["#uCard .t-micro", "#uCard .crow"], {autoAlpha: 1});
  G.irisOpen("#tkU", @unas, 540, 300, 0.85);
  drift1("#tkU", @unas, 9.8);
  ["sp", "pb", "bc"].forEach(function (n) { G.drawPrep("ct-" + n); G.drawPrep("cc-" + n); });
  // the phone grows out of the iris point; the page is live
  tl.set("#uPhM", {autoAlpha: 1}, @unas+0.05);
  bin("#uPhA", @unas+0.05, 16, 0.45);
  tl.fromTo("#uPhA", {scale: 0.3}, {scale: 1, duration: 1.0, ease: spring(0.72, 12)}, @unas+0.05);
  // «сайт»
  shn("#uPhS .sheen", @sait);
  // «на сайті є кнопка» — the sticky button, ringed and tapped
  tl.fromTo("#uBtnR", {autoAlpha: 0, scale: 1.12}, {autoAlpha: 1, scale: 1, duration: 0.4, ease: POP}, @knopka-0.10);
  tl.fromTo("#uTap", {autoAlpha: 0.95, scale: 0.3}, {autoAlpha: 0, scale: 1.7, duration: 0.6, ease: "power2.out", immediateRender: false}, @knopka+0.20);
  G.bump("#uPhA", @knopka+0.18);
  // «яка веде в чат-бот» — the phone docks, a cable to the bot
  tl.to("#uBtnR", {autoAlpha: 0, duration: 0.2}, @vede-0.20);
  tl.to("#uPhM", {x: -194, scale: 0.5, duration: 0.62, ease: SP}, @vede-0.22);
  arr("#uBotW", @vede, {s: 0.5, y: 40});
  tl.fromTo(["#uSP", "#uBn", "#uBo"], {autoAlpha: 0, y: 12}, {autoAlpha: 1, y: 0, duration: 0.5, ease: SP, stagger: 0.06}, @vede+0.18);
  tl.fromTo("#uBh", {scaleX: 0, transformOrigin: "0 0"}, {scaleX: 1, duration: 0.6, ease: "power3.out"}, @vede+0.26);
  tl.to(["#ct-pb", "#cc-pb"], {strokeDashoffset: 0, duration: 0.4, ease: "power2.inOut"}, @chatbot);
  G.packet("cp-pb", @chatbot+0.30, 0.4);
  G.bump("#uBotW", @chatboti);
  shn("#uSP .sheen", @chatboti+0.06);
  // «вже проходить реєстрація»
  tl.fromTo("#bb1", {autoAlpha: 0, y: 18, scale: 0.9, transformOrigin: "0% 100%"}, {autoAlpha: 1, y: 0, scale: 1, duration: 0.45, ease: SP}, @vzhe);
  tl.fromTo("#bb2", {autoAlpha: 0, y: 18, scale: 0.9, transformOrigin: "100% 100%"}, {autoAlpha: 1, y: 0, scale: 1, duration: 0.45, ease: SP}, @vzhe+0.42);
  tl.fromTo("#bb3", {autoAlpha: 0, y: 18, scale: 0.9, transformOrigin: "0% 100%"}, {autoAlpha: 1, y: 0, scale: 1, duration: 0.45, ease: SP}, @reiestr);
  tl.fromTo("#bb4", {autoAlpha: 0, y: 18, scale: 0.9, transformOrigin: "100% 100%"}, {autoAlpha: 1, y: 0, scale: 1, duration: 0.45, ease: SP}, @reiestr+0.44);
  // «одразу зберігаються дані людини» — the contact card
  tl.to(["#ct-bc", "#cc-bc"], {strokeDashoffset: 0, duration: 0.3, ease: "power2.inOut"}, @odrazu);
  G.packet("cp-bc", @odrazu+0.22, 0.3);
  arr("#uCardW", @odrazu+0.12, {s: 0.5, y: -30});
  bout(["#uCnb", "#uCsb"], @zberih, 6, 0.2);
  bin("#uCn", @zberih+0.02, 8, 0.3);
  bin("#uCs", @zberih+0.14, 8, 0.3);
  bin("#uCph", @zberih+0.34, 8, 0.3);
  tl.fromTo("#uQ1", {autoAlpha: 0, scale: 0.5}, {autoAlpha: 1, scale: 1, duration: 0.5, ease: POP}, @dani);
  tl.fromTo("#uQ2", {autoAlpha: 0, scale: 0.5}, {autoAlpha: 1, scale: 1, duration: 0.5, ease: POP}, @dani+0.16);
  shn("#uCard .sheen", @dani+0.10);
  G.haptic("#uCardW", @lyudyny+0.04);
  // the iris closes into the «?»
  G.irisClose("#tkU", @lyudyny+0.24, 915, 1061, 0.45);
  tl.set("#siteV", {autoAlpha: 0}, @lyudyny+0.71);
  tl.set("#siteStill", {autoAlpha: 1}, @lyudyny+0.71);
  tl.to("#gU", {autoAlpha: 0, duration: 0.02}, @lyudyny+0.71);''')
    return funnel_html(), src


# =================================================================== b09
k.css("""
/* ---- b09 · near: the card above her head — which reel, which ad? ---- */
#q9 { left: 90px; top: 160px; width: 900px; height: 190px; border-radius: 64px; overflow: hidden; }
.q9b { left: 90px; top: 160px; width: 900px; height: 190px; border-radius: 64px; transform-origin: 450px 0; }
#q9av { left: 34px; top: 40px; width: 110px; height: 110px; }
#q9n { left: 172px; top: 44px; font-size: 44px; font-weight: 700; letter-spacing: -0.015em; }
#q9p { left: 172px; top: 104px; font-size: 28px; font-weight: 500; color: rgba(255,255,255,0.72); }
#q9slot { left: 648px; top: 34px; width: 214px; height: 122px; }
#q9slot .jelly { border-radius: 36px; }
#q9lab { position: absolute; left: 0; right: 0; top: 16px; text-align: center; font-size: 20px; font-weight: 700;
  letter-spacing: 0.16em; color: rgba(255,255,255,0.72); z-index: 1; }
#q9q { left: 0; top: 0; width: 60px; height: 72px; margin: -36px 0 0 -30px; text-align: center; font-size: 72px;
  font-weight: 900; line-height: 72px; color: #fff; }
#q9sr { left: 648px; top: 34px; width: 214px; height: 122px; border-radius: 36px; }
.t9 { width: 150px; height: 150px; }
.c9 { position: absolute; height: 72px; border-radius: 36px; display: flex; align-items: center;
  justify-content: center; font-size: 44px; font-weight: 900; }
.c9 svg { width: 40px; height: 40px; fill: none; stroke-width: 3; stroke-linecap: round; stroke-linejoin: round; }
.c9.pk { color: #fff; background: linear-gradient(160deg, #ff8ab0 0%, #e0204b 55%, #8d0d24 100%);
  box-shadow: inset 0 2px 1px rgba(255,255,255,0.5), 0 20px 36px -14px rgba(70,4,20,0.7); }
.c9.pk svg { stroke: #fff; }
.c9.pl { color: #17141c; background: linear-gradient(160deg, #ffffff 0%, #fff5f8 52%, #f5dfe6 100%);
  box-shadow: inset 0 2px 1px #fff, 0 20px 36px -14px rgba(30,4,12,0.55); }
.c9.pl svg { stroke: #17141c; }
""")


@beat
def b09_which_one():
    """«І щоб зрозуміти, звідки саме прийшли ці реєстрації, чи добре працює
    реклама, і яких рілсів нам знімати більше, а яких менше,»

    The «?» the iris closed into flies up into a card above her head — Олена,
    her phone, and a pink source slot holding the «?». It rings on «звідки»,
    two more registrations stack in behind it on «ці реєстрації». A Meta
    tile lands with its own «?» on «реклама»; a Reels tile on «рілсів», an
    up arrow on «більше», a down arrow on «менше». The iris into the funnel
    opens out of the card."""
    html = fill(u'''
      <div class="g full" id="g9">
        <div class="dchip q9b hide" id="q9b2"></div>
        <div class="dchip q9b hide" id="q9b1"></div>
        <div id="q9" class="dglass edge abs hide">
          <div class="cx avc hide" id="q9av">{{person}}</div>
          <div class="cx hide" id="q9n">Олена</div>
          <div class="cx hide" id="q9p">+380 67 ••• •• 17</div>
          <div class="tw hide" id="q9slot"><div class="jelly"><div id="q9lab">ДЖЕРЕЛО</div></div></div>
          <div class="sheen"></div>
        </div>
        <div class="sqring hide" id="q9sr"></div>
        <div class="cx hide" id="q9q">?</div>
        <div class="tw t9 hide" id="t9M" style="left:170px;top:386px"><div class="clear edge">{{meta}}</div></div>
        <div class="c9 pk hide" id="c9M" style="left:336px;top:425px;width:92px">?</div>
        <div class="tw t9 hide" id="t9R" style="left:652px;top:386px"><div class="clear edge">{{reels}}</div></div>
        <div class="c9 pk hide" id="c9U" style="left:818px;top:384px;width:110px">{{up}}</div>
        <div class="c9 pl hide" id="c9D" style="left:818px;top:466px;width:110px">{{down}}</div>
      </div>''', person=PERSON, meta=g.mark("meta"), reels=sk(REELS),
                up=sk(UP, ""), down=sk(DOWN, ""))
    src = js('''
  tl.set("#g9", {autoAlpha: 1}, @ishchob);
  // the «?» flies up out of the closing iris into its slot
  tl.set("#q9q", {autoAlpha: 1, x: 915, y: 1061, scale: 0.7}, @ishchob);
  tl.to("#q9q", {x: 845, y: 274, scale: 1, duration: 0.7, ease: SP}, @ishchob);
  arr("#q9", @ishchob, {s: 0.7, y: 30});
  tl.fromTo("#q9slot", {autoAlpha: 0, scale: 0.6}, {autoAlpha: 1, scale: 1, duration: 0.55, ease: POP}, @ishchob+0.22);
  tl.fromTo(["#q9av", "#q9n", "#q9p"], {autoAlpha: 0, x: -14}, {autoAlpha: 1, x: 0, duration: 0.5, ease: SP, stagger: 0.06}, @ishchob+0.14);
  shn("#q9 .sheen", @zrozum);
  // «звідки саме прийшли»
  G.bump("#q9q", @zvidky2);
  G.ripple("#q9sr", @zvidky2+0.04);
  // «ці реєстрації» — two more stack in behind it
  tl.fromTo("#q9b1", {autoAlpha: 0, y: 0, scale: 1}, {autoAlpha: 0.9, y: -34, scale: 0.95, duration: 0.55, ease: SP}, @reiestratsii);
  tl.fromTo("#q9b2", {autoAlpha: 0, y: 0, scale: 1}, {autoAlpha: 0.75, y: -64, scale: 0.9, duration: 0.55, ease: SP}, @reiestratsii+0.14);
  // «чи добре працює реклама»
  arr("#t9M", @pratsyuye, {s: 0.5, y: 40});
  tl.fromTo("#t9M .mk", {scale: 0.55, autoAlpha: 0}, {scale: 1, autoAlpha: 1, duration: 0.55, ease: SP}, @pratsyuye+0.10);
  tl.fromTo("#c9M", {autoAlpha: 0, scale: 0.4}, {autoAlpha: 1, scale: 1, duration: 0.5, ease: POP}, @reklama);
  // «яких рілсів нам знімати більше, а яких менше»
  arr("#t9R", @rilsiv-0.08, {s: 0.5, y: 40});
  tl.fromTo("#t9R .sk", {scale: 0.55, autoAlpha: 0}, {scale: 1, autoAlpha: 1, duration: 0.55, ease: SP}, @rilsiv+0.02);
  tl.fromTo("#c9U", {autoAlpha: 0, scale: 0.4, y: 20}, {autoAlpha: 1, scale: 1, y: 0, duration: 0.5, ease: POP}, @bilshe2);
  tl.fromTo("#c9D", {autoAlpha: 0, scale: 0.4, y: -20}, {autoAlpha: 1, scale: 1, y: 0, duration: 0.5, ease: POP}, @menshe);
  // «у нас стоїть» — everything folds back into the card; the iris opens out of it
  bout(["#t9M", "#c9M", "#t9R", "#c9U", "#c9D"], @unas2-0.10, 10, 0.26);
  tl.to("#g9", {autoAlpha: 0, duration: 0.02}, @unas2+0.36);''')
    return html, src


# =================================================================== b10
@beat
def b10_end_to_end():
    """«у нас стоїть наскрізна аналітика. Наскрізна вона тому, що проходить
    через кілька етапів, а не фіксується тільки в кінці.»

    TK2. The iris opens back onto the same funnel — site, SendPulse, the card
    with its «?» — and the first stage joins it: the Reels tile, cabled up
    into the phone. One packet runs the whole length on «наскрізна»; on
    «кілька етапів» a tick lands at every stage in turn, reel · site · bot ·
    card; on «а не … тільки в кінці» the first three ring together and the
    last one last. The iris closes into the address bar."""
    src = js('''
  tl.set("#gU", {autoAlpha: 1}, @unas2);
  G.irisOpen("#tkU", @unas2, 540, 255, 0.8);
  drift1("#tkU", @unas2, 7.0);
  // «стоїть» — the source joins the funnel
  arr("#uSrcW", @stoyit, {s: 0.5, y: 40});
  tl.fromTo("#uSrcW .sk", {scale: 0.55, autoAlpha: 0}, {scale: 1, autoAlpha: 1, duration: 0.55, ease: SP}, @stoyit+0.10);
  tl.to(["#ct-sp", "#cc-sp"], {strokeDashoffset: 0, duration: 0.4, ease: "power2.inOut"}, @stoyit+0.30);
  // «наскрізна аналітика» — one packet runs the whole length
  G.packet("cp-sp", @naskr, 0.34);
  G.bump("#uPhA", @naskr+0.30);
  G.packet("cp-pb", @naskr+0.36, 0.34);
  G.bump("#uBotW", @naskr+0.66);
  G.packet("cp-bc", @naskr+0.72, 0.28);
  G.bump("#uCardW", @naskr+0.98);
  shn("#uSrcW .sheen", @analit);
  // «Наскрізна вона тому» — again, quicker
  G.packet("cp-sp", @naskr2, 0.26); G.packet("cp-pb", @naskr2+0.24, 0.26); G.packet("cp-bc", @naskr2+0.48, 0.24);
  // «через кілька етапів» — a tick at every stage
  function tick(n, t) {
    tl.fromTo("#tk-" + n, {autoAlpha: 0, scale: 0.3}, {autoAlpha: 1, scale: 1, duration: 0.5, ease: POP}, t);
    G.draw("tkp-" + n, t + 0.08, 0.3);
  }
  tick("src", @prokhod+0.06); tick("ph", @cherez); tick("bot", @kilka); tick("card", @etapiv);
  // «а не фіксується тільки в кінці»
  G.bump("#tk-src", @ne); G.bump("#tk-ph", @ne+0.06); G.bump("#tk-bot", @ne+0.12);
  G.bump("#tk-card", @kintsi);
  // into the address bar
  G.irisClose("#tkU", @kintsi+0.40, 540, 212, 0.55);
  tl.to("#gU", {autoAlpha: 0, duration: 0.02}, @kintsi+0.98);''')
    return "", src


# =================================================================== b11
URL_D = "site.com/"
URL_T = "?utm_source=instagram&amp;utm_medium=reels"
NODES = [("n1", 150, "jelly", sk(REELS)), ("n2", 345, "pearl", sk(GLOBE)),
         ("n3", 540, "pearl", '<i class="mbtn"></i>'), ("n4", 735, "pearl", sp_wm(25)),
         ("n5", 930, "jelly", sk(CARDG))]
k.css("""
/* ---- b11 · near: the link, its UTM tail, and where the tail goes ---- */
#ub { left: 60px; top: 150px; width: 960px; height: 124px; border-radius: 62px; transform-origin: 480px 62px; }
#ubL { left: 38px; top: 38px; width: 48px; height: 48px; }
#ubL svg, #ubK svg { width: 48px; height: 48px; fill: none; stroke: #fff; stroke-width: 2; stroke-linecap: round; stroke-linejoin: round; }
#ubK { left: 38px; top: 38px; width: 48px; height: 48px; }
#ubK svg { stroke: #ff9cbc; }
#ubX { left: 106px; top: 0; height: 124px; line-height: 124px; font-size: 31px; font-weight: 500;
  white-space: nowrap; color: rgba(255,255,255,0.86); letter-spacing: -0.005em; }
#ubT { color: #fff; font-weight: 700; padding: 4px 2px; border-radius: 10px;
  background-image: linear-gradient(rgba(255,110,156,0.62), rgba(255,110,156,0.62));
  background-repeat: no-repeat; background-position: 0 50%; background-size: 0% 100%; }
#ubR { left: 60px; top: 150px; width: 960px; height: 124px; border-radius: 62px; }
#uc { left: 0; top: 0; width: 560px; height: 128px; margin: -64px 0 0 -280px; border-radius: 42px; }
#uc .jelly { border-radius: 42px; justify-content: flex-start; padding-left: 34px; gap: 22px; }
#uc svg { width: 50px; height: 50px; fill: none; stroke: #fff; stroke-width: 2; stroke-linejoin: round;
  position: relative; z-index: 1; flex: none; }
#uc .ln { position: relative; z-index: 1; color: #fff; font-size: 30px; font-weight: 700; line-height: 40px;
  letter-spacing: -0.005em; white-space: nowrap; }
#pipe { left: 40px; top: 410px; width: 1000px; height: 150px; border-radius: 75px; }
#pipeC { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; overflow: visible; }
.nd { position: absolute; width: 104px; height: 104px; margin: -52px 0 0 -52px; }
.nd.wide { width: 170px; margin-left: -85px; }
.nd.wide .pearl { border-radius: 30px; }
.nd .mbtn { position: relative; z-index: 1; display: block; width: 58px; height: 26px; border-radius: 8px;
  background: linear-gradient(160deg, #ff8ab0 0%, #ff4f86 100%); box-shadow: 0 0 0 3px rgba(255,79,134,0.25); }
.ndr { position: absolute; width: 104px; height: 104px; margin: -52px 0 0 -52px; }
""")


@beat
def b11_the_link():
    """«І працює це все добре на UTM-мітках. UTM-мітка — це просто
    інформація, яка передається далі і далі, з одного джерела до самого
    кінцевого етапу. У нашому випадку ми ховаємо ці мітки в посиланні на
    сайт,»

    The iris closes into an address bar above her head and the link types
    itself; on «UTM-мітках» its `?utm_…` tail is marked pink. On «UTM-мітка»
    the tail lifts off as a pink chip — utm_source=instagram / utm_medium=
    reels — and on «передається далі і далі» a glass rail of the five stages
    draws under it: reel, site, button, SendPulse, card. On «з одного джерела»
    the chip drops onto the reel; «до самого кінцевого етапу» it rides the
    rail to the card. On «ховаємо» it flies back and sinks into the link, the
    tail goes quiet, and on «посиланні» the bar shrinks to a link chip. The
    captions stay: the bar reads `utm_`, not the word she says."""
    nodes = "".join('<div class="nd%s hide" id="%s" style="left:%dpx;top:485px"><div class="%s">%s</div></div>'
                    % (" wide" if n == "n4" else "", n, x, mat, glyph) for n, x, mat, glyph in NODES)
    rips = "".join('<div class="ndr sqring hide" id="%sr" style="left:%dpx;top:485px"></div>' % (n, x)
                   for n, x, _, _ in NODES)
    html = fill(u'''
      <div class="g full" id="g11">
        <div id="pipe" class="dglass edge abs hide"></div>
        <svg id="pipeC" class="cab" viewBox="0 0 1080 1920">
          <path class="tube" id="pT" d="M 150 485 L 930 485"/><path class="core" id="pC" d="M 150 485 L 930 485"/>
        </svg>
        {{nodes}}{{rips}}
        <div class="sqring hide" id="ubR"></div>
        <div id="ub" class="dglass edge abs hide">
          <div class="cx" id="ubL">{{lock}}</div>
          <div class="cx hide" id="ubK">{{link}}</div>
          <div class="cx" id="ubX"><span id="ubD">{{d}}</span><span id="ubT" data-layout-allow-overlap>{{t}}</span></div>
        </div>
        <div class="tw hide" id="uc" data-layout-allow-overlap><div class="jelly">{{tag}}<div class="ln" data-layout-allow-overlap>utm_source=instagram<br>utm_medium=reels</div>
          <div class="sheen"></div></div></div>
      </div>''', nodes=nodes, rips=rips, lock=sk(LOCK, ""), link=sk(LINK, ""), d=URL_D, t=URL_T,
                tag=sk(TAG, ""))
    src = js('''
  tl.set("#g11", {autoAlpha: 1}, @kintsi+0.72);
  // the bar opens out of the closing iris; the link types itself
  arr("#ub", @kintsi+0.72, {s: 0.4, y: 0});
  tl.fromTo("#ubX", {clipPath: "inset(0px 100% 0px 0px)"}, {clipPath: "inset(0px 0% 0px 0px)", duration: 1.3,
            ease: "steps(48)"}, @pratsyuye_tse);
  // «UTM-мітках» — the tail is marked
  tl.to("#ubT", {backgroundSize: "100% 100%", duration: 0.45, ease: "power2.out"}, @utm1);
  G.bump("#ub", @utm1+0.30);
  // «UTM-мітка» — it lifts off as a chip
  tl.set("#uc", {x: 610, y: 212, scale: 0.55}, @utm2-0.02);
  tl.fromTo("#uc", {autoAlpha: 0}, {autoAlpha: 1, duration: 0.2}, @utm2-0.02);
  tl.to("#uc", {x: 540, y: 344, scale: 1, duration: 0.7, ease: SP}, @utm2);
  tl.to("#ubT", {opacity: 0.22, duration: 0.3}, @utm2);
  // «інформація»
  shn("#uc .sheen", @inform2);
  G.bump("#uc", @inform2+0.06);
  // «передається далі і далі» — the rail of stages draws under it
  bin("#pipe", @pered-0.06, 12, 0.34);
  tl.fromTo("#pipe", {scaleX: 0.6}, {scaleX: 1, duration: 0.7, ease: SP}, @pered-0.06);
  G.draw("pT", @pered+0.10, 0.9); G.draw("pC", @pered+0.10, 0.9);
  NODEJS
  // «з одного джерела» — the chip drops onto the reel
  tl.to("#uc", {x: 150, y: 400, scale: 0.36, duration: 0.5, ease: SP}, @dzherela-0.10);
  G.ripple("#n1r", @dzherela+0.30);
  // «до самого кінцевого етапу» — it rides the rail to the card
  tl.to("#uc", {x: 930, duration: 1.1, ease: "power1.inOut"}, @do);
  G.bump("#n2", @do+0.22); G.bump("#n3", @do+0.50); G.bump("#n4", @do+0.78);
  tl.to("#uc", {y: 485, scale: 0.3, duration: 0.3, ease: "power2.in"}, @etapu-0.10);
  G.ripple("#n5r", @etapu+0.12);
  G.bump("#n5", @etapu+0.14);
  // «У нашому випадку» — the rail clears; «ховаємо» — the chip sinks back into the link
  bout(["#pipe", "#pipeC", "#n1", "#n2", "#n3", "#n4", "#n5"], @unashomu-0.04, 10, 0.32);
  tl.to("#uc", {x: 610, y: 330, scale: 0.7, duration: 0.6, ease: SP}, @unashomu+0.10);
  tl.to("#uc", {y: 212, autoAlpha: 0, scale: 0.4, duration: 0.26, ease: "power2.in"}, @khovayemo-0.04);
  tl.to("#ubT", {opacity: 1, duration: 0.2}, @khovayemo+0.10);
  tl.to("#ubT", {backgroundSize: "0% 100%", color: "rgba(255,255,255,0.86)", fontWeight: 500, duration: 0.5,
                 ease: "power2.inOut"}, @khovayemo+0.26);
  G.bump("#ub", @khovayemo+0.12);
  // «в посиланні» — the bar becomes a link
  tl.to("#ubL", {autoAlpha: 0, scale: 0.5, duration: 0.2}, @posyl);
  tl.fromTo("#ubK", {autoAlpha: 0, scale: 0.5}, {autoAlpha: 1, scale: 1, duration: 0.45, ease: POP}, @posyl+0.10);
  tl.to("#ub", {scale: 0.78, duration: 0.6, ease: SP}, @posyl);
  // «на сайт»
  G.ripple("#ubR", @sait2);
  tl.fromTo("#ubR", {scale: 0.78}, {scale: 1.3, duration: 0.8, ease: "power2.out", immediateRender: false}, @sait2);
  G.bump("#ub", @sait2+0.04);
  // «і фінально» — the iris opens out of the link
  tl.to("#g11", {autoAlpha: 0, duration: 0.02}, @i_fin+0.40);''')
    nodejs = "\n".join(
        '  tl.fromTo("#%s", {autoAlpha: 0, scale: 0.4}, {autoAlpha: 1, scale: 1, duration: 0.5, ease: POP}, %.3f);'
        % (n, T["pered"] + 0.12 + i * 0.26) for i, (n, _, _, _) in enumerate(NODES))
    return html, src.replace("NODEJS", nodejs.strip())


# =================================================================== b13
@beat
def b13_it_lands():
    """«і фінально вони зберігаються вже в чат-боті. Тобто якщо людина
    перейшла по секретному посиланню, яке ми їй дали, ці дані лишаються
    прямо в її картці в чат-боті»

    TK3. The iris opens out of the link chip onto the funnel. The link lands
    under the Reels tile as a bubble; the card's two UTM rows ring on
    «зберігаються», the bot on «чат-боті». On «перейшла» the link is tapped
    and the pink `utm` chip leaves it: up into the reel's tile, up into the
    site, out through the button on «посиланню» into SendPulse, down on
    «лишаються» into the card — and the «?» in UTM_SOURCE turns into
    instagram, UTM_MEDIUM into reels, on «прямо в її картці». On «картці» the
    camera pushes in on the card and it lights once."""
    lines = [js('''
  tl.set("#gU", {autoAlpha: 1}, @i_fin+0.06);
  tl.set(".tick", {autoAlpha: 0}, @i_fin+0.06);
  G.irisOpen("#tkU", @i_fin+0.06, 540, 212, 0.8);
  drift1("#tkU", @i_fin+0.06, 10.0);
  // «фінально» — the link lands under the reel
  arr("#uLink", @finalno-0.06, {s: 0.5, y: -30});
  // «зберігаються» — where they end up; «в чат-боті» — who keeps them
  tl.fromTo(["#uRowR", "#uRowR2"], {autoAlpha: 0}, {autoAlpha: 1, duration: 0.3, stagger: 0.1}, @zberih2);
  tl.to(["#uRowR", "#uRowR2"], {autoAlpha: 0, duration: 0.4}, @zberih2+0.9);
  G.bump("#uBotW", @chatboti2);
  shn("#uSP .sheen", @chatboti2+0.06);
  // «перейшла» — the link is tapped; the chip leaves it
  tl.fromTo("#uLtap", {autoAlpha: 0.95, scale: 0.3}, {autoAlpha: 0, scale: 1.6, duration: 0.6, ease: "power2.out", immediateRender: false}, @pereishla);
  G.bump("#uLink", @pereishla);
  tl.set("#uChip", {x: %(lx)d, y: %(ly)d, scale: 0.5}, @pereishla+0.04);
  tl.to("#uChip", {autoAlpha: 1, scale: 1, duration: 0.3, ease: POP}, @pereishla+0.04);''' % {
        "lx": CHIP["link"][0], "ly": CHIP["link"][1]}),
        chip_to("src", T["pereishla"] + 0.18, 0.30),
        js('''  G.ripple("#uSrcR", @pereishla+0.44);'''),
        chip_to("ph", T["sekret"] - 0.02, 0.42),
        js('''  G.bump("#uPhA", @sekret+0.38);'''),
        chip_to("btn", T["posylannyu"] - 0.04, 0.26),
        chip_to("bot", T["posylannyu"] + 0.24, 0.30),
        # SendPulse takes it in (the bot keeps it) and hands it on at its
        # bottom edge — never dragged across the chat
        js('''  tl.to("#uChip", {autoAlpha: 0, scale: 0.4, duration: 0.2, ease: "power2.in"}, @posylannyu+0.50);
  G.bump("#uBotW", @posylannyu+0.56);
  tl.set("#uChip", {x: %d, y: %d}, @posylannyu+0.72);
  tl.to("#uChip", {autoAlpha: 1, scale: 1, duration: 0.3, ease: POP}, @lyshayut-0.24);'''
           % CHIP["botB"]),
        chip_to("card", T["lyshayut"] + 0.06, 0.30),
        chip_to("row", T["lyshayut"] + 0.36, 0.34),
        js('''  tl.to("#uChip", {autoAlpha: 0, scale: 0.4, duration: 0.2, ease: "power2.in"}, @lyshayut+0.66);
  // «прямо в її картці» — the «?»s turn into her source
  tl.to("#uQ1", {autoAlpha: 0, scale: 0.6, duration: 0.18, ease: "power2.in"}, @pryamo-0.10);
  tl.fromTo("#uV1", {autoAlpha: 0, x: 24}, {autoAlpha: 1, x: 0, duration: 0.5, ease: SP}, @pryamo+0.04);
  tl.to("#uQ2", {autoAlpha: 0, scale: 0.6, duration: 0.18, ease: "power2.in"}, @pryamo+0.16);
  tl.fromTo("#uV2", {autoAlpha: 0, x: 24}, {autoAlpha: 1, x: 0, duration: 0.5, ease: SP}, @pryamo+0.30);
  // «картці» — push in on the card; it lights once
  tl.to("#uCam", {x: %(px)d, y: %(py)d, scale: %(k).2f, duration: 0.85, ease: "power2.inOut"}, @kartsi-0.12);
  bout("#uLink", @kartsi-0.12, 8, 0.3);
  tl.fromTo("#uCardW", {filter: "drop-shadow(0 0 0px rgba(255,110,156,0))"},
            {filter: "drop-shadow(0 0 46px rgba(255,110,156,0.85))", duration: 0.4, ease: "power2.out", immediateRender: false}, @kartsi+0.30);
  tl.to("#uCardW", {filter: "drop-shadow(0 0 0px rgba(255,110,156,0))", duration: 0.7, ease: "power2.in"}, @kartsi+0.80);
  tl.set("#uCardW", {filter: "none"}, @kartsi+1.52);
  shn("#uCard .sheen", @kartsi+0.36);
  // «і далі» — the iris closes into the card
  G.irisClose("#tkU", @idali, 540, 660, 0.5);
  tl.to("#gU", {autoAlpha: 0, duration: 0.02}, @idali+0.52);''' % {
            "px": PUSH[0], "py": PUSH[1], "k": PUSH_K}),
    ]
    return "", "\n".join(x.rstrip() for x in lines)


# =================================================================== b15
COLS = [("R", 190, sk(REELS), 12), ("M", 540, g.mark("meta"), 5), ("S", 890, sk(STORY), 7)]
MC_PITCH = 70
k.css("""
/* ---- b15 · behind her: every client, sorted by where they came from ---- */
#g15tint { position: absolute; inset: 0;
  background: linear-gradient(180deg, rgba(62,8,24,0.26) 0%, rgba(40,5,15,0.40) 100%); }
.mc { position: absolute; left: 0; top: 0; width: 250px; height: 62px; margin: -31px 0 0 -125px; border-radius: 20px;
  background: linear-gradient(160deg, #ffffff 0%, #fff5f8 60%, #f7e4ea 100%);
  box-shadow: inset 0 2px 1px #fff, 0 16px 30px -12px rgba(24,4,12,0.55);
  display: flex; align-items: center; gap: 14px; padding: 0 16px; }
.mc i { width: 36px; height: 36px; border-radius: 50%; flex: none; display: block;
  background: linear-gradient(160deg, #f6d7e0 0%, #d9a3b3 100%); }
.mc u { flex: 1; height: 14px; border-radius: 7px; background: rgba(23,20,28,0.16); display: block; }
.mc svg { width: 32px; height: 32px; flex: none; }
.mc .sk { stroke: #b4122f; } .mc .sk .fl { fill: #b4122f; } .mc .sk .ring { stroke: #e0204b; }
.mc .mkc { fill: #b4122f; }
.ch { width: 118px; height: 118px; margin: -59px 0 0 -59px; }
.cnt { position: absolute; min-width: 74px; height: 54px; padding: 0 16px; border-radius: 27px;
  margin: -27px 0 0 0; background: #fff; z-index: 2; color: #b4122f; font-size: 32px; font-weight: 900; text-align: center;
  line-height: 54px; box-shadow: 0 14px 26px -10px rgba(24,4,12,0.6); }
#m15 { left: 60px; top: 70px; height: 70px; padding: 0 30px 0 22px; border-radius: 35px; color: #fff;
  display: flex; align-items: center; gap: 12px; font-size: 30px; font-weight: 700;
  background: linear-gradient(160deg, #ff8ab0 0%, #e0204b 55%, #8d0d24 100%);
  box-shadow: inset 0 2px 1px rgba(255,255,255,0.5), 0 20px 36px -14px rgba(70,4,20,0.7); }
#m15 svg { width: 34px; height: 34px; fill: none; stroke: #fff; stroke-width: 3; stroke-linecap: round; stroke-linejoin: round; }
#c15r { left: 131px; top: 141px; width: 118px; height: 118px; }
""")


def seg_cards():
    """24 clients: where they land in the heap, and their seat in a column."""
    out = []
    seq = []
    for key, cx, glyph, n in COLS:
        for i in range(n):
            seq.append((key, cx, glyph, i))
    # interleave so the heap is mixed, deterministic
    order = sorted(range(len(seq)), key=lambda j: (j * 7) % len(seq))
    for idx, j in enumerate(order):
        key, cx, glyph, i = seq[j]
        hx = 150 + (idx * 263) % 780
        hy = 250 + (idx * 157) % 760
        rot = ((idx * 37) % 25) - 12
        out.append({"id": "mc%d" % idx, "key": key, "glyph": glyph, "hx": hx, "hy": hy, "rot": rot,
                    "sx": cx, "sy": 300 + i * MC_PITCH})
    return out


SEG = seg_cards()


@beat
def b15_segments():
    """«і далі по цьому вже можна сегментувати людей: тобто, розділяти, звідки
    вони прийшли, і під це редагувати маркетинг.»

    Out of the closed iris, the room goes soft behind her and 24 client cards
    pour into it — each carrying its source mark. On «розділяти» three column
    heads land, Reels, Meta, Stories, and every card flies to its column; on
    «прийшли» the counts run up, 12 · 5 · 7. On «редагувати» the Reels column
    rings and a chip lands over it: «більше рілсів». Matte `segs` keeps her
    in front of all of it."""
    cards = "".join('<div class="mc hide" id="%s"><i></i><u></u>%s</div>'
                    % (c["id"], c["glyph"].replace('class="mk"', 'class="mkc"')) for c in SEG)
    heads = "".join('<div class="tw ch hide" id="h15%s" style="left:%dpx;top:200px"><div class="jelly">%s</div></div>'
                    '<div class="cnt hide" id="n15%s" style="left:%dpx;top:200px">0</div>'
                    % (key, cx, glyph, key, cx + 66) for key, cx, glyph, _ in COLS)
    html = fill(u'''
      <div class="g full" id="g15">
        <div id="g15soft" class="hide">{{soft}}<div id="g15tint"></div></div>
        {{cards}}
        {{heads}}
        <div class="sqring hide" id="c15r"></div>
        <div class="cx hide" id="m15">{{up}}більше рілсів</div>
      </div>''', soft=soft("segs"), cards=cards, heads=heads, up=sk(UP, ""))
    cfg = [{"id": c["id"], "hx": c["hx"], "hy": c["hy"], "r": c["rot"], "sx": c["sx"], "sy": c["sy"]} for c in SEG]
    src = js('''
  var C15 = CFG15;
  tl.set("#g15", {autoAlpha: 1}, @idali+0.56);
  tl.fromTo("#g15soft", {autoAlpha: 0}, {autoAlpha: 1, duration: 0.5, ease: "power1.inOut"}, @idali+0.56);
  // «можна сегментувати людей» — clients pour into the room
  C15.forEach(function (c, i) {
    var t = @idali+0.62 + i * 0.055;
    tl.fromTo("#" + c.id, {autoAlpha: 0, x: c.hx, y: c.hy - 520, rotation: c.r * 2, scale: 0.8},
              {autoAlpha: 1, y: c.hy, rotation: c.r, scale: 1, duration: 0.7, ease: SP}, t);
    tl.set("#" + c.id, {x: c.hx}, t);
  });
  // «розділяти» — three columns; every card to its own
  HEADJS
  C15.forEach(function (c, i) {
    tl.to("#" + c.id, {x: c.sx, y: c.sy, rotation: 0, duration: 0.62, ease: SP}, @rozdil+0.10 + i * 0.022);
  });
  // «звідки вони прийшли» — the counts
  G.count("#n15R", @pryishly, 12, 0.9); G.count("#n15M", @pryishly+0.08, 5, 0.9); G.count("#n15S", @pryishly+0.16, 7, 0.9);
  // «редагувати маркетинг» — more of what works
  G.ripple("#c15r", @redah);
  G.bump("#h15R", @redah);
  tl.fromTo("#m15", {autoAlpha: 0, scale: 0.5, y: 20}, {autoAlpha: 1, scale: 1, y: 0, duration: 0.55, ease: POP}, @redah+0.10);
  G.bump("#m15", @market+0.04);
  // clears before the matte ends
  bout(["#m15", ".ch", ".cnt", ".mc"], @market+0.36, 10, 0.26);
  tl.to("#g15soft", {autoAlpha: 0, duration: 0.3, ease: "power1.in"}, @market+0.34);
  tl.to("#g15", {autoAlpha: 0, duration: 0.02}, @market+0.66);'''.replace("CFG15", json.dumps(cfg)))
    headjs = "\n  ".join(
        'arr("#h15%s", %.3f, {s: 0.5, y: -30}); tl.fromTo("#h15%s .sk, #h15%s .mk", {scale: 0.55, autoAlpha: 0}, '
        '{scale: 1, autoAlpha: 1, duration: 0.5, ease: SP}, %.3f); '
        'tl.fromTo("#n15%s", {autoAlpha: 0, scale: 0.5}, {autoAlpha: 1, scale: 1, duration: 0.45, ease: POP}, %.3f);'
        % (key, T["rozdil"] - 0.12 + i * 0.1, key, key, T["rozdil"] - 0.02 + i * 0.1, key,
           T["rozdil"] + 0.30 + i * 0.1) for i, (key, _, _, _) in enumerate(COLS))
    return html, src.replace("HEADJS", headjs)


# =================================================================== b17
k.css("""
/* ---- b17 · near: her profile, and the Follow button (reel 13) ---- */
#p17 { left: 110px; top: 190px; width: 860px; height: 150px; border-radius: 75px; overflow: hidden; }
#p17av { left: 23px; top: 23px; width: 104px; height: 104px; }
#p17n { left: 150px; top: 30px; font-size: 44px; font-weight: 700; letter-spacing: -0.015em; }
#p17s { left: 150px; top: 88px; font-size: 28px; font-weight: 500; color: rgba(255,255,255,0.72); }
.flw { position: absolute; }
.fla, .flb { position: absolute; inset: 0; border-radius: 999px; display: flex; align-items: center;
  justify-content: center; gap: 10px; font-size: 32px; font-weight: 700; letter-spacing: -0.01em; }
.fla { color: #fff; background: linear-gradient(165deg, #e0204b 0%, #ab112e 46%, #6b081c 100%);
  box-shadow: inset 0 2px 1px rgba(255,255,255,0.5), inset 0 -16px 26px -12px rgba(255,125,165,0.6),
              0 22px 40px -16px rgba(70,4,20,0.7); }
.flb { color: #17141c; font-size: 29px; background: linear-gradient(160deg, #ffffff 0%, #fff5f8 52%, #f5dfe6 100%);
  box-shadow: inset 0 2px 1px #fff, 0 22px 40px -16px rgba(30,4,12,0.6); }
.flb svg { width: 30px; height: 30px; fill: none; stroke: #b4122f; stroke-width: 3; stroke-linecap: round; stroke-linejoin: round; }
""")


@beat
def b17_follow():
    """«Якщо ти вперше чуєш про UTM мітки, то тобі обов'язково треба
    підписатись»

    Her profile row lands above her head — avatar, «Рута», «технічна
    продюсерка»; the Follow button lands on «то тобі», rings on
    «обов'язково» and is pressed on «підписатись»: Стежити -> Відстежується.
    The reel ends on it."""
    html = fill(u'''
      <div class="g full" id="g17">
        <div id="p17" class="dglass edge abs hide">
          <div class="cx avc me" id="p17av"></div>
          <div class="cx" id="p17n">Рута</div>
          <div class="cx" id="p17s">технічна продюсерка</div>
          <div class="flw hide" id="flw" style="left:540px;top:35px;width:290px;height:80px">
            <div class="fla" id="flwA">Стежити</div>
            <div class="flb hide" id="flwB"><svg viewBox="0 0 24 24"><path d="{{ck}}"/></svg>Відстежується</div>
          </div>
          <div class="sheen"></div>
        </div>
      </div>''', ck=CHECK_D)
    src = js('''
  tl.set("#g17", {autoAlpha: 1}, @vpershe-0.06);
  arr("#p17", @vpershe-0.06, {s: 0.6, y: 30});
  tl.fromTo(["#p17av", "#p17n", "#p17s"], {autoAlpha: 0, x: -14}, {autoAlpha: 1, x: 0, duration: 0.5, ease: SP, stagger: 0.06}, @vpershe+0.16);
  shn("#p17 .sheen", @proutm);
  arr("#flw", @totobi, {s: 0.6, x: 30, y: 0});
  G.bump("#flw", @obov);
  tl.to("#flw", {scale: 0.9, duration: 0.08, ease: "power2.out"}, @pidp);
  tl.to("#flw", {scale: 1, duration: 0.4, ease: POP}, @pidp+0.08);
  tl.set("#flwB", {autoAlpha: 1}, @pidp+0.08);
  tl.set("#flwA", {autoAlpha: 0}, @pidp+0.08);
  G.inner("#flwB svg", @pidp+0.02);''')
    return html, src


# ---------------------------------------------------------------------------
# Captions drop only on redundancy (STYLE.md §2b.1).
BLACKOUT = [
    (13.70, 14.85, "b03 — the shelf says ×2 on «вдвічі більше»"),
    (15.70, 16.30, "b03 — the card says «Вебінар» on «вебінару»"),
]
INVERT = []
# a two-word blackout mid-sentence: the caption goes, the plaque stays
KEEP_PLAQUE = [(13.70, 14.85), (15.70, 16.30)]

EXTRA_DEFS = (
    '<linearGradient id="gStory" x1="0" y1="0" x2="1" y2="1">'
    '<stop offset="0" stop-color="#ffd0de"/><stop offset="0.5" stop-color="#ff6e9c"/>'
    '<stop offset="1" stop-color="#e0204b"/></linearGradient>')

HEAD_JS = r"""
  var G = helpers(tl);
  function bin(sel, t, b, d) { d = d || 0.38; G.blurIn(sel, t, b || 12, d); tl.set(sel, {filter: "none"}, t + d + 0.01); }
  function bout(sel, t, b, d) { d = d || 0.32; G.blurOut(sel, t, b || 10, d); tl.set(sel, {filter: "none"}, t + d + 0.01); }
  function arr(sel, t, o) {
    o = o || {};
    bin(sel, t, o.blur || 12, 0.36);
    tl.fromTo(sel, {scale: o.s == null ? 0.5 : o.s, x: o.x || 0, y: o.y == null ? 34 : o.y},
              {scale: 1, x: 0, y: 0, duration: o.d || 0.85, ease: o.ease || POP}, t);
  }
  function shn(sel, t) {
    tl.fromTo(sel, {xPercent: -120}, {xPercent: 120, duration: 0.8, ease: "power2.inOut", immediateRender: false}, t);
  }
  function drift1(sel, t, d) { tl.fromTo(sel + " .aurs", {x: 0, y: 0}, {x: -110, y: 70, duration: d, ease: "sine.inOut"}, t); }
  gsap.set(".sheen", {xPercent: -120});
"""


def main():
    gh, gj = [], []
    for fn in BEATS:
        h, j = fn()
        if h.strip():
            gh.append(h.rstrip())
        gj.append("  /* %s */" % fn.__name__)
        gj.append(j.rstrip())

    # the slow push on the plate (§0.8): her, her mattes and the soft rooms
    # move as one, so the cut-outs stay on their own pixels
    push = ["#vid", ".matte", ".soft"]
    head = [g.js(), HEAD_JS,
            '  gsap.set(%s, {transformOrigin: "540px 820px"});' % json.dumps(push),
            '  tl.fromTo(%s, {scale: 1}, {scale: 1.045, duration: %.3f, ease: "none"}, 0);'
            % (json.dumps(push), DUR)]
    doc = k.document(
        title=u"Reel 16 — звідки приходять клієнти (UTM)",
        plate="assets/base.mp4",
        gfx_html=g.defs(EXTRA_DEFS) + "\n" + "\n".join(gh),
        gfx_js="\n".join(head + gj),
        caps=CAPS,
        blackout=BLACKOUT,
        invert=INVERT,
    )
    for a, b in KEEP_PLAQUE:
        for line in ('  tl.to("#scrim", {autoAlpha: 0, duration: 0.20}, %.3f);\n' % (a - 0.20),
                     '  tl.to("#scrim", {autoAlpha: 1, duration: 0.25}, %.3f);\n' % b):
            assert line in doc, line
            doc = doc.replace(line, "", 1)

    out = os.path.join(HERE, "index.html")
    io.open(out, "w", encoding="utf-8").write(doc)
    print("index.html  %d captions, %d beats, %d segment cards, %.1f KB"
          % (len(CAPS), len(BEATS), len(SEG), os.path.getsize(out) / 1024.0))


main()
