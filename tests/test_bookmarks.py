"""Define tests for the client."""
# pylint: disable=protected-access
import json

import aiohttp
import pytest

from aiolinkding import Client

from .common import TEST_TOKEN, TEST_URL


@pytest.mark.asyncio
async def test_archive(aresponses):
    """Test archiving a bookmark."""
    aresponses.add(
        "127.0.0.1:8000",
        "/api/bookmarks/1/archive/",
        "post",
        aresponses.Response(status=204),
    )

    async with aiohttp.ClientSession() as session:
        client = Client(TEST_URL, TEST_TOKEN, session=session)
        await client.bookmarks.async_archive(1)

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_create(aresponses, bookmarks_async_get_single_response):
    """Test creating a single bookmark."""
    aresponses.add(
        "127.0.0.1:8000",
        "/api/bookmarks/",
        "post",
        aresponses.Response(
            text=json.dumps(bookmarks_async_get_single_response),
            status=201,
            headers={"Content-Type": "application/json"},
        ),
    )

    async with aiohttp.ClientSession() as session:
        client = Client(TEST_URL, TEST_TOKEN, session=session)
        created_bookmark = await client.bookmarks.async_create(
            "https://example.com",
            title="Example title",
            description="Example description",
            tag_names=[
                "tag1",
                "tag2",
            ],
        )
        assert created_bookmark == bookmarks_async_get_single_response

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_delete(aresponses):
    """Test deleting a bookmark."""
    aresponses.add(
        "127.0.0.1:8000",
        "/api/bookmarks/1/",
        "delete",
        aresponses.Response(status=204),
    )

    async with aiohttp.ClientSession() as session:
        client = Client(TEST_URL, TEST_TOKEN, session=session)
        await client.bookmarks.async_delete(1)

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_get_all(aresponses, bookmarks_async_get_all_response):
    """Test getting all bookmarks."""
    aresponses.add(
        "127.0.0.1:8000",
        "/api/bookmarks/?limit=100",
        "get",
        aresponses.Response(
            text=json.dumps(bookmarks_async_get_all_response),
            status=200,
            headers={"Content-Type": "application/json"},
        ),
        match_querystring=True,
    )

    async with aiohttp.ClientSession() as session:
        client = Client(TEST_URL, TEST_TOKEN, session=session)
        # Include limit to exercise the inclusion of request parameters:
        bookmarks = await client.bookmarks.async_get_all(limit=100)
        assert bookmarks == bookmarks_async_get_all_response

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_get_all_no_explicit_session(
    aresponses, bookmarks_async_get_all_response
):
    """Test getting all bookmarks without an explicit ClientSession."""
    aresponses.add(
        "127.0.0.1:8000",
        "/api/bookmarks/",
        "get",
        aresponses.Response(
            text=json.dumps(bookmarks_async_get_all_response),
            status=200,
            headers={"Content-Type": "application/json"},
        ),
    )

    client = Client(TEST_URL, TEST_TOKEN)
    assert client._session is None

    bookmarks = await client.bookmarks.async_get_all()
    assert bookmarks == bookmarks_async_get_all_response

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_get_archived(aresponses, bookmarks_async_get_archived_response):
    """Test getting archived bookmarks."""
    aresponses.add(
        "127.0.0.1:8000",
        "/api/bookmarks/archived/",
        "get",
        aresponses.Response(
            text=json.dumps(bookmarks_async_get_archived_response),
            status=200,
            headers={"Content-Type": "application/json"},
        ),
    )

    async with aiohttp.ClientSession() as session:
        client = Client(TEST_URL, TEST_TOKEN, session=session)
        archived_bookmarks = await client.bookmarks.async_get_archived()
        assert archived_bookmarks == bookmarks_async_get_archived_response

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_get_single(aresponses, bookmarks_async_get_single_response):
    """Test getting a single bookmark."""
    aresponses.add(
        "127.0.0.1:8000",
        "/api/bookmarks/1/",
        "get",
        aresponses.Response(
            text=json.dumps(bookmarks_async_get_single_response),
            status=200,
            headers={"Content-Type": "application/json"},
        ),
    )

    async with aiohttp.ClientSession() as session:
        client = Client(TEST_URL, TEST_TOKEN, session=session)
        single_bookmark = await client.bookmarks.async_get_single(1)
        assert single_bookmark == bookmarks_async_get_single_response

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_unarchive(aresponses):
    """Test unarchiving a bookmark."""
    aresponses.add(
        "127.0.0.1:8000",
        "/api/bookmarks/1/unarchive/",
        "post",
        aresponses.Response(status=204),
    )

    async with aiohttp.ClientSession() as session:
        client = Client(TEST_URL, TEST_TOKEN, session=session)
        await client.bookmarks.async_unarchive(1)

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_update(aresponses, bookmarks_async_get_single_response):
    """Test creating a single bookmark."""
    aresponses.add(
        "127.0.0.1:8000",
        "/api/bookmarks/1/",
        "patch",
        aresponses.Response(
            text=json.dumps(bookmarks_async_get_single_response),
            status=200,
            headers={"Content-Type": "application/json"},
        ),
    )

    async with aiohttp.ClientSession() as session:
        client = Client(TEST_URL, TEST_TOKEN, session=session)
        updated_bookmark = await client.bookmarks.async_update(
            1,
            url="https://example.com",
            title="Example title",
            description="Example description",
            tag_names=[
                "tag1",
                "tag2",
            ],
        )
        assert updated_bookmark == bookmarks_async_get_single_response

    aresponses.assert_plan_strictly_followed()
