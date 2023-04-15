from datetime import datetime

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
        
    #Member Join Listener
    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild_data = DataManager.get_guild_data(member.guild.id)
        logs_channel = self.bot.get_channel(guild_data["logs_channel_id"])

        if logs_channel == None:
            return
        
        join = discord.Embed(
            title="Member Joined",
            description=f"{member.mention} has joined the server",
            colour=discord.Colour.green(),
        )
        join.add_field(name="Account Created", value=discord.utils.format_dt(member.created_at, style="F"))
        join.set_author(icon_url=member.avatar, name=member)
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
        
        leave = discord.Embed(
            title="Member Left",
            description=f"{member.mention} has left the server",
            colour=discord.Colour.red(),
        )
        leave.set_author(icon_url=member.avatar, name=member)
        leave.set_footer(text=f"ID: {member.id}")
        leave.timestamp = datetime.now()
        await logs_channel.send(embed=leave)

    # Member Ban Listener
    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        guild_data = DataManager.get_guild_data(guild.id)
        logs_channel = self.bot.get_channel(guild_data["logs_channel_id"])
        
        if logs_channel == None:
            return
        
        ban = discord.Embed(
            title="Member Banned",
            description=f"{user.mention} has been banned from the server",
            colour=discord.Colour.red(),
        )
        ban.set_author(icon_url=user.avatar, name=user)
        ban.set_footer(text=f"ID: {user.id}")
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
            description=f"{user.mention} has been unbanned from the server",
            colour=discord.Colour.green(),
        )
        unban.set_author(icon_url=user.avatar, name=user)
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
            title="Member Updated",
            description=f"{before.mention}'s profile has been updated",
            colour=discord.Colour.gold(),
        )

        nick = before.nick
        if nick == None:
            nick = before.name
        nick2 = after.nick
        if nick2 == None:
            nick2 = after.name
        
        if before.roles != after.roles:
            update.add_field(name="Roles", value=f"Before: {', '.join([role.name for role in before.roles])}\nAfter: {', '.join([role.name for role in after.roles])}")
        if before.nick != after.nick:
            update.add_field(name="Nickname", value=f"Before: {nick} \nAfter: {nick2}")
        if before.name != after.name:
            update.add_field(name="Username", value=f"Before: {before.name} \nAfter: {after.name}")
        if len(update.fields) <= 0:
            return
        update.set_author(icon_url=before.avatar, name=before)
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
            description=f"{role.mention} has been created",
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
            description=f"{role.name} has been deleted",
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
            title="Role Updated",
            description=f"{before.mention} has been updated",
            colour=discord.Colour.gold(),
        )

        if before.name != after.name:
            update.add_field(name="Name", value=f"Before: {before.name} \nAfter: {after.name}")
        if before.colour != after.colour:
            update.add_field(name="Colour RGB Value", value=f"Before: {before.colour} \nAfter: {after.colour}")
        if before.hoist != after.hoist:
            update.add_field(name="Displayed Separately From Others", value=f"Before: {before.hoist} \nAfter: {after.hoist}")
        if before.mentionable != after.mentionable:
            update.add_field(name="Mentionable By Anyone", value=f"Before: {before.mentionable} \nAfter: {after.mentionable}")
        if before.display_icon != after.display_icon:
            update.add_field(name="Display Icon", value=f"Before: {before.display_icon} \nAfter: {after.display_icon}")
        if before.position != after.position:
            update.add_field(name="Position", value=f"Before: {before.position} \nAfter: {after.position}") 
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
            title="Voice Channel Update",
            description=f"{member.mention} has updated their voice channel",
            colour=discord.Colour.gold(),
        )

        if before.channel != after.channel:
            voice.add_field(name="Voice Channel", value=f"Before: {before.channel} \nAfter: {after.channel}")
        if before.mute != after.mute:
            voice.add_field(name="Muted By Admin", value=f"Before: {before.mute} \nAfter: {after.mute}")
        if before.deaf != after.deaf:
            voice.add_field(name="Deafened By Admin", value=f"Before: {before.deaf} \nAfter: {after.deaf}")
        if len(voice.fields) <= 0:
            return
        voice.set_author(icon_url=member.avatar, name=member)
        voice.set_footer(text=f"ID: {member.id}")
        voice.timestamp = datetime.now()
        return await logs_channel.send(embed=voice)
        
    # Blacklisted Word Listener
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):

        if message.author.bot:
            return
        
        if isinstance(message.channel.type, discord.DMChannel):
            return
        
        guild_data = DataManager.get_guild_data(message.guild.id)
        logs_channel = self.bot.get_channel(guild_data["logs_channel_id"])
        words_in_blacklist = guild_data["blacklisted_words"]

        if logs_channel == None:
            return

        if message.author.id in guild_data["whitelist"] or any(
            role.id in guild_data["whitelist"] for role in message.author.roles
        ):
            return

        content = message.content.lower()

        if any(word in words_in_blacklist for word in message.content.split(" ")):
            await message.delete()
            return await logs_channel.send(
                embed=discord.Embed(
                    title="Blacklisted Word",
                    description=f"{message.author.mention} sent a blacklisted word",
                    timestamp=datetime.utcnow(),
                    colour=discord.Colour.red(),
                )
            )
        
    # Message Edit Logs
    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        guild_data = DataManager.get_guild_data(before.guild.id)
        logs_channel = self.bot.get_channel(guild_data["logs_channel_id"])

        if logs_channel == None:
            return

        if before.author.bot:
            return
        
        if before.attachments:
            return

        delete = discord.Embed(
            description=f"**Message Edited in {before.channel.mention}** [Jump to Message]({before.jump_url})",
            colour=discord.Colour.orange(),
        )
        delete.add_field(name="Before", value=f"{before.content}", inline=True)
        delete.add_field(name="After", value=f"{after.content}", inline=True)
        delete.set_author(icon_url=before.author.avatar.url, name=f"{before.author}")
        delete.set_footer(text=f"Author ID: {before.author.id}")
        delete.timestamp = datetime.now()
        await logs_channel.send(embed=delete)

    # Delete Logs
    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        guild_data = DataManager.get_guild_data(message.guild.id)
        logs_channel = self.bot.get_channel(guild_data["logs_channel_id"])

        if logs_channel == None:
            return

        if message.author.bot:
            return

        embed = discord.Embed(
            description=f"**Message sent by {message.author.mention} Deleted in {message.channel.mention}**",
            colour=discord.Colour.orange(),
        ) 
        if len(message.attachments) > 1:
            embed.add_field(
                name="Attachments",
                value=f"{', '.join([attachment.url for attachment in message.attachments])}",
                inline=False,
            )
        elif len(message.attachments) == 1:
            embed.set_image(url=message.attachments[0].url)
        if len(message.content) > 0:
            embed.add_field(name="Content", value=f"{message.content}", inline=True)
        embed.set_author(icon_url=message.author.avatar.url, name=f"{message.author}")
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

        await logs_channel.send(
            embed=discord.Embed(
                title="Channel Created",
                description=f"Created {channel.mention} channel",
                timestamp=datetime.utcnow(),
                colour=discord.Colour.green(),
            )
        )

    # Channel Delete Listener
    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        guild_data = DataManager.get_guild_data(channel.guild.id)
        logs_channel = self.bot.get_channel(guild_data["logs_channel_id"])

        await logs_channel.send(
            embed=discord.Embed(
                title="Channel Deleted",
                description=f'Deleted {channel} channel',
                timestamp=datetime.utcnow(),
                colour=discord.Colour.red(),
            )
        )

async def setup(bot):
    await bot.add_cog(Logging(bot))
