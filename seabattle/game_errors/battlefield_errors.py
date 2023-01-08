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


class CellNotExistError(BaseBattleFieldError):
    """Raised if cell with specified coordinates is not exist."""


class ExtraShipInFleetError(BaseBattleFieldError):
    """Raised if we add too many ships with size to the battlefield."""
