from ..strokes import rect
from ..superellipse import reverse

NAME, UNI = ".notdef", None


def draw(m):
    t = m.stem_uc * 0.6
    ht = m.h_uc * 0.6
    outer = rect(m, 60, 0, 540, 720)
    inner = reverse(rect(m, 60 + t, ht, 540 - t, 720 - ht))
    return 600, [outer, inner]
