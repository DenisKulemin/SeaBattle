"""Module contains flash application for running and interacting with games."""
import json
import os
from flask import Flask, request
from flask_swagger_ui import get_swaggerui_blueprint  # type: ignore
from marshmallow import ValidationError
from seabattle.game import Game
from seabattle.helpers.constants import StatusCode, SWAGGER_URL, API_URL, API_NAME, API_VERSION
from seabattle.helpers.logger import API_LOGGER
from seabattle.listener import config
from seabattle.listener.api_error_handlers import handle_validation_error, handle_application_error, handle_api_error
from seabattle.listener.apispec_generator import get_apispec
from seabattle.listener.validators import (
    GAME_STORAGE,
    validate_game_and_player,
    validate_create_game_info_response,
    validate_start_game_request,
    validate_create_new_ship_request,
    validate_create_new_ship_response,
    validate_player_shoot_request,
    validate_enemy_shoot_request
)

app = Flask(__name__)
app.register_error_handler(Exception, handle_application_error)
app.register_error_handler(ValidationError, handle_validation_error)
app.register_error_handler(StatusCode.BAD_REQUEST.value, handle_api_error)
app.register_error_handler(StatusCode.ENTITY_NOT_FOUND.value, handle_api_error)
app.config.from_object(getattr(config, os.environ.get("SEABATTLE_SETTINGS", "DevConfig")))

swagger_ui_blueprint = get_swaggerui_blueprint(
    base_url=SWAGGER_URL,
    api_url=API_URL,
    config={"app_name": API_NAME}
)


@app.route("/health-check", methods=["POST"])
def health_check():
    """
    ---
    post:
        summary: Method contains health check data.
        responses:
            "200":
                description: OK
        tags:
            - Endpoints
    """
    return "Hi, I'm OK!", StatusCode.OK.value


@app.route("/new-game", methods=["POST"])
def create_new_game():
    """
    ---
    post:
        summary: Method creates a new game.
        responses:
            "200":
                description: OK
                content:
                    application/json:
                        schema: CreateNewGameOutputSchema
        tags:
            - Endpoints
    """
    game = Game()
    API_LOGGER.info(f"Create game with id: {game.id}")
    GAME_STORAGE.update({game.id: game})
    response = validate_create_game_info_response(game.return_game_state())
    return response, StatusCode.OK.value


@app.route("/new-ship", methods=["POST"])
def add_new_ship():
    """
    ---
    post:
        summary: Method creates a new ship for the game.
        requestBody:
            description: API for adding a new ship to game board.
            required: true
            content:
                application/json:
                    schema: CreateNewShipInputSchema
        responses:
            "200":
                description: OK
                content:
                    application/json:
                        schema: CreateNewShipOutputSchema
        tags:
            - Endpoints
    """
    player_data = validate_create_new_ship_request(request.json)
    game = validate_game_and_player(player_data)
    API_LOGGER.info(f"Try to add ship with coordinates: {player_data['coordinates']} to game with id {game.id}.")
    coordinates = player_data.pop("coordinates")
    player_ship_cells = game.player_set_ship(coordinates)
    response = validate_create_new_ship_response({**player_ship_cells, **player_data})
    API_LOGGER.info(f"Successfully added ship with coordinates: {coordinates} to game with id {game.id}.")
    return response, StatusCode.OK.value


@app.route("/game-start", methods=["POST"])
def start_game():
    """
    ---
    post:
        summary: Method starts a game.
        requestBody:
            description: API for starting a new game.
            required: true
            content:
                application/json:
                    schema: GameStartInputSchema
        responses:
            "200":
                description: OK
                content:
                    application/json:
                        schema: GameStartOutputSchema
        tags:
            - Endpoints
    """
    player_data = validate_start_game_request(request.json)
    game = validate_game_and_player(player_data)
    API_LOGGER.info(f"Try to start game with id {game.id}.")
    response = game.start_game()
    response = validate_create_game_info_response({**response})
    API_LOGGER.info(f"Game with id {game.id} is started.")
    return response, StatusCode.OK.value


@app.route("/player-shoot", methods=["POST"])
def player_shoot():
    """
    ---
    post:
        summary: Method calls player shooting method.
        requestBody:
            description: API for player shooting.
            required: true
            content:
                application/json:
                    schema: PlayerShootInputSchema
        responses:
            "200":
                description: OK
                content:
                    application/json:
                        schema: PlayerShootOutputSchema
        tags:
            - Endpoints
    """
    player_data = validate_player_shoot_request(request.json)
    game = validate_game_and_player(player_data)
    API_LOGGER.info(f"Player is trying to shoot on coordinate {player_data['coordinate']} in game with id {game.id}.")
    result = game.player_shoot(player_data["coordinate"])
    response = validate_create_game_info_response({**result})
    API_LOGGER.info(f"Player doesn't have any problems with shooting on coordinate {player_data['coordinate']} "
                    f"in game with id {game.id}.")

    return response, StatusCode.OK.value


@app.route("/enemy-shoot", methods=["POST"])
def enemy_shoot():
    """
    ---
    post:
        summary: Method calls enemy shooting method.
        requestBody:
            description: API for enemy shooting.
            required: true
            content:
                application/json:
                    schema: EnemyShootInputSchema
        responses:
            "200":
                description: OK
                content:
                    application/json:
                        schema: EnemyShootOutputSchema
        tags:
            - Endpoints
    """
    player_data = validate_enemy_shoot_request(request.json)
    game = validate_game_and_player(player_data)
    API_LOGGER.info(f"Enemy is trying to shoot in game with id {game.id}.")
    result = game.enemy_shoot()
    response = validate_create_game_info_response({**result})
    API_LOGGER.info(f"Enemy doesn't have any problems with shooting in game with id {game.id}.")

    return response, StatusCode.OK.value


@app.route("/exit", methods=["POST"])
def exit_game():
    """
    ---
    post:
        summary: Method for exit from the game and delete it.
        requestBody:
            description: API for ending a game.
            required: true
            content:
                application/json:
                    schema: GameStartInputSchema
        responses:
            "200":
                description: OK
                content:
                    application/json:
                        schema: CreateNewGameOutputSchema
        tags:
            - Endpoints
    """
    # Use the same validation as for start game.
    player_data = validate_start_game_request(request.json)
    game = validate_game_and_player(player_data, True)
    API_LOGGER.info(f"Try to exit game with id {game.id}.")
    GAME_STORAGE.pop(game.id)
    API_LOGGER.info(f"Game with id {game.id} is stopped and deleted.")
    return {}, StatusCode.OK.value


@app.route("/apidocs", methods=["GET"])
def create_swagger_spec():
    """Method creates swagger endpoint."""
    API_LOGGER.info("Generate API Specification.")
    return json.dumps(get_apispec(app, API_NAME, API_VERSION).to_dict())


app.register_blueprint(swagger_ui_blueprint)

if __name__ == "__main__":
    app.run(
        host=app.config["HOST"],
        port=app.config["PORT"],
        debug=app.config["DEBUG"]
    )
