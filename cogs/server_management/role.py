import discord
from discord import app_commands
from discord.ext import commands


class role(commands.Cog):
    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot

    @app_commands.command(name="role_info", description="Get information about a role")
    @app_commands.guild_only()
    @app_commands.checks.cooldown(1, 20, key=lambda i: (i.guild.id, i.user.id))
    @app_commands.describe(role="The role to get information about")
    async def roleinfo(
        self,
        interaction: discord.Interaction,
        role: discord.Role,
        ephemeral: bool = True,
    ):
        embed = discord.Embed(
            description=(
                f"* **Role Name**: {role.name}\n"
                f"* **Role ID**: `{role.id}`\n"
                f"* **Created At**: {discord.utils.format_dt(role.created_at, style='F')}\n"
                f"* **Displayed Separately From Other Roles**: {'Yes' if role.hoist else 'No'}\n"
                f"* **Position**: {role.position}\n"
                f"* **Mentionable By Anyone**: {'Yes' if role.mentionable else 'No'}\n"
                f"* **Members**: {len(role.members)}\n"
                f"* **Colour**: `{role.colour if role.colour != discord.Colour.default() else 'No Colour'}`\n"
            )
            + (
                f"* **Permissions**: {', '.join([perm.replace('_', ' ').title() for perm, value in role.permissions if value])}\n\n"
                if role.permissions
                else "* **Permissions**: This role has no permissions set for it.\n\n"
            )
            + (
                f"* **Members List**: {', '.join([member.mention for member in role.members])}"
            ),
            colour=(
                role.colour
                if role.colour != discord.Colour.default()
                else discord.Colour.blurple()
            ),
        )
        embed.set_thumbnail(url=role.icon)

        await interaction.response.send_message(embed=embed, ephemeral=ephemeral)

    @app_commands.command(name="add_role", description="Add a role to the mentioned user")
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(manage_roles=True)
    @app_commands.checks.cooldown(1, 7, key=lambda i: (i.guild.id, i.user.id))
    @app_commands.describe(
        user="The user to add the role to", role="The role to add to the user"
    )
    async def role_add(
        self,
        interaction: discord.Interaction,
        user: discord.Member,
        role: discord.Role,
    ):
        if role in user.roles:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    description="<:white_cross:1096791282023669860> That user already has that role",
                    colour=discord.Colour.red(),
                )
            )

        bot = interaction.guild.get_member(self.bot.user.id)
        if bot.top_role <= role:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    description="<:white_cross:1096791282023669860> I cannot add a role higher than my highest role",
                    colour=discord.Colour.red(),
                )
            )

        if interaction.user.top_role <= role:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    description="<:white_cross:1096791282023669860> You cannot add a role higher than your highest role",
                    colour=discord.Colour.red(),
                )
            )

        await interaction.response.send_message(
            embed=discord.Embed(
                description=f"<:white_checkmark:1096793014287995061> Added {role.mention} role to {user.mention}",
                colour=discord.Colour.green(),
            )
        )
        await user.add_roles(role)

    @app_commands.command(
        name="remove_role", description="Remove a role from the mentioned user"
    )
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(manage_roles=True)
    @app_commands.checks.cooldown(1, 7, key=lambda i: (i.guild.id, i.user.id))
    @app_commands.describe(
        user="The user to remove the role from", role="The role to remove from the user"
    )
    async def role_remove(
        self,
        interaction: discord.Interaction,
        user: discord.Member,
        role: discord.Role,
    ):
        if role not in user.roles:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    description="<:white_cross:1096791282023669860> That user does not have that role.",
                    colour=discord.Colour.red(),
                )
            )

        bot = interaction.guild.get_member(self.bot.user.id)
        if bot.top_role <= role:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    description="<:white_cross:1096791282023669860> I cannot remove a role that is higher than my highest role.",
                    colour=discord.Colour.red(),
                )
            )

        if interaction.user.top_role <= role:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    description="<:white_cross:1096791282023669860> You cannot remove a role that is higher than your highest role.",
                    colour=discord.Colour.red(),
                )
            )

        await interaction.response.send_message(
            embed=discord.Embed(
                description=f"<:white_checkmark:1096793014287995061> Removed {role.mention} role from {user.mention}",
                colour=discord.Colour.green(),
            )
        )
        await user.remove_roles(role)