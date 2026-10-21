# Batch 2026-10-21 — 12 raw takes, reels 41–52, first in the §00 look

Raw takes from Drive «Inbox», recorded 2026-10-21 13:10–13:35 in script-list
order. Scripts from the RUTA app (status «film»). Her notes: she was tired, so
more fumbles than usual — cut them, then double-check (work/b1021/joincheck.py
re-hears every cut plate); and a lighter look → her spec, STYLE.md §00.

| reel | posts | take | RUTA title | plate |
|---|---|---|---|---|
| 41 | 19 Oct | 131056 | Не просто промти | 97.0 s |
| 42 | 19 Oct | 131316 | Що від мене треба? | 45.5 s |
| 43 | 20 Oct | 131454 | €400 чи €1300 | 62.7 s |
| 44 | 20 Oct | 131657 | Дзвінок → пропозиція | 59.6 s |
| 45 | 21 Oct | 131854 | Вчиться на статистиці | 33.9 s |
| 46 | 21 Oct | 132020 | Два акаунти, одна система | 66.1 s |
| 47 | 23 Oct | 132653 | Навіщо Notion | 87.5 s |
| 48 | 23 Oct | 132857 | Уроки і YouTube | 81.5 s |
| 49 | 24 Oct | 133238 | Все з телефону | 27.0 s |
| 50 | 24 Oct | 133100 | Поки я сплю | 38.0 s |
| 51 | 25 Oct | 133317 | Твій стиль з першого дня | 70.5 s |
| 52 | — | 133511 | Якщо в тебе фомо на… | 54.5 s |

## Her calls

- **Render**: HeyGen (API wallet, via the environment's network secret) for
  41–46, the ones posting first; 47–52 render locally in the cloud container.
- **Sound effects stay.** The kit lives in her laptop's `assets/sfx`
  (gitignored) — needed before the final renders.
- **Reel 51**: keep 10 s of the pause after «…змонтував штучний інтелект»,
  then cut to the next text. She adds the two reels herself — the pause stays
  empty (her plate only, no graphics, no captions).
- **Sound**: the stand-in kit from tools/sfxsynth.py — "they're fine".
- **No covers** — Instagram previews are not generated.
- Deliver here in the chat (SendUserFile), not her Desktop. **From 43 on: hold
  them** — when all 12 are back, one review page (artifact) with every reel
  and a download button; she comments in one batch.
- **Drive, from now on**: every finished reel is saved to her Drive, so she can
  revisit / repost from the phone. tools/driveup.py uploads any size through
  her own Apps Script (tools/drive-hook.gs, a web app; its URL in the env var
  REELS_DRIVE_HOOK — she's adding it). Files land in «Reels» in her My Drive.

## Reel 53 — the unplanned take

| reel | posts | take | what | plate |
|---|---|---|---|---|
| 53 | — | 144227 (14:45) | «Це не запланований рілс» — her process on camera: gallery → Drive → link → Claude → 2–3 h → Edits | 75.2 s |

**Skipped completely** (her call, 2026-10-21: she edited it herself). Its
cut plan and plate were made, then removed from the repo.

## Her review of reel 41 (2026-10-21)

Captions back to the old rail; calmer sketches (roughness 1); behind-me words
white; over the footage, sketches are white stickers / dark ink with a white
halo (white lines failed AA on her light room); a full screen never opens onto
empty white; longer arrows, no arrowhead on a loop. All in tools/gstyle.py.

## Status (2026-10-21, afternoon)

All 12 rendered and verified (frame count = plate, audio, no black tail):
41–46 on HeyGen, 47–52 here with `render --workers 1` (streams frames into
the encoder, so the ~8 MB/frame disk check never trips). Review page with
720p copies and a download button per reel:
https://claude.ai/artifact/Hpozkm3M6n9BrTomm8hABe — she comments in one batch.
Full-quality files: reel-NN/renders/REEL-NN.mp4 (gitignored).

## Posting (2026-10-21 evening, her calls)

Full-quality files in her Drive folder (link-shared), posted through Buffer:
- She posted **50 and 52 on Instagram** herself (from the 720p previews).
- **TikTok now**: 50, 52.
- **Queued, 2 a day**, Instagram on its queue slots, TikTok at fixed times on
  its slots (its next slot was tonight, too close to 50/52):

| reel | Instagram | TikTok |
|---|---|---|
| 41 | Thu 22 · 08:19 | Thu 22 · 21:37 |
| 42 | Thu 22 · 10:21 | Thu 22 · 22:22 |
| 43 | Fri 23 · 07:21 | Fri 23 · 20:18 |
| 44 | Fri 23 · 08:05 | Fri 23 · 22:47 |
| 45 | Sat 24 · 06:12 | Sat 24 · 08:25 |
| 46 | Sat 24 · 22:01 | Sat 24 · 18:56 |
| 47 | Sun 25 · 19:31 | Sun 25 · 09:29 |
| 48 | Sun 25 · 22:50 | Sun 25 · 10:14 |
| 49 | Mon 26 · 18:59 | Mon 26 · 08:01 |

- **51 skipped**: it waits for her version with the two comparison reels.
- Captions in her voice; the reel's own CTA on both; last line TikTok =
  «Підпишись…», Instagram = «Відправ <one specific woman>…» (her rule).
