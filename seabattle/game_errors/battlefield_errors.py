"""Module with errors for battlefield."""


class BaseBattleFieldError(Exception):
    """Base exception class for battlefield."""


class AreaOutsideBattleFieldError(BaseBattleFieldError):
    """Raised if area with coordinates is outside game battlefield."""


class BlockedAreaError(BaseBattleFieldError):
    """Raised if area with coordinates is not empty."""


class BlockedAreaAroundError(BaseBattleFieldError):
    """Raised if area around coordinates is not empty."""


class ShotCellEarlierError(BaseBattleFieldError):
    """Raised if cell for shooting was already shot earlier."""
