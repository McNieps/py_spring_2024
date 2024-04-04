import random

from isec.app import Resource

from isec.environment import Entity, Sprite
from isec.environment.position import SimplePos

from game.utils.level import Level


class XPChunk(Entity):
    def __init__(self,
                 level: Level,
                 position: tuple[float, float]) -> None:

        position = SimplePos(position)
        sprite = Sprite(Resource.image["sprite"]["misc"][f"xp_chunk_{random.randint(0, 3)}"])
        super().__init__(position, sprite)

        self.level = level

    def update(self,
               delta: float) -> None:
        vec = self.level.player.position.position - self.position.position
        dist = vec.length()

        if dist < self.level.player.attributes["pickup_range"]:
            Resource.sound["effects"]["xp_pickup"].play()
            self.level.player.xp_chunks += 1
            self.destroy()
