from ..strokes import bar, stem
from ..uc_params import sb as SB

NAME, UNI = "F", 0x46


def draw(m):
    m = m.origin(360)
    l, r, w, st, h = SB(m, "STR"), SB(m, "OPN"), 460, m.stem_uc, m.h_uc
    ym = (720 - h) / 2 + 20
    return w + l + r, [stem(m, l, 0, 720, st), bar(m, l, l + w, 720 - h, h),
                       bar(m, l, l + w - 30, ym, h)]
