from dataclasses import dataclass
from typing import Optional

import pandas as pd


@dataclass
class Constraints:
    min_alt_deg: float = 20.0
    max_mag: Optional[float] = None
    max_airmass: Optional[float] = None
    sun_alt_max_deg: Optional[float] = -12.0


def apply_observability(df: pd.DataFrame, constraints: Constraints) -> pd.DataFrame:
    """Filter a Horizons ephemeris table using simple observability constraints."""
    def pick(*names):
        for name in names:
            for column in df.columns:
                if name.lower() in column.lower():
                    return column
        return None

    alt_col = pick("EL", "elev", "a-observer", "a-obs", "elevation")
    mag_col = pick("APmag", "T-mag", "mag")
    am_col = pick("airmass")
    sun_col = pick("sun alt", "SAlt", "S-Alt", "S-Oppo")

    keep = pd.Series(True, index=df.index)
    if alt_col is not None:
        keep &= pd.to_numeric(df[alt_col], errors="coerce") >= constraints.min_alt_deg
    if constraints.max_mag is not None and mag_col is not None:
        keep &= pd.to_numeric(df[mag_col], errors="coerce") <= constraints.max_mag
    if constraints.max_airmass is not None and am_col is not None:
        keep &= pd.to_numeric(df[am_col], errors="coerce") <= constraints.max_airmass
    if constraints.sun_alt_max_deg is not None and sun_col is not None:
        keep &= pd.to_numeric(df[sun_col], errors="coerce") <= constraints.sun_alt_max_deg
    return df[keep].copy()
