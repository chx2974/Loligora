"""Dotted circle U+25CC: ring of 12 round dots, base for combining marks."""
import math

from .. import params as P
from ..cs_kit import sq_dot

NAME, UNI = "uni25CC", 0x25CC
ADV = 600
R = 232          # radius of the dot centres


def draw(m):
    d = m.pick(40, 62, 100)
    cx, cy = ADV / 2, P.XH / 2
    cs = []
    for i in range(12):
        a = math.pi / 6 * i
        x, y = cx + R * math.cos(a), cy + R * math.sin(a)
        cs.append(sq_dot(m, x, y, d))
    top = (cx + m.s * (P.XH - m.y0), P.XH)
    bot = (cx + m.s * (0 - m.y0), 0)
    return ADV, cs, {"top": top, "bottom": bot,
                "ogonek": (bot[0] + d / 2, 0)}
