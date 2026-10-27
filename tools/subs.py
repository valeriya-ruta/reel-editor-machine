# -*- coding: utf-8 -*-
"""Simple subtitles for a long horizontal video: one calm line at a time.

    python tools/subs.py work/r41        -> work/r41/subs.ass (+ subs.txt to proofread)

Her call, 2026-10-27, for the UDC tutorial: simple sentence subtitles (not the
reel word-by-word captions), and "not too low otherwise they will be hidden by
the YT line" — the line sits MARGIN_V px above the bottom, clear of YouTube's
progress bar and controls.

Words come from cutlong.py's words.json (output timeline). Whisper's spelling
sits in a soft dark translucent box (BorderStyle 3), so it reads on her room
and on the light screen-demo background alike. Whisper's spelling
is corrected by the FIX list in the work dir (fix.json: [[wrong, right], ...],
applied to each line as plain substring replacements, longest first).
"""
import json
import os
import re
import sys

MAX_CH = 46          # one line, comfortably readable at 1080p
MAX_DUR = 4.2
GAP_BREAK = 0.55
MARGIN_V = 132
FONT, SIZE = "Product Sans", 52


def merge_words(words, merges):
    """Whisper splits a name over several words (Charge GPT, e -mail): join
    them back into one, keeping the outer timing and the last word's punctuation."""
    def base(w):
        return re.sub(r"[^\w-]+$", "", w["w"]).strip()
    out, i = [], 0
    while i < len(words):
        for seq, rep in merges:
            n = len(seq)
            if [base(x) for x in words[i:i + n]] == seq:
                last = words[i + n - 1]["w"]
                punct = last[len(base(words[i + n - 1])):]
                out.append({"w": rep + punct, "s": words[i]["s"], "e": last and words[i + n - 1]["e"]})
                i += n
                break
        else:
            out.append(words[i])
            i += 1
    return out


def chunks(words):
    out, cur = [], []
    for w in words:
        # a cut that joined two thoughts («теми, Після того») starts a new line
        if cur and cur[-1]["w"].endswith(",") and re.match(r"(Після|Отже|Тому|Але)\b", w["w"]):
            cur[-1] = dict(cur[-1], w=cur[-1]["w"][:-1] + ".")
            out.append(cur)
            cur = []
        if cur:
            text = " ".join(x["w"] for x in cur + [w])
            gap = w["s"] - cur[-1]["e"]
            if (len(text) > MAX_CH or w["e"] - cur[0]["s"] > MAX_DUR or gap > GAP_BREAK
                    or re.search(r"[.?!…]$", cur[-1]["w"])):
                out.append(cur)
                cur = []
        cur.append(w)
        # prefer to break after a comma once the line is half full
        if re.search(r"[,;:—–]$", w["w"]) and len(" ".join(x["w"] for x in cur)) > MAX_CH * 0.55:
            out.append(cur)
            cur = []
    if cur:
        out.append(cur)
    # an orphan (one or two short words) joins the line before it
    res = []
    for c in out:
        txt = " ".join(x["w"] for x in c)
        if res and len(txt) <= 16 and len(c) <= 2 and c[0]["s"] - res[-1][-1]["e"] < 0.4 \
                and len(" ".join(x["w"] for x in res[-1])) + len(txt) <= MAX_CH + 16:
            res[-1] = res[-1] + c
        else:
            res.append(c)
    return res


def ts(t):
    t = max(0.0, t)
    h, r = divmod(t, 3600)
    m, s = divmod(r, 60)
    return "%d:%02d:%05.2f" % (h, m, s)


def clean(text, fix):
    text = re.sub(r" ([-'’]) ?", r"\1", text)            # whisper splits «п 'ять», «по -перше»
    text = text.replace(" -", "-")
    for a, b in fix:
        text = text.replace(a, b)
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"[,;:]$", "", text)                    # a line never ends on a comma
    return text


def main():
    wd = sys.argv[1]
    words = json.load(open(os.path.join(wd, "words.json"), encoding="utf-8"))
    fp = os.path.join(wd, "fix.json")
    fix = json.load(open(fp, encoding="utf-8")) if os.path.exists(fp) else []
    fix.sort(key=lambda p: -len(p[0]))
    mp = os.path.join(wd, "merge.json")
    if os.path.exists(mp):
        words = merge_words(words, json.load(open(mp, encoding="utf-8")))
    lines = []
    for c in chunks(words):
        text = clean(" ".join(x["w"] for x in c), fix)
        if not text:
            continue
        if lines and re.search(r"[.?!…»]$", lines[-1][2]):
            text = text[0].upper() + text[1:]
        lines.append((c[0]["s"], c[-1]["e"] + 0.12, text))
    # never overlap; bridge tiny gaps so the line does not flicker
    for i in range(len(lines) - 1):
        a, b, t = lines[i]
        na = lines[i + 1][0]
        if na - b < 0.35:
            b = na - 0.02
        lines[i] = (a, min(b, na - 0.02), t)
    head = ("[Script Info]\nScriptType: v4.00+\nPlayResX: 1920\nPlayResY: 1080\nWrapStyle: 2\n\n"
            "[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, "
            "BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, "
            "Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
            "Style: S,%s,%d,&H00FFFFFF,&H00FFFFFF,&H5A140F12,&H00000000,0,0,0,0,100,100,0,0,3,12,0,2,120,120,%d,1\n\n"
            "[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"
            % (FONT, SIZE, MARGIN_V))
    with open(os.path.join(wd, "subs.ass"), "w", encoding="utf-8") as f:
        f.write(head)
        for a, b, t in lines:
            f.write("Dialogue: 0,%s,%s,S,,0,0,0,,{\\fad(80,80)}%s\n" % (ts(a), ts(b), t))
    with open(os.path.join(wd, "subs.txt"), "w", encoding="utf-8") as f:
        for i, (a, b, t) in enumerate(lines):
            f.write("%3d %7.2f %s\n" % (i, a, t))
    print("subs: %d lines" % len(lines))


if __name__ == "__main__":
    main()
