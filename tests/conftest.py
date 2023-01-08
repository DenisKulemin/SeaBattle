"""Module contains general data for pytest (fixtures, etc.)."""
import pytest

from seabattle.game import Game
from seabattle.game_objects.battlefield import BattleField


@pytest.fixture(name="game")
def game_fixture():
    """Method returns game right after starting game."""
    game = Game()
    # Set ship for player and enemy.
    ship_coordinates = (
        [(10, 1), (10, 2), (10, 3), (10, 4)],
        [(10, 6), (10, 7), (10, 8)],
        [(8, 1), (8, 2), (8, 3)],
        [(1, 2), (2, 2)],
        [(8, 5), (8, 6)],
        [(8, 8), (8, 9)],
        [(6, 1)],
        [(6, 3)],
        [(6, 5)],
        [(6, 7)]
    )
    for coordinates in ship_coordinates:
        _ = game.player_set_ship(coordinates)
        game.player.enemy_battlefield.set_ship_coordinates(coordinates)
    yield game


@pytest.fixture(name="battlefield")
def battlefield_fixture():
    """Method returns battlefield with one ship."""
    battlefield = BattleField(name="Mike")
    battlefield.set_ship_coordinates([(1, 1), (1, 2)])
    return battlefield
