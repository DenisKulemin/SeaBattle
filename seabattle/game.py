"""Module with main game cycle."""
import ast

from seabattle.game_errors.battlefield_errors import BaseBattleFieldError, ShotCellEarlierError
from seabattle.game_objects.battlefield import BattleField


def main() -> None:
    """Method with main game logic."""
    command = input("Type your command (possible commands: set_ship, start_game, shoot, exit): ")
    battlefield_area = BattleField()
    game_starts = False

    battlefield_area.set_ship_coordinate([(1, 2), (2, 2)])
    battlefield_area.set_ship_coordinate([(4, 4), (6, 6), (4, 6)])

    while command != "exit":
        if (command == "set_ship") and not game_starts:
            try:
                coordinates = ast.literal_eval(input("Type coordinates in format [(x, y), (x, y)]: "))
                battlefield_area.set_ship_coordinate(coordinates)
            except (BaseBattleFieldError, SyntaxError, TypeError) as exp:
                print(exp)
        elif (command == "set_ship") and game_starts:
            print("Game is started. Cannot add new ship.")
        elif command == "start_game":
            game_starts = True
        elif (command == "shoot") and not game_starts:
            print("Game is not started. Cannot shooting.")
        elif (command == "shoot") and game_starts:
            try:
                coordinate = ast.literal_eval(input("Type coordinate for shooting in format (x, y): "))
                battlefield_area.shoot(coordinate)
            except (ShotCellEarlierError, SyntaxError, TypeError) as exp:
                print(exp)
        else:
            print(f"Unknown command: {command}")
        print(battlefield_area)
        if not battlefield_area.game_is_over:
            command = input("Type your command (possible commands: set_ship, start_game, shoot, exit): ")
        else:
            command = "exit"

    print("The game is over")


if __name__ == "__main__":
    main()
