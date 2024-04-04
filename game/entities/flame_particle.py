import random
import pygame

from isec.environment import Sprite, Entity
from isec.environment.position import SimplePos


class FlameParticle(Entity):
    def __init__(self,
                 strength: float,
                 vec: pygame.Vector2 = (516, 512),
                 spread: float = 10) -> None:

        self.duration = 0
        self.max_duration = 0
        x_spread = int((random.random()-0.5)*3*spread)
        y_spread = int((random.random()-0.5)*2*spread)
        position = SimplePos((vec[0]+x_spread, vec[1]+y_spread),
                             (0, -random.random()*10*strength))

        sprite = Sprite(self.create_surf())
        super().__init__(position, sprite)

    def update(self,
               delta: float) -> None:

        self.duration += delta
        self.sprite.surface.set_alpha(int(255*(1-self.duration/self.max_duration)))
        if self.duration > self.max_duration:
            self.destroy()
            return

        self.position.speed *= 0.05 ** delta

        super().update(delta)

    def create_surf(self) -> pygame.Surface:
        self.max_duration = 0.5+random.random()
        surf = pygame.Surface((10, 10), pygame.SRCALPHA)
        size = random.randint(1, 10)
        pygame.draw.ellipse(surf, (246, 205, 38), (0, 0, size, size))
        return surf
