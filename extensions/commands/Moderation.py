import asyncio
from datetime import datetime

import discord
from discord import app_commands
from discord.ext import commands

from utils import DataManager


class Moderation(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="set_muted_role", description="Set the muted role")
    @app_commands.default_permissions(manage_roles=True)
    async def set_muted_role(
        self, interaction: discord.Interaction, role: discord.Role
    ):
        await interaction.response.send_message(
            embed=discord.Embed(
                title="Muted Role Set",
                description=f"Set muted role to {role.mention}",
                colour=discord.Colour.green(),
            )
        )
        DataManager.edit_guild_data(interaction.guild.id, "muted_role_id", role.id)

    @app_commands.command(name="mute", description="Mutes the mentioned user")
    @app_commands.default_permissions(manage_roles=True)
    async def mute(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        duration: int,
        reason: str = "Unspecified",
    ):
        muted_role = DataManager.get_guild_data(interaction.guild.id)["muted_role_id"]

        if muted_role == None:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    description="<:white_cross:1096791282023669860> Please set a muted role first",
                    colour=discord.Colour.orange(),
                )
            )

        if member.id == interaction.user.id:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    description="<:white_cross:1096791282023669860> You can't mute yourself",
                    colour=discord.Colour.orange(),
                )
            )

        if interaction.user.top_role.position <= member.top_role.position:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    description="<:white_cross:1096791282023669860> You can't mute your superiors",
                    colour=discord.Colour.orange(),
                )
            )

        bot = interaction.guild.get_member(self.bot.user.id)
        if bot.top_role.position <= member.top_role.position:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    description="<:white_cross:1096791282023669860> That user is higher than me, I can't do that",
                    colour=discord.Colour.orange(),
                )
            )

        muted_user_roles = DataManager.get_guild_data(interaction.guild.id)[
            "muted_user_roles"
        ]
        if str(member.id) not in muted_user_roles:
            muted_user_roles[str(member.id)] = []

        saved_roles = DataManager.get_guild_data(interaction.guild.id)[
            "muted_user_roles"
        ][str(member.id)]
        for role in member.roles:
            if (
                role.name != "@everyone"
                and role.id != muted_role
                and role.id not in saved_roles
            ):
                DataManager.save_roles(interaction.guild.id, member.id, role.id)

        role = interaction.guild.get_role(muted_role)
        if role in member.roles:
            await interaction.response.send_message(
                embed=discord.Embed(
                    description=f"<:white_cross:1096791282023669860> Could not mute {member.mention} because they are already muted",
                    colour=discord.Colour.orange(),
                )
            )
        else:
            await member.edit(roles=[role])
            await interaction.response.send_message(
                embed=discord.Embed(
                    description=f"<:white_checkmark:1096793014287995061> Muted {member.mention} for {duration} seconds",
                    colour=discord.Colour.green(),
                )
            )
            if duration == 0:
                return
            await asyncio.sleep(duration)
            saved_roles1 = []
            roles = DataManager.get_guild_data(interaction.guild.id)["muted_user_roles"]
            for role in saved_roles:
                saved_roles1.append(interaction.guild.get_role(role))
            await member.edit(roles=saved_roles1)
            roles.pop(str(member.id))
            DataManager.save("guilds")

    @app_commands.command(name="unmute", description="Unmutes the mentioned user")
    @app_commands.default_permissions(manage_roles=True)
    async def unmute(self, interaction: discord.Interaction, member: discord.Member):
        muted_role = DataManager.get_guild_data(interaction.guild.id)["muted_role_id"]
        saved_roles = DataManager.get_guild_data(interaction.guild.id)[
            "muted_user_roles"
        ][str(member.id)]

        if muted_role in member.roles:
            saved_roles1 = []
            for role in saved_roles:
                saved_roles1.append(interaction.guild.get_role(role))
            await member.edit(roles=saved_roles1)
            await interaction.response.send_message(
                embed=discord.Embed(
                    description=f"Successfully unmuted {member.mention}",
                    colour=discord.Colour.green(),
                )
            )
        else:
            await interaction.response.send_message(
                embed=discord.Embed(
                    description=f"<:white_cross:1096791282023669860> Could not unmute {member.mention} because they are not muted",
                    colour=discord.Colour.orange(),
                )
            )

    @app_commands.command(name="kick", description="Kicks the mentioned user")
    @app_commands.default_permissions(kick_members=True)
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

        if interaction.user.top_role.position <= member.top_role.position:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    description="<:white_cross:1096791282023669860> You can't kick your superiors",
                    colour=discord.Colour.orange(),
                )
            )

        bot = interaction.guild.get_member(self.bot.user.id)
        if bot.top_role.position <= member.top_role.position:
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
            except Exception as exc:
                print(exc)
                await interaction.response.send_message(
                    embed=discord.Embed(
                        description=f"<:white_cross:1096791282023669860> Could not kick {member.mention}",
                        colour=discord.Colour.orange(),
                    )
                )

    @app_commands.command(name="ban", description="Bans the mentioned user")
    @app_commands.default_permissions(ban_members=True)
    async def ban(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        reason: str = "Unspecified",
    ):
        if member.id == interaction.user.id:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    description="<:white_cross:1096791282023669860> You can't ban yourself",
                    colour=discord.Colour.red(),
                )
            )

        if interaction.user.top_role.position <= member.top_role.position:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    description="<:white_cross:1096791282023669860> You can't ban your superiors",
                    colour=discord.Colour.red(),
                )
            )

        if member.guild_permissions.administrator:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    description="<:white_cross:1096791282023669860> That user is an adminstrator, I can't do that",
                    colour=discord.Colour.red(),
                )
            )

        bot = interaction.guild.get_member(self.bot.user.id)
        if bot.top_role.position <= member.top_role.position:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    description="<:white_cross:1096791282023669860> That user is higher than me, I can't do that",
                    colour=discord.Colour.red(),
                )
            )

        else:
            try:
                await member.ban(reason=reason)
                await interaction.response.send_message(
                    embed=discord.Embed(
                        description=f"<:white_checkmark:1096793014287995061> Successfully banned {member.mention}",
                        colour=discord.Colour.green(),
                    )
                )
            except:
                await interaction.response.send_message(
                    embed=discord.Embed(
                        description=f"<:white_cross:1096791282023669860> Could not ban {member.mention}",
                        colour=discord.Colour.orange(),
                    )
                )

    @app_commands.command(
        name="unban",
        description="Unbans the user by their discord ID",
    )
    @app_commands.default_permissions(ban_members=True)
    async def unban(self, interaction: discord.Interaction, member: int):
        member = await self.bot.fetch_user(member)

        async for ban in interaction.guild.bans():
            if ban.user.id == int(member):
                await interaction.guild.unban(ban.user)
                return await interaction.response.send_message(
                    embed=discord.Embed(
                        description=f"<:white_checkmark:1096793014287995061> unbanned {member.mention}",
                        colour=discord.Colour.green(),
                    )
                )

        await interaction.response.send_message(
            embed=discord.Embed(
                description=f"<:white_cross:1096791282023669860> Could not unban {member} because they are not banned",
                colour=discord.Colour.orange(),
            )
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(Moderation(bot))
