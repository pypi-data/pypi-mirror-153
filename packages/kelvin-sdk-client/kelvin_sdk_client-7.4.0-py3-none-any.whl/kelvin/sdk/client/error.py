"""
Errors.
"""

from __future__ import annotations

import json
from textwrap import indent
from typing import TYPE_CHECKING, List

from requests import Response

if TYPE_CHECKING:
    from .model.responses import ErrorMessage  # noqa: F401


class ClientError(Exception):
    """General exception"""


class LoginError(ClientError):
    """Login exception"""


class APIError(ClientError):
    """API Error."""

    def __init__(self, response: Response) -> None:
        """Initialise API error."""

        from .model.responses import ErrorMessage

        self.response = response
        self.errors: List[ErrorMessage] = []

        for error in response.json().get("errors", []):
            message = error.get("message", [])
            if not isinstance(message, list):
                message = [message]
            self.errors += [
                ErrorMessage(client=None, **{**error, "message": [str(x) for x in message]})
            ]

        super().__init__()

    def __str__(self) -> str:

        return json.dumps([error.dict() for error in self.errors], indent=2)

    def __repr__(self) -> str:

        return f"{type(self).__name__}(errors={self.errors!r})"


class ResponseError(ClientError):
    """Response error."""

    def __init__(self, message: str, response: Response) -> None:
        """Initialise error."""

        self.message = message
        self.response = response

    def __str__(self) -> str:

        content_type = self.response.headers.get("Content-Type", "unknown").split(";", 1)[0]

        return f"{self.message} ({content_type}):\n{indent(self.response.text, '  ')}"

    def __repr__(self) -> str:

        return f"{type(self).__name__}(message={self.message!r}, response={self.response!r})"
