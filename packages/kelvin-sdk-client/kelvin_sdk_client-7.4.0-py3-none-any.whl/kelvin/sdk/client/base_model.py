"""
Base data-model.
"""

from __future__ import annotations

from datetime import date
from functools import reduce
from typing import (
    TYPE_CHECKING,
    Any,
    Iterable,
    Iterator,
    Mapping,
    Optional,
    Sequence,
    Tuple,
    TypeVar,
)

import pydantic
from pydantic.main import ModelMetaclass

if TYPE_CHECKING:
    from IPython.lib.pretty import PrettyPrinter


class BaseModelMeta(ModelMetaclass):
    """BaseModel metaclass."""


class BaseModel(pydantic.BaseModel, Mapping[str, Any], metaclass=BaseModelMeta):
    """Base data-model with mapping methods."""

    __slots__ = ("_owner", "_name")

    class Config(pydantic.BaseConfig):
        """Configuration defaults."""

        validate_all = True
        validate_assignment = True

    def __init__(
        self, _owner: Optional["BaseModel"] = None, _name: Optional[str] = None, **kwargs: Any
    ) -> None:
        """Initialise model."""

        super().__init__(**kwargs)

        self._set_owner(_owner, _name)

        # take ownership of model fields
        for name, value in self.items():
            if isinstance(value, BaseModel):
                value._set_owner(self, name)
            elif isinstance(value, list):
                for x in value:
                    if not isinstance(x, BaseModel):
                        break
                    x._set_owner(self, name)

    def _set_owner(self, owner: Optional["BaseModel"], name: Optional[str] = None) -> None:
        """Set owner of object."""

        object.__setattr__(self, "_owner", owner)
        object.__setattr__(self, "_name", name)

    def __setattr__(self, name: str, value: Any) -> Any:
        """Set attribute."""

        super().__setattr__(name, value)

        result = getattr(self, name)

        if isinstance(result, BaseModel):
            result._set_owner(self, name)
        elif isinstance(result, list):
            for x in result:
                if not isinstance(x, BaseModel):
                    break
                x._set_owner(self, name)

        return result

    # Mapping methods
    def __getitem__(self, name: str) -> Any:
        """Get item."""

        if "." in name:
            try:
                return reduce(lambda x, y: x[y], name.split("."), self)
            except KeyError:
                raise KeyError(name) from None

        try:
            return getattr(self, name)
        except AttributeError:
            raise KeyError(name) from None

    def __setitem__(self, name: str, value: Any) -> Any:
        """Set item."""

        if "." not in name:
            return setattr(self, name, value)

        head, tail = name.rsplit(".", 1)
        head = self[head]

        return setattr(head, tail, value)

    def __len__(self) -> int:
        """Number of keys."""

        return len(self.__dict__)

    def __iter__(self) -> Iterator[str]:  # type: ignore
        """Key iterator."""

        return iter(self.__dict__)

    def _items_pretty_(self) -> Iterable[Tuple[str, Any]]:
        """Pretty items list."""

        return self.items()

    def _repr_pretty_(self, p: PrettyPrinter, cycle: bool) -> None:
        """Pretty representation."""

        name = type(self).__name__
        if cycle:
            p.text(f"{name}(...)")
        else:
            with p.group(4, f"{name}(", ")"):
                for i, (k, v) in enumerate(self._items_pretty_()):
                    if i:
                        p.text(",")
                        p.breakable()
                    else:
                        p.breakable("")
                    p.text(f"{k}=")
                    p.pretty(v.isoformat() if isinstance(v, date) else v)


P = TypeVar("P")


class BaseModelRoot(pydantic.BaseModel, Sequence[P], metaclass=BaseModelMeta):
    """Base data-model with sequence methods."""

    class Config(pydantic.BaseConfig):
        """Configuration defaults."""

        validate_all = True
        validate_assignment = True

    def __init__(self, **kwargs: Any) -> None:
        """Initialise model."""

        super().__init__(**kwargs)

    # Sequence methods
    def __getitem__(self, item: int) -> P:  # type: ignore
        """Get item."""

        return self.__root__[item]

    def __len__(self) -> int:
        """Number of items."""

        return len(self.__root__)

    def __iter__(self) -> Iterator[P]:  # type: ignore
        """Item iterator."""

        return iter(self.__root__)

    def _repr_pretty_(self, p: PrettyPrinter, cycle: bool) -> None:
        """Pretty representation."""

        name = type(self).__name__
        if cycle:
            p.text(f"{name}[...]")
        else:
            with p.group(4, f"{name}[", "]"):
                for i, v in enumerate(self.__root__):
                    if i:
                        p.text(",")
                        p.breakable()
                    else:
                        p.breakable("")
                    p.pretty(f"{v}" if isinstance(v, date) else v)
