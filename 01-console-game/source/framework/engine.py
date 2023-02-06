from .screen import Screen
from .scene import Scene


class Engine:
    _screen: Screen
    _scene: Scene

    def __init__(self, screen: Screen, scene: Scene):
        self._screen = screen
        self._scene = scene

    @property
    def screen(self):
        return self._screen

    @property
    def scene(self):
        return self._scene
