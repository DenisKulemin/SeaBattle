"""Module contains test for player class."""
from copy import deepcopy
from unittest.mock import patch

import pytest

from seabattle.game_objects.player import Player
from seabattle.helpers.constants import SignObjects


def test_empty_player_repr(player):
    """
    Method tests player text representation for emtpy battlefields.
    Args:
        player: Player object.
    """

    # pylint: disable=duplicate-code

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


def test_player_repr(player):
    """
    Method tests player text representation with some sings.
    Args:
        player: Player object.
    """

    # pylint: disable=duplicate-code

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


@pytest.mark.parametrize(
    ("shooting_results", "is_killed"), [
        ({(1, 1): SignObjects.hit_sign.sign, (1, 2): SignObjects.miss_sign.sign}, True),
        ({(1, 1): SignObjects.hit_sign.sign, (1, 2): SignObjects.miss_sign.sign}, False),
        ({(1, 1): SignObjects.miss_sign.sign}, True),
        ({(1, 1): SignObjects.miss_sign.sign}, False)
    ]
)
@patch("seabattle.game_objects.player.Player.define_top_target_coordinates")
@patch("seabattle.game_objects.player.Player.clear_coordinates_for_shooting")
def test_shoot(clear_func, define_func, player, shooting_results, is_killed):
    """
    Method checks if shoot player's method correctly set new signs for cells.
    Args:
        clear_func: Mock the call clear_coordinates_for_shooting function.
        define_func: Mock the call define_top_target_coordinates function.
        player: Player object.
        shooting_results: Dictionary with coordinates as keys and sings of shooting result on enemy battlefield
            as values.
        is_killed: Bool mark, that informs if the ship is sunk.
    """
    clear_func.return_value = None
    define_func.return_value = None
    player = Player(player_name="Mike", enemy_name="Sailor")

    # We don't add ships, so all cells should be empty.
    for coordinate in shooting_results.keys():
        assert player.enemy_battlefield.battlefield[coordinate].sign == SignObjects.empty_sign.sign
    player.shoot(shooting_results, is_killed)
    # Check that all cells from shooting_results were updated.
    for coordinate, sign in shooting_results.items():
        assert player.enemy_battlefield.battlefield[coordinate].sign == sign
        if sign == SignObjects.hit_sign.sign:
            assert player.demaged_ships_coordinates == [coordinate]


@pytest.mark.parametrize(
    ("test_input",), [
        (((1, 1), SignObjects.hit_sign.sign, True),),
        (((1, 1), SignObjects.hit_sign.sign, False),),
        (((1, 1), SignObjects.miss_sign.sign, True),),
        (((1, 1), SignObjects.miss_sign.sign, False),)
    ]
)
@patch("seabattle.game_objects.player.Player.set_sings_for_lucky_shoot")
@patch("seabattle.game_objects.battlefield.BattleField.shoot")
def test_enemy_shooting(shoot_func, set_func, player, test_input):
    """
    Method checks if enemy_shooting player's method correctly set new signs for cells.
    Args:
        shoot_func: Mock the call shoot function.
        set_func: Mock the call set_sings_for_lucky_shoot function.
        player: Player object.
        test_input: Tuple with: Coordinate for shooting; Sign shooting result on enemy battlefield; and Bool mark,
            that informs if the ship is sunk.
    """
    coordinate, shooting_results, is_killed = test_input
    shoot_func.return_value = ({coordinate: shooting_results}, is_killed)
    set_func.return_value = {coordinate: shooting_results}

    assert shooting_results, is_killed == player.enemy_shooting(coordinate)


def test_choose_shooting_coordinate(player):
    """
    Method tests that choose_shooting_coordinate returns tuple with coordinate
    and delete them from the list of possible coordinates for shooting.
    Args:
        player: Player object.
    """
    coordinates_for_shooting = deepcopy(player.coordinates_for_shooting)
    coordinate = player.choose_shooting_coordinate()
    assert isinstance(coordinate, tuple)
    assert coordinate in coordinates_for_shooting
    assert coordinate not in player.coordinates_for_shooting


@pytest.mark.parametrize(
    ("coordinate", "demaged_ships_coordinates", "is_killed", "result"), [
        ((1, 1), [(1, 1)], True, []),
        ((1, 1), [(1, 1)], False, [(0, 1), (2, 1), (1, 0), (1, 2)]),
        ((1, 1), [(1, 1), (1, 2)], True, []),
        # vertical ship with no previous top_target, return only vertical coordinates.
        ((1, 1), [(1, 1), (1, 2)], False, [(1, 0), (1, 2)]),
        ((1, 1), [(1, 1), (2, 1)], True, []),
        # horizontal ship with no previous top_target, return only horizontal coordinates.
        ((1, 1), [(1, 1), (2, 1)], False, [(0, 1), (2, 1)])
    ]
)
def test_define_top_target_coordinates(player, coordinate, demaged_ships_coordinates, is_killed, result):
    """
    Method tests that define_top_target_coordinates works correctly.
    Args:
        player: Player object.
        coordinate: Coordinate that was used for shooting right now.
        demaged_ships_coordinates: List of coordinates for previously demaged cells in this ship.
        is_killed: Boolean mark. True, if ship was sunk.
        result: Value that should have top_target_coordinates attribute.
    """

    player.demaged_ships_coordinates = demaged_ships_coordinates
    player.define_top_target_coordinates(coordinate, is_killed)
    assert player.top_target_coordinates == result


@pytest.mark.parametrize(
    ("top_target_coordinates", "coordinates"), [
        ([(1, 1), (1, 2)], [(1, 1), (1, 3)]),
        ([], [(1, 1), (1, 3)])
    ]
)
def test_clear_coordinates_for_shooting(player, top_target_coordinates, coordinates):
    """
    Method tests that clear_coordinates_for_shooting method deletes all coordinates from all shooting lists.
    Args:
        player: Player object.
        top_target_coordinates: List with coordinates for first shooting (possible ship coordinates).
        coordinates: List of coordinates for deleting.
    """

    # Initial player has all coordinates in coordinates_for_shooting attribute.
    player.top_target_coordinates = top_target_coordinates
    player.clear_coordinates_for_shooting(coordinates)

    for coordinate in coordinates:
        assert coordinate not in player.coordinates_for_shooting
        assert coordinate not in player.top_target_coordinates


@pytest.mark.parametrize(
    ("ship_coordinates", "coordinate", "is_killed", "result"), [
        ([(1, 1)], (1, 1), True, [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]),
        ([(1, 1), (1, 2)], (1, 1), False, [(0, 0), (0, 2), (1, 1), (2, 0), (2, 2)])
    ]
)
def test_get_coordinates_for_update(player, ship_coordinates, coordinate, is_killed, result):
    """
    Method tests that get_coordinates_for_update method creates coordinates around the cell/ship that should
    be updated after successful shooting.
    Args:
        player: Player object.
        ship_coordinates: Coordinates for setting a ship.
        coordinate: Shooting coordinate.
        is_killed: Boolean mark. True, if ship was sunk.
        result: get_coordinates_for_update output.
    """

    # Initial player has all coordinates in coordinates_for_shooting attribute.
    player.player_battlefield.set_ship_coordinates(ship_coordinates)
    assert set(player.get_coordinates_for_update(player.player_battlefield, coordinate, is_killed)) == set(result)


@pytest.mark.parametrize(
    ("get_mock", "coordinate", "is_killed"), [
        ([(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)], (1, 1), True),
        ([(0, 0), (0, 2), (1, 1), (2, 0), (2, 2)], (1, 1), False),
    ]
)
@patch("seabattle.game_objects.player.Player.get_coordinates_for_update")
def test_set_sings_for_lucky_shoot(get_func, player, get_mock, coordinate, is_killed):
    """
    Method checks if set_sings_for_lucky_shoot player's method correctly set miss signs for area around the
    demaged ship.
    Args:
        get_func: Mock the call get_coordinates_for_update function.
        player: Player object.
        coordinate: Coordinate for shooting.
        is_killed: Bool mark, that informs if the ship is sunk.
    """
    get_func.return_value = get_mock
    player.set_sings_for_lucky_shoot(player.player_battlefield, coordinate, is_killed)

    # As we have no shooting and ships, all coordinates for updates will be marked as miss_sign.
    # hit_sign tested in shoot function.
    for x, y in get_mock:
        assert player.player_battlefield.battlefield[(x, y)].sign == SignObjects.miss_sign.sign
