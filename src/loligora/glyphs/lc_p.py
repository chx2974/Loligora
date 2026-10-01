from .. import params as P
from ..lc_bowls import bowl_letter

NAME, UNI = "p", 0x70


def draw(m):
    return bowl_letter(m, True, P.DESC, P.XH)
