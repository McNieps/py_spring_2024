import pygame

from isec.environment import Entity, Sprite
from isec.environment.position import SimplePos

from game.utils.level import Level


class Timer(Entity):
    def __init__(self,
                 level: Level) -> None:
        self.spawner = level.spawner
        self.size = (385, 5)
        position = SimplePos((4, 291))
        sprite = Sprite(pygame.Surface(self.size, pygame.SRCALPHA), position_anchor="topleft")

        super().__init__(position, sprite)
