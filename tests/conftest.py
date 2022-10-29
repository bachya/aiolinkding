"""Define dynamic fixtures."""
# pylint: disable=redefined-outer-name
import json
from typing import Any, cast

import pytest

from tests.common import load_fixture


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
