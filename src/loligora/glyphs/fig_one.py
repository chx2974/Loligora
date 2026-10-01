from .. import params as P
from ..fig_parts import cpoly

NAME, UNI = "one", 0x31


def draw(m):
    m = m.origin(360)
    w, cap = m.stem_dg, P.CAP
    sx = P.DIGIT_WIDTH / 2 + 25 - w / 2
    fl = m.pick(165, 175, 155)                 # flag reach
    fd = m.pick(125, 130, 115)                 # flag drop
    t = m.h_dg * 1.2                           # flag thickness (vertical)
    tx, ty = sx - fl, cap - fd

    def edge(dy):        # upper edge shifted down by dy, from stem to tip
        return (sx, cap - dy), (sx - fl * .35, cap - dy - fd * .16), (sx - fl * .72, cap - dy - fd * .55), (tx, ty - dy)
    a0, a1, a2, a3 = edge(0)
    b0, b1, b2, b3 = edge(t)
    segs = [('L', (sx + w, 0), (sx + w, cap)), ('L', (sx + w, cap), a0),
            ('C', a0, a1, a2, a3), ('L', a3, b3),
            ('C', b3, b2, b1, b0), ('L', b0, (sx, 0)), ('L', (sx, 0), (sx + w, 0))]
    return P.DIGIT_WIDTH, [cpoly(m, segs)]
