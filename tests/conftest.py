"""Define dynamic fixtures."""
# pylint: disable=redefined-outer-name
import json

import pytest

from tests.common import load_fixture


@pytest.fixture(name="bookmarks_async_all_response")
def bookmarks_async_all_response_fixture():
    """Define a fixture to return all bookmarks."""
    return json.loads(load_fixture("bookmarks_async_all_response.json"))


@pytest.fixture(name="bookmarks_async_archived_response")
def bookmarks_async_archived_response_fixture():
    """Define a fixture to return all archived bookmarks."""
    return json.loads(load_fixture("bookmarks_async_archived_response.json"))


@pytest.fixture(name="bookmarks_async_get_response")
def bookmarks_async_get_response_fixture():
    """Define a fixture to return a single bookmark."""
    return json.loads(load_fixture("bookmarks_async_get_response.json"))
