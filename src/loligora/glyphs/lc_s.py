from .. import lc_params as L
from .. import params as P
from ..arcs import cring
from ..arcs import rot180

NAME, UNI = "s", 0x73


def draw(m):
    sb, w = L.sb_r(m) + 4, L.w(m, L.W_S)
    ty = m.h_lc * m.pick(0.92, 0.92, 0.76)
    delta = m.pick(6, 10, 12)                  # upper ring shifted right of the lower one
    x0 = sb + delta
    ym = P.XH / 2
    y_top = L.hx(m.pick(392, 392, 388))
    upper = cring(m, (x0, ym - ty / 2, sb + w, P.XH), m.stem_lc * m.pick(0.92, 0.92, 0.84), ty,
                  y_top, None, over="top", kappa=0.28)
    adv = w + 2 * sb
    return adv, [upper] + rot180([upper], adv, P.XH / 2)
