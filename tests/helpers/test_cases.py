"""Module contains test cases for api testing."""
import uuid

START_GAME_BAD_REQUEST = [
    ({"gameId": "wrong uuid", "playerId": uuid.uuid4()},
     {"message": "Validation failed.", "errors": {"gameId": ["Not a valid UUID."]}, "statusCode": 400}),
    ({"gameId": uuid.uuid4(), "playerId": "wrong uuid"},
     {"message": "Validation failed.", "errors": {"playerId": ["Not a valid UUID."]}, "statusCode": 400})
]


ADD_SHIP_BAD_REQUEST = [
    ({"gameId": "wrong uuid", "playerId": uuid.uuid4(), "coordinates": [[1, 2]]},
     {"message": "Validation failed.", "errors": {"gameId": ["Not a valid UUID."]}, "statusCode": 400}),
    ({"gameId": uuid.uuid4(), "playerId": "wrong uuid", "coordinates": [[1, 2]]},
     {"message": "Validation failed.", "errors": {"playerId": ["Not a valid UUID."]}, "statusCode": 400}),
    ({"gameId": uuid.uuid4(), "playerId": uuid.uuid4(), "coordinates": "[[1, 2]]"},
     {"message": "Validation failed.", "errors": {"coordinates": ["Not a valid list."]}, "statusCode": 400}),
    ({"gameId": uuid.uuid4(), "playerId": uuid.uuid4(), "coordinates": ["[1, 2]"]},
     {"message": "Validation failed.", "errors": {"coordinates": {"0": ["Not a valid tuple."]}}, "statusCode": 400}),
    ({"gameId": uuid.uuid4(), "playerId": uuid.uuid4(), "coordinates": [["wrong_value", 2]]},
     {"message": "Validation failed.",
      "errors": {"coordinates": {"0": {"0": ["Not a valid integer."]}}}, "statusCode": 400}),
    ({"gameId": uuid.uuid4(), "playerId": uuid.uuid4(), "coordinates": [[1, "wrong_value"]]},
     {"message": "Validation failed.",
      "errors": {"coordinates": {"0": {"1": ["Not a valid integer."]}}}, "statusCode": 400}),

    ({"gameId": uuid.uuid4(), "playerId": uuid.uuid4(), "coordinates": [[0, 2]]},
     {"message": "Validation failed.", "statusCode": 400,
      "errors": {"coordinates": {"0": {"0": ["Must be greater than or equal to 1 and less than or equal to 10."]}}}}),
    ({"gameId": uuid.uuid4(), "playerId": uuid.uuid4(), "coordinates": [[11, 2]]},
     {"message": "Validation failed.", "statusCode": 400,
      "errors": {"coordinates": {"0": {"0": ["Must be greater than or equal to 1 and less than or equal to 10."]}}}}),

    ({"gameId": uuid.uuid4(), "playerId": uuid.uuid4(), "coordinates": [[1, 0]]},
     {"message": "Validation failed.", "statusCode": 400,
      "errors": {"coordinates": {"0": {"1": ["Must be greater than or equal to 1 and less than or equal to 10."]}}}}),
    ({"gameId": uuid.uuid4(), "playerId": uuid.uuid4(), "coordinates": [[1, 11]]},
     {"message": "Validation failed.", "statusCode": 400,
      "errors": {"coordinates": {"0": {"1": ["Must be greater than or equal to 1 and less than or equal to 10."]}}}}),
]


PLAYER_SHOOT_BAD_REQUEST = [
    ({"gameId": "wrong uuid", "playerId": uuid.uuid4(), "coordinate": [1, 2]},
     {"message": "Validation failed.", "errors": {"gameId": ["Not a valid UUID."]}, "statusCode": 400}),
    ({"gameId": uuid.uuid4(), "playerId": "wrong uuid", "coordinate": [1, 2]},
     {"message": "Validation failed.", "errors": {"playerId": ["Not a valid UUID."]}, "statusCode": 400}),
    ({"gameId": uuid.uuid4(), "playerId": uuid.uuid4(), "coordinate": "[1, 2]"},
     {"message": "Validation failed.", "errors": {"coordinate": ["Not a valid tuple."]}, "statusCode": 400}),
    ({"gameId": uuid.uuid4(), "playerId": uuid.uuid4(), "coordinate": ["wrong_value", 2]},
     {"message": "Validation failed.", "errors": {"coordinate": {"0": ["Not a valid integer."]}}, "statusCode": 400}),
    ({"gameId": uuid.uuid4(), "playerId": uuid.uuid4(), "coordinate": [1, "wrong_value"]},
     {"message": "Validation failed.", "errors": {"coordinate": {"1": ["Not a valid integer."]}}, "statusCode": 400}),

    ({"gameId": uuid.uuid4(), "playerId": uuid.uuid4(), "coordinate": [0, 2]},
     {"message": "Validation failed.", "statusCode": 400,
      "errors": {"coordinate": {"0": ["Must be greater than or equal to 1 and less than or equal to 10."]}}}),
    ({"gameId": uuid.uuid4(), "playerId": uuid.uuid4(), "coordinate": [11, 2]},
     {"message": "Validation failed.", "statusCode": 400,
      "errors": {"coordinate": {"0": ["Must be greater than or equal to 1 and less than or equal to 10."]}}}),

    ({"gameId": uuid.uuid4(), "playerId": uuid.uuid4(), "coordinate": [1, 0]},
     {"message": "Validation failed.", "statusCode": 400,
      "errors": {"coordinate": {"1": ["Must be greater than or equal to 1 and less than or equal to 10."]}}}),
    ({"gameId": uuid.uuid4(), "playerId": uuid.uuid4(), "coordinate": [1, 11]},
     {"message": "Validation failed.", "statusCode": 400,
      "errors": {"coordinate": {"1": ["Must be greater than or equal to 1 and less than or equal to 10."]}}}),
]
