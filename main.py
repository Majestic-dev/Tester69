import os
import traceback

import discord
from discord import app_commands
from discord.ext import commands

from utils import DataManager

DataManager(
    [
        ("guilds", "data/guilds.json", {}),
        ("users", "data/users.json", {}),
        (
            "config",
            "data/config.json",
            {
                "token": None,
                "giphy_key": None,
                "unsplash_key": None,
                "weather_api_key": None,
            },
        ),
        (
            "economy",
            "data/economy.json",
            {
                "items": {
                    "skunk": {
                        "name": "Skunk",
                        "description": "> Skunks eat duck eggs. There is nothing else of importance to talk about with skunks.",
                        "type": "Animal",
                        "sell price": 325,
                        "buy price": 0,
                        "emoji": "<:skunk_item:1101063035793182760>",
                        "id": 1101063035793182760,
                    },
                    "rabbit": {
                        "name": "Rabbit",
                        "description": "> A rabbit is also known as a Bunny",
                        "type": "Animal",
                        "sell price": 125,
                        "buy price": 0,
                        "emoji": "<:rabbit_item:1101086856227078244>",
                        "id": 1101086856227078244,
                    },
                    "duck": {
                        "name": "Duck",
                        "description": "> A duck is a bird that is commonly found in ponds and lakes.",
                        "type": "Animal",
                        "sell price": 3000,
                        "buy price": 0,
                        "emoji": "<:duck_item:1101084032474808400>",
                        "id": 1101084032474808400,
                    },
                    "deer": {
                        "name": "Deer",
                        "description": "> A deer is a wild Animal that is commonly found in forests.",
                        "type": "Animal",
                        "sell price": 3750,
                        "buy price": 0,
                        "emoji": "<:deer_item:1101063041812008991>",
                        "id": 1101063041812008991,
                    },
                    "boar": {
                        "name": "Boar",
                        "description": "> A boar is a wild pig that is commonly found in forests.",
                        "type": "Animal",
                        "sell price": 2000,
                        "buy price": 0,
                        "emoji": "<:boar_item:1101087079183699978>",
                        "id": 1101087079183699978,
                    },
                    "junk": {
                        "name": "Junk",
                        "description": "> Junk is junk.",
                        "type": "Animal",
                        "sell price": 225,
                        "buy price": 0,
                        "emoji": "<:junk:1101084987744342016>",
                        "id": 1101084987744342016,
                    },
                    "dragon": {
                        "name": "Dragon",
                        "description": "> A dragon is a mythical creature that is commonly found in fantasy books.",
                        "type": "Animal",
                        "sell price": 100000,
                        "buy price": 0,
                        "emoji": "<:dragon_item:1101085869735153815>",
                        "id": 1101085869735153815,
                    },
                    "common fish": {
                        "name": "Common Fish",
                        "description": "> A common Fish is a Fish that is commonly found in ponds and lakes.",
                        "type": "Fish",
                        "sell price": 325,
                        "buy price": 0,
                        "emoji": "<:common_Fish:1101084306484514897>",
                        "id": 1101084306484514897,
                    },
                    "exotic fish": {
                        "name": "Exotic Fish",
                        "description": "> If this was Minecraft, this Fish would be used to feed a pet axolotl",
                        "type": "Fish",
                        "sell price": 650,
                        "buy price": 0,
                        "emoji": "<:exotic_Fish:1101086121275961414>",
                        "id": 1101086121275961414,
                    },
                    "rare fish": {
                        "name": "Rare Fish",
                        "description": "> Some say this is the most rare Fish in the sea! Until of course they catch a legendary Fish.",
                        "type": "Fish",
                        "sell price": 2500,
                        "buy price": 0,
                        "emoji": "<:rare_Fish:1101063038284603524>",
                        "id": 1101063038284603524,
                    },
                    "jelly fish": {
                        "name": "Jelly Fish",
                        "description": "> It stings.. yup, that's all!",
                        "type": "Fish",
                        "sell price": 7500,
                        "buy price": 0,
                        "emoji": "<:jelly_Fish:1101086630913253427>",
                        "id": 1101086630913253427,
                    },
                    "legendary fish": {
                        "name": "Legendary Fish",
                        "description": "> This is the most legendary Fish in the sea! Until of course they catch a kraken.",
                        "type": "Fish",
                        "sell price ": 30000,
                        "buy price": 0,
                        "emoji": "<a:legendary_Fish:1101063039769378816>",
                        "id": 1101063039769378816,
                    },
                    "kraken": {
                        "name": "Kraken",
                        "description": "> This is the most mythical creature in the sea.. But not for long 😈",
                        "type": "Fish",
                        "sell price": 100000,
                        "buy price": 0,
                        "emoji": "<:kraken:1101085322302988378>",
                        "id": 1101085322302988378,
                    },
                    "seaweed": {
                        "name": "Seaweed(https://github.com/Majestic-dev/Tester69",
                        "description": "> It's not as fun as land weed.. But you can still do something with it.. Right?",
                        "type": "Fish",
                        "sell price": 750,
                        "buy price": 0,
                        "emoji": "<a:seaaweed:1101085507020140645>",
                        "id": 1101085507020140645,
                    },
                    "fishing pole": {
                        "name": "Fishing Pole",
                        "description": "> It's no Bassmaster 2000 but it should do the job.",
                        "type": "Tool",
                        "sell price": 10000,
                        "buy price": 35000,
                        "emoji": "<:Fishing_pole:1101061913938509855>",
                        "id": 1101061913938509855,
                    },
                    "hunting rifle": {
                        "name": "Hunting Rifle",
                        "description": "> It's no Remington 700 but it should do the job.",
                        "type": "Tool",
                        "sell price": 10000,
                        "buy price": 35000,
                        "emoji": "<:hunting_rifle:1101060264713003028>",
                        "id": 1101060264713003028,
                    },
                },
                "hunting items": {
                    "skunk": {"chance": 50},
                    "rabbit": {"chance": 30},
                    "duck": {"chance": 10},
                    "deer": {"chance": 3},
                    "boar": {"chance": 4},
                    "junk": {"chance": 2},
                    "dragon": {"chance": 1},
                },
                "fishing items": {
                    "common fish": {"chance": 50},
                    "exotic fish": {"chance": 30},
                    "rare fish": {"chance": 10},
                    "jelly fish": {"chance": 3},
                    "legendary fish": {"chance": 4},
                    "kraken": {"chance": 1},
                    "seaweed": {"chance": 2},
                },
                "shop items": {
                    "hunting rifle": {"price": 35000},
                    "fishing pole": {"price": 35000},
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
        for root, _, files in os.walk("extensions"):
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
            embed=discord.Embed(
                description=f"<:white_cross:1096791282023669860> Wait {error.retry_after:.1f} seconds before using this command again.",
                colour=discord.Colour.red(),
            ),
        )
    else:
        return await bot.get_user(bot.owner_id).send(
            embed=discord.Embed(
                title="Error",
                description=f"If this error persists, DM <@705435835306213418> or mail them: `tester69.discord@gmail.com`\n```py\n{traceback.format_exc()}\n```",
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
        return await ctx.reply(
            embed=discord.Embed(
                description=f"<:white_cross:1096791282023669860> Command not found",
                colour=discord.Colour.red(),
            )
        )

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
                description=f"If this error persists, DM <@705435835306213418> or mail them: `tester69.discord@gmail.com`\n```py\n{traceback.format_exc()}\n```",
                colour=discord.Colour.red(),
            )
        )


if DataManager.get("config", "token") is None:
    print("Please set your bot's token in data/config.json.")
else:
    bot.run(DataManager.get("config", "token"))
