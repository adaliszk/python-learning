from __future__ import annotations

from typing import Optional, TYPE_CHECKING

import tcod.event

from actions import Action, BumpAction, EscapeAction

if TYPE_CHECKING:
    from engine import Engine


class EventHandler(tcod.event.EventDispatch[Action]):
    # We’re creating a class called EventHandler,
    # which is a subclass of tcod’s EventDispatch class.
    # EventDispatch is a class that allows us to send an event to its proper method based on what type of event it is.

    def __init__(self, engine: Engine):
        self.engine = engine

    def handle_events(self, context: tcod.context.Context) -> None:
        for event in tcod.event.wait():
            context.convert_event(event)
            self.dispatch(event)

    def ev_mousemotion(self, event: tcod.event.MouseMotion) -> None:
        if self.engine.game_map.in_bounds(event.tile.x, event.tile.y):
            self.engine.mouse_location = event.tile.x, event.tile.y

     # TODO fix runtime error after death. ` uninitialized tiles. pass through `Context.convert_event`

    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        raise SystemExit()

    def on_render(self, console: tcod.Console) -> None:
        self.engine.render(console)


class MainGameEventHandler(EventHandler):
    def handle_events(self, context: tcod.context.Context) -> None:
        for event in tcod.event.wait():
            context.convert_event(event)

            action = self.dispatch(event)

            if action is None:
                continue

            action.perform()

            self.engine.handle_enemy_turns()
            self.engine.update_fov()  # Update the FOV before the players next action.

    # using a method of EventDispatch: ev_quit is a method defined in EventDispatch,
    # which we’re overriding in EventHandler.
    # ev_quit is called when we receive a “quit” event,
    # which happens when we click the “X” in the window of the program.
    # In that case, we want to quit the program, so we raise SystemExit() to do so.

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        player = self.engine.player

        match event.sym:
            case tcod.event.K_UP:
                return BumpAction(player, dx=0, dy=-1)
            case tcod.event.K_DOWN:
                return BumpAction(player, dx=0, dy=1)
            case tcod.event.K_LEFT:
                return BumpAction(player, dx=-1, dy=0)
            case tcod.event.K_RIGHT:
                return BumpAction(player, dx=1, dy=0)
            case tcod.event.K_w:
                return BumpAction(player, dx=0, dy=-1)
            case tcod.event.K_s:
                return BumpAction(player, dx=0, dy=1)
            case tcod.event.K_a:
                return BumpAction(player, dx=-1, dy=0)
            case tcod.event.K_d:
                return BumpAction(player, dx=1, dy=0)
            case tcod.event.K_ESCAPE:
                return EscapeAction()


# TODO add diagonal walk and uninterrupted direction change.

class GameOverEventHandler(EventHandler):
    def handle_events(self, context: tcod.context.Context) -> None:
        for event in tcod.event.wait():
            action = self.dispatch(event)

            if action is None:
                continue

            action.perform()
