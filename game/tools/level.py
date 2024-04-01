from isec.app import Resource
from isec.instance import BaseInstance
from isec.environment.base import OrthogonalTilemap
from isec.environment.scene import EntityScene, OrthogonalTilemapScene

from isec.environment import Entity
from isec.environment.sprite.pymunk_sprite import PymunkSprite

from game.entities.player import Player


class Level:
    def __init__(self,
                 linked_instance: BaseInstance,
                 phase: str = "phase_1") -> None:

        self.linked_instance = linked_instance

        tileset = OrthogonalTilemap.create_tileset_from_surface(Resource.image["tileset"], 32)

        # Scenes
        self.floor_scene = OrthogonalTilemapScene(OrthogonalTilemap([[]], tileset))
        self.walls_scene = OrthogonalTilemapScene(OrthogonalTilemap([[]], tileset),
                                                  camera=self.floor_scene.camera)
        self.entity_scene = EntityScene(self.linked_instance.fps,
                                        camera=self.floor_scene.camera)

        # Entities
        self.player = Player((20, 20), self.entity_scene, self.linked_instance)
        self.player_debug = Entity(self.player.position, PymunkSprite(self.player.position, "static"), self.entity_scene, self)
        self.create_level(phase)

    def create_level(self,
                     phase: str) -> None:

        phase_dict = Resource.data["level"][phase]
        self.floor_scene.tilemap.tilemap_array = Resource.get_nested(phase_dict["floor"])
        self.walls_scene.tilemap.tilemap_array = Resource.get_nested(phase_dict["walls"])

    def update(self) -> None:
        delta = self.linked_instance.delta

    def render(self) -> None:
        self.floor_scene.render()
        self.walls_scene.render()
        self.entity_scene.render()
        delta = self.linked_instance.delta
