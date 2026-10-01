from ..arcs import cring
from ..fig_parts import ccw
from ..strokes import poly
from ..uc_params import sb as SB

NAME, UNI = "G", 0x47


def _cross0(ring, xr):
    """x (right half) where the ring contour crosses y=0 going up, by sampling."""
    best = xr
    for sg in ring:
        if len(sg) != 4:
            continue
        pts = [tuple(sum(b * p[k] for b, p in zip((u ** 3, 3 * u * u * (1 - u), 3 * u * (1 - u) ** 2, (1 - u) ** 3), sg[::-1])) for k in (0, 1))
               for u in [i / 200 for i in range(201)]]
        for a, b in zip(pts, pts[1:]):
            if a[1] < 0 <= b[1] or b[1] < 0 <= a[1]:
                x = a[0] + (b[0] - a[0]) * (0 - a[1]) / (b[1] - a[1])
                if x > 400:
                    best = min(best, x)
    return best


def draw(m):
    m = m.origin(360)
    l, r, w, st, h = SB(m, "RND"), SB(m, "RND"), 630, m.stem_uc, m.h_uc
    yt = m.pick(540, 536, 546)
    yb = 370                                  # top of the bar / spur stem
    ring = cring(m, (l, -12, l + w, 732), st, h, yt, yb, over=False, optical=False)
    xr = l + w
    hb, ws = h * m.pick(1, 1, 0.8), st * m.pick(1, 1, 0.86)
    xb = l + w * 0.52
    # right edge flush with the ring's true extreme (cubic nodes overshoot by ~2u)
    xr = max(p[0] for sg in ring for p in sg)
    xc = _cross0(ring, xr)                    # where the ring's outer edge rises through y=0
    # bar + spur stem as ONE polygon: same right edge, foot merges into the ring curve
    spur = ccw(poly([m.sh(xb, yb - hb), m.sh(xr - ws, yb - hb), (xr - ws if m.weight_name != "ExtraBlack" else min(xc, xr - ws), 0),
                     (xr, 0), m.sh(xr, yb), m.sh(xb, yb)]))
    return w + l + r, [ring, spur]
