from .. import params as P
from ..fig_parts import ebox, ring

NAME, UNI = "eight", 0x38
OV = P.OVERSHOOT


def draw(m):
    m = m.origin(P.CAP / 2)
    sb, w, h = m.sb_dg, m.stem_dg, m.h_dg
    L, R = sb, P.DIGIT_WIDTH - sb
    yw = m.pick(395, 398, 392)            # waist centre
    dx = m.pick(16, 18, 20)               # top bowl narrower
    bot = ebox(m, L, -OV, R, yw + h / 2)
    top = ebox(m, L + dx, yw - h / 2, R - dx, P.CAP + OV)
    return P.DIGIT_WIDTH, ring(m, bot, w, h) + ring(m, top, w * .96, h)
