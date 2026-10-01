from .. import params as P
from ..fig_parts import band, ebox
from ..strokes import bar

NAME, UNI = "three", 0x33
OV = P.OVERSHOOT


def draw(m):
    m = m.origin(P.CAP / 2)
    sb, w, h = m.sb_dg, m.stem_dg, m.h_dg
    L, R = sb, P.DIGIT_WIDTH - sb
    hw = h * m.pick(1, 1, 1.0)                # waist bar = band thickness (no notch)
    yw = m.pick(400, 404, 396)
    top = ebox(m, L + m.pick(14, 16, 18), yw - h / 2, R - m.pick(30, 34, 34), P.CAP + OV)
    bot = ebox(m, L + 2, -OV, R, yw + h / 2)
    yt, yb = m.pick(585, 590, 570), m.pick(135, 130, 150)
    xm = max((top[0] + top[2]) / 2, (bot[0] + bot[2]) / 2)
    xl = (top[0] + top[2]) / 2 - m.pick(80, 85, 70)
    return P.DIGIT_WIDTH, [
        band(m, top, w, h * m.pick(1, 1, .9), ('a', 270), ('y', yt, 155 + 360), 9),
        band(m, bot, w, h * m.pick(1, 1, .9), ('y', yb, 205), ('a', 450), 9),
        bar(m, xl, xm + 30, yw - hw / 2, hw)]
