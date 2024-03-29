import pygame

from isec.app import Resource
from isec.instance import BaseInstance, LoopHandler
from isec.environment.scene.isometric_tilemap_scene import IsometricTilemapScene, IsometricTilemap
from isec.environment import Entity, EntityScene, Pos, Sprite


class InstanceTest(BaseInstance):
    def __init__(self):
        super().__init__(6000)
        self.create_callback()

        self.tileset = {0: Resource.image["complex_soil"]}
        self.tilemap_array = [[-1, -1, -1, -1],
                              [ 0,  0,  0,  0],
                              [ 0, -1,  0,  0],
                              [ 0,  0,  0, -1]]

        self.tilemap = IsometricTilemap(self.tilemap_array, self.tileset)
        self.iso_tilemap_scene = IsometricTilemapScene(self.tilemap)
        self.entity_scene = EntityScene(60)
        self.entity_scene.add_entities(Entity(Pos(),
                                              Sprite(Resource.image["stock"]["face"]), self.entity_scene, self))

        self.entity_scene.camera = self.iso_tilemap_scene.camera

    async def loop(self):
        LoopHandler.fps_caption()
        self.window.fill((51, 28, 23))
        self.iso_tilemap_scene.render()
        self.entity_scene.render()

    def create_callback(self):
        speed = 100

        async def move_up():
            self.iso_tilemap_scene.camera.position.y -= speed * self.delta

        async def move_left():
            self.iso_tilemap_scene.camera.position.x -= speed * self.delta

        async def move_down():
            self.iso_tilemap_scene.camera.position.y += speed * self.delta

        async def move_right():
            self.iso_tilemap_scene.camera.position.x += speed * self.delta

        self.event_handler.register_keypressed_callback(pygame.K_z, move_up)
        self.event_handler.register_keypressed_callback(pygame.K_q, move_left)
        self.event_handler.register_keypressed_callback(pygame.K_s, move_down)
        self.event_handler.register_keypressed_callback(pygame.K_d, move_right)
