"""Module for creation board game."""
from typing import Tuple, List
from seabatlle.helpers.constants import GAME_OBJECTS, AREA_AROUND
from seabatlle.game_errors.board_errors import BlockedAreaError, BlockedAreaAroundError


class GameBoard:
    """Class contains board game object and its methods."""

    def __init__(self, width: int = 12, height: int = 12):

        self.width = width
        self.height = height
        self.board = [list(GAME_OBJECTS.get("empty").get("sign") * self.width).copy() for _ in range(self.height)]

    def __repr__(self):
        return "\n".join([" ".join(line[1:-1]) for line in self.board[1:-1]])

    def _check_empty_area(self, coordinates: List[Tuple[int, int]]) -> bool:
        """
        Method checks if area with coordinates is empty.
        Args:
            coordinates: List of coordinates.

        Returns: True if empty, else False.
        """
        empty_place = GAME_OBJECTS.get("empty").get("sign")
        return sum(self.board[x][y] == empty_place for x, y in coordinates) == len(coordinates)

    def _check_empty_area_around(self, coordinates: List[Tuple[int, int]]):
        """
        Method checks if area around (one cell around) coordinates is empty.
        Args:
            coordinates: List of coordinates.

        Returns: True if empty, else False.
        """
        empty_place = GAME_OBJECTS.get("empty").get("sign")
        return sum(sum(self.board[x + x_coord][y + y_coord] == empty_place for x_coord, y_coord in AREA_AROUND)
                   for x, y in coordinates) == len(coordinates) * len(AREA_AROUND)

    def set_ship_coordinate(self, coordinates: List[Tuple[int, int]]) -> None:
        """
        Method sets ship signs with specified coordinates.
        Args:
            coordinates: List of coordinates.
        """

        if not self._check_empty_area(coordinates):
            raise BlockedAreaError(f"Area with coordinates: {coordinates} is not empty.")
        if not self._check_empty_area_around(coordinates):
            raise BlockedAreaAroundError(f"Area around coordinates: {coordinates} is not empty")
        for x, y in coordinates:
            self.board[x][y] = GAME_OBJECTS.get("ship").get("sign")
