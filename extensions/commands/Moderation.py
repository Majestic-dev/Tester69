from datetime import datetime

import discord
from discord import app_commands
from discord.ext import commands

from utils import DataManager


class Moderation(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="mute", description="Mutes the mentioned user")
    @commands.has_permissions(kick_members=True)
    async def mute(
        self,
        interaction: discord.Interaction,
        member: discord.Member = None,
        *,
        reason: str = "Unspecified",
    ):
        if member == None:
            Mute = discord.Embed(
                title="Mute",
                description="Mutes the user by their discord user ID \n Example: `'Mute 705435835306213418 Not cool`",
                timestamp=datetime.utcnow(),
                colour=discord.Colour.light_gray(),
            )

            await interaction.response.send_message(embed=Mute)

        else:
            MuteA = discord.Embed(
                title=":warning: Error :warning:",
                description=(f"Could not mute {member} because they are already muted"),
                timestamp=datetime.utcnow(),
                colour=discord.Colour.dark_orange(),
            )

            MuteB = discord.Embed(
                title=":white_check_mark: Mute Successful :white_check_mark:",
                description=(f"Successfully muted {member}"),
                timestamp=datetime.utcnow(),
                colour=discord.Colour.red(),
            )

            role = discord.utils.get(interaction.guild.roles, name="muted")

            if role in member.roles:
                await interaction.response.send_message(embed=MuteA)
            else:
                await member.add_roles(role)
                await interaction.response.send_message(embed=MuteB)

    @app_commands.command(name="unmute", description="Unmutes the mentioned user")
    @commands.has_permissions(kick_members=True)
    async def unmute(
        self, interaction: discord.Interaction, member: discord.Member = None
    ):
        if member == None:
            Unmute = discord.Embed(
                title="Unmute",
                description="Unmutes the user by their discord user ID \n Example: `'Unmute 705435835306213418 Very cool`",
                timestamp=datetime.utcnow(),
                colour=discord.Colour.light_gray(),
            )

            await interaction.response.send_message(embed=Unmute)

        else:
            UnmuteA = discord.Embed(
                title=":warning: Error :warning:",
                description=(f"Could not unmute {member} because they are not muted"),
                timestamp=datetime.utcnow(),
                colour=discord.Colour.dark_orange(),
            )

            UnmuteB = discord.Embed(
                title=":white_check_mark: Unmute Successful :white_check_mark:",
                description=(f"Successfully unmuted {member}"),
                timestamp=datetime.utcnow(),
                colour=discord.Colour.green(),
            )

            role = discord.utils.get(interaction.guild.roles, name="muted")

            if role in member.roles:
                await member.remove_roles(role)
                await interaction.response.send_message(embed=UnmuteB)
            else:
                await interaction.response.send_message(embed=UnmuteA)

    @app_commands.command(name="kick", description="Kicks the mentioned user")
    @commands.has_permissions(kick_members=True)
    async def kick(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        reason: str = "Unspecified",
    ):
        if member == None:
            Kick = discord.Embed(
                title="Kick",
                description="kicks the user by their discord user ID \n Example: `'Kick 705435835306213418 Not cool`",
                timestamp=datetime.utcnow(),
                colour=discord.Colour.light_gray(),
            )

            await interaction.response.send_message(embed=Kick)

        else:
            KickA = discord.Embed(
                title=":white_check_mark: Kick Successful :white_check_mark:",
                description=(f"Successfully kicked {member}"),
                timestamp=datetime.utcnow(),
                colour=discord.Colour.red(),
            )

            KickB = discord.Embed(
                title=":warning: Error :warning:",
                description=(
                    f"Couldn't kick {member}, they might be higher than me or not in the server"
                ),
                timestamp=datetime.utcnow(),
                colour=discord.Colour.dark_orange(),
            )

            if member.id == interaction.user.id:
                await interaction.response.send_message("You cannot kick yourself!")

            else:
                try:
                    await member.kick(reason=reason)
                    await interaction.response.send_message(embed=KickA)
                except Exception as exc:
                    print(exc)
                    await interaction.response.send_message(embed=KickB)

    @app_commands.command(name="ban", description="Bans the mentioned user")
    @commands.has_permissions(ban_members=True)
    async def ban(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        reason: str = "Unspecified",
    ):
        if member == None:
            Ban = discord.Embed(
                title="Ban",
                description="Bans the user by their discord user ID \n Example: `'ban 705435835306213418 Not cool`",
                timestamp=datetime.utcnow(),
                colour=discord.Colour.light_gray(),
            )

            await interaction.response.send_message(embed=Ban)

        else:
            BanA = discord.Embed(
                title=":white_check_mark: Ban Successful :white_check_mark:",
                description=(f"Successfully banned {member}"),
                timestamp=datetime.utcnow(),
                colour=discord.Colour.red(),
            )

            BanB = discord.Embed(
                title=":warning: Error :warning:",
                description=(
                    f"Could not ban {member}, they might be higher than me or not in the server"
                ),
                timestamp=datetime.utcnow(),
                colour=discord.Colour.dark_orange(),
            )

            if member.id == interaction.user.id:
                await interaction.response.send_message("You cannot ban yourself!")

            else:
                try:
                    await member.ban(reason=reason)
                    await interaction.response.send_message(embed=BanA)
                except:
                    await interaction.response.send_message(embed=BanB)

    @app_commands.command(
        name="unban",
        description="Unbans the mentioned user (Has to be discord user ID)",
    )
    @commands.has_permissions(ban_members=True)
    async def unban(self, interaction: discord.Interaction, member: str):
        member = int(member)
        if member == None:
            Unban = discord.Embed(
                title="Unban",
                description="Unbans the user by their discord user ID \n Example: `'unban 705435835306213418 Very cool`",
                timestamp=datetime.utcnow(),
                colour=discord.Colour.light_gray(),
            )

            await interaction.response.send_message(embed=Unban)

        else:
            UnbanA = discord.Embed(
                title=":white_check_mark: Unban Successful :white_check_mark:",
                description=(f"Successfully unbanned <@{member}>"),
                timestamp=datetime.utcnow(),
                colour=discord.Colour.green(),
            )

            UnbanB = discord.Embed(
                title=":warning: Error :warning:",
                description=(
                    f"Could not unban <@{member}> because they are not banned"
                ),
                timestamp=datetime.utcnow(),
                colour=discord.Colour.dark_orange(),
            )

            async for ban in interaction.guild.bans():
                if ban.user.id == int(member):
                    await interaction.guild.unban(ban.user)
                    return await interaction.response.send_message(embed=UnbanA)

            await interaction.response.send_message(embed=UnbanB)


async def setup(bot: commands.Bot):
    await bot.add_cog(Moderation(bot))
