from game.items.base_item import BaseItem
from game.utils import Level


# Increase speed, increase attack speed

class ItemTin(BaseItem):
    def __init__(self, level: Level):
        super().__init__(level)

    def on_equip(self):
        self.player.attributes["speed"] *= 1.05
        self.primary.attributes["attack_period"] *= 1/1.25
