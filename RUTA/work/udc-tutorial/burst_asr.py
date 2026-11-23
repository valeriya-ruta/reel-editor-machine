# Per-burst ASR on problem windows: whisper over a long segment swallows repeats,
# one burst at a time it hears every attempt.
import json, sys, wave
import numpy as np
from faster_whisper import WhisperModel
w_ = wave.open("work/udc-tutorial/audio.wav"); sr = w_.getframerate()
A = np.frombuffer(w_.readframes(w_.getnframes()), np.int16).astype(np.float32) / 32768
hop = int(sr * 0.01); n = len(A) // hop
env = np.sqrt((A[:n * hop].reshape(n, hop) ** 2).mean(1))
thr = max(0.012, np.percentile(env, 30) * 2.5)
m = WhisperModel("medium", device="cpu", compute_type="int8", cpu_threads=4)
wins = json.loads(sys.argv[1])
out = {}
for a, b in wins:
    i0, i1 = int(a * 100), int(b * 100)
    on = env[i0:i1] > thr
    # bursts: speech runs separated by >= 0.25 s of quiet
    bursts, s, q = [], None, 0
    for k, v in enumerate(on):
        if v:
            if s is None: s = k
            q = 0
        elif s is not None:
            q += 1
            if q >= 25:
                bursts.append((s, k - q + 1)); s = None; q = 0
    if s is not None: bursts.append((s, len(on)))
    print("== window %.1f-%.1f" % (a, b))
    for s, e in bursts:
        t0, t1 = a + s / 100 - 0.08, a + e / 100 + 0.08
        if t1 - t0 < 0.25: continue
        seg = A[int(t0 * sr):int(t1 * sr)]
        r, _ = m.transcribe(seg, language="uk", word_timestamps=True, vad_filter=False, condition_on_previous_text=False)
        ws = [(x.word.strip(), round(t0 + x.start, 2), round(t0 + x.end, 2)) for sg in r for x in (sg.words or [])]
        print("  %7.2f-%7.2f  %s" % (t0, t1, " ".join("%s@%.2f" % (w, s_) for w, s_, _ in ws)))
        out.setdefault("%s,%s" % (a, b), []).append({"a": round(t0, 3), "b": round(t1, 3), "text": "",
            "words": [{"w": w, "s": s_, "e": e_} for w, s_, e_ in ws if a <= s_ < b]})
if len(sys.argv) > 2:
    json.dump(out, open(sys.argv[2], "w", encoding="utf-8"), ensure_ascii=False, indent=0)
