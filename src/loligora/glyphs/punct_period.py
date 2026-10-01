from .. import params as P
from ..rounds import oval

NAME, UNI = "period", 0x2E


def dot_size(m):
    return m.pick(30, 104, 206)


def draw(m):
    d, c = dot_size(m), P.PUNCT_WIDTH / 2
    return P.PUNCT_WIDTH, [oval(m, (c - d / 2, 0, c + d / 2, d), over=False)]
