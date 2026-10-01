from ..arcs import shift
from ..uc_params import apex_k, sb as SB
from ..uc_parts import dw, v_outline

NAME, UNI = "V", 0x56


def draw(m):
    m = m.origin(360)
    sb, w0 = SB(m, "DIA"), m.pick(650, 665, 770)
    wd = dw(m, w0 / 2, 720)
    return w0 + 2 * sb, shift([v_outline(m, w0, 720, 0, wd, wd * apex_k(m))], sb)
