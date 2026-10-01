from ..strokes import bar, stem
from ..uc_params import sb as SB

NAME, UNI = "H", 0x48


def draw(m):
    m = m.origin(360)
    sb, w, st = SB(m, "STR"), 570, m.stem_uc
    y = (720 - m.h_uc) / 2 + 6
    return w + 2 * sb, [stem(m, sb, 0, 720, st), stem(m, sb + w - st, 0, 720, st),
                        bar(m, sb + st / 2, sb + w - st / 2, y, m.h_uc)]
