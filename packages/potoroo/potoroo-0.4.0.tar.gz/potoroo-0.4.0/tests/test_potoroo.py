"""Tests for the potoroo package."""

from __future__ import annotations

from eris import ErisResult, Ok

from potoroo import Repo, TaggedRepo


class FakeDB(Repo[int, str]):
    """Fake database."""

    def __init__(self) -> None:
        self._keys = list(range(100))
        self._db: dict[int, str] = {}

    def add(self, some_item: str, /, *, key: int = None) -> ErisResult[int]:
        """Fake add."""
        key = self._keys.pop(0)
        self._db[key] = some_item
        return Ok(key)

    def get(self, key: int) -> ErisResult[str | None]:
        """Fake get."""
        return Ok(self._db[key])

    def remove(self, key: int) -> ErisResult[str | None]:
        """Fake remove."""
        return Ok(self._db.pop(key))

    def update(self, key: int, some_item: str, /) -> ErisResult[str]:
        """Fake update."""
        self._db[key] = some_item
        return Ok(some_item)

    def all(self) -> ErisResult[list[str]]:
        """Fake all."""
        return Ok(sorted(self._db.values()))


class FakeTaggedDB(FakeDB, TaggedRepo[int, str, str]):
    """Fake tagged database."""

    def get_by_tag(self, tag: str) -> ErisResult[list[str]]:
        """Fake get_by_tag."""
        return Ok([v for v in self._db.values() if tag in v])

    def remove_by_tag(self, tag: str) -> ErisResult[list[str]]:
        """Fake remove_by_tag."""
        res: list[str] = []
        for k, v in dict(self._db).items():
            if tag in v:
                res.append(self._db.pop(k))
        return Ok(res)


def test_repo() -> None:
    """Test the Repo type."""
    db = FakeDB()
    foo_idx = db.add("foo").unwrap()
    assert db.get(foo_idx).unwrap() == "foo"
    assert db.update(foo_idx, "bar").unwrap() == "bar"
    assert db.remove(foo_idx).unwrap() == "bar"


def test_tagged_repo() -> None:
    """Test the TaggedRepo type."""
    db = FakeTaggedDB()
    foo_idx = db.add("foo").unwrap()
    db.add("bar").unwrap()
    db.add("baz").unwrap()

    assert db.get(foo_idx).unwrap() == "foo"
    assert db.get_by_tag("f").unwrap() == ["foo"]
    assert db.all().unwrap() == ["bar", "baz", "foo"]
    assert db.remove_by_tag("b").unwrap() == ["bar", "baz"]
