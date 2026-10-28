# Reel 41 cut: word-index ranges of the "better" take, kept in order.
# Within a range, any pause longer than GAP is closed to a short breath.
import json, sys
W = json.load(open("better.words.json"))["words"]
KEEP = [
 (0, 30, "hook: plan the week with my AI producer; who I am"),
 (31, 60, "the system: analyses, ideas, edits, designs, posts"),
 (67, 103, "nobody shows how it physically happens — I will"),
 (129, 150, "proof: +300 followers a week, DMs"),
 (194, 234, "step 1: analyses everything, especially last week"),
 (244, 256, "stats and scripts"),
 (266, 286, "which hooks, topics, formats, CTAs worked"),
 (287, 297, "step 2: it looks for ideas"),
 (306, 335, "from consultations, calls, Threads"),
 (336, 352, "while it works I type my ideas"),
 (362, 371, "for example"),
 (388, 423, "numbered list, I pick 14-15, into the Ruta app"),
 (424, 438, "open on the phone, each script with no text"),
 (452, 462, "I record a voice note"),
 (508, 534, "14 scripts in 15-20 min; voila"),
 (535, 544, "next day: makeup, dress"),
 (552, 559, "film all 14 at once"),
 (560, 577, "upload to Drive, link into Claude Code"),
 (584, 593, "Claude edits in my style"),
 (614, 644, "courses say keep the laptop open; «а я знаю»"),
 (645, 670, "schedules 2/day, IG + TikTok"),
 (684, 703, "I don't even rewatch them"),
 (795, 808, "that's the whole system"),
 (809, 836, "CTA: consultation or done-for-you"),
 (847, 862, "write + in the comments"),
]
GAP, PRE, POST = 0.22, 0.08, 0.12
segs = []
for a, b, _ in KEEP:
    s = W[a]["s"]
    for i in range(a, b):
        if W[i+1]["s"] - W[i]["e"] > GAP:
            segs.append((s - PRE, W[i]["e"] + POST)); s = W[i+1]["s"]
    segs.append((s - PRE, W[b]["e"] + POST))
segs = [(max(0, round(x, 3)), round(y, 3)) for x, y in segs]
# merge overlaps
out = [list(segs[0])]
for x, y in segs[1:]:
    if x <= out[-1][1]: out[-1][1] = max(out[-1][1], y)
    else: out.append([x, y])
json.dump(out, open("cut.json", "w"), indent=0)
tot = sum(y - x for x, y in out)
print("segments", len(out), "plate %.1f s" % tot)
