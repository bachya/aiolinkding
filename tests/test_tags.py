"""Define tests for tag endpoints."""
from typing import Any

import aiohttp
import pytest
from aresponses import ResponsesMockServer

from aiolinkding import async_get_client

from .common import TEST_TOKEN, TEST_URL


@pytest.mark.asyncio
async def test_create(
    aresponses: ResponsesMockServer,
    authenticated_linkding_api_server: ResponsesMockServer,
    tags_async_get_single_response: dict[str, Any],
) -> None:
    """Test creating a single tag.

    Args:
        aresponses: An aresponses server.
        authenticated_linkding_api_server: A mock authenticated linkding API server.
        tags_async_get_single_response: An API response payload.
    """
    async with authenticated_linkding_api_server:
        authenticated_linkding_api_server.add(
            "127.0.0.1:8000",
            "/api/tags/",
            "post",
            response=aiohttp.web_response.json_response(
                tags_async_get_single_response, status=201
            ),
        )

        async with aiohttp.ClientSession() as session:
            client = await async_get_client(TEST_URL, TEST_TOKEN, session=session)
            created_bookmark = await client.tags.async_create("example-tag")
            assert created_bookmark == tags_async_get_single_response

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_get_all(
    aresponses: ResponsesMockServer,
    authenticated_linkding_api_server: ResponsesMockServer,
    tags_async_get_all_response: dict[str, Any],
) -> None:
    """Test getting all tags.

    Args:
        aresponses: An aresponses server.
        authenticated_linkding_api_server: A mock authenticated linkding API server.
        tags_async_get_all_response: An API response payload.
    """
    async with authenticated_linkding_api_server:
        authenticated_linkding_api_server.add(
            "127.0.0.1:8000",
            "/api/tags/?limit=100",
            "get",
            response=aiohttp.web_response.json_response(
                tags_async_get_all_response, status=200
            ),
            match_querystring=True,
        )

        async with aiohttp.ClientSession() as session:
            client = await async_get_client(TEST_URL, TEST_TOKEN, session=session)
            # Include limit to exercise the inclusion of request parameters:
            tags = await client.tags.async_get_all(limit=100)
            assert tags == tags_async_get_all_response

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_get_single(
    aresponses: ResponsesMockServer,
    authenticated_linkding_api_server: ResponsesMockServer,
    tags_async_get_single_response: dict[str, Any],
) -> None:
    """Test getting a single tag.

    Args:
        aresponses: An aresponses server.
        authenticated_linkding_api_server: A mock authenticated linkding API server.
        tags_async_get_single_response: An API response payload.
    """
    async with authenticated_linkding_api_server:
        authenticated_linkding_api_server.add(
            "127.0.0.1:8000",
            "/api/tags/1/",
            "get",
            response=aiohttp.web_response.json_response(
                tags_async_get_single_response, status=200
            ),
        )

        async with aiohttp.ClientSession() as session:
            client = await async_get_client(TEST_URL, TEST_TOKEN, session=session)
            single_tag = await client.tags.async_get_single(1)
            assert single_tag == tags_async_get_single_response

    aresponses.assert_plan_strictly_followed()
