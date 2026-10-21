# -*- coding: utf-8 -*-
"""Small bottom subtitles (her ask: "tiny, few words at a time, for
accessibility") from the Whisper words, mapped onto the cut.

    python3 leadmagnet/subs.py   -> leadmagnet/subs.ass

Whisper's spelling of her tech words is fixed by FIX (phrase -> phrase).
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from cut import src_to_out  # noqa: E402

FIX = [
    ("штучним етелектом", "штучним інтелектом"), ("штучний телек", "штучний інтелект"), ("штучного телека", "штучного інтелекту"),
    ("штучний надзинок", "штучний інтелект"), ("штучний телек щитує", "штучний інтелект зчитує"),
    ("в STLMT", "StyleMD"), ("StyleMT", "StyleMD"), ("стайл МД", "StyleMD"), ("StyleMD", "StyleMD"),
    ("ChGPT", "ChatGPT"), ("чат -GPT", "ChatGPT"), ("чат-GPT", "ChatGPT"),
    ("клад -коді", "Claude Code"), ("клад -код", "Claude Code"), ("клад-коді", "Claude Code"), ("клад-код", "Claude Code"),
    ("Хіксфілд", "Higgsfield"), ("опендраутер", "OpenRouter"), ("Біганск", "Behance"), ("польщу", "постю"),
    ("осеменниця", "SMM-ниця"), ("побранштормали", "побрейнштормили"), ("надзайнути", "задизайнити"),
    ("Save Asbot", "SaveAsBot"), ("впромт", "в промт"), ("віду", "відео"), ("Субтитери", "Субтитри"),
    ("кориштя", "звісно"), ("розкриття слайдів", "розкадрування"), ("клієнки", "клієнтки"), ("цілюва", "цільова"),
    ("суперщиткого", "суперчіткого"), ("скімішоти", "скріншоти"), ("облазі", "образі"), ("клонами", "Claude"),
    ("рендерні хмарі", "рендер у хмарі"), ("гідхаб", "GitHub"), ("Reels 'ю", "рілсах"), ("рілосів", "рілсів"),
    ("часини", "частини"), ("субтитру", "субтитри"), ("піта секції", "підсекції"), ("додакові", "додаткові"),
    ("продукт саншрифт", "Product Sans шрифт"), ("дизайн за саме", "дизайнимо саме"), ("Лоремипсум", "Lorem Ipsum"),
    ("різдоріжчі", "роздоріжжі"), ("пожалтуєш", "пошкодуєш"), ("Єтнамі", "В'єтнамі"), ("Джейсоном, Пайтоном", "JSON-ом, Python-ом"),
    ("нанобанани", "Nano Banana"), ("клінг", "Kling"), ("пром.", "промт."), ("цей пром ", "цей промт "),
    (" -", "-"), ("пам 'яті", "пам'яті"), ("комп 'ютер", "комп'ютер"), ("з 'являлось", "з'являлось"), ("пов 'язані", "пов'язані"),
    ("обов 'язково", "обов'язково"), ("абіз 'яна", "мавпа"),
]

MAXW, MAXC = 5, 30


def main():
    edl = json.load(open(os.path.join(HERE, "edl.json")))
    d = json.load(open(os.path.join(HERE, "transcript.json")))
    words = []
    for sg in d["segments"]:
        for w in sg["words"]:
            # map with the voiced part: try start, middle, end
            ts = [src_to_out(edl, x) for x in (w["s"] + 0.05, (w["s"] + w["e"]) / 2, w["e"] - 0.05)]
            ts = [t for t in ts if t is not None]
            if not ts:
                continue
            words.append([w["w"], min(ts), max(ts) + 0.05])
    # glue whisper's split tokens ("-привіт", "'ютер") back on
    merged = []
    for w in words:
        if merged and (w[0].startswith("-") or w[0].startswith("'")) and w[1] - merged[-1][2] < 0.3:
            merged[-1][0] += w[0]
            merged[-1][2] = w[2]
        else:
            merged.append(w)
    words = merged
    # chunk
    chunks, cur = [], []
    for w in words:
        if cur and (len(cur) >= MAXW or len(" ".join(x[0] for x in cur + [w])) > MAXC or w[1] - cur[-1][2] > 0.6):
            chunks.append(cur); cur = []
        cur.append(w)
        if re.search(r"[.?!,:;–]$", w[0]) and len(cur) >= 2:
            chunks.append(cur); cur = []
    if cur:
        chunks.append(cur)
    lines = []
    for i, c in enumerate(chunks):
        txt = " ".join(x[0] for x in c)
        for a, b in FIX:
            txt = txt.replace(a, b)
        txt = txt.rstrip(",")
        s = c[0][1]
        e = c[-1][2] + 0.25
        if i + 1 < len(chunks):
            e = min(e, chunks[i + 1][0][1] - 0.02)
        lines.append((s, e, txt))

    def ts(t):
        h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
        return f"{h}:{m:02d}:{s:05.2f}"
    head = """[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: S,Product Sans Medium,34,&H00FFFFFF,&H00FFFFFF,&H6A1E1A17,&H6A1E1A17,0,0,0,0,100,100,0.5,0,3,9,0,2,40,40,26,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    out = head + "".join(f"Dialogue: 0,{ts(s)},{ts(e)},S,,0,0,0,,{t}\n" for s, e, t in lines if e > s)
    open(os.path.join(HERE, "subs.ass"), "w").write(out)
    print(len(lines), "subtitle chunks")


if __name__ == "__main__":
    main()
