import pygame

from isec.app import Resource
from isec.instance import BaseInstance
from isec.environment import Entity
from isec.environment.sprite import StateSprite
from isec.environment.position import PymunkPos

from game.entities.game_entity import GameEntity
from game.entities.shape_info import PlayerShapeInfo
from game.weapons.pan import Pan


class Player(GameEntity):
    def __init__(self, 
                 position: pygame.Vector2) -> None:

        # player_dict = Resource.data["entities"]["player"]

        # position = PymunkPos("DYNAMIC", PlayerShapeInfo, pygame.math.Vector2(position))
        # position.create_circle_shape(player_dict["position"]["hitbox_radius"])
        # position.body.mass = player_dict["position"]["mass"]
        # position.body.moment = float("inf")

        sprite = StateSprite.create_from_directory("sprite/player",
                                                   "static",
                                                   0,
                                                   Resource.data["entities"]["player"]["sprite"]["anchor"])
        position = self.create_position(position, PlayerShapeInfo)

        super().__init__(position, sprite)

        # Inputs related
        self.last_dir = -1
        self.inputs = {"up": False, "down": False, "left": False, "right": False}

        # Gameplay related
        self.primary = Pan()

    def update(self,
               delta: float) -> None:

        self.sprite.update(delta)
        self.handle_movement(delta)
        weapon_vec = -pygame.Vector2(200, 150) + pygame.mouse.get_pos()
        if weapon_vec.length():
            weapon_vec.scale_to_length(15)
            self.primary.position.x = self.position.x + weapon_vec.x
            self.primary.position.y = self.position.y + weapon_vec.y - 3
            self.primary.position.angle = weapon_vec.angle_to((1, 0))

        else:
            self.primary.position.x, self.primary.position.y = self.position.x, self.position.y

    def handle_movement(self,
                        delta: float) -> None:

        self.position.speed *= self.attributes["air_resistance"] ** delta

        move_vec = (pygame.Vector2(1, 0) * (self.inputs["right"]-self.inputs["left"]) +
                    pygame.Vector2(0, 1) * (self.inputs["down"]-self.inputs["up"]))

        if move_vec.length() == 0:
            self.sprite.switch_state("idle")
            self.inputs = {"up": False, "down": False, "left": False, "right": False}
            return

        if move_vec.x * self.last_dir < 0:
            self.last_dir = -self.last_dir
            self.sprite.flip()

        self.sprite.switch_state("run")

        move_vec.scale_to_length(self.attributes["speed"])
        self.position.body.apply_force_at_local_point((move_vec.x, move_vec.y))

        self.inputs = {"up": False, "down": False, "left": False, "right": False}

    def add_callbacks(self,
                      instance: BaseInstance):

        async def move_up():
            self.inputs["up"] = True

        async def move_down():
            self.inputs["down"] = True

        async def move_left():
            self.inputs["left"] = True

        async def move_right():
            self.inputs["right"] = True

        instance.event_handler.register_keypressed_callback(pygame.K_z, move_up)
        instance.event_handler.register_keypressed_callback(pygame.K_s, move_down)
        instance.event_handler.register_keypressed_callback(pygame.K_q, move_left)
        instance.event_handler.register_keypressed_callback(pygame.K_d, move_right)
