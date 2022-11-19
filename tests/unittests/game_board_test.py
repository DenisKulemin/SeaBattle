"""Module with unittests for game board."""
from unittest.mock import patch
import pytest

from seabatlle.game_errors.board_errors import BlockedAreaError, BlockedAreaAroundError, ShotCellEarlierError, \
    AreaOutsideBoardError
from seabatlle.game_objects.board import GameBoard
from seabatlle.game_objects.ship import Ship
from seabatlle.helpers.constants import SignObjects

BOARD_GAME = GameBoard()
BOARD_GAME.set_ship_coordinate([(1, 2), (2, 2)])
BOARD_GAME.set_ship_coordinate([(6, 6)])
BOARD_GAME.set_ship_coordinate([(9, 6), (9, 7), (9, 8)])


@patch("seabatlle.game_objects.board.Ship")
def test_set_ship_coordinate(mock_simple_value):
    """Method tests correct work of set_ship_coordinate method."""
    # Mock correct Ship object, to avoid Ship specific errors.
    mock_simple_value.return_value = Ship([(0, 0)])
    board_game = GameBoard()
    board_game.set_ship_coordinate([(1, 2), (2, 2)])
    # Check if game board is not empty.
    assert board_game != GameBoard()
    # Check if method raises AreaOutsideBoardError if used coordinates is outside the game board.
    with pytest.raises(AreaOutsideBoardError):
        board_game.set_ship_coordinate([(50, -1)])
    # Check if method couldn't set a new ship on area with other ship's part.
    with pytest.raises(BlockedAreaError):
        board_game.set_ship_coordinate([(1, 1), (1, 2)])
    # Check if method couldn't set a new ship in one cell perimeter around other ship.
    with pytest.raises(BlockedAreaAroundError):
        board_game.set_ship_coordinate([(2, 3), (3, 3)])
    # Check if method raises TypeError if used wrong coordinate format.
    with pytest.raises(TypeError):
        board_game.set_ship_coordinate((3, 3))


def test_shoot():
    """Method tests correct work of shoot method."""
    board_game = GameBoard()
    board_game.set_ship_coordinate([(1, 2), (2, 2)])
    # Check if sign after successful shooting is correct.
    board_game.shoot((1, 2))
    assert board_game.board.get((1, 2)).sign == SignObjects.hit_sign.sign
    # Check if sign after miss shooting is correct.
    board_game.shoot((3, 3))
    assert board_game.board.get((3, 3)).sign == SignObjects.miss_sign.sign
    # Check if method raises ShotCellEarlierError if cell was shot earlier.
    with pytest.raises(ShotCellEarlierError):
        board_game.shoot((1, 2))
        board_game.shoot((3, 3))
