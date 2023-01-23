"""Module contains flash application for running and interacting with games."""
import os
from flask import Flask, request
from marshmallow import ValidationError
from seabattle.game import Game
from seabattle.helpers.constants import StatusCode
from seabattle.listener import config
from seabattle.listener.api_error_handlers import handle_validation_error, handle_application_error, handle_api_error
from seabattle.listener.validators import GAME_STORAGE, validate_game_and_player, validate_create_new_game_response, \
    validate_start_game_response, validate_start_game_request, validate_create_new_ship_request, \
    validate_create_new_ship_response, validate_player_shoot_request, validate_player_shoot_response, \
    validate_enemy_shoot_request, validate_enemy_shoot_response


app = Flask(__name__)
app.register_error_handler(Exception, handle_application_error)
app.register_error_handler(ValidationError, handle_validation_error)
app.register_error_handler(StatusCode.BAD_REQUEST.value, handle_api_error)
app.register_error_handler(StatusCode.ENTITY_NOT_FOUND.value, handle_api_error)
app.config.from_object(getattr(config, os.environ.get("SEABATTLE_SETTINGS", "DevConfig")))


@app.route("/health-check", methods=["POST"])
def health_check():
    """Method contains health check data."""
    return "Hi, I'm OK!", StatusCode.OK.value


@app.route("/new-game", methods=["POST"])
def create_new_game():
    """Method creates a new game."""
    game = Game()
    GAME_STORAGE.update({game.id: game})
    response = validate_create_new_game_response(
        {"message": "Game created.", "game_id": game.id, "player_id": game.player.id}
    )
    return response, StatusCode.OK.value


@app.route("/new-ship", methods=["POST"])
def add_new_ship():
    """Method creates a new ship for the game."""
    player_data = validate_create_new_ship_request(request.json)
    game = validate_game_and_player(player_data)
    message = game.player_set_ship(player_data["coordinates"])
    response = validate_create_new_ship_response({"message": message, **player_data})
    return response, StatusCode.OK.value


@app.route("/game-start", methods=["POST"])
def start_game():
    """Method starts a game."""
    player_data = validate_start_game_request(request.json)
    game = validate_game_and_player(player_data)
    response = game.start_game()
    response = validate_start_game_response({**response, **player_data})
    return response, StatusCode.OK.value


@app.route("/player-shoot", methods=["POST"])
def player_shoot():
    """Method calls player shooting method."""
    player_data = validate_player_shoot_request(request.json)
    game = validate_game_and_player(player_data)
    result = game.player_shoot(player_data["coordinate"])
    response = validate_player_shoot_response(
        {**result, "game_id": player_data["game_id"], "player_id": player_data["player_id"]}
    )
    return response, StatusCode.OK.value


@app.route("/enemy-shoot", methods=["POST"])
def enemy_shoot():
    """Method calls enemy shooting method."""
    player_data = validate_enemy_shoot_request(request.json)
    game = validate_game_and_player(player_data)
    result = game.enemy_shoot()
    response = validate_enemy_shoot_response({**result, **player_data})
    return response, StatusCode.OK.value


@app.route("/exit", methods=["POST"])
def exit_game():
    """Method deletes the game."""
    # Use the same validation as for start game.
    player_data = validate_start_game_request(request.json)
    game = validate_game_and_player(player_data)
    GAME_STORAGE.pop(game.id)
    response = validate_create_new_game_response(
        {"message": f"Game with id {game.id} is over.", "game_id": game.id, "player_id": game.player.id}
    )
    return response, StatusCode.OK.value


if __name__ == "__main__":
    app.run(
        host=app.config["HOST"],
        port=app.config["PORT"],
        debug=app.config["DEBUG"]
    )
