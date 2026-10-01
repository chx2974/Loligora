"""Verify tabular figures: every digit has the same advance width in every
master UFO (3 upright + 3 italic) and in both variable fonts instanced at
several weights.

Exit code 1 on any failure.
"""
import sys
from pathlib import Path

import ufoLib2
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from loligora.params import DIGIT_WIDTH, PUNCT_WIDTH  # noqa: E402

DIGITS = ["zero", "one", "two", "three", "four", "five", "six", "seven",
          "eight", "nine"]
PUNCT = ["period", "comma"]
# tabular maths, currency signs and figure space: DIGIT_WIDTH in every master
TABULAR = ["plus", "minus", "equal", "less", "greater", "plusminus", "multiply", "divide",
           "logicalnot", "figurespace", "Euro", "sterling", "yen", "cent", "dollar",
           "currency", "florin"]
TTFS = {"upright": ROOT / "fonts" / "variable" / "Loligora[wght].ttf",
        "italic": ROOT / "fonts" / "variable" / "Loligora-Italic[wght].ttf"}
WEIGHTS = [100, 250, 400, 700, 950]


def check(label, widths, failures):
    digits = {g: widths.get(g) for g in DIGITS if g in widths}
    punct = {g: widths.get(g) for g in PUNCT if g in widths}
    ok_d = set(digits.values()) == {DIGIT_WIDTH}
    ok_p = set(punct.values()) == {PUNCT_WIDTH}
    tab = {g: widths.get(g) for g in TABULAR}
    ok_t = set(tab.values()) == {DIGIT_WIDTH}          # all present and 580
    ok_p = ok_p and ok_t
    status = "OK  " if ok_d and ok_p else "FAIL"
    print(f"{status} {label:<22} digits={sorted(set(digits.values()), key=str)}"
          f" punct={sorted(set(punct.values()), key=str)}"
          f" maths/currency={sorted(set(tab.values()), key=str)}")
    for g, w in tab.items():
        if w != DIGIT_WIDTH:
            print(f"     {g}: {w}")
    if not (ok_d and ok_p):
        failures.append(label)


def check_pnum(label, widths, failures):
    """Proportional digits exist (unencoded) and 1 is narrower than tabular."""
    missing = [d for d in DIGITS if d + ".pnum" not in widths]
    ok = not missing and widths["one.pnum"] < DIGIT_WIDTH - 100
    print(f"{'OK  ' if ok else 'FAIL'} {label:<22} pnum one={widths.get('one.pnum')}"
          f" zero={widths.get('zero.pnum')} missing={missing}")
    if not ok:
        failures.append(label + " pnum")


def main():
    failures = []
    for ufo_path in sorted((ROOT / "build" / "sources").glob("*.ufo")):
        ufo = ufoLib2.Font.open(ufo_path)
        widths = {g.name: g.width for g in ufo}
        check(f"master {ufo_path.stem}", widths, failures)
        check_pnum(f"master {ufo_path.stem}", widths, failures)
    for style, ttf in TTFS.items():
        for w in WEIGHTS:
            inst = instantiateVariableFont(TTFont(ttf), {"wght": w})
            widths = {g: inst["hmtx"][g][0] for g in inst.getGlyphOrder()}
            check(f"{style} wght={w}", widths, failures)
            check_pnum(f"{style} wght={w}", widths, failures)
    if failures:
        print("FAILED:", ", ".join(failures))
        sys.exit(1)
    print(f"All digits, maths signs, currency signs and figure space = {DIGIT_WIDTH};"
          f" period/comma = {PUNCT_WIDTH}"
          " units in all 6 masters and in instances of both fonts.")


if __name__ == "__main__":
    main()
