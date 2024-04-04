import pygame

from isec.app import Resource
from isec.environment.sprite import AnimatedSprite
from isec.environment.position import SimplePos

from game.utils.game_entity import GameEntity

from game.utils import Level


class EnemyBullet(GameEntity):
    def __init__(self,
                 level: Level,
                 position: pygame.Vector2,
                 aim_vec: pygame.Vector2) -> None:

        sprite = AnimatedSprite([Resource.image["sprite"]["misc"][f"bullet_{i}"] for i in range(2)],
                                [0.1, 0.1])

        aim_vec.normalize_ip()
        position = SimplePos(position, -aim_vec*100)
        super().__init__(position, sprite, level)

    def update(self,
               delta: float) -> None:

        super().update(delta)
        if not -500 < self.position.x < 1500:
            self.destroy()
            return

        if not -500 < self.position.y < 1500:
            self.destroy()
            return

        dist_to_player = self.position.position - self.level.player.position.position
        if dist_to_player.length() < 10:
            if self.level.player.hit(1):   # Return true if the player is able to take damage
                self.destroy()
