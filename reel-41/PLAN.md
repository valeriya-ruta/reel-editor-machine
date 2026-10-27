# Reel 41 — «Клод розсилає повідомлення, поки я вмиваюсь»

Built 2026-10-27 · one raw take (364 s, 4K HEVC, `20261027_233640.mp4`) cut to a
36.95 s plate (1109 frames) by `work/r41/ramp.py` · no animations, by her brief.
`build.py` is the source of truth.

## The cut (her brief, so the "never re-cut" rule yields here)

| out (s) | source (s) | what |
|---|---|---|
| 0.00–7.16 | 0.45–7.61 | intro, 1x. Her own switch to the screen (7.61) lands right on the end of «Дивіться!» |
| 7.16–17.94 | 7.61–298.77 | the screen session at 27x |
| 17.94–19.44 | 298.77–310.60 | the brake: speed falls geometrically 27x → 1x |
| 19.44–22.64 | 310.60–313.80 | real time: the inbox switches to the next profile (311.7) and its card loads (313.1) |
| 22.64–36.95 | 349.62–363.95 | outro, take 2 («Дякую дуже…»); take 1 (333.1–349.3) dropped |

The 20 s after 313.8 are a still screen and are dropped. Sound: her voice on the two
talking parts; a soft clock tick across the time-lapse, one per 6 source seconds, so
it slows with the picture and stops at real time (room tone under the hold).

## Graphics — hard on/off only

- **Footnote** on «повідомлення*» (2.97–5.17): «*персоналізовані», a small pill above
  the caption. She forgot to say the word.
- **Explainer** over the keyboard for the whole screen part (7.16–22.64), ruta-voice:
  «По суті, Клод працює через вбудований браузер і робить паузу мінімум 30 секунд між
  повідомленнями, щоб інстаграм мене не заблокував. / До кожної людини він спершу
  заходить у профіль: дивиться контент, біо, ім'я і вже тоді пише персональне
  повідомлення за моїм правилом.»
- Both on ink-burgundy glass at 0.88 alpha: worst case over a white screen, white
  13:1, the pink accent 6:1. `hyperframes check`: 7/7 text checks pass AA.
- **Blur** (her «blurred where personal» rule): the browser's address bar and
  profile header, plus one @handle and two first names in Claude's report on the
  left. The phone never moved, so the boxes are static.

Caption fixes: «моїм» (whisper: «мимо»), «розіслано» (whisper: «розіслено»).
