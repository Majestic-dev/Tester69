import asyncio
import os
import traceback

import discord
from discord import app_commands
from discord.ext import commands

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

if "fonts" not in os.listdir("."):
    os.mkdir("fonts")

bot = commands.AutoShardedBot(
    command_prefix="'", owner_id=705435835306213418, intents=discord.Intents.all()
)
bot.remove_command("help")


@bot.event
async def on_ready():
    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Game(f"/help | https://discord.gg/VsDDf8YKBV"),
    )

    try:
        for root, _, files in os.walk("extensions", "test"):
            for file in files:
                if file.endswith(".py"):
                    await bot.load_extension(root.replace("\\", ".") + "." + file[:-3])
    except commands.ExtensionAlreadyLoaded:
        pass
    await bot.tree.sync()


@bot.tree.error
async def on_app_command_error(
    interaction: discord.Interaction, error: app_commands.AppCommandError
):
    if isinstance(error, app_commands.CommandOnCooldown):
        return await interaction.response.send_message(
            delete_after=error.retry_after,
            ephemeral=True,
            embed=discord.Embed(
                description=f"<:white_cross:1096791282023669860> Wait {error.retry_after:.0f} seconds before using this command again.",
                colour=discord.Colour.red(),
            ),
        )
    else:
        return await bot.get_user(bot.owner_id).send(
            embed=discord.Embed(
                title="Error",
                description=f"```py\n{traceback.format_exc()}\n```",
                colour=discord.Colour.red(),
            )
        )


@bot.event
async def on_error(event, *args, **kwargs):
    return await bot.get_user(bot.owner_id).send(
        embed=discord.Embed(
            title="Error",
            description=f"```py\n{traceback.format_exc()}\n```",
            colour=discord.Colour.red(),
        )
    )


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return

    if isinstance(error, commands.NotOwner):
        return await ctx.reply(
            embed=discord.Embed(
                description="<:white_cross:1096791282023669860> You are not the owner of this bot",
                colour=discord.Colour.red(),
            )
        )

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
        await bot.start(DataManager.get("config", "token"))

if __name__ == "__main__":
    asyncio.run(main())