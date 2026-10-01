from ..arcs import shift
from ..strokes import bar
from ..uc_params import apex_k, sb as SB
from ..uc_parts import a_outline, dw

NAME, UNI = "A", 0x41


def draw(m):
    m = m.origin(360)
    sb, w0, h = SB(m, "DIA"), m.pick(650, 665, 770), m.h_uc
    wd = dw(m, w0 / 2, 720)
    u = wd * apex_k(m)
    yb = m.pick(170, 175, 150)
    sl = (w0 / 2 - u / 2) / 720
    xl = sl * (yb + h / 2) + wd / 2
    return w0 + 2 * sb, shift([a_outline(m, w0, wd, u), bar(m, xl, w0 - xl, yb, h * 0.92)], sb)
