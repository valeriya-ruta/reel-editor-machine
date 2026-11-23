# -*- coding: utf-8 -*-
"""Continuous-curvature corners as a CSS clip-path.

Plain `border-radius` bolts a quarter-circle onto a straight edge, and the
break where they meet is the single biggest tell that a shape was drawn in
2013. Apple's corners ease into the curve instead. This is Figma's corner
smoothing, which is the same construction: the arc is shortened and the
remaining sweep is carried by a cubic on each side.

`smoothing` 0 is a plain rounded rect, 0.6 is Figma's "60%" and what we use.

usage:  path(w, h, radius, smoothing) -> "M ... Z" for clip-path: path('...')
"""
import math


def _corner(r, s):
    """Figma's corner-smoothing construction for one corner."""
    arc = 90.0 * (1.0 - s)
    arc_len = math.sin(math.radians(arc / 2.0)) * r * math.sqrt(2.0)
    alpha = (90.0 - arc) / 2.0
    beta = 45.0 * s
    c = r * math.tan(math.radians(alpha / 2.0))
    d = c * math.tan(math.radians(beta))
    p = (1.0 + s) * r
    b = (p - arc_len - c - d) / 3.0
    a = 2.0 * b
    return a, b, c, d, p, arc_len


def path(w, h, r, s=0.6):
    """Clip-path geometry for a w x h box with radius r at smoothing s."""
    r = min(r, min(w, h) / 2.0)
    a, b, c, d, p, L = _corner(r, s)
    p = min(p, min(w, h) / 2.0)

    def f(x):
        return ("%.3f" % x).rstrip("0").rstrip(".")

    out = ["M %s 0" % f(w - p)]
    # top-right
    out.append("c %s 0 %s 0 %s %s" % (f(a), f(a + b), f(a + b + c), f(d)))
    out.append("a %s %s 0 0 1 %s %s" % (f(r), f(r), f(L), f(L)))
    out.append("c %s %s %s %s %s %s" % (f(d), f(c), f(d), f(b + c), f(d), f(a + b + c)))
    out.append("L %s %s" % (f(w), f(h - p)))
    # bottom-right
    out.append("c 0 %s 0 %s %s %s" % (f(a), f(a + b), f(-d), f(a + b + c)))
    out.append("a %s %s 0 0 1 %s %s" % (f(r), f(r), f(-L), f(L)))
    out.append("c %s %s %s %s %s %s" % (f(-c), f(d), f(-(b + c)), f(d), f(-(a + b + c)), f(d)))
    out.append("L %s %s" % (f(p), f(h)))
    # bottom-left
    out.append("c %s 0 %s 0 %s %s" % (f(-a), f(-(a + b)), f(-(a + b + c)), f(-d)))
    out.append("a %s %s 0 0 1 %s %s" % (f(r), f(r), f(-L), f(-L)))
    out.append("c %s %s %s %s %s %s" % (f(-d), f(-c), f(-d), f(-(b + c)), f(-d), f(-(a + b + c))))
    out.append("L 0 %s" % f(p))
    # top-left
    out.append("c 0 %s 0 %s %s %s" % (f(-a), f(-(a + b)), f(d), f(-(a + b + c))))
    out.append("a %s %s 0 0 1 %s %s" % (f(r), f(r), f(L), f(-L)))
    out.append("c %s %s %s %s %s %s" % (f(c), f(-d), f(b + c), f(-d), f(a + b + c), f(-d)))
    out.append("Z")
    return " ".join(out)


def clip(w, h, r, s=0.6):
    return "clip-path: path('%s');" % path(w, h, r, s)


if __name__ == "__main__":
    print(path(400, 240, 48))
