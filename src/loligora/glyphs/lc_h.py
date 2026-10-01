from .. import lc_params as L
from ..lc_parts import arch
from ..strokes import stem

NAME, UNI = "h", 0x68


def draw(m):
    sb, st = L.sb_s(m), m.stem_lc
    xs, xr = sb + st, sb + L.w(m, L.W_N)
    a = arch(m, xs, xr, xs - st / 2, *L.arch_args(m), 0)
    return L.w(m, L.W_N) + 2 * sb, [stem(m, sb, 0, 760, st), a]
