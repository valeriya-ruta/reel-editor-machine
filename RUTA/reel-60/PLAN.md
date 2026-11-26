# Reel 60 — «Скільки ти насправді платиш за монтаж за місяць?» (монтаж з Клодом)

Batch 2026-11-20 · plate 68.55 s (2057 frames, tools/cut.py + cut-fix.json; the
ТЕСТ CTA is cut, raw 123.4 s → end) · STYLE §00 + her review of reel 61.
`build.py` is the source of truth.

Chain: the one object is **the 5-hour limit bar**. Two equal tasks eat different
token amounts (scheme) → the Claude window: $20, the 5-hour bar, five reels fill
it → which videos (shuffle) → longer videos (shuffle) → the same bar, only three
reels → token optimisation switches on → template straight into the reel
(scheme) → Claude · €100 → «10–15» behind her → the bar is a sliver → her.
Only her numbers: $20, 5 годин, 5 рілсів, 2–3 хв, 5–6 хв, 3 рілси, €100, 10–15.

| time | layer | what |
|---|---|---|
| 0.05–3.2 | BEHIND | «Claude» (cover frame) |
| 3.5–8.8 | — | her own cut / punch-ins |
| 8.85–10.05 | MEME top | 12 hamster praying, after «юсадж це штука непередбачувана» |
| 10.1–12.9 | — | her |
| 13.0–18.6 | HALF 1 | задача = задача; token bars short vs long; «токени» |
| 20.0–25.9 | FULL 1 | Claude window (900×1000 → ~945 px wide, y ≈ 290–1350) rises in 3D, $20 rings, zoom into «Ліміт · 5 годин», 5 reel slots fill, «5 рілсів» |
| 27.1–32.8 | ABOVE shuffle | експертні відео · з суфлера · 2–3 хвилини |
| 33.95–35.15 | MEME top | 35 hamster in sunglasses, after «тоді можна навіть і більше, ніж пʼять» |
| 35.5–38.3 | ABOVE shuffle | 5–6 хвилин · багато вставок · помилки |
| 38.3–41.0 | FULL 2 | same window at the bar, 3 wide slots fill, «3 рілси», zoom out |
| 41.3–46.3 | — | her |
| 46.4–51.2 | ABOVE glass | «Оптимізація токенів» switch flips on «оптимізую» |
| 51.5–58.4 | HALF 2 | шаблон анімації · «з нуля» struck · arrow → рілс on «просто взяти» |
| 61.0–62.5 | ABOVE glass | pill «Claude · €100» (kaching) |
| 63.6–65.6 | BEHIND | «10–15» |
| 66.1–68.1 | ABOVE glass | «Ліміт · 5 годин» bar: a sliver that barely moves; ends on her |

## Memes (BUILD-BRIEF, MEMES.md) — 2 of max 3, slot `top` (above her head, y 40–520; her head top ≈ y 615–645)

- **12 @ 8.85 s** (1.2 s) — «юсадж це штука непередбачувана»: you can't know in advance, you
  just pray it fits (hamster praying, "hoping it works"). Clear stretch: her punch-ins 3.5–13.0.
- **35 @ 33.95 s** (1.2 s) — «тоді можна навіть і більше, ніж пʼять»: the win (deal-with-it
  sunglasses). Replaces the old «більше ніж 5» chip, so the shuffle ends at 32.8 and the next
  list starts 35.5 — clear either side.
- No CTA line remains (ТЕСТ cut), so `g.cta_start = DUR − 2`: nothing in the last 2 s. The
  ending («10–15» behind her, the limit card) had no free stretch for a third, so none.

## Fixes 2026-11-23 (second builder)

- Full screens: the window was 840×600 (frame mostly empty, left edge cropped on the zoom). Now 900×1000,
  wide pose ~88 % of the width, text ≥ 34 px; the push to $20 keeps its top at y 290; the zoom into the
  limit block crosses the sides on purpose.
- Shuffle chips 48 px (as reel-57).
