# -*- coding: utf-8 -*-
"""Reel 8 — «я витрачаю 130 євро кожного місяця на свій бізнес».

Variant B: her cut, graded, no subtitles. Materials from tools/kit.py
(STYLE.md §5a); what each beat depicts is invented for this script.

The recurring object is **the bill**. She opens with a total and then spends
the whole reel itemising it, so every product beat is one line of a receipt —
a mark and a price — and at the end the five lines assemble and add back up to
the number she opened with. STYLE.md §4 «reuse objects»: the total is the first
thing the viewer sees and the last, and the middle is the working.

Numbers carry this reel, which §4 allows explicitly — a quantity is not a word.
Four of the five products have no mark on the machine (ClickUp, Mojo, Google
Workspace, Gemini), so they are set as type, the answer STYLE.md §4a.2 gives
when an image would not be instantly legible. Swapping in real artwork later is
one <img> each.

usage: python build.py
"""
import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
from kit import Kit  # noqa: E402

DUR = 101.417          # 3043 plate frames / 30, rounded down: the renderer
                       # ceils DUR*fps, so asking for 3043.5 would emit 3044.
k = Kit(width=1080, height=1920, fps=30, duration=DUR)

BEATS = []


def beat(fn):
    BEATS.append(fn)
    return fn


# ---------------------------------------------------------------------------
# NO-PAINT ZONES — her own editing (STYLE.md §4a).
#
# tools/shots.py found 17 shots; three are comedy inserts. tools/pullouts.py
# found no zooms in this one.
#
#  18.10 – 19.10   big closeup, sipping — and it already carries HER OWN
#                  sticker, «фінансово грамотна квін👑». Two graphics arguing
#                  is worse than either alone, and hers is funnier.
#  62.30 – 63.25   extreme closeup, her hand
#  72.95 – 74.45   big closeup, cropped tight
NO_PAINT = [(18.10, 19.10), (62.30, 63.25), (72.95, 74.45)]


# ---------------------------------------------------------------- materials

def mark(name):
    return '<img class="mk" src="assets/logos/%s.png" alt="">' % name


def wordtile(tid, text, cls="", size=54):
    """A product with no artwork on the machine. STYLE.md §4a.2 — when the
    image would not be instantly legible, the word is the honest answer, and a
    wordmark *is* the logo (§5b already ships Fathom and Gamma that way)."""
    return ('<div class="tile brand prod %s" id="%s">'
            '<span class="wordmark" style="font-size:%dpx">%s</span></div>'
            % (cls, tid, size, text))


def marktile(tid, name, cls=""):
    return ('<div class="tile brand prod %s" id="%s">%s</div>'
            % (cls, tid, mark(name)))


def freebadge(bid):
    """«безкоштовна версія» — 0 €, the same badge as reel 7. A returning
    object costs nothing to read (STYLE.md §4)."""
    return ('<div class="freewrap" id="%s"><div class="lit soft"></div>'
            '<div class="free"><span>0</span><small>€</small></div></div>' % bid)


def price(pid, amount, unit="€", cls=""):
    return ('<div class="price %s" id="%s"><span>%s</span><small>%s</small></div>'
            % (cls, pid, amount, unit))


k.css("""
    /* ---- the number, which is what this reel is about ---- */
    .big { position: absolute; left: 0; width: 1080px; text-align: center;
           font-weight: 900; color: #fff; letter-spacing: -0.05em;
           text-shadow: 0 18px 60px rgba(8,6,12,0.55); line-height: 1; }
    .big small { font-size: 0.44em; letter-spacing: -0.02em; }

    /* ---- a product tile, and the price hanging off it ---- */
    .tile.brand.prod { position: absolute; width: 300px; height: 300px;
                       display: grid; place-items: center;
                       background: var(--lit-blush); }
    .tile.brand.prod .mk { width: 62%; height: auto; display: block;
                           max-height: 66%; object-fit: contain; }
    .wordmark { font-weight: 900; color: var(--accent); line-height: 1;
                letter-spacing: -0.045em; -webkit-text-stroke: 3px var(--accent); }

    .price { position: absolute; display: grid; place-items: center;
             grid-auto-flow: column; gap: 6px; height: 128px; padding: 0 34px;
             border-radius: 64px; background: var(--lit-accent);
             box-shadow: var(--rim-dark); filter: var(--cast); }
    .price span { font-size: 82px; font-weight: 900; color: #fff;
                  letter-spacing: -0.04em; line-height: 1; }
    .price small { font-size: 42px; font-weight: 900; color: #fff; }
    .price.ink { background: var(--lit-ink); }

    /* ---- the bill, assembled at the end ---- */
    .bill { position: absolute; left: 130px; top: 44px; width: 820px;
            padding: 26px 30px 30px; background: var(--lit-blush);
            box-shadow: var(--rim); filter: var(--cast); }
    .brow { display: flex; align-items: center; gap: 20px; height: 74px;
            border-bottom: 3px solid rgba(23,20,28,0.10); }
    .brow .bn { font-size: 40px; font-weight: 900; color: var(--ink);
                letter-spacing: -0.02em; white-space: nowrap; flex: 1; }
    .brow .bv { font-size: 46px; font-weight: 900; color: var(--accent);
                letter-spacing: -0.03em; white-space: nowrap; }
    .brow .bm { width: 46px; height: 46px; flex: none; border-radius: 12px;
                object-fit: contain; display: block; }
    .btot { display: flex; align-items: center; gap: 20px; height: 104px;
            margin-top: 12px; padding: 0 22px; border-radius: 22px;
            background: var(--lit-accent); box-shadow: var(--rim-dark); }
    .btot .bn { font-size: 42px; font-weight: 900; color: #fff; flex: 1; }
    .btot .bv { font-size: 62px; font-weight: 900; color: #fff;
                letter-spacing: -0.04em; }

    /* ---- «безкоштовна версія до посиніння» — the 0, reused from reel 7 ---- */
    .freewrap { position: absolute; left: 390px; top: 150px; width: 300px;
                height: 300px; }
    .free { position: absolute; inset: 0; display: grid; place-items: center;
            grid-auto-flow: column; gap: 4px; border-radius: 50%;
            background: var(--lit-accent); box-shadow: var(--rim-dark); }
    .free span { font-size: 168px; font-weight: 900; color: #fff;
                 letter-spacing: -0.06em; line-height: 1; }
    .free small { font-size: 76px; font-weight: 900; color: #fff; }

    /* ---- «купою різних платформ» ---- */
    .swarm { position: absolute; left: 60px; top: 60px; width: 960px;
             display: grid; gap: 18px; grid-template-columns: repeat(6, 1fr); }
    .swarm i { display: block; height: 132px; border-radius: 30px;
               background: rgba(255,255,255,0.62); box-shadow: var(--rim);
               filter: var(--cast-sm); }
    .swarm i.keep { background: var(--lit-accent); box-shadow: var(--rim-dark); }

    /* ---- «ліміт» — a bar that hits a ceiling ---- */
    .gauge { position: absolute; left: 280px; top: 90px; width: 520px;
             height: 400px; }
    .gauge .cap { position: absolute; left: 0; top: 0; width: 520px;
                  height: 22px; border-radius: 11px; background: var(--accent);
                  box-shadow: 0 0 40px rgba(180,18,47,0.7); }
    .gauge .fill { position: absolute; left: 150px; bottom: 0; width: 220px;
                   border-radius: 26px 26px 0 0; background: var(--lit-pink);
                   box-shadow: var(--rim-dark); }

    /* ---- «субтитри» and «вирізання пауз» ---- */
    .subs { position: absolute; left: 240px; top: 190px; width: 600px; }
    .subs b { display: block; height: 42px; border-radius: 21px;
              background: rgba(255,255,255,0.92); margin-bottom: 20px;
              box-shadow: var(--rim); }
    .subs b:nth-child(2) { width: 78%; }
    .subs b:nth-child(3) { width: 54%; }
    .gapwave { position: absolute; left: 150px; top: 230px; width: 780px;
               height: 180px; display: flex; align-items: center; gap: 10px; }
    .gapwave i { display: block; width: 16px; border-radius: 8px;
                 background: var(--pink); }
    .gapwave i.dead { background: rgba(255,255,255,0.28); }

    /* ---- «українською мовою» — STYLE.md §4, the one sanctioned departure
           from the palette, because a flag has to be its own colours ---- */
    .flag { position: absolute; left: 315px; top: 180px; width: 450px;
            height: 300px; border-radius: 26px; overflow: hidden;
            box-shadow: var(--rim); filter: var(--cast); }
    .flag i { position: absolute; left: 0; width: 450px; height: 150px; }
    .flag i.b { top: 0; background: linear-gradient(160deg,#4d8ff0,#0057b7); }
    .flag i.y { top: 150px; background: linear-gradient(160deg,#ffdf4f,#ffd700); }
""")

# §5a.1 — squircle the LARGE surfaces only; the budget that turns a render
# black counts elements, and small repeated ones keep a plain border-radius.
for _sel, _w, _h, _r in [
    (".tile.brand.prod", 300, 300, 72),
    (".bill", 820, 560, 54),
]:
    k.squircle(_sel, _w, _h, _r)


# ------------------------------------------------------------------ A · hook


@beat
def b01_the_number():
    """«Я витрачаю 130 євро кожного місяця на свій бізнес»

    Open on the total. The whole reel is the working behind it, so it is the
    first thing on screen and the last.
    """
    html = '''
      <div class="g full" id="g1">
        <div class="big" id="g1n" style="top:150px;font-size:280px">130<small>€</small></div>
      </div>'''
    js = '''
  gsap.set("#g1", {autoAlpha: 0});
  gsap.set("#g1n", {autoAlpha: 0, scale: 0.55, transformOrigin: "50% 50%"});
  gsap.set("#g1n small", {autoAlpha: 0});
  tl.set("#g1", {autoAlpha: 1}, 1.22);
  tl.to("#g1n", {autoAlpha: 1, scale: 1, duration: 0.40, ease: "back.out(2.8)"}, 1.32);
  // «євро» — the unit arrives on its own word
  tl.to("#g1n small", {autoAlpha: 1, duration: 0.22, ease: "back.out(3)"}, 2.12);
  tl.to("#g1", {autoAlpha: 0, duration: 0.26, ease: "power2.in"}, 5.10);'''
    return html, js


@beat
def b02_where_it_goes():
    """«і ось куди йдуть ці гроші» — the total splits and falls into slots."""
    html = '''
      <div class="g full" id="g2">
        <div class="slots" id="g2s">
          <i></i><i></i><i></i><i></i><i></i>
        </div>
      </div>'''
    js = '''
  gsap.set("#g2", {autoAlpha: 0});
  gsap.set("#g2s i", {autoAlpha: 0, y: -90, scaleY: 0.4,
                      transformOrigin: "50% 0%"});
  tl.set("#g2", {autoAlpha: 1}, 6.70);
  tl.to("#g2s i", {autoAlpha: 1, y: 0, scaleY: 1, duration: 0.34,
                   ease: "back.out(2)", stagger: 0.07}, 6.88);
  tl.to("#g2", {autoAlpha: 0, duration: 0.26, ease: "power2.in"}, 8.60);'''
    return html, js


@beat
def b03_tightfisted():
    """«я людина, яка не дуже любить витрачати гроші»

    A coin is pulled back rather than handed over. The verb is «not spend».
    """
    html = '''
      <div class="g full" id="g3">
        <div class="coin" id="g3c"><span>€</span></div>
      </div>'''
    js = '''
  gsap.set("#g3", {autoAlpha: 0});
  gsap.set("#g3c", {autoAlpha: 0, scale: 0.6, x: 0, transformOrigin: "50% 50%"});
  tl.set("#g3", {autoAlpha: 1}, 8.90);
  tl.to("#g3c", {autoAlpha: 1, scale: 1, duration: 0.30, ease: "back.out(2.4)"}, 9.06);
  // «не дуже люблю витрачати» — it starts to go, and comes straight back
  tl.to("#g3c", {x: 230, duration: 0.34, ease: "power2.out"}, 9.54);
  tl.to("#g3c", {x: 0, duration: 0.44, ease: "back.out(2.2)"}, 9.92);
  tl.to("#g3", {autoAlpha: 0, duration: 0.26, ease: "power2.in"}, 11.20);'''
    return html, js


@beat
def b04_free_forever():
    """«буду сидіти на безкоштовній версії до посиніння»

    The 0 €, and it refuses to move. Same badge as reel 7 — it means the same
    thing and a returning object costs nothing to read (§4).
    Clears before 18.10: her own sticker owns that insert.
    """
    html = '''
      <div class="g full" id="g4">
        %s
      </div>''' % freebadge("g4free")
    js = '''
  gsap.set("#g4", {autoAlpha: 0});
  gsap.set("#g4free", {autoAlpha: 0, scale: 0.5, transformOrigin: "50% 50%"});
  tl.set("#g4", {autoAlpha: 1}, 16.48);
  tl.to("#g4free", {autoAlpha: 1, scale: 1, duration: 0.34, ease: "back.out(2.8)"}, 16.60);
  // «до посиніння» — it sits there, and it is not going anywhere
  tl.to("#g4free", {rotation: -5, duration: 0.24, ease: "power2.out"}, 17.58);
  tl.to("#g4free", {rotation: 4, duration: 0.30, ease: "power2.inOut"}, 17.82);
  tl.to("#g4free", {rotation: 0, duration: 0.30, ease: "power2.out"}, 18.12);
  tl.to("#g4", {autoAlpha: 0, duration: 0.20, ease: "power2.in"}, 17.90);'''
    return html, js


@beat
def b05_many_few():
    """«користуюсь купою різних платформ, реально плачу лише за кілька»

    Thirty tiles; four of them light up and the rest drain away.
    """
    html = '''
      <div class="g full" id="g5">
        <div class="swarm" id="g5s">%s</div>
      </div>''' % "".join(
        '<i class="%s"></i>' % ("keep" if i in (3, 8, 15, 22) else "")
        for i in range(30))
    js = '''
  gsap.set("#g5", {autoAlpha: 0});
  gsap.set("#g5s i", {autoAlpha: 0, scale: 0.5, transformOrigin: "50% 50%"});
  gsap.set("#g5s i.keep", {backgroundColor: "rgba(255,255,255,0.62)"});
  tl.set("#g5", {autoAlpha: 1}, 21.30);
  // «купою різних платформ»
  tl.to("#g5s i", {autoAlpha: 1, scale: 1, duration: 0.34, ease: "back.out(1.8)",
                   stagger: {each: 0.012, from: "random"}}, 21.46);
  // «реально плачу лише за кілька з них» — the rest drain out
  tl.to("#g5s i:not(.keep)", {autoAlpha: 0.13, scale: 0.86, duration: 0.44,
                              ease: "power2.inOut",
                              stagger: {each: 0.008, from: "edges"}}, 23.70);
  tl.to("#g5s i.keep", {backgroundImage:
        "linear-gradient(115deg, #c41434 0%, #8d0d24 100%)",
        scale: 1.06, duration: 0.30, ease: "back.out(2.4)"}, 23.86);
  tl.to("#g5", {autoAlpha: 0, duration: 0.28, ease: "power2.in"}, 25.00);'''
    return html, js


# --------------------------------------------------------------- B · Claude


@beat
def b06_claude():
    """«Найбільша витрата — штучний інтелект, я користуюсь Клодом… 100 євро»"""
    html = '''
      <div class="g full" id="g6">
        %s
        %s
        <div class="tier" id="g6t"><span>5</span><small>×</small></div>
      </div>''' % (
        marktile("g6tile", "claude-tile").replace(
            'class="tile brand prod "', 'class="tile brand prod" style="left:390px;top:90px"'),
        price("g6p", "100").replace('class="price "', 'class="price" style="left:396px;top:430px"'))
    js = '''
  gsap.set("#g6", {autoAlpha: 0});
  gsap.set("#g6tile", {autoAlpha: 0, scale: 0.78, transformOrigin: "50% 50%"});
  gsap.set("#g6p", {autoAlpha: 0, scale: 0.7, y: -40, transformOrigin: "50% 50%"});
  gsap.set("#g6t", {autoAlpha: 0, scale: 0.6, transformOrigin: "50% 50%"});
  tl.set("#g6", {autoAlpha: 1}, 26.70);
  // «штучний інтелект… Клодом»
  tl.to("#g6tile", {autoAlpha: 1, scale: 1, duration: 0.36, ease: "back.out(2.4)"}, 26.84);
  // «100 євро на місяць»
  tl.to("#g6p", {autoAlpha: 1, scale: 1, y: 0, duration: 0.36,
                 ease: "back.out(2.6)"}, 29.96);
  // «тариф Max 5x» — the tier, as a number, which is what it is
  tl.to("#g6t", {autoAlpha: 1, scale: 1, duration: 0.30, ease: "back.out(2.8)"}, 31.64);
  tl.to("#g6", {autoAlpha: 0, duration: 0.28, ease: "power2.in"}, 33.40);'''
    return html, js


@beat
def b07_best_investment():
    """«це була найкраща інвестиція в мій бізнес»

    The spend turns into a rising line — the only beat in the reel where money
    goes the other way.
    """
    html = '''
      <div class="g full" id="g7">
        <svg width="1080" height="560" viewBox="0 0 1080 560"
             style="position:absolute;left:0;top:40px">
          <path id="g7line" d="M170 470 L360 400 L560 300 L760 190 L920 90"
                fill="none" stroke="#ff6e9c" stroke-width="22"
                stroke-linecap="round" stroke-linejoin="round"
                stroke-dasharray="960" stroke-dashoffset="960"/>
          <circle id="g7dot" cx="920" cy="90" r="26" fill="#fff"/>
        </svg>
      </div>'''
    js = '''
  gsap.set("#g7", {autoAlpha: 0});
  gsap.set("#g7dot", {autoAlpha: 0, scale: 0, transformOrigin: "920px 90px"});
  tl.set("#g7", {autoAlpha: 1}, 33.90);
  tl.to("#g7line", {strokeDashoffset: 0, duration: 0.70, ease: "power2.out"}, 34.04);
  tl.to("#g7dot", {autoAlpha: 1, scale: 1, duration: 0.26, ease: "back.out(3)"}, 34.72);
  tl.to("#g7", {autoAlpha: 0, duration: 0.28, ease: "power2.in"}, 37.40);'''
    return html, js


# ------------------------------------------------------ C · Google Workspace


@beat
def b08_workspace():
    """«мій Google Workspace — це 16 євро на місяць»"""
    html = '''
      <div class="g full" id="g8">
        %s
        %s
      </div>''' % (
        marktile("g8tile", "workspace-mark").replace(
            'prod "', 'prod" style="left:390px;top:90px"'),
        price("g8p", "16").replace('class="price "', 'class="price" style="left:414px;top:430px"'))
    js = '''
  gsap.set("#g8", {autoAlpha: 0});
  gsap.set("#g8tile", {autoAlpha: 0, scale: 0.78, transformOrigin: "50% 50%"});
  gsap.set("#g8p", {autoAlpha: 0, scale: 0.7, y: -40, transformOrigin: "50% 50%"});
  tl.set("#g8", {autoAlpha: 1}, 41.86);
  tl.to("#g8tile", {autoAlpha: 1, scale: 1, duration: 0.34, ease: "back.out(2.4)"}, 42.00);
  tl.to("#g8p", {autoAlpha: 1, scale: 1, y: 0, duration: 0.34,
                 ease: "back.out(2.6)"}, 42.92);
  tl.to("#g8", {autoAlpha: 0, duration: 0.26, ease: "power2.in"}, 45.20);'''
    return html, js


@beat
def b09_what_you_get():
    """«своя доменна пошта, підписка на Джеміну, де я генерую картинки»

    Three things on three phrases: an address, the model, an image coming out
    of it.
    """
    html = '''
      <div class="g full" id="g9">
        <div class="at" id="g9at"><span>@</span></div>
        %s
        <div class="pic" id="g9pic"><i></i><s></s></div>
      </div>''' % marktile("g9gem", "gemini-mark").replace(
        'prod "', 'prod small" style="left:150px;top:180px"')
    js = '''
  gsap.set("#g9", {autoAlpha: 0});
  gsap.set("#g9at, #g9gem, #g9pic", {autoAlpha: 0, scale: 0.7,
                                     transformOrigin: "50% 50%"});
  tl.set("#g9", {autoAlpha: 1}, 45.84);
  // «своя доменна пошта»
  tl.to("#g9at", {autoAlpha: 1, scale: 1, duration: 0.32, ease: "back.out(2.6)"}, 45.96);
  tl.to("#g9at", {autoAlpha: 0, scale: 0.8, duration: 0.22, ease: "power2.in"}, 46.90);
  // «підписка на Джеміну»
  tl.to("#g9gem", {autoAlpha: 1, scale: 1, duration: 0.30, ease: "back.out(2.4)"}, 47.10);
  // «де я генерую картинки» — and something comes out of it
  tl.to("#g9pic", {autoAlpha: 1, scale: 1, duration: 0.32, ease: "back.out(2.4)"}, 48.02);
  tl.to("#g9", {autoAlpha: 0, duration: 0.26, ease: "power2.in"}, 49.30);'''
    return html, js


@beat
def b10_ecosystem():
    """«вся екосистема Гугла в мене трошки краща, ніж у тих, хто сидить на
    безкоштовному» — a ring of Google things, and then the free version, alone.
    """
    html = '''
      <div class="g full" id="g10">
        <div class="ring" id="g10r">
          <i style="left:60px;top:210px"><span class="at2">@</span></i>
          <i style="left:250px;top:100px"><img class="mk" src="assets/logos/gcal-mark.png" alt=""></i>
          <i style="left:470px;top:60px"><span class="doc"><b></b><b></b><b></b></span></i>
          <i style="left:690px;top:100px"><img class="mk" src="assets/logos/meet-mark.png" alt=""></i>
          <i style="left:880px;top:210px"><span class="drv"></span></i>
        </div>
      </div>'''
    js = '''
  gsap.set("#g10", {autoAlpha: 0});
  gsap.set("#g10r i", {autoAlpha: 0, scale: 0.5, transformOrigin: "50% 50%"});
  tl.set("#g10", {autoAlpha: 1}, 49.56);
  tl.to("#g10r i", {autoAlpha: 1, scale: 1, duration: 0.32, ease: "back.out(2.2)",
                    stagger: 0.06}, 49.70);
  // «ніж у тих, хто сидить на безкоштовному» — all but one go out
  tl.to("#g10r i:not(:nth-child(3))", {autoAlpha: 0.16, scale: 0.8,
        duration: 0.40, ease: "power2.inOut", stagger: 0.04}, 53.10);
  tl.to("#g10", {autoAlpha: 0, duration: 0.28, ease: "power2.in"}, 54.60);'''
    return html, js


# -------------------------------------------------------------- D · ClickUp


@beat
def b11_clickup():
    """«ще плачу за Клікап, 7 євро на місяць»"""
    html = '''
      <div class="g full" id="g11">
        %s
        %s
      </div>''' % (
        marktile("g11tile", "clickup-mark").replace(
            'prod "', 'prod" style="left:390px;top:90px"'),
        price("g11p", "7").replace('class="price "', 'class="price" style="left:438px;top:430px"'))
    js = '''
  gsap.set("#g11", {autoAlpha: 0});
  gsap.set("#g11tile", {autoAlpha: 0, scale: 0.78, transformOrigin: "50% 50%"});
  gsap.set("#g11p", {autoAlpha: 0, scale: 0.7, y: -40, transformOrigin: "50% 50%"});
  tl.set("#g11", {autoAlpha: 1}, 55.88);
  tl.to("#g11tile", {autoAlpha: 1, scale: 1, duration: 0.34, ease: "back.out(2.4)"}, 56.02);
  tl.to("#g11p", {autoAlpha: 1, scale: 1, y: 0, duration: 0.34,
                  ease: "back.out(2.6)"}, 56.44);
  tl.to("#g11", {autoAlpha: 0, duration: 0.26, ease: "power2.in"}, 58.80);'''
    return html, js


@beat
def b11b_free_vs_paid():
    """«довго відкладала перехід на платний тариф, бо безкоштовного вистачало»

    Added after tools/review.py found 7.5 s of nothing between the ClickUp
    price and the command centre. The 0 € she was sitting on, the 7 € she
    eventually moved to, and the choice wavering between them — then it settles
    on the paid one. Clears before 62.30, her hand insert.
    """
    html = '''
      <div class="g full" id="g11b">
        <div class="opt" id="g11bf"><span>0</span><small>€</small></div>
        <div class="opt paid" id="g11bp"><span>7</span><small>€</small></div>
        <div class="pick" id="g11bs"></div>
      </div>'''
    js = '''
  gsap.set("#g11b", {autoAlpha: 0});
  gsap.set("#g11bf, #g11bp", {autoAlpha: 0, scale: 0.7,
                              transformOrigin: "50% 50%"});
  gsap.set("#g11bs", {autoAlpha: 0, x: 0});
  tl.set("#g11b", {autoAlpha: 1}, 60.72);
  tl.to("#g11bf", {autoAlpha: 1, scale: 1, duration: 0.28, ease: "back.out(2.4)"}, 60.86);
  tl.to("#g11bp", {autoAlpha: 1, scale: 1, duration: 0.28, ease: "back.out(2.4)"}, 61.08);
  // «довго відкладала» — the choice goes back and forth and does not commit
  tl.to("#g11bs", {autoAlpha: 1, duration: 0.14}, 61.22);
  tl.to("#g11bs", {x: 470, duration: 0.30, ease: "power2.inOut"}, 61.30);
  tl.to("#g11bs", {x: 0, duration: 0.30, ease: "power2.inOut"}, 61.62);
  tl.to("#g11bs", {x: 470, duration: 0.26, ease: "power2.inOut"}, 61.92);
  tl.to("#g11bf", {autoAlpha: 0.22, scale: 0.88, duration: 0.24}, 61.96);
  tl.to("#g11b", {autoAlpha: 0, duration: 0.20, ease: "power2.in"}, 62.14);'''
    return html, js


@beat
def b12_command_centre():
    """«використовую Клод як командний центр, який сам ставить мені задачі
    в Клікап»

    Claude on the left, ClickUp on the right, tasks crossing between them.
    Clears before 62.30 — her hand insert.
    """
    html = '''
      <div class="g full" id="g12">
        <div class="tile brand prod half" id="g12a" style="left:110px;top:150px">%s</div>
        <div class="tile brand prod half" id="g12b" style="left:730px;top:150px">
          <img class="mk" src="assets/logos/clickup-mark.png" alt=""></div>
        <div class="task" id="g12t1"></div>
        <div class="task" id="g12t2"></div>
        <div class="task" id="g12t3"></div>
      </div>''' % mark("claude-tile")
    js = '''
  gsap.set("#g12", {autoAlpha: 0});
  gsap.set("#g12a, #g12b", {autoAlpha: 0, scale: 0.78, transformOrigin: "50% 50%"});
  gsap.set("#g12 .task", {autoAlpha: 0, x: 0});
  tl.set("#g12", {autoAlpha: 1}, 66.28);
  // «командний центр»
  tl.to("#g12a", {autoAlpha: 1, scale: 1, duration: 0.32, ease: "back.out(2.4)"}, 66.42);
  tl.to("#g12b", {autoAlpha: 1, scale: 1, duration: 0.32, ease: "back.out(2.4)"}, 67.20);
  // «сам ставить мені задачі в Клікап» — they cross on their own
  [68.82, 69.10, 69.38].forEach(function (t, i) {
    tl.fromTo("#g12t" + (i + 1), {autoAlpha: 0, x: 0},
              {autoAlpha: 1, x: 0, duration: 0.14}, t);
    tl.to("#g12t" + (i + 1), {x: 420, duration: 0.52, ease: "power2.inOut"}, t + 0.06);
    tl.to("#g12t" + (i + 1), {autoAlpha: 0, duration: 0.14}, t + 0.52);
  });
  tl.to("#g12", {autoAlpha: 0, duration: 0.24, ease: "power2.in"}, 70.00);'''
    return html, js


@beat
def b13_the_limit():
    """«а там був ліміт, скільки задач можна відправити»

    A bar rises and stops dead against a ceiling. The ceiling is the beat.
    Clears before 72.95, her cropped closeup.
    """
    html = '''
      <div class="g full" id="g13">
        <div class="gauge" id="g13g">
          <span class="cap"></span>
          <span class="fill" id="g13f"></span>
        </div>
      </div>'''
    js = '''
  gsap.set("#g13", {autoAlpha: 0});
  gsap.set("#g13g .cap", {autoAlpha: 0, scaleX: 0.3, transformOrigin: "50% 50%"});
  gsap.set("#g13f", {height: 0});
  tl.set("#g13", {autoAlpha: 1}, 70.02);
  // «ліміт» — the ceiling first, so the bar has something to hit
  tl.to("#g13g .cap", {autoAlpha: 1, scaleX: 1, duration: 0.26,
                       ease: "back.out(2.6)"}, 70.14);
  tl.to("#g13f", {height: 300, duration: 0.70, ease: "power2.out"}, 70.50);
  // and it stops dead, twice, because she kept hitting it
  tl.to("#g13f", {height: 286, duration: 0.10, ease: "power2.in"}, 71.24);
  tl.to("#g13f", {height: 300, duration: 0.14, ease: "power2.out"}, 71.34);
  tl.to("#g13f", {height: 288, duration: 0.10, ease: "power2.in"}, 71.60);
  tl.to("#g13f", {height: 300, duration: 0.14, ease: "power2.out"}, 71.70);
  tl.to("#g13", {autoAlpha: 0, duration: 0.22, ease: "power2.in"}, 72.70);'''
    return html, js


@beat
def b14_ceiling_gone():
    """«тож плачу, щоб просто не думати про цю проблему» — the ceiling lifts."""
    html = '''
      <div class="g full" id="g14">
        <div class="gauge" id="g14g">
          <span class="cap" id="g14c"></span>
          <span class="fill" id="g14f" style="height:300px"></span>
        </div>
      </div>'''
    js = '''
  gsap.set("#g14", {autoAlpha: 0});
  tl.set("#g14", {autoAlpha: 1}, 76.76);
  tl.to("#g14c", {y: -110, autoAlpha: 0, duration: 0.44, ease: "power2.out"}, 76.90);
  tl.to("#g14f", {height: 420, duration: 0.50, ease: "power2.out"}, 76.98);
  tl.to("#g14", {autoAlpha: 0, duration: 0.24, ease: "power2.in"}, 78.20);'''
    return html, js


# ----------------------------------------------------------------- E · Mojo


@beat
def b15_mojo():
    """«остання, найдешевша підписка — це Моджо»"""
    html = '''
      <div class="g full" id="g15">
        %s
      </div>''' % marktile("g15tile", "mojo-mark").replace(
        'prod "', 'prod" style="left:390px;top:130px"')
    js = '''
  gsap.set("#g15", {autoAlpha: 0});
  gsap.set("#g15tile", {autoAlpha: 0, scale: 0.78, transformOrigin: "50% 50%"});
  tl.set("#g15", {autoAlpha: 1}, 79.36);
  tl.to("#g15tile", {autoAlpha: 1, scale: 1, duration: 0.34, ease: "back.out(2.4)"}, 79.50);
  tl.to("#g15", {autoAlpha: 0, duration: 0.24, ease: "power2.in"}, 80.50);'''
    return html, js


DEAD = (5, 6, 7, 16, 17, 18, 19, 27, 28)   # the silences Mojo cuts out


@beat
def b16_subtitles_and_gaps():
    """«роблю в ньому субтитри» → «класна функція вирізання пауз»

    Caption bars, then a waveform with its silences physically removed and the
    sound closing the gap.
    """
    html = '''
      <div class="g full" id="g16">
        <div class="subs" id="g16s"><b></b><b></b><b></b></div>
        <div class="gapwave" id="g16w">%s</div>
      </div>''' % "".join(
        '<i class="%s" id="g16b%d" style="height:%dpx"></i>'
        % ("dead" if i in DEAD else "", i,
           14 if i in DEAD else [30, 78, 132, 96, 160][i % 5])
        for i in range(34))
    js = '''
  gsap.set("#g16", {autoAlpha: 0});
  gsap.set("#g16s, #g16w", {autoAlpha: 0});
  gsap.set("#g16s b", {scaleX: 0, transformOrigin: "0% 50%"});
  tl.set("#g16", {autoAlpha: 1}, 80.60);
  // «субтитри»
  tl.to("#g16s", {autoAlpha: 1, duration: 0.18}, 80.72);
  tl.to("#g16s b", {scaleX: 1, duration: 0.26, stagger: 0.08,
                    ease: "power2.out"}, 80.76);
  tl.to("#g16s", {autoAlpha: 0, duration: 0.22, ease: "power2.in"}, 83.20);
  // «функція вирізання пауз» — the silences are cut out and the rest closes up
  tl.to("#g16w", {autoAlpha: 1, duration: 0.18}, 83.48);
  tl.to("#g16w i.dead", {scaleX: 0, autoAlpha: 0, duration: 0.30,
                         transformOrigin: "50% 50%",
                         ease: "power3.in"}, 84.10);
  tl.to("#g16b8", {x: -78, duration: 0.46, ease: "power3.inOut"}, 84.16);
  tl.to("#g16b9", {x: -78, duration: 0.46, ease: "power3.inOut"}, 84.16);
  tl.to("#g16b10", {x: -78, duration: 0.46, ease: "power3.inOut"}, 84.16);
  tl.to("#g16b11", {x: -78, duration: 0.46, ease: "power3.inOut"}, 84.16);
  tl.to("#g16b12", {x: -78, duration: 0.46, ease: "power3.inOut"}, 84.16);
  tl.to("#g16b13", {x: -78, duration: 0.46, ease: "power3.inOut"}, 84.16);
  tl.to("#g16b14", {x: -78, duration: 0.46, ease: "power3.inOut"}, 84.16);
  tl.to("#g16b15", {x: -78, duration: 0.46, ease: "power3.inOut"}, 84.16);
  tl.to("#g16b20", {x: -182, duration: 0.46, ease: "power3.inOut"}, 84.16);
  tl.to("#g16b21", {x: -182, duration: 0.46, ease: "power3.inOut"}, 84.16);
  tl.to("#g16b22", {x: -182, duration: 0.46, ease: "power3.inOut"}, 84.16);
  tl.to("#g16b23", {x: -182, duration: 0.46, ease: "power3.inOut"}, 84.16);
  tl.to("#g16b24", {x: -182, duration: 0.46, ease: "power3.inOut"}, 84.16);
  tl.to("#g16b25", {x: -182, duration: 0.46, ease: "power3.inOut"}, 84.16);
  tl.to("#g16b26", {x: -182, duration: 0.46, ease: "power3.inOut"}, 84.16);
  tl.to("#g16b29", {x: -234, duration: 0.46, ease: "power3.inOut"}, 84.16);
  tl.to("#g16b30", {x: -234, duration: 0.46, ease: "power3.inOut"}, 84.16);
  tl.to("#g16b31", {x: -234, duration: 0.46, ease: "power3.inOut"}, 84.16);
  tl.to("#g16b32", {x: -234, duration: 0.46, ease: "power3.inOut"}, 84.16);
  tl.to("#g16b33", {x: -234, duration: 0.46, ease: "power3.inOut"}, 84.16);
  tl.to("#g16", {autoAlpha: 0, duration: 0.24, ease: "power2.in"}, 85.60);'''
    return html, js


@beat
def b17_ukrainian():
    """«дуже добре працює з українською мовою»

    STYLE.md §4: reach for the obvious literal image. She asked for the flag by
    name on this exact phrase in an earlier reel, and it is the one sanctioned
    departure from the palette, because a flag has to be its own colours.
    """
    html = '''
      <div class="g full" id="g17">
        <div class="flag" id="g17f"><i class="b"></i><i class="y"></i></div>
      </div>'''
    js = '''
  gsap.set("#g17", {autoAlpha: 0});
  gsap.set("#g17f", {autoAlpha: 0, scale: 0.7, transformOrigin: "50% 50%"});
  gsap.set("#g17f i.y", {scaleY: 0, transformOrigin: "50% 100%"});
  tl.set("#g17", {autoAlpha: 1}, 85.80);
  tl.to("#g17f", {autoAlpha: 1, scale: 1, duration: 0.34, ease: "back.out(2.4)"}, 85.94);
  tl.to("#g17f i.y", {scaleY: 1, duration: 0.30, ease: "power2.out"}, 86.10);
  tl.to("#g17", {autoAlpha: 0, duration: 0.24, ease: "power2.in"}, 87.00);'''
    return html, js


@beat
def b18_hryvnia_to_pennies():
    """«коштує 1000 гривень на рік, тобто на місяць виходить взагалі копійки»

    The year price is big; the month price is what is left of it.
    """
    html = '''
      <div class="g full" id="g18">
        <div class="big" id="g18y" style="top:180px;font-size:200px">1000<small>₴</small></div>
        <div class="big" id="g18m" style="top:250px;font-size:96px">2<small>€</small></div>
      </div>'''
    js = '''
  gsap.set("#g18", {autoAlpha: 0});
  gsap.set("#g18y", {autoAlpha: 0, scale: 0.6, transformOrigin: "50% 50%"});
  gsap.set("#g18m", {autoAlpha: 0, scale: 0.4, transformOrigin: "50% 50%"});
  tl.set("#g18", {autoAlpha: 1}, 87.08);
  tl.to("#g18y", {autoAlpha: 1, scale: 1, duration: 0.36, ease: "back.out(2.6)"}, 87.20);
  // «на місяць виходить взагалі копійки» — it collapses to almost nothing
  tl.to("#g18y", {autoAlpha: 0, scale: 0.28, duration: 0.44,
                  ease: "power3.in"}, 89.52);
  tl.to("#g18m", {autoAlpha: 1, scale: 1, duration: 0.34,
                  ease: "back.out(2.4)"}, 89.90);
  tl.to("#g18", {autoAlpha: 0, duration: 0.26, ease: "power2.in"}, 91.60);'''
    return html, js


@beat
def b19_domain():
    """«плюс ще домен, я плачу 12 євро на рік»"""
    html = '''
      <div class="g full" id="g19">
        <div class="tile brand prod" id="g19t" style="left:180px;top:120px">
          <span class="wordmark" style="font-size:80px">.com</span></div>
        %s
      </div>''' % price("g19p", "12", "€/рік").replace(
        'class="price "', 'class="price ink" style="left:672px;top:216px"')
    js = '''
  gsap.set("#g19", {autoAlpha: 0});
  gsap.set("#g19t", {autoAlpha: 0, scale: 0.78, transformOrigin: "50% 50%"});
  gsap.set("#g19p", {autoAlpha: 0, scale: 0.7, y: -40, transformOrigin: "50% 50%"});
  tl.set("#g19", {autoAlpha: 1}, 93.36);
  tl.to("#g19t", {autoAlpha: 1, scale: 1, duration: 0.32, ease: "back.out(2.4)"}, 93.50);
  tl.to("#g19p", {autoAlpha: 1, scale: 1, y: 0, duration: 0.32,
                  ease: "back.out(2.6)"}, 94.72);
  tl.to("#g19", {autoAlpha: 0, duration: 0.26, ease: "power2.in"}, 96.10);'''
    return html, js


# ------------------------------------------------------------- F · the bill


@beat
def b20_the_bill():
    """«якщо ти завжди хочеш знати що варто інвестувати, а на чому можна
    зекономити»

    The payoff: five lines, and they add back up to the number she opened with.
    """
    rows = [("Claude", "~100 €"), ("Google Workspace", "16 €"),
            ("ClickUp", "7 €"), ("Mojo", "2 €"), (".com", "1 €")]
    body = "".join(
        '<div class="brow" id="g20r%d"><span class="bn">%s</span>'
        '<span class="bv">%s</span></div>' % (i, n, v)
        for i, (n, v) in enumerate(rows))
    html = '''
      <div class="g full" id="g20">
        <div class="bill" id="g20b">%s
          <div class="btot" id="g20t">
            <span class="bn">/ міс</span><span class="bv">130 €</span>
          </div>
        </div>
      </div>''' % body
    js = '''
  gsap.set("#g20", {autoAlpha: 0});
  gsap.set("#g20b", {autoAlpha: 0, scale: 0.92, transformOrigin: "50% 40%"});
  gsap.set("#g20 .brow", {autoAlpha: 0, x: -30});
  gsap.set("#g20t", {autoAlpha: 0, scale: 0.9, transformOrigin: "50% 50%"});
  tl.set("#g20", {autoAlpha: 1}, 96.30);
  tl.to("#g20b", {autoAlpha: 1, scale: 1, duration: 0.34, ease: "power2.out"}, 96.36);
  tl.to("#g20 .brow", {autoAlpha: 1, x: 0, duration: 0.24, stagger: 0.10,
                       ease: "power3.out"}, 96.50);
  // «а на чому можна зекономити» — and the total she opened with comes back
  tl.to("#g20t", {autoAlpha: 1, scale: 1, duration: 0.36,
                  ease: "back.out(2.6)"}, 99.70);
  tl.to("#g20", {autoAlpha: 0, duration: 0.30, ease: "power2.in"}, 100.90);'''
    return html, js


k.css("""
    /* b02 — where it goes */
    .slots { position: absolute; left: 90px; top: 210px; width: 900px;
             display: flex; gap: 22px; }
    .slots i { display: block; flex: 1; height: 190px; border-radius: 28px;
               background: rgba(255,255,255,0.55); box-shadow: var(--rim);
               filter: var(--cast-sm); }

    /* b03 — the coin she does not want to hand over */
    .coin { position: absolute; left: 300px; top: 210px; width: 210px;
            height: 210px; border-radius: 50%; display: grid;
            place-items: center; background: var(--lit-pink);
            box-shadow: var(--rim-dark), inset 0 0 0 14px rgba(255,255,255,0.55);
            filter: var(--cast); }
    .coin span { font-size: 116px; font-weight: 900; color: #fff;
                 line-height: 1; letter-spacing: -0.04em; }

    /* b06 — the plan tier, which is a number */
    .tier { position: absolute; left: 686px; top: 104px; width: 156px;
            height: 156px; border-radius: 50%; display: grid;
            place-items: center; grid-auto-flow: column; gap: 2px;
            background: var(--lit-pink); box-shadow: var(--rim-dark);
            filter: var(--cast); }
    .tier span { font-size: 82px; font-weight: 900; color: #fff; line-height: 1;
                 letter-spacing: -0.04em; }
    .tier small { font-size: 48px; font-weight: 900; color: #fff; }

    /* b09 — the address, and the picture that comes out */
    .at { position: absolute; left: 400px; top: 160px; width: 280px;
          height: 280px; border-radius: 50%; display: grid; place-items: center;
          background: var(--lit); box-shadow: var(--rim); filter: var(--cast); }
    .at span { font-size: 150px; font-weight: 900; color: var(--accent);
               line-height: 1; }
    .tile.brand.prod.small { width: 280px; height: 280px; }
    .pic { position: absolute; left: 610px; top: 215px; width: 320px;
           height: 240px; border-radius: 30px; overflow: hidden;
           background: var(--lit-blush); box-shadow: var(--rim);
           filter: var(--cast); }
    .pic i { position: absolute; left: 40px; top: 44px; width: 78px;
             height: 78px; border-radius: 50%; background: var(--lit-pink); }
    .pic s { position: absolute; left: 0; bottom: 0; width: 320px; height: 110px;
             background: linear-gradient(160deg,#c41434,#8d0d24);
             clip-path: polygon(0 62%, 30% 20%, 55% 55%, 78% 28%, 100% 58%,
                                100% 100%, 0 100%); }

    /* b10 — the ecosystem, and the one left on the free tier */
    .ring i { position: absolute; width: 150px; height: 150px;
              border-radius: 40px; display: grid; place-items: center;
              background: var(--lit-blush);
              box-shadow: var(--rim); filter: var(--cast-sm); }
    .ring i .mk { width: 62%; height: auto; display: block; }
    .at2 { font-size: 78px; font-weight: 900; color: var(--accent);
           line-height: 1; }
    .doc { display: block; width: 76px; }
    .doc b { display: block; height: 12px; border-radius: 6px;
             background: var(--accent); margin-bottom: 11px; }
    .doc b:nth-child(2) { width: 74%; background: var(--graphite); }
    .doc b:nth-child(3) { width: 50%; background: var(--graphite); }
    .drv { display: block; width: 0; height: 0; border-left: 44px solid transparent;
           border-right: 44px solid transparent;
           border-bottom: 76px solid var(--accent); }

    /* b11b — the tier she sat on, and the one she moved to */
    .opt { position: absolute; top: 170px; width: 230px; height: 230px;
           border-radius: 50%; display: grid; place-items: center;
           grid-auto-flow: column; gap: 4px; background: var(--lit-ink);
           box-shadow: var(--rim-dark); filter: var(--cast); }
    .opt { left: 195px; }
    .opt.paid { left: 665px; background: var(--lit-accent); }
    .opt span { font-size: 116px; font-weight: 900; color: #fff; line-height: 1;
                letter-spacing: -0.05em; }
    .opt small { font-size: 54px; font-weight: 900; color: #fff; }
    .pick { position: absolute; left: 285px; top: 434px; width: 50px;
            height: 50px; border-radius: 50%; background: var(--pink);
            filter: drop-shadow(0 0 22px rgba(255,110,156,0.9)); }

    /* b12 — tasks crossing from the hub to the task list */
    .tile.brand.prod.half { width: 240px; height: 240px; }
    .task { position: absolute; left: 360px; top: 250px; width: 96px;
            height: 44px; border-radius: 16px; background: var(--lit-accent);
            box-shadow: var(--rim-dark); }
""")

for _sel, _w, _h, _r in [
    (".tile.brand.prod.half", 240, 240, 58),
    (".tile.brand.prod.small", 280, 280, 68),
]:
    k.squircle(_sel, _w, _h, _r)


def main():
    caps = k.load_captions(os.path.join(ROOT, "work", "r08", "captions.json"))
    gh, gj = [], []
    for fn in BEATS:
        h, j = fn()
        if h.strip():
            gh.append(h.rstrip())
        gj.append("  /* %s */" % fn.__name__)
        gj.append(j.rstrip())

    doc = k.document(
        title="Reel 8 — 130 євро",
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
