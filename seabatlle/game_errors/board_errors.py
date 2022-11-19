"""Module with errors for game board."""


class BaseBoardError(Exception):
    """Base exception class for board."""


class BlockedAreaError(BaseBoardError):
    """Raised if area with coordinates is not empty."""


class BlockedAreaAroundError(BaseBoardError):
    """Raised if area around coordinates is not empty."""


class ShotCellEarlierError(BaseBoardError):
    """Raised if cell for shooting was already shot earlier."""
