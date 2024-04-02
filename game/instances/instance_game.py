from isec.app import Resource
from isec.instance import BaseInstance, LoopHandler

from game.tools import Level


class InstanceGame(BaseInstance):
    def __init__(self):
        super().__init__(fps=Resource.data["instance"]["game"]["fps"])
        self.level = Level(self)
        self.level.add_callbacks()

    async def loop(self):
        LoopHandler.fps_caption()
        self.level.update()
        self.level.render()
