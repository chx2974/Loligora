"""Barred letters for GF Latin Core: Ł ł (slanted stroke through the stem),
đ ħ (horizontal bar across the ascender stem), Ħ (bar across both stems)."""
from .. import lc_params as L
from ..arcs import shift
from ..cs_kit import H, strut
from ..strokes import bar
from ..uc_params import sb as SB
from . import lc_d, lc_h, lc_l, uc_H, uc_L


def Lslash(m):
    adv, cs = uc_L.draw(m)
    m = m.origin(360)
    dx, l = 44, SB(m, "STR")
    x0, x1 = l + dx - 54, l + dx + m.stem_uc + 80
    y = 330 + 0 * m.stem_uc
    return adv + dx, shift(cs, dx) + [strut(m, (x0, y - 36), (x1, y + 36), H(m) * 0.95)]


def lslash(m):
    adv, cs = lc_l.draw(m)
    sb, st = L.sb_s(m), m.stem_lc
    x0, x1 = sb - 36, sb + st + 46
    return adv, cs + [strut(m, (x0, 396), (x1, 454), m.h_lc * 0.9)]


def dcroat(m):
    adv, cs = lc_d.draw(m)
    xr = adv - L.sb_s(m)
    return adv, cs + [bar(m, xr - m.stem_lc - 86, adv - 16, 590, m.h_lc * 0.8)]


def hbar(m):
    adv, cs = lc_h.draw(m)
    sb, st = L.sb_s(m), m.stem_lc
    return adv, cs + [bar(m, sb - 52, sb + st + 74, 590, m.h_lc * 0.8)]


def Hbar(m):
    adv, cs = uc_H.draw(m)
    m = m.origin(360)
    dx, sb, w = 30, SB(m, "STR"), 570
    return adv + 2 * dx, shift(cs, dx) + [bar(m, sb + dx - 58, sb + dx + w + 58, 572, m.h_uc * 0.8)]


GLYPHS = [("Lslash", 0x141, Lslash), ("lslash", 0x142, lslash), ("dcroat", 0x111, dcroat),
          ("Hbar", 0x126, Hbar), ("hbar", 0x127, hbar)]
