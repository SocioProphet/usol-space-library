from pathlib import Path

import pytest

from usolspace.books import load_book, load_book_registry, resolve_book_projection


def test_curated_books_load_and_resolve_projection():
    book = load_book("data/books/book-viii.yaml")
    assert book.volume == "VIII"
    assert book.target_jpl_id == "10"
    projection = resolve_book_projection(book)
    assert projection.name == "rev12-sun-bride"
    assert projection.target_jpl_id == book.target_jpl_id


def test_book_registry_has_vii_viii_xi():
    registry = load_book_registry("data/books")
    assert set(registry) == {"VII", "VIII", "XI"}


def test_book_registry_detects_duplicate_volumes(tmp_path: Path):
    content = Path("data/books/book-viii.yaml").read_text()
    (tmp_path / "a.yaml").write_text(content)
    (tmp_path / "b.yaml").write_text(content)
    with pytest.raises(ValueError, match="duplicate book volume"):
        load_book_registry(tmp_path)


def test_book_rejects_target_projection_mismatch(tmp_path: Path):
    book_path = tmp_path / "bad-book.yaml"
    book_path.write_text(
        "code: Bad\n"
        "title: Bad\n"
        "volume: BAD\n"
        "target_jpl_id: '999'\n"
        "projection_path: data/projections/rev12-sun-bride.yaml\n"
    )
    book = load_book(book_path)
    with pytest.raises(ValueError, match="does not match"):
        resolve_book_projection(book)
