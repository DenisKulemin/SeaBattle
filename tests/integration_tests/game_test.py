"""Module with integration tests for the whole game."""
from seabattle.game import Game


def test_game():
    """Method checks if game works correctly, and doesn't raise any errors."""
    game = Game()
    # Set ship.
    game.player_set_ship([(1, 2), (2, 2)])
    # Start game.
    game.start_game()

    # Check if game is not over right after start.
    assert not game.player.is_game_over

    game.player_shoot((5, 5))
    game.player_shoot((2, 7))
    game.player_shoot((2, 2))
    game.player_shoot((2, 3))
    game.player_shoot((1, 2))

    # Check if game is over after all ships destroyed.
    assert game.player.is_game_over
