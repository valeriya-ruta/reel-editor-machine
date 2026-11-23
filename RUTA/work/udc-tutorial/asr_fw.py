# faster-whisper pass over the whole raw take (cloud container has no openai-whisper).
import json, sys, wave
import numpy as np
from faster_whisper import WhisperModel
m = WhisperModel("medium", device="cpu", compute_type="int8", cpu_threads=4)
w_ = wave.open(sys.argv[1]); audio = np.frombuffer(w_.readframes(w_.getnframes()), np.int16).astype(np.float32) / 32768
segs, info = m.transcribe(audio, language="uk", word_timestamps=True, vad_filter=True,
                          condition_on_previous_text=False, beam_size=5)
out = []
with open(sys.argv[2], "w", encoding="utf-8") as f:
    for s in segs:
        ws = [{"w": w.word.strip(), "s": round(w.start, 3), "e": round(w.end, 3)} for w in (s.words or [])]
        rec = {"a": round(s.start, 3), "b": round(s.end, 3), "text": s.text.strip(), "words": ws}
        f.write(json.dumps(rec, ensure_ascii=False) + "\n"); f.flush()
        print("%7.2f %s" % (s.start, s.text.strip()), flush=True)
