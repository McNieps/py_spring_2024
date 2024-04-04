from isec.app import Resource
from isec.instance import BaseInstance, LoopHandler

from game.tools import Level
from game.tools.gui import GUI


class InstanceGame(BaseInstance):
    def __init__(self):
        super().__init__(fps=Resource.data["instance"]["game"]["fps"])
        self.level = Level(self)
        self.level.add_callbacks()
        self.gui = GUI(self.level)

    async def loop(self):
        LoopHandler.fps_caption()
        self.level.update()
        self.level.render()
        self.gui.update()
        self.gui.render()
