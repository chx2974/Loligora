import math

from ..arcs import shift
from ..strokes import zpoly
from ..uc_params import sb as SB

NAME, UNI = "Z", 0x5A


def draw(m):
    """One-piece Z; diagonal thinned optically (k x stem, perpendicular)."""
    m = m.origin(360)
    sb, w, h = SB(m, "OPN"), m.pick(520, 540, 600), m.h_uc
    k = m.pick(1.0, 0.94, 0.86) * m.stem_uc
    dy, wd = 720 - 2 * h, m.stem_uc
    for _ in range(20):                       # wd = k * hypot(dx, dy) / dy, dx = w - wd
        wd = k * math.hypot(w - wd, dy) / dy
    return w + 2 * sb, shift([zpoly(m, w, 720, h, wd)], sb)
