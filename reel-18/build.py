# -*- coding: utf-8 -*-
"""Reel 18 — «Знаєш, коли на сайті просто висить кнопка». Telegram Business:
a chat link with a pre-typed message, then a bot triggered by that message.

Variant B, refined glass (STYLE.md §0, tools/glass.py). Structure follows
reel-15/build.py: kit document, her plate, captions on the plaque, one
`.g full` container per graphic, blocks grouped per chain so tools/review.py
reads each handoff as one movement.

The one object is **the chat the visitor lands in**: bare early (an empty
chat, a blinking cursor, a manager who reads you an hour later), then opened
from the site button with the message already typed, then answered by a bot
before the manager has finished her coffee.

The chain:
    a glass site with a «Написати в Telegram» button above her head, pressed
    on «Телеграм» -> the iris opens out of the button into the empty chat ->
    typing, deleting, «Добрий день!» sent, read an hour later -> the iris
    closes onto a row of ten visitors, five leave -> ×2 -> the Telegram tile
    earns the Premium star -> the tile opens into **her screen recording, full
    frame, and she shrinks into the bottom-right corner as if shot on a
    greenscreen** (her explicit ask): Settings, Telegram Business, Links to
    Chat, create, type, save, copy, each item lit and tapped on its word ->
    the copied link lifts off the recording as a glass chip, she grows back,
    the recording closes, the chip drops into the site button -> the button
    is tapped and the chat opens with «Привіт! Хочу на Мадейру!» already typed
    -> sent, ✓✓ -> that bubble becomes a trigger wired to a bot on her own
    account -> the travel-agency chat: «вітаю, мене цікавить подорож на
    Мадейру», the bot answers at once with the trip card -> the manager is
    still «був(ла) нещодавно» over a coffee -> Follow.

Her cut: two shots (0-45.07, 45.07-70.64), a plain jump cut, no inserts and
no pull-outs (work/r18/shots, pullout-spans.json) — so nothing is NO_PAINT.

The recording (work/media/r18/telegram-business.mp4) is re-timed and blurred
by screen.py: see its docstring for what is blurred and why.

usage: python build.py
"""
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))
sys.path.insert(0, HERE)
from kit import Kit  # noqa: E402
from glass import Glass  # noqa: E402
import screen as SCR  # noqa: E402

DUR = 70.583           # 2118 plate frames / 30 (work/w40-queue2.log)
FPS = 30
k = Kit(width=1080, height=1920, fps=FPS, duration=DUR)
g = Glass()
k.css(g.css())

BEATS = []


def beat(fn):
    BEATS.append(fn)
    return fn


# ---------------------------------------------------------------------------
# NO-PAINT ZONES (STYLE.md §4a). Two shots, cut at 45.07 on «Це вже трошки»
# at the same framing — an ordinary jump cut, not an insert. No pull-outs.
NO_PAINT = []

# ---------------------------------------------------------------------------
# Words. Script spelling on her timing (work/r18/captions.json after
# tools/patchcaps.py with work/r18/caption-patch.json): «Створюєш» (whisper:
# «Свориш»), «турагенція, людина» («турагентія. Людмила»), «надсилати» («не
# цилати»), «доп'є» («доп'я»), a stray «–» dropped. Kept as she said it:
# «просто копійки», «його лише відправити», «в тебе, не знаю, турагенція».
CAPS = k.load_captions(os.path.join(ROOT, "work", "r18", "captions.json"))
for _a, _b in zip(CAPS, CAPS[1:]):
    _a["e"] = round(max(_a["s"] + 0.10, min(_b["s"] - 0.085, _a["s"] + 1.2)), 3)
    if _a["e"] > _b["s"]:
        _a["e"] = _b["s"]
CAPS[-1]["e"] = round(min(CAPS[-1]["e"], DUR - 0.05), 3)


def _n(s):
    return "".join(ch for ch in s.lower() if ch.isalnum() or ch in "+'")


def at(word, near):
    hits = [c for c in CAPS if _n(word) in [_n(x) for x in c["w"].split()]]
    c = min(hits, key=lambda c: abs(c["s"] - near))
    assert abs(c["s"] - near) < 1.0, (word, near, c["s"])
    return c


def S(w, near):
    return at(w, near)["s"]


def E(w, near):
    return at(w, near)["e"]


T = {
    # b01-b04
    "sayti": S(u"сайті", 0.96), "knopka": S(u"кнопка", 1.78), "napys": S(u"написати", 2.20),
    "tg1": S(u"Телеграм", 2.80), "tg1_e": E(u"Телеграм", 2.80), "zakh": S(u"заходить", 3.74),
    "chat1": S(u"чат", 4.22), "men1": S(u"менеджером", 4.44), "men1_e": E(u"менеджером", 4.44),
    "pustota": S(u"пустота", 5.18), "vona": S(u"Вона", 5.88), "dumaye": S(u"думає", 6.54),
    "pochaty": S(u"почати", 7.10), "men2": S(u"менеджер", 7.98), "vidp": S(u"відповідає", 8.38),
    "cherez": S(u"через", 8.82), "hodynu": S(u"годину", 9.06), "hodynu_e": E(u"годину", 9.06),
    # b05-b07
    "polov": S(u"половина", 9.62), "lyudey": S(u"людей", 10.06), "zakr": S(u"закриває", 10.76),
    "chat2": S(u"чат", 11.22), "dopys": S(u"дописавши", 11.50), "dopys_e": E(u"дописавши", 11.50),
    "sposib": S(u"спосіб", 13.66), "prysk": S(u"прискорити", 14.66), "dva": S(u"два", 16.12),
    "razy_e": E(u"рази", 16.28), "potr": S(u"потрібна", 17.18), "odna": S(u"одна", 18.46),
    "tg2": S("Telegram", 19.30), "prem": S("Premium", 19.84), "prem_e": E("Premium", 19.84),
    "kosht": S(u"коштує", 20.64), "kop": S(u"копійки", 21.58), "kop_e": E(u"копійки", 21.58),
    # b08-b12
    "zakhodysh": S(u"Заходиш", 22.16), "nalasht": S(u"налаштування", 22.54),
    "akauntu": S(u"акаунту", 23.36), "skrol": S(u"скролиш", 23.96), "vnyz": S(u"вниз", 24.36),
    "znakh": S(u"знаходиш", 25.06), "tg3": S("Telegram", 25.60), "biznes": S(u"Бізнес", 26.10),
    "vnomu": S(u"ньому", 26.90), "posyl1": S(u"посилання", 27.20), "rozmovu": S(u"розмову", 28.02),
    "stvor": S(u"Створюєш", 28.66), "nove": S(u"нове", 29.10), "odrazu": S(u"одразу", 29.96),
    "propys": S(u"прописуєш", 30.26), "typu": S(u"типу", 32.68), "zber": S(u"Зберігаєш", 34.60),
    "beresh": S(u"береш", 35.30), "vstavl": S(u"вставляєш", 36.36), "na_sayt": S(u"на", 37.00),
    "sayt": S(u"сайт", 37.18), "koly": S(u"коли", 38.08), "tytsyaye": S(u"тицяє", 38.68),
    "knopku": S(u"кнопку", 39.16), "vidkr": S(u"відкривається", 39.82), "pustyi": S(u"пустий", 40.66),
    "vzhe": S(u"вже", 41.68), "napysane": S(u"написане", 42.08), "zalysh": S(u"залишається", 43.34),
    "vidpr": S(u"відправити", 44.62), "vidpr_e": E(u"відправити", 44.62),
    # b14
    "ale": S(u"Але", 47.30), "druhyi": S(u"другий", 47.60), "tsikav": S(u"цікавіший", 48.16),
    "tse2": S(u"Це", 49.10), "povid2": S(u"повідомлення", 49.58), "pidkl": S(u"підключити", 50.36),
    "tryger": S(u"тригер", 51.20), "chatbota": S(u"чат-бота", 51.78), "svoyemu": S(u"своєму", 52.46),
    "person": S(u"персональному", 52.96), "akaunti_e": E(u"акаунті", 53.70),
    # b15-b16
    "tobto": S(u"Тобто", 54.62), "umovno": S(u"умовно", 54.96), "turag": S(u"турагенція", 56.06),
    "turag_e": E(u"турагенція", 56.06), "lyudyna": S(u"людина", 56.90), "pyshe": S(u"пише", 57.26),
    "vitayu": S(u"вітаю", 57.52), "mad": S(u"Мадейру", 59.04), "mad_e": E(u"Мадейру", 59.04),
    "bot": S(u"бот", 59.96), "rozpiz": S(u"розпізнає", 60.66), "pochyn": S(u"починає", 62.52),
    "nadsyl": S(u"надсилати", 62.92), "detali": S(u"деталі", 63.66), "podorozh": S(u"подорож", 64.22),
    "podorozh_e": E(u"подорож", 64.22),
    # b17-b18
    "poky": S(u"поки", 64.92), "men3": S(u"менеджер", 65.30), "dopye": S(u"доп'є", 65.92),
    "kavu": S(u"каву", 66.26), "pidiyde": S(u"підійде", 66.62), "telef": S(u"телефону", 67.06),
    "yakshcho": S(u"Якщо", 68.12), "korysno": S(u"корисно", 68.48), "obov": S(u"обов'язково", 69.46),
    "pidpys": S(u"підпишись", 70.04),
    "dur": DUR,
}


def js(src, **extra):
    """`@name` -> a literal time. Literals, not variables, because
    tools/review.py reads the timeline off the generated numbers."""
    vals = dict(T)
    vals.update(extra)

    def rep(m):
        v = vals[m.group(1)]
        return "%.3f" % v if isinstance(v, (int, float)) else str(v)
    return re.sub(r"@(\w+)", rep, src)


def fill(s, **kw):
    for key, v in kw.items():
        s = s.replace("{{%s}}" % key, v if isinstance(v, str) else str(v))
    assert "{{" not in s, s[s.index("{{"):s.index("{{") + 40]
    return s


# ---------------------------------------------------------------------------
# Glyphs: strokes and fills, never emoji (§5a.11).
GL = {
    "back": '<path d="M15 5l-7 7 7 7"/>',
    "clip": '<path d="M20 11.4l-8 8a5 5 0 0 1-7.1-7.1l8.4-8.4a3.3 3.3 0 0 1 4.7 4.7l-8.2 8.2a1.6 1.6 0 0 1-2.3-2.3l7.5-7.5"/>',
    "mic": '<rect x="9" y="3" width="6" height="11" rx="3"/><path d="M5.5 11a6.5 6.5 0 0 0 13 0M12 17.5V21"/>',
    "clock": '<circle cx="12" cy="12" r="9"/>',
    "cup": '<path d="M4.5 9.5h12v4.2a5.3 5.3 0 0 1-5.3 5.3h-1.4a5.3 5.3 0 0 1-5.3-5.3z"/>'
           '<path d="M16.5 10.8h1.3a2.6 2.6 0 0 1 0 5.2h-1.6"/><path d="M3.5 21.2h14"/>',
    "link": '<path d="M10.2 13.8a4 4 0 0 0 5.7 0l3.4-3.4a4 4 0 0 0-5.7-5.7l-1.2 1.2"/>'
            '<path d="M13.8 10.2a4 4 0 0 0-5.7 0l-3.4 3.4a4 4 0 0 0 5.7 5.7l1.2-1.2"/>',
    "empty": '<path d="M4 6.5A2.5 2.5 0 0 1 6.5 4h11A2.5 2.5 0 0 1 20 6.5v8a2.5 2.5 0 0 1-2.5 2.5H10l-4.5 3.5V17A2.5 2.5 0 0 1 4 14.5z"/>',
}
FILLS = {
    "send": "M3.4 20.4l17.4-7.5a1 1 0 0 0 0-1.8L3.4 3.6a.9.9 0 0 0-1.3 1l1.6 6.2 9.3 1.2-9.3 1.2-1.6 6.2a.9.9 0 0 0 1.3 1z",
    "bolt": "M13.6 2.2L4.6 13.6h6.1l-1.3 8.2 9-11.5h-6.2z",
    "star": "M12 2.4l2.9 6 6.5.8-4.8 4.5 1.2 6.5L12 17l-5.8 3.2 1.2-6.5L2.6 9.2l6.5-.8z",
    "person": "M12 4.2a4.3 4.3 0 1 1 0 8.6 4.3 4.3 0 0 1 0-8.6zM4.2 20.6c1.1-4.4 4.3-6.6 7.8-6.6s6.7 2.2 7.8 6.6z",
    "plane": "M21.6 15.6v-2l-8.2-5.2V3.2a1.5 1.5 0 0 0-3 0v5.2l-8.2 5.2v2l8.2-2.6v5.3l-2.1 1.6v1.5l3.6-1 3.6 1v-1.5l-2.1-1.6V13z",
    "bot": ("M12 1.6a1.7 1.7 0 0 1 .85 3.17V6.4h4.35a3.4 3.4 0 0 1 3.4 3.4v7.2a3.4 3.4 0 0 1-3.4 3.4"
            "H6.8a3.4 3.4 0 0 1-3.4-3.4V9.8a3.4 3.4 0 0 1 3.4-3.4h4.35V4.77A1.7 1.7 0 0 1 12 1.6z"
            "M8.9 11.3a1.75 1.75 0 1 0 0 3.5 1.75 1.75 0 0 0 0-3.5zm6.2 0a1.75 1.75 0 1 0 0 3.5"
            " 1.75 1.75 0 0 0 0-3.5zM.8 11.4h1.6v4.6H.8zm20.8 0h1.6v4.6h-1.6z"),
}
TICK1 = "M2 9.6l4.1 4.1L14.4 5"
TICK2 = "M8.6 13.7L17 5"


def gl(name, cls="gy", extra=""):
    return '<svg class="%s" viewBox="0 0 24 24"%s>%s</svg>' % (cls, extra, GL[name])


def fl(name, cls="gf"):
    return '<svg class="%s" viewBox="0 0 24 24"><path fill-rule="evenodd" d="%s"/></svg>' % (cls, FILLS[name])


def ticks(tid):
    return ('<svg class="tk2" viewBox="0 0 20 18"><path d="%s"/><path class="t2" id="%s" d="%s"/></svg>'
            % (TICK1, tid, TICK2))


def tap(tid, x, y):
    return '<div class="tap" id="%s" style="left:%dpx;top:%dpx"><i class="td"></i><i class="tr"></i></div>' % (tid, x, y)


# ---------------------------------------------------------------------------
k.css(u"""
.abs, .cx { position: absolute; }
.hide { opacity: 0; visibility: hidden; }
.ctr { position: absolute; left: 0; width: 1080px; display: flex; justify-content: center; }
.gy { fill: none; stroke: currentColor; stroke-width: 2.2; stroke-linecap: round; stroke-linejoin: round; }
.gf { fill: currentColor; }
/* the takeover's three light pools as one element (reel 15) */
.aurs { position: absolute; left: -700px; top: -700px; width: 2480px; height: 3320px; pointer-events: none;
  background:
    radial-gradient(circle 526px at 1560px 880px, rgba(255,110,156,0.50), rgba(255,110,156,0)),
    radial-gradient(circle 634px at 760px 2360px, rgba(222,32,74,0.55), rgba(222,32,74,0)),
    radial-gradient(circle 382px at 1480px 1910px, rgba(255,198,214,0.20), rgba(255,198,214,0)); }
.tkx { position: absolute; inset: 0; overflow: hidden; }
/* small dark chips without a backdrop blur: the budget (STYLE.md §5a.1) */
.dchip { position: absolute; color: #fff; border-radius: 999px;
  background: linear-gradient(160deg, rgba(66,24,36,0.88) 0%, rgba(28,11,17,0.84) 100%);
  box-shadow: inset 0 1.5px 1px rgba(255,255,255,0.30), inset 0 -16px 30px -16px rgba(255,255,255,0.14),
              0 30px 60px -26px rgba(10,0,4,0.6); }

/* ---- a tap: a pink dot and a ring, the Android "show taps" made ours ---- */
.tap { position: absolute; width: 0; height: 0; }
.tap i { position: absolute; display: block; border-radius: 50%; opacity: 0; visibility: hidden; }
.tap .td { left: -46px; top: -46px; width: 92px; height: 92px;
  background: radial-gradient(circle, rgba(255,110,156,0.75) 0%, rgba(255,110,156,0.35) 60%, rgba(255,110,156,0) 72%); }
.tap .tr { left: -64px; top: -64px; width: 128px; height: 128px; border: 6px solid #ff6e9c;
  box-shadow: 0 0 22px rgba(255,110,156,0.6); }

/* ---- the site: a glass browser window with the button ---- */
.site { position: absolute; left: 100px; top: 92px; width: 880px; height: 420px; }
.site .dot { position: absolute; top: 31px; width: 16px; height: 16px; border-radius: 50%; background: rgba(255,255,255,0.55); }
.site .url { position: absolute; left: 130px; top: 22px; width: 620px; height: 34px; border-radius: 17px;
  background: rgba(255,255,255,0.16); }
.site .hr { position: absolute; left: 0; right: 0; top: 78px; height: 2px; background: rgba(255,255,255,0.16); }
.site .hd { position: absolute; left: 48px; top: 116px; width: 430px; height: 46px; border-radius: 14px;
  background: rgba(255,255,255,0.90); }
.site .br { position: absolute; left: 48px; height: 22px; border-radius: 11px; background: rgba(255,255,255,0.42); }
.site .im { position: absolute; left: 600px; top: 112px; width: 232px; height: 172px; border-radius: 34px; overflow: hidden;
  background: linear-gradient(165deg, rgba(255,150,185,0.70) 0%, rgba(196,20,52,0.60) 100%);
  box-shadow: inset 0 2px 1px rgba(255,255,255,0.5); }
.site .im svg { position: absolute; left: 0; top: 0; width: 232px; height: 172px; }
.sbtn { position: absolute; left: 48px; top: 290px; width: 480px; height: 96px; }
.sbtn .jelly { border-radius: 48px; gap: 18px; color: #fff; font-size: 33px; font-weight: 700; letter-spacing: -0.01em; }
.sbtn .jelly .mk { width: 46px; height: 46px; fill: #fff; }
.sbtn .jelly span { position: relative; z-index: 1; }
.sbtn .lk { position: absolute; right: -14px; top: -14px; width: 52px; height: 52px; border-radius: 50%;
  background: linear-gradient(160deg, #ffffff 0%, #ffe3ec 100%); color: #b4122f; z-index: 2;
  display: flex; align-items: center; justify-content: center; box-shadow: 0 10px 20px -8px rgba(60,4,18,0.6); }
.sbtn .lk svg { width: 32px; height: 32px; stroke-width: 2.6; }

/* ---- the chat: a white Telegram sheet on the burgundy ground ---- */
.chw { position: absolute; left: 100px; top: 136px; width: 880px; height: 1090px; }
.chat { position: absolute; inset: 0; }
.chh { position: absolute; left: 0; top: 0; width: 880px; height: 150px; }
.chh .bk { position: absolute; left: 30px; top: 51px; width: 48px; height: 48px; color: #b4122f; stroke-width: 2.6; }
.chh .av { position: absolute; left: 96px; top: 29px; width: 92px; height: 92px; border-radius: 50%; overflow: hidden;
  background: linear-gradient(165deg, #ff7aa4 0%, #e0204b 50%, #8d0d24 100%); color: #fff;
  display: flex; align-items: center; justify-content: center; font-size: 42px; font-weight: 700;
  box-shadow: inset 0 2px 1px rgba(255,255,255,0.45); }
.chh .av .gf { width: 50px; height: 50px; }
.chh .nm { left: 214px; top: 34px; font-size: 38px; font-weight: 700; letter-spacing: -0.015em; }
.chh .st { left: 214px; top: 84px; font-size: 26px; font-weight: 500; color: rgba(23,20,28,0.46); white-space: nowrap; }
.chh .st b { font-weight: 700; color: #d0194a; }
.chh .ln { position: absolute; left: 0; width: 880px; top: 149px; height: 2px; background: rgba(23,20,28,0.07); }
.chb { position: absolute; left: 0; top: 151px; width: 880px; height: 809px; overflow: hidden;
  background: linear-gradient(180deg, #fcf5f7 0%, #f8eaef 100%); }
.chi { position: absolute; left: 0; top: 960px; width: 880px; height: 130px;
  background: linear-gradient(180deg, #ffffff 0%, #fffafb 100%); box-shadow: 0 -2px 0 rgba(23,20,28,0.05); }
.chi .clp { position: absolute; left: 22px; top: 41px; width: 48px; height: 48px; color: rgba(23,20,28,0.42); }
.fld { position: absolute; left: 82px; top: 23px; width: 682px; height: 84px; border-radius: 42px;
  background: #f6eef1; box-shadow: inset 0 0 0 1.5px rgba(23,20,28,0.05); }
.fld .plh { position: absolute; left: 34px; top: 0; line-height: 84px; font-size: 30px; font-weight: 500;
  color: rgba(23,20,28,0.34); white-space: nowrap; }
.fld .tx { position: absolute; left: 28px; top: 0; height: 84px; display: flex; align-items: center;
  font-size: 30px; font-weight: 500; color: #17141c; white-space: nowrap; }
.fld .cur { display: block; width: 3px; height: 40px; border-radius: 2px; background: #d0194a; margin-left: 2px; }
.fld .rim { position: absolute; inset: -5px; border-radius: 47px; box-shadow: 0 0 0 4px #ff6e9c, 0 0 26px rgba(255,110,156,0.55);
  opacity: 0; visibility: hidden; }
.snd { position: absolute; left: 776px; top: 23px; width: 84px; height: 84px; }
.snd .mic { position: absolute; left: 18px; top: 18px; width: 48px; height: 48px; color: rgba(23,20,28,0.42); }
.snd .go { position: absolute; inset: 0; border-radius: 50%; opacity: 0;
  background: linear-gradient(165deg, #e0204b 0%, #ab112e 50%, #7a0a20 100%);
  box-shadow: inset 0 2px 1px rgba(255,255,255,0.5), 0 10px 22px -10px rgba(120,8,32,0.7);
  display: flex; align-items: center; justify-content: center; color: #fff; }
.snd .go .gf { width: 40px; height: 40px; margin-left: 4px; }
/* bubbles */
.bo, .bi { position: absolute; max-width: 680px; padding: 18px 24px 16px 26px; font-size: 30px; font-weight: 500;
  line-height: 38px; letter-spacing: -0.005em; }
.bo { right: 26px; color: #fff; border-radius: 34px 34px 10px 34px;
  background: linear-gradient(165deg, #e0204b 0%, #ab112e 60%, #8d0d24 100%);
  box-shadow: inset 0 1.5px 1px rgba(255,255,255,0.35), 0 16px 30px -16px rgba(120,8,32,0.6); }
.bi { left: 26px; color: #17141c; border-radius: 34px 34px 34px 10px; background: #ffffff;
  box-shadow: 0 16px 30px -18px rgba(60,10,25,0.4), 0 1px 2px rgba(60,10,25,0.08); }
.mt { display: inline-flex; align-items: center; gap: 6px; font-size: 20px; font-weight: 500;
  color: rgba(255,255,255,0.74); margin-left: 16px; vertical-align: -1px; }
.bi .mt { color: rgba(23,20,28,0.42); }
.tk2 { width: 26px; height: 22px; fill: none; stroke: currentColor; stroke-width: 2.2; stroke-linecap: round; stroke-linejoin: round; }
.tk2 .t2 { opacity: 0; }
.emp { position: absolute; left: 190px; top: 250px; width: 500px; padding: 34px 30px 30px; border-radius: 40px;
  background: rgba(23,20,28,0.045); text-align: center; }
.emp .gy { width: 76px; height: 76px; color: rgba(23,20,28,0.24); stroke-width: 1.8; }
.emp .et { margin-top: 12px; font-size: 30px; font-weight: 700; color: rgba(23,20,28,0.50); letter-spacing: -0.01em; }
.emp .es { margin-top: 8px; font-size: 24px; font-weight: 500; color: rgba(23,20,28,0.36); }
.tpill { position: absolute; left: 0; width: 880px; display: flex; justify-content: center; }
.tpill div { height: 54px; padding: 0 24px 0 16px; border-radius: 27px; background: rgba(23,20,28,0.09);
  display: flex; align-items: center; gap: 10px; font-size: 26px; font-weight: 700; color: rgba(23,20,28,0.62);
  font-variant-numeric: tabular-nums; }
.tpill svg { width: 34px; height: 34px; }
.tpill .hand { stroke: currentColor; stroke-width: 2.4; stroke-linecap: round; }

/* ---- b05 · ten visitors ---- */
#g5s { left: 70px; top: 290px; width: 940px; height: 190px; }
#g5row { position: absolute; left: 0; top: 0; width: 940px; height: 190px; display: flex; align-items: center;
  justify-content: center; gap: 12px; }
.pp { position: relative; width: 78px; height: 78px; color: #fff; }
.pp .gf { width: 78px; height: 78px; }
.pp.stay .gf { color: #ffb3c9; }

/* ---- b06 · ×2 ---- */
#g6c { left: 300px; top: 318px; width: 480px; height: 156px; border-radius: 60px; overflow: hidden; }
#g6t { left: 22px; top: 22px; width: 112px; height: 112px; }
#g6t .gf { position: relative; z-index: 1; width: 52%; height: 52%; color: #b4122f; }
#g6m { left: 160px; top: 30px; font-size: 20px; font-weight: 700; letter-spacing: 0.16em; color: #ffb3c9; }
#g6win { left: 156px; top: 54px; width: 300px; height: 80px; overflow: hidden; }
#g6roll { position: absolute; left: 0; top: 0; }
#g6roll div { height: 80px; line-height: 80px; font-size: 72px; font-weight: 900; letter-spacing: -0.04em; color: #fff; }
#g6sp { left: 150px; top: 330px; width: 150px; height: 130px; overflow: visible; }
#g6sp path { fill: none; stroke: rgba(255,255,255,0.85); stroke-width: 9; stroke-linecap: round; }

/* ---- b07 · Telegram Premium ---- */
#g7t { left: 440px; top: 180px; width: 210px; height: 210px; }
#g7t .mk { fill: url(#gw); }
#g7st { left: 604px; top: 150px; width: 88px; height: 88px; border-radius: 50%; z-index: 2;
  background: linear-gradient(165deg, #ff8ab0 0%, #e0204b 50%, #8d0d24 100%);
  box-shadow: inset 0 2px 1px rgba(255,255,255,0.55), 0 16px 30px -12px rgba(70,4,20,0.7);
  display: flex; align-items: center; justify-content: center; color: #fff; overflow: hidden; }
#g7st .gf { width: 50px; height: 50px; position: relative; z-index: 1; }
#g7r { left: 440px; top: 180px; width: 210px; height: 210px; }
#g7l { height: 70px; padding: 0 30px 0 22px; display: flex; align-items: center; gap: 12px;
  font-size: 32px; font-weight: 700; letter-spacing: -0.01em; white-space: nowrap; }
#g7l .gf { width: 34px; height: 34px; color: #ff8ab0; }
#g7l .pr { color: #ffb3c9; }
#g7c { left: 712px; top: 250px; height: 76px; padding: 0 28px 0 16px; display: flex; align-items: center; gap: 12px;
  font-size: 30px; font-weight: 700; white-space: nowrap; }
#g7c .cn { width: 46px; height: 46px; border-radius: 50%; position: relative;
  background: linear-gradient(160deg, #ffd0dd 0%, #ff8ab0 55%, #d0194a 100%);
  box-shadow: inset 0 0 0 3px rgba(255,255,255,0.45), inset 0 -4px 6px rgba(120,8,32,0.35); }
#g7c .cn i { position: absolute; left: 11px; top: 11px; width: 24px; height: 24px; border-radius: 50%;
  box-shadow: inset 0 0 0 2.5px rgba(255,255,255,0.75); }
""")


def site_html(p):
    """The glass site window. `p` prefixes ids — it appears twice (b01, b10)."""
    return fill(u'''
        <div class="site shelf edge hide" id="{{p}}">
          <i class="dot" style="left:40px"></i><i class="dot" style="left:66px"></i><i class="dot" style="left:92px"></i>
          <i class="url"></i><i class="hr"></i>
          <i class="hd" id="{{p}}Hd"></i>
          <i class="br" id="{{p}}B1" style="top:186px;width:470px"></i>
          <i class="br" id="{{p}}B2" style="top:226px;width:340px"></i>
          <div class="im" id="{{p}}Im"><svg viewBox="0 0 232 172"><circle cx="160" cy="62" r="24" fill="rgba(255,255,255,0.75)"/>
            <path d="M0 130 L58 78 L96 112 L140 70 L232 142 L232 172 L0 172Z" fill="rgba(255,255,255,0.42)"/></svg></div>
          <div class="sbtn" id="{{p}}Btn"><div class="jelly">{{tg}}<span>Написати в Telegram</span><div class="sheen"></div></div>
            <div class="lk hide" id="{{p}}Lk">{{link}}</div></div>
        </div>''', p=p, tg=g.mark("telegram"), link=gl("link"))


# site button centre on screen (for the iris and the taps)
BTN = (100 + 48 + 240, 92 + 290 + 48)


def chat_html(p, name, status, av, body):
    return fill(u'''
          <div class="chw hide" id="{{p}}W"><div class="sheet chat" id="{{p}}">
            <div class="chh">
              {{back}}<div class="av">{{av}}</div>
              <div class="cx nm">{{name}}</div><div class="cx st" id="{{p}}St">{{status}}</div><i class="ln"></i>
            </div>
            <div class="chb" id="{{p}}B">{{body}}</div>
            <div class="chi">
              {{clip}}
              <div class="fld" id="{{p}}F"><i class="rim" id="{{p}}Rim"></i><div class="plh" id="{{p}}P">Повідомлення</div>
                <div class="tx"><span id="{{p}}T"></span><b class="cur" id="{{p}}C"></b></div></div>
              <div class="snd" id="{{p}}Snd">{{mic}}<div class="go" id="{{p}}Go">{{send}}</div></div>
            </div>
            <div class="sheen"></div>
          </div></div>''', p=p, name=name, status=status, av=av, body=body,
                back=gl("back", "gy bk"), clip=gl("clip", "gy clp"),
                mic=gl("mic", "gy mic", ' id="%sMic"' % p), send=fl("send"))


def takeover(tid, inner):
    return (u'<div class="tkx hide" id="%s"><div class="tkg"></div><div class="aurs"></div>'
            u'<div class="grain"></div>%s\n        </div>' % (tid, inner))


EMPTY = (u'<div class="emp" id="%sE">' + gl("empty") +
         u'<div class="et">Повідомлень ще немає</div><div class="es">Напишіть перше повідомлення</div></div>')

# Typed text, as a pure function of time (painted by one clock tween, the way
# reel 15 does its counters, so any seek lands on the right characters).
# id -> [t0, t1, text, mode]; mode type / del / set.
TYPE = {}


# =================================================================== b01-b04
@beat
def b01_button_to_empty_chat():
    """«Знаєш, коли на сайті просто висить кнопка «написати в Телеграм», а
    людина заходить в чат з менеджером — і там пустота. Вона сидить і думає,
    з чого почати, менеджер відповідає через годину»

    NEAR -> OVER. A glass site window above her head on «сайті», the button
    lands on «кнопка» (it says «Написати в Telegram» — blackout) and is
    pressed on «Телеграм». On «заходить» the iris opens out of the button onto
    the burgundy ground and the chat grows from the same point: «Менеджер»,
    nothing in it, a cursor blinking («пустота»). «думає, з чого почати» —
    two openings typed and deleted. «менеджер відповідає» — «Добрий день!»
    sent with one tick; «через годину» — the time pill rolls 14:02 -> 15:02
    and only then the second tick: read, an hour later."""
    TYPE["c1"] = [
        [T["vona"] + 0.10, T["vona"] + 0.62, u"Добрий день, я хоті", "type"],
        [T["dumaye"] + 0.12, T["dumaye"] + 0.40, u"Добрий день, я хоті", "del"],
        [T["pochaty"] - 0.20, T["pochaty"] + 0.30, u"Вітаю! Підкажіть", "type"],
        [T["pochaty"] + 0.40, T["pochaty"] + 0.66, u"Вітаю! Підкажіть", "del"],
        [T["men2"] - 0.20, T["men2"] + 0.14, u"Добрий день!", "type"],
        [T["vidp"] - 0.06, T["vidp"] - 0.06, u"", "set"],
    ]
    body = (EMPTY % "c1" +
            u'<div class="tpill hide" id="c1Tp" style="top:560px"><div><svg viewBox="0 0 24 24">'
            u'<circle class="hand" cx="12" cy="12" r="9" fill="none"/>'
            u'<path class="hand" id="c1Hm" d="M12 12V6.6"/><path class="hand" d="M12 12l3.2 2"/></svg>'
            u'<span id="c1Clk">14:02</span></div></div>'
            u'<div class="bo hide" id="c1M" style="bottom:36px">Добрий день!<span class="mt">14:02 %s</span></div>'
            % ticks("c1Tk"))
    html = fill(u'''
      <div class="g full" id="g1">
        {{site}}
        {{tap}}
      </div>
      <div class="g full" id="g2">
        {{tk}}
      </div>''', site=site_html("s1"), tap=tap("tp1", BTN[0] + 60, BTN[1] + 6),
                tk=takeover("tk2", chat_html("c1", u"Менеджер", u"був(ла) нещодавно",
                                             u"М", body)))
    src = js('''
  tl.set("#g1", {autoAlpha: 1}, @t_in);
  arr("#s1", @t_in, {s: 0.86, y: 30});
  tl.fromTo(["#s1Hd", "#s1B1", "#s1B2", "#s1Im"], {autoAlpha: 0, y: 14}, {autoAlpha: 1, y: 0, duration: 0.5, ease: SP, stagger: 0.07}, @t_in2);
  // «кнопка»
  arr("#s1Btn", @t_btn, {s: 0.55, y: 24});
  shn("#s1Btn .sheen", @t_sh);
  // «Телеграм» — pressed
  press("#s1Btn", @tg1);
  tapAt("#tp1", @tg1);
  // «заходить в чат» — the iris opens out of the button
  tl.set("#g2", {autoAlpha: 1}, @t_iris);
  G.irisOpen("#tk2", @t_iris, @bx, @by, 0.85);
  drift1("#tk2", @t_iris, 6.5);
  bin("#c1W", @t_sheet, 16, 0.42);
  tl.fromTo("#c1W", {scale: 0.3, x: @ox, y: @oy}, {scale: 1, x: 0, y: 0, duration: 1.0, ease: spring(0.72, 12)}, @t_sheet);
  tl.fromTo("#c1 .chh > *", {autoAlpha: 0, y: 10}, {autoAlpha: 1, y: 0, duration: 0.5, ease: SP, stagger: 0.05}, @t_hd);
  tl.set("#g1", {autoAlpha: 0}, @t_g1off);
  // «пустота»
  tl.fromTo("#c1E", {autoAlpha: 0, scale: 0.85}, {autoAlpha: 1, scale: 1, duration: 0.6, ease: SP}, @t_emp);
  // «менеджер відповідає» — «Добрий день!» goes out, one tick
  tl.to("#c1E", {autoAlpha: 0, scale: 0.92, duration: 0.25, ease: "power2.in"}, @t_send);
  sendBubble("#c1M", "#c1Go", @t_send);
  // «через годину» — the time rolls an hour; read only then
  tl.fromTo("#c1Tp", {autoAlpha: 0, y: 12}, {autoAlpha: 1, y: 0, duration: 0.4, ease: SP}, @t_tp);
  tl.fromTo("#c1Hm", {rotation: 0, svgOrigin: "12 12"}, {rotation: 360, svgOrigin: "12 12", duration: 0.62, ease: "power2.inOut"}, @cherez);
  tl.to("#c1Tk", {opacity: 1, duration: 0.12}, @t_read);
  G.bump("#c1M", @t_read);
  // «і половина людей» — the chat closes onto the row of visitors
  tl.to("#c1W", {scale: 0.3, y: 120, duration: 0.45, ease: "power3.in"}, @t_out);
  bout("#c1W", @t_out2, 12, 0.24);
  G.irisClose("#tk2", @t_out, 540, 386, 0.55);
  tl.set("#g2", {autoAlpha: 0}, @t_off);''',
             t_in=T["sayti"] - 0.10, t_in2=T["sayti"] + 0.05, t_btn=T["knopka"] - 0.08,
             t_sh=T["knopka"] + 0.45, t_iris=T["zakh"] - 0.05, bx=BTN[0], by=BTN[1],
             t_sheet=T["zakh"] + 0.05, ox=BTN[0] - 540, oy=BTN[1] - 681, t_hd=T["chat1"] - 0.02,
             t_g1off=T["zakh"] + 0.90, t_emp=T["pustota"] - 0.06, t_send=T["men2"] + 0.30,
             t_tp=T["vidp"] + 0.25, t_read=T["hodynu_e"] - 0.02, t_out=T["polov"] - 0.20,
             t_out2=T["polov"] + 0.02, t_off=T["polov"] + 0.38)
    return html, src


CLOCK = (T["cherez"], 0.62)     # c1Clk rolls 14:02 -> 15:02 over this span


# ======================================================================= b05
@beat
def b05_half_leave():
    """«і половина людей просто закриває чат, не дописавши.»

    NEAR. The iris closes onto a glass row of ten visitors above her head;
    on «закриває чат» five of them drop out (every other one, not the right
    half — it is half of *people*, not a bar)."""
    leave_i = [1, 3, 4, 7, 8]
    ppl = "".join('<div class="pp%s" id="pp%d">%s</div>' % ("" if i in leave_i else " stay", i, fl("person"))
                  for i in range(10))
    html = fill(u'''
      <div class="g full" id="g5">
        <div class="dglass edge abs hide" id="g5s"><div id="g5row">{{ppl}}</div></div>
      </div>''', ppl=ppl)
    src = js('''
  tl.set("#g5", {autoAlpha: 1}, @t_in);
  arr("#g5s", @t_in, {s: 0.4, y: 0});
  tl.fromTo("#g5row .pp", {autoAlpha: 0, scale: 0.4, y: 16}, {autoAlpha: 1, scale: 1, y: 0, duration: 0.5, ease: POP, stagger: 0.045}, @t_pp);
  // «закриває чат» — half of them leave
  tl.to("#g5row .pp:not(.stay)", {autoAlpha: 0, y: 46, scale: 0.7, duration: 0.42, ease: "power2.in", stagger: 0.08}, @zakr);
  tl.to("#g5row .pp.stay", {scale: 1.08, duration: 0.2, ease: "power2.out"}, @t_stay);
  tl.to("#g5row .pp.stay", {scale: 1, duration: 0.5, ease: SP}, @t_stay2);
  // «не дописавши»
  G.bump("#g5s", @dopys);
  bout("#g5s", @t_out, 10, 0.3);
  tl.set("#g5", {autoAlpha: 0}, @t_off);''',
             t_in=T["polov"] + 0.02, t_pp=T["polov"] + 0.14, t_stay=T["chat2"] + 0.10,
             t_stay2=T["chat2"] + 0.30, t_out=T["dopys_e"] - 0.20, t_off=T["dopys_e"] + 0.12)
    return html, src


# ======================================================================= b06
@beat
def b06_twice_as_fast():
    """«є спосіб це прискорити приблизно в два рази»

    NEAR. A dark-glass chip lands on «спосіб»: a bolt in a pearl tile,
    ШВИДКІСТЬ ×1. «прискорити» — speed lines draw off its left edge and the
    bolt jolts; «два рази» — the value rolls to ×2 (blackout, it says it)."""
    html = fill(u'''
      <div class="g full" id="g6">
        <svg class="abs" id="g6sp" viewBox="0 0 150 130"><path id="g6l0" d="M140 34 H40"/><path id="g6l1" d="M140 66 H10"/><path id="g6l2" d="M140 98 H56"/></svg>
        <div class="dglass edge abs hide" id="g6c">
          <div class="cx" id="g6t"><div class="pearl">{{bolt}}</div></div>
          <div class="cx" id="g6m">ШВИДКІСТЬ</div>
          <div class="cx" id="g6win"><div id="g6roll" data-layout-allow-overlap><div data-layout-allow-overlap>×1</div><div data-layout-allow-overlap>×2</div></div></div>
          <div class="sheen"></div>
        </div>
      </div>''', bolt=fl("bolt"))
    src = js('''
  tl.set("#g6", {autoAlpha: 1}, @t_in);
  arr("#g6c", @t_in, {s: 0.6, y: 20});
  tl.fromTo("#g6t", {scale: 0.5, autoAlpha: 0}, {scale: 1, autoAlpha: 1, duration: 0.55, ease: SP}, @t_in2);
  tl.fromTo(["#g6m", "#g6win"], {autoAlpha: 0, x: -12}, {autoAlpha: 1, x: 0, duration: 0.5, ease: SP, stagger: 0.06}, @t_in3);
  // «прискорити»
  G.drawPrep("g6l0"); G.drawPrep("g6l1"); G.drawPrep("g6l2");
  tl.to(["#g6l0", "#g6l1", "#g6l2"], {strokeDashoffset: 0, duration: 0.32, ease: "power2.out", stagger: 0.05}, @prysk);
  tl.to(["#g6l0", "#g6l1", "#g6l2"], {autoAlpha: 0, x: -40, duration: 0.4, ease: "power2.in", stagger: 0.05}, @t_sl2);
  tl.to("#g6c", {x: 14, duration: 0.12, ease: "power2.out"}, @prysk);
  tl.to("#g6c", {x: 0, duration: 0.5, ease: SP}, @t_px);
  // «два рази»
  tl.to("#g6roll", {y: -80, duration: 0.5, ease: SP}, @t_dva);
  G.bump("#g6c", @dva);
  shn("#g6c .sheen", @t_dsh);
  bout("#g6c", @t_out, 10, 0.28);
  tl.set("#g6", {autoAlpha: 0}, @t_off);''',
             t_in=T["sposib"] - 0.08, t_in2=T["sposib"] + 0.04, t_in3=T["sposib"] + 0.14,
             t_sl2=T["prysk"] + 0.45, t_px=T["prysk"] + 0.12, t_dva=T["dva"] - 0.04,
             t_dsh=T["dva"] + 0.20, t_out=T["razy_e"] - 0.10, t_off=T["razy_e"] + 0.20)
    return html, src


# ======================================================================= b07
@beat
def b07_premium():
    """«і потрібна для цього всього одна штука — Telegram Premium, який
    коштує просто копійки.»

    NEAR. The Telegram mark in a clear tile on «одна штука»; its label writes
    itself on «Telegram», and on «Premium» the star badge pops onto the tile
    with a square ripple and the label gains «Premium» (blackout: it says
    it). «копійки» — a coin chip beside it (blackout). On «Заходиш» the tile
    opens into her screen recording (b08)."""
    html = fill(u'''
      <div class="g full" id="g7">
        <div class="sqring abs" id="g7r"></div>
        <div class="abs hide" id="g7t"><div class="clear edge">{{tg}}</div></div>
        <div class="abs hide" id="g7st">{{star}}<div class="sheen"></div></div>
        <div class="ctr" id="g7lw" style="top:418px"><div class="dchip edge hide" id="g7l" style="position:relative">{{star2}}<span>Telegram</span><span class="pr" id="g7lp">Premium</span></div></div>
        <div class="dchip edge hide" id="g7c"><div class="cn"><i></i></div><span>копійки</span></div>
      </div>''', tg=g.mark("telegram"), star=fl("star"), star2=fl("star"))
    src = js('''
  tl.set("#g7", {autoAlpha: 1}, @t_in);
  arr("#g7t", @t_in, {s: 0.5, y: 30});
  tl.fromTo("#g7t .mk", {scale: 0.55, autoAlpha: 0}, {scale: 1, autoAlpha: 1, duration: 0.55, ease: SP}, @t_in2);
  // «Telegram»
  gsap.set("#g7lp", {autoAlpha: 0});
  arr("#g7l", @t_lab, {s: 0.7, y: -10});
  // «Premium» — the star lands, the label completes
  tl.fromTo("#g7st", {autoAlpha: 0, scale: 0.2, rotation: -40}, {autoAlpha: 1, scale: 1, rotation: 0, duration: 0.7, ease: POP, immediateRender: false}, @t_st);
  G.ripple("#g7r", @t_rip);
  G.bump("#g7t", @t_rip);
  shn("#g7st .sheen", @t_rip);
  tl.fromTo("#g7lp", {autoAlpha: 0, x: -10}, {autoAlpha: 1, x: 0, duration: 0.4, ease: SP, immediateRender: false}, @prem);
  // «копійки»
  bout("#g7l", @t_lo, 8, 0.25);
  arr("#g7c", @t_kop, {s: 0.5, x: -30, y: 0});
  tl.fromTo("#g7c .cn", {rotationY: 0}, {rotationY: 360, duration: 0.8, ease: "power2.out"}, @t_kop);
  // «Заходиш» — the tile opens into her screen (b08 irises out of its centre)
  bout("#g7c", @t_out, 8, 0.22);
  tl.to(["#g7t", "#g7st"], {scale: 1.5, autoAlpha: 0, duration: 0.3, ease: "power2.in"}, @t_out2);
  tl.set("#g7", {autoAlpha: 0}, @t_off);''',
             t_in=T["odna"] - 0.06, t_in2=T["odna"] + 0.06, t_lab=T["tg2"] - 0.04,
             t_st=T["prem"] - 0.06, t_rip=T["prem"] + 0.10, t_lo=T["kop"] - 0.36,
             t_kop=T["kop"] - 0.06, t_out=T["zakhodysh"] - 0.30, t_out2=T["zakhodysh"] - 0.08,
             t_off=T["zakhodysh"] + 0.24)
    return html, src


# ============================================================ b08-b12 screen
# Her corner seat: the matte is her whole plate, so the wrapper scales it
# about (0, 0) and moves it — head top (540, ~570 on the pushed plate) lands
# at (880, 1548), just under the caption band; she is bottom-right because the
# recording's labels and taps are all on the left of every row.
HER_S = 0.45
HER_X, HER_Y = 880 - 540 * HER_S, 1548 - 570 * HER_S
RY = SCR.REC_Y

# Screen items in RECORDING coordinates (1080x2082) — screen.py SEG maps the
# recording's time onto her words. (x, y, w, h, radius)
HL = {
    "tab": (536, 1908, 224, 144, 60),       # Settings tab, bottom bar
    "biz": (34, 1030, 1012, 128, 30),       # Telegram Business row
    "lnk": (26, 1088, 1028, 170, 30),       # Links to Chat row
    "new": (34, 724, 1012, 132, 30),        # Create a Link to Chat
    "fld": (24, 1058, 1040, 124, 62),       # the preset-message field
    "ok": (944, 1068, 104, 104, 52),        # the ✓ (save)
    "url": (318, 762, 444, 80, 24),         # the link on the card (blurred)
}
TAPS = {"tab": (648, 1962), "biz": (330, 1094), "lnk": (330, 1172), "new": (340, 790),
        "fld": (560, 1120), "ok": (996, 1120), "url": (540, 802)}
CHIP = (540, 330)              # where the lifted link chip hovers

k.css(u"""
/* ---- b08 · her screen recording, the whole frame ---- */
#scr { position: absolute; inset: 0; overflow: hidden; clip-path: circle(0px at 540px 290px); }
#scrBg { position: absolute; inset: 0; background: #f3f2f5; }
#scrW { position: absolute; left: 0; top: %(ry)dpx; width: 1080px; height: 2082px; transform-origin: 0 0; }
#scrV { position: absolute; left: 0; top: 0; width: 1080px; height: 2082px; }
.hl { position: absolute; border-radius: 30px; opacity: 0; visibility: hidden;
  background: linear-gradient(160deg, rgba(255,110,156,0.20) 0%%, rgba(255,110,156,0.08) 100%%);
  box-shadow: inset 0 0 0 4px rgba(255,110,156,0.95), 0 0 0 10px rgba(255,110,156,0.16),
              0 24px 50px -22px rgba(180,18,47,0.55); }
.hl::before { content: ""; position: absolute; inset: 0; border-radius: inherit; padding: 2px;
  background: linear-gradient(140deg, rgba(255,255,255,0.95) 0%%, rgba(255,255,255,0.1) 30%%,
              rgba(255,255,255,0.05) 70%%, rgba(255,255,255,0.9) 100%%);
  -webkit-mask: linear-gradient(#000 0 0) content-box, linear-gradient(#000 0 0);
  -webkit-mask-composite: xor; mask-composite: exclude; }
#swipe { position: absolute; left: 560px; top: 1640px; width: 0; height: 0; }
#swipe i { position: absolute; left: -40px; top: -40px; width: 80px; height: 80px; border-radius: 50%%;
  background: radial-gradient(circle, rgba(255,110,156,0.85) 0%%, rgba(255,110,156,0.4) 60%%, rgba(255,110,156,0) 72%%); }
#herSh { position: absolute; left: 520px; top: 1330px; width: 820px; height: 820px; border-radius: 50%%;
  background: radial-gradient(closest-side, rgba(24,6,12,0.42), rgba(24,6,12,0)); }
#herBox { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; transform-origin: 0 0; }
/* the lifted link */
#lnk { height: 92px; padding: 0 34px 0 16px; border-radius: 46px; display: flex; align-items: center; gap: 16px;
  font-size: 34px; font-weight: 700; letter-spacing: -0.01em; white-space: nowrap; }
#lnk .lc { width: 62px; height: 62px; border-radius: 50%%; display: flex; align-items: center; justify-content: center;
  background: linear-gradient(165deg, #ff8ab0 0%%, #e0204b 50%%, #8d0d24 100%%); box-shadow: inset 0 2px 1px rgba(255,255,255,0.5); }
#lnk .lc svg { width: 36px; height: 36px; stroke: #fff; stroke-width: 2.6; }
""" % {"ry": RY})


def rbox(key):
    x, y, w, h, r = HL[key]
    return ('<div class="hl" id="hl-%s" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx;border-radius:%dpx"></div>'
            % (key, x, y, w, h, r))


def punch(t, key, kk, d=0.55, ease="SOFT"):
    """Gentle punch-in on a recording point: scale kk about it, the point
    staying where it is on screen (#scrW scales about its own 0 0)."""
    x, y = TAPS[key]
    return ('  tl.to("#scrW", {scale: %.3f, x: %.1f, y: %.1f, duration: %.2f, ease: %s}, %.3f);'
            % (kk, x * (1 - kk), y * (1 - kk), d, ease, t))


def unpunch(t, d=0.45):
    return '  tl.to("#scrW", {scale: 1, x: 0, y: 0, duration: %.2f, ease: "power2.inOut"}, %.3f);' % (d, t)


def light(key, t_in, t_out):
    return ('  tl.fromTo("#hl-%s", {autoAlpha: 0, scale: 1.06}, {autoAlpha: 1, scale: 1, duration: 0.45, ease: SP, immediateRender: false}, %.3f);\n'
            '  tl.to("#hl-%s", {autoAlpha: 0, duration: 0.25, ease: "power2.in"}, %.3f);' % (key, t_in, key, t_out))


@beat
def b08_screen_to_chat():
    """«Заходиш в налаштування свого акаунту, скролиш вниз, знаходиш там
    Telegram Бізнес, а в ньому — посилання на розмову. Створюєш нове
    посилання і одразу прописуєш текст, з яким людина до тебе прийде, типу
    «доброго дня, мене цікавить те й те». Зберігаєш, береш це посилання і
    вставляєш на сайт. І тепер, коли людина тицяє на кнопку, в неї
    відкривається не пустий чат, а вже написане повідомлення — залишається
    його лише відправити.»

    SCREEN -> NEAR -> OVER, one movement, so one block.

    Her explicit ask: her screen recording is the whole frame and she is cut
    out in the corner, as if filmed on a greenscreen. The Premium tile opens
    (iris) into the recording *behind* her — her matte sits exactly over the
    plate, so her room simply turns into Telegram — and then she shrinks into
    the bottom-right corner, head just under the captions. Each item she
    names gets a glass highlight and a gentle punch-in, and every tap a pink
    ripple: Settings (the tab), the scroll, Telegram Business, Links to Chat,
    Create, the field while «Привіт! Хочу на Мадейру!» types itself (her
    recording's message — captions stay: what she says is a different
    example), ✓ on «Зберігаєш», the link on «береш». The link lifts off as a
    glass chip; she grows back into her plate *before* the recording closes
    (so there is never a second her), then it irises shut behind her. «на
    сайт» — the site window returns and the chip drops into the button.
    «тицяє на кнопку» — tap; the chat opens out of the button with the
    message already in the field; «відправити» — sent, ✓✓."""
    TYPE["c2"] = [[T["vidkr"] - 0.10, T["vidkr"] - 0.10, u"Привіт! Хочу на Мадейру!", "set"],
                  [T["vidpr"] + 0.08, T["vidpr"] + 0.08, u"", "set"]]
    hls = "\n            ".join(rbox(kk) for kk in ["tab", "biz", "lnk", "new", "fld", "ok", "url"])
    taps = "\n            ".join(tap("tp-" + kk, x, y) for kk, (x, y) in sorted(TAPS.items()))
    body2 = (u'<div class="bo hide" id="c2M" style="bottom:36px">Привіт! Хочу на Мадейру!'
             u'<span class="mt">14:05 %s</span></div>' % ticks("c2Tk"))
    html = fill(u'''
      <div class="g full" id="g8">
        <div id="scr" class="hide">
          <div id="scrBg"></div>
          <div id="scrW" data-layout-allow-overflow>
            <video id="scrV" src="assets/media/screen.mp4" data-start="{{s0}}" data-duration="{{sd}}"
                   data-media-start="0" muted playsinline></video>
            {{hls}}
            {{taps}}
            <div id="swipe" class="hide"><i></i></div>
          </div>
        </div>
        <div id="herSh" class="hide" data-layout-allow-overflow></div>
        <div id="herBox" data-layout-allow-overflow><video id="matte-her" class="plate matte" src="assets/mattes/her.webm"
             data-start="{{s0}}" data-duration="{{sd}}" data-media-start="0" muted playsinline></video></div>
      </div>
      <div class="g full" id="g10">
        {{site}}
        {{tap}}
      </div>
      <div class="g full" id="g9">
        <div class="ctr" style="top:{{cy}}px"><div class="dchip edge hide" id="lnk" style="position:relative"><div class="lc">{{link}}</div><span>t.me/m/…</span></div></div>
      </div>
      <div class="g full" id="g11">
        {{tk}}
      </div>''', s0="%.3f" % SCR.SCR0, sd="%.3f" % (SCR.SCR1 - SCR.SCR0), hls=hls, taps=taps,
                cy=CHIP[1] - 46, link=gl("link"), site=site_html("s2"),
                tap=tap("tp2", BTN[0] + 60, BTN[1] + 6),
                tk=takeover("tk11", chat_html("c2", u"Менеджер", u"був(ла) нещодавно", u"М", body2)))
    lines = []
    L = lines.append
    L('''  tl.set("#g8", {autoAlpha: 1}, @t_in);
  tl.set("#scr", {autoAlpha: 1}, @t_in);
  // «Заходиш» — the Premium tile opens into her recording, behind her
  tl.fromTo("#scr", {clipPath: "circle(0px at 540px 290px)"}, {clipPath: "circle(2300px at 540px 290px)", duration: 0.82, ease: "power3.inOut", immediateRender: false}, @t_in);
  // then she shrinks into the corner (only once the room is gone)
  tl.fromTo("#herBox", {x: 0, y: 0, scale: 1}, {x: @hx, y: @hy, scale: @hs, duration: 0.85, ease: SOFT, immediateRender: false}, @t_shr);
  tl.fromTo("#herSh", {autoAlpha: 0}, {autoAlpha: 1, duration: 0.6}, @t_shr2);''')
    # «свого акаунту» — Settings, the tab
    L(light("tab", T["akauntu"] - 0.06, T["skrol"] - 0.06))
    L('  tapAt("#tp-tab", %.3f);' % (T["akauntu"] + 0.04))
    # «скролиш вниз» — a finger drags up
    L('''  tl.set("#swipe", {autoAlpha: 1, y: 0}, @t_sw);
  tl.fromTo("#swipe", {y: 0}, {y: -720, duration: 0.95, ease: "power2.inOut", immediateRender: false}, @t_sw);
  tl.to("#swipe", {autoAlpha: 0, duration: 0.2}, @t_sw2);''')
    # «Telegram Бізнес»
    L(light("biz", T["tg3"] - 0.06, T["biznes"] + 0.20))
    L(punch(T["tg3"] - 0.10, "biz", 1.07))
    L('  tapAt("#tp-biz", %.3f);' % SCR.comp(4.15))
    L(unpunch(T["biznes"] + 0.16))
    # «посилання на розмову»
    L(light("lnk", T["posyl1"] - 0.04, T["rozmovu"] + 0.12))
    L(punch(T["posyl1"] - 0.08, "lnk", 1.07))
    L('  tapAt("#tp-lnk", %.3f);' % SCR.comp(6.40))
    L(unpunch(T["rozmovu"] + 0.10))
    # «Створюєш нове посилання»
    L(light("new", T["stvor"] - 0.04, T["nove"] + 0.14))
    L(punch(T["stvor"] - 0.08, "new", 1.07))
    L('  tapAt("#tp-new", %.3f);' % SCR.comp(7.80))
    L(unpunch(T["nove"] + 0.12))
    # «одразу прописуєш текст» — the field, punch in while it types
    L('  tapAt("#tp-fld", %.3f);' % T["odrazu"])
    L(light("fld", T["propys"] - 0.04, T["zber"] - 0.30))
    L(punch(T["propys"] - 0.08, "fld", 1.10, 0.7))
    L(punch(T["typu"] - 0.04, "fld", 1.15, 0.9))
    L(unpunch(T["zber"] - 0.32, 0.3))
    # «Зберігаєш» — ✓
    L(light("ok", T["zber"] - 0.06, T["beresh"] - 0.10))
    L('  tapAt("#tp-ok", %.3f);' % SCR.comp(18.20))
    # «береш це посилання» — tap the link, it lifts off as a chip
    L(light("url", T["beresh"] - 0.06, T["beresh"] + 0.50))
    L(punch(T["beresh"] - 0.10, "url", 1.10, 0.5))
    L('  tapAt("#tp-url", %.3f);' % SCR.comp(20.35))
    L('''  tl.set("#g9", {autoAlpha: 1}, @t_ch);
  bin("#lnk", @t_ch, 10, 0.3);
  tl.fromTo("#lnk", {scale: 0.72, y: @chy0}, {scale: 1, y: 0, duration: 0.9, ease: SP, immediateRender: false}, @t_ch);
  // «і вставляєш» — she grows back into her plate first, then it closes
  tl.to("#herBox", {x: 0, y: 0, scale: 1, duration: 0.5, ease: "power3.inOut"}, @t_grow);
  tl.to("#herSh", {autoAlpha: 0, duration: 0.3}, @t_grow);
  tl.to("#scr", {clipPath: "@clip_end", duration: 0.5, ease: "power3.inOut"}, @t_cls);
  tl.set("#g8", {autoAlpha: 0}, @t_g8off);
  // «на сайт» — the site returns, the chip drops into its button
  tl.set("#g10", {autoAlpha: 1}, @t_site);
  arr("#s2", @t_site, {s: 0.86, y: 30});
  tl.fromTo(["#s2Hd", "#s2B1", "#s2B2", "#s2Im", "#s2Btn"], {autoAlpha: 0, y: 14}, {autoAlpha: 1, y: 0, duration: 0.5, ease: SP, stagger: 0.05}, @t_site2);
  tl.to("#lnk", {x: @dx, y: @dy, scale: 0.3, duration: 0.42, ease: "power3.in"}, @t_drop);
  tl.to("#lnk", {autoAlpha: 0, duration: 0.1}, @t_drop2);
  tl.set("#g9", {autoAlpha: 0}, @t_g9off);
  tl.fromTo("#s2Lk", {autoAlpha: 0, scale: 0.3}, {autoAlpha: 1, scale: 1, duration: 0.55, ease: POP, immediateRender: false}, @t_drop2);
  G.bump("#s2Btn", @t_drop2);
  shn("#s2Btn .sheen", @t_drop3);
  // «тицяє на кнопку»
  press("#s2Btn", @tytsyaye);
  tapAt("#tp2", @tytsyaye);
  // «відкривається» — the chat opens out of the button, already typed
  tl.set("#g11", {autoAlpha: 1}, @t_iris);
  G.irisOpen("#tk11", @t_iris, @bx, @by, 0.85);
  drift1("#tk11", @t_iris, 6.5);
  bin("#c2W", @t_sheet, 16, 0.42);
  tl.fromTo("#c2W", {scale: 0.3, x: @ox, y: @oy}, {scale: 1, x: 0, y: 0, duration: 1.0, ease: spring(0.72, 12)}, @t_sheet);
  tl.set("#g10", {autoAlpha: 0}, @t_g10off);
  // «не пустий чат» — the field is already full
  tl.fromTo("#c2Rim", {autoAlpha: 0, scale: 1.04}, {autoAlpha: 1, scale: 1, duration: 0.45, ease: SP, immediateRender: false}, @pustyi);
  // «а вже написане повідомлення»
  G.bump("#c2F", @vzhe);
  shn("#c2 > .sheen", @napysane);
  // «залишається його лише відправити»
  tl.to("#c2Rim", {autoAlpha: 0, duration: 0.3}, @zalysh);
  G.bump("#c2Go", @zalysh);
  tapAt("#tp2b", @vidpr);
  sendBubble("#c2M", "#c2Go", @t_send);
  tl.to("#c2Tk", {opacity: 1, duration: 0.12}, @t_read);
  G.bump("#c2M", @t_read);
  // «Це вже трошки спрощує» — the chat closes; clear frame for «життя всім»
  tl.to("#c2W", {scale: 0.3, y: -300, duration: 0.45, ease: "power3.in"}, @t_out);
  bout("#c2W", @t_out2, 12, 0.24);
  G.irisClose("#tk11", @t_out, 540, 280, 0.55);
  tl.set("#g11", {autoAlpha: 0}, @t_off);''')
    src = js("\n".join(lines),
             t_in=T["zakhodysh"] - 0.08, t_shr=T["zakhodysh"] + 0.76, t_shr2=T["zakhodysh"] + 0.90,
             hx="%.1f" % HER_X, hy="%.1f" % HER_Y, hs="%.3f" % HER_S,
             t_sw=T["skrol"] - 0.02, t_sw2=T["skrol"] + 0.90,
             t_ch=T["beresh"] + 0.28, chy0=(TAPS["url"][1] + RY) - CHIP[1],
             t_grow=T["vstavl"] - 0.30, t_cls=T["vstavl"] + 0.24, clip_end="circle(0px at %dpx %dpx)" % CHIP,
             t_g8off=SCR.SCR1 - 0.02, t_site=T["na_sayt"] - 0.18, t_site2=T["na_sayt"] - 0.06,
             dx=BTN[0] - CHIP[0], dy=BTN[1] - CHIP[1], t_drop=T["sayt"] - 0.06,
             t_drop2=T["sayt"] + 0.34, t_drop3=T["sayt"] + 0.50, t_g9off=T["sayt"] + 0.46,
             t_iris=T["vidkr"] - 0.10, bx=BTN[0], by=BTN[1], t_sheet=T["vidkr"],
             ox=BTN[0] - 540, oy=BTN[1] - 681, t_g10off=T["vidkr"] + 0.80,
             t_send=T["vidpr"] + 0.08, t_read=T["vidpr_e"] + 0.30,
             t_out=T["vidpr_e"] + 0.62, t_out2=T["vidpr_e"] + 0.84, t_off=T["vidpr_e"] + 1.20)
    html = html.replace("{{tp2b}}", "")
    html = html.replace('<div class="snd" id="c2Snd">',
                        '<div class="snd" id="c2Snd">' + tap("tp2b", 42, 42))
    return html, src


# ======================================================================= b14
k.css(u"""
/* ---- b14 · the message becomes a trigger for a bot on her account ---- */
#g14s { left: 80px; top: 110px; width: 920px; height: 250px; border-radius: 72px; overflow: hidden; }
#g14st { left: 0; top: 73px; width: 920px; height: 104px; }
.stp { position: absolute; top: 10px; width: 84px; height: 84px; border-radius: 50%; display: flex;
  align-items: center; justify-content: center; font-size: 40px; font-weight: 900; color: #fff; }
.stp.one { left: 318px; background: linear-gradient(160deg, #ffffff 0%, #ffe3ec 100%); color: #b4122f; }
.stp.one svg { width: 44px; height: 44px; fill: none; stroke: #b4122f; stroke-width: 3.2; stroke-linecap: round; stroke-linejoin: round; }
.stp.two { left: 518px; box-shadow: inset 0 0 0 4px rgba(255,255,255,0.5); }
.stp.two .on { position: absolute; inset: 0; border-radius: 50%;
  background: linear-gradient(165deg, #ff7aa4 0%, #e0204b 50%, #8d0d24 100%);
  box-shadow: inset 0 2px 1px rgba(255,255,255,0.5), 0 0 30px rgba(255,110,156,0.6); }
.stp.two span { position: relative; }
#g14ln { position: absolute; left: 402px; top: 50px; width: 116px; height: 6px; border-radius: 3px;
  background: rgba(255,255,255,0.35); }
#g14ln i { position: absolute; inset: 0; border-radius: 3px; background: #ff8ab0; transform-origin: 0 50%; }
#g14b { left: 36px; right: auto; top: 83px; font-size: 34px; line-height: 42px; padding: 20px 26px 18px 30px; }
#g14b .mt { font-size: 22px; }
#g14b .rim { position: absolute; inset: -6px; border-radius: 40px 40px 16px 40px;
  box-shadow: 0 0 0 4px #ffb3c9, 0 0 34px rgba(255,110,156,0.75); opacity: 0; visibility: hidden; }
.bolt { position: absolute; width: 66px; height: 66px; border-radius: 50%; z-index: 3;
  background: linear-gradient(160deg, #ffffff 0%, #ffe3ec 100%); color: #d0194a;
  display: flex; align-items: center; justify-content: center; box-shadow: 0 12px 24px -10px rgba(60,4,18,0.65); }
.bolt .gf { width: 40px; height: 40px; }
#g14bt { left: 10px; top: 52px; }
#g14cab { position: absolute; left: 0; top: 0; width: 920px; height: 250px; overflow: visible; }
#g14bot { left: 740px; top: 50px; width: 150px; height: 150px; }
#g14bot .gf { position: relative; z-index: 1; width: 54%; height: 54%; color: #17141c; }
#g14av { left: 740px; top: 50px; width: 150px; height: 150px; border-radius: 50%;
  background: url("assets/avatar.jpg") center / cover no-repeat;
  box-shadow: 0 0 0 4px rgba(255,255,255,0.75), 0 26px 50px -20px rgba(20,2,8,0.7); }
#g14r { left: 740px; top: 50px; width: 150px; height: 150px; }
""")


@beat
def b14_trigger():
    """«Але другий крок цікавіший. Це саме повідомлення можна підключити як
    тригер до чат-бота на своєму персональному акаунті.»

    NEAR, above her head (shot 2 frames her a little higher: head top ~490).
    A step pair 1 ✓ — 2, the 2 lighting on «другий». On «Це саме
    повідомлення» the pair gives way to the same bubble she just sent,
    «Привіт! Хочу на Мадейру!»; «тригер» — a bolt clips onto it and it rims
    pink; «чат-бота» — a bot tile, a cable, a packet; «на своєму персональному
    акаунті» — her own avatar takes the bot's seat and the bot shrinks into a
    badge on it. The takeover (b15) irises out of her avatar."""
    html = fill(u'''
      <div class="g full" id="g14">
        <div class="dglass edge abs hide" id="g14s">
          <div class="cx" id="g14st">
            <i id="g14ln"><i id="g14lf"></i></i>
            <div class="stp one" id="g14s1"><svg viewBox="0 0 24 24"><path d="M5.5 12.5l4 4 9-9.5"/></svg></div>
            <div class="stp two" id="g14s2"><i class="on" id="g14s2on"></i><span>2</span></div>
          </div>
          <svg class="cab" id="g14cab" viewBox="0 0 920 250">
            <path class="tube" id="g14cT" d="M 632 125 C 670 125 700 125 740 125"/>
            <path class="core" id="g14cC" d="M 632 125 C 670 125 700 125 740 125"/>
            <g class="pkg"><path class="pkt" id="g14cP" d="M 632 125 C 670 125 700 125 740 125"/></g>
          </svg>
          <div class="bo hide" id="g14b"><i class="rim" id="g14rim"></i>Привіт! Хочу на Мадейру!<span class="mt">14:05 {{tk}}</span></div>
          <div class="bolt hide" id="g14bt">{{bolt}}</div>
          <div class="sqring abs" id="g14r"></div>
          <div class="abs hide" id="g14av"></div>
          <div class="abs hide" id="g14bot"><div class="pearl">{{bot}}</div></div>
          <div class="sheen"></div>
        </div>
      </div>''', tk=ticks("g14tk").replace('class="t2"', 'class="t2" style="opacity:1"'),
                bolt=fl("bolt"), bot=fl("bot"))
    src = js('''
  tl.set("#g14", {autoAlpha: 1}, @t_in);
  arr("#g14s", @t_in, {s: 0.8, y: 24});
  tl.fromTo(["#g14s1", "#g14s2"], {autoAlpha: 0, scale: 0.4}, {autoAlpha: 1, scale: 1, duration: 0.55, ease: POP, stagger: 0.1}, @t_st);
  gsap.set("#g14lf", {scaleX: 0});
  gsap.set("#g14s2on", {autoAlpha: 0});
  // «другий»
  tl.to("#g14lf", {scaleX: 1, duration: 0.3, ease: "power2.out"}, @t_ln);
  tl.to("#g14s2on", {autoAlpha: 1, duration: 0.25}, @druhyi);
  G.bump("#g14s2", @druhyi);
  // «цікавіший»
  shn("#g14s .sheen", @tsikav);
  // «Це саме повідомлення»
  bout("#g14st", @t_st2, 10, 0.28);
  bin("#g14b", @t_b, 12, 0.36);
  tl.fromTo("#g14b", {scale: 0.7, y: 30}, {scale: 1, y: 0, duration: 0.8, ease: POP, immediateRender: false}, @t_b);
  // «тригер»
  tl.fromTo("#g14bt", {autoAlpha: 0, scale: 0.2, rotation: -30}, {autoAlpha: 1, scale: 1, rotation: 0, duration: 0.6, ease: POP, immediateRender: false}, @t_tr);
  tl.fromTo("#g14rim", {autoAlpha: 0}, {autoAlpha: 1, duration: 0.3, immediateRender: false}, @tryger);
  // «до чат-бота»
  arr("#g14bot", @t_bot, {s: 0.5, x: 30, y: 0});
  tl.fromTo("#g14bot .gf", {scale: 0.5, autoAlpha: 0}, {scale: 1, autoAlpha: 1, duration: 0.5, ease: SP}, @t_bot2);
  G.drawPrep("g14cT"); G.drawPrep("g14cC"); gsap.set("#g14cP", {autoAlpha: 0});
  tl.to(["#g14cT", "#g14cC"], {strokeDashoffset: 0, duration: 0.4, ease: "power2.inOut"}, @t_cab);
  G.packet("g14cP", @t_pk, 0.45);
  G.bump("#g14bot", @t_pk2);
  // «на своєму персональному акаунті» — her avatar takes the seat, the bot becomes its badge
  tl.fromTo("#g14av", {autoAlpha: 0, scale: 0.6}, {autoAlpha: 1, scale: 1, duration: 0.7, ease: POP, immediateRender: false}, @t_av);
  tl.to("#g14bot", {x: 60, y: 60, scale: 0.42, duration: 0.6, ease: SP}, @t_av);
  G.ripple("#g14r", @t_av2);
  G.packet("g14cP", @t_pk3, 0.45);
  bout("#g14s", @t_out, 10, 0.3);
  tl.set("#g14", {autoAlpha: 0}, @t_off);''',
             t_in=T["ale"] - 0.08, t_st=T["ale"] + 0.04, t_ln=T["druhyi"] - 0.20,
             t_st2=T["tse2"] - 0.16, t_b=T["tse2"] - 0.04, t_tr=T["tryger"] - 0.04,
             t_bot=T["chatbota"] - 0.06, t_bot2=T["chatbota"] + 0.06, t_cab=T["chatbota"] + 0.10,
             t_pk=T["chatbota"] + 0.40, t_pk2=T["chatbota"] + 0.84, t_av=T["person"] - 0.04,
             t_av2=T["person"] + 0.30, t_pk3=T["akaunti_e"] - 0.60,
             t_out=T["tobto"] - 0.22, t_off=T["tobto"] + 0.06)
    return html, src


AV14 = (80 + 740 + 75, 110 + 50 + 75)    # her avatar's centre on screen


# =================================================================== b15-b16
k.css(u"""
/* ---- b15-b16 · the travel agency, and its bot ---- */
.typ { width: 120px; height: 76px; padding: 0; display: flex; align-items: center; justify-content: center; gap: 10px; }
.typ i { display: block; width: 14px; height: 14px; border-radius: 50%; background: rgba(23,20,28,0.32); }
.trip { width: 600px; height: 432px; padding: 0; overflow: hidden; }
.trip .img { position: absolute; left: 0; top: 0; width: 600px; height: 236px; }
.trip .plane { position: absolute; left: 480px; top: 34px; width: 60px; height: 60px; color: #fff; }
.trip .plane .gf { width: 60px; height: 60px; transform: rotate(62deg); }
.trip .tt { position: absolute; left: 28px; top: 254px; font-size: 38px; font-weight: 700; letter-spacing: -0.015em; }
.trip .ts { position: absolute; left: 28px; top: 302px; font-size: 24px; font-weight: 500; color: rgba(23,20,28,0.46); }
.trip .pdf { position: absolute; left: 28px; top: 346px; width: 544px; height: 64px; }
.trip .pdf .pi { position: absolute; left: 0; top: 0; width: 64px; height: 64px; border-radius: 16px;
  background: linear-gradient(165deg, #e0204b 0%, #ab112e 60%, #7a0a20 100%); color: #fff;
  font-size: 18px; font-weight: 900; letter-spacing: 0.04em; display: flex; align-items: center; justify-content: center;
  box-shadow: inset 0 2px 1px rgba(255,255,255,0.45); }
.trip .pdf b { position: absolute; left: 82px; top: 2px; font-size: 26px; font-weight: 700; white-space: nowrap; }
.trip .pdf span { position: absolute; left: 82px; top: 36px; font-size: 22px; font-weight: 700; color: #d0194a; }
.kbd { position: absolute; left: 26px; width: 600px; height: 64px; display: flex; gap: 12px; }
.kbd div { flex: 1; border-radius: 20px; background: rgba(180,18,47,0.10); color: #b4122f;
  display: flex; align-items: center; justify-content: center; font-size: 25px; font-weight: 700;
  box-shadow: inset 0 0 0 1.5px rgba(180,18,47,0.12); }
#c3M .bolt { left: -20px; top: -24px; width: 58px; height: 58px; }
#c3M .bolt .gf { width: 34px; height: 34px; }
#c3M .rim { position: absolute; inset: -6px; border-radius: 40px 40px 16px 40px;
  box-shadow: 0 0 0 4px #ff8ab0, 0 0 30px rgba(255,110,156,0.6); opacity: 0; visibility: hidden; }
#c3nm { display: inline-block; }
""")

TRIP_IMG = u'''<svg class="img" viewBox="0 0 600 236" preserveAspectRatio="none">
  <defs><linearGradient id="c3sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffe1ea"/><stop offset="1" stop-color="#ff9dbb"/></linearGradient>
  <linearGradient id="c3sea" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#c4143a"/><stop offset="1" stop-color="#5e071a"/></linearGradient></defs>
  <rect width="600" height="236" fill="url(#c3sky)"/>
  <circle cx="36" cy="178" r="9" fill="#fff"/>
  <path d="M170 196 C 210 150 250 120 300 104 C 340 92 372 112 398 130 C 430 150 470 170 520 196 Z" fill="#8d0d24"/>
  <path d="M250 196 C 280 160 318 142 350 150 C 378 158 400 176 420 196 Z" fill="#6b081c"/>
  <rect y="190" width="600" height="46" fill="url(#c3sea)"/>
  <path id="c3rt" d="M 36 178 C 140 30 380 10 506 70" fill="none" stroke="#fff" stroke-width="6" stroke-linecap="round" opacity="0.9"/>
</svg>'''


@beat
def b15_madeira_bot():
    """«Тобто, умовно, в тебе, не знаю, турагенція, людина пише «вітаю, мене
    цікавить подорож на Мадейру» — і бот одразу розпізнає це повідомлення і
    починає надсилати деталі про подорож»

    OVER. The iris opens out of her avatar: the same white chat, now with a
    travel agency, its name landing on «турагенція» (blackout). «людина
    пише» — the field types her quote as she says it (blackout — it is on
    screen), sent on «і бот». The bot is typing at once; «розпізнає» — the
    bolt from b14 clips onto the message; «починає надсилати» — the typing
    turns into a trip card: Madeira at sunset, a flight line drawn on
    «надсилати», the programme PDF on «деталі», two buttons on «подорож». No
    prices anywhere — none were given."""
    q = u"Вітаю, мене цікавить подорож на Мадейру"
    TYPE["c3"] = [[T["vitayu"] - 0.04, T["mad_e"] - 0.10, q, "type"],
                  [T["mad_e"] + 0.10, T["mad_e"] + 0.10, u"", "set"]]
    body = fill(u'''
            <div class="bo hide" id="c3M" style="bottom:36px"><i class="rim" id="c3rim"></i><div class="bolt hide" id="c3bt">{{bolt}}</div>{{q}}<span class="mt">09:41 {{tk}}</span></div>
            <div class="bi typ hide" id="c3ty" style="bottom:36px"><i></i><i></i><i></i></div>
            <div class="bi trip hide" id="c3cd" style="bottom:112px">{{img}}
              <div class="plane hide" id="c3pl">{{plane}}</div>
              <div class="tt">Мадейра</div><div class="ts">Португалія · програма туру</div>
              <div class="pdf hide" id="c3pdf"><div class="pi">PDF</div><b>Мадейра — програма.pdf</b><span>Відкрити</span></div>
            </div>
            <div class="kbd hide" id="c3kb" style="bottom:36px"><div>Обрати дати</div><div>Готелі</div></div>''',
                bolt=fl("bolt"), q=q, tk=ticks("c3Tk"), img=TRIP_IMG, plane=fl("plane"))
    name = u'<span id="c3nm">Турагенція</span>'
    html = fill(u'''
      <div class="g full" id="g15">
        {{tk}}
      </div>''', tk=takeover("tk15", chat_html("c3", name, u"<b>●</b> онлайн", fl("plane"), body)))
    src = js('''
  tl.set("#g15", {autoAlpha: 1}, @t_iris);
  G.irisOpen("#tk15", @t_iris, @ax, @ay, 0.85);
  drift1("#tk15", @t_iris, 10.5);
  bin("#c3W", @t_sheet, 16, 0.42);
  tl.fromTo("#c3W", {scale: 0.3, x: @ox, y: @oy}, {scale: 1, x: 0, y: 0, duration: 1.0, ease: spring(0.72, 12)}, @t_sheet);
  tl.fromTo("#c3 .chh > *", {autoAlpha: 0, y: 10}, {autoAlpha: 1, y: 0, duration: 0.5, ease: SP, stagger: 0.05}, @t_hd);
  // «турагенція» — its name lands
  gsap.set("#c3nm", {autoAlpha: 0});
  tl.fromTo("#c3nm", {autoAlpha: 0, x: -12}, {autoAlpha: 1, x: 0, duration: 0.45, ease: SP, immediateRender: false}, @t_nm);
  // «людина пише «…»» — the field lights, typed as she says it; sent on «і бот»
  tl.fromTo("#c3Rim", {autoAlpha: 0, scale: 1.04}, {autoAlpha: 1, scale: 1, duration: 0.45, ease: SP, immediateRender: false}, @t_rim);
  tl.to("#c3Rim", {autoAlpha: 0, duration: 0.25}, @t_rim2);
  sendBubble("#c3M", "#c3Go", @t_send);
  tl.to("#c3Tk", {opacity: 1, duration: 0.12}, @t_read);
  // «бот одразу» — typing at once
  tl.to("#c3M", {y: -94, duration: 0.5, ease: SP}, @t_ty);
  tl.fromTo("#c3ty", {autoAlpha: 0, scale: 0.6, transformOrigin: "0% 100%"}, {autoAlpha: 1, scale: 1, duration: 0.45, ease: POP, immediateRender: false}, @t_ty);
  tl.to("#c3ty i", {keyframes: {y: [0, -9, 0]}, duration: 0.42, ease: "sine.inOut", stagger: 0.12, repeat: 3}, @t_ty2);
  // «розпізнає» — the trigger fires
  tl.fromTo("#c3bt", {autoAlpha: 0, scale: 0.2, rotation: -30}, {autoAlpha: 1, scale: 1, rotation: 0, duration: 0.55, ease: POP, immediateRender: false}, @t_rz);
  tl.fromTo("#c3rim", {autoAlpha: 0}, {autoAlpha: 1, duration: 0.3, immediateRender: false}, @rozpiz);
  G.bump("#c3M", @t_rz2);
  // «починає надсилати» — the answer arrives: the trip
  tl.to("#c3ty", {autoAlpha: 0, scale: 0.7, duration: 0.2, ease: "power2.in"}, @t_cd0);
  tl.to("#c3M", {y: -526, duration: 0.7, ease: SP}, @t_cd0);
  tl.fromTo("#c3cd", {autoAlpha: 0, scale: 0.4, transformOrigin: "0% 100%"}, {autoAlpha: 1, scale: 1, duration: 0.8, ease: spring(0.7, 12), immediateRender: false}, @t_cd);
  G.draw("c3rt", @nadsyl, 0.6);
  tl.fromTo("#c3pl", {autoAlpha: 0, scale: 0.4}, {autoAlpha: 1, scale: 1, duration: 0.5, ease: POP, immediateRender: false}, @t_pl);
  // «деталі»
  tl.fromTo("#c3pdf", {autoAlpha: 0, y: 14}, {autoAlpha: 1, y: 0, duration: 0.45, ease: SP, immediateRender: false}, @t_pdf);
  // «подорож»
  tl.fromTo("#c3kb", {autoAlpha: 0, y: 16}, {autoAlpha: 1, y: 0, duration: 0.45, ease: SP, immediateRender: false}, @t_kb);
  shn("#c3 > .sheen", @t_kb2);
  // «поки твій менеджер» — the chat closes onto the manager (b17)
  tl.to("#c3W", {scale: 0.3, y: -330, duration: 0.45, ease: "power3.in"}, @t_out);
  bout("#c3W", @t_out2, 12, 0.24);
  G.irisClose("#tk15", @t_out, 540, 336, 0.55);
  tl.set("#g15", {autoAlpha: 0}, @t_off);''',
             t_iris=T["tobto"] - 0.10, ax=AV14[0], ay=AV14[1], t_sheet=T["tobto"] + 0.02,
             ox=AV14[0] - 540, oy=AV14[1] - 681, t_hd=T["umovno"] - 0.10, t_nm=T["turag"] - 0.04,
             t_rim=T["pyshe"] - 0.06, t_rim2=T["mad_e"] - 0.05,
             t_send=T["mad_e"] + 0.10, t_read=T["mad_e"] + 0.50, t_ty=T["bot"] + 0.02,
             t_ty2=T["bot"] + 0.30, t_rz=T["rozpiz"] - 0.04, t_rz2=T["rozpiz"] + 0.20,
             t_cd0=T["pochyn"] - 0.08, t_cd=T["pochyn"], t_pl=T["nadsyl"] + 0.52,
             t_pdf=T["detali"] - 0.04, t_kb=T["podorozh"] - 0.04, t_kb2=T["podorozh"] + 0.20,
             t_out=T["poky"] + 0.02, t_out2=T["poky"] + 0.24, t_off=T["poky"] + 0.60)
    return html, src


# ======================================================================= b17
k.css(u"""
/* ---- b17 · the manager, still over her coffee ---- */
#g17s { left: 230px; top: 262px; width: 620px; height: 164px; border-radius: 82px; overflow: hidden; }
#g17cup { left: 22px; top: 22px; width: 120px; height: 120px; }
#g17cup .gy { position: relative; z-index: 1; width: 56%; height: 56%; color: #17141c; stroke-width: 1.9; margin-top: 26%; }
#g17stm { position: absolute; left: 0; top: 4px; width: 120px; height: 46px; overflow: visible; z-index: 2; }
#g17stm path { fill: none; stroke: #d0194a; stroke-width: 5; stroke-linecap: round; }
#g17av { left: 168px; top: 38px; width: 88px; height: 88px; border-radius: 50%; color: #fff;
  background: linear-gradient(165deg, #ff7aa4 0%, #e0204b 50%, #8d0d24 100%);
  display: flex; align-items: center; justify-content: center; box-shadow: inset 0 2px 1px rgba(255,255,255,0.45); }
#g17av .gf { width: 52px; height: 52px; }
#g17nm { left: 278px; top: 36px; font-size: 34px; font-weight: 700; letter-spacing: -0.01em; color: #fff; }
#g17st { left: 278px; top: 84px; width: 320px; height: 40px; }
#g17st span { position: absolute; left: 0; top: 0; white-space: nowrap; font-size: 27px; font-weight: 500; color: rgba(255,255,255,0.72); }
#g17st b { color: #ff8ab0; }
""")


@beat
def b17_coffee():
    """«поки твій менеджер ще доп'є каву і підійде до телефону.»

    NEAR. The chat closes onto a glass capsule: «Менеджер», last seen
    «був(ла) нещодавно» (blackout on «менеджер», the capsule says it). A cup
    lands on «доп'є каву» and steams; on «телефону» the status finally flips
    to online — the bot answered minutes ago."""
    html = fill(u'''
      <div class="g full" id="g17">
        <div class="dglass edge abs hide" id="g17s">
          <div class="cx" id="g17cup"><div class="pearl">{{cup}}</div>
            <svg id="g17stm" viewBox="0 0 120 46"><path id="g17s1" d="M50 42 C 42 32 58 24 50 10"/><path id="g17s2" d="M70 42 C 62 32 78 24 70 10"/></svg></div>
          <div class="cx" id="g17av">{{person}}</div>
          <div class="cx" id="g17nm">Менеджер</div>
          <div class="cx" id="g17st"><span id="g17a">був(ла) нещодавно</span><span id="g17b"><b>●</b> онлайн</span></div>
          <div class="sheen"></div>
        </div>
      </div>''', cup=gl("cup"), person=fl("person"))
    src = js('''
  tl.set("#g17", {autoAlpha: 1}, @t_in);
  gsap.set(["#g17b", "#g17cup"], {autoAlpha: 0});
  arr("#g17s", @t_in, {s: 0.4, y: 0});
  tl.fromTo(["#g17av", "#g17nm", "#g17st"], {autoAlpha: 0, x: -12}, {autoAlpha: 1, x: 0, duration: 0.5, ease: SP, stagger: 0.06}, @t_in2);
  // «доп'є каву»
  tl.fromTo("#g17cup", {autoAlpha: 0, scale: 0.4, rotation: -14}, {autoAlpha: 1, scale: 1, rotation: 0, duration: 0.6, ease: POP, immediateRender: false}, @t_cup);
  G.drawPrep("g17s1"); G.drawPrep("g17s2");
  tl.to(["#g17s1", "#g17s2"], {strokeDashoffset: 0, duration: 0.5, ease: "power2.out", stagger: 0.12}, @kavu);
  tl.to(["#g17s1", "#g17s2"], {autoAlpha: 0, y: -14, duration: 0.5, ease: "power1.in", stagger: 0.12}, @t_stm2);
  tl.to("#g17cup", {rotation: -10, duration: 0.3, ease: "sine.inOut"}, @pidiyde);
  tl.to("#g17cup", {rotation: 0, duration: 0.5, ease: SP}, @t_sip2);
  // «до телефону» — online, finally
  tl.to("#g17a", {autoAlpha: 0, y: -10, duration: 0.2, ease: "power2.in"}, @t_on);
  tl.fromTo("#g17b", {autoAlpha: 0, y: 12}, {autoAlpha: 1, y: 0, duration: 0.45, ease: SP, immediateRender: false}, @t_on2);
  G.bump("#g17av", @t_on2);
  shn("#g17s .sheen", @t_on2);
  bout("#g17s", @t_out, 10, 0.28);
  tl.set("#g17", {autoAlpha: 0}, @t_off);''',
             t_in=T["poky"] + 0.34, t_in2=T["poky"] + 0.46, t_cup=T["dopye"] - 0.06,
             t_stm2=T["kavu"] + 0.62, t_sip2=T["pidiyde"] + 0.30, t_on=T["telef"] - 0.04,
             t_on2=T["telef"] + 0.12, t_out=T["yakshcho"] - 0.34, t_off=T["yakshcho"] - 0.04)
    return html, src


# ======================================================================= b18
k.css(u"""
/* ---- b18 · Follow (reel 13's button) ---- */
#g18s { left: 170px; top: 286px; width: 740px; height: 140px; border-radius: 70px; overflow: hidden; }
#g18av { left: 22px; top: 22px; width: 96px; height: 96px; border-radius: 50%;
  background: url("assets/avatar.jpg") center / cover no-repeat; box-shadow: 0 0 0 3px rgba(255,255,255,0.7); }
#g18nm { left: 138px; top: 30px; font-size: 36px; font-weight: 700; letter-spacing: -0.01em; color: #fff; }
#g18sb { left: 138px; top: 78px; font-size: 24px; font-weight: 500; color: rgba(255,255,255,0.7); white-space: nowrap; }
.flw { position: absolute; }
.fla, .flb { position: absolute; inset: 0; border-radius: 999px; display: flex; align-items: center;
  justify-content: center; gap: 10px; font-size: 31px; font-weight: 700; letter-spacing: -0.01em; }
.fla { color: #fff; background: linear-gradient(165deg, #e0204b 0%, #ab112e 46%, #6b081c 100%);
  box-shadow: inset 0 2px 1px rgba(255,255,255,0.5), inset 0 -16px 26px -12px rgba(255,125,165,0.6),
              0 22px 40px -16px rgba(70,4,20,0.7); }
.flb { color: #17141c; font-size: 28px; background: linear-gradient(160deg, #ffffff 0%, #fff5f8 52%, #f5dfe6 100%);
  box-shadow: inset 0 2px 1px #fff, 0 22px 40px -16px rgba(30,4,12,0.6); }
.flb svg { width: 30px; height: 30px; fill: none; stroke: #b4122f; stroke-width: 3; stroke-linecap: round; stroke-linejoin: round; }
""")


@beat
def b18_follow():
    """«Якщо було корисно, то обов'язково підпишись»

    NEAR. Her capsule — avatar, «Рута», «технічна продюсерка» (her own
    Telegram title) — with the Follow button, pressed on «підпишись»:
    Стежити -> Відстежується. The reel ends on it."""
    html = u'''
      <div class="g full" id="g18">
        <div class="dglass edge abs hide" id="g18s">
          <div class="cx" id="g18av"></div>
          <div class="cx" id="g18nm">Рута</div>
          <div class="cx" id="g18sb">технічна продюсерка</div>
          <div class="flw" id="flw" style="left:444px;top:32px;width:274px;height:76px">
            <div class="fla" id="flwA">Стежити</div>
            <div class="flb hide" id="flwB"><svg viewBox="0 0 24 24"><path id="flwK" d="M5.5 12.5l4 4 9-9.5"/></svg>Відстежується</div>
          </div>
          <div class="sheen"></div>
        </div>
      </div>'''
    src = js('''
  tl.set("#g18", {autoAlpha: 1}, @t_in);
  arr("#g18s", @t_in, {s: 0.7, y: 24});
  tl.fromTo(["#g18av", "#g18nm", "#g18sb"], {autoAlpha: 0, x: -12}, {autoAlpha: 1, x: 0, duration: 0.5, ease: SP, stagger: 0.06}, @t_in2);
  tl.fromTo("#flw", {autoAlpha: 0, scale: 0.6}, {autoAlpha: 1, scale: 1, duration: 0.6, ease: POP}, @korysno);
  shn("#g18s .sheen", @obov);
  // «підпишись»
  press("#flw", @pidpys);
  tl.set("#flwB", {autoAlpha: 1}, @t_p);
  tl.set("#flwA", {autoAlpha: 0}, @t_p);
  G.draw("flwK", @t_p, 0.3);''', t_in=T["yakshcho"] - 0.02, t_in2=T["yakshcho"] + 0.10, t_p=T["pidpys"] + 0.09)
    return html, src


# ---------------------------------------------------------------------------
# Captions drop only on redundancy (STYLE.md §2b.1): where a graphic's own
# text says the word she is saying at that moment. Spans under SHORT drop the
# caption but keep the plaque — dropping the plaque for one word reads as a
# blink. Kept on purpose: her quote «доброго дня, мене цікавить те й те» over
# the recording (it types a different example, «Привіт! Хочу на Мадейру!»),
# and «Telegram Бізнес» / «посилання на розмову» (her UI is in English).
def _bo(k0, k1, why):
    return (round(T[k0] - 0.01, 3), round(T[k1] + 0.01, 3), why)


BLACKOUT = [
    _bo("napys", "tg1_e", u"b01 — the button reads «Написати в Telegram»"),
    _bo("men1", "men1_e", u"b02 — the chat header reads «Менеджер»"),
    _bo("dva", "razy_e", u"b06 — the chip reads ×2"),
    _bo("tg2", "prem_e", u"b07 — the label reads «Telegram Premium»"),
    _bo("kop", "kop_e", u"b07 — the chip reads «копійки»"),
    _bo("turag", "turag_e", u"b15 — the header reads «Турагенція»"),
    _bo("vitayu", "mad_e", u"b15 — the field types her quote"),
    (round(T["men3"] - 0.01, 3), round(E(u"менеджер", 65.30) + 0.01, 3), u"b17 — the capsule reads «Менеджер»"),
]
INVERT = []
SHORT = 1.3

HEAD_JS = r"""
  var G = helpers(tl);
  function bin(sel, t, b, d) { d = d || 0.38; G.blurIn(sel, t, b || 12, d); tl.set(sel, {filter: "none"}, t + d + 0.01); }
  function bout(sel, t, b, d) { d = d || 0.32; G.blurOut(sel, t, b || 10, d); tl.set(sel, {filter: "none"}, t + d + 0.01); }
  function arr(sel, t, o) {
    o = o || {};
    bin(sel, t, o.blur || 12, 0.36);
    tl.fromTo(sel, {scale: o.s == null ? 0.5 : o.s, x: o.x || 0, y: o.y == null ? 34 : o.y},
              {scale: 1, x: 0, y: 0, duration: o.d || 0.85, ease: o.ease || POP, immediateRender: false}, t);
  }
  function shn(sel, t) {
    tl.fromTo(sel, {xPercent: -120}, {xPercent: 120, duration: 0.8, ease: "power2.inOut", immediateRender: false}, t);
  }
  function press(sel, t) {
    tl.to(sel, {scale: 0.9, duration: 0.09, ease: "power2.out"}, t);
    tl.to(sel, {scale: 1, duration: 0.45, ease: POP}, t + 0.09);
  }
  function tapAt(sel, t) {
    tl.fromTo(sel + " .td", {autoAlpha: 0.95, scale: 0.35}, {autoAlpha: 0, scale: 1.1, duration: 0.6, ease: "power2.out", immediateRender: false}, t);
    tl.fromTo(sel + " .tr", {autoAlpha: 1, scale: 0.3}, {autoAlpha: 0, scale: 1.5, duration: 0.7, ease: "power2.out", immediateRender: false}, t);
  }
  function sendBubble(sel, go, t) {
    tl.to(go, {scale: 0.86, duration: 0.08, ease: "power2.out"}, t - 0.08);
    tl.to(go, {scale: 1, duration: 0.4, ease: POP}, t);
    tl.fromTo(sel, {autoAlpha: 0, y: 110, scale: 0.86, transformOrigin: "100% 100%"},
              {autoAlpha: 1, y: 0, scale: 1, duration: 0.6, ease: SP, immediateRender: false}, t);
  }
  function drift1(sel, t, d) { tl.fromTo(sel + " .aurs", {x: 0, y: 0}, {x: -110, y: 70, duration: d, ease: "sine.inOut"}, t); }
  gsap.set(".sheen", {xPercent: -120});
"""


def paint_js():
    return (u"""
  var TY = %s, CLOCK = %s;
  var CN = {}, CV = {};
  function put(id, s) { if (CN[id] !== s) { CN[id] = s; document.getElementById(id).textContent = s; } }
  function op(id, v) { if (CV[id] !== v) { CV[id] = v; document.getElementById(id).style.opacity = v; } }
  function typed(segs, t) {
    var s = "";
    for (var i = 0; i < segs.length; i++) {
      var q = segs[i];
      if (t < q[0]) break;
      var p = q[1] > q[0] ? Math.min(1, (t - q[0]) / (q[1] - q[0])) : 1, n = q[2].length;
      if (q[3] === "type") s = q[2].slice(0, Math.round(p * n));
      else if (q[3] === "del") s = q[2].slice(0, Math.round((1 - p) * n));
      else s = q[2];
    }
    return s;
  }
  function paint(t) {
    for (var p in TY) {
      var segs = TY[p], s = typed(segs, t), busy = false;
      for (var i = 0; i < segs.length; i++) if (t >= segs[i][0] && t < segs[i][1] + 0.3) busy = true;
      put(p + "T", s);
      op(p + "P", s ? 0 : 1);
      op(p + "C", busy || Math.floor(t * 1.9) %% 2 === 0 ? 1 : 0);
      op(p + "Mic", s ? 0 : 1);
      op(p + "Go", s ? 1 : 0);
    }
    var m = 2 + Math.round(60 * Math.min(1, Math.max(0, (t - CLOCK[0]) / CLOCK[1])));
    put("c1Clk", (14 + Math.floor(m / 60)) + ":" + ("0" + (m %% 60)).slice(-2));
  }
  var CLK = {t: 0};
  paint(0);
  tl.fromTo(CLK, {t: 0}, {t: %.3f, duration: %.3f, ease: "none", onUpdate: function () { paint(CLK.t); }}, 0);"""
            % (json.dumps(TYPE, ensure_ascii=False), json.dumps(CLOCK), DUR, DUR))


def main():
    gh, gj = [], []
    for fn in BEATS:
        h, j = fn()
        gh.append(h.rstrip())
        gj.append("  /* %s */" % fn.__name__)
        gj.append(j.rstrip())

    long_bo = [b for b in BLACKOUT if b[1] - b[0] >= SHORT]
    short_bo = [b for b in BLACKOUT if b[1] - b[0] < SHORT]
    caps = [c for c in CAPS if not any(a <= c["s"] < b for a, b, _ in short_bo)]

    # the slow push on the plate (§0.8): her and her matte move as one
    head = [g.js(), HEAD_JS, paint_js(),
            '  gsap.set(["#vid", ".matte"], {transformOrigin: "540px 820px"});',
            '  tl.fromTo(["#vid", ".matte"], {scale: 1}, {scale: 1.045, duration: %.3f, '
            'ease: "none"}, 0);' % DUR]
    doc = k.document(
        title=u"Reel 18 — Telegram Business",
        plate="assets/base.mp4",
        gfx_html=g.defs() + "\n" + "\n".join(gh),
        gfx_js="\n".join(head + gj),
        caps=caps,
        blackout=long_bo,
        invert=INVERT,
    )
    out = os.path.join(HERE, "index.html")
    io.open(out, "w", encoding="utf-8").write(doc)
    print("index.html  %d captions, %d beats, %.1f KB"
          % (len(caps), len(BEATS), os.path.getsize(out) / 1024.0))
    for b in BLACKOUT:
        print("  blackout %6.2f-%6.2f  %s" % b)


if __name__ == "__main__":
    main()
