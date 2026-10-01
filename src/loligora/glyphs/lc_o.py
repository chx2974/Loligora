from .. import lc_params as L
from .. import params as P
from ..rounds import oval_ring

NAME, UNI = "o", 0x6F


def draw(m):
    sb, w = L.sb_r(m), L.w(m, L.W_O)
    return w + 2 * sb, oval_ring(m, (sb, 0, sb + w, P.XH), m.stem_lc, m.h_lc)
