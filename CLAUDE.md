# reel-editor-machine — read this first

**Ruta hands over a reel (a file, a Drive link/folder, a reel number, "edit
this") → run the `/reel` skill. Don't ask about the style: it is fixed.**

## The look is locked (her call, 2026-11-23)

There is exactly one look for Ruta's reels: **`RUTA/STYLE.md` §00, including
"Her review of reel 61"**. Build it with `RUTA/tools/gstyle.py`; copy the
skeleton of **`RUTA/reel-61/build.py`** (the approved example); follow
**`RUTA/BUILD-BRIEF.md`** step by step (a builder subagent gets that file plus
its reel number).

In one breath: natural editing — a graphic only where it carries information;
big white words behind her head (her cut-out over them, the hook word = the
cover frame); real UI as a full-screen platform-ad sequence (3D tilt, smooth
zooms, UI rebuilt in HTML); Excalidraw only for half-screen schemes; white +
`#7A1424`, Google Sans, a little glass; lists as a card `shuffle`; graphics never
crowd her head; the CTA pill in the subtitle band; captions word by word, Product
Sans Black.

Never: any look in `RUTA/archive/`, Google's four colours, red handwriting over
her footage, decorative arrows, a chip for every phrase, tiny screenshots.

## Fixed rules

- `main` is the only source of truth. If you are on another branch and
  `RUTA/STYLE.md` has no "THE LOOK IS LOCKED" banner, you are on a stale branch:
  stop and switch to `main`.
- Her footage, scripts and status live in the **RUTA app** (MCP `RUTA`): match
  each take to its script there, set the reel's status to `edit` when you
  start, `ready` when it's scheduled.
- **The ТЕСТ CTA** («якщо ти не впевнена… пиши ТЕСТ… я змонтую твоє відео») is
  always cut out of the reel, even if the ending turns abrupt.
- **No HeyGen** — not for renders, not for hosting. Render locally; every heavy
  step (cut, sound mix, cut-out, render) through `RUTA/work/b1021/heavy.sh`.
- Verify before showing her: zero decode errors in plate and render, frame
  count exact, picture/sound in sync (`BUILD-BRIEF.md` step 10).
- Posting: her Cloudinary for the public link → Buffer (Instagram reel shared to
  feed + TikTok) at her Kyiv-evening slots, keeping the RUTA calendar in step
  (`RUTA/work/b1120/POSTING.md` has the slots and the routine).
- **Buffer overflow → Content Vault** (her rule, 2026-11-24). Buffer's free plan holds
  only 10 scheduled posts per channel. Reels that don't fit go into her Notion
  **Content Vault** (data source `collection://42291df4-181d-81fb-84d1-000b3ea99b8a`):
  name, video link, caption, planned date + IG/TikTok times, RUTA id, Status
  "Waiting for Buffer". Then set ONE scheduled task for the day enough slots have
  freed (2 reels a day → ~5 days frees 10), not a nightly check. That run schedules
  the leftovers in Buffer, flips their vault rows to "Scheduled" with the Buffer ids,
  re-dates anything whose day has passed (vault + RUTA), and if some still don't fit,
  sets the next one-shot check the same way. Only the leftovers go in the vault.
- Nika's reels (`Nika/`) are a different person and contract — `Nika/README.md`.
