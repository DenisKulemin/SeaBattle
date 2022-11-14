"""Module with game constants."""


GAME_OBJECTS = {
    "empty": {"sign": " ", "value": 0},
    "ship": {"sign": "O", "value": 1},
    "miss": {"sign": "*", "value": 10},
    "hit": {"sign": "X", "value": 1000}
}

AREA_AROUND = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
