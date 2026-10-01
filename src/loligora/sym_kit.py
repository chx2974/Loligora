"""Helpers for the symbol redraws ([sym]): reversed-C rings, leaning strokes."""
from .arcs import cring, rot180


def back_c(m, box, tx, ty, y_low, y_up=None, n=3.0):
    """Reversed C (opens to the LEFT): the upper-left end stops at the left
    extreme (height = ring centre, bury it in a stem), the lower-left end is a
    horizontal terminal at y_low. box is used as is (no overshoot). Fixed topology."""
    x0, y0, x1, y1 = box
    cy = (y0 + y1) / 2
    cx = (x0 + x1) / 2
    fx, _ = m.sh(cx, cy)
    c = cring(m, box, tx, ty, 2 * cy - y_low, y_up if y_up is not None else cy,
              over=False, n=n)
    return rot180([c], 2 * fx, cy)[0]


def lean(contours, k, y_pivot):
    """Extra shear x += k*(y - y_pivot) on finished contours (affine, so exact
    for cubics); horizontal edges stay horizontal."""
    f = lambda p: (p[0] + k * (p[1] - y_pivot), p[1])
    return [[tuple(f(p) for p in seg) for seg in c] for c in contours]


def arcp(m, cx, cy, a, b, tx, ty, bounds, ks, n=3.0):
    """Band (closed contour) between outer ring (a, b) and inner ring (a-tx,
    b-ty) along polar-angle `bounds` (ascending radians; the slanted extreme
    nodes are given as base + 'tr' via the callable form: an entry may be a
    tuple (angle, 'tr') meaning angle + tr). Same cut angles on both rings."""
    from .arcs import band, path_at
    from .superellipse import _extreme_angle
    fx, fy = m.sh(cx, cy)
    a = a * m.round_w
    en = m.n(n)
    paths = []
    for aa, bb in ((a, b), (a - tx, b - ty)):
        tr = _extreme_angle(aa, bb, en, m.s)
        bs = [v[0] + tr if isinstance(v, tuple) else v for v in bounds]
        paths.append(path_at(fx, fy, aa, bb, en, m.s, bs, ks))
    return band(*paths)


def arcy(m, cx, cy, a, b, tx, ty, start, end, ks, n=3.0):
    """Band like `arcp` but for the bottom-left -> top-left sweep (ccw through
    the bottom, right side, top) of a ring. `start` is ('y', y_cut) for a
    horizontal terminal cut on the lower left (each ring gets its own angle) or
    ('a', angle_from_bottom) for a radial end; `end` likewise with ('x', x_cut)
    (upper-left end at x = x_cut, radial) or ('a', angle). Fixed topology."""
    from math import pi
    from .arcs import band, path_at, theta_at, theta_at_y
    from .superellipse import _extreme_angle
    fx, fy = m.sh(cx, cy)
    a = a * m.round_w
    en = m.n(n)
    paths = []
    for aa, bb in ((a, b), (a - tx, b - ty)):
        tr = _extreme_angle(aa, bb, en, m.s)
        if start[0] == 'y':
            s = pi + theta_at_y(min(0.97, (cy - start[1]) / bb), en)
        elif start[0] == 'x':
            s = 2 * pi - theta_at((start[1] - cx) / a, en)
        else:
            s = 1.5 * pi - start[1]
        if end[0] == 'x':
            e = 2 * pi + theta_at((end[1] - cx) / a, en)
        elif end[0] == 'L':
            e = 3 * pi + tr
        else:
            e = 2.5 * pi + end[1]
        paths.append(path_at(fx, fy, aa, bb, en, m.s, [s, 1.5 * pi, 2 * pi + tr, 2.5 * pi, e], ks))
    return band(*paths)


def arcz(m, cx, cy, a, b, tx, ty, y_start, y_end, ks, n=3.0):
    """Band from a horizontal cut on the upper RIGHT (height y_start) ccw over
    the top, the left side and the bottom to a horizontal cut on the lower
    RIGHT (height y_end < cy). Each ring gets its own angle so both cuts are
    flat. Fixed topology."""
    from math import pi
    from .arcs import band, path_at, theta_at_y
    from .superellipse import _extreme_angle
    fx, fy = m.sh(cx, cy)
    a = a * m.round_w
    en = m.n(n)
    paths = []
    for aa, bb in ((a, b), (a - tx, b - ty)):
        tr = _extreme_angle(aa, bb, en, m.s)
        s = theta_at_y(min(0.97, (y_start - cy) / bb), en)
        e = 2 * pi - theta_at_y(min(0.97, (cy - y_end) / bb), en)
        paths.append(path_at(fx, fy, aa, bb, en, m.s,
                             [s, pi / 2, pi + tr, 1.5 * pi, e], ks))
    return band(*paths)


def s_mini(m, x0, x1, ym, ytop, tx, ty, yt, n=3.0):
    """Small S (as uc_parts.s_shape) with a free top: two point-symmetric
    C-arcs meeting at the spine (centre ym), top of the upper arc at ytop,
    upper-right terminal cut at height yt. Fixed topology."""
    from .arcs import PI, ang_y, path_at, snap
    from .superellipse import _extreme_angle, reverse
    from .uc_parts import geom
    ylow = ym - ty / 2
    fx, fy, a, b = geom(m, x0, ylow, x1, ytop)
    en = m.n(n)
    arcs = []
    for aa, bb in ((a, b), (a - tx, b - ty)):
        tr = _extreme_angle(aa, bb, en, m.s)
        arcs.append(path_at(fx, fy, aa, bb, en, m.s,
                            [ang_y((yt - fy) / bb, en), PI / 2, PI + tr, 1.5 * PI],
                            (2, 4, 4)))
    o, i = arcs
    bo, bi = o[-1][3], i[-1][3]
    cx, cy = (bo[0] + bi[0]) / 2, (bo[1] + bi[1]) / 2
    rp = lambda p: (2 * cx - p[0], 2 * cy - p[1])
    refl = lambda path: [tuple(rp(p) for p in seg) for seg in path]
    ro, ri = refl(o), refl(i)
    c = (o + reverse(ri) + [(ri[0][0], ro[0][0])] + ro + reverse(i)
         + [(i[0][0], o[0][0])])
    return snap(c)
