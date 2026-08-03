"""Tests for the USOL HTTP service routing (pure `route`, no socket)."""

from usolspace.service import route


def test_quadrant_route_returns_the_payload():
    status, body = route("/space/quadrant")
    assert status == 200
    assert body["source"] == "usol.nearby_stars"
    assert body["systems"] and body["systems"][0]["name"] == "Sol"


def test_quadrant_route_ignores_query_and_trailing_slash():
    assert route("/space/quadrant/?x=1")[0] == 200
    assert route("/quadrant")[0] == 200


def test_healthz_ok():
    status, body = route("/healthz")
    assert status == 200 and body["ok"] is True and "/space/quadrant" in body["routes"]


def test_unknown_route_is_404_not_a_silent_200():
    status, body = route("/nope")
    assert status == 404 and "error" in body
