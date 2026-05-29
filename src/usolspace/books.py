"""Curated Book registry helpers for the projection layer."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from usolspace.projection import CulturalProjection, load_projection, CURATED_BOOK_TIERS


@dataclass(frozen=True)
class CuratedBook:
    code: str
    title: str
    volume: str
    target_jpl_id: str
    projection_path: str
    default_center: str = "500@399"
    default_start: str = "2025-09-01"
    default_stop: str = "2025-09-02"
    default_step: str = "1 d"
    default_quantities: str = "1,9,20"


def _require_string(data: dict[str, Any], key: str, source: Path) -> str:
    value = data.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{source}: book field `{key}` must be a non-empty string")
    return value.strip()


def book_from_dict(data: dict[str, Any], source: str | Path = "<memory>") -> CuratedBook:
    path = Path(source) if not isinstance(source, Path) else source
    return CuratedBook(
        code=_require_string(data, "code", path),
        title=_require_string(data, "title", path),
        volume=_require_string(data, "volume", path),
        target_jpl_id=_require_string(data, "target_jpl_id", path),
        projection_path=_require_string(data, "projection_path", path),
        default_center=str(data.get("default_center", "500@399")),
        default_start=str(data.get("default_start", "2025-09-01")),
        default_stop=str(data.get("default_stop", "2025-09-02")),
        default_step=str(data.get("default_step", "1 d")),
        default_quantities=str(data.get("default_quantities", "1,9,20")),
    )


def load_book(path: str | Path) -> CuratedBook:
    book_path = Path(path)
    raw = yaml.safe_load(book_path.read_text())
    if not isinstance(raw, dict):
        raise ValueError(f"{book_path}: book YAML must contain a mapping")
    return book_from_dict(raw, book_path)


def load_book_registry(directory: str | Path) -> dict[str, CuratedBook]:
    registry_path = Path(directory)
    books: dict[str, CuratedBook] = {}
    for path in sorted(registry_path.glob("*.yaml")):
        book = load_book(path)
        if book.volume in books:
            raise ValueError(f"duplicate book volume: {book.volume}")
        books[book.volume] = book
    return books


def resolve_book_projection(book: CuratedBook, registry_root: str | Path = ".") -> CulturalProjection:
    projection_path = Path(registry_root) / book.projection_path
    projection = load_projection(projection_path)
    if projection.target_jpl_id != book.target_jpl_id:
        raise ValueError(
            f"book {book.volume} target {book.target_jpl_id} does not match projection target {projection.target_jpl_id}"
        )
    if projection.tier not in CURATED_BOOK_TIERS:
        raise ValueError(f"book {book.volume} cannot use non-curatable projection tier `{projection.tier}`")
    return projection
