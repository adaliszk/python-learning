from dataclasses import dataclass
from typing import List, Any

from numpy.typing import NDArray
from numpy import select, full

import random

from framework import Canvas, Context, Scene, Screen

import tilemap
from procgen import RectangularRoom, tunnel_between
from color import White


@dataclass
class DungeonConfig:
    width: int
    height: int
    min_size: int = 6
    max_size: int = 10
    rooms: int = 4


class Dungeon(Scene):
    rooms: List[RectangularRoom] = []
    tiles: NDArray[Any]

    def __init__(self, screen: Screen):
        width = screen.inner_width
        height = screen.inner_height
        config = DungeonConfig(width, height)

        self.tiles = full((width, height), fill_value=tilemap.WALL, order="F")
        self.explored = full((width, height), fill_value=False, order="F")  # Tiles the player has seen before.
        self.visible = full((width, height), fill_value=False, order="F")  # Tiles the player can currently see.

        self.generate_dungeon(config)

    def generate_dungeon(self, config: DungeonConfig):
        for r in range(config.rooms):
            room_width = random.randint(config.min_size, config.max_size)
            room_height = random.randint(config.min_size, config.max_size)

            x = random.randint(0, config.width - room_width - 1)
            y = random.randint(0, config.height - room_height - 1)

            # "RectangularRoom" class makes rectangles easier to work with
            new_room = RectangularRoom(x, y, room_width, room_height)

            # Run through the other rooms and see if they intersect this one.
            if any(new_room.intersects(other_room) for other_room in self.rooms):
                continue  # This room intersects, so go to the next attempt.

            # if there are no intersects then the room is valid.
            # Dig out the rooms inner area.
            self.tiles[new_room.inner] = tilemap.FLOOR
            self.rooms.append(new_room)

    def on_render(self, canvas: Canvas, screen: Screen, **kwargs) -> None:
        # canvas.rgb[screen.inner_left: screen.inner_right, screen.inner_top] = White
        # canvas.rgb[screen.inner_left: screen.inner_right, screen.inner_bottom] = White
        # canvas.rgb[screen.inner_left, screen.inner_top: screen.inner_bottom] = White
        # canvas.rgb[screen.inner_right - 1, screen.inner_top: screen.inner_bottom] = White

        # canvas.rgb[0: screen.inner_width, 0: screen.inner_height] = select(
        #     condlist=[self.visible, self.explored],
        #     choicelist=[self.tiles["light"], self.tiles["dark"]],
        #     default=tilemap.FLOOR,
        # )

        for room in self.rooms:
            for x, y in tunnel_between(self.rooms[-1].center, room.center):
                canvas.rgb[x, y] = White

    def listen(self, context: Context):
        super().listen(context)
