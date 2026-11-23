"""Phrase subtitles: her usual captions, 3-4 words at a time. A whole run in one command.

Use when she asks for "2-3 / 3-4 word subtitles", "phrase subtitles", or "just
put subtitles, nothing else". The DEFAULT for reels is still one word at a time
(STYLE.md §2b via gstyle.py); this is the opt-in variant (STYLE.md §2c).

Look is identical to the one-word captions — nothing changed but the grouping:
  Product Sans Black, UPPERCASE, punctuation kept, flat white (no stroke, no
  shadow), tracking -0.015em, centred, vertical centre y=1472, on the dark
  underlay plaque (1040x450 at 20,1247; fades in 0.5 s, out 0.6 s).
  Size 68 px instead of 90 (~25% smaller) so a 3-4 word line fits.
Grouping: up to 4 words, line <= 880 px; break after . ? ! and after a comma
  once the line has 3 words; a lone last word joins the previous line.
Timing: a phrase shows from its first word to its last word (+0.15 s), clamped to
  end 0.085 s before the next phrase.
Pauses: gentle. Trim only dead air at the start (first word - 0.15 s) and end
  (last word + 0.35 s); in the middle only a gap over 0.9 s is shortened, to
  0.4 s. Her pacing is proper already — do not cut harder.

    python3 tools/phrasecaps.py <in.mp4> <out.mp4> [--words words.json]
        [--fix fix.json] [--size 68] [--model medium]

--words  reuse a words.json (tools/asr_fw.py format); otherwise transcribe it.
--fix    {"asr text": "right text"} applied to words (single or multi-word keys,
         e.g. {"відео, юз,": "video-use"}). Spelling from SCRIPTS.md wins over ASR.
Prints every phrase with its time, so wording can be checked before delivery.
"""
import argparse, json, os, subprocess, sys, tempfile
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "..", "assets", "captions")
FONT = os.path.join(ASSETS, "ProductSans-Black.woff")
PLAQUE = os.path.join(ASSETS, "underlay.png")
CY, MAXW, TRACK = 1472, 880, -0.015

ap = argparse.ArgumentParser()
ap.add_argument("src"); ap.add_argument("out")
ap.add_argument("--words"); ap.add_argument("--fix")
ap.add_argument("--size", type=int, default=68)
ap.add_argument("--model", default="medium")
a = ap.parse_args()
tmp = tempfile.mkdtemp(prefix="phrasecaps-")

if not a.words:
    a.words = os.path.join(tmp, "words.json")
    subprocess.run([sys.executable, os.path.join(HERE, "asr_fw.py"), a.src, a.words, a.model], check=True)
W = [dict(w) for w in json.load(open(a.words, encoding="utf-8"))["words"]]

# merge split apostrophes («п» + «'я»), strip leading hyphens
M = []
for w in W:
    w["w"] = w["w"].strip()
    if M and w["w"][:1] in "'’": M[-1]["w"] += w["w"]; M[-1]["e"] = w["e"]
    elif w["w"]: M.append(w)
W = M
if a.fix:
    fix = json.load(open(a.fix, encoding="utf-8"))
    for k, v in sorted(fix.items(), key=lambda kv: -len(kv[0].split())):
        ks = k.split(); n = len(ks); i = 0; R = []
        while i < len(W):
            if [x["w"] for x in W[i:i + n]] == ks:
                R.append({"w": v, "s": W[i]["s"], "e": W[i + n - 1]["e"]}); i += n
            else: R.append(W[i]); i += 1
        W = R

dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                            "-of", "csv=p=0", a.src], capture_output=True, text=True).stdout)
# gentle pause trim
segs = []
for i, w in enumerate(W):
    s = max(0.0, w["s"] - (0.15 if i == 0 else 0.2))
    e = min(dur, w["e"] + (0.35 if i == len(W) - 1 else 0.2))
    if segs and s - segs[-1][1] < 0.5: segs[-1][1] = max(segs[-1][1], e)
    else: segs.append([s, e])
def tmap(t):
    acc = 0.0
    for s, e in segs:
        if t < s: return acc
        if t <= e: return acc + t - s
        acc += e - s
    return acc
DUR = sum(e - s for s, e in segs)
for w in W: w["s"], w["e"] = tmap(w["s"]), tmap(w["e"]); w["w"] = w["w"].upper()

F = ImageFont.truetype(FONT, a.size); sp = TRACK * a.size
def width(t): return sum(F.getlength(c) + sp for c in t) - sp
def text(ws): return " ".join(x["w"] for x in ws)
ch, cur = [], []
for w in W:
    if cur and (len(cur) >= 4 or width(text(cur + [w])) > MAXW): ch.append(cur); cur = []
    cur.append(w)
    if w["w"][-1] in ".?!…" or (w["w"][-1] == "," and len(cur) >= 3): ch.append(cur); cur = []
if cur:
    if ch and len(cur) == 1 and len(ch[-1]) < 4 and width(text(ch[-1] + cur)) <= MAXW: ch[-1] += cur
    else: ch.append(cur)

ev = []
for k, c in enumerate(ch):
    s0, e0 = max(0.0, c[0]["s"]), c[-1]["e"] + 0.15
    if k + 1 < len(ch): e0 = max(c[-1]["e"], min(e0, ch[k + 1][0]["s"] - 0.085))
    t = text(c)
    im = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    x = 540 - width(t) / 2
    for g in t:
        d.text((x, CY), g, font=F, fill=(255, 255, 255, 255), anchor="lm"); x += F.getlength(g) + sp
    p = os.path.join(tmp, "c%03d.png" % k); im.save(p); ev.append((p, s0, e0))
    print("%6.2f-%6.2f  %s" % (s0, e0, t))

args = ["ffmpeg", "-v", "error", "-y", "-i", a.src, "-loop", "1", "-t", "%.3f" % DUR, "-i", PLAQUE]
for p, _, _ in ev: args += ["-i", p]
fc = []
for k, (s, e) in enumerate(segs):
    fc.append("[0:v]trim=%.3f:%.3f,setpts=PTS-STARTPTS,fps=30,scale=1080:1920,setsar=1[v%d]" % (s, e, k))
    fc.append("[0:a]atrim=%.3f:%.3f,asetpts=PTS-STARTPTS[a%d]" % (s, e, k))
fc.append("".join("[v%d][a%d]" % (k, k) for k in range(len(segs))) + "concat=n=%d:v=1:a=1[b][a]" % len(segs))
fc.append("[1:v]scale=1040:450,format=rgba,fade=in:st=%.2f:d=0.5:alpha=1,fade=out:st=%.2f:d=0.6:alpha=1[u]"
          % (max(0, ev[0][1] - 0.3), ev[-1][2] + 0.1))
fc.append("[b][u]overlay=20:1247:eof_action=pass[s0]")
for k, (p, s, e) in enumerate(ev):
    fc.append("[s%d][%d:v]overlay=0:0:enable='between(t,%.3f,%.3f)'[s%d]" % (k, k + 2, s, e, k + 1))
args += ["-filter_complex", ";".join(fc), "-map", "[s%d]" % len(ev), "-map", "[a]", "-t", "%.3f" % DUR,
         "-c:v", "libx264", "-crf", "18", "-preset", "fast", "-pix_fmt", "yuv420p",
         "-c:a", "aac", "-b:a", "192k", a.out]
subprocess.run(args, check=True)
print("OUT", a.out, "%.2fs" % DUR, "(trimmed %.2fs)" % (dur - DUR))
