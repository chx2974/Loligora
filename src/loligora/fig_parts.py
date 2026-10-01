"""Figure building blocks with fixed topology (own arcs, no cuts.py).

All boxes are UPRIGHT design boxes of the *effective* extent (`ebox` undoes the
optical width factor of italic rounds). Polar angles are in degrees, counter-
clockwise, unwrapped (end > start). An arc end is either
    ('a', deg)            radial cut at that polar angle, or
    ('y', y, hint_deg)    horizontal cut at height y, solved near the hint.
`band` draws the outline of a stroke of an outer/inner superellipse pair
between two ends: exactly 2k+2 segments whatever the master.
"""
import math

from . import params as P
from .rounds import oval
from .strokes import shpoly
from .superellipse import _node, _segment, _unit, reverse

D = math.radians
MID = P.CAP / 2


def ebox(m, x0, y0, x1, y1):
    """Box whose rounds have effective extent x0..x1 (italic width factor)."""
    c, h = (x0 + x1) / 2, (x1 - x0) / 2 / m.round_w
    return (c - h, y0, c + h, y1)


def ring(m, box, tx, ty, n=P.N_LETTER, box_in=None):
    """Closed ring: [outer ccw, counter cw]. Boxes include any overshoot."""
    x0, y0, x1, y1 = box
    ins = box_in or (x0 + tx / m.round_w, y0 + ty, x1 - tx / m.round_w, y1 - ty)
    return [oval(m, box, n, over=False), reverse(oval(m, ins, n, over=False))]


def _geom(m, box):
    x0, y0, x1, y1 = box
    fx, fy = m.sh((x0 + x1) / 2, (y0 + y1) / 2)
    return fx, fy, (x1 - x0) / 2 * m.round_w, (y1 - y0) / 2


def _solve_y(y, cy, b, n, hint):
    target = (y - cy) / b
    f = lambda th: _unit(th, n)[1] - target
    lo, steps, best = hint - math.pi / 2, 180, None
    prev = f(lo)
    for i in range(1, steps + 1):
        th = lo + math.pi * i / steps
        v = f(th)
        if prev * v <= 0:
            a, c = th - math.pi / steps, th
            for _ in range(50):
                mid = (a + c) / 2
                if f(a) * f(mid) <= 0:
                    c = mid
                else:
                    a = mid
            r = (a + c) / 2
            if best is None or abs(r - hint) < abs(best - hint):
                best = r
        prev = v
    return best if best is not None else hint


def _angle(m, end, cy, b, n):
    if end[0] == 'a':
        return D(end[1])
    return _solve_y(end[1], cy, b, n, D(end[2]))


def _run(th0, th1, k, cx, cy, a, b, n, s):
    """k+1 nodes (point, unit tangent) between two polar angles."""
    return [_node(th0 + (th1 - th0) * i / k, cx, cy, a, b, n, s) for i in range(k + 1)]


def tangent_node(m, box, tx, ty, inner, cond, n=P.N_LETTER, lo=-90.0, hi=0.0):
    """Polar angle (deg) in [lo, hi] of the outer (or inner) ellipse of a band
    where cond(point, tangent) changes sign (bisection after a scan)."""
    x0, y0, x1, y1 = box
    ins = (x0 + tx / m.round_w, y0 + ty, x1 - tx / m.round_w, y1 - ty)
    nn = m.n(n)
    cx, cy, a, b = _geom(m, ins if inner else box)
    f = lambda deg: cond(*_node(D(deg), cx, cy, a, b, nn, m.s))
    N = 360
    prev = f(lo)
    for i in range(1, N + 1):
        d1 = lo + (hi - lo) * i / N
        v = f(d1)
        if prev * v <= 0:
            a0, a1 = d1 - (hi - lo) / N, d1
            for _ in range(60):
                mid = (a0 + a1) / 2
                if f(a0) * f(mid) <= 0:
                    a1 = mid
                else:
                    a0 = mid
            return (a0 + a1) / 2
        prev = v
    raise ValueError("no tangent node")


def band(m, box, tx, ty, e0, e1, k, n=P.N_LETTER, box_in=None, info=False, e0i=None):
    """Stroke between outer/inner superellipses from end e0 to e1 (ccw).
    e0i: optional separate start end for the inner curve."""
    x0, y0, x1, y1 = box
    ins = box_in or (x0 + tx / m.round_w, y0 + ty, x1 - tx / m.round_w, y1 - ty)
    nn = m.n(n)
    fx, fy, a, b = _geom(m, box)
    gx, gy, c, d = _geom(m, ins)
    out = _run(_angle(m, e0, fy, b, nn), _angle(m, e1, fy, b, nn), k, fx, fy, a, b, nn, m.s)
    inn = _run(_angle(m, e0i or e0, gy, d, nn), _angle(m, e1, gy, d, nn), k, gx, gy, c, d, nn, m.s)
    segs = [_segment(*out[i], *out[i + 1]) for i in range(k)]
    segs.append((out[-1][0], inn[-1][0]))
    for i in range(k, 0, -1):
        (p1, t1), (p0, t0) = inn[i], inn[i - 1]
        segs.append(_segment(p1, (-t1[0], -t1[1]), p0, (-t0[0], -t0[1])))
    segs.append((inn[0][0], out[0][0]))
    return (segs, out, inn) if info else segs


def rot180(contours, cx=P.DIGIT_WIDTH / 2, cy=MID):
    f = lambda p: (2 * cx - p[0], 2 * cy - p[1])
    return [[tuple(f(p) for p in seg) for seg in c] for c in contours]


def cpoly(m, segs):
    """Contour from upright-design segments: ('L', p0, p1) or ('C', p0, c1, c2, p1)."""
    return [tuple(m.sh(*p) for p in s[1:]) for s in segs]


def tri(m, pts):
    return shpoly(m, pts)


def ccw(contour):
    """Return the contour reversed if it winds clockwise (line-only polygons)."""
    pts = [s[0] for s in contour]
    area = sum(pts[i][0] * pts[(i + 1) % len(pts)][1] - pts[(i + 1) % len(pts)][0] * pts[i][1]
               for i in range(len(pts)))
    return contour if area > 0 else reverse(contour)
