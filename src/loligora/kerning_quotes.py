"""Quote / guillemet kerning (classes + pairs), merged into kerning.py.

qo = opening quotes, qc = closing / straight quotes, gl / gr = « ‹ and » ›.
A glyph can only sit in one kern1 and one kern2 group, so these replace the old
single "quote" class. Low quotes (quotesinglbase, quotedblbase) are kerned as
commas (they join L_stop in kerning.py). Digits are never involved.
Values: (thin, regular, black); positive opens, negative closes.
"""
QO = ["quoteleft", "quotedblleft"]
QC = ["quoteright", "quotedblright", "quotesingle", "quotedbl"]
GL = ["guillemotleft", "guilsinglleft"]
GR = ["guillemotright", "guilsinglright"]

R_Q = {"qo": QO, "qc": QC, "gl": GL, "gr": GR}
L_Q = {"qo": QO, "qc": QC, "gl": GL, "gr": GR, "L": ["L"], "P": ["P"], "F": ["F"]}

PAIRS_Q = [
    # opening quote + capital / lowercase
    ("qo", "A", -56, -64, -50), ("qo", "J", -14, -16, -14), ("qo", "T", 0, 0, 0),
    ("qo", "VW", -4, -6, -4), ("qo", "Y", -4, -6, -4), ("qo", "L", 0, 0, 0),
    ("qo", "P", 0, 0, 0), ("qo", "F", 0, 0, 0), ("qo", "O", -12, -12, -10),
    ("qo", "o", -24, -28, -22), ("qo", "s", -8, -10, -8),
    # capital / lowercase + closing quote
    ("A", "qo", -60, -68, -54), ("A", "qc", -60, -68, -54), ("L", "qo", -100, -110, -90),
    ("L", "qc", -100, -110, -90), ("T", "qc", 0, 0, 0), ("VW", "qc", 0, 0, 0),
    ("Y", "qc", 0, 0, 0), ("P", "qc", 0, 0, 0), ("F", "qc", 0, 0, 0),
    ("vwy", "qc", -6, -8, -6), ("f", "qc", 20, 28, 22),
    ("qc", "A", -56, -64, -50), ("qc", "o", -24, -28, -22),
    # guillemets
    ("A", "gr", -20, -24, -18), ("T", "gr", -26, -30, -24), ("VW", "gr", -20, -24, -18),
    ("Y", "gr", -26, -30, -24), ("gl", "A", -10, -12, -10), ("gl", "T", -8, -10, -8),
    ("gl", "VW", -6, -8, -6), ("gl", "Y", -8, -10, -8), ("gr", "A", -20, -24, -18),
]
PAIRS_QI = []
