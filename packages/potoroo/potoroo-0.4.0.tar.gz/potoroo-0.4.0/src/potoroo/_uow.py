"""Contains the `UnitOfWork` abstract type."""

from __future__ import annotations

import abc
from types import TracebackType
from typing import Generic, Type, TypeVar

from ._repo import BasicRepo


R = TypeVar("R", bound=BasicRepo)
U = TypeVar("U", bound="UnitOfWork")


class UnitOfWork(Generic[R], abc.ABC):
    """Implements the 'Unit-of-Work' persistance pattern."""

    @property
    @abc.abstractmethod
    def repo(self) -> R:
        """The Repo type this UoW is associated with."""

    @abc.abstractmethod
    def __enter__(self: U) -> U:
        """Called before entering the UoW context manager."""

    @abc.abstractmethod
    def __exit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """Called before leaving the UoW context manager."""

    @abc.abstractmethod
    def commit(self) -> None:
        """Commits our changes to `self.repo`."""

    @abc.abstractmethod
    def rollback(self) -> None:
        """Reverts our changes to `self.repo`."""
