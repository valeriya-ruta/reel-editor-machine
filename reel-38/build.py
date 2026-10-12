# -*- coding: utf-8 -*-
"""Reel 38 — «Одне відео → карусель і імейл». Posts 2026-10-17.

Cut from her raw take by tools/cut.py (no closeups this time — no_paint is
empty), sound design by tools/sfx.py, refined glass (STYLE.md §0).

The spine is before → after, and the one object is **the pipeline**:
before it is four separate apps with copy-paste between them, after it is one
chat that does every step.

Chain:  near: a video call (her + the SMM, the SMM's clients) -> the call
folds into her process: a shelf of four ghost slots (video, Gemini, ChatGPT,
Canva) lit one by one, an artefact under each (film strip, transcript, three
scripts, slides clicked out by hand) -> a strike runs through the steps
(«зайвих кроків») -> OVER: the iris opens out of the strike: subscription
cards pile up and bleed off the frame, swept away on «Можна», Claude lands and
grows two arms with plugs («потужні руки») -> the iris closes onto Claude ->
near: a plug goes into OpenRouter, wires out to a wall of models, € on «цінами»
-> the pair moves up, Gemini and ChatGPT get ×'d and drop -> Whisper and the
other models pop out of OpenRouter and fly into one chat -> OVER: the iris
opens out of that chat: the chat full frame — tools connected, the video
dropped in once, Whisper via OpenRouter transcribes, Claude writes the carousel
and the email, the design system deals the slides, «ОК» pressed -> the iris
closes -> near: four app windows, copy-paste keycaps flying -> they collapse
into one chat, the video drops in -> the comment box types «+».

usage: python build.py   (then: python ../tools/sfx.py mix 38)
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

CUT = json.load(io.open(os.path.join(ROOT, "work", "r38", "cut.json"), encoding="utf-8"))
DUR = 63.116           # (1894 plate frames - 0.5) / 30, floored
FPS = 30
k = Kit(width=1080, height=1920, fps=FPS, duration=DUR)
g = Glass(["claude", "googlegemini", "openai", "canva", "openrouter", "kling", "perplexity",
           "mistralai", "anthropic", "meta", "nvidia", "huggingface", "ollama", "gmail"])
k.css(g.css())

NO_PAINT = [tuple(x) for x in CUT["no_paint"]]      # empty on this cut

CAPS = k.load_captions(os.path.join(ROOT, "work", "r38", "captions.json"))
# whisper mangled these; restore the script word (align.txt "SHE IMPROVISED")
FIX = {u"Семенницю,": u"СММницею,", u"джеміний,": u"Gemini,", u"тон": u"той", u"короселі": u"каруселі",
       u"емейл,": u"імейл,", u"чанель,": u"чат,", u"якому": u"в якому"}
for c in CAPS:
    c["w"] = FIX.get(c["w"], c["w"])
# «ОК» is spoken (51.65–51.87, two syllables after a gap) but whisper folded it
# into «твоє». Give it back its own caption.
_i = next(i for i, c in enumerate(CAPS) if c["w"] == u"твоє")
CAPS.insert(_i + 1, {"w": u"ОК.", "s": 51.630, "e": 51.900, "src": "added"})
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
    "konsult": S(u"консультація", 1.06), "smm": S(u"СММницею", 1.74), "kliientiv": S(u"клієнтів", 2.70),
    "pokazala": S(u"показала", 3.53), "protses": S(u"процес", 4.51), "dovho": S(u"довго", 5.53),
    "video": S(u"відео", 5.79), "klienta": S(u"клієнта", 6.15),
    "kydaie": S(u"кидає", 6.75), "gemini": S("Gemini", 7.19), "transkr": S(u"транскрибує", 7.89),
    "potim": S(u"потім", 8.75), "chatgpt": S("ChatGPT", 8.95), "dilyt": S(u"ділить", 9.49),
    "stsenarii": S(u"сценарії", 10.31), "vruchnu": S(u"вручну", 11.65), "dyzain": S(u"дизайнити", 12.35),
    "canva": S("Canva", 13.31), "sydila": S(u"сиділа", 14.31), "dumala": S(u"думала", 14.85),
    "navishcho": S(u"навіщо", 15.55), "zaivykh": S(u"зайвих", 16.43), "krokiv": S(u"кроків", 16.89),
    "tomu": S(u"Тому", 17.53), "trymaty": S(u"тримати", 18.68), "pidpysky": S(u"підписки", 19.06),
    "pidpyskye": E(u"підписки", 19.06),
    "kupu": S(u"купу", 19.74), "riznykh": S(u"різних", 20.02), "shtuchnykh": S(u"штучних", 20.38),
    "intelekt": S(u"інтелектів", 20.78), "mozhna": S(u"Можна", 21.73), "svoiemu": S(u"своєму", 22.83),
    "klodu": S(u"Клоду", 23.19), "duzhe": S(u"дуже", 23.55), "potuzhni": S(u"потужні", 24.25),
    "ruky": S(u"руки", 24.93), "napryklad": S(u"наприклад", 25.55), "pidkl": S(u"підключити", 26.23),
    "openrouter": S("OpenRouter", 26.63), "openroutere": E("OpenRouter", 26.63),
    "dostup": S(u"доступ", 27.77), "vsikh": S(u"всіх", 28.31), "modelei": S(u"моделей", 28.57),
    "rynkovymy": S(u"ринковими", 29.39), "tsinamy": S(u"цінами", 29.91),
    "tody": S(u"тоді", 30.64), "ni1": S(u"ні", 31.74), "gemini2": S("Gemini", 31.98),
    "ni2": S(u"ні", 32.54), "chatgpt2": S("ChatGPT", 32.70), "okremo": S(u"окремо", 33.24),
    "ie": S(u"є", 33.87), "whisper": S("Whisper", 34.10), "whispere": E("Whisper", 34.10),
    "kupa": S(u"купа", 34.66), "inshykh": S(u"інших", 34.91),
    "vse": S(u"все", 35.77), "pratsiuie": S(u"працює", 36.16), "vseredyni": S(u"всередині", 36.95),
    "odnoho": S(u"одного", 37.60), "chatu": S(u"чату", 37.98),
    "tomu2": S(u"Тому", 38.73), "nalasht": S(u"налаштували", 39.46), "video2": S(u"відео", 40.36),
    "kydaiesh": S(u"кидаєш", 40.64), "odyn": S(u"один", 41.12), "vse2": S(u"все", 42.06),
    "whisper2": S("Whisper", 42.71), "cherez": S(u"через", 43.05), "openrouter2": S("OpenRouter", 43.23),
    "openrouter2e": E("OpenRouter", 43.23), "transkr2": S(u"транскрибує", 44.03),
    "claude": S("Claude", 44.95), "pyshe": S(u"пише", 45.79), "tekst": S(u"текст", 46.11),
    "karuseli": S(u"каруселі", 46.65), "karuselie": E(u"каруселі", 46.65),
    "imeil": S(u"імейл", 47.31), "imeile": E(u"імейл", 47.31),
    "dsys": S(u"дизайн-система", 48.15), "dsyse": E(u"дизайн-система", 48.15),
    "sama": S(u"сама", 48.89), "skladaie": S(u"складає", 49.47), "slaidy": S(u"слайди", 49.91),
    "chekaie": S(u"чекає", 50.73), "tvoie": S(u"твоє", 51.25), "ok": S(u"ОК", 51.63), "oke": E(u"ОК", 51.63),
    "tobto": S(u"Тобто", 51.97), "ranishe": S(u"раніше", 52.25), "chotyry": S(u"чотири", 53.11),
    "prohramy": S(u"програми", 53.99), "kupa2": S(u"купа", 54.69), "kopipastu": S(u"копіпасту", 55.07),
    "mizh": S(u"між", 55.63), "teper": S(u"тепер", 56.37), "odyn2": S(u"один", 56.66),
    "chat": S(u"чат", 57.05), "kynula": S(u"кинула", 58.06), "video3": S(u"відео", 58.41),
    "yakshcho": S(u"Якщо", 59.04), "nalasht2": S(u"налаштувати", 60.46), "plius": S(u"плюс", 62.04),
    "pliuse": E(u"плюс", 62.04), "koment": S(u"коментарі", 62.60),
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
# Sound design (tools/sfx.py). Quiet, on the event.
SFX = []


def sfx(name, t, db=0):
    if isinstance(t, str):
        t = float(js(t))
    SFX.append({"t": round(max(0.0, t), 3), "name": name, "db": db})


# ---------------------------------------------------------------------------
# Glyphs
STROKES = {
    "up": '<path d="M12 19.2V5.4M6.2 11l5.8-5.8 5.8 5.8"/>',
    "check": '<path d="M5.4 12.6l4.3 4.3 8.9-9.5"/>',
    "x": '<path d="M6.8 6.8l10.4 10.4M17.2 6.8L6.8 17.2"/>',
    "person": '<circle cx="12" cy="8.2" r="3.6"/><path d="M4.8 20c.9-3.8 3.7-5.8 7.2-5.8s6.3 2 7.2 5.8"/>',
    "mic": '<rect x="9" y="3" width="6" height="11" rx="3"/><path d="M5.5 11a6.5 6.5 0 0 0 13 0M12 17.5V21"/>',
    "cam": '<rect x="3" y="6.5" width="12.5" height="11" rx="2.5"/><path d="M15.5 10.5l5-3v9l-5-3z"/>',
    "plug": '<path d="M9 3v5M15 3v5M6.5 8h11v3.5a5.5 5.5 0 0 1-11 0zM12 17v4"/>',
    "repeat": ('<path d="M4.6 11A7.4 7.4 0 0 1 17.6 6.4L19 7.8M19 3.6v4.2h-4.2'
               'M19.4 13a7.4 7.4 0 0 1-13 4.6L5 16.2M5 20.4v-4.2h4.2"/>'),
    "mail": '<rect x="3" y="5.5" width="18" height="13" rx="2.5"/><path d="M3.8 7l8.2 6.2L20.2 7"/>',
    "hang": '<path d="M3.5 13.5c4.8-4 12.2-4 17 0l-1.8 2.6-3.4-1.2-.4-2.6c-2.3-.7-4.5-.7-6.8 0l-.4 2.6-3.4 1.2z"/>',
    "heart": '<path d="M12 20s-7.5-4.6-7.5-10A4.3 4.3 0 0 1 12 7.3 4.3 4.3 0 0 1 19.5 10c0 5.4-7.5 10-7.5 10z"/>',
}
PLAY = '<svg class="play" viewBox="0 0 24 24"><path d="M8.5 5.8v12.4L18.6 12z"/></svg>'
CURSOR = ('<svg viewBox="0 0 24 24" width="64" height="64"><path d="M4.2 2.8l14.6 8.1-6.3 1.5-3.1 5.9z" '
          'fill="#fff" stroke="#17141c" stroke-width="1.6" stroke-linejoin="round"/></svg>')


def stroke(name, cls="sk"):
    return '<svg class="%s" viewBox="0 0 24 24">%s</svg>' % (cls, STROKES[name])


def tile(tid, size, x, y, material, inner, extra_cls="", hide=True, ring=True):
    r = ('<div class="sqring" id="%sR" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx"></div>'
         % (tid, x, y, size, size)) if ring else ""
    return ('%s<div class="tw%s %s" id="%s" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx">'
            '<div class="%s">%s<div class="sheen"></div></div></div>'
            % (r, " hide" if hide else "", extra_cls, tid, x, y, size, size, material, inner))


def mini(name, size, cls="pearl"):
    """a small static mark tile, positioned by its parent's flow"""
    return ('<span class="mt" style="width:%dpx;height:%dpx"><span class="%s">%s</span></span>'
            % (size, size, cls, g.mark(name)))


k.css("""
.abs { position: absolute; }
.hide { opacity: 0; visibility: hidden; }
.tw { position: absolute; }
.sk { fill: none; stroke: url(#gw); stroke-width: 2.3; stroke-linecap: round; stroke-linejoin: round;
  width: 50%; height: 50%; position: relative; z-index: 1; overflow: visible; }
.pearl .sk { stroke: #17141c; }
.clear { overflow: hidden; }
.circ .jelly, .circ .pearl, .circ .clear, .circ .sheen { border-radius: 50%; }
.ghost .mk { opacity: 0.42; }
.ghost .sk { opacity: 0.42; }
.play { width: 46%; height: 46%; fill: #fff; position: relative; z-index: 1; margin-left: 6%; }
.mt { position: relative; display: inline-block; flex: none; }
.mt .pearl, .mt .jelly { position: absolute; inset: 0; }
.aurs { position: absolute; left: -700px; top: -700px; width: 2480px; height: 3320px; pointer-events: none;
  background:
    radial-gradient(circle 526px at 1560px 880px, rgba(255,110,156,0.50), rgba(255,110,156,0)),
    radial-gradient(circle 634px at 760px 2360px, rgba(222,32,74,0.55), rgba(222,32,74,0)),
    radial-gradient(circle 382px at 1480px 1910px, rgba(255,198,214,0.20), rgba(255,198,214,0)); }
.shc { position: absolute; inset: 0; border-radius: inherit; overflow: hidden; pointer-events: none; }
.shc .sheen { mix-blend-mode: normal; opacity: 0.4; }
.cur { position: absolute; width: 64px; height: 64px; z-index: 8;
  filter: drop-shadow(0 6px 10px rgba(24,4,12,0.35)); }
.ck { position: absolute; width: 120px; height: 120px; margin: -60px 0 0 -60px; border-radius: 50%;
  border: 7px solid #ff6e9c; opacity: 0; visibility: hidden; z-index: 7; }
i.rr { position: absolute; display: block; border-radius: 9px; background: rgba(23,20,28,0.13); }
i.hb { position: absolute; display: block; border-radius: 10px; background: linear-gradient(115deg, #c41434 0%, #8d0d24 100%); }

/* A · the call */
#call .pane { position: absolute; top: 30px; width: 390px; height: 290px; border-radius: 36px;
  background: linear-gradient(160deg, rgba(255,255,255,0.16) 0%, rgba(255,255,255,0.06) 100%);
  box-shadow: inset 0 1.5px 1px rgba(255,255,255,0.3); overflow: hidden; }
#call .tag { position: absolute; left: 22px; bottom: 20px; height: 48px; padding: 0 18px; border-radius: 24px;
  background: rgba(23,20,28,0.55); color: #fff; font-size: 26px; font-weight: 700; line-height: 48px; letter-spacing: 0.04em; }
#call .ctl { position: absolute; top: 340px; width: 74px; height: 74px; }
#call .hang { position: absolute; top: 340px; left: 462px; width: 130px; height: 74px; border-radius: 37px;
  background: linear-gradient(165deg, #e0204b 0%, #8d0d24 100%);
  box-shadow: inset 0 2px 1px rgba(255,255,255,0.5); display: flex; align-items: center; justify-content: center; }
#call .hang .sk { width: 50px; height: 50px; stroke: #fff; }

/* B · the process shelf */
.chev { position: absolute; fill: none; stroke: rgba(255,255,255,0.85); stroke-width: 9; stroke-linecap: round;
  stroke-linejoin: round; }
.art { position: absolute; top: 210px; width: 180px; height: 220px; }
.film { position: absolute; inset: 0; border-radius: 26px; overflow: hidden;
  background: linear-gradient(170deg, #2a1f2a 0%, #17141c 100%);
  box-shadow: inset 0 1.5px 0 rgba(255,255,255,0.16), 0 30px 60px -24px rgba(10,0,4,0.7); transform-origin: 50% 0%; }
.film .hole { position: absolute; width: 14px; height: 12px; border-radius: 3px; background: rgba(255,255,255,0.55); }
.film .fr { position: absolute; left: 34px; width: 112px; height: 58px; border-radius: 10px;
  background: linear-gradient(150deg, #ff8ab0 0%, #b4122f 100%); display: flex; align-items: center; justify-content: center; }
.film .fr.dim { background: linear-gradient(150deg, rgba(255,138,176,0.55) 0%, rgba(180,18,47,0.55) 100%); }
.film .fr .play { width: 36px; height: 36px; margin: 0 0 0 4px; }
.paper { position: absolute; border-radius: 26px; overflow: hidden;
  background: linear-gradient(172deg, #ffffff 0%, #fff9fb 60%, #fdf0f4 100%);
  box-shadow: inset 0 2px 1px #fff, 0 30px 60px -24px rgba(24,4,12,0.6); }
.scr { position: absolute; width: 150px; height: 92px; border-radius: 20px; overflow: hidden;
  background: linear-gradient(172deg, #ffffff 0%, #fff6f9 100%);
  box-shadow: inset 0 2px 1px #fff, 0 20px 40px -16px rgba(24,4,12,0.6); }
.scr .n { position: absolute; left: 14px; top: 14px; width: 34px; height: 34px; border-radius: 50%;
  background: linear-gradient(165deg, #e0204b 0%, #8d0d24 100%); color: #fff; font-size: 20px; font-weight: 900;
  line-height: 34px; text-align: center; }
.sl { position: absolute; width: 124px; height: 155px; border-radius: 18px; overflow: hidden;
  background: linear-gradient(160deg, #ffffff 0%, #fdeef3 100%);
  box-shadow: inset 0 2px 1px #fff, 0 20px 40px -16px rgba(24,4,12,0.6); }
.sl i { position: absolute; display: block; }
.sl .sph { left: 14px; top: 16px; width: 70px; height: 70px; border-radius: 14px; background: linear-gradient(150deg, #f4dfe5, #ecc8d0); }
.strike { position: absolute; fill: none; stroke: #ff6e9c; stroke-width: 16; stroke-linecap: round;
  filter: drop-shadow(0 0 14px rgba(255,110,156,0.9)); }

/* TK1 · subscriptions */
.sub { position: absolute; width: 900px; height: 170px; border-radius: 48px; overflow: hidden; color: #17141c;
  background: linear-gradient(172deg, #ffffff 0%, #fff9fb 55%, #fdf0f4 100%);
  box-shadow: inset 0 2px 1px #fff, 0 50px 100px -36px rgba(8,0,3,0.75); }
.sub .nm { position: absolute; left: 170px; top: 30px; font-size: 50px; font-weight: 700; letter-spacing: -0.02em; }
.sub .ds { position: absolute; left: 170px; top: 98px; font-size: 29px; font-weight: 500; color: rgba(23,20,28,0.46); }
.sub .rp { position: absolute; right: 36px; top: 43px; width: 84px; height: 84px; }
.sub .rp .sk { width: 56%; height: 56%; }
.plg .sk { width: 54%; height: 54%; }
.arm .tube { fill: none; stroke: rgba(255,255,255,0.30); stroke-width: 34; stroke-linecap: round; }
.arm .core { fill: none; stroke: rgba(255,255,255,0.95); stroke-width: 7; stroke-linecap: round; }
.armg { filter: drop-shadow(0 0 16px rgba(255,120,165,0.85)); }

/* I · OpenRouter */
.lbl { position: absolute; height: 64px; border-radius: 32px; color: #fff; font-size: 31px; font-weight: 700;
  line-height: 64px; text-align: center; letter-spacing: -0.01em; }

/* J/K */
.wp { position: absolute; width: 340px; height: 110px; border-radius: 55px; color: #17141c;
  background: linear-gradient(172deg, #ffffff 0%, #fff6f9 100%);
  box-shadow: inset 0 2px 1px #fff, 0 34px 70px -26px rgba(24,4,12,0.65); transform-origin: 0 0; }
.wp .nm { position: absolute; left: 112px; top: 0; line-height: 110px; font-size: 48px; font-weight: 700; letter-spacing: -0.02em; }
.chat { position: absolute; border-radius: 52px; overflow: hidden; color: #17141c;
  background: linear-gradient(172deg, #ffffff 0%, #fff9fb 55%, #fdf0f4 100%);
  box-shadow: inset 0 2px 1px #fff, 0 50px 100px -36px rgba(24,4,12,0.65); }
.chat .ti { position: absolute; font-weight: 700; letter-spacing: -0.02em; }
.inp { position: absolute; border-radius: 40px; background: #f6eaee; box-shadow: inset 0 0 0 1.5px rgba(23,20,28,0.05); }
.inp i.rr { background: rgba(23,20,28,0.16); }

/* TK2 · the chat, full frame */
.tchip { position: absolute; height: 66px; border-radius: 33px; padding: 0 24px 0 12px; display: flex; align-items: center;
  gap: 12px; background: #fbe3ea; color: #8d0d24; font-size: 29px; font-weight: 700; white-space: nowrap; }
.tchip .mt { width: 44px; height: 44px; }
.tchip.on { background: linear-gradient(165deg, #e0204b 0%, #8d0d24 100%); color: #fff; }
.vb { position: absolute; border-radius: 40px; overflow: hidden;
  background: linear-gradient(160deg, #ff8ab0 0%, #b4122f 55%, #6b081c 100%);
  box-shadow: inset 0 2px 1px rgba(255,255,255,0.5), 0 40px 80px -30px rgba(24,4,12,0.7); }
.vb .pc { position: absolute; width: 104px; height: 104px; border-radius: 50%; display: flex; align-items: center;
  justify-content: center; background: rgba(255,255,255,0.22); box-shadow: inset 0 2px 1px rgba(255,255,255,0.6); }
.vb .pc .play { width: 52px; height: 52px; margin: 0 0 0 6px; }
.vb .fn { position: absolute; left: 22px; bottom: 20px; height: 46px; padding: 0 18px; border-radius: 23px;
  background: rgba(23,20,28,0.45); color: #fff; font-size: 25px; font-weight: 700; line-height: 46px; }
.vb .bar { position: absolute; left: 22px; right: 22px; bottom: 82px; height: 8px; border-radius: 4px; background: rgba(255,255,255,0.3); }
.vb .bar b { position: absolute; left: 0; top: 0; bottom: 0; width: 34%; border-radius: 4px; background: #fff; }
.okb { position: absolute; width: 74px; height: 74px; border-radius: 50%; display: flex; align-items: center; justify-content: center;
  background: linear-gradient(165deg, #e0204b 0%, #8d0d24 100%); box-shadow: inset 0 2px 1px rgba(255,255,255,0.5); }
.okb .sk { width: 52%; height: 52%; stroke: #fff; }
.step { position: absolute; height: 76px; border-radius: 38px; padding: 0 26px 0 12px; display: flex; align-items: center;
  gap: 14px; background: #f6eaee; font-size: 33px; font-weight: 700; white-space: nowrap; color: #17141c; }
.step .via { font-weight: 500; color: rgba(23,20,28,0.5); }
.step .mt { width: 52px; height: 52px; }
.spn { position: absolute; fill: none; stroke: #b4122f; stroke-width: 7; stroke-linecap: round; stroke-dasharray: 70 40; }
.out { position: absolute; height: 230px; border-radius: 36px; overflow: hidden;
  background: #ffffff; box-shadow: inset 0 0 0 2px rgba(23,20,28,0.07), 0 24px 50px -26px rgba(24,4,12,0.45); }
.out .t-micro { position: absolute; }
.out .nb { position: absolute; left: 28px; width: 36px; height: 36px; border-radius: 50%; background: #fbe3ea; color: #b4122f;
  font-size: 21px; font-weight: 900; line-height: 36px; text-align: center; }
.dsl { position: absolute; width: 190px; height: 238px; border-radius: 26px; overflow: hidden;
  background: linear-gradient(160deg, #e0204b 0%, #ab112e 46%, #6b081c 100%);
  box-shadow: inset 0 2px 1px rgba(255,255,255,0.45), 0 40px 70px -26px rgba(30,2,10,0.75); }
.dsl i { position: absolute; display: block; }
.dsl .h1 { left: 20px; top: 26px; height: 22px; border-radius: 8px; background: #fff; }
.dsl .h2 { left: 20px; top: 58px; height: 22px; border-radius: 8px; background: #fff; }
.dsl .bd { left: 20px; height: 10px; border-radius: 5px; background: rgba(255,255,255,0.5); }
.dsl .pk { right: 18px; bottom: 18px; width: 54px; height: 54px; border-radius: 50%; background: #ff8ab0; }
.dsl .dt { left: 20px; bottom: 26px; height: 8px; border-radius: 4px; background: rgba(255,255,255,0.4); }
.okp { position: absolute; height: 84px; border-radius: 42px; display: flex; align-items: center; justify-content: center;
  background: linear-gradient(165deg, #e0204b 0%, #ab112e 46%, #6b081c 100%); color: #fff; font-size: 46px; font-weight: 900;
  letter-spacing: 0.02em; box-shadow: inset 0 2px 1px rgba(255,255,255,0.5), 0 24px 50px -20px rgba(70,4,20,0.7); }
.dots { position: absolute; display: flex; gap: 12px; }
.dots b { width: 18px; height: 18px; border-radius: 50%; background: rgba(23,20,28,0.32); display: block; }

/* L · four windows */
.win { position: absolute; width: 420px; height: 240px; border-radius: 34px; overflow: hidden; color: #17141c;
  background: linear-gradient(172deg, #ffffff 0%, #fff9fb 60%, #fdf0f4 100%);
  box-shadow: inset 0 2px 1px #fff, 0 40px 80px -30px rgba(24,4,12,0.65), 0 0 0 1px rgba(255,255,255,0.4); }
.win .tb { position: absolute; left: 0; top: 0; right: 0; height: 50px; background: #f6e6eb; }
.win .dt3 { position: absolute; top: 18px; width: 14px; height: 14px; border-radius: 50%; background: rgba(23,20,28,0.2); }
.win .nm { position: absolute; left: 112px; top: 82px; font-size: 38px; font-weight: 700; letter-spacing: -0.02em; }
.kc { position: absolute; height: 72px; padding: 0 24px; border-radius: 18px; color: #fff; font-size: 31px; font-weight: 700;
  line-height: 72px; white-space: nowrap; background: linear-gradient(170deg, #3a2a36 0%, #17141c 100%);
  box-shadow: inset 0 2px 0 rgba(255,255,255,0.22), inset 0 -6px 0 rgba(0,0,0,0.35), 0 24px 44px -16px rgba(10,0,4,0.75); }

/* N · the comment */
.cmt { position: absolute; border-radius: 65px; overflow: hidden; color: #17141c;
  background: linear-gradient(172deg, #ffffff 0%, #fff6f9 100%);
  box-shadow: inset 0 2px 1px #fff, 0 40px 80px -28px rgba(24,4,12,0.65); }
.cmt .cph { position: absolute; left: 136px; top: 0; line-height: 130px; font-size: 38px; font-weight: 500; color: rgba(23,20,28,0.58); }
.cmt .pl { position: absolute; left: 136px; top: 0; line-height: 126px; font-size: 76px; font-weight: 900; color: #b4122f; }
.post { position: absolute; border-radius: 48px; color: #fff;
  background: linear-gradient(160deg, rgba(58,22,32,0.62) 0%, rgba(24,10,15,0.55) 100%);
  -webkit-backdrop-filter: blur(26px) saturate(1.7); backdrop-filter: blur(26px) saturate(1.7);
  box-shadow: inset 0 1.5px 1px rgba(255,255,255,0.3), 0 30px 60px -24px rgba(10,0,4,0.6); }
.post .pl { position: absolute; left: 120px; top: 0; line-height: 110px; font-size: 64px; font-weight: 900; color: #fff; }
.hrt { position: absolute; width: 58px; height: 58px; fill: none; stroke: #fff; stroke-width: 2.2; stroke-linejoin: round; }
.hrt.f { fill: #ff6e9c; stroke: #ff6e9c; }
""")

L = []          # graphics html, in z order
BEATS = []


def beat(fn):
    BEATS.append(fn)
    return fn


# ===========================================================================
# A · the consultation call — her and the SMM, the SMM's clients
@beat
def a_call():
    av = "".join('<div class="tw circ hide av" id="aAv%d" style="left:%dpx;top:%dpx;width:76px;height:76px">'
                 '<div class="pearl">%s</div></div>' % (i, 200 + i * 50, 196, stroke("person"))
                 for i in range(3))
    L.append(
        '<div class="g full" id="gA">'
        '<div class="dglass edge hide" id="call" style="left:110px;top:140px;width:860px;height:450px">'
        '<div class="pane" style="left:30px"><div class="tw circ" style="left:125px;top:65px;width:140px;height:140px">'
        '<div class="pearl">%s</div></div></div>'
        '<div class="pane" id="aP2" style="left:440px"><div class="tw circ" id="aSm" style="left:125px;top:65px;width:140px;height:140px">'
        '<div class="jelly">%s</div></div>%s<div class="tag hide" id="aTag">SMM</div></div>'
        '<div class="tw circ ctl" style="left:278px"><div class="clear">%s</div></div>'
        '<div class="tw circ ctl" style="left:368px"><div class="clear">%s</div></div>'
        '<div class="hang">%s</div>'
        '<div class="shc"><div class="sheen"></div></div></div></div>'
        % (stroke("person"), stroke("person"), av, stroke("mic"), stroke("cam"), stroke("hang")))
    sfx("pop", 0.16, -2)
    sfx("click-soft", T["smm"] + 0.05)
    return js("""
  tl.set("#gA", {autoAlpha: 1}, 0);
  arr("#call", 0.12, {s: 0.7, y: 40});
  shn("#call .sheen", 0.6);
  G.bump("#aSm", @smm); tl.fromTo("#aTag", {autoAlpha: 0, y: 14}, {autoAlpha: 1, y: 0, duration: 0.35, ease: SP}, @smm+0.05);
  tl.to("#aSm", {x: -70, duration: 0.5, ease: SP}, @kliientiv-0.1);
  [0, 1, 2].forEach(function (i) { arr("#aAv" + i, @kliientiv-0.02 + i * 0.08, {s: 0.3, y: 20, d: 0.55}); });
  tl.to("#call", {scale: 0.55, y: -60, autoAlpha: 0, filter: "blur(10px)", duration: 0.32, ease: "power2.in"}, @pokazala-0.32);
  tl.set("#gA", {autoAlpha: 0}, @pokazala+0.05);""")


# ===========================================================================
# B · her process: four slots, lit one by one, an artefact under each
COLS = [40, 280, 520, 760]          # shelf-local x of each 180-wide column
SH_X, SH_Y = 50, 150


@beat
def b_process():
    ghosts = [PLAY, g.mark("googlegemini"), g.mark("openai"), g.mark("canva")]
    lit = [("jelly", PLAY), ("pearl", g.mark("googlegemini")), ("pearl", g.mark("openai")), ("pearl", g.mark("canva"))]
    h = ""
    for i, x in enumerate(COLS):
        h += ('<div class="tw ghost" style="left:%dpx;top:30px;width:140px;height:140px"><div class="clear">%s</div></div>'
              % (x + 20, ghosts[i]))
        h += tile("bT%d" % i, 140, x + 20, 30, lit[i][0], lit[i][1])
    for i in range(3):
        x0 = COLS[i] + 180 + 16
        h += ('<svg class="abs" width="40" height="60" style="left:%dpx;top:70px;overflow:visible">'
              '<path class="chev" id="bCh%d" d="M8 8 L30 30 L8 52"/></svg>' % (x0, i))
    # 0 · film strip (a long video)
    holes = "".join('<i class="hole" style="left:%dpx;top:%dpx"></i>' % (x, 14 + j * 28)
                    for x in (10, 156) for j in range(7))
    film = ('<div class="art" style="left:%dpx"><div class="film hide" id="bFilm">%s'
            '<div class="fr dim" style="top:14px"></div><div class="fr" style="top:80px">%s</div>'
            '<div class="fr dim" style="top:146px"></div></div>'
            '<div class="tw circ hide" id="bCli" style="left:118px;top:-26px;width:76px;height:76px"><div class="pearl">%s</div></div>'
            '</div>' % (COLS[0], holes, PLAY, stroke("person")))
    # 1 · transcript
    rows = "".join('<i class="rr" style="left:20px;top:%dpx;width:%dpx;height:14px;border-radius:7px"></i>' % (26 + j * 30, w)
                   for j, w in enumerate((140, 128, 140, 96, 134, 112)))
    trans = ('<div class="art" style="left:%dpx"><div class="paper hide" id="bTr" style="left:0;top:0;width:180px;height:220px">%s'
             '</div></div>' % (COLS[1], rows))
    # 2 · three scripts
    scr = "".join('<div class="scr hide" id="bSc%d" style="left:%dpx;top:%dpx"><div class="n">%d</div>'
                  '<i class="hb" style="left:58px;top:20px;width:72px;height:14px;border-radius:7px"></i>'
                  '<i class="rr" style="left:16px;top:58px;width:118px;height:11px;border-radius:6px"></i></div>'
                  % (i, 4 + i * 13, i * 64, i + 1) for i in range(3))
    scripts = '<div class="art" style="left:%dpx">%s</div>' % (COLS[2], scr)
    # 3 · slides, one by one, by hand
    sls = "".join('<div class="sl hide" id="bSl%d" style="left:%dpx;top:%dpx">'
                  '<i class="sph"></i><i class="hb" style="left:14px;top:100px;width:84px;height:14px;border-radius:7px"></i>'
                  '<i class="rr" style="left:14px;top:124px;width:62px;height:10px;border-radius:5px"></i></div>'
                  % (i, 6 + i * 11, 4 + i * 13) for i in range(5))
    slides = ('<div class="art" style="left:%dpx">%s<div class="cur hide" id="bCur" style="left:110px;top:120px">%s</div>'
              '<div class="ck" id="bCk" style="left:120px;top:126px"></div></div>' % (COLS[3], sls, CURSOR))
    strike = ('<svg class="abs" width="980" height="220" style="left:0;top:0;overflow:visible">'
              '<path class="strike" id="bStr" style="opacity:0" d="M30 112 C 300 96 680 128 950 104"/></svg>')
    L.append('<div class="g full" id="gB"><div class="shelf edge hide" id="proc" style="left:%dpx;top:%dpx;width:980px;height:460px">'
             '%s%s%s%s%s%s</div></div>' % (SH_X, SH_Y, h, film, trans, scripts, slides, strike))
    sfx("whoosh-short", T["pokazala"] - 0.05, -2)
    sfx("pop", T["dovho"] + 0.05, -1)
    sfx("click", T["dyzain"] + 0.08, -2)
    sfx("whoosh-short", T["zaivykh"] - 0.02, -1)
    return js("""
  tl.set("#gB", {autoAlpha: 1}, @pokazala-0.1);
  arr("#proc", @pokazala-0.05, {s: 0.82, y: 40});
  [0, 1, 2].forEach(function (i) { tl.set("#bCh" + i, {autoAlpha: 1}, 0); draw2("bCh" + i, @protses + i * 0.16, 0.3); });
  arr("#bT0", @video-0.05, {s: 0.6, y: 0, d: 0.6}); G.ripple("#bT0R", @video+0.2);
  tl.fromTo("#bFilm", {autoAlpha: 0, scaleY: 0.25}, {autoAlpha: 1, scaleY: 1, duration: 0.7, ease: SP}, @dovho-0.02);
  arr("#bCli", @klienta-0.02, {s: 0.3, y: 10, d: 0.55});
  /* the film goes into Gemini */
  tl.set("#bFilm", {transformOrigin: "50% 50%"}, @kydaie-0.01);
  tl.to("#bFilm", {x: 240, y: -220, scale: 0.3, autoAlpha: 0, duration: 0.45, ease: "power2.in"}, @kydaie);
  tl.to("#bCli", {x: 240, y: -220, scale: 0.3, autoAlpha: 0, duration: 0.45, ease: "power2.in"}, @kydaie);
  arr("#bT1", @gemini-0.05, {s: 0.6, y: 0, d: 0.6}); G.ripple("#bT1R", @gemini+0.2);
  tl.set("#bTr", {autoAlpha: 1}, @transkr-0.05);
  tl.fromTo("#bTr", {clipPath: "inset(0px 0px 220px 0px round 26px)"}, {clipPath: "inset(0px 0px 0px 0px round 26px)", duration: 0.75, ease: "power1.inOut"}, @transkr-0.05);
  /* the transcript goes to ChatGPT, which splits it into scripts */
  tl.to("#bTr", {x: 240, y: -220, scale: 0.3, autoAlpha: 0, duration: 0.45, ease: "power2.in"}, @potim-0.05);
  arr("#bT2", @chatgpt-0.05, {s: 0.6, y: 0, d: 0.6}); G.ripple("#bT2R", @chatgpt+0.2);
  [0, 1, 2].forEach(function (i) { arr("#bSc" + i, @dilyt+0.1 + i * 0.3, {s: 0.4, y: -30, d: 0.6}); });
  /* by hand, slide by slide, in Canva */
  [0, 1, 2].forEach(function (i) { tl.to("#bSc" + i, {x: 240, y: -220, scale: 0.3, autoAlpha: 0, duration: 0.4, ease: "power2.in"}, @vruchnu-0.4 + i * 0.05); });
  arr("#bT3", @canva-0.05, {s: 0.6, y: 0, d: 0.6}); G.ripple("#bT3R", @canva+0.2);
  bin("#bCur", @vruchnu, 6, 0.25);
  var CL = [@dyzain+0.08, @canva+0.2, @sydila, @dumala+0.05, @navishcho];
  CL.forEach(function (t, i) {
    tl.to("#bCur", {scale: 0.84, duration: 0.08}, t - 0.08); tl.to("#bCur", {scale: 1, duration: 0.25}, t);
    tl.fromTo("#bCk", {scale: 0.3, autoAlpha: 0.95}, {scale: 1.1, autoAlpha: 0, duration: 0.45, ease: "power2.out", immediateRender: false}, t);
    tl.fromTo("#bSl" + i, {autoAlpha: 0, scale: 0.5, y: -20}, {autoAlpha: 1, scale: 1, y: 0, duration: 0.45, ease: POP}, t + 0.02);
  });
  /* too many steps: a strike runs through them, the shelf shudders */
  tl.set("#bStr", {opacity: 1}, @zaivykh-0.05); draw2("bStr", @zaivykh-0.05, 0.5);
  G.haptic("#proc", @krokiv+0.02);
  tl.set("#gB", {autoAlpha: 0}, @tomu+0.75);""")


# ===========================================================================
# I · near: Claude plugs into OpenRouter -> every model; Gemini, ChatGPT out;
# Whisper + the rest fly into one chat
ICL = (50, 300, 180)        # Claude tile x, y, size
IOR = (350, 300, 180)       # OpenRouter
GRID_X = [640, 774, 908]
GRID_Y = [190, 324, 458]
GRID = ["openai", "googlegemini", "anthropic", "meta", "mistralai", "perplexity", "nvidia", "huggingface", "ollama"]
ROW6 = ["mistralai", "meta", "perplexity", "nvidia", "huggingface", "ollama"]
WP = (370, 300)             # Whisper pill
R6X0, R6Y = 238, 450        # the row of six
CHAT = (90, 120, 900, 490)  # the chat window


@beat
def i_router():
    cab = ('<svg class="cab abs" width="1080" height="700" viewBox="0 0 1080 700" style="left:0;top:0">'
           '<path class="tube hide" id="iT" d="M230 390 L350 390"/>'
           '<path class="core hide" id="iC" d="M230 390 L350 390"/>'
           '<g class="pkg"><path class="pkt" id="iP" style="opacity:0" d="M230 390 L350 390"/></g></svg>')
    wires = "".join('<path class="wire hide" id="iW%d" d="M530 390 C 590 390 580 %d 640 %d"/>' % (r, y + 56, y + 56)
                    for r, y in enumerate(GRID_Y))
    wsvg = ('<svg class="cab abs" width="1080" height="700" viewBox="0 0 1080 700" style="left:0;top:0">%s</svg>' % wires)
    grid = ""
    for n, name in enumerate(GRID):
        grid += tile("iG%d" % n, 112, GRID_X[n % 3], GRID_Y[n // 3], "clear", g.mark(name), extra_cls="gw9", ring=False)
    pair = ('<div class="abs" id="iPair" style="left:0;top:0;width:1080px;height:700px">' + cab
            + tile("iCl", ICL[2], ICL[0], ICL[1], "jelly", g.mark("claude"))
            + tile("iOR", IOR[2], IOR[0], IOR[1], "pearl", g.mark("openrouter"))
            + '<div class="lbl dglass hide" id="iLb" style="left:330px;top:500px;width:220px;position:absolute">OpenRouter</div>'
            + '</div>')
    coin = tile("iEu", 96, 488, 262, "jelly", '<span class="wmark" style="font-size:58px;color:#fff">€</span>',
                extra_cls="circ")
    gem = tile("jGe", 170, 250, 320, "pearl", g.mark("googlegemini"), ring=False)
    gpt = tile("jGp", 170, 660, 320, "pearl", g.mark("openai"), ring=False)
    x1 = tile("jX1", 76, 382, 296, "jelly", stroke("x"), extra_cls="circ", ring=False)
    x2 = tile("jX2", 76, 792, 296, "jelly", stroke("x"), extra_cls="circ", ring=False)
    cx, cy, cw, ch = CHAT
    chat = ('<div class="chat hide" id="kChat" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx">'
            '<div class="tw" style="left:40px;top:30px;width:84px;height:84px"><div class="jelly">%s</div></div>'
            '<div class="ti" data-layout-allow-overlap style="left:146px;top:44px;font-size:46px">Claude</div>'
            '<i class="hair abs" style="left:40px;top:142px;width:820px;display:block"></i>'
            '<div class="inp" style="left:40px;top:390px;width:820px;height:74px">'
            '<i class="rr" style="left:30px;top:30px;width:300px;height:14px;border-radius:7px"></i></div>'
            '<div class="okb" style="left:792px;top:398px;width:58px;height:58px">%s</div>'
            '<div class="shc"><div class="sheen"></div></div></div>'
            % (cx, cy, cw, ch, g.mark("claude"), stroke("up")))
    wp = ('<div class="wp hide" id="kWp" style="left:%dpx;top:%dpx"><span class="mt" style="position:absolute;left:17px;top:17px;'
          'width:76px;height:76px"><span class="jelly">%s</span></span><div class="nm">Whisper</div></div>'
          % (WP[0], WP[1], g.mark("openai")))
    row6 = "".join('<div class="tw hide k6" id="k6%d" style="left:%dpx;top:%dpx;width:84px;height:84px;transform-origin:0 0">'
                   '<div class="pearl">%s</div></div>' % (i, R6X0 + i * 104, R6Y, g.mark(n))
                   for i, n in enumerate(ROW6))
    L.append('<div class="g full" id="gI">' + wsvg + grid + pair + coin + gem + gpt + x1 + x2
             + chat + wp + row6 + '</div>')
    sfx("pop", T["openrouter"] + 0.02)
    sfx("sparkle", T["vsikh"] - 0.02, -2)
    sfx("kaching", T["tsinamy"] + 0.04)
    sfx("pop", T["whisper"] + 0.02)
    sfx("pop", T["vse"] + 0.08, -2)
    # flight targets into the chat (transform-origin 0 0)
    wp_x, wp_y = cx + 40 - WP[0], cy + 166 - WP[1]
    r6 = ["[%d, %d]" % (cx + 270 + i * 72 - (R6X0 + i * 104), cy + 170 - R6Y) for i in range(6)]
    return js("""
  tl.set("#gI", {autoAlpha: 1}, @napryklad-0.3);
  tl.set("#iCl", {autoAlpha: 1}, @napryklad-0.3);
  tl.set(["#iT", "#iC"], {autoAlpha: 1}, @pidkl+0.05);
  draw2("iT", @pidkl+0.05, 0.4); draw2("iC", @pidkl+0.05, 0.4);
  arr("#iOR", @openrouter-0.12, {s: 0.4, x: 40, y: 0, d: 0.7}); G.ripple("#iORR", @openrouter+0.2);
  bin("#iLb", @openrouter+0.05, 8, 0.3);
  G.packet("iP", @openrouter+0.55, 0.45);
  [0, 1, 2].forEach(function (r) { tl.set("#iW" + r, {autoAlpha: 1}, @dostup-0.05); draw2("iW" + r, @dostup-0.05 + r * 0.08, 0.4); });
  {{grid}}
  arr("#iEu", @tsinamy-0.08, {s: 0.2, y: 20, d: 0.6}); G.ripple("#iEuR", @tsinamy+0.15); shn("#iEu .sheen", @tsinamy+0.2);
  /* the wall folds back into OpenRouter, the pair goes up */
  tl.to(".gw9", {x: function (i) { return 440 - [{{gx}}][i]; }, y: function (i) { return 390 - [{{gy}}][i]; },
        scale: 0.2, autoAlpha: 0, duration: 0.42, ease: "power2.in", stagger: 0.02}, @tody-0.2);
  bout(["#iW0", "#iW1", "#iW2", "#iEu", "#iLb"], @tody-0.2, 8, 0.3);
  gsap.set("#iPair", {transformOrigin: "290px 430px"});
  tl.to("#iPair", {x: 250, y: -255, scale: 0.6, duration: 0.7, ease: SP}, @tody);
  /* not Gemini, not ChatGPT, separately */
  arr("#jGe", @gemini2-0.08, {s: 0.5, y: 30, d: 0.7});
  arr("#jX1", @gemini2+0.3, {s: 0.2, y: 0, d: 0.5});
  arr("#jGp", @chatgpt2-0.08, {s: 0.5, y: 30, d: 0.7});
  arr("#jX2", @chatgpt2+0.3, {s: 0.2, y: 0, d: 0.5});
  tl.to(["#jGe", "#jX1"], {y: 120, rotation: -8, autoAlpha: 0, duration: 0.42, ease: "power2.in"}, @okremo+0.05);
  tl.to(["#jGp", "#jX2"], {y: 120, rotation: 8, autoAlpha: 0, duration: 0.42, ease: "power2.in"}, @okremo+0.12);
  /* Whisper and the other models come out of OpenRouter */
  tl.fromTo("#kWp", {autoAlpha: 0, x: 260, y: -149, scale: 0.2}, {autoAlpha: 1, x: 0, y: 0, scale: 1, duration: 0.7, ease: POP}, @whisper-0.12);
  G.bump("#iOR", @whisper-0.12);
  [0, 1, 2, 3, 4, 5].forEach(function (i) {
    tl.fromTo("#k6" + i, {autoAlpha: 0, x: 630 - (238 + i * 104) - 13, y: 151 - 450 - 13, scale: 0.3},
              {autoAlpha: 1, x: 0, y: 0, scale: 1, duration: 0.6, ease: POP}, @kupa+0.0 + i * 0.07);
  });
  /* ... and all of it works inside one chat */
  bout("#iPair", @vse-0.05, 10, 0.3);
  arr("#kChat", @vse+0.0, {s: 0.8, y: 40, d: 0.8});
  tl.to("#kWp", {x: {{wpx}}, y: {{wpy}}, scale: 0.62, duration: 0.6, ease: SP}, @pratsiuie);
  var R6 = [{{r6}}];
  R6.forEach(function (p, i) { tl.to("#k6" + i, {x: p[0], y: p[1], scale: 0.62, duration: 0.6, ease: SP}, @pratsiuie+0.08 + i * 0.04); });
  G.bump("#kChat", @odnoho); shn("#kChat .sheen", @odnoho+0.05);
  tl.set("#gI", {autoAlpha: 0}, @tomu2+0.45);""").replace(
        "{{grid}}", "\n  ".join('arr("#iG%d", %.3f, {s: 0.3, y: 10, d: 0.6});'
                               % (n, T["vsikh"] - 0.1 + (n % 3) * 0.07 + (n // 3) * 0.1) for n in range(9))).replace(
        "{{gx}}", ",".join(str(GRID_X[n % 3] + 56) for n in range(9))).replace(
        "{{gy}}", ",".join(str(GRID_Y[n // 3] + 56) for n in range(9))).replace(
        "{{wpx}}", str(wp_x)).replace("{{wpy}}", str(wp_y)).replace("{{r6}}", ", ".join(r6))


# ===========================================================================
# L · near: before — four open apps, copy-paste between them
WINS = [("googlegemini", "Gemini", 70, 130, -3), ("openai", "ChatGPT", 590, 100, 2.5),
        ("canva", "Canva", 110, 370, 2), ("gmail", "Gmail", 560, 360, -2.5)]


@beat
def l_four():
    h = ""
    for i, (mk, nm, x, y, r) in enumerate(WINS):
        h += ('<div class="win hide" id="lW%d" style="left:%dpx;top:%dpx" data-rot="%s">'
              '<div class="tb"></div><i class="dt3" style="left:22px"></i><i class="dt3" style="left:44px"></i>'
              '<i class="dt3" style="left:66px"></i>'
              '<span class="mt" style="position:absolute;left:24px;top:70px;width:72px;height:72px"><span class="pearl">%s</span></span>'
              '<div class="nm" data-layout-allow-overlap>%s</div>'
              '<i class="rr" style="left:24px;top:164px;width:360px;height:16px;border-radius:8px"></i>'
              '<i class="rr" style="left:24px;top:192px;width:250px;height:16px;border-radius:8px"></i></div>'
              % (i, x, y, r, g.mark(mk), nm))
    kc = "".join('<div class="kc hide" id="lK%d" data-layout-allow-overlap style="left:0;top:0">%s</div>' % (i, t)
                 for i, t in enumerate(("Ctrl+C", "Ctrl+V", "Ctrl+C")))
    L.append('<div class="g full" id="gL">' + h + kc + '</div>')
    sfx("pop", T["ranishe"] + 0.02, -2)
    sfx("click-soft", T["kopipastu"] - 0.05)
    sfx("whoosh-short", T["teper"] - 0.02, -2)
    centres = [(x + 210, y + 120) for _, _, x, y, _ in WINS]
    hops = [(0, 1, T["kupa2"] + 0.05), (1, 2, T["kopipastu"] + 0.05), (2, 3, T["kopipastu"] + 0.5)]
    hj = []
    for n, (a, b, t) in enumerate(hops):
        (ax, ay), (bx, by) = centres[a], centres[b]
        hj.append('  tl.set("#lK%d", {x: %d, y: %d}, 0);' % (n, ax - 85, ay - 36))
        hj.append('  tl.fromTo("#lK%d", {autoAlpha: 0, scale: 0.4}, {autoAlpha: 1, scale: 1, duration: 0.25, ease: POP}, %.3f);' % (n, t))
        hj.append('  tl.to("#lK%d", {x: %d, y: %d, duration: 0.5, ease: "power2.inOut"}, %.3f);' % (n, bx - 85, by - 36, t + 0.2))
        hj.append('  tl.to("#lK%d", {autoAlpha: 0, scale: 0.6, duration: 0.2, ease: "power2.in"}, %.3f);' % (n, t + 0.72))
        hj.append('  G.bump("#lW%d", %.3f);' % (b, t + 0.66))
    return js("""
  tl.set("#gL", {autoAlpha: 1}, @tobto+0.2);
  [{{rots}}].forEach(function (r, i) { gsap.set("#lW" + i, {rotation: r}); });
  [@ranishe+0.0, @ranishe+0.32, @chotyry-0.05, @chotyry+0.35].forEach(function (t, i) { arr("#lW" + i, t, {s: 0.6, y: 40, d: 0.75}); });
  tl.to(["#lW0", "#lW1", "#lW2", "#lW3"], {y: -10, duration: 0.25, ease: "power2.out", stagger: 0.05}, @prohramy);
  tl.to(["#lW0", "#lW1", "#lW2", "#lW3"], {y: 0, duration: 0.35, ease: SP, stagger: 0.05}, @prohramy+0.25);
{{hops}}
  G.haptic(["#lW0", "#lW1", "#lW2", "#lW3"], @mizh+0.05);
  /* now: they all collapse into one chat */
  [0, 1, 2, 3].forEach(function (i) {
    var c = [{{cx}}][i], d = [{{cy}}][i];
    tl.to("#lW" + i, {x: 540 - c, y: 370 - d, scale: 0.25, rotation: 0, autoAlpha: 0, duration: 0.42, ease: "power2.in"}, @teper-0.08 + i * 0.03);
  });
  tl.set("#gL", {autoAlpha: 0}, @odyn2+0.2);""").replace("{{hops}}", "\n".join(hj)).replace(
        "{{cx}}", ",".join(str(c[0]) for c in centres)).replace("{{rots}}", ",".join(str(w[4]) for w in WINS)).replace("{{cy}}", ",".join(str(c[1]) for c in centres))


# ===========================================================================
# M · near: after — one chat, the video goes in
@beat
def m_one():
    chat = ('<div class="chat hide" id="mChat" style="left:140px;top:140px;width:800px;height:460px">'
            '<div class="tw" style="left:36px;top:28px;width:80px;height:80px"><div class="jelly">%s</div></div>'
            '<div class="ti" style="left:136px;top:40px;font-size:44px">Claude</div>'
            '<i class="hair abs" style="left:36px;top:132px;width:728px;display:block"></i>'
            '<div class="inp" style="left:36px;top:362px;width:728px;height:70px">'
            '<i class="rr" style="left:30px;top:28px;width:260px;height:14px;border-radius:7px"></i></div>'
            '<div class="okb" style="left:700px;top:368px;width:58px;height:58px">%s</div>'
            '<div class="shc"><div class="sheen"></div></div></div>' % (g.mark("claude"), stroke("up")))
    vb = ('<div class="vb hide" id="mVb" style="left:560px;top:290px;width:340px;height:196px">'
          '<div class="pc" style="left:118px;top:28px">%s</div><div class="bar"><b></b></div>'
          '<div class="fn">запис.mp4</div></div>' % PLAY)
    ok = tile("mOk", 64, 866, 266, "jelly", stroke("check"), extra_cls="circ", ring=False)
    L.append('<div class="g full" id="gM">' + chat + vb + ok + '</div>')
    sfx("pop", T["chat"] - 0.02)
    sfx("pop", T["kynula"] + 0.12, -2)
    return js("""
  tl.set("#gM", {autoAlpha: 1}, @odyn2-0.15);
  arr("#mChat", @odyn2-0.1, {s: 0.3, y: 0, d: 0.8});
  shn("#mChat .sheen", @chat+0.1);
  tl.fromTo("#mVb", {autoAlpha: 0, y: -360, rotation: -6, scale: 0.8}, {autoAlpha: 1, y: 0, rotation: 0, scale: 1, duration: 0.55, ease: "power3.out"}, @kynula-0.25);
  G.bump("#mChat", @kynula+0.25);
  arr("#mOk", @video3+0.1, {s: 0.2, y: 0, d: 0.5});
  tl.to(["#mChat", "#mVb", "#mOk"], {y: -40, scale: 0.9, autoAlpha: 0, filter: "blur(10px)", duration: 0.32, ease: "power2.in"}, @yakshcho-0.05);
  tl.set("#gM", {autoAlpha: 0}, @yakshcho+0.35);""")


# ===========================================================================
# N · the comment: «+»
@beat
def n_comment():
    cmt = ('<div class="cmt hide" id="nC" style="left:90px;top:380px;width:900px;height:130px">'
           '<div class="tw circ" style="left:22px;top:22px;width:86px;height:86px"><div class="pearl">%s</div></div>'
           '<div class="cph" id="nPh">Додай коментар…</div><div class="pl hide" id="nPl">+</div>'
           '<div class="tw circ" id="nS" style="left:792px;top:22px;width:86px;height:86px"><div class="jelly">%s</div></div>'
           '<div class="shc"><div class="sheen"></div></div></div>' % (stroke("person"), stroke("up")))
    post = ('<div class="post hide" id="nP" style="left:240px;top:200px;width:600px;height:110px">'
            '<div class="tw circ" style="left:18px;top:14px;width:82px;height:82px"><div class="pearl">%s</div></div>'
            '<div class="pl">+</div>'
            '<svg class="hrt" id="nH0" viewBox="0 0 24 24" style="left:516px;top:26px">%s</svg>'
            '<svg class="hrt f hide" id="nH1" viewBox="0 0 24 24" style="left:516px;top:26px">%s</svg></div>'
            % (stroke("person"), STROKES["heart"], STROKES["heart"]))
    ck = '<div class="ck" id="nCk" style="left:925px;top:445px"></div>'
    L.append('<div class="g full" id="gN">' + cmt + post + ck + '</div>')
    sfx("click-soft", T["plius"] + 0.02)
    sfx("click", T["koment"] - 0.12)
    return js("""
  tl.set("#gN", {autoAlpha: 1}, @yakshcho-0.05);
  arr("#nC", @yakshcho+0.02, {s: 0.7, y: 60, d: 0.8});
  shn("#nC .sheen", @yakshcho+0.5);
  tl.set("#nPh", {autoAlpha: 0}, @plius);
  tl.fromTo("#nPl", {autoAlpha: 0, scale: 0.4}, {autoAlpha: 1, scale: 1, duration: 0.3, ease: POP}, @plius+0.01);
  G.bump("#nS", @koment-0.12);
  tl.fromTo("#nCk", {scale: 0.3, autoAlpha: 0.95}, {scale: 1.4, autoAlpha: 0, duration: 0.5, ease: "power2.out", immediateRender: false}, @koment-0.12);
  tl.set("#nPl", {autoAlpha: 0}, @koment-0.02); tl.set("#nPh", {autoAlpha: 1}, @koment+0.02);
  tl.fromTo("#nP", {autoAlpha: 0, y: 150, scale: 0.85}, {autoAlpha: 1, y: 0, scale: 1, duration: 0.5, ease: SOFT}, @koment-0.04);
  tl.fromTo("#nH1", {autoAlpha: 0, scale: 0.3, transformOrigin: "50% 50%"}, {autoAlpha: 1, scale: 1, duration: 0.35, ease: POP}, @koment+0.3);""")


# ===========================================================================
# TK1 · over: the iris opens out of the strike — a pile of subscriptions,
# swept away; Claude lands and grows two arms with plugs
SUBS = [("openai", "ChatGPT", 60, 190, -2, "trymaty"), ("googlegemini", "Gemini", 150, 400, 1.5, "pidpysky"),
        ("kling", "Kling", -140, 610, -1.5, "kupu"), ("perplexity", "Perplexity", 320, 815, 2, "riznykh"),
        ("mistralai", "Mistral", -70, 1020, -2, "shtuchnykh")]
TKC = (390, 410, 300)       # Claude, on the takeover


@beat
def t1_subs():
    subs = ""
    for i, (mk, nm, x, y, r, w) in enumerate(SUBS):
        subs += ('<div class="sub hide" id="sS%d" style="left:%dpx;top:%dpx" data-layout-allow-overflow>'
                 '<div class="tw" style="left:30px;top:30px;width:110px;height:110px"><div class="pearl">%s</div></div>'
                 '<div class="nm">%s</div><div class="ds">Підписка · щомісяця</div>'
                 '<div class="tw circ rp"><div class="jelly">%s</div></div></div>'
                 % (i, x, y, g.mark(mk), nm, stroke("repeat")))
    arms = ('<svg class="arm abs" width="1080" height="1000" viewBox="0 0 1080 1000" style="left:0;top:0"><g class="armg">'
            '<path class="tube hide" id="sAt0" d="M398 610 C 300 620 240 560 196 470"/>'
            '<path class="tube hide" id="sAt1" d="M682 610 C 780 620 840 560 884 470"/>'
            '<path class="core hide" id="sAc0" d="M398 610 C 300 620 240 560 196 470"/>'
            '<path class="core hide" id="sAc1" d="M682 610 C 780 620 840 560 884 470"/></g></svg>')
    plugs = (tile("sPl0", 130, 126, 380, "pearl", stroke("plug"), extra_cls="circ plg")
             + tile("sPl1", 130, 824, 380, "pearl", stroke("plug"), extra_cls="circ plg"))
    L.append('<div class="g full" id="gT1"><div class="tkg"></div><div class="aurs"></div><div class="grain"></div>'
             + subs + arms + plugs + tile("sCl", TKC[2], TKC[0], TKC[1], "jelly", g.mark("claude")) + '</div>')
    sfx("whoosh-short", T["krokiv"] + 0.45)
    sfx("pop", T["trymaty"] + 0.02, -1)
    sfx("pop", T["kupu"] + 0.02, -3)
    sfx("whoosh-short", T["mozhna"] + 0.02)
    sfx("pop", T["klodu"] + 0.0)
    sfx("whoosh-short", T["ruky"] + 0.45, -2)
    tx = ICL[0] + ICL[2] / 2.0 - (TKC[0] + TKC[2] / 2.0)
    ty = ICL[1] + ICL[2] / 2.0 - (TKC[1] + TKC[2] / 2.0)
    out = js("""
  [{{rots}}].forEach(function (r, i) { gsap.set("#sS" + i, {rotation: r}); });
  G.irisOpen("#gT1", @krokiv+0.42, 540, 262, 0.7);
  drift1("#gT1", @krokiv+0.42, @napryklad-@krokiv);
  [{{subs}}].forEach(function (p, i) {
    arr("#sS" + i, p, {s: 0.7, x: (i % 2 ? 160 : -160), y: 40, d: 0.8});
  });
  tl.to(".sub .rp", {rotation: 360, duration: 0.7, ease: "power2.inOut", stagger: 0.05}, @intelekt+0.05);
  [0, 1, 2, 3, 4].forEach(function (i) {
    tl.to("#sS" + i, {x: (i % 2 ? 1300 : -1300), autoAlpha: 0, duration: 0.45, ease: "power3.in"}, @mozhna-0.05 + i * 0.05);
  });
  arr("#sCl", @svoiemu+0.05, {s: 0.3, y: 60, d: 0.85}); G.ripple("#sClR", @klodu+0.15);
  shn("#sCl .sheen", @klodu+0.2);
  [0, 1].forEach(function (i) {
    tl.set(["#sAt" + i, "#sAc" + i], {autoAlpha: 1}, @duzhe-0.05);
    draw2("sAt" + i, @duzhe-0.05, 0.5); draw2("sAc" + i, @duzhe-0.05, 0.5);
    arr("#sPl" + i, @duzhe+0.35, {s: 0.3, y: 30, d: 0.6});
  });
  tl.to(".arm .tube", {strokeWidth: 52, duration: 0.5, ease: SP}, @potuzhni);
  tl.to(".arm .core", {strokeWidth: 11, duration: 0.5, ease: SP}, @potuzhni);
  G.bump("#sCl", @potuzhni);
  tl.to("#sPl0", {x: -26, y: -34, rotation: -14, duration: 0.3, ease: "power2.out"}, @ruky);
  tl.to("#sPl1", {x: 26, y: -34, rotation: 14, duration: 0.3, ease: "power2.out"}, @ruky);
  tl.to(["#sPl0", "#sPl1"], {x: 0, y: 0, rotation: 0, duration: 0.5, ease: SP}, @ruky+0.3);
  G.ripple("#sPl0R", @ruky+0.05); G.ripple("#sPl1R", @ruky+0.05);
  /* the arms fold away, Claude moves to where it sits next, the iris closes onto it */
  bout(["#sAt0", "#sAt1", "#sAc0", "#sAc1", "#sPl0", "#sPl1"], @napryklad-0.35, 8, 0.25);
  tl.to("#sCl", {x: {{tx}}, y: {{ty}}, scale: {{sc}}, duration: 0.55, ease: SP}, @napryklad-0.3);
  G.irisClose("#gT1", @napryklad-0.05, {{cx}}, {{cy}}, 0.55);""")
    subs_t = ", ".join("%.3f" % (T[w] - 0.08) for *_, w in SUBS)
    return (out.replace("{{subs}}", subs_t).replace("{{rots}}", ",".join(str(w[4]) for w in SUBS)).replace("{{tx}}", "%.1f" % tx).replace("{{ty}}", "%.1f" % ty)
            .replace("{{sc}}", "%.3f" % (ICL[2] / float(TKC[2])))
            .replace("{{cx}}", str(ICL[0] + ICL[2] // 2)).replace("{{cy}}", str(ICL[1] + ICL[2] // 2)))


# ===========================================================================
# TK2 · over: the iris opens out of the chat — the whole pipeline in it
@beat
def t2_chat():
    chips = ('<div class="tchip hide" id="cC0" style="left:80px;top:272px">%s Whisper</div>'
             '<div class="tchip hide" id="cC1" style="left:318px;top:272px">%s OpenRouter</div>'
             '<div class="tchip hide" id="cC2" style="left:614px;top:272px">%s Дизайн-система</div>'
             % (mini("openai", 44, "jelly"), mini("openrouter", 44, "jelly"),
                '<span class="mt" style="width:44px;height:44px"><span class="jelly">'
                '<span class="wmark" style="font-size:26px;color:#fff">Aa</span></span></span>'))
    head = ('<div class="tw" id="cHd" style="left:80px;top:146px;width:100px;height:100px"><div class="jelly">%s</div></div>'
            '<div class="ti abs" data-layout-allow-overlap style="left:206px;top:166px;font-size:56px;font-weight:700;color:#17141c;letter-spacing:-0.02em">Claude</div>'
            '<i class="hair abs" style="left:80px;top:368px;width:920px;display:block"></i>' % g.mark("claude"))
    vb = ('<div class="vb hide" id="cVb" style="left:620px;top:396px;width:380px;height:222px">'
          '<div class="pc" style="left:138px;top:34px">%s</div><div class="bar"><b></b></div>'
          '<div class="fn">запис.mp4</div></div>' % PLAY)
    vok = tile("cVk", 62, 966, 376, "jelly", stroke("check"), extra_cls="circ", ring=False)
    av = tile("cAv", 62, 80, 660, "jelly", g.mark("claude"))
    step = ('<div class="step hide" id="cSt" style="left:160px;top:653px">%s<span id="cSt1">Whisper</span>'
            '<span class="via" id="cSt2">через</span><span id="cSt3" style="display:flex;align-items:center;gap:14px">%s OpenRouter</span></div>'
            % (mini("openai", 52, "jelly"), mini("openrouter", 52, "pearl")))
    spn = ('<svg class="spn hide abs" id="cSp" viewBox="0 0 60 60" width="60" height="60" style="left:830px;top:661px">'
           '<circle cx="30" cy="30" r="24"/></svg>')
    sok = tile("cSk", 60, 830, 661, "jelly", stroke("check"), extra_cls="circ", ring=False)
    trs = "".join('<i class="rr cTr" style="left:160px;top:%dpx;width:%dpx;height:18px"></i>' % (752 + j * 32, w)
                  for j, w in enumerate((800, 740, 520)))
    trw = '<div class="abs hide" id="cTrw" style="left:0;top:0;width:1080px;height:860px">%s</div>' % trs
    car_rows = "".join('<div class="nb" style="top:%dpx">%d</div>'
                       '<i class="rr cR%d" style="left:80px;top:%dpx;width:%dpx;height:16px;border-radius:8px"></i>'
                       % (78 + j * 46, j + 1, j, 88 + j * 46, w) for j, w in enumerate((300, 250, 320)))
    car = ('<div class="out hide" id="cCar" style="left:80px;top:868px;width:450px">'
           '<div class="t-micro hide" id="cCarL" style="left:28px;top:26px">КАРУСЕЛЬ</div>%s</div>' % car_rows)
    mail = ('<div class="out hide" id="cMl" style="left:550px;top:868px;width:450px">'
            '<span class="mt" style="position:absolute;left:24px;top:18px;width:52px;height:52px"><span class="pearl">%s</span></span>'
            '<div class="t-micro hide" id="cMlL" style="left:92px;top:30px">ІМЕЙЛ</div>'
            '<i class="hb cM0" style="left:28px;top:92px;width:240px;height:22px;border-radius:8px"></i>'
            '<i class="rr cM1" style="left:28px;top:134px;width:380px;height:14px;border-radius:7px"></i>'
            '<i class="rr cM2" style="left:28px;top:160px;width:330px;height:14px;border-radius:7px"></i>'
            '<i class="rr cM3" style="left:28px;top:186px;width:210px;height:14px;border-radius:7px"></i></div>'
            % stroke("mail"))
    dsl = ""
    for i, (x, r) in enumerate(((96, -5), (318, -1.6), (540, 1.6), (762, 5))):
        dsl += ('<div class="dsl hide" id="cDs%d" style="left:%dpx;top:850px;transform:rotate(%sdeg)">'
                '<i class="h1 cDh" style="width:%dpx"></i><i class="h2 cDh" style="width:%dpx"></i>'
                '<i class="bd" style="top:104px;width:130px"></i><i class="bd" style="top:124px;width:96px"></i>'
                '<i class="pk"></i><i class="dt" style="width:%dpx"></i></div>'
                % (i, x, r, (140, 120, 132, 110)[i], (96, 128, 80, 104)[i], 24 + i * 22))
    inp = ('<div class="inp abs" id="cIn" style="left:80px;top:1118px;width:920px;height:100px;border-radius:50px">'
           '<i class="rr" id="cInPh" style="left:36px;top:42px;width:340px;height:16px;border-radius:8px"></i>'
           '<div class="dots hide" id="cDots" style="left:40px;top:41px"><b></b><b></b><b></b></div></div>'
           '<div class="okb" id="cSend" style="left:910px;top:1131px">%s</div>'
           '<div class="okp hide" id="cOk" style="left:740px;top:1126px;width:244px">ОК</div>'
           '<div class="cur hide" id="cCur" style="left:0;top:0">%s</div>'
           '<div class="ck" id="cCk" style="left:862px;top:1168px"></div>' % (stroke("up"), CURSOR))
    L.append('<div class="g full" id="gT2"><div class="tkg"></div><div class="aurs"></div><div class="grain"></div>'
             '<div class="sheet hide" id="cSh" style="left:-40px;top:110px;width:1160px;height:1130px" data-layout-allow-overflow>'
             '<div class="sheen"></div></div>'
             '<div class="abs hide" id="cAll" style="left:0;top:0;width:1080px;height:1920px">'
             + head + chips + av + step + spn + sok + trw + car + mail + dsl + inp + vb + vok
             + '</div></div>')
    sfx("whoosh-short", T["tomu2"] - 0.02)
    sfx("click", T["odyn"] + 0.02, -1)
    sfx("pop", T["whisper2"] + 0.0, -2)
    sfx("typing", T["transkr2"] + 0.0, -3)
    sfx("sparkle", T["dsys"] + 0.02, -3)
    sfx("pop", T["skladaie"] + 0.02, -2)
    sfx("click", T["ok"] - 0.02)
    sfx("whoosh-short", T["oke"] + 0.02, -2)
    vbx, vby = 300 - 810, 1168 - 507          # the video sits in the input bar first
    return js("""
  G.irisOpen("#gT2", @tomu2-0.03, 540, 365, 0.7);
  drift1("#gT2", @tomu2, @oke-@tomu2);
  arr("#cSh", @tomu2+0.05, {s: 0.82, y: 30, d: 0.9}); shn("#cSh .sheen", @tomu2+0.45);
  bin("#cAll", @tomu2+0.15, 8, 0.35);
  [0, 1, 2].forEach(function (i) { arr("#cC" + i, @nalasht-0.05 + i * 0.13, {s: 0.5, y: 10, d: 0.55}); });
  /* the video is dropped in, once */
  tl.fromTo("#cVb", {autoAlpha: 0, x: {{vbx}}, y: {{vby}} - 420, scale: 0.42, rotation: -8},
            {autoAlpha: 1, x: {{vbx}}, y: {{vby}}, scale: 0.42, rotation: 0, duration: 0.5, ease: "power3.out"}, @video2-0.05);
  tl.set("#cInPh", {autoAlpha: 0}, @kydaiesh);
  G.bump("#cSend", @odyn-0.02);
  tl.to("#cVb", {x: 0, y: 0, scale: 1, duration: 0.6, ease: SP}, @odyn+0.08);
  tl.set("#cInPh", {autoAlpha: 1}, @odyn+0.3);
  arr("#cVk", @vse2+0.0, {s: 0.2, y: 0, d: 0.5});
  /* Whisper, via OpenRouter, transcribes */
  arr("#cAv", @whisper2-0.15, {s: 0.4, y: 0, d: 0.55});
  arr("#cSt", @whisper2-0.08, {s: 0.8, y: 16, d: 0.6});
  tl.fromTo("#cSt2", {autoAlpha: 0}, {autoAlpha: 1, duration: 0.2}, @cherez);
  tl.fromTo("#cSt3", {autoAlpha: 0, x: -20}, {autoAlpha: 1, x: 0, duration: 0.35, ease: SP}, @openrouter2);
  tl.set("#cSp", {autoAlpha: 1, rotation: 0, transformOrigin: "50% 50%"}, @openrouter2+0.4);
  tl.to("#cSp", {rotation: 540, duration: 1.2, ease: "none"}, @openrouter2+0.4);
  tl.set("#cSp", {autoAlpha: 0}, @claude-0.15);
  arr("#cSk", @claude-0.15, {s: 0.3, y: 0, d: 0.45});
  tl.set("#cTrw", {autoAlpha: 1}, @transkr2-0.05);
  tl.fromTo(".cTr", {scaleX: 0, transformOrigin: "0% 50%"}, {scaleX: 1, duration: 0.45, ease: "power2.out", stagger: 0.22}, @transkr2-0.05);
  /* Claude writes the carousel and the email */
  G.bump("#cAv", @claude); G.ripple("#cAvR", @claude+0.05);
  arr("#cCar", @pyshe-0.1, {s: 0.85, y: 30, d: 0.6});
  arr("#cMl", @pyshe+0.02, {s: 0.85, y: 30, d: 0.6});
  tl.fromTo([".cR0", ".cR1", ".cR2"], {scaleX: 0, transformOrigin: "0% 50%"}, {scaleX: 1, duration: 0.3, ease: "power2.out", stagger: 0.16}, @tekst);
  tl.fromTo([".cM0", ".cM1", ".cM2", ".cM3"], {scaleX: 0, transformOrigin: "0% 50%"}, {scaleX: 1, duration: 0.3, ease: "power2.out", stagger: 0.14}, @tekst+0.45);
  tl.fromTo("#cCarL", {autoAlpha: 0, y: 8}, {autoAlpha: 1, y: 0, duration: 0.25}, @karuseli);
  tl.fromTo("#cMlL", {autoAlpha: 0, y: 8}, {autoAlpha: 1, y: 0, duration: 0.25}, @imeil);
  G.bump("#cCar", @karuseli); G.bump("#cMl", @imeil);
  /* the design system lays out the slides by itself */
  tl.set("#cC2", {className: "tchip on"}, @dsys); G.bump("#cC2", @dsys);
  tl.to(["#cCar", "#cMl"], {autoAlpha: 0.18, scale: 0.94, duration: 0.4, ease: "power2.out"}, @sama);
  [0, 1, 2, 3].forEach(function (i) {
    tl.fromTo("#cDs" + i, {autoAlpha: 0, x: 280 - [96, 318, 540, 762][i], y: 40, scale: 0.4},
              {autoAlpha: 1, x: 0, y: 0, scale: 1, duration: 0.7, ease: POP}, @skladaie-0.05 + i * 0.12);
  });
  tl.fromTo(".cDh", {scaleX: 0, transformOrigin: "0% 50%"}, {scaleX: 1, duration: 0.3, ease: "power2.out", stagger: 0.06}, @slaidy);
  /* ... and waits only for your OK */
  tl.set("#cInPh", {autoAlpha: 0}, @chekaie-0.2);
  bin("#cDots", @chekaie-0.2, 6, 0.25);
  tl.to("#cDots b", {keyframes: {y: [0, -12, 0]}, duration: 0.4, ease: "sine.inOut", stagger: 0.12}, @chekaie);
  tl.to("#cDots b", {keyframes: {y: [0, -12, 0]}, duration: 0.4, ease: "sine.inOut", stagger: 0.12}, @chekaie+0.5);
  tl.to("#cSend", {autoAlpha: 0, duration: 0.2}, @chekaie-0.25);
  arr("#cOk", @chekaie-0.2, {s: 0.5, y: 10, d: 0.6});
  tl.set("#cCur", {x: 1010, y: 1300}, 0);
  bin("#cCur", @tvoie-0.4, 6, 0.2);
  tl.to("#cCur", {x: 905, y: 1180, duration: 0.6, ease: "power2.inOut"}, @tvoie-0.35);
  tl.to("#cCur", {scale: 0.84, duration: 0.08}, @ok-0.08); tl.to("#cCur", {scale: 1, duration: 0.25}, @ok);
  tl.to("#cOk", {scale: 0.93, duration: 0.08}, @ok-0.08); tl.to("#cOk", {scale: 1, duration: 0.35, ease: SP}, @ok);
  tl.fromTo("#cCk", {scale: 0.3, autoAlpha: 0.95}, {scale: 1.6, autoAlpha: 0, duration: 0.5, ease: "power2.out", immediateRender: false}, @ok);
  G.irisClose("#gT2", @oke-0.05, 540, 360, 0.5);""").replace("{{vbx}}", str(vbx)).replace("{{vby}}", str(vby))


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
def span(a, b):
    return (round(a - 0.02, 3), round(b, 3), "")


BLACKOUT = [
    span(T["pidpysky"], T["pidpyskye"]),                # the cards say «Підписка»
    span(T["openrouter"], T["openroutere"]),            # the label says OpenRouter
    span(T["whisper"], T["whispere"]),                  # the pill says Whisper
    span(T["whisper2"], T["openrouter2e"]),             # «Whisper через OpenRouter» in the step row
    span(T["karuseli"], T["karuselie"]),                # КАРУСЕЛЬ
    span(T["imeil"], T["imeile"]),                      # ІМЕЙЛ
    span(T["dsys"], T["dsyse"]),                        # the Дизайн-система chip lights
    span(T["ok"], T["oke"]),                            # the ОК button
    span(T["plius"], T["pliuse"]),                      # the comment types «+»
]


def main():
    assert not NO_PAINT, "this cut has closeups now — re-check the beats against them"
    gj = []
    for fn in BEATS:
        j = fn()
        gj.append("  /* %s */" % fn.__name__)
        gj.append(j.rstrip())
    push = ["#vid"]
    head = [g.js(), HEAD_JS,
            '  gsap.set(%s, {transformOrigin: "540px 900px"});' % json.dumps(push),
            '  tl.fromTo(%s, {scale: 1}, {scale: 1.045, duration: %.3f, ease: "none"}, 0);' % (json.dumps(push), DUR)]
    doc = k.document(
        title=u"Reel 38 — одне відео, один чат",
        plate="assets/base.mp4",
        gfx_html=g.defs() + "\n" + "\n".join(L),
        gfx_js="\n".join(head + gj),
        caps=CAPS,
        blackout=BLACKOUT,
    )
    io.open(os.path.join(HERE, "index.html"), "w", encoding="utf-8").write(doc)
    SFX.sort(key=lambda c: c["t"])
    io.open(os.path.join(HERE, "sfx.json"), "w", encoding="utf-8").write(json.dumps(SFX, indent=1))
    print("index.html  %d captions, %d beats, %d sfx cues (%.2f/s)" % (len(CAPS), len(BEATS), len(SFX), len(SFX) / DUR))


main()
