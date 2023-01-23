"""Module contains integration api tests."""
import uuid
from unittest.mock import patch

import pytest

from seabattle.helpers.constants import StatusCode, SignObjects
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
    assert response.json.get("message") == "Game created."
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

    response = client.post(f"{BASE_URL}/new-ship", json=json_request)

    assert response.json == {"message": "Ship with coordinates [(1, 2)] was added.", **json_request}
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
    ("game_type", "coordinates", "error"), [
        ("game_started_player", [[1, 2]], "StartedGameError"),
        ("ships_added", [[1, 2]], "BlockedAreaError"),
        ("ships_added", [[10, 5]], "BlockedAreaAroundError"),
        ("ships_added", [[3, 9]], "ExtraShipInFleetError"),
        ("just_created", [[3, 9], [2, 10]], "ShipError"),
        ("just_created", [[3, 8], [3, 10]], "ShipError"),
        ("just_created", [[3, 8], [4, 9], [3, 10]], "ShipError"),
    ]
)
def test_add_new_ship_cannot_work_correctly(application, client, game_type, coordinates, error):
    """
    Method tests that /game-start endpoint return correct info if game produce an error during adding new ship.
    Args:
        application: Fixture with tuple, that contains application object and game information for api tests.
        client: Fixture with flash client to make a request.
        game_type: Key for getting correct game stage for testing.
        coordinates: List of coordinates for ship.
        error: Error name that would be produced.
    """
    json_request = application[1][game_type]
    json_request.update({"coordinates": coordinates})

    response = client.post(f"{BASE_URL}/new-ship", json=json_request)

    assert response.json == {"message": "Internal Server Error.", "errorCode": error, "statusCode": 500}
    assert response.status_code == StatusCode.APPLICATION_ERROR.value


def test_start_game_works_correct(application, client):
    """
    Method tests correct work /game-start endpoint.
    Args:
        application: Fixture with tuple, that contains application object and game information for api tests.
        client: Fixture with flash client to make a request.
    """
    json_request = application[1]["ships_added"]

    response = client.post(f"{BASE_URL}/game-start", json=json_request)
    is_player_move = response.json["isPlayerMove"]

    assert response.json == {"message": "Game is started.", "isPlayerMove": is_player_move, **json_request}
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

    assert response.json == {"message": "Internal Server Error.", "errorCode": "NotStartedGameError", "statusCode": 500}
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

    assert response.json == {"message": "Internal Server Error.", "errorCode": "StartedGameError", "statusCode": 500}
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
    # Test if hit and kill the ship.
    mock_shooting_result.return_value = (
        {
            (1, 2): SignObjects.miss_sign.sign,
            (2, 1): SignObjects.miss_sign.sign,
            (1, 1): SignObjects.hit_sign.sign,
            (2, 2): SignObjects.miss_sign.sign,
        },
        True
    )
    response = client.post(f"{BASE_URL}/player-shoot", json={**json_request, "coordinate": [1, 1]})

    assert response.json == {
        **json_request,
        "coordinates": [[1, 2], [2, 1], [1, 1], [2, 2]],
        "shootingResults": [SignObjects.miss_sign.sign, SignObjects.miss_sign.sign,
                            SignObjects.hit_sign.sign, SignObjects.miss_sign.sign],
        "isKilled": True,
        "isPlayerMove": True,
        "isGameOver": False
    }

    # Test if hit but not kill the ship.
    mock_shooting_result.return_value = (
        {
            (1, 1): SignObjects.hit_sign.sign,
            (2, 2): SignObjects.miss_sign.sign,
        },
        False
    )
    response = client.post(f"{BASE_URL}/player-shoot", json={**json_request, "coordinate": [1, 1]})

    assert response.json == {
        **json_request,
        "coordinates": [[1, 1], [2, 2]],
        "shootingResults": [SignObjects.hit_sign.sign, SignObjects.miss_sign.sign],
        "isKilled": False,
        "isPlayerMove": True,
        "isGameOver": False
    }

    # Test when miss shooting.
    mock_shooting_result.return_value = (
        {
            (1, 1): SignObjects.miss_sign.sign,
        },
        False
    )
    response = client.post(f"{BASE_URL}/player-shoot", json={**json_request, "coordinate": [1, 1]})

    assert response.json == {
        **json_request,
        "coordinates": [[1, 1]],
        "shootingResults": [SignObjects.miss_sign.sign],
        "isKilled": False,
        "isPlayerMove": False,
        "isGameOver": False
    }

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
    ("game_type", "coordinate", "error"), [
        ("just_created", [1, 2], "NotStartedGameError"),
        ("game_started_enemy", [1, 2], "NotYourTurnError"),
        ("game_started_player_after_shoot", [10, 1], "ShotCellEarlierError")
    ]
)
def test_player_shoot_cannot_work_correctly(application, client, game_type, coordinate, error):
    """
    Method tests that /player-shoot endpoint return correct info if game produce an error during adding new ship.
    Args:
        application: Fixture with tuple, that contains application object and game information for api tests.
        client: Fixture with flash client to make a request.
        game_type: Key for getting correct game stage for testing.
        coordinate: Coordinate for shooting.
        error: Error name that would be produced.
    """
    json_request = application[1][game_type]

    json_request.update({"coordinate": coordinate})
    response = client.post(f"{BASE_URL}/player-shoot", json=json_request)

    assert response.json == {"message": "Internal Server Error.", "errorCode": error, "statusCode": 500}
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

    # Hit and kill shoot.
    mocking_coordinate.return_value = (6, 1)

    response = client.post(f"{BASE_URL}/enemy-shoot", json={**json_request})

    assert response.json == {
        **json_request,
        "coordinates": [[6, 2], [7, 1], [6, 1], [5, 1], [7, 2], [5, 2]],
        "shootingResults": [SignObjects.miss_sign.sign, SignObjects.miss_sign.sign,
                            SignObjects.hit_sign.sign, SignObjects.miss_sign.sign,
                            SignObjects.miss_sign.sign, SignObjects.miss_sign.sign],
        "isKilled": True,
        "isPlayerMove": False,
        "isGameOver": False
    }
    assert response.status_code == StatusCode.OK.value

    # Hit but not kill shoot.
    mocking_coordinate.return_value = (8, 8)

    response = client.post(f"{BASE_URL}/enemy-shoot", json={**json_request})

    assert response.json == {
        **json_request,
        "coordinates": [[8, 8], [7, 7], [9, 9], [7, 9], [9, 7]],
        "shootingResults": [SignObjects.hit_sign.sign, SignObjects.miss_sign.sign,
                            SignObjects.miss_sign.sign, SignObjects.miss_sign.sign,
                            SignObjects.miss_sign.sign],
        "isKilled": False,
        "isPlayerMove": False,
        "isGameOver": False
    }
    assert response.status_code == StatusCode.OK.value

    # Kill the ship to move to the next part of test.
    mocking_coordinate.return_value = (8, 9)
    _ = client.post(f"{BASE_URL}/enemy-shoot", json={**json_request})

    # Miss shoot.
    mocking_coordinate.return_value = (1, 1)

    response = client.post(f"{BASE_URL}/enemy-shoot", json={**json_request})

    assert response.json == {
        **json_request,
        "coordinates": [[1, 1]],
        "shootingResults": [SignObjects.miss_sign.sign],
        "isKilled": False,
        "isPlayerMove": True,
        "isGameOver": False
    }
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
    ("game_type", "error"), [
        ("just_created", "NotStartedGameError"),
        ("game_started_player", "NotYourTurnError")
    ]
)
def test_enemy_shoot_cannot_work_correctly(application, client, game_type, error):
    """
    Method tests that /enemy-shoot endpoint return correct info if game produce an error during adding new ship.
    Args:
        application: Fixture with tuple, that contains application object and game information for api tests.
        client: Fixture with flash client to make a request.
        game_type: Key for getting correct game stage for testing.
        error: Error name that would be produced.
    """
    json_request = application[1][game_type]

    response = client.post(f"{BASE_URL}/enemy-shoot", json=json_request)

    assert response.json == {"message": "Internal Server Error.", "errorCode": error, "statusCode": 500}
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

    assert response.json == {"message": f"Game with id {json_request['gameId']} is over.", **json_request}
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
    response = client.post(f"{BASE_URL}/exit", json={**json_request, "gameId": uuid.uuid4()})

    assert response.json == {"message": "Internal Server Error.", "errorCode": "NoGameApiError", "statusCode": 500}
    assert response.status_code == StatusCode.APPLICATION_ERROR.value

    response = client.post(f"{BASE_URL}/exit", json={**json_request, "playerId": uuid.uuid4()})

    assert response.json == {"message": "Internal Server Error.",
                             "errorCode": "NoGamePlayerApiError",
                             "statusCode": 500}
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
        "statusCode": 404
    }
    assert response.status_code == StatusCode.ENTITY_NOT_FOUND.value
