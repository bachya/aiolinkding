"""Define an API client."""
from __future__ import annotations

from typing import Any

from aiohttp import ClientSession, ClientTimeout
from aiohttp.client_exceptions import ClientResponseError

from aiolinkding.bookmark import BookmarkManager
from aiolinkding.const import LOGGER
from aiolinkding.errors import InvalidTokenError, RequestError
from aiolinkding.tag import TagManager

DEFAULT_REQUEST_TIMEOUT = 10


class Client:  # pylint: disable=too-few-public-methods
    """Define a client for the linkding API."""

    def __init__(
        self, url: str, token: str, *, session: ClientSession | None = None
    ) -> None:
        """Initialize.

        Args:
            url: The full URL to a linkding instance.
            token: A linkding API token.
            session: An optional aiohttp ClientSession.
        """
        self._session = session
        self._token = token
        self._url = url

        self.bookmarks = BookmarkManager(self.async_request)
        self.tags = TagManager(self.async_request)

    async def async_request(
        self, method: str, endpoint: str, **kwargs: dict[str, Any]
    ) -> dict[str, Any]:
        """Make an API request.

        Args:
            method: An HTTP method.
            endpoint: A relative API endpoint.
            **kwargs: Additional kwargs to send with the request.

        Returns:
            An API response payload.

        Raises:
            InvalidTokenError: Raised upon an invalid API token.
            RequestError: Raised upon an underlying HTTP error.
        """
        kwargs.setdefault("headers", {})
        kwargs["headers"]["Authorization"] = f"Token {self._token}"

        if use_running_session := self._session and not self._session.closed:
            session = self._session
        else:
            session = ClientSession(
                timeout=ClientTimeout(total=DEFAULT_REQUEST_TIMEOUT)
            )

        data: dict[str, Any] = {}

        try:
            async with session.request(
                method, f"{self._url}{endpoint}", **kwargs
            ) as resp:
                data = await resp.json()
                resp.raise_for_status()
        except ClientResponseError as err:
            if resp.status == 204:
                # An HTTP 204 will not return parsable JSON data, but it's still a
                # successful response, so we swallow the exception and return:
                return {}
            if err.status == 401:
                raise InvalidTokenError("Invalid API token") from err
            raise RequestError(f"Error while requesting {endpoint}: {data}") from err
        finally:
            if not use_running_session:
                await session.close()

        LOGGER.debug("Data received for %s: %s", endpoint, data)

        return data
