"""Projection-layer data model and loader.

This module is intentionally separate from substrate modules such as
``horizons``, ``observability``, ``dirbe``, and ``firas``. Substrate code must
not import projection code. Projections annotate substrate outputs; they do not
mutate scientific data products.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal

import yaml

ProjectionTier = Literal["exact", "placement", "synthesis", "fails"]
ALLOWED_TIERS: set[str] = {"exact", "placement", "synthesis", "fails"}
CURATED_BOOK_TIERS: set[str] = {"exact", "placement"}


@dataclass(frozen=True)
class CulturalProjection:
    name: str
    tradition: str
    archetype: str
    target_jpl_id: str
    tier: ProjectionTier
    citation: str
    commentary_md: str
    related: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def is_curatable(self) -> bool:
        return self.tier in CURATED_BOOK_TIERS


def _require_string(data: dict[str, Any], key: str, path: Path) -> str:
    value = data.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{path}: projection field `{key}` must be a non-empty string")
    return value.strip()


def projection_from_dict(data: dict[str, Any], source: str | Path = "<memory>") -> CulturalProjection:
    path = Path(source) if not isinstance(source, Path) else source
    tier = _require_string(data, "tier", path)
    if tier not in ALLOWED_TIERS:
        raise ValueError(f"{path}: projection tier `{tier}` is invalid; expected one of {sorted(ALLOWED_TIERS)}")

    related_raw = data.get("related", [])
    if related_raw is None:
        related: list[str] = []
    elif isinstance(related_raw, list) and all(isinstance(item, str) for item in related_raw):
        related = list(related_raw)
    else:
        raise ValueError(f"{path}: projection field `related` must be a list of strings")

    metadata_raw = data.get("metadata", {})
    if metadata_raw is None:
        metadata: dict[str, Any] = {}
    elif isinstance(metadata_raw, dict):
        metadata = dict(metadata_raw)
    else:
        raise ValueError(f"{path}: projection field `metadata` must be a mapping")

    return CulturalProjection(
        name=_require_string(data, "name", path),
        tradition=_require_string(data, "tradition", path),
        archetype=_require_string(data, "archetype", path),
        target_jpl_id=_require_string(data, "target_jpl_id", path),
        tier=tier,  # type: ignore[arg-type]
        citation=_require_string(data, "citation", path),
        commentary_md=_require_string(data, "commentary_md", path),
        related=related,
        metadata=metadata,
    )


def load_projection(path: str | Path) -> CulturalProjection:
    projection_path = Path(path)
    raw = yaml.safe_load(projection_path.read_text())
    if not isinstance(raw, dict):
        raise ValueError(f"{projection_path}: projection YAML must contain a mapping")
    return projection_from_dict(raw, projection_path)


def load_projection_registry(directory: str | Path) -> dict[str, CulturalProjection]:
    registry_path = Path(directory)
    projections: dict[str, CulturalProjection] = {}
    for path in sorted(registry_path.glob("*.yaml")):
        projection = load_projection(path)
        if projection.name in projections:
            raise ValueError(f"duplicate projection name: {projection.name}")
        projections[projection.name] = projection
    return projections


def attach_projection_record(substrate_record: dict[str, Any], projection: CulturalProjection) -> dict[str, Any]:
    """Return a copied record with projection metadata attached.

    The input mapping is never mutated. This protects substrate products from
    projection-layer side effects.
    """
    output = dict(substrate_record)
    output["projection"] = {
        "name": projection.name,
        "tradition": projection.tradition,
        "archetype": projection.archetype,
        "target_jpl_id": projection.target_jpl_id,
        "tier": projection.tier,
        "citation": projection.citation,
        "related": list(projection.related),
    }
    return output
