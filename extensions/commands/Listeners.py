from datetime import datetime

import discord
from discord.ext import commands

from utils import DataManager


class Listeners(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # Blacklisted Word Listener
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        guild_data = DataManager.get_guild_data(message.guild.id)
        logs_channel = self.bot.get_channel(guild_data["logs_channel_id"])
        words_in_blacklist = guild_data["blacklisted_words"]

        if isinstance(message.channel.type, discord.DMChannel):
            return

        if message.author.bot:
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
        embed.add_field(name="Content", value=f"{message.content}", inline=True)
        embed.set_author(icon_url=message.author.avatar.url, name=f"{message.author}")
        embed.set_footer(
            text=f"Author ID: {message.author.id} | Message ID: {message.id}"
        )
        embed.timestamp = datetime.now()
        await logs_channel.send(embed=embed)

    # Message Edit Logs
    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        guild_data = DataManager.get_guild_data(before.guild.id)
        logs_channel = self.bot.get_channel(guild_data["logs_channel_id"])

        if logs_channel == None:
            return

        if before.author.bot:
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


async def setup(bot: commands.Bot):
    await bot.add_cog(Listeners(bot))
