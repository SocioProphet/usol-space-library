# USOL Space Library — v4 Industrial Architecture

## Purpose

v4 reorganizes the library into three coexisting layers without changing the scientific substrate:

1. **Layer 1 — Substrate:** pure ephemeris, observability, background, and provenance code.
2. **Layer 2 — Projection:** optional `CulturalProjection` data attached to substrate outputs.
3. **Layer 3 — Curated Books:** named convenience entries that reference projection YAML and default observation recipes.

The substrate-only mode is load-bearing. Users who want only JPL/SSD-derived ephemeris data must not need the cultural-projection layer.

## Inviolable rule

Layer 1 substrate code never imports Layer 2 projection code. Projections attach to substrate artifacts; they never mutate the CSV data, column names, or provenance facts emitted by substrate code.

## Projection object target

```python
@dataclass
class CulturalProjection:
    name: str
    tradition: str
    archetype: str
    target_jpl_id: str
    tier: Literal["exact", "placement", "synthesis", "fails"]
    citation: str
    commentary_md: str
    related: list[str] = field(default_factory=list)
```

Every YAML projection must declare `tier`. Untagged projections are invalid. Only `exact` and `placement` projections can be promoted into the curated Book series.

## Three modes

Mode A: substrate-only plate.

```bash
python -m usolspace plate --target 10 --center 500@399 --start 2025-09-01 --stop 2025-09-02 --step 1d
```

Mode B: generic projection.

```bash
python -m usolspace project --target 10 --center 500@399 --start 2025-09-01 --stop 2025-09-02 --step 1d --projection data/projections/rev12-sun-bride.yaml
```

Mode C: curated Book.

```bash
python -m usolspace book VIII
```

Modes A, B, and C must produce invariant CSV data for the same target and date window. Only commentary/report artifacts differ.

## Non-claims

v4 does not validate any tradition, replace peer-reviewed astronomy, require users to engage with projections, or depend on the formal research repos. It provides a reproducible substrate and an auditable overlay mechanism.

## Acceptance criteria

v4 is accepted when Books VII/VIII/XI are YAML-driven and backward-compatible, all three modes exist, precession and galactic-ecliptic modules emit provenance-bearing artifacts, CI is green, tutorial notebook 07 exists, at least one non-Rev12 projection is present, and release docs mark v4 stable.
