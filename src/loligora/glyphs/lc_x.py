from .. import lc_params as L
from .. import params as P
from ..strokes import diagonal

NAME, UNI = "x", 0x78


def draw(m):
    sb, w, d = L.sb_o(m), L.w(m, L.W_X), L.dw(m) * m.pick(0.95, 0.95, 0.76)
    return w + 2 * sb, [diagonal(m, (sb + w - d, 0), (sb, P.XH), d),
                        diagonal(m, (sb, 0), (sb + w - d, P.XH), d)]
