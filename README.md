# reel-editor-machine

Ruta's reel pipeline. She records and cuts; this repo holds everything that
turns a cut into a finished, captioned, animated reel.

**Read [`STYLE.md`](STYLE.md) before touching a composition.** It is the
contract — palette, frame geometry, the animation rule, and §5a, the surface
system that decides whether a shape reads as 2013 flat or 2026 material.

## How this runs

She drops a reel; the next thing she hears is that it's done. No check-ins, no
progress reports, no mid-build questions. Everything about *how* it got built
lands in this repo, not in a message. Break silence only for money, her time, or
input only she has — one line, then keep building on the best assumption.

The pipeline is also billed by conversation length, not by work done: cost is
`calls × context`, so it grows quadratically inside one long session. Measured on
reels 4+5 — a single 7.8h session ran a mean context of 474k tokens across 2,214
calls and burned 1.05B cache-read tokens, ~15× more in its last hour than its
first for the same kind of work. Hence:

- **One reel, one session.** `STYLE.md` briefs a cold session completely; that is
  what it is for. Clear between reels, and between building and verifying.
- **Verification runs in a subagent.** ~70% of calls are `ffprobe` / `ls` /
  `hyperframes check` / frame counts. In a subagent they run in a fresh 20k
  context and return one paragraph, instead of re-reading a 500k main thread.
  A cheap model is fine for that half; authoring beats and diagnosing a bad
  frame is not.
- **Probe pixels, don't eyeball frames.** A numeric sample answers in 50 tokens
  and stays answered; a screenshot costs ~1.6k and is re-read on every later
  call. Reels 4+5 pulled in 136 of them. Confirm with an image at the end, not
  while hunting.
- **`Edit`, never re-`Write`.** A whole `build.py` rewrite parks 10–24k tokens in
  context permanently. `reel-03/build.py` went in three times.

`/reel` is installed twice: `.claude/skills/reel/` here (wins inside the repo,
versioned with the pipeline) and `~/.claude/skills/reel/` as a thin launcher so a
chat opened anywhere can still start one. **The launcher hard-codes this repo's
absolute path** — if the repo moves, update it. `.claude/agents/reel-verify.md`
is the cheap inspection subagent the run dispatches to.

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
| `STYLE.md` | **the contract** for Ruta's reels. Delivery model, captions, geometry, animation rule, surfaces |
| `Nika/` | **a separate client and style**: Nika's UNLOCK ads. Own contract in `Nika/README.md`; nothing in `STYLE.md` applies there |
| `SCRIPTS.md` | all six scripts as written and read. The spelling authority |
| `ANIMATION-PROCESS.html` | the design playbook — how a beat is specified |
| `tools/align.py` | binds script spelling to ASR timing; separates whisper's mangling from her improvisation |
| `tools/gstyle.py` | **the look** (STYLE.md §00): Google style + Excalidraw — layers, captions, sketches, motion |
| `archive/STYLE-refined-glass.md` | the archived refined-glass look (reels 12–40); `tools/glass.py` and `style-test/` belong to it |
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
