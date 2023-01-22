"""Module contains custom API errors."""


class ApiError(Exception):
    """Base class for custom API errors."""


class NoGameApiError(ApiError):
    """Raises if request contains game id that doesn't exist in storage."""


class NoGamePlayerApiError(ApiError):
    """Raises if request contains player id that doesn't exist in game from storage."""
