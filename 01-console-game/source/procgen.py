import random
from typing import Iterator, Tuple

import tcod


class RectangularRoom:

    def __init__(self, x: int, y: int, width: int, height: int):
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height

    @property
    def center(self) -> Tuple[int, int]:
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)

        return center_x, center_y

    @property
    def inner(self) -> Tuple[slice, slice]:
        """Return the inner area of this room as a 2d array index"""
        return slice(self.x1 + 1, self.x2), slice(self.y1 + 1, self.y2)

    def intersects(self, other) -> bool:
        """Return True if this room overlaps with another room."""
        return (
                self.x1 <= other.x2
                and self.x2 >= other.x1
                and self.y1 <= other.y2
                and self.y2 >= other.y1
        )


def tunnel_between(start: Tuple[int, int], end: Tuple[int, int]) -> Iterator[Tuple[int, int]]:
    """Return an L-shape tunnel between these two points"""
    x1, y1 = start
    x2, y2 = end
    if random.random() < 0.5:  # 50% chance
        # Move horizontally, then vertically.
        corner_x, corner_y = x2, y1
    else:
        # Move vertically then horizontally.
        corner_x, corner_y = x1, y2

    # Generate the coordinates for this tunnel.
    for x, y in tcod.los.bresenham((x1, y1), (corner_x, corner_y)).tolist():
        yield x, y
    for x, y in tcod.los.bresenham((corner_x, corner_y), (x2, y2)).tolist():
        yield x, y
