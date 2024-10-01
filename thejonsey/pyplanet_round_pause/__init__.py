import logging

from pyplanet.apps.config import AppConfig
from pyplanet.contrib.command import Command

logger = logging.getLogger(__name__)


class PyplanetRoundPauseApp(AppConfig):
    game_dependencies = ["trackmania_next"]
    app_dependencies = ["core.maniaplanet", "core.trackmania"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_init(self):
        await super().on_init()

    async def on_start(self):
        await super().on_start()

        await self.instance.command_manager.register(Command(
            namespace="",
            command="pause",
            target=self.pause,
            admin=True,
            description="Pause the current round"
        ))
        await self.instance.command_manager.register(Command(
            namespace="",
            command="unpause",
            aliases=["endpause", "resume"],
            target=self.unpause,
            admin=True,
            description="Unpause"
        ))

    async def on_stop(self):
        await super().on_stop()

    async def on_destroy(self):
        await super().on_destroy()

    async def pause(self, player, data, *args, **kwargs):
        if (await self.instance.gbx.script("Maniaplanet.Pause.GetStatus"))["available"]:
            await self.instance.gbx.script("Maniaplanet.Pause.SetActive", "True", encode_json=False)

    async def unpause(self, player, data, *args, **kwargs):
        if (await self.instance.gbx.script("Maniaplanet.Pause.GetStatus"))["available"]:
            await self.instance.gbx.script("Maniaplanet.Pause.SetActive", "False", encode_json=False)
