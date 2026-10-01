"""Verify that every target code point is mapped in both variable fonts.

Target: Basic Latin (U+0020-007E), Latin-1 Supplement (U+00A0-00FF) and
Œ œ Š š Ž ž Ÿ ƒ ı ˆ ˜ – — ‘ ’ ‚ “ ” „ † ‡ • … ‰ ‹ › € ™ − and U+2007
(figure space). Also checks the combining marks and that every glyph the cmap
points to exists. Exit code 1 on failure.
"""
import sys
from pathlib import Path

from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parents[1]
TTFS = {"upright": ROOT / "fonts" / "variable" / "Loligora[wght].ttf",
        "italic": ROOT / "fonts" / "variable" / "Loligora-Italic[wght].ttf"}
EXTRAS = [0x152, 0x153, 0x160, 0x161, 0x17D, 0x17E, 0x178, 0x192, 0x131, 0x2C6, 0x2DC,
          0x2013, 0x2014, 0x2018, 0x2019, 0x201A, 0x201C, 0x201D, 0x201E, 0x2020, 0x2021,
          0x2022, 0x2026, 0x2030, 0x2039, 0x203A, 0x20AC, 0x2122, 0x2212, 0x2007, 0x25CC]
ACCENT_EXTRAS = [0x2C7, 0x2DA, 0x300, 0x301, 0x302, 0x303, 0x304, 0x308, 0x30A, 0x30C, 0x327]
ACCENT_EXTRAS += [0x2D8, 0x2D9, 0x2DB, 0x2DD, 0x306, 0x307, 0x30B, 0x326, 0x328]
TARGET = (list(range(0x20, 0x7F)) + list(range(0xA0, 0x100)) + EXTRAS + ACCENT_EXTRAS)
try:                       # Google Fonts "GF Latin Core" glyph set
    from glyphsets import unicodes_per_glyphset
    TARGET = sorted(set(TARGET) | set(unicodes_per_glyphset("GF_Latin_Core")))
except ImportError:
    pass


def main():
    failures = []
    for style, path in TTFS.items():
        f = TTFont(path)
        cmap = f.getBestCmap()
        missing = [c for c in TARGET if c not in cmap]
        broken = [hex(c) for c, g in cmap.items() if g not in f.getGlyphOrder()]
        n = len(f.getGlyphOrder())
        status = "OK  " if not missing and not broken else "FAIL"
        print(f"{status} {style}: {len(TARGET)} target code points, {len(cmap)} mapped, "
              f"{n} glyphs, missing: {['U+%04X' % c for c in missing] or 'none'}")
        if missing or broken:
            failures.append(style)
    if failures:
        print("FAILED:", ", ".join(failures))
        sys.exit(1)
    print(f"All {len(TARGET)} target code points are mapped in both fonts.")


if __name__ == "__main__":
    main()
