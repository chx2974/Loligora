"""Render PNG proofs of the variable font at several weights.

Writes specimen/proofs/proof-<wght>.png (text lines) and
specimen/proofs/waterfall.png (one line per named weight).
"""
from pathlib import Path

import freetype
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
FONTS = {False: ROOT / "fonts" / "variable" / "Loligora[wght].ttf",
         True: ROOT / "fonts" / "variable" / "Loligora-Italic[wght].ttf"}
OUT = ROOT / "specimen" / "proofs"

LINES = ["HOnol", "HOHnonol HOnol", "0110 1,010.10", "100.01 1,001.00",
         "HHOOnnooll", "lol non hoho", "111.11 0,000.10", "Hoo 1011 lolo"]
CONTROL = "HOnol 01 HOHnonol 1,010.10"


def face_at(wght, italic=False):
    face = freetype.Face(str(FONTS[italic]))
    face.set_var_design_coords((wght,))
    return face


def render_line(face, text, size):
    """Return an L-mode image of one line of text (black on white)."""
    face.set_char_size(size * 64)
    asc = int(face.size.ascender / 64) + 4
    desc = int(-face.size.descender / 64) + 4
    width = 20
    for ch in text:
        face.load_char(ch, freetype.FT_LOAD_NO_HINTING)
        width += face.glyph.advance.x >> 6
    img = Image.new("L", (width + 20, asc + desc), 255)
    x = 10
    for ch in text:
        face.load_char(ch, freetype.FT_LOAD_RENDER | freetype.FT_LOAD_NO_HINTING)
        g = face.glyph
        bm = g.bitmap
        if bm.width and bm.rows:
            glyph_img = Image.frombytes("L", (bm.width, bm.rows), bytes(bm.buffer))
            ink = Image.new("L", glyph_img.size, 0)
            img.paste(ink, (x + g.bitmap_left, asc - g.bitmap_top), glyph_img)
        x += g.advance.x >> 6
    return img


def stack(images, pad=6, right=False):
    w = max(i.width for i in images)
    h = sum(i.height + pad for i in images)
    out = Image.new("L", (w, h), 255)
    y = 0
    for i in images:
        out.paste(i, (w - i.width if right else 0, y))
        y += i.height + pad
    return out


def label(img, text):
    ImageDraw.Draw(img).text((img.width - 60, 4), text, fill=140)
    return img


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for italic in (False, True):
        sfx = "-italic" if italic else ""
        for wght in (100, 400, 950):
            face = face_at(wght, italic)
            imgs = [render_line(face, t, 72) for t in LINES]
            path = OUT / f"proof-{wght}{sfx}.png"
            label(stack(imgs), str(wght)).save(path)
            print("wrote", path)
        rows = [label(render_line(face_at(w, italic), "HOnol 0110 1,010.10", 48),
                      str(w)) for w in (100, 200, 300, 400, 500, 600, 700, 800, 900, 950)]
        stack(rows, 2).save(OUT / f"waterfall{sfx}.png")
    # control.png: HOnol sample at 100/400/950, upright then italic
    rows = [render_line(face_at(w, it), CONTROL, 96)
            for it in (False, True) for w in (100, 400, 950)]
    stack(rows, 4).save(OUT / "control.png")
    # numbers column: right-aligned, shows tabular alignment across weights
    cols = []
    for italic in (False, True):
        for wght in (100, 400, 950):
            face = face_at(wght, italic)
            cols.append(stack([render_line(face, t, 48) for t in
                               ("1,010.10", "100.01", "111.11", "0,001.00")], 0, right=True))
    w = max(c.width for c in cols)
    grid = Image.new("L", (w * 3 + 40, max(c.height for c in cols) * 2 + 10), 255)
    for n, c in enumerate(cols):
        grid.paste(c, ((n % 3) * (w + 20), (n // 3) * (c.height + 10)))
    grid.save(OUT / "numbers.png")
    print("wrote control.png, waterfalls, numbers.png")


if __name__ == "__main__":
    main()
