"""Dots and stems: : ; ! ? ¡ ¿ … · •"""
import math

from .. import params as P
from ..arcs import path_at
from ..cs_kit import _tok
from ..superellipse import _node, reverse
from ..arcs import rot180
from ..cs_kit import H, abands, ccw_pts, dotd, pg, poly, rect, S, sq_dot, sbp
from . import punct_comma

W = P.PUNCT_WIDTH


def _dots(m, ys):
    d = dotd(m)
    return [sq_dot(m, W / 2, y, d) for y in ys]


def colon(m):
    d = dotd(m)
    return W, _dots(m, [d / 2, P.XH - d / 2])


def semicolon(m):
    d = dotd(m)
    adv, cs = punct_comma.draw(m)
    return W, [sq_dot(m, W / 2, P.XH - d / 2, d)] + cs


def _excl(m, cx, adv):
    """Tapered stem over a dot, centred at cx."""
    m = m.origin(360)
    d, w = dotd(m), S(m)
    top, bot = 720, d * 1.05 + m.pick(70, 110, 120)
    wb = w * 0.72
    stem = pg(m, [(cx - wb / 2, bot), (cx + wb / 2, bot), (cx + w / 2, top), (cx - w / 2, top)])
    return [stem, sq_dot(m, cx, d / 2, d)]


def exclam(m):
    d = max(dotd(m), S(m))
    adv = d + 2 * sbp(m)
    return adv, _excl(m, adv / 2, adv)


def exclamdown(m):
    adv, c = exclam(m)
    return adv, rot180(c, adv, 360)


def _isect(p, d, q, e):
    """Intersection of lines p + t d and q + u e."""
    c = d[0] * e[1] - d[1] * e[0]
    t = ((q[0] - p[0]) * e[1] - (q[1] - p[1]) * e[0]) / c
    return (p[0] + t * d[0], p[1] + t * d[1])


def _question(m, adv):
    m = m.origin(360)
    d, st = dotd(m), S(m) * m.pick(1, 0.95, 0.8)
    ty = H(m) * m.pick(1, 1, 0.8)
    b = m.pick(190, 195, 190)
    a = (adv - 2 * sbp(m)) / 2
    cx, cy = adv / 2, 720 - b + P.OVERSHOOT
    fx, fy = m.sh(cx, cy)
    a *= m.round_w
    en, s = m.n(P.N_LETTER), m.s
    ao, bo, ai, bi = a, b, a - st, b - ty
    cross = lambda u, v: u[0] * v[1] - u[1] * v[0]
    nd = lambda th, aa, bb: _node(th, fx, fy, aa, bb, en, s)
    # neck direction: tangent of the outer curve at THO (lower right)
    sr = m.sh(cx + st / 2, 0)
    sv = (m.sh(0, 1)[0] - m.sh(0, 0)[0], 1.0)
    yt = cy - b - m.pick(40, 40, 20)

    def hit(th):
        pp, tt = nd(th, ao, bo)
        return _isect(pp, tt, sr, sv)[1] - yt

    lo, hi = math.radians(-88), math.radians(-5)    # hit() falls as th rises
    for _ in range(80):
        mid = (lo + hi) / 2
        if hit(mid) > 0:
            lo = mid
        else:
            hi = mid
    tho = (lo + hi) / 2
    po, to = nd(tho, ao, bo)
    dv = (-to[0], -to[1])                       # heading down-left
    # inner curve: the parallel tangent
    f = lambda th: cross(nd(th, ai, bi)[1], dv)
    lo, hi = math.radians(-89), math.radians(-1)
    for _ in range(80):
        mid = (lo + hi) / 2
        if f(lo) * f(mid) <= 0:
            hi = mid
        else:
            lo = mid
    thi = (lo + hi) / 2
    pi = nd(thi, ai, bi)[0]
    ybot = d * m.pick(1.05, 1.05, 1.0) + m.pick(60, 100, 55)
    sl = m.sh(cx - st / 2, 0)
    rr = _isect(po, dv, sr, sv)
    ll = _isect(pi, dv, sl, sv)
    bl, br = m.sh(cx - st / 2, ybot), m.sh(cx + st / 2, ybot)
    # hook: outer from THO to the left terminal, inner likewise
    ends = []
    for aa, bb in ((ao, bo), (ai, bi)):
        ends.append(_tok(("yl", cy + 0.35 * (b - ty)), aa, bb, cy, en, s))
    pa = []
    for (aa, bb), th0, th1 in (((ao, bo), tho, ends[0]), ((ai, bi), thi, ends[1])):
        pa.append(path_at(fx, fy, aa, bb, en, s, [th0, math.pi / 2, th1], (5, 3)))
    o, i = pa
    segs = o + [(o[-1][3], i[-1][3])] + reverse(i)
    segs += [(pi, ll), (ll, bl), (bl, br), (br, rr), (rr, po)]
    return [segs, sq_dot(m, cx, d / 2, d)]


def question(m):
    adv = m.pick(470, 510, 600)
    return adv, _question(m, adv)


def questiondown(m):
    adv, c = question(m)
    return adv, rot180(c, adv, 360)


def ellipsis(m):
    d = dotd(m)
    return 3 * W, [sq_dot(m, W / 2 + i * W, d / 2, d) for i in range(3)]


def periodcentered(m):
    return W, _dots(m, [P.XH / 2])


def bullet(m):
    m = m.origin(P.XH / 2)
    d = m.pick(60, 150, 200)
    w = d + 2 * m.pick(60, 70, 70)
    return w, [sq_dot(m, w / 2, P.XH / 2, d)]


GLYPHS = [("colon", 0x3A, colon), ("semicolon", 0x3B, semicolon), ("exclam", 0x21, exclam),
          ("question", 0x3F, question), ("exclamdown", 0xA1, exclamdown),
          ("questiondown", 0xBF, questiondown), ("ellipsis", 0x2026, ellipsis),
          ("periodcentered", 0xB7, periodcentered), ("bullet", 0x2022, bullet)]
