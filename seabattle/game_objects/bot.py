"""Module contains bot objects."""
import random
from copy import deepcopy
from typing import Tuple, List

from seabattle.game_errors.battlefield_errors import BaseBattleFieldError
from seabattle.game_objects.player import Player
from seabattle.helpers.constants import AREA_AROUND


class EasyBot(Player):
    """Class contains logic for the simplest bot."""

    def __init__(self, player_name: str, enemy_name: str):
        super().__init__(player_name, enemy_name)
        self.coordinates_for_shooting = [
            (x, y) for x in range(1, self.player_battlefield.width)
            for y in range(1, self.player_battlefield.height)
        ]
        self.__fill_bot_battlefield()

    @staticmethod
    def __create_bot_ship_coordinates(ship_len: int, empty_cells: dict) -> list:
        """
        Method creates list of possible coordinates for ship with specified length according to correctly available
        cells.
        Args:
            ship_len: Length of ship.
            empty_cells: Dictionary with coordinates of empty cells for bot battlefield.

        Returns:
            list: List of all possible coordinates for ship.
        """
        list_of_coordinates = []
        for x, y in empty_cells.keys():
            for dimension in [(1, 0), (0, 1)]:
                is_coordinates_empty = [empty_cells.get(x + i * dimension[0], y + i * dimension[1])
                                        for i in range(ship_len)]
                if None is not is_coordinates_empty:
                    list_of_coordinates.append([(x + i * dimension[0], y + i * dimension[1]) for i in range(ship_len)])
        return list_of_coordinates

    @staticmethod
    def __clear_not_empty_coordinates(coordinates: List[Tuple[int, int]], empty_cells: dict):
        """
        Method clear the dictionary with empty cells.
        Args:
            coordinates: Ship coordinates.
            empty_cells: Dictionary with coordinates of empty cells for bot battlefield.
        """
        for x, y in coordinates:
            _ = [empty_cells.pop((x + x_, y + y_), None) for x_, y_ in [(0, 0)] + AREA_AROUND]

    def __fill_bot_battlefield(self):
        """Method creates the full flotilla of ships for bot battlefield with random coordinates."""
        empty_cells = {key: 1 for key in self.coordinates_for_shooting}
        for ship_len in deepcopy(self.player_battlefield.create_initial_ships()):
            list_of_coordinates = self.__create_bot_ship_coordinates(ship_len, empty_cells)
            for _ in range(len(list_of_coordinates)):
                try:
                    coordinates = random.choice(list_of_coordinates)
                    list_of_coordinates.remove(coordinates)
                    self.player_battlefield.set_ship_coordinates(coordinates)
                    self.__clear_not_empty_coordinates(coordinates, empty_cells)
                    break
                except (BaseBattleFieldError, SyntaxError, TypeError):
                    continue

    def choose_shooting_coordinate(self) -> Tuple[int, int]:
        """
        Method chooses the random coordinate for shooting.

        Returns:
            tuple: Coordinate for shooting
        """
        return self.coordinates_for_shooting.pop(random.randint(0, len(self.coordinates_for_shooting) - 1))
