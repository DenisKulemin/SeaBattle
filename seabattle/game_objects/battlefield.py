"""Module for creation battlefield."""
from typing import Tuple, List

from seabattle.game_errors.ship_errors import BaseShipError
from seabattle.game_objects.cell import Cell
from seabattle.game_objects.ship import Ship
from seabattle.helpers.constants import SignObjects, AREA_AROUND
from seabattle.game_errors.battlefield_errors import BlockedAreaError, BlockedAreaAroundError, ShotCellEarlierError, \
    AreaOutsideBattleFieldError, CellNotExistError, ExtraShipInFleetError


class BattleField:
    """Class contains battlefield object and its methods."""

    # pylint: disable=too-many-instance-attributes

    def __init__(self, name: str, width: int = 11, height: int = 11, is_visible: bool = True):

        self.name = name
        self.width = width
        self.height = height
        self.battlefield = {(x, y): Cell(x=x, y=y) for x in range(self.width + 1) for y in range(self.height + 1)}
        self.__new_ships: list = self.create_initial_ships()
        self.ships: list = []
        self.is_game_over = False
        self.__is_visible = is_visible

    def __repr__(self):
        representation = "\n".join(
            [" ".join([self.battlefield.get((x, y)).sign for x in range(1, self.width)]) for y in range(1, self.height)]
        )
        if not self.__is_visible:
            return representation.replace(SignObjects.ship_sign.sign, SignObjects.empty_sign.sign)
        return representation

    @staticmethod
    def create_initial_ships() -> list:
        """Method creates list of initial ships lengths."""
        new_ships = []
        for ind, i in enumerate(range(4, 0, -1)):
            for _ in range(0, ind + 1):
                new_ships.append(i)
        return new_ships

    def _check_cell_coordinates(self, coordinates: List[Tuple[int, int]]) -> bool:
        """
        Method checks if cell with coordinate is inside the battlefield and not on border (lines with index 0 and -1).
        Args:
            coordinates: List of coordinates.

        Returns: True if coordinate inside the battlefield, else False.
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
        return sum(self.battlefield[(x, y)].sign == SignObjects.empty_sign.sign for x, y in coordinates) \
            == len(coordinates)

    def _check_empty_area_around(self, coordinates: List[Tuple[int, int]]):
        """
        Method checks if area around (one cell around) coordinates is empty.
        Args:
            coordinates: List of coordinates.

        Returns: True if empty, else False.
        """
        return sum(sum(self.battlefield[(x + x_, y + y_)].sign == SignObjects.empty_sign.sign
                       for x_, y_ in AREA_AROUND)
                   for x, y in coordinates
                   ) == len(coordinates) * len(AREA_AROUND)

    def _game_is_over(self) -> None:
        """Method checks if battlefield has ship signs."""
        self.is_game_over = not sum(sign.sign == SignObjects.ship_sign.sign for sign in self.battlefield.values())

    def _return_new_ship_from_list(self, number_of_cells: int) -> None:
        for index, ship in enumerate(self.__new_ships):
            if ship == number_of_cells:
                self.__new_ships.pop(index)
                break

    def is_all_ships_added(self) -> bool:
        """Method checks if all ships were added to the battlefield."""
        return not self.__new_ships

    def set_ship_coordinates(self, coordinates: List[Tuple[int, int]]) -> None:
        """
        Method sets ship signs with specified coordinates.
        Args:
            coordinates: List of coordinates.
        """

        if not self._check_cell_coordinates(coordinates):
            raise AreaOutsideBattleFieldError(f"Area with coordinates: {coordinates} is outside the battlefield."
                                              f"Should be inside x - 1:{self.width - 1}, y - 1:{self.height - 1}")
        if not self._check_empty_area(coordinates):
            raise BlockedAreaError(f"Area with coordinates: {coordinates} is not empty.")
        if not self._check_empty_area_around(coordinates):
            raise BlockedAreaAroundError(f"Area around coordinates: {coordinates} is not empty")

        ship_len = len(coordinates)
        if ship_len in self.__new_ships:
            self._return_new_ship_from_list(ship_len)
        else:
            raise ExtraShipInFleetError(f"Couldn't add ship with such size: {ship_len}")

        try:
            ship = Ship({coordinate: self.battlefield[coordinate] for coordinate in coordinates})
            self.ships.append(ship)
        except BaseShipError as exp:
            print("Couldn't create a ship.")
            print(exp)
            raise BaseShipError from exp

    def shoot(self, coordinate: Tuple[int, int]) -> str:
        """
        Method contains logic for shooting and changing marks on battlefield.
        Args:
            coordinate: Coordinate for shooting.
        Returns:
            str: New sign after shooting for coordinate.
        """
        x, y = coordinate
        if self.battlefield.get(coordinate) is None:
            raise CellNotExistError(f"Cell with coordinate {coordinate} is not exist.")
        if not self._check_cell_coordinates([coordinate]):
            raise AreaOutsideBattleFieldError(f"Area with coordinates: {coordinate} is outside the battlefield."
                                              f"Should be inside x - 1:{self.width - 1}, y - 1:{self.height - 1}")
        if self.battlefield[(x, y)].sign == SignObjects.empty_sign.sign:
            self.battlefield[(x, y)] = Cell(x=x, y=y, sign=SignObjects.miss_sign.sign)
        elif self.battlefield[(x, y)].sign == SignObjects.ship_sign.sign:
            self.battlefield[(x, y)] = Cell(x=x, y=y, sign=SignObjects.hit_sign.sign)
        else:
            raise ShotCellEarlierError(f"Cell with coordinate {coordinate} was shot already.")
        self._game_is_over()
        return self.battlefield[(x, y)].sign
