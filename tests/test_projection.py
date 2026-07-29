from pathlib import Path

import pytest

from usolspace.projection import (
    CulturalProjection,
    attach_projection_record,
    load_projection,
    load_projection_registry,
    projection_from_dict,
)


def test_projection_loads_from_yaml():
    projection = load_projection("data/projections/rev12-sun-bride.yaml")
    assert isinstance(projection, CulturalProjection)
    assert projection.name == "rev12-sun-bride"
    assert projection.target_jpl_id == "10"
    assert projection.tier == "placement"
    assert projection.is_curatable


def test_projection_rejects_invalid_tier():
    with pytest.raises(ValueError, match="invalid"):
        projection_from_dict(
            {
                "name": "bad",
                "tradition": "test",
                "archetype": "test",
                "target_jpl_id": "10",
                "tier": "unbounded",
                "citation": "test",
                "commentary_md": "test",
            }
        )


def test_projection_registry_detects_duplicate_names(tmp_path: Path):
    content = Path("data/projections/rev12-sun-bride.yaml").read_text()
    (tmp_path / "a.yaml").write_text(content)
    (tmp_path / "b.yaml").write_text(content)
    with pytest.raises(ValueError, match="duplicate projection name"):
        load_projection_registry(tmp_path)


def test_attach_projection_record_does_not_mutate_substrate_record():
    substrate = {"target": "10", "value": 1}
    projection = load_projection("data/projections/rev12-sun-bride.yaml")
    attached = attach_projection_record(substrate, projection)
    assert substrate == {"target": "10", "value": 1}
    assert attached["projection"]["name"] == "rev12-sun-bride"
