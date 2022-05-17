"""Run a base example."""
import asyncio
import logging

from aiohttp import ClientSession

from aiolinkding import Client
from aiolinkding.errors import LinkDingError

_LOGGER = logging.getLogger()

URL = "<URL>"
TOKEN = "<TOKEN>"


async def main() -> None:
    """Create the aiohttp session and run the example."""
    logging.basicConfig(level=logging.INFO)
    async with ClientSession() as session:
        try:
            client = Client(URL, TOKEN, session=session)

            bookmarks = await client.bookmarks.async_all()
            _LOGGER.info("Bookmarks: %s", bookmarks)

            archived_bookmarks = await client.bookmarks.async_archived()
            _LOGGER.info("Archived Bookmarks: %s", archived_bookmarks)

            single_bookmark = await client.bookmarks.async_get(1)
            _LOGGER.info("Bookmark ID: %s", single_bookmark)
        except LinkDingError as err:
            _LOGGER.error("There was an error: %s", err)


asyncio.run(main())
