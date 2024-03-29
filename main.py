import asyncio

from isec.app import App
from game.instances.instance_test import InstanceTest


async def main() -> None:
    App.init("game/assets/")
    await InstanceTest().execute()


asyncio.run(main())
