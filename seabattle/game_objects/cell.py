""""Module for creation cell objects."""
from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from seabattle.helpers.constants import SignObjects


@dataclass
class Cell:
    """Class contains cell object and its methods."""
    x: int
    y: int
    sign: str
    ship_id: Optional[UUID]

    def __init__(self, x: int, y: int, sign: str = SignObjects.empty_sign.sign):
        self.x = x
        self.y = y
        self.sign = sign
        self.ship_id = None

    def __repr__(self):
        return self.sign
