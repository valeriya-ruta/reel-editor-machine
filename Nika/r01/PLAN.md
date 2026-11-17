# Nika r01: «Шукаю 25 експертів», plan

Source: `IMG_7332.MOV`, 72.2 s, one continuous take (no cuts), front camera,
warm beige wall. Spelling: `script.txt`. Timing: `Nika/work/r01/words.json`
(faster-whisper large-v3).

## Whisper's mistakes, fixed in script.txt

| ASR heard | she said | at |
|---|---|---|
| «для перших сьогодні. Та експертів» | «для перших **ста** експертів» | 57.2 s |
| «побачимося на день» | «побачимося на **демо**» | 71.3 s |
| «коучи» | «коучі» | 59 s |

Both confirmed against her earlier version of the same script (`example.MOV`),
where she says «перших 100 експертів» and «побачимося на демо».

## The language

- **Her**: full frame, untouched, for the personal lines. No circle crop.
- **Product**: full-screen shots of the real UNLOCK UI. Each shot is an angled
  3D mockup on a clean white-to-lavender stage, with a slow push-in and a little
  drift, like a normal app promo. One idea per shot, and one move per shot.
- **Captions**: short phrases in pink type on the torn grid-paper plaque, the
  one text style for the whole reel. They sit in the lower-middle, clear of
  Instagram's UI.
- **Sound**: soft click on each caption, whoosh on each cut to product, pop when
  a card lands, ka-ching on the offer. Everything sits under her voice.
- UI source: the site's own product mockups (`unlockexpertise.online/uk`),
  captured at 3× so zooms stay sharp.

## Cuts and grade (as built)

- **Spans kept** (source seconds): 0.52–14.92, 15.52–20.00, 20.42–45.05,
  45.85–55.00, 55.36–68.40 and 68.66–72.10. That makes 69.1 s from 72.2 s.
  Pauses over 0.5 s are tightened to about 0.3 s, and the lead-in is trimmed.
  - Three cuts land under the stage, so they can't be seen.
  - The two cuts on her (before «А якщо…» and before «Пиши…») hide behind a
    step to a closer frame.
- **Grade:** `tools/plate.py` GRADE. It takes out the orange cast of her camera
  filter, adds a touch of contrast and a light sharpen. Approved on a still.
- **Voice:** −33 LUFS in, −14 LUFS out.

## Beats (as built; source times)

| time | line | on screen |
|---|---|---|
| 0.5–8.7 | Привіт! Я шукаю 25 експертів… без команди. Раніше для цього | Her. A snap zoom on «25 експертів» |
| 8.7–14.9 | потрібні були сайт, телеграм-бот, платіжна система, купа інтеграцій і ще хтось… | Stage, greyed: the old way. One tile per thing she lists, piling up; they fall away on the cut |
| 15.5–18.0 | А тепер достатньо лише двох речей | Her |
| 18.0–20.0 | твоєї експертизи та Unlock | Stage: «твоя експертиза» scrap + the Unlock logo |
| 20.4–23.0 | Мене звати Ніка, і я працюю над Unlock | Her |
| 23.0–29.8 | над платформою… мінікурси, приймати оплати, продавати… і все в одному місці | Product, approved in the look test: home + click → editor → payments + ka-ching → sales page + click → pull back to everything |
| 29.8–35.7 | І зараз я хочу особисто познайомитися… Тому запрошую тебе | Her |
| 35.7–41.3 | на 20-хвилинну демозустріч зі мною, де я покажу платформу, відповім на запитання | Stage: an invite card («Демозустріч з Нікою · 20 хвилин · онлайн»), then a call window screen-sharing the dashboard, with a «?» and a typing reply |
| 41.3–50.3 | і ми разом подивимося… саме тобі. А якщо після зустрічі… цього тижня | Her |
| 50.3–55.0 | то ти отримаєш цілий рік Unlock за ціною одного місяця | Stage: 12 month tiles; all but «1» dim, «ціна 1 місяця» lands with the ka-ching |
| 55.4–59.0 | Пропозиція діє тільки для перших ста експертів | Stage: a count up to a big gradient «100», «перших експертів» |
| 59.0–66.0 | Психологи, коучі, викладачі мов… і всі-всі-всі | Her. Her words as chips in the site's style, one per word; then the site's 12 fields burst in around her |
| 66.0–68.4 | хто хоче монетизувати свої знання | Her |
| 68.7–72.1 | Пиши Unlock у коментарях, і побачимося на демо | Her, with a comment box typing «Unlock», then sent and a heart |
