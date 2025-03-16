from typing import Optional

import discord
from discord import app_commands
from discord.ext import commands

from utils import DataManager


class logging(commands.GroupCog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="set_channel",
        description="Set where all server logs will be sent and optionally where all blocked words will be sent",
    )
    @app_commands.describe(
        logging_channel="Choose the channel where all server logs will be sent",
        blocked_words_channel="Choose the channel where all blocked words will be sent",
    )
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.checks.cooldown(1, 10, key=lambda i: (i.user.id))
    async def set_logs_channel(
        self,
        interaction: discord.Interaction,
        logging_channel: discord.TextChannel,
        blocked_words_channel: Optional[discord.TextChannel] = None,
    ):
        if blocked_words_channel == None:
            data = await DataManager.get_filter_data(interaction.guild.id)
            if data["channel_id"] != None:
                await DataManager.edit_filter_data(
                    interaction.guild.id, "channel_id", None
                )

            await interaction.response.send_message(
                embed=discord.Embed(
                    description=f"<:white_checkmark:1096793014287995061> Set the logging channel to {logging_channel.mention}",
                    colour=discord.Colour.green(),
                )
            )

            await DataManager.edit_guild_data(
                interaction.guild.id, "logs_channel_id", logging_channel.id
            )

        elif blocked_words_channel != None:
            await interaction.response.send_message(
                embed=discord.Embed(
                    description=f"<:white_checkmark:1096793014287995061> Set the logging channel to {logging_channel.mention} and the blocked words channel to {blocked_words_channel.mention}",
                    colour=discord.Colour.green(),
                )
            )

            await DataManager.edit_guild_data(
                interaction.guild.id, "logs_channel_id", logging_channel.id
            )

            await DataManager.edit_filter_data(
                interaction.guild.id, "channel_id", blocked_words_channel.id
            )

    @app_commands.command(name="disable", description="Disable logging for this server")
    @app_commands.checks.has_permissions(administrator=True)
    async def disable_logs(self, interaction: discord.Interaction):
        guild_data = await DataManager.get_guild_data(interaction.guild.id)
        logs_channel = self.bot.get_channel(guild_data["logs_channel_id"])

        if logs_channel == None:
            return await interaction.response.send_message(
                ephemeral=True,
                embed=discord.Embed(
                    description="<:white_cross:1096791282023669860> Logging is already disabled",
                    colour=discord.Colour.red(),
                ),
            )

        else:
            await DataManager.edit_guild_data(
                interaction.guild.id, "logs_channel_id", None
            )
            return await interaction.response.send_message(
                ephemeral=True,
                embed=discord.Embed(
                    title="Logging Disabled",
                    description="Logging has been disabled for this server",
                    colour=discord.Colour.red(),
                ),
            )