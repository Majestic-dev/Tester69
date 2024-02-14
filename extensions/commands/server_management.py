import asyncio
from typing import Optional

import discord
from discord import app_commands
from discord.abc import GuildChannel
from discord.enums import ChannelType
from discord.ext import commands

from utils import DataManager


class server_management(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="slowmode", description="Set the slowmode in the channel of your choice"
    )
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(manage_channels=True)
    @app_commands.checks.cooldown(1, 10, key=lambda i: (i.guild.id, i.user.id))
    @app_commands.describe(
        channel="The channel to set the slowmode in (defaults to the channel where the command was ran in)",
        slowmode="The slowmode in seconds to set in the channel (0 to disable)",
    )
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

    @app_commands.command(
        name="set_appeal_link",
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
        name="disable_appealing",
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

    @app_commands.command(
        name="create_channel",
        description="Create a channel with the name of your choice",
    )
    @app_commands.guild_only()
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
    @app_commands.checks.has_permissions(manage_channels=True)
    @app_commands.checks.cooldown(1, 20, key=lambda i: (i.guild.id, i.user.id))
    @app_commands.describe(
        channeltype="The type of channel to create",
        name="The name of the channel to create",
        category="The category to create the channel in (defaults no category)",
        slowmode="The slowmode in seconds to set in the channel (0 to disable)",
    )
    async def create_channel(
        self,
        interaction: discord.Interaction,
        channeltype: app_commands.Choice[int],
        name: str,
        category: Optional[discord.CategoryChannel],
        slowmode: Optional[int],
    ):
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

    @app_commands.command(
        name="delete_channel", description="Delete the mentioned channel"
    )
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(manage_channels=True)
    @app_commands.checks.cooldown(1, 10, key=lambda i: (i.guild.id, i.user.id))
    @app_commands.describe(
        channel="The channel to delete", reason="The reason for deleting the channel"
    )
    async def delete_channel(
        self,
        interaction: discord.Interaction,
        channel: GuildChannel,
        reason: str = None,
    ):
        await channel.delete(reason=reason)

        ChannelDelete = discord.Embed(
            description=f"<:white_checkmark:1096793014287995061> Deleted {channel.type} channel {channel} ",
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

    @app_commands.command(
        name="add_role", description="Add a role to the mentioned user"
    )
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(manage_roles=True)
    @app_commands.checks.cooldown(1, 7, key=lambda i: (i.guild.id, i.user.id))
    @app_commands.describe(
        user="The user to add the role to", role="The role to add to the user"
    )
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
        if bot.top_role <= role:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    description="<:white_cross:1096791282023669860> I cannot add a role higher than my highest role",
                    colour=discord.Colour.red(),
                )
            )

        if interaction.user.top_role <= role:
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

    @app_commands.command(
        name="remove_role", description="Remove a role from the mentioned user"
    )
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(manage_roles=True)
    @app_commands.checks.cooldown(1, 7, key=lambda i: (i.guild.id, i.user.id))
    @app_commands.describe(
        user="The user to remove the role from", role="The role to remove from the user"
    )
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
        if bot.top_role <= role:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    description="<:white_cross:1096791282023669860> I cannot remove a role that is higher than my highest role.",
                    colour=discord.Colour.red(),
                )
            )

        if interaction.user.top_role <= role:
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

    @app_commands.command(
        name="purge", description="Purge a custom amount of messages from this channel"
    )
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(manage_channels=True)
    @app_commands.checks.cooldown(1, 10, key=lambda i: (i.guild.id, i.user.id))
    @app_commands.describe(count="The amount of messages to purge")
    async def purge(self, interaction: discord.Interaction, count: int):
        guild_data = await DataManager.get_guild_data(interaction.guild.id)
        logs_channel = self.bot.get_channel(guild_data["logs_channel_id"])
        await interaction.response.defer(ephemeral=True)
        await interaction.channel.purge(limit=count)

        await asyncio.sleep(2)

        embed = discord.Embed(
            description=f"{interaction.user.mention} purged {count} messages in {interaction.channel.mention}",
            colour=discord.Colour.red(),
        )
        embed.set_author(url=interaction.user.display_avatar, name=interaction.user)
        embed.set_footer(text=f"User ID: {interaction.user.id}")
        await logs_channel.send(embed=embed)

        return await interaction.edit_original_response(
            embed=discord.Embed(
                description=f"<:white_checkmark:1096793014287995061> Purged {count} messages!",
                colour=discord.Colour.green(),
            )
        )

    @app_commands.command(
        name="add_blacklisted_words",
        description="Add words to the blacklisted words list",
    )
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.describe(
        blacklisted_words="The word(s) to add to the blacklisted words list, if adding multiple, separate them by commas (a, b)"
    )
    async def add_blacklisted_word(
        self, interaction: discord.Interaction, blacklisted_words: str
    ):
        await interaction.response.defer(ephemeral=True)
        filtered_words = await DataManager.get_guild_filtered_words(
            interaction.guild.id
        )
        old_existing_words = filtered_words["blacklisted_words"]
        new_existing_words = old_existing_words.copy()
        words_not_added = []

        for i in blacklisted_words.split(","):
            if i.strip() in old_existing_words:
                words_not_added.append(i.strip())
                pass
            elif i.strip() not in old_existing_words:
                new_existing_words.append(i.strip())

        await DataManager.edit_blacklisted_words(
            interaction.guild.id, new_existing_words
        )

        if len(words_not_added) >= 0 and (
            len(new_existing_words) > len(old_existing_words)
        ):
            return await interaction.edit_original_response(
                embed=discord.Embed(
                    description=(
                        f"<:white_checkmark:1096793014287995061> Added the following words to the blacklisted words list:\n\n"
                        f"`{', '.join(list(set(new_existing_words) - set(old_existing_words)))}`\n\n"
                    )
                    + (
                        f"Could not add the following words to the blacklisted words list because they already exist there:\n"
                        f"`{', '.join(words_not_added)}`"
                        if len(words_not_added) > 0
                        else ""
                    ),
                    colour=discord.Colour.green(),
                )
            )

        elif len(words_not_added) > 0 and (
            len(new_existing_words) == len(old_existing_words)
        ):
            return await interaction.edit_original_response(
                embed=discord.Embed(
                    description=f"<:white_cross:1096791282023669860> Could not add any of the words to the blacklisted words list because they already exist there!",
                    colour=discord.Colour.orange(),
                ),
            )

    async def word_autocomplete(
        self, interaction: discord.Interaction, current: str
    ) -> list[app_commands.Choice[str]]:
        filtered_words = await DataManager.get_guild_filtered_words(
            interaction.guild.id
        )
        words_in_blacklist = filtered_words["blacklisted_words"]

        return [
            app_commands.Choice(name=word, value=word)
            for word in words_in_blacklist
            if word.lower().startswith(current.lower())
            or len(current) < 1
        ]

    @app_commands.command(
        name="remove_blacklisted_word",
        description="Remove a blacklisted word from the blacklisted words list.",
    )
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.autocomplete(blacklisted_word=word_autocomplete)
    @app_commands.describe(
        blacklisted_word="The word to remove from the blacklisted words list"
    )
    async def remove_blacklisted_word(
        self, interaction: discord.Interaction, blacklisted_word: str
    ):
        filtered_words = await DataManager.get_guild_filtered_words(
            interaction.guild.id
        )
        blacklisted_words = filtered_words["blacklisted_words"]

        if (
            blacklisted_words is None
            or blacklisted_word.lower() not in blacklisted_words
        ):
            return await interaction.response.send_message(
                ephemeral=True,
                embed=discord.Embed(
                    description=f'<:white_cross:1096791282023669860> Could not remove "{blacklisted_word.lower()}" from blacklisted words list, because it does not exist there',
                    colour=discord.Colour.orange(),
                ),
            )

        elif blacklisted_word.lower() in blacklisted_words:
            blacklisted_words.remove(blacklisted_word.lower())
            await DataManager.edit_blacklisted_words(
                interaction.guild.id, blacklisted_words
            )
            return await interaction.response.send_message(
                ephemeral=True,
                embed=discord.Embed(
                    description=f'<:white_checkmark:1096793014287995061> Removed "{blacklisted_word.lower()}" from blacklisted words list',
                    colour=discord.Colour.green(),
                ),
            )

    @app_commands.command(
        name="whitelist_add", description="Add a user in the whitelist"
    )
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.describe(whitelist="The user or role to add to the whitelist")
    async def whitelist_add(
        self, interaction: discord.Interaction, whitelist: discord.User | discord.Role
    ):
        guild_filtered_words_data = await DataManager.get_guild_filtered_words(
            interaction.guild.id
        )
        wlist = guild_filtered_words_data["whitelist"]

        if wlist is None or whitelist.id not in wlist:
            wlist.append(whitelist.id)
            await DataManager.edit_whitelist(interaction.guild.id, wlist)
            await interaction.response.send_message(
                ephemeral=True,
                embed=discord.Embed(
                    description=f"<:white_checkmark:1096793014287995061> Added {whitelist.mention} to whitelist",
                    colour=discord.Colour.green(),
                ),
            )

        elif whitelist.id in wlist:
            return await interaction.response.send_message(
                ephemeral=True,
                embed=discord.Embed(
                    description=f"<:white_cross:1096791282023669860> Could not add {whitelist.mention} to the whitelist because they already are in the whitelist",
                    colour=discord.Colour.orange(),
                ),
            )

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
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.describe(whitelist="The user or role to remove from the whitelist")
    async def whitelist_remove(
        self, interaction: discord.Interaction, whitelist: discord.User | discord.Role
    ):
        filtered_words_data = await DataManager.get_guild_filtered_words(
            interaction.guild.id
        )
        wlist = filtered_words_data["whitelist"]

        if wlist is None or whitelist.id not in wlist:
            return await interaction.response.send_message(
                ephemeral=True,
                embed=discord.Embed(
                    description=f"<:white_cross:1096791282023669860> Could not remove {whitelist.mention} from the whitelist because they are not in it",
                    colour=discord.Colour.orange(),
                ),
            )

        elif whitelist.id in wlist:
            wlist.remove(whitelist.id)
            await DataManager.edit_whitelist(interaction.guild.id, wlist)
            await interaction.response.send_message(
                ephemeral=True,
                embed=discord.Embed(
                    description=f"<:white_checkmark:1096793014287995061> Removed {whitelist.mention} from whitelist",
                    colour=discord.Colour.green(),
                ),
            )

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
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.describe(message="The message to send to users DMs when they join")
    async def set_welcome_message(self, interaction: discord.Interaction, message: str):
        await interaction.response.send_message(
            embed=discord.Embed(
                description=f"<:white_checkmark:1096793014287995061> Set the welcome message to: \n ```{message}```",
                colour=discord.Colour.green(),
            )
        )

        await DataManager.edit_guild_data(
            interaction.guild.id, "welcome_message", message
        )

    @app_commands.command(
        name="disable_welcome_message",
        description="Disable the welcome message that is sent to users DMs when they join the server",
    )
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(administrator=True)
    async def disable_welcome_message(self, interaction: discord.Interaction):
        await DataManager.edit_guild_data(interaction.guild.id, "welcome_message", None)

        await interaction.response.send_message(
            embed=discord.Embed(
                description=f"<:white_checkmark:1096793014287995061> Disabled welcome message",
                colour=discord.Colour.green(),
            )
        )


async def setup(bot):
    await bot.add_cog(server_management(bot))
