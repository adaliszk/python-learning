import tcod

from scene import Scene


# TODO: check if scene or action for EventDispatch.
class Player(tcod.event.EventDispatch[Scene]):
    """Player configs."""

    def __init__(self):
        self.color = (255, 255, 255),
        self.name = "player"
        self.defense = 3,
        self.attack = 5,
        self.char = "@"
        self.hp = 30,

    def is_alive(self):
        return self.hp > 0

    def is_dead(self):
        return self.hp <= 0


class Orc(tcod.event.EventDispatch[Scene]):
    """Orc configs."""

    def __init__(self):
        self.color = (63, 127, 63),
        self.name = "Orc"
        self.defense = 1,
        self.attack = 2,
        self.char = "o"
        self.hp = 15,

    def is_alive(self):
        return self.hp > 0

    def is_dead(self):
        return self.hp <= 0


class Troll(tcod.event.EventDispatch[Scene]):
    """Troll configs."""

    def __init__(self):
        self.color = (0, 127, 0),
        self.name = "Troll"
        self.defense = 5,
        self.attack = 4,
        self.char = "T"
        self.hp = 40,

    def is_alive(self):
        return self.hp > 0

    def is_dead(self):
        return self.hp <= 0
