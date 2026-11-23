# Chibi Ruta: character prompt kit

Use this to generate any new pose or emotion of the chibi character for the explainer reels. Reference images that match this description: `chibi-ref-single.png` (the approved look), `chibi-ref-sheet.png` (core poses), `chibi-ref-over-the-top.png` (exaggerated emotions).

## Model
- OpenRouter, model `google/gemini-3.1-flash-image` (Nano Banana 2). About $0.07 per image.
- Do NOT use Seedream for this character: it adds cleavage, pink hands and wrong earrings.
- Do NOT use Higgsfield.
- If the tool accepts reference images, also pass `chibi-ref-single.png` as the character reference.

## How to build a prompt
Always: **FORMAT** + **STYLE** + **CHARACTER** + **POSE**.
Copy FORMAT, STYLE and CHARACTER word for word. Only the POSE part changes.

### FORMAT (one pose, for the video)
Vertical portrait image (2:3). Single character illustration, centred, plain pure white background. No sticker outline, no white border around the character, no cutout edge, no text, no labels, no speech bubbles. Framed from the top of the head down to the knees.

### FORMAT (a sheet of several poses)
Character expression sheet, landscape, exactly [N] poses of the SAME character side by side on a plain pure white background. No sticker outline, no border, no text, no labels. Each pose framed from the top of the head down to the knees, same scale and same height.

### STYLE
Art style: bright, cute modern anime art, polished kawaii mascot. Big sparkly round anime eyes with large white highlights and a soft gradient inside the iris, long lashes, vivid clean colours, crisp dark-brown lineart, soft glossy cel shading, shiny highlights on the hair. Classic exaggerated anime comedy expressions.

### CHARACTER
Young woman in her twenties, slightly chibi (head a bit oversized, simple stylised body). Hair: dark chocolate-brown fluffy short bob, soft messy waves, face-framing pieces, centre part, ends at the jaw, tucked behind the ears so both earlobes are visible. Eyes: dark green irises. Soft brown eyeliner, full dark-brown brows, muted berry lips, a little blush only on the cheeks. Earrings: on each earlobe only, two small thin silver hoops side by side in two separate piercings, one slightly bigger at the bottom of the lobe and one slightly smaller just above it; the hoops do not touch or link; no other piercings anywhere on the ear. Hands and arms are the same fair skin colour as the face. Nails: plain glossy dark burgundy. Outfit: white sleeveless top with a high round crew neckline; light-blue straight jeans.

### POSE
One line describing the face, the hands and any prop. Default to OVER THE TOP: every emotion is exaggerated anime-comedy style, because the reels live on attention.

## Pose library (approved)
Core:
1. **neutral**: standing, friendly smile, one hand waving.
2. **typing**: typing on a silver laptop held at hip height, focused.
3. **frustrated**: both hands on her head, eyes squeezed shut, pout.
4. **phone**: holding a smartphone in both hands, looking down at it, slightly worried.
5. **coffee**: happy and relaxed, eyes closed, holding a plain white ceramic mug with a handle filled with black coffee.
6. **thinking**: index finger on her chin, eyes looking up.

Over the top (favourite style, use these first):
7. **ecstatic**: huge open-mouth grin, eyes closed into happy arcs, both fists raised in the air, little sparkles around her.
8. **waterworks**: wailing with mouth wide open, two big streams of tears gushing out of her eyes like fountains, small puddle-splashes of tears, hands clenched near her face.
9. **furious**: anime rage, red angry face, sharp narrowed eyes, gritted teeth, a cross-shaped anger vein mark on her forehead, small puffs of steam from her head, fists clenched and shaking.

Ready-to-use extras, in the same over-the-top spirit:
10. **shocked**: jaw dropped wide open, eyes turned into tiny white dots, hands on her cheeks, a few sweat drops flying.
11. **confused**: head tilted, one eyebrow up, a big question mark floating above her head, finger scratching her head.
12. **exhausted**: slumped shoulders, half-closed eyes with dark circles, a ghost-like puff of soul leaving her mouth.
13. **panicked**: eyes as spinning swirls, mouth in a wobbly zigzag, hands flailing, big sweat drops.
14. **bored**: chin resting on her hand, flat half-lidded eyes, a tiny "zzz" puff (drawn as a symbol, not text).
15. **smug / proud**: hands on her hips, eyes closed, confident grin, a small sparkle next to her head.
16. **sad**: small frown, glossy eyes with one tear, a little dark rain cloud above her head.

## Rules
1. One emotion or action per image. Describe the face, the hands and the prop only.
2. Never write "cherry" for the nails (models draw real cherries). Write "dark burgundy".
3. Never write "child" or "little girl". Keep "young woman in her twenties".
4. Never write "no pink" or other negative colour words; naming a colour pulls it in.
5. Check every result: dark green eyes, two separate hoops per lobe, no extra piercings, knee-up crop, no outline, no text. Regenerate if any fails.
6. After generating: remove the white background to a transparent PNG, crop at the knee, save as `chibi/<pose-name>.png`.
