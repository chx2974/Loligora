"""ı (dotless i) and ȷ (dotless j): the letters without their dots (bases for
accented i / j)."""
from . import lc_i, lc_j


def dotlessi(m):
    adv, cs = lc_i.draw(m)
    return adv, cs[:-1]


def dotlessj(m):
    adv, cs = lc_j.draw(m)
    return adv, cs[:-1]


GLYPHS = [("dotlessi", 0x131, dotlessi), ("dotlessj", 0x237, dotlessj)]
