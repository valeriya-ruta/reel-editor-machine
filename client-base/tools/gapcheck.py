# -*- coding: utf-8 -*-
"""Did the cut remove any of her voice it was not told to?

    python tools/gapcheck.py 01        # reads work/r01/cut.json + cut-fix.json

Every stretch of raw audio the plan leaves out is either a pause, a bad take
or a manual drop (cut-fix.json). This lists the removed stretches that still
hold voice-level audio and are not inside a manual drop: on IMG_0861 that is
how «не» went missing from «Тому що я не думаю» (whisper stretched one word
over a gap, and the gap looked like a pause). Run it after cut.py, before
--render. Exit code 1 if anything is listed.
"""
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cut import ROOT, SCRATCH, SPEECH_DB, envelope, read_wav  # noqa: E402

LOUD_MIN = 0.06     # seconds of voice-level audio before a removed gap is suspicious


def main():
    nn = sys.argv[1].zfill(2)
    wd = os.path.join(ROOT, "work", "r" + nn)
    clips = json.load(open(os.path.join(wd, "cut.json"), encoding="utf-8"))["clips"]
    fixp = os.path.join(wd, "cut-fix.json")
    drops = json.load(open(fixp, encoding="utf-8")).get("drop", []) if os.path.exists(fixp) else []
    sr, a = read_wav(os.path.join(SCRATCH, "r" + nn, "full48.wav"))
    env, hop = envelope(a, sr, 0.01)
    db = 20 * np.log10(env / 32768.0 + 1e-9)
    words = sorted((w["s"], w["e"], w["w"]) for l in open(os.path.join(wd, "utt.jsonl"), encoding="utf-8")
                   for w in json.loads(l)["words"])
    bad, prev = 0, None
    for c in clips + [{"src_in": len(a) / sr, "dur": 0}]:
        s = c["src_in"]
        if prev is not None and s - prev > 0.02:
            loud = float((db[int(prev / hop):int(s / hop)] > SPEECH_DB).sum()) * hop
            meant = any(x - 0.10 <= prev + 0.05 and s - 0.05 <= y + 0.40 for x, y in drops)
            if loud >= LOUD_MIN and not meant:
                ws = [w for s0, e0, w in words if prev - 0.05 < (s0 + e0) / 2 < s + 0.05]
                print("VOICE REMOVED %7.2f-%7.2f (%.2f s, %.2f s loud)  %s"
                      % (prev, s, s - prev, loud, " ".join(ws)))
                bad += 1
        prev = s + c["dur"]
    print("gapcheck: %d removed stretch(es) hold voice outside a manual drop" % bad)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
