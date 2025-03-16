import discord
from discord.ext import commands

from discord import app_commands

from utils import DataManager


class appealing(commands.GroupCog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="set_link",
        description="Set the appeal link that will be sent to users who get banned",
    )
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(manage_guild=True)
    @app_commands.checks.cooldown(1, 600, key=lambda i: (i.guild.id, i.user.id))
    @app_commands.describe(
        appeal_link="The appeal link to set (sent to users who get banned)"
    )
    async def set_appeal_link(self, interaction: discord.Interaction, appeal_link: str):
        await DataManager.edit_guild_data(
            interaction.guild.id, "appeal_link", f"{appeal_link}"
        )
        await interaction.response.send_message(
            embed=discord.Embed(
                description=f"<:white_checkmark:1096793014287995061> Set the appeal link to {appeal_link}",
                colour=discord.Colour.green(),
            )
        )

    @app_commands.command(
        name="disable",
        description="Disable the appeal link that will be sent to users who get banned",
    )
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(manage_guild=True)
    @app_commands.checks.cooldown(1, 600, key=lambda i: (i.guild.id, i.user.id))
    async def disable_appealing(self, interaction: discord.Interaction):
        await DataManager.edit_guild_data(interaction.guild.id, "appeal_link", None)
        await interaction.response.send_message(
            embed=discord.Embed(
                description=f"<:white_checkmark:1096793014287995061> Disabled appealing",
                colour=discord.Colour.green(),
            )
        )