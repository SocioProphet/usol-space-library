# Implementation Agent Handoff — v4 Migration

**Repo state:** v3 baseline with one pre-applied fix: the `scripts/generate_volume_plate.py` syntax bug is corrected. The target GitHub repository was empty, so Tranche 1 bootstraps the executable baseline before projection-layer work.

**Target:** v4 three-layer architecture: substrate / projection / curated books. See `docs/architecture/v4-industrial-spec.md` and `docs/architecture/tranche-plan.md`.

## Operational rules

1. Every tranche is a draft PR against `main`, not a direct commit, after the one-time empty-repo initializer.
2. Tranche N+1 starts only after Tranche N merges.
3. Substrate code never imports projection code. Projections attach to substrate outputs; they never mutate them.
4. The v3 CLI `python scripts/generate_volume_plate.py --volume VIII` must keep working through v4.
5. Every emitted artifact carries provenance; STAC output remains the artifact contract.
6. Every YAML projection declares its tier: `exact`, `placement`, `synthesis`, or `fails`.

## Handoff completion target

When all six tranches merge, v4 supports substrate-only plates, generic projection overlays, curated Books, non-Rev12 convergence reporting, precession and galactic-ecliptic modules with provenance, CI, and tutorial notebook 07.

## Out of scope

No changes to formal research repos. No new science claims. No interpretive content in the substrate layer.

## Quick-start sanity check

```bash
pip install -r requirements.txt
pip install -e .
python -m py_compile scripts/generate_volume_plate.py
pytest -q
python scripts/generate_volume_plate.py --help
```
