"""Tests for the nearby-star catalogue (the quadrant 'cube of space' canonical source)."""

import math

from usolspace.nearby_stars import CUBE_LY, nearby_stars, quadrant_payload


def test_sol_is_first_and_at_the_origin():
    sys = nearby_stars()
    assert sys[0].name == "Sol"
    assert sys[0].position == [0.0, 0.0, 0.0]


def test_ids_are_unique_nonempty_slugs():
    ids = [s.id for s in nearby_stars()]
    assert len(ids) == len(set(ids))
    assert all(i and all(c.islower() or c.isdigit() or c == "-" for c in i) for i in ids)


def test_positions_reconstruct_the_declared_distance():
    # |xyz| must equal distLy (the Cartesian conversion is consistent).
    for s in nearby_stars():
        assert math.isclose(math.hypot(*s.position), s.distLy, abs_tol=0.01)


def test_all_systems_lie_within_the_mapped_cube():
    for s in nearby_stars():
        x, y, z = s.position
        assert max(abs(x), abs(y), abs(z)) <= CUBE_LY, f"{s.name} outside the cube"


def test_payload_shape_matches_the_client_contract():
    p = quadrant_payload()
    assert p["source"] == "usol.nearby_stars"
    assert p["cube_ly"] == CUBE_LY
    assert p["systems"] and isinstance(p["systems"], list)
    s0 = p["systems"][0]
    for k in ("id", "name", "position", "color", "distLy", "spectral"):
        assert k in s0, f"missing {k}"
    assert len(s0["position"]) == 3 and len(s0["color"]) == 3
