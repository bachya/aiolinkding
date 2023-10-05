"""Define an object to manage bookmark-based API requests."""
from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import Any

from aiolinkding.util import generate_api_payload


class BookmarkManager:
    """Define the API manager object."""

    def __init__(self, async_request: Callable[..., Awaitable[dict[str, Any]]]) -> None:
        """Initialize.

        Args:
            async_request: The request method from the Client object.
        """
        self._async_request = async_request

    async def _async_get_bookmarks(
        self,
        *,
        archived: bool = False,
        query: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> dict[str, Any]:
        """Return all bookmarks.

        Args:
            archived: Include archived bookmarks.
            query: Return bookmarks matching a query string.
            limit: Limit the number of returned bookmarks.
            offset: The index at which to return results.

        Returns:
            An API response payload.
        """
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

        return await self._async_request("get", endpoint, params=params)

    async def async_archive(self, bookmark_id: int) -> None:
        """Archive a bookmark.

        Args:
            bookmark_id: The ID of the bookmark to archive.
        """
        await self._async_request("post", f"/api/bookmarks/{bookmark_id}/archive/")

    async def async_delete(self, bookmark_id: int) -> None:
        """Delete a bookmark.

        Args:
            bookmark_id: The ID of the bookmark to delete.
        """
        await self._async_request("delete", f"/api/bookmarks/{bookmark_id}/")

    async def async_get_all(
        self,
        *,
        query: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> dict[str, Any]:
        """Return all bookmarks.

        Args:
            query: Return bookmarks matching a query string.
            limit: Limit the number of returned bookmarks.
            offset: The index at which to return results.

        Returns:
            An API response payload.
        """
        return await self._async_get_bookmarks(query=query, limit=limit, offset=offset)

    async def async_get_archived(
        self,
        *,
        query: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> dict[str, Any]:
        """Return all archived bookmarks.

        Args:
            query: Return bookmarks matching a query string.
            limit: Limit the number of returned bookmarks.
            offset: The index at which to return results.

        Returns:
            An API response payload.
        """
        return await self._async_get_bookmarks(
            archived=True, query=query, limit=limit, offset=offset
        )

    async def async_create(  # pylint: disable=too-many-arguments
        self,
        url: str,
        *,
        title: str | None = None,
        description: str | None = None,
        notes: str | None = None,
        tag_names: list[str] | None = None,
        is_archived: bool = False,
        unread: bool = False,
        shared: bool = False,
    ) -> dict[str, Any]:
        """Create a new bookmark.

        Args:
            url: The bookmark URL.
            title: The bookmark title.
            description: The bookmark description.
            notes: Any Markdown-formatted notes.
            tag_names: A list of strings to use as tags.
            is_archived: Immediately archive the bookmark.
            unread: Immediately mark the bookmark as unread.
            shared: Immediately mark the bookmark as shared.

        Returns:
            An API response payload.
        """
        payload = generate_api_payload(
            (
                ("url", url),
                ("title", title),
                ("description", description),
                ("notes", notes),
                ("tag_names", tag_names),
                ("is_archived", is_archived),
                ("unread", unread),
                ("shared", shared),
            )
        )

        return await self._async_request("post", "/api/bookmarks/", json=payload)

    async def async_get_single(self, bookmark_id: int) -> dict[str, Any]:
        """Return a single bookmark.

        Args:
            bookmark_id: The ID of the bookmark to get.

        Returns:
            An API response payload.
        """
        return await self._async_request("get", f"/api/bookmarks/{bookmark_id}/")

    async def async_unarchive(self, bookmark_id: int) -> None:
        """Unarchive a bookmark.

        Args:
            bookmark_id: The ID of the bookmark to unarchive.
        """
        await self._async_request("post", f"/api/bookmarks/{bookmark_id}/unarchive/")

    async def async_update(  # pylint: disable=too-many-arguments
        self,
        bookmark_id: int,
        *,
        url: str | None = None,
        title: str | None = None,
        description: str | None = None,
        notes: str | None = None,
        tag_names: list[str] | None = None,
        unread: bool = False,
        shared: bool = False,
    ) -> dict[str, Any]:
        """Update an existing bookmark.

        Args:
            bookmark_id: The ID of the bookmark to update.
            url: The bookmark URL.
            title: The bookmark title.
            description: The bookmark description.
            notes: Any Markdown-formatted notes.
            tag_names: A list of strings to use as tags.
            unread: Immediately mark the bookmark as unread.
            shared: Immediately mark the bookmark as shared.

        Returns:
            An API response payload.
        """
        payload = generate_api_payload(
            (
                ("url", url),
                ("title", title),
                ("description", description),
                ("notes", notes),
                ("tag_names", tag_names),
                ("unread", unread),
                ("shared", shared),
            )
        )

        return await self._async_request(
            "patch", f"/api/bookmarks/{bookmark_id}/", json=payload
        )
