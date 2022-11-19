"""Module with unittests for game board."""
import pytest

from seabatlle.game_errors.ship_errors import NotParallelShipError, WrongShipSizeError, WrongShipCoordinateError
from seabatlle.game_objects.ship import Ship
from seabatlle.helpers.constants import GAME_OBJECTS, SHIP_SIGN, SIGN


def test_ship_creation():
    """Method tests correct creates Ship object and raise Errors if coordinates are wrong."""
    ship = Ship([(1, 1)])
    # Check if Ship created properly.
    assert ship.ship_coordinates == [(1, 1)]
    assert ship.ship_size == 1
    assert ship.ship == [GAME_OBJECTS.get(SHIP_SIGN).get(SIGN)]
    # Check if Ship raises NotParallelShipError if it is not vertical | or horizontal - line.
    with pytest.raises(NotParallelShipError):
        Ship([(1, 2), (2, 3)])
    # Check if Ship raises WrongShipSizeError if number coordinates is not match with length between end's coordinates.
    with pytest.raises(WrongShipSizeError):
        Ship([(1, 1), (1, 10)])
    # Check if Ship raises WrongShipCoordinateError if the theoretical coordinates (calculated based on the first
    # and the last coordinate don't match with giving coordinates.
    with pytest.raises(WrongShipCoordinateError):
        Ship([(1, 1), (4, 4),  (1, 3)])
    # Check if Ship raises TypeError if used wrong coordinate format.
    with pytest.raises(TypeError):
        Ship((3, 3))
