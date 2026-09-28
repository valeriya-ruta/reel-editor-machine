# Build brief — week 40 reels (read fully before touching anything)

You are building one of Ruta's reels end to end, in a fresh context, for the
orchestrating session. **You never message Ruta.** You report back to the
orchestrator in ≤ 20 lines when done (format at the bottom).

Repo: `C:/Users/Ruta/Desktop/reels-2026-09`. Use `./hf` (or `../hf` from a reel
dir) for every HyperFrames command — plain npx is broken on this machine.

## 1. Read, in this order

1. `STYLE.md` — all of it, but **§0 (refined glass, locked 2026-09-28) wins over
   anything older.** Also §2b captions (blackout / invert), §2c takeovers, §4,
   §4a (her review rules), §5a traps.
2. `.claude/skills/reel/SKILL.md` — the run.
3. `tools/kit.py` — the document, the video plate, captions, `k.matte()`.
4. `tools/glass.py` — the look: materials CSS + `helpers(tl)` motion. Build every
   beat from it.
5. `style-test/build.py` — **the approved worked example** of the look (she
   said *"fucking amazing. delicious. just YES"*). It is a still-photo build
   without the kit; lift its choreography and CSS patterns, not its document.
6. `reel-11/build.py` — how a real reel is structured on the kit: video plate,
   NO_PAINT, beats, mattes, captions, blackout.
7. `reel-NN/PLAN.md` — your beat plan, and `work/W40.md` for the week.

## 2. What is already done for you

- `reel-NN/assets/base.mp4` — her plate, 1080×1920 @30. `DUR` for the build is
  in `work/w40-queue.log` (the `DUR = …` line for your reel — use it exactly).
- `work/rNN/words.json` (whisper, word timings), `work/rNN/captions.json`
  (script spelling bound to her timing), `work/rNN/align-report.txt` (settle
  any REVIEW lines — her wording wins when she improvised, script spelling wins
  when whisper misheard).
- `work/rNN/shots/sheet.jpg` + `shots.json` (her cuts), pull-out spans from
  `tools/pullouts.py` in the same folder / the log.
- Fonts (ProductSans Regular/Medium/Bold/Black) and `grain.png` in
  `reel-NN/assets/`. Monochrome marks: `assets/icons/*.svg` via `Glass(marks)`.

## 3. The rules she enforces (from her own reviews — non-negotiable)

- **A graphic lands ON its word** and clears before the next phrase starts.
  She counts seconds: 0.6 s late reads to her as "3 seconds late".
- **Never outstay a sentence** — and never flash for one second either. More,
  shorter events on the actual phrases.
- **Every object nameable.** If a viewer would ask "what is that", it's not done.
  When an icon is weak, **write the word**.
- **Don't paint over her jokes.** Her short inserts (closeups, pull-outs,
  0.6–1.5 s shots) are comedy → NO_PAINT: captions only. Delete beats that fall
  inside rather than nudging them.
- **Captions drop only on redundancy**: `blackout=` only where a graphic's own
  text says the word she is saying at that moment. Light takeover → `invert=`.
  The burgundy takeover keeps white captions on the plaque.
- **Graphics off her face**: small things above her head (clear band ~y 60–560,
  check her real framing on the sheet) or low over her chest; big things go
  **behind her** via `tools/matte.py` + `k.matte()` (~1.75 s/frame CPU, per
  beat only), or own the whole frame as a takeover.
- **Plan as a chain** (§0.4): objects turn into the next object; use near /
  behind / over across the reel. Iris into and out of takeovers.
- **No invented stats presented as hers** (views, followers, money): use her real numbers or none — shape-only charts are fine.
- Tasks are checks and lines. Emoji only as Apple PNGs via `Kit.emoji()` —
  avoid them rather than ship a glyph.
- Behind her with a soft room on *moving* footage: blurring the plate smears her
  silhouette into a halo. Either build the soft room per beat in ffmpeg as
  blur(plate×(1−α)) / blur(1−α) using the matte's alpha, or put the burgundy
  ground behind her matte instead. Check the edge on a snapshot either way.

## 4. Machine discipline

- A background queue (`work/w40-queue.sh`) may still be transcribing other
  reels. `tail -2 work/w40-queue.log`: while it shows `=== asr`, `hf check` /
  `snapshot` can fail with *Navigation timeout* — that is not your bug; wait
  and retry. Never start another whisper yourself.
- One heavy job at a time: mattes, snapshots and checks sequentially.
- Probe numbers before eyeballing frames; `Edit` build.py, don't re-`Write` it.

## 5. Validate — this is the double check she asked for

1. `../hf check` → 0 errors.
2. `python tools/review.py reel-NN` → fix every finding (cold opens, holds,
   overlaps, beats on NO_PAINT).
3. Snapshot every beat's proof pose + first and last frame, read the contact
   sheet against section 3 above, fix, re-snapshot.
4. Render in the cloud **on the API wallet** (already configured):
   `cd reel-NN && ../hf cloud render --aspect-ratio 9:16 --quality high -o renders/REEL-NN.mp4`
5. Verify the file: 1080×1920, 30 fps, frame count == ceil(DUR×30), audio
   present, no black tail. Spot-check one extracted frame per beat.
6. Copy to `C:/Users/Ruta/Desktop/REEL-NN.mp4`.
7. Commit `reel-NN/` (build.py, index.html, PLAN.md, project json) and
   `work/rNN/*.json|*.txt`. Do not push. Media is gitignored.

## 6. Report back (≤ 20 lines)

- Desktop path, DUR, render id/cost if shown.
- Beat list: `mm:ss  placement  what`.
- Blackout and NO_PAINT spans.
- Where she departed from the script (her wording used in captions).
- Anything you were unsure about or could not do.

## 7. Parallel builds

Another reel may be building at the same time. Wrap every heavy command
(matte.py, snapshot, check, ffmpeg passes, review.py) in `sh work/heavy.sh …`
from the repo root, e.g. `sh work/heavy.sh sh -c "cd reel-NN && ../hf check"`.
If a check/snapshot still fails with *Navigation timeout*, it is contention:
retry once the lock is free. Commit only your own reel's paths (`git add reel-NN work/rNN`) — never `git add -A`.
