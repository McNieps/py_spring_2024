import asyncio

from isec.app import App
from game.instances.instance_game import InstanceGame


async def main() -> None:
    App.init("game/assets/")
    await InstanceGame().execute()


asyncio.run(main())
