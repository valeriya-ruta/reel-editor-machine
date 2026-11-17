# -*- coding: utf-8 -*-
"""Her voiceover for reel 56's two silent stretches -> work/r56/vo.json.

    python3 work/r56/vo.py <her recording>      then: mkplate.py, captions.py, reel-56/build.py

Finds the three lines of PLAN.md in her recording (whisper large-v3, word
times), keeps the LAST take of each (her rule: last take wins), and places
them: lines 1+2 over C (the base prompt, ends on the send), line 3 over F (the
finished deck). If a line runs longer than its slot, the slot grows from the
front (C starts earlier in her clip, F1 too) and every later caption shifts by
the same amount — the pieces after it are untouched.
"""
import difflib
import json
import os
import re
import subprocess
import sys

import numpy as np
from faster_whisper import WhisperModel

HERE = os.path.dirname(os.path.abspath(__file__))
LINES = [
    u"Даю йому базовий промт — і він уже починає працювати.",
    u"А поки він працює, я записую голосове: пояснюю, що хочу бачити в презентації.",
    u"Йду на п'ять хвилин. Повертаюсь — презентація готова, і її можна редагувати. Вуаля!",
]
C0, C1 = 13.8333, 21.6        # plate span of piece C (pieces.out.json, before any growth)
F0, F1 = 36.6333, 45.1333     # F1 + F2
LEAD, GAP, TAIL = 0.20, 0.35, 0.25


def norm(s):
    return re.sub(u"[^\\w']", "", s.lower().replace(u"’", "'"))


def main():
    src = sys.argv[1]
    pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", src, "-ac", "1", "-ar", "16000", "-f", "s16le", "-"],
                         capture_output=True, check=True).stdout
    audio = np.frombuffer(pcm, np.int16).astype(np.float32) / 32768
    m = WhisperModel("large-v3", device="cpu", compute_type="int8")
    segs, _ = m.transcribe(audio, language="uk", word_timestamps=True, beam_size=5,
                           initial_prompt=" ".join(LINES))
    W = [{"w": x.word.strip(), "s": x.start, "e": x.end} for s in segs for x in (s.words or [])]
    heard = [norm(w["w"]) for w in W]
    takes = []
    for li, line in enumerate(LINES):
        want = [norm(t) for t in line.split() if norm(t)]
        wins = []
        for i in range(len(W)):
            for j in range(i + max(1, len(want) - 3), min(len(W), i + len(want) + 4) + 1):
                wins.append((difflib.SequenceMatcher(None, want, heard[i:j]).ratio(), i, j))
        top = max(wins)[0] if wins else 0
        ok = [w for w in wins if w[0] >= max(0.6, top - 0.15)]
        if not ok:
            sys.exit("line %d not found in the recording: %s" % (li + 1, line))
        last = max(w[1] for w in ok)                        # the last take wins
        r, i, j = max(w for w in ok if w[1] >= last - 2)    # its best-fitting window
        best = (i, j, r)
        i, j, r = best
        takes.append({"line": li, "a": max(0.0, W[i]["s"] - 0.08), "b": W[j - 1]["e"] + 0.12, "ratio": round(r, 2)})
    d = [t["b"] - t["a"] for t in takes]
    grow_c = max(0.0, LEAD + d[0] + GAP + d[1] + TAIL - (C1 - C0))
    grow_f = max(0.0, LEAD + d[2] + TAIL - (F1 - F0))
    takes[0]["at"] = C0 + LEAD
    takes[1]["at"] = takes[0]["at"] + d[0] + GAP
    takes[2]["at"] = F0 + grow_c + LEAD
    # her words, spelled as written, on her recording's timing
    words = []
    for t in takes:
        toks = []
        for x in LINES[t["line"]].split():
            if not norm(x) and toks:
                toks[-1] += u" " + x                         # the dash stays glued to its word
            elif norm(x):
                toks.append(x)
        got = [w for w in W if t["a"] - 0.01 <= w["s"] < t["b"]]
        sm = difflib.SequenceMatcher(None, [norm(x) for x in toks], [norm(w["w"]) for w in got])
        tm = {}
        for a, b, n in sm.get_matching_blocks():
            for k in range(n):
                tm[a + k] = got[b + k]
        for k, tok in enumerate(toks):
            if k in tm:
                s = tm[k]["s"]
            else:   # unmatched: between its neighbours
                prev = max([q for q in tm if q < k], default=None)
                s = tm[prev]["e"] if prev is not None else t["a"]
            words.append({"w": tok, "s": round(t["at"] + s - t["a"], 3), "vo": True})
    json.dump({"src": os.path.abspath(src), "grow_c": round(grow_c, 3), "grow_f": round(grow_f, 3),
               "takes": takes, "words": words},
              open(os.path.join(HERE, "vo.json"), "w"), ensure_ascii=False, indent=1)
    print("takes", [(t["line"] + 1, round(t["b"] - t["a"], 2), t["ratio"]) for t in takes],
          "grow C %.2f F %.2f" % (grow_c, grow_f))


main()
