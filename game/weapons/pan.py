import time

import pygame
import random

from isec.app import Resource
from isec.environment import Sprite
from isec.environment.position import AdvancedPos, SimplePos

from game.utils.game_entity import GameEntity
from game.utils.base_enemy import BaseEnemy
from game.weapons.base_weapon import BaseWeapon, BaseProjectile


class PanProjectile(BaseProjectile):
    def __init__(self,
                 linked_weapon: BaseWeapon,
                 aim_vec: pygame.Vector2,
                 base_position: pygame.Vector2) -> None:

        self.half_size = (Resource.data["weapons"]["pan"]["animation_max_width"] +
                          Resource.data["weapons"]["pan"]["animation_radius"])

        super().__init__(linked_weapon,
                         aim_vec,
                         SimplePos(base_position),
                         Sprite(pygame.Surface((self.half_size*2, self.half_size*2), pygame.SRCALPHA)))

        self.start_time = time.time()

        self.rect = self.sprite.surface.get_rect()
        self.rect.center = base_position

        aim_angle = aim_vec.angle_to((1, 0))
        self.direction = random.randint(0, 1)*2-1
        self.start_angle = aim_angle - self.linked_weapon.attributes["swing_arc_length"]/2 * self.direction
        self.current_angle = self.start_angle
        self.anim_points = []

        self.sound = None

    def update(self,
               delta: float) -> None:

        super().update(delta)

        percent_in = (time.time()-self.start_time)/self.attributes["duration"]
        self.current_angle = self.start_angle + percent_in * self.attributes["swing_arc_length"] * self.direction

        if percent_in > 1:
            self.destroy()
            return

        if percent_in < 0.005:
            return

        self.draw_effect(percent_in)
        self.fade_effect(percent_in)
        self.linked_weapon.animation_angle = (percent_in-0.5) * self.attributes["swing_arc_length"] * self.direction
        self.check_hits()

    def draw_effect(self,
                    percent_in: float) -> None:

        self.sprite.surface.fill((255, 255, 255, 0))

        pos = pygame.Vector2(self.attributes["animation_radius"], 0)
        pos.rotate_ip(-self.current_angle)
        pos = pos + (self.half_size, self.half_size)

        self.anim_points.append((pos, percent_in))

        for pos, date in self.anim_points:
            pos_percentage = date/percent_in
            point_size = int(self.attributes["animation_max_width"]*pos_percentage)
            pygame.draw.circle(self.sprite.surface, (246, 205, 38), pos, point_size)

    def fade_effect(self,
                    percent_in: float) -> None:

        if self.attributes["animation_fade"] != 0 and percent_in > self.attributes["animation_fade"]:
            max_fade_time = 1-self.attributes["animation_fade"]
            alpha = (1-(percent_in-self.attributes["animation_fade"])/max_fade_time)*255
            self.sprite.surface.set_alpha(alpha)
            return

    def check_hits(self) -> None:
        if len(self.hit_entities) == self.attributes["max_hit"]:
            return

        for enemy in self.linked_weapon.linked_entity.level.entities:
            if len(self.hit_entities) == self.attributes["max_hit"]:
                return

            if not isinstance(enemy, BaseEnemy):
                continue

            if enemy in self.hit_entities:
                continue

            relative_pos = enemy.position.position - self.position.position
            if 1 <= relative_pos.length() <= self.attributes["radius"]:
                raw_diff = abs(relative_pos.angle_to((1, 0)) % 360 - self.current_angle % 360)
                if min(raw_diff, 360 - raw_diff) < 15:
                    relative_pos.scale_to_length(self.attributes["knockback"])
                    enemy.position.body.apply_impulse_at_local_point((tuple(relative_pos)))
                    enemy_killed = enemy.hit(self.attributes["damage"])
                    if self.sound is not None:
                        self.sound.play(Resource.sound["weapons"][f"pan_hit_{min(3, len(self.hit_entities))}"])
                    else:
                        self.sound = Resource.sound["weapons"][f"pan_hit_0"].play()
                    self.hit_entities.add(enemy)
                    # if enemy.to_delete:
                    #     self.on_kill(enemy)

    def on_kill(self,
                entity_killed: GameEntity) -> None:

        new_attack = PanProjectile(self.linked_weapon,
                                   self.aim_vec.copy(),
                                   entity_killed.position.position)

        self.linked_weapon.projectiles_to_spawn.append(new_attack)  # NOQA


class Pan(BaseWeapon):
    def __init__(self,
                 linked_entity: GameEntity) -> None:

        sprite = Sprite(Resource.image["sprite"]["weapons"]["pan"], "rotated")
        sprite.displayed = True
        super().__init__(linked_entity, AdvancedPos((0, 0), a=0), sprite)
        self.attributes = Resource.data["weapons"]["pan"]
        self.linked_entity = linked_entity
        self.projectiles_to_spawn = []
        self.sound = None
        self.animation_angle = 0
        self.time_since_last_attack = 1000

    def update(self,
               delta: float) -> None:

        self.time_since_last_attack += delta
        self.animation_angle *= 0.01 ** delta

        if self.sprite.displayed:
            self.flip_sprite()

            weapon_vec = -pygame.Vector2(200, 150) + pygame.mouse.get_pos()
            weapon_vec.rotate_ip(-self.animation_angle)
            if weapon_vec.length():
                weapon_vec.scale_to_length(15)
                self.position.x = self.linked_entity.position.x + weapon_vec.x
                self.position.y = self.linked_entity.position.y + weapon_vec.y - 3
                self.position.angle = weapon_vec.angle_to((1, 0))

            else:
                self.position.x, self.position.y = self.linked_entity.position.x, self.linked_entity.position.y

        for attack in self.projectiles_to_spawn:
            self.linked_entity.level.add_entities(attack)
        self.projectiles_to_spawn.clear()

    def attack(self,
               aim_vec: pygame.Vector2):

        if self.time_since_last_attack < self.attributes["attack_period"]:
            return

        self.time_since_last_attack = 0
        self.sound = Resource.sound["weapons"]["pan_swing"].play()
        self.projectiles_to_spawn.append(PanProjectile(self,
                                                       aim_vec,
                                                       self.linked_entity.position.position.copy()))
