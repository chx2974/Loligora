from .. import lc_params as L
from .. import params as P
from ..strokes import diagonal

NAME, UNI = "v", 0x76


def draw(m):
    sb, w, d = L.sb_o(m), L.w(m, L.W_V), L.dw(m)
    xm = sb + (w - d) / 2
    return w + 2 * sb, [diagonal(m, (xm, 0), (sb, P.XH), d),
                        diagonal(m, (xm, 0), (sb + w - d, P.XH), d)]
