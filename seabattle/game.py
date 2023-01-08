"""Module with game class."""
import ast
from typing import Optional

from seabattle.game_errors.battlefield_errors import BaseBattleFieldError, ShotCellEarlierError
from seabattle.game_objects.player import Player


class Game:
    """Class with main game logic."""
    # TODO Replace prints with errors after adding api error handlers.

    def __init__(self):
        self.player = Player(player_name="Mike", enemy_name="Sailor")
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

    def player_shoot(self, coordinate: tuple) -> Optional[str]:
        """
        Method processes player shoot command.
        Args:
            coordinate: Tuple with coordinate for shooting.

        Returns:
            str: New sign after shooting for coordinate.
        """
        if self.game_starts:
            return self.player.shoot(coordinate)
        print("Game is not started. Cannot shooting.")
        return None

    def player_set_ship(self, coordinates: list[tuple]) -> bool:
        """
        Method processes player set ship command.
        Args:
            coordinates: List of ship's cells coordinates.

        Returns:
            bool: True if ship is set, else - False.
        """
        if not self.game_starts:
            self.player.set_ship_coordinates(coordinates)
            return True
        print("Game is started. Cannot add new ship.")
        return False

    def start_game(self):
        """Method starts a game after player's command if there is any ships."""
        if self.player.is_all_ships_added():
            self.game_starts = True
        else:
            print("There are not all ships added. Cannot start a game.")

    def main_player_loop(self):    # pragma: no cover
        """Main game loop for the interactive game through the terminal."""
        _ = self.player_set_ship([(1, 2), (2, 2)])
        _ = self.player_set_ship([(4, 4), (6, 6), (4, 6)])
        # TODO Delete adding ships to enemy, when bots will be created.
        self.player.enemy_battlefield.set_ship_coordinates([(1, 2), (2, 2)])
        self.player.enemy_battlefield.set_ship_coordinates([(4, 4), (6, 6), (4, 6)])
        command = self.get_command("Type your command (possible commands: set_ship, start_game, shoot, exit): ")
        while command != "exit":
            if (command == "set_ship") and not self.game_starts:
                try:
                    coordinates = ast.literal_eval(self.get_command("Type coordinates in format [(x, y), (x, y)]: "))
                    self.player_set_ship(coordinates)
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
                    _ = self.player_shoot(coordinate)
                except (ShotCellEarlierError, SyntaxError, TypeError) as exp:
                    print(exp)
            else:
                print(f"Unknown command: {command}")
            print(self.player)
            if not self.player.is_game_over:
                command = self.get_command("Type your command (possible commands: set_ship, start_game, shoot, exit): ")
            else:
                command = "exit"

        print("The game is over")


if __name__ == "__main__":    # pragma: no cover
    Game().main_player_loop()
