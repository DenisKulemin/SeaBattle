"""Module with errors for ship's objects."""


class BaseShipError(Exception):
    """Base class for ship error."""


class NotParallelShipError(BaseShipError):
    """Raised if ship is not parallel x- or y-axis."""


class WrongShipSizeError(BaseShipError):
    """Raised if ship size doesn't match with end's coordinates size."""


class WrongShipCoordinateError(BaseShipError):
    """Raised if ship size according to end's coordinates doesn't match the actual coordinates."""
