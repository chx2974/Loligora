from .. import lc_params as L
from .. import params as P
from ..lc_curls import dot, tail
from ..strokes import stem

NAME, UNI = "j", 0x6A


def draw(m):
    st = m.stem_lc
    xf = L.sb_s(m) - L.tail_ext(m) + 20          # tail tucks under the previous letter
    xo = xf + st + L.tail_ext(m) - 10
    cy = P.DESC + L.tail_v(m) * 0.9
    t = tail(m, -1, xo, xf, cy, P.DESC - P.OVERSHOOT, cy - 12, st, L.term(m),
             m.h_lc * 0.95, 120)
    return xo + L.sb_s(m), [stem(m, xo - st, 100, P.XH, st), t,
                            dot(m, xo - st / 2, L.dot_cy(m), L.dot_size(m))]
