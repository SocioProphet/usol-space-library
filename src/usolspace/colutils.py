import pandas as pd

PREFS = {
    "altitude": ["EL", "elev", "elevation", "a-obs", "a-observer", "El."],
    "magnitude": ["APmag", "T-mag", "mag"],
    "airmass": ["airmass", "Airmass"],
    "time": ["Date__(UT)__HR:MN:SC", "Calendar Date (TDB)", "UTC", "Time (UT)"]
}


def pick_col(df: pd.DataFrame, role: str):
    wanted = PREFS.get(role, [])
    for w in wanted:
        for c in df.columns:
            if w.lower() in c.lower():
                return c
    return None
