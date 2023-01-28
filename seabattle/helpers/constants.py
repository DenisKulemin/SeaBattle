"""Module with game constants."""
from copy import deepcopy
from dataclasses import dataclass
from enum import Enum


@dataclass
class Sign:
    """Class for sign mark and value."""
    sign: str
    value: int


@dataclass
class SignObjects:
    """Class contains all possible sings for game."""
    empty_sign = Sign(sign=" ", value=0)
    ship_sign = Sign(sign="0", value=10)
    miss_sign = Sign(sign="*", value=100)
    hit_sign = Sign(sign="X", value=1000)


class StatusCode(Enum):
    """Class contains all useful status codes."""
    OK = 200
    BAD_REQUEST = 400
    VALIDATION_FAILED = 400
    ENTITY_NOT_FOUND = 404
    APPLICATION_ERROR = 500


DIAG_AROUND = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

HORIZONTAL_AROUND = [(-1, 0), (1, 0)]

VERTICAL_AROUND = [(0, -1), (0, 1)]

AREA_AROUND = deepcopy(DIAG_AROUND) + deepcopy(HORIZONTAL_AROUND) + deepcopy(VERTICAL_AROUND)

SHIPS_COORDINATES = (
    [(10, 1), (10, 2), (10, 3), (10, 4)],
    [(10, 6), (10, 7), (10, 8)],
    [(1, 2), (2, 2), (3, 2)],
    [(8, 1), (8, 2)],
    [(8, 5), (8, 6)],
    [(8, 8), (8, 9)],
    [(6, 1)],
    [(6, 3)],
    [(6, 5)],
    [(6, 7)]
)


SWAGGER_URL = "/swagger"
API_URL = "/apidocs"
API_NAME = "Seabattle API"
API_VERSION = "1.0.0"
