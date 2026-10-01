from ..strokes import bar, stem
from ..uc_params import sb as SB

NAME, UNI = "T", 0x54


def draw(m):
    m = m.origin(360)
    sb, w, st, h = SB(m, "OPN"), 570, m.stem_uc, m.h_uc
    return w + 2 * sb, [bar(m, sb, sb + w, 720 - h, h),
                        stem(m, sb + (w - st) / 2, 0, 720, st)]
