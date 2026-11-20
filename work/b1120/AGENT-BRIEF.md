# Brief — build ONE reel of the 2026-11-20 batch (Google × Excalidraw look)

You build one of Ruta's Instagram reels end to end in this cloud container and
report back to the orchestrating session in ≤ 15 lines. **Never message Ruta,
never ask anything.** If truly blocked, say so in the report and stop.

Repo: `/home/user/reel-editor-machine`. Your reel number is `NN` (given in your
prompt); work dir `work/rNN/`, reel dir `reel-NN/`.

## Read first (in this order, skim what you already know)

1. `STYLE.md` **§0b** (the look for this batch) and §0's rules on timing, chains,
   nameable objects; §2b captions (blackout / invert).
2. `tools/sketch.py` — the whole library is ~400 lines; read it.
3. **`reel-45/build.py`** — the worked example of this exact look, same batch.
   Copy its skeleton (FIX by position, `S()/E()`, `T{}`, `js()` with `@name`,
   `sfx()`, `beat()`, `INVERT`, `main()`), its CSS idioms (`.bub`, `.av`, `.lbl`,
   `.field`, `.row`) and its rhythm. Invent your own beats for your script.

## Environment (already set up — do not reinstall)

```bash
cd /home/user/reel-editor-machine
export CUT_SCRATCH=$PWD/work/scratch REELS_SCRATCH=$PWD/work/scratch CUT_MOTION=1
HF=/tmp/claude-0/-home-user-reel-editor-machine/1ca4d4dc-1e63-5529-89a7-5a7617ac9a0f/scratchpad/hf/node_modules/.bin/hyperframes
```

- Raw take: path in `work/rNN/SOURCE.txt`. Per-utterance ASR (faster-whisper
  medium): `work/rNN/utt.jsonl` — done. Whisper often hallucinates a leading
  «Дякуємо за підтримку!» / «Субтитрувальник…» on silence: that is not her.
- Python is `python3`. Chromium/Playwright work for previews (below).
- Do NOT use `./hf` or `npx hyperframes` (broken here); use `$HF`.

## The run

1. **Script.** Fetch it from the RUTA app: `mcp__RUTA__get_content` with the id
   in your prompt (load the tool with ToolSearch `select:mcp__RUTA__get_content`).
   Write the `script` field verbatim to `work/rNN/script.txt`, the id to
   `work/rNN/RUTA_ID.txt`. If the transcript clearly is a different script than
   your id, find the right one with `mcp__RUTA__list_content` (status film) and say
   so in the report.
2. **Cut.** `sh work/b1120/scaffold.sh NN`, then
   `python3 tools/cut.py NN --render` → `reel-NN/assets/voice.mp4`,
   `work/rNN/cut.json`, `cut.txt`, `words.json`. Read `cut.txt`: FLAG lines,
   dropped takes, the clip list. Last take of a fumble wins (that is the cutter's
   rule — trust it unless it obviously cut a real line; then add a
   `work/rNN/cut-fix.json` like other reels' and re-run).
   `DUR` = the `DUR = …` it prints. No punch-ins are planned this batch, so
   `no_paint` is empty unless the cutter made some.
3. **Captions.** `python3 tools/align.py work/rNN/words.json work/rNN/script.txt work/rNN/captions.json`.
   Then go through every "SHE IMPROVISED" / REVIEW line: whisper errors (non-words,
   mangled brands like «синпуївсь», «Клодії», «Супабейс») get the script word via
   the positional `fix()` in build.py; genuine improvisation keeps her words.
   Brand spelling: Claude → «Клод» only if the script spells it so, else as the
   script has it; SendPulse, Supabase, Vercel, Notion, Google, ChatGPT as written.
   Captions must read as clean Ukrainian — print the final caption string and
   read it before rendering.
4. **Plan** in `reel-NN/PLAN.md` (short table like `reel-40/PLAN.md`): one
   object or metaphor carried through the reel, near → OVER (board) → near …
   chain, a visual event every 3–5 s, all landing ON her words.
5. **Author** `reel-NN/build.py` (copy reel-45's skeleton; `NN`, `DUR`, title).
   `python3 build.py` → `index.html` + `sfx.json`.
   `python3 tools/sfx.py mix NN` → `reel-NN/assets/base.mp4` (re-run after cue changes).
6. **Preview** (cheap, do it): `node tools/shoot.js reel-NN/index.html /tmp/rNN t1 t2 …`
   then `python3 tools/sheet.py /tmp/rNN t1 t2 …` and Read `/tmp/rNN-sheet.jpg`
   (one contact sheet, ≤ 8 frames, one frame per beat). Fix what's wrong.
   Never return a GSAP timeline from `page.evaluate` (hangs).
7. **Check**: `cd reel-NN && $HF check` → must print `Check passed`
   (lint errors like `gsap_css_transform_conflict`: animate with `fromTo`, never
   leave a CSS transform on a tweened element).
8. **Render**: `python3 tools/hfrender.py reel-NN` (HeyGen cloud, ~1 min; the
   key is injected by the proxy — the dummy `~/.heygen/credentials` is fine).
9. **Verify**: frame count of `reel-NN/renders/REEL-NN.mp4` ==
   `round(DUR*30)`; audio stream present; sample 4–6 frames from the RENDER
   (ffmpeg -ss) into one sheet and look at it once. Then
   `ffmpeg -i REEL-NN.mp4 -vf scale=540:960 -c:v libx264 -crf 30 -c:a aac -b:a 96k REEL-NN-preview.mp4`.
10. **Don't commit or push** — the orchestrator does that.

## Her rules (from her reviews — non-negotiable)

- **A graphic lands ON its word**, and clears before the next phrase. Never
  outstays its sentence, never flashes for under ~1 s.
- **Every object nameable.** If an icon would make a viewer ask "what is that",
  write the word (Google Sans label or handwriting). Tasks = checkboxes + lines.
- **Graphics stay off her face**: near graphics in y ≈ 60–640; her head starts
  ≈ y 690. Board content keeps its bottom ≤ y 1240 (captions at ~1470).
- **No invented numbers presented as hers.** Only numbers she says. Example
  text inside a depicted chat/UI is fine when obviously illustrative.
- No brand logos as images; brand = a Google-Sans wordmark in a pill/chip, or a
  monochrome mark from `assets/icons/*.svg` if you really need one.
- **No emoji glyphs** in HTML (render machine has the wrong emoji font).
- **Captions drop only on redundancy** (`blackout=` only where a graphic says the
  same word at the same time). Over the white board use `invert=` spans.
- Use the board (OVER) at least once, ideally twice in a long reel; near beats
  between. Chain the beats — each grows out of the last (a card shrinks into a
  sticky note, the board wipes in from it, closes onto the next object…).
- Sound: `pencil` under big draw-ons, `pop` on cards/chips, `whoosh-short` on
  board in/out, `click`/`click-soft` on UI, `kaching` only on money words,
  `ping`/`notification` on messages. ≤ ~0.5 cues/s.
- CTA at the end: show what she asks for (the word to comment, «+», DM) as UI.

## Report format (≤ 15 lines)

```
REEL-NN  <title>  DUR <s>  frames <n>/<expected>  check: passed
script: <RUTA id>  (matched / changed: why)
cut: raw <s> -> <s>; dropped takes: <n>; anything odd
captions fixed: <n> (notable: …)
beats: <one line per board/near chain, very short>
render: reel-NN/renders/REEL-NN.mp4 (+ preview)
her side: <a line she improvised that changed meaning / anything she must know, or "nothing">
```
