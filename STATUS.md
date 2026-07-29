# USOL Sensor Suite Space Library — STATUS

**Updated:** 2026-05-29 20:20 UTC

## Current migration state

**v4 in progress (Tranche 2).**

Tranche 1 merged the executable v3+bugfix baseline and CI. Tranche 2 introduces the projection-layer foundation while preserving substrate/projection separation.

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

## Added in Tranche 2
- `CulturalProjection` dataclass and YAML projection loader.
- Curated Book registry helpers for Books VII, VIII, and XI.
- Initial YAML projections for Revelation 12 overlays.
- Tests for projection loading, invalid tiers, duplicate registries, Book/projection target matching, and substrate/projection boundary enforcement.

## Next
- Three-mode CLI restructure: substrate-only, generic projection, curated book.
- Precession and galactic-ecliptic substrate modules with provenance.
- Cross-tradition convergence report and non-Rev12 projections.
- Comparative plates, quantities table, fetch helpers, tutorial notebook 07, and v4 release docs.
