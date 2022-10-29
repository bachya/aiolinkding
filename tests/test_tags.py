"""Define tests for the client."""
# pylint: disable=protected-access
import json
from typing import Any

import aiohttp
import pytest
from aresponses import ResponsesMockServer

from aiolinkding import Client

from .common import TEST_TOKEN, TEST_URL


@pytest.mark.asyncio
async def test_create(
    aresponses: ResponsesMockServer, tags_async_get_single_response: dict[str, Any]
) -> None:
    """Test creating a single tag.

    Args:
        aresponses: An aresponses server.
        tags_async_get_single_response: An API response payload.
    """
    aresponses.add(
        "127.0.0.1:8000",
        "/api/tags/",
        "post",
        aresponses.Response(
            text=json.dumps(tags_async_get_single_response),
            status=201,
            headers={"Content-Type": "application/json"},
        ),
    )

    async with aiohttp.ClientSession() as session:
        client = Client(TEST_URL, TEST_TOKEN, session=session)
        created_bookmark = await client.tags.async_create("example-tag")
        assert created_bookmark == tags_async_get_single_response

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_get_all(
    aresponses: ResponsesMockServer, tags_async_get_all_response: dict[str, Any]
) -> None:
    """Test getting all tags.

    Args:
        aresponses: An aresponses server.
        tags_async_get_all_response: An API response payload.
    """
    aresponses.add(
        "127.0.0.1:8000",
        "/api/tags/?limit=100",
        "get",
        aresponses.Response(
            text=json.dumps(tags_async_get_all_response),
            status=200,
            headers={"Content-Type": "application/json"},
        ),
        match_querystring=True,
    )

    async with aiohttp.ClientSession() as session:
        client = Client(TEST_URL, TEST_TOKEN, session=session)
        # Include limit to exercise the inclusion of request parameters:
        tags = await client.tags.async_get_all(limit=100)
        assert tags == tags_async_get_all_response

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_get_single(
    aresponses: ResponsesMockServer, tags_async_get_single_response: dict[str, Any]
) -> None:
    """Test getting a single tag.

    Args:
        aresponses: An aresponses server.
        tags_async_get_single_response: An API response payload.
    """
    aresponses.add(
        "127.0.0.1:8000",
        "/api/tags/1/",
        "get",
        aresponses.Response(
            text=json.dumps(tags_async_get_single_response),
            status=200,
            headers={"Content-Type": "application/json"},
        ),
    )

    async with aiohttp.ClientSession() as session:
        client = Client(TEST_URL, TEST_TOKEN, session=session)
        single_tag = await client.tags.async_get_single(1)
        assert single_tag == tags_async_get_single_response

    aresponses.assert_plan_strictly_followed()
