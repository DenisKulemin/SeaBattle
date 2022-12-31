"""Module with integration tests for the whole game."""


def test_game_is_not_started(game):
    """
    Method checks if game is not finished right after start.
    Args:
        game: Game object with one ship.
    """
    # Check if game is not over right after start.
    assert not game.player.is_game_over


def test_game_is_over(game):
    """
    Method checks if game works correctly, and doesn't raise any errors during game.
    Args:
        game: Game object with one ship.
    """
    game.player_shoot((5, 5))
    game.player_shoot((2, 7))
    game.player_shoot((2, 2))
    game.player_shoot((2, 3))
    game.player_shoot((1, 2))

    # Check if game is over after all ships destroyed.
    assert game.player.is_game_over
