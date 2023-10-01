"""Define an API client."""
from __future__ import annotations

from typing import Any

from aiohttp import ClientSession, ClientTimeout
from aiohttp.client_exceptions import ClientResponseError
from packaging import version

from aiolinkding.bookmark import BookmarkManager
from aiolinkding.const import LOGGER
from aiolinkding.errors import (
    InvalidServerVersionError,
    InvalidTokenError,
    RequestError,
    UnknownEndpointError,
)
from aiolinkding.tag import TagManager
from aiolinkding.user import UserManager

DEFAULT_REQUEST_TIMEOUT = 10

SERVER_VERSION_HEALTH_CHECK_INTRODUCED = version.parse("1.17.0")
SERVER_VERSION_MINIMUM_REQUIRED = version.parse("1.22.0")

INVALID_SERVER_VERSION_MESSAGE = (
    "Server version ({0}) is below the minimum version required "
    f"({SERVER_VERSION_MINIMUM_REQUIRED})"
)


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
        self.user = UserManager(self.async_request)

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
            UnknownEndpointError: Raised when requesting an unknown API endpoint.
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
            if resp.status == 401:
                raise InvalidTokenError("Invalid API token") from err
            if resp.status == 404:
                # We break out this particular response for the health check; if we
                # catch this when querying GET /health, we can raise a better final
                # exception:
                raise UnknownEndpointError(f"Unknown API endpoint: {endpoint}") from err
            raise RequestError(f"Error while requesting {endpoint}: {data}") from err
        finally:
            if not use_running_session:
                await session.close()

        LOGGER.debug("Data received for %s: %s", endpoint, data)

        return data


async def async_get_client(
    url: str, token: str, *, session: ClientSession | None = None
) -> Client:
    """Get an authenticated, version-checked client.

    Args:
        url: The full URL to a linkding instance.
        token: A linkding API token.
        session: An optional aiohttp ClientSession.

    Returns:
        A Client object.

    Raises:
        InvalidServerVersionError: Raised when the server version is too low.
    """
    client = Client(url, token, session=session)

    try:
        health_resp = await client.async_request("get", "/health")
    except UnknownEndpointError as err:
        raise InvalidServerVersionError(
            INVALID_SERVER_VERSION_MESSAGE.format(
                f"older than {SERVER_VERSION_HEALTH_CHECK_INTRODUCED}"
            )
        ) from err

    server_version = version.parse(health_resp["version"])

    if server_version < SERVER_VERSION_MINIMUM_REQUIRED:
        raise InvalidServerVersionError(
            INVALID_SERVER_VERSION_MESSAGE.format(server_version)
        )

    return client
