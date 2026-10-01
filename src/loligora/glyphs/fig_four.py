from .. import params as P
from ..fig_parts import ccw
from ..strokes import shpoly, stem

NAME, UNI = "four", 0x34


def draw(m):
    m = m.origin(P.CAP / 2)
    sb, w, h = m.sb_dg, m.stem_dg, m.h_dg
    L, R = sb, P.DIGIT_WIDTH - sb
    yb = m.pick(165, 165, 150)                 # bar bottom
    xs = R - m.pick(52, 56, 52) - w            # stem left edge
    dw = w * m.pick(1, 1, .78)                 # diagonal horizontal width (<= stem: no nub at the top)
    # One polygon: diagonal + bar. The outer (left) edge runs from the stem's top-left
    # corner straight to the bar's bottom-left corner (L, yb); the inner edge is parallel
    # and ends on the bar top edge (counter corner). Stem stays its own stroke.
    k = (xs - L) / (P.CAP - yb)                # dx/dy of both diagonal edges
    xi = xs + dw - (P.CAP - (yb + h)) * k
    diag = ccw(shpoly(m, [(L, yb), (R, yb), (R, yb + h), (xi, yb + h), (xs + dw, P.CAP), (xs, P.CAP)]))
    return P.DIGIT_WIDTH, [stem(m, xs, 0, P.CAP, w), diag]
