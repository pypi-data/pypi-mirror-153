"""The `*Repo` abstract types which implement the "Repository" pattern."""

from __future__ import annotations

import abc
from typing import Generic, TypeVar

from eris import ErisResult, Err, Ok


K = TypeVar("K")
V = TypeVar("V")
T = TypeVar("T")


class BasicRepo(Generic[K, V], abc.ABC):
    """The simplest possible Repository type."""

    @abc.abstractmethod
    def add(self, item: V, /, *, key: K = None) -> ErisResult[K]:
        """Add a new `item` to the repo and associsate it with `key`."""

    @abc.abstractmethod
    def get(self, key: K) -> ErisResult[V | None]:
        """Retrieve an item from the repo by key."""


class Repo(BasicRepo[K, V], Generic[K, V], abc.ABC):
    """A full-featured Repository

    Adds the ability to update, delete, and list all items ontop of the
    BasicRepo type.
    """

    @abc.abstractmethod
    def remove(self, key: K) -> ErisResult[V | None]:
        """Remove an item from the repo by key."""

    def update(self, key: K, item: V, /) -> ErisResult[V]:
        """Update an item by key."""
        old_item_result = self.remove(key)
        if isinstance(old_item_result, Err):
            err: Err = Err(
                "An error occurred while removing the old item."
            ).chain(old_item_result)
            return err

        old_item = old_item_result.ok()
        if old_item is None:
            return Err(f"Old item with this ID does not exist. | id={key}")

        self.add(item, key=key).unwrap()

        return Ok(old_item)

    @abc.abstractmethod
    def all(self) -> ErisResult[list[V]]:
        """Retrieve all items stored in this repo."""


class TaggedRepo(Repo[K, V], Generic[K, V, T], abc.ABC):
    """A Repository that is aware of some kind of "tags".

    Adds the ability to retrieve / delete a group of objects based off of some
    arbitrary "tag" type.

    NOTE: In general, K can be expected to be a primitive type, whereas T is
      often a custom user-defined type.
    """

    @abc.abstractmethod
    def get_by_tag(self, tag: T) -> ErisResult[list[V]]:
        """Retrieve a group of items that meet the given tag's criteria."""

    @abc.abstractmethod
    def remove_by_tag(self, tag: T) -> ErisResult[list[V]]:
        """Remove a group of items that meet the given tag's criteria."""
