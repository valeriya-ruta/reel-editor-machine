"""Word timings for a voiceover: python scripts/words.py public/vo/05-calls.mp3 episodes/05-calls.words.json

faster-whisper, word-level. Only the timing is used; spelling comes from the spec.
"""
import json
import subprocess
import sys

import numpy as np

from faster_whisper import WhisperModel

src, dst = sys.argv[1], sys.argv[2]
model = WhisperModel(sys.argv[3] if len(sys.argv) > 3 else "small", device="cpu", compute_type="int8")
# decode with ffmpeg: faster-whisper's own decoder breaks on some PyAV versions
pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", src, "-f", "f32le", "-ac", "1", "-ar", "16000", "-"], capture_output=True, check=True).stdout
audio = np.frombuffer(pcm, np.float32)
segs, _ = model.transcribe(audio, language="uk", word_timestamps=True, vad_filter=False)
words = [{"w": w.word.strip(), "s": round(w.start, 3), "e": round(w.end, 3)} for s in segs for w in s.words]
json.dump({"audio": src.split("public/")[-1], "words": words}, open(dst, "w"), ensure_ascii=False, indent=0)
print(dst, len(words), "words")
