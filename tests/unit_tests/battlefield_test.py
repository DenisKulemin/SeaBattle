"""Module with unit tests for battlefield."""
from unittest.mock import patch
import pytest

from seabattle.game_errors.battlefield_errors import BlockedAreaError, BlockedAreaAroundError, ShotCellEarlierError, \
    AreaOutsideBattleFieldError
from seabattle.game_objects.battlefield import BattleField
from seabattle.game_objects.ship import Ship
from seabattle.helpers.constants import SignObjects

BOARD_GAME = BattleField()
BOARD_GAME.set_ship_coordinate([(1, 2), (2, 2)])
BOARD_GAME.set_ship_coordinate([(6, 6)])
BOARD_GAME.set_ship_coordinate([(9, 6), (9, 7), (9, 8)])


@patch("seabattle.game_objects.battlefield.Ship")
def test_set_ship_coordinate(mock_simple_value):
    """Method tests correct work of set_ship_coordinate method."""
    board_game = BattleField()
    # Mock correct Ship object, to avoid Ship specific errors. This mock also create ship in board_game.
    mock_simple_value.return_value = Ship({(1, 1): board_game.battlefield.get((1, 1)),
                                           (1, 2): board_game.battlefield.get((1, 2))})
    # Check if battlefield is not empty.
    assert board_game != BattleField()
    # Check if method raises AreaOutsideBoardError if used coordinates is outside the battlefield.
    with pytest.raises(AreaOutsideBattleFieldError):
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
    board_game = BattleField()
    board_game.set_ship_coordinate([(1, 2), (2, 2)])
    # Check if sign after successful shooting is correct.
    board_game.shoot((1, 2))
    assert board_game.battlefield.get((1, 2)).sign == SignObjects.hit_sign.sign
    # Check if sign after miss shooting is correct.
    board_game.shoot((3, 3))
    assert board_game.battlefield.get((3, 3)).sign == SignObjects.miss_sign.sign
    # Check if method raises ShotCellEarlierError if cell was shot earlier.
    with pytest.raises(ShotCellEarlierError):
        board_game.shoot((1, 2))
