# re-decode one span with a vocabulary prompt (whisper heard «введення 3D за яй»)
import subprocess, sys, numpy as np
from faster_whisper import WhisperModel
src, a, b = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])
pcm = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(a), "-t", str(b - a), "-i", src, "-f", "s16le", "-ac", "1",
                      "-ar", "16000", "-"], capture_output=True, check=True).stdout
audio = np.frombuffer(pcm, np.int16).astype(np.float32) / 32768.0
m = WhisperModel("large-v3", device="cpu", compute_type="int8")
for p in [None, u"Вебінар про те, як автоматизувати ведення Threads і Instagram з ШІ. Клод, Claude."]:
    segs, _ = m.transcribe(audio, language="uk", initial_prompt=p, beam_size=5)
    print(repr(p)[:30], "|", " ".join(s.text.strip() for s in segs))
