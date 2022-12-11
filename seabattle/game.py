"""Module with game class."""
import ast

from seabattle.game_errors.battlefield_errors import BaseBattleFieldError, ShotCellEarlierError
from seabattle.game_objects.battlefield import BattleField


class Game:
    """Class with main game logic."""
    # TODO Replace prints with errors after adding api error handlers.

    def __init__(self):
        self.battlefield_area = BattleField()
        self.game_starts = False

    @staticmethod
    def get_command(prompt: str) -> str:
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
        """
        if self.game_starts:
            self.battlefield_area.shoot(coordinate)
        else:
            print("Game is not started. Cannot shooting.")

    def player_set_ship(self, coordinates: list[tuple]):
        """
        Method processes player set ship command.
        Args:
            coordinates: List of ship's cells coordinates.
        """
        if not self.game_starts:
            self.battlefield_area.set_ship_coordinates(coordinates)
        else:
            print("Game is started. Cannot add new ship.")

    def start_game(self):
        """Method starts a game after player's command if there is any ships."""
        # TODO Update method after adding constraints for ships quantity.
        if self.battlefield_area.ships:
            self.game_starts = True
        else:
            print("There is no ships for a game. Cannot start a game.")

    def main_player_loop(self):
        """Main game loop for the interactive game through the terminal."""
        self.player_set_ship([(1, 2), (2, 2)])
        self.player_set_ship([(4, 4), (6, 6), (4, 6)])
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
                    self.player_shoot(coordinate)
                except (ShotCellEarlierError, SyntaxError, TypeError) as exp:
                    print(exp)
            else:
                print(f"Unknown command: {command}")
            print(self.battlefield_area)
            if not self.battlefield_area.game_is_over:
                command = self.get_command("Type your command (possible commands: set_ship, start_game, shoot, exit): ")
            else:
                command = "exit"

        print("The game is over")


if __name__ == "__main__":
    Game().main_player_loop()
