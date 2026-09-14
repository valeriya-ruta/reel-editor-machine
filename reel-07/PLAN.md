# Reel 7 — «системи, які я б поставила з самого початку»

133.3 s, variant B (no burned-in subtitles), 1080×1920 @30.

## The recurring object

A **system board**: six squircled tiles that land one at a time as she names
them, stay on the board, and at «командний центр» wire themselves into a hub.
STYLE.md §4 «reuse objects» — the board is the argument, not decoration. By the
CTA the viewer has watched a stack get built, which is the thing the script is
selling.

Board geometry: 3×2 grid, 300px tiles, 40px gutter, centred, living in the clear
band (y 60–540) while she talks. It leaves for the big single-system beats and
comes back to accept the next tile.

## Beats

| # | line | shows |
|---|---|---|
| 1 | «думати про системи вже зараз» | an empty board draws itself — six frosted slots, nothing in them yet (§5a.9, the empty plaque before the filled state) |
| 2 | «а не через півроку» | a clock hand sweeps half a turn; the slots stay empty |
| 3 | «звідки прийшли твої клієнти / скільки грошей / з ким ти розмовляла» | three answers fall out of the frame one per phrase — a source arrow, a number, a face — and do not come back |
| 4 | «що б я зробила прямо зараз» | the board resets, first slot lights |
| 5 | «система запису на консультації» | slot 1 accepts a **calendar** |
| 6 | «"коли тобі зручно"» | two chat bubbles volley back and forth, accelerating, going nowhere |
| 7 | «просто давати посилання» | the volley collapses into a single link chip |
| 8 | «людина сама обирає час» | a slot on the calendar fills itself |
| 9 | «Cal.com… синхронізується з Google Календарем» | the Cal mark and the Calendar mark join by a wire; the event copies across |
| 10 | «Друге — Fathom, який записує дзвінки» | slot 2 accepts the **Fathom** wordmark card |
| 11 | «зберігає одразу в тексті» | a waveform resolves into lines of text (§5a.3 bar rhythm) |
| 12 | «щоб не переслуховувати весь дзвінок» | a scrub bar tries to replay and is struck out |
| 13 | «Третє — CRM» | slot 3 accepts a **database** glyph — no brand exists (§5b) |
| 14 | «базових полів: хто / звідки / чим займається / що хотіла» | a row fills field by field, one per word (§4 «every element on its word») |
| 15 | «що вже зроблено, який наступний крок» | two more columns; the last cell is the only accent on the card (§5a.4) |
| 16 | «дня народження» | a small cake lands in a corner cell — drawn, no emoji artwork on the machine |
| 17 | «роблю це просто в Notion» | the **Notion** mark drops onto the CRM card |
| 18 | «Четверте — система для задач» | slot 4 accepts a **checklist** |
| 19 | «здається, що само запам'ятається» | three tasks fade out mid-air, unrecorded |
| 20 | «почнеш все забувати» | the same three re-land as checked rows in the list |
| 21 | «тримаю задачі теж в Notion» | the Notion mark returns — the same object twice, §4 |
| 22 | «показати процес цікавіше, ніж результат» | a finished trophy shrinks; the messy process behind it grows |
| 23 | «один дзвінок — це вже ідеї для контенту» | one call card fans into several content cards |
| 24 | «словами твоєї цільової аудиторії» | a quote lifts out of the call and sets itself in the content card |
| 25 | «на вагу золота» | the fan of cards tips a balance |
| 26 | «мій додаток RUTA» | slot 5 accepts the **RUTA** wordmark — all caps, heaviest weight available, her call |
| 27 | «на основі голосових створює рілси, сторіс, каруселі» | a voice note splits into three outputs |
| 28 | «10 євро на місяць» | the number, alone (§4 — a number is the one word allowed) |
| 29 | «замінює тисячу промтів і підписок» | a wall of small tiles collapses into the one RUTA tile |
| 30 | «командний центр… Клод або GPT» | slot 6 accepts **Claude**; the GPT mark sits beside it as the alternative |
| 31 | «екосистема між чатом, коворком, дизайном і кодом» | four panes open around the Claude tile, one per word |
| 32 | «з тарифу за 20 євро» | the number |
| 33 | «найбільша витрата, але вона того варта» | the six tiles wire into the hub — the board completes **behind her** (matte beat) |
| 34 | «з людини, яка все робить руками, до людини, яка думає» | hands→head: the wired board lifts off the tiles and becomes one shape |
| 35 | «відправ цей рілс подружці» | a send arrow leaves the frame |

## Mattes

Two beats earn one (STYLE.md §1 — size is the trigger, 3.3 s/frame CPU):

- **b33** the completed six-tile board wiring up, full width behind her head
- **b29** the wall of a thousand tiles collapsing

Everything else is board-sized and sits in the clear band or low over her chest.

## Missing assets

`cal.png`, `google-calendar.png` — drawn as calendar glyphs until she uploads
them. `RUTA` is type, not artwork, by her decision: no icon exists yet.

---

## What the delivered audio changed

Written against the script; these are the places her actual cut overruled it.

**She cut the ending.** The script closes «…але вона того варта: саме вона
перевела мене з людини, яка все робить руками, до людини, яка думає про більші
речі, а не про те, які задачі виписати з дзвінка.» None of that is in the
audio — she goes straight from «вона того варта» to «до речі, відправ цей рілс
подружці». So the planned hands→mind beat does not exist, and the board-wiring
beat carries that section alone.

**She improvised the booking gag.** «а у вівторок, а у четверг» is not in the
script. It is the funniest three seconds in the reel and it is hers, so
21.30–24.80 is graphic-free and the chat-volley beat planned for it is gone.

**She pulls the camera way out at 11.0–14.7s**, across «звідки прийшли твої
клієнти, скільки в тебе грошей, з ким ти розмовляла». That is a zoom inside one
continuous shot, so `tools/shots.py` never saw it — `tools/pullouts.py` exists
now because of it. The three-things-falling-out beat planned there is gone: the
pull-out *is* the beat.

## No-paint zones, final

    3.63 –  4.83   punch-in to her hands      (cut)
   11.00 – 14.75   pulled way out             (zoom)
   16.30 – 17.27   big face closeup           (cut)
   21.30 – 24.80   «а у вівторок, а у четверг» (hers, flagged by her)
   61.47 – 63.17   pulled way out             (cut)
   67.27 – 68.10   punch-in to her hands      (cut)

## Mattes, final

One, not two. Everything else in this reel lives in the clear band above her
head and never needed to pass behind her — the board geometry (y 36–556) keeps
it there by construction. The exception is **b22**, «замінює тисячу промтів»,
where the wall now runs y 60–1050 and goes behind her shoulders on purpose.
~6 min of CPU for 118 frames, which is what STYLE.md §1 says that is worth.
