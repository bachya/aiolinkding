"""Define an object to manage tag-based API requests."""
from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import Any, cast

from aiolinkding.util import generate_api_payload


class TagManager:
    """Define the API manager object."""

    def __init__(self, async_request: Callable[..., Awaitable]) -> None:
        """Initialize.

        Args:
            async_request: The request method from the Client object.
        """
        self._async_request = async_request

    async def async_create(self, tag_name: str) -> dict[str, Any]:
        """Create a new tag.

        Args:
            tag_name: The tag to create.

        Returns:
            An API response payload.
        """
        data = await self._async_request(
            "post", "/api/tags/", json={"example": tag_name}
        )
        return cast(dict[str, Any], data)

    async def async_get_all(
        self,
        *,
        limit: int | None = None,
        offset: int | None = None,
    ) -> dict[str, Any]:
        """Return all tags.

        Args:
            limit: Limit the number of returned tags.
            offset: The index at which to return results.

        Returns:
            An API response payload.
        """
        params = generate_api_payload(
            (
                ("limit", limit),
                ("offset", offset),
            )
        )

        data = await self._async_request("get", "/api/tags/", params=params)
        return cast(dict[str, Any], data)

    async def async_get_single(self, tag_id: int) -> dict[str, Any]:
        """Return a single tag.

        Args:
            tag_id: The ID of the tag to get.

        Returns:
            An API response payload.
        """
        data = await self._async_request("get", f"/api/tags/{tag_id}/")
        return cast(dict[str, Any], data)
