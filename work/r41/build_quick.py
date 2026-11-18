# Quick edit for reel 41: tighten pauses + word-by-word captions (STYLE.md §2b).
import json, re, subprocess
W = json.load(open("words.json"))["words"]
FIX = {12: "надавати", 13: None, 15: "послугу", 105: "Протестувала", 129: None,
       131: "побачите", 140: "які,", 141: "як", 142: "команда,", 143: None,
       144: "передають", 145: "задачі", 146: "одне", 147: "одному.", 154: "коліні.",
       166: "наступний", 169: "до сраки", 173: "до сраки", 179: "чат", 181: "Клоді,",
       195: "отримати", 224: "Клод,"}
SIL = [(0.221,0.703),(5.568,6.059),(7.328,7.615),(15.673,16.090),(22.133,22.842),
       (25.148,25.435),(36.230,36.592),(38.751,39.041),(41.479,41.787),(45.137,45.528),
       (57.368,57.771),(69.076,69.384),(70.940,71.262),(72.070,72.329),(77.474,79.115),
       (87.677,87.968)]
END = 92.30
KEEP_PAD = 0.07
keep, t = [], 0.0
for s, e in SIL:
    if e - s < 0.28: continue
    keep.append((t, s + KEEP_PAD)); t = e - KEEP_PAD
keep.append((t, END))
def remap(x):
    off = 0.0
    for a, b in keep:
        if x < a: return off
        if x <= b: return off + x - a
        off += b - a
    return off
DUR = round(sum(b - a for a, b in keep) * 30) / 30
caps = []
for i, w in enumerate(W):
    txt = FIX.get(i, w["word"])
    if txt is None: continue
    caps.append([remap(w["start"]), remap(w["end"]), txt.upper()])
for i in range(len(caps) - 1):           # §2b: no superimposed words; hold through short gaps
    nxt = caps[i + 1][0]
    caps[i][1] = nxt - 0.034 if nxt - caps[i][1] < 0.4 else caps[i][1]
caps[-1][1] = min(caps[-1][1] + 0.4, DUR)
def ts(x):
    cs = int(round(x * 100)); return f"{cs//360000}:{cs//6000%60:02d}:{cs//100%60:02d}.{cs%100:02d}"
ass = ["[Script Info]", "ScriptType: v4.00+", "PlayResX: 1080", "PlayResY: 1920", "",
 "[V4+ Styles]", "Format: Name, Fontname, Fontsize, PrimaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
 "Style: Cap,Product Sans Black,90,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,-1,0,1,0,0,5,0,0,0,1", "",
 "[Events]", "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"]
for a, b, txt in caps:
    ass.append(f"Dialogue: 0,{ts(a)},{ts(b)},Cap,,0,0,0,,{{\\pos(540,1472)}}{txt}")
open("captions.ass", "w").write("\n".join(ass) + "\n")
json.dump({"keep": keep, "dur": DUR}, open("cut.json", "w"), indent=1)
import os
R = lambda *a: subprocess.run(["ffmpeg", "-v", "error", "-y", *a], check=True)
if not os.path.exists("plate.mp4"):
    R("-threads", "2", "-i", "in/raw.mp4", "-vf", "scale=1080:1920,fps=30,setsar=1",
      "-c:v", "libx264", "-crf", "16", "-preset", "fast", "-g", "15", "-c:a", "pcm_s16le", "plate.mov".replace(".mov",".mkv"))
    os.rename("plate.mkv", "plate.mp4.mkv"); os.rename("plate.mp4.mkv", "plate.mkv"); open("plate.mp4","w").close()
os.makedirs("seg", exist_ok=True)
with open("seg/list.txt", "w") as L:
    for k, (a, b) in enumerate(keep):
        R("-ss", f"{a:.3f}", "-i", "plate.mkv", "-t", f"{b-a:.3f}",
          "-af", f"afade=t=in:d=0.008,afade=t=out:st={b-a-0.008:.3f}:d=0.008",
          "-c:v", "libx264", "-crf", "16", "-preset", "fast", "-c:a", "pcm_s16le", f"seg/{k:02d}.mkv")
        L.write(f"file '{k:02d}.mkv'\n")
R("-f", "concat", "-safe", "0", "-i", "seg/list.txt", "-i", "underlay.png", "-filter_complex",
  "[1:v]scale=1040:450[pl];[0:v][pl]overlay=20:1247,subtitles=captions.ass:fontsdir=fonts,fps=30[out]",
  "-map", "[out]", "-map", "0:a", "-t", f"{DUR:.3f}", "-c:v", "libx264", "-crf", "18", "-preset", "medium",
  "-pix_fmt", "yuv420p", "-r", "30", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "REEL-41.mp4")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "REEL-41.mp4", "-vf", "scale=540:960",
  "-c:v", "libx264", "-crf", "30", "-c:a", "aac", "-b:a", "96k", "REEL-41-preview.mp4"], check=True)
print("DUR", DUR, "segments", len(keep), "caps", len(caps))
