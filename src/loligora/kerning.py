"""Class-based kerning, written per master into each UFO (groups + kerning).

ufo2ft turns UFO groups/kerning into a `kern` GPOS feature and fontmake/varLib
interpolates every pair between the three masters (variable kerning), so the
classes must be identical in all masters (they are: they do not depend on m).

Naming: R_x = first glyph of a pair (its RIGHT side), L_x = second glyph (its
LEFT side); UFO group names are public.kern1.* / public.kern2.*.
Digits and every fig_* / punct_* glyph are never in a class, except the
`period` and `comma` glyphs as second glyph after letters (L_stop).
Values: (thin, regular, black) in font units; italic pairs are scaled by
ITALIC_K (slanted shapes overhang less). Positive numbers open, negative close.
"""
from . import params as P
from .composites import composites
from .kerning_quotes import R_Q, L_Q, PAIRS_Q, PAIRS_QI

DASHES = ["hyphen", "endash", "emdash"]

# glyph classes: first glyph (right side)
R = {
    "A": ["A"], "VW": ["V", "W"], "Y": ["Y"], "T": ["T"], "F": ["F"], "P": ["P"],
    "L": ["L"], "vwy": ["v", "w", "y"], "r": ["r"], "f": ["f"], "t": ["t"],
    "o": ["o", "c", "e"], "K": ["K"], "k": ["k"],
    # capitals: closed round right side (C G are open on the right: not in it), U, X, Z
    "O": ["O", "Q", "Oslash"], "U": ["U"], "X": ["X"], "Z": ["Z"],
    "hyph": DASHES,
}
R.update(R_Q)
# second glyph (left side)
L = {
    "A": ["A"], "VW": ["V", "W"], "Y": ["Y"], "T": ["T"],
    "o": ["a", "c", "d", "e", "g", "o", "q"], "s": ["s"],
    "urn": ["u", "r", "n", "m", "p"], "vwy": ["v", "w", "y"],
    "stop": ["period", "comma", "quotesinglbase", "quotedblbase"], "O": ["O", "C", "G", "Q", "Oslash", "OE"],
    "U": ["U"], "X": ["X"], "Z": ["Z"], "J": ["J"],
    "hyph": DASHES,
}
L.update(L_Q)

# (first class, second class, thin, regular, black)
PAIRS = [
    ("A", "T", -70, -76, -60), ("A", "VW", -62, -66, -50), ("A", "Y", -76, -82, -66),
    ("VW", "A", -68, -76, -60), ("Y", "A", -78, -86, -70), ("T", "A", -80, -86, -70),
    ("F", "A", -56, -62, -50), ("P", "A", -74, -80, -64),
    ("L", "T", -104, -112, -92), ("L", "VW", -90, -98, -80), ("L", "Y", -104, -112, -92),
    ("L", "vwy", -34, -40, -32),
    ("T", "o", -80, -88, -72), ("T", "s", -56, -62, -48), ("T", "urn", -40, -46, -36),
    ("T", "vwy", -50, -56, -46),
    ("VW", "o", -60, -66, -54), ("VW", "urn", -30, -34, -28), ("VW", "s", -36, -40, -32),
    ("Y", "o", -82, -90, -74), ("Y", "urn", -46, -54, -42), ("Y", "s", -60, -66, -52),
    ("T", "stop", -84, -92, -74), ("VW", "stop", -72, -80, -64), ("Y", "stop", -84, -92, -74),
    ("P", "stop", -68, -74, -60), ("F", "stop", -62, -68, -54),
    ("vwy", "stop", -66, -72, -58), ("r", "stop", -44, -50, -40), ("f", "stop", -16, -20, -16),
    ("vwy", "o", -22, -26, -22), ("o", "vwy", -14, -16, -14), ("vwy", "vwy", -8, -10, -8),
    ("r", "vwy", -16, -18, -14), ("t", "vwy", -8, -10, -8), ("r", "o", -8, -10, -8),
    ("f", "vwy", -8, -10, -8),
    # K (narrow, open diagonals) and k
    ("K", "O", -40, -44, -34), ("K", "o", -34, -38, -30), ("K", "urn", -22, -26, -20),
    ("K", "vwy", -40, -46, -38),
    ("k", "o", -26, -30, -24), ("k", "vwy", -30, -34, -28),
    # [kc] capital against round / U / J capitals (same values both directions)
    ("T", "O", -56, -54, -38), ("O", "T", -56, -54, -38),
    ("VW", "O", -26, -22, -32), ("O", "VW", -26, -22, -32),
    ("Y", "O", -50, -50, -50), ("O", "Y", -50, -50, -50),
    ("A", "O", -26, -26, -34), ("O", "A", -26, -26, -34),
    ("A", "U", -30, -30, -34), ("U", "A", -30, -30, -34),
    ("L", "O", -50, -50, -34), ("L", "U", -44, -40, -30),
    ("X", "O", -34, -34, -36), ("O", "X", -34, -34, -36),
    ("Z", "O", -32, -32, -20), ("O", "Z", -32, -32, -20),
    ("P", "J", -30, -30, -30), ("F", "J", -34, -34, -30), ("T", "J", -40, -40, -36),
    ("VW", "J", -24, -24, -24), ("Y", "J", -36, -36, -32), ("A", "J", -14, -14, -14),
    ("L", "J", -24, -24, -20),
    # quotes and dashes
    ("T", "hyph", -36, -40, -32), ("Y", "hyph", -36, -40, -32),
    ("VW", "hyph", -26, -30, -24), ("hyph", "T", -36, -40, -32), ("hyph", "Y", -40, -46, -38),
    ("hyph", "VW", -22, -26, -20), ("hyph", "A", -10, -12, -10), ("A", "hyph", -10, -12, -10),
]
PAIRS += PAIRS_Q
ITALIC_K = 0.9
# Italic: tuned per pair from shaped proofs + a de-slanted ink-gap measure (upright
# values x0.9 left rounds, diagonals and stops too open in the slant). Pairs not listed
# (quotes, dashes) use the upright values x ITALIC_K.
PAIRS_ITALIC = [
("A", "T", -70, -74, -59),
("A", "VW", -64, -66, -52),
("A", "Y", -78, -82, -68),
("VW", "A", -69, -75, -61),
("Y", "A", -79, -87, -71),
("T", "A", -79, -86, -69),
("F", "A", -55, -62, -50),
("P", "A", -75, -81, -65),
("L", "T", -102, -110, -90),
("L", "VW", -90, -98, -79),
("L", "Y", -105, -112, -92),
("L", "vwy", -49, -54, -46),
("T", "o", -91, -99, -85),
("T", "s", -65, -71, -58),
("T", "urn", -54, -62, -50),
("T", "vwy", -64, -70, -60),
("VW", "o", -73, -77, -68),
("VW", "urn", -45, -48, -43),
("VW", "s", -46, -49, -44),
("Y", "o", -95, -103, -88),
("Y", "urn", -61, -69, -57),
("Y", "s", -70, -77, -64),
("T", "stop", -97, -107, -89),
("VW", "stop", -86, -95, -81),
("Y", "stop", -99, -109, -91),
("P", "stop", -82, -90, -77),
("F", "stop", -75, -83, -69),
("vwy", "stop", -66, -74, -60),
("r", "stop", -43, -53, -42),
("f", "stop", -15, -21, -17),
("vwy", "o", -20, -24, -21),
("o", "vwy", -13, -14, -14),
("vwy", "vwy", -9, -11, -9),
("r", "vwy", -17, -20, -15),
("t", "vwy", -9, -10, -9),
("r", "o", -6, -9, -6),
("f", "vwy", -9, -10, -8),
("K", "O", -39, -43, -34),
("K", "o", -45, -49, -44),
("K", "urn", -35, -39, -35),
("K", "vwy", -54, -60, -54),
("k", "o", -23, -26, -23),
("k", "vwy", -30, -34, -29),
("T", "O", -56, -56, -37),
("O", "T", -56, -55, -38),
("VW", "O", -26, -22, -32),
("O", "VW", -26, -22, -32),
("Y", "O", -51, -51, -51),
("O", "Y", -51, -51, -51),
("A", "O", -26, -26, -34),
("O", "A", -26, -26, -34),
("A", "U", -27, -26, -31),
("U", "A", -27, -26, -31),
("L", "O", -51, -51, -34),
("L", "U", -43, -38, -27),
("X", "O", -34, -34, -36),
("O", "X", -34, -34, -36),
("Z", "O", -32, -33, -20),
("O", "Z", -32, -33, -20),
("P", "J", -29, -29, -29),
("F", "J", -33, -33, -29),
("T", "J", -39, -39, -35),
("VW", "J", -23, -23, -23),
("Y", "J", -35, -35, -31),
("A", "J", -12, -11, -12),
("L", "J", -23, -21, -17),
]

PAIRS_ITALIC += PAIRS_QI
PAIRS_ITALIC_SET = {tuple(p) for p in PAIRS_ITALIC}


def install(ufo, m):
    """Write groups and kerning for master m into a ufoLib2 Font."""
    from .composites import tune_advances
    tune_advances(ufo, m)                        # wider advance for accented I / i
    have = set(ufo.keys())
    groups = {}
    extra = {}                                   # base letter -> accented glyphs
    for name, _, base, _, _ in composites():
        extra.setdefault(base, []).append(name)
    extra["o"] = extra.get("o", []) + ["oslash", "oe"]
    for side, table in (("kern1", R), ("kern2", L)):
        for k, names in table.items():
            names = names + [a for n in names for a in extra.get(n, [])]
            g = [n for n in names if n in have]
            if g:
                groups[f"public.{side}.{'R' if side == 'kern1' else 'L'}_{k}"] = g
    ufo.groups.update(groups)
    k = ITALIC_K if m.italic else 1.0
    table = PAIRS
    if m.italic:
        tuned = {(a, b) for a, b, *_ in PAIRS_ITALIC}
        table = PAIRS_ITALIC + [p for p in PAIRS if (p[0], p[1]) not in tuned]
    for a, b, *vals in table:
        ka, kb = f"public.kern1.R_{a}", f"public.kern2.L_{b}"
        if ka in groups and kb in groups:
            ufo.kerning[(ka, kb)] = round(m.pick(*vals) * (k if (a, b, *vals) not in PAIRS_ITALIC_SET else 1.0))
