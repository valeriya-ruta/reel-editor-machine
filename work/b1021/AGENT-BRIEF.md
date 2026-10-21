# Brief — author one reel of the 2026-10-21 batch (reels 42–52)

You are building ONE of Ruta's Instagram reels in her **new look** (Google style
+ Excalidraw sketches), inside `/home/user/reel-editor-machine`, a Linux cloud
container. You report back to the orchestrating session only — **never message
Ruta, never ask her anything**. Truly blocked → say so in your report and stop.

## What is already done for you

- `reel-NN/assets/voice.mp4` — her cut plate, 1080×1920 @30, her voice. The
  fumbles are already cut out and double-checked (`work/rNN/joincheck.txt`).
  If it is not there yet, a queue is still rendering it: wait with
  `until [ -f reel-NN/assets/voice.mp4 ]; do sleep 15; done` (background).
  Then `cp reel-NN/assets/voice.mp4 reel-NN/assets/base.mp4` (the sound mix
  replaces base.mp4 later; same frames).
- `work/rNN/cut.json` (`duration`, `clips`, `no_paint` — empty this batch),
  `work/rNN/words.json` (her words on the plate timeline), `work/rNN/script.txt`
  (her script from the RUTA app — the spelling source; she improvised a lot this
  time), `work/rNN/cut-fix.json` (why each cut was made).
- `reel-NN/` is scaffolded: Google Sans, Pangolin, rough.js, project files.
- `DUR` = (plate frames − 0.5) / 30, floored to 3 decimals. Frames:
  `ffprobe -v error -count_packets -select_streams v -show_entries stream=nb_read_packets -of csv=p=0 reel-NN/assets/voice.mp4`

## Read first, in this order

1. `STYLE.md` **§00** (her spec, 2026-10-21 — it wins over everything below it),
   then §4 and §4a (her review rules, still in force).
2. `tools/gstyle.py` — the kit: layers, captions, motion helpers, sketches.
3. **`reel-41/build.py`** — the worked example of this look. Copy its skeleton
   (FIX dict, `load_caps`, `Words`, the B/P/F/C/J lists, `HALF` + matte loop,
   `PLACE`, `BLACKOUT`, `g.sfx`, `main()`); write your own beats.

## The run

1. Captions: `python3 tools/align.py work/rNN/words.json work/rNN/script.txt work/rNN/captions.json > work/rNN/align.txt`.
   Read align.txt. Whisper mangles names and her fast speech; build a `FIX`
   dict (whisper's token → what she said, keyed by text or `(text, round(s,1))`,
   `None` drops a token) exactly like reel-41. When you can't tell what she
   said, re-hear it on the plate with a solo faster-whisper pass (see how the
   orchestrator did it: slice 16 kHz audio, `WhisperModel("medium", cpu, int8,
   cpu_threads=2)`, optionally `initial_prompt=` the script line) — wrap it in
   `sh work/b1021/heavy.sh`. Captions show **what she said**, spelled right.
   Print the fixed word list with times once (`'%s/%.1f'`) and anchor every
   beat to real word times with `S("word", t)` / `E(...)`.
2. Write `reel-NN/PLAN.md` (the chain in a few lines + a beat table:
   time · layer · what) and `reel-NN/build.py`; `python3 build.py`.
3. Mattes: `sh work/b1021/heavy.sh sh work/b1021/mattes.sh NN` (cuts every
   `g.matte()` the built index.html asks for; ~1 s/frame — budget below).
4. Snapshots: `sh work/b1021/heavy.sh npx --yes hyperframes@0.8.33 snapshot reel-NN --at t1,t2,... --no-end -o /tmp/claude-0/-home-user-reel-editor-machine/cd246088-a040-50f5-93d6-6b9a5955beda/scratchpad/snapNN --timeout 20000`
   — one proof pose per beat. Tile them into one or two contact sheets with
   ffmpeg (`xstack`, ~300×533 per frame) and read the sheet, not 15 PNGs.
   Fix what is wrong, re-snapshot only the times you changed.
5. `sh work/b1021/heavy.sh npx --yes hyperframes@0.8.33 check reel-NN` → 0 errors.
6. **Do not render, do not commit, do not push.** The orchestrator does that.

## The look, in practice (measured on her plates this batch)

- Her head top ≈ y 710–735, chin ≈ y 1065–1100, face centred x ≈ 520.
  Check one frame of your plate (`ffmpeg -ss T -i voice.mp4 -frames:v 1`) before
  trusting these.
- **Above me** (most beats): cards / chips / pills in the band **y 290–680**,
  x 90–990, centred and wide. Over her chest only if it truly won't fit above.
- **Captions**: automatic phrase chunks with a key-word pill (`g.chunks`).
  Default bottom y 1520. During a half screen, `PLACE` puts them on the panel
  (bottom **980** — her hair rises to ≈ y 1035 when pushed down, and the spec wants ≥ 40 px of air) — reel-41's loop does it for every `HALF` span.
- **Half screen** (`HALF.append((t0, t1))` + sketches in `#skP`): the explanation
  layer. Sketch zone on the panel: **y 290–820**. **At most two per reel, each
  ≤ 12 s** — every half-screen second costs a matte (~1 s/frame CPU).
- **Behind me** (`B` + `g.matte`): big words, Google Sans 700, 240 px, top ≥ 290,
  two lines max at line-height 0.9, first line top ≈ 320 so her hair just overlaps the lower line (≤ 25 % covered — and visibly > 0, or it doesn't read as behind).
  **At most one per reel, ≤ 4 s.**
- **Full screen** (`full(t0, t1)` + `#cover` content): only for a big
  explanation / section moment. **Never the CTA.** Zero or one per reel.
- **CTA**: always above me, with her visible — chips / a red pill
  («Став + в коментарях», or whatever her CTA says) + a red pointer doodle.
- **Sketches** only for explanations and pointers (boxes, arrows, circles,
  underlines, a calendar, a cloud…). Draw the arrow ~0.5 s before its word so
  the box lands ON the word. Labels Pangolin 40–56 px, written out — every
  object nameable.
- **No** stars / starbursts / cookies / flowers / morphing shapes. White and dark
  red only. Brand marks: `mark("notion", 30)` from `assets/icons/` (monochrome,
  red); no icon → a wordmark.
- Her rules (STYLE §4a): every graphic lands ON its word and clears before the
  next phrase; never outstays its sentence, never flashes for under ~1 s; no
  invented numbers presented as hers (only numbers she says); captions drop
  (`BLACKOUT`) only where a graphic's own text says the word she is saying.
- A visual event every 3–5 s; plan the reel as a **chain** — the next beat
  grows out of the last where it can. Don't repeat reel-41's spine; pick the
  one object that is *this* script's idea.
- Sound: call `g.sfx(name, t)` — `pop` (a card/chip lands), `click-soft`
  (a word/tick), `whoosh-short` (panel / cover / big move), `kaching` (money
  words only), `notification`, `typing`. ≤ ~0.5 cues/s.

## Report back (≤ 15 lines)

DUR · beat list (`mm:ss layer what`) · BLACKOUT spans · caption words you
fixed and any you were unsure of · matte seconds used · anything you could
not do.
