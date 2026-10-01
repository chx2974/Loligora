from .. import lc_params as L
from .. import params as P
from ..lc_curls import tail

NAME, UNI = "l", 0x6C


def draw(m):
    """Tailed l: stem + superellipse elbow ending in a horizontal cut."""
    sb, st = L.sb_s(m), m.stem_lc
    cy = L.tail_v(m) - P.OVERSHOOT
    xf = sb + st + L.ltail_ext(m)
    t = tail(m, 1, sb, xf, cy, -P.OVERSHOOT, L.ltail_cut(m, cy, -P.OVERSHOOT), st, L.term(m),
             m.h_lc * 0.95, P.ASC)
    return xf + L.sb_o(m), [t]
