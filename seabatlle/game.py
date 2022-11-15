"""Module with main game cycle."""
import ast

from seabatlle.game_errors.board_errors import BlockedAreaError, BlockedAreaAroundError, ShotCellEarlierError
from seabatlle.game_objects.board import GameBoard


def main() -> None:
    """Method with main game logic."""
    command = input("Type your command (possible commands: set_ship, start_game, shoot, exit): ")
    game_board = GameBoard()
    game_starts = False
    while command != "exit":
        if (command == "set_ship") and not game_starts:
            try:
                coordinates = ast.literal_eval(input("Type coordinates in format [(x, y), (x, y)]: "))
                game_board.set_ship_coordinate(coordinates)
            except (BlockedAreaError, BlockedAreaAroundError, SyntaxError) as exp:
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
                game_board.shoot(coordinate)
            except (ShotCellEarlierError, SyntaxError) as exp:
                print(exp)
        else:
            print(f"Unknown command: {command}")
        print(game_board)
        if not game_board.game_is_over:
            command = input("Type your command (possible commands: set_ship, start_game, shoot, exit): ")
        else:
            command = "exit"

    print("The game is over")


if __name__ == "__main__":
    main()
