"""Client review (відгук про консультацію) — tight cut + phrase captions + static label.

    python3 review-01/build.py <src.mp4> <out.mp4>      (run from RUTA/)

Cut list is in source seconds. The on-screen video span (33.2-50.65) is kept whole.
Captions: 2-4 words a line, UPPERCASE, Google Sans 700 at 64 px (house is 90 px word by
word; this brief asked smaller phrases), white on the underlay. A static label at half
the caption size sits above them for the whole reel.
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC, OUT = sys.argv[1], sys.argv[2]
WORDS = json.load(open(os.path.join(HERE, "words.json"), encoding="utf-8"))["words"]

KEEP = [  # (start, end) in source seconds
    (0.36, 3.50),    # Дякую, що пояснила, як можна простіше монтувати відео,
    (3.52, 8.94),    # бо коли всі говорять ... пам'яті то і немає,
    (10.98, 12.80),  # ось твій спосіб реально працює.
    (12.82, 15.36),  # Ми вже змонтували перше відео, перший варіант,
    (15.36, 17.08),  # навіть те, що ми його ще нічому не вчили,
    (19.14, 22.58),  # дуже нормальний, якби мені було все одно, я б його запостила.
    (24.66, 27.26),  # А покажи зараз відео, як змонтували.
    (33.20, 50.66),  # the video on screen, whole, + "Клас ... хтось монтував, до речі?"
    (51.18, 52.82),  # Це відео я сама монтувала.
    (53.38, 56.40),  # Взагалі, все, я тобі зберегла півгодини часу.
]

# Spelling fixes over ASR (index -> text); merged tokens are joined below.
FIX = {63: "нормальний,", 140: "півгодини", 72: "запостила.", 87: "змонтували."}
CAP = 72
LABEL = CAP // 2
LABEL_TEXT = "ВІДГУК ПРО КОНСУЛЬТАЦІЮ"

# --- words inside the cut, merged (apostrophe splits), remapped to output time
words = []
for i, w in enumerate(WORDS):
    t = FIX.get(i, w["w"])
    if words and (t.startswith("'") or t.startswith("-")):
        words[-1]["w"] += t
        words[-1]["e"] = w["e"]
        continue
    words.append({"w": t, "s": w["s"], "e": w["e"]})


def remap(t):
    off = 0.0
    for a, b in KEEP:
        if a - 0.06 <= t <= b + 0.06:
            return off + min(max(t, a), b) - a
        off += b - a
    return None


kept = []
for w in words:
    mid = (w["s"] + w["e"]) / 2
    seg = next((k for k, (a, b) in enumerate(KEEP) if a <= mid <= b), None)
    if seg is None:
        continue
    kept.append({"w": w["w"].upper(), "s": remap(w["s"]), "e": remap(w["e"]), "seg": seg})

# --- phrases: 2-3 words a line (her brief). Break at a cut, a full stop or a
# pause; three words only when they fit (<= 18 chars); never end a line on a
# one/two-letter word; a lone leftover word joins the line before it if it fits.
MAXC = 18
phrases, cur = [], []
for k, w in enumerate(kept):
    cur.append(w)
    nxt = kept[k + 1] if k + 1 < len(kept) else None
    text = " ".join(x["w"] for x in cur)
    hard = (nxt is None or nxt["seg"] != w["seg"] or w["w"][-1] in ".?!"
            or nxt["s"] - w["e"] > 0.45)
    full = len(cur) >= 3 or (nxt is not None and len(text) + 1 + len(nxt["w"]) > MAXC) \
        or (len(cur) >= 2 and w["w"][-1] == ",")
    if hard or full:
        if not hard and len(cur) > 1 and len(w["w"]) <= 2:
            phrases.append(cur[:-1]); cur = [w]
        else:
            phrases.append(cur); cur = []
merged = []
for p in phrases:
    if (len(p) == 1 and merged and len(merged[-1]) < 3 and p[0]["seg"] == merged[-1][-1]["seg"]
            and merged[-1][-1]["w"][-1] not in ".?!"
            and len(" ".join(x["w"] for x in merged[-1] + p)) <= MAXC + 2):
        merged[-1] += p
    else:
        merged.append(p)
phrases = merged
# no flashes: a line that would be up < 0.4 s takes the next line in (3 words max)
k = 0
while k < len(phrases) - 1:
    p, q = phrases[k], phrases[k + 1]
    if (q[0]["s"] - p[0]["s"] < 0.4 and q[0]["seg"] == p[-1]["seg"]
            and len(p) + len(q) <= 3 and p[-1]["w"][-1] not in ".?!"):
        phrases[k] = p + q
        del phrases[k + 1]
    elif (q[0]["s"] - p[0]["s"] < 0.4 and q[0]["seg"] == p[-1]["seg"]
            and len(p) < 3 and len(q) > 1):
        phrases[k] = p + q[:1]          # borrow one word so p stays up long enough
        phrases[k + 1] = q[1:]
        k += 1
    else:
        k += 1

DUR = sum(b - a for a, b in KEEP)


def ts(t):
    t = max(0, t)
    return "%d:%02d:%02d.%02d" % (t // 3600, t % 3600 // 60, int(t % 60), round(t * 100) % 100)


# Our normal captions (kit.py): Product Sans Black, white, flat, centred on y 1472,
# on the underlay. Smaller than the usual 90 px because a line holds 2-3 words.
CAP_Y = 1472
events = []
for k, p in enumerate(phrases):
    s = p[0]["s"]
    e = p[-1]["e"] + 0.25
    if k + 1 < len(phrases):
        e = min(e, phrases[k + 1][0]["s"])
    text = " ".join(x["w"] for x in p).rstrip(",")
    events.append("Dialogue: 0,%s,%s,Cap,,0,0,0,,{\\an5\\pos(540,%d)\\blur6}%s" % (ts(s), ts(e), CAP_Y, text))
# label: half the caption size, just above the caption line, never moves
LABEL_Y = CAP_Y - CAP // 2 - 22 - LABEL // 2
events.append("Dialogue: 1,%s,%s,Label,,0,0,0,,{\\an5\\pos(540,%d)\\blur4}%s" % (ts(0), ts(DUR + 1), LABEL_Y, LABEL_TEXT))

ass = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Product Sans Black,%d,&H00FFFFFF,&H00FFFFFF,&H60000000,&H00000000,0,0,0,0,100,100,-1,0,1,4,0,5,40,40,0,1
Style: Label,Product Sans Black,%d,&H00FFFFFF,&H00FFFFFF,&H60000000,&H00000000,0,0,0,0,100,100,1,0,1,3,0,5,40,40,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
""" % (CAP, LABEL)
ass += "\n".join(events) + "\n"
assp = os.path.join(os.path.dirname(os.path.abspath(OUT)), "captions.ass")
open(assp, "w", encoding="utf-8").write(ass)
print("phrases:", len(phrases), "dur: %.2f" % DUR)
for p in phrases:
    print("  %.2f  %s" % (p[0]["s"], " ".join(x["w"] for x in p)))

# --- render: cut each segment alone (one HEVC decode at a time), concat, then
# one pass for underlay + captions
tmp = os.path.join(os.path.dirname(os.path.abspath(OUT)), "seg")
os.makedirs(tmp, exist_ok=True)
lst = []
for k, (s, e) in enumerate(KEEP):
    f = os.path.join(tmp, "s%02d.mp4" % k)
    d = e - s
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", "%.3f" % s, "-i", SRC, "-t", "%.3f" % d,
                    "-vf", "scale=1080:1920,fps=30", "-af",
                    "afade=t=in:d=0.02,afade=t=out:st=%.3f:d=0.03" % (d - 0.03),
                    "-c:v", "libx264", "-crf", "14", "-preset", "fast", "-pix_fmt", "yuv420p",
                    "-c:a", "pcm_s16le", "-ar", "48000", f.replace(".mp4", ".mov")], check=True)
    lst.append("file '%s'" % f.replace(".mp4", ".mov"))
open(os.path.join(tmp, "list.txt"), "w").write("\n".join(lst) + "\n")
fontsdir = os.path.join(HERE, "..", "assets", "fonts")
fc = ("[1:v]scale=1040:450,format=rgba[ul];"
      "[0:v][ul]overlay=20:1247:shortest=1[cu];[cu]ass=%s:fontsdir=%s[outv]" % (assp, fontsdir))
subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i",
                os.path.join(tmp, "list.txt"), "-loop", "1", "-i",
                os.path.join(HERE, "..", "reel-08", "assets", "underlay.png"),
                "-filter_complex", fc, "-map", "[outv]", "-map", "0:a",
                "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-pix_fmt", "yuv420p",
                "-r", "30", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", OUT],
               check=True)
print("wrote", OUT)
