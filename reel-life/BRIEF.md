---
workflow: general-video
flow: autonomous
resolution: portrait
duration: 55
fps: 30
---

# «Проєкт твого життя» — reel

Recreation of the typographic system in
`Examples/AQNt6yKMaoXZBgEmbC7I_…mp4` (49.7s Ukrainian kinetic-typography reel),
applied to Ruta's own footage, script and voiceover.

## Source of truth

| Thing | Where |
|---|---|
| Voiceover | `work/ref/VO.wav` — hook from «1 фраза», body from «Всі інші», joined at the gap after «проєкту?», loudnorm -14 LUFS, 54.98s |
| Word timings | `work/ref/VO-words.json` — whisper `medium`, 148 words |
| Spelling | the script she pasted, never ASR (see Divergences) |
| Footage | 26 clips, normalised to `assets/clips/c01…c26.mp4` (1080×1920, 30fps) |
| Type | Inter variable, `assets/fonts/Inter.ttf` — Black for heroes, per her call |

## Divergences: delivered audio vs written script

She improvised in three places. **The delivered audio wins** — on-screen text follows
what she actually said, spelled correctly.

| Written | Delivered |
|---|---|
| «Що рішення почнуть даватися спокійно, бо ти знатимеш, з чого їх приймати.» | «Що цілі почнуть досягатися, бо ти нарешті поставиш їх і себе в пріоритет.» |
| «…не пообіцяти собі, а **довести**?» | «…не пообіцяти собі, а **зробити**?» |
| «Третій потік. Анкета запису в шапці.» | «Третя група вже у вересні. Заповни анкету перед записом в шапці профілю.» |

## The system being recreated

Five layers, lifted from the reference:

1. **Base** — full-bleed footage, hard cuts, ~0.9s average shot.
2. **Hero** — one loud word, UPPERCASE, Inter Black, white. Lands on its spoken word.
3. **Parenthetical** — lowercase in round brackets, light weight, overlapping under the hero.
4. **Spine** — a word rotated 90° on the frame edge that *survives several cuts*.
5. **Caption** — small sentence-case line, bottom third.

**Motion law, measured off the reference at 12fps: nothing eases.** Every element
pops in hard on its word and stays until its sentence ends. No fades, no slides,
no springs. Elements accumulate over a shot, then clear together.

## Open

- 26 clips in hand; she is sourcing the rest and they slot in by swapping `assets/clips/cNN.mp4`.
