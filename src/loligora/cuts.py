"""Bezier utilities: splitting a cubic and finding where a contour crosses a height.

Building open rings / arches by cutting finished contours was removed: the
segment index of a crossing differs between masters, so point counts did too.
Use arcs.py (polar-angle arcs, fixed topology) and rounds.oval_c / oval_arch.
"""


def _lerp(a, b, t):
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


def split(seg, t):
    """de Casteljau split of a cubic at t -> (left, right)."""
    p0, p1, p2, p3 = seg
    a, b, c = _lerp(p0, p1, t), _lerp(p1, p2, t), _lerp(p2, p3, t)
    d, e = _lerp(a, b, t), _lerp(b, c, t)
    f = _lerp(d, e, t)
    return (p0, a, d, f), (f, e, c, p3)


def sub(seg, t0, t1):
    """Part of a cubic between parameters t0 < t1."""
    right = split(seg, t0)[1] if t0 > 0 else seg
    if t1 >= 1:
        return right
    return split(right, (t1 - t0) / (1 - t0))[0]


def _y(seg, t):
    m = 1 - t
    return (m**3 * seg[0][1] + 3*m*m*t * seg[1][1]
            + 3*m*t*t * seg[2][1] + t**3 * seg[3][1])


def locate_y(seg, y, samples=40):
    """Parameter where the cubic crosses height y (first crossing), or None."""
    prev = _y(seg, 0) - y
    for i in range(1, samples + 1):
        t = i / samples
        cur = _y(seg, t) - y
        if prev == 0:
            return (i - 1) / samples
        if prev * cur < 0:
            lo, hi = (i - 1) / samples, t
            for _ in range(50):
                mid = (lo + hi) / 2
                if (_y(seg, mid) - y) * prev > 0:
                    lo = mid
                else:
                    hi = mid
            return (lo + hi) / 2
        prev = cur
    return None


def crossing(contour, y, xc, right=True):
    """(segment index, t) where the contour crosses height y on the right
    (x >= xc) or left (x < xc) side."""
    for i, seg in enumerate(contour):
        t = locate_y(seg, y)
        if t is not None and (split(seg, t)[0][3][0] >= xc) == right:
            return i, t
    raise ValueError("no crossing at y=%s" % y)
