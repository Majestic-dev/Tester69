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
    @app_commands.checks.cooldown(1, 10, key=lambda i: (i.guild.id, i.user.id))
    async def slowmode(
        self,
        interaction: discord.Interaction,
        channel: Optional[discord.TextChannel],
        slowmode: int,
    ):
        if channel == None:
            channel = interaction.channel
        await channel.edit(reason="Slowmode command", slowmode_delay=slowmode)

        if slowmode == 0:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    description=f"<:white_checkmark:1096793014287995061> Disabled slowmode in {channel.mention}",
                    colour=discord.Colour.green(),
                )
            )

        await interaction.response.send_message(
            embed=discord.Embed(
                description=f"<:white_checkmark:1096793014287995061> Set the slowmode to {slowmode} seconds in {channel.mention}",
                colour=discord.Colour.green(),
            )
        )

    @slowmode.error
    async def on_slowmode_error(
        self, interaction: discord.Interaction, error: app_commands.AppCommandError
    ):
        if isinstance(error, app_commands.CommandOnCooldown):
            await interaction.response.send_message(
                ephemeral=True,
                embed=discord.Embed(
                    description=f"<:white_cross:1096791282023669860> Wait {error.retry_after:.1f} seconds before using this command again.",
                    colour=discord.Colour.red(),
                ),
            )

    @app_commands.command(
        name="set_appeal_link",
        description="Set the appeal link that will be sent to users who get banned",
    )
    @app_commands.default_permissions(manage_guild=True)
    @app_commands.checks.cooldown(1, 600, key=lambda i: (i.guild.id, i.user.id))
    async def set_appeal_link(self, interaction: discord.Interaction, appeal_link: str):
        DataManager.edit_guild_data(
            interaction.guild.id, "appeal_link", f"{appeal_link}"
        )
        await interaction.response.send_message(
            embed=discord.Embed(
                description=f"<:white_checkmark:1096793014287995061> Set the appeal link to {appeal_link}",
                colour=discord.Colour.green(),
            )
        )

    @set_appeal_link.error
    async def on_set_appeal_link_error(
        self, interaction: discord.Interaction, error: app_commands.AppCommandError
    ):
        if isinstance(error, app_commands.CommandOnCooldown):
            await interaction.response.send_message(
                ephemeral=True,
                embed=discord.Embed(
                    description=f"<:white_cross:1096791282023669860> Wait {error.retry_after:.1f} seconds before using this command again.",
                    colour=discord.Colour.red(),
                ),
            )

    @app_commands.command(
        name="disable_appealing",
        description="Disable the appeal link that will be sent to users who get banned",
    )
    @app_commands.default_permissions(manage_guild=True)
    @app_commands.checks.cooldown(1, 600, key=lambda i: (i.guild.id, i.user.id))
    async def disable_appealing(self, interaction: discord.Interaction):
        guild_data = DataManager.get_guild_data(interaction.guild.id)
        DataManager.edit_guild_data(interaction.guild.id, "appeal_link", None)
        await interaction.response.send_message(
            embed=discord.Embed(
                description=f"<:white_checkmark:1096793014287995061> Disabled appealing",
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
    @app_commands.checks.cooldown(1, 20, key=lambda i: (i.guild.id, i.user.id))
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

        channel = await interaction.guild._create_channel(
            name=name,
            channel_type=channeltype,
            category=category,
            slowmode_delay=slowmode,
        )
        channel = interaction.guild.get_channel(int(channel["id"]))
        TextChannel = discord.Embed(
            description=f"<:white_checkmark:1096793014287995061> Created text channel {channel.mention}",
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
                    description=f"<:white_checkmark:1096793014287995061> Created {channeltype} channel {channel.mention}",
                    colour=discord.Colour.green(),
                )
            )

        await interaction.response.send_message(embed=TextChannel)

    @create_channel.error
    async def on_create_channel_error(
        self, interaction: discord.Interaction, error: app_commands.AppCommandError
    ):
        if isinstance(error, app_commands.CommandOnCooldown):
            await interaction.response.send_message(
                ephemeral=True,
                embed=discord.Embed(
                    description=f"<:white_cross:1096791282023669860> Wait {error.retry_after:.1f} seconds before using this command again.",
                    colour=discord.Colour.red(),
                ),
            )

    @app_commands.command(
        name="delete_channel", description="Delete the mentioned channel"
    )
    @app_commands.default_permissions(manage_channels=True)
    @app_commands.checks.cooldown(1, 10, key=lambda i: (i.guild.id, i.user.id))
    async def delete_channel(
        self,
        interaction: discord.Interaction,
        channel: GuildChannel,
        reason: str = None,
    ):
        guild_data = DataManager.get_guild_data(interaction.guild.id)
        logs_channel = self.bot.get_channel(guild_data["logs_channel_id"])
        channeltype = discord.ChannelType

        await channel.delete(reason=reason)

        ChannelDelete = discord.Embed(
            description=f"<:white_checkmark:1096793014287995061> Deleted {channeltype} channel {channel} ",
            colour=discord.Colour.green(),
        )

        if not (reason) == None:
            ChannelDelete.add_field(name="Reason", value=f"```{reason}```", inline=True)

        if len(ChannelDelete.fields) == 0:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    description=f"<:white_checkmark:1096793014287995061> Deleted `{channel}` channel with no reason provided",
                    colour=discord.Colour.green(),
                )
            )

        await interaction.response.send_message(embed=ChannelDelete)

    @delete_channel.error
    async def on_delete_channel_error(
        self, interaction: discord.Interaction, error: app_commands.AppCommandError
    ):
        if isinstance(error, app_commands.CommandOnCooldown):
            await interaction.response.send_message(
                ephemeral=True,
                embed=discord.Embed(
                    description=f"<:white_cross:1096791282023669860> Wait {error.retry_after:.1f} seconds before using this command again.",
                    colour=discord.Colour.red(),
                ),
            )

    @app_commands.command(
        name="add_role", description="Add a role to the mentioned user"
    )
    @app_commands.default_permissions(manage_roles=True)
    @app_commands.checks.cooldown(1, 7, key=lambda i: (i.guild.id, i.user.id))
    async def add_role(
        self,
        interaction: discord.Interaction,
        user: discord.Member,
        role: discord.Role,
    ):
        if role in user.roles:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    description="<:white_cross:1096791282023669860> That user already has that role",
                    colour=discord.Colour.red(),
                )
            )

        bot = interaction.guild.get_member(self.bot.user.id)
        if bot.top_role < role or bot.top_role == role:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    description="<:white_cross:1096791282023669860> I cannot add a role higher than my highest role",
                    colour=discord.Colour.red(),
                )
            )

        if interaction.user.top_role < role:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    description="<:white_cross:1096791282023669860> You cannot add a role higher than your highest role",
                    colour=discord.Colour.red(),
                )
            )

        await interaction.response.send_message(
            embed=discord.Embed(
                description=f"<:white_checkmark:1096793014287995061> added {role.mention} to {user.mention}",
                colour=discord.Colour.green(),
            )
        )
        await user.add_roles(role)

    @add_role.error
    async def on_add_role_error(
        self, interaction: discord.Interaction, error: app_commands.AppCommandError
    ):
        if isinstance(error, app_commands.CommandOnCooldown):
            await interaction.response.send_message(
                ephemeral=True,
                embed=discord.Embed(
                    description=f"<:white_cross:1096791282023669860> Wait {error.retry_after:.1f} seconds before using this command again.",
                    colour=discord.Colour.red(),
                ),
            )

    @app_commands.command(
        name="remove_role", description="Remove a role from the mentioned user"
    )
    @app_commands.default_permissions(manage_roles=True)
    @app_commands.checks.cooldown(1, 7, key=lambda i: (i.guild.id, i.user.id))
    async def remove_role(
        self,
        interaction: discord.Interaction,
        user: discord.Member,
        role: discord.Role,
    ):
        if role not in user.roles:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    description="<:white_cross:1096791282023669860> That user does not have that role.",
                    colour=discord.Colour.red(),
                )
            )

        bot = interaction.guild.get_member(self.bot.user.id)
        if bot.top_role < role or bot.top_role == role:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    description="<:white_cross:1096791282023669860> I cannot remove a role that is higher than my highest role.",
                    colour=discord.Colour.red(),
                )
            )

        if interaction.user.top_role < role:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    description="<:white_cross:1096791282023669860> You cannot remove a role that is higher than your highest role.",
                    colour=discord.Colour.red(),
                )
            )

        await interaction.response.send_message(
            embed=discord.Embed(
                description=f"<:white_checkmark:1096793014287995061> removed {role.mention} from {user.mention}",
                colour=discord.Colour.green(),
            )
        )
        await user.remove_roles(role)

    @remove_role.error
    async def on_remove_role_error(
        self, interaction: discord.Interaction, error: app_commands.AppCommandError
    ):
        if isinstance(error, app_commands.CommandOnCooldown):
            await interaction.response.send_message(
                ephemeral=True,
                embed=discord.Embed(
                    description=f"<:white_cross:1096791282023669860> Wait {error.retry_after:.1f} seconds before using this command again.",
                    colour=discord.Colour.red(),
                ),
            )

    @app_commands.command(
        name="purge", description="Purge a custom amount of messages from this channel"
    )
    @app_commands.default_permissions(manage_channels=True)
    @app_commands.checks.cooldown(1, 10, key=lambda i: (i.guild.id, i.user.id))
    async def purge(self, interaction: discord.Interaction, count: int):
        await interaction.response.defer(ephemeral=True)
        await interaction.channel.purge(limit=count)

        await asyncio.sleep(3)

        return await interaction.edit_original_response(
            embed=discord.Embed(
                description=f"<:white_checkmark:1096793014287995061> Purged {count} messages!",
                colour=discord.Colour.green(),
            )
        )

    @purge.error
    async def on_purge_error(
        self, interaction: discord.Interaction, error: app_commands.AppCommandError
    ):
        if isinstance(error, app_commands.CommandOnCooldown):
            await interaction.response.send_message(
                ephemeral=True,
                embed=discord.Embed(
                    description=f"<:white_cross:1096791282023669860> Wait {error.retry_after:.1f} seconds before using this command again.",
                    colour=discord.Colour.red(),
                ),
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
                    description=f'<:white_cross:1096791282023669860> Could not add "{word.lower()}" to blacklisted words list, because it already exists there',
                    colour=discord.Colour.orange(),
                ),
            )

        await interaction.response.send_message(
            ephemeral=True,
            embed=discord.Embed(
                description=f'<:white_checkmark:1096793014287995061> Added "{word.lower()}" to blacklisted words list',
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
                    description=f'<:white_cross:1096791282023669860> Could not remove "{word.lower()}" from blacklisted words list, because it does not exist there',
                    colour=discord.Colour.orange(),
                ),
            )

        await interaction.response.send_message(
            ephemeral=True,
            embed=discord.Embed(
                title="Removed Word From Blacklist",
                description=f'<:white_checkmark:1096793014287995061> Removed "{word.lower()}" from blacklisted words list',
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
                    description=f"<:white_cross:1096791282023669860> Could not add {whitelist.mention} to the whitelist because they already are in the whitelist",
                    colour=discord.Colour.orange(),
                ),
            )

        await interaction.response.send_message(
            ephemeral=True,
            embed=discord.Embed(
                title="Added Person To Whitelist",
                description=f"<:white_checkmark:1096793014287995061> Added {whitelist.mention} to whitelist",
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
                description=f"<:white_checkmark:1096793014287995061> You have been whitelisted in {interaction.guild.name} by {interaction.user.mention}",
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
                    description=f"<:white_cross:1096791282023669860> Could not remove {whitelist.mention} from the whitelist because they are not in it",
                    colour=discord.Colour.orange(),
                ),
            )

        await interaction.response.send_message(
            ephemeral=True,
            embed=discord.Embed(
                description=f"<:white_checkmark:1096793014287995061> Removed {whitelist.mention} from whitelist",
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
                description=f"<:white_cross:1096791282023669860> You have been removed from the whitelist in {interaction.guild.name} by {interaction.user.mention}",
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
                description=f"<:white_checkmark:1096793014287995061> Set the welcome message to: \n {message}",
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
                description=f"<:white_checkmark:1096793014287995061> Disabled welcome message",
                colour=discord.Colour.green(),
            )
        )


async def setup(bot):
    await bot.add_cog(ServerManagement(bot))
