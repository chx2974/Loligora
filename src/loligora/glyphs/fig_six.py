from .. import params as P
from ..fig_parts import band, ebox, rot180, ring
from ..strokes import stem

NAME, UNI = "six", 0x36
OV = P.OVERSHOOT


def six(m):
    m = m.origin(P.CAP / 2)
    sb, w, h = m.sb_dg, m.stem_dg, m.h_dg
    L, R = sb, P.DIGIT_WIDTH - sb
    bowl_top = m.pick(415, 425, 400)
    bowl = ebox(m, L, -OV, R, bowl_top)
    # top hook: quarter-ish superellipse from the left stem over to a horizontal cut
    ya = P.CAP + OV - m.pick(370, 380, 370)
    hook = ebox(m, L, ya, R - m.pick(10, 12, 10), P.CAP + OV)
    yc = m.pick(580, 580, 560)
    cy_hook = (ya + P.CAP + OV) / 2
    cy_bowl = (bowl_top - OV) / 2
    return (ring(m, bowl, w, h)
            + [band(m, hook, w, h, ('y', yc, 5), ('a', 180), 8),
               stem(m, L, cy_bowl, cy_hook + 2, w)])


def draw(m):
    return P.DIGIT_WIDTH, six(m)
