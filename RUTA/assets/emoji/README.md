# Emoji artwork

Apple's set, as PNG. Ruta asked for it by name after reel 5 shipped with a
literal `💩` in the HTML: the composition renders on HeyGen's cloud Chrome,
which has Noto Color Emoji, so a glyph comes out looking like Android no matter
what is installed on her machine. An `<img>` renders identically everywhere.

## Naming

File stem = the short name, lowercase, no colons, `-` for spaces:

    poop.png  fire.png  thinking-face.png  face-with-tears-of-joy.png

`Kit.emoji("poop")` emits `<img class="emoji" src="assets/emoji/poop.png">`.
Size it in the beat's own CSS (`.verdict .emoji { height: 260px; }`), never
with a `font-size`.

## Source

Apple's emoji artwork is Apple's; it is not redistributable, which is why the
PNGs are not committed and this folder ships with only a README. Populate it
from a set on the machine that has one, or from an emoji CDN, at 160px or
better — these get scaled to 260px in a 1080-wide frame and a 72px sprite
falls apart.

Anything dropped in here is picked up by name. Nothing else needs to change.
