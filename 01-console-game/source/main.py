from framework import Screen, Engine
from tcod.console import Console
from tcod.tileset import CHARMAP_TCOD, load_tilesheet
from tcod.context import new_terminal

from scenes import Dungeon


def main() -> None:
    screen = Screen(180, 120)
    tiles = load_tilesheet("resources/dejavu10x10_gs_tc.png", 32, 8, CHARMAP_TCOD)
    canvas = Console(screen.width, screen.height, order="F")
    scene = Dungeon(screen)
    engine = Engine(screen, scene, canvas)

    with new_terminal(screen.width, screen.height, tileset=tiles, title="MY ROUGE GAME", vsync=True) as context:
        while True:
            canvas.clear()
            engine.scene.on_render(engine=engine, screen=screen)
            context.present(canvas)
            engine.scene.listen(context)


if __name__ == "__main__":
    main()
