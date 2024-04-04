import math
import pygame
import random

from isec.app import Resource

from isec.environment import Entity, Sprite
from isec.environment.position import SimplePos

from game.utils.level import Level
from game.entities.flame_particle import FlameParticle


class Campfire(Entity):
    def __init__(self,
                 level: Level) -> None:

        position = SimplePos((512, 512-50))
        sprite = Sprite(Resource.image["sprite"]["misc"]["campfire"])
        super().__init__(position, sprite)

        self.level = level
        self.is_in_range = False
        self.time_in_range = 0
        self.can_convert = 0
        self.rate = 0

        self.flame_period = 1/50
        self.last_flame = 0

        self.range_indicator_period = 1
        self.last_range_indicator = 0

    def update(self,
               delta: float) -> None:

        self.passive_flame(delta)
        self.range_indicator(delta)

        vec = self.level.player.position.position - (512, 512)
        if vec.length() > Resource.data["entities"]["campfire"]["range"]:
            self.player_leave()
            return

        self.player_in_range(delta)

    def passive_flame(self,
                      delta: float) -> None:
        self.last_flame += delta
        if self.last_flame > self.flame_period:
            self.level.add_entities(FlameParticle(1))
            self.last_flame -= self.flame_period
            self.passive_flame(0)

    def range_indicator(self,
                        delta: float) -> None:
        self.last_range_indicator += delta
        if self.last_range_indicator > self.range_indicator_period:
            self.last_range_indicator -= self.range_indicator_period
            number_of_indicators = 20
            angle_step = 360/number_of_indicators
            angle_offset = random.random()*angle_step
            vec = pygame.Vector2(Resource.data["entities"]["campfire"]["range"], 0)
            for i in range(number_of_indicators):
                new_vec = pygame.Vector2(512, 512) + vec.rotate(angle_offset+i*angle_step)
                self.level.add_entities(FlameParticle(10.5, new_vec, 0.2))

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

        for _ in range(consumable_chunks*10):
            self.level.add_entities(FlameParticle(self.rate))

    def player_leave(self):
        self.is_in_range = False
        self.time_in_range = 0
        self.can_convert = 0
