from game.utils import Level


class BaseItem:
    def __init__(self,
                 level: Level) -> None:
        self.level = level
        self.player = level.player
        self.primary = self.player.primary

    def on_update(self) -> None:
        """Update effects go here"""
        pass

    def on_equip(self):
        """Stats alteration go here"""
        pass

    def on_attack(self):
        """Attack effects go here"""
        pass

    def on_kill(self):
        """kill effects go here"""
        pass

    def on_xp_gain(self):
        """???"""
        pass

    def on_damage_receive(self):
        """???"""
        pass
