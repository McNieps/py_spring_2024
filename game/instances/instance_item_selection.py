import random
import pygame

from isec.app import Resource
from isec.environment import Entity, EntityScene, Sprite
from isec.environment.position import SimplePos
from isec.instance import BaseInstance, LoopHandler

from game.utils import Level
from game.items import item_dict


class InstanceItemSelection(BaseInstance):
    def __init__(self, level: Level):
        self.level = level
        self.player = level.player
        super().__init__(Resource.data["instance"]["game"]["fps"])
        self.scene = EntityScene(Resource.data["instance"]["game"]["fps"])

        elem_1, elem_2 = random.sample(list(item_dict.items()), 2)
        print(elem_1, elem_2)

        self.item_1 = elem_1[1]
        self.item_2 = elem_2[1]

        self.bg = pygame.transform.gaussian_blur(self.window, 1)
        self.bg.blit(Resource.image["gui"]["item_selection"], (50, 50))

        button_1 = Entity(SimplePos((115, 160)), Sprite(Resource.image["gui"][f"{elem_1[0]}_card"]))
        button_2 = Entity(SimplePos((285, 160)), Sprite(Resource.image["gui"][f"{elem_2[0]}_card"]))

        self.rect_1 = pygame.Rect((0, 0), (80, 150))
        self.rect_2 = pygame.Rect((0, 0), (80, 150))
        self.rect_1.center = (115, 160)
        self.rect_2.center = (285, 160)

        self.scene.add_entities(button_1, button_2)

    async def loop(self):
        for event in self.event_handler.events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if self.rect_1.collidepoint(*mouse_pos):  # NOQA
                    self.player.add_item(self.item_1(self.level))
                    LoopHandler.stop_instance(self)
                if self.rect_2.collidepoint(*mouse_pos):  # NOQA
                    self.player.add_item(self.item_2(self.level))
                    LoopHandler.stop_instance(self)
        self.window.blit(self.bg, (0, 0))
        LoopHandler.fps_caption()
        self.scene.render()
