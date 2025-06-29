import os
import discord

from discord.ext import commands

class reload_cogs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="reload", description="Reload the cogs in the bot")
    @commands.is_owner()
    async def reload(self, ctx):
        for root, _, files in os.walk("cogs"):
            for file in files:
                if not file.endswith(".py"):
                    continue

                ext_name = os.path.join(root, file[:-3]).replace(os.sep, ".")
                
                if (ext_name) in self.bot.extensions:
                    await self.bot.unload_extension(ext_name)
                    await self.bot.load_extension(ext_name)

        await ctx.reply(
            embed=discord.Embed(
                description="<:white_checkmark:1096793014287995061> Reloaded all cogs",
                colour=discord.Colour.green(),
            )
        )
        return await self.bot.tree.sync()
    
async def setup(bot: commands.AutoShardedBot):
    await bot.add_cog(reload_cogs(bot))