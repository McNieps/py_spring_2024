from isec.app import Resource
from isec.instance import BaseInstance, LoopHandler

from game.tools import Level


class InstanceGame(BaseInstance):
    def __init__(self):
        super().__init__(fps=Resource.data["instance"]["game"]["fps"])
        self.level = Level(self)

    async def loop(self):
        self.level.update()
        # self.gui.update()
        self.level.render()
        # self.gui.render()
