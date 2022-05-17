"""Run a base example."""
import asyncio
import logging

from aiohttp import ClientSession

from aiolinkding import Client
from aiolinkding.errors import LinkDingError

_LOGGER = logging.getLogger()

URL = "https://4605c307-e14e-4ae8-962b-0789cc65642f.bachyaproductions.com:2096"
TOKEN = "b9f328064c2589ba473b5f1692de774d22528f0d"


async def main() -> None:
    """Create the aiohttp session and run the example."""
    logging.basicConfig(level=logging.INFO)
    async with ClientSession() as session:
        try:
            client = Client(URL, TOKEN, session=session)

            bookmarks = await client.bookmarks.async_all()
            _LOGGER.info("Bookmarks: %s", bookmarks)
        except LinkDingError as err:
            _LOGGER.error("There was an error: %s", err)


asyncio.run(main())
