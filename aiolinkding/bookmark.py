"""Define an object to manage bookmark-based API requests."""
from __future__ import annotations

from collections.abc import Awaitable
from typing import Any, Callable, Dict, cast

DEFAULT_LIMIT = 100


class BookmarkManager:
    """Define the API manager object."""

    def __init__(self, async_request: Callable[..., Awaitable]) -> None:
        """Initialize."""
        self._async_request = async_request

    async def async_all(
        self,
        *,
        query: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> dict[str, Any]:
        """Return all bookmarks."""
        params = {}
        for kwarg, param_name in (
            (query, "q"),
            (limit, "limit"),
            (offset, "offset"),
        ):
            if kwarg:
                params[param_name] = kwarg
        data = await self._async_request("get", "/api/bookmarks/")
        return cast(Dict[str, Any], data)
