from .. import params as P
from ..lc_bowls import bowl_letter

NAME, UNI = "b", 0x62


def draw(m):
    return bowl_letter(m, True, 0, P.ASC)
