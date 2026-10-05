# -*- coding: utf-8 -*-
"""Reel 22 — «Якщо ти хочеш продати свій перший гайд…». Posts 2026-10-06.

An explainer, so the full refined-glass chain (STYLE.md §0): near -> over ->
near, five takeovers, one stopwatch that opens the reel at 15:00 and closes it
at 1:00. Her two closeups (cut.py punches on «мільйони доларів» and «супер
пупер») stay clear.

Chain:  near: a guide card lands, a ₴ coin on it flips into a magnet, leads
slide in; ghost slots for days / hours light -> [closeup] -> near: a shelf of
design / layout / settings tiles, the gear turns on «і так далі», all collapse
to one point -> over: the iris opens out of it onto a stopwatch, 15:00 slams in,
the crown is pressed -> the iris closes into the step bar's timer: КРОК 1, the
timer ticks 15:00 -> 14:00, Notion is created (ghost -> lit, + -> ✓); КРОК 2,
13:00, Claude and ChatGPT land and Notion is wired to both; КРОК 3 ★: a voice
panel, the mic, a live waveform into Claude, the waveform becomes a draft that
becomes a guide -> [closeup] -> over: the draft on a sheet, the SKILL.md tile
lands, a scan rewrites every line, her signature -> the iris closes into a DM:
«КОПІ» typed and sent, a YouTube link comes back -> near: voice notes drop
into Claude, the prompt types itself, send -> over: the iris opens out of
Notion and the guide page builds, the link pops, БЕЗКОШТОВНО, ✓ -> the iris
closes on the link: it drops into a chatbot, the guide flies to a person ->
near: the guide gets a ₴ tag, +1 КРОК, WayForPay -> over: the invoice form,
Соцінвойс, Продукти, the Notion link pastes in, Зберегти, the pay link rises ->
the iris closes on it: stories, profile bio, Telegram -> near: a person pays
(kaching), Gmail delivers -> near: technical work is a short bar, the content a
long one, 15 хв slides to days, pages pile up -> over: Notion · WayForPay ·
Gmail inside the same stopwatch, one lap, 1:00 -> near: Стежити.

usage: python build.py   (then: python ../tools/sfx.py mix 22)
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

CUT = json.load(io.open(os.path.join(ROOT, "work", "r22", "cut.json"), encoding="utf-8"))
# The beats were authored against cut-authored.json (86.03 s). When the cut is
# re-trimmed, every hand-written time below is carried to the new timeline
# through source time, so the "near" hints and caption fixes still land.
CUT0 = json.load(io.open(os.path.join(HERE, "cut-authored.json"), encoding="utf-8"))


def remap(t):
    for c in CUT0["clips"]:
        if c["tl"] - 1e-6 <= t < c["tl"] + c["dur"] + 1e-6:
            src = c["src_in"] + (t - c["tl"])
            break
    else:
        return t
    best = None
    for c in CUT["clips"]:
        if c["src_in"] - 1e-6 <= src <= c["src_in"] + c["dur"] + 1e-6:
            return c["tl"] + (src - c["src_in"])
        for edge_src, edge_tl in ((c["src_in"], c["tl"]), (c["src_in"] + c["dur"], c["tl"] + c["dur"])):
            d = abs(edge_src - src)
            if best is None or d < best[0]:
                best = (d, edge_tl)
    return best[1]


def plate_dur():
    """(plate frames - 0.5) / 30, floored to 3 decimals — read off the plate itself."""
    import math
    import subprocess
    n = int(subprocess.check_output(
        ["ffprobe", "-v", "error", "-count_packets", "-select_streams", "v", "-show_entries",
         "stream=nb_read_packets", "-of", "csv=p=0", os.path.join(HERE, "assets", "voice.mp4")]).decode().strip())
    return math.floor((n - 0.5) / 30.0 * 1000) / 1000.0, n


DUR, PLATE_FRAMES = plate_dur()
FPS = 30
k = Kit(width=1080, height=1920, fps=FPS, duration=DUR)
g = Glass(["notion", "claude", "openai", "telegram", "instagram", "youtube", "gmail"])
k.css(g.css())

# ---------------------------------------------------------------------------
# NO-PAINT: the closeups cut.py punched in. Captions only.
NO_PAINT = [tuple(x) for x in CUT["no_paint"]]


def np_near(t):
    for a, b in NO_PAINT:
        if a - 1.0 <= t <= b + 1.0:
            return (a, b)
    return None


NP1 = np_near(5.4)      # «мільйони доларів»
NP2 = np_near(31.0)     # «супер пупер»
assert NP1 and NP2, NO_PAINT

CAPS = k.load_captions(os.path.join(ROOT, "work", "r22", "captions.json"))
# Whisper errors that align kept as "her wording" (align.txt): restore what she
# actually said. Keyed by caption start; None drops the word.
FIXAT = {8.801: u"зараз",          # «я зараз» + «я» -> «зараз я покажу» (she said it in that order)
         18.89: u"або",            # she said «Клод або ChatGPT», not «чи»
         31.467: u"якщо",          # «І жовтиме» is whisper for «якщо в тебе»
         31.697: u"в тебе",
         40.577: u"просиш",        # «про це» = «просиш»
         40.837: None,
         41.457: u"інтелект",      # «телек»
         58.832: u"свою"}          # «своїй сторінку»
FIXAT = {remap(t): v for t, v in FIXAT.items()}
_caps = []
for c in CAPS:
    hit = [v for t, v in FIXAT.items() if abs(c["s"] - t) < 0.05]
    if hit:
        if hit[0] is None:
            continue
        c["w"] = hit[0]
    _caps.append(c)
assert len(CAPS) - len(_caps) == 1
CAPS = _caps
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


WORDS = [
    ("yakshcho0", u"Якщо", 0.0), ("prodaty", u"продати", 0.97), ("haid0", u"гайд", 1.85),
    ("lidmagnit", u"лід-магніт", 3.07), ("vytrachaty", u"витрачати", 3.79), ("dni", u"дні", 4.29),
    ("hodyny", u"години", 4.65), ("dyzain", u"дизайн", 5.91), ("oform", u"оформлення", 6.56),
    ("nalasht", u"налаштування", 7.12), ("tak", u"так", 7.80), ("pokazhu", u"покажу", 9.28),
    ("bukv", u"буквально", 10.51), ("p15", u"15", 11.31), ("khvylyn", u"хвилин", 11.77),
    ("pershyi", u"Перший", 12.94), ("khvylynu", u"хвилину", 13.74), ("stvor", u"створюєш", 14.24),
    ("notion1", u"Notion", 14.99), ("nema", u"нема", 16.02), ("druhyi", u"Другий", 16.65),
    ("khvylyna", u"хвилина", 17.47), ("vidkr", u"відкриваєш", 18.01), ("klod", u"Клод", 18.59),
    ("chatgpt", u"ChatGPT", 19.04), ("pidkl", u"підключаєш", 19.72), ("notion2", u"Notion", 21.16),
    ("dali", u"Далі", 21.73), ("naivazh", u"найважливіша", 22.62), ("ty", u"ти", 23.97),
    ("nahovor", u"наговорюєш", 24.47), ("intelektu", u"інтелекту", 26.43),
    ("rozkaz", u"розказати", 28.06), ("lidmag2", u"лідмагніті", 28.80),
    ("yakshcho1", u"якщо", 31.467), ("skil", u"скіл", 32.38), ("perepys", u"переписує", 32.92),
    ("tvoiemu", u"твоєму", 34.18), ("styli", u"стилі", 34.80), ("napyshy", u"напиши", 35.40),
    ("kopi", u"КОПІ", 36.28), ("i_ya", u"і", 36.82), ("posyl1", u"посилання", 37.60),
    ("youtube", u"YouTube", 38.84), ("koly", u"Коли", 39.37), ("nahovoreno", u"наговорено", 40.06),
    ("prosysh", u"просиш", 40.58), ("shtuchnyi", u"штучний", 41.0), ("zrobyty", u"зробити", 41.68),
    ("notion3", u"Notion", 44.0), ("posyl2", u"посилання", 45.12), ("bezkosht", u"безкоштовний", 46.32),
    ("hotova", u"готова", 47.66), ("beresh", u"береш", 48.02), ("posyl3", u"посилання", 48.46),
    ("vstavl", u"вставляєш", 48.90), ("chatbota", u"чат-бота", 49.32), ("liudyna", u"людина", 49.99),
    ("otrymuie", u"отримує", 50.27), ("haid3", u"гайд", 50.63), ("yakshcho2", u"Якщо", 50.97),
    ("oplatu", u"оплату", 51.94), ("ye", u"є", 52.78), ("krok3", u"крок", 53.46),
    ("vidkr2", u"Відкриваєш", 53.96), ("wfp", u"Way4Pay", 54.68), ("stvor2", u"створюєш", 55.51),
    ("socinv", u"соцінвойс", 55.93), ("produkty", u"продукти", 57.17), ("posyl4", u"посилання", 58.23),
    ("notion4", u"Notion", 59.53), ("zberih", u"Зберігаєш", 59.83), ("zabyr", u"забираєш", 60.64),
    ("oplatu2", u"оплату", 61.54), ("storis", u"сторіс", 62.50), ("shapku", u"шапку", 63.0),
    ("profiliu", u"профілю", 63.40), ("telegram", u"телеграм", 63.80), ("kudy", u"куди", 64.36),
    ("liudyna2", u"Людина", 65.33), ("platyt", u"платить", 65.63), ("otrymuie2", u"отримує", 66.85),
    ("haid4", u"гайд", 67.33), ("poshtu", u"пошту", 68.01), ("naidovsha", u"Найдовша", 68.63),
    ("tekhn", u"технічна", 70.83), ("robota", u"робота", 71.31), ("liudiam", u"людям", 73.29),
    ("haidi", u"гайді", 73.89), ("p15b", u"15", 75.19), ("kilka", u"кілька", 76.12),
    ("dniv", u"днів", 76.40), ("inform", u"інформації", 78.46), ("a_", u"А", 79.07),
    ("dyzain2", u"дизайн", 80.22), ("oplata", u"оплата", 80.76), ("dostavka", u"доставка", 81.24),
    ("zabyraie", u"забирає", 81.86), ("khvylynu2", u"хвилину", 83.08), ("yakshcho3", u"Якщо", 83.82),
    ("pidpysh", u"підпишись", 85.28),
]
T = {key: S(w, remap(t)) for key, w, t in WORDS}
T["dur"] = DUR
# derived beat edges
T["aend"] = NP1[0] - 0.34                      # hook clears before the first closeup
T["b0"] = NP1[1] + 0.03                        # the shelf comes in after it
T["c0"] = T["pokazhu"] + 0.30                  # iris onto the stopwatch
T["sb0"] = T["pershyi"] - 0.08                 # step bar lands as the iris closes into it
T["fend"] = NP2[0] - 0.34                      # step 3 clears before the second closeup
T["g0"] = NP2[1] + 0.03                        # the skill takeover opens after it
T["j0"] = T["notion3"] + 0.30                  # iris out of Notion: the guide page
T["l0"] = T["wfp"] + 0.62                      # iris out of WayForPay: the invoice
T["m0"] = T["zabyr"] + 0.36                    # iris closes onto the pay link
T["p0"] = T["a_"] - 0.04                       # iris out of the guide tile: the last lap


def js(src, **extra):
    """`@name`, `@name+0.12`, `@name-0.1` -> one literal time."""
    vals = dict(T)
    vals.update(extra)

    def rep(m):
        v = vals[m.group(1)] + (float(m.group(2)) if m.group(2) else 0.0)
        return "%.3f" % v
    return re.sub(r"@(\w+)([+-]\d+(?:\.\d+)?)?", rep, src)


# ---------------------------------------------------------------------------
# Sound design (tools/sfx.py). Quiet, on the event, never on her closeups.
SFX = []


def sfx(name, t, db=0):
    if isinstance(t, str):
        t = float(js(t))
    SFX.append({"t": round(max(0.0, t), 3), "name": name, "db": db})


# ---------------------------------------------------------------------------
# Glyphs (24-unit strokes in the tile family)
STROKES = {
    "up": '<path d="M12 19.2V5.4M6.2 11l5.8-5.8 5.8 5.8"/>',
    "check": '<path d="M5.4 12.6l4.3 4.3 8.9-9.5"/>',
    "plus": '<path d="M12 5.2v13.6M5.2 12h13.6"/>',
    "person": '<circle cx="12" cy="8.2" r="3.6"/><path d="M4.8 20c.9-3.8 3.7-5.8 7.2-5.8s6.3 2 7.2 5.8"/>',
    "calendar": '<rect x="3.6" y="5.2" width="16.8" height="15.2" rx="3"/><path d="M3.6 10.2h16.8M8 3.2v4M16 3.2v4"/>',
    "clock": '<circle cx="12" cy="12" r="8.6"/><path d="M12 7.4V12l3.2 2.1"/>',
    "palette": ('<path d="M12 3.5a8.5 8.5 0 1 0 0 17c1.2 0 1.8-.8 1.8-1.7 0-1.2-1-1.6-1-2.6 0-.9.8-1.6 1.8-1.6h2.1'
                'a3.8 3.8 0 0 0 3.8-3.8c0-4.2-3.8-7.3-8.5-7.3z"/><circle cx="7.6" cy="11.2" r="1.15"/>'
                '<circle cx="10.4" cy="7.4" r="1.15"/><circle cx="15" cy="7.8" r="1.15"/>'),
    "layout": '<rect x="3.6" y="3.6" width="16.8" height="16.8" rx="3"/><path d="M3.6 9.2h16.8M9.6 9.2v11.2"/>',
    "gear": ('<circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0'
             'l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4'
             'a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0'
             '-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83'
             ' 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09'
             'a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0'
             '-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/>'),
    "doc": '<path d="M7 2.8h7.2l4.2 4.2v13.4a.8.8 0 0 1-.8.8H7a.8.8 0 0 1-.8-.8V3.6a.8.8 0 0 1 .8-.8z"/><path d="M14 2.8V7h4.2M9.2 11.6h5.6M9.2 15h5.6M9.2 18.2h3.4"/>',
    "mic": '<rect x="9" y="3" width="6" height="11.2" rx="3"/><path d="M5.6 11.2a6.4 6.4 0 0 0 12.8 0M12 17.6V21"/>',
    "link": '<path d="M10.2 13.8a4.2 4.2 0 0 0 6 0l3-3a4.2 4.2 0 0 0-6-6l-1.1 1.1"/><path d="M13.8 10.2a4.2 4.2 0 0 0-6 0l-3 3a4.2 4.2 0 0 0 6 6l1.1-1.1"/>',
    "bot": ('<rect x="4.4" y="8" width="15.2" height="11.4" rx="3.6"/><path d="M12 8V4.6M2.6 12.6v2.8M21.4 12.6v2.8"/>'
            '<circle cx="12" cy="3.9" r="1"/><circle cx="9.2" cy="13.4" r="1.25"/><circle cx="14.8" cy="13.4" r="1.25"/>'),
}
STAR = ('<svg viewBox="0 0 24 24" width="34" height="34"><path d="M12 2.8l2.75 5.6 6.15.9-4.45 4.35 1.05 6.1L12 16.9l-5.5 2.85'
        ' 1.05-6.1L3.1 9.3l6.15-.9z" fill="#fff"/></svg>')
# a horseshoe magnet: red body, steel tips, tilted so it never reads as the letter U
MAGNET = ('<svg class="mag" viewBox="0 0 24 24"><g transform="rotate(38 12 12)">'
          '<path d="M7 5.6v6.2a5 5 0 0 0 10 0V5.6" fill="none" stroke="#c41434" stroke-width="4.4"/>'
          '<path d="M7 2.4v3.6M17 2.4v3.6" fill="none" stroke="#8f8e99" stroke-width="4.4"/>'
          '<path d="M5.6 2.4v3.6M15.6 2.4v3.6" fill="none" stroke="#c9c8d2" stroke-width="1.2"/>'
          '<path d="M3.2 -0.6h-1.6M20.8 -0.6h1.6M12 -2.4v-1.6" fill="none" stroke="#ff6e9c" stroke-width="1.3" '
          'stroke-linecap="round"/></g></svg>')
# «₴» is not in Product Sans, so it is drawn: a mirrored S (the handwritten г) with two bars
UAH_D = ("M7 7.4C7.6 5.4 9.6 4.2 12 4.2c2.8 0 4.8 1.6 4.8 3.8 0 4.2-9.6 4.4-9.6 8.2 0 2.2 2 3.6 4.8 3.6 "
         "2.6 0 4.4-1.2 5.2-3M5.4 10.4h13.2M5.4 13.8h13.2")


def uah(size, color="#fff", sw=2.4, style=""):
    return ('<svg viewBox="0 0 24 24" width="%d" height="%d" style="position:relative;z-index:1;%s">'
            '<path d="%s" fill="none" stroke="%s" stroke-width="%.2f" stroke-linecap="round" '
            'stroke-linejoin="round"/></svg>' % (size, size, style, UAH_D, color, sw))


TAG = ('<svg viewBox="0 0 210 130" width="210" height="130" style="overflow:visible">'
       '<defs><linearGradient id="tg" x1="0" y1="0" x2="0.3" y2="1"><stop offset="0" stop-color="#e0204b"/>'
       '<stop offset="0.5" stop-color="#ab112e"/><stop offset="1" stop-color="#6b081c"/></linearGradient></defs>'
       '<path d="M46 10 H188 a16 16 0 0 1 16 16 V104 a16 16 0 0 1 -16 16 H46 L8 65 Z" fill="url(#tg)" '
       'style="filter:drop-shadow(0 18px 24px rgba(40,2,12,.45))"/>'
       '<circle cx="40" cy="65" r="10" fill="#fff" fill-opacity=".92"/>'
       '<g transform="translate(92 29) scale(3)"><path d="%s" fill="none" stroke="#fff" stroke-width="2.5" '
       'stroke-linecap="round" stroke-linejoin="round"/></g></svg>' % UAH_D)
SIG = ("M14 118 C 40 40, 74 28, 70 92 C 66 140, 104 120, 126 74 C 140 46, 160 48, 152 96 C 146 128, 178 116, 198 84 "
       "C 214 58, 232 64, 228 100 C 226 120, 252 112, 276 88 C 300 64, 330 70, 352 84 C 372 96, 392 92, 406 80")


def stroke(name, cls="sk", style=""):
    return '<svg class="%s" viewBox="0 0 24 24"%s>%s</svg>' % (cls, (' style="%s"' % style) if style else "", STROKES[name])


def tile(tid, size, x, y, material, inner, extra_cls="", hide=True, ring=True):
    r = ('<div class="sqring" id="%sR" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx"></div>'
         % (tid, x, y, size, size)) if ring else ""
    return ('%s<div class="tw%s %s" id="%s" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx">'
            '<div class="%s">%s<div class="sheen"></div></div></div>'
            % (r, " hide" if hide else "", extra_cls, tid, x, y, size, size, material, inner))


def wide(tid, x, y, w, h, inner, r=46, material="pearl", ring=True):
    rr = ('<div class="sqring" id="%sR" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx;border-radius:%dpx"></div>'
          % (tid, x, y, w, h, r)) if ring else ""
    return ('%s<div class="tw hide" id="%s" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx">'
            '<div class="%s" style="border-radius:%dpx">%s<div class="sheen"></div></div></div>'
            % (rr, tid, x, y, w, h, material, r, inner))


def wfp(size):
    return '<span class="wmark" style="font-size:%dpx;letter-spacing:-0.035em">Way<i>For</i>Pay</span>' % size


def gdoc(did, x, y, s=1.0, hide=True):
    """The guide: a small Notion-style page (cover, icon, title, text, checklist)."""
    w, h = int(round(300 * s)), int(round(390 * s))
    inner = ('<div class="gd" style="transform:scale(%.4f)">'
             '<i class="cov"></i>'
             '<div class="tw" style="left:24px;top:74px;width:74px;height:74px"><div class="jelly">%s</div></div>'
             '<i class="hb" style="left:24px;top:168px;width:196px;height:26px;border-radius:9px"></i>'
             '<i class="rr" style="left:24px;top:212px;width:240px;height:13px;border-radius:7px"></i>'
             '<i class="rr" style="left:24px;top:234px;width:206px;height:13px;border-radius:7px"></i>'
             '<i class="rr" style="left:24px;top:256px;width:150px;height:13px;border-radius:7px"></i>'
             '<i class="cb" style="left:24px;top:292px"></i>'
             '<i class="rr" style="left:62px;top:299px;width:170px;height:12px;border-radius:6px"></i>'
             '<i class="cb" style="left:24px;top:332px"></i>'
             '<i class="rr" style="left:62px;top:339px;width:128px;height:12px;border-radius:6px"></i>'
             '<div class="shc"><div class="sheen"></div></div></div>' % (s, stroke("doc")))
    return ('<div class="tw%s" id="%s" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx">%s</div>'
            % (" hide" if hide else "", did, x, y, w, h, inner))


def ground():
    return '<div class="tkg"></div><div class="aurs"></div><div class="grain"></div>'


def cable(prefix, d, packet=True):
    out = ('<path class="tube hide" id="%sT" d="%s"/><path class="core hide" id="%sK" d="%s"/>' % (prefix, d, prefix, d))
    if packet:
        out += '<g class="pkg"><path class="pkt" id="%sP" style="opacity:0" d="%s"/></g>' % (prefix, d)
    return out


def chip(cid, x, y, w, kind, inner, hide=True):
    return ('<div class="lchip %s%s" id="%s" style="left:%dpx;top:%dpx;width:%dpx">%s'
            '<div class="shc"><div class="sheen"></div></div></div>'
            % (kind, " hide" if hide else "", cid, x, y, w, inner))


def stopwatch(prefix):
    """The stopwatch ring both ends of the reel share: same centre, same size."""
    return ('<div class="stem" style="left:522px;top:84px;width:36px;height:32px"></div>'
            '<div class="crown" id="%sCr" style="left:470px;top:28px;width:140px;height:64px"></div>'
            '<svg class="abs" width="1080" height="1920" viewBox="0 0 1080 1920" style="left:0;top:0;overflow:visible">'
            '<circle class="rtrk" cx="540" cy="700" r="580"/>'
            '<circle class="rtick" cx="540" cy="700" r="520"/>'
            '<circle class="rarc" id="%sArc" cx="540" cy="700" r="580" transform="rotate(-90 540 700)" style="opacity:0"/>'
            '</svg>' % (prefix, prefix))


RING_C = 2 * 3.14159265 * 580


k.css("""
.abs { position: absolute; }
.hide { opacity: 0; visibility: hidden; }
.tw { position: absolute; }
.sk { fill: none; stroke: url(#gw); stroke-width: 2.3; stroke-linecap: round; stroke-linejoin: round;
  width: 50%; height: 50%; position: relative; z-index: 1; overflow: visible; }
.pearl .sk, .sk.ink { stroke: #17141c; }
.sk.red { stroke: #b4122f; }
.inkmk { fill: #17141c; }
.clear { overflow: hidden; }
.circ .jelly, .circ .pearl, .circ .clear, .circ .sheen { border-radius: 50%; }
.ghost .mk, .ghost .sk { opacity: 0.34; }
.mag { width: 64%; height: 64%; position: relative; z-index: 1; overflow: visible; }
.aurs { position: absolute; left: -700px; top: -700px; width: 2480px; height: 3320px; pointer-events: none;
  background:
    radial-gradient(circle 526px at 1560px 880px, rgba(255,110,156,0.50), rgba(255,110,156,0)),
    radial-gradient(circle 634px at 760px 2360px, rgba(222,32,74,0.55), rgba(222,32,74,0)),
    radial-gradient(circle 382px at 1480px 1910px, rgba(255,198,214,0.20), rgba(255,198,214,0)); }
.shc { position: absolute; inset: 0; border-radius: inherit; overflow: hidden; pointer-events: none; }
.shc .sheen { mix-blend-mode: normal; opacity: 0.4; }
.ck { position: absolute; width: 120px; height: 120px; margin: -60px 0 0 -60px; border-radius: 50%;
  border: 7px solid #ff6e9c; opacity: 0; visibility: hidden; z-index: 5; }
.hb { position: absolute; display: block; border-radius: 12px; background: linear-gradient(115deg, #c41434 0%, #8d0d24 100%); }
.rr { position: absolute; display: block; border-radius: 9px; background: rgba(23,20,28,0.13); }
.cbx { position: absolute; width: 50px; height: 50px; border-radius: 15px; box-shadow: inset 0 0 0 4px rgba(23,20,28,0.22); }

/* a card flip: two faces, backs hidden */
.fx { position: absolute; perspective: 1100px; }
.fxi { position: absolute; inset: 0; transform-style: preserve-3d; }
.ff { position: absolute; inset: 0; backface-visibility: hidden; -webkit-backface-visibility: hidden; }
.ff.bk { transform: rotateY(180deg); }

/* the guide (small Notion-style page) */
.gd { position: absolute; left: 0; top: 0; width: 300px; height: 390px; transform-origin: 0 0; border-radius: 34px;
  overflow: hidden; background: linear-gradient(172deg, #ffffff 0%, #fff9fb 60%, #fdf0f4 100%);
  box-shadow: inset 0 2px 1px #fff, 0 44px 90px -34px rgba(24,4,12,0.62), 0 0 0 1px rgba(255,255,255,0.4); }
.gd i { position: absolute; display: block; }
.gd .cov { left: 0; top: 0; right: 0; height: 112px;
  background: linear-gradient(120deg, #ffd6e3 0%, #ff8ab0 46%, #b4122f 100%); }
.gd .cb { width: 26px; height: 26px; border-radius: 8px; box-shadow: inset 0 0 0 3px rgba(23,20,28,0.22); }

/* the stopwatch */
.rtrk { fill: none; stroke: rgba(255,255,255,0.10); stroke-width: 44; }
.rtick { fill: none; stroke: rgba(255,255,255,0.26); stroke-width: 24; stroke-dasharray: 5 49.454; }
.rarc { fill: none; stroke: url(#gpk); stroke-width: 44; stroke-linecap: round;
  filter: drop-shadow(0 0 18px rgba(255,110,156,0.7)); }
.crown { position: absolute; border-radius: 22px;
  background: linear-gradient(170deg, #ffffff 0%, #ffe3ec 55%, #f2bfcf 100%);
  box-shadow: inset 0 2px 1px #fff, inset 0 -10px 18px -8px rgba(180,18,47,0.3), 0 22px 40px -16px rgba(8,0,3,0.7); }
.stem { position: absolute; border-radius: 8px; background: linear-gradient(90deg, rgba(255,255,255,0.35), rgba(255,255,255,0.7), rgba(255,255,255,0.35)); }
.bigt { position: absolute; left: 0; width: 1080px; text-align: center; font-weight: 900; letter-spacing: -0.045em;
  background: linear-gradient(180deg, #ffffff 0%, #ffd0de 100%); -webkit-background-clip: text; background-clip: text;
  color: transparent; }

/* the step bar */
#sb .tmr { position: absolute; left: 26px; top: 22px; width: 80px; height: 80px; }
#sb .tmr circle { fill: none; stroke-width: 9; }
#sb .tmr .trk { stroke: rgba(255,255,255,0.18); }
#sb .tmr .arc { stroke: #ff8ab0; stroke-linecap: round; }
#sb .dw { position: absolute; left: 122px; top: 18px; width: 214px; height: 88px; overflow: hidden; }
#sb .dw b { display: block; height: 88px; line-height: 88px; font-size: 64px; font-weight: 900; color: #fff;
  letter-spacing: -0.02em; }
#sb .sep { position: absolute; left: 346px; top: 30px; width: 2px; height: 64px; background: rgba(255,255,255,0.18); }
#sb .cw { position: absolute; left: 366px; top: 20px; width: 312px; height: 84px; overflow: hidden; border-radius: 42px; }
#sb .cw b { display: flex; align-items: center; justify-content: center; gap: 12px; height: 84px; font-size: 36px;
  font-weight: 700; color: #fff; border-radius: 42px; background: rgba(255,255,255,0.13); letter-spacing: 0.01em; }
#sb .cw b.hot { background: linear-gradient(165deg, #e0204b 0%, #ab112e 46%, #6b081c 100%); font-weight: 900; }

/* step 3: the voice panel */
.wb { position: absolute; top: 60px; width: 12px; height: 180px; border-radius: 6px;
  background: linear-gradient(180deg, #ffffff 0%, #ffbfd2 100%); transform: scaleY(0.14); }
.mring { position: absolute; border-radius: 50%; border: 6px solid rgba(255,138,176,0.9); opacity: 0; visibility: hidden; }
.dr { position: absolute; border-radius: 30px; overflow: hidden;
  background: linear-gradient(172deg, #ffffff 0%, #fff9fb 60%, #fdf0f4 100%);
  box-shadow: inset 0 2px 1px #fff, 0 30px 60px -24px rgba(24,4,12,0.6); }
.dr i { position: absolute; display: block; }
.dr .cov { left: 0; top: 0; right: 0; height: 58px; transform: scaleY(0); transform-origin: 50% 0;
  background: linear-gradient(120deg, #ffd6e3 0%, #ff8ab0 46%, #b4122f 100%); }

/* the skill rewrite */
.ol { position: absolute; display: block; height: 28px; border-radius: 14px; background: rgba(23,20,28,0.13); }
.nl { position: absolute; left: 50px; width: 780px; height: 44px; opacity: 0; visibility: hidden; }
.nl i { position: absolute; display: block; }
.nl .hl { border-radius: 10px; background: rgba(255,110,156,0.38); }
.nl .bd { width: 22px; height: 22px; border-radius: 50%; background: linear-gradient(165deg, #e0204b, #8d0d24); }
.scan { position: absolute; left: -30px; right: -30px; height: 16px; border-radius: 8px; opacity: 0; visibility: hidden;
  background: linear-gradient(90deg, rgba(255,110,156,0), #ff6e9c 18%, #ffe0ea 50%, #ff6e9c 82%, rgba(255,110,156,0));
  box-shadow: 0 0 34px 10px rgba(255,110,156,0.40); }
.sig { fill: none; stroke: #b4122f; stroke-width: 7; stroke-linecap: round; stroke-linejoin: round; opacity: 0; }
.sklab { position: relative; z-index: 1; display: flex; flex-direction: column; align-items: center; gap: 8px; }
.sklab .sk { width: 92px; height: 92px; }
.sklab span { color: #fff; font-size: 36px; font-weight: 700; letter-spacing: -0.01em; }

/* the DM */
.dmb { position: absolute; display: flex; align-items: center; justify-content: center; }
.bar { position: absolute; display: block; border-radius: 9px; }
#hS { border-radius: 31px 31px 10px 31px; background: linear-gradient(165deg, #e0204b 0%, #ab112e 46%, #6b081c 100%);
  box-shadow: inset 0 2px 1px rgba(255,255,255,0.45), 0 20px 40px -16px rgba(70,4,20,0.7);
  color: #fff; font-size: 36px; font-weight: 900; letter-spacing: 0.02em; }
#hR { border-radius: 30px 30px 30px 10px; overflow: hidden;
  background: linear-gradient(172deg, #ffffff 0%, #fff7fa 100%); box-shadow: 0 24px 50px -20px rgba(10,0,4,0.6); }
.thumb { position: absolute; border-radius: 20px; display: flex; align-items: center; justify-content: center;
  background: linear-gradient(135deg, #3c0716 0%, #8d0d24 45%, #ff6e9c 100%); }
.thumb .mk { width: 78px; height: 78px; fill: #fff; }
#hI { border-radius: 31px; background: rgba(255,255,255,0.12); box-shadow: inset 0 0 0 1.5px rgba(255,255,255,0.18); }
.dtx { position: absolute; left: 26px; top: 0; height: 62px; line-height: 62px; font-size: 34px; font-weight: 700;
  color: #fff; letter-spacing: 0.02em; white-space: pre; }
.dtx::after, .ptx::after { content: ""; display: inline-block; width: 3px; height: 38px; margin-left: 3px;
  vertical-align: -7px; background: #ff8ab0; }
.yring { position: absolute; width: 110px; height: 110px; margin: -55px 0 0 -55px; border-radius: 50%;
  border: 6px solid #fff; opacity: 0; visibility: hidden; }

/* the prompt */
.ptx { position: absolute; left: 44px; top: 32px; width: 790px; font-size: 38px; font-weight: 500; line-height: 1.32;
  color: #fff; white-space: pre-wrap; }
.vpl { position: absolute; width: 190px; height: 60px; border-radius: 30px; display: flex; align-items: center;
  justify-content: center; gap: 9px;
  background: linear-gradient(165deg, #e0204b 0%, #8d0d24 100%);
  box-shadow: inset 0 2px 1px rgba(255,255,255,0.45), 0 18px 36px -14px rgba(70,4,20,0.7); }
.vpl i { display: block; width: 7px; border-radius: 4px; background: #fff; }

/* the Notion page */
.np { position: absolute; border-radius: 56px; overflow: hidden; color: #17141c;
  background: linear-gradient(172deg, #ffffff 0%, #fff9fb 55%, #fdf0f4 100%);
  box-shadow: inset 0 2px 1px #fff, 0 70px 130px -40px rgba(8,0,3,0.75), 0 0 0 1px rgba(255,255,255,0.35); }
.np i { position: absolute; display: block; }
.np .ncov { left: 0; top: 0; width: 860px; height: 250px;
  background: linear-gradient(118deg, #ffe3ec 0%, #ff9cbb 38%, #e0204b 74%, #6b081c 100%); }
.call { position: absolute; border-radius: 30px; background: #fbeef2; }
.lchip { position: absolute; height: 88px; border-radius: 44px; display: flex; align-items: center; justify-content: center;
  gap: 16px; font-size: 31px; font-weight: 700; letter-spacing: -0.005em; overflow: hidden; }
.lchip.pl { background: linear-gradient(160deg, #ffffff 0%, #fff5f8 52%, #f5dfe6 100%); color: #17141c;
  box-shadow: inset 0 2px 1px #fff, 0 30px 60px -22px rgba(30,4,12,0.6); }
.lchip.jl { background: linear-gradient(165deg, #e0204b 0%, #ab112e 46%, #6b081c 100%); color: #fff;
  box-shadow: inset 0 2px 1px rgba(255,255,255,0.5), 0 30px 60px -22px rgba(70,4,20,0.7); }
.lchip .lg { width: 42px; height: 42px; fill: none; stroke-width: 2.4; stroke-linecap: round; flex: none; }
.lchip.pl .lg { stroke: #b4122f; }
.lchip.jl .lg { stroke: #fff; }
.lchip .mkb { width: 44px; height: 44px; flex: none; }
.stk { position: absolute; height: 96px; border-radius: 48px; display: flex; align-items: center; justify-content: center;
  background: linear-gradient(165deg, #e0204b 0%, #ab112e 46%, #6b081c 100%); color: #fff; font-size: 40px; font-weight: 900;
  letter-spacing: 0.04em; box-shadow: inset 0 2px 1px rgba(255,255,255,0.5), 0 30px 60px -18px rgba(70,4,20,0.75); }

/* the chatbot */
.bub { position: absolute; }
.kpill { position: absolute; border-radius: 46px; display: flex; align-items: center; justify-content: center;
  background: linear-gradient(165deg, #e0204b 0%, #ab112e 46%, #6b081c 100%); color: #fff; font-size: 42px; font-weight: 900;
  letter-spacing: 0.03em; box-shadow: inset 0 2px 1px rgba(255,255,255,0.5), 0 26px 50px -18px rgba(70,4,20,0.7); }

/* the invoice form */
.fm { position: absolute; border-radius: 60px; overflow: hidden; color: #17141c;
  background: linear-gradient(172deg, #ffffff 0%, #fff9fb 55%, #fdf0f4 100%);
  box-shadow: inset 0 2px 1px #fff, 0 70px 130px -40px rgba(8,0,3,0.75), 0 0 0 1px rgba(255,255,255,0.35); }
.fm .lbl { position: absolute; left: 56px; font-size: 24px; font-weight: 700; letter-spacing: 0.16em; color: rgba(23,20,28,0.42); }
.fm .inp { position: absolute; left: 56px; width: 768px; height: 84px; border-radius: 24px; background: #fbeef2;
  box-shadow: inset 0 0 0 2px rgba(180,18,47,0.07); }
.fm .inp i { position: absolute; display: block; left: 28px; top: 32px; height: 20px; border-radius: 10px; background: rgba(23,20,28,0.16); }
.fm .inp b { position: absolute; right: 26px; top: 21px; width: 42px; height: 42px; display: block; }
.fT { font-size: 76px; font-weight: 700; letter-spacing: -0.02em; line-height: 1; }
.fP { font-size: 50px; font-weight: 700; letter-spacing: -0.015em; line-height: 1; }
.dz { position: absolute; width: 768px; height: 130px; border-radius: 30px; border: 4px dashed rgba(180,18,47,0.40);
  background: #fff7fa; }
.dzs { position: absolute; left: -4px; top: -4px; right: -4px; bottom: -4px; border-radius: 30px; border: 4px solid #ff6e9c;
  box-shadow: 0 0 0 9px rgba(255,110,156,0.16); }
.sv { position: absolute; border-radius: 56px; display: flex; align-items: center; justify-content: center;
  background: linear-gradient(165deg, #e0204b 0%, #ab112e 46%, #6b081c 100%); color: #fff; font-size: 46px; font-weight: 700;
  box-shadow: inset 0 2px 1px rgba(255,255,255,0.5), 0 24px 46px -18px rgba(70,4,20,0.6); }

/* stories / profile */
.st { position: absolute; border-radius: 32px; overflow: hidden;
  background: linear-gradient(170deg, #5c1022 0%, #b4122f 52%, #ff8ab0 100%);
  box-shadow: inset 0 2px 1px rgba(255,255,255,0.4), 0 40px 80px -30px rgba(24,4,12,0.65); }
.st i { position: absolute; display: block; }
.st .seg { top: 14px; height: 6px; border-radius: 3px; background: rgba(255,255,255,0.45); }
.sstk { position: absolute; height: 54px; border-radius: 27px; background: #fff; display: flex; align-items: center; gap: 10px;
  padding: 0 16px; box-shadow: 0 14px 28px -10px rgba(24,4,12,0.55); }
.sstk .lg { width: 30px; height: 30px; fill: none; stroke: #b4122f; stroke-width: 2.6; stroke-linecap: round; }
.sstk i { position: static; display: block; height: 12px; border-radius: 6px; background: rgba(180,18,47,0.55); }
.pf { position: absolute; border-radius: 40px; overflow: hidden;
  background: linear-gradient(172deg, #ffffff 0%, #fff8fa 60%, #fbecf1 100%);
  box-shadow: inset 0 2px 1px #fff, 0 40px 80px -30px rgba(24,4,12,0.62); }
.pf i { position: absolute; display: block; border-radius: 8px; }
.pf .av { position: absolute; left: 24px; top: 24px; width: 112px; height: 112px; border-radius: 50%;
  background: linear-gradient(135deg, #ffb3c9 0%, #e0204b 55%, #8d0d24 100%); }
.pf .av b { position: absolute; left: 7px; top: 7px; width: 98px; height: 98px; border-radius: 50%; background: #fdeef3;
  box-shadow: inset 0 0 0 4px #fff; display: flex; align-items: center; justify-content: center; }
.pf .av .sk { width: 56%; height: 56%; stroke: #b4122f; }
.pflk { position: absolute; left: 24px; top: 236px; height: 34px; display: flex; align-items: center; gap: 10px; }
.pflk .lg { width: 30px; height: 30px; fill: none; stroke: #b4122f; stroke-width: 2.6; stroke-linecap: round; }
.pflk i { position: static; display: block; width: 190px; height: 14px; border-radius: 7px; background: rgba(180,18,47,0.6); }
.pfbt { position: absolute; left: 24px; top: 284px; width: 304px; height: 36px; border-radius: 12px;
  background: linear-gradient(165deg, #e0204b 0%, #8d0d24 100%); }
.tbub { position: absolute; height: 50px; border-radius: 25px; background: #fff; display: flex; align-items: center; gap: 10px;
  padding: 0 16px; box-shadow: 0 14px 28px -10px rgba(24,4,12,0.55); }
.tbub .lg { width: 28px; height: 28px; fill: none; stroke: #b4122f; stroke-width: 2.6; stroke-linecap: round; }
.tbub i { display: block; width: 74px; height: 12px; border-radius: 6px; background: rgba(23,20,28,0.25); }

/* the Gmail notification */
#eN .app { position: absolute; left: 168px; top: 34px; font-size: 30px; font-weight: 700; color: rgba(255,255,255,0.72); }
#eN .tm  { position: absolute; right: 44px; top: 36px; font-size: 26px; font-weight: 500; color: rgba(255,255,255,0.5); }
.att { position: absolute; height: 52px; border-radius: 26px; background: rgba(255,255,255,0.94); display: flex; align-items: center;
  gap: 12px; padding: 0 18px; }
.att .sk { width: 32px; height: 32px; stroke: #b4122f; }
.att i { display: block; height: 12px; border-radius: 6px; background: rgba(23,20,28,0.3); }
.att .mkb { width: 28px; height: 28px; }

/* the long bar */
.trk { position: absolute; height: 44px; border-radius: 22px; background: rgba(255,255,255,0.14);
  box-shadow: inset 0 1.5px 1px rgba(255,255,255,0.3); }
.fil { position: absolute; height: 44px; border-radius: 22px;
  background: linear-gradient(180deg, #ffffff 0%, #ffe6ee 100%); box-shadow: inset 0 2px 1px #fff; }
.fil.hot { background: linear-gradient(165deg, #ff8ab0 0%, #e0204b 55%, #8d0d24 100%);
  filter: drop-shadow(0 0 14px rgba(255,110,156,0.75)); }
.pgx { position: absolute; width: 116px; height: 146px; border-radius: 22px;
  background: linear-gradient(172deg, #ffffff 0%, #fdf0f4 100%); box-shadow: 0 14px 30px -12px rgba(24,4,12,0.5); }
.dch { position: absolute; height: 66px; border-radius: 33px;
  background: linear-gradient(160deg, #ffffff 0%, #fff5f8 52%, #f5dfe6 100%);
  box-shadow: inset 0 2px 1px #fff, 0 22px 44px -16px rgba(30,4,12,0.6); }
.dch span { position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; font-size: 34px;
  font-weight: 900; color: #17141c; letter-spacing: -0.01em; }

/* follow */
.fl { position: absolute; border-radius: 80px; overflow: hidden;
  background: linear-gradient(160deg, #ffffff 0%, #fff5f8 52%, #f5dfe6 100%);
  box-shadow: inset 0 2px 1px #fff, 0 40px 80px -28px rgba(30,4,12,0.65); }
.fl .t { position: absolute; left: 160px; top: 0; height: 150px; line-height: 150px; font-size: 56px; font-weight: 700;
  letter-spacing: -0.02em; color: #17141c; }
.fl .on { position: absolute; inset: 0; background: linear-gradient(165deg, #e0204b 0%, #ab112e 46%, #6b081c 100%);
  opacity: 0; visibility: hidden; }
.fl .on .t { color: #fff; left: 150px; }
""")

L = []
BEATS = []


def beat(fn):
    BEATS.append(fn)
    return fn


def link_svg(cls="lg"):
    return '<svg class="%s" viewBox="0 0 24 24">%s</svg>' % (cls, STROKES["link"])


# ===========================================================================
# A · hook — a guide to sell, or a lead magnet; days and hours it eats
@beat
def a_hook():
    coin = uah(78, "#fff", 2.5)
    badge = ('<div class="fx hide" id="aB" style="left:612px;top:92px;width:136px;height:136px">'
             '<div class="fxi" id="aBi">'
             '<div class="ff circ"><div class="jelly">%s<div class="sheen"></div></div></div>'
             '<div class="ff bk circ"><div class="pearl">%s</div></div>'
             '</div></div>' % (coin, MAGNET))
    people = "".join(tile("aP%d" % i, 92, 790, 250 + i * 110, "pearl", stroke("person"), extra_cls="circ", ring=False)
                     for i in range(3))
    costs = ""
    for n, (name, y) in enumerate((("calendar", 252), ("clock", 384))):
        costs += ('<div class="tw hide ghost" id="aG%d" style="left:214px;top:%dpx;width:116px;height:116px">'
                  '<div class="clear">%s</div></div>' % (n, y, stroke(name)))
        costs += tile("aK%d" % n, 116, 214, y, "pearl", stroke(name), ring=False)
    L.append('<div class="g full" id="gA">' + gdoc("aD", 390, 150, 1.0) + badge + people + costs + '</div>')
    sfx("pop", 0.06, -3)
    sfx("pop", T["prodaty"] - 0.05, -1)
    sfx("click-soft", T["lidmagnit"], -2)
    return js("""
  tl.set("#gA", {autoAlpha: 1}, 0);
  arr("#aD", 0.04, {s: 0.6, y: 40});
  arr("#aB", @prodaty-0.1, {s: 0.3, x: -20, y: 30, d: 0.7});
  shn("#aD .sheen", @haid0-0.1); G.bump("#aD", @haid0);
  tl.to("#aBi", {rotationY: 180, duration: 0.8, ease: FLIP}, @lidmagnit-0.08);
  [0, 1, 2].forEach(function (i) { arr("#aP" + i, @lidmagnit+0.18 + i * 0.1, {s: 0.7, x: 230, y: 0, d: 0.75}); });
  G.bump("#aB", @lidmagnit+0.7);
  bin(["#aG0", "#aG1"], @vytrachaty-0.08, 8, 0.3);
  arr("#aK0", @dni-0.06, {s: 0.85, y: 0, d: 0.55, blur: 8}); tl.set("#aG0", {autoAlpha: 0}, @dni+0.25);
  arr("#aK1", @hodyny-0.06, {s: 0.85, y: 0, d: 0.55, blur: 8}); tl.set("#aG1", {autoAlpha: 0}, @hodyny+0.25);
  bout("#gA", @aend, 10, 0.28);""")


# ===========================================================================
# B · design, layout, settings — and so on; they collapse into one point
@beat
def b_setup():
    tiles = (tile("bT0", 200, 95, 65, "pearl", stroke("palette"))
             + tile("bT1", 200, 370, 65, "pearl", stroke("layout"))
             + tile("bT2", 200, 645, 65, "pearl", stroke("gear")))
    L.append('<div class="g full" id="gB"><div class="shelf edge hide" id="bS" '
             'style="left:70px;top:170px;width:940px;height:330px">' + tiles + '</div></div>')
    sfx("pop", T["dyzain"] - 0.05, -1)
    sfx("pop", T["nalasht"] - 0.05, -2)
    sfx("whoosh-short", T["pokazhu"] - 0.25)
    return js("""
  tl.set("#gB", {autoAlpha: 1}, @b0);
  arr("#bS", @b0, {s: 0.85, y: 30});
  arr("#bT0", @dyzain-0.08, {s: 0.4, y: 30}); G.ripple("#bT0R", @dyzain+0.25);
  arr("#bT1", @oform-0.08, {s: 0.4, y: 30}); G.ripple("#bT1R", @oform+0.25);
  arr("#bT2", @nalasht-0.08, {s: 0.4, y: 30}); G.ripple("#bT2R", @nalasht+0.25);
  tl.to("#bT2 .sk", {rotation: 120, transformOrigin: "50% 50%", duration: 1.0, ease: SP}, @tak-0.05);
  G.haptic("#bT0", @tak); G.haptic("#bT1", @tak+0.1); G.haptic("#bT2", @tak+0.2);
  tl.to("#bT0", {x: 275, scale: 0.2, autoAlpha: 0, duration: 0.42, ease: "power3.in"}, @pokazhu-0.3);
  tl.to("#bT1", {scale: 0.2, autoAlpha: 0, duration: 0.42, ease: "power3.in"}, @pokazhu-0.3);
  tl.to("#bT2", {x: -275, scale: 0.2, autoAlpha: 0, duration: 0.42, ease: "power3.in"}, @pokazhu-0.3);
  tl.to("#bS", {scale: 0.25, autoAlpha: 0, duration: 0.45, ease: "power3.in"}, @pokazhu-0.24);
  tl.set("#gB", {autoAlpha: 0}, @pokazhu+0.3);""")


# ===========================================================================
# C · OVER: the stopwatch, 15:00
@beat
def c_fifteen():
    L.append('<div class="g full" id="gC">' + ground() + stopwatch("c")
             + '<div class="bigt hide" id="cD" style="top:550px;height:300px;line-height:300px;font-size:300px">15:00</div>'
             + '</div>')
    sfx("pop", T["p15"] - 0.04)
    sfx("click", T["khvylyn"] + 0.02)
    return js("""
  G.irisOpen("#gC", @c0, 540, 335, 0.8);
  drift1("#gC", @c0, @pershyi-@c0);
  tl.set("#cArc", {opacity: 1}, @bukv-0.05);
  draw2("cArc", @bukv-0.05, 1.85);
  bin("#cD", @p15-0.06, 16, 0.3);
  tl.fromTo("#cD", {scale: 1.5}, {scale: 1, duration: 0.6, ease: POP, immediateRender: false}, @p15-0.06);
  press("#cCr", @khvylyn);
  G.bump("#cD", @khvylyn+0.05);
  G.irisClose("#gC", @pershyi-0.24, 256, 154, 0.5);""")


# ===========================================================================
# the step bar: the timer the steps spend, and which step this is
@beat
def s_stepbar():
    L.append(
        '<div class="g full" id="gSB"><div class="dglass edge hide" id="sb" '
        'style="left:190px;top:92px;width:700px;height:124px;border-radius:62px">'
        '<svg class="tmr" id="sbT" viewBox="0 0 80 80"><circle class="trk" cx="40" cy="40" r="32"/>'
        '<circle class="arc" id="sbA" cx="40" cy="40" r="32" transform="rotate(-90 40 40)"/></svg>'
        '<div class="dw" id="sbW"><div id="sbD"><b>15:00</b><b>14:00</b><b>13:00</b></div></div>'
        '<div class="sep" id="sbSep"></div>'
        u'<div class="cw" id="sbCw"><div id="sbC"><b>КРОК 1 · 1 хв</b><b>КРОК 2 · 1 хв</b>'
        u'<b class="hot">КРОК 3 %s</b></div></div>'
        '<div class="shc"><div class="sheen"></div></div></div></div>' % STAR)
    sfx("click-soft", T["khvylynu"] - 0.1, -2)
    sfx("click-soft", T["khvylyna"] - 0.1, -2)
    sfx("sparkle", T["naivazh"] - 0.05, -2)
    c = 2 * 3.14159265 * 32
    return js("""
  tl.set("#gSB", {autoAlpha: 1}, @sb0);
  gsap.set("#sb", {transformOrigin: "66px 62px"});
  arr("#sb", @sb0, {s: 0.4, x: -30, y: 0, d: 0.75});
  gsap.set("#sbA", {strokeDasharray: "@cc 400", strokeDashoffset: 0});
  tl.to("#sbD", {y: -88, duration: 0.55, ease: "power3.inOut"}, @khvylynu-0.12);
  tl.to("#sbA", {strokeDashoffset: @c1, duration: 0.55, ease: "power3.inOut"}, @khvylynu-0.12);
  tl.to("#sbC", {y: -84, duration: 0.55, ease: "power3.inOut"}, @druhyi-0.1);
  tl.to("#sbD", {y: -176, duration: 0.55, ease: "power3.inOut"}, @khvylyna-0.12);
  tl.to("#sbA", {strokeDashoffset: @c2, duration: 0.55, ease: "power3.inOut"}, @khvylyna-0.12);
  tl.to(["#sbT", "#sbW", "#sbSep"], {autoAlpha: 0.3, duration: 0.4}, @dali);
  tl.to("#sbC", {y: -168, duration: 0.55, ease: "power3.inOut"}, @naivazh-0.1);
  G.bump("#sb", @naivazh+0.35); shn("#sb .sheen", @naivazh+0.3);
  bout("#gSB", @fend, 10, 0.28);""", cc=c, c1=c / 15.0, c2=2 * c / 15.0)


# ===========================================================================
# D/E · step 1: a Notion account; step 2: Claude or ChatGPT, wired to Notion
@beat
def de_steps():
    c1 = "M404 390 C 590 390 590 285 766 285"
    c2 = "M404 390 C 590 390 590 495 766 495"
    cab = ('<svg class="cab abs" width="1080" height="700" viewBox="0 0 1080 700" style="left:0;top:0">'
           + cable("e1", c1) + cable("e2", c2) + '</svg>')
    L.append('<div class="g full" id="gDE">' + cab
             + '<div class="tw hide ghost" id="dG" style="left:420px;top:270px;width:240px;height:240px">'
               '<div class="clear">%s</div></div>' % g.mark("notion")
             + tile("dN", 240, 420, 270, "pearl", g.mark("notion"))
             + '<div class="sqring" id="dNR2" style="left:200px;top:290px;width:200px;height:200px"></div>'
             + tile("dPl", 84, 622, 236, "jelly", stroke("plus"), extra_cls="circ", ring=False)
             + tile("dOk", 84, 622, 236, "jelly", stroke("check"), extra_cls="circ", ring=False)
             + tile("eC", 170, 770, 200, "jelly", g.mark("claude"))
             + tile("eO", 170, 770, 410, "pearl", g.mark("openai"))
             + '</div>')
    sfx("pop", T["notion1"] - 0.03)
    sfx("pop", T["klod"] - 0.04, -1)
    sfx("click", T["notion2"] - 0.1, -1)
    return js("""
  tl.set("#gDE", {autoAlpha: 1}, @stvor-0.1);
  arr(["#dG", "#dPl"], @stvor-0.06, {s: 0.6, y: 20, d: 0.7});
  arr("#dN", @notion1-0.05, {s: 0.85, y: 0, d: 0.6, blur: 8}); G.ripple("#dNR", @notion1+0.2);
  tl.set("#dG", {autoAlpha: 0}, @notion1+0.3);
  tl.to("#dPl", {scale: 0.3, autoAlpha: 0, duration: 0.2, ease: "power2.in"}, @nema-0.05);
  arr("#dOk", @nema+0.05, {s: 0.3, y: 0, d: 0.55});
  bout("#dOk", @druhyi-0.05, 8, 0.25);
  tl.to("#dN", {x: -220, y: 20, scale: 0.8333, transformOrigin: "0px 0px", duration: 0.7, ease: SP}, @vidkr-0.15);
  arr("#eC", @klod-0.06, {s: 0.4, x: 30, y: 20}); G.ripple("#eCR", @klod+0.25);
  arr("#eO", @chatgpt-0.06, {s: 0.4, x: 30, y: 20}); G.ripple("#eOR", @chatgpt+0.25);
  tl.set(["#e1T", "#e1K", "#e2T", "#e2K"], {autoAlpha: 1}, @pidkl-0.05);
  draw2("e1T", @pidkl-0.05, 0.5); draw2("e1K", @pidkl-0.05, 0.5);
  draw2("e2T", @pidkl+0.05, 0.5); draw2("e2K", @pidkl+0.05, 0.5);
  bmp("#dN", @notion2-0.08, 0.8333); G.ripple("#dNR2", @notion2-0.02);
  G.packet("e1P", @notion2-0.05, 0.5); G.packet("e2P", @notion2-0.05, 0.5);
  G.bump("#eC", @notion2+0.42); G.bump("#eO", @notion2+0.46);
  bout("#gDE", @dali-0.06, 10, 0.28);""")


# ===========================================================================
# F · step 3: talk to it — the mic, a live waveform into Claude, a draft
WB_N = 24


@beat
def f_voice():
    bars = "".join('<i class="wb" style="left:%dpx"></i>' % (252 + i * 18) for i in range(WB_N))
    draft = ('<div class="dr hide" id="fDr" style="left:250px;top:50px;width:460px;height:200px">'
             '<i class="cov" id="fDc"></i>'
             '<i class="rr" style="left:30px;top:80px;width:400px;height:15px"></i>'
             '<i class="rr" style="left:30px;top:110px;width:356px;height:15px"></i>'
             '<i class="rr" style="left:30px;top:140px;width:390px;height:15px"></i>'
             '<i class="rr" style="left:30px;top:170px;width:220px;height:15px"></i>'
             '<div class="shc"><div class="sheen"></div></div></div>')
    L.append('<div class="g full" id="gF"><div class="dglass edge hide" id="fP" '
             'style="left:70px;top:262px;width:940px;height:300px;border-radius:64px">'
             '<div class="mring" id="fMr" style="left:40px;top:65px;width:170px;height:170px"></div>'
             '<div class="tw circ" id="fM" style="left:40px;top:65px;width:170px;height:170px"><div class="jelly">%s</div></div>'
             '%s%s'
             '<div class="sqring" id="fCR" style="left:760px;top:75px;width:150px;height:150px"></div>'
             '<div class="tw" id="fC" style="left:760px;top:75px;width:150px;height:150px"><div class="jelly">%s'
             '<div class="sheen"></div></div></div>'
             '</div></div>' % (stroke("mic"), bars, draft, g.mark("claude")))
    sfx("click-soft", T["nahovor"], -3)
    return js("""
  tl.set("#gF", {autoAlpha: 1}, @ty-0.15);
  arr("#fP", @ty-0.12, {s: 0.85, y: 40});
  G.inner("#fM", @ty-0.12); G.inner("#fC", @ty-0.02);
  G.bump("#fM", @nahovor);
  tl.fromTo("#fMr", {scale: 1, autoAlpha: 0.85}, {scale: 1.45, autoAlpha: 0, duration: 0.8, ease: "power2.out", immediateRender: false}, @nahovor);
  G.bump("#fC", @intelektu); G.ripple("#fCR", @intelektu+0.05);
  tl.to(".wb", {autoAlpha: 0, duration: 0.25}, @rozkaz-0.15);
  arr("#fDr", @rozkaz-0.1, {s: 0.7, y: 20, d: 0.7});
  tl.fromTo("#fDc", {scaleY: 0}, {scaleY: 1, duration: 0.45, ease: SP, immediateRender: false}, @lidmag2-0.05);
  shn("#fDr .sheen", @lidmag2+0.2);
  bout("#gF", @fend, 10, 0.28);""")


# ===========================================================================
# G · OVER: a skill rewrites the draft in her style
OLD_W = [720, 640, 760, 520, 700, 600, 740, 430]
NEW_L = [
    '<i class="hb" style="left:0;top:-4px;width:520px;height:42px;border-radius:14px"></i>',
    '<i class="hl" style="left:130px;top:1px;width:236px;height:40px"></i><i class="rr" style="left:0;top:8px;width:700px;height:26px;border-radius:13px"></i>',
    '<i class="rr" style="left:0;top:8px;width:610px;height:26px;border-radius:13px"></i>',
    '<i class="bd" style="left:0;top:10px"></i><i class="rr" style="left:42px;top:8px;width:560px;height:26px;border-radius:13px"></i>',
    '<i class="bd" style="left:0;top:10px"></i><i class="rr" style="left:42px;top:8px;width:470px;height:26px;border-radius:13px"></i>',
    '<i class="hb" style="left:0;top:-2px;width:380px;height:38px;border-radius:13px"></i>',
    '<i class="hl" style="left:400px;top:1px;width:196px;height:40px"></i><i class="rr" style="left:0;top:8px;width:690px;height:26px;border-radius:13px"></i>',
    '<i class="rr" style="left:0;top:8px;width:400px;height:26px;border-radius:13px"></i>',
]
LINE_Y = [180 + i * 92 for i in range(8)]
SCAN_Y0, SCAN_DY, SCAN_D = 170, 700, 1.1


@beat
def g_skill():
    old = "".join('<i class="ol" id="gO%d" style="left:50px;top:%dpx;width:%dpx"></i>' % (i, y, w)
                  for i, (y, w) in enumerate(zip(LINE_Y, OLD_W)))
    new = "".join('<div class="nl" id="gN%d" style="top:%dpx">%s</div>' % (i, y, h)
                  for i, (y, h) in enumerate(zip(LINE_Y, NEW_L)))
    sheet = ('<div class="sheet hide" id="gS" style="left:100px;top:150px;width:880px;height:1040px">'
             '<div class="tw" style="left:50px;top:46px;width:84px;height:84px"><div class="jelly">%s</div></div>'
             '<i class="hb" style="left:160px;top:68px;width:340px;height:40px;border-radius:14px"></i>'
             '%s%s<i class="scan" id="gScan" style="top:%dpx"></i>'
             '<svg class="abs" width="420" height="170" viewBox="0 0 420 170" style="left:420px;top:850px;overflow:visible">'
             '<path class="sig" id="gSig" d="%s"/></svg>'
             '<div class="sheen"></div></div>' % (g.mark("claude"), old, new, SCAN_Y0, SIG))
    skill = ('<div class="sqring" id="gKR" style="left:730px;top:60px;width:230px;height:230px"></div>'
             '<div class="tw hide" id="gK" style="left:730px;top:60px;width:230px;height:230px"><div class="jelly">'
             '<div class="sklab">%s<span>SKILL.md</span></div><div class="sheen"></div></div></div>' % stroke("doc"))
    L.append('<div class="g full" id="gG">' + ground() + sheet + skill + '</div>')
    sfx("whoosh-short", T["g0"] - 0.02)
    sfx("pop", T["skil"] - 0.04)
    swaps = []
    t0 = T["perepys"] - 0.04
    for i, y in enumerate(LINE_Y):
        ti = t0 + (y + 14 - (SCAN_Y0 + 8)) / float(SCAN_DY) * SCAN_D
        swaps.append('  tl.to("#gO%d", {autoAlpha: 0, duration: 0.15}, %.3f);'
                     ' tl.fromTo("#gN%d", {autoAlpha: 0, x: -16}, {autoAlpha: 1, x: 0, duration: 0.35, ease: SP, immediateRender: false}, %.3f);'
                     % (i, ti, i, ti))
    return js("""
  G.irisOpen("#gG", @g0, 540, 412, 0.85);
  drift1("#gG", @g0, @napyshy+0.3-@g0);
  gsap.set("#gS", {transformOrigin: "440px 262px"});
  arr("#gS", @g0+0.05, {s: 0.4, y: 0, d: 0.9});
  arr("#gK", @skil-0.06, {s: 0.3, x: 40, y: -40}); G.ripple("#gKR", @skil+0.25);
  tl.set("#gScan", {autoAlpha: 1}, @perepys-0.04);
  tl.fromTo("#gScan", {y: 0}, {y: @sdy, duration: @sd, ease: "none", immediateRender: false}, @perepys-0.04);
  tl.to("#gScan", {autoAlpha: 0, duration: 0.2}, @perepys+1.02);
  G.bump("#gK", @perepys);
{{swaps}}
  tl.set("#gSig", {opacity: 1}, @tvoiemu-0.05);
  draw2("gSig", @tvoiemu-0.05, 0.85);
  shn("#gS > .sheen", @styli);
  G.irisClose("#gG", @napyshy-0.2, 540, 280, 0.5);""", sdy=SCAN_DY, sd=SCAN_D).replace("{{swaps}}", "\n".join(swaps))


# ===========================================================================
# H · the DM: «КОПІ» -> a YouTube link comes back. She leans in here (hair ~y 510):
# the card stays above y 490.
@beat
def h_dm():
    card = ('<div class="dglass edge hide" id="hD" style="left:90px;top:70px;width:900px;height:420px;border-radius:56px">'
            '<div class="tw circ" style="left:28px;top:16px;width:62px;height:62px"><div class="jelly">%s</div></div>'
            '<i class="bar" style="left:106px;top:28px;width:200px;height:18px;background:rgba(255,255,255,0.6)"></i>'
            '<i class="bar" style="left:106px;top:56px;width:120px;height:12px;background:rgba(255,255,255,0.28)"></i>'
            '<i class="bar" style="left:0;top:92px;width:900px;height:2px;border-radius:0;background:rgba(255,255,255,0.10)"></i>'
            u'<div class="dmb hide" id="hS" style="left:684px;top:106px;width:188px;height:62px">КОПІ</div>'
            '<div class="bub hide" id="hR" style="left:28px;top:180px;width:540px;height:150px">'
            '<div class="thumb" style="left:12px;top:12px;width:516px;height:92px"><span id="hY" style="display:flex">%s</span></div>'
            '<div class="yring" id="hYr" style="left:270px;top:58px"></div>'
            '<i class="bar" style="left:14px;top:118px;width:280px;height:14px;background:rgba(23,20,28,0.6)"></i>'
            '<div class="shc"><div class="sheen"></div></div></div>'
            '<div class="bub" id="hI" style="left:28px;top:342px;width:844px;height:62px"><div class="dtx" id="hT"></div>'
            '<div class="tw circ" id="hSend" style="left:788px;top:6px;width:50px;height:50px"><div class="jelly">%s</div></div></div>'
            '</div>' % (g.mark("instagram"), g.mark("youtube"), stroke("up")))
    L.append('<div class="g full" id="gH">' + card + '</div>')
    sfx("typing", T["kopi"], -2)
    sfx("click", T["i_ya"])
    sfx("notification", T["posyl1"] - 0.04, -2)
    return js("""
  tl.set("#gH", {autoAlpha: 1}, @napyshy-0.2);
  arr("#hD", @napyshy-0.16, {s: 0.8, y: 30, d: 0.8});
  G.bump("#hSend", @i_ya);
  arr("#hS", @i_ya+0.06, {s: 0.6, y: 200, d: 0.7});
  arr("#hR", @posyl1-0.06, {s: 0.7, x: -40, y: 20, d: 0.7});
  G.bump("#hY", @youtube);
  tl.fromTo("#hYr", {scale: 0.6, autoAlpha: 0.9}, {scale: 1.7, autoAlpha: 0, duration: 0.7, ease: "power2.out", immediateRender: false}, @youtube);
  shn("#hR .sheen", @youtube+0.1);
  bout("#gH", @koly-0.1, 10, 0.28);""")


# ===========================================================================
# I · the voice notes go in, the prompt types itself
PROMPT = u"Зроби з цього гарний гайд прямо в Notion"
VPL = [(80, 410), (330, 440), (600, 404)]


@beat
def i_prompt():
    cab = ('<svg class="cab abs" width="1080" height="700" viewBox="0 0 1080 700" style="left:0;top:0">'
           + cable("i1", "M344 215 C 460 160 620 160 736 215") + '</svg>')
    pills = ""
    hs = (18, 34, 24, 42, 28, 36, 16)
    for n, (x, y) in enumerate(VPL):
        pills += ('<div class="vpl hide" id="iV%d" style="left:%dpx;top:%dpx">%s</div>'
                  % (n, x, y, "".join('<i style="height:%dpx"></i>' % h for h in hs[n:] + hs[:n])))
    bar = ('<div class="dglass edge hide" id="iB" style="left:60px;top:380px;width:960px;height:210px;border-radius:52px">'
           '<div class="ptx" id="iT"></div>'
           '<div class="tw circ" id="iSend" style="left:846px;top:100px;width:84px;height:84px"><div class="jelly">%s</div></div>'
           '</div>' % stroke("up"))
    L.append('<div class="g full" id="gI">' + cab
             + tile("iC", 190, 150, 120, "jelly", g.mark("claude"))
             + tile("iN", 190, 740, 120, "pearl", g.mark("notion"))
             + pills + bar + '</div>')
    mv = []
    for n, (x, y) in enumerate(VPL):
        mv.append('  tl.to("#iV%d", {x: %d, y: %d, scale: 0.15, autoAlpha: 0, duration: 0.45, ease: "power2.in"}, %.3f);'
                  % (n, 245 - (x + 95), 215 - (y + 30), T["nahovoreno"] - 0.05 + n * 0.08))
    sfx("typing", T["zrobyty"], -1)
    sfx("click", T["notion3"] + 0.08)
    return js("""
  tl.set("#gI", {autoAlpha: 1}, @koly-0.1);
  arr("#iC", @koly-0.06, {s: 0.5, y: 30});
  [0, 1, 2].forEach(function (i) { arr("#iV" + i, @koly+0.12 + i * 0.1, {s: 0.6, y: 40, d: 0.6}); });
{{mv}}
  G.bump("#iC", @nahovoreno+0.42); G.ripple("#iCR", @nahovoreno+0.42);
  arr("#iN", @prosysh-0.06, {s: 0.4, y: 30});
  tl.set(["#i1T", "#i1K"], {autoAlpha: 1}, @prosysh+0.3);
  draw2("i1T", @prosysh+0.3, 0.5); draw2("i1K", @prosysh+0.3, 0.5);
  arr("#iB", @shtuchnyi-0.1, {s: 0.85, y: 40, d: 0.7});
  G.bump("#iSend", @notion3+0.08);
  G.packet("i1P", @notion3+0.1, 0.4);
  G.bump("#iN", @notion3+0.42); G.ripple("#iNR", @notion3+0.42);
  tl.set("#gI", {autoAlpha: 0}, @j0+1.0);""").replace("{{mv}}", "\n".join(mv))


# ===========================================================================
# J' · OVER: the guide page builds in Notion; its link; free; ready
@beat
def j_page():
    rows = ""
    for n, (y, w) in enumerate(((724, 520), (796, 440), (868, 560))):
        rows += ('<div class="cbx jb" style="left:60px;top:%dpx"></div>'
                 '<i class="rr jb" style="left:132px;top:%dpx;width:%dpx;height:22px;border-radius:11px"></i>' % (y, y + 14, w))
    page = ('<div class="np hide" id="jP" style="left:110px;top:150px;width:860px;height:1040px">'
            '<i class="ncov" id="jCv"></i>'
            '<div class="tw" id="jIc" style="left:60px;top:176px;width:150px;height:150px"><div class="jelly">%s</div></div>'
            '<i class="hb" id="jTi" style="left:60px;top:370px;width:560px;height:60px;border-radius:18px"></i>'
            '<i class="rr jb" style="left:60px;top:458px;width:640px;height:22px;border-radius:11px"></i>'
            '<i class="rr jb" style="left:60px;top:494px;width:480px;height:22px;border-radius:11px"></i>'
            '<div class="call jb" style="left:60px;top:552px;width:740px;height:136px">'
            '<div class="tw circ" style="left:26px;top:31px;width:74px;height:74px"><div class="jelly">%s</div></div>'
            '<i class="rr" style="left:126px;top:44px;width:520px;height:20px;border-radius:10px"></i>'
            '<i class="rr" style="left:126px;top:78px;width:360px;height:20px;border-radius:10px"></i></div>'
            '%s<div class="shc"><div class="sheen"></div></div></div>'
            % (stroke("doc"), STAR.replace('width="34" height="34"', 'width="38" height="38" style="position:relative;z-index:1"'), rows))
    L.append('<div class="g full" id="gJ">' + ground() + page
             + chip("jL", 310, 92, 460, "pl", link_svg() + '<span>notion.site/guide</span>')
             + u'<div class="stk hide" id="jF" style="left:560px;top:330px;width:380px">БЕЗКОШТОВНО</div>'
             + '<div class="ck" id="jOkR" style="left:855px;top:1115px"></div>'
             + tile("jOk", 170, 770, 1030, "jelly", stroke("check"), extra_cls="circ", ring=False)
             + '</div>')
    sfx("whoosh-short", T["j0"] - 0.02)
    sfx("pop", T["bezkosht"] - 0.04)
    sfx("pop", T["hotova"] - 0.04, -2)
    return js("""
  G.irisOpen("#gJ", @j0, 835, 215, 0.8);
  drift1("#gJ", @j0, @beresh+0.5-@j0);
  gsap.set("#jP", {transformOrigin: "725px 65px"});
  arr("#jP", @j0+0.04, {s: 0.25, y: 0, d: 0.9});
  tl.fromTo("#jCv", {scaleY: 0}, {scaleY: 1, transformOrigin: "50% 0%", duration: 0.5, ease: SP}, @j0+0.3);
  G.inner("#jIc", @j0+0.4);
  tl.fromTo("#jTi", {scaleX: 0}, {scaleX: 1, transformOrigin: "0% 50%", duration: 0.5, ease: SP}, @j0+0.5);
  tl.fromTo("#jP .jb", {autoAlpha: 0, y: 26}, {autoAlpha: 1, y: 0, duration: 0.45, ease: SP, stagger: 0.06}, @j0+0.58);
  arr("#jL", @posyl2-0.08, {s: 0.5, y: 50, d: 0.7}); shn("#jL .sheen", @posyl2+0.3);
  gsap.set("#jF", {rotation: -7});
  arr("#jF", @bezkosht-0.06, {s: 1.6, y: 0, d: 0.6, blur: 6});
  arr("#jOk", @hotova-0.06, {s: 0.3, y: 0, d: 0.6});
  tl.fromTo("#jOkR", {scale: 0.8, autoAlpha: 0.95}, {scale: 2.2, autoAlpha: 0, duration: 0.7, ease: "power2.out", immediateRender: false}, @hotova+0.1);
  G.irisClose("#gJ", @beresh-0.07, 540, 136, 0.5);""")


# ===========================================================================
# J · the link goes into a chatbot; a person gets the guide
@beat
def k_bot():
    bot = ('<div class="dglass edge hide" id="kB" style="left:80px;top:236px;width:560px;height:350px;border-radius:52px">'
           '<div class="tw circ" style="left:24px;top:22px;width:72px;height:72px"><div class="jelly">%s</div></div>'
           '<i class="bar" style="left:112px;top:38px;width:170px;height:20px;background:rgba(255,255,255,0.6)"></i>'
           '<i class="bar" style="left:112px;top:68px;width:100px;height:12px;background:rgba(255,255,255,0.28)"></i>'
           '<i class="bar" style="left:0;top:114px;width:560px;height:2px;border-radius:0;background:rgba(255,255,255,0.10)"></i>'
           '<div class="bub" style="left:300px;top:132px;width:232px;height:60px;border-radius:30px 30px 8px 30px;'
           'background:rgba(255,255,255,0.16)"><i class="bar" style="left:26px;top:24px;width:150px;height:12px;'
           'background:rgba(255,255,255,0.55)"></i></div>'
           '<div class="bub hide" id="kBb" style="left:24px;top:212px;width:340px;height:100px;border-radius:32px 32px 32px 8px;'
           'background:rgba(255,255,255,0.18);box-shadow:inset 0 0 0 1.5px rgba(255,255,255,0.22)"></div>'
           '</div>' % stroke("bot"))
    L.append('<div class="g full" id="gK">' + bot
             + tile("kP", 190, 790, 300, "pearl", stroke("person"), extra_cls="circ")
             + gdoc("kG", 640, 330, 0.4)
             + tile("kOk", 66, 930, 290, "jelly", stroke("check"), extra_cls="circ", ring=False)
             + chip("kL", 310, 92, 460, "pl", link_svg() + '<span>notion.site/guide</span>')
             + '</div>')
    sfx("click", T["chatbota"] - 0.02)
    sfx("click-soft", T["haid3"], -2)
    return js("""
  tl.set(["#gK", "#kL"], {autoAlpha: 1}, @beresh-0.07);
  G.bump("#kL", @posyl3);
  arr("#kB", @vstavl-0.1, {s: 0.75, y: 40, d: 0.75});
  tl.to("#kL", {x: -266, y: 362, scale: 0.66, duration: 0.5, ease: "power3.inOut"}, @chatbota-0.4);
  bin("#kBb", @chatbota+0.02, 6, 0.25);
  arr("#kP", @liudyna-0.06, {s: 0.4, y: 30}); G.ripple("#kPR", @liudyna+0.25);
  tl.fromTo("#kG", {autoAlpha: 0, x: -340, y: 70, scale: 0.6}, {autoAlpha: 1, x: 0, y: 0, scale: 1, duration: 0.42, ease: "power2.out"}, @otrymuie-0.05);
  G.bump("#kP", @haid3); arr("#kOk", @haid3, {s: 0.3, y: 0, d: 0.5});
  bout("#gK", @yakshcho2-0.14, 10, 0.26);""")


# ===========================================================================
# K · paid: a ₴ tag on the guide, +1 step, WayForPay
@beat
def pd_paid():
    L.append('<div class="g full" id="gPd">'
             '<div class="abs" id="pdG" style="left:0;top:0;width:1080px;height:700px">'
             + gdoc("pdD", 405, 140, 0.9)
             + '<div class="abs hide" id="pdT" style="left:628px;top:225px;width:210px;height:130px">%s</div>' % TAG
             + '</div>'
             + u'<div class="kpill hide" id="pdK" style="left:126px;top:250px;width:250px;height:92px">+1 КРОК</div>'
             + wide("pdW", 470, 300, 440, 170, wfp(66))
             + '</div>')
    sfx("pop", T["oplatu"] - 0.1, -2)
    sfx("pop", T["ye"] - 0.04)
    sfx("pop", T["wfp"] - 0.06, -1)
    return js("""
  tl.set("#gPd", {autoAlpha: 1}, @yakshcho2-0.1);
  arr("#pdD", @yakshcho2-0.05, {s: 0.6, y: 40});
  gsap.set("#pdT", {transformOrigin: "40px 65px"});
  bin("#pdT", @oplatu-0.12, 6, 0.2);
  tl.fromTo("#pdT", {rotation: -80}, {rotation: 0, duration: 1.4, ease: SWING, immediateRender: false}, @oplatu-0.12);
  arr("#pdK", @ye-0.06, {s: 0.3, x: -20, y: 0, d: 0.6});
  bout("#pdK", @vidkr2-0.05, 8, 0.25);
  tl.to("#pdG", {x: -250, y: -10, scale: 0.62, transformOrigin: "405px 140px", duration: 0.7, ease: SP}, @vidkr2-0.05);
  arr("#pdW", @wfp-0.08, {s: 0.4, y: 30}); G.ripple("#pdWR", @wfp+0.25);
  tl.set("#gPd", {autoAlpha: 0}, @l0+0.9);""")


# ===========================================================================
# L · OVER: the WayForPay invoice — Соцінвойс, Продукти, paste, Зберегти
@beat
def l_form():
    form = ('<div class="fm hide" id="fmF" style="left:100px;top:140px;width:880px;height:1060px">'
            '<div class="abs fj" style="left:56px;top:44px">%s</div>'
            u'<div class="abs fT hide" id="fmT" style="left:56px;top:122px">Соцінвойс</div>'
            u'<div class="lbl fj" style="top:262px">НАЗВА</div><div class="inp fj" style="top:300px"><i style="width:340px"></i></div>'
            u'<div class="lbl fj" style="top:418px">СУМА</div><div class="inp fj" style="top:456px"><i style="width:180px"></i><b>%s</b></div>'
            u'<div class="abs fP hide" id="fmP" style="left:56px;top:584px">Продукти</div>'
            '<div class="dz hide" id="fmZ" style="left:56px;top:652px"><div class="dzs" id="fmZs" style="opacity:0"></div></div>'
            u'<div class="sv fj" id="fmS" style="left:56px;top:870px;width:768px;height:112px">Зберегти</div>'
            '<div class="ck" id="fmSr" style="left:440px;top:926px"></div>'
            '<div class="shc"><div class="sheen"></div></div></div>' % (wfp(44), uah(42, "rgba(23,20,28,0.55)", 2.6)))
    nmark = '<svg class="mkb" id="fmLn" viewBox="0 0 24 24"><use href="#i-notion" width="24" height="24" fill="#17141c"/></svg>'
    L.append('<div class="g full" id="gM">' + ground() + form
             + chip("fmL", 270, 814, 540, "pl", nmark + '<span>notion.site/guide</span>')
             + chip("fmPay", 270, 92, 540, "jl", link_svg() + u'<span>secure.wayforpay.com/…</span>')
             + '</div>')
    sfx("whoosh-short", T["l0"] - 0.02)
    sfx("click", T["posyl4"])
    sfx("click", T["zberih"] + 0.01)
    return js("""
  G.irisOpen("#gM", @l0, 690, 385, 0.8);
  drift1("#gM", @l0, @m0+0.5-@l0);
  gsap.set("#fmF", {transformOrigin: "590px 245px"});
  arr("#fmF", @l0+0.04, {s: 0.3, y: 0, d: 0.9});
  tl.fromTo("#fmF .fj", {autoAlpha: 0, y: 24}, {autoAlpha: 1, y: 0, duration: 0.45, ease: SP, stagger: 0.07}, @l0+0.3);
  arr("#fmT", @socinv-0.06, {s: 0.7, x: -30, y: 0, d: 0.6, blur: 8});
  arr(["#fmP", "#fmZ"], @produkty-0.06, {s: 0.8, y: 20, d: 0.6});
  tl.fromTo("#fmL", {autoAlpha: 0, y: -760, scale: 0.7}, {autoAlpha: 1, y: 0, scale: 1, duration: 0.62, ease: SP}, @posyl4-0.6);
  tl.to("#fmZs", {opacity: 1, duration: 0.25}, @posyl4-0.02);
  shn("#fmL .sheen", @posyl4+0.1);
  G.bump("#fmLn", @notion4);
  press("#fmS", @zberih);
  tl.fromTo("#fmSr", {scale: 0.6, autoAlpha: 0.95}, {scale: 2.6, autoAlpha: 0, duration: 0.7, ease: "power2.out", immediateRender: false}, @zberih+0.02);
  tl.fromTo("#fmPay", {autoAlpha: 0, y: 930, scale: 0.6}, {autoAlpha: 1, y: 0, scale: 1, duration: 0.6, ease: SP}, @zabyr-0.06);
  G.irisClose("#gM", @m0, 540, 136, 0.5);""")


# ===========================================================================
# M · the pay link goes into stories, the profile bio, Telegram — anywhere
@beat
def m_share():
    stories = ('<div class="st hide" id="nS" style="left:110px;top:236px;width:214px;height:380px">'
               '<i class="seg" style="left:14px;width:56px;background:#fff"></i>'
               '<i class="seg" style="left:78px;width:56px"></i><i class="seg" style="left:142px;width:56px"></i>'
               '<i style="left:14px;top:32px;width:36px;height:36px;border-radius:50%%;background:rgba(255,255,255,0.85)"></i>'
               '<i style="left:58px;top:44px;width:90px;height:10px;border-radius:5px;background:rgba(255,255,255,0.7)"></i>'
               '<div class="sstk hide" id="nSs" style="left:23px;top:168px;width:168px">%s<i style="width:84px"></i></div>'
               '</div>' % link_svg())
    igm = '<svg viewBox="0 0 24 24" style="position:absolute;left:300px;top:24px;width:32px;height:32px"><use href="#i-instagram" width="24" height="24" fill="#17141c"/></svg>'
    prof = ('<div class="pf hide" id="nP" style="left:360px;top:250px;width:352px;height:340px">'
            '<div class="av"><b>%s</b></div>%s'
            '<i style="left:160px;top:50px;width:40px;height:18px;background:rgba(23,20,28,0.72)"></i>'
            '<i style="left:222px;top:50px;width:40px;height:18px;background:rgba(23,20,28,0.72)"></i>'
            '<i style="left:284px;top:50px;width:40px;height:18px;background:rgba(23,20,28,0.72)"></i>'
            '<i style="left:156px;top:80px;width:48px;height:10px;background:rgba(23,20,28,0.25)"></i>'
            '<i style="left:218px;top:80px;width:48px;height:10px;background:rgba(23,20,28,0.25)"></i>'
            '<i style="left:280px;top:80px;width:48px;height:10px;background:rgba(23,20,28,0.25)"></i>'
            '<i style="left:24px;top:156px;width:170px;height:18px;background:rgba(23,20,28,0.78)"></i>'
            '<i style="left:24px;top:188px;width:280px;height:12px;background:rgba(23,20,28,0.2)"></i>'
            '<i style="left:24px;top:210px;width:220px;height:12px;background:rgba(23,20,28,0.2)"></i>'
            '<div class="pflk hide" id="nPl">%s<i></i></div>'
            '<div class="pfbt"></div>'
            '</div>' % (stroke("person"), igm, link_svg()))
    L.append('<div class="g full" id="gN">' + stories + prof
             + tile("nT", 190, 770, 290, "jelly", g.mark("telegram"))
             + '<div class="tbub hide" id="nTb" style="left:784px;top:496px">%s<i></i></div>' % link_svg()
             + '<div class="abs hide" id="nCr" style="left:270px;top:92px;width:540px;height:88px;border-radius:44px;'
               'border:4px solid rgba(255,255,255,0.8)"></div>'
             + chip("nC", 270, 92, 540, "jl", link_svg() + u'<span>secure.wayforpay.com/…</span>')
             + '</div>')
    sfx("pop", T["storis"] - 0.1, -2)
    sfx("pop", T["telegram"] - 0.05, -2)
    return js("""
  tl.set(["#gN", "#nC"], {autoAlpha: 1}, @m0);
  G.bump("#nC", @oplatu2); shn("#nC .sheen", @oplatu2);
  arr("#nS", @storis-0.12, {s: 0.5, y: 40, d: 0.75});
  tl.fromTo("#nSs", {autoAlpha: 0, y: -200, scale: 0.5}, {autoAlpha: 1, y: 0, scale: 1, duration: 0.5, ease: SP}, @storis+0.1);
  arr("#nP", @shapku-0.08, {s: 0.5, y: 40, d: 0.75});
  tl.fromTo("#nPl", {autoAlpha: 0, scaleX: 0.2}, {autoAlpha: 1, scaleX: 1, transformOrigin: "0% 50%", duration: 0.45, ease: SP}, @profiliu);
  arr("#nT", @telegram-0.06, {s: 0.4, y: 30}); G.ripple("#nTR", @telegram+0.25);
  arr("#nTb", @telegram+0.2, {s: 0.4, x: -20, y: -10, d: 0.55});
  tl.fromTo("#nCr", {scale: 1, autoAlpha: 0.85}, {scale: 1.3, autoAlpha: 0, duration: 0.8, ease: "power2.out", immediateRender: false}, @kudy);
  G.bump("#nS", @kudy+0.1); G.bump("#nP", @kudy+0.22); G.bump("#nT", @kudy+0.34);
  bout("#gN", @liudyna2-0.14, 10, 0.28);""")


# ===========================================================================
# N · a person pays (kaching), Gmail delivers the guide
@beat
def n_pay():
    cab = ('<svg class="cab abs" width="1080" height="700" viewBox="0 0 1080 700" style="left:0;top:0">'
           + cable("o1", "M314 439 C 400 404 476 404 556 439", packet=False) + '</svg>')
    gm = '<svg class="mkb" viewBox="0 0 24 24"><use href="#i-notion" width="24" height="24" fill="#17141c"/></svg>'
    note = ('<div class="dglass edge hide" id="eN" style="left:80px;top:96px;width:920px;height:200px">'
            '<div class="tw" style="left:32px;top:48px;width:104px;height:104px"><div class="pearl">%s</div></div>'
            '<div class="app">Gmail</div><div class="tm">%s</div>'
            '<i class="bar" style="left:168px;top:88px;width:330px;height:22px;background:rgba(255,255,255,0.85)"></i>'
            '<div class="att" id="eA" style="left:168px;top:126px">%s<i style="width:150px"></i>%s</div>'
            '<div class="shc"><div class="sheen"></div></div></div>'
            % (g.mark("gmail"), u"зараз", stroke("doc"), gm))
    L.append('<div class="g full" id="gE">' + cab
             + tile("eP", 190, 120, 344, "pearl", stroke("person"), extra_cls="circ")
             + wide("eW", 560, 364, 400, 150, wfp(58), r=44)
             + tile("eOk", 66, 924, 340, "jelly", stroke("check"), extra_cls="circ", ring=False)
             + tile("eM", 76, 262, 330, "pearl", g.mark("gmail"), extra_cls="circ", ring=False)
             + '<div class="tw circ hide" id="eK0" style="left:262px;top:391px;width:96px;height:96px"><div class="jelly">'
               + uah(56, "#fff", 2.6) + '</div></div>'
             + note + '</div>')
    sfx("kaching", T["platyt"] + 0.36)
    sfx("notification", T["otrymuie2"] - 0.15, -1)
    return js("""
  tl.set("#gE", {autoAlpha: 1}, @liudyna2-0.1);
  arr("#eP", @liudyna2-0.06, {s: 0.4, y: 30});
  arr("#eW", @liudyna2+0.04, {s: 0.6, y: 30});
  tl.set(["#o1T", "#o1K"], {autoAlpha: 1}, @liudyna2+0.1);
  draw2("o1T", @liudyna2+0.1, 0.35); draw2("o1K", @liudyna2+0.1, 0.35);
  tl.fromTo("#eK0", {autoAlpha: 0, scale: 0.4}, {autoAlpha: 1, scale: 1, duration: 0.25, ease: "power2.out"}, @platyt-0.08);
  tl.to("#eK0", {x: 250, duration: 0.42, ease: "power2.inOut"}, @platyt-0.02);
  tl.to("#eK0", {keyframes: {y: [0, -38, 0]}, duration: 0.42, ease: "none"}, @platyt-0.02);
  tl.to("#eK0", {scale: 0.3, autoAlpha: 0, duration: 0.16, ease: "power2.in"}, @platyt+0.38);
  G.bump("#eW", @platyt+0.4); G.ripple("#eWR", @platyt+0.4);
  arr("#eOk", @platyt+0.45, {s: 0.3, y: 0, d: 0.5});
  tl.fromTo("#eN", {autoAlpha: 0, y: -300, scale: 0.92}, {autoAlpha: 1, y: 0, scale: 1, duration: 0.9, ease: SOFT}, @otrymuie2-0.22);
  G.haptic("#eN", @haid4);
  shn("#eN .sheen", @haid4);
  arr("#eM", @poshtu-0.06, {s: 0.3, y: 0, d: 0.5}); G.bump("#eP", @poshtu);
  bout("#gE", @naidovsha-0.12, 10, 0.28);""")


# ===========================================================================
# O · the longest part is not technical: a short bar and a long one
@beat
def o_bars():
    pages = "".join('<div class="pgx" id="oPg%d" style="left:47px;top:242px"></div>' % i for i in range(3))
    shelf = ('<div class="shelf edge hide" id="oS" style="left:70px;top:150px;width:940px;height:440px">'
             + pages
             + tile("oG", 130, 40, 50, "pearl", stroke("gear"), ring=False)
             + tile("oD", 130, 40, 250, "jelly", stroke("doc"))
             + '<div class="trk" style="left:206px;top:93px;width:690px"></div>'
             + '<div class="fil" id="oF1" style="left:206px;top:93px;width:690px"></div>'
             + '<div class="trk" style="left:206px;top:293px;width:690px"></div>'
             + '<div class="fil hot" id="oF2" style="left:206px;top:293px;width:690px"></div>'
             + u'<div class="dch hide" id="oC" style="left:206px;top:206px;width:160px"><span id="oCt">15 хв</span>'
             + stroke("calendar", "sk ink", "position:absolute;left:58px;top:11px;width:44px;height:44px;opacity:0") + '</div>'
             + '</div>')
    L.append('<div class="g full" id="gO">' + shelf + '</div>')
    sfx("click-soft", T["tekhn"], -2)
    sfx("click-soft", T["p15b"] - 0.04, -1)
    rot = [(-15, -30, -8), (-8, -18, -4), (-3, -8, -1)]
    pg = "\n".join('  tl.fromTo("#oPg%d", {rotation: 0, x: 0, y: 0}, {rotation: %d, x: %d, y: %d, duration: 0.55, ease: SP, '
                   'immediateRender: false}, %.3f);' % (i, r, x, y, T["inform"] - 0.3 + i * 0.08)
                   for i, (r, x, y) in enumerate(rot))
    return js("""
  tl.set("#gO", {autoAlpha: 1}, @naidovsha-0.1);
  arr("#oS", @naidovsha-0.06, {s: 0.85, y: 30});
  G.inner("#oG", @naidovsha); G.inner("#oD", @naidovsha+0.1);
  gsap.set(["#oF1", "#oF2"], {scaleX: 0, transformOrigin: "0% 50%"});
  gsap.set(".pgx", {transformOrigin: "50% 100%"});
  tl.to("#oF1", {scaleX: 0.17, duration: 0.6, ease: SP}, @tekhn-0.05);
  tl.to(["#oF1", "#oG"], {autoAlpha: 0.5, duration: 0.4}, @robota);
  tl.to("#oF2", {scaleX: 0.97, duration: 0.95, ease: "power2.out"}, @liudiam-0.3);
  G.bump("#oD", @haidi); shn("#oD .sheen", @haidi);
  arr("#oC", @p15b-0.06, {s: 0.3, y: 20, d: 0.55});
  tl.to("#oC", {x: 530, duration: 0.5, ease: "power2.inOut"}, @kilka-0.12);
  tl.to("#oCt", {autoAlpha: 0, duration: 0.15}, @dniv-0.05);
  tl.fromTo("#oC .sk", {opacity: 0, scale: 0.4}, {opacity: 1, scale: 1, duration: 0.45, ease: POP, immediateRender: false}, @dniv+0.05);
{{pg}}
  tl.set("#gO", {autoAlpha: 0}, @p0+0.9);""").replace("{{pg}}", pg)


# ===========================================================================
# P · OVER: design, payment, delivery — one lap of the same stopwatch, 1:00
@beat
def p_minute():
    cab = ('<svg class="cab abs" width="1080" height="1000" viewBox="0 0 1080 1000" style="left:0;top:0">'
           + cable("q1", "M326 490 L394 490", packet=False) + cable("q2", "M686 490 L754 490", packet=False) + '</svg>')
    L.append('<div class="g full" id="gP">' + ground() + stopwatch("q") + cab
             + tile("qN", 220, 110, 380, "pearl", g.mark("notion"))
             + wide("qW", 390, 380, 300, 220, wfp(50), r=50)
             + tile("qG", 220, 750, 380, "pearl", g.mark("gmail"))
             + '<div class="bigt hide" id="qD" style="top:715px;height:250px;line-height:250px;font-size:250px">1:00</div>'
             + '</div>')
    sfx("whoosh-short", T["p0"] - 0.02)
    sfx("pop", T["dyzain2"] - 0.05, -2)
    sfx("click", T["khvylynu2"] - 0.04)
    return js("""
  G.irisOpen("#gP", @p0, 175, 465, 0.85);
  drift1("#gP", @p0, @yakshcho3+0.5-@p0);
  arr("#qN", @dyzain2-0.06, {s: 0.4, y: 30}); G.ripple("#qNR", @dyzain2+0.25);
  arr("#qW", @oplata-0.06, {s: 0.4, y: 30}); G.ripple("#qWR", @oplata+0.25);
  arr("#qG", @dostavka-0.06, {s: 0.4, y: 30}); G.ripple("#qGR", @dostavka+0.25);
  tl.set(["#q1T", "#q1K", "#q2T", "#q2K"], {autoAlpha: 1}, @dostavka+0.15);
  draw2("q1T", @dostavka+0.15, 0.3); draw2("q1K", @dostavka+0.15, 0.3);
  draw2("q2T", @dostavka+0.25, 0.3); draw2("q2K", @dostavka+0.25, 0.3);
  press("#qCr", @zabyraie);
  tl.set("#qArc", {opacity: 1}, @zabyraie);
  gsap.set("#qArc", {strokeDasharray: "@rc @rc2", strokeDashoffset: @rc3});
  tl.fromTo("#qArc", {strokeDashoffset: @rc3}, {strokeDashoffset: 0, duration: @khvylynu2-@zabyraie, ease: "none", immediateRender: false}, @zabyraie);
  bin("#qD", @khvylynu2-0.06, 16, 0.3);
  tl.fromTo("#qD", {scale: 1.5}, {scale: 1, duration: 0.6, ease: POP, immediateRender: false}, @khvylynu2-0.06);
  G.irisClose("#gP", @yakshcho3-0.08, 540, 375, 0.5);""", rc=RING_C, rc2=RING_C + 40, rc3=RING_C + 3)


# ===========================================================================
# Q · Стежити
@beat
def q_follow():
    L.append('<div class="g full" id="gQ"><div class="fl hide" id="fl" style="left:190px;top:300px;width:700px;height:150px">'
             '<div class="tw circ" style="left:28px;top:27px;width:96px;height:96px"><div class="jelly">%s</div></div>'
             u'<div class="t" id="flT">Стежити</div>'
             '<div class="on" id="flOn"><div class="tw circ" style="left:28px;top:27px;width:96px;height:96px">'
             u'<div class="pearl">%s</div></div><div class="t">Ви стежите</div></div>'
             '<div class="ck" id="ck4" style="left:470px;top:75px"></div>'
             '<div class="shc"><div class="sheen"></div></div></div></div>'
             % (g.mark("instagram"), stroke("check")))
    sfx("click", T["pidpysh"] + 0.02)
    return js("""
  tl.set("#gQ", {autoAlpha: 1}, @yakshcho3-0.1);
  arr("#fl", @yakshcho3-0.02, {s: 0.6, y: 40});
  tl.to("#fl", {scale: 0.95, duration: 0.09, ease: "power2.out"}, @pidpysh);
  tl.to("#fl", {scale: 1, duration: 0.45, ease: SP}, @pidpysh+0.09);
  tl.fromTo("#flOn", {autoAlpha: 0}, {autoAlpha: 1, duration: 0.2}, @pidpysh+0.04);
  tl.set("#flT", {autoAlpha: 0}, @pidpysh+0.05);
  tl.fromTo("#ck4", {scale: 0.3, autoAlpha: 0.95}, {scale: 2.4, autoAlpha: 0, duration: 0.7, ease: "power2.out", immediateRender: false}, @pidpysh+0.02);
  shn("#fl .sheen", @pidpysh+0.15);""")


# ---------------------------------------------------------------------------
HEAD_JS = r"""
  var G = helpers(tl);
  var SWING = spring(0.16, 12);
  function bin(sel, t, b, d) { d = d || 0.38; G.blurIn(sel, t, b || 12, d); tl.set(sel, {filter: "none"}, t + d + 0.01); }
  function bout(sel, t, b, d) { d = d || 0.32; G.blurOut(sel, t, b || 10, d); tl.set(sel, {filter: "none"}, t + d + 0.01); }
  function arr(sel, t, o) {
    o = o || {};
    bin(sel, t, o.blur || 12, 0.36);
    tl.fromTo(sel, {scale: o.s == null ? 0.5 : o.s, x: o.x || 0, y: o.y == null ? 34 : o.y},
              {scale: 1, x: 0, y: 0, duration: o.d || 0.85, ease: o.ease || POP}, t);
  }
  function bmp(sel, t, s) { s = s || 1; tl.to(sel, {scale: s * 1.07, duration: 0.1, ease: "power2.out"}, t);
    tl.to(sel, {scale: s, duration: 0.45, ease: SP}, t + 0.1); }
  function press(sel, t) { tl.to(sel, {scale: 0.94, y: 8, duration: 0.09, ease: "power2.out"}, t);
    tl.to(sel, {scale: 1, y: 0, duration: 0.42, ease: SP}, t + 0.09); }
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


def clock_js():
    """Typing (the DM, the prompt) and the live waveform, all from one clock so any frame renders cold."""
    typ = [
        {"el": "hT", "txt": u"КОПІ", "t0": T["kopi"], "t1": T["kopi"] + 0.34, "tc": T["i_ya"] + 0.06},
        {"el": "iT", "txt": PROMPT, "t0": T["zrobyty"] - 0.02, "t1": T["notion3"] + 0.05, "tc": 1e9},
    ]
    w0, w1 = T["nahovor"] - 0.02, T["rozkaz"] - 0.15
    return r"""
  var CLK = {t: 0}, TYP = %s, W0 = %.3f, W1 = %.3f;
  TYP.forEach(function (o) { o.node = document.getElementById(o.el); o.cur = -1; });
  var WB = Array.prototype.slice.call(document.querySelectorAll(".wb")), WCUR = -1;
  function paintAll() {
    var t = CLK.t;
    TYP.forEach(function (o) {
      var n = (t <= o.t0 || t >= o.tc) ? 0 : t >= o.t1 ? o.txt.length : Math.round(o.txt.length * (t - o.t0) / (o.t1 - o.t0));
      if (n !== o.cur) { o.cur = n; o.node.textContent = o.txt.slice(0, n); }
    });
    var on = t > W0 && t < W1, key = on ? Math.round(t * 30) : -2;
    if (key === WCUR) return;
    WCUR = key;
    WB.forEach(function (b, i) {
      var v = 0.14;
      if (on) {
        var env = Math.min(1, (t - W0) / 0.25, (W1 - t) / 0.25);
        var gate = 0.72 + 0.28 * Math.sin(t * 2.3 + 0.6);
        var c = 1 - Math.abs(i - (WB.length - 1) / 2) / WB.length;
        var a = Math.pow(Math.abs(Math.sin(t * 7.3 + i * 0.9) * Math.sin(t * 3.1 + i * 0.37 + 1.0)), 0.6);
        v = 0.14 + 0.86 * env * gate * (0.3 + 0.7 * a) * (0.55 + 0.45 * c);
      }
      b.style.transform = "scaleY(" + v.toFixed(3) + ")";
    });
  }
  tl.fromTo(CLK, {t: 0}, {t: %.3f, duration: %.3f, ease: "none", onUpdate: paintAll}, 0);""" % (
        json.dumps(typ, ensure_ascii=False), w0, w1, DUR, DUR)


# captions that would repeat the graphic's own words (STYLE.md §2b.1)
def span_words(a, b):
    return (round(a - 0.02, 3), round(b, 3), "")


BLACKOUT = [
    span_words(T["p15"], E(u"хвилин", 11.77)),               # the stopwatch says 15:00
    span_words(T["pershyi"], E(u"хвилину", 13.74)),          # КРОК 1 · 1 хв
    span_words(T["druhyi"], E(u"хвилина", 17.47)),           # КРОК 2 · 1 хв
    span_words(T["skil"], E(u"скіл", 32.38)),                # SKILL.md
    span_words(T["kopi"], E(u"КОПІ", 36.28)),                # typed in the DM
    span_words(T["zrobyty"], E(u"Notion", 44.0)),            # the prompt types it
    span_words(T["bezkosht"], E(u"безкоштовний", 46.32)),    # БЕЗКОШТОВНО
    span_words(T["ye"], E(u"крок", 53.46)),                  # +1 КРОК
    span_words(T["wfp"], E(u"Way4Pay", 54.68)),              # the wordmark
    span_words(T["socinv"], E(u"соцінвойс", 55.93)),         # the form title
    span_words(T["produkty"], E(u"продукти", 57.17)),        # the section label
    span_words(T["zberih"], E(u"Зберігаєш", 59.83)),         # Зберегти
    span_words(T["p15b"], E(u"хвилин", 75.47)),              # 15 хв
    span_words(T["khvylynu2"], E(u"хвилину", 83.08)),        # 1:00
]


def check_no_paint():
    """No beat on screen inside a closeup, no sound cue on one."""
    a1, b1 = NP1
    a2, b2 = NP2
    assert T["aend"] + 0.29 < a1, "hook runs into the first closeup"
    assert T["b0"] >= b1, "shelf arrives inside the first closeup"
    assert T["fend"] + 0.29 < a2, "step 3 runs into the second closeup"
    assert T["dali"] - 0.06 + 0.28 < a2
    assert T["g0"] >= b2, "skill takeover opens inside the second closeup"
    for c in SFX:
        for a, b in NO_PAINT:
            assert not (a - 0.05 <= c["t"] <= b), ("sfx on a closeup", c)


def main():
    gj = []
    for fn in BEATS:
        j = fn()
        gj.append("  /* %s */" % fn.__name__)
        gj.append(j.rstrip())
    check_no_paint()
    push = ["#vid"]
    head = [g.js(), HEAD_JS, clock_js(),
            '  gsap.set(%s, {transformOrigin: "540px 900px"});' % json.dumps(push),
            '  tl.fromTo(%s, {scale: 1}, {scale: 1.045, duration: %.3f, ease: "none"}, 0);' % (json.dumps(push), DUR)]
    extra = ('<linearGradient id="gpk" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffe0ea"/>'
             '<stop offset="1" stop-color="#ff5c8f"/></linearGradient>')
    doc = k.document(
        title=u"Reel 22 — guide in 15 minutes",
        plate="assets/base.mp4",
        gfx_html=g.defs(extra) + "\n" + "\n".join(L),
        gfx_js="\n".join(head + gj),
        caps=CAPS,
        blackout=BLACKOUT,
    )
    io.open(os.path.join(HERE, "index.html"), "w", encoding="utf-8").write(doc)
    SFX.sort(key=lambda c: c["t"])
    io.open(os.path.join(HERE, "sfx.json"), "w", encoding="utf-8").write(json.dumps(SFX, indent=1))
    print("index.html  DUR %.3f (%d frames)  %d captions, %d beats, %d sfx cues (%.2f/s)" % (DUR, PLATE_FRAMES, len(CAPS), len(BEATS), len(SFX), len(SFX) / DUR))


main()
