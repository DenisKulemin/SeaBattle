"""Module with game class."""
import random
from typing import Tuple, List
from uuid import UUID, uuid4
from seabattle.game_errors.game_errors import StartedGameError, NotStartedGameError, NotYourTurnError
from seabattle.game_objects.bot import EasyBot
from seabattle.game_objects.player import Player
from seabattle.helpers.constants import SignObjects


class Game:
    """Class with main game logic."""
    id: UUID
    player: Player
    enemy: EasyBot
    is_game_started: bool
    is_player_move: bool

    def __init__(self):
        self.id = uuid4()
        self.player = Player(player_name="Mike", enemy_name="Sailor")
        self.enemy = EasyBot(player_name="Sailor", enemy_name="Mike")
        self.is_game_started = False
        self.is_player_move = random.choice([True, False])

    def player_shoot(self, coordinate: Tuple[int, int]) -> dict:
        """
        Method processes player shoot command.
        Args:
            coordinate: Tuple with coordinate for shooting.
        """
        if self.is_game_started:
            if self.is_player_move:
                shooting_results, is_killed = self.enemy.enemy_shooting(coordinate)
                if shooting_results[coordinate] != SignObjects.hit_sign.sign:
                    self.is_player_move = not self.is_player_move
                self.player.shoot(shooting_results, is_killed)
                return {"coordinates": list(shooting_results.keys()),
                        "shooting_results": list(shooting_results.values()),
                        "is_killed": is_killed,
                        "is_player_move": self.is_player_move,
                        "is_game_over": self.enemy.is_game_over}
            raise NotYourTurnError("Right now is not your turn for shooting.")
        raise NotStartedGameError("Game is not started. Cannot shooting.")

    def enemy_shoot(self) -> dict:
        """
        Method processes enemy shoot command.

        Returns:
            str: New sign after shooting for coordinate.
        """
        if self.is_game_started:
            if not self.is_player_move:
                coordinate = self.enemy.choose_shooting_coordinate()
                shooting_results, is_killed = self.player.enemy_shooting(coordinate)
                if shooting_results[coordinate] != SignObjects.hit_sign.sign:
                    self.is_player_move = not self.is_player_move
                self.enemy.shoot(shooting_results, is_killed)
                return {"coordinates": list(shooting_results.keys()),
                        "shooting_results": list(shooting_results.values()),
                        "is_killed": is_killed,
                        "is_player_move": self.is_player_move,
                        "is_game_over": self.player.is_game_over}
            raise NotYourTurnError("Right now is not your turn for shooting.")
        raise NotStartedGameError("Game is not started. Cannot shooting.")

    def player_set_ship(self, coordinates: List[Tuple[int, int]]) -> str:
        """
        Method processes player set ship command.
        Args:
            coordinates: List of ship's cells coordinates.
        """
        if not self.is_game_started:
            self.player.set_ship_coordinates(coordinates)
            return f"Ship with coordinates {coordinates} was added."
        raise StartedGameError("Cannot set a ship after game started")

    def start_game(self) -> dict:
        """Method starts a game after player's command if there is any ships."""
        if self.is_game_started:
            raise StartedGameError(f"Game with id {self.id} is already started.")
        if self.player.is_all_ships_added() and self.enemy.is_all_ships_added():
            self.is_game_started = True
            return {"message": "Game is started.", "is_player_move": self.is_player_move}
        raise NotStartedGameError("There are not all ships added. Cannot start a game.")
