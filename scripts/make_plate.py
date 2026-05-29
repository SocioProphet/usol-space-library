#!/usr/bin/env python3
import argparse
from pathlib import Path

import pandas as pd

from usolspace import horizons, sb_ident, sbdb
from usolspace.provenance import write_provenance


def main():
    ap = argparse.ArgumentParser(description="Generate a USOL plate CSV + provenance from Horizons/SB_Ident/SBDB")
    ap.add_argument("--target", default="499", help="Horizons COMMAND (e.g., '499' for Mars)")
    ap.add_argument("--site", default="500@399", help="Observer center (e.g., 500@399 geocenter)")
    ap.add_argument("--start", required=False, default="2025-09-01", help="START_TIME")
    ap.add_argument("--stop", required=False, default="2025-09-02", help="STOP_TIME")
    ap.add_argument("--step", required=False, default="1 d", help="STEP_SIZE")
    ap.add_argument("--quantities", default="1,9,20", help="Horizons QUANTITIES list")
    ap.add_argument("--fov-ra", type=float, default=0.0, help="FOV center RA (deg)")
    ap.add_argument("--fov-dec", type=float, default=0.0, help="FOV center Dec (deg)")
    ap.add_argument("--fov-w", type=float, default=2.0, help="FOV width (deg)")
    ap.add_argument("--fov-h", type=float, default=2.0, help="FOV height (deg)")
    ap.add_argument("--time", default="2025-09-01 00:00", help="UTC time for SB_Ident")
    ap.add_argument("--dry-run", action="store_true", help="Skip network calls; output mock CSV")
    args = ap.parse_args()

    out_dir = Path("artifacts")
    out_dir.mkdir(parents=True, exist_ok=True)
    csv_path = out_dir / "plate_example.csv"
    prov_path = out_dir / "plate_example.provenance.json"

    if args.dry_run:
        df = pd.DataFrame([{"example": "dry-run", "note": "Replace with real API calls"}])
        df.to_csv(csv_path, index=False)
        write_provenance(prov_path, vars(args), ["DRY_RUN"])
        print(f"Wrote {csv_path} (dry-run)")
        return

    horizons.ephemeris(args.target, args.site, args.start, args.stop, args.step, args.quantities)
    fov = sb_ident.identify(args.time, args.fov_ra, args.fov_dec, args.fov_w, args.fov_h, site=args.site)

    rows = []
    ids = []
    try:
        ids = [o.get("des") or o.get("full_name") or o.get("name") for o in fov.get("result", [])]
        ids = [i for i in ids if i]
    except Exception:
        ids = []

    for item in ids[:10]:
        try:
            info = sbdb.lookup(item)
            rows.append({
                "sstr": item,
                "H": info.get("object", {}).get("phys_par", {}).get("H"),
                "diameter_km": info.get("object", {}).get("phys_par", {}).get("diameter"),
            })
        except Exception:
            rows.append({"sstr": item, "H": None, "diameter_km": None})

    df = pd.DataFrame(rows if rows else [{"note": "No SB_Ident matches in FOV or API unavailable"}])
    df.to_csv(csv_path, index=False)
    write_provenance(
        prov_path,
        vars(args),
        [
            "https://ssd-api.jpl.nasa.gov/api/horizons.api",
            "https://ssd-api.jpl.nasa.gov/sb_ident.api",
            "https://ssd-api.jpl.nasa.gov/sbdb.api",
        ],
        stac_item_path=str(out_dir / "plate_example.stac-item.json"),
    )
    print(f"Wrote {csv_path}, {prov_path}, and STAC item")


if __name__ == "__main__":
    main()
