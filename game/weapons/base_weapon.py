import pygame

from typing import Iterable

from isec.environment import Entity, Pos, Sprite


class BaseProjectile:
    pass


class BaseWeapon(Entity):
    def __init__(self,
                 position: Pos,
                 sprite: Sprite):

        super().__init__(position, sprite)
        self.side = 1

    def attack(self,
               aim_vec: pygame.Vector2) -> None:
        return

    def update(self,
               delta: float) -> None:
        return

    def render(self,
               camera_offset: Iterable,
               surface: pygame.Surface,
               rect: pygame.Rect) -> None:

        self.flip_sprite()
        super().render(camera_offset, surface, rect)

    def flip_sprite(self) -> None:
        if int(90 > self.position.angle > -90) != self.side:
            self.side = 1-self.side
            self.sprite.flip(False, True)
