from game.items.base_item import BaseItem
from game.utils import Level


# Increase damage, reduces attack period

class ItemLead(BaseItem):
    def __init__(self, level: Level):
        super().__init__(level)

    def on_equip(self):
        self.primary.attributes["damage"] += 2
        self.primary.attributes["attack_period"] *= 1.25
        self.primary.attributes["knockback"] *= 1.25
