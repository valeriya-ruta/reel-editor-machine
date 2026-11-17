# Voiceover style — "AI evolution" explainers

How the voiceover and captions for these reels are written. Draft: to be tuned
against Ruta's example reel. Each episode's text goes into the `caption` / `vo`
/ `minus` fields of its file in `episodes/`.

## The shape: a chain, not a list

Every step happens *because* the step before it failed.

1. **Open on the want, in the viewer's words, and the obvious first move.** One
   breath: what she's trying to do, and what she does about it. No intro, no
   greeting, no "сьогодні розкажу". Tool names don't open a reel: her
   «Дзвінок → ідеї» reel opened with tools and lost 67% of viewers in the first
   seconds, and she switched to opening with the real question.
2. **The minus**, starting with «Але…». Concrete and felt: lost hours, money,
   forgetting, embarrassment, chaos. It has to be the reason for the next step.
3. **The next move**, starting with «Тоді…», «Тож…» or «Окей,…». It fixes the
   last minus and brings its own.
4. **The last step is the AI setup she actually uses.** No minus. It ends on the
   result and a calm payoff: the work happened while she did something else.
   No call to action, no outro (the brief: the reel ends on the final state).

## Length and pace

- 95–115 words for the whole episode, which is 40–50 seconds at 2.5 words a second.
- One step (attempt plus minus) is one or two short sentences, about 15–20 words.
- One idea per sentence. A sentence over ~12 words gets split.
- Every sentence has to be something we can show: an action, an object, a face.

## Voice

- «Ти», present tense, spoken Ukrainian: how she talks on camera, not how a post reads.
- Plain words. No канцелярит: «задля», «здійснювати», «наразі», «у рамках».
- Honest about limits, the way she is: "80%, not 100%", "you still check it with
  your own eyes". No hype: «магія», «революція», «в один клік».
- Everyday comparisons are hers: skills are muscle memory, connectors are hands,
  a routine is like brushing your teeth.
- No exclamation marks and no rhetorical questions, except the opening want.

## Truth

- Only facts and numbers she has said or shown. Her own figures are fine (a
  cloud render costs her 15–20 cents a reel; an editor charges about 30 € a reel;
  she spends about 10 active minutes per reel). Invented view counts,
  followers or results are never fine.
- Her real workflow wins over a generic one. For example: the free Fathom
  records her calls, Claude writes the offer, and she always reads it before it goes out.

## Written for the voice (ElevenLabs Matilda, via OpenRouter)

The voiceover is ElevenLabs' stock voice Matilda, generated through OpenRouter:
no clone, no recording. The `vo` text is what she reads, so spell it the way it
should sound:

| caption (on screen) | vo (spoken) |
|---|---|
| Claude | Клод |
| Fathom | Фатом |
| ClickUp | Клікап |
| Canva | Канва |
| Instagram | інстаграм |

- Numbers as words: «тридцять євро», not «30 €».
- No abbreviations, no slashes, no emoji.
- Commas and «—» set the pauses; keep «…» for a real trailing-off.
- If a word comes out with the wrong stress, rephrase it; Ukrainian stress marks
  aren't reliable in TTS.

## Captions

- 2–5 words, on screen while the line is spoken.
- One key word in `*stars*` gets the yellow marker.
- Product names stay in Latin here (Claude, Fathom, ClickUp).
- A long final step can change caption mid-way: give the beat its own `caption`.

## Output, per step

```
caption:  2–5 words, one *key word*
vo:       the attempt, as it is spoken
minus:
  caption: …
  vo:      «Але…», as it is spoken
```

## Worked example: episode 5 (calls), 96 words

| caption | vo |
|---|---|
| Оффер — *одразу* після дзвінка | Хочеш одразу після дзвінка надіслати клієнтці оффер, поки все свіже. |
| Але *не пам’ятаєш*, про що домовились | Але вже за годину не пам'ятаєш, про що саме домовились. |
| Пишеш *нотатки* на дзвінку | Тож пишеш нотатки прямо під час розмови. |
| Але губиш *фокус* | Але дивишся в блокнот, а не на людину, і забуваєш свої ж питання. |
| Вмикаєш *запис* | Окей, вмикаєш запис дзвінка. |
| І перемотуєш *всю годину* | Але щоб знайти одну домовленість, передивляєшся годину запису на перемотці. |
| *Fathom* + Claude | Тоді підключаєш до Клода безкоштовний Фатом, і він сам розшифровує дзвінок. |
| Задачі й оффер — *руками* | Але задачі й оффер однаково переписуєш руками. |
| Робиш *скіл* → Задачі вже в *ClickUp* → *Оффер* — чернетка → Лишається *перечитати* | Тож робиш скіл. Дзвінок закінчився — задачі вже стоять у Клікапі з дедлайнами, а чернетка оффера чекає в чаті. Тобі лишається перечитати її і надіслати. |
