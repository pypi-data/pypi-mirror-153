"""
Utilities.
"""
from __future__ import annotations

import contextlib
import os
import re
from functools import wraps
from io import IOBase
from itertools import islice, zip_longest
from mimetypes import guess_type
from operator import itemgetter
from pathlib import Path
from typing import (
    Any,
    Callable,
    Dict,
    Generic,
    Iterable,
    Iterator,
    List,
    Mapping,
    MutableMapping,
    Optional,
    Sequence,
    Tuple,
    TypeVar,
    Union,
)

T = TypeVar("T")
FileTuple = Tuple[Optional[str], Union[IOBase, bytes], Optional[str]]


def snake_name(name: str) -> str:
    """Create underscore-separated name from camel-case."""

    return re.sub(r"(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])", "_", name).lower()


@contextlib.contextmanager
def chdir(path: Optional[Path]) -> Iterator[None]:
    """Changes working directory and returns to previous on exit."""

    if path is None:
        yield
    else:
        prev_cwd = Path.cwd()
        try:
            os.chdir(path if path.is_dir() else path.parent)
            yield
        finally:
            os.chdir(prev_cwd)


def relative_to_home(path: Path) -> Path:
    """Make path relative to HOME."""

    try:
        return Path("~").joinpath(path.relative_to(Path.home()))
    except ValueError:
        return path


class instance_classproperty(Generic[T]):
    """Property that works on instances and classes."""

    def __init__(self, fget: Callable[..., T]) -> None:
        """Initialise instance-classproperty."""

        self.fget = fget

    def __get__(self, owner_self: Any, owner_cls: Any) -> T:
        """Get descriptor."""

        return self.fget(owner_self if owner_self is not None else owner_cls)


class instance_classmethod(classmethod, Generic[T]):
    """Method that works on instances and classes."""

    def __init__(self, f: Callable[..., T]) -> None:
        """Initialise instance-classmethod."""

        self.f = f

    def __get__(self, owner_self: Any, owner_cls: Any) -> Callable[..., T]:  # type: ignore
        """Get descriptor."""

        x = owner_self if owner_self is not None else owner_cls

        @wraps(self.f)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            return self.f(x, *args, **kwargs)

        return wrapper


def update(data: MutableMapping[str, Any], *more: Mapping[str, Any]) -> MutableMapping[str, Any]:
    """Merge mappings into data."""

    if data is None:
        data = {}

    for x in more:
        for k, v in x.items():
            if isinstance(v, Mapping):
                update(data.setdefault(k, {}), v)
            else:
                data[k] = v

    return data


def merge(*args: Mapping[str, Any], **kwargs: Any) -> Dict[str, Any]:
    """Merge dictionaries."""

    result: Dict[str, Any] = {}

    if kwargs:
        args += (kwargs,)

    for arg in args:
        if arg is None:
            continue
        for k, v in arg.items():
            result[k] = merge(result.get(k) or {}, v) if isinstance(v, Mapping) else v

    return result


def _make_key(k: str, q: str, sep: str = ".") -> str:
    """Make flattened key."""

    if not q:
        return k

    if not q.startswith("["):
        k += sep

    return f"{k}{q}"


def flatten(x: Any, sep: str = ".", sequence: bool = True) -> List[Tuple[str, Any]]:
    """Flatten nested mappings and sequences."""

    # basic conversions
    if isinstance(x, Mapping):
        x = x.items()
    elif sequence and isinstance(x, Sequence) and not isinstance(x, str):
        x = ((f"[{i}]", v) for i, v in enumerate(x))
    else:
        return [("", x)]

    return [(_make_key(k, q, sep), w) for k, v in x for q, w in flatten(v, sep, sequence)]


def inflate(x: Iterable[Tuple[str, Any]], separator: str = ".") -> Dict[str, Any]:
    """Re-inflate flattened keys into nested object."""

    result: Dict[str, Any] = {}
    inputs: List[Tuple[Sequence[Union[int, str]], Any]] = []

    delims = re.compile("|".join(re.escape(x) for x in [separator, "[", "]"]))

    for key_, value_ in x:
        split_key: List[Union[int, str]] = [
            int(k) if k.isnumeric() else k for k in delims.split(key_) if k and not delims.match(k)
        ]
        inputs += [(split_key, value_)]

    root: Union[Dict[str, Any], List[Any]]
    fill: Optional[Union[Dict[str, Any], List[Any]]]

    for key, value in sorted(inputs, key=itemgetter(0)):
        root = result
        for k, l in zip_longest(key, key[1:]):
            fill = {} if isinstance(l, str) else [] if isinstance(l, int) else None
            if isinstance(k, str):
                if not isinstance(root, Dict):
                    raise ValueError("Invalid structure")
                if k not in root:
                    root[k] = fill
            else:
                if not isinstance(root, List):
                    raise ValueError("Invalid structure")
                root += [fill] * (k + 1 - len(root))

            if l is None:
                root[k] = value
            else:
                root = root[k]

    return result


def chunks(x: Sequence[T], n: int) -> Iterator[Sequence[T]]:
    """Yield successive n-sized chunks from l."""

    for i in range(0, len(x), n):
        yield x[i : (i + n)]


def map_chunks(
    chunk_size: int, f: Callable[..., Any], x: Iterable[T], **kwargs: Any
) -> Iterator[Any]:
    """Map function to chunks or iterable."""

    while True:
        result = f(islice(x, chunk_size), **kwargs)
        if result is None:
            break
        yield result


def deep_itemgetter(path: str) -> Callable[[str], Any]:
    """Deep itemgetter, halting on first ``None``"""

    if "." not in path:
        return itemgetter(path)

    def getter(x: Any) -> Any:
        if x is None:
            return None
        for key in path.split("."):
            x = x[key]
            if x is None:
                break
        return x

    return getter


def file_tuple(x: Union[str, IOBase, bytes, Tuple]) -> FileTuple:
    """Create file tuple for multipart request."""

    if isinstance(x, tuple):
        name, data, *tail = x
        if not tail:
            mime_type = None
        elif len(tail) == 1:
            mime_type = tail[0]
        else:
            raise ValueError("Too many values")
    else:
        if isinstance(x, str):
            name = x
            data = open(x, "rb")
        elif isinstance(x, IOBase):
            name = getattr(x, "name", None)
            data = x
        else:
            name = None
            data = x

        mime_type = None

    if mime_type is None and name is not None:
        mime_type = guess_type(name)

    return (name, data, mime_type)
