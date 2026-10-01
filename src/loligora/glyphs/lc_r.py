from .. import lc_params as L
from ..lc_parts import arch
from ..strokes import stem
from .. import params as P

NAME, UNI = "r", 0x72


def draw(m):
    sb, st = L.sb_s(m), m.stem_lc
    xs, xr = sb + st, sb + L.w(m, L.W_R)
    args = list(L.arch_args(m))
    args[0] = m.stem_lc * 0.82          # thinner arm terminal
    a = arch(m, xs, xr, xs - st / 2, *args, 0, hcut=L.hx(390))
    return L.w(m, L.W_R) + sb + L.sb_o(m) + m.pick(12, 6, 2), [stem(m, sb, 0, P.XH, st), a]
