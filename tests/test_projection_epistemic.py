"""Projection epistemic-typing: a lens is governed by the canonical estate lattice, never ground truth.

These bind usol's projection tiers to the SAME epistemic lattice the rest of the estate uses, and
enforce the mismatch guard: an interpretive projection can never certify itself as empirical fact.
Teeth both ways — the cap holds for every tier, and a real curated lens loads below it.
"""

from pathlib import Path

import pytest

from usolspace.projection import (
    ALLOWED_TIERS,
    EPISTEMIC_LATTICE,
    PROJECTION_EPISTEMIC_CAP,
    TIER_TO_EPISTEMIC,
    load_projection_registry,
    projection_from_dict,
    attach_projection_record,
)

CAP_RANK = EPISTEMIC_LATTICE.index(PROJECTION_EPISTEMIC_CAP)


def _proj(**over):
    base = dict(name="t", tradition="tr", archetype="A", target_jpl_id="301",
               tier="placement", citation="c", commentary_md="m")
    base.update(over)
    return projection_from_dict(base)


def test_tier_map_covers_every_allowed_tier():
    # completeness: the mapping must not silently under-cover a tier (self-validating).
    assert set(TIER_TO_EPISTEMIC) == ALLOWED_TIERS


def test_every_tier_is_capped_below_empirical():
    # the mismatch guard: no projection tier may reach `empirical` or above.
    for tier, level in TIER_TO_EPISTEMIC.items():
        assert EPISTEMIC_LATTICE.index(level) <= CAP_RANK, f"{tier} -> {level} exceeds the projection cap"
    assert EPISTEMIC_LATTICE.index("empirical") > CAP_RANK  # empirical is genuinely above the cap


def test_tier_maps_to_expected_lattice_level():
    assert _proj(tier="fails").epistemic_level == "rejected"
    assert _proj(tier="synthesis").epistemic_level == "speculative"
    assert _proj(tier="placement").epistemic_level == "synthetic"
    # an EXACT placement certifies the placement, not the interpretation -> still capped at synthetic.
    assert _proj(tier="exact").epistemic_level == "synthetic"
    assert _proj(tier="exact").epistemic_rank <= CAP_RANK


def test_a_projection_is_never_substrate():
    assert _proj().is_substrate is False


def test_candidate_ontology_flag_reads_from_metadata():
    assert _proj().candidate_ontology is False
    lens = _proj(metadata={"candidate_ontology": True})
    assert lens.candidate_ontology is True
    # ...but flagging a graduation candidate does NOT raise its epistemic level in place.
    assert lens.epistemic_rank <= CAP_RANK


def test_curated_rev12_projections_load_below_the_cap():
    reg = load_projection_registry("data/projections")
    assert reg, "expected curated rev12 projections to exist"
    for name, proj in reg.items():
        assert proj.epistemic_rank <= CAP_RANK, f"{name} claims {proj.epistemic_level} > cap — a lens as fact"
        assert proj.is_substrate is False


def test_attached_record_carries_typing_and_never_mutates_or_forges_substrate():
    substrate = {"target": "301", "value": 42}
    out = attach_projection_record(substrate, _proj(tier="exact"))
    assert "projection" not in substrate  # input never mutated
    p = out["projection"]
    assert p["epistemic_level"] == "synthetic"
    assert p["is_substrate"] is False
    assert p["candidate_ontology"] is False
    # the substrate values are untouched by the overlay.
    assert out["value"] == 42 and out["target"] == "301"
