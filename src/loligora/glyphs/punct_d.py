"""Angle quotes, daggers, section, pilcrow, asterisk, number sign: ‹ › « » † ‡ § ¶ * #"""
from .. import params as P
from ..arcs import rot180
from ..cs_kit import H, S, chevron, pg, rect, sbp, strut, hstrut
from ..rounds import oval, oval_ring
from ..uc_parts import s_shape


def _chev(m, n, right):
    m = m.origin(P.XH / 2)
    dx, hh, w = m.pick(140, 150, 175), m.pick(150, 155, 165), m.pick(22, 78, 130)
    sb, gap = m.pick(50, 55, 45), m.pick(20, 26, 30)
    step = dx + w * 0.5 + gap
    xs = [sb + i * step for i in range(n)]
    cs = [chevron(m, x, P.XH / 2, hh, dx, w, right) for x in xs]
    return sb * 2 + (n - 1) * step + dx + w, cs


def dagger(m, double=False):
    m = m.origin(360)
    st, h, sb = S(m) * 0.9, H(m) * 0.95, sbp(m)
    w = m.pick(300, 330, 380)
    cx = sb + w / 2
    yb = 470
    out = [rect(m, cx - st / 2, -140, cx + st / 2, 720), rect(m, sb, yb, sb + w, yb + h)]
    if double:
        out.append(rect(m, sb, 60, sb + w, 60 + h))
    return w + 2 * sb, out


def doubledagger(m):
    return dagger(m, True)


def section(m):
    """Two small S strokes stacked and interlocking (top one turned around the
    glyph centre for the bottom), terminals tucked into the opposite bowl."""
    from ..sym_kit import s_mini
    m = m.origin(360)
    w, sb = m.pick(360, 380, 500), m.pick(60, 60, 46)
    t, h = S(m) * m.pick(0.85, 0.6, 0.42), H(m) * m.pick(0.85, 0.6, 0.38)
    ytop, ylow = 720 + P.OVERSHOOT + 20, 360 - h * 0.5
    ym = (ytop + ylow) / 2
    up = s_mini(m, sb, sb + w, ym, ytop, t, h, ytop - 135)
    low = rot180([up], w + 2 * sb, 360)
    return w + 2 * sb, [up] + low


def paragraph(m):
    m = m.origin(360)
    st, sb = S(m) * m.pick(0.9, 0.8, 0.4), m.pick(50, 50, 40)
    h = H(m) * m.pick(0.9, 0.8, 0.4)
    w = m.pick(470, 530, 600)
    x2 = sb + w - st
    x1 = x2 - st - m.pick(30, 40, 50)
    b = oval_ring(m, (sb, 310, x1 + st, 720), st, h, n=3, over=False)
    return w + 2 * sb, b + [rect(m, x1, -100, x1 + st, 720), rect(m, x2, -100, x2 + st, 720)]


def asterisk(m):
    m = m.origin(600)
    t, sb, r = S(m) * m.pick(0.9, 0.85, 0.55), m.pick(40, 45, 40), m.pick(150, 160, 175)
    cx, cy = sb + r, 570
    import math
    cs = [strut(m, (cx + r * math.cos(a), cy + r * math.sin(a)),
                (cx - r * math.cos(a), cy - r * math.sin(a)), t)
          for a in (math.pi / 2, math.pi / 6, 5 * math.pi / 6)]
    return 2 * (sb + r), cs


def numbersign(m):
    m = m.origin(360)
    st, h, sb = S(m) * 0.7, H(m) * 0.8, 40
    dx = 40
    out = [hstrut(m, (sb + 80, 0), (sb + 80 + dx + 60, 720), st),
           hstrut(m, (sb + 250, 0), (sb + 250 + dx + 60, 720), st)]
    out += [rect(m, sb, 220, 580 - sb, 220 + h), rect(m, sb, 470, 580 - sb, 470 + h)]
    return P.DIGIT_WIDTH, out


GLYPHS = [("guilsinglleft", 0x2039, lambda m: _chev(m, 1, False)),
          ("guilsinglright", 0x203A, lambda m: _chev(m, 1, True)),
          ("guillemotleft", 0xAB, lambda m: _chev(m, 2, False)),
          ("guillemotright", 0xBB, lambda m: _chev(m, 2, True)),
          ("dagger", 0x2020, dagger), ("daggerdbl", 0x2021, doubledagger),
          ("section", 0xA7, section), ("paragraph", 0xB6, paragraph),
          ("asterisk", 0x2A, asterisk), ("numbersign", 0x23, numbersign)]
