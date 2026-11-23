# BUILD-BRIEF — build one of her reels (the standing brief, locked 2026-11-23)

You build one of Ruta's Instagram reels end to end in this Linux cloud
container (`/home/user/reel-editor-machine`, her pipeline lives in `RUTA/` —
every path below is relative to `RUTA/`). You report to the orchestrating
session only, in ≤ 15 lines. **Never message Ruta, never ask her anything.**
Truly blocked → say so in the report and stop.

## Read first, in this order

1. `STYLE.md` **§00** — her spec — and in it **"Her review of reel 61
   (2026-11-23)"**: it wins over everything else. Then §4 / §4a (her timing
   rules).
2. `work/b1021/AGENT-BRIEF.md` — the 2026-10-21 batch's brief for this kit. Its
   "Her review of reel 41" and "The look, in practice" still hold, EXCEPT where
   the reel-61 review overrides them (fewer graphics, no handwriting over her
   footage, no decorative arrows, no glass around shuffle chips).
3. `tools/gstyle.py` — the kit (layers, captions, `half`, `full`, `shuffle`,
   sketches).
4. **`reel-61/build.py` — the approved worked example of THIS batch.** Her
   verdict: "everything else is amazing". Copy its skeleton and its idioms:
   behind-me words with a matte, a glass DM card, the full-screen
   platform-ad sequence (`#stage` / `#win` 3D camera, a UI rebuilt 1:1 in
   HTML), the half-screen Excalidraw scheme, the `shuffle` CTA chips, the CTA
   pill in the subtitle band.

## Memes: comic relief (her rules, 2026-11-23: every reel gets them)

63 reaction memes live in `assets/memes/`; **`assets/memes/MEMES.md` is the index**
(caption, feeling, when to use) and holds the rules. Read it in full, then for THIS
reel pick **1-3 moments** (cap 3 images) where a meme *is* the feeling of what she just said
(a missed deadline, a wrong-button panic, a "client asks for more"). Not a quota, but
don't ship a reel with none unless truly nothing fits.

- `g.cta_start = <the CTA line's first word time>` right after `g = G(...)`; then
  `g.meme(F, J, "42", t, dur=1.2)` per meme (`slot="l"` + `slot="r"` at the same `t` for a pair).
  The kit refuses a 4th image, one touching the CTA, or an unplanned overlap, and
  copies the files into `reel-NN/assets/memes/`.
- Place it just after the word/phrase it reacts to (`E(word) + 0.1`), never mid-line.
- Slapped straight on, no frame or card, in her zones: slot `top` (above her head), `r` (right of
  her head), `l` (low left). A pair only with a long clear stretch around it. Memes sit under captions and over her footage;
  keep them off beats that already have a behind-me word, card, half or full screen.
- First 3 s allowed if it fits; profanity allowed; English reel -> caption-free memes only.
- Write the picks into `PLAN.md` (meme NN, time, the line it reacts to, why).

## What she wants (her words, 2026-11-23)

- *"a more natural editing style, where I only show things that are really
  necessary, but we are not animating every single word for the sake of
  animations"*. Roughly one meaningful moment per sentence group.
- *"there are other ways to do a scene change every 2–3 seconds, which also
  includes full screen animations"* — her own cuts/punch-ins, a behind-me word,
  a full screen, a camera move inside a full screen.
- **Behind-me big text in every reel**: 1–2 words, white, Google Sans 700,
  200–250 px, her hair overlapping the lower edge a little (needs a matte).
  Pick the **hook word that makes a good cover frame** (her note: «AI-агент»
  beats «страх» — what attracts people, ifykyk).
- **Real UI → full-screen platform-ad sequence** (3D tilt, smooth zoom into the
  part she names, a control changes state on its word, zoom out). Build the UI
  as clean HTML. If you have her real screenshot (`app-screenshots/`), rebuild
  it 1:1 from it; otherwise a clean, plausible Material/product UI with only the
  labels she says — never fake numbers or fake proof (stats, DMs, reviews).
- **Excalidraw only for real schemes / highlights** (a half-screen diagram).
  No red handwriting with a white halo over her footage, no doodles, no
  decorative arrows (the CTA arrow "is shit").
- **Modern Google look, slight glass occasionally** (`.glass` for a DM card).
- **Lists → `shuffle`** (one slot, cards rise in and leave upward), plain white
  cards, no glass around them.
- **Give her head room**: above-me elements in y 300–560, never touching her
  hair/forehead (her head top ≈ y 640–700 on wide shots, higher on punch-ins —
  check frames of YOUR plate). CTA pill may sit in the subtitle band
  (top ≈ 1404) once `BLACKOUT` from its word frees it.
- **ТЕСТ CTA («якщо ти не впевнена… пиши ТЕСТ… я змонтую твоє відео») is cut out entirely**, even if the ending turns abrupt — a `drop` to the end in `work/rNN/cut-fix.json`.

## Environment (set up — don't reinstall)

```bash
cd /home/user/reel-editor-machine/RUTA
export CUT_SCRATCH=$PWD/work/scratch REELS_SCRATCH=$PWD/work/scratch MATTE_REMBG=1
HF=/tmp/claude-0/-home-user-reel-editor-machine/1ca4d4dc-1e63-5529-89a7-5a7617ac9a0f/scratchpad/hf/node_modules/.bin/hyperframes
H="sh work/b1021/heavy.sh"     # EVERY heavy step goes through it (one at a time across all builders)
```
Never `npx hyperframes` / `./hf` (broken here). Use `$HF`. Never HeyGen.

## The run

1. `work/rNN/` has `script.txt`, `RUTA_ID.txt`, `utt.jsonl`, `cut-fix.json`
   (maybe), `old-sketch-build.py` (an earlier build in a rejected look — use it
   ONLY for its caption fixes and beat timing ideas, not its visuals).
2. **Cut** (always re-run — the cutter changed): `$H python3 tools/cut.py NN --render`
   → `reel-NN/assets/voice.mp4`, `work/rNN/cut.json`, `cut.txt`, `words.json`.
   Read `cut.txt`; if a real line was dropped, add `keep` to `cut-fix.json`, rerun.
   `DUR = (frames − 0.5)/30` floored to 3 decimals (`ffprobe -count_packets`).
3. `sh work/b1021/scaffold.sh NN` (if `reel-NN/assets/fonts/Pangolin.ttf` is
   missing).
4. **Captions**: `python3 tools/align.py work/rNN/words.json work/rNN/script.txt work/rNN/captions.json > work/rNN/align.txt`,
   then a `FIX` dict like reel-61's (whisper's token → what she said; `None`
   drops). Captions show what she SAID, spelled right; print them once and read.
5. Write `reel-NN/PLAN.md` (chain + beat table) and `reel-NN/build.py`.
   `python3 build.py`. Preview: `node tools/shoot.js reel-NN/index.html /tmp/rNN t1 t2 …`
   + `python3 tools/sheet.py /tmp/rNN t1 t2 …` → read the one sheet (mattes
   aren't seeked in previews — a ghost double of her there is normal).
6. **Sound mix**: `$H python3 tools/sfx.py mix NN`, then verify
   `ffmpeg -v error -i reel-NN/assets/base.mp4 -f null - 2>&1 | wc -l` is **0**.
   (Two overlapping mixes corrupted reel 61's plate on 2026-11-23 — the render
   froze and drifted out of sync. Never run a mix outside `$H`.)
7. **Mattes**: `$H sh work/b1021/mattes.sh NN` (~1 s/frame; behind words ≤ 4 s
   each, half screens ≤ 12 s each, at most two of each).
8. `cd reel-NN && $HF check` → 0 errors (contrast warnings on rebuilt UI
   hint text are OK).
9. **Render, locally** (over ~70 s, or when it refuses for disk: prefix `HF_DE_PARALLEL_STREAM=true` — streaming encode): `rm -rf reel-NN/renders/work-*; $H $HF render reel-NN -o reel-NN/renders/REEL-NN.mp4 --workers 3 --low-memory-mode --quiet`
   (run from `RUTA/`; if the CLI wants the dir differently, `cd reel-NN` first).
10. **Verify** (all must hold, or fix and re-render):
    - frames == plate frames; `ffmpeg -v error -i REEL-NN.mp4 -f null -` prints nothing
    - sync: at 3 times with no graphic up, PSNR of a 500×400 face crop of the
      render vs `assets/base.mp4` is highest at the same time vs ±0.4 s
      (see `work/scratch/r61c.sh` for the commands)
    - one contact sheet of 6–8 frames from the RENDER, read once (include a frame with a meme up: it
      must not cover the captions, and the image must not be cut off)
    - `ls reel-NN/assets/memes` has ≤ 3 files and none is after the CTA's first word
11. **Don't commit, push, or touch the RUTA app.** The orchestrator does.

## Report (≤ 15 lines)

```
REEL-NN «title»  DUR s  frames n/n  decode 0  sync ok  check: passed
cut: raw s -> s; anything she said that was dropped / kept on purpose
behind-me word(s): …   full screens: …   half screens: …   memes: NN@t, …
captions fixed: n (unsure: …)
her side: lines she improvised that change meaning; example UI text you invented
```

## After the render (the orchestrator, or you when running alone)

- Gallery copy at 1080p CRF 27 (≤ 15 MB) for the review artifact.
- Post: upload `REEL-NN.mp4` to her Cloudinary (MCP `sign-upload`, folder
  `reels/`), schedule with Buffer (IG reel shared to feed + TikTok) at the slots
  in `work/b1120/POSTING.md`, caption = RUTA `write_caption` first line + the
  reel's own CTA. RUTA status → `ready`; after it goes out, `mark_posted`.
