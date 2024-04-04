from game.items.base_item import BaseItem
from game.utils import Level


# Increase health, increase health regen

class ItemCopper(BaseItem):
    def __init__(self, level: Level):
        super().__init__(level)

    def on_equip(self):
        self.player.attributes["health"] += 1
        self.player.hp += 1
        self.player.attributes["health_regen"] += 0.1
