import discord
from discord import app_commands
from discord.ext import commands

from utils import data_manager, cooldown_check, UserData


class timed_claims(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="hourly", description="Gain 1000 🪙 every time you use this command"
    )
    async def hourly(self, interaction: discord.Interaction):
        user_data: UserData = await data_manager.get_user_data(interaction.user.id)

        if await cooldown_check(
            interaction.user.id,
            "<:white_cross:1096791282023669860> You already claimed your hourly coins",
            "hourly",
            3600,
        ):
            await data_manager.edit_user_data(
                interaction.user.id, "balance", user_data["balance"] + 1000
            )
            await interaction.response.send_message(
                embed=discord.Embed(
                    description="<:white_checkmark:1096793014287995061> You received 1000 🪙",
                    colour=discord.Colour.green(),
                )
            )

    @app_commands.command(
        name="daily", description="Gain 10000 🪙 every time you use this command"
    )
    async def daily(self, interaction: discord.Interaction):
        user_data: UserData = await data_manager.get_user_data(interaction.user.id)

        if await cooldown_check(
            interaction.user.id,
            "<:white_cross:1096791282023669860> You already claimed your daily coins",
            "daily",
            86400,
        ):
            await data_manager.edit_user_data(
                interaction.user.id, "balance", user_data["balance"] + 10000
            )
            await interaction.response.send_message(
                embed=discord.Embed(
                    description="<:white_checkmark:1096793014287995061> You received 10000 🪙",
                    colour=discord.Colour.green(),
                )
            )

    @app_commands.command(
        name="weekly", description="Gain 25000 🪙 every time you use the command"
    )
    async def weekly(self, interaction: discord.Interaction):
        user_data: UserData = await data_manager.get_user_data(interaction.user.id)

        if await cooldown_check(
            interaction.user.id,
            "<:white_cross:1096791282023669860> You already claimed your weekly coins",
            "weekly",
            604800,
        ):
            await data_manager.edit_user_data(
                interaction.user.id, "balance", user_data["balance"] + 25000
            )
            await interaction.response.send_message(
                embed=discord.Embed(
                    description="<:white_checkmark:1096793014287995061> You received 25000 🪙",
                    colour=discord.Colour.green(),
                )
            )

    @app_commands.command(
        name="monthly", description="Gain 50000 🪙 every time you use the command"
    )
    async def monthly(self, interaction: discord.Interaction):
        user_data: UserData = await data_manager.get_user_data(interaction.user.id)

        if await cooldown_check(
            interaction.user.id,
            "<:white_cross:1096791282023669860> You already claimed your monthly coins",
            "monthly",
            2592000,
        ):
            await data_manager.edit_user_data(
                interaction.user.id, "balance", user_data["balance"] + 50000
            )
            await interaction.response.send_message(
                embed=discord.Embed(
                    description="<:white_checkmark:1096793014287995061> You received 50000 🪙",
                    colour=discord.Colour.green(),
                )
            )

async def setup(bot: commands.AutoShardedBot):
    await bot.add_cog(timed_claims(bot))