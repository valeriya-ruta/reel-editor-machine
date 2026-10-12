# -*- coding: utf-8 -*-
"""Reel 39 — «Одне правило запису для AI-монтажу». Posts 2026-10-17.

Explainer, refined glass (STYLE.md §0). The spine is two recording modes:
EXPERT reels are read off a teleprompter sentence by sentence with pauses, so
the AI cuts them perfectly; FLOW reels you cut yourself first.

The one object is **her take as a strip on a timeline** — words as bars, pauses
as gaps — and a two-way switch «Експертні | Потокові» that decides who cuts it.

Chain:  near: the people who promise «AI cuts anything» -> their promise as a
strip: Claude lands, the pauses snip out, the strip closes into a finished video
-> *«трошки брехня» — her wink, left clear* -> REC: the same take repeats, ×300,
Claude hovers with nowhere clean to cut, «?» -> the iris opens out of Claude: her
settings, the rule types itself, three takes, the last one crowned -> the iris
closes onto take 3: the cut runs crooked and a sliver of the previous word stays
-> the switch lands on «Експертні», the teleprompter lights line by line, pauses
after every sentence, a calm tick -> viewers watch her reel, «ти» doesn't know —
the reel flips over to the teleprompter -> the teleprompter tile: every blogger
and expert -> the switch flips to «Потокові»: one unbroken wave, the written
script struck out -> the iris opens out of the switch: one long take, a moment
that felt good, later cut out; Claude can't see what you felt -> the iris closes
onto Claude: 10 minutes on a stopwatch, you snip the pauses and the junk
yourself, the clean video goes to Claude -> the iris opens out of Claude: the
rule, both modes on one sheet -> the iris closes onto «Стежити».

usage: python build.py   (then: python ../tools/sfx.py mix 39)
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

CUT = json.load(io.open(os.path.join(ROOT, "work", "r39", "cut.json"), encoding="utf-8"))
DUR = 82.550           # (2477 plate frames - 0.5) / 30
FPS = 30
k = Kit(width=1080, height=1920, fps=FPS, duration=DUR)
g = Glass(["claude"])
k.css(g.css())

# NO-PAINT: cut.py found no closeups in this take. Her wink on «трошки брехня»
# (9.0-11.4) is kept clear by hand: no graphic, no sound.
NO_PAINT = [tuple(x) for x in CUT["no_paint"]] + [(9.0, 11.4)]

CAPS = k.load_captions(os.path.join(ROOT, "work", "r39", "captions.json"))


def _at(t, w=None):
    i = min(range(len(CAPS)), key=lambda i: abs(CAPS[i]["s"] - t))
    assert abs(CAPS[i]["s"] - t) < 0.05, (t, CAPS[i])
    if w is not None:
        assert CAPS[i]["w"] == w, (t, w, CAPS[i]["w"])
    return i


def fix(t, old, new):
    CAPS[_at(t, old)]["w"] = new


def merge(t1, t2, new):
    i, j = _at(t1), _at(t2)
    assert j == i + 1
    CAPS[i]["w"] = new
    CAPS[i]["e"] = CAPS[j]["e"]
    del CAPS[j]


# whisper errors the aligner kept as «her wording» — script spelling restored
fix(2.002, u"цим", u"зі")                       # «зі штучним інтелектом»
merge(6.87, 6.99, u"змонтувати")                # «з монтувати»
merge(7.45, 7.75, u"будь-які")
fix(27.06, u"криву", u"криво")
fix(27.34, u"і лежить", u"і лишає")
fix(36.43, u"калестрофа,", u"катастрофа,")
fix(39.78, u"я зараз", u"зараз")                # she said «що зараз я читаю»; the token doubled «я»
fix(60.83, u"телек", u"інтелект")
fix(68.62, u"паузу", u"паузи")
fix(69.26, u"зайви", u"зайве")
fix(81.77, u"то Підпишись", u"то підпишись")
for _a, _b in zip(CAPS, CAPS[1:]):
    _a["e"] = round(max(_a["s"] + 0.10, _b["s"] - 0.085), 3)
CAPS[-1]["e"] = min(CAPS[-1]["e"], DUR - 0.05)


def _n(s):
    return "".join(ch for ch in s.lower() if ch.isalnum())


def _hit(word, near):
    hits = [c for c in CAPS if _n(word) in [_n(x) for x in c["w"].split()]]
    c = min(hits, key=lambda c: abs(c["s"] - near))
    assert abs(c["s"] - near) < 0.6, (word, near, c["s"])
    return c


def S(word, near):
    return _hit(word, near)["s"]


def E(word, near):
    return _hit(word, near)["e"]


T = {
    # A — the promise
    "vsi": S(u"Всі", 0.32), "khto": S(u"хто", 0.9), "rozpov": S(u"розповідає", 1.04),
    "montazh": S(u"монтаж", 1.66), "claude": S("Claude", 4.23), "vyrizaty": S(u"вирізати", 5.31),
    "pauzy": S(u"паузи", 6.11), "zmont": S(u"змонтувати", 6.87), "vid": S(u"відео", 7.89),
    "nulia": S(u"нуля", 8.67), "ale": S(u"Але", 8.84),
    # B — 300 takes
    "yakshcho": S(u"Якщо", 11.6), "zapys": S(u"записуєш", 11.98), "zbyv": S(u"збиваєшся", 12.78),
    "trysta": S("300", 13.72), "trystae": E("300", 13.72), "povtor": S(u"повторюючи", 14.36),
    "odne": S(u"одне", 15.08), "slovo": S(u"слово", 15.94), "yomu": S(u"йому", 16.5),
    "vazhko": S(u"важко", 17.46), "vyriz2": S(u"вирізати", 18.04),
    # TK1 — her settings
    "mene": S(u"мене", 18.91), "nalasht": S(u"налаштуваннях", 19.11), "nalashte": E(u"налаштуваннях", 19.11),
    "shchoz": S(u"що", 20.47), "povtoriv": S(u"повторів", 21.11), "ostanniu": S(u"останню", 22.07),
    "frazu": S(u"фразу", 22.49), "frazue": E(u"фразу", 22.49), "naikr": S(u"найкраща", 23.99),
    # C — the crooked cut
    "ale2": S(u"Але", 24.9), "obrizaie": S(u"обрізає", 26.48), "kryvo": S(u"криво", 27.06),
    "lyshaie": S(u"лишає", 27.34), "chastynku": S(u"частинку", 27.72), "poper": S(u"попереднього", 28.24),
    # D — expert: teleprompter
    "tomu2": S(u"Тому", 29.9), "ekspert": S(u"експертних", 30.52), "eksperte": E(u"експертних", 30.52),
    "ya": S(u"я", 31.44), "sufl": S(u"суфлера", 32.1), "rech": S(u"речення", 32.66),
    "pauzamy": S(u"паузами", 34.1), "i": S(u"І", 35.36), "strashno": S(u"страшно", 35.74),
    "strashnoe": E(u"страшно", 35.74), "kat": S(u"катастрофа", 36.43),
    # E — nobody guesses
    "nikhto": S(u"ніхто", 37.09), "zdoh": S(u"здогадується", 37.73), "ty": S(u"Ти", 38.57),
    "neznala": S(u"знала", 39.19), "chytaiu2": S(u"читаю", 40.54), "sufl2": S(u"суфлер", 40.84),
    "skazala": S(u"сказала", 41.94),
    # F — everybody does it
    "tse": S(u"Це", 42.83), "normal": S(u"нормальний", 43.62), "koryst": S(u"користуються", 44.69),
    "blohery": S(u"блогери", 45.62), "eksperty": S(u"експерти", 46.45),
    # G — flow
    "a": S(u"А", 47.07), "potokove": S(u"потокове", 48.56), "potokovee": E(u"потокове", 48.56),
    "potik": S(u"потік", 49.95), "dumok": S(u"думок", 50.31), "propys": S(u"прописувати", 51.21),
    "napered": S(u"наперед", 51.93), "insha": S(u"інша", 52.63),
    # TK2 — what felt good
    "tomu3": S(u"Тому", 53.68), "dumaiesh": S(u"думаєш", 54.72), "vidchuv": S(u"відчувалось", 56.36),
    "dobre": S(u"добре", 56.78), "zapysu": S(u"запису", 57.4), "potim": S(u"потім", 58.03),
    "zakhot": S(u"захотіти", 59.13), "vyriz3": S(u"вирізати", 59.53), "shtuch": S(u"штучний", 60.47),
    "znaie": S(u"знає", 61.27), "vidchuv2": S(u"відчувалось", 62.02), "tsoho": S(u"цього", 63.2),
    "bachyt": S(u"бачить", 63.7),
    # H — 10 minutes, cut it yourself
    "tomu4": S(u"Тому", 64.34), "vydil": S(u"виділити", 65.86), "desiat": S("10", 66.88),
    "khvylyne": E(u"хвилин", 67.22), "vyriz4": S(u"вирізати", 68.14), "pauzy2": S(u"паузи", 68.62),
    "zaive": S(u"зайве", 69.26), "samost": S(u"самостійно", 69.68), "hotove": S(u"готове", 70.94),
    "viddav": S(u"віддавати", 71.7), "montazh2": S(u"монтаж", 72.34),
    # TK3 — the rule
    "tozh": S(u"Тому", 73.03), "pravylo": S(u"правило", 73.35), "pravyloe": E(u"правило", 73.35),
    "dlia": S(u"для", 74.31), "ekspert2": S(u"експертних", 74.45), "rilsiv2e": E(u"рілсів", 74.97),
    "chytai": S(u"читай", 75.44), "pauzamy2": S(u"паузами", 76.8), "vin": S(u"він", 77.48),
    "idealno": S(u"ідеально", 78.14), "dlia2": S(u"Для", 78.92), "potokovykh": S(u"потокових", 79.11),
    "potokovykhe": E(u"потокових", 79.11), "vyrizai": S(u"вирізай", 79.71), "sama": S(u"сама", 80.17),
    # CTA
    "yakshcho2": S(u"якщо", 80.71), "pidpysh": S(u"підпишись", 81.77),
    "dur": DUR,
}


def js(src, **extra):
    """`@name`, `@name+0.12`, `@name-0.1` -> one literal time."""
    vals = dict(T)
    vals.update(extra)

    def rep(m):
        v = vals[m.group(1)] + (float(m.group(2)) if m.group(2) else 0.0)
        return "%.3f" % v
    return re.sub(r"@([A-Za-z_]\w*)([+-]\d+(?:\.\d+)?)?", rep, src)


# ---------------------------------------------------------------------------
SFX = []


def sfx(name, t, db=0):
    if isinstance(t, str):
        t = float(js(t))
    SFX.append({"t": round(max(0.0, t), 3), "name": name, "db": db})


# ---------------------------------------------------------------------------
STROKES = {
    "check": '<path d="M5.4 12.6l4.3 4.3 8.9-9.5"/>',
    "person": '<circle cx="12" cy="8.2" r="3.6"/><path d="M4.8 20c.9-3.8 3.7-5.8 7.2-5.8s6.3 2 7.2 5.8"/>',
    "bubble": '<path d="M4 6.6A2.6 2.6 0 0 1 6.6 4h10.8A2.6 2.6 0 0 1 20 6.6v6.8a2.6 2.6 0 0 1-2.6 2.6H10.2L6 19.4V16A2.6 2.6 0 0 1 4 13.4z"/>',
    "scissors": '<circle cx="6.2" cy="6.6" r="2.7"/><circle cx="6.2" cy="17.4" r="2.7"/><path d="M8.4 8.2L19.8 17.6M8.4 15.8L19.8 6.4"/>',
    "play": '<path d="M8.6 5.8v12.4l9.8-6.2z"/>',
    "pause": '<path d="M9 6.5v11M15 6.5v11"/>',
    "eyeoff": ('<path d="M2.8 12s3.4-6.2 9.2-6.2 9.2 6.2 9.2 6.2-3.4 6.2-9.2 6.2S2.8 12 2.8 12z"/>'
               '<circle cx="12" cy="12" r="2.8"/><path d="M4.2 4.2l15.6 15.6"/>'),
    "heart": '<path d="M12 19.6s-7.4-4.5-7.4-10a4.2 4.2 0 0 1 7.4-2.7 4.2 4.2 0 0 1 7.4 2.7c0 5.5-7.4 10-7.4 10z"/>',
    "star": '<path d="M12 3.8l2.5 5.3 5.8.7-4.3 4 1.1 5.7L12 16.7l-5.1 2.8 1.1-5.7-4.3-4 5.8-.7z"/>',
    "q": '<path d="M9.1 9.1a2.9 2.9 0 1 1 4.3 2.5c-.9.5-1.4 1.1-1.4 2.1v.6"/><path d="M12 18.1v.2"/>',
    "bang": '<path d="M12 5.6v8.2M12 18.1v.2"/>',
    "cross": '<path d="M6.8 6.8l10.4 10.4M17.2 6.8L6.8 17.2"/>',
    "prompter": '<rect x="3.6" y="4.2" width="16.8" height="11.6" rx="2.2"/><path d="M7.2 8.2h9.6M7.2 11.8h6.4M12 15.8v3.4M8.4 19.6h7.2"/>',
    "wave": '<path d="M2.6 12c1.6-4.6 3.2-4.6 4.7 0s3.1 4.6 4.7 0 3.1-4.6 4.7 0 3.1 4.6 4.7 0"/>',
    "arrow": '<path d="M4 12h15M13.5 6.5L19 12l-5.5 5.5"/>',
}


def stroke(name, cls="sk"):
    return '<svg class="%s" viewBox="0 0 24 24">%s</svg>' % (cls, STROKES[name])


def tile(tid, size, x, y, material, inner, extra_cls="", hide=True, ring=True):
    r = ('<div class="sqring%s" id="%sR" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx"></div>'
         % (" rnd" if "circ" in extra_cls else "", tid, x, y, size, size)) if ring else ""
    return ('%s<div class="tw%s %s" id="%s" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx">'
            '<div class="%s">%s<div class="sheen"></div></div></div>'
            % (r, " hide" if hide else "", extra_cls, tid, x, y, size, size, material, inner))


def bars(n, x0, step, w, hmax, seed, cls="wb", y_mid=None, hmin=0.22):
    """A run of waveform bars, centred on y_mid, deterministic heights."""
    out = []
    for i in range(n):
        v = ((seed * 7919 + i * 104729) % 1000) / 1000.0
        h = int(hmax * (hmin + (1 - hmin) * (0.5 + 0.5 * abs(((i * 37 + seed * 11) % 17) / 8.5 - 1)) * (0.55 + 0.45 * v)))
        h = max(h, int(hmax * hmin))
        out.append('<i class="%s" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx"></i>'
                   % (cls, x0 + i * step, y_mid - h // 2, w, h))
    return "".join(out)


k.css("""
.abs { position: absolute; }
.hide { opacity: 0; visibility: hidden; }
.tw { position: absolute; }
.sk { fill: none; stroke: url(#gw); stroke-width: 2.3; stroke-linecap: round; stroke-linejoin: round;
  width: 50%; height: 50%; position: relative; z-index: 1; overflow: visible; }
.pearl .sk { stroke: #17141c; }
.circ .jelly, .circ .pearl, .circ .clear, .circ .sheen { border-radius: 50%; }
.sqring.rnd { border-radius: 50%; }
.aurs { position: absolute; left: -700px; top: -700px; width: 2480px; height: 3320px; pointer-events: none;
  background:
    radial-gradient(circle 526px at 1560px 880px, rgba(255,110,156,0.50), rgba(255,110,156,0)),
    radial-gradient(circle 634px at 760px 2360px, rgba(222,32,74,0.55), rgba(222,32,74,0)),
    radial-gradient(circle 382px at 1480px 1910px, rgba(255,198,214,0.20), rgba(255,198,214,0)); }
.shc { position: absolute; inset: 0; border-radius: inherit; overflow: hidden; pointer-events: none; }
.shc .sheen { mix-blend-mode: normal; opacity: 0.4; }

/* waveform bars */
i.wb, i.gb, i.ib, i.pb { position: absolute; display: block; border-radius: 999px; }
i.wb { background: linear-gradient(180deg, #ffffff 0%, #ffe3ec 100%); box-shadow: 0 6px 14px -6px rgba(24,4,12,0.4); }
i.gb { background: rgba(23,20,28,0.22); }
i.ib { background: rgba(23,20,28,0.24); }
i.pb { background: linear-gradient(180deg, #e0204b 0%, #8d0d24 100%); }
.gap { position: absolute; border-radius: 22px;
  background: repeating-linear-gradient(135deg, rgba(255,110,156,0.55) 0 10px, rgba(255,110,156,0.22) 10px 20px);
  box-shadow: inset 0 0 0 3px rgba(255,138,176,0.9); }
.grp { position: absolute; left: 0; top: 0; }

/* REC pill */
.rec { display: flex; align-items: center; justify-content: center; gap: 18px; font-size: 44px; font-weight: 900;
  letter-spacing: 0.08em; }
.rec b { width: 28px; height: 28px; border-radius: 50%; background: #ff3b5c; display: block;
  box-shadow: 0 0 18px rgba(255,59,92,0.9); }
.pill { position: absolute; border-radius: 999px; display: flex; align-items: center; justify-content: center;
  background: linear-gradient(165deg, #e0204b 0%, #ab112e 46%, #6b081c 100%); color: #fff; font-weight: 900;
  letter-spacing: -0.02em; box-shadow: inset 0 2px 1px rgba(255,255,255,0.5), 0 26px 50px -18px rgba(70,4,20,0.7); }

/* the same take, repeated */
.tk6 { position: absolute; border-radius: 34px; overflow: hidden;
  background: linear-gradient(160deg, #ffffff 0%, #fff5f8 55%, #f5dfe6 100%);
  box-shadow: inset 0 2px 1px #fff, 0 26px 50px -22px rgba(24,4,12,0.6); }

/* the settings sheet + takes */
#t1T { position: absolute; left: 140px; top: 214px; width: 930px; font-size: 66px; font-weight: 700; line-height: 1.14;
  letter-spacing: -0.02em; color: #17141c; white-space: pre-wrap; }
#t1T::after { content: ""; display: inline-block; width: 5px; height: 62px; margin-left: 4px; vertical-align: -8px;
  background: #ff6e9c; }
.take { position: absolute; border-radius: 44px; overflow: hidden;
  background: linear-gradient(172deg, #ffffff 0%, #fff9fb 55%, #fdf0f4 100%);
  box-shadow: inset 0 2px 1px #fff, 0 50px 100px -36px rgba(8,0,3,0.75); }
.take .t-micro, .blk .t-micro { position: absolute; left: 34px; top: 28px; }
.strike { position: absolute; fill: none; stroke: #ff6e9c; stroke-width: 12; stroke-linecap: round; }

/* the crooked cut */
.blk { position: absolute; border-radius: 30px; overflow: hidden;
  background: linear-gradient(160deg, #ffffff 0%, #fff5f8 55%, #f5dfe6 100%);
  box-shadow: inset 0 2px 1px #fff, 0 30px 60px -24px rgba(24,4,12,0.6); }
.blk.prev { background: linear-gradient(160deg, #ece4e8 0%, #ddd0d6 100%); }
.cutln { fill: none; stroke: #ff6e9c; stroke-width: 9; stroke-linecap: round; stroke-dasharray: 2 18;
  filter: drop-shadow(0 0 8px rgba(255,110,156,0.9)); }
.slv { fill: #ff6e9c; filter: drop-shadow(0 0 10px rgba(255,110,156,1)) drop-shadow(0 0 26px rgba(255,110,156,0.7)); }
.ringo { position: absolute; border-radius: 50%; border: 8px solid #ff8ab0;
  box-shadow: 0 0 24px rgba(255,110,156,0.8), inset 0 0 24px rgba(255,110,156,0.5); }

/* the switch */
.seg { position: absolute; }
.seg .th { position: absolute; left: 8px; top: 8px; width: 372px; height: 96px; border-radius: 48px;
  background: linear-gradient(165deg, #e0204b 0%, #ab112e 46%, #6b081c 100%);
  box-shadow: inset 0 2px 1px rgba(255,255,255,0.55), inset 0 -18px 30px -14px rgba(255,125,165,0.6),
              0 20px 40px -16px rgba(70,4,20,0.7); }
.seg .lb { position: absolute; top: 0; width: 380px; height: 112px; line-height: 112px; text-align: center;
  font-size: 42px; font-weight: 700; color: #fff; z-index: 2; letter-spacing: -0.01em; }
.seg .l0 { left: 4px; } .seg .l1 { left: 376px; }

/* the teleprompter */
.tpr .cam { position: absolute; left: 50%; top: 20px; width: 26px; height: 26px; margin-left: -13px; border-radius: 50%;
  background: #0c0a10; box-shadow: 0 0 0 4px rgba(255,255,255,0.22), inset 0 0 0 6px #2d2333; }
.tpr .ln { position: absolute; left: 70px; font-size: 38px; font-weight: 700; color: rgba(255,255,255,0.30);
  white-space: nowrap; letter-spacing: -0.01em; }
.tpr .mkr { position: absolute; left: 38px; width: 10px; height: 40px; border-radius: 5px; background: #ff6e9c;
  box-shadow: 0 0 14px rgba(255,110,156,0.9); }

/* a reel on a phone */
.phn { position: absolute; border-radius: 46px; overflow: hidden;
  background: linear-gradient(170deg, #ffffff 0%, #fff6f9 60%, #f8e6ec 100%);
  box-shadow: inset 0 2px 1px #fff, 0 44px 80px -30px rgba(24,4,12,0.6); }
.phn .sil { position: absolute; left: 30px; top: 70px; width: 160px; height: 200px; fill: none;
  stroke: rgba(23,20,28,0.28); stroke-width: 1.6; stroke-linecap: round; }
.phn i { position: absolute; display: block; border-radius: 8px; }
.ph2 i { position: absolute; display: block; border-radius: 8px; background: rgba(255,255,255,0.32); height: 16px; }
.ph2 i.on { background: #fff; box-shadow: 0 0 12px rgba(255,255,255,0.6); }

/* creators */
.igr { position: absolute; inset: -9px; border-radius: 50%;
  background: linear-gradient(135deg, #ffb3c9 0%, #ff6e9c 40%, #b4122f 100%); }

/* the doc that is struck out */
.doc { position: absolute; border-radius: 34px; overflow: hidden;
  background: linear-gradient(170deg, #ffffff 0%, #fff7fa 100%);
  box-shadow: inset 0 2px 1px #fff, 0 40px 80px -30px rgba(24,4,12,0.6); }
.doc i { position: absolute; display: block; }
.hb { border-radius: 10px; background: linear-gradient(115deg, #c41434 0%, #8d0d24 100%); }
.rr { border-radius: 8px; background: rgba(23,20,28,0.13); }
.wv { fill: none; stroke: #fff; stroke-width: 12; stroke-linecap: round;
  filter: drop-shadow(0 0 10px rgba(255,110,156,0.95)) drop-shadow(0 0 28px rgba(255,110,156,0.6)); }

/* the long take */
.ruler { position: absolute; height: 22px;
  background: repeating-linear-gradient(90deg, rgba(23,20,28,0.22) 0 3px, transparent 3px 42px); }
.hl { position: absolute; border-radius: 26px; background: rgba(255,110,156,0.20);
  box-shadow: inset 0 0 0 3px rgba(255,110,156,0.55); }
.sel { position: absolute; border-radius: 26px; border: 5px dashed #b4122f; }
.phd { position: absolute; width: 8px; border-radius: 4px; background: #e0204b; box-shadow: 0 0 14px rgba(224,32,75,0.7); }
.phd::before { content: ""; position: absolute; left: -12px; top: -14px; width: 32px; height: 22px; border-radius: 8px;
  background: #e0204b; }

/* stopwatch */
.sw { position: absolute; border-radius: 50%;
  background: linear-gradient(160deg, #ffffff 0%, #fff5f8 52%, #f5dfe6 100%);
  box-shadow: inset 0 2px 1px #fff, 0 36px 64px -22px rgba(30,4,12,0.55); }
.sw .crown { position: absolute; left: 50%; top: -26px; width: 44px; height: 30px; margin-left: -22px; border-radius: 10px;
  background: linear-gradient(165deg, #e0204b 0%, #8d0d24 100%); }
.sw svg { position: absolute; left: 0; top: 0; }
.sw .trk { fill: none; stroke: rgba(23,20,28,0.10); stroke-width: 16; }
.sw .arc { fill: none; stroke: #e0204b; stroke-width: 16; stroke-linecap: round; }
.sw .num { position: absolute; left: 0; right: 0; top: 54px; text-align: center; font-size: 70px; font-weight: 900;
  letter-spacing: -0.04em; color: #17141c; line-height: 1; }
.sw .unit { position: absolute; left: 0; right: 0; top: 126px; text-align: center; font-size: 28px; font-weight: 700;
  color: rgba(23,20,28,0.5); }
.vcard { position: absolute; border-radius: 36px;
  background: linear-gradient(160deg, #ffffff 0%, #fff5f8 52%, #f5dfe6 100%);
  box-shadow: inset 0 2px 1px #fff, 0 36px 64px -22px rgba(30,4,12,0.6); }
.vcard i { position: absolute; display: block; }

/* the rule sheet */
.rpill { position: absolute; height: 124px; border-radius: 62px; padding: 0 54px; display: flex; align-items: center;
  font-size: 62px; font-weight: 900; letter-spacing: -0.02em; color: #fff;
  background: linear-gradient(165deg, #e0204b 0%, #ab112e 46%, #6b081c 100%);
  box-shadow: inset 0 2px 1px rgba(255,255,255,0.55), 0 22px 44px -18px rgba(70,4,20,0.6); }
.rpill.pale { background: linear-gradient(165deg, #fbe3ea 0%, #f4cfd9 100%); color: #b4122f;
  box-shadow: inset 0 2px 1px #fff, 0 22px 44px -18px rgba(70,4,20,0.35); }
.arw { position: absolute; fill: none; stroke: rgba(23,20,28,0.5); stroke-width: 2.4; stroke-linecap: round;
  stroke-linejoin: round; }

/* follow */
.fl { position: absolute; border-radius: 80px; overflow: hidden;
  background: linear-gradient(160deg, #ffffff 0%, #fff5f8 52%, #f5dfe6 100%);
  box-shadow: inset 0 2px 1px #fff, 0 40px 80px -28px rgba(30,4,12,0.65); }
.fl .t { position: absolute; left: 160px; top: 0; height: 150px; line-height: 150px; font-size: 56px; font-weight: 700;
  letter-spacing: -0.02em; color: #17141c; }
.fl .on { position: absolute; inset: 0; background: linear-gradient(165deg, #e0204b 0%, #ab112e 46%, #6b081c 100%);
  opacity: 0; visibility: hidden; }
.fl .on .t { color: #fff; left: 150px; }
.ck { position: absolute; width: 120px; height: 120px; margin: -60px 0 0 -60px; border-radius: 50%;
  border: 7px solid #ff6e9c; opacity: 0; visibility: hidden; z-index: 5; }
""")

L = []
BEATS = []


def beat(fn):
    BEATS.append(fn)
    return fn


# ===========================================================================
# A · the promise: «Claude will cut any pause, edit from zero»
A_GROUPS = (6, 8, 5, 7)
A_STEP, A_W, A_GAP = 22, 12, 70
A_X0 = 540 - (sum(A_GROUPS) * A_STEP + A_GAP * 3) // 2


@beat
def a_promise():
    people = ""
    for i, x in enumerate((225, 475, 725)):
        people += tile("aP%d" % i, 130, x, 250, "pearl", stroke("person"), extra_cls="circ", ring=False)
        people += tile("aB%d" % i, 64, x + 92, 228, "jelly", stroke("bubble"), extra_cls="circ", ring=False)
    strip, x, gaps = "", A_X0, ""
    for gi, n in enumerate(A_GROUPS):
        strip += ('<div class="grp" id="ag%d">%s</div>' % (gi, bars(n, x, A_STEP, A_W, 104, gi + 3, y_mid=430)))
        x += n * A_STEP
        if gi < 3:
            gaps += '<div class="gap ag" id="agap%d" style="left:%dpx;top:380px;width:%dpx;height:100px"></div>' % (
                gi, x + 2, A_GAP - 14)
            x += A_GAP
    L.append(
        '<div class="g full" id="gA">'
        '<div class="shelf edge hide" id="aSh" style="left:70px;top:150px;width:940px;height:390px">'
        '<div class="shc"><div class="sheen"></div></div></div>'
        + people
        + '<div class="abs hide" id="aStrip" style="left:0;top:0;width:1080px;height:600px">%s%s</div>' % (gaps, strip)
        + tile("aCl", 150, 465, 190, "jelly", g.mark("claude"))
        + tile("aOk", 92, 838, 384, "jelly", stroke("play"), extra_cls="circ", ring=False)
        + '</div>')
    sfx("pop", T["vsi"] - 0.02, -3)
    sfx("whoosh-short", T["montazh"] - 0.05, -2)
    sfx("pop", T["claude"])
    sfx("click", T["vyrizaty"] + 0.1, -1)
    sfx("sparkle", T["vid"], -3)
    # after the cut the four groups close up, centred: group k moves 105 - 70k
    comp = "\n".join('  tl.to("#ag%d", {x: %d, duration: 0.55, ease: SP}, @pauzy-0.05);' % (k_, (A_GAP * 3) // 2 - A_GAP * k_)
                     for k_ in range(4))
    return js("""
  tl.set("#gA", {autoAlpha: 1}, 0.05);
  arr("#aSh", 0.08, {s: 0.85, y: 30});
  arr("#aP0", @vsi-0.02, {s: 0.4, y: 30, d: 0.7}); arr("#aB0", @vsi+0.18, {s: 0.2, y: 10, d: 0.55});
  arr("#aP1", @khto-0.06, {s: 0.4, y: 30, d: 0.7}); arr("#aB1", @khto+0.14, {s: 0.2, y: 10, d: 0.55});
  arr("#aP2", @rozpov-0.02, {s: 0.4, y: 30, d: 0.7}); arr("#aB2", @rozpov+0.18, {s: 0.2, y: 10, d: 0.55});
  bout(["#aP0", "#aP1", "#aP2", "#aB0", "#aB1", "#aB2"], @montazh-0.12, 10, 0.26);
  bin("#aStrip", @montazh+0.02, 12, 0.36);
  tl.fromTo("#aStrip .wb", {scaleY: 0.15}, {scaleY: 1, duration: 0.6, ease: SP, stagger: 0.012}, @montazh+0.05);
  arr("#aCl", @claude-0.05, {s: 0.4, y: 30}); G.ripple("#aClR", @claude+0.3);
  tl.to(".ag", {scaleX: 0, autoAlpha: 0, duration: 0.3, ease: "power2.in", stagger: 0.2}, @vyrizaty+0.05);
{{comp}}
  G.bump("#aCl", @vyrizaty+0.05);
  arr("#aOk", @vid-0.06, {s: 0.3, y: 0, d: 0.6});
  shn("#aSh .sheen", @zmont+0.1);
  G.bump("#aOk", @nulia-0.1);
  bout("#gA", @ale-0.14, 10, 0.24);""").replace("{{comp}}", js(comp))


# ===========================================================================
# B · REC — the same take, again and again, ×300; Claude has nowhere to cut
B_X0 = 125


@beat
def b_takes():
    cards = "".join(
        '<div class="tk6 hide" id="bk%d" style="left:%dpx;top:300px;width:130px;height:130px">%s</div>'
        % (i, B_X0 + i * 140, bars(6, 22, 16, 9, 70, 5, cls="ib", y_mid=65)) for i in range(6))
    L.append(
        '<div class="g full" id="gB">'
        '<div class="dglass edge rec hide" id="bRec" style="left:390px;top:120px;width:300px;height:96px;border-radius:48px">'
        '<b></b>REC</div>'
        '<div class="shelf edge hide" id="bSh" style="left:70px;top:262px;width:940px;height:206px"></div>'
        + cards
        + '<div class="pill hide" id="b300" style="left:790px;top:132px;width:220px;height:104px;font-size:60px">×300</div>'
        + tile("bCl", 130, 475, 110, "jelly", g.mark("claude"))
        + tile("bSc", 60, 570, 96, "pearl", stroke("scissors"), extra_cls="circ", ring=False)
        + tile("bQ", 66, 386, 92, "pearl", stroke("q"), extra_cls="circ", ring=False)
        + '</div>')
    sfx("click-soft", T["zapys"])
    sfx("pop", T["trysta"], -2)
    sfx("pop", T["yomu"], -3)
    times = ["@zbyv+0.05", "@zbyv+0.45", "@povtor-0.05", "@povtor+0.45", "@odne+0.1", "@slovo"]
    cj = "\n".join('  arr("#bk%d", %s, {s: 0.5, y: 24, d: 0.6});' % (i, t) for i, t in enumerate(times))
    return js("""
  tl.set("#gB", {autoAlpha: 1}, @yakshcho-0.2);
  arr("#bRec", @zapys-0.08, {s: 0.6, y: 20, d: 0.7});
  arr("#bSh", @zbyv-0.1, {s: 0.9, y: 20});
%s
  arr("#b300", @trysta-0.06, {s: 0.4, y: 20, d: 0.7});
  bout("#bRec", @yomu-0.2, 10, 0.24);
  arr("#bCl", @yomu-0.05, {s: 0.4, y: -20}); arr("#bSc", @yomu+0.2, {s: 0.2, y: 0, d: 0.5});
  tl.to(["#bCl", "#bSc"], {keyframes: {x: [0, -170, -170, 150, 150, 0]}, duration: 1.5, ease: "sine.inOut"}, @yomu+0.45);
  arr("#bQ", @vazhko-0.02, {s: 0.2, y: 0, d: 0.55});
  G.haptic("#bCl", @vazhko+0.1);""" % js(cj))


# ===========================================================================
# TK1 · the iris opens out of Claude: her settings, the rule types, three takes
TAKES_X = (60, 390, 720)


@beat
def t1_settings():
    takes = ""
    for i, x in enumerate(TAKES_X):
        takes += ('<div class="take hide" id="tk%d" style="left:%dpx;top:820px;width:300px;height:220px">'
                  '<span class="t-micro">ДУБЛЬ %d</span>%s<div class="shc"><div class="sheen"></div></div></div>'
                  % (i, x, i + 1, bars(10, 34, 23, 12, 90, 5, cls="ib" if i < 2 else "pb", y_mid=140)))
    strikes = ('<svg class="abs" width="1080" height="1920" style="left:0;top:0;overflow:visible">'
               '<path class="strike hide" id="st0" d="M90 1000 L330 860"/>'
               '<path class="strike hide" id="st1" d="M420 1000 L660 860"/></svg>')
    sheet = ('<div class="sheet hide" id="t1S" style="left:-60px;top:170px;width:1200px;height:520px" '
             'data-layout-allow-overflow>'
             '<div class="tw" style="left:140px;top:52px;width:96px;height:96px"><div class="pearl">%s</div></div>'
             '<span class="t-micro abs" style="left:268px;top:64px">НАЛАШТУВАННЯ</span>'
             '<span class="t-title abs" style="left:268px;top:98px">Монтаж</span>'
             '<div class="hair abs" id="t1Hr" style="left:140px;top:178px;width:920px"></div>'
             '<div id="t1T"></div><div class="shc"><div class="sheen"></div></div></div>' % g.mark("claude"))
    L.append(
        '<div class="g full" id="gT1"><div class="tkg"></div><div class="aurs"></div><div class="grain"></div>'
        + sheet + takes + strikes
        + tile("tkSt", 96, 960, 784, "jelly", stroke("star"), extra_cls="circ")
        + '</div>')
    sfx("whoosh-short", T["mene"] - 0.32)
    sfx("typing", T["shchoz"] + 0.02, -1)
    sfx("click", T["ostanniu"] + 0.05, -1)
    sfx("pop", T["naikr"] + 0.02, -2)
    return js("""
  G.irisOpen("#gT1", @mene-0.34, 540, 175, 0.6);
  drift1("#gT1", @mene-0.34, 6.6);
  tl.set("#gB", {autoAlpha: 0}, @mene+0.3);
  arr("#t1S", @mene-0.1, {s: 0.8, y: 60, d: 0.85});
  shn("#t1S .sheen", @nalasht+0.1);
  [0, 1, 2].forEach(function (i) { arr("#tk" + i, @povtoriv-0.12 + i * 0.16, {s: 0.6, y: 50, d: 0.75}); });
  tl.to(["#tk0", "#tk1"], {autoAlpha: 0.45, scale: 0.94, duration: 0.4, ease: SP}, @ostanniu);
  tl.set(["#st0", "#st1"], {autoAlpha: 1}, @ostanniu+0.05);
  draw2("st0", @ostanniu+0.05, 0.3); draw2("st1", @ostanniu+0.15, 0.3);
  tl.to("#tk2", {y: -26, scale: 1.08, duration: 0.6, ease: SP}, @ostanniu+0.1);
  arr("#tkSt", @naikr-0.04, {s: 0.2, y: 0, d: 0.6}); G.ripple("#tkStR", @naikr+0.25);
  shn("#tk2 .sheen", @naikr+0.1);
  /* take 3 carries on: it moves to where the next beat's strip will be */
  bout(["#t1S", "#tk0", "#tk1", "#st0", "#st1", "#tkSt"], @ale2-0.5, 10, 0.28);
  tl.to("#tk2", {x: -330, y: -575, scale: 0.8, duration: 0.45, ease: "power2.inOut"}, @ale2-0.48);
  G.irisClose("#gT1", @ale2-0.12, 540, 330, 0.45);""")


# ===========================================================================
# C · the crooked cut: a sliver of the previous word stays on take 3
@beat
def c_crooked():
    svg = ('<svg class="abs" width="1080" height="700" style="left:0;top:0;overflow:visible">'
           '<path class="cutln hide" id="cLn" d="M566 222 L446 474"/>'
           '<polygon class="slv hide" id="cSl" points="510,343 510,420 473,420"/></svg>')
    L.append(
        '<div class="g full" id="gC">'
        '<div class="shelf edge hide" id="cSh" style="left:70px;top:160px;width:940px;height:370px"></div>'
        '<div class="blk prev hide" id="cPrev" style="left:150px;top:270px;width:360px;height:150px">'
        '<span class="t-micro">ДУБЛЬ 2</span>%s</div>'
        '<div class="blk hide" id="cTake" style="left:510px;top:270px;width:420px;height:150px">'
        '<span class="t-micro">ДУБЛЬ 3</span>%s</div>'
        % (bars(12, 34, 25, 12, 66, 5, cls="ib", y_mid=100), bars(14, 34, 26, 12, 66, 5, cls="pb", y_mid=100))
        + svg
        + tile("cSc", 92, 520, 176, "jelly", stroke("scissors"), extra_cls="circ", ring=False)
        + '<div class="ringo hide" id="cRg" style="left:405px;top:300px;width:170px;height:170px"></div>'
        + tile("cBg", 66, 334, 300, "jelly", stroke("bang"), extra_cls="circ", ring=False)
        + '</div>')
    sfx("whoosh-short", T["obrizaie"], -2)
    sfx("pop", T["chastynku"], -2)
    return js("""
  tl.set("#gC", {autoAlpha: 1}, @ale2+0.0);
  bin("#cSh", @ale2+0.0, 12, 0.36);
  bin(["#cPrev", "#cTake"], @ale2+0.05, 10, 0.3);
  arr("#cSc", @obrizaie-0.35, {s: 0.3, y: -20, d: 0.6});
  tl.set("#cLn", {autoAlpha: 1}, @obrizaie);
  draw2("cLn", @obrizaie, 0.5);
  tl.to("#cSc", {x: -120, y: 252, rotation: 25, duration: 0.5, ease: "power2.inOut"}, @obrizaie);
  bout("#cSc", @kryvo+0.15, 8, 0.25);
  tl.set("#cSl", {autoAlpha: 1}, @lyshaie-0.05);
  tl.to("#cPrev", {x: -110, autoAlpha: 0.25, duration: 0.5, ease: SP}, @lyshaie);
  tl.fromTo("#cRg", {autoAlpha: 0, scale: 0.4}, {autoAlpha: 1, scale: 1, duration: 0.55, ease: POP}, @chastynku-0.04);
  arr("#cBg", @poper-0.04, {s: 0.2, y: 0, d: 0.55});
  G.haptic("#cTake", @poper+0.1);
  bout("#gC", @tomu2-0.22, 10, 0.24);""")


# ===========================================================================
# D · «Експертні»: the teleprompter, sentence by sentence, pauses between
PROMPT_LINES = (u"я читаю з суфлера", u"речення за реченням,", u"з паузами між ними.", u"І це не страшно,")


def seg_html(sid):
    return ('<div class="dglass edge seg hide" id="%s" style="left:160px;top:110px;width:760px;height:112px;border-radius:56px">'
            '<div class="th" id="%sTh"></div><span class="lb l0" id="%sL0">Експертні</span>'
            '<span class="lb l1" id="%sL1" style="opacity:0.55">Потокові</span></div>' % (sid, sid, sid, sid))


@beat
def d_expert():
    lines = "".join('<span class="ln" id="pl%d" style="top:%dpx">%s</span>' % (i, 62 + i * 54, t)
                    for i, t in enumerate(PROMPT_LINES))
    pz = "".join(tile("pz%d" % i, 46, 190 + 520 + (i * 20), 260 + 62 + i * 54 - 2, "jelly", stroke("pause"),
                      extra_cls="circ", ring=False) for i in range(3))
    L.append(
        '<div class="g full" id="gD">' + seg_html("seg")
        + '<div class="dglass edge tpr hide" id="tp" style="left:190px;top:262px;width:700px;height:290px;border-radius:48px">'
        '<div class="cam"></div>%s<div class="mkr" id="pMk" style="top:62px"></div></div>' % lines
        + pz
        + tile("pOk", 80, 846, 236, "jelly", stroke("check"), extra_cls="circ")
        + '</div>')
    sfx("click", T["ekspert"] - 0.02)
    sfx("pop", T["ya"] - 0.1, -2)
    sfx("click-soft", T["pauzamy"] + 0.05, -2)
    sfx("pop", T["strashno"], -3)
    return js("""
  tl.set("#gD", {autoAlpha: 1}, @tomu2-0.12);
  arr("#seg", @tomu2-0.1, {s: 0.8, y: 30});
  tl.fromTo("#segTh", {autoAlpha: 0, scale: 0.6}, {autoAlpha: 1, scale: 1, duration: 0.5, ease: POP}, @ekspert-0.08);
  arr("#tp", @ya-0.2, {s: 0.7, y: 40});
  tl.fromTo("#pMk", {autoAlpha: 0}, {autoAlpha: 1, duration: 0.2}, @ya);
  tl.to("#pl0", {color: "#ffffff", duration: 0.2}, @ya);
  [["#pl1", @rech-0.05, 1], ["#pl2", @pauzamy-0.25, 2], ["#pl3", @i-0.05, 3]].forEach(function (p) {
    tl.to(p[0], {color: "#ffffff", duration: 0.2}, p[1]);
    tl.to("#pl" + (p[2] - 1), {color: "rgba(255,255,255,0.30)", duration: 0.25}, p[1]);
    tl.to("#pMk", {y: p[2] * 54, duration: 0.35, ease: SP}, p[1]);
  });
  [0, 1, 2].forEach(function (i) { arr("#pz" + i, @pauzamy+0.02 + i * 0.12, {s: 0.2, y: 0, d: 0.5}); });
  arr("#pOk", @strashno-0.04, {s: 0.2, y: 0, d: 0.55}); G.ripple("#pOkR", @strashno+0.2);
  G.bump("#tp", @kat);
  bout("#gD", @nikhto-0.2, 10, 0.24);""")


# ===========================================================================
# E · nobody guesses — «ти» didn't know: the reel flips over to the teleprompter
@beat
def e_nobody():
    av = ""
    for i, (x, y) in enumerate(((120, 190), (250, 330), (720, 330), (850, 190))):
        av += tile("eV%d" % i, 110, x, y, "pearl", stroke("person"), extra_cls="circ")
    phone = ('<div class="phn hide" id="ph" style="left:430px;top:130px;width:220px;height:400px">'
             '<svg class="sil" viewBox="0 0 24 24"><circle cx="12" cy="8.2" r="3.6"/>'
             '<path d="M4.8 20c.9-3.8 3.7-5.8 7.2-5.8s6.3 2 7.2 5.8"/></svg>'
             '<i style="left:44px;top:300px;width:132px;height:22px;background:rgba(23,20,28,0.85)"></i>'
             '<i style="left:24px;top:22px;width:56px;height:12px;background:rgba(23,20,28,0.14)"></i>'
             '<i style="left:180px;top:200px;width:16px;height:16px;border-radius:50%;background:rgba(23,20,28,0.18)"></i>'
             '<i style="left:180px;top:236px;width:16px;height:16px;border-radius:50%;background:rgba(23,20,28,0.18)"></i>'
             '</div>')
    ph2 = ('<div class="dglass edge ph2 hide" id="ph2" style="left:430px;top:130px;width:220px;height:400px;border-radius:46px">'
           '<div class="cam" style="position:absolute;left:97px;top:18px;width:26px;height:26px;border-radius:50%;'
           'background:#0c0a10;box-shadow:0 0 0 4px rgba(255,255,255,0.22)"></div>'
           + "".join('<i class="%s" style="left:30px;top:%dpx;width:%dpx"></i>'
                     % ("on" if j == 2 else "", 90 + j * 46, w) for j, w in enumerate((160, 128, 150, 104, 140, 92)))
           + '</div>')
    L.append('<div class="g full" id="gE">' + av + phone + ph2
             + tile("eQ", 64, 812, 316, "pearl", stroke("q"), extra_cls="circ", ring=False)
             + tile("eB", 64, 812, 316, "jelly", stroke("bang"), extra_cls="circ", ring=False)
             + '</div>')
    sfx("pop", T["nikhto"] - 0.05, -3)
    sfx("pop", T["ty"], -2)
    sfx("whoosh-short", T["sufl2"] - 0.1, -3)
    return js("""
  tl.set("#gE", {autoAlpha: 1}, @nikhto-0.2);
  arr("#ph", @nikhto-0.15, {s: 0.7, y: 40});
  [0, 1, 2, 3].forEach(function (i) { arr("#eV" + i, @nikhto+0.05 + i * 0.1, {s: 0.4, y: 30, d: 0.7}); });
  tl.to(["#eV0", "#eV1", "#eV3"], {autoAlpha: 0.45, scale: 0.9, duration: 0.4, ease: SP}, @ty-0.04);
  tl.to("#eV2", {scale: 1.25, duration: 0.6, ease: POP}, @ty-0.04); G.ripple("#eV2R", @ty+0.15);
  arr("#eQ", @neznala-0.04, {s: 0.2, y: 0, d: 0.55});
  tl.to("#ph", {rotationY: 90, transformPerspective: 900, duration: 0.22, ease: "power2.in"}, @sufl2-0.2);
  tl.set("#ph", {autoAlpha: 0}, @sufl2+0.02);
  tl.set("#ph2", {autoAlpha: 1, rotationY: -90, transformPerspective: 900}, @sufl2+0.02);
  tl.to("#ph2", {rotationY: 0, duration: 0.6, ease: FLIP}, @sufl2+0.02);
  tl.to("#eQ", {autoAlpha: 0, scale: 0.6, duration: 0.2}, @skazala);
  arr("#eB", @skazala+0.02, {s: 0.2, y: 0, d: 0.5});
  bout(["#eV0", "#eV1", "#eV2", "#eV3", "#eB"], @tse-0.18, 10, 0.24);
  tl.to("#ph2", {x: 0, y: -40, scale: 0.4, autoAlpha: 0, duration: 0.35, ease: "power2.in"}, @tse-0.2);
  tl.set("#gE", {autoAlpha: 0}, @tse+0.2);""")


# ===========================================================================
# F · every blogger and expert does it
@beat
def f_everyone():
    cr = ""
    rows = [(130 + i * 175, 268) for i in range(5)] + [(217 + i * 175, 404) for i in range(4)]
    for i, (x, y) in enumerate(rows):
        cr += ('<div class="tw hide circ" id="fC%d" style="left:%dpx;top:%dpx;width:100px;height:100px">'
               '<div class="igr"></div><div class="pearl" style="inset:4px">%s</div></div>' % (i, x, y, stroke("person")))
    L.append('<div class="g full" id="gF">'
             + tile("fTp", 170, 455, 140, "jelly", stroke("prompter"))
             + tile("fOk", 70, 590, 120, "pearl", stroke("check"), extra_cls="circ", ring=False)
             + cr + '</div>')
    sfx("pop", T["tse"] - 0.05, -3)
    sfx("pop", T["blohery"], -2)
    return js("""
  tl.set("#gF", {autoAlpha: 1}, @tse-0.2);
  arr("#fTp", @tse-0.12, {s: 0.4, y: 30});
  arr("#fOk", @normal+0.1, {s: 0.2, y: 0, d: 0.5});
  G.ripple("#fTpR", @koryst); G.bump("#fTp", @koryst);
  tl.to("#fOk", {autoAlpha: 0, scale: 0.5, duration: 0.2, ease: "power2.in"}, @blohery-0.32);
  tl.to("#fTp", {scale: 0.62, y: -62, duration: 0.5, ease: SP}, @blohery-0.3);
  [0, 1, 2, 3, 4].forEach(function (i) { arr("#fC" + i, @blohery-0.1 + i * 0.07, {s: 0.4, y: 30, d: 0.7}); });
  [5, 6, 7, 8].forEach(function (i) { arr("#fC" + i, @eksperty-0.3 + (i - 5) * 0.07, {s: 0.4, y: 30, d: 0.7}); });
  bout("#gF", @a-0.16, 10, 0.24);""")


# ===========================================================================
# G · the switch flips to «Потокові»: one unbroken wave, the script struck out
def wave_path(x0, x1, y, amp, period):
    pts, x = [], x0
    d = "M%d %d" % (x0, y)
    sgn = -1
    while x < x1:
        nx = min(x + period / 2.0, x1)
        d += " Q %.1f %.1f %.1f %d" % ((x + nx) / 2.0, y + sgn * amp * (1.0 if (x // period) % 3 else 0.6), nx, y)
        sgn = -sgn
        x = nx
    return d


@beat
def g_flow():
    doc = ('<div class="doc hide" id="gDoc" style="left:700px;top:262px;width:230px;height:270px">'
           '<i class="hb" style="left:28px;top:30px;width:120px;height:22px"></i>'
           + "".join('<i class="rr" style="left:28px;top:%dpx;width:%dpx;height:14px"></i>' % (76 + j * 30, w)
                     for j, w in enumerate((174, 160, 120, 168, 140, 96)))
           + '</div>')
    L.append('<div class="g full" id="gG">' + seg_html("sg2")
             + '<div class="shelf edge hide" id="gSh" style="left:110px;top:270px;width:540px;height:250px"></div>'
             + '<svg class="abs" width="1080" height="700" style="left:0;top:0;overflow:visible">'
             '<path class="wv hide" id="gWv" d="%s"/>'
             '<path class="strike hide" id="gSt" d="M716 512 L914 282"/></svg>' % wave_path(150, 610, 395, 62, 92)
             + doc
             + tile("gX", 84, 872, 236, "jelly", stroke("cross"), extra_cls="circ")
             + '</div>')
    sfx("click", T["potokove"] - 0.02)
    sfx("whoosh-short", T["potik"], -4)
    sfx("click", T["napered"] + 0.02, -1)
    return js("""
  tl.set("#gG", {autoAlpha: 1}, @a-0.1);
  arr("#sg2", @a-0.06, {s: 0.8, y: 30});
  tl.to("#sg2Th", {x: 372, duration: 0.6, ease: SP}, @potokove-0.08);
  tl.to("#sg2L0", {opacity: 0.55, duration: 0.25}, @potokove-0.05);
  tl.to("#sg2L1", {opacity: 1, duration: 0.25}, @potokove-0.05);
  arr("#gSh", @potik-0.4, {s: 0.85, y: 20});
  tl.set("#gWv", {autoAlpha: 1}, @potik-0.1);
  draw2("gWv", @potik-0.1, 1.0);
  arr("#gDoc", @propys-0.05, {s: 0.6, y: 30});
  tl.set("#gSt", {autoAlpha: 1}, @napered-0.04);
  draw2("gSt", @napered-0.04, 0.3);
  tl.to("#gDoc", {autoAlpha: 0.5, scale: 0.95, duration: 0.35}, @napered+0.1);
  arr("#gX", @napered-0.02, {s: 0.2, y: 0, d: 0.55}); G.ripple("#gXR", @napered+0.2);
  G.bump("#sg2", @insha);
  bout(["#gSh", "#gWv", "#gDoc", "#gSt", "#gX"], @tomu3-0.45, 10, 0.25);""")


# ===========================================================================
# TK2 · the iris opens out of the switch: one long take; the moment that felt
# good gets cut later; Claude can't see what you felt
N_L, N_S, N_R = 18, 10, 16
T2_STEP = 21


@beat
def t2_stream():
    x0 = 140
    left = bars(N_L, x0, T2_STEP, 12, 210, 9, cls="gb", y_mid=270)
    segx = x0 + N_L * T2_STEP
    seg = bars(N_S, segx, T2_STEP, 12, 210, 4, cls="gb sb", y_mid=270)
    rx = segx + N_S * T2_STEP
    right = bars(N_R, rx, T2_STEP, 12, 210, 2, cls="gb", y_mid=270)
    sheet = (
        '<div class="sheet hide" id="t2S" style="left:-60px;top:250px;width:1200px;height:470px" data-layout-allow-overflow>'
        '<div class="chip abs" style="left:140px;top:36px"><b style="width:18px;height:18px;border-radius:50%%;'
        'background:#e0204b;display:block"></b>REC</div>'
        '<div class="ruler" style="left:140px;top:116px;width:930px"></div>'
        '<div class="grp" id="t2L">%s</div>'
        '<div class="grp" id="t2G"><div class="hl hide" id="t2Hl" style="left:%dpx;top:150px;width:%dpx;height:240px"></div>'
        '<div class="sel hide" id="t2Sel" style="left:%dpx;top:142px;width:%dpx;height:256px"></div>%s</div>'
        '<div class="grp" id="t2R">%s</div>'
        '<div class="phd" id="t2Ph" style="left:136px;top:120px;height:300px"></div>'
        '</div>' % (left, segx - 14, N_S * T2_STEP + 6, segx - 22, N_S * T2_STEP + 22, seg, right))
    hx = 60 + segx + (N_S * T2_STEP) // 2 - 60 - 45
    L.append(
        '<div class="g full" id="gT2"><div class="tkg"></div><div class="aurs"></div><div class="grain"></div>'
        + sheet
        + tile("t2H", 90, hx, 196, "jelly", stroke("heart"), extra_cls="circ")
        + tile("t2Sc", 84, hx + 3, 196, "pearl", stroke("scissors"), extra_cls="circ", ring=False)
        + tile("t2Cl", 220, 430, 830, "jelly", g.mark("claude"))
        + '<div class="tw hide circ" id="t2Gh" style="left:236px;top:860px;width:120px;height:120px">'
          '<div class="clear">%s</div></div>' % stroke("heart")
        + tile("t2Q", 76, 612, 808, "pearl", stroke("q"), extra_cls="circ", ring=False)
        + tile("t2Eye", 92, 604, 800, "pearl", stroke("eyeoff"), extra_cls="circ", ring=False)
        + '</div>')
    sfx("whoosh-short", T["tomu3"] - 0.28)
    sfx("pop", T["vidchuv"] + 0.1, -2)
    sfx("whoosh-short", T["vyriz3"], -2)
    sfx("pop", T["shtuch"] - 0.05, -3)
    run_end = 140 + (N_L + N_S + N_R) * T2_STEP
    return js("""
  G.irisOpen("#gT2", @tomu3-0.3, 726, 166, 0.6);
  drift1("#gT2", @tomu3-0.3, 10.6);
  tl.set("#gG", {autoAlpha: 0}, @tomu3+0.3);
  arr("#t2S", @tomu3-0.12, {s: 0.82, y: 60, d: 0.85});
  tl.fromTo("#t2S .gb", {scaleY: 0.1}, {scaleY: 1, duration: 0.6, ease: SP, stagger: 0.01}, @tomu3+0.05);
  tl.to("#t2Ph", {x: {{phx}}, duration: {{phd}}, ease: "none"}, @dumaiesh-0.3);
  tl.fromTo("#t2Hl", {autoAlpha: 0, scaleX: 0.3}, {autoAlpha: 1, scaleX: 1, duration: 0.45, ease: SP}, @vidchuv-0.02);
  tl.to("#t2S .sb", {backgroundColor: "#c41434", duration: 0.3, stagger: 0.03}, @vidchuv-0.02);
  arr("#t2H", @vidchuv+0.05, {s: 0.2, y: 20, d: 0.6}); G.ripple("#t2HR", @dobre+0.05); G.bump("#t2H", @dobre);
  tl.to("#t2H", {autoAlpha: 0, scale: 0.6, duration: 0.25, ease: "power2.in"}, @potim-0.05);
  tl.fromTo("#t2Sel", {autoAlpha: 0, scale: 1.08}, {autoAlpha: 1, scale: 1, duration: 0.4, ease: SP}, @potim);
  arr("#t2Sc", @zakhot-0.1, {s: 0.2, y: 0, d: 0.5});
  tl.to("#t2G", {y: 330, rotation: 7, transformOrigin: "{{sgc}}px 270px", autoAlpha: 0, duration: 0.55, ease: "power2.in"}, @vyriz3);
  tl.to("#t2Sc", {y: 40, autoAlpha: 0, duration: 0.3, ease: "power2.in"}, @vyriz3);
  tl.to("#t2R", {x: -{{segw}}, duration: 0.55, ease: SP}, @vyriz3+0.45);
  arr("#t2Cl", @shtuch-0.08, {s: 0.4, y: 60}); G.ripple("#t2ClR", @shtuch+0.3);
  arr("#t2Q", @znaie-0.04, {s: 0.2, y: 0, d: 0.5});
  tl.fromTo("#t2Gh", {autoAlpha: 0, scale: 0.5}, {autoAlpha: 0.55, scale: 1, duration: 0.6, ease: SOFT}, @vidchuv2-0.05);
  tl.to("#t2Q", {autoAlpha: 0, scale: 0.6, duration: 0.2}, @tsoho-0.1);
  arr("#t2Eye", @tsoho-0.05, {s: 0.2, y: 0, d: 0.55});
  G.haptic("#t2Cl", @bachyt);
  /* Claude carries on: it moves to its seat in the next beat */
  bout(["#t2S", "#t2Gh", "#t2Eye"], @tomu4-0.55, 10, 0.26);
  tl.to("#t2Cl", {x: 355, y: -600, scale: 0.68, duration: 0.45, ease: "power2.inOut"}, @tomu4-0.55);
  G.irisClose("#gT2", @tomu4-0.18, 895, 340, 0.45);""").replace("{{phx}}", str(run_end - 140)).replace("{{phd}}", "%.3f" % (T["zapysu"] - T["dumaiesh"] + 0.4)).replace(
        "{{segw}}", str(N_S * T2_STEP)).replace("{{sgc}}", str(140 + N_L * T2_STEP + N_S * T2_STEP // 2))


# ===========================================================================
# H · 10 minutes, cut the pauses and the junk yourself, hand the clean video over
@beat
def h_self():
    # strip: g0 [gap] g1 [junk] g2 , x 350..
    x = 352
    g0 = bars(4, x, 22, 12, 84, 3, y_mid=345); x += 4 * 22
    gap = '<div class="gap" id="hGap" style="left:%dpx;top:300px;width:40px;height:90px"></div>' % (x + 2); x += 48
    g1 = bars(5, x, 22, 12, 84, 6, y_mid=345); x += 5 * 22
    junk = ('<div class="gap" id="hJunk" style="left:%dpx;top:300px;width:64px;height:90px;'
            'background:repeating-linear-gradient(45deg, rgba(23,20,28,0.30) 0 8px, rgba(23,20,28,0.10) 8px 16px);'
            'box-shadow:inset 0 0 0 3px rgba(255,255,255,0.7)"></div>' % (x + 2)); x += 72
    g2 = bars(4, x, 22, 12, 84, 8, y_mid=345)
    sw = ('<div class="sw hide" id="hSw" style="left:112px;top:248px;width:200px;height:200px">'
          '<div class="crown"></div>'
          '<svg width="200" height="200" viewBox="0 0 200 200"><circle class="trk" cx="100" cy="100" r="80"/>'
          '<path class="arc" id="hArc" d="M100 20 A80 80 0 0 1 169.3 60"/></svg>'
          '<div class="num">10</div><div class="unit">хв</div></div>')
    vc = ('<div class="vcard hide" id="hVid" style="left:420px;top:270px;width:270px;height:150px">'
          '<div class="tw circ" style="left:24px;top:36px;width:78px;height:78px"><div class="jelly">%s</div></div>'
          '<i class="hb" style="left:122px;top:46px;width:116px;height:20px"></i>'
          '<i class="rr" style="left:122px;top:82px;width:96px;height:14px"></i>'
          '<i class="rr" style="left:122px;top:108px;width:64px;height:14px"></i>'
          '<div class="shc"><div class="sheen"></div></div></div>' % stroke("play"))
    L.append('<div class="g full" id="gH">'
             '<div class="shelf edge hide" id="hSh" style="left:70px;top:150px;width:940px;height:380px"></div>'
             + sw
             + '<div class="abs hide" id="hStr" style="left:0;top:0;width:1080px;height:600px">'
               '<div class="grp" id="hg0">%s</div>%s<div class="grp" id="hg1">%s</div>%s<div class="grp" id="hg2">%s</div></div>'
               % (g0, gap, g1, junk, g2)
             + tile("hSc", 80, 520, 184, "pearl", stroke("scissors"), extra_cls="circ", ring=False)
             + tile("hMe", 80, 424, 184, "pearl", stroke("person"), extra_cls="circ")
             + vc
             + tile("hOk", 54, 664, 252, "jelly", stroke("check"), extra_cls="circ", ring=False)
             + tile("hCl", 150, 820, 265, "jelly", g.mark("claude"))
             + '</div>')
    sfx("pop", T["vydil"], -3)
    sfx("click-soft", T["desiat"] + 0.02, -2)
    sfx("click", T["pauzy2"] + 0.05, -2)
    sfx("whoosh-short", T["viddav"], -2)
    return js("""
  tl.set("#gH", {autoAlpha: 1}, @tomu4-0.2);
  tl.set("#hCl", {autoAlpha: 1}, @tomu4-0.2);
  G.ripple("#hClR", @tomu4+0.15);
  arr("#hSh", @tomu4-0.05, {s: 0.9, y: 20});
  arr("#hSw", @vydil-0.08, {s: 0.4, y: 30});
  draw2("hArc", @desiat-0.05, 0.7);
  tl.fromTo("#hSw .num", {scale: 0.5, autoAlpha: 0}, {scale: 1, autoAlpha: 1, duration: 0.5, ease: POP}, @desiat-0.05);
  bin("#hStr", @vyriz4-0.35, 10, 0.3);
  arr("#hSc", @vyriz4-0.05, {s: 0.3, y: 10, d: 0.55});
  tl.to("#hSc", {x: -88 + 0, y: 70, duration: 0.3, ease: "power2.inOut"}, @pauzy2-0.25);
  tl.to("#hGap", {scaleX: 0, autoAlpha: 0, duration: 0.28, ease: "power2.in"}, @pauzy2+0.02);
  tl.to("#hSc", {x: 60, y: 70, duration: 0.35, ease: "power2.inOut"}, @zaive-0.3);
  tl.to("#hJunk", {y: 140, rotation: 14, autoAlpha: 0, duration: 0.45, ease: "power2.in"}, @zaive+0.02);
  tl.to("#hg0", {x: 60, duration: 0.5, ease: SP}, @samost-0.1);
  tl.to("#hg1", {x: 12, duration: 0.5, ease: SP}, @samost-0.1);
  tl.to("#hg2", {x: -60, duration: 0.5, ease: SP}, @samost-0.1);
  tl.to("#hSc", {x: 0, y: 0, duration: 0.4, ease: SP}, @samost-0.1);
  arr("#hMe", @samost-0.02, {s: 0.3, y: 10, d: 0.6}); G.ripple("#hMeR", @samost+0.25);
  bout(["#hStr", "#hSc", "#hMe"], @hotove-0.15, 10, 0.24);
  arr("#hVid", @hotove-0.05, {s: 0.5, y: 0}); shn("#hVid .sheen", @hotove+0.25);
  arr("#hOk", @hotove+0.3, {s: 0.2, y: 0, d: 0.5});
  tl.to(["#hVid", "#hOk"], {x: 330, scale: 0.3, autoAlpha: 0, duration: 0.45, ease: "power2.in"}, @viddav+0.05);
  G.bump("#hCl", @viddav+0.5); G.ripple("#hClR", @viddav+0.5);
  bout(["#hSh", "#hSw"], @montazh2, 10, 0.3);
  shn("#hCl .sheen", @montazh2);""")


# ===========================================================================
# TK3 · the iris opens out of Claude: the rule, both modes on one sheet
@beat
def t3_rule():
    def tl_(tid, x, y, mat, inner, circ=False):
        return ('<div class="tw hide%s" id="%s" style="left:%dpx;top:%dpx;width:210px;height:210px">'
                '<div class="%s">%s</div></div>' % (" circ" if circ else "", tid, x, y, mat, inner))

    def arrow(aid, x, y):
        return ('<svg class="arw hide" id="%s" viewBox="0 0 24 24" style="left:%dpx;top:%dpx;width:90px;height:90px">%s</svg>'
                % (aid, x, y, STROKES["arrow"]))
    sh = (
        '<div class="sheet hide" id="t3S" style="left:-60px;top:130px;width:1200px;height:1090px" data-layout-allow-overflow>'
        '<span class="t-micro abs" id="t3M" style="left:140px;top:60px;color:rgba(23,20,28,0.62)">ПРАВИЛО</span>'
        '<div class="rpill" id="r1" style="left:140px;top:110px">Експертні рілси</div>'
        + tl_("r1a", 140, 290, "jelly", stroke("prompter"))
        + arrow("r1x", 355, 350)
        + tl_("r1b", 450, 290, "pearl", stroke("pause"))
        + arrow("r1y", 665, 350)
        + tl_("r1c", 760, 290, "jelly", g.mark("claude"))
        + '<div class="tw hide circ" id="r1k" style="left:916px;top:258px;width:96px;height:96px"><div class="pearl">%s</div></div>'
          % stroke("check")
        + '<div class="hair abs" style="left:140px;top:566px;width:920px"></div>'
        '<div class="rpill pale" id="r2" style="left:140px;top:616px">Потокові рілси</div>'
        + tl_("r2a", 140, 796, "pearl", stroke("wave"))
        + arrow("r2x", 355, 856)
        + tl_("r2b", 450, 796, "jelly", stroke("scissors"))
        + tl_("r2c", 680, 796, "pearl", stroke("person"), circ=True)
        + '<div class="shc"><div class="sheen"></div></div></div>')
    L.append('<div class="g full" id="gT3"><div class="tkg"></div><div class="aurs"></div><div class="grain"></div>'
             + sh + '</div>')
    sfx("whoosh-short", T["tozh"] - 0.15)
    sfx("pop", T["dlia"] - 0.02, -3)
    sfx("click", T["vin"], -2)
    sfx("sparkle", T["idealno"], -4)
    sfx("pop", T["dlia2"] - 0.02, -3)
    sfx("click", T["vyrizai"] + 0.02, -2)
    return js("""
  G.irisOpen("#gT3", @tozh-0.16, 895, 340, 0.6);
  drift1("#gT3", @tozh-0.16, 7.8);
  tl.set("#gH", {autoAlpha: 0}, @tozh+0.4);
  arr("#t3S", @tozh-0.05, {s: 0.82, y: 60, d: 0.85});
  tl.fromTo("#t3M", {autoAlpha: 0, y: 14}, {autoAlpha: 1, y: 0, duration: 0.35, ease: SP}, @pravylo);
  tl.fromTo("#r1", {autoAlpha: 0, scale: 0.6, transformOrigin: "0% 50%"}, {autoAlpha: 1, scale: 1, duration: 0.55, ease: POP}, @dlia-0.04);
  arr("#r1a", @chytai-0.05, {s: 0.4, y: 20, d: 0.7});
  tl.fromTo("#r1x", {autoAlpha: 0, x: -20}, {autoAlpha: 1, x: 0, duration: 0.35, ease: SP}, @pauzamy2-0.2);
  arr("#r1b", @pauzamy2-0.05, {s: 0.4, y: 20, d: 0.7});
  tl.fromTo("#r1y", {autoAlpha: 0, x: -20}, {autoAlpha: 1, x: 0, duration: 0.35, ease: SP}, @vin-0.25);
  arr("#r1c", @vin-0.05, {s: 0.4, y: 20, d: 0.7});
  arr("#r1k", @idealno-0.04, {s: 0.2, y: 0, d: 0.5});
  shn("#t3S .sheen", @idealno);
  tl.fromTo("#r2", {autoAlpha: 0, scale: 0.6, transformOrigin: "0% 50%"}, {autoAlpha: 1, scale: 1, duration: 0.55, ease: POP}, @dlia2-0.04);
  arr("#r2a", @potokovykh+0.05, {s: 0.4, y: 20, d: 0.7});
  tl.fromTo("#r2x", {autoAlpha: 0, x: -20}, {autoAlpha: 1, x: 0, duration: 0.35, ease: SP}, @vyrizai-0.25);
  arr("#r2b", @vyrizai-0.05, {s: 0.4, y: 20, d: 0.7});
  arr("#r2c", @sama-0.05, {s: 0.4, y: 20, d: 0.7});
  G.irisClose("#gT3", @yakshcho2-0.25, 540, 375, 0.45);""")


# ===========================================================================
# CTA · Стежити
@beat
def z_follow():
    L.append('<div class="g full" id="gZ"><div class="fl hide" id="fl" style="left:190px;top:300px;width:700px;height:150px">'
             '<div class="tw circ" style="left:28px;top:27px;width:96px;height:96px"><div class="jelly">%s</div></div>'
             '<div class="t" id="flT">Стежити</div>'
             '<div class="on" id="flOn"><div class="tw circ" style="left:28px;top:27px;width:96px;height:96px">'
             '<div class="pearl">%s</div></div><div class="t">Ви стежите</div></div>'
             '<div class="ck" id="ck4" style="left:470px;top:75px"></div>'
             '<div class="shc"><div class="sheen"></div></div></div></div>'
             % (g.mark("instagram"), stroke("check")))
    press = T["pidpysh"] + 0.2      # the token starts on «то»
    sfx("pop", T["yakshcho2"] + 0.02, -3)
    sfx("click", press + 0.02)
    return js("""
  tl.set("#gZ", {autoAlpha: 1}, @yakshcho2-0.25);
  arr("#fl", @yakshcho2-0.2, {s: 0.6, y: 40});
  tl.to("#fl", {scale: 0.95, duration: 0.09, ease: "power2.out"}, @press);
  tl.to("#fl", {scale: 1, duration: 0.45, ease: SP}, @press+0.09);
  tl.fromTo("#flOn", {autoAlpha: 0}, {autoAlpha: 1, duration: 0.2}, @press+0.04);
  tl.set("#flT", {autoAlpha: 0}, @press+0.05);
  tl.fromTo("#ck4", {scale: 0.3, autoAlpha: 0.95}, {scale: 2.4, autoAlpha: 0, duration: 0.7, ease: "power2.out", immediateRender: false}, @press+0.02);
  shn("#fl .sheen", @press+0.15);""", press=press)


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

RULE = u"З кількох повторів треба брати останню фразу"


def typing_js():
    """The rule types itself, driven from one clock so any frame renders cold."""
    t0, t1 = T["shchoz"] + 0.05, T["frazue"] - 0.05
    return r"""
  var CLK = {t: 0}, PB = document.getElementById("t1T"), PTXT = %s, PCUR = null;
  function paintAll() {
    var t = CLK.t, n = t <= %.3f ? 0 : t >= %.3f ? PTXT.length : Math.round(PTXT.length * (t - %.3f) / %.3f);
    if (n !== PCUR) { PCUR = n; PB.textContent = PTXT.slice(0, n); }
  }
  tl.fromTo(CLK, {t: 0}, {t: %.3f, duration: %.3f, ease: "none", onUpdate: paintAll}, 0);""" % (
        json.dumps(RULE, ensure_ascii=False), t0, t1, t0, t1 - t0, DUR, DUR)


# captions that would repeat the graphic's own words (STYLE.md §2b.1)
def span_words(a, b):
    return (round(a - 0.02, 3), round(b, 3), "")


BLACKOUT = [
    span_words(T["trysta"], T["trystae"]),                  # ×300
    span_words(T["nalasht"], T["nalashte"]),                # НАЛАШТУВАННЯ
    span_words(T["shchoz"], T["frazue"]),                   # the rule types itself
    span_words(T["ekspert"], T["eksperte"]),                # the switch: Експертні
    span_words(T["ya"], T["strashnoe"]),                    # the teleprompter's lines are her words
    span_words(T["potokove"], T["potokovee"]),              # the switch: Потокові
    span_words(T["desiat"], T["khvylyne"]),                 # 10 хв
    span_words(T["pravylo"], T["pravyloe"]),                # ПРАВИЛО
    span_words(T["ekspert2"], T["rilsiv2e"]),               # «Експертні рілси»
    span_words(T["potokovykh"], T["potokovykhe"]),          # «Потокові рілси»
]


def check_no_paint():
    """Nothing on screen across her wink («трошки брехня»)."""
    a, b = NO_PAINT[-1]
    assert T["ale"] - 0.14 + 0.24 <= a + 0.05, "beat A runs into the wink"
    assert T["yakshcho"] - 0.2 >= b, "beat B arrives inside the wink"
    for c in SFX:
        assert not (a <= c["t"] < b), ("sfx on the wink", c)


def main():
    gj = []
    for fn in BEATS:
        j = fn()
        gj.append("  /* %s */" % fn.__name__)
        gj.append(j.rstrip())
    check_no_paint()
    push = ["#vid"]
    head = [g.js(), HEAD_JS, typing_js(),
            '  gsap.set(%s, {transformOrigin: "540px 900px"});' % json.dumps(push),
            '  tl.fromTo(%s, {scale: 1}, {scale: 1.045, duration: %.3f, ease: "none"}, 0);' % (json.dumps(push), DUR)]
    doc = k.document(
        title=u"Reel 39 — одне правило запису",
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
