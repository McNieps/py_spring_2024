import pygame

from isec.environment import Entity, Sprite
from isec.environment.position import SimplePos

from game.utils.level import Level


class ChunkCounter(Entity):
    def __init__(self,
                 level: Level) -> None:

        self.player = level.player
        self.size = (58, 15)
        position = SimplePos((334, 8))
        sprite = Sprite(pygame.Surface(self.size, pygame.SRCALPHA), position_anchor="topleft")
        self.font = pygame.font.Font("game/assets/font/owre_kynge.ttf", 15)
        super().__init__(position, sprite)

    def update(self,
               delta: float) -> None:

        self.sprite.surface.fill((57, 57, 57))
        text_surf = self.font.render(str(self.player.xp_chunks), False, (246, 205, 38))
        # text_surf = self.font.render("feur", False, (246, 205, 38))
        text_rect = text_surf.get_rect()
        text_rect.center = self.size[0]/2, self.size[1]/2+1

        self.sprite.surface.blit(text_surf, text_rect)
