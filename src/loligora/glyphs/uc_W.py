from ..arcs import shift
from ..uc_params import apex_k, sb as SB
from ..uc_parts import dw, w_outline

NAME, UNI = "W", 0x57


def draw(m):
    m = m.origin(360)
    sb, w0 = SB(m, "DIA"), m.pick(900, 935, 1060)
    wd = dw(m, w0 / 4, 720)
    return w0 + 2 * sb, shift([w_outline(m, w0, wd, wd * apex_k(m))], sb)
