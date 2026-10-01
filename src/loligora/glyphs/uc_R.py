from ..strokes import stem
from ..uc_params import sb as SB
from ..uc_parts import bowl_d, dpoly, dw

NAME, UNI = "R", 0x52


def draw(m):
    m = m.origin(360)
    l, r, st, h = SB(m, "STR"), SB(m, "OPN"), m.stem_uc, m.h_uc
    w = m.pick(520, 540, 580)
    a = m.pick(200, 212, 256)
    ymb = m.pick(300, 300, 280)
    bx1 = l + w - m.pick(6, 8, 14)
    bowl = bowl_d(m, l + st / 2, bx1, ymb, 720, a, st, h)
    yj = ymb + h * 0.75                       # leg starts inside the bowl's lower stroke
    xt = l + w * 0.36
    wd = dw(m, l + w - xt - 100, yj)
    leg = dpoly(m, (xt, yj), (l + w - wd, 0), wd)
    return w + l + r, [stem(m, l, 0, 720, st), bowl, leg]
