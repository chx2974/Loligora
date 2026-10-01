from ..strokes import stem
from ..uc_params import sb as SB
from ..uc_parts import bowl_d

NAME, UNI = "B", 0x42


def draw(m):
    m = m.origin(360)
    l, r, st, h = SB(m, "STR"), SB(m, "RND"), m.stem_uc, m.h_uc
    w = m.pick(520, 540, 580)
    au, al = m.pick(180, 192, 240), m.pick(200, 212, 262)
    ymb = 360 - h / 2 + 10                     # bottom of the waist bar
    xl = l + st / 2
    up = bowl_d(m, xl, l + w - m.pick(20, 22, 30), ymb, 720, au, st, h)
    lo = bowl_d(m, xl, l + w, 0, ymb + h, al, st, h)
    return w + l + r, [stem(m, l, 0, 720, st), up, lo]
