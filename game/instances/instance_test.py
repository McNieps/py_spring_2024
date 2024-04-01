import pygame

from isec.app import Resource
from isec.instance import BaseInstance, LoopHandler
from isec.environment.scene.orthogonal_tilemap_scene import OrthogonalTilemapScene, OrthogonalTilemap
from isec.environment import Entity, Sprite, EntityScene
from isec.environment.position import SimplePos


class InstanceTest(BaseInstance):
    def __init__(self):
        super().__init__(6000)
        # Tilemap
        self.tileset = {0: Resource.image["planks_soil"], 1: Resource.image["planks_portal"]}
        size = 20
        wall_height = 106  # 24
        self.tilemap_array = [[0 for _ in range(size)] for _ in range(size)]
        self.tilemap_array[10][10] = 1
        self.tilemap = OrthogonalTilemap(self.tilemap_array, self.tileset)
        self.tilemap_scene = OrthogonalTilemap(self.tilemap)

        # Entities
        self.entity_scene = EntityScene(60)

        # Camera
        self.entity_scene.camera = self.iso_tilemap_scene.camera
        self.create_callback()

    async def loop(self):
        LoopHandler.fps_caption()

        # Rendering
        self.window.fill((51, 28, 23))
        iso_rect_viewspace = self.iso_tilemap_scene.renderable_rect()
        self.entity_scene.z_sort()
        self.entity_scene.update(self.delta)
        last_row = None

        for row in range(iso_rect_viewspace.top, iso_rect_viewspace.bottom):
            # print(row)

            if isinstance(last_row, int):
                print("i")
                last_row += 1
            self.entity_scene.render_iso_range(row_min=last_row, row_max=row+1)
            self.iso_tilemap_scene.render_row(row,
                                              iso_rect_viewspace.left,
                                              iso_rect_viewspace.right)
            last_row = row

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

        async def up():
            self.movable_entity.position.y -= 2*self.delta
            self.movable_entity.position.x -= 2*self.delta

        async def down():
            self.movable_entity.position.y += 2*self.delta
            self.movable_entity.position.x += 2*self.delta

        async def left():
            self.movable_entity.position.x -= self.delta
            self.movable_entity.position.y += self.delta

        async def right():
            self.movable_entity.position.x += self.delta
            self.movable_entity.position.y -= self.delta

        self.event_handler.register_keypressed_callback(pygame.K_z, move_up)
        self.event_handler.register_keypressed_callback(pygame.K_q, move_left)
        self.event_handler.register_keypressed_callback(pygame.K_s, move_down)
        self.event_handler.register_keypressed_callback(pygame.K_d, move_right)

        self.event_handler.register_keypressed_callback(pygame.K_UP, up)
        self.event_handler.register_keypressed_callback(pygame.K_LEFT, left)
        self.event_handler.register_keypressed_callback(pygame.K_DOWN, down)
        self.event_handler.register_keypressed_callback(pygame.K_RIGHT, right)
