# -*- coding: utf-8 -*-
"""Re-hear a span of a take on its own and patch work/rNN/utt.jsonl with it.

The packed ASR pass (26 s windows) sometimes invents a line on a breath
(«Дякуємо!», «Дякуємо за підтримку!») or loses the first words of the next
utterance. A solo pass over just the span is the better ear. Words are
reassigned to the utterances they fall in, as asr_batch.py does.

    python work/b1021/resolo.py 47 108.2 114.5 [108.2 114.5 ...]

Also drops, everywhere in the take, words that start after their own
utterance's audio has ended and last under 0.1 s — whisper's sign-off
hallucinations on silence.
"""
import json
import os
import sys
import wave

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
nn = sys.argv[1]
spans = [(float(sys.argv[i]), float(sys.argv[i + 1])) for i in range(2, len(sys.argv) - 1, 2)]
wd = os.path.join(ROOT, "work", "r" + nn)
stem = os.path.basename(open(wd + "/SOURCE.txt").read().strip())[:-4]
utts = [json.loads(l) for l in open(wd + "/utt.jsonl", encoding="utf-8")]

for u in utts:
    ghost = [w for w in u["words"] if w["s"] >= u["b"] + 0.02 and w["e"] - w["s"] < 0.1]
    if ghost:
        print("k%d ghost: %s" % (u["k"], " ".join(w["w"] for w in ghost)))
        u["words"] = [w for w in u["words"] if w not in ghost]
        u["text"] = " ".join(w["w"] for w in u["words"])

if spans:
    from faster_whisper import WhisperModel
    m = WhisperModel("medium", device="cpu", compute_type="int8", cpu_threads=2)
    with wave.open(os.path.join(ROOT, "work", "b1021", "asr", stem, "a16.wav")) as f:
        x = np.frombuffer(f.readframes(f.getnframes()), np.int16).astype(np.float32) / 32768.0
    for a, b in spans:
        segs, _ = m.transcribe(x[int(a * 16000):int(b * 16000)], language="uk", word_timestamps=True,
                               condition_on_previous_text=False, beam_size=5, vad_filter=False)
        words = [{"w": w.word.strip(), "s": round(a + w.start, 3), "e": round(a + w.end, 3)}
                 for s in segs for w in (s.words or [])]
        hit = [u for u in utts if u["b"] > a and u["a"] < b]
        if not hit:
            continue
        per = {u["k"]: [] for u in hit}
        for w in words:
            mid = (w["s"] + w["e"]) / 2
            k = min(hit, key=lambda u: 0 if u["a"] - 0.1 <= mid <= u["b"] + 0.1
                    else min(abs(mid - u["a"]), abs(mid - u["b"])))["k"]
            per[k].append(w)
        for u in hit:
            old = u["text"]
            # an utterance only partly inside the span keeps its words outside it
            keep = [w for w in u["words"] if not (a <= (w["s"] + w["e"]) / 2 <= b)]
            u["words"] = sorted(keep + per[u["k"]], key=lambda w: w["s"])
            u["text"] = " ".join(w["w"] for w in u["words"])
            u["how"] = "resolo"
            print("k%d  %s\n  -> %s" % (u["k"], old, u["text"]))

with open(wd + "/utt.jsonl", "w", encoding="utf-8") as f:
    for u in utts:
        f.write(json.dumps(u, ensure_ascii=False) + "\n")
