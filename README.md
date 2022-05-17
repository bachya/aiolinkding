# 🚰 aiolinkding: DESCRIPTION

[![CI](https://github.com/bachya/aiolinkding/workflows/CI/badge.svg)](https://github.com/bachya/aiolinkding/actions)
[![PyPi](https://img.shields.io/pypi/v/aiolinkding.svg)](https://pypi.python.org/pypi/aiolinkding)
[![Version](https://img.shields.io/pypi/pyversions/aiolinkding.svg)](https://pypi.python.org/pypi/aiolinkding)
[![License](https://img.shields.io/pypi/l/aiolinkding.svg)](https://github.com/bachya/aiolinkding/blob/master/LICENSE)
[![Code Coverage](https://codecov.io/gh/bachya/aiolinkding/branch/master/graph/badge.svg)](https://codecov.io/gh/bachya/aiolinkding)
[![Maintainability](https://api.codeclimate.com/v1/badges/189379773edd4035a612/maintainability)](https://codeclimate.com/github/bachya/aiolinkding/maintainability)
[![Say Thanks](https://img.shields.io/badge/SayThanks-!-1EAEDB.svg)](https://saythanks.io/to/bachya)

DESCRIPTION

 [Installation](#installation)
- [Python Versions](#python-versions)
- [Usage](#usage)
  * [Creating a Client](#creating-a-client)
  * [Working with Bookmarks](#working-with-bookmarks)
    + [Getting All Bookmarks](#getting-all-bookmarks)
    + [Getting Archived Bookmarks](#getting-archived-bookmarks)
    + [Getting a Single Bookmark](#getting-a-single-bookmark)
  * [Connection Pooling](#connection-pooling)
- [Contributing](#contributing)

# Installation

```python
pip install aiolinkding
```

# Python Versions

`aiolinkding` is currently supported on:

* Python 3.8
* Python 3.9
* Python 3.10

# Usage

## Creating a Client

It's easy to create an API client for a linkding instance. All you need are two
parameters:

1. A URL to a linkding instance
2. A linkding API token

```python
import asyncio

from aiohttp import ClientSession

from aiolinkding import Client


async def main() -> None:
    """Use aiolinkding for fun and profit."""
    client = Client("http://127.0.0.1:8000", "token_abcde12345")


asyncio.run(main())
```

## Working with Bookmarks

The `Client` object provides easy access to several bookmark-related API operations.

### Getting All Bookmarks

```python
import asyncio

from aiohttp import ClientSession

from aiolinkding import Client


async def main() -> None:
    """Use aiolinkding for fun and profit."""
    client = Client("http://127.0.0.1:8000", "token_abcde12345")

    # Get all bookmarks:
    bookmarks = await client.bookmarks.async_all()
    # >>> { "count": 100, "next": null, "previous": null, "results": [...] }


asyncio.run(main())
```

`client.bookmarks.async_all()` takes three optional parameters:

* `query`: a string query to filter the returned bookmarks
* `limit`: the maximum number of results that should be returned
* `offset`: the index from which to return results (e.g., `5` starts at the fifth bookmark)

### Getting Archived Bookmarks

```python
import asyncio

from aiohttp import ClientSession

from aiolinkding import Client


async def main() -> None:
    """Use aiolinkding for fun and profit."""
    client = Client("http://127.0.0.1:8000", "token_abcde12345")

    # Get all bookmarks:
    bookmarks = await client.bookmarks.async_archived()
    # >>> { "count": 100, "next": null, "previous": null, "results": [...] }


asyncio.run(main())
```

`client.bookmarks.async_archived()` takes three optional parameters:

* `query`: a string query to filter the returned bookmarks
* `limit`: the maximum number of results that should be returned
* `offset`: the index from which to return results (e.g., `5` starts at the fifth bookmark)

### Getting a Single Bookmark by ID

```python
import asyncio

from aiohttp import ClientSession

from aiolinkding import Client


async def main() -> None:
    """Use aiolinkding for fun and profit."""
    client = Client("http://127.0.0.1:8000", "token_abcde12345")

    # Get all bookmarks:
    bookmarks = await client.bookmarks.async_get(37)
    # >>> { "id": 1, "url": "https://example.com", "title": "Example title", ... }


asyncio.run(main())
```

## Connection Pooling

By default, the library creates a new connection to linkding with each coroutine. If you
are calling a large number of coroutines (or merely want to squeeze out every second of
runtime savings possible), an
[`aiohttp`](https://github.com/aio-libs/aiohttp) `ClientSession` can be used for connection
pooling:

```python
import asyncio

from aiohttp import ClientSession

from aiolinkding import Client


async def main() -> None:
    """Use aiolinkding for fun and profit."""
    async with ClientSession() as session:
        client = Client("http://127.0.0.1:8000", "token_abcde12345", session=session)

        # Get to work...


asyncio.run(main())
```

# Contributing

1. [Check for open features/bugs](https://github.com/bachya/aiolinkding/issues)
  or [initiate a discussion on one](https://github.com/bachya/aiolinkding/issues/new).
2. [Fork the repository](https://github.com/bachya/aiolinkding/fork).
3. (_optional, but highly recommended_) Create a virtual environment: `python3 -m venv .venv`
4. (_optional, but highly recommended_) Enter the virtual environment: `source ./.venv/bin/activate`
5. Install the dev environment: `script/setup`
6. Code your new feature or bug fix.
7. Write tests that cover your new functionality.
8. Run tests and ensure 100% code coverage: `nox -rs coverage`
9. Update `README.md` with any new documentation.
10. Add yourself to `AUTHORS.md`.
11. Submit a pull request!
