from isec.app import Resource
from isec.instance import BaseInstance, LoopHandler

from game.gui import GUI
from game.utils import Level

from game.entities import entities, Player, Campfire
from game.instances.instance_item_selection import InstanceItemSelection


class InstanceGame(BaseInstance):
    def __init__(self):
        super().__init__(fps=Resource.data["instance"]["game"]["fps"])
        self.level = Level(Player(), self, entities)
        self.level.add_callbacks()
        self.gui = GUI(self.level)
        self.level.add_entities(Campfire(self.level))

    async def loop(self):
        self.level.update()
        self.level.render()
        self.gui.update()
        self.gui.render()
        for _ in range(self.level.player.level_to_award):  # lol
            self.level.player.level_to_award -= 1
            await InstanceItemSelection(self.level).execute()
