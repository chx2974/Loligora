from ..strokes import stem
from ..uc_params import sb as SB
from ..uc_parts import j_hook

NAME, UNI = "J", 0x4A


def draw(m):
    m = m.origin(360)
    l, r, w, st, h = SB(m, "RND"), SB(m, "STR"), m.pick(400, 410, 500), m.stem_uc, m.h_uc
    hook, yc = j_hook(m, l, l + w, -12, st, h, m.pick(215, 215, 245), m.pick(255, 250, 262))
    return w + l + r, [stem(m, l + w - st, yc, 720, st), hook]
