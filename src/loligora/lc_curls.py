"""Curled stroke ends built from superellipse arcs: tails (down: l t g j) and
hooks (up: a f), with horizontal terminal cuts. Design space is upright; italic
arcs are built slanted (see lc_parts.path). One closed contour each.

side=+1: stem on the left, curl to the right. side=-1: stem on the right.
xo = outer edge of the stem side, xf = far outer extreme of the curl,
st = stem thickness, te = thickness at the terminal, ty = arc thickness,
cy = height of the ring centre (where the stem starts to curve), y_end = height
of the horizontal terminal cut, y_far = end of the straight stem.
"""
import math

from . import params as P
from .arcs import path, theta_at_y
from .superellipse import reverse

PI = math.pi


def _ring(xo, xf, side, st, te):
    xn, xe = xo + side * st, xf - side * te
    return ((xo + xf) / 2, abs(xf - xo) / 2), ((xn + xe) / 2, abs(xe - xn) / 2)


def _stem_end(m, p, cy, y_far):
    return (p[0] + m.s * (y_far - cy), y_far)


def tail(m, side, xo, xf, cy, ybot, y_end, st, te, ty, y_far, n=P.N_LETTER):
    bo = cy - ybot
    bi = bo - ty
    (co, ao), (ci, ai) = _ring(xo, xf, side, st, te)
    en = m.n(n)
    arcs = []
    for c, a, b in ((co, ao, bo), (ci, ai, bi)):
        phi = theta_at_y(abs(y_end - cy) / b, en)
        if side > 0:
            arcs.append(path(m, c, cy, a, b, n, [PI, 1.5 * PI, 2 * PI - phi], (4, 3)))
        else:
            arcs.append(path(m, c, cy, a, b, n, [PI + phi, 1.5 * PI, 2 * PI], (3, 4)))
    o, i = arcs
    if side > 0:
        e0, e1 = o[0][0], i[0][0]
        return (o + [(o[-1][3], i[-1][3])] + reverse(i)
                + [(e1, _stem_end(m, e1, cy, y_far)),
                   (_stem_end(m, e1, cy, y_far), _stem_end(m, e0, cy, y_far)),
                   (_stem_end(m, e0, cy, y_far), e0)])
    e0, e1 = o[-1][3], i[-1][3]
    return (o + [(e0, _stem_end(m, e0, cy, y_far)),
                 (_stem_end(m, e0, cy, y_far), _stem_end(m, e1, cy, y_far)),
                 (_stem_end(m, e1, cy, y_far), e1)] + reverse(i)
            + [(i[0][0], o[0][0])])


def hook(m, side, xo, xf, cy, ytop, y_end, st, te, ty, y_far, n=P.N_LETTER):
    """Upper curl: over the top from the stem to a free horizontal terminal."""
    bo = ytop - cy
    bi = bo - ty
    (co, ao), (ci, ai) = _ring(xo, xf, side, st, te)
    en = m.n(n)
    arcs = []
    for c, a, b in ((co, ao, bo), (ci, ai, bi)):
        phi = theta_at_y((y_end - cy) / b, en)
        if side > 0:
            arcs.append(path(m, c, cy, a, b, n, [phi, PI / 2, PI], (3, 4)))
        else:
            arcs.append(path(m, c, cy, a, b, n, [0, PI / 2, PI - phi], (4, 3)))
    o, i = arcs
    if side > 0:
        e0, e1 = o[-1][3], i[-1][3]
        return (o + [(e0, _stem_end(m, e0, cy, y_far)),
                     (_stem_end(m, e0, cy, y_far), _stem_end(m, e1, cy, y_far)),
                     (_stem_end(m, e1, cy, y_far), e1)] + reverse(i)
                + [(i[0][0], o[0][0])])
    e0, e1 = o[0][0], i[0][0]
    return (o + [(o[-1][3], i[-1][3])] + reverse(i)
            + [(e1, _stem_end(m, e1, cy, y_far)),
               (_stem_end(m, e1, cy, y_far), _stem_end(m, e0, cy, y_far)),
               (_stem_end(m, e0, cy, y_far), e0)])


def dot(m, cx, cy, size, n=4.5):
    """Square-ish dot (high-exponent superellipse)."""
    from .lc_parts import se
    return se(m, cx, cy, size / 2, size / 2, n)
