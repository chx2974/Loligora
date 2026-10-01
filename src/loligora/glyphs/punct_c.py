"""Brackets and slashes: ( ) [ ] { } / \\"""
from ..arcs import rot180
from ..cs_kit import abands, max_x, H, S, dotd, hstrut, pg, rect, sbp

Y0, Y1 = -140, 760          # bracket extent
YC = (Y0 + Y1) / 2


def _paren(m):
    m = m.origin(360)
    t = S(m) * 0.62 if m.wght > 300 else S(m) * 0.9
    ty = min(H(m) * 0.5, 40)
    a, b = m.pick(170, 175, 200), 520
    sb = m.pick(70, 70, 56)
    k = 0.86
    cx = sb + a
    c = abands(m, cx, YC, a, b, t, ty, [("yl", YC + k * (b - ty)), "L", ("yl", YC - k * (b - ty))],
               (4, 4))
    adv = max_x(m, [c]) + sb
    return adv, [c]


def parenleft(m):
    return _paren(m)


def parenright(m):
    adv, c = _paren(m)
    return adv, rot180(c, adv, YC)


def _bracket(m):
    m = m.origin(360)
    t, h, sb = S(m) * 0.85, H(m) * 0.95, m.pick(80, 80, 60)
    arm = m.pick(190, 200, 230)
    x0, x1 = sb, sb + arm
    pts = [(x0, Y0), (x1, Y0), (x1, Y0 + h), (x0 + t, Y0 + h), (x0 + t, Y1 - h),
           (x1, Y1 - h), (x1, Y1), (x0, Y1)]
    return arm + 2 * sb, [pg(m, pts)]


def bracketleft(m):
    return _bracket(m)


def bracketright(m):
    adv, c = _bracket(m)
    return adv, rot180(c, adv, YC)


def _brace(m):
    """Upright `{`: hook, stem, quarter, half-ring tip, quarter, stem, hook."""
    m = m.origin(360)
    t = m.pick(22, 66, 112)
    rr, r2, arm = m.pick(96, 100, 150), m.pick(70, 90, 132), m.pick(50, 60, 60)
    sb = m.pick(60, 60, 50)
    xt = sb                                # leftmost point of the tip
    xa = xt + rr + r2 - t                  # stem left edge
    c1x = xa + t - rr                      # quarter-ring centres x (= tip ring x)
    ct = YC                                # tip ring centre y
    c1y = ct + r2 - t + rr                 # upper quarter ring centre
    c2y = ct - r2 + t - rr                 # lower quarter ring centre
    q = lambda cx, cy, r, spec, ks: abands(m, cx, cy, r, r, t, t, spec, ks)
    ch = q(xa + rr, Y1 - rr, rr, ["T", "l"], (3,))            # top hook
    q1 = q(c1x, c1y, rr, ["B", "r"][::1], (3,))               # stem -> west
    tip = q(c1x, ct, r2, ["T", "L", "B"], (3, 3))
    q2 = q(c1x, c2y, rr, ["r", "T"], (3,))                    # east -> stem
    cb = q(xa + rr, Y0 + rr, rr, ["l", "B"], (3,))            # bottom hook
    arm_t = rect(m, xa + rr - 4, Y1 - t, xa + rr + arm, Y1)
    arm_b = rect(m, xa + rr - 4, Y0, xa + rr + arm, Y0 + t)
    s1 = rect(m, xa, c1y, xa + t, Y1 - rr)
    s2 = rect(m, xa, Y0 + rr, xa + t, c2y)
    adv = xa + rr + arm + sb
    return adv, [ch, arm_t, s1, q1, tip, q2, s2, cb, arm_b]


def braceleft(m):
    return _brace(m)


def braceright(m):
    adv, c = _brace(m)
    return adv, rot180(c, adv, YC)


def slash(m):
    m = m.origin(360)
    w, sb = S(m) * 0.62, m.pick(24, 24, 20)
    dx = m.pick(300, 320, 340)
    return dx + w + 2 * sb, [hstrut(m, (sb, -30), (sb + dx, 750), w)]


def backslash(m):
    m = m.origin(360)
    w, sb = S(m) * 0.62, m.pick(24, 24, 20)
    dx = m.pick(300, 320, 340)
    return dx + w + 2 * sb, [hstrut(m, (sb + dx, -30), (sb, 750), w)]


GLYPHS = [("parenleft", 0x28, parenleft), ("parenright", 0x29, parenright),
          ("bracketleft", 0x5B, bracketleft), ("bracketright", 0x5D, bracketright),
          ("braceleft", 0x7B, braceleft), ("braceright", 0x7D, braceright),
          ("slash", 0x2F, slash), ("backslash", 0x5C, backslash)]
