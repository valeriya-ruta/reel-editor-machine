# Voiceover style — "AI evolution" explainers

How the voiceover and captions for these reels are written, tuned against the
reel Ruta picked as the closest style: @dee.ugctips, the pool explainer, its
first 25 seconds. Each episode's text goes into the `caption` / `vo` / `minus`
fields of its file in `episodes/`. The current scripts: [`VO-SCRIPTS.md`](VO-SCRIPTS.md).

## The shape (from the reference reel)

The reference, word for word:

> If you dig a hole in your yard and fill it with a hose, you have a pool. But the
> dirt walls crumble and the water turns to mud. So you build a cage of steel bars
> and spray concrete over it. This is shotcrete. But concrete is rough and it cracks
> when the ground moves. So you coat it in smooth plaster with a band of tiles at
> the waterline. But leaves blow in and the water turns green. So you add a…

What makes it work, and what we copy:

1. **It opens on the naive version already "working".** «Якщо [найпростіший крок],
   у тебе є [результат].» Deadpan and confident, a little funny, because it's
   obviously not enough.
2. **Then two beats, over and over, never varied.** «Але [що ламається].» /
   «Тож ти [конкретна дія].» The repetition is the rhythm, so no «Тоді» or
   «Окей» for variety.
3. **Every «Але» is physical and visible:** the cause and what you see, in one
   sentence (the walls crumble *and* the water turns to mud). No feelings words;
   the chibi plays the feelings.
4. **Every «Тож ти» builds on what's already there** ("coat *it*"), so one thing
   grows step by step.
5. **One term reveal per episode, two words:** «Це — скіл.» right after the
   viewer has seen what it does, the way "This is shotcrete." lands.
6. **Pace:** about 3.3 words a second in English; sentences of 8–15 words, with a
   very short one now and then for punch.
7. **The ending is ours.** The reference cuts off mid-sentence because it turns
   into an ad. Our episodes end on the last setup working, and the payoff.

As in the brief, the last step is the AI setup she actually uses: no «Але», no
call to action, no outro. Tool names don't open a reel: her «Дзвінок → ідеї»
reel opened with tools and lost 67% of viewers in the first seconds.

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
- No exclamation marks, no rhetorical questions.

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
