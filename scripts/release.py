"""Assemble dist/Loligora-v1.0.0/ and dist/Loligora-v1.0.0.zip.

Run via `make release` (which builds + checks first through the lock);
running this script directly also calls `make build` and `make check`.
"""
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TAG = "v1.0.0"
NAME = f"Loligora-{TAG}"
DIST = ROOT / "dist"
OUT = DIST / NAME
FONTS = {"Loligora[wght]": "normal", "Loligora-Italic[wght]": "italic"}

README = """# Loligora {tag} (font version 1.000)

Variable sans-serif, weight axis 100-950, upright and italic as two fonts.
Western and Central European Latin. License: SIL Open Font License 1.1 (OFL.txt).
Copyright 2026 The Loligora Project Authors (https://github.com/chx2974/Loligora).

## Contents

- `fonts/variable/`  Loligora[wght] and Loligora-Italic[wght], as .woff2 (web) and .ttf
- `fonts/static/`    static TTFs for the 9 named instances per style (if present)
- `css/loligora.css`  @font-face rules (copy css/ and fonts/ together, keep paths)
- `specimen/`        demo page; serve this folder, e.g.
  `python3 -m http.server 8080` and open http://localhost:8080/specimen/
- `OFL.txt`, `FONTLOG.txt`, `AUTHORS.txt`, `CONTRIBUTORS.txt`

## Usage

```html
<link rel="stylesheet" href="css/loligora.css">
<style> body {{ font-family: "Loligora", sans-serif; }} h1 {{ font-weight: 950; }} </style>
```

Figures are tabular by default; `font-variant-numeric: proportional-nums` (OpenType `pnum`) switches to proportional figures.

## Name notice

A formal trademark check for "Loligora" is still needed before public release.
"""


def make(target):
    r = subprocess.run(["make", target], cwd=ROOT)
    if r.returncode:
        sys.exit(f"make {target} failed, aborting release")


def statics(src_dir, out_dir):
    from fontTools.ttLib import TTFont
    from fontTools.varLib import instancer
    out_dir.mkdir(parents=True)
    n = 0
    for stem in FONTS:
        names = [(i.coordinates["wght"], i) for i in
                 TTFont(src_dir / f"{stem}.ttf")["fvar"].instances]
        for w, inst in names:
            f = TTFont(src_dir / f"{stem}.ttf")
            sub = f["name"].getDebugName(inst.subfamilyNameID).replace(" ", "")
            style = "Italic" if sub == "Italic" else sub  # already has "Italic"
            f = instancer.instantiateVariableFont(
                f, {"wght": w}, updateFontNames=True)
            nm = f["name"]  # PostScript name Loligora-<Style>; drop variations prefix (ID 25)
            nm.names = [r for r in nm.names if r.nameID not in (6, 25)]
            nm.setName(f"Loligora-{style}", 6, 3, 1, 0x409)
            f.save(out_dir / f"Loligora-{style}.ttf")
            n += 1
    return n


def main():
    if "--no-build" not in sys.argv:
        make("build")
        make("check")
    var = ROOT / "fonts" / "variable"
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "fonts/variable").mkdir(parents=True)
    for stem in FONTS:
        shutil.copy2(var / f"{stem}.ttf", OUT / "fonts/variable")
        shutil.copy2(var / f"{stem}.woff2", OUT / "fonts/variable")
    (OUT / "css").mkdir()
    shutil.copy2(ROOT / "css/loligora.css", OUT / "css")
    for f in ("OFL.txt", "FONTLOG.txt", "AUTHORS.txt", "CONTRIBUTORS.txt"):
        shutil.copy2(ROOT / f, OUT)
    (OUT / "README.md").write_text(README.format(tag=TAG))
    # specimen: same page and relative font paths as in the repo
    (OUT / "specimen").mkdir()
    html = (ROOT / "specimen/index.html").read_text()
    (OUT / "specimen/index.html").write_text(html)
    try:
        n = statics(var, OUT / "fonts/static")
        print(f"static instances: {n}")
    except Exception as e:  # static instances are optional
        shutil.rmtree(OUT / "fonts/static", ignore_errors=True)
        print(f"WARNING: static instances skipped: {e!r}")
    zp = DIST / f"{NAME}.zip"
    zp.unlink(missing_ok=True)
    with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
        for p in sorted(OUT.rglob("*")):
            if p.is_file():
                z.write(p, Path(NAME) / p.relative_to(OUT))
    print(f"wrote {zp} ({zp.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
