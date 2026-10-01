"""Helpers for the Western-European additions (punctuation, maths, currency,
accents). Design coordinates are UPRIGHT (see strokes.py), m.sh slants them.
All shapes use fixed topology (no geometry-dependent point counts)."""
import math

from . import params as P
from .arcs import PI, ang_y, band, path_at, rot180, shift
from .rounds import oval
from .strokes import poly, rect, shpoly
from .superellipse import _extreme_angle, reverse


def S(m):          # capital stem
    return m.stem_uc


def H(m):          # capital horizontal stroke
    return m.h_uc


def dotd(m):       # period dot
    return m.pick(30, 104, 206)


def sbp(m):        # side bearing of punctuation
    return m.pick(70, 80, 56)


def ccw_pts(pts):
    a = sum(pts[i][0] * pts[(i + 1) % len(pts)][1] - pts[(i + 1) % len(pts)][0] * pts[i][1]
            for i in range(len(pts)))
    return pts if a > 0 else list(reversed(pts))


def pg(m, pts):
    """Polygon from upright design points (forced ccw), slanted."""
    return shpoly(m, ccw_pts(pts))


def strut(m, p0, p1, t):
    """Straight stroke of perpendicular thickness t with square ends."""
    (x0, y0), (x1, y1) = p0, p1
    L = math.hypot(x1 - x0, y1 - y0)
    nx, ny = -(y1 - y0) / L * t / 2, (x1 - x0) / L * t / 2
    return pg(m, [(x0 - nx, y0 - ny), (x1 - nx, y1 - ny), (x1 + nx, y1 + ny), (x0 + nx, y0 + ny)])


def hstrut(m, p0, p1, w):
    """Stroke with horizontal cuts and horizontal width w (like strokes.diagonal)."""
    (x0, y0), (x1, y1) = p0, p1
    return pg(m, [(x0, y0), (x0 + w, y0), (x1 + w, y1), (x1, y1)])


def sq_dot(m, cx, cy, d):
    return oval(m, (cx - d / 2, cy - d / 2, cx + d / 2, cy + d / 2), over=False)


def chevron(m, xt, cy, hh, dx, w, right=False):
    """Angle bracket: tip at xt (pointing left; right=True points right), arms
    reaching dx away, half height hh, horizontal stroke width w, horizontal cuts."""
    pts = [(xt, cy), (xt + dx, cy - hh), (xt + dx + w, cy - hh), (xt + w, cy),
           (xt + dx + w, cy + hh), (xt + dx, cy + hh)]
    if right:
        c = xt + (dx + w) / 2
        pts = [(2 * c - x, y) for x, y in pts]
    return pg(m, pts)


def peak(m, cx, y0, y1, hw, w, down=False):
    """Chevron pointing up (down=True: pointing down): legs from y0 (horizontal
    cuts, half width hw, horizontal stroke w) to the tip at y1."""
    yi = y1 - w * (y1 - y0) / hw
    pts = [(cx - hw, y0), (cx - hw + w, y0), (cx, yi), (cx + hw - w, y0), (cx + hw, y0), (cx, y1)]
    if down:
        pts = [(x, y0 + y1 - y) for x, y in pts]
    return pg(m, pts)


def sup_glyph(m, mod, k, f, dx, dy, cy0=360):
    """Draw glyph module `mod` with strokes x f, scale by k, place at (dx, dy)
    (italic: the slant axis is re-centred). Returns (advance, contours)."""
    adv, cs = mod.draw(emb(m, f))[:2]
    dx += m.s * (cy0 * k + dy - cy0)
    return adv * k, scale(cs, k, dx, dy)


def rot(m, contours, adv, ymid):
    return rot180(contours, adv, ymid)


def _tok(t, a, b, cy, en, s, side_hint=None):
    """Angle for a spec token on the ellipse (a, b, exponent en, slant s)."""
    if t == "T":
        return PI / 2
    if t == "B":
        return 1.5 * PI
    if t == "L":
        return PI + _extreme_angle(a, b, en, s)
    if t == "R":
        return _extreme_angle(a, b, en, s)
    if t == "l":            # centre height, left (slanted tangent = slant)
        return PI
    if t == "r":
        return 0.0
    kind, y = t             # ("yl", y) / ("yr", y): horizontal cut at height y
    v = (y - cy) / b
    th = ang_y(v, en)
    return (PI - th) if kind == "yl" else th


def abands(m, cx, cy, a, b, tx, ty, spec, ks, n=P.N_LETTER, over_w=True):
    """Band (closed contour) between the outer superellipse (a, b) and the inner
    (a - tx, b - ty) along the polar-angle `spec` (tokens T B L R l r or
    ("yl"|"yr", height)); angles must ascend (mod 2pi). ks[i] cubic segments
    per interval. Centre (cx, cy) in upright design space."""
    fx, fy = m.sh(cx, cy)
    a = a * (m.round_w if over_w else 1.0)
    en = m.n(n)
    paths = []
    for aa, bb in ((a, b), (a - tx, b - ty)):
        ang, prev = [], None
        for t in spec:
            th = _tok(t, aa, bb, cy, en, m.s)
            while prev is not None and th < prev - 1e-9:
                th += 2 * PI
            ang.append(th)
            prev = th
        paths.append(path_at(fx, fy, aa, bb, en, m.s, ang, ks))
    return band(*paths)


def wave(m, x0, x1, ym, amp, t, ph0=-0.35, ph1=None):
    """Tilde stroke: y = ym + amp*sin(phase), vertical thickness t, vertical end
    cuts. 4 Hermite-cubic pieces per edge, fixed topology."""
    ph1 = 2 * PI + 0.35 if ph1 is None else ph1
    k = 4
    ph = [ph0 + (ph1 - ph0) * i / k for i in range(k + 1)]
    xs = [x0 + (x1 - x0) * i / k for i in range(k + 1)]

    def edge(dy):
        segs = []
        for i in range(k):
            dx = xs[i + 1] - xs[i]
            sl = lambda j: amp * math.cos(ph[j]) * (ph1 - ph0) / (x1 - x0)
            p0 = m.sh(xs[i], ym + dy + amp * math.sin(ph[i]))
            p3 = m.sh(xs[i + 1], ym + dy + amp * math.sin(ph[i + 1]))
            p1 = m.sh(xs[i] + dx / 3, ym + dy + amp * math.sin(ph[i]) + sl(i) * dx / 3)
            p2 = m.sh(xs[i + 1] - dx / 3, ym + dy + amp * math.sin(ph[i + 1]) - sl(i + 1) * dx / 3)
            segs.append((p0, p1, p2, p3))
        return segs

    top, bot = edge(t / 2), edge(-t / 2)
    return (bot + [(bot[-1][3], top[-1][3])] + reverse(top) + [(top[0][0], bot[0][0])])


def max_x(m, contours):
    """Largest x of the outlines measured on the upright design grid."""
    return max(p[0] - m.s * (p[1] - m.y0) for c in contours for seg in c for p in seg)


def cross_tick(m, cx, y0, y1, w):
    return rect(m, cx - w / 2, y0, cx + w / 2, y1)


def anchor(m, x, y):
    """Slanted anchor position from upright design x at height y."""
    return m.sh(x, y)


def scale(contours, k, dx=0.0, dy=0.0):
    return [[tuple((x * k + dx, y * k + dy) for x, y in seg) for seg in c] for c in contours]


def emb(m, f):
    """Master with heavier strokes (f>1): draw, then scale down -> superior
    figures / letters keep a sturdier colour than plain scaling."""
    from dataclasses import replace
    return replace(m, stem_uc=m.stem_uc * f, stem_lc=m.stem_lc * f, h_uc=m.h_uc * f,
                   h_lc=m.h_lc * f, stem_dg=m.stem_dg * f, h_dg=m.h_dg * f)


__all__ = [n for n in dir() if not n.startswith("_")]
