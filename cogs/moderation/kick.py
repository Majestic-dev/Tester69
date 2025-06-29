import discord

from discord import app_commands
from discord.ext import commands

class kick(commands.Cog):
    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot

    @app_commands.command(name="kick", description="Kicks the mentioned user")
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(kick_members=True)
    @app_commands.checks.cooldown(1, 10, key=lambda i: (i.guild.id, i.user.id))
    @app_commands.describe(
        member="The user to kick",
        reason='The reason for kicking the user ("Unspecified" by default))',
    )
    async def kick(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        reason: str = "Unspecified",
    ):
        if member.id == interaction.user.id:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    description="<:white_cross:1096791282023669860> You can't kick yourself",
                    colour=discord.Colour.orange(),
                )
            )

        if interaction.user.top_role <= member.top_role:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    description="<:white_cross:1096791282023669860> You can't kick your superiors",
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

        else:
            try:
                await member.kick(reason=reason)
                await interaction.response.send_message(
                    embed=discord.Embed(
                        description=f"<:white_checkmark:1096793014287995061> Kicked {member.mention}",
                        colour=discord.Colour.green(),
                    )
                )

                self.bot.dispatch(
                    "kick",
                    kicker=interaction.user,
                    kicked=member,
                    reason=reason,
                )

                if await member.create_dm():
                    await member.dm_channel.send(
                        embed=discord.Embed(
                            description=f'You have been kicked from {interaction.guild.name} for "{reason}"',
                            colour=discord.Colour.red(),
                        )
                    )
                else:
                    pass

            except Exception:
                await interaction.response.send_message(
                    embed=discord.Embed(
                        description=f"<:white_cross:1096791282023669860> Could not kick {member.mention}",
                        colour=discord.Colour.orange(),
                    )
                )

async def setup(bot: commands.AutoShardedBot):
    await bot.add_cog(kick(bot))