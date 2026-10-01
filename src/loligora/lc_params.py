"""Lowercase-only parameters (per master via m.pick(thin, regular, black)).

Spacing method (classic): o and n are set first, everything else is derived
from three side types.
  sb_s  straight side (n stem, i, l, h ...)
  sb_r  round side    (o, c, e, bowls; slightly tighter, the curve rolls away)
  sb_o  open side     (r arm, y/v/w/x diagonals, f/t/z terminals)
Thin needs much tighter values than its stem width suggests: the counters
stay large while the ink is nearly invisible.
"""


def sb_s(m):
    return m.pick(75, 74, 58)


def sb_r(m):
    return m.pick(56, 56, 40)


def sb_o(m):
    return m.pick(41, 42, 32)


def notch(m):
    """Depth of the outer notch where an arch/bowl leaves a stem (units below x-height)."""
    return m.pick(11, 24, 30)


def arch_out(m):
    """Height (fraction of XH) where the outer edge of an arch/bowl leaves the stem."""
    return m.pick(0.78, 0.78, 0.74)


def arch_in(m):
    """Height (fraction of XH) where the counter edge of an arch/bowl meets the stem."""
    return m.pick(0.60, 0.58, 0.54)


def arch_notch(m):
    """Depth of the V-notch crossing below the x-height (units)."""
    return _P().XH * (1 - arch_out(m))


def arch_tj(m):
    """Vertical stroke thickness of the arch where it branches off the stem."""
    return _P().XH * (arch_out(m) - arch_in(m))


N_ARCH = 2.7        # superellipse exponent of the n h m u r arch (o/bowls keep N_LETTER = 3)


def join_thin(m):
    """Arch stroke thickness at the join, as a fraction of the arch top thickness."""
    return m.pick(0.85, 0.72, 0.66)


def arch_top(m):
    """Arch / bowl top+bottom stroke thickness."""
    return m.h_lc * m.pick(0.90, 0.90, 0.80)


def leg(m):
    """Right leg thickness of n h m u ..."""
    return m.stem_lc * 0.96


# widths (ink to ink) at the Thin/Regular masters; use w(m, W_N) in glyphs
W_N = 458
W_O = 500

ARCH_B = 240        # half-height of the arch ring of n h m (centre at x-height + overshoot - ARCH_B)


def _P():
    from . import params
    return params


def hx(v):
    """Scale a height that was designed for the old 540 x-height to the current XH."""
    return v * _P().XH / 540


def ws(m):
    """Width factor: the black master is widened (counters of a e s g o would
    otherwise close up next to the capitals); linear in between."""
    return m.pick(1.0, 1.0, 1.2)


def w(m, base):
    """Ink width of a lowercase letter for master m."""
    return base * ws(m)


def arch_cy():
    from . import params as P
    return P.XH + P.OVERSHOOT - ARCH_B

W_M = 790           # m ink width
W_R = 340           # r arm
W_B = 490           # bowl letters b d p q (ink width incl. stem)


def arch_args(m):
    """(top thickness, notch, join thickness, leg thickness, centre height)"""
    ty = arch_top(m)
    return leg(m), ty, arch_notch(m), arch_tj(m), arch_cy()

# other widths (ink to ink)
W_C, W_E, W_A = 450, 480, 470
W_V, W_W, W_X, W_Y, W_Z, W_S, W_K = 470, 740, 470, 470, 430, 430, 450


def dw(m):
    """Horizontal width of diagonal strokes (perpendicular thickness ~0.9 stem)."""
    return m.stem_lc * 1.12


def dot_size(m):
    return m.pick(36, 104, 168)


def dot_cy(m):
    # dot top = 760 - (540 - XH): same gap above the x-height as before the 75% -> 72% change
    return 760 - (540 - _P().XH) - dot_size(m) / 2


def term(m):
    """Horizontal thickness of curled terminals (tails, hooks)."""
    return m.h_lc * m.pick(1.0, 1.0, 0.7)


def tail_v(m):
    """Vertical radius of tail rings (l t g j f)."""
    return m.pick(100, 118, 165)


def tail_ext(m):
    """How far the tail reaches beyond the stem edge."""
    return m.pick(120, 150, 175)


def ltail_ext(m):
    """Short foot tail of l t j: reach beyond the stem edge."""
    return m.pick(62, 74, 84)


def ltail_cut(m, cy, ybot):
    """Height of the low, near-horizontal terminal cut of the short tail."""
    return ybot + (cy - ybot) * 0.2


def gtail_ext(m):
    """Descender hook of g: reach beyond the stem's left edge, long enough to
    run under the bowl (about 80% of the bowl width from the right edge)."""
    return 0.8 * w(m, W_B) - m.stem_lc
