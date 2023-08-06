"""Provides JupiterOne related exceptions."""


class JupiterOneException(Exception):
    """A generic JupiterOne exception.

    All exceptions should inherit from this to allow for hierarchical handling.
    """


class QueryTimeout(JupiterOneException):
    """Indicates that a tiemout was reached and the query incomplete."""

    pass


class QueryException(JupiterOneException):
    """Indicates an error occurred during a query."""

    pass
