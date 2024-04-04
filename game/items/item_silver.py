import random

from game.items.base_item import BaseItem
from game.utils import Level


# increase piercing

class ItemSilver(BaseItem):
    def __init__(self, level: Level):
        super().__init__(level)

    def on_equip(self):
        self.primary.attributes["max_hit"] += 1
