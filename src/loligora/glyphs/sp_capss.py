"""Capital sharp s (U+1E9E): flat stem and top bar, a straight diagonal that runs from
the bar's right end down-left into a round lower bowl (superellipse, as the lower half
of a 3/B), closing back to a terminal near the stem. ONE contour: the diagonal's two
straight edges end exactly on the bowl's outer and inner curves (intersections found
per master), and the bar turns into the diagonal in a single sharp miter. Drawn
differently from the lowercase ß on purpose."""
import math

from .. import params as P
from ..fig_parts import _angle, _geom, _run, ebox, tangent_node
from ..superellipse import _node, _segment
from ..uc_params import sb as SB
from ..uc_parts import dw

NAME = "Germandbls"
UNI = 0x1E9E
K = 9                                            # cubic pieces per bowl arc
D = math.radians


def _bowl(m, box, tx, ty, ycut, th_o, th_i):
    """Node lists (outer, inner) of the bowl from the horizontal terminal cut at ycut
    ccw over the bottom and the right to the angles th_o (outer) / th_i (inner)."""
    x0, y0, x1, y1 = box
    ins = (x0 + tx / m.round_w, y0 + ty, x1 - tx / m.round_w, y1 - ty)
    nn = m.n(P.N_LETTER)
    res = []
    for bx, th in ((box, th_o), (ins, th_i)):
        cx, cy, a, b = _geom(m, bx)
        t0 = _angle(m, ('y', ycut, 215), cy, b, nn)
        res.append(_run(t0, D(th), K, cx, cy, a, b, nn, m.s))
    return res


def draw(m):
    m = m.origin(360)
    st, h, sb = m.stem_uc, m.h_uc, SB(m, "STR")
    tx, ty = st * m.pick(1, 1, 0.64), h * m.pick(1, 1, 0.68)
    R = sb + m.pick(650, 670, 720)               # right end of the bar (apex of the miter)
    xl = sb + st + m.pick(26, 30, 24)            # left extreme of the bowl
    top = 720.0
    ytop = m.pick(410, 410, 450)                 # top of the bowl
    ycut = m.pick(100, 110, 120)                 # height of the terminal cut
    box = ebox(m, xl, -P.OVERSHOOT, R - m.pick(70, 70, 10), ytop)
    # left edge B: from the bar's top toward the inner curve at angle ai; edge A = B
    # shifted right by wd, ending on the outer curve (intersection found by bisection)
    nn = m.n(P.N_LETTER)
    ai = 360 + m.pick(136, 136, 136)
    ins = (box[0] + tx / m.round_w, box[1] + ty, box[2] - tx / m.round_w, box[3] - ty)
    qi = _node(D(ai), *_geom(m, ins), nn, m.s)[0]
    C = m.sh(R, top)
    wd = st * 1.4
    for _ in range(30):
        dx, dy = qi[0] - (C[0] - wd), qi[1] - top
        wd = dw(m, abs(dx), abs(dy)) * m.pick(0.95, 0.95, 0.82)
    B0 = (C[0] - wd, C[1])
    cross = lambda u, v: u[0] * v[1] - u[1] * v[0]
    th_o = 360 + tangent_node(m, box, tx, ty, False,
                              lambda p, t: cross((dx, dy), (p[0] - C[0], p[1] - C[1])), lo=60, hi=200)
    out, inn = _bowl(m, box, tx, ty, ycut, th_o, ai)
    yi = top - h                                    # underside of the bar
    I1 = (B0[0] + dx * (yi - top) / dy, yi)
    S = [m.sh(sb, 0), m.sh(sb + st, 0), m.sh(sb + st, yi), m.sh(sb, top)]
    c = [(S[0], S[1]), (S[1], S[2]), (S[2], I1), (I1, inn[-1][0])]
    for i in range(K, 0, -1):
        (p1, t1), (p0, t0) = inn[i], inn[i - 1]
        c.append(_segment(p1, (-t1[0], -t1[1]), p0, (-t0[0], -t0[1])))
    c.append((inn[0][0], out[0][0]))
    c += [_segment(*out[i], *out[i + 1]) for i in range(K)]
    r = m.pick(150, 180, 200)                       # top-left shoulder (one continuous stroke)
    q0, q1 = m.sh(sb, top - r), m.sh(sb + r, top)
    tv = m.sh(0, -1)[0] - m.sh(0, 0)[0], -1.0
    c += [(out[-1][0], C), (C, q1), _segment(q1, (-1, 0), q0, tv), (q0, S[0])]
    return R + SB(m, "RND"), [c]
