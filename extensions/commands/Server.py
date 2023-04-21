import random
from datetime import datetime

import discord
from discord import app_commands
from discord.ext import commands


class Server(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="serverinfo", description="Get information about the server"
    )
    @app_commands.checks.cooldown(1, 20, key=lambda i: (i.guild.id, i.user.id))
    async def serverinfo(self, interaction: discord.Interaction):
        guild = interaction.guild
        embed = discord.Embed(title=f"Server Info", colour=discord.Colour.random())

        embed.set_thumbnail(url=guild.icon)
        embed.set_author(name=guild.name, icon_url=guild.icon)
        embed.add_field(name="Owner", value=guild.owner.name, inline=True)
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

    @serverinfo.error
    async def on_serverinfo_error(
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
        name="membercount", description="Get the member count of the server"
    )
    @app_commands.checks.cooldown(1, 20, key=lambda i: (i.guild.id, i.user.id))
    async def membercount(self, interaction: discord.Interaction):
        guild = interaction.guild
        embed = discord.Embed(
            title=f"Member Count",
            description=f"Total Members: {guild.member_count}",
            colour=discord.Colour.random(),
        )
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Server(bot))
