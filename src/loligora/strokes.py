"""Straight-stroke helpers: stems, bars, diagonals, polygons, join thinning.

All take the Master `m` and design coordinates in UPRIGHT space (x measured
at the shear origin height m.y0); `m.sh` slants them. Vertical edges become
slanted, horizontal edges (bar tops, stem feet, terminals) stay horizontal.
Contours are ccw; segment format is described in superellipse.py.
"""


def poly(pts):
    """Closed polygon (list of points) -> contour of line segments."""
    return [(pts[i], pts[(i + 1) % len(pts)]) for i in range(len(pts))]


def shpoly(m, pts):
    """Polygon from upright design points, slanted by the master."""
    return poly([m.sh(x, y) for x, y in pts])


def rect(m, x0, y0, x1, y1):
    """Axis-aligned (upright) rectangle; slanted sides in italic."""
    return shpoly(m, [(x0, y0), (x1, y0), (x1, y1), (x0, y1)])


def stem(m, x, y0, y1, w):
    """Vertical stem with left edge x and width w (horizontal measure)."""
    return rect(m, x, y0, x + w, y1)


def bar(m, x0, x1, y, h):
    """Horizontal bar: bottom edge y, thickness h."""
    return rect(m, x0, y, x1, y + h)


def diagonal(m, p0, p1, w):
    """Diagonal from foot p0 to head p1, horizontal cuts, horizontal width w."""
    (x0, y0), (x1, y1) = p0, p1
    return shpoly(m, [(x0, y0), (x0 + w, y0), (x1 + w, y1), (x1, y1)])


def thin(w, k=0.86):
    """Join thinning: stroke thickness where a round meets a stem."""
    return w * k


def shear_contours(contours, s, y0=0.0):
    """Naive shear of finished contours (only for line-only shapes; rounds
    must be built slanted via superellipse(s=...))."""
    def f(p):
        return (p[0] + s * (p[1] - y0), p[1])
    return [[tuple(f(p) for p in seg) for seg in c] for c in contours]


def zpoly(m, w, top, h, wd, x0=0.0, y0=0.0):
    """One-piece Z: bars of thickness h between y0 and top, diagonal of
    horizontal width wd whose outer edges end exactly on the bars' outer
    corners (x0, y0+h) and (x0+w, top-h). Single ccw contour, 10 vertices."""
    x1, y1 = x0 + w, top
    return shpoly(m, [(x0, y0), (x1, y0), (x1, y0 + h), (x0 + wd, y0 + h),
                      (x1, y1 - h), (x1, y1), (x0, y1), (x0, y1 - h),
                      (x1 - wd, y1 - h), (x0, y0 + h)])


def npoly(m, w, top, wd, st, x0=0.0):
    """One-piece N (10 vertices, ccw): stems of width st, diagonal of horizontal
    width wd whose edges end exactly on the stems and on the flat cuts."""
    x1 = x0 + w
    xa = x0 + w - wd                              # diagonal foot left edge at y=0
    ya = top * (1 - st / (w - wd))                # lower-left edge meets left stem
    yb = top * (1 - (w - st - wd) / (w - wd))     # upper-right edge meets right stem
    return shpoly(m, [(x0, 0), (x0 + st, 0), (x0 + st, ya), (xa, 0), (x1, 0),
                      (x1, top), (x1 - st, top), (x1 - st, yb), (x0 + wd, top),
                      (x0, top)])


def xpoly(m, w, top, wd, x0=0.0):
    """One-piece X (12 vertices, ccw): flat cuts at y=0 and y=top, all crossing
    vertices computed from the two diagonals' edges."""
    s = (w - wd) / top
    yt, yb = top / 2 + wd / (2 * s), top / 2 - wd / (2 * s)
    x1 = x0 + w
    return shpoly(m, [(x0, 0), (x0 + wd, 0), (x0 + w / 2, yb), (x1 - wd, 0), (x1, 0),
                      (x0 + (w + wd) / 2, top / 2), (x1, top), (x1 - wd, top),
                      (x0 + w / 2, yt), (x0 + wd, top), (x0, top),
                      (x0 + (w - wd) / 2, top / 2)])


def kpoly(m, w, st, top_stem, top_arm, ya, px, wa, wl, x0=0.0):
    """One-piece K (12 vertices, ccw). Stem [x0, x0+st] up to top_stem. The arm's
    underside runs from the stem at height ya to the top-right corner
    (x0+w, top_arm); its upper edge is parallel, horizontal width wa. The leg's
    upper-right edge runs from the foot corner (x0+w, 0) to the point P on the
    arm underside px right of the stem; its lower-left edge (horizontal width wl)
    ends on the arm underside at Q. Returns (contour, Q.x - stem edge)."""
    xs = x0 + st
    rx = (w - st) / (top_arm - ya)                # arm underside dx/dy
    ux = lambda y: xs + (y - ya) * rx             # underside x at height y
    yp = ya + px / rx
    xp = xs + px
    # leg edges: x = x1 - kx*y  (upper-right), x - wl (lower-left)
    kx = (x0 + w - xp) / yp
    # lower-left edge: x = x0+w-wl - kx*y meets underside ux(y)
    yq = (x0 + w - wl - xs + ya * rx) / (rx + kx)
    xq = ux(yq)
    yu = ya + wa / rx
    pts = [(x0, 0), (xs, 0), (xs, ya), (xq, yq), (x0 + w - wl, 0), (x0 + w, 0),
           (xp, yp), (x0 + w, top_arm), (x0 + w - wa, top_arm), (xs, yu),
           (xs, top_stem), (x0, top_stem)]
    return shpoly(m, pts), xq - xs
