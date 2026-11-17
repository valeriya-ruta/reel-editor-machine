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
    # one whisper pass per utterance: over the whole file whisper drops a repeated
    # take (seen on the synthetic test), and its times drift (reel 55)
    hop = 320
    n = len(audio) // hop
    db = 20 * np.log10(np.sqrt((audio[:n * hop].reshape(n, hop) ** 2).mean(1)) + 1e-9)
    on = db > np.percentile(db, 10) + 12
    utts, s0 = [], None
    for k, v in enumerate(list(on) + [False]):
        if v and s0 is None:
            s0 = k
        if not v and s0 is not None:
            if utts and (s0 - utts[-1][1]) * 0.02 < 0.45:
                utts[-1][1] = k
            else:
                utts.append([s0, k])
            s0 = None
    utts = [(max(0.0, a * 0.02 - 0.15), min(len(audio) / 16000.0, b * 0.02 + 0.2))
            for a, b in utts if (b - a) * 0.02 > 0.25]
    m = WhisperModel("large-v3", device="cpu", compute_type="int8")
    W = []
    for a, b in utts:
        segs, _ = m.transcribe(audio[int(a * 16000):int(b * 16000)], language="uk", word_timestamps=True,
                               beam_size=5, vad_filter=False)
        W += [{"w": x.word.strip(), "s": a + x.start, "e": a + x.end} for s in segs for x in (s.words or [])]
    heard = [norm(w["w"]) for w in W]
    takes = []
    for li, line in enumerate(LINES):
        want = [norm(t) for t in line.split() if norm(t)]
        wins = []
        for i in range(len(W)):
            for j in range(i + max(1, len(want) - 3), min(len(W), i + len(want) + 4) + 1):
                if any(W[q + 1]["s"] - W[q]["e"] > 1.5 for q in range(i, j - 1)):
                    break               # a long pause ends a take: no window spans two
                wins.append((difflib.SequenceMatcher(None, want, heard[i:j]).ratio(), i, j))
        top = max(wins)[0] if wins else 0
        ok = [w for w in wins if w[0] >= max(0.6, top - 0.15)]
        if not ok:
            sys.exit("line %d not found in the recording: %s" % (li + 1, line))
        last = max(w[1] for w in ok)                        # the last take wins
        r, i, j = max(w for w in ok if last - len(want) // 2 <= w[1] <= last)   # its best window
        # out to the take's own edges: a word whisper missed at either end is still hers,
        # but never past the neighbouring take (the previous / next word) or its utterance
        ua = max(u[0] for u in utts if u[0] <= W[i]["s"] + 0.01)
        ub = min(u[1] for u in utts if u[1] >= W[j - 1]["e"] - 0.01)
        a = max(ua, W[i - 1]["e"] + 0.05 if i > 0 else 0.0, W[i]["s"] - 0.6)
        k = j           # words in the same breath right after the window are the take's tail
        while k < len(W) and k < j + 3 and W[k]["s"] - W[k - 1]["e"] < 0.6:
            k += 1
        b = min(ub, W[k]["s"] - 0.05 if k < len(W) else ub)
        b = max(b, W[k - 1]["e"] + 0.12)
        takes.append({"line": li, "a": round(min(a, W[i]["s"] - 0.08), 3), "b": round(max(b, W[j - 1]["e"] + 0.12), 3),
                      "ratio": round(r, 2)})
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
