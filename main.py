import os
from typing import Literal, Optional

import discord
from discord.ext import commands

from utils import DataManager

DataManager(
    [
        ("guilds", "data/guilds.json", {}),
        ("users", "data/users.json", {}),
        (
            "config",
            "data/config.json",
            {"token": None, "global_whitelist": [], "owners": []},
        ),
        (
            "economy",
            "data/economy.json",
            {
                "hunt_items": {
                    "skunk": {"chance": 20, "price": 50},
                    "pig": {"chance": 15, "price": 100},
                    "cow": {"chance": 10, "price": 200},
                    "deer": {"chance": 7, "price": 300},
                    "bear": {"chance": 5, "price": 400},
                    "junk": {"chance": 2, "price": 25},
                    "treasure": {"chance": 0.5, "price": 10000},
                },
                "fish_items": {
                    "common fish": {"chance": 45, "price": 10},
                    "uncommon fish": {"chance": 30, "price": 20},
                    "rare fish": {"chance": 15, "price": 50},
                    "epic fish": {"chance": 7, "price": 200},
                    "legendary fish": {"chance": 1, "price": 1000},
                    "junk": {"chance": 0.9, "price": 25},
                    "treasure": {"chance": 0.1, "price": 10000},
                    "seaweed": {"chance": 1, "price": 25},
                },
                "sell_prices": {
                    "common fish": 5,
                    "uncommon fish": 10,
                    "rare fish": 25,
                    "epic fish": 100,
                    "legendary fish": 500,
                    "junk": 15,
                    "treasure": 10000,
                    "seaweed": 15,
                    "skunk": 5,
                    "pig": 10,
                    "cow": 25,
                    "deer": 150,
                    "bear": 200,
                },
            },
        ),
    ]
)

if "fonts" not in os.listdir("."):
    os.mkdir("fonts")

bot = commands.Bot(command_prefix="'", owner_id=705435835306213418, intents=discord.Intents.all())
bot.remove_command("help")

@bot.event
async def on_ready():
    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Game(f"/help - https://discord.gg/VsDDf8YKBV"),
    )

    for root, _, files in os.walk("extensions"):
        for file in files:
            if file.endswith(".py"):
                await bot.load_extension(root.replace("\\", ".") + "." + file[:-3])

    await bot.tree.sync()


@commands.guild_only()
@commands.is_owner()
async def sync(
    ctx: commands.Context,
    guilds: commands.Greedy[discord.Object],
    spec: Optional[Literal["~", "*", "^"]] = None,
) -> None:
    if not guilds:
        if spec == "~":
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "*":
            ctx.bot.tree.copy_global_to(guild=ctx.guild)
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "^":
            ctx.bot.tree.clear_commands(guild=ctx.guild)
            await ctx.bot.tree.sync(guild=ctx.guild)
            synced = []
        else:
            synced = await ctx.bot.tree.sync()

        await ctx.send(
            f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
        )
        return

    ret = 0
    for guild in guilds:
        try:
            await ctx.bot.tree.sync(guild=guild)
        except discord.HTTPException:
            pass
        else:
            ret += 1

    await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")


if DataManager.get("config", "token") is None:
    print("Please set your bot's token in data/config.json.")
else:
    bot.run(DataManager.get("config", "token"))
