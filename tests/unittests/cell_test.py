"""Module with unittests for cell object."""
from seabatlle.game_objects.cell import Cell
from seabatlle.helpers.constants import SignObjects


def test_cell_creation():
    """Method tests correct creates Cell object."""
    # Check if Cell creates with default sign.
    cell = Cell(x=1, y=1)
    assert cell.sign == SignObjects.empty_sign.sign
