# Reel 12 — «Бачила питання в Threads» (SMM-звітність через Windsor)

Posts 2026-09-28 · ~41 s (123 words at her ~3 w/s) · variant B · refined glass (STYLE.md §0)

## The chain

This is the reel the style test was cut from, so the middle is already built:
`style-test/build.py` is beats 4–8 almost verbatim — lift them, re-time to ASR.

The one object is **the report**. Bare early: the Threads post, a girl doing it
all «вручну». Paid off late: the Monday report that arrives by itself.

## Beats

| # | line | where | what happens → hands to |
|---|---|---|---|
| 1 | «Люди, які автоматизували… вручну 😫» | BEHIND (or NEAR if her head leaves < 560 px clear) | the Threads post as a white glass card, big, lower edge tucked behind her head; handle blurred out. Words light up as she reads them (Apple Music lyrics), pink marker sweeps «робити все вручну». **Blackout captions** — the card says it |
| 2 | «Привіт, я Рута — твоя технічна продюсерка» | NEAR | the card folds up into a dglass name capsule above her head: «Рута · технічна продюсерка». **Blackout** those words |
| 3 | «розкажу як це можна автоматизувати!» | NEAR | the capsule stretches into an iOS toggle; the knob slides ON on «автоматизувати» (liquid stretch mid-travel, track fills burgundy → pink) |
| 4 | «через Windsor, підключений до Claude або ChatGPT» | NEAR | knob becomes the Windsor «w.» pearl tile on a glass shelf; cable draws; Claude jelly lands; flips to ChatGPT on «ChatGPT» (FLIP, not on «або») — test §A |
| 5 | «Інстаграм, Фейсбук, таргет, ТікТок, статистику сайту» | BEHIND | the shelf's frost spreads into the room; hub moves up; five clear tiles land on their words around her, wired to the hub, packets travel — test §B |
| 6 | «і ще мільйон інших джерел даних» | BEHIND | the wall ripples out of the hub behind her — test §B |
| 7 | «налаштувати повторювану рутину в своєму ШІ» | NEAR | wall collapses into the hub; hub flips to Claude; a repeat ring draws round it and keeps turning (the loop is the meaning) |
| 8 | «Наприклад, кожен понеділок» | OVER | iris opens out of the ring onto burgundy: a month sheet, every Monday lights up top to bottom |
| 9 | «Claude збирає статистику з усіх джерел» | OVER | calendar shrinks to a chip «ПН 09:00»; source marks stream into the Claude tile, bump per hit |
| 10 | «аналізує її за твоїми критеріями» | OVER | three criteria chips tick ✓ under the tile (Охоплення · ER · Ліди) |
| 11 | «гарненько сформований звіт» | OVER | the report sheet grows out of the tile — test §C (+38 %, chart, three rows) |
| 12 | «Тадааам! Автоматизація» | NEAR | sheet folds into the notification as the iris closes onto it; haptic shake — test §D |
| 13 | «став + в коментарі і ми поспілкуємось» | NEAR | notification turns into an IG comment composer; «+» types, send, a heart lands on the posted comment. **Blackout «+»** |

## Captions

Blackout: beat 1 (the read), beat 2 («Рута … продюсерка»), beat 13 («+»).
Everything else keeps captions, including over the burgundy.

## Assets

Have everything: Windsor «w.», Claude, ChatGPT, Instagram, Facebook, Meta, TikTok,
Google Analytics marks. Nothing needed from her.

## As built (2026-09-28, re-timed to her cut, DUR 44.350)

Her cut: 0–11.33 reads the post off a tablet; 11.33–44.39 to camera. No
inserts, no pull-outs → NO_PAINT empty. Head top y 580–660 all reel.

| t | placement | beat |
|---|---|---|
| 0.00–7.34 | behind (matte `post`) | Threads post rises off the tablet, words light as read, marker on «все робити вручну» |
| 7.05–12.62 | near | name capsule (her face as avatar) → «Звітність СММ» toggle, ON on «автоматизувати» 10.72 |
| 12.28–18.0 | near | knob → disc on the shelf (ghost w./Claude) → Windsor 15.14 → cable 15.84 → Claude 16.50 → ChatGPT 17.06 |
| 18.0–24.6 | behind (matte `room`, soft room) | sources 19.06–21.08, wall on «мільйон» 22.14, collapse 23.72 |
| 24.84–27.68 | near | repeat ring on «повторювану», hub flips to Claude on «штучному» |
| 27.30–35.50 | over | iris → September, Mondays on «понеділок» → «ПН 09:00» + Claude, sources stream in → criteria tick → report |
| 35.19–37.62 | near (matte `tada` from 35.50) | notification, haptic on «дам»; her raised arm passes in front |
| 41.10–end | near | comment composer: «+» typed 42.58, posted 42.92, liked 43.52 |

Dropped from the plan: nothing. Beats 9–11 merged into one takeover container;
the notification does not turn into the composer (3.5 s of her talking sits
between them).

The soft room is `work/r12/softroom.sh`: blur(plate×(1−α))/blur(1−α) in float,
from the `room` matte — her silhouette is filled from the room, no halo.
