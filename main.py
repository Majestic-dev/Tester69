import asyncio
import logging
import os
import traceback
import time
import discord

from discord import app_commands
from discord.ext import commands

from utils import data_manager, cooldown_error

from cogs.giveaway_system.giveaway_commands import giveaway_views
from cogs.ticket_system.ticket_system import (
    closed_ticket_views,
    panel_views,
    ticket_views,
)

data_manager.setup(
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
                        "crafting_time": 1,  # How many minutes to craft this item (Not a required field)
                        "smelting_time": 1,  # How many minutes to forge this item (Not a mandatory field)
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
        (
            "data/recipes/crafting_recipes.json",
            {
                "recipes": {
                    "Example Item": {"Example resource": 1, "Example resource 2": 2}
                }
            },
        ),
        (
            "data/recipes/forging_recipes.json",
            {
                "recipes": {
                    "Example Item": {"Example resource": 1, "Example resource 2": 2}
                }
            },
        ),
        (
            "data/mine/mines.json",
            {
                "example mine": {
                    "requiredLevel": 0,
                    "mainOre": "example ore",
                    "secondaryOre": "example ore 2",
                    "emoji": "Use a discord emoji here",
                    "resources": {
                        "example resource": {"min": 1, "max": 2},
                    },
                },
            },
        ),
        (
            "data/mine/ores.json",
            {
                "ores": {
                    "example ore": {
                        "name": "Example Ore",
                        "emoji": "Use a discord emoji here",
                        "type": "Example type (e.g material, consumable, etc)",
                        "xp": 0,
                    },
                },
            },
        ),
    ]
)


class Bot(commands.Bot):
    def __init__(self) -> None:
        intents = discord.Intents.all()
        super().__init__(
            command_prefix="'", owner_id=705435835306213418, intents=intents
        )

    async def setup_hook(self) -> None:
        for root, _, files in os.walk("cogs"):
            for file in files:
                if not file.endswith(".py"):
                    continue

                await self.load_extension(
                    os.path.join(root, file[:-3]).replace(os.sep, ".")
                )
        await bot.tree.sync()

        self.add_view(giveaway_views(bot))
        self.add_view(panel_views(bot))
        tickets = await data_manager.get_all_tickets()
        panels = await data_manager.get_all_panels()

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


bot = Bot()
handler = logging.FileHandler(filename="data/discord.log", encoding="utf-8", mode="w")


@bot.tree.error
async def on_app_command_error(
    interaction: discord.Interaction, error: app_commands.AppCommandError
):
    await interaction.response.defer(ephemeral=True)

    if isinstance(error, app_commands.errors.MissingPermissions):
        return await interaction.edit_original_response(
            embed=discord.Embed(
                description="<:white_cross:1096791282023669860> You are missing the required permissions to use this command.",
                colour=discord.Colour.red(),
            ),
        )

    elif isinstance(error, app_commands.CommandOnCooldown):
        await interaction.edit_original_response(
            embed=discord.Embed(
                description=f"<:white_cross:1096791282023669860> You can use this command again <t:{int(time.time() + error.retry_after)}:R>",
                colour=discord.Colour.red(),
            ),
        )
        await asyncio.sleep(error.retry_after)
        try:
            return await interaction.delete_original_response()
        except:
            pass

    elif isinstance(error.original, cooldown_error):
        await interaction.edit_original_response(
            embed=discord.Embed(
                description=f"{error.original.error_message}, try again <t:{int(time.time() + error.original.time_left)}:R>",
                colour=discord.Colour.red(),
            ),
        )
        await asyncio.sleep(error.original.time_left)
        try:
            return await interaction.delete_original_response()
        except:
            pass

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
    await data_manager.initialise()

    discord.utils.setup_logging(handler=handler, level=logging.INFO)
    await bot.start(data_manager.get("config", "token"))


if __name__ == "__main__":
    asyncio.run(main())
