# <CLIENT>'s reel editor

Read `README.md` (the run), `RULES.md` (the base contract: editing, safe zones,
review rules) and `LOOK.md` (her look) before anything. `/reel` builds one
reel end to end.

- Cutting: under 3 minutes; only pauses and bad takes, per Ruta's
  instructions and the transcript; never cut content. No length targets.
- Transcription: local whisper (`tools/utt.py`, word timestamps), OpenRouter
  whisper as the fallback. Never ElevenLabs. If another skill (e.g. video-use)
  says otherwise, this folder's pipeline wins.
- Captions are what she said, verbatim (her surzhyk kept).
- **Don't ask Ruta anything mid-run** (her rule). The folder is the brief:
  decide every cut, take and beat from RULES.md, LOOK.md, the transcript and
  the refs, write each call into `reel-NN/PLAN.md`, and come back once with
  the finished reel and the list of calls you made.
- Never invent a rule, a target or an asset. Everything shown is real (her
  photos, her screenshots); with no real asset for a beat, use type instead.
- `RULES.md` and every file in `tools/` except `look.py` are the shared base:
  don't change them for one client.
