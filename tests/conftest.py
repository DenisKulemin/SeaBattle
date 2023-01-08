"""Module contains general data for pytest (fixtures, etc.)."""
import pytest

from seabattle.game import Game
from seabattle.game_objects.battlefield import BattleField
from seabattle.helpers.constants import SHIPS_COORDINATES


@pytest.fixture(name="game")
def game_fixture():
    """Method returns game right after starting game."""
    game = Game()
    # Set ship for player and enemy.
    for coordinates in SHIPS_COORDINATES:
        _ = game.player_set_ship(coordinates)
    yield game


@pytest.fixture(name="battlefield")
def battlefield_fixture():
    """Method returns battlefield with one ship."""
    battlefield = BattleField(name="Mike")
    battlefield.set_ship_coordinates([(1, 1), (1, 2)])
    return battlefield
