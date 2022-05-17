"""Define an object to manage bookmark-based API requests."""
from __future__ import annotations

from collections.abc import Awaitable
from typing import Any, Callable


class BookmarkManager:
    """Define the API manager object."""

    def __init__(self, async_request: Callable[..., Awaitable]) -> None:
        """Initialize."""
        self._async_request = async_request

    async def async_all(self) -> dict[str, Any]:
        """Return all bookmarks."""
        return await self._async_request("get", "/api/bookmarks/")
