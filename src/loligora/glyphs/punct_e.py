"""Big symbols: @ & % ‰ © ®"""
from .. import params as P
from ..arcs import cring
from ..cs_kit import H, S, abands, hstrut, pg, rect, sup_glyph, strut
from ..rounds import oval_ring
from ..strokes import diagonal


def at(m):
    m = m.origin(300)
    t, h = m.stem_lc * m.pick(1, 0.9, 0.75), m.h_lc * m.pick(1, 0.9, 0.75)
    sb, w = m.pick(50, 50, 40), m.pick(800, 830, 900)
    y0, y1 = -150, 700
    outer = cring(m, (sb, y0, sb + w, y1), t, h, 330, 40, over=False, kappa=0.4)
    iw = m.pick(300, 320, 370)
    ix = sb + w / 2 - iw / 2 - 30
    ring = oval_ring(m, (ix, 120, ix + iw, 470), t * 0.9, h * 0.9, over=False)
    stem = rect(m, ix + iw - t * 0.9, 130, ix + iw + t * 0.1, 500 - h * 0.2)
    return w + 2 * sb, [outer] + ring + [stem]


def ampersand(m):
    m = m.origin(360)
    t, h = S(m) * m.pick(1, 0.9, 0.62), H(m) * m.pick(1, 0.9, 0.62)
    sb = m.pick(40, 40, 30)
    wl = m.pick(390, 400, 450)                        # lower bowl width
    top = oval_ring(m, (sb + 50, 410, sb + m.pick(300, 310, 390), 725), t * m.pick(1, 1, 0.78), h, over=True)
    yl = P.OVERSHOOT
    box = (sb, -yl, sb + wl, 460)
    cy, b = (box[1] + box[3]) / 2, (box[3] - box[1]) / 2
    low = abands(m, sb + wl / 2, cy, wl / 2, b, t, h,
                 ["T", "L", "B", ("yr", cy + 0.35 * (b - h))], (3, 3, 4), over_w=False)
    xf = sb + wl + m.pick(150, 150, 170)               # foot of the diagonal
    diag = diagonal(m, (xf - t * 1.15, 0), (sb + 62, 500), t * 1.0)
    return xf + m.pick(25, 25, 20), top + [low, diag]


def _pct_rings(m, sb, w, n):
    t, h = m.stem_lc * m.pick(1, 0.9, 0.55), m.h_lc * m.pick(1, 0.9, 0.55)
    rw, rh = m.pick(260, 270, 300), 330
    boxes = [(sb, 390, sb + rw, 720)]
    for i in range(n - 1):
        boxes.append((w - sb - rw - i * (rw + 30) - (0), 0, w - sb - i * (rw + 30), rh))
    out = []
    for b in boxes:
        out += oval_ring(m, b, t, h, over=False)
    return out


def percent(m):
    m = m.origin(360)
    sb, w = m.pick(40, 40, 30), m.pick(830, 860, 900)
    sl = diagonal(m, (w * 0.29, -10), (w * 0.71 - 40, 730), S(m) * m.pick(0.7, 0.55, 0.42))
    return w, _pct_rings(m, sb, w, 2) + [sl]


def perthousand(m):
    m = m.origin(360)
    sb, w = m.pick(40, 40, 30), m.pick(1140, 1170, 1210)
    sl = diagonal(m, (w * 0.22, -10), (w * 0.56 - 40, 730), S(m) * m.pick(0.7, 0.55, 0.42))
    return w, _pct_rings(m, sb, w, 3) + [sl]


def _circled(m):
    m = m.origin(360)
    t, h = m.stem_lc * m.pick(0.9, 0.8, 0.5), m.h_lc * m.pick(0.9, 0.8, 0.5)
    sb, d = m.pick(40, 40, 30), 700
    return sb, d, oval_ring(m, (sb, 10, sb + d, 710), t, h, over=False), t, h


def copyright(m):
    sb, d, ring, t, h = _circled(m)
    m = m.origin(360)
    c = cring(m, (sb + 200, 210, sb + d - 200, 510), t * 0.9, h * 0.9, 320, 400, over=False,
              kappa=0.5) if False else cring(m, (sb + 180, 200, sb + d - 180, 520), t * 0.9,
                                              h * 0.9, 380, 340, over=False)
    return d + 2 * sb, ring + [c]


def registered(m):
    from . import uc_R
    sb, d, ring, t, h = _circled(m)
    k, f = 0.5, m.pick(1.7, 1.45, 0.95)
    adv, cs = sup_glyph(m, uc_R, k, f, 0, 360 * (1 - k))
    dx = (d + 2 * sb - adv) / 2 - 4
    cs = [[tuple((x + dx, y) for x, y in seg) for seg in c] for c in cs]
    return d + 2 * sb, ring + cs


GLYPHS = [("at", 0x40, at), ("ampersand", 0x26, ampersand), ("percent", 0x25, percent),
          ("perthousand", 0x2030, perthousand), ("copyright", 0xA9, copyright),
          ("registered", 0xAE, registered)]
