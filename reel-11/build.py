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


k.css("""
    /* ---- the budget, in all three of its states ----
       One object, shown padded (2.25), struck through (27.45) and reduced to
       a single line (41.00). Same rows, same pitch, same positions each time,
       because the argument is that it is the *same list* all along. */
    .bl { position: absolute; left: 70px; width: 940px; height: 80px; }
    .bl b { position: absolute; top: 10px; font-weight: 500; font-size: 40px;
            color: var(--ink); }
    .bl b.lb { left: 0; }
    .bl b.am { right: 0; font-weight: 900; text-align: right; }
    .bl i { position: absolute; left: -10px; top: 32px; width: 960px;
            height: 9px; border-radius: 5px; background: var(--accent);
            transform-origin: 0% 50%; }
    .blr { position: absolute; left: 70px; width: 940px; height: 2px;
           background: rgba(23,20,28,0.18); }
    .tot { position: absolute; left: 70px; width: 940px; height: 110px; }
    .tot b { position: absolute; font-weight: 900; color: var(--ink); }
    .tot b.lb { left: 0; top: 30px; font-size: 44px; }
    .tot b.am { right: 0; top: 4px; font-size: 86px; color: var(--accent);
                text-align: right; }

    /* ---- TK4: a free tier is a gauge, not a badge ----
       Her note on reel 7 was that an unnameable shape is worthless. A track
       with a generous filled band and a small marker well inside it reads as
       "there is far more room here than you use". */
    .gauge { position: absolute; height: 76px; border-radius: 999px;
             background: var(--container); box-shadow: var(--rim);
             overflow: hidden; }
    .gauge i.free { position: absolute; left: 0; top: 0; height: 76px;
                    border-radius: 999px; background: var(--lit-pink);
                    transform-origin: 0% 50%; }
    .gauge i.used { position: absolute; top: 0; height: 76px; width: 10px;
                    background: var(--ink); }
    .glab { position: absolute; font-weight: 900; font-size: 38px;
            color: var(--ink); }

    /* ---- TK5: money in, tokens out ---- */
    .orbox { position: absolute; display: grid; place-items: center;
             border-radius: 56px; background: var(--lit); box-shadow: var(--rim);
             filter: var(--cast); }
    .orbox svg { width: 62%; height: auto; display: block; }
    .coin { position: absolute; display: grid; place-items: center;
            width: 128px; height: 128px; border-radius: 50%;
            background: var(--lit-accent); color: #fff; font-weight: 900;
            font-size: 52px; box-shadow: var(--rim-dark); }
    .tok { position: absolute; height: 34px; border-radius: 999px;
           background: var(--lit-pink); box-shadow: var(--rim-dark); }
""")


# ------------------------------------------------------------------ A · hook


@beat
def b01_five_hundred():
    """«У Тредсі постійно пишуть, що для цього треба мати 500 євро на місяць»

    Takeover 1, and the padded state of the reel's one object: ten line items
    and a total, laid out like a real breakdown so that striking it apart at
    27s means something. Nothing here is styled to look wrong — it has to look
    plausible first.

    Captions are blacked out 4.20-5.42: the total says 500 € while she says
    «500 євро», which is the exact case her rule names.
    """
    html = '''
      <div class="g full" id="g1">
        <div class="tk paper"></div><div class="gp"></div>
        <div class="bl" id="g1r0" style="top:290px"><b class="lb">Хостинг</b><b class="am">40 &#8364;</b><i id="g1rs0"></i></div>
        <div class="bl" id="g1r1" style="top:386px"><b class="lb">База даних</b><b class="am">60 &#8364;</b><i id="g1rs1"></i></div>
        <div class="bl" id="g1r2" style="top:482px"><b class="lb">AI підписка</b><b class="am">100 &#8364;</b><i id="g1rs2"></i></div>
        <div class="bl" id="g1r3" style="top:578px"><b class="lb">Домен</b><b class="am">15 &#8364;</b><i id="g1rs3"></i></div>
        <div class="bl" id="g1r4" style="top:674px"><b class="lb">Моніторинг</b><b class="am">45 &#8364;</b><i id="g1rs4"></i></div>
        <div class="bl" id="g1r5" style="top:770px"><b class="lb">Аналітика</b><b class="am">35 &#8364;</b><i id="g1rs5"></i></div>
        <div class="bl" id="g1r6" style="top:866px"><b class="lb">CDN</b><b class="am">30 &#8364;</b><i id="g1rs6"></i></div>
        <div class="bl" id="g1r7" style="top:962px"><b class="lb">Email</b><b class="am">25 &#8364;</b><i id="g1rs7"></i></div>
        <div class="bl" id="g1r8" style="top:1058px"><b class="lb">Бекапи</b><b class="am">20 &#8364;</b><i id="g1rs8"></i></div>
        <div class="bl" id="g1r9" style="top:1154px"><b class="lb">Інструменти</b><b class="am">130 &#8364;</b><i id="g1rs9"></i></div>
        <i class="blr" id="g1sep" style="top:1268px"></i>
        <div class="tot" id="g1t" style="top:1288px">
          <b class="lb">на місяць</b><b class="am">500 &#8364;</b>
        </div>
      </div>'''
    js = '''
  gsap.set("#g1", {autoAlpha: 0});
  gsap.set("#g1 .bl", {autoAlpha: 0, x: -30});
  gsap.set("#g1 .bl i", {scaleX: 0});
  gsap.set("#g1sep", {scaleX: 0, transformOrigin: "0% 50%"});
  gsap.set("#g1t", {autoAlpha: 0, scale: 0.7, transformOrigin: "100% 50%"});
  tl.set("#g1", {autoAlpha: 1}, 2.25);
  // «постійно пишуть, що треба мати» — the breakdown lists itself out
  tl.to("#g1 .bl", {autoAlpha: 1, x: 0, duration: 0.24, ease: "power2.out",
                    stagger: 0.13}, 2.68);
  tl.to("#g1sep", {scaleX: 1, duration: 0.30, ease: "power2.out"}, 4.06);
  // «500 євро на місяць»
  tl.to("#g1t", {autoAlpha: 1, scale: 1, duration: 0.40,
                 ease: "back.out(2.4)"}, 4.28);
  tl.to("#g1", {autoAlpha: 0, duration: 0.24, ease: "power2.in"}, 7.28);'''
    return html, js


@beat
def b01b_twenty_dollars():
    """«А насправді можна почати з 20 доларів»

    Matted, and the first big thing behind her in this reel. The 500 has just
    left the screen; this is the number that replaces it, so it is set at
    420px and passes behind her head rather than sitting over her.

    Captions blacked out 8.64-9.95 — it says 20 $ while she says «20 доларів».
    """
    html = '''
      <div class="g full" id="g1b">
        <div class="big" id="g1bn" style="top:330px;font-size:300px;color:#b4122f;text-shadow:none">20<small> $</small></div>
      </div>'''
    js = '''
  gsap.set("#g1b", {autoAlpha: 0});
  gsap.set("#g1bn", {autoAlpha: 0, scale: 0.5, transformOrigin: "50% 50%"});
  tl.set("#g1b", {autoAlpha: 1}, 7.40);
  // «20 доларів»
  tl.to("#g1bn", {autoAlpha: 1, scale: 1, duration: 0.44,
                  ease: "back.out(2.2)"}, 8.64);
  tl.to("#g1b", {autoAlpha: 0, duration: 0.28, ease: "power2.in"}, 9.95);'''
    return html, js


# The 20 goes behind her: it is the number that replaces the 500 that just
# left the screen, so it needs the size, and at 420px it would otherwise sit
# on her face. 80 frames.
k.matte("twenty", 7.300, 2.667)


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
    """«і ще купа якихось додаткових штук — це все безкоштовне на старті.
    І виходить, що цифра ніби роздувається ШТУЧНО»

    Takeover 2. The same ten rows return in the same places, and nine of them
    are struck through — every line except the AI subscription, which is the
    only one anybody actually pays. Then the total balloons, because that is
    literally what she says is happening to it.

    Merges the old b04 and b05: they were one movement and cutting between
    them lost which list was being talked about.
    """
    html = '''
      <div class="g full" id="g4">
        <div class="tk paper"></div><div class="gp"></div>
        <div class="bl" id="g4r0" style="top:290px"><b class="lb">Хостинг</b><b class="am">40 &#8364;</b><i id="g4rs0"></i></div>
        <div class="bl" id="g4r1" style="top:386px"><b class="lb">База даних</b><b class="am">60 &#8364;</b><i id="g4rs1"></i></div>
        <div class="bl" id="g4r2" style="top:482px"><b class="lb">AI підписка</b><b class="am">100 &#8364;</b><i id="g4rs2"></i></div>
        <div class="bl" id="g4r3" style="top:578px"><b class="lb">Домен</b><b class="am">15 &#8364;</b><i id="g4rs3"></i></div>
        <div class="bl" id="g4r4" style="top:674px"><b class="lb">Моніторинг</b><b class="am">45 &#8364;</b><i id="g4rs4"></i></div>
        <div class="bl" id="g4r5" style="top:770px"><b class="lb">Аналітика</b><b class="am">35 &#8364;</b><i id="g4rs5"></i></div>
        <div class="bl" id="g4r6" style="top:866px"><b class="lb">CDN</b><b class="am">30 &#8364;</b><i id="g4rs6"></i></div>
        <div class="bl" id="g4r7" style="top:962px"><b class="lb">Email</b><b class="am">25 &#8364;</b><i id="g4rs7"></i></div>
        <div class="bl" id="g4r8" style="top:1058px"><b class="lb">Бекапи</b><b class="am">20 &#8364;</b><i id="g4rs8"></i></div>
        <div class="bl" id="g4r9" style="top:1154px"><b class="lb">Інструменти</b><b class="am">130 &#8364;</b><i id="g4rs9"></i></div>
        <i class="blr" id="g4sep" style="top:1268px"></i>
        <div class="tot" id="g4t" style="top:1288px">
          <b class="lb">на місяць</b><b class="am">500 &#8364;</b>
        </div>
      </div>'''
    js = '''
  gsap.set("#g4", {autoAlpha: 0});
  gsap.set("#g4 .bl", {autoAlpha: 0, x: -24});
  gsap.set("#g4 .bl i", {scaleX: 0});
  gsap.set("#g4t", {autoAlpha: 0});
  tl.set("#g4", {autoAlpha: 1}, 27.45);
  // «ще купа якихось додаткових штук» — the same list, back where it was
  tl.to("#g4 .bl", {autoAlpha: 1, x: 0, duration: 0.18, ease: "power2.out",
                    stagger: 0.055}, 27.50);
  tl.to("#g4t", {autoAlpha: 1, duration: 0.24}, 28.30);
  // «це все безкоштовне» — nine of ten, struck through in order
  tl.to("#g4rs0", {scaleX: 1, duration: 0.26, ease: "power2.out"}, 30.340);
  tl.to("#g4rs1", {scaleX: 1, duration: 0.26, ease: "power2.out"}, 30.445);
  tl.to("#g4rs3", {scaleX: 1, duration: 0.26, ease: "power2.out"}, 30.550);
  tl.to("#g4rs4", {scaleX: 1, duration: 0.26, ease: "power2.out"}, 30.655);
  tl.to("#g4rs5", {scaleX: 1, duration: 0.26, ease: "power2.out"}, 30.760);
  tl.to("#g4rs6", {scaleX: 1, duration: 0.26, ease: "power2.out"}, 30.865);
  tl.to("#g4rs7", {scaleX: 1, duration: 0.26, ease: "power2.out"}, 30.970);
  tl.to("#g4rs8", {scaleX: 1, duration: 0.26, ease: "power2.out"}, 31.075);
  tl.to("#g4rs9", {scaleX: 1, duration: 0.26, ease: "power2.out"}, 31.180);
  // «на старті» — and their amounts stop counting
  tl.to("#g4r0 b.am", {autoAlpha: 0.22, duration: 0.22}, 31.660);
  tl.to("#g4r1 b.am", {autoAlpha: 0.22, duration: 0.22}, 31.715);
  tl.to("#g4r3 b.am", {autoAlpha: 0.22, duration: 0.22}, 31.770);
  tl.to("#g4r4 b.am", {autoAlpha: 0.22, duration: 0.22}, 31.825);
  tl.to("#g4r5 b.am", {autoAlpha: 0.22, duration: 0.22}, 31.880);
  tl.to("#g4r6 b.am", {autoAlpha: 0.22, duration: 0.22}, 31.935);
  tl.to("#g4r7 b.am", {autoAlpha: 0.22, duration: 0.22}, 31.990);
  tl.to("#g4r8 b.am", {autoAlpha: 0.22, duration: 0.22}, 32.045);
  tl.to("#g4r9 b.am", {autoAlpha: 0.22, duration: 0.22}, 32.100);
  // «цифра ніби роздувається ШТУЧНО» — so the total does exactly that
  tl.to("#g4t", {scale: 1.9, duration: 0.70, ease: "back.out(1.4)",
                 transformOrigin: "100% 50%"}, 33.68);
  tl.to("#g4t", {scale: 2.05, duration: 0.30, ease: "power2.out",
                 transformOrigin: "100% 50%"}, 34.48);
  tl.to("#g4", {autoAlpha: 0, duration: 0.16, ease: "power2.in"}, 36.70);'''
    return html, js


# ------------------------------------------------- C · what it actually costs


@beat
def b06_only_one_thing():
    """«тобі потрібно тільки ОДНЕ — підписка на сам штучний інтелект, тобто
    Claude Code або Codex, і це навіть не 100 євро, а 20»

    Takeover 3, and the last state of the object: one row left, in the place
    it occupied in the list, with the two products that fill it. Then the
    amount corrects itself — 100 struck, 20 in its place.

    Merges the old b06 and b07. Captions blacked out 51.02-52.15, where the
    row says 100 and 20 while she says «сто» and «двадцять».
    """
    html = '''
      <div class="g full" id="g6">
        <div class="tk paper"></div><div class="gp"></div>
        <div class="bl" id="g6row" style="top:760px">
          <b class="lb">AI підписка</b>
          <b class="am" id="g6old">100 &#8364;</b>
          <i id="g6strike"></i>
        </div>
        <i class="blr" id="g6sep" style="top:880px"></i>
        <div class="tile brand prod" id="g6a" style="left:190px;top:1020px">%s</div>
        <div class="tile brand prod" id="g6b" style="left:640px;top:1020px">%s</div>
      </div>''' % (mark("claude-tile"), mark("codex-mark"))
    js = '''
  gsap.set("#g6", {autoAlpha: 0});
  gsap.set("#g6row", {autoAlpha: 0, scale: 0.86, transformOrigin: "50% 50%"});
  gsap.set("#g6sep", {scaleX: 0, transformOrigin: "0% 50%"});
  gsap.set("#g6strike", {scaleX: 0});
  gsap.set("#g6a, #g6b", {autoAlpha: 0, scale: 0.6, y: 40,
                          transformOrigin: "50% 50%"});
  tl.set("#g6", {autoAlpha: 1}, 44.80);
  // «тільки одне»
  tl.to("#g6row", {autoAlpha: 1, scale: 1, duration: 0.40,
                   ease: "back.out(2.2)"}, 45.06);
  tl.to("#g6sep", {scaleX: 1, duration: 0.30, ease: "power2.out"}, 45.78);
  // «Claude Code»
  tl.to("#g6a", {autoAlpha: 1, scale: 1, y: 0, duration: 0.36,
                 ease: "back.out(2.4)"}, 48.58);
  // «або Codex»
  tl.to("#g6b", {autoAlpha: 1, scale: 1, y: 0, duration: 0.36,
                 ease: "back.out(2.4)"}, 49.52);
  // «навіть не 100 євро» — the padded figure crosses itself out and that is
  // the last thing the page does; «а 20» is hers to say.
  tl.to("#g6strike", {scaleX: 1, duration: 0.30, ease: "power2.out"}, 50.88);
  tl.to("#g6old", {autoAlpha: 0.32, duration: 0.26}, 51.06);
  tl.to("#g6", {autoAlpha: 0, duration: 0.22, ease: "power2.in"}, 51.95);'''
    return html, js


@beat
def b08_hosting_and_db():
    """«Хостинг — це той самий Versal, але в нього є щедрі безкоштовні ліміти,
    і їх вистачає. База даних Supabase, там теж безкоштовний ліміт»

    Takeover 4. Each product gets a gauge rather than a badge: a generous
    filled band with a small marker sitting well inside it, which is what
    "the free tier is more than enough" actually looks like. STYLE.md 4a.4 —
    every object has to be nameable, and a lone chip reading 0 € is not.
    """
    html = '''
      <div class="g full" id="g8">
        <div class="tk paper"></div><div class="gp"></div>
        <div id="g8top" style="position:absolute;inset:0">
          <div class="tile brand prod" id="g8a" style="left:100px;top:300px">%s</div>
          <div class="gauge" id="g8g1" style="left:100px;top:620px;width:880px">
            <i class="free" id="g8f1" style="width:880px"></i>
            <i class="used" id="g8u1" style="left:206px"></i>
          </div>
          <div class="glab" id="g8l1" style="left:100px;top:722px">0 &#8364;</div>
        </div>
        <div class="tile brand prod" id="g8b" style="left:100px;top:880px">%s</div>
        <div class="gauge" id="g8g2" style="left:100px;top:1200px;width:880px">
          <i class="free" id="g8f2" style="width:880px"></i>
          <i class="used" id="g8u2" style="left:158px"></i>
        </div>
        <div class="glab" id="g8l2" style="left:100px;top:1302px">0 &#8364;</div>
      </div>''' % (mark("vercel-mark"), mark("supabase-mark"))
    js = '''
  gsap.set("#g8", {autoAlpha: 0});
  gsap.set("#g8top", {y: 300});
  gsap.set("#g8a, #g8b", {autoAlpha: 0, scale: 0.62, transformOrigin: "50% 50%"});
  gsap.set("#g8g1, #g8g2", {autoAlpha: 0});
  gsap.set("#g8f1, #g8f2", {scaleX: 0});
  gsap.set("#g8u1, #g8u2", {autoAlpha: 0});
  gsap.set("#g8l1, #g8l2", {autoAlpha: 0, y: 16});
  tl.set("#g8", {autoAlpha: 1}, 53.40);
  // «Versal»
  tl.to("#g8a", {autoAlpha: 1, scale: 1, duration: 0.36,
                 ease: "back.out(2.4)"}, 54.84);
  // «щедрі безкоштовні ліміти, і їх вистачає»
  tl.to("#g8g1", {autoAlpha: 1, duration: 0.20}, 56.50);
  tl.to("#g8f1", {scaleX: 1, duration: 0.52, ease: "power3.out"}, 56.56);
  tl.to("#g8u1", {autoAlpha: 1, duration: 0.20}, 57.60);
  tl.to("#g8l1", {autoAlpha: 1, y: 0, duration: 0.24}, 57.72);
  // «База даних» — the first product moves up to make room for the second
  tl.to("#g8top", {y: 0, duration: 0.58, ease: "power2.inOut"}, 58.90);
  // «Supabase»
  tl.to("#g8b", {autoAlpha: 1, scale: 1, duration: 0.36,
                 ease: "back.out(2.4)"}, 59.68);
  // «там теж безкоштовний ліміт, який точно достатньо»
  tl.to("#g8g2", {autoAlpha: 1, duration: 0.20}, 60.78);
  tl.to("#g8f2", {scaleX: 1, duration: 0.52, ease: "power3.out"}, 60.84);
  tl.to("#g8u2", {autoAlpha: 1, duration: 0.20}, 61.78);
  tl.to("#g8l2", {autoAlpha: 1, y: 0, duration: 0.24}, 61.90);
  tl.to("#g8", {autoAlpha: 0, duration: 0.16, ease: "power2.in"}, 63.30);'''
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
        <div class="big" id="g9r" style="top:80px;font-size:280px;color:#b4122f;text-shadow:none;letter-spacing:-0.03em">RUTA</div>
        <div class="voice" id="g9v" style="left:420px;top:430px;width:240px;
             height:90px;justify-content:center">%s</div>
        <div class="outs" id="g9o" style="top:580px"><span></span><span></span><span></span></div>
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


# RUTA behind her head — the one she singled out from reel 7. 151 frames.
k.matte("ruta", 67.900, 5.033)


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


# Three numbers in this reel are spoken and shown at the same moment, which is
# exactly the case her rule names (STYLE.md 2b.1).
BLACKOUT = [
    (4.20, 5.42, "TK1 — the total reads 500 € on «500 євро»"),
    (8.64, 9.95, "M1 — 20 $ on «20 доларів»"),
    (50.80, 51.70, "TK3 — the row reads 100 € on «не 100 євро»"),
]

INVERT = [
    (2.25, 7.30, "TK1 — the padded breakdown"),
    (27.45, 36.75, "TK2 — the same list, struck through"),
    (44.80, 51.95, "TK3 — one line left"),
    (53.40, 63.40, "TK4 — the free tiers"),
]


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
        blackout=BLACKOUT,
        invert=INVERT,
    )
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "index.html")
    io.open(out, "w", encoding="utf-8").write(doc)
    print("index.html  %d captions, %d beats, %.1f KB"
          % (len(caps), len(BEATS), os.path.getsize(out) / 1024.0))


main()
