# Meme library: comic relief for Ruta's reels

63 files, all in this folder as `NN-slug.ext` (renamed from the camera-roll names in her Drive
`Memes` folder; the NN is stable, don't renumber). Read this index, pick by **use**, never by
browsing the images. Captions are transcribed exactly as burned into the image.

## Rules for placing one (her rules, updated 2026-11-23)

- **Slapped straight onto the reel — no plaque, no white frame, no glass card**, in the zones she
  marked: `top` (the band above her head), `r` (beside her head, right), `l` (low left, over her
  shoulder). Never over her face, never over the captions.

- **Comic relief, after the beat lands.** A meme reacts to the line she just said; don't cover a
  line she is still in the middle of. About 1-1.4 s: a quick pop in (0.28 s), a quick drop out.
- **Max 3 per reel** (counted as images). **Two at once is allowed** (a pair, slots `l` + `r` in
  `g.meme`), but only when it really makes sense AND there is a long break between animations
  (no behind-me word, card, half or full screen for a few seconds either side).
- **Never in the CTA.** Nothing from the CTA line's first word to the end (`g.cta_start`).
  The first 3 seconds are allowed again, if it fits.
- **Profanity is allowed, always.** No filter; the 🔞 tag below is only information.
- **Match the feeling, not the topic.** If nothing fits a moment, put none; 3 is a cap, not a quota.
  Aim for 1-3 per reel, spread out, not clumped.
- **Language:** captions are Ukrainian; on an English reel use the `[no text]` ones (or 41).
- Near-duplicates exist (Цить 01/37, «хоспаде» 24/57, «грандіозна робота» 36/62 RU, 62 UA).
  Use the sharper copy (01, 57, 62); the other is a spare.
- Image sizes are mixed (320 px up to ~1200 px). The small ones (01, 02, 37) get blurry in the
  `top` slot: give them slot `l`/`r` or skip them.
- In the build: `g.meme(F, J, "42", t_word_end + 0.1, dur=1.2)`, from `tools/gstyle.py`. It copies the file
  into `reel-NN/assets/memes/` and refuses a 4th meme, one touching the CTA, or a stray overlap.

## Index

Tags: **who/what** · **feeling** · **use when she says…**

### Phones, calls, "no time"
| # | file | caption | feeling | use when… |
|---|---|---|---|---|
| 02 | nema-chasu-empty-watch | нема часу | dismissive | "I don't have time", deadlines she's ignoring |
| 03 | alo-zhelejna-fabryka-budgie | альо желейна фабрика, пожалійте мене | begging, absurd | asking for mercy, overload, "please be gentle" |
| 32 | budgie-bell-ia-perezvonyu | я перезвоню | avoidant | dodging a client/ask, "I'll get back to you" |
| 59 | cockatiel-alividerchi | алівідерчі | peeking out, bye | leaving a topic, "so… moving on", sign-off |

### Deadlines & work (the workhorse set for a freelancer/agency reel)
| # | file | caption | feeling | use when… |
|---|---|---|---|---|
| 23 | yakyj-status-po-zadachi-dark-painting | який статус по задачі | dread, hiding | client/manager chasing, "any update?" |
| 26 | lovebird-nicho-nicho-vstyhaiem | нічо нічо встигаєм | calm denial | she says she'll make the deadline (she won't) |
| 27 | mister-kot-vstyhaiem-dedlajn | містер кот, встигаєм до дедлайна? / встигаєм, але дедлайн прийдеться перенести | the lie, then the truth | missed deadlines, over-promising |
| 42 | harold-dedlajn-vchora | зараз подивлюсь, коли дедлайн / Вчора | forced smile, pain | the deadline was already yesterday |
| 28 | yeti-vizmesh-shche-proekt-davajte | — Візьмеш ще один проект? Я: давайте | yes-person gremlin | taking on too many projects, can't say no |
| 29 | hedgehog-posadovi-obovyazky | бачиш яка велика хуйня це мої посадові обов'язки 🔞 | existential, tiny vs huge | scale of the job, "this is my actual role" |
| 36 | dog-headset-rabota-proveedena-ru | РАБОТА ПРОВЕДЕНА ГРАНДІОЗНА, АЛЕ ВИЙШЛО ПОГАНО | proud and wrecked | big effort, bad result |
| 62 | dog-headset-hrandiozna-robota | була зроблена грандіозна робота, але вийшло погано | same, nicer type | same (preferred copy) |
| 33 | dog-old-pc-des-projob-ale-de | десь пройоб але де | debugging, lost | hunting for the mistake, "something's off but what" |
| 25 | cat-zhurnal-obliku-myshej | Блять, який нахуй журнал обліку мишей 🔞 | bureaucratic rage | pointless admin/paperwork |
| 34 | kitten-khikhanky-zakinchylys | хіханьки хаханьки закінчились | mood switch | the fun part ended, now serious |
| 22 | obitsiaty-i-na-moroz-mouse-fairy | ОБІЦЯТИ І НА МОРОЗ! | smug, bad-faith promise | promising and not delivering |

### Tech, tools, "what did I click"
| # | file | caption | feeling | use when… |
|---|---|---|---|---|
| 57 | khospade-kuda-ia-zhmav-kitten-b | хоспаде, куда я жмав? | panic, lost | a tool did something unexpected, wrong button |
| 24 | khospade-kuda-ia-zhmav-kitten-a | same, taller crop | same | spare of 57 |
| 46 | cat-laptop-bozhe-pomozhy | боже поможи | helpless | confusing interface/setting, "help" |
| 48 | hedgehog-keyboard-de-knopka | дє туть кнопка йди нахуй 🔞 | rage at UI | can't find the button |
| 08 | cat-screaming-at-laptop | [no text] orange cat yelling at laptop | rage at the screen | bug, crash, lost work |
| 61 | woman-biting-laptop | [no text] woman biting her laptop | breaking point | the 5th failed attempt |
| 20 | dog-glasses-phone-treba-zh-take | ти бач, треба ж таке | doomscrolling, "wow" | discovering a trick/news, mild surprise |
| 40 | budgie-breaking-news-pm | BREAKING NEWS: Папуга навчився говорити "Ну шо там?" і був підвищений до Проджект Менеджера | office satire | PM jokes, status meetings (dev/design humour) |
| 38 | monster-basement-rozkazhy-pro-aiti | Вийди та розкажи гостям про це своє айті | embarrassing relative | being asked to explain her job/tech at a party |
| 56 | dog-tsej-vo-zabuv | Цей во… Забув… | blank, melancholic | forgot something mid-thought |

### Reactions: shock, disbelief, "what"
| # | file | caption | feeling | use when… |
|---|---|---|---|---|
| 63 | fish-sho-za-khujnia | шо за хуйня 🔞 | baffled | something absurd, bad client request |
| 30 | old-man-nikhuia-sobi | НІХУЯ СОБІ БЛЯТЬ 🔞 | stunned | a big number/result |
| 07 | cillian-side-eye | [no text] | awkward side-eye | cringe moment, someone said something dumb |
| 14 | cat-shocked-closeup | [no text] | wide-eyed shock | reveal, "and the price was…" |
| 06 | cat-screaming-white | [no text] | scream | frustration, hype scream (both read) |
| 09 | cats-hugging-screaming | [no text] | clinging, panic | two things going wrong at once |
| 12 | hamster-cross-scared | [no text] | praying, scared | hoping it works, fear |
| 15 | cat-hand-mouth-hirshe-ne-bude | хуже вже не буде блять 🔞 | doom, resigned | "it can't get worse"… it will |
| 43 | pavement-figure-bliashcho-kuda | Бля шо куда 🔞 | lost, confused | too many options, which way |
| 54 | zelensky-khto-ia | хто я? | identity crisis | "who am I even", role confusion |
| 21 | four-faces-mustache-smile | [no text] | cursed smile, escalating | forced smile through nonsense |
| 45 | doll-angry-face | [no text] | disgust | gross/bad take, strong "no" |
| 13 | cat-paw-stop | [no text] | hand up, "stop" | "no", talk to the hand |
| 11 | sunglasses-double-middle-finger | [no text] | defiant, cool | sassy "no" 🔞 (gesture) |

### Quiet, smug, deadpan, hush
| # | file | caption | feeling | use when… |
|---|---|---|---|---|
| 01 | tsyt-seagull-shush | ЦИТЬ | "shh" | she's about to say something not-to-be-said, shut up |
| 37 | tsyt-seagull-shush-b | ЦИТЬ | same, 320 px | spare of 01 |
| 50 | dog-smug-side-look | [no text] | guilty smirk | "I definitely did it", sneaky |
| 51 | shrek-side-look | [no text] | knowing smirk | "you know what I mean" |
| 35 | hamster-sunglasses | [no text] | deal-with-it cool | after a win |
| 10 | pu-pu-pu-dog-smile | пу пу пу | nervous grin | awkward silence, "uhh" |
| 05 | pu-pu-pu-rat | пу-пу-пу... | stalling | stalling for time |
| 52 | marmots-two | [no text] | gossip, "can you believe" | drama, telling secrets |
| 53 | moomin-knife | [no text] | calm menace | quietly planning revenge/hard cut |
| 60 | charlie-day-conspiracy-board | [no text] | spiralling | over-explaining, connecting dots, anxious planning |

### Self-deprecating, mood, sad
| # | file | caption | feeling | use when… |
|---|---|---|---|---|
| 58 | cat-ia-debilna-debilka | я дебільна дебілка | self-roast | she admits a dumb mistake (female form: hers) |
| 19 | ne-kepkujte-black-cat-cap | не кепкуйте з мене | wounded | "don't make fun of me" |
| 31 | dark-kermit-smoking-ot-by-zaraz-v-durku | от би зараз в дурку | burnout | exhaustion, "I want out" |
| 49 | spravka-vavka | СПРАВКА шо в голові вавка | joke note | "I have a note: my head's not okay" |
| 44 | goat-ni-be-ni-me | Я бачу ти ні бе ні ме | clueless | someone has no idea, not understanding |
| 41 | fox-dont-die-today | ✨don't die today✨ | unhinged hope | surviving the week (English text, works in EN reels) |
| 16 | wet-dog-windblown | [no text] | battered | "I went through it", rough week |
| 39 | woman-batia-ia-staraius | батя, я стараюсь | trying hard | effort not noticed |

### Wholesome / sign-off
| # | file | caption | feeling | use when… |
|---|---|---|---|---|
| 47 | diakuiu-za-uvagu-end-card | Дякую за увагу! якщо ще є питання то загуглітʼ | deadpan sign-off | **last beat only**: her "thanks for watching" gag; don't stack with her CTA |
| 55 | squirrel-coffee-dobryj-ranok | ДОБРИЙ РАНОК ВСІМ ахаха бля яке нахуй в сім мені на восьму 🔞 | morning rage | morning/early-start content |
| 17 | nybryshy-cat-towel-hat | Нибриши | gentle chaos | "don't touch me" tone, cozy |
| 18 | nybryshu-cat-towel-hat-mirror | Нибришу | pair of 17 | use 17 → 18 as a two-frame exchange |
| 04 | machyny-ne-machyny-fence | МАШИНИ НЕ МАШИНИ СТАВИТИ НЕ СТАВИТИ | contradictory instructions | confusing client brief, "do it / don't do it" |

## Quick picker by moment

- **Client asks for more** → 28 (давайте), 63, 43
- **Missed deadline** → 42, 27, 26, 23
- **I made a mistake** → 58, 33, 57, 56
- **Tool/AI did something dumb** → 08, 57, 48, 46, 61
- **Big result/number** → 30, 14, 35
- **Burnout / exhausted** → 31, 49, 16, 54
- **Smug / knowing** → 51, 50, 01
- **Awkward** → 07, 21, 10, 05
- **Ending gag** → 47, 59 (never after the CTA)

## Open items for Ruta

- Several captions are Ukrainian-only; none are in English except 41. If her English account
  needs memes, give me a second folder or a few caption-free picks and I'll tag them.
- Nothing here is licensed or credited; they're reaction images from the internet. Fine for
  reels, but say so if any should never be used (faces of real people: 07 Cillian Murphy,
  54 Zelensky, 39).
