from pathlib import Path

SUBSTRATE_MODULES = [
    "background.py",
    "colutils.py",
    "dirbe.py",
    "firas.py",
    "fov.py",
    "horizons.py",
    "horizons_lookup.py",
    "horizons_parser.py",
    "observability.py",
    "plothelpers.py",
    "provenance.py",
    "sb_ident.py",
    "sbdb.py",
    "utils_time.py",
]


def test_substrate_modules_do_not_import_projection_layer():
    root = Path("src/usolspace")
    offenders = []
    for module in SUBSTRATE_MODULES:
        text = (root / module).read_text()
        if "usolspace.projection" in text or "usolspace.books" in text:
            offenders.append(module)
    assert offenders == []
