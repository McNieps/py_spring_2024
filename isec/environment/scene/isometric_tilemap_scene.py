import pygame
import numpy
import math

from isec.app import Resource
from isec.environment.base import IsometricTilemap
from isec.environment.base.scene import Scene
from isec.environment.base.camera import Camera


class IsometricTilemapScene(Scene):
    def __init__(self,
                 tilemap: IsometricTilemap,
                 surface: pygame.Surface = None,
                 camera: Camera = None) -> None:

        super().__init__(surface, camera)
        self.tilemap = tilemap

    def render(self,
               camera: Camera = None) -> None:

        if camera is None:
            camera = self.camera

        tile_size = self.tilemap.tile_size

        camera_pos = pygame.Vector2(math.floor(camera.position.x),
                                    math.floor(camera.position.y))

        # r for row, c for column
        print(tile_size)
        r_min = math.floor(self.camera.position.y/tile_size[1]*2)
        r_max = math.ceil(self.surface.get_height()/tile_size[1]*2)+r_min+2
        c_min = math.floor(self.camera.position.x/tile_size[0]*2)
        c_max = math.ceil(self.surface.get_width()/tile_size[0]*2)+c_min+2  # Need more work to take height into account

        # r & c: row and column, i & j: tile pos in tilemap, x & y: tile pos in viewspace
        for r in range(r_min, r_max):
            for c in range(c_min, c_max):
                if (c + r) % 2 != 0:
                    continue

                i = (r + c)//2
                j = (r - c)//2

                if i < 0 or j < 0 or i > self.tilemap.width or j > self.tilemap.height:
                    pass  # continue

                x = math.floor(c*tile_size[0]/2 - camera.position.x - tile_size[0]/2)
                y = math.floor(r*tile_size[1]/2 - camera.position.y - tile_size[1]/2)
                # tile
                self.surface.blit(self.tilemap.tileset[0], (x, y))

        return


        start_x = max(0, math.floor(camera_pos[0]/tile_size[0]))  # NOQA
        end_x = min(math.ceil((camera_pos[0]+self.rect.width)/tile_size[0]), self.tilemap.width)
        start_y = max(0, math.floor(camera_pos[1]/tile_size[1]))
        end_y = min(math.ceil((camera_pos[1]+self.rect.height)/tile_size[1]), self.tilemap.height)

        pos_x = numpy.floor(numpy.arange(end_x) * self.tilemap.tile_size[0] - camera_pos[0])
        pos_y = numpy.floor(numpy.arange(end_y) * self.tilemap.tile_size[1] - camera_pos[1])

        self.surface.fblits([(self.tilemap.tileset[self.tilemap[y][x]], (pos_x[x], pos_y[y]))
                             for x in range(start_x, end_x)
                             for y in range(start_y, end_y)
                             if self.tilemap[y][x] != -1])

        return

    def update(self,
               delta: float) -> None:
        pass
