"""Proportional digits (`pnum`): the tabular outlines shifted into a new,
naturally spaced advance. Same contour structure as the defaults, so the
masters stay compatible. Sidebearings follow the lowercase o/n values."""
from dataclasses import replace
from importlib import import_module

from .. import lc_params as LC

DIGITS = [("zero", "fig_zero"), ("one", "fig_one"), ("two", "fig_two"),
          ("three", "fig_three"), ("four", "fig_four"), ("five", "fig_five"),
          ("six", "fig_six"), ("seven", "fig_seven"), ("eight", "fig_eight"),
          ("nine", "fig_nine")]
# extra sidebearing (x sb) per digit: 1 has an open flag on the left
SB = {"one": 1.0}


def _pts(contours):
    for c in contours:
        for s in c:
            yield from s[1:] if len(s) > 2 else s


def _bounds_x(contours):
    xs = [p[0] for p in _pts(contours)]
    return min(xs), max(xs)


def _shift(contours, dx):
    return [[tuple((x + dx, y) for x, y in s) for s in c] for c in contours]


def _make(name, mod):
    def draw(m):
        drw = import_module(f".{mod}", __package__).draw
        _, contours = drw(m)[:2]
        # advance and shift are measured on the upright master of the same
        # weight (the slant only shears about CAP/2, so italics reuse them)
        lo, hi = _bounds_x(drw(replace(m, italic=False))[1])
        sb = LC.sb_r(m) * SB.get(name, 1.0) + {"one": 22, "seven": 4}.get(name, 4)
        sb = round(sb)
        dx = sb - lo
        return round(hi - lo + 2 * sb), _shift(contours, dx)
    return draw


GLYPHS = [(f"{n}.pnum", None, _make(n, mod)) for n, mod in DIGITS]
