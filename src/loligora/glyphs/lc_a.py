from .. import lc_params as L
from .. import params as P
from ..lc_curls import hook
import math

from ..lc_a_parts import bowl, lower_bowl
from ..strokes import stem

NAME, UNI = "a", 0x61


def _single(m):
    """Italic default: single-storey a (ring bowl + right stem)."""
    st, sb = m.stem_lc, L.sb_r(m)
    xs = sb + L.w(m, L.W_B) - st
    ty = L.arch_top(m) * m.pick(1, 1, 0.86)      # lighter bowl at 950: open counter
    b = bowl(m, xs, sb, -1, xs + st / 2, -P.OVERSHOOT, P.XH + P.OVERSHOOT,
             L.leg(m) * m.pick(1, 1, 0.86), ty, L.notch(m), L.join_thin(m) * ty)
    return L.w(m, L.W_B) + sb + L.sb_s(m), [stem(m, xs, 0, P.XH, st), b]


def draw(m):
    """Double-storey a, Public Sans-like: straight stem, generous hook, tall round bowl."""
    if m.italic:
        return _single(m)
    st, sb = m.stem_lc, L.sb_s(m)
    x0 = L.sb_r(m)
    wa = L.W_A * 0.97
    xo = x0 + L.w(m, wa)
    ty = L.arch_top(m)
    y_end = P.XH * m.pick(0.72, 0.72, 0.69)        # hook terminal height
    n_a = 3.2
    N_BOWL = 4.0
    h = hook(m, -1, xo, x0 + 4, L.arch_cy(), P.XH + P.OVERSHOOT, y_end,
             st, L.term(m) * 0.95, ty, 0, n=n_a)
    top = P.XH * m.pick(0.60, 0.60, 0.62)            # outer bar height at the stem edge
    sl = math.tan(math.radians(m.pick(8.0, 8.0, 6.5)))   # slope of the middle line
    xb = xo - st                                     # stem edge
    tp = ty * m.pick(0.95, 0.95, 0.66)               # perpendicular bar / bottom thickness
    tj = L.join_thin(m) * ty * m.pick(1.0, 1.0, 0.8)  # thickness at the stem join
    W = xb - x0
    cfg = dict(hc=0.26 * W, bc=0.16 * P.XH, wall=20, hci=0.22 * W, L=0.2 * W)
    b = lower_bowl(m, x0, xb, xb + 14, xb + 8, top, sl,
                   L.leg(m) * m.pick(.95, .95, .76), tp, tj,
                   m.pick(0, 3, 6), cfg, n=N_BOWL)
    return L.w(m, wa) + x0 + sb, [h, b]
