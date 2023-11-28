# 🔖 aiolinkding: a Python3, async library to the linkding REST API

[![CI][ci-badge]][ci]
[![PyPI][pypi-badge]][pypi]
[![Version][version-badge]][version]
[![License][license-badge]][license]
[![Code Coverage][codecov-badge]][codecov]
[![Maintainability][maintainability-badge]][maintainability]

<a href="https://www.buymeacoffee.com/bachya1208P" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a>

`aiolinkding` is a Python3, async library that interfaces with [linkding][linkding]
instances. It is intended to be a reasonably light wrapper around the linkding API
(meaning that instead of drowning the user in custom objects/etc., it focuses on
returning JSON straight from the API).

- [Installation](#installation)
- [Python Versions](#python-versions)
- [Usage](#usage)
  - [Creating a Client](#creating-a-client)
  - [Working with Bookmarks](#working-with-bookmarks)
    - [Getting All Bookmarks](#getting-all-bookmarks)
    - [Getting Archived Bookmarks](#getting-archived-bookmarks)
    - [Getting a Single Bookmark](#getting-a-single-bookmark-by-id)
    - [Creating a New Bookmark](#creating-a-new-bookmark)
    - [Updating an Existing Bookmark by ID](#updating-an-existing-bookmark-by-id)
    - [Archiving/Unarchiving a Bookmark](#archivingunarchiving-a-bookmark)
    - [Deleting a Bookmark](#deleting-a-bookmark)
  - [Working with Tags](#working-with-tags)
    - [Getting All Tags](#getting-all-tags)
    - [Getting a Single Tag](#getting-a-single-tag-by-id)
    - [Creating a New Tag](#creating-a-new-Tag)
  - [Working with User Data](#working-with-user-data)
    - [Getting Profile Info](#getting-profile-info)
  - [Connection Pooling](#connection-pooling)
- [Contributing](#contributing)

# Installation

```bash
pip install aiolinkding
```

# Python Versions

`aiolinkding` is currently supported on:

- Python 3.10
- Python 3.11
- Python 3.12

# Usage

## Creating a Client

It's easy to create an API client for a linkding instance. All you need are two
parameters:

1. A URL to a linkding instance
2. A linkding API token

```python
import asyncio

from aiolinkding import async_get_client


async def main() -> None:
    """Use aiolinkding for fun and profit."""
    client = await async_get_client("http://127.0.0.1:8000", "token_abcde12345")


asyncio.run(main())
```

## Working with Bookmarks

### Getting All Bookmarks

```python
import asyncio

from aiolinkding import async_get_client


async def main() -> None:
    """Use aiolinkding for fun and profit."""
    client = await async_get_client("http://127.0.0.1:8000", "token_abcde12345")

    # Get all bookmarks:
    bookmarks = await client.bookmarks.async_get_all()
    # >>> { "count": 100, "next": null, "previous": null, "results": [...] }


asyncio.run(main())
```

`client.bookmarks.async_get_all()` takes three optional parameters:

- `query`: a string query to filter the returned bookmarks
- `limit`: the maximum number of results that should be returned
- `offset`: the index from which to return results (e.g., `5` starts at the fifth bookmark)

### Getting Archived Bookmarks

```python
import asyncio

from aiolinkding import async_get_client


async def main() -> None:
    """Use aiolinkding for fun and profit."""
    client = await async_get_client("http://127.0.0.1:8000", "token_abcde12345")

    # Get all archived bookmarks:
    bookmarks = await client.bookmarks.async_get_archived()
    # >>> { "count": 100, "next": null, "previous": null, "results": [...] }


asyncio.run(main())
```

`client.bookmarks.async_get_archived()` takes three optional parameters:

- `query`: a string query to filter the returned bookmarks
- `limit`: the maximum number of results that should be returned
- `offset`: the index from which to return results (e.g., `5` starts at the fifth bookmark)

### Getting a Single Bookmark by ID

```python
import asyncio

from aiolinkding import async_get_client


async def main() -> None:
    """Use aiolinkding for fun and profit."""
    client = await async_get_client("http://127.0.0.1:8000", "token_abcde12345")

    # Get a single bookmark:
    bookmark = await client.bookmarks.async_get_single(37)
    # >>> { "id": 37, "url": "https://example.com", "title": "Example title", ... }


asyncio.run(main())
```

### Creating a New Bookmark

```python
import asyncio

from aiolinkding import async_get_client


async def main() -> None:
    """Use aiolinkding for fun and profit."""
    client = await async_get_client("http://127.0.0.1:8000", "token_abcde12345")

    # Create a new bookmark:
    created_bookmark = await client.bookmarks.async_create(
        "https://example.com",
        title="Example title",
        description="Example description",
        tag_names=[
            "tag1",
            "tag2",
        ],
    )
    # >>> { "id": 37, "url": "https://example.com", "title": "Example title", ... }


asyncio.run(main())
```

`client.bookmarks.async_create()` takes four optional parameters:

- `title`: the bookmark's title
- `description`: the bookmark's description
- `notes`: Markdown notes to add to the bookmark
- `tag_names`: the tags to assign to the bookmark (represented as a list of strings)
- `is_archived`: whether the newly-created bookmark should automatically be archived
- `unread`: whether the newly-created bookmark should be marked as unread
- `shared`: whether the newly-created bookmark should be shareable with other linkding users

### Updating an Existing Bookmark by ID

```python
import asyncio

from aiolinkding import async_get_client


async def main() -> None:
    """Use aiolinkding for fun and profit."""
    client = await async_get_client("http://127.0.0.1:8000", "token_abcde12345")

    # Update an existing bookmark:
    updated_bookmark = await client.bookmarks.async_update(
        37,
        url="https://different-example.com",
        title="Different example title",
        description="Different example description",
        tag_names=[
            "tag1",
            "tag2",
        ],
    )
    # >>> { "id": 37, "url": "https://different-example.com", ... }


asyncio.run(main())
```

`client.bookmarks.async_update()` takes four optional parameters (inclusion of any parameter
will change that value for the existing bookmark):

- `url`: the bookmark's URL
- `title`: the bookmark's title
- `description`: the bookmark's description
- `notes`: Markdown notes to add to the bookmark
- `tag_names`: the tags to assign to the bookmark (represented as a list of strings)
- `unread`: whether the bookmark should be marked as unread
- `shared`: whether the bookmark should be shareable with other linkding users

### Archiving/Unarchiving a Bookmark

```python
import asyncio

from aiolinkding import async_get_client


async def main() -> None:
    """Use aiolinkding for fun and profit."""
    client = await async_get_client("http://127.0.0.1:8000", "token_abcde12345")

    # Archive a bookmark by ID:
    await client.bookmarks.async_archive(37)

    # ...and unarchive it:
    await client.bookmarks.async_unarchive(37)


asyncio.run(main())
```

### Deleting a Bookmark

```python
import asyncio

from aiolinkding import async_get_client


async def main() -> None:
    """Use aiolinkding for fun and profit."""
    client = await async_get_client("http://127.0.0.1:8000", "token_abcde12345")

    # Delete a bookmark by ID:
    await client.bookmarks.async_delete(37)


asyncio.run(main())
```

## Working with Tags

### Getting All Tags

```python
import asyncio

from aiolinkding import async_get_client


async def main() -> None:
    """Use aiolinkding for fun and profit."""
    client = await async_get_client("http://127.0.0.1:8000", "token_abcde12345")

    # Get all tags:
    tags = await client.tags.async_get_all()
    # >>> { "count": 100, "next": null, "previous": null, "results": [...] }


asyncio.run(main())
```

`client.tags.async_get_all()` takes two optional parameters:

- `limit`: the maximum number of results that should be returned
- `offset`: the index from which to return results (e.g., `5` starts at the fifth bookmark)

### Getting a Single Tag by ID

```python
import asyncio

from aiolinkding import async_get_client


async def main() -> None:
    """Use aiolinkding for fun and profit."""
    client = await async_get_client("http://127.0.0.1:8000", "token_abcde12345")

    # Get a single tag:
    tag = await client.tags.async_get_single(22)
    # >>> { "id": 22, "name": "example-tag", ... }


asyncio.run(main())
```

### Creating a New Tag

```python
import asyncio

from aiolinkding import async_get_client


async def main() -> None:
    """Use aiolinkding for fun and profit."""
    client = await async_get_client("http://127.0.0.1:8000", "token_abcde12345")

    # Create a new tag:
    created_tag = await client.tags.async_create("example-tag")
    # >>> { "id": 22, "name": "example-tag", ... }


asyncio.run(main())
```

## Working with User Data

### Getting Profile Info

```python
import asyncio

from aiolinkding import async_get_client


async def main() -> None:
    """Use aiolinkding for fun and profit."""
    client = await async_get_client("http://127.0.0.1:8000", "token_abcde12345")

    # Get all tags:
    tags = await client.user.async_get_profile()
    # >>> { "theme": "auto", "bookmark_date_display": "relative", ... }


asyncio.run(main())
```

## Connection Pooling

By default, the library creates a new connection to linkding with each coroutine. If you
are calling a large number of coroutines (or merely want to squeeze out every second of
runtime savings possible), an [`aiohttp`][aiohttp] `ClientSession` can be used for
connection pooling:

```python
import asyncio

from aiohttp import async_get_clientSession
from aiolinkding import async_get_client


async def main() -> None:
    """Use aiolinkding for fun and profit."""
    async with ClientSession() as session:
        client = await async_get_client(
            "http://127.0.0.1:8000", "token_abcde12345", session=session
        )

        # Get to work...


asyncio.run(main())
```

# Contributing

Thanks to all of [our contributors][contributors] so far!

1. [Check for open features/bugs][issues] or [initiate a discussion on one][new-issue].
2. [Fork the repository][fork].
3. (_optional, but highly recommended_) Create a virtual environment: `python3 -m venv .venv`
4. (_optional, but highly recommended_) Enter the virtual environment: `source ./.venv/bin/activate`
5. Install the dev environment: `script/setup`
6. Code your new feature or bug fix on a new branch.
7. Write tests that cover your new functionality.
8. Run tests and ensure 100% code coverage: `poetry run pytest --cov aiolinkding tests`
9. Update `README.md` with any new documentation.
10. Submit a pull request!

[aiohttp]: https://github.com/aio-libs/aiohttp
[linkding]: https://github.com/sissbruecker/linkding
[ci-badge]: https://github.com/bachya/aiolinkding/workflows/CI/badge.svg
[ci]: https://github.com/bachya/aiolinkding/actions
[codecov-badge]: https://codecov.io/gh/bachya/aiolinkding/branch/dev/graph/badge.svg
[codecov]: https://codecov.io/gh/bachya/aiolinkding
[contributors]: https://github.com/bachya/aiolinkding/graphs/contributors
[fork]: https://github.com/bachya/aiolinkding/fork
[issues]: https://github.com/bachya/aiolinkding/issues
[license-badge]: https://img.shields.io/pypi/l/aiolinkding.svg
[license]: https://github.com/bachya/aiolinkding/blob/main/LICENSE
[maintainability-badge]: https://api.codeclimate.com/v1/badges/189379773edd4035a612/maintainability
[maintainability]: https://codeclimate.com/github/bachya/aiolinkding/maintainability
[new-issue]: https://github.com/bachya/aiolinkding/issues/new
[new-issue]: https://github.com/bachya/aiolinkding/issues/new
[pypi-badge]: https://img.shields.io/pypi/v/aiolinkding.svg
[pypi]: https://pypi.python.org/pypi/aiolinkding
[version-badge]: https://img.shields.io/pypi/pyversions/aiolinkding.svg
[version]: https://pypi.python.org/pypi/aiolinkding
