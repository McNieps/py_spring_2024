import random

from game.items.base_item import BaseItem
from game.utils import Level


# increase item pickup range, 25% chance to re-trigger others items

class ItemGold(BaseItem):
    def __init__(self, level: Level):
        super().__init__(level)

    def on_equip(self):
        self.player.attributes["pickup_range"] *= 1.25

        if random.random() >= 0.75:
            for item in self.player.items:
                item.on_equip()

