import asyncio
from datetime import datetime

import discord
from discord import app_commands
from discord.ext import commands

from utils import DataManager


class MuteSystem(commands.Cog):
    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot

    @app_commands.command(name="set_muted_role", description="Set the muted role")
    @app_commands.guild_only()
    @app_commands.default_permissions(manage_roles=True)
    @app_commands.checks.cooldown(1, 30, key=lambda i: (i.guild.id, i.user.id))
    @app_commands.describe(
        role="The role that will be assigned to users when muting them"
    )
    async def set_muted_role(
        self, interaction: discord.Interaction, role: discord.Role
    ):
        await interaction.response.send_message(
            embed=discord.Embed(
                description=f"<:white_checkmark:1096793014287995061> Set the muted role to {role.mention}",
                colour=discord.Colour.green(),
            )
        )
        DataManager.edit_guild_data(interaction.guild.id, "muted_role_id", role.id)

    @app_commands.command(name="mute", description="Mutes the mentioned user")
    @app_commands.guild_only()
    @app_commands.default_permissions(manage_roles=True)
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
        await interaction.response.defer()
        muted_role = DataManager.get_guild_data(interaction.guild.id)["muted_role_id"]

        if muted_role == None:
            return await interaction.edit_original_response(
                embed=discord.Embed(
                    description="<:white_cross:1096791282023669860> Please set a muted role first",
                    colour=discord.Colour.orange(),
                )
            )

        if member.id == interaction.user.id:
            return await interaction.edit_original_response(
                embed=discord.Embed(
                    description="<:white_cross:1096791282023669860> You can't mute yourself",
                    colour=discord.Colour.orange(),
                )
            )

        if interaction.user.top_role <= member.top_role:
            return await interaction.edit_original_response(
                embed=discord.Embed(
                    description="<:white_cross:1096791282023669860> You can't mute your superiors",
                    colour=discord.Colour.orange(),
                )
            )

        bot = interaction.guild.get_member(self.bot.user.id)
        if bot.top_role <= member.top_role:
            return await interaction.edit_original_response(
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
            await interaction.edit_original_response(
                embed=discord.Embed(
                    description=f"<:white_cross:1096791282023669860> Could not mute {member.mention} because they are already muted",
                    colour=discord.Colour.orange(),
                )
            )

        else:
            await member.edit(roles=[role])
            await interaction.edit_original_response(
                embed=discord.Embed(
                    description=f"<:white_checkmark:1096793014287995061> Muted {member.mention} for {duration} seconds",
                    colour=discord.Colour.green(),
                )
            )

            self.bot.dispatch(
                "mute",
                muter=interaction.user,
                muted=member,
                duration=duration,
                reason=reason,
            )

            try:
                await member.create_dm()
                await member.dm_channel.send(
                    embed=discord.Embed(
                        description=f'You have been muted in {interaction.guild.name} for {duration} seconds for "{reason}"',
                        colour=discord.Colour.orange(),
                    )
                )
            except:
                pass
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
    @app_commands.guild_only()
    @app_commands.default_permissions(manage_roles=True)
    @app_commands.checks.cooldown(1, 10, key=lambda i: (i.guild.id, i.user.id))
    @app_commands.describe(member="The user to unmute")
    async def unmute(self, interaction: discord.Interaction, member: discord.Member):
        muted_role = DataManager.get_guild_data(interaction.guild.id)["muted_role_id"]
        saved_roles = DataManager.get_guild_data(interaction.guild.id)[
            "muted_user_roles"
        ][str(member.id)]

        if saved_roles == None or len(saved_roles) == 0:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    description="<:white_cross:1096791282023669860> That user is not muted",
                    colour=discord.Colour.orange(),
                )
            )

        role = interaction.guild.get_role(muted_role)

        if role in member.roles:
            saved_roles1 = []
            for role in saved_roles:
                saved_roles1.append(interaction.guild.get_role(role))
            await member.edit(roles=saved_roles1)

            self.bot.dispatch(
                "unmute",
                unmuter=interaction.user,
                unmuted=member,
            )

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

async def setup(bot: commands.AutoShardedBot):
    await bot.add_cog(MuteSystem(bot))