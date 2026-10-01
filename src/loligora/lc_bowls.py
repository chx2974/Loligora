"""Shared drawing of b d p q: a stem plus a notched bowl."""
from . import lc_params as L
from . import params as P
from .lc_parts import bowl
from .strokes import stem


def bowl_letter(m, right_bowl, y0, y1):
    """right_bowl=True: stem on the left (b p); False: stem on the right (d q).
    Stem runs y0..y1."""
    st = m.stem_lc
    ty = L.arch_top(m)
    args = (-P.OVERSHOOT, P.XH + P.OVERSHOOT, L.leg(m), ty, L.arch_notch(m),
            L.arch_tj(m))
    if right_bowl:
        sb = L.sb_s(m)
        xs = sb + st
        b = bowl(m, xs, sb + L.w(m, L.W_B), 1, xs - st / 2, *args)
        adv, sx = L.w(m, L.W_B) + sb + L.sb_r(m), sb
    else:
        sb = L.sb_r(m)
        xs = sb + L.w(m, L.W_B) - st
        b = bowl(m, xs, sb, -1, xs + st / 2, *args)
        adv, sx = L.w(m, L.W_B) + sb + L.sb_s(m), xs
    return adv, [stem(m, sx, y0, y1, st), b]
