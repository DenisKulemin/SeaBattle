"""Module contains test for player class."""
from seabattle.game_objects.player import Player
from seabattle.helpers.constants import SignObjects


def test_empty_player_repr():
    """Method tests player text representation for emtpy battlefields."""

    # pylint: disable=duplicate-code

    player = Player(player_name="Mike", enemy_name="Sailor")
    assert repr(player) == "------------Mike's battlefield---------\n" \
                           "                   \n" \
                           "                   \n" \
                           "                   \n" \
                           "                   \n" \
                           "                   \n" \
                           "                   \n" \
                           "                   \n" \
                           "                   \n" \
                           "                   \n" \
                           "                   \n" \
                           "------------Sailor's battlefield---------\n" \
                           "                   \n" \
                           "                   \n" \
                           "                   \n" \
                           "                   \n" \
                           "                   \n" \
                           "                   \n" \
                           "                   \n" \
                           "                   \n" \
                           "                   \n" \
                           "                   "


def test_player_repr():
    """Method tests player text representation with some sings."""

    # pylint: disable=duplicate-code

    player = Player(player_name="Mike", enemy_name="Sailor")
    # Set ship sign on player battlefield. Should be visible.
    player.player_battlefield.battlefield[(1, 1)].sign = SignObjects.ship_sign.sign
    # Set ship sign on enemy battlefield. Shouldn't be visible.
    player.enemy_battlefield.battlefield[(1, 1)].sign = SignObjects.ship_sign.sign
    # Set miss sign on player battlefield. Should be visible.
    player.player_battlefield.battlefield[(1, 2)].sign = SignObjects.miss_sign.sign
    # Set hit sign on player battlefield. Should be visible.
    player.player_battlefield.battlefield[(1, 3)].sign = SignObjects.hit_sign.sign

    assert repr(player) == "------------Mike's battlefield---------\n" \
                           "0                  \n" \
                           "*                  \n" \
                           "X                  \n" \
                           "                   \n" \
                           "                   \n" \
                           "                   \n" \
                           "                   \n" \
                           "                   \n" \
                           "                   \n" \
                           "                   \n" \
                           "------------Sailor's battlefield---------\n" \
                           "                   \n" \
                           "                   \n" \
                           "                   \n" \
                           "                   \n" \
                           "                   \n" \
                           "                   \n" \
                           "                   \n" \
                           "                   \n" \
                           "                   \n" \
                           "                   "
