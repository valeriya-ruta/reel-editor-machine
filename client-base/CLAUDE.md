# <CLIENT>'s reel editor (on Ruta's editing base)

Read `README.md` (the run), `RULES.md` (the editing contract, same for every
client, no design in it) and `LOOK.md` (this client's look) before anything.
`/reel` builds one reel end to end.

- Cutting: under 3 minutes; only pauses and bad takes, per Ruta's
  instructions and the transcript; never cut content. No length targets.
- Pauses from the audio and the transcript, cut only where the audio agrees
  (`tools/gapcheck.py NN` = 0 before `--render`). Last take wins.
- Transcription: local whisper, OpenRouter as fallback. Never ElevenLabs.
- Captions are what she said, verbatim, in her own words.
- Readable text stays inside Instagram's safe area (x 130–950,
  y 250–1470; RULES.md §3a); `node tools/safezone.js reel-NN` before a render
  (it also checks her head and the subtitles).
- Nothing on her head, ever: every beat sits under her chin, measured per
  frame (`tools/facemap.py`, `under()` in build.py), or on a half-screen;
  never zoom in under a graphic (RULES.md §3b, §1). Never in a corner.
- Half-screen cut-outs are baked into the plate (`tools/halfscreen.py`), never
  laid over her in the browser: her face changes colour (RULES.md §1, §2c).
- Every element is a real element, never an icon standing in for one
  (RULES.md §4). Proof is her real screenshot. No invented stats.
- Render on the machine (`npx hyperframes render`), not HeyGen (Ruta, 2026-11-17).
- No music for now (Ruta, 2026-11-17). Basic sfx on the frame a graphic appears.
- Never invent a rule, a target or an asset. What RULES.md, LOOK.md, the
  transcript and the refs settle, decide (calls go in `reel-NN/PLAN.md`).
  Anything not settled, ask Ruta (Ruta, 2026-11-20).
- Design (fonts, colours, sizes, materials, motion, rhythm) lives only in
  `LOOK.md`, `tools/look.py` and `assets/fonts/`. Everything else is the base:
  don't change it per client.
