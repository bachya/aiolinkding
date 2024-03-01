"""Define tests for user endpoints."""

from typing import Any

import aiohttp
import pytest
from aresponses import ResponsesMockServer

from aiolinkding import async_get_client

from .common import TEST_TOKEN, TEST_URL


@pytest.mark.asyncio
async def test_get_profile(
    aresponses: ResponsesMockServer,
    authenticated_linkding_api_server: ResponsesMockServer,
    user_async_get_profile_response: dict[str, Any],
) -> None:
    """Test getting all tags.

    Args:
        aresponses: An aresponses server.
        authenticated_linkding_api_server: A mock authenticated linkding API server.
        user_async_get_profile_response: An API response payload.
    """
    async with authenticated_linkding_api_server:
        authenticated_linkding_api_server.add(
            "127.0.0.1:8000",
            "/api/user/profile/",
            "get",
            response=aiohttp.web_response.json_response(
                user_async_get_profile_response, status=200
            ),
        )

        async with aiohttp.ClientSession() as session:
            client = await async_get_client(TEST_URL, TEST_TOKEN, session=session)
            profile_info = await client.user.async_get_profile()
            assert profile_info == user_async_get_profile_response

    aresponses.assert_plan_strictly_followed()
