# Voiceover style — "AI evolution" explainers

How the voiceover and captions for these reels are written. Each episode's text
goes into the `caption` / `vo` / `minus` fields of its file in `episodes/`. The
current scripts: [`VO-SCRIPTS.md`](VO-SCRIPTS.md).

## The shape (from Ruta's own drafts of episodes 1 and 2)

The reference reel she picked (a pool explainer: "If you dig a hole… you have a
pool. But… So you…") gave the chain. Her drafts show how it sounds in her voice,
and they win where the two differ.

1. **Open on what she already does, as a little story.** «Ти записала відео та
   виклала його в інстаграм.» / «Ти постиш контент кожного дня, але один рілс
   залітає, а інший — ні.» Talking to a woman («записала», «виклала»), not a
   deadpan "якщо…, у тебе є…".
2. **«Тоді ти…, але…».** The attempt and its catch are often one sentence. The
   connector is «Тоді», not «Тож».
3. **The catch is what it costs her:** nobody watches, you burn out, you go into
   the red, you don't understand a thing, you have to do it yourself every week.
   Not things physically breaking.
4. **The AI step gets credit first, then its limit.** «Він монтує самостійно, але
   лише на комп'ютері.» «Він усе проаналізував, але…»
5. **The steps are her real path and her real tools:** Claude with reel examples
   and skills, the cloud, the phone; screenshots, Buffer, Notion, a skill and a
   routine. Not a generic ladder: a step from the brief can go if it isn't hers.
6. **Loose and spoken:** «улітаєш в мінус», «мільйон скріншотів», «залітає».
   Sentences of 6–19 words, no forced symmetry, no term reveal, no punchline.
7. **«Тепер…» marks the new state,** and the ending is what she gets: editing from
   her phone whenever she likes; a full report with new ideas every Sunday.

## Length and pace

- 95–115 words for the whole episode, which is 40–50 seconds at 2.5 words a second.
- One step (attempt plus minus) is one or two sentences, about 15–25 words; her
  sentences run 6–19 words.
- Every sentence has to be something we can show: an action, an object, a face.

## Voice

- «Ти» to a woman, spoken Ukrainian: how she talks on camera, not how a post reads.
  The story moves in the present («Тоді ти…»), after an opening that can be past («Ти записала…»).
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
| Buffer | Баффер |
| Notion | Ноушн |

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
