# Plate from cut.json: each segment encoded on its own, then concatenated.
import json, subprocess, os
segs = json.load(open("cut.json"))
os.makedirs("seg", exist_ok=True)
lst = []
for i, (a, b) in enumerate(segs):
    d = b - a
    out = "seg/s%02d.mp4" % i
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-ss", "%.3f" % a, "-i", "better-1080.mp4", "-t", "%.3f" % d,
                    "-af", "afade=t=in:d=0.012,afade=t=out:st=%.3f:d=0.015" % (d - 0.015),
                    "-r", "30", "-c:v", "libx264", "-crf", "17", "-preset", "fast", "-pix_fmt", "yuv420p",
                    "-c:a", "pcm_s16le", "-ar", "48000", "seg/s%02d.mov" % i], check=True)
    lst.append("file 's%02d.mov'" % i)
open("seg/list.txt", "w").write("\n".join(lst) + "\n")
subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", "seg/list.txt",
                "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "plate-cut.mp4"], check=True)
print("PLATE_OK")
