# Reel 41 — «Незапланований рілс» (test pass)

Test run, 2026-10-13: a 7.4 s raw take (`20260929_141244.mp4`, 4K HEVC), cut by
`tools/cut.py` to a 6.4 s plate (192 frames, 2 clips, in → base, no closeups).
Built and rendered entirely in the cloud container (local hyperframes render, 49 s).
`build.py` is the source of truth.

## The chain

The one object is **the post that goes to Instagram**: a chat-bot wired to it,
the slot it leaves, the reel that takes the slot.

| time | where | beat |
|---|---|---|
| 0.4–2.3 | NEAR | the chat-bot tile (dots typing) and Instagram land, a cable draws between them and a packet runs; «перестав працювати» — the core dies, the halves fall apart, the bot greys, ✕, haptic |
| 2.3–4.1 | OVER | iris out of the dead bot: burgundy ground, a content-plan sheet (two weeks from Mon 28 Sep), planned reels in their days, today (Tue 29) empty and ringed; «незапланований» a reel card drops in tilted and too big for the cell, lands on «рілс» |
| 4.1–6.4 | NEAR | iris closes onto the card; it comes up above her head, Instagram cables into it on «вважаю», a packet on «ідеальний», the tick on «варіант» |

No written script exists (she says it is unplanned on camera), so captions are her
spoken words: «ріос» → «рілс», «чотвод на Саграмі» → «чат-бот на Інстаграмі»
(REVIEW from align: she may say «в Інстаграмі»). Align merged «що це ідеальний»
into one slot; split back on whisper's own word times. Nothing on screen says her
words, so no blackout spans. 12 sound cues in `sfx.json`, **not mixed** on this
pass — the sfx kit is not in the repo, so `base.mp4` is the plain voice plate;
`python ../tools/sfx.py mix 41` on her machine adds them.

Cloud notes: whisper ran as faster-whisper `medium` (int8, CPU); its audio decoder
breaks on this PyAV, so the wav is fed as a numpy array.
