"""Module contains validation methods for input and output data."""
from typing import Dict
from uuid import UUID

from seabattle.game import Game
from seabattle.game_errors.api_errors import NoGameApiError, NoGamePlayerApiError
from seabattle.game_errors.game_errors import GameOverError
from seabattle.listener.validation_schemas import (
    CreateGameInfoOutputSchema,
    GameStartInputSchema,
    CreateNewShipInputSchema,
    CreateNewShipOutputSchema,
    PlayerShootInputSchema,
    EnemyShootInputSchema,
)

GAME_STORAGE: Dict[UUID, Game] = {}


def validate_create_game_info_response(data: dict) -> dict:
    """
    Method validates response for several endpoints that return full game information.
    Args:
        data: Response from endpoint.

    Returns:
        dict: Validated response data from endpoint.
    """
    validator = CreateGameInfoOutputSchema()
    # Validate response and dump it (make camel case keys).
    return validator.dump(validator.load(data))


def validate_start_game_request(data: dict) -> dict:
    """
    Method validates request for '/game-start' endpoint.
    Args:
        data: Request to endpoint.

    Returns:
        dict: Validated request data to endpoint.
    """
    validator = GameStartInputSchema()
    # Validate request and load it (make snake case keys).
    return validator.load(data)


def validate_create_new_ship_request(data: dict) -> dict:
    """
    Method validates request for '/new-ship' endpoint.
    Args:
        data: Request to endpoint.

    Returns:
        dict: Validated request data to endpoint.
    """
    validator = CreateNewShipInputSchema()
    # Validate request and load it (make snake case keys).
    return validator.load(data)


def validate_create_new_ship_response(data: dict) -> dict:
    """
    Method validates response for '/new-ship' endpoint.
    Args:
        data: Response from endpoint.

    Returns:
        dict: Validated response data from endpoint.
    """
    validator = CreateNewShipOutputSchema()
    # Validate response and dump it (make camel case keys).
    return validator.dump(validator.load(data))


def validate_player_shoot_request(data: dict) -> dict:
    """
    Method validates request for '/player-shoot' endpoint.
    Args:
        data: Request to endpoint.

    Returns:
        dict: Validated request data to endpoint.
    """
    validator = PlayerShootInputSchema()
    # Validate request and load it (make snake case keys).
    return validator.load(data)


def validate_enemy_shoot_request(data: dict) -> dict:
    """
    Method validates request for '/enemy-shoot' endpoint.
    Args:
        data: Request to endpoint.

    Returns:
        dict: Validated request data to endpoint.
    """
    validator = EnemyShootInputSchema()
    # Validate request and load it (make snake case keys).
    return validator.load(data)


def validate_game_and_player(player_data: dict, exit_mark: bool = False) -> Game:
    """
    Method validates that request contains game id and player id, that contains real game and player in game storage.
    Args:
        player_data: Request to endpoint.
        exit_mark: Boolean mark if we get the game for exit. It allows to ignore game.is_game_over check.

    Returns:
        Game: game object.
    """

    game_id = player_data["game_id"]
    game = GAME_STORAGE.get(game_id)
    if game is None:
        raise NoGameApiError(f"No game with id: {game_id}")

    player_id = player_data["player_id"]
    if player_id != game.player.id:
        raise NoGamePlayerApiError(f"Game with id {game_id} doesn't have player with id {player_id}")

    if game.is_game_over and not exit_mark:
        raise GameOverError(f"Game with id {game_id} is already over.")

    return game
