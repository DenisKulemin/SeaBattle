"""Module contains bot objects."""
import random
from copy import deepcopy
from typing import Tuple, List, Dict
from seabattle.game_objects.player import Player
from seabattle.helpers.constants import AREA_AROUND


class EasyBot(Player):
    """Class contains logic for the simplest bot."""

    def __init__(self, player_name: str, enemy_name: str):
        super().__init__(player_name, enemy_name)
        self._fill_bot_battlefield()

    @staticmethod
    def _create_bot_ship_coordinates(ship_len: int, empty_cells: Dict[Tuple[int, int], int]) -> List[Tuple[int, int]]:
        """
        Method creates list of possible coordinates for ship with specified length according to correctly available
        cells.
        Args:
            ship_len: Length of ship.
            empty_cells: Dictionary with coordinates of empty cells for bot battlefield.

        Returns:
            list: The random coordinates for ship from list of all possible coordinates.
        """
        list_of_coordinates = []
        for x, y in empty_cells.keys():
            for dimension in [(1, 0), (0, 1)]:
                is_coordinates_empty = [empty_cells.get((x + i * dimension[0], y + i * dimension[1]))
                                        for i in range(ship_len)]
                if None not in is_coordinates_empty:
                    list_of_coordinates.append([(x + i * dimension[0], y + i * dimension[1]) for i in range(ship_len)])
        return random.choice(list_of_coordinates)

    @staticmethod
    def _clear_not_empty_coordinates(coordinates: List[Tuple[int, int]], empty_cells: dict):
        """
        Method clear the dictionary with empty cells.
        Args:
            coordinates: Ship coordinates.
            empty_cells: Dictionary with coordinates of empty cells for bot battlefield.
        """
        for x, y in coordinates:
            _ = [empty_cells.pop((x + x_, y + y_), None) for x_, y_ in [(0, 0)] + AREA_AROUND]

    def _fill_bot_battlefield(self):
        """Method creates the full flotilla of ships for bot battlefield with random coordinates."""
        empty_cells = {key: 1 for key in self.coordinates_for_shooting}
        for ship_len in deepcopy(self.player_battlefield.create_initial_ships()):
            coordinates = self._create_bot_ship_coordinates(ship_len, empty_cells)
            self.player_battlefield.set_ship_coordinates(coordinates)
            self._clear_not_empty_coordinates(coordinates, empty_cells)
