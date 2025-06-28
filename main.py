# -*- coding: utf-8 -*-
from functools import reduce
from typing import (
    Any,
    Callable,
    Dict,
    Generator,
    Generic,
    Iterable,
    Iterator,
    List,
    Optional,
    Tuple,
    TypeVar,
    Union,
)


I = TypeVar("I")  # input type
O = TypeVar("O")  # output type after transformations


class LazyCollection(Generic[I]):
    """A collection that supports lazy evaluation of transformations."""

    def __init__(self, iterable: Union[Iterable[I], Generator[I, None, None]]) -> None:
        """Initialize with an iterable or generator."""
        self._source = iterable

    def __iter__(self) -> Iterator[I]:
        """Iterate over the elements."""
        return iter(self._source)

    def filter(self, predicate: Callable[[I], bool]) -> "LazyCollection[I]":
        """Filter elements using a predicate function."""
        return LazyCollection(item for item in self if predicate(item))

    def map(self, transform: Callable[[I], O]) -> "LazyCollection[O]":
        """Apply a transformation to each element."""
        return LazyCollection(transform(item) for item in self)

    def flat_map(self, transform: Callable[[I], Iterable[O]]) -> "LazyCollection[O]":
        """Apply a transformation that returns iterables and flatten the results."""
        return LazyCollection(subitem for item in self for subitem in transform(item))

    def take(self, n: int) -> "LazyCollection[I]":
        """Take at most n elements from the collection."""

        def take_generator() -> Generator[I, None, None]:
            for i, item in enumerate(self):
                if i >= n:
                    break
                yield item

        return LazyCollection(take_generator())

    def skip(self, n: int) -> "LazyCollection[I]":
        """Skip the first n elements of the collection."""

        def skip_generator() -> Generator[I, None, None]:
            for i, item in enumerate(self):
                if i >= n:
                    yield item

        return LazyCollection(skip_generator())

    def reduce(self, reducer: Callable[[O, I], O], initial: O) -> O:
        """Reduce the collection to a single value."""
        return reduce(reducer, self, initial)

    def chunk(self, size: int) -> "LazyCollection[List[I]]":
        """Split the collection into chunks of the given size."""

        def chunk_generator() -> Generator[List[I], None, None]:
            chunk: List[I] = []
            for item in self:
                chunk.append(item)
                if len(chunk) == size:
                    yield chunk
                    chunk = []
            if chunk:  # yield the last partial chunk
                yield chunk

        return LazyCollection(chunk_generator())

    def paginate(self, page: int, per_page: int) -> "LazyCollection[I]":
        """Get a specific page of results."""
        return self.skip((page - 1) * per_page).take(per_page)

    def collect(self) -> List[I]:
        """Evaluate and collect all results into a list."""
        return list(self)

    def first(self) -> Optional[I]:
        """Get the first element or None if empty."""
        for item in self:
            return item
        return None

    def count(self) -> int:
        """Count the number of elements in the collection."""
        return sum(1 for _ in self)

    def any(self, predicate: Optional[Callable[[I], bool]] = None) -> bool:
        """Check if any element satisfies the predicate (or if any exists)."""
        if predicate is None:
            predicate = lambda x: True
        return any(predicate(item) for item in self)

    def all(self, predicate: Callable[[I], bool]) -> bool:
        """Check if all elements satisfy the predicate."""
        return all(predicate(item) for item in self)

    def group_by(self, key_func: Callable[[I], O]) -> Dict[O, List[I]]:
        """Group elements by a key function."""
        result: Dict[O, List[I]] = {}
        for item in self:
            key = key_func(item)
            if key not in result:
                result[key] = []
            result[key].append(item)
        return result

    def distinct(self) -> "LazyCollection[I]":
        """Return distinct elements (requires hashable elements)."""
        seen = set()
        return LazyCollection(item for item in self if not (item in seen or seen.add(item)))

    def sort(self, key: Optional[Callable[[I], Any]] = None, reverse: bool = False) -> "LazyCollection[I]":
        """Sort the collection (non-lazy operation)."""
        return LazyCollection(sorted(self.collect(), key=key, reverse=reverse))

    def zip(self, other: Iterable[O]) -> "LazyCollection[Tuple[I, O]]":
        """Zip with another iterable."""
        return LazyCollection(zip(self, other))

    def enumerate(self) -> "LazyCollection[Tuple[int, I]]":
        """Add indices to elements."""
        return LazyCollection(enumerate(self))

    def __repr__(self) -> str:
        """String representation of the collection."""
        return f"LazyCollection(...)"

    @classmethod
    def range(cls, start: int, stop: Optional[int] = None, step: int = 1) -> "LazyCollection[int]":
        """Create a LazyCollection from a range."""
        if stop is None:
            return cls(range(0, start, step))
        return cls(range(start, stop, step))
