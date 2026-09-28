# Reel 18 — «Знаєш, коли на сайті просто висить кнопка» (Telegram Business)

Posts 2026-10-03 · ~66 s (197 words) · variant B · refined glass (STYLE.md §0)

## The chain

The one object is **the chat the visitor lands in**. Bare early: an empty chat,
a blinking cursor, a manager who answers in an hour. Paid off twice: the same
chat opening with the message already typed, and then a bot answering it
instantly.

The middle is **her screen recording as the whole frame, with her cut out in the
bottom corner**, as if shot on greenscreen — her explicit ask. She explains
where to click while her phone does it behind her.

## Beats

| # | line | where | what happens → hands to |
|---|---|---|---|
| 1 | «кнопка «написати в Телеграм»» | NEAR | a glass site button above her head; it presses on «Телеграм» |
| 2 | «заходить в чат з менеджером — і там пустота» | OVER | iris onto burgundy: a white Telegram chat sheet, empty, cursor blinking — the bare state |
| 3 | «сидить і думає, з чого почати» | OVER | typing dots appear, stop, appear, stop |
| 4 | «менеджер відповідає через годину» | OVER | a clock chip spins to «+1 год» |
| 5 | «половина людей просто закриває чат» | NEAR | iris closes to a row of ten people glyphs; five fade out |
| 6 | «прискорити приблизно в два рази» | NEAR | a «×2» chip |
| 7 | «Telegram Premium, який коштує якісь копійки» | NEAR | the Telegram clear tile gains the Premium star; a tiny «копійки» coin chip |
| 8 | «Заходиш в налаштування… скролиш вниз… Telegram Бізнес… посилання на розмову» | **SCREEN** | **her screen recording fills the frame; she is cut out bottom-left at ~45 %**, head just under the caption band. Each menu item she names gets a glass highlight and a gentle punch-in; a pink tap ripple on every tap |
| 9 | «Створюєш нове посилання… прописуєш текст… «доброго дня, мене цікавить те й те»» | **SCREEN** | punch-in on the text field as it is typed. **Blackout** the quoted phrase — it is on screen |
| 10 | «Зберігаєш, береш це посилання і вставляєш на сайт» | **SCREEN → NEAR** | the copied link lifts off the recording as a glass chip, the recording iris-closes, and the chip drops into the site button from beat 1 |
| 11 | «коли людина тицяє на кнопку… вже написане повідомлення» | OVER | the chat sheet from beat 2 again — now opening with the message pre-typed in the input |
| 12 | «залишається просто відправити» | OVER | send; the bubble flies up, ✓✓ |
| 13 | «спрощує життя всім» | — | clear |
| 14 | «другий крок цікавіший… тригер до чат-бота» | NEAR | a bot tile wires itself to the chat |
| 15 | «турагенція… «вітаю, мене цікавить подорож на Мадейру»» | OVER | incoming bubble with that text. **Blackout** the quote |
| 16 | «бот одразу розпізнає… надсилати деталі про подорож» | OVER | the bot answers instantly: a trip card (Мадейра, a route line, a PDF chip) — no invented prices |
| 17 | «поки твій менеджер ще доп'є каву» | NEAR | a coffee cup with steam; the manager's status «був(ла) нещодавно» |
| 18 | «Якщо було корисно — підпишись» | NEAR | Follow → Following |

## Captions

Blackout the two quoted messages (beats 9, 15). During the screen recording the
captions stay at their usual height; her cutout sits below them.

## Machine time

Her cutout runs for the whole recording segment (~20–30 s). At 1.75 s/frame
that is ~20–25 min of CPU on her laptop — the biggest matte of the week, still
fine.

## Assets

- **From her — already on her list:** the screen recording. What makes it
  cuttable:
  - vertical, full screen, Telegram in Ukrainian;
  - **start from Settings, not the chat list** (the chat list shows her real
    chats) — or tell me to blur it;
  - slow: rest ~1 s on each screen before tapping;
  - the full path: Settings → scroll → Telegram Business → Посилання на
    розмову → create → type the message → save → copy the link;
  - then, if possible: tapping such a link so the chat opens with the message
    pre-typed, and sending it;
  - if she has a demo bot: the «Мадейра» message getting the automatic reply.
    If not, I build that chat as a graphic.
  - Android: turning on *Show taps* in Developer options helps me place the tap
    ripples exactly; optional.
- Have: Telegram mark.

## As built (2026-09-28)

- DUR 70.583. Her cut is two shots (jump cut at 45.07), no inserts: nothing is NO_PAINT.
- Her recording is 1080×2082, English UI, 28 s; `screen.py` re-times it onto her
  words (9 constant-speed segments + a held last frame, 22.00–37.10) and blurs
  her phone/@username on the Settings header, her existing links and their
  preset messages, and the new link's address (card + clipboard bar). Her
  Profile tab and the link list after copying are not used at all.
- The recording's message is «Привіт! Хочу на Мадейру!», not the spoken «доброго
  дня, мене цікавить те й те» — so beat 9 keeps its captions (no redundancy),
  and beats 11–14 carry her real message (the chat opens with it pre-typed, it
  is sent, it becomes the trigger). Beat 15 types her spoken quote (blackout).
- Her cutout: matte `her` 22.00–37.10, the whole plate cut out, seated at 45 %
  bottom-right (head top ~1548). She shrinks only after the recording has
  irised in behind her, and grows back before it irises out, so there is
  never a second her.
- The bot's trip card and the pre-typed chat are graphics (her recording has
  neither). No prices.
