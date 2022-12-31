"""Module contains general data for pytest (fixtures, etc.)."""
import pytest

from seabattle.game import Game
from seabattle.game_objects.battlefield import BattleField


@pytest.fixture(name="game")
def game_fixture():
    """Method returns game right after starting game."""
    game = Game()
    # Set ship for player and enemy.
    game.player_set_ship([(1, 2), (2, 2)])
    game.player.enemy_battlefield.set_ship_coordinates([(1, 2), (2, 2)])
    # Start game.
    game.start_game()
    yield game


@pytest.fixture(name="battlefield")
def battlefield_fixture():
    """Method returns battlefield with one ship."""
    battlefield = BattleField(name="Mike")
    battlefield.set_ship_coordinates([(1, 1), (1, 2)])
    return battlefield
