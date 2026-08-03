"""Nearby-star catalogue for the Space Twin 'cube of space' quadrant surface.

Factual astrometry — names, right ascension, declination, distance — for stars within ~40 light-years,
compiled from public catalogues (facts are uncopyrightable, Feist). Equatorial Cartesian positions with
Sol at the origin:

    x = d·cos(dec)·cos(ra),  y = d·cos(dec)·sin(ra),  z = d·sin(dec)   (light-years)

This module is the CANONICAL source for the client-vue quadrant surface: ``quadrant_payload()`` emits the
exact ``{"systems": [...]}`` shape that the live USOL endpoint serves and that the shipped initial-load
asset carries. The UI owns no star catalogue — it loads this.
"""

from __future__ import annotations

import math
from dataclasses import asdict, dataclass
from typing import Dict, List, Tuple

CUBE_LY = 40  # half-extent of the mapped cube (Sol-centred)

# Approximate black-body tint by spectral class.
_SPECTRAL: Dict[str, Tuple[int, int, int]] = {
    "O": (155, 176, 255), "B": (170, 191, 255), "A": (202, 215, 255), "F": (248, 247, 255),
    "G": (255, 236, 170), "K": (255, 210, 161), "M": (255, 163, 120),
}

# (name, RA hours, Dec degrees, distance ly, spectral class) — real stars within ~40 ly.
_RAW: List[Tuple[str, float, float, float, str]] = [
    ("Sol", 0.0, 0.0, 0.0, "G"),
    ("Alpha Centauri", 14.66, -60.83, 4.37, "G"),
    ("Barnard's Star", 17.96, 4.69, 5.96, "M"),
    ("Wolf 359", 10.94, 7.01, 7.86, "M"),
    ("Lalande 21185", 11.06, 35.97, 8.31, "M"),
    ("Sirius", 6.75, -16.72, 8.66, "A"),
    ("Luyten 726-8", 1.64, -17.95, 8.73, "M"),
    ("Ross 154", 18.83, -23.84, 9.68, "M"),
    ("Ross 248", 23.69, 44.18, 10.32, "M"),
    ("Epsilon Eridani", 3.55, -9.46, 10.48, "K"),
    ("Lacaille 9352", 23.09, -35.85, 10.74, "M"),
    ("Ross 128", 11.79, 0.80, 11.01, "M"),
    ("Procyon", 7.66, 5.22, 11.46, "F"),
    ("61 Cygni", 21.11, 38.75, 11.40, "K"),
    ("Tau Ceti", 1.73, -15.94, 11.90, "G"),
    ("Altair", 19.85, 8.87, 16.73, "A"),
    ("Eta Cassiopeiae", 0.82, 57.82, 19.42, "G"),
    ("Vega", 18.62, 38.78, 25.04, "A"),
    ("Fomalhaut", 22.96, -29.62, 25.13, "A"),
    ("Pollux", 7.76, 28.03, 33.78, "K"),
    ("Denebola", 11.82, 14.57, 35.90, "A"),
    ("Arcturus", 14.26, 19.18, 36.70, "K"),
]


@dataclass(frozen=True)
class StarSystem:
    id: str
    name: str
    position: List[float]  # [x, y, z] in light-years, Sol at origin
    color: List[int]       # [r, g, b]
    distLy: float
    spectral: str


def _slug(name: str) -> str:
    s = "".join(c.lower() if c.isalnum() else "-" for c in name)
    while "--" in s:
        s = s.replace("--", "-")
    return s.strip("-")


def _to_system(name: str, ra_h: float, dec_deg: float, dist_ly: float, spectral: str) -> StarSystem:
    ra = (ra_h / 24.0) * math.tau
    dec = math.radians(dec_deg)
    x = dist_ly * math.cos(dec) * math.cos(ra)
    y = dist_ly * math.cos(dec) * math.sin(ra)
    z = dist_ly * math.sin(dec)
    return StarSystem(
        id=_slug(name),
        name=name,
        position=[round(x, 4), round(y, 4), round(z, 4)],
        color=list(_SPECTRAL.get(spectral, (200, 200, 210))),
        distLy=round(dist_ly, 3),
        spectral=spectral,
    )


def nearby_stars() -> List[StarSystem]:
    """The catalogue as StarSystem records (Sol first, all within the cube)."""
    return [_to_system(*row) for row in _RAW]


def quadrant_payload() -> dict:
    """The exact wire shape the client-vue quadrant surface consumes (live + initial-load)."""
    return {
        "source": "usol.nearby_stars",
        "cube_ly": CUBE_LY,
        "systems": [asdict(s) for s in nearby_stars()],
    }
