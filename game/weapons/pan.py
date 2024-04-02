import pygame

from isec.app import Resource
from isec.environment import Sprite
from isec.environment.position import AdvancedPos

from game.weapons.base_weapon import BaseWeapon, BaseProjectile


class Pan(BaseWeapon):
    def __init__(self):
        sprite = Sprite(Resource.image["sprite"]["weapons"]["pan"], "rotated")
        super().__init__(AdvancedPos((0, 0), a=0), sprite)

    def update(self,
               delta: float) -> None:
        pass
