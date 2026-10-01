from ..uc_params import sb as SB
from ..uc_parts import s_shape

NAME, UNI = "S", 0x53


def draw(m):
    m = m.origin(360)
    l, r, w = SB(m, "RND"), SB(m, "RND"), m.pick(540, 550, 580)
    yt = m.pick(570, 566, 570)
    return w + l + r, [s_shape(m, l, l + w, 360, m.stem_uc * 0.96, m.h_uc, yt)]
