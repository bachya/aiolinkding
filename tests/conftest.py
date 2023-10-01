"""Define dynamic fixtures."""
import json
from collections.abc import Generator
from typing import Any, cast

import aiohttp
import pytest
from aresponses import ResponsesMockServer

from aiolinkding.client import SERVER_VERSION_MINIMUM_REQUIRED
from tests.common import load_fixture


@pytest.fixture(name="authenticated_linkding_api_server")
def authenticated_linkding_api_server_fixture(
    health_response: dict[str, Any]
) -> Generator[ResponsesMockServer, None, None]:
    """Return a fixture that mocks an authenticated linkding API server.

    Args:
        health_response: An API response payload
    """
    server = ResponsesMockServer()
    server.add(
        "127.0.0.1:8000",
        "/health",
        "get",
        response=aiohttp.web_response.json_response(health_response, status=200),
    )
    yield server


@pytest.fixture(name="bookmarks_async_get_all_response", scope="session")
def bookmarks_async_get_all_response_fixture() -> dict[str, Any]:
    """Define a fixture to return all bookmarks."""
    return cast(
        dict[str, Any],
        json.loads(load_fixture("bookmarks_async_get_all_response.json")),
    )


@pytest.fixture(name="bookmarks_async_get_archived_response", scope="session")
def bookmarks_async_get_archived_response_fixture() -> dict[str, Any]:
    """Define a fixture to return all archived bookmarks."""
    return cast(
        dict[str, Any],
        json.loads(load_fixture("bookmarks_async_get_archived_response.json")),
    )


@pytest.fixture(name="bookmarks_async_get_single_response", scope="session")
def bookmarks_async_get_single_response_fixture() -> dict[str, Any]:
    """Define a fixture to return a single bookmark."""
    return cast(
        dict[str, Any],
        json.loads(load_fixture("bookmarks_async_get_single_response.json")),
    )


@pytest.fixture(name="health_response")
def health_response_fixture() -> dict[str, Any]:
    """Define a fixture to return a healthy health response."""
    return {
        "version": str(SERVER_VERSION_MINIMUM_REQUIRED),
        "status": "healthy",
    }


@pytest.fixture(name="invalid_token_response", scope="session")
def invalid_token_response_fixture() -> dict[str, Any]:
    """Define a fixture to return an invalid token response."""
    return cast(dict[str, Any], json.loads(load_fixture("invalid_token_response.json")))


@pytest.fixture(name="missing_field_response", scope="session")
def missing_field_response_fixture() -> dict[str, Any]:
    """Define a fixture to return a missing field response."""
    return cast(dict[str, Any], json.loads(load_fixture("missing_field_response.json")))


@pytest.fixture(name="tags_async_get_all_response", scope="session")
def tags_async_get_all_response_fixture() -> dict[str, Any]:
    """Define a fixture to return all tags."""
    return cast(
        dict[str, Any], json.loads(load_fixture("tags_async_get_all_response.json"))
    )


@pytest.fixture(name="tags_async_get_single_response", scope="session")
def tags_async_get_single_response_fixture() -> dict[str, Any]:
    """Define a fixture to return a single tag."""
    return cast(
        dict[str, Any], json.loads(load_fixture("tags_async_get_single_response.json"))
    )


@pytest.fixture(name="user_async_get_profile_response", scope="session")
def user_async_get_profile_response_fixture() -> dict[str, Any]:
    """Define a fixture to return user profile data."""
    return cast(
        dict[str, Any],
        json.loads(load_fixture("user_async_get_profile_response.json")),
    )
