"""Lowercase building blocks: arches and bowls that leave a stem with a notch.

The outer curve of an arch/bowl is a superellipse whose box is solved so that
it crosses the stem edge at a chosen height (`nd` below the flat stem end):
the small V-notch of the grotesque join. The counter curve is solved the same
way so the stroke is `tj` thick where it meets the stem (thinning at the join).
Both curves are then cut by a (slanted) vertical line buried inside the stem.
All numbers are given in UPRIGHT design space; italic curves are built slanted
by superellipse(s=...), which is exactly the sheared upright curve.
"""
from . import params as P
import math

from .arcs import path, theta_at, theta_at_y
from .superellipse import _extreme_angle, reverse, superellipse


def solve(D, dy, b, n):
    """Half-width a of a superellipse (half-height b) whose far extreme is D
    from the stem edge and which passes the stem edge at height offset dy from
    its centre."""
    r = 1 - min(abs(dy) / b, 0.995) ** n
    return D / (1 + r ** (1 / n))


def se(m, cx, cy, a, b, n=P.N_LETTER):
    fx, fy = m.sh(cx, cy)
    return superellipse(fx, fy, a, b, m.n(n), m.s)


def curves(m, xs, xfar, dirn, top, bot, tx, ty, dy, tj, n=P.N_LETTER):
    """Parameters (cx, a, b) of outer and counter superellipses of a bowl/arch
    whose stem edge is at xs and far outer extreme at xfar (dirn=+1: bowl right
    of the stem, -1: left). Outer spans bot..top, counter is tx thick at the far
    side and ty thick top and bottom. dy = height offset of the outer stem
    crossing from the centre, tj = stroke thickness at the join."""
    en = m.n(n)
    bo = (top - bot) / 2
    ao = solve(abs(xfar - xs), dy, bo, en)
    bi = bo - ty
    xi = xfar - dirn * tx
    ai = solve(abs(xi - xs), dy - tj, bi, en)
    return (xfar - dirn * ao, ao, bo), (xi - dirn * ai, ai, bi)


def _ends(m, par, xl, dirn, n):
    cx, a, _ = par
    return theta_at((xl - cx) / a, m.n(n))


def bowl(m, xs, xfar, dirn, xl, bot, top, tx, ty, nd, tj, n=P.N_LETTER):
    """Ring cut by the line x = xl (inside the stem): the bowl of b d p q."""
    cy = (bot + top) / 2
    op, ip = curves(m, xs, xfar, dirn, top, bot, tx, ty, cy - nd, tj, n)
    h, pi = math.pi / 2, math.pi
    tr = _extreme_angle(op[1], op[2], m.n(n), m.s)
    parts = []
    for par, x in ((op, xl), (ip, xs - 8 * dirn)):
        th = _ends(m, par, x, dirn, n)          # in (0, pi): upper crossing
        if dirn > 0:
            bnd = [2 * pi - th, 3 * h, 4 * h + tr, 5 * h, 2 * pi + th]
        else:
            bnd = [th, h, pi + tr, 3 * h, 2 * pi - th]
        parts.append(path(m, par[0], cy, par[1], par[2], n, bnd, (2, 2, 2, 2)))
    o, i = parts
    return o + [(o[-1][3], i[-1][3])] + reverse(i) + [(i[0][0], o[0][0])]


def arch(m, xs, xr, xl, tx, ty, nd, tj, cy, y_foot, n=None, hcut=None):
    """Upper half of a ring from the stem over the top, then a straight
    (slanted) leg down to y_foot: n h m r. Cut by the line x = xl in the stem."""
    if n is None:
        from . import lc_params
        n = lc_params.N_ARCH
    top = P.XH + P.OVERSHOOT
    op, ip = curves(m, xs, xr, 1, top, 2 * cy - top, tx, ty, P.XH - nd - cy, tj, n)
    parts = []
    for par, x in ((op, xl), (ip, xs - 8)):
        th = _ends(m, par, x, 1, n)
        t0 = 0 if hcut is None else theta_at_y((hcut - cy) / par[2], m.n(n))
        parts.append(path(m, par[0], cy, par[1], par[2], n,
                          [t0, math.pi / 2, th], (4, 3)))
    o, i = parts
    if hcut is not None:      # arm of r: horizontal terminal cut
        return (o + [(o[-1][3], i[-1][3])] + reverse(i) + [(i[0][0], o[0][0])])
    (xo, yo), (xi, yi) = o[0][0], i[0][0]
    leg_o = (xo - m.s * (yo - y_foot), y_foot)
    leg_i = (xi - m.s * (yi - y_foot), y_foot)
    return (o + [(o[-1][3], i[-1][3])] + reverse(i)
            + [(i[0][0], leg_i), (leg_i, leg_o), (leg_o, o[0][0])])
