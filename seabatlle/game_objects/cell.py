""""Module for creation cell objects."""
from dataclasses import dataclass

from seabatlle.helpers.constants import SignObjects


@dataclass
class Cell:
    """Class contains cell object and its methods."""

    def __init__(self, x: int, y: int, sign: str = SignObjects.empty_sign.sign):
        self.x = x
        self.y = y
        self.sign = sign

    def __repr__(self):
        return self.sign
