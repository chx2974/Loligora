from ..arcs import shift
from ..strokes import stem
from ..uc_params import apex_k, sb as SB
from ..uc_parts import dw, v_outline

NAME, UNI = "M", 0x4D


def draw(m):
    m = m.origin(360)
    sb, w0, st = SB(m, "STR"), m.pick(700, 740, 820), m.stem_uc
    yv = m.pick(0, 0, 30)
    wd = dw(m, w0 / 2, 720 - yv)
    v = v_outline(m, w0, 720, yv, wd, wd * apex_k(m))
    return w0 + 2 * sb, shift([stem(m, 0, 0, 720, st), stem(m, w0 - st, 0, 720, st), v], sb)
