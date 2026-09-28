# Reel 13 — «Ти пробувала робити каруселі через ШІ»

Posts 2026-09-29 · ~71 s (214 words) · variant B · refined glass (STYLE.md §0)

## The chain

The one object is **a single carousel slide**. Early it is AI slop — glowing,
rainbow, stuffed with stickers, the deliberately bleak "before". Late it is the
same slide rebuilt clean from a template. Reel 19 is the promised follow-up and
opens on this clean slide, so the two reels hand off to each other.

Settled: this reel says «за 15 хвилин», reel 19 says 5 — both correct per her.

## As built (2026-09-28) — DUR 75.517, one shot, no NO_PAINT

| t | where | what |
|---|---|---|
| 0.05 | NEAR | glass shelf; slop stack on «каруселі», AI sparkle tile on «штучний», timer chip «15 хв» on «швиденько» |
| 4.16 | NEAR | chip rolls 15 хв → 2 год → 8 год → 1 день → **2 дні** (haptic), a sticker lands per roll |
| 6.26 | NEAR | Canva clear tile; a clean slide (kejs-galyny 04) pops out on «канві» |
| 7.88 | NEAR | effort meter: ТИ / ШІ rows (the AI tile slides into its row); promise → swap on «навпаки» → ТИ overflows off the frame on «більше» |
| 12.30 | BEHIND | shelf frost spreads, soft room (matte `wall`), wall of 62 real slides ripples out on «тебе не намахали», Instagram tile on «інстаграмі», pulled in on «чого не знаєш ти» |
| 18.9–22.4 | — | her line «і слава богу, що є я» left clear |
| 22.42 | OVER | iris out of a «1»; AI tile on «правильний», splits on «два типи» into picture model (image mark) / builder (</>) |
| 26.64 | OVER | left sheet: colour noise resolves into the slop (.png) |
| 28.42 | OVER | right sheet: wireframe snaps together on «збирає», blond-webinar 04 lands on «сайти» (.html) |
| 31.18 | OVER | left dims, the builder gets the tick on «другий» |
| 32.82 | NEAR | iris closes onto the slop as it rises over her head; 12 stickers slapped on through «не потрібні» |
| 36.12 | NEAR | stickers knocked off, flips to the clean slide on «другий»; a sticker bounces off it on «фізично» |
| 40.72 | OVER | «2»; the clean slide opens TK2 at 2×; style swatches on «навчити», step back on «а того»; layout zones on «розміщувати»; ТЕКСТ, ФОТО, smart guides on «де що стоїть» |
| 49.56 | OVER | the slide's picture fades, the zones stay: a template, locked on «шаблон»; iris closes onto it |
| 54.16 | BEHIND | five blond-trend slides dealt from the template into a fan behind her (matte `fan`), riffle on «швидко» |
| 56.18 | NEAR | fan collapses back; template on the shelf, the AI tile fills it: tексти / картинки / елементи |
| 61.98 | NEAR | «3», a text editor: headline typed by hand with a typo; AI ring fills on «навчити», body lands on «це робити!» |
| 68.46 | NEAR | glass notification: reel thumbnail, three slides on «повна система», the chip back at 2 дні → **15 хв** on «15» |
| 74.32 | NEAR | Стежити → Відстежується on «підпишись» |

Blackouts (plaque stays): 5.06–5.50 (chip «2 дні» on «другий день»), 73.08–74.00 (chip «15 хв»).

The slop slide is `reel-13/slop.py` — reels 17 and 19 import it from there.

## Beats

| # | line | where | what happens → hands to |
|---|---|---|---|
| 1 | «думала, що зробиш швиденько» | NEAR | a carousel stack on the glass shelf, a timer chip starts |
| 2 | «сидиш над нею вже другий день» | NEAR | chip flips «1 день» → «2 дні»; the top slide is visibly worse each flip |
| 3 | «швидше було б зробити в канві» | NEAR | a Canva clear tile slides in beside the stack and a finished slide pops out of it instantly |
| 4 | «автоматизація навпаки… більше роботи, ніж ШІ» | NEAR | two effort bars, ТИ and ШІ: hers overfills past the shelf edge, the AI's stays a sliver |
| 5 | «знають дещо, чого не знаєш ти» | — | her line, no paint |
| 6 | «Перше — обрати правильний ШІ. Є два типи» | OVER | iris onto burgundy, two white sheets side by side |
| 7 | «один малює картинки з нуля» | OVER | left sheet: noise resolving into the slop slide (the "before", garish on purpose — the one sanctioned off-palette frame) |
| 8 | «а інший збирає їх, як сайти» | OVER | right sheet: wireframe blocks snap into a clean layout, `</>` corner mark |
| 9 | «Нам потрібен саме другий» | OVER | left sheet dims and drops away; right slides to centre |
| 10 | «наліпить купу елементів» / «фізично не може наліпити» | OVER | ghost of the left keeps sprouting stickers at the edge; the right stays still and clean |
| 11 | «навчити… як розміщувати інформацію: скільки тексту, які картинки, де що стоїть» | OVER | layout guides draw over the clean slide, zones written in: ЗАГОЛОВОК / ТЕКСТ / ФОТО (text in a depicted interface) |
| 12 | «зробити собі шаблон» | NEAR | guides lock, the slide becomes a template tile; iris closes back to her |
| 13 | «почнеш робити каруселі швидко» | BEHIND | five finished slides fan out of the template behind her, big, like a hand of cards |
| 14 | «правильно написати сам текст… навчити той же самий ШІ» | NEAR | the text lines on the top slide type themselves; a Claude jelly tile with a skill chip sits beside |
| 15 | «в наступному рілсі… повна система… підпишись» | NEAR | dglass "next reel" card with the timer chip from beat 1, now reading the promised minutes; Follow → Following |

## Captions

No blackouts planned — no graphic repeats her words (ТИ / ШІ in beat 4 is a
label on a depicted bar, and a single word; drop that one caption only if it
reads doubled on the snapshot).

## Assets

Her real carousels arrived 2026-09-28, in `work/carousels/` (gitignored — client
work). She said to mix and match so it looks like many; reuse freely.

| set | slides | size | use here |
|---|---|---|---|
| `blond-trend` | 5 | 1080×1350 | **beat 13** — five slides, one template, same salon photo and hands: the template point made literal |
| `blond-webinar` | 12 | 1080×1440 | **the clean slide** in beats 8–11 (04 «дорогий блонд — це система» or 06 «і головне»), and the fan |
| `kejs-galyny` | 9 | 1080×1350 | a **draft** — placeholder boxes and «уточнити в Лери» notes on 02, 03, 07, 08; «фото …» labels on 01, 09. Only 04, 05, 06 are clean; 01/09 only small |

Faces (webinar 09–10, the testimonial on 11): keep them small, in a wall or a
fan, never a hero frame. A fourth set is on its way from her.

- Optional, for laughs: an early ugly AI attempt, if she kept one. Otherwise I
  build the slop slide myself.
- Have: Canva, Claude marks.
