import discord
from datetime import datetime
from discord import app_commands
from discord.ext import commands


class MainStuff(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="ping", description="Show my ping")
    async def ping(self, interaction: discord.Interaction):

        Ping = discord.Embed(
            title="Pong!",
            description=f"🏓 My ping is {round(self.bot.latency * 1000)}ms 🏓",
            timestamp=datetime.now(),
            colour=discord.Colour.green(),
        )

        await interaction.response.send_message(embed=Ping, ephemeral=True)

    @app_commands.command(name="prefix", description="Show my prefix")
    async def prefix(self, interaction: discord.Interaction):

        Prefix = discord.Embed(
            title="Prefix",
            description="Tester69 uses slash commands, enter `/` or `/help` and you will see all the available commands",
            timestamp=datetime.now(),
            colour=discord.Colour.light_gray(),
        )

        await interaction.response.send_message(embed=Prefix, ephemeral=True)

    @app_commands.command(name="help", description="Get the basic help for commands")
    async def help(self, interaction: discord.Interaction):

        help = discord.Embed(
            title="Tetser69's command list", 
            timestamp=datetime.now(),
            colour=discord.Colour.light_gray()
        )

        help.add_field(name="Moderation", value="`/moderation`", inline=True)
        help.add_field(name="Economy", value="`/economy`")

        await interaction.response.send_message(embed=help, ephemeral=True)

    @app_commands.command(
        name="moderation", description="Get all current moderation commands"
    )
    async def moderation(self, interaction: discord.Interaction):

        moderation = discord.Embed(
            title="Tester69's moderation commands", 
            timestamp=datetime.now(),
            colour=discord.Colour.darker_gray()
        )
        moderation.add_field(name="Kick", value="`/kick`", inline=True)
        moderation.add_field(name="Mute", value="`/mute`", inline=True)
        moderation.add_field(name="Unmute", value="`/unmute`", inline=True)
        moderation.add_field(name="RandomBan", value="`/randomban`", inline=True)
        moderation.add_field(name="Ban", value="`/ban`", inline=True)
        moderation.add_field(name="Unban", value="`/unban`", inline=True)
        moderation.add_field(name="Warn", value="`/warn`", inline=True)
        moderation.add_field(name="Delwarn", value="`/delwarn`", inline=True)

        await interaction.response.send_message(embed=moderation, ephemeral=True)

    @app_commands.command(
        name="economy", description="Get all current economy commands"
    )
    async def economy(self, interaction: discord.Interaction):

        economy = discord.Embed(
            title="Tester69's economy commands", 
            timestamp=datetime.now(),
            colour=discord.Colour.darker_grey()
        )
        economy.add_field(name="Balance", value="`/balance`", inline=True)
        economy.add_field(name="Inventory", value="`/inventory`", inline=True)
        economy.add_field(name="Fish", value="`/fish`", inline=True)
        economy.add_field(name="Hourly", value="`/hourly`", inline=True)
        economy.add_field(name="Monthly", value="`/monthly`", inline = True)
        economy.add_field(name="Sell", value="`/sell`", inline=True)
        economy.add_field(name="Gamble", value="`/gamble`", inline=True)
        economy.add_field(name="Snakeeyes", value="`/snakeeyes`", inline=True)
        economy.add_field(name="Blackjack", value="`/blackjack`", inline=True)

        await interaction.response.send_message(embed=economy, ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(MainStuff(bot))
