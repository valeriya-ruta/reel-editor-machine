# -*- coding: utf-8 -*-
"""Generate index.html for reel 3 — «дизайн без Фігми».

Variant B (STYLE.md §1): her cut arrives graded and with no subtitles, so this
owns both the animation and the captions.

Everything here obeys STYLE.md:
  - «не кажи — покажи»: a graphic carries no words. A number is allowed, and so
    is text inside a depicted interface, because that is an action being shown.
  - a visual event every 3-5s, each landing on its own word
  - centred, 600-900px wide, in the y 40-650 band that is empty in every shot
  - strokes >= 12px; nothing loops unless the loop is the meaning
  - no graphic outlives its sentence

usage: python build.py
"""
import io
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# The plate's last usable frame is 6276. base.mp4 reports 6282 frames and the
# container 104.763s, but the tail past frame 6276 decodes black -- rendering to
# the container duration put 9 black frames on the end of the reel. Length is
# therefore pinned to the frames that actually exist: 6277 / 60.
DUR = 104.6167
FPS = 60
W, H = 1080, 1920

CAP_Y = 1472          # caption centre — matches her burned-in captions on reel 2
CAP_SIZE = 90
GFX_TOP = 40          # graphics band: empty background in every shot of her cut
GFX_BOT = 650

RED = "#b4122f"
RED_DEEP = "#8d0d24"
PINK = "#ff6e9c"
INK = "#17141c"
PAPER = "#fdf1f4"


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


# ---------------------------------------------------------------- captions

def load_captions():
    p = os.path.join(ROOT, "work", "r3", "captions.json")
    return json.load(io.open(p, encoding="utf-8"))["words"]


def caption_html(caps):
    out = []
    for i, c in enumerate(caps):
        out.append('<div class="cap" id="cap%d">%s</div>'
                   % (i, esc(c["w"].upper())))
    return "\n      ".join(out)


# Windows where the animation says the word, so the caption does not.
# «the subtitles are always word by word, unless you want to use animation to
# substitute subtitles» -- her note. STYLE.md also records that she catches a
# graphic which duplicates her own subtitle, and «30%» on screen twice at once
# is exactly that.
# Windows where the caption stays but the scrim comes down: on a takeover pane
# the caption already has a clean ground, and the scrim shows through as a halo.
SCRIM_OFF = [
    (82.90, 86.70, "the Mobbin pane is its own ground"),
]

BLACKOUT = [
    (19.30, 21.90, "takeover: the grid counts out 30% itself"),
    (36.50, 39.40, "takeover: the two marks fusing is the whole sentence"),
]


def blacked(c):
    return any(a <= c["s"] < b for a, b, _ in BLACKOUT)


def caption_js(caps):
    """Instant on, instant off. One word at a time, as she asked.

    A fade would smear two words together at this rate -- the median caption is
    255ms and the shortest is 100ms.
    """
    lines = []
    for i, c in enumerate(caps):
        if blacked(c):
            continue
        lines.append('  tl.set("#cap%d", {autoAlpha: 1}, %.3f);' % (i, c["s"]))
        lines.append('  tl.set("#cap%d", {autoAlpha: 0}, %.3f);' % (i, c["e"]))
    # the scrim rides the whole spoken stretch rather than flickering per word
    lines.append('  tl.to("#scrim", {autoAlpha: 1, duration: 0.5}, %.3f);'
                 % max(0.0, caps[0]["s"] - 0.3))
    lines.append('  tl.to("#scrim", {autoAlpha: 0, duration: 0.6}, %.3f);'
                 % (caps[-1]["e"] + 0.1))
    # The scrim backs white text on her footage. A takeover has neither, and it
    # reads through the solid ground as a grey smudge under the card.
    for a, b, _why in list(BLACKOUT) + list(SCRIM_OFF):
        lines.append('  tl.to("#scrim", {autoAlpha: 0, duration: 0.20}, %.3f);'
                     % max(0.0, a - 0.20))
        lines.append('  tl.to("#scrim", {autoAlpha: 1, duration: 0.25}, %.3f);' % b)
    return "\n".join(lines)


# ---------------------------------------------------------------- beats
# Each beat is (html, js). js may use `tl` and the beat's own element ids.
# Times are bound to the word the beat lands on, taken from captions.json.

BEATS = []


def beat(fn):
    BEATS.append(fn)
    return fn


def card(idx, x, y, w, h, extra="", cls=""):
    return ('<div class="card %s" id="%s" style="left:%dpx;top:%dpx;'
            'width:%dpx;height:%dpx;%s"></div>' % (cls, idx, x, y, w, h, extra))


# ---- A · hook -------------------------------------------------------------

@beat
def b01_figma_gate():
    """«…працювати в фігмі?» — the premise, stated as an object."""
    html = '''
      <div class="g" id="g1">
        <div class="tile big" id="g1tile">
          <img src="assets/logos/figma.png" alt="">
        </div>
        <div class="qmark" id="g1q">?</div>
      </div>'''
    js = '''
  gsap.set("#g1", {autoAlpha: 0});
  gsap.set("#g1tile", {scale: 0.2, autoAlpha: 0, transformOrigin: "50% 50%"});
  gsap.set("#g1q", {scale: 0.3, autoAlpha: 0, transformOrigin: "50% 50%"});
  tl.to("#g1", {autoAlpha: 1, duration: 0.12}, 2.30);
  tl.to("#g1tile", {scale: 1, autoAlpha: 1, duration: 0.34, ease: "back.out(2.2)"}, 2.30);
  tl.to("#g1q", {scale: 1, autoAlpha: 1, duration: 0.26, ease: "back.out(3)"}, 3.92);
  tl.to("#g1", {autoAlpha: 0, scale: 0.86, duration: 0.26, ease: "power2.in"}, 4.42);'''
    return html, js


@beat
def b02_episode_three():
    """«Це третя серія» — a number is the one word-like thing STYLE.md allows."""
    html = '''
      <div class="g" id="g2">
        <div class="pips">
          <i class="pip" id="g2p1"></i><i class="pip" id="g2p2"></i>
          <i class="pip on" id="g2p3"></i><i class="pip" id="g2p4"></i>
        </div>
        <div class="bignum" id="g2n">3</div>
      </div>'''
    js = '''
  gsap.set("#g2", {autoAlpha: 0});
  gsap.set([".pip"], {scale: 0, transformOrigin: "50% 50%"});
  gsap.set("#g2n", {scale: 0.4, autoAlpha: 0, transformOrigin: "50% 50%"});
  tl.to("#g2", {autoAlpha: 1, duration: 0.10}, 4.58);
  tl.to("#g2p1", {scale: 1, duration: 0.16, ease: "back.out(3)"}, 4.62);
  tl.to("#g2p2", {scale: 1, duration: 0.16, ease: "back.out(3)"}, 4.74);
  tl.to("#g2p3", {scale: 1, duration: 0.16, ease: "back.out(3)"}, 4.86);
  tl.to("#g2n",  {scale: 1, autoAlpha: 1, duration: 0.30, ease: "back.out(2.4)"}, 4.90);
  tl.to("#g2p4", {scale: 1, duration: 0.16, ease: "back.out(3)"}, 5.60);
  tl.to("#g2", {autoAlpha: 0, y: -30, duration: 0.28, ease: "power2.in"}, 8.20);'''
    return html, js


@beat
def b03_ruta_app():
    """«починала розробляти Руту» — the app itself, since it exists."""
    html = '''
      <div class="g" id="g3">
        <div class="phone shot" id="g3p">
          <img src="assets/ruta-app.jpg" alt="">
        </div>
      </div>'''
    js = '''
  gsap.set("#g3", {autoAlpha: 0});
  gsap.set("#g3p", {scale: 0.7, rotation: -4, transformOrigin: "50% 60%"});
  tl.to("#g3", {autoAlpha: 1, duration: 0.22}, 10.40);
  tl.to("#g3p", {scale: 1, rotation: 0, duration: 0.46, ease: "back.out(1.7)"}, 10.40);
  tl.to("#g3", {autoAlpha: 0, scale: 0.9, duration: 0.26, ease: "power2.in"}, 12.30);'''
    return html, js


# ---- B · the Figma story --------------------------------------------------

@beat
def b04_bad_layout():
    """«ШІ не зробить гарний дизайн» — the thing she believed it would make."""
    html = '''
      <div class="g" id="g4">
        <div class="frame" id="g4f">
          <i class="blk" id="g4a"></i><i class="blk" id="g4b"></i>
          <i class="blk" id="g4c"></i><i class="blk" id="g4d"></i>
        </div>
      </div>'''
    js = '''
  gsap.set("#g4", {autoAlpha: 0});
  gsap.set("#g4f", {scale: 0.86, transformOrigin: "50% 50%"});
  gsap.set([".blk"], {scaleY: 0, transformOrigin: "50% 0%"});
  tl.to("#g4", {autoAlpha: 1, duration: 0.18}, 12.90);
  tl.to("#g4f", {scale: 1, duration: 0.34, ease: "power3.out"}, 12.90);
  tl.to("#g4a", {scaleY: 1, duration: 0.14, ease: "power2.out"}, 13.10);
  tl.to("#g4b", {scaleY: 1, duration: 0.14, ease: "power2.out"}, 13.26);
  tl.to("#g4c", {scaleY: 1, duration: 0.14, ease: "power2.out"}, 13.42);
  tl.to("#g4d", {scaleY: 1, duration: 0.14, ease: "power2.out"}, 13.58);
  // it lands crooked on «гарний» -- the blocks shove out of alignment
  tl.to("#g4a", {x: -96, y: -18, rotation: -7, duration: 0.20, ease: "power4.out"}, 13.70);
  tl.to("#g4b", {x: 54, y: 30, rotation: 5, duration: 0.20, ease: "power4.out"}, 13.76);
  tl.to("#g4c", {x: 88, y: -26, rotation: 8, duration: 0.20, ease: "power4.out"}, 13.82);
  tl.to("#g4d", {x: -40, y: 54, rotation: -6, duration: 0.20, ease: "power4.out"}, 13.88);
  tl.to("#g4", {autoAlpha: 0, duration: 0.24, ease: "power2.in"}, 14.70);'''
    return html, js


@beat
def b05_figma_canvas():
    """«обов'язково це зробити професійно в Фігмі» — the workspace, not the mark.

    Her note on the first cut: too many Figma logos between 20s and 30s. The
    mark already lands at 2.3s and again at 24.4s, so this beat shows what
    working in it actually looks like — a canvas filling with artboards.
    """
    html = '''
      <div class="g" id="g5">
        <div class="workspace" id="g5w">
          <i class="rail" id="g5r"></i>
          <i class="art" id="g5a1"></i><i class="art" id="g5a2"></i>
          <i class="art" id="g5a3"></i><i class="art" id="g5a4"></i>
        </div>
      </div>'''
    js = '''
  gsap.set("#g5", {autoAlpha: 0});
  gsap.set("#g5w", {scale: 0.88, transformOrigin: "50% 50%"});
  gsap.set("#g5r", {scaleY: 0, transformOrigin: "50% 0%"});
  gsap.set([".art"], {scale: 0, transformOrigin: "50% 50%"});
  tl.to("#g5", {autoAlpha: 1, duration: 0.16}, 15.60);
  tl.to("#g5w", {scale: 1, duration: 0.32, ease: "power3.out"}, 15.60);
  tl.to("#g5r", {scaleY: 1, duration: 0.24, ease: "power3.out"}, 15.76);
  tl.to("#g5a1", {scale: 1, duration: 0.22, ease: "back.out(2.4)"}, 16.10);
  tl.to("#g5a2", {scale: 1, duration: 0.22, ease: "back.out(2.4)"}, 16.34);
  tl.to("#g5a3", {scale: 1, duration: 0.22, ease: "back.out(2.4)"}, 16.58);
  tl.to("#g5a4", {scale: 1, duration: 0.22, ease: "back.out(2.4)"}, 16.82);
  tl.to("#g5", {autoAlpha: 0, duration: 0.24, ease: "power2.in"}, 18.30);'''
    return html, js



@beat
def b06_thirty_percent():
    """«зробила там десь 30% екранів» — 20 screens, 6 of them done.

    Full-frame takeover in the card language she pointed at: a solid ground in
    her red, translucent cards on top, hairline edges, separation coming from
    the translucency rather than a drop shadow. The number sits in its own card
    the way a value does in that reference -- without the label, because a
    graphic here carries no words.
    """
    cells = "".join('<i class="cell%s" id="g6s%d"><b class="cf"></b></i>'
                    % (" fill" if k in (0, 1, 4, 6, 9, 12) else "", k)
                    for k in range(20))
    html = '''
      <div class="g full" id="g6">
        <div class="ground" id="g6bg"></div>
        <div class="bigGrid" id="g6g">%s</div>
        <div class="valcard" id="g6n"><span>30%%</span></div>
      </div>''' % cells
    js = '''
  gsap.set("#g6", {autoAlpha: 0});
  gsap.set("#g6bg", {autoAlpha: 0});
  gsap.set(".cell", {scale: 0.6, autoAlpha: 0, transformOrigin: "50% 50%"});
  gsap.set(".cf", {autoAlpha: 0});
  gsap.set("#g6n", {scale: 0.8, autoAlpha: 0, transformOrigin: "50% 50%"});
  tl.to("#g6", {autoAlpha: 1, duration: 0.10}, 19.10);
  tl.to("#g6bg", {autoAlpha: 1, duration: 0.26, ease: "power2.out"}, 19.10);
  tl.to(".cell", {scale: 1, autoAlpha: 1, duration: 0.34, ease: "power3.out",
                  stagger: 0.020}, 19.34);
  // the six that are done fill on «30%» itself
  tl.to(".cell.fill .cf", {autoAlpha: 1, duration: 0.24,
                           ease: "power2.out", stagger: 0.05}, 20.40);
  tl.to("#g6n", {scale: 1, autoAlpha: 1, duration: 0.34, ease: "back.out(1.8)"}, 20.58);
  tl.to("#g6", {autoAlpha: 0, duration: 0.30, ease: "power2.in"}, 21.90);'''
    return html, js



@beat
def b07_figma_abandoned():
    """«у Фігмі не заходила взагалі… просто не потрібно» — one mark, two events.

    Was two separate beats, each with its own Figma tile. Her note was that the
    20-30s stretch repeats the logo, so the colour draining out and the strike
    now happen to the same object, which is also STYLE.md's «reuse objects».
    """
    html = '''
      <div class="g" id="g7">
        <div class="tile big" id="g7tile">
          <img src="assets/logos/figma.png" alt="">
        </div>
        <div class="dust" id="g7d1"></div>
        <div class="dust" id="g7d2"></div>
        <div class="dust" id="g7d3"></div>
        <div class="strike" id="g7s"></div>
      </div>'''
    js = '''
  gsap.set("#g7", {autoAlpha: 0});
  gsap.set("#g7tile", {scale: 0.9, transformOrigin: "50% 50%"});
  gsap.set([".dust"], {autoAlpha: 0, scale: 0.4, transformOrigin: "50% 50%"});
  gsap.set("#g7s", {scaleX: 0, transformOrigin: "0% 50%"});
  tl.to("#g7", {autoAlpha: 1, duration: 0.20}, 24.40);
  tl.to("#g7tile", {scale: 1, duration: 0.30, ease: "power3.out"}, 24.40);
  // «не заходила взагалі» — the colour drains out of it
  tl.to("#g7tile img", {filter: "grayscale(1)", opacity: 0.34,
                        duration: 0.60, ease: "power2.inOut"}, 26.40);
  tl.to("#g7d1", {autoAlpha: 0.85, scale: 1, x: -80, y: -46, duration: 0.55, ease: "power2.out"}, 26.60);
  tl.to("#g7d2", {autoAlpha: 0.85, scale: 1, x: 70, y: -62, duration: 0.55, ease: "power2.out"}, 26.72);
  tl.to("#g7d3", {autoAlpha: 0.85, scale: 1, x: 12, y: -80, duration: 0.55, ease: "power2.out"}, 26.84);
  tl.to([".dust"], {autoAlpha: 0, duration: 0.30}, 27.40);
  // «просто не потрібно» — struck through and dropped, same tile
  tl.to("#g7s", {scaleX: 1, duration: 0.20, ease: "power4.out"}, 29.54);
  tl.to("#g7", {y: 260, autoAlpha: 0, rotation: 8, duration: 0.46, ease: "power2.in"}, 29.98);'''
    return html, js




# ---- C · Claude Design ----------------------------------------------------

@beat
def b09_claude_arrives():
    """«У Клоді є штука» — the coral tile is its own brand mark, left as is."""
    html = '''
      <div class="g" id="g9">
        <div class="tile big claude" id="g9tile">
          <img src="assets/logos/claude-tile.png" alt="">
        </div>
        <div class="halo" id="g9h"></div>
      </div>'''
    js = '''
  gsap.set("#g9", {autoAlpha: 0});
  gsap.set("#g9tile", {scale: 0.3, transformOrigin: "50% 50%"});
  gsap.set("#g9h", {scale: 0.4, autoAlpha: 0, transformOrigin: "50% 50%"});
  tl.to("#g9", {autoAlpha: 1, duration: 0.14}, 33.40);
  tl.to("#g9tile", {scale: 1, duration: 0.40, ease: "back.out(2)"}, 33.40);
  tl.to("#g9h", {scale: 1, autoAlpha: 1, duration: 0.40, ease: "power2.out"}, 33.50);
  tl.to("#g9", {autoAlpha: 0, duration: 0.24, ease: "power2.in"}, 35.40);'''
    return html, js


@beat
def b10_merge():
    """«дитини штучного інтелекту і Фігми одночасно» — the two marks become one.

    Takeover #2, and the conceptual peak of the reel. Wordless, so the caption
    stands down and the picture makes the joke on its own.
    """
    html = '''
      <div class="g" id="g10">
        <div class="tile big claude" id="g10c">
          <img src="assets/logos/claude-tile.png" alt="">
        </div>
        <div class="tile big" id="g10f">
          <img src="assets/logos/figma.png" alt="">
        </div>
        <div class="plus" id="g10plus"></div>
        <div class="tile merged" id="g10m">
          <img src="assets/logos/claude-tile.png" alt="" class="mA">
          <img src="assets/logos/figma.png" alt="" class="mB">
        </div>
        <div class="burst" id="g10b"></div>
      </div>'''
    js = '''
  gsap.set("#g10", {autoAlpha: 0});
  gsap.set("#g10c", {x: -250, scale: 0.9, transformOrigin: "50% 50%"});
  gsap.set("#g10f", {x: 250, scale: 0.9, transformOrigin: "50% 50%"});
  gsap.set("#g10plus", {scale: 0, autoAlpha: 0, transformOrigin: "50% 50%"});
  gsap.set("#g10m", {scale: 0.2, autoAlpha: 0, transformOrigin: "50% 50%"});
  gsap.set("#g10b", {scale: 0.2, autoAlpha: 0, transformOrigin: "50% 50%"});
  tl.to("#g10", {autoAlpha: 1, duration: 0.14}, 36.30);
  tl.to("#g10c", {scale: 1, duration: 0.26, ease: "back.out(2)"}, 36.50);
  tl.to("#g10f", {scale: 1, duration: 0.26, ease: "back.out(2)"}, 36.62);
  tl.to("#g10plus", {scale: 1, autoAlpha: 1, duration: 0.20, ease: "back.out(3)"}, 36.92);
  // they converge on «дитини»
  tl.to("#g10c", {x: 0, duration: 0.34, ease: "power3.inOut"}, 37.50);
  tl.to("#g10f", {x: 0, duration: 0.34, ease: "power3.inOut"}, 37.50);
  tl.to("#g10plus", {scale: 0, autoAlpha: 0, duration: 0.18, ease: "power2.in"}, 37.62);
  tl.set(["#g10c", "#g10f"], {autoAlpha: 0}, 37.84);
  tl.to("#g10m", {scale: 1, autoAlpha: 1, duration: 0.30, ease: "back.out(2.6)"}, 37.84);
  tl.to("#g10b", {scale: 1.8, autoAlpha: 0.9, duration: 0.16, ease: "power2.out"}, 37.86);
  tl.to("#g10b", {scale: 2.6, autoAlpha: 0, duration: 0.40, ease: "power2.out"}, 38.02);
  tl.to("#g10", {autoAlpha: 0, scale: 1.04, duration: 0.30, ease: "power2.in"}, 39.40);'''
    return html, js



@beat
def b11_prototype():
    """«для дизайну додатків і прототипуванням» — screens flip through a phone."""
    html = '''
      <div class="g" id="g11">
        <div class="phone" id="g11p">
          <span class="pscr" id="g11a"><b class="ph"></b><b class="pr"></b><b class="pr"></b><b class="pr"></b></span>
          <span class="pscr" id="g11b"><b class="ph"></b><b class="pr"></b><b class="pr"></b><b class="pr"></b></span>
          <span class="pscr" id="g11c"><b class="ph"></b><b class="pr"></b><b class="pr"></b><b class="pr"></b></span>
        </div>
      </div>'''
    js = '''
  gsap.set("#g11", {autoAlpha: 0});
  gsap.set("#g11p", {scale: 0.7, transformOrigin: "50% 50%"});
  gsap.set(["#g11a", "#g11b", "#g11c"], {autoAlpha: 0, x: 90});
  tl.to("#g11", {autoAlpha: 1, duration: 0.18}, 42.30);
  tl.to("#g11p", {scale: 1, duration: 0.36, ease: "back.out(1.8)"}, 42.30);
  tl.to("#g11a", {autoAlpha: 1, x: 0, duration: 0.20, ease: "power3.out"}, 42.70);
  tl.to("#g11a", {autoAlpha: 0, x: -90, duration: 0.18, ease: "power3.in"}, 43.36);
  tl.to("#g11b", {autoAlpha: 1, x: 0, duration: 0.20, ease: "power3.out"}, 43.40);
  tl.to("#g11b", {autoAlpha: 0, x: -90, duration: 0.18, ease: "power3.in"}, 44.02);
  tl.to("#g11c", {autoAlpha: 1, x: 0, duration: 0.20, ease: "power3.out"}, 44.06);
  tl.to("#g11", {autoAlpha: 0, duration: 0.26, ease: "power2.in"}, 45.20);'''
    return html, js


# ---- D · the workflow -----------------------------------------------------

@beat
def b12_brainstorm():
    """«всі функції в брейнштормі» — one node branches into many."""
    html = '''
      <div class="g" id="g12">
        <svg id="g12svg" viewBox="0 0 880 470" width="880" height="470">
          <defs><linearGradient id="wireGrad" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ff8ab0"/><stop offset="1" stop-color="#d0173a"/></linearGradient></defs>
          <path class="wire" id="g12w1" d="M440 76 C 440 210, 110 200, 110 330"/>
          <path class="wire" id="g12w2" d="M440 76 C 440 230, 330 220, 330 370"/>
          <path class="wire" id="g12w3" d="M440 76 C 440 230, 550 220, 550 370"/>
          <path class="wire" id="g12w4" d="M440 76 C 440 210, 770 200, 770 330"/>
          <circle class="node hub" id="g12h" cx="440" cy="72" r="46"/>
          <circle class="node" id="g12n1" cx="110" cy="366" r="36"/>
          <circle class="node" id="g12n2" cx="330" cy="406" r="36"/>
          <circle class="node" id="g12n3" cx="550" cy="406" r="36"/>
          <circle class="node" id="g12n4" cx="770" cy="366" r="36"/>
        </svg>
      </div>'''
    js = '''
  gsap.set("#g12", {autoAlpha: 0});
  gsap.set("#g12h", {scale: 0, transformOrigin: "380px 56px"});
  ["#g12n1","#g12n2","#g12n3","#g12n4"].forEach(function (s, i) {
    var c = document.querySelector(s);
    gsap.set(s, {scale: 0, transformOrigin: c.getAttribute("cx") + "px " + c.getAttribute("cy") + "px"});
  });
  document.querySelectorAll("#g12svg .wire").forEach(function (p) {
    var L = p.getTotalLength();
    gsap.set(p, {strokeDasharray: L, strokeDashoffset: L});
  });
  tl.to("#g12", {autoAlpha: 1, duration: 0.16}, 45.60);
  tl.to("#g12h", {scale: 1, duration: 0.28, ease: "back.out(2.4)"}, 45.60);
  var wt = [46.34, 46.54, 46.74, 46.94];
  ["#g12w1","#g12w2","#g12w3","#g12w4"].forEach(function (s, i) {
    tl.to(s, {strokeDashoffset: 0, duration: 0.26, ease: "power2.out"}, wt[i]);
  });
  ["#g12n1","#g12n2","#g12n3","#g12n4"].forEach(function (s, i) {
    tl.to(s, {scale: 1, duration: 0.22, ease: "back.out(2.6)"}, wt[i] + 0.20);
  });
  tl.to("#g12", {autoAlpha: 0, duration: 0.26, ease: "power2.in"}, 48.40);'''
    return html, js


@beat
def b13_prompt():
    """«розповіла, який додаток бачу» — text inside an interface is allowed,
    because what is shown is the act of telling it."""
    html = '''
      <div class="g" id="g13">
        <div class="promptbox" id="g13box">
          <span class="ptext" id="g13t"></span><i class="caret" id="g13c"></i>
        </div>
        <div class="outrow" id="g13out">
          <span class="oscr" id="g13o1"><b class="ph"></b><b class="pr"></b><b class="pr"></b><b class="pr"></b></span>
          <span class="oscr" id="g13o2"><b class="ph"></b><b class="pr"></b><b class="pr"></b><b class="pr"></b></span>
          <span class="oscr" id="g13o3"><b class="ph"></b><b class="pr"></b><b class="pr"></b><b class="pr"></b></span>
        </div>
      </div>'''
    js = '''
  var P13 = "додаток для продюсерки";
  var t13 = {n: 0};
  var n13 = document.createTextNode("");
  document.getElementById("g13t").appendChild(n13);
  gsap.set("#g13", {autoAlpha: 0});
  gsap.set("#g13box", {scale: 0.9, transformOrigin: "50% 50%"});
  gsap.set([".oscr"], {scaleY: 0, autoAlpha: 0, transformOrigin: "50% 100%"});
  gsap.set("#g13c", {autoAlpha: 0});
  tl.to("#g13", {autoAlpha: 1, duration: 0.18}, 49.40);
  tl.to("#g13box", {scale: 1, duration: 0.30, ease: "back.out(1.8)"}, 49.40);
  tl.to("#g13c", {autoAlpha: 1, duration: 0.10}, 49.70);
  tl.to(t13, {n: P13.length, duration: 1.15, ease: "none",
              onUpdate: function () { n13.nodeValue = P13.slice(0, Math.floor(t13.n)); }}, 50.46);
  tl.to("#g13c", {autoAlpha: 0, duration: 0.10}, 51.70);
  tl.to("#g13o1", {scaleY: 1, autoAlpha: 1, duration: 0.22, ease: "back.out(2)"}, 51.80);
  tl.to("#g13o2", {scaleY: 1, autoAlpha: 1, duration: 0.22, ease: "back.out(2)"}, 51.94);
  tl.to("#g13o3", {scaleY: 1, autoAlpha: 1, duration: 0.22, ease: "back.out(2)"}, 52.08);
  tl.to("#g13", {autoAlpha: 0, duration: 0.24, ease: "power2.in"}, 53.00);'''
    return html, js


@beat
def b14_comments():
    """«коментуєш, виправляєш деталі» — pins land, one nudges a block straight."""
    html = '''
      <div class="g" id="g14">
        <div class="canvas" id="g14c">
          <i class="cblk" id="g14b1"></i><i class="cblk" id="g14b2"></i>
          <i class="cblk" id="g14b3"></i>
        </div>
        <div class="pin" id="g14p1"></div>
        <div class="pin" id="g14p2"></div>
      </div>'''
    js = '''
  gsap.set("#g14", {autoAlpha: 0});
  gsap.set("#g14c", {scale: 0.92, transformOrigin: "50% 50%"});
  gsap.set([".pin"], {scale: 0, autoAlpha: 0, transformOrigin: "50% 100%"});
  gsap.set("#g14b2", {x: 40, rotation: 4, transformOrigin: "50% 50%"});
  tl.to("#g14", {autoAlpha: 1, duration: 0.18}, 53.10);
  tl.to("#g14c", {scale: 1, duration: 0.28, ease: "power3.out"}, 53.10);
  tl.to("#g14p1", {scale: 1, autoAlpha: 1, duration: 0.22, ease: "back.out(3)"}, 53.46);
  tl.to("#g14p2", {scale: 1, autoAlpha: 1, duration: 0.22, ease: "back.out(3)"}, 53.86);
  // «виправляєш» — the crooked block snaps into line
  tl.to("#g14b2", {x: 0, rotation: 0, duration: 0.26, ease: "back.out(2.2)"}, 54.40);
  tl.to("#g14", {autoAlpha: 0, duration: 0.24, ease: "power2.in"}, 55.30);'''
    return html, js


@beat
def b15_tap():
    """«потикала прототип з телефону» — taps ripple where a thumb would land."""
    html = '''
      <div class="g" id="g15">
        <div class="phone" id="g15p"><i class="pscr on" id="g15s"></i></div>
        <div class="ripple" id="g15r1"></div>
        <div class="ripple" id="g15r2"></div>
      </div>'''
    js = '''
  gsap.set("#g15", {autoAlpha: 0});
  gsap.set("#g15p", {scale: 0.8, rotation: 6, transformOrigin: "50% 70%"});
  gsap.set([".ripple"], {scale: 0.2, autoAlpha: 0, transformOrigin: "50% 50%"});
  tl.to("#g15", {autoAlpha: 1, duration: 0.18}, 55.60);
  tl.to("#g15p", {scale: 1, rotation: 0, duration: 0.40, ease: "back.out(1.6)"}, 55.60);
  tl.to("#g15r1", {scale: 1.6, autoAlpha: 0.9, duration: 0.14, ease: "power2.out"}, 56.30);
  tl.to("#g15r1", {scale: 2.4, autoAlpha: 0, duration: 0.34, ease: "power2.out"}, 56.44);
  tl.to("#g15r2", {scale: 1.6, autoAlpha: 0.9, duration: 0.14, ease: "power2.out"}, 57.00);
  tl.to("#g15r2", {scale: 2.4, autoAlpha: 0, duration: 0.34, ease: "power2.out"}, 57.14);
  tl.to("#g15", {autoAlpha: 0, duration: 0.24, ease: "power2.in"}, 58.20);'''
    return html, js


@beat
def b16_handoff():
    """«однією кнопкою… у Клод Код… і він зробить точнісінько так, як я скинула»

    Takeover #3, and the rebuild of the beat she called weird. The old version
    was an abstract red pill over a white card; this one tells the actual story
    — the design goes in on the button press, the code writes itself, and the
    same design comes back out. It absorbs the old «точнісінько» beat, which was
    the payoff of this one all along.

    The code pane is deliberately parked under the caption line so her white
    subtitles keep their contrast through the takeover, instead of being
    suppressed for six seconds.
    """
    html = '''
      <div class="g full" id="g16">
        <div class="tko" id="g16bg"></div>
        <div class="phone fs" id="g16p">
          <span class="pscr"><b class="ph"></b><b class="pr"></b><b class="pr"></b><b class="pr"></b></span>
        </div>
        <div class="btn" id="g16btn"></div>
        <div class="codepane" id="g16code">
          <i class="cl" id="g16l1"></i><i class="cl" id="g16l2"></i>
          <i class="cl gap" id="g16l3"></i><i class="cl" id="g16l4"></i>
          <i class="cl" id="g16l5"></i>
        </div>
        <div class="tickring" id="g16r"></div>
      </div>'''
    js = '''
  gsap.set("#g16", {autoAlpha: 0});
  gsap.set("#g16bg", {scaleY: 0, transformOrigin: "50% 50%"});
  gsap.set("#g16p", {scale: 0.7, autoAlpha: 0, y: 0, transformOrigin: "50% 50%"});
  gsap.set("#g16btn", {scale: 0.4, autoAlpha: 0, transformOrigin: "50% 50%"});
  gsap.set("#g16code", {y: 260, autoAlpha: 0});
  gsap.set([".cl"], {scaleX: 0, transformOrigin: "0% 50%"});
  gsap.set("#g16r", {scale: 0.4, autoAlpha: 0, transformOrigin: "50% 50%"});
  tl.to("#g16", {autoAlpha: 1, duration: 0.14}, 60.20);
  tl.to("#g16bg", {scaleY: 1, duration: 0.30, ease: "power4.out"}, 60.20);
  tl.to("#g16p", {scale: 1, autoAlpha: 1, duration: 0.34, ease: "back.out(1.8)"}, 60.34);
  tl.to("#g16btn", {scale: 1, autoAlpha: 1, duration: 0.26, ease: "back.out(2.4)"}, 60.50);
  // the press lands exactly on «кнопкою»
  tl.to("#g16btn", {scale: 0.86, duration: 0.09, ease: "power3.in"}, 60.78);
  tl.to("#g16btn", {scale: 1, duration: 0.20, ease: "back.out(3)"}, 60.87);
  // the design drops into the editor
  tl.to("#g16code", {y: 0, autoAlpha: 1, duration: 0.40, ease: "power3.out"}, 61.30);
  tl.to("#g16p", {y: 780, scale: 0.42, duration: 0.66, ease: "power2.inOut"}, 61.42);
  tl.to("#g16btn", {autoAlpha: 0, scale: 0.8, duration: 0.22, ease: "power2.in"}, 61.42);
  tl.to("#g16p", {autoAlpha: 0, duration: 0.20}, 62.30);
  // «розробляй» — the code writes itself
  var lt = [63.75, 63.94, 64.13, 64.32, 64.51];
  ["#g16l1","#g16l2","#g16l3","#g16l4","#g16l5"].forEach(function (s, i) {
    tl.to(s, {scaleX: 1, duration: 0.16, ease: "power2.out"}, lt[i]);
  });
  // «точнісінько так, як я скинула» — the same design comes back out
  tl.to("#g16p", {autoAlpha: 1, duration: 0.20}, 66.00);
  tl.to("#g16p", {y: 0, scale: 1, duration: 0.52, ease: "back.out(1.5)"}, 66.00);
  tl.to("#g16r", {scale: 1.5, autoAlpha: 0.9, duration: 0.18, ease: "power2.out"}, 66.60);
  tl.to("#g16r", {scale: 2.1, autoAlpha: 0, duration: 0.44, ease: "power2.out"}, 66.78);
  tl.to("#g16", {autoAlpha: 0, duration: 0.30, ease: "power2.in"}, 68.40);'''
    return html, js




@beat
def b18_no_exports():
    """«без жодних експортів і скріншотів» — both struck out."""
    html = '''
      <div class="g" id="g18">
        <div class="pairrow" id="g18r">
          <div class="tile sm" id="g18a"><svg viewBox="0 0 100 100"><path d="M50 20 v44 M32 48 l18 18 18-18 M24 78 h52" fill="none" stroke="#fff" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/></svg></div>
          <div class="tile sm" id="g18b"><svg viewBox="0 0 100 100"><rect x="20" y="28" width="60" height="46" rx="7" fill="none" stroke="#fff" stroke-width="12"/><circle cx="50" cy="51" r="12" fill="none" stroke="#fff" stroke-width="12"/></svg></div>
        </div>
        <div class="strike thin" id="g18s1"></div>
        <div class="strike thin" id="g18s2"></div>
      </div>'''
    js = '''
  gsap.set("#g18", {autoAlpha: 0});
  gsap.set(["#g18a", "#g18b"], {scale: 0.5, autoAlpha: 0, transformOrigin: "50% 50%"});
  gsap.set(["#g18s1", "#g18s2"], {scaleX: 0, transformOrigin: "0% 50%"});
  tl.to("#g18", {autoAlpha: 1, duration: 0.16}, 69.40);
  tl.to("#g18a", {scale: 1, autoAlpha: 1, duration: 0.24, ease: "back.out(2.4)"}, 69.40);
  tl.to("#g18b", {scale: 1, autoAlpha: 1, duration: 0.24, ease: "back.out(2.4)"}, 69.56);
  tl.to("#g18s1", {scaleX: 1, duration: 0.16, ease: "power4.out"}, 69.94);
  tl.to("#g18s2", {scaleX: 1, duration: 0.16, ease: "power4.out"}, 70.72);
  tl.to("#g18", {autoAlpha: 0, duration: 0.24, ease: "power2.in"}, 71.60);'''
    return html, js


# ---- E · two lifehacks ----------------------------------------------------

@beat
def b19_two():
    """«два лайфхаки» — two slots open and stay open for beats 20 and 21."""
    html = '''
      <div class="g" id="g19">
        <div class="slot" id="g19s1">
          <div class="slotfill" id="g19f1"></div>
          <img class="slotlogo" id="g19i1" src="assets/logos/claude-tile.png" alt="">
        </div>
        <div class="slot" id="g19s2">
          <div class="slotfill" id="g19f2"></div>
          <img class="slotlogo wide" id="g19i2" src="assets/logos/mobbin-word.png" alt="">
        </div>
        <div class="bignum small" id="g19n">2</div>
      </div>'''
    js = '''
  gsap.set("#g19", {autoAlpha: 0});
  gsap.set(["#g19s1", "#g19s2"], {scale: 0.3, autoAlpha: 0, transformOrigin: "50% 50%"});
  gsap.set(["#g19f1", "#g19f2"], {scaleX: 0, transformOrigin: "0% 50%"});
  gsap.set(["#g19i1", "#g19i2"], {autoAlpha: 0, scale: 0.6, transformOrigin: "50% 50%"});
  gsap.set("#g19n", {scale: 0.4, autoAlpha: 0, transformOrigin: "50% 50%"});
  tl.to("#g19", {autoAlpha: 1, duration: 0.16}, 71.90);
  tl.to("#g19n", {scale: 1, autoAlpha: 1, duration: 0.26, ease: "back.out(2.6)"}, 72.08);
  tl.to("#g19s1", {scale: 1, autoAlpha: 1, duration: 0.28, ease: "back.out(2.2)"}, 72.30);
  tl.to("#g19s2", {scale: 1, autoAlpha: 1, duration: 0.28, ease: "back.out(2.2)"}, 72.48);
  tl.to("#g19n", {scale: 0.5, autoAlpha: 0, y: -40, duration: 0.30, ease: "power2.in"}, 74.60);
  // «Перший — скіл» : slot 1 fills
  tl.to("#g19f1", {scaleX: 1, duration: 0.34, ease: "power3.out"}, 75.52);
  tl.to("#g19i1", {autoAlpha: 1, scale: 1, duration: 0.28, ease: "back.out(2.4)"}, 75.70);
  // «допомагає розробити його якісно» — slot 1 answers rather than sitting still
  tl.to("#g19s1", {scale: 1.06, duration: 0.14, ease: "power3.out"}, 77.48);
  tl.to("#g19s1", {scale: 1, duration: 0.30, ease: "power2.out"}, 77.62);
  // «Другий — Mobbin» : slot 2 fills
  tl.to("#g19f2", {scaleX: 1, duration: 0.34, ease: "power3.out"}, 80.10);
  tl.to("#g19i2", {autoAlpha: 1, scale: 1, duration: 0.28, ease: "back.out(2.4)"}, 80.80);
  tl.to("#g19", {autoAlpha: 0, duration: 0.28, ease: "power2.in"}, 82.60);'''
    return html, js


@beat
def b20_mobbin():
    """«збірка найкращих додатків з усіма їхніми елементами й процесами»

    Her own capture of Mobbin, cut from the scroll at the head of the recording
    and run at 2.8x so a ten-second browse lands inside a 3.6s beat. Solid
    ground behind it in the palette, which is also what keeps her white
    captions readable over a bright product UI.
    """
    html = '''
      <div class="g full" id="g20">
        <div class="ground" id="g20bg"></div>
        <div class="mobframe" id="g20f">
          <video id="g20v" src="assets/mobbin-scroll.mp4"
                 data-start="83.06" data-duration="3.48" data-media-start="0"
                 muted playsinline></video>
        </div>
      </div>'''
    js = '''
  gsap.set("#g20", {autoAlpha: 0});
  gsap.set("#g20bg", {autoAlpha: 0});
  gsap.set("#g20f", {scale: 0.86, autoAlpha: 0, transformOrigin: "50% 50%"});
  tl.to("#g20", {autoAlpha: 1, duration: 0.10}, 83.00);
  tl.to("#g20bg", {autoAlpha: 1, duration: 0.26, ease: "power2.out"}, 83.00);
  tl.to("#g20f", {scale: 1, autoAlpha: 1, duration: 0.40, ease: "power3.out"}, 83.04);
  tl.to("#g20", {autoAlpha: 0, duration: 0.30, ease: "power2.in"}, 86.30);'''
    return html, js



@beat
def b21_wire():
    """«підключити до Клода» — a thick wire, and screens travelling along it."""
    html = '''
      <div class="g" id="g21">
        <div class="tile big" id="g21m"><img src="assets/logos/mobbin-mark.png" alt=""></div>
        <div class="tile big claude" id="g21c"><img src="assets/logos/claude-tile.png" alt=""></div>
        <svg id="g21svg" viewBox="0 0 1080 120" width="1080" height="120">
          <defs><linearGradient id="wireGrad2" gradientUnits="userSpaceOnUse" x1="392" y1="0" x2="688" y2="0"><stop offset="0" stop-color="#ff8ab0"/><stop offset="1" stop-color="#d0173a"/></linearGradient></defs>
          <path class="wire fat" id="g21w" d="M 392 60 H 688"/>
        </svg>
        <i class="pkt" id="g21k1"></i><i class="pkt" id="g21k2"></i>
      </div>'''
    js = '''
  gsap.set("#g21", {autoAlpha: 0});
  gsap.set("#g21m", {scale: 0.5, autoAlpha: 0, transformOrigin: "50% 50%"});
  gsap.set("#g21c", {scale: 0.5, autoAlpha: 0, transformOrigin: "50% 50%"});
  gsap.set([".pkt"], {autoAlpha: 0, x: 0});
  (function () {
    var p = document.getElementById("g21w"), L = p.getTotalLength();
    gsap.set(p, {strokeDasharray: L, strokeDashoffset: L});
  })();
  tl.to("#g21", {autoAlpha: 1, duration: 0.16}, 87.00);
  tl.to("#g21m", {scale: 1, autoAlpha: 1, duration: 0.26, ease: "back.out(2.2)"}, 87.00);
  tl.to("#g21c", {scale: 1, autoAlpha: 1, duration: 0.26, ease: "back.out(2.2)"}, 87.16);
  tl.to("#g21w", {strokeDashoffset: 0, duration: 0.34, ease: "power2.out"}, 87.40);
  tl.to("#g21k1", {autoAlpha: 1, duration: 0.10}, 88.20);
  tl.to("#g21k1", {x: 250, duration: 0.66, ease: "power1.inOut"}, 88.24);
  tl.to("#g21k1", {autoAlpha: 0, duration: 0.12}, 88.80);
  tl.to("#g21k2", {autoAlpha: 1, duration: 0.10}, 89.10);
  tl.to("#g21k2", {x: 250, duration: 0.66, ease: "power1.inOut"}, 89.14);
  tl.to("#g21k2", {autoAlpha: 0, duration: 0.12}, 89.70);
  tl.to("#g21", {autoAlpha: 0, duration: 0.26, ease: "power2.in"}, 91.20);'''
    return html, js


@beat
def b22_first_time():
    """«класно з першого разу» — one screen, landing right, once."""
    html = '''
      <div class="g" id="g22">
        <div class="phone good" id="g22p"><i class="pscr on" id="g22s"></i></div>
        <div class="tickring" id="g22r"></div>
      </div>'''
    js = '''
  gsap.set("#g22", {autoAlpha: 0});
  gsap.set("#g22p", {scale: 0.6, autoAlpha: 0, transformOrigin: "50% 50%"});
  gsap.set("#g22r", {scale: 0.4, autoAlpha: 0, transformOrigin: "50% 50%"});
  tl.to("#g22", {autoAlpha: 1, duration: 0.14}, 92.60);
  tl.to("#g22p", {scale: 1, autoAlpha: 1, duration: 0.34, ease: "back.out(2.2)"}, 92.60);
  tl.to("#g22r", {scale: 1.5, autoAlpha: 0.9, duration: 0.18, ease: "power2.out"}, 93.00);
  tl.to("#g22r", {scale: 2.1, autoAlpha: 0, duration: 0.40, ease: "power2.out"}, 93.18);
  tl.to("#g22", {autoAlpha: 0, duration: 0.26, ease: "power2.in"}, 95.20);'''
    return html, js


# ---- F · outro ------------------------------------------------------------

@beat
def b23_three_tools():
    """«Claude, Codex чи Cursor» — the three real marks, chosen between.

    She supplied the Codex and Cursor marks after the first render, so the
    neutral stand-in cards are gone and the ring now steps across the actual
    app tiles as she names each one.
    """
    html = '''
      <div class="g" id="g23">
        <div class="triorow" id="g23r">
          <div class="slot sq" id="g23a"><img src="assets/logos/claude-tile.png" alt=""></div>
          <div class="slot sq" id="g23b"><img src="assets/logos/codex-tile.png" alt=""></div>
          <div class="slot sq" id="g23c"><img src="assets/logos/cursor-tile.png" alt=""></div>
        </div>
        <div class="chooser" id="g23pick"></div>
      </div>'''
    js = '''
  gsap.set("#g23", {autoAlpha: 0});
  gsap.set(["#g23a", "#g23b", "#g23c"], {scale: 0.3, autoAlpha: 0, transformOrigin: "50% 50%"});
  gsap.set("#g23pick", {autoAlpha: 0, x: 0, transformOrigin: "50% 50%"});
  tl.to("#g23", {autoAlpha: 1, duration: 0.14}, 99.10);
  tl.to("#g23a", {scale: 1, autoAlpha: 1, duration: 0.26, ease: "back.out(2.4)"}, 99.20);
  tl.to("#g23b", {scale: 1, autoAlpha: 1, duration: 0.26, ease: "back.out(2.4)"}, 99.36);
  tl.to("#g23c", {scale: 1, autoAlpha: 1, duration: 0.26, ease: "back.out(2.4)"}, 99.52);
  // the ring steps across on each name she says
  tl.to("#g23pick", {autoAlpha: 1, duration: 0.14}, 99.28);
  tl.to("#g23pick", {x: 310, duration: 0.24, ease: "power3.inOut"}, 99.96);
  tl.to("#g23pick", {x: 620, duration: 0.24, ease: "power3.inOut"}, 100.48);
  tl.to("#g23", {autoAlpha: 0, duration: 0.26, ease: "power2.in"}, 101.40);'''
    return html, js



@beat
def b24_subscribe():
    """«підпишись, щоб не пропустити наступні» — the episode pips return and a
    fourth one lights: the next video. Reusing the object from beat 2."""
    html = '''
      <div class="g" id="g24">
        <div class="pips big">
          <i class="pip on" id="g24p1"></i><i class="pip on" id="g24p2"></i>
          <i class="pip on" id="g24p3"></i><i class="pip next" id="g24p4"></i>
        </div>
        <div class="halo soft" id="g24h"></div>
      </div>'''
    js = '''
  gsap.set("#g24", {autoAlpha: 0});
  gsap.set(["#g24p1","#g24p2","#g24p3","#g24p4"], {scale: 0, transformOrigin: "50% 50%"});
  gsap.set("#g24h", {scale: 0.4, autoAlpha: 0, transformOrigin: "50% 50%"});
  tl.to("#g24", {autoAlpha: 1, duration: 0.14}, 101.70);
  tl.to("#g24p1", {scale: 1, duration: 0.18, ease: "back.out(3)"}, 101.70);
  tl.to("#g24p2", {scale: 1, duration: 0.18, ease: "back.out(3)"}, 101.82);
  tl.to("#g24p3", {scale: 1, duration: 0.18, ease: "back.out(3)"}, 101.94);
  tl.to("#g24p4", {scale: 1, duration: 0.26, ease: "back.out(3)"}, 102.22);
  tl.to("#g24h", {scale: 1.4, autoAlpha: 0.85, duration: 0.20, ease: "power2.out"}, 102.30);
  tl.to("#g24h", {scale: 2.0, autoAlpha: 0, duration: 0.50, ease: "power2.out"}, 102.50);
  tl.to("#g24", {autoAlpha: 0, duration: 0.30, ease: "power2.in"}, 104.20);'''
    return html, js


# ---------------------------------------------------------------- assembly

CSS = """
    #root {
      /* §5a.4 — a tonal ladder, not two values. The accent appears once. */
      --surface:        #fdf6f6;
      --container:      #f4dde2;
      --container-high: #ecc8d0;
      --graphite:       rgba(23,20,28,0.13);
      --accent:         #b4122f;
      --accent-deep:    #8d0d24;
      --pink:           #ff6e9c;
      --ink:            #17141c;

      /* §5a.5 — never a flat fill */
      --lit:       linear-gradient(115deg, #ffffff 0%%, #fafafb 100%%);
      --lit-blush: linear-gradient(115deg, #fffdfd 0%%, #fdf1f4 100%%);
      --lit-accent:linear-gradient(115deg, #c41434 0%%, #8d0d24 100%%);
      --lit-pink:  linear-gradient(115deg, #ff8ab0 0%%, #ff5c8f 100%%);
      --lit-ink:   linear-gradient(115deg, #241f2c 0%%, #17141c 100%%);

      /* §5a.6 — edge light, bright on top, almost gone at the bottom */
      --rim: inset 0 1.5px 0 rgba(255,255,255,0.92),
             inset 0 -1.5px 0 rgba(255,255,255,0.14),
             inset 0 0 0 1px rgba(255,255,255,0.28);
      --rim-dark: inset 0 1.5px 0 rgba(255,255,255,0.16),
                  inset 0 0 0 1px rgba(255,255,255,0.08);

      /* §5a.7 — ambient, not drop. Doubled from the spec because these sit
         over footage rather than on a light page. */
      --cast: drop-shadow(0 1px 2px rgba(26,30,39,0.10))
              drop-shadow(0 24px 48px rgba(26,30,39,0.14));
      --cast-sm: drop-shadow(0 1px 2px rgba(26,30,39,0.08))
                 drop-shadow(0 12px 24px rgba(26,30,39,0.12));
    }

    @font-face {
      font-family: "ProductSans";
      src: url("assets/fonts/ProductSans-Black.woff") format("woff");
      font-weight: 900; font-style: normal; font-display: block;
    }
    * { margin: 0; padding: 0; box-sizing: border-box; }
    #root {
      position: relative; width: %(W)dpx; height: %(H)dpx;
      overflow: hidden; background: #000;
      font-family: "ProductSans", system-ui, sans-serif;
      --red: %(RED)s; --red-deep: %(RED_DEEP)s; --paper: %(PAPER)s;
    }
    .plate { position: absolute; inset: 0; width: %(W)dpx; height: %(H)dpx;
             object-fit: cover; }

    /* ---- captions ---- */
    #scrim {
      position: absolute; left: 20px; top: %(SCRIM_TOP)dpx;
      width: 1040px; height: 450px;
      background-image: url("assets/underlay.png");
      background-size: 100%% 100%%; background-repeat: no-repeat;
      opacity: 0; visibility: hidden; pointer-events: none;
    }
    .cap {
      position: absolute; left: 0; width: %(W)dpx; top: %(CAP_TOP)dpx;
      height: %(CAP_H)dpx; line-height: %(CAP_H)dpx;
      text-align: center; color: #fff;
      font-size: %(CAP_SIZE)dpx; font-weight: 900;
      letter-spacing: -0.015em; white-space: nowrap;
      opacity: 0; visibility: hidden;
    }

    /* ---- stage ---- */
    .g { position: absolute; left: 0; top: %(GFX_TOP)dpx;
         width: %(W)dpx; height: %(GFX_H)dpx;
         opacity: 0; visibility: hidden; }
    .g.full { top: 0; height: %(H)dpx; }

    /* A takeover is a solid ground in the palette with glass cards on it --
       her own reference. Frosting the footage instead blurs her out of her
       reel, which was rejected on v2. */
    /* A takeover is a sheet of tinted glass laid ON the footage, not a fill
       that replaces it. The margin is the point: edge-to-edge reads as a blur
       applied to the video, while an inset pane with a lit rim reads as an
       object on top, and she stays visible moving behind it. */
    .ground { position: absolute; left: 44px; top: 64px;
              width: 992px; height: 1792px;
              background: linear-gradient(158deg, rgba(196,20,52,0.62) 0%%,
                          rgba(141,13,36,0.70) 100%%);
              -webkit-backdrop-filter: blur(30px) saturate(1.5);
              backdrop-filter: blur(30px) saturate(1.5);
              box-shadow: inset 0 2px 0 rgba(255,255,255,0.70),
                          inset 0 -2px 0 rgba(255,255,255,0.10),
                          inset 0 0 0 1.5px rgba(255,255,255,0.30);
              filter: var(--cast);
              clip-path: path('M 825.6 0 c 55.507 0 83.26 0 108.228 12.722 a 104 104 0 0 1 45.45 45.45 c 12.722 24.968 12.722 52.722 12.722 108.228 L 992 1625.6 c 0 55.507 0 83.26 -12.722 108.228 a 104 104 0 0 1 -45.45 45.45 c -24.968 12.722 -52.722 12.722 -108.228 12.722 L 166.4 1792 c -55.507 0 -83.26 0 -108.228 -12.722 a 104 104 0 0 1 -45.45 -45.45 c -12.722 -24.968 -12.722 -52.722 -12.722 -108.228 L 0 166.4 c 0 -55.507 0 -83.26 12.722 -108.228 a 104 104 0 0 1 45.45 -45.45 c 24.968 -12.722 52.722 -12.722 108.228 -12.722 Z'); }

    /* ---- surfaces ---- */
    .tile { position: absolute; display: grid; place-items: center;
            background: var(--lit-blush); filter: var(--cast);
            box-shadow: var(--rim); }
    .tile.big { width: 360px; height: 360px; left: 360px; top: 125px; }
    .tile.big img { height: 236px; width: auto; }
    .tile.big.fs { top: 700px; }
    .tile.claude { background: none; box-shadow: none; }
    .tile.claude img { height: 360px; width: 360px; }
    .tile.sm { width: 240px; height: 240px; background: var(--lit-accent);
               top: 170px; box-shadow: var(--rim-dark); }
    .tile.sm svg { width: 150px; height: 150px; }
    .tile.merged { width: 440px; height: 440px; left: 320px; top: 95px;
                   background: var(--lit-blush); overflow: hidden; }
    .tile.merged .mA { position: absolute; left: 0; top: 0;
                       width: 440px; height: 440px;
                       clip-path: inset(0 50%% 0 0); }
    .tile.merged .mB { position: absolute; height: 268px; width: auto;
                       left: 246px; top: 86px; }

    #g1tile { left: 268px; }
    .qmark { position: absolute; left: 686px; top: 158px;
             font-size: 250px; line-height: 250px; font-weight: 900;
             color: %(PINK)s;
             filter: drop-shadow(0 2px 0 rgba(255,255,255,0.45))
                     drop-shadow(0 20px 40px rgba(26,30,39,0.30)); }

    /* ---- radial accents ---- */
    .ring, .halo, .burst, .tickring, .ripple {
      position: absolute; border-radius: 50%%; pointer-events: none; }
    .ring     { width: 480px; height: 480px; left: 300px; top: 65px;
                border: 18px solid rgba(255,110,156,0.92);
                filter: drop-shadow(0 0 40px rgba(255,110,156,0.55)); }
    .tickring { width: 480px; height: 480px; left: 300px; top: 340px;
                border: 18px solid rgba(255,110,156,0.92);
                filter: drop-shadow(0 0 40px rgba(255,110,156,0.55)); }
    .halo { width: 540px; height: 540px; left: 270px; top: 35px;
            background: radial-gradient(circle, rgba(255,110,156,0.5) 0%%,
                        rgba(255,110,156,0) 70%%); }
    .halo.soft { width: 420px; height: 420px; left: 600px; top: 35px; }
    .burst { width: 700px; height: 700px; left: 190px; top: -35px;
             background: radial-gradient(circle, rgba(255,255,255,0.9) 0%%,
                         rgba(255,138,176,0.5) 42%%, rgba(255,110,156,0) 72%%); }
    .ripple { width: 180px; height: 180px;
              border: 15px solid rgba(255,110,156,0.9);
              filter: drop-shadow(0 0 30px rgba(255,110,156,0.5)); }
    #g15r1 { left: 428px; top: 172px; }
    #g15r2 { left: 468px; top: 322px; }

    /* ---- episode pips. §5a.8: the row deliberately mixes shapes ---- */
    .pips { position: absolute; left: 290px; top: 330px;
            display: flex; gap: 44px; align-items: center; }
    .pips.big { left: 205px; top: 200px; gap: 50px; }
    .pip { width: 92px; height: 26px; border-radius: 13px; display: block;
           background: rgba(255,255,255,0.40);
           box-shadow: inset 0 1px 0 rgba(255,255,255,0.6); }
    .pips.big .pip { width: 130px; height: 90px; border-radius: 0; }
    .pip.on { background: var(--lit-accent); filter: var(--cast-sm);
              box-shadow: var(--rim-dark); }
    .pip.next { background: var(--lit-pink);
                filter: drop-shadow(0 0 40px rgba(255,110,156,0.9))
                        drop-shadow(0 12px 24px rgba(26,30,39,0.2));
                box-shadow: var(--rim-dark); }

    .bignum { position: absolute; left: 0; width: %(W)dpx; text-align: center;
              top: 60px; font-size: 230px; line-height: 230px;
              font-weight: 900; letter-spacing: -0.05em; color: #fff;
              text-shadow: 0 2px 0 rgba(255,255,255,0.4),
                           0 22px 48px rgba(26,30,39,0.55); }
    .bignum.small { top: 30px; font-size: 150px; line-height: 150px; }
    .valcard { position: absolute; left: 280px; top: 1240px;
               width: 520px; height: 230px;
               background: rgba(255,255,255,0.16);
               -webkit-backdrop-filter: blur(16px) saturate(1.3);
               backdrop-filter: blur(16px) saturate(1.3);
               box-shadow: var(--rim-dark);
               display: grid; place-items: center; }
    .valcard span { font-size: 150px; line-height: 150px; color: #fff;
                    font-weight: 900; letter-spacing: -0.04em; }

    /* ---- bar rhythm. §5a.3: a heading and ragged body, never a skeleton ---- */
    .ph { display: block; height: 66px; border-radius: 18px;
          background: var(--lit-accent); margin-bottom: 26px;
          box-shadow: var(--rim-dark); }
    .pr { display: block; height: 40px; border-radius: 12px;
          background: var(--graphite); margin-bottom: 18px; }
    .pr:nth-of-type(2) { width: 94%%; }
    .pr:nth-of-type(3) { width: 71%%; }
    .pr:nth-of-type(4) { width: 43%%; }

    /* b04 — the layout that comes out wrong */
    .frame { position: absolute; left: 180px; top: 45px; overflow: visible;
             width: 720px; height: 520px; background: var(--lit-blush);
             filter: var(--cast); box-shadow: var(--rim);
             padding: 46px; display: flex; flex-wrap: wrap;
             align-content: flex-start; gap: 22px; }
    .blk { display: block; width: 296px; height: 88px; border-radius: 24px;
           background: var(--container); }
    #g4b { width: 232px; }
    #g4c { width: 356px; }
    #g4a { background: var(--lit-accent); box-shadow: var(--rim-dark); }
    #g4d { width: 614px; }

    /* b05 — the Figma workspace */
    .workspace { position: absolute; left: 110px; top: 85px;
                 width: 860px; height: 440px; background: var(--lit-blush);
                 filter: var(--cast); box-shadow: var(--rim); }
    .rail { position: absolute; left: 34px; top: 34px; display: block;
            width: 92px; height: 372px; border-radius: 30px;
            background: var(--container); }
    .art { position: absolute; display: block; background: var(--container);
           box-shadow: inset 0 1.5px 0 rgba(255,255,255,0.7); }
    #g5a2 { background: var(--container-high); }
    #g5a1 { left: 168px; top: 46px;  width: 300px; height: 168px; }
    #g5a2 { left: 500px; top: 46px;  width: 320px; height: 168px; }
    #g5a3 { left: 168px; top: 240px; width: 214px; height: 156px; }
    #g5a4 { left: 414px; top: 240px; width: 406px; height: 156px; }

    /* b06 — 20 screens, 6 done. Glass on a solid ground. */
    .bigGrid { position: absolute; left: 101px; top: 400px; width: 878px;
               display: flex; flex-wrap: wrap; gap: 26px; }
    .cell { position: relative; display: block; width: 200px; height: 140px;
            background: rgba(255,255,255,0.14);
            -webkit-backdrop-filter: blur(10px); backdrop-filter: blur(10px);
            box-shadow: var(--rim-dark); }
    .cell.fill { box-shadow: var(--rim); }
    .cf { position: absolute; inset: 0; display: block;
          background: var(--lit); }

    .dust { position: absolute; left: 520px; top: 280px;
            width: 28px; height: 28px; border-radius: 50%%;
            background: var(--lit-pink);
            filter: drop-shadow(0 0 20px rgba(255,110,156,0.8)); }
    .strike { position: absolute; left: 320px; top: 288px;
              width: 440px; height: 24px; border-radius: 12px;
              background: var(--lit-pink); rotate: -12deg;
              filter: drop-shadow(0 0 26px rgba(255,110,156,0.5))
                      drop-shadow(0 10px 20px rgba(26,30,39,0.22)); }
    .strike.thin { width: 250px; height: 20px; top: 278px; }
    #g18s1 { left: 255px; }
    #g18s2 { left: 575px; }

    /* ---- phones ---- */
    .phone { position: absolute; left: 380px; top: 15px;
             width: 320px; height: 580px; background: var(--lit-blush);
             overflow: hidden; filter: var(--cast); box-shadow: var(--rim); }
    .phone.fs { top: 40px; }
    .phone.shot { background: #000; }
    .phone.shot img { width: 100%%; height: 100%%; object-fit: cover; }
    .pscr { position: absolute; left: 18px; top: 18px;
            width: 284px; height: 544px; display: block;
            background: var(--lit); padding: 30px 26px;
            box-shadow: inset 0 0 0 1px rgba(180,18,47,0.10); }
    .pscr.on { background: var(--lit-pink); }

    /* b12 — the brainstorm tree */
    #g12svg { position: absolute; left: 100px; top: 70px; overflow: visible; }
    .wire { fill: none; stroke: url(#wireGrad); stroke-width: 19;
            stroke-linecap: round;
            filter: drop-shadow(0 8px 18px rgba(26,30,39,0.22)); }
    .wire.fat { stroke-width: 24; stroke: url(#wireGrad2); }
    .node { fill: #fdf6f6; stroke: #b4122f; stroke-width: 14;
            filter: drop-shadow(0 10px 22px rgba(26,30,39,0.24)); }
    .node.hub { fill: #b4122f; stroke: #fff; }

    /* b13 — telling it what the app is */
    .promptbox { position: absolute; left: 100px; top: 55px;
                 width: 880px; height: 150px; background: var(--lit-blush);
                 filter: var(--cast); box-shadow: var(--rim);
                 padding: 0 46px; font-size: 52px; color: var(--ink);
                 font-weight: 900; display: flex; align-items: center; gap: 8px; }
    .caret { display: inline-block; width: 7px; height: 56px;
             background: var(--accent); }
    .outrow { position: absolute; left: 165px; top: 270px;
              display: flex; gap: 30px; }
    .oscr { display: block; width: 230px; height: 300px; padding: 22px 20px;
            background: var(--lit-blush); filter: var(--cast-sm);
            overflow: hidden; box-shadow: var(--rim); }
    .oscr .ph { height: 44px; border-radius: 14px; margin-bottom: 16px; }
    .oscr .pr { height: 20px; border-radius: 8px; margin-bottom: 12px; }

    /* b14 — comments landing on the canvas */
    .canvas { position: absolute; left: 110px; top: 95px;
              width: 860px; height: 420px; background: var(--lit-blush);
              filter: var(--cast); box-shadow: var(--rim); padding: 46px;
              display: flex; flex-direction: column; gap: 28px; }
    .cblk { display: block; height: 80px; border-radius: 26px;
            background: var(--container); }
    #g14b1 { height: 56px; width: 54%%; background: var(--lit-accent);
             box-shadow: var(--rim-dark); }
    .pin { position: absolute; width: 84px; height: 84px;
           border-radius: 50%% 50%% 50%% 14px; background: var(--lit-accent);
           filter: var(--cast); box-shadow: var(--rim-dark); }
    #g14p1 { left: 830px; top: 120px; }
    #g14p2 { left: 200px; top: 400px; }

    /* b16 — the handoff. The code pane sits under the caption line so her
       white subtitles keep contrast right through the takeover. */
    .btn { position: absolute; left: 340px; top: 700px;
           width: 400px; height: 128px; border-radius: 64px;
           background: var(--lit-accent);
           filter: drop-shadow(0 0 60px rgba(255,110,156,0.4))
                   drop-shadow(0 20px 40px rgba(26,30,39,0.28));
           box-shadow: var(--rim-dark); }
    .codepane { position: absolute; left: 100px; top: 1160px;
                width: 880px; height: 470px; background: var(--lit-ink);
                filter: var(--cast); box-shadow: var(--rim-dark); }
    .cl { position: absolute; left: 56px; display: block;
          height: 24px; border-radius: 12px; background: var(--lit-pink); }
    #g16l1 { top: 54px;  width: 62%%; height: 38px; border-radius: 19px; }
    #g16l2 { top: 112px; width: 44%%; }
    #g16l3 { top: 158px; width: 70%%; }
    #g16l4 { top: 356px; width: 52%%; }
    #g16l5 { top: 402px; width: 34%%; }

    /* b18 / b19 / b23 — rows */
    .pairrow { position: absolute; left: 240px; top: 170px;
               display: flex; gap: 120px; }
    .pairrow .tile.sm { position: relative; top: 0; }
    .triorow { position: absolute; left: 100px; top: 175px; width: 880px;
               display: flex; justify-content: space-between; }
    .slot { position: absolute; width: 400px; height: 220px;
            background: rgba(255,255,255,0.15); overflow: hidden;
            -webkit-backdrop-filter: blur(24px) saturate(1.4);
            backdrop-filter: blur(24px) saturate(1.4);
            filter: var(--cast); box-shadow: var(--rim);
            display: grid; place-items: center; }
    .slot.sq { position: relative; width: 260px; height: 260px; }
    .slot.sq img { width: 200px; height: 200px; border-radius: 46px; }
    .slotfill { position: absolute; inset: 0; background: var(--lit-accent); }
    .slotlogo { position: relative; width: 150px; border-radius: 34px; }
    .slotlogo.wide { width: 290px; border-radius: 0;
                     filter: brightness(0) invert(1); }
    #g19s1 { left: 100px; top: 210px; }
    #g19s2 { left: 580px; top: 210px; }
    .chooser { position: absolute; left: 86px; top: 161px;
               width: 288px; height: 288px; border-radius: 72px;
               box-shadow: inset 0 0 0 14px rgba(255,110,156,0.95);
               filter: drop-shadow(0 0 40px rgba(255,110,156,0.75)); }

    /* b20 — the wall of screens */
    .masonry { position: absolute; left: 79px; top: 300px; width: 922px;
               display: flex; flex-wrap: wrap; gap: 26px;
               align-content: flex-start; justify-content: center; }
    .mt { display: block; width: 290px; padding: 22px 20px;
          background: var(--lit-blush); overflow: hidden;
          filter: var(--cast-sm); box-shadow: var(--rim); }
    .mt .ph { height: 48px; border-radius: 14px; margin-bottom: 16px; }
    .mt .pr { height: 22px; border-radius: 8px; margin-bottom: 12px; }
    .m0 { height: 210px; } .m1 { height: 170px; } .m2 { height: 240px; }
    .m3 { height: 190px; } .m4 { height: 220px; }

    /* b20 — her Mobbin capture, framed on a solid ground */
    .mobframe { position: absolute; left: 230px; top: 150px;
                width: 620px; height: 1102px; overflow: hidden;
                filter: var(--cast); background: #000;
                clip-path: path('M 501.6 0 c 39.495 0 59.243 0 77.009 9.052 a 74 74 0 0 1 32.339 32.339 c 9.052 17.766 9.052 37.513 9.052 77.009 L 620 983.6 c 0 39.495 0 59.243 -9.052 77.009 a 74 74 0 0 1 -32.339 32.339 c -17.766 9.052 -37.513 9.052 -77.009 9.052 L 118.4 1102 c -39.495 0 -59.243 0 -77.009 -9.052 a 74 74 0 0 1 -32.339 -32.339 c -9.052 -17.766 -9.052 -37.513 -9.052 -77.009 L 0 118.4 c 0 -39.495 0 -59.243 9.052 -77.009 a 74 74 0 0 1 32.339 -32.339 c 17.766 -9.052 37.513 -9.052 77.009 -9.052 Z'); }
    .mobframe video { width: 100%%; height: 100%%; object-fit: cover;
                      display: block; }
    /* b21 — Mobbin wired into Claude */
    #g21svg { position: absolute; left: 0; top: 250px; overflow: visible; }
    #g21m, #g21c { width: 300px; height: 300px; }
    #g21m { left: 80px; top: 155px; }
    #g21c { left: 700px; top: 155px; }
    #g21c img { width: 300px; height: 300px; }
    #g21m img { height: 168px; width: auto; }
    .pkt { position: absolute; display: block; width: 62px; height: 62px;
           border-radius: 50%%; background: var(--lit); left: 397px; top: 279px;
           filter: drop-shadow(0 0 26px rgba(255,110,156,0.9)); }

    /* §5a.1 — continuous-curvature corners, Figma smoothing 60%%.
       filter: drop-shadow survives clip-path; box-shadow would not. */
    .tile.big { clip-path: path('M 219.2 0 c 46.967 0 70.451 0 91.578 10.765 a 88 88 0 0 1 38.457 38.457 c 10.765 21.127 10.765 44.611 10.765 91.578 L 360 219.2 c 0 46.967 0 70.451 -10.765 91.578 a 88 88 0 0 1 -38.457 38.457 c -21.127 10.765 -44.611 10.765 -91.578 10.765 L 140.8 360 c -46.967 0 -70.451 0 -91.578 -10.765 a 88 88 0 0 1 -38.457 -38.457 c -10.765 -21.127 -10.765 -44.611 -10.765 -91.578 L 0 140.8 c 0 -46.967 0 -70.451 10.765 -91.578 a 88 88 0 0 1 38.457 -38.457 c 21.127 -10.765 44.611 -10.765 91.578 -10.765 Z'); }
    .tile.merged { clip-path: path('M 267.2 0 c 57.642 0 86.463 0 112.391 13.211 a 108 108 0 0 1 47.198 47.198 c 13.211 25.929 13.211 54.749 13.211 112.391 L 440 267.2 c 0 57.642 0 86.463 -13.211 112.391 a 108 108 0 0 1 -47.198 47.198 c -25.929 13.211 -54.749 13.211 -112.391 13.211 L 172.8 440 c -57.642 0 -86.463 0 -112.391 -13.211 a 108 108 0 0 1 -47.198 -47.198 c -13.211 -25.929 -13.211 -54.749 -13.211 -112.391 L 0 172.8 c 0 -57.642 0 -86.463 13.211 -112.391 a 108 108 0 0 1 47.198 -47.198 c 25.929 -13.211 54.749 -13.211 112.391 -13.211 Z'); }
    .tile.sm { clip-path: path('M 144 0 c 32.023 0 48.035 0 62.439 7.34 a 60 60 0 0 1 26.221 26.221 c 7.34 14.405 7.34 30.416 7.34 62.439 L 240 144 c 0 32.023 0 48.035 -7.34 62.439 a 60 60 0 0 1 -26.221 26.221 c -14.405 7.34 -30.416 7.34 -62.439 7.34 L 96 240 c -32.023 0 -48.035 0 -62.439 -7.34 a 60 60 0 0 1 -26.221 -26.221 c -7.34 -14.405 -7.34 -30.416 -7.34 -62.439 L 0 96 c 0 -32.023 0 -48.035 7.34 -62.439 a 60 60 0 0 1 26.221 -26.221 c 14.405 -7.34 30.416 -7.34 62.439 -7.34 Z'); }
    .cell { clip-path: path('M 145.6 0 c 18.146 0 27.22 0 35.382 4.159 a 34 34 0 0 1 14.859 14.859 c 4.159 8.163 4.159 17.236 4.159 35.382 L 200 85.6 c 0 18.146 0 27.22 -4.159 35.382 a 34 34 0 0 1 -14.859 14.859 c -8.163 4.159 -17.236 4.159 -35.382 4.159 L 54.4 140 c -18.146 0 -27.22 0 -35.382 -4.159 a 34 34 0 0 1 -14.859 -14.859 c -4.159 -8.163 -4.159 -17.236 -4.159 -35.382 L 0 54.4 c 0 -18.146 0 -27.22 4.159 -35.382 a 34 34 0 0 1 14.859 -14.859 c 8.163 -4.159 17.236 -4.159 35.382 -4.159 Z'); }
    .valcard { clip-path: path('M 433.6 0 c 28.821 0 43.231 0 56.196 6.606 a 54 54 0 0 1 23.599 23.599 c 6.606 12.964 6.606 27.375 6.606 56.196 L 520 143.6 c 0 28.821 0 43.231 -6.606 56.196 a 54 54 0 0 1 -23.599 23.599 c -12.964 6.606 -27.375 6.606 -56.196 6.606 L 86.4 230 c -28.821 0 -43.231 0 -56.196 -6.606 a 54 54 0 0 1 -23.599 -23.599 c -6.606 -12.964 -6.606 -27.375 -6.606 -56.196 L 0 86.4 c 0 -28.821 0 -43.231 6.606 -56.196 a 54 54 0 0 1 23.599 -23.599 c 12.964 -6.606 27.375 -6.606 56.196 -6.606 Z'); }
    .workspace { clip-path: path('M 760.8 0 c 33.091 0 49.636 0 64.521 7.584 a 62 62 0 0 1 27.095 27.095 c 7.584 14.885 7.584 31.43 7.584 64.521 L 860 340.8 c 0 33.091 0 49.636 -7.584 64.521 a 62 62 0 0 1 -27.095 27.095 c -14.885 7.584 -31.43 7.584 -64.521 7.584 L 99.2 440 c -33.091 0 -49.636 0 -64.521 -7.584 a 62 62 0 0 1 -27.095 -27.095 c -7.584 -14.885 -7.584 -31.43 -7.584 -64.521 L 0 99.2 c 0 -33.091 0 -49.636 7.584 -64.521 a 62 62 0 0 1 27.095 -27.095 c 14.885 -7.584 31.43 -7.584 64.521 -7.584 Z'); }
    #g5a1 { clip-path: path('M 252 0 c 16.012 0 24.017 0 31.22 3.67 a 30 30 0 0 1 13.11 13.11 c 3.67 7.202 3.67 15.208 3.67 31.22 L 300 120 c 0 16.012 0 24.017 -3.67 31.22 a 30 30 0 0 1 -13.11 13.11 c -7.202 3.67 -15.208 3.67 -31.22 3.67 L 48 168 c -16.012 0 -24.017 0 -31.22 -3.67 a 30 30 0 0 1 -13.11 -13.11 c -3.67 -7.202 -3.67 -15.208 -3.67 -31.22 L 0 48 c 0 -16.012 0 -24.017 3.67 -31.22 a 30 30 0 0 1 13.11 -13.11 c 7.202 -3.67 15.208 -3.67 31.22 -3.67 Z'); }
    #g5a2 { clip-path: path('M 272 0 c 16.012 0 24.017 0 31.22 3.67 a 30 30 0 0 1 13.11 13.11 c 3.67 7.202 3.67 15.208 3.67 31.22 L 320 120 c 0 16.012 0 24.017 -3.67 31.22 a 30 30 0 0 1 -13.11 13.11 c -7.202 3.67 -15.208 3.67 -31.22 3.67 L 48 168 c -16.012 0 -24.017 0 -31.22 -3.67 a 30 30 0 0 1 -13.11 -13.11 c -3.67 -7.202 -3.67 -15.208 -3.67 -31.22 L 0 48 c 0 -16.012 0 -24.017 3.67 -31.22 a 30 30 0 0 1 13.11 -13.11 c 7.202 -3.67 15.208 -3.67 31.22 -3.67 Z'); }
    #g5a3 { clip-path: path('M 169.2 0 c 14.944 0 22.416 0 29.138 3.425 a 28 28 0 0 1 12.236 12.236 c 3.425 6.722 3.425 14.194 3.425 29.138 L 214 111.2 c 0 14.944 0 22.416 -3.425 29.138 a 28 28 0 0 1 -12.236 12.236 c -6.722 3.425 -14.194 3.425 -29.138 3.425 L 44.8 156 c -14.944 0 -22.416 0 -29.138 -3.425 a 28 28 0 0 1 -12.236 -12.236 c -3.425 -6.722 -3.425 -14.194 -3.425 -29.138 L 0 44.8 c 0 -14.944 0 -22.416 3.425 -29.138 a 28 28 0 0 1 12.236 -12.236 c 6.722 -3.425 14.194 -3.425 29.138 -3.425 Z'); }
    #g5a4 { clip-path: path('M 361.2 0 c 14.944 0 22.416 0 29.138 3.425 a 28 28 0 0 1 12.236 12.236 c 3.425 6.722 3.425 14.194 3.425 29.138 L 406 111.2 c 0 14.944 0 22.416 -3.425 29.138 a 28 28 0 0 1 -12.236 12.236 c -6.722 3.425 -14.194 3.425 -29.138 3.425 L 44.8 156 c -14.944 0 -22.416 0 -29.138 -3.425 a 28 28 0 0 1 -12.236 -12.236 c -3.425 -6.722 -3.425 -14.194 -3.425 -29.138 L 0 44.8 c 0 -14.944 0 -22.416 3.425 -29.138 a 28 28 0 0 1 12.236 -12.236 c 6.722 -3.425 14.194 -3.425 29.138 -3.425 Z'); }
    .frame { clip-path: path('M 620.8 0 c 33.091 0 49.636 0 64.521 7.584 a 62 62 0 0 1 27.095 27.095 c 7.584 14.885 7.584 31.43 7.584 64.521 L 720 420.8 c 0 33.091 0 49.636 -7.584 64.521 a 62 62 0 0 1 -27.095 27.095 c -14.885 7.584 -31.43 7.584 -64.521 7.584 L 99.2 520 c -33.091 0 -49.636 0 -64.521 -7.584 a 62 62 0 0 1 -27.095 -27.095 c -7.584 -14.885 -7.584 -31.43 -7.584 -64.521 L 0 99.2 c 0 -33.091 0 -49.636 7.584 -64.521 a 62 62 0 0 1 27.095 -27.095 c 14.885 -7.584 31.43 -7.584 64.521 -7.584 Z'); }
    .promptbox { clip-path: path('M 809.6 0 c 23.484 0 35.225 0 45.789 5.382 a 44 44 0 0 1 19.229 19.229 c 5.382 10.563 5.382 22.305 5.382 45.789 L 880 79.6 c 0 23.484 0 35.225 -5.382 45.789 a 44 44 0 0 1 -19.229 19.229 c -10.563 5.382 -22.305 5.382 -45.789 5.382 L 70.4 150 c -23.484 0 -35.225 0 -45.789 -5.382 a 44 44 0 0 1 -19.229 -19.229 c -5.382 -10.563 -5.382 -22.305 -5.382 -45.789 L 0 70.4 c 0 -23.484 0 -35.225 5.382 -45.789 a 44 44 0 0 1 19.229 -19.229 c 10.563 -5.382 22.305 -5.382 45.789 -5.382 Z'); }
    .oscr { clip-path: path('M 166 0 c 21.349 0 32.023 0 41.626 4.893 a 40 40 0 0 1 17.481 17.481 c 4.893 9.603 4.893 20.278 4.893 41.626 L 230 236 c 0 21.349 0 32.023 -4.893 41.626 a 40 40 0 0 1 -17.481 17.481 c -9.603 4.893 -20.278 4.893 -41.626 4.893 L 64 300 c -21.349 0 -32.023 0 -41.626 -4.893 a 40 40 0 0 1 -17.481 -17.481 c -4.893 -9.603 -4.893 -20.278 -4.893 -41.626 L 0 64 c 0 -21.349 0 -32.023 4.893 -41.626 a 40 40 0 0 1 17.481 -17.481 c 9.603 -4.893 20.278 -4.893 41.626 -4.893 Z'); }
    .canvas { clip-path: path('M 760.8 0 c 33.091 0 49.636 0 64.521 7.584 a 62 62 0 0 1 27.095 27.095 c 7.584 14.885 7.584 31.43 7.584 64.521 L 860 320.8 c 0 33.091 0 49.636 -7.584 64.521 a 62 62 0 0 1 -27.095 27.095 c -14.885 7.584 -31.43 7.584 -64.521 7.584 L 99.2 420 c -33.091 0 -49.636 0 -64.521 -7.584 a 62 62 0 0 1 -27.095 -27.095 c -7.584 -14.885 -7.584 -31.43 -7.584 -64.521 L 0 99.2 c 0 -33.091 0 -49.636 7.584 -64.521 a 62 62 0 0 1 27.095 -27.095 c 14.885 -7.584 31.43 -7.584 64.521 -7.584 Z'); }
    .codepane { clip-path: path('M 780.8 0 c 33.091 0 49.636 0 64.521 7.584 a 62 62 0 0 1 27.095 27.095 c 7.584 14.885 7.584 31.43 7.584 64.521 L 880 370.8 c 0 33.091 0 49.636 -7.584 64.521 a 62 62 0 0 1 -27.095 27.095 c -14.885 7.584 -31.43 7.584 -64.521 7.584 L 99.2 470 c -33.091 0 -49.636 0 -64.521 -7.584 a 62 62 0 0 1 -27.095 -27.095 c -7.584 -14.885 -7.584 -31.43 -7.584 -64.521 L 0 99.2 c 0 -33.091 0 -49.636 7.584 -64.521 a 62 62 0 0 1 27.095 -27.095 c 14.885 -7.584 31.43 -7.584 64.521 -7.584 Z'); }
    .phone { clip-path: path('M 211.2 0 c 36.293 0 54.439 0 70.765 8.318 a 68 68 0 0 1 29.717 29.717 c 8.318 16.325 8.318 34.472 8.318 70.765 L 320 471.2 c 0 36.293 0 54.439 -8.318 70.765 a 68 68 0 0 1 -29.717 29.717 c -16.325 8.318 -34.472 8.318 -70.765 8.318 L 108.8 580 c -36.293 0 -54.439 0 -70.765 -8.318 a 68 68 0 0 1 -29.717 -29.717 c -8.318 -16.325 -8.318 -34.472 -8.318 -70.765 L 0 108.8 c 0 -36.293 0 -54.439 8.318 -70.765 a 68 68 0 0 1 29.717 -29.717 c 16.325 -8.318 34.472 -8.318 70.765 -8.318 Z'); }
    .pscr { clip-path: path('M 200.8 0 c 27.753 0 41.63 0 54.114 6.361 a 52 52 0 0 1 22.725 22.725 c 6.361 12.484 6.361 26.361 6.361 54.114 L 284 460.8 c 0 27.753 0 41.63 -6.361 54.114 a 52 52 0 0 1 -22.725 22.725 c -12.484 6.361 -26.361 6.361 -54.114 6.361 L 83.2 544 c -27.753 0 -41.63 0 -54.114 -6.361 a 52 52 0 0 1 -22.725 -22.725 c -6.361 -12.484 -6.361 -26.361 -6.361 -54.114 L 0 83.2 c 0 -27.753 0 -41.63 6.361 -54.114 a 52 52 0 0 1 22.725 -22.725 c 12.484 -6.361 26.361 -6.361 54.114 -6.361 Z'); }
    .slot { clip-path: path('M 316.8 0 c 27.753 0 41.63 0 54.114 6.361 a 52 52 0 0 1 22.725 22.725 c 6.361 12.484 6.361 26.361 6.361 54.114 L 400 136.8 c 0 27.753 0 41.63 -6.361 54.114 a 52 52 0 0 1 -22.725 22.725 c -12.484 6.361 -26.361 6.361 -54.114 6.361 L 83.2 220 c -27.753 0 -41.63 0 -54.114 -6.361 a 52 52 0 0 1 -22.725 -22.725 c -6.361 -12.484 -6.361 -26.361 -6.361 -54.114 L 0 83.2 c 0 -27.753 0 -41.63 6.361 -54.114 a 52 52 0 0 1 22.725 -22.725 c 12.484 -6.361 26.361 -6.361 54.114 -6.361 Z'); }
    .slot.sq { clip-path: path('M 164 0 c 32.023 0 48.035 0 62.439 7.34 a 60 60 0 0 1 26.221 26.221 c 7.34 14.405 7.34 30.416 7.34 62.439 L 260 164 c 0 32.023 0 48.035 -7.34 62.439 a 60 60 0 0 1 -26.221 26.221 c -14.405 7.34 -30.416 7.34 -62.439 7.34 L 96 260 c -32.023 0 -48.035 0 -62.439 -7.34 a 60 60 0 0 1 -26.221 -26.221 c -7.34 -14.405 -7.34 -30.416 -7.34 -62.439 L 0 96 c 0 -32.023 0 -48.035 7.34 -62.439 a 60 60 0 0 1 26.221 -26.221 c 14.405 -7.34 30.416 -7.34 62.439 -7.34 Z'); }
    .mt.m0 { clip-path: path('M 219.6 0 c 23.484 0 35.225 0 45.789 5.382 a 44 44 0 0 1 19.229 19.229 c 5.382 10.563 5.382 22.305 5.382 45.789 L 290 139.6 c 0 23.484 0 35.225 -5.382 45.789 a 44 44 0 0 1 -19.229 19.229 c -10.563 5.382 -22.305 5.382 -45.789 5.382 L 70.4 210 c -23.484 0 -35.225 0 -45.789 -5.382 a 44 44 0 0 1 -19.229 -19.229 c -5.382 -10.563 -5.382 -22.305 -5.382 -45.789 L 0 70.4 c 0 -23.484 0 -35.225 5.382 -45.789 a 44 44 0 0 1 19.229 -19.229 c 10.563 -5.382 22.305 -5.382 45.789 -5.382 Z'); }
    .mt.m1 { clip-path: path('M 226 0 c 21.349 0 32.023 0 41.626 4.893 a 40 40 0 0 1 17.481 17.481 c 4.893 9.603 4.893 20.278 4.893 41.626 L 290 106 c 0 21.349 0 32.023 -4.893 41.626 a 40 40 0 0 1 -17.481 17.481 c -9.603 4.893 -20.278 4.893 -41.626 4.893 L 64 170 c -21.349 0 -32.023 0 -41.626 -4.893 a 40 40 0 0 1 -17.481 -17.481 c -4.893 -9.603 -4.893 -20.278 -4.893 -41.626 L 0 64 c 0 -21.349 0 -32.023 4.893 -41.626 a 40 40 0 0 1 17.481 -17.481 c 9.603 -4.893 20.278 -4.893 41.626 -4.893 Z'); }
    .mt.m2 { clip-path: path('M 216.4 0 c 24.551 0 36.827 0 47.87 5.627 a 46 46 0 0 1 20.103 20.103 c 5.627 11.044 5.627 23.319 5.627 47.87 L 290 166.4 c 0 24.551 0 36.827 -5.627 47.87 a 46 46 0 0 1 -20.103 20.103 c -11.044 5.627 -23.319 5.627 -47.87 5.627 L 73.6 240 c -24.551 0 -36.827 0 -47.87 -5.627 a 46 46 0 0 1 -20.103 -20.103 c -5.627 -11.044 -5.627 -23.319 -5.627 -47.87 L 0 73.6 c 0 -24.551 0 -36.827 5.627 -47.87 a 46 46 0 0 1 20.103 -20.103 c 11.044 -5.627 23.319 -5.627 47.87 -5.627 Z'); }
    .mt.m3 { clip-path: path('M 222.8 0 c 22.416 0 33.624 0 43.708 5.138 a 42 42 0 0 1 18.355 18.355 c 5.138 10.083 5.138 21.291 5.138 43.708 L 290 122.8 c 0 22.416 0 33.624 -5.138 43.708 a 42 42 0 0 1 -18.355 18.355 c -10.083 5.138 -21.291 5.138 -43.708 5.138 L 67.2 190 c -22.416 0 -33.624 0 -43.708 -5.138 a 42 42 0 0 1 -18.355 -18.355 c -5.138 -10.083 -5.138 -21.291 -5.138 -43.708 L 0 67.2 c 0 -22.416 0 -33.624 5.138 -43.708 a 42 42 0 0 1 18.355 -18.355 c 10.083 -5.138 21.291 -5.138 43.708 -5.138 Z'); }
    .mt.m4 { clip-path: path('M 219.6 0 c 23.484 0 35.225 0 45.789 5.382 a 44 44 0 0 1 19.229 19.229 c 5.382 10.563 5.382 22.305 5.382 45.789 L 290 149.6 c 0 23.484 0 35.225 -5.382 45.789 a 44 44 0 0 1 -19.229 19.229 c -10.563 5.382 -22.305 5.382 -45.789 5.382 L 70.4 220 c -23.484 0 -35.225 0 -45.789 -5.382 a 44 44 0 0 1 -19.229 -19.229 c -5.382 -10.563 -5.382 -22.305 -5.382 -45.789 L 0 70.4 c 0 -23.484 0 -35.225 5.382 -45.789 a 44 44 0 0 1 19.229 -19.229 c 10.563 -5.382 22.305 -5.382 45.789 -5.382 Z'); }
    #g21m { clip-path: path('M 181.6 0 c 39.495 0 59.243 0 77.009 9.052 a 74 74 0 0 1 32.339 32.339 c 9.052 17.766 9.052 37.513 9.052 77.009 L 300 181.6 c 0 39.495 0 59.243 -9.052 77.009 a 74 74 0 0 1 -32.339 32.339 c -17.766 9.052 -37.513 9.052 -77.009 9.052 L 118.4 300 c -39.495 0 -59.243 0 -77.009 -9.052 a 74 74 0 0 1 -32.339 -32.339 c -9.052 -17.766 -9.052 -37.513 -9.052 -77.009 L 0 118.4 c 0 -39.495 0 -59.243 9.052 -77.009 a 74 74 0 0 1 32.339 -32.339 c 17.766 -9.052 37.513 -9.052 77.009 -9.052 Z'); }
    #g21c { clip-path: path('M 181.6 0 c 39.495 0 59.243 0 77.009 9.052 a 74 74 0 0 1 32.339 32.339 c 9.052 17.766 9.052 37.513 9.052 77.009 L 300 181.6 c 0 39.495 0 59.243 -9.052 77.009 a 74 74 0 0 1 -32.339 32.339 c -17.766 9.052 -37.513 9.052 -77.009 9.052 L 118.4 300 c -39.495 0 -59.243 0 -77.009 -9.052 a 74 74 0 0 1 -32.339 -32.339 c -9.052 -17.766 -9.052 -37.513 -9.052 -77.009 L 0 118.4 c 0 -39.495 0 -59.243 9.052 -77.009 a 74 74 0 0 1 32.339 -32.339 c 17.766 -9.052 37.513 -9.052 77.009 -9.052 Z'); }
    .pips.big .pip { clip-path: path('M 85 0 c 16.012 0 24.017 0 31.22 3.67 a 30 30 0 0 1 13.11 13.11 c 3.67 7.202 3.67 15.208 3.67 31.22 L 130 45 c 0 16.012 0 24.017 -3.67 31.22 a 30 30 0 0 1 -13.11 13.11 c -7.202 3.67 -15.208 3.67 -31.22 3.67 L 45 90 c -16.012 0 -24.017 0 -31.22 -3.67 a 30 30 0 0 1 -13.11 -13.11 c -3.67 -7.202 -3.67 -15.208 -3.67 -31.22 L 0 45 c 0 -16.012 0 -24.017 3.67 -31.22 a 30 30 0 0 1 13.11 -13.11 c 7.202 -3.67 15.208 -3.67 31.22 -3.67 Z'); }
""" % {"W": W, "H": H, "RED": RED, "RED_DEEP": RED_DEEP, "PINK": PINK,
       "INK": INK, "PAPER": PAPER, "CAP_SIZE": CAP_SIZE,
       "CAP_TOP": CAP_Y - CAP_SIZE // 2 - 14, "CAP_H": CAP_SIZE + 28,
       "SCRIM_TOP": CAP_Y - 225, "GFX_TOP": GFX_TOP, "GFX_H": GFX_BOT - GFX_TOP}


def main():
    caps = load_captions()
    gh, gj = [], []
    for fn in BEATS:
        h, j = fn()
        gh.append(h.rstrip())
        gj.append("  /* %s */" % fn.__name__)
        gj.append(j.rstrip())

    doc = '''<!DOCTYPE html>
<html lang="uk">
  <head>
    <meta charset="utf-8">
    <title>Reel 3 — дизайн без Фігми</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
    <style>%(css)s
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0"
         data-width="%(W)d" data-height="%(H)d" data-duration="%(DUR).3f" data-fps="%(FPS)d">

      <video id="vid" class="plate" src="assets/base.mp4"
             data-start="0" data-duration="%(DUR).3f" data-media-start="0"
             muted playsinline></video>
%(gfx)s

      <div id="scrim"></div>
      %(caps)s

      <audio id="vo" src="assets/base.mp4"
             data-start="0" data-duration="%(DUR).3f" data-media-start="0"></audio>
    </div>

    <script>
      function build() {
        var tl = gsap.timeline({paused: true});

%(capjs)s

%(gfxjs)s

        window.__timelines["main"] = tl;
      }
      if (document.fonts && document.fonts.ready) document.fonts.ready.then(build);
      else build();
    </script>
  </body>
</html>
''' % {"css": CSS, "W": W, "H": H, "DUR": DUR, "FPS": FPS,
       "gfx": "\n".join(gh), "caps": caption_html(caps),
       "capjs": caption_js(caps), "gfxjs": "\n".join(gj)}

    out = os.path.join(HERE, "index.html")
    io.open(out, "w", encoding="utf-8").write(doc)
    print("index.html  %d captions, %d beats, %.1f KB"
          % (len(caps), len(BEATS), os.path.getsize(out) / 1024.0))


main()
