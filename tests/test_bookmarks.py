"""Define tests for the client."""
# pylint: disable=protected-access
import json

import aiohttp
import pytest

from aiolinkding import Client

from .common import TEST_TOKEN, TEST_URL, load_fixture


@pytest.mark.asyncio
async def test_bookmarks_get_all(aresponses, bookmarks_async_all_response):
    """Test getting all bookmarks."""
    aresponses.add(
        "127.0.0.1:8000",
        "/api/bookmarks/",
        "get",
        aresponses.Response(
            text=json.dumps(bookmarks_async_all_response),
            status=200,
            headers={"Content-Type": "application/json"},
        ),
    )

    async with aiohttp.ClientSession() as session:
        client = Client(TEST_URL, TEST_TOKEN, session=session)
        # Include limit to exercise the inclusion of request parameters:
        bookmarks = await client.bookmarks.async_all(limit=100)
        assert bookmarks == bookmarks_async_all_response


@pytest.mark.asyncio
async def test_bookmarks_get_archived(aresponses, bookmarks_async_archived_response):
    """Test getting archived bookmarks."""
    aresponses.add(
        "127.0.0.1:8000",
        "/api/bookmarks/archived/",
        "get",
        aresponses.Response(
            text=json.dumps(bookmarks_async_archived_response),
            status=200,
            headers={"Content-Type": "application/json"},
        ),
    )

    async with aiohttp.ClientSession() as session:
        client = Client(TEST_URL, TEST_TOKEN, session=session)
        archived_bookmarks = await client.bookmarks.async_archived()
        assert archived_bookmarks == bookmarks_async_archived_response


@pytest.mark.asyncio
async def test_bookmarks_get_all_no_explicit_session(
    aresponses, bookmarks_async_all_response
):
    """Test getting all bookmarks without an explicit ClientSession."""
    aresponses.add(
        "127.0.0.1:8000",
        "/api/bookmarks/",
        "get",
        aresponses.Response(
            text=json.dumps(bookmarks_async_all_response),
            status=200,
            headers={"Content-Type": "application/json"},
        ),
    )

    client = Client(TEST_URL, TEST_TOKEN)
    assert client._session is None

    bookmarks = await client.bookmarks.async_all()
    assert bookmarks == bookmarks_async_all_response
