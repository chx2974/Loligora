from .. import lc_params as L
from ..arcs import rot180
from ..lc_parts import arch
from ..strokes import stem
from .. import params as P

NAME, UNI = "u", 0x75


def draw(m):
    sb, st = L.sb_s(m), m.stem_lc
    xs, xr = sb + st, sb + L.w(m, L.W_N)
    a = arch(m, xs, xr, xs - st / 2, *L.arch_args(m), 0)
    adv = L.w(m, L.W_N) + 2 * sb
    return adv, rot180([stem(m, sb, 0, P.XH, st), a], adv, P.XH / 2)
