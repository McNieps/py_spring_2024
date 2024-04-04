import pygame

from isec.app import Resource
from isec.environment.sprite import StateSprite

from game.utils.base_enemy import BaseEnemy
from game.utils.shape_info import EnemyShapeInfo

from game.entities.xp_chunk import XPChunk
from game.utils import Level


class Peanut(BaseEnemy):
    def __init__(self,
                 level: Level,
                 position: pygame.Vector2) -> None:

        sprite = StateSprite.create_from_directory("sprite/enemies/peanut",
                                                   "static",
                                                   0,
                                                   Resource.data["entities"]["peanut"]["sprite"]["anchor"])
        position = self.create_position(position, EnemyShapeInfo)

        super().__init__(level, sprite, position)

        self.sprite.switch_state("attack")

    def update(self,
               delta: float) -> None:

        self.sprite.update(delta)
        self.set_target(self.level.player)

        self.position.speed *= self.attributes["air_resistance"] ** delta
        self.walk_toward_target()

        super().update(delta)

    def on_death(self) -> None:
        for _ in range(self.attributes["xp"]):
            self.level.add_entities(XPChunk(self.level, tuple(self.position.position)))
