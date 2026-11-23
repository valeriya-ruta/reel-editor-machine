# -*- coding: utf-8 -*-
"""Captions for reel 56, v2 (intro + six voiceover sections + outro).

Intro and outro: her words from whisper large-v3 on the v1 plate
(work/r56/words.json), spelled right below; segment-first words snapped to
the speech onsets (work/r56/vad.py), since whisper starts them early. The
intro sits at the same place in v2; the outro moves with the plate.

The middle: her voiceover take in her own words (work/r56/vo.json, whisper per
utterance, «код» -> «Клод»), on her recording's timing, from where mkplate.py
started the take (pieces.out.json "t_vo"). The headphones footage gets no
words of its own.

    python3 work/r56/captions.py      -> work/r56/captions.json
"""
import io
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
W = json.load(io.open(os.path.join(HERE, "words.json"), encoding="utf-8"))["words"]
PIECES = json.load(io.open(os.path.join(HERE, "pieces.out.json"), encoding="utf-8"))
INTRO, OUTRO = range(0, 35), range(80, 87)      # word indices on the v1 plate
OUTRO_T0_V1 = 45.1333                            # where the outro started on the v1 plate

# index -> her word (None drops it); whisper heard «введення 3D за яй» for
# «ведення Threads з AI» (re-decoded with a vocabulary prompt: work/r56/redo2.py)
FIX = {
    13: u"ведення", 14: u"Threads", 15: u"з", 16: u"AI,",
    17: u"але в",            # «в» is swallowed into «моїй» on the plate
    84: u"обов'язково", 85: None,
}
# speech onsets on the v1 plate (vad.py) for words whisper starts early
ONSET = {0: 0.22, 34: 10.58, 80: 45.46}


def spoken(idx, shift):
    out = []
    for i in idx:
        txt = FIX.get(i, W[i]["w"])
        if txt is None:
            continue
        s = ONSET.get(i, W[i]["s"])
        e = W[i + 1]["e"] if FIX.get(i + 1, "") is None else W[i]["e"]
        out.append({"w": txt, "s": round(s + shift, 3), "e": round(max(e, s + 0.1) + shift, 3)})
    return out


def main():
    words = spoken(INTRO, 0.0) + spoken(OUTRO, PIECES[-1]["t0"] - OUTRO_T0_V1)
    vo = json.load(io.open(os.path.join(HERE, "vo.json"), encoding="utf-8"))
    off = PIECES[0]["t_vo"] - vo["v0"]          # her take's time -> plate time
    words += [{"w": w["w"], "s": round(w["s"] + off, 3), "e": round(w["e"] + off, 3), "vo": True}
              for w in vo["words"]]
    words.sort(key=lambda x: x["s"])
    json.dump({"words": words}, io.open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print("%d words (%d voiceover)" % (len(words), sum(1 for x in words if x.get("vo"))))


main()
