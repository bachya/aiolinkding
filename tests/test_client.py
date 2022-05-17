"""Define tests for the client."""
# pylint: disable=protected-access
import aiohttp
import pytest

from aiolinkding import Client
from aiolinkding.errors import InvalidTokenError, RequestError

from .common import TEST_TOKEN, TEST_URL, load_fixture


@pytest.mark.asyncio
async def test_invalid_token(aresponses):
    """Test an API call with an invalid token."""
    aresponses.add(
        "127.0.0.1:8000",
        "/api/whatever/",
        "get",
        aresponses.Response(
            text=load_fixture("invalid_token_response.json"),
            status=401,
            headers={"Content-Type": "application/json"},
        ),
    )

    async with aiohttp.ClientSession() as session:
        with pytest.raises(InvalidTokenError):
            client = Client(TEST_URL, TEST_TOKEN, session=session)
            await client.async_request("get", "/api/whatever/")


@pytest.mark.asyncio
async def test_request_error(aresponses):
    """Test an API call with a general request error."""
    aresponses.add(
        "127.0.0.1:8000",
        "/api/whatever/",
        "get",
        aresponses.Response(
            text=load_fixture("missing_field_response.json"),
            status=400,
            headers={"Content-Type": "application/json"},
        ),
    )

    async with aiohttp.ClientSession() as session:
        with pytest.raises(RequestError) as err:
            client = Client(TEST_URL, TEST_TOKEN, session=session)
            await client.async_request("get", "/api/whatever/")
        assert "This field is required" in str(err)
