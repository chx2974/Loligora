from ..strokes import stem
from ..uc_params import sb as SB
from ..uc_parts import bowl_d

NAME, UNI = "D", 0x44


def draw(m):
    m = m.origin(360)
    l, r, w, st, h = SB(m, "STR"), SB(m, "RND"), 610, m.stem_uc, m.h_uc
    bowl = bowl_d(m, l + st / 2, l + w, 0, 720, 300, st, h)
    return w + l + r, [stem(m, l, 0, 720, st), bowl]
