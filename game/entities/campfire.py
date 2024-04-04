import math

from isec.app import Resource

from isec.environment import Entity, Sprite
from isec.environment.position import SimplePos

from game.utils.level import Level


class Campfire(Entity):
    def __init__(self,
                 level: Level) -> None:

        position = SimplePos((512, 512))
        sprite = Sprite(Resource.image["sprite"]["misc"]["campfire"])
        super().__init__(position, sprite)

        self.level = level
        self.is_in_range = False
        self.time_in_range = 0
        self.can_convert = 0
        self.rate = 0

    def update(self,
               delta: float) -> None:

        vec = self.level.player.position.position - self.position.position
        if vec.length() > Resource.data["entities"]["campfire"]["range"]:
            self.player_leave()
            return

        self.player_in_range(delta)

    def player_in_range(self, delta):
        self.is_in_range = True
        self.time_in_range += delta
        self.rate = self.get_conversion_rate()
        self.can_convert += self.rate * delta
        self.consume_chunks()

    def get_conversion_rate(self) -> float:
        """Return a float representing the conversion of xp chunk to xp in xp chunk consumed PER SECOND"""
        factor = Resource.data["entities"]["campfire"]["conversion_rate_factor"]
        power = Resource.data["entities"]["campfire"]["conversion_rate_power"]
        return factor * self.time_in_range ** power

    def consume_chunks(self) -> None:
        player_chunks = self.level.player.xp_chunks
        can_convert_int = math.floor(self.can_convert)
        if can_convert_int <= 0 or player_chunks <= 0:
            return

        consumable_chunks = can_convert_int if can_convert_int < player_chunks else player_chunks
        self.can_convert -= consumable_chunks
        self.level.player.gain_xp(consumable_chunks)
        self.level.player.xp_chunks -= consumable_chunks
        sound_value = int(min(self.rate/10, 5))
        Resource.sound["effects"][f"xp_convert_{sound_value}"].play()

    def player_leave(self):
        self.is_in_range = False
        self.time_in_range = 0
        self.can_convert = 0
