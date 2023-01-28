from discord.ext import commands
from typing import Literal, Optional
from discord.ext import commands
from discord.ext.commands import Greedy, Context
import json
import os
import discord
from dotenv import load_dotenv
load_dotenv()

if not os.path.isfile("data/users.json"):
    with open("data/users.json", "w") as f:
        json.dump({}, f)

intents = discord.Intents.all()
intents.members = True
whitelist = ["705435835306213418"]
owners = [705435835306213418]

bot_prefix = "'"
bot = commands.Bot(command_prefix = bot_prefix, intents = intents)
bot.remove_command("help")

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(f"'help - https://discord.gg/VsDDf8YKBV"))
    await bot.load_extension("extensions.commands.MainStuff")
    await bot.load_extension("extensions.commands.WarningSystem")
    await bot.load_extension("extensions.commands.Economy")
    await bot.load_extension("extensions.commands.Moderation")
    await bot.load_extension("extensions.commands.Gambling")

@bot.command()
@commands.guild_only()
@commands.is_owner()
async def sync(
  ctx: Context, guilds: Greedy[discord.Object], spec: Optional[Literal["~", "*", "^"]] = None) -> None:
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

users = {}

try:
    with open('data/users.json', 'r') as f:
        users = json.load(f)
except:
    print('Could not load data')

def save_data():
    with open('data/users.json', 'w') as f:
        json.dump(users, f, indent=4)

bot.run(os.getenv('TOKEN'))