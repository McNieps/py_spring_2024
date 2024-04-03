import pygame

from isec.app import Resource
from isec.environment import Entity, Pos, Sprite

from game.entities.game_entity import GameEntity


class BaseProjectile(Entity):
    def __init__(self,
                 linked_weapon: "BaseWeapon",
                 aim_vec: pygame.Vector2,
                 position: Pos,
                 sprite: Sprite) -> None:

        super().__init__(position, sprite)

        self.aim_vec = aim_vec
        self.linked_weapon = linked_weapon

        self.dict = Resource.data["weapons"][self.__class__.__name__.lower().removesuffix("projectile")]
        self.hit_entities = set()

    def update(self,
               delta: float) -> None:

        speed_vec = self.aim_vec.copy()
        speed_vec.scale_to_length(self.dict["base"]["speed"])
        self.position.position += speed_vec * delta


class BaseWeapon(Entity):
    def __init__(self,
                 linked_entity: GameEntity,
                 position: Pos,
                 sprite: Sprite):

        super().__init__(position, sprite)
        self.linked_entity = linked_entity
        self.side = 1

    async def attack(self,
                     aim_vec: pygame.Vector2) -> None:
        return

    def flip_sprite(self) -> None:
        if int(90 > self.position.angle > -90) != self.side:
            self.side = 1-self.side
            self.sprite.flip(False, True)
