"""Module with integration tests for the whole game."""
from seabattle.game import Game
from seabattle.helpers.constants import SignObjects


def test_game_is_started(game):
    """
    Method tests that game switch game_starts value from False to True correctly.
    Args:
        game: Game object with ships.
    """

    assert not game.game_starts

    # Start game.
    game.start_game()

    assert game.game_starts


def test_game_is_not_started():
    """
    Method tests that game couldn't switch game_starts value from False to True if not all ships added.
    """
    game = Game()
    assert not game.game_starts

    # Start game.
    game.start_game()

    assert not game.game_starts


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
    for coordinate in game.player.player_battlefield.battlefield.keys():
        _ = game.player_shoot(coordinate)

    # Check if game is over after all ships destroyed.
    assert game.player.is_game_over


def test_game_is_not_shooting_before_start(game):
    """
    Method checks if game couldn't shoot if game is not started.
    Args:
        game: Game object with ships.
    """
    assert game.player_shoot((1, 2)) is None


def test_game_is_shooting_after_start(game):
    """
    Method checks if game is shooting after game is started.
    Args:
        game: Game object with ships.
    """
    game.start_game()
    assert game.player_shoot((1, 2)) is SignObjects.hit_sign.sign


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
    assert not game.player_set_ship([(4, 4)])
