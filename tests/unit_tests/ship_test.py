"""Module with unit tests for ship object."""
import pytest

from seabattle.game_errors.ship_errors import NotParallelShipError, WrongShipSizeError, WrongShipCoordinateError
from seabattle.game_objects.cell import Cell
from seabattle.game_objects.ship import Ship


def test_ship_created_correctly():
    """Method tests correct creates Ship object and raise Errors if coordinates are wrong."""
    # Check if Ship created properly.
    ship = Ship({(1, 1): Cell(x=1, y=1)})
    assert ship.ship == {(1, 1): Cell(x=1, y=1)}


@pytest.mark.parametrize(
    ("cells", "error"), [
        # Ship raises NotParallelShipError if it is not vertical | or horizontal - line.
        ({(1, 2): Cell(x=1, y=2), (2, 3): Cell(x=2, y=3)}, NotParallelShipError),
        # Ship raises WrongShipSizeError if number coordinates is not match with length between end's coordinates.
        ({(1, 1): Cell(x=1, y=1), (1, 10): Cell(x=1, y=10)}, WrongShipSizeError),
        # Ship raises WrongShipCoordinateError if the theoretical coordinates (calculated based on the first
        # and the last coordinate) don't match with giving coordinates.
        ({(1, 1): Cell(x=1, y=1), (4, 4): Cell(x=4, y=4), (1, 3): Cell(x=1, y=3)}, WrongShipCoordinateError)
    ]
)
def test_ship_raised_error_due_creation(cells, error):
    """
    Method tests that raises Error if something wrong.
    Args:
        cells: Dictionary with coordinates and cells associated with these coordinates.
        error: Error class that should be raised.
    """
    with pytest.raises(error):
        Ship(cells)
