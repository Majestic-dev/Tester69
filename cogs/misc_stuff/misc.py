import discord
from discord import app_commands
from discord.ext import commands

class misc(commands.Cog):
    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot

    @app_commands.command(name="ping", description="Show my ping")
    async def ping(self, interaction: discord.Interaction):
        Ping = discord.Embed(
            title="Pong!",
            description=f"🏓 My ping is {round(self.bot.latency * 1000)}ms 🏓",
            colour=discord.Colour.green(),
        )

        await interaction.response.send_message(embed=Ping, ephemeral=True)
    
    @app_commands.command(name="source", description="Get the source code for the bot")
    @app_commands.checks.cooldown(1, 10, key=lambda i: (i.user.id))
    async def source(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            content="https://github.com/Majestic-dev/Tester69/tree/main", ephemeral=True
        )

async def setup(bot: commands.AutoShardedBot):
    await bot.add_cog(misc(bot))