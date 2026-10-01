from .. import params as P
from ..fig_parts import band, ebox
from ..strokes import bar, stem

NAME, UNI = "five", 0x35
OV = P.OVERSHOOT


def draw(m):
    m = m.origin(P.CAP / 2)
    sb, w, h = m.sb_dg, m.stem_dg, m.h_dg
    L, R = sb + 6, P.DIGIT_WIDTH - sb
    bt = m.pick(455, 460, 440)             # top of bowl
    bowl = ebox(m, L + m.pick(4, 6, 6), -OV, R, bt)
    cy = (bt - OV) / 2
    ys = cy + m.pick(30, 30, 20)
    yb = m.pick(150, 150, 160)
    return P.DIGIT_WIDTH, [
        bar(m, L, R - m.pick(14, 20, 20), P.CAP - h, h),
        stem(m, L, ys, P.CAP, w),
        band(m, bowl, w * .95, h, ('y', yb, 215), ('a', 168 + 360), 9)]
