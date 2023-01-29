from typing import Optional

import tcod.event

from actions import Action, EscapeAction, MovementAction


class EventHandler(tcod.event.EventDispatch[Action]):
    # We’re creating a class called EventHandler,
    # which is a subclass of tcod’s EventDispatch class.
    # EventDispatch is a class that allows us to send an event to its proper method based on what type of event it is.
    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        raise SystemExit()

    # using a method of EventDispatch: ev_quit is a method defined in EventDispatch,
    # which we’re overriding in EventHandler.
    # ev_quit is called when we receive a “quit” event,
    # which happens when we click the “X” in the window of the program.
    # In that case, we want to quit the program, so we raise SystemExit() to do so.

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        match event.sym:
            case tcod.event.K_UP:
                return MovementAction(dx=0, dy=-1)
            case tcod.event.K_DOWN:
                return MovementAction(dx=0, dy=1)
            case tcod.event.K_LEFT:
                return MovementAction(dx=-1, dy=0)
            case tcod.event.K_RIGHT:
                return MovementAction(dx=1, dy=0)
            case tcod.event.K_ESCAPE:
                return EscapeAction()
