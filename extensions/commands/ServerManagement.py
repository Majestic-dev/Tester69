import asyncio
from datetime import datetime
from typing import Optional

import discord
from discord import app_commands
from discord.abc import GuildChannel
from discord.enums import ChannelType
from discord.ext import commands

from utils import DataManager


class ServerManagement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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
    @app_commands.choices(
        channeltype=[
            app_commands.Choice(name="text", value=0),
            app_commands.Choice(name="voice", value=2),
            app_commands.Choice(name="category", value=4),
            app_commands.Choice(name="news", value=5),
            app_commands.Choice(name="stage_voice", value=13),
            app_commands.Choice(name="forum", value=15),
        ]
    )
    @app_commands.default_permissions(manage_channels=True)
    async def create_channel(
        self,
        interaction: discord.Interaction,
        channeltype: app_commands.Choice[int],
        name: str,
        category: Optional[discord.CategoryChannel],
        slowmode: Optional[int],
    ):
        guild_data = DataManager.get_guild_data(interaction.guild.id)
        logs_channel = self.bot.get_channel(guild_data["logs_channel_id"])
        channeltype = ChannelType(interaction.namespace.channeltype)

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
            name=name,
            channel_type=channeltype,
            category=category,
            slowmode_delay=slowmode,
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
        channeltype = discord.ChannelType

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
            description=f"Successfully deleted {channeltype} channel {channel} ",
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

    @app_commands.command(
        name="purge", description="Purge a custom amount of messages from this channel"
    )
    @app_commands.default_permissions(manage_channels=True)
    async def purge(self, interaction: discord.Interaction, count: int):
        await interaction.response.defer()
        await interaction.channel.purge(limit=count + 1)

        await asyncio.sleep(3)

        return await interaction.edit_original_response(
            embed=discord.Embed(
                title="Messages Purged!",
                description=f"Successfully purged {count} messages!",
                timestamp=datetime.utcnow(),
                colour=discord.Colour.green(),
            )
        )

    @app_commands.command(
        name="add_blacklisted_word",
        description="Add a word to the blacklisted words list.",
    )
    @app_commands.default_permissions(administrator=True)
    async def add_blacklisted_word(self, interaction: discord.Interaction, word: str):
        blacklisted_words = DataManager.get_guild_data(interaction.guild.id)[
            "blacklisted_words"
        ]

        if word.lower() in blacklisted_words:
            return await interaction.response.send_message(
                ephemeral=True,
                embed=discord.Embed(
                    title="Word Is Already In Blacklist",
                    description=f'Could not add "{word.lower()}" to blacklisted words list, because it already exists there',
                    timestamp=datetime.utcnow(),
                    colour=discord.Colour.orange(),
                ),
            )

        await interaction.response.send_message(
            ephemeral=True,
            embed=discord.Embed(
                title="Added Word To Blacklist",
                description=f'Successfully added "{word.lower()}" to blacklisted words list',
                timestamp=datetime.utcnow(),
                colour=discord.Colour.green(),
            ),
        )

        blacklisted_words.append(word.lower())
        DataManager.edit_guild_data(
            interaction.guild.id, "blacklisted_words", blacklisted_words
        )

    async def word_autocomplete(
        self, interaction: discord.Interaction, current: str
    ) -> list[app_commands.Choice[str]]:
        guild_data = DataManager.get_guild_data(interaction.guild.id)
        words_in_blacklist = guild_data["blacklisted_words"]

        return [
            app_commands.Choice(name=word, value=word) for word in words_in_blacklist
        ]

    @app_commands.command(
        name="remove_blacklisted_word",
        description="Remove a blacklisted word from the blacklisted words list.",
    )
    @app_commands.default_permissions(administrator=True)
    @app_commands.autocomplete(word=word_autocomplete)
    async def remove_blacklisted_word(
        self, interaction: discord.Interaction, word: str
    ):
        blacklisted_words = DataManager.get_guild_data(interaction.guild.id)[
            "blacklisted_words"
        ]

        if word not in blacklisted_words:
            return await interaction.response.send_message(
                ephemeral=True,
                embed=discord.Embed(
                    title="Could Not Remove Word From Blacklist",
                    description=f'Could not remove "{word.lower()}" from blacklisted words list, because it does not exist there',
                    timestamp=datetime.utcnow(),
                    colour=discord.Colour.orange(),
                ),
            )

        await interaction.response.send_message(
            ephemeral=True,
            embed=discord.Embed(
                title="Removed Word From Blacklist",
                description=f'Successfully removed "{word.lower()}" from blacklisted words list',
                timestamp=datetime.utcnow(),
                colour=discord.Colour.green(),
            ),
        )

        blacklisted_words.remove(word.lower())
        DataManager.edit_guild_data(
            interaction.guild.id, "blacklisted_words", blacklisted_words
        )

    @app_commands.command(
        name="whitelist_add", description="Add a user in the whitelist"
    )
    @app_commands.default_permissions(administrator=True)
    async def whitelist_add(
        self, interaction: discord.Interaction, whitelist: discord.User | discord.Role
    ):
        wlist = DataManager.get_guild_data(interaction.guild.id)["whitelist"]

        if whitelist.id in wlist:
            return await interaction.response.send_message(
                ephemeral=True,
                embed=discord.Embed(
                    title="User Already In Whitelist",
                    description=f"Could not add {whitelist.mention} to the whitelist because they already are in the whitelist",
                    timestamp=datetime.utcnow(),
                    colour=discord.Colour.orange(),
                ),
            )

        await interaction.response.send_message(
            ephemeral=True,
            embed=discord.Embed(
                title="Added Person To Whitelist",
                description=f"Successfully added {whitelist.mention} to whitelist",
                timestamp=datetime.utcnow(),
                colour=discord.Colour.green(),
            ),
        )

        wlist.append(whitelist.id)
        DataManager.edit_guild_data(interaction.guild.id, "whitelist", wlist)

        if isinstance(whitelist, discord.Role):
            return

        dm_channel = await whitelist.create_dm()
        await dm_channel.send(
            embed=discord.Embed(
                title="You Have Been Whitelisted!",
                description=f"You have been whitelisted in {interaction.guild.name} by {interaction.user.mention}",
                timestamp=datetime.utcnow(),
                colour=discord.Colour.green(),
            )
        )

    @app_commands.command(
        name="whitelist_remove", description="Remove a user from the whitelist"
    )
    @app_commands.default_permissions(administrator=True)
    async def whitelist_remove(
        self, interaction: discord.Interaction, whitelist: discord.User | discord.Role
    ):
        wlist = DataManager.get_guild_data(interaction.guild.id)["whitelist"]

        if whitelist.id not in wlist:
            return await interaction.response.send_message(
                ephemeral=True,
                embed=discord.Embed(
                    title="Could Not Remove User From Whitelist",
                    description=f"Could not remove {whitelist.mention} from the whitelist because they are not in it",
                    timestamp=datetime.utcnow(),
                    colour=discord.Colour.orange(),
                ),
            )

        await interaction.response.send_message(
            ephemeral=True,
            embed=discord.Embed(
                title="Removed User From Whitelist",
                description=f"Successfully removed {whitelist.mention} from whitelist",
                timestamp=datetime.utcnow(),
                colour=discord.Colour.green(),
            ),
        )

        wlist.remove(whitelist.id)
        DataManager.edit_guild_data(interaction.guild.id, "whitelist", wlist)

        if isinstance(whitelist, discord.Role):
            return

        dm_channel = await whitelist.create_dm()
        await dm_channel.send(
            embed=discord.Embed(
                title="You Have Been Removed From The Whitelist!",
                description=f"You have been removed from the whitelist in {interaction.guild.name} by {interaction.user.mention}",
                timestamp=datetime.utcnow(),
                colour=discord.Colour.red(),
            )
        )

    @app_commands.command(
        name="set_welcome_message",
        description="Add a welcome message that will be sent to users DMs when they join the server",
    )
    @app_commands.default_permissions(administrator=True)
    async def set_welcome_message(self, interaction: discord.Interaction, message: str):
        await interaction.response.send_message(
            embed=discord.Embed(
                title="Welcome Message Set",
                description=f"Welcome message set to: \n {message}",
                timestamp=datetime.utcnow(),
                colour=discord.Colour.green(),
            )
        )

        DataManager.edit_guild_data(interaction.guild.id, "welcome_message", message)

    @app_commands.command(
        name="disable_welcome_message",
        description="Disable the welcome message that is sent to users DMs when they join the server",
    )
    @app_commands.default_permissions(administrator=True)
    async def disable_welcome_message(self, interaction: discord.Interaction):
        DataManager.edit_guild_data(interaction.guild.id, "welcome_message", None)

        await interaction.response.send_message(
            embed=discord.Embed(
                title="Welcome Message Disabled",
                description=f"Welcome message has been disabled",
                timestamp=datetime.utcnow(),
                colour=discord.Colour.green(),
            )
        )


async def setup(bot):
    await bot.add_cog(ServerManagement(bot))
