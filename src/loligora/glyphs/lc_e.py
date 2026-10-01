from .. import lc_params as L
from .. import params as P
from ..arcs import cring as oval_c
from ..strokes import bar

NAME, UNI = "e", 0x65


def draw(m):
    sb, w = L.sb_r(m), L.w(m, L.W_E)
    yb = L.hx(m.pick(250, 246, 224))                # bar bottom = aperture top
    hb = m.h_lc * m.pick(1.0, 0.95, 0.66)
    y_bot = L.hx(m.pick(140, 140, 168))
    ring = oval_c(m, (sb, 0, sb + w, P.XH), m.stem_lc * m.pick(1, 1, 0.9), m.h_lc * m.pick(1, 1, 0.86), yb, y_bot)
    b = bar(m, sb + m.stem_lc / 2, sb + w - m.stem_lc / 2, yb, hb)
    return w + 2 * sb, [ring, b]
