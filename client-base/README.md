# Reel editing base

The reusable part of Ruta's reel pipeline, for **every client**. It is
Ruta's `reel-editor-machine` (and Marina's editor built from it) split in two:

| layer | files | changes per client? |
|---|---|---|
| **BASE** (the editing) | `RULES.md`, `tools/` (all but `look.py`), `reel-00/`, `.claude/`, `assets/sfx/`, `assets/emoji/README.md`, `hf`, `.gitignore` | **never.** Copied as is |
| **LOOK** (the design) | `LOOK.md`, `tools/look.py`, `assets/fonts/`, `refs/`, `broll/CATALOG.md`, the client's name in `CLAUDE.md` / `README.md` / the `/reel` skill | **yes.** Filled from the client's own reels |

The base holds everything that makes the edit right: pauses found from the
audio **and** the transcript, bad takes (last take wins), framing steps,
closeups as `NO_PAINT`, transcript spelling on whisper timing, caption
blackout / invert, takeovers, **safe zones** (never on her face, never in a
corner, clear of Instagram's UI), the animation rule, what Ruta flags in
review, sound effects, cloud check / render / verify.

The look holds what makes it *hers*: palette, fonts, caption style (a phrase,
a word, or typing on), materials, where her refs put things, pace.

**Cutting rule (Ruta, 2026-11-05):** under 3 minutes; cut only pauses and bad
takes, per Ruta's instructions and the transcript; never cut content. No
length targets. **Transcription:** local whisper, OpenRouter whisper as the
fallback, never ElevenLabs (and not the video-use skill).

## New client in 6 steps

1. Copy this folder to `clients/<name>/<name>-reel-editor/`.
2. Pull 5–10 of **her own** reels (Apify `apify/instagram-reel-scraper`,
   her handle), make a contact sheet per reel (a frame every 1.5 s) and read
   them scene by scene into `refs/REFERENCES.md` (template in `refs/`).
3. Fill `LOOK.md` from the refs: palette (sample the pixels), fonts (render
   candidates next to a crop of her frame and pick the match), caption
   style/size/height, materials, zones, pace. Only what her reels do or what
   Ruta / the client said. No taste, no invented rules.
4. Put the fonts in `assets/fonts/` (local woff2 + `fonts.css`).
5. Write `tools/look.py`: `TOKENS`, `SURFACES`, `CAPTION_CSS`, `LOOK`.
6. Put her name in `CLAUDE.md`, this README's title and the `/reel` skill;
   test one frame (`npx hyperframes snapshot`) against a ref frame.

Worked examples: `clients/marina/marina-reel-editor` (phrase captions, serif)
and `clients/iryna/iryna-reel-editor` (typing captions, gold script).

## The pipeline (base)

```
Ruta drops the raw take into raw/
  → utt          tools/utt.py — silences + whisper per spoken span (utt.jsonl)
  → takes        tools/takes.py — restart candidates → work/rNN/script.txt
  → cut          tools/cut.py — pauses squeezed, bad takes dropped (last take wins),
                 framing step on every cut, closeups → reel-NN/assets/voice.mp4
  → align        tools/align.py — transcript spelling onto the real timing
  → author       reel-NN/build.py emits index.html: captions + beats (look from tools/look.py)
  → sfx          tools/sfx.py mix NN → reel-NN/assets/base.mp4
  → check        tools/cloudqa.py reel-NN --at <times>   (cloud)
  → render       tools/hfrender.py reel-NN               (HeyGen cloud)
  → verify       reel-verify subagent: frames = DUR×30, no black tail, audio
```

```bash
sh tools/newreel.sh 01 raw/<file>
python tools/utt.py 01
python tools/takes.py 01                        # then write work/r01/script.txt
python tools/cut.py 01                          # read work/r01/cut.txt
python tools/cut.py 01 --render
python tools/align.py work/r01/words.json work/r01/script.txt work/r01/captions.json
cd reel-01 && python build.py && python ../tools/sfx.py mix 01
cd .. && python tools/cloudqa.py reel-01 --at 2,10,20
python tools/hfrender.py reel-01
```

## What the base changed from Marina's editor (and nothing else)

- `STYLE.md` split into `RULES.md` (base, Ruta's rules as is, plus a §3 that
  collects the safe-zone rules in one place) and `LOOK.md` (the client).
- `tools/kit.py`: the look moved out to `tools/look.py`; captions gained a
  mode (`phrase` = Marina, `type` = typing on with a cursor, `word` = Ruta's
  one word). Timing, blackout, invert, scrim, matte, emoji: as is.
- `tools/cut.py`: reads the raw file's real size (rotation applied) instead
  of a hard-coded 1080×1920. Logic as is.

## Machine notes (as in Ruta's repo)

- whisper `medium`, ffmpeg and Node (for `npx hyperframes`) must be installed.
- On Ruta's laptop: whisper in Python 3.13, npm via `./hf`. On another machine
  `./hf` may need its PATH line removed.
- Video and audio are gitignored; the sound-effects kit is kept.
