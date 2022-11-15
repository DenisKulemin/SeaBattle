"""Module with game constants."""

EMPTY_SIGN = "empty"
SHIP_SIGN = "ship"
MISS_SIGN = "miss"
HIT_SIGN = "hit"
SIGN = "sign"
VALUE = "value"

GAME_OBJECTS = {
    EMPTY_SIGN: {SIGN: " ", VALUE: 0},
    SHIP_SIGN: {SIGN: "O", VALUE: 1},
    MISS_SIGN: {SIGN: "*", VALUE: 10},
    HIT_SIGN: {SIGN: "X", VALUE: 1000}
}

AREA_AROUND = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
