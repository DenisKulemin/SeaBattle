"""Module contains player class."""
from seabattle.game_objects.battlefield import BattleField


class Player:
    """Class contains battlefields and rule them in a game."""
    name: str
    enemy_name: str
    player_battlefield: BattleField
    enemy_battlefield: BattleField
    is_game_over: bool

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

    def shoot(self, coordinate):
        """
        Method runs shoot command on enemy battlefield.
        Args:
            coordinate: Coordinate for shooting.
        """
        self.enemy_battlefield.shoot(coordinate)
        self._is_game_over()

    def set_ship_coordinates(self, coordinates):
        """
        Method sets ship signs with specified coordinates on player battlefield.
        Args:
            coordinates: List of coordinates.
        """
        self.player_battlefield.set_ship_coordinates(coordinates)
