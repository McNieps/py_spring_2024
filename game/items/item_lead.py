from game.items.base_item import BaseItem
from game.utils import Level


# Increase damage, reduces attack period

class ItemLead(BaseItem):
    def __init__(self, level: Level):
        super().__init__(level)

    def on_equip(self):
        pass

