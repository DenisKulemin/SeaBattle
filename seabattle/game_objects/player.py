"""Module contains player class."""
import random
from typing import Tuple, List, Set, Dict, Optional
from uuid import uuid4, UUID

from seabattle.game_objects.battlefield import BattleField
from seabattle.helpers.constants import SignObjects, DIAG_AROUND, AREA_AROUND, HORIZONTAL_AROUND, VERTICAL_AROUND


class Player:
    """Class contains battlefields and rule them in a game."""

    # pylint: disable=too-many-instance-attributes

    id: UUID
    player_battlefield: BattleField
    enemy_battlefield: BattleField
    is_game_over: bool
    coordinates_for_shooting: list
    top_target_coordinates: list
    demaged_ships_coordinates: list
    is_horizontal: Optional[bool]

    def __init__(self, player_name: str, enemy_name: str):
        self.id = uuid4()
        self.player_battlefield = BattleField(name=player_name)
        self.enemy_battlefield = BattleField(name=enemy_name, is_visible=False)
        self.is_game_over = self.player_battlefield.is_game_over or self.enemy_battlefield.is_game_over
        self.coordinates_for_shooting = [
            (x, y) for x in range(1, self.player_battlefield.width)
            for y in range(1, self.player_battlefield.height)
        ]
        self.top_target_coordinates = []
        self.demaged_ships_coordinates = []

    def __repr__(self):
        return f"------------{self.player_battlefield.name}'s battlefield---------\n" \
               f"{repr(self.player_battlefield)}\n" \
               f"------------{self.enemy_battlefield.name}'s battlefield---------\n" \
               f"{repr(self.enemy_battlefield)}"

    def _is_game_over(self):
        """Method checks if game for player is over based on its battlefield."""
        self.is_game_over = self.player_battlefield.is_game_over or self.enemy_battlefield.is_game_over

    def _is_horizontal_ship(self) -> Optional[bool]:
        """Method defines if the demaged ship is horizontal or not."""
        if len(self.demaged_ships_coordinates) > 1:
            # Check if all x coordinate in demaged_ships_coordinates are the same.
            return bool(len({coordinate[0] for coordinate in self.demaged_ships_coordinates}) - 1)
        return None

    def shoot(self, shooting_results: Dict[Tuple[int, int], str], is_killed: bool):
        """
        Method runs shoot command on enemy battlefield.
        Args:
            shooting_results: Dictionary with coordinates as keys and sings of shooting result on enemy battlefield
                as values.
            is_killed: Bool mark, that informs if the ship is sunk.
        """
        for coordinate, shooting_result in shooting_results.items():
            self.enemy_battlefield.battlefield[coordinate].sign = shooting_result
            if shooting_result == SignObjects.hit_sign.sign:
                self.demaged_ships_coordinates.append(coordinate)
                self.define_top_target_coordinates(coordinate, is_killed)
        self.clear_coordinates_for_shooting(list(shooting_results.keys()))

    def enemy_shooting(self, coordinate: Tuple[int, int]) -> Tuple[Dict[Tuple[int, int], str], bool]:
        """
        Method runs shoot command on player battlefield.
        Args:
            coordinate: Coordinate for shooting.
        Returns:
            str: New sign after shooting for coordinate.
        """
        shooting_results, is_killed = self.player_battlefield.shoot(coordinate)
        if shooting_results[coordinate] == SignObjects.hit_sign.sign:
            shooting_results = self.set_sings_for_lucky_shoot(self.player_battlefield, coordinate, is_killed)
        self._is_game_over()
        return shooting_results, is_killed

    def set_ship_coordinates(self, coordinates: List[Tuple[int, int]]) -> None:
        """
        Method sets ship signs with specified coordinates on player battlefield.
        Args:
            coordinates: List of coordinates.
        """
        self.player_battlefield.set_ship_coordinates(coordinates)

    def is_all_ships_added(self) -> bool:
        """Method check if all ships added to the battlefield."""
        return self.player_battlefield.is_all_ships_added()

    def choose_shooting_coordinate(self) -> Tuple[int, int]:
        """
        Method chooses the random coordinate for shooting. Shouldn't be used for player.

        Returns:
            tuple: Coordinate for shooting
        """

        if self.top_target_coordinates:
            coordinate = self.top_target_coordinates.pop(random.randint(0, len(self.top_target_coordinates) - 1))
            self.coordinates_for_shooting.remove(coordinate)
            return coordinate

        return self.coordinates_for_shooting.pop(random.randint(0, len(self.coordinates_for_shooting) - 1))

    def define_top_target_coordinates(self, coordinate: Tuple[int, int], is_killed: bool):
        """
        Method defines coordinates that should be used for shooting be used first, if we hit the ship.
        Args:
            coordinate: Coordinate that was used for shooting right now.
            is_killed: Boolean mark. True, if ship was sunk.
        """
        if is_killed:
            # Clear all these variable if previous ship was sunk.
            self.top_target_coordinates = []
            self.demaged_ships_coordinates = []
            self.is_horizontal = None
        else:
            self.is_horizontal = self._is_horizontal_ship()
            x, y = coordinate
            if self.is_horizontal is None:
                # Add all directions as ship has only one cell for now.
                self.top_target_coordinates.extend([(x + x_, y + y_) for x_, y_ in HORIZONTAL_AROUND])
                self.top_target_coordinates.extend([(x + x_, y + y_) for x_, y_ in VERTICAL_AROUND])
            elif self.is_horizontal:
                # Add horizontal coordinates.
                self.top_target_coordinates.extend([(x + x_, y + y_) for x_, y_ in HORIZONTAL_AROUND])
                self.top_target_coordinates = [top_coordinate for top_coordinate in self.top_target_coordinates
                                               if top_coordinate[1] == y]
            else:
                # Add vertical coordinates.
                self.top_target_coordinates.extend([(x + x_, y + y_) for x_, y_ in VERTICAL_AROUND])
                self.top_target_coordinates = [top_coordinate for top_coordinate in self.top_target_coordinates
                                               if top_coordinate[0] == x]

    def clear_coordinates_for_shooting(self, coordinates: list):
        """
        Method deletes coordinates that cannot be used for shooting (were shot already or were updated after
        successful shooting).
        Args:
            coordinates: List of coordinates for deleting.
        """
        for coordinate in coordinates:
            if coordinate in self.coordinates_for_shooting:
                self.coordinates_for_shooting.remove(coordinate)

        # Update top_target_coordinates if it has any coordinates.
        if self.top_target_coordinates:
            self.top_target_coordinates = list(
                set(self.top_target_coordinates).intersection(set(self.coordinates_for_shooting))
            )

    @staticmethod
    def get_coordinates_for_update(battlefield: BattleField,
                                   coordinate: Tuple[int, int],
                                   is_killed: bool) -> Set[Tuple[int, int]]:
        """
        Method generates set of coordinates that should be updated after shooting.
        Args:
            battlefield: BattleField object.
            coordinate: Shooting coordinate.
            is_killed: Boolean mark. True, if ship was sunk.

        Returns:
            set: Set of coordinates for cells on battlefield, that should be updated (change signs).
        """
        coordinates = {coordinate}
        x, y = coordinate
        for x_add, y_add in DIAG_AROUND:
            coordinates.add((x + x_add, y + y_add))

        if is_killed:
            ship_id = battlefield.battlefield[(x, y)].ship_id
            for cell in battlefield.ships[ship_id].ship.values():
                for x_add, y_add in AREA_AROUND:
                    coordinates.add((cell.x + x_add, cell.y + y_add))
        return coordinates

    def set_sings_for_lucky_shoot(self, battlefield: BattleField,
                                  coordinate: Tuple[int, int],
                                  is_killed: bool) -> Dict[Tuple[int, int], str]:
        """
        Method updates cell sings on battlefield after successful shooting.
        Args:
            battlefield: BattleField object.
            coordinate: Shooting coordinate.
            is_killed: Boolean mark. True, if ship was sunk.

        Returns:
            dict: Dict of coordinates for cells on battlefield as keys, and new signs as values.
        """
        coordinates_for_update = self.get_coordinates_for_update(battlefield, coordinate, is_killed)
        shooting_results = {}
        for new_coordinate in coordinates_for_update:
            if battlefield.battlefield[new_coordinate].sign == SignObjects.empty_sign.sign:
                battlefield.battlefield[new_coordinate].sign = SignObjects.miss_sign.sign
            if 1 <= new_coordinate[0] <= self.player_battlefield.width - 1 and \
                    1 <= new_coordinate[1] <= self.player_battlefield.height - 1:
                shooting_results.update({new_coordinate: battlefield.battlefield[new_coordinate].sign})
        return shooting_results
