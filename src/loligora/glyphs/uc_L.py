from ..strokes import bar, stem
from ..uc_params import sb as SB

NAME, UNI = "L", 0x4C


def draw(m):
    m = m.origin(360)
    l, r, w, st, h = SB(m, "STR"), SB(m, "OPN"), 430, m.stem_uc, m.h_uc
    return w + l + r, [stem(m, l, 0, 720, st), bar(m, l, l + w, 0, h)]
