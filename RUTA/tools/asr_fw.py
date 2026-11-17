"""Word-level transcription with faster-whisper — for cloud sessions.

Same output shape as tools/asr.py ({"text", "words": [{w, s, e}]}), so
tools/align.py reads either. Use this one where openai-whisper's model host is
unreachable (the cloud container): faster-whisper pulls its models from
Hugging Face instead.

    python3 tools/asr_fw.py <audio or video> <words.json> [model] [lang]   (copied from Nika/tools, 2026-11-17)

model defaults to large-v3; lang defaults to auto-detect.
"""
import json
import subprocess
import sys

import numpy as np
from faster_whisper import WhisperModel

src, out = sys.argv[1], sys.argv[2]
model = sys.argv[3] if len(sys.argv) > 3 else "large-v3"
lang = sys.argv[4] if len(sys.argv) > 4 else None

# Decode with ffmpeg rather than faster-whisper's PyAV path: newer PyAV dropped
# the `metadata_errors` argument it passes, and ffmpeg takes any container.
pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", src, "-f", "s16le", "-ac", "1",
                      "-ar", "16000", "-"], capture_output=True, check=True).stdout
audio = np.frombuffer(pcm, np.int16).astype(np.float32) / 32768.0

m = WhisperModel(model, device="cpu", compute_type="int8")
segs, info = m.transcribe(audio, language=lang, word_timestamps=True,
                          vad_filter=False, beam_size=5)
segs = list(segs)
words = [{"w": x.word.strip(), "s": round(x.start, 3), "e": round(x.end, 3)}
         for s in segs for x in (s.words or [])]
json.dump({"lang": info.language, "text": " ".join(s.text.strip() for s in segs),
           "segments": [{"s": round(s.start, 3), "e": round(s.end, 3), "t": s.text.strip()}
                        for s in segs],
           "words": words},
          open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("LANG", info.language, round(info.language_probability, 2), "WORDS", len(words))
