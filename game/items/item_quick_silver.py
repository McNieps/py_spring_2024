from game.items.base_item import BaseItem
from game.utils import Level


# increase projectile speed, increase projectile duration

class ItemQuickSilver(BaseItem):
    def __init__(self, level: Level):
        super().__init__(level)

    def on_equip(self):
        self.primary.attributes["speed"] *= 1.5
        self.primary.attributes["duration"] *= 1.5
        self.primary.attributes["swing_arc_length"] *= 1.5
