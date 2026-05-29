# v4 Migration — Tranche Plan

Six tranches, each a single draft PR. Each tranche must merge before the next begins.

## Tranche 1 — Foundation & CI

Goal: lock the working v3+bugfix baseline and put it under CI.

Status: merged.

Acceptance:
- CI runs on push and pull request.
- `python -m py_compile scripts/generate_volume_plate.py` exits 0.
- `pytest -q` exits 0.
- Smoke test imports every `usolspace` module and verifies `generate_volume_plate.py --help`.

## Tranche 2 — Projection Layer Foundation

Goal: introduce `CulturalProjection`, YAML projections, and curated Book lookup for VII/VIII/XI without breaking the v3 CLI.

Files added or modified:
- `src/usolspace/projection.py`
- `src/usolspace/books.py`
- `data/projections/*.yaml`
- `data/books/*.yaml`
- projection/book/boundary tests
- `STATUS.md`

Acceptance:
- Projection YAML loads into a typed `CulturalProjection` object.
- Projection tiers are validated against `exact`, `placement`, `synthesis`, and `fails`.
- Curated Books VII/VIII/XI resolve to curatable projection tiers only.
- Book target and projection target must match.
- Substrate modules do not import projection or book modules.
- The existing v3 volume script remains untouched and backward-compatible.

Out of scope:
- Three-mode CLI.
- New substrate astronomy modules.
- Non-Rev12 projection registry.

## Tranche 3 — CLI Restructure

Add three modes: substrate-only plate, generic projection, and curated book. The same target/window must produce invariant CSV data across modes.

## Tranche 4 — New Substrate Modules

Add precession, galactic-ecliptic geometry, and target registry as pure astronomy substrate modules with provenance.

## Tranche 5 — Cross-Tradition Coverage & Convergence

Add at least one non-Rev12 projection and a convergence-report mechanic.

## Tranche 6 — Polish, Comparative Plates, and v4 Release

Add comparative plates, quantities table, fetch helpers, tutorial notebook 07, README update, status update, and release metadata.

## Release acceptance checklist

- [x] Syntax bug fixed; existing Books VII/VIII/XI run.
- [x] Books have YAML registry foundation.
- [ ] Books are routed through YAML in CLI.
- [ ] Substrate-only Mode A exists.
- [ ] Generic projection Mode B exists.
- [ ] Precession and galactic-ecliptic modules exist with provenance.
- [ ] CI is green.
- [ ] Tutorial notebook 07 demonstrates all three modes.
- [ ] At least one non-Rev12 projection is in the registry.
- [ ] `STATUS.md` marks v4 stable.
- [ ] README documents three-mode usage.
