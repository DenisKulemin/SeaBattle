"""Module contains player class."""
from abc import ABC
from typing import Tuple, List

from seabattle.game_objects.battlefield import BattleField


class BasePlayer(ABC):
    """Base class for player."""
    player_battlefield: BattleField
    enemy_battlefield: BattleField
    is_game_over: bool

    def _is_game_over(self):  # pragma: no cover
        raise NotImplementedError

    def shoot(self, coordinate: Tuple[int, int], shooting_result: str):  # pragma: no cover
        """Base method for shooting."""
        raise NotImplementedError

    def enemy_shooting(self, coordinate: Tuple[int, int]) -> str:  # pragma: no cover
        """Base method for enemy shooting."""
        raise NotImplementedError

    def set_ship_coordinates(self, coordinates: List[Tuple[int, int]]) -> None:  # pragma: no cover
        """Base method for adding ship."""
        raise NotImplementedError

    def is_all_ships_added(self) -> bool:
        """Method check if all ships added to the battlefield."""
        return self.player_battlefield.is_all_ships_added()


class Player(BasePlayer):
    """Class contains battlefields and rule them in a game."""
    player_battlefield: BattleField

    def __init__(self, player_name: str, enemy_name: str):
        self.player_battlefield = BattleField(name=player_name)
        self.enemy_battlefield = BattleField(name=enemy_name, is_visible=False)
        self.is_game_over = self.player_battlefield.is_game_over or self.enemy_battlefield.is_game_over

    def __repr__(self):
        return f"------------{self.player_battlefield.name}'s battlefield---------\n"\
               f"{repr(self.player_battlefield)}\n" \
               f"------------{self.enemy_battlefield.name}'s battlefield---------\n" \
               f"{repr(self.enemy_battlefield)}"

    def _is_game_over(self):
        """Method checks if game for player is over based on its battlefield."""
        self.is_game_over = self.player_battlefield.is_game_over or self.enemy_battlefield.is_game_over

    def shoot(self, coordinate: Tuple[int, int], shooting_result: str):
        """
        Method runs shoot command on enemy battlefield.
        Args:
            coordinate: Coordinate for shooting.
            shooting_result: Sing of shooting result on enemy battlefield.
        """
        self.enemy_battlefield.battlefield[coordinate].sign = shooting_result

    def enemy_shooting(self, coordinate: Tuple[int, int]) -> str:
        """
        Method runs shoot command on player battlefield.
        Args:
            coordinate: Coordinate for shooting.
        Returns:
            str: New sign after shooting for coordinate.
        """
        shooting_result = self.player_battlefield.shoot(coordinate)
        self._is_game_over()
        return shooting_result

    def set_ship_coordinates(self, coordinates: List[Tuple[int, int]]) -> None:
        """
        Method sets ship signs with specified coordinates on player battlefield.
        Args:
            coordinates: List of coordinates.
        """
        self.player_battlefield.set_ship_coordinates(coordinates)
