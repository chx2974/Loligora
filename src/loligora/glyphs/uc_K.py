from ..arcs import shift
from ..strokes import kpoly
from ..uc_params import sb as SB
from ..uc_parts import dw

NAME, UNI = "K", 0x4B


def draw(m):
    m = m.origin(360)
    l, r, st = SB(m, "STR"), SB(m, "OPN"), m.stem_uc
    w = m.pick(520, 545, 610)
    ya = m.pick(300, 300, 300)                      # arm underside meets the stem
    px = m.pick(80, 90, 150)                        # leg springs from the arm this far off the stem
    wa = dw(m, w - st, 720 - ya)
    wl = dw(m, w - st - px, ya + px * (720 - ya) / (w - st))
    c, q = kpoly(m, w, st, 720, 720, ya, px, wa, wl)
    return w + l + r, shift([c], l)
