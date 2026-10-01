from ..strokes import stem
from ..uc_params import sb as SB
from ..uc_parts import u_bottom

NAME, UNI = "U", 0x55


def draw(m):
    m = m.origin(360)
    sb, w, st, h = SB(m, "STR"), 570, m.stem_uc, m.h_uc
    bot, yc = u_bottom(m, sb, sb + w, -12, st, h, 265)
    return w + 2 * sb, [stem(m, sb, yc, 720, st), stem(m, sb + w - st, yc, 720, st), bot]
