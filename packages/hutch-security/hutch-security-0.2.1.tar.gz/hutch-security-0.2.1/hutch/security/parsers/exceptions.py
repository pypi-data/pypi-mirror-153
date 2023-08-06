"""Provides parser related exceptions."""


class ParserException(Exception):
    """A generic parser exception.

    All exceptions should inherit from this to allow for hierarchical handling.
    """

    pass


class FieldNotFoundException(ParserException):
    """Indicates that a requested field was not found."""

    pass
