"""Provides SumoLogic related exceptions."""


class SumologicException(Exception):
    """A generic SumoLogic exception.

    All exceptions should inherit from this to allow for hierarchical handling.
    """


class SearchTimeout(SumologicException):
    """Indicates that a tiemout was reached and the query incomplete."""

    pass


class SearchException(SumologicException):
    """Indicates an error occurred during search."""

    pass
