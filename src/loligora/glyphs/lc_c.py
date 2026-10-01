from .. import lc_params as L
from .. import params as P
from ..arcs import cring as oval_c

NAME, UNI = "c", 0x63


def draw(m):
    sb, w = L.sb_r(m), L.w(m, L.W_C)
    y_top, y_bot = L.hx(m.pick(392, 392, 372)), L.hx(m.pick(148, 148, 168))
    return w + sb + L.sb_o(m), [oval_c(m, (sb, 0, sb + w, P.XH), m.stem_lc, m.h_lc, y_top, y_bot)]
