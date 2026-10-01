from .. import lc_params as L
from .. import params as P
from ..lc_curls import hook
from ..strokes import bar

NAME, UNI = "f", 0x66


def draw(m):
    st = m.stem_lc
    r = L.tail_v(m)
    xb = L.sb_o(m)
    xo = xb + m.pick(92, 68, 36)   # long crossbar left of the stem
    top = P.ASC + P.OVERSHOOT
    cy = top - r
    xf = xo + st + L.tail_ext(m) + m.pick(45, 22, 0) - 20
    h = hook(m, 1, xo, xf, cy, top, cy + 12, st, L.term(m), m.h_lc * 0.95, 0)
    hb = m.h_lc * 0.95
    return xf - 30 + L.sb_o(m), [h, bar(m, xb, xf - 10, P.XH - hb, hb)]
