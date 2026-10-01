"""Write one UFO per master plus the designspace document."""
from pathlib import Path

import ufoLib2
from fontTools.designspaceLib import (AxisDescriptor, DesignSpaceDocument,
                                      InstanceDescriptor, SourceDescriptor)

from . import params as P
from . import composites, features, kerning
from .glyphs import all_glyphs


def _draw(glyph, contours):
    pen = glyph.getPen()
    for c in contours:
        pen.moveTo(c[0][0])
        segs = c
        if len(c[-1]) == 2 and c[-1][1] == c[0][0]:
            segs = c[:-1]            # closing line is implied by closePath
        for s in segs:
            if len(s) == 2:
                pen.lineTo(s[1])
            else:
                pen.curveTo(s[1], s[2], s[3])
        pen.closePath()


def _info(ufo, m):
    i = ufo.info
    i.familyName = P.FAMILY
    i.styleName = style_name(m)
    i.styleMapFamilyName = P.FAMILY if m.wght == 400 else f"{P.FAMILY} {m.weight_name}"
    i.styleMapStyleName = "italic" if m.italic else "regular"
    i.versionMajor, i.versionMinor = P.VERSION
    i.unitsPerEm = P.UPM
    i.capHeight, i.xHeight = P.CAP, P.XH
    i.ascender, i.descender = P.ASC, P.DESC
    i.italicAngle = -P.SLANT_DEG if m.italic else 0
    i.copyright = ("Copyright 2026 The Loligora Project Authors "
                   "(https://github.com/chx2974/Loligora)")
    i.openTypeNameDesigner = "Charlie Champanhet"
    i.openTypeNameManufacturer = "Charlie Champanhet"
    i.openTypeNameLicense = ("This Font Software is licensed under the SIL "
                             "Open Font License, Version 1.1. This license is "
                             "available with a FAQ at: https://openfontlicense.org")
    i.openTypeNameLicenseURL = "https://openfontlicense.org"
    i.openTypeOS2WeightClass = m.wght
    i.openTypeOS2VendorID = "NONE"
    i.openTypeOS2Type = []                      # installable embedding
    i.openTypeOS2Selection = [7]                # USE_TYPO_METRICS (italic bit comes from styleMapStyleName)
    i.openTypeOS2TypoAscender = P.LINE_ASC
    i.openTypeOS2TypoDescender = P.LINE_DESC
    i.openTypeOS2TypoLineGap = 0
    i.openTypeHheaAscender = P.LINE_ASC
    i.openTypeHheaDescender = P.LINE_DESC
    i.openTypeHheaLineGap = 0
    i.openTypeOS2WinAscent = P.WIN_ASC
    i.openTypeOS2WinDescent = P.WIN_DESC
    i.postscriptUnderlinePosition = -100
    i.postscriptUnderlineThickness = 50


def style_name(m, weight_name=None):
    """'Thin', 'Regular', 'Thin Italic', 'Italic' (Regular Italic -> Italic)."""
    w = weight_name or m.weight_name
    if not m.italic:
        return w
    return "Italic" if w == "Regular" else f"{w} Italic"


def _add_anchors(g, anchors):
    for k, (x, y) in anchors.items():
        g.appendAnchor({"name": k, "x": round(x), "y": round(y)})


def _alt_caron(ufo, m, name, uni, base):
    """d/l/t/L + vertical caron (`caronalt`) right of the stem top; advance widened."""
    from .composites import caron_alt_place
    g = ufo.newGlyph(name)
    g.unicodes = [uni]
    dx, dy, adv, k = caron_alt_place(ufo, m, base)
    g.width = adv
    pen = g.getPen()
    pen.addComponent(base, (1, 0, 0, 1, 0, 0))
    pen.addComponent("caronalt", (k, 0, 0, k, dx, dy))
    return name


def _place_composites(ufo, m):
    """Accented letters = base component + combining-mark component, offset so
    that the base anchor (top/bottom) meets the mark's `_top`/`_bottom`."""
    out = []
    for name, uni, base, acc, cap in composites.composites():
        if acc == "caronalt":
            out.append(_alt_caron(ufo, m, name, uni, base))
            continue
        mark = composites.ACCENTS[acc][1] + (composites.CASE if cap else "")
        if base not in ufo or mark not in ufo:
            continue            # (batches still in progress)
        an = composites.ANCHOR.get(acc, "top")
        b = {a.name: (a.x, a.y) for a in ufo[base].anchors}
        k = {a.name: (a.x, a.y) for a in ufo[mark].anchors}
        if an not in b:
            continue
        dx, dy = b[an][0] - k["_" + an][0], b[an][1] - k["_" + an][1]
        g = ufo.newGlyph(name)
        g.width = ufo[base].width
        g.unicodes = [uni]
        pen = g.getPen()
        pen.addComponent(base, (1, 0, 0, 1, 0, 0))
        pen.addComponent(mark, (1, 0, 0, 1, dx, dy))
        out.append(name)
    return out


def build_master(m, outdir):
    ufo = ufoLib2.Font()
    _info(ufo, m)
    order = []
    for mod in all_glyphs():
        res = mod.draw(m)
        adv, contours = res[0], res[1]
        g = ufo.newGlyph(mod.NAME)
        g.width = round(adv)
        if mod.UNI is not None:
            g.unicodes = [mod.UNI]
        _draw(g, contours)
        for c in (res[3] if len(res) > 3 else []):
            k = c[3] if len(c) > 3 else 1
            g.getPen().addComponent(c[0], (k, 0, 0, k, c[1], c[2]))
        _add_anchors(g, {**composites.base_anchors(mod.NAME, adv, m),
                         **composites.ogonek_anchor(mod.NAME, contours, m),
                         **(res[2] if len(res) > 2 else {})})
        order.append(mod.NAME)
    order += _place_composites(ufo, m)
    ufo["Eth"].unicodes = [0xD0, 0x110]            # Đ = Ð (D with bar)
    ufo.lib["public.glyphOrder"] = order
    ufo.features.text = features.text(order)
    kerning.install(ufo, m)
    path = Path(outdir) / f"{P.FILE}-{m.name.replace(' ', '')}.ufo"
    ufo.save(path, overwrite=True)
    return path


def build_designspace(outdir, italic=False):
    """3 UFO masters + designspace (STAT is written in build.py)."""
    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    masters = P.ITALIC_MASTERS if italic else P.MASTERS
    doc = DesignSpaceDocument()
    doc.addAxis(AxisDescriptor(tag="wght", name="Weight", minimum=P.AXIS_MIN,
                               default=P.AXIS_DEFAULT, maximum=P.AXIS_MAX))
    for m in masters:
        path = build_master(m, outdir)
        doc.addSource(SourceDescriptor(
            filename=path.name, name=m.name, familyName=P.FAMILY,
            styleName=style_name(m), location={"Weight": m.wght}))
    for name, v in P.INSTANCES:
        st = style_name(masters[0], name)
        doc.addInstance(InstanceDescriptor(
            familyName=P.FAMILY, styleName=st, location={"Weight": v}))
    ds = outdir / (f"{P.FILE}-Italic.designspace" if italic
                   else f"{P.FILE}.designspace")
    doc.write(ds)
    return ds
