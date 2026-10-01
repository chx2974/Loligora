"""Master-aware round shapes: boxes -> superellipses / rings / open rings.

Boxes are given in upright design coordinates (x0, y0, x1, y1) = the box the
round should occupy BEFORE overshoot; pass `over=True` to add the standard
overshoot top and bottom. In italic the superellipse is constructed slanted
(nodes on the true extrema, softer exponent, optical width factor), see
params.ITAL_* and superellipse.py.
"""
from . import params as P
from .arcs import PI, cring, path_at
from .superellipse import reverse, ring as _ring, superellipse


def _geom(m, box, over):
    x0, y0, x1, y1 = box
    if over:            # True: both ends; 'top': only the top (arches)
        y1 += P.OVERSHOOT
        if over is True:
            y0 -= P.OVERSHOOT
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    a, b = (x1 - x0) / 2 * m.round_w, (y1 - y0) / 2
    fx, fy = m.sh(cx, cy)
    return fx, fy, a, b


def oval(m, box, n=P.N_LETTER, over=True):
    """Solid superellipse (ccw)."""
    fx, fy, a, b = _geom(m, box, over)
    return superellipse(fx, fy, a, b, m.n(n), m.s)


def oval_ring(m, box, tx, ty, n=P.N_LETTER, over=True):
    """[outer ccw, counter cw]; tx/ty = side / top-bottom stroke thickness."""
    fx, fy, a, b = _geom(m, box, over)
    return _ring(fx, fy, a, b, tx, ty, m.n(n), m.s)


def oval_c(m, box, tx, ty, y_top, y_bot, n=P.N_LETTER, over=True):
    """C-shaped open ring, gap on the right between heights y_bot..y_top
    (horizontal terminal cuts). Returns one contour; same point count in every
    master (polar-angle construction, see arcs.py)."""
    return cring(m, box, tx, ty, y_top, y_bot, over=over, n=n)


def oval_arch(m, box, tx, ty, y_foot=0, n=P.N_LETTER, over="top"):
    """Upper half of a ring + slanted right leg down to y_foot (n, h, m ...).
    Cut at the ring's centre height, where the tangent equals the slant, so
    leg and arch join smoothly. Left end is buried in the caller's stem."""
    fx, fy, a, b = _geom(m, box, over)
    en = m.n(n)
    o, i = (path_at(fx, fy, aa, bb, en, m.s, [0, PI / 2, PI], (4, 4))
            for aa, bb in ((a, b), (a - tx, b - ty)))
    (xo, yo), (xi, yi) = o[0][0], i[0][0]
    leg_o = (xo - m.s * (yo - y_foot), y_foot)
    leg_i = (xi - m.s * (yi - y_foot), y_foot)
    return (o + [(o[-1][3], i[-1][3])] + reverse(i)
            + [(i[0][0], leg_i), (leg_i, leg_o), (leg_o, o[0][0])])


__all__ = ["oval", "oval_ring", "oval_c", "oval_arch", "reverse"]
