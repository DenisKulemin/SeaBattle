"""Module for creation board game."""
from typing import Tuple, List

from seabatlle.game_errors.ship_errors import BaseShipError
from seabatlle.game_objects.cell import Cell
from seabatlle.game_objects.ship import Ship
from seabatlle.helpers.constants import SignObjects, AREA_AROUND
from seabatlle.game_errors.board_errors import BlockedAreaError, BlockedAreaAroundError, ShotCellEarlierError, \
    AreaOutsideBoardError


class GameBoard:
    """Class contains board game object and its methods."""

    def __init__(self, width: int = 12, height: int = 12):

        self.width = width
        self.height = height
        self.board = {(x, y): Cell(x=x, y=y) for x in range(self.width + 1) for y in range(self.height + 1)}
        self.ships = []
        self.game_is_over = False

    def __repr__(self):
        return "\n".join(
            [" ".join([self.board.get((x, y)).sign for x in range(1, self.width)]) for y in range(1, self.height)]
        )

    def _check_cell_coordinates(self, coordinates: List[Tuple[int, int]]) -> bool:
        """
        Method checks if cell with coordinate is inside the game board and not on border (lines with index 0 and -1).
        Args:
            coordinates: List of coordinates.

        Returns: True if coordinate inside the game board, else False.
        """
        return sum((0 < coord[0] < self.width) and (0 < coord[1] < self.height) for coord in coordinates) \
            == len(coordinates)

    def _check_empty_area(self, coordinates: List[Tuple[int, int]]) -> bool:
        """
        Method checks if area with coordinates is empty.
        Args:
            coordinates: List of coordinates.

        Returns: True if empty, else False.
        """
        return sum(self.board.get((x, y)).sign == SignObjects.empty_sign.sign for x, y in coordinates) \
            == len(coordinates)

    def _check_empty_area_around(self, coordinates: List[Tuple[int, int]]):
        """
        Method checks if area around (one cell around) coordinates is empty.
        Args:
            coordinates: List of coordinates.

        Returns: True if empty, else False.
        """
        return sum(sum(self.board.get((x + x_, y + y_)).sign == SignObjects.empty_sign.sign for x_, y_ in AREA_AROUND)
                   for x, y in coordinates
                   ) == len(coordinates) * len(AREA_AROUND)

    def _game_is_over(self) -> None:
        """Method checks if board game has ship signs."""
        self.game_is_over = not sum(sign.sign == SignObjects.ship_sign.sign for sign in self.board.values())

    def set_ship_coordinate(self, coordinates: List[Tuple[int, int]]) -> None:
        """
        Method sets ship signs with specified coordinates.
        Args:
            coordinates: List of coordinates.
        """

        if not self._check_cell_coordinates(coordinates):
            raise AreaOutsideBoardError(f"Area with coordinates: {coordinates} is outside the game board."
                                        f"Should be inside x - 1:{self.width - 1}, y - 1:{self.height - 1}")
        if not self._check_empty_area(coordinates):
            raise BlockedAreaError(f"Area with coordinates: {coordinates} is not empty.")
        if not self._check_empty_area_around(coordinates):
            raise BlockedAreaAroundError(f"Area around coordinates: {coordinates} is not empty")

        try:
            ship = Ship(coordinates)
            self.ships.append(ship)
            for x, y in coordinates:
                self.board[(x, y)] = Cell(x=x, y=y, sign=SignObjects.ship_sign.sign)
        except BaseShipError as exp:
            print("Couldn't create a ship.")
            print(exp)

    def shoot(self, coordinate: Tuple[int, int]) -> None:
        """
        Method contains logic for shooting and changing marks on battlefield.
        Args:
            coordinate: Coordinate for shooting.
        """
        x, y = coordinate
        if self.board.get((x, y)).sign == SignObjects.empty_sign.sign:
            self.board[(x, y)] = Cell(x=x, y=y, sign=SignObjects.miss_sign.sign)
        elif self.board.get((x, y)).sign == SignObjects.ship_sign.sign:
            self.board[(x, y)] = Cell(x=x, y=y, sign=SignObjects.hit_sign.sign)
        else:
            raise ShotCellEarlierError(f"Cell with coordinate {coordinate} was shot already.")
        self._game_is_over()
