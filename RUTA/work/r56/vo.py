# -*- coding: utf-8 -*-
"""Her voiceover for reel 56's middle -> work/r56/vo.json.

    python3 work/r56/vo.py <her recording>      then: mkplate.py, captions.py, reel-56/build.py

v2 (her call, 2026-11-17): only the intro and the outro stay as filmed;
everything between is her voiceover. She recorded it in her own words as one
continuous take (`Pptx w claude.m4a`, 19.6 s), not the six scripted lines, so
it plays as ONE track and the footage is cut to her: each section ends where
the next one's first words begin (SPLIT), in the gap between words.

Whisper runs per utterance (over a whole file it drops a repeated take and
its times drift) and is cached in vo.words.json per recording.

vo.json: {"src", "v0", "v1", "sections": [{id, a, b}], "words": [{w, s, e}]}
— every time in seconds of her recording.
"""
import json
import os
import re
import subprocess
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
# section -> the words that open it in her take (the first section opens the take)
SPLIT = [("S1", None), ("S2", u"і тепер"), ("S3", u"поки"), ("S5", u"відправляємо"), ("S6", u"маю готову")]
HOLD = 2.4          # the slides keep flipping this long after her last word (her v2 note: show the slides)
FIX = {u"код,": u"Клод,", u"код": u"Клод"}     # whisper's mishearing -> her word


def norm(s):
    return re.sub(u"[^\\w']", "", s.lower())


def utterances(audio):
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
    return [(max(0.0, a * 0.02 - 0.15), min(len(audio) / 16000.0, b * 0.02 + 0.2))
            for a, b in utts if (b - a) * 0.02 > 0.25]


def words_of(src):
    cache = os.path.join(HERE, "vo.words.json")
    key = "%s|%d" % (os.path.abspath(src), os.path.getmtime(src))
    got = json.load(open(cache)) if os.path.exists(cache) else {}
    if got.get("key") == key:
        return got["words"]
    from faster_whisper import WhisperModel
    pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", src, "-ac", "1", "-ar", "16000", "-f", "s16le", "-"],
                         capture_output=True, check=True).stdout
    audio = np.frombuffer(pcm, np.int16).astype(np.float32) / 32768
    m = WhisperModel("large-v3", device="cpu", compute_type="int8")
    W = []
    for a, b in utterances(audio):
        segs, _ = m.transcribe(audio[int(a * 16000):int(b * 16000)], language="uk", word_timestamps=True,
                               beam_size=5, vad_filter=False)
        W += [{"w": x.word.strip(), "s": a + x.start, "e": a + x.end} for s in segs for x in (s.words or [])]
    json.dump({"key": key, "words": W}, open(cache, "w"), ensure_ascii=False, indent=0)
    return W


def main():
    src = sys.argv[1]
    W = words_of(src)
    heard = [norm(w["w"]) for w in W]
    starts = []
    for sid, cue in SPLIT[1:]:
        cue = [norm(x) for x in cue.split()]
        hits = [i for i in range(len(W)) if heard[i:i + len(cue)] == cue]
        if not hits:
            sys.exit("cue %r for %s not in her take: %s" % (" ".join(cue), sid, " ".join(heard)))
        i = hits[-1]                                   # a re-said phrase: the last one wins
        starts.append((W[i - 1]["e"] + W[i]["s"]) / 2.0 if i else W[i]["s"] - 0.05)
    v0 = max(0.0, W[0]["s"] - 0.15)
    v1 = W[-1]["e"] + HOLD
    bounds = [v0] + starts + [v1]
    sections = [{"id": sid, "a": round(a, 3), "b": round(b, 3)}
                for (sid, _), a, b in zip(SPLIT, bounds, bounds[1:])]
    words = [{"w": FIX.get(w["w"], w["w"]), "s": round(w["s"], 3), "e": round(w["e"], 3)} for w in W]
    json.dump({"src": os.path.abspath(src), "v0": round(v0, 3), "v1": round(v1, 3), "speech_end": W[-1]["e"],
               "sections": sections, "words": words},
              open(os.path.join(HERE, "vo.json"), "w"), ensure_ascii=False, indent=1)
    print("take %.2f-%.2f s;" % (v0, v1), ", ".join("%s %.2f" % (s["id"], s["b"] - s["a"]) for s in sections))


main()
