---
name: reel
description: Build one of <CLIENT>'s reels end to end, from her raw take to a finished MP4. Use whenever Ruta hands over a raw take or a reel number. Covers the run: transcribe, cut pauses and bad takes, align captions, author the beats in her look, render, verify.
---

# Reel (<CLIENT>)

Ruta's `/reel` from `reel-editor-machine`, on the shared editing base.
**Read [`RULES.md`](../../../RULES.md), [`LOOK.md`](../../../LOOK.md) and
[`README.md`](../../../README.md) first.** This skill is the *run*; RULES.md
is the editing contract, LOOK.md is her look.

## The deal

- Raw take in `raw/`. Cut **only pauses and bad takes**, never content; the
  reel stays under 3 minutes (RULES.md §1). No length targets.
- Last take wins; anything `cut.py` flags that the transcript doesn't settle goes to Ruta, not guessed.
- Captions: what she said, verbatim, in her caption style (LOOK.md §2b).
- Safe zones (RULES.md §3): never on her face, never in a corner, clear of
  Instagram's UI.
- 30 fps. Output `reel-NN/renders/REEL-NN.mp4`.

## When to ask (Ruta, 2026-11-20)

Anything not settled is asked, not decided. Decide every cut, take and beat
that RULES.md, LOOK.md, the transcript and the refs settle, and write each
call into `reel-NN/PLAN.md`. When they don't settle it (a bad take that may
be content, a missing real asset, a call no rule covers), ask Ruta, then
carry on. No editing plan for approval and no check-ins beyond that.

## The run

Reel N lives in `reel-NN/`, its intermediates in `work/rNN/`.

1. `sh tools/newreel.sh NN raw/<file>`.
2. `python tools/utt.py NN` (whisper medium). Then `python tools/takes.py NN`:
   write `work/rNN/script.txt` = the transcript with the fumbled earlier
   attempts deleted (repeats on purpose are content: keep).
3. `python tools/cut.py NN` → read `work/rNN/cut.txt` (every clip with its
   words, every dropped take, flags). Manual calls in `cut-fix.json`
   (`drops`, `keeps`, `punch`, `wide` = every clip a graphic sits on).
   `python tools/gapcheck.py NN` → 0. Then `python tools/cut.py NN --render`.
4. `python tools/align.py work/rNN/words.json work/rNN/script.txt work/rNN/captions.json`;
   settle the REVIEW lines; whisper errors into `FIX_AT` in `build.py`.
5. `python tools/facemap.py NN --flat` → `work/rNN/face_flat.json`.
6. Author `reel-NN/build.py` from `reel-00/build.py`: beats anchored on words
   with `A()`/`X()`, placed with `under()` (never on her head), half-screens
   with `half()`, materials from `tools/look.py` (LOOK.md §5a), b-roll from
   `broll/CATALOG.md`, `BLACKOUT` only where a graphic says the word, nothing
   inside `NO_PAINT`. `python build.py` (fix every `fit:` line) and
   `python ../tools/sfx.py mix NN`.
7. One `python tools/matte.py ...` per half-screen (as build.py prints), then
   `python tools/halfscreen.py NN`, then `python tools/facemap.py NN`.
8. `python tools/review.py reel-NN`, `node tools/safezone.js reel-NN` (must be
   empty), `node tools/frames.js reel-NN --beats`, `npx hyperframes check`.
9. `npx hyperframes render` on the machine (not HeyGen).
10. Verify through the `reel-verify` subagent: frames = round(DUR×30), audio,
    no black tail. Deliver the 8 Mbps Instagram copy and the <100 MB
    Cloudinary copy (RULES.md §7).

## Keep the run cheap (Ruta's rule, as is)

One reel, one session. Verification in the subagent. Probe pixels, don't
eyeball frames. `Edit`, never re-`Write` `build.py`. Emoji as `<img>`.
