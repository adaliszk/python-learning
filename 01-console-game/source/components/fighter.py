from components.base_components import BaseComponent


class Fighter(BaseComponent):
    def __init__(self, hp: int, defense: int, power: int):
        self.max_hp = hp
        self._hp = hp
        self.defense = defense
        self.power = power

    @property
    def hp(self) -> int:
        return self.hp

    @hp.setter
    def hp(self, value: int) -> None:
        self._hp = max(0, min(value, self.max_hp))