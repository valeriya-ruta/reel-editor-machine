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
- Last take wins; anything `cut.py` flags goes to Ruta, not guessed.
- Captions: what she said, verbatim, in her caption style (LOOK.md §2b).
- Safe zones (RULES.md §3): never on her face, never in a corner, clear of
  Instagram's UI.
- 30 fps. Output `reel-NN/renders/REEL-NN.mp4`.

## Silence (Ruta's rule, as is)

She hands the take over and the next thing she hears is that it's done. No
questions, no editing plan for approval, no check-ins (Ruta, 2026-11-05: "dont
ask me — the instructions should be enough for you to take decisions"). Decide
every cut, take and beat from RULES.md, LOOK.md, the transcript and the refs,
and write each call into `reel-NN/PLAN.md`. Speak mid-run only for money (a
cloud render can't be paid) — nothing else. A bad take you are unsure of: keep
it (never cut content) and list it in the final message.

## The run

Reel N lives in `reel-NN/`, its intermediates in `work/rNN/`.

1. `sh tools/newreel.sh NN raw/<file>`.
2. `python tools/utt.py NN` (whisper medium). Then `python tools/takes.py NN`:
   write `work/rNN/script.txt` = the transcript with the fumbled earlier
   attempts deleted (repeats on purpose are content: keep).
3. `python tools/cut.py NN` → read `work/rNN/cut.txt` (every clip with its
   words, every dropped take, flags). Manual calls in `cut-fix.json`.
   Then `python tools/cut.py NN --render`.
4. `python tools/align.py work/rNN/words.json work/rNN/script.txt work/rNN/captions.json`;
   settle the REVIEW lines; whisper errors into `FIX` in `build.py`.
5. Author `reel-NN/build.py` from `reel-00/build.py`: beats anchored on words
   with `S()`/`E()`, materials from `tools/look.py` (LOOK.md §5a), b-roll
   from `broll/CATALOG.md`, `BLACKOUT` only where a graphic says the word,
   nothing inside `NO_PAINT`. `python build.py && python ../tools/sfx.py mix NN`.
6. `python tools/cloudqa.py reel-NN --at <one time per beat>` → 0 errors; fix.
7. `python tools/hfrender.py reel-NN` (cloud).
8. Verify through the `reel-verify` subagent: frames = round(DUR×30), audio,
   no black tail.

## Keep the run cheap (Ruta's rule, as is)

One reel, one session. Verification in the subagent. Probe pixels, don't
eyeball frames. `Edit`, never re-`Write` `build.py`. Emoji as `<img>`.
