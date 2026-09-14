# -*- coding: utf-8 -*-
"""Reel 11 — «скільки коштує почати вайбкодити».

Variant B: her cut, graded, no subtitles. Materials from tools/kit.py
(STYLE.md §5a); what each beat depicts is invented for this script.

The recurring object is **somebody else's budget**. The script's argument is
that the number people quote is padded with things that are free, so the object
is a line-item list that arrives long and expensive and gets emptied: each line
struck through as it turns out to cost nothing, until one line is left and it
says 20.

Deliberately not reel 8's receipt. That one accumulated toward a true total;
this one is a list being *taken apart*, and the difference is the whole point of
each reel.

The series name is «вайбкодити», not «вайпкодити» as SCRIPTS.md §6 had it —
she says /vajb/ and the same script's closing line already spelled it that way.
Fixed at source, so the next reel in the series inherits it.

usage: python build.py
"""
import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
from kit import Kit  # noqa: E402

DUR = 88.483           # 2655 plate frames / 30, rounded down
k = Kit(width=1080, height=1920, fps=30, duration=DUR)

BEATS = []


def beat(fn):
    BEATS.append(fn)
    return fn


# ---------------------------------------------------------------------------
# NO-PAINT ZONES — her own editing (STYLE.md §4a). This is the busiest cut in
# the batch: ~11 s of 88 belongs to her.
#
#  22.15 – 23.10   pushes the frame back mid-sentence
#  24.40 – 27.40   pulls back AND tilts the whole frame over — a 1.5 s skewed
#                  shot, which is the biggest single gag in the reel
#  36.90 – 40.60   a 3.7 s pull-out under «чим більше грошей, тим крутіше»
#  52.20 – 53.35   big face closeup
#  81.37 – 82.60   big face closeup
#  87.65 – 88.55   pulls way out for the last beat of the reel
#
# Found by tools/shots.py (the cuts) and tools/pullouts.py (the zooms, which
# scene detection cannot see).
NO_PAINT = [(22.15, 23.10), (24.40, 27.40), (36.90, 40.60),
            (52.20, 53.35), (81.37, 82.60), (87.65, 88.55)]


# ---------------------------------------------------------------- materials

def mark(name):
    return '<img class="mk" src="assets/logos/%s.png" alt="">' % name


def marktile(tid, name, cls="", style=""):
    return ('<div class="tile brand prod %s" id="%s"%s>%s</div>'
            % (cls, tid, (' style="%s"' % style) if style else "", mark(name)))


def openrouter():
    """Her OpenRouter asset is an SVG and there is no rasteriser on the
    machine, so it goes in as inline SVG — which renders identically and takes
    its colour from the tile."""
    return io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "assets", "logos", "openrouter.svg.txt"),
                   encoding="utf-8").read()


def budget_row(rid, label_mark=None, cls=""):
    inner = mark(label_mark) if label_mark else '<span class="ph"></span>'
    return ('<div class="brow %s" id="%s">%s<span class="bar"></span>'
            '<span class="cost"></span><span class="strike"></span></div>'
            % (cls, rid, inner))


k.css("""
    /* ---- somebody else's budget, which is the object of the reel ---- */
    .budget { position: absolute; left: 120px; top: 60px; width: 840px;
              padding: 28px 30px; background: var(--lit-blush);
              box-shadow: var(--rim); filter: var(--cast); }
    .brow { position: relative; display: flex; align-items: center; gap: 20px;
            height: 84px; }
    .brow + .brow { border-top: 3px solid rgba(23,20,28,0.09); }
    .brow .mk { width: 52px; height: 52px; object-fit: contain; flex: none;
                display: block; }
    .brow .ph { display: block; width: 52px; height: 52px; border-radius: 16px;
                background: var(--container-high); flex: none;
                box-shadow: inset 0 0 0 3px rgba(23,20,28,0.16); }
    .brow .bar { display: block; flex: 1; height: 26px; border-radius: 13px;
                 background: rgba(23,20,28,0.32); }
    .brow:nth-child(2) .bar { width: 88%; flex: 0 1 auto; }
    .brow:nth-child(3) .bar { width: 72%; flex: 0 1 auto; }
    .brow:nth-child(4) .bar { width: 56%; flex: 0 1 auto; }
    .brow .cost { display: block; width: 104px; height: 34px; flex: none;
                  border-radius: 17px; background: var(--lit-accent);
                  box-shadow: var(--rim-dark); }
    .brow .strike { position: absolute; left: 0; top: 40px; width: 100%;
                    height: 9px; border-radius: 5px; background: var(--accent); }
    .brow.gone .cost { background: rgba(23,20,28,0.12); box-shadow: none; }

    /* ---- numbers ---- */
    .big { position: absolute; left: 0; width: 1080px; text-align: center;
           font-weight: 900; color: #fff; letter-spacing: -0.05em;
           line-height: 1; text-shadow: 0 18px 60px rgba(8,6,12,0.55); }
    .big small { font-size: 0.42em; }
    .big .sx { position: absolute; left: 22%; top: 46%; width: 56%;
               height: 16px; border-radius: 8px; background: var(--accent); }

    /* ---- product tiles ---- */
    .tile.brand.prod { position: absolute; width: 240px; height: 240px;
                       display: grid; place-items: center;
                       background: var(--lit-blush); }
    .tile.brand.prod .mk { width: 60%; height: auto; max-height: 62%;
                           object-fit: contain; display: block; }
    .tile.brand.prod .orsvg { width: 68%; height: auto; display: block;
                              color: var(--accent); }
    .wordmark { font-weight: 900; color: var(--accent); line-height: 1;
                letter-spacing: -0.045em; -webkit-text-stroke: 3px var(--accent); }

    /* ---- the free badge, fourth reel running ---- */
    .freewrap { position: absolute; width: 190px; height: 190px; }
    .free { position: absolute; inset: 0; display: grid; place-items: center;
            grid-auto-flow: column; gap: 3px; border-radius: 50%;
            background: var(--lit-accent); box-shadow: var(--rim-dark); }
    .free span { font-size: 106px; font-weight: 900; color: #fff;
                 letter-spacing: -0.06em; line-height: 1; }
    .free small { font-size: 46px; font-weight: 900; color: #fff; }

    /* ---- the apps she has already built ---- */
    .apps { position: absolute; left: 180px; top: 150px; width: 720px;
            display: flex; gap: 24px; justify-content: center; }
    .apps i { display: block; width: 150px; height: 150px; border-radius: 40px;
              background: var(--lit-blush); box-shadow: var(--rim);
              filter: var(--cast-sm); }
    .apps i:nth-child(2) { background: var(--lit-accent);
                           box-shadow: var(--rim-dark); }
    .apps i:nth-child(4) { background: var(--lit-pink);
                           box-shadow: var(--rim-dark); }

    /* ---- what the RUTA app actually does ---- */
    .voice { position: absolute; display: flex; align-items: center; gap: 9px; }
    .voice i { display: block; width: 13px; border-radius: 7px;
               background: var(--pink); }
    .outs { position: absolute; left: 150px; top: 330px; width: 780px;
            display: flex; gap: 22px; justify-content: center; }
    .outs span { display: block; width: 180px; height: 210px; border-radius: 30px;
                 background: var(--lit-blush); box-shadow: var(--rim);
                 filter: var(--cast-sm); }
    .outs span:nth-child(2) { background: var(--lit-accent);
                              box-shadow: var(--rim-dark); }

    /* ---- tokens: money going in, usage coming out ---- */
    .meter { position: absolute; left: 240px; top: 330px; width: 600px;
             height: 48px; border-radius: 24px;
             background: rgba(255,255,255,0.30); box-shadow: var(--rim);
             overflow: hidden; }
    .meter i { position: absolute; left: 0; top: 0; height: 48px; width: 100%;
               background: var(--lit-pink); }
""")

for _sel, _w, _h, _r in [
    (".tile.brand.prod", 240, 240, 58),
    (".budget", 840, 520, 52),
]:
    k.squircle(_sel, _w, _h, _r)


# ------------------------------------------------------------------ A · hook


@beat
def b01_five_hundred():
    """«у Тредсі пишуть, що треба мати 500 євро на місяць» → «а насправді
    можна почати з 20 доларів»

    The quoted number, then the real one. The gap between them is the reel.
    """
    html = '''
      <div class="g full" id="g1">
        <div class="big" id="g1a" style="top:150px;font-size:250px">500<small>€</small><span class="sx" id="g1x"></span></div>
        <div class="big" id="g1b" style="top:180px;font-size:250px">20<small>$</small></div>
      </div>'''
    js = '''
  gsap.set("#g1", {autoAlpha: 0});
  gsap.set("#g1a", {autoAlpha: 0, scale: 0.6, transformOrigin: "50% 50%"});
  gsap.set("#g1x", {scaleX: 0, transformOrigin: "0% 50%"});
  gsap.set("#g1b", {autoAlpha: 0, scale: 0.5, transformOrigin: "50% 50%"});
  tl.set("#g1", {autoAlpha: 1}, 4.16);
  // «500 євро на місяць»
  tl.to("#g1a", {autoAlpha: 1, scale: 1, duration: 0.36, ease: "back.out(2.8)"}, 4.28);
  // it keeps inflating while she describes it, which is the claim
  tl.to("#g1a", {scale: 1.12, duration: 1.40, ease: "power1.inOut"}, 5.00);
  // «а насправді можна почати з 20 доларів» — struck, and replaced
  tl.to("#g1x", {scaleX: 1, duration: 0.30, ease: "power3.out"}, 8.14);
  tl.to("#g1a", {autoAlpha: 0, scale: 0.7, duration: 0.34,
                 ease: "power2.in"}, 8.50);
  tl.to("#g1b", {autoAlpha: 1, scale: 1, duration: 0.38, ease: "back.out(2.8)"}, 8.72);
  tl.to("#g1", {autoAlpha: 0, duration: 0.26, ease: "power2.in"}, 10.30);'''
    return html, js


@beat
def b02_four_apps():
    """«я вже розробила чотири додатки і купу власних інструментів»"""
    html = '''
      <div class="g full" id="g2">
        <div class="apps" id="g2a"><i></i><i></i><i></i><i></i></div>
        <div class="apps small" id="g2t" style="top:340px">
          <i></i><i></i><i></i><i></i><i></i><i></i>
        </div>
      </div>'''
    js = '''
  gsap.set("#g2", {autoAlpha: 0});
  gsap.set("#g2a i, #g2t i", {autoAlpha: 0, scale: 0.5,
                              transformOrigin: "50% 50%"});
  tl.set("#g2", {autoAlpha: 1}, 10.58);
  // «чотири додатки» — four of them, counted out
  [10.70, 10.86, 11.02, 11.18].forEach(function (t, i) {
    tl.to("#g2a i:nth-child(" + (i + 1) + ")",
          {autoAlpha: 1, scale: 1, duration: 0.28, ease: "back.out(2.6)"}, t);
  });
  // «і купу власних інструментів» — and a pile more, too many to count
  tl.to("#g2t i", {autoAlpha: 1, scale: 1, duration: 0.24, ease: "back.out(2.2)",
                   stagger: 0.05}, 12.30);
  tl.to("#g2", {autoAlpha: 0, duration: 0.26, ease: "power2.in"}, 14.30);'''
    return html, js


# --------------------------------------------------- B · somebody's budget


@beat
def b03_the_budget_post():
    """«такі пости з розписаним бюджетом… навіщо туди вписують платформи, за
    які на початку не треба платити взагалі»

    The list arrives long and priced. Clears at 22.05 — she pushes the frame
    back at 22.15 and then tilts the whole shot over until 27.40.
    """
    html = '''
      <div class="g full" id="g3">
        <div class="budget" id="g3b">%s%s%s%s</div>
      </div>''' % (budget_row("g3r0"), budget_row("g3r1"),
                   budget_row("g3r2"), budget_row("g3r3"))
    js = '''
  gsap.set("#g3", {autoAlpha: 0});
  gsap.set("#g3b", {autoAlpha: 0, scale: 0.92, transformOrigin: "50% 30%"});
  gsap.set("#g3 .brow", {autoAlpha: 0, x: -26});
  tl.set("#g3", {autoAlpha: 1}, 15.00);
  // «такі пости з розписаним бюджетом»
  tl.to("#g3b", {autoAlpha: 1, scale: 1, duration: 0.30, ease: "power2.out"}, 15.12);
  tl.to("#g3 .brow", {autoAlpha: 1, x: 0, duration: 0.24, stagger: 0.10,
                      ease: "power3.out"}, 15.98);
  // «навіщо туди вписують платформи» — the priced lines are the problem
  tl.to("#g3 .cost", {scale: 1.16, duration: 0.24, ease: "back.out(3)",
                      stagger: 0.05, transformOrigin: "50% 50%"}, 18.54);
  tl.to("#g3 .cost", {scale: 1, duration: 0.26, stagger: 0.04}, 18.90);
  // «за які на початку не треба платити взагалі»
  tl.to("#g3 .cost", {autoAlpha: 0.35, duration: 0.34, stagger: 0.04}, 20.88);
  tl.to("#g3", {autoAlpha: 0, duration: 0.22, ease: "power2.in"}, 21.90);'''
    return html, js


@beat
def b04_all_of_it_free():
    """«і ще купа якихось додаткових штук, хоча по факту це все безкоштовне на
    старті»

    The list comes back, now with the two she actually named, and every line
    is struck through. She names Versal and Supabase at 24.9 and 25.9 — both
    inside the tilted shot — so the marks arrive here instead, at the first
    moment the frame is mine again.
    """
    html = '''
      <div class="g full" id="g4">
        <div class="budget" id="g4b">%s%s%s%s</div>
        <div class="freewrap" id="g4f" style="left:445px;top:330px">
          <div class="lit soft"></div>
          <div class="free"><span>0</span><small>€</small></div>
        </div>
      </div>''' % (budget_row("g4r0", "vercel-mark"),
                   budget_row("g4r1", "supabase-mark"),
                   budget_row("g4r2"), budget_row("g4r3"))
    js = '''
  gsap.set("#g4", {autoAlpha: 0});
  gsap.set("#g4b", {autoAlpha: 0, scale: 0.94, transformOrigin: "50% 30%"});
  gsap.set("#g4 .brow", {autoAlpha: 0});
  gsap.set("#g4 .strike", {scaleX: 0, transformOrigin: "0% 50%"});
  gsap.set("#g4f", {autoAlpha: 0, scale: 0.5, transformOrigin: "50% 50%"});
  tl.set("#g4", {autoAlpha: 1}, 27.50);
  tl.to("#g4b", {autoAlpha: 1, scale: 1, duration: 0.28, ease: "power2.out"}, 27.56);
  tl.to("#g4 .brow", {autoAlpha: 1, duration: 0.22, stagger: 0.08}, 27.64);
  // «і ще купа якихось додаткових штук» — the pile grows
  tl.to("#g4r2, #g4r3", {scale: 1.03, duration: 0.24, ease: "back.out(2.6)",
                         transformOrigin: "50% 50%"}, 29.61);
  tl.to("#g4r2, #g4r3", {scale: 1, duration: 0.26}, 29.90);
  // «хоча по факту це все безкоштовне на старті» — every line struck
  tl.to("#g4 .strike", {scaleX: 1, duration: 0.26, ease: "power3.out",
                        stagger: 0.09}, 30.34);
  tl.to("#g4 .cost", {autoAlpha: 0.28, duration: 0.24}, 30.90);
  tl.to("#g4f", {autoAlpha: 1, scale: 1, duration: 0.34,
                 ease: "back.out(2.8)"}, 31.66);
  tl.to("#g4", {autoAlpha: 0, duration: 0.26, ease: "power2.in"}, 33.20);'''
    return html, js


@beat
def b05_inflated():
    """«цифра ніби роздувається штучно, щоб здавалось, що це дорога і серйозна
    штука»

    The number swells past what it should be, and a pin is all it would take.
    Clears at 36.80 — she pulls the frame way out from 36.90 to 40.60, under
    «чим більше грошей, тим крутіше», which is the joke landing without help.
    """
    html = '''
      <div class="g full" id="g5">
        <div class="big" id="g5n" style="top:190px;font-size:180px">500<small>€</small></div>
      </div>'''
    js = '''
  gsap.set("#g5", {autoAlpha: 0});
  gsap.set("#g5n", {autoAlpha: 0, scale: 0.7, transformOrigin: "50% 50%"});
  tl.set("#g5", {autoAlpha: 1}, 33.56);
  tl.to("#g5n", {autoAlpha: 1, scale: 1, duration: 0.30, ease: "back.out(2.6)"}, 33.68);
  // «роздувається штучно» — and it keeps going, well past sense
  tl.to("#g5n", {scale: 1.5, duration: 0.70, ease: "power2.out"}, 34.48);
  tl.to("#g5n", {scale: 1.72, duration: 0.90, ease: "power1.inOut"}, 35.66);
  tl.to("#g5", {autoAlpha: 0, duration: 0.24, ease: "power2.in"}, 36.56);'''
    return html, js


# ------------------------------------------------- C · what it actually costs


@beat
def b06_only_one_thing():
    """«щоб розробити свій перший маленький інструмент, тобі потрібно тільки
    одне — підписка на сам штучний інтелект»
    """
    html = '''
      <div class="g full" id="g6">
        <div class="budget" id="g6b">%s</div>
      </div>''' % budget_row("g6r0")
    js = '''
  gsap.set("#g6", {autoAlpha: 0});
  gsap.set("#g6b", {autoAlpha: 0, scale: 0.9, transformOrigin: "50% 50%"});
  gsap.set("#g6r0", {autoAlpha: 0, x: -30});
  tl.set("#g6", {autoAlpha: 1}, 42.94);
  // «свій перший маленький інструмент» — card and line together; an empty card
  // says nothing (STYLE.md §4a.5)
  tl.to("#g6b", {autoAlpha: 1, scale: 1, duration: 0.30, ease: "back.out(2.2)"}, 43.06);
  tl.to("#g6r0", {autoAlpha: 1, x: 0, duration: 0.26, ease: "power3.out"}, 43.20);
  // «тільки одне» — and it is still only the one line
  tl.to("#g6r0", {scale: 1.05, duration: 0.24, ease: "back.out(2.8)",
                  transformOrigin: "50% 50%"}, 45.06);
  tl.to("#g6r0", {scale: 1, duration: 0.28, ease: "power2.out"}, 45.36);
  tl.to("#g6", {autoAlpha: 0, duration: 0.24, ease: "power2.in"}, 46.60);'''
    return html, js


@beat
def b07_claude_or_codex():
    """«тобто Claude Code або Codex, і це навіть не 100 євро, а 20»

    Clears at 52.12: she cuts to a big closeup at 52.20.
    """
    html = '''
      <div class="g full" id="g7">
        %s
        %s
        <div class="big" id="g7h" style="top:400px;font-size:140px">100<small>€</small><span class="sx" id="g7x"></span></div>
        <div class="big" id="g7t" style="top:400px;font-size:150px">20<small>$</small></div>
      </div>''' % (
        marktile("g7a", "claude-tile", style="left:180px;top:110px"),
        marktile("g7b", "codex-mark", style="left:660px;top:110px"))
    js = '''
  gsap.set("#g7", {autoAlpha: 0});
  gsap.set("#g7a, #g7b", {autoAlpha: 0, scale: 0.7, transformOrigin: "50% 50%"});
  gsap.set("#g7h, #g7t", {autoAlpha: 0, scale: 0.6, transformOrigin: "50% 50%"});
  gsap.set("#g7x", {scaleX: 0, transformOrigin: "0% 50%"});
  tl.set("#g7", {autoAlpha: 1}, 48.46);
  tl.to("#g7a", {autoAlpha: 1, scale: 1, duration: 0.30, ease: "back.out(2.4)"}, 48.58);
  tl.to("#g7b", {autoAlpha: 1, scale: 1, duration: 0.30, ease: "back.out(2.4)"}, 49.52);
  // «не 100 євро»
  tl.to("#g7h", {autoAlpha: 1, scale: 1, duration: 0.28, ease: "back.out(2.6)"}, 51.10);
  tl.to("#g7x", {scaleX: 1, duration: 0.24, ease: "power3.out"}, 51.50);
  // «а 20»
  tl.to("#g7h", {autoAlpha: 0, duration: 0.20}, 51.90);
  tl.to("#g7t", {autoAlpha: 1, scale: 1, duration: 0.30, ease: "back.out(2.8)"}, 51.98);
  tl.to("#g7", {autoAlpha: 0, duration: 0.18, ease: "power2.in"}, 52.00);'''
    return html, js


@beat
def b08_hosting_and_db():
    """«хостинг — це той самий Versal, у нього щедрі безкоштовні ліміти… база
    даних — Supabase, там теж безкоштовний»

    Both marks, both with the same badge, because the point is that they are
    the same answer twice.
    """
    html = '''
      <div class="g full" id="g8">
        %s
        <div class="freewrap" id="g8fa" style="left:470px;top:135px">
          <div class="lit soft"></div>
          <div class="free"><span>0</span><small>€</small></div>
        </div>
        %s
        <div class="freewrap" id="g8fb" style="left:470px;top:135px">
          <div class="lit soft"></div>
          <div class="free"><span>0</span><small>€</small></div>
        </div>
      </div>''' % (
        marktile("g8a", "vercel-mark", style="left:170px;top:110px"),
        marktile("g8b", "supabase-mark", style="left:170px;top:110px"))
    js = '''
  gsap.set("#g8", {autoAlpha: 0});
  gsap.set("#g8a, #g8b", {autoAlpha: 0, scale: 0.7, transformOrigin: "50% 50%"});
  gsap.set("#g8fa, #g8fb", {autoAlpha: 0, scale: 0.5,
                            transformOrigin: "50% 50%"});
  tl.set("#g8", {autoAlpha: 1}, 54.72);
  // «той самий Versal»
  tl.to("#g8a", {autoAlpha: 1, scale: 1, duration: 0.30, ease: "back.out(2.4)"}, 54.84);
  // «щедрі безкоштовні ліміти»
  tl.to("#g8fa", {autoAlpha: 1, scale: 1, duration: 0.32,
                  ease: "back.out(2.8)"}, 57.10);
  tl.to("#g8a, #g8fa", {autoAlpha: 0, scale: 0.86, duration: 0.26,
                        ease: "power2.in"}, 58.90);
  // «база даних — Supabase, там теж безкоштовний»
  tl.to("#g8b", {autoAlpha: 1, scale: 1, duration: 0.30, ease: "back.out(2.4)"}, 59.20);
  tl.to("#g8fb", {autoAlpha: 1, scale: 1, duration: 0.32,
                  ease: "back.out(2.8)"}, 60.78);
  tl.to("#g8", {autoAlpha: 0, duration: 0.26, ease: "power2.in"}, 62.60);'''
    return html, js


# ------------------------------------------------------ D · the one exception


@beat
def b09_ruta_does_work():
    """«єдине, за що доведеться доплатити окремо — це якщо в твоєму додатку сам
    штучний інтелект щось робить, як у мене в Руті, де голосове перетворюється
    на рілс, сторіс чи карусель»
    """
    html = '''
      <div class="g full" id="g9">
        <div class="tile brand prod" id="g9r" style="left:420px;top:60px">
          <span class="wordmark" style="font-size:58px">RUTA</span>
        </div>
        <div class="voice" id="g9v" style="left:420px;top:330px;width:240px;
             height:90px;justify-content:center">%s</div>
        <div class="outs" id="g9o"><span></span><span></span><span></span></div>
      </div>''' % "".join('<i style="height:%dpx"></i>' % h
                          for h in [22, 52, 84, 40, 70, 30, 60, 44, 78, 28])
    js = '''
  gsap.set("#g9", {autoAlpha: 0});
  gsap.set("#g9r", {autoAlpha: 0, scale: 0.7, transformOrigin: "50% 50%"});
  gsap.set("#g9v", {autoAlpha: 0});
  gsap.set("#g9v i", {scaleY: 0.2, transformOrigin: "50% 50%"});
  gsap.set("#g9o span", {autoAlpha: 0, scale: 0.6, y: -50,
                         transformOrigin: "50% 50%"});
  tl.set("#g9", {autoAlpha: 1}, 67.34);
  // «сам штучний інтелект щось робить… як у мене в Руті»
  tl.to("#g9r", {autoAlpha: 1, scale: 1, duration: 0.32, ease: "back.out(2.4)"}, 67.46);
  // «де голосове»
  tl.to("#g9v", {autoAlpha: 1, duration: 0.16}, 69.54);
  tl.to("#g9v i", {scaleY: 1, duration: 0.30, ease: "back.out(2)",
                   stagger: {each: 0.018, from: "center"}}, 69.58);
  // «на рілс, сторіс чи карусель» — one output per word
  [71.28, 71.55, 72.12].forEach(function (t, i) {
    tl.to("#g9o span:nth-child(" + (i + 1) + ")",
          {autoAlpha: 1, scale: 1, y: 0, duration: 0.30,
           ease: "back.out(2.4)"}, t);
  });
  tl.to("#g9", {autoAlpha: 0, duration: 0.26, ease: "power2.in"}, 73.40);'''
    return html, js


@beat
def b10_openrouter():
    """«для цього я користуюсь OpenRouter — туди просто кладеш гроші, і вони
    йдуть за токенами»

    Her OpenRouter file is an SVG, inlined rather than rasterised: there is no
    converter on the machine and an inline path renders identically.
    """
    html = '''
      <div class="g full" id="g10">
        <div class="tile brand prod" id="g10t" style="left:420px;top:60px">%s</div>
        <div class="meter" id="g10m"><i id="g10f"></i></div>
      </div>''' % openrouter()
    js = '''
  gsap.set("#g10", {autoAlpha: 0});
  gsap.set("#g10t", {autoAlpha: 0, scale: 0.7, transformOrigin: "50% 50%"});
  gsap.set("#g10m", {autoAlpha: 0});
  gsap.set("#g10f", {scaleX: 0, transformOrigin: "0% 50%"});
  tl.set("#g10", {autoAlpha: 1}, 75.30);
  tl.to("#g10t", {autoAlpha: 1, scale: 1, duration: 0.32, ease: "back.out(2.4)"}, 75.42);
  // «туди просто кладеш гроші» — the balance goes in
  tl.to("#g10m", {autoAlpha: 1, duration: 0.20}, 77.42);
  tl.to("#g10f", {scaleX: 1, duration: 0.46, ease: "power2.out"}, 77.50);
  // «і вони йдуть за токенами» — and it goes down slowly, which is the point
  tl.to("#g10f", {scaleX: 0.72, duration: 0.80, ease: "power1.inOut"}, 78.58);
  tl.to("#g10", {autoAlpha: 0, duration: 0.26, ease: "power2.in"}, 80.40);'''
    return html, js


@beat
def b11_subscribe():
    """«обов'язково підпишись, бо я розповідаю про закулісся реального
    вайбкодингу»

    Clears at 87.55 — she pulls the frame way out for the last three quarters
    of a second and that is hers.
    """
    html = '''
      <div class="g full" id="g11">
        <div class="plus" id="g11p"><i></i><i></i></div>
      </div>'''
    js = '''
  gsap.set("#g11", {autoAlpha: 0});
  gsap.set("#g11p", {autoAlpha: 0, scale: 0.4, rotation: -90,
                     transformOrigin: "50% 50%"});
  tl.set("#g11", {autoAlpha: 1}, 84.26);
  tl.to("#g11p", {autoAlpha: 1, scale: 1, rotation: 0, duration: 0.36,
                  ease: "back.out(2.8)"}, 84.38);
  // «реального вайбкодингу» — one last settle on the series name
  tl.to("#g11p", {scale: 1.08, duration: 0.34, ease: "power2.inOut"}, 87.14);
  tl.to("#g11", {autoAlpha: 0, duration: 0.20, ease: "power2.in"}, 87.50);'''
    return html, js


k.css("""
    .apps.small i { width: 96px; height: 96px; border-radius: 26px; }
    .apps.small { gap: 18px; }

    /* b11 — subscribe. Top of frame: her last shots are closeups. */
    .plus { position: absolute; left: 468px; top: 100px; width: 144px;
            height: 144px; border-radius: 44px; background: var(--lit-accent);
            box-shadow: var(--rim-dark); filter: var(--cast); }
    .plus i { position: absolute; left: 34px; top: 62px; width: 76px;
              height: 20px; border-radius: 10px; background: #fff; }
    .plus i:nth-child(2) { transform: rotate(90deg); }
""")

for _sel, _w, _h, _r in [
    (".plus", 144, 144, 44),
]:
    k.squircle(_sel, _w, _h, _r)


def main():
    caps = k.load_captions(os.path.join(ROOT, "work", "r11", "captions.json"))
    gh, gj = [], []
    for fn in BEATS:
        h, j = fn()
        if h.strip():
            gh.append(h.rstrip())
        gj.append("  /* %s */" % fn.__name__)
        gj.append(j.rstrip())

    doc = k.document(
        title="Reel 11 — скільки коштує вайбкодити",
        plate="assets/base.mp4",
        gfx_html="\n".join(gh),
        gfx_js="\n".join(gj),
        caps=caps,
    )
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "index.html")
    io.open(out, "w", encoding="utf-8").write(doc)
    print("index.html  %d captions, %d beats, %.1f KB"
          % (len(caps), len(BEATS), os.path.getsize(out) / 1024.0))


main()
