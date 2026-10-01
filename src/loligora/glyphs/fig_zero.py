from .. import params as P
from ..rounds import oval_ring

NAME, UNI = "zero", 0x30


def draw(m):
    m = m.origin(360)
    sb = m.sb_dg
    box = (sb, 0, P.DIGIT_WIDTH - sb, P.CAP)
    return P.DIGIT_WIDTH, oval_ring(m, box, m.stem_dg, m.h_dg, n=P.N_ZERO)
