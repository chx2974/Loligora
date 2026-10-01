"""OpenType feature code (besides kern and mark/mkmk, which ufo2ft writes from
the kerning groups and the glyph anchors).

`case` swaps spacing accents / combining marks to their capital-height forms;
`calt` swaps a combining mark that follows a capital (or another case mark)
to its `.case` form, so decomposed text matches the precomposed glyphs."""
from . import composites as C

DIGITS = ["zero", "one", "two", "three", "four", "five", "six", "seven",
          "eight", "nine"]


def text(order):
    have = set(order)
    comb = [c for c in C.COMBINING if c in have and c + C.CASE in have]
    sp = [a[0] for a in C.ACCENTS.values() if a[0] in have and a[0] + C.CASE in have]
    if not comb:
        return ""
    dg = [d for d in DIGITS if d in have and d + ".pnum" in have]
    # Without explicit language systems the kern feature is compiled for `latn`
    # only and mark/mkmk/calt/case stay in DFLT, so shapers never apply them
    # to Latin text (marks then sit at the pen position, off to the right).
    uc = [g for g in C.UC if g in have] + [n for n, _, _, _, cap in C.composites() if cap]
    return "\n".join([
        "languagesystem DFLT dflt;",
        "languagesystem latn dflt;",
        f"@UC = [{' '.join(uc)}];",
        f"@comb = [{' '.join(comb)}];",
        f"@comb_case = [{' '.join(c + C.CASE for c in comb)}];",
        f"@sp = [{' '.join(sp)}];",
        f"@sp_case = [{' '.join(a + C.CASE for a in sp)}];",
        "feature calt {",
        "    sub [@UC @comb_case] @comb' by @comb_case;",
        "} calt;",
        "feature case {",
        "    sub @sp by @sp_case;",
        "    sub @comb by @comb_case;",
        "} case;",
        f"@dg = [{' '.join(dg)}];",
        f"@dg_pnum = [{' '.join(d + '.pnum' for d in dg)}];",
        "feature pnum {",
        "    sub @dg by @dg_pnum;",
        "} pnum;",
        "feature tnum {",
        "    sub @dg_pnum by @dg;",
        "} tnum;", ""])
