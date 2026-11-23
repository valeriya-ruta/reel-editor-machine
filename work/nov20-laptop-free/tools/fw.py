import json, sys
from faster_whisper import WhisperModel
m = WhisperModel(sys.argv[3], device="cpu", compute_type="int8", cpu_threads=4)
import wave, numpy as np
wf=wave.open(sys.argv[1]); a=np.frombuffer(wf.readframes(wf.getnframes()),np.int16).astype(np.float32)/32768
segs, info = m.transcribe(a, language="uk", word_timestamps=True, vad_filter=False, beam_size=5)
out = []
for s in segs:
    out.append({"s": round(s.start,2), "e": round(s.end,2), "t": s.text.strip(),
                "words": [{"w": w.word.strip(), "s": round(w.start,3), "e": round(w.end,3)} for w in s.words]})
    print(f"{s.start:7.2f}-{s.end:7.2f} {s.text.strip()}", flush=True)
json.dump(out, open(sys.argv[2], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
