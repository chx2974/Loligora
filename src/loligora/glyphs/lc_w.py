from .. import lc_params as L
from .. import params as P
from ..strokes import diagonal

NAME, UNI = "w", 0x77


def draw(m):
    sb, w, d = L.sb_o(m), L.w(m, L.W_W), L.dw(m) * m.pick(0.92, 0.92, 0.72)
    xa, xb = sb + w * 0.25 - d / 2, sb + w * 0.75 - d / 2
    xm = sb + (w - d) / 2
    return w + 2 * sb, [diagonal(m, (xa, 0), (sb, P.XH), d), diagonal(m, (xa, 0), (xm, P.XH), d),
                        diagonal(m, (xb, 0), (xm, P.XH), d),
                        diagonal(m, (xb, 0), (sb + w - d, P.XH), d)]
