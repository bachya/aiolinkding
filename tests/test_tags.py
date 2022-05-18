"""Define tests for the client."""
# pylint: disable=protected-access
import json

import aiohttp
import pytest

from aiolinkding import Client

from .common import TEST_TOKEN, TEST_URL


@pytest.mark.asyncio
async def test_get_all(aresponses, tags_async_get_all_response):
    """Test getting all tags."""
    aresponses.add(
        "127.0.0.1:8000",
        "/api/tags/",
        "get",
        aresponses.Response(
            text=json.dumps(tags_async_get_all_response),
            status=200,
            headers={"Content-Type": "application/json"},
        ),
    )

    async with aiohttp.ClientSession() as session:
        client = Client(TEST_URL, TEST_TOKEN, session=session)
        # Include limit to exercise the inclusion of request parameters:
        tags = await client.tags.async_get_all(limit=100)
        assert tags == tags_async_get_all_response
