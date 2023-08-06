from __future__ import annotations
from typing import Callable, Iterable, TypeVar

R = TypeVar("R")
Result = TypeVar("Result")


class FADLStream(Iterable[R]):
    """Typing class to add `func_adl` stream operators to iterables

    This allows type checking and predictive engines to figure out what is available to
    the user when working with sequences and writing func adl.
    """

    def First(self) -> R:
        "Returns the first element in the sequence"
        ...

    def Count(self) -> int:
        "Return the number of elements in a sequence"
        ...

    # We have to repeat what is in ObjectStream here b.c. I do not
    # know how to do covariant return types in a way that makes
    # the type engine work (like duck typing, but...)
    def Where(self, x: Callable[[R], bool]) -> FADLStream[R]:
        "Filter"
        ...

    def Select(self, x: Callable[[R], Result]) -> FADLStream[Result]:
        ...

    def SelectMany(self, func: Callable[[R], Iterable[Result]]) -> FADLStream[Result]:
        ...
