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

    while game.player.coordinates_for_shooting:
        game.player_shoot(game.player.choose_shooting_coordinate())

    while game.enemy.coordinates_for_shooting:
        game.enemy_shoot()

    # Check if game is over after all ships destroyed.
    assert game.player.is_game_over
    assert game.enemy.is_game_over


def test_game_is_not_shooting_before_start(game):
    """
    Method checks if game couldn't shoot if game is not started.
    Args:
        game: Game object with ships.
    """
    coordinate = (1, 2)
    game.player_shoot(coordinate)
    assert game.player.enemy_battlefield.battlefield[coordinate].sign is SignObjects.empty_sign.sign
    enemy_battlefield = repr(game.enemy.player_battlefield)
    game.enemy_shoot()
    assert repr(game.enemy.player_battlefield) == enemy_battlefield


def test_game_is_shooting_after_start(game):
    """
    Method checks if game is shooting after game is started.
    Args:
        game: Game object with ships.
    """
    game.start_game()
    coordinate = (1, 2)
    game.player_shoot(coordinate)
    assert game.player.enemy_battlefield.battlefield[coordinate].sign is not SignObjects.empty_sign.sign


def test_game_is_adding_ship_before_game_start():
    """
    Method checks if game is adding a ship before game is started.
    """
    game = Game()
    assert game.player_set_ship([(4, 4)])


def test_game_cannot_add_ship_before_game_start():
    """
    Method checks if game process correctly if it cannot add a ship before game is started.
    """
    game = Game()
    assert game.player_set_ship([(4, 4), (4, 5), (4, 6), (4, 7), (4, 8)]) is None


def test_game_is_not_adding_ship_after_game_start(game):
    """
    Method checks if game couldn't add the ship after game is started.
    Args:
        game: Game object with ships.
    """
    game.start_game()
    assert not game.player_set_ship([(4, 4)])
