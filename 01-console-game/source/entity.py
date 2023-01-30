from dataclasses import dataclass

import copy
from typing import Tuple, TYPE_CHECKING
from game_map import GameMap


@dataclass
class Entity:
    """
    A generic object to represent players, enemies, items, etc.
    """
    id: int = 0
    x: int = 0
    y: int = 0
    char: chr = "?"
    color: Tuple[int, int, int] = (255, 255, 255)
    name: str = "<Unnamed>"
    blocks_movement: bool = False

    def __hash__(self) -> int:
        return self.id

    def spawn(self, gamemap: GameMap, x: int, y: int):
        """Spawn a copy of this instance at the given location."""
        clone = copy.deepcopy(self)
        clone.x = x
        clone.y = y
        gamemap.entities.add(clone)
        return clone

    def move(self, dx: int, dy: int, ) -> None:
        # Move the entity by a given amount
        self.x += dx
        self.y += dy
