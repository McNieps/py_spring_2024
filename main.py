import asyncio
import pygame

from isec.app import App
from game.instances.instance_game import InstanceGame


async def main() -> None:
    App.init("game/assets/")
    pygame.mixer.music.load("game/assets/sound/music.wav")
    pygame.mixer.music.set_volume(0.15)
    pygame.mixer.music.play(-1)
    await InstanceGame().execute()


asyncio.run(main())
