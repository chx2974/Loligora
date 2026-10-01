"""Shared design parameters for Loligora (v2: neo-grotesque x superellipse).

Every glyph module receives a `Master` and reads numbers from it, so each
master is built by the same code with different values -> interpolation-
compatible outlines. Upright and italic masters use the same fields; italic
just has a non-zero slant `s` (see slant.py) and its own correction values.
"""
import math
from dataclasses import dataclass, field, replace

FAMILY = "Loligora"
FILE = "Loligora"          # file-name / PostScript-name prefix
VERSION = (1, 0)
UPM = 1000

# Vertical metrics (shared by all masters)
CAP = 720            # cap height (= lining figure height)
XH = 518             # x-height = 72% of cap (0.72 * 720 = 518.4)
ASC = 760            # ascender (l, b, d ...)
DESC = -200          # descender
OVERSHOOT = 12       # round overshoot above/below flat heights

LINE_ASC, LINE_DESC = 960, -240       # hhea / typo
WIN_ASC, WIN_DESC = 1000, 260

# Tabular figures: identical in ALL masters, upright and italic.
DIGIT_WIDTH = 580
PUNCT_WIDTH = 290    # period, comma

# Superellipse |x/a|^n + |y/b|^n = 1 : 2 = ellipse, ~3 = visible flat sides
# (halfway between Inter's ovals and Monda's squircles), inf = rectangle.
N_LETTER = 3.0
N_ZERO = 3.3         # zero is a bit squarer than O

# Italic
SLANT_DEG = 9.0
SLANT_TAN = math.tan(math.radians(SLANT_DEG))
ITAL_N_DELTA = -0.15     # slanted rounds get a slightly softer exponent (sharpens less at the acute corners)
ITAL_ROUND_W = 0.975     # optical width factor for slanted rounds (a sheared oval looks wider)

AXIS_MIN, AXIS_DEFAULT, AXIS_MAX = 100, 400, 950

INSTANCES = [
    ("Thin", 100), ("ExtraLight", 200), ("Light", 300), ("Regular", 400),
    ("Medium", 500), ("SemiBold", 600), ("Bold", 700), ("ExtraBold", 800),
    ("Black", 900),
]

_ORDER = ("Thin", "Regular", "ExtraBlack")


@dataclass(frozen=True)
class Master:
    weight_name: str        # Thin / Regular / ExtraBlack
    wght: int
    italic: bool
    stem_uc: float          # vertical stem, capitals
    stem_lc: float          # vertical stem, lowercase
    h_uc: float             # horizontal stroke, capitals
    h_lc: float
    stem_dg: float          # vertical stroke, digits (thinner at heavy end)
    h_dg: float
    sb_uc: float            # side bearings
    sb_lc: float
    sb_dg: float
    join: float = 0.86      # join thinning: arch/bowl stroke = join * stem
    y0: float = XH / 2      # shear origin (height that does not move)
    extra: dict = field(default_factory=dict)

    # -- derived ---------------------------------------------------------
    @property
    def name(self):
        """UFO/style name: 'Thin', 'Regular', 'ExtraBlack' (+ ' Italic')."""
        return self.weight_name + (" Italic" if self.italic else "")

    @property
    def s(self):
        """tan(slant): x shift per unit height. 0 for upright."""
        return SLANT_TAN if self.italic else 0.0

    def n(self, base=N_LETTER):
        """Superellipse exponent, softened a little for slanted rounds."""
        return base + (ITAL_N_DELTA if self.italic else 0.0)

    @property
    def round_w(self):
        return ITAL_ROUND_W if self.italic else 1.0

    def sh(self, x, y):
        """Upright design coordinate -> final (slanted) point."""
        return (x + self.s * (y - self.y0), y)

    def origin(self, y0):
        """Copy with another shear origin (caps/digits use CAP/2)."""
        return replace(self, y0=y0)

    def pick(self, thin, regular, black):
        return (thin, regular, black)[_ORDER.index(self.weight_name)]


_W = {  # per weight: stem_uc, stem_lc, h_uc, h_lc, stem_dg, h_dg, sb_uc, sb_lc, sb_dg
    "Thin":       (24, 22, 22, 20, 22, 20, 88, 62, 62),
    "Regular":    (92, 86, 80, 74, 84, 74, 88, 60, 56),
    "ExtraBlack": (196, 180, 150, 136, 150, 122, 66, 44, 38),
}
_WGHT = {"Thin": 100, "Regular": 400, "ExtraBlack": 950}


def _masters(italic):
    return [Master(n, _WGHT[n], italic, *_W[n]) for n in _ORDER]


MASTERS = _masters(False)
ITALIC_MASTERS = _masters(True)
