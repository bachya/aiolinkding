"""Define tests for the client."""
from typing import Any

import aiohttp
import pytest
from aresponses import ResponsesMockServer

from aiolinkding import async_get_client
from aiolinkding.errors import (
    InvalidServerVersionError,
    InvalidTokenError,
    RequestError,
)

from .common import TEST_TOKEN, TEST_URL


@pytest.mark.asyncio
async def test_health_endpiont_missing(
    aresponses: ResponsesMockServer,
) -> None:
    """Test an API call when /health missing.

    Args:
        aresponses: An aresponses server.
    """
    aresponses.add(
        "127.0.0.1:8000",
        "/health",
        "get",
        response=aresponses.Response(
            text=None, status=404, headers={"Content-Type": "text/html; charset=utf-8"}
        ),
    )

    async with aiohttp.ClientSession() as session:
        with pytest.raises(InvalidServerVersionError):
            _ = await async_get_client(TEST_URL, TEST_TOKEN, session=session)

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "health_response",
    [
        {
            "version": "1.0.0",
            "status": "healthy",
        }
    ],
)
async def test_invalid_server_version(
    aresponses: ResponsesMockServer,
    health_response: dict[str, Any],
) -> None:
    """Test an API call with an invalid server version.

    Args:
        aresponses: An aresponses server.
        health_response: An API response payload.
    """
    aresponses.add(
        "127.0.0.1:8000",
        "/health",
        "get",
        response=aiohttp.web_response.json_response(health_response, status=200),
    )

    async with aiohttp.ClientSession() as session:
        with pytest.raises(InvalidServerVersionError):
            _ = await async_get_client(TEST_URL, TEST_TOKEN, session=session)

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_invalid_token(
    aresponses: ResponsesMockServer,
    authenticated_linkding_api_server: ResponsesMockServer,
    invalid_token_response: dict[str, Any],
) -> None:
    """Test an API call with an invalid token.

    Args:
        aresponses: An aresponses server.
        authenticated_linkding_api_server: A mock authenticated linkding API server.
        invalid_token_response: An API response payload.
    """
    async with authenticated_linkding_api_server:
        authenticated_linkding_api_server.add(
            "127.0.0.1:8000",
            "/api/whatever/",
            "get",
            response=aiohttp.web_response.json_response(
                invalid_token_response, status=401
            ),
        )

        async with aiohttp.ClientSession() as session:
            with pytest.raises(InvalidTokenError):
                client = await async_get_client(TEST_URL, TEST_TOKEN, session=session)
                await client.async_request("get", "/api/whatever/")

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_request_error(
    aresponses: ResponsesMockServer,
    authenticated_linkding_api_server: ResponsesMockServer,
    missing_field_response: dict[str, Any],
) -> None:
    """Test an API call with a general request error.

    Args:
        aresponses: An aresponses server.
        authenticated_linkding_api_server: A mock authenticated linkding API server.
        missing_field_response: An API response payload.
    """
    async with authenticated_linkding_api_server:
        authenticated_linkding_api_server.add(
            "127.0.0.1:8000",
            "/api/whatever/",
            "get",
            response=aiohttp.web_response.json_response(
                missing_field_response, status=400
            ),
        )

        async with aiohttp.ClientSession() as session:
            with pytest.raises(RequestError) as err:
                client = await async_get_client(TEST_URL, TEST_TOKEN, session=session)
                await client.async_request("get", "/api/whatever/")
            assert "This field is required" in str(err)

    aresponses.assert_plan_strictly_followed()
