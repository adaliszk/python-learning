from __future__ import annotations

from typing import Iterable, Iterator, Optional, TYPE_CHECKING

import numpy as np  # type: ignore
from tcod.console import Console

import tile_types

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity, Actor


class GameMap:
    def __init__(
            self, engine: Engine, width: int, height: int, entities: Iterable[Entity, Actor] = ()
    ):
        self.engine = engine
        self.width, self.height = width, height
        self.entities = set(entities)
        self.tiles = np.full((width, height), fill_value=tile_types.wall, order="F")

        self.visible = np.full(
            (width, height), fill_value=False, order="F"
        )  # Tiles the player can currently see.
        self.explored = np.full(
            (width, height), fill_value=False, order="F"
        )  # Tiles the player has seen before.

        self.tiles[30:33, 22] = tile_types.wall

    @property
    def actors(self) -> Iterator[Actor]:
        """Iterate over this maps living actors"""
        yield from (
            entity
            for entity in self.entities
            if hasattr(entity, "is_alive") and entity.is_alive
        )

    def get_blocking_entity_at_location(
            self, location_x: int, location_y: int
    ) -> Optional[Entity]:
        for entity in self.entities:
            if (
                    entity.blocks_movement
                    and entity.x == location_x
                    and entity.y == location_y
            ):
                return entity

        return None

    def get_actor_at_location(self, x: int, y: int) -> Optional[Actor]:
        for actor in self.actors:
            if actor.x == x and actor.y == y:
                return actor

        return None

    def in_bounds(self, x: int, y: int) -> bool:
        """Return True if x and y are inside the bounds of this map."""
        return 0 <= x < self.width and 0 <= y < self.height

    def render(self, console: Console) -> None:
        """
                Renders the map.

                If a tile is in the "visible" array, then draw it with the "light" colors.
                If it isn't, but it's in the "explored" array, then draw it with the "dark" colors.
                Otherwise, the default is "SHROUD".
                """
        console.tiles_rgb[0: self.width, 0: self.height] = np.select(
            condlist=[self.visible, self.explored],
            choicelist=[self.tiles["light"], self.tiles["dark"]],
            default=tile_types.SHROUD,
        )

        for entity in self.entities:
            if self.visible[entity.x, entity.y]:
                console.print(x=entity.x, y=entity.y, string=entity.char, fg=entity.color)