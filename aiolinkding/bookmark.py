"""Define an object to manage bookmark-based API requests."""
from __future__ import annotations

from collections.abc import Awaitable
from typing import Any, Callable, Dict, cast


class BookmarkManager:
    """Define the API manager object."""

    def __init__(self, async_request: Callable[..., Awaitable]) -> None:
        """Initialize."""
        self._async_request = async_request

    async def _async_get_bookmarks(
        self,
        *,
        archived: bool = False,
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

        endpoint = "/api/bookmarks/"
        if archived:
            endpoint += "archived/"

        data = await self._async_request("get", endpoint)
        return cast(Dict[str, Any], data)

    async def async_get_all(
        self,
        *,
        query: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> dict[str, Any]:
        """Return all bookmarks."""
        return await self._async_get_bookmarks(query=query, limit=limit, offset=offset)

    async def async_get_archived(
        self,
        *,
        query: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> dict[str, Any]:
        """Return all archived bookmarks."""
        return await self._async_get_bookmarks(
            archived=True, query=query, limit=limit, offset=offset
        )

    async def async_create(
        self,
        url: str,
        *,
        title: str | None = None,
        description: str | None = None,
        tag_names: list[str] | None = None,
    ) -> dict[str, Any]:
        """Create a new bookmark."""
        payload: dict[str, str | list] = {"url": url}
        for kwarg, param_name in (
            (title, "title"),
            (description, "description"),
            (tag_names, "tag_names"),
        ):
            if kwarg:
                payload[param_name] = kwarg
        data = await self._async_request("post", "/api/bookmarks/", json=payload)
        return cast(Dict[str, Any], data)

    async def async_get_single(self, bookmark_id: int) -> dict[str, Any]:
        """Return a single bookmark by its ID."""
        data = await self._async_request("get", f"/api/bookmarks/{bookmark_id}/")
        return cast(Dict[str, Any], data)
