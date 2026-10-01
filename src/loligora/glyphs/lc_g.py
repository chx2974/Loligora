from .. import lc_params as L
from .. import params as P
from ..lc_curls import tail
from ..lc_parts import bowl
from ..strokes import stem

NAME, UNI = "g", 0x67


def draw(m):
    st, sb = m.stem_lc, L.sb_r(m)
    xs = sb + L.w(m, L.W_B) - st
    ty = L.arch_top(m) * m.pick(1, 1, 0.86)      # lighter loop strokes at 950: open counter
    b = bowl(m, xs, sb, -1, xs + st / 2, -P.OVERSHOOT, P.XH + P.OVERSHOOT,
             L.leg(m) * m.pick(1, 1, 0.86), ty, L.notch(m), L.join_thin(m) * ty)
    cy = P.DESC + L.tail_v(m) * 0.9
    ybot = P.DESC - P.OVERSHOOT
    xf = xs + st - st - L.gtail_ext(m)          # far extreme of the curl
    t = tail(m, -1, xs + st, xf, cy, ybot, ybot + (cy - ybot) * 0.4,
             st, L.term(m), m.h_lc * 0.95, 120)
    return L.w(m, L.W_B) + sb + L.sb_s(m), [stem(m, xs, 100, P.XH, st), b, t]
