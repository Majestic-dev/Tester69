from datetime import datetime
from typing import Optional

import discord
from discord import app_commands
from discord.ext import commands
from discord.abc import GuildChannel

from utils import DataManager


class ServerManagement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="set_logs_channel", description="Set where all logs will be sent"
    )
    @app_commands.default_permissions(administrator=True)
    async def set_logs_channel(
        self, interaction: discord.Interaction, channel: discord.TextChannel
    ):
        await interaction.response.send_message(
            embed=discord.Embed(
                title="Logs Channel Set!",
                description=f"Logs channel set to {channel.mention}",
                timestamp=datetime.utcnow(),
                colour=discord.Colour.green(),
            )
        )

        DataManager.edit_guild_data(interaction.guild.id, "logs_channel_id", channel.id)

    @app_commands.command(
        name="slowmode", description="Set the slowmode in the channel of your choice"
    )
    @app_commands.default_permissions(manage_channels=True)
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
                    timestamp=datetime.utcnow(),
                    colour=discord.Colour.orange(),
                )
            )

        if slowmode == 0:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="Slowmode Disabled!",
                    description=f"Successfully disabled slowmode in {channel.mention}",
                    timestamp=datetime.utcnow(),
                    colour=discord.Colour.green(),
                )
            )

        await interaction.response.send_message(
            embed=discord.Embed(
                title="Slowmode Set!",
                description=f"Successfully set the slowmode to {slowmode} seconds in {channel.mention}",
                timestamp=datetime.utcnow(),
                colour=discord.Colour.green(),
            )
        )

    @app_commands.command(
        name="create_channel",
        description="Create a channel with the name of your choice",
    )
    @app_commands.default_permissions(manage_channels=True)
    async def create_channel(
        self,
        interaction: discord.Interaction,
        channeltype: discord.ChannelType,
        name: str,
        category: Optional[discord.CategoryChannel],
        slowmode: Optional[int  ],
    ):

        guild_data = DataManager.get_guild_data(interaction.guild.id)
        logs_channel = self.bot.get_channel(guild_data["logs_channel_id"])

        if logs_channel == None:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="No Logs Channel",
                    description="Please set a channel where all logs will be sent. `/set_logs_channel`",
                    timestamp=datetime.utcnow(),
                    colour=discord.Colour.orange(),
                )
            )
        
        channel = await interaction.guild._create_channel(
        name=name, channel_type=channeltype, category=category, slowmode_delay=slowmode,
    )
        channel = interaction.guild.get_channel(int(channel["id"]))
        TextChannel = discord.Embed(
        title="Channel Created!",
        description=f"Successfully created text channel {channel.mention}",
        timestamp=datetime.utcnow(),
        colour=discord.Colour.green(),
    )

        if not (category) is None:
            TextChannel.add_field(name="Category", value=f"{category}", inline=True)

        if slowmode == 1:
            TextChannel.add_field(
                name="Slowmode", value=f"{slowmode} second", inline=True
            )
        if slowmode != 1 and slowmode == 0:
            TextChannel.add_field(
                name="Slowmode", value=f"{slowmode} seconds", inline=True
            )

        if len(TextChannel.fields) == 0:
            return await interaction.response.send_message(
            embed=discord.Embed(
                title="Channel Created!",
                description=f"Successfully created {channeltype} channel {channel.mention}",
                timestamp=datetime.utcnow(),
                colour=discord.Colour.green(),
            )
        )

        await interaction.response.send_message(embed=TextChannel)

    @app_commands.command(
        name="delete_channel", description="Delete the mentioned channel"
    )
    @app_commands.default_permissions(manage_channels=True)
    async def delete_channel(
        self,
        interaction: discord.Interaction,
        channel: GuildChannel,
        reason: str = None,
    ):
        guild_data = DataManager.get_guild_data(interaction.guild.id)
        logs_channel = self.bot.get_channel(guild_data["logs_channel_id"])

        if logs_channel == None:
            return await interaction.response.send_message(
            embed=discord.Embed(
                title="No Logs Channel",
                description="Please set a channel where all logs will be sent. `/set_logs_channel`",
                timestamp=datetime.utcnow(),
                colour=discord.Colour.orange(),
            )
        )

        await channel.delete(reason=reason)

        ChannelDelete = discord.Embed(
        title="Channel Deleted!",
        description=f"Successfully deleted `{channel}` channel",
        timestamp=datetime.utcnow(),
        colour=discord.Colour.green(),
    )

        if not (reason) == None:
            ChannelDelete.add_field(name="Reason", value=f"```{reason}```", inline=True)

        if len(ChannelDelete.fields) == 0:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="Channel Deleted!",
                    description=f"Successfully deleted `{channel}` channel with no reason provided",
                    timestamp=datetime.utcnow(),
                    colour=discord.Colour.green(),
                )
            )

        await interaction.response.send_message(embed=ChannelDelete)

    @app_commands.command(name="purge", description="Purge a custom amount of messages from this channel")
    @app_commands.default_permissions(manage_channels=True)
    async def purge(self, interaction: discord.Interaction, count: int):
        await interaction.response.defer()
        await interaction.channel.purge(limit=count+1)

        e = discord.Embed(
            title="Messages Purged!",
            description=f"Successfully purged {count} messages!",
            timestamp=datetime.utcnow(),
            colour=discord.Colour.green(),
        )

        return await interaction.edit_original_response(embed=e)
    
async def setup(bot):
    await bot.add_cog(ServerManagement(bot))
