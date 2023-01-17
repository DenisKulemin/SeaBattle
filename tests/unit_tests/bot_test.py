"""Module contains tests for Bot objects."""
from seabattle.game_objects.bot import EasyBot


def test_all_ships_have_correct_size():
    """Method tests that all bot ships were added correct number of ships with correct sizes."""
    bot = EasyBot(player_name="Sailor", enemy_name="Mike")
    ships_lens = bot.player_battlefield.create_initial_ships()
    assert len(bot.player_battlefield.ships) == len(ships_lens)
    for ship_len in set(ships_lens):
        assert len([1 for ship in bot.player_battlefield.ships.values() if len(ship.ship) == ship_len]) \
               == ships_lens.count(ship_len)
