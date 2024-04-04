import pygame

from isec.app import Resource
from isec.environment.sprite import StateSprite

from game.utils.base_enemy import BaseEnemy
from game.utils.shape_info import EnemyShapeInfo

from game.entities.enemy_bullet import EnemyBullet
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

        self.time_since_last_attack = -self.attributes["attack_period"]

    def update(self,
               delta: float) -> None:

        super().update(delta)
        self.position.speed *= self.attributes["air_resistance"] ** delta
        self.time_since_last_attack += delta
        self.sprite.update(delta)
        self.set_target(self.level.player)

        aim_vec = self.position.position - self.level.player.position.position
        dist_to_player = aim_vec.length()

        if dist_to_player > 150:
            self.walk_toward_target()

        else:
            self.attack(aim_vec)

    def attack(self, aim_vec: pygame.Vector2):
        if self.time_since_last_attack > self.attributes["attack_period"]:
            self.time_since_last_attack = 0
            self.sprite.reset_animation()   # NOQA
            self.level.add_entities(EnemyBullet(self.level,
                                                self.position.position,
                                                aim_vec))

    def on_death(self) -> None:
        for _ in range(self.attributes["xp"]):
            self.level.add_entities(XPChunk(self.level, tuple(self.position.position)))
