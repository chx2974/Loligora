"""Superellipse primitive: |x/a|^n + |y/b|^n = 1 as a closed cubic contour.

Contour format used everywhere: list of segments, a segment is either a line
`(p0, p1)` or a cubic `(p0, c1, c2, p1)`; segment i ends where i+1 starts.
Outer contours run counter-clockwise, counters clockwise.

Construction (fixed topology: 4 arcs x SEGS cubics = 16 segments, so every
master and every exponent interpolates):
  * The four arc boundaries are the true extreme points of the (sheared)
    curve: top/bottom at y = +-b, left/right where the tangent is vertical
    AFTER the shear. In slanted space the curve is built directly, so on-curve
    nodes sit on the extrema (no post-shear of an upright shape).
  * Interior nodes: uniform polar angle between arc boundaries.
  * Handles: tangent from the implicit gradient. For a segment P0->P1 with
    unit tangents T0,T1 and turning angle phi, both handles run along the
    tangents to the tangent-intersection Q, of length
        k * |Q - P|,  k = (4/3) tan(phi/4) / tan(phi/2)
    (exact for a circular arc; -> 2/3 for short arcs). Flat stretches get
    chord/3 handles.
Approximation error (max |F-1| of the implicit function, 16 segments):
  n=3.0: 0.5% upright, 1.0% slanted 9 deg (~0.15% / 0.3% of the radius,
  i.e. < 1 unit at o size); n=3.3: 0.6% / 1.9%. See `max_error()` below.
"""
import math

SEGS = 4  # cubics per arc (4 arcs)


def _unit(th, n):
    c, s = math.cos(th), math.sin(th)
    r = (abs(c) ** n + abs(s) ** n) ** (-1 / n)
    return r * c, r * s


def _tangent(ux, uy, n):
    """Unit-space tangent (ccw) at unit-space point on |x|^n+|y|^n=1."""
    return (-math.copysign(abs(uy) ** (n - 1), uy),
            math.copysign(abs(ux) ** (n - 1), ux))


def _extreme_angle(a, b, n, s):
    """Polar angle in (0, pi/2) where the sheared tangent is vertical."""
    if s == 0:
        return 0.0
    lo, hi = 0.0, math.pi / 2
    for _ in range(60):
        mid = (lo + hi) / 2
        tx, ty = _tangent(*_unit(mid, n), n)
        if a * tx + s * b * ty > 0:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def _node(th, cx, cy, a, b, n, s):
    ux, uy = _unit(th, n)
    tx, ty = _tangent(ux, uy, n)
    x, y = a * ux, b * uy
    t = (a * tx + s * b * ty, b * ty)
    ln = math.hypot(*t)
    return (cx + x + s * y, cy + y), (t[0] / ln, t[1] / ln)


def _segment(p0, t0, p1, t1):
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    chord = math.hypot(dx, dy)
    cr = t0[0] * t1[1] - t0[1] * t1[0]
    h0 = h1 = chord / 3
    if abs(cr) > 1e-6:
        u = (dx * t1[1] - dy * t1[0]) / cr
        v = (dx * t0[1] - dy * t0[0]) / cr
        if u > 0 and v > 0:
            phi = math.atan2(abs(cr), t0[0] * t1[0] + t0[1] * t1[1])
            k = (4 / 3) * math.tan(phi / 4) / math.tan(phi / 2)
            h0, h1 = k * u, k * v
    return (p0, (p0[0] + t0[0] * h0, p0[1] + t0[1] * h0),
            (p1[0] - t1[0] * h1, p1[1] - t1[1] * h1), p1)


def superellipse(cx, cy, a, b, n=3.0, s=0.0):
    """Closed ccw contour; (cx, cy) = final centre, s = tan(slant).

    Starts at the right-hand extreme node (vertical tangent)."""
    tr = _extreme_angle(a, b, n, s)
    bounds = [tr, math.pi / 2, math.pi + tr, 1.5 * math.pi, 2 * math.pi + tr]
    angles = []
    for i in range(4):
        for j in range(SEGS):
            angles.append(bounds[i] + (bounds[i + 1] - bounds[i]) * j / SEGS)
    angles.append(bounds[4])
    nodes = [_node(t, cx, cy, a, b, n, s) for t in angles]
    nodes[-1] = nodes[0]                       # close exactly (no float gap)
    return [_segment(*nodes[i], *nodes[i + 1]) for i in range(len(nodes) - 1)]


def reverse(contour):
    return [tuple(reversed(seg)) for seg in reversed(contour)]


def max_error(n=3.0, s=0.0, a=300.0, b=270.0, samples=40):
    """Max |F-1| over the curve, F = |x/a|^n+|y/b|^n in unsheared coords."""
    worst = 0.0
    for seg in superellipse(0, 0, a, b, n, s):
        for i in range(samples + 1):
            t = i / samples
            m = 1 - t
            x = sum(w * p[0] for w, p in zip((m**3, 3*m*m*t, 3*m*t*t, t**3), seg))
            y = sum(w * p[1] for w, p in zip((m**3, 3*m*m*t, 3*m*t*t, t**3), seg))
            x -= s * y
            worst = max(worst, abs(abs(x / a) ** n + abs(y / b) ** n - 1))
    return worst


def ring(cx, cy, a, b, tx, ty, n=3.0, s=0.0):
    """Outer superellipse (ccw) + counter (cw). tx = stroke thickness on the
    left/right sides, ty = on top/bottom. Counter is a superellipse of radii
    (a - tx, b - ty) about the same centre."""
    return [superellipse(cx, cy, a, b, n, s),
            reverse(superellipse(cx, cy, a - tx, b - ty, n, s))]


if __name__ == "__main__":
    for n in (2.0, 2.85, 3.0, 3.3):
        print(n, "upright %.4f" % max_error(n), "slant %.4f" % max_error(n, 0.158))
