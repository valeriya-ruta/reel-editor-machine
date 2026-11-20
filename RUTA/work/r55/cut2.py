# -*- coding: utf-8 -*-
"""Reel 55 cut v2 — her notes of 2026-10-28 on the first cut.

Built on per-utterance ASR (utt.json / utt_w.json, utt_asr.py): whisper's
whole-take pass drifted up to 2 s on this 5-minute take, which is what made
v1's joins land inside fumbles («на тиждень» twice at 1:46).

Every piece is (take, utterance, first word, last word, the words as she said
them). Takes: b = «Plan w me better» (better-1080.mp4), w = «Plan w me worse»
(worse-1080-12s.mp4, starts at 12.0 s of the take). Spelling is hers — whisper
only supplies the timing.

    python3 cut2.py          -> pieces.json + captions.json   (then mkplate2.py)
"""
import difflib
import json
import re

U = {"b": json.load(open("utt.json")), "w": json.load(open("utt_w.json"))}
SRC = {"b": ("better-1080.mp4", 0.0), "w": ("worse-1080-12s.mp4", 12.0)}

# (take, utt, w0, w1 (inclusive, None = last), text as she said it, framing)
# framing: None = alternate base/in, "in", "punch" (her jokes: NO_PAINT)
P = [
    ("b", 0, 0, 10, u"Зараз ми разом сплануємо контент на тиждень завдяки моєму AI-продюсеру.", "base"),
    # her note: drop the self-intro; the second take's «третій тиждень … два рази на день» instead
    ("w", 4, 0, None, u"Третій тиждень підряд я пощу два", "in"),
    ("w", 5, 0, None, u"рази на день.", None),
    ("w", 6, 0, None, u"І це взагалі без напрягу,", None),
    ("w", 8, 7, None, u"мені просто треба витратити", None),
    ("w", 9, 0, None, u"20 хвилин на те, щоб", None),
    ("w", 10, 0, None, u"придумати ідеї і 20 хвилин на те,", None),
    ("w", 11, 0, None, u"щоб зняти. Все інше:", None),
    ("w", 12, 0, None, u"аналіз, ідеї, монтаж, сценарій, все це", None),
    ("w", 13, 0, 1, u"робить Клод.", None),
    ("b", 1, 6, None, u"І я розробила AI-систему,", None),
    # «яка створює мені контент» out (her note)
    ("b", 3, 0, None, u"яка працює як", None),
    ("b", 4, 0, None, u"повний SMM-ник:", None),
    ("b", 5, 0, None, u"аналізує мій контент, придумує ідеї, монтує мої рілси, дизайнить,", None),
    ("b", 6, 0, None, u"постить", None),
    ("b", 7, 0, None, u"і так по колу кожного тижня.", None),
    ("b", 9, 0, None, u"І мені здається, що люди не дуже розуміють, як це взагалі відбувається, тому що нам кажуть,", None),
    ("b", 10, 0, None, u"там працює агент, там працює скіл, а по факту як це фізично відбувається,", None),
    ("b", 11, 0, None, u"ніхто не розповідає, тому зараз це розповім я.", None),
    ("b", 25, 0, None, u"Отже, перший крок, що він робить, це він аналізує мій контент.", None),
    ("b", 26, 0, None, u"Він аналізує загалом весь масив того контенту, який я запостила,", None),
    ("b", 27, 0, None, u"і особливо звертає увагу на останній тиждень, тому що я люблю тестувати різні теми, формати", None),
    ("b", 28, 0, None, u"і взагалі гіпотези по тижнях.", None),
    ("b", 31, 0, None, u"І він бере інформацію не тільки зі", None),
    ("b", 32, 0, None, u"статистики, а ще й зі сценаріїв.", None),
    ("b", 34, 0, None, u"І на основі цього він може проаналізувати, які гачки найкраще спрацювали, які теми, які формати, заклики до дій і так далі.", None),
    ("b", 35, 0, None, u"Другий етап — це він починає шукати ідеї для наступного контенту.", None),
    ("b", 36, 8, None, u"Він багато бере інформації з моїх консультацій і дзвінків, тому що там мені реально задають питання.", None),
    ("b", 37, 0, None, u"А ще з Threads, тому що я там дуже активна, і там теж класний супер контент.", None),
    ("b", 38, 0, None, u"І поки він це все робить, а це займає хвилин 5–10, я йому пишу свої ідеї.", None),
    ("b", 39, 9, None, u"Наприклад,", None),
    ("b", 40, 0, None, u"цього тижня я хочу показати більше роботи з клієнтами.", None),
    ("b", 44, 0, None, u"Він збирає це докупи і дає мені величезний нумерований список всіх ідей і тем, які він мені пропонує.", None),
    ("b", 45, 0, None, u"Я з цих 30 обираю плюс-мінус 14–15,", None),
    ("b", 46, 0, None, u"після чого він заливає їх в мій додаток Рута.", None),
    ("b", 47, 0, None, u"Я її відкриваю в себе на телефоні", None),
    ("b", 48, 0, None, u"і на кожен зі сценаріїв, де немає тексту,", None),
    ("b", 50, 0, None, u"я записую своє голосове, що я хочу подати на цю тему.", None),
    ("b", 58, 0, None, u"Тобто на 14 сценаріїв на тиждень мені йде десь 15–20 хвилин.", None),
    ("b", 60, 0, None, u"І на цьому все, в принципі, вуаля, в мене є сценарії, вони готові для зйомок.", None),
    ("b", 61, 0, None, u"Після цього я зазвичай на наступний день гарно малююся і одягаюсь.", "punch"),
    ("b", 62, 7, None, u"Знімаю всі ці 14 рілсів", None),
    ("b", 63, 0, None, u"одразу одним масивом,", None),
    ("b", 64, 0, None, u"заливаю ці відео з телефона на Google Диск,", None),
    ("b", 65, 0, None, u"беру посилання на Google Диск", None),
    ("b", 66, 0, None, u"і вставляю в Claude Code.", None),
    # «Клод монтує» had three starts; the last one, whole
    ("b", 70, 0, None, u"І він, Клод, одразу починає їх монтувати в моєму стилі.", None),
    # back in (her note): it makes the courses line make sense
    ("b", 71, 0, None, u"Причому він може монтувати як з комп'ютера, так і з телефона. Я абсолютно не прив'язана ні до чого. Я знаю, що є курси, які кажуть, що", None),
    ("b", 72, 0, None, u"треба обов'язково, щоб комп'ютер був відкритий. Не треба. Вони просто не знають, як це налаштувати на хмарі.", None),
    # «А я знаю» + the hair flip (her note: keep it)
    ("b", 73, 0, None, u"А я знаю.", "punch"),
    ("b", 74, 0, None, u"", "punch"),
    ("b", 75, 0, None, u"І після того, як він змонтував ці рілси, він одразу їх планує по два на день, на вечір,", None),
    ("b", 76, 0, None, u"з годиною між кожним,", None),
    ("b", 77, 0, 4, u"в мій Instagram і TikTok.", None),
    ("b", 78, 0, None, u"Тобто я насправді ці рілси більше не переглядаю, я знаю, що там буде нормально, там будуть субтитри, анімації, все як треба.", None),
    ("b", 96, 0, None, u"От і вся система, і таким чином ми спланували мені контент на цілий", None),
    ("b", 97, 0, None, u"тиждень.", None),
    ("b", 98, 0, None, u"І якщо тобі цікава така система, то в мене є консультація,", None),
    ("b", 99, 0, None, u"в якій ми налаштовуємо це все разом,", None),
    # her note: «вже завтра» stays; only the repeated one at the very end goes
    ("b", 100, 0, 17, u"або налаштування під ключ, де у тебе все буде готове, вже завтра ти можеш вже почати працювати з цим.", None),
    ("b", 101, 0, None, u"Тому, якщо тебе цікавить один із цих варіантів, то", None),
    ("b", 102, 0, None, u"пиши плюс в коментарі, і я тобі напишу.", None),
]

PRE, POST, POST_SENT = 0.07, 0.10, 0.24
FRAMES = {"base": 1.00, "in": 1.10, "punch": 1.45}
MIN_HOLD = 2.6       # a framing holds at least this long before the next step


def norm(w):
    return re.sub(u"[^\\w]", "", w.lower()).replace(u"ї", u"і").replace(u"й", u"и").replace(u"є", u"е")


def edges(take, k, w0, w1, text):
    u = U[take][k]
    ws = u["words"][w0:(w1 + 1) if w1 is not None else None] if u["words"] else []
    a = (ws[0]["s"] if ws and w0 > 0 else u["a"]) - PRE
    b = ws[-1]["e"] if ws and w1 is not None else u["b"]
    if not text:                            # the hair flip: the laugh and its tail
        b = u["b"] + 0.25
    b += POST_SENT if re.search(u"[.!?:]$", text) else POST
    a = max(a, (ws[0]["s"] if ws else u["a"]) - 0.12)
    return u, ws, a, b


ED = [edges(*x[:5]) for x in P]
for i in range(len(P) - 1):                 # neighbours in one take never overlap:
    if P[i][0] == P[i + 1][0]:              # a shared stretch would play twice
        a1 = ED[i + 1][2]
        if ED[i][3] > a1:
            u, ws, a, b = ED[i]
            ED[i] = (u, ws, a, a1 - 0.005)

pieces, caps, t, cur, held = [], [], 0.0, "in", 99.0
for (take, k, w0, w1, text, fr), (u, ws, a, b) in zip(P, ED):
    if fr is None:
        if held >= MIN_HOLD:
            cur, held = ("in" if cur == "base" else "base"), 0.0
        fr = cur
    elif fr != "punch":
        cur, held = fr, 0.0
    src, off = SRC[take]
    d = b - a
    pieces.append({"take": take, "src": src, "a": round(a - off, 3), "b": round(b - off, 3),
                   "t": round(t, 3), "frame": fr, "zoom": FRAMES[fr], "text": text})
    # captions: her words onto whisper's timing inside the piece
    mine = text.split()
    if mine:
        if not ws:
            ws = [{"w": x, "s": a + PRE + i * (d - PRE - POST) / len(mine), "e": 0} for i, x in enumerate(mine)]
        sm = difflib.SequenceMatcher(None, [norm(x) for x in mine], [norm(x["w"]) for x in ws], autojunk=False)
        st = [None] * len(mine)
        for blk in sm.get_matching_blocks():
            for j in range(blk.size):
                st[blk.a + j] = ws[blk.b + j]["s"]
        st[0] = st[0] if st[0] is not None else ws[0]["s"]
        end = ws[-1]["e"] or (a + d - POST)
        # fill gaps by character share between known anchors
        i = 0
        while i < len(mine):
            if st[i] is None:
                j = i
                while j < len(mine) and st[j] is None:
                    j += 1
                lo, hi = st[i - 1], (st[j] if j < len(mine) else end)
                tot = sum(len(x) for x in mine[i - 1:j])
                acc = len(mine[i - 1])
                for q in range(i, j):
                    st[q] = lo + (hi - lo) * acc / float(tot)
                    acc += len(mine[q])
                i = j
            i += 1
        for q, x in enumerate(mine):
            s0 = max(st[q], a + 0.0)
            caps.append({"w": x, "s": round(t + (s0 - a), 3)})
    if fr != "punch":
        held += d
    t += round(d * 30) / 30.0                  # each piece is encoded to whole frames

for c, n in zip(caps, caps[1:]):
    if n["s"] < c["s"] + 0.12:
        n["s"] = round(c["s"] + 0.12, 3)
for c, n in zip(caps, caps[1:]):
    c["e"] = round(min(max(c["s"] + 0.12, n["s"] - 0.085), n["s"] - 0.02), 3)
caps[-1]["e"] = round(t - 0.1, 3)
no_paint = [[p["t"], round(p["t"] + (p["b"] - p["a"]), 3)] for p in pieces if p["frame"] == "punch"]
json.dump(pieces, open("pieces.json", "w"), ensure_ascii=False, indent=0)
json.dump({"words": caps, "no_paint": no_paint}, open("captions.json", "w"), ensure_ascii=False, indent=0)
print("pieces %d  plate %.2f s  words %d  no_paint %s" % (len(pieces), t, len(caps), no_paint))
