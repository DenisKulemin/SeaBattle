"""Module with integration tests for the whole game."""
import pytest

from seabattle.game import Game
from seabattle.game_errors.game_errors import StartedGameError, NotStartedGameError
from seabattle.helpers.constants import SignObjects


def test_game_is_started(game):
    """
    Method tests that game switch is_game_started value from False to True correctly.
    Args:
        game: Game object with ships.
    """

    assert not game.is_game_started

    # Start game.
    game.start_game()

    assert game.is_game_started


def test_game_is_not_started():
    """
    Method tests that game couldn't switch is_game_started value from False to True if not all ships added.
    """
    game = Game()
    assert not game.is_game_started

    with pytest.raises(NotStartedGameError):
        # Start game.
        game.start_game()


def test_game_is_not_finished(game):
    """
    Method checks if game is not finished right after start.
    Args:
        game: Game object with ships.
    """
    game.start_game()
    # Check if game is not over right after start.
    assert not game.player.is_game_over


def test_game_is_over(game):
    """
    Method checks if game works correctly, and doesn't raise any errors during game.
    Args:
        game: Game object with ships.
    """
    game.start_game()

    while game.player.coordinates_for_shooting and game.enemy.coordinates_for_shooting:
        if game.is_player_move:
            game.player_shoot(game.player.choose_shooting_coordinate())
        else:
            game.enemy_shoot()

    # Check if game is over after all ships for one player are destroyed.
    assert (game.player.is_game_over or game.enemy.is_game_over)


def test_game_is_not_shooting_before_start(game):
    """
    Method checks if game couldn't shoot if game is not started.
    Args:
        game: Game object with ships.
    """
    game.is_player_move = True
    coordinate = (1, 2)
    # Test player shoot.
    with pytest.raises(NotStartedGameError):
        game.player_shoot(coordinate)

    # Test enemy shoot.
    with pytest.raises(NotStartedGameError):
        game.enemy_shoot()


def test_game_is_shooting_after_start(game):
    """
    Method checks if game is shooting after game is started.
    Args:
        game: Game object with ships.
    """
    game.start_game()
    game.is_player_move = True
    coordinate = (1, 2)
    game.player_shoot(coordinate)
    assert game.player.enemy_battlefield.battlefield[coordinate].sign is not SignObjects.empty_sign.sign


def test_game_is_adding_ship_before_game_start():
    """
    Method checks if game is adding a ship before game is started.
    """
    game = Game()
    assert game.player_set_ship([(4, 4)])


def test_game_is_not_adding_ship_after_game_start(game):
    """
    Method checks if game couldn't add the ship after game is started.
    Args:
        game: Game object with ships.
    """
    game.start_game()
    with pytest.raises(StartedGameError):
        _ = game.player_set_ship([(4, 4)])


def test_game_cannot_start_after_start(game):
    """
    Method checks if game raises an error if we try to start game after it already started.
    Args:
        game: Game object with ships.
    """
    game.start_game()
    with pytest.raises(StartedGameError):
        game.start_game()
