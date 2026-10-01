from .. import params as P
from ..rounds import oval
from ..strokes import shpoly
from .punct_period import dot_size

NAME, UNI = "comma", 0x2C


def draw(m):
    d, c = dot_size(m), P.PUNCT_WIDTH / 2
    # squared tail: flat bottom, right edge sweeping left, left edge near vertical
    # Thin: much longer tail swept to the left so it does not read as a period
    yb, xa, xb = m.pick(-3.6, -.92, -.92), m.pick(-1.05, -.34, -.34), m.pick(-.55, .1, .1)
    tail = shpoly(m, [(c - .5 * d, .3 * d), (c + xa * d, yb * d), (c + xb * d, yb * d),
                      (c + .5 * d, .3 * d)])
    return P.PUNCT_WIDTH, [oval(m, (c - d / 2, 0, c + d / 2, d), over=False), tail]
