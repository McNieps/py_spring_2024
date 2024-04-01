import pygame

from isec.app import Resource
from isec.instance import BaseInstance
from isec.environment import Entity, EntityScene
from isec.environment.sprite import StateSprite
from isec.environment.position import PymunkPos


class Player(Entity):
    def __init__(self, 
                 position: tuple[float, float],
                 scene: EntityScene,
                 instance: BaseInstance) -> None:

        position = PymunkPos(body_type="KINEMATIC", position=pygame.math.Vector2(position))
        position.create_circle_shape(Resource.data["entities"]["player"]["position"]["hitbox_radius"])

        sprite = StateSprite.create_from_directory("sprite/player",
                                                   "static",
                                                   position_anchor=(8, 27))

        super().__init__(position, sprite, scene, instance)
