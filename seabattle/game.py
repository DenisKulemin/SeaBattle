"""Module with game class."""
import ast
from typing import Optional

from seabattle.game_errors.battlefield_errors import BaseBattleFieldError, ShotCellEarlierError, ExtraShipInFleetError
from seabattle.game_errors.ship_errors import BaseShipError
from seabattle.game_objects.bot import EasyBot
from seabattle.game_objects.player import Player
from seabattle.helpers.constants import SHIPS_COORDINATES


class Game:
    """Class with main game logic."""
    # TODO Replace prints with errors after adding api error handlers.

    def __init__(self):
        self.player = Player(player_name="Mike", enemy_name="Sailor")
        self.enemy = EasyBot(player_name="Sailor", enemy_name="Mike")
        self.game_starts = False

    @staticmethod
    def get_command(prompt: str) -> str:    # pragma: no cover
        """
        Method gets user input and returns it for processing.
        Args:
            prompt: String with a hint for user about current input request.
        Returns:
            String with user input.
        """
        return input(prompt)

    def player_shoot(self, coordinate: tuple):
        """
        Method processes player shoot command.
        Args:
            coordinate: Tuple with coordinate for shooting.

        Returns:
            str: New sign after shooting for coordinate.
        """
        if self.game_starts:
            shooting_result = self.enemy.enemy_shooting(coordinate)
            self.player.shoot(coordinate, shooting_result)
        else:
            print("Game is not started. Cannot shooting.")

    def enemy_shoot(self):
        """
        Method processes enemy shoot command.

        Returns:
            str: New sign after shooting for coordinate.
        """
        if self.game_starts:
            coordinate = self.enemy.choose_shooting_coordinate()
            shooting_result = self.player.enemy_shooting(coordinate)
            self.enemy.shoot(coordinate, shooting_result)
        else:
            print("Game is not started. Cannot shooting.")

    def player_set_ship(self, coordinates: list[tuple]) -> Optional[bool]:
        """
        Method processes player set ship command.
        Args:
            coordinates: List of ship's cells coordinates.

        Returns:
            bool: True if ship is set, else - False.
        """
        if not self.game_starts:
            try:
                self.player.set_ship_coordinates(coordinates)
                return True
            except (ExtraShipInFleetError, BaseShipError):
                print("Couldn't add new ship.")
                return None
        print("Game is started. Cannot add new ship.")
        return False

    def start_game(self):
        """Method starts a game after player's command if there is any ships."""
        if self.player.is_all_ships_added() and self.enemy.is_all_ships_added():
            self.game_starts = True
        else:
            print("There are not all ships added. Cannot start a game.")

    def main_player_loop(self):  # pragma: no cover
        """Main game loop for the interactive game through the terminal."""
        # TODO Remove for read game.
        for coordinates in SHIPS_COORDINATES:
            _ = self.player_set_ship(coordinates)
        command = self.get_command("Type your command (possible commands: set_ship, start_game, shoot, exit): ")
        while command != "exit":
            if (command == "set_ship") and not self.game_starts:
                try:
                    coordinates = ast.literal_eval(self.get_command("Type coordinates in format [(x, y), (x, y)]: "))
                    _ = self.player_set_ship(coordinates)
                except (BaseBattleFieldError, SyntaxError, TypeError) as exp:
                    print(exp)
            elif (command == "set_ship") and self.game_starts:
                print("Game is started. Cannot add new ship.")
            elif command == "start_game":
                self.start_game()
            elif (command == "shoot") and not self.game_starts:
                print("Game is not started. Cannot shooting.")
            elif (command == "shoot") and self.game_starts:
                try:
                    coordinate = ast.literal_eval(self.get_command("Type coordinate for shooting in format (x, y): "))
                    self.player_shoot(coordinate)
                except (ShotCellEarlierError, SyntaxError, TypeError) as exp:
                    print(exp)
            else:
                print(f"Unknown command: {command}")
            print(self.player)
            print("Enemy shooting!")
            self.enemy_shoot()
            print(self.player)
            if not self.player.is_game_over or self.enemy.is_game_over:
                command = self.get_command("Type your command (possible commands: set_ship, start_game, shoot, exit): ")
            else:
                command = "exit"

        print("The game is over")


if __name__ == "__main__":    # pragma: no cover
    Game().main_player_loop()
