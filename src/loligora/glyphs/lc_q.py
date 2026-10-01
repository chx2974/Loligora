from .. import params as P
from ..lc_bowls import bowl_letter

NAME, UNI = "q", 0x71


def draw(m):
    return bowl_letter(m, False, P.DESC, P.XH)
