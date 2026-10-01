from ..arcs import shift
from ..strokes import xpoly
from ..uc_params import sb as SB
from ..uc_parts import dw

NAME, UNI = "X", 0x58


def draw(m):
    m = m.origin(360)
    sb, w = SB(m, "DIA"), m.pick(610, 630, 700)
    wd = dw(m, w - m.stem_uc, 720)
    return w + 2 * sb, shift([xpoly(m, w, 720, wd)], sb)
