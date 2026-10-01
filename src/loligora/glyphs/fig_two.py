from .. import params as P
from ..fig_parts import band, ccw, ebox, tangent_node
from ..strokes import bar, shpoly, poly

NAME, UNI = "two", 0x32
OV = P.OVERSHOOT


def draw(m):
    m = m.origin(P.CAP / 2)
    sb, w, h = m.sb_dg, m.stem_dg, m.h_dg
    L, R = sb, P.DIGIT_WIDTH - sb
    hook = ebox(m, L + m.pick(12, 14, 16), m.pick(300, 300, 320), R - m.pick(6, 10, 10), P.CAP + OV)
    yt = m.pick(575, 580, 560)

    tx, ty = w * m.pick(1, 1, .84), h * m.pick(1, 1, .9)
    # the diagonal's upper-left edge runs from the base's top-left corner and is
    # TANGENT to the hook's inner curve; the lower-right edge is the parallel
    # tangent of the outer curve. Both edges are straight, thickness constant.
    pl = m.sh(L, h)
    cross = lambda u, v: u[0] * v[1] - u[1] * v[0]
    ai = tangent_node(m, hook, tx, ty, True, lambda p, t: cross(t, (pl[0] - p[0], pl[1] - p[1])))
    pin = band(m, hook, tx, ty, ('a', ai), ('y', yt, 165), 9, info=True)[2][0]
    d = (pin[0][0] - pl[0], pin[0][1] - pl[1])
    ao = tangent_node(m, hook, tx, ty, False, lambda p, t: cross(t, d))
    segs, out, inn = band(m, hook, tx, ty, ('a', ao), ('y', yt, 165), 9, info=True, e0i=('a', ai))
    po, pi = out[0][0], inn[0][0]

    def at(a, b, y):                    # point of line a-b at height y
        t = (y - a[1]) / (b[1] - a[1])
        return (a[0] + t * (b[0] - a[0]), y)

    # one contour: diagonal + base. The outer edge runs (on its own line) into
    # the base's top edge, the inner edge into the base's top-left corner.
    xh = at(po, (po[0] - d[0], po[1] - d[1]), h)
    diag = ccw(poly([pi, po, xh, m.sh(R, h), m.sh(R, 0), m.sh(L, 0), m.sh(L, h)]))
    return P.DIGIT_WIDTH, [segs, diag]
