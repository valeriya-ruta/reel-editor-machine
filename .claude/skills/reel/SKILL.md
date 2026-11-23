---
name: reel
description: Build one of Ruta's Instagram reels end to end, from her delivered cut to a finished MP4 in her hands. Use whenever she hands over a reel — a file, a Drive link, or just a reel number. Covers the whole run: transcribe, align the script, author the beats, render, verify, deliver. Silent by default; she gets one message at the end.
---

# Reel

**Whose reel?** This skill and `RUTA/STYLE.md` are Ruta's, and everything of
hers lives under `RUTA/`: run every path below from inside it. If the footage, the
request or the path says Nika (anything under `Nika/`, UNLOCK ads), drop this
skill's look and work from `Nika/README.md`. If nothing says whose it is, ask
one line before touching anything. That counts as *her input alone* below.

She records, cuts and colour-grades. This builds everything on top — animations,
word-by-word captions, the render — and hands her back a finished file.

**Read [`RUTA/STYLE.md`](../../../RUTA/STYLE.md) before authoring anything.** It is the
design contract and it wins over instinct every time. This skill is the *run*;
STYLE.md is the *look*.

## The deal

- She delivers a cut, graded, **subtitle-free** plate. Never re-cut her footage.
- Captions take their spelling from her script (the RUTA app), never from ASR. Whisper supplies timing only.
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

Reel N lives in `RUTA/reel-0N/`, its intermediates in `RUTA/work/rN/`.

The steps are in **`RUTA/BUILD-BRIEF.md`** (script from the RUTA app → cut →
captions → plan → `build.py` from reel-61's skeleton → sound mix → cut-outs →
check → local render → verify → post). For a batch, give each reel to a builder
subagent with that file and its number; keep posting, RUTA and the review
artifact here.

On her laptop: `./hf` instead of `npx hyperframes`, Python 3.13 for whisper.
In a cloud session: `tools/asr_fw.py` / faster-whisper, `MATTE_REMBG=1` for
cut-outs, the hyperframes CLI installed with `npm i --ignore-scripts`.

**The look is locked (2026-11-23): STYLE.md §00 + "Her review of reel 61".**
One look only — `tools/gstyle.py`, white + `#7A1424`, Google Sans; big white words
behind her (matte), the half screen for schemes (Excalidraw only there), full-screen
platform-ad sequences for real UI (3D tilt, smooth zooms, the UI rebuilt in HTML),
a little glass, lists as a card `shuffle`, the CTA pill in the subtitle band. Not
every phrase gets a graphic. **`reel-61/build.py` is the worked example and
`BUILD-BRIEF.md` the standing brief** (a builder subagent gets that file and its
reel number). Every other look is in `archive/` and never used unless she asks for
it by name. `tools/matte.py` cuts her out (≈1 s/frame on the cloud box with
`MATTE_REMBG=1`). The ТЕСТ CTA is always cut out of the reel.

**Memes (her rule, 2026-11-23): every reel gets 1-3 reaction memes as comic relief.**
Pick from `RUTA/assets/memes/MEMES.md` (index + rules: max 3, a pair only with a long break
between animations, never in the CTA, profanity fine, first 3 s fine) and place them with
`g.meme()` in `tools/gstyle.py`; `BUILD-BRIEF.md` says how.

**Render locally, never HeyGen** (her call, 2026-11-20): from `RUTA/`,
`sh work/b1021/heavy.sh <hyperframes> render reel-NN -o reel-NN/renders/REEL-NN.mp4 --workers 3 --low-memory-mode`.
Every heavy step (cut, sound mix, matte, render) goes through `heavy.sh` — two
overlapping sound mixes corrupted a plate on 2026-11-23 (frozen, out-of-sync render).

## Verify before delivering

Non-negotiable, and cheap:

- `check` passes with 0 errors
- rendered frame count equals `DUR × 30` exactly — a short render means a
  truncated tail, which is the one failure she will notice immediately
- no black tail, no missing audio
- spot-check one frame per beat
- the plate (`assets/base.mp4`) and the render decode with zero errors, and the
  render is in sync with the plate (face-crop PSNR peaks at the same time, not
  ±0.4 s — `BUILD-BRIEF.md` step 10)

## Deliver

Post through Buffer from her Cloudinary (see `BUILD-BRIEF.md`, "After the
render"), keep RUTA's status and dates in step, add the reel to the review
artifact. Her Desktop, then `SendUserFile` both files. Once rclone has write scope, also
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
- No HeyGen at all — not for renders, not for hosting (her call, 2026-11-20). Render locally; host for Buffer on her Cloudinary.
- Emoji must be `<img>`, never glyphs — the cloud renderer has Noto, so a literal
  emoji ships as the Android one. `Kit.emoji()` + `assets/emoji/`.
