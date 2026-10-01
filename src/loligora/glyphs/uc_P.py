from ..strokes import stem
from ..uc_params import sb as SB
from ..uc_parts import bowl_d

NAME, UNI = "P", 0x50


def draw(m):
    m = m.origin(360)
    l, r, st, h = SB(m, "STR"), SB(m, "RND"), m.stem_uc, m.h_uc
    w = m.pick(510, 530, 570)
    a = m.pick(200, 212, 256)
    ymb = m.pick(285, 285, 262)
    bowl = bowl_d(m, l + st / 2, l + w, ymb, 720, a, st, h)
    return w + l + r, [stem(m, l, 0, 720, st), bowl]
