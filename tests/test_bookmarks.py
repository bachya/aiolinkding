"""Define tests for the client."""
# pylint: disable=protected-access
import json

import aiohttp
import pytest

from aiolinkding import Client

from .common import TEST_TOKEN, TEST_URL


@pytest.mark.asyncio
async def test_client_creation(aresponses, bookmarks_async_all_response):
    """Test the successful creation of a client."""
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
        assert client._session == session
        assert client._token == TEST_TOKEN
        assert client._url == TEST_URL

    async with aiohttp.ClientSession() as session:
        client = Client(TEST_URL, TEST_TOKEN, session=session)
        bookmarks = await client.bookmarks.async_all()
        assert bookmarks == bookmarks_async_all_response


@pytest.mark.asyncio
async def test_client_creation_no_explicit_session(
    aresponses, bookmarks_async_all_response
):
    """Test the successful creation of a client without an explicit ClientSession."""
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
    assert client._token == TEST_TOKEN
    assert client._url == TEST_URL

    client = Client(TEST_URL, TEST_TOKEN)
    bookmarks = await client.bookmarks.async_all()
    assert bookmarks == bookmarks_async_all_response
