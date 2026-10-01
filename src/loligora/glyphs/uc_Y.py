from ..arcs import shift
from ..strokes import stem
from ..uc_params import sb as SB
from ..uc_parts import buried, dw

NAME, UNI = "Y", 0x59


def draw(m):
    m = m.origin(360)
    sb, w, st = SB(m, "DIA"), m.pick(610, 630, 700), m.stem_uc
    cx, yb = w / 2, m.pick(300, 300, 330)
    wd = dw(m, cx - st / 2, 720 - yb)
    r = (cx - st / 2) / (720 - yb)
    ya = 720 - (cx + st / 2 - wd) / r
    left = buried(m, [(cx - st / 2, yb), (cx + st / 2, ya), (wd, 720), (0, 720)])
    right = buried(m, [(w - x, y) for x, y in
                       reversed([(cx - st / 2, yb), (cx + st / 2, ya), (wd, 720), (0, 720)])])
    return w + 2 * sb, shift([stem(m, cx - st / 2, 0, max(ya, yb), st), left, right], sb)
