"""Accent builders added for GF Latin Core: breve, dot above, ogonek, double acute,
comma below, turned comma above, plus the vertical caron (`caronalt`, beside the
stem of d l t L). Same conventions as acc_a: BUILD[acc](m, cx, case) ->
(contours, top y); m has the shear origin of the base case."""
from .. import params as P
from ..arcs import PI
from ..composites import alt_h, alt_w
from ..cs_kit import abands, hstrut, pg, rect, sq_dot
from . import punct_comma
from .punct_period import dot_size

YB = {False: P.XH + 70, True: P.CAP + 52}


def _w(m):
    return m.pick(22, 78, 130)


def _breve(m, cx, case):
    c = 0.88 if case else 1.0
    a, t = m.pick(110, 124, 150) * c, m.pick(20, 50, 64)
    b = m.pick(66, 72, 80) * c
    yb = YB[case]
    cy, ycut = yb + b, yb + b * 1.22
    return [abands(m, cx, cy, a, b, t, t * 0.9, [("yl", ycut), "B", ("yr", ycut)], (3, 3))], ycut


def _dot(m, cx, case):
    d = m.pick(40, 104, 152) * (0.92 if case else 1.0)
    return [sq_dot(m, cx, YB[case] + d / 2, d)], YB[case] + d


def _hungarumlaut(m, cx, case):
    c = 0.82 if case else 1.0
    h, w = m.pick(135, 145, 160) * c, m.pick(20, 66, 92) * 0.9
    dx = h * (0.5 if case else 0.4)
    sp = m.pick(90, 122, 178) * (0.95 if case else 1.0)
    yb = YB[case]
    cs = [hstrut(m, (x - dx / 2 - w / 2, yb), (x + dx / 2 - w / 2, yb + h), w)
          for x in (cx - sp / 2, cx + sp / 2)]
    return cs, yb + h


def _bez(p, u):
    q = 1 - u
    return tuple(q**3 * p[0][i] + 3*q*q*u * p[1][i] + 3*q*u*u * p[2][i] + u**3 * p[3][i]
                 for i in (0, 1))


def _crs(pts):
    """Smooth cubics through the points (Catmull-Rom)."""
    n, out = len(pts), []
    for i in range(n - 1):
        p0, p1, p2, p3 = pts[max(i - 1, 0)], pts[i], pts[i + 1], pts[min(i + 2, n - 1)]
        out.append((p1, (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6),
                    (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6), p2))
    return out


def _ogonek(m, cx, case):
    """Hook hanging from the baseline: neck down (leaning left), round bottom, tail
    sweeping back right and up. Fixed size; only the stroke follows the weight."""
    t = m.pick(20, 48, 58)
    x0, d = cx - t / 2, 188
    yb = t / 2 - d
    ch = [((x0, 24), (x0, -50), (x0 - 10, -90), (x0 - 22, -120)),
          ((x0 - 22, -120), (x0 - 29, -143), (x0 - 28, yb), (x0 - 2, yb)),
          ((x0 - 2, yb), (x0 + 32, yb), (x0 + 60, yb + 12), (x0 + 74, yb + 38))]
    cl = []
    for si, seg in enumerate(ch):
        for j in range(8):
            u = j / 8
            pt = _bez(seg, u)
            e = 1e-3
            a, b = _bez(seg, max(u - e, 0)), _bez(seg, min(u + e, 1))
            tx, ty = b[0] - a[0], b[1] - a[1]
            L = (tx * tx + ty * ty) ** 0.5
            g = (si + u) / 3
            w = t * (1.0 if g < 0.55 else 1.0 - 0.6 * ((g - 0.55) / 0.45) ** 1.4)
            cl.append((pt, (-ty / L, tx / L), w))
    pt = ch[-1][3]
    cl.append((pt, (-0.9, 0.43), t * 0.36))
    left = [(p[0] + n[0] * w / 2, p[1] + n[1] * w / 2) for p, n, w in cl]
    right = [(p[0] - n[0] * w / 2, p[1] - n[1] * w / 2) for p, n, w in cl]
    sh = lambda q: m.sh(*q)
    lo = _crs([sh(q) for q in left])
    ro = _crs([sh(q) for q in right])
    cont = lo + [(lo[-1][3], ro[-1][3])] + [tuple(reversed(c)) for c in reversed(ro)] \
        + [(ro[0][0], lo[0][0])]
    area = sum(c[0][0] * c[-1][1] - c[-1][0] * c[0][1] for c in cont)
    if area < 0:
        cont = [tuple(reversed(c)) for c in reversed(cont)]
    return [cont], 0


def _comma(m, cx, yc, k, turn):
    """The comma glyph scaled by k, dot centre moved to (cx, yc); turn = 180 degrees."""
    _, cs = punct_comma.draw(m)
    d = dot_size(m)
    rx, ry = m.sh(P.PUNCT_WIDTH / 2, d / 2)
    tx, ty = m.sh(cx, yc)
    s = -k if turn else k
    return [[tuple((tx + s * (x - rx), ty + s * (y - ry)) for x, y in seg) for seg in c]
            for c in cs]


def _commaaccent(m, cx, case):
    k = m.pick(1.0, 0.6, 0.4)
    d = dot_size(m) * k
    yc = -m.pick(50, 48, 34) - d / 2
    return _comma(m, cx, yc, k, False), 0


def _commaturn(m, cx, case):
    k = m.pick(1.0, 0.6, 0.4)
    d = dot_size(m) * k
    yc = YB[case] + d / 2 + m.pick(18, 28, 40)
    return _comma(m, cx, yc, k, True), yc + d / 2 + 0.92 * d


BUILD = {"breve": _breve, "dotaccent": _dot, "ogonek": _ogonek,
         "hungarumlaut": _hungarumlaut, "commaaccent": _commaaccent,
         "commaturn": _commaturn}
UNI = {"breve": 0x2D8, "dotaccent": 0x2D9, "ogonek": 0x2DB, "hungarumlaut": 0x2DD,
       "commaaccent": None, "commaturn": None}
ADV = {"breve": (300, 330, 390), "dotaccent": (200, 250, 310), "ogonek": (240, 270, 330),
       "hungarumlaut": (340, 360, 440), "commaaccent": (260, 260, 300),
       "commaturn": (260, 260, 300)}
# marks hanging below the base: combining glyph anchor name
BELOW = {"cedilla": "_bottom", "commaaccent": "_bottom", "ogonek": "_ogonek"}


def caronalt(m):
    """Vertical tapered tick (like quotesingle), bottom at y = 0, axis x = 0 at mid height."""
    w, h = alt_w(m), alt_h(m)
    m0 = m.origin(h / 2)
    return round(w + 40), [pg(m0, [(-w * 0.25, 0), (w * 0.25, 0), (w / 2, h), (-w / 2, h)])]


GLYPHS = [("caronalt", None, caronalt)]
