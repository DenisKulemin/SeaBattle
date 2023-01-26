"""Module contains general data for pytest (fixtures, etc.)."""
from copy import deepcopy

import pytest

from seabattle.game import Game
from seabattle.game_objects.battlefield import BattleField
from seabattle.game_objects.player import Player
from seabattle.helpers.constants import SHIPS_COORDINATES
from seabattle.listener.listener import app
from seabattle.listener.validators import GAME_STORAGE


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
    yield battlefield


@pytest.fixture(name="player")
def player_fixture():
    """Method returns player object."""
    yield Player(player_name="Mike", enemy_name="Sailor")


@pytest.fixture(name="application")
def app_fixture():
    """Method returns flask application object and dictionary with game information for testing."""
    test_info = {}

    game = Game()
    GAME_STORAGE.update({game.id: game})
    test_info.update({"just_created": {"gameId": str(game.id), "playerId": str(game.player.id)}})

    game = Game()
    for coordinates in SHIPS_COORDINATES:
        game.player_set_ship(coordinates)
    GAME_STORAGE.update({game.id: game})
    test_info.update({"ships_added": {"gameId": str(game.id), "playerId": str(game.player.id)}})

    game = Game()
    for coordinates in SHIPS_COORDINATES:
        game.player_set_ship(coordinates)
    game.start_game()
    game.is_player_move = True
    GAME_STORAGE.update({game.id: game})
    test_info.update({"game_started_player": {"gameId": str(game.id), "playerId": str(game.player.id)}})

    game = Game()
    for coordinates in SHIPS_COORDINATES:
        game.player_set_ship(coordinates)
    game.start_game()
    game.is_player_move = False
    GAME_STORAGE.update({game.id: game})
    test_info.update({"game_started_enemy": {"gameId": str(game.id), "playerId": str(game.player.id)}})

    game = Game()
    for coordinates in SHIPS_COORDINATES:
        game.player_set_ship(coordinates)
    game.start_game()
    game.is_player_move = True
    game.player_shoot((10, 1))
    game.is_player_move = True
    GAME_STORAGE.update({game.id: game})
    test_info.update({"game_started_player_after_shoot": {"gameId": str(game.id), "playerId": str(game.player.id)}})

    game = Game()
    game.is_game_over = True
    GAME_STORAGE.update({game.id: game})
    test_info.update({"game_is_over": {"gameId": str(game.id), "playerId": str(game.player.id)}})

    yield app, test_info

    # Clear GAME_STORAGE after test.
    for game_id in deepcopy(GAME_STORAGE):
        GAME_STORAGE.pop(game_id)


@pytest.fixture(name="client")
def client_fixture(application):
    """Method returns flask client object."""
    yield application[0].test_client()
