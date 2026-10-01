from ..arcs import shift
from ..strokes import npoly
from ..uc_params import sb as SB
from ..uc_parts import dw

NAME, UNI = "N", 0x4E


def draw(m):
    m = m.origin(360)
    sb, w0, st = SB(m, "STR"), m.pick(590, 610, 670), m.stem_uc
    wd = dw(m, w0 - st, 720)
    return w0 + 2 * sb, shift([npoly(m, w0, 720, wd, st)], sb)
