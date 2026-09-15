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


def dcard(cid, x, y, w, h):
    """One finished artefact. Rotation is deliberately NOT in the style
    attribute: GSAP writes `transform` wholesale, so an inline rotate would be
    wiped the first time the card is tweened."""
    return ('<div class="dk" id="%s" data-layout-allow-overflow'
            ' style="left:%dpx;top:%dpx;width:%dpx;height:%dpx">'
            '<i class="hb" style="width:%dpx"></i>'
            '<i class="rr" style="top:%dpx;width:%dpx"></i>'
            '<i class="rr" style="top:%dpx;width:%dpx"></i>'
            '<i class="pb" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx"></i>'
            '</div>'
            % (cid, x, y, w, h,
               int(w * 0.52), int(h * 0.27), int(w * 0.70),
               int(h * 0.37), int(w * 0.50),
               int(w * 0.10), int(h * 0.52), int(w * 0.78), int(h * 0.36)))


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

k.css("""
    /* ---------------------------------------------- takeover materials ----
       STYLE.md 2b: a takeover owns the frame. The plate is gone, so none of
       the over-footage rules apply — no glow budget, no band discipline, ink
       type on a light ground. What they must not do is look composed and
       centred. */
    .tk { position: absolute; inset: 0; }
    .tk.paper { background: var(--surface); }
    .tk.white { background: #ffffff; }
    .tk.blush { background: linear-gradient(150deg,#ffffff 0%,#fffafc 55%,
                                            #fdf4f8 100%); }
    /* graph paper — the texture every reference takeover has and mine had
       none of. 60px cells at 5.8% ink: visible, never a pattern you read. */
    .gp { position: absolute; inset: 0;
          background-image:
            repeating-linear-gradient(0deg, rgba(23,20,28,.058) 0 1px,
                                      transparent 1px 60px),
            repeating-linear-gradient(90deg, rgba(23,20,28,.058) 0 1px,
                                      transparent 1px 60px); }

    /* ---- TK1: the prompt, and the mess it makes ---- */
    .pbar { position: absolute; left: -70px; top: 250px; width: 1220px;
            height: 170px; background: var(--lit-ink); display: flex;
            align-items: center; padding: 0 110px; filter: var(--cast);
            overflow: hidden; }
    .pbar span { font-weight: 500; font-size: 52px; white-space: nowrap;
                 color: rgba(255,255,255,0.92); display: inline-block; }
    .pbar i { display: block; width: 7px; height: 62px; background: var(--pink);
              margin-left: 16px; flex: none; }
    .spill { position: absolute; height: 22px; border-radius: 4px;
             background: rgba(23,20,28,0.34); }

    /* ---- TK2: a wall of skeletons, bleeding off both sides ---- */
    .tile.brand.prod.xl { width: 300px; height: 300px; }
    .sk { position: absolute; width: 400px; height: 236px; background: #fff;
          border: 4px solid rgba(23,20,28,0.16); border-radius: 14px;
          overflow: hidden; }
    .sk b { position: absolute; display: block; border-radius: 3px;
            background: rgba(23,20,28,0.30); transform-origin: 0% 50%; }
    .sk b.h { background: #17141c; }
    .mnote { position: absolute; border: 4px dashed rgba(23,20,28,0.38);
             border-radius: 8px; display: grid; place-items: center;
             font-weight: 500; color: rgba(23,20,28,0.66); }

    /* ---- TK3: the skeleton with no card under it ---- */
    .fb { position: absolute; background: #17141c; transform-origin: 0% 50%; }
    .fbox { position: absolute; border: 8px dashed #17141c;
            display: grid; place-items: center; font-weight: 500;
            font-size: 44px; color: #17141c; }

    /* ---- TK4: five bands that fill the frame, then become swatches ----
       They sit at their *resting* size and scale up to fill, rather than
       sitting full-height and scaling down: a 26px radius stays 26px that
       way instead of stretching into a 260px ellipse during the slam. */
    .band { position: absolute; top: 546px; width: 216px; height: 190px;
            transform-origin: 50% 0%; }
    .bbh { position: absolute; left: 100px; top: 400px; font-weight: 500;
           font-size: 34px; letter-spacing: 0.18em; color: rgba(23,20,28,0.66); }
    .bbr { position: absolute; left: 100px; width: 880px; height: 2px;
           background: rgba(23,20,28,0.16); transform-origin: 0% 50%; }
    .hex { position: absolute; width: 216px; text-align: center;
           font-weight: 500; font-size: 22px; color: rgba(23,20,28,0.50); }
    .spec { position: absolute; font-weight: 900; line-height: 0.78;
            color: #17141c; }
    .chiprow { position: absolute; display: grid; place-items: center;
               font-weight: 500; color: #fff; }

    /* ---- TK5: the deck, too big for the frame ---- */
    .hero { position: absolute; left: -90px; top: 300px; width: 1260px;
            height: 1080px; border-radius: 52px; overflow: hidden;
            background: var(--lit); filter: var(--cast); }
    .hero .ht { position: absolute; left: 130px; top: 96px; font-weight: 900;
                font-size: 112px; letter-spacing: -0.03em; color: var(--accent); }
    .hero .hu { position: absolute; left: 130px; top: 254px; width: 180px;
                height: 16px; border-radius: 999px; background: var(--lit-pink); }
    .hero b { position: absolute; display: block; height: 18px;
              border-radius: 5px; background: rgba(23,20,28,0.40); }
    .hero .pic { position: absolute; left: 130px; top: 500px; width: 560px;
                 height: 340px; border-radius: 34px; background: var(--lit-pink);
                 box-shadow: var(--rim-dark); }
    .hero .tab { position: absolute; right: 0; top: 0; width: 300px;
                 height: 20px; background: var(--lit-accent); }
    .fan { position: absolute; border-radius: 52px; background: #fff;
           filter: var(--cast-sm); }

    /* ---- the finished artefact, in her system: behind-her beats ----
       One class for both, because they are the same object at different
       aspect ratios — a deck, a poster, a story, a card. Inner parts are
       proportional so a 340px story and a 620px banner stay consistent. */
    .dk { position: absolute; overflow: hidden; border-radius: 28px;
          background: var(--lit-blush); box-shadow: var(--rim);
          filter: var(--cast); }
    .dk i { position: absolute; display: block; }
    .dk .hb { left: 30px; top: 30px; height: 20px; border-radius: 6px;
              background: var(--lit-accent); }
    .dk .rr { left: 30px; height: 9px; border-radius: 4px;
              background: rgba(23,20,28,0.22); }
    .dk .pb { border-radius: 16px; background: var(--lit-pink);
              box-shadow: var(--rim-dark); }
""")


for _sel, _w, _h, _r in [
    (".slide", 620, 380, 40),
    (".tile.brand.prod", 250, 250, 60),
    (".dsys", 700, 420, 48),
    (".tile.brand.prod.xl", 300, 300, 76),
]:
    k.squircle(_sel, _w, _h, _r)


DECK_WALL = [('g2w0', -180, 120, 520, 360, -6.0), ('g2w1', 280, 60, 560, 380, 3.0), ('g2w2', 700, 140, 540, 370, -4.0), ('g2w3', -140, 460, 540, 370, 4.0), ('g2w4', 330, 430, 570, 390, -3.0), ('g2w5', 760, 500, 520, 360, 5.0), ('g2w6', -190, 810, 560, 380, -5.0), ('g2w7', 300, 830, 540, 370, 2.0), ('g2w8', 720, 870, 560, 380, -3.0)]

FAN_OUT = [('g12f0', 180, 80, 540, 330, -5.0), ('g12f1', 640, 30, 380, 520, 6.0), ('g12f2', -200, 480, 370, 370, 5.0), ('g12f3', 790, 600, 330, 580, -7.0), ('g12f4', 40, 900, 600, 240, 3.0), ('g12f5', 660, 1140, 430, 250, -5.0), ('g12f6', -150, 1080, 450, 300, 7.0)]


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
    """«пишеш — "зроби презентацію на таку тему" і він просто розкидує якусь
    інформацію по слайду»

    Takeover 1. The plate goes, the prompt bar runs wider than the frame, and
    the answer is thrown across all 1920px of it — 54 lines flung out from
    under the bar, most of them cropped by an edge.

    Captions are blacked out 15.28-17.44, because the bar types her sentence
    back at her; they return in ink over the light page for «розкидує».
    """
    html = '''
      <div class="g full" id="g2">
        <div class="tk paper"><div class="gp"></div></div>
        <div class="pbar" id="g2p" data-layout-allow-overflow>
          <span id="g2pt">зроби презентацію на таку тему</span><i id="g2pc"></i>
        </div>
        <i class="spill" id="g2s0" style="left:542px;top:1515px;width:953px;transform:rotate(-5.7deg)"></i>
        <i class="spill" id="g2s1" style="left:251px;top:677px;width:507px;transform:rotate(4.8deg)"></i>
        <i class="spill" id="g2s2" style="left:849px;top:1329px;width:870px;transform:rotate(3.5deg)"></i>
        <i class="spill" id="g2s3" style="left:285px;top:1255px;width:384px;transform:rotate(0.9deg)"></i>
        <i class="spill" id="g2s4" style="left:444px;top:1346px;width:737px;transform:rotate(-7.1deg)"></i>
        <i class="spill" id="g2s5" style="left:833px;top:684px;width:550px;transform:rotate(2.6deg)"></i>
        <i class="spill" id="g2s6" style="left:462px;top:1769px;width:262px;transform:rotate(4.8deg)"></i>
        <i class="spill" id="g2s7" style="left:754px;top:1409px;width:553px;transform:rotate(3.5deg)"></i>
        <i class="spill" id="g2s8" style="left:361px;top:839px;width:487px;transform:rotate(1.4deg)"></i>
        <i class="spill" id="g2s9" style="left:615px;top:1157px;width:819px;transform:rotate(0.4deg)"></i>
        <i class="spill" id="g2s10" style="left:441px;top:604px;width:885px;transform:rotate(7.1deg)"></i>
        <i class="spill" id="g2s11" style="left:-138px;top:842px;width:935px;transform:rotate(8.4deg)"></i>
        <i class="spill" id="g2s12" style="left:864px;top:1748px;width:300px;transform:rotate(3.4deg)"></i>
        <i class="spill" id="g2s13" style="left:49px;top:1762px;width:243px;transform:rotate(-3.8deg)"></i>
        <i class="spill" id="g2s14" style="left:434px;top:932px;width:402px;transform:rotate(-7.1deg)"></i>
        <i class="spill" id="g2s15" style="left:583px;top:1004px;width:843px;transform:rotate(-7.1deg)"></i>
        <i class="spill" id="g2s16" style="left:186px;top:500px;width:793px;transform:rotate(0.1deg)"></i>
        <i class="spill" id="g2s17" style="left:-80px;top:1370px;width:704px;transform:rotate(-3.8deg)"></i>
        <i class="spill" id="g2s18" style="left:412px;top:669px;width:484px;transform:rotate(-2.1deg)"></i>
        <i class="spill" id="g2s19" style="left:509px;top:890px;width:666px;transform:rotate(0.7deg)"></i>
        <i class="spill" id="g2s20" style="left:869px;top:540px;width:619px;transform:rotate(-7.6deg)"></i>
        <i class="spill" id="g2s21" style="left:196px;top:1464px;width:765px;transform:rotate(5.5deg)"></i>
        <i class="spill" id="g2s22" style="left:855px;top:727px;width:408px;transform:rotate(-6.8deg)"></i>
        <i class="spill" id="g2s23" style="left:741px;top:896px;width:317px;transform:rotate(1.2deg)"></i>
        <i class="spill" id="g2s24" style="left:587px;top:699px;width:958px;transform:rotate(-8.0deg)"></i>
        <i class="spill" id="g2s25" style="left:242px;top:1607px;width:827px;transform:rotate(-2.7deg)"></i>
        <i class="spill" id="g2s26" style="left:661px;top:1129px;width:659px;transform:rotate(-3.6deg)"></i>
        <i class="spill" id="g2s27" style="left:561px;top:626px;width:528px;transform:rotate(7.9deg)"></i>
        <i class="spill" id="g2s28" style="left:-28px;top:1543px;width:725px;transform:rotate(-4.5deg)"></i>
        <i class="spill" id="g2s29" style="left:439px;top:1624px;width:938px;transform:rotate(-7.2deg)"></i>
        <i class="spill" id="g2s30" style="left:-42px;top:1290px;width:569px;transform:rotate(6.0deg)"></i>
        <i class="spill" id="g2s31" style="left:-102px;top:1451px;width:949px;transform:rotate(-0.0deg)"></i>
        <i class="spill" id="g2s32" style="left:664px;top:1006px;width:250px;transform:rotate(-4.6deg)"></i>
        <i class="spill" id="g2s33" style="left:748px;top:569px;width:295px;transform:rotate(-5.9deg)"></i>
        <i class="spill" id="g2s34" style="left:140px;top:1250px;width:742px;transform:rotate(0.9deg)"></i>
        <i class="spill" id="g2s35" style="left:260px;top:480px;width:893px;transform:rotate(1.1deg)"></i>
        <i class="spill" id="g2s36" style="left:346px;top:1117px;width:457px;transform:rotate(8.5deg)"></i>
        <i class="spill" id="g2s37" style="left:698px;top:1325px;width:532px;transform:rotate(5.0deg)"></i>
        <i class="spill" id="g2s38" style="left:373px;top:834px;width:351px;transform:rotate(4.6deg)"></i>
        <i class="spill" id="g2s39" style="left:628px;top:898px;width:911px;transform:rotate(-8.5deg)"></i>
        <i class="spill" id="g2s40" style="left:468px;top:1461px;width:292px;transform:rotate(-4.0deg)"></i>
        <i class="spill" id="g2s41" style="left:670px;top:1260px;width:398px;transform:rotate(2.0deg)"></i>
        <i class="spill" id="g2s42" style="left:513px;top:551px;width:458px;transform:rotate(2.3deg)"></i>
        <i class="spill" id="g2s43" style="left:-2px;top:1039px;width:976px;transform:rotate(-4.5deg)"></i>
        <i class="spill" id="g2s44" style="left:-115px;top:635px;width:866px;transform:rotate(7.9deg)"></i>
        <i class="spill" id="g2s45" style="left:434px;top:895px;width:291px;transform:rotate(4.0deg)"></i>
        <i class="spill" id="g2s46" style="left:702px;top:675px;width:969px;transform:rotate(6.2deg)"></i>
        <i class="spill" id="g2s47" style="left:134px;top:1283px;width:538px;transform:rotate(8.1deg)"></i>
        <i class="spill" id="g2s48" style="left:-81px;top:1449px;width:440px;transform:rotate(-4.5deg)"></i>
        <i class="spill" id="g2s49" style="left:-53px;top:1305px;width:424px;transform:rotate(0.5deg)"></i>
        <i class="spill" id="g2s50" style="left:-20px;top:1275px;width:618px;transform:rotate(-7.0deg)"></i>
        <i class="spill" id="g2s51" style="left:-112px;top:784px;width:357px;transform:rotate(-5.7deg)"></i>
        <i class="spill" id="g2s52" style="left:875px;top:1121px;width:869px;transform:rotate(-3.5deg)"></i>
        <i class="spill" id="g2s53" style="left:-50px;top:670px;width:464px;transform:rotate(1.8deg)"></i>
      </div>'''
    js = '''
  gsap.set("#g2", {autoAlpha: 0});
  gsap.set("#g2p", {autoAlpha: 0, y: -40});
  gsap.set("#g2pt", {clipPath: "inset(0 100% 0 0)"});
  gsap.set("#g2pc", {x: -790});
  gsap.set("#g2 .spill", {autoAlpha: 0});
  tl.set("#g2", {autoAlpha: 1}, 15.28);
  tl.to("#g2p", {autoAlpha: 1, y: 0, duration: 0.26, ease: "power3.out"}, 15.30);
  // the bar types while she reads it out — 15.64 to 17.36 is her exact phrase.
  // clipPath, not width: a layout tween snaps to whole pixels and stutters.
  tl.to("#g2pt", {clipPath: "inset(0 0% 0 0)", duration: 1.62,
                  ease: "none"}, 15.66);
  tl.to("#g2pc", {x: 0, duration: 1.62, ease: "none"}, 15.66);
  // «розкидує» — and it throws the answer at the whole frame
  tl.fromTo("#g2s0", {x: -72, y: -1085, scale: 0.05, autoAlpha: 0}, {x: 0, y: 0, scale: 1, autoAlpha: 1, duration: 0.42, ease: "power3.out"}, 18.040);
  tl.fromTo("#g2s1", {x: 219, y: -247, scale: 0.05, autoAlpha: 0}, {x: 0, y: 0, scale: 1, autoAlpha: 1, duration: 0.45, ease: "power3.out"}, 18.050);
  tl.fromTo("#g2s2", {x: -379, y: -899, scale: 0.05, autoAlpha: 0}, {x: 0, y: 0, scale: 1, autoAlpha: 1, duration: 0.48, ease: "power3.out"}, 18.060);
  tl.fromTo("#g2s3", {x: 185, y: -825, scale: 0.05, autoAlpha: 0}, {x: 0, y: 0, scale: 1, autoAlpha: 1, duration: 0.51, ease: "power3.out"}, 18.070);
  tl.fromTo("#g2s4", {x: 26, y: -916, scale: 0.05, autoAlpha: 0}, {x: 0, y: 0, scale: 1, autoAlpha: 1, duration: 0.54, ease: "power3.out"}, 18.080);
  tl.fromTo("#g2s5", {x: -363, y: -254, scale: 0.05, autoAlpha: 0}, {x: 0, y: 0, scale: 1, autoAlpha: 1, duration: 0.42, ease: "power3.out"}, 18.090);
  tl.fromTo("#g2s6", {x: 8, y: -1339, scale: 0.05, autoAlpha: 0}, {x: 0, y: 0, scale: 1, autoAlpha: 1, duration: 0.45, ease: "power3.out"}, 18.100);
  tl.fromTo("#g2s7", {x: -284, y: -979, scale: 0.05, autoAlpha: 0}, {x: 0, y: 0, scale: 1, autoAlpha: 1, duration: 0.48, ease: "power3.out"}, 18.110);
  tl.fromTo("#g2s8", {x: 109, y: -409, scale: 0.05, autoAlpha: 0}, {x: 0, y: 0, scale: 1, autoAlpha: 1, duration: 0.51, ease: "power3.out"}, 18.120);
  tl.fromTo("#g2s9", {x: -145, y: -727, scale: 0.05, autoAlpha: 0}, {x: 0, y: 0, scale: 1, autoAlpha: 1, duration: 0.54, ease: "power3.out"}, 18.130);
  tl.fromTo("#g2s10", {x: 29, y: -174, scale: 0.05, autoAlpha: 0}, {x: 0, y: 0, scale: 1, autoAlpha: 1, duration: 0.42, ease: "power3.out"}, 18.140);
  tl.fromTo("#g2s11", {x: 608, y: -412, scale: 0.05, autoAlpha: 0}, {x: 0, y: 0, scale: 1, autoAlpha: 1, duration: 0.45, ease: "power3.out"}, 18.150);
  tl.fromTo("#g2s12", {x: -394, y: -1318, scale: 0.05, autoAlpha: 0}, {x: 0, y: 0, scale: 1, autoAlpha: 1, duration: 0.48, ease: "power3.out"}, 18.160);
  tl.fromTo("#g2s13", {x: 421, y: -1332, scale: 0.05, autoAlpha: 0}, {x: 0, y: 0, scale: 1, autoAlpha: 1, duration: 0.51, ease: "power3.out"}, 18.170);
  tl.fromTo("#g2s14", {x: 36, y: -502, scale: 0.05, autoAlpha: 0}, {x: 0, y: 0, scale: 1, autoAlpha: 1, duration: 0.54, ease: "power3.out"}, 18.180);
  tl.fromTo("#g2s15", {x: -113, y: -574, scale: 0.05, autoAlpha: 0}, {x: 0, y: 0, scale: 1, autoAlpha: 1, duration: 0.42, ease: "power3.out"}, 18.190);
  tl.fromTo("#g2s16", {x: 284, y: -70, scale: 0.05, autoAlpha: 0}, {x: 0, y: 0, scale: 1, autoAlpha: 1, duration: 0.45, ease: "power3.out"}, 18.200);
  tl.fromTo("#g2s17", {x: 550, y: -940, scale: 0.05, autoAlpha: 0}, {x: 0, y: 0, scale: 1, autoAlpha: 1, duration: 0.48, ease: "power3.out"}, 18.210);
  tl.fromTo("#g2s18", {x: 58, y: -239, scale: 0.05, autoAlpha: 0}, {x: 0, y: 0, scale: 1, autoAlpha: 1, duration: 0.51, ease: "power3.out"}, 18.220);
  tl.fromTo("#g2s19", {x: -39, y: -460, scale: 0.05, autoAlpha: 0}, {x: 0, y: 0, scale: 1, autoAlpha: 1, duration: 0.54, ease: "power3.out"}, 18.230);
  tl.fromTo("#g2s20", {x: -399, y: -110, scale: 0.05, autoAlpha: 0}, {x: 0, y: 0, scale: 1, autoAlpha: 1, duration: 0.42, ease: "power3.out"}, 18.240);
  tl.fromTo("#g2s21", {x: 274, y: -1034, scale: 0.05, autoAlpha: 0}, {x: 0, y: 0, scale: 1, autoAlpha: 1, duration: 0.45, ease: "power3.out"}, 18.250);
  tl.fromTo("#g2s22", {x: -385, y: -297, scale: 0.05, autoAlpha: 0}, {x: 0, y: 0, scale: 1, autoAlpha: 1, duration: 0.48, ease: "power3.out"}, 18.260);
  tl.fromTo("#g2s23", {x: -271, y: -466, scale: 0.05, autoAlpha: 0}, {x: 0, y: 0, scale: 1, autoAlpha: 1, duration: 0.51, ease: "power3.out"}, 18.270);
  tl.fromTo("#g2s24", {x: -117, y: -269, scale: 0.05, autoAlpha: 0}, {x: 0, y: 0, scale: 1, autoAlpha: 1, duration: 0.54, ease: "power3.out"}, 18.280);
  tl.fromTo("#g2s25", {x: 228, y: -1177, scale: 0.05, autoAlpha: 0}, {x: 0, y: 0, scale: 1, autoAlpha: 1, duration: 0.42, ease: "power3.out"}, 18.290);
  tl.fromTo("#g2s26", {x: -191, y: -699, scale: 0.05, autoAlpha: 0}, {x: 0, y: 0, scale: 1, autoAlpha: 1, duration: 0.45, ease: "power3.out"}, 18.300);
  tl.fromTo("#g2s27", {x: -91, y: -196, scale: 0.05, autoAlpha: 0}, {x: 0, y: 0, scale: 1, autoAlpha: 1, duration: 0.48, ease: "power3.out"}, 18.310);
  tl.fromTo("#g2s28", {x: 498, y: -1113, scale: 0.05, autoAlpha: 0}, {x: 0, y: 0, scale: 1, autoAlpha: 1, duration: 0.51, ease: "power3.out"}, 18.320);
  tl.fromTo("#g2s29", {x: 31, y: -1194, scale: 0.05, autoAlpha: 0}, {x: 0, y: 0, scale: 1, autoAlpha: 1, duration: 0.54, ease: "power3.out"}, 18.330);
  tl.fromTo("#g2s30", {x: 512, y: -860, scale: 0.05, autoAlpha: 0}, {x: 0, y: 0, scale: 1, autoAlpha: 1, duration: 0.42, ease: "power3.out"}, 18.340);
  tl.fromTo("#g2s31", {x: 572, y: -1021, scale: 0.05, autoAlpha: 0}, {x: 0, y: 0, scale: 1, autoAlpha: 1, duration: 0.45, ease: "power3.out"}, 18.350);
  tl.fromTo("#g2s32", {x: -194, y: -576, scale: 0.05, autoAlpha: 0}, {x: 0, y: 0, scale: 1, autoAlpha: 1, duration: 0.48, ease: "power3.out"}, 18.360);
  tl.fromTo("#g2s33", {x: -278, y: -139, scale: 0.05, autoAlpha: 0}, {x: 0, y: 0, scale: 1, autoAlpha: 1, duration: 0.51, ease: "power3.out"}, 18.370);
  tl.fromTo("#g2s34", {x: 330, y: -820, scale: 0.05, autoAlpha: 0}, {x: 0, y: 0, scale: 1, autoAlpha: 1, duration: 0.54, ease: "power3.out"}, 18.380);
  tl.fromTo("#g2s35", {x: 210, y: -50, scale: 0.05, autoAlpha: 0}, {x: 0, y: 0, scale: 1, autoAlpha: 1, duration: 0.42, ease: "power3.out"}, 18.390);
  tl.fromTo("#g2s36", {x: 124, y: -687, scale: 0.05, autoAlpha: 0}, {x: 0, y: 0, scale: 1, autoAlpha: 1, duration: 0.45, ease: "power3.out"}, 18.400);
  tl.fromTo("#g2s37", {x: -228, y: -895, scale: 0.05, autoAlpha: 0}, {x: 0, y: 0, scale: 1, autoAlpha: 1, duration: 0.48, ease: "power3.out"}, 18.410);
  tl.fromTo("#g2s38", {x: 97, y: -404, scale: 0.05, autoAlpha: 0}, {x: 0, y: 0, scale: 1, autoAlpha: 1, duration: 0.51, ease: "power3.out"}, 18.420);
  tl.fromTo("#g2s39", {x: -158, y: -468, scale: 0.05, autoAlpha: 0}, {x: 0, y: 0, scale: 1, autoAlpha: 1, duration: 0.54, ease: "power3.out"}, 18.430);
  tl.fromTo("#g2s40", {x: 2, y: -1031, scale: 0.05, autoAlpha: 0}, {x: 0, y: 0, scale: 1, autoAlpha: 1, duration: 0.42, ease: "power3.out"}, 18.440);
  tl.fromTo("#g2s41", {x: -200, y: -830, scale: 0.05, autoAlpha: 0}, {x: 0, y: 0, scale: 1, autoAlpha: 1, duration: 0.45, ease: "power3.out"}, 18.450);
  tl.fromTo("#g2s42", {x: -43, y: -121, scale: 0.05, autoAlpha: 0}, {x: 0, y: 0, scale: 1, autoAlpha: 1, duration: 0.48, ease: "power3.out"}, 18.460);
  tl.fromTo("#g2s43", {x: 472, y: -609, scale: 0.05, autoAlpha: 0}, {x: 0, y: 0, scale: 1, autoAlpha: 1, duration: 0.51, ease: "power3.out"}, 18.470);
  tl.fromTo("#g2s44", {x: 585, y: -205, scale: 0.05, autoAlpha: 0}, {x: 0, y: 0, scale: 1, autoAlpha: 1, duration: 0.54, ease: "power3.out"}, 18.480);
  tl.fromTo("#g2s45", {x: 36, y: -465, scale: 0.05, autoAlpha: 0}, {x: 0, y: 0, scale: 1, autoAlpha: 1, duration: 0.42, ease: "power3.out"}, 18.490);
  tl.fromTo("#g2s46", {x: -232, y: -245, scale: 0.05, autoAlpha: 0}, {x: 0, y: 0, scale: 1, autoAlpha: 1, duration: 0.45, ease: "power3.out"}, 18.500);
  tl.fromTo("#g2s47", {x: 336, y: -853, scale: 0.05, autoAlpha: 0}, {x: 0, y: 0, scale: 1, autoAlpha: 1, duration: 0.48, ease: "power3.out"}, 18.510);
  tl.fromTo("#g2s48", {x: 551, y: -1019, scale: 0.05, autoAlpha: 0}, {x: 0, y: 0, scale: 1, autoAlpha: 1, duration: 0.51, ease: "power3.out"}, 18.520);
  tl.fromTo("#g2s49", {x: 523, y: -875, scale: 0.05, autoAlpha: 0}, {x: 0, y: 0, scale: 1, autoAlpha: 1, duration: 0.54, ease: "power3.out"}, 18.530);
  tl.fromTo("#g2s50", {x: 490, y: -845, scale: 0.05, autoAlpha: 0}, {x: 0, y: 0, scale: 1, autoAlpha: 1, duration: 0.42, ease: "power3.out"}, 18.540);
  tl.fromTo("#g2s51", {x: 582, y: -354, scale: 0.05, autoAlpha: 0}, {x: 0, y: 0, scale: 1, autoAlpha: 1, duration: 0.45, ease: "power3.out"}, 18.550);
  tl.fromTo("#g2s52", {x: -405, y: -691, scale: 0.05, autoAlpha: 0}, {x: 0, y: 0, scale: 1, autoAlpha: 1, duration: 0.48, ease: "power3.out"}, 18.560);
  tl.fromTo("#g2s53", {x: 520, y: -240, scale: 0.05, autoAlpha: 0}, {x: 0, y: 0, scale: 1, autoAlpha: 1, duration: 0.51, ease: "power3.out"}, 18.570);
  tl.to("#g2p", {y: -230, duration: 0.50, ease: "power2.inOut"}, 18.04);
  tl.to("#g2", {autoAlpha: 0, duration: 0.24, ease: "power2.in"}, 20.45);'''
    return html, js


@beat
def b02b_deck_wall():
    """«Але ГАРНІ презентації зі штучним інтелектом реально ЗРОБИТИ»

    A wall of finished decks rises from under the frame and keeps going past
    the top of it — nine cards, bleeding off both sides. Matted, so it passes
    behind her head rather than sitting on it (STYLE.md 1).

    This is the turn of the reel: everything before it was the mess the AI
    makes, and this is the claim that it does not have to be. So it is the
    biggest object so far, and it arrives while she is still saying it.
    """
    html = '''
      <div class="g full" id="g2w">
        %s
      </div>''' % "\n        ".join(
        dcard(i, x, y, w, h) for i, x, y, w, h, r in DECK_WALL)
    sets = "\n".join(
        '  gsap.set("#%s", {rotation: %s, y: 560, scale: 0.92, autoAlpha: 0,'
        ' transformOrigin: "50%% 50%%"});' % (i, r)
        for i, x, y, w, h, r in DECK_WALL)
    rises = "\n".join(
        '  tl.to("#%s", {y: 0, scale: 1, autoAlpha: 1, duration: 0.54,'
        ' ease: "back.out(1.5)"}, %.3f);' % (i, 20.68 + n * 0.195)
        for n, (i, x, y, w, h, r) in enumerate(DECK_WALL))
    js = '''
  gsap.set("#g2w", {autoAlpha: 0});
%s
  tl.set("#g2w", {autoAlpha: 1}, 20.55);
  // «Гарні презентації… штучним інтелектом» — one card per beat of the phrase
%s
  // «реально зробити» — and the whole wall settles as one thing
  tl.to("#g2w", {scale: 1.03, duration: 0.42, ease: "power2.out",
                 transformOrigin: "50%% 60%%"}, 22.64);
  tl.to("#g2w", {autoAlpha: 0, duration: 0.30, ease: "power2.in"}, 24.00);''' % (
        sets, rises)
    return html, js


# She goes back on top for this beat: nine decks rising past the top of the
# frame would otherwise be stuck to her head. 114 frames, ~3 min of CPU.
k.matte("deckwall", 20.533, 3.800)


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
    """«Отже, перший крок — відкриваєш канву або гугл презентації»

    Opening of takeover 2. The marks land at 300px rather than in a 250px
    tile: they are the two products, and they should read across a room.
    """
    html = '''
      <div class="g full" id="g6">
        <div class="tk paper" id="g6bg"><div class="gp"></div></div>
        <div class="tile brand prod xl" id="g6a" style="left:110px;top:130px">%s</div>
        <div class="tile brand prod xl" id="g6b" style="left:670px;top:130px">%s</div>
      </div>''' % (mark("canva-mark"), mark("gslides-mark"))
    js = '''
  gsap.set("#g6", {autoAlpha: 0});
  gsap.set("#g6a, #g6b", {autoAlpha: 0, scale: 0.55, y: -70,
                          transformOrigin: "50% 50%"});
  tl.set("#g6", {autoAlpha: 1}, 41.22);
  // «канву»
  tl.to("#g6a", {autoAlpha: 1, scale: 1, y: 0, duration: 0.36,
                 ease: "back.out(2.6)"}, 42.90);
  // «гугл презентації»
  tl.to("#g6b", {autoAlpha: 1, scale: 1, y: 0, duration: 0.36,
                 ease: "back.out(2.6)"}, 43.60);
  // they retreat once the wall starts building under them
  tl.to("#g6a, #g6b", {scale: 0.58, y: -104, duration: 0.44,
                       ease: "power2.inOut"}, 45.40);
  // the marks go — the wall is the subject now, and STYLE.md 4a.3 says a
  // graphic must not outstay its sentence. But #g6 carries the paper ground
  // for the whole takeover, so only its children leave: dropping the wrapper
  // here put her footage back behind the wall for the entire push-in.
  tl.to("#g6a, #g6b", {autoAlpha: 0, scale: 0.50, y: -160, duration: 0.34,
                       ease: "power2.in"}, 47.30);
  tl.to("#g6", {autoAlpha: 0, duration: 0.24, ease: "power2.in"}, 54.35);'''
    return html, js


@beat
def b07_skeleton_built():
    """«коротко накидаєш скелет: що має бути на кожному слайді… якщо хочеш
    картинку чи графік, то просто прописуєш збоку»

    Takeover 2 proper: twelve slides in a wall that runs off both sides and
    the bottom, sketching themselves one at a time. Then the frame pushes in
    so the margin notes get written at a size you can actually read.

    The push-in numbers are solved, not eyeballed: to bring a point p to the
    centre c at scale k the wrapper needs offset c - (c + (p - c)k), so
    centring (420, 640) at k=1.7 is x=204, y=544.

    Captions are blacked out 51.10-52.15 only — that is exactly where the
    notes spell «картинка» and «графік» while she says those two words.
    """
    cells = []
    for r in range(4):
        for c in range(3):
            i = r * 3 + c
            rows = [3, 2, 4, 3, 2, 3, 4, 2, 3, 3, 4, 2][i]
            bars = "".join(
                '<b style="left:28px;top:%dpx;width:%dpx;height:7px"></b>'
                % (72 + n * 26, [318, 262, 300, 214, 286][(i + n) % 5])
                for n in range(rows))
            cells.append(
                '<div class="sk" id="g7c%d" data-layout-allow-overflow'' style="left:%dpx;top:%dpx">'
                '<b class="h" style="left:28px;top:28px;width:%dpx;height:11px"></b>'
                '%s</div>' % (i, -100 + c * 440, 430 + r * 276,
                              [240, 196, 260, 212, 178, 230][i % 6], bars))
    html = '''
      <div class="g full" id="g7">
        <div id="g7w" style="position:absolute;inset:0">
          %s
          <div class="mnote" id="g7n1" style="left:368px;top:502px;width:150px;height:110px;font-size:26px">графік</div>
          <div class="mnote" id="g7n2" style="left:368px;top:778px;width:186px;height:110px;font-size:26px">картинка</div>
        </div>
      </div>''' % "\n          ".join(cells)
    js = '''
  gsap.set("#g7", {autoAlpha: 0});
  gsap.set("#g7w", {transformOrigin: "50% 50%"});
  gsap.set("#g7 .sk", {autoAlpha: 0, scale: 0.86, transformOrigin: "50% 50%"});
  gsap.set("#g7 .sk b", {scaleX: 0});
  gsap.set("#g7 .mnote", {autoAlpha: 0, scale: 0.6, transformOrigin: "50% 50%"});
  tl.set("#g7", {autoAlpha: 1}, 44.30);
  // «накидаєш скелет» — the wall arrives, then writes itself
  tl.to("#g7 .sk", {autoAlpha: 1, scale: 1, duration: 0.30, ease: "back.out(2)",
                    stagger: {each: 0.055, from: "start"}}, 44.40);
  tl.to("#g7 .sk b", {scaleX: 1, duration: 0.22, ease: "power2.out",
                      stagger: {each: 0.016, from: "start"}}, 45.10);
  // «Десь пишеш загальні сенси, десь розписуєш детальніше» — push in
  tl.to("#g7w", {scale: 1.7, x: 204, y: 544, duration: 1.30,
                 ease: "power2.inOut"}, 48.20);
  // «картинку» / «графік» — written into the margin, each on its own word
  tl.to("#g7n2", {autoAlpha: 1, scale: 1, duration: 0.30,
                  ease: "back.out(2.4)"}, 51.16);
  tl.to("#g7n1", {autoAlpha: 1, scale: 1, duration: 0.30,
                  ease: "back.out(2.4)"}, 51.72);
  // «збоку, що тут має бути» — ease back out
  tl.to("#g7w", {scale: 1.3, x: 150, y: 400, duration: 0.90,
                 ease: "power2.inOut"}, 53.00);
  tl.to("#g7", {autoAlpha: 0, duration: 0.24, ease: "power2.in"}, 54.35);'''
    return html, js


@beat
def b08_black_and_white():
    """«І в результаті маєш чорно-білий скелет: текст на білому фоні, без
    жодного дизайну»

    Takeover 3, and the only frame in the reel with none of her palette in it.
    No card, no border, no radius — the rules sit straight on the frame and
    run nearly edge to edge. The flatness is the point: this is the "before"
    that makes 96s land, so it has to be genuinely bleak.

    Captions stay on and invert to ink. White type would be invisible here,
    which is what the kit's new `invert` span is for.
    """
    body = "".join(
        '<i class="fb" style="left:80px;top:%dpx;width:%dpx;height:20px"></i>'
        % (640 + n * 74, w)
        for n, w in enumerate([920, 878, 940, 816, 900, 642]))
    html = '''
      <div class="g full" id="g8">
        <div class="tk white"></div>
        <i class="fb" id="g8h" style="left:80px;top:420px;width:900px;height:58px"></i>
        <i class="fb" id="g8u" style="left:80px;top:520px;width:520px;height:22px"></i>
        <div id="g8b">%s</div>
        <div class="fbox" id="g8p" style="left:80px;top:1168px;width:560px;height:372px">картинка</div>
        <i class="fb" id="g8r1" style="left:684px;top:1200px;width:296px;height:20px"></i>
        <i class="fb" id="g8r2" style="left:684px;top:1274px;width:252px;height:20px"></i>
        <i class="fb" id="g8r3" style="left:684px;top:1348px;width:280px;height:20px"></i>
      </div>''' % body
    js = '''
  gsap.set("#g8", {autoAlpha: 0});
  gsap.set("#g8 .fb", {scaleX: 0});
  gsap.set("#g8p", {autoAlpha: 0});
  tl.set("#g8", {autoAlpha: 1}, 54.42);
  // «чорно-білий скелет» — all of it wipes on, left to right, fast
  tl.to("#g8h", {scaleX: 1, duration: 0.24, ease: "power3.out"}, 54.50);
  tl.to("#g8u", {scaleX: 1, duration: 0.20, ease: "power3.out"}, 54.76);
  tl.to("#g8b .fb", {scaleX: 1, duration: 0.20, ease: "power2.out",
                     stagger: 0.045}, 55.00);
  tl.to("#g8r1, #g8r2, #g8r3", {scaleX: 1, duration: 0.20, ease: "power2.out",
                                stagger: 0.05}, 55.40);
  tl.to("#g8p", {autoAlpha: 1, duration: 0.18}, 55.62);
  // «без жодного дизайну» — and then nothing happens at all, on purpose
  tl.to("#g8", {autoAlpha: 0, duration: 0.24, ease: "power2.in"}, 58.70);'''
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
def b12_system_fills():
    """«Хвилин через п\u2019ять маєш готову дизайн-систему з кольорами,
    шрифтами, елементами — коротше, брендбук»

    Takeover 4, and the loudest frame in the reel: five bands fill the whole
    height for about two seconds — the screen is nothing but her colours —
    then drop into the swatch row of a brandbook that builds under them, one
    section per word.

    Captions blacked out for the whole beat. The page is text, and its header
    reads ДИЗАЙН-СИСТЕМА while she says «дизайн-систему».
    """
    bands = "".join(
        '<i class="band" id="g12b%d" style="left:%dpx;background:%s"></i>'
        % (i, i * 216, bg) for i, bg in enumerate([
            "var(--lit-accent)", "var(--accent-deep)", "var(--lit-pink)",
            "var(--container-high)", "var(--lit-ink)"]))
    hexes = "".join(
        '<div class="hex" id="g12x%d" style="left:%dpx;top:750px">%s</div>'
        % (i, i * 216, h) for i, h in enumerate(
            ["B4122F", "8D0D24", "FF6E9C", "F4DFE5", "17141C"]))
    html = '''
      <div class="g full" id="g12">
        <div class="tk paper" id="g12bg"><div class="gp"></div></div>
        %s
        %s
        <div class="bbh" id="g12h">ДИЗАЙН-СИСТЕМА</div>
        <i class="bbr" id="g12r1" style="top:464px"></i>
        <i class="bbr" id="g12r2" style="top:834px"></i>
        <i class="bbr" id="g12r3" style="top:1238px"></i>
        <div class="spec" id="g12s" style="left:96px;top:898px;font-size:280px">Аа</div>
        <div id="g12l" style="position:absolute;left:520px;top:914px">
          <div style="font-weight:900;font-size:66px;color:#17141c;line-height:1.18">Заголовок</div>
          <div style="font-weight:500;font-size:46px;color:#17141c;opacity:.82;line-height:1.24">Підзаголовок</div>
          <div style="font-weight:500;font-size:32px;color:#17141c;opacity:.60;line-height:1.3">Основний текст</div>
        </div>
        <div class="chiprow" id="g12c1" style="left:100px;top:1302px;width:300px;height:96px;border-radius:999px;background:var(--lit-accent);font-size:36px">Кнопка</div>
        <div class="chiprow" id="g12c2" style="left:426px;top:1302px;width:200px;height:96px;border-radius:999px;background:var(--lit-pink)"></div>
        <div class="chiprow" id="g12c3" style="left:652px;top:1302px;width:160px;height:96px;border-radius:30px;background:var(--lit);box-shadow:var(--rim)"></div>
      </div>''' % (bands, hexes)
    js = '''
  gsap.set("#g12", {autoAlpha: 0});
  gsap.set("#g12bg, #g12h, #g12 .bbr, #g12s, #g12l, #g12 .hex", {autoAlpha: 0});
  gsap.set("#g12c1, #g12c2, #g12c3", {autoAlpha: 0, scaleX: 0.3,
                                      transformOrigin: "0% 50%"});
  // resting size is the swatch; the slam is that scaled up to fill the frame,
  // so the 26px radius stays 26px instead of stretching to a 260px ellipse
  gsap.set("#g12 .band", {scaleY: 0, y: -546, borderRadius: 0});
  tl.set("#g12", {autoAlpha: 1}, 72.52);
  // «Хвилин через п'ять» — the whole frame goes to colour, and stays there
  tl.to("#g12 .band", {scaleY: 10.11, duration: 0.42, ease: "power3.out",
                       stagger: 0.055}, 72.60);
  // «дизайн-систему» — the bands drop into a swatch row, page appears under
  tl.to("#g12bg", {autoAlpha: 1, duration: 0.24}, 74.46);
  tl.to("#g12 .band", {scaleY: 1, y: 0, borderRadius: 26, duration: 0.58,
                       ease: "power2.inOut", stagger: 0.03}, 74.46);
  tl.to("#g12h, #g12r1", {autoAlpha: 1, duration: 0.26}, 74.84);
  // «кольорами»
  tl.to("#g12 .hex", {autoAlpha: 1, duration: 0.22, stagger: 0.04}, 75.36);
  // «шрифтами»
  tl.to("#g12r2", {autoAlpha: 1, duration: 0.20}, 75.90);
  tl.to("#g12s, #g12l", {autoAlpha: 1, duration: 0.26, ease: "power2.out"}, 75.96);
  // «елементами»
  tl.to("#g12r3", {autoAlpha: 1, duration: 0.20}, 76.42);
  tl.to("#g12c1, #g12c2, #g12c3", {autoAlpha: 1, scaleX: 1, duration: 0.26,
                                   ease: "back.out(2.2)", stagger: 0.06}, 76.48);
  tl.to("#g12", {autoAlpha: 0, duration: 0.26, ease: "power2.in"}, 78.20);'''
    return html, js


# --------------------------------------------------- D · step 3, and the payoff


@beat
def b12b_fan_out():
    """«і вона потім працює не тільки для ПРЕЗЕНТАЦІЙ, а взагалі для
    БУДЬ-ЯКОГО ДИЗАЙНУ»

    Seven artefacts burst out from behind her head and leave the frame on
    every side — a deck, a poster, a square, a story, a banner, a card, a
    page. Matted, so they come from *behind* her, which is the whole reason
    the beat reads as the system radiating outwards rather than a grid
    appearing.

    The slide goes first, on «презентацій». The other six go on «будь-якого
    дизайну», because that is the word that means all the rest.
    """
    html = '''
      <div class="g full" id="g12f">
        %s
      </div>''' % "\n        ".join(
        dcard(i, x, y, w, h) for i, x, y, w, h, r in FAN_OUT)
    # everything starts as one point behind her head, at 540 x 620
    sets = "\n".join(
        '  gsap.set("#%s", {x: %d, y: %d, rotation: 0, scale: 0.06,'
        ' autoAlpha: 0, transformOrigin: "50%% 50%%"});'
        % (i, 540 - (x + w // 2), 620 - (y + h // 2))
        for i, x, y, w, h, r in FAN_OUT)
    first = FAN_OUT[0]
    rest = "\n".join(
        '  tl.to("#%s", {x: 0, y: 0, rotation: %s, scale: 1, autoAlpha: 1,'
        ' duration: 0.66, ease: "power3.out"}, %.3f);' % (i, r, 80.96 + n * 0.085)
        for n, (i, x, y, w, h, r) in enumerate(FAN_OUT[1:]))
    js = '''
  gsap.set("#g12f", {autoAlpha: 0});
%s
  tl.set("#g12f", {autoAlpha: 1}, 78.30);
  // «презентацій» — the one it was built for
  tl.to("#%s", {x: 0, y: 0, rotation: %s, scale: 1, autoAlpha: 1,
                duration: 0.62, ease: "power3.out"}, 79.60);
  // «будь-якого дизайну» — and everything else it also does
%s
  tl.to("#g12f", {autoAlpha: 0, duration: 0.30, ease: "power2.in"}, 82.05);''' % (
        sets, first[0], first[5], rest)
    return html, js


# Same again — the artefacts fly out from *behind* her, which is the whole
# reason the beat reads as the system radiating rather than a grid appearing.
k.matte("fanout", 78.300, 3.800)


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
  tl.set("#g14", {autoAlpha: 1}, 92.55);
  tl.to("#g14c", {autoAlpha: 1, scale: 1, duration: 0.34, ease: "back.out(2.4)"}, 92.70);
  tl.to("#g14 .steam", {autoAlpha: 1, scaleY: 1, duration: 0.40,
                        ease: "power2.out", stagger: 0.10}, 93.50);
  tl.to("#g14", {autoAlpha: 0, duration: 0.24, ease: "power2.in"}, 93.85);'''
    return html, js


@beat
def b15_it_is_done():
    """«через п\u2019ять-десять хвилин в тебе буде вже готова гарно задизайнена
    презентація, яку треба хіба що трошки підправити»

    Takeover 5, the payoff, and deliberately too big for the frame — the slide
    runs off both sides and three more sit behind it. It is the *same* object
    as the white skeleton at 54s: same picture box, same ragged body, same
    heading position. Only now it is dressed.

    Captions stay on, inverted. The heading reads «Як це працює», which is not
    a phrase she speaks here, so there is nothing to double up on.
    """
    body = "".join(
        '<b style="left:130px;top:%dpx;width:%dpx"></b>' % (306 + n * 62, w)
        for n, w in enumerate([560, 490, 530]))
    side = "".join(
        '<b style="left:760px;top:%dpx;width:%dpx"></b>' % (520 + n * 62, w)
        for n, w in enumerate([300, 250, 284, 190]))
    html = '''
      <div class="g full" id="g15">
        <div class="tk blush" id="g15bg"></div>
        <div class="big" id="g15n" style="top:740px;font-size:300px;color:#b4122f;text-shadow:none">5-10<small> хв</small></div>
        <div class="fan" id="g15f1" data-layout-allow-overflow style="left:-60px;top:206px;width:1200px;height:1080px"></div>
        <div class="fan" id="g15f2" data-layout-allow-overflow style="left:-100px;top:250px;width:1280px;height:1080px"></div>
        <div class="hero" id="g15h" data-layout-allow-overflow>
          <i class="tab"></i>
          <div class="ht">Як це працює</div>
          <div class="hu"></div>
          %s
          <div class="pic"></div>
          %s
        </div>
      </div>''' % (body, side)
    js = '''
  gsap.set("#g15", {autoAlpha: 0});
  gsap.set("#g15bg", {autoAlpha: 0});
  gsap.set("#g15n", {autoAlpha: 0, scale: 0.55, transformOrigin: "50% 50%"});
  gsap.set("#g15h", {autoAlpha: 0, scale: 1.22, transformOrigin: "50% 50%"});
  gsap.set("#g15f1, #g15f2", {autoAlpha: 0, rotation: 0,
                              transformOrigin: "50% 100%"});
  tl.set("#g15", {autoAlpha: 1}, 93.95);
  tl.to("#g15bg", {autoAlpha: 1, duration: 0.26}, 93.97);
  // «п'ять-десять хвилин» — a number is the one word §4 allows
  tl.to("#g15n", {autoAlpha: 1, scale: 1, duration: 0.34,
                  ease: "back.out(2.8)"}, 94.28);
  tl.to("#g15n", {autoAlpha: 0, scale: 0.8, duration: 0.26,
                  ease: "power2.in"}, 96.20);
  // «гарно задизайнена презентація» — the deck lands, bigger than the frame
  tl.to("#g15f1", {autoAlpha: 1, rotation: -7.0, duration: 0.46,
                   ease: "back.out(1.8)"}, 96.52);
  tl.to("#g15f2", {autoAlpha: 1, rotation: 4.5, duration: 0.46,
                   ease: "back.out(1.8)"}, 96.58);
  tl.to("#g15h", {autoAlpha: 1, scale: 1, duration: 0.50,
                  ease: "back.out(1.9)"}, 96.64);
  tl.to("#g15", {autoAlpha: 0, duration: 0.28, ease: "power2.in"}, 99.00);'''
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


# Captions drop ONLY where a takeover's own text would say the word she is
# already saying — her rule, 2026-09-15: "the no subtitles only affects
# animations that have text, so that its not like subtitles say 10 euros and
# animation also says 10 euros". Everything else keeps its captions.
BLACKOUT = [
    (15.28, 17.44, "TK1 — the bar types «зроби презентацію на таку тему»"),
    (51.10, 52.15, "TK2 — the margin notes write «картинка» / «графік»"),
    (72.52, 78.20, "TK4 — the brandbook page, header says ДИЗАЙН-СИСТЕМА"),
]

# Over a light takeover white captions are invisible, so they set in ink.
INVERT = [
    (17.44, 20.45, "TK1 — the mess, on paper"),
    (41.22, 58.70, "TK2 into TK3 — paper, then flat white, no plate between"),
    (93.95, 99.00, "TK5 — the blushed deck"),
]


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
        blackout=BLACKOUT,
        invert=INVERT,
    )
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "index.html")
    io.open(out, "w", encoding="utf-8").write(doc)
    print("index.html  %d captions, %d beats, %.1f KB"
          % (len(caps), len(BEATS), os.path.getsize(out) / 1024.0))


main()
