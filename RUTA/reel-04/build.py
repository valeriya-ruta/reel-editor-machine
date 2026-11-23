# -*- coding: utf-8 -*-
"""Reel 4 — «Мобін: Пінтерест для розробників».

Variant B: her cut, graded, no subtitles. This owns animations and captions.
Materials come from tools/kit.py (STYLE.md §5a); what each beat depicts is
invented for this script.

Two beats use her own Mobbin screen capture — the sections reel 3 did not
touch, so the pair does not read as the same reel twice.

usage: python build.py
"""
import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
from kit import Kit  # noqa: E402

DUR = 67.400
k = Kit(width=1080, height=1920, fps=30, duration=DUR)

# She cut «плюс відео, як екран переходить в екран» from the written script, so
# the swipe capture lands on «скріншоти кожного етапу користування» instead —
# her actual words for the same idea.
BEATS = []


def beat(fn):
    BEATS.append(fn)
    return fn


# ---------------------------------------------------------------- A · the problem

@beat
def b01_functions_are_easy():
    """«Розробити функції додатку — це найпростіша частина.»

    Four rows tick through almost too fast to read: building the functions is
    not where the difficulty is.
    """
    rows = "".join('<i class="fnrow" id="b1r%d"><b class="fnfill"></b></i>' % i
                   for i in range(4))
    html = '''
      <div class="g" id="g1">
        <div class="card fnlist" id="g1c">%s</div>
      </div>''' % rows
    js = '''
  gsap.set("#g1", {autoAlpha: 0});
  gsap.set("#g1c", {scale: 0.92, transformOrigin: "50% 50%"});
  gsap.set(".fnfill", {scaleX: 0, transformOrigin: "0% 50%"});
  tl.to("#g1", {autoAlpha: 1, duration: 0.16}, 1.70);
  tl.to("#g1c", {scale: 1, duration: 0.30, ease: "power3.out"}, 1.70);
  ["#b1r0 .fnfill","#b1r1 .fnfill","#b1r2 .fnfill","#b1r3 .fnfill"].forEach(function (s, i) {
    tl.to(s, {scaleX: 1, duration: 0.16, ease: "power2.out"}, 2.16 + i * 0.17);
  });
  tl.to("#g1", {autoAlpha: 0, duration: 0.24, ease: "power2.in"}, 4.30);'''
    return html, js


@beat
def b02_real_app_then_scatter():
    """«щоб в ньому виглядати як справжній додаток… а не просто набір цифр,
    букв і кнопок, розкиданих по екрану»

    One object, two states — STYLE.md's «reuse objects». The screen lands
    composed on «справжній», then on «розкиданих» its own contents fly apart.
    """
    html = '''
      <div class="g" id="g2">
        <div class="phone" id="g2p">
          <span class="pscr" id="g2s">
            <b class="ph" id="g2e0"></b>
            <b class="pr" id="g2e1"></b>
            <b class="pr" id="g2e2"></b>
            <b class="pr" id="g2e3"></b>
          </span>
        </div>
        <i class="loose l0" id="g2l0"></i><i class="loose l1" id="g2l1"></i>
        <i class="loose l2" id="g2l2"></i><i class="loose l3" id="g2l3"></i>
      </div>'''
    js = '''
  gsap.set("#g2", {autoAlpha: 0});
  gsap.set("#g2p", {scale: 0.74, transformOrigin: "50% 50%"});
  gsap.set(["#g2e0","#g2e1","#g2e2","#g2e3"], {autoAlpha: 0, y: 26});
  tl.to("#g2", {autoAlpha: 1, duration: 0.18}, 4.90);
  tl.to("#g2p", {scale: 1, duration: 0.38, ease: "back.out(1.7)"}, 4.90);
  ["#g2e0","#g2e1","#g2e2","#g2e3"].forEach(function (s, i) {
    tl.to(s, {autoAlpha: 1, y: 0, duration: 0.20, ease: "power3.out"}, 5.38 + i * 0.13);
  });
  // «розкиданих по екрану» — the phone goes and its parts are left loose in
  // the frame. Scattering them inside the phone was invisible: clip-path
  // clips descendants, so they simply vanished at the bezel.
  tl.to("#g2p", {scale: 0.9, autoAlpha: 0, duration: 0.26, ease: "power2.in"}, 8.62);
  gsap.set(".loose", {autoAlpha: 0, scale: 0.7, transformOrigin: "50% 50%"});
  var LP = [[-250, -140, -17], [210, -40, 12], [-170, 110, -8], [250, 170, 19]];
  ["#g2l0", "#g2l1", "#g2l2", "#g2l3"].forEach(function (s, i) {
    tl.fromTo(s, {x: 0, y: 0, rotation: 0},
              {x: LP[i][0], y: LP[i][1], rotation: LP[i][2], autoAlpha: 1,
               scale: 1, duration: 0.34, ease: "power4.out"}, 8.62 + i * 0.07);
  });
  tl.to("#g2", {autoAlpha: 0, duration: 0.26, ease: "power2.in"}, 10.70);'''
    return html, js


@beat
def b03_reference_stream():
    """«навіть з розвинутою надивленістю» — references streaming past.

    Seeing a lot is not the same as being able to make it; the screens go by
    faster than they can be read.
    """
    cards = "".join(
        '<span class="refcard r%d" id="g3c%d"><b class="ph"></b>'
        '<b class="pr"></b><b class="pr"></b></span>' % (i % 3, i)
        for i in range(6))
    html = '''
      <div class="g" id="g3">
        <div class="refstrip" id="g3s">%s</div>
      </div>''' % cards
    js = '''
  gsap.set("#g3", {autoAlpha: 0});
  gsap.set(".refcard", {autoAlpha: 0, x: 150, scale: 0.9});
  tl.to("#g3", {autoAlpha: 1, duration: 0.16}, 15.30);
  tl.to(".refcard", {autoAlpha: 1, x: 0, scale: 1, duration: 0.34,
                     ease: "power3.out", stagger: 0.055}, 15.30);
  tl.to("#g3s", {x: -46, duration: 2.0, ease: "none"}, 16.29);
  tl.to("#g3", {autoAlpha: 0, duration: 0.26, ease: "power2.in"}, 17.90);'''
    return html, js


@beat
def b04_expensive():
    """«щоб додаток виглядав дорого і продумано» — one considered surface.

    The glass plaque she liked on reel 3, used as the thing itself: the look
    that is hard to reach.
    """
    html = '''
      <div class="g" id="g4">
        <div class="glass plaque" id="g4p">
          <b class="ph" id="g4h"></b>
          <b class="pr"></b><b class="pr"></b><b class="pr"></b>
          <span class="plaquerow"><i class="chip"></i><i class="chip"></i><i class="chip wide"></i></span>
        </div>
        <div class="ring" id="g4r"></div>
      </div>'''
    js = '''
  gsap.set("#g4", {autoAlpha: 0});
  gsap.set("#g4p", {scale: 0.86, transformOrigin: "50% 50%"});
  gsap.set("#g4r", {scale: 0.5, autoAlpha: 0, transformOrigin: "50% 50%"});
  tl.to("#g4", {autoAlpha: 1, duration: 0.18}, 18.40);
  tl.to("#g4p", {scale: 1, duration: 0.44, ease: "back.out(1.6)"}, 18.40);
  tl.to("#g4r", {scale: 1.4, autoAlpha: 0.85, duration: 0.20, ease: "power2.out"}, 18.82);
  tl.to("#g4r", {scale: 2.0, autoAlpha: 0, duration: 0.46, ease: "power2.out"}, 19.02);
  tl.to("#g4", {autoAlpha: 0, duration: 0.26, ease: "power2.in"}, 21.30);'''
    return html, js


# ---------------------------------------------------------------- B · Mobbin

@beat
def b05_five_hundred():
    """«коштує лише 500 гривень на місяць» — a number is allowed."""
    html = '''
      <div class="g" id="g5">
        <div class="valcard big" id="g5v"><span>500 ₴</span></div>
      </div>'''
    js = '''
  gsap.set("#g5", {autoAlpha: 0});
  gsap.set("#g5v", {scale: 0.7, transformOrigin: "50% 50%"});
  tl.to("#g5", {autoAlpha: 1, duration: 0.14}, 22.90);
  tl.to("#g5v", {scale: 1, duration: 0.42, ease: "back.out(2)"}, 23.10);
  tl.to("#g5", {autoAlpha: 0, duration: 0.26, ease: "power2.in"}, 26.00);'''
    return html, js


@beat
def b06_mobbin_mark():
    """«Платформа називається Мобін» — the real mark."""
    html = '''
      <div class="g" id="g6">
        <div class="lit" id="g6g">
          <div class="tile brand" id="g6t"><img src="assets/logos/mobbin-mark.png" alt=""></div>
        </div>
      </div>'''
    js = '''
  gsap.set("#g6", {autoAlpha: 0});
  gsap.set("#g6t", {scale: 0.3, transformOrigin: "50% 50%"});
  tl.to("#g6", {autoAlpha: 1, duration: 0.14}, 28.70);
  tl.to("#g6t", {scale: 1, duration: 0.42, ease: "back.out(2)"}, 28.80);
  tl.to("#g6", {autoAlpha: 0, duration: 0.24, ease: "power2.in"}, 30.70);'''
    return html, js


@beat
def b07_pinterest_wall():
    """«по суті, Пінтерест для розробників» — the wall of apps.

    A grid, not the Pinterest mark: she says «як Пінтерест», a simile, and the
    wrong brand mark would be a lie.
    """
    tiles = "".join(
        '<span class="mt m%d" id="g7t%d"><b class="ph"></b>'
        '<b class="pr"></b><b class="pr"></b></span>' % (i % 5, i)
        for i in range(9))
    html = '''
      <div class="g" id="g7">
        <div class="masonry" id="g7m">%s</div>
      </div>''' % tiles
    js = '''
  gsap.set("#g7", {autoAlpha: 0});
  gsap.set(".mt", {scale: 0, transformOrigin: "50% 50%"});
  tl.to("#g7", {autoAlpha: 1, duration: 0.16}, 30.90);
  tl.to(".mt", {scale: 1, duration: 0.32, ease: "back.out(2)", stagger: 0.038}, 31.08);
  tl.to("#g7", {autoAlpha: 0, duration: 0.28, ease: "power2.in"}, 35.10);'''
    return html, js


@beat
def b08_every_stage():
    """«скріншоти кожного етапу користування» — her own capture, the section
    where one screen swipes into the next. Takeover on a tinted pane."""
    html = '''
      <div class="g full" id="g8">
        <div class="ground" id="g8bg"></div>
        <div class="phone capture" id="g8f">
          <video id="g8v" src="assets/mobbin-swipe.mp4"
                 data-start="36.55" data-duration="4.60" data-media-start="0"
                 muted playsinline></video>
        </div>
      </div>'''
    js = '''
  gsap.set("#g8", {autoAlpha: 0});
  gsap.set("#g8bg", {autoAlpha: 0});
  gsap.set("#g8f", {scale: 0.88, autoAlpha: 0, transformOrigin: "50% 50%"});
  tl.to("#g8", {autoAlpha: 1, duration: 0.10}, 36.40);
  tl.to("#g8bg", {autoAlpha: 1, duration: 0.26, ease: "power2.out"}, 36.40);
  tl.to("#g8f", {scale: 1, autoAlpha: 1, duration: 0.40, ease: "power3.out"}, 36.50);
  tl.to("#g8", {autoAlpha: 0, duration: 0.28, ease: "power2.in"}, 40.90);'''
    return html, js


@beat
def b09_search_by_need():
    """«шукати саме під свої проблеми. Тобто онбординг, список задач»

    Her capture again, the filter panel — which happens to list «Onboarding»
    on screen exactly as she says it.
    """
    html = '''
      <div class="g full" id="g9">
        <div class="ground" id="g9bg"></div>
        <div class="phone capture" id="g9f">
          <video id="g9v" src="assets/mobbin-search.mp4"
                 data-start="41.90" data-duration="3.70" data-media-start="0"
                 muted playsinline></video>
        </div>
      </div>'''
    js = '''
  gsap.set("#g9", {autoAlpha: 0});
  gsap.set("#g9bg", {autoAlpha: 0});
  gsap.set("#g9f", {scale: 0.88, autoAlpha: 0, transformOrigin: "50% 50%"});
  tl.to("#g9", {autoAlpha: 1, duration: 0.10}, 41.80);
  tl.to("#g9bg", {autoAlpha: 1, duration: 0.24, ease: "power2.out"}, 41.80);
  tl.to("#g9f", {scale: 1, autoAlpha: 1, duration: 0.36, ease: "power3.out"}, 41.86);
  tl.to("#g9", {autoAlpha: 0, duration: 0.28, ease: "power2.in"}, 45.30);'''
    return html, js


# ---------------------------------------------------------------- C · the MCP

@beat
def b10_wire():
    """«безкоштовний MCP, який підключається прямо до штучного інтелекту»
    …«мій Клод сам заходить туди, шукає варіанти»

    One object across two sentences: the wire is drawn on «підключається»,
    then screens travel it on «заходить туди».
    """
    html = '''
      <div class="g" id="g10">
        <div class="tile brand sm" id="g10m"><img src="assets/logos/mobbin-mark.png" alt=""></div>
        <div class="tile brand sm claude" id="g10c"><img src="assets/logos/claude-tile.png" alt=""></div>
        <svg id="g10svg" viewBox="0 0 1080 120" width="1080" height="120">
          <defs><linearGradient id="wg" gradientUnits="userSpaceOnUse" x1="372" y1="0" x2="668" y2="0">
            <stop offset="0" stop-color="#ff8ab0"/><stop offset="1" stop-color="#d0173a"/>
          </linearGradient></defs>
          <path class="wire" id="g10w" d="M 372 60 H 668"/>
        </svg>
        <i class="pkt" id="g10k1"></i><i class="pkt" id="g10k2"></i><i class="pkt" id="g10k3"></i>
      </div>'''
    js = '''
  gsap.set("#g10", {autoAlpha: 0});
  gsap.set("#g10m", {scale: 0.5, autoAlpha: 0, transformOrigin: "50% 50%"});
  gsap.set("#g10c", {scale: 0.5, autoAlpha: 0, transformOrigin: "50% 50%"});
  gsap.set([".pkt"], {autoAlpha: 0, x: 0});
  (function () {
    var p = document.getElementById("g10w"), L = p.getTotalLength();
    gsap.set(p, {strokeDasharray: L, strokeDashoffset: L});
  })();
  tl.to("#g10", {autoAlpha: 1, duration: 0.16}, 46.40);
  tl.to("#g10m", {scale: 1, autoAlpha: 1, duration: 0.28, ease: "back.out(2.2)"}, 46.40);
  tl.to("#g10c", {scale: 1, autoAlpha: 1, duration: 0.28, ease: "back.out(2.2)"}, 46.60);
  tl.to("#g10w", {strokeDashoffset: 0, duration: 0.36, ease: "power2.out"}, 47.92);
  // «мій Клод сам заходить туди» — it goes and fetches, three times over
  [52.20, 53.30, 54.40].forEach(function (t, i) {
    var s = "#g10k" + (i + 1);
    tl.to(s, {autoAlpha: 1, duration: 0.10}, t);
    tl.to(s, {x: 236, duration: 0.62, ease: "power1.inOut"}, t + 0.04);
    tl.to(s, {autoAlpha: 0, duration: 0.12}, t + 0.56);
  });
  tl.to("#g10", {autoAlpha: 0, duration: 0.26, ease: "power2.in"}, 56.40);'''
    return html, js


@beat
def b11_not_invented():
    """«а не вигадує з голови» — the invented one dissolves.

    Two screens side by side: the one it found stays solid, the one it would
    have imagined falls apart.
    """
    html = '''
      <div class="g" id="g11">
        <div class="pairrow" id="g11r">
          <span class="mini real" id="g11a"><b class="ph"></b><b class="pr"></b><b class="pr"></b></span>
          <span class="mini fake" id="g11b"><b class="ph"></b><b class="pr"></b><b class="pr"></b></span>
        </div>
      </div>'''
    js = '''
  gsap.set("#g11", {autoAlpha: 0});
  gsap.set(["#g11a","#g11b"], {scale: 0.7, autoAlpha: 0, transformOrigin: "50% 50%"});
  tl.to("#g11", {autoAlpha: 1, duration: 0.16}, 57.40);
  tl.to("#g11a", {scale: 1, autoAlpha: 1, duration: 0.30, ease: "back.out(2)"}, 57.40);
  tl.to("#g11b", {scale: 1, autoAlpha: 1, duration: 0.30, ease: "back.out(2)"}, 57.60);
  // «не вигадує» — the imagined one comes apart and goes
  tl.to("#g11b", {rotation: 9, y: 40, autoAlpha: 0, duration: 0.50,
                  ease: "power2.in", transformOrigin: "50% 50%"}, 58.86);
  tl.to("#g11", {autoAlpha: 0, duration: 0.26, ease: "power2.in"}, 60.20);'''
    return html, js


# ---------------------------------------------------------------- D · CTA

@beat
def b12_discount():
    """«то в тебе буде знижка 10%»"""
    html = '''
      <div class="g" id="g12">
        <div class="valcard big" id="g12v"><span>−10%</span></div>
      </div>'''
    js = '''
  gsap.set("#g12", {autoAlpha: 0});
  gsap.set("#g12v", {scale: 0.7, transformOrigin: "50% 50%"});
  tl.to("#g12", {autoAlpha: 1, duration: 0.14}, 62.10);
  tl.to("#g12v", {scale: 1, duration: 0.40, ease: "back.out(2.2)"}, 62.30);
  tl.to("#g12", {autoAlpha: 0, duration: 0.26, ease: "power2.in"}, 64.40);'''
    return html, js


@beat
def b13_comment():
    """«Пиши "знижка" в коментарі»

    The one place a word is allowed: it is the thing she is asking the viewer
    to type, shown inside the field they will type it in.
    """
    html = '''
      <div class="g" id="g13">
        <div class="card cmt" id="g13c">
          <span class="cmttext" id="g13t"></span><i class="caret" id="g13k"></i>
          <span class="cmtsend" id="g13s"></span>
        </div>
      </div>'''
    js = '''
  var WORD = "знижка";
  var typed = {n: 0};
  var node = document.createTextNode("");
  document.getElementById("g13t").appendChild(node);
  gsap.set("#g13", {autoAlpha: 0});
  gsap.set("#g13c", {y: 40, scale: 0.94, transformOrigin: "50% 50%"});
  gsap.set("#g13k", {autoAlpha: 0});
  tl.to("#g13", {autoAlpha: 1, duration: 0.16}, 64.70);
  tl.to("#g13c", {y: 0, scale: 1, duration: 0.32, ease: "power3.out"}, 64.70);
  tl.to("#g13k", {autoAlpha: 1, duration: 0.10}, 64.90);
  tl.to(typed, {n: WORD.length, duration: 0.48, ease: "none",
        onUpdate: function () { node.nodeValue = WORD.slice(0, Math.floor(typed.n)); }}, 65.22);
  tl.to("#g13k", {autoAlpha: 0, duration: 0.12}, 65.78);
  tl.to("#g13s", {scale: 1.16, duration: 0.14, ease: "power3.out",
                  transformOrigin: "50% 50%"}, 65.92);
  tl.to("#g13s", {scale: 1, duration: 0.28, ease: "power2.out"}, 66.06);'''
    return html, js


# ---------------------------------------------------------------- geometry

k.css('''
    /* b01 — the easy part */
    .fnlist { left: 160px; top: 90px; width: 760px; height: 380px;
              padding: 44px; display: flex; flex-direction: column; gap: 26px; }
    .fnrow { position: relative; display: block; height: 62px;
             border-radius: 20px; background: var(--container); overflow: hidden; }
    .fnrow:nth-child(2) { width: 82%; }
    .fnrow:nth-child(3) { width: 64%; }
    .fnrow:nth-child(4) { width: 45%; }
    .fnfill { position: absolute; inset: 0; display: block;
              background: var(--graphite); }
    /* §5a.4 — the accent lands once, on the first row */
    #b1r0 .fnfill { background: var(--lit-accent); }

    /* b02 — the screen, then its pieces */
    .phone { left: 380px; top: 30px; width: 320px; height: 580px; }
    .pscr { position: absolute; left: 18px; top: 18px; width: 284px;
            height: 544px; display: block; background: var(--lit);
            padding: 30px 26px; }
    .pscr .ph, .pscr .pr { position: relative; }
    /* the pieces, once they are no longer a screen */
    .loose { position: absolute; display: block; left: 430px; top: 290px;
             border-radius: 18px; filter: var(--cast-sm); }
    .loose.l0 { width: 220px; height: 62px; background: var(--lit-accent); }
    .loose.l1 { width: 170px; height: 44px; background: var(--container-high); }
    .loose.l2 { width: 250px; height: 44px; background: var(--container); }
    .loose.l3 { width: 130px; height: 44px; background: var(--container-high); }

    /* b03 — references going past */
    .refstrip { position: absolute; left: 84px; top: 150px; width: 912px;
                display: flex; gap: 22px; align-items: flex-start; }
    .refcard { display: block; width: 138px; height: 250px; padding: 16px 14px;
               background: var(--lit-blush); overflow: hidden;
               filter: var(--cast-sm); box-shadow: var(--rim); }
    .refcard.r1 { height: 210px; } .refcard.r2 { height: 280px; }
    .refcard .ph { height: 34px; border-radius: 11px; margin-bottom: 12px; }
    .refcard .pr { height: 16px; border-radius: 7px; margin-bottom: 9px; }

    /* b04 — the considered surface */
    .plaque { position: absolute; left: 210px; top: 105px; width: 660px;
              height: 380px; padding: 44px; }
    .plaque .ph { background: var(--lit-accent); height: 54px;
                  border-radius: 16px; margin-bottom: 20px; width: 58%; }
    .plaque .pr { height: 24px; border-radius: 9px; margin-bottom: 14px;
                  background: rgba(255,255,255,0.34); }
    .plaquerow { position: absolute; left: 44px; bottom: 40px;
                 display: flex; gap: 14px; }
    .chip { display: block; width: 96px; height: 44px; border-radius: 16px;
            background: rgba(255,255,255,0.42); }
    .chip.wide { width: 150px; }
    .ring { width: 460px; height: 460px; left: 310px; top: 55px; }

    /* b05 / b12 — numbers */
    .valcard.big { left: 250px; top: 140px; width: 580px; height: 280px; }
    .valcard.big span { font-size: 150px; line-height: 150px; }

    /* b06 / b10 — brand tiles */
    /* §5a.10 — no filter here at all: the clip-path below would eat it. The
       light lives on the .lit wrapper, and only b06 uses one, because the
       glow belongs to the beat's subject and b10's subject is the wire. */
    .tile.brand { width: 340px; height: 340px; left: 370px; top: 130px;
                  filter: none; }
    .tile.brand img { height: 190px; width: auto; }
    .tile.brand.sm { width: 260px; height: 260px; top: 180px; }
    .tile.brand.sm img { height: 146px; }
    .tile.brand.claude { background: none; box-shadow: none; }
    .tile.brand.claude img { width: 260px; height: 260px;
                             border-radius: 60px; }
    #g10m { left: 120px; }
    #g10c { left: 660px; }


    /* b07 — the wall */
    .masonry { position: absolute; left: 79px; top: 30px; width: 922px;
               display: flex; flex-wrap: wrap; gap: 26px;
               align-content: flex-start; justify-content: center; }
    .mt { display: block; width: 290px; padding: 22px 20px;
          background: var(--lit-blush); overflow: hidden;
          filter: var(--cast-sm); box-shadow: var(--rim); }
    .mt .ph { height: 48px; border-radius: 14px; margin-bottom: 16px; }
    .mt .pr { height: 22px; border-radius: 8px; margin-bottom: 12px; }
    .m0 { height: 200px; } .m1 { height: 162px; } .m2 { height: 228px; }
    .m3 { height: 180px; } .m4 { height: 210px; }

    /* b08 / b09 — her capture, framed on the pane */
    .phone.capture { left: 230px; top: 150px; width: 620px; height: 1102px; }

    /* b10 — the wire */
    #g10svg { position: absolute; left: 0; top: 250px; overflow: visible; }
    .wire { stroke: url(#wg); stroke-width: 24; }
    .pkt { position: absolute; display: block; width: 62px; height: 62px;
           border-radius: 50%; background: var(--lit); left: 392px; top: 279px;
           filter: drop-shadow(0 0 26px rgba(255,110,156,0.9)); }

    /* b11 — found versus invented */
    .pairrow { position: absolute; left: 190px; top: 90px; width: 700px;
               display: flex; justify-content: space-between; }
    .mini { display: block; width: 300px; height: 400px; padding: 30px 26px;
            background: var(--lit-blush); overflow: hidden;
            filter: var(--cast); box-shadow: var(--rim); }
    .mini.fake { background: linear-gradient(115deg, #f7f2f3 0%, #efe6e8 100%);
                 box-shadow: inset 0 0 0 3px rgba(180,18,47,0.18); }
    .mini.fake .ph { background: var(--graphite); }

    /* b13 — the comment field */
    .cmt { left: 130px; top: 190px; width: 820px; height: 190px;
           padding: 0 40px; display: flex; align-items: center; gap: 10px;
           font-size: 62px; font-weight: 900; color: var(--ink); }
    .caret { display: inline-block; width: 7px; height: 66px;
             background: var(--accent); }
    .cmtsend { position: absolute; right: 36px; width: 108px; height: 108px;
               border-radius: 50%; background: var(--lit-accent);
               box-shadow: var(--rim-dark); }
''')

# STYLE.md §5a.1 says continuous corners; the renderer caps how many elements
# may carry clip-path/blur/radial-gradient before capture goes black. So the
# squircle goes on the large surfaces, where the corner break is actually
# visible, and everything smaller keeps a plain radius.
for sel, w, h, r in [
    (".fnlist", 760, 380, 62),
    (".phone", 320, 580, 68), (".pscr", 284, 544, 52),
    (".plaque", 660, 380, 60), (".valcard.big", 580, 280, 58),
    (".tile.brand", 340, 340, 84), (".tile.brand.sm", 260, 260, 66),
    (".phone.capture", 620, 1102, 74),
    (".cmt", 820, 190, 52),
]:
    k.squircle(sel, w, h, r)

# small and repeated surfaces: plain radius, no clip-path
k.css("""
    .fnrow { border-radius: 20px; }
    .refcard { border-radius: 34px; }
    .refcard.r1 { border-radius: 32px; }
    .refcard.r2 { border-radius: 36px; }
    .mt { border-radius: 44px; }
    .mini { border-radius: 52px; }
""")


def main():
    caps = k.load_captions(os.path.join(ROOT, "work", "r4", "captions.json"))
    gh, gj = [], []
    for fn in BEATS:
        h, j = fn()
        gh.append(h.rstrip())
        gj.append("  /* %s */" % fn.__name__)
        gj.append(j.rstrip())

    doc = k.document(
        title="Reel 4 — Мобін",
        plate="assets/base.mp4",
        gfx_html="\n".join(gh),
        gfx_js="\n".join(gj),
        caps=caps,
        scrim_off=[(36.30, 41.00, "the swipe pane is its own ground"),
                   (41.70, 45.40, "the search pane is its own ground")],
    )
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "index.html")
    io.open(out, "w", encoding="utf-8").write(doc)
    print("index.html  %d captions, %d beats, %.1f KB"
          % (len(caps), len(BEATS), os.path.getsize(out) / 1024.0))


main()
