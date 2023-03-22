"""Module contains integration api tests."""
import uuid
from copy import deepcopy
from unittest.mock import patch

import pytest

from seabattle.game_objects.cell import Cell
from seabattle.helpers.constants import StatusCode, SignObjects
from seabattle.listener.validators import GAME_STORAGE, validate_create_game_info_response
from tests.helpers.test_cases import START_GAME_BAD_REQUEST, ADD_SHIP_BAD_REQUEST, PLAYER_SHOOT_BAD_REQUEST

BASE_URL = "https://localhost:8080"


def test_health_check(client):
    """
    Method tests correct work /health-check endpoint.
    Args:
        client: Fixture with flash client to make a request.
    """
    response = client.post(f"{BASE_URL}/health-check")
    assert response.text == "Hi, I'm OK!"
    assert response.status_code == StatusCode.OK.value


def test_create_new_game(client):
    """
    Method tests correct work /health-check endpoint.
    Args:
        client: Fixture with flash client to make a request.
    """
    response = client.post(f"{BASE_URL}/new-game")
    assert response.json == validate_create_game_info_response(
        GAME_STORAGE[uuid.UUID(response.json["gameId"])].return_game_state()
    )
    assert response.status_code == StatusCode.OK.value


def test_add_new_ship_works_correct(application, client):
    """
    Method tests correct work /new-ship endpoint.
    Args:
        application: Fixture with tuple, that contains application object and game information for api tests.
        client: Fixture with flash client to make a request.
    """
    json_request = application[1]["just_created"]
    json_request.update({"coordinates": [[1, 2]]})
    game_state = GAME_STORAGE[uuid.UUID(json_request["gameId"])].return_game_state()
    game_state["player_fleet"]["patrol_boat"] += 1
    check_game_state_result = validate_create_game_info_response({**game_state})

    response = client.post(f"{BASE_URL}/new-ship", json=json_request)

    assert response.json == {
        "gameId": json_request["gameId"],
        "playerId": json_request["playerId"],
        "playerFleet": check_game_state_result["playerFleet"],
        "playerShipCells": [{"x": 1, "y": 2, "sign": SignObjects.ship_sign.sign}],
    }
    assert response.status_code == StatusCode.OK.value


@pytest.mark.parametrize(("wrong_request", "validation_error_dict"), ADD_SHIP_BAD_REQUEST)
def test_add_new_ship_validation_failed(client, wrong_request, validation_error_dict):
    """
    Method tests correct work /new-ship endpoint.
    Args:
        client: Fixture with flash client to make a request.
        wrong_request: Dictionary that contains one wrong value, to produce validation error.
        validation_error_dict: Dictionary with validation error information.
    """
    response = client.post(f"{BASE_URL}/new-ship", json=wrong_request)

    assert response.json == validation_error_dict
    assert response.status_code == StatusCode.BAD_REQUEST.value


@pytest.mark.parametrize(
    ("game_type", "coordinates", "error", "error_hint"), [
        ("game_started_player", [[1, 2]], "StartedGameError", "Cannot set a ship after game started"),
        ("ships_added", [[1, 2]], "BlockedAreaError", "Area with coordinates: 1b is not empty."),
        ("ships_added", [[10, 5]], "BlockedAreaAroundError", "Area around coordinates: 10e is not empty"),
        ("ships_added", [[3, 9]], "ExtraShipInFleetError", "Couldn't add ship with such size: 1"),
        ("just_created", [[3, 9], [2, 10]], "NotParallelShipError",
         "Ship with coordinates 2j, 3i is not parallel x- or y-axis."),
        ("just_created", [[3, 8], [3, 10]], "WrongShipCoordinateError",
         "Ship with coordinates 3h, 3j doesn't match theory coordinates 3h, 3i, based on coordinates quantity - 2."),
        ("just_created", [[3, 8], [4, 9], [3, 10]], "NotParallelShipError",
         "Ship with coordinates 3h, 3j, 4i is not parallel x- or y-axis."),
    ]
)
def test_add_new_ship_cannot_work_correctly(application, client, game_type, coordinates, error, error_hint):

    # pylint: disable=too-many-arguments

    """
    Method tests that /game-start endpoint return correct info if game produce an error during adding new ship.
    Args:
        application: Fixture with tuple, that contains application object and game information for api tests.
        client: Fixture with flash client to make a request.
        game_type: Key for getting correct game stage for testing.
        coordinates: List of coordinates for ship.
        error: Error name that would be produced.
        error_hint: Error hint that would be produced.
    """
    json_request = application[1][game_type]
    json_request.update({"coordinates": coordinates})

    response = client.post(f"{BASE_URL}/new-ship", json=json_request)

    assert response.json == {
        "message": "Internal Server Error.",
        "errorCode": error,
        "statusCode": 500,
        "hint": error_hint
    }
    assert response.status_code == StatusCode.APPLICATION_ERROR.value


def test_start_game_works_correct(application, client):
    """
    Method tests correct work /game-start endpoint.
    Args:
        application: Fixture with tuple, that contains application object and game information for api tests.
        client: Fixture with flash client to make a request.
    """
    json_request = application[1]["ships_added"]
    game_state = GAME_STORAGE[uuid.UUID(json_request["gameId"])].return_game_state()
    check_game_state_result = validate_create_game_info_response({**game_state})

    response = client.post(f"{BASE_URL}/game-start", json=json_request)
    check_game_state_result["isPlayerMove"] = response.json["isPlayerMove"]

    assert response.json == check_game_state_result
    assert response.status_code == StatusCode.OK.value


@pytest.mark.parametrize(("wrong_request", "validation_error_dict"), START_GAME_BAD_REQUEST)
def test_start_game_validation_failed(client, wrong_request, validation_error_dict):
    """
    Method tests that /game-start endpoint produce ValidationError correctly.
    Args:
        client: Fixture with flash client to make a request.
        wrong_request: Dictionary that contains one wrong value, to produce validation error.
        validation_error_dict: Dictionary with validation error information.
    """
    response = client.post(f"{BASE_URL}/game-start", json=wrong_request)

    assert response.json == validation_error_dict
    assert response.status_code == StatusCode.VALIDATION_FAILED.value


def test_start_game_game_cannot_be_started(application, client):
    """
    Method tests that /game-start endpoint return correct info if game cannot be started yet.
    Args:
        application: Fixture with tuple, that contains application object and game information for api tests.
        client: Fixture with flash client to make a request.
    """
    json_request = application[1]["just_created"]

    response = client.post(f"{BASE_URL}/game-start", json=json_request)

    assert response.json == {
        "message": "Internal Server Error.",
        "errorCode": "NotStartedGameError",
        "statusCode": 500,
        "hint": "There are not all ships added. Cannot start a game."
    }
    assert response.status_code == StatusCode.APPLICATION_ERROR.value


def test_start_game_game_is_already_started(application, client):
    """
    Method tests correct returning for /game-start endpoint.
    Args:
        application: Fixture with tuple, that contains application object and game information for api tests.
        client: Fixture with flash client to make a request.
    """
    json_request = application[1]["game_started_player"]

    response = client.post(f"{BASE_URL}/game-start", json=json_request)

    assert response.json == {
        "message": "Internal Server Error.",
        "errorCode": "StartedGameError",
        "statusCode": 500,
        "hint": f"Game with id {json_request['gameId']} is already started."
    }
    assert response.status_code == StatusCode.APPLICATION_ERROR.value


@patch("seabattle.game_objects.player.Player.enemy_shooting")
def test_player_shoot_works_correct(mock_shooting_result, application, client):
    """
    Method tests correct work /player-shoot endpoint.
    Args:
        application: Fixture with tuple, that contains application object and game information for api tests.
        client: Fixture with flash client to make a request.
    """
    json_request = application[1]["game_started_player"]
    game_state_after_shooting = GAME_STORAGE[uuid.UUID(json_request['gameId'])].return_game_state()

    # Not exclude killed ship as we use mock.
    for x, y, sign in [
        [1, 2, SignObjects.miss_sign.sign],
        [2, 1, SignObjects.miss_sign.sign],
        [1, 1, SignObjects.hit_sign.sign],
        [2, 2, SignObjects.miss_sign.sign],
    ]:
        for cell_info in game_state_after_shooting["enemy_battle_field_cells"]:
            if cell_info["x"] == str(x) and cell_info["y"] == str(y):
                cell_info["sign"] = sign
                break
    check_result_after_shooting = validate_create_game_info_response({**game_state_after_shooting})

    # Test if hit and kill the ship.
    mock_shooting_result.return_value = (
        {
            (1, 2): Cell(1, 2, SignObjects.miss_sign.sign),
            (2, 1): Cell(2, 1, SignObjects.miss_sign.sign),
            (1, 1): Cell(1, 1, SignObjects.hit_sign.sign),
            (2, 2): Cell(2, 2, SignObjects.miss_sign.sign),
        },
        True
    )
    response = client.post(f"{BASE_URL}/player-shoot", json={**json_request, "coordinate": [1, 1]})

    assert response.json == check_result_after_shooting

    # Test if hit but not kill the ship.

    # Not exclude killed ship as we use mock.
    for x, y, sign in [
        [1, 1, SignObjects.hit_sign.sign],
        [2, 2, SignObjects.miss_sign.sign],
    ]:
        for cell_info in game_state_after_shooting["enemy_battle_field_cells"]:
            if cell_info["x"] == str(x) and cell_info["y"] == str(y):
                cell_info["sign"] = sign
                break
    check_result_after_shooting = validate_create_game_info_response({**game_state_after_shooting})

    mock_shooting_result.return_value = (
        {
            (1, 1): Cell(1, 1, SignObjects.hit_sign.sign),
            (2, 2): Cell(2, 2, SignObjects.miss_sign.sign),
        },
        False
    )
    response = client.post(f"{BASE_URL}/player-shoot", json={**json_request, "coordinate": [1, 1]})

    assert response.json == check_result_after_shooting

    # Test when miss shooting.

    # Not exclude killed ship as we use mock.
    for x, y, sign in [
        [1, 1, SignObjects.miss_sign.sign],
    ]:
        for cell_info in game_state_after_shooting["enemy_battle_field_cells"]:
            if cell_info["x"] == str(x) and cell_info["y"] == str(y):
                cell_info["sign"] = sign
                break
    game_state_after_shooting["is_player_move"] = not game_state_after_shooting["is_player_move"]
    check_result_after_shooting = validate_create_game_info_response({**game_state_after_shooting})

    mock_shooting_result.return_value = (
        {
            (1, 1): Cell(1, 1, SignObjects.miss_sign.sign),
        },
        False
    )
    response = client.post(f"{BASE_URL}/player-shoot", json={**json_request, "coordinate": [1, 1]})

    assert response.json == check_result_after_shooting
    assert response.status_code == StatusCode.OK.value


@pytest.mark.parametrize(("wrong_request", "validation_error_dict"), PLAYER_SHOOT_BAD_REQUEST)
def test_player_shoot_validation_failed(client, wrong_request, validation_error_dict):
    """
    Method tests that /player-shoot endpoint produce ValidationError correctly.
    Args:
        client: Fixture with flash client to make a request.
        wrong_request: Dictionary that contains one wrong value, to produce validation error.
        validation_error_dict: Dictionary with validation error information.
    """
    response = client.post(f"{BASE_URL}/player-shoot", json=wrong_request)

    assert response.json == validation_error_dict
    assert response.status_code == StatusCode.VALIDATION_FAILED.value


@pytest.mark.parametrize(
    ("game_type", "coordinate", "error", "error_hint"), [
        ("just_created", [1, 2], "NotStartedGameError", "Game is not started. Cannot shooting."),
        ("game_started_enemy", [1, 2], "NotYourTurnError", "Right now is not your turn for shooting."),
        ("game_started_player_after_shoot", [10, 1], "ShotCellEarlierError",
         "Cell with coordinate 10a was shot already.")
    ]
)
def test_player_shoot_cannot_work_correctly(application, client, game_type, coordinate, error, error_hint):

    # pylint: disable=too-many-arguments

    """
    Method tests that /player-shoot endpoint return correct info if game produce an error during adding new ship.
    Args:
        application: Fixture with tuple, that contains application object and game information for api tests.
        client: Fixture with flash client to make a request.
        game_type: Key for getting correct game stage for testing.
        coordinate: Coordinate for shooting.
        error: Error name that would be produced.
        error_hint: Error hint that would be produced.
    """
    json_request = application[1][game_type]

    json_request.update({"coordinate": coordinate})
    response = client.post(f"{BASE_URL}/player-shoot", json=json_request)

    assert response.json == {
        "message": "Internal Server Error.",
        "errorCode": error,
        "statusCode": 500,
        "hint": error_hint
    }
    assert response.status_code == StatusCode.APPLICATION_ERROR.value


@patch("seabattle.game_objects.bot.EasyBot.choose_shooting_coordinate")
def test_enemy_shoot_works_correct(mocking_coordinate, application, client):
    """
    Method tests correct work /enemy-shoot endpoint.
    Args:
        application: Fixture with tuple, that contains application object and game information for api tests.
        client: Fixture with flash client to make a request.
    """
    json_request = application[1]["game_started_enemy"]
    game_state_after_shooting = deepcopy(GAME_STORAGE[uuid.UUID(json_request['gameId'])].return_game_state())
    game_state_after_shooting["player_fleet"]["patrol_boat"] -= 1
    for x, y, sign in zip(
            [6, 7, 6, 5, 7, 5],
            [2, 1, 1, 1, 2, 2],
            [SignObjects.miss_sign.sign, SignObjects.miss_sign.sign,
             SignObjects.hit_sign.sign, SignObjects.miss_sign.sign,
             SignObjects.miss_sign.sign, SignObjects.miss_sign.sign]
    ):
        for cell_info in game_state_after_shooting["player_battle_field_cells"]:
            if cell_info["x"] == str(x) and cell_info["y"] == str(y):
                cell_info["sign"] = sign
                break
    check_result_after_shooting = validate_create_game_info_response({**game_state_after_shooting})

    # Hit and kill shoot.
    mocking_coordinate.return_value = (6, 1)

    response = client.post(f"{BASE_URL}/enemy-shoot", json={**json_request})

    assert response.json == check_result_after_shooting
    assert response.status_code == StatusCode.OK.value

    # Hit but not kill shoot.
    mocking_coordinate.return_value = (8, 8)
    game_state_after_shooting = deepcopy(GAME_STORAGE[uuid.UUID(json_request['gameId'])].return_game_state())
    for x, y, sign in zip(
            [8, 7, 9, 7, 9],
            [8, 7, 9, 9, 7],
            [SignObjects.hit_sign.sign, SignObjects.miss_sign.sign,
             SignObjects.miss_sign.sign, SignObjects.miss_sign.sign,
             SignObjects.miss_sign.sign]
    ):
        for cell_info in game_state_after_shooting["player_battle_field_cells"]:
            if cell_info["x"] == str(x) and cell_info["y"] == str(y):
                cell_info["sign"] = sign
                break
    check_result_after_shooting = validate_create_game_info_response({**game_state_after_shooting})

    response = client.post(f"{BASE_URL}/enemy-shoot", json={**json_request})

    assert response.json == check_result_after_shooting
    assert response.status_code == StatusCode.OK.value

    # Kill the ship to move to the next part of test.
    mocking_coordinate.return_value = (8, 9)
    _ = client.post(f"{BASE_URL}/enemy-shoot", json={**json_request})

    # Miss shoot.
    mocking_coordinate.return_value = (1, 1)
    game_state_after_shooting = deepcopy(GAME_STORAGE[uuid.UUID(json_request['gameId'])].return_game_state())
    for cell_info in game_state_after_shooting["player_battle_field_cells"]:
        if cell_info["x"] == '1' and cell_info["y"] == '1':
            cell_info["sign"] = SignObjects.miss_sign.sign
            break
    game_state_after_shooting["is_player_move"] = not game_state_after_shooting["is_player_move"]
    check_result_after_shooting = validate_create_game_info_response({**game_state_after_shooting})

    response = client.post(f"{BASE_URL}/enemy-shoot", json={**json_request})

    assert response.json == check_result_after_shooting
    assert response.status_code == StatusCode.OK.value


@pytest.mark.parametrize(("wrong_request", "validation_error_dict"), START_GAME_BAD_REQUEST)
def test_enemy_shoot_validation_failed(client, wrong_request, validation_error_dict):
    """
    Method tests that /enemy-shoot endpoint produce ValidationError correctly.
    Args:
        client: Fixture with flash client to make a request.
        wrong_request: Dictionary that contains one wrong value, to produce validation error.
        validation_error_dict: Dictionary with validation error information.
    """
    response = client.post(f"{BASE_URL}/enemy-shoot", json=wrong_request)

    assert response.json == validation_error_dict
    assert response.status_code == StatusCode.VALIDATION_FAILED.value


@pytest.mark.parametrize(
    ("game_type", "error", "error_hint"), [
        ("just_created", "NotStartedGameError", "Game is not started. Cannot shooting."),
        ("game_started_player", "NotYourTurnError", "Right now is not your turn for shooting.")
    ]
)
def test_enemy_shoot_cannot_work_correctly(application, client, game_type, error, error_hint):
    """
    Method tests that /enemy-shoot endpoint return correct info if game produce an error during adding new ship.
    Args:
        application: Fixture with tuple, that contains application object and game information for api tests.
        client: Fixture with flash client to make a request.
        game_type: Key for getting correct game stage for testing.
        error: Error name that would be produced.
        error_hint: Error hint that would be produced.
    """
    json_request = application[1][game_type]

    response = client.post(f"{BASE_URL}/enemy-shoot", json=json_request)

    assert response.json == {
        "message": "Internal Server Error.",
        "errorCode": error,
        "statusCode": 500,
        "hint": error_hint
    }
    assert response.status_code == StatusCode.APPLICATION_ERROR.value


def test_exit_works_correct(application, client):
    """
    Method tests that /exit endpoint works correctly.
    Args:
        application: Fixture with tuple, that contains application object and game information for api tests.
        client: Fixture with flash client to make a request.
    """
    json_request = application[1]["game_started_player_after_shoot"]

    response = client.post(f"{BASE_URL}/exit", json=json_request)

    assert response.json == {}
    assert response.status_code == StatusCode.OK.value


@pytest.mark.parametrize(("wrong_request", "validation_error_dict"), START_GAME_BAD_REQUEST)
def test_exit_validation_failed(client, wrong_request, validation_error_dict):
    """
    Method tests that /exit endpoint produce ValidationError correctly.
    Args:
        client: Fixture with flash client to make a request.
        wrong_request: Dictionary that contains one wrong value, to produce validation error.
        validation_error_dict: Dictionary with validation error information.
    """
    response = client.post(f"{BASE_URL}/exit", json=wrong_request)

    assert response.json == validation_error_dict
    assert response.status_code == StatusCode.VALIDATION_FAILED.value


def test_validate_game_and_player_validation_failed(application, client):
    """
    Method tests that validate_game_and_player produce Error correctly.
    Args:
        application: Fixture with tuple, that contains application object and game information for api tests.
        client: Fixture with flash client to make a request.
    """
    json_request = application[1]["just_created"]
    game_id = uuid.uuid4()
    response = client.post(f"{BASE_URL}/game-start", json={**json_request, "gameId": game_id})

    assert response.json == {
        "message": "Internal Server Error.",
        "errorCode": "NoGameApiError",
        "statusCode": 500,
        "hint": f"No game with id: {game_id}"
    }
    assert response.status_code == StatusCode.APPLICATION_ERROR.value

    player_id = uuid.uuid4()
    response = client.post(f"{BASE_URL}/game-start", json={**json_request, "playerId": player_id})

    assert response.json == {
        "message": "Internal Server Error.",
        "errorCode": "NoGamePlayerApiError",
        "statusCode": 500,
        "hint": f"Game with id {json_request['gameId']} doesn't have player with id {player_id}"
    }
    assert response.status_code == StatusCode.APPLICATION_ERROR.value

    json_request = application[1]["game_is_over"]

    response = client.post(f"{BASE_URL}/game-start", json=json_request)

    assert response.json == {
        "message": "Internal Server Error.",
        "errorCode": "GameOverError",
        "statusCode": 500,
        "hint": f"Game with id {json_request['gameId']} is already over."
    }
    assert response.status_code == StatusCode.APPLICATION_ERROR.value


def test_wrong_endpoint(client):
    """
    Method tests that wrong endpoint correctly processed by error handler.
    Args:
        client: Fixture with flash client to make a request.
    """
    response = client.post(f"{BASE_URL}/wrong-endpoing")

    assert response.json == {
        "message": "The requested URL was not found on the server. "
                   "If you entered the URL manually please check your spelling and try again.",
        "statusCode": 404,
        "hint": ""
    }
    assert response.status_code == StatusCode.ENTITY_NOT_FOUND.value


def test_api_swagger_endpoint(client):
    """
    Method tests availability of swagger endpoint.
    Args:
        client: Fixture with flash client to make a request.
    """
    response = client.get(f"{BASE_URL}/swagger/")
    assert response.status_code == StatusCode.OK.value


def test_raw_api_endpoint(client):
    """
    Method tests availability of raw apispec documentation endpoint.
    Args:
        client: Fixture with flash client to make a request.
    """
    response = client.get(f"{BASE_URL}/apidocs")
    assert response.status_code == StatusCode.OK.value
