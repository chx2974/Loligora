from ..rounds import oval_ring
from ..uc_params import sb as SB

NAME, UNI = "O", 0x4F


def draw(m):
    m = m.origin(360)
    sb, w = SB(m, "RND"), 640
    return w + 2 * sb, oval_ring(m, (sb, 0, sb + w, 720), m.stem_uc, m.h_uc)
