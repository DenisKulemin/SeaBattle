"""Module with unit tests for battlefield."""
from unittest.mock import patch
import pytest

from seabattle.game_errors.battlefield_errors import BlockedAreaError, BlockedAreaAroundError, ShotCellEarlierError, \
    AreaOutsideBattleFieldError, CellNotExistError
from seabattle.game_objects.battlefield import BattleField
from seabattle.game_objects.ship import Ship
from seabattle.helpers.constants import SignObjects

BOARD_GAME = BattleField(name="Mike")
BOARD_GAME.set_ship_coordinates([(1, 2), (2, 2)])
BOARD_GAME.set_ship_coordinates([(6, 6)])
BOARD_GAME.set_ship_coordinates([(9, 6), (9, 7), (9, 8)])


@patch("seabattle.game_objects.battlefield.Ship")
def test_set_ship_coordinate(mock_ship):
    """
    Method tests correct work of set_ship_coordinates method.
    Args:
        mock_ship: Mock object for Ship.
    """
    board_game = BattleField(name="Mike")
    # Mock correct Ship object, to avoid Ship specific errors. This mock also create ship in board_game.
    mock_ship.return_value = Ship({(1, 1): board_game.battlefield.get((1, 1)),
                                   (1, 2): board_game.battlefield.get((1, 2))})
    # Check if battlefield is not empty.
    assert board_game != BattleField(name="Mike")
    # Check if method raises AreaOutsideBoardError if used coordinates is outside the battlefield.
    with pytest.raises(AreaOutsideBattleFieldError):
        board_game.set_ship_coordinates([(50, -1)])
    # Check if method couldn't set a new ship on area with other ship's part.
    with pytest.raises(BlockedAreaError):
        board_game.set_ship_coordinates([(1, 1), (1, 2)])
    # Check if method couldn't set a new ship in one cell perimeter around other ship.
    with pytest.raises(BlockedAreaAroundError):
        board_game.set_ship_coordinates([(2, 3), (3, 3)])
    # Check if method raises TypeError if used wrong coordinate format.
    with pytest.raises(TypeError):
        board_game.set_ship_coordinates((3, 3))


@patch("seabattle.game_objects.battlefield.Ship")
def test_shoot(mock_ship):
    """
    Method tests correct work of shoot method.
    Args:
        mock_ship: Mock object for Ship
    """
    board_game = BattleField(name="Mike")
    # Mock correct Ship object, to avoid Ship specific errors. This mock also create ship in board_game.
    mock_ship.return_value = Ship({(1, 1): board_game.battlefield.get((1, 1)),
                                   (1, 2): board_game.battlefield.get((1, 2))})
    # Check if sign after successful shooting is correct.
    board_game.shoot((1, 2))
    assert board_game.battlefield.get((1, 2)).sign == SignObjects.hit_sign.sign
    # Check if sign after miss shooting is correct.
    board_game.shoot((3, 3))
    assert board_game.battlefield.get((3, 3)).sign == SignObjects.miss_sign.sign
    # Check if method raises ShotCellEarlierError if cell was shot earlier.
    with pytest.raises(ShotCellEarlierError):
        board_game.shoot((1, 2))
    # Check if method raises CellNotExistError if cell with coordinates is not exist.
    with pytest.raises(CellNotExistError):
        board_game.shoot((50, 50))


def test_player_battlefield_repr():
    """Method checks if player battlefield printing in console works correct."""

    # pylint: disable=duplicate-code

    board_game = BattleField(name="Mike")
    # Check empty battlefield.
    assert repr(board_game) == \
           "                   \n" \
           "                   \n" \
           "                   \n" \
           "                   \n" \
           "                   \n" \
           "                   \n" \
           "                   \n" \
           "                   \n" \
           "                   \n" \
           "                   "  # Line has 19 signs: 10 - cells signs and 9 - whitespaces between them.

    # Check battlefield with ship mark.
    board_game.battlefield.get((1, 2)).sign = SignObjects.ship_sign.sign
    assert repr(board_game) == \
           "                   \n" \
           "0                  \n" \
           "                   \n" \
           "                   \n" \
           "                   \n" \
           "                   \n" \
           "                   \n" \
           "                   \n" \
           "                   \n" \
           "                   "

    # Check battlefield with miss mark.
    board_game.battlefield.get((5, 5)).sign = SignObjects.miss_sign.sign
    assert repr(board_game) == \
           "                   \n" \
           "0                  \n" \
           "                   \n" \
           "                   \n" \
           "        *          \n" \
           "                   \n" \
           "                   \n" \
           "                   \n" \
           "                   \n" \
           "                   "

    # Check battlefield with hit mark.
    board_game.battlefield.get((1, 2)).sign = SignObjects.hit_sign.sign
    assert repr(board_game) == \
           "                   \n" \
           "X                  \n" \
           "                   \n" \
           "                   \n" \
           "        *          \n" \
           "                   \n" \
           "                   \n" \
           "                   \n" \
           "                   \n" \
           "                   "


def test_enemy_battlefield_repr():
    """Method checks if enemy battlefield printing in console works correct."""

    # pylint: disable=duplicate-code

    board_game = BattleField(name="Sailor", is_visible=False)
    # Check battlefield with ship mark. Player shouldn't see enemy's ships.
    board_game.battlefield.get((1, 2)).sign = SignObjects.ship_sign.sign
    assert repr(board_game) == \
           "                   \n" \
           "                   \n" \
           "                   \n" \
           "                   \n" \
           "                   \n" \
           "                   \n" \
           "                   \n" \
           "                   \n" \
           "                   \n" \
           "                   "
