"""Define package exceptions."""


class LinkDingError(Exception):
    """Define a base exception."""


class InvalidServerVersionError(LinkDingError):
    """Define an error related to an invalid server version."""


class InvalidTokenError(LinkDingError):
    """Define an error related to an invalid API token."""


class RequestError(LinkDingError):
    """An error related to invalid requests."""


class UnknownEndpointError(RequestError):
    """An error related to an unknown endpoint."""
