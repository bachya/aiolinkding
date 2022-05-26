"""Define an object to manage bookmark-based API requests."""
from __future__ import annotations

from collections.abc import Awaitable
from typing import Any, Callable, Dict, cast

from aiolinkding.util import generate_api_payload


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
        params = generate_api_payload(
            (
                ("q", query),
                ("limit", limit),
                ("offset", offset),
            )
        )

        endpoint = "/api/bookmarks/"
        if archived:
            endpoint += "archived/"

        data = await self._async_request("get", endpoint, params=params)
        return cast(Dict[str, Any], data)

    async def async_archive(self, bookmark_id: int) -> None:
        """Archive a bookmark."""
        await self._async_request("post", f"/api/bookmarks/{bookmark_id}/archive/")

    async def async_delete(self, bookmark_id: int) -> None:
        """Delete a bookmark."""
        await self._async_request("delete", f"/api/bookmarks/{bookmark_id}/")

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
        is_archived: bool = False,
    ) -> dict[str, Any]:
        """Create a new bookmark."""
        payload = generate_api_payload(
            (
                ("url", url),
                ("title", title),
                ("description", description),
                ("tag_names", tag_names),
                ("is_archived", is_archived),
            )
        )

        data = await self._async_request("post", "/api/bookmarks/", json=payload)
        return cast(Dict[str, Any], data)

    async def async_get_single(self, bookmark_id: int) -> dict[str, Any]:
        """Return a single bookmark."""
        data = await self._async_request("get", f"/api/bookmarks/{bookmark_id}/")
        return cast(Dict[str, Any], data)

    async def async_unarchive(self, bookmark_id: int) -> None:
        """Unarchive a bookmark."""
        await self._async_request("post", f"/api/bookmarks/{bookmark_id}/unarchive/")

    async def async_update(
        self,
        bookmark_id: int,
        *,
        url: str | None = None,
        title: str | None = None,
        description: str | None = None,
        tag_names: list[str] | None = None,
    ) -> dict[str, Any]:
        """Update an existing bookmark."""
        payload = generate_api_payload(
            (
                ("url", url),
                ("title", title),
                ("description", description),
                ("tag_names", tag_names),
            )
        )

        data = await self._async_request(
            "patch", f"/api/bookmarks/{bookmark_id}/", json=payload
        )
        return cast(Dict[str, Any], data)
