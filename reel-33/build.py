# -*- coding: utf-8 -*-
"""Reel 33 — «Жодної втраченої клієнтки в дірект». Posts 2026-10-14.

Raw take cut by tools/cut.py (last take wins, one closeup on her sung
«Тадааам» — captions only there). Refined glass (STYLE.md §0), sound design.

The one object is **an unanswered chat**. It hangs off a client, gets lost in
a flood of messages, is read by her routine through SendPulse, turns into a
task, gets a ready script, waits at her for approval, and only then goes out.

Chain:  near: three clients, each with a DM; the DMs fall away unseen; the
clients fold into Instagram and Telegram -> OVER: the iris opens out of
Telegram: her inbox, new chats flood in on top and push the unread ones out
of sight; an eye-off lands -> the iris closes onto the routine tile -> near:
the routine, Instagram + Telegram cabled through SendPulse -> SendPulse
deals out the unanswered chats, each flips into a task (checkbox + lines),
assigned to her / the team -> *closeup «Тадааам», clear* -> OVER: the iris
opens on the scripts sheet: three ghost rows light up on their words ->
the iris closes onto row 1 -> near: a DM comes in, the reply is typed from
that script -> the reply heads to the client and stops at her -> it opens
into an approval card, her cursor taps «Затвердити», it flies -> a bot
wanders off on its own and is struck out -> Стежити.

usage: python build.py   (then: python ../tools/sfx.py mix 33)
"""
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))
from kit import Kit  # noqa: E402
from glass import Glass  # noqa: E402

CUT = json.load(io.open(os.path.join(ROOT, "work", "r33", "cut.json"), encoding="utf-8"))
DUR = 41.216           # (1237 plate frames - 0.5) / 30, floored
FPS = 30
k = Kit(width=1080, height=1920, fps=FPS, duration=DUR)
g = Glass(["instagram", "telegram", "sendpulse"])
k.css(g.css())

NO_PAINT = [tuple(x) for x in CUT["no_paint"]]          # [(20.3, 21.167)] — «Тадааам»

CAPS = k.load_captions(os.path.join(ROOT, "work", "r33", "captions.json"))
# whisper heard «Сенпульс» and «здачу»; the script says SendPulse and задачу
FIX = {u"Сенпульс.": u"SendPulse.", u"Сенпульс": u"SendPulse", u"здачу": u"задачу"}
for c in CAPS:
    c["w"] = FIX.get(c["w"], c["w"])
for _a, _b in zip(CAPS, CAPS[1:]):
    _a["e"] = round(max(_a["s"] + 0.10, _b["s"] - 0.085), 3)


def _n(s):
    return "".join(ch for ch in s.lower() if ch.isalnum())


def S(word, near):
    hits = [c for c in CAPS if _n(word) in [_n(x) for x in c["w"].split()]]
    c = min(hits, key=lambda c: abs(c["s"] - near))
    assert abs(c["s"] - near) < 0.6, (word, near, c["s"])
    return c["s"]


def E(word, near):
    hits = [c for c in CAPS if _n(word) in [_n(x) for x in c["w"].split()]]
    return min(hits, key=lambda c: abs(c["s"] - near))["e"]


T = {
    "pratsiuvav": S(u"працював", 0.43), "znaie": S(u"знає", 1.47), "odna": S(u"одна", 2.01),
    "problem": S(u"проблем", 3.01), "propusk": S(u"пропускала", 4.13), "insta": S(u"інстаграмі", 5.37),
    "tele": S(u"телеграмі", 5.95), "roboty": S(u"роботи", 6.68), "povidomlen": S(u"повідомлень", 7.60),
    "bilshe": S(u"більше", 8.38), "chaty": S(u"чати", 9.08), "khov": S(u"ховаються", 9.30),
    "khove": E(u"ховаються", 9.30), "prosto": S(u"просто", 10.10), "pomich": S(u"помічаю", 10.56),
    "tomu": S(u"Тому", 11.39), "zrobyla": S(u"зробила", 11.75), "rutynu": S(u"рутину", 12.09),
    "chytaie": S(u"читає", 13.15), "ig": S("Instagram", 13.47), "tg": S("Telegram", 13.97),
    "cherez": S(u"через", 14.47), "sp": S("SendPulse", 15.03), "spe": E("SendPulse", 15.03),
    "kozhen": S(u"Кожен", 16.01), "chat": S(u"чат", 16.41), "nikhto": S(u"ніхто", 16.97),
    "vidpoviv": S(u"відповів", 17.49), "peretv": S(u"перетворюється", 18.09), "zadachu": S(u"задачу", 18.69),
    "meni": S(u"мені", 19.07), "abo": S(u"або", 19.43), "komandi": S(u"команді", 19.71),
    "a": S(u"А", 21.17), "typovykh": S(u"типових", 21.53), "hotovi": S(u"готові", 22.80),
    "skrypty": S(u"скрипти", 23.28), "zapys": S(u"записатись", 23.84), "pidtv": S(u"підтвердити", 24.94),
    "nadisl": S(u"надіслати", 25.95), "ofer": S(u"офер", 26.39), "ofere": E(u"офер", 26.39),
    "tobto": S(u"Тобто", 27.03), "rutynni": S(u"рутинні", 27.37), "vono": S(u"воно", 28.29),
    "vidpovisty": S(u"відповісти", 28.73), "same": S(u"саме", 29.29), "hotovomu": S(u"готовому", 29.81),
    "stsen": S(u"сценарію", 30.23), "i": S(u"І", 31.03), "klientsi": S(u"клієнтці", 31.87),
    "nichoho": S(u"нічого", 32.59), "yde": S(u"йде", 33.29), "bez": S(u"без", 33.45),
    "mene": S(u"мене", 33.69), "shcho": S(u"Що", 34.25), "vidpravl": S(u"відправляється", 34.69),
    "zatv": S(u"затверджую", 35.87), "zatve": E(u"затверджую", 35.87), "sama": S(u"сама", 36.57),
    "tse": S(u"це", 36.99), "bot": S(u"бот", 37.35), "zhyve": S(u"живе", 37.79),
    "zhyttiam": S(u"життям", 38.31), "dyrekti": S(u"директі", 38.91), "dyrektie": E(u"директі", 38.91),
    "yakshcho": S(u"Якщо", 39.60), "tsikavo": S(u"цікаво", 40.08), "pidpysh": S(u"підпишись", 40.56),
    "dur": DUR,
}


def js(src, **extra):
    """`@name`, `@name+0.12`, `@name-0.1` -> one literal time."""
    vals = dict(T)
    vals.update(extra)

    def rep(m):
        v = vals[m.group(1)] + (float(m.group(2)) if m.group(2) else 0.0)
        return "%.3f" % v
    return re.sub(r"@(\w+)([+-]\d+(?:\.\d+)?)?", rep, src)


# ---------------------------------------------------------------------------
# Sound design (tools/sfx.py). Quiet, on the event, never on her closeup.
SFX = []


def sfx(name, t, db=0):
    if isinstance(t, str):
        t = float(js(t))
    SFX.append({"t": round(max(0.0, t), 3), "name": name, "db": db})


# ---------------------------------------------------------------------------
# Glyphs (24 grid, stroked)
STROKES = {
    "person": '<circle cx="12" cy="8.2" r="3.6"/><path d="M4.8 20c.9-3.8 3.7-5.8 7.2-5.8s6.3 2 7.2 5.8"/>',
    "team": '<circle cx="9" cy="8.6" r="3.2"/><path d="M3 19.6c.7-3.3 3-5 6-5s5.3 1.7 6 5"/>'
            '<circle cx="16.6" cy="7.4" r="2.6"/><path d="M16.2 12.4c2.6 0 4.4 1.6 5 4.6"/>',
    "check": '<path d="M5.4 12.6l4.3 4.3 8.9-9.5"/>',
    "loop": '<path d="M4.2 11.2a7.9 7.9 0 0 1 13.6-4.6L20 8.8M20 4v4.8h-4.8"/>'
            '<path d="M19.8 12.8a7.9 7.9 0 0 1-13.6 4.6L4 15.2M4 20v-4.8h4.8"/>',
    "eyeoff": '<path d="M2.8 12s3.4-6.4 9.2-6.4 9.2 6.4 9.2 6.4-3.4 6.4-9.2 6.4S2.8 12 2.8 12z"/>'
              '<circle cx="12" cy="12" r="2.9"/><path d="M4 3.6l16 16.8"/>',
    "doc": '<path d="M6 2.8h8.2l4 4V21.2H6z"/><path d="M14 2.8v4.2h4.2M9 12h6.2M9 15.4h6.2M9 18.8h3.6"/>',
    "calplus": '<rect x="3.4" y="5" width="17.2" height="15.6" rx="3"/><path d="M3.4 10h17.2M8 3v4M16 3v4"/>'
               '<path d="M12 12.6v5.4M9.3 15.3h5.4"/>',
    "calcheck": '<rect x="3.4" y="5" width="17.2" height="15.6" rx="3"/><path d="M3.4 10h17.2M8 3v4M16 3v4"/>'
                '<path d="M8.9 15.2l2.2 2.3 4.1-4.4"/>',
    "send": '<path d="M21 3L10.2 13.8"/><path d="M21 3l-6.6 18-4.2-7.2L3 9.6z"/>',
    "bot": '<rect x="4" y="8.4" width="16" height="11.6" rx="3.6"/><path d="M12 4.6v3.8"/>'
           '<circle cx="12" cy="3.6" r="1.1"/><circle cx="9.2" cy="13.6" r="1.2"/><circle cx="14.8" cy="13.6" r="1.2"/>'
           '<path d="M9.6 17h4.8M1.8 12.6v3.4M22.2 12.6v3.4"/>',
}
CURSOR = ('<svg viewBox="0 0 24 24" width="64" height="64"><path d="M4.2 2.8l14.6 8.1-6.3 1.5-3.1 5.9z" '
          'fill="#fff" stroke="#17141c" stroke-width="1.6" stroke-linejoin="round"/></svg>')


def stroke(name, cls="sk", style=""):
    return '<svg class="%s" viewBox="0 0 24 24"%s>%s</svg>' % (
        cls, (' style="%s"' % style) if style else "", STROKES[name])


def tile(tid, size, x, y, material, inner, extra_cls="", hide=True, ring=True):
    r = ('<div class="sqring%s" id="%sR" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx"></div>'
         % (" rnd" if "circ" in extra_cls else "", tid, x, y, size, size)) if ring else ""
    return ('%s<div class="tw%s %s" id="%s" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx">'
            '<div class="%s">%s<div class="sheen"></div></div></div>'
            % (r, " hide" if hide else "", extra_cls, tid, x, y, size, size, material, inner))


def face(fid, size, x, y, hide=True):
    """Her own face in a round tile (assets/avatar.jpg, a still of her)."""
    return ('<div class="tw circ%s" id="%s" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx">'
            '<div class="me"></div></div>' % (" hide" if hide else "", fid, x, y, size, size))


k.css("""
.abs { position: absolute; }
.hide { opacity: 0; visibility: hidden; }
.tw { position: absolute; }
.sk { fill: none; stroke: url(#gw); stroke-width: 2.3; stroke-linecap: round; stroke-linejoin: round;
  width: 50%; height: 50%; position: relative; z-index: 1; overflow: visible; }
.pearl .sk { stroke: #17141c; }
.clear { overflow: hidden; }
.circ .jelly, .circ .pearl, .circ .clear, .circ .sheen { border-radius: 50%; }
.sqring.rnd { border-radius: 50%; }
.me { position: absolute; inset: 0; border-radius: 50%;
  background: url("assets/avatar.jpg") center / cover no-repeat;
  box-shadow: 0 0 0 5px rgba(255,255,255,0.92), 0 26px 50px -18px rgba(24,4,12,0.6); }
.aurs { position: absolute; left: -700px; top: -700px; width: 2480px; height: 3320px; pointer-events: none;
  background:
    radial-gradient(circle 526px at 1560px 880px, rgba(255,110,156,0.50), rgba(255,110,156,0)),
    radial-gradient(circle 634px at 760px 2360px, rgba(222,32,74,0.55), rgba(222,32,74,0)),
    radial-gradient(circle 382px at 1480px 1910px, rgba(255,198,214,0.20), rgba(255,198,214,0)); }

/* the unread dot: Instagram's blue dot, in her pink */
.ud { position: absolute; width: 30px; height: 30px; border-radius: 50%;
  background: linear-gradient(160deg, #ff8ab0 0%, #e0204b 100%);
  box-shadow: 0 0 0 4px rgba(255,255,255,0.9), 0 0 18px rgba(255,110,156,0.9); }
.ud.flat { box-shadow: 0 0 14px rgba(255,110,156,0.6); }

/* a DM bubble over footage */
.bub { position: absolute; border-radius: 40px 40px 40px 12px; }
.bub i { position: absolute; display: block; height: 18px; border-radius: 9px; background: rgba(255,255,255,0.86); }
.bub i.lo { background: rgba(255,255,255,0.5); }
.bub.me2 { border-radius: 40px 40px 12px 40px;
  background: linear-gradient(165deg, #e0204b 0%, #ab112e 50%, #7a0a20 100%);
  box-shadow: inset 0 2px 1px rgba(255,255,255,0.45), 0 30px 60px -22px rgba(70,4,20,0.7); }
.bub.in2 { background: linear-gradient(160deg, rgba(255,255,255,0.30) 0%, rgba(255,255,255,0.14) 100%);
  box-shadow: inset 0 1.5px 1px rgba(255,255,255,0.5); }
.dots3 b { position: absolute; top: 34px; width: 20px; height: 20px; border-radius: 50%; background: #fff; display: block; }

/* the inbox on the takeover */
.inb { position: absolute; overflow: hidden; }
.lv { position: absolute; left: 0; width: 1200px; top: 300px; height: 1040px; overflow: hidden; }
#ibx { position: absolute; left: 0; top: 0; width: 1200px; }
.ir { position: absolute; left: 0; width: 1200px; height: 150px; }
.ir i { position: absolute; display: block; }
.ir .av { left: 120px; top: 27px; width: 96px; height: 96px; border-radius: 50%;
  background: linear-gradient(150deg, #f6e3e8 0%, #ecc8d0 100%); display: flex; align-items: center; justify-content: center; }
.ir .av .sk { stroke: rgba(23,20,28,0.32); width: 56%; height: 56%; }
.ir .nm { left: 250px; top: 40px; height: 28px; border-radius: 14px; background: rgba(23,20,28,0.80); }
.ir .ms { left: 250px; top: 86px; height: 22px; border-radius: 11px; background: rgba(23,20,28,0.18); }
.ir.rd .nm { background: rgba(23,20,28,0.30); }
.ir .tm { left: 900px; top: 46px; width: 66px; height: 16px; border-radius: 8px; background: rgba(23,20,28,0.14); }
.ir .ud { left: 920px; top: 80px; box-shadow: 0 0 14px rgba(255,110,156,0.55); }
.ir .hl { left: 250px; right: 120px; bottom: 0; height: 2px; background: rgba(23,20,28,0.07); }
.hb { position: absolute; border-radius: 14px; background: linear-gradient(115deg, #c41434 0%, #8d0d24 100%); }

/* the shelf of chats that become tasks */
.row { position: absolute; left: 30px; width: 620px; height: 120px; transform-style: preserve-3d; }
.row .fa, .row .fb { position: absolute; inset: 0; backface-visibility: hidden; }
.row i { position: absolute; display: block; }
.row .wb { height: 24px; border-radius: 12px; background: rgba(255,255,255,0.92); }
.row .wl { height: 18px; border-radius: 9px; background: rgba(255,255,255,0.55); }
.row .ud { left: 560px; top: 45px; }
.cbx { position: absolute; width: 64px; height: 64px; border-radius: 18px;
  box-shadow: inset 0 0 0 4.5px rgba(255,255,255,0.92); }
.cbx.ink { box-shadow: inset 0 0 0 4.5px rgba(23,20,28,0.25); }

/* the scripts sheet */
.scr { position: absolute; left: 120px; width: 960px; height: 230px; border-radius: 48px;
  background: linear-gradient(170deg, #fdf3f6 0%, #f8e4ea 100%);
  box-shadow: inset 0 2px 1px #fff, 0 20px 44px -26px rgba(80,6,24,0.35); }
.scr .ic { position: absolute; left: 36px; top: 50px; width: 130px; height: 130px; }
.scr .ghost { position: absolute; inset: 0; border-radius: 22.4%; background: rgba(23,20,28,0.06);
  box-shadow: inset 0 0 0 3px rgba(23,20,28,0.08); display: flex; align-items: center; justify-content: center; }
.scr .ghost .sk { stroke: rgba(23,20,28,0.22); }
.scr .ttl { position: absolute; left: 200px; top: 48px; font-size: 52px; font-weight: 700; letter-spacing: -0.02em;
  color: #17141c; white-space: nowrap; }
.scr i { position: absolute; display: block; left: 200px; height: 22px; border-radius: 11px;
  background: rgba(23,20,28,0.14); transform-origin: 0 50%; }
.scr .gl2 { position: absolute; left: 200px; top: 64px; width: 420px; height: 34px; border-radius: 17px;
  background: rgba(23,20,28,0.07); }

/* the script chip under a reply */
.chipS { position: absolute; height: 78px; border-radius: 39px; padding: 0 30px 0 18px; display: flex; align-items: center; gap: 14px;
  background: linear-gradient(160deg, #ffffff 0%, #fff5f8 52%, #f5dfe6 100%); color: #17141c;
  font-size: 32px; font-weight: 700; letter-spacing: -0.01em; white-space: nowrap;
  box-shadow: inset 0 2px 1px #fff, 0 26px 50px -20px rgba(24,4,12,0.6); }
.chipS .sk { width: 46px; height: 46px; stroke: #b4122f; }

/* the approval card */
.apc { position: absolute; border-radius: 56px; overflow: hidden; color: #17141c;
  background: linear-gradient(172deg, #ffffff 0%, #fff9fb 55%, #fdf0f4 100%);
  box-shadow: inset 0 2px 1px #fff, 0 50px 100px -36px rgba(24,4,12,0.65); }
.apc i { position: absolute; display: block; }
.apc .to { left: 44px; top: 36px; font-size: 26px; font-weight: 700; letter-spacing: 0.16em; color: rgba(23,20,28,0.42); }
.apc .rr { height: 22px; border-radius: 11px; background: rgba(255,255,255,0.75); }
.abtn { position: absolute; height: 96px; border-radius: 48px; display: flex; align-items: center; justify-content: center; gap: 14px;
  font-size: 38px; font-weight: 700; letter-spacing: -0.01em; }
.abtn.ghostb { color: rgba(23,20,28,0.55); box-shadow: inset 0 0 0 3px rgba(23,20,28,0.14); }
.abtn.go { color: #fff; background: linear-gradient(165deg, #e0204b 0%, #ab112e 46%, #6b081c 100%);
  box-shadow: inset 0 2px 1px rgba(255,255,255,0.5), 0 22px 44px -16px rgba(70,4,20,0.7); }
.abtn .sk { width: 44px; height: 44px; }
.cur { position: absolute; width: 64px; height: 64px; z-index: 6; filter: drop-shadow(0 6px 10px rgba(24,4,12,0.35)); }
.ck { position: absolute; width: 120px; height: 120px; margin: -60px 0 0 -60px; border-radius: 50%;
  border: 7px solid #ff6e9c; opacity: 0; visibility: hidden; z-index: 5; }
.slash { fill: none; stroke: #ff6e9c; stroke-width: 18; stroke-linecap: round;
  filter: drop-shadow(0 0 12px rgba(255,110,156,0.9)); }

/* follow */
.fl { position: absolute; border-radius: 80px; overflow: hidden;
  background: linear-gradient(160deg, #ffffff 0%, #fff5f8 52%, #f5dfe6 100%);
  box-shadow: inset 0 2px 1px #fff, 0 40px 80px -28px rgba(30,4,12,0.65); }
.fl .t { position: absolute; left: 160px; top: 0; height: 150px; line-height: 150px; font-size: 56px; font-weight: 700;
  letter-spacing: -0.02em; color: #17141c; }
.fl .on { position: absolute; inset: 0; background: linear-gradient(165deg, #e0204b 0%, #ab112e 46%, #6b081c 100%);
  opacity: 0; visibility: hidden; }
.fl .on .t { color: #fff; left: 150px; }
.shc { position: absolute; inset: 0; border-radius: inherit; overflow: hidden; pointer-events: none; }
.shc .sheen { mix-blend-mode: normal; opacity: 0.4; }
""")

L = []
LATE = []           # groups that must sit above later beats' cables
BEATS = []


def beat(fn):
    BEATS.append(fn)
    return fn


# ===========================================================================
# A · hook — clients write, the DMs fall away, Instagram + Telegram
AV = [(250, 140), (474, 140), (698, 140)]       # avatar tiles, 132 px


@beat
def a_clients():
    h = ""
    for i, (x, y) in enumerate(AV):
        h += tile("aAv%d" % i, 132, x, y, "pearl", stroke("person"), extra_cls="circ", ring=False)
        h += '<div class="ud hide" id="aUd%d" style="left:%dpx;top:%dpx"></div>' % (i, x + 100, y + 2)
        h += ('<div class="bub in2 hide" id="aBb%d" style="left:%dpx;top:%dpx;width:210px;height:96px">'
              '<i style="left:28px;top:26px;width:150px"></i><i class="lo" style="left:28px;top:56px;width:96px"></i></div>'
              % (i, x - 39, y + 160))
    h += tile("aIG", 190, 250, 200, "clear", g.mark("instagram"))
    h += '<div class="ud hide" id="aIGd" style="left:420px;top:190px"></div>'
    h += tile("aTG", 190, 640, 200, "clear", g.mark("telegram"))
    h += '<div class="ud hide" id="aTGd" style="left:810px;top:190px"></div>'
    L.append('<div class="g full" id="gA">' + h + '</div>')
    sfx("pop", T["pratsiuvav"] + 0.05, -2)
    sfx("notification", T["problem"] + 0.05)
    sfx("pop", T["insta"] + 0.02, -2)
    return js("""
  tl.set("#gA", {autoAlpha: 1}, 0.2);
  [0, 1, 2].forEach(function (i) { arr("#aAv" + i, @pratsiuvav-0.05 + i * 0.1, {s: 0.4, y: 30, d: 0.75}); });
  tl.to(["#aAv0", "#aAv1", "#aAv2"], {y: -10, duration: 0.18, ease: "power2.out", stagger: 0.07}, @znaie);
  tl.to(["#aAv0", "#aAv1", "#aAv2"], {y: 0, duration: 0.45, ease: SP, stagger: 0.07}, @znaie+0.18);
  /* each client writes */
  [0, 1, 2].forEach(function (i) {
    arr("#aBb" + i, @problem-0.08 + i * 0.09, {s: 0.3, y: -60, d: 0.7});
    tl.fromTo("#aUd" + i, {autoAlpha: 0, scale: 0.2}, {autoAlpha: 1, scale: 1, duration: 0.45, ease: POP}, @problem+0.1 + i * 0.09);
  });
  G.haptic(["#aBb0", "#aBb1", "#aBb2"], @problem+0.82);
  /* she misses them: the DMs drop away unread */
  [0, 1, 2].forEach(function (i) {
    tl.to("#aBb" + i, {y: 150, rotation: [-7, 5, -4][i], autoAlpha: 0, filter: "blur(8px)", duration: 0.55, ease: "power2.in"}, @propusk+0.05 + i * 0.1);
  });
  tl.to(["#aAv0", "#aAv1", "#aAv2"], {autoAlpha: 0.55, duration: 0.4}, @propusk+0.3);
  /* the clients fold into the two apps they write in */
  tl.to(["#aAv0", "#aAv1", "#aAv2", "#aUd0", "#aUd1", "#aUd2"], {x: function (i) { return [29, -195, -419, -20, -244, -468][i]; },
        y: 90, scale: 0.3, autoAlpha: 0, duration: 0.4, ease: "power3.in"}, @insta-0.3);
  arr("#aIG", @insta-0.04, {s: 0.4, y: 30, d: 0.75}); G.ripple("#aIGR", @insta+0.25);
  tl.fromTo("#aIGd", {autoAlpha: 0, scale: 0.2}, {autoAlpha: 1, scale: 1, duration: 0.45, ease: POP}, @insta+0.25);
  arr("#aTG", @tele-0.04, {s: 0.4, y: 30, d: 0.75}); G.ripple("#aTGR", @tele+0.25);
  tl.fromTo("#aTGd", {autoAlpha: 0, scale: 0.2}, {autoAlpha: 1, scale: 1, duration: 0.45, ease: POP}, @tele+0.25);
  tl.set("#gA", {autoAlpha: 0}, @roboty+0.6);""")


# ===========================================================================
# B · OVER — the inbox floods; the unread chats sink out of sight
ROWS = 14            # rows 7..13 are on screen first (all unread), 0..6 flood in on top
# (name width, message width, unread)
ROWDATA = [(250, 560, 1), (190, 470, 0), (300, 610, 1), (220, 420, 1), (270, 530, 0), (180, 590, 1),
           (240, 450, 0), (280, 600, 1), (200, 500, 1), (260, 560, 1), (230, 430, 1), (290, 580, 1),
           (210, 520, 1), (250, 470, 1)]


@beat
def b_inbox():
    rows = ""
    for i, (nw, mw, un) in enumerate(ROWDATA):
        rows += ('<div class="ir%s" style="top:%dpx"><i class="av">%s</i><i class="nm" style="width:%dpx"></i>'
                 '<i class="ms" style="width:%dpx"></i><i class="tm"></i>%s<i class="hl"></i></div>'
                 % ("" if un else " rd", i * 150, stroke("person"), nw, mw,
                    '<i class="ud"></i>' if un else ""))
    sheet = ('<div class="sheet hide" id="bSh" style="left:-60px;top:-100px;width:1200px;height:1340px" '
             'data-layout-allow-overflow>'
             '<div class="tw" style="left:120px;top:150px;width:100px;height:100px"><div class="pearl">%s</div></div>'
             '<div class="tw" style="left:240px;top:150px;width:100px;height:100px"><div class="pearl">%s</div></div>'
             '<i class="hb" style="left:380px;top:180px;width:250px;height:38px"></i>'
             '<i class="hair abs" style="left:120px;top:284px;width:960px"></i>'
             '<div class="lv" id="bLv"><div id="ibx">%s</div></div>'
             '<div class="sheen"></div></div>' % (g.mark("instagram"), g.mark("telegram"), rows))
    L.append('<div class="g full" id="gB"><div class="tkg"></div><div class="aurs"></div><div class="grain"></div>'
             + sheet + tile("bEye", 230, 425, 520, "jelly", stroke("eyeoff")) + '</div>')
    sfx("whoosh-short", T["roboty"] - 0.12)
    sfx("click-soft", T["povidomlen"] + 0.05, -3)
    sfx("pop", T["pomich"] + 0.02)
    return js("""
  G.irisOpen("#gB", @roboty-0.13, 735, 295, 0.7);
  drift1("#gB", @roboty-0.13, @tomu-@roboty+0.4);
  gsap.set("#ibx", {y: -1050});
  arr("#bSh", @roboty-0.05, {s: 0.82, y: 80, d: 0.85});
  shn("#bSh .sheen", @roboty+0.4);
  /* more and more: new chats pile in on top, the unread ones are pushed out the bottom */
  tl.to("#ibx", {y: 0, duration: @khove-@povidomlen+0.05, ease: "power2.in"}, @povidomlen-0.05);
  G.bump("#bSh", @bilshe);
  /* she does not see them */
  arr("#bEye", @pomich-0.06, {s: 0.4, y: 30, d: 0.75}); G.ripple("#bEyeR", @pomich+0.25);
  tl.to("#bLv", {filter: "blur(7px)", autoAlpha: 0.55, duration: 0.5, ease: "power2.out"}, @pomich-0.05);
  G.irisClose("#gB", @tomu-0.18, 540, 172, 0.5);""")


# ===========================================================================
# C · near — the routine reads Instagram + Telegram through SendPulse
@beat
def c_routine():
    cab = ('<svg class="cab abs" width="1080" height="640" viewBox="0 0 1080 640" style="left:0;top:0">'
           '<path class="tube hide" id="cT1" d="M266 410 H 368"/><path class="core hide" id="cC1" d="M266 410 H 368"/>'
           '<path class="tube hide" id="cT2" d="M814 410 H 712"/><path class="core hide" id="cC2" d="M814 410 H 712"/>'
           '<path class="tube hide" id="cT3" d="M540 334 V 262"/><path class="core hide" id="cC3" d="M540 334 V 262"/>'
           '<g class="pkg"><path class="pkt" id="cP1" style="opacity:0" d="M266 410 H 368"/>'
           '<path class="pkt" id="cP2" style="opacity:0" d="M814 410 H 712"/>'
           '<path class="pkt" id="cP3" style="opacity:0" d="M540 334 V 262"/></g></svg>')
    sp = ('<div class="sqring" id="cSPR" style="left:370px;top:340px;width:340px;height:140px;border-radius:70px"></div>'
          '<div class="tw hide" id="cSP" style="left:370px;top:340px;width:340px;height:140px">'
          '<div class="jelly" style="border-radius:70px;gap:16px">%s'
          '<span class="wmark" style="font-size:50px;letter-spacing:-0.03em;font-weight:700">SendPulse</span>'
          '<div class="sheen"></div></div></div>' % g.mark("sendpulse", cls="mk spm"))
    L.append('<div class="g full" id="gC">' + cab
             + tile("cRt", 172, 454, 88, "pearl", stroke("loop", style="stroke:#b4122f;stroke-width:2.6"))
             + tile("cIG", 150, 112, 335, "clear", g.mark("instagram"))
             + tile("cTG", 150, 818, 335, "clear", g.mark("telegram"))
             + sp + '</div>')
    k.css(".spm { width: 64px; height: 64px; flex: none; }")
    sfx("pop", T["rutynu"] + 0.02)
    sfx("pop", T["sp"] + 0.02)
    return js("""
  tl.set("#gC", {autoAlpha: 1}, @tomu-0.2);
  arr("#cRt", @zrobyla-0.2, {s: 0.25, y: 0, d: 0.8});
  tl.fromTo("#cRt .sk", {rotation: -200, transformOrigin: "50% 50%"}, {rotation: 0, duration: 1.0, ease: SP, immediateRender: false}, @rutynu-0.05);
  G.ripple("#cRtR", @rutynu+0.2);
  G.bump("#cRt", @chytaie);
  arr("#cIG", @ig-0.05, {s: 0.4, x: 40, y: 20, d: 0.75}); G.ripple("#cIGR", @ig+0.25);
  arr("#cTG", @tg+0.08, {s: 0.4, x: -40, y: 20, d: 0.75}); G.ripple("#cTGR", @tg+0.35);
  arr("#cSP", @sp-0.06, {s: 0.5, y: 30, d: 0.8}); G.ripple("#cSPR", @sp+0.25);
  shn("#cSP .sheen", @sp+0.3);
  tl.set(["#cT1", "#cC1", "#cT2", "#cC2"], {autoAlpha: 1}, @cherez+0.05);
  draw2("cT1", @cherez+0.05, 0.4); draw2("cC1", @cherez+0.05, 0.4);
  draw2("cT2", @cherez+0.12, 0.4); draw2("cC2", @cherez+0.12, 0.4);
  G.packet("cP1", @sp+0.35, 0.4); G.packet("cP2", @sp+0.42, 0.4);
  tl.set(["#cT3", "#cC3"], {autoAlpha: 1}, @sp+0.55);
  draw2("cT3", @sp+0.55, 0.3); draw2("cC3", @sp+0.55, 0.3);
  G.packet("cP3", @sp+0.8, 0.35); G.bump("#cRt", @sp+1.1);
  bout(["#cRt", "#cIG", "#cTG", "#cT1", "#cC1", "#cT2", "#cC2", "#cT3", "#cC3"], @kozhen-0.12, 10, 0.26);
  /* SendPulse stays: it deals out the chats */
  tl.to("#cSP", {x: -365, y: -60, scale: 0.6, duration: 0.6, ease: SP}, @kozhen-0.05);
  tl.set("#gC", {autoAlpha: 0}, {{np0}}-0.04);""").replace("{{np0}}", "%.3f" % NO_PAINT[0][0])


# ===========================================================================
# D · near — every unanswered chat becomes a task, for her or the team
@beat
def d_tasks():
    rows = ""
    for i, (nw, mw) in enumerate(((200, 330), (160, 380), (230, 300))):
        y = 32 + i * 136
        rows += ('<div class="row" id="dR%d" style="top:%dpx">'
                 '<div class="fa" id="dA%d">'
                 '<div class="tw circ" style="left:0;top:14px;width:92px;height:92px"><div class="pearl">%s</div></div>'
                 '<i class="wb" style="left:120px;top:30px;width:%dpx"></i>'
                 '<i class="wl" style="left:120px;top:70px;width:%dpx"></i>'
                 '<div class="ud" id="dU%d"></div></div>'
                 '<div class="fb" id="dB%d">'
                 '<div class="cbx" style="left:14px;top:28px"></div>'
                 '<i class="wb" style="left:110px;top:34px;width:%dpx"></i>'
                 '<i class="wl" style="left:110px;top:72px;width:%dpx"></i></div></div>'
                 % (i, y, i, stroke("person"), nw, mw, i, i, mw + 40, nw + 60))
    shelf = ('<div class="shelf edge hide" id="dSh" style="left:330px;top:90px;width:690px;height:450px">%s</div>'
             % rows)
    L.append('<div class="g full" id="gD">' + shelf
             + face("dMe", 96, 910, 132)
             + tile("dTm1", 96, 910, 268, "pearl", stroke("team"), extra_cls="circ", ring=False)
             + tile("dTm2", 96, 910, 404, "pearl", stroke("team"), extra_cls="circ", ring=False)
             + '</div>')
    sfx("pop", T["chat"] + 0.05, -2)
    sfx("click", T["zadachu"] - 0.05)
    return js("""
  tl.set("#gD", {autoAlpha: 1}, @kozhen-0.1);
  gsap.set(["#dB0", "#dB1", "#dB2"], {rotationX: -90, transformPerspective: 900, transformOrigin: "50% 50%"});
  gsap.set(["#dA0", "#dA1", "#dA2"], {transformPerspective: 900, transformOrigin: "50% 50%"});
  arr("#dSh", @kozhen+0.02, {s: 0.75, x: -120, y: 0, d: 0.8});
  /* the chats come out of SendPulse */
  [0, 1, 2].forEach(function (i) { arr("#dR" + i, @chat-0.1 + i * 0.13, {s: 0.4, x: -260, y: 0, d: 0.75}); });
  /* nobody answered: the dots call */
  [0, 1, 2].forEach(function (i) { G.bump("#dU" + i, @vidpoviv+0.05 + i * 0.08); });
  /* each one flips into a task */
  [0, 1, 2].forEach(function (i) {
    var t = @peretv+0.05 + i * 0.13;
    tl.to("#dA" + i, {rotationX: 90, duration: 0.2, ease: "power2.in"}, t);
    tl.to("#dB" + i, {rotationX: 0, duration: 0.6, ease: FLIP}, t + 0.2);
  });
  /* for her, or for the team */
  arr("#dMe", @meni-0.06, {s: 0.3, x: -40, y: 0, d: 0.7});
  arr("#dTm1", @komandi-0.12, {s: 0.3, x: -40, y: 0, d: 0.7});
  arr("#dTm2", @komandi-0.03, {s: 0.3, x: -40, y: 0, d: 0.7});
  bout("#gD", {{np0}}-0.34, 10, 0.26);
  bout("#cSP", {{np0}}-0.34, 10, 0.26);""").replace("{{np0}}", "%.3f" % NO_PAINT[0][0])


# ===========================================================================
# E · OVER — the ready scripts
SCRIPTS = [("calplus", u"Записатись на дзвінок", "zapys", (560, 400)),
           ("calcheck", u"Підтвердити дзвінок", "pidtv", (600, 360)),
           ("send", u"Надіслати офер", "nadisl", (520, 430))]
SCR_TOP = 300        # first row, inside the sheet (sheet top 150 on screen)


@beat
def e_scripts():
    rows = ""
    for i, (ic, title, _, (w1, w2)) in enumerate(SCRIPTS):
        y = SCR_TOP + i * 262
        rows += ('<div class="scr hide" id="eS%d" style="top:%dpx">'
                 '<div class="ic"><div class="ghost">%s</div>'
                 '<div class="tw hide" id="eI%d" style="left:0;top:0;width:130px;height:130px"><div class="jelly">%s'
                 '<div class="sheen"></div></div></div></div>'
                 '<div class="gl2" id="eG%d"></div>'
                 '<div class="ttl" id="eT%d">%s</div>'
                 '<i id="eL%da" style="top:132px;width:%dpx"></i><i id="eL%db" style="top:168px;width:%dpx"></i>'
                 '</div>' % (i, y, stroke(ic), i, stroke(ic), i, i, title, i, w1, i, w2))
    sheet = ('<div class="sheet hide" id="eSh" style="left:-60px;top:150px;width:1200px;height:1090px" '
             'data-layout-allow-overflow>'
             '<div class="tw hide" id="eHd" style="left:120px;top:70px;width:150px;height:150px"><div class="jelly">%s'
             '<div class="sheen"></div></div></div>'
             '<div class="t-micro abs hide" id="eHm" style="left:306px;top:92px">ГОТОВІ</div>'
             '<div class="t-title abs hide" id="eHt" style="left:304px;top:128px;font-size:64px">Скрипти</div>'
             '%s<div class="sheen"></div></div>' % (stroke("doc"), rows))
    L.append('<div class="g full" id="gE"><div class="tkg"></div><div class="aurs"></div><div class="grain"></div>'
             + sheet + '</div>')
    sfx("whoosh-short", T["a"] + 0.03)
    for _, _, key, _ in SCRIPTS:
        sfx("click", T[key] + 0.05)
    lit = []
    for i, (_, _, key, _) in enumerate(SCRIPTS):
        lit.append("""
  tl.set("#eT{{i}}", {clipPath: "inset(0% 100% 0% 0%)"}, 0);
  gsap.set(["#eL{{i}}a", "#eL{{i}}b"], {scaleX: 0});
  arr("#eI{{i}}", @{{k}}-0.05, {s: 0.5, y: 0, d: 0.7}); shn("#eI{{i}} .sheen", @{{k}}+0.25);
  tl.to("#eT{{i}}", {clipPath: "inset(0% 0% 0% 0%)", duration: 0.5, ease: "power2.out"}, @{{k}}+0.02);
  tl.to("#eG{{i}}", {autoAlpha: 0, duration: 0.25}, @{{k}}+0.02);
  tl.to(["#eL{{i}}a", "#eL{{i}}b"], {scaleX: 1, duration: 0.5, ease: SP, stagger: 0.08}, @{{k}}+0.3);
  G.bump("#eS{{i}}", @{{k}}+0.02);""".replace("{{i}}", str(i)).replace("{{k}}", key))
    # the iris closes onto row 1's icon (sheet x -60, row left 120, icon 36+65)
    cx, cy = -60 + 120 + 36 + 65, 150 + SCR_TOP + 50 + 65
    return js("""
  G.irisOpen("#gE", @a+0.02, 540, 330, 0.7);
  drift1("#gE", @a, @ofere-@a+0.6);
  arr("#eSh", @a+0.12, {s: 0.82, y: 80, d: 0.85});
  [0, 1, 2].forEach(function (i) { arr("#eS" + i, @typovykh-0.1 + i * 0.12, {s: 0.85, y: 50, d: 0.7}); });
  arr("#eHd", @hotovi-0.05, {s: 0.4, y: 20, d: 0.7}); shn("#eHd .sheen", @hotovi+0.3);
  bin("#eHm", @hotovi+0.05, 8, 0.3);
  bin("#eHt", @skrypty-0.04, 8, 0.32);
  tl.fromTo("#eHt", {x: -20}, {x: 0, duration: 0.6, ease: SP}, @skrypty-0.04);""" + "".join(lit) + """
  G.irisClose("#gE", @ofere-0.02, {{cx}}, {{cy}}, 0.5);""").replace("{{cx}}", str(cx)).replace("{{cy}}", str(cy))


# ===========================================================================
# F · near — a routine DM, answered from the script
@beat
def f_reply():
    panel = ('<div class="dglass edge hide" id="fP" style="left:90px;top:84px;width:900px;height:466px">'
             '<div class="tw circ" style="left:34px;top:34px;width:76px;height:76px"><div class="pearl">%s</div></div>'
             '<div class="bub in2 hide" id="fIn" style="left:130px;top:34px;width:500px;height:118px">'
             '<i style="left:34px;top:34px;width:360px"></i><i class="lo" style="left:34px;top:66px;width:230px"></i></div>'
             '<div class="bub me2 dots3 hide" id="fDt" style="left:676px;top:182px;width:190px;height:88px">'
             '<b style="left:44px"></b><b style="left:85px"></b><b style="left:126px"></b></div>'
             '</div>' % stroke("person"))
    reply = ('<div class="bub me2 hide" id="fRe" style="left:416px;top:266px;width:540px;height:150px">'
             '<i style="left:36px;top:36px;width:420px"></i><i style="left:36px;top:68px;width:450px"></i>'
             '<i class="lo" style="left:36px;top:100px;width:260px"></i></div>')
    chip = ('<div class="chipS hide" id="fCh" style="left:430px;top:442px">%s%s</div>'
            % (stroke("calplus"), SCRIPTS[0][1]))
    cab = ('<svg class="cab abs" width="1080" height="640" viewBox="0 0 1080 640" style="left:0;top:0">'
           '<path class="wire hide" id="fW" d="M690 446 V 420"/></svg>')
    L.append('<div class="g full" id="gF">' + panel + cab + chip + '</div>')
    LATE.append('<div class="g full" id="gR">' + reply + '</div>')       # above G's cable
    sfx("ping", T["rutynni"] + 0.02, -2)
    sfx("typing", T["vono"] + 0.05, -4)
    return js("""
  tl.set(["#gF", "#gR"], {autoAlpha: 1}, @ofere-0.05);
  /* the script from the sheet lands first */
  arr("#fCh", @ofere+0.3, {s: 0.4, x: -260, y: 40, d: 0.8});
  arr("#fP", @tobto-0.08, {s: 0.85, y: 30, d: 0.8});
  arr("#fIn", @rutynni-0.04, {s: 0.5, x: -40, y: 10, d: 0.7});
  G.haptic("#fIn", @rutynni+0.35);
  arr("#fDt", @vono-0.05, {s: 0.4, y: 10, d: 0.5});
  tl.to("#fDt b", {keyframes: {y: [0, -12, 0]}, duration: 0.36, stagger: 0.12, repeat: 1, ease: "sine.inOut"}, @vono+0.2);
  tl.to("#fDt", {autoAlpha: 0, scale: 0.6, duration: 0.18, ease: "power2.in"}, @vidpovisty-0.02);
  arr("#fRe", @vidpovisty+0.02, {s: 0.4, x: 120, y: -40, d: 0.8});
  G.bump("#fRe", @same);
  /* written from the ready script */
  tl.set("#fW", {autoAlpha: 1}, @hotovomu);
  G.bump("#fCh", @hotovomu); G.bump("#fRe", @hotovomu+0.15);
  bout(["#fP", "#fCh", "#fW"], @i-0.25, 10, 0.26);""")


# ===========================================================================
# G · near — nothing goes to the client without her
@beat
def g_gate():
    cab = ('<svg class="cab abs" width="1080" height="640" viewBox="0 0 1080 640" style="left:0;top:0">'
           '<path class="tube hide" id="gwT" d="M492 330 H 836"/><path class="core hide" id="gwC" d="M492 330 H 836"/></svg>')
    L.append('<div class="g full" id="gG">' + cab
             + tile("gCl", 156, 840, 252, "pearl", stroke("person"), extra_cls="circ")
             + face("gMe", 150, 628, 255)
             + '<div class="sqring rnd" id="gMeR" style="left:628px;top:255px;width:150px;height:150px"></div>'
             + '</div>')
    sfx("click-soft", T["bez"] + 0.05)
    return js("""
  tl.set("#gG", {autoAlpha: 1}, @i-0.3);
  /* the reply steps aside, the client waits on the other end */
  tl.to("#fRe", {x: -364, y: -11, scale: 0.6, duration: 0.7, ease: SP}, @i-0.2);
  arr("#gCl", @klientsi-0.05, {s: 0.4, x: 40, y: 0, d: 0.75}); G.ripple("#gClR", @klientsi+0.25);
  tl.set(["#gwT", "#gwC"], {autoAlpha: 1}, @klientsi+0.15);
  draw2("gwT", @klientsi+0.15, 0.45); draw2("gwC", @klientsi+0.15, 0.45);
  /* it sets off … and stops: she stands in the way */
  tl.to("#fRe", {x: -238, duration: 0.8, ease: "power2.out"}, @nichoho);
  arr("#gMe", @bez-0.08, {s: 0.3, y: -70, d: 0.75}); G.ripple("#gMeR", @bez+0.22);
  tl.to("#fRe", {x: -282, duration: 0.16, ease: "power2.out"}, @bez+0.1);
  tl.to("#fRe", {x: -268, duration: 0.4, ease: SP}, @bez+0.26);
  bout(["#gwT", "#gwC", "#gCl", "#gMe"], @shcho-0.15, 10, 0.26);
  tl.set("#gG", {autoAlpha: 0}, @shcho+0.2);""")


# ===========================================================================
# H · near — she approves it; it is not a bot living its own life
@beat
def h_approve():
    card = ('<div class="apc hide" id="hC" style="left:110px;top:92px;width:860px;height:452px">'
            '<div class="tw circ" style="left:40px;top:30px;width:84px;height:84px"><div class="pearl">%s</div></div>'
            '<i style="left:150px;top:44px;width:230px;height:26px;border-radius:13px;background:rgba(23,20,28,0.78)"></i>'
            '<i style="left:150px;top:84px;width:140px;height:18px;border-radius:9px;background:rgba(23,20,28,0.18)"></i>'
            '<div class="bub me2" style="left:300px;top:136px;width:520px;height:142px;position:absolute">'
            '<i style="left:36px;top:34px;width:410px"></i><i style="left:36px;top:66px;width:440px"></i>'
            '<i class="lo" style="left:36px;top:98px;width:250px"></i></div>'
            '<div class="abtn ghostb" style="left:40px;top:318px;width:330px">Редагувати</div>'
            '<div class="abtn go" id="hGo" style="left:400px;top:318px;width:420px">'
            '<span id="hGoT">Затвердити</span>'
            '<svg class="sk hide" id="hGoK" viewBox="0 0 24 24" style="stroke:#fff;stroke-width:3;position:absolute;right:30px;top:26px">%s</svg></div>'
            '<div class="ck" id="hCk" style="left:610px;top:366px"></div>'
            '<div class="cur hide" id="hCur" style="left:600px;top:360px">%s</div>'
            '<div class="shc"><div class="sheen"></div></div></div>'
            % (stroke("person"), STROKES["check"], CURSOR))
    bot = ('<svg class="abs" width="1080" height="640" viewBox="0 0 1080 640" style="left:0;top:0;overflow:visible">'
           '<path class="slash hide" id="hX1" d="M405 135 L 675 405"/><path class="slash hide" id="hX2" d="M675 135 L 405 405"/>'
           '</svg>')
    L.append('<div class="g full" id="gH">' + card
             + tile("hBot", 210, 435, 165, "clear", stroke("bot"))
             + bot + '</div>')
    sfx("click", T["zatv"] + 0.02)
    sfx("whoosh-short", T["sama"] - 0.05, -1)
    sfx("pop", T["bot"] + 0.02, -2)
    return js("""
  tl.set("#gH", {autoAlpha: 1}, @shcho-0.2);
  /* the reply opens into the approval card */
  tl.to("#fRe", {scale: 0.9, autoAlpha: 0, duration: 0.3, ease: "power2.in"}, @shcho-0.1);
  tl.set("#gR", {autoAlpha: 0}, @shcho+0.3);
  gsap.set("#hC", {transformOrigin: "62% 46%"});
  arr("#hC", @shcho-0.05, {s: 0.55, y: 30, d: 0.85});
  shn("#hC .sheen", @vidpravl);
  /* her cursor taps «Затвердити» */
  tl.fromTo("#hCur", {x: 240, y: 140}, {x: 0, y: 0, duration: 0.75, ease: "power2.inOut", immediateRender: false}, @zatv-0.8);
  bin("#hCur", @zatv-0.8, 6, 0.25);
  tl.to("#hCur", {scale: 0.86, duration: 0.09}, @zatv); tl.to("#hCur", {scale: 1, duration: 0.3}, @zatv+0.09);
  tl.to("#hGo", {scale: 0.95, duration: 0.09, ease: "power2.out"}, @zatv);
  tl.to("#hGo", {scale: 1, duration: 0.45, ease: SP}, @zatv+0.09);
  tl.fromTo("#hCk", {scale: 0.3, autoAlpha: 0.95}, {scale: 2.2, autoAlpha: 0, duration: 0.7, ease: "power2.out", immediateRender: false}, @zatv+0.02);
  tl.fromTo("#hGoK", {autoAlpha: 0, scale: 0.3}, {autoAlpha: 1, scale: 1, duration: 0.45, ease: POP}, @zatv+0.1);
  /* and only then it goes */
  tl.to("#hC", {x: 520, y: -40, scale: 0.25, rotation: 6, autoAlpha: 0, filter: "blur(6px)", duration: 0.5, ease: "power3.in"}, @sama-0.08);
  /* not a bot living its own life in her DMs */
  arr("#hBot", @bot-0.12, {s: 0.4, y: 30, d: 0.7});
  tl.to("#hBot", {keyframes: {x: [0, -210, 170, -90, 0], y: [0, 40, -30, 50, 0], rotation: [0, -10, 9, -6, 0]},
        duration: @dyrekti-@zhyve+0.1, ease: "sine.inOut"}, @zhyve-0.15);
  tl.set(["#hX1", "#hX2"], {autoAlpha: 1}, @dyrekti-0.05);
  draw2("hX1", @dyrekti-0.05, 0.25); draw2("hX2", @dyrekti+0.12, 0.25);
  tl.to("#hBot", {autoAlpha: 0.85, scale: 0.94, duration: 0.3}, @dyrekti+0.1);
  bout("#gH", @yakshcho-0.2, 10, 0.24);""")


# ===========================================================================
# I · Стежити
@beat
def i_follow():
    L.append('<div class="g full" id="gI"><div class="fl hide" id="fl" style="left:190px;top:300px;width:700px;height:150px">'
             '<div class="tw circ" style="left:28px;top:27px;width:96px;height:96px"><div class="jelly">%s</div></div>'
             '<div class="t" id="flT">Стежити</div>'
             '<div class="on" id="flOn"><div class="tw circ" style="left:28px;top:27px;width:96px;height:96px">'
             '<div class="pearl">%s</div></div><div class="t">Ви стежите</div></div>'
             '<div class="ck" id="ck4" style="left:470px;top:75px"></div>'
             '<div class="shc"><div class="sheen"></div></div></div></div>'
             % (g.mark("instagram"), stroke("check")))
    sfx("click", T["pidpysh"] + 0.16)
    return js("""
  tl.set("#gI", {autoAlpha: 1}, @yakshcho-0.1);
  arr("#fl", @yakshcho-0.02, {s: 0.6, y: 40});
  tl.to("#fl", {scale: 0.95, duration: 0.09, ease: "power2.out"}, @pidpysh+0.14);
  tl.to("#fl", {scale: 1, duration: 0.45, ease: SP}, @pidpysh+0.23);
  tl.fromTo("#flOn", {autoAlpha: 0}, {autoAlpha: 1, duration: 0.2}, @pidpysh+0.18);
  tl.set("#flT", {autoAlpha: 0}, @pidpysh+0.19);
  tl.fromTo("#ck4", {scale: 0.3, autoAlpha: 0.95}, {scale: 2.4, autoAlpha: 0, duration: 0.7, ease: "power2.out", immediateRender: false}, @pidpysh+0.16);
  shn("#fl .sheen", @pidpysh+0.3);""")


# ---------------------------------------------------------------------------
HEAD_JS = r"""
  var G = helpers(tl);
  function bin(sel, t, b, d) { d = d || 0.38; G.blurIn(sel, t, b || 12, d); tl.set(sel, {filter: "none"}, t + d + 0.01); }
  function bout(sel, t, b, d) { d = d || 0.32; G.blurOut(sel, t, b || 10, d); tl.set(sel, {filter: "none"}, t + d + 0.01); }
  function arr(sel, t, o) {
    o = o || {};
    bin(sel, t, o.blur || 12, 0.36);
    tl.fromTo(sel, {scale: o.s == null ? 0.5 : o.s, x: o.x || 0, y: o.y == null ? 34 : o.y},
              {scale: 1, x: 0, y: 0, duration: o.d || 0.85, ease: o.ease || POP}, t);
  }
  function draw2(id, t, d) {
    var L = document.getElementById(id).getTotalLength() + 3;
    tl.fromTo("#" + id, {strokeDasharray: (L - 3) + " " + (L + 40), strokeDashoffset: L},
              {strokeDashoffset: 0, duration: d || 0.5, ease: "power2.inOut", immediateRender: false}, t);
    gsap.set("#" + id, {strokeDasharray: (L - 3) + " " + (L + 40), strokeDashoffset: L});
  }
  function shn(sel, t) {
    gsap.set(sel, {xPercent: -120});
    tl.fromTo(sel, {xPercent: -120}, {xPercent: 120, duration: 0.8, ease: "power2.inOut", immediateRender: false}, t);
  }
  function drift1(sel, t, d) { tl.fromTo(sel + " .aurs", {x: 0, y: 0}, {x: -110, y: 70, duration: d, ease: "sine.inOut"}, t); }
  gsap.set(".sheen", {xPercent: -120});
"""


# captions that would repeat the graphic's own words (STYLE.md §2b.1)
def span_words(a, b):
    return (round(a - 0.02, 3), round(b, 3), "")


BLACKOUT = [
    span_words(T["sp"], T["spe"]),                 # the SendPulse tile says it
    span_words(T["hotovi"], T["ofere"]),           # ГОТОВІ Скрипти + the three script titles
    span_words(T["zatv"], T["zatve"]),             # the «Затвердити» button
]


def check_no_paint():
    """No graphic may be on screen inside the closeup."""
    a, b = NO_PAINT[0]
    assert T["komandi"] + 0.1 < a - 0.34, "task beat runs into the closeup"
    assert T["a"] >= b - 0.01, "scripts takeover opens inside the closeup"
    for c in SFX:
        assert not (a - 0.05 <= c["t"] <= b), ("sfx on the closeup", c)


def main():
    gj = []
    for fn in BEATS:
        j = fn()
        gj.append("  /* %s */" % fn.__name__)
        gj.append(j.rstrip())
    check_no_paint()
    push = ["#vid"]
    head = [g.js(), HEAD_JS,
            '  gsap.set(%s, {transformOrigin: "540px 900px"});' % json.dumps(push),
            '  tl.fromTo(%s, {scale: 1}, {scale: 1.045, duration: %.3f, ease: "none"}, 0);' % (json.dumps(push), DUR)]
    doc = k.document(
        title=u"Reel 33 — Жодної втраченої клієнтки в дірект",
        plate="assets/base.mp4",
        gfx_html=g.defs() + "\n" + "\n".join(L + LATE),
        gfx_js="\n".join(head + gj),
        caps=CAPS,
        blackout=BLACKOUT,
    )
    io.open(os.path.join(HERE, "index.html"), "w", encoding="utf-8").write(doc)
    SFX.sort(key=lambda c: c["t"])
    io.open(os.path.join(HERE, "sfx.json"), "w", encoding="utf-8").write(json.dumps(SFX, indent=1))
    print("index.html  %d captions, %d beats, %d sfx cues (%.2f/s)" % (len(CAPS), len(BEATS), len(SFX), len(SFX) / DUR))


main()
