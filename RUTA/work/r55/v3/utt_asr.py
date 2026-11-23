# Per-utterance ASR on the better take: whisper's whole-file pass drifts by up
# to 2 s on a 5-minute take, so each speech span between silences gets its own.
import json, wave, numpy as np
from faster_whisper import WhisperModel
sil = [tuple(map(float, l.split())) for l in open("v3/silences.tsv") if l.strip()]
wf = wave.open("v3/audio.wav"); a = np.frombuffer(wf.readframes(wf.getnframes()), dtype=np.int16).astype(np.float32) / 32768
dur = len(a) / 16000.0
spans, cur = [], 0.0
for s, e in sil:
    if s - cur > 0.12: spans.append((cur, s))
    cur = e
if dur - cur > 0.12: spans.append((cur, dur))
m = WhisperModel("medium", device="cpu", compute_type="int8", cpu_threads=4)
out = []
for k, (s, e) in enumerate(spans):
    s0, e0 = max(0, s - 0.12), min(dur, e + 0.12)
    seg, _ = m.transcribe(a[int(s0 * 16000):int(e0 * 16000)], language="uk", word_timestamps=True,
                          beam_size=5, condition_on_previous_text=False)
    ws = [{"w": w.word.strip(), "s": round(s0 + w.start, 3), "e": round(s0 + w.end, 3)} for x in seg for w in x.words]
    out.append({"k": k, "a": round(s, 3), "b": round(e, 3), "words": ws})
    print(k, len(spans), "%.1f" % s, " ".join(w["w"] for w in ws), flush=True)
json.dump(out, open("v3/utt.json", "w"), ensure_ascii=False, indent=0)
print("UTT_DONE")
