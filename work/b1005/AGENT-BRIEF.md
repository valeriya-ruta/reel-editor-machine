# Brief — build one reel of the 2026-10-05 batch

You are building ONE of Ruta's Instagram reels end to end, inside the repo
`C:\Users\Ruta\Desktop\reels-2026-09`. You report back to the orchestrating
session only — **never message Ruta, never ask her anything**. If something is
truly blocked, say so in your final report and stop.

## What is already done for you

- Her raw take is **already cut** by `tools/cut.py` (last take of every fumble
  wins, silences removed, a new framing on every cut, one or two closeups).
  Do NOT re-run `tools/cut.py --render` and do not edit `tools/cut.py`.
  - `reel-NN/assets/voice.mp4` — the cut plate, 1080×1920 @30, her voice only.
    It may still be rendering when you start: wait for it with
    `until [ -f reel-NN/assets/voice.mp4 ]; do sleep 10; done` (run in background).
  - `work/rNN/cut.json` — `clips`, `duration`, and `no_paint`: the closeup spans
    on the output timeline. **No graphic may be on screen inside a no_paint
    span** — captions only (STYLE.md §4a: her closeups are comedy).
  - `work/rNN/cut.txt` — human-readable cut report.
- `work/rNN/script.txt` — her script from the Ruta app (spelling source).
- `work/rNN/captions.json` + `work/rNN/align.txt` — script spelling on her real
  timing. Read align.txt: "WHISPER MISHEARD" lines are already fixed; "SHE
  IMPROVISED" lines keep what she said — but if a "said" word is obviously a
  whisper error (a non-word, a mangled brand), restore the script word through a
  `FIX` dict in build.py, exactly like `reel-21/build.py` does.
- `reel-NN/` is scaffolded (fonts, underlay, grain, hyperframes.json,
  package.json, `.hyperframesignore`).

## Read before authoring (in this order)

1. `STYLE.md` — the design contract. §0 (refined glass) is the look.
2. `tools/glass.py` and `tools/kit.py` — materials, motion helpers, captions.
3. **`reel-21/build.py`** — the worked example from this same batch: same
   structure, same helpers (`S()`, `E()`, `js()` with `@name`, `tile()`,
   `arr/bin/bout/draw2/shn`, `sfx()`, `BLACKOUT`, the typing clock), a full
   near → over → near chain. Copy its skeleton and its CSS idioms; write your own
   beats. `reel-19/build.py` and `reel-20/PLAN.md` are older good examples.

## Her rules (all from her own reviews — they outrank instinct)

- **Land every graphic ON its word**; budget arrival + move + exit inside the
  phrase; clear before the next phrase. A graphic never outstays its sentence,
  and never flashes for under ~1 s either.
- **Every object must be nameable.** If an icon is not instantly legible, use
  the word (a wordmark, a field label inside a depicted UI). Tasks are always
  checkboxes + lines.
- Monochrome marks from `assets/icons/<slug>.svg` in the tile family
  (`.clear` / `.pearl` / `.jelly`). Missing icon: fetch with
  `curl -so assets/icons/<slug>.svg https://cdn.jsdelivr.net/npm/simple-icons@13/icons/<slug>.svg`
  (e.g. `obsstudio`); no icon exists → a wordmark in the tile. **RUTA** (her
  app) is always a wordmark, caps, heaviest weight.
- **Graphics stay off her face**: near graphics live in y ≈ 80–640 (her head
  starts ≈ y 690 in these plates); if something will not fit, go below her over
  the chest rather than over the face. Never in a corner — centred, wide.
- **Use all placements**: near (shelves, tiles, notifications above her head)
  and **over** (the burgundy takeover `.tkg` + `.aurs` + `.grain`, iris in /
  iris out, a white sheet on it). Takeovers own the frame — bold, big, bleeding
  off edges, not a polite card. Behind-her (matte) is allowed for **at most one
  beat ≤ 3.5 s** per reel this batch (CPU is scarce): `tools/matte.py`, run it
  through the heavy lock.
- **Captions drop only on redundancy**: `BLACKOUT` only the spans where a
  graphic's own text says the word she is saying. Everywhere else they stay.
  A light takeover needs `invert=`.
- **No invented numbers presented as hers.** Only numbers she says. Shape-only
  charts are fine. Proof (IG stats, DMs, reviews) = her real screenshots, never
  redesigned — if you have none, don't fake one.
- Plan the reel as a **chain** — each beat grows out of the previous one
  (STYLE.md §0.4). A visual event every 3–5 s.
- Slow push on the plate 1.0 → 1.045 across the reel (as in reel-21).

## Sound design (new — her ask: *"some clicking on text, whooshing, kachinging etc? nothing too crazy, just to give some style"*)

Call `sfx(name, time, db)` in each beat, as reel-21 does. Kit in `assets/sfx/`:
`click-soft` / `click` (text, UI taps, ticks), `pop` (a tile/card lands),
`whoosh-short` (a transition, iris, big move), `kaching` (money — only on a
money word), `notification` / `ping` (a notification), `typing` (a prompt
typing), `sparkle` (rare). **≤ ~0.5 cues per second overall**, nothing on her
joke/closeup spans. `build.py` writes `sfx.json`; then
`python ../tools/sfx.py mix NN` makes `assets/base.mp4` (plate + effects) — the
composition's plate is `assets/base.mp4`. Re-run the mix whenever cues change.

## Nothing heavy on her laptop (it overheats — her words, 2026-10-05)

No `hf check`, no `hf snapshot`, no `hf render`, no `tools/matte.py` locally.
Use the cloud tools instead:
- check + snapshots: `python tools/cloudqa.py reel-NN --at t1,t2,...` (repo
  root; ~3–5 min; prints the check summary + any ✗ lines and the contact-sheet
  paths under reel-NN/study/cloud-*/). Without `--at` it only checks.
- render: `python tools/hfrender.py reel-NN` (HeyGen cloud, ~3–6 min).
- a behind-her matte: ask the orchestrator (it runs on GitHub) — or skip it.
`python build.py` and `python ../tools/sfx.py mix NN` are light; fine locally.

## The run

1. `DUR` = (plate frames − 0.5) / 30, floored to 3 decimals. Frames:
   `ffprobe -v error -count_packets -select_streams v -show_entries stream=nb_read_packets -of csv=p=0 assets/voice.mp4`
2. Write `reel-NN/build.py` (+ a short `PLAN.md`: the chain + a beat table).
3. `python build.py && python ../tools/sfx.py mix NN`
4+5. `python tools/cloudqa.py reel-NN --at <one time per beat>` → check must be
   **0 errors**; read the contact sheets; fix what is wrong (text overflow,
   overlaps, a graphic over her face, empty frames, a beat late on its word).
   Re-run with only the times you changed. Batch your times — every call is a
   cloud round-trip.
6. Render — **in the cloud only, never on her laptop** (her rule):
   `python tools/hfrender.py reel-NN` from the repo root. It uploads, submits,
   polls and downloads to `reel-NN/renders/REEL-NN.mp4`. Do not use
   `hf cloud render` (its upload and poll are broken) or `hf render`.
7. Verify: frame count of the render == round(DUR×30) (or DUR×30 rounded up by
   one); audio stream present and not silent; last frames not black.
8. Do NOT copy to the Desktop, do NOT commit, do NOT post anything. The
   orchestrator delivers.

## Final report (keep it short)

Render path + duration + frame count verdict; the chain in 3–5 lines; any
caption wording you changed; anything you could not do. No command transcripts.
