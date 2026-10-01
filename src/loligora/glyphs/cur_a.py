"""Currency (all 580 wide, tabular): $ ¢ € £ ¥ ¤ ƒ"""
import math

from .. import lc_params as L
from .. import params as P
from ..arcs import cring
from ..cs_kit import H, S, abands, hstrut, pg, rect, strut
from ..lc_curls import hook, tail
from ..rounds import oval_ring
from ..strokes import bar
from ..uc_parts import s_shape

W = P.DIGIT_WIDTH


def dollar(m):
    m = m.origin(360)
    sb = m.pick(80, 72, 58)
    t = S(m) * 0.62
    s1 = s_shape(m, sb, W - sb, 360, S(m) * 0.96, H(m), m.pick(570, 566, 570))
    return W, [s1, rect(m, W / 2 - t / 2, -150, W / 2 + t / 2, 60),
               rect(m, W / 2 - t / 2, 660, W / 2 + t / 2, 870)]


def cent(m):
    m = m.origin(360)
    sb, t = m.pick(75, 70, 55), S(m) * 0.62
    c = cring(m, (sb, 60, W - sb, 680), S(m) * 0.92, H(m) * 0.95, 460, 260, over=False)
    return W, [c, rect(m, W / 2 - t / 2, -140, W / 2 + t / 2, 130),
               rect(m, W / 2 - t / 2, 610, W / 2 + t / 2, 860)]


def euro(m):
    m = m.origin(360)
    sb, h = m.pick(50, 45, 36), H(m) * m.pick(0.9, 0.9, 0.6)
    c = cring(m, (sb + 20, 0, W - sb, 720), S(m) * 0.92, H(m) * 0.95, 500, 215)
    y1, y2 = m.pick(330, 325, 330), m.pick(200, 200, 205)
    return W, [c, rect(m, 25, y1, 360, y1 + h), rect(m, 25, y2, 360, y2 + h)]


def sterling(m):
    m = m.origin(360)
    t, h = S(m) * 0.95, H(m) * 0.95
    xs = m.pick(140, 130, 110)
    b, xr = m.pick(170, 175, 190), W - m.pick(80, 75, 60)
    a = (xr - xs) / 2
    cy = 720 + P.OVERSHOOT - b
    k = 0.3 * (b - h)
    top = abands(m, xs + a, cy, a, b, t, h, [("yr", cy - k), "T", "l"], (4, 3))
    return W, [top, rect(m, xs, 0, xs + t, cy), rect(m, xs - 55, 0, xr + 20, h),
               rect(m, xs - 60, 300, xs + t + 60, 300 + h)]


def yen(m):
    m = m.origin(360)
    st, h = S(m) * 0.95, H(m) * 0.75
    w = st * m.pick(1.0, 0.95, 0.8) * 1.15
    cx, x0, x1 = W / 2, m.pick(50, 45, 36), W - m.pick(50, 45, 36)
    y1, y2 = m.pick(215, 200, 190), m.pick(345, 335, 345)
    return W, [hstrut(m, (x0, 720), (cx - w / 2, 300), w), hstrut(m, (x1 - w, 720), (cx - w / 2, 300), w),
               rect(m, cx - st / 2, 0, cx + st / 2, 340), rect(m, 110, y1, W - 110, y1 + h),
               rect(m, 110, y2, W - 110, y2 + h)]


def currency(m):
    m = m.origin(345)
    t, r = H(m) * m.pick(0.9, 0.9, 0.62), m.pick(125, 130, 150)
    cx, cy = W / 2, 345
    out = oval_ring(m, (cx - r, cy - r, cx + r, cy + r), t, t, over=False)
    for a in (45, 135, 225, 315):
        c, s = math.cos(math.radians(a)), math.sin(math.radians(a))
        out.append(strut(m, (cx + c * (r - t * 0.4), cy + s * (r - t * 0.4)),
                         (cx + c * (r + 85), cy + s * (r + 85)), t))
    return W, out


def florin(m):
    st, hb = m.stem_lc, m.h_lc * 0.95
    xs = 250
    top = P.ASC + P.OVERSHOOT
    r = L.tail_v(m)
    xf = xs + st + L.tail_ext(m) - 20
    h = hook(m, 1, xs, xf, top - r, top, top - r + 12, st, L.term(m), hb, 0)
    xj = xs + st
    xfj = xj - st - L.tail_ext(m) + 10
    cy = P.DESC + L.tail_v(m) * 0.9
    t = tail(m, -1, xj, xfj, cy, P.DESC - P.OVERSHOOT, cy - 12, st, L.term(m), hb, 120)
    return W, [h, t, bar(m, xs - 110, xs + st + 110, P.XH - hb, hb)]


GLYPHS = [("dollar", 0x24, dollar), ("cent", 0xA2, cent), ("Euro", 0x20AC, euro),
          ("sterling", 0xA3, sterling), ("yen", 0xA5, yen), ("currency", 0xA4, currency),
          ("florin", 0x192, florin)]
