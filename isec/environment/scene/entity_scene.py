import math
import pygame
import pymunk

from isec.environment.base.camera import Camera
from isec.environment.base import RenderingTechniques, Entity, Scene
from isec.environment.position import PymunkPos


class EntityScene(Scene):
    def __init__(self,
                 fps: int,
                 surface: pygame.Surface = None,
                 entities: list[Entity] = None,
                 camera: Camera = None) -> None:

        super().__init__(surface, camera)

        if entities is None:
            entities = []
        self.entities = entities

        self.avg_delta = 1 / fps
        self._space = pymunk.Space()

    def add_entities(self,
                     *entities: Entity) -> None:

        for entity in entities:
            if isinstance(entity.position, PymunkPos):
                entity.position.add_to_space(self._space)

        self.entities.extend([entity for entity in entities
                              if entity not in self.entities])

    def remove_entities(self,
                        *entities: Entity) -> None:

        for entity in entities:
            if entity not in self.entities:
                continue

            if isinstance(entity.position, PymunkPos):
                entity.position.remove_from_space()

            self.entities.remove(entity)

    def remove_entities_by_name(self,
                                name: str) -> None:

        for entity in self.entities:
            if entity.__class__.__name__ == name:
                self.remove_entities(entity)

    def update(self,
               _delta: float) -> None:

        for entity in self.entities:
            entity.update(self.avg_delta)

        for entity in reversed(self.entities):
            if entity.to_delete:
                self.remove_entities(entity)

        self.space.step(self.avg_delta)

    def z_sort(self):
        self.entities.sort(key=lambda ent: ent.position.y)

    def render(self,
               camera: Camera = None) -> None:

        if camera is None:
            camera = self.camera

        for entity in self.entities:
            vec = camera.get_offset_pos(entity.position)  # NOQA
            x, y = math.floor(vec.x), math.floor(vec.y)
            entity.render((x, y), self.surface, self.rect)

    @property
    def space(self) -> pymunk.Space:
        return self._space

