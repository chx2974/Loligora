"""Glyph registry.

Every module in this package (not starting with `_`) is either ONE glyph:

    NAME = "H"           # glyph name
    UNI = 0x48           # code point or None
    def draw(m): ...     # m = params.Master -> (advance, [contour, ...])

or several: `GLYPHS = [(name, unicode-or-None, draw), ...]` (used by the
Western-European additions: punctuation, maths, accents ...).

draw() may return extra items: (advance, contours, anchors, components) where
anchors = {"top": (x, y), ...} and components = [(glyphname, dx, dy)]
or (glyphname, dx, dy, scale). Composite accented letters are NOT modules:
see composites.py (built in ufo.py from anchors).

File names use prefixes because macOS is case-insensitive: uc_H.py, lc_o.py,
fig_zero.py, punct_period.py, misc_notdef.py ...
"""
import pkgutil
from importlib import import_module
from types import SimpleNamespace


def all_glyphs():
    """Glyph objects (NAME, UNI, draw): .notdef first, then space, then by module."""
    out = []
    for i in pkgutil.iter_modules(__path__):
        if i.name.startswith("_"):
            continue
        mod = import_module(f"{__name__}.{i.name}")
        if hasattr(mod, "GLYPHS"):
            out += [(i.name, SimpleNamespace(NAME=n, UNI=u, draw=d))
                    for n, u, d in mod.GLYPHS]
        else:
            out.append((i.name, mod))
    out.sort(key=lambda t: (t[1].NAME != ".notdef", t[1].NAME != "space", t[0]))
    return [g for _, g in out]
