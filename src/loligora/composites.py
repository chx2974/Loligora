"""Accented letters as UFO components: base letter + combining mark, placed
from anchors (base `top`/`bottom` vs mark `_top`/`_bottom`).

Capitals use the `.case` marks (lower and flatter). i and j accents use the
dotless bases. Also: base anchors for every letter (mark/mkmk features)."""
import unicodedata

from . import params as P

# accent name -> (spacing glyph, combining glyph, combining unicode)
ACCENTS = {
    "grave": ("grave", "gravecomb", 0x300), "acute": ("acute", "acutecomb", 0x301),
    "circumflex": ("circumflex", "uni0302", 0x302), "tilde": ("tilde", "tildecomb", 0x303),
    "dieresis": ("dieresis", "uni0308", 0x308), "macron": ("macron", "uni0304", 0x304),
    "cedilla": ("cedilla", "uni0327", 0x327), "ring": ("ring", "uni030A", 0x30A),
    "caron": ("caron", "uni030C", 0x30C),
    "breve": ("breve", "uni0306", 0x306), "dotaccent": ("dotaccent", "uni0307", 0x307),
    "ogonek": ("ogonek", "uni0328", 0x328), "hungarumlaut": ("hungarumlaut", "uni030B", 0x30B),
    "commaaccent": ("commaaccent", "uni0326", 0x326),
    "commaturn": ("commaturn", "uni0312", 0x312),
}
# marks attached to a base anchor other than `top`
ANCHOR = {"cedilla": "bottom", "commaaccent": "bottom", "ogonek": "ogonek"}
# accent -> letters carrying it (Latin-1 + GF Latin Core)
TABLE = {
    "grave": "AEIOUWYaeiouwy", "acute": "AEIOUYaeiouyCLNRSZWclnrszw",
    "circumflex": "AEIOUWYaeiouwy", "tilde": "ANOano", "dieresis": "AEIOUWYaeiouwy",
    "ring": "AUau", "cedilla": "CcSs", "caron": "CDENRSTZcenrsz",
    "macron": "AEIUaeiu", "breve": "AGag", "dotaccent": "CEGIZcegz",
    "ogonek": "AEIUaeiu", "hungarumlaut": "OUou", "commaaccent": "GKLNSTklnst",
    "commaturn": "g",
}
# letters with the vertical caron (caron.alt) beside the stem: glyph, unicode, base
ALT = [("dcaron", 0x10F, "d"), ("lcaron", 0x13E, "l"), ("Lcaron", 0x13D, "L"),
       ("tcaron", 0x165, "t")]
UNAME = {"dieresis": "DIAERESIS", "ring": "RING ABOVE", "cedilla": "CEDILLA",
         "caron": "CARON", "dotaccent": "DOT ABOVE", "hungarumlaut": "DOUBLE ACUTE",
         "commaturn": "CEDILLA"}
COMBINING = [v[1] for v in ACCENTS.values()]
CASE = ".case"


def _base(letter, acc=""):
    return "dotlessi" if letter == "i" and acc != "ogonek" else letter


def composites():
    """[(glyph name, unicode, base glyph, accent name, is_capital)]"""
    out = []
    for acc, letters in TABLE.items():
        for L in letters:
            name = L + acc
            what = UNAME.get(acc, acc.upper())
            if acc == "commaaccent":
                what = "COMMA BELOW" if L in "SsTt" else "CEDILLA"
            uni = ord(unicodedata.lookup(
                f"LATIN {'CAPITAL' if L.isupper() else 'SMALL'} LETTER {L.upper()} WITH {what}"))
            out.append((name, uni, _base(L, acc), acc, L.isupper()))
    out += [(n, u, b, "caronalt", b.isupper()) for n, u, b in ALT]
    return out


LC = list("abcdefghijklmnopqrstuvwxyz") + ["dotlessi", "dotlessj", "oe", "ae", "germandbls",
                                            "eth", "thorn", "oslash",
                                            "lslash", "hbar", "dcroat"]
UC = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ") + ["AE", "OE", "Eth", "Thorn", "Oslash", "Lslash", "Hbar",
                                                               "Germandbls"]


# Optical shift of the `top` anchor (fraction of the advance, upright design
# space) for asymmetric lowercase bases: the accent sits over the visual centre
# (bowl of a, stem/arch of n u, bowl of d) rather than the middle of the advance.
TOP_DX = {"a": -0.03, "d": 0.06, "b": -0.05, "n": -0.015, "h": -0.015, "m": -0.01,
          "u": 0.02, "r": -0.06, "y": 0.0, "g": -0.03, "q": -0.03, "f": 0.05, "t": 0.0,
          "dotlessj": 0.05, "germandbls": -0.02, "k": -0.03, "l": 0.0, "p": -0.02,
          "J": 0.04, "Y": 0.0, "L": -0.18}


def base_anchors(name, adv, m):
    """top/bottom anchors of a base letter (x on the slant axis at that height)."""
    if name in LC:
        y0, top = P.XH / 2, P.XH
    elif name in UC:
        y0, top = P.CAP / 2, P.CAP
    else:
        return {}
    dx = TOP_DX.get(name, 0.0) * adv
    if name == "l":                      # accent over the ascender stem
        from . import lc_params as L
        x = L.sb_s(m) + m.stem_lc / 2 + m.s * (P.ASC - y0)
        return {"top": (x, P.ASC), "bottom": (adv / 2 + m.s * (0 - y0), 0)}
    return {"top": (adv / 2 + dx + m.s * (top - y0), top),
            "bottom": (adv / 2 + m.s * (0 - y0), 0)}


def alt_w(m):
    """Width of the vertical caron (caron.alt) at the top."""
    return m.pick(22, 70, 108)


def alt_h(m):
    return m.pick(112, 126, 138)


def caron_alt_place(ufo, m, base):
    """(dx, dy, advance, scale) of the vertical caron right of the stem top of `base`: the
    tick's top edge is level with the top of the base (ascender / cap / t top) and its
    top-left corner is a fixed gap from the stem's right edge."""
    g = ufo[base]
    pts = [(p.x, p.y) for c in g.contours for p in c.points]
    ymax = max(y for _, y in pts)
    xr = max(x for x, y in pts if y >= ymax - 4)
    h, w = alt_h(m), alt_w(m)
    gap = m.pick(24, 34, 40)
    k = 0.8 if base == "t" else 1.0              # t: shorter tick, clear of the crossbar
    dx = xr + gap + k * (w / 2 - m.s * h / 2)
    right = xr + gap + k * w
    rsb = g.width - max(x for x, y in pts)
    adv = max(g.width, round(right + 0.7 * rsb))
    return dx, ymax - k * h, adv, k


OGONEK_BASES = ("A", "E", "I", "U", "a", "e", "i", "dotlessi", "u")


def ogonek_anchor(name, contours, m):
    """`ogonek` anchor: right edge of the ink at the baseline (x at y = 0)."""
    if name not in OGONEK_BASES:
        return {}
    best = None
    for c in contours:
        for seg in c:
            n = 12 if len(seg) == 4 else 1
            for i in range(n + 1):
                t = i / n
                if len(seg) == 4:
                    u = 1 - t
                    x = sum(w * p[0] for w, p in zip((u**3, 3*u*u*t, 3*u*t*t, t**3), seg))
                    y = sum(w * p[1] for w, p in zip((u**3, 3*u*u*t, 3*u*t*t, t**3), seg))
                else:
                    x = seg[0][0] + (seg[1][0] - seg[0][0]) * t
                    y = seg[0][1] + (seg[1][1] - seg[0][1]) * t
                if 0 <= y <= 30:
                    v = x - m.s * y
                    best = v if best is None else max(best, v)
    return {"ogonek": (best, 0)}


# --- spacing of accented narrow letters -------------------------------------
# An accent wider than a narrow I/i overflows the advance (circumflex, dieresis) and
# collides with the accent of the neighbouring letter. The base letter is left
# untouched: only the composite gets a larger advance (and its components are moved),
# so that every accent ink edge keeps at least ACC_CLEAR from the advance edge,
# measured along the slant (de-slanted) in italic. Called from kerning.install (the
# last step of ufo.build_master) because ufo.py places the composites.
NARROW_BASES = ("I", "dotlessi")


def acc_clear(m):
    """Minimum distance between accent ink and the advance edge."""
    return m.pick(16, 20, 22)


def _inked_bounds(layer, g, shear, y0):
    from fontTools.pens.boundsPen import BoundsPen
    from fontTools.pens.transformPen import TransformPen
    from fontTools.pens.recordingPen import DecomposingRecordingPen
    rec = DecomposingRecordingPen(layer)
    g.draw(rec)
    bp = BoundsPen(None)
    rec.replay(TransformPen(bp, (1, 0, -shear, 1, shear * y0, 0)))
    return bp.bounds


def tune_advances(ufo, m):
    layer = ufo.layers.defaultLayer
    shear = P.SLANT_TAN if m.italic else 0.0
    T = acc_clear(m)
    for name, _, base, _, _ in composites():
        if base not in NARROW_BASES or name not in ufo:
            continue
        g = ufo[name]
        x0, _, x1, _ = _inked_bounds(layer, g, shear, (P.CAP if base == 'I' else P.XH) / 2)
        pl, pr = max(0, T - x0), max(0, T - (g.width - x1))
        if pl or pr:
            for c in g.components:
                t = c.transformation
                c.transformation = (t[0], t[1], t[2], t[3], t[4] + pl, t[5])
            g.width = round(g.width + pl + pr)
