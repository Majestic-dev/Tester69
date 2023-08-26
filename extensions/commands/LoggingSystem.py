import os
import datetime

import discord
from discord import app_commands
from discord.ext import commands

from utils import DataManager


class Logging(commands.GroupCog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="set_channel", description="Set where all server logs will be sent"
    )
    @app_commands.describe(
        channel="Choose the channel where all server logs will be sent"
    )
    @app_commands.default_permissions(administrator=True)
    async def set_logs_channel(
        self, interaction: discord.Interaction, channel: discord.TextChannel
    ):
        await interaction.response.send_message(
            embed=discord.Embed(
                description=f"<:white_checkmark:1096793014287995061> Set the logging channel to {channel.mention}",
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
                    description="<:white_cross:1096791282023669860> Logging is already disabled",
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

    # Member Join Listener
    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild_data = DataManager.get_guild_data(member.guild.id)
        logs_channel = self.bot.get_channel(guild_data["logs_channel_id"])

        if member.guild.get_member(member.id) == None:
            return

        if logs_channel == None:
            return

        join = discord.Embed(
            title="Member Joined",
            description=f"{member.mention} has joined the server",
            colour=discord.Colour.green(),
        )
        join.add_field(
            name="Account Created",
            value=discord.utils.format_dt(member.created_at, style="F"),
        )
        join.set_author(icon_url=member.display_avatar, name=member)
        join.set_footer(text=f"ID: {member.id}")
        join.timestamp = datetime.now()
        await logs_channel.send(embed=join)

    # Member Leave Listener
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        guild_data = DataManager.get_guild_data(member.guild.id)
        logs_channel = self.bot.get_channel(guild_data["logs_channel_id"])

        if logs_channel == None:
            return

        try:
            await member.guild.fetch_ban(member)
            return

        except:
            leave = discord.Embed(
                title="Member Left",
                description=f"{member.mention} Has left the server",
                colour=discord.Colour.red(),
            )
            leave.set_author(icon_url=member.display_avatar, name=member)
            leave.set_footer(text=f"ID: {member.id}")
            leave.timestamp = datetime.now()
            await logs_channel.send(embed=leave)

    # Warning Listener
    @commands.Cog.listener()
    async def on_warning(
        self,
        guild: discord.Guild,
        warned: discord.Member,
        warner: discord.Member,
        reason: str,
    ):
        guild_data = DataManager.get_guild_data(guild.id)
        logs_channel = self.bot.get_channel(guild_data["logs_channel_id"])

        if logs_channel == None:
            return

        warning = discord.Embed(
            title="Member Warned",
            description=f"{warned.mention} Has been warned by {warner.mention}",
            colour=discord.Colour.red(),
        )
        warning.add_field(name="Reason", value=f"```{reason}```")
        warning.set_author(icon_url=warned.display_avatar, name=warned)
        warning.set_footer(text=f"ID: {warned.id}")
        warning.timestamp = datetime.now()
        await logs_channel.send(embed=warning)

    # Member Timeout Listener
    @commands.Cog.listener()
    async def on_timeout(
        self,
        guild: discord.Guild,
        timeouter: discord.Member,
        timeouted: discord.Member,
        timedout_until: int,
        reason: str,
    ):
        guild_data = DataManager.get_guild_data(guild.id)
        logs_channel = self.bot.get_channel(guild_data["logs_channel_id"])

        if logs_channel == None:
            return

        timeout = discord.Embed(
            title="Member Timed Out",
            description=f"{timeouted.mention} Has been timed out by {timeouter.mention}",
            colour=discord.Colour.red(),
        )
        timeout.add_field(name="Reason", value=f"```{reason}```")
        timeout.add_field(
            name="Timed Out Until",
            value=discord.utils.format_dt(datetime.datetime.now() + datetime.timedelta(seconds=timedout_until), "F"),
        )
        timeout.set_author(icon_url=timeouted.display_avatar, name=timeouted)
        timeout.set_footer(text=f"ID: {timeouted.id}")
        await logs_channel.send(embed=timeout)

    # Member Mute Listener
    @commands.Cog.listener()
    async def on_mute(
        self,
        guild: discord.Guild,
        muted: discord.Member,
        muter: discord.Member,
        reason: str,
    ):
        guild_data = DataManager.get_guild_data(guild.id)
        logs_channel = self.bot.get_channel(guild_data["logs_channel_id"])

        if logs_channel == None:
            return

        mute = discord.Embed(
            title="Member Muted",
            description=f"{muted.mention} Has been muted by {muter.mention}",
            colour=discord.Colour.red(),
        )
        mute.add_field(name="Reason", value=f"```{reason}```")
        mute.set_author(icon_url=muted.display_avatar, name=muted)
        mute.set_footer(text=f"ID: {muted.id}")
        mute.timestamp = datetime.now()
        await logs_channel.send(embed=mute)

    # Member Unmute Listener
    @commands.Cog.listener()
    async def on_unmute(
        self,
        guild: discord.Guild,
        unmuted: discord.Member,
        unmuter: discord.Member,
        reason: str,
    ):
        guild_data = DataManager.get_guild_data(guild.id)
        logs_channel = self.bot.get_channel(guild_data["logs_channel_id"])

        if logs_channel == None:
            return

        unmute = discord.Embed(
            title="Member Unmuted",
            description=f"{unmuted.mention} Has been unmuted by {unmuter.mention}",
            colour=discord.Colour.green(),
        )
        unmute.add_field(name="Reason", value=f"```{reason}```")
        unmute.set_author(icon_url=unmuted.display_avatar, name=unmuted)
        unmute.set_footer(text=f"ID: {unmuted.id}")
        unmute.timestamp = datetime.now()
        await logs_channel.send(embed=unmute)

    # Member Kick Listener
    @commands.Cog.listener()
    async def on_kick(
        self, kicker: discord.User, guild: discord.Guild, user: discord.User
    ):
        guild_data = DataManager.get_guild_data(guild.id)
        logs_channel = self.bot.get_channel(guild_data["logs_channel_id"])

        if logs_channel == None:
            return

        kick = discord.Embed(
            title="Member Kicked",
            description=f"{user.mention} Has been kicked from the server",
            colour=discord.Colour.red(),
        )
        kick.set_author(icon_url=user.display_avatar, name=user)
        kick.set_footer(text=f"ID: {user.id}")
        kick.timestamp = datetime.now()
        await logs_channel.send(embed=kick)

    # Member Ban Listener
    @commands.Cog.listener()
    async def on_ban(
        self,
        guild: discord.Guild,
        banner: discord.User,
        banned: discord.User,
        reason: str,
    ):
        guild_data = DataManager.get_guild_data(guild.id)
        logs_channel = self.bot.get_channel(guild_data["logs_channel_id"])

        if logs_channel == None:
            return

        ban = discord.Embed(
            title="Member Banned",
            description=f"{banned.mention} Has been banned by {banner} from the server\nReason: {reason}",
            colour=discord.Colour.red(),
        )
        ban.set_author(icon_url=banned.display_avatar, name=banned)
        ban.set_footer(text=f"ID: {banned.id}")
        ban.timestamp = datetime.now()
        await logs_channel.send(embed=ban)

    # Member Unban Listener
    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        guild_data = DataManager.get_guild_data(guild.id)
        logs_channel = self.bot.get_channel(guild_data["logs_channel_id"])

        if logs_channel == None:
            return

        unban = discord.Embed(
            title="Member Unbanned",
            description=f"{user.mention} Has been unbanned from the server",
            colour=discord.Colour.green(),
        )
        unban.set_author(icon_url=user.display_avatar, name=user)
        unban.set_footer(text=f"ID: {user.id}")
        unban.timestamp = datetime.now()
        await logs_channel.send(embed=unban)

    # Member Update Listener
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        guild_data = DataManager.get_guild_data(before.guild.id)
        logs_channel = self.bot.get_channel(guild_data["logs_channel_id"])

        if logs_channel == None:
            return

        update = discord.Embed(
            description=f"{after.mention} has been updated",
            colour=discord.Colour.gold(),
        )

        nick = before.nick
        if nick == None:
            nick = before.name
        nick2 = after.nick
        if nick2 == None:
            nick2 = after.name

        if before.roles != after.roles:
            update.add_field(
                name="Member Roles Updated",
                value=f"**Before: `{', '.join([role.name for role in before.roles])}`\nAfter: `{', '.join([role.name for role in after.roles])}`**",
            )
        if before.nick != after.nick:
            update.add_field(
                name="Member Nickname Updated",
                value=f"**Before: {nick} \nAfter: {nick2}**",
            )
        if before.name != after.name:
            update.add_field(
                name="Member Username Updated",
                value=f"**Before: {before.name} \nAfter: {after.name}**",
            )
        if len(update.fields) <= 0:
            return
        update.set_author(icon_url=after.display_avatar, name=after)
        update.set_footer(text=f"ID: {before.id}")
        update.timestamp = datetime.now()
        return await logs_channel.send(embed=update)

    # Role Create Listener
    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        guild_data = DataManager.get_guild_data(role.guild.id)
        logs_channel = self.bot.get_channel(guild_data["logs_channel_id"])

        if logs_channel == None:
            return

        create = discord.Embed(
            title="Role Created",
            description=f"{role.mention} Role has been created",
            colour=discord.Colour.green(),
        )
        create.set_author(icon_url=role.guild.icon, name=role.guild)
        create.set_footer(text=f"Role ID: {role.id}")
        create.timestamp = datetime.now()
        await logs_channel.send(embed=create)

    # Role Delete Listener
    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        guild_data = DataManager.get_guild_data(role.guild.id)
        logs_channel = self.bot.get_channel(guild_data["logs_channel_id"])

        if logs_channel == None:
            return

        delete = discord.Embed(
            title="Role Deleted",
            description=f"{role.name} Role has been deleted",
            colour=discord.Colour.red(),
        )
        delete.set_author(icon_url=role.guild.icon, name=role.guild)
        delete.set_footer(text=f"Role ID: {role.id}")
        delete.timestamp = datetime.now()
        await logs_channel.send(embed=delete)

    # Role Update Listener
    @commands.Cog.listener()
    async def on_guild_role_update(self, before, after):
        guild_data = DataManager.get_guild_data(before.guild.id)
        logs_channel = self.bot.get_channel(guild_data["logs_channel_id"])

        if logs_channel == None:
            return

        update = discord.Embed(
            description=f"{after.mention} Role has been updated",
            colour=discord.Colour.gold(),
        )

        if before.name != after.name:
            update.add_field(
                name=f"Role Name",
                value=f"**Before: {before.name} \nAfter: {after.name}**",
            )
        if before.colour != after.colour:
            update.add_field(
                name=f"Role Colour RGB Value",
                value=f"**Before: {before.colour} \nAfter: {after.colour}**",
            )
        if before.hoist != after.hoist:
            update.add_field(
                name=f"Role Displayed Separately From Others",
                value=f"**Before: {before.hoist} \nAfter: {after.hoist}**",
            )
        if before.mentionable != after.mentionable:
            update.add_field(
                name=f"Role Mentionable By Anyone",
                value=f"**Before: {before.mentionable} \nAfter: {after.mentionable}**",
            )
        if before.display_icon != after.display_icon:
            update.add_field(
                name=f"Role Display Icon",
                value=f"**Before: {before.display_icon} \nAfter: {after.display_icon}**",
            )
        if len(update.fields) <= 0:
            return
        update.set_author(icon_url=before.guild.icon, name=before.guild)
        update.set_footer(text=f"Role ID: {before.id}")
        update.timestamp = datetime.now()
        return await logs_channel.send(embed=update)

    # Voice Channel Listener
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        guild_data = DataManager.get_guild_data(member.guild.id)
        logs_channel = self.bot.get_channel(guild_data["logs_channel_id"])

        if logs_channel == None:
            return

        voice = discord.Embed(
            description=f"{member.mention} Voice channel updated",
            colour=discord.Colour.gold(),
        )

        if before.channel == None and after.channel != None:
            voice.add_field(
                name="Voice Channel Joined",
                value=f"**{member.mention} Joined {after.channel.mention} voice channel**",
            )
        if before.channel != None and after.channel == None:
            voice.add_field(
                name="Voice Channel Left",
                value=f"**{member.mention} Left {before.channel.mention} voice channel**",
            )
        if (
            before.channel != None
            and before.channel != after.channel
            and after.channel != None
        ):
            voice.add_field(
                name="Voice Channel Moved",
                value=f"**{member.mention} Swithced voice channels {before.channel.mention} -> {after.channel.mention}**",
            )
        if before.mute == False and after.mute == True:
            voice.add_field(
                name="Voice Muted By Admin",
                value=f"**{member.mention} Was muted by an admin**",
            )
        if before.mute == True and after.mute == False:
            voice.add_field(
                name="Voice Unmuted By Admin",
                value=f"**{member.mention} Was unmuted by an admin**",
            )
        if before.deaf == False and after.deaf == True:
            voice.add_field(
                name="Voice Deafened By Admin",
                value=f"**{member.mention} Was deafened by an admin**",
            )
        if before.deaf == True and after.deaf == False:
            voice.add_field(
                name="Voice Undeafened By Admin",
                value=f"**{member.mention} Was undeafened by an admin**",
            )
        if len(voice.fields) <= 0:
            return
        voice.set_author(icon_url=member.display_avatar, name=member)
        voice.set_footer(text=f"ID: {member.id}")
        voice.timestamp = datetime.now()
        return await logs_channel.send(embed=voice)

    # Blacklisted Word Listener
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        if message.channel.type == discord.channel.ChannelType.private:
            return

        guild_data = DataManager.get_guild_data(message.guild.id)
        words_in_blacklist = guild_data["blacklisted_words"]
        content = message.content.lower()

        if message.author.id in guild_data["whitelist"] or any(
            role.id in guild_data["whitelist"] for role in message.author.roles
        ):
            return

        if any(word in words_in_blacklist for word in content.split(" ")):
            await message.delete()

    # Message Edit Logs
    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        if before.channel.type == discord.channel.ChannelType.private:
            return

        guild_data = DataManager.get_guild_data(before.guild.id)
        logs_channel = self.bot.get_channel(guild_data["logs_channel_id"])
        words_in_blacklist = guild_data["blacklisted_words"]
        content = after.content.lower()

        if before.author.bot and before.channel != logs_channel:
            return

        if before.is_system() == True:
            return

        if logs_channel == None:
            return

        if before.author.id in guild_data["whitelist"] or any(
            role.id in guild_data["whitelist"] for role in before.author.roles
        ):
            return

        if any(word in words_in_blacklist for word in content.split(" ")):
            return await after.delete()

        edit = discord.Embed(
            description=f"**Message Edited in {before.channel.mention}** [Jump to Message]({before.jump_url})",
            colour=discord.Colour.orange(),
        )

        if (
            before.flags.suppress_embeds is False
            and after.flags.suppress_embeds is True
        ):
            embeds = before.embeds[0]
            return await logs_channel.send(embed=embeds)

        if len(before.content or after.content) >= 1024:
            with open(f"{after.author.id}_edit.txt", "a") as n:
                n.write(f"Before: {before.content}\nAfter: {after.content}")
            embed = discord.Embed(
                title="Message Edit (Too Long)",
                description=f"**Message Edited in {before.channel.mention}** [Jump to Message]({before.jump_url})",
                colour=discord.Colour.orange(),
            )
            embed.set_author(icon_url=after.author.avatar, name=after.author)
            await logs_channel.send(
                embed=embed, file=discord.File(f"{after.author.id}_edit.txt")
            )
            return os.remove(f"{after.author.id}_edit.txt")

        if before.content != after.content:
            edit.add_field(
                name="**Before**",
                value=f"{before.content}",
                inline=True,
            )

            edit.add_field(
                name="**After**",
                value=f"{after.content}",
                inline=True,
            )

        if len(after.attachments) >= 1:
            edit.add_field(
                name="Attachments",
                value=f"**{', '.join([attachment.url for attachment in after.attachments])}**",
                inline=False,
            )

        if len(after.stickers) >= 1:
            edit.add_field(
                name="Stickers",
                value=f"**{', '.join([sticker.url for sticker in after.stickers])}**",
                inline=False,
            )

        if before.pinned != after.pinned:
            edit.add_field(
                name="Pinned",
                value=f"**Before:** {before.pinned}\n**After:** {after.pinned}",
                inline=True,
            )
        if len(edit.fields) <= 0:
            return

        edit.set_author(icon_url=after.author.avatar, name=f"{before.author}")
        edit.set_footer(text=f"Author ID: {before.author.id}")
        edit.timestamp = datetime.now()
        await logs_channel.send(embed=edit)

    # Delete Logs
    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        if (
            message.author.bot
            and message.embeds == False
            or message.is_system() == True
            or message.channel.type == discord.channel.ChannelType.private
        ):
            return

        guild_data = DataManager.get_guild_data(message.guild.id)
        logs_channel = self.bot.get_channel(guild_data["logs_channel_id"])

        if message.author.bot and message.channel != logs_channel:
            return

        if logs_channel == None:
            return

        words_in_blacklist = guild_data["blacklisted_words"]
        content = message.content.lower()
        content2 = message.content.split(" ")
        bad_words_said = "\n".join(list(set(content2) & set(words_in_blacklist)))

        if (
            message.author.bot == True
            and message.embeds
            and message.channel == logs_channel
        ):
            embed = message.embeds[0]
            return await logs_channel.send(content=f"{message.content}", embed=embed)

        if message.embeds:
            embed = message.embeds[0]
            return await logs_channel.send(
                content=f"Embed sent by {message.author} deleted in {message.channel.mention}",
                embed=embed,
            )

        embed = discord.Embed(
            description=f"**Message sent by {message.author.mention} Deleted in {message.channel.mention}**",
            colour=discord.Colour.orange(),
        )
        if len(message.content) >= 1024:
            with open(f"{message.author.id}_delete.txt", "a") as n:
                n.write(message.content)

            embed = discord.Embed(
                title="Message Deleted (Too Long)",
                description=f"**Message sent by {message.author.mention} Deleted in {message.channel.mention}**",
                colour=discord.Colour.orange(),
            )
            embed.set_author(
                icon_url=message.author.display_avatar, name=message.author
            )
            await logs_channel.send(
                embed=embed, file=discord.File(f"{message.author.id}_delete.txt")
            )
            return os.remove(f"{message.author.id}_delete.txt")

        if len(message.content) > 0:
            embed.add_field(name="**Content**", value=f"{message.content}")
        if any(word in words_in_blacklist for word in content.split(" ")):
            embed.add_field(name="**Reason**", value="Blacklisted Word")
            embed.add_field(name="**Detailed Reason**", value=f"`{bad_words_said}`")
        if len(message.attachments) > 1:
            embed.add_field(
                name="Attachments",
                value=f"**{', '.join([attachment.url for attachment in message.attachments])}**",
                inline=False,
            )
        elif len(message.attachments) == 1:
            embed.set_image(url=message.attachments[0].url)
        if len(message.stickers) >= 1:
            embed.add_field(
                name="Stickers",
                value=f"**{', '.join([sticker.url for sticker in message.stickers])}**",
                inline=False,
            )
        embed.set_author(
            icon_url=message.author.display_avatar, name=f"{message.author}"
        )
        embed.set_footer(
            text=f"Author ID: {message.author.id} | Message ID: {message.id}"
        )
        embed.timestamp = datetime.now()
        await logs_channel.send(embed=embed)

    # Channel Create Listener
    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        guild_data = DataManager.get_guild_data(channel.guild.id)
        logs_channel = self.bot.get_channel(guild_data["logs_channel_id"])

        if logs_channel == None:
            return

        embed = discord.Embed(
            title="Channel Created",
            description=f"Created {channel.mention} channel",
            timestamp=datetime.utcnow(),
            colour=discord.Colour.green(),
        )

        embed.set_author(name=channel.guild.name, icon_url=channel.guild.icon)
        embed.set_footer(text=f"Channel ID: {channel.id}")

        await logs_channel.send(embed=embed)

    # Channel Delete Listener
    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        guild_data = DataManager.get_guild_data(channel.guild.id)
        logs_channel = self.bot.get_channel(guild_data["logs_channel_id"])

        if logs_channel == None:
            return

        embed = discord.Embed(
            title="Channel Deleted",
            description=f"Deleted channel {channel.name}",
            timestamp=datetime.utcnow(),
            colour=discord.Colour.red(),
        )

        embed.set_author(name=channel.guild.name, icon_url=channel.guild.icon)

        await logs_channel.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Logging(bot))
