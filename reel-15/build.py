# -*- coding: utf-8 -*-
"""Reel 15 — «СРМ для агенцій». What CRM an agency needs, and hers.

Variant B, refined glass (STYLE.md §0, tools/glass.py). Structure follows
reel-12/build.py: kit document, her plate, mattes per beat, captions on the
plaque, one `.g full` container per beat.

The one object is **one client's CRM card**. Bare early (three conversations
behind her head that she forgets on «1, 2, 3»), written out on the burgundy
ground field by field, re-skinned as a Notion table that builds itself, and
paid off as **Floor** — the CRM she vibe-coded — recreated screen by screen
inside a glass phone, amounts blurred, the Quote tab readable.

The chain, near -> behind -> over, three times:
    a filter chip «для агенцій · CRM» that tries to scroll away and comes
    back -> her name tag, two role chips -> a routine checklist Claude ticks
    -> three contacts behind her head, forgotten on «1, 2, 3» -> the middle
    one opens (iris) into a CRM card, five fields filled on their words ->
    the card folds into a shelf of three cheap tools, Notion wins -> (her
    closeup) -> the Notion tile opens into a table that fills itself, Claude
    flips to ChatGPT, «майже agentic system» -> its row count runs away and
    the iris closes on it -> (her pull-out) -> the count lands in a capsule,
    €0 -> a chat inbox: client, bot, manager -> SendPulse -> the room behind
    her tints and integrations ripple out of SendPulse -> Notion and SendPulse
    on a shelf, both flicked off -> the empty shelf opens into Floor:
    Pipeline, P&L, Money blurred, Quote sliders to €400 / 8 h = €50/h ->
    the iris closes into Claude, the command centre -> a task goes in, a
    notification comes out -> comment composer, «+».

Her cut: six shots — 0-13.70, 13.70-18.10, 18.10-49.07, 49.07-50.33 (a
closeup on «афігєнно»: hers), 50.33-61.27, 61.27-109.76 — plus a pull-out
at 60.25-61.25 on «дууууже» (tools/pullouts.py). Both are NO_PAINT.

usage: python build.py
"""
import io
import json
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))
from kit import Kit  # noqa: E402
from glass import Glass, available  # noqa: E402

DUR = 109.683          # 3291 plate frames / 30 (work/w40-queue.log)
FPS = 30
k = Kit(width=1080, height=1920, fps=FPS, duration=DUR)
g = Glass()
k.css(g.css())

BEATS = []


def beat(fn):
    BEATS.append(fn)
    return fn


# ---------------------------------------------------------------------------
# NO-PAINT ZONES — her own editing (STYLE.md §4a).
#   49.07 – 50.33   a 1.27 s closeup on «афігєнно» (tools/shots.py, shot 3)
#   60.25 – 61.25   she pulls the frame back on «дууууже» (tools/pullouts.py)
# Shot 1 (13.70-18.10, 4.4 s) is an ordinary jump cut on «коротше» at the
# same framing, not an insert, so it keeps its beat.
NO_PAINT = [(49.07, 50.33), (60.25, 61.25)]

# ---------------------------------------------------------------------------
# Words. Script spelling on her timing (work/r15/captions.json, settled with
# work/r15/caption-patch.json). Ends re-derived from the next start, the rule
# align.py uses, because the patch dropped two tokens.
CAPS = k.load_captions(os.path.join(ROOT, "work", "r15", "captions.json"))
for _a, _b in zip(CAPS, CAPS[1:]):
    _a["e"] = round(max(_a["s"] + 0.10, _b["s"] - 0.085), 3)


def _n(s):
    return "".join(ch for ch in s.lower() if ch.isalnum() or ch == "+")


def at(word, near):
    """The caption carrying `word` whose start is nearest `near` seconds —
    readable in the source, and it fails loudly if the words ever move."""
    hits = [c for c in CAPS if _n(word) in [_n(x) for x in c["w"].split()]]
    c = min(hits, key=lambda c: abs(c["s"] - near))
    assert abs(c["s"] - near) < 1.0, (word, near, c["s"])
    return c


def S(w, near):
    return at(w, near)["s"]


def E(w, near):
    return at(w, near)["e"]


T = {
    # b01-b03
    "nish": S(u"нішевий", 1), "ag1": S(u"агенції", 3), "crm1": S("CRM", 4.4),
    "hort": S(u"гортати", 5.7), "dali": S(u"далі", 6.4), "ayak": S(u"якщо", 6.9),
    "korotko": S(u"коротко", 7.7), "poznay": S(u"познайомимось", 8.1),
    "pryvit": S(u"привіт", 8.9), "ruta": S(u"Рута", 9.3), "vlasn2": S(u"власниця", 9.9),
    "fract": S("fractional", 11.7), "partner": S("partner", 13.0),
    "korotshe": S(u"коротше", 13.8), "dopom": S(u"допомагаю", 14.3),
    "biz": S(u"бізнесам", 14.7), "shi": S(u"ШІ", 15.8), "avtomat": S(u"автоматизовувати", 16.3),
    "yikh": S(u"їх", 17.3), "robotu": S(u"роботу", 17.7),
    # b05
    "crm2": S("CRM", 22.0), "stoyalo": S(u"стояло", 22.6), "duzhe1": S(u"дуже", 23.1),
    "hostro": S(u"гостро", 23.6), "one": S("1", 24.5), "two": S("2", 24.8),
    "three": S("3", 25.0), "zabula": S(u"забула", 25.6), "zkym": S(u"ким", 26.2),
    "spilk1": S(u"спілкувались", 26.7),
    # b06
    "ale1": S(u"Але", 27.3), "shchos": S(u"щось", 29.9), "proste": S(u"просте", 31.2),
    "detali": S(u"деталі", 33.0), "lyudynu": S(u"людину", 33.5),
    "proshcho": S(u"про", 34.1), "spilk2": S(u"спілкувались", 34.6),
    "zvidky": S(u"звідки", 36.2), "skilky1": S(u"скільки", 37.6),
    "groshey": S(u"грошей", 38.5), "komanda": S(u"команда", 39.7),
    "totodi": S(u"тоді", 40.9), "skilky2": S(u"скільки", 41.8),
    "kozhnomu": S(u"кожному", 43.0), "tomu1": S(u"Тому", 43.9),
    # b11
    "pochyn": S(u"починаємо", 44.7), "deshev": S(u"дешеве", 46.0),
    "serdyte": S(u"сердите", 46.6), "obyekt": S(u"об'єктивно", 47.7),
    "notion1": S("Notion", 48.3), "pidiyde": S(u"підійде", 48.6),
    # b12
    "i_af": S(u"І", 50.4), "navit": S(u"навіть", 50.7), "nichoho": S(u"нічого", 51.4),
    "robyty": S(u"робити", 52.0), "claude1": S("Claude", 52.7),
    "chatgpt": S("ChatGPT", 53.3), "pobuduye": S(u"побудує", 54.3),
    "maizhe": S(u"майже", 56.6), "agentic1": S("agentic", 57.1),
    "system": S("system", 57.8), "setap": S(u"сетап", 59.0), "mozhe": S(u"може", 59.3),
    # b14
    "bahato": S(u"багато", 61.3), "navant": S(u"навантаження", 61.9),
    "bezkosht": S(u"безкоштовному", 63.0), "taryfi": S(u"тарифі", 63.5),
    "ale2": S(u"Але", 64.1),
    # b15-b16
    "treba6": S(u"треба", 65.9), "menedzh": S(u"менеджери", 66.2),
    "spilkuv": S(u"спілкуватись", 67.0), "chatboty": S(u"чатботи", 68.4),
    "bachyty": S(u"бачити", 68.9), "perepysky": S(u"переписки", 69.4),
    "kandydat": S(u"кандидат", 70.9), "sp1": S("Sendpulse", 72.1),
    "de": S(u"де", 73.0), "integr": S(u"інтегрується", 74.4),
    "zchat": S(u"чатботами", 75.0), "milyon": S(u"мільйоном", 75.8),
    "typu": S(u"типу", 77.5), "imeyliv": S(u"імейлів", 77.9),
    # b17
    "ale3": S(u"Але", 79.0), "mayu": S(u"маю", 79.6), "chesno": S(u"чесно", 80.1),
    "notion2": S("Notion", 81.2), "sp2": S("Sendpulse", 82.0),
    # b18
    "navaib": S(u"навайбкодила", 83.1), "prostenku": S(u"простеньку", 84.4),
    "agentic2": S("agentic", 85.0), "crm5": S("CRM", 85.6),
    "rozshyr": S(u"розширеним", 86.3), "dashbord": S(u"дашбордом", 87.6),
    "kilka": S(u"кілька", 88.7), "uspishno": S(u"успішно", 89.6),
    "koryst": S(u"користуюсь", 90.1), "vse1": S(u"Все", 91.3),
    "prodazh": S(u"продажами", 92.6), "perepys": S(u"переписками", 93.2),
    # b19-b20
    "vykor": S(u"використовую", 94.7), "claude2": S("Claude", 95.2),
    "komand": S(u"командний", 95.7), "tsentr": S(u"центр", 96.2),
    "crm6": S("CRM", 98.5), "chatbot2": S(u"чатбот", 99.4), "vzahali": S(u"взагалі", 99.7),
    "dayu": S(u"даю", 100.8), "zadachi": S(u"задачі", 101.1), "vin": S(u"він", 101.8),
    "zvituye": S(u"звітує", 102.2), "tomu2": S(u"Тому", 103.4),
    # b21
    "yakshcho2": S(u"Якщо", 103.6), "pytannya": S(u"питання", 104.5),
    "pidibr": S(u"підібрати", 105.2), "potreby": S(u"потреби", 106.7),
    "pyshy": S(u"пиши", 107.3), "plus": S("+", 107.8), "i_last": S(u"і", 108.1),
    "pospilk": S(u"поспілкуємось", 108.6),
    "dur": DUR,
}
T["partner_e"] = E("partner", 13.0)
T["robotu_e"] = E(u"роботу", 17.7)


def js(src, **extra):
    """`@name` -> a literal time. Literals, not variables, because
    tools/review.py reads the timeline off the generated numbers."""
    vals = dict(T)
    vals.update(extra)

    def rep(m):
        v = vals[m.group(1)]
        return "%.3f" % v if isinstance(v, (int, float)) else str(v)
    return re.sub(r"@(\w+)", rep, src)


def fill(s, **kw):
    for key, v in kw.items():
        s = s.replace("{{%s}}" % key, v if isinstance(v, str) else str(v))
    assert "{{" not in s, s[s.index("{{"):s.index("{{") + 40]
    return s


# ---------------------------------------------------------------------------
# Mattes (tools/matte.py via work/r15/mattes.sh). (first frame, frames used).
# `contacts` stops one frame before the iris opens at «Але» (27.26): a matte
# on top of the burgundy ground would paste her back over the takeover.
MATTES = {"contacts": (655, 163), "orbit": (2187, 184)}
for _name, (_f0, _n) in sorted(MATTES.items()):
    k.matte(_name, _f0 / 30.0, _n / 30.0)

# ---------------------------------------------------------------------------
# Glyphs. Strokes and fills, never emoji (§5a.11). SendPulse is not in
# simple-icons: its mark is the pulse line from sendpulse.com's own pinned-tab
# icon (mask-icon.svg, 16 px box), scaled to the 24 px symbol box.
SP_PATH = ("M13.683 15L13.625 14.561L12.896 9.521L9.487 22.5H6.868L6.777 22.11L5.026 15H1.5V12"
           "H7.291L7.345 12.281L8.248 16.281L12.06 1.5H14.777L14.831 1.945L16.092 12.028H18.276"
           "C18.749 11.314 19.558 10.843 20.476 10.843C21.935 10.843 23.118 12.033 23.118 13.5"
           "C23.118 14.967 21.935 16.157 20.476 16.157C19.57 16.157 18.771 15.698 18.295 15H13.683Z")
BOT_PATH = ("M12 1.6a1.7 1.7 0 0 1 .85 3.17V6.4h4.35a3.4 3.4 0 0 1 3.4 3.4v7.2a3.4 3.4 0 0 1-3.4 3.4"
            "H6.8a3.4 3.4 0 0 1-3.4-3.4V9.8a3.4 3.4 0 0 1 3.4-3.4h4.35V4.77A1.7 1.7 0 0 1 12 1.6z"
            "M8.9 11.3a1.75 1.75 0 1 0 0 3.5 1.75 1.75 0 0 0 0-3.5zm6.2 0a1.75 1.75 0 1 0 0 3.5"
            " 1.75 1.75 0 0 0 0-3.5zM.8 11.4h1.6v4.6H.8zm20.8 0h1.6v4.6h-1.6z")
FUNNEL_PATH = ("M3.2 4.2h17.6a.9.9 0 0 1 .7 1.5l-6.7 7.6v5.6a.9.9 0 0 1-.5.8l-3.4 1.8"
               "a.9.9 0 0 1-1.3-.8v-7.4L2.5 5.7a.9.9 0 0 1 .7-1.5z")
SPARK_PATH = "M12 2.5l2.1 6.4 6.4 2.1-6.4 2.1L12 19.5l-2.1-6.4-6.4-2.1 6.4-2.1z"
HEART = ("M12 20.6s-7.6-4.5-9.4-9.3C1.3 7.8 3.5 4.4 7 4.4c2 0 3.7 1.1 5 3 "
         "1.3-1.9 3-3 5-3 3.5 0 5.7 3.4 4.4 6.9-1.8 4.8-9.4 9.3-9.4 9.3z")
PERSON = ('<svg viewBox="0 0 24 24"><circle cx="12" cy="9" r="4.3"/>'
          '<path d="M4.2 21c1.1-4.4 4.3-6.6 7.8-6.6s6.7 2.2 7.8 6.6z"/></svg>')
CHECK_D = "M6.2 12.6l3.9 3.9 7.7-8.6"
CURSOR = ('<svg viewBox="0 0 24 24"><path d="M5.5 2.8v16.9l4.3-4.1 2.8 6.3 3-1.3-2.8-6.2h6z" '
          'fill="#fff" stroke="#17141c" stroke-width="1.3" stroke-linejoin="round"/></svg>')


def sym(name, cls="mk"):
    """A local symbol (defined in EXTRA_DEFS) in the same shape as g.mark()."""
    return ('<svg class="%s"><use href="#i-%s" width="100%%" height="100%%"/></svg>'
            % (cls, name))


def floor_wm(size):
    return '<span class="wmark" style="font-size:%dpx">Floor</span>' % size


def check_svg(pid):
    return '<svg viewBox="0 0 24 24"><path id="%s" d="%s"/></svg>' % (pid, CHECK_D)


k.css("""
.abs, .cx { position: absolute; }
.hide { opacity: 0; visibility: hidden; }
.ctr { position: absolute; left: 0; width: 1080px; display: flex; justify-content: center; }
.ctr > .dglass, .ctr > .shelf, .ctr > .dchip { position: relative; }
/* Budget (STYLE.md §5a.1): `check` counts every backdrop-filter, blur,
   radial-gradient and clip-path, hidden ones included, and ~40 turns the
   render black. Small chips and the cards stacked behind a window get a
   denser tint instead of a backdrop blur — at their size nobody can tell. */
.dchip { position: absolute; color: #fff;
  background: linear-gradient(160deg, rgba(66,24,36,0.86) 0%, rgba(28,11,17,0.82) 100%);
  box-shadow: inset 0 1.5px 1px rgba(255,255,255,0.30), inset 0 -16px 30px -16px rgba(255,255,255,0.14),
              0 30px 60px -26px rgba(10,0,4,0.6); }
/* the takeover's three light pools as one element (was three .aur) */
.aurs { position: absolute; left: -700px; top: -700px; width: 2480px; height: 3320px; pointer-events: none;
  background:
    radial-gradient(circle 526px at 1560px 880px, rgba(255,110,156,0.50), rgba(255,110,156,0)),
    radial-gradient(circle 634px at 760px 2360px, rgba(222,32,74,0.55), rgba(222,32,74,0)),
    radial-gradient(circle 382px at 1480px 1910px, rgba(255,198,214,0.20), rgba(255,198,214,0)); }
/* a round check: ring, burgundy fill, white tick drawn on */
.rck { position: relative; flex: none; border-radius: 50%; box-shadow: inset 0 0 0 3.5px rgba(255,255,255,0.45); }
.rck .f { position: absolute; inset: 0; border-radius: 50%;
  background: linear-gradient(165deg, #ff7aa4 0%, #e0204b 50%, #8d0d24 100%); }
.rck svg { position: absolute; inset: 0; width: 100%; height: 100%; fill: none; stroke: #fff;
  stroke-width: 3.2; stroke-linecap: round; stroke-linejoin: round; }
""")

# =================================================================== b01
k.css("""
/* ---- b01 · a feed filter: «для агенцій · CRM» ---- */
#f1cap { left: 190px; top: 250px; width: 700px; height: 150px; border-radius: 75px; }
#f1ic { left: 23px; top: 23px; width: 104px; height: 104px; }
#f1chips { left: 152px; top: 39px; display: flex; gap: 16px; }
.fchip { position: relative; display: inline-flex; align-items: center; gap: 14px; height: 72px;
  padding: 0 30px 0 14px; border-radius: 36px; font-size: 34px; font-weight: 700; white-space: nowrap;
  color: rgba(255,255,255,0.55); background: rgba(255,255,255,0.08);
  box-shadow: inset 0 0 0 2px rgba(255,255,255,0.22); }
.fchip .on { position: absolute; inset: 0; border-radius: 36px; display: block;
  background: linear-gradient(160deg, #ff7aa4 0%, #e0204b 55%, #a8102c 100%);
  box-shadow: inset 0 2px 1px rgba(255,255,255,0.5), inset 0 -10px 18px -8px rgba(255,190,210,0.5); }
.fchip .rck { width: 46px; height: 46px; }
.fchip span { position: relative; }
#f1sw { left: 485px; top: 452px; width: 110px; height: 110px; border-radius: 55px; }
#f1sw svg { position: absolute; left: 27px; top: 25px; width: 56px; height: 56px; fill: none;
  stroke: #fff; stroke-width: 4; stroke-linecap: round; stroke-linejoin: round; }
""")


@beat
def b01_niche_filter():
    """«Зараз буде супер нішевий контент, тому якщо ти не власниця агенції і
    тобі не треба CRM, то в принципі можеш гортати далі»

    A feed filter above her head: a funnel and two ghost chips that light on
    their words — «для агенцій» on «агенції», «CRM» on «CRM» (blackout for
    that one word, the chip says it). On «гортати» a swipe-up hint nudges; on
    «далі» the whole filter starts to scroll away — and on «А якщо ти тут»
    it gives up and springs back, empty, to become her name tag."""
    chips = "".join(
        '<div class="fchip" id="fc%d"><i class="on"></i><div class="rck">%s</div><span>%s</span></div>'
        % (i, check_svg("fck%d" % i), t) for i, t in enumerate([u"для агенцій", "CRM"]))
    html = fill(u'''
      <div class="g full" id="g1">
        <div id="f1sw" class="dchip edge abs hide"><svg viewBox="0 0 56 56"><path d="M14 34 28 20l14 14"/></svg></div>
        <div id="f1cap" class="dglass edge abs">
          <div class="cx" id="f1ic"><div class="jelly">{{funnel}}</div></div>
          <div class="cx" id="f1chips">{{chips}}</div>
        </div>
      </div>''', funnel=sym("funnel"), chips=chips)
    src = js('''
  tl.set("#g1", {autoAlpha: 1}, 0.020);
  gsap.set("#g1 .fchip .on", {autoAlpha: 0});
  G.drawPrep("fck0"); G.drawPrep("fck1");
  G.arrive("#f1cap", 0.020, {s: 0.72, y: 30});
  tl.fromTo("#f1ic", {scale: 0.5, autoAlpha: 0}, {scale: 1, autoAlpha: 1, duration: 0.55, ease: SP}, 0.140);
  tl.fromTo("#g1 .fchip", {autoAlpha: 0, x: -14}, {autoAlpha: 1, x: 0, duration: 0.5, ease: SP, stagger: 0.08}, 0.260);
  // «супер нішевий» — the funnel squeezes
  tl.to("#f1ic", {scaleX: 0.76, scaleY: 1.12, duration: 0.14, ease: "power2.out"}, @nish);
  tl.to("#f1ic", {scaleX: 1, scaleY: 1, duration: 0.5, ease: SP}, @t_nish2);
  // «агенції» — the first filter applies
  tl.to("#fc0 .on", {autoAlpha: 1, duration: 0.22}, @t_c0);
  tl.to("#fc0", {color: "#ffffff", duration: 0.2}, @t_c0);
  G.draw("fck0", @t_c0k, 0.3);
  G.bump("#fc0", @t_c0);
  // «CRM»
  tl.to("#fc1 .on", {autoAlpha: 1, duration: 0.22}, @t_c1);
  tl.to("#fc1", {color: "#ffffff", duration: 0.2}, @t_c1);
  G.draw("fck1", @t_c1k, 0.3);
  G.bump("#fc1", @t_c1);
  // «гортати» — the swipe-up hint
  G.blurIn("#f1sw", @t_sw, 10, 0.3);
  tl.fromTo("#f1sw", {y: 40, scale: 0.6}, {y: 0, scale: 1, duration: 0.7, ease: POP}, @t_sw);
  tl.to("#f1sw svg", {y: -14, duration: 0.16, ease: "power2.out"}, @t_nudge);
  tl.to("#f1sw svg", {y: 0, duration: 0.34, ease: SP}, @t_nudge2);
  // «далі» — the filter starts to scroll away...
  tl.to(["#f1cap", "#f1sw"], {y: -130, duration: 0.42, ease: "power2.in"}, @dali);
  // «А якщо ти тут» — ...and gives up
  tl.to("#f1cap", {y: 0, duration: 0.85, ease: POP}, @ayak);
  G.blurOut("#f1sw", @ayak, 10, 0.3);
  // «коротко» — it empties, ready to be her name tag
  G.blurOut(["#f1chips", "#f1ic"], @korotko, 10, 0.3);
  tl.to("#g1", {autoAlpha: 0, duration: 0.02}, @t_off);''',
             t_nish2=T["nish"] + 0.16, t_c0=T["ag1"] - 0.06, t_c0k=T["ag1"],
             t_c1=T["crm1"] - 0.04, t_c1k=T["crm1"] + 0.02,
             t_sw=T["hort"] - 0.10, t_nudge=T["hort"] + 0.18, t_nudge2=T["hort"] + 0.34,
             t_off=T["poznay"] - 0.02)
    return html, src


# =================================================================== b02
k.css("""
/* ---- b02 · her name tag and two role chips ---- */
#n2cap { left: 190px; top: 250px; width: 700px; height: 150px; border-radius: 75px; overflow: hidden; }
#n2av { left: 206px; top: 23px; width: 104px; height: 104px; border-radius: 50%; overflow: hidden;
  box-shadow: 0 0 0 3px rgba(255,255,255,0.55), 0 10px 24px -8px rgba(10,0,4,0.5); }
#n2av img { width: 100%; height: 100%; object-fit: cover; display: block; }
#n2name { left: 338px; top: 34px; font-size: 66px; font-weight: 700; letter-spacing: -0.02em; line-height: 80px; }
.rchip { height: 88px; padding: 0 38px 0 30px; border-radius: 44px; display: inline-flex; align-items: center;
  gap: 18px; font-size: 38px; font-weight: 700; letter-spacing: -0.01em; white-space: nowrap; }
.rchip i { display: block; width: 18px; height: 18px; border-radius: 50%;
  background: linear-gradient(160deg, #ffb3c9, #e0204b); box-shadow: 0 0 14px rgba(255,110,156,0.9); }
#n2r1 { top: 434px; } #n2r2 { top: 540px; }
""")


@beat
def b02_name_tag():
    """«А якщо ти тут, то коротко познайомимось, привіт, я Рута і я власниця
    продюсерської агенції і fractional automation partner»

    The emptied filter is now her name tag: her photo on «познайомимось», a
    wave of the capsule on «привіт», «Рута» on her name. Two role chips drop
    out of it on their words. Every word from «я Рута» to «partner» is on
    screen as she says it — blackout 9.30-13.80."""
    html = fill(u'''
      <div class="g full" id="g2">
        <div id="n2cap" class="dglass edge abs">
          <div class="cx" id="n2av"><img src="assets/avatar.jpg" alt=""></div>
          <div class="cx" id="n2name">Рута</div>
        </div>
        <div class="ctr" id="n2r1"><div class="dchip edge rchip"><i></i>власниця продюсерської агенції</div></div>
        <div class="ctr" id="n2r2"><div class="dchip edge rchip"><i></i>fractional automation partner</div></div>
      </div>''')
    src = js('''
  tl.set("#g2", {autoAlpha: 1}, @t_in);
  gsap.set(["#n2av", "#n2name", "#n2r1", "#n2r2"], {autoAlpha: 0});
  // «познайомимось» — her photo lands in the capsule
  tl.fromTo("#n2av", {scale: 0.5, autoAlpha: 0}, {scale: 1, autoAlpha: 1, duration: 0.6, ease: POP}, @poznay);
  // «привіт»
  tl.to("#n2cap", {rotation: -2.2, duration: 0.14, ease: "power2.out"}, @pryvit);
  tl.to("#n2cap", {rotation: 0, duration: 0.6, ease: SP}, @t_wave);
  // «Рута»
  G.blurIn("#n2name", @t_name, 10, 0.32);
  tl.fromTo("#n2name", {x: -18}, {x: 0, duration: 0.6, ease: SP}, @t_name);
  G.sheen("#n2cap .sheen", @t_name);
  // «власниця продюсерської агенції»
  G.blurIn("#n2r1", @t_r1, 10, 0.3);
  tl.fromTo("#n2r1", {y: -80, scale: 0.8}, {y: 0, scale: 1, duration: 0.8, ease: POP}, @t_r1);
  // «fractional automation partner»
  G.blurIn("#n2r2", @t_r2, 10, 0.3);
  tl.fromTo("#n2r2", {y: -90, scale: 0.8}, {y: 0, scale: 1, duration: 0.8, ease: POP}, @t_r2);
  G.bump("#n2r2 .rchip", @partner);
  // «коротше» (her jump cut) — the tag and chips fold into one card
  tl.to(["#n2r1", "#n2r2"], {y: -150, scale: 0.7, autoAlpha: 0, duration: 0.3, ease: "power2.in", stagger: 0.04}, @t_fold);
  tl.to("#n2cap", {scaleY: 1.5, y: 40, autoAlpha: 0, duration: 0.3, ease: "power2.in"}, @t_fold2);
  tl.to("#g2", {autoAlpha: 0, duration: 0.02}, @t_off);''',
             t_in=T["poznay"] - 0.02, t_wave=T["pryvit"] + 0.14, t_name=T["ruta"] + 0.02,
             t_r1=T["vlasn2"] - 0.04, t_r2=T["fract"] - 0.06,
             t_fold=T["korotshe"] - 0.12, t_fold2=T["korotshe"] - 0.06,
             t_off=T["korotshe"] + 0.26)
    return html.replace('<div class="cx" id="n2name">', '<div class="sheen"></div><div class="cx" id="n2name">'), src


# =================================================================== b03
TASKS = [u"Звіти вручну", u"Нагадування клієнтам", u"Рахунки та акти", u"Копіпаст у таблиці"]
k.css("""
/* ---- b03 · the routine, and Claude ticking it off ---- */
#c3 { left: 120px; top: 170px; width: 840px; height: 560px; border-radius: 64px; }
#c3lab { left: 60px; top: 46px; font-size: 24px; font-weight: 700; letter-spacing: 0.16em; color: rgba(255,255,255,0.58); }
.c3row { position: absolute; left: 60px; height: 88px; display: flex; align-items: center; gap: 26px; }
.c3row .rck { width: 58px; height: 58px; border-radius: 18px; }
.c3row .rck .f { border-radius: 18px; }
.c3t { position: relative; font-size: 40px; font-weight: 500; color: #fff; white-space: nowrap; }
.c3s { position: absolute; left: -6px; right: -6px; top: 24px; height: 5px; border-radius: 3px;
  background: rgba(255,255,255,0.85); transform-origin: 0% 50%; }
#c3ai { left: 792px; top: 118px; width: 150px; height: 150px; }
""")


@beat
def b03_routine_checklist():
    """«коротше я допомагаю бізнесам впроваджувати ШІ та автоматизовувати їх
    роботу.»

    Her jump cut folds the tag into a card of routine: four jobs written out
    (checks and lines — her rule for tasks). Claude lands on «ШІ» and on
    «автоматизовувати» runs down the list: each box fills, each line is
    struck. Gone by her next cut at 18.10. She says «їх роботу», not the
    script's «дурні процеси»."""
    rows = "".join(
        '<div class="c3row" id="c3r%d" style="top:%dpx"><div class="rck"><div class="f" id="c3f%d"></div>%s</div>'
        '<div class="c3t" id="c3t%d">%s<i class="c3s" id="c3s%d"></i></div></div>'
        % (i, 104 + i * 106, i, check_svg("c3k%d" % i), i, t, i) for i, t in enumerate(TASKS))
    html = fill(u'''
      <div class="g full" id="g3">
        <div id="c3" class="dglass edge abs">
          <div class="cx" id="c3lab">РУТИНА</div>
          {{rows}}
        </div>
        <div id="c3ai" class="abs hide"><div class="jelly">{{claude}}<div class="sheen"></div></div></div>
      </div>''', rows=rows, claude=g.mark("claude"))
    src = js('''
  tl.set("#g3", {autoAlpha: 1}, @t_in);
  gsap.set(".c3row .f", {autoAlpha: 0, scale: 0.4, transformOrigin: "50% 50%"});
  gsap.set(".c3s", {scaleX: 0});
  ["c3k0", "c3k1", "c3k2", "c3k3"].forEach(function (id) { G.drawPrep(id); });
  G.blurIn("#c3", @t_in, 12, 0.32);
  tl.fromTo("#c3", {scaleY: 0.3, scaleX: 0.93, transformOrigin: "50% 25%"}, {scaleY: 1, scaleX: 1, duration: 0.8, ease: SP}, @t_in);
  tl.fromTo("#c3lab", {autoAlpha: 0, y: 10}, {autoAlpha: 1, y: 0, duration: 0.5, ease: SP}, @t_lab);
  // «допомагаю бізнесам» — the routine lists itself
  tl.fromTo(".c3row", {autoAlpha: 0, x: -24}, {autoAlpha: 1, x: 0, duration: 0.5, ease: SP, stagger: 0.12}, @dopom);
  // «ШІ» — Claude lands on the card
  G.arrive("#c3ai", @t_ai, {s: 0.4, y: -40});
  tl.fromTo("#c3ai .mk", {scale: 0.55, autoAlpha: 0}, {scale: 1, autoAlpha: 1, duration: 0.55, ease: SP}, @shi);
  G.sheen("#c3ai .sheen", @t_aish);
  // «автоматизовувати» — it runs down the list and every line is done
  tl.to("#c3ai", {y: 443, duration: 1.0, ease: "power2.inOut"}, @avtomat);
  [0, 1, 2, 3].forEach(function (i) {
    var t = @avtomat + 0.12 + i * 0.27;
    tl.to("#c3f" + i, {autoAlpha: 1, scale: 1, duration: 0.35, ease: POP}, t);
    G.draw("c3k" + i, t + 0.05, 0.25);
    tl.to("#c3s" + i, {scaleX: 1, duration: 0.3, ease: "power2.out"}, t + 0.06);
    tl.to("#c3t" + i, {color: "rgba(255,255,255,0.5)", duration: 0.3}, t + 0.06);
  });
  // «їх роботу» — done
  G.bump("#c3ai", @yikh);
  tl.to(["#c3", "#c3ai"], {scale: 0.9, y: "-=30", duration: 0.26, ease: "power2.in"}, @t_out);
  G.blurOut(["#c3", "#c3ai"], @t_out, 10, 0.24);
  tl.to("#g3", {autoAlpha: 0, duration: 0.02}, @t_off);''',
             t_in=T["korotshe"] - 0.04, t_lab=T["korotshe"] + 0.2,
             t_ai=T["shi"] - 0.14, t_aish=T["shi"] + 0.35,
             t_out=T["robotu"] + 0.14, t_off=T["robotu"] + 0.42)
    return html, src


# =================================================================== b05
CONTACTS = [  # (initial, name, preview, unread, left, top)
    (u"О", u"Оля", u"Коли стартуємо?", 2, 40, 850),
    (u"М", u"Макс", u"Скинь рахунок, будь ласка", 5, 370, 680),
    (u"І", u"Ірина", u"А що там по дзвінку?", 3, 700, 880),
]
k.css("""
/* ---- b05 · three conversations behind her head ---- */
.ct { width: 340px; height: 164px; border-radius: 50px; }
.ctav { position: absolute; left: 24px; top: 40px; width: 84px; height: 84px; border-radius: 50%;
  background: linear-gradient(160deg, #ff8ab0 0%, #c4143a 60%, #7a0a20 100%);
  box-shadow: inset 0 2px 1px rgba(255,255,255,0.5), 0 8px 18px -6px rgba(10,0,4,0.5);
  display: flex; align-items: center; justify-content: center; font-size: 40px; font-weight: 700; color: #fff; }
.ctav b { position: absolute; font-weight: 700; }
.ctn { position: absolute; left: 128px; top: 36px; font-size: 36px; font-weight: 700; }
.ctp { position: absolute; left: 128px; top: 88px; width: 190px; font-size: 25px; font-weight: 500;
  color: rgba(255,255,255,0.68); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.ctb { position: absolute; z-index: 4; right: -12px; top: -14px; width: 54px; height: 54px; border-radius: 50%;
  background: linear-gradient(165deg, #ff5c8f 0%, #e0204b 100%); color: #fff; font-size: 28px; font-weight: 700;
  display: flex; align-items: center; justify-content: center;
  box-shadow: 0 0 0 4px rgba(255,255,255,0.9), 0 10px 20px -6px rgba(10,0,4,0.5); }
""")


@beat
def b05_forgotten_contacts():
    """«то питання CRM в мене стояло дуже гостро, бо 1, 2, 3 і я всьо забула
    з ким про що спілкувались»

    Behind her (matte `contacts`): three conversations float up round her
    head on «CRM», «стояло», «дуже», and each gets an unread badge on
    «гостро». On «1», «2», «3» she forgets them one by one — name and message
    blur, the card sinks; on «забула» they drift off; on «з ким» their
    initials turn into question marks. The middle one lifts clear of her hair
    on «спілкувались» and the takeover opens out of it."""
    cards = []
    for i, (ini, nm, pv, n, x, y) in enumerate(CONTACTS):
        cards.append(
            u'<div class="dglass edge abs ct hide" id="ct%d" style="left:%dpx;top:%dpx">'
            u'<div class="ctav"><b id="cti%d">%s</b><b id="ctq%d" class="hide">?</b></div>'
            u'<div class="ctn" id="ctn%d">%s</div><div class="ctp" id="ctp%d">%s</div>'
            u'<div class="ctb hide" id="ctb%d">%d</div></div>' % (i, x, y, i, ini, i, i, nm, i, pv, i, n))
    html = u'''
      <div class="g full" id="g5">
        %s
      </div>''' % "\n        ".join(cards)
    src = js('''
  tl.set("#g5", {autoAlpha: 1}, @t_in);
  // «CRM» / «стояло» / «дуже» — three conversations come up behind her
  G.arrive("#ct0", @t_a0, {s: 0.55, y: 40});
  G.arrive("#ct1", @t_a1, {s: 0.55, y: 40});
  G.arrive("#ct2", @t_a2, {s: 0.55, y: 40});
  // «гостро» — every one of them is waiting on her
  [0, 1, 2].forEach(function (i) {
    var t = @hostro + i * 0.09;
    tl.fromTo("#ctb" + i, {scale: 0, autoAlpha: 0}, {scale: 1, autoAlpha: 1, duration: 0.45, ease: POP}, t);
    G.haptic("#ct" + i, t + 0.05);
  });
  // «1, 2, 3» — and one by one she forgets who they were
  [[0, @one], [1, @two], [2, @three]].forEach(function (p) {
    var i = p[0], t = p[1];
    tl.to(["#ctn" + i, "#ctp" + i], {filter: "blur(9px)", autoAlpha: 0.45, duration: 0.3, ease: "power2.out"}, t);
    tl.to("#ctb" + i, {scale: 0, autoAlpha: 0, duration: 0.2, ease: "power2.in"}, t);
    tl.to("#ct" + i, {scale: 0.93, y: "+=18", duration: 0.4, ease: SP}, t);
  });
  // «забула» — they drift off
  tl.to("#ct0", {x: -50, autoAlpha: 0.6, duration: 0.7, ease: "power2.out"}, @zabula);
  tl.to("#ct2", {x: 50, autoAlpha: 0.6, duration: 0.7, ease: "power2.out"}, @zabula);
  tl.to("#ct1", {y: "-=16", autoAlpha: 0.7, duration: 0.7, ease: "power2.out"}, @zabula);
  // «з ким» — who was that?
  [0, 1, 2].forEach(function (i) {
    tl.to("#cti" + i, {autoAlpha: 0, scale: 0.5, duration: 0.2}, @zkym + i * 0.07);
    tl.fromTo("#ctq" + i, {autoAlpha: 0, scale: 0.4}, {autoAlpha: 1, scale: 1, duration: 0.45, ease: POP}, @t_q + i * 0.07);
  });
  // «спілкувались» — the sides go; the middle lifts clear of her hair
  G.blurOut(["#ct0", "#ct2"], @spilk1, 10, 0.3);
  tl.to("#ct1", {y: -120, scale: 1, autoAlpha: 1, duration: 0.5, ease: SP}, @spilk1);
  tl.to("#g5", {autoAlpha: 0, duration: 0.02}, @t_off);''',
             t_in=T["crm2"] - 0.10, t_a0=T["crm2"] - 0.06, t_a1=T["stoyalo"] - 0.06,
             t_a2=T["duzhe1"] - 0.06, t_q=T["zkym"] + 0.1, t_off=T["ale1"] + 0.16)
    return html, src


# =================================================================== b06
FIELDS = [u"ХТО", u"ПРО ЩО", u"ЗВІДКИ", u"СКІЛЬКИ", u"ЕТАП"]
BLANKS = [520, 610, 300, 240, 700]
STAGES = [u"Лід", u"Дзвінок", u"Офер", u"Оплата"]
STAGE_X = [26, 254, 482, 710]
DAYS = [u"2 дн", u"3 дн", u"1 дн"]
k.css("""
/* ---- b06 · over her: one client's CRM card, field by field ---- */
#tk6 { position: absolute; inset: 0; clip-path: circle(0px at 540px 642px); }
#crdW { left: 100px; top: 170px; width: 880px; height: 1040px; transform-origin: 440px 472px; }
#crd { position: absolute; inset: 0; }
#crLab { left: 60px; top: 50px; }
#crHair { left: 60px; right: 60px; top: 104px; }
.fld { position: absolute; left: 60px; width: 760px; height: 178px; }
.fld > .t-micro { position: absolute; left: 0; top: 24px; }
#crLab, .fld > .t-micro { color: rgba(23,20,28,0.58); }
.fld .blank { position: absolute; left: 0; top: 76px; height: 46px; border-radius: 16px; background: rgba(23,20,28,0.07); }
.fld .fh { position: absolute; left: 0; right: 0; bottom: 0; height: 2px; background: rgba(23,20,28,0.07); }
#fav { left: 0; top: 64px; width: 96px; height: 96px; border-radius: 50%;
  background: linear-gradient(165deg, #e0204b 0%, #ab112e 50%, #6b081c 100%);
  box-shadow: inset 0 2px 1px rgba(255,255,255,0.5), 0 12px 24px -10px rgba(70,4,20,0.6);
  display: flex; align-items: center; justify-content: center; color: #fff; font-size: 46px; font-weight: 700; }
#fnm { left: 122px; top: 66px; font-size: 44px; font-weight: 700; letter-spacing: -0.015em; }
#fsb { left: 122px; top: 120px; }
.fnote { position: absolute; left: 0; font-size: 32px; font-weight: 500; color: rgba(23,20,28,0.84); white-space: nowrap; }
#fn1 { top: 66px; } #fn2 { top: 114px; color: rgba(23,20,28,0.56); }
#fsrc { left: 0; top: 72px; height: 66px; padding: 0 28px 0 18px; border-radius: 33px; font-size: 30px; }
#fsrc .mk { width: 34px; height: 34px; fill: #b4122f; }
#fsum { left: -4px; top: 56px; font-size: 96px; }
#fpaid { left: 360px; top: 88px; }
#fpaid .rck { width: 36px; height: 36px; box-shadow: none; }
#fpaid .rck svg { stroke-width: 3.6; }
.tmav { position: absolute; top: 0px; width: 52px; height: 52px; border-radius: 50%; color: #fff; font-size: 24px;
  font-weight: 700; display: flex; align-items: center; justify-content: center;
  box-shadow: 0 0 0 4px #fff, 0 8px 16px -6px rgba(70,4,20,0.4); }
#stTrack { left: 26px; top: 116px; width: 684px; height: 8px; border-radius: 4px; background: #f4dfe5; transform-origin: 0% 50%; }
.stdot { position: absolute; top: 104px; width: 32px; height: 32px; margin-left: -16px; border-radius: 50%;
  background: #fff; box-shadow: inset 0 0 0 5px #ecc8d0; }
.stdot i { position: absolute; inset: 0; border-radius: 50%; display: block;
  background: linear-gradient(165deg, #e0204b 0%, #8d0d24 100%); box-shadow: 0 0 0 5px rgba(255,110,156,0.25); }
.stlab { position: absolute; top: 144px; width: 160px; margin-left: -80px; text-align: center;
  font-size: 24px; font-weight: 700; color: rgba(23,20,28,0.62); }
.stdur { position: absolute; top: 56px; width: 110px; margin-left: -55px; height: 44px; border-radius: 22px;
  background: #fbe3ea; color: #b4122f; font-size: 24px; font-weight: 700;
  display: flex; align-items: center; justify-content: center; }
""")


@beat
def b06_crm_card():
    """«Але при цьому CRM для агенції це зазвичай щось дуже і дуже просте: нам
    треба знати всі деталі про людину, про що ми спілкувались, обов'язково
    звідки вона прийшла, скільки вона заплатила нам грошей і якщо у нас є
    команда продажів, то тоді ще й скільки часу пройшло на кожному етапі»

    The iris opens out of the forgotten middle contact onto burgundy; the
    contact grows into one white CRM card. On «щось дуже і дуже просте» five
    fields appear, all empty — ХТО / ПРО ЩО / ЗВІДКИ / СКІЛЬКИ / ЕТАП. Each
    fills on its own words: the person, the notes, Instagram, €1 200 counted
    up (a demo card), a sales team, then the stages with the days between
    them, lit in turn on «на кожному етапі». On «Тому» the card folds up into
    the shelf above her head as the iris closes on it. Field names are not
    her words at those moments, so captions stay (white, on the plaque)."""
    blanks = "".join(
        '<div class="fld" id="fld%d" style="top:%dpx"><div class="t-micro">%s</div>'
        '<div class="blank" id="fb%d" style="width:%dpx"></div>{{v%d}}%s</div>'
        % (i, 124 + i * 178, f, i, BLANKS[i], i, '<div class="fh"></div>' if i < 4 else "")
        for i, f in enumerate(FIELDS))
    team = "".join('<div class="tmav" style="right:%dpx;background:%s">%s</div>' % (r, bg, t)
                   for r, bg, t in [(0, "linear-gradient(160deg,#ff8ab0,#c4143a)", u"А"),
                                    (40, "linear-gradient(160deg,#c4143a,#6b081c)", u"Т"),
                                    (80, "linear-gradient(160deg,#e8a0b4,#a8102c)", u"О")])
    stages = "".join('<div class="stdot" style="left:%dpx"><i></i></div><div class="stlab" style="left:%dpx">%s</div>'
                     % (x, x, s) for x, s in zip(STAGE_X, STAGES))
    durs = "".join('<div class="stdur" style="left:%dpx">%s</div>' % ((a + b) // 2, d)
                   for a, b, d in zip(STAGE_X, STAGE_X[1:], DAYS))
    html = fill(u'''
      <div class="g full" id="g6">
        <div id="tk6">
          <div class="tkg"></div>
          <div class="aurs"></div>
          <div class="grain"></div>
          <div id="crdW" class="abs hide"><div id="crd" class="sheet">
            <div class="cx t-micro" id="crLab">КАРТКА КЛІЄНТА</div>
            <div class="cx hair" id="crHair"></div>
            {{fields}}
            <div class="sheen"></div>
          </div></div>
        </div>
      </div>''', fields=fill(blanks,
        v0=u'<div class="cx" id="fav">М</div><div class="cx" id="fnm">Марія Коваль</div>'
           u'<div class="cx t-sub" id="fsb">кав’ярня «Зерно» · Київ</div>',
        v1=u'<div class="fnote" id="fn1">Хоче чатбот для замовлень</div>'
           u'<div class="fnote" id="fn2">Дзвінок у четвер · офер до п’ятниці</div>',
        v2=u'<div class="cx chip" id="fsrc">%s<span>Instagram · рілс</span></div>' % g.mark("instagram"),
        v3=u'<div class="cx t-big" id="fsum">€0</div>'
           u'<div class="cx chip" id="fpaid"><div class="rck"><div class="f"></div>%s</div><span>оплачено</span></div>'
           % check_svg("fpk"),
        v4=u'<div id="team">%s</div><div class="cx" id="stTrack"></div>%s%s' % (team, stages, durs)))
    src = js('''
  tl.set("#g6", {autoAlpha: 1}, @ale1);
  gsap.set(["#fav", "#fnm", "#fsb", "#fn1", "#fn2", "#fsrc", "#fsum", "#fpaid", ".tmav", ".stdot", ".stlab", ".stdur"], {autoAlpha: 0});
  gsap.set(".stdot i", {autoAlpha: 0, scale: 0.3, transformOrigin: "50% 50%"});
  gsap.set("#stTrack", {scaleX: 0});
  G.drawPrep("fpk");
  // «Але» — the iris opens out of the forgotten contact
  G.irisOpen("#tk6", @ale1, 540, 642, 0.85);
  drift1("#tk6", @ale1, 17.4);
  G.blurIn("#crdW", @t_c, 16, 0.45);
  tl.fromTo("#crdW", {scale: 0.39}, {scale: 1, duration: 1.05, ease: spring(0.72, 12)}, @t_c);
  tl.fromTo("#crLab", {autoAlpha: 0, y: 12}, {autoAlpha: 1, y: 0, duration: 0.5, ease: SP}, @t_c2);
  tl.fromTo("#crHair", {scaleX: 0}, {scaleX: 1, duration: 0.7, ease: "power3.out"}, @t_c2);
  // «щось дуже і дуже просте» — five fields, all empty
  tl.fromTo(".fld > .t-micro", {autoAlpha: 0, y: 12}, {autoAlpha: 1, y: 0, duration: 0.5, ease: SP, stagger: 0.12}, @shchos);
  tl.fromTo(".fld .blank", {scaleX: 0, transformOrigin: "0% 50%"}, {scaleX: 1, duration: 0.55, ease: "power3.out", stagger: 0.12}, @t_bl);
  tl.fromTo(".fld .fh", {scaleX: 0, transformOrigin: "0% 50%"}, {scaleX: 1, duration: 0.6, ease: "power3.out", stagger: 0.12}, @t_bl);
  G.sheen("#crd .sheen", @proste);
  // ХТО — «всі деталі про людину»
  tl.to("#fb0", {autoAlpha: 0, duration: 0.2}, @detali);
  tl.fromTo("#fav", {scale: 0.4, autoAlpha: 0}, {scale: 1, autoAlpha: 1, duration: 0.6, ease: POP}, @detali);
  G.blurIn("#fnm", @t_nm, 10, 0.3);
  tl.fromTo("#fnm", {x: -16}, {x: 0, duration: 0.6, ease: SP}, @t_nm);
  G.blurIn("#fsb", @t_sb, 10, 0.3);
  // ПРО ЩО — «про що ми спілкувались»
  tl.to("#fb1", {autoAlpha: 0, duration: 0.2}, @proshcho);
  tl.set("#fn1", {autoAlpha: 1}, @proshcho);
  tl.fromTo("#fn1", {clipPath: "inset(0px 100% 0px 0px)"}, {clipPath: "inset(0px 0% 0px 0px)", duration: 0.6, ease: "power1.inOut", immediateRender: false}, @proshcho);
  tl.set("#fn2", {autoAlpha: 1}, @t_n2);
  tl.fromTo("#fn2", {clipPath: "inset(0px 100% 0px 0px)"}, {clipPath: "inset(0px 0% 0px 0px)", duration: 0.6, ease: "power1.inOut", immediateRender: false}, @t_n2);
  // ЗВІДКИ — «звідки вона прийшла»
  tl.to("#fb2", {autoAlpha: 0, duration: 0.2}, @t_src);
  G.arrive("#fsrc", @t_src, {s: 0.5, y: 20});
  // СКІЛЬКИ — «скільки вона заплатила нам грошей»
  tl.to("#fb3", {autoAlpha: 0, duration: 0.2}, @t_sum);
  tl.fromTo("#fsum", {autoAlpha: 0, y: 20}, {autoAlpha: 1, y: 0, duration: 0.5, ease: SP}, @t_sum);
  tl.fromTo("#fpaid", {autoAlpha: 0, scale: 0.6}, {autoAlpha: 1, scale: 1, duration: 0.55, ease: POP}, @groshey);
  G.draw("fpk", @t_pk, 0.3);
  // ЕТАП — «команда продажів»
  tl.fromTo(".tmav", {scale: 0, autoAlpha: 0}, {scale: 1, autoAlpha: 1, duration: 0.5, ease: POP, stagger: 0.09}, @komanda);
  // «то тоді ще й» — the stages
  tl.to("#fb4", {autoAlpha: 0, duration: 0.2}, @totodi);
  tl.to("#stTrack", {scaleX: 1, duration: 0.6, ease: "power2.inOut"}, @totodi);
  tl.fromTo(".stdot", {scale: 0, autoAlpha: 0}, {scale: 1, autoAlpha: 1, duration: 0.45, ease: POP, stagger: 0.12}, @t_dots);
  tl.fromTo(".stlab", {autoAlpha: 0, y: 8}, {autoAlpha: 1, y: 0, duration: 0.4, ease: SP, stagger: 0.12}, @t_labs);
  // «скільки часу пройшло» — the days between them
  tl.fromTo(".stdur", {autoAlpha: 0, scale: 0.5}, {autoAlpha: 1, scale: 1, duration: 0.5, ease: POP, stagger: 0.16}, @t_dur);
  // «на кожному етапі» — each stage lit in turn
  tl.to(".stdot i", {autoAlpha: 1, scale: 1, duration: 0.35, ease: POP, stagger: 0.2}, @t_lit);
  // «Тому» — the card folds up into the shelf above her head
  tl.set("#crdW", {transformOrigin: "440px 230px"}, @t_f0);
  tl.to("#crdW", {scale: 0.3, duration: 0.5, ease: "power3.in"}, @tomu1);
  G.blurOut("#crdW", @t_f1, 12, 0.28);
  G.irisClose("#tk6", @t_f2, 540, 400, 0.6);
  tl.to("#g6", {autoAlpha: 0, duration: 0.02}, @t_off);''',
             t_c=T["ale1"] + 0.10, t_c2=T["ale1"] + 0.50, t_bl=T["shchos"] + 0.08,
             t_nm=T["lyudynu"] - 0.08, t_sb=T["lyudynu"] + 0.16, t_n2=T["spilk2"] + 0.30,
             t_src=T["zvidky"] - 0.06, t_sum=T["skilky1"] - 0.12, t_pk=T["groshey"] + 0.08,
             t_dots=T["totodi"] + 0.10, t_labs=T["totodi"] + 0.16, t_dur=T["skilky2"] + 0.10,
             t_lit=T["kozhnomu"] - 0.10, t_f0=T["tomu1"] - 0.02, t_f1=T["tomu1"] + 0.22,
             t_f2=T["tomu1"] + 0.02, t_off=T["tomu1"] + 0.66)
    return html, src


# =================================================================== b11
TOOLS = [("googlesheets", 250), ("airtable", 540), ("notion", 830)]
k.css("""
/* ---- b11 · near: three cheap tools, Notion wins ---- */
#s11 { left: 70px; top: 250px; width: 940px; height: 300px; }
.s11t { position: absolute; top: 290px; width: 176px; height: 176px; margin-left: -88px; }
.pz { position: absolute; top: 486px; width: 104px; margin-left: -52px; height: 52px; border-radius: 26px;
  background: linear-gradient(160deg, #ff7aa4 0%, #e0204b 60%, #a8102c 100%); color: #fff;
  font-size: 30px; font-weight: 700; display: flex; align-items: center; justify-content: center;
  box-shadow: inset 0 2px 1px rgba(255,255,255,0.45), 0 12px 24px -10px rgba(40,2,12,0.6); }
#s11r { left: 742px; top: 290px; width: 176px; height: 176px; }
""")


@beat
def b11_cheap_tools():
    """«Тому якщо ми тільки починаємо і нам треба щось дешеве і сердите, то
    об'єктивно Notion нам підійде»

    The CRM card folded into a glass shelf above her head. Three cheap tools
    arrive as ghosts on «починаємо» — Google Sheets, Airtable, Notion — and
    each gets a €0 tag on «дешеве»; they firm up on «сердите». On
    «об'єктивно» two step back, and on «Notion» the third turns pearl, the
    hero. Everything is gone at 49.04: her closeup at 49.07 is a joke."""
    tiles = "".join(
        '<div class="s11t hide" id="s11t%d" style="left:%dpx"><div class="clear edge">%s</div>%s</div>'
        % (i, x, g.mark(m), ('<div class="pearl hide" id="s11np">%s<div class="sheen"></div></div>'
                             % g.mark("notion")) if m == "notion" else "")
        for i, (m, x) in enumerate(TOOLS))
    tags = "".join('<div class="pz hide" id="pz%d" style="left:%dpx">€0</div>' % (i, x)
                   for i, (_, x) in enumerate(TOOLS))
    html = fill(u'''
      <div class="g full" id="g11">
        <div id="s11" class="shelf edge abs hide"></div>
        <div class="sqring hide" id="s11r"></div>
        {{tiles}}
        {{tags}}
      </div>''', tiles=tiles, tags=tags)
    src = js('''
  tl.set("#g11", {autoAlpha: 1}, @t_in);
  G.blurIn("#s11", @t_in, 14, 0.4);
  tl.fromTo("#s11", {scaleX: 0.5, scaleY: 0.7}, {scaleX: 1, scaleY: 1, duration: 0.9, ease: SP}, @t_in);
  // «тільки починаємо» — three ghosts
  gsap.set(".s11t .clear .mk", {autoAlpha: 0.3});
  [0, 1, 2].forEach(function (i) { G.arrive("#s11t" + i, @t_g + i * 0.1, {s: 0.5, y: 30}); });
  // «дешеве» — every one of them costs nothing
  tl.fromTo(".pz", {autoAlpha: 0, scale: 0.4, y: -20}, {autoAlpha: 1, scale: 1, y: 0, duration: 0.5, ease: POP, stagger: 0.1}, @deshev);
  // «і сердите» — they firm up
  tl.to(".s11t .clear .mk", {autoAlpha: 1, duration: 0.3, stagger: 0.08}, @serdyte);
  [0, 1, 2].forEach(function (i) { G.bump("#s11t" + i, @serdyte + i * 0.08); });
  // «об'єктивно» — two step back
  tl.to(["#s11t0", "#s11t1", "#pz0", "#pz1"], {autoAlpha: 0.3, scale: 0.86, duration: 0.4, ease: "power2.out"}, @obyekt);
  // «Notion» — the one
  tl.to("#s11np", {autoAlpha: 1, duration: 0.25}, @t_n);
  tl.to("#s11t2", {scale: 1.16, duration: 0.5, ease: POP}, @t_n);
  G.ripple("#s11r", @notion1);
  G.sheen("#s11np .sheen", @t_nsh);
  // clear before her closeup at 49.07
  tl.to(["#s11t0", "#s11t1", ".pz"], {autoAlpha: 0, scale: 0.6, duration: 0.2, ease: "power2.in"}, @t_x);
  G.blurOut("#s11", @t_x, 12, 0.22);
  tl.to("#s11t2", {scale: 0.5, autoAlpha: 0, duration: 0.22, ease: "power2.in"}, @t_x);
  tl.to("#g11", {autoAlpha: 0, duration: 0.02}, @t_off);''',
             t_in=T["tomu1"] + 0.46, t_g=T["pochyn"] - 0.08, t_n=T["notion1"] - 0.06,
             t_nsh=T["notion1"] + 0.12, t_x=48.800, t_off=49.040)
    return html, src


# =================================================================== b12
ROWS = [  # name, source, sum, stage, stage class
    (u"Марія Коваль", "Instagram", u"€1 200", u"Оплата", "s4"),
    (u"Андрій Шевчук", u"Сайт", u"€800", u"Офер", "s3"),
    (u"Олена Бондар", "Telegram", u"—", u"Дзвінок", "s2"),
    (u"Студія «Піксель»", u"Реферал", u"€2 400", u"Оплата", "s4"),
    (u"Ігор Мельник", "Instagram", u"—", u"Лід", "s1"),
]
k.css("""
/* ---- b12 · over her: the Notion table that builds itself ---- */
#tk12 { position: absolute; inset: 0; clip-path: circle(0px at 830px 378px); }
#ndT { left: 742px; top: 290px; width: 176px; height: 176px; }
#ndW { left: 70px; top: 190px; width: 940px; height: 1010px; transform-origin: 760px 188px; }
#nd { position: absolute; inset: 0; }
#ndIc { left: 56px; top: 50px; width: 96px; height: 96px; }
#ndTitle { left: 176px; top: 50px; font-size: 52px; font-weight: 700; letter-spacing: -0.02em; }
#ndSub { left: 178px; top: 116px; }
#ndViews { left: 56px; top: 180px; display: flex; gap: 10px; }
.vw { height: 50px; padding: 0 22px; border-radius: 25px; font-size: 24px; font-weight: 700;
  display: flex; align-items: center; color: rgba(23,20,28,0.5); background: rgba(23,20,28,0.05); }
.vw.on { background: #17141c; color: #fff; }
.ndc { position: absolute; top: 0; }
.ndc.c0 { left: 0; } .ndc.c1 { left: 360px; } .ndc.c2 { left: 560px; } .ndc.c3 { left: 690px; }
#ndHead { left: 56px; width: 828px; top: 262px; height: 50px; font-size: 22px; font-weight: 700;
  letter-spacing: 0.08em; color: rgba(23,20,28,0.58); }
#ndHair { left: 56px; right: 56px; top: 312px; }
.ndr { position: absolute; left: 56px; width: 828px; height: 92px; }
.ndr .ndc { top: 26px; font-size: 30px; }
.ndr .c0 { font-weight: 700; } .ndr .c1 { font-weight: 500; color: rgba(23,20,28,0.56); }
.ndr .c2 { font-weight: 700; }
.ndr .c3 { top: 20px; height: 48px; padding: 0 20px; border-radius: 24px; font-size: 24px; font-weight: 700;
  display: flex; align-items: center; }
.s1 { background: rgba(23,20,28,0.07); color: rgba(23,20,28,0.6); }
.s2 { background: #f4dfe5; color: #6b081c; }
.s3 { background: #fbe3ea; color: #b4122f; }
.s4 { background: linear-gradient(165deg, #e0204b 0%, #8d0d24 100%); color: #fff; }
.ndr .rl { position: absolute; left: 0; right: 0; bottom: 0; height: 2px; background: rgba(23,20,28,0.06); }
#ndNew { left: 56px; top: 314px; height: 92px; font-size: 30px; font-weight: 500; color: rgba(23,20,28,0.54);
  display: flex; align-items: center; }
#ndCur { left: 690px; top: 860px; width: 64px; height: 64px; }
#ndCur svg { width: 100%; height: 100%; filter: drop-shadow(0 6px 10px rgba(8,0,3,0.35)); }
#ndAI { left: 822px; top: 104px; width: 190px; height: 190px; perspective: 1100px; }
#ndFlip { position: absolute; inset: 0; transform-style: preserve-3d; }
.face { position: absolute; inset: 0; backface-visibility: hidden; -webkit-backface-visibility: hidden; }
.face.back { transform: rotateY(180deg); }
#ndAg { top: 1040px; }
#ndAgC { position: relative; height: 104px; padding: 0 46px 0 34px; border-radius: 52px; display: inline-flex; align-items: center; gap: 16px;
  font-size: 42px; font-weight: 700; color: #fff; overflow: hidden; white-space: nowrap;
  background: linear-gradient(160deg, #ff7aa4 0%, #e0204b 45%, #8d0d24 100%);
  box-shadow: inset 0 2px 1px rgba(255,255,255,0.55), inset 0 -14px 26px -10px rgba(255,190,210,0.55),
              0 0 0 1px rgba(255,255,255,0.2), 0 0 60px rgba(255,110,156,0.55), 0 40px 70px -30px rgba(8,0,3,0.8); }
#ndAgC svg { width: 46px; height: 46px; fill: #fff; flex: none; }
#ndAgC .mz { font-weight: 500; color: rgba(255,255,255,0.72); }
#ndAgC .sheen { mix-blend-mode: normal; opacity: 0.5; }
#ndAgR { left: 250px; top: 1040px; width: 580px; height: 104px; border-radius: 52px; }
""")


@beat
def b12_notion_builds_itself():
    """«І навіть не треба нічого ручками робити, твій Claude або ChatGPT сам
    побудує там систему як треба, і це буде майже agentic system! Такий сетап
    може витримати»

    After her closeup the Notion tile is back where it left, and the iris
    opens out of it onto burgundy. It flies up to become the icon of a
    Notion page «Клієнти»: views, columns, an empty table. On «нічого
    ручками» a cursor reaches for «+ Новий» and is not needed. Claude lands on
    «Claude», flips to ChatGPT on «ChatGPT», and on «сам побудує» five rows
    arrive by themselves — Марія Коваль from the card first. «майже agentic
    system» lights as a chip (blackout 56.58-58.86: it says the words). On
    «може витримати» the record count runs away and the iris closes onto it,
    clear before her pull-out at 60.25."""
    rows = []
    for i, (nm, src_, sm, st, sc) in enumerate(ROWS):
        rows.append(u'<div class="ndr hide" id="ndr%d" style="top:%dpx"><div class="ndc c0">%s</div>'
                    u'<div class="ndc c1">%s</div><div class="ndc c2">%s</div>'
                    u'<div class="ndc c3 %s">%s</div><i class="rl"></i></div>'
                    % (i, 314 + i * 92, nm, src_, sm.replace(" ", "&nbsp;"), sc, st))
    html = fill(u'''
      <div class="g full" id="g12">
        <div id="tk12">
          <div class="tkg"></div>
          <div class="aurs"></div>
          <div class="grain"></div>
          <div id="ndW" class="abs hide"><div id="nd" class="sheet">
            <div class="cx hide" id="ndIc"><div class="pearl">{{notion}}</div></div>
            <div class="cx" id="ndTitle">Клієнти</div>
            <div class="cx t-sub" id="ndSub">База даних · записів: <b id="ndN">0</b></div>
            <div class="cx" id="ndViews"><div class="vw on">Таблиця</div><div class="vw">Дошка</div><div class="vw">Календар</div></div>
            <div class="cx" id="ndHead"><div class="ndc c0">ІМ’Я</div><div class="ndc c1">ДЖЕРЕЛО</div><div class="ndc c2">СУМА</div><div class="ndc c3">ЕТАП</div></div>
            <div class="cx hair" id="ndHair"></div>
            {{rows}}
            <div class="cx" id="ndNew">+&nbsp;&nbsp;Новий</div>
            <div class="sheen"></div>
          </div></div>
          <div class="sqring hide" id="ndAgR"></div>
          <div class="ctr hide" id="ndAg"><div id="ndAgC">{{spark}}<span class="mz">майже</span><span id="ndAgW">agentic system</span><div class="sheen"></div></div></div>
          <div id="ndCur" class="abs hide">{{cursor}}</div>
          <div id="ndAI" class="abs hide"><div id="ndFlip">
            <div class="face front"><div class="jelly">{{claude}}</div></div>
            <div class="face back"><div class="jelly">{{openai}}</div></div>
          </div></div>
        </div>
        <div id="ndT" class="abs hide"><div class="pearl">{{notion}}</div></div>
      </div>''', notion=g.mark("notion"), rows="\n            ".join(rows),
                spark='<svg viewBox="0 0 24 24"><path d="%s"/></svg>' % SPARK_PATH, cursor=CURSOR,
                claude=g.mark("claude"), openai=g.mark("openai"))
    src = js('''
  tl.set("#g12", {autoAlpha: 1}, @i_af);
  // «І» — the Notion tile is back where it left, and the iris opens out of it
  G.arrive("#ndT", @i_af, {s: 0.5, y: 20});
  G.irisOpen("#tk12", @t_iris, 830, 378, 0.85);
  drift1("#tk12", @t_iris, 9.9);
  // the page grows out of the tile; the tile becomes its icon
  G.blurIn("#ndW", @t_sh, 16, 0.45);
  tl.fromTo("#ndW", {scale: 0.2}, {scale: 1, duration: 1.05, ease: spring(0.72, 12)}, @t_sh);
  tl.to("#ndT", {x: -656, y: -90, scale: 0.545, duration: 0.7, ease: SP}, @t_sh);
  tl.set("#ndIc", {autoAlpha: 1}, @t_land);
  tl.set("#ndT", {autoAlpha: 0}, @t_land);
  tl.fromTo(["#ndTitle", "#ndSub", "#ndViews"], {autoAlpha: 0, y: 14}, {autoAlpha: 1, y: 0, duration: 0.55, ease: SP, stagger: 0.07}, @t_ttl);
  // «навіть не треба» — an empty table
  tl.fromTo("#ndHead .ndc", {autoAlpha: 0, y: 10}, {autoAlpha: 1, y: 0, duration: 0.45, ease: SP, stagger: 0.06}, @navit);
  tl.fromTo("#ndHair", {scaleX: 0}, {scaleX: 1, duration: 0.6, ease: "power3.out", transformOrigin: "0% 50%"}, @navit);
  tl.fromTo("#ndNew", {autoAlpha: 0}, {autoAlpha: 1, duration: 0.4}, @t_new);
  // «нічого ручками робити» — a cursor reaches for «+ Новий» and is not needed
  G.blurIn("#ndCur", @t_cur, 8, 0.25);
  tl.fromTo("#ndCur", {x: 0, y: 0}, {x: -500, y: -324, duration: 0.95, ease: "power2.inOut"}, @t_cur);
  tl.to("#ndCur", {scale: 0.5, autoAlpha: 0, filter: "blur(8px)", duration: 0.3, ease: "power2.in"}, @robyty);
  // «твій Claude»
  G.blurIn("#ndAI", @t_ai, 14, 0.36);
  tl.fromTo("#ndAI", {x: 90, scale: 0.55}, {x: 0, scale: 1, duration: 0.85, ease: POP}, @t_ai);
  tl.fromTo("#ndAI .front .mk", {scale: 0.55, autoAlpha: 0}, {scale: 1, autoAlpha: 1, duration: 0.55, ease: SP}, @claude1);
  // «або ChatGPT» — FLIP, started on the word that names the new face
  tl.fromTo("#ndFlip", {rotationY: 0}, {rotationY: 180, duration: 1.0, ease: FLIP}, @t_flip);
  tl.to("#ndFlip", {scale: 0.9, duration: 0.3, ease: "power2.out"}, @t_flip);
  tl.to("#ndFlip", {scale: 1, duration: 0.6, ease: SP}, @t_flip2);
  // «сам побудує там систему як треба» — the rows arrive by themselves
  [0, 1, 2, 3, 4].forEach(function (i) {
    var t = @t_r0 + i * 0.28;
    G.blurIn("#ndr" + i, t, 10, 0.3);
    tl.fromTo("#ndr" + i, {x: 70, y: -12}, {x: 0, y: 0, duration: 0.6, ease: SP}, t);
    tl.to("#ndNew", {y: 92 * (i + 1), duration: 0.4, ease: SP}, t);
    G.bump("#ndFlip", t);
  });
  G.sheen("#nd .sheen", @t_rsh);
  // «майже agentic system»
  G.blurIn("#ndAg", @t_ag, 12, 0.35);
  tl.fromTo("#ndAg", {scale: 0.6, y: 24}, {scale: 1, y: 0, duration: 0.8, ease: POP}, @t_ag);
  tl.fromTo("#ndAgW", {autoAlpha: 0.2}, {autoAlpha: 1, duration: 0.3, immediateRender: false}, @t_agw);
  G.sheen("#ndAgC .sheen", @t_agsh);
  G.ripple("#ndAgR", @system);
  // «Такий сетап може витримати» — the record count runs away
  G.bump("#ndSub", @setap);
  // the iris closes onto the count, clear of her pull-out at 60.25
  G.blurOut(["#ndAg", "#ndAI"], @t_x0, 10, 0.3);
  G.irisClose("#tk12", @t_x1, 570, 322, 0.55);
  tl.to("#g12", {autoAlpha: 0, duration: 0.02}, @t_off);''',
             t_iris=T["i_af"] + 0.12, t_sh=T["i_af"] + 0.30, t_land=T["i_af"] + 0.92,
             t_ttl=T["i_af"] + 0.62, t_new=T["navit"] + 0.2, t_cur=T["nichoho"] - 0.04,
             t_ai=T["claude1"] - 0.12, t_flip=T["chatgpt"] - 0.16, t_flip2=T["chatgpt"] + 0.14,
             t_r0=T["pobuduye"] - 0.10, t_rsh=T["pobuduye"] + 1.5,
             t_ag=T["maizhe"] - 0.08, t_agw=T["agentic1"] - 0.04, t_agsh=T["agentic1"] + 0.12,
             t_run=T["mozhe"] - 0.06, t_x0=59.520, t_x1=59.560, t_off=60.180)
    return html, src


# =================================================================== b14
k.css("""
/* ---- b14 · near: the count lands in a capsule, €0 ---- */
#q14 { left: 90px; top: 240px; width: 900px; height: 190px; border-radius: 95px; }
#q14t { left: 30px; top: 30px; width: 130px; height: 130px; }
#q14n { left: 190px; top: 22px; font-size: 90px; font-weight: 900; letter-spacing: -0.04em; line-height: 100px; }
#q14l { left: 194px; top: 122px; font-size: 30px; font-weight: 500; color: rgba(255,255,255,0.72); }
#q14f { right: 34px; top: 52px; height: 86px; padding: 0 30px; border-radius: 43px; font-size: 40px; font-weight: 700;
  display: flex; align-items: center; color: #fff;
  background: linear-gradient(160deg, #ff7aa4 0%, #e0204b 55%, #a8102c 100%);
  box-shadow: inset 0 2px 1px rgba(255,255,255,0.5), 0 14px 28px -12px rgba(40,2,12,0.6); }
""")


@beat
def b14_free_tier():
    """«дууууже [her pull-out] багато навантаження ще й на безкоштовному
    тарифі»

    The runaway count lands in a glass capsule above her head and keeps
    climbing through «багато навантаження» to 10 000+; on «безкоштовному» a
    «€0 / міс» tag pops beside it."""
    html = fill(u'''
      <div class="g full" id="g14">
        <div id="q14" class="dglass edge abs">
          <div class="cx" id="q14t"><div class="pearl">{{notion}}</div></div>
          <div class="cx" id="q14n">1&nbsp;000</div>
          <div class="cx" id="q14l">записів у базі</div>
          <div class="cx hide" id="q14f">€0 / міс</div>
        </div>
      </div>''', notion=g.mark("notion"))
    src = js('''
  tl.set("#g14", {autoAlpha: 1}, @t_in);
  G.blurIn("#q14", @t_in, 14, 0.36);
  tl.fromTo("#q14", {scale: 0.3, x: 30, y: -13}, {scale: 1, x: 0, y: 0, duration: 0.9, ease: POP}, @t_in);
  tl.fromTo("#q14t", {scale: 0.5, autoAlpha: 0}, {scale: 1, autoAlpha: 1, duration: 0.55, ease: SP}, @t_in2);
  tl.fromTo("#q14l", {autoAlpha: 0, x: -12}, {autoAlpha: 1, x: 0, duration: 0.5, ease: SP}, @t_in3);
  // «багато навантаження» — it keeps climbing
  G.bump("#q14", @navant);
  // «безкоштовному» — and it costs nothing
  G.blurIn("#q14f", @t_f, 10, 0.3);
  tl.fromTo("#q14f", {scale: 0.5}, {scale: 1, duration: 0.7, ease: POP}, @t_f);
  G.bump("#q14f", @taryfi);
  // «Але» — it goes
  tl.to("#q14", {y: -40, scale: 0.94, duration: 0.3, ease: "power2.in"}, @ale2);
  G.blurOut("#q14", @t_out, 10, 0.3);
  tl.to("#g14", {autoAlpha: 0, duration: 0.02}, @t_off);''',
             t_in=61.280, t_in2=61.380, t_in3=61.500, t_f=T["bezkosht"] - 0.06,
             t_out=T["ale2"] + 0.04, t_off=T["ale2"] + 0.36)
    return html, src


# =================================================================== b15
k.css("""
/* ---- b15 · near: the inbox — client, bot, manager — then SendPulse ---- */
#w15, .w15s { left: 90px; top: 130px; width: 900px; height: 600px; border-radius: 64px; }
#w15hav { left: 34px; top: 28px; width: 76px; height: 76px; border-radius: 50%;
  background: linear-gradient(160deg, #ff8ab0 0%, #c4143a 60%, #7a0a20 100%);
  display: flex; align-items: center; justify-content: center; font-size: 36px; font-weight: 700;
  box-shadow: inset 0 2px 1px rgba(255,255,255,0.5); }
#w15hn { left: 130px; top: 26px; font-size: 36px; font-weight: 700; }
#w15hs { left: 130px; top: 72px; font-size: 24px; font-weight: 500; color: rgba(255,255,255,0.62); }
#w15mg { right: 30px; top: 32px; height: 68px; padding: 0 24px 0 8px; border-radius: 34px; display: flex;
  align-items: center; gap: 12px; font-size: 26px; font-weight: 700; background: rgba(255,255,255,0.12);
  box-shadow: inset 0 0 0 1.5px rgba(255,255,255,0.2); }
#w15mg i { width: 52px; height: 52px; border-radius: 50%; font-style: normal; display: flex; align-items: center;
  justify-content: center; background: linear-gradient(160deg, #ffffff 0%, #f3dde4 100%); color: #b4122f; font-size: 26px; }
#w15hr { left: 34px; right: 34px; top: 124px; height: 2px; background: rgba(255,255,255,0.16); }
.bb { position: absolute; max-width: 620px; padding: 20px 30px; border-radius: 34px; font-size: 32px; font-weight: 500;
  line-height: 42px; }
#m1 { left: 34px; top: 150px; background: rgba(255,255,255,0.93); color: #17141c; border-bottom-left-radius: 10px; }
.brow { position: absolute; right: 34px; display: flex; align-items: flex-end; gap: 14px; }
.brow .bb { position: relative; }
#m2r { top: 290px; } #m3r { top: 470px; }
#m2 { background: linear-gradient(160deg, #e0204b 0%, #8d0d24 100%); color: #fff; border-bottom-right-radius: 10px; }
#m3 { background: linear-gradient(160deg, #ff8ab0 0%, #e0204b 100%); color: #fff; border-bottom-right-radius: 10px; }
.bbadge { width: 60px; height: 60px; position: relative; flex: none; }
.bbadge.av { border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 28px;
  font-weight: 700; color: #b4122f; background: linear-gradient(160deg, #ffffff 0%, #f3dde4 100%); }
#qrs { right: 108px; top: 390px; display: flex; gap: 12px; }
.qr { height: 58px; padding: 0 24px; border-radius: 29px; font-size: 26px; font-weight: 700; display: flex;
  align-items: center; background: rgba(255,255,255,0.14); box-shadow: inset 0 0 0 2px rgba(255,255,255,0.4); }
#sp15 { left: 440px; top: 280px; width: 200px; height: 200px; }
#sp15l { top: 500px; }
.spl { height: 64px; padding: 0 28px; border-radius: 32px; font-size: 34px; font-weight: 700; display: inline-flex;
  align-items: center; }
""")


@beat
def b15_inbox_sendpulse():
    """«Але якщо нам кров з носа треба, щоб менеджери могли спілкуватись з
    клієнтами через чатботи і бачити переписки, то тоді кандидат це
    Sendpulse,»

    A glass chat window above her head on «треба»: Марія (the same client)
    and her manager Оля in the header on «менеджери». Марія writes on
    «спілкуватись з клієнтами»; the bot answers with two time slots on
    «чатботи»; the manager steps in on «бачити», and two more threads stack
    behind on «переписки». On «кандидат» the window steps back; on
    «Sendpulse» the SendPulse tile lands on it with its name under it —
    blackout for that word, plaque kept."""
    stack = "".join('<div class="dchip edge abs w15s hide" id="w15s%d"></div>' % i for i in (2, 1))
    html = fill(u'''
      <div class="g full" id="g15">
        {{stack}}
        <div id="w15" class="dglass edge abs hide">
          <div class="cx" id="w15hav">М</div>
          <div class="cx" id="w15hn">Марія Коваль</div>
          <div class="cx" id="w15hs">клієнтка · онлайн</div>
          <div class="cx" id="w15mg"><i>О</i>Оля · менеджерка</div>
          <div class="cx" id="w15hr"></div>
          <div class="bb" id="m1">Добрий день! Є вільні дати<br>на зйомку?</div>
          <div class="brow" id="m2r"><div class="bbadge"><div class="jelly">{{bot}}</div></div><div class="bb" id="m2">Так! Оберіть зручний час:</div></div>
          <div class="cx" id="qrs" data-layout-allow-overlap><div class="qr" data-layout-allow-overlap>Пн 10:00</div><div class="qr" data-layout-allow-overlap>Ср 14:00</div></div>
          <div class="brow" id="m3r"><div class="bbadge av">О</div><div class="bb" id="m3">Марія, бронюю вам середу</div></div>
        </div>
        <div id="sp15" class="abs hide"><div class="pearl">{{sp}}<div class="sheen"></div></div></div>
        <div class="sqring hide" id="sp15r" style="left:440px;top:280px;width:200px;height:200px"></div>
        <div class="ctr hide" id="sp15l" data-layout-allow-overlap><div class="dchip edge spl" data-layout-allow-overlap>SendPulse</div></div>
      </div>''', stack=stack, bot=sym("bot"), sp=sym("sendpulse"))
    src = js('''
  tl.set("#g15", {autoAlpha: 1}, @treba6);
  gsap.set(["#w15hav", "#w15hn", "#w15hs", "#w15mg", "#m1", "#m2r", ".qr", "#m3r"], {autoAlpha: 0});
  G.arrive("#w15", @treba6, {s: 0.7, y: 40});
  // «менеджери» — who is talking to whom
  tl.fromTo("#w15hav", {scale: 0.5, autoAlpha: 0}, {scale: 1, autoAlpha: 1, duration: 0.55, ease: POP}, @menedzh);
  G.blurIn(["#w15hn", "#w15hs"], @t_h2, 10, 0.3);
  G.blurIn("#w15mg", @t_h3, 10, 0.3);
  tl.fromTo("#w15mg", {x: 30}, {x: 0, duration: 0.6, ease: SP}, @t_h3);
  // «спілкуватись з клієнтами» — Марія writes
  G.blurIn("#m1", @spilkuv, 10, 0.3);
  tl.fromTo("#m1", {y: 30, scale: 0.9, transformOrigin: "0% 100%"}, {y: 0, scale: 1, duration: 0.7, ease: POP}, @spilkuv);
  // «через чатботи» — the bot answers
  G.blurIn("#m2r", @t_bot, 10, 0.3);
  tl.fromTo("#m2r", {y: 30, scale: 0.9, transformOrigin: "100% 100%"}, {y: 0, scale: 1, duration: 0.7, ease: POP}, @t_bot);
  tl.fromTo(".qr", {autoAlpha: 0, y: 12}, {autoAlpha: 1, y: 0, duration: 0.5, ease: SP, stagger: 0.1}, @t_qr);
  // «бачити» — the manager steps in
  G.blurIn("#m3r", @bachyty, 10, 0.3);
  tl.fromTo("#m3r", {y: 30, scale: 0.9, transformOrigin: "100% 100%"}, {y: 0, scale: 1, duration: 0.7, ease: POP}, @bachyty);
  // «переписки» — and there are more threads behind this one
  tl.fromTo("#w15s1", {autoAlpha: 0, y: 0, scale: 1}, {autoAlpha: 0.75, y: -46, scale: 0.94, duration: 0.6, ease: SP}, @perepysky);
  tl.fromTo("#w15s2", {autoAlpha: 0, y: 0, scale: 1}, {autoAlpha: 0.5, y: -90, scale: 0.88, duration: 0.6, ease: SP}, @t_s2);
  // «кандидат» — the inbox steps back for its owner
  tl.to(["#w15", "#w15s1", "#w15s2"], {scale: "-=0.06", autoAlpha: 0.4, duration: 0.5, ease: "power2.out"}, @kandydat);
  // «Sendpulse»
  G.arrive("#sp15", @t_sp, {s: 0.4, y: 40});
  tl.fromTo("#sp15 .mk", {scale: 0.55, autoAlpha: 0}, {scale: 1, autoAlpha: 1, duration: 0.55, ease: SP}, @sp1);
  G.ripple("#sp15r", @t_spr);
  G.sheen("#sp15 .sheen", @t_spsh);
  G.blurIn("#sp15l", @t_spl, 10, 0.3);
  tl.fromTo("#sp15l", {y: -20}, {y: 0, duration: 0.6, ease: SP}, @t_spl);
  // «де» — the inbox folds into SendPulse
  tl.to(["#w15", "#w15s1", "#w15s2"], {scale: 0.25, autoAlpha: 0, duration: 0.4, ease: "power3.in"}, @t_fold);
  tl.set(["#sp15", "#sp15l"], {autoAlpha: 0}, @t_hand);
  tl.to("#g15", {autoAlpha: 0, duration: 0.02}, @t_off);''',
             t_h2=T["menedzh"] + 0.12, t_h3=T["menedzh"] + 0.30, t_bot=T["chatboty"] - 0.08,
             t_qr=T["chatboty"] + 0.36, t_s2=T["perepysky"] + 0.18,
             t_sp=T["sp1"] - 0.10, t_spr=T["sp1"] + 0.10, t_spsh=T["sp1"] + 0.3, t_spl=T["sp1"] + 0.06,
             t_fold=T["de"] - 0.10, t_hand=T["de"] - 0.02, t_off=T["de"] + 0.32)
    return html, src


# =================================================================== b16
HUB16 = (540, 380)
HERO16 = [("tg", "telegram", (170, 700)), ("wa", "whatsapp", (910, 700)),
          ("ig", "instagram", (285, 1010))]
GMAIL16 = (795, 1010)
PITCH16 = 124
_cells16 = [(HUB16[0] + i * PITCH16, HUB16[1] + j * PITCH16) for j in range(-2, 7) for i in range(-4, 5)]
_skip16 = [c for _, _, c in HERO16] + [GMAIL16]
FILL16 = [n for n in available() if n not in
          ("telegram", "whatsapp", "instagram", "gmail", "claude", "openai", "anthropic", "notion", "threads")]
wall16 = []
for (x, y) in _cells16:
    d = math.hypot(x - HUB16[0], y - HUB16[1])
    if d < 170 or any(math.hypot(x - a, y - b) < 110 for a, b in _skip16):
        continue
    if 380 <= x <= 700 and 470 <= y <= 580:          # the «SendPulse» label
        continue
    i, j = (x - HUB16[0]) // PITCH16 + 4, (y - HUB16[1]) // PITCH16 + 2
    wall16.append({"x": x, "y": y, "d": round(d, 1), "o": round(max(0.38, 1 - d / 1500.0), 3),
                   "g": FILL16[(i * 7 + j * 5 + i * j) % len(FILL16)]})
MAXD16 = max(t["d"] for t in wall16)


def wire16(p):
    x0, y0 = p
    x1, y1 = HUB16
    side = -1 if x0 < 540 else 1
    cx, cy = (x0 + x1) / 2 + side * 120, (y0 + y1) / 2 + 40
    return "M %d %d Q %d %d %d %d" % (x0, y0, cx, cy, x1, y1 + 70)


k.css("""
/* ---- b16 · behind her: SendPulse plugs into everything ---- */
#tint16 { position: absolute; inset: 0;
  background: linear-gradient(180deg, rgba(74,10,28,0.46) 0%, rgba(40,5,15,0.58) 100%); }
#wr16 { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; overflow: visible; }
#wr16 .w { fill: none; stroke: rgba(255,255,255,0.55); stroke-width: 5; stroke-linecap: round; }
#wr16 .p { fill: none; stroke: #fff; stroke-width: 10; stroke-linecap: round; }
#wr16 .pk { filter: drop-shadow(0 0 8px rgba(255,150,185,0.95)); }
#wall16 { position: absolute; inset: 0; transform-origin: 540px 380px; }
.src16 { position: absolute; width: 168px; height: 168px; margin: -84px 0 0 -84px; }
.wt { position: absolute; width: 100px; height: 100px; margin: -50px 0 0 -50px; border-radius: 23px;
  background: linear-gradient(158deg, rgba(255,255,255,0.30) 0%, rgba(255,255,255,0.09) 52%, rgba(255,255,255,0.15) 100%);
  box-shadow: inset 0 1.5px 1px rgba(255,255,255,0.65), inset 0 -10px 18px -10px rgba(255,255,255,0.36),
              inset 0 0 0 1px rgba(255,255,255,0.10), 0 16px 30px -14px rgba(24,4,12,0.45);
  display: flex; align-items: center; justify-content: center; }
.wt svg { width: 46px; height: 46px; fill: #fff; opacity: 0.92; }
#h16 { left: 440px; top: 280px; width: 200px; height: 200px; }
.h16r { left: 440px; top: 280px; width: 200px; height: 200px; }
#h16l { top: 500px; }
""")


@beat
def b16_integrations_behind():
    """«де CRM як миленька інтегрується з чатботами, і ще мільйоном різних
    штук типу імейлів.»

    Behind her (matte `orbit`): the inbox folded into SendPulse, which stays
    the hub above her head while the room behind her takes a burgundy tint.
    Telegram, WhatsApp and Instagram plug in from behind her shoulders on
    «інтегрується з чатботами»; on «мільйоном різних штук» a wall of tiles
    ripples out of the hub behind her — reel 12's wall, smaller; Gmail steps
    forward on «імейлів». Then it all folds back into the hub. (What she says
    after «імейлів» is not in the script and whisper made no sense of it —
    those 0.5 s carry the previous caption.)"""
    wall_html = "\n        ".join(
        '<div class="wt hide" id="wt%d" style="left:%dpx;top:%dpx">%s</div>'
        % (i, t["x"], t["y"], g.mark(t["g"], "")) for i, t in enumerate(wall16))
    heroes = "\n        ".join(
        '<div class="src16 hide" id="h16-%s" style="left:%dpx;top:%dpx"><div class="clear edge">%s</div></div>'
        % (key, c[0], c[1], g.mark(ic)) for key, ic, c in HERO16 + [("gm", "gmail", GMAIL16)])
    wires = "\n          ".join(
        '<path class="w" id="w16-%s" d="%s"/><g class="pk"><path class="p hide" id="p16-%s" d="%s"/></g>'
        % (key, wire16(c), key, wire16(c)) for key, _, c in HERO16)
    rips = "".join('<div class="sqring h16r hide" id="h16r%d"></div>' % i for i in range(4))
    html = fill(u'''
      <div class="g full" id="g16">
        <div id="tint16" class="hide"></div>
        <svg id="wr16" viewBox="0 0 1080 1920">
          {{wires}}
        </svg>
        <div id="wall16">
        {{wall}}
        </div>
        {{heroes}}
        {{rips}}
        <div id="h16" class="abs"><div class="pearl">{{sp}}</div></div>
        <div class="ctr" id="h16l" data-layout-allow-overlap><div class="dchip edge spl" data-layout-allow-overlap>SendPulse</div></div>
      </div>''', wires=wires, wall=wall_html, heroes=heroes, rips=rips, sp=sym("sendpulse"))
    cfg = {"hub": HUB16, "maxd": MAXD16,
           "wall": [{"x": t["x"], "y": t["y"], "d": t["d"], "o": t["o"]} for t in wall16],
           "hero": [{"k": key, "x": c[0], "y": c[1]} for key, _, c in HERO16 + [("gm", "", GMAIL16)]]}
    src = js('''
  var C16 = CFG16;
  tl.set("#g16", {autoAlpha: 1}, @t_in);
  gsap.set(["#p16-tg", "#p16-wa", "#p16-ig"], {autoAlpha: 0});
  // the room behind her goes burgundy while she is matted on top of it
  tl.fromTo("#tint16", {autoAlpha: 0}, {autoAlpha: 1, duration: 0.6, ease: "power1.inOut"}, @de);
  // «інтегрується з чатботами» — three chat channels plug in from behind her
  function plug(k, i, t) {
    var s = "#h16-" + k;
    G.blurIn(s, t, 12, 0.36);
    tl.fromTo(s, {scale: 0.5, y: 40}, {scale: 1, y: 0, duration: 0.8, ease: POP}, t);
    tl.fromTo(s + " .mk", {scale: 0.55, autoAlpha: 0}, {scale: 1, autoAlpha: 1, duration: 0.55, ease: SP}, t + 0.1);
    G.drawPrep("w16-" + k);
    tl.to("#w16-" + k, {strokeDashoffset: 0, duration: 0.45, ease: "power2.inOut"}, t + 0.14);
    G.packet("p16-" + k, t + 0.4, 0.45);
    G.bump("#h16", t + 0.84);
    G.ripple("#h16r" + i, t + 0.86);
  }
PLUGS
  // «мільйоном різних штук» — the wall ripples out of the hub, behind her
  var tM = @t_m;
  tl.to("#wr16", {autoAlpha: 0, duration: 0.3, ease: "power1.in"}, @t_m);
  C16.wall.forEach(function (w, n) {
    var t = tM + w.d * 0.00045;
    tl.fromTo("#wt" + n, {autoAlpha: 0, scale: 0.3}, {autoAlpha: w.o, duration: 0.3, ease: "power2.out"}, t);
    tl.to("#wt" + n, {scale: 1, duration: 0.6, ease: SP}, t);
  });
  tl.fromTo("#wall16", {scale: 1.1}, {scale: 1, duration: 1.5, ease: "power2.out"}, @t_m);
  // «типу імейлів» — email is one of them
  G.blurIn("#h16-gm", @t_gm, 12, 0.36);
  tl.fromTo("#h16-gm", {scale: 0.5, y: 40}, {scale: 1.12, y: 0, duration: 0.8, ease: POP}, @t_gm);
  G.ripple("#h16r3", @imeyliv);
  G.blurOut("#h16l", @imeyliv, 10, 0.3);
  // everything folds back into the hub
  var tC = @t_c;
  C16.wall.forEach(function (w, n) {
    tl.to("#wt" + n, {x: (C16.hub[0] - w.x) * 0.4, y: (C16.hub[1] - w.y) * 0.4, scale: 0, autoAlpha: 0,
                      duration: 0.4, ease: "power2.in"}, tC + (C16.maxd - w.d) * 0.0002);
  });
  C16.hero.forEach(function (h) {
    tl.to("#h16-" + h.k, {x: (C16.hub[0] - h.x) * 0.4, y: (C16.hub[1] - h.y) * 0.4, scale: 0, autoAlpha: 0,
                          duration: 0.4, ease: "power2.in"}, tC);
  });
  G.bump("#h16", @t_c2);
  tl.to("#tint16", {autoAlpha: 0, duration: 0.4, ease: "power1.inOut"}, @t_c3);
  tl.to("#g16", {autoAlpha: 0, duration: 0.02}, @t_off);'''.replace("CFG16", json.dumps(cfg)),
             t_in=T["de"] - 0.02, t_m=T["milyon"] - 0.04, t_gm=T["typu"] - 0.06,
             t_c=78.300, t_c2=78.620, t_c3=78.520, t_off=79.000)
    plugs = "\n".join('  plug("%s", %d, %.3f);' % (key, i, t) for i, (key, t) in enumerate(
        [("tg", T["integr"] - 0.08), ("wa", T["integr"] + 0.24), ("ig", T["zchat"] - 0.02)]))
    return html, src.replace("PLUGS", plugs)


# =================================================================== b17
k.css("""
/* ---- b17 · near: not Notion, not SendPulse ---- */
#s17 { left: 70px; top: 250px; width: 940px; height: 300px; overflow: hidden; }
#nt17 { left: 235px; top: 305px; width: 190px; height: 190px; }
#sp17 { left: 655px; top: 305px; width: 190px; height: 190px; }
""")


@beat
def b17_flick_off():
    """«Але я маю сказати чесно, що в мене не Notion і не Sendpulse»

    SendPulse drops from the hub onto a glass shelf; Notion comes back beside
    it on «маю сказати». On «не Notion» Notion is flicked off the shelf; on
    «не Sendpulse» so is SendPulse. The shelf is left empty for the thing
    that is hers."""
    html = fill(u'''
      <div class="g full" id="g17">
        <div id="s17" class="shelf edge abs hide"><div class="sheen"></div></div>
        <div id="nt17" class="abs hide"><div class="pearl">{{notion}}</div></div>
        <div id="sp17" class="abs"><div class="pearl">{{sp}}</div></div>
      </div>''', notion=g.mark("notion"), sp=sym("sendpulse"))
    src = js('''
  tl.set("#g17", {autoAlpha: 1}, @t_in);
  G.blurIn("#s17", @t_in, 14, 0.4);
  tl.fromTo("#s17", {scaleX: 0.7, scaleY: 0.6}, {scaleX: 1, scaleY: 1, duration: 0.9, ease: SP}, @t_in);
  // SendPulse, from the hub (540, 380) to its seat on the shelf
  tl.fromTo("#sp17", {x: -210, y: -20, scale: 1.05}, {x: 0, y: 0, scale: 1, duration: 0.85, ease: SP, immediateRender: true}, @t_in);
  // «маю сказати» — Notion is back beside it
  G.arrive("#nt17", @mayu, {s: 0.5, y: 30});
  // «чесно»
  G.bump("#nt17", @chesno);
  G.bump("#sp17", @t_ch2);
  G.sheen("#s17 .sheen", @chesno);
  // «не Notion» — flicked off the shelf
  tl.to("#nt17", {x: -440, y: 150, rotation: -38, duration: 0.55, ease: "power2.in"}, @t_n);
  G.blurOut("#nt17", @t_n2, 12, 0.3);
  // «не Sendpulse»
  tl.to("#sp17", {x: 440, y: 150, rotation: 38, duration: 0.55, ease: "power2.in"}, @t_s);
  G.blurOut("#sp17", @t_s2, 12, 0.3);
  // the empty shelf is where her own CRM opens
  tl.to("#s17", {scaleX: 0.9, scaleY: 1.2, duration: 0.35, ease: "power2.in"}, @t_x);
  G.blurOut("#s17", @t_x2, 12, 0.3);
  tl.to("#g17", {autoAlpha: 0, duration: 0.02}, @t_off);''',
             t_in=79.000, t_ch2=T["chesno"] + 0.1, t_n=T["notion2"] - 0.06, t_n2=T["notion2"] + 0.14,
             t_s=T["sp2"] - 0.04, t_s2=T["sp2"] + 0.16, t_x=82.880, t_x2=83.000, t_off=83.340)
    return html, src


# =================================================================== b18
TABS = ["Today", "Pipeline", "P&amp;L", "Quote", "Money", "Insights", "People"]
k.css("""
/* ---- b18 · over her: Floor, her own CRM, in a glass phone ----
   Recreated from work/media/r15/floor-notes.md. Her rule: every amount, name
   and handle blurred, the Quote tab readable. The blur is a text-shadow on
   transparent text (.bz) — it reads as blur(7px) and costs nothing against
   the heavy-element budget, which a filter per value would blow. The values
   under it are placeholders, not her data. */
#tk18 { position: absolute; inset: 0; clip-path: circle(0px at 540px 400px); }
#phW { left: 240px; top: 70px; width: 600px; height: 1170px; transform-origin: 300px 330px; }
#phF { position: absolute; inset: 0; border-radius: 92px;
  background: linear-gradient(160deg, rgba(70,24,38,0.92) 0%, rgba(22,8,13,0.94) 100%);
  box-shadow: inset 0 2px 1px rgba(255,255,255,0.35), inset 0 0 0 2px rgba(255,255,255,0.10),
              0 80px 140px -40px rgba(8,0,3,0.85), 0 0 0 1px rgba(255,255,255,0.18); }
#phS { position: absolute; left: 16px; top: 16px; width: 568px; height: 1138px; border-radius: 76px;
  overflow: hidden; background: #f7f5f2; color: #17141c; }
#phIsl { left: 209px; top: 16px; width: 150px; height: 42px; border-radius: 21px; background: #0b0709; }
#phTime { left: 52px; top: 20px; font-size: 24px; font-weight: 700; }
#phBat { right: 48px; top: 24px; width: 44px; height: 22px; border-radius: 7px; box-shadow: inset 0 0 0 2.5px #17141c; }
#phBat i { position: absolute; left: 4px; top: 4px; width: 30px; height: 14px; border-radius: 4px; background: #17141c; display: block; }
#flWm { left: 28px; top: 74px; font-size: 44px; font-weight: 900; letter-spacing: -0.035em; }
#flAv { right: 28px; top: 76px; width: 50px; height: 50px; border-radius: 50%; background: #e4ded8; }
#flTabs { left: 20px; top: 146px; display: flex; gap: 8px; white-space: nowrap; }
.tb { position: relative; height: 54px; padding: 0 22px; border-radius: 27px; font-size: 22px; font-weight: 700;
  display: flex; align-items: center; background: rgba(23,20,28,0.05); color: rgba(23,20,28,0.62); }
.tb i { position: absolute; inset: 0; border-radius: 27px; background: #17141c; display: block; opacity: 0; }
.tb span { position: relative; }
.scr { position: absolute; left: 20px; top: 222px; width: 528px; height: 916px; }
.kc { position: absolute; left: 0; width: 528px; border-radius: 24px; background: #fff;
  box-shadow: 0 0 0 1px rgba(0,0,0,0.06), 0 1px 2px rgba(0,0,0,0.04), 0 10px 22px rgba(0,0,0,0.05); }
.kc .mi { position: absolute; left: 26px; font-size: 17px; font-weight: 700; letter-spacing: 0.12em; color: rgba(23,20,28,0.46); }
.kc .ti { position: absolute; left: 26px; font-size: 24px; font-weight: 700; }
.kc .nu { position: absolute; left: 26px; font-size: 58px; font-weight: 900; letter-spacing: -0.03em; line-height: 64px; }
.kc .ds { position: absolute; left: 26px; right: 26px; font-size: 19px; font-weight: 500; line-height: 26px; color: rgba(23,20,28,0.56); }
.peach { background: #fbeee4; box-shadow: 0 0 0 1px rgba(192,86,27,0.10); }
.mint { background: #e6f4ec; box-shadow: 0 0 0 1px rgba(27,122,74,0.10); }
.bz { color: transparent !important; --bc: rgba(23,20,28,0.9);
  text-shadow: 0 0 max(20px, 0.8em) var(--bc), 0 0 max(20px, 0.8em) var(--bc), 0 0 max(12px, 0.45em) var(--bc); }
.bz.gr { --bc: rgba(27,122,74,0.95); } .bz.or { --bc: rgba(192,86,27,0.95); } .bz.pu { --bc: rgba(91,69,214,0.95); }
#kb { position: absolute; left: 0; top: 520px; display: flex; gap: 14px; }
.col { position: relative; width: 300px; flex: none; }
.col .hd { display: flex; align-items: center; gap: 10px; font-size: 24px; font-weight: 700; }
.col .hd i { width: 12px; height: 12px; border-radius: 50%; display: block; }
.col .hd b { font-size: 18px; font-weight: 700; padding: 3px 10px; border-radius: 12px; background: rgba(23,20,28,0.06); }
.col .cd { margin-top: 8px; font-size: 18px; line-height: 24px; color: rgba(23,20,28,0.52); height: 50px; }
.dl { position: relative; margin-top: 14px; border-radius: 20px; background: #fff; padding: 18px 20px; height: 176px;
  box-shadow: 0 0 0 1px rgba(0,0,0,0.06), 0 8px 18px rgba(0,0,0,0.05); }
.dl .dn { font-size: 22px; font-weight: 700; } .dl .dh { font-size: 18px; margin-top: 4px; }
.dl .chs { display: flex; gap: 6px; margin-top: 12px; }
.dl .chs span { font-size: 16px; font-weight: 700; padding: 5px 11px; border-radius: 12px; background: rgba(23,20,28,0.06); color: rgba(23,20,28,0.6); }
.dl .ft { display: flex; justify-content: space-between; margin-top: 14px; font-size: 17px; font-weight: 700; }
.dl .ft .ym { color: #c0561b; } .dl .ft .wt2 { color: rgba(23,20,28,0.45); }
.plr { position: absolute; left: 26px; right: 26px; height: 52px; display: flex; justify-content: space-between;
  align-items: center; font-size: 21px; font-weight: 500; border-bottom: 1px solid rgba(27,122,74,0.14); }
.plr b { font-weight: 700; }
.pill { position: absolute; font-size: 16px; font-weight: 700; padding: 6px 14px; border-radius: 14px; }
.nb { position: absolute; left: 26px; top: 24px; width: 40px; height: 40px; border-radius: 50%; background: #17141c;
  color: #fff; font-size: 20px; font-weight: 700; display: flex; align-items: center; justify-content: center; }
.h1 { position: absolute; left: 0; font-size: 34px; font-weight: 900; letter-spacing: -0.02em; line-height: 40px; }
.sub { position: absolute; left: 0; right: 0; font-size: 20px; line-height: 28px; color: rgba(23,20,28,0.56); }
.mic { position: absolute; left: 0; font-size: 17px; font-weight: 700; letter-spacing: 0.12em; color: rgba(23,20,28,0.46); }
#qChips { position: absolute; left: 0; top: 172px; width: 528px; display: flex; flex-wrap: wrap; gap: 10px; }
#qChips span { font-size: 21px; font-weight: 700; padding: 0 18px; height: 48px; border-radius: 24px; display: flex;
  align-items: center; box-shadow: inset 0 0 0 1.5px rgba(23,20,28,0.12); color: rgba(23,20,28,0.7); }
#qChips span.on { background: #17141c; color: #fff; box-shadow: none; }
.val { position: absolute; right: 0; font-size: 30px; font-weight: 900; letter-spacing: -0.02em; }
.trk { position: absolute; left: 0; width: 528px; height: 12px; border-radius: 6px; background: rgba(23,20,28,0.08); }
.trk .fl { position: absolute; left: 0; top: 0; width: 528px; height: 12px; border-radius: 6px; background: #5b45d6;
  transform-origin: 0% 50%; }
.trk .th { position: absolute; left: 0; top: -12px; width: 36px; height: 36px; border-radius: 50%; background: #fff;
  box-shadow: inset 0 0 0 4px #5b45d6, 0 4px 10px rgba(0,0,0,0.18); }
#qRes { position: absolute; left: 0; top: 560px; width: 528px; height: 350px; border-radius: 24px; background: #fbeee4;
  box-shadow: 0 0 0 1px rgba(192,86,27,0.12); overflow: hidden; }
#qRes .sheen { mix-blend-mode: normal; opacity: 0.6; }
#qRate { position: absolute; left: 26px; top: 50px; font-size: 76px; font-weight: 900; letter-spacing: -0.035em; color: #c0561b; }
#qNote { position: absolute; left: 26px; right: 26px; top: 140px; font-size: 19px; line-height: 26px; color: rgba(23,20,28,0.7); }
#qSend { position: absolute; left: 18px; right: 18px; top: 204px; height: 130px; border-radius: 18px; background: #fff;
  box-shadow: 0 0 0 1px rgba(0,0,0,0.05); }
#qSendV { position: absolute; left: 20px; top: 38px; font-size: 32px; font-weight: 900; letter-spacing: -0.02em; }
#qSendD { position: absolute; left: 20px; right: 20px; top: 82px; font-size: 15px; line-height: 20px; color: rgba(23,20,28,0.52); }
#phAI { left: 792px; top: 38px; width: 150px; height: 150px; }
#phAIg { left: 617px; top: -137px; width: 500px; height: 500px;
  background: radial-gradient(circle, rgba(255,110,156,0.55) 0%, rgba(255,110,156,0) 62%); }
""")

PIPE = u'''
<div class="scr" id="scP">
  <div class="kc" style="top:0;height:150px"><div class="mi" style="top:22px">LIVE DEALS</div>
    <div class="nu bz" style="top:48px">12</div>
    <div class="ds" style="top:112px">Worth <span class="bz">€18 400</span> where a price is set.</div></div>
  <div class="kc peach" style="top:166px;height:150px"><div class="ti" style="top:20px">Waiting on you</div>
    <div class="nu bz or" style="top:50px;color:#c0561b">5</div>
    <div class="ds" style="top:114px">These do not move until you move them.</div></div>
  <div class="kc" style="top:332px;height:150px"><div class="ti" style="top:20px">Waiting on them</div>
    <div class="nu bz" style="top:50px">7</div>
    <div class="ds" style="top:114px">Nudging beats patience once they go quiet.</div></div>
  <div id="kb">
    <div class="col" id="kc0"><div class="hd"><i style="background:#c0561b"></i>Lead<b class="bz">3</b></div>
      <div class="cd">They landed. You have not replied properly yet.</div>
      <div class="dl"><div class="dn bz">Олена — запуск курсу</div><div class="dh bz">@olena.k</div>
        <div class="chs"><span>no price</span><span>Tech setup</span></div>
        <div class="ft"><span class="ym">● Your move</span><span class="wt2"><span class="bz">2</span> days</span></div></div></div>
    <div class="col" id="kc1"><div class="hd"><i style="background:#5b45d6"></i>Talking<b class="bz">4</b></div>
      <div class="cd">Conversation is live. Keep it moving.</div>
      <div class="dl"><div class="dn bz">Макс — редизайн сайту</div><div class="dh bz">@max.studio</div>
        <div class="chs"><span>no price</span><span>Strategy session</span></div>
        <div class="ft"><span class="wt2">● Waiting on them</span><span class="wt2"><span class="bz">4</span> days</span></div></div></div>
    <div class="col" id="kc2"><div class="hd"><i style="background:#1b7a4a"></i>Call scheduled<b class="bz">2</b></div>
      <div class="cd">Booked. Waiting on the date.</div></div>
  </div>
</div>'''

PNL_ROWS = [("Money in", u"€4 860", " gr"), ("Tax (6%)", u"€292", ""), (u"ЄСВ", u"€40", ""),
            ("Rent and food", u"€1 350", ""), ("Travel set-aside", u"€400", ""),
            ("Business subscriptions", u"€180", "")]
PNL = u'''
<div class="scr" id="scL">
  <div class="kc mint" style="top:0;height:900px">
    <div class="ti" style="top:24px;font-size:30px">September 2026</div>
    <div class="pill" style="right:26px;top:28px;background:rgba(255,255,255,0.7);color:#1b7a4a">still running</div>
    <div class="ds" style="top:74px">Everything that came in, everything that has to go out, and what is left. In that order.</div>
    {{rows}}
    <div class="kc" style="left:18px;width:492px;top:560px;height:300px">
      <div class="ti" style="top:26px">Left for you</div>
      <div class="nu bz gr" style="top:72px;font-size:80px;line-height:88px;color:#1b7a4a">€2 140</div>
      <div class="ds" style="top:186px">After everything. This month is not finished yet, so this will still move.</div>
    </div>
  </div>
</div>'''.replace("{{rows}}", "".join(
    u'<div class="plr" style="top:%dpx"><span>%s</span><b class="bz%s">%s</b></div>'
    % (164 + i * 62, lab, cls, v.replace(" ", "&nbsp;")) for i, (lab, v, cls) in enumerate(PNL_ROWS)))

MONEY = u'''
<div class="scr" id="scM">
  <div class="h1" style="top:0">Where the money actually goes</div>
  <div class="sub" style="top:88px">Same money, three different words. This month’s real numbers.</div>
  {{cards}}
  <div class="ti" style="position:absolute;left:0;top:880px;font-size:24px;font-weight:700">The month where you keep nothing</div>
</div>'''.replace("{{cards}}", "".join(
    u'<div class="kc" style="top:%dpx;height:214px"><div class="nb">%d</div>'
    u'<div class="ti" style="left:82px;top:28px">%s</div>'
    u'<div class="nu bz%s" style="top:84px;color:%s">%s</div>'
    u'<div class="ds" style="top:160px">%s</div></div>'
    % (170 + i * 232, i + 1, t, cls, col, v.replace(" ", "&nbsp;"), d)
    for i, (t, cls, col, v, d) in enumerate([
        ("Came in", "", "#17141c", u"€4 860", "Everything clients paid this month."),
        ("Left after costs", " pu", "#5b45d6", u"€3 910", u"…went to tax at 6%. What survives is profit."),
        ("Left for you", " gr", "#1b7a4a", u"€2 140", "After rent, food and the set-asides.")])))

QUOTE = u'''
<div class="scr" id="scQ">
  <div class="h1" style="top:0">What should I charge</div>
  <div class="sub" style="top:50px">Drag until it feels right. Nothing is saved — this is for thinking.</div>
  <div class="mic" style="top:138px">KIND OF WORK</div>
  <div id="qChips"><span class="on">Strategy session</span><span>Tech setup</span><span>Content &amp; storytelling</span><span>Producing</span></div>
  <div class="mic" style="top:318px">PRICE</div><div class="val" id="qP" style="top:306px">€200</div>
  <div class="trk" style="top:368px"><div class="fl" id="qPf"></div><div class="th" id="qPt"></div></div>
  <div class="mic" style="top:420px">HOURS YOU THINK IT WILL TAKE</div><div class="val" id="qH" style="top:408px">3 h</div>
  <div class="trk" style="top:470px"><div class="fl" id="qHf"></div><div class="th" id="qHt"></div></div>
  <div id="qRes">
    <div class="ti" style="position:absolute;left:26px;top:22px;font-size:22px;font-weight:700">That works out at</div>
    <div id="qRate">€67/h</div>
    <div id="qNote">Below your usual €60/h, but not badly. Fine if you want the client.</div>
    <div id="qSend"><div class="mic" style="left:20px;top:14px">SEND IT LIKE THIS</div>
      <div id="qSendV">€200 (10&nbsp;200 ₴)</div>
      <div id="qSendD">Rounded down to the nearest 100 UAH at 51 UAH/€, the way you always do. This number is frozen once you send it.</div></div>
    <div class="sheen"></div>
  </div>
</div>'''


@beat
def b18_floor():
    """«я навайбкодила сама собі простеньку agentic CRM з розширеним
    фінансовим дашбордом буквально за кілька годин, і успішно нею
    користуюсь. Все тому що я займаюсь продажами і переписками самостійно,»

    The payoff. The empty shelf opens (iris) onto burgundy and a glass phone
    grows out of it: **Floor**, her own CRM, recreated from
    work/media/r15/floor-notes.md. Pipeline first — three KPI cards, the
    kanban with deal cards — every figure, name and handle blurred. Claude
    docks on the phone's corner on «agentic». P&L on «розширеним», Money on
    «дашбордом» (all amounts blurred), Quote on «кілька годин» — readable, as
    she allowed: on «успішно» the price slider runs to €400, on «користуюсь»
    the hours to 8 h and the rate settles at €50/h; on «продажами» the
    camera pushes in on it. The iris closes into Claude on «використовую»."""
    tabs = "".join('<div class="tb" id="tb%d"><i></i><span>%s</span></div>' % (i, t) for i, t in enumerate(TABS))
    html = fill(u'''
      <div class="g full" id="g18">
        <div id="tk18">
          <div class="tkg"></div>
          <div class="aurs"></div>
          <div class="grain"></div>
          <div id="phW" class="abs hide" data-layout-allow-overflow>
            <div id="phF" class="edge"></div>
            <div id="phS">
              <div class="cx" id="phIsl"></div><div class="cx" id="phTime">9:41</div><div class="cx" id="phBat"><i></i></div>
              <div class="cx" id="flWm">Floor</div><div class="cx" id="flAv"></div>
              <div class="cx" id="flTabs">{{tabs}}</div>
              {{pipe}}{{pnl}}{{money}}{{quote}}
            </div>
          </div>
        </div>
        <div id="phAIg" class="abs hide"></div>
        <div id="phAI" class="abs hide"><div class="jelly">{{claude}}<div class="sheen"></div></div></div>
      </div>''', tabs=tabs, pipe=PIPE, pnl=PNL, money=MONEY, quote=QUOTE, claude=g.mark("claude"))
    src = js('''
  tl.set("#g18", {autoAlpha: 1}, @t_in);
  gsap.set(["#scL", "#scM", "#scQ", "#qNote"], {autoAlpha: 0});
  gsap.set("#tb1 i", {opacity: 1}); gsap.set("#tb1", {color: "#ffffff"});
  // the Quote sliders start at €200 / 3 h
  gsap.set("#qPf", {scaleX: 0.2}); gsap.set("#qPt", {x: 0.2 * 492});
  gsap.set("#qHf", {scaleX: 2 / 19}); gsap.set("#qHt", {x: 2 / 19 * 492});
  // «навайбкодила» — the empty shelf opens onto burgundy; the phone grows out of it
  G.irisOpen("#tk18", @t_in, 540, 400, 0.85);
  drift1("#tk18", @t_in, 11.6);
  G.blurIn("#phW", @t_ph, 16, 0.45);
  tl.fromTo("#phW", {scale: 0.3}, {scale: 1, duration: 1.05, ease: spring(0.72, 12)}, @t_ph);
  tl.fromTo(["#flWm", "#flAv", "#flTabs"], {autoAlpha: 0, y: 12}, {autoAlpha: 1, y: 0, duration: 0.5, ease: SP, stagger: 0.07}, @t_top);
  tl.fromTo("#scP .kc", {autoAlpha: 0, y: 24}, {autoAlpha: 1, y: 0, duration: 0.55, ease: SP, stagger: 0.1}, @t_kpi);
  // «простеньку» — the pipeline
  tl.fromTo("#scP .col", {autoAlpha: 0, x: 70}, {autoAlpha: 1, x: 0, duration: 0.6, ease: SP, stagger: 0.12}, @prostenku);
  // «agentic» — Claude docks on it
  G.arrive("#phAI", @t_ai, {s: 0.4, y: -30});
  tl.fromTo("#phAI .mk", {scale: 0.55, autoAlpha: 0}, {scale: 1, autoAlpha: 1, duration: 0.55, ease: SP}, @agentic2);
  tl.fromTo("#phAIg", {autoAlpha: 0, scale: 0.6}, {autoAlpha: 1, scale: 1, duration: 0.35, ease: "power2.out"}, @agentic2);
  tl.to("#phAIg", {autoAlpha: 0, duration: 0.6, ease: "power2.in"}, @t_aig);
  G.sheen("#phAI .sheen", @t_aish);
  G.bump("#phW", @crm5);
  // tab switch: the old screen slides out left, the new one in from the right
  function tab(from, to, sFrom, sTo, t, shift) {
    tl.to("#tb" + from + " i", {opacity: 0, duration: 0.2}, t);
    tl.to("#tb" + from, {color: "rgba(23,20,28,0.62)", duration: 0.2}, t);
    tl.to("#tb" + to + " i", {opacity: 1, duration: 0.2}, t);
    tl.to("#tb" + to, {color: "#ffffff", duration: 0.2}, t);
    tl.to("#flTabs", {x: shift, duration: 0.45, ease: SP}, t);
    tl.to(sFrom, {x: -70, autoAlpha: 0, duration: 0.28, ease: "power2.in"}, t);
    tl.fromTo(sTo, {x: 70, autoAlpha: 0}, {x: 0, autoAlpha: 1, duration: 0.55, ease: SP, immediateRender: false}, t + 0.12);
  }
  // «розширеним» — P&L
  tab(1, 2, "#scP", "#scL", @t_pl, -40);
  // «дашбордом» — Money
  tab(2, 4, "#scL", "#scM", @t_mo, -170);
  // «кілька годин» — Quote, readable
  tab(4, 3, "#scM", "#scQ", @t_qu, -130);
  // «успішно» — the price runs to €400
  tl.to("#qPf", {scaleX: 0.4, duration: 0.75, ease: "power2.inOut"}, @t_p);
  tl.to("#qPt", {x: 0.4 * 492, duration: 0.75, ease: "power2.inOut"}, @t_p);
  // «нею користуюсь» — the hours to 8, and the rate settles
  tl.to("#qHf", {scaleX: 7 / 19, duration: 0.7, ease: "power2.inOut"}, @t_h);
  tl.to("#qHt", {x: 7 / 19 * 492, duration: 0.7, ease: "power2.inOut"}, @t_h);
  G.bump("#qRate", @t_rate);
  G.blurIn("#qNote", @t_rate, 8, 0.3);
  G.sheen("#qRes .sheen", @vse1);
  // «продажами» — push in on the result
  tl.set("#phW", {transformOrigin: "300px 946px"}, @t_push0);
  tl.to("#phW", {scale: 1.4, y: -376, duration: 0.85, ease: "power2.inOut"}, @t_push);
  G.bump("#qSend", @perepys);
  // «використовую Claude» — the iris closes into Claude
  tl.to("#phW", {scale: 0.5, autoAlpha: 0, duration: 0.45, ease: "power3.in"}, @t_x);
  tl.to("#phAI", {x: -327, y: 187, scale: 1.467, duration: 0.56, ease: "power3.inOut"}, @t_x);
  G.irisClose("#tk18", @t_x, 540, 300, 0.56);
  tl.to("#g18", {autoAlpha: 0, duration: 0.02}, @t_off);''',
             t_in=82.960, t_ph=T["navaib"], t_top=T["navaib"] + 0.40, t_kpi=T["navaib"] + 0.55,
             t_ai=T["agentic2"] - 0.12, t_aig=T["agentic2"] + 0.4, t_aish=T["agentic2"] + 0.35,
             t_pl=T["rozshyr"] - 0.06, t_mo=T["dashbord"] - 0.06, t_qu=T["kilka"] - 0.06,
             t_p=T["uspishno"] - 0.04, t_h=T["koryst"] + 0.10, t_rate=T["koryst"] + 0.82,
             t_push0=T["prodazh"] - 0.36, t_push=T["prodazh"] - 0.30,
             t_x=94.160, t_off=94.720)
    return html, src


# =================================================================== b19
SAT = [("fl", (180, 600)), ("cal", (540, 660)), ("bot", (900, 600))]
k.css("""
/* ---- b19-b20 · near: Claude, the command centre; a task in, a report out ---- */
#hub19 { left: 430px; top: 190px; width: 220px; height: 220px; }
#hub19g { left: 240px; top: 0px; width: 600px; height: 600px;
  background: radial-gradient(circle, rgba(255,110,156,0.55) 0%, rgba(255,110,156,0) 60%); }
.h19r { left: 430px; top: 190px; width: 220px; height: 220px; }
.sat { position: absolute; width: 170px; height: 170px; margin: -85px 0 0 -85px; }
#cab19 { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; overflow: visible; }
#tk20 { left: 180px; top: 56px; width: 720px; height: 116px; border-radius: 58px; }
#tk20 .rck { position: absolute; left: 30px; top: 30px; width: 56px; height: 56px; }
#tk20 span { position: absolute; left: 110px; top: 34px; font-size: 38px; font-weight: 700; white-space: nowrap; }
#banner { left: 60px; top: 200px; width: 960px; height: 176px; }
#bIcon { left: 36px; top: 36px; width: 104px; height: 104px; }
#bTitle { left: 170px; top: 42px; font-size: 36px; font-weight: 700; letter-spacing: -0.01em; }
#bBody { left: 170px; top: 94px; font-size: 30px; font-weight: 400; color: rgba(255,255,255,0.84); }
#bTime { right: 44px; top: 48px; font-size: 26px; color: rgba(255,255,255,0.5); }
""")


def cab19(p):
    x, y = p
    return "M 540 410 C 540 %d %d %d %d %d" % (470, x, y - 190, x, y - 85)


@beat
def b19_claude_hq():
    """«і використовую Claude як командний центр, і тому мені не треба заходити
    в ту CRM або в чатбот взагалі — я даю йому задачі, він мені звітує, і
    все.»

    The iris closes into the Claude tile, which is the hub now. On
    «командний центр» three cables draw out to Floor (her CRM), the calendar
    and the chatbot, with a packet down each. On «CRM» Floor recedes, on
    «чатбот» the bot recedes, on «взагалі» the calendar — she does not go in,
    Claude does. On «даю йому задачі» the tools fold into Claude and a task
    card («Надіслати офер Марії» — the client from the card) drops into it;
    on «звітує» Claude comes back as a notification: sent. Haptic on
    «звітує»."""
    sats = "\n        ".join(
        '<div class="sat hide" id="sat-%s" style="left:%dpx;top:%dpx">%s</div>'
        % (key, c[0], c[1], inner) for (key, c), inner in zip(SAT, [
            '<div class="pearl">%s</div>' % floor_wm(46),
            '<div class="clear edge">%s</div>' % g.mark("googlecalendar"),
            '<div class="clear edge">%s</div>' % sym("bot")]))
    cabs = "".join('<path class="tube" id="cT-%s" d="%s"/><path class="core" id="cC-%s" d="%s"/>'
                   '<g class="pkg"><path class="pkt hide" id="cP-%s" d="%s"/></g>'
                   % (key, cab19(c), key, cab19(c), key, cab19(c)) for key, c in SAT)
    html = fill(u'''
      <div class="g full" id="g19">
        <div id="hub19g" class="abs hide"></div>
        <svg id="cab19" class="cab" viewBox="0 0 1080 1920">{{cabs}}</svg>
        {{sats}}
        <div class="sqring h19r hide" id="h19r0"></div><div class="sqring h19r hide" id="h19r1"></div>
        <div id="hub19" class="abs hide"><div class="jelly">{{claude}}<div class="sheen"></div></div></div>
        <div id="tk20" class="dchip edge abs hide"><div class="rck"><div class="f" id="tk20f"></div>{{ck}}</div><span>Надіслати офер Марії</span></div>
        <div id="banner" class="dglass edge abs hide">
          <div class="cx" id="bIcon"><div class="jelly">{{claude}}</div></div>
          <div class="cx" id="bTitle">Claude</div>
          <div class="cx" id="bTime">зараз</div>
          <div class="cx" id="bBody">Офер надіслано · Марія Коваль, €1&nbsp;200</div>
        </div>
      </div>''', cabs=cabs, sats=sats, claude=g.mark("claude"), ck=check_svg("tk20k"))
    src = js('''
  tl.set("#g19", {autoAlpha: 1}, @t_in);
  gsap.set(["#cP-fl", "#cP-cal", "#cP-bot"], {autoAlpha: 0});
  gsap.set("#tk20f", {autoAlpha: 0, scale: 0.4, transformOrigin: "50% 50%"});
  G.drawPrep("tk20k");
  gsap.set("#hub19 .sheen", {xPercent: -120});
  // the iris closed into Claude (b18's corner tile, now here): it is the hub
  tl.set("#hub19", {autoAlpha: 1}, @t_in2);
  // «Claude»
  tl.fromTo("#hub19g", {autoAlpha: 0, scale: 0.6}, {autoAlpha: 1, scale: 1, duration: 0.5, ease: "power2.out"}, @claude2);
  tl.to("#hub19 .sheen", {xPercent: 120, duration: 0.75, ease: "power2.inOut"}, @t_sh);
  G.ripple("#h19r0", @claude2);
  // «командний центр» — the spokes
  ["fl", "cal", "bot"].forEach(function (k, i) {
    var t = @komand + i * 0.14;
    G.drawPrep("cT-" + k); G.drawPrep("cC-" + k);
    tl.to(["#cT-" + k, "#cC-" + k], {strokeDashoffset: 0, duration: 0.5, ease: "power2.inOut"}, t);
    G.blurIn("#sat-" + k, t + 0.2, 12, 0.34);
    tl.fromTo("#sat-" + k, {scale: 0.5, y: -30}, {scale: 1, y: 0, duration: 0.8, ease: POP}, t + 0.2);
    G.packet("cP-" + k, @tsentr + 0.1 + i * 0.08, 0.5);
  });
  G.bump("#hub19", @tsentr);
  // «в ту CRM» / «в чатбот» / «взагалі» — she does not go in; they recede
  tl.to("#sat-fl", {autoAlpha: 0.38, scale: 0.82, duration: 0.45, ease: "power2.out"}, @crm6);
  tl.to(["#cT-fl", "#cC-fl"], {autoAlpha: 0.35, duration: 0.45}, @crm6);
  tl.to("#sat-bot", {autoAlpha: 0.38, scale: 0.82, duration: 0.45, ease: "power2.out"}, @chatbot2);
  tl.to(["#cT-bot", "#cC-bot"], {autoAlpha: 0.35, duration: 0.45}, @chatbot2);
  tl.to("#sat-cal", {autoAlpha: 0.38, scale: 0.82, duration: 0.45, ease: "power2.out"}, @vzahali);
  tl.to(["#cT-cal", "#cC-cal"], {autoAlpha: 0.35, duration: 0.45}, @vzahali);
  G.bump("#hub19", @t_vz);
  // «я даю йому задачі» — the tools fold into Claude; a task drops in
  ["fl", "cal", "bot"].forEach(function (k) {
    tl.to("#sat-" + k, {scale: 0, autoAlpha: 0, duration: 0.4, ease: "power2.in"}, @t_fold);
    tl.to(["#cT-" + k, "#cC-" + k], {autoAlpha: 0, duration: 0.3}, @t_fold);
  });
  G.blurIn("#tk20", @t_task, 10, 0.3);
  tl.fromTo("#tk20", {y: -40, scale: 0.8}, {y: 0, scale: 1, duration: 0.46, ease: POP}, @t_task);
  tl.to("#tk20", {y: 190, scale: 0.28, autoAlpha: 0, duration: 0.4, ease: "power2.in"}, @zadachi);
  G.bump("#hub19", @t_in3);
  G.ripple("#h19r1", @t_in3);
  // «він мені звітує» — Claude comes back as a notification
  tl.to("#hub19", {x: -392, y: -12, scale: 0.47, duration: 0.5, ease: "power3.inOut"}, @vin);
  tl.to("#hub19g", {autoAlpha: 0, duration: 0.4}, @vin);
  gsap.set("#bIcon", {autoAlpha: 0});
  G.blurIn("#banner", @t_bn, 12, 0.3);
  tl.fromTo("#banner", {scale: 0.62, y: -26}, {scale: 1, y: 0, duration: 0.9, ease: POP}, @t_bn);
  tl.set("#hub19", {autoAlpha: 0}, @t_bn2);
  tl.set("#bIcon", {autoAlpha: 1}, @t_bn2);
  tl.fromTo(["#bTitle", "#bTime", "#bBody"], {autoAlpha: 0, y: 10}, {autoAlpha: 1, y: 0, duration: 0.5, ease: SP, stagger: 0.05}, @t_bn3);
  G.haptic("#banner", @t_hap);
  // «Тому» — it slides up and goes
  tl.to("#banner", {y: -48, scale: 0.97, duration: 0.42, ease: "power2.in"}, @tomu2);
  G.blurOut("#banner", @t_bo, 10, 0.34);
  tl.to("#g19", {autoAlpha: 0, duration: 0.02}, @t_off);''',
             t_in=94.340, t_in2=94.700, t_sh=T["claude2"] + 0.2, t_vz=T["vzahali"] + 0.1,
             t_fold=T["dayu"] - 0.24, t_task=T["dayu"] - 0.14, t_in3=T["zadachi"] + 0.4,
             t_bn=T["vin"] + 0.06, t_bn2=T["vin"] + 0.50, t_bn3=T["vin"] + 0.18, t_hap=T["zvituye"] + 0.1,
             t_bo=T["tomu2"] + 0.08, t_off=T["tomu2"] + 0.46)
    return html, src


# =================================================================== b21
k.css("""
/* ---- b21 · the comment composer (reel 12's) ---- */
#cmBox { left: 70px; top: 372px; width: 940px; height: 128px; border-radius: 64px; }
#cmPost { left: 70px; top: 188px; width: 940px; height: 152px; border-radius: 64px; }
.cmav { width: 80px; height: 80px; border-radius: 50%; overflow: hidden;
  background: linear-gradient(160deg, #ffffff 0%, #f6e3e9 100%);
  box-shadow: inset 0 2px 1px #fff, 0 8px 18px -6px rgba(10,0,4,0.5); }
.cmav svg { width: 100%; height: 100%; fill: rgba(180,18,47,0.42); transform: translateY(8%); }
#cmAv { left: 24px; top: 24px; } #cpAv { left: 26px; top: 36px; }
#cmPh { left: 130px; top: 42px; font-size: 36px; font-weight: 500; color: rgba(255,255,255,0.58); }
#cmTyped { left: 130px; top: 26px; font-size: 64px; font-weight: 900; line-height: 76px; }
#cmCaret { left: 132px; top: 38px; width: 4px; height: 52px; border-radius: 2px; background: #ff9cbc; }
#cmSend { right: 40px; top: 44px; font-size: 32px; font-weight: 700; color: #ff9cbc; }
#cpUser { left: 128px; top: 28px; font-size: 32px; font-weight: 700; }
#cpUser span { font-weight: 500; color: rgba(255,255,255,0.55); margin-left: 12px; }
#cpTxt { left: 128px; top: 66px; font-size: 60px; font-weight: 900; line-height: 70px; }
#cpHeart { right: 44px; top: 34px; width: 60px; height: 60px; }
#cpHeart svg { position: absolute; inset: 0; width: 60px; height: 60px; }
#cpHeart .o { fill: none; stroke: rgba(255,255,255,0.8); stroke-width: 1.8; }
#cpHeart .fl { fill: url(#gHeart); }
#cpLiked { right: 128px; top: 44px; width: 48px; height: 48px; border-radius: 50%; overflow: hidden;
  box-shadow: 0 0 0 3px rgba(255,255,255,0.7); background: url("assets/avatar.jpg") center / cover no-repeat; }
#cpLikedH { right: 118px; top: 78px; width: 26px; height: 26px; }
#cpLikedH svg { width: 100%; height: 100%; fill: #ff4f86; stroke: #fff; stroke-width: 2.4; }
#cpRip { right: 44px; top: 34px; width: 60px; height: 60px; border-radius: 50%; border: 3px solid rgba(255,140,180,0.9); }
""")


@beat
def b21_comment_plus():
    """«Тому якщо в тебе залишились питання і ти хочеш підібрати CRM під свої
    потреби, то пиши + і ми поспілкуємось»

    The composer arrives as the notification leaves. The caret comes up on
    «підібрати», «+» is typed on «+» (blackout, plaque kept), posted on «і»,
    liked by her on «поспілкуємось»."""
    html = fill(u'''
      <div class="g full" id="g21">
        <div id="cmPost" class="dglass edge abs hide">
          <div class="cx cmav" id="cpAv">{{person}}</div>
          <div class="cx" id="cpUser">ти<span>щойно</span></div>
          <div class="cx" id="cpTxt">+</div>
          <div class="cx hide" id="cpRip"></div>
          <div class="cx hide" id="cpLiked"></div>
          <div class="cx hide" id="cpLikedH"><svg viewBox="0 0 24 24"><path d="{{heart}}"/></svg></div>
          <div class="cx" id="cpHeart"><svg viewBox="0 0 24 24"><path class="o" d="{{heart}}"/></svg>
            <svg viewBox="0 0 24 24" id="cpFill"><path class="fl" d="{{heart}}"/></svg></div>
        </div>
        <div id="cmBox" class="dglass edge abs">
          <div class="cx cmav" id="cmAv">{{person}}</div>
          <div class="cx" id="cmPh">Додайте коментар…</div>
          <div class="cx hide" id="cmTyped">+</div>
          <div class="cx hide" id="cmCaret"></div>
          <div class="cx" id="cmSend">Опублікувати</div>
        </div>
      </div>''', person=PERSON, heart=HEART)
    src = js('''
  tl.set("#g21", {autoAlpha: 1}, @t_in);
  gsap.set("#cpFill", {scale: 0, autoAlpha: 0, transformOrigin: "50% 60%"});
  gsap.set("#cmSend", {autoAlpha: 0.4});
  G.arrive("#cmBox", @t_in, {s: 0.7, y: 40});
  tl.fromTo("#cmAv", {scale: 0.55, autoAlpha: 0}, {scale: 1, autoAlpha: 1, duration: 0.55, ease: SP}, @t_in2);
  tl.fromTo("#cmPh", {autoAlpha: 0, x: -14}, {autoAlpha: 1, x: 0, duration: 0.5, ease: SP}, @t_in3);
  G.bump("#cmBox", @pytannya);
  // «підібрати» — the cursor
  tl.set("#cmCaret", {autoAlpha: 1}, @pidibr);
  tl.set("#cmPh", {autoAlpha: 0}, @pidibr);
  G.bump("#cmAv", @potreby);
  // «+»
  tl.fromTo("#cmTyped", {autoAlpha: 0, scale: 0.4, transformOrigin: "20% 50%"},
            {autoAlpha: 1, scale: 1, duration: 0.3, ease: POP}, @plus);
  tl.to("#cmCaret", {x: 46, duration: 0.06}, @plus);
  tl.to("#cmSend", {autoAlpha: 1, duration: 0.12}, @plus);
  // «і» — sent; it posts above
  G.bump("#cmSend", @i_last);
  tl.set(["#cmTyped", "#cmCaret"], {autoAlpha: 0}, @t_post);
  tl.set("#cmPh", {autoAlpha: 1}, @t_post);
  tl.to("#cmSend", {autoAlpha: 0.4, duration: 0.2}, @t_post);
  G.blurIn("#cmPost", @t_post, 10, 0.3);
  tl.fromTo("#cmPost", {y: 150, scale: 0.9}, {y: 0, scale: 1, duration: 0.8, ease: SP}, @t_post);
  tl.fromTo("#cpTxt", {scale: 0.6, transformOrigin: "0% 50%"}, {scale: 1, duration: 0.6, ease: POP}, @t_post2);
  // «поспілкуємось» — she likes it
  tl.to("#cpFill", {scale: 1, autoAlpha: 1, duration: 0.55, ease: POP}, @pospilk);
  tl.fromTo("#cpRip", {scale: 1, autoAlpha: 0.9}, {scale: 2.1, autoAlpha: 0, duration: 0.7, ease: "power2.out", immediateRender: false}, @pospilk);
  tl.fromTo("#cpLiked", {autoAlpha: 0, scale: 0.4}, {autoAlpha: 1, scale: 1, duration: 0.55, ease: POP}, @t_lk);
  tl.fromTo("#cpLikedH", {autoAlpha: 0, scale: 0.3}, {autoAlpha: 1, scale: 1, duration: 0.5, ease: POP}, @t_lk2);''',
             t_in=T["yakshcho2"] - 0.02, t_in2=T["yakshcho2"] + 0.08, t_in3=T["yakshcho2"] + 0.22,
             t_post=T["i_last"] + 0.14, t_post2=T["i_last"] + 0.24,
             t_lk=T["pospilk"] + 0.16, t_lk2=T["pospilk"] + 0.28)
    return html, src


# ---------------------------------------------------------------------------
# Captions drop only on redundancy (STYLE.md §2b.1).
BLACKOUT = [
    (4.38, 4.82, "b01 — the chip says «CRM» on «CRM»"),
    (9.30, 13.80, "b02 — the tag and chips say «Рута · власниця продюсерської агенції · fractional automation partner»"),
    (56.58, 58.86, "b12 — the chip says «майже agentic system»"),
    (72.06, 72.92, "b15 — the SendPulse tile is named on «Sendpulse»"),
    (107.76, 108.02, "b21 — the composer types «+» on «+»"),
]
# Blackouts of one word mid-sentence: dropping the plaque for 0.4 s reads as
# a blink (reel 12's lesson), so the word goes and the plaque stays.
KEEP_PLAQUE = [(4.38, 4.82), (72.06, 72.92), (107.76, 108.02)]
INVERT = []

EXTRA_DEFS = (
    '<linearGradient id="gHeart" x1="0" y1="0" x2="0" y2="1">'
    '<stop offset="0" stop-color="#ff6e9c"/><stop offset="1" stop-color="#c4143a"/></linearGradient>'
    '<symbol id="i-sendpulse" viewBox="0 0 24 24"><path d="%s"/></symbol>'
    '<symbol id="i-bot" viewBox="0 0 24 24"><path fill-rule="evenodd" d="%s"/></symbol>'
    '<symbol id="i-funnel" viewBox="0 0 24 24"><path d="%s"/></symbol>'
    % (SP_PATH, BOT_PATH, FUNNEL_PATH))


def counters():
    c = {"sk": T["skilky1"], "r0": T["pobuduye"] - 0.10, "run": T["mozhe"] - 0.06,
         "bh": T["bahato"], "p0": T["uspishno"] - 0.04, "h0": T["koryst"] + 0.10, "dur": DUR}
    return js(r"""
  var CLK = {t: 0};
  function e2o(x) { return 1 - (1 - x) * (1 - x); }
  function e2i(x) { return x * x; }
  function e2io(x) { return x < 0.5 ? 2 * x * x : 1 - Math.pow(-2 * x + 2, 2) / 2; }
  function seg(t, t0, d, a, b, f) { return t <= t0 ? a : t >= t0 + d ? b : a + (b - a) * f((t - t0) / d); }
  function sp(n) { return String(n).replace(/\B(?=(\d{3})+(?!\d))/g, "\u00a0"); }
  var CN = {};
  function put(id, txt) { if (CN[id] !== txt) { CN[id] = txt; document.getElementById(id).textContent = txt; } }
  function paintAll() {
    var t = CLK.t;
    put("fsum", "€" + sp(Math.round(seg(t, @sk, 1.05, 0, 1200, e2o) / 10) * 10));
    put("ndN", sp(Math.round(t < @run ? seg(t, @r0, 1.4, 0, 5, e2o) : seg(t, @run, 0.95, 5, 1000, e2i))));
    var q = seg(t, @bh, 1.5, 1000, 10000, e2o);
    put("q14n", sp(Math.round(q / 10) * 10) + (q > 9990 ? "+" : ""));
    var p = Math.round(seg(t, @p0, 0.75, 200, 400, e2io) / 10) * 10, h = Math.round(seg(t, @h0, 0.7, 3, 8, e2io));
    put("qP", "€" + p); put("qH", h + " h"); put("qRate", "€" + Math.round(p / h) + "/h");
    put("qSendV", "€" + p + " (" + sp(Math.floor(p * 51 / 100) * 100) + " ₴)");
  }
  tl.fromTo(CLK, {t: 0}, {t: @dur, duration: @dur, ease: "none", onUpdate: paintAll}, 0);""", **c)


def main():
    gh, gj = [], []
    for fn in BEATS:
        h, j = fn()
        gh.append(h.rstrip())
        gj.append("  /* %s */" % fn.__name__)
        gj.append(j.rstrip())

    # the slow push on the plate (§0.8): her and her mattes move as one
    head = [g.js(), "  var G = helpers(tl);", counters(),
            '  function drift1(sel, t, d) { tl.fromTo(sel + " .aurs", {x: 0, y: 0}, '
            '{x: -110, y: 70, duration: d, ease: "sine.inOut"}, t); }',
            '  gsap.set(["#vid", ".matte"], {transformOrigin: "540px 820px"});',
            '  tl.fromTo(["#vid", ".matte"], {scale: 1}, {scale: 1.045, duration: %.3f, '
            'ease: "none"}, 0);' % DUR]
    doc = k.document(
        title=u"Reel 15 — СРМ для агенцій",
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
    print("index.html  %d captions, %d beats, %d wall tiles, %.1f KB"
          % (len(CAPS), len(BEATS), len(wall16), os.path.getsize(out) / 1024.0))


main()
