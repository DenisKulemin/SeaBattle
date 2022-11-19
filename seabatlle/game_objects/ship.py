"""Module for creation ship objects."""
from typing import List, Tuple

from seabatlle.game_errors.ship_errors import NotParallelShipError, WrongShipSizeError, WrongShipCoordinateError
from seabatlle.helpers.constants import GAME_OBJECTS, SHIP_SIGN, SIGN


class Ship:
    """Class contains ship object and its methods."""

    def __init__(self, coordinates: List[Tuple[int, int]]):
        self.ship_size = len(coordinates)
        self.ship_coordinates = coordinates
        self._check_coordinates()

        self.ship = [GAME_OBJECTS.get(SHIP_SIGN).get(SIGN) for _ in range(self.ship_size)]

    def _check_coordinates(self):
        x_size = abs(self.ship_coordinates[0][0] - self.ship_coordinates[-1][0])
        y_size = abs(self.ship_coordinates[0][1] - self.ship_coordinates[-1][1])

        if not (x_size == 0 or y_size == 0):
            raise NotParallelShipError(f"Ship with coordinates {self.ship_coordinates} is not parallel x- or y-axis.")

        if (x_size == 0 and y_size != self.ship_size - 1) or (y_size == 0 and x_size != self.ship_size - 1):
            raise WrongShipSizeError(f"Ship with coordinates {self.ship_coordinates} has wrong size {self.ship_size}.")

        if x_size:
            theory_ship_coord = [(self.ship_coordinates[0][0] + x, self.ship_coordinates[0][1])
                                 for x in range(self.ship_size)]
        else:
            theory_ship_coord = [(self.ship_coordinates[0][0], self.ship_coordinates[0][1] + y)
                                 for y in range(self.ship_size)]

        if self.ship_coordinates != theory_ship_coord:
            raise WrongShipCoordinateError(f"Ship with coordinates {self.ship_coordinates} doesn't match theory "
                                           f"coordinates {theory_ship_coord}.")
