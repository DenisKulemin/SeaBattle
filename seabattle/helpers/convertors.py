"""Module contains functions for converting data before send them to front."""
from typing import Dict, Tuple, List

from seabattle.game_objects.cell import Cell
from seabattle.helpers.constants import DEFAULT_BATTLEFIELD_BEGINNING_COORD, DEFAULT_BATTLEFIELD_END_COORD


def convert_coordinates(coordinates: Dict[Tuple[int, int], Cell]) -> List[Dict[str, str]]:
    """
    Method converts coordinates and cells information into dictionary.
    Args:
        coordinates: Dictionary with tuple coordinates as keys and cell object as values.

    Returns:
        Dictionary with x, y and sign keys, and its values.
    """
    return [{"x": str(coord[0]), "y": str(coord[1]), "sign": cell.sign}
            for coord, cell in coordinates.items()
            if DEFAULT_BATTLEFIELD_BEGINNING_COORD < coord[0] < DEFAULT_BATTLEFIELD_END_COORD
            and DEFAULT_BATTLEFIELD_BEGINNING_COORD < coord[1] < DEFAULT_BATTLEFIELD_END_COORD]
