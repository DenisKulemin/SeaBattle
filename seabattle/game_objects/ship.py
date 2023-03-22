"""Module for creation ship objects."""
import uuid
from dataclasses import dataclass
from typing import Tuple

from seabattle.game_errors.ship_errors import NotParallelShipError, WrongShipCoordinateError
from seabattle.game_objects.cell import Cell
from seabattle.helpers.constants import SignObjects, SHIP_NAMES


@dataclass
class Ship:
    """Class contains ship object and its methods."""

    def __init__(self, ship_cells: dict[Tuple[int, int], Cell]):
        self.id = uuid.uuid4()
        self._check_coordinates(list(ship_cells.keys()))

        self.ship = self._set_ship_info(ship_cells)
        self.name = SHIP_NAMES.get(len(self.ship))
        self.is_alive = True

    def _set_ship_info(self, ship_cells: dict[Tuple[int, int], Cell]) -> dict[Tuple[int, int], Cell]:
        """
        Method changes cell signs from empty to ship sign and add ship id.
        Args:
            ship_cells: Dictionary with cell coordinates as keys, and cells as values

        Returns:
            Dictionary with cell coordinates and cells with updated sings.
        """
        for cell in ship_cells.values():
            cell.sign = SignObjects.ship_sign.sign
            cell.ship_id = self.id

        return ship_cells

    @staticmethod
    def _check_coordinates(coordinates: list[Tuple[int, int]]):
        """
        Method checks giving coordinates if they acceptable as ship coordinates.
        Args:
            coordinates: List of tuples with coordinates.
        """
        ship_len = len(coordinates)
        coordinates = sorted(coordinates, key=lambda coordinate: coordinate[0] * 10 + coordinate[1])
        x_size = abs(coordinates[0][0] - coordinates[-1][0])
        y_size = abs(coordinates[0][1] - coordinates[-1][1])

        if not (x_size == 0 or y_size == 0):
            raise NotParallelShipError(f"Ship with coordinates {coordinates} is not parallel x- or y-axis.")

        if x_size:
            theory_ship_coord = [(coordinates[0][0] + x, coordinates[0][1])
                                 for x in range(ship_len)]
        else:
            theory_ship_coord = [(coordinates[0][0], coordinates[0][1] + y)
                                 for y in range(ship_len)]

        if coordinates != theory_ship_coord:
            raise WrongShipCoordinateError(
                f"Ship with coordinates {coordinates} doesn't match theory "
                f"coordinates {theory_ship_coord}, based on coordinates quantity - {ship_len}."
            )

    def is_ship_alive(self) -> bool:
        """
        Method check if there are any ship's cells that still alive.

        Returns:
            True, if there is at least one ship cell that alive.
        """
        self.is_alive = sum(cell.sign == SignObjects.ship_sign.sign for cell in self.ship.values()) > 0
        return self.is_alive
