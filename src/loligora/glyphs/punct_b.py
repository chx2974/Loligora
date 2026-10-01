"""Dashes, bars, quotes: - – — ­ _ | ¦ ' " ‘ ’ ‚ “ ” „"""
from .. import params as P
from ..arcs import rot180
from ..cs_kit import H, S, dotd, pg, rect, sbp
from . import punct_comma

DASH_Y = 268


def _dash(m, w, sb):
    h = H(m) * 0.95
    return w + 2 * sb, [rect(m, sb, DASH_Y - h / 2, sb + w, DASH_Y + h / 2)]


def hyphen(m):
    return _dash(m, m.pick(200, 230, 250), 70)


def endash(m):
    return _dash(m, 440, 40)


def emdash(m):
    return _dash(m, 860, 40)


def softhyphen(m):
    return hyphen(m)


def underscore(m):
    h = H(m) * 0.95
    return 500, [rect(m, 0, -130, 500, -130 + h)]


def bar(m):
    st, sb = S(m) * 0.9, sbp(m)
    return st + 2 * sb, [rect(m.origin(280), sb, -200, sb + st, 760)]


def brokenbar(m):
    st, sb, m = S(m) * 0.9, sbp(m), m.origin(280)
    return st + 2 * sb, [rect(m, sb, -200, sb + st, 130), rect(m, sb, 420, sb + st, 760)]


def _tick(m, cx):
    """Tapered straight tick (quotesingle)."""
    w = S(m)
    return pg(m, [(cx - w * 0.36, 450), (cx + w * 0.36, 450), (cx + w / 2, 720), (cx - w / 2, 720)])


def quotesingle(m):
    adv = S(m) + 2 * sbp(m)
    return adv, [_tick(m.origin(360), adv / 2)]


def quotedbl(m):
    m0, w = m.origin(360), S(m)
    gap = w * 1.2 + m.pick(70, 90, 60)
    adv = 2 * w + gap + 2 * sbp(m) * 0.9
    return adv, [_tick(m0, adv / 2 - gap / 2 - w / 2 + 0), _tick(m0, adv / 2 + gap / 2 + w / 2 - 0)]


def _shiftc(cs, dx, dy):
    return [[tuple((x + dx, y + dy) for x, y in seg) for seg in c] for c in cs]


def _quote(m, n, low=False, flip=False):
    """n comma shapes raised to the top (or at the baseline, low=True); flip =
    rotated by 180 degrees (left quotes)."""
    d = dotd(m)
    _, cs = punct_comma.draw(m)
    gap = d + m.pick(80, 100, 50)
    sb = sbp(m) * 0.8
    adv = d + (n - 1) * gap + 2 * sb
    dy = 0 if low else 720 - d
    out = []
    for i in range(n):
        out += _shiftc(cs, sb + d / 2 + i * gap - P.PUNCT_WIDTH / 2, dy)
    if flip:
        out = rot180(out, adv, 720 - 0.96 * d)
    return adv, out


GLYPHS = [("hyphen", 0x2D, hyphen), ("endash", 0x2013, endash), ("emdash", 0x2014, emdash),
          ("softhyphen", 0xAD, softhyphen), ("underscore", 0x5F, underscore),
          ("bar", 0x7C, bar), ("brokenbar", 0xA6, brokenbar),
          ("quotesingle", 0x27, quotesingle), ("quotedbl", 0x22, quotedbl),
          ("quoteright", 0x2019, lambda m: _quote(m, 1)),
          ("quotedblright", 0x201D, lambda m: _quote(m, 2)),
          ("quoteleft", 0x2018, lambda m: _quote(m, 1, flip=True)),
          ("quotedblleft", 0x201C, lambda m: _quote(m, 2, flip=True)),
          ("quotesinglbase", 0x201A, lambda m: _quote(m, 1, True)),
          ("quotedblbase", 0x201E, lambda m: _quote(m, 2, True))]
