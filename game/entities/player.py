import pygame

from isec.app import Resource
from isec.instance import BaseInstance
from isec.environment import Entity
from isec.environment.sprite import StateSprite
from isec.environment.position import PymunkPos

from game.entities.shape_info import PlayerShapeInfo


class Player(Entity):
    def __init__(self, 
                 position: tuple[float, float]) -> None:

        player_dict = Resource.data["entities"]["player"]

        position = PymunkPos("DYNAMIC", PlayerShapeInfo, pygame.math.Vector2(position))
        position.create_circle_shape(player_dict["position"]["hitbox_radius"])
        position.body.mass = player_dict["position"]["mass"]
        position.body.moment = float("inf")

        sprite = StateSprite.create_from_directory("sprite/player",
                                                   "static",
                                                   position_anchor=player_dict["position"]["hitbox_center"])

        super().__init__(position, sprite)

    def update(self,
               delta: float) -> None:
        self.position.speed *= 0.01 ** delta

    def add_callbacks(self,
                      instance: BaseInstance):

        force = 500

        async def move_up():

            # self.position.y -= speed * instance.delta
            self.position.body.apply_force_at_local_point((0, -force))

        async def move_down():
            self.position.body.apply_force_at_local_point((0, force))

        async def move_left():
            self.position.body.apply_force_at_local_point((-force, 0))

        async def move_right():
            self.position.body.apply_force_at_local_point((force, 0))

        instance.event_handler.register_keypressed_callback(pygame.K_z, move_up)
        instance.event_handler.register_keypressed_callback(pygame.K_s, move_down)
        instance.event_handler.register_keypressed_callback(pygame.K_q, move_left)
        instance.event_handler.register_keypressed_callback(pygame.K_d, move_right)

        #self.position.body.moment = float("inf")
