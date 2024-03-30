"""Run a base example."""

import asyncio
import logging

from aiohttp import ClientSession

from aiolinkding import async_get_client
from aiolinkding.errors import LinkDingError

_LOGGER = logging.getLogger()

URL = "<LINDKING URL>"
TOKEN = "<LINDKING TOKEN>"  # noqa: S105


async def main() -> None:
    """Create the aiohttp session and run the example."""
    logging.basicConfig(level=logging.INFO)
    async with ClientSession() as session:
        try:
            client = await async_get_client(URL, TOKEN, session=session)

            bookmarks = await client.bookmarks.async_get_all()
            _LOGGER.info("Bookmarks: %s", bookmarks)

            archived_bookmarks = await client.bookmarks.async_get_archived()
            _LOGGER.info("Archived Bookmarks: %s", archived_bookmarks)

            single_bookmark = await client.bookmarks.async_get_single(1)
            _LOGGER.info("Bookmark ID: %s", single_bookmark)

            created_bookmark = await client.bookmarks.async_create(
                "https://example.com",
                title="Example title",
                description="Example description",
                tag_names=[
                    "tag1",
                    "tag2",
                ],
            )
            _LOGGER.info("Created Bookmark: %s", created_bookmark)

            tags = await client.tags.async_get_all()
            _LOGGER.info("tags: %s", tags)
        except LinkDingError:
            _LOGGER.exception("There was an error: %s")


asyncio.run(main())
