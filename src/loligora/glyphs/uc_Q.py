from ..rounds import oval_ring
from ..uc_params import sb as SB
from ..uc_parts import dpoly, dw
from ..strokes import shpoly

NAME, UNI = "Q", 0x51


def draw(m):
    m = m.origin(360)
    sb, w, st, h = SB(m, "RND"), 640, m.stem_uc, m.h_uc
    cx = sb + w / 2
    x0, y0, x1, y1 = cx + 20, 170, cx + 175, -60
    wd = dw(m, x1 - x0, y0 - y1, 1.0 * h / st)
    tail = dpoly(m, (x0, y0), (x1, y1), wd)
    return w + 2 * sb, oval_ring(m, (sb, 0, sb + w, 720), st, h) + [tail]
