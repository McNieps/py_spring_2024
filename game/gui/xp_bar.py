import pygame

from isec.environment import Entity, Sprite
from isec.environment.position import SimplePos

from game.utils.level import Level


class XPBar(Entity):
    def __init__(self,
                 level: Level) -> None:
        self.player = level.player
        self.size = (5, 250)
        position = SimplePos((391, 46))
        sprite = Sprite(pygame.Surface(self.size, pygame.SRCALPHA), position_anchor="topleft")

        super().__init__(position, sprite)

    def update(self,
               delta: float) -> None:

        self.sprite.surface.fill((57, 57, 57))

        xp_remaining_percentage = 1-self.player.xp / self.player.xp_to_max
        rect = pygame.Rect((0, round(self.size[1]*xp_remaining_percentage)), self.size)
        pygame.draw.rect(self.sprite.surface, (246, 205, 38), rect)
