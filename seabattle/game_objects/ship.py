"""Module for creation ship objects."""
from dataclasses import dataclass

from seabattle.game_errors.ship_errors import NotParallelShipError, WrongShipSizeError, WrongShipCoordinateError
from seabattle.game_objects.cell import Cell
from seabattle.helpers.constants import SignObjects


@dataclass
class Ship:
    """Class contains ship object and its methods."""

    def __init__(self, ship_cells: dict[tuple, Cell]):
        self._check_coordinates(list(ship_cells.keys()))

        self.ship = self._set_ship_sign(ship_cells)

    @staticmethod
    def _set_ship_sign(ship_cells: dict[tuple, Cell]) -> dict[tuple, Cell]:
        """
        Method changes cell signs from empty to ship sign.
        Args:
            ship_cells: Dictionary with cell coordinates as keys, and cells as values

        Returns:
            Dictionary with cell coordinates and cells with updated sings.
        """
        for cell in ship_cells.values():
            cell.sign = SignObjects.ship_sign.sign

        return ship_cells

    @staticmethod
    def _check_coordinates(coordinates: list[tuple]):
        """
        Method checks giving coordinates if they acceptable as ship coordinates.
        Args:
            coordinates: List of tuples with coordinates.
        """
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
