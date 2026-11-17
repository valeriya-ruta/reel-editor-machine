# Archived — the refined-glass look (reels 12–40)

**Archived 2026-10-28, her call:** *"just archive the old style. take the one
from the reels 50+"* and *"make that one the default"*. Never build in this look
unless she asks for it by name. The default is STYLE.md §00 (Google style +
Excalidraw, `tools/gstyle.py`). This file keeps the old spec so the reels built
in it (`reel-12`…`reel-40`, `style-test/`, `tools/glass.py`) can still be read
and rebuilt.

What is gone with it: the burgundy ground (`.tkg`, light pools, grain), the
burgundy iris takeovers, glass shelves / jelly tiles as the house surface, and a
half screen built as a glass window on a burgundy ground (reel 55 v1 shipped
that way and she rejected it: *"half screen is completely wrong"*, *"the
burgundy bg was eradicated completely"*).

---

## 0. The look — refined glass (locked 2026-09-28)

Her brief: the reels were *"good and smooth"* but visually lacked *"refinement"* —
*"flat and flaticon-ish more than apple-ish"*, with *"pretty basic"* animation.
Same concept, better craft. Her verdict on the test pass: *"this is fucking
amazing. delicious. just YES"*, and *"lock this in"*.

- **Reference build:** `style-test/` — `build.py`, a 16.5 s slice of the
  2026-09-28 script over a still of her. Near her 0–4 s, behind her 4–11 s, over
  her 11–14.5 s, near again 14.5–16.5 s.
- **Library:** `tools/glass.py` — the materials (CSS) and the motion (springs +
  `helpers(tl)`), on top of `kit.py`. Start every beat from it.

**Unchanged, and not up for redesign:** the palette (burgundy, white, baby pink,
black), Product Sans, rounded corners, liquid/frosted glass, the three placements
(above her, behind her via matte, covering her), and the basic captions
(ProductSans Black, white, on the blurred `underlay.png` plaque).

**What refined means — nine rules:**

1. **Glass is built in layers.** Blur + saturation, a faint tint gradient, light
   inside the bottom edge (thickness), a huge soft shadow, and `.edge` — a
   gradient rim bright at two opposite corners and nearly gone along the sides.
   Never a uniform outline. `.shelf` over footage, `.dglass` for white text over
   footage.
2. **One tile family for every mark.** iOS icon radius (22.4%), glyph at 50%,
   three materials: `.clear` (in the room, over footage), `.pearl` (the neutral
   or the hub), `.jelly` (the AI or the hero, burgundy). Marks are **monochrome**
   simple-icons paths from `assets/icons/`, never full-colour brand PNGs — she
   approved this explicitly. No icon exists → a wordmark in the tile (RUTA,
   Windsor's «w.»).
3. **Springs, not stock eases.** `SP` / `POP` / `SOFT` / `FLIP` for transforms.
   Things arrive from depth — blur → sharp, small → full — never by a plain
   fade. A container's contents land ~0.1 s after it. Exits are quicker than
   entrances and ease *in*.
4. **Continuity: plan a reel as a chain, not a list.** No beat fades to nothing
   when the next one can grow out of it. The test's chain: the shelf's frost
   spreads into the room → the Windsor tile becomes the hub → the icon wall
   ripples out of the hub → collapses back into it → the hub opens (iris) into
   the takeover → the report grows out of the hub point → folds into a
   notification as the iris closes onto it. The transitions are where the craft
   shows.
5. **Use all three placements in a reel**: near (a shelf above her head, a
   notification), behind (objects in her room via the matte, the room itself
   gone soft), over (the burgundy takeover).
6. **The takeover ground is deep burgundy** — `.tkg` + three drifting light pools
   (`.aur`) + `.grain` — carrying a white `.sheet`. This overrides §5's old
   "never a dark ground". White and blush grounds stay allowed for a
   deliberately bare "before" state (§2c).
7. **Type ladder in a card**: micro label 24/700 at +0.16em and 42% ink; title
   42/700; sub 26/500 at 46% ink; the big number 176/900 in a burgundy → pink
   gradient. The weight contrast is the point.
8. **Details that sell it**: one `.sheen` sweep when a hero surface lands; square
   ripples (`.sqring`) the shape of the tile that sent them; cables as a glass
   tube with a bright core and a travelling packet; a haptic shake when a
   notification lands; a slow push on the plate (1.0 → 1.045 across the reel).
   Ambient motion is allowed now; looping graphics still are not.
9. **Captions carry on over everything**, the burgundy ground included (white
   on the plaque). Keep a sheet's bottom at y ≤ 1240, clear of the plaque.

**Traps hit building it:**

- `fromTo` renders its *from* state at build time. A ripple starting from
  `autoAlpha: 0.7` sat on screen from frame 0 → `immediateRender: false`
  (`helpers.ripple` does it).
- A dash draw-on whose offset equals the path length leaves a round-cap dot at
  the start → `helpers.drawPrep` offsets by +3.
- Springs front-load motion: a flip on `POP` passes 90° within ~0.1 s, so the
  first face is barely seen. Use `FLIP`, and start the flip on the word that
  names the new face, not on «або».
- **Behind her with the room soft-focused** was proven on a still, where the
  soft room is a clean plate (her inpainted out) blurred 26 px. On moving
  footage, blurring the plate smears her silhouette into a halo around her.
  Build the soft room as blur(plate × (1 − matte)) / blur(1 − matte) per beat
  in ffmpeg, or replace the room with the burgundy ground behind her matte.
  Check it on the first real reel before trusting it.
- Budget: the test ran ~23 heavy elements with a 134-tile wall, because wall
  tiles carry no filter and no backdrop-filter — they sit on the pre-blurred
  room. Keep it that way.
- A synthesised read is ~6 syllables/s; hers is slower. Plan beats against
  phrases, not seconds, and re-time them to the ASR.

---

## 2c. Takeovers

Her four reference reels (`Examples/`) all make the same structural argument,
and it is not about polish: **the graphic owns the frame or it is not there.**
None of them float a card over footage. They alternate — footage with a short
phrase on it, then no footage at all.

What a takeover is, mechanically: a `.g.full` whose first child is an opaque
ground (`.tk.paper` / `.tk.white` / `.tk.blush`), usually with `.gp` graph
paper over it. The plate is gone, so **none of the over-footage rules apply** —
no glow budget, no band discipline, ink type on a light ground, and the
heavy-overlay element ceiling does not bite.

Rules learned building reel 9's five:

- **Bleed off at least two edges.** A takeover composed inside the frame with
  margins reads as a slide, not a takeover. Mark the elements
  `data-layout-allow-overflow` so the layout checker stops flagging them.
- **The ground belongs to the beat that starts first and must outlive every
  other part of the takeover.** Reel 9's paper lived on the wrapper carrying
  the Canva/Slides marks; fading that wrapper when the marks had said their
  piece put her footage back behind the wall for the whole push-in. Fade the
  *children*, keep the ground.
- **Transforms only.** `width`, `height` and `margin` are layout properties:
  the linter rejects them and they snap to integer device pixels mid-tween. A
  typing reveal is `clipPath: inset(...)`; a band that fills the frame sits at
  its *resting* size and scales **up**, so a 26px radius stays 26px instead of
  stretching into a 260px ellipse.
- **Solve push-ins, don't eyeball them.** To bring point `p` to centre `c` at
  scale `k`, the wrapper offset is `c - (c + (p - c)k)`.
- **Use the whole frame when captions are blacked out.** TK4's brandbook first
  sat in the top half with 800px of dead paper under it, because it had been
  laid out around a caption band that was not going to be there.


