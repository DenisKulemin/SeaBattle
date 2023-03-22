"""Module for creation battlefield."""
from typing import Tuple, List, Dict

from seabattle.game_objects.cell import Cell
from seabattle.game_objects.ship import Ship
from seabattle.helpers.constants import SignObjects, AREA_AROUND, SHIP_NAMES, DEFAULT_BATTLEFIELD_END_COORD
from seabattle.game_errors.battlefield_errors import BlockedAreaError, BlockedAreaAroundError, ShotCellEarlierError, \
    AreaOutsideBattleFieldError, CellNotExistError, ExtraShipInFleetError


class BattleField:
    """Class contains battlefield object and its methods."""

    # pylint: disable=too-many-instance-attributes

    def __init__(
            self,
            name: str,
            width: int = DEFAULT_BATTLEFIELD_END_COORD,
            height: int = DEFAULT_BATTLEFIELD_END_COORD,
            is_visible: bool = True
    ):

        self.name = name
        self.width = width
        self.height = height
        self.battlefield = {(x, y): Cell(x=x, y=y) for y in range(self.height + 1) for x in range(self.width + 1)}
        self.__new_ships: list = self.create_initial_ships()
        self.ships: dict = {}
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
            new_ships.extend([i for _ in range(0, ind + 1)])
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

    def _exclude_new_ship_from_list(self, number_of_cells: int) -> None:
        self.__new_ships.remove(number_of_cells)

    def is_all_ships_added(self) -> bool:
        """Method checks if all ships were added to the battlefield."""
        return not self.__new_ships

    def set_ship_coordinates(self, coordinates: List[Tuple[int, int]]) -> Dict[Tuple[int, int], Cell]:
        """
        Method sets ship signs with specified coordinates.
        Args:
            coordinates: List of coordinates.

        Returns:
            Dictionary with coordinates as keys and cell as values.
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
            ship = Ship({coordinate: self.battlefield[coordinate] for coordinate in coordinates})
            self._exclude_new_ship_from_list(ship_len)
        else:
            raise ExtraShipInFleetError(f"Couldn't add ship with such size: {ship_len}")

        self.ships.update({ship.id: ship})
        return ship.ship

    def shoot(self, coordinate: Tuple[int, int]) -> Tuple[dict[Tuple[int, int], Cell], bool]:
        """
        Method contains logic for shooting and changing marks on battlefield.
        Args:
            coordinate: Coordinate for shooting.
        Returns:
            str: Updated cells after shooting for coordinate and bool value if the ship was killed.
        """
        x, y = coordinate
        if self.battlefield.get(coordinate) is None:
            raise CellNotExistError(f"Cell with coordinate {coordinate} is not exist.")
        if not self._check_cell_coordinates([coordinate]):
            raise AreaOutsideBattleFieldError(f"Area with coordinates: {coordinate} is outside the battlefield."
                                              f"Should be inside x - 1:{self.width - 1}, y - 1:{self.height - 1}")
        if self.battlefield[(x, y)].sign == SignObjects.empty_sign.sign:
            self.battlefield[(x, y)].sign = SignObjects.miss_sign.sign
        elif self.battlefield[(x, y)].sign == SignObjects.ship_sign.sign:
            self.battlefield[(x, y)].sign = SignObjects.hit_sign.sign
        else:
            raise ShotCellEarlierError(f"Cell with coordinate {coordinate} was shot already.")

        # Get ship id and check if ship is still alive.
        ship_id = self.battlefield[(x, y)].ship_id
        is_killed = False
        if ship_id is not None:
            is_killed = not self.ships[ship_id].is_ship_alive()

        self._game_is_over()
        return {coordinate: self.battlefield[coordinate]}, is_killed

    def get_fleet_structure(self) -> Dict[str, int]:
        """
        Method collects information about alive ships in the fleet.

        Returns:
            Dictionary with ship name as key and number of such ships that still alive.
        """
        fleet_structure = {ship_name: 0 for ship_name in SHIP_NAMES.values()}
        for ship in self.ships.values():
            fleet_structure[SHIP_NAMES[len(ship.ship)]] += ship.is_alive

        return fleet_structure

    def get_battlefield(self) -> Dict[Tuple[int, int], Cell]:
        """
        Method filters battlefield coordinates (returns only cells that end user should see).

        Returns:
            Dictionary with tuple coordinates as key and cell as value.
        """
        return {coord: cell for coord, cell in self.battlefield.items()
                if (1 <= coord[0] < self.width and 1 <= coord[1] < self.height)}
