from datetime import datetime
from typing import Union

import discord
from discord import ChannelType, app_commands
from discord.ext import commands

from utils import DataManager

from .ServerManagement import ServerManagement


class Logging(commands.GroupCog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="set_channel", description="Set where all server logs will be sent"
    )
    @app_commands.default_permissions(administrator=True)
    async def set_logs_channel(
        self, interaction: discord.Interaction, channel: discord.TextChannel
    ):
        await interaction.response.send_message(
            embed=discord.Embed(
                title="Logging Channel Set!",
                description=f"Logging channel set to {channel.mention}",
                timestamp=datetime.utcnow(),
                colour=discord.Colour.green(),
            )
        )

        DataManager.edit_guild_data(interaction.guild.id, "logs_channel_id", channel.id)

    @app_commands.command(name="disable", description="Disable logging for this server")
    @app_commands.default_permissions(administrator=True)
    async def disable_logs(self, interaction: discord.Interaction):
        guild_data = DataManager.get_guild_data(interaction.guild.id)
        logs_channel = self.bot.get_channel(guild_data["logs_channel_id"])

        if logs_channel == None:
            return await interaction.response.send_message(
                ephemeral=True,
                embed=discord.Embed(
                    title="Logging Already Disabled",
                    description="Logging is already disabled",
                    timestamp=datetime.utcnow(),
                    colour=discord.Colour.red(),
                ),
            )

        else:
            DataManager.edit_guild_data(interaction.guild.id, "logs_channel_id", None)
            return await interaction.response.send_message(
                ephemeral=True,
                embed=discord.Embed(
                    title="Logging Disabled",
                    description="Logging has been disabled for this server",
                    timestamp=datetime.utcnow(),
                    colour=discord.Colour.red(),
                ),
            )

    @commands.Cog.listener()
    async def on_app_command_completion(
        self,
        interaction: discord.Interaction,
        command: Union[app_commands.Command, app_commands.ContextMenu],
    ):
        guild_data = DataManager.get_guild_data(interaction.guild.id)
        logs_channel = self.bot.get_channel(guild_data["logs_channel_id"])

        if logs_channel is None:
            return

        if command.name == "set_verification_channel":
            channel = interaction.namespace.channel

            verification_channel = self.bot.get_channel(
                guild_data["verification_channel_id"]
            )
            if verification_channel == None:
                return

            return await logs_channel.send(
                embed=discord.Embed(
                    title="Verification Channel Set",
                    description=f"{interaction.user.mention} Set the verification channel to {channel.mention}",
                    timestamp=datetime.utcnow(),
                    colour=discord.Colour.green(),
                )
            )

        if command.name == "set_verification_logs_channel":
            channel = interaction.namespace.channel

            verification_logs_channel = self.bot.get_channel(
                guild_data["verification_logs_channel_id"]
            )
            if verification_logs_channel == None:
                return

            return await logs_channel.send(
                embed=discord.Embed(
                    title="Verification Logs Channel Set",
                    description=f"{interaction.user.mention} Set the verification logs channel to {channel.mention}",
                    timestamp=datetime.utcnow(),
                    colour=discord.Colour.green(),
                )
            )

        if command.name == "set_unverified_role":
            role = interaction.namespace.role

            unverified_role = self.bot.get_guild(interaction.guild.id).get_role(
                guild_data["unverified_role_id"]
            )
            if unverified_role == None:
                return

            return await logs_channel.send(
                embed=discord.Embed(
                    title="Unverified Role Set",
                    description=f"{interaction.user.mention} Set the unverified role to {role.mention}",
                    timestamp=datetime.utcnow(),
                    colour=discord.Colour.green(),
                )
            )

        if command.name == "slowmode":
            channel = interaction.namespace.channel
            slowmode = interaction.namespace.slowmode
            if slowmode == 0:
                return await logs_channel.send(
                    embed=discord.Embed(
                        title="Slowmode Disabled",
                        description=f"{interaction.user.mention} Disabled slowmode in {channel.mention}",
                        timestamp=datetime.utcnow(),
                        colour=discord.Colour.green(),
                    )
                )

            return await logs_channel.send(
                embed=discord.Embed(
                    title="Slowmode Set",
                    description=f"{interaction.user.mention} Set the slowmode to {slowmode} seconds in {channel.mention}",
                    timestamp=datetime.utcnow(),
                    colour=discord.Colour.green(),
                )
            )

        if command.name == "purge":
            return await logs_channel.send(
                embed=discord.Embed(
                    title="Messages Purged",
                    description=f"{interaction.user.mention} purged {interaction.namespace.count} messages",
                    timestamp=datetime.utcnow(),
                    colour=discord.Colour.green(),
                )
            )


async def setup(bot):
    await bot.add_cog(Logging(bot))
