from datetime import datetime
from typing import Optional

import discord
from discord import app_commands
from discord.ext import commands

from utils import DataManager


class ServerManagement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="set_logs_channel", description="Set where all logs will be sent"
    )
    @commands.has_permissions(administrator=True)
    async def set_logs_channel(
        self, interaction: discord.Interaction, channel: discord.TextChannel
    ):
        await interaction.response.send_message(
            embed=discord.Embed(
                title="Logs Channel Set!",
                description=f"Logs channel set to {channel.mention}.",
                timestamp=datetime.now(),
                colour=discord.Colour.green(),
            )
        )

        DataManager.edit_guild_data(interaction.guild.id, "logs_channel_id", channel.id)

    @app_commands.command(
        name="slowmode", description="Set the slowmode in the channel of your choice"
    )
    @commands.has_permissions(manage_channels=True)
    async def slowmode(
        self,
        interaction: discord.Interaction,
        channel: discord.TextChannel,
        slowmode: int,
    ):
        guild_data = DataManager.get_guild_data(interaction.guild.id)
        logs_channel = self.bot.get_channel(guild_data["logs_channel_id"])
        await channel.edit(reason="Slowmode command", slowmode_delay=slowmode)

        if logs_channel == None:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="No Logs Channel",
                    description="Please set a channel where all logs will be sent. `/set_logs_channel`",
                    timestamp=datetime.now(),
                    colour=discord.Colour.orange(),
                )
            )

        if slowmode == 0:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="Slowmode Disabled!",
                    description=f"Successfully disabled slowmode in {channel.mention}",
                    timestamp=datetime.now(),
                    colour=discord.Colour.green(),
                )
            )

        await interaction.response.send_message(
            embed=discord.Embed(
                title="Slowmode Set!",
                description=f"Successfully set the slowmode to {slowmode} seconds in {channel.mention}",
                timestamp=datetime.now(),
                colour=discord.Colour.green(),
            )
        )

    @app_commands.command(
        name="create_text_channel",
        description="Create a text channel with the name of your choice",
    )
    @commands.has_permissions(manage_channels=True)
    async def test(
        self,
        interaction: discord.Interaction,
        name: str,
        category: Optional[discord.CategoryChannel],
        slowmode: Optional[int],
    ):
        guild_data = DataManager.get_guild_data(interaction.guild.id)
        logs_channel = self.bot.get_channel(guild_data["logs_channel_id"])

        if logs_channel == None:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="No Logs Channel",
                    description="Please set a channel where all logs will be sent. `/set_logs_channel`",
                    timestamp=datetime.now(),
                    colour=discord.Colour.orange(),
                )
            )

        textchannel = await interaction.guild.create_text_channel(
            name=name, category=category, slowmode_delay=slowmode
        )
        TextChannel = discord.Embed(
            title="Channel Created!",
            description=f"Successfully created text channel {textchannel.mention}",
            timestamp=datetime.now(),
            colour=discord.Colour.green(),
        )

        if not (category) is None:
            TextChannel.add_field(name="Category", value=f"{category}", inline=True)
        if slowmode == 0:
            TextChannel.add_field(
                name="Slowmode", value="Slowmode disabled", inline=True
            )
        if slowmode == 1:
            TextChannel.add_field(
                name="Slowmode", value=f"{slowmode} second", inline=True
            )
        if slowmode != 1 and 0:
            TextChannel.add_field(
                name="Slowmode", value=f"{slowmode} seconds", inline=True
            )

        if len(TextChannel.fields) == 0:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="Channel Created!",
                    description=f"Successfully created text channel {textchannel.mention}",
                    timestamp=datetime.now(),
                    colour=discord.Colour.green(),
                )
            )

        await interaction.response.send_message(embed=TextChannel)

    @app_commands.command(
        name="create_voice_channel",
        description="Create a voice channel with the name of your choice",
    )
    @commands.has_permissions(manage_channels=True)
    async def create_voice_channel(
        self,
        interaction: discord.Interaction,
        name: str,
        category: Optional[discord.CategoryChannel],
        userlimit: Optional[int],
    ):
        guild_data = DataManager.get_guild_data(interaction.guild.id)
        logs_channel = self.bot.get_channel(guild_data["logs_channel_id"])

        if logs_channel == None:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="No Logs Channel",
                    description="Please set a channel where all logs will be sent. `/set_logs_channel`",
                    timestamp=datetime.now(),
                    colour=discord.Colour.orange(),
                )
            )

        voicechannel = await interaction.guild.create_voice_channel(
            name, category=category, user_limit=userlimit
        )
        VoiceChannel = discord.Embed(
            title="Voice Channel Created!",
            description=f"Successfully created voice channel {voicechannel.mention}",
            timestamp=datetime.now(),
            colour=discord.Colour.green()
        )

        if not (category is None):
            VoiceChannel.add_field(name="Category", value=f"{category.mention}", inline=True)
        if userlimit == 0:
            VoiceChannel.add_field(
                name="User Limit", value="No user limit", inline=True
            )
        if userlimit == 1:
            VoiceChannel.add_field(
                name="User Limit", value=f"{userlimit} user", inline=True
            )
        if userlimit != 1 and 0:
            VoiceChannel.add_field(
                name="User Limit", value=f"{userlimit} users", inline=True
            )

        if len(VoiceChannel.fields) == 0:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="Voice Channel Created!",
                    description=f"Successfully created voice channel {voicechannel.mention}",
                    timestamp=datetime.now(),
                    colour=discord.Colour.green(),
                )
            )

        await interaction.response.send_message(embed=VoiceChannel)

    @app_commands.command(
        name="delete_text_channel", description="Delete the mentioned text channel"
    )
    @commands.has_permissions(manage_channels=True)
    async def delete_text_channel(
        self,
        interaction: discord.Interaction,
        channel: discord.TextChannel,
        reason: str = None,
    ):
        guild_data = DataManager.get_guild_data(interaction.guild.id)
        logs_channel = self.bot.get_channel(guild_data["logs_channel_id"])

        if logs_channel == None:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="No Logs Channel",
                    description="Please set a channel where all logs will be sent. `/set_logs_channel`",
                    timestamp=datetime.now(),
                    colour=discord.Colour.orange(),
                )
            )

        await channel.delete(reason=reason)
        ChannelDelete = discord.Embed(
            title="Channel Deleted!",
            description=f"Successfully deleted `{channel}` text channel",
            timestamp=datetime.now(),
            colour=discord.Colour.green(),
        )

        if not (reason) == None:
            ChannelDelete.add_field(name="Reason", value=f"```{reason}```", inline=True)

        if len(ChannelDelete.fields) == 0:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="Channel Deleted!",
                    description=f"Successfully deleted `{channel}` text channel with no reason provided",
                    timestamp=datetime.now(),
                    colour=discord.Colour.green(),
                )
            )

        await interaction.response.send_message(embed=ChannelDelete)

    @app_commands.command(
        name="delete_voice_channel", description="Delete the mentioned voice channel"
    )
    @commands.has_permissions(manage_channels=True)
    async def delete_voice_channel(
        self,
        interaction: discord.Interaction,
        channel: discord.VoiceChannel,
        reason: str = None,
    ):
        guild_data = DataManager.get_guild_data(interaction.guild.id)
        logs_channel = self.bot.get_channel(guild_data["logs_channel_id"])

        if logs_channel == None:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="No Logs Channel",
                    description="Please set a channel where all logs will be sent. `/set_logs_channel`",
                    timestamp=datetime.now(),
                    colour=discord.Colour.orange(),
                )
            )

        await channel.delete(reason=reason)
        ChannelDelete = discord.Embed(
            title="Channel Deleted!",
            description=f"Successfully deleted `{channel}` voice channel",
            timestamp=datetime.now(),
            colour=discord.Colour.green(),
        )

        if not (reason) == None:
            ChannelDelete.add_field(name="Reason", value=f"```{reason}```", inline=True)

        if len(ChannelDelete.fields) == 0:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="Channel Deleted!",
                    description=f"Successfully deleted `{channel}` voice channel with no reason provided",
                    timestamp=datetime.now(),
                    colour=discord.Colour.green(),
                )
            )

        await interaction.response.send_message(embed=ChannelDelete)


async def setup(bot):
    await bot.add_cog(ServerManagement(bot))
