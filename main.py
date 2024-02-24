import asyncio
import logging
import os
import aiohttp
import traceback

import discord
from discord import app_commands
from discord.ext import commands

from extensions.commands.giveaway import giveaway_views
from extensions.commands.ticket_system import (
    closed_ticket_views,
    panel_views,
    ticket_views,
)
from utils import DataManager

DataManager.setup(
    [
        (
            "data/config.json",
            {
                "token": None,
                "postgres_user": None,
                "postgres_password": None,
                "postgres_database": None,
                "giphy_key": None,
                "unsplash_key": None,
                "weather_api_key": None,
            },
        ),
        (
            "data/economy.json",
            {
                "items": {
                    "Example Item": {
                        "name": "Example Item",
                        "description": "> This is an example item, not meant to be used",
                        "type": "Example",
                        "sell price": 0,
                        "buy price": 0,
                        "emoji": "Use a discord emoji here",
                        "emoji_id": 0,
                    },
                },
                "hunting items": {
                    "Example Item": {"chance": 0},
                },
                "fishing items": {
                    "Example Item": {"chance": 0},
                },
                "shop items": {
                    "Example Item": {"price": 0},
                },
            },
        ),
    ]
)


class bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents().all()
        super().__init__(
            command_prefix="'",
            owner_id=705435835306213418,
            intents=intents,
        )

    async def setup_hook(self) -> None:
        self.add_view(giveaway_views(bot))
        self.add_view(panel_views(bot))
        tickets = await DataManager.get_all_tickets()
        panels = await DataManager.get_all_panels()

        try:
            for panel in panels:
                for ticket in tickets:
                    self.add_view(
                        view=closed_ticket_views(
                            bot,
                            panel["id"],
                            ticket["ticket_creator"],
                            ticket["ticket_id"],
                        )
                    )
                    self.add_view(
                        view=ticket_views(bot, panel["id"], ticket["ticket_creator"])
                    )
        except Exception as e:
            print(e)


bot = bot()
bot.remove_command("help")
handler = logging.FileHandler(
    filename="data/discord.log",
    encoding="utf-8",
    mode="w",
)

if "fonts" not in os.listdir("."):
    os.mkdir("fonts")


@bot.event
async def on_ready():
    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Game(f"/help | https://discord.gg/VsDDf8YKBV"),
    )

    for root, _, files in os.walk("extensions"):
        for file in files:
            if file.endswith(".py"):
                extension_name = root.replace("\\", ".") + "." + file[:-3]
                if extension_name in bot.extensions:
                    await bot.unload_extension(extension_name)
                try:
                    await bot.load_extension(extension_name)
                except discord.ext.commands.errors.ExtensionAlreadyLoaded:
                    await bot.reload_extension(extension_name)
    await bot.tree.sync()


@bot.tree.error
async def on_app_command_error(
    interaction: discord.Interaction, error: app_commands.AppCommandError
):
    await interaction.response.defer(ephemeral=True)

    if isinstance(error, app_commands.CommandOnCooldown):
        await interaction.edit_original_response(
            embed=discord.Embed(
                description=f"<:white_cross:1096791282023669860> Wait {error.retry_after:.0f} seconds before using this command again.",
                colour=discord.Colour.red(),
            ),
        )
        await asyncio.sleep(error.retry_after)
        return await interaction.delete_original_response()

    elif isinstance(error, app_commands.errors.MissingPermissions):
        return await interaction.edit_original_response(
            embed=discord.Embed(
                description="<:white_cross:1096791282023669860> You are missing the required permissions to use this command.",
                colour=discord.Colour.red(),
            ),
        )

    else:
        logging.error(f"An error occurred: {error}")

@bot.event
async def on_command_error(ctx: commands.Context, error: commands.CommandError):
    if isinstance(error, commands.CommandNotFound):
        return

    if isinstance(error, commands.NotOwner):
        return

    else:
        return await bot.get_user(bot.owner_id).send(
            embed=discord.Embed(
                description=f"```py\n{traceback.format_exc()}\n```",
                colour=discord.Colour.red(),
            )
        )


async def main():
    await DataManager.initialise()
    if None in [
        DataManager.get("config", key)
        for key in [
            "token",
            "postgres_user",
            "postgres_password",
            "postgres_database",
            "giphy_key",
            "unsplash_key",
            "weather_api_key",
        ]
    ]:
        print(f"Please fill out the config.json file before running {__file__}")
    else:
        discord.utils.setup_logging(handler=handler, level=logging.INFO)
        await bot.start(DataManager.get("config", "token"))


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except aiohttp.client_exceptions.ClientConnectorError as e:
        logging.warning(f"A network error occurred: {e}")