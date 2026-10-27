# -*- coding: utf-8 -*-
"""Reel 41 subtitles: sentence by sentence, calm, low — her ask for the
YouTube cut: *"simple subtitles, sentence by sentence, calm on the bottom, but
not too low otherwise they will be hidden by the YT line"*.

    python work/r41/subs.py      -> work/r41/captions.json (+ prints the lines)

No script exists for this one (it was improvised), so the words are whisper's,
mapped onto the cut's timeline (timeline.json), with her spelling restored
through FIX / TEXT_FIX where whisper misheard.
"""
import io
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
FPS = 30

MAXC = 84          # two calm lines at most

# whisper -> what she said (single tokens)
FIX = {
    "РІОС": "рілс", "РЮС": "рілс", "ріос": "рілс", "ріоси": "рілси", "рюси": "рілси", "Reels": "рілс",
    "середня,": "серпня,", "запасила": "запостила", "Деск": "Диск", "Деск,": "Диск,",
    "Клот.": "Клод.", "клоді.": "Клоді.", "клодом": "Клодом", "клод.": "Клод.",
    "-акенти,": "-агенти,", "голосовій,": "голосове,", "тормалась": "трималась",
    "послати": "постити", "послати,": "постити,", "послала": "постила", "класом": "класно",
    "інстаграму": "Інстаграму", "інстаграм.": "Інстаграм.", "бачило,": "бачили,",
    "машина...": "машина", "Писати": "писати", "напроти...": "напроти", "Вікна?": "вікна",
    "Відкрываю": "Відкриваю", "аналіз.": "аналіз", "Назискаю": "Натискаю", "кавардак.": "кавардак,",
    "піруться": "беруться", "'ять,": "п'ять,", "Потім": "потім", "Тобі": "тобі",
}
# phrase fixes on the joined sentence text: dropped or misheard words
TEXT_FIX = [
    ("перестали набирати", "перестали набирати перегляди."),
    ("нових підписників, я не набирала більше", "нових підписників, я не набирала більше переглядів,"),
    ("і в мені це просто", "і мені це просто"),
    ("Хочу з цих сценарів", "Кожен з цих сценаріїв"),
    ("зняти ці рюси", "зняти ці рілси"),
    ("я зробив аналіз. і підготував", "я зробив аналіз і підготував"),
    ("У нас він файл", "У нас є файл"),
    ("сидячи з ранку в неділя скави", "сидячи зранку в неділю за кавою"),
    ("на код.", "на Code."), ("в чат, в коді.", "в чат, у Code."),
    ("просто беру це відео", "Я просто беру це відео"),
    ("Ой, смирилась.", "Ось мій рілс."),
    ("це все працює просто", "Це все працює просто"),
    ("відео, Так він", "відео, так він"),
    ("максимум те, щоб", "максимум на те, щоб"),
    ("я просто не можу змусити", "Я просто не можу змусити"),
]


def load_words(src):
    f = {"M": "u151122.jsonl", "B": "u152651.jsonl"}[src]
    out = []
    for line in io.open(os.path.join(HERE, f), encoding="utf-8"):
        for w in json.loads(line)["words"]:
            if w["w"]:
                out.append(w)
    return out


def main():
    tl = json.load(io.open(os.path.join(HERE, "timeline.json"), encoding="utf-8"))
    W = {"M": load_words("M"), "B": load_words("B")}
    words = []
    for sp in tl["spans"]:
        if sp["speed"] != 1.0 or sp["tag"] in ("shhh", "wink"):
            continue
        t0 = sp["start"] / FPS
        for w in W[sp["src"]]:
            mid = (w["s"] + w["e"]) / 2
            if sp["a"] <= mid < sp["b"] - 0.03 and "перегляд" not in w["w"]:
                s = t0 + max(0.0, w["s"] - sp["a"])
                e = t0 + min(sp["b"], w["e"]) - sp["a"]
                words.append({"w": FIX.get(w["w"], w["w"]), "s": round(s, 3), "e": round(e, 3),
                              "span": sp["i"]})
    # merge whisper's split tokens («п» + «'ять», «AI» + «-системи»)
    merged = []
    for w in words:
        if merged and (w["w"].startswith("'") or w["w"].startswith("-")) and merged[-1]["span"] == w["span"]:
            merged[-1]["w"] += w["w"]
            merged[-1]["e"] = w["e"]
        else:
            merged.append(dict(w))
    words = merged
    json.dump({"words": words}, io.open(os.path.join(HERE, "words_out.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=0)

    # sentences: an end mark, a jump between spans, or a real pause
    sents, cur = [], []
    for w in words:
        if cur:
            gap = w["s"] - cur[-1]["e"]
            if (w["span"] != cur[-1]["span"] and gap > 0.25) or gap > 0.9:
                sents.append(cur); cur = []
        cur.append(w)
        if re.search(r"[.?!]$", w["w"]):
            sents.append(cur); cur = []
    if cur:
        sents.append(cur)

    def text(ws):
        return " ".join(x["w"] for x in ws)

    def split(ws):
        """a sentence longer than two lines: cut at the comma nearest the middle
        (any word boundary if there is none), recursively"""
        if len(text(ws)) <= MAXC or len(ws) < 4:
            return [ws]
        half = len(text(ws)) / 2.0
        best, bestd = None, 1e9
        for k in range(1, len(ws) - 1):
            pos = len(text(ws[:k + 1]))
            d = abs(pos - half) - (25 if ws[k]["w"].endswith((",", ":", "–", ";")) else 0)
            if d < bestd and len(ws[k + 1:]) >= 2:
                best, bestd = k, d
        return split(ws[:best + 1]) + split(ws[best + 1:])

    lines = []
    for sw in sents:
        for ch in split(sw):
            lines.append({"t": text(ch), "s": ch[0]["s"], "e": ch[-1]["e"]})
    for L in lines:
        for o, n in TEXT_FIX:
            L["t"] = L["t"].replace(o, n)
        L["t"] = re.sub(r"\s+([,.?!])", r"\1", L["t"])
    # hold each line until the next one (a calm read), never more than +0.6 s
    for a, b in zip(lines, lines[1:]):
        a["e"] = round(min(b["s"] - 0.04, max(a["e"] + 0.25, min(a["e"] + 0.6, b["s"] - 0.04))), 3)
    lines[-1]["e"] = round(lines[-1]["e"] + 0.5, 3)
    json.dump({"lines": lines}, io.open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    for i, L in enumerate(lines):
        print("%3d %7.2f %7.2f  %s" % (i, L["s"], L["e"], L["t"]))


if __name__ == "__main__":
    main()


def ass(path_json, path_ass):
    """The same lines as an .ass file, for the plain cut burned in by ffmpeg
    (v1, before the animation pass). Product Sans Bold, white, soft shadow,
    bottom centre with 130 px clear of YouTube's progress bar."""
    lines = json.load(io.open(path_json, encoding="utf-8"))["lines"]

    def ts(t):
        h, r = divmod(max(0.0, t), 3600)
        mnt, sec = divmod(r, 60)
        return "%d:%02d:%05.2f" % (h, mnt, sec)
    head = """[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Sub,Product Sans,50,&H00FFFFFF,&H00FFFFFF,&H64000000,&H8C000000,-1,0,0,0,100,100,0,0,1,2.2,1.6,2,300,300,128,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    ev = ["Dialogue: 0,%s,%s,Sub,,0,0,0,,{\\fad(120,120)\\blur2.5}%s" % (ts(L["s"]), ts(L["e"]), L["t"])
          for L in lines]
    io.open(path_ass, "w", encoding="utf-8").write(head + "\n".join(ev) + "\n")


if __name__ == "__main__" and "--ass" in __import__("sys").argv:
    ass(os.path.join(HERE, "captions.json"), os.path.join(HERE, "captions.ass"))
