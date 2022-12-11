"""Module with unit tests for ship object."""
import pytest

from seabattle.game_errors.ship_errors import NotParallelShipError, WrongShipSizeError, WrongShipCoordinateError
from seabattle.game_objects.cell import Cell
from seabattle.game_objects.ship import Ship


def test_ship_creation():
    """Method tests correct creates Ship object and raise Errors if coordinates are wrong."""
    ship = Ship({(1, 1): Cell(x=1, y=1)})
    # Check if Ship created properly.
    assert ship.ship == {(1, 1): Cell(x=1, y=1)}
    # Check if Ship raises NotParallelShipError if it is not vertical | or horizontal - line.
    with pytest.raises(NotParallelShipError):
        Ship({(1, 2): Cell(x=1, y=2), (2, 3): Cell(x=2, y=3)})
    # Check if Ship raises WrongShipSizeError if number coordinates is not match with length between end's coordinates.
    with pytest.raises(WrongShipSizeError):
        Ship({(1, 1): Cell(x=1, y=1), (1, 10): Cell(x=1, y=10)})
    # Check if Ship raises WrongShipCoordinateError if the theoretical coordinates (calculated based on the first
    # and the last coordinate don't match with giving coordinates.
    with pytest.raises(WrongShipCoordinateError):
        Ship({(1, 1): Cell(x=1, y=1), (4, 4): Cell(x=4, y=4), (1, 3): Cell(x=1, y=3)})
