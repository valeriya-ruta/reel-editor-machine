# which phrase did she say at 4.2-6.6 s? score candidate prompts by avg_logprob
import subprocess, sys, numpy as np
from faster_whisper import WhisperModel
src = sys.argv[1]
pcm = subprocess.run(["ffmpeg", "-v", "error", "-ss", "1.4", "-t", "5.2", "-i", src, "-f", "s16le", "-ac", "1",
                      "-ar", "16000", "-"], capture_output=True, check=True).stdout
audio = np.frombuffer(pcm, np.int16).astype(np.float32) / 32768.0
m = WhisperModel("large-v3", device="cpu", compute_type="int8")
for p in [u"Threads з AI.", u"соцмереж з ШІ.", u"Instagram з AI.", u"контенту з AI.", u"соцмереж з AI."]:
    segs, _ = m.transcribe(audio, language="uk", initial_prompt=u"Автоматизувати ведення " + p, beam_size=5)
    segs = list(segs)
    print(p, "|", " ".join(s.text.strip() for s in segs), "|", " ".join("%.3f" % s.avg_logprob for s in segs))
