# -*- coding: utf-8 -*-
"""Reel 9 — «я ненавиджу робити презентації».

Variant B: her cut, graded, no subtitles. Materials from tools/kit.py
(STYLE.md §5a); what each beat depicts is invented for this script.

The recurring object is **one slide, and what happens to it**. It arrives as a
black-and-white wireframe, gets a design system built beside it, and at
«гарно задизайнена презентація» the wireframe turns into the finished thing.
The transformation *is* the reel, so the same object carries the whole argument
(STYLE.md §4, reuse objects).

Deliberately not reel 5's object. Reel 5 was also about presentations and its
spine was «a slide the AI wrote, then the same slide read properly»; repeating
that would make two reels look like one. Here the slide is hers from the start
and the AI only ever dresses it.

tools/shots.py found 5 shots and no comedy inserts; tools/pullouts.py found no
zooms. So this is the one reel in the batch with no NO_PAINT list — her editing
is plain and the frame is mine. The last shot (100.53+) is framed closer for
the CTA, so the graphic there stays small and low.

usage: python build.py
"""
import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
from kit import Kit  # noqa: E402

DUR = 103.250          # 3098 plate frames / 30, rounded down
k = Kit(width=1080, height=1920, fps=30, duration=DUR)

BEATS = []


def beat(fn):
    BEATS.append(fn)
    return fn


# Her editing is plain in this one: no inserts, no zooms. Nothing to keep off.
NO_PAINT = []


# ---------------------------------------------------------------- materials

def mark(name):
    return '<img class="mk" src="assets/logos/%s.png" alt="">' % name


def marktile(tid, name, cls="", style=""):
    return ('<div class="tile brand prod %s" id="%s"%s>%s</div>'
            % (cls, tid, (' style="%s"' % style) if style else "", mark(name)))


def wire(sid, cls="", rows=3, pic=False, chart=False, style=""):
    """The skeleton slide: a heading rule and ragged body, no colour at all.
    §5a.3 — ragged lengths read as abstracted text, uniform ones read as a
    loading state."""
    body = "".join('<b class="wr"></b>' for _ in range(rows))
    extra = ''
    if pic:
        extra += '<span class="wpic"></span>'
    if chart:
        extra += ('<span class="wchart"><i></i><i></i><i></i><i></i></span>')
    return ('<div class="slide %s" id="%s"%s><b class="wh"></b>%s%s</div>'
            % (cls, sid, (' style="%s"' % style) if style else "", body, extra))


k.css("""
    /* ---- the slide, in both of its states ---- */
    .slide { position: absolute; width: 620px; height: 380px; padding: 40px 44px;
             overflow: hidden;
             background: #ffffff; box-shadow: var(--rim); filter: var(--cast); }
    .slide .wh { display: block; height: 40px; width: 64%; border-radius: 10px;
                 background: #2a2730; margin-bottom: 30px; }
    .slide .wr { display: block; height: 20px; border-radius: 6px;
                 background: rgba(23,20,28,0.26); margin-bottom: 18px; }
    .slide .wr:nth-of-type(2) { width: 92%; }
    .slide .wr:nth-of-type(3) { width: 68%; }
    .slide .wr:nth-of-type(4) { width: 44%; }
    .slide .wpic { position: absolute; right: 44px; bottom: 44px; width: 190px;
                   height: 140px; border-radius: 12px;
                   background: rgba(23,20,28,0.14); }
    .slide .wchart { position: absolute; right: 44px; bottom: 44px; width: 190px;
                     height: 140px; display: flex; align-items: flex-end;
                     gap: 12px; }
    .slide .wchart i { display: block; flex: 1; border-radius: 6px 6px 0 0;
                       background: rgba(23,20,28,0.20); }
    .slide .wchart i:nth-child(1) { height: 46%; }
    .slide .wchart i:nth-child(2) { height: 78%; }
    .slide .wchart i:nth-child(3) { height: 58%; }
    .slide .wchart i:nth-child(4) { height: 100%; }

    /* the designed state — same geometry, dressed */
    .slide.done { background: var(--lit-blush); }
    .slide.done .wh { background: var(--lit-accent); box-shadow: var(--rim-dark);
                      height: 46px; border-radius: 14px; }
    .slide.done .wr { background: var(--graphite); }
    .slide.done .wpic { background: var(--lit-pink); box-shadow: var(--rim-dark);
                        border-radius: 20px; }

    /* ---- product tiles ---- */
    .tile.brand.prod { position: absolute; width: 250px; height: 250px;
                       display: grid; place-items: center;
                       background: var(--lit-blush); }
    .tile.brand.prod .mk { width: 60%; height: auto; max-height: 62%;
                           object-fit: contain; display: block; }

    /* ---- the design system it builds ---- */
    .dsys { position: absolute; left: 190px; top: 70px; width: 700px;
            padding: 34px; background: var(--lit-blush); box-shadow: var(--rim);
            filter: var(--cast); }
    .swatches { display: flex; gap: 18px; margin-bottom: 26px; }
    .swatches i { display: block; width: 92px; height: 92px; border-radius: 26px;
                  box-shadow: var(--rim); }
    .swatches i:nth-child(1) { background: var(--accent); }
    .swatches i:nth-child(2) { background: var(--pink); }
    .swatches i:nth-child(3) { background: var(--container-high); }
    .swatches i:nth-child(4) { background: var(--ink); }
    .typerow { display: flex; align-items: baseline; gap: 20px;
               margin-bottom: 24px; }
    .typerow span { font-weight: 900; color: var(--ink); line-height: 1;
                    letter-spacing: -0.03em; }
    .typerow span.a { font-size: 84px; }
    .typerow span.b { font-size: 52px; color: var(--accent); }
    .typerow span.c { font-size: 34px; color: rgba(23,20,28,0.45); }
    .elems { display: flex; gap: 18px; }
    .elems i { display: block; height: 62px; flex: 1; border-radius: 18px;
               background: var(--container); box-shadow: var(--rim); }
    .elems i:nth-child(2) { border-radius: 31px; }
    .elems i:nth-child(3) { flex: 0 0 62px; border-radius: 50%; }

    /* ---- numbers, steps, and the coffee ---- */
    .big { position: absolute; left: 0; width: 1080px; text-align: center;
           font-weight: 900; color: #fff; letter-spacing: -0.05em;
           line-height: 1; text-shadow: 0 18px 60px rgba(8,6,12,0.55); }
    .big small { font-size: 0.42em; }
    .step { position: absolute; width: 130px; height: 130px; border-radius: 50%;
            display: grid; place-items: center; background: var(--lit-accent);
            box-shadow: var(--rim-dark); filter: var(--cast); }
    .step span { font-size: 70px; font-weight: 900; color: #fff; line-height: 1; }
    .step.off { background: rgba(255,255,255,0.22); box-shadow: var(--rim); }

    .cup { position: absolute; left: 430px; top: 170px; width: 220px;
           height: 200px; }
    .cup .body { position: absolute; left: 0; bottom: 0; width: 176px;
                 height: 156px; border-radius: 20px 20px 46px 46px;
                 background: var(--lit-blush); box-shadow: var(--rim);
                 filter: var(--cast); }
    .cup .brew { position: absolute; left: 14px; bottom: 116px; width: 148px;
                 height: 26px; border-radius: 13px;
                 background: linear-gradient(160deg,#6b3b22,#3d1f10); }
    .cup .handle { position: absolute; right: 0; bottom: 56px; width: 62px;
                   height: 74px; border-radius: 0 40px 40px 0;
                   border: 16px solid var(--surface); border-left: 0; }
    .cup .steam { position: absolute; width: 14px; border-radius: 7px;
                  background: rgba(255,255,255,0.75); }

    /* ---- the mess the AI makes when you just ask it ---- */
    .junk { position: absolute; border-radius: 8px;
            background: rgba(23,20,28,0.30); }
""")

for _sel, _w, _h, _r in [
    (".slide", 620, 380, 40),
    (".tile.brand.prod", 250, 250, 60),
    (".dsys", 700, 420, 48),
]:
    k.squircle(_sel, _w, _h, _r)


# ------------------------------------------------------------------ A · hook


@beat
def b01_hate_making_them():
    """«я ненавиджу робити презентації… простіше імпровізувати, ніж сидіти і
    дизайнити кожен слайд»

    One slide, then the pile behind it. The verb is «this keeps coming».
    """
    html = '''
      <div class="g full" id="g1">
        %s
        %s
        %s
        <div class="venues" id="g1v">
          <span id="g1v0"></span><span id="g1v1"></span><span id="g1v2"></span>
        </div>
      </div>''' % (
        wire("g1a", style="left:230px;top:110px"),
        wire("g1b", style="left:230px;top:110px"),
        wire("g1c", style="left:230px;top:110px"))
    js = '''
  gsap.set("#g1", {autoAlpha: 0});
  gsap.set("#g1a, #g1b, #g1c", {autoAlpha: 0, transformOrigin: "50% 50%"});
  tl.set("#g1", {autoAlpha: 1}, 1.50);
  gsap.set("#g1v span", {autoAlpha: 0, scale: 0.5,
                         transformOrigin: "50% 50%"});
  tl.fromTo("#g1a", {scale: 0.84, y: 0, rotation: 0},
            {autoAlpha: 1, scale: 1, duration: 0.32, ease: "back.out(2.4)"}, 1.64);
  // «для вебінарів, майстеркласів і виступів» — three of them, one per word,
  // so the slide is not just sitting there for six seconds
  [3.30, 4.06, 4.94].forEach(function (t, i) {
    tl.to("#g1v" + i, {autoAlpha: 1, scale: 1, duration: 0.26,
                       ease: "back.out(2.6)"}, t);
  });
  // «простіше імпровізувати, ніж сидіти і дизайнити» — the whole lot sags
  tl.to("#g1v span", {autoAlpha: 0.3, duration: 0.34}, 6.30);
  // «кожен слайд» — and another, and another
  tl.fromTo("#g1b", {scale: 0.9, x: 0, y: 0, rotation: 0},
            {autoAlpha: 1, x: 46, y: 40, rotation: 2.4, duration: 0.30,
             ease: "back.out(2)"}, 8.78);
  tl.fromTo("#g1c", {scale: 0.9, x: 0, y: 0, rotation: 0},
            {autoAlpha: 1, x: -44, y: 78, rotation: -2.2, duration: 0.30,
             ease: "back.out(2)"}, 9.04);
  tl.to("#g1", {autoAlpha: 0, duration: 0.28, ease: "power2.in"}, 10.30);'''
    return html, js


@beat
def b02_ai_makes_junk():
    """«пробувала робити презентації зі штучним інтелектом… виходить трошки
    гімняно: розкидає інформацію по слайду»

    The AI fills a slide instantly and the filling is garbage — text thrown at
    the page at angles, overlapping, no order.
    """
    junk = "".join(
        '<span class="junk" id="g2j%d" style="left:%dpx;top:%dpx;width:%dpx;'
        'height:%dpx;transform:rotate(%sdeg)"></span>'
        % (i, x, y, w, h, r) for i, (x, y, w, h, r) in enumerate([
            (64, 52, 300, 22, "-7"), (300, 96, 230, 20, "5"),
            (48, 150, 400, 24, "3"), (250, 196, 180, 18, "-9"),
            (96, 232, 330, 20, "6"), (330, 262, 210, 22, "-4"),
            (60, 292, 260, 18, "8"),
        ]))
    html = '''
      <div class="g full" id="g2">
        %s
        <div class="slide" id="g2s" style="left:230px;top:110px">
          <div class="junkwrap" id="g2j">%s</div>
        </div>
        <div class="nope" id="g2x"></div>
      </div>''' % ("", junk)
    js = '''
  gsap.set("#g2", {autoAlpha: 0});
  gsap.set("#g2s", {autoAlpha: 0, scale: 0.86, transformOrigin: "50% 50%"});
  gsap.set("#g2 .junk", {autoAlpha: 0, scale: 0.6, transformOrigin: "50% 50%"});
  gsap.set("#g2x", {autoAlpha: 0, scale: 0.4, rotation: -20,
                    transformOrigin: "50% 50%"});
  tl.set("#g2", {autoAlpha: 1}, 11.44);
  // «зі штучним інтелектом» — it arrives instantly and already full, because
  // the speed is the appeal and an empty slide here says nothing
  tl.to("#g2s", {autoAlpha: 1, scale: 1, duration: 0.28, ease: "back.out(2.4)"}, 11.58);
  tl.to("#g2 .junk", {autoAlpha: 1, scale: 1, duration: 0.18,
                      ease: "back.out(2)",
                      stagger: {each: 0.035, from: "start"}}, 11.74);
  // «розкидує якусь інформацію по слайду» — and it reshuffles into worse.
  // The offsets are baked from a seeded PRNG at build time, not rolled by GSAP:
  // `random()` re-rolls at tween init and every render worker initialises
  // independently, so the same frame would come out differently twice.
  tl.to("#g2j0", {rotation: "+=0", x: "+=38", y: "+=5", duration: 0.44, ease: "power2.inOut"}, 18.04);
  tl.to("#g2j1", {rotation: "+=-6", x: "+=-23", y: "+=-7", duration: 0.44, ease: "power2.inOut"}, 18.06);
  tl.to("#g2j2", {rotation: "+=13", x: "+=-40", y: "+=3", duration: 0.44, ease: "power2.inOut"}, 18.08);
  tl.to("#g2j3", {rotation: "+=2", x: "+=19", y: "+=-13", duration: 0.44, ease: "power2.inOut"}, 18.10);
  tl.to("#g2j4", {rotation: "+=-4", x: "+=30", y: "+=-16", duration: 0.44, ease: "power2.inOut"}, 18.12);
  tl.to("#g2j5", {rotation: "+=9", x: "+=8", y: "+=-8", duration: 0.44, ease: "power2.inOut"}, 18.14);
  tl.to("#g2j6", {rotation: "+=8", x: "+=17", y: "+=9", duration: 0.44, ease: "power2.inOut"}, 18.16);
  // «гімняно» lands earlier than the mess: the verdict first, then the reason
  tl.to("#g2x", {autoAlpha: 1, scale: 1, rotation: 0, duration: 0.32,
                 ease: "back.out(2.8)"}, 14.12);
  tl.to("#g2x", {autoAlpha: 0, scale: 0.8, duration: 0.22}, 17.60);
  tl.to("#g2", {autoAlpha: 0, duration: 0.28, ease: "power2.in"}, 20.90);'''
    return html, js


@beat
def b03_three_steps():
    """«гарні презентації реально зробити, просто тут є декілька кроків»"""
    html = '''
      <div class="g full" id="g3">
        <div class="step" id="g3s0" style="left:280px;top:230px"><span>1</span></div>
        <div class="step" id="g3s1" style="left:475px;top:230px"><span>2</span></div>
        <div class="step" id="g3s2" style="left:670px;top:230px"><span>3</span></div>
      </div>'''
    js = '''
  gsap.set("#g3", {autoAlpha: 0});
  gsap.set("#g3 .step", {autoAlpha: 0, scale: 0.5, transformOrigin: "50% 50%"});
  tl.set("#g3", {autoAlpha: 1}, 24.86);
  [25.00, 25.16, 25.32].forEach(function (t, i) {
    tl.to("#g3s" + i, {autoAlpha: 1, scale: 1, duration: 0.30,
                       ease: "back.out(2.6)"}, t);
  });
  tl.to("#g3", {autoAlpha: 0, duration: 0.26, ease: "power2.in"}, 26.10);'''
    return html, js


@beat
def b04_clients_and_speed():
    """«робила не тільки собі, а й клієнтам… і тим, як швидко це відбувається»

    Several finished decks, then the clock that makes them cheap.
    """
    html = '''
      <div class="g full" id="g4">
        <div class="decks" id="g4d">
          <span style="left:0px;top:36px"></span>
          <span style="left:186px;top:12px"></span>
          <span style="left:372px;top:36px"></span>
          <span style="left:558px;top:12px"></span>
        </div>
        <svg id="g4c" width="230" height="230" viewBox="0 0 230 230"
             style="position:absolute;left:425px;top:150px">
          <circle cx="115" cy="115" r="96" fill="rgba(23,20,28,0.40)"/>
          <circle cx="115" cy="115" r="96" fill="none"
                  stroke="rgba(255,255,255,0.6)" stroke-width="13"/>
          <line id="g4h" x1="115" y1="115" x2="115" y2="42" stroke="#ff6e9c"
                stroke-width="15" stroke-linecap="round"/>
          <circle cx="115" cy="115" r="12" fill="#fff"/>
        </svg>
      </div>'''
    js = '''
  gsap.set("#g4", {autoAlpha: 0});
  gsap.set("#g4d span", {autoAlpha: 0, scale: 0.7, transformOrigin: "50% 50%"});
  gsap.set("#g4c", {autoAlpha: 0, scale: 0.7, transformOrigin: "50% 50%"});
  tl.set("#g4", {autoAlpha: 1}, 26.20);
  // «не тільки собі, а й клієнтам»
  tl.to("#g4d span", {autoAlpha: 1, scale: 1, duration: 0.28,
                      ease: "back.out(2.2)", stagger: 0.09}, 26.34);
  // «і всі максимально задоволені» — each one gets its tick
  tl.to("#g4d span", {backgroundImage:
        "linear-gradient(115deg, #ff8ab0 0%, #ff5c8f 100%)",
        duration: 0.22, stagger: 0.07}, 29.64);
  tl.to("#g4d", {autoAlpha: 0, duration: 0.26, ease: "power2.in"}, 31.40);
  // «як швидко це відбувається» — one fast sweep, and it is over
  tl.to("#g4c", {autoAlpha: 1, scale: 1, duration: 0.26, ease: "back.out(2.4)"}, 32.06);
  tl.to("#g4h", {rotation: 360, svgOrigin: "115 115", duration: 0.60,
                 ease: "power2.inOut"}, 32.24);
  tl.to("#g4", {autoAlpha: 0, duration: 0.26, ease: "power2.in"}, 33.60);'''
    return html, js


@beat
def b05_same_day():
    """«робила презентацію прямо в день майстер-класу — і не просто встигла, а
    ще й лишилось кілька годин»

    A deadline bar that fills and stops well short of the line.
    """
    html = '''
      <div class="g full" id="g5">
        <div class="deadline" id="g5d">
          <span class="track"></span>
          <span class="fill" id="g5f"></span>
          <span class="line"></span>
          <span class="slack" id="g5s"></span>
        </div>
      </div>'''
    js = '''
  gsap.set("#g5", {autoAlpha: 0});
  gsap.set("#g5d", {autoAlpha: 0});
  gsap.set("#g5f", {scaleX: 0, transformOrigin: "0% 50%"});
  gsap.set("#g5s", {autoAlpha: 0, scaleX: 0, transformOrigin: "100% 50%"});
  tl.set("#g5", {autoAlpha: 1}, 35.66);
  tl.to("#g5d", {autoAlpha: 1, duration: 0.22}, 35.78);
  // «встигла» — the work fills the bar
  tl.to("#g5f", {scaleX: 1, duration: 0.70, ease: "power2.out"}, 37.44);
  // «ще й лишилось кілька годин» — and there is room left over
  tl.to("#g5s", {autoAlpha: 1, scaleX: 1, duration: 0.40, ease: "power3.out"}, 38.98);
  tl.to("#g5", {autoAlpha: 0, duration: 0.26, ease: "power2.in"}, 40.60);'''
    return html, js


# -------------------------------------------------------- B · step 1, the skeleton


@beat
def b06_step_one_tools():
    """«перший крок — відкриваєш канву або гугл презентації»"""
    html = '''
      <div class="g full" id="g6">
        <div class="step" id="g6n" style="left:475px;top:70px"><span>1</span></div>
        %s
        %s
      </div>''' % (
        marktile("g6a", "canva-mark", style="left:230px;top:250px"),
        marktile("g6b", "gslides-mark", style="left:600px;top:250px"))
    js = '''
  gsap.set("#g6", {autoAlpha: 0});
  gsap.set("#g6n, #g6a, #g6b", {autoAlpha: 0, scale: 0.6,
                                transformOrigin: "50% 50%"});
  tl.set("#g6", {autoAlpha: 1}, 41.72);
  tl.to("#g6n", {autoAlpha: 1, scale: 1, duration: 0.30, ease: "back.out(2.8)"}, 41.86);
  tl.to("#g6a", {autoAlpha: 1, scale: 1, duration: 0.30, ease: "back.out(2.4)"}, 42.96);
  tl.to("#g6b", {autoAlpha: 1, scale: 1, duration: 0.30, ease: "back.out(2.4)"}, 43.58);
  tl.to("#g6", {autoAlpha: 0, duration: 0.26, ease: "power2.in"}, 45.30);'''
    return html, js


@beat
def b07_skeleton_built():
    """«накидаєш скелет: що має бути на кожному слайді… загальні сенси… якщо
    хочеш картинку чи графік, просто прописуєш збоку»

    The wireframe writes itself, one part per phrase. This is the object the
    whole reel is about, so it is built in front of the viewer rather than
    arriving finished.
    """
    html = '''
      <div class="g full" id="g7">
        %s
      </div>''' % wire("g7s", rows=4, pic=True, chart=True,
                       style="left:230px;top:130px")
    js = '''
  gsap.set("#g7", {autoAlpha: 0});
  gsap.set("#g7s", {autoAlpha: 0, scale: 0.88, transformOrigin: "50% 50%"});
  gsap.set("#g7s .wh, #g7s .wr", {scaleX: 0, transformOrigin: "0% 50%"});
  gsap.set("#g7s .wpic, #g7s .wchart", {autoAlpha: 0, scale: 0.7,
                                        transformOrigin: "50% 50%"});
  tl.set("#g7", {autoAlpha: 1}, 45.50);
  // «накидаєш скелет»
  tl.to("#g7s", {autoAlpha: 1, scale: 1, duration: 0.30, ease: "back.out(2.2)"}, 45.66);
  tl.to("#g7s .wh", {scaleX: 1, duration: 0.26, ease: "power2.out"}, 45.90);
  // «що має бути на кожному слайді»
  tl.to("#g7s .wr", {scaleX: 1, duration: 0.24, stagger: 0.10,
                     ease: "power2.out"}, 47.34);
  // «загальні сенси» — the body thickens
  tl.to("#g7s .wr", {scaleY: 1.25, duration: 0.22, ease: "power2.out"}, 48.72);
  // «якщо хочеш картинку чи графік — прописуєш збоку»
  tl.to("#g7s .wpic", {autoAlpha: 1, scale: 1, duration: 0.28,
                       ease: "back.out(2.4)"}, 51.16);
  tl.to("#g7s .wpic", {autoAlpha: 0, duration: 0.18}, 51.66);
  tl.to("#g7s .wchart", {autoAlpha: 1, scale: 1, duration: 0.28,
                         ease: "back.out(2.4)"}, 51.72);
  tl.to("#g7", {autoAlpha: 0, duration: 0.24, ease: "power2.in"}, 54.90);'''
    return html, js


@beat
def b08_black_and_white():
    """«в результаті маєш чорно-білий скелет: текст на білому фоні, без жодного
    дизайну»

    The same slide, stated plainly. No colour anywhere — which is the setup for
    the payoff, so it has to be seen properly before Claude touches it.
    """
    html = '''
      <div class="g full" id="g8">
        %s
      </div>''' % wire("g8s", rows=4, chart=True, style="left:230px;top:130px")
    js = '''
  gsap.set("#g8", {autoAlpha: 0});
  gsap.set("#g8s", {autoAlpha: 0, scale: 0.9, transformOrigin: "50% 50%"});
  tl.set("#g8", {autoAlpha: 1}, 55.36);
  tl.to("#g8s", {autoAlpha: 1, scale: 1, duration: 0.30, ease: "back.out(2.2)"}, 55.50);
  // «на білому фоні» — it is a white rectangle and nothing else
  tl.to("#g8s", {boxShadow: "0 0 0 0 rgba(0,0,0,0)", duration: 0.30}, 57.32);
  // «без жодного дизайну» — a small, deliberate nothing
  tl.to("#g8s", {scale: 0.96, duration: 0.30, ease: "power2.out"}, 58.10);
  tl.to("#g8", {autoAlpha: 0, duration: 0.24, ease: "power2.in"}, 59.60);'''
    return html, js


# ------------------------------------------------ C · step 2, the design system


@beat
def b09_claude_two_steps():
    """«береш цей скелет і йдеш у Клод дизайн, і тут уже два кроки»"""
    html = '''
      <div class="g full" id="g9">
        %s
        <div class="step off" id="g9a" style="left:400px;top:400px"><span>1</span></div>
        <div class="step off" id="g9b" style="left:560px;top:400px"><span>2</span></div>
      </div>''' % marktile("g9t", "claude-tile", style="left:415px;top:110px")
    js = '''
  gsap.set("#g9", {autoAlpha: 0});
  gsap.set("#g9t", {autoAlpha: 0, scale: 0.7, transformOrigin: "50% 50%"});
  gsap.set("#g9a, #g9b", {autoAlpha: 0, scale: 0.5, transformOrigin: "50% 50%"});
  tl.set("#g9", {autoAlpha: 1}, 61.14);
  tl.to("#g9t", {autoAlpha: 1, scale: 1, duration: 0.32, ease: "back.out(2.4)"}, 61.28);
  // «два кроки»
  tl.to("#g9a", {autoAlpha: 1, scale: 1, duration: 0.26, ease: "back.out(2.6)"}, 63.22);
  tl.to("#g9b", {autoAlpha: 1, scale: 1, duration: 0.26, ease: "back.out(2.6)"}, 63.42);
  tl.to("#g9", {autoAlpha: 0, duration: 0.24, ease: "power2.in"}, 64.50);'''
    return html, js


@beat
def b10_style_or_pinterest():
    """«якщо в тебе є розуміння свого стилю — описуєш його. Якщо ні — йдеш у
    Pinterest, робиш скріншоти того, що тобі подобається»

    Two routes to the same place. The Pinterest one gets the screenshots
    flying in, because that is the branch most people take.
    """
    html = '''
      <div class="g full" id="g10">
        <div class="dsys empty" id="g10d" style="left:230px;top:250px">
          <div class="swatches"><i></i><i></i><i></i><i></i></div>
        </div>
        %s
        <div class="shots" id="g10s">
          <span style="left:120px;top:80px"><i></i><b></b></span>
          <span style="left:300px;top:44px"><i></i><b></b></span>
          <span style="left:480px;top:86px"><i></i><b></b></span>
          <span style="left:660px;top:50px"><i></i><b></b></span>
        </div>
      </div>''' % marktile("g10p", "pinterest-mark", style="left:415px;top:60px")
    js = '''
  gsap.set("#g10", {autoAlpha: 0});
  gsap.set("#g10p", {autoAlpha: 0, scale: 0.7, transformOrigin: "50% 50%"});
  gsap.set("#g10s span", {autoAlpha: 0, scale: 0.6, transformOrigin: "50% 50%"});
  gsap.set("#g10d", {autoAlpha: 0, scale: 0.9, transformOrigin: "50% 50%"});
  tl.set("#g10", {autoAlpha: 1}, 67.04);
  // «розуміння свого стилю» — you already have it, so it lands straight away
  tl.to("#g10d", {autoAlpha: 1, scale: 1, duration: 0.30, ease: "back.out(2.2)"}, 67.18);
  tl.to("#g10d", {autoAlpha: 0, duration: 0.22, ease: "power2.in"}, 68.80);
  // «йдеш у Pinterest, робиш скріншоти»
  tl.to("#g10p", {autoAlpha: 1, scale: 1, duration: 0.30, ease: "back.out(2.4)"}, 69.28);
  tl.to("#g10s span", {autoAlpha: 1, scale: 1, duration: 0.26,
                       ease: "back.out(2.2)", stagger: 0.08}, 70.02);
  // «і відправляєш туди» — they go up into it
  tl.to("#g10s span", {y: -180, autoAlpha: 0, duration: 0.46,
                       ease: "power2.in", stagger: 0.05}, 71.00);
  tl.to("#g10", {autoAlpha: 0, duration: 0.24, ease: "power2.in"}, 72.10);'''
    return html, js


@beat
def b11_five_minutes():
    """«хвилин через п'ять»"""
    html = '''
      <div class="g full" id="g11">
        <div class="big" id="g11n" style="top:190px;font-size:230px">5<small> хв</small></div>
      </div>'''
    js = '''
  gsap.set("#g11", {autoAlpha: 0});
  gsap.set("#g11n", {autoAlpha: 0, scale: 0.6, transformOrigin: "50% 50%"});
  tl.set("#g11", {autoAlpha: 1}, 72.40);
  tl.to("#g11n", {autoAlpha: 1, scale: 1, duration: 0.34, ease: "back.out(2.8)"}, 72.52);
  tl.to("#g11", {autoAlpha: 0, duration: 0.22, ease: "power2.in"}, 74.00);'''
    return html, js


@beat
def b12_system_fills():
    """«готову дизайн-систему з кольорами, шрифтами, елементами — коротше,
    брендбук — і вона працює не тільки для презентацій»

    One part per word, which is four words in 2.1 s, so they land fast and
    uneven. §4: put every element on its word.
    """
    html = '''
      <div class="g full" id="g12">
        <div class="dsys" id="g12d">
          <div class="swatches" id="g12c"><i></i><i></i><i></i><i></i></div>
          <div class="typerow" id="g12t">
            <span class="a">Aa</span><span class="b">Aa</span><span class="c">Aa</span>
          </div>
          <div class="elems" id="g12e"><i></i><i></i><i></i></div>
        </div>
      </div>'''
    js = '''
  gsap.set("#g12", {autoAlpha: 0});
  gsap.set("#g12d", {autoAlpha: 0, scale: 0.9, transformOrigin: "50% 40%"});
  gsap.set("#g12c i", {autoAlpha: 0, scale: 0.5, transformOrigin: "50% 50%"});
  gsap.set("#g12t span", {autoAlpha: 0, y: 24});
  gsap.set("#g12e i", {autoAlpha: 0, scaleX: 0.4, transformOrigin: "50% 50%"});
  tl.set("#g12", {autoAlpha: 1}, 74.34);
  tl.to("#g12d", {autoAlpha: 1, scale: 1, duration: 0.30, ease: "back.out(2.2)"}, 74.46);
  // «кольорами»
  tl.to("#g12c i", {autoAlpha: 1, scale: 1, duration: 0.24, ease: "back.out(2.4)",
                    stagger: 0.05}, 75.36);
  // «шрифтами»
  tl.to("#g12t span", {autoAlpha: 1, y: 0, duration: 0.24, ease: "power3.out",
                       stagger: 0.06}, 75.96);
  // «елементами»
  tl.to("#g12e i", {autoAlpha: 1, scaleX: 1, duration: 0.24, ease: "back.out(2.4)",
                    stagger: 0.05}, 76.48);
  // «коротше, брендбук» — the whole thing is one object now
  tl.to("#g12d", {scale: 0.94, duration: 0.34, ease: "power2.out"}, 77.50);
  tl.to("#g12", {autoAlpha: 0, duration: 0.26, ease: "power2.in"}, 80.90);'''
    return html, js


# --------------------------------------------------- D · step 3, and the payoff


@beat
def b13_upload_and_ask():
    """«повертаєшся у вкладку дизайни, обираєш презентацію, завантажуєш свій
    скелет… ось мій файл, ось моя дизайн система, зроби гарно»
    """
    html = '''
      <div class="g full" id="g13">
        <div class="tabs" id="g13t">
          <span></span><span class="on"></span><span></span>
        </div>
        %s
        <div class="prompt" id="g13p">
          <b></b><b></b><span class="send"></span>
        </div>
      </div>''' % wire("g13s", rows=3, style="left:230px;top:170px")
    js = '''
  gsap.set("#g13", {autoAlpha: 0});
  gsap.set("#g13t", {autoAlpha: 0});
  gsap.set("#g13s", {autoAlpha: 0, scale: 0.8, y: 60, transformOrigin: "50% 50%"});
  gsap.set("#g13p", {autoAlpha: 0, y: 30});
  gsap.set("#g13p b", {scaleX: 0, transformOrigin: "0% 50%"});
  tl.set("#g13", {autoAlpha: 1}, 83.56);
  // «вкладка дизайни»
  tl.to("#g13t", {autoAlpha: 1, duration: 0.24}, 83.70);
  // «обираєш презентацію»
  tl.to("#g13t span.on", {scaleY: 1.18, duration: 0.24, ease: "back.out(3)",
                          transformOrigin: "50% 100%"}, 84.88);
  // «завантажуєш свій скелет» — the same object from step 1, going in
  tl.to("#g13s", {autoAlpha: 1, scale: 0.8, y: 0, duration: 0.36,
                  ease: "back.out(2.2)"}, 85.64);
  // «ось мій файл, ось моя дизайн система»
  tl.to("#g13p", {autoAlpha: 1, y: 0, duration: 0.26}, 89.08);
  tl.to("#g13p b:nth-child(1)", {scaleX: 1, duration: 0.22,
                                 ease: "power2.out"}, 89.12);
  tl.to("#g13p b:nth-child(2)", {scaleX: 1, duration: 0.22,
                                 ease: "power2.out"}, 90.28);
  // «зроби гарно» — and send
  tl.to("#g13p .send", {scale: 1.25, duration: 0.18, ease: "back.out(3)",
                        transformOrigin: "50% 50%"}, 91.18);
  tl.to("#g13p .send", {scale: 1, duration: 0.22}, 91.38);
  tl.to("#g13", {autoAlpha: 0, duration: 0.26, ease: "power2.in"}, 92.40);'''
    return html, js


@beat
def b14_coffee():
    """«відправляєш і йдеш пити каву»"""
    html = '''
      <div class="g full" id="g14">
        <div class="cup" id="g14c">
          <span class="steam" id="g14s1" style="left:38px;bottom:170px;height:44px"></span>
          <span class="steam" id="g14s2" style="left:78px;bottom:178px;height:56px"></span>
          <span class="steam" id="g14s3" style="left:118px;bottom:170px;height:44px"></span>
          <span class="handle"></span>
          <span class="body"></span>
          <span class="brew"></span>
        </div>
      </div>'''
    js = '''
  gsap.set("#g14", {autoAlpha: 0});
  gsap.set("#g14c", {autoAlpha: 0, scale: 0.7, transformOrigin: "50% 100%"});
  gsap.set("#g14 .steam", {autoAlpha: 0, scaleY: 0.3,
                           transformOrigin: "50% 100%"});
  tl.set("#g14", {autoAlpha: 1}, 93.04);
  tl.to("#g14c", {autoAlpha: 1, scale: 1, duration: 0.34, ease: "back.out(2.4)"}, 93.18);
  tl.to("#g14 .steam", {autoAlpha: 1, scaleY: 1, duration: 0.40,
                        ease: "power2.out", stagger: 0.10}, 93.50);
  tl.to("#g14", {autoAlpha: 0, duration: 0.24, ease: "power2.in"}, 94.70);'''
    return html, js


@beat
def b15_it_is_done():
    """«через п'ять-десять хвилин у тебе вже готова гарно задизайнена
    презентація, яку хіба трошки підправити»

    The payoff. Same slide, same geometry, dressed — so the viewer reads it as
    the thing they watched get built, not a new object.
    """
    html = '''
      <div class="g full" id="g15">
        <div class="big" id="g15n" style="top:120px;font-size:150px">5-10<small> хв</small></div>
        %s
        <div class="tweak" id="g15t"></div>
      </div>''' % wire("g15s", "done", rows=4, pic=True,
                       style="left:230px;top:140px")
    js = '''
  gsap.set("#g15", {autoAlpha: 0});
  gsap.set("#g15n", {autoAlpha: 0, scale: 0.6, transformOrigin: "50% 50%"});
  gsap.set("#g15s", {autoAlpha: 0, scale: 0.86, transformOrigin: "50% 50%"});
  gsap.set("#g15t", {autoAlpha: 0, scale: 0.4, transformOrigin: "50% 50%"});
  tl.set("#g15", {autoAlpha: 1}, 94.76);
  // «п'ять-десять хвилин»
  tl.to("#g15n", {autoAlpha: 1, scale: 1, duration: 0.32, ease: "back.out(2.8)"}, 94.88);
  tl.to("#g15n", {autoAlpha: 0, y: -60, duration: 0.30, ease: "power2.in"}, 96.30);
  // «гарно задизайнена презентація» — the skeleton, finished
  tl.to("#g15s", {autoAlpha: 1, scale: 1, duration: 0.40, ease: "back.out(2.2)"}, 96.64);
  // «хіба що трошки підправити» — one small nudge, and that is all
  tl.to("#g15t", {autoAlpha: 1, scale: 1, duration: 0.26, ease: "back.out(2.8)"}, 100.02);
  tl.to("#g15", {autoAlpha: 0, duration: 0.28, ease: "power2.in"}, 101.30);'''
    return html, js


@beat
def b16_subscribe():
    """«якщо тобі було корисно — обов'язково підпишись»

    Her last shot is framed closer, so this sits low and small rather than over
    her face (STYLE.md §3).
    """
    html = '''
      <div class="g full" id="g16">
        <div class="plus" id="g16p"><i></i><i></i></div>
      </div>'''
    js = '''
  gsap.set("#g16", {autoAlpha: 0});
  gsap.set("#g16p", {autoAlpha: 0, scale: 0.4, rotation: -90,
                     transformOrigin: "50% 50%"});
  tl.set("#g16", {autoAlpha: 1}, 102.08);
  tl.to("#g16p", {autoAlpha: 1, scale: 1, rotation: 0, duration: 0.34,
                  ease: "back.out(2.8)"}, 102.20);
  tl.to("#g16p", {scale: 1.06, duration: 0.36, ease: "power2.inOut"}, 102.66);
  tl.to("#g16p", {scale: 1, duration: 0.20, ease: "power2.out"}, 103.04);'''
    return html, js


k.css("""
    /* b02 — the verdict on what the AI produced unaided */
    .junkwrap { position: absolute; inset: 0; }
    .nope { position: absolute; z-index: 3; left: 430px; top: 210px; width: 220px;
            height: 220px; border-radius: 50%; background: var(--lit-accent);
            box-shadow: var(--rim-dark); filter: var(--cast); }
    .nope::before, .nope::after { content: ""; position: absolute; left: 50px;
            top: 100px; width: 120px; height: 20px; border-radius: 10px;
            background: #fff; }
    .nope::before { transform: rotate(45deg); }
    .nope::after { transform: rotate(-45deg); }

    /* b04 — decks she has already made */
    .decks { position: absolute; left: 150px; top: 200px; width: 780px;
             height: 200px; }
    .decks span { position: absolute; width: 150px; height: 106px;
                  border-radius: 18px; background: var(--lit-blush);
                  box-shadow: var(--rim); filter: var(--cast-sm); }

    /* b05 — the deadline, and the room she had left */
    .deadline { position: absolute; left: 150px; top: 250px; width: 780px;
                height: 60px; }
    .deadline .track { position: absolute; left: 0; top: 16px; width: 100%;
                       height: 28px; border-radius: 14px;
                       background: rgba(255,255,255,0.28); }
    .deadline .fill { position: absolute; left: 0; top: 16px; width: 74%;
                      height: 28px; border-radius: 14px;
                      background: var(--lit-accent); box-shadow: var(--rim-dark); }
    .deadline .line { position: absolute; right: 0; top: 0; width: 12px;
                      height: 60px; border-radius: 6px; background: #fff; }
    .deadline .slack { position: absolute; right: 12px; top: 16px; width: 26%;
                       height: 28px; border-radius: 14px;
                       background: var(--lit-pink); }

    /* b10 — what you send it if you have no style of your own */
    .shots { position: absolute; left: 150px; top: 300px; width: 780px;
             height: 200px; }
    .shots span { position: absolute; width: 130px; height: 120px;
                  border-radius: 20px; background: var(--lit-blush);
                  box-shadow: var(--rim); filter: var(--cast-sm);
                  overflow: hidden; }
    .shots span i { position: absolute; left: 0; bottom: 0; width: 130px;
                    height: 58px; background: linear-gradient(160deg,#ff8ab0,#ff5c8f); }
    .shots span b { position: absolute; left: 16px; top: 18px; width: 64px;
                    height: 14px; border-radius: 7px; background: var(--accent); }
    .shots span:nth-child(2) i { background: linear-gradient(160deg,#c41434,#8d0d24); }
    .shots span:nth-child(3) i { background: linear-gradient(160deg,#ecc8d0,#f4dde2); }
    .shots span:nth-child(4) i { background: linear-gradient(160deg,#241f2c,#17141c); }
    /* not empty: if she already knows her style, the colours are the point */
    .dsys.empty { padding: 26px 34px; }

    /* b13 — the tab, and the thing you type into it */
    .tabs { position: absolute; left: 330px; top: 80px; width: 420px;
            display: flex; gap: 16px; }
    .tabs span { display: block; flex: 1; height: 54px; border-radius: 16px;
                 background: rgba(255,255,255,0.32); box-shadow: var(--rim); }
    .tabs span.on { background: var(--lit-accent); box-shadow: var(--rim-dark); }
    .prompt { position: absolute; left: 230px; top: 500px; width: 620px;
              padding: 26px 30px; border-radius: 34px;
              background: var(--lit-blush); box-shadow: var(--rim);
              filter: var(--cast); }
    .prompt b { display: block; height: 22px; border-radius: 11px;
                background: var(--graphite); margin-bottom: 16px; width: 82%; }
    .prompt b:nth-child(2) { width: 58%; }
    .prompt .send { position: absolute; right: 26px; bottom: 24px; width: 66px;
                    height: 66px; border-radius: 50%;
                    background: var(--lit-accent); box-shadow: var(--rim-dark); }

    /* b15 — the one tweak left to make */
    .tweak { position: absolute; left: 790px; top: 170px; width: 84px;
             height: 84px; border-radius: 50%; background: var(--lit-pink);
             box-shadow: var(--rim-dark);
             filter: drop-shadow(0 0 26px rgba(255,110,156,0.8)); }

    /* b01 — the three places she has to make these for */
    .venues { position: absolute; left: 230px; top: 420px; width: 620px;
              display: flex; gap: 20px; justify-content: center; }
    .venues span { display: block; width: 168px; height: 66px;
                   border-radius: 33px; background: var(--lit-accent);
                   box-shadow: var(--rim-dark); filter: var(--cast-sm); }

    /* b16 — subscribe */
    /* Her last shot is a closeup, so y 980 put this squarely on her cheek.
       STYLE.md 3: off her face, and in a closeup the only clear band is the
       very top of the frame. */
    .plus { position: absolute; left: 468px; top: 110px; width: 144px;
            height: 144px; border-radius: 44px; background: var(--lit-accent);
            box-shadow: var(--rim-dark); filter: var(--cast); }
    .plus i { position: absolute; left: 34px; top: 62px; width: 76px;
              height: 20px; border-radius: 10px; background: #fff; }
    .plus i:nth-child(2) { transform: rotate(90deg); }
""")

for _sel, _w, _h, _r in [
    (".prompt", 620, 150, 34),
    (".plus", 144, 144, 44),
]:
    k.squircle(_sel, _w, _h, _r)


def main():
    caps = k.load_captions(os.path.join(ROOT, "work", "r09", "captions.json"))
    gh, gj = [], []
    for fn in BEATS:
        h, j = fn()
        if h.strip():
            gh.append(h.rstrip())
        gj.append("  /* %s */" % fn.__name__)
        gj.append(j.rstrip())

    doc = k.document(
        title="Reel 9 — презентації",
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
