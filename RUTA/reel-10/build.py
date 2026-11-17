# -*- coding: utf-8 -*-
"""Reel 10 — «кожна консультація — це і є твоє джерело контенту».

Variant B: her cut, graded, no subtitles. Materials from tools/kit.py
(STYLE.md §5a); what each beat depicts is invented for this script.

The recurring object is **the client's own sentence**. The argument of the
script is not "record your calls", it is "the words your client already used
are the words your content should use" — so the object is a speech bubble that
comes out of the client, gets lifted out of the call, and ends up as the line
on a finished piece. It appears in the second beat and is the last thing on
screen before the CTA (STYLE.md §4, reuse objects).

Reel 7 had one beat on the same idea («один дзвінок — це вже ідеї для
контенту»). Here it is the whole reel, and the treatment is deliberately
different: there the object was the call, here it is the sentence inside it.

usage: python build.py
"""
import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
from kit import Kit  # noqa: E402

DUR = 81.917           # 2458 plate frames / 30, rounded down
k = Kit(width=1080, height=1920, fps=30, duration=DUR)

BEATS = []


def beat(fn):
    BEATS.append(fn)
    return fn


# ---------------------------------------------------------------------------
# NO-PAINT ZONE — her own editing (STYLE.md §4a).
#
# tools/shots.py found 4 shots; one is a 0.73 s cutaway to a completely
# different place — a balcony, different top, a phone on a tripod — dropped in
# under «перетворити на контент». It is B-roll of her actually making the
# thing she is describing, and it is the whole joke. tools/pullouts.py found no
# zooms.
NO_PAINT = [(32.00, 32.95)]


# ---------------------------------------------------------------- materials

def mark(name):
    return '<img class="mk" src="assets/logos/%s.png" alt="">' % name


def marktile(tid, name, cls="", style=""):
    return ('<div class="tile brand prod %s" id="%s"%s>%s</div>'
            % (cls, tid, (' style="%s"' % style) if style else "", mark(name)))


def bubble(bid, cls="", rows=2, style=""):
    """The client's sentence. Two ragged lines, a tail, and the accent colour
    that marks it as hers rather than yours."""
    body = "".join('<b></b>' for _ in range(rows))
    return ('<div class="bub %s" id="%s"%s>%s<span class="tail"></span></div>'
            % (cls, bid, (' style="%s"' % style) if style else "", body))


def card(cid, cls="", style=""):
    return ('<div class="cc %s" id="%s"%s><b></b><b></b><b></b></div>'
            % (cls, cid, (' style="%s"' % style) if style else ""))


k.css("""
    /* ---- the client's sentence, which is the object of the whole reel ---- */
    .bub { position: absolute; width: 520px; padding: 32px 36px;
           background: var(--lit-blush); box-shadow: var(--rim);
           filter: var(--cast); border-radius: 44px; }
    .bub b { display: block; height: 26px; border-radius: 13px;
             background: var(--graphite); margin-bottom: 18px; }
    .bub b:last-child { margin-bottom: 0; width: 64%; }
    .bub .tail { position: absolute; left: 46px; bottom: -22px; width: 0;
                 height: 0; border-left: 30px solid transparent;
                 border-right: 0 solid transparent;
                 border-top: 30px solid var(--surface); }
    /* hers — the one that matters, in the accent */
    .bub.client { background: var(--lit-accent); box-shadow: var(--rim-dark); }
    .bub.client b { background: rgba(255,255,255,0.90); }
    .bub.client .tail { border-top-color: #a81030; }
    /* yours — the reply, quieter */
    .bub.mine { background: var(--lit); }
    .bub.mine .tail { left: auto; right: 46px;
                      border-left: 0 solid transparent;
                      border-right: 30px solid transparent;
                      border-top-color: #fafafb; }

    /* ---- a finished piece of content ---- */
    .cc { position: absolute; width: 210px; height: 300px; padding: 24px;
          background: var(--lit-blush); box-shadow: var(--rim);
          filter: var(--cast); }
    .cc b { display: block; height: 15px; border-radius: 8px;
            background: var(--graphite); margin-bottom: 13px; }
    .cc b:first-child { height: 26px; width: 74%; background: var(--lit-accent); }
    .cc.quoted b:first-child { background: var(--lit-pink); }

    /* ---- product tiles ---- */
    .tile.brand.prod { position: absolute; width: 260px; height: 260px;
                       display: grid; place-items: center;
                       background: var(--lit-blush); }
    .tile.brand.prod .mk { width: 62%; height: auto; max-height: 64%;
                           object-fit: contain; display: block; }
    .tile.brand.prod.wide { width: 360px; height: 220px; }

    /* ---- numbers ---- */
    .big { position: absolute; left: 0; width: 1080px; text-align: center;
           font-weight: 900; color: #fff; letter-spacing: -0.05em;
           line-height: 1; text-shadow: 0 18px 60px rgba(8,6,12,0.55); }
    .big small { font-size: 0.42em; }

    /* ---- «безкоштовний» — the 0, third reel running ---- */
    .freewrap { position: absolute; left: 640px; top: 150px; width: 230px;
                height: 230px; }
    .free { position: absolute; inset: 0; display: grid; place-items: center;
            grid-auto-flow: column; gap: 4px; border-radius: 50%;
            background: var(--lit-accent); box-shadow: var(--rim-dark); }
    .free span { font-size: 130px; font-weight: 900; color: #fff;
                 letter-spacing: -0.06em; line-height: 1; }
    .free small { font-size: 58px; font-weight: 900; color: #fff; }

    /* ---- a calendar of content, every day ---- */
    .cal { position: absolute; left: 190px; top: 90px; width: 700px;
           display: grid; gap: 14px; grid-template-columns: repeat(7, 1fr); }
    .cal i { display: block; height: 86px; border-radius: 22px;
             background: rgba(255,255,255,0.55); box-shadow: var(--rim); }
    .cal i.on { background: var(--lit-accent); box-shadow: var(--rim-dark); }

    /* ---- the transcript the recorder leaves behind ---- */
    .wave { position: absolute; display: flex; align-items: center; gap: 10px; }
    .wave i { display: block; width: 14px; border-radius: 7px;
              background: var(--pink); }
    .lines { position: absolute; }
    .lines b { display: block; height: 22px; border-radius: 11px;
               background: rgba(255,255,255,0.90); margin-bottom: 16px;
               box-shadow: var(--rim); }
    .lines b:nth-child(2) { width: 88%; }
    .lines b:nth-child(3) { width: 62%; }

    /* ---- the word she wants typed. It is an instruction the viewer has to
           follow exactly, so it is the one place the word itself is the
           content (STYLE.md §4a.2). ---- */
    .word { position: absolute; left: 190px; top: 210px; width: 700px;
            height: 150px; display: grid; place-items: center;
            background: var(--lit-accent); box-shadow: var(--rim-dark);
            filter: var(--cast); }
    .word span { font-size: 88px; font-weight: 900; color: #fff;
                 letter-spacing: -0.03em; }
""")

for _sel, _w, _h, _r in [
    (".tile.brand.prod", 260, 260, 62),
    (".tile.brand.prod.wide", 360, 220, 54),
    (".cc", 210, 300, 34),
    (".word", 700, 150, 50),
]:
    k.squircle(_sel, _w, _h, _r)


k.css("""
    /* ---- TK1: the raw transcript, deliberately unloved ----
       This is reel 10's bare state. It must look like an export and nothing
       else: no radius, no card, no colour until the one line lights up. */
    .tr { position: absolute; left: 80px; width: 920px; height: 150px; }
    .tr b { position: absolute; top: 0; font-weight: 500; font-size: 30px; }
    .tr b.ts { left: 0; color: rgba(23,20,28,0.38); letter-spacing: 0.02em; }
    .tr b.sp { left: 150px; color: rgba(23,20,28,0.55); letter-spacing: 0.14em; }
    .tr i { position: absolute; left: 150px; height: 14px; border-radius: 4px;
            background: rgba(23,20,28,0.22); transform-origin: 0%% 50%%; }
    .qhl { position: absolute; border-radius: 10px;
           background: rgba(255,110,156,0.32); transform-origin: 0%% 50%%; }
    .qt { position: absolute; font-weight: 900; color: var(--accent);
          letter-spacing: -0.02em; white-space: nowrap; }

    /* ---- M1: what she said, what you said, what she paid ---- */
    .bub { position: absolute; overflow: hidden; border-radius: 48px;
           background: var(--lit); box-shadow: var(--rim); filter: var(--cast); }
    .bub.cl { background: var(--lit-blush); }
    .bub i { position: absolute; left: 46px; height: 16px; border-radius: 5px;
             background: rgba(23,20,28,0.24); transform-origin: 0%% 50%%; }
    .eur { position: absolute; display: grid; place-items: center;
           width: 264px; height: 112px; border-radius: 999px;
           background: var(--lit-accent); color: #fff; font-weight: 900;
           font-size: 56px; box-shadow: var(--rim-dark); filter: var(--cast); }

    /* ---- TK2: the system, top to bottom ---- */
    .wv { position: absolute; display: flex; align-items: center; gap: 14px; }
    .wv i { display: block; flex: 1; border-radius: 7px;
            background: var(--lit-accent); transform-origin: 50%% 50%%; }
    .fm { position: absolute; object-fit: contain; }
    /* Ink on pink, not white: white on --lit-pink measures 2.47:1 and the
       contrast check wants 3:1. A pink chip with dark type also reads better
       against the paper than another red pill would. */
    .zero { position: absolute; display: grid; place-items: center;
            width: 190px; height: 96px; border-radius: 999px;
            background: var(--lit-pink); color: var(--ink); font-weight: 900;
            font-size: 46px; box-shadow: var(--rim-dark); }
    .txb { position: absolute; background: var(--lit); border-radius: 26px;
           box-shadow: var(--rim); filter: var(--cast-sm); overflow: hidden; }
    .txb i { position: absolute; left: 34px; height: 12px; border-radius: 4px;
             background: rgba(23,20,28,0.22); transform-origin: 0%% 50%%; }

    /* ---- TK3: the same sentence, dressed ---- */
    .qcard { position: absolute; overflow: hidden; border-radius: 40px;
             background: var(--lit-blush); box-shadow: var(--rim);
             filter: var(--cast); }
    .qcard .big2 { position: absolute; left: 54px; font-weight: 900;
                   color: var(--accent); letter-spacing: -0.02em; }
""")


QUOTE = 'я не розумію, з чого почати'

ENTRIES = '<div class="tr" id="g3e0" style="top:350px"><b class="ts">00:14</b><b class="sp">КЛІЄНТКА</b><i style="top:64px;width:640px"></i><i style="top:98px;width:520px"></i></div>\n        <div class="tr" id="g3e1" style="top:525px"><b class="ts">01:02</b><b class="sp">ТИ</b><i style="top:64px;width:700px"></i><i style="top:98px;width:430px"></i></div>\n        <div class="tr" id="g3e2" style="top:700px"><b class="ts">02:47</b><b class="sp">КЛІЄНТКА</b><i style="top:64px;width:560px"></i><i style="top:98px;width:610px"></i></div>\n        <div class="tr" id="g3e3" style="top:875px"><b class="ts">03:19</b><b class="sp">КЛІЄНТКА</b><i style="top:64px;width:690px"></i><i style="top:98px;width:500px"></i></div>\n        <div class="tr" id="g3e4" style="top:1050px"><b class="ts">04:05</b><b class="sp">ТИ</b><i style="top:64px;width:600px"></i><i style="top:98px;width:540px"></i></div>\n        <div class="tr" id="g3e5" style="top:1225px"><b class="ts">05:31</b><b class="sp">КЛІЄНТКА</b><i style="top:64px;width:660px"></i><i style="top:98px;width:470px"></i></div>'

WAVE = '<i style="height:38px"></i><i style="height:88px"></i><i style="height:140px"></i><i style="height:66px"></i><i style="height:176px"></i><i style="height:44px"></i><i style="height:120px"></i><i style="height:92px"></i><i style="height:158px"></i><i style="height:58px"></i><i style="height:104px"></i><i style="height:72px"></i>'

TXR = '<i style="top:44px;width:690px"></i><i style="top:84px;width:620px"></i><i style="top:124px;width:660px"></i><i style="top:164px;width:540px"></i>'

ANGLES = [('g9a', -140, 160, 520, 330, -6.0, 57.2), ('g9b', 700, 230, 500, 320, 5.0, 58.4), ('g9c', -120, 640, 480, 310, 4.0, 59.48), ('g9d', 720, 700, 470, 300, -5.0, 60.68)]


# ------------------------------------------------------------------ A · hook


@beat
def b00_expert_and_blogger():
    """«таку імбу покажу… якщо ти експертка і блогерка одночасно»

    Added after tools/review.py found 7.5 s of nothing at the top. Two roles
    arrive separately and then sit on top of each other, because «одночасно» is
    the condition the whole reel depends on.
    """
    html = '''
      <div class="g full" id="g0">
        <div class="burst" id="g0b"></div>
        <div class="role" id="g0e" style="left:150px;top:200px"><i></i><b></b></div>
        <div class="role alt" id="g0g" style="left:610px;top:200px"><i></i><b></b></div>
      </div>'''
    js = '''
  gsap.set("#g0", {autoAlpha: 0});
  gsap.set("#g0b", {autoAlpha: 0, scale: 0.2, transformOrigin: "50% 50%"});
  gsap.set("#g0e, #g0g", {autoAlpha: 0, scale: 0.7,
                          transformOrigin: "50% 50%"});
  tl.set("#g0", {autoAlpha: 1}, 1.90);
  // «таку імбу покажу» — something lands
  tl.to("#g0b", {autoAlpha: 1, scale: 1, duration: 0.34, ease: "back.out(2.8)"}, 2.02);
  tl.to("#g0b", {autoAlpha: 0, scale: 1.5, duration: 0.34,
                 ease: "power2.out"}, 2.60);
  // «експертка»
  tl.to("#g0e", {autoAlpha: 1, scale: 1, duration: 0.30, ease: "back.out(2.4)"}, 3.74);
  // «і блогерка»
  tl.to("#g0g", {autoAlpha: 1, scale: 1, duration: 0.30, ease: "back.out(2.4)"}, 4.18);
  // «одночасно» — and they are the same person
  tl.to("#g0e", {x: 160, duration: 0.44, ease: "power2.inOut"}, 4.60);
  tl.to("#g0g", {x: -160, duration: 0.44, ease: "power2.inOut"}, 4.60);
  tl.to("#g0g", {autoAlpha: 0.55, duration: 0.30}, 4.90);
  tl.to("#g0", {autoAlpha: 0, duration: 0.26, ease: "power2.in"}, 6.30);'''
    return html, js


@beat
def b01_content_every_day():
    """«якщо ти експертка і блогерка одночасно, то в тебе є геніальний спосіб
    мати легкий контент хоч кожен день»

    A week of days, and every one of them fills. The claim is frequency, so
    the picture is frequency.
    """
    html = '''
      <div class="g full" id="g1">
        <div class="cal" id="g1c">%s</div>
      </div>''' % "".join('<i id="g1d%d"></i>' % i for i in range(14))
    js = '''
  gsap.set("#g1", {autoAlpha: 0});
  gsap.set("#g1c i", {autoAlpha: 0, scale: 0.6, transformOrigin: "50% 50%"});
  tl.set("#g1", {autoAlpha: 1}, 7.56);
  // «легкий контент»
  tl.to("#g1c i", {autoAlpha: 1, scale: 1, duration: 0.26, ease: "back.out(2)",
                   stagger: 0.022}, 7.70);
  // «хоч кожен день» — and every single one of them lights
  tl.to("#g1c i", {backgroundImage:
        "linear-gradient(115deg, #c41434 0%, #8d0d24 100%)",
        duration: 0.20, stagger: 0.018}, 9.10);
  tl.to("#g1", {autoAlpha: 0, duration: 0.24, ease: "power2.in"}, 9.62);'''
    return html, js


@beat
def b02_call_is_the_source():
    """«кожна консультація — це і є твоє джерело контенту»

    A call, and content coming straight out of it. The pipe of the whole reel,
    stated once and plainly before it is taken apart.
    """
    html = '''
      <div class="g full" id="g2">
        <div class="tile brand prod wide" id="g2call" style="left:80px;top:180px">
          <div class="wave" id="g2w" style="position:relative;height:90px">%s</div>
        </div>
        %s
        %s
      </div>''' % (
        "".join('<i style="height:%dpx"></i>' % h
                for h in [26, 58, 90, 44, 76, 34, 66, 48, 84, 30]),
        card("g2c0", style="left:560px;top:150px"),
        card("g2c1", style="left:800px;top:180px"))
    js = '''
  gsap.set("#g2", {autoAlpha: 0});
  gsap.set("#g2call", {autoAlpha: 0, scale: 0.8, transformOrigin: "50% 50%"});
  gsap.set("#g2c0, #g2c1", {autoAlpha: 0, scale: 0.7, x: -180,
                            transformOrigin: "50% 50%"});
  tl.set("#g2", {autoAlpha: 1}, 9.80);
  tl.to("#g2call", {autoAlpha: 1, scale: 1, duration: 0.30, ease: "back.out(2.4)"}, 9.92);
  // «це і є твоє джерело контенту» — it comes out of the call, not from you
  tl.to("#g2c0", {autoAlpha: 1, scale: 1, x: 0, duration: 0.34,
                  ease: "back.out(2.2)"}, 11.78);
  tl.to("#g2c1", {autoAlpha: 1, scale: 1, x: 0, duration: 0.34,
                  ease: "back.out(2.2)"}, 11.98);
  tl.to("#g2", {autoAlpha: 0, duration: 0.26, ease: "power2.in"}, 13.40);'''
    return html, js


@beat
def b03_not_topic_but_words():
    """«це не просто тема… це ще й ТЕКСТ саме так, як говорить твоя цільова
    аудиторія»

    Takeover 1, and reel 10's bare state. A raw call transcript on ruled
    paper: timestamps, speaker labels, grey rules where the words would be.
    Deliberately unloved — no card, no radius, no colour — because the whole
    reel turns on seeing this same sentence dressed at 50s.

    On «текст» the fourth entry stops being rules and becomes the client's
    actual line. That is the object of the reel arriving, and STYLE.md 4a.2
    says to write the word when the image alone would not read.
    """
    html = '''
      <div class="g full" id="g3">
        <div class="tk paper"></div><div class="gl"></div>
        %s
        <div class="qhl" id="g3hl" style="left:222px;top:%dpx;width:768px;height:74px"></div>
        <div class="qt" id="g3q" style="left:232px;top:%dpx;font-size:46px">%s</div>
      </div>''' % ("""<div class="tr" id="g3e0" style="top:350px"><b class="ts">00:14</b><b class="sp">КЛІЄНТКА</b><i style="top:64px;width:640px"></i><i style="top:98px;width:520px"></i></div>
        <div class="tr" id="g3e1" style="top:525px"><b class="ts">01:02</b><b class="sp">ТИ</b><i style="top:64px;width:700px"></i><i style="top:98px;width:430px"></i></div>
        <div class="tr" id="g3e2" style="top:700px"><b class="ts">02:47</b><b class="sp">КЛІЄНТКА</b><i style="top:64px;width:560px"></i><i style="top:98px;width:610px"></i></div>
        <div class="tr" id="g3e3" style="top:875px"><b class="ts">03:19</b><b class="sp">КЛІЄНТКА</b><i style="top:64px;width:690px"></i><i style="top:98px;width:500px"></i></div>
        <div class="tr" id="g3e4" style="top:1050px"><b class="ts">04:05</b><b class="sp">ТИ</b><i style="top:64px;width:600px"></i><i style="top:98px;width:540px"></i></div>
        <div class="tr" id="g3e5" style="top:1225px"><b class="ts">05:31</b><b class="sp">КЛІЄНТКА</b><i style="top:64px;width:660px"></i><i style="top:98px;width:470px"></i></div>""", 350 + 3 * 175 + 52, 350 + 3 * 175 + 58, QUOTE)
    js = '''
  gsap.set("#g3", {autoAlpha: 0});
  gsap.set("#g3 .tr b", {autoAlpha: 0});
  gsap.set("#g3 .tr i", {scaleX: 0});
  gsap.set("#g3hl", {scaleX: 0});
  gsap.set("#g3q", {autoAlpha: 0, y: 14});
  tl.set("#g3", {autoAlpha: 1}, 13.70);
  // «тема, з якою до тебе звертаються люди» — the export writes itself out
  tl.to("#g3 .tr b", {autoAlpha: 1, duration: 0.18, stagger: 0.082}, 13.84);
  tl.to("#g3 .tr i", {scaleX: 1, duration: 0.22, ease: "power2.out",
                      stagger: 0.041}, 13.96);
  // «текст» — and the one line that matters stops being a grey rule
  tl.to("#g3e3 i", {autoAlpha: 0, duration: 0.16}, 16.40);
  tl.to("#g3hl", {scaleX: 1, duration: 0.30, ease: "power3.out"}, 16.42);
  tl.to("#g3q", {autoAlpha: 1, y: 0, duration: 0.26, ease: "power2.out"}, 16.54);
  // «саме так, як говорить твоя цільова аудиторія»
  tl.to("#g3hl", {scaleY: 1.06, duration: 0.24, ease: "power2.out",
                  transformOrigin: "50%% 50%%"}, 17.50);
  tl.to("#g3", {autoAlpha: 0, duration: 0.26, ease: "power2.in"}, 19.95);'''
    return html, js


@beat
def b04_she_said_you_replied():
    """«клієнтка вже сказала тобі щось, ти якось відповіла, і вона за це
    заплатила гроші»

    Matted. Two bubbles arrive from opposite sides *behind* her, and the fee
    lands on the client's one — the money attaches to what she said, which is
    the argument of the beat.
    """
    html = '''
      <div class="g full" id="g4">
        <div class="bub cl" id="g4a" style="left:-70px;top:190px;width:640px;height:268px">
          <i style="top:76px;width:470px"></i><i style="top:124px;width:404px"></i>
          <i style="top:172px;width:300px"></i>
        </div>
        <div class="bub" id="g4b" style="left:500px;top:556px;width:640px;height:250px">
          <i style="top:70px;width:420px"></i><i style="top:118px;width:362px"></i>
          <i style="top:166px;width:250px"></i>
        </div>
        <div class="eur" id="g4e" style="left:352px;top:392px">250 €</div>
      </div>'''
    js = '''
  gsap.set("#g4", {autoAlpha: 0});
  gsap.set("#g4a", {autoAlpha: 0, x: -440, transformOrigin: "50%% 50%%"});
  gsap.set("#g4b", {autoAlpha: 0, x: 440, transformOrigin: "50%% 50%%"});
  gsap.set("#g4 .bub i", {scaleX: 0});
  gsap.set("#g4e", {autoAlpha: 0, scale: 1.7, rotation: -12,
                    transformOrigin: "50%% 50%%"});
  tl.set("#g4", {autoAlpha: 1}, 22.95);
  // «клієнтка вже сказала тобі щось»
  tl.to("#g4a", {autoAlpha: 1, x: 0, duration: 0.46, ease: "back.out(1.6)"}, 23.02);
  tl.to("#g4a i", {scaleX: 1, duration: 0.22, ease: "power2.out",
                   stagger: 0.07}, 23.40);
  // «ти якось відповіла»
  tl.to("#g4b", {autoAlpha: 1, x: 0, duration: 0.46, ease: "back.out(1.6)"}, 25.14);
  tl.to("#g4b i", {scaleX: 1, duration: 0.22, ease: "power2.out",
                   stagger: 0.07}, 25.52);
  // «заплатила гроші» — it lands on her sentence, not between them
  tl.to("#g4e", {autoAlpha: 1, scale: 1, rotation: -6, duration: 0.34,
                 ease: "back.out(2.6)"}, 27.12);
  tl.to("#g4", {autoAlpha: 0, duration: 0.28, ease: "power2.in"}, 28.96);'''
    return html, js


# Two bubbles and a fee, behind her (STYLE.md 1). 191 frames.
k.matte("saidpaid", 22.933, 6.400)


@beat
def b05_lift_it_out():
    """«лишилось тільки забрати це і перетворити на контент»

    Her sentence lifts out of the conversation and lands as the headline of a
    finished piece — the move the whole reel is selling, done once, plainly.
    Clears before 32.00: the balcony cutaway is hers.
    """
    html = '''
      <div class="g full" id="g5">
        %s
        %s
      </div>''' % (
        bubble("g5b", "client", rows=2, style="left:280px;top:110px"),
        card("g5c", "quoted", style="left:435px;top:300px"))
    js = '''
  gsap.set("#g5", {autoAlpha: 0});
  gsap.set("#g5b", {autoAlpha: 0, scale: 0.86, transformOrigin: "50% 50%"});
  gsap.set("#g5c", {autoAlpha: 0, scale: 0.7, transformOrigin: "50% 0%"});
  tl.set("#g5", {autoAlpha: 1}, 29.38);
  tl.to("#g5b", {autoAlpha: 1, scale: 1, duration: 0.28, ease: "back.out(2.2)"}, 29.50);
  // «забрати це» — it comes up out of the call
  tl.to("#g5b", {y: -70, scale: 0.9, duration: 0.40, ease: "power2.inOut"}, 30.10);
  // «і перетворити на контент» — and lands as the piece
  tl.to("#g5c", {autoAlpha: 1, scale: 1, duration: 0.36, ease: "back.out(2.4)"}, 31.36);
  tl.to("#g5", {autoAlpha: 0, duration: 0.22, ease: "power2.in"}, 31.84);'''
    return html, js


# ------------------------------------------------------------- B · the system


@beat
def b06_fathom():
    """«щось, що записує дзвінки — я для цього використовую Фатом, він
    безкоштовний» … «і штучний інтелект, у мене це Клод, який розшифровує ці
    дзвінки, розділяє їх на ідеї для контенту і витягує цитати клієнток»

    Takeover 2: the whole system in one frame, top to bottom, built one piece
    per word. Merged what used to be two beats (b06 + b07) because it is one
    diagram and cutting away mid-pipeline lost the thread.
    """
    html = '''
      <div class="g full" id="g6">
        <div class="tk paper"></div><div class="gp"></div>
        <div id="g6top" style="position:absolute;inset:0">
          <div class="wv" id="g6w" style="left:240px;top:170px;width:600px;height:180px">%s</div>
          <img class="fm" id="g6f" src="assets/logos/fathom-word.png" alt=""
               style="left:236px;top:392px;width:430px">
          <div class="zero" id="g6z" style="left:722px;top:390px">0 €</div>
        </div>
        <div class="tile brand prod" id="g6c" style="left:410px;top:566px">%s</div>
        <div class="txb" id="g6t" style="left:140px;top:894px;width:800px;height:214px">%s</div>
        <div class="dk" id="g6o1" style="left:110px;top:1146px;width:400px;height:250px">
          <i class="hb" style="width:210px"></i>
          <i class="rr" style="top:96px;width:300px"></i>
          <i class="rr" style="top:130px;width:240px"></i>
          <i class="pb" style="left:30px;top:168px;width:340px;height:52px"></i>
        </div>
        <div class="dk" id="g6o2" style="left:566px;top:1146px;width:400px;height:250px">
          <i class="hb" style="width:180px"></i>
          <i class="rr" style="top:96px;width:280px"></i>
          <i class="rr" style="top:130px;width:320px"></i>
          <i class="pb" style="left:30px;top:168px;width:340px;height:52px"></i>
        </div>
      </div>''' % ("""<i style="height:38px"></i><i style="height:88px"></i><i style="height:140px"></i><i style="height:66px"></i><i style="height:176px"></i><i style="height:44px"></i><i style="height:120px"></i><i style="height:92px"></i><i style="height:158px"></i><i style="height:58px"></i><i style="height:104px"></i><i style="height:72px"></i>""", mark("claude-tile"), """<i style="top:44px;width:690px"></i><i style="top:84px;width:620px"></i><i style="top:124px;width:660px"></i><i style="top:164px;width:540px"></i>""")
    js = '''
  gsap.set("#g6", {autoAlpha: 0});
  gsap.set("#g6top", {y: 430});
  gsap.set("#g6w i", {scaleY: 0.08, transformOrigin: "50%% 50%%"});
  gsap.set("#g6f, #g6z, #g6c", {autoAlpha: 0, scale: 0.6,
                                transformOrigin: "50%% 50%%"});
  gsap.set("#g6t", {autoAlpha: 0, y: 34});
  gsap.set("#g6t i", {scaleX: 0});
  gsap.set("#g6o1, #g6o2", {autoAlpha: 0, scale: 0.68, y: 40,
                            transformOrigin: "50%% 50%%"});
  tl.set("#g6", {autoAlpha: 1}, 34.74);
  // «щось, що записує дзвінки»
  tl.to("#g6w i", {scaleY: 1, duration: 0.34, ease: "back.out(2)",
                   stagger: {each: 0.026, from: "center"}}, 34.86);
  // «Фатом»
  tl.to("#g6f", {autoAlpha: 1, scale: 1, duration: 0.34,
                 ease: "back.out(2.4)"}, 37.34);
  // «безкоштовний» — a number is the one word §4 allows
  tl.to("#g6z", {autoAlpha: 1, scale: 1, duration: 0.30,
                 ease: "back.out(2.8)"}, 37.98);
  // «і штучний інтелект» — the recorder moves up to make room for what
  // reads it. Before this the frame was a logo and 1400px of empty paper.
  tl.to("#g6top", {y: 0, duration: 0.62, ease: "power2.inOut"}, 39.26);
  // «Клод»
  tl.to("#g6c", {autoAlpha: 1, scale: 1, duration: 0.34,
                 ease: "back.out(2.4)"}, 40.44);
  // «розшифровує ці дзвінки»
  tl.to("#g6t", {autoAlpha: 1, y: 0, duration: 0.30, ease: "power3.out"}, 41.00);
  tl.to("#g6t i", {scaleX: 1, duration: 0.20, ease: "power2.out",
                   stagger: 0.075}, 41.22);
  // «ідеї для контенту»
  tl.to("#g6o1", {autoAlpha: 1, scale: 1, y: 0, duration: 0.36,
                  ease: "back.out(2.2)"}, 43.36);
  // «витягує цитати клієнток»
  tl.to("#g6o2", {autoAlpha: 1, scale: 1, y: 0, duration: 0.36,
                  ease: "back.out(2.2)"}, 45.00);
  tl.to("#g6", {autoAlpha: 0, duration: 0.28, ease: "power2.in"}, 47.00);'''
    return html, js


@beat
def b08_ready_made():
    """«не просто тема, а готові сценарії, цитати, різні кути, як це подати»

    Takeover 3, and the payoff: the sentence from the transcript at 13.7s,
    now set large on a finished quote card, with three other pieces around it.
    Same words, same reel, forty seconds apart — that contrast is the whole
    mechanic, so the transcript at 13.7s must stay as bleak as it is.
    """
    html = '''
      <div class="g full" id="g8">
        <div class="tk blush"></div>
        <div class="dk" id="g8plain" style="left:290px;top:700px;width:500px;height:320px">
          <i class="rr" style="top:60px;width:380px"></i>
          <i class="rr" style="top:100px;width:300px"></i>
        </div>
        <div class="dk" id="g8p1" data-layout-allow-overflow
             style="left:-130px;top:180px;width:560px;height:700px">
          <i class="hb" style="width:300px"></i>
          <i class="rr" style="top:110px;width:460px"></i>
          <i class="rr" style="top:148px;width:400px"></i>
          <i class="rr" style="top:186px;width:440px"></i>
          <i class="pb" style="left:30px;top:250px;width:500px;height:300px"></i>
          <i class="rr" style="top:592px;width:420px"></i>
        </div>
        <div class="qcard" id="g8p2" data-layout-allow-overflow
             style="left:470px;top:110px;width:690px;height:486px">
          <div class="big2" style="top:96px;width:560px;font-size:64px;line-height:1.12">%s</div>
          <i style="position:absolute;left:54px;top:380px;width:150px;height:14px;border-radius:999px;background:var(--lit-pink)"></i>
        </div>
        <div class="dk" id="g8p3" data-layout-allow-overflow
             style="left:-100px;top:940px;width:600px;height:420px">
          <i class="hb" style="width:260px"></i>
          <i class="pb" style="left:30px;top:110px;width:540px;height:220px"></i>
        </div>
        <div class="dk" id="g8p4" data-layout-allow-overflow
             style="left:630px;top:664px;width:490px;height:700px">
          <i class="hb" style="width:230px"></i>
          <i class="pb" style="left:30px;top:100px;width:430px;height:360px"></i>
          <i class="rr" style="top:500px;width:380px"></i>
          <i class="rr" style="top:538px;width:300px"></i>
        </div>
      </div>''' % QUOTE
    js = '''
  gsap.set("#g8", {autoAlpha: 0});
  gsap.set("#g8plain", {autoAlpha: 0, scale: 0.8, transformOrigin: "50%% 50%%"});
  gsap.set("#g8p1", {autoAlpha: 0, x: -260, rotation: -8,
                     transformOrigin: "50%% 50%%"});
  gsap.set("#g8p2", {autoAlpha: 0, scale: 1.18, transformOrigin: "50%% 50%%"});
  gsap.set("#g8p3", {autoAlpha: 0, x: -220, rotation: 6,
                     transformOrigin: "50%% 50%%"});
  gsap.set("#g8p4", {autoAlpha: 0, x: 240, rotation: -5,
                     transformOrigin: "50%% 50%%"});
  tl.set("#g8", {autoAlpha: 1}, 50.52);
  // «не просто тема» — the thin version of the idea, on its own
  tl.to("#g8plain", {autoAlpha: 1, scale: 1, duration: 0.30,
                     ease: "back.out(2.2)"}, 50.64);
  tl.to("#g8plain", {autoAlpha: 0, scale: 0.86, duration: 0.26,
                     ease: "power2.in"}, 51.30);
  // «а готові сценарії»
  tl.to("#g8p1", {autoAlpha: 1, x: 0, rotation: -3.5, duration: 0.48,
                  ease: "back.out(1.7)"}, 51.36);
  // «цитати» — the transcript line from 16.4s, dressed
  tl.to("#g8p2", {autoAlpha: 1, scale: 1, duration: 0.50,
                  ease: "back.out(1.9)"}, 52.60);
  // «різні кути»
  tl.to("#g8p3", {autoAlpha: 1, x: 0, rotation: 3.0, duration: 0.46,
                  ease: "back.out(1.7)"}, 53.22);
  tl.to("#g8p4", {autoAlpha: 1, x: 0, rotation: -2.2, duration: 0.46,
                  ease: "back.out(1.7)"}, 53.52);
  tl.to("#g8", {autoAlpha: 0, duration: 0.28, ease: "power2.in"}, 55.70);'''
    return html, js


@beat
def b09_four_angles():
    """«з чим прийшла клієнтка, з чим вона пішла, як ви вирішили проблему і
    чому саме так, а не інакше»

    Matted. Four pieces fly out from behind her, one per clause, and leave the
    frame on both sides. Four phrases, four objects, each on its own word —
    STYLE.md 4.
    """
    html = '''
      <div class="g full" id="g9">
        %s
      </div>''' % "\n        ".join(
        '<div class="dk" id="%s" data-layout-allow-overflow'
        ' style="left:%dpx;top:%dpx;width:%dpx;height:%dpx">'
        '<i class="hb" style="width:%dpx"></i>'
        '<i class="rr" style="top:96px;width:%dpx"></i>'
        '<i class="pb" style="left:30px;top:140px;width:%dpx;height:%dpx"></i>'
        '</div>' % (i, x, y, w, h, int(w * 0.44), int(w * 0.66),
                    int(w * 0.82), int(h * 0.42))
        for i, x, y, w, h, r, t in ANGLES)
    sets = "\n".join(
        '  gsap.set("#%s", {x: %d, y: %d, scale: 0.08, rotation: 0,'
        ' autoAlpha: 0, transformOrigin: "50%%%% 50%%%%"});'
        % (i, 540 - (x + w // 2), 700 - (y + h // 2))
        for i, x, y, w, h, r, t in ANGLES)
    flies = "\n".join(
        '  tl.to("#%s", {x: 0, y: 0, scale: 1, rotation: %s, autoAlpha: 1,'
        ' duration: 0.62, ease: "power3.out"}, %.3f);' % (i, r, t)
        for i, x, y, w, h, r, t in ANGLES)
    js = '''
  gsap.set("#g9", {autoAlpha: 0});
%s
  tl.set("#g9", {autoAlpha: 1}, 55.90);
%s
  tl.to("#g9", {autoAlpha: 0, duration: 0.30, ease: "power2.in"}, 61.80);''' % (
        sets, flies)
    return html, js


# ------------------------------------------------------------------ C · the ask


# Four pieces flying out from behind her head. 188 frames.
k.matte("fourangles", 55.833, 6.300)


@beat
def b10_one_hour():
    """«підключити все це можна буквально за годину»"""
    html = '''
      <div class="g full" id="g10">
        <div class="big" id="g10n" style="top:200px;font-size:220px">1<small> год</small></div>
      </div>'''
    js = '''
  gsap.set("#g10", {autoAlpha: 0});
  gsap.set("#g10n", {autoAlpha: 0, scale: 0.6, transformOrigin: "50% 50%"});
  tl.set("#g10", {autoAlpha: 1}, 62.00);
  tl.to("#g10n", {autoAlpha: 1, scale: 1, duration: 0.34, ease: "back.out(2.8)"}, 62.12);
  tl.to("#g10", {autoAlpha: 0, duration: 0.24, ease: "power2.in"}, 64.20);'''
    return html, js


@beat
def b11_the_guide():
    """«якщо тобі страшно самій це все налаштовувати — у мене є інструкція саме
    для нетехнічних експерток, де я показую, куди натиснути»
    """
    html = '''
      <div class="g full" id="g11">
        <div class="guide" id="g11g">
          <span class="gh"></span><b></b><b></b><b></b>
          <span class="tapdot" id="g11d"></span>
        </div>
      </div>'''
    js = '''
  gsap.set("#g11", {autoAlpha: 0});
  gsap.set("#g11g", {autoAlpha: 0, scale: 0.86, transformOrigin: "50% 50%"});
  gsap.set("#g11g b", {scaleX: 0, transformOrigin: "0% 50%"});
  gsap.set("#g11d", {autoAlpha: 0, scale: 0.4, transformOrigin: "50% 50%"});
  tl.set("#g11", {autoAlpha: 1}, 68.08);
  // «є інструкція»
  tl.to("#g11g", {autoAlpha: 1, scale: 1, duration: 0.32, ease: "back.out(2.2)"}, 68.20);
  tl.to("#g11g b", {scaleX: 1, duration: 0.24, stagger: 0.10,
                    ease: "power2.out"}, 68.36);
  // «саме для нетехнічних експерток»
  tl.to("#g11g", {scale: 1.04, duration: 0.26, ease: "back.out(2.6)"}, 70.42);
  tl.to("#g11g", {scale: 1, duration: 0.30, ease: "power2.out"}, 70.72);
  // «де я показую, куди натиснути» — the tap lands where it is told to
  tl.to("#g11d", {autoAlpha: 1, scale: 1, duration: 0.26,
                  ease: "back.out(2.8)"}, 72.24);
  tl.to("#g11d", {scale: 0.82, duration: 0.14, ease: "power2.in"}, 72.60);
  tl.to("#g11d", {scale: 1, duration: 0.20, ease: "back.out(3)"}, 72.74);
  tl.to("#g11", {autoAlpha: 0, duration: 0.26, ease: "power2.in"}, 74.20);'''
    return html, js


@beat
def b12_write_the_word():
    """«якщо хочеш мати нескінченну кількість ідей — пиши слово «дзвінок»»

    The word itself, because it is an instruction the viewer has to follow
    exactly and a picture of a word is not a word (STYLE.md §4a.2). It lands in
    a message field and the send button fires.
    """
    html = '''
      <div class="g full" id="g12">
        <div class="word" id="g12w"><span>ДЗВІНОК</span></div>
        <div class="sendrow" id="g12s">
          <span class="field"></span><span class="go"></span>
        </div>
      </div>'''
    js = '''
  gsap.set("#g12", {autoAlpha: 0});
  gsap.set("#g12w", {autoAlpha: 0, scale: 0.78, transformOrigin: "50% 50%"});
  gsap.set("#g12s", {autoAlpha: 0, y: 30});
  tl.set("#g12", {autoAlpha: 1}, 75.64);
  // «нескінченну кількість ідей»
  tl.to("#g12w", {autoAlpha: 1, scale: 1, duration: 0.34, ease: "back.out(2.4)"}, 75.76);
  // «пиши слово «дзвінок»»
  tl.to("#g12w", {scale: 1.06, duration: 0.24, ease: "back.out(2.8)"}, 78.58);
  tl.to("#g12w", {scale: 1, duration: 0.26, ease: "power2.out"}, 78.84);
  tl.to("#g12s", {autoAlpha: 1, y: 0, duration: 0.28, ease: "back.out(2.2)"}, 79.98);
  tl.to("#g12s .go", {scale: 1.22, duration: 0.18, ease: "back.out(3)",
                      transformOrigin: "50% 50%"}, 80.36);
  tl.to("#g12s .go", {scale: 1, duration: 0.22}, 80.56);'''
    return html, js


k.css("""
    /* b00 — the two roles, and the moment they turn out to be one person */
    .role { position: absolute; width: 320px; height: 260px; border-radius: 54px;
            padding: 34px; background: var(--lit-blush); box-shadow: var(--rim);
            filter: var(--cast); }
    .role i { display: block; width: 92px; height: 92px; border-radius: 50%;
              background: var(--lit-accent); box-shadow: var(--rim-dark);
              margin-bottom: 26px; }
    .role b { display: block; height: 22px; border-radius: 11px;
              background: var(--graphite); width: 78%; }
    .role.alt { background: var(--lit-accent); box-shadow: var(--rim-dark); }
    .role.alt i { background: var(--lit-pink); }
    .role.alt b { background: rgba(255,255,255,0.85); }
    .burst { position: absolute; left: 420px; top: 220px; width: 240px;
             height: 240px; border-radius: 50%; background: var(--lit-pink);
             box-shadow: var(--rim-dark);
             filter: drop-shadow(0 0 40px rgba(255,110,156,0.9)); }

    /* b03 / b08 — the topic, which is only ever a label */
    .tag { position: absolute; left: 390px; top: 250px; width: 300px;
           height: 92px; border-radius: 46px;
           background: rgba(255,255,255,0.42); box-shadow: var(--rim);
           filter: var(--cast-sm); }

    /* b04 — what the exchange was worth */
    .coin { position: absolute; left: 430px; top: 170px; width: 200px;
            height: 200px; border-radius: 50%; display: grid;
            place-items: center; background: var(--lit-pink);
            box-shadow: var(--rim-dark),
                        inset 0 0 0 13px rgba(255,255,255,0.55);
            filter: var(--cast); }
    .coin span { font-size: 108px; font-weight: 900; color: #fff;
                 line-height: 1; letter-spacing: -0.04em; }

    /* b09 — four angles on one call */
    .grid4 { position: absolute; left: 150px; top: 100px; width: 780px;
             display: grid; gap: 22px; grid-template-columns: repeat(2, 1fr); }
    .grid4 span { display: block; height: 200px; border-radius: 36px;
                  background: var(--lit-blush); box-shadow: var(--rim);
                  filter: var(--cast-sm); }
    .grid4 span:nth-child(2) { background: var(--lit-accent);
                               box-shadow: var(--rim-dark); }
    .grid4 span:nth-child(3) { background: var(--lit-pink);
                               box-shadow: var(--rim-dark); }

    /* b11 — the instruction, and the thing it tells you to press */
    .guide { position: absolute; left: 240px; top: 120px; width: 600px;
             padding: 36px; background: var(--lit-blush); box-shadow: var(--rim);
             filter: var(--cast); border-radius: 48px; }
    .guide .gh { display: block; height: 48px; width: 58%; border-radius: 16px;
                 background: var(--lit-accent); margin-bottom: 28px;
                 box-shadow: var(--rim-dark); }
    .guide b { display: block; height: 22px; border-radius: 11px;
               background: var(--graphite); margin-bottom: 20px; }
    .guide b:nth-of-type(2) { width: 84%; }
    .guide b:nth-of-type(3) { width: 56%; }
    .guide .tapdot { position: absolute; right: 54px; bottom: 44px; width: 96px;
                     height: 96px; border-radius: 50%; background: var(--lit-pink);
                     box-shadow: var(--rim-dark);
                     filter: drop-shadow(0 0 30px rgba(255,110,156,0.85)); }

    /* b12 — the message she wants sent */
    .sendrow { position: absolute; left: 190px; top: 400px; width: 700px;
               display: flex; align-items: center; gap: 20px; }
    .sendrow .field { display: block; flex: 1; height: 96px; border-radius: 48px;
                      background: rgba(255,255,255,0.55); box-shadow: var(--rim); }
    .sendrow .go { display: block; width: 96px; height: 96px; flex: none;
                   border-radius: 50%; background: var(--lit-accent);
                   box-shadow: var(--rim-dark); }
""")

for _sel, _w, _h, _r in [
    (".guide", 600, 300, 48),
    (".role", 320, 260, 54),
]:
    k.squircle(_sel, _w, _h, _r)


# Nothing in reel 10's graphics says a word she is saying, so there is no
# blackout at all here (STYLE.md 2b.1) — the test is redundancy, not takeover.
BLACKOUT = []

INVERT = [
    (13.70, 19.95, "TK1 — the raw transcript, ruled paper"),
    (34.74, 47.00, "TK2 — the system"),
    (50.52, 55.70, "TK3 — the payoff, blushed"),
]


def main():
    caps = k.load_captions(os.path.join(ROOT, "work", "r10", "captions.json"))
    gh, gj = [], []
    for fn in BEATS:
        h, j = fn()
        if h.strip():
            gh.append(h.rstrip())
        gj.append("  /* %s */" % fn.__name__)
        gj.append(j.rstrip())

    doc = k.document(
        title="Reel 10 — контент з дзвінків",
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
