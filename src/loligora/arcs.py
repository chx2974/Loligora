"""Fixed-topology arcs of superellipses (shared by capitals and lowercase).

Why: cutting a finished superellipse contour at a height and keeping "the
segments between the crossings" makes the point count depend on which segment
the crossing falls in, which differs between masters. Here every arc is
instead built from POLAR ANGLES: the caller gives angle bounds and the number
of uniform segments per interval, so the topology is fixed by the call, never
by the geometry. Angles are those of the unit superellipse
(x, y) = r(th) (cos th, sin th); the shear (slant) does not change y, so a
horizontal cut at height y is the angle `ang_y((y - cy) / b, n)`.

Angle map: 0 right, pi/2 top, pi left, 3pi/2 bottom; the extreme nodes of a
slanted ring sit at +tr (see superellipse._extreme_angle).
"""
import math

from . import params as P
from .superellipse import _extreme_angle, _node, _segment, _unit, reverse

PI = math.pi


def theta_at(v, n):
    """Polar angle in (0, pi) where the unit superellipse has x = v (|v|<1)."""
    v = max(-0.985, min(0.985, v))
    lo, hi = 0.0, PI
    for _ in range(60):
        mid = (lo + hi) / 2
        if _unit(mid, n)[0] > v:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def theta_at_y(v, n):
    """Polar angle in (0, pi/2) where the unit superellipse has y = v."""
    lo, hi = 0.0, PI / 2
    for _ in range(60):
        mid = (lo + hi) / 2
        if _unit(mid, n)[1] < v:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def ang_y(v, n):
    """Signed version of theta_at_y (v may be negative): angle on the right side."""
    return math.copysign(theta_at_y(abs(v), n), v)


def path_at(fx, fy, a, b, en, s, bounds, ks):
    """Open cubic path along a superellipse (final centre fx, fy, exponent en,
    slant s) between the polar-angle `bounds`, ks[i] uniform segments in
    interval i. Same segment count whatever the numbers."""
    ang = []
    for i, k in enumerate(ks):
        ang += [bounds[i] + (bounds[i + 1] - bounds[i]) * j / k for j in range(k)]
    ang.append(bounds[-1])
    nodes = [_node(t, fx, fy, a, b, en, s) for t in ang]
    return [_segment(*nodes[i], *nodes[i + 1]) for i in range(len(nodes) - 1)]


def path(m, cx, cy, a, b, n, bounds, ks):
    """`path_at` with the centre given in upright design space and the master's
    exponent / slant."""
    fx, fy = m.sh(cx, cy)
    return path_at(fx, fy, a, b, m.n(n), m.s, bounds, ks)


def band(o, i):
    """Close two open paths (outer ccw, counter ccw) into one band contour:
    outer, cross to the counter's end, counter reversed, cross back."""
    return o + [(o[-1][3], i[-1][3])] + reverse(i) + [(i[0][0], o[0][0])]


def cring(m, box, tx, ty, y_top, y_bot, over=True, n=P.N_LETTER, kappa=0.5,
          optical=True):
    """C-shaped open ring (gap on the right, horizontal terminal cuts at y_top
    and y_bot; y_bot None = a fixed angle) with the same segment count in every
    master. box = upright (x0, y0, x1, y1) before overshoot; over=True adds the
    overshoot both ends, False adds none; optical=False skips the italic
    optical width factor."""
    x0, y0, x1, y1 = box
    if over:
        y1 += P.OVERSHOOT
        if over is True:
            y0 -= P.OVERSHOOT
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    a, b = (x1 - x0) / 2 * (m.round_w if optical else 1.0), (y1 - y0) / 2
    en = m.n(n)
    fx, fy = m.sh(cx, cy)
    arcs = []
    for aa, bb in ((a, b), (a - tx, b - ty)):
        pt = ang_y((y_top - cy) / bb, en)
        pb = ang_y((cy - y_bot) / bb, en) if y_bot is not None else PI / 2 - kappa
        tr = _extreme_angle(aa, bb, en, m.s)
        arcs.append(path_at(fx, fy, aa, bb, en, m.s,
                            [pt, PI / 2, PI + tr, 1.5 * PI, 2 * PI - pb], (2, 4, 4, 2)))
    return band(*arcs)


def rot180(contours, adv, ymid):
    """Rotate finished contours by 180 degrees about (adv/2, ymid). Keeps
    orientation and the slant direction of stems."""
    f = lambda p: (adv - p[0], 2 * ymid - p[1])
    return [[tuple(f(p) for p in seg) for seg in c] for c in contours]


def shift(contours, dx):
    """Translate finished contours horizontally (left side bearing)."""
    return [[tuple((x + dx, y) for x, y in seg) for seg in c] for c in contours]


def snap(contour):
    """Make every segment start exactly where the previous one ends."""
    out = []
    for seg in contour:
        seg = tuple(seg)
        if out:
            seg = (out[-1][-1],) + seg[1:]
        out.append(seg)
    first = out[0]
    out[-1] = out[-1][:-1] + (first[0],)
    return out
