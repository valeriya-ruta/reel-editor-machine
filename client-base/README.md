# Reel editing base (all clients)

Ruta's reel pipeline from `reel-editor-machine`, as it stands in her latest
Marina editor (2026-11-17), split into two layers:

| layer | files | changes per client? |
|---|---|---|
| **BASE** (no design in it) | `RULES.md`, `CLAUDE.md`, `tools/` (all but `look.py`), `reel-00/`, `.claude/`, `assets/sfx/`, `assets/emoji/`, `hf` | **never** |
| **LOOK** (all the design) | `LOOK.md`, `tools/look.py`, `assets/fonts/`, `refs/`, `broll/CATALOG.md` | yes: from the client's own reels |

The base has no fonts, colours, type sizes, stroke weights, element styling,
motion style or rhythm numbers. `tools/kit.py` takes every one of those from
`tools/look.py` (`TOKENS`, `SURFACES`, `CAPTION_CSS`, `LOOK`).

**Read [`RULES.md`](RULES.md) and [`LOOK.md`](LOOK.md) before touching a
composition.**

## New client in 6 steps

1. Copy this folder to `clients/<name>/<name>-reel-editor`. Don't edit the
   base files in the copy (names in `CLAUDE.md` and the skill aside).
2. Download her own reels (Apify), `python tools/refstudy.py` each one, and
   fill `refs/REFERENCES.md` scene by scene.
3. Fill `LOOK.md` from them only: captions, palette, type, materials, motion,
   rhythm, where things sit. Nothing that isn't in her reels or said by Ruta /
   the client.
4. Put her fonts in `assets/fonts/` (local woff2 + `fonts.css`).
5. Write `tools/look.py` to match `LOOK.md`.
6. Test: one snapshot of captions + a beat over a real plate, against a
   frame of her own reel.

## The pipeline

```
Ruta drops the raw take into raw/
  → utt        tools/utt.py — silences + whisper per spoken span (never ElevenLabs)
  → takes      tools/takes.py — restart candidates → work/rNN/script.txt
  → cut        tools/cut.py — pauses (audio + transcript, voice guard), last take wins,
               framing (base / in / punch, "wide" under graphics)
  → gapcheck   tools/gapcheck.py — no voice removed outside a manual drop (must be 0)
  → align      tools/align.py — transcript spelling onto the real timing
  → facemap    tools/facemap.py --flat — her face on every frame
  → author     reel-NN/build.py → index.html, sfx.json, halves.json
  → sfx        tools/sfx.py mix NN → reel-NN/assets/base.mp4
  → halves     tools/matte.py (per half-screen) + tools/halfscreen.py — baked into the plate
  → check      tools/review.py, tools/safezone.js, tools/frames.js, npx hyperframes check
  → render     npx hyperframes render — on the machine, not HeyGen
  → verify     reel-verify subagent: frames = DUR×30, no black tail, audio
  → deliver    8 Mbps Instagram copy + <100 MB Cloudinary copy
```

**Cutting rule:** under 3 minutes; cut only pauses and bad takes, per Ruta's
instructions and the transcript; never cut content.

## The run

```bash
sh tools/newreel.sh 01 raw/<file>               # scaffold reel-01 + work/r01
python tools/utt.py 01                          # whisper
python tools/takes.py 01                        # write work/r01/script.txt
python tools/cut.py 01                          # plan -> work/r01/cut.txt: read it
python tools/gapcheck.py 01                     # must be 0
python tools/cut.py 01 --render                 # -> reel-01/assets/voice.mp4
python tools/align.py work/r01/words.json work/r01/script.txt work/r01/captions.json
python tools/facemap.py 01 --flat               # -> work/r01/face_flat.json
cd reel-01 && python build.py && python ../tools/sfx.py mix 01   # prints fit: and the matte commands
cd .. && python tools/matte.py reel-01 <s> <e> <beat>            # one per half-screen, as printed
python tools/halfscreen.py 01                   # bake the half-screens into base.mp4
python tools/facemap.py 01                      # her face as rendered
python tools/review.py reel-01 && node tools/safezone.js reel-01
node tools/frames.js reel-01 --beats
cd reel-01 && npx hyperframes check && npx hyperframes render
```

## Layout

| path | what |
|---|---|
| `RULES.md` | **the editing contract** (base, no design) |
| `LOOK.md` | **the client's look** (design layer) |
| `tools/look.py` | the look in code: tokens, materials, caption CSS, measured numbers |
| `tools/kit.py` | composition kit: captions (phrase / type / word), blackout, invert, scrim, matte, emoji, motion helpers `on` `off` `type_on` `count_up` `slide_in` `fade_in`. Imports the look from `look.py` |
| `tools/utt.py` | silences + per-utterance whisper |
| `tools/takes.py` | bad-take candidates, to write `script.txt` |
| `tools/cut.py` | raw take → plate: pauses, bad takes, framing, closeups; probes the raw size |
| `tools/gapcheck.py` | removed stretches that still hold her voice |
| `tools/align.py` | transcript spelling onto ASR timing |
| `tools/facemap.py` | her face on every frame (OpenCV YuNet): box, eyes, mouth, chin, top of hair |
| `tools/matte.py`, `tools/halfscreen.py` | half-screen cut-outs, baked into the plate in ffmpeg |
| `tools/safezone.js` | readable text outside the IG safe area, anything on her head, any graphic on a subtitle |
| `tools/frames.js` | stills over the real plate, one per beat, contact sheets |
| `tools/review.py` | timeline: holds, flashes, gaps, drift |
| `tools/refstudy.py` | study material for a reference reel |
| `tools/sfx.py`, `tools/sfxkit.py`, `assets/sfx/` | sound effects: kit, cues, mix |
| `tools/shots.py`, `pullouts.py`, `cutcam.py`, `patchcaps.py`, `squircle.py`, `asr.py`, `cloudqa.py`, `hfrender.py`, `hfup.py` | Ruta's tools, as is (HeyGen ones kept for when she asks) |
| `tools/newreel.sh` | scaffolds `reel-NN/` from `reel-00/` |
| `reel-00/` | the empty reel: `build.py` with all the mechanics (FIX_AT, merges, under-chin, half-screens, fit check) |
| `.claude/skills/reel/`, `.claude/agents/reel-verify.md` | `/reel` and the verification subagent |

## Machine notes

- whisper `medium`, ffmpeg, OpenCV, Node (for `npx hyperframes`).
- `./hf` is Ruta's laptop wrapper for npx (fix its PATH line elsewhere).
- Video and audio are gitignored; the sfx kit is kept in git on purpose.
