from .. import lc_params as L
from .. import params as P
from ..strokes import zpoly

NAME, UNI = "z", 0x7A


def draw(m):
    """One-piece z: diagonal edges run exactly into the bars' outer corners."""
    sb, w = L.sb_r(m), L.w(m, L.W_Z)
    h = m.h_lc * 0.95
    d = m.h_lc * 1.25
    return w + 2 * sb, [zpoly(m, w, P.XH, h, d, sb)]
