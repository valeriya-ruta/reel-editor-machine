# -*- coding: utf-8 -*-
"""Catch the things Ruta catches, before she has to.

    python tools/review.py reel-08

Her ask, 2026-09-14: *"can i also ask you to do a pass after youre done and
catch errors i would catch?"* — so this is RULES.md §4a turned into a check
that runs before every render instead of depending on anyone's attention.

Three of her five rules are arithmetic on the timeline and are enforced here.
The other two — is the object nameable, is it a blank plaque — need eyes, and
are printed at the end as a prompt against the contact sheet rather than
silently passed.

  PAINT   a graphic is up inside one of her comedy inserts. Always an error:
          the footage is doing the joke and a card on top competes with her.
  HOLD    a graphic sits unchanged longer than HOLD_MAX. "took too long too",
          at 4.0 s.
  FLASH   a graphic is up for less than FLASH_MIN. "literally one second wtf".
  GAP     dead air longer than GAP_MAX while she is still talking, not counting
          the spans her own editing owns. §4 wants an event every 3-5 s.
  DRIFT   a beat opens more than DRIFT_MAX from the nearest spoken word.
          "waaaay too late … to match the text".
  STACK   two beats up at once — usually a missing clear, which is how reel 7's
          four panes ended up on top of the board.

How it reads the timeline: the generated JS is emitted one block per beat,
each headed by a `/* beat_name */` comment, so a block is the unit. Within a
block every float in [0, DUR] is a moment when *something* changes — which
sidesteps the fact that half the tweens address selectors built at runtime
(`"#g11c" + i`) that no regex over literals would ever see.

Exit code 1 if anything at error level fired, so it can gate a render.
"""
import io
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

HOLD_MAX = 3.60     # how long one graphic may sit unchanged
FLASH_MIN = 0.80    # shorter than this reads as a glitch
GAP_MAX = 5.50      # dead air with her still talking
DRIFT_MAX = 0.45    # how far a beat may open from the nearest spoken word
TAIL = 2.0          # ignore a gap this close to the end


def parse_no_paint(build_path):
    src = io.open(build_path, encoding="utf-8").read()
    m = re.search(r"NO_PAINT\s*=\s*\[(.*?)\]\s*\n", src, re.S)
    if not m:
        return []
    return [(float(a), float(b)) for a, b in
            re.findall(r"\(\s*([\d.]+)\s*,\s*([\d.]+)\s*\)", m.group(1))]


def beat_blocks(html_path):
    """The JS, split into one block per beat by the `/* beat_name */` headers
    build.py already emits."""
    src = io.open(html_path, encoding="utf-8").read()
    js = src[src.index("function build()"):]
    parts = re.split(r"/\*\s*(b\w+)\s*\*/", js)
    out = []
    for i in range(1, len(parts) - 1, 2):
        out.append((parts[i], parts[i + 1]))
    return out


def container_ids(html_path):
    src = io.open(html_path, encoding="utf-8").read()
    ids = set(re.findall(r'class="g(?: full)?"\s+id="([A-Za-z0-9_]+)"', src))
    ids |= set(re.findall(r'id="([A-Za-z0-9_]+)"\s+class="g(?: full)?"', src))
    return ids


def span_of(block, gid, dur):
    """When this block's container is on screen, and every moment inside it at
    which anything changes.

    A container that is never explicitly hidden closes at its own last event:
    that is what an empty `.g` is — reel 7's b15 hides its three children and
    leaves the wrapper up, which renders nothing but would otherwise look like
    a graphic sitting there for 65 seconds."""
    show = hide = None
    for body, t in re.findall(
            r'tl\.(?:set|to)\(\s*"#%s"\s*,\s*(\{.*?\})\s*,\s*([\d.]+)\s*\)' % gid,
            block, re.S):
        t = float(t)
        a = re.search(r"autoAlpha:\s*([\d.]+)", body)
        if not a:
            continue
        if float(a.group(1)) > 0.02:
            show = t if show is None else min(show, t)
        else:
            hide = t if hide is None else max(hide, t)
    if show is None:
        return None
    times = sorted(set(
        float(x) for x in re.findall(r"[,\[(]\s*(\d+\.\d+)\s*[,)\]]", block)
        if 0.0 <= float(x) <= dur))
    inner = [t for t in times if t > show and (hide is None or t < hide)]
    if hide is None or hide <= show:
        hide = inner[-1] if inner else show + 0.4
        inner = [t for t in inner if t < hide]
    return show, hide, inner


def main():
    reel = sys.argv[1] if len(sys.argv) > 1 else "reel-08"
    n = reel.split("-")[-1]
    html = os.path.join(ROOT, reel, "index.html")
    build = os.path.join(ROOT, reel, "build.py")
    caps = json.load(io.open(os.path.join(ROOT, "work", "r" + n,
                                          "captions.json"), encoding="utf-8"))["words"]
    starts = [c["s"] for c in caps]
    last_word = caps[-1]["e"]
    dur = float(re.search(r'data-duration="([\d.]+)"',
                          io.open(html, encoding="utf-8").read()).group(1))

    no_paint = parse_no_paint(build)
    ids = container_ids(html)

    beats = []
    for name, block in beat_blocks(html):
        for gid in sorted(ids):
            if '"#%s"' % gid not in block:
                continue
            sp = span_of(block, gid, dur)
            if sp:
                beats.append((sp[0], sp[1], gid, name, sp[2]))
    beats.sort()

    # A container several beats share — reel 7's board — is a spine, not a
    # graphic: each block only sees the fragment it owns, so the fragments look
    # like flashes. Its continuity is the whole point, so FLASH does not apply.
    from collections import Counter
    spine = set(g for g, c in Counter(g for _, _, g, _, _ in beats).items() if c >= 3)

    errors, warns = [], []

    for a, b, gid, name, inner in beats:
        for na, nb in no_paint:
            if a < nb and b > na:
                errors.append("PAINT  %-9s %6.2f-%6.2f sits on her insert %.2f-%.2f"
                              % (gid, a, b, na, nb))
        marks = [a] + [t for t in inner] + [b]
        for i in range(len(marks) - 1):
            if marks[i + 1] - marks[i] > HOLD_MAX:
                warns.append("HOLD   %-9s unchanged %.2f s  (%6.2f-%6.2f)  %s"
                             % (gid, marks[i + 1] - marks[i], marks[i],
                                marks[i + 1], name))
        if b - a < FLASH_MIN and gid not in spine:
            warns.append("FLASH  %-9s up only %.2f s at %6.2f  %s"
                         % (gid, b - a, a, name))
        near = min(abs(a - s) for s in starts)
        if near > DRIFT_MAX:
            warns.append("DRIFT  %-9s opens %6.2f, %.2f s off the nearest word  %s"
                         % (gid, a, near, name))

    # gaps, ignoring the spans her own editing owns
    merged = []
    for a, b, _, _, _ in beats:
        if merged and a <= merged[-1][1] + 0.01:
            merged[-1][1] = max(merged[-1][1], b)
        else:
            merged.append([a, b])
    prev = 0.0
    for a, b in merged:
        hole = a - prev
        if hole > GAP_MAX and prev < last_word - TAIL:
            hers = sum(min(b2, a) - max(a2, prev)
                       for a2, b2 in no_paint if a2 < a and b2 > prev)
            if hole - hers > GAP_MAX:
                warns.append("GAP    nothing on screen %6.2f-%6.2f  (%.2f s, "
                             "%.2f of it hers)" % (prev, a, hole, hers))
        prev = max(prev, b)

    for i in range(len(beats)):
        for j in range(i + 1, len(beats)):
            a1, b1, g1, n1, _ = beats[i]
            a2, b2, g2, n2, _ = beats[j]
            if a2 < b1 - 0.40 and g1 != g2 and n1 != n2:
                warns.append("STACK  %s and %s both up %6.2f-%6.2f  (%s / %s)"
                             % (g1, g2, a2, min(b1, b2), n1, n2))

    print("REVIEW %s — %d beat spans, %d no-paint zones, %.2f s"
          % (reel, len(beats), len(no_paint), dur))
    print()
    for e in errors:
        print("  x " + e)
    for w in sorted(set(warns)):
        print("  ! " + w)
    if not errors and not warns:
        print("  ok  timeline clean")
    print()
    print("  Eyes still needed on the contact sheet (RULES.md 4a.2, 4a.4):")
    print("    - is every object nameable, or is it a glowing dot?")
    print("    - is anything a blank plaque that should carry a mark?")
    print("    - is any graphic sitting on her face?")
    print("    - do the numbers on screen agree with each other?")
    sys.exit(1 if errors else 0)


main()
