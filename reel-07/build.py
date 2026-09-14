# -*- coding: utf-8 -*-
"""Reel 7 — «системи, які я б поставила з самого початку».

Variant B: her cut, graded, no subtitles. Materials from tools/kit.py
(STYLE.md §5a); what each beat depicts is invented for this script.

The recurring object is a **board of six slots**. She names six systems in
order, so the board is the script's own structure made visible: the slots are
drawn empty in the first beat, each one accepts its system as she gets to it,
and at «командний центр» they wire into a hub. STYLE.md §4 — reuse objects; a
returning object costs nothing to read, and the final wiring only lands because
the viewer watched the board fill.

Design notes that are decisions, not taste:
  * RUTA is set as type, not artwork — her call, no icon exists yet. All caps,
    ProductSans-Black, thickened with -webkit-text-stroke because that is the
    heaviest weight on the machine.
  * Cal.com and Google Calendar are drawn glyphs until she uploads marks; the
    swap is one <img> each and nothing else changes.
  * CRM stays a drawn database glyph on purpose (STYLE.md §5b — the script
    names no CRM brand, so a real logo would be the wrong brand).

usage: python build.py
"""
import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
from kit import Kit  # noqa: E402

DUR = 133.266          # 3998 plate frames / 30, rounded DOWN:
                       # the renderer ceils DUR*fps, so 133.267 asks
                       # for 3998.01 and emits 3999 frames.
k = Kit(width=1080, height=1920, fps=30, duration=DUR)

BEATS = []


def beat(fn):
    BEATS.append(fn)
    return fn


# ---------------------------------------------------------------- materials

def slot(sid, ghost="", cls=""):
    """One frosted slot, holding a greyed-out ghost of the mark that will land
    in it. §5a.9 still applies — the plaque arrives before the colour does —
    but a *blank* plaque turned out to say nothing at all."""
    return ('<div class="slot %s" id="%s"><span class="ghost">%s</span></div>'
            % (cls, sid, ghost))


def tile(tid, inner, cls="", lit=False, over=""):
    """A filled system tile.

    `lit` is off by default on purpose. The glow rides the wrapper rather than
    the clipped element (§5a.10) — but six glowing tiles is six filters against
    the heavy-overlay budget and, worse, "everything glowing is nothing
    glowing". Only her own product gets it."""
    halo = '<div class="lit soft"></div>' if lit else ''
    # `over` is a SIBLING of the tile face, never a child: b13/b16 swap a
    # tile by fading its face out, and a child would fade out with it.
    return ('<div class="slotwrap %s" id="%s">%s'
            '<div class="tile brand">%s</div>%s</div>'
            % (cls, tid, halo, inner, over))


def bars(n, cls="pr"):
    return "".join('<b class="%s"></b>' % cls for _ in range(n))


def logo(name, cls=""):
    return '<img class="mk %s" src="assets/logos/%s.png" alt="">' % (cls, name)


def checklist(cid=""):
    """Tasks are checks and lines, her note — not three coloured bars."""
    rows = "".join('<i><b></b><s></s></i>' for _ in range(3))
    return '<span class="chk"%s>%s</span>' % (
        (' id="%s"' % cid) if cid else "", rows)


def freebadge(bid):
    """«безкоштовний» — a number is the one word STYLE.md §4 allows, and 0 is
    the whole point of both Cal.com and Fathom. Reused for the second one."""
    return ('<div class="freewrap" id="%s"><div class="lit soft"></div>'
            '<div class="free"><span>0</span><small>\u20ac</small></div></div>' % bid)


def cal(cid, on=6):
    """Calendar glyph — placeholder for Cal.com and Google Calendar both."""
    cells = "".join('<i class="%s"></i>' % ("on" if i == on else "")
                    for i in range(12))
    return ('<div class="cal" id="%s"><span class="top"></span>'
            '<span class="grid">%s</span></div>' % (cid, cells))


k.css("""
    /* ---- the board: 3x2, centred, inside the clear band (STYLE.md §3) ---- */
    .board { position: absolute; left: 60px; top: 36px; width: 960px;
             height: 520px; display: grid; gap: 40px;
             grid-template-columns: repeat(3, 1fr);
             grid-template-rows: repeat(2, 1fr); }
    /* An empty slot has to read as an object over a dark kitchen, so it runs
       warmer and brighter than plain glass: 0.15 alpha disappeared entirely in
       the first snapshot pass. */
    .slot { position: relative; display: grid; place-items: center;
            background: linear-gradient(158deg, rgba(255,255,255,0.30) 0%,
                        rgba(255,214,225,0.20) 100%);
            -webkit-backdrop-filter: blur(26px) saturate(1.6);
            backdrop-filter: blur(26px) saturate(1.6);
            box-shadow: var(--rim-glass); filter: var(--cast); }

    /* The not-yet-set-up state: the mark is there, drained of colour and sunk
       into the glass. Never invisible — the whole point is that you can read
       what the board is before a single tile has landed. */
    .ghost { display: grid; place-items: center; width: 100%; height: 100%;
             opacity: 0.42; filter: grayscale(1) contrast(0.75) brightness(1.25); }
    .ghost .mk { width: 52%; }
    .ghost .mk.wide { width: 72%; }
    .ghost .wordmark { font-size: 58px; color: rgba(255,255,255,0.9);
                       -webkit-text-stroke: 3px rgba(255,255,255,0.9); }
    .slotwrap { position: relative; }
    .slotwrap .tile.brand { position: absolute; inset: 0; display: grid;
                            place-items: center; background: var(--lit-blush); }
    .mk { display: block; width: 62%; height: auto; object-fit: contain; }
    .mk.wide { width: 84%; }

    /* ---- RUTA: type as a mark, her call. Stroke thickens Black further. ---- */
    .wordmark { font-size: 74px; font-weight: 900; color: var(--accent);
                letter-spacing: -0.045em; line-height: 1;
                -webkit-text-stroke: 4px var(--accent); }
    .wordmark.big { font-size: 150px; -webkit-text-stroke: 7px var(--accent); }
    #tlcrm { font-size: 64px; }

    /* ---- a number on its own: the one word §4 allows ---- */
    .num { position: absolute; left: 0; width: 1080px; text-align: center;
           font-size: 220px; font-weight: 900; color: #fff;
           letter-spacing: -0.05em; text-shadow: 0 18px 60px rgba(8,6,12,0.55); }
    .num small { font-size: 0.46em; letter-spacing: -0.02em; }

    /* ---- calendar glyph ---- */
    .cal { position: absolute; width: 210px; height: 200px;
           background: var(--lit); box-shadow: var(--rim);
           filter: var(--cast); border-radius: 34px; overflow: hidden; }
    .cal .top { position: absolute; left: 0; top: 0; width: 100%; height: 50px;
                background: var(--lit-accent); }
    .cal .grid { position: absolute; left: 18px; top: 72px; right: 18px;
                 display: grid; gap: 9px; grid-template-columns: repeat(4, 1fr); }
    .cal .grid i { display: block; height: 22px; border-radius: 7px;
                   background: var(--graphite); }
    .cal .grid i.on { background: var(--accent); }

    /* ---- chat volley ---- */
    .bub { position: absolute; height: 92px; border-radius: 46px;
           background: var(--lit); box-shadow: var(--rim);
           filter: var(--cast-sm); }
    .bub.them { background: var(--lit-accent); }
    .linkchip { position: absolute; height: 104px; border-radius: 52px;
                background: var(--lit-accent); box-shadow: var(--rim-dark);
                display: grid; place-items: center; }
    .linkchip b { display: block; width: 96px; height: 16px; border-radius: 8px;
                  background: #fff; }

    /* ---- waveform -> text ---- */
    .wave { position: absolute; display: flex; align-items: center; gap: 11px; }
    .wave i { display: block; width: 14px; border-radius: 7px;
              background: var(--pink); }

    /* ---- database / CRM ---- */
    .db { position: absolute; width: 190px; height: 200px; }
    .db i { position: absolute; left: 0; width: 190px; height: 58px;
            border-radius: 95px / 29px; background: var(--lit-accent);
            box-shadow: var(--rim-dark); }
    .row { position: absolute; display: grid; gap: 14px; }
    .row .cell { height: 78px; border-radius: 20px; background: var(--container);
                 box-shadow: var(--rim); }
    .row .cell.on { background: var(--lit-accent); }

    /* ---- checklist ---- */
    .task { position: absolute; height: 96px; border-radius: 28px;
            background: var(--lit); box-shadow: var(--rim);
            filter: var(--cast-sm); display: flex; align-items: center;
            padding: 0 28px; gap: 24px; }
    .task .box { width: 52px; height: 52px; border-radius: 16px;
                 background: var(--container-high); flex: none; }
    .task.done .box { background: var(--lit-accent); }
    .task .line { height: 20px; border-radius: 10px; background: var(--graphite);
                  flex: 1; }

    /* ---- content fan ---- */
    .cc { position: absolute; width: 220px; height: 300px;
          background: var(--lit-blush); box-shadow: var(--rim);
          filter: var(--cast); padding: 26px; }
    .cc b { display: block; border-radius: 8px; background: var(--graphite);
            height: 16px; margin-bottom: 14px; }
    .cc b:first-child { height: 28px; background: var(--lit-accent); width: 70%; }

    /* ---- four panes around the hub ---- */
    .pane { position: absolute; width: 200px; height: 150px; border-radius: 34px;
            background: linear-gradient(158deg, rgba(255,255,255,0.34) 0%,
                        rgba(255,214,225,0.24) 100%);
            -webkit-backdrop-filter: blur(20px) saturate(1.6);
            backdrop-filter: blur(20px) saturate(1.6);
            box-shadow: var(--rim-glass); filter: var(--cast); padding: 22px; }
    .pane b { display: block; height: 15px; border-radius: 8px;
              background: rgba(255,255,255,0.94); margin-bottom: 13px; }
    .pane b:nth-child(2) { width: 78%; }
    .pane b:nth-child(3) { width: 52%; }
""")

# §5a.1 — squircle the LARGE surfaces only. The budget that turns a render
# black counts elements carrying clip-path / blur / radial-gradient, so small
# and repeated things (cells, bars, chips) keep a plain border-radius.
for sel, w, h, r in [
    (".slot", 293, 240, 54),
    (".slotwrap .tile.brand", 293, 240, 54),
]:
    k.squircle(sel, w, h, r)


# ---------------------------------------------------------------------------
# NO-PAINT ZONES — her own editing, and it is doing a job.
#
#   "when you see some funny editing (extra closeup, extra far away) those are
#    funny bits and dont paint over them"                    — 2026-09-14
#
# tools/shots.py found 13 shots; five of them are inserts she cut in for
# comedy, and one more span she flagged by hand. Nothing is drawn inside these:
#
#   3.63 –  4.83   punch-in to her hands  (shot 1)
#  16.30 – 17.27   big face closeup       (shot 4)
#  21.30 – 24.80   «а у вівторок, а у четверг» — the jump-cut gag she flagged
#  61.47 – 63.17   pulled way out         (shot 7)
#  67.27 – 68.10   punch-in to her hands  (shot 9)
#
# Captions keep running through them; only graphics stand down.
NO_PAINT = [(3.63, 4.83), (11.00, 14.75), (16.30, 17.27), (21.30, 24.80),
            (61.47, 63.17), (67.27, 68.10)]
#
# 11.00–14.75 and 61.50–63.00 are *zooms*, not cuts — she pushes the plate back
# and black appears around it. Scene detection cannot see those, so they are
# found by border luminance instead: tools/pullouts.py.


def board_html():
    """The spine. One board, six slots, built once and referred to by every
    system beat — STYLE.md §4 «reuse objects». Slots land empty (§5a.9) and
    each tile drops into its own slot when she names it."""
    ghosts = [logo("cal-mark"), logo("fathom-word", "wide"),
              '<span class="wordmark">CRM</span>', checklist(),
              '<span class="wordmark">RUTA</span>', logo("claude-tile")]
    cells = []
    for i in range(6):
        cells.append(slot("sl%d" % i, ghosts[i]))
    return ('\n      <div class="g full" id="gboard"><div class="board">%s</div>'
            '<div class="board" id="boardfill">%s</div></div>'
            % ("".join(cells), "".join([
                tile("tl0", logo("cal-mark")),
                tile("tl1", logo("fathom-word", "wide")),
                tile("tl2", '<span class="wordmark" id="tlcrm">CRM</span>',
                     over='<div class="tile brand ontile" id="tl2notion">%s</div>'
                          % logo("notion-mark")),
                tile("tl3", checklist("tlchk"),
                     over='<div class="tile brand ontile" id="tl3notion">%s</div>'
                          % logo("notion-mark")),
                tile("tl4", '<span class="wordmark">RUTA</span>', lit=True),
                tile("tl5", logo("claude-tile")),
            ])))


# ------------------------------------------------------------------ A · hook


@beat
def b01_board_appears():
    """«тобі потрібно думати про системи вже зараз, а не через півроку»

    Six empty slots snap in — the shape of a system before there is anything in
    it. It cannot land on «системи» (3.58) because her hand punch-in owns
    3.63–4.83, so it arrives the moment that insert releases the frame.
    """
    js = '''
  gsap.set("#gboard", {autoAlpha: 0});
  gsap.set("#boardfill .slotwrap", {autoAlpha: 0});
  gsap.set(".board .slot", {autoAlpha: 0, scale: 0.72, transformOrigin: "50% 50%"});
  tl.set("#gboard", {autoAlpha: 1}, 4.88);
  // six slots, unevenly — even spacing reads as automated (§4)
  [0,1,2,3,4,5].forEach(function (i) {
    tl.to("#sl" + i, {autoAlpha: 1, scale: 1, duration: 0.30, ease: "back.out(2.2)"},
          4.88 + [0, 0.07, 0.17, 0.26, 0.30, 0.41][i]);
  });'''
    return "", js


@beat
def b02_half_year():
    """«коли настане момент масштабуватись… через півроку буде пізно»

    A clock sweeps half a turn across the empty board and the slots dim behind
    it: six months pass and nothing got built.
    """
    html = '''
      <div class="g full" id="g2">
        <svg id="g2clock" width="300" height="300" viewBox="0 0 300 300"
             style="position:absolute;left:390px;top:146px">
          <circle cx="150" cy="150" r="130" fill="rgba(23,20,28,0.42)"/>
          <circle cx="150" cy="150" r="118" fill="none"
                  stroke="rgba(255,255,255,0.62)" stroke-width="16"/>
          <path id="g2arc" d="M150 32 A118 118 0 0 1 150 268" fill="none"
                stroke="#ff6e9c" stroke-width="22" stroke-linecap="round"
                stroke-dasharray="371" stroke-dashoffset="371"/>
          <line id="g2hand" x1="150" y1="150" x2="150" y2="48" stroke="#fff"
                stroke-width="20" stroke-linecap="round"/>
          <circle cx="150" cy="150" r="16" fill="#fff"/>
        </svg>
      </div>'''
    js = '''
  gsap.set("#g2", {autoAlpha: 0});
  tl.set("#g2", {autoAlpha: 1}, 5.58);
  tl.to("#g2clock", {autoAlpha: 1, duration: 0.20}, 5.58);
  // «півроку» — half a turn, and it does not come back
  tl.to("#g2hand", {rotation: 180, svgOrigin: "150 150",
                    duration: 1.30, ease: "power2.inOut"}, 5.62);
  tl.to("#g2arc", {strokeDashoffset: 0, duration: 1.30, ease: "power2.inOut"}, 5.62);
  tl.to(".board .slot", {opacity: 0.34, duration: 0.60}, 8.26);
  tl.to("#g2", {autoAlpha: 0, duration: 0.30, ease: "power2.in"}, 8.90);
  // out before 11.00 — her pull-out owns the frame from there to 14.75
  tl.to("#gboard", {autoAlpha: 0, duration: 0.40, ease: "power2.in"}, 10.40);'''
    return html, js


# b03 «звідки прийшли твої клієнти, скільки в тебе грошей, з ким ти
# розмовляла» used to draw three objects falling out of frame here. It is gone:
# she pulls the camera way out across exactly those words, and that *is* the
# beat. Painting over it would be competing with her own joke.


# ------------------------------------------------------- B · 1 · booking


@beat
def b04_slot_one():
    """«якщо б я тільки починала надавати послуги. Перша це система запису»

    The board comes back clean — this is the do-over she is describing — and
    slot 1 lights. Held clear of 16.30–17.27, her face closeup.
    """
    js = '''
  tl.set("#gboard", {autoAlpha: 1}, 17.34);
  tl.set(".board .slot", {opacity: 1}, 17.34);
  [0,1,2,3,4,5].forEach(function (i) {
    tl.to("#sl" + i, {autoAlpha: 1, scale: 1, duration: 0.26, ease: "back.out(2)"},
          17.34 + i * 0.05);
  });
  // «Перша» — the first one is the one we are talking about
  tl.to("#sl0", {scale: 1.06, duration: 0.22, ease: "back.out(3)"}, 19.27);
  tl.to("#sl0", {scale: 1, duration: 0.30, ease: "power2.out"}, 19.52);'''
    return "", js


@beat
def b05_calendar_lands():
    """«система запису на консультації»

    The calendar drops into slot 1 and is gone again before 21.30 — her
    «а у вівторок, а у четверг» gag owns the frame from there to 24.80.
    """
    js = '''
  tl.to("#tl0", {autoAlpha: 1, duration: 0.24, ease: "power2.out"}, 20.02);
  gsap.set("#tl0", {scale: 0.8, transformOrigin: "50% 50%"});
  tl.to("#tl0", {scale: 1, duration: 0.34, ease: "back.out(2.4)"}, 20.02);
  // stand down for her jump-cut gag, come back when she does
  tl.to("#gboard", {autoAlpha: 0, duration: 0.22, ease: "power2.in"}, 21.06);'''
    return "", js


@beat
def b06_one_link():
    """«а просто давати посилання, і людина сама обирає час»

    One link chip, then a slot on the calendar fills itself — the viewer sees
    the booking happen without her touching it.
    """
    html = '''
      <div class="g full" id="g6">
        <div class="linkchip" id="g6link" style="left:390px;top:300px;width:300px">
          <b></b>
        </div>
        %s
      </div>''' % cal("g6cal").replace('class="cal"',
                                       'class="cal" style="left:435px;top:236px"')
    js = '''
  gsap.set("#g6", {autoAlpha: 0});
  gsap.set("#g6link", {autoAlpha: 0, scale: 0.7, transformOrigin: "50% 50%"});
  gsap.set("#g6cal", {autoAlpha: 0, scale: 0.86, transformOrigin: "50% 50%"});
  gsap.set("#g6cal .grid i.on", {autoAlpha: 0});
  tl.set("#g6", {autoAlpha: 1}, 24.94);
  // «посилання» — one chip instead of the volley
  tl.to("#g6link", {autoAlpha: 1, scale: 1, duration: 0.30, ease: "back.out(2.6)"}, 25.58);
  tl.to("#g6link", {autoAlpha: 0, scale: 0.82, y: -40, duration: 0.30,
                    ease: "power2.in"}, 26.62);
  // «людина сама обирає час» — the slot fills itself
  tl.to("#g6cal", {autoAlpha: 1, scale: 1, duration: 0.30, ease: "back.out(2.2)"}, 26.72);
  tl.to("#g6cal .grid i.on", {autoAlpha: 1, duration: 0.18, ease: "power2.out"}, 27.06);
  tl.to("#g6", {autoAlpha: 0, duration: 0.26, ease: "power2.in"}, 28.20);'''
    return html, js


@beat
def b07_cal_syncs():
    """«Cal.com, він безкоштовний, і сам синхронізується з Google Календарем»

    Rebuilt after her review. Three things were wrong: the price never appeared
    though «безкоштовний» is the selling point, the sync landed a beat late and
    was still finishing over «Друге», and the thing travelling the wire was a
    glowing dot nobody could read. Now it is an event block, it leaves on
    «синхронізується» and it is gone before she says «Друге» at 31.92.
    """
    html = '''
      <div class="g full" id="g7">
        <div class="tile brand pair" id="g7a" style="left:150px;top:200px">%s</div>
        <div class="tile brand pair" id="g7b" style="left:640px;top:200px">%s</div>
        <svg width="1080" height="600" viewBox="0 0 1080 600"
             style="position:absolute;left:0;top:0">
          <path id="g7wire" class="wire" stroke="#ff6e9c"
                d="M440 345 C 500 345, 580 345, 640 345"
                stroke-dasharray="200" stroke-dashoffset="200"/>
        </svg>
        <div class="event" id="g7ev"><b></b><s></s></div>
        %s
      </div>''' % (logo("cal-mark"), logo("gcal-mark"), freebadge("g7free"))
    js = '''
  gsap.set("#g7", {autoAlpha: 0});
  gsap.set("#g7a, #g7b", {autoAlpha: 0, scale: 0.86, transformOrigin: "50% 50%"});
  gsap.set("#g7ev", {autoAlpha: 0, x: 300, y: 318, scale: 0.9});
  gsap.set("#g7free", {autoAlpha: 0, scale: 0.5, transformOrigin: "50% 50%"});
  tl.set("#g7", {autoAlpha: 1}, 28.50);
  tl.to("#g7a", {autoAlpha: 1, scale: 1, duration: 0.28, ease: "back.out(2.2)"}, 28.58);
  // «він безкоштовний» — the price, and the only reason it is on the board
  tl.to("#g7free", {autoAlpha: 1, scale: 1, duration: 0.32,
                    ease: "back.out(2.8)"}, 29.36);
  tl.to("#g7free", {autoAlpha: 0, scale: 0.8, duration: 0.24,
                    ease: "power2.in"}, 30.24);
  // «сам синхронізується» — the other calendar, then the wire between them
  tl.to("#g7b", {autoAlpha: 1, scale: 1, duration: 0.28, ease: "back.out(2.2)"}, 30.50);
  tl.to("#g7wire", {strokeDashoffset: 0, duration: 0.34, ease: "power2.out"}, 30.74);
  // «з Google Календарем» — the booking itself crosses. An event block, not a
  // dot: she could not tell what the dot was, which means it was not an object.
  tl.to("#g7ev", {autoAlpha: 1, duration: 0.14}, 31.10);
  tl.to("#g7ev", {x: 700, duration: 0.42, ease: "power2.inOut"}, 31.16);
  tl.to("#g7ev", {autoAlpha: 0, scale: 0.7, duration: 0.16}, 31.58);
  tl.to("#g7b", {scale: 1.08, duration: 0.18, ease: "back.out(3)"}, 31.56);
  tl.to("#g7b", {scale: 1, duration: 0.26, ease: "power2.out"}, 31.74);
  // out before «Друге»
  tl.to("#g7", {autoAlpha: 0, duration: 0.20, ease: "power2.in"}, 31.86);'''
    return html, js


# ------------------------------------------------------- C · 2 · Fathom


@beat
def b08_fathom_slot():
    """«Друге Fathom, який записує наші дзвінки»"""
    js = '''
  tl.set("#gboard", {autoAlpha: 1}, 32.10);
  tl.to("#tl1", {autoAlpha: 1, duration: 0.20}, 32.30);
  gsap.set("#tl1", {scale: 0.8, transformOrigin: "50% 50%"});
  tl.to("#tl1", {scale: 1, duration: 0.34, ease: "back.out(2.4)"}, 32.30);
  tl.to("#gboard", {autoAlpha: 0, duration: 0.22, ease: "power2.in"}, 33.60);'''
    return "", js


@beat
def b09_wave_to_text():
    """«записує наші дзвінки» → «теж безкоштовний» → «ціла інструкція» →
    «зберігає одразу в тексті» → «щоб не переслуховувати»

    Rebuilt after her review: the waveform used to land at 35.6 and sit there,
    unchanged, until 39.7 — through two sentences it had nothing to do with.
    Her note was just "took too long too", and STYLE.md §4 already says a
    graphic must not outlive its sentence. It is now five short events on five
    phrases, and the 0 € badge comes back for «теж безкоштовний» because it is
    the same claim about a second product (§4, reuse objects).
    """
    bars_html = "".join('<i style="height:%dpx"></i>' % h for h in
                        [34, 72, 128, 96, 168, 62, 140, 104, 188, 76, 132, 54,
                         160, 92, 118, 44, 150, 86, 126, 60])
    html = '''
      <div class="g full" id="g9">
        <div class="wave" id="g9w" style="left:180px;top:250px;width:720px;
             height:200px;justify-content:center">%s</div>
        %s
        <div class="guide" id="g9g">
          <span class="gh"></span><b class="pr"></b><b class="pr"></b>
          <b class="pr"></b>
        </div>
        <div class="lines" id="g9t" style="left:230px;top:236px;width:620px">
          <b class="ph"></b>%s
        </div>
        <div class="scrub" id="g9s" style="left:230px;top:430px;width:620px">
          <span class="track"></span><span class="knob"></span>
          <span class="strike" id="g9x"></span>
        </div>
      </div>''' % (bars_html, freebadge("g9free"), bars(3))
    js = '''
  gsap.set("#g9", {autoAlpha: 0});
  gsap.set("#g9t, #g9s, #g9g", {autoAlpha: 0});
  gsap.set("#g9free", {autoAlpha: 0, scale: 0.5, transformOrigin: "50% 50%"});
  gsap.set("#g9w", {autoAlpha: 0});
  gsap.set("#g9w i", {scaleY: 0.15, transformOrigin: "50% 50%"});
  gsap.set("#g9x", {scaleX: 0, transformOrigin: "0% 50%"});
  tl.set("#g9", {autoAlpha: 1}, 33.76);

  // «наші дзвінки» — the call arrives as sound, and leaves again
  tl.to("#g9w", {autoAlpha: 1, duration: 0.12}, 33.84);
  tl.to("#g9w i", {scaleY: 1, duration: 0.34, ease: "back.out(2)",
                   stagger: {each: 0.014, from: "center"}}, 33.86);
  tl.to("#g9w", {autoAlpha: 0, duration: 0.20, ease: "power2.in"}, 34.36);

  // «теж безкоштовний» — the same badge as Cal.com, which is the joke
  tl.to("#g9free", {autoAlpha: 1, scale: 1, duration: 0.32,
                    ease: "back.out(2.8)"}, 34.58);
  tl.to("#g9free", {autoAlpha: 0, scale: 0.8, duration: 0.22,
                    ease: "power2.in"}, 35.70);

  // «ціла інструкція» — a guide, not a label
  tl.to("#g9g", {autoAlpha: 1, duration: 0.24}, 36.26);
  tl.from("#g9g .pr", {scaleX: 0, transformOrigin: "0% 50%", duration: 0.22,
                       stagger: 0.06, ease: "power2.out"}, 36.34);
  tl.to("#g9g", {autoAlpha: 0, duration: 0.22, ease: "power2.in"}, 37.44);

  // «зберігає записи» — sound again, briefly, so the morph has a before
  tl.to("#g9w", {autoAlpha: 1, duration: 0.14}, 37.72);
  tl.to("#g9w i", {scaleY: 1, duration: 0.26, ease: "power2.out",
                   stagger: {each: 0.010, from: "center"}}, 37.74);
  // «одразу в тексті» — and it resolves into lines
  tl.to("#g9w", {autoAlpha: 0, scaleY: 0.2, duration: 0.26,
                 ease: "power2.in"}, 39.60);
  tl.to("#g9t", {autoAlpha: 1, duration: 0.26, ease: "power2.out"}, 39.74);
  tl.from("#g9t .pr", {scaleX: 0, transformOrigin: "0% 50%", duration: 0.24,
                       stagger: 0.06, ease: "power2.out"}, 39.78);

  // «щоб не переслуховувати» — the replay is struck out
  tl.to("#g9s", {autoAlpha: 1, duration: 0.20}, 40.54);
  tl.to("#g9x", {scaleX: 1, duration: 0.24, ease: "power3.out"}, 40.86);
  tl.to("#g9", {autoAlpha: 0, duration: 0.26, ease: "power2.in"}, 41.80);'''
    return html, js


# ---------------------------------------------------------- D · 3 · CRM


@beat
def b10_crm_slot():
    """«Третє CRM»

    The tile carries the letters CRM, not a drawn database. Her note: "shitty
    icon, either do properly or write CRM". No CRM brand is named in the script
    (STYLE.md §5b), so type is the honest answer — the same call as RUTA.
    """
    js = '''
  tl.set("#gboard", {autoAlpha: 1}, 42.36);
  tl.to("#tl2", {autoAlpha: 1, duration: 0.20}, 42.52);
  gsap.set("#tl2", {scale: 0.8, transformOrigin: "50% 50%"});
  tl.to("#tl2", {scale: 1, duration: 0.34, ease: "back.out(2.4)"}, 42.52);
  tl.to("#gboard", {autoAlpha: 0, duration: 0.26, ease: "power2.in"}, 45.60);'''
    return "", js


@beat
def b11_fields_fill():
    """«хто ця людина, звідки прийшла, чим займається, що хотіла, що вже
    зроблено, який наступний крок»

    Her note: "the points could have been written out properly". They are now
    real rows in a real table rather than six blank pills — which STYLE.md §4
    allows explicitly, because this is text *inside a depicted interface*, and
    a CRM with no field names is not a depicted CRM.

    One row per word, on her timing, so the spacing stays uneven.
    """
    rows = ["ХТО", "ЗВІДКИ", "ЧИМ ЗАЙМАЄТЬСЯ", "ЩО ХОТІЛА",
            "ЩО ЗРОБЛЕНО", "НАСТУПНИЙ КРОК"]
    cells = "".join(
        '<div class="crow" id="g11c%d"><span class="dot"></span>'
        '<span class="lbl">%s</span></div>' % (i, r)
        for i, r in enumerate(rows))
    html = '''
      <div class="g full" id="g11">
        <div class="crm" id="g11r">%s</div>
      </div>''' % cells
    js = '''
  gsap.set("#g11", {autoAlpha: 0});
  gsap.set("#g11 .crow", {autoAlpha: 0, x: -40});
  tl.set("#g11", {autoAlpha: 1}, 48.40);
  [48.64, 49.18, 50.30, 51.12, 52.00, 53.24].forEach(function (t, i) {
    tl.to("#g11c" + i, {autoAlpha: 1, x: 0, duration: 0.26,
                        ease: "power3.out"}, t);
  });
  // «який наступний крок» is the only row that is a decision, so it is the
  // only one that takes the accent (§5a.4 — the accent appears once)
  tl.set("#g11c5", {backgroundImage:
        "linear-gradient(158deg, #c41434 0%, #8d0d24 100%)"}, 53.46);
  tl.set("#g11c5 .lbl", {color: "#ffffff"}, 53.46);
  tl.set("#g11c5 .dot", {backgroundColor: "#ffffff"}, 53.46);
  tl.fromTo("#g11c5", {scale: 0.97}, {scale: 1, duration: 0.26,
            ease: "back.out(3)", transformOrigin: "50% 50%"}, 53.46);
  tl.to("#g11", {autoAlpha: 0, duration: 0.28, ease: "power2.in"}, 54.40);'''
    return html, js


@beat
def b12_birthday():
    """«плюс дрібниці типу дня народження»

    The literal image, drawn rather than an emoji — there is no Apple emoji
    artwork on the machine and a Noto glyph would ship as the Android one
    (§5a.11). A cake is simple enough to draw honestly.
    """
    html = '''
      <div class="g full" id="g12">
        <div class="cake" id="g12c" style="left:428px;top:250px">
          <span class="flame"></span><span class="candle"></span>
          <span class="ice"></span><span class="body"></span>
        </div>
      </div>'''
    js = '''
  gsap.set("#g12", {autoAlpha: 0});
  gsap.set("#g12c", {autoAlpha: 0, scale: 0.4, y: -40, transformOrigin: "50% 100%"});
  tl.set("#g12", {autoAlpha: 1}, 55.06);
  tl.to("#g12c", {autoAlpha: 1, scale: 1, y: 0, duration: 0.40,
                  ease: "back.out(2.6)"}, 55.14);
  tl.to("#g12c .flame", {scaleY: 1.25, duration: 0.22, yoyo: true, repeat: 3,
                         transformOrigin: "50% 100%", ease: "sine.inOut"}, 55.56);
  tl.to("#g12", {autoAlpha: 0, duration: 0.26, ease: "power2.in"}, 57.10);'''
    return html, js


@beat
def b13_notion_on_crm():
    """«роблю це просто в Notion»"""
    js = '''
  tl.set("#gboard", {autoAlpha: 1}, 57.80);
  tl.to("#tl2 .tile.brand", {autoAlpha: 0, duration: 0.20}, 57.98);
  tl.to("#tl2notion", {autoAlpha: 1, scale: 1, duration: 0.34,
                       ease: "back.out(2.4)"}, 57.98);
  // no clear here: b14 brings the tasks tile in at 59.58 and the board simply
  // keeps accumulating.'''
    return "", js


# -------------------------------------------------------- E · 4 · tasks


@beat
def b14_tasks_slot():
    """«Четверте — система для задач»

    Her note: "literally one second wtf". It was, because her pull-out owns
    61.47–63.17 and the tile had to clear before it. So the tile now lands
    earlier, on «Четверте», and — more to the point — comes straight back at
    63.25 and stays for the rest of the section instead of flashing once.
    """
    js = '''
  tl.set("#gboard", {autoAlpha: 1}, 59.50);
  tl.to("#tl3", {autoAlpha: 1, duration: 0.20}, 59.58);
  gsap.set("#tl3", {scale: 0.8, transformOrigin: "50% 50%"});
  tl.to("#tl3", {scale: 1, duration: 0.34, ease: "back.out(2.4)"}, 59.58);
  // «система для задач» — the checklist writes itself in
  tl.from("#tlchk i", {autoAlpha: 0, x: -18, duration: 0.22, stagger: 0.10,
                       ease: "power2.out"}, 60.04);
  // down for her pull-out, and back the moment it ends
  tl.to("#gboard", {autoAlpha: 0, duration: 0.22, ease: "power2.in"}, 61.16);'''
    return "", js


@beat
def b15_forget_then_capture():
    """«а по факту ти дуже швидко почнеш все забувати» → «краще вибудувати це
    зараз»

    Three tasks evaporate unrecorded, then the same three land as checked rows.
    The same objects twice: forgetting and capturing are one gesture reversed.
    Clears for 67.27–68.10, her second hand punch-in.
    """
    rows = "".join(
        '<div class="task" id="g15t%d" style="left:%dpx;top:%dpx;width:%dpx">'
        '<span class="box"></span><span class="line"></span></div>'
        % (i, 190 + i * 26, 210 + i * 120, 700 - i * 52) for i in range(3))
    html = '<div class="g full" id="g15">%s</div>' % rows
    js = '''
  gsap.set("#g15", {autoAlpha: 0});
  gsap.set(".task", {autoAlpha: 0, y: 0, scale: 1});
  tl.set("#g15", {autoAlpha: 1}, 63.30);
  // they appear and drift off, unrecorded
  [63.34, 63.70, 64.06].forEach(function (t, i) {
    tl.to("#g15t" + i, {autoAlpha: 1, duration: 0.22, ease: "power2.out"}, t);
    tl.to("#g15t" + i, {autoAlpha: 0, y: -120, scale: 0.9, duration: 0.70,
                        ease: "power2.in"}, 65.34 + i * 0.10);
  });
  // «краще вибудувати це зараз» — the same three, kept this time
  [66.74, 66.92, 67.08].forEach(function (t, i) {
    tl.set("#g15t" + i, {y: 0, scale: 1}, t);
    tl.to("#g15t" + i, {autoAlpha: 1, duration: 0.20, ease: "back.out(2)"}, t);
  });
  tl.to("#g15 .task", {autoAlpha: 0, duration: 0.18}, 67.20);'''
    return html, js


@beat
def b16_notion_on_tasks():
    """«я тримаю задачі теж в Notion»

    The Notion mark returns — the second time the viewer sees it, which is the
    whole point of «теж».
    """
    js = '''
  tl.set("#gboard", {autoAlpha: 1}, 68.20);
  tl.to("#tl3 .tile.brand", {autoAlpha: 0, duration: 0.20}, 70.76);
  tl.to("#tl3notion", {autoAlpha: 1, scale: 1, duration: 0.34,
                       ease: "back.out(2.4)"}, 70.76);
  tl.to("#gboard", {autoAlpha: 0, duration: 0.26, ease: "power2.in"}, 72.40);'''
    return "", js


# ------------------------------------------------------ F · 5 · content


@beat
def b17_process_over_result():
    """«показати процес часом цікавіше, ніж готовий результат»

    The polished result shrinks; the messy process behind it grows past it.
    """
    html = '''
      <div class="g full" id="g17">
        <div class="cc" id="g17r" style="left:600px;top:200px">
          <b></b><b></b><b></b><b></b>
        </div>
        <div class="mess" id="g17p" style="left:170px;top:180px">
          <span></span><span></span><span></span><span></span><span></span>
        </div>
      </div>'''
    js = '''
  gsap.set("#g17", {autoAlpha: 0});
  gsap.set("#g17r", {autoAlpha: 0, scale: 0.86, transformOrigin: "50% 50%"});
  gsap.set("#g17p", {autoAlpha: 0, scale: 0.8, transformOrigin: "50% 50%"});
  tl.set("#g17", {autoAlpha: 1}, 76.50);
  tl.to("#g17p", {autoAlpha: 1, scale: 1, duration: 0.34, ease: "back.out(2.2)"}, 76.62);
  tl.to("#g17r", {autoAlpha: 1, scale: 1, duration: 0.30, ease: "back.out(2)"}, 78.60);
  // the finished thing is the smaller one
  tl.to("#g17r", {scale: 0.72, duration: 0.50, ease: "power2.inOut"}, 79.10);
  tl.to("#g17p", {scale: 1.14, duration: 0.50, ease: "power2.inOut"}, 79.10);
  tl.to("#g17", {autoAlpha: 0, duration: 0.28, ease: "power2.in"}, 80.20);'''
    return html, js


@beat
def b18_call_fans_out():
    """«один дзвінок з клієнткою» → «ідеї для контенту» → «написані словами
    твоєї цільової аудиторії» → «на вагу золота» → «перевикористовуємо»

    Her note on the old version: "too long". It was one object held for ten
    seconds across five different claims. Now the fan lands, the quote lifts
    out of it, the weight registers, and then the whole thing loops back — five
    events instead of one, and the frame clears between them.
    """
    fan = "".join(
        '<div class="cc" id="g18c%d" style="left:%dpx;top:250px">'
        '<b></b><b></b><b></b></div>' % (i, 120 + i * 225) for i in range(4))
    html = '''
      <div class="g full" id="g18">
        <div class="cc call" id="g18call" style="left:430px;top:250px">
          <b></b><b></b><b></b>
        </div>
        %s
        <span class="quote" id="g18q"></span>
        <svg id="g18loop" width="1080" height="600" viewBox="0 0 1080 600"
             style="position:absolute;left:0;top:0">
          <path id="g18arc" class="wire" stroke="#ff6e9c"
                d="M300 500 C 300 590, 780 590, 780 500"
                stroke-dasharray="520" stroke-dashoffset="520"
                marker-end="url(#g18head)"/>
          <defs><marker id="g18head" markerWidth="5" markerHeight="5" refX="2.5"
                        refY="2.5" orient="auto">
            <path d="M0 0 L5 2.5 L0 5 z" fill="#ff6e9c"/></marker></defs>
        </svg>
      </div>''' % fan
    js = '''
  gsap.set("#g18", {autoAlpha: 0});
  gsap.set("#g18call", {autoAlpha: 0, scale: 0.84, transformOrigin: "50% 50%"});
  gsap.set("#g18 .cc:not(.call)", {autoAlpha: 0, scale: 0.7, y: 0,
                                   transformOrigin: "50% 50%"});
  gsap.set("#g18q, #g18loop", {autoAlpha: 0});
  tl.set("#g18", {autoAlpha: 1}, 80.70);

  // «один дзвінок з клієнткою»
  tl.to("#g18call", {autoAlpha: 1, scale: 1, duration: 0.30,
                     ease: "back.out(2.4)"}, 80.78);
  // «це вже ідеї для контенту» — one call becomes four
  tl.to("#g18call", {autoAlpha: 0, duration: 0.22}, 82.28);
  [82.30, 82.44, 82.58, 82.74].forEach(function (t, i) {
    tl.to("#g18c" + i, {autoAlpha: 1, scale: 1, duration: 0.30,
                        ease: "back.out(2.2)"}, t);
  });
  // «написані словами твоєї цільової аудиторії» — her words lift out and land
  tl.fromTo("#g18q", {autoAlpha: 0, y: 60, scale: 0.8},
            {autoAlpha: 1, y: 0, scale: 1, duration: 0.32,
             ease: "back.out(2.6)"}, 83.46);
  tl.to("#g18q", {autoAlpha: 0, duration: 0.24, ease: "power2.in"}, 85.30);
  // «на вагу золота» — the fan has weight, and then it goes
  tl.to("#g18 .cc:not(.call)", {y: 40, duration: 0.34, ease: "power2.out",
                                stagger: 0.04}, 87.52);
  tl.to("#g18 .cc:not(.call)", {autoAlpha: 0, scale: 0.8, duration: 0.28,
                                ease: "power2.in", stagger: 0.03}, 88.30);

  // «те, що було на дзвінках, ми просто перевикористовуємо для контенту»
  // the call comes back and the arrow loops it into the content again
  tl.set("#g18call", {scale: 0.9, x: -190}, 89.02);
  tl.to("#g18call", {autoAlpha: 1, scale: 1, duration: 0.28,
                     ease: "back.out(2.4)"}, 89.04);
  tl.to("#g18loop", {autoAlpha: 1, duration: 0.16}, 90.32);
  tl.to("#g18arc", {strokeDashoffset: 0, duration: 0.60,
                    ease: "power2.inOut"}, 90.40);
  tl.set("#g18c1", {x: 190, y: 0}, 90.98);
  tl.to("#g18c1", {autoAlpha: 1, scale: 1, duration: 0.30,
                   ease: "back.out(2.4)"}, 91.00);
  tl.to("#g18", {autoAlpha: 0, duration: 0.30, ease: "power2.in"}, 92.10);'''
    return html, js


# --------------------------------------------------------- G · 6 · RUTA


@beat
def b19_ruta_slot():
    """«мій додаток "RUTA"»

    Her own product, set as type because there is no icon yet — her call,
    2026-09-14. It gets the glow the other tiles do not: it is the one thing on
    the board she is selling.
    """
    js = '''
  tl.set("#gboard", {autoAlpha: 1}, 95.70);
  tl.to("#tl4", {autoAlpha: 1, duration: 0.20}, 95.89);
  gsap.set("#tl4", {scale: 0.78, transformOrigin: "50% 50%"});
  tl.to("#tl4", {scale: 1, duration: 0.40, ease: "back.out(2.6)"}, 95.89);
  tl.to("#gboard", {autoAlpha: 0, duration: 0.24, ease: "power2.in"}, 96.70);'''
    return "", js


@beat
def b20_voice_to_three():
    """«на основі голосових створює рілси, сторіс і готові каруселі»

    One voice note splits into three outputs, one per word.
    """
    bars_html = "".join('<i style="height:%dpx"></i>' % h for h in
                        [30, 64, 108, 78, 130, 52, 96, 70, 118, 44])
    html = '''
      <div class="g full" id="g20">
        <div class="wave" id="g20w" style="left:400px;top:150px;width:280px;
             height:140px;justify-content:center">%s</div>
        <div class="cc" id="g20a" style="left:110px;top:330px"><b></b><b></b><b></b></div>
        <div class="cc" id="g20b" style="left:430px;top:330px"><b></b><b></b><b></b></div>
        <div class="cc" id="g20c" style="left:750px;top:330px"><b></b><b></b><b></b></div>
      </div>''' % bars_html
    js = '''
  gsap.set("#g20", {autoAlpha: 0});
  gsap.set("#g20w i", {scaleY: 0.2, transformOrigin: "50% 50%"});
  gsap.set("#g20a, #g20b, #g20c", {autoAlpha: 0, scale: 0.7, y: -60,
                                   transformOrigin: "50% 50%"});
  tl.set("#g20", {autoAlpha: 1}, 96.86);
  tl.to("#g20w i", {scaleY: 1, duration: 0.36, ease: "back.out(2)",
                    stagger: {each: 0.03, from: "center"}}, 96.94);
  [["#g20a", 97.82], ["#g20b", 98.32], ["#g20c", 99.14]].forEach(function (p) {
    tl.to(p[0], {autoAlpha: 1, scale: 1, y: 0, duration: 0.34,
                 ease: "back.out(2.4)"}, p[1]);
  });
  tl.to("#g20", {autoAlpha: 0, duration: 0.26, ease: "power2.in"}, 100.50);'''
    return html, js


@beat
def b21_ten_euro():
    """«коштує лише 10 євро на місяць» — a number is the one word §4 allows."""
    html = '''
      <div class="g full" id="g21">
        <div class="num" id="g21n" style="top:210px">10<small>€</small></div>
      </div>'''
    js = '''
  gsap.set("#g21", {autoAlpha: 0});
  gsap.set("#g21n", {autoAlpha: 0, scale: 0.6, transformOrigin: "50% 50%"});
  tl.set("#g21", {autoAlpha: 1}, 100.92);
  tl.to("#g21n", {autoAlpha: 1, scale: 1, duration: 0.36, ease: "back.out(2.8)"}, 101.00);
  tl.to("#g21", {autoAlpha: 0, duration: 0.24, ease: "power2.in"}, 102.30);'''
    return html, js


@beat
def b22_thousand_collapses():
    """«замінює тисячу промтів і підписок»

    A wall of small tiles collapses into the one RUTA tile. This is the big
    object of the reel, so it goes **behind her** — STYLE.md §1, matte this
    beat rather than shuffling it out of her way.
    """
    wall = "".join('<span class="wt" id="g22w%d"></span>' % i for i in range(121))
    html = '''
      <div class="g full" id="g22">
        <div class="wall" id="g22wall">%s</div>
        <div class="lit soft" id="g22lit"></div>
        <div class="tile brand one" id="g22one">
          <span class="wordmark big">RUTA</span>
        </div>
      </div>''' % wall
    js = '''
  gsap.set("#g22", {autoAlpha: 0});
  gsap.set("#g22 .wt", {autoAlpha: 0, scale: 0.5, transformOrigin: "50% 50%"});
  gsap.set("#g22one, #g22lit", {autoAlpha: 0, scale: 0.6,
                                transformOrigin: "50% 50%"});
  tl.set("#g22", {autoAlpha: 1}, 102.66);
  tl.to("#g22 .wt", {autoAlpha: 1, scale: 1, duration: 0.40, ease: "back.out(1.8)",
                     stagger: {each: 0.008, from: "random"}}, 102.76);
  // «і підписок» — and then all of it folds into the one thing
  tl.to("#g22 .wt", {autoAlpha: 0, scale: 0.2, x: 0, y: 0, duration: 0.52,
                     ease: "power3.in", stagger: {each: 0.006, from: "edges"}}, 103.90);
  tl.to("#g22one, #g22lit", {autoAlpha: 1, scale: 1, duration: 0.44,
                             ease: "back.out(2.2)"}, 104.36);
  tl.to("#g22", {autoAlpha: 0, duration: 0.30, ease: "power2.in"}, 106.40);'''
    return html, js


# The one matte in this reel (STYLE.md §1). The wall runs y 60-1050, so it
# crosses her shoulders and head; without it the wall would be stuck to her
# face instead of passing behind her. 118 frames, 8 min of CPU, spent once.
k.matte("wall", 102.600, 3.933)


@beat
def b23_fallback():
    """«якщо це забагато — просто візьми Notion для планування і штучний
    інтелект для стратегії»

    The cheap version of the same thing: two tiles instead of the app.
    """
    html = '''
      <div class="g full" id="g23">
        <div class="tile brand pair" id="g23a" style="left:180px;top:220px">
          %s
        </div>
        <div class="tile brand pair" id="g23b" style="left:610px;top:220px">
          %s
        </div>
      </div>''' % (logo("notion-mark"), logo("claude-tile"))
    js = '''
  gsap.set("#g23", {autoAlpha: 0});
  gsap.set("#g23a, #g23b", {autoAlpha: 0, scale: 0.78, transformOrigin: "50% 50%"});
  tl.set("#g23", {autoAlpha: 1}, 108.00);
  tl.to("#g23a", {autoAlpha: 1, scale: 1, duration: 0.34, ease: "back.out(2.4)"}, 108.12);
  tl.to("#g23b", {autoAlpha: 1, scale: 1, duration: 0.34, ease: "back.out(2.4)"}, 110.14);
  tl.to("#g23", {autoAlpha: 0, duration: 0.28, ease: "power2.in"}, 111.30);'''
    return html, js


# ------------------------------------------------- H · the command centre


@beat
def b24_hub_slot():
    """«найважливіше — наш командний центр… це Клод або GPT»

    The last slot. GPT sits beside it as the stated alternative, smaller,
    because she says she took Claude.
    """
    html = '''
      <div class="g full" id="g24">
        <div class="alt" id="g24gpt" style="left:760px;top:300px">%s</div>
      </div>''' % logo("gpt-mark")
    js = '''
  tl.set("#gboard", {autoAlpha: 1}, 111.00);
  gsap.set("#g24", {autoAlpha: 0});
  gsap.set("#g24gpt", {autoAlpha: 0, scale: 0.7, transformOrigin: "50% 50%"});
  // «командний центр»
  tl.to("#tl5", {autoAlpha: 1, duration: 0.20}, 112.60);
  gsap.set("#tl5", {scale: 0.78, transformOrigin: "50% 50%"});
  tl.to("#tl5", {scale: 1, duration: 0.40, ease: "back.out(2.6)"}, 112.60);
  // «або GPT» — the alternative, named and set aside
  tl.set("#g24", {autoAlpha: 1}, 115.50);
  tl.to("#g24gpt", {autoAlpha: 1, scale: 1, duration: 0.30, ease: "back.out(2.2)"}, 115.56);
  tl.to("#g24gpt", {autoAlpha: 0.25, scale: 0.86, duration: 0.40,
                    ease: "power2.out"}, 116.88);
  tl.to("#g24", {autoAlpha: 0, duration: 0.26}, 117.80);'''
    return html, js


@beat
def b25_four_panes():
    """«екосистема між чатом, коворком, дизайном і кодом»

    Four panes, one per word, 0.4 s apart — her spacing, so they land uneven.
    Frosted over her kitchen (§5a.9), which is the house look.
    """
    panes = "".join(
        '<div class="pane" id="g25p%d" style="left:%dpx;top:%dpx">'
        '<b></b><b></b><b></b></div>'
        % (i, [96, 784, 96, 784][i], [120, 120, 372, 372][i]) for i in range(4))
    html = ('<div class="g full" id="g25">%s'
            '<div class="tile brand hub" id="g25hub">%s</div></div>'
            % (panes, logo("claude-tile")))
    js = '''
  gsap.set("#g25", {autoAlpha: 0});
  gsap.set("#g25 .pane", {autoAlpha: 0, scale: 0.72, transformOrigin: "50% 50%"});
  // the board steps aside: these four panes are what is *inside* the hub
  tl.to("#gboard", {autoAlpha: 0, duration: 0.26, ease: "power2.in"}, 118.80);
  tl.set("#g25", {autoAlpha: 1}, 119.10);
  gsap.set("#g25hub", {autoAlpha: 0, scale: 0.8, transformOrigin: "50% 50%"});
  tl.to("#g25hub", {autoAlpha: 1, scale: 1, duration: 0.30,
                    ease: "back.out(2.4)"}, 119.10);
  [119.18, 119.60, 120.04, 120.54].forEach(function (t, i) {
    tl.to("#g25p" + i, {autoAlpha: 1, scale: 1, duration: 0.28,
                        ease: "back.out(2.6)"}, t);
  });
  tl.to("#g25", {autoAlpha: 0, duration: 0.28, ease: "power2.in"}, 122.00);'''
    return html, js


@beat
def b26_twenty_euro():
    """«почати можна з тарифу за 20 євро»"""
    html = '''
      <div class="g full" id="g26">
        <div class="num" id="g26n" style="top:210px">20<small>€</small></div>
      </div>'''
    js = '''
  gsap.set("#g26", {autoAlpha: 0});
  gsap.set("#g26n", {autoAlpha: 0, scale: 0.6, transformOrigin: "50% 50%"});
  tl.set("#g26", {autoAlpha: 1}, 122.34);
  // and the board stays down until the payoff at 126.6
  tl.to("#g26n", {autoAlpha: 1, scale: 1, duration: 0.36, ease: "back.out(2.8)"}, 122.42);
  tl.to("#g26", {autoAlpha: 0, duration: 0.24, ease: "power2.in"}, 123.90);'''
    return html, js


@beat
def b27_board_wires_up():
    """«це найбільша витрата з усіх систем, але вона того варта»

    The payoff: all six tiles are on the board at once for the first time, and
    they wire into the hub. This is the biggest object in the reel and it is
    full width, so she is matted and it passes **behind** her (STYLE.md §1).

    NB she cut the script's ending here — «саме вона перевела мене з людини,
    яка все робить руками…» is not in the delivered audio, so there is no
    hands-to-head beat and this one carries the section alone.
    """
    html = '''
      <div class="g full" id="g27">
        <svg width="1080" height="600" viewBox="0 0 1080 600"
             style="position:absolute;left:0;top:0">
          <!-- Board: left 60, top 36, tiles 293x240, gutters 40. Column
               centres 206/540/873; the row gutter is y 276-316, so a bus at
               y=296 with stubs to the tile edges never crosses a tile face. -->
          <g id="g27wires" stroke="#ff6e9c" fill="none" stroke-width="15"
             stroke-linecap="round">
            <path d="M206 296 H873" stroke-dasharray="667" stroke-dashoffset="667"/>
            <path d="M206 276 V296" stroke-dasharray="20" stroke-dashoffset="20"/>
            <path d="M540 276 V296" stroke-dasharray="20" stroke-dashoffset="20"/>
            <path d="M873 276 V296" stroke-dasharray="20" stroke-dashoffset="20"/>
            <path d="M206 316 V296" stroke-dasharray="20" stroke-dashoffset="20"/>
            <path d="M540 316 V296" stroke-dasharray="20" stroke-dashoffset="20"/>
            <path d="M873 316 V296" stroke-dasharray="20" stroke-dashoffset="20"/>
          </g>
          <circle id="g27hub" cx="873" cy="296" r="17" fill="#ff6e9c"/>
        </svg>
      </div>'''
    js = '''
  gsap.set("#g27", {autoAlpha: 0});
  tl.set("#gboard", {autoAlpha: 1}, 126.60);
  [0,1,2,3,4,5].forEach(function (i) {
    tl.to("#tl" + i, {autoAlpha: 1, scale: 1, duration: 0.24,
                      ease: "back.out(2.2)"}, 126.68 + i * 0.06);
  });
  // the two tiles whose faces were swapped for Notion come back as Notion,
  // not as the database and the checklist they started as
  tl.to("#tl2notion, #tl3notion", {autoAlpha: 1, scale: 1, duration: 0.24}, 126.70);
  gsap.set("#g27hub", {autoAlpha: 0, scale: 0, transformOrigin: "873px 296px"});
  tl.set("#g27", {autoAlpha: 1}, 127.40);
  tl.to("#g27wires path", {strokeDashoffset: 0, duration: 0.60,
                           ease: "power2.out", stagger: 0.05}, 127.46);
  tl.to("#g27hub", {autoAlpha: 1, scale: 1, duration: 0.26,
                    ease: "back.out(3)"}, 128.10);
  tl.to("#tl5", {scale: 1.1, duration: 0.34, ease: "back.out(2.6)"}, 128.60);
  tl.to("#g27, #gboard", {autoAlpha: 0, duration: 0.34, ease: "power2.in"}, 129.70);'''
    return html, js


@beat
def b28_send_it():
    """«відправ цей рілс подружці, якій час масштабуватися»

    Low over her chest, not over her face — she leans into the lens for the
    CTA and that shot is hers (STYLE.md §3, her note on reel 3 v2).
    """
    html = '''
      <div class="g full" id="g28">
        <svg id="g28s" width="260" height="260" viewBox="0 0 100 100"
             style="position:absolute;left:410px;top:1180px">
          <path d="M8 50 L92 12 L64 92 L50 60 Z" fill="#ff6e9c"
                stroke="#fff" stroke-width="5" stroke-linejoin="round"/>
        </svg>
      </div>'''
    js = '''
  gsap.set("#g28", {autoAlpha: 0});
  gsap.set("#g28s", {autoAlpha: 0, scale: 0.5, rotation: -18,
                     transformOrigin: "50% 50%"});
  tl.set("#g28", {autoAlpha: 1}, 130.20);
  tl.to("#g28s", {autoAlpha: 1, scale: 1, rotation: 0, duration: 0.36,
                  ease: "back.out(2.6)"}, 130.30);
  // «масштабуватися» — and it leaves
  tl.to("#g28s", {x: 620, y: -180, rotation: 16, autoAlpha: 0, duration: 0.70,
                  ease: "power2.in"}, 132.20);'''
    return html, js


k.css("""
    /* b03 — the three things you stop knowing */
    .lost { position: absolute; left: 0; width: 1080px; text-align: center;
            top: 250px; }
    .lost .arrowin, .lost .coin, .lost .head {
        display: inline-block; filter: var(--cast); }
    .lost .arrowin { width: 190px; height: 190px; border-radius: 50%;
                     background: var(--lit-accent); box-shadow: var(--rim-dark);
                     clip-path: polygon(50% 0, 100% 55%, 74% 55%, 74% 100%,
                                        26% 100%, 26% 55%, 0 55%); }
    .lost .coin { width: 190px; height: 190px; border-radius: 50%;
                  background: var(--lit-pink); box-shadow: var(--rim-dark); }
    .lost .head { width: 170px; height: 190px; border-radius: 86px 86px 44px 44px;
                  background: var(--lit); box-shadow: var(--rim); }

    /* b09 — transcript lines and the replay that is struck out.
       The kit's .pr is graphite at 13% alpha, which is built for a light card
       ground and is simply not there over her kitchen: the first snapshot pass
       showed a heading bar and nothing under it. Over footage the body bars
       have to carry their own light. */
    .lines { position: absolute; }
    .lines .pr { background: rgba(255,255,255,0.88); box-shadow: var(--rim);
                 height: 34px; }
    .scrub { position: absolute; height: 40px; }
    .scrub .track { position: absolute; left: 0; top: 14px; width: 100%;
                    height: 14px; border-radius: 7px;
                    background: rgba(255,255,255,0.30); }
    .scrub .knob { position: absolute; left: 132px; top: 0; width: 40px;
                   height: 40px; border-radius: 50%; background: #fff;
                   box-shadow: 0 6px 16px rgba(8,6,12,0.4); }
    .scrub .strike { position: absolute; left: 0; top: 14px; width: 100%;
                     height: 14px; border-radius: 7px; background: var(--accent);
                     transform: rotate(-6deg); transform-origin: 0 50%; }

    /* b12 — a cake, drawn */
    .cake { position: absolute; width: 300px; height: 282px;
            transform-origin: 50% 100%; }
    .cake .body { position: absolute; left: 0; bottom: 0; width: 300px;
                  height: 140px; border-radius: 26px; background: var(--lit-accent);
                  box-shadow: var(--rim-dark); }
    .cake .ice { position: absolute; left: 8px; bottom: 124px; width: 284px;
                 height: 62px; border-radius: 24px; background: var(--lit-blush);
                 box-shadow: var(--rim); }
    .cake .candle { position: absolute; left: 140px; bottom: 178px; width: 20px;
                    height: 68px; border-radius: 8px; background: var(--lit-pink); }
    .cake .flame { position: absolute; left: 134px; bottom: 240px; width: 32px;
                   height: 44px; border-radius: 12px 12px 12px 12px / 18px 18px 12px 12px;
                   background: #ffd9a0;
                   filter: drop-shadow(0 0 18px rgba(255,196,218,0.95))
                           drop-shadow(0 0 40px rgba(255,110,156,0.7)); }

    /* b13 / b16 — the Notion mark, dropped onto a tile that already exists */
    .ontile { position: absolute; inset: 0; opacity: 0; visibility: hidden;
              transform: scale(0.8); }

    /* b15 — the checklist inside the board tile. Her note: "tasks are always
       checks and lines like a checklist", so that is what it is. */
    .chk { display: grid; gap: 16px; }
    .chk i { display: flex; align-items: center; gap: 14px; }
    .chk i b { display: block; width: 30px; height: 30px; border-radius: 9px;
               flex: none; background: var(--lit-accent);
               box-shadow: var(--rim-dark); }
    .chk i s { display: block; height: 16px; border-radius: 8px;
               background: var(--graphite); }
    .chk i:nth-child(1) s { width: 132px; }
    .chk i:nth-child(2) s { width: 104px; }
    .chk i:nth-child(3) s { width: 120px; }
    .ghost .chk i b { background: rgba(255,255,255,0.85); box-shadow: none; }
    .ghost .chk i s { background: rgba(255,255,255,0.55); }

    /* b17 — process vs result */
    .mess { position: absolute; width: 320px; height: 340px; }
    .mess span { position: absolute; border-radius: 22px;
                 background: var(--lit-blush); box-shadow: var(--rim);
                 filter: var(--cast-sm); }
    .mess span:nth-child(1) { left: 0;   top: 20px;  width: 190px; height: 90px;
                              transform: rotate(-4deg); }
    .mess span:nth-child(2) { left: 120px; top: 96px; width: 200px; height: 84px;
                              transform: rotate(3deg); }
    .mess span:nth-child(3) { left: 10px; top: 180px; width: 170px; height: 96px;
                              transform: rotate(2deg); }
    .mess span:nth-child(4) { left: 150px; top: 240px; width: 160px; height: 80px;
                              transform: rotate(-5deg); }
    .mess span:nth-child(5) { left: 60px;  top: 0;    width: 120px; height: 70px;
                              transform: rotate(6deg); }

    /* b18 — the quote that lifts out of the call */
    .cc.call { background: var(--lit-accent); }
    .cc.call b { background: rgba(255,255,255,0.5); }
    .cc.call b:first-child { background: #fff; }
    .quote { position: absolute; left: 330px; top: 170px; width: 420px;
             height: 120px; border-radius: 34px; background: var(--lit-pink);
             box-shadow: var(--rim-dark); filter: var(--cast); }

    /* b22 — a thousand of them, then one */
    /* 11 x 11 at 74px + 16px gap = y 60-1050: past her shoulders, which is
       the point — it goes behind her rather than stopping politely above. */
    .wall { position: absolute; left: 40px; top: 60px; width: 1000px;
            display: grid; gap: 16px; grid-template-columns: repeat(11, 1fr); }
    .wall .wt { display: block; height: 74px; border-radius: 18px;
                background: rgba(255,255,255,0.62); box-shadow: var(--rim);
                filter: var(--cast-sm); }
    .tile.brand.one { position: absolute; left: 330px; top: 190px; width: 420px;
                      height: 260px; display: grid; place-items: center; }
    #g22lit { position: absolute; left: 330px; top: 190px; width: 420px;
              height: 260px; inset: auto; }

    /* b07 — the booking that travels the wire */
    .pip { position: absolute; left: 0; top: 0; width: 28px; height: 28px;
           border-radius: 50%; background: #fff;
           filter: drop-shadow(0 0 14px rgba(255,196,218,0.95))
                   drop-shadow(0 0 34px rgba(255,110,156,0.8)); }

    /* b23 — the cheap pair */
    .tile.brand.pair { width: 290px; height: 290px; }

    /* «безкоштовний» — 0 euro, reused for Cal.com and for Fathom */
    .freewrap { position: absolute; left: 470px; top: 190px; width: 300px;
                height: 300px; }
    .free { position: absolute; inset: 0; display: grid; place-items: center;
            grid-auto-flow: column; gap: 4px; border-radius: 50%;
            background: var(--lit-accent); box-shadow: var(--rim-dark); }
    .free span { font-size: 168px; font-weight: 900; color: #fff;
                 letter-spacing: -0.06em; line-height: 1; }
    .free small { font-size: 76px; font-weight: 900; color: #fff;
                  align-self: center; }

    /* b07 — the booking that crosses the wire. It was a glowing dot and she
       could not tell what it was; an object with a header and a body reads as
       an appointment even at 80px. */
    .event { position: absolute; left: 0; top: 0; width: 92px; height: 74px;
             border-radius: 18px; background: var(--lit); box-shadow: var(--rim);
             filter: drop-shadow(0 0 18px rgba(255,110,156,0.85));
             padding: 12px 12px 0; }
    .event b { display: block; height: 14px; border-radius: 7px;
               background: var(--accent); margin-bottom: 9px; }
    .event s { display: block; height: 9px; border-radius: 5px; width: 74%;
               background: var(--graphite); }

    /* b09 — «ціла інструкція» */
    .guide { position: absolute; left: 330px; top: 190px; width: 420px;
             height: 300px; padding: 34px; background: var(--lit-blush);
             box-shadow: var(--rim); filter: var(--cast); border-radius: 44px; }
    .guide .gh { display: block; height: 46px; width: 62%; border-radius: 14px;
                 background: var(--lit-accent); margin-bottom: 26px;
                 box-shadow: var(--rim-dark); }
    .guide .pr { background: rgba(23,20,28,0.16); }

    /* b11 — the CRM, with its fields actually named */
    .crm { position: absolute; left: 90px; top: 40px; width: 900px;
           display: grid; gap: 12px; }
    .crow { display: flex; align-items: center; gap: 22px; height: 74px;
            padding: 0 28px; border-radius: 24px;
            background: linear-gradient(158deg, rgba(255,255,255,0.93) 0%,
                        rgba(253,241,244,0.93) 100%);
            box-shadow: var(--rim); filter: var(--cast-sm); }
    .crow .dot { width: 22px; height: 22px; border-radius: 50%; flex: none;
                 background: var(--accent); }
    .crow .lbl { font-size: 42px; font-weight: 900; color: var(--ink);
                 letter-spacing: -0.02em; white-space: nowrap; }

    /* b25 — the hub the four panes belong to */
    .tile.brand.hub { position: absolute; left: 440px; top: 218px;
                      width: 200px; height: 200px; display: grid;
                      place-items: center; }

    /* b24 — the alternative she did not take */
    .alt { position: absolute; width: 180px; height: 180px; border-radius: 46px;
           background: var(--lit); box-shadow: var(--rim); filter: var(--cast);
           display: grid; place-items: center; }
    .alt .mk { width: 58%; }
""")

for _sel, _w, _h, _r in [
    (".tile.brand.one", 420, 260, 62),
    (".tile.brand.pair", 290, 290, 70),
    (".tile.brand.hub", 200, 200, 50),
]:
    k.squircle(_sel, _w, _h, _r)


def main():
    caps = k.load_captions(os.path.join(ROOT, "work", "r07", "captions.json"))
    gh, gj = [board_html()], []
    for fn in BEATS:
        h, j = fn()
        if h.strip():
            gh.append(h.rstrip())
        gj.append("  /* %s */" % fn.__name__)
        gj.append(j.rstrip())

    # The two Notion marks live inside tiles that already exist, so they are
    # appended to those tiles rather than being beats of their own.
    extra = ('\n      <div class="g full" id="gnotion"></div>')

    doc = k.document(
        title="Reel 7 — системи",
        plate="assets/base.mp4",
        gfx_html="\n".join(gh) + extra,
        gfx_js="\n".join(gj),
        caps=caps,
    )
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "index.html")
    io.open(out, "w", encoding="utf-8").write(doc)
    print("index.html  %d captions, %d beats, %.1f KB"
          % (len(caps), len(BEATS), os.path.getsize(out) / 1024.0))


main()
