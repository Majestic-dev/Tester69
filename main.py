import asyncio
import logging

import discord
from discord.ext import commands

from typing import Tuple

from utils import DataManager

initial_extensions: Tuple[str, ...] = (
    "cogs.giveaway_system",
    "cogs.server_management"
)
class Bot(commands.Bot):
    def __init__(self) -> None:
        intents = discord.Intents.all()
        super().__init__(
            command_prefix="'",
            owner_id=705435835306213418,
            intents=intents
        )

    async def setup_hook(self) -> None:
        for extension in initial_extensions:
            await bot.load_extension(extension)
        await bot.tree.sync()

bot = Bot()
handler = logging.FileHandler(
    filename="data/discord.log",
    encoding="utf-8",
    mode="w"
)

@bot.event
async def on_ready() -> None:
    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Game("https://discord.gg/VsDDf8YKBV")
    )

async def main():
    await DataManager.initialise()
    
    discord.utils.setup_logging(handler=handler, level=logging.INFO)
    await bot.start(DataManager.get("config", "token"))

if __name__ == "__main__":
    asyncio.run(main())
    