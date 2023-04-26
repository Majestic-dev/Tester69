from datetime import datetime

import discord
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
            colour=discord.Colour.green(),
        )

        await interaction.response.send_message(embed=Ping, ephemeral=True)

    @app_commands.command(name="prefix", description="Show my prefix")
    async def prefix(self, interaction: discord.Interaction):
        Prefix = discord.Embed(
            title="Prefix",
            description="Tester69 uses slash commands, enter `/` or `/help` and you will see all the available commands",
            colour=discord.Colour.light_gray(),
        )

        await interaction.response.send_message(embed=Prefix, ephemeral=True)

    @app_commands.command(name="help", description="Get the basic help for commands")
    async def help(self, interaction: discord.Interaction):
        help = discord.Embed(
            title="Tetser69's command list",
            colour=discord.Colour.darker_gray(),
        )

        help.add_field(name="Moderation", value="`/moderation`", inline=True)
        help.add_field(name="Economy", value="`/economy`", inline=True)
        help.add_field(name="Gambling", value="`/gambling`", inline=True)
        help.add_field(
            name="Server Management", value="`/servermanagement`", inline=True
        )
        help.add_field(name="Main", value="`/main`", inline=True)
        help.add_field(
            name="Support",
            value=f"Need more help? Join our community [server](https://discord.gg/VsDDf8YKBV) to get more help",
            inline=False,
        )

        await interaction.response.send_message(embed=help, ephemeral=True)

    @app_commands.command(
        name="moderation", description="Get all current moderation commands"
    )
    async def moderation(self, interaction: discord.Interaction):
        moderation = discord.Embed(
            title="Tester69's moderation commands",
            colour=discord.Colour.light_gray(),
        )
        moderation.add_field(name="Kick", value="`/kick`", inline=True)
        moderation.add_field(name="Mute", value="`/mute`", inline=True)
        moderation.add_field(name="Unmute", value="`/unmute`", inline=True)
        moderation.add_field(name="Ban", value="`/ban`", inline=True)
        moderation.add_field(name="Unban", value="`/unban`", inline=True)
        moderation.add_field(name="Warnings", value="`/warnings`", inline=True)
        moderation.add_field(name="Warn", value="`/warn`", inline=True)
        moderation.add_field(name="Delwarn", value="`/delwarn`", inline=True)

        await interaction.response.send_message(embed=moderation, ephemeral=True)

    @app_commands.command(
        name="economy", description="Get all current economy commands"
    )
    async def economy(self, interaction: discord.Interaction):
        economy = discord.Embed(
            title="Tester69's economy commands",
            colour=discord.Colour.light_gray(),
        )
        economy.add_field(name="Balance", value="`/balance`", inline=True)
        economy.add_field(name="Inventory", value="`/inventory`", inline=True)
        economy.add_field(name="Fish", value="`/fish`", inline=True)
        economy.add_field(name="Hourly", value="`/hourly`", inline=True)
        economy.add_field(name="Monthly", value="`/monthly`", inline=True)
        economy.add_field(name="Yearly", value="`/yearly`", inline=True)
        economy.add_field(name="Sell", value="`/sell`", inline=True)

        await interaction.response.send_message(embed=economy, ephemeral=True)

    @app_commands.command(
        name="gambling", description="Get all current gambling commands"
    )
    async def gambling(self, interaction: discord.Interaction):
        gambling = discord.Embed(
            title="Tester69's gambling commands",
            colour=discord.Colour.light_gray(),
        )
        gambling.add_field(name="Gamble", value="`/gamble`", inline=True)
        gambling.add_field(name="Blackjack", value="`/blackjack`", inline=True)
        gambling.add_field(name="Snakeeyes", value="`/snakeeyes`", inline=True)
        gambling.add_field(name="Coinflip", value="`/coinflip`", inline=True)

        await interaction.response.send_message(embed=gambling, ephemeral=True)

    @app_commands.command(name="main", description="Get all current main commands")
    async def misc(self, interaction: discord.Interaction):
        misc = discord.Embed(
            title="Tester69's misc commands",
            colour=discord.Colour.light_gray(),
        )
        misc.add_field(name="Ping", value="`/ping`", inline=True)
        misc.add_field(name="Prefix", value="`/prefix`", inline=True)
        misc.add_field(name="Help", value="`/help`", inline=True)

        await interaction.response.send_message(embed=misc, ephemeral=True)

    @app_commands.command(
        name="servermanagement",
        description="Get all current server management commands",
    )
    async def servermanagement(self, interaction: discord.Interaction):
        servermanagement = discord.Embed(
            title="Tester69's server management commands",
            colour=discord.Colour.light_gray(),
        )

        servermanagement.add_field(
            name="Set Logging Channel", value="`/set_logging_channel`", inline=True
        )
        servermanagement.add_field(
            name="Disable Logging System", value="`/logging disable`", inline=True
        )
        servermanagement.add_field(
            name="Setup Verification", value="`/verification setup`", inline=True
        )
        servermanagement.add_field(
            name="Disable Verification", value="`/verification disable`", inline=True
        )
        servermanagement.add_field(name="Slowmode", value="`/slowmode`", inline=True)
        servermanagement.add_field(
            name="Create A Channel", value="`/create_channel`", inline=True
        )
        servermanagement.add_field(
            name="Delete A Channel", value="`/delete_channel`", inline=True
        )
        servermanagement.add_field(name="Purge", value="`/purge`", inline=True)
        servermanagement.add_field(
            name="Add A Blacklisted Word", value="`/add_blacklisted_word`", inline=True
        )
        servermanagement.add_field(
            name="Remove A Blacklisted Word",
            value="`/remove_blacklisted_word`",
            inline=True,
        )
        servermanagement.add_field(
            name="Add A Whitelisted User", value="`/whitelist_add`", inline=True
        )
        servermanagement.add_field(
            name="Remove A Whitelisted User", value="`/whitelist_remove`", inline=True
        )
        servermanagement.add_field(
            name="Set A Welcome Message", value="`/set_welcome_message`", inline=True
        )
        servermanagement.add_field(
            name="Disable Welcome Message",
            value="`/disable_welcome_message`",
            inline=True,
        )

        await interaction.response.send_message(embed=servermanagement, ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(MainStuff(bot))
