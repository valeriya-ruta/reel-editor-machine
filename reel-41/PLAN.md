# Reel 41: the long YouTube video, «моя AI-система для контенту»

The first landscape piece, recorded 16:9 for YouTube: 1920×1080 @30, ~6:23 after
v2's cuts. Three raw takes from Drive, all cut here (`work/r41/plate.py` +
`work/r41/edl.py`); there was no script, so the subtitles are Whisper's words
with her spelling restored (`work/r41/subs.py`).

## Her brief

- Open on «shhh», then her filming the reel on the phone. Two seconds in, it
  goes fast-forward and black & white (×6, voice pitch-safe and ducked).
- The take where she shows the Drive upload is b-roll while she explains where
  the videos go. The scrolling clip (…152423) is b-roll for the Sunday analysis.
  Both are flipped back (`hflip`) because the front camera mirrors the screens.
- The 48 s add-on (not checking the videos + scheduling) goes in after the
  editing part.
- Subtitles: simple, sentence by sentence, calm, low but clear of YouTube's bar
  (`captions.ass`, Product Sans Bold 50, 128 px bottom margin).
- v1 notes: no b-roll where she looks at her phone; the strategy part stays on
  her; tighten the pauses; cut the problem section to its beats (ideas + the
  parrot, scripts, editing, a shorter price); keep the wink at the very end.

## How it is built

Not rendered end to end. Each beat is a **window**, a small composition over its
own slice of the plate (`reel-41/w/<name>/`). `work/r41/final.py` overlays the
rendered windows back onto the plate frame-exact and burns the subtitles last.
Beat times were authored on v1; `R()` in `build.py` carries them through the
source take onto the current cut, so a re-cut moves every beat with its words.

## The chain

The recurring object is **the content line**: Ідеї → Сценарій → Зйомка → Монтаж.

| beat | where | what |
|---|---|---|
| month | right | September calendar, every day empty; «0 рілсів», «0 каруселей» |
| expert | left | UGC-креаторка / Блогерка struck out → Експертка; Клієнти, Послуги |
| drop | right | the marketing line climbs, then sinks on «бачити» |
| line1 | left | the content line, Ідеї lit on «ідеї» |
| script | right | the script card: роки досвіду struck → хі-хі-ха-ха, + Гачок |
| daily | right | 1 раз на день → 2 рази на день |
| week | right | seven script cards, Пн–Нд |
| line2 | left | the line again: прописати ✓, зняти ✓, змонтувати lights |
| cost | OVER | editor tile, €€€ on «дорого»; €20–30 a video; reels ×; $500 → $600 → $1000 |
| thirty | left | the line with ×30 on every step; it sags on «і я вмру» |
| twohours | right | 2 год на тиждень |
| claude | right | Claude tile; Telegram struck; all chats in one app |
| notif | right | «Аналіз готовий» notification, haptic |
| ideas | right | numbered list; ticks land on раз, два, три, п'ять, шість, сім |
| strategy | right | the strategy file: Послуги, Вартість, Кейси, Лідмагніти, Курси |
| voice1/2 | right | a voice note; the mess shakes, then folds into… |
| script2 | right | …the script card with Гачок ✓, Заклик до дії ✓ |
| prompter | right | Понеділок; a teleprompter scrolling |
| videos | right | finished reels drop in |
| buffer | right | Buffer → Instagram, «Заплановано» |
| twoaday | right | the week, two reels a day |
| cta | right | «Кнопка під відео» |

Her stats screenshots go in as screenshots (cropped, highlighted, never retyped)
on the month of silence («Custom» period: 10,379 views, −7 followers, the flat
stretch) and on «до і після» (30 days: 67,946 views, +177) once the files are
in Drive.
