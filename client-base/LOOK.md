# <CLIENT> — the look (DESIGN LAYER, template)

**Everything design lives here and only here** (plus `tools/look.py` and
`assets/fonts/`): palette, fonts, caption style and size, type tiers, how each
real element is drawn, stroke weights, motion style, timing lead, rhythm, and
where her refs put things. `RULES.md` (the base) has no design in it and
doesn't change per client.

Every line comes from **her own reels** (`refs/REFERENCES.md`) or from what
Ruta / the client said, and names the ref moment it was measured on. If a
value isn't in her reels, it isn't here. This file never loosens a rule in
`RULES.md` (safe area, nothing on her head, real elements, cutting).

Section numbers match `RULES.md`.

---

## 0. The look in one paragraph

## 2b. Captions (`tools/look.py` CAPTION_CSS + LOOK)

```
mode        phrase | type | word          (LOOK["caption_mode"])
font        <family> <weight>, NN px at 1080 wide   (LOOK["cap_size"])
case        lowercase / as said / UPPERCASE         (LOOK["lowercase"])
colour      ... ; inverted on a light takeover: ...
treatment   underlay / outline / shadow / none
chunk       <= NN characters (LOOK["max_chars"]), break on a pause > NN s
position    bottom edge / centre at y = NNNN (LOOK["cap_y"]), inside the safe area
change      hard swap / types on / word by word
```

## 2c. Takeovers (her refs)

- length:
- how they build:
- grounds (`.tk.<name>`):
- half-screen panel ground and content type:

## 3. Where her refs put things (inside RULES.md §3, never against it)

| zone | what goes there | refs |
|---|---|---|

Her plates: chin range at base framing, headroom (measure on the first raw).

## 4. Motion, timing and rhythm (her refs)

- words in graphics: allowed / not (her refs, Ruta's call)
- entrance / exit:
- allowed motions (kit helpers `on`, `off`, `type_on`, `count_up`,
  `slide_in`, `fade_in`):
- banned:
- lead: first frame NN s before the word (LOOK["lead"])
- builds:
- a new graphic every ~N s; graphics on screen NN % of the runtime
- caption-only rests up to NN s (LOOK["gap_max"])
- hook:

## 5. Palette and type

```
name   #HEX   where
```

| tier | size at 1080 wide | what |
|---|---|---|

Fonts: local files in `assets/fonts/` + `fonts.css`.

## 5a. Materials (`tools/look.py` SURFACES)

| class | what | ref moment |
|---|---|---|

How the real elements (RULES.md §4) are drawn in her look:

| element | built as |
|---|---|
| to-do card | |
| struck list | |
| search box | |
| messages | |
| chips | |
| chart card | |
| spreadsheet | |
| viewfinder | |

Line weights (strikes, checkboxes, chart lines):

## 9. How her refs use b-roll and sound
