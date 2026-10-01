from .. import lc_params as L
from .. import params as P
from ..strokes import kpoly

NAME, UNI = "k", 0x6B


def draw(m):
    sb, st, d = L.sb_s(m), m.stem_lc, L.dw(m) * m.pick(0.95, 0.95, 0.76)
    w = L.w(m, L.W_K)
    ya = L.hx(m.pick(215, 215, 230))                  # arm underside meets the stem
    px = m.pick(60, 65, 100)                    # leg springs from the arm this far off the stem
    c, q = kpoly(m, w, st, P.ASC, P.XH, ya, px, d, d, x0=sb)
    return w + sb + L.sb_o(m), [c]
