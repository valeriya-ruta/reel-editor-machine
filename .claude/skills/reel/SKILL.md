---
name: reel
description: Build one of Ruta's Instagram reels end to end, from her delivered cut to a finished MP4 in her hands. Use whenever she hands over a reel — a file, a Drive link, or just a reel number. Covers the whole run: transcribe, align the script, author the beats, render, verify, deliver. Silent by default; she gets one message at the end.
---

# Reel

**Whose reel?** This skill and `STYLE.md` are Ruta's. If the footage, the
request or the path says Nika (anything under `Nika/`, UNLOCK ads), drop this
skill's look and work from `Nika/README.md`. If nothing says whose it is, ask
one line before touching anything. That counts as *her input alone* below.

She records, cuts and colour-grades. This builds everything on top — animations,
word-by-word captions, the render — and hands her back a finished file.

**Read [`STYLE.md`](../../../STYLE.md) before authoring anything.** It is the
design contract and it wins over instinct every time. This skill is the *run*;
STYLE.md is the *look*.

## The deal

- She delivers a cut, graded, **subtitle-free** plate. Never re-cut her footage.
- Captions come from `SCRIPTS.md`, never from ASR. Whisper supplies timing only.
- Product Sans Black, white only, word by word, unless an animation replaces the
  words entirely.
- 30 fps from reel 4 onward.
- Output: `REEL-NN.mp4` on her Desktop plus a small `REEL-NN-preview.mp4`.

## Silence

She hands the reel over and the next thing she hears is that it's done. No
check-ins, no progress reports, no "should I…", no summary of what was fixed.
Decide it and write it into the repo.

Speak mid-run for exactly three things, one line each, then keep building on the
best assumption rather than waiting:

- **money** — something is about to cost her, or a plan/quota ran out
- **time** — something will make her wait materially longer than usual
- **her input alone** — a wording call, a missing asset, a credential

A design question is not her input. Pick the answer STYLE.md implies.

## The run

Reel N lives in `reel-0N/`, its intermediates in `work/rN/`.

```bash
export PATH="/c/Users/Ruta/AppData/Roaming/npm:$PATH"   # or use ./hf

# 1. plate — hers, untouched. Normalise only if it is 4K/HEVC.
ffmpeg -i <hers> -c:v libx264 -crf 18 -vf scale=1080:1920 -r 30 reel-0N/assets/base.mp4

# 2. words — whisper is in Python 3.13, not bare `python`
~/AppData/Local/Programs/Python/Python313/python.exe tools/asr.py \
    work/rN/audio.wav work/rN/words.json medium

# 3. captions — script spelling onto her real timing; settle any REVIEW lines
python tools/align.py work/rN/words.json work/rN/script.txt work/rN/captions.json

# 4. author — build.py is the source of truth; index.html is generated
cd reel-0N && python build.py && ../hf check

# 5. render
../hf cloud render
```

`tools/kit.py` holds the shared surfaces, tokens and squircles — build beats out
of it rather than hand-rolling CSS, and it keeps STYLE.md §5a satisfied for free.
**`tools/gstyle.py` is the look (STYLE.md §00, the default since 2026-10-28)** —
Google style + Excalidraw sketches: white cards and chips above her, big white
words behind her, the white half-screen panel (the video pushes down 330 px),
the white full-screen cover, rough.js sketches, Google Sans, white and
`#7A1424` only. `reel-54/build.py` is the latest worked example. The refined-glass
look (`tools/glass.py`, burgundy ground, iris takeovers) is **archived** —
`archive/STYLE-refined-glass.md` — and never used for a new reel unless she asks.
`tools/matte.py` cuts her out of a span so a **big** graphic can sit behind her
(§1) — per beat only, ~3.3 s/frame on CPU.

## Verify before delivering

Non-negotiable, and cheap:

- `check` passes with 0 errors
- rendered frame count equals `DUR × 30` exactly — a short render means a
  truncated tail, which is the one failure she will notice immediately
- no black tail, no missing audio
- spot-check one frame per beat

## Deliver

Her Desktop, then `SendUserFile` both files. Once rclone has write scope, also
`rclone copy` to `gdrive:Reels inbox/Done`. Commit the reel and push.

**The full-quality 1080p file is what she posts, so it always reaches her.**
A review page (artifact) can only hold ~15 MB per file, so it carries 720p
previews: every label, button and download filename on it says *preview, not
for posting* (`REEL-NN-PREVIEW-720p.mp4`), and the full files go to her in the
same message via `SendUserFile`. On 2026-10-21 she posted the 720p copies from
the 41–52 page because the page only said "review copies" in small print.

One closing message: it's done, here it is, and anything that changed about
*her* side — a line she improvised, a beat that needed a different treatment.
Not what broke internally.

## Keep the run cheap

Cost is `calls × context`, so it grows quadratically inside a long session.
Reels 4+5 in one 7.8h session: mean 474k context, 2,214 calls, 1.05B cache-read
tokens — the last hour cost ~15× the first for the same kind of work.

- **One reel, one session.** This skill briefs a cold session completely. Clear
  between reels, and between authoring and verifying.
- **Verification goes in a subagent.** ~70% of calls are `ffprobe` / `ls` /
  `check` / frame counts. In a subagent they run in a fresh ~20k context and come
  back as one paragraph. A cheap model is fine there. Authoring beats and
  diagnosing a bad frame is not — that stays here.
- **Probe pixels, don't eyeball frames.** A numeric sample answers in ~50 tokens
  and stays answered; a screenshot costs ~1.6k and is re-read on every later
  call. Confirm with an image at the end, never while hunting.
- **`Edit`, never re-`Write`.** A full `build.py` rewrite parks 10–24k tokens in
  context for good.

## Machine notes

- **Two Pythons.** whisper in **3.13**; Pillow and everything else in **3.10**,
  which is what bare `python` resolves to. Name the interpreter.
- **npm in `C:\Program Files\nodejs` is broken.** Use `./hf`, or prepend
  `/c/Users/Ruta/AppData/Roaming/npm` to `PATH`.
- Local renders need `--low-memory-mode`; her disk runs near full.
- Cloud renders bill to the **free** HeyGen plan via OAuth, not the API wallet.
- Emoji must be `<img>`, never glyphs — the cloud renderer has Noto, so a literal
  emoji ships as the Android one. `Kit.emoji()` + `assets/emoji/`.
