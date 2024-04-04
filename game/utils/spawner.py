import typing
import random

import pygame

from isec.app import Resource

from game.utils.game_entity import GameEntity

if typing.TYPE_CHECKING:
    from game.utils.level import Level


class Spawner:
    def __init__(self,
                 spawnable_entities: list[typing.Type[GameEntity]],
                 level: "Level") -> None:

        self.level = level
        self.spawnable_entities = spawnable_entities
        self.waves = Resource.data["level"][level.phase]["waves"]
        self._time = 0
        self._time_since_last_spawn = 0
        self._current_wave_index = 0
        self._max_wave_index = len(self.waves)-1
        self._current_wave = self.waves[0]

    def update(self,
               delta: float) -> list[GameEntity]:

        self._time += delta
        self._time_since_last_spawn += delta

        self.update_wave()
        return self.handle_spawn()

    def update_wave(self) -> None:
        if self._time < self._current_wave["time"]:
            return

        if self._current_wave_index == self._max_wave_index:
            return

        self._current_wave_index += 1
        self._current_wave = self.waves[self._current_wave_index]
        self.update_wave()

    def handle_spawn(self) -> list[GameEntity]:
        if self._time_since_last_spawn < self._current_wave["every"]:
            return []

        self._time_since_last_spawn -= self._current_wave["every"]
        entities_to_spawn = []
        for entity_name, entity_quantity in self._current_wave["entities"].items():
            for _ in range(entity_quantity):
                entities_to_spawn.append(self.spawnable_entities[entity_name](self.level, self.choose_position()))  # NOQA

        entities_to_spawn.extend(self.handle_spawn())
        return entities_to_spawn

    def choose_position(self) -> tuple[int, int]:
        zone = self._current_wave["zone"]

        if isinstance(zone, list):
            if len(zone) == 2:
                return tuple(zone)

            if len(zone) == 4:
                return (random.randint(zone[0], zone[0]+zone[2]),
                        random.randint(zone[1], zone[1]+zone[3]))

        if isinstance(zone, str):
            if zone == "near":
                spawn_vec = self.level.player.position.position + pygame.Vector2(500, 0).rotate(random.randint(0, 360))
                return tuple(spawn_vec)

        err_msg = f"Invalid zone argument: {self._current_wave['zone']}"
        raise Exception(err_msg)
