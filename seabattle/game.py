"""Module with game class."""
import logging
import random
from typing import Tuple, List, Dict, Any
from uuid import UUID, uuid4
from seabattle.game_errors.game_errors import StartedGameError, NotStartedGameError, NotYourTurnError
from seabattle.game_objects.bot import EasyBot
from seabattle.game_objects.player import Player
from seabattle.helpers.constants import SignObjects
from seabattle.helpers.convertors import convert_coordinates
from seabattle.helpers.logger import get_logger


class Game:
    """Class with main game logic."""
    id: UUID
    logger: logging.Logger
    player: Player
    enemy: EasyBot
    is_game_started: bool
    is_player_move: bool

    def __init__(self):
        self.id = uuid4()
        self.logger = get_logger(game_id=self.id, name="seabattle_game")
        self.player = Player(player_name="Player", enemy_name="Enemy", logger=self.logger)
        self.enemy = EasyBot(player_name="Enemy", enemy_name="Player", logger=self.logger)
        self.is_game_started = False
        self.is_player_move = random.choice([True, False])
        self.is_game_over = False

    def _is_game_over(self):
        """Method checks if game for player is over based on its battlefield."""
        self.is_game_over = self.player.is_game_over or self.enemy.is_game_over
        if self.is_game_over:
            self.logger.info("Game is over.")

    def player_shoot(self, coordinate: Tuple[int, int]) -> dict:
        """
        Method processes player shoot command.
        Args:
            coordinate: Tuple with coordinate for shooting.

        Returns:
            Dictionary with current game state information.
        """
        self.logger.info(f"Try to make player shoot with coordinate {coordinate}.")
        if self.is_game_started:
            if self.is_player_move:
                shooting_results, is_killed = self.enemy.enemy_shooting(coordinate)
                if shooting_results[coordinate].sign != SignObjects.hit_sign.sign:
                    self.is_player_move = not self.is_player_move

                self.player.shoot(shooting_results, is_killed)
                self._is_game_over()

                return self.return_game_state()
            raise NotYourTurnError("Right now is not your turn for shooting.")
        raise NotStartedGameError("Game is not started. Cannot shooting.")

    def enemy_shoot(self) -> dict:
        """
        Method processes enemy shoot command.

        Returns:
            Dictionary with current game state information.
        """
        self.logger.info("Try to make enemy shoot.")
        if self.is_game_started:
            if not self.is_player_move:
                coordinate = self.enemy.choose_shooting_coordinate()
                self.logger.info(f"Use coordinate {coordinate} for shooting.")

                shooting_results, is_killed = self.player.enemy_shooting(coordinate)
                if shooting_results[coordinate].sign != SignObjects.hit_sign.sign:
                    self.is_player_move = not self.is_player_move

                self.enemy.shoot(shooting_results, is_killed)
                self._is_game_over()

                return self.return_game_state()

            raise NotYourTurnError("Right now is not your turn for shooting.")
        raise NotStartedGameError("Game is not started. Cannot shooting.")

    def player_set_ship(
            self, coordinates: List[Tuple[int, int]]
    ) -> Dict[str, List[Dict[str, str]] | Dict[str, int]]:
        """
        Method processes player set ship command.
        Args:
            coordinates: List of ship's cells coordinates.

        Returns:
            Dictionary with player ship information (coordinates and ship sign).
        """
        self.logger.info(f"Try to add ship with coordinates {coordinates}")
        if not self.is_game_started:
            ship_coordinates = self.player.set_ship_coordinates(coordinates)
            self.logger.info(f"Ship with coordinates {coordinates} was added.")
            return {
                "player_ship_cells": convert_coordinates(ship_coordinates),
                "player_fleet": self.player.player_battlefield.get_fleet_structure()
            }
        raise StartedGameError("Cannot set a ship after game started")

    def start_game(self) -> dict:
        """
        Method starts a game after player's command if there is all needed ships.

        Returns:
            Dictionary with current game state information.
        """
        self.logger.info("Try to start game.")
        if self.is_game_started:
            raise StartedGameError(f"Game with id {self.id} is already started.")
        if self.player.is_all_ships_added() and self.enemy.is_all_ships_added():
            self.logger.info("The game is started.")
            self.is_game_started = True
            return self.return_game_state()
        raise NotStartedGameError("There are not all ships added. Cannot start a game.")

    def return_game_state(self) -> Dict[str, Any]:
        """
        Method collects current game state information.
        Returns:
            Dictionary with current game state information.
        """
        winner = ""
        if self.player.is_game_over:
            winner = self.enemy.player_battlefield.name
        elif self.enemy.is_game_over:
            winner = self.player.player_battlefield.name
        return {
            "game_id": self.id,
            "player_id": self.player.id,
            "is_player_move": self.is_player_move,
            "is_game_over": self.is_game_over,
            "player_battle_field_cells": convert_coordinates(self.player.player_battlefield.get_battlefield()),
            "player_fleet": self.player.player_battlefield.get_fleet_structure(),
            "enemy_battle_field_cells": convert_coordinates(self.player.enemy_battlefield.get_battlefield()),
            "enemy_fleet": self.enemy.player_battlefield.get_fleet_structure(),
            "winner": winner
        }
