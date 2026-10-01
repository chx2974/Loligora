from .. import lc_params as L
from .. import params as P
from ..lc_curls import dot
from ..strokes import stem

NAME, UNI = "i", 0x69


def draw(m):
    sb, st = L.sb_s(m), m.stem_lc
    return st + 2 * sb, [stem(m, sb, 0, P.XH, st), dot(m, sb + st / 2, L.dot_cy(m), L.dot_size(m))]
