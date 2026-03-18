import datetime
import logging
import traceback
import typing
import aiohttp
import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

from core.command.loader import command_loader

load_dotenv()

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True

class Proto1Bot(commands.Bot):
    client: aiohttp.ClientSession
    _uptime: datetime.datetime = datetime.datetime.now(datetime.UTC)
    
    def __init__(self, prefix: str, ext_dir: str, *args: typing.Any, **kwargs: typing.Any) -> None:
        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True
        super().__init__(*args, **kwargs, command_prefix=commands.when_mentioned_or(prefix), intents=intents)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.ext_dir = ext_dir
        self.synced = False

    async def _load_extensions(self) -> None:
        await command_loader.load_extensions(self)

    async def on_error(self, event_method: str, *args: typing.Any, **kwargs: typing.Any) -> None:
        self.logger.error(f"An error occurred in {event_method}.\n{traceback.format_exc()}")

    async def on_ready(self) -> None:
        self.logger.info(f"Logged in as {self.user} ({self.user.id})")

    async def setup_hook(self) -> None:
        self.client = aiohttp.ClientSession()
        await self._load_extensions()
        if not self.synced:
            await self.tree.sync()
            self.synced = not self.synced
            self.logger.info("Synced command tree")

    async def close(self) -> None:
        await super().close()
        await self.client.close()

    def run(self, *args: typing.Any, **kwargs: typing.Any) -> None:
        load_dotenv()
        try:
            super().run(str(os.getenv("TOKEN")), *args, **kwargs)
        except (discord.LoginFailure, KeyboardInterrupt):
            self.logger.info("Exiting...")
            exit()

    @property
    def user(self) -> discord.ClientUser:
        assert super().user, "Bot is not ready yet"
        return typing.cast(discord.ClientUser, super().user)

    @property
    def uptime(self) -> datetime.timedelta:
        return datetime.datetime.now(datetime.UTC) - self._uptime


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s")
    bot = Proto1Bot(prefix="!", ext_dir="modules")
    
    bot.run()


if __name__ == "__main__":
    main()
