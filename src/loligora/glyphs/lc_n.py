from .. import lc_params as L
from ..lc_parts import arch
from ..strokes import stem
from .. import params as P

NAME, UNI = "n", 0x6E


def draw(m):
    sb, st = L.sb_s(m), m.stem_lc
    xs, xr = sb + st, sb + L.w(m, L.W_N)
    ty = L.arch_top(m)
    a = arch(m, xs, xr, xs - st / 2, L.leg(m), ty, L.arch_notch(m),
             L.arch_tj(m), L.arch_cy(), 0)
    return L.w(m, L.W_N) + 2 * sb, [stem(m, sb, 0, P.XH, st), a]
