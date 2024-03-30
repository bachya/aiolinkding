"""Define the aiolinkding package."""

from .client import Client, async_get_client

__all__ = [
    "Client",
    "async_get_client",
]
