# -*- coding: utf-8 -*-
"""Reel 41 — the decision list. Source seconds off u151122.jsonl / u152651.jsonl.

Sources: M = the long take (20261027_151122), S = scrolling b-roll (…152423,
silent), B = the 48 s add-on about not checking the videos (…152651).

Last take wins, as always: every restart drops the earlier attempt.
"""
PI, PO = 0.07, 0.10          # pad around kept speech
_W = []


def W(word, near, end=0):
    """a word's start (or end) in the long take, by its whisper spelling"""
    import io, json, os
    if not _W:
        for line in io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "u151122.jsonl"), encoding="utf-8"):
            _W.extend(json.loads(line)["words"])
    w = min((x for x in _W if x["w"] == word), key=lambda x: abs(x["s"] - near))
    assert abs(w["s"] - near) < 2.0, (word, near, w["s"])
    return w["e"] if end else w["s"]


def m(a, b, **o):
    return ("M", round(a - PI, 3), round(b + PO, 3), o)


def bb(a, b, **o):
    return ("B", round(a - PI, 3), round(b + PO, 3), o)


EDL = [
    # ---- cold open: «shhh», she films the reel on her phone
    ("M", 0.60, 5.00, {"frame": "base", "tag": "shhh"}),
    # ... two seconds into the phone recording it goes fast-forward, black & white
    ("M", 5.00, 27.50, {"speed": 6.0, "bw": True, "frame": "base", "gain": -7, "tag": "fast"}),
    m(137.64, 139.60, frame="in", tag="back"),                  # «Ми до цього ще повернемось.»

    # ---- the problem (her v1 note: keep the business opening, tighten it; the
    # problem part goes by beats only — ideas + the parrot, scripts, editing,
    # a shorter price — without the «it's so hard, skills, knowledge» passages)
    m(154.15, 183.77, tag="hook"),                              # Можливо, це неочікувано … катастрофа.
    m(189.94, 191.98),                                          # Я не можу собі це дозволити.
    m(196.69, 211.41),                                          # … постить раз на місяць.
    m(227.08, 229.62, tag="ideas"),                             # По-перше, тобі треба придумати ідеї для контенту.
    m(230.02, W("постійно.", 236.0, 1)),                        # … я просто папуга … постійно.
    m(248.16, 250.50),                                          # В якийсь момент тебе просто закінчуються ідеї.
    m(250.66, 255.35),                                          # … потім тобі треба написати сценарій.
    m(255.47, 270.99),                                          # А сценарій … щоб воно було цікаво дивитись.
    # 286.3–297.3: three starts of «І навіть якщо тобі вдалося написати…» — the fourth wins
    m(298.11, 305.59),                                          # … хоча б один раз на день, бажано два.
    m(321.27, 322.15),                                          # Але уявимо,
    m(323.25, 325.43),                                          # що ти вирішила постити один раз на день,
    m(326.53, 331.52),                                          # сім сценаріїв … Кожного тижня.
    m(333.33, 344.37),                                          # прописати, зняти, змонтувати … ви це знаєте.
    m(351.47, 355.07, tag="deleg"),                             # А делегувати коштує дорого. Об'єктивно дорого.
    m(359.03, 370.93),                                          # класні анімації … 20-30 євро … на місяць.
    m(371.90, 376.32),                                          # І отримаємо суму 500, 600, аж до 1000 доларів,
    m(403.20, 413.58, tag="vmru"),                              # я просто не можу змусити себе … і я вмру.
    m(414.31, 417.67),                                          # Я не зроблю цього, я просто випаду знову з контенту.
    m(419.95, 433.81, tag="aisys"),                             # … до і після … Як це працює?

    # ---- how it works. 434.7–468: three tries at «все працює в Claude» — the last wins
    m(470.83, 514.44, tag="claude"),                            # це все працює просто в додатку Клод … проглядаю.
    m(515.01, 518.99),                                          # раз, два, три, п'ять, шість, сім.
    m(519.50, 522.00),
    m(524.31, 544.27, tag="strat"),                             # стратегія … ця, ця, ця і ця.
    m(544.66, 588.52, tag="voice"),                             # голосове -> сценарій
    m(588.75, 596.68, tag="monday"),                            # понеділок … камеру напроти...
    m(598.15, 604.65),                                          # вікна? … записати відео.
    m(605.33, 611.19, tag="nomont"),                            # не треба монтувати … монтажеру.
    # 611.4–641.9: «Я заливаю їх на Google Диск» twice, a pause, «Я просто беру посилання» — last wins
    m(642.55, 656.46, tag="upload"),                            # я просто беру це відео … отримую свої відео.

    # ---- her add-on: she doesn't even check them, and they get scheduled
    bb(0.47, 4.67, tag="buffer"),
    bb(5.09, 19.18),                                            # … зняла йому на тиждень,
    # «він просто запощить» -> she corrects it to «запланує»: the correction wins
    bb(21.18, 38.11),

    # ---- the reveal
    m(662.60, 668.34, tag="reveal"),                            # … сказала, що ми до цього повернемось.
    m(674.11, 679.54),                                          # Відкриваю Клод. Заходжу в меню. Натискаю на код.
    ("M", 679.64, 688.55, {"speed": 4.0, "gain": -14}),         # she finds it, fast
    m(688.67, 689.45),                                          # Ось мій рілс.
    # the reel she filmed at the start, now edited, playing on her phone. The
    # camera mirrors, so the phone is flipped back and pushed in to read
    ("M", 701.40, 723.20, {"frame": {"z": 1.25, "cx": 0.56, "cy": 0.55, "flip": True}, "tag": "cta"}),
    # the phone comes down and she winks at the camera — her note: keep it
    ("M", 723.20, 725.30, {"frame": "base", "tag": "wink"}),
]

# b-roll: (source-M time it starts on, length s, source, source in, speed, framing)
FLIP = {"z": 1.10, "cx": 0.5, "cy": 0.5, "flip": True}
BROLL = [
    # the Drive upload, while she explains where the videos go
    (607.09, 4.25, "M", 46.0, 2.0, FLIP),       # не треба монтувати … монтажеру
    (642.55, 3.10, "M", 55.0, 2.0, FLIP),       # я просто беру це відео, заливаю на Google Диск
    (645.70, 1.70, "M", 85.0, 1.5, FLIP),       # беру посилання Google Диск
    (647.42, 2.10, "M", 133.0, 1.2, FLIP),      # і вставляю їх в чат, в коді
    # the Sunday analysis and ideas, scrolled on her phone
    (489.86, 5.70, "S", 0.3, 1.0, FLIP),        # Я відкриваю цей чат. Він мені каже …
    (495.56, 10.5, "S", 43.0, 1.1, FLIP),       # … ось тобі список ідей на цей тиждень
    (578.29, 6.0, "S", 16.0, 1.0, FLIP),        # перетворює на сценарій в моєму стилі …
]

# a punch-in on the lines that land (source-M spans)
CLOSE = [(181.75, 183.87), (412.94, 413.70), (562.4, 563.7)]
