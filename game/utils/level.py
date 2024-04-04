import typing

from isec.app import Resource
from isec.instance import BaseInstance, LoopHandler
from isec.environment.base import OrthogonalTilemap, Camera, Entity
from isec.environment.scene import EntityScene, OrthogonalTilemapScene
from isec.environment.terrain import TerrainCollision

from game.utils.base_enemy import BaseEnemy
from game.utils.game_entity import GameEntity
from game.utils.shape_info import TerrainShapeInfo

from game.utils.spawner import Spawner
if typing.TYPE_CHECKING:
    from game.entities.player import Player


class Level:
    def __init__(self,
                 player: "Player",
                 linked_instance: BaseInstance,
                 spawnable_entities: list[GameEntity],
                 phase: str = "phase_1") -> None:

        self.linked_instance = linked_instance

        self.phase = phase

        self.spawner = Spawner(spawnable_entities, self)

        # Scenes
        tileset = OrthogonalTilemap.create_tileset_from_surface(Resource.image["tileset"], 32)
        self.camera = Camera()
        self.terrain_scenes = [OrthogonalTilemapScene(OrthogonalTilemap([[]], tileset), camera=self.camera),
                               OrthogonalTilemapScene(OrthogonalTilemap([[]], tileset), camera=self.camera),
                               OrthogonalTilemapScene(OrthogonalTilemap([[]], tileset), camera=self.camera)]
        self.entity_scene = EntityScene(self.linked_instance.fps, camera=self.camera)
        self.create_level(phase)

        # Entities
        self.player = player
        self.player.level = self
        self.enemies: list[BaseEnemy] = []
        self.entity_scene.add_entities(self.player, self.player.primary, *self.enemies)

    def update(self) -> None:
        delta = self.linked_instance.delta

        self.add_entities(*self.spawner.update(delta))

        for enemy in self.enemies:
            enemy.set_target(tuple(self.player.position.position))
        self.entity_scene.update(delta)

        self.entity_scene.camera.position.x = self.player.position.x-200
        self.entity_scene.camera.position.y = self.player.position.y-150

    def render(self) -> None:
        self.entity_scene.z_sort()
        self.linked_instance.window.fill((32, 32, 32))
        for terrain_scene in self.terrain_scenes:
            terrain_scene.render()

        self.entity_scene.render()

    def create_level(self,
                     phase: str) -> None:

        # Scene
        phase_dict = Resource.data["level"][phase]
        for i in range(len(phase_dict["terrain"])):
            self.terrain_scenes[i].tilemap.tilemap_array = Resource.get_nested(phase_dict["terrain"][i]["tilemap"])

            if phase_dict["terrain"][i]["solid"]:
                self.entity_scene.add_entities(*TerrainCollision.from_tilemap(self.terrain_scenes[i].tilemap,
                                                                              TerrainShapeInfo,
                                                                              show_collisions=False))

    def add_entities(self, *entities: Entity):
        self.entity_scene.add_entities(*entities)

    @property
    def entities(self) -> list[Entity]:
        return self.entity_scene.entities

    def add_callbacks(self):
        self.player.add_callbacks(self.linked_instance)
        self.linked_instance.event_handler.register_callback("quit", "down", LoopHandler.stop_game)
