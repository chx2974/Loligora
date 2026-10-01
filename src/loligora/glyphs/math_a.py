"""Tabular maths (all 580 wide): + − = < > ± × ÷ ¬ and figure space."""
import math

from .. import params as P
from ..cs_kit import H, S, chevron, pg, rect, sq_dot, strut, dotd

W = P.DIGIT_WIDTH
AX = 268                 # maths axis
LEN = 400                # bar length


def _hb(m, y, x0=None, x1=None, h=None):
    h = h or H(m) * 0.95
    x0 = (W - LEN) / 2 if x0 is None else x0
    x1 = W - x0 if x1 is None else x1
    return rect(m, x0, y - h / 2, x1, y + h / 2)


def _plus(m, cy, size=LEN):
    t = H(m) * 1.0
    size = size + m.pick(0, 0, 40)
    x0 = (W - size) / 2
    return [_hb(m, cy, x0, W - x0), rect(m, W / 2 - t / 2, cy - size / 2, W / 2 + t / 2, cy + size / 2)]


def plus(m):
    return W, _plus(m.origin(AX), AX)


def minus(m):
    return W, [_hb(m.origin(AX), AX)]


def equal(m):
    m = m.origin(AX)
    g = m.pick(120, 130, 190)
    return W, [_hb(m, AX + g / 2), _hb(m, AX - g / 2)]


def less(m, right=False):
    m = m.origin(AX)
    w, dx, hh = H(m) * 1.05, 250, m.pick(170, 175, 190)
    xt = (W - dx - w) / 2
    return W, [chevron(m, xt, AX, hh, dx, w, right)]


def greater(m):
    return less(m, True)


def plusminus(m):
    m = m.origin(AX)
    return W, _plus(m, AX + 90, 360) + [_hb(m, AX - 210, (W - 360) / 2, W - (W - 360) / 2)]


def multiply(m):
    m = m.origin(AX)
    r, t = 150, H(m) * m.pick(1.0, 0.95, 0.85)
    c = W / 2
    return W, [strut(m, (c - r, AX - r), (c + r, AX + r), t), strut(m, (c - r, AX + r), (c + r, AX - r), t)]


def divide(m):
    m = m.origin(AX)
    d = dotd(m) * m.pick(1.0, 0.95, 0.8)
    return W, [_hb(m, AX), sq_dot(m, W / 2, AX + 125 + d / 2, d), sq_dot(m, W / 2, AX - 125 - d / 2, d)]


def logicalnot(m):
    m = m.origin(AX)
    t = S(m) * 0.9
    x0, x1 = (W - LEN) / 2, W - (W - LEN) / 2
    return W, [_hb(m, AX + 40, x0, x1), rect(m, x1 - t, AX + 40 - 150, x1, AX + 40 + H(m) * 0.475)]


def figurespace(m):
    return W, []


GLYPHS = [("plus", 0x2B, plus), ("minus", 0x2212, minus), ("equal", 0x3D, equal),
          ("less", 0x3C, less), ("greater", 0x3E, greater), ("plusminus", 0xB1, plusminus),
          ("multiply", 0xD7, multiply), ("divide", 0xF7, divide), ("logicalnot", 0xAC, logicalnot),
          ("figurespace", 0x2007, figurespace)]
