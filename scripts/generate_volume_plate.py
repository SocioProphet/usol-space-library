#!/usr/bin/env python3
import argparse
from pathlib import Path

import pandas as pd

from usolspace.colutils import pick_col
from usolspace.horizons import ephemeris
from usolspace.horizons_parser import parse_table
from usolspace.observability import Constraints, apply_observability
from usolspace.plothelpers import plot_altitude
from usolspace.provenance import write_provenance


def run_volume(command: str, center: str, start: str, stop: str, step: str, quantities: str, volume_code: str, title: str):
    out = Path(f"artifacts/{volume_code}")
    out.mkdir(parents=True, exist_ok=True)
    prov = out / f"{volume_code}.provenance.json"
    stac = out / f"{volume_code}.stac-item.json"
    csv = out / f"{volume_code}.csv"
    png = out / f"{volume_code}.altitude.png"
    md = out / f"{volume_code}_appendix.md"

    res = ephemeris(command, center, start, stop, step, quantities)
    df = parse_table(res.get("result", ""))
    if df.empty:
        df = pd.DataFrame([{"note": "No rows parsed from Horizons result."}])
        df.to_csv(csv, index=False)
        write_provenance(prov, locals(), ["https://ssd-api.jpl.nasa.gov/api/horizons.api"], stac_item_path=str(stac))
        md.write_text(f"# {title} Appendix\nNo data available.\n")
        return

    df_obs = apply_observability(df, Constraints(min_alt_deg=15.0, sun_alt_max_deg=-6.0))
    df_obs.to_csv(csv, index=False)

    tcol = pick_col(df_obs, "time")
    acol = pick_col(df_obs, "altitude")
    if tcol and acol:
        plot_altitude(df_obs, tcol, acol, f"{title} — Altitude vs. Time", str(png))

    md.write_text(f"""# {title} — Appendix
- COMMAND: {command}
- CENTER: {center}
- START/STOP/STEP: {start} → {stop} / {step}
- QUANTITIES: {quantities}

Artifacts:
- CSV: {csv}
- Plot: {png if (tcol and acol) else 'n/a'}
- STAC: {stac}
""")

    write_provenance(
        prov,
        {"command": command, "center": center, "start": start, "stop": stop, "step": step, "quantities": quantities},
        ["https://ssd-api.jpl.nasa.gov/api/horizons.api"],
        stac_item_path=str(stac),
    )


def main():
    ap = argparse.ArgumentParser(description="Per-volume pipeline runner")
    ap.add_argument("--volume", required=True, choices=["VII", "VIII", "XI"])
    ap.add_argument("--center", default="500@399")
    ap.add_argument("--start", default="2025-09-01")
    ap.add_argument("--stop", default="2025-09-02")
    ap.add_argument("--step", default="1 d")
    ap.add_argument("--quantities", default="1,9,20")
    args = ap.parse_args()

    if args.volume == "VII":
        run_volume(
            command="499",
            center=args.center,
            start=args.start,
            stop=args.stop,
            step=args.step,
            quantities=args.quantities,
            volume_code="BookVII",
            title="Book VII — The Mother & the Son",
        )
    elif args.volume == "VIII":
        run_volume(
            command="10",
            center=args.center,
            start=args.start,
            stop=args.stop,
            step=args.step,
            quantities=args.quantities,
            volume_code="BookVIII",
            title="Book VIII — The Sun & the Bride",
        )
    elif args.volume == "XI":
        run_volume(
            command="301",
            center=args.center,
            start=args.start,
            stop=args.stop,
            step=args.step,
            quantities=args.quantities,
            volume_code="BookXI",
            title="Book XI — The Crown",
        )


if __name__ == "__main__":
    main()
