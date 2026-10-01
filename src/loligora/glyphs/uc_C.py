from ..arcs import cring
from ..uc_params import sb as SB

NAME, UNI = "C", 0x43


def draw(m):
    m = m.origin(360)
    l, r, w = SB(m, "RND"), SB(m, "OPN"), 610
    yt = m.pick(540, 536, 546)
    return w + l + r, [cring(m, (l, -12, l + w, 732), m.stem_uc, m.h_uc, yt, 720 - yt,
                                over=False, optical=False)]
