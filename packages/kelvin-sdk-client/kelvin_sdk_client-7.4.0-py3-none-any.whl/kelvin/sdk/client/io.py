"""IO functions."""

from __future__ import annotations

from datetime import tzinfo
from typing import Any, Dict, Iterable, Iterator, List, Mapping, Optional, Union

import numpy
from pandas import DataFrame, Series, concat, json_normalize, to_datetime
from typing_extensions import Literal
from tzlocal import get_localzone

from .model.requests import StorageCreate
from .utils import chunks, inflate, map_chunks

STORAGE_FIELDS = {*StorageCreate.__fields__} - {"id", "payload"}
INDEX = [
    "asset_name",
    # "source",
    # "target",
    "timestamp",
    "name",
]
DEFAULT_TZ = str(get_localzone())


def _convert_storage(
    x: Iterable[Mapping[str, Any]],
    tz: Union[tzinfo, str],
    insertion_timestamp: bool = False,
    expand_payload: Optional[Literal["column", "row"]] = "column",
) -> Optional[DataFrame]:
    """Convert storage into datframe."""

    data = DataFrame.from_records(x)
    if data.empty:
        return None

    data["timestamp"] = to_datetime(data.timestamp, utc=True).dt.tz_convert(tz)

    if "_insertion_timestamp" in data:
        if insertion_timestamp:
            data["_insertion_timestamp"] = to_datetime(
                data._insertion_timestamp, utc=True
            ).dt.tz_convert(tz)
        else:
            data.drop(columns=["_insertion_timestamp"], inplace=True)

    data.set_index(INDEX, inplace=True)

    if expand_payload == "column":
        payload = json_normalize(data.pop("payload"))
        payload.index = data.index
        return concat([payload, data], axis=1)

    if expand_payload == "row":
        payload = concat({k: json_normalize(v).T for k, v in data.pop("payload").items()})
        payload.columns = ["value"]
        payload.index.names = [*data.index.names, "field"]
        return payload.join(data)

    return data


def storage_to_dataframe(
    x: Iterable[Mapping[str, Any]],
    chunk_size: Optional[int] = None,
    tz: Union[tzinfo, str] = DEFAULT_TZ,
    insertion_timestamp: bool = False,
    expand_payload: Optional[Literal["column", "row"]] = "column",
    compress: bool = False,
) -> Union[DataFrame, Iterator[DataFrame]]:
    """Convert storage into datframe, optionally in chunks."""

    kwargs: Mapping[str, Any] = {
        "tz": tz,
        "insertion_timestamp": insertion_timestamp,
        "expand_payload": expand_payload,
    }

    if chunk_size is None:
        return _convert_storage(x, **kwargs)

    result = map_chunks(chunk_size, _convert_storage, x, **kwargs)

    return compress_time(result, "timestamp") if compress else result


def _convert_dataframe(x: DataFrame) -> List[Dict[str, Any]]:
    """Convert dataframe into storage."""

    x = x.reset_index()

    missing = STORAGE_FIELDS - {*x}
    if missing:
        raise ValueError(f"Missing fields: {', '.join(sorted(missing))}")

    columns = {*x} - STORAGE_FIELDS

    if not columns:
        raise ValueError("No columns found")

    if "payload" in columns:
        extra = columns - {"payload"}
        if extra:
            raise ValueError("Unexpected columns: {', '.join(sorted(extra))}")

    elif "field" in columns and "value" in columns:
        extra = columns - {"field", "value"}
        if extra:
            raise ValueError("Unexpected columns: {', '.join(sorted(extra))}")
        x = (
            x.groupby([*STORAGE_FIELDS])[["field", "value"]]
            .apply(lambda x: inflate(x.itertuples(index=False)))
            .reset_index(name="payload")
        )

    else:
        x["payload"] = [inflate(v.items()) for v in x[columns].to_dict(orient="records")]
        x = x.drop(columns=columns)

    x["timestamp"] = x.timestamp.astype(int)

    return x.to_dict(orient="records")


def dataframe_to_storage(
    x: DataFrame, chunk_size: Optional[int] = None
) -> Union[List[Dict[str, Any]], Iterator[List[Dict[str, Any]]]]:
    """Convert dataframe into storage, optionally in chunks."""

    if chunk_size is None:
        return _convert_dataframe(x)

    return (_convert_dataframe(chunk) for chunk in chunks(x, chunk_size))


def compress_time(x: Union[DataFrame, Series], time: str = "time") -> DataFrame:
    """Compress dataframe/series along time axis."""

    if isinstance(x, Series):
        x = x.to_frame(name="value")

    x = x.sort_index()
    y = x.fillna(-numpy.Inf)
    x = x.reset_index(time)

    aggregations = {
        time: ["first", "last"],
        **{name: ["first", "count"] for name in x.columns if name != time},
    }

    names = [name for name in x.index.names if name is not None]
    group_id = (y != y.shift()).any(axis=1).cumsum().values

    result = x.groupby(names + [group_id]).agg(aggregations)
    if names:
        result.index = result.index.droplevel(-1)  # drop group ID
    result = result.set_index([(time, "first"), (time, "last")], append=True).rename(
        columns={"first": "value"}
    )
    result.index = result.index.rename(["start", "end"], level=(-2, -1))

    return result
