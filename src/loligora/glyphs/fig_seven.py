from .. import params as P
from ..fig_parts import ccw
from ..strokes import shpoly

NAME, UNI = "seven", 0x37


def draw(m):
    m = m.origin(P.CAP / 2)
    sb, w, h = m.sb_dg, m.stem_dg, m.h_dg
    L, R = sb, P.DIGIT_WIDTH - sb
    dw = w * 1.15
    xb = L + (R - L) * m.pick(.20, .22, .27)
    top, yb = P.CAP, P.CAP - h
    # one contour: the diagonal's outer edge runs exactly into the bar's
    # bottom-right corner, the inner edge into the bar's underside
    return P.DIGIT_WIDTH, [ccw(shpoly(m, [(L, top), (R, top), (R, yb), (xb + dw, 0), (xb, 0),
                                      (R - dw, yb), (L, yb)]))]
