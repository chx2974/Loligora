"""Sharp s (ß): stem + round arch (low exponent) into a narrow upper bowl whose
waist ends in a free vertical cut short of the stem, plus a wider lower bowl
(n~3) that returns to a horizontal terminal on the baseline, open to the left.
Stem, arch, upper bowl, waist and lower bowl are one connected shape; the only
white gap is the open one between the waist end and the stem."""
from .. import lc_params as L
from .. import params as P
from ..cs_kit import rect
from ..sym_kit import arcy

NAME = "germandbls"
UNI = 0xDF


def draw(m):
    st, sb = m.stem_lc * m.pick(1, 1, 0.78), L.sb_s(m)
    ty = m.h_lc * m.pick(1.0, 1.0, 0.60)
    tx = st * m.pick(1.0, 1.0, 0.61)
    wl = m.pick(450, 460, 650)             # lower bowl: stem left edge -> right extreme
    frac = m.pick(0.72, 0.76, 0.88)        # upper bowl width / lower bowl width
    ytop = P.ASC + P.OVERSHOOT
    yw0 = L.hx(m.pick(380, 380, 370))            # waist band bottom
    gap = st * m.pick(0.5, 0.5, 0.6)                          # free end of the waist to the stem
    xw = sb + st + gap                      # waist free end
    wu = frac * (wl - st) + st              # upper ring: left extreme at sb
    cyu, bu = (yw0 + ytop) / 2, (ytop - yw0) / 2
    yl_top = yw0 + ty
    cyl, bl = (yl_top - P.OVERSHOOT) / 2, (yl_top + P.OVERSHOOT) / 2
    nu = m.pick(2.3, 2.3, 2.3)
    up = arcy(m, sb + wu / 2, cyu, wu / 2, bu, st * m.pick(0.98, 0.98, 0.87), ty, ('x', sb + wu / 2 - 15), ('L',),
              (2, 3, 3, 4), n=nu)
    wl2 = wl - gap - 0.0
    xl = xw - 10
    low = arcy(m, xl + wl2 / 2, cyl, wl2 / 2, bl, tx, ty, ('y', m.pick(90, 100, 105)),
               ('x', xl + wl2 / 2 - 30), (3, 3, 3, 2), n=3.0)
    arm = rect(m, xw, yw0, xl + wl2 / 2 - 10, yl_top)
    ystem = cyu
    return xl + wl2 + L.sb_r(m) + 10, [rect(m, sb, 0, sb + st, ystem), up, low, arm]
