"""
Deep-list for querying structures.
"""

from __future__ import annotations

import re
from fnmatch import fnmatchcase
from functools import reduce
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    Iterable,
    List,
    Mapping,
    Optional,
    Pattern,
    Sequence,
    Tuple,
    TypeVar,
)

from .utils import deep_itemgetter, flatten

if TYPE_CHECKING:
    from IPython.lib.pretty import PrettyPrinter

INDEX_RE = re.compile(r"^(?P<head>\w+)?\[(?P<index>[^\[\]]+)\]$")
T = TypeVar("T")


def make_matcher(value: Any) -> Callable[[Any], bool]:
    """Make matcher function."""

    if value is None:
        return lambda x: True

    if callable(value):
        return value

    if isinstance(value, Pattern):
        return lambda x: x is not None and value.match(x)

    if isinstance(value, str):
        if "*" in value or "?" in value:
            return lambda x: x is not None and fnmatchcase(x, value)
        return lambda x: x == value

    if isinstance(value, Sequence):
        list_matchers: Sequence[Callable[[Any], Any]] = [make_matcher(v) for v in value]
        return lambda x: any(matcher(x) for matcher in list_matchers)

    if isinstance(value, Mapping):
        dict_matchers = [
            (k if callable(k) else deep_itemgetter(k), make_matcher(v)) for k, v in value.items()
        ]
        return lambda x: all(matcher(getter(x)) for getter, matcher in dict_matchers)

    return lambda x: x == value


class deeplist(list):
    """List with support for getting attributes of members."""

    def __getitem__(self, item: Any) -> Any:
        """Extended item getter."""

        if isinstance(item, int):
            return super().__getitem__(item)

        if isinstance(item, slice):
            return type(self)(super().__getitem__(item))

        if isinstance(item, str):
            # handle index queries (name[index])
            match = INDEX_RE.match(item)
            if match:
                head, index = match.groups()
                result = self[head] if head is not None else self

                if index == ":":
                    return result[:]

                if ":" in index:
                    return result[slice(*(int(x) if x else None for x in index.split(":")))]

                if index[index[0] in "+-" :].isnumeric():
                    return [int(index)]

                return result[index]

            # descend into structure
            if "." in item:
                head, tail = item.split(".", 1)
                try:
                    return reduce(lambda x, y: x[y], item.split("."), self)
                except KeyError:
                    raise KeyError(item)

            key = item

            # handle wildcard
            if "*" in item or "?" in item:
                types = {type(value) for value in self if value is not None}

                # nothing to do
                if not types:
                    return type(self)()

                if types == {str}:
                    item = [value is not None and fnmatchcase(value, item) for value in self]
                elif all(issubclass(x, Mapping) for x in types):

                    def item(x: Optional[Mapping[str, Any]]) -> Optional[Dict[str, Any]]:
                        if x is None:
                            return None
                        return {k: v for k, v in x.items() if fnmatchcase(k, key)}

                elif len(types) != 1:
                    raise TypeError(
                        "Mixed types in wildcard filter:"
                        f" {', '.join(sorted(repr(x.__name__) for x in types))}"
                    )
                else:
                    raise TypeError(f"Invalid type in list-index: {types.pop().__name__!r}")
            else:
                item = lambda x: x[key] if x is not None else None

        if isinstance(item, Iterable):
            if not isinstance(item, list):
                item = [*item]

            # nothing to do
            if not item:
                return type(self)()

            # check for mixed types in index
            types = {type(x) for x in item}

            if types == {bool}:
                if len(item) != len(self):
                    raise IndexError(f"Boolean list-index length does not match list: {len(item)}")
                return type(self)(value for value, x in zip(self, item) if x)

            if types == {int}:
                return type(self)(self[x] for x in item)

            if len(types) != 1:
                raise TypeError(
                    "Mixed types in list-index:"
                    f" {', '.join(sorted(repr(x.__name__) for x in types))}"
                )
            raise TypeError(f"Invalid type in list-index: {types.pop().__name__!r}")

        if callable(item):
            return type(self)(item(value) for value in self)

        # fall-through fail
        return super().__getitem__(item)

    def __setitem__(self, item: Any, value: Any) -> None:
        """Extended item setter."""

        if not isinstance(item, str):
            super().__setitem__(item, value)
            return

        if "." in item:
            # descend
            head, tail = item.split(".", 1)
            self[head][tail] = value
        else:
            for x in self:
                if x is None:
                    continue
                x[item] = value

    def __delitem__(self, item: Any) -> None:
        """Extended item deleter."""

        if not isinstance(item, str):
            super().__delitem__(item)
            return

        if "." in item:
            # descend
            head, tail = item.split(".", 1)
            del self[head][tail]
        else:
            for x in self:
                if x is None:
                    continue
                del x[item]

    def __getattr__(self, name: str) -> Any:
        """Get attributes of members."""

        result = [getattr(x, name) if x is not None else None for x in self]

        # wrap callable result as closure for apply
        if result and all(callable(x) and not isinstance(x, list) for x in result):

            def wrapper(*args: Any, **kwargs: Any) -> deeplist:
                return type(self)(x(*args, **kwargs) for x in result)

            wrapper.__name__ = f"{name}_wrapper"
            wrapper.__doc__ = f"Wrapper for {name}."

            return wrapper

        return type(self)(result)

    def __setattr__(self, name: str, value: Any) -> None:
        """Set attributes of members."""

        self[name] = value

    def __delattr__(self, name: str) -> None:
        """Delete attributes of members."""

        del self[name]

    def __call__(self, **kwargs: Any) -> List[Any]:
        """Filter list."""

        if not kwargs:
            return self[:]

        filters = {k.replace("__", "."): v for k, v in kwargs.items()}
        matcher = make_matcher(filters)

        return self[[matcher(value) for value in self]]

    def flatten(self) -> List[Tuple[str, Any]]:
        """Flatten structure."""

        return flatten(self)

    def _repr_pretty_(self, p: PrettyPrinter, cycle: bool) -> None:
        """Pretty representation."""

        if cycle:
            name = type(self).__name__
            p.text(f"{name}(...)")
        else:
            with p.group(4, "[", "]"):
                for i, x in enumerate(self):
                    if i:
                        p.text(",")
                        p.breakable()
                    else:
                        p.breakable("")
                    p.pretty(x)

    def __eq__(self, x: Any) -> deeplist:  # type: ignore
        """Check equality."""

        if isinstance(x, Sequence) and not isinstance(x, (str, Mapping)):
            if not len(x) == len(self):
                raise ValueError("Lengths of sequences for comparison do not match")
            return type(self)(u == v for u, v in zip(x, self))
        else:
            return type(self)(x == v for v in self)

    def __ne__(self, x: Any) -> deeplist:  # type: ignore
        """Check non-equality."""

        return ~(self == x)

    def __invert__(self) -> deeplist:
        """Invert objects."""

        return type(self)(not x for x in self)

    def __and__(self, x: Sequence[Any]) -> deeplist:
        """Logical and."""

        return type(self)(u and v for u, v in zip(x, self))

    def __or__(self, x: Sequence[Any]) -> deeplist:
        """Logical or."""

        return type(self)(u or v for u, v in zip(x, self))

    def __dir__(self) -> List[str]:
        """Return list of names of the object items/attributes."""

        return [*super().__dir__(), *sorted({v for x in self for v in dir(x)})]
