"""Build everything: UFO masters -> fontmake variable TTFs -> WOFF2.

Usage: python -m loligora.build   (from src/, or via `make build`)
Produces fonts/variable/Loligora[wght].{ttf,woff2} and
Loligora-Italic[wght].{ttf,woff2}, linked through the STAT `ital` axis.
"""
import shutil
import subprocess
import sys
from pathlib import Path

from fontTools.otlLib.builder import buildStatTable
from fontTools.ttLib import TTFont, newTable
from fontTools.ttLib.tables import ttProgram

from . import params as P
from .ufo import build_designspace, style_name

ROOT = Path(__file__).resolve().parents[2]
SOURCES = ROOT / "build" / "sources"
OUT = ROOT / "fonts" / "variable"
REPO_SOURCES = ROOT / "sources"      # commit-ready copy (UFOs + designspaces)


def set_overlap_flags(font):
    """Mark glyphs as having overlaps (we keep overlapping contours)."""
    glyf = font["glyf"]
    for name in font.getGlyphOrder():
        g = glyf[name]
        if g.numberOfContours > 0:
            g.flags[0] |= 0x40          # OVERLAP_SIMPLE


def add_stat(font, italic):
    """STAT: wght (named weights, Regular linked to Bold) + ital (0/1, linked)."""
    wvals = []
    for name, v in P.INSTANCES:
        d = {"value": v, "name": name}
        if v == 400:
            d.update(flags=2, linkedValue=700)          # elidable
        wvals.append(d)
    ital = ({"value": 1, "name": "Italic"} if italic else
            {"value": 0, "name": "Roman", "flags": 2, "linkedValue": 1})
    axes = [{"tag": "wght", "name": "Weight", "values": wvals},
            {"tag": "ital", "name": "Italic", "values": [ital]}]
    buildStatTable(font, axes, elidedFallbackName="Regular")


def add_unhinted_tables(font):
    """Unhinted-font boilerplate: `gasp` (grayscale smoothing at all sizes) and
    a minimal `prep` that turns smart dropout control on."""
    gasp = newTable("gasp")
    gasp.version = 1
    gasp.gaspRange = {0xFFFF: 0x000F}
    font["gasp"] = gasp
    prep = newTable("prep")
    prep.program = ttProgram.Program()
    prep.program.fromBytecode(bytes([0xB8, 0x01, 0xFF, 0x85, 0xB0, 0x04, 0x8D]))
    font["prep"] = prep
    meta = newTable("meta")             # design / supported language scripts (ScriptLangTags)
    meta.data = {"dlng": "Latn", "slng": "Latn"}
    font["meta"] = meta


def fix_names(font, italic):
    """Drop legacy Mac (platform 1) names; add the variations PostScript name
    prefix (ID 25), which must end in 'Italic' for the italic."""
    name = font["name"]
    name.names = [n for n in name.names if n.platformID != 1]
    name.setName(P.FILE + ("Italic" if italic else ""), 25, 3, 1, 0x409)


def finish(ttf, italic):
    font = TTFont(ttf)
    set_overlap_flags(font)
    add_unhinted_tables(font)
    os2, head, post = font["OS/2"], font["head"], font["post"]
    if italic:
        os2.fsSelection = (os2.fsSelection | 1) & ~(1 << 6)   # ITALIC on, REGULAR off
        head.macStyle |= 2
        post.italicAngle = -P.SLANT_DEG
    else:
        os2.fsSelection = (os2.fsSelection & ~1) | (1 << 6)
        head.macStyle &= ~2
        post.italicAngle = 0
    add_stat(font, italic)
    fix_names(font, italic)     # after STAT, which adds Mac names
    font.save(ttf)
    font.flavor = "woff2"
    font.save(ttf.with_suffix(".woff2"))
    print("wrote", ttf.name, "and", ttf.with_suffix(".woff2").name)


def build(italic):
    ds = build_designspace(SOURCES, italic)
    suffix = "-Italic" if italic else ""
    ttf = OUT / f"{P.FILE}{suffix}[wght].ttf"
    cmd = [sys.executable, "-m", "fontmake", "-m", str(ds), "-o", "variable",
           "--output-path", str(ttf), "--flatten-components"]
    print("$", " ".join(cmd))
    subprocess.run(cmd, check=True)
    finish(ttf, italic)


def export_sources():
    """Copy the generated UFO masters + designspaces to sources/ (config.yaml stays)."""
    REPO_SOURCES.mkdir(exist_ok=True)
    for old in list(REPO_SOURCES.glob("*.ufo")) + list(REPO_SOURCES.glob("*.designspace")):
        shutil.rmtree(old) if old.is_dir() else old.unlink()
    for src in sorted(SOURCES.iterdir()):
        if src.suffix == ".ufo":
            shutil.copytree(src, REPO_SOURCES / src.name)
        elif src.suffix == ".designspace":
            shutil.copy2(src, REPO_SOURCES / src.name)
    print("exported sources to", REPO_SOURCES)


def main():
    shutil.rmtree(SOURCES, ignore_errors=True)
    if "sources" in sys.argv[1:]:       # sources only, no font build
        build_designspace(SOURCES, False)
        build_designspace(SOURCES, True)
        export_sources()
        return
    OUT.mkdir(parents=True, exist_ok=True)
    build(False)
    build(True)
    export_sources()


if __name__ == "__main__":
    main()
