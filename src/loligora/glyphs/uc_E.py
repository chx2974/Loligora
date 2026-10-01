from ..strokes import bar, stem
from ..uc_params import sb as SB

NAME, UNI = "E", 0x45


def draw(m):
    m = m.origin(360)
    l, r, w, st, h = SB(m, "STR"), SB(m, "OPN"), 480, m.stem_uc, m.h_uc
    ym = (720 - h) / 2 + 6
    return w + l + r, [stem(m, l, 0, 720, st), bar(m, l, l + w, 720 - h, h),
                       bar(m, l, l + w - 28, ym, h), bar(m, l, l + w, 0, h)]
