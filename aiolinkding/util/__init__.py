"""Define utilities."""
from __future__ import annotations

from typing import Any


def generate_api_payload(param_pairs: tuple) -> dict[str, Any]:
    """Generate an aiolinkding payload dict from parameters.

    Args:
        param_pairs: A tuple of parameter key/values.

    Returns:
        An API response payload.
    """
    payload = {}

    for key, value in param_pairs:
        if value is None:
            continue
        payload[key] = value

    return payload
