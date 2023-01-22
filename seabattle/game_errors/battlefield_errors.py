"""Module with errors for battlefield."""


class BattleFieldError(Exception):
    """Base exception class for battlefield."""


class AreaOutsideBattleFieldError(BattleFieldError):
    """Raised if area with coordinates is outside game battlefield."""


class BlockedAreaError(BattleFieldError):
    """Raised if area with coordinates is not empty."""


class BlockedAreaAroundError(BattleFieldError):
    """Raised if area around coordinates is not empty."""


class ShotCellEarlierError(BattleFieldError):
    """Raised if cell for shooting was already shot earlier."""


class CellNotExistError(BattleFieldError):
    """Raised if cell with specified coordinates is not exist."""


class ExtraShipInFleetError(BattleFieldError):
    """Raised if we add too many ships with size to the battlefield."""
