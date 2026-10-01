"""Capital-letter parameters (side bearings by shape class, diagonal thinning).

All numbers are (thin 100, regular 400, black 950) via Master.pick.
Side-bearing classes: STR straight vertical stem, RND round side, OPN open side
(arm ends, apertures), DIA diagonal end (A V W X foot / top corner).
"""

_SB = {
    "STR": (78, 84, 60),
    "RND": (58, 60, 42),
    "OPN": (46, 48, 32),
    "DIA": (32, 20, 12),
}


def sb(m, kind):
    return m.pick(*_SB[kind])


def diag_k(m):
    """Perpendicular thickness of diagonals relative to the stem (thinner when heavy)."""
    return m.pick(1.0, 0.94, 0.78)


def apex_k(m):
    """Flat apex / vertex width relative to the diagonal's horizontal width."""
    return m.pick(1.0, 0.88, 0.70)
