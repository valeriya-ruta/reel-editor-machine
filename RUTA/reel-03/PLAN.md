# Reel 3 — «дизайн без Фігми»

Variant B: her cut, graded, no subtitles. This project owns animations **and**
captions. Built against `STYLE.md` — §3 for frame geometry, §4 for the animation
rule, **§5a for the surface system**, which was written during this reel.

| | |
|---|---|
| Source | `VID_20260909_214652_299_bsl.mp4` — 2160×3840 @60, 104.76s |
| Plate | `assets/base.mp4` — 1080×1920 @60, lanczos, crf 17 |
| Mobbin | `assets/mobbin-scroll.mp4` — her capture, 1.0–11.08s at 2.8×, 3.6s |
| Script | `SCRIPTS.md` § 3 (spelling authority) |
| Captions | `work/r3/captions.json` — 271, built by `tools/align.py` |
| Type | Product Sans Black, Ukrainian verified (624 glyphs, 0 missing) |
| Corners | `tools/squircle.py` — Figma corner smoothing 60% as `clip-path` |

**Duration is pinned to 104.6167s = 6277 / 60.** `base.mp4` reports 6282 frames
and a 104.763s container, but everything past frame 6276 decodes black; v1
rendered nine black frames onto the end because of it.

## Captions

Word at a time, UPPERCASE, white, flat, on her reel-2 caption line (y≈1472).
Each holds until the next replaces it, backed off 85 ms. 19 of 271 are two-word
pairs, only where whisper put the words under 100 ms apart. Median 0.26s.

`tools/align.py` binds script spelling to ASR timing and separates whisper's
mangling from her improvisation with a phonetic key plus a brand lexicon —
«Cloud Design» for «Клод Дизайн» scores *lower* than the genuine «коментуєш»
for «коментувала», so the brand names are settled by name before any scoring.

Two calls worth knowing:

- **«ВАЙБКОДИНГ», not «вебкодинг».** Her script writes the latter; three
  separate whisper passes over 5.9s and 8.8s return вайп/вай/вип, never веб.
  Wording follows the delivered audio (STYLE.md §2).
- Her second-person shift is kept: «коментуєш, виправляєш», «потикаєш»,
  «можна відправити». Both spellings of Mobbin normalise to **Mobbin**.

## Beats — 22 over 104.6s

| at | beat | |
|---|---|---|
| 2.3 | Figma mark + a question — the premise being asked | |
| 4.6 | **3** — episode pips, the third lit | |
| 10.4 | the Ruta app itself | |
| 12.9 | a layout assembles, then visibly breaks on «гарний» | |
| 15.6 | the Figma *workspace* filling with artboards | |
| 19.1 | 20 screens, **6 done**, **30%** | **takeover** |
| 24.4 | the colour drains out of the file; then struck and dropped | |
| 33.4 | the Claude tile arrives | |
| 36.3 | **Claude + Figma fuse into one tile** — «дитина» | |
| 42.3 | screens flip through a phone | |
| 45.6 | one node branches into four | |
| 49.4 | a prompt types; three screens come out | |
| 53.1 | comment pins land; a crooked block snaps straight | |
| 55.6 | taps ripple on the phone | |
| 60.2 | design → button → code → **the same design back out** | **full frame** |
| 69.4 | export and screenshot, both struck out | |
| 71.9 | **2** — two slots; skill fills at 75.5, Mobbin at 80.1 | |
| 83.0 | **her Mobbin capture**, framed on a solid ground | **takeover** |
| 87.0 | Mobbin wired into Claude, a packet travelling the wire | |
| 92.6 | one screen, landing right, once | |
| 99.1 | Claude / Codex / Cursor, a ring choosing across them | |
| 101.7 | the episode row returns; a fourth lights | |

One visual event every ~4.5s. No graphic carries a word; the exceptions are the
three numerals and the prompt being typed at 50.5s.

Captions stand down for the two wordless takeovers (19.3–21.9, 36.5–39.4), and
the scrim goes down with them — on a solid ground it reads as a grey smudge.
The b16 code pane is parked under the caption line so her white subtitles keep
contrast through that takeover instead of being suppressed for six seconds.

## Rejected, do not re-propose

- **Frosted glass over her footage.** A full-frame frosted ground blurs her out
  of her own reel. Glass belongs on a solid ground (STYLE.md §5a).
- **Three separate Figma tiles between 15s and 30s.** Her note: too repetitive.
  One mark, reused, with events happening to it.

## Open

- Graphics still cross her face at 61s and 93.3s. Her call was to ship this one
  and fix it next time by dropping them **below** her rather than defending the
  clear band — now STYLE.md §3.
