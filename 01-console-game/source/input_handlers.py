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
            case tcod.event.K_v:
                self.engine.event_handler = HistoryViewer(self.engine)


# TODO add diagonal walk and uninterrupted direction change.

class GameOverEventHandler(EventHandler):
    def handle_events(self, context: tcod.context.Context) -> None:
        for event in tcod.event.wait():
            action = self.dispatch(event)

            if action is None:
                continue

            action.perform()


class HistoryViewer(EventHandler):
    """Print the history on a larger window which can be navigated."""

    def __init__(self, engine: Engine):
        super().__init__(engine)
        self.log_length = len(engine.message_log.messages)
        self.cursor = self.log_length - 1

    def move_cursor(self, new_value: int):
        cursor = self.cursor + new_value

        if cursor < 0:
            cursor = self.log_length - 1

        if cursor > self.log_length:
            cursor = 0

        self.cursor = cursor

    def on_render(self, console: tcod.Console) -> None:
        super().on_render(console)  # Draw the main state as the background.

        log_console = tcod.Console(console.width - 6, console.height - 6)

        # Draw a frame with a custom banner title.
        log_console.draw_frame(0, 0, log_console.width, log_console.height)
        log_console.print_box(
            0, 0, log_console.width, 1, "┤Message history├", alignment=tcod.CENTER
        )

        # Render the message log using the cursor parameter.
        self.engine.message_log.render_messages(
            console=log_console,
            x=1,
            y=1,
            width=log_console.width - 2,
            height=log_console.height - 2,
            messages=self.engine.message_log.messages[: self.cursor + 1],
        )
        log_console.blit(console, 3, 3)

    def ev_keydown(self, event: tcod.event.KeyDown) -> None:
        match event.sym:
            case tcod.event.K_HOME:
                self.cursor = 0
            case tcod.event.K_PAGEUP:
                self.move_cursor(-10)
            case tcod.event.K_UP:
                self.move_cursor(-1)
            case tcod.event.K_DOWN:
                self.move_cursor(+1)
            case tcod.event.K_PAGEDOWN:
                self.move_cursor(+10)
            case tcod.event.K_END:
                self.cursor = self.log_length - 1
            case _:
                self.switch_handler(MainGameEventHandler)
                # self.engine.event_handler = MainGameEventHandler(self.engine)
