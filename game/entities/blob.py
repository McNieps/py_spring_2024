import pygame

from isec.app import Resource
from isec.environment import Sprite

from game.entities.shape_info import EnemyShapeInfo
from game.entities.base_enemy import BaseEnemy


class Blob(BaseEnemy):
    def __init__(self,
                 position: pygame.Vector2) -> None:

        sprite = Sprite(Resource.image["sprite"]["enemies"]["blob"],
                        "static",
                        0,
                        Resource.data["entities"]["blob"]["sprite"]["anchor"])

        position = self.create_position(position, EnemyShapeInfo)

        super().__init__(sprite, position)

    def update(self,
               delta: float) -> None:

        self.position.speed *= self.attributes["air_resistance"] ** delta
        self.walk_toward_target()

        super().update(delta)
