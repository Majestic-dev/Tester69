import datetime
import discord

from discord import app_commands
from discord.ext import commands


class timeout(commands.Cog):
    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot

    @app_commands.command(name="timeout", description="Timeouts the mentioned user")
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(manage_roles=True)
    @app_commands.checks.cooldown(1, 10, key=lambda i: (i.guild.id, i.user.id))
    @app_commands.describe(
        member="The user to mute",
        duration="The duration to mute the user for (in seconds)",
        reason='The reason for muting the user ("Unspecified" by default)',
    )
    async def mute(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        duration: int,
        reason: str = "Unspecified",
    ):
        if member.id == interaction.user.id:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    description="<:white_cross:1096791282023669860> You can't timeout yourself",
                    colour=discord.Colour.orange(),
                )
            )

        if interaction.user.top_role <= member.top_role:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    description="<:white_cross:1096791282023669860> You can't timeout your superiors",
                    colour=discord.Colour.orange(),
                )
            )

        bot = interaction.guild.get_member(self.bot.user.id)
        if bot.top_role <= member.top_role:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    description="<:white_cross:1096791282023669860> That user is higher than me, I can't do that",
                    colour=discord.Colour.orange(),
                )
            )

        if member.is_timed_out():
            return await interaction.response.send_message(
                embed=discord.Embed(
                    description="<:white_cross:1096791282023669860> That user is already timed out",
                    colour=discord.Colour.orange(),
                )
            )

        else:
            await member.timeout(datetime.timedelta(seconds=duration), reason=reason)
            await interaction.response.send_message(
                embed=discord.Embed(
                    description=f"<:white_checkmark:1096793014287995061> Successfully timed out {member.mention}",
                    colour=discord.Colour.green(),
                )
            )

            self.bot.dispatch(
                "timeout",
                guild=interaction.guild,
                timeouter=interaction.user,
                timeouted=member,
                timedout_until=duration,
                reason=reason,
            )

    @app_commands.command(
        name="untimeout", description="Removes the timeout from the mentioned user"
    )
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(manage_roles=True)
    @app_commands.checks.cooldown(1, 10, key=lambda i: (i.guild.id, i.user.id))
    @app_commands.describe(member="The user to remove the timeout from")
    async def untimeout(self, interaction: discord.Interaction, member: discord.Member):
        if member.id == interaction.user.id:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    description="<:white_cross:1096791282023669860> You can't do this to yourself",
                    colour=discord.Colour.orange(),
                )
            )

        if interaction.user.top_role <= member.top_role:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    description="<:white_cross:1096791282023669860> You can't remove a timeout your superiors",
                    colour=discord.Colour.orange(),
                )
            )

        bot = interaction.guild.get_member(self.bot.user.id)
        if bot.top_role <= member.top_role:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    description="<:white_cross:1096791282023669860> That user is higher than me, I can't do that",
                    colour=discord.Colour.orange(),
                )
            )

        if member.is_timed_out():
            await member.timeout(None, reason="Untimeout")
            await interaction.response.send_message(
                embed=discord.Embed(
                    description=f"<:white_checkmark:1096793014287995061> Successfully removed the timeout from {member.mention}",
                    colour=discord.Colour.green(),
                )
            )

        elif member.is_timed_out() == False:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    description=f"<:white_cross:1096791282023669860> That user is not timed out",
                    colour=discord.Colour.orange(),
                )
            )


async def setup(bot: commands.AutoShardedBot):
    await bot.add_cog(timeout(bot))
