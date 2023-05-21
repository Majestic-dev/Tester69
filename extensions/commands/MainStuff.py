from datetime import datetime

import discord
from discord import app_commands
from discord.ext import commands


class MainStuff(commands.Cog):
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
        economy.add_field(name="Pay", value="`/pay`", inline=True)
        economy.add_field(name="Deposit", value="`/deposit`", inline=True)
        economy.add_field(name="Withdraw", value="`/withdraw`", inline=True)
        economy.add_field(name="Balance", value="`/balance`", inline=True)
        economy.add_field(name="Inventory", value="`/inventory`", inline=True)
        economy.add_field(name="Fish", value="`/fish`", inline=True)
        economy.add_field(name="Hourly", value="`/hourly`", inline=True)
        economy.add_field(name="Daily", value="`/daily`", inline=True)
        economy.add_field(name="Weekly", value="`/weekly`", inline=True)
        economy.add_field(name="Monthly", value="`/monthly`", inline=True)
        economy.add_field(name="Shop", value="`/shop`", inline=True)
        economy.add_field(name="Sell", value="`/sell`", inline=True)
        economy.add_field(name="Buy", value="`/buy_item`", inline=True)
        economy.add_field(name="Leaderboard", value="`/leaderboard`", inline=True)

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
    async def main(self, interaction: discord.Interaction):
        main = discord.Embed(
            title="Tester69's main commands",
            colour=discord.Colour.light_gray(),
        )
        main.add_field(name="Ping", value="`/ping`", inline=True)
        main.add_field(name="Prefix", value="`/prefix`", inline=True)
        main.add_field(name="Help", value="`/help`", inline=True)

        await interaction.response.send_message(embed=main, ephemeral=True)

    @app_commands.command(name="misc", description="Get all current misc commands")
    async def misc(self, interaction: discord.Interaction):
        misc = discord.Embed(
            title="Tester69's misc commands",
            colour=discord.Colour.light_gray(),
        )
        misc.add_field(name="Server info", value="`/serverinfo`", inline=True)
        misc.add_field(name="User info", value="`/userinfo`", inline=True)
        misc.add_field(name="Role info", value="`/roleinfo`", inline=True)
        misc.add_field(name="Channel info", value="`/channelinfo`", inline=True)
        misc.add_field(name="Member count", value="`/membercount`", inline=True)
        misc.add_field(name="Avatar", value="`/avatar`", inline=True)
        misc.add_field(name="Server icon", value="`/servericon`", inline=True)
        misc.add_field(name="Server banner", value="`/serverbanner`", inline=True)
        misc.add_field(name="Search a Gif", value="`/search_giphy`", inline=True)
        misc.add_field(name="Search an Image", value="`/search_unsplash`", inline=True)
        misc.add_field(name="Get a Cat Image", value="`/cat`", inline=True)
        misc.add_field(name="Get a Dog Image", value="`/dog`", inline=True)
        misc.add_field(name="Get a Dad Joke", value="`/dadjoke`", inline=True)
        misc.add_field(name="Search Wikipedia", value="`/wikipedia`", inline=True)
        misc.add_field(name="Search Urban Dictionary", value="`/urban`", inline=True)
        misc.add_field(name="Get a Github Profile", value="`/github`", inline=True)
        misc.add_field(name="Get Covid Stats", value="`/covid`", inline=True)
        misc.add_field(name="Weather", value="`/weather`", inline=True)
        misc.add_field(name="Weather Forecast", value="`/forecast`", inline=True)

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


async def setup(bot: commands.AutoShardedBot):
    await bot.add_cog(MainStuff(bot))
