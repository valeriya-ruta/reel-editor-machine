# -*- coding: utf-8 -*-
"""Find the bad takes in a raw take's transcript, to write script.txt from it.

    python tools/takes.py 01        # reads work/r01/utt.jsonl

Ruta's rule for Marina (2026-11-05): the transcript is the script. But the
transcript of a raw take still contains every fumbled attempt, and cut.py's
"last take wins" only sees a restart when the script has the line once. So
this lists every place where she starts the same words again shortly after
(a restart), with timestamps and both attempts side by side. Read it against
the transcript, then write work/rNN/script.txt = the transcript with the
earlier attempts deleted. cut.py does the rest. Unsure whether a repeat is a
fumble or on purpose: keep it (never cut content) and list it at the end.
A manual drop goes in cut-fix.json.
"""
import io
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cut import norm  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
N = 3          # words that must repeat to count as a restart
WITHIN = 40    # ... within this many words (cut.py's MAX_DROP_WORDS)

nn = sys.argv[1].zfill(2)
utts = [json.loads(l) for l in io.open(os.path.join(ROOT, "work", "r" + nn, "utt.jsonl"),
                                        encoding="utf-8")]
W = [x for u in sorted(utts, key=lambda u: u["a"]) for x in u["words"] if norm(x["w"])]
T = [norm(x["w"]) for x in W]
print("Restart candidates. Many are her repeating on purpose (content: keep it).\n"
      "Only a fumbled line said again is a bad take.\n")
seen = set()
for i in range(len(T) - N):
    for j in range(i + 1, min(len(T) - N, i + WITHIN) + 1):
        if T[i:i + N] == T[j:j + N] and i not in seen:
            seen.update(range(i, j))
            a = " ".join(x["w"] for x in W[i:j])
            b = " ".join(x["w"] for x in W[j:j + N + 6])
            print("%7.2f  restart at %7.2f  (%d words)\n   first:  %s\n   again:  %s ..."
                  % (W[i]["s"], W[j]["s"], j - i, a, b))
            break
