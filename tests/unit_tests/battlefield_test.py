"""Module with unit tests for battlefield."""
import pytest

from seabattle.game_errors.battlefield_errors import BlockedAreaError, BlockedAreaAroundError, ShotCellEarlierError, \
    AreaOutsideBattleFieldError, CellNotExistError, ExtraShipInFleetError
from seabattle.game_errors.ship_errors import ShipError
from seabattle.game_objects.battlefield import BattleField
from seabattle.helpers.constants import SignObjects, SHIPS_COORDINATES


def test_set_ship_coordinate(battlefield):
    """
    Method tests correct work of set_ship_coordinates method.
    Args:
        battlefield: Battlefield object.
    """
    # Check if battlefield is not empty (from fixture), BattleField(name="Mike") created empty.
    assert battlefield != BattleField(name="Mike")


@pytest.mark.parametrize(
    ("coordinates", "error"), [
        # Method raises AreaOutsideBattleFieldError if used coordinates is outside the battlefield.
        ([(50, -1)], AreaOutsideBattleFieldError),
        # Method couldn't set a new ship in one cell perimeter around other ship
        ([(2, 3), (3, 3)], BlockedAreaAroundError),
        # Method couldn't set a new ship in one cell perimeter around other ship.
        ([(1, 1), (1, 2)], BlockedAreaError),
        # Method raises TypeError if used wrong coordinate format.
        ((3, 3), TypeError),
        # Method raises ExtraShipInFleetError if there are no more ships with that size can be added.
        ([(10, 1), (10, 2), (10, 3), (10, 4), (10, 5)], ExtraShipInFleetError),
        # Method raises BaseShipError if we set coordinates that cannot be used for building a ship.
        ([(10, 10), (9, 9)], ShipError)
    ]
)
def test_set_ship_coordinate_raised_error(battlefield, coordinates, error):
    """
    Method tests if battlefield raises error if coordinates are wrong.
    Args:
        battlefield: Battlefield object.
        coordinates: List of coordinates.
        error: Error class that should be raised.
    """
    with pytest.raises(error):
        battlefield.set_ship_coordinates(coordinates)


@pytest.mark.parametrize(
    ("coordinate", "sign"), [
        ((1, 2), SignObjects.hit_sign.sign),  # Sign after successful shooting is correct.
        ((3, 3), SignObjects.miss_sign.sign)  # Sign after miss shooting is correct.
    ]
)
def test_shoot_is_correct(battlefield, coordinate, sign):
    """
    Method tests correct work of shoot method.
    Args:
        battlefield: Battlefield object.
    """
    # Check if sign after successful shooting is correct.
    battlefield.shoot(coordinate)
    assert battlefield.battlefield[coordinate].sign == sign


def test_shoot_twice_in_one_place(battlefield):
    """
    Method tests battlefield raises ShotCellEarlierError if shoot twice in one place.
    Args:
        battlefield: Battlefield object.
    """
    battlefield.shoot((1, 2))
    with pytest.raises(ShotCellEarlierError):
        battlefield.shoot((1, 2))


def test_shoot_not_existing_coordinates(battlefield):
    """
    Method tests that battlefield raises CellNotExistError if coordinates are not exists.
    Args:
        battlefield: Battlefield object.
    """
    with pytest.raises(CellNotExistError):
        battlefield.shoot((50, 50))


def test_shoot_border_coordinates(battlefield):
    """
    Method tests that battlefield raises AreaOutsideBattleFieldError if coordinates are belongs to battlefield boarder.
    Args:
        battlefield: Battlefield object.
    """
    with pytest.raises(AreaOutsideBattleFieldError):
        battlefield.shoot((0, 0))


@pytest.mark.parametrize(
    ("coordinate", "sign", "result"), [
        # Line has 19 signs: 10 - cells signs and 9 - whitespaces between them.
        ((10, 10), SignObjects.empty_sign.sign, "0                  \n"
                                                "0                  \n"
                                                "                   \n"
                                                "                   \n"
                                                "                   \n"
                                                "                   \n"
                                                "                   \n"
                                                "                   \n"
                                                "                   \n"
                                                "                   "),
        ((1, 3), SignObjects.ship_sign.sign, "0                  \n"
                                             "0                  \n"
                                             "0                  \n"
                                             "                   \n"
                                             "                   \n"
                                             "                   \n"
                                             "                   \n"
                                             "                   \n"
                                             "                   \n"
                                             "                   "),
        ((5, 5), SignObjects.miss_sign.sign, "0                  \n"
                                             "0                  \n"
                                             "                   \n"
                                             "                   \n"
                                             "        *          \n"
                                             "                   \n"
                                             "                   \n"
                                             "                   \n"
                                             "                   \n"
                                             "                   "),
        ((1, 2), SignObjects.hit_sign.sign, "0                  \n"
                                            "X                  \n"
                                            "                   \n"
                                            "                   \n"
                                            "                   \n"
                                            "                   \n"
                                            "                   \n"
                                            "                   \n"
                                            "                   \n"
                                            "                   "),
    ]
)
def test_player_battlefield_repr(battlefield, coordinate, sign, result):
    """Method checks if player battlefield printing in console works correct."""
    battlefield.battlefield[coordinate].sign = sign
    assert repr(battlefield) == result


def test_enemy_battlefield_repr():
    """Method checks if enemy battlefield printing in console works correct."""
    battlefield = BattleField(name="Sailor", is_visible=False)
    # Check battlefield with ship mark. Player shouldn't see enemy's ships.
    battlefield.battlefield.get((1, 2)).sign = SignObjects.ship_sign.sign
    assert repr(battlefield) == \
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


def test_create_initial_ships():
    """Method test battlefield creates the correct list of ships lengths."""
    battlefield = BattleField(name="Sailor", is_visible=False)
    assert battlefield.create_initial_ships() == [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]


def test_all_ships_added_correct():
    """Method tests that battlefield returns correct bool value if all ships or not."""
    battlefield = BattleField(name="Sailor", is_visible=False)

    # Check before adding the ship. Until we add all ships, should be false.
    for ship_coordinate in SHIPS_COORDINATES:
        assert not battlefield.is_all_ships_added()
        battlefield.set_ship_coordinates(ship_coordinate)

    # After adding the last ship, should be true.
    assert battlefield.is_all_ships_added()
