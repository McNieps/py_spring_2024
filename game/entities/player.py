import pygame

from isec.app import Resource
from isec.instance import BaseInstance
from isec.environment.sprite import StateSprite
from isec.environment import EntityScene

from game.entities.game_entity import GameEntity
from game.entities.shape_info import PlayerShapeInfo
from game.weapons.pan import Pan


class Player(GameEntity):
    def __init__(self,
                 scene: EntityScene,
                 position: pygame.Vector2) -> None:

        position = self.create_position(position, PlayerShapeInfo)
        sprite = StateSprite.create_from_directory("sprite/player",
                                                   "static",
                                                   0,
                                                   Resource.data["entities"]["player"]["sprite"]["anchor"])
        super().__init__(scene,
                         position,
                         sprite)

        # Inputs related
        self.last_dir = -1
        self.events = self.reset_events()

        # Gameplay related
        self.state = {"state": "", "time_left": 0}
        self.primary = Pan(self)
        self.secondary = Pan(self)
        self.health = 10
        self.max_health = 15
        self.level = 0
        self.xp = 1
        self.max_xp = 10

    def update(self,
               delta: float) -> None:

        self.sprite.update(delta)
        self.handle_actions(delta)
        self.handle_movement(delta)

    def handle_movement(self,
                        delta: float) -> None:

        self.state["time_left"] -= delta

        if self.state["state"] != "":
            if self.state["time_left"] > 0:
                self.events = self.reset_events()
                return

            self.state["state"] = ""
            self.state["time_left"] = 0

        self.position.speed *= self.attributes["air_resistance"] ** delta

        move_vec = (pygame.Vector2(1, 0) * (self.events["right"]["pressed"] - self.events["left"]["pressed"]) +
                    pygame.Vector2(0, 1) * (self.events["down"]["pressed"] - self.events["up"]["pressed"]))

        if move_vec.length() == 0:
            self.sprite.switch_state("idle")
            self.events = self.reset_events()
            return

        if move_vec.x * self.last_dir < 0:
            self.last_dir = -self.last_dir
            self.sprite.flip()

        self.sprite.switch_state("run")

        move_vec.scale_to_length(self.attributes["speed"])
        self.position.body.apply_force_at_local_point((move_vec.x, move_vec.y))

        self.events = self.reset_events()

    def handle_actions(self,
                       delta: float) -> None:

        aim_vec = -pygame.Vector2(200, 150) + pygame.mouse.get_pos()
        if self.events["primary"]["down"]:
            self.primary.attack(aim_vec)

        if self.events["dodge"]["down"]:
            self.start_dodge()

    def start_dodge(self):
        self.state["state"] = "dodge"
        self.state["time_left"] = self.attributes["dodge_duration"]
        self.sprite.switch_state("roll")

        impulse_vec = -pygame.Vector2(200, 150) + pygame.mouse.get_pos()
        impulse_vec.scale_to_length(self.attributes["dodge_impulse"])
        self.position.body.apply_impulse_at_local_point(tuple(impulse_vec))

    @staticmethod
    def reset_events() -> dict:
        events = {}
        for event_type in Resource.data["controls"]["InstanceGame"]:
            events[event_type] = {"down": False, "up": False, "pressed": False}

        return events

    def add_callbacks(self,
                      instance: BaseInstance):

        async def move_up():
            self.events["up"]["pressed"] = True

        async def move_down():
            self.events["down"]["pressed"] = True

        async def move_left():
            self.events["left"]["pressed"] = True

        async def move_right():
            self.events["right"]["pressed"] = True

        async def attack_primary():
            self.events["primary"]["down"] = True

        async def dodge():
            self.events["dodge"]["down"] = True

        instance.event_handler.register_callback("up", "pressed", move_up)
        instance.event_handler.register_callback("down", "pressed", move_down)
        instance.event_handler.register_callback("left", "pressed", move_left)
        instance.event_handler.register_callback("right", "pressed", move_right)
        instance.event_handler.register_callback("primary", "down", attack_primary)
        instance.event_handler.register_callback("dodge", "down", dodge)
