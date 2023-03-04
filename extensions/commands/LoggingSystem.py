from datetime import datetime
from typing import Union

import discord
from discord import ChannelType, app_commands
from discord.ext import commands

from utils import DataManager

from .ServerManagement import ServerManagement


class LoggingSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_app_command_completion(
        self,
        interaction: discord.Interaction,
        command: Union[app_commands.Command, app_commands.ContextMenu],
    ):
        ChannelType(interaction.namespace.channeltype)
        guild_data = DataManager.get_guild_data(interaction.guild.id)
        logs_channel = self.bot.get_channel(guild_data["logs_channel_id"])

        if command.name == "set_verification_channel":
            channel = interaction.namespace.channel
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

        if command.name == "create_channel":
            TextChannel = discord.Embed(
                title=f"{str(ChannelType(interaction.namespace.channeltype)).capitalize()} Channel Created",
                description=f"{interaction.user.mention} created a {ChannelType(interaction.namespace.channeltype)} channel named {interaction.namespace.name}",
                timestamp=datetime.utcnow(),
                colour=discord.Colour.green(),
            )

            TextChannel.add_field(
                name="Category",
                value=f"{interaction.namespace.category}",
                inline=True,
            )
            if (interaction.namespace.slowmode) == None or 0:
                TextChannel.add_field(
                    name="Slowmode", value="No slowmode set", inline=True
                )
            if (interaction.namespace.slowmode) == 1:
                TextChannel.add_field(
                    name="Slowmode", value=f"{slowmode} second", inline=True
                )
            if (interaction.namespace.slowmode) != 1 and (
                interaction.namespace.slowmode
            ) == 0:
                TextChannel.add_field(
                    name="Slowmode",
                    value=f"{interaction.namespace.slowmode} seconds",
                    inline=True,
                )

            await logs_channel.send(embed=TextChannel)

        if command.name == "delete_channel":
            ChannelDelete = discord.Embed(
                title="Channel Deleted",
                description=f"{interaction.user.mention} deleted `{interaction.namespace.channel}` channel",
                timestamp=datetime.utcnow(),
                colour=discord.Colour.green(),
            )

            if not (interaction.namespace.reason) == None:
                ChannelDelete.add_field(
                    name="Reason",
                    value=f"```{interaction.namespace.reason}```",
                    inline=True,
                )

            if len(ChannelDelete.fields) == 0:
                return await logs_channel.send(
                    embed=discord.Embed(
                        title="Channel Deleted",
                        description=f"{interaction.user.mention} deleted `{interaction.namespace.channel}` channel with no reason provided",
                        timestamp=datetime.utcnow(),
                        colour=discord.Colour.green(),
                    )
                )

            await logs_channel.send(embed=ChannelDelete)

        if command.name == "purge":
            return await logs_channel.send(
                embed=discord.Embed(
                    title="Messages Purged",
                    description=f"{interaction.user.mention} purged {interaction.namespace.count} messages",
                    timestamp=datetime.utcnow(),
                    colour=discord.Colour.green(),
                )
            )

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        guild_data = DataManager.get_guild_data(channel.guild.id)
        logs_channel = self.bot.get_channel(guild_data["logs_channel_id"])

        await logs_channel.send(
            embed=discord.Embed(
                title="Channel Created",
                description=f"Created {channel.mention} channel",
                timestamp=datetime.utcnow(),
                colour=discord.Colour.green(),
            )
        )


async def setup(bot):
    await bot.add_cog(LoggingSystem(bot))
