"""
Kelvin API Client IPython magic: %client
"""

from __future__ import annotations

import datetime
from time import time
from typing import Any, Mapping, Optional

from IPython import get_ipython
from IPython.core.magic import register_line_magic
from IPython.terminal.interactiveshell import TerminalInteractiveShell

from kelvin.sdk.client.client import MODELS, Client

try:
    from kelvin.sdk.client.io import dataframe_to_storage, storage_to_dataframe
except ModuleNotFoundError:
    dataframe_to_storage = storage_to_dataframe = None  # type: ignore


def load_ipython_extension(ipython: TerminalInteractiveShell) -> None:
    """Load Kelvin API Client IPython extension."""

    @register_line_magic
    def client(line: str) -> Optional[Client]:
        """Set up Kelvin API Client session and import all API classes."""

        session = get_ipython()
        session.push({k: v for k, v in vars(datetime).items() if isinstance(v, type)})
        session.push({T.__name__: T for T in MODELS.values()})
        session.push(
            {
                "dataframe_to_storage": dataframe_to_storage,
                "storage_to_dataframe": storage_to_dataframe,
                "time": time,
            }
        )

        if not line:
            return None

        line = line.strip()

        kwargs: Mapping[str, Any]
        if " " in line:
            site, options = line.split(" ", 1)
            kwargs = eval(f"dict({options})")  # nosec
        else:
            site = line
            kwargs = {}

        site = site.strip("'\"")

        return Client.from_file(site=site, **kwargs)


def unload_ipython_extension(ipython: TerminalInteractiveShell) -> None:
    """Unload Kelvin API Client IPython extension."""
