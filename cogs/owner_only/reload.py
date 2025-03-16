import os
import discord

from discord.ext import commands

class reload_cogs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="reload", description="Reload the cogs in the bot")
    @commands.is_owner()
    async def reload(self, ctx):
        for folder in os.listdir("cogs"):
            extension_name = f"cogs.{folder}"
            if extension_name in self.bot.extensions:
                await self.bot.unload_extension(extension_name)
            try:
                    await self.bot.load_extension(extension_name)
            except Exception as e:
                print(f"Failed to load {extension_name}: {e}")
                await self.bot.reload_extension(extension_name)

        await ctx.reply(
            embed=discord.Embed(
                description="<:white_checkmark:1096793014287995061> Reloaded all cogs",
                colour=discord.Colour.green(),
            )
        )
        return await self.bot.tree.sync()