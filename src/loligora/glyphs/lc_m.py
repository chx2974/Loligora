from .. import lc_params as L
from ..lc_parts import arch
from ..strokes import stem
from .. import params as P

NAME, UNI = "m", 0x6D


def draw(m):
    sb, st = L.sb_s(m), m.stem_lc
    tx = L.leg(m)
    cw = (L.w(m, L.W_M) - st - 2 * tx) / 2
    xs1 = sb + st
    xr1 = xs1 + cw + tx
    xr2 = xr1 + cw + tx
    args = L.arch_args(m)
    a1 = arch(m, xs1, xr1, xs1 - st / 2, *args, 0, n=L.N_ARCH - 0.5)
    a2 = arch(m, xr1, xr2, xr1 - tx / 2, *args, 0)
    return L.w(m, L.W_M) + 2 * sb, [stem(m, sb, 0, P.XH, st),
                            stem(m, xr1 - tx, 0, L.arch_cy(), tx), a1, a2]
