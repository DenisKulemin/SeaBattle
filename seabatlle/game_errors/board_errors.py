"""Module with errors for game board."""


class BlockedAreaError(Exception):
    """Raised if area with coordinates is not empty."""


class BlockedAreaAroundError(Exception):
    """Raised if area around coordinates is not empty."""


class ShotCellEarlierError(Exception):
    """Raised if cell for shooting was already shot earlier."""
