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
    """«це не просто тема… це ще й текст саме так, як говорить твоя цільова
    аудиторія»

    The topic is a label; the words are the thing. So a plain tag arrives, and
    is replaced by the client's own sentence — the object the reel is built on.
    """
    html = '''
      <div class="g full" id="g3">
        <div class="tag" id="g3t"></div>
        %s
      </div>''' % bubble("g3b", "client", rows=2, style="left:280px;top:190px")
    js = '''
  gsap.set("#g3", {autoAlpha: 0});
  gsap.set("#g3t", {autoAlpha: 0, scale: 0.7, transformOrigin: "50% 50%"});
  gsap.set("#g3b", {autoAlpha: 0, scale: 0.84, transformOrigin: "50% 50%"});
  tl.set("#g3", {autoAlpha: 1}, 13.70);
  // «не просто тема» — a label, and that is all it is
  tl.to("#g3t", {autoAlpha: 1, scale: 1, duration: 0.28, ease: "back.out(2.4)"}, 13.84);
  tl.to("#g3t", {autoAlpha: 0, scale: 0.8, y: -40, duration: 0.28,
                 ease: "power2.in"}, 16.10);
  // «це ще й текст саме так, як говорить твоя аудиторія»
  tl.to("#g3b", {autoAlpha: 1, scale: 1, duration: 0.34, ease: "back.out(2.2)"}, 16.40);
  // «саме так, як говорить» — it is hers, and it stays hers
  tl.to("#g3b", {scale: 1.05, duration: 0.26, ease: "back.out(2.6)"}, 18.96);
  tl.to("#g3b", {scale: 1, duration: 0.30, ease: "power2.out"}, 19.24);
  tl.to("#g3", {autoAlpha: 0, duration: 0.26, ease: "power2.in"}, 19.90);'''
    return html, js


@beat
def b04_she_said_you_replied():
    """«тобі не треба вигадувати… клієнтка вже сказала тобі щось, ти якось
    відповіла, і вона за це заплатила гроші»

    Three moves on three phrases: her line, your line, and the money that
    proves the exchange worked.
    """
    html = '''
      <div class="g full" id="g4">
        %s
        %s
        <div class="coin" id="g4m"><span>€</span></div>
      </div>''' % (
        bubble("g4a", "client", rows=2, style="left:110px;top:120px"),
        bubble("g4b", "mine", rows=2, style="left:450px;top:300px"))
    js = '''
  gsap.set("#g4", {autoAlpha: 0});
  gsap.set("#g4a, #g4b", {autoAlpha: 0, scale: 0.84, transformOrigin: "50% 50%"});
  gsap.set("#g4m", {autoAlpha: 0, scale: 0.4, transformOrigin: "50% 50%"});
  tl.set("#g4", {autoAlpha: 1}, 22.90);
  // «клієнтка вже сказала тобі щось»
  tl.to("#g4a", {autoAlpha: 1, scale: 1, duration: 0.30, ease: "back.out(2.2)"}, 23.02);
  // «ти якось відповіла»
  tl.to("#g4b", {autoAlpha: 1, scale: 1, duration: 0.30, ease: "back.out(2.2)"}, 25.66);
  // «і вона за це заплатила гроші»
  tl.to("#g4m", {autoAlpha: 1, scale: 1, duration: 0.34, ease: "back.out(2.8)"}, 27.64);
  tl.to("#g4b, #g4a", {autoAlpha: 0.25, duration: 0.30}, 27.84);
  tl.to("#g4", {autoAlpha: 0, duration: 0.26, ease: "power2.in"}, 29.20);'''
    return html, js


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
    """«потрібна система: щось, що записує дзвінки — я використовую Фатом, він
    безкоштовний»
    """
    html = '''
      <div class="g full" id="g6">
        %s
        <div class="freewrap" id="g6free"><div class="lit soft"></div>
          <div class="free"><span>0</span><small>€</small></div></div>
      </div>''' % marktile("g6t", "fathom-word", "wide",
                           style="left:180px;top:170px")
    js = '''
  gsap.set("#g6", {autoAlpha: 0});
  gsap.set("#g6t", {autoAlpha: 0, scale: 0.8, transformOrigin: "50% 50%"});
  gsap.set("#g6free", {autoAlpha: 0, scale: 0.5, transformOrigin: "50% 50%"});
  tl.set("#g6", {autoAlpha: 1}, 34.74);
  // «щось, що записує дзвінки»
  tl.to("#g6t", {autoAlpha: 1, scale: 1, duration: 0.32, ease: "back.out(2.4)"}, 34.86);
  // «він безкоштовний» — the same badge as reels 7 and 8
  tl.to("#g6free", {autoAlpha: 1, scale: 1, duration: 0.32,
                    ease: "back.out(2.8)"}, 37.34);
  tl.to("#g6", {autoAlpha: 0, duration: 0.26, ease: "power2.in"}, 39.20);'''
    return html, js


@beat
def b07_claude_does_three_things():
    """«штучний інтелект — у мене це Клод, який розшифровує ці дзвінки,
    розділяє їх на ідеї для контенту і витягує цитати клієнток»

    Three verbs, three moves, one per word: the sound becomes text, the text
    splits into pieces, and her sentence comes back out of it.
    """
    html = '''
      <div class="g full" id="g7">
        %s
        <div class="wave" id="g7w" style="left:230px;top:330px;width:620px;
             height:120px;justify-content:center">%s</div>
        <div class="lines" id="g7t" style="left:280px;top:330px;width:520px">
          <b></b><b></b><b></b>
        </div>
        %s%s%s
        %s
      </div>''' % (
        marktile("g7c", "claude-tile", style="left:410px;top:40px"),
        "".join('<i style="height:%dpx"></i>' % h for h in
                [24, 56, 96, 40, 78, 30, 66, 44, 88, 34, 72, 26, 60, 48]),
        card("g7a", style="left:180px;top:300px"),
        card("g7b", style="left:435px;top:300px"),
        card("g7d", style="left:690px;top:300px"),
        bubble("g7q", "client", rows=1, style="left:280px;top:285px;width:520px"))
    js = '''
  gsap.set("#g7", {autoAlpha: 0});
  gsap.set("#g7c", {autoAlpha: 0, scale: 0.78, transformOrigin: "50% 50%"});
  gsap.set("#g7w, #g7t, #g7q", {autoAlpha: 0});
  gsap.set("#g7w i", {scaleY: 0.2, transformOrigin: "50% 50%"});
  gsap.set("#g7a, #g7b, #g7d", {autoAlpha: 0, scale: 0.7,
                                transformOrigin: "50% 50%"});
  tl.set("#g7", {autoAlpha: 1}, 39.52);
  // «у мене це Клод»
  tl.to("#g7c", {autoAlpha: 1, scale: 1, duration: 0.32, ease: "back.out(2.4)"}, 39.64);
  // «розшифровує ці дзвінки» — sound in, text out
  tl.to("#g7w", {autoAlpha: 1, duration: 0.14}, 41.00);
  tl.to("#g7w i", {scaleY: 1, duration: 0.30, ease: "back.out(2)",
                   stagger: {each: 0.012, from: "center"}}, 41.02);
  tl.to("#g7w", {autoAlpha: 0, scaleY: 0.3, duration: 0.24,
                 ease: "power2.in"}, 42.02);
  tl.to("#g7t", {autoAlpha: 1, duration: 0.22}, 42.14);
  tl.from("#g7t b", {scaleX: 0, transformOrigin: "0% 50%", duration: 0.22,
                     stagger: 0.06, ease: "power2.out"}, 42.16);
  // «розділяє їх на ідеї для контенту» — the text becomes pieces
  tl.to("#g7t", {autoAlpha: 0, duration: 0.20}, 42.74);
  [42.78, 43.00, 43.22].forEach(function (t, i) {
    tl.to(["#g7a", "#g7b", "#g7d"][i], {autoAlpha: 1, scale: 1, duration: 0.30,
                                        ease: "back.out(2.2)"}, t);
  });
  // «і витягує цитати клієнток» — and her own sentence comes back out
  tl.to("#g7a, #g7b, #g7d", {autoAlpha: 0.2, duration: 0.26}, 45.00);
  tl.fromTo("#g7q", {autoAlpha: 0, y: 50, scale: 0.86},
            {autoAlpha: 1, y: 0, scale: 1, duration: 0.36,
             ease: "back.out(2.4)"}, 45.00);
  tl.to("#g7", {autoAlpha: 0, duration: 0.28, ease: "power2.in"}, 46.90);'''
    return html, js


@beat
def b08_ready_made():
    """«після кожного дзвінка не просто тема, а готові сценарії, цитати, різні
    кути, як це подати»
    """
    html = '''
      <div class="g full" id="g8">
        <div class="tag" id="g8t"></div>
        %s%s%s
      </div>''' % (
        card("g8a", style="left:180px;top:240px"),
        card("g8b", "quoted", style="left:435px;top:240px"),
        card("g8c", style="left:690px;top:240px"))
    js = '''
  gsap.set("#g8", {autoAlpha: 0});
  gsap.set("#g8t", {autoAlpha: 0, scale: 0.7, transformOrigin: "50% 50%"});
  gsap.set("#g8a, #g8b, #g8c", {autoAlpha: 0, scale: 0.7, y: 40,
                                transformOrigin: "50% 50%"});
  tl.set("#g8", {autoAlpha: 1}, 50.52);
  // «не просто тема»
  tl.to("#g8t", {autoAlpha: 1, scale: 1, duration: 0.26, ease: "back.out(2.4)"}, 50.64);
  tl.to("#g8t", {autoAlpha: 0, scale: 0.8, duration: 0.22, ease: "power2.in"}, 51.70);
  // «готові сценарії» / «цитати» / «різні кути»
  [51.89, 52.60, 53.60].forEach(function (t, i) {
    tl.to(["#g8a", "#g8b", "#g8c"][i], {autoAlpha: 1, scale: 1, y: 0,
                                        duration: 0.32,
                                        ease: "back.out(2.2)"}, t);
  });
  // «як це подати» — they fan to show they are different angles on one thing
  tl.to("#g8a", {rotation: -5, duration: 0.30, ease: "power2.out",
                 transformOrigin: "50% 100%"}, 54.20);
  tl.to("#g8c", {rotation: 5, duration: 0.30, ease: "power2.out",
                 transformOrigin: "50% 100%"}, 54.20);
  tl.to("#g8", {autoAlpha: 0, duration: 0.26, ease: "power2.in"}, 55.60);'''
    return html, js


@beat
def b09_four_angles():
    """«з чим прийшла клієнтка, з чим вона пішла, як ви вирішували проблему і
    чому саме так, а не інакше»

    Four pieces out of one call, one per phrase, on her uneven spacing.
    """
    html = '''
      <div class="g full" id="g9">
        <div class="grid4" id="g9g">
          <span id="g9a"></span><span id="g9b"></span>
          <span id="g9c"></span><span id="g9d"></span>
        </div>
      </div>'''
    js = '''
  gsap.set("#g9", {autoAlpha: 0});
  gsap.set("#g9g span", {autoAlpha: 0, scale: 0.6, transformOrigin: "50% 50%"});
  tl.set("#g9", {autoAlpha: 1}, 55.90);
  [57.68, 58.68, 60.00, 61.56].forEach(function (t, i) {
    tl.to(["#g9a", "#g9b", "#g9c", "#g9d"][i],
          {autoAlpha: 1, scale: 1, duration: 0.30, ease: "back.out(2.4)"}, t);
  });
  tl.to("#g9", {autoAlpha: 0, duration: 0.26, ease: "power2.in"}, 62.00);'''
    return html, js


# ------------------------------------------------------------------ C · the ask


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
    )
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "index.html")
    io.open(out, "w", encoding="utf-8").write(doc)
    print("index.html  %d captions, %d beats, %.1f KB"
          % (len(caps), len(BEATS), os.path.getsize(out) / 1024.0))


main()
