import pygame
import typing

from isec.app import Resource
from isec.environment import Pos, Sprite, Entity

from game.utils.game_entity import GameEntity

if typing.TYPE_CHECKING:
    from game.utils import Level


class BaseEnemy(GameEntity):
    BASE_ATTRIBUTES = {}

    def __init__(self,
                 level: "Level",
                 sprite: Sprite,
                 position: Pos) -> None:

        super().__init__(position, sprite, level)
        self.dict = Resource.data["entities"][self.__class__.__name__.lower()]
        self.target_pos: pygame.Vector2 | None = None

        self.hp = self.attributes["hp"]

    def set_target(self,
                   target: tuple[float, float] | Entity | Pos | pygame.Vector2):

        if isinstance(target, tuple):
            self.target_pos = pygame.Vector2(target[0], target[1])
            return

        if isinstance(target, pygame.Vector2):
            self.target_pos = target
            return

        if isinstance(target, Entity):
            self.target_pos = target.position.position
            return

        if isinstance(target, Pos):
            self.target_pos = target.position
            return

    def update(self,
               delta: float) -> None:

        return

    def walk_toward_target(self) -> None:

        if self.target_pos is not None:
            move_vec = self.target_pos - self.position.position
            if move_vec.length() > 0:
                move_vec.scale_to_length(self.attributes["speed"])
                self.position.body.apply_force_at_local_point(tuple(move_vec))
