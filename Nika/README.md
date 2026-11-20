# Nika — UNLOCK ad reels

**A different person and a different style from the rest of this repo.** Nothing
in the root `STYLE.md`, `tools/glass.py`, `SCRIPTS.md` or the `/reel` skill's
look applies here: no refined glass, no burgundy, no Product Sans, no Ruta
captions.

**Everything for her lives under `Nika/`**: her brief, her reels, her tools
(`Nika/tools/`), her sound kit and her intermediates (`Nika/work/`, footage
gitignored). Nothing of hers goes in the root folders, and nothing here imports
from the root `tools/`. The path is what marks a reel as hers.
Ruta's reels are the `reel-NN/` folders at the root. If a session can't tell
whose reel it is, it asks before doing anything.

## Who and what

- **Nika** works at **UNLOCK** («unlock — your expertise»): a platform where
  experts build and sell mini-courses and digital products. Logo: purple
  padlock mark + black «unlock» wordmark.
- The reels are **ads for the platform**, in Ukrainian, her talking to camera.
- Source footage: the Drive folder `1XBXWPTPEnVrAFoJSXDskVR-qGKxis889`.
  Downloads land in `Nika/work/src/` (gitignored).

## The look (working brief, 2026-11-17)

Her earlier edit (`example.MOV` in the Drive folder) is the reference for what to
keep and what to drop. Verdict: *over-edited, we don't like it in general.*

**Keep**

- **Pink type.** Baby-pink fill (~`#F8B2C6`), a dark raspberry outline
  (~`#9A1040`) and a slight 3D drop. Heavy, rounded sans.
- **The torn-paper plaque.** A ripped scrap of white grid-notebook paper with a
  soft torn edge, sitting under the text.

**Drop**

- Something happening on every line.
- Four type styles in one reel: condensed caps title, handwriting, rounded bold,
  and a plain grey sans.
- Stock 3D emoji icons and a stock man in a hoodie.
- A background swap every few seconds (purple → cream → lavender).
- B-roll of her: laptop in bed, café.

**Instead of B-roll**, show the product: the real UNLOCK UI. It should feel
modern and gen-Z, and it should be clearly about the platform.

- **Like a normal app promo.** Smooth zoom-ins and angled 3D mockups.
- **Clear, not fancy.** One idea per shot and one move per shot. The editing
  should never be the thing you notice.
- **Show the actual platform.** The UI comes from the site,
  `https://unlockexpertise.online/uk`. It draws its product "screenshots" in
  HTML: home, course editor, payments, sales page, analytics, the Telegram
  phone, and the «Оплату отримано» toast. `tools/capture_site.js` clones each one
  onto a blank page and shoots it at 4× as a transparent PNG. The real app can't
  stand in yet: the test account is empty, with no plan and no products
  (2026-11-17).
- **Sound design, as on Ruta's reels:** click on captions, whoosh on cuts, pop
  when a card lands, ka-ching on money. Always under her voice. The kit is
  synthesised by `tools/sfx.py synth` into `Nika/assets/sfx/` (gitignored, so
  run it once per machine), because Ruta's kit is on her laptop only.

## As built (r01 look test)

`r01-test/build.py` is the worked example; copy from it.

- **Text:** Montserrat Black, lowercase except names, 64 px. Pink `#F9B5CA` with
  a raspberry ring outline `#B4195B` and a 3-step drop `#93104A`, all as text
  shadows. It sits on a torn scrap of grid paper: a white blurred fibre layer
  under a grid layer, each with its own seeded ragged `clip-path`. One short
  phrase at a time, centred at y 1262. Each scrap lands with a small tilt and
  is replaced, not faded. Where the stage itself says the words, the captions
  drop.
- **Her:** full frame, a slow push-in on each of her shots (1.0 → 1.04), framed
  a little tighter after each product shot.
- **Stage:** UNLOCK's own white → `#EFEBFF` with two drifting brand glows
  (`#8F31EA`, `#3F58E8`) and a faint 72 px grid, an echo of her paper. It opens
  from her as a rounded rectangle growing out of the centre (0.5 s), and closes
  the same way.
- **Screens:** each one is a card in a 2300 px-perspective scene, at rest at
  rotY −21°, rotX 13°, rotZ 2°. It enters from the right out of depth
  (`expo.out`, 0.62 s), pushes in slowly while it is the shot, and leaves left
  (`power2.in`). There is one screen per thing she names. A cursor clicks the
  real buttons, and the money toast lands with the ka-ching. «все в одному
  місці» pulls back to all of them at once around the dashboard.
- **Logo:** rebuilt in HTML from the site's SVG: the brand gradient
  `#2D43D2 → #8F31EA` tile with the white padlock, and «unlock» in Geist 700.
- **Render:** locally, `npx hyperframes@0.8.33 render <dir> -q high --fps 30`.
  `tools/stills.js` previews stills without a render.

## Reels

| reel | source | length | status |
|---|---|---|---|
| r01 | `IMG_7332.MOV`: one continuous take, 1080×1920 HEVC 30 fps, warm beige wall | 72.2 s | transcribed, beats planned (`r01/PLAN.md`); look test approved; v2 sent for review: 1.2×, end card instead of the comment CTA (`r01/`) |

`IMG_7335.MOV` is the same script already cropped into a circle (720p). It is
not used.
