# -*- coding: utf-8 -*-
"""Captions for reel 56 on the cut plate (reel-56/assets/base.mp4).

Her spoken words come from whisper large-v3 on the plate (work/r56/words.json),
spelled right below. Segment-first words are snapped to the plate's speech
onsets (work/r56/vad.py): whisper starts them up to 0.4 s early, sometimes
inside the previous piece.

The two silent stretches (C: the base prompt, F: the finished deck) carry the
voiceover lines from PLAN.md. Until she records them they run as text at a
reading pace; each word is tagged "vo" so her recording can replace them.

    python3 work/r56/captions.py      -> work/r56/captions.json
"""
import io
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
W = json.load(io.open(os.path.join(HERE, "words.json"), encoding="utf-8"))["words"]

# index -> her word (None drops it); whisper heard «введення 3D за яй» for
# «ведення Threads з AI» (re-decoded with a vocabulary prompt: work/r56/redo2.py)
FIX = {
    13: u"ведення", 14: u"Threads", 15: u"з", 16: u"AI,",
    17: u"але в",            # «в» is swallowed into «моїй» on the plate
    45: u"кращий,", 61: u"основні",
    84: u"обов'язково", 85: None,
}
# speech onsets on the plate (vad.py) for words whisper starts early
ONSET = {0: 0.22, 34: 10.58, 40: 21.88, 41: 22.02, 64: 29.34, 73: 33.32, 74: 33.46, 78: 35.92, 80: 45.46}

VO = [
    # (start, end, line) — text-only until her recording lands
    (13.95, 17.25, u"Даю йому базовий промт — і він уже починає працювати."),
    (17.45, 21.45, u"А поки він працює, я записую голосове: пояснюю, що хочу бачити в презентації."),
    (36.85, 38.45, u"Йду на п'ять хвилин."),
    (38.75, 40.65, u"Повертаюсь — презентація готова,"),
    (41.10, 43.10, u"і її можна редагувати."),
    (43.60, 44.90, u"Вуаля!"),
]


def paced(a, b, line):
    """words of a line spread over [a, b] by length, the dash glued to its word"""
    toks = []
    for t in line.split():
        if t in (u"—", u"–") and toks:
            toks[-1] += u" " + t
        else:
            toks.append(t)
    wt = [len(t.strip(u"—–,.:!?")) + 3 for t in toks]
    tot, t, out = float(sum(wt)), a, []
    for tok, x in zip(toks, wt):
        d = (b - a) * x / tot
        out.append({"w": tok, "s": round(t, 3), "e": round(t + d, 3), "vo": True})
        t += d
    return out


def main():
    words = []
    for i, w in enumerate(W):
        txt = FIX.get(i, w["w"])
        if txt is None:
            continue
        s = ONSET.get(i, w["s"])
        e = W[i + 1]["e"] if FIX.get(i + 1, "") is None else w["e"]
        words.append({"w": txt, "s": round(s, 3), "e": round(max(e, s + 0.1), 3)})
    vf = os.path.join(HERE, "vo.json")
    if os.path.exists(vf):
        vo = json.load(io.open(vf, encoding="utf-8"))
        for w in words:          # pieces after C / F start later by what those slots grew
            w["s"] = round(w["s"] + (vo["grow_c"] if w["s"] >= 21.6 else 0)
                           + (vo["grow_f"] if w["s"] >= 45.13 else 0), 3)
            w["e"] = round(w["e"] + (vo["grow_c"] if w["e"] > 21.6 else 0)
                           + (vo["grow_f"] if w["e"] > 45.13 else 0), 3)
        nxt = sorted(vo["words"], key=lambda x: x["s"])
        for k, w in enumerate(nxt):
            w["e"] = round(nxt[k + 1]["s"] if k + 1 < len(nxt) else w["s"] + 0.5, 3)
        words += nxt
    else:
        for a, b, line in VO:
            words += paced(a, b, line)
    words.sort(key=lambda x: x["s"])
    json.dump({"words": words}, io.open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print("%d words (%d voiceover)" % (len(words), sum(1 for x in words if x.get("vo"))))


main()
