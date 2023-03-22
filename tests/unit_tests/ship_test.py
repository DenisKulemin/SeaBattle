"""Module with unit tests for ship object."""
import pytest

from seabattle.game_errors.ship_errors import NotParallelShipError, WrongShipCoordinateError
from seabattle.game_objects.cell import Cell
from seabattle.game_objects.ship import Ship
from seabattle.helpers.constants import SignObjects


def test_ship_created_correctly():
    """Method tests correct creates Ship object."""
    ship = Ship({(1, 1): Cell(x=1, y=1)})
    cell = Cell(x=1, y=1, sign=SignObjects.ship_sign.sign)
    cell.ship_id = ship.id
    assert ship.ship == {(1, 1): cell}


@pytest.mark.parametrize(
    ("cells", "error"), [
        # Ship raises NotParallelShipError if it is not vertical | or horizontal - line.
        ({(1, 2): Cell(x=1, y=2), (2, 3): Cell(x=2, y=3)}, NotParallelShipError),
        # Ship raises WrongShipSizeError if number coordinates is not match with length between end's coordinates.
        ({(1, 1): Cell(x=1, y=1), (1, 10): Cell(x=1, y=10)}, WrongShipCoordinateError)
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


@pytest.mark.parametrize(
    ("hit_cells", "result"), [
        ([], True),
        ([(1, 2)], True),
        ([(1, 2), (1, 3)], False)
    ]
)
def test_is_ship_alive(hit_cells, result):
    """
    Method checks if is_ship_alive returns correct information about unsunk ship.
    Args:
        hit_cells: Coordinates for cells that were hit in the ship
        result:
    """
    ship = Ship({(1, 2): Cell(x=1, y=2), (1, 3): Cell(x=1, y=3)})
    for coordinate in hit_cells:
        ship.ship[coordinate].sign = SignObjects.hit_sign.sign

    assert ship.is_ship_alive() == result
