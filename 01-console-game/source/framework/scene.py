from typing import Optional

from tcod.context import Context
from tcod.event import EventDispatch, Quit
from tcod.console import Console
from tcod.event import wait

from .screen import Screen
from .action import Action


class Scene(EventDispatch[Action]):
    
    def __init__(self, screen: Screen):
        pass

    def ev_quit(self, event: Quit) -> Optional[Action]:
        raise SystemExit()

    def on_render(self, engine: Console, screen: Screen) -> None:
        raise NotImplemented

    def listen(self, context: Context):
        for event in wait():
            context.convert_event(event)
            action = self.dispatch(event)

            if action is None:
                continue

            action.perform()
