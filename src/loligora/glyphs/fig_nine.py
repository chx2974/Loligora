from .. import params as P
from ..fig_parts import rot180
from .fig_six import six

NAME, UNI = "nine", 0x39


def draw(m):
    return P.DIGIT_WIDTH, rot180(six(m))
