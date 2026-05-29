# USOL Sensor Suite Space Library — STATUS

**Updated:** 2026-05-29 14:40 UTC

## Current migration state

**v3+bugfix → v4 in progress (Tranche 1).**

The repository is being bootstrapped from the v4 handoff package. Tranche 1 locks the v3 baseline under CI before projection-layer work begins.

## Completed (v3)
- Repo scaffolding (MIT), docs for APIs & datasets.
- Horizons wrapper + parser to DataFrame.
- SBDB, CAD, SB_Ident wrappers.
- Observability filters (SBWObs-like).
- DIRBE: bilinear sampling & beam solid angle.
- FIRAS: Planck spectrum, residuals, plotting.
- End-to-end plate generator with STAC Item.
- **Per-volume kits**: Book VII, VIII, XI plate scripts & appendix emitters.
- Teaching polish: Notebook challenges.

## Completed in Tranche 1
- Restored executable v3 package baseline into an empty GitHub repository.
- Added editable package metadata via `pyproject.toml`.
- Added GitHub Actions CI for dependency install, compile check, and pytest.
- Added smoke tests for package importability and `generate_volume_plate.py --help`.
- Preserved the v4 architecture handoff as follow-on implementation direction.

## Next
- Projection layer foundation: `CulturalProjection`, YAML registry, and curated Book lookup.
- Three-mode CLI restructure: substrate-only, generic projection, curated book.
- Precession and galactic-ecliptic substrate modules with provenance.
- Cross-tradition convergence report and non-Rev12 projections.
- Comparative plates, quantities table, fetch helpers, tutorial notebook 07, and v4 release docs.
