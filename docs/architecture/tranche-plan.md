# v4 Migration — Tranche Plan

Six tranches, each a single draft PR. Each tranche must merge before the next begins.

## Tranche 1 — Foundation & CI

Goal: lock the working v3+bugfix baseline and put it under CI.

Files added or modified:
- `.github/workflows/ci.yml`
- `pyproject.toml`
- `tests/test_smoke.py`
- `STATUS.md`
- executable v3 baseline package, scripts, and tests because the target GitHub repo was empty.

Acceptance:
- CI runs on push and pull request.
- `python -m py_compile scripts/generate_volume_plate.py` exits 0.
- `pytest -q` exits 0.
- Smoke test imports every `usolspace` module and verifies `generate_volume_plate.py --help`.

Out of scope:
- Projection layer work.
- New substrate modules.
- New science claims.

## Tranche 2 — Projection Layer Foundation

Introduce `CulturalProjection`, YAML projections, and curated Book lookup for VII/VIII/XI without breaking the v3 CLI.

## Tranche 3 — CLI Restructure

Add three modes: substrate-only plate, generic projection, and curated book. The same target/window must produce invariant CSV data across modes.

## Tranche 4 — New Substrate Modules

Add precession, galactic-ecliptic geometry, and target registry as pure astronomy substrate modules with provenance.

## Tranche 5 — Cross-Tradition Coverage & Convergence

Add at least one non-Rev12 projection and a convergence-report mechanic.

## Tranche 6 — Polish, Comparative Plates, and v4 Release

Add comparative plates, quantities table, fetch helpers, tutorial notebook 07, README update, status update, and release metadata.

## Release acceptance checklist

- [ ] Syntax bug fixed; existing Books VII/VIII/XI run.
- [ ] Books are YAML-driven and backward-compatible.
- [ ] Substrate-only Mode A exists.
- [ ] Generic projection Mode B exists.
- [ ] Precession and galactic-ecliptic modules exist with provenance.
- [ ] CI is green.
- [ ] Tutorial notebook 07 demonstrates all three modes.
- [ ] At least one non-Rev12 projection is in the registry.
- [ ] `STATUS.md` marks v4 stable.
- [ ] README documents three-mode usage.
