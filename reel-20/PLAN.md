# Reel 20 — «Пам'ятаєш… штучних двійників»

Posts 2026-10-04 · ~82 s (247 words) · variant B · refined glass (STYLE.md §0)

## The chain

The one object is **her** — two versions of her. Early: clones of her, cut out
of her own plate and repeated behind her, desaturated, slightly off — the twin
hype. Late: her content pipeline as a chain of tiles where every step is
automated except the last one, and the last tile *is* her. The clones leave; she
stays.

## As built (2026-09-28, her cut: 93.95 s, 8 shots)

Re-timed to her words; `build.py` is the source of truth. Her old Kling twin
reel is not available, so every "twin" is her own matte (`her0`, shot 0),
greyed and a few frames out of sync. Two closeups are hers and stay clear:
24.13–26.43 («дорожче, складніше і довше») and 63.20–65.33 («але себе зі
зйомок не прибирай») — plan beats 7 and 13 moved around them.

| time | where | beat |
|---|---|---|
| 0.30–7.49 | BEHIND | four grey clones step out of her (her0 matte ×4, lagged); «AI» tags; step forward on «замінять»; the room behind everyone becomes beach / mountains / city on «знімати де завгодно» |
| 7.60–20.86 | NEAR | shelf: Kling tile → a twin reel jumps out → three reels → collapse into the peak of a views chart (1,2M → 3K flat on «затихло»); flame on «нахайпили»; tick on «ти права»; avatars jump onto the spike |
| 20.50–24.10 | OVER | iris out of the peak: ДВІЙНИК vs ТИ sheet, headers + empty tracks |
| 26.46–30.92 | OVER | same sheet: twin bars long, hers short; window / teleprompter / REC land on her portrait |
| 31.12–42.86 | NEAR | her portrait becomes a reel card; she is erased on «прибрати людину»; the twin glitches in; beach / mountains / city behind it; tick; €€€ on «грошей»; checklist on «рівень підготовки» |
| 42.50–49.02 | OVER | the twin's face full size; magnifier on the mouth with a slice one-two frames out and knocked sideways; then up to the eyes |
| 48.98–55.84 | NEAR | twin tile + money meter; fills on «постаратись», overflows off the frame on «вбухати туди гроші»; ROI ↓ |
| 56.12–63.10 | NEAR | four stages with hours; three count down to minutes and go automatic; filming is left |
| 65.44–74.79 | OVER | pipeline: AI analysis → RUTA (topics → script) → Claude (edit) → the last tile is her, live, and grows into the frame |
| 75.30–81.52 | NEAR | teleprompter reads along with her (front camera, REC) |
| 81.30–83.58 | BEHIND | one grey clone flickers in beside her and breaks up on «двійником» (tw2 matte) |
| 84.16–end | NEAR | IG poll: «Як тобі ШІ-двійники?» — Було зручно / Не пробувала |

## Beats

| # | line | where | what happens → hands to |
|---|---|---|---|
| 1 | «всі хайпили на темі штучних двійників» | BEHIND | copies of her fan out behind her — her own matte, repeated, greyed, a frame out of sync with each other |
| 2 | «замінять блогерів» | BEHIND | the clones step forward in a row |
| 3 | «можна знімати де завгодно» | BEHIND | each clone's backdrop swaps to a different plain colour field |
| 4 | «Я теж на цю тему стрибала, знімала рілси» | NEAR | **a clip of her old AI-twin reel** in a glass phone frame on the shelf, an «AI» badge |
| 5 | «все це якось затихло» | NEAR | a trend line spikes and flattens (shape only, no numbers) |
| 6 | «ми всі трохи нахайпили… круто вірусилась» | NEAR | the same line, the spike marked with a small flame |
| 7 | «набагато дорожче, складніше і довше, ніж… перед вікном з телефоном» | OVER | iris onto burgundy: a two-column sheet, ДВІЙНИК vs ТЕЛЕФОН, three rows filling on «дорожче», «складніше», «довше» — bars long on the left, short on the right |
| 8 | «прибрати людину з блогінгу взагалі» | BEHIND | iris closes; the clones behind her start to fade |
| 9 | «по-перше, коштує грошей» | NEAR | chip 1 with a € glyph |
| 10 | «по-друге… рівень підготовки» | NEAR | chip 2 with a checklist glyph |
| 11 | «на аматорському рівні… виглядає трошки дивно — рот не так» | NEAR | chip 3; her twin clip returns with a magnifier on the mouth, a one-frame glitch offset |
| 12 | «вбухати туди гроші… просто не рентабельно» | NEAR | a cost bar overflows the shelf edge |
| 13 | «скорочуй час на всі інші етапи… але себе зі зйомок не прибирай» | BEHIND | the last clones vanish; she is alone in the room |
| 14 | «штучний інтелект аналізує контент» | OVER | the pipeline starts on burgundy: tile 1, a chart glyph |
| 15 | «Рута допомагає знайти теми і перетворити думки на сценарій» | OVER | tile 2, RUTA wordmark; a cable; a packet turns into a script card |
| 16 | «Клод монтує відео за мене» | OVER | tile 3, Claude jelly; the packet turns into a reel |
| 17 | «встати перед вікном, увімкнути фронтальну камеру і читати текст з суфлера» | NEAR | iris closes onto tile 4, which is **her** — the live plate; a teleprompter shelf above her head scrolls the next line of her own script |
| 18 | «набагато краще, ніж… замінити себе двійником» | NEAR | one greyed clone flickers in beside her and is gone |
| 19 | «хто пробував таких двійників… зручно, чи ти так і не спробувала?» | NEAR | an IG poll sticker: «Було зручно» / «Не пробувала» |

## Captions

Blackout the ДВІЙНИК / ТЕЛЕФОН headers only if they land on those exact words.

## Assets

- **From her:** a 5–10 s clip from one of her old AI-twin reels — ideally a bit
  where the mouth is visibly off (beat 11) — and which platform made it, for
  the mark.
- Clones come from her own plate via `tools/matte.py` (behind-her beats only,
  a few seconds each).
- Have: Claude mark, RUTA wordmark rule.
