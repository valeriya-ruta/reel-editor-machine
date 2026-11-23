# Plate v2 from pieces.json: every piece encoded on its own with its framing
# (a centred scale step, tools/cut.py's rule: 100 > 110 > 100, XY stay 0),
# to whole frames, then concatenated.
import json, os, subprocess
P = json.load(open("pieces.json"))
os.makedirs("seg2", exist_ok=True)
lst = []
for i, p in enumerate(P):
    n = int(round((p["b"] - p["a"]) * 30))
    z = p["zoom"]
    vf = "scale=1080:1920" if z == 1.0 else "crop=iw/%.4f:ih/%.4f,scale=1080:1920:flags=lanczos" % (z, z)
    d = n / 30.0
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-ss", "%.3f" % p["a"], "-i", p["src"], "-t", "%.4f" % d,
                    "-vf", vf + ",fps=30", "-frames:v", str(n),
                    "-af", "apad,atrim=0:%.4f,afade=t=in:d=0.012,afade=t=out:st=%.4f:d=0.02" % (d, d - 0.02),
                    "-c:v", "libx264", "-crf", "17", "-preset", "fast", "-pix_fmt", "yuv420p",
                    "-c:a", "pcm_s16le", "-ar", "48000", "-ac", "2", "seg2/p%02d.mov" % i], check=True)
    lst.append("file 'p%02d.mov'" % i)
open("seg2/list.txt", "w").write("\n".join(lst) + "\n")
subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", "seg2/list.txt",
                "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "plate2.mp4"], check=True)
print("PLATE2_OK")
