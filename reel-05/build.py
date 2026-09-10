# -*- coding: utf-8 -*-
"""Reel 5 — «презентації, які пише ШІ, зазвичай фігня».

Variant B: her cut, graded, no subtitles. Materials from tools/kit.py
(STYLE.md §5a); what each beat depicts is invented for this script.

The recurring object is a **slide**. The whole script is about presentations,
so one object carries the argument: a slide the AI wrote, the same slide read
properly, her own ordering, and finally a deck that matches her outline.
STYLE.md §4 — «reuse objects», a returning object costs nothing to read.

usage: python build.py
"""
import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
from kit import Kit  # noqa: E402

DUR = 87.960
k = Kit(width=1080, height=1920, fps=30, duration=DUR)

BEATS = []


def beat(fn):
    BEATS.append(fn)
    return fn


def slide(sid, cls="", rows=3):
    """A slide: one heading bar, then ragged body. §5a.3."""
    body = "".join('<b class="pr"></b>' for _ in range(rows))
    return ('<span class="slide %s" id="%s"><b class="ph"></b>%s</span>'
            % (cls, sid, body))


# ---------------------------------------------------------------- A · the problem


@beat
def b02_ai_deck():
    """«презентації, які пише штучний інтелект, зазвичай фігня»
    …«виглядають класно, робляться швидко»

    The deck arrives fast and looks perfectly fine. That is the trap, so it is
    played straight here and undone later.
    """
    html = '''
      <div class="g" id="g2">
        <div class="deck" id="g2d">%s%s%s</div>
        <div class="verdict" id="g2v">💩</div>
      </div>''' % (slide("g2s0"), slide("g2s1"), slide("g2s2"))
    js = '''
  gsap.set("#g2", {autoAlpha: 0});
  gsap.set("#g2 .slide", {autoAlpha: 0, scale: 0.86, transformOrigin: "50% 50%"});
  tl.to("#g2", {autoAlpha: 1, duration: 0.16}, 6.10);
  // «робляться швидко» — three of them, almost at once
  ["#g2s0","#g2s1","#g2s2"].forEach(function (s, i) {
    tl.to(s, {autoAlpha: 1, scale: 1, duration: 0.26, ease: "back.out(2)"}, 6.30 + i * 0.14);
  });
  // «зазвичай фігня» — the verdict lands on the deck
  gsap.set("#g2v", {scale: 0.2, autoAlpha: 0, y: -70, rotation: -14,
                    transformOrigin: "50% 50%"});
  tl.to("#g2v", {scale: 1, autoAlpha: 1, y: 0, rotation: 0,
                 duration: 0.34, ease: "back.out(2.6)"}, 8.30);
  tl.to("#g2d", {scale: 0.95, duration: 0.30, ease: "power2.out"}, 8.34);
  // «виглядають класно, робляться швидко» — said over the verdict, deadpan
  tl.to("#g2v", {rotation: 6, duration: 0.20, ease: "power3.out"}, 10.76);
  tl.to("#g2v", {rotation: 0, duration: 0.34, ease: "power2.out"}, 10.96);
  tl.to("#g2", {autoAlpha: 0, duration: 0.26, ease: "power2.in"}, 12.60);'''
    return html, js


@beat
def b03_too_much_too_little():
    """«Десь забагато, десь замало» — the same slide, twice, both wrong."""
    html = '''
      <div class="g" id="g3">
        <div class="pairslides" id="g3r">
          <span class="slide dense" id="g3a"><b class="ph"></b>%s</span>
          <span class="slide sparse" id="g3b"><b class="ph"></b><b class="pr"></b></span>
        </div>
      </div>''' % ("".join('<b class="pr"></b>' for _ in range(7)))
    js = '''
  gsap.set("#g3", {autoAlpha: 0});
  gsap.set(["#g3a","#g3b"], {autoAlpha: 0, y: 30});
  tl.to("#g3", {autoAlpha: 1, duration: 0.16}, 16.90);
  tl.to("#g3a", {autoAlpha: 1, y: 0, duration: 0.26, ease: "power3.out"}, 17.48);
  tl.to("#g3b", {autoAlpha: 1, y: 0, duration: 0.26, ease: "power3.out"}, 18.10);
  tl.to("#g3", {autoAlpha: 0, duration: 0.24, ease: "power2.in"}, 19.10);'''
    return html, js


@beat
def b04_cut_wrong():
    """«і розрізано якось дивно» — a run of text sliced across the wrong seam."""
    html = '''
      <div class="g" id="g4">
        <div class="cutblock" id="g4b">
          <i class="cutrow"></i><i class="cutrow"></i><i class="cutrow"></i>
          <i class="cutrow"></i>
        </div>
        <div class="cutline" id="g4l"></div>
      </div>'''
    js = '''
  gsap.set("#g4", {autoAlpha: 0});
  gsap.set("#g4b", {scale: 0.92, transformOrigin: "50% 50%"});
  gsap.set("#g4l", {scaleX: 0, transformOrigin: "0% 50%"});
  tl.to("#g4", {autoAlpha: 1, duration: 0.16}, 19.20);
  tl.to("#g4b", {scale: 1, duration: 0.28, ease: "power3.out"}, 19.20);
  // the cut lands mid-thought, and the halves slide apart
  tl.to("#g4l", {scaleX: 1, duration: 0.18, ease: "power4.out"}, 19.32);
  tl.to("#g4b", {y: -18, duration: 0.24, ease: "power3.out"}, 19.58);
  tl.to("#g4l", {y: 26, duration: 0.24, ease: "power3.out"}, 19.58);
  tl.to("#g4", {autoAlpha: 0, duration: 0.24, ease: "power2.in"}, 21.80);'''
    return html, js


# ---------------------------------------------------------------- B · her method

@beat
def b05_her_order():
    """«є свій метод пояснення, свій спосіб сторітелінгу»

    Numbered steps in a deliberate order — the thing the model does not have.
    """
    pts = [(70, 230), (370, 70), (660, 150), (820, 110)]
    dots = "".join('<circle class="step" id="g5s%d" cx="%d" cy="%d" r="34"/>'
                   % (i, x, y) for i, (x, y) in enumerate(pts))
    html = '''
      <div class="g" id="g5">
        <svg id="g5svg" viewBox="0 0 880 300" width="880" height="300">
          <path class="wire" id="g5w" d="M 70 230 C 230 230, 210 70, 370 70
                                          S 530 230, 660 150 S 790 90, 820 110"/>
          %s
        </svg>
      </div>''' % dots
    js = '''
  gsap.set("#g5", {autoAlpha: 0});
  [[70, 230], [370, 70], [660, 150], [820, 110]].forEach(function (pt, i) {
    gsap.set("#g5s" + i, {scale: 0, transformOrigin: pt[0] + "px " + pt[1] + "px"});
  });
  (function () {
    var p = document.getElementById("g5w"), L = p.getTotalLength();
    gsap.set(p, {strokeDasharray: L, strokeDashoffset: L});
  })();
  tl.to("#g5", {autoAlpha: 1, duration: 0.16}, 25.30);
  ["#g5s0","#g5s1","#g5s2","#g5s3"].forEach(function (s, i) {
    tl.to(s, {scale: 1, duration: 0.24, ease: "back.out(2.4)"}, 25.72 + i * 0.20);
  });
  // «свій спосіб сторітелінгу» — the thread that joins them, in her order
  tl.to("#g5w", {strokeDashoffset: 0, duration: 1.10, ease: "power2.inOut"}, 27.62);
  tl.to("#g5", {autoAlpha: 0, duration: 0.26, ease: "power2.in"}, 30.60);'''
    return html, js


@beat
def b06_reordered():
    """«подати інформацію так, як логічно НАМ» — the same blocks, her sequence."""
    html = '''
      <div class="g" id="g6">
        <div class="ordercol" id="g6c">
          <i class="ord o0" id="g6a"></i><i class="ord o1" id="g6b"></i>
          <i class="ord o2" id="g6c2"></i><i class="ord o3" id="g6d"></i>
        </div>
      </div>'''
    js = '''
  gsap.set("#g6", {autoAlpha: 0});
  gsap.set("#g6 .ord", {autoAlpha: 0, x: -40});
  tl.to("#g6", {autoAlpha: 1, duration: 0.16}, 32.60);
  tl.to("#g6 .ord", {autoAlpha: 1, x: 0, duration: 0.24, ease: "power3.out",
                 stagger: 0.09}, 32.60);
  // «логічно НАМ» — they swap into her order
  tl.to("#g6a", {y: 218, duration: 0.34, ease: "power3.inOut"}, 33.78);
  tl.to("#g6c2", {y: -218, duration: 0.34, ease: "power3.inOut"}, 33.78);
  tl.to("#g6", {autoAlpha: 0, duration: 0.24, ease: "power2.in"}, 36.20);'''
    return html, js


@beat
def b07_mass_chopped():
    """«а не просто розбити якусь масу тексту на слайди» — mechanical slicing."""
    lines = "".join('<i class="massline"></i>' for _ in range(16))
    html = '''
      <div class="g" id="g7">
        <div class="massblock" id="g7m">%s</div>
        <div class="chops" id="g7c">
          <i class="chop"></i><i class="chop"></i><i class="chop"></i>
        </div>
      </div>''' % lines
    js = '''
  gsap.set("#g7", {autoAlpha: 0});
  gsap.set("#g7m", {scaleY: 0, transformOrigin: "50% 0%"});
  gsap.set("#g7 .chop", {scaleX: 0, transformOrigin: "50% 50%"});
  tl.to("#g7", {autoAlpha: 1, duration: 0.16}, 35.60);
  tl.to("#g7m", {scaleY: 1, duration: 0.34, ease: "power3.out"}, 35.60);
  tl.to("#g7 .chop", {scaleX: 1, duration: 0.14, ease: "power4.out",
                  stagger: 0.10}, 37.38);
  tl.to("#g7", {autoAlpha: 0, duration: 0.24, ease: "power2.in"}, 38.70);'''
    return html, js


@beat
def b08_gamma_or_claude():
    """«коли ти відкриваєш Gamma чи той самий Клод» — the two she names."""
    html = '''
      <div class="g" id="g8">
        <div class="duo" id="g8r">
          <div class="tile brand" id="g8a"><img src="assets/logos/gamma.png" alt=""></div>
          <div class="tile brand claude" id="g8b"><img src="assets/logos/claude-tile.png" alt=""></div>
        </div>
      </div>'''
    js = '''
  gsap.set("#g8", {autoAlpha: 0});
  gsap.set(["#g8a","#g8b"], {scale: 0.4, autoAlpha: 0, transformOrigin: "50% 50%"});
  tl.to("#g8", {autoAlpha: 1, duration: 0.14}, 38.90);
  tl.to("#g8a", {scale: 1, autoAlpha: 1, duration: 0.30, ease: "back.out(2.2)"}, 39.06);
  tl.to("#g8b", {scale: 1, autoAlpha: 1, duration: 0.30, ease: "back.out(2.2)"}, 40.06);
  tl.to("#g8", {autoAlpha: 0, duration: 0.24, ease: "power2.in"}, 42.60);'''
    return html, js


@beat
def b09_writes_rubbish():
    """«воно тобі, скоріш за все, напише…» — the output collapses."""
    html = '''
      <div class="g" id="g9">
        %s
      </div>''' % slide("g9s", "lone", 4)
    js = '''
  gsap.set("#g9", {autoAlpha: 0});
  gsap.set("#g9s", {scale: 0.9, autoAlpha: 0, transformOrigin: "50% 50%"});
  tl.to("#g9", {autoAlpha: 1, duration: 0.16}, 43.20);
  tl.to("#g9s", {scale: 1, autoAlpha: 1, duration: 0.28, ease: "back.out(1.8)"}, 43.20);
  // «напише фігню» — it folds
  tl.to("#g9s", {rotation: 7, y: 70, scaleY: 0.82, autoAlpha: 0,
                 duration: 0.52, ease: "power2.in",
                 transformOrigin: "50% 100%"}, 44.10);
  tl.to("#g9", {autoAlpha: 0, duration: 0.20}, 45.60);'''
    return html, js


# ---------------------------------------------------------------- C · the method

@beat
def b10_more_steps():
    """«трохи складніший, вимагає більше рухів» — a longer path, on purpose."""
    dots = "".join('<i class="mstep" id="g10d%d"></i>' % i for i in range(5))
    html = '''
      <div class="g" id="g10">
        <div class="mrow" id="g10r">%s</div>
        <div class="mline" id="g10l"></div>
      </div>''' % dots
    js = '''
  gsap.set("#g10", {autoAlpha: 0});
  gsap.set("#g10 .mstep", {scale: 0, transformOrigin: "50% 50%"});
  gsap.set("#g10l", {scaleX: 0, transformOrigin: "0% 50%"});
  tl.to("#g10", {autoAlpha: 1, duration: 0.16}, 46.50);
  tl.to("#g10l", {scaleX: 1, duration: 0.60, ease: "power2.out"}, 46.87);
  tl.to("#g10 .mstep", {scale: 1, duration: 0.22, ease: "back.out(2.6)",
                   stagger: 0.13}, 46.99);
  tl.to("#g10", {autoAlpha: 0, duration: 0.26, ease: "power2.in"}, 50.60);'''
    return html, js


@beat
def b11_outline_by_hand():
    """«тобі треба власноруч підготувати по слайдову» …«Скелет.»

    She writes the outline herself. The rows land one at a time, unevenly —
    a person typing, not a model generating.
    """
    rows = "".join('<i class="olrow o%d" id="g11r%d"></i>' % (i % 4, i)
                   for i in range(5))
    html = '''
      <div class="g" id="g11">
        <div class="card outline" id="g11c">%s</div>
      </div>''' % rows
    js = '''
  gsap.set("#g11", {autoAlpha: 0});
  gsap.set("#g11c", {scale: 0.92, transformOrigin: "50% 50%"});
  gsap.set("#g11c .olrow", {scaleX: 0, transformOrigin: "0% 50%"});
  tl.to("#g11", {autoAlpha: 1, duration: 0.18}, 57.20);
  tl.to("#g11c", {scale: 1, duration: 0.30, ease: "power3.out"}, 57.20);
  // uneven on purpose: written, not generated
  var T = [57.78, 58.46, 59.44, 60.30, 61.40];
  T.forEach(function (t, i) {
    tl.to("#g11r" + i, {scaleX: 1, duration: 0.22, ease: "power2.out"}, t);
  });
  // «Скелет.» — the whole thing reads as one structure
  tl.to("#g11c", {scale: 1.04, duration: 0.16, ease: "power3.out"}, 62.86);
  tl.to("#g11c", {scale: 1, duration: 0.30, ease: "power2.out"}, 63.02);
  tl.to("#g11", {autoAlpha: 0, duration: 0.24, ease: "power2.in"}, 64.20);'''
    return html, js


@beat
def b12_claude_design_prompt():
    """«я відкриваю Claude Design і пишу приблизний промт: ось тобі файл зі
    слайдами, ось тобі дизайн системи»

    Text inside an interface is allowed — it is the act being shown. Two
    attachments land on the prompt as she names them.
    """
    html = '''
      <div class="g" id="g12">
        <div class="tile brand claude sm" id="g12t"><img src="assets/logos/claude-tile.png" alt=""></div>
        <div class="card promptbox" id="g12p">
          <span class="attachrow">
            <i class="attach" id="g12a1"></i><i class="attach" id="g12a2"></i>
          </span>
          <b class="pr"></b><b class="pr"></b>
        </div>
      </div>'''
    js = '''
  gsap.set("#g12", {autoAlpha: 0});
  gsap.set("#g12t", {scale: 0.4, autoAlpha: 0, transformOrigin: "50% 50%"});
  gsap.set("#g12p", {y: 40, autoAlpha: 0});
  gsap.set("#g12 .attach", {scale: 0, transformOrigin: "50% 50%"});
  tl.to("#g12", {autoAlpha: 1, duration: 0.14}, 64.60);
  tl.to("#g12t", {scale: 1, autoAlpha: 1, duration: 0.32, ease: "back.out(2.2)"}, 64.90);
  tl.to("#g12p", {y: 0, autoAlpha: 1, duration: 0.32, ease: "power3.out"}, 66.85);
  // «ось тобі файл зі слайдами» / «ось тобі дизайн системи»
  tl.to("#g12a1", {scale: 1, duration: 0.24, ease: "back.out(2.6)"}, 68.12);
  tl.to("#g12a2", {scale: 1, duration: 0.24, ease: "back.out(2.6)"}, 69.38);
  tl.to("#g12", {autoAlpha: 0, duration: 0.26, ease: "power2.in"}, 70.80);'''
    return html, js


@beat
def b13_text_untouched():
    """«не змінюючи нічого з тексту» — the words hold, the surface changes."""
    html = '''
      <div class="g" id="g13">
        <span class="slide big" id="g13s">
          <b class="ph" id="g13h"></b>
          <b class="pr"></b><b class="pr"></b><b class="pr"></b>
        </span>
        <div class="lockring" id="g13l"></div>
      </div>'''
    js = '''
  gsap.set("#g13", {autoAlpha: 0});
  gsap.set("#g13s", {scale: 0.9, transformOrigin: "50% 50%"});
  gsap.set("#g13l", {scale: 0.5, autoAlpha: 0, transformOrigin: "50% 50%"});
  tl.to("#g13", {autoAlpha: 1, duration: 0.16}, 70.90);
  tl.to("#g13s", {scale: 1, duration: 0.30, ease: "power3.out"}, 70.90);
  // the ground restyles underneath, the bars do not move
  tl.to("#g13s", {backgroundColor: "#fdf1f4", duration: 0.50,
                  ease: "power2.inOut"}, 71.22);
  tl.to("#g13l", {scale: 1.3, autoAlpha: 0.9, duration: 0.20, ease: "power2.out"}, 71.30);
  tl.to("#g13l", {scale: 1.9, autoAlpha: 0, duration: 0.44, ease: "power2.out"}, 71.50);
  tl.to("#g13", {autoAlpha: 0, duration: 0.24, ease: "power2.in"}, 72.90);'''
    return html, js


@beat
def b14_five_minutes():
    """«буквально через 5 хвилин»"""
    html = '''
      <div class="g" id="g14">
        <div class="valcard big" id="g14v"><span>5</span></div>
      </div>'''
    js = '''
  gsap.set("#g14", {autoAlpha: 0});
  gsap.set("#g14v", {scale: 0.7, transformOrigin: "50% 50%"});
  tl.to("#g14", {autoAlpha: 1, duration: 0.14}, 73.10);
  tl.to("#g14v", {scale: 1, duration: 0.40, ease: "back.out(2.2)"}, 73.32);
  tl.to("#g14", {autoAlpha: 0, duration: 0.26, ease: "power2.in"}, 75.60);'''
    return html, js


@beat
def b15_as_i_imagined():
    """«зроблена саме так, як я її уявляю» — the deck matches the outline.

    The outline from b11 returns beside the finished deck: same rows, same
    order. A returning object, per STYLE.md §4.
    """
    html = '''
      <div class="g" id="g15">
        <div class="matchpair" id="g15w">
          <div class="card outline mini" id="g15o">
            <i class="olrow o0"></i><i class="olrow o1"></i>
            <i class="olrow o2"></i><i class="olrow o3"></i>
          </div>
          <span class="eq" id="g15e"></span>
          %s
        </div>
      </div>''' % slide("g15s", "res", 3)
    js = '''
  gsap.set("#g15", {autoAlpha: 0});
  gsap.set("#g15o", {x: -50, autoAlpha: 0});
  gsap.set("#g15s", {x: 50, autoAlpha: 0});
  gsap.set("#g15e", {scale: 0, autoAlpha: 0, transformOrigin: "50% 50%"});
  tl.to("#g15", {autoAlpha: 1, duration: 0.16}, 76.30);
  tl.to("#g15o", {x: 0, autoAlpha: 1, duration: 0.30, ease: "power3.out"}, 76.30);
  tl.to("#g15s", {x: 0, autoAlpha: 1, duration: 0.30, ease: "power3.out"}, 76.46);
  tl.to("#g15e", {scale: 1, autoAlpha: 1, duration: 0.26, ease: "back.out(3)"}, 77.64);
  tl.to("#g15", {autoAlpha: 0, duration: 0.26, ease: "power2.in"}, 79.60);'''
    return html, js


@beat
def b16_fifty_comments():
    """«пишіть "треба" в коментарі… якщо набереться 50 коментарів»"""
    html = '''
      <div class="g" id="g16">
        <div class="card cmt" id="g16c">
          <span class="cmttext" id="g16t"></span><i class="caret" id="g16k"></i>
          <span class="cmtsend" id="g16s"></span>
        </div>
        <div class="valcard tally" id="g16v"><span>50</span></div>
      </div>'''
    js = '''
  var WORD = "треба";
  var typed = {n: 0};
  var node = document.createTextNode("");
  document.getElementById("g16t").appendChild(node);
  gsap.set("#g16", {autoAlpha: 0});
  gsap.set("#g16c", {y: 40, scale: 0.94, transformOrigin: "50% 50%"});
  gsap.set("#g16k", {autoAlpha: 0});
  gsap.set("#g16v", {scale: 0.6, autoAlpha: 0, transformOrigin: "50% 50%"});
  tl.to("#g16", {autoAlpha: 1, duration: 0.16}, 82.10);
  tl.to("#g16c", {y: 0, scale: 1, duration: 0.32, ease: "power3.out"}, 82.10);
  tl.to("#g16k", {autoAlpha: 1, duration: 0.10}, 82.30);
  tl.to(typed, {n: WORD.length, duration: 0.44, ease: "none",
        onUpdate: function () { node.nodeValue = WORD.slice(0, Math.floor(typed.n)); }}, 82.60);
  tl.to("#g16k", {autoAlpha: 0, duration: 0.12}, 83.10);
  tl.to("#g16s", {scale: 1.16, duration: 0.14, ease: "power3.out",
                  transformOrigin: "50% 50%"}, 83.40);
  tl.to("#g16s", {scale: 1, duration: 0.28, ease: "power2.out"}, 83.54);
  // «якщо набереться 50 коментарів»
  tl.to("#g16v", {scale: 1, autoAlpha: 1, duration: 0.34, ease: "back.out(2.2)"}, 84.78);
  tl.to("#g16", {autoAlpha: 0, duration: 0.28, ease: "power2.in"}, 87.10);'''
    return html, js


# ---------------------------------------------------------------- geometry

k.css('''
    /* the recurring object: a slide */
    .slide { position: relative; display: block; width: 300px; height: 210px;
             padding: 26px 24px; background: var(--lit-blush);
             overflow: hidden; filter: var(--cast-sm); box-shadow: var(--rim);
             border-radius: 34px; }
    .slide .ph { height: 34px; border-radius: 11px; margin-bottom: 16px;
                 width: 62%; }
    .slide .pr { height: 17px; border-radius: 7px; margin-bottom: 11px; }
    .verdict { position: absolute; left: 0; width: 1080px; top: 300px;
               text-align: center; font-size: 260px; line-height: 260px;
               filter: drop-shadow(0 18px 40px rgba(26,30,39,0.45)); }

    .deck { position: absolute; left: 75px; top: 130px; width: 930px;
            display: flex; gap: 15px; justify-content: center; }

    /* b01 — depth against surface */
    .stackwrap { position: absolute; left: 150px; top: 120px;
                 width: 330px; height: 380px; }
    .sl { position: absolute; display: block; width: 300px; height: 76px;
          border-radius: 26px; background: var(--lit-blush);
          filter: var(--cast-sm); box-shadow: var(--rim); }
    .s1 { top: 0; } .s2 { top: 88px; } .s3 { top: 176px; } .s4 { top: 264px; }
    .sl.thin { left: 600px; top: 264px; width: 300px;
               background: var(--container); }

    /* b03 — too much, too little */
    .pairslides { position: absolute; left: 150px; top: 90px; width: 780px;
                  display: flex; justify-content: space-between;
                  align-items: flex-start; }
    .slide.dense { width: 340px; height: 400px; }
    .slide.dense .pr { margin-bottom: 8px; }
    .slide.sparse { width: 340px; height: 400px; }

    /* b04 — cut across the wrong seam */
    .cutblock { position: absolute; left: 200px; top: 130px; width: 680px;
                height: 340px; padding: 44px; background: var(--lit-blush);
                filter: var(--cast); box-shadow: var(--rim);
                display: flex; flex-direction: column; gap: 18px;
                border-radius: 44px; }
    .cutrow { display: block; height: 30px; border-radius: 12px;
              background: rgba(23,20,28,0.22); }
    .cutrow:nth-child(2) { width: 88%; }
    .cutrow:nth-child(4) { width: 54%; }
    .cutline { position: absolute; left: 170px; top: 286px; width: 740px;
               height: 12px; border-radius: 6px; background: var(--lit-pink);
               filter: drop-shadow(0 0 22px rgba(255,110,156,0.7)); }

    /* b05 — her method, and the thread through it */
    #g5svg { position: absolute; left: 100px; top: 130px; overflow: visible; }
    .wire { stroke: url(#swg); stroke-width: 18; }
    .step { fill: #b4122f; stroke: #fff; stroke-width: 8;
            filter: drop-shadow(0 8px 18px rgba(26,30,39,0.35)); }

    /* b06 — reordered to her logic */
    .ordercol { position: absolute; left: 280px; top: 90px; width: 520px;
                display: flex; flex-direction: column; gap: 28px; }
    .ord { display: block; height: 90px; border-radius: 28px;
           background: var(--container); filter: var(--cast-sm); }
    .ord.o0 { background: var(--lit-accent); }
    .ord.o2 { background: var(--container-high); }

    /* b07 — the mass, chopped */
    .massblock { position: absolute; left: 280px; top: 70px; width: 520px;
                 height: 460px; border-radius: 44px; padding: 34px 30px;
                 background: var(--lit-ink); filter: var(--cast);
                 box-shadow: var(--rim-dark);
                 display: flex; flex-direction: column; gap: 13px; }
    .massline { display: block; height: 15px; border-radius: 7px;
                background: rgba(255,255,255,0.30); }
    .massline:nth-child(4n) { width: 72%; }
    .massline:nth-child(5n) { width: 88%; }
    .chops { position: absolute; left: 260px; top: 70px; width: 560px;
             height: 460px; }
    .chop { position: absolute; left: 0; display: block; width: 560px;
            height: 10px; border-radius: 5px; background: var(--lit-pink);
            filter: drop-shadow(0 0 18px rgba(255,110,156,0.7)); }
    .chop:nth-child(1) { top: 118px; }
    .chop:nth-child(2) { top: 236px; }
    .chop:nth-child(3) { top: 354px; }

    /* b08 / b12 — the marks */
    .duo { position: absolute; left: 170px; top: 130px; width: 740px;
           display: flex; justify-content: space-between; }
    .tile.brand { position: relative; width: 300px; height: 300px; }
    .tile.brand img { width: 190px; height: auto; }
    .tile.brand.claude { background: none; box-shadow: none; }
    .tile.brand.claude img { width: 300px; height: 300px; border-radius: 70px; }
    .tile.brand.sm { position: absolute; left: 390px; top: 40px;
                     width: 220px; height: 220px; }
    .tile.brand.claude.sm img { width: 220px; height: 220px; border-radius: 54px; }

    .promptbox { position: absolute; left: 130px; top: 300px; width: 820px;
                 height: 230px; padding: 30px 34px;
                 display: flex; flex-direction: column; gap: 16px; }
    .attachrow { display: flex; gap: 16px; margin-bottom: 8px; }
    .attach { display: block; width: 130px; height: 84px; border-radius: 22px;
              background: var(--lit-accent); box-shadow: var(--rim-dark); }
    .promptbox .pr { height: 22px; border-radius: 9px; }

    /* b09 — the output that folds */
    .slide.lone { position: absolute; left: 340px; top: 120px;
                  width: 400px; height: 330px; }

    /* b10 — more steps */
    .mrow { position: absolute; left: 140px; top: 265px; width: 800px;
            display: flex; justify-content: space-between; }
    .mstep { display: block; width: 64px; height: 64px; border-radius: 50%;
             background: var(--lit-accent); box-shadow: var(--rim-dark);
             filter: var(--cast-sm); }
    .mline { position: absolute; left: 172px; top: 290px; width: 736px;
             height: 14px; border-radius: 7px; background: var(--lit-pink); }

    /* b11 / b15 — the outline she writes */
    .outline { left: 190px; top: 100px; width: 700px; height: 420px;
               padding: 44px; display: flex; flex-direction: column; gap: 22px;
               border-radius: 52px; }
    .olrow { display: block; height: 44px; border-radius: 16px;
             background: var(--container); }
    .olrow.o0 { background: var(--lit-accent); width: 58%; }
    .olrow.o1 { width: 92%; } .olrow.o2 { width: 74%; } .olrow.o3 { width: 46%; }

    /* b13 — the text holds while the surface changes */
    .slide.big { position: absolute; left: 270px; top: 110px;
                 width: 540px; height: 400px; padding: 40px 36px; }
    .slide.big .ph { height: 50px; border-radius: 16px; }
    .slide.big .pr { height: 26px; border-radius: 10px; margin-bottom: 18px; }
    .lockring { position: absolute; left: 290px; top: 90px; width: 500px;
                height: 440px; border-radius: 60px;
                box-shadow: inset 0 0 0 12px rgba(255,110,156,0.9);
                filter: drop-shadow(0 0 34px rgba(255,110,156,0.6)); }

    /* b14 / b16 — numbers */
    .valcard.big { position: absolute; left: 300px; top: 140px;
                   width: 480px; height: 280px; border-radius: 58px; }
    .valcard.big span { font-size: 170px; line-height: 170px; }
    .valcard.tally { position: absolute; left: 380px; top: 40px;
                     width: 320px; height: 170px; border-radius: 46px; }
    .valcard.tally span { font-size: 104px; line-height: 104px; }

    /* b15 — outline equals result */
    .matchpair { position: absolute; left: 90px; top: 120px; width: 900px;
                 display: flex; align-items: center;
                 justify-content: space-between; }
    .outline.mini { position: relative; left: 0; top: 0; width: 350px;
                    height: 330px; padding: 32px; gap: 16px; }
    .outline.mini .olrow { height: 34px; border-radius: 12px; }
    .slide.res { width: 350px; height: 330px; }
    .eq { display: block; width: 86px; height: 86px; position: relative; }
    .eq::before, .eq::after { content: ""; position: absolute; left: 0;
        width: 86px; height: 18px; border-radius: 9px; background: #fff;
        box-shadow: 0 8px 22px rgba(26,30,39,0.45); }
    .eq::before { top: 20px; } .eq::after { top: 52px; }

    /* b16 — the comment field */
    .cmt { position: absolute; left: 130px; top: 250px; width: 820px;
           height: 180px; padding: 0 40px; display: flex; align-items: center;
           gap: 10px; font-size: 58px; font-weight: 900; color: var(--ink); }
    .caret { display: inline-block; width: 7px; height: 62px;
             background: var(--accent); }
    .cmtsend { position: absolute; right: 34px; width: 100px; height: 100px;
               border-radius: 50%; background: var(--lit-accent);
               box-shadow: var(--rim-dark); }
''')

# §5a.1 — squircle the large surfaces only; small repeated ones keep a radius,
# so the heavy-overlay budget that turns a render black is not blown.
for sel, w, h, r in [
    (".cutblock", 680, 340, 44), (".outline", 700, 420, 52),
    (".slide.big", 540, 400, 52), (".promptbox", 820, 230, 52),
    (".valcard.big", 480, 280, 58), (".cmt", 820, 180, 52),
    (".tile.brand", 300, 300, 74),
]:
    k.squircle(sel, w, h, r)


def main():
    caps = k.load_captions(os.path.join(ROOT, "work", "r5", "captions.json"))
    gh, gj = [], []
    for fn in BEATS:
        h, j = fn()
        gh.append(h.rstrip())
        gj.append("  /* %s */" % fn.__name__)
        gj.append(j.rstrip())

    defs = ('\n      <svg width="0" height="0" style="position:absolute">'
            '<defs><linearGradient id="swg" gradientUnits="userSpaceOnUse" '
            'x1="70" y1="0" x2="820" y2="0">'
            '<stop offset="0" stop-color="#ff8ab0"/>'
            '<stop offset="1" stop-color="#d0173a"/>'
            '</linearGradient></defs></svg>')

    doc = k.document(
        title="Reel 5 — презентації",
        plate="assets/base.mp4",
        gfx_html=defs + "\n" + "\n".join(gh),
        gfx_js="\n".join(gj),
        caps=caps,
    )
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "index.html")
    io.open(out, "w", encoding="utf-8").write(doc)
    print("index.html  %d captions, %d beats, %.1f KB"
          % (len(caps), len(BEATS), os.path.getsize(out) / 1024.0))


main()
