# reel-editor-machine

Ruta's reel pipeline. She records and cuts; this repo holds everything that
turns a cut into a finished, captioned, animated reel.

**Read [`STYLE.md`](STYLE.md) before touching a composition.** It is the
contract — palette, frame geometry, the animation rule, and §5a, the surface
system that decides whether a shape reads as 2013 flat or 2026 material.

## The pipeline

```
she records + cuts + grades        (her laptop, 5-10 min)
  → transcribe          whisper, word-level timings
  → normalise           4K HEVC → 1080p H.264 plate   (skippable if she records 1080 H.264)
  → align               tools/align.py — script spelling onto ASR timing
  → author              build.py emits index.html: captions + beats
  → render              HeyGen cloud, ~11 min, ~$0.17   (or local, ~25 min)
  → post                Windsor → Instagram, from the render's public URL
  → track               Reels Planner: status, posted link, insights
```

## Layout

| path | what |
|---|---|
| `STYLE.md` | **the contract.** Delivery model, captions, geometry, animation rule, surfaces |
| `SCRIPTS.md` | all six scripts as written and read. The spelling authority |
| `ANIMATION-PROCESS.html` | the design playbook — how a beat is specified |
| `tools/align.py` | binds script spelling to ASR timing; separates whisper's mangling from her improvisation |
| `tools/squircle.py` | continuous-curvature corners as a `clip-path` (STYLE.md §5a.1) |
| `tools/asr.py` | whisper wrapper, word-level timestamps |
| `reel-03/` | reel 3 — «дизайн без Фігми». `build.py` generates `index.html` |
| `assets/` | her logos and fonts |

## Building a reel

```bash
python tools/asr.py <audio.wav> work/<reel>/words.json medium
python tools/align.py work/<reel>/words.json work/<reel>/script.txt work/<reel>/captions.json
cd reel-NN && python build.py && npx hyperframes check
npx hyperframes cloud render          # or: npx hyperframes render --low-memory-mode
```

`build.py` is the source of truth for a reel — `index.html` is generated and
should never be hand-edited.

## Machine notes

- **Two Python installs.** whisper lives in **3.13**
  (`~/AppData/Local/Programs/Python/Python313/python.exe`), Pillow in **3.10**,
  which is what bare `python` resolves to. Name the interpreter explicitly.
- **npm in `C:\Program Files\nodejs` is broken.** Prepend the working one:
  `export PATH="/c/Users/Ruta/AppData/Roaming/npm:$PATH"` — see `hf`.
- Local renders need `--low-memory-mode`; disk runs near full, so clear the
  HyperFrames frame cache between batches.
- Video and audio are gitignored. Footage moves outside the repo.
