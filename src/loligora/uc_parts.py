"""Helpers for capital letters: D-bowls, U/J bottoms, S, diagonals.

Design coordinates are UPRIGHT (see strokes.py); m.sh slants them. Rounds are
built directly in slanted space through superellipse(); arcs with free ends use
arcs.path_at (polar angles, fixed topology). bowl_d slices the 16-segment
superellipse: seg 0-3 right->top node, 12-15 bottom->right.
"""
import math

from . import params as P
from .arcs import PI, ang_y, band, path_at, snap
from .strokes import poly, shpoly
from .superellipse import _extreme_angle, reverse, superellipse
from .uc_params import diag_k


def ln(a, b):
    return (a, b)


def geom(m, x0, y0, x1, y1):
    """Final centre + radii of the box (no optical width factor)."""
    fx, fy = m.sh((x0 + x1) / 2, (y0 + y1) / 2)
    return fx, fy, (x1 - x0) / 2, (y1 - y0) / 2


def dw(m, dx, dy, k=None):
    """Horizontal width of a diagonal that runs dx over dy with perpendicular
    thickness k * stem (diagonal optical thinning)."""
    k = diag_k(m) if k is None else k
    return m.stem_uc * k * math.hypot(dx, dy) / abs(dy)


def bowl_d(m, xl, x1, y0, y1, a, tx, ty, n=P.N_LETTER):
    """D-shaped bowl: flat top/bottom strokes from x = xl (bury it in the
    stem) into a half superellipse of horizontal radius a ending at x1."""
    fx, fy, aa, b = geom(m, x1 - 2 * a, y0, x1, y1)
    nn = m.n(n)
    o = superellipse(fx, fy, aa, b, nn, m.s)
    i = superellipse(fx, fy, aa - tx, b - ty, nn, m.s)
    po, pi = o[12:16] + o[0:4], i[12:16] + i[0:4]
    c = ([ln(m.sh(xl, y0), po[0][0])] + po
         + [ln(po[-1][3], m.sh(xl, y1)), ln(m.sh(xl, y1), m.sh(xl, y1 - ty)),
            ln(m.sh(xl, y1 - ty), pi[-1][3])]
         + reverse(pi)
         + [ln(pi[0][0], m.sh(xl, y0 + ty)), ln(m.sh(xl, y0 + ty), m.sh(xl, y0))])
    return snap(c)


def _arcs(m, x0, x1, ybot, tx, ty, b, n, start, ks):
    """Lower-half arcs from polar angle start(bb) (left side) to the right end
    at the ring centre height; start gets the counter/outer radius bb."""
    fx, fy, a, bb = geom(m, x0, ybot, x1, ybot + 2 * b)
    en = m.n(n)
    arcs = []
    for aa, b2 in ((a, bb), (a - tx, bb - ty)):
        arcs.append(path_at(fx, fy, aa, b2, en, m.s,
                            [start(b2, en, fy), 1.5 * PI, 2 * PI], ks))
    return arcs, fy


def u_bottom(m, x0, x1, ybot, tx, ty, b, n=P.N_LETTER):
    """Lower half ring, cut where its tangent equals the slant (bury the ends
    in the stems). Returns (contour, y_cut)."""
    arcs, fy = _arcs(m, x0, x1, ybot, tx, ty, b, n, lambda b2, en, fy: PI, (4, 4))
    return snap(band(*arcs)), fy


def j_hook(m, x0, x1, ybot, tx, ty, b, y_term, n=P.N_LETTER):
    """Hook of J: from the right side at the ring centre, round the bottom, up
    to a horizontal cut at y_term on the left."""
    arcs, fy = _arcs(m, x0, x1, ybot, tx, ty, b, n,
                     lambda b2, en, fy: PI - ang_y((y_term - fy) / b2, en), (4, 4))
    return snap(band(*arcs)), fy


def s_shape(m, x0, x1, ym, tx, ty, yt, n=P.N_LETTER):
    """S from two point-symmetric C-arcs meeting at the spine (centre ym)."""
    ytop, ylow = 720 + P.OVERSHOOT, ym - ty / 2
    fx, fy, a, b = geom(m, x0, ylow, x1, ytop)
    en = m.n(n)
    arcs = []
    for aa, bb in ((a, b), (a - tx, b - ty)):
        tr = _extreme_angle(aa, bb, en, m.s)
        arcs.append(path_at(fx, fy, aa, bb, en, m.s,
                            [ang_y((yt - fy) / bb, en), PI / 2, PI + tr, 1.5 * PI],
                            (2, 4, 4)))
    o, i = arcs
    bo, bi = o[-1][3], i[-1][3]
    cx, cy = (bo[0] + bi[0]) / 2, (bo[1] + bi[1]) / 2

    def rp(p):
        return (2 * cx - p[0], 2 * cy - p[1])

    def refl(path):
        return [tuple(rp(p) for p in seg) for seg in path]

    ro, ri = refl(o), refl(i)
    c = (o + reverse(ri) + [ln(ri[0][0], ro[0][0])] + ro + reverse(i)
         + [ln(i[0][0], o[0][0])])
    return snap(c)


def dpoly(m, top, bot, w):
    """Parallelogram diagonal with horizontal cuts. top/bot = (left edge x, y)."""
    (xa, ya), (xb, yb) = top, bot
    return shpoly(m, [(xb, yb), (xb + w, yb), (xa + w, ya), (xa, ya)])


def buried(m, pts):
    return poly([m.sh(x, y) for x, y in pts])


def v_outline(m, w, ytop, ybot, wd, u):
    """One-piece V (or M's diagonals): outer edges converge on a flat vertex of
    width u at ybot, inner edges (horizontal width wd) meet at the counter
    vertex Q, so u < wd gives a thinned, trapped vertex."""
    cx = w / 2
    sx = (cx - u / 2) / (ytop - ybot)
    q = (cx, ytop - (cx - wd) / sx)
    return buried(m, [(cx - u / 2, ybot), (cx + u / 2, ybot), (w, ytop),
                      (w - wd, ytop), q, (wd, ytop), (0, ytop)])


def a_outline(m, w, wd, u):
    """One-piece A, open at the baseline; apex flat width u (< wd = trap)."""
    cx = w / 2
    sx = (cx - u / 2) / 720
    q = (cx, (cx - wd) / sx)
    return buried(m, [(0, 0), (wd, 0), q, (w - wd, 0), (w, 0),
                      (cx + u / 2, 720), (cx - u / 2, 720)])


def w_outline(m, w, wd, u):
    """One-piece W, four diagonals, flat vertices of width u everywhere."""
    c1 = (w + 2 * wd - u) / 4
    sl = (c1 - u / 2) / 720
    cm = w / 2
    qm = (cm, (cm - c1 - u / 2) / sl)
    y1 = (2 * wd - u) / (2 * sl)
    return buried(m, [(c1 - u / 2, 0), (c1 + u / 2, 0), qm,
                      (w - c1 - u / 2, 0), (w - c1 + u / 2, 0), (w, 720),
                      (w - wd, 720), (w - c1, y1), (w - 2 * c1 + wd, 720),
                      (2 * c1 - wd, 720), (c1, y1), (wd, 720), (0, 720)])
