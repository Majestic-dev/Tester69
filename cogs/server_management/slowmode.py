from typing import Optional

import discord
from discord.ext import commands

from discord import app_commands


class slowmode(commands.Cog):
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


async def setup(bot: commands.AutoShardedBot):
    await bot.add_cog(slowmode(bot))
