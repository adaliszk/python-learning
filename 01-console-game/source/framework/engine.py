from typing import Tuple, Any

from numpy.typing import NDArray
from numpy import array, dtype, int32, bool_

from tcod.console import Console as Canvas

from .screen import Screen
from .scene import Scene



# Tile graphics structured type compatible with console.tiles_rgb.
GRAPHIC = dtype(
    [
        ("ch", int32),  # unicode codepoint
        ("fg", "3B"),  # 3 unsigned bytes, for RGB colors
        ("bg", "3B"),
    ]
)

# tile struct used for statically defined tile data
TILE = dtype(
    [
        ("walkable", bool_),  # True if this tile can be walked over.
        ("transparent", bool_),  # True if this tile doesn't block FOV
        ("dark", GRAPHIC),  # Graphics for when this tile is not in FOV.
        ("light", GRAPHIC),  # Graphics for when the tile is in FOV.
    ]
)


def new_tile(
        *,  # Enforce the use of keywords, so that parameter order doesn't matter.
        walkable: int,
        transparent: int,
        dark: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
        light: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
) -> NDArray:
    """Helper function for defining individual tile types """
    return array((walkable, transparent, dark, light), dtype=TILE)


class Engine:
    _screen: Screen
    _scene: Scene

    def __init__(self, screen: Screen, scene: Scene, canvas: Canvas):
        self._canvas = canvas
        self._screen = screen
        self._scene = scene

    @property
    def screen(self):
        return self._screen

    @property
    def scene(self):
        return self._scene

    def render(self, **kwargs: NDArray[Any]):

        for tile in kwargs.get('center'):
            print(tile)

        # self._canvas.rgb[self.screen.inner_left: self.screen.inner_right, self.screen.inner_top: self.screen.inner_bottom] =
