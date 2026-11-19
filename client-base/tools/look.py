# -*- coding: utf-8 -*-
"""THE CLIENT'S LOOK (design layer) — TEMPLATE. Replace everything here.

This is the only Python file that changes per client. kit.py (the base)
imports these four names and nothing else client-specific:

    TOKENS       css custom properties: palette + font families
    SURFACES     the client's materials (headline, accent, chip, takeover
                 grounds ...), each named after the ref moment it copies
    CAPTION_CSS  how a caption looks (and the #scrim underlay, empty or not)
    LOOK         numbers measured off the client's refs: caption size and
                 height, graphics band, caption mode, phrase length

Fill every value from the client's own example reels (refs/REFERENCES.md),
never from taste. Worked examples: Marina (clients/marina/marina-reel-editor)
and Iryna (clients/iryna/iryna-reel-editor).
"""

TOKENS = """
      --white:  #FFFFFF;
      --ink:    #111111;
      --sans:   Arial, sans-serif;
      --serif:  Georgia, serif;
"""

SURFACES = """
    /* client materials go here (RULES.md / LOOK.md §5a) */
    .shot { position: absolute; display: block; object-fit: cover; }
    .emoji { display: block; width: auto; }
    .tk { position: absolute; inset: 0; }
"""

# %(w)d, %(capTop)d, %(capBottom)d, %(capSize)d are filled in by kit.py.
# Anchor the caption by its bottom (one line sits at cap_y, two grow upward).
CAPTION_CSS = """
    #scrim { position: absolute; left: 0; top: 0; width: 0; height: 0;
             opacity: 0; visibility: hidden; pointer-events: none; }
    .cap { position: absolute; left: 140px; width: 800px; bottom: %(capBottom)dpx;
           text-align: center; color: var(--white); font-family: var(--sans);
           font-size: %(capSize)dpx; font-weight: 600; line-height: 1.1;
           opacity: 0; visibility: hidden; }
    .cap.inv { color: var(--ink); }
"""

LOOK = {
    "cap_y": 1430,          # caption centre y at 1080x1920 (measure it)
    "cap_size": 44,         # px at 1080 wide (measure it)
    "gfx_top": 40, "gfx_bot": 640,
    "caption_mode": "phrase",   # "phrase" | "type" | "word"
    "max_chars": 34, "gap_break": 0.30, "lowercase": True,
    "lang": "uk",
    "lead": 0.10,           # a graphic's first frame this long before its word (her refs)
    "gap_max": 5.50,        # review.py warns on a caption-only rest longer than this (her refs)
    "type_max": 0.35,       # caption_mode "type": longest time one word takes to type on
}
