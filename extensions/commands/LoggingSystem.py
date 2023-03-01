from datetime import datetime
from typing import Union

import discord
from discord import app_commands
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
        guild_data = DataManager.get_guild_data(interaction.guild.id)
        logs_channel = self.bot.get_channel(guild_data["logs_channel_id"])

        if command.name == "slowmode":
            channel = interaction.namespace.channel
            slowmode = interaction.namespace.slowmode
            if slowmode == 0:
                return await logs_channel.send(
                    embed=discord.Embed(
                        title="Slowmode Disabled",
                        description=f"{interaction.user.mention} Disabled slowmode in {channel.mention}",
                        timestamp=datetime.now(),
                        colour=discord.Colour.green(),
                    )
                )

            return await logs_channel.send(
                embed=discord.Embed(
                    title="Slowmode Set",
                    description=f"{interaction.user.mention} Set the slowmode to {slowmode} seconds in {channel.mention}",
                    timestamp=datetime.now(),
                    colour=discord.Colour.green(),
                )
            )

        elif command.name == "create_text_channel":
            TextChannel = discord.Embed(
                title="Text Channel Created",
                description=f"{interaction.user.mention} created a text channel named `{interaction.namespace.name}`",
                timestamp=datetime.now(),
                colour=discord.Colour.green(),
            )

            if not (interaction.namespace.category) is None:
                TextChannel.add_field(
                    name="Category",
                    value=f"{interaction.namespace.category}",
                    inline=True,
                )
            if (interaction.namespace.slowmode) == 0:
                TextChannel.add_field(
                    name="Slowmode", value="Slowmode disabled", inline=True
                )
            if (interaction.namespace.slowmode) == 1:
                TextChannel.add_field(
                    name="Slowmode", value=f"{slowmode} second", inline=True
                )
            if (interaction.namespace.slowmode) != 1 and 0:
                TextChannel.add_field(
                    name="Slowmode",
                    value=f"{interaction.namespace.slowmode} seconds",
                    inline=True,
                )

            if len(TextChannel.fields) == 0:
                return await logs_channel.send(
                    embed=discord.Embed(
                        title="Text Channel Created",
                        description=f"{interaction.user.mention} created a text channel named `{interaction.namespace.name}`",
                        timestamp=datetime.now(),
                        colour=discord.Colour.green(),
                    )
                )
            await logs_channel.send(embed=TextChannel)

        if command.name == "create_voice_channel":
            VoiceChannel = discord.Embed(
                title="Voice Channel Created",
                description=f"{interaction.user.mention} created a voice channel named `{interaction.namespace.name}`",
                timestamp=datetime.now(),
                colour=discord.Colour.green(),
            )

            if not (interaction.namespace.category is None):
                VoiceChannel.add_field(
                    name="Category",
                    value=f"{interaction.namespace.category}",
                    inline=True,
                )
            if (interaction.namespace.userlimit) == 0:
                VoiceChannel.add_field(
                    name="User Limit", value="No user limit", inline=True
                )
            if (interaction.namespace.userlimit) == 1:
                VoiceChannel.add_field(
                    name="User Limit",
                    value=f"{interaction.namespace.userlimit} user",
                    inline=True,
                )
            if (interaction.namespace.userlimit) != 1 and 0:
                VoiceChannel.add_field(
                    name="User Limit",
                    value=f"{interaction.namespace.userlimit} users",
                    inline=True,
                )

            if len(VoiceChannel.fields) == 0:
                return await logs_channel.send(
                    embed=discord.Embed(
                        title="Voice Channel Created",
                        description=f"{interaction.user.mention} created a voice channel named `{interaction.namespace.name}`",
                        timestamp=datetime.now(),
                        colour=discord.Colour.green(),
                    )
                )

            await logs_channel.send(embed=VoiceChannel)

        if command.name == "delete_text_channel":
            ChannelDelete = discord.Embed(
                title="Channel Deleted",
                description=f"{interaction.user.mention} deleted `{interaction.namespace.channel}` channel",
                timestamp=datetime.now(),
                colour=discord.Colour.green(),
            )

            if not (interaction.namespace.reason) == None:
                ChannelDelete.add_field(
                    name="Reason", value=f"{interaction.namespace.reason}", inline=True
                )

            if len(ChannelDelete.fields) == 0:
                return await logs_channel.send(
                    embed=discord.Embed(
                        title="Channel Deleted",
                        description=f"{interaction.user.mention} deleted `{interaction.namespace.channel}` channel with no reason provided",
                        timestamp=datetime.now(),
                        colour=discord.Colour.green(),
                    )
                )

            await logs_channel.send(embed=ChannelDelete)

        if command.name == "delete_voice_channel":
            ChannelDelete = discord.Embed(
                title="Channel Deleted",
                description=f"{interaction.user.mention} deleted `{interaction.namespace.channel}` voice channel",
                timestamp=datetime.now(),
                colour=discord.Colour.green(),
            )

            if not (interaction.namespace.reason) == None:
                ChannelDelete.add_field(
                    name="Reason", value=f"{interaction.namespace.reason}", inline=True
                )

            if len(ChannelDelete.fields) == 0:
                return await logs_channel.send(
                    embed=discord.Embed(
                        title="Channel Deleted",
                        description=f"{interaction.user.mention} deleted `{interaction.namespace.channel}` voice channel with no reason provided",
                        timestamp=datetime.now(),
                        colour=discord.Colour.green(),
                    )
                )

            await logs_channel.send(embed=ChannelDelete)


async def setup(bot):
    await bot.add_cog(LoggingSystem(bot))
