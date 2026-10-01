from .. import lc_params as L
from .. import params as P
from ..strokes import diagonal

NAME, UNI = "y", 0x79


def draw(m):
    """A v (same arm angles, vertex at the baseline centre) whose right arm runs
    straight on into the descender."""
    sb, w, d = L.sb_o(m), L.w(m, L.W_Y), L.dw(m)
    xm = sb + (w - d) / 2                   # vertex, left edge, at the baseline (as v)
    xr = sb + w - d                         # right arm, left edge at x-height
    xt = xm + (xr - xm) * P.DESC / P.XH     # right arm extended to the descender
    return w + 2 * sb, [diagonal(m, (xt, P.DESC), (xr, P.XH), d),
                        diagonal(m, (xm, 0), (sb, P.XH), d)]
