"""Module with errors for ship's objects."""


class ShipError(Exception):
    """Base class for ship error."""


class NotParallelShipError(ShipError):
    """Raised if ship is not parallel x- or y-axis."""


class WrongShipSizeError(ShipError):
    """Raised if ship size doesn't match with end's coordinates size."""


class WrongShipCoordinateError(ShipError):
    """Raised if ship size according to end's coordinates doesn't match the actual coordinates."""
