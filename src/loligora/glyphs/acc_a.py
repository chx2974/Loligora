"""Accents: spacing marks (` ´ ˆ ˜ ¨ ¯ ¸ ˚ ˇ), their capital-height `.case` forms
and the zero-width combining marks (components of the spacing glyphs, with
_top/_bottom anchors for the mark feature)."""
from .. import params as P
from ..composites import ACCENTS, CASE
from ..cs_kit import abands, hstrut, peak, rect, sq_dot, wave
from ..rounds import oval_ring
from . import _acc_new as N

YB = {False: P.XH + 70, True: P.CAP + 52}       # bottom of the mark
BASE = {False: P.XH, True: P.CAP}               # height of the base's `top`


def _k(m, case):
    """Common numbers: stroke, height, case flag scale."""
    return dict(w=m.pick(22, 78, 130), c=0.82 if case else 1.0)


def _acute(m, cx, case, sign=1):
    k = _k(m, case)
    h = m.pick(140, 150, 165) * k["c"]
    dx = h * (0.5 if case else 0.4) * sign
    yb = YB[case]
    return [hstrut(m, (cx - dx / 2 - k["w"] / 2, yb), (cx + dx / 2 - k["w"] / 2, yb + h), k["w"])], yb + h


def _grave(m, cx, case):
    return _acute(m, cx, case, -1)


def _peak(m, cx, case, down=False):
    k = _k(m, case)
    h = m.pick(120, 125, 140) * k["c"]
    hw = m.pick(115, 125, 160) * (1.1 if case else 1.0)
    yb = YB[case]
    return [peak(m, cx, yb, yb + h, hw, k["w"] * m.pick(1, 1, 0.95), down)], yb + h


def _caron(m, cx, case):
    return _peak(m, cx, case, True)


def _dieresis(m, cx, case):
    k = _k(m, case)
    d = m.pick(36, 100, 150) * (0.92 if case else 1.0)
    g = m.pick(50, 62, 50)
    yb = YB[case]
    return [sq_dot(m, cx - d / 2 - g / 2, yb + d / 2, d), sq_dot(m, cx + d / 2 + g / 2, yb + d / 2, d)], yb + d


def _macron(m, cx, case):
    wd, h = m.pick(210, 250, 300), max(m.h_uc * 0.9, 20) * (0.9 if case else 1.0)
    yb = YB[case] + 20
    return [rect(m, cx - wd / 2, yb, cx + wd / 2, yb + h)], yb + h


def _ring(m, cx, case):
    d = m.pick(140, 160, 190) * (0.94 if case else 1.0)
    t = m.pick(20, 52, 66)
    yb = YB[case]
    return oval_ring(m, (cx - d / 2, yb, cx + d / 2, yb + d), t, t, over=False), yb + d


def _tilde(m, cx, case):
    wd = m.pick(240, 290, 350)
    amp = m.pick(30, 36, 40) * (0.85 if case else 1.0)
    t = m.pick(20, 46, 62)
    ym = YB[case] + amp + t / 2 + 4
    return [wave(m, cx - wd / 2, cx + wd / 2, ym, amp, t)], ym + amp + t / 2


def _cedilla(m, cx, case):
    t = m.pick(20, 48, 58)
    a, b = m.pick(58, 74, 108), m.pick(60, 80, 112)
    cy = -m.pick(70, 88, 120)
    xr = cx + t / 2
    hook = abands(m, xr - a, cy, a, b, t, t, [("yl", cy - 0.3 * (b - t)), "B", "r"], (2, 3))
    return [hook, rect(m, cx - t / 2, cy, xr, 26)], 0


BUILD = {"grave": _grave, "acute": _acute, "circumflex": _peak, "tilde": _tilde,
         "dieresis": _dieresis, "macron": _macron, "cedilla": _cedilla, "ring": _ring,
         "caron": _caron}
UNI = {"grave": 0x60, "acute": 0xB4, "circumflex": 0x2C6, "tilde": 0x2DC, "dieresis": 0xA8,
       "macron": 0xAF, "cedilla": 0xB8, "ring": 0x2DA, "caron": 0x2C7}
ADV = {"grave": (300, 340, 400), "acute": (300, 340, 400), "circumflex": (330, 360, 460),
       "tilde": (330, 380, 440), "dieresis": (250, 330, 430), "macron": (330, 380, 440),
       "cedilla": (260, 280, 340), "ring": (260, 280, 320), "caron": (330, 360, 460)}


BUILD.update(N.BUILD)
UNI.update(N.UNI)
ADV.update(N.ADV)


def _spacing(acc, case):
    def draw(m):
        m0 = m.origin(360 if case else P.XH / 2)
        adv = ADV[acc][(0, 1, 2)[["Thin", "Regular", "ExtraBlack"].index(m.weight_name)]]
        cs, _ = BUILD[acc](m0, adv / 2, case)
        return adv, cs
    return draw


def _combining(acc, case):
    sp = _spacing(acc, case)

    def draw(m):
        adv = sp(m)[0]
        m0 = m.origin(360 if case else P.XH / 2)
        cs, top = BUILD[acc](m0, 0, case)
        b = BASE[case]
        an = {"_top": (m0.sh(0, b)[0], b), "top": (m0.sh(0, top - 45)[0], top - 45 + 25 + 0 * b)}
        an["top"] = (an["top"][0], top + 25 - (YB[case] - b))
        if acc in N.BELOW:
            an = {N.BELOW[acc]: (m0.sh(0, 0)[0], 0)}
        return 0, [], an, [(acc + (CASE if case else ""), -adv / 2, 0)]
    return draw


def _glyphs():
    out = []
    for acc, (sp, comb, cuni) in ACCENTS.items():
        for case in (False, True):
            suf = CASE if case else ""
            out.append((sp + suf, None if case else UNI[acc], _spacing(acc, case)))
            out.append((comb + suf, None if case else cuni, _combining(acc, case)))
    return out


GLYPHS = _glyphs() + N.GLYPHS
