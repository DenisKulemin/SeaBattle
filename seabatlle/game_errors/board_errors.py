"""Module with errors for game board."""


class BlockedAreaError(Exception):
    """Raised if area with coordinates is not empty."""


class BlockedAreaAroundError(Exception):
    """Raised if area around coordinates is not empty."""
