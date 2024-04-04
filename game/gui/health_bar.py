import pygame

from isec.environment import Entity, Sprite
from isec.environment.position import SimplePos

from game.utils.level import Level


class HealthBar(Entity):
    def __init__(self,
                 level: Level) -> None:
        self.player = level.player
        self.size = (385, 5)
        position = SimplePos((4, 291))
        sprite = Sprite(pygame.Surface(self.size, pygame.SRCALPHA), position_anchor="topleft")

        super().__init__(position, sprite)

    def update(self,
               delta: float) -> None:
        self.sprite.surface.fill((57, 57, 57))

        health_percentage = self.player.current_health / self.player.attributes["health"]
        rect = pygame.Rect((0, 0), (self.size[0]*health_percentage, self.size[1]))
        pygame.draw.rect(self.sprite.surface, (187, 127, 87), rect)
