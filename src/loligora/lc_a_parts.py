"""Copy of the bowl helpers from lc_parts, private to the a (decoupled)."""
from . import params as P
import math

from .arcs import path, path_at, theta_at
from .superellipse import _extreme_angle, _segment, _tangent, _unit, reverse, superellipse


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


def bowl(m, xs, xfar, dirn, xl, bot, top, tx, ty, nd, tj, n=P.N_LETTER, xin=None):
    """Ring cut by the line x = xl (inside the stem): the bowl of b d p q."""
    cy = (bot + top) / 2
    op, ip = curves(m, xs, xfar, dirn, top, bot, tx, ty, cy - nd, tj, n)
    h, pi = math.pi / 2, math.pi
    tr = _extreme_angle(op[1], op[2], m.n(n), m.s)
    parts = []
    for par, x in ((op, xl), (ip, xs - 8 * dirn if xin is None else xin)):
        th = _ends(m, par, x, dirn, n)          # in (0, pi): upper crossing
        if dirn > 0:
            bnd = [2 * pi - th, 3 * h, 4 * h + tr, 5 * h, 2 * pi + th]
        else:
            bnd = [th, h, pi + tr, 3 * h, 2 * pi - th]
        parts.append(path(m, par[0], cy, par[1], par[2], n, bnd, (2, 2, 2, 2)))
    o, i = parts
    return o + [(o[-1][3], i[-1][3])] + reverse(i) + [(i[0][0], o[0][0])]


def _aff(cx, cy, a, b, d, n, t0, t1, k):
    """Quarter of a superellipse whose x axis is the unit vector d (oblique) and
    whose y axis stays vertical: P = C + a*ux*d + b*uy*(0,1). G1 with a line along
    d at theta = pi/2 and with a vertical at theta = pi."""
    nodes = []
    for j in range(k + 1):
        ux, uy = _unit(t0 + (t1 - t0) * j / k, n)
        tx, ty = _tangent(ux, uy, n)
        v = (a * tx * d[0], a * tx * d[1] + b * ty)
        ln = math.hypot(*v)
        nodes.append(((cx + a * ux * d[0], cy + a * ux * d[1] + b * uy),
                      (v[0] / ln, v[1] / ln)))
    return [_segment(*nodes[i], *nodes[i + 1]) for i in range(k)]


def lower_bowl(m, x0, xb, xe_o, xe_i, top, sl, tx, tp, tj, cb, cfg, n=4.0):
    """Lower bowl of the double-storey a: ring open to the stem. Outer and counter
    top edges are straight parallel lines (slope sl), joined to the vertical left
    wall by affine superellipse corners, wall straight, bottom a squared curve
    that meets the stem edge xb at height cb (outer) / cb+tj (counter).
    Contour ccw, built point by point (no shear)."""
    en = m.n(n)
    ca = math.sqrt(1 / (1 + sl * sl))
    d = (ca, ca * sl)
    ov = P.OVERSHOOT
    hc, bc, wall, hci, thin_l = cfg["hc"], cfg["bc"], cfg["wall"], cfg["hci"], cfg["L"]
    tv = tp / ca                                   # vertical thickness of the bar
    yo = lambda x: top + sl * (x - xb)             # outer top line
    yi = lambda x: top - tv + sl * (x - xb)        # counter top line
    xl_i = x0 + tx
    # outer corner and wall
    xt = x0 + hc
    ao = hc / ca
    y_t = yo(xt)
    ly = y_t - bc - hc * sl                        # wall top
    yc = ly - wall                                 # bottom ellipse centre height
    # counter corner
    xti = xl_i + hci
    ai = hci / ca
    y_ti = yi(xti)
    bci = y_ti - hci * sl - yc - wall
    lyi = yc + wall
    segs = []
    # ---- outer, travelling left
    A = (xe_o, yo(xe_o))
    T = (xt, y_t)
    outer = [(A, T)]
    outer += _aff(xt, y_t - bc, ao, bc, d, en, math.pi / 2, math.pi, 2)
    outer += [((x0, ly), (x0, yc))]
    b2 = yc + ov
    a2 = solve(xb - x0, yc - cb, b2, en)
    cx2 = x0 + a2
    th = theta_at((xe_o - cx2) / a2, en)
    outer += path_at(cx2, yc, a2, b2, en, 0.0, [math.pi, 1.5 * math.pi, 2 * math.pi - th], (3, 3))
    # ---- counter, same direction
    b2i = yc - (-ov + tp)
    a2i = solve(xb - xl_i, yc - (cb + tj), b2i, en)
    cx2i = xl_i + a2i
    thi = theta_at((xe_i - cx2i) / a2i, en)
    # thin transition: hermite with equal slopes, lifts the counter top by dlt
    dlt = 0.0                                      # no lift: constant-thickness bar into the stem
    xs = xb - thin_l
    P0 = (xs, yi(xs))
    P3 = (xe_i, yi(xe_i) + dlt)
    hh = (P3[0] - P0[0]) / 3
    thinc = (P0, (P0[0] + hh, P0[1] + hh * sl), (P3[0] - hh, P3[1] - hh * sl), P3)
    inner = [tuple(reversed(thinc)), (P0, (xti, y_ti))]
    inner += _aff(xti, y_ti - bci, ai, bci, d, en, math.pi / 2, math.pi, 2)
    inner += [((xl_i, lyi), (xl_i, yc))]
    inner += path_at(cx2i, yc, a2i, b2i, en, 0.0, [math.pi, 1.5 * math.pi, 2 * math.pi - thi], (3, 3))
    return outer + [(outer[-1][3], inner[-1][3])] + reverse(inner) + [(inner[0][0], outer[0][0])]
