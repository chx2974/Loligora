from .. import params as P
from ..lc_bowls import bowl_letter

NAME, UNI = "d", 0x64


def draw(m):
    return bowl_letter(m, False, 0, P.ASC)
