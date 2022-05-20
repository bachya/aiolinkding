"""Define an object to manage tag-based API requests."""
from __future__ import annotations

from collections.abc import Awaitable
from typing import Any, Callable, Dict, cast


class TagManager:
    """Define the API manager object."""

    def __init__(self, async_request: Callable[..., Awaitable]) -> None:
        """Initialize."""
        self._async_request = async_request

    async def async_create(self, tag_name: str) -> dict[str, Any]:
        """Create a new tag."""
        data = await self._async_request(
            "post", "/api/tags/", json={"example": tag_name}
        )
        return cast(Dict[str, Any], data)

    async def async_get_all(
        self,
        *,
        limit: int | None = None,
        offset: int | None = None,
    ) -> dict[str, Any]:
        """Return all tags."""
        params = {}
        for kwarg, param_name in (
            (limit, "limit"),
            (offset, "offset"),
        ):
            if kwarg:
                params[param_name] = kwarg

        data = await self._async_request("get", "/api/tags/", params=params)
        return cast(Dict[str, Any], data)

    async def async_get_single(self, tag_id: int) -> dict[str, Any]:
        """Return a single tag."""
        data = await self._async_request("get", f"/api/tags/{tag_id}/")
        return cast(Dict[str, Any], data)
