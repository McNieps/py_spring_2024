import pygame
import typing

from isec.app import Resource
from isec.environment import Pos, Sprite, Entity
from isec.environment.position.pymunk_pos import PymunkPos, PymunkShapeInfo

if typing.TYPE_CHECKING:
    from game.utils.level import Level


class GameEntity(Entity):
    BASE_ATTRIBUTES = {}

    def __init__(self,
                 position: Pos,
                 sprite: Sprite,
                 level: "Level" = None) -> None:

        super().__init__(position, sprite)
        self.level = level
        self.target_pos: pygame.Vector2 | None = None
        self.attributes = self.load_attributes()

        self.hp = self.attributes["hp"]

    def set_target(self,
                   target: tuple[float, float] | Entity | Pos):

        if isinstance(target, tuple):
            self.target_pos = pygame.Vector2(target[0], target[1])
            return

        if isinstance(target, Entity):
            self.target_pos = target.position.position
            return

        if isinstance(target, Pos):
            self.target_pos = target.position
            return

    def update(self,
               delta: float) -> None:

        if self.target_pos is not None:
            move_vec = self.target_pos - self.position.position
            if move_vec.length() > 0:
                move_vec.scale_to_length(self.attributes["speed"])
                self.position.body.apply_force_at_local_point(move_vec)

    def hit(self,
            damage: float) -> bool:

        self.on_hit(damage)

        if self.hp > 0:
            return False

        self.kill()
        return True

    def kill(self):
        self.on_death()
        self.destroy()

    def on_hit(self,
               damage: float) -> None:
        self.hp -= damage

    def on_death(self) -> None:
        pass

    @classmethod
    def create_position(cls,
                        position: pygame.Vector2,
                        shape_info: typing.Type[PymunkShapeInfo]) -> PymunkPos:

        position_dict = Resource.data["entities"][cls.__name__.lower()]["position"]
        position = PymunkPos("DYNAMIC", shape_info, position)

        if position_dict["shape"] == "circle":
            position.create_circle_shape(position_dict["radius"])

        position.body.mass = position_dict["mass"]
        position.body.moment = float(position_dict["moment"])

        return position

    @classmethod
    def load_attributes(cls,
                        entity_name: str = None) -> dict[str, typing.Any]:

        if entity_name is None:
            entity_name = cls.__name__
        entity_name = entity_name.lower()

        return Resource.data["entities"][entity_name]["attributes"]
