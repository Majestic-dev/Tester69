from typing import Optional

import discord
from discord import app_commands
from discord.ext import commands


class Server(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="serverinfo", description="Get information about the server"
    )
    @app_commands.guild_only()
    @app_commands.checks.cooldown(1, 20, key=lambda i: (i.guild.id, i.user.id))
    async def serverinfo(self, interaction: discord.Interaction):
        guild = interaction.guild
        embed = discord.Embed(title=f"Server Info", colour=discord.Colour.random())

        embed.set_thumbnail(url=guild.icon)
        embed.set_author(name=guild.name, icon_url=guild.icon)
        embed.add_field(
            name="Owner",
            value=f"{guild.owner.name}#{guild.owner.discriminator}",
            inline=True,
        )
        embed.add_field(
            name="Category Channels", value=len(guild.categories), inline=True
        )
        embed.add_field(
            name="Text Channels", value=len(guild.text_channels), inline=True
        )
        embed.add_field(
            name="Voice Channels", value=len(guild.voice_channels), inline=True
        )
        embed.add_field(name="Members", value=guild.member_count, inline=True)
        embed.add_field(name="Roles", value=len(guild.roles), inline=True)
        embed.add_field(
            name="Role List",
            value=", ".join([role.name for role in guild.roles]),
            inline=False,
        )
        embed.set_footer(
            text=f"ID: {guild.id} | Created at {guild.created_at.strftime('%m/%d/%Y %H:%M')}"
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="userinfo", description="Get information about a user")
    @app_commands.guild_only()
    @app_commands.checks.cooldown(1, 20, key=lambda i: (i.guild.id, i.user.id))
    @app_commands.describe(user = "The user to get information about")
    async def userinfo(
        self,
        interaction: discord.Interaction,
        user: Optional[discord.User] = None,
    ):
        if user is None:
            user = interaction.user
        else:
            await self.bot.fetch_user(user.id)
        embed = discord.Embed(title=f"User Info", colour=discord.Colour.random())

        embed.set_thumbnail(url=user.avatar)
        embed.set_author(name=user.name, icon_url=user.avatar)
        embed.add_field(
            name="Name", value=f"{user.name}#{user.discriminator}", inline=True
        )
        embed.add_field(
            name="Account Created",
            value=discord.utils.format_dt(user.created_at, style="F"),
            inline=True,
        )
        if interaction.guild.get_member(user.id):
            embed.add_field(
                name="Joined Server",
                value=discord.utils.format_dt(user.joined_at, style="F"),
                inline=True,
            )
        embed.add_field(name="ID", value=user.id, inline=True)
        embed.add_field(name="Bot", value=user.bot, inline=True)
        embed.set_footer(
            text=f"ID: {user.id} | Created at {user.created_at.strftime('%m/%d/%Y %H:%M')}"
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="roleinfo", description="Get information about a role")
    @app_commands.guild_only()
    @app_commands.checks.cooldown(1, 20, key=lambda i: (i.guild.id, i.user.id))
    @app_commands.describe(role = "The role to get information about")
    async def roleinfo(
        self,
        interaction: discord.Interaction,
        role: Optional[discord.Role] = None,
    ):
        if role is None:
            role = interaction.guild.default_role
        embed = discord.Embed(colour=role.colour)

        embed.set_thumbnail(url=role.icon)
        embed.add_field(name="ID", value=role.id, inline=True)
        embed.add_field(name="Name", value=role.name, inline=True)
        embed.add_field(name="Color", value=role.colour, inline=True)
        embed.add_field(name="Mention", value=f"`<@&{role.id}>`", inline=True)
        embed.add_field(name="Hoisted", value=role.hoist, inline=True)
        embed.add_field(name="Position", value=role.position, inline=True)
        embed.add_field(name="Mentionable", value=role.mentionable, inline=True)
        embed.add_field(name="Members", value=len(role.members), inline=True)

        embed.set_footer(
            text=f"Role Created • {role.created_at.strftime('%m/%d/%Y %H:%M')}"
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(
        name="channelinfo", description="Get information about a channel"
    )
    @app_commands.guild_only()
    @app_commands.checks.cooldown(1, 20, key=lambda i: (i.guild.id, i.user.id))
    @app_commands.describe(channel = "The channel to get information about")
    async def channelinfo(
        self,
        interaction: discord.Interaction,
        channel: Optional[discord.TextChannel] = None,
    ):
        if channel is None:
            channel = interaction.channel
        embed = discord.Embed(colour=discord.Colour.random())

        embed.set_thumbnail(url=channel.guild.icon)
        embed.add_field(name="ID", value=channel.id, inline=True)
        embed.add_field(name="Name", value=channel.name, inline=True)
        embed.add_field(name="Type", value=channel.type, inline=True)
        embed.add_field(name="Mention", value=f"`<#{channel.id}>`", inline=True)
        embed.add_field(name="NSFW", value=channel.is_nsfw(), inline=True)
        embed.add_field(name="Position", value=channel, inline=True)
        embed.add_field(name="Slowmode", value=channel.slowmode_delay, inline=True)
        embed.add_field(name="Topic", value=channel.topic, inline=True)
        embed.add_field(name="Members", value=len(channel.members), inline=True)

        embed.set_footer(
            text=f"Channel Created • {channel.created_at.strftime('%m/%d/%Y %H:%M')}"
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(
        name="membercount", description="Get the member count of the server"
    )
    @app_commands.guild_only()
    @app_commands.checks.cooldown(1, 20, key=lambda i: (i.guild.id, i.user.id))
    async def membercount(self, interaction: discord.Interaction):
        guild = interaction.guild
        embed = discord.Embed(
            title=f"Member Count",
            description=f"Total Members: {guild.member_count}",
            colour=discord.Colour.random(),
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(
        name="avatar", description="Get the avatar of a user or yourself"
    )
    @app_commands.checks.cooldown(1, 20, key=lambda i: (i.guild.id, i.user.id))
    @app_commands.describe(user = "The user to get the avatar of, defaults to yourself")
    async def avatar(
        self,
        interaction: discord.Interaction,
        user: Optional[discord.User] = None,
    ):
        if user is None:
            user = interaction.user
        embed = discord.Embed(
            title=f"{user.name}'s Avatar", colour=discord.Colour.darker_gray()
        )
        embed.set_author(name=f"{user.name}#{user.discriminator}", icon_url=user.avatar)
        embed.set_image(url=user.avatar)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(
        name="servericon", description="Get the icon of the server you are in"
    )
    @app_commands.guild_only()
    @app_commands.checks.cooldown(1, 20, key=lambda i: (i.guild.id, i.user.id))
    async def servericon(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title=f"{interaction.guild.name}'s Icon",
            colour=discord.Colour.darker_gray(),
        )
        embed.set_author(
            name=f"{interaction.guild.name}", icon_url=interaction.guild.icon
        )
        embed.set_image(url=interaction.guild.icon)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(
        name="serverbanner", description="Get the banner of the server you are in"
    )
    @app_commands.guild_only()
    @app_commands.checks.cooldown(1, 20, key=lambda i: (i.guild.id, i.user.id))
    async def serverbanner(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title=f"{interaction.guild.name}'s Banner",
            colour=discord.Colour.darker_gray(),
        )
        embed.set_author(
            name=f"{interaction.guild.name}", icon_url=interaction.guild.icon
        )
        embed.set_image(url=interaction.guild.banner)
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Server(bot))
