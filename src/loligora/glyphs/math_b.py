"""Tilde, caret, degree, superior figures, fractions, ª º µ ™"""
from .. import params as P
from ..cs_kit import H, S, hstrut, peak, pg, rect, sup_glyph, wave
from ..rounds import oval_ring

from . import (fig_eight, fig_four, fig_one, fig_three, fig_two, lc_a, lc_o, lc_u, uc_M, uc_T)

W = P.DIGIT_WIDTH
K = 0.6


def _f(m):
    return m.pick(1.3, 1.3, 1.12)   # superior stroke boost; lighter at 950 (open counters)


def asciitilde(m):
    m = m.origin(268)
    return W, [wave(m, 90, 490, 268, m.pick(62, 66, 70), H(m) * m.pick(1.0, 0.95, 0.85))]


def asciicircum(m):
    m = m.origin(500)
    hw, w = m.pick(190, 195, 215), m.pick(22, 84, 150)
    return W, [peak(m, W / 2, 470, 720, hw, w)]


def degree(m):
    m = m.origin(600)
    d = m.pick(230, 240, 270)
    t = m.pick(22, 70, 96)
    sb = m.pick(40, 45, 40)
    return d + 2 * sb, oval_ring(m, (sb, 720 - d, sb + d, 720), t, t, over=False)


def _sup(mod):
    def f(m):
        adv, cs = sup_glyph(m, mod, K, _f(m), 20, 720 - 720 * K)
        return adv + 40, cs
    return f


def _frac(num, den):
    def f(m):
        a, c1 = sup_glyph(m, num, K, _f(m), 20, 720 - 720 * K)
        x2 = 20 + a + 170
        b, c2 = sup_glyph(m, den, K, _f(m), x2, 0)
        sl = hstrut(m.origin(360), (20 + a - 60, -10), (20 + a + 130, 730), S(m) * m.pick(0.6, 0.5, 0.4))
        return x2 + b + 20, c1 + c2 + [sl]
    return f


def _ord(mod):
    def f(m):
        a, cs = sup_glyph(m, mod, 0.62, 1.25, 20, 720 - P.XH * 0.62, cy0=P.XH / 2)
        h = H(m) * 0.55
        return a + 40, cs + [rect(m, 20, 280 + 0.62 * (540 - P.XH), 20 + a, 280 + 0.62 * (540 - P.XH) + h)]
    return f


def mu(m):
    adv, cs = lc_u.draw(m)
    from .. import lc_params as L
    sb, st = L.sb_s(m), m.stem_lc
    return adv, cs + [rect(m, sb, P.DESC, sb + st, 120)]


def trademark(m):
    a, c1 = sup_glyph(m, uc_T, 0.5, m.pick(1.4, 1.4, 1.05), 20, 360)
    b, c2 = sup_glyph(m, uc_M, 0.5, m.pick(1.4, 1.4, 1.05), 20 + a - 10, 360)
    return 20 + a + b + 10, c1 + c2


GLYPHS = [("asciitilde", 0x7E, asciitilde), ("asciicircum", 0x5E, asciicircum),
          ("degree", 0xB0, degree), ("onesuperior", 0xB9, _sup(fig_one)),
          ("twosuperior", 0xB2, _sup(fig_two)), ("threesuperior", 0xB3, _sup(fig_three)),
          ("onequarter", 0xBC, _frac(fig_one, fig_four)),
          ("onehalf", 0xBD, _frac(fig_one, fig_two)),
          ("threequarters", 0xBE, _frac(fig_three, fig_four)),
          ("ordfeminine", 0xAA, _ord(lc_a)), ("ordmasculine", 0xBA, _ord(lc_o)),
          ("mu", 0xB5, mu), ("trademark", 0x2122, trademark)]
