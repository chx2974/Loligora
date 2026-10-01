"""Check that combining marks are centred on the base anchor, with real shaping.

For every base x mark x master weight (100/400/950) x upright/italic, shape
base+mark with HarfBuzz, measure the mark's ink centre (projected along the
slant to the anchor height) and compare it with the base's top/bottom anchor
read from the built masters. Also fails when the mark was not attached at all
(x offset 0: mark/mkmk feature missing for `latn`).
Pairs that HarfBuzz composes into a precomposed glyph are skipped (their
placement is derived from the same anchors in ufo.py).
Exit code 1 on any deviation > TOL units."""
import math
import sys
from pathlib import Path

import ufoLib2
import uharfbuzz as hb
from fontTools.pens.recordingPen import RecordingPen

ROOT = Path(__file__).resolve().parents[1]
TOL = 6.0
BASES = list("aeonAOSC") + ["u", "y", "d", "r", "i", "E", "Y"]
MARKS = {0x300: "top", 0x301: "top", 0x302: "top", 0x303: "top", 0x308: "top",
         0x304: "top", 0x30A: "top", 0x30C: "top", 0x327: "bottom",
         0x306: "top", 0x307: "top", 0x30B: "top", 0x326: "bottom", 0x328: "ogonek"}
MASTERS = {100: "Thin", 400: "Regular", 950: "ExtraBlack"}
SLANT = math.tan(math.radians(9.0))


def anchors(ufo, name):
    return {a.name: (a.x, a.y) for a in ufo[name].anchors}


def ink_centre(font, gid, kind):
    pen = RecordingPen()
    font.draw_glyph_with_pen(gid, pen)
    pts = [p for _, args in pen.value for p in args]
    if kind == "ogonek":                       # right edge of the stem (its top edge)
        ymax = max(y for _, y in pts)
        x = max(x for x, y in pts if abs(y - ymax) < 1)
        return (x, ymax), (x, ymax)
    if kind == "bottom":                       # cedilla: centre of the stem (its top edge)
        ymax = max(y for _, y in pts)
        xs = [x for x, y in pts if abs(y - ymax) < 1]
        return (min(xs), ymax), (max(xs), ymax)
    lo = min(pts, key=lambda p: p[0])            # leftmost / rightmost ink points
    hi = max(pts, key=lambda p: p[0])
    return lo, hi


def main():
    bad = n = 0
    for italic in (False, True):
        path = ROOT / "fonts/variable" / ("Loligora-Italic[wght].ttf" if italic else "Loligora[wght].ttf")
        face = hb.Face(hb.Blob.from_file_path(str(path)))
        for w, wn in MASTERS.items():
            ufo = ufoLib2.Font.open(ROOT / "build/sources" / f"Loligora-{wn}{'Italic' if italic else ''}.ufo")
            font = hb.Font(face)
            font.set_variations({"wght": w})
            s = SLANT if italic else 0.0
            for base in BASES:
                for mk, kind in MARKS.items():
                    if base in "iy" and kind in ("bottom", "ogonek"):
                        continue
                    buf = hb.Buffer()
                    buf.add_str(base + chr(mk))
                    buf.guess_segment_properties()
                    hb.shape(font, buf, {})
                    if len(buf.glyph_infos) != 2:
                        continue
                    (gb, gm), (pb, pm) = buf.glyph_infos, buf.glyph_positions
                    bname = font.glyph_to_string(gb.codepoint)
                    if kind not in anchors(ufo, bname):
                        continue
                    an = anchors(ufo, bname)[kind]
                    lo, hi = ink_centre(font, gm.codepoint, kind)
                    # project both extreme points along the slant to the anchor height
                    proj = sum(pb.x_advance + pm.x_offset + p[0] - s * (pm.y_offset + p[1] - an[1])
                               for p in (lo, hi)) / 2
                    n += 1
                    if pm.x_offset == 0 or abs(proj - an[0]) > TOL:
                        bad += 1
                        print(f"BAD {'it' if italic else 'up'} {w} {base}+U+{mk:04X}: "
                              f"centre {proj:.1f} vs anchor {an[0]:.1f} (offset {pm.x_offset})")
    print(f"check_marks: {n} pairs, {bad} off by more than {TOL:g} units")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
