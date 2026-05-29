# USOL Sensor Suite Space Library

A first-class, reproducible **learning system** that fuses **JPL/SSD** near-field dynamics
(Horizons, SBDB, SBWObs, SB_Ident) with **COBE/LAMBDA** far-field backgrounds (DIRBE, FIRAS)
to make the universe **calculable** for everyone.

## Features
- **Horizons**: high-precision ephemerides (JSON API).
- **SBDB / SBDB Query / CAD**: identity, orbit & approach metadata.
- **SBWObs**: forward observability.
- **SB_Ident**: reverse identification by field-of-view (FOV).
- **DIRBE / FIRAS**: infrared & microwave sky baselines via FITS/HEALPix.
- **Plates**: reproducible CSV outputs with provenance.
- **Notebooks**: step-by-step learning modules.
- **Provenance**: every artifact carries parameters & source references.

## Quickstart
```bash
# Python 3.10+ recommended
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pip install -e .

# Run an example plate (dry-run uses small mock inputs)
python scripts/make_plate.py --target '499' --start '2025-09-01' --stop '2025-09-02' --step '1 d' --site '500@399' --quantities '1,9,20'
```

## Data Sources (Authoritative)
- JPL Horizons API (JSON): see `docs/apis/horizons.md`
- SBDB (lookup & query): see `docs/apis/sbdb.md`
- SBWObs & SB_Ident: see `docs/apis/sbwobs_sbident.md`
- LAMBDA DIRBE & FIRAS: see `docs/datasets/dirbe.md`, `docs/datasets/firas.md`

All examples include **citations & parameters** for reproducibility.

---

© 2025-08-29 USOL. Licensed MIT. See `LICENSE`.

## New in this edition
- **Horizons table parser** → tidy DataFrames from JSON `result` blocks.
- **Observability engine** → SBWObs-like filters (altitude, magnitude, sun-altitude).
- **DIRBE interpolation & beam** → bilinear sampling + Gaussian beam solid angle helper.
- **FIRAS utilities** → Planck law, residuals, and plotting.
- **STAC provenance** → optional STAC Item emitted alongside every plate.
- **Notebook challenges** → guided exercises to cement learning.

## Per-Volume Kits
Run a complete plate for a USOL volume:
```bash
python scripts/generate_volume_plate.py --volume VII   # The Mother & the Son
python scripts/generate_volume_plate.py --volume VIII  # The Sun & the Bride
python scripts/generate_volume_plate.py --volume XI    # The Crown
```
Artifacts land under `artifacts/<BookCode>/` with CSV, STAC, and an appendix markdown.

## v4 migration status

This repository is bootstrapped from the v4 handoff package. Tranche 1 locks the v3+bugfix baseline under CI before projection-layer work begins.
