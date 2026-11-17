# Reel 56 — «Презентація з Клодом за 5 хвилин»

Drive folder «Presentation with Claude» (`18Lffz8he73KV5u0GHXzh4NvNvnbbgRkZ`), four phone
clips and her voiceover from 2026-11-17. Her brief: *"simple editing today, minimal
animations, just cutting+subtitles"*. The first build in `RUTA/` (Ruta's pipeline moved there
today, beside `Nika/`).

## v2 (shipped) — her voiceover over everything but the intro and outro

Her note on v1: *"the part where I'm talking in the headphones … just speed that whole part up,
remove completely the text or the sounds … I'm gonna record everything that's not the
beginning, the intro or the outro."* She recorded it in her own words as one continuous take
(`Pptx w claude.m4a`, 19.6 s) rather than the six scripted lines, so it plays as one track
from the end of the intro and each section of footage is cut on her timing
(`work/r56/vo.py` → `mkplate.py` → `captions.py`). DUR 34.533 (1036 frames).

| plate | section | her words | footage |
|---|---|---|---|
| 0.00–11.07 | A | «Сьогодні ввечері в мене вебінар… ведення Threads з AI… з моїм Клодом. Погнали!» (to camera, her own sound) | `132849` 1.60–12.65 |
| 11.07–12.97 | S1 | «Відкриваємо Клод, натискаємо на New,» | `132924` sidebar → New, 1.8x |
| 12.97–18.40 | S2 | «і тепер я даю йому тему презентації та прошу підготувати основу дизайну, щоб далі все пішло набагато швидше.» | `132924` prompt pasted → sent, 2.4x |
| 18.40–24.47 | S3 | «Поки він це все робить, я голосовим записую, що я хочу сказати, деякі схеми мають бути, взагалі всі свої ідеї.» | `132924` her in headphones, 7x, its own sound and words gone |
| 24.47–27.07 | S5 | «Відправляємо, і через буквально 5 хвилин» | `134447` the voice notes in the chat, 1.4x |
| 27.07–31.97 | S6 | «маю готову презентацію, яку я можу далі редагувати.» + 2.4 s of slides | `135042` the clean title slide, then `134447` 2.0–7.7: her clicking through «Що сьогодні робимо» → «Яку модель обрати» → 02 → 03 → 04 → the prompt slide, 1.4x |
| 31.97–34.53 | G | «Якщо було корисно, то обов'язково підпишись.» (to camera) | `132849` 13.45–16.00 |

Her note on v2 (*"perfect"*, then): show the slides — *"I want to show how nicely it looks"* —
and cut the «Що обрати?» edit if it doesn't fit. So S6 is the slide flip from `134447` (the
moment she said «Ось він мені вже приготував основу» on camera), opened by the clean title slide
from `135042`, and holds 2.4 s past her last word; the edit is out. The cut lands on «маю готову».

Captions: the word rail (STYLE §00, her review of reel 41), her words as she said them;
whisper's «код» → «Клод». Intro: «ведення Threads з AI» (whisper heard «введення 3D за яй»;
re-decoded with a vocabulary prompt, `work/r56/redo2.py`). Voiceover levelled to her intro to
camera. No graphics, no sound cues, no push on the plate.

## v1 (superseded)

Her original clips cut in order: her on-camera lines, 9 s of her dictating with its own sound,
and the two silent stretches (the base prompt, the finished deck) carrying three scripted lines
as caption text. In git history at `15f2914`.

## Re-doing the voiceover

```bash
python3 work/r56/vo.py <her recording>     # SPLIT in vo.py: the words that open each section
python3 work/r56/mkplate.py
python3 work/r56/captions.py
cd reel-56 && python3 build.py && sh ../hf check && cd .. && python3 tools/hfrender.py reel-56
```

## Posted (2026-11-17, her call: «post it directly to my Instagram … something very simple … sharing is better»)

Instagram only, as a reel shared to feed, through Buffer, share now (post `6afc269754b9dc9e0726b28a`). Buffer
can't read the render's signed S3 link, so the final file went to HeyGen's asset store first
(`tools/hfasset.py` → `resource2.heygen.ai/video/b8fe2a1411bb4ee8a09aeac60ada06f3/original.mp4`).
Caption:

> Презентація до вебінару за 5 хвилин з Клодом 🫠
>
> Відправ подрузі-блогерці, яка досі робить презентації вручну
