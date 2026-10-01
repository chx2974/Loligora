from .. import lc_params as L
from .. import params as P
from ..lc_curls import tail
from ..strokes import bar

NAME, UNI = "t", 0x74


def draw(m):
    st = m.stem_lc
    xb = L.sb_o(m)
    xo = xb + m.pick(92, 72, 44)   # long crossbar left of the stem
    cy = L.tail_v(m) - P.OVERSHOOT
    xf = xo + st + L.tail_ext(m) - 20
    t = tail(m, 1, xo, xf, cy, -P.OVERSHOOT, cy - 14, st, L.term(m),
             m.h_lc * 0.95, P.XH + 150)
    hb = m.h_lc * 0.95
    xr = xf - 6 + m.pick(34, 16, 0)   # crossbar reaches past the foot curl
    return xr + 6 + L.sb_o(m), [t, bar(m, xb, xr, P.XH - hb, hb)]
