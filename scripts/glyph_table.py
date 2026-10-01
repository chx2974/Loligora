"""Write specimen/glyphs.json: every glyph with name, code point, group, advances
at 100/400/950, outline SVG path (default master) and, for unencoded glyphs, the
GSUB feature + input glyph that reaches them."""
import json
import sys
import unicodedata
from pathlib import Path

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

ROOT = Path(__file__).resolve().parents[1]
UP = ROOT / "fonts" / "variable" / "Loligora[wght].ttf"
IT = ROOT / "fonts" / "variable" / "Loligora-Italic[wght].ttf"
OUT = ROOT / "specimen" / "glyphs.json"
WEIGHTS = (100, 400, 950)
SYMBOL_CATS = ("Sc", "Sk", "So", "Pc")
SPACES = (0x20, 0xA0, 0x2007)
MARK_HELPERS = ("commaaccent", "commaturn", "caronalt")   # unencoded accent helpers


def group(cp):
    if cp is None:
        return "Other / unencoded"
    ch = chr(cp)
    cat = unicodedata.category(ch)
    if cp in SPACES or cat == "Zs":
        return "Spaces"
    if cat.startswith("M") or cat == "Lm" or (cat == "Sk" and cp in (0x2C6, 0x2C7, 0x2DA, 0x2DC, 0xA8, 0xAF, 0xB4, 0xB8, 0x60, 0x5E)):
        return "Marks"
    if cat == "Nd":
        return "Figures"
    if cat in ("Lu", "Ll", "Lo"):
        base = unicodedata.normalize("NFD", ch)
        accented = len(base) > 1
        if not accented and cp in (0xC6, 0x152, 0xD0, 0xDE, 0x178, 0x1E9E, 0x160, 0x17D):
            accented = cp in (0x178, 0x160, 0x17D)
        if cat == "Lu":
            return "Accented uppercase" if accented else "Uppercase"
        return "Accented lowercase" if accented else "Lowercase"
    if cat == "No":
        return "Figures"
    if cat == "Sm" or cp in (0xD7, 0xF7, 0x2212, 0xB1, 0xAC):
        return "Maths"
    if cat == "Sc":
        return "Symbols & currency"
    if cat.startswith("P") or cat == "Cf":
        return "Punctuation"
    if cat.startswith("S"):
        return "Symbols & currency"
    return "Other / unencoded"


def advances(path):
    out = {}
    for w in WEIGHTS:
        f = TTFont(path)
        inst = instancer.instantiateVariableFont(f, {"wght": w}, inplace=False)
        out[w] = {n: inst["hmtx"][n][0] for n in inst.getGlyphOrder()}
    return out


def reach(font):
    """glyph -> list of 'feature: input' from single substitutions, or contextual."""
    gsub = font["GSUB"].table if "GSUB" in font else None
    res = {}
    if not gsub:
        return res
    lookups = gsub.LookupList.Lookup

    def singles(i, tag, seen, ctx):
        lk = lookups[i]
        for st in lk.SubTable:
            if lk.LookupType == 7:
                st = st.ExtSubTable
            t = type(st).__name__
            if t == "SingleSubst":
                for a, b in st.mapping.items():
                    res.setdefault(b, []).append((tag, a, ctx))
            elif t.startswith("Chain") or t.startswith("Context"):
                recs = []
                for attr in ("SubstLookupRecord", "SubstLookupRecord"):
                    pass
                for rs in (getattr(st, "ChainSubRuleSet", None) or getattr(st, "SubRuleSet", None) or
                           getattr(st, "ChainSubClassSet", None) or getattr(st, "SubClassSet", None) or []):
                    for r in rs or []:
                        rules = (getattr(r, "ChainSubRule", None) or getattr(r, "SubRule", None) or
                                 getattr(r, "ChainSubClassRule", None) or getattr(r, "SubClassRule", None) or [r])
                        recs += [x.LookupListIndex for x in getattr(r, "SubstLookupRecord", [])]
                for x in getattr(st, "SubstLookupRecord", []):
                    recs.append(x.LookupListIndex)
                for j in set(recs):
                    if j not in seen:
                        singles(j, tag, seen | {j}, True)

    for fr in gsub.FeatureList.FeatureRecord:
        for i in fr.Feature.LookupListIndex:
            singles(i, fr.FeatureTag, {i}, False)
    return res


def main():
    font = TTFont(UP)
    order = font.getGlyphOrder()
    cmap = font.getBestCmap()
    rev = {}
    for cp, n in sorted(cmap.items()):
        rev.setdefault(n, cp)
    adv = advances(UP)
    r = reach(font)
    gs = font.getGlyphSet()
    glyphs = []
    for n in order:
        cp = rev.get(n)
        pen = SVGPathPen(gs)
        gs[n].draw(TransformPen(pen, (1, 0, 0, -1, 0, 0)))
        e = {"name": n, "cp": cp, "group": "Marks" if n.endswith(".case") or n in MARK_HELPERS else "Figures" if n.endswith(".pnum") else group(cp),
             "adv": {str(w): adv[w][n] for w in WEIGHTS}, "path": pen.getCommands()}
        if cp is None and n in r:
            tag, src, ctx = r[n][0]
            e["feature"] = tag
            e["via"] = rev.get(src)
            e["viaName"] = src
            e["contextual"] = ctx
        glyphs.append(e)
    OUT.write_text(json.dumps({"upm": font["head"].unitsPerEm,
                               "italic": IT.exists(), "glyphs": glyphs}, separators=(",", ":")))
    counts = {}
    for g in glyphs:
        counts[g["group"]] = counts.get(g["group"], 0) + 1
    print(f"glyph_table: {len(glyphs)} glyphs -> {OUT.relative_to(ROOT)}", counts)


if __name__ == "__main__":
    sys.exit(main())
