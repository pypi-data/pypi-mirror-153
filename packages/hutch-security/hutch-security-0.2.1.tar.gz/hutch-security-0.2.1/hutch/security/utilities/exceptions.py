"""Provides Utility related exceptions."""


class UtilityException(Exception):
    """A generic Utility exception.

    All exceptions should inherit from this to allow for hierarchical handling.
    """


class SocketException(UtilityException):
    """Indicates that a socket did not respond to connection attempts."""

    pass


class UnknownSchemeException(UtilityException):
    """Indicates that the scheme for the service on the given socket is unknown."""

    pass
