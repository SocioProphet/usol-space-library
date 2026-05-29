import responses

from usolspace import sbdb


@responses.activate
def test_lookup():
    responses.add(
        responses.GET,
        "https://ssd-api.jpl.nasa.gov/sbdb.api",
        json={"object": {"designation": "(1) Ceres"}},
        status=200,
    )
    out = sbdb.lookup("Ceres")
    assert out["object"]["designation"] == "(1) Ceres"
