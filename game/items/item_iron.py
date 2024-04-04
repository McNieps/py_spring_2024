from game.items.base_item import BaseItem
from game.utils import Level


# reduce dodge CD

class ItemIron(BaseItem):
    def __init__(self, level: Level):
        super().__init__(level)

    def on_equip(self):
        self.player.attributes["dodge_period"] *= 1/1.25
        self.player.attributes["dodge_impulse"] *= 1.25
