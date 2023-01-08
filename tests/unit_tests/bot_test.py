"""Module contains tests for Bot objects."""
from copy import deepcopy

from seabattle.game_objects.bot import EasyBot


def test_choose_shooting_coordinate():
    """
    Method tests that choose_shooting_coordinate returns tuple with coordinate
    and delete them from the list of possible coordinates for shooting.
    """
    bot = EasyBot(player_name="Sailor", enemy_name="Mike")
    coordinates_for_shooting = deepcopy(bot.coordinates_for_shooting)
    coordinate = bot.choose_shooting_coordinate()
    assert isinstance(coordinate, tuple)
    assert coordinate in coordinates_for_shooting
    assert coordinate not in bot.coordinates_for_shooting


def test_all_ships_have_correct_size():
    """Method tests that all bot ships were added correct number of ships with correct sizes."""
    bot = EasyBot(player_name="Sailor", enemy_name="Mike")
    ships_lens = bot.player_battlefield.create_initial_ships()
    assert len(bot.player_battlefield.ships) == len(ships_lens)
    for ship_len in set(ships_lens):
        assert len([1 for ship in bot.player_battlefield.ships if len(ship.ship) == ship_len]) \
               == ships_lens.count(ship_len)
