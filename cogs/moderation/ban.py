import re
import discord

from discord import app_commands
from discord.ext import commands

from utils import data_manager


class ban(commands.Cog):
    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot

    @app_commands.command(name="ban", description="Bans the mentioned user")
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(ban_members=True)
    @app_commands.checks.cooldown(1, 10, key=lambda i: (i.guild.id, i.user.id))
    @app_commands.describe(
        member="The user to ban",
        reason='The reason for banning the user ("Unspecified" by default)',
    )
    async def ban(
        self,
        interaction: discord.Interaction,
        member: discord.User,
        reason: str = "Unspecified",
    ):
        guild_data = await data_manager.get_guild_data(interaction.guild.id)
        appeal_link = guild_data["appeal_link"]

        if member.id == interaction.user.id:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    description="<:white_cross:1096791282023669860> You can't ban yourself",
                    colour=discord.Colour.red(),
                )
            )

        elif (
            isinstance(member, discord.Member)
            and interaction.user.top_role <= member.top_role
        ):
            return await interaction.response.send_message(
                embed=discord.Embed(
                    description="<:white_cross:1096791282023669860> You can't ban your superiors",
                    colour=discord.Colour.red(),
                )
            )

        elif (
            isinstance(member, discord.Member)
            and member.guild_permissions.administrator
        ):
            return await interaction.response.send_message(
                embed=discord.Embed(
                    description="<:white_cross:1096791282023669860> That user is an adminstrator, I can't do that",
                    colour=discord.Colour.red(),
                )
            )

        bot = interaction.guild.get_member(self.bot.user.id)
        if isinstance(member, discord.Member) and bot.top_role <= member.top_role:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    description="<:white_cross:1096791282023669860> That user is higher than me, I can't do that",
                    colour=discord.Colour.red(),
                )
            )

        else:
            try:
                if appeal_link != None:
                    dm_channel = await member.create_dm()
                    try:
                        await dm_channel.send(
                            embed=discord.Embed(
                                title="You have been banned from the server",
                                description=f"You have been banned from {interaction.guild.nam}. Appeal for unban at {appeal_link}",
                                colour=discord.Colour.red(),
                            )
                        )
                    except:
                        pass
                await member.ban(reason=reason)
                await interaction.response.send_message(
                    embed=discord.Embed(
                        description=f"<:white_checkmark:1096793014287995061> Successfully banned {member.mention}",
                        colour=discord.Colour.green(),
                    )
                )

                self.bot.dispatch(
                    "ban",
                    guild=interaction.guild,
                    banner=interaction.user,
                    banned=member,
                    reason=reason,
                )

                try:
                    await member.create_dm()
                    await member.dm_channel.send(
                        embed=discord.Embed(
                            description=f'You have been banned from {interaction.guild.name} for "{reason}"',
                            colour=discord.Colour.red(),
                        )
                    )
                except:
                    pass

            except:
                await interaction.response.send_message(
                    embed=discord.Embed(
                        description=f"<:white_cross:1096791282023669860> Could not ban {member.mention}",
                        colour=discord.Colour.orange(),
                    )
                )

    @app_commands.command(
        name="unban",
        description="Unban the user by their discord ID or username",
    )
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(ban_members=True)
    @app_commands.checks.cooldown(1, 10, key=lambda i: (i.guild.id, i.user.id))
    @app_commands.describe(member="The user to unban (by ID or username)")
    async def unban(self, interaction: discord.Interaction, member: str):
        await interaction.response.defer()
        bans = [entry async for entry in interaction.guild.bans(limit=None)]
        for entry in bans:
            if member.isdigit() and self.bot.get_user(int(member)):
                if any(entry.user.id == int(member) for entry in bans):
                    await interaction.guild.unban(entry.user)
                    return await interaction.edit_original_response(
                        embed=discord.Embed(
                            description=f"<:white_checkmark:1096793014287995061> Successfully unbanned {entry.user.mention}",
                            colour=discord.Colour.green(),
                        )
                    )
                else:
                    return await interaction.edit_original_response(
                        embed=discord.Embed(
                            description="<:white_cross:1096791282023669860> Could not find that user",
                            colour=discord.Colour.red(),
                        )
                    )

            elif re.match(
                r"(?P<name>(?:[a-zA-Z0-9_]|(?<!\.)\.(?!\.)){2,32})(?P<disc>#[0-9]{0,4})?",
                member,
            ):
                if any(member in entry.user.name for entry in bans):
                    if any(member == entry.user.name for entry in bans):
                        await interaction.guild.unban(entry.user)
                        return await interaction.edit_original_response(
                            embed=discord.Embed(
                                description=f"<:white_checkmark:1096793014287995061> Successfully unbanned {entry.user.mention}",
                                colour=discord.Colour.green(),
                            )
                        )
                    else:
                        return await interaction.edit_original_response(
                            embed=discord.Embed(
                                description=(
                                    "<:white_cross:1096791282023669860> Could not find that user"
                                )
                                + (
                                    f", did you mean any of these similar usernames?\n\n {'\n'.join([f'* {entry.user.mention} - {entry.user.id} - {entry.user.name}' for entry in bans if member in entry.user.name])}"
                                    if len(
                                        [
                                            entry.user.name
                                            for entry in bans
                                            if member in entry.user.name
                                        ]
                                    )
                                    > 0
                                    else ""
                                ),
                                colour=discord.Colour.red(),
                            )
                        )
                else:
                    return await interaction.edit_original_response(
                        embed=discord.Embed(
                            description="<:white_cross:1096791282023669860> Could not find that user",
                            colour=discord.Colour.red(),
                        )
                    )
            else:
                return await interaction.edit_original_response(
                    embed=discord.Embed(
                        description="<:white_cross:1096791282023669860> Please enter a proper username",
                        colour=discord.Colour.red(),
                    )
                )
            
async def setup(bot: commands.AutoShardedBot):
    await bot.add_cog(ban(bot))