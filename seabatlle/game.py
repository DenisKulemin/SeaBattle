"""Module with main game cycle."""

from seabatlle.game_objects.board import GameBoard


def main() -> None:
    """Method with main game logic."""
    game_board = GameBoard()
    game_board.set_ship_coordinate([(1, 2), (2, 2)])
    game_board.set_ship_coordinate([(6, 4), (6, 5), (6, 6), (6, 7)])
    game_board.set_ship_coordinate([(4, 2), (4, 3), (4, 4)])


if __name__ == "__main__":
    main()
