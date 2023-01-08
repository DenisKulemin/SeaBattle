"""Module with unit tests for cell object."""
from seabattle.game_objects.cell import Cell
from seabattle.helpers.constants import SignObjects


def test_cell_creation():
    """Method tests correct creates Cell object."""
    # Check if Cell creates with default sign.
    cell = Cell(x=1, y=1)
    assert cell.sign == SignObjects.empty_sign.sign


def test_cell_representation():
    """Method tests correct Cell object representation."""
    cell = Cell(x=1, y=1)
    assert repr(cell) == cell.sign
