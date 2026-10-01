from ..strokes import stem
from ..uc_params import sb as SB

NAME, UNI = "I", 0x49


def draw(m):
    m = m.origin(360)
    sb = SB(m, "STR")
    return m.stem_uc + 2 * sb, [stem(m, sb, 0, 720, m.stem_uc)]
