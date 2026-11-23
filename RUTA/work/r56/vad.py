# Speech spans per clip from a 20 ms RMS envelope, threshold = noise floor + 10 dB
import subprocess, sys, numpy as np
src, a, b = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])
pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", src, "-ac", "1", "-ar", "16000", "-f", "s16le", "-"],
                     capture_output=True, check=True).stdout
x = np.frombuffer(pcm, np.int16).astype(np.float32) / 32768
hop = 320
n = len(x) // hop
db = 20 * np.log10(np.sqrt((x[:n * hop].reshape(n, hop) ** 2).mean(1)) + 1e-9)
floor = np.percentile(db, 10)
th = floor + 10
on = db > th
print("floor %.1f dB, p50 %.1f, p90 %.1f, th %.1f" % (floor, np.percentile(db, 50), np.percentile(db, 90), th))
spans, s = [], None
for i, v in enumerate(on):
    t = i * 0.02
    if v and s is None: s = t
    if not v and s is not None:
        spans.append([s, t]); s = None
if s is not None: spans.append([s, n * 0.02])
merged = []
for sp in spans:
    if merged and sp[0] - merged[-1][1] < 0.15: merged[-1][1] = sp[1]
    else: merged.append(sp)
print(" ".join("%.2f-%.2f" % (p, q) for p, q in merged if q - p > 0.06 and q > a and p < b))
