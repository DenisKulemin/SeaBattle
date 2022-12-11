"""Module for creation ship objects."""
from dataclasses import dataclass
from typing import List, Tuple

from seabattle.game_errors.ship_errors import NotParallelShipError, WrongShipSizeError, WrongShipCoordinateError
from seabattle.game_objects.cell import Cell


@dataclass
class Ship:
    """Class contains ship object and its methods."""

    def __init__(self, coordinates: List[Tuple[int, int]]):
        self._check_coordinates(coordinates)

        self.ship = {(x, y): Cell(x=x, y=y) for x, y in coordinates}

    @staticmethod
    def _check_coordinates(coordinates):
        ship_len = len(coordinates)
        x_size = abs(coordinates[0][0] - coordinates[-1][0])
        y_size = abs(coordinates[0][1] - coordinates[-1][1])

        if not (x_size == 0 or y_size == 0):
            raise NotParallelShipError(f"Ship with coordinates {coordinates} is not parallel x- or y-axis.")

        if (x_size == 0 and y_size != ship_len - 1) or (y_size == 0 and x_size != ship_len - 1):
            raise WrongShipSizeError(f"Ship with coordinates {coordinates} has wrong size {ship_len}.")

        if x_size:
            theory_ship_coord = [(coordinates[0][0] + x, coordinates[0][1])
                                 for x in range(ship_len)]
        else:
            theory_ship_coord = [(coordinates[0][0], coordinates[0][1] + y)
                                 for y in range(ship_len)]

        if coordinates != theory_ship_coord:
            raise WrongShipCoordinateError(f"Ship with coordinates {coordinates} doesn't match theory "
                                           f"coordinates {theory_ship_coord}.")
