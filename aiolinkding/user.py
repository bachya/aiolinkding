"""Define an object to manage user-based API requests."""
from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import Any, cast


class UserManager:  # pylint: disable=too-few-public-methods
    """Define the API manager object."""

    def __init__(self, async_request: Callable[..., Awaitable]) -> None:
        """Initialize.

        Args:
            async_request: The request method from the Client object.
        """
        self._async_request = async_request

    async def async_get_profile(self) -> dict[str, Any]:
        """Return user profile info.

        Returns:
            An API response payload.
        """
        data = await self._async_request("get", "/api/user/profile/")
        return cast(dict[str, Any], data)
