from typing import Iterable

import pygame

from isec.app import Resource
from isec.environment import Sprite
from isec.environment.position import AdvancedPos

from game.entities.game_entity import GameEntity
from game.weapons.base_weapon import BaseWeapon, BaseProjectile


class Pan(BaseWeapon):
    def __init__(self,
                 linked_entity: GameEntity) -> None:

        sprite = Sprite(Resource.image["sprite"]["weapons"]["pan"], "rotated")
        sprite.displayed = True
        super().__init__(AdvancedPos((0, 0), a=0), sprite)
        self.linked_entity = linked_entity

    def update(self,
               delta: float) -> None:

        if self.sprite.displayed:
            self.flip_sprite()

            weapon_vec = -pygame.Vector2(200, 150) + pygame.mouse.get_pos()
            if weapon_vec.length():
                weapon_vec.scale_to_length(15)
                self.position.x = self.linked_entity.position.x + weapon_vec.x
                self.position.y = self.linked_entity.position.y + weapon_vec.y - 3
                self.position.angle = weapon_vec.angle_to((1, 0))

            else:
                self.position.x, self.position.y = self.linked_entity.position.x, self.linked_entity.position.y
