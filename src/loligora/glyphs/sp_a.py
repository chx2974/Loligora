"""Special letters: Ø ø Ð ð Þ þ Æ æ Œ œ ß"""
from .. import lc_params as L
from .. import params as P
from ..arcs import cring, shift
from ..cs_kit import H, S, hstrut, rect
from ..lc_curls import hook
from ..rounds import oval_ring
from ..strokes import bar
from ..sym_kit import arcp, back_c, lean
from ..uc_params import sb as SB
from ..uc_parts import bowl_d
from . import lc_e, lc_o, lc_p, uc_D, uc_O


def Oslash(m):
    adv, cs = uc_O.draw(m)
    m = m.origin(360)
    w = S(m) * m.pick(0.7, 0.6, 0.55)
    return adv, cs + [hstrut(m, (adv * 0.13, -25), (adv * 0.87 - w, 745), w)]


def oslash(m):
    adv, cs = lc_o.draw(m)
    w = m.stem_lc * m.pick(0.7, 0.6, 0.55)
    return adv, cs + [hstrut(m, (adv * 0.16, -25), (adv * 0.84 - w, P.XH + 25), w)]


def Eth(m):
    adv, cs = uc_D.draw(m)
    m = m.origin(360)
    dx, h = 70, H(m) * 0.95
    l = SB(m, "STR")
    return adv + dx, shift(cs, dx) + [rect(m, 24, 360 - h / 2, l + dx + S(m) + 70, 360 + h / 2)]


def Thorn(m):
    m = m.origin(360)
    l, r, st, h = SB(m, "STR"), SB(m, "RND"), S(m), H(m)
    w, a = m.pick(500, 520, 570), m.pick(190, 200, 250)
    bowl = bowl_d(m, l + st / 2, l + w, 130, 590, a, st, h)
    return w + l + r, [rect(m, l, 0, l + st, 720), bowl]


def thorn(m):
    adv, cs = lc_p.draw(m)
    sb = L.sb_s(m)
    return adv, cs + [rect(m, sb, P.XH - 20, sb + m.stem_lc, P.ASC)]


def eth(m):
    adv, cs = lc_o.draw(m)
    st, hb = m.stem_lc, m.h_lc * 0.9
    k = -0.36                                  # leftward lean of the ascender
    xo = adv - L.sb_r(m) - m.pick(0, 6, 20)
    top = P.ASC + P.OVERSHOOT
    r = L.tail_v(m) * 0.85
    y0 = 400
    h = hook(m, -1, xo, xo - st - L.tail_ext(m) + 10, top - r, top, top - r - 8,
             st * 0.95, L.term(m), m.h_lc * 0.95, y0)
    asc = lean([h], k, y0)
    xb = xo + k * (600 - y0)
    return adv, cs + asc + [bar(m, xb - st - 80, xb + 50, 563, hb * 0.8)]


def _e_arms(m, xe, we, sbr):
    st, h = S(m), H(m)
    ym = (720 - h) / 2 + 6
    return [rect(m, xe, 0, xe + st, 720), rect(m, xe, 720 - h, xe + we, 720),
            rect(m, xe, ym, xe + we - 28, ym + h), rect(m, xe, 0, xe + we, h)]


def AE(m):
    m = m.origin(360)
    st, h, sb = S(m), H(m), SB(m, "DIA")
    w = st * m.pick(1.0, 0.94, 0.8) * 1.05
    xe, we = sb + m.pick(400, 410, 450), m.pick(400, 410, 430)
    xl = sb + (xe - w / 2 - sb) * 0.3
    diag = hstrut(m, (sb, 0), (xe - w / 2, 720), w)
    xb = sb + (xe - w / 2 - sb) * 190 / 720
    return xe + st + we + SB(m, "OPN"), [diag, rect(m, xb, 190, xe, 190 + h * 0.92)] + _e_arms(m, xe, we, 0)


def OE(m):
    m = m.origin(360)
    st, sb = S(m), SB(m, "RND")
    wo, we = m.pick(600, 610, 650), m.pick(400, 410, 430)
    xs = sb + wo - st
    ring = oval_ring(m, (sb, 0, sb + wo, 720), st, H(m))
    return xs + we + SB(m, "OPN"), ring + _e_arms(m, xs, we, 0)


def _fuse(m, left, sb_left):
    """left glyph module + e, sharing one vertical stroke."""
    adv, cs = left.draw(m)
    ae, ce = lc_e.draw(m)
    dx = adv - sb_left - m.stem_lc - L.sb_r(m)
    return dx + ae, cs + shift(ce, dx)


def oe(m):
    return _fuse(m, lc_o, L.sb_r(m))


def ae(m):
    from . import lc_a
    return _fuse(m, lc_a, L.sb_s(m) if not m.italic else L.sb_s(m))


GLYPHS = [("Oslash", 0xD8, Oslash), ("oslash", 0xF8, oslash), ("Eth", 0xD0, Eth),
          ("eth", 0xF0, eth), ("Thorn", 0xDE, Thorn), ("thorn", 0xFE, thorn),
          ("AE", 0xC6, AE), ("ae", 0xE6, ae), ("OE", 0x152, OE), ("oe", 0x153, oe)]
